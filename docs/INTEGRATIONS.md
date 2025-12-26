# Integration Strategy

**Status:** v1 (justasking thin slice implemented; ITPU/GP still adapters only)

Resonance Engine is designed to integrate with a broader stack of tools for diversity actuation, metrics computation, and diagnostic analysis. This document describes the integration architecture and implementation status.

---

## Integration Philosophy

**v0 Policy: Adapters + Links, Not Imports**

For the initial release, Resonance Engine defines clean adapter interfaces to upstream repositories but does **not** import or vendor their code. This approach:

- **Decouples development cycles:** Each repo can evolve independently
- **Avoids dependency hell:** No version conflicts or transitive dependencies in v0
- **Forces interface clarity:** Adapters must expose minimal, well-defined APIs
- **Enables experimentation:** Users can swap implementations or skip integrations

**Future:** Once interfaces stabilize and upstream repos reach 1.0, we may add optional dependencies or vendored implementations behind feature flags.

---

## Integration Stack

### 1. justasking — Diversity Actuator (Fan-Out)

**Repository:** [github.com/justindbilyeu/justasking](https://github.com/justindbilyeu/justasking)

**Purpose:** Generate diverse perspectives on a research question by fanning out prompts across multiple models/temperatures/system prompts.

**Role in Resonance Engine:**
- **Discovery stage:** When Coherence Controller decides to "diversify," justasking fans out the current hypothesis to multiple LLMs to generate architectural diversity
- **Prevents premature convergence:** If Builder/Skeptic agree too quickly, justasking injects alternate framings
- **Dissent generation:** Produces competing interpretations that Skeptic can use to identify failure modes

**Adapter Interface:** `core/integrations/justasking_adapter.py`

```python
def fanout(
    prompt_bundle: dict,
    models: list[str],
    temperature_range: tuple[float, float] = (0.7, 1.2),
    n_variations: int = 5
) -> list[dict]:
    """
    Fan out a prompt to multiple models/temperatures for diversity.

    Returns list of responses with metadata (model, temp, timestamp).
    """
```

**Example use case:**
```python
# When dissent drops below threshold, diversify
if dissent_score < 0.3:
    variations = fanout(
        prompt_bundle={"hypothesis": current_claim, "context": operationalize_doc},
        models=["gpt-4", "claude-3", "llama-70b"],
        n_variations=5,
        simulate=True  # v1: simulated diversity for demo
    )
    # Feed variations to Skeptic for adversarial critique

# With diversity metrics
responses, metrics = fanout_with_diversity_metrics(
    prompt_bundle={"hypothesis": claim},
    target_diversity=0.7
)
print(f"Diversity achieved: {metrics['diversity_achieved']}")
```

**Status:** ✅ v1 thin slice implemented
- `fanout()`: Simulated fan-out with synthetic diverse responses
- `compute_diversity_score()`: Measures model/text/temperature diversity
- `fanout_with_diversity_metrics()`: Iterative fan-out until target diversity reached
- DISSENT.md template for documenting disagreement maps
- 23 comprehensive tests validating structure

**v1 Implementation:**
- Simulated responses demonstrate structure without requiring LLM API calls
- Deterministic output for reproducibility
- Ready to swap with real justasking calls when available
- Feature flag: `simulate=True` (default) vs `simulate=False` (raises NotImplementedError)

---

### 2. ITPU — Metrics Provider (Mutual Information / Windowed MI)

**Repository:** [github.com/justindbilyeu/ITPU](https://github.com/justindbilyeu/ITPU)

**Purpose:** Information-theoretic metrics for measuring dependencies, correlations, and information flow in experimental data.

**Role in Resonance Engine:**
- **Constraint health metrics:** Measure mutual information between claim and null hypotheses (are they truly independent?)
- **Convergence detection:** Windowed MI across compilation stages to detect when constraint health is improving
- **Dissent quantification:** MI between Builder and Skeptic outputs (low MI = high dissent)

**Adapter Interface:** `core/integrations/itpu_adapter.py`

```python
def compute_mutual_info(
    x: np.ndarray,
    y: np.ndarray,
    method: str = "ksg",  # Kraskov-Stögbauer-Grassberger estimator
    k: int = 3
) -> float:
    """
    Compute mutual information between two variables.

    Returns MI in nats (natural units).
    """

def windowed_mutual_info(
    series: list[np.ndarray],
    window_size: int = 3,
    stride: int = 1
) -> np.ndarray:
    """
    Compute windowed MI across a time series of distributions.

    Useful for tracking convergence over compilation stages.
    """
```

**Example use case:**
```python
# Measure Builder/Skeptic dissent via MI
builder_embedding = embed_text(builder_output)
skeptic_embedding = embed_text(skeptic_output)
dissent_score = 1.0 - compute_mutual_info(builder_embedding, skeptic_embedding)

# Track constraint health improvement across stages
stage_embeddings = [embed_stage(s) for s in compilation_stages]
convergence = windowed_mutual_info(stage_embeddings, window_size=3)
```

**Status:** Adapter stub only (NotImplementedError)

---

### 3. Geometric-Plasticity — Diagnostics Exemplar (Ringing Criteria)

**Repository:** [github.com/justindbilyeu/Resonance_Geometry](https://github.com/justindbilyeu/Resonance_Geometry) (submodule: geometric-plasticity)

**Purpose:** Theory-specific validators for geometric phase transitions, ringing detection, and curvature analysis.

**Role in Resonance Engine:**
- **First "theory plugin":** Demonstrates how domain-specific validators extend the core compiler
- **Ringing detection:** Detect when constraint health oscillates without improving (degenerate oscillation)
- **Phase transition identification:** Identify when discovery process transitions from exploration → execution

**Adapter Interface:** `core/integrations/gp_adapter.py`

```python
def detect_ringing(
    series: np.ndarray,
    psd_threshold_db: float = 6.0,
    min_overshoots: int = 2,
    window_size: int = 10
) -> dict:
    """
    Detect ringing (persistent oscillation without convergence).

    Uses power spectral density analysis to identify resonance peaks
    and overshoot counting to validate.

    Returns:
        {
            "is_ringing": bool,
            "dominant_frequency": float,
            "overshoot_count": int,
            "damping_ratio": float
        }
    """

def compute_curvature_spike(
    trajectory: np.ndarray,
    method: str = "discrete"
) -> tuple[np.ndarray, list[int]]:
    """
    Compute curvature along a trajectory and identify spikes.

    Useful for detecting phase transitions in constraint space.
    """
```

**Example use case:**
```python
# Detect degenerate oscillation in constraint health
constraint_health_series = [stage["falsifiability"] for stage in stages]
ringing_analysis = detect_ringing(
    series=np.array(constraint_health_series),
    psd_threshold_db=6.0,
    min_overshoots=2
)

if ringing_analysis["is_ringing"]:
    controller.decision = "restart"  # Kill degenerate oscillation
```

**Status:** Adapter stub only (NotImplementedError)

---

## Adapter Implementation Status

| Adapter | Repository | Interface Defined | Implementation | Tests |
|---------|-----------|-------------------|----------------|-------|
| `justasking_adapter` | [justasking](https://github.com/justindbilyeu/justasking) | ✓ | Stub (NotImplementedError) | Import test only |
| `itpu_adapter` | [ITPU](https://github.com/justindbilyeu/ITPU) | ✓ | Stub (NotImplementedError) | Import test only |
| `gp_adapter` | [Resonance_Geometry](https://github.com/justindbilyeu/Resonance_Geometry) | ✓ | Stub (NotImplementedError) | Import test only |

---

## Integration Roadmap

### v0 (Current)
- ✓ Adapter interfaces defined
- ✓ Docstrings with usage examples
- ✓ Links to upstream repositories
- ✓ Import tests (no actual implementation)

### Post-v0 (Future)
1. **Wire justasking fan-out** behind `--enable-diversity-fanout` flag
2. **Vendor or depend on ITPU** after license review + interface freeze
3. **Implement GP diagnostics** as optional plugin (`plugins/geometric_plasticity/`)
4. **Add integration tests** with mock implementations
5. **Feature flags** for enabling/disabling each integration

### Integration Criteria
Before wiring real implementations:
- Upstream repo has tagged release (≥0.1.0)
- License is compatible (MIT/Apache/BSD)
- Interface is stable (documented + tested)
- Integration adds clear value (not just nice-to-have)

---

## Design Principles

**1. Adapters are thin**
- No business logic in adapters
- Simple function signatures
- Clear input/output types
- Raise NotImplementedError until wired

**2. Links over imports**
- Document what each integration does
- Provide usage examples
- Point to upstream repos
- Don't vendor code in v0

**3. Fail gracefully**
- Missing integrations should not break core functionality
- Provide helpful error messages
- Suggest installation steps
- Allow disabling via flags

**4. Clean interfaces**
- Adapters expose minimal APIs
- Hide upstream complexity
- Use standard types (numpy arrays, dicts, not custom classes)
- Document expected shapes/formats

---

## Example Integration Flow

```python
# Hypothetical future implementation (post-v0)

from core.integrations import justasking_adapter, itpu_adapter, gp_adapter

# Discovery stage: Builder generates hypothesis
hypothesis = builder.generate(seed)

# Skeptic critiques
critique = skeptic.critique(hypothesis)

# Measure dissent
builder_emb = embed(hypothesis)
skeptic_emb = embed(critique)
dissent = 1.0 - itpu_adapter.compute_mutual_info(builder_emb, skeptic_emb)

# If dissent too low, diversify using justasking
if dissent < 0.3:
    variations = justasking_adapter.fanout(
        prompt_bundle={"hypothesis": hypothesis},
        models=["gpt-4", "claude-3"],
        n_variations=5
    )
    # Feed to Skeptic for more aggressive critique

# Track constraint health over stages
health_series = [stage["falsifiability"] for stage in stages]
ringing = gp_adapter.detect_ringing(health_series)

if ringing["is_ringing"]:
    print("Degenerate oscillation detected. Restarting compilation.")
    controller.decision = "restart"
```

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - Overall system design
- [METRICS.md](METRICS.md) - Constraint health metrics
- [PHILOSOPHY.md](PHILOSOPHY.md) - Why adapters instead of tight coupling

---

**Questions?**
- For justasking integration: See [justasking/README.md](https://github.com/justindbilyeu/justasking)
- For ITPU integration: See [ITPU/README.md](https://github.com/justindbilyeu/ITPU)
- For Geometric-Plasticity: See [Resonance_Geometry](https://github.com/justindbilyeu/Resonance_Geometry)
