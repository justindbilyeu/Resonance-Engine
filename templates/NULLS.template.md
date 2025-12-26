# Null Hypotheses and Rejection Criteria

<!-- Replace this template with your specific numeric falsification thresholds -->
<!-- REQUIRED: Must contain ≥2 explicit numeric thresholds (enforced by null_gate) -->

**Seed idea:** {seed}

## Rejection Criteria

We will **reject the hypothesis** if **ANY** of the following conditions are met:

### Primary Null Hypotheses

1. **Threshold 1: [Metric name]**
   - **Reject if:** [Metric] < 0.55
   - **Rationale:** [Why this threshold? e.g., "Barely above random chance for binary classification"]
   - **Measurement:** [How is this measured? Reference OPERATIONALIZE.md]

2. **Threshold 2: [Metric name]**
   - **Reject if:** [Improvement metric] <= 5%
   - **Rationale:** [Why this threshold? e.g., "Below practical significance threshold"]
   - **Measurement:** [How is this measured? Reference OPERATIONALIZE.md]

### Secondary Null Hypotheses (optional but recommended)

3. **Threshold 3: [Metric name]**
   - **Reject if:** [Variance metric] > 2x [mean performance]
   - **Rationale:** [e.g., "Results are not stable across runs"]
   - **Measurement:** [Standard deviation across N runs]

4. **Threshold 4: [Metric name]**
   - **Reject if:** [Performance metric] >= 10% [worse than baseline]
   - **Rationale:** [e.g., "Method harms performance"]
   - **Measurement:** [Comparison to baseline in PREREG.yaml]

## Interpretation

- **Any single failure criterion triggers rejection** (conservative interpretation)
- Thresholds are intentionally conservative to avoid p-hacking
- These criteria are **locked before seeing results** (see PREREG.yaml)

## Examples of Good Numeric Thresholds

✓ **Explicit comparators:**
  - "accuracy < 0.55"
  - "speedup <= 1.5x baseline"
  - "error rate > 10%"
  - "p-value >= 0.05"

✗ **Vague criteria (will fail null_gate):**
  - "results are inconsistent"
  - "performance does not improve significantly"
  - "model appears to overfit"

---

**Null Completeness Gate:**
This file will be validated by `assert_numeric_nulls()` which requires ≥2 explicit numeric thresholds. See [docs/METRICS.md](../docs/METRICS.md) for details.

**Constraint checklist:**
- [ ] At least 2 numeric thresholds specified
- [ ] Each threshold has explicit comparator (>=, <=, <, >, ==, !=) or multiplier/percentage
- [ ] Thresholds are justified (why these values?)
- [ ] Thresholds match failure criteria in PREREG.yaml
- [ ] No ambiguous language ("significant", "good", "bad")
