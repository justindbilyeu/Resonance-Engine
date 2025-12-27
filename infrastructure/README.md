# Infrastructure Components

**Status:** Directory structure created, integration pending

This directory will contain the supporting infrastructure that enables Resonance Engine to maintain constraint health and produce rigorous experiments.

## Overview

Infrastructure components provide the computational substrate for:
- **Real-time constraint health monitoring** (ITPU)
- **Ringing diagnostics and quality gates** (Geometric-Plasticity)
- **Multi-AI coordination and diversity** (Orchestration)

## Planned Components

### 1. ITPU — Information-Theoretic Processing Unit

**Location:** `infrastructure/itpu/`
**Status:** 🚧 Not yet integrated

**Purpose:** Real-time constraint health metrics and coherence measurement

**Capabilities:**
- Compute mutual information between claim and null hypotheses
- Windowed MI across compilation stages (convergence detection)
- Quantify dissent between Builder and Skeptic outputs
- Provide computational substrate for quality monitoring

**Integration Point:**
```python
from infrastructure.itpu import compute_mutual_info, windowed_mutual_info

# Measure dissent between Builder/Skeptic
dissent_score = compute_mutual_info(builder_output, skeptic_output)

# Track constraint health over compilation stages
health_trajectory = windowed_mutual_info(stage_outputs)
```

**Repository:** [github.com/justindbilyeu/ITPU](https://github.com/justindbilyeu/ITPU)

---

### 2. Geometric-Plasticity

**Location:** `infrastructure/geometric_plasticity/`
**Status:** 🚧 Not yet integrated

**Purpose:** Ringing diagnostics and spectral stability analysis

**Capabilities:**
- Detect productive vs degenerate Builder/Skeptic oscillation
- Spectral stability analysis (ringing detection)
- Quality gates for compilation process
- Answer: "Is this oscillation converging on testable truth?"

**Integration Point:**
```python
from infrastructure.geometric_plasticity import detect_ringing, spectral_analysis

# Detect ringing in oscillation pattern
ringing_metrics = detect_ringing(oscillation_series)

# Quality gate: block degenerate oscillation
if ringing_metrics['degenerate']:
    raise ValueError("Oscillation not converging — restart with diversity injection")
```

**Repository:** [github.com/justindbilyeu/Resonance_Geometry](https://github.com/justindbilyeu/Resonance_Geometry)

---

### 3. Orchestration

**Location:** `infrastructure/orchestration/`
**Status:** 🚧 Not yet integrated

**Purpose:** Multi-AI coordination with architectural diversity

**Capabilities:**
- Fan-out patterns for parallel AI queries (justasking integration)
- Consensus and dissent analysis across diverse models
- Break premature convergence through architectural diversity
- Prevent narrative drift by enforcing minimum dissent

**Integration Point:**
```python
from infrastructure.orchestration import fanout, diversity_score

# Fan out hypothesis to multiple models
variations = fanout(
    hypothesis="...",
    models=["gpt-4", "claude-3", "llama-70b"],
    temperature_range=(0.7, 1.2)
)

# Check diversity
diversity = diversity_score(variations)
if diversity < 0.3:
    # Too much agreement — diversify further
    variations += fanout(hypothesis, inject_dissent=True)
```

**Repository:** [github.com/justindbilyeu/justasking](https://github.com/justindbilyeu/justasking)

---

## Integration Architecture

```
                    Question
                       ↓
              Discovery Compiler
                       ↓
            ┌──────────┼──────────┐
            ↓          ↓          ↓
         ITPU    Geometric-   Orchestration
                 Plasticity
            ↓          ↓          ↓
      Constraint  Ringing    Diversity
       Health     Detection   Actuation
            └──────────┼──────────┘
                       ↓
                 Bundle (validated)
```

Infrastructure components provide feedback to the compiler:
- **ITPU** says when constraint health is improving
- **Geometric-Plasticity** says when oscillation is productive
- **Orchestration** provides architectural diversity on demand

## Current Status

**Directory structure created** ✅
**Integration pending** 🚧

Next steps:
1. Clone upstream repositories
2. Create adapter interfaces
3. Wire minimal integration (v1 thin slice)
4. Validate with Bundle 0001

## Development Philosophy

**v0 Policy:** Adapters + Links, Not Imports

For initial development, we define clean adapter interfaces without importing upstream code. This:
- Decouples development cycles
- Avoids dependency hell
- Forces interface clarity
- Enables experimentation

Real implementations will be wired post-v0 behind feature flags.

See [docs/INTEGRATIONS.md](../docs/INTEGRATIONS.md) for full integration strategy.

---

**Remember:** Infrastructure serves the core compiler. Every component exists to make constraint-based compilation more effective.
