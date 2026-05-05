"""Section 2: Background -- characterising the action space.

Section 2 of Stein 2026 [@Stein2026]. Develops the conceptual scaffold:
(2.1) the action space is one of three dimensions of agent capability
alongside autonomy and goal complexity; (2.2) the action space shapes
four risk categories (misuse, mistake/misalignment, structural, and
recursive self-improvement); (2.3) five attributes of tools jointly
characterise the action space; and (2.4) what current literature does
and does not measure about agent-tool usage.

This module formalises the *qualitative* claims of Section 2 -- the
tool taxonomy and the link from action-space attributes to risk classes
-- which the empirical sections (s5, s6) will then evaluate.
"""

from gaia.lang import claim, setting

from .motivation import (
    setup_action_space,
    setup_ai_agent_definition,
    setup_mcp_definition,
)

# ---------------------------------------------------------------------------
# 2.1 Three capability dimensions
# ---------------------------------------------------------------------------

setup_three_dimensions = setting(
    "**Three capability dimensions.** Building on prior frameworks "
    "[@Chan2023Harms; @Kasirzadeh2025; @Cihon2025Autonomy], the paper "
    "decomposes AI-agent capability into three orthogonal dimensions:\n\n"
    "1. **Autonomy** -- the ability to fulfil tasks without per-step "
    "human direction. Determined by system configuration (e.g. Claude "
    "Code's `dangerously-skip-permissions` mode), *not* by tools.\n"
    "2. **Goal complexity** -- the ability to pursue high-level objectives "
    "via decomposition and adaptive planning over extended horizons. "
    "Determined by context-window size, memory architecture, and the "
    "underlying LLM, *not* by tools.\n"
    "3. **Action space** -- the set of available external actions. "
    "Determined entirely by the tools the agent has access to. This is "
    "the dimension the paper measures.",
    title="Three orthogonal dimensions of AI-agent capability",
)

# ---------------------------------------------------------------------------
# 2.2 Action-space-to-risk mapping (qualitative)
# ---------------------------------------------------------------------------

claim_action_space_amplifies_misuse = claim(
    "**Misuse risks scale with action space.** An AI agent's attack "
    "surface is defined by its action space: (i) it is more likely to "
    "*encounter* manipulative instructions (prompt injections) when it "
    "has general-purpose tools accessing the open web, and (ii) it can "
    "only *act* on malicious instructions when it has tools to act, e.g. "
    "to send emails or transfer cryptocurrency. Documented incidents "
    "include cyber criminals exploiting AI agents to leak sensitive data "
    "and transfer hundreds of thousands of dollars in cryptocurrency "
    "[@Hou2025MCP]. Therefore, more action and more general-purpose tools "
    "in the ecosystem implies a larger collective misuse attack surface.",
    title="Action-space -> misuse risk",
    background=[setup_action_space],
)

claim_action_space_amplifies_misalignment = claim(
    "**Mistake and misalignment risks scale with action space.** Misaligned "
    "or erroneous agents *limited to perception or reasoning tools* can "
    "deceive users but cannot themselves take harmful real-world action. "
    "Documented production incidents (live-database deletion by AI coding "
    "tools [@Stein2026], exposure of patient records, simulated blackmail "
    "by misaligned agents [@Anthropic2025Misalignment]) all required the "
    "agent to possess action tools (send-email, execute-code, modify-db). "
    "Cryptocurrency transfer tools enable immediate, irreversible damage. "
    "An agent's *propensity* for misaligned behaviour comes from the "
    "underlying LLM, but whether that propensity translates into harmful "
    "action depends entirely on the tools available.",
    title="Action-space -> mistake/misalignment risk",
    background=[setup_action_space],
)

claim_action_space_amplifies_structural = claim(
    "**Structural risks scale with action space.** When AI agent actions "
    "substitute for human actions at scale, those actions are often more "
    "*correlated* (similar training, faster execution, no human in the "
    "loop) [@Stein2026]. Plausible structural-harm scenarios include: "
    "agents with `browser_click` or `phone_call` tools flooding government "
    "websites or emergency lines; simultaneous use of automated banking "
    "tools triggering 'agent bank runs' / liquidity crises "
    "[@Aldasoro2025FinancialAI; @Danielsson2025]; and agents editing "
    "encyclopedia or web pages at scale, reducing online content "
    "diversity. These scenarios all require general-purpose action tools "
    "operating across many sites simultaneously.",
    title="Action-space -> structural risk",
    background=[setup_action_space],
)

claim_self_improvement_risk = claim(
    "**Recursive self-improvement risk.** AI agents that can *create* "
    "their own tools expand the action space without requiring "
    "additional human effort. When AI coding agents build new MCP servers "
    "for other AI agents, tool proliferation is no longer bottlenecked by "
    "human developers, and the rate of tool creation may scale beyond "
    "human oversight capacity. This makes the share of AI-coauthored "
    "tools a leading indicator of the action space's growth rate.",
    title="Recursive risk: AI agents creating AI agent tools",
    background=[setup_action_space],
)

# ---------------------------------------------------------------------------
# 2.3 Five attributes of tools that jointly define the action space
# ---------------------------------------------------------------------------

setup_attribute_direct_impact = setting(
    "**Attribute 1 -- direct impact** describes whether a tool permits "
    "*perception* (read external state), *reasoning* (analyse data or "
    "concepts), or *action* (modify the external environment). Examples: "
    "perception = internal database query, web search, sensor read; "
    "reasoning = task-decomposition planner, calculator; action = "
    "file edit, send-email, drone steering, payment execution.",
    title="Tool attribute 1: direct impact (perception/reasoning/action)",
)

setup_attribute_generality = setting(
    "**Attribute 2 -- generality** describes whether a tool interacts "
    "with a *narrow, constrained* environment (specific API endpoint, "
    "single platform) or a *general, unconstrained* environment (open "
    "web, arbitrary code execution, full filesystem). Examples: narrow "
    "= a Coinbase API tool that only sends BTC; general = a "
    "`computer_mouse_click` tool that can drive any desktop application "
    "[@CAISI2025].",
    title="Tool attribute 2: generality (constrained/unconstrained)",
)

setup_attribute_task_domain = setting(
    "**Attribute 3 -- task domain** describes the kind of work the tool "
    "helps complete. The paper classifies domains using the O*NET "
    "occupational taxonomy [@ONET2025] and distinguishes lower- vs "
    "higher-stakes domains using O*NET's *impact of decisions* survey "
    "score. A 'submit feedback' tool is less consequential than a "
    "'submit cryptocurrency trade' tool.",
    title="Tool attribute 3: task domain (O*NET-mapped)",
)

setup_attribute_geography = setting(
    "**Attribute 4 -- geography** describes the region(s) where a tool is "
    "used. Some MCP servers are built for and used in a single country "
    "(e.g. Cyprus-specific trading tools), while others are used "
    "worldwide (e.g. enterprise workspace integrations).",
    title="Tool attribute 4: geography",
)

setup_attribute_aicoauth = setting(
    "**Attribute 5 -- AI co-authorship** describes whether a tool was "
    "created with the assistance of an AI coding agent. Some tools are "
    "fully human-authored, others are conceptualised by humans and "
    "implemented with AI assistance, and a growing fraction may eventually "
    "be conceptualised and implemented entirely by AI agents.",
    title="Tool attribute 5: AI co-authorship",
)

# ---------------------------------------------------------------------------
# Tables 1 and 2 (Section 2.3) -- agent-tool examples
# ---------------------------------------------------------------------------

claim_table1_examples = claim(
    "**Table 1 (agent-tool examples by generality x direct impact).** "
    "The paper illustrates the (generality, direct-impact) cross-tab with "
    "concrete MCP examples:\n\n"
    "| | Perception | Reasoning | Action |\n"
    "|---|---|---|---|\n"
    "| **Narrow-purpose** | Search for tickets (Ticketmaster MCP) | Reason "
    "through biomedical research questions (BioMCP) | Send crypto "
    "(Coinbase MCP) |\n"
    "| **General-purpose** | Search the internet (DuckDuckGo MCP) | "
    "Perform accessibility audits of any website (A11Y MCP) | Use a "
    "computer via mouse clicks (Desktop Commander MCP) |\n\n"
    "**General-purpose action tools** (e.g. `computer_mouse_click`) expand "
    "the action space the most; narrow-purpose action tools expand it "
    "somewhat; perception and reasoning tools expand it less.",
    title="Table 1: tool examples by generality x direct impact",
    metadata={"source_table": "artifacts/2603.23802.pdf, Table 1"},
)

claim_table2_examples = claim(
    "**Table 2 (action-tool examples by geography x consequentiality).** "
    "The paper illustrates the (geography, stakes) cross-tab for action "
    "tools using the most-used MCP server in each cell. Stakes are based "
    "on the O*NET 0-100 impact-of-decisions score: low (<50), medium "
    "(50-75), high (>75).\n\n"
    "| | Low-stakes | Medium-stakes | High-stakes |\n"
    "|---|---|---|---|\n"
    "| **One country** | Test software (mcp-server-spira, US) | Build "
    "websites (django-mcp-server, US) | Execute financial trades "
    "(metatrader-mcp-server, Cyprus) |\n"
    "| **One continent** | Bulk-grade students (canvas-mcp, N. America) "
    "| Create documentation (office-word-mcp-server, Asia) | Configure "
    "delegation to AI agents (mcp-feedback-enhanced, Asia) |\n"
    "| **Worldwide** | Configure AI agent tool connections (llmling) | "
    "Manage enterprise software suite (mcp-server-odoo) | Manage "
    "workspace permissions, send emails (google_workspace_mcp) |\n\n"
    "Action tools used worldwide in high-stakes settings have the largest "
    "action-space footprint.",
    title="Table 2: action-tool examples by geography x consequentiality",
    metadata={"source_table": "artifacts/2603.23802.pdf, Table 2"},
)

# ---------------------------------------------------------------------------
# 2.3 closing claim: large action space amplifies risk (composite of risk
# claims above)
# ---------------------------------------------------------------------------

claim_large_action_space_amplifies_risk = claim(
    "**Across all four risk categories, tools that enable a *large* action "
    "space -- general-purpose action tools used at scale across "
    "consequential domains and across geographies -- are the dominant "
    "amplifiers of AI-agent risk.** A large action space is not itself "
    "harm, but it is the necessary condition for many of the most "
    "discussed harm scenarios. Monitoring the size and composition of "
    "the public agent-tool ecosystem therefore provides a *leading "
    "indicator* for the four risk categories above.",
    title="Section 2 thesis: large action space = amplifier of agent risks",
)

# ---------------------------------------------------------------------------
# 2.3 closing claim: MCP tools as early indicators
# ---------------------------------------------------------------------------

claim_mcp_early_indicator = claim(
    "**MCP tools published on developer platforms function as *early* "
    "indicators of agent-tool trends.** Concrete example from the paper: "
    "an unofficial Google Calendar MCP server was published on GitHub on "
    "**5 December 2024** and captured in this dataset; Anthropic and "
    "OpenAI added pre-built Google Calendar tools to claude.ai and "
    "ChatGPT four to eight months later (April and August 2025 "
    "respectively). Large-scale developer-platform downloads of MCP tools "
    "thus *foreshadow* later integration into mainstream consumer agent "
    "products.",
    title="MCP downloads as early indicators of mainstream agent tooling",
    background=[setup_mcp_definition],
)

# ---------------------------------------------------------------------------
# 2.4 Current state of evidence (Table 3 summary)
# ---------------------------------------------------------------------------

claim_existing_evidence_gap_breakdown = claim(
    "**State of existing evidence on agent action spaces (Table 3).** "
    "Across seven prior usage studies of LLM and agent platforms (Bing "
    "Copilot, ChatGPT, Claude.ai, OpenRouter API, Claude API, Perplexity "
    "Comet, and the IT-workforce baseline), no study reports the *full* "
    "(perception, reasoning, action) x (constrained, unconstrained) "
    "breakdown for the action space:\n\n"
    "* Action coverage is reported only by OpenRouter, Claude API, and "
    "Comet, but without quantitative shares.\n"
    "* No study reports the constrained-vs-unconstrained generality "
    "distribution quantitatively.\n"
    "* Geography is partially reported by ChatGPT, Claude.ai, OpenRouter "
    "and (qualitatively) Bing Copilot.\n"
    "* All studies focus on US-based platforms, leaving Chinese and other "
    "non-Western platforms largely uncovered.\n\n"
    "This paper's MCP-monitoring approach is the first to provide "
    "**quantitative** download-share figures for action vs reasoning vs "
    "perception (64.8% / 3.3% / 31.7%) and constrained vs unconstrained "
    "(54.6% / 45.4%) for the public agent-tool ecosystem.",
    title="Table 3: prior studies leave the action-space attributes largely unmeasured",
    metadata={"source_table": "artifacts/2603.23802.pdf, Table 3"},
)

__all__ = [
    "setup_three_dimensions",
    "claim_action_space_amplifies_misuse",
    "claim_action_space_amplifies_misalignment",
    "claim_action_space_amplifies_structural",
    "claim_self_improvement_risk",
    "setup_attribute_direct_impact",
    "setup_attribute_generality",
    "setup_attribute_task_domain",
    "setup_attribute_geography",
    "setup_attribute_aicoauth",
    "claim_table1_examples",
    "claim_table2_examples",
    "claim_large_action_space_amplifies_risk",
    "claim_mcp_early_indicator",
    "claim_existing_evidence_gap_breakdown",
]
