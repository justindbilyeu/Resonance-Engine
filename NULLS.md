# NULLS.md
**Bundle:** 0001_rfo_ringing_wedge  
**Hard-gate:** ≥2 numeric rejection thresholds present (this file contains 4).

## Purpose
Define explicit numeric conditions under which the ringing-wedge claim is rejected.

## Definitions (from OPERATIONALIZE.md)
- A grid point (K,γ) is labeled **RINGING** iff all preregistered conditions pass.
- S = set of grid points labeled RINGING after majority vote over replicates.

---

## Null 1 — No ringing anywhere (pointwise failure)
**Reject the claim if:**
- There exists **no** grid point with:
  - Δ_PSD_dB ≥ **6.0 dB** AND
  - N_over ≥ **2** AND
  - r_mean ≥ **0.35**

If no point satisfies all three, “ringing” is not detected and the wedge cannot exist.

---

## Null 2 — Ringing exists but no wedge-like region (region failure)
**Reject the claim if:**
- |S| / |Grid| < **0.02** (less than 2% of points labeled RINGING), OR
- The largest connected component of S (4-neighbor connectivity) has size < **20** points.

This prevents declaring victory from isolated “spark points” or noise-driven detections.

---

## Null 3 — No bounded wedge (no meaningful boundaries)
**Reject the claim if:**
- For every γ row, the set of RINGING K-values is either empty or spans > **60%** of the K-range.

Interpretation: A wedge is bounded; if ringing covers almost all K (or none), the “wedge” structure is not supported.

---

## Null 4 — Negative control contradiction
Run the negative control sweep (plasticity_off: α=0.0, W fixed) on the same grid.

**Reject the claim if:**
- The negative control produces a ringing region S_nc with:
  - |S_nc| ≥ **0.8 * |S|**  (i.e., ≥80% of the ringing area persists without plasticity)

Interpretation: If plasticity is not necessary for the observed structure under this model specification,
then the “plastic-RFO ringing wedge” claim (as stated) fails.

---

## Notes
- These thresholds are locked. No post-hoc adjustment is permitted.
- Passing these nulls does not prove the most general theory; it supports this RFO specification.
- All failures must be reported with the same prominence as successes.
