"""Priors for independent (leaf) claims in the 2603.23802 formalization.

Priors are calibrated against the source paper's qualitative confidence
language (Section 3 methodology, Section 4 validation kappa, Appendix
A.1) and against external commonly-accepted facts.
"""

from .motivation import (
    claim_evidence_gap,
    claim_prior_assumption_action_rare,
)
from .s2_background import (
    claim_action_space_amplifies_misalignment,
    claim_action_space_amplifies_misuse,
    claim_action_space_amplifies_structural,
    claim_existing_evidence_gap_breakdown,
    claim_mcp_early_indicator,
    claim_self_improvement_risk,
    claim_table1_examples,
    claim_table2_examples,
)
from .s3_data import (
    claim_data_sources,
    claim_dataset_scale,
    claim_downloads_as_usage_proxy,
    claim_downloads_concentration,
    claim_geography_subsample,
    claim_official_subset_definition,
    claim_validation_pipeline,
)
from .s4_methodology import (
    claim_aiauth_criteria,
    claim_aiauth_firstmonth_variant,
    claim_aiauth_lower_bound,
    claim_bottomup_pipeline,
    claim_bottomup_validation,
    claim_consequentiality_score,
    claim_directimpact_classification,
    claim_directimpact_taxonomy,
    claim_directimpact_validation,
    claim_generality_classification,
    claim_generality_taxonomy,
    claim_generality_validation,
    claim_geography_methodology,
    claim_topdown_pipeline,
    claim_topdown_validation,
    claim_wls_regression,
)
from .s5_findings import (
    claim_figure2_consequentiality,
    claim_figure3_geography,
    claim_generality_overall_shares,
    claim_table6_taskdomains,
)
from .s6_case_study import (
    claim_figure7_payments_growth,
    claim_regulator_use_case_validation,
    claim_table7_methods_comparison,
)
from .s7_reasoning import (
    claim_counter_uniform_stakes,
    claim_pred_alt_random,
    claim_pred_h_general_purpose_drives,
)

PRIORS: dict = {
    # ---- Motivation: literature gaps -----------------------------------
    claim_evidence_gap: (
        0.92,
        "Direct literature survey of the seven prior agent-usage "
        "studies cited (Table 3); gap is documented in Section 1 with "
        "explicit citations to each study covered.",
    ),
    claim_prior_assumption_action_rare: (
        0.55,
        "A baseline policy view; some practitioner surveys (Pan et al. "
        "2025) report restrictive deployment patterns consistent with "
        "this view, but the overall ecosystem-level prior is contested. "
        "Set near-uniform to let the contradiction with empirical "
        "findings drive the BP outcome.",
    ),
    # ---- s2 Background: risk amplification channels --------------------
    claim_action_space_amplifies_misuse: (
        0.88,
        "Well-supported by documented misuse incidents (cyber criminals "
        "exploiting agents to leak sensitive data and transfer "
        "cryptocurrency, [@Hou2025MCP]). The general principle is "
        "broadly accepted in the security literature.",
    ),
    claim_action_space_amplifies_misalignment: (
        0.92,
        "Multiple documented production incidents (database deletion, "
        "patient-record exposure, [@Anthropic2025Misalignment] simulated "
        "blackmail). The 'tools must exist for misalignment to "
        "manifest' principle is near-tautological.",
    ),
    claim_action_space_amplifies_structural: (
        0.78,
        "Structural-risk scenarios (agent bank runs, content "
        "homogenisation) are plausible but largely theoretical at the "
        "panel's date; only entry-level developer job-market effects "
        "[@Brynjolfsson2025Canaries] provide direct empirical evidence.",
    ),
    claim_self_improvement_risk: (
        0.85,
        "AI agents creating their own tools is empirically demonstrable "
        "(Section 5.5 finds 28-36% of MCP tools are AI-coauthored). The "
        "amplification mechanism is a straightforward consequence.",
    ),
    claim_existing_evidence_gap_breakdown: (
        0.95,
        "Direct tabulation of seven cited prior studies (Table 3). "
        "Verifiable claim about what each study does and does not "
        "report.",
    ),
    claim_table1_examples: (
        0.95,
        "Concrete examples of public MCP servers (Ticketmaster MCP, "
        "BioMCP, Coinbase MCP, DuckDuckGo MCP, A11Y MCP, Desktop "
        "Commander MCP). Each is independently verifiable as a public "
        "repository.",
    ),
    claim_table2_examples: (
        0.92,
        "Concrete examples of public MCP servers in each "
        "(geography x stakes) cell; verifiable as the most-used server "
        "per cell from the dataset.",
    ),
    claim_mcp_early_indicator: (
        0.9,
        "Specific verifiable example given (Google Calendar MCP "
        "published Dec 5, 2024; Anthropic and OpenAI integrated April "
        "and August 2025). The general 'developer publication leads "
        "vendor integration' pattern is broadly supported.",
    ),
    # ---- s3 Data: methodology and dataset facts ------------------------
    claim_data_sources: (
        0.95,
        "Direct procedural description of the data harvest; counts are "
        "tabulated and reproducible.",
    ),
    claim_validation_pipeline: (
        0.9,
        "LLM-validated filtering with Sonnet 4.5; 73,338 -> 19,388 "
        "selection ratio is reasonable and the criterion (servers "
        "exposing tools in README) is operationalised.",
    ),
    claim_dataset_scale: (
        0.95,
        "Direct dataset tabulation; numbers are mechanically derivable "
        "from the harvested files.",
    ),
    claim_official_subset_definition: (
        0.92,
        "Operational definition of 'official' (legally registered "
        "commercial entities marked on MCP-server lists); 8,469 / 45M "
        "tally is mechanically derivable.",
    ),
    claim_downloads_as_usage_proxy: (
        0.85,
        "Standard practice in package-ecosystem studies; the paper "
        "explicitly acknowledges the install-vs-call gap and provides "
        "Smithery cross-validation showing modest developer bias.",
    ),
    claim_downloads_concentration: (
        0.95,
        "Direct distributional statistic computable from the dataset; "
        "no estimation uncertainty.",
    ),
    claim_geography_subsample: (
        0.93,
        "Direct sub-sample tabulation: 528 servers, 11.91M downloads. "
        "Mechanically derivable.",
    ),
    # ---- s4 Methodology -------------------------------------------------
    claim_topdown_pipeline: (
        0.9,
        "Three-level hierarchical LLM classifier adapted from Anthropic's "
        "Claude.ai pipeline ([@Handa2025Claude]); methodology is "
        "established and reproducible.",
    ),
    claim_topdown_validation: (
        0.9,
        "78% server / 74% tool agreement at L1 with Fleiss kappa = "
        "0.32-0.57 (n=14 raters x 100 items each); blind protocol; "
        "Anthropic's earlier non-blind validation reported similar "
        "ranges.",
    ),
    claim_bottomup_pipeline: (
        0.9,
        "Standard BERTopic pipeline (Stella-400M -> UMAP -> HDBSCAN), "
        "well-established in topic modelling [@Grootendorst2022BERTopic].",
    ),
    claim_bottomup_validation: (
        0.85,
        "25% outlier rate and 50% topic coherence (42% on test set) are "
        "in the typical range for BERTopic on noisy text.",
    ),
    claim_consequentiality_score: (
        0.9,
        "O*NET impact-of-decisions is a long-established US Department "
        "of Labor occupational survey instrument; the 0-100 scaling is "
        "standard.",
    ),
    claim_geography_methodology: (
        0.85,
        "PyPI IP-based geolocation is a documented PyPI-supported data "
        "channel (Linehaul); Western-skew limitation is explicitly "
        "acknowledged.",
    ),
    claim_directimpact_taxonomy: (
        0.92,
        "Directly adopted from CAISI's [@CAISI2025] published 11-way "
        "tool-use taxonomy; an authoritative public source.",
    ),
    claim_directimpact_classification: (
        0.88,
        "Sonnet 4.5 tool-level classification using the CAISI taxonomy; "
        "reliability anchored by validation kappa (separate claim).",
    ),
    claim_directimpact_validation: (
        0.92,
        "81% agreement / Fleiss kappa = 0.7 (substantial range) on "
        "perception/reasoning/action with 14 raters x 100 items each. "
        "Strong human validation.",
    ),
    claim_generality_taxonomy: (
        0.9,
        "Directly adopted from CAISI [@CAISI2025]; the binary "
        "constrained/unconstrained distinction is conceptually sharp.",
    ),
    claim_generality_classification: (
        0.82,
        "Sonnet 4.5 server-level generality classification; reliability "
        "lower than direct-impact classification due to genuine "
        "borderline cases.",
    ),
    claim_generality_validation: (
        0.78,
        "72% agreement / Fleiss kappa = 0.3 (fair range) with 6 raters "
        "x 100 items. Lower than direct-impact validation, but the "
        "generality boundary is genuinely fuzzy.",
    ),
    claim_aiauth_criteria: (
        0.88,
        "Four GitHub-metadata signals are directly observable; "
        "Co-Authored-By trailers and config files are essentially "
        "unambiguous; bot accounts and explicit mentions carry some "
        "false-positive risk.",
    ),
    claim_aiauth_firstmonth_variant: (
        0.93,
        "Direct procedural restriction (30-day window from repo "
        "creation); deterministic given the four-signal detector.",
    ),
    claim_aiauth_lower_bound: (
        0.92,
        "Pangram cross-validation (28.2% overlap on 197-repo sample) "
        "directly demonstrates undercount; the 'lower bound' framing is "
        "well-justified.",
    ),
    claim_wls_regression: (
        0.92,
        "Standard panel-data regression methodology; specifications "
        "(linear, quadratic, asymptotic, polynomial-convergence) are "
        "reported per figure with R^2 and confidence intervals.",
    ),
    # ---- s5 Findings: independent observations and figures -------------
    claim_table6_taskdomains: (
        0.93,
        "Direct tabulation of L1 task-domain shares from the validated "
        "top-down classifier; mechanically derivable conditional on "
        "classifier output.",
    ),
    claim_figure2_consequentiality: (
        0.9,
        "Figure 2 plots count-of-action-tools vs O*NET impact score per "
        "occupation; quadratic fit R^2 ~ 0.03 with F-test p=0.015. The "
        "underlying scatter is mechanically reproducible.",
    ),
    claim_figure3_geography: (
        0.92,
        "Direct PyPI-IP geolocation tabulation for the 528-server "
        "geo-sample; numbers are reproducible from PyPI download logs.",
    ),
    claim_generality_overall_shares: (
        0.88,
        "Direct panel-wide aggregate from the generality classifier; "
        "uncertainty inherits from the classifier's fair-range kappa.",
    ),
    # ---- s6 Case study --------------------------------------------------
    claim_figure7_payments_growth: (
        0.92,
        "Direct count of payment-MCP servers per month from the "
        "payments-autonomy classifier (which has 83% / Fleiss kappa = "
        "0.42 human agreement). The 47 -> 1,578 growth is robust to "
        "modest classifier noise.",
    ),
    claim_regulator_use_case_validation: (
        0.95,
        "Acknowledgements section names AISI and Bank of England staff "
        "who collaborated; a verifiable institutional claim.",
    ),
    claim_table7_methods_comparison: (
        0.85,
        "Comparative methodology table; the classifications "
        "(early-indicator, coverage, etc.) are reasoned arguments "
        "rather than empirically measured. Author's expert "
        "characterisation.",
    ),
    # ---- s7 Synthesis: hypothesis and counter-hypothesis priors --------
    claim_pred_h_general_purpose_drives: (
        0.85,
        "If the general-purpose-tooling hypothesis is correct, the "
        "auxiliary predictions follow logically and are reported as "
        "observed.",
    ),
    claim_pred_alt_random: (
        0.3,
        "If the noise alternative held, its predicted observables "
        "(non-monotonicity, low R^2, trend disappearing on commercial "
        "subset) would manifest. They do not, so this prediction's "
        "compatibility with observation is low.",
    ),
    claim_counter_uniform_stakes: (
        0.25,
        "Counter-hypothesis used to formalise the action-stakes "
        "contradiction. Empirically false (action tools cluster at "
        "medium stakes with finance outlier), so prior is low; the "
        "contradiction operator will further suppress it.",
    ),
}
