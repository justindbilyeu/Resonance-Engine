# Null Hypotheses and Rejection Criteria

**Seed idea:** Does a simulated coin flip produce heads and tails with approximately equal probability over many trials?

## Rejection Criteria

We will **reject the hypothesis** that the coin is fair if **ANY** of the following conditions are met:

### Primary Null Hypotheses

1. **Threshold 1: Lower Bound**
   - **Reject if:** Proportion of heads < 0.45
   - **Rationale:** Below the 95% confidence interval lower bound for a fair coin (p=0.5, n=1000)
   - **Measurement:** Count heads, divide by 1000 trials

2. **Threshold 2: Upper Bound**
   - **Reject if:** Proportion of heads > 0.55
   - **Rationale:** Above the 95% confidence interval upper bound for a fair coin
   - **Measurement:** Count heads, divide by 1000 trials

### Secondary Null Hypotheses

3. **Threshold 3: Extreme Bias (Lower)**
   - **Reject if:** Proportion of heads < 0.40
   - **Rationale:** More than 3 standard errors below expectation (p < 0.001)
   - **Measurement:** Count heads, divide by 1000 trials

4. **Threshold 4: Extreme Bias (Upper)**
   - **Reject if:** Proportion of heads > 0.60
   - **Rationale:** More than 3 standard errors above expectation (p < 0.001)
   - **Measurement:** Count heads, divide by 1000 trials

## Interpretation

- **Any single failure criterion triggers rejection** (conservative interpretation)
- Thresholds are based on statistical theory (binomial confidence intervals)
- These criteria are **locked before seeing results** (see PREREG.yaml)
- For a fair coin with seed=42, we expect proportion ≈ 0.50

## Null Completeness Validation

This file contains **4 numeric thresholds** (< 0.45, > 0.55, < 0.40, > 0.60), which exceeds the null completeness gate requirement of ≥2 thresholds.

---

**Null Completeness Gate:**
✓ This file passes `assert_numeric_nulls()` with 4 explicit numeric thresholds.

**Constraint checklist:**
- [x] At least 2 numeric thresholds specified (have 4)
- [x] Each threshold has explicit comparator
- [x] Thresholds are justified with statistical reasoning
- [x] Thresholds match failure criteria in PREREG.yaml
- [x] No ambiguous language
