"""Layer 2 — MCP Tools: Cross-Platform Large-N Evidence (2603.23802)

First large-N empirical study of agent-tool usage: 177k tools across 19k MCP servers.
Reveals software dominance, action-tool growth (27%→65%), AI co-authorship trend.
"""

from gaia.lang import claim, setting

large_n_tool_evidence = claim(
    "First cross-platform, large-N dataset of agent tool usage: 177,000 "
    "MCP tools across 19,000 servers, spanning 16 months. This provides "
    "the first empirical baseline for what agents ACTUALLY do — as opposed "
    "to what papers claim agents can do. The dataset is the core contribution: "
    "it enables longitudinal tracking of agent capability evolution.",
    title="177k tools / 19k servers = first large-N empirical baseline for agent tooling",
    aggregated_from=[
        "claim_evidence_gap", "claim_contribution_dataset",
        "claim_contribution_timetrend",
    ],
)

software_dominates_action_growing = claim(
    "Two headline trends: (1) Software development tools dominate — 67% of "
    "tools and 90% of downloads are dev-related (IDEs, linters, package "
    "managers, git wrappers). (2) Action-tool share grew from 27% to 65% "
    "over 16 months — agents are increasingly being given tools that DO "
    "things (run code, deploy, modify files) rather than just READ things "
    "(search, summarize). This shift toward action has direct governance "
    "implications: higher stakes, harder to audit.",
    title="Software dominates (67%); action-tool share grew 27%→65% in 16 months",
    aggregated_from=[
        "claim_finding_software_dominates", "claim_finding_action_share_growth",
        "claim_finding_action_stakes_distribution",
    ],
)

ai_coauthorship_explosion = claim(
    "AI co-authorship of MCP servers rose from 6% to 62% in 13 months. "
    "This suggests a recursive dynamic: agents are building tools for other "
    "agents. If this trend continues, the majority of agent-facing tools "
    "will be agent-authored within 18 months — raising questions about "
    "tool quality assurance, security, and the 'self-improvement' feedback "
    "loop where agents modify their own tool ecosystem.",
    title="AI co-authorship of MCP tools: 6%→62% in 13 months",
    aggregated_from=[
        "claim_finding_ai_coauthorship_growth",
        "claim_self_improvement_risk",
    ],
)

geographic_concentration = claim(
    "~50% of agent-tool usage geolocates to the United States. This "
    "concentration has regulatory implications: US export controls and "
    "AI governance decisions will disproportionately shape the agent-tool "
    "ecosystem globally.",
    title="~50% US concentration of agent-tool usage",
    aggregated_from=["claim_finding_us_concentration"],
)

# ── Boundary ──

mcp_only_platform = claim(
    "Data is limited to the MCP ecosystem. Other tool protocols (function "
    "calling, plugin systems) are not captured. MCP may over-represent "
    "developer-oriented tools and under-represent enterprise/proprietary "
    "tool usage behind firewalls.",
    title="Limitation: MCP ecosystem only — not all agent tooling",
)
