"""Section 4: Methodology -- classification pipelines.

Section 4 of Stein 2026 [@Stein2026]. Specifies four classification
pipelines applied to the 177k tools / 19k servers:

* 4.1 -- task-domain mapping via O*NET, with a bottom-up BERTopic
  validation pipeline and a top-down hierarchical LLM classifier
  (12 L1 categories, 400 L2 clusters, 18,796 L3 O*NET tasks),
  plus an O*NET impact-of-decisions score for consequentiality.
* 4.2 -- geographic mapping via PyPI IP-geolocated download counts.
* 4.3 -- direct-impact classification (perception/reasoning/action)
  via Claude Sonnet 4.5, validated by 14 ML-trained human raters.
* 4.4 -- generality classification (constrained/unconstrained) via
  Claude Sonnet 4.5, validated by 6 raters.
* 4.5 -- AI co-authorship detection via four GitHub-metadata
  signals (Co-Authored-By, AI config files, bot accounts, mentions).

The methodology claims here are *premises* for the empirical findings
in s5; their validation rests on the human-validation agreement
statistics (Fleiss' kappa) reported here and in Appendix A.1.
"""

from gaia.lang import claim, setting

from .motivation import setup_mcp_definition
from .s2_background import (
    setup_attribute_aicoauth,
    setup_attribute_direct_impact,
    setup_attribute_generality,
    setup_attribute_task_domain,
)

# ---------------------------------------------------------------------------
# 4.1 Task domain via O*NET
# ---------------------------------------------------------------------------

setup_onet_taxonomy = setting(
    "**O*NET taxonomy.** O*NET (US Department of Labor) "
    "[@ONET2025] is a taxonomy of **18,796 task descriptions across "
    "1,016 occupations**, organised into **23 major Standard "
    "Occupational Classification (SOC) groups**. The paper uses O*NET "
    "as the canonical task taxonomy for cross-study comparability, "
    "matching prior LLM-usage studies such as Anthropic's Claude.ai "
    "analysis [@Handa2025Claude] and Chatterji et al. [@Chatterji2025ChatGPT].",
    title="Setup: O*NET task and SOC occupational taxonomies",
)

claim_bottomup_pipeline = claim(
    "**Bottom-up validation pipeline.** A standard topic-modelling "
    "pipeline is used to verify the top-down O*NET assignment and to "
    "discover sub-clusters within each domain: (1) embed each MCP "
    "server's title + description + README summary using "
    "**Stella_en_400M_v5** sentence transformer (1024-dim), (2) apply "
    "**UMAP** dimensionality reduction to 5-dim, and (3) cluster with "
    "**HDBSCAN** (min_cluster_size=0.3% of dataset, min_samples=30% of "
    "min_cluster, cluster_selection_epsilon=0.02), tuned to yield 40-60 "
    "topics [@Grootendorst2022BERTopic]. Cluster names are produced by "
    "Claude Sonnet 4.5 in '<2 words> tools' format from the top 10 terms "
    "and 5 sampled descriptions.",
    title="4.1 bottom-up: BERTopic pipeline (Stella -> UMAP -> HDBSCAN)",
    background=[setup_attribute_task_domain],
)

claim_bottomup_validation = claim(
    "**Bottom-up validation metrics.** The clustering achieves an outlier "
    "rate of **25%** on the main set (26% on a held-out test set), and "
    "**topic coherence of 50%** on the main set (42% on the held-out test "
    "set), measured per Roder et al. [@Roder2015]. The authors describe "
    "these as 'reasonable outlier rate' and 'high topic coherence', "
    "indicating the bottom-up clusters are well-formed.",
    title="4.1 bottom-up: 25% outliers, 50% topic coherence",
)

claim_topdown_pipeline = claim(
    "**Top-down O*NET classification pipeline.** Each tool is mapped to "
    "an O*NET task using **three-level hierarchical LLM classification** "
    "(adapted from Anthropic's Claude.ai pipeline, Appendix A.2 of "
    "[@Handa2025Claude]). The hierarchy is constructed once: (i) embed "
    "all 18,796 O*NET task descriptions using stella_en_400M_v5 "
    "(augmented with occupation context); (ii) cluster into 400 "
    "**Level-2 (L2) clusters** via K-means (k=400, n_init=10), avg "
    "cluster size 47 tasks; (iii) assign each L2 cluster to one of 12 "
    "predefined **Level-1 (L1) categories** by maximum cosine similarity "
    "between cluster centroid and category embedding (avg similarity "
    "0.61, range 0.45-0.82); (iv) generate L2 cluster names with Claude "
    "Sonnet 4 using *contrastive* prompting against neighbouring "
    "clusters. At inference time, each tool is classified by the LLM in "
    "three sequential prompts: select L1 -> select L2 in chosen L1 -> "
    "select L3 (O*NET task) in chosen L2. This addresses the fact that "
    "all 18,796 O*NET tasks do not fit in any LLM context window.",
    title="4.1 top-down: 3-level hierarchical (12/400/18,796) LLM classifier",
    background=[setup_onet_taxonomy],
)

claim_topdown_validation = claim(
    "**Top-down validation -- L1 task domain.** 14 human validators with "
    "ML Master's or PhD degrees (sourced via Prolific) each labelled "
    "n = 100 random items in a *blind* protocol (assigning items to "
    "occupational tasks at the top hierarchy level, rather than judging "
    "whether the LLM's choice was 'acceptable'). Agreement with Claude "
    "Sonnet 4.5 was **78% on MCP-server level (Fleiss' kappa = 0.32)** "
    "and **74% on tool level (Fleiss' kappa = 0.57)**. L2 and L3 "
    "agreement is lower due to the extreme specificity of O*NET tasks "
    "and the broader remit of many MCP tools (e.g. GPT-5 vs Sonnet 4.5 "
    "agreement at <70% at lower levels), so the paper reports only "
    "*highest-level* (L1 task domain and SOC cluster) statistics.",
    title="4.1 validation: 78% server / 74% tool agreement at L1 (k=0.32-0.57)",
)

claim_consequentiality_score = claim(
    "**Consequentiality (impact of decisions) score.** Each tool inherits "
    "the consequentiality of the SOC occupations it supports, using "
    "O*NET's [@ONET2025] *Impact of Decisions on Co-workers or Company "
    "Results* survey: 'What results do your decisions usually have on "
    "other people or the image or reputation or financial resources of "
    "your employer?' Scores are on the **0-100 scale**: low (<50), "
    "medium (50-75), high (>75).",
    title="Consequentiality: O*NET impact-of-decisions score (0-100)",
    background=[setup_onet_taxonomy],
)

# ---------------------------------------------------------------------------
# 4.2 Geography
# ---------------------------------------------------------------------------

claim_geography_methodology = claim(
    "**Geography methodology.** Country-level geographic splits are "
    "obtained from **PyPI download IP-address data** [@Stein2026], "
    "available for a subset of PyPI downloads. Splits are **not available "
    "for NPM**, and not available for PyPI in 11/2025-02/2026 at the "
    "time of writing. The geographic share therefore reflects PyPI's "
    "Western-skewed user base.",
    title="4.2 geography: PyPI IP-based country splits (Western-biased)",
)

# ---------------------------------------------------------------------------
# 4.3 Direct impact
# ---------------------------------------------------------------------------

claim_directimpact_taxonomy = claim(
    "**Direct-impact taxonomy (Table 4, adapted from CAISI [@CAISI2025]).** "
    "Each tool is classified into one of 11 functionality sub-categories, "
    "grouped into 3 direct-impact classes:\n\n"
    "| Direct impact | Functionality | Examples |\n"
    "|---|---|---|\n"
    "| **Perception** | Sensors | Database query, monitoring, GUI read, "
    "voice, internet search, physical sensing |\n"
    "| **Reasoning** | Planning | Task-decomposition, path-finding |\n"
    "| | Analysis | Scratchpads, calculators, simulations |\n"
    "| | Resource mgmt. | Memory, self-management |\n"
    "| **Action** | Authentication | Login, CAPTCHA, wallet |\n"
    "| | Computer use | Application-specific GUI, web automation, "
    "computer use |\n"
    "| | Running code | Sandboxed interpreter, file ops, code execution |\n"
    "| | Software extensions | Calendar, social-media API |\n"
    "| | Physical extensions | Robotic arm, lab tools, robot in open env |\n"
    "| | Human interaction | Phone calls |\n"
    "| | Agent interaction | Multi-agent workflows |\n",
    title="Table 4: 11-way direct-impact x functionality taxonomy",
    background=[setup_attribute_direct_impact],
    metadata={"source_table": "artifacts/2603.23802.pdf, Table 4"},
)

claim_directimpact_classification = claim(
    "**Direct-impact classification.** Each of the 177k tools is "
    "classified by **Claude Sonnet 4.5** into one of the 3 direct-impact "
    "classes and one of the 11 functionality sub-classes following "
    "CAISI's [@CAISI2025] taxonomy (prompt in Appendix A.4.4). "
    "Classification is performed at *tool level*, not server level, "
    "because a single MCP server typically bundles tools of mixed "
    "direct-impact (e.g. `read_file` perception + `edit_file` action).",
    title="4.3 direct impact: Sonnet 4.5 tool-level (perception/reasoning/action)",
    background=[setup_attribute_direct_impact],
)

claim_directimpact_validation = claim(
    "**Direct-impact human validation.** 14 human validators (n = 100 "
    "items each) reach **81% agreement (Fleiss' kappa = 0.7)** with "
    "Sonnet 4.5 on the perception/reasoning/action label, and **85% "
    "(Fleiss' kappa = 0.5)** on the functionality sub-label conditional "
    "on matching direct impact. When the label is propagated to server "
    "level (max direct impact across the server's tools), human "
    "validators reach **78% agreement (Fleiss' kappa = 0.5)**. These "
    "kappa values fall in the 'substantial' range, supporting the "
    "reliability of LLM-based direct-impact classification.",
    title="4.3 validation: 81% (k=0.7) on direct impact -- substantial agreement",
)

# ---------------------------------------------------------------------------
# 4.4 Generality
# ---------------------------------------------------------------------------

claim_generality_taxonomy = claim(
    "**Generality taxonomy (Table 5, adapted from CAISI [@CAISI2025]).** "
    "Two-class:\n\n"
    "| Generality | Examples |\n"
    "|---|---|\n"
    "| **Narrow-purpose (constrained env.)** | Access to specific software "
    "or platform via API, data retrieval |\n"
    "| **General-purpose (unconstrained env.)** | Deep research, browser "
    "use, computer use |\n",
    title="Table 5: 2-class generality taxonomy",
    background=[setup_attribute_generality],
    metadata={"source_table": "artifacts/2603.23802.pdf, Table 5"},
)

claim_generality_classification = claim(
    "**Generality classification.** Each MCP server is classified by "
    "Claude Sonnet 4.5 as narrow-purpose (constrained environment) or "
    "general-purpose (unconstrained environment). Generality is assigned "
    "at **server level** (not tool level), because a server typically "
    "bundles tools that all interact with the same environment, and the "
    "label is then inherited by all the server's tools.",
    title="4.4 generality: Sonnet 4.5 server-level (constrained/unconstrained)",
    background=[setup_attribute_generality],
)

claim_generality_validation = claim(
    "**Generality human validation.** Six human experts each labelled "
    "n = 100 servers, reaching **72% agreement (Fleiss' kappa = 0.3, "
    "'fair')** with Sonnet 4.5. This is lower than for direct-impact "
    "classification, reflecting genuine semantic ambiguity in deciding "
    "whether an environment is 'constrained' (e.g. some platform APIs "
    "are very broad). Generality-share trends should therefore be "
    "interpreted as approximate.",
    title="4.4 validation: 72% (k=0.3, fair) -- generality is harder",
)

# ---------------------------------------------------------------------------
# 4.5 AI co-authorship
# ---------------------------------------------------------------------------

claim_aiauth_criteria = claim(
    "**AI-authorship detection (four GitHub-metadata signals).** A server "
    "is flagged as AI-coauthored if **any one** of four pieces of "
    "evidence is found via the GitHub REST API:\n\n"
    "1. **Co-Authored-By trailers** in commit messages or PR bodies "
    "referencing known AI tools (Claude Code, GitHub Copilot, ChatGPT, "
    "etc.) -- the most reliable signal.\n"
    "2. **AI configuration files** in the repository tree (e.g. "
    "`CLAUDE.md`, `.cursorrules`).\n"
    "3. **Bot accounts** (e.g. `copilot[bot]`) appearing as commit or PR "
    "authors.\n"
    "4. **Explicit AI tool mentions** in commit messages or PR bodies "
    "(e.g. `@codex`) -- highest false-positive risk.\n\n"
    "The scan covers up to 10,000 commits, the 30 most recent PRs, and "
    "the full file tree. Each repository's most-likely AI agent is "
    "identified by weighted scoring: config files (10), bots (5), "
    "Co-Authored-By (3), mentions (1).",
    title="4.5 AI-authorship: 4 OR-combined GitHub signals",
    background=[setup_attribute_aicoauth],
)

claim_aiauth_firstmonth_variant = claim(
    "**First-month restricted variant.** To distinguish AI assistance "
    "*present from project inception* from AI tools adopted later, the "
    "paper computes a 'first-month' variant of AI-authorship: the same "
    "four criteria are evaluated only against commits and PRs dated "
    "**within 30 days of repository creation**, and configuration files "
    "are checked at the file tree of the latest commit within that "
    "30-day window. This reduces false-positive retroactive labelling "
    "and is the variant used for time-trend figures (Figure 1 panels b "
    "and d, Figure 6, and the 28%/36% headline numbers in Section 5.5).",
    title="4.5 first-month variant: AI evidence within 30 days of repo creation",
)

claim_aiauth_lower_bound = claim(
    "**AI-authorship is a lower bound.** The detection procedure can only "
    "capture *clearly labelled* AI footprints (commit trailers, config "
    "files, bot accounts, explicit mentions). It cannot detect AI usage "
    "that leaves no git trace -- e.g. copy-pasting from a web chat "
    "interface, AI-generated code committed under a human author, or "
    "squashed merges that hide Co-Authored-By trailers. Cross-validation "
    "against the Pangram commercial AI-content detector on a 197-repo "
    "sub-sample shows the conservative procedure captures only **28.2% "
    "of repositories whose READMEs Pangram classifies as 'significantly "
    "AI-generated'** (53.3% binary agreement). Reported AI-authorship "
    "shares are therefore lower bounds on the true rate.",
    title="4.5 limitation: detected AI authorship is a lower bound",
)

# ---------------------------------------------------------------------------
# 4.3 trend regression methodology
# ---------------------------------------------------------------------------

claim_wls_regression = claim(
    "**Time-trend regression methodology.** Throughout Sections 5 and 6, "
    "monthly observations are fit with **weighted least squares (WLS)** "
    "regressions, weighted by monthly download count (where applicable). "
    "Regression form (linear, quadratic, asymptotic-convergence "
    "$y(t) = L - (L - y_0) e^{-kt}$, or polynomial-convergence "
    "$y = L - \\exp(a + bt + ct^2)$) is chosen per figure to balance "
    "simplicity and explanatory power; the chosen specification is "
    "reported in the figure legend along with the asymptotic limit "
    "$L$ and 95% confidence intervals (parameter-covariance or wild "
    "bootstrap, as noted).",
    title="Time-trend method: download-weighted WLS with reported CI",
)

__all__ = [
    "setup_onet_taxonomy",
    "claim_bottomup_pipeline",
    "claim_bottomup_validation",
    "claim_topdown_pipeline",
    "claim_topdown_validation",
    "claim_consequentiality_score",
    "claim_geography_methodology",
    "claim_directimpact_taxonomy",
    "claim_directimpact_classification",
    "claim_directimpact_validation",
    "claim_generality_taxonomy",
    "claim_generality_classification",
    "claim_generality_validation",
    "claim_aiauth_criteria",
    "claim_aiauth_firstmonth_variant",
    "claim_aiauth_lower_bound",
    "claim_wls_regression",
]
