"""
Null Completeness Gate

Enforces the first hard constraint: no experiment bundle without numeric falsifiers.
Rejects any preregistration with fewer than the minimum number of specific numeric
thresholds that would invalidate the hypothesis.

This is a mechanical gate, not a "smart" one—it counts explicit numeric patterns
and does not attempt semantic analysis.
"""

import re
from typing import List, Tuple


def count_numeric_thresholds(text: str) -> int:
    """
    Count numeric threshold expressions in text.

    Counts thresholds expressed in the following formats:
    - Comparator + number: >= 2, < 0.1, <= 10.0, > 5, == 0, != 1
    - Multiplier forms: 1.5x, 2x, 10.2x
    - Percentage forms: 10%, 0.5%, 95.5%

    Pattern limitations:
    - Does not handle complex mathematical expressions
    - Does not validate semantic correctness
    - May count non-threshold numbers in some edge cases
    - Focuses on explicit, simple threshold patterns

    Args:
        text: Text to search for numeric thresholds

    Returns:
        Count of numeric threshold expressions found

    Examples:
        >>> count_numeric_thresholds("Reject if accuracy < 0.55")
        1
        >>> count_numeric_thresholds("Reject if delta >= 0.10 or variance > 2x baseline")
        2
        >>> count_numeric_thresholds("Results should be good")
        0
    """
    if not text:
        return 0

    # Pattern 1: Comparator + number (>=, <=, <, >, ==, !=)
    # Matches: >= 2, < 0.1, <= 10.0, > 5, == 0, != 1
    # Use negative lookahead to exclude numbers followed by 'x' or '%'
    comparator_pattern = r'(?:>=|<=|<|>|==|!=)\s*\d+(?:\.\d+)?(?![x%])'

    # Pattern 2: Multiplier forms (1.5x, 2x, 10.2x)
    # Matches: 1.5x, 2x, 0.5x
    multiplier_pattern = r'\d+(?:\.\d+)?x\b'

    # Pattern 3: Percentage forms (10%, 0.5%, 95.5%)
    # Matches: 10%, 0.5%, 95.5%
    percentage_pattern = r'\d+(?:\.\d+)?%'

    # Collect all matches with their ranges
    all_matches = []

    patterns = [
        (comparator_pattern, 'comparator'),
        (multiplier_pattern, 'multiplier'),
        (percentage_pattern, 'percentage'),
    ]

    for pattern, pattern_type in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            all_matches.append((match.start(), match.end(), pattern_type))

    # Deduplicate overlapping matches by keeping only non-overlapping ones
    # Sort by start position
    all_matches.sort(key=lambda x: x[0])

    # Filter to remove overlaps - keep longer/earlier matches
    unique_matches = []
    for start, end, ptype in all_matches:
        # Check if this match overlaps with any already accepted match
        overlaps = False
        for u_start, u_end, _ in unique_matches:
            # Check for overlap: ranges overlap if one starts before the other ends
            if not (end <= u_start or start >= u_end):
                overlaps = True
                break

        if not overlaps:
            unique_matches.append((start, end, ptype))

    return len(unique_matches)


def assert_numeric_nulls(text: str, min_thresholds: int = 2) -> None:
    """
    Assert that text contains at least the minimum number of numeric thresholds.

    This is the enforcement function for the null completeness gate. Use this to
    validate that null hypotheses or rejection criteria contain sufficient numeric
    specificity to be falsifiable.

    Args:
        text: Text to validate (typically NULLS.md content)
        min_thresholds: Minimum number of numeric thresholds required (default: 2)

    Raises:
        ValueError: If fewer than min_thresholds numeric thresholds are found

    Examples:
        >>> assert_numeric_nulls("Reject if accuracy < 0.55 and delta >= 0.10")  # OK
        >>> assert_numeric_nulls("Reject if results are inconsistent")  # Raises
        Traceback (most recent call last):
        ...
        ValueError: Null completeness gate failure: Found 0 numeric thresholds, need at least 2.
        ...
    """
    count = count_numeric_thresholds(text)

    if count < min_thresholds:
        raise ValueError(
            f"Null completeness gate failure: Found {count} numeric threshold(s), "
            f"need at least {min_thresholds}.\n\n"
            f"Numeric thresholds must be explicit and measurable. Examples:\n"
            f"  ✓ 'Reject if accuracy < 0.55'\n"
            f"  ✓ 'Reject if speedup <= 1.5x baseline'\n"
            f"  ✓ 'Reject if error rate > 10%'\n"
            f"  ✗ 'Reject if results are inconsistent'\n"
            f"  ✗ 'Reject if performance does not improve'\n\n"
            f"Add {min_thresholds - count} more numeric threshold(s) to your null hypotheses."
        )


def find_numeric_thresholds(text: str) -> List[Tuple[str, int, int]]:
    """
    Find and return all numeric thresholds with their positions in text.

    Utility function for debugging or detailed analysis of threshold detection.

    Args:
        text: Text to search for numeric thresholds

    Returns:
        List of tuples (matched_text, start_position, end_position)

    Examples:
        >>> find_numeric_thresholds("Reject if x < 0.5 or y >= 2")
        [('< 0.5', 13, 18), ('>= 2', 24, 28)]
    """
    if not text:
        return []

    patterns = [
        (r'(?:>=|<=|<|>|==|!=)\s*\d+(?:\.\d+)?', 'comparator'),
        (r'\d+(?:\.\d+)?x\b', 'multiplier'),
        (r'\d+(?:\.\d+)?%', 'percentage'),
    ]

    results = []
    for pattern, pattern_type in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            results.append((match.group(), match.start(), match.end()))

    # Sort by position
    results.sort(key=lambda x: x[1])

    return results
