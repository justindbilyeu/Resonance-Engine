"""
Experiment Tests: Coin Flip Fairness Test

Validates that the experiment runs correctly and checks that null hypothesis
thresholds can be evaluated against experimental outcomes.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import the experiment
example_dir = Path(__file__).parent.parent
sys.path.insert(0, str(example_dir))

from src.experiment import run_experiment, format_results


class TestExperimentRuns:
    """Test that experiment executes without errors."""

    def test_experiment_imports(self):
        """Test that experiment module can be imported."""
        from src import experiment
        assert hasattr(experiment, "run_experiment")

    def test_run_experiment_executes(self):
        """Test that run_experiment() completes without error."""
        results = run_experiment()
        assert results is not None
        assert isinstance(results, dict)

    def test_run_experiment_with_default_params(self):
        """Test that experiment runs with default preregistered parameters."""
        results = run_experiment()

        # Should return all expected keys
        expected_keys = {
            "n_trials", "n_heads", "n_tails", "proportion_heads",
            "standard_error", "ci_lower_computed", "ci_upper_computed",
            "ci_lower_preregistered", "ci_upper_preregistered",
            "passes_primary_null", "passes_extreme_null", "verdict"
        }
        assert set(results.keys()) == expected_keys

    def test_run_experiment_with_custom_params(self):
        """Test that experiment accepts custom parameters."""
        results = run_experiment(n_trials=100, coin_p=0.5, random_seed=123)

        assert results["n_trials"] == 100
        assert results["n_heads"] + results["n_tails"] == 100


class TestExperimentResults:
    """Test that experiment produces valid results."""

    def test_proportion_in_valid_range(self):
        """Test that proportion is between 0 and 1."""
        results = run_experiment()
        proportion = results["proportion_heads"]

        assert 0.0 <= proportion <= 1.0

    def test_counts_sum_to_trials(self):
        """Test that heads + tails = total trials."""
        results = run_experiment()

        assert results["n_heads"] + results["n_tails"] == results["n_trials"]

    def test_proportion_matches_count(self):
        """Test that proportion equals n_heads / n_trials."""
        results = run_experiment()

        expected_proportion = results["n_heads"] / results["n_trials"]
        actual_proportion = results["proportion_heads"]

        assert abs(expected_proportion - actual_proportion) < 1e-10

    def test_standard_error_positive(self):
        """Test that standard error is positive."""
        results = run_experiment()

        assert results["standard_error"] > 0

    def test_verdict_is_pass_or_fail(self):
        """Test that verdict is either PASS or FAIL."""
        results = run_experiment()

        assert results["verdict"] in ["PASS", "FAIL"]


class TestNullThresholds:
    """Test that null hypothesis thresholds can be evaluated."""

    def test_null_threshold_1_lower_bound(self):
        """Test threshold 1: proportion < 0.45 triggers failure."""
        # This is hard to test with actual randomness, but we can verify
        # the logic works by checking the condition
        results = run_experiment()

        if results["proportion_heads"] < 0.45:
            assert not results["passes_primary_null"]
            assert results["verdict"] == "FAIL"

    def test_null_threshold_2_upper_bound(self):
        """Test threshold 2: proportion > 0.55 triggers failure."""
        results = run_experiment()

        if results["proportion_heads"] > 0.55:
            assert not results["passes_primary_null"]
            assert results["verdict"] == "FAIL"

    def test_null_thresholds_within_bounds(self):
        """Test that result within 0.45-0.55 passes primary null."""
        results = run_experiment()

        if 0.45 <= results["proportion_heads"] <= 0.55:
            assert results["passes_primary_null"]
            assert results["verdict"] == "PASS"

    def test_extreme_null_threshold_3_lower(self):
        """Test threshold 3: proportion < 0.40 (extreme bias)."""
        results = run_experiment()

        if results["proportion_heads"] < 0.40:
            assert not results["passes_extreme_null"]

    def test_extreme_null_threshold_4_upper(self):
        """Test threshold 4: proportion > 0.60 (extreme bias)."""
        results = run_experiment()

        if results["proportion_heads"] > 0.60:
            assert not results["passes_extreme_null"]


class TestDeterministicBehavior:
    """Test that experiment is deterministic with fixed seed."""

    def test_same_seed_same_results(self):
        """Test that same seed produces identical results."""
        results1 = run_experiment(random_seed=42)
        results2 = run_experiment(random_seed=42)

        assert results1["n_heads"] == results2["n_heads"]
        assert results1["proportion_heads"] == results2["proportion_heads"]

    def test_different_seed_different_results(self):
        """Test that different seeds likely produce different results."""
        results1 = run_experiment(random_seed=42)
        results2 = run_experiment(random_seed=123)

        # With high probability, different seeds yield different results
        # (Could be same by chance, but very unlikely)
        assert results1["n_heads"] != results2["n_heads"] or \
               results1["random_seed"] == results2.get("random_seed", None)


class TestPreregisteredParameters:
    """Test that preregistered parameters match PREREG.yaml."""

    def test_default_n_trials_is_1000(self):
        """Test that default n_trials matches PREREG.yaml (1000)."""
        from src.experiment import N_TRIALS
        assert N_TRIALS == 1000

    def test_default_random_seed_is_42(self):
        """Test that default random_seed matches PREREG.yaml (42)."""
        from src.experiment import RANDOM_SEED
        assert RANDOM_SEED == 42

    def test_default_coin_p_is_0_5(self):
        """Test that default coin_p matches PREREG.yaml (0.5)."""
        from src.experiment import COIN_PROBABILITY
        assert COIN_PROBABILITY == 0.5

    def test_ci_bounds_match_prereg(self):
        """Test that CI bounds match PREREG.yaml."""
        from src.experiment import CI_LOWER, CI_UPPER
        assert CI_LOWER == 0.45
        assert CI_UPPER == 0.55


class TestOutputFormatting:
    """Test that results can be formatted for display."""

    def test_format_results_returns_string(self):
        """Test that format_results returns a string."""
        results = run_experiment()
        formatted = format_results(results)

        assert isinstance(formatted, str)
        assert len(formatted) > 0

    def test_format_results_contains_key_info(self):
        """Test that formatted output contains key information."""
        results = run_experiment()
        formatted = format_results(results)

        # Should contain essential information
        assert "COIN FLIP" in formatted
        assert str(results["n_trials"]) in formatted
        assert str(results["n_heads"]) in formatted
        assert results["verdict"] in formatted


class TestReproducibility:
    """Test that experiment satisfies reproducibility requirements."""

    def test_with_seed_42_gets_expected_result(self):
        """Test that seed=42 produces the expected deterministic result.

        This test documents the expected outcome for the golden path example.
        With seed=42, n_trials=1000, p=0.5, we expect a specific result.
        """
        results = run_experiment(random_seed=42, n_trials=1000, coin_p=0.5)

        # Document the deterministic result (this is what we actually get)
        # Note: This is implementation-dependent (numpy's RNG)
        assert results["n_trials"] == 1000
        assert 0.45 <= results["proportion_heads"] <= 0.55  # Should pass

        # The experiment should pass with fair coin and reasonable sample size
        assert results["verdict"] == "PASS"
