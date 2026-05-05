"""Section 6: High-stakes example -- agentic financial transactions.

Section 5.6 / 6 of Stein 2026 [@Stein2026]. The financial-transactions
case study demonstrates the *applied* value of the monitoring approach
for regulators. It is presented as a worked example of how MCP-tool
monitoring detects an early signal of high-stakes agent deployment
that financial authorities would otherwise see only after the fact.

Key claims here:

* Agentic-payment MCP servers grew from 47 servers in 01/2025 to
  **1,578 servers in 02/2026** (Figure 7) -- a 33x increase in 13
  months.
* This trend foreshadows risks to systemic financial stability,
  particularly for cryptocurrency transactions which have less
  regulatory oversight and limited reversal options.
* The case study was produced as part of an active collaboration
  with UK financial authorities (Bank of England, FCA), validating
  the regulatory use case.
* Discussion (Section 6) draws five higher-level governance
  implications from the empirical findings.
"""

from gaia.lang import claim, setting

from .motivation import (
    setup_action_space,
    setup_mcp_definition,
)
from .s2_background import (
    claim_action_space_amplifies_misalignment,
    claim_action_space_amplifies_misuse,
    claim_action_space_amplifies_structural,
    claim_self_improvement_risk,
    claim_mcp_early_indicator,
)
from .s5_findings import (
    claim_finding_action_growth,
    claim_finding_aiauth_growth,
    claim_finding_finance_highstakes_outlier,
    claim_finding_general_purpose_action_correlation,
    claim_finding_general_purpose_growth,
)

# ---------------------------------------------------------------------------
# 6.1 Financial case study -- the empirical observation
# ---------------------------------------------------------------------------

setup_payments_autonomy_scale = setting(
    "**Payments-autonomy 0-4 scale (Appendix A.4.2).** Each MCP server "
    "with payment functionality is rated by Claude Sonnet 4.5 on a 0-4 "
    "ordinal scale:\n\n"
    "* **0** = not a payment server (no payment functionality);\n"
    "* **1** = read-only information about payments (invoice view, "
    "payment history);\n"
    "* **2** = payment request / link creation only (no execution);\n"
    "* **3** = payment processing via third-party API "
    "(execution-but-mediated);\n"
    "* **4** = autonomous payment execution (e.g. signed crypto "
    "transactions without external approval).\n\n"
    "Human validators (n = 6) agree with the LLM classification 83% "
    "(Fleiss' kappa = 0.42).",
    title="Setup: payments-autonomy 0-4 scale",
)

claim_figure7_payments_growth = claim(
    "**Figure 7 -- agentic transaction tools by autonomy level.** "
    "Number of publicly available MCP servers with **any** payment-related "
    "tool (autonomy >= 1):\n\n"
    "| Month | # Payment MCP servers |\n"
    "|---|---:|\n"
    "| 01/2025 | 47 |\n"
    "| 02/2026 | **1,578** |\n\n"
    "A ~33x increase over 13 months, with corresponding growth in monthly "
    "downloads. Higher-autonomy servers (level 4: autonomous payment "
    "execution) include cryptocurrency wallet tools that sign and submit "
    "transactions directly.",
    title="Figure 7: payment MCP servers grew 47 -> 1,578 (Jan 2025 - Feb 2026)",
    background=[setup_payments_autonomy_scale, setup_mcp_definition],
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 7"},
)

claim_finding_crypto_payment_trend = claim(
    "**Finding 6.1.** MCP-tool monitoring detects a sharply rising "
    "trend toward **direct agentic payment infrastructure**, "
    "particularly for **cryptocurrencies**, which financial regulators "
    "are concerned with because crypto transactions face less regulatory "
    "oversight, fewer reversal options, and can be executed at greater "
    "scale than traditional payment rails [@Aldasoro2025FinancialAI; "
    "@Danielsson2025]. This direct agentic-crypto trend is exactly the "
    "kind of early signal that traditional regulatory channels (sectoral "
    "surveys, interviews, usage-data agreements) capture only with "
    "months-to-years lag.",
    title="6.1 detected: rising direct agentic crypto-payment infrastructure",
)

claim_regulator_use_case_validation = claim(
    "**Regulatory validation.** The financial-transactions monitoring "
    "case study was conducted as part of an **active collaboration "
    "between the UK AI Security Institute (AISI) and the Bank of England** "
    "on agentic-payment foresight, with named contributions from Bank of "
    "England staff (Elliot Jones, Andrew Walters) and AISI staff (Rosco "
    "Hunter, Ture Hinrichsen). This provides concrete external validation "
    "that MCP-tool monitoring is operationally useful for financial "
    "authorities, not just an academic exercise [@BoE2025Innovation].",
    title="6.1 validated: monitor delivered to Bank of England",
)

# ---------------------------------------------------------------------------
# 6.2 - 6.6 Discussion: five governance implications
# ---------------------------------------------------------------------------

claim_disc_attack_surface = claim(
    "**Discussion implication 1: attack surface.** The rising deployment "
    "of agents with general-purpose tools (computer use, browser, code "
    "execution) **expands the attack surface exposed to malicious actors**. "
    "Misuse risks like prompt-injection-based credential theft become more "
    "potent when agents can execute code and access file systems. The "
    "detected growth in general-purpose action tools (Sections 5.3-5.4) "
    "is therefore evidence of a growing collective misuse exposure.",
    title="Discussion 1: general-purpose action tools expand the misuse attack surface",
)

claim_disc_misalignment_consequences = claim(
    "**Discussion implication 2: misalignment consequences.** As agents "
    "increasingly modify external environments with little oversight, "
    "**the consequences of any misaligned model update are amplified**. "
    "If a widely-deployed underlying LLM (on which many agents depend) "
    "receives a misaligned update, the action capability of those agents "
    "translates that misalignment into real-world harm at scale. The "
    "detected growth in action-tool share is evidence that this risk "
    "channel is opening.",
    title="Discussion 2: action growth amplifies misalignment consequences",
)

claim_disc_software_finance_concentration = claim(
    "**Discussion implication 3: structural change in software and "
    "finance.** Tool counts and downloads are particularly high in "
    "**software development and financial tasks**. Both domains exhibit "
    "scale and speed sensitivities that may produce structural changes -- "
    "early evidence in the entry-level software-developer job market is "
    "already visible [@Brynjolfsson2025Canaries], and finance has the "
    "anomalous high-stakes action-tool concentration documented in 5.1. "
    "Public-tool monitoring is a measurable early signal for these "
    "structural shifts; however, this approach must be paired with "
    "data on private internal tooling and on agent-system orchestration "
    "to remain useful as agents start building their own tools.",
    title="Discussion 3: software & finance show structural-change signals",
)

claim_disc_governance_complication = claim(
    "**Discussion implication 4: tool-based governance is harder for "
    "general-purpose tools.** **Narrow-purpose tools** (e.g. a "
    "cryptocurrency-transfer tool) have a *clear* risk profile and "
    "governance can attach to specific tool calls. **General-purpose "
    "tools** (e.g. a browser tool that can download files or malware) "
    "have ambiguous risk profiles and the per-call user review needed "
    "to govern them becomes operationally arduous. Current systems like "
    "Claude Code's `settings.json` permit/block specific narrow tools "
    "but require user review for general-purpose tools. Future systems "
    "could condition permissions on tool-call *context*; consequential "
    "actions (large transfers, legal registration) could mandate human "
    "authentication.",
    title="Discussion 4: general-purpose tools complicate tool-based governance",
)

claim_disc_unconstrained_structural = claim(
    "**Discussion implication 5: unconstrained-environment structural "
    "risks.** Because **94% of general-purpose-server downloads involve "
    "action tools**, *consequential agent actions are now occurring "
    "predominantly in the least controlled environments* (web, "
    "filesystem) rather than via secure APIs. AI agents using these "
    "tools become indistinguishable from human users in those "
    "environments, motivating proposals for *agent IDs* "
    "[@Chan2024IDs]. This is a structural-risk channel not addressed "
    "by per-tool governance.",
    title="Discussion 5: action-in-unconstrained env raises structural risks",
)

# ---------------------------------------------------------------------------
# Synthetic discussion claim: tool monitoring is a useful regulatory
# instrument
# ---------------------------------------------------------------------------

claim_governance_thesis = claim(
    "**Section 6 thesis: MCP-tool monitoring is a viable regulatory "
    "instrument.** The combination of (i) early detection of "
    "consequential trends (financial case study), (ii) the documented "
    "lead time of MCP publication over mainstream-platform integration "
    "(Google Calendar example), and (iii) the demonstrated five "
    "discussion implications collectively argues that MCP-tool monitoring "
    "is a useful, lightweight, automatable instrument for governments "
    "and regulators to extend oversight beyond model outputs to the "
    "tool layer where agent action is actually exercised.",
    title="6 thesis: MCP-tool monitoring is a viable regulatory instrument",
    background=[setup_action_space],
)

# ---------------------------------------------------------------------------
# Comparative methodology claim: when to use which monitoring approach
# (Appendix A.5, Table 7)
# ---------------------------------------------------------------------------

claim_table7_methods_comparison = claim(
    "**Table 7 -- comparison of agent-monitoring methods (Appendix A.5).** "
    "MCP-tool monitoring sits in a particular niche relative to other "
    "approaches:\n\n"
    "| Criterion | MCP tools (this paper) | Web scraping | Interviews/surveys | Provider usage data |\n"
    "|---|---|---|---|---|\n"
    "| Early indicator | **Yes** (e.g. Coinbase MCP visible 01/2025) | "
    "Yes | No (months-to-years lag) | Partly |\n"
    "| Wide coverage | Partly (developer-skewed) | Partly | Partly | Yes (with data agreement) |\n"
    "| Precise coverage | No (caching-limited) | Partly | Yes | Yes |\n"
    "| Region-specific | Partly | Partly | Yes | Yes |\n"
    "| High-stakes coverage | Partly (public only) | Partly | Yes | Partly |\n"
    "| Efficient & available | **Yes** (automatable, public) | Partly | "
    "No (resource-intensive) | Partly (data-access dependent) |\n"
    "| Purpose | **Early scanning** | Early scanning | In-depth analysis | Scanning + in-depth |\n",
    title="Table 7: MCP monitoring is best for early scanning",
    metadata={"source_table": "artifacts/2603.23802.pdf, Table 7 (Appendix A.5)"},
)

# ---------------------------------------------------------------------------
# Conclusion (Section 7) headline
# ---------------------------------------------------------------------------

claim_conclusion_action_space_expanded = claim(
    "**Conclusion 7.1.** Across the panel, the agent action space "
    "expanded significantly along all five attributes: tool availability "
    "rose >36x (~4,888 tools in 01/2025 to 177,000 in 02/2026); the "
    "**action-tool download share rose 27% -> 65%** (21% -> 71% for "
    "official commercial servers); **general-purpose tool share rose "
    "41% -> 50%** of downloads, with 94% of these being action; tools "
    "remain heavily geographically concentrated (US 57%, W. Europe 20%, "
    "China 5%); and **AI-coauthored share of new servers rose 6% -> 62%**. "
    "AI agents are transitioning from primarily *observing* environments "
    "to actively *modifying* them, increasingly through general-purpose "
    "tools in unconstrained environments, with early deployment in "
    "high-stakes domains such as finance.",
    title="Conclusion 7.1: action space expanded along all five attributes",
)

claim_limitation_lower_bound = claim(
    "**Conclusion 7.2 (limitation).** MCP repositories are *one* "
    "channel through which agents acquire tools. Developers also build "
    "custom integrations, use proprietary internal tooling, or distribute "
    "tools via channels not covered by GitHub or Smithery. The reported "
    "177k tools therefore represent a **lower bound** on the actions "
    "actually available to AI agents, not a comprehensive enumeration. "
    "Multi-level monitoring (agent systems, agent actions in target "
    "environments) and skill-level / AGENTS.md monitoring would be "
    "needed to cover the gap, especially as the trend toward "
    "general-purpose tools makes per-tool descriptions less informative "
    "about what agents actually do.",
    title="Conclusion 7.2: 177k is a lower bound; multi-level monitoring needed",
)

__all__ = [
    "setup_payments_autonomy_scale",
    "claim_figure7_payments_growth",
    "claim_finding_crypto_payment_trend",
    "claim_regulator_use_case_validation",
    "claim_disc_attack_surface",
    "claim_disc_misalignment_consequences",
    "claim_disc_software_finance_concentration",
    "claim_disc_governance_complication",
    "claim_disc_unconstrained_structural",
    "claim_governance_thesis",
    "claim_table7_methods_comparison",
    "claim_conclusion_action_space_expanded",
    "claim_limitation_lower_bound",
]
