"""LEAS+DART: Reasoning and Tool-use Compete in Agentic RL.

Formalisation of arXiv:2602.00994. The source artifact bundled in this
package is the title-level stub (title + arXiv link + three-keyword list +
status line); the full PDF body was not available at formalisation time, so
only the title-level thesis claim, its companion remedy claim, and the three
listed keyword topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    keyword_dual_lora,
    keyword_gradient_conflict,
    keyword_rl_training,
    leas_dart_resolves_competition,
    reasoning_and_tooluse_compete,
)

__all__ = [
    "motivation",
    "reasoning_and_tooluse_compete",
    "leas_dart_resolves_competition",
    "keyword_rl_training",
    "keyword_gradient_conflict",
    "keyword_dual_lora",
]
