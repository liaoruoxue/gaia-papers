"""How are AI agents used? Evidence from 177,000 MCP tools.

Formalisation of arXiv:2603.23802. The source artifact bundled in this package
is the abstract-level stub (title + arXiv link + GitHub link + keyword list +
two-sentence abstract); the full PDF body was not available at formalisation
time, so only the abstract conclusions and the listed keyword topics are
extracted as claims.
"""

from . import motivation

# Headline exported conclusions -- the package's external API.
from .motivation import (
    empirical_177k_tools_analyzed,
    evidence_based_scale_study,
    keyword_agent_consequentiality,
    keyword_agentic_action,
    keyword_high_stakes_ai_deployment,
    keyword_mcp_server_usage_trends,
    keyword_tool_ecosystem_monitoring,
)

__all__ = [
    "motivation",
    "empirical_177k_tools_analyzed",
    "evidence_based_scale_study",
    "keyword_agentic_action",
    "keyword_tool_ecosystem_monitoring",
    "keyword_mcp_server_usage_trends",
    "keyword_agent_consequentiality",
    "keyword_high_stakes_ai_deployment",
]
