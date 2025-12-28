# Resonance Engine

**Discovery Compiler + Coherence Controller**

A human-AI interface that transforms intuitive research questions into **preregistered, falsifiable experiments** through constraint-based compilation.

> **Start here:** [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) — *"Coherence Under Tension"* (why constraints enable rather than limit, and how the Engine avoids narrative drift)

---

## What This Is

### Discovery Compiler
Orchestrates multi-AI roles (Builder/Skeptic/Auditor/Operator) to progressively constrain a research question from high-dimensional intuition into a **runnable experiment with explicit failure criteria**.

### Coherence Controller
Tracks measurable constraint health at each compilation stage (falsifiability, null completeness, operational clarity, skeptic dissent). Decides when to diversify perspectives vs converge on protocol. Prevents narrative drift by requiring **minimum dissent** and **numeric rejection thresholds**.

---

## What Makes This Not "Prompting"

Traditional prompt engineering optimizes for **plausible output**.
Resonance Engine optimizes for **experiments that can fail**:

- **Hard Gates:** Automated null-completeness gate (`assert_numeric_nulls`) rejects any preregistration with **< 2 numeric thresholds** that would invalidate the hypothesis ([docs/METRICS.md](docs/METRICS.md))
- **Dissent Metrics:** Builder/Skeptic disagreement must remain above baseline—if they agree too quickly, controller mandates diversity injection
- **Constraint Health Tracking:** Falsifiability, operational clarity, and null completeness must improve stage-to-stage or pipeline restarts
- **Preregistration Standard:** All experiments conform to Resonance Method (RM-01/02/03): locked parameters, stopping rules, acceptance/failure criteria **before execution**
- **Reproducibility:** Third-party replication must be possible from bundle artifacts alone

**The system succeeds when experiments can fail—and fail in ways we preregistered.**

---

## Quickstart

### Installation

```bash
# Clone repository
git clone https://github.com/justindbilyeu/Resonance-Engine.git
cd Resonance-Engine

# Install
pip install -e .

# Run tests (validates gates + metrics)
python -m pytest -q
```

### Generate Your First Bundle

```bash
# Compile a research question into an experiment bundle
python -m core.discovery_compiler \
  --seed "Your research question here" \
  --output bundles/my_experiment

# Inspect generated bundle
cd bundles/my_experiment
ls  # CLAIM.md, NULLS.md, PREREG.yaml, COHERENCE_METRICS.yaml, src/, tests/

# Review constraint health
cat COHERENCE_METRICS.yaml
```

**What just happened:**
1. Templates compiled into experiment scaffold
2. Null gate verified NULLS.md has ≥2 numeric rejection thresholds
3. Constraint health metrics recorded
4. Ready-to-customize experiment structure generated

---

## Example: Golden Path Toy

**See:** [examples/golden_path_toy/](examples/golden_path_toy/)

Transparent coin flip fairness test demonstrating the complete workflow:

```bash
cd examples/golden_path_toy

# Run the experiment
python src/experiment.py

# Run tests
python -m pytest -v
```

**What it demonstrates:**
- ✓ Complete bundle structure (CLAIM, OPERATIONALIZE, PREREG, NULLS, COHERENCE_METRICS)
- ✓ Null completeness gate passes (4 numeric thresholds)
- ✓ Runnable experiment with deterministic results (seed=42)
- ✓ Tests validate null hypothesis evaluation
- ✓ Third-party reproducibility from bundle alone

The example is intentionally simple (coin flips) to make the structure transparent. Real experiments follow the same pattern but with more complex hypotheses.

---

## Bundle 0001: RFO Ringing Wedge

**See:** [bundles/0001_rfo_ringing_wedge/](bundles/0001_rfo_ringing_wedge/)

First complete experiment compiled by Resonance Engine, proving the entire stack works end-to-end. This bundle validates Resonance Geometry theory predictions through falsifiable numeric thresholds.

**Status:** Complete bundle structure, ready for execution

---

## Repository Structure

```
Resonance-Engine/
├── bundles/                        # Compiled experiment bundles
│   ├── README.md                   # Bundle philosophy + standards
│   └── 0001_rfo_ringing_wedge/     # First proof-of-concept bundle
│
├── core/                           # Discovery compiler implementation
│   ├── discovery_compiler.py       # Main orchestration loop
│   ├── coherence_controller.py     # Metric tracking + controller decisions
│   ├── roles/                      # Builder/Skeptic/Auditor/Operator
│   │   ├── builder.py
│   │   ├── skeptic.py
│   │   ├── auditor.py
│   │   └── operator.py
│   ├── metrics/                    # Constraint health tracking
│   │   └── null_gate.py            # Null completeness enforcement
│   └── integrations/               # Adapter interfaces
│       ├── justasking_adapter.py
│       ├── itpu_adapter.py
│       └── gp_adapter.py
│
├── infrastructure/                 # Supporting components (integration pending)
│   ├── README.md                   # Integration architecture
│   ├── itpu/                       # Information-theoretic metrics
│   ├── geometric_plasticity/       # Ringing diagnostics
│   └── orchestration/              # Multi-AI coordination
│
├── standards/                      # RM-01, RM-02, RM-03 specifications
│   ├── README.md                   # Standards hierarchy
│   ├── rm01/                       # Epistemic Rigor
│   ├── rm02/                       # Red-Team Procedures
│   └── rm03/                       # Falsifiability Requirements
│
├── docs/                           # Documentation
│   ├── PHILOSOPHY.md               # Why constraints enable rather than limit
│   ├── ARCHITECTURE.md             # System design
│   ├── METRICS.md                  # Null completeness gate + metrics
│   ├── INTEGRATIONS.md             # Integration strategy
│   └── setup/                      # Setup guides
│       ├── README.md
│       ├── CLAUDE_CODE_QUICKSTART.md
│       └── CLAUDE_CODE_CHEATSHEET.md
│
├── examples/                       # Working examples
│   └── golden_path_toy/            # Simple demonstration
│
├── templates/                      # Bundle generation templates
│   ├── CLAIM.template.md
│   ├── OPERATIONALIZE.template.md
│   ├── PREREG.template.yaml
│   ├── NULLS.template.md
│   └── COHERENCE_METRICS.template.yaml
│
└── tests/                          # Test suite
    ├── test_null_gate.py           # Gate validation (30 tests)
    ├── test_bundle_generation.py   # Compilation tests
    └── test_adapters_exist.py      # Integration stubs
```

---

## Bundle Standard (What Compilation Produces)

Each compilation cycle produces a complete experiment bundle:

```
bundles/[experiment_id]/
├── CLAIM.md                    # ≤3 sentences, falsifiable, bounded scope
├── OPERATIONALIZE.md           # Observable quantities + measurement protocol
├── PREREG.yaml                 # Locked params, seeds, stopping rules
├── NULLS.md                    # ≥2 explicit numeric rejection thresholds
├── COHERENCE_METRICS.yaml      # Constraint health + controller decisions
├── src/
│   └── experiment.py           # Runnable implementation
└── tests/
    └── test_experiment.py      # Validation + null-threshold checks
```

**Automated Gate:** If NULLS.md contains < 2 numeric rejection thresholds, bundle generation fails.

**Examples:**
- ✓ "Reject if accuracy < 0.55"
- ✓ "Reject if speedup <= 1.5x baseline"
- ✗ "Reject if results are inconsistent"

---

## Integration Posture

**v0 Policy: Adapters + Links, Not Imports**

Resonance Engine integrates with a broader cognitive infrastructure stack:

- **[justasking](https://github.com/justindbilyeu/justasking):** Multi-model fan-out for diversity actuation
- **[ITPU](https://github.com/justindbilyeu/ITPU):** Information-theoretic metrics (MI, transfer entropy)
- **[Geometric-Plasticity](https://github.com/justindbilyeu/Resonance_Geometry):** Ringing detection + spectral analysis

**Current status:** Clean adapter interfaces defined (`core/integrations/`), no upstream code imported. This decouples development cycles and forces interface clarity. Real implementations will be wired post-v0 behind feature flags.

**See:** [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) for full strategy.

---

## Theoretical Foundation

Resonance Engine operationalizes concepts from:

- **[Resonance Method](https://github.com/justindbilyeu/Resonance-Method):** RM-01/02/03 standards for preregistration and epistemic rigor
- **[Resonance Geometry](https://github.com/justindbilyeu/Resonance_Geometry):** Geometric framework for information dynamics and constraint-based convergence

The architecture assumes *ideas have geometry* and that convergence on testable truth is a measurable geometric process, not subjective narrative.

---

## Contributing

Before submitting PRs:

1. All new experiments must pass automated null-completeness gate (≥2 numeric thresholds)
2. Constraint health metrics must show stage-to-stage improvement
3. Include COHERENCE_METRICS.yaml demonstrating controller decision logic
4. Tests must validate both success *and* failure pathways

**We value experiments that fail cleanly over those that "mostly work."**

---

## Documentation

- **Philosophy:** [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) — Why constraints are the medium
- **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — System design
- **Metrics:** [docs/METRICS.md](docs/METRICS.md) — Null completeness gate
- **Setup Guides:** [docs/setup/](docs/setup/) — Installation and quickstart
- **Bundles:** [bundles/README.md](bundles/README.md) — Experiment bundle standards
- **Infrastructure:** [infrastructure/README.md](infrastructure/README.md) — Integration architecture
- **Standards:** [standards/README.md](standards/README.md) — RM-01/02/03 specifications

---

## License

MIT

---

## Citation

If you use Resonance Engine in research:

```bibtex
@software{resonance_engine_2025,
  author = {Bilyeu, Justin D.},
  title = {Resonance Engine: Discovery Compiler + Coherence Controller},
  year = {2025},
  url = {https://github.com/justindbilyeu/Resonance-Engine}
}
```

---

**Remember:** Constraints aren't limitations—they're the medium that enables coherent experiments to emerge from distributed human-AI cognition. Every gate, every metric, every standard serves that goal.
