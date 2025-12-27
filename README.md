# Resonance Engine

**Discovery compiler + coherence controller.**

Resonance Engine is a human–AI interface that transforms *intuitive questions* into **preregistered, falsifiable experiments**. It does this by enforcing **constraint-based convergence**: explicit metrics, dissent tracking, and automated falsifiability gates.

> Start here: `docs/PHILOSOPHY.md` — **“Coherence Under Tension”** (why constraints are the medium, and how the Engine avoids narrative drift).

---

## What this is

### 1) Discovery Compiler
Orchestrates multi-AI roles (Builder / Skeptic / Auditor / Operator) to progressively constrain a research question from high-dimensional intuition into a runnable experiment with explicit failure criteria.

### 2) Coherence Controller
Tracks measurable constraint health at each compilation stage (falsifiability, null completeness, operational clarity, skeptic dissent). Decides when to diversify perspectives vs converge on a protocol. Prevents “story coherence” from masquerading as truth by requiring **minimum dissent** and **numeric rejection thresholds**.

---

## What makes this not “prompting”

Traditional prompt engineering optimizes for plausible output.

Resonance Engine optimizes for **experiments that can fail**:

- **Hard Gates:** automated null-completeness gate rejects any preregistration with **< 2 numeric thresholds** that would invalidate the hypothesis.
- **Dissent Metrics:** Builder/Skeptic disagreement must remain above baseline—if they agree too quickly, the controller mandates diversification.
- **Constraint Health Tracking:** falsifiability, operational clarity, and null completeness must improve stage-to-stage or the pipeline restarts.
- **Prereg Standard:** experiments conform to Resonance Method (RM-01+) conventions: locked parameters, stopping rules, acceptance/failure criteria **before execution**.
- **Reproducibility:** third-party replication must be possible from bundle artifacts alone.

**If it doesn’t compile, it’s not yet testable.**

---

## Quickstart

```bash
# Clone
git clone https://github.com/justindbilyeu/Resonance-Engine.git
cd Resonance-Engine

# Install
pip install -e .

# Run tests (validates gates + metric computation)
pytest -q

Generate an experiment bundle from a seed idea

python -m core.discovery_compiler \
  --seed "Your research question here" \
  --output experiments/example_001

cd experiments/example_001
ls
# CLAIM.md  OPERATIONALIZE.md  PREREG.yaml  NULLS.md  COHERENCE_METRICS.yaml  src/  tests/

Review the compilation health

cat COHERENCE_METRICS.yaml

What just happened:
	1.	Templates were compiled into an experiment scaffold
	2.	Null gate verified NULLS.md contains ≥ 2 numeric rejection thresholds
	3.	Constraint-health metrics were recorded in COHERENCE_METRICS.yaml
	4.	You now have a runnable/testing skeleton that can be implemented and executed

⸻

Golden paths

A) Example: examples/golden_path_toy/

A transparent, end-to-end demo (simple coin flip fairness test) showing:
	•	complete bundle structure
	•	null gate passing (multiple numeric thresholds)
	•	runnable experiment + deterministic result
	•	tests validating null evaluation
	•	third-party reproducibility

cd examples/golden_path_toy
python src/experiment.py
pytest -q

B) Bundle #0001: RFO Ringing Wedge (RG² “real content” path)

This repository is designed to host real theory-linked bundles (e.g., Resonance Geometry experiments) that demonstrate the full compile → run → null-eval loop.

Bundle outputs are standardized (see next section). Bundle #0001 is intended to be the canonical “golden path” for RG-linked work.

⸻

Bundle outputs (what compilation produces)

Each compilation cycle produces:

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

Automated Gate: if NULLS.md contains fewer than 2 numeric rejection thresholds, bundle generation fails.

⸻

Repository structure (v0)

Resonance-Engine/
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
├── templates/                      # Bundle templates
├── examples/                       # Demonstrations
├── docs/                           # Philosophy, architecture, metrics, integrations
└── tests/                          # Engine-level tests (gates, metrics, compiler)


⸻

Integration posture

v0 policy: adapters + links, not imports.

Resonance Engine is designed to integrate with a broader stack for:
	•	diversity actuation (multi-model fan-out),
	•	information-theoretic metrics,
	•	oscillation / ringing diagnostics.

Planned integration targets:
	•	JustAsking: architecture-diverse fan-out to prevent premature convergence
	•	ITPU: mutual information / transfer entropy / dissent quantification
	•	Geometric-Plasticity / Resonance Geometry: ringing detection + domain-specific validators

See docs/INTEGRATIONS.md.

⸻

Contributing

Before submitting PRs:
	1.	All new experiments must pass the automated null-completeness gate (≥ 2 numeric thresholds).
	2.	Constraint-health metrics must show stage-to-stage improvement (or explicitly justify a restart).
	3.	Include COHERENCE_METRICS.yaml demonstrating controller decision logic.
	4.	Tests must validate both success and failure pathways.

We value experiments that fail cleanly over experiments that “mostly work.”

⸻

License

MIT

This README is consistent with the repo’s stated purpose (discovery compiler + coherence controller), the **hard gate** requirement (≥2 numeric null thresholds), the bundle artifact standard, and the **integration posture** (adapters/links first).  [oai_citation:0‡github.com](https://github.com/justindbilyeu/Resonance-Engine)
