# Results: Coin Flip Fairness Test

**Experiment:** Golden Path Toy Example (Public Demo - Locked)
**Date:** 2025-12-26
**Engine Version:** v0

## Running the Experiment

```bash
cd examples/golden_path_toy
python src/experiment.py
```

## Experimental Output

```
Running coin flip fairness experiment...
  Random seed: 42
  Trials: 1000
  Coin probability: 0.5

============================================================
COIN FLIP FAIRNESS TEST - RESULTS
============================================================

Total flips:       1000
Heads:             497
Tails:             503
Proportion heads:  0.4970
Standard error:    0.0158

Preregistered Criteria:
  Primary null bounds:  [0.45, 0.55]
  Passes primary null:  True
  Passes extreme null:  True

VERDICT: PASS

✓ Coin appears fair (within 95% confidence interval)
============================================================
```

## Null Hypothesis Evaluation

From NULLS.md, we preregistered 4 numeric thresholds:

1. **Threshold 1:** Reject if proportion < 0.45
   - **Result:** PASS
   - **Observed proportion:** 0.4970

2. **Threshold 2:** Reject if proportion > 0.55
   - **Result:** PASS
   - **Observed proportion:** 0.4970

3. **Threshold 3:** Reject if proportion < 0.40
   - **Result:** PASS
   - **Observed proportion:** 0.4970

4. **Threshold 4:** Reject if proportion > 0.60
   - **Result:** PASS
   - **Observed proportion:** 0.4970

## Final Verdict

**Outcome:** PASS

**Interpretation:**
With seed=42, the simulated fair coin (p=0.5) produced 497 heads out of 1000
flips (proportion=0.497). This falls comfortably within all preregistered
rejection thresholds:
- Primary bounds [0.45, 0.55]: ✓ PASS
- Extreme bounds [0.40, 0.60]: ✓ PASS

The experiment demonstrates that the null hypothesis ("coin is fair") cannot
be rejected. The observed proportion is within 2 standard errors of the
expected value (0.5), consistent with normal sampling variation.

## Constraint Health Retrospective

Looking back at the experiment design:

**What worked well:**
- Numeric thresholds were explicit, evaluable, and unambiguous (4 thresholds passed gate)
- Deterministic execution with fixed seed=42 made reproduction perfect
- Simple experiment structure makes bundle template transparent for new users
- Falsifiability was clear: any proportion outside [0.45, 0.55] would fail
- Third-party reproduction possible from bundle alone (no external dependencies beyond numpy)

**What could be improved:**
- Could add confidence interval overlap check as additional threshold
- Could test robustness across multiple seeds (10+ trials)
- Statistical power analysis could strengthen preregistration

**Lessons for future experiments:**
- Toy examples are valuable for demonstrating methodology without obscuring structure
- Four thresholds (primary + extreme bounds) provides good coverage
- Deterministic seeds enable perfect reproducibility for demos

## Reproducibility Verification

**Can a third party reproduce this experiment from the bundle alone?**
- [x] Yes
- [ ] No

**If no, what additional information is needed?**
- N/A - All parameters locked in PREREG.yaml, dependencies minimal (numpy), seed fixed

**Reproduction steps from clone:**
```bash
git clone https://github.com/justindbilyeu/Resonance-Engine.git
cd Resonance-Engine
pip install -e .
cd examples/golden_path_toy
python src/experiment.py
```

Expected output: Identical to "Experimental Output" section above (497 heads, PASS verdict).

## Notes

This is the **locked public demo** for Resonance Engine v0. The results are
deterministic and serve as a reference implementation of the full workflow:

1. Seed idea → Bundle generation
2. Preregistered parameters (PREREG.yaml)
3. Explicit numeric thresholds (NULLS.md passes gate)
4. Runnable experiment (src/experiment.py)
5. Results documentation (this file)

The coin flip example is intentionally trivial to make the structure transparent.
Real experiments would involve more complex hypotheses but follow the same pattern.

**Status:** Locked as of v1 (2025-12-26). This example demonstrates perfect
clone → results reproducibility with zero configuration.
