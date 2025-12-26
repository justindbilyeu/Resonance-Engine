"""
justasking Adapter — Diversity Actuator (Fan-Out)

Clean interface to the justasking repository for generating diverse perspectives
on research questions by fanning out prompts across multiple models/temperatures.

Repository: https://github.com/justindbilyeu/justasking
Purpose: Diversity actuation for preventing premature convergence
Status: v1 thin slice (simulated fan-out for demonstration)

Usage in Resonance Engine:
- When Coherence Controller decides to "diversify," justasking fans out the
  current hypothesis to multiple LLMs to generate architectural diversity
- If Builder/Skeptic agree too quickly (low dissent), inject alternate framings
- Produces competing interpretations for Skeptic to identify failure modes

v1 Implementation:
- Simulated fan-out with synthetic diversity (no actual LLM calls)
- Demonstrates structure for real integration
- Feature flag: --enable-diversity-fanout
"""

import datetime
import hashlib
from typing import Optional


def fanout(
    prompt_bundle: dict,
    models: Optional[list[str]] = None,
    temperature_range: tuple[float, float] = (0.7, 1.2),
    n_variations: int = 5,
    simulate: bool = True,
) -> list[dict]:
    """
    Fan out a prompt to multiple models/temperatures for diversity.

    Generates diverse responses by varying:
    - Model (GPT-4, Claude, Llama, etc.)
    - Temperature (sampling randomness)
    - System prompt framing

    Args:
        prompt_bundle: Dictionary with keys:
            - "hypothesis": Current claim or hypothesis
            - "context": Optional context (OPERATIONALIZE.md, etc.)
            - "constraints": Optional constraint specifications
        models: List of model identifiers (default: ["gpt-4", "claude-3"])
        temperature_range: (min, max) temperature for sampling
        n_variations: Number of diverse responses to generate
        simulate: If True (default), generate synthetic responses for demo

    Returns:
        List of response dictionaries, each containing:
            - "response": Generated text
            - "model": Model used
            - "temperature": Temperature used
            - "timestamp": Generation timestamp
            - "metadata": Additional model-specific metadata

    Raises:
        ValueError: If prompt_bundle is invalid

    Example:
        >>> variations = fanout(
        ...     prompt_bundle={
        ...         "hypothesis": "Model size predicts recovery time",
        ...         "context": operationalize_doc
        ...     },
        ...     models=["gpt-4", "claude-3", "llama-70b"],
        ...     n_variations=5
        ... )
        >>> # Feed variations to Skeptic for adversarial critique
        >>> for var in variations:
        ...     skeptic.critique(var["response"])

    v1 Note:
        Currently uses simulated responses to demonstrate structure.
        Set simulate=False for real LLM calls (requires justasking installed).
    """
    # Validate input
    if not isinstance(prompt_bundle, dict):
        raise ValueError("prompt_bundle must be a dictionary")
    if "hypothesis" not in prompt_bundle:
        raise ValueError("prompt_bundle must contain 'hypothesis' key")

    # Default models
    if models is None:
        models = ["gpt-4", "claude-3", "llama-70b"]

    # For v1 thin slice: generate simulated diverse responses
    if simulate:
        return _simulate_fanout(
            prompt_bundle, models, temperature_range, n_variations
        )
    else:
        raise NotImplementedError(
            "Real LLM fan-out not yet wired. Install justasking and wire adapter.\n"
            "For now, use simulate=True to demo structure."
        )


def _simulate_fanout(
    prompt_bundle: dict,
    models: list[str],
    temperature_range: tuple[float, float],
    n_variations: int,
) -> list[dict]:
    """
    Generate simulated diverse responses for demonstration.

    This creates synthetic variations by:
    - Using different models
    - Varying temperature
    - Creating deterministic but diverse response stubs

    Real implementation would call actual LLMs via justasking.
    """
    hypothesis = prompt_bundle["hypothesis"]
    responses = []

    # Generate variations with different framings
    framings = [
        f"Quantitative framing: {hypothesis}",
        f"Qualitative framing: {hypothesis}",
        f"Mechanistic framing: {hypothesis}",
        f"Phenomenological framing: {hypothesis}",
        f"Comparative framing: {hypothesis}",
    ]

    for i in range(n_variations):
        model = models[i % len(models)]
        temp_min, temp_max = temperature_range
        temperature = temp_min + (temp_max - temp_min) * (i / max(1, n_variations - 1))

        # Create deterministic but unique response
        seed = hashlib.md5(
            f"{hypothesis}_{model}_{temperature}_{i}".encode()
        ).hexdigest()[:8]

        response = {
            "response": framings[i % len(framings)],
            "model": model,
            "temperature": round(temperature, 2),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "metadata": {
                "simulated": True,
                "seed": seed,
                "framing_index": i % len(framings),
            },
        }
        responses.append(response)

    return responses


def compute_diversity_score(responses: list[dict]) -> float:
    """
    Compute diversity score from a set of responses.

    Measures diversity by:
    - Model distribution entropy
    - Response text uniqueness
    - Temperature spread

    Args:
        responses: List of response dictionaries from fanout()

    Returns:
        Diversity score in [0, 1], where higher = more diverse

    Example:
        >>> variations = fanout(...)
        >>> diversity = compute_diversity_score(variations)
        >>> print(f"Diversity: {diversity:.2f}")
    """
    if not responses:
        return 0.0

    # Count unique models
    models_used = set(r["model"] for r in responses)
    model_diversity = len(models_used) / max(1, len(responses))

    # Count unique responses (by text content)
    unique_responses = set(r["response"] for r in responses)
    text_diversity = len(unique_responses) / max(1, len(responses))

    # Temperature spread (normalized to [0, 1])
    temperatures = [r["temperature"] for r in responses]
    if len(temperatures) > 1:
        temp_range = max(temperatures) - min(temperatures)
        temp_diversity = min(1.0, temp_range / 1.0)  # Normalize by typical range
    else:
        temp_diversity = 0.0

    # Weighted average
    diversity = 0.4 * model_diversity + 0.4 * text_diversity + 0.2 * temp_diversity

    return round(diversity, 3)


def fanout_with_diversity_metrics(
    prompt_bundle: dict,
    models: Optional[list[str]] = None,
    target_diversity: float = 0.7,
    max_iterations: int = 10,
    simulate: bool = True,
) -> tuple[list[dict], dict]:
    """
    Fan out with diversity tracking, stopping when target diversity reached.

    Args:
        prompt_bundle: Prompt specification
        models: List of models to use
        target_diversity: Target diversity score (0-1)
        max_iterations: Maximum fan-out attempts
        simulate: If True, use simulated responses

    Returns:
        (responses, metrics) where metrics includes:
            - "diversity_achieved": Final diversity score
            - "iterations": Number of fan-out rounds
            - "model_distribution": Distribution of models used

    Example:
        >>> responses, metrics = fanout_with_diversity_metrics(
        ...     prompt_bundle={"hypothesis": "..."},
        ...     target_diversity=0.7
        ... )
        >>> print(f"Achieved diversity: {metrics['diversity_achieved']}")
    """
    all_responses = []
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Generate variations
        batch = fanout(
            prompt_bundle, models=models, n_variations=5, simulate=simulate
        )
        all_responses.extend(batch)

        # Check diversity
        diversity = compute_diversity_score(all_responses)

        if diversity >= target_diversity:
            break

    # Compute final metrics
    model_counts = {}
    for r in all_responses:
        model = r["model"]
        model_counts[model] = model_counts.get(model, 0) + 1

    metrics = {
        "diversity_achieved": compute_diversity_score(all_responses),
        "iterations": iteration,
        "model_distribution": model_counts,
        "total_responses": len(all_responses),
        "target_diversity": target_diversity,
    }

    return all_responses, metrics
