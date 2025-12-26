"""
Dissent Metrics

Measures Builder/Skeptic disagreement levels. Detects premature convergence
(agreement rising too quickly) and degenerate oscillations (persistent disagreement
without constraint health improvement).
"""


def measure_dissent(builder_output: str, skeptic_output: str) -> float:
    """
    Measure degree of disagreement between Builder and Skeptic outputs.

    Args:
        builder_output: Builder's hypothesis or protocol
        skeptic_output: Skeptic's critique and failure modes

    Returns:
        Dissent score (0.0 = full agreement, 1.0 = maximum disagreement)

    Raises:
        NotImplementedError: This is a stub for PR-0
    """
    raise NotImplementedError("Dissent measurement coming in future PR")


def detect_premature_convergence(dissent_history: list) -> bool:
    """
    Detect if Builder and Skeptic are agreeing too quickly.

    Args:
        dissent_history: List of dissent scores across stages

    Returns:
        True if converging prematurely, False otherwise

    Raises:
        NotImplementedError: This is a stub for PR-0
    """
    raise NotImplementedError("Premature convergence detection coming in future PR")
