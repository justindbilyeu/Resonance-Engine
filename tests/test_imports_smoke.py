"""
Smoke tests for Resonance Engine imports.

Ensures all core modules are importable and the package structure is consistent.
"""

import pytest


def test_core_package_imports():
    """Test that core package and main modules can be imported."""
    import core
    from core import discovery_compiler
    from core import coherence_controller

    assert hasattr(core, '__version__')
    assert hasattr(discovery_compiler, 'compile')
    assert hasattr(coherence_controller, 'CoherenceController')


def test_roles_package_imports():
    """Test that all role modules can be imported."""
    from core.roles import builder
    from core.roles import skeptic
    from core.roles import auditor
    from core.roles import operator

    assert hasattr(builder, 'Builder')
    assert hasattr(skeptic, 'Skeptic')
    assert hasattr(auditor, 'Auditor')
    assert hasattr(operator, 'Operator')


def test_metrics_package_imports():
    """Test that all metrics modules can be imported."""
    from core.metrics import constraint_health
    from core.metrics import convergence
    from core.metrics import dissent

    # Constraint health metrics
    assert hasattr(constraint_health, 'measure_falsifiability')
    assert hasattr(constraint_health, 'measure_null_completeness')
    assert hasattr(constraint_health, 'measure_operational_clarity')

    # Convergence metrics
    assert hasattr(convergence, 'measure_stage_improvement')
    assert hasattr(convergence, 'detect_convergence')

    # Dissent metrics
    assert hasattr(dissent, 'measure_dissent')
    assert hasattr(dissent, 'detect_premature_convergence')


def test_stubs_raise_not_implemented():
    """Test that stub implementations raise NotImplementedError as expected."""
    from core.roles.builder import Builder
    from core.metrics.constraint_health import measure_falsifiability

    # Role stub
    with pytest.raises(NotImplementedError):
        Builder()

    # Metric stub
    with pytest.raises(NotImplementedError):
        measure_falsifiability("test claim", [])
