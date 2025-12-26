# Metrics and Gates

**Resonance Engine** enforces falsifiability through measurable constraint health metrics and automated gates. This document describes the metrics system and hard gates that ensure experiments can genuinely fail.

---

## Null Completeness Gate

**Module:** `core/metrics/null_gate.py`
**Status:** Implemented (PR-1)
**Type:** Hard gate (blocks bundle generation)

### Purpose

The null completeness gate enforces the first non-negotiable constraint: **no experiment bundle without numeric falsifiers.**

Vague rejection criteria like "if results are inconsistent" or "if performance does not improve" are **not falsifiable**. They invite rationalization and p-hacking. The gate mechanically counts explicit numeric thresholds and rejects any null hypothesis document with fewer than 2 specific, measurable rejection criteria.

### How It Works

The gate uses regex pattern matching to count numeric thresholds in three formats:

1. **Comparator + number**: `>= 2`, `< 0.1`, `<= 10.0`, `> 5`, `== 0`, `!= 1`
2. **Multiplier forms**: `1.5x`, `2x`, `10.2x`
3. **Percentage forms**: `10%`, `0.5%`, `95.5%`

This is a **mechanical gate**, not a "smart" one. It does not attempt semantic analysis or understand context. It simply counts explicit patterns that represent measurable thresholds.

### API

#### `count_numeric_thresholds(text: str) -> int`

Counts the number of numeric threshold expressions in text.

```python
from core.metrics.null_gate import count_numeric_thresholds

text = "Reject if accuracy < 0.55 and delta >= 0.10"
count = count_numeric_thresholds(text)
# Returns: 2
```

#### `assert_numeric_nulls(text: str, min_thresholds: int = 2) -> None`

Validates that text contains at least `min_thresholds` numeric thresholds. Raises `ValueError` with helpful message if validation fails.

```python
from core.metrics.null_gate import assert_numeric_nulls

# This passes (2 thresholds)
assert_numeric_nulls("Reject if accuracy < 0.55 and delta >= 0.10")

# This fails (0 thresholds)
assert_numeric_nulls("Reject if results are inconsistent")
# Raises: ValueError with examples and guidance
```

#### `find_numeric_thresholds(text: str) -> List[Tuple[str, int, int]]`

Returns all numeric thresholds with their positions in text. Useful for debugging or detailed analysis.

```python
from core.metrics.null_gate import find_numeric_thresholds

text = "Reject if x < 0.5 or y >= 2"
thresholds = find_numeric_thresholds(text)
# Returns: [('< 0.5', 13, 18), ('>= 2', 24, 28)]
```

### Usage in Discovery Compiler

The gate is enforced during bundle generation (PR-2):

```python
from core.metrics.null_gate import assert_numeric_nulls

# Read generated NULLS.md
with open(output_dir / "NULLS.md") as f:
    nulls_content = f.read()

# Enforce gate (raises if < 2 thresholds)
assert_numeric_nulls(nulls_content, min_thresholds=2)

# If we get here, bundle generation can proceed
```

If the gate fails, bundle generation is **aborted** and no partial artifacts are left behind.

### Examples

#### ✓ Passing Examples

```markdown
# Null Hypotheses

Reject if:
- Accuracy < 0.55 (barely above random)
- Improvement over baseline <= 5%
```

**Threshold count:** 2 ✓

```markdown
# Rejection Criteria

We will reject the hypothesis if ANY of:
1. Classification accuracy < 0.60
2. Speedup <= 1.5x baseline
3. Error rate > 10%
4. Variance across runs > 2x mean
```

**Threshold count:** 4 ✓

#### ✗ Failing Examples

```markdown
# Null Hypotheses

Reject if:
- Results are inconsistent across runs
- Performance does not improve significantly
- The model appears to overfit
```

**Threshold count:** 0 ✗

```markdown
# Rejection Criteria

Reject if accuracy is below acceptable threshold.
```

**Threshold count:** 0 ✗ (no specific number given)

### Design Rationale

**Why 2 thresholds minimum?**

One threshold is easy to rationalize away or adjust post-hoc. Two independent thresholds create genuine constraint. They force you to think about multiple ways the hypothesis could fail.

**Why mechanical pattern matching instead of semantic analysis?**

Semantic analysis is:
- Unreliable (LLMs can be convinced that vague criteria are "specific")
- Non-reproducible (different models/temperatures give different results)
- Gameable (prompt engineering to pass validation)

Mechanical pattern matching is:
- Deterministic (same input → same output)
- Transparent (you can see exactly what it's counting)
- Honest (forces you to write actual numbers)

**What are the limitations?**

The gate will:
- Not catch semantically meaningless thresholds ("reject if accuracy < 1000")
- Not validate that thresholds are appropriate for the domain
- Count thresholds that appear in non-null contexts (low false positive rate in practice)

These are acceptable tradeoffs. The gate's job is to enforce **numeric specificity**, not semantic correctness. Semantic validation is the Auditor role's job (future PR).

### Error Messages

When the gate fails, it provides actionable guidance:

```
ValueError: Null completeness gate failure: Found 0 numeric threshold(s), need at least 2.

Numeric thresholds must be explicit and measurable. Examples:
  ✓ 'Reject if accuracy < 0.55'
  ✓ 'Reject if speedup <= 1.5x baseline'
  ✓ 'Reject if error rate > 10%'
  ✗ 'Reject if results are inconsistent'
  ✗ 'Reject if performance does not improve'

Add 2 more numeric threshold(s) to your null hypotheses.
```

---

## Future Metrics (Post-PR-1)

### Falsifiability Score

**Module:** `core/metrics/constraint_health.py` (stub exists)
**Status:** Future work

Measures how falsifiable a claim is based on its null hypotheses, operational definitions, and measurement protocol.

### Null Completeness Score

**Module:** `core/metrics/constraint_health.py` (stub exists)
**Status:** Future work

Beyond just counting thresholds, measures coverage of potential failure modes and quality of null hypotheses.

### Operational Clarity Score

**Module:** `core/metrics/constraint_health.py` (stub exists)
**Status:** Future work

Measures how operationally clear a protocol is—can a third party reproduce this from the artifacts alone?

### Dissent Metrics

**Module:** `core/metrics/dissent.py` (stub exists)
**Status:** Future work

Measures Builder/Skeptic disagreement levels to detect premature convergence (agreement rising too quickly → narrative lock-in).

### Convergence Metrics

**Module:** `core/metrics/convergence.py` (stub exists)
**Status:** Future work

Tracks stage-to-stage improvement in constraint health. Detects productive progress vs stalling vs degenerate oscillations.

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - Overall system design
- [PHILOSOPHY.md](PHILOSOPHY.md) - Why constraints are the medium
- [Repository README](../README.md) - Usage and quickstart
