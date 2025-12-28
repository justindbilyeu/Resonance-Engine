#!/usr/bin/env python3
"""
enforce_bundle_contract.py

Gate G1: Bundle Contract Enforcement (RM-01)

This script enforces the bundle contract:
1. No bundle artifacts in repository root
2. Each bundle has required files
3. Bundle structure is valid

Exit codes:
  0 - All checks pass
  1 - Contract violations found

This is RG² Step 2: Make RM-01 real by enforcing exactly one gate.
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Bundle contract: required files
REQUIRED_BUNDLE_FILES = {
    "CLAIM.md": "Falsifiable claim (≤3 sentences)",
    "NULLS.md": "Numeric rejection thresholds (≥2)",
    "OPERATIONALIZE.md": "Observables and estimators",
    "PREREG.yaml": "Locked parameters and sweep",
}

# Bundle artifacts that must NOT appear in root
FORBIDDEN_IN_ROOT = [
    "CLAIM.md",
    "NULLS.md",
    "OPERATIONALIZE.md",
    "PREREG.yaml",
    "COHERENCE_METRICS.yaml",
    "MANIFEST.json",
    "DEVELOPER_NOTES.md",
    "constraint_health_history.csv",
    "dissent_history.csv",
    "decision_trace.md",
    "hard_gate_results.json",
    "parameters_used.json",
    "seed_manifest.json",
    "wedge_report.md",
    "grid.csv",
]


class ContractViolation:
    """Represents a bundle contract violation"""
    
    def __init__(self, severity: str, category: str, message: str):
        self.severity = severity  # ERROR, WARNING
        self.category = category
        self.message = message
    
    def __str__(self):
        return f"[{self.severity}] {self.category}: {self.message}"


def check_root_cleanliness(repo_root: Path) -> List[ContractViolation]:
    """Check that no bundle artifacts appear in repository root"""
    violations = []
    
    for forbidden_file in FORBIDDEN_IN_ROOT:
        if (repo_root / forbidden_file).exists():
            violations.append(ContractViolation(
                severity="ERROR",
                category="Root Cleanliness",
                message=f"Bundle artifact '{forbidden_file}' found in root (should be in bundles/*/)"
            ))
    
    return violations


def check_bundle_structure(bundle_path: Path) -> List[ContractViolation]:
    """Check that bundle has required files and valid structure"""
    violations = []
    bundle_name = bundle_path.name
    
    # Check required files exist
    for required_file, description in REQUIRED_BUNDLE_FILES.items():
        file_path = bundle_path / required_file
        if not file_path.exists():
            violations.append(ContractViolation(
                severity="ERROR",
                category="Bundle Structure",
                message=f"Bundle '{bundle_name}' missing {required_file} ({description})"
            ))
    
    # Check CLAIM.md is bounded (≤3 sentences heuristic: ≤500 chars)
    claim_path = bundle_path / "CLAIM.md"
    if claim_path.exists():
        claim_text = claim_path.read_text()
        # Very rough heuristic: claim should be short
        if len(claim_text) > 2000:
            violations.append(ContractViolation(
                severity="WARNING",
                category="Claim Boundedness",
                message=f"Bundle '{bundle_name}' CLAIM.md seems very long ({len(claim_text)} chars). Should be ≤3 sentences."
            ))
    
    # Check NULLS.md has numeric thresholds
    nulls_path = bundle_path / "NULLS.md"
    if nulls_path.exists():
        nulls_text = nulls_path.read_text()
        # Count numeric literals (crude but effective)
        import re
        nums = re.findall(r'\b\d+(?:\.\d+)?\b', nulls_text)
        if len(nums) < 2:
            violations.append(ContractViolation(
                severity="ERROR",
                category="Null Thresholds",
                message=f"Bundle '{bundle_name}' NULLS.md contains <2 numeric thresholds (found {len(nums)})"
            ))
    
    # Check src/ directory exists
    src_path = bundle_path / "src"
    if not src_path.exists():
        violations.append(ContractViolation(
            severity="WARNING",
            category="Bundle Structure",
            message=f"Bundle '{bundle_name}' missing src/ directory (experiment code)"
        ))
    
    return violations


def find_bundles(repo_root: Path) -> List[Path]:
    """Find all bundle directories in bundles/"""
    bundles_dir = repo_root / "bundles"
    
    if not bundles_dir.exists():
        return []
    
    # Bundle directories are direct children of bundles/
    # They should match pattern: NNNN_* or similar
    bundles = []
    for item in bundles_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            bundles.append(item)
    
    return sorted(bundles)


def main() -> int:
    """
    Enforce bundle contract across repository.
    
    Returns:
        0 if all checks pass
        1 if violations found
    """
    # Find repository root (where this script is run from)
    repo_root = Path.cwd()
    
    print("=" * 60)
    print("Gate G1: Bundle Contract Enforcement (RM-01)")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print()
    
    all_violations = []
    
    # Check 1: Root cleanliness
    print("[1/3] Checking root cleanliness...")
    root_violations = check_root_cleanliness(repo_root)
    all_violations.extend(root_violations)
    
    if root_violations:
        print(f"  ✗ {len(root_violations)} violation(s) found")
        for v in root_violations:
            print(f"      {v}")
    else:
        print("  ✓ Root is clean (no bundle artifacts)")
    print()
    
    # Check 2: Find bundles
    print("[2/3] Finding bundles...")
    bundles = find_bundles(repo_root)
    
    if not bundles:
        print("  ⚠ No bundles found in bundles/ directory")
        print("  (This is not a violation, but bundles are expected)")
    else:
        print(f"  Found {len(bundles)} bundle(s):")
        for bundle in bundles:
            print(f"    - {bundle.name}")
    print()
    
    # Check 3: Validate each bundle
    print("[3/3] Validating bundle structures...")
    for bundle_path in bundles:
        bundle_violations = check_bundle_structure(bundle_path)
        all_violations.extend(bundle_violations)
        
        if bundle_violations:
            print(f"  ✗ {bundle_path.name}: {len(bundle_violations)} violation(s)")
            for v in bundle_violations:
                print(f"      {v}")
        else:
            print(f"  ✓ {bundle_path.name}: passes contract")
    
    print()
    print("=" * 60)
    
    # Summary
    errors = [v for v in all_violations if v.severity == "ERROR"]
    warnings = [v for v in all_violations if v.severity == "WARNING"]
    
    if errors:
        print(f"GATE FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        print()
        print("Errors must be fixed:")
        for v in errors:
            print(f"  {v}")
        
        if warnings:
            print()
            print("Warnings (should fix but not blocking):")
            for v in warnings:
                print(f"  {v}")
        
        print()
        print("Bundle contract violated. Fix errors before committing.")
        return 1
    
    elif warnings:
        print(f"GATE PASSED (with warnings): {len(warnings)} warning(s)")
        print()
        print("Warnings (should fix but not blocking):")
        for v in warnings:
            print(f"  {v}")
        print()
        print("Bundle contract satisfied (warnings are advisory)")
        return 0
    
    else:
        print("GATE PASSED: All checks passed ✓")
        print()
        print("Bundle contract satisfied:")
        print(f"  - Root is clean ({len(FORBIDDEN_IN_ROOT)} artifact types checked)")
        print(f"  - All {len(bundles)} bundle(s) have required files")
        print(f"  - All bundles have valid structure")
        return 0


if __name__ == "__main__":
    sys.exit(main())
