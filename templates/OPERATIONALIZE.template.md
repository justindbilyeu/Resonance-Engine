# Operationalization

<!-- Replace this template with concrete measurement protocols for your claim -->

**Seed idea:** {seed}

## Observable Quantities

[Define exactly what you will measure. Each observable should have:
- Clear measurement protocol
- Units and precision
- Expected range of values]

### Primary Observables

1. **[Observable name]**
   - **What it measures:** [Description]
   - **How to measure:** [Exact protocol]
   - **Units:** [e.g., accuracy (0-1), seconds, dimensionless ratio]
   - **Expected range:** [e.g., 0.5-0.95]

2. **[Observable name]**
   - **What it measures:** [Description]
   - **How to measure:** [Exact protocol]
   - **Units:** [...]
   - **Expected range:** [...]

### Secondary Observables (optional)

[Additional measurements for diagnostics or post-hoc analysis]

## Measurement Protocol

### Data

[Describe the dataset, sample size, train/test splits, random seeds]

- **Dataset:** [Name and version]
- **Sample size:** [N samples]
- **Splits:** [e.g., 80/20 train/test, seed=42]
- **Preprocessing:** [Normalization, tokenization, etc.]

### Procedure

[Step-by-step instructions that a third party could follow]

1. [Step 1]
2. [Step 2]
3. [...]

### Compute Requirements

[Specify hardware, runtime estimates, reproducibility requirements]

- **Hardware:** [e.g., 1x NVIDIA A100, 32GB RAM]
- **Estimated runtime:** [e.g., ~2 hours]
- **Random seeds:** [All seeds specified in PREREG.yaml]

## Reproducibility

[What must be locked to ensure third-party replication?]

- [ ] Random seeds specified
- [ ] Dataset version pinned
- [ ] Model architecture specified
- [ ] Hyperparameters locked (see PREREG.yaml)
- [ ] Dependencies pinned (requirements.txt)

---

**Constraint checklist:**
- [ ] Every observable has a clear measurement protocol
- [ ] Units and precision specified
- [ ] Third party could reproduce from these instructions alone
- [ ] No ambiguous terms (e.g., "good performance" → specific threshold)
