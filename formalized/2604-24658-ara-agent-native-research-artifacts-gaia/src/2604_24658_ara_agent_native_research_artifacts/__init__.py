"""ARA: Agent-Native Research Artifacts.

Formalisation of arXiv:2604.24658. The source artifact bundled in this
package is the title-level stub (title + arXiv link + three-keyword list +
status line); the full PDF body was not available at formalisation time, so
only the title-level thesis claim, its companion framework claim, and the
three listed keyword topics are extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    ara_realises_agent_native_artifacts,
    artifacts_should_be_agent_native,
    keyword_arm,
    keyword_knowledge_representation,
    keyword_paper_agentification,
)

__all__ = [
    "motivation",
    "artifacts_should_be_agent_native",
    "ara_realises_agent_native_artifacts",
    "keyword_paper_agentification",
    "keyword_arm",
    "keyword_knowledge_representation",
]
