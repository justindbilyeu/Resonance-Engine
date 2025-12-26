# Operationalization

**Seed idea:** Does a simulated coin flip produce heads and tails with approximately equal probability over many trials?

## Observable Quantities

### Primary Observables

1. **Proportion of Heads**
   - **What it measures:** Fraction of coin flips that result in "heads"
   - **How to measure:** Count heads, divide by total flips
   - **Units:** Proportion (0.0 to 1.0, dimensionless)
   - **Expected range:** 0.45 to 0.55 for fair coin (95% CI)

2. **Total Trials**
   - **What it measures:** Number of coin flips performed
   - **How to measure:** Length of results array
   - **Units:** Count (integer)
   - **Expected range:** Exactly 1000 (locked in PREREG.yaml)

### Secondary Observables

3. **Standard Error**
   - **What it measures:** Uncertainty in proportion estimate
   - **How to measure:** sqrt(p * (1-p) / n) where p = proportion, n = trials
   - **Units:** Dimensionless
   - **Expected range:** ~0.016 for p=0.5, n=1000

## Measurement Protocol

### Data

- **Dataset:** Simulated coin flips (no external data)
- **Sample size:** 1000 flips
- **Random seed:** 42 (locked in PREREG.yaml for reproducibility)
- **Coin bias:** p=0.5 (fair coin)

### Procedure

1. Initialize random number generator with seed=42
2. Generate 1000 random samples from Bernoulli(p=0.5)
3. Count number of heads (value=1)
4. Compute proportion: heads / total_flips
5. Compare proportion to acceptance/rejection criteria

### Compute Requirements

- **Hardware:** Any machine (minimal computation)
- **Estimated runtime:** <1 second
- **Random seed:** 42 (specified in PREREG.yaml)
- **Dependencies:** Python 3.10+, numpy

## Reproducibility

- [x] Random seed specified (42)
- [x] Number of trials specified (1000)
- [x] Coin probability specified (p=0.5)
- [x] Measurement procedure specified
- [x] Dependencies minimal and standard (numpy)

---

**Constraint checklist:**
- [x] Every observable has a clear measurement protocol
- [x] Units and precision specified
- [x] Third party could reproduce from these instructions alone
- [x] No ambiguous terms
