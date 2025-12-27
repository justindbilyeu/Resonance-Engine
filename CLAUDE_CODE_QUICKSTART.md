# Claude Code Quick Start Guide
## Organizing Resonance Engine Repository

This guide walks you through using Claude Code to organize your four repositories into the unified Resonance Engine structure.

## Prerequisites

1. **Install Claude Code**
   ```bash
   # Install via pip
   pip install claude-code
   
   # Or via homebrew (if available)
   brew install claude-code
   ```

2. **Clone All Repositories**
   ```bash
   mkdir ~/resonance-workspace
   cd ~/resonance-workspace
   
   git clone https://github.com/YourUsername/Resonance-Engine.git
   git clone https://github.com/YourUsername/ITPU.git
   git clone https://github.com/YourUsername/Geometric-Plasticity.git
   git clone https://github.com/YourUsername/JustAsking.git
   ```

3. **Verify Structure**
   ```bash
   ls ~/resonance-workspace
   # Should show: Resonance-Engine  ITPU  Geometric-Plasticity  JustAsking
   ```

## Method 1: Using the Python Script (Recommended)

### Step 1: Dry Run First
```bash
cd ~/resonance-workspace/Resonance-Engine
python organize_repos.py \
    --workspace ~/resonance-workspace \
    --target ~/resonance-workspace/Resonance-Engine \
    --dry-run
```

This will show you what would be done without making changes.

### Step 2: Execute the Organization
```bash
python organize_repos.py \
    --workspace ~/resonance-workspace \
    --target ~/resonance-workspace/Resonance-Engine
```

### Step 3: Review and Test
```bash
# Review the structure
tree -L 2

# Check the operation log
cat organization_log.json

# Run any existing tests
pytest tests/
```

## Method 2: Using Claude Code Interactively

### Step 1: Start Claude Code
```bash
cd ~/resonance-workspace/Resonance-Engine
claude-code
```

### Step 2: Initial Setup Command
```
@claude-code

I need to organize four repositories into a unified structure:
- Resonance-Engine (current repo)
- ITPU (in ~/resonance-workspace/ITPU)
- Geometric-Plasticity (in ~/resonance-workspace/Geometric-Plasticity)
- JustAsking (in ~/resonance-workspace/JustAsking)

Create the following directory structure:
- core/ (for Resonance Engine compiler)
- infrastructure/itpu/ (for ITPU)
- infrastructure/geometric_plasticity/ (for Geometric-Plasticity)
- infrastructure/orchestration/ (for JustAsking)
- bundles/ (for compiled experiments)
- standards/rm01/, standards/rm02/, standards/rm03/
- docs/, examples/, tests/

Show me the complete directory tree you'll create before making changes.
```

### Step 3: Integrate ITPU
```
@claude-code

Copy the contents from ~/resonance-workspace/ITPU to infrastructure/itpu/

Include:
- All source code for constraint health metrics
- Documentation about information-theoretic processing
- Any existing tests

Create infrastructure/itpu/README.md that explains:
- Purpose: Real-time constraint health metrics
- Role: Computational substrate for measuring coherence
- How it integrates with Resonance Engine

Preserve the original git history if possible using git subtree.
```

### Step 4: Integrate Geometric-Plasticity
```
@claude-code

Copy the contents from ~/resonance-workspace/Geometric-Plasticity to infrastructure/geometric_plasticity/

Include:
- Spectral stability analysis tools
- Phase transition detection
- Ringing diagnostics
- Pattern recognition algorithms

Create infrastructure/geometric_plasticity/README.md that explains:
- Purpose: Detect productive vs degenerate oscillation
- Role: Quality gates for constraint-driven development
- Integration with Builder/Skeptic roles

Show me what files will be moved before proceeding.
```

### Step 5: Integrate JustAsking
```
@claude-code

Copy the contents from ~/resonance-workspace/JustAsking to infrastructure/orchestration/

Include:
- Multi-AI fan-out patterns
- Consensus/dissent analysis
- Architectural diversity protocols
- Orchestration utilities

Create infrastructure/orchestration/README.md that explains:
- Purpose: Multi-AI coordination with architectural diversity
- Role: Breaking premature convergence
- Integration patterns for bundles

List the key files you'll be moving.
```

### Step 6: Add Bundle 0001
```
@claude-code

I have Bundle 0001 (the first compiled experiment) that needs to go in bundles/0001_rfo_ringing_wedge/

This bundle contains:
- CLAIM.md (falsifiable claim)
- OPERATIONALIZE.md (exact observables)
- PREREG.yaml (locked parameters)
- NULLS.md (rejection thresholds)
- COHERENCE_METRICS.yaml (constraint health)
- src/ directory with experiment code
- tests/ directory with validation tests

Create bundles/README.md explaining what bundles are and how Bundle 0001 proves the stack works.
```

### Step 7: Create Main Documentation
```
@claude-code

Create a comprehensive README.md for the repository that includes:

1. What Resonance Engine is (discovery compiler)
2. The four-component stack (Core, ITPU, Geometric-Plasticity, Orchestration)
3. Core principle: "Coherence is earned by constraints"
4. Quick start guide
5. Philosophy about democratizing research
6. Link to Bundle 0001 as proof of concept

Make it compelling and clear for someone discovering the project.
```

### Step 8: Create Configuration Files
```
@claude-code

Create the following configuration files:

1. pyproject.toml with:
   - Project metadata
   - Dependencies for all four components
   - Build system configuration
   - Dev dependencies (pytest, black, mypy, etc.)

2. setup.py for backwards compatibility

3. requirements.txt with all dependencies

4. .gitignore appropriate for Python projects

5. CONTRIBUTING.md with guidelines for:
   - Adding new bundles
   - Improving infrastructure
   - Standards refinement
```

### Step 9: Set Up Testing
```
@claude-code

Create a testing infrastructure:

tests/unit/ - Unit tests for individual components
tests/integration/ - Tests for component interactions  
tests/system/ - End-to-end bundle compilation tests

Create tests/README.md explaining:
- How to run tests
- Testing philosophy
- Coverage requirements
- How to add new tests

Set up pytest configuration in pyproject.toml.
```

### Step 10: Verify Everything
```
@claude-code

Please verify the integration:

1. Check that all imports work correctly
2. Ensure no circular dependencies
3. Validate directory structure matches the plan
4. Check that READMEs are accurate
5. Run any existing tests
6. Generate a final report of what was done

Create a file INTEGRATION_REPORT.md documenting:
- What was moved
- Any issues encountered
- Recommendations for next steps
```

## Method 3: Step-by-Step Manual with Claude Code Assistance

If you prefer more control, use Claude Code to help with individual steps:

### Moving Files
```
@claude-code
Move ~/resonance-workspace/ITPU/src/constraint_health.py to infrastructure/itpu/constraint_health.py
Update any imports that reference this file
```

### Creating READMEs
```
@claude-code
Create infrastructure/itpu/README.md explaining what ITPU does and how it fits in the stack
```

### Updating Imports
```
@claude-code
Update all imports in the codebase from 'itpu.constraint_health' to 'infrastructure.itpu.constraint_health'
Show me the changes before applying them
```

### Creating Tests
```
@claude-code
Create tests/integration/test_itpu_integration.py that validates ITPU works with the core compiler
```

## Validation Checklist

After organization, verify:

- [ ] All four repositories integrated
- [ ] Directory structure matches specification
- [ ] All imports updated correctly
- [ ] READMEs created for each component
- [ ] Main README is comprehensive
- [ ] Configuration files created
- [ ] Tests still pass (or new tests created)
- [ ] No broken dependencies
- [ ] Bundle 0001 in place
- [ ] Git history preserved where important

## Common Issues and Solutions

### Issue: Import Errors
```
@claude-code
I'm getting import errors after moving files. Please:
1. Scan all Python files for import statements
2. Update them to match the new structure
3. Add __init__.py files where needed
4. Show me the changes before applying
```

### Issue: Tests Failing
```
@claude-code
Tests are failing after the reorganization. Please:
1. Identify which tests are failing
2. Update test imports to match new structure
3. Fix any broken fixtures or test data paths
4. Run tests again and show results
```

### Issue: Git History Lost
```
@claude-code
I want to preserve git history when moving ITPU. Please use git subtree to:
1. Create a subtree for infrastructure/itpu
2. Pull in the ITPU repository
3. Preserve commit history
4. Show me the git log to verify
```

### Issue: Circular Dependencies
```
@claude-code
Please analyze the import graph and identify any circular dependencies.
For each one found:
1. Explain why it's circular
2. Suggest how to refactor
3. Show the proposed changes
```

## Next Steps After Organization

### 1. Validate the Integration
```bash
# Run all tests
pytest tests/ -v

# Check import structure
python -c "from core import ResonanceEngine; from infrastructure.itpu import ConstraintHealthMonitor"

# Verify bundle structure
ls bundles/0001_rfo_ringing_wedge/
```

### 2. Create Your First Experiment
```
@claude-code

Using the integrated stack, help me create Bundle 0002.

Question: [Your research question]

Walk me through:
1. Using the Resonance Engine compiler
2. Monitoring constraint health with ITPU
3. Validating with Geometric-Plasticity diagnostics
4. Orchestrating multi-AI validation

Generate the complete bundle structure.
```

### 3. Improve Documentation
```
@claude-code

Create comprehensive documentation in docs/:

docs/architecture/SYSTEM_OVERVIEW.md - How all components work together
docs/tutorials/FIRST_BUNDLE.md - Step-by-step first bundle
docs/tutorials/MULTI_AI_ORCHESTRATION.md - Using JustAsking patterns
docs/api/ - API documentation for each component
```

### 4. Set Up CI/CD
```
@claude-code

Create .github/workflows/ with:
1. test.yml - Run tests on every PR
2. validate_bundle.yml - Validate new bundles
3. constraint_health.yml - Monitor constraint health
4. docs.yml - Build and deploy documentation

Each should use appropriate caching and report results clearly.
```

## Tips for Working with Claude Code

1. **Be Specific**: Describe exactly what you want moved/created
2. **Review First**: Always ask Claude Code to show changes before applying
3. **Incremental**: Do one major change at a time
4. **Test Often**: Run tests after each integration
5. **Commit Frequently**: Commit after each successful step
6. **Use Dry Runs**: Test with `--dry-run` when available

## Getting Help

If you run into issues:

1. **Check the logs**: `organization_log.json` has details
2. **Use dry-run**: See what would change without changing it
3. **Ask Claude Code**: It can diagnose and fix issues
4. **Rollback**: Use git to revert if needed: `git reset --hard HEAD`

## Philosophy

Remember: This isn't just organizing code. You're building infrastructure where:
- Constraints enable rather than limit
- Human intuition + AI capability + rigorous constraints = insights neither could reach alone
- Distributed cognition becomes more coherent than individual cognition
- Rigorous research becomes accessible to anyone

Every step in this process serves that goal.

---

**Questions?** Create an issue or ask Claude Code for help with any step.
