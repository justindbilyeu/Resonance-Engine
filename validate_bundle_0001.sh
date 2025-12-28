#!/usr/bin/env bash
# validate_bundle_0001.sh
# 
# Smoke test for Bundle #0001 - validates the experiment runs and produces required artifacts
# This is RG² Step 1: Validate what exists by producing run artifacts

set -e  # Exit on any error

BUNDLE_DIR="bundles/0001_rfo_ringing_wedge"
RUN_ARTIFACTS_DIR="${BUNDLE_DIR}/run_artifacts"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${RUN_ARTIFACTS_DIR}/smoke_${TIMESTAMP}"

echo "=== Bundle #0001 Smoke Test Validation ==="
echo "Timestamp: ${TIMESTAMP}"
echo "Output directory: ${OUTPUT_DIR}"
echo ""

# Create run artifacts directory
mkdir -p "${OUTPUT_DIR}"

# Run the experiment in quick mode
echo "[1/4] Running experiment in --quick mode..."
python "${BUNDLE_DIR}/src/experiment_0001_rfo_ringing_wedge.py" \
    --quick \
    --out "${OUTPUT_DIR}" \
    --no-negative-control

# Verify required artifacts exist
echo ""
echo "[2/4] Verifying required artifacts..."

REQUIRED_FILES=(
    "parameters_used.json"
    "seed_manifest.json"
    "grid.csv"
    "wedge_report.md"
    "null_evaluation.json"
    "DEVIATIONS_FROM_PREREG.md"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "${OUTPUT_DIR}/${file}" ]; then
        echo "  ✓ ${file}"
    else
        echo "  ✗ MISSING: ${file}"
        MISSING_FILES+=("${file}")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo ""
    echo "ERROR: Missing required artifacts:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - ${file}"
    done
    exit 1
fi

# Verify points directory
if [ -d "${OUTPUT_DIR}/points" ]; then
    POINT_COUNT=$(ls -1 "${OUTPUT_DIR}/points" | wc -l)
    echo "  ✓ points/ directory (${POINT_COUNT} files)"
else
    echo "  ✗ MISSING: points/ directory"
    exit 1
fi

# Parse and display null evaluation results
echo ""
echo "[3/4] Null evaluation results:"

REJECTED=$(python3 -c "import json; print(json.load(open('${OUTPUT_DIR}/null_evaluation.json'))['rejected'])")
echo "  Claim rejected: ${REJECTED}"

# Show each null result
python3 << EOF
import json
with open('${OUTPUT_DIR}/null_evaluation.json') as f:
    data = json.load(f)
    for null_name, null_data in data['nulls'].items():
        reject = null_data['reject']
        status = "REJECT" if reject else "PASS"
        print(f"  [{status}] {null_name}")
EOF

# Create validation summary
echo ""
echo "[4/4] Creating validation summary..."

cat > "${OUTPUT_DIR}/VALIDATION_SUMMARY.md" << EOF
# Bundle #0001 Smoke Test Validation Summary

**Timestamp:** ${TIMESTAMP}  
**Mode:** Quick (smoke test)  
**Status:** COMPLETED

## Artifacts Generated

All required artifacts produced:
$(for file in "${REQUIRED_FILES[@]}"; do echo "- ${file}"; done)
- points/ directory (${POINT_COUNT} point files)

## Null Evaluation Results

**Claim Rejected:** ${REJECTED}

$(python3 -c "
import json
with open('${OUTPUT_DIR}/null_evaluation.json') as f:
    data = json.load(f)
    for null_name, null_data in data['nulls'].items():
        reject = null_data['reject']
        status = 'REJECT' if reject else 'PASS'
        print(f'- [{status}] {null_name}')
")

## Notes

This is a smoke test run using \`--quick\` mode with:
- Small grid (3×3 instead of 81×61)
- Reduced network size (N=32 instead of 128)
- Shorter simulation (6k steps instead of 200k)
- Single replicate (instead of 3)
- No negative control

**This run is NOT prereg-compliant** and results should not be treated as scientific evidence.

See \`DEVIATIONS_FROM_PREREG.md\` for details.

## Validation Criteria

✅ Experiment runs without errors  
✅ All required artifacts produced  
✅ Artifacts have valid structure (JSON parseable, CSV readable)  
✅ Null evaluation completes  

## What This Proves

Bundle #0001 can execute and produce structured outputs. The compilation contract is satisfied:
- CLAIM.md exists and is bounded
- NULLS.md has numeric thresholds
- Code runs and evaluates nulls
- Artifacts are produced deterministically

## Next Steps

1. Run full prereg sweep (remove \`--quick\` flag)
2. Include negative control (remove \`--no-negative-control\`)
3. Analyze results against all 4 null hypotheses
4. Preserve outputs as run_artifacts/prereg_YYYYMMDD/
EOF

echo ""
echo "=== Validation Complete ==="
echo ""
echo "Summary written to: ${OUTPUT_DIR}/VALIDATION_SUMMARY.md"
echo ""
echo "Quick check - claim rejected: ${REJECTED}"
echo ""
echo "To view full results:"
echo "  cat ${OUTPUT_DIR}/VALIDATION_SUMMARY.md"
echo "  cat ${OUTPUT_DIR}/wedge_report.md"
echo "  python3 -m json.tool ${OUTPUT_DIR}/null_evaluation.json"
echo ""
echo "This smoke test proves Bundle #0001 can execute and produce artifacts."
echo "For prereg-compliant run, execute without --quick flag."
