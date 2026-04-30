"""Motivation: how AI agents are actually used at scale.

Formalisation of arXiv:2603.23802 ("How are AI agents used? Evidence from
177,000 MCP tools"). The source artifact in this package is a thin stub
(title + arXiv link + GitHub link + keyword list + a two-sentence abstract);
no PDF body is available. Therefore only the abstract-level conclusions and
the explicit keyword claims are formalised here.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

mcp_ecosystem_setting = setting(
    "The Model Context Protocol (MCP) is an open protocol that exposes external "
    "tools (file systems, browsers, APIs, databases, code interpreters, ...) to "
    "LLM-based agents through a standardised JSON-RPC interface. An *MCP tool* is "
    "a single callable endpoint published by an MCP server; an MCP server may "
    "expose many tools. The public MCP server registry "
    "(https://github.com/modelcontextprotocol/servers) and downstream catalogues "
    "make tool metadata and (where instrumented) usage telemetry observable at "
    "scale.",
    title="MCP tool ecosystem (formal setting)",
)

study_scope = setting(
    "The study scope is the population of MCP tools observable at the time of "
    "data collection -- approximately 177,000 distinct tools across the public "
    "MCP server ecosystem. 'Use' refers to invocations of these tools by AI "
    "agents in deployed (non-toy) settings, as evidenced by the metadata and "
    "telemetry exposed by the surveyed servers.",
    title="Study population: 177,000 MCP tools",
)

# ---------------------------------------------------------------------------
# Headline abstract claims (the 2 sentences of the abstract)
# ---------------------------------------------------------------------------

empirical_177k_tools_analyzed = claim(
    "The study performs an **empirical analysis of 177,000 MCP tools** observed "
    "in real-world AI-agent deployments, rather than a synthetic benchmark or "
    "lab-scale evaluation.",
    title="177,000 MCP tools analysed empirically",
    metadata={"source": "artifacts/2603.23802-mcp-tools-evidence.md (abstract, sentence 1)"},
)

evidence_based_scale_study = claim(
    "The work is an **evidence-based, at-scale study of how agents actually use "
    "tools** in production -- i.e. the unit of analysis is observed tool-call "
    "behaviour aggregated across the ecosystem, not designer intent or "
    "advertised tool capability.",
    title="Evidence-based at-scale study of agent tool use",
    metadata={"source": "artifacts/2603.23802-mcp-tools-evidence.md (abstract, sentence 2)"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 5 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim of the form "this paper studies / provides evidence on X".
# ---------------------------------------------------------------------------

keyword_agentic_action = claim(
    "The work provides empirical evidence on **agentic action** -- i.e. the "
    "actual actions (tool invocations) issued by LLM-based agents in the wild, "
    "as opposed to the actions designers or benchmarks assume agents take.",
    title="Keyword: agentic action",
    metadata={"keyword_index": 1, "source": "artifacts/2603.23802-mcp-tools-evidence.md (keywords)"},
)

keyword_tool_ecosystem_monitoring = claim(
    "The work contributes to **tool ecosystem monitoring** -- characterising the "
    "MCP-tool ecosystem (which tools exist, how many, by whom) and tracking it "
    "at scale, providing the substrate for longitudinal observation.",
    title="Keyword: tool ecosystem monitoring",
    metadata={"keyword_index": 2, "source": "artifacts/2603.23802-mcp-tools-evidence.md (keywords)"},
)

keyword_mcp_server_usage_trends = claim(
    "The work surfaces **MCP server usage trends** -- aggregate statistics on "
    "which MCP servers (and which of their tools) are invoked, how often, and "
    "how that distribution shifts.",
    title="Keyword: MCP server usage trends",
    metadata={"keyword_index": 3, "source": "artifacts/2603.23802-mcp-tools-evidence.md (keywords)"},
)

keyword_agent_consequentiality = claim(
    "The work provides evidence on **agent consequentiality** -- i.e. the "
    "degree to which agent tool invocations have real-world side effects "
    "(state-changing, irreversible, or externally visible operations) versus "
    "being read-only / advisory.",
    title="Keyword: agent consequentiality",
    metadata={"keyword_index": 4, "source": "artifacts/2603.23802-mcp-tools-evidence.md (keywords)"},
)

keyword_high_stakes_ai_deployment = claim(
    "The work informs **high-stakes AI deployment** -- by documenting which "
    "tool categories (e.g. financial, infrastructure, communication) agents are "
    "actually being wired into, the study identifies where AI-agent tool use "
    "carries elevated operational or societal risk.",
    title="Keyword: high-stakes AI deployment",
    metadata={"keyword_index": 5, "source": "artifacts/2603.23802-mcp-tools-evidence.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two abstract sentences jointly grant evidence to each of the five
# keyword-topic claims: an empirical, at-scale evidence-based study of agent
# tool use is *the kind of work* that supplies evidence on agentic action,
# ecosystem monitoring, usage trends, consequentiality, and high-stakes
# deployment.

strat_evidence_for_agentic_action = support(
    [empirical_177k_tools_analyzed, evidence_based_scale_study],
    keyword_agentic_action,
    background=[mcp_ecosystem_setting, study_scope],
    reason=(
        "An empirical analysis of 177,000 MCP tools "
        "(@empirical_177k_tools_analyzed) framed as an evidence-based study of "
        "real-world agent tool use (@evidence_based_scale_study) directly "
        "observes agentic action -- the actual invocations agents emit in the "
        "wild. The MCP setting (@mcp_ecosystem_setting) and the population "
        "scope (@study_scope) make those invocations observable. Hence the "
        "work supplies evidence on agentic action."
    ),
    prior=0.9,
)

strat_evidence_for_ecosystem_monitoring = support(
    [empirical_177k_tools_analyzed, evidence_based_scale_study],
    keyword_tool_ecosystem_monitoring,
    background=[mcp_ecosystem_setting, study_scope],
    reason=(
        "Surveying 177,000 MCP tools (@empirical_177k_tools_analyzed) at the "
        "ecosystem level (@study_scope) is, definitionally, tool ecosystem "
        "monitoring: the work enumerates and characterises the population of "
        "tools available within the MCP setting (@mcp_ecosystem_setting). "
        "Combined with the evidence-based posture "
        "(@evidence_based_scale_study), this licenses the keyword claim."
    ),
    prior=0.93,
)

strat_evidence_for_usage_trends = support(
    [empirical_177k_tools_analyzed, evidence_based_scale_study],
    keyword_mcp_server_usage_trends,
    background=[mcp_ecosystem_setting],
    reason=(
        "Once the population is enumerated (@empirical_177k_tools_analyzed) "
        "and analysed empirically (@evidence_based_scale_study), aggregate "
        "usage statistics of MCP servers and their tools fall out as a direct "
        "by-product. The MCP protocol (@mcp_ecosystem_setting) exposes the "
        "telemetry needed to compute those trends."
    ),
    prior=0.85,
)

strat_evidence_for_consequentiality = support(
    [empirical_177k_tools_analyzed, evidence_based_scale_study],
    keyword_agent_consequentiality,
    background=[mcp_ecosystem_setting, study_scope],
    reason=(
        "Classifying the 177,000 surveyed tools (@empirical_177k_tools_analyzed, "
        "@study_scope) by their effect type (read-only vs state-changing vs "
        "external-side-effect) and weighting by observed invocation frequency "
        "(@evidence_based_scale_study) is the standard way to quantify agent "
        "consequentiality from MCP metadata (@mcp_ecosystem_setting)."
    ),
    prior=0.8,
)

strat_evidence_for_high_stakes = support(
    [keyword_agent_consequentiality, keyword_mcp_server_usage_trends],
    keyword_high_stakes_ai_deployment,
    background=[study_scope],
    reason=(
        "Knowing which tools have material side effects "
        "(@keyword_agent_consequentiality) **and** which of them are actually "
        "popular with agents (@keyword_mcp_server_usage_trends), evaluated over "
        "the full surveyed population (@study_scope), pinpoints the subset of "
        "tool categories where AI-agent deployment is high-stakes -- precisely "
        "the input a deployer needs."
    ),
    prior=0.85,
)

__all__ = [
    "mcp_ecosystem_setting",
    "study_scope",
    "empirical_177k_tools_analyzed",
    "evidence_based_scale_study",
    "keyword_agentic_action",
    "keyword_tool_ecosystem_monitoring",
    "keyword_mcp_server_usage_trends",
    "keyword_agent_consequentiality",
    "keyword_high_stakes_ai_deployment",
]
