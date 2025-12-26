"""
Tests for Null Completeness Gate

Validates that the gate correctly identifies numeric thresholds and enforces
the minimum threshold requirement for falsifiability.
"""

import pytest
from core.metrics.null_gate import (
    count_numeric_thresholds,
    assert_numeric_nulls,
    find_numeric_thresholds,
)


class TestCountNumericThresholds:
    """Test threshold counting across different formats."""

    def test_comparator_thresholds(self):
        """Test detection of comparator-based thresholds."""
        text = "Reject if accuracy < 0.55 and precision >= 0.60"
        assert count_numeric_thresholds(text) == 2

    def test_single_comparator(self):
        """Test single comparator threshold."""
        assert count_numeric_thresholds("performance > 100") == 1

    def test_multiplier_thresholds(self):
        """Test detection of multiplier-based thresholds."""
        text = "Reject if speedup <= 1.5x baseline or overhead > 2x"
        assert count_numeric_thresholds(text) == 2

    def test_percentage_thresholds(self):
        """Test detection of percentage-based thresholds."""
        text = "Reject if error rate > 10% or improvement < 5%"
        assert count_numeric_thresholds(text) == 2

    def test_mixed_threshold_formats(self):
        """Test mixed threshold formats in single text."""
        text = """
        Reject if:
        - Accuracy < 0.55
        - Speedup <= 1.5x baseline
        - Error rate > 10%
        """
        assert count_numeric_thresholds(text) == 3

    def test_no_thresholds(self):
        """Test text with no numeric thresholds."""
        text = "Reject if results are inconsistent or unclear"
        assert count_numeric_thresholds(text) == 0

    def test_empty_text(self):
        """Test empty string."""
        assert count_numeric_thresholds("") == 0

    def test_complex_realistic_example(self):
        """Test realistic null hypothesis document."""
        text = """
        # Null Hypotheses

        We will reject the hypothesis if:

        1. **Accuracy threshold**: Classification accuracy < 0.55 (barely above random)
        2. **Delta threshold**: Improvement over baseline <= 5%
        3. **Convergence**: Training loss >= 0.1 (fails to converge)
        4. **Stability**: Variance across runs > 2x mean performance

        Any single failure criterion triggers rejection.
        """
        # Should find 4 unique thresholds (overlapping patterns deduplicated)
        assert count_numeric_thresholds(text) == 4

    def test_all_comparator_types(self):
        """Test all comparator types are detected."""
        text = "a >= 1, b <= 2, c < 3, d > 4, e == 5, f != 6"
        assert count_numeric_thresholds(text) == 6

    def test_decimal_numbers(self):
        """Test thresholds with decimal numbers."""
        text = "x < 0.001 and y >= 99.99"
        assert count_numeric_thresholds(text) == 2

    def test_integer_numbers(self):
        """Test thresholds with integer numbers."""
        text = "count > 100 and iterations <= 1000"
        assert count_numeric_thresholds(text) == 2


class TestAssertNumericNulls:
    """Test null completeness gate enforcement."""

    def test_passes_with_sufficient_thresholds(self):
        """Test that assertion passes with 2+ thresholds."""
        text = "Reject if accuracy < 0.55 and delta >= 0.10"
        # Should not raise
        assert_numeric_nulls(text, min_thresholds=2)

    def test_passes_with_more_than_minimum(self):
        """Test that assertion passes with more than minimum thresholds."""
        text = "Reject if a < 1, b > 2, c >= 3, d <= 4"
        # Should not raise
        assert_numeric_nulls(text, min_thresholds=2)

    def test_fails_with_no_thresholds(self):
        """Test that assertion fails with vague nulls."""
        text = "Reject if results are inconsistent or performance degrades"
        with pytest.raises(ValueError, match="Null completeness gate failure"):
            assert_numeric_nulls(text, min_thresholds=2)

    def test_fails_with_one_threshold_when_two_required(self):
        """Test that assertion fails with only 1 threshold when 2 required."""
        text = "Reject if accuracy < 0.55"
        with pytest.raises(ValueError, match="Found 1 numeric threshold"):
            assert_numeric_nulls(text, min_thresholds=2)

    def test_error_message_is_helpful(self):
        """Test that error message provides actionable guidance."""
        text = "Reject if performance is bad"
        with pytest.raises(ValueError) as exc_info:
            assert_numeric_nulls(text, min_thresholds=2)

        error_msg = str(exc_info.value)
        # Check that error message contains helpful examples
        assert "✓" in error_msg  # Has positive examples
        assert "✗" in error_msg  # Has negative examples
        assert "accuracy < 0.55" in error_msg  # Shows concrete example

    def test_custom_minimum_threshold(self):
        """Test custom minimum threshold value."""
        text = "Reject if x < 1, y > 2, z >= 3"
        # Should pass with min=3
        assert_numeric_nulls(text, min_thresholds=3)
        # Should fail with min=4
        with pytest.raises(ValueError):
            assert_numeric_nulls(text, min_thresholds=4)

    def test_realistic_pass_case(self):
        """Test realistic passing null hypothesis."""
        text = """
        # Null Hypotheses and Rejection Criteria

        We will reject the hypothesis if ANY of the following conditions are met:

        ## Primary Metrics
        1. **Accuracy**: Model accuracy on test set < 0.55 (barely above random chance for binary classification)
        2. **Precision**: Precision score < 0.50

        ## Secondary Metrics
        3. **Improvement**: Performance improvement over baseline <= 5%
        4. **Stability**: Standard deviation across 5 runs > 10% of mean performance

        Preregistered thresholds are intentionally conservative to avoid p-hacking.
        """
        # Should not raise - has 4 numeric thresholds
        assert_numeric_nulls(text, min_thresholds=2)

    def test_realistic_fail_case(self):
        """Test realistic failing null hypothesis (vague)."""
        text = """
        # Null Hypotheses

        We will reject the hypothesis if:
        - The model does not perform significantly better than baseline
        - Results are not reproducible across multiple runs
        - The improvement is marginal or negligible
        """
        # Should raise - no numeric thresholds
        with pytest.raises(ValueError, match="Found 0 numeric threshold"):
            assert_numeric_nulls(text, min_thresholds=2)


class TestFindNumericThresholds:
    """Test threshold finding and position tracking."""

    def test_returns_matches_with_positions(self):
        """Test that function returns matches with positions."""
        text = "Reject if x < 0.5 or y >= 2"
        results = find_numeric_thresholds(text)

        assert len(results) == 2
        # Each result should be a tuple (match, start, end)
        assert all(len(r) == 3 for r in results)
        assert all(isinstance(r[1], int) and isinstance(r[2], int) for r in results)

    def test_sorted_by_position(self):
        """Test that results are sorted by position."""
        text = "b >= 2 and a < 1"
        results = find_numeric_thresholds(text)

        # Should be sorted by position, so ">= 2" comes before "< 1"
        assert results[0][1] < results[1][1]

    def test_empty_text_returns_empty_list(self):
        """Test empty text returns empty list."""
        assert find_numeric_thresholds("") == []

    def test_no_matches_returns_empty_list(self):
        """Test text with no matches returns empty list."""
        assert find_numeric_thresholds("no thresholds here") == []


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_whitespace_variations(self):
        """Test various whitespace patterns around operators."""
        # With spaces
        assert count_numeric_thresholds("x >= 1") == 1
        # Without spaces
        assert count_numeric_thresholds("x>=1") == 1
        # Multiple spaces
        assert count_numeric_thresholds("x >=  1") == 1

    def test_case_insensitivity(self):
        """Test that patterns work regardless of case."""
        # Multiplier with different cases
        assert count_numeric_thresholds("2X baseline") == 1
        assert count_numeric_thresholds("2x baseline") == 1

    def test_multiple_thresholds_same_line(self):
        """Test multiple thresholds on same line."""
        text = "Reject if a < 1 and b > 2 or c >= 3"
        assert count_numeric_thresholds(text) == 3

    def test_thresholds_in_different_formats_same_text(self):
        """Test all three format types in same text."""
        text = "Reject if accuracy < 0.5, speedup <= 1.5x, and error > 10%"
        assert count_numeric_thresholds(text) == 3

    def test_zero_as_threshold(self):
        """Test that zero is counted as valid threshold."""
        text = "Reject if value <= 0 or count == 0"
        assert count_numeric_thresholds(text) == 2

    def test_very_small_numbers(self):
        """Test very small decimal numbers."""
        text = "Reject if p-value >= 0.05 or epsilon < 0.0001"
        assert count_numeric_thresholds(text) == 2

    def test_very_large_numbers(self):
        """Test large numbers."""
        text = "Reject if iterations > 10000 or memory >= 1000000"
        assert count_numeric_thresholds(text) == 2
