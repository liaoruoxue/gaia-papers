"""Layer 2 semantic package for Anthropic 2026 'Teaching Claude Why' blog."""

import sys, os, importlib

# Make sibling Layer 1 package importable when running from a workspace
# layout where the formalize package lives outside this tree
# (agent-docs/gaia-packages/anthropic2026-teaching-claude-why-gaia).
_here = os.path.dirname(os.path.abspath(__file__))
_candidates = [
    # Sibling under gaia-papers/semantic (mirrors joint-grpo-fragility pattern)
    os.path.abspath(os.path.join(_here, "..", "..", "..", "anthropic2026-teaching-claude-why-gaia", "src")),
    # Cross-repo: agent-docs gaia-packages
    os.path.expanduser("~/Code/agent-docs/gaia-packages/anthropic2026-teaching-claude-why-gaia/src"),
]
for p in _candidates:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

# Eagerly load Layer 1 so its claims are registered in the global Gaia
# knowledge index (required for `gaia infer --depth 1`).
for sub in ("paper_anthropic2026", "priors"):
    try:
        importlib.import_module(f"anthropic2026_teaching_claude_why.{sub}")
    except ImportError:
        pass

from . import motivation, s2_strategies, priors

__all__ = ["motivation", "s2_strategies", "priors"]
