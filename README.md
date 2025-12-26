# Resonance Engine

A human-AI interface that transforms intuitive questions into preregistered, falsifiable experiments. The system enforces geometric convergence on testable truth through explicit metrics, dissent tracking, and automated falsifiability gates.
> Start here: **[docs/PHILOSOPHY.md](docs/PHILOSOPHY.md)** — “Coherence Under Tension” (why constraints are the medium, and how the Engine avoids narrative drift).
## What This Is

**Discovery Compiler:** Orchestrates multi-AI roles (Builder/Skeptic/Auditor/Operator) to progressively constrain a research question from high-dimensional intuition into a runnable experiment with explicit failure criteria.

**Coherence Controller:** Tracks measurable constraint health (falsifiability, null completeness, operational clarity, skeptic dissent) at each compilation stage. Decides when to diversify perspectives vs converge on protocol. Prevents drift into narrative coherence by requiring minimum dissent and numerical rejection thresholds.

## What Makes This Not Prompting

Traditional prompt engineering optimizes for *plausible output*. Resonance Engine optimizes for *falsifiable experiments* through:

- **Hard Gates:** Automated null-completeness gate (`assert_numeric_nulls`) rejects any preregistration with <2 specific numeric thresholds that would invalidate the hypothesis (see [docs/METRICS.md](docs/METRICS.md))
- **Dissent Metrics:** Builder/Skeptic disagreement must remain above baseline—if they agree too quickly, controller mandates architectural diversity
- **Constraint Health Tracking:** Falsifiability, operational clarity, and null completeness must improve stage-to-stage or pipeline restarts
- **Preregistration Standard:** All experiments conform to [RM-01](https://github.com/justindbilyeu/Resonance-Method) protocol—locked parameters, stopping rules, acceptance/failure criteria before execution
- **Reproducibility Requirement:** Third-party replication must be possible from bundle artifacts alone

The system succeeds when experiments *can fail*—and fail in ways we preregistered.

## Quickstart

**Status (v0 scaffold):** Core package structure and tests are in place. Bundle generation and full compilation cycle coming in PR-2.

```bash
# Clone
git clone https://github.com/justindbilyeu/Resonance-Engine.git
cd Resonance-Engine

# Install
pip install -e .

# Run tests (validates package structure)
python -m pytest -q

# Coming in PR-2: Bundle generator CLI
# python -m core.discovery_compiler --seed "..." --output experiments/example_001/
```

For now, explore the architecture and philosophy:
- [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) - Coherence under tension
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design

## Bundle Outputs

Each compilation cycle produces:

```
experiments/[experiment_id]/
├── CLAIM.md                    # ≤3 sentences, falsifiable, bounded scope
├── OPERATIONALIZE.md           # Observable quantities + measurement protocol
├── PREREG.yaml                 # Locked params, seeds, stopping rules, acceptance/failure criteria
├── NULLS.md                    # ≥2 explicit numeric thresholds that would reject hypothesis
├── COHERENCE_METRICS.yaml      # Constraint health progression + controller decisions
├── src/
│   └── experiment_[id].py      # Runnable implementation
└── tests/
    └── test_experiment_[id].py # Validation + null-threshold checks
```

**Automated Gate:** If `NULLS.md` contains <2 numeric rejection thresholds, bundle generation fails.

## Repository Structure (v0)

```
Resonance-Engine/
├── README.md                   
├── requirements.txt
│
├── core/
│   ├── discovery_compiler.py       # Main orchestration loop
│   ├── coherence_controller.py     # Metric tracking + diversify/converge decisions
│   ├── roles/
│   │   ├── builder.py              # Hypothesis generation
│   │   ├── skeptic.py              # Null identification + adversarial probing
│   │   ├── auditor.py              # Falsifiability validation
│   │   └── operator.py             # Code/test scaffold generation
│   └── metrics/
│       ├── constraint_health.py    # Falsifiability, null completeness, clarity
│       ├── convergence.py          # Stage-to-stage improvement tracking
│       └── dissent.py              # Builder/Skeptic divergence measurement
│
├── templates/
│   ├── CLAIM.template.md
│   ├── OPERATIONALIZE.template.md
│   ├── PREREG.template.yaml
│   ├── NULLS.template.md
│   └── COHERENCE_METRICS.template.yaml
│
├── examples/
│   └── golden_path_hallucination/  # Demonstration: hallucination-as-phase-transition
│       ├── seed_idea.md
│       ├── [full bundle outputs]
│       └── RESULTS.md              # Outcomes + constraint health retrospective
│
├── plugins/
│   └── resonance_geometry/         # Theory-specific validators + metrics
│
└── tests/
    ├── test_null_completeness.py   # Gate validation
    ├── test_constraint_health.py   # Metric computation accuracy
    └── test_discovery_compiler.py  # End-to-end cycle
```

## Theoretical Foundation

Resonance Engine operationalizes concepts from:

- **[Resonance-Method](https://github.com/justindbilyeu/Resonance-Method):** RM-01/02/03 standards for preregistration, red-team protocols, decision trail documentation
- **[Resonance Geometry](https://github.com/justindbilyeu/Resonance_Geometry):** Geometric framework for understanding information dynamics—first “theory plugin” demonstrating how domain-specific validators extend the core compiler

The architecture assumes *ideas have geometry* and that convergence on testable truth is a measurable geometric process, not a subjective narrative.

## Contributing

Before submitting PRs:

1. All new experiments must pass automated null-completeness gate (≥2 numeric thresholds)
1. Constraint health metrics must show stage-to-stage improvement
1. Include `COHERENCE_METRICS.yaml` demonstrating controller decision logic
1. Tests must validate both success *and* failure pathways

We value experiments that *fail cleanly* over those that “mostly work.”

## License

MIT

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

-----

**Status:** v0 (metrics + gates + minimal runnable cycle)  
**Next:** Golden path example (hallucination curvature spike), plugin architecture for theory-specific validators
