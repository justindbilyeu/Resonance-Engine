# Architecture

**Status:** Living document (v0 scaffold)

## Overview

Resonance Engine transforms research questions into falsifiable experiments through constrained multi-role orchestration. The architecture treats discovery as a dynamical system where constraints enable productive oscillation between hypothesis generation and adversarial critique.

## Core Components

### Discovery Compiler

Orchestrates the multi-role compilation process from seed idea to preregistered experiment bundle.

**Responsibilities:**
- Role coordination (Builder → Skeptic → Auditor → Operator)
- Stage progression management
- Bundle artifact generation

**Key interfaces:** `core/discovery_compiler.py`

### Coherence Controller

Tracks constraint health metrics and decides when to diversify perspectives vs converge on protocol.

**Responsibilities:**
- Constraint health measurement across stages
- Premature convergence detection
- Diversify/converge/restart decisions

**Key interfaces:** `core/coherence_controller.py`

### Roles (Multi-Oscillator System)

#### Builder
- **Phase:** Synchronizing tendency
- **Function:** Hypothesis generation, pattern identification
- **Output:** Candidate claims and protocols

#### Skeptic
- **Phase:** Counter-phase
- **Function:** Adversarial probing, null generation
- **Output:** Failure modes and numeric rejection thresholds

#### Auditor
- **Phase:** Boundary conditions
- **Function:** Falsifiability validation, prereg integrity checks
- **Output:** Validation reports and integrity issues

#### Operator
- **Phase:** Crystallization
- **Function:** Code and test generation
- **Output:** Runnable experiment artifacts

**Key interfaces:** `core/roles/`

### Metrics System

Measures constraint health, convergence, and dissent throughout the discovery process.

**Key metrics:**
- Falsifiability (can this claim actually fail?)
- Null completeness (≥2 numeric thresholds?)
- Operational clarity (can third parties reproduce this?)
- Dissent level (Builder/Skeptic disagreement)
- Stage-to-stage improvement

**Key interfaces:** `core/metrics/`

## Data Flow

```
Seed Idea
    ↓
Discovery Compiler (orchestration)
    ↓
[Builder → Skeptic → Auditor] (iterative oscillation)
    ↓
Coherence Controller (health check + decision)
    ├─ diversify → inject architectural diversity
    ├─ converge → Operator generates bundle
    └─ restart → tighten seed and retry
    ↓
Experiment Bundle (artifacts)
```

## Bundle Outputs

Each successful compilation produces:
- `CLAIM.md` - Falsifiable claim (≤3 sentences)
- `OPERATIONALIZE.md` - Observable quantities + measurement protocol
- `PREREG.yaml` - Locked parameters, stopping rules, acceptance/failure criteria
- `NULLS.md` - Numeric rejection thresholds (≥2 required by gate)
- `COHERENCE_METRICS.yaml` - Constraint health progression
- `src/experiment.py` - Runnable implementation
- `tests/test_experiment.py` - Validation suite

## Hard Gates

**Null Completeness Gate** (PR-1): Rejects any bundle with <2 specific numeric thresholds in `NULLS.md`.

Future gates (post-v0):
- Falsifiability gate (Auditor validation)
- Dissent baseline (minimum Builder/Skeptic disagreement)
- Reproducibility check (third-party replication test)

## Design Principles

1. **Constraints enable reach:** Rigor is not a tax—it's the structure that makes discovery possible
2. **Dissent over agreement:** Premature consensus signals narrative drift
3. **Oscillation over pipeline:** Multi-role interaction is dynamical, not sequential
4. **Artifacts over conversations:** Bundle outputs must be reproducible independently
5. **Failure is success:** Experiments succeed when they can fail in preregistered ways

## Future Extensions

- **Integration adapters** (PR-3): Clean interfaces to justasking, ITPU, Geometric-Plasticity
- **Plugin architecture:** Theory-specific validators and metrics
- **Real-time constraint visualization:** Dashboard for health metrics during compilation
- **Automated replication testing:** Third-party bundle execution validation

---

**See also:**
- [PHILOSOPHY.md](PHILOSOPHY.md) - Why constraints are the medium
- [Repository README](../README.md) - Usage and quickstart
