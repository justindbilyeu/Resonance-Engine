"""
Bundle 0001 Execution Test
Forces experiment.py to run in quick mode and validates outputs exist.
This is the golden path test proving the Resonance Engine works.
"""

import subprocess
import json
from pathlib import Path
import shutil


def test_bundle_0001_runs_and_produces_outputs():
    """Run Bundle 0001 in quick mode and verify all required outputs."""

    bundle_dir = Path(__file__).parent.parent
    output_dir = bundle_dir / "test_outputs"

    # Clean previous test outputs
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Run experiment in quick mode
    result = subprocess.run(
        [
            "python",
            str(bundle_dir / "src" / "experiment.py"),
            "--quick",
            "--no-negative-control",
            "--out",
            str(output_dir)
        ],
        capture_output=True,
        text=True
    )

    # Verify execution succeeded
    assert result.returncode == 0, f"Experiment failed:\n{result.stderr}"

    # Verify required outputs exist
    required_files = [
        "grid.csv",
        "wedge_report.md",
        "null_evaluation.json",
        "parameters_used.json",
        "seed_manifest.json"
    ]

    for filename in required_files:
        filepath = output_dir / filename
        assert filepath.exists(), f"Missing required output: {filename}"

    # Verify null_evaluation.json has required structure
    with open(output_dir / "null_evaluation.json") as f:
        null_eval = json.load(f)

    # Check for key top-level fields
    assert "bundle_id" in null_eval, "null_evaluation.json missing bundle_id"
    assert "mode" in null_eval, "null_evaluation.json missing mode"
    assert "claim_rejected" in null_eval, "null_evaluation.json missing claim_rejected"
    assert "rejection_criteria" in null_eval, "null_evaluation.json missing rejection_criteria"

    print("Bundle 0001 execution test passed")
    print(f"   Outputs created in: {output_dir}")
