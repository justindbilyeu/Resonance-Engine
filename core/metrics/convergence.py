"""
Convergence Metrics

Tracks stage-to-stage improvement in constraint health and protocol clarity.
Detects when the discovery process is making productive progress vs stalling.
"""


def measure_stage_improvement(current_metrics: dict, previous_metrics: dict) -> float:
    """
    Measure improvement in constraint health from one stage to the next.

    Args:
        current_metrics: Current stage constraint health metrics
        previous_metrics: Previous stage constraint health metrics

    Returns:
        Improvement score (negative if regression, positive if improvement)

    Raises:
        NotImplementedError: This is a stub for PR-0
    """
    raise NotImplementedError("Stage improvement measurement coming in future PR")


def detect_convergence(metrics_history: list) -> bool:
    """
    Detect if the discovery process is converging toward a valid protocol.

    Args:
        metrics_history: List of metrics from all stages

    Returns:
        True if converging, False if diverging or stalling

    Raises:
        NotImplementedError: This is a stub for PR-0
    """
    raise NotImplementedError("Convergence detection coming in future PR")
