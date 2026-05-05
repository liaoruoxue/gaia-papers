"""Section 5: Results -- the empirical headline numbers.

Section 5 of Stein 2026 [@Stein2026]. Reports five sets of empirical
findings answering the five research questions:

* 5.1 -- task-domain breakdown of tools and downloads (Table 6).
* 5.2 -- geographic concentration (Figure 3).
* 5.3 -- the action-tool share rose 27% -> 65% over 16 months
  (Figure 4); ratchets up to 21% -> 71% for commercial servers.
* 5.4 -- general-purpose share rose 41% -> 50%; 94% of
  general-purpose downloads are action tools (Figure 5).
* 5.5 -- AI-coauthored servers rose 6% -> 62%; Claude dominates
  (Figure 6).
* 5.1 (continued) -- consequentiality plot (Figure 2): action tools
  cluster at medium stakes, finance is a high-stakes outlier.

Each subsection separates the methodology-derived headline number
(an *atomic empirical claim*) from per-month observations and from
the regression-fitted asymptotic limits.
"""

from gaia.lang import claim, setting

from .motivation import (
    setup_action_space,
)
from .s2_background import (
    setup_attribute_direct_impact,
    setup_attribute_generality,
)
from .s3_data import setup_collection_window
from .s4_methodology import (
    claim_consequentiality_score,
    setup_onet_taxonomy,
)

# ---------------------------------------------------------------------------
# 5.1 Task domains -- Table 6
# ---------------------------------------------------------------------------

claim_table6_taskdomains = claim(
    "**Table 6 -- agent tools by task domain.** Top-down O*NET "
    "classification of all 19,388 servers and 177,436 tools, with "
    "PyPI/NPM download shares and Claude.ai usage shares for "
    "comparison [@Handa2025Claude]:\n\n"
    "| Task domain | Servers (%, dl%) | Tools (%, dl%) | Claude.ai usage |\n"
    "|---|---:|---:|---:|\n"
    "| Design, implement, maintain IT systems | 12,004 (68%, **90%**) | "
    "**119,685 (67%, 94%)** | 52% |\n"
    "| Business mgmt, finance, customer service | 2,397 (14%, 5%) | "
    "31,882 (**18%**, 4%) | 11% |\n"
    "| Scientific research, technical analysis | 1,273 (7%, 3%) | 8,989 "
    "(5%, 1%) | 6% |\n"
    "| Art, culture, religion | 723 (4%, <1%) | 6,053 (3%, <1%) | 15% |\n"
    "| Education, HR, prof. dev. | 201 (1%, <1%) | 1,857 (1%, <1%) | 8% |\n"
    "| Other (regulatory, public safety, industrial, logistics, "
    "sustainability, healthcare) | 931 (5%, 1%) | 8,968 (5%, <1%) | 6% |\n",
    title="Table 6: task-domain shares -- IT dominates (67% tools / 90% downloads)",
    background=[setup_onet_taxonomy],
    metadata={
        "source_table": "artifacts/2603.23802.pdf, Table 6",
        "figure": "artifacts/2603.23802.pdf, Figure 1 panel A & C",
    },
)

claim_finding_it_dominates = claim(
    "**Finding 5.1 (RQ1, headline).** Tools designed for **software "
    "development and IT tasks** account for **67% of the 177,436-tool "
    "dataset and 90% of MCP-server downloads**. The next-largest domain "
    "is **business management, finance, and customer service** at 18% "
    "of tools and 5% of downloads. The remaining nine domains together "
    "account for ~15% of tools and ~5% of downloads. The IT concentration "
    "is more extreme in the MCP dataset than in Claude.ai conversation "
    "data (52%), reflecting that MCP servers are primarily built and "
    "downloaded by developers.",
    title="5.1 IT tools = 67% of tools, 90% of downloads",
)

claim_finding_finance_share = claim(
    "**Finding 5.1 (RQ1, secondary).** Tools for **business management, "
    "finance, and customer service** are the second-largest domain at "
    "**18% of tools and 5% of downloads**. While the *download* share "
    "is small, the absolute number of tools (31,882) makes finance one "
    "of the most populated non-IT domains and motivates the financial "
    "case study in Section 6.",
    title="5.1 finance/business = 18% of tools, 5% of downloads",
)

# ---------------------------------------------------------------------------
# 5.1 Consequentiality (Figure 2)
# ---------------------------------------------------------------------------

claim_figure2_consequentiality = claim(
    "**Figure 2 -- consequentiality distribution of action tools.** Each "
    "dot is one SOC O*NET occupation, plotted as O*NET impact-of-decisions "
    "score (0-100) on the x-axis vs log of number of action tools "
    "supporting that occupation on the y-axis. Key observations:\n\n"
    "* Most action tools cluster at **medium-stakes** occupations "
    "(impact score 50-75), e.g. computer-systems administration.\n"
    "* A quadratic polynomial fit explains very little of the "
    "cross-occupation variance ($R^2 \\approx 0.03$); an F-test "
    "rejects the null that all slope coefficients are jointly zero "
    "($p = 0.015$).\n"
    "* The pink-shaded high-stakes region (score > 75) contains a small "
    "but non-trivial set of occupations with disproportionately many "
    "action tools, dominated by **financial occupations** (cryptocurrency "
    "transfer, payment execution, trading).\n"
    "* Occupations with no associated agent tools (near-exclusively "
    "non-computer-based) are excluded.",
    title="Figure 2: action tools cluster at medium stakes; finance is a high-stakes outlier",
    background=[claim_consequentiality_score],
    metadata={
        "figure": "artifacts/2603.23802.pdf, Figure 2",
        "caption": "Consequentiality distribution of AI agent actions.",
    },
)

claim_finding_action_medium_stakes = claim(
    "**Finding 5.1 (consequentiality).** Most action tools support "
    "**medium-stakes occupations** (50-75 on the O*NET impact-of-decisions "
    "scale), such as computer-systems administration, with relatively "
    "few tools for either low-stakes or high-stakes occupations. The "
    "absence of broad coverage of high-stakes occupations is consistent "
    "with current developer caution about deploying agents into "
    "high-impact contexts.",
    title="5.1 action tools predominantly support medium-stakes occupations",
)

claim_finding_finance_highstakes_outlier = claim(
    "**Finding 5.1 (high-stakes outlier).** Within the high-stakes "
    "(>75) region, **financial occupations have disproportionately many "
    "action tools** relative to the cross-occupation pattern. Beyond "
    "finance, the few other high-stakes MCP examples include medication "
    "management, tax filing, drone navigation, and legal-document "
    "generation. Within high-stakes occupations, tools typically support "
    "*lower-stakes subtasks* (e.g. medical tools enable image processing "
    "but not prescription authorisation).",
    title="5.1 finance is the standout high-stakes domain for action tools",
)

# ---------------------------------------------------------------------------
# 5.2 Geography (Figure 3)
# ---------------------------------------------------------------------------

claim_figure3_geography = claim(
    "**Figure 3 -- geographic distribution of action-tool downloads.** "
    "PyPI IP-based geolocation of N = 6.73M downloads of 528 MCP servers "
    "with action tools, 11/2024-10/2025:\n\n"
    "| Region | Share |\n"
    "|---|---:|\n"
    "| United States | ~50% |\n"
    "| Western Europe | ~20% |\n"
    "| China | ~5% |\n"
    "| Singapore | ~5% |\n"
    "| South Korea | 2.3% |\n"
    "| Other (Japan, Taiwan, India, Australia, Canada, etc.) | <2% each |\n",
    title="Figure 3: ~50% US, ~20% Europe, ~5% each China & Singapore",
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 3"},
)

claim_finding_action_us_concentration = claim(
    "**Finding 5.2 (RQ2).** Action-tool deployment is heavily concentrated "
    "in the **United States** (~50% of action-tool PyPI downloads in "
    "2025), followed by Western Europe (~20%) and China (~5%). The PyPI "
    "registry has a Western-skewed user base, so the share of activity "
    "in regions using alternative distribution channels (e.g. Chinese "
    "PyPI mirrors, internal registries) is likely under-represented. "
    "The conclusion 7.1 update gives 57% / 20% / 5% as the final figures.",
    title="5.2 action-tool usage: ~50% US, ~20% Europe, ~5% China",
    background=[setup_action_space],
)

# ---------------------------------------------------------------------------
# 5.3 Direct-impact mix over time (Figure 4)
# ---------------------------------------------------------------------------

claim_directimpact_overall_shares = claim(
    "**Direct-impact overall shares (across the full panel).** Across all "
    "16 months and all servers/tools with download data, the overall "
    "shares are:\n\n"
    "| Direct impact | Download share | Tool share |\n"
    "|---|---:|---:|\n"
    "| **Action** | **64.8%** | 36.0% |\n"
    "| Perception | 31.7% | 50.6% |\n"
    "| Reasoning | 3.3% | 13.4% |\n",
    title="5.3 panel-wide shares: action 64.8% downloads / 36.0% tools",
    background=[setup_attribute_direct_impact],
)

claim_observation_action_share_nov2024 = claim(
    "**Per-month observation (Nov 2024, panel start).** At the start of "
    "the panel (November 2024, the first month with substantive MCP "
    "downloads), **action tools were ~27% of monthly downloads** -- "
    "perception and reasoning together dominated.",
    title="Observation: action share = 27% in Nov 2024",
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 4 (left edge)"},
)

claim_observation_action_share_feb2026 = claim(
    "**Per-month observation (Feb 2026, panel end).** By the end of the "
    "panel (February 2026), **action tools had risen to ~65% of monthly "
    "downloads**, with perception and reasoning collapsing to a combined "
    "~35%.",
    title="Observation: action share = 65% in Feb 2026",
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 4 (right edge)"},
)

claim_observation_action_share_intermediate = claim(
    "**Per-month observation (intermediate months, Figure 4).** The "
    "monthly action-tool download share between November 2024 and "
    "February 2026 traces a roughly monotonic upward path: starting near "
    "27% in late 2024, action tools dominated by mid-2025 (~50%) and "
    "continued rising through to ~65% in early 2026. The asymptotic "
    "convergence model $y(t) = L - (L - y_0) e^{-kt}$ fitted via "
    "WLS reports a confidence interval consistent with $L \\ge 65%$. "
    "Each intermediate monthly share provides an independent observation "
    "consistent with the trend.",
    title="Observation: intermediate monthly action shares trace a monotonic rise",
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 4 (full curve)"},
)

claim_finding_action_growth = claim(
    "**Finding 5.3 (RQ3, headline time trend).** The download-weighted "
    "share of **action tools** rose from **27% in 11/2024 to 65% in "
    "02/2026** -- a 38-percentage-point increase in 16 months. Over the "
    "same period, perception's share fell from a clear majority to ~30%, "
    "and reasoning's share fell to ~5%. AI agents transitioned from a "
    "primarily *observe-and-report* posture to a primarily *act-on-"
    "environment* posture during the panel.",
    title="5.3 action-tool download share rose 27% -> 65% (Nov 2024 - Feb 2026)",
)

claim_finding_action_growth_official = claim(
    "**Finding 5.3 (commercial servers).** Among MCP servers published "
    "by registered commercial entities ('official servers', N = 8,469 "
    "tools, ~58% of all tracked downloads), the action-tool download "
    "share rose more sharply, from **21% in 11/2024 to 71% in 02/2026** "
    "(a 50-pp increase). Commercial-grade tooling has shifted to action "
    "even faster than the broader ecosystem.",
    title="5.3 official-server action share rose 21% -> 71%",
)

claim_finding_action_growth_driver = claim(
    "**Finding 5.3 (mechanism).** The action-tool share growth is "
    "driven primarily by adoption of **general-purpose tools for browser "
    "use, mobile-phone control, and AppleScript-desktop integration** "
    "(e.g. playwright). Initial action-tool growth (early 2025) was "
    "concentrated in software-extension tools and code-execution tools; "
    "from mid-2025 onward, general computer-use tools have captured the "
    "majority of new action-tool downloads.",
    title="5.3 driver: general-purpose computer-use tools (browser, AppleScript, etc.)",
)

# ---------------------------------------------------------------------------
# 5.4 Generality over time (Figure 5)
# ---------------------------------------------------------------------------

claim_generality_overall_shares = claim(
    "**Generality overall shares (panel-wide).** Across the full panel:\n\n"
    "| Generality | Download share | Tool share |\n"
    "|---|---:|---:|\n"
    "| **General-purpose (unconstrained)** | **45.4%** | 14.3% |\n"
    "| Narrow-purpose (constrained) | 54.6% | 85.7% |\n",
    title="5.4 panel-wide: general-purpose 45.4% downloads, 14.3% tools",
    background=[setup_attribute_generality],
)

claim_finding_general_purpose_growth = claim(
    "**Finding 5.4 (RQ4, top of Fig 5).** The download-weighted share of "
    "**general-purpose** tools (operating in unconstrained environments "
    "like the open web) rose from **41% in 11/2024 to 50% in 02/2026**. "
    "A polynomial-convergence WLS fit reports an asymptotic limit of "
    "$L = 55\\%$ (95% CI [50%, 100%], $R^2 = 0.84$).",
    title="5.4 general-purpose download share: 41% -> 50% (asymptote ~55%)",
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 5 (top panel)"},
)

claim_finding_general_purpose_count_stable = claim(
    "**Finding 5.4 (count basis, bottom of Fig 5).** When measured by "
    "*cumulative server count* rather than downloads, the general-purpose "
    "share stays stable at **~21%**, with a polynomial-convergence "
    "asymptote $L = 21\\%$ (95% CI [21%, 21%], $R^2 \\approx 0$). Thus "
    "the rise in *download-weighted* general-purpose share is driven "
    "by disproportionate *adoption* of a small population of "
    "general-purpose servers, not by their number growing faster than "
    "narrow-purpose servers.",
    title="5.4 general-purpose count-share is stable at ~21% -- adoption, not creation",
)

claim_finding_general_purpose_action_correlation = claim(
    "**Finding 5.4 (cross-tab key result).** **94% of general-purpose "
    "server downloads involve action tools**, while perception tools "
    "remain predominantly narrow-purpose (95% of downloaded perception "
    "tools operate in constrained environments, e.g. API-mediated data "
    "access). This correlation implies that **potentially consequential "
    "agent actions are increasingly happening in the *least controlled* "
    "environments** -- web browsers, arbitrary code execution -- rather "
    "than in restricted, secure API integrations.",
    title="5.4 94% of general-purpose downloads are action; 95% of perception is narrow",
)

# ---------------------------------------------------------------------------
# 5.5 AI co-authorship over time (Figure 6)
# ---------------------------------------------------------------------------

claim_aiauth_overall_shares = claim(
    "**AI co-authorship overall shares (panel-wide, first-month variant).** "
    "AI assistance is detected in:\n\n"
    "| Unit | Count | Share |\n"
    "|---|---:|---:|\n"
    "| MCP servers with AI evidence in first-month commits | 5,494 of "
    "19,388 | **28.3%** |\n"
    "| Tools on AI-coauthored servers | 64,489 of 177,436 | **36.3%** |\n",
    title="5.5 panel-wide: 28.3% of servers / 36.3% of tools are AI-coauthored",
)

claim_observation_aiauth_jan2025 = claim(
    "**Per-month observation (Jan 2025).** At the start of measurable AI "
    "assistance (January 2025), only **6%** of newly created MCP servers "
    "showed first-month AI-authorship evidence.",
    title="Observation: AI-coauthored share of new servers = 6% in 01/2025",
)

claim_observation_aiauth_feb2026 = claim(
    "**Per-month observation (Feb 2026).** By the end of the panel "
    "(February 2026), **62%** of newly created MCP servers showed "
    "first-month AI-authorship evidence.",
    title="Observation: AI-coauthored share of new servers = 62% in 02/2026",
)

claim_observation_aiauth_intermediate = claim(
    "**Per-month observation (intermediate months, Figure 6).** The monthly "
    "AI-coauthored share traces a near-monotonic ascending curve "
    "from 6% in 01/2025 to 62% in 02/2026. A WLS quadratic fit "
    "weighted by monthly server count reports $R^2 = 0.97$ and an "
    "average marginal change of **+4.10 pp/month** (95% CI "
    "[+3.55, +4.65] via the delta method), making each intermediate "
    "monthly share a tightly-clustered observation around the rising "
    "trend.",
    title="Observation: intermediate monthly AI-coauthored shares trace +4.10pp/month",
    metadata={"figure": "artifacts/2603.23802.pdf, Figure 6"},
)

claim_finding_aiauth_growth = claim(
    "**Finding 5.5 (RQ5).** The share of newly created MCP servers with "
    "first-month detected AI assistance rose from **6% in January 2025 "
    "to 62% in February 2026** -- a 56-percentage-point increase in 13 "
    "months. AI-assisted tool creation is now the *modal* mode of MCP "
    "server creation. Among AI-coauthored servers, **Claude (3,770 "
    "servers, 68.6%) dominates**, followed by Cursor (507, 9.2%), "
    "Copilot (502, 9.1%), and Codex (328, 6.0%, combining ChatGPT and "
    "Codex).",
    title="5.5 AI-coauthored share of new servers: 6% -> 62% (Claude 69% of those)",
)

# ---------------------------------------------------------------------------
# Comparative claim: how the MCP-tool view differs from chatbot studies
# ---------------------------------------------------------------------------

claim_comparison_with_chatbot_studies = claim(
    "**Comparison with prior chatbot/agent usage studies (Table 3).** "
    "The MCP-tool dataset and prior LLM/agent platform studies "
    "[@Aubakirova2025; @Handa2025Claude; @Chatterji2025ChatGPT; "
    "@Yang2025Comet; @Appel2026EconIndex] agree on the qualitative US "
    "and IT/computational concentration of agent-related activity. The "
    "MCP-tool view is *more* IT-skewed (92% of downloads in Computer & "
    "Mathematical SOC vs 30-58% on chatbot platforms), reflecting that "
    "MCP servers are mostly developer-published, while the relative "
    "importance of arts, education, and life sciences is lower in MCP "
    "than in chatbot conversation data.",
    title="MCP-tool view is more IT-skewed than chatbot conversation data",
)

__all__ = [
    "claim_table6_taskdomains",
    "claim_finding_it_dominates",
    "claim_finding_finance_share",
    "claim_figure2_consequentiality",
    "claim_finding_action_medium_stakes",
    "claim_finding_finance_highstakes_outlier",
    "claim_figure3_geography",
    "claim_finding_action_us_concentration",
    "claim_directimpact_overall_shares",
    "claim_observation_action_share_nov2024",
    "claim_observation_action_share_feb2026",
    "claim_observation_action_share_intermediate",
    "claim_finding_action_growth",
    "claim_finding_action_growth_official",
    "claim_finding_action_growth_driver",
    "claim_generality_overall_shares",
    "claim_finding_general_purpose_growth",
    "claim_finding_general_purpose_count_stable",
    "claim_finding_general_purpose_action_correlation",
    "claim_aiauth_overall_shares",
    "claim_observation_aiauth_jan2025",
    "claim_observation_aiauth_feb2026",
    "claim_observation_aiauth_intermediate",
    "claim_finding_aiauth_growth",
    "claim_comparison_with_chatbot_studies",
]
