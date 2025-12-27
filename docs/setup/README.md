# Setup Documentation

This directory contains guides for setting up and using Resonance Engine.

## Quick Start

**New to Resonance Engine?** Start here:

1. **[CLAUDE_CODE_QUICKSTART.md](./CLAUDE_CODE_QUICKSTART.md)** — Get up and running in 5 minutes
2. **[CLAUDE_CODE_CHEATSHEET.md](./CLAUDE_CODE_CHEATSHEET.md)** — Common commands and patterns
3. **[setup_resonance_engine.md](./setup_resonance_engine.md)** — Comprehensive setup guide

## Documentation Index

### For Users

**[INDEX.md](./INDEX.md)** — Complete documentation index

**[CLAUDE_CODE_QUICKSTART.md](./CLAUDE_CODE_QUICKSTART.md)**
- Installation (5 minutes)
- Your first bundle
- Running tests
- Basic workflow

**[CLAUDE_CODE_CHEATSHEET.md](./CLAUDE_CODE_CHEATSHEET.md)**
- Command reference
- Common patterns
- Troubleshooting
- Quick lookups

### For Developers

**[setup_resonance_engine.md](./setup_resonance_engine.md)**
- Full system architecture
- Integration with ITPU, Geometric-Plasticity, Orchestration
- Development workflow
- Contributing guidelines

**[organize_repos.py](./organize_repos.py)**
- Repository organization automation
- Bundle structure validation
- Cleanup scripts

## Installation

### Prerequisites

```bash
# Python 3.10+ required
python --version  # Should be 3.10 or higher

# Git for version control
git --version
```

### Basic Setup

```bash
# Clone repository
git clone https://github.com/justindbilyeu/Resonance-Engine.git
cd Resonance-Engine

# Install dependencies
pip install -e .

# Run tests to verify installation
python -m pytest -q
```

Expected output: All tests pass ✓

## Your First Bundle

```bash
# Generate experiment bundle from a research question
python -m core.discovery_compiler \
  --seed "Your research question here" \
  --output bundles/0002_my_first_experiment

# Inspect generated bundle
cd bundles/0002_my_first_experiment
ls  # CLAIM.md, NULLS.md, PREREG.yaml, etc.

# Review constraint health
cat COHERENCE_METRICS.yaml
```

## Common Workflows

### 1. Development Mode

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=core tests/

# Format code
black core/ tests/

# Type checking
mypy core/
```

### 2. Creating Experiments

```bash
# Generate bundle
python -m core.discovery_compiler --seed "..." --output bundles/XXXX

# Customize templates
# Edit CLAIM.md, NULLS.md, etc.

# Validate null completeness
# NULLS.md must have ≥2 numeric thresholds
```

### 3. Integration Testing

```bash
# Test full pipeline
python -m pytest tests/system/

# Test individual components
python -m pytest tests/unit/test_null_gate.py
python -m pytest tests/integration/
```

## Troubleshooting

### Tests Failing?

```bash
# Check Python version
python --version  # Must be ≥3.10

# Reinstall dependencies
pip install -e . --force-reinstall

# Clear pytest cache
rm -rf .pytest_cache
pytest --cache-clear
```

### Bundle Generation Fails?

**Common issue:** Null completeness gate rejects NULLS.md

**Solution:** Ensure NULLS.md has ≥2 explicit numeric thresholds

✓ Good: "Reject if accuracy < 0.55"
✓ Good: "Reject if speedup <= 1.5x baseline"
✗ Bad: "Reject if results are inconsistent"

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/justindbilyeu/Resonance-Engine/issues)
- **Documentation:** `docs/`
- **Examples:** `examples/golden_path_toy/`

## Philosophy

Before diving into setup, read:
- **[docs/PHILOSOPHY.md](../PHILOSOPHY.md)** — Why constraints enable rather than limit
- **[docs/ARCHITECTURE.md](../ARCHITECTURE.md)** — System design

Understanding the "why" makes the "how" much clearer.

---

**Remember:** Resonance Engine exists to make human-AI cognition more coherent than either alone. Every constraint serves that goal.
