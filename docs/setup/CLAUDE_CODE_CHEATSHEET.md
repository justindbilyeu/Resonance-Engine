# Claude Code Command Cheat Sheet
## Resonance Engine Organization

Quick reference for common Claude Code commands during repository organization.

## Initial Setup

```bash
# Verify all repos are present
@claude-code List all directories in ~/resonance-workspace

# Create directory structure
@claude-code Create these directories in the current repo:
core/
infrastructure/{itpu,geometric_plasticity,orchestration}/
bundles/
standards/{rm01,rm02,rm03}/
docs/{architecture,tutorials,api}/
examples/{basic,advanced,integration}/
tests/{unit,integration,system}/
```

## Integration Commands

### ITPU Integration
```bash
@claude-code Copy ~/resonance-workspace/ITPU to infrastructure/itpu/
Preserve key git commits
Create infrastructure/itpu/README.md
Update imports throughout codebase
```

### Geometric-Plasticity Integration
```bash
@claude-code Copy ~/resonance-workspace/Geometric-Plasticity to infrastructure/geometric_plasticity/
Create README explaining ringing diagnostics
Update any cross-references
```

### JustAsking Integration
```bash
@claude-code Copy ~/resonance-workspace/JustAsking to infrastructure/orchestration/
Create README about multi-AI coordination
Preserve orchestration examples
```

## File Operations

### Move Single File
```bash
@claude-code Move file.py from source/ to infrastructure/itpu/
Update all imports that reference it
```

### Move Multiple Files
```bash
@claude-code Move all files matching pattern *.py from src/ to core/
Update imports
Create __init__.py if needed
```

### Copy with History
```bash
@claude-code Use git subtree to copy ITPU to infrastructure/itpu/
Preserve commit history
Show git log to verify
```

## Documentation

### Create README
```bash
@claude-code Create infrastructure/itpu/README.md with:
- Purpose (constraint health metrics)
- Role in stack
- Key components
- Usage example
- Links to detailed docs
```

### Create Main README
```bash
@claude-code Create comprehensive README.md covering:
- What Resonance Engine is
- Four-component stack
- Core principle
- Quick start
- Philosophy
```

### API Documentation
```bash
@claude-code Generate API documentation for infrastructure/itpu/
Include all public functions
Add usage examples
Create docs/api/ITPU_API.md
```

## Import Management

### Update All Imports
```bash
@claude-code Update all imports from 'itpu' to 'infrastructure.itpu'
Show me changes before applying
Run import checker after
```

### Fix Broken Imports
```bash
@claude-code Scan for broken imports after reorganization
Fix each one
Verify with import checker
```

### Create __init__.py Files
```bash
@claude-code Create __init__.py files for all packages
Export public APIs
Add docstrings
```

## Testing

### Create Test Structure
```bash
@claude-code Create test structure in tests/:
unit/ - individual components
integration/ - component interactions
system/ - end-to-end tests
Add tests/README.md
```

### Run Tests
```bash
@claude-code Run pytest tests/ -v
Show me any failures
Suggest fixes for failing tests
```

### Update Test Imports
```bash
@claude-code Update all test imports to match new structure
Fix broken fixtures
Update test data paths
```

## Configuration

### Create pyproject.toml
```bash
@claude-code Create pyproject.toml with:
- Project metadata
- Dependencies (all components)
- Build configuration
- Dev dependencies
- Pytest configuration
```

### Create Setup Files
```bash
@claude-code Create:
- setup.py (for backwards compatibility)
- requirements.txt
- requirements-dev.txt
- .gitignore (Python project)
```

## Validation

### Check Structure
```bash
@claude-code Show me complete directory tree
Verify it matches specification
List any missing directories
```

### Verify Imports
```bash
@claude-code Test all imports:
from core import ResonanceEngine
from infrastructure.itpu import ConstraintHealthMonitor
from infrastructure.geometric_plasticity import RingingDetector
from infrastructure.orchestration import MultiAIOrchestrator
```

### Run Integration Test
```bash
@claude-code Create and run integration test that:
- Imports all components
- Tests basic interactions
- Validates constraint health
- Checks orchestration patterns
```

## Troubleshooting

### Find Import Errors
```bash
@claude-code Scan entire codebase for import errors
List each error with file location
Suggest fix for each
```

### Fix Circular Dependencies
```bash
@claude-code Analyze import graph
Identify circular dependencies
Suggest refactoring
Show proposed changes
```

### Restore from Backup
```bash
@claude-code Help me restore from git:
Show recent commits
Identify good restore point
Explain rollback process
```

## Common Workflows

### Add New Component
```bash
@claude-code Add new component to infrastructure/component_name/
Create README
Update main README
Add to __init__.py
Create tests
Update documentation
```

### Create New Bundle
```bash
@claude-code Create bundles/NNNN_bundle_name/ with:
- CLAIM.md
- OPERATIONALIZE.md
- PREREG.yaml
- NULLS.md
- COHERENCE_METRICS.yaml
- src/ directory
- tests/ directory
- README.md
```

### Update Documentation
```bash
@claude-code Update docs/ with:
- New tutorials
- API changes
- Architecture updates
- Usage examples
```

## Quick Checks

```bash
# Verify Python imports
@claude-code python -c "import core; import infrastructure.itpu"

# Run quick test
@claude-code pytest tests/unit/ -x

# Check file structure
@claude-code tree -L 2

# Verify git status
@claude-code git status

# Show recent changes
@claude-code git diff

# List all READMEs
@claude-code find . -name "README.md" -type f
```

## Best Practices

1. **Always review first**: Ask Claude Code to show changes before applying
2. **Test incrementally**: Run tests after each integration
3. **Commit often**: Commit after each successful step
4. **Use dry-run**: When available, test without making changes
5. **Check imports**: Verify imports work after each move
6. **Update docs**: Keep documentation in sync with code
7. **Preserve history**: Use git subtree when history matters

## Emergency Commands

### Undo Last Change
```bash
@claude-code git reset --hard HEAD~1
Show me what was undone
```

### Check What Would Break
```bash
@claude-code Before moving file.py, show me:
- All files that import it
- All files it imports
- Tests that depend on it
```

### Safe Mode Move
```bash
@claude-code Move file.py but:
1. Create backup first
2. Update all imports
3. Run tests
4. Only commit if tests pass
5. Rollback if anything fails
```

## Reminder

Every command is building infrastructure where:
- **Constraints enable** rather than limit
- **Distributed cognition** is more coherent than individual cognition  
- **Rigorous research** is accessible to anyone

Use these commands in service of that goal.
