# Results: Coin Flip Fairness Test

**Experiment:** Golden Path Toy Example
**Date:** [Fill in when experiment is run]
**Engine Version:** v0

## Running the Experiment

```bash
cd examples/golden_path_toy
python src/experiment.py
```

## Experimental Output

```
[Paste output from src/experiment.py here]
```

## Null Hypothesis Evaluation

From NULLS.md, we preregistered 4 numeric thresholds:

1. **Threshold 1:** Reject if proportion < 0.45
   - **Result:** [PASS/FAIL]
   - **Observed proportion:** [value]

2. **Threshold 2:** Reject if proportion > 0.55
   - **Result:** [PASS/FAIL]
   - **Observed proportion:** [value]

3. **Threshold 3:** Reject if proportion < 0.40
   - **Result:** [PASS/FAIL]
   - **Observed proportion:** [value]

4. **Threshold 4:** Reject if proportion > 0.60
   - **Result:** [PASS/FAIL]
   - **Observed proportion:** [value]

## Final Verdict

**Outcome:** [PASS/FAIL]

**Interpretation:**
[Explain what the result means. For a fair coin with seed=42, we expect the
hypothesis to PASS since the proportion should be within [0.45, 0.55].]

## Constraint Health Retrospective

Looking back at the experiment design:

**What worked well:**
- [e.g., "Numeric thresholds were clear and evaluable"]
- [e.g., "Deterministic execution with fixed seed made reproduction perfect"]
- [e.g., "Simple experiment made the bundle structure transparent"]

**What could be improved:**
- [e.g., "Could add more sophisticated statistical tests"]
- [e.g., "Could test robustness across multiple seeds"]

**Lessons for future experiments:**
- [Document insights that would help design better experiments]

## Reproducibility Verification

**Can a third party reproduce this experiment from the bundle alone?**
- [ ] Yes
- [ ] No

**If no, what additional information is needed?**
- [List any missing information or ambiguities]

## Notes

[Any additional observations, unexpected results, or commentary]

---

**Template Instructions:**
1. Run the experiment: `python src/experiment.py`
2. Copy output to "Experimental Output" section
3. Fill in observed values in "Null Hypothesis Evaluation"
4. Determine final verdict
5. Complete retrospective sections
6. Commit this file with results documented
