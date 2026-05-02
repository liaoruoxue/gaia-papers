"""AHE: Agentic Harness Engineering.

Formalisation of arXiv:2604.25850. The source artifact bundled in this
package is the title-level stub (title + arXiv link + three-keyword list +
status line); the full PDF body was not available at formalisation time, so
only the title-level thesis claim, its companion framework claim, and the
three listed keyword topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    ahe_realises_harness_engineering,
    harness_is_the_engineering_object,
    keyword_harness_design,
    keyword_observability,
    keyword_self_evolution,
)

__all__ = [
    "motivation",
    "harness_is_the_engineering_object",
    "ahe_realises_harness_engineering",
    "keyword_harness_design",
    "keyword_self_evolution",
    "keyword_observability",
]
