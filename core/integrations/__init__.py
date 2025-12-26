"""
Integration Adapters

Clean interfaces to upstream repositories for diversity actuation, metrics
computation, and diagnostic analysis.

v0 Policy: Adapters + links only. No upstream code imported.

Available adapters:
- justasking_adapter: Diversity fan-out across models
- itpu_adapter: Information-theoretic metrics (MI, windowed MI)
- gp_adapter: Geometric diagnostics (ringing detection, curvature)

See docs/INTEGRATIONS.md for integration strategy and roadmap.
"""

__all__ = [
    "justasking_adapter",
    "itpu_adapter",
    "gp_adapter",
]
