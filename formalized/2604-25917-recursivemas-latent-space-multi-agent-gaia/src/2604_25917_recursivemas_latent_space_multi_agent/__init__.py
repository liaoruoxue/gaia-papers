"""RecursiveMAS: Latent-Space Multi-Agent.

Formalisation of arXiv:2604.25917. The source artifact bundled in this
package is the title-level stub (title + arXiv link + three-keyword list +
status line); the full PDF body was not available at formalisation time,
so only the title-level thesis claim, its companion framework claim, and
the three listed keyword topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    keyword_latent_communication,
    keyword_multi_agent,
    keyword_recursive,
    latent_space_is_the_mas_channel,
    recursivemas_realises_recursive_latent_mas,
)

__all__ = [
    "motivation",
    "latent_space_is_the_mas_channel",
    "recursivemas_realises_recursive_latent_mas",
    "keyword_multi_agent",
    "keyword_latent_communication",
    "keyword_recursive",
]
