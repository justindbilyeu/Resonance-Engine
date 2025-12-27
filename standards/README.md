# Resonance Method Standards

**Status:** Directory structure created, specifications pending

This directory contains the rigorous standards (RM-01, RM-02, RM-03) that ensure epistemic quality in compiled experiments.

## Overview

Resonance Method standards define **non-negotiable constraints** that experiments must satisfy to be considered valid. These aren't guidelines—they're **hard gates** enforced by the compiler.

## Standards Hierarchy

```
RM-01: Epistemic Rigor
  ↓
RM-02: Red-Team Procedures
  ↓
RM-03: Falsifiability Requirements
```

Each standard builds on the previous, creating a **constraint cascade** that filters out weak experiments.

---

## RM-01: Epistemic Rigor

**Location:** `standards/rm01/`
**Status:** 🚧 Specification pending

**Purpose:** Maintain epistemic rigor throughout the compilation process

**Key Requirements:**

1. **Preregistration**
   - All parameters locked before execution
   - Stopping rules explicit
   - Success/failure criteria defined upfront

2. **Hypothesis Clarity**
   - Claims must be ≤3 sentences
   - Scope must be bounded
   - Terms must be operationally defined

3. **Data Handling**
   - Measurement protocol explicit
   - No post-hoc analysis without preregistration
   - Reproducibility from bundle alone

**Enforcement:**
- Compiler validates PREREG.yaml completeness
- CLAIM.md must pass sentence count check
- OPERATIONALIZE.md must define all terms

**See:** `standards/rm01/SPECIFICATION.md` (to be created)

---

## RM-02: Red-Team Procedures

**Location:** `standards/rm02/`
**Status:** 🚧 Specification pending

**Purpose:** Structured adversarial validation

**Key Requirements:**

1. **Skeptic Role Protocols**
   - Must identify ≥3 distinct failure modes
   - Must propose alternative explanations
   - Must challenge hidden assumptions

2. **Challenge Generation**
   - Steel-man the opposing view
   - Find the experiment's weakest point
   - Propose hardest-to-pass null hypothesis

3. **Stress Testing**
   - Test edge cases
   - Violate assumptions to find brittleness
   - Check for survivorship bias

**Enforcement:**
- Dissent metrics must remain above baseline
- Builder/Skeptic agreement requires justification
- Auditor validates challenge quality

**See:** `standards/rm02/SPECIFICATION.md` (to be created)

---

## RM-03: Falsifiability Requirements

**Location:** `standards/rm03/`
**Status:** 🚧 Specification pending

**Purpose:** Ensure experiments are genuinely falsifiable

**Key Requirements:**

1. **Numeric Rejection Thresholds**
   - **Hard gate:** ≥2 explicit numeric thresholds in NULLS.md
   - Thresholds must be evaluable before execution
   - "Reject if accuracy < 0.55" ✓
   - "Reject if results are inconsistent" ✗

2. **Hard-Gate Stopping Rules**
   - Experiment must terminate on specific conditions
   - No manual "looks good enough" judgments
   - Automate pass/fail determination

3. **Null Hypothesis Specifications**
   - Null must predict specific outcomes
   - Must be testable independently
   - Acceptance of null = rejection of hypothesis

**Enforcement:**
- `assert_numeric_nulls()` in null_gate.py
- Compiler rejects bundles with <2 thresholds
- PREREG.yaml must include stopping rules

**Current Implementation:**
```python
from core.metrics.null_gate import assert_numeric_nulls

# Enforced during bundle generation
nulls_content = read_file("NULLS.md")
assert_numeric_nulls(nulls_content, min_thresholds=2)
# Raises ValueError if <2 numeric thresholds found
```

**See:**
- `core/metrics/null_gate.py` (implemented)
- `docs/METRICS.md` (documentation)
- `standards/rm03/SPECIFICATION.md` (to be created)

---

## Integration with Compiler

Standards are enforced at compile time:

```python
from core import ResonanceEngine

engine = ResonanceEngine()
bundle = engine.compile(
    question="Your research question",
    standards=['RM-01', 'RM-02', 'RM-03']  # Enforced
)
```

If any standard is violated, compilation fails with explicit feedback.

## Standard Violations

### Examples of Failures

**RM-01 Violation:**
```
❌ CLAIM.md exceeds 3 sentences (found 5)
```

**RM-02 Violation:**
```
❌ Skeptic dissent too low (0.12 < 0.30 threshold)
   Requires diversity injection or restart
```

**RM-03 Violation:**
```
❌ Null completeness gate failure
   Found 1 numeric threshold, need at least 2

   Add numeric thresholds to NULLS.md:
   ✓ "Reject if accuracy < 0.55"
   ✓ "Reject if speedup <= 1.5x baseline"
   ✗ "Reject if results are inconsistent"
```

## Development Status

| Standard | Specification | Implementation | Tests | Docs |
|----------|--------------|----------------|-------|------|
| **RM-01** | 🚧 Pending | ⚠️ Partial | ❌ None | ❌ None |
| **RM-02** | 🚧 Pending | ⚠️ Partial | ❌ None | ❌ None |
| **RM-03** | ✅ Complete | ✅ Complete | ✅ 30 tests | ✅ docs/METRICS.md |

**Next steps:**
1. Write RM-01 specification
2. Write RM-02 specification
3. Expand RM-03 specification (currently in METRICS.md)
4. Implement remaining enforcement logic
5. Create comprehensive test suites

## Philosophy

**Constraints enable rather than limit.**

Standards aren't bureaucracy—they're the **medium** that enables coherent experiments to emerge from distributed human-AI cognition.

Just as musical instruments need constraints (strings under tension, resonant chambers) to produce coherent sound, research needs constraints to produce testable truth.

---

**Remember:** We value experiments that **fail cleanly** over those that "mostly work." Standards ensure failures are meaningful.
