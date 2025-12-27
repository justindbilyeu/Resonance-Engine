#!/usr/bin/env python3
"""
Resonance Engine Repository Organization Script

This script automates the initial setup of the Resonance Engine repository structure.
It's designed to work with Claude Code to organize the four repositories into a
unified cognitive infrastructure stack.

Usage:
    python organize_repos.py --workspace ~/resonance-workspace --target ~/Resonance-Engine

Prerequisites:
    - All four repositories cloned into workspace directory
    - Python 3.8+
    - Git installed
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import sys


class ResonanceOrganizerError(Exception):
    """Base exception for organizer errors"""
    pass


class ResonanceOrganizer:
    """Organizes four repositories into unified Resonance Engine structure"""
    
    def __init__(self, workspace: Path, target: Path, dry_run: bool = False):
        self.workspace = workspace
        self.target = target
        self.dry_run = dry_run
        self.log_file = target / "organization_log.json"
        self.operations_log = []
        
    def log_operation(self, operation: str, details: Dict):
        """Log an operation for tracking and potential rollback"""
        entry = {
            "operation": operation,
            "details": details,
            "dry_run": self.dry_run
        }
        self.operations_log.append(entry)
        print(f"{'[DRY RUN] ' if self.dry_run else ''}{operation}: {details.get('description', '')}")
        
    def verify_prerequisites(self) -> bool:
        """Verify all prerequisites are met"""
        print("\n=== Verifying Prerequisites ===\n")
        
        # Check workspace exists
        if not self.workspace.exists():
            raise ResonanceOrganizerError(f"Workspace not found: {self.workspace}")
        
        # Check for required repositories
        required_repos = ["Resonance-Engine", "ITPU", "Geometric-Plasticity", "JustAsking"]
        missing_repos = []
        
        for repo in required_repos:
            repo_path = self.workspace / repo
            if not repo_path.exists():
                missing_repos.append(repo)
            else:
                print(f"✓ Found {repo}")
        
        if missing_repos:
            raise ResonanceOrganizerError(
                f"Missing repositories: {', '.join(missing_repos)}\n"
                f"Please clone all repositories to {self.workspace}"
            )
        
        # Check git is available
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            print("✓ Git is available")
        except subprocess.CalledProcessError:
            raise ResonanceOrganizerError("Git is not available")
        
        print("\n✓ All prerequisites met\n")
        return True
    
    def create_directory_structure(self):
        """Create the new directory structure"""
        print("\n=== Creating Directory Structure ===\n")
        
        directories = [
            "core",
            "infrastructure/itpu",
            "infrastructure/geometric_plasticity",
            "infrastructure/orchestration",
            "bundles",
            "standards/rm01",
            "standards/rm02",
            "standards/rm03",
            "docs/architecture",
            "docs/tutorials",
            "docs/api",
            "examples/basic",
            "examples/advanced",
            "examples/integration",
            "tests/unit",
            "tests/integration",
            "tests/system",
        ]
        
        for directory in directories:
            dir_path = self.target / directory
            if not self.dry_run:
                dir_path.mkdir(parents=True, exist_ok=True)
            self.log_operation("create_directory", {
                "description": f"Created {directory}",
                "path": str(dir_path)
            })
    
    def copy_with_git_history(self, source: Path, dest: Path, description: str):
        """Copy files while attempting to preserve relevant git history"""
        if not self.dry_run:
            if dest.exists():
                print(f"  Destination exists: {dest}, skipping copy")
                return
            
            # For now, simple copy - git history preservation would need git subtree
            shutil.copytree(source, dest, dirs_exist_ok=True)
        
        self.log_operation("copy_repository_content", {
            "description": description,
            "source": str(source),
            "destination": str(dest)
        })
    
    def integrate_itpu(self):
        """Integrate ITPU repository into infrastructure/itpu/"""
        print("\n=== Integrating ITPU (Information-Theoretic Processing) ===\n")
        
        source = self.workspace / "ITPU"
        dest = self.target / "infrastructure" / "itpu"
        
        self.copy_with_git_history(
            source,
            dest,
            "Integrated ITPU for constraint health metrics and coherence measurement"
        )
        
        # Create README
        readme_content = """# ITPU - Information-Theoretic Processing Unit

## Purpose
Real-time constraint health metrics and coherence measurement for the Resonance Engine.

## Role in the Stack
ITPU provides the computational substrate for measuring how well constraints are being
maintained throughout the compilation process. It answers: "Is this constraint healthy?"

## Key Components
- Constraint health monitoring
- Coherence metrics
- Information flow analysis
- Real-time diagnostics

## Integration
ITPU powers the Resonance Engine compiler by providing continuous feedback about
whether constraints are enabling coherence or breaking down.

## Usage
```python
from infrastructure.itpu import ConstraintHealthMonitor

monitor = ConstraintHealthMonitor()
health = monitor.measure_constraint_health(constraint_id)
```

## See Also
- Main documentation: docs/api/ITPU_API.md
- Examples: examples/basic/constraint_health.py
"""
        
        if not self.dry_run:
            readme_path = dest / "README.md"
            readme_path.write_text(readme_content)
        
        self.log_operation("create_readme", {
            "description": "Created ITPU README",
            "path": str(dest / "README.md")
        })
    
    def integrate_geometric_plasticity(self):
        """Integrate Geometric-Plasticity repository"""
        print("\n=== Integrating Geometric-Plasticity (Ringing Diagnostics) ===\n")
        
        source = self.workspace / "Geometric-Plasticity"
        dest = self.target / "infrastructure" / "geometric_plasticity"
        
        self.copy_with_git_history(
            source,
            dest,
            "Integrated Geometric-Plasticity for ringing detection and spectral stability analysis"
        )
        
        readme_content = """# Geometric Plasticity - Ringing Diagnostics

## Purpose
Detect when Builder/Skeptic oscillation is productive versus degenerate through
spectral stability analysis and phase transition detection.

## Role in the Stack
Geometric-Plasticity provides diagnostics that determine whether the constraint-driven
development process is converging toward coherence or stuck in unproductive patterns.

## Key Components
- Spectral stability analysis
- Phase transition detection
- Oscillation pattern recognition
- Ringing diagnostics

## Integration
Used as quality gates in the compilation process to ensure that Builder/Skeptic
dialogue is genuinely improving the experiment design.

## Usage
```python
from infrastructure.geometric_plasticity import RingingDetector

detector = RingingDetector()
is_productive = detector.analyze_oscillation(history)
```

## See Also
- Main documentation: docs/api/GEOMETRIC_PLASTICITY_API.md
- Examples: examples/basic/ringing_detection.py
"""
        
        if not self.dry_run:
            readme_path = dest / "README.md"
            readme_path.write_text(readme_content)
        
        self.log_operation("create_readme", {
            "description": "Created Geometric-Plasticity README",
            "path": str(dest / "README.md")
        })
    
    def integrate_just_asking(self):
        """Integrate JustAsking repository"""
        print("\n=== Integrating JustAsking (Multi-AI Orchestration) ===\n")
        
        source = self.workspace / "JustAsking"
        dest = self.target / "infrastructure" / "orchestration"
        
        self.copy_with_git_history(
            source,
            dest,
            "Integrated JustAsking for multi-AI coordination and architectural diversity"
        )
        
        readme_content = """# Orchestration - Multi-AI Coordination

## Purpose
Multi-AI coordination using architectural diversity to break premature convergence
and ensure robust validation.

## Role in the Stack
Orchestration provides the proven fan-out pattern for querying multiple AI architectures
in parallel, enabling genuine disagreement and consensus analysis.

## Key Components
- Multi-AI fan-out patterns
- Architectural diversity protocols
- Consensus analysis
- Dissent tracking

## Integration
Powers the multi-architecture validation in bundles, ensuring that experimental
designs are robust across different AI perspectives.

## Usage
```python
from infrastructure.orchestration import MultiAIOrchestrator

orchestrator = MultiAIOrchestrator(architectures=['claude', 'gpt4', 'gemini'])
results = orchestrator.fan_out(question)
consensus = orchestrator.analyze_consensus(results)
```

## See Also
- Main documentation: docs/api/ORCHESTRATION_API.md
- Examples: examples/advanced/multi_ai_compilation.py
"""
        
        if not self.dry_run:
            readme_path = dest / "README.md"
            readme_path.write_text(readme_content)
        
        self.log_operation("create_readme", {
            "description": "Created Orchestration README",
            "path": str(dest / "README.md")
        })
    
    def organize_core(self):
        """Organize core Resonance Engine components"""
        print("\n=== Organizing Core Resonance Engine ===\n")
        
        # This assumes the target IS the Resonance-Engine repo
        # We're just organizing existing content
        
        readme_content = """# Core - Discovery Compiler

## Purpose
Transform intuitive research questions into rigorous, falsifiable experiments through
constraint-based compilation.

## Architecture
The core compiler uses four roles in constraint-driven development:
- **Builder**: Proposes experiment designs
- **Skeptic**: Challenges and stress-tests proposals
- **Auditor**: Ensures standards compliance (RM-01, RM-02, RM-03)
- **Operator**: Executes validated experiments

## Principles
**"Coherence is earned by constraints"**

Constraints aren't limitations—they're the medium that enables coherent structure
to emerge from the Builder/Skeptic oscillation.

## Key Components
- Constraint-based compilation engine
- Role system (Builder/Skeptic/Auditor/Operator)
- Bundle generation
- Standards enforcement

## Integration
The core compiler orchestrates all other infrastructure components:
- Uses ITPU for constraint health monitoring
- Uses Geometric-Plasticity for ringing detection
- Uses Orchestration for multi-AI validation

## Usage
```python
from core import ResonanceEngine

engine = ResonanceEngine()
bundle = engine.compile(
    question="Does geometric resonance predict consciousness?",
    standards=['RM-01', 'RM-02', 'RM-03']
)
```

## See Also
- Main documentation: docs/architecture/SYSTEM_OVERVIEW.md
- Examples: examples/basic/simple_bundle.py
"""
        
        core_path = self.target / "core"
        if not self.dry_run:
            readme_path = core_path / "README.md"
            readme_path.write_text(readme_content)
        
        self.log_operation("create_readme", {
            "description": "Created Core README",
            "path": str(core_path / "README.md")
        })
    
    def create_main_readme(self):
        """Create the main repository README"""
        print("\n=== Creating Main README ===\n")
        
        readme_content = """# Resonance Engine

**Discovery compiler that makes human-AI cognition more coherent than either alone**

## What is Resonance Engine?

Resonance Engine transforms intuitive research questions into rigorous, falsifiable experiments through constraint-based compilation. It's infrastructure that uses constraints not to limit but to enable—making distributed cognition between humans and AI genuinely more capable than either alone.

## The Cognitive Infrastructure Stack

Resonance Engine integrates four components into a unified system:

1. **Resonance Engine (Core)**: Discovery compiler
   - Transforms questions into experiments
   - Enforces epistemic rigor (RM-01, RM-02, RM-03)
   - Produces "bundles" (complete, executable experiments)

2. **ITPU**: Information-theoretic processing
   - Real-time constraint health metrics
   - Coherence measurement
   - Computational substrate for quality monitoring

3. **Geometric-Plasticity**: Ringing diagnostics
   - Detects productive vs degenerate oscillation
   - Spectral stability analysis
   - Quality gates for compilation

4. **Orchestration**: Multi-AI coordination
   - Architectural diversity for robust validation
   - Parallel perspectives
   - Consensus and dissent analysis

## Core Principle

**"Coherence is earned by constraints"**

Constraints aren't limitations—they're the medium that enables coherent structure to emerge. Just as a musical instrument needs constraints (strings under tension, resonant chamber) to produce coherent sound, human-AI cognition needs constraints to produce coherent insights.

## Quick Start

### Installation

```bash
git clone https://github.com/YourUsername/Resonance-Engine.git
cd Resonance-Engine
pip install -e .
```

### Your First Bundle in 30 Minutes

```python
from core import ResonanceEngine

# Initialize the engine
engine = ResonanceEngine()

# Ask your question
bundle = engine.compile(
    question="Your research question here",
    standards=['RM-01', 'RM-02', 'RM-03']
)

# Get a complete, executable experiment
bundle.save('bundles/my_first_bundle/')
```

See `bundles/0001_rfo_ringing_wedge/` for a complete example proving the stack works.

## Philosophy

This project exists to democratize rigorous research methodology for people without institutional access. It proves that:
- Constraints enable rather than limit
- Distributed cognition can be genuinely additive
- Epistemic rigor is accessible to anyone
- Infrastructure can make us collectively smarter

## Architecture

```
Question → Compilation → Bundle
    ↓          ↓          ↓
  ITPU    Geometric  Executable
  metrics  Plasticity Experiment
           diagnostics
```

Each bundle contains:
- Falsifiable claim (≤3 sentences)
- Operationalized observables
- Preregistered parameters
- Hard-gate stopping rules
- Complete execution code

## Bundle 0001: Proof of Concept

Our first bundle validates the entire stack by compiling a real experiment from Resonance Geometry theory. It demonstrates:
- Constraint-driven compilation works
- Multi-AI orchestration produces robust designs
- Infrastructure enables insights neither human nor AI could reach alone

See `bundles/0001_rfo_ringing_wedge/README.md` for details.

## Contributing

We're building infrastructure for collective intelligence. Contributions welcome in:
- New bundles (experiments from any field)
- Infrastructure improvements
- Documentation and tutorials
- Standards refinement

See `CONTRIBUTING.md` for guidelines.

## Documentation

- **Architecture**: `docs/architecture/SYSTEM_OVERVIEW.md`
- **Tutorials**: `docs/tutorials/GETTING_STARTED.md`
- **API Reference**: `docs/api/`
- **Examples**: `examples/`

## Support

- **GitHub Issues**: Technical problems
- **Discussions**: Questions and ideas
- **Email**: [Your email for private inquiries]

## License

[Your chosen license]

## Acknowledgments

This work stands on shoulders:
- Information theory (Shannon, Kolmogorov)
- Distributed cognition research
- Open science movement
- Everyone who believes rigorous research should be accessible to all

---

**Remember**: This is infrastructure that should make human-AI cognition more coherent than either alone. Every constraint, every component, every bundle serves that goal.
"""
        
        if not self.dry_run:
            readme_path = self.target / "README.md"
            readme_path.write_text(readme_content)
        
        self.log_operation("create_readme", {
            "description": "Created main README",
            "path": str(self.target / "README.md")
        })
    
    def create_bundle_readme(self):
        """Create README for bundles directory"""
        print("\n=== Creating Bundles README ===\n")
        
        readme_content = """# Bundles - Compiled Experiments

## What is a Bundle?

A bundle is a complete, self-contained experiment compiled by the Resonance Engine. Each bundle contains everything needed to execute and validate a falsifiable claim.

## Bundle Structure

```
bundle_name/
├── CLAIM.md                    # Falsifiable claim (≤3 sentences)
├── OPERATIONALIZE.md           # Exact observables and outputs
├── PREREG.yaml                 # Locked parameters and sweep
├── NULLS.md                    # Numeric rejection thresholds
├── COHERENCE_METRICS.yaml      # Constraint health metrics
├── src/                        # Execution code
│   ├── __init__.py
│   └── experiment_*.py
├── tests/                      # Validation tests
└── README.md                   # Bundle-specific documentation
```

## Bundle 0001: The First Experiment

Bundle 0001 (`0001_rfo_ringing_wedge/`) proves the entire stack works by compiling a real experiment from Resonance Geometry theory. It demonstrates:

- **Constraint-Driven Compilation**: Question → rigorous experiment
- **Multi-AI Orchestration**: Architectural diversity for robust design
- **Infrastructure Integration**: All four components working together
- **Epistemic Rigor**: RM-01, RM-02, RM-03 standards enforced

## Creating Your Own Bundle

```python
from core import ResonanceEngine

engine = ResonanceEngine()
bundle = engine.compile(
    question="Your research question",
    standards=['RM-01', 'RM-02', 'RM-03'],
    constraints={
        'max_parameters': 5,
        'min_effect_size': 0.3,
        'require_preregistration': True
    }
)
```

## Bundle Validation

Every bundle must pass:
1. Standards compliance (RM-01, RM-02, RM-03)
2. Constraint health checks (via ITPU)
3. Ringing diagnostics (via Geometric-Plasticity)
4. Multi-architecture consensus (via Orchestration)
5. Execution tests
6. Hard-gate validation

## Philosophy

Bundles embody "coherence earned by constraints":
- Pre-registered to prevent p-hacking
- Falsifiable claims with numeric thresholds
- Complete execution code for reproducibility
- Hard gates that cannot be circumvented

Each bundle is a proof: rigorous research is possible outside institutions.

## Contributing Bundles

We welcome bundles from any field:
- Physics and natural sciences
- Social sciences
- Psychology and cognition
- Technology and engineering
- Interdisciplinary questions

See `CONTRIBUTING.md` for bundle submission guidelines.
"""
        
        bundles_path = self.target / "bundles"
        if not self.dry_run:
            readme_path = bundles_path / "README.md"
            readme_path.write_text(readme_content)
        
        self.log_operation("create_readme", {
            "description": "Created Bundles README",
            "path": str(bundles_path / "README.md")
        })
    
    def save_log(self):
        """Save operations log to JSON"""
        if not self.dry_run:
            with open(self.log_file, 'w') as f:
                json.dump(self.operations_log, f, indent=2)
            print(f"\n✓ Operations log saved to {self.log_file}")
    
    def run(self):
        """Execute the full organization process"""
        try:
            print("\n" + "="*60)
            print("RESONANCE ENGINE REPOSITORY ORGANIZATION")
            print("="*60)
            
            if self.dry_run:
                print("\n*** DRY RUN MODE - No changes will be made ***\n")
            
            self.verify_prerequisites()
            self.create_directory_structure()
            self.integrate_itpu()
            self.integrate_geometric_plasticity()
            self.integrate_just_asking()
            self.organize_core()
            self.create_main_readme()
            self.create_bundle_readme()
            self.save_log()
            
            print("\n" + "="*60)
            print("✓ ORGANIZATION COMPLETE")
            print("="*60)
            print(f"\nTarget repository: {self.target}")
            print(f"Operations logged: {len(self.operations_log)}")
            
            if not self.dry_run:
                print("\nNext steps:")
                print("1. Review the changes")
                print("2. Run tests: pytest tests/")
                print("3. Check constraint health")
                print("4. Commit with descriptive message")
                print("5. Create Bundle 0002 to prove the stack")
            
        except ResonanceOrganizerError as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Organize four repositories into unified Resonance Engine structure"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        required=True,
        help="Path to workspace containing all four repositories"
    )
    parser.add_argument(
        "--target",
        type=Path,
        required=True,
        help="Path to target Resonance-Engine repository"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    organizer = ResonanceOrganizer(
        workspace=args.workspace,
        target=args.target,
        dry_run=args.dry_run
    )
    organizer.run()


if __name__ == "__main__":
    main()
