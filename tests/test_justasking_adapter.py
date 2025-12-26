"""
Tests for justasking Adapter — Diversity Fan-Out

Validates simulated diversity generation, diversity scoring, and fan-out with
target diversity tracking.
"""

import pytest
from core.integrations.justasking_adapter import (
    fanout,
    compute_diversity_score,
    fanout_with_diversity_metrics,
)


class TestFanoutBasics:
    """Test basic fan-out functionality."""

    def test_fanout_returns_list(self):
        """Test that fanout returns a list of responses."""
        bundle = {"hypothesis": "Test hypothesis"}
        result = fanout(bundle, n_variations=3)

        assert isinstance(result, list)
        assert len(result) == 3

    def test_fanout_response_structure(self):
        """Test that each response has required fields."""
        bundle = {"hypothesis": "Test hypothesis"}
        result = fanout(bundle, n_variations=2)

        required_fields = {"response", "model", "temperature", "timestamp", "metadata"}
        for response in result:
            assert isinstance(response, dict)
            assert required_fields.issubset(response.keys())

    def test_fanout_with_custom_models(self):
        """Test that fanout uses specified models."""
        bundle = {"hypothesis": "Test hypothesis"}
        models = ["model-a", "model-b"]
        result = fanout(bundle, models=models, n_variations=4)

        models_used = [r["model"] for r in result]
        # Should cycle through provided models
        assert all(m in models for m in models_used)

    def test_fanout_temperature_range(self):
        """Test that temperatures are within specified range."""
        bundle = {"hypothesis": "Test hypothesis"}
        temp_range = (0.5, 1.0)
        result = fanout(bundle, temperature_range=temp_range, n_variations=5)

        temperatures = [r["temperature"] for r in result]
        assert all(temp_range[0] <= t <= temp_range[1] for t in temperatures)

    def test_fanout_deterministic_with_same_input(self):
        """Test that same input produces same output (deterministic)."""
        bundle = {"hypothesis": "Test hypothesis"}

        result1 = fanout(bundle, n_variations=3)
        result2 = fanout(bundle, n_variations=3)

        # Seeds should match for same inputs
        seeds1 = [r["metadata"]["seed"] for r in result1]
        seeds2 = [r["metadata"]["seed"] for r in result2]
        assert seeds1 == seeds2


class TestFanoutValidation:
    """Test input validation for fanout."""

    def test_fanout_requires_dict(self):
        """Test that fanout requires prompt_bundle to be a dict."""
        with pytest.raises(ValueError, match="must be a dictionary"):
            fanout("not a dict")

    def test_fanout_requires_hypothesis_key(self):
        """Test that fanout requires 'hypothesis' key in bundle."""
        with pytest.raises(ValueError, match="must contain 'hypothesis'"):
            fanout({})

    def test_fanout_with_empty_hypothesis(self):
        """Test that fanout works with empty hypothesis string."""
        # This should not raise (empty string is valid, just not useful)
        bundle = {"hypothesis": ""}
        result = fanout(bundle, n_variations=1)
        assert len(result) == 1


class TestDiversityScoring:
    """Test diversity score computation."""

    def test_diversity_score_empty_responses(self):
        """Test that empty response list yields 0 diversity."""
        score = compute_diversity_score([])
        assert score == 0.0

    def test_diversity_score_single_response(self):
        """Test diversity with single response."""
        responses = [
            {
                "response": "Test response",
                "model": "gpt-4",
                "temperature": 0.7,
            }
        ]
        score = compute_diversity_score(responses)

        # Single response should have low diversity
        assert 0.0 <= score <= 1.0

    def test_diversity_score_identical_responses(self):
        """Test that identical responses yield low diversity."""
        responses = [
            {
                "response": "Same response",
                "model": "gpt-4",
                "temperature": 0.7,
            },
            {
                "response": "Same response",
                "model": "gpt-4",
                "temperature": 0.7,
            },
        ]
        score = compute_diversity_score(responses)

        # Identical responses should have low diversity
        assert score < 0.5

    def test_diversity_score_diverse_responses(self):
        """Test that diverse responses yield high diversity."""
        responses = [
            {
                "response": "Response A",
                "model": "gpt-4",
                "temperature": 0.7,
            },
            {
                "response": "Response B",
                "model": "claude-3",
                "temperature": 0.9,
            },
            {
                "response": "Response C",
                "model": "llama-70b",
                "temperature": 1.1,
            },
        ]
        score = compute_diversity_score(responses)

        # Diverse responses should have high diversity
        assert score > 0.5

    def test_diversity_score_in_valid_range(self):
        """Test that diversity score is always in [0, 1]."""
        bundle = {"hypothesis": "Test hypothesis"}
        result = fanout(bundle, n_variations=10)

        score = compute_diversity_score(result)
        assert 0.0 <= score <= 1.0


class TestFanoutWithMetrics:
    """Test fan-out with diversity tracking."""

    def test_fanout_with_metrics_returns_tuple(self):
        """Test that fanout_with_diversity_metrics returns (responses, metrics)."""
        bundle = {"hypothesis": "Test hypothesis"}
        responses, metrics = fanout_with_diversity_metrics(bundle)

        assert isinstance(responses, list)
        assert isinstance(metrics, dict)

    def test_fanout_with_metrics_structure(self):
        """Test that metrics dict has required fields."""
        bundle = {"hypothesis": "Test hypothesis"}
        _, metrics = fanout_with_diversity_metrics(bundle)

        required_fields = {
            "diversity_achieved",
            "iterations",
            "model_distribution",
            "total_responses",
            "target_diversity",
        }
        assert required_fields.issubset(metrics.keys())

    def test_fanout_with_metrics_achieves_target(self):
        """Test that fan-out reaches target diversity."""
        bundle = {"hypothesis": "Test hypothesis"}
        target = 0.6

        responses, metrics = fanout_with_diversity_metrics(
            bundle, target_diversity=target, max_iterations=5
        )

        # Should achieve or get close to target
        assert metrics["diversity_achieved"] >= target - 0.1

    def test_fanout_with_metrics_respects_max_iterations(self):
        """Test that fan-out doesn't exceed max_iterations."""
        bundle = {"hypothesis": "Test hypothesis"}

        _, metrics = fanout_with_diversity_metrics(
            bundle, target_diversity=0.99, max_iterations=3
        )

        assert metrics["iterations"] <= 3

    def test_fanout_with_metrics_model_distribution(self):
        """Test that model_distribution counts models correctly."""
        bundle = {"hypothesis": "Test hypothesis"}

        responses, metrics = fanout_with_diversity_metrics(bundle)

        # Sum of model counts should equal total responses
        total_from_dist = sum(metrics["model_distribution"].values())
        assert total_from_dist == metrics["total_responses"]
        assert total_from_dist == len(responses)


class TestSimulatedResponses:
    """Test simulated response generation."""

    def test_simulated_responses_have_metadata_flag(self):
        """Test that simulated responses are marked as such."""
        bundle = {"hypothesis": "Test hypothesis"}
        result = fanout(bundle, simulate=True, n_variations=2)

        for response in result:
            assert "metadata" in response
            assert response["metadata"]["simulated"] is True

    def test_simulated_responses_use_different_framings(self):
        """Test that simulated responses use diverse framings."""
        bundle = {"hypothesis": "Coin flips are fair"}
        result = fanout(bundle, n_variations=5)

        # Should have different framings
        framings = [r["response"] for r in result]
        unique_framings = set(framings)

        # Should have multiple unique framings (5 variations, 5 framings)
        assert len(unique_framings) >= 3

    def test_simulate_false_raises_not_implemented(self):
        """Test that simulate=False raises NotImplementedError."""
        bundle = {"hypothesis": "Test hypothesis"}

        with pytest.raises(NotImplementedError, match="Real LLM fan-out not yet wired"):
            fanout(bundle, simulate=False)


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    def test_diversity_score_reflects_framing_uniqueness(self):
        """Test that diversity score reflects uniqueness of framings."""
        bundle = {"hypothesis": "Model size predicts performance"}

        # With 5 variations, we get 5 unique framings (our template has 5 framings)
        result_5 = fanout(bundle, n_variations=5)
        diversity_5 = compute_diversity_score(result_5)

        # With 10 variations, framings repeat, so diversity should be lower
        result_10 = fanout(bundle, n_variations=10)
        diversity_10 = compute_diversity_score(result_10)

        # 5 variations should have higher diversity than 10 (less repetition)
        assert diversity_5 >= diversity_10

        # Both should be in valid range
        assert 0.0 <= diversity_5 <= 1.0
        assert 0.0 <= diversity_10 <= 1.0

    def test_fanout_workflow_for_discovery_compiler(self):
        """Test complete workflow for discovery compiler integration."""
        # 1. Create hypothesis bundle
        bundle = {
            "hypothesis": "Interaction topology induces emergent capabilities",
            "context": "From RG-AISysTheory",
        }

        # 2. Fan out for diversity
        responses, metrics = fanout_with_diversity_metrics(
            bundle, target_diversity=0.7
        )

        # 3. Verify diversity achieved
        assert metrics["diversity_achieved"] >= 0.6

        # 4. Verify multiple models used
        assert len(metrics["model_distribution"]) >= 2

        # 5. Verify responses can be used for dissent analysis
        assert len(responses) >= 5
        for r in responses:
            assert "response" in r
            assert "model" in r
