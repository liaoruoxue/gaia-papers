"""Motivation: Why monitor AI agent tools?

Section 1 (Introduction) of Stein 2026 [@Stein2026]. Motivates the central
research gap: AI agents are rapidly being deployed via tools that read and
modify external environments, but developers, researchers, and governments
lack a system-level view of what tools exist, what tasks they enable, and
how their popularity is evolving. Existing studies focus on chatbot LLM
usage and miss the agent-tool layer that defines the agent's action space.

The paper proposes monitoring publicly published Model Context Protocol
(MCP) servers as an empirical proxy: harvest tool descriptions from
public repositories, classify each tool by direct impact (perception /
reasoning / action) and task domain (O*NET), and observe how the
ecosystem evolves over a 16-month panel.
"""

from gaia.lang import claim, setting, question

# ---------------------------------------------------------------------------
# Background settings (definitional / framing)
# ---------------------------------------------------------------------------

setup_ai_agent_definition = setting(
    "**AI agent (working definition).** An AI agent is a system built on a "
    "Large Language Model (LLM), augmented with memory components and "
    "provided with access to *external tools*. Tools are functions the "
    "agent can call to access, analyse, or modify external environments "
    "(e.g. a tool to send an email via Google MCP, search Amazon, or "
    "execute a financial transaction via Coinbase MCP). Unlike a standalone "
    "LLM that can only generate text, an agent can autonomously act in the "
    "world through these tools, often with little human oversight "
    "[@Stein2026; @RussellNorvig2020].",
    title="Setup: AI agent = LLM + memory + tools",
)

setup_mcp_definition = setting(
    "**Model Context Protocol (MCP).** MCP is an open standard launched in "
    "November 2024 in which a lightweight server program exposes one or "
    "more *tools* (typed function endpoints with name, description, and "
    "input schema) to an AI agent. Each MCP server packages tools that "
    "give an agent access to a particular environment -- a data source, an "
    "API, a browser, etc. As of H1/2025 every agent-related repository in "
    "GitHub's top 10 new repositories built MCP infrastructure or "
    "integrated MCP, and major agent providers (OpenAI, Anthropic, Google) "
    "support MCP integration; thus MCP is the predominant open protocol "
    "for agent tools at the time of the study [@Stein2026].",
    title="Setup: MCP is the dominant open protocol for AI agent tools",
)

setup_action_space = setting(
    "**Action space.** Following prior risk-framework literature "
    "[@Kasirzadeh2025; @Chan2023Harms; @Cihon2025Autonomy], an AI agent's "
    "action space is the set of actions it can take in the world. Tools "
    "*define* the action space: an LLM-only system (no tools) has an "
    "empty action space and can only emit text, while an agent with a "
    "browser tool, a code-execution tool, and a payments tool has a much "
    "larger action space. Three orthogonal characteristics jointly govern "
    "agent capability and risk: (i) **autonomy** (whether the agent can "
    "act without per-step human confirmation), (ii) **goal complexity** "
    "(how long-horizon and decomposable a goal it can pursue), and (iii) "
    "**action space** (the set of available external actions, controlled "
    "by tools). This paper focuses on the third dimension.",
    title="Setup: tools define the agent's action space",
)

# ---------------------------------------------------------------------------
# Open research questions
# ---------------------------------------------------------------------------

q_central = question(
    "How are AI agents currently used? Specifically, what tools do agents "
    "have access to, what tasks do those tools enable, where are they "
    "deployed, and how are these characteristics evolving over time?",
    title="How are AI agents being used in the wild?",
)

q_rq1_domain = question(
    "RQ1: How widely are AI agents used across (task) domains?",
    title="RQ1: distribution across task domains",
)

q_rq2_geography = question(
    "RQ2: How widely are AI agents used across geographies?",
    title="RQ2: distribution across geographies",
)

q_rq3_impact = question(
    "RQ3: What fraction of AI agents are used for perception, reasoning, "
    "or action over time?",
    title="RQ3: direct-impact mix and its evolution",
)

q_rq4_generality = question(
    "RQ4: What fraction of AI agents are used to access narrow, "
    "constrained environments versus general, unconstrained environments?",
    title="RQ4: generality (constrained vs. unconstrained)",
)

q_rq5_aiauth = question(
    "RQ5: What fraction of AI agent tools are themselves created with the "
    "support of AI agents?",
    title="RQ5: AI co-authorship of MCP servers",
)

# ---------------------------------------------------------------------------
# Problem-framing claims
# ---------------------------------------------------------------------------

claim_evidence_gap = claim(
    "**Evidence gap on agent-tool usage.** Most published studies that "
    "monitor how AI systems are used focus on *LLM* usage (chat traffic on "
    "ChatGPT, Claude.ai, etc.) [@Chatterji2025ChatGPT; @Handa2025Claude] or "
    "on user surveys that do not distinguish standalone-LLM use from "
    "agent use. Recent platform-data studies of agent usage cover only a "
    "narrow slice of the ecosystem: Aubakirova & Midha [@Aubakirova2025] "
    "track OpenRouter token traffic, Casper et al. [@Casper2025AgentIndex] "
    "manually catalogue 67 deployed agents, Yang et al. [@Yang2025Comet] "
    "study Perplexity's Comet browser agent, and Pan et al. "
    "[@Pan2025Practitioners] survey 306 implementers. None of these "
    "provide cross-platform, large-scale evidence of what tools agents "
    "are actually being given access to.",
    title="Problem: no cross-platform large-N evidence of agent-tool usage",
    background=[setup_ai_agent_definition],
)

claim_tools_proxy_for_action_space = claim(
    "**MCP-server monitoring as a proxy for the agent action space.** "
    "Because MCP is the dominant open protocol for agent tools and is "
    "supported by all major agent developers, monitoring publicly "
    "available MCP servers (their tool catalogues, creation dates, and "
    "package-registry download counts) yields a tractable, cross-platform "
    "empirical view of which tools are being created, which are popular, "
    "and how the ecosystem of agent capabilities is evolving over time. "
    "This complements -- but does not replace -- platform-traffic studies, "
    "deployer interviews, and agent-system inspection.",
    title="Approach: MCP monitoring as a tractable empirical lens on agent action spaces",
    background=[setup_mcp_definition, setup_action_space],
)

claim_contribution_dataset = claim(
    "**Contribution 1: An agent-tool dataset.** The paper curates a panel "
    "of **177,436 distinct public MCP tools** drawn from **19,388** "
    "verified MCP-server repositories on GitHub and the Smithery registry, "
    "spanning 11/2024-02/2026 (approximately 16 months). To the authors' "
    "knowledge this is the largest public AI-agent-tool dataset to date. "
    "Each tool is classified by direct impact (perception / reasoning / "
    "action), generality (narrow- vs general-purpose environment), and "
    "task domain via O*NET mapping. The dataset is augmented with monthly "
    "package-registry download counts (NPM, PyPI) for 3,854 servers "
    "(42,498 tools) to approximate usage trends.",
    title="Contribution 1: dataset of 177k MCP tools across 19k servers",
)

claim_contribution_timetrend = claim(
    "**Contribution 2: Time-resolved agent-tool trends.** Tracking each "
    "MCP server's creation date, AI co-authorship signals, and monthly "
    "downloads, the paper shows how the *direct-impact mix* of agent "
    "tools (perception/reasoning/action), the *generality mix* "
    "(constrained/unconstrained environments), and the *AI co-authorship* "
    "share evolve month-by-month over the 16-month panel.",
    title="Contribution 2: longitudinal evolution of agent-tool composition",
)

claim_contribution_governance = claim(
    "**Contribution 3: A method for early monitoring of agent deployment.** "
    "By demonstrating, on the example of agentic financial-transaction "
    "tools (a UK-government collaboration), how MCP-tool monitoring can "
    "anticipate the rollout of consequential agent capabilities months "
    "before they appear in mainstream platforms, the paper proposes "
    "tool-layer monitoring as a lightweight regulatory instrument that "
    "complements model-output oversight [@Stein2026; @BoE2025Innovation].",
    title="Contribution 3: tool-layer monitoring as a regulatory instrument",
)

# ---------------------------------------------------------------------------
# Headline empirical findings (previewed in introduction; details in s5/s6)
# ---------------------------------------------------------------------------

claim_finding_software_dominates = claim(
    "**Headline finding 1.** Tools designed for **software development "
    "and IT tasks account for 67%** of the 177k MCP tools and **90% of "
    "MCP-server downloads**, indicating that the current dominant utility "
    "of AI agents is to accelerate technical workflows rather than to "
    "automate broader economic tasks. Finance and business management "
    "tools are the next-largest category at 18% of tools and 5% of "
    "downloads.",
    title="Headline 1: software development = 67% of tools, 90% of downloads",
)

claim_finding_us_concentration = claim(
    "**Headline finding 2.** PyPI download IP-geolocation shows that "
    "agent tool usage is heavily concentrated in the **United States "
    "(~50%)**, followed by Western Europe (~20%) and China (~5%). The "
    "PyPI-based geographic split is biased toward Western users, but the "
    "US concentration is consistent with prior findings on Claude.ai, "
    "ChatGPT, OpenRouter, and Perplexity Comet usage [@Handa2025Claude; "
    "@Chatterji2025ChatGPT; @Aubakirova2025; @Yang2025Comet].",
    title="Headline 2: ~50% of agent-tool usage geolocates to the US",
)

claim_finding_action_share_growth = claim(
    "**Headline finding 3 (the key time trend).** Between **November 2024 "
    "and February 2026** the *download-weighted* share of **action tools** "
    "(tools that directly modify external environments, e.g. file editing, "
    "sending emails, executing code) rose from **27% to 65%** of total "
    "monthly tool downloads. The shift is even more pronounced for tools "
    "released by registered commercial entities (21% -> 71%). Growth was "
    "driven primarily by adoption of **general-purpose** tools for browser "
    "use, computer control, and code execution, rather than by narrow "
    "API-specific tools.",
    title="Headline 3: action-tool share rose 27% -> 65% over 16 months",
)

claim_finding_action_stakes_distribution = claim(
    "**Headline finding 4.** Action tools predominantly support "
    "**medium-stakes occupations** (50-75 on the O*NET 0-100 "
    "impact-of-decisions scale), such as computer-systems administration. "
    "Most high-stakes occupations have few action tools, with one notable "
    "exception: **finance has disproportionately many high-stakes action "
    "tools** (cryptocurrency transfer, payment execution, trading) "
    "relative to the cross-occupation pattern. Other higher-stakes "
    "examples observed include medication management, tax filing, drone "
    "navigation, and legal-document generation.",
    title="Headline 4: action tools cluster at medium stakes, with finance an outlier",
)

claim_finding_ai_coauthorship_growth = claim(
    "**Headline finding 5.** AI assistance is detected in **28.3%** of "
    "MCP servers (5,494 of 19,388) and **36.3%** of tools (64,489 of "
    "177,436), based on first-month commit evidence. The share of *newly "
    "created* MCP servers that show AI assistance rose from **6% in "
    "01/2025 to 62% in 02/2026**, dominated by Claude Code (68.6% of "
    "AI-coauthored servers), Cursor (9.2%), Copilot (9.1%), and Codex "
    "(6.0%). A substantial and growing fraction of the agent-tool "
    "ecosystem is being built by AI agents themselves.",
    title="Headline 5: AI co-authorship of MCP servers rose 6% -> 62% in 13 months",
)

# ---------------------------------------------------------------------------
# Baseline assumption that the empirical findings will challenge
# ---------------------------------------------------------------------------

claim_prior_assumption_action_rare = claim(
    "**Common prior assumption (to be tested).** A baseline policy view, "
    "consistent with surveys reporting that practitioners deploy agents "
    "*restrictively* (no more than ~10 steps before human intervention) "
    "[@Pan2025Practitioners] and with regulatory framings that emphasise "
    "*read-only* access patterns, is that **action tools (those that "
    "directly modify external environments) constitute a small minority "
    "of deployed agent tooling**, while the bulk of agent activity remains "
    "in perception (search, lookup) and reasoning (analysis) tools. Under "
    "this view, regulatory attention to the tool layer is a low priority.",
    title="Baseline assumption: action tools are rare in deployed agent tooling",
)

__all__ = [
    "setup_ai_agent_definition",
    "setup_mcp_definition",
    "setup_action_space",
    "q_central",
    "q_rq1_domain",
    "q_rq2_geography",
    "q_rq3_impact",
    "q_rq4_generality",
    "q_rq5_aiauth",
    "claim_evidence_gap",
    "claim_tools_proxy_for_action_space",
    "claim_contribution_dataset",
    "claim_contribution_timetrend",
    "claim_contribution_governance",
    "claim_finding_software_dominates",
    "claim_finding_us_concentration",
    "claim_finding_action_share_growth",
    "claim_finding_action_stakes_distribution",
    "claim_finding_ai_coauthorship_growth",
    "claim_prior_assumption_action_rare",
]
