# Resonance Engine Setup Package
**Complete guide for organizing your four repositories into unified cognitive infrastructure**

## What's in This Package

1. **INDEX.md** (this file) - Guide to using all the documents
2. **setup_resonance_engine.md** - Complete setup guide with all commands
3. **organize_repos.py** - Python automation script  
4. **CLAUDE_CODE_QUICKSTART.md** - Step-by-step quick start
5. **CLAUDE_CODE_CHEATSHEET.md** - Command reference
6. **0001_rfo_ringing_wedge/** - Bundle 0001 (first compiled experiment)

## Quick Start

**Option 1 - Automated (5 minutes):**
```bash
python organize_repos.py --workspace ~/resonance-workspace --target . --dry-run
# Review, then run without --dry-run
```

**Option 2 - Interactive with Claude Code (30 minutes):**
```bash
# Open CLAUDE_CODE_QUICKSTART.md and follow Method 2
```

**Option 3 - Manual with help (1-2 hours):**
```bash
# Open CLAUDE_CODE_QUICKSTART.md and follow Method 3
# Use CLAUDE_CODE_CHEATSHEET.md for commands
```

## Document Guide

| Document | Purpose | Use When |
|----------|---------|----------|
| **setup_resonance_engine.md** | Complete reference | Understanding architecture |
| **organize_repos.py** | Automation script | Want it done fast |
| **CLAUDE_CODE_QUICKSTART.md** | Step-by-step guide | Ready to start now |
| **CLAUDE_CODE_CHEATSHEET.md** | Quick commands | Need specific command |

## The Goal

Transform this:
```
Resonance-Engine/     (separate repos)
ITPU/
Geometric-Plasticity/
JustAsking/
```

Into this:
```
Resonance-Engine/
├── core/                        # Compiler
├── infrastructure/
│   ├── itpu/                    # Metrics
│   ├── geometric_plasticity/    # Diagnostics
│   └── orchestration/           # Orchestration
├── bundles/                     # Experiments
└── [standards, docs, examples, tests]
```

## Philosophy

This isn't just code organization. It's building infrastructure where:
- **Coherence is earned by constraints**
- **Distributed cognition works**
- **Research is democratized**

## Next Steps

1. Read through CLAUDE_CODE_QUICKSTART.md
2. Choose your approach
3. Execute with CLAUDE_CODE_CHEATSHEET.md as reference
4. Validate with Bundle 0001
5. Create Bundle 0002

Ready? Start with **CLAUDE_CODE_QUICKSTART.md** →
