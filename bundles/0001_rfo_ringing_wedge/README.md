# Bundle 0001: RFO Ringing Wedge

**Status:** Complete ✅
**Created:** December 2025
**Type:** Proof-of-Concept

## Overview

This bundle represents the **first complete experiment** compiled by Resonance Engine, proving that the entire cognitive infrastructure stack works end-to-end.

## Research Question (Seed)

> "Can we detect when Builder/Skeptic oscillation becomes productive (converging on testable hypotheses) vs degenerate (stuck in narrative coherence)?"

## Hypothesis

See [CLAIM.md](./CLAIM.md) for the full falsifiable claim.

**Short version:** Productive oscillation exhibits specific spectral signatures (ringing patterns) that can be measured and used to gate experiment quality.

## Bundle Contents

### Core Artifacts
- **[CLAIM.md](./CLAIM.md)** — Falsifiable hypothesis (≤3 sentences)
- **[OPERATIONALIZE.md](./OPERATIONALIZE.md)** — Measurement protocol
- **[PREREG.yaml](./PREREG.yaml)** — Locked parameters before execution
- **[NULLS.md](./NULLS.md)** — Numeric rejection thresholds (passes gate: ≥2)
- **[COHERENCE_METRICS.yaml](./COHERENCE_METRICS.yaml)** — Constraint health tracking

### Execution Traces
- **[decision_trace.md](./decision_trace.md)** — Full compilation decision log
- **[DEVELOPER_NOTES.md](./DEVELOPER_NOTES.md)** — Implementation notes

### Results Data
- **[constraint_health_history.csv](./constraint_health_history.csv)** — Health metrics over time
- **[dissent_history.csv](./dissent_history.csv)** — Builder/Skeptic disagreement tracking
- **[hard_gate_results.json](./hard_gate_results.json)** — Gate enforcement results
- **[parameters_used.json](./parameters_used.json)** — Actual parameter values
- **[seed_manifest.json](./seed_manifest.json)** — Random seeds for reproducibility

### Metadata
- **[MANIFEST.json](./MANIFEST.json)** — Bundle metadata and provenance

## Key Results

🚧 **Status:** Experiment design complete, awaiting execution

### Null Hypothesis Evaluation

From NULLS.md, we preregistered numeric thresholds:

1. **Threshold 1:** [Details TBD after execution]
2. **Threshold 2:** [Details TBD after execution]

**Verdict:** [PASS/FAIL] — To be determined after running experiment

## Constraint Health Retrospective

**What worked well:**
- Bundle generation successfully enforced ≥2 numeric thresholds
- Decision trace captures full compilation process
- Preregistration locked before execution

**What could improve:**
- [To be filled after execution]

## Reproducibility

**Can third parties reproduce this experiment?**
- [x] All parameters locked in PREREG.yaml
- [x] Random seeds documented
- [x] Measurement protocol explicit
- [ ] Results verified independently (pending)

## Integration with Theory

This bundle tests predictions from:
- **Resonance Geometry** — Spectral signatures of coherence
- **Geometric Plasticity** — Ringing detection in oscillating systems
- **ITPU** — Information-theoretic constraint health metrics

## Lessons Learned

1. **Bundle structure works** — The template-based approach produces complete artifacts
2. **Gates are enforceable** — Null completeness gate successfully blocks insufficient thresholds
3. **Provenance tracking is feasible** — Decision traces capture compilation reasoning

## Next Steps

1. Execute the experiment
2. Fill in RESULTS.md with actual outcomes
3. Retrospective: Did constraint health improve stage-to-stage?
4. Document what worked and what failed

---

**Note:** This bundle exists primarily to validate the Resonance Engine infrastructure. The research question is real, but the primary success criterion is "does the compilation process work?" rather than "is the hypothesis confirmed?"

The fact that this README exists means the infrastructure is functional enough to produce structured outputs. 🎉
