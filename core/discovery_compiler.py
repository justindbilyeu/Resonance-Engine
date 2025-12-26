"""
Discovery Compiler

Orchestrates multi-AI roles (Builder/Skeptic/Auditor/Operator) to progressively
constrain a research question into a runnable experiment with explicit failure criteria.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from core.metrics.null_gate import assert_numeric_nulls


def compile(seed: str, output_dir: str, enforce_null_gate: bool = True) -> None:
    """
    Compile a seed research question into a preregistered experiment bundle.

    This is a "dumb copier" implementation for PR-2. It generates a bundle skeleton
    from templates, replacing {seed} placeholders and enforcing the null completeness
    gate.

    Future versions will orchestrate multi-role AI agents (Builder/Skeptic/Auditor/
    Operator) to progressively refine the bundle through constraint-driven iteration.

    Args:
        seed: Initial research question or hypothesis
        output_dir: Directory to write experiment bundle artifacts (will be created)
        enforce_null_gate: Whether to enforce null completeness gate (default: True)

    Raises:
        ValueError: If null completeness gate fails and enforce_null_gate=True
        FileExistsError: If output_dir already exists
        RuntimeError: If bundle generation fails (output_dir will be cleaned up)

    Example:
        >>> compile(
        ...     seed="Does model size predict recovery time from perturbations?",
        ...     output_dir="experiments/model_recovery_001"
        ... )
        Bundle generated successfully at experiments/model_recovery_001/
    """
    output_path = Path(output_dir)
    templates_dir = Path(__file__).parent.parent / "templates"

    # Validate inputs
    if not seed or not seed.strip():
        raise ValueError("Seed idea cannot be empty")

    if output_path.exists():
        raise FileExistsError(
            f"Output directory already exists: {output_dir}\n"
            f"Please choose a different path or remove the existing directory."
        )

    # Template files to copy
    template_files = {
        "CLAIM.template.md": "CLAIM.md",
        "OPERATIONALIZE.template.md": "OPERATIONALIZE.md",
        "PREREG.template.yaml": "PREREG.yaml",
        "NULLS.template.md": "NULLS.md",
        "COHERENCE_METRICS.template.yaml": "COHERENCE_METRICS.yaml",
    }

    try:
        # Create output directory structure
        output_path.mkdir(parents=True, exist_ok=False)
        (output_path / "src").mkdir(exist_ok=True)
        (output_path / "tests").mkdir(exist_ok=True)

        # Copy and process templates
        for template_name, output_name in template_files.items():
            template_path = templates_dir / template_name
            output_file = output_path / output_name

            if not template_path.exists():
                raise FileNotFoundError(f"Template not found: {template_path}")

            # Read template and replace {seed} placeholder
            with open(template_path, "r") as f:
                content = f.read()

            # Replace placeholders
            content = content.replace("{seed}", seed)

            # Write to output
            with open(output_file, "w") as f:
                f.write(content)

        # Generate stub experiment code
        _generate_experiment_stubs(output_path, seed)

        # Enforce null completeness gate
        if enforce_null_gate:
            nulls_path = output_path / "NULLS.md"
            with open(nulls_path, "r") as f:
                nulls_content = f.read()

            # This will raise ValueError if < 2 numeric thresholds
            assert_numeric_nulls(nulls_content, min_thresholds=2)

        # Update COHERENCE_METRICS.yaml with actual generation data
        _update_coherence_metrics(output_path, seed, enforce_null_gate)

    except Exception as e:
        # Clean up partial bundle on failure
        if output_path.exists():
            shutil.rmtree(output_path)

        # Re-raise with context
        raise RuntimeError(
            f"Bundle generation failed: {e}\n"
            f"Cleaned up partial bundle at: {output_dir}"
        ) from e


def _generate_experiment_stubs(output_path: Path, seed: str) -> None:
    """Generate stub experiment.py and test_experiment.py files."""

    # Generate src/experiment.py
    experiment_code = f'''"""
Experiment Implementation

Seed idea: {seed}

This is a stub implementation. Replace with your actual experiment code.
"""


def run_experiment():
    """
    Main experiment entry point.

    Implement your experiment logic here following the protocol in
    OPERATIONALIZE.md and using parameters from PREREG.yaml.

    Returns:
        dict: Results dictionary with metrics matching NULLS.md thresholds
    """
    raise NotImplementedError(
        "Implement experiment following OPERATIONALIZE.md protocol"
    )


def main():
    """Command-line entry point."""
    results = run_experiment()
    print("Results:", results)


if __name__ == "__main__":
    main()
'''

    # Generate tests/test_experiment.py
    test_code = f'''"""
Experiment Tests

Validates that the experiment can run and checks null hypothesis thresholds.

Seed idea: {seed}
"""

import pytest


def test_experiment_imports():
    """Test that experiment module can be imported."""
    from src import experiment
    assert hasattr(experiment, "run_experiment")


def test_experiment_stub_not_implemented():
    """Test that stub raises NotImplementedError (remove when implemented)."""
    from src.experiment import run_experiment

    with pytest.raises(NotImplementedError):
        run_experiment()


# Add tests for your specific experiment here
# def test_null_threshold_1():
#     """Test that results meet/fail first null hypothesis threshold."""
#     pass
#
# def test_null_threshold_2():
#     """Test that results meet/fail second null hypothesis threshold."""
#     pass
'''

    # Write files
    with open(output_path / "src" / "experiment.py", "w") as f:
        f.write(experiment_code)

    with open(output_path / "tests" / "test_experiment.py", "w") as f:
        f.write(test_code)

    # Create __init__.py files for proper package structure
    (output_path / "src" / "__init__.py").touch()
    (output_path / "tests" / "__init__.py").touch()


def _update_coherence_metrics(
    output_path: Path,
    seed: str,
    null_gate_enforced: bool
) -> None:
    """Update COHERENCE_METRICS.yaml with actual generation data."""
    import yaml

    metrics_path = output_path / "COHERENCE_METRICS.yaml"

    # Read the template
    with open(metrics_path, "r") as f:
        metrics = yaml.safe_load(f)

    # Count actual thresholds in generated NULLS.md
    nulls_path = output_path / "NULLS.md"
    with open(nulls_path, "r") as f:
        nulls_content = f.read()

    from core.metrics.null_gate import count_numeric_thresholds
    threshold_count = count_numeric_thresholds(nulls_content)

    # Update with actual values
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metrics["generation"]["timestamp"] = timestamp
    metrics["constraint_health"]["null_completeness"]["numeric_thresholds_found"] = threshold_count
    metrics["constraint_health"]["null_completeness"]["status"] = (
        "pass" if threshold_count >= 2 else "fail"
    )
    metrics["stages"][0]["timestamp"] = timestamp
    metrics["controller_decisions"][0]["timestamp"] = timestamp

    if not null_gate_enforced:
        metrics["controller_decisions"][0]["reason"] += " (gate enforcement disabled)"

    # Write back
    with open(metrics_path, "w") as f:
        yaml.dump(metrics, f, default_flow_style=False, sort_keys=False)


def main():
    """Command-line interface for the discovery compiler."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="python -m core.discovery_compiler",
        description="Resonance Engine Discovery Compiler - Generate experiment bundles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate bundle from seed idea
  python -m core.discovery_compiler \\
    --seed "Does model size predict recovery time from perturbations?" \\
    --output experiments/model_recovery_001

  # Skip null gate enforcement (for testing)
  python -m core.discovery_compiler \\
    --seed "Test experiment" \\
    --output experiments/test_001 \\
    --no-null-gate

For more information, see: https://github.com/justindbilyeu/Resonance-Engine
        """
    )

    parser.add_argument(
        "--seed",
        required=True,
        help="Seed research question or hypothesis"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for experiment bundle (will be created)"
    )

    parser.add_argument(
        "--no-null-gate",
        action="store_true",
        help="Disable null completeness gate enforcement (not recommended)"
    )

    args = parser.parse_args()

    try:
        # Run compiler
        print(f"Generating experiment bundle...")
        print(f"  Seed: {args.seed}")
        print(f"  Output: {args.output}")
        print()

        compile(
            seed=args.seed,
            output_dir=args.output,
            enforce_null_gate=not args.no_null_gate
        )

        print(f"✓ Bundle generated successfully at: {args.output}")
        print()
        print("Next steps:")
        print(f"  1. Review and customize templates in {args.output}/")
        print(f"  2. Implement experiment logic in {args.output}/src/experiment.py")
        print(f"  3. Update tests in {args.output}/tests/test_experiment.py")
        print(f"  4. Run experiments and document results")
        print()

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
