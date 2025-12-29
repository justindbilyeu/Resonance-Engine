"""
Bundle 0001 — RFO Ringing Wedge
Executable experiment implementation per OPERATIONALIZE.md + PREREG.yaml.

Design goals:
- Pure numpy + pyyaml (no scipy required)
- Deterministic seeds (stable hash, not Python's salted hash)
- Produces required outputs:
  - grid.csv
  - wedge_report.md
  - parameters_used.json
  - seed_manifest.json
  - null_evaluation.json
- Quick mode for smoke tests (tiny grid, short run)

NOTE:
The prereg sweep (81x61x3 with 200k steps) is computationally enormous.
This implementation is honest about runtime: use --quick or --max-points for development.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import yaml


# ----------------------------
# Utilities
# ----------------------------

def stable_seed(base_seed: int, K: float, gamma: float, rep: int) -> int:
    """Deterministic seed rule: base_seed + hash(K,gamma,rep) mod 1e9."""
    s = f"{K:.6f},{gamma:.6f},{rep}".encode("utf-8")
    h = hashlib.sha256(s).hexdigest()
    x = int(h[:16], 16)  # take 64 bits
    return int((base_seed + (x % 1_000_000_000)) % 1_000_000_000)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def robust_mad(x: np.ndarray, eps: float = 1e-12) -> float:
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return float(mad + eps)


def count_upward_crossings(z: np.ndarray, thr: float = 1.0) -> int:
    """Count upward crossings of z above thr."""
    if z.size < 2:
        return 0
    prev = z[:-1]
    curr = z[1:]
    return int(np.sum((prev <= thr) & (curr > thr)))


# ----------------------------
# Welch PSD (pure NumPy)
# ----------------------------

def welch_psd(x: np.ndarray, fs: float, nperseg: int = 256, noverlap: int = 128) -> Tuple[np.ndarray, np.ndarray]:
    """
    Minimal Welch PSD for 1D signal x.
    Returns (freqs, psd). Uses Hann window.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    if n < 8:
        freqs = np.array([0.0])
        psd = np.array([0.0])
        return freqs, psd

    nperseg = int(min(nperseg, n))
    noverlap = int(min(noverlap, max(0, nperseg - 1)))
    step = nperseg - noverlap
    if step <= 0:
        step = max(1, nperseg // 2)

    window = np.hanning(nperseg)
    win_norm = np.sum(window**2)

    # Segment start indices
    starts = list(range(0, n - nperseg + 1, step))
    if not starts:
        starts = [0]

    psd_accum = None
    for st in starts:
        seg = x[st:st + nperseg]
        seg = seg - np.mean(seg)
        segw = seg * window
        X = np.fft.rfft(segw)
        P = (np.abs(X) ** 2) / (fs * win_norm)
        psd_accum = P if psd_accum is None else (psd_accum + P)

    psd = psd_accum / len(starts)
    freqs = np.fft.rfftfreq(nperseg, d=1.0 / fs)
    return freqs, psd


def psd_peak_prominence_db(freqs: np.ndarray, psd: np.ndarray) -> float:
    """
    Δ_PSD_dB = 10*log10(P_peak / P_base)
    Excludes DC bin (freq=0).
    """
    if psd.size < 2:
        return 0.0
    # Exclude DC
    psd_ndc = psd[1:]
    if np.all(psd_ndc <= 0):
        return 0.0
    P_peak = float(np.max(psd_ndc))
    P_base = float(np.median(psd_ndc))
    if P_base <= 0:
        return 0.0
    return float(10.0 * math.log10(P_peak / P_base))


# ----------------------------
# RFO simulation
# ----------------------------

@dataclass
class PointResult:
    K: float
    gamma: float
    rep: int
    seed: int
    r_mean: float
    delta_psd_db: float
    n_over: int
    ring_label: bool
    invalid: bool
    reason: str = ""


def simulate_point(
    *,
    N: int,
    K: float,
    gamma: float,
    rep: int,
    dt: float,
    steps_total: int,
    steps_burnin: int,
    steps_measure: int,
    omega_mean: float,
    omega_std: float,
    D: float,
    Omega: float,
    plasticity_enabled: bool,
    alpha: float,
    beta: float,
    W_init_value: float,
    W_max: float,
    seed: int,
    # thresholds for point-level ringing label
    thr_psd_db: float,
    thr_n_over: int,
    thr_r_mean: float,
) -> Tuple[PointResult, Dict[str, float]]:
    """
    Run one (K,gamma,rep) simulation and compute metrics over measurement window.
    Returns PointResult and a small dict of metrics.
    """
    rng = np.random.default_rng(seed)

    # Initialize
    theta = rng.uniform(0.0, 2.0 * np.pi, size=N)
    omega = rng.normal(loc=omega_mean, scale=omega_std, size=N).astype(float)

    W = np.full((N, N), float(W_init_value), dtype=float)
    np.fill_diagonal(W, 0.0)

    sigma = float(gamma * math.sqrt(dt))
    fs = 1.0 / dt

    r_series: List[float] = []
    R_series: List[float] = []

    try:
        t = 0.0
        for step in range(steps_total):
            # Coupling term: (K/N) * sum_j W_ij * sin(theta_j - theta_i)
            # Build sin(theta_j - theta_i) as sin(theta[None,:] - theta[:,None])
            dtheta = theta[None, :] - theta[:, None]
            sin_d = np.sin(dtheta)

            coupling = (K / N) * np.sum(W * sin_d, axis=1)

            drive = D * np.sin(Omega * t - theta)
            noise = rng.normal(0.0, sigma, size=N) if sigma > 0 else 0.0

            dtheta_dt = omega + coupling + drive
            theta = theta + dt * dtheta_dt + noise

            # Wrap phase to keep numbers stable
            theta = np.mod(theta, 2.0 * np.pi)

            # Plasticity update
            if plasticity_enabled and alpha != 0.0:
                hebb = alpha * np.cos(dtheta)
                W = W + dt * (hebb - beta * W)
                # Clip and no self-coupling
                W = np.clip(W, 0.0, W_max)
                np.fill_diagonal(W, 0.0)

            # Collect metrics after burn-in
            if step >= steps_burnin:
                # r(t)
                z = np.exp(1j * theta)
                r = np.abs(np.mean(z))
                r_series.append(float(r))

                # R(t) = std(W)/mean(W)
                m = float(np.mean(W))
                s = float(np.std(W))
                R = s / (m + 1e-12)
                R_series.append(float(R))

            t += dt

        r_arr = np.asarray(r_series, dtype=float)
        R_arr = np.asarray(R_series, dtype=float)

        if r_arr.size == 0 or R_arr.size == 0:
            pr = PointResult(K, gamma, rep=-1, seed=seed, r_mean=0.0, delta_psd_db=0.0,
                             n_over=0, ring_label=False, invalid=True, reason="empty_measure_window")
            return pr, {}

        r_mean = float(np.mean(r_arr))

        freqs, psd = welch_psd(r_arr, fs=fs, nperseg=256, noverlap=128)
        delta_db = psd_peak_prominence_db(freqs, psd)

        medR = float(np.median(R_arr))
        madR = robust_mad(R_arr)
        zR = (R_arr - medR) / madR
        n_over = count_upward_crossings(zR, thr=1.0)

        ring_label = (delta_db >= thr_psd_db) and (n_over >= thr_n_over) and (r_mean >= thr_r_mean)

        pr = PointResult(
            K=float(K),
            gamma=float(gamma),
            rep=int(rep),
            seed=int(seed),
            r_mean=float(r_mean),
            delta_psd_db=float(delta_db),
            n_over=int(n_over),
            ring_label=bool(ring_label),
            invalid=False,
            reason="",
        )
        metrics = {
            "r_mean": r_mean,
            "Delta_PSD_dB": delta_db,
            "N_over": float(n_over),
        }
        return pr, metrics

    except FloatingPointError as e:
        pr = PointResult(K, gamma, rep=int(rep), seed=seed, r_mean=0.0, delta_psd_db=0.0,
                         n_over=0, ring_label=False, invalid=True, reason=f"floating_point:{e}")
        return pr, {}
    except Exception as e:
        pr = PointResult(K, gamma, rep=int(rep), seed=seed, r_mean=0.0, delta_psd_db=0.0,
                         n_over=0, ring_label=False, invalid=True, reason=f"exception:{e}")
        return pr, {}


# ----------------------------
# Grid aggregation + null evaluation
# ----------------------------

def majority_vote(labels: List[bool]) -> bool:
    if not labels:
        return False
    return sum(1 for x in labels if x) >= (len(labels) // 2 + 1)


def largest_connected_component_size(mask: np.ndarray) -> int:
    """4-neighbor connectivity."""
    H, W = mask.shape
    visited = np.zeros_like(mask, dtype=bool)

    def neighbors(r: int, c: int):
        if r > 0: yield (r - 1, c)
        if r + 1 < H: yield (r + 1, c)
        if c > 0: yield (r, c - 1)
        if c + 1 < W: yield (r, c + 1)

    best = 0
    for r in range(H):
        for c in range(W):
            if not mask[r, c] or visited[r, c]:
                continue
            # BFS
            q = [(r, c)]
            visited[r, c] = True
            size = 0
            while q:
                rr, cc = q.pop()
                size += 1
                for nr, nc in neighbors(rr, cc):
                    if mask[nr, nc] and not visited[nr, nc]:
                        visited[nr, nc] = True
                        q.append((nr, nc))
            best = max(best, size)
    return int(best)


def eval_nulls(
    *,
    grid_mask: np.ndarray,
    K_values: np.ndarray,
    gamma_values: np.ndarray,
    # thresholds
    null2_area_frac_min: float = 0.02,
    null2_cc_min: int = 20,
    null3_span_frac_max: float = 0.60,
    negative_control_mask: np.ndarray | None = None,
    null4_area_ratio_min: float = 0.80,
) -> Dict[str, dict]:
    """
    Implements NULLS.md logic (Null1 handled pointwise during labeling).
    Returns dict keyed by null name -> result dict {pass/fail/skip, details}.
    """
    H, W = grid_mask.shape
    total = H * W
    S = int(np.sum(grid_mask))
    area_frac = S / total if total > 0 else 0.0
    cc = largest_connected_component_size(grid_mask)

    # Null 2
    null2_fail = (area_frac < null2_area_frac_min) or (cc < null2_cc_min)
    null2 = {
        "name": "null2_region_minimums",
        "fail": bool(null2_fail),
        "details": {
            "area_frac": float(area_frac),
            "area_frac_min": float(null2_area_frac_min),
            "largest_cc_size": int(cc),
            "largest_cc_min": int(null2_cc_min),
        },
    }

    # Null 3
    K_min = float(np.min(K_values))
    K_max = float(np.max(K_values))
    K_range = max(1e-12, K_max - K_min)

    row_spans_ok = False
    for gi in range(H):
        cols = np.where(grid_mask[gi, :])[0]
        if cols.size == 0:
            continue
        Ks = K_values[cols]
        span_frac = float((np.max(Ks) - np.min(Ks)) / K_range)
        if 0.0 < span_frac <= null3_span_frac_max:
            row_spans_ok = True
            break

    null3_fail = not row_spans_ok
    null3 = {
        "name": "null3_unbounded_or_empty_rows",
        "fail": bool(null3_fail),
        "details": {
            "span_frac_max": float(null3_span_frac_max),
            "row_spans_ok": bool(row_spans_ok),
        },
    }

    # Null 4
    if negative_control_mask is None:
        null4 = {
            "name": "null4_negative_control",
            "skip": True,
            "reason": "negative control not run (disabled or quick mode)",
        }
    else:
        S_nc = int(np.sum(negative_control_mask))
        # Reject if S_nc >= 0.8 * S
        fail = (S > 0) and (S_nc >= null4_area_ratio_min * S)
        null4 = {
            "name": "null4_negative_control",
            "fail": bool(fail),
            "details": {
                "S": int(S),
                "S_nc": int(S_nc),
                "ratio": float(S_nc / max(1, S)),
                "ratio_min": float(null4_area_ratio_min),
            },
        }

    return {
        "null2": null2,
        "null3": null3,
        "null4": null4,
    }


# ----------------------------
# Main run
# ----------------------------

def build_grid(minv: float, maxv: float, num: int) -> np.ndarray:
    if num <= 1:
        return np.array([float(minv)], dtype=float)
    return np.linspace(float(minv), float(maxv), int(num), dtype=float)


def quick_grid(K_min: float, K_max: float, gamma_min: float, gamma_max: float) -> Tuple[np.ndarray, np.ndarray]:
    # 3x3 grid: corners + mid
    K_vals = np.array([K_min, 0.5 * (K_min + K_max), K_max], dtype=float)
    g_vals = np.array([gamma_min, 0.5 * (gamma_min + gamma_max), gamma_max], dtype=float)
    return K_vals, g_vals


def run_bundle(config_path: Path, outdir: Path, quick: bool, no_negative_control: bool, max_points: int | None) -> None:
    cfg = read_yaml(config_path)

    # Load prereg parameters
    dt = float(cfg["model"]["dynamics"]["dt"])
    steps_total = int(cfg["model"]["dynamics"]["steps_total"])
    steps_burnin = int(cfg["model"]["dynamics"]["steps_burnin"])
    steps_measure = int(cfg["model"]["dynamics"]["steps_measure"])

    N = int(cfg["model"]["network"]["N"])
    omega_mean = float(cfg["model"]["network"]["omega_params"]["mean"])
    omega_std = float(cfg["model"]["network"]["omega_params"]["std"])

    D = float(cfg["model"]["drive"]["D"])
    Omega = float(cfg["model"]["drive"]["Omega"])

    alpha = float(cfg["model"]["plasticity"]["alpha"])
    beta = float(cfg["model"]["plasticity"]["beta"])
    W_max = float(cfg["model"]["plasticity"]["W_max"])
    W_init_value = float(cfg["model"]["plasticity"]["W_init_value"])

    base_seed = int(cfg["sweep"]["seeds"]["base_seed"])
    reps = int(cfg["sweep"]["replicates_per_point"])

    # Point-level thresholds from NULLS.md (locked here as well)
    thr_psd_db = 6.0
    thr_n_over = 2
    thr_r_mean = 0.35

    # Grid
    K_spec = cfg["sweep"]["grid"]["K"]
    g_spec = cfg["sweep"]["grid"]["gamma"]

    K_full = build_grid(K_spec["min"], K_spec["max"], K_spec["num"])
    g_full = build_grid(g_spec["min"], g_spec["max"], g_spec["num"])

    deviations: Dict[str, str] = {}

    if quick:
        # Make quick actually usable: tiny steps + 3x3 grid + 1 replicate
        K_vals, g_vals = quick_grid(float(K_spec["min"]), float(K_spec["max"]), float(g_spec["min"]), float(g_spec["max"]))
        steps_total_q = 1000
        steps_burnin_q = 200
        steps_measure_q = steps_total_q - steps_burnin_q
        reps_q = 1

        deviations["mode"] = "quick"
        deviations["steps_total"] = f"{steps_total} -> {steps_total_q}"
        deviations["steps_burnin"] = f"{steps_burnin} -> {steps_burnin_q}"
        deviations["steps_measure"] = f"{steps_measure} -> {steps_measure_q}"
        deviations["replicates_per_point"] = f"{reps} -> {reps_q}"
        deviations["grid"] = f"{K_full.size}x{g_full.size} -> {K_vals.size}x{g_vals.size}"

        steps_total, steps_burnin, steps_measure, reps = steps_total_q, steps_burnin_q, steps_measure_q, reps_q
    else:
        K_vals, g_vals = K_full, g_full

    ensure_dir(outdir)

    # Seed manifest
    seed_manifest: List[dict] = []

    # Accumulate per-replicate results
    all_point_results: List[PointResult] = []

    total_points = K_vals.size * g_vals.size
    # Optional cap for development sanity
    cap = max_points if (max_points is not None and max_points > 0) else None

    point_counter = 0
    for gi, gamma in enumerate(g_vals):
        for ki, K in enumerate(K_vals):
            point_counter += 1
            if cap is not None and point_counter > cap:
                break

            rep_labels: List[bool] = []
            rep_metrics: List[Tuple[float, float, int]] = []
            invalid_any = False
            invalid_reasons: List[str] = []

            for rep in range(reps):
                seed = stable_seed(base_seed, float(K), float(gamma), int(rep))
                seed_manifest.append({"K": float(K), "gamma": float(gamma), "rep": int(rep), "seed": int(seed)})

                pr, _ = simulate_point(
                    N=N, K=float(K), gamma=float(gamma), rep=rep,
                    dt=dt, steps_total=steps_total, steps_burnin=steps_burnin, steps_measure=steps_measure,
                    omega_mean=omega_mean, omega_std=omega_std,
                    D=D, Omega=Omega,
                    plasticity_enabled=True, alpha=alpha, beta=beta,
                    W_init_value=W_init_value, W_max=W_max,
                    seed=seed,
                    thr_psd_db=thr_psd_db, thr_n_over=thr_n_over, thr_r_mean=thr_r_mean,
                )
                all_point_results.append(pr)
                if pr.invalid:
                    invalid_any = True
                    invalid_reasons.append(pr.reason)
                rep_labels.append(pr.ring_label)
                rep_metrics.append((pr.r_mean, pr.delta_psd_db, pr.n_over))

            # Majority vote for grid label
            # If invalids occur, we still vote, but record invalid status in CSV
            # (stopping_rules in PREREG covers invalid_rate > 1% at sweep level; not enforced here yet)
            _ = majority_vote(rep_labels)

        if cap is not None and point_counter > cap:
            break

    # Aggregate to grid with majority vote (by point)
    # Build a dict keyed by (gamma_index, K_index) -> list of replicates
    # We reconstruct the grid by grouping results per (K,gamma).
    point_map: Dict[Tuple[float, float], List[PointResult]] = {}
    for pr in all_point_results:
        key = (float(pr.K), float(pr.gamma))
        point_map.setdefault(key, []).append(pr)

    H = g_vals.size
    W = K_vals.size
    grid_mask = np.zeros((H, W), dtype=bool)

    grid_rows: List[dict] = []
    for gi, gamma in enumerate(g_vals):
        for ki, K in enumerate(K_vals):
            key = (float(K), float(gamma))
            reps_pr = point_map.get(key, [])
            if not reps_pr:
                continue

            labels = [p.ring_label for p in reps_pr if not p.invalid]
            # If all invalid, treat as non-ringing but mark invalid_rate via reason
            if len(labels) == 0:
                ring = False
                invalid_rate = 1.0
            else:
                ring = majority_vote(labels)
                invalid_rate = float(np.mean([p.invalid for p in reps_pr]))

            # Aggregate metrics as means over reps
            r_mean = float(np.mean([p.r_mean for p in reps_pr]))
            d_db = float(np.mean([p.delta_psd_db for p in reps_pr]))
            n_over = float(np.mean([p.n_over for p in reps_pr]))

            grid_mask[gi, ki] = bool(ring)

            grid_rows.append({
                "K": float(K),
                "gamma": float(gamma),
                "ring_label": int(ring),
                "r_mean": r_mean,
                "Delta_PSD_dB": d_db,
                "N_over": n_over,
                "replicates": int(len(reps_pr)),
                "invalid_rate": float(invalid_rate),
            })

    # Write grid.csv
    grid_path = outdir / "grid.csv"
    with grid_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()) if grid_rows else ["K", "gamma"])
        w.writeheader()
        for row in grid_rows:
            w.writerow(row)

    # Null 1: "ringing anywhere" — check if any point satisfies the triple threshold
    # Use majority-voted grid rows (not individual reps) to match S definition.
    any_ringing = any(
        (row["Delta_PSD_dB"] >= thr_psd_db) and (row["N_over"] >= thr_n_over) and (row["r_mean"] >= thr_r_mean)
        for row in grid_rows
    )
    null1_fail = not any_ringing
    null1 = {
        "name": "null1_no_ringing_anywhere",
        "fail": bool(null1_fail),
        "details": {
            "thresholds": {"Delta_PSD_dB": thr_psd_db, "N_over": thr_n_over, "r_mean": thr_r_mean},
            "any_point_passed": bool(any_ringing),
        },
    }

    # Negative control (plasticity off)
    negative_control_mask = None
    if (not no_negative_control) and (not quick):
        # Run a *cheap* negative control pass by reusing the same grid but 1 replicate.
        # This is still expensive for full grid; you can cap points during development with --max-points.
        nc_point_map: Dict[Tuple[float, float], List[PointResult]] = {}
        for gi, gamma in enumerate(g_vals):
            for ki, K in enumerate(K_vals):
                if cap is not None and (gi * W + ki + 1) > cap:
                    break
                seed = stable_seed(base_seed, float(K), float(gamma), 0)
                pr, _ = simulate_point(
                    N=N, K=float(K), gamma=float(gamma), rep=0,
                    dt=dt, steps_total=steps_total, steps_burnin=steps_burnin, steps_measure=steps_measure,
                    omega_mean=omega_mean, omega_std=omega_std,
                    D=D, Omega=Omega,
                    plasticity_enabled=False, alpha=0.0, beta=beta,
                    W_init_value=W_init_value, W_max=W_max,
                    seed=seed,
                    thr_psd_db=thr_psd_db, thr_n_over=thr_n_over, thr_r_mean=thr_r_mean,
                )
                nc_point_map.setdefault((float(K), float(gamma)), []).append(pr)

        negative_control_mask = np.zeros_like(grid_mask, dtype=bool)
        for gi, gamma in enumerate(g_vals):
            for ki, K in enumerate(K_vals):
                reps_pr = nc_point_map.get((float(K), float(gamma)), [])
                if not reps_pr:
                    continue
                ring = majority_vote([p.ring_label for p in reps_pr if not p.invalid])
                negative_control_mask[gi, ki] = bool(ring)

    nulls = eval_nulls(
        grid_mask=grid_mask,
        K_values=K_vals,
        gamma_values=g_vals,
        negative_control_mask=negative_control_mask,
        null2_area_frac_min=0.02,
        null2_cc_min=20,
        null3_span_frac_max=0.60,
        null4_area_ratio_min=0.80,
    )
    nulls["null1"] = null1

    # Overall rejection if ANY applicable null fails
    null_fail_flags = []
    for k, v in nulls.items():
        if v.get("skip", False):
            continue
        null_fail_flags.append(bool(v.get("fail", False)))
    rejected = any(null_fail_flags)

    # Write null_evaluation.json
    null_eval = {
        "bundle_id": cfg.get("bundle_id", "0001_rfo_ringing_wedge"),
        "mode": "quick" if quick else "full",
        "rejected": bool(rejected),
        "nulls": nulls,
        "grid_shape": {"gamma": int(H), "K": int(W)},
        "summary": {
            "S": int(np.sum(grid_mask)),
            "grid_points": int(H * W),
            "area_frac": float(np.sum(grid_mask) / max(1, H * W)),
            "largest_cc": int(largest_connected_component_size(grid_mask)),
        },
    }
    write_text(outdir / "null_evaluation.json", json.dumps(null_eval, indent=2))

    # Write parameters_used.json
    params_used = {
        "bundle_id": cfg.get("bundle_id"),
        "version": cfg.get("version"),
        "mode": "quick" if quick else "full",
        "effective": {
            "dt": dt,
            "steps_total": steps_total,
            "steps_burnin": steps_burnin,
            "steps_measure": steps_measure,
            "N": N,
            "K_num": int(K_vals.size),
            "gamma_num": int(g_vals.size),
            "replicates_per_point": int(reps),
        },
        "deviations": deviations,
        "notes": "All files written as UTF-8. Seeds use stable sha256-based hash.",
    }
    write_text(outdir / "parameters_used.json", json.dumps(params_used, indent=2))

    # Write seed_manifest.json
    write_text(outdir / "seed_manifest.json", json.dumps(seed_manifest, indent=2))

    # Write wedge_report.md (text-only report)
    report_lines = []
    report_lines.append(f"# Wedge Report — {cfg.get('bundle_id','0001_rfo_ringing_wedge')}")
    report_lines.append("")
    report_lines.append(f"- Mode: {'quick' if quick else 'full'}")
    report_lines.append(f"- Grid: gamma={H}, K={W}")
    report_lines.append(f"- Replicates per point: {reps}")
    report_lines.append("")
    report_lines.append("## Ringing thresholds (point-level)")
    report_lines.append(f"- Δ_PSD_dB ≥ {thr_psd_db}")
    report_lines.append(f"- N_over ≥ {thr_n_over}")
    report_lines.append(f"- r_mean ≥ {thr_r_mean}")
    report_lines.append("")
    report_lines.append("## Sweep summary")
    report_lines.append(f"- Ringing points |S|: {int(np.sum(grid_mask))} / {H*W} ({(np.sum(grid_mask)/max(1,H*W)):.4f})")
    report_lines.append(f"- Largest connected component size (4-neighbor): {largest_connected_component_size(grid_mask)}")
    report_lines.append("")
    report_lines.append("## Null evaluation")
    report_lines.append(f"- Rejected: **{rejected}**")
    report_lines.append("")
    for key in ["null1", "null2", "null3", "null4"]:
        v = nulls.get(key, {})
        if v.get("skip", False):
            report_lines.append(f"- {v.get('name', key)}: SKIP — {v.get('reason','')}")
        else:
            report_lines.append(f"- {v.get('name', key)}: {'FAIL' if v.get('fail', False) else 'PASS'}")
            details = v.get("details", {})
            if details:
                report_lines.append(f"  - details: `{json.dumps(details)}`")
    report_lines.append("")
    report_lines.append("## Files written")
    report_lines.append(f"- {grid_path.name}")
    report_lines.append("- null_evaluation.json")
    report_lines.append("- parameters_used.json")
    report_lines.append("- seed_manifest.json")
    report_lines.append("- wedge_report.md")
    report_lines.append("")
    if deviations:
        report_lines.append("## Deviations (recorded)")
        for k, v in deviations.items():
            report_lines.append(f"- {k}: {v}")
        report_lines.append("")

    write_text(outdir / "wedge_report.md", "\n".join(report_lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="Bundle 0001 — RFO Ringing Wedge experiment runner")
    ap.add_argument("--config", type=str, default=str(Path(__file__).resolve().parents[1] / "PREREG.yaml"),
                    help="Path to PREREG.yaml (default: bundle PREREG.yaml)")
    ap.add_argument("--out", type=str, default=str(Path.cwd() / "outputs_0001"),
                    help="Output directory")
    ap.add_argument("--quick", action="store_true", help="Quick mode (tiny grid + short run; for CI/smoke)")
    ap.add_argument("--no-negative-control", action="store_true", help="Skip negative control run")
    ap.add_argument("--max-points", type=int, default=0, help="Cap number of grid points (dev sanity). 0=none.")
    args = ap.parse_args()

    config_path = Path(args.config).resolve()
    outdir = Path(args.out).resolve()
    max_points = args.max_points if args.max_points and args.max_points > 0 else None

    run_bundle(
        config_path=config_path,
        outdir=outdir,
        quick=bool(args.quick),
        no_negative_control=bool(args.no_negative_control),
        max_points=max_points,
    )
    print(f"Done. Outputs written to: {outdir}")


if __name__ == "__main__":
    main()
