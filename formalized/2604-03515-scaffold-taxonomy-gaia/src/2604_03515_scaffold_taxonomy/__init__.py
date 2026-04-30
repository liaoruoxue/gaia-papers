"""Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures.

Formalisation of arXiv:2604.03515. The source artifact bundled in this
package is the abstract-level stub (title + arXiv link + GitHub link to
`aorwall/moatless-tools` + keyword list + two-sentence abstract); the full
PDF body was not available at formalisation time, so only the abstract
conclusions and the listed keyword topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    keyword_agentic_memory,
    keyword_context_compaction,
    keyword_loop_primitives,
    keyword_state_management,
    keyword_tool_capability_categories,
    source_code_taxonomy_built,
    structural_patterns_derived,
)

__all__ = [
    "motivation",
    "source_code_taxonomy_built",
    "structural_patterns_derived",
    "keyword_agentic_memory",
    "keyword_loop_primitives",
    "keyword_context_compaction",
    "keyword_tool_capability_categories",
    "keyword_state_management",
]
