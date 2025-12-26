"""
Tests for Integration Adapters

Validates that adapter modules exist, can be imported, and expose expected
function signatures. Does NOT test actual implementation (all stubs in v0).
"""

import pytest
import numpy as np


class TestAdapterImports:
    """Test that adapter modules can be imported."""

    def test_integrations_package_imports(self):
        """Test that integrations package can be imported."""
        from core import integrations
        assert hasattr(integrations, '__all__')

    def test_justasking_adapter_imports(self):
        """Test that justasking_adapter module can be imported."""
        from core.integrations import justasking_adapter
        assert justasking_adapter is not None

    def test_itpu_adapter_imports(self):
        """Test that itpu_adapter module can be imported."""
        from core.integrations import itpu_adapter
        assert itpu_adapter is not None

    def test_gp_adapter_imports(self):
        """Test that gp_adapter (geometric-plasticity) module can be imported."""
        from core.integrations import gp_adapter
        assert gp_adapter is not None


class TestJustaskingAdapter:
    """Test justasking adapter function signatures."""

    def test_fanout_exists(self):
        """Test that fanout function exists."""
        from core.integrations.justasking_adapter import fanout
        assert callable(fanout)

    def test_fanout_signature(self):
        """Test that fanout has expected signature."""
        from core.integrations.justasking_adapter import fanout
        import inspect

        sig = inspect.signature(fanout)
        params = list(sig.parameters.keys())

        assert "prompt_bundle" in params
        assert "models" in params
        assert "temperature_range" in params
        assert "n_variations" in params

    def test_fanout_works_in_simulated_mode(self):
        """Test that fanout works in simulated mode (v1 thin slice)."""
        from core.integrations.justasking_adapter import fanout

        # Should work with simulate=True (default)
        result = fanout(prompt_bundle={"hypothesis": "test"}, n_variations=2)
        assert isinstance(result, list)
        assert len(result) == 2

        # Should raise with simulate=False (not yet wired)
        with pytest.raises(NotImplementedError, match="Real LLM fan-out not yet wired"):
            fanout(prompt_bundle={"hypothesis": "test"}, simulate=False)

    def test_fanout_with_diversity_metrics_exists(self):
        """Test that fanout_with_diversity_metrics function exists."""
        from core.integrations.justasking_adapter import fanout_with_diversity_metrics
        assert callable(fanout_with_diversity_metrics)

    def test_fanout_with_diversity_metrics_works_in_simulated_mode(self):
        """Test that fanout_with_diversity_metrics works (v1 thin slice)."""
        from core.integrations.justasking_adapter import fanout_with_diversity_metrics

        # Should work with simulate=True (default)
        responses, metrics = fanout_with_diversity_metrics(
            prompt_bundle={"hypothesis": "test"}
        )
        assert isinstance(responses, list)
        assert isinstance(metrics, dict)
        assert "diversity_achieved" in metrics


class TestITPUAdapter:
    """Test ITPU adapter function signatures."""

    def test_compute_mutual_info_exists(self):
        """Test that compute_mutual_info function exists."""
        from core.integrations.itpu_adapter import compute_mutual_info
        assert callable(compute_mutual_info)

    def test_compute_mutual_info_signature(self):
        """Test that compute_mutual_info has expected signature."""
        from core.integrations.itpu_adapter import compute_mutual_info
        import inspect

        sig = inspect.signature(compute_mutual_info)
        params = list(sig.parameters.keys())

        assert "x" in params
        assert "y" in params
        assert "method" in params
        assert "k" in params

    def test_compute_mutual_info_raises_not_implemented(self):
        """Test that compute_mutual_info stub raises NotImplementedError."""
        from core.integrations.itpu_adapter import compute_mutual_info

        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])

        with pytest.raises(NotImplementedError, match="ITPU"):
            compute_mutual_info(x, y)

    def test_windowed_mutual_info_exists(self):
        """Test that windowed_mutual_info function exists."""
        from core.integrations.itpu_adapter import windowed_mutual_info
        assert callable(windowed_mutual_info)

    def test_windowed_mutual_info_raises_not_implemented(self):
        """Test that windowed_mutual_info stub raises NotImplementedError."""
        from core.integrations.itpu_adapter import windowed_mutual_info

        series = [np.array([1, 2, 3]), np.array([4, 5, 6])]

        with pytest.raises(NotImplementedError):
            windowed_mutual_info(series)

    def test_compute_transfer_entropy_exists(self):
        """Test that compute_transfer_entropy function exists."""
        from core.integrations.itpu_adapter import compute_transfer_entropy
        assert callable(compute_transfer_entropy)

    def test_compute_transfer_entropy_raises_not_implemented(self):
        """Test that compute_transfer_entropy stub raises NotImplementedError."""
        from core.integrations.itpu_adapter import compute_transfer_entropy

        source = np.array([1, 2, 3, 4, 5])
        target = np.array([2, 3, 4, 5, 6])

        with pytest.raises(NotImplementedError):
            compute_transfer_entropy(source, target)


class TestGPAdapter:
    """Test Geometric-Plasticity adapter function signatures."""

    def test_detect_ringing_exists(self):
        """Test that detect_ringing function exists."""
        from core.integrations.gp_adapter import detect_ringing
        assert callable(detect_ringing)

    def test_detect_ringing_signature(self):
        """Test that detect_ringing has expected signature."""
        from core.integrations.gp_adapter import detect_ringing
        import inspect

        sig = inspect.signature(detect_ringing)
        params = list(sig.parameters.keys())

        assert "series" in params
        assert "psd_threshold_db" in params
        assert "min_overshoots" in params
        assert "window_size" in params

    def test_detect_ringing_raises_not_implemented(self):
        """Test that detect_ringing stub raises NotImplementedError."""
        from core.integrations.gp_adapter import detect_ringing

        series = np.array([1, 2, 1, 2, 1, 2])  # Mock oscillating series

        with pytest.raises(NotImplementedError, match="Geometric-Plasticity"):
            detect_ringing(series)

    def test_compute_curvature_spike_exists(self):
        """Test that compute_curvature_spike function exists."""
        from core.integrations.gp_adapter import compute_curvature_spike
        assert callable(compute_curvature_spike)

    def test_compute_curvature_spike_raises_not_implemented(self):
        """Test that compute_curvature_spike stub raises NotImplementedError."""
        from core.integrations.gp_adapter import compute_curvature_spike

        trajectory = np.array([[0, 0], [1, 1], [2, 0]])  # Mock trajectory

        with pytest.raises(NotImplementedError):
            compute_curvature_spike(trajectory)

    def test_validate_constraint_geometry_exists(self):
        """Test that validate_constraint_geometry function exists."""
        from core.integrations.gp_adapter import validate_constraint_geometry
        assert callable(validate_constraint_geometry)

    def test_validate_constraint_geometry_raises_not_implemented(self):
        """Test that validate_constraint_geometry stub raises NotImplementedError."""
        from core.integrations.gp_adapter import validate_constraint_geometry

        with pytest.raises(NotImplementedError):
            validate_constraint_geometry(
                claim="test claim",
                nulls=["null1", "null2"],
                constraints={}
            )


class TestAdapterDocstrings:
    """Test that adapters have proper documentation."""

    def test_justasking_fanout_has_docstring(self):
        """Test that fanout has a docstring."""
        from core.integrations.justasking_adapter import fanout
        assert fanout.__doc__ is not None
        assert len(fanout.__doc__) > 100

    def test_itpu_compute_mutual_info_has_docstring(self):
        """Test that compute_mutual_info has a docstring."""
        from core.integrations.itpu_adapter import compute_mutual_info
        assert compute_mutual_info.__doc__ is not None
        assert len(compute_mutual_info.__doc__) > 100

    def test_gp_detect_ringing_has_docstring(self):
        """Test that detect_ringing has a docstring."""
        from core.integrations.gp_adapter import detect_ringing
        assert detect_ringing.__doc__ is not None
        assert len(detect_ringing.__doc__) > 100

    def test_justasking_docstring_has_repository_link(self):
        """Test that justasking adapter docstring links to repository."""
        from core.integrations import justasking_adapter
        module_doc = justasking_adapter.__doc__
        assert module_doc is not None
        assert "github.com/justindbilyeu/justasking" in module_doc

    def test_itpu_docstring_has_repository_link(self):
        """Test that ITPU adapter docstring links to repository."""
        from core.integrations import itpu_adapter
        module_doc = itpu_adapter.__doc__
        assert module_doc is not None
        assert "github.com/justindbilyeu/ITPU" in module_doc

    def test_gp_docstring_has_repository_link(self):
        """Test that GP adapter docstring links to repository."""
        from core.integrations import gp_adapter
        module_doc = gp_adapter.__doc__
        assert module_doc is not None
        assert "github.com/justindbilyeu/Resonance_Geometry" in module_doc


class TestNotImplementedMessages:
    """Test that NotImplementedError messages are helpful."""

    def test_fanout_error_message_helpful(self):
        """Test that fanout NotImplementedError message is helpful."""
        from core.integrations.justasking_adapter import fanout

        try:
            fanout(prompt_bundle={"hypothesis": "test"})
        except NotImplementedError as e:
            error_msg = str(e)
            # Should mention repository
            assert "justasking" in error_msg.lower()
            # Should mention docs
            assert "INTEGRATIONS.md" in error_msg or "docs/" in error_msg
            # Should provide instructions
            assert "install" in error_msg.lower() or "enable" in error_msg.lower()

    def test_compute_mutual_info_error_message_helpful(self):
        """Test that compute_mutual_info NotImplementedError message is helpful."""
        from core.integrations.itpu_adapter import compute_mutual_info

        try:
            compute_mutual_info(np.array([1]), np.array([2]))
        except NotImplementedError as e:
            error_msg = str(e)
            assert "ITPU" in error_msg
            assert "INTEGRATIONS.md" in error_msg or "docs/" in error_msg

    def test_detect_ringing_error_message_helpful(self):
        """Test that detect_ringing NotImplementedError message is helpful."""
        from core.integrations.gp_adapter import detect_ringing

        try:
            detect_ringing(np.array([1, 2, 3]))
        except NotImplementedError as e:
            error_msg = str(e)
            assert "Geometric-Plasticity" in error_msg
            assert "INTEGRATIONS.md" in error_msg or "docs/" in error_msg
