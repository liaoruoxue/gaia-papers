"""TPO: Target Policy Optimization.

Formalisation of arXiv:2604.06159. The source artifact bundled in this
package is the title-level stub (title + arXiv link + four-keyword list +
status line); the full PDF body was not available at formalisation time, so
only the title-level thesis claim, its companion method claim, and the
four listed keyword topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    keyword_cross_entropy,
    keyword_gradient_conflict,
    keyword_grpo_alternative,
    keyword_rl_training,
    target_policy_is_the_optimisation_object,
    tpo_realises_target_policy_optimization,
)

__all__ = [
    "motivation",
    "target_policy_is_the_optimisation_object",
    "tpo_realises_target_policy_optimization",
    "keyword_rl_training",
    "keyword_grpo_alternative",
    "keyword_cross_entropy",
    "keyword_gradient_conflict",
]
