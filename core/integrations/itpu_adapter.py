"""
ITPU Adapter — Metrics Provider (Mutual Information / Windowed MI)

Clean interface to the ITPU repository for information-theoretic metrics on
experimental data and constraint health tracking.

Repository: https://github.com/justindbilyeu/ITPU
Purpose: Measure dependencies, correlations, and information flow
Status: v0 stub (NotImplementedError)

Usage in Resonance Engine:
- Constraint health metrics: MI between claim and null hypotheses
- Convergence detection: Windowed MI across compilation stages
- Dissent quantification: MI between Builder and Skeptic outputs (low MI = high dissent)
"""

from typing import Optional
import numpy as np


def compute_mutual_info(
    x: np.ndarray,
    y: np.ndarray,
    method: str = "ksg",
    k: int = 3,
) -> float:
    """
    Compute mutual information between two variables.

    Uses information-theoretic estimators to measure the amount of information
    shared between two random variables.

    Args:
        x: First variable (n_samples,) or (n_samples, n_features)
        y: Second variable (n_samples,) or (n_samples, n_features)
        method: Estimator method:
            - "ksg": Kraskov-Stögbauer-Grassberger (default, robust)
            - "histogram": Histogram-based (fast, less accurate)
            - "kernel": Kernel density (smooth, slower)
        k: Number of nearest neighbors for KSG estimator

    Returns:
        Mutual information in nats (natural units)
        Higher values = more shared information
        0 = independent variables

    Raises:
        NotImplementedError: This is a v0 stub. Wire ITPU in post-v0.
        ValueError: If x and y have incompatible shapes

    Example:
        >>> # Measure Builder/Skeptic dissent
        >>> builder_emb = embed_text(builder_output)
        >>> skeptic_emb = embed_text(skeptic_output)
        >>> mi = compute_mutual_info(builder_emb, skeptic_emb)
        >>> dissent_score = 1.0 - (mi / max_possible_mi)
        >>>
        >>> if dissent_score < 0.3:
        >>>     # Low dissent! Diversify using justasking
        >>>     variations = fanout(prompt_bundle, n_variations=5)

    Integration:
        To wire this adapter:
        1. Install ITPU: pip install itpu
        2. Import actual implementation
        3. Replace NotImplementedError with real call
        4. Handle edge cases (empty arrays, etc.)

        See docs/INTEGRATIONS.md for roadmap.
    """
    raise NotImplementedError(
        "ITPU integration not yet wired.\n"
        "\n"
        "This adapter provides information-theoretic metrics for measuring\n"
        "dependencies and correlations in experimental data.\n"
        "\n"
        "To enable (post-v0):\n"
        "  1. Install ITPU: pip install itpu\n"
        "  2. Wire adapter implementation\n"
        "  3. Verify license compatibility\n"
        "\n"
        "Repository: https://github.com/justindbilyeu/ITPU\n"
        "See: docs/INTEGRATIONS.md for integration strategy"
    )


def windowed_mutual_info(
    series: list[np.ndarray],
    window_size: int = 3,
    stride: int = 1,
    method: str = "ksg",
) -> np.ndarray:
    """
    Compute windowed MI across a time series of distributions.

    Useful for tracking convergence over compilation stages or detecting
    when constraint health stops improving.

    Args:
        series: List of arrays, one per time step
        window_size: Size of sliding window
        stride: Step size for sliding window
        method: MI estimation method (see compute_mutual_info)

    Returns:
        Array of windowed MI values, shape (n_windows,)

    Raises:
        NotImplementedError: This is a v0 stub

    Example:
        >>> # Track constraint health improvement across stages
        >>> stage_embeddings = [embed_stage(s) for s in compilation_stages]
        >>> windowed_mi = windowed_mutual_info(
        ...     series=stage_embeddings,
        ...     window_size=3
        ... )
        >>>
        >>> # Detect convergence
        >>> if np.std(windowed_mi[-5:]) < 0.01:
        ...     print("Constraint health has converged")
        ...     controller.decision = "converge"
    """
    raise NotImplementedError(
        "ITPU integration not yet wired. See docs/INTEGRATIONS.md"
    )


def compute_transfer_entropy(
    source: np.ndarray,
    target: np.ndarray,
    lag: int = 1,
    k: int = 3,
) -> float:
    """
    Compute transfer entropy from source to target.

    Measures directed information flow (how much knowing source's past
    helps predict target's future).

    Args:
        source: Source time series (n_samples,)
        target: Target time series (n_samples,)
        lag: Time lag for prediction
        k: Number of nearest neighbors

    Returns:
        Transfer entropy in nats
        Higher values = stronger directional influence

    Raises:
        NotImplementedError: This is a v0 stub

    Example:
        >>> # Measure if Builder influences Skeptic more than vice versa
        >>> builder_series = [embed(b) for b in builder_outputs]
        >>> skeptic_series = [embed(s) for s in skeptic_outputs]
        >>>
        >>> te_b_to_s = compute_transfer_entropy(builder_series, skeptic_series)
        >>> te_s_to_b = compute_transfer_entropy(skeptic_series, builder_series)
        >>>
        >>> if te_b_to_s > 2 * te_s_to_b:
        ...     print("Skeptic is too passive! Increase dissent weight.")
    """
    raise NotImplementedError(
        "ITPU integration not yet wired. See docs/INTEGRATIONS.md"
    )
