# OPERATIONALIZE.md
**Bundle:** 0001_rfo_ringing_wedge  
**Goal:** Convert “ringing wedge” into measurable, automatable diagnostics with explicit null rejection thresholds.

## 1) Model definition (RFO network)
We simulate an N-node RFO network with phases θ_i(t) and a plastic coupling matrix W_ij(t).

### State variables
- θ_i(t): oscillator phase for node i
- ω_i: natural frequency (fixed per run)
- W_ij(t): directed coupling weight (plastic)
- Optional: A_i(t) amplitude (if using amplitude-extended RFO); otherwise use phase-only.

### Dynamics (reference form; fixed for this bundle)
Discrete-time Euler update with step Δt:

1) Phase update:
θ_i(t+Δt) = θ_i(t) + Δt * [ ω_i
                           + (K/N) * Σ_j W_ij(t) * sin(θ_j(t) - θ_i(t))
                           + D * sin(Ω t - θ_i(t)) ] + ξ_i(t)

2) Plasticity update (Hebbian-style phase alignment with decay):
W_ij(t+Δt) = clip( W_ij(t) + Δt * [ α * cos(θ_j(t) - θ_i(t)) - β * W_ij(t) ], 0, W_max )

Where:
- N = 128 oscillators
- K = global coupling strength (swept)
- γ = effective damping/noise strength (swept via ξ amplitude; see below)
- D = drive amplitude (fixed)
- Ω = drive frequency (fixed)
- ξ_i(t): zero-mean Gaussian noise with std σ = γ * sqrt(Δt)
- clip enforces bounded weights, preventing divergence

## 2) Observables
We compute time series over a measurement window after burn-in.

### (A) Kuramoto order parameter (macroscopic coherence)
r(t) = | (1/N) Σ_i exp(i θ_i(t)) |
ψ(t) = arg( (1/N) Σ_i exp(i θ_i(t)) )  # not required but logged

We use r(t) as the primary “ringing carrier” time series.

### (B) Plasticity / redundancy proxy (network “memory surface”)
Let W(t) be the coupling matrix. Define:
m(t) = mean(W(t))  # mean coupling mass
s(t) = std(W(t))   # coupling heterogeneity
R(t) = s(t) / (m(t) + ε)  # normalized redundancy/heterogeneity proxy

R(t) is used for overshoot/hysteresis diagnostics.

## 3) Ringing diagnostics (binary decision per (K,γ) point)
We label a parameter point as RINGING iff all conditions hold on the measurement window:

### Condition 1 — PSD peak prominence (numeric)
Compute PSD of r(t) over measurement window (Welch method).
Let P_peak = maximum PSD excluding DC bin.
Let P_base = median PSD excluding DC bin.
Define peak prominence in dB:
Δ_PSD_dB = 10 * log10(P_peak / P_base)

### Condition 2 — Overshoot count (numeric)
Define normalized redundancy z-score over the measurement window:
Z_R(t) = (R(t) - median(R))/MAD(R)
Count overshoots:
N_over = number of upward crossings of Z_R(t) above +1.0

### Condition 3 — Persistence (numeric)
Let r̄ be mean(r(t)) over measurement window.
Require r̄ ≥ r_min to avoid “false PSD” from tiny amplitude.

## 4) “Wedge” structure test (region-level)
After labeling each grid point as RINGING / NONRINGING, define the ringing set S.
We evaluate whether S forms a “wedge-like” connected region in (K,γ) space:
- Connectivity: 4-neighbor connectivity on the grid.
- Wedge criterion: for at least one γ-band, there exists a contiguous interval in K with ≥M consecutive RINGING points, and the upper boundary K_high(γ) increases with γ over a measurable span (monotone trend test).

(Region-level criteria are used as a secondary confirmation; rejection is driven by NULLS.md.)

## 5) Data products (what is saved)
For each (K,γ):
- summary.json: r_mean, Δ_PSD_dB, N_over, ring_label, seed, runtime
- timeseries.npz: r(t), R(t) (optional; save only for boundary points to limit storage)
- psd.npz: frequencies, psd_r

For the whole sweep:
- grid.csv with all summary metrics
- wedge_report.md with plots + connectivity + boundary extraction

## 6) Notes on interpretability
- “Ringing” here is a measurable resonance signature, not metaphor.
- The claim is rejected if the preregistered null thresholds are not met.
