"""DeepSeek Visual Primitives -- thinking with visual primitives.

Formalisation of the GitHub repository
https://github.com/deepseek-ai/Thinking-with-Visual-Primitives. The source
artifact bundled in this package is the title-level stub (title + GitHub
link + three-keyword list + status line); the full README, paper, and code
were not available at formalisation time, so only the title-level thesis
claim, its companion realisation claim, and the three listed keyword
topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    deepseek_visual_primitives_realises_thesis,
    keyword_multimodal,
    keyword_reference_gap,
    keyword_visual_reasoning,
    thinking_with_visual_primitives_thesis,
)

__all__ = [
    "motivation",
    "thinking_with_visual_primitives_thesis",
    "deepseek_visual_primitives_realises_thesis",
    "keyword_multimodal",
    "keyword_visual_reasoning",
    "keyword_reference_gap",
]
