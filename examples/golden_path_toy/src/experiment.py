"""
Experiment Implementation: Coin Flip Fairness Test

Seed idea: Does a simulated coin flip produce heads and tails with approximately
equal probability over many trials?

This is a toy example demonstrating the Resonance Engine golden path.
"""

import numpy as np
from typing import Dict, Any


# Preregistered parameters (from PREREG.yaml)
RANDOM_SEED = 42
N_TRIALS = 1000
COIN_PROBABILITY = 0.5

# Acceptance/failure criteria (from NULLS.md and PREREG.yaml)
CI_LOWER = 0.45
CI_UPPER = 0.55
EXTREME_LOWER = 0.40
EXTREME_UPPER = 0.60


def run_experiment(
    n_trials: int = N_TRIALS,
    coin_p: float = COIN_PROBABILITY,
    random_seed: int = RANDOM_SEED
) -> Dict[str, Any]:
    """
    Run coin flip fairness experiment.

    Args:
        n_trials: Number of coin flips to perform
        coin_p: Probability of heads (0.5 for fair coin)
        random_seed: Random seed for reproducibility

    Returns:
        Dictionary with experiment results:
            - "n_trials": Number of flips performed
            - "n_heads": Number of heads observed
            - "n_tails": Number of tails observed
            - "proportion_heads": Proportion of heads
            - "standard_error": Standard error of proportion
            - "ci_lower": Lower bound of 95% CI
            - "ci_upper": Upper bound of 95% CI
            - "passes_primary_null": Whether result passes primary null (0.45-0.55)
            - "passes_extreme_null": Whether result passes extreme null (0.40-0.60)
            - "verdict": "PASS" or "FAIL"
    """
    # Set random seed for reproducibility
    np.random.seed(random_seed)

    # Simulate coin flips (1 = heads, 0 = tails)
    flips = np.random.binomial(n=1, p=coin_p, size=n_trials)

    # Count results
    n_heads = np.sum(flips)
    n_tails = n_trials - n_heads
    proportion_heads = n_heads / n_trials

    # Compute standard error
    se = np.sqrt(proportion_heads * (1 - proportion_heads) / n_trials)

    # Compute 95% confidence interval (using normal approximation)
    ci_lower_computed = proportion_heads - 1.96 * se
    ci_upper_computed = proportion_heads + 1.96 * se

    # Evaluate null hypotheses
    passes_primary_null = CI_LOWER <= proportion_heads <= CI_UPPER
    passes_extreme_null = EXTREME_LOWER <= proportion_heads <= EXTREME_UPPER

    # Overall verdict
    verdict = "PASS" if passes_primary_null else "FAIL"

    return {
        "n_trials": n_trials,
        "n_heads": int(n_heads),
        "n_tails": int(n_tails),
        "proportion_heads": float(proportion_heads),
        "standard_error": float(se),
        "ci_lower_computed": float(ci_lower_computed),
        "ci_upper_computed": float(ci_upper_computed),
        "ci_lower_preregistered": CI_LOWER,
        "ci_upper_preregistered": CI_UPPER,
        "passes_primary_null": passes_primary_null,
        "passes_extreme_null": passes_extreme_null,
        "verdict": verdict,
    }


def format_results(results: Dict[str, Any]) -> str:
    """
    Format experiment results as human-readable string.

    Args:
        results: Results dictionary from run_experiment()

    Returns:
        Formatted string for display
    """
    output = []
    output.append("=" * 60)
    output.append("COIN FLIP FAIRNESS TEST - RESULTS")
    output.append("=" * 60)
    output.append("")
    output.append(f"Total flips:       {results['n_trials']}")
    output.append(f"Heads:             {results['n_heads']}")
    output.append(f"Tails:             {results['n_tails']}")
    output.append(f"Proportion heads:  {results['proportion_heads']:.4f}")
    output.append(f"Standard error:    {results['standard_error']:.4f}")
    output.append("")
    output.append("Preregistered Criteria:")
    output.append(f"  Primary null bounds:  [{results['ci_lower_preregistered']}, {results['ci_upper_preregistered']}]")
    output.append(f"  Passes primary null:  {results['passes_primary_null']}")
    output.append(f"  Passes extreme null:  {results['passes_extreme_null']}")
    output.append("")
    output.append(f"VERDICT: {results['verdict']}")
    output.append("")

    if results['verdict'] == "PASS":
        output.append("✓ Coin appears fair (within 95% confidence interval)")
    else:
        output.append("✗ Coin fairness rejected (outside confidence interval)")

    output.append("=" * 60)

    return "\n".join(output)


def main():
    """Command-line entry point."""
    print("Running coin flip fairness experiment...")
    print(f"  Random seed: {RANDOM_SEED}")
    print(f"  Trials: {N_TRIALS}")
    print(f"  Coin probability: {COIN_PROBABILITY}")
    print()

    results = run_experiment()
    print(format_results(results))


if __name__ == "__main__":
    main()
