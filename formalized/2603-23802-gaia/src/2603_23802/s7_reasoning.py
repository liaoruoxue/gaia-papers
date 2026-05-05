"""Section 7 (synthesis): inferential connections across the paper.

This module is *not* a section of the source paper. It carries the
reasoning strategies that connect the atomic claims extracted in
modules motivation through s6:

* Methodology -> findings supports (e.g. validated direct-impact
  classification + monthly download data -> the Nov-2024 and Feb-2026
  action-share observations).
* Inductions over the per-month observations to the headline time
  trends (action share, AI-coauthorship share).
* Abductions where the paper compares its empirical findings against
  baseline assumptions or competing explanations (action-tool growth
  vs random fluctuation; the misalignment thesis vs alternative
  explanations).
* Contradictions between the paper's empirical findings and the
  baseline policy assumption that action tools are rare.
* The synthesis chain that takes Sections 5-6 findings -> the
  Section 6 governance thesis -> the Section 7 conclusion.
"""

from gaia.lang import (
    abduction,
    claim,
    compare,
    contradiction,
    induction,
    support,
)

from .motivation import (
    claim_contribution_dataset,
    claim_contribution_governance,
    claim_contribution_timetrend,
    claim_evidence_gap,
    claim_finding_action_share_growth,
    claim_finding_action_stakes_distribution,
    claim_finding_ai_coauthorship_growth,
    claim_finding_software_dominates,
    claim_finding_us_concentration,
    claim_prior_assumption_action_rare,
    claim_tools_proxy_for_action_space,
)
from .s2_background import (
    claim_action_space_amplifies_misalignment,
    claim_action_space_amplifies_misuse,
    claim_action_space_amplifies_structural,
    claim_existing_evidence_gap_breakdown,
    claim_large_action_space_amplifies_risk,
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
from .s5_findings import (
    claim_comparison_with_chatbot_studies,
)
from .s6_case_study import (
    claim_limitation_lower_bound,
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
    claim_aiauth_overall_shares,
    claim_directimpact_overall_shares,
    claim_figure2_consequentiality,
    claim_figure3_geography,
    claim_finding_action_growth,
    claim_finding_action_growth_driver,
    claim_finding_action_growth_official,
    claim_finding_action_medium_stakes,
    claim_finding_action_us_concentration,
    claim_finding_aiauth_growth,
    claim_finding_finance_highstakes_outlier,
    claim_finding_finance_share,
    claim_finding_general_purpose_action_correlation,
    claim_finding_general_purpose_count_stable,
    claim_finding_general_purpose_growth,
    claim_finding_it_dominates,
    claim_generality_overall_shares,
    claim_observation_action_share_feb2026,
    claim_observation_action_share_intermediate,
    claim_observation_action_share_nov2024,
    claim_observation_aiauth_feb2026,
    claim_observation_aiauth_intermediate,
    claim_observation_aiauth_jan2025,
    claim_table6_taskdomains,
)
from .s6_case_study import (
    claim_conclusion_action_space_expanded,
    claim_disc_attack_surface,
    claim_disc_governance_complication,
    claim_disc_misalignment_consequences,
    claim_disc_software_finance_concentration,
    claim_disc_unconstrained_structural,
    claim_figure7_payments_growth,
    claim_finding_crypto_payment_trend,
    claim_governance_thesis,
    claim_regulator_use_case_validation,
    claim_table7_methods_comparison,
)

# ===========================================================================
# Block A: Background reasoning (Section 2 thesis)
# ===========================================================================

# A.1 -- The risk-amplification thesis from the four risk-channel claims.
strat_large_action_space_amplifies_risk = support(
    [
        claim_action_space_amplifies_misuse,
        claim_action_space_amplifies_misalignment,
        claim_action_space_amplifies_structural,
        claim_self_improvement_risk,
    ],
    claim_large_action_space_amplifies_risk,
    reason=(
        "The Section 2 thesis that 'large action space amplifies "
        "agent risks' is built by aggregating four channel-specific "
        "arguments: (i) misuse risks scale with the attack-surface "
        "exposure that action tools create "
        "(@claim_action_space_amplifies_misuse), (ii) mistake/"
        "misalignment risks materialise only when the agent has action "
        "tools to execute incorrect intentions "
        "(@claim_action_space_amplifies_misalignment), (iii) structural "
        "risks arise from correlated action of many agents using the "
        "same general-purpose tools "
        "(@claim_action_space_amplifies_structural), and (iv) AI agents "
        "creating their own tools accelerates action-space growth "
        "beyond human oversight (@claim_self_improvement_risk). All "
        "four channels share the property that *more action / more "
        "general-purpose tools in the ecosystem* increases the "
        "ceiling of plausible harm scenarios."
    ),
    prior=0.88,
)

# A.2 -- MCP monitoring as a tractable proxy is justified by the evidence
# gap (no other source covers this) plus MCP's protocol dominance.
strat_mcp_proxy_justification = support(
    [
        claim_evidence_gap,
        claim_existing_evidence_gap_breakdown,
    ],
    claim_tools_proxy_for_action_space,
    reason=(
        "Two lines of argument together justify MCP-server monitoring as "
        "a tractable proxy for the agent action space: (a) the broad "
        "literature gap on agent-tool usage (@claim_evidence_gap) and "
        "(b) the specific finding that no prior usage study quantifies "
        "the perception/reasoning/action and constrained/unconstrained "
        "decomposition of agent tool calls "
        "(@claim_existing_evidence_gap_breakdown). MCP being the "
        "predominant open agent-tool protocol makes its public servers "
        "the most representative single channel currently available."
    ),
    prior=0.85,
)

# ===========================================================================
# Block B: Methodology -> per-month observation supports
# ===========================================================================

# B.1 -- Direct-impact classifier is reliable enough to support per-month
# observations. The classifier rests on the taxonomy + Sonnet 4.5 + human
# validation.
strat_directimpact_classifier_reliable = support(
    [
        claim_directimpact_taxonomy,
        claim_directimpact_classification,
        claim_directimpact_validation,
    ],
    claim_directimpact_overall_shares,
    reason=(
        "The panel-wide direct-impact share statistics (action 64.8% of "
        "downloads / 36.0% of tools, perception 31.7%/50.6%, reasoning "
        "3.3%/13.4%) are derived by applying the CAISI-derived 11-way "
        "direct-impact taxonomy (@claim_directimpact_taxonomy) and the "
        "Sonnet 4.5 tool-level classifier "
        "(@claim_directimpact_classification) to the 177k-tool dataset, "
        "with classifier reliability anchored by 14-rater human "
        "validation reaching 81% agreement and Fleiss kappa = 0.7 "
        "(@claim_directimpact_validation). Substantial-range kappa "
        "supports treating the classifier output as reliable for "
        "*aggregate-level* claims, though individual tool labels may "
        "still err."
    ),
    prior=0.9,
)

# B.2 -- The Nov 2024 starting share and Feb 2026 ending share are derived
# from the same classifier applied to monthly download data.
strat_nov2024_observation = support(
    [
        claim_directimpact_classification,
        claim_directimpact_validation,
        claim_downloads_as_usage_proxy,
    ],
    claim_observation_action_share_nov2024,
    reason=(
        "The 27% action-tool download share for Nov 2024 is the "
        "monthly aggregate of the validated direct-impact classifier "
        "(@claim_directimpact_classification, "
        "@claim_directimpact_validation) restricted to the first month "
        "of the panel, with downloads as the usage proxy "
        "(@claim_downloads_as_usage_proxy). November 2024 is the first "
        "month with substantive MCP downloads (MCP launched in 11/2024)."
    ),
    prior=0.92,
)

strat_feb2026_observation = support(
    [
        claim_directimpact_classification,
        claim_directimpact_validation,
        claim_downloads_as_usage_proxy,
    ],
    claim_observation_action_share_feb2026,
    reason=(
        "The 65% action-tool download share for Feb 2026 is the same "
        "validated direct-impact classifier "
        "(@claim_directimpact_classification, "
        "@claim_directimpact_validation) applied to the final month of "
        "the panel, with the same download proxy "
        "(@claim_downloads_as_usage_proxy)."
    ),
    prior=0.92,
)

strat_intermediate_observation = support(
    [
        claim_directimpact_classification,
        claim_directimpact_validation,
        claim_downloads_as_usage_proxy,
        claim_wls_regression,
    ],
    claim_observation_action_share_intermediate,
    reason=(
        "Each intermediate-month action-tool share is produced by the "
        "same classifier and download data "
        "(@claim_directimpact_classification, "
        "@claim_directimpact_validation, "
        "@claim_downloads_as_usage_proxy), and the smooth monotonic "
        "rise traced through them is summarised by the asymptotic-"
        "convergence WLS fit (@claim_wls_regression)."
    ),
    prior=0.9,
)

# B.3 -- AI co-authorship classifier is reliable enough to support
# per-month observations, modulo the lower-bound caveat.
strat_aiauth_classifier_reliable = support(
    [
        claim_aiauth_criteria,
        claim_aiauth_firstmonth_variant,
        claim_aiauth_lower_bound,
    ],
    claim_aiauth_overall_shares,
    reason=(
        "The panel-wide AI-coauthorship shares (28.3% of servers / "
        "36.3% of tools) follow from applying the four-signal detector "
        "(@claim_aiauth_criteria) in its first-month restricted variant "
        "(@claim_aiauth_firstmonth_variant) to the 19,388 verified "
        "servers. Pangram cross-validation shows the detector captures "
        "only ~28.2% of repositories with strongly AI-generated "
        "READMEs (@claim_aiauth_lower_bound), so the reported shares "
        "should be interpreted as a lower bound but their *direction* "
        "and *relative growth* remain interpretable."
    ),
    prior=0.85,
)

strat_aiauth_jan2025_observation = support(
    [claim_aiauth_criteria, claim_aiauth_firstmonth_variant],
    claim_observation_aiauth_jan2025,
    reason=(
        "The 6% AI-coauthored share for January 2025 is the first-month "
        "restricted four-signal detector (@claim_aiauth_criteria, "
        "@claim_aiauth_firstmonth_variant) applied to MCP servers "
        "created in 01/2025."
    ),
    prior=0.9,
)

strat_aiauth_feb2026_observation = support(
    [claim_aiauth_criteria, claim_aiauth_firstmonth_variant],
    claim_observation_aiauth_feb2026,
    reason=(
        "The 62% AI-coauthored share for February 2026 is the same "
        "first-month four-signal detector (@claim_aiauth_criteria, "
        "@claim_aiauth_firstmonth_variant) applied to MCP servers "
        "created in 02/2026."
    ),
    prior=0.9,
)

strat_aiauth_intermediate_observation = support(
    [
        claim_aiauth_criteria,
        claim_aiauth_firstmonth_variant,
        claim_wls_regression,
    ],
    claim_observation_aiauth_intermediate,
    reason=(
        "Each intermediate-month AI-coauthored share is produced by "
        "the same first-month detector (@claim_aiauth_criteria, "
        "@claim_aiauth_firstmonth_variant); the WLS quadratic fit "
        "(@claim_wls_regression) reports R^2 = 0.97 and average "
        "marginal change +4.10pp/month, giving a tight summary of the "
        "intermediate observations."
    ),
    prior=0.9,
)

# ===========================================================================
# Block C: Inductions over per-month observations -> headline time trends
# ===========================================================================

# C.1 -- Action-tool share rose 27% -> 65%: induct over Nov 2024, the
# intermediate-month curve, and Feb 2026.

# Each induction sub-strategy must be in the generative direction:
# support([law], prediction).
ind_action_growth_s_nov2024 = support(
    [claim_finding_action_growth],
    claim_observation_action_share_nov2024,
    reason=(
        "If the action-tool share rose monotonically from 27% to 65% "
        "over the 16-month panel (@claim_finding_action_growth), then "
        "the Nov 2024 starting observation should be ~27% "
        "(@claim_observation_action_share_nov2024)."
    ),
    prior=0.95,
)

ind_action_growth_s_intermediate = support(
    [claim_finding_action_growth],
    claim_observation_action_share_intermediate,
    reason=(
        "If the action-tool share rose monotonically from 27% to 65% "
        "(@claim_finding_action_growth), the intermediate-month "
        "values should trace a near-monotonic ascending curve "
        "(@claim_observation_action_share_intermediate)."
    ),
    prior=0.9,
)

ind_action_growth_s_feb2026 = support(
    [claim_finding_action_growth],
    claim_observation_action_share_feb2026,
    reason=(
        "If the action-tool share rose monotonically from 27% to 65% "
        "(@claim_finding_action_growth), the Feb 2026 ending "
        "observation should be ~65% "
        "(@claim_observation_action_share_feb2026)."
    ),
    prior=0.95,
)

ind_action_growth_12 = induction(
    ind_action_growth_s_nov2024,
    ind_action_growth_s_intermediate,
    law=claim_finding_action_growth,
    reason=(
        "The Nov-2024 and intermediate-month observations are "
        "approximately independent (different months, different "
        "monthly download cohorts) and jointly constrain the headline "
        "27%->65% trend."
    ),
)

ind_action_growth_full = induction(
    ind_action_growth_12,
    ind_action_growth_s_feb2026,
    law=claim_finding_action_growth,
    reason=(
        "Adding the Feb-2026 endpoint observation (independent of the "
        "earlier months) closes the induction over the panel."
    ),
)

# C.2 -- AI-coauthored share rose 6% -> 62%: same induction shape.
ind_aiauth_growth_s_jan2025 = support(
    [claim_finding_aiauth_growth],
    claim_observation_aiauth_jan2025,
    reason=(
        "If the AI-coauthored share of new servers rose monotonically "
        "from 6% to 62% over 13 months (@claim_finding_aiauth_growth), "
        "the Jan 2025 starting observation should be ~6% "
        "(@claim_observation_aiauth_jan2025)."
    ),
    prior=0.95,
)

ind_aiauth_growth_s_intermediate = support(
    [claim_finding_aiauth_growth],
    claim_observation_aiauth_intermediate,
    reason=(
        "If the AI-coauthored share rose monotonically from 6% to 62% "
        "(@claim_finding_aiauth_growth), the intermediate monthly "
        "shares should trace +4.10pp/month with R^2=0.97 "
        "(@claim_observation_aiauth_intermediate)."
    ),
    prior=0.9,
)

ind_aiauth_growth_s_feb2026 = support(
    [claim_finding_aiauth_growth],
    claim_observation_aiauth_feb2026,
    reason=(
        "If the AI-coauthored share rose monotonically from 6% to 62% "
        "(@claim_finding_aiauth_growth), the Feb 2026 ending "
        "observation should be ~62% "
        "(@claim_observation_aiauth_feb2026)."
    ),
    prior=0.95,
)

ind_aiauth_growth_12 = induction(
    ind_aiauth_growth_s_jan2025,
    ind_aiauth_growth_s_intermediate,
    law=claim_finding_aiauth_growth,
    reason=(
        "Jan-2025 and intermediate-month observations are independent "
        "across cohorts and jointly constrain the 6%->62% trend."
    ),
)

ind_aiauth_growth_full = induction(
    ind_aiauth_growth_12,
    ind_aiauth_growth_s_feb2026,
    law=claim_finding_aiauth_growth,
    reason=(
        "Adding the Feb-2026 endpoint completes the induction over the "
        "13-month AI-authorship panel."
    ),
)

# ===========================================================================
# Block D: Other Section-5 supports
# ===========================================================================

# D.1 -- IT dominance derived from O*NET classifier + downloads.
strat_it_dominates = support(
    [
        claim_topdown_pipeline,
        claim_topdown_validation,
        claim_bottomup_pipeline,
        claim_bottomup_validation,
        claim_table6_taskdomains,
    ],
    claim_finding_it_dominates,
    reason=(
        "The IT-dominates finding (67% of tools / 90% of downloads) is "
        "the L1-task-domain aggregate from the top-down O*NET "
        "classifier (@claim_topdown_pipeline) validated against human "
        "raters at 78%/Fleiss kappa = 0.32 "
        "(@claim_topdown_validation), cross-checked by the BERTopic "
        "bottom-up pipeline (@claim_bottomup_pipeline, "
        "@claim_bottomup_validation) showing congruent IT cluster "
        "structure, and reported in Table 6 "
        "(@claim_table6_taskdomains)."
    ),
    prior=0.92,
)

strat_finance_share = support(
    [claim_topdown_pipeline, claim_topdown_validation, claim_table6_taskdomains],
    claim_finding_finance_share,
    reason=(
        "The 18%-of-tools / 5%-of-downloads finance share is derived "
        "from the validated top-down O*NET classifier "
        "(@claim_topdown_pipeline, @claim_topdown_validation), "
        "tabulated in Table 6 (@claim_table6_taskdomains)."
    ),
    prior=0.92,
)

# D.2 -- Consequentiality finding (medium-stakes cluster) from Figure 2.
strat_action_medium_stakes = support(
    [
        claim_consequentiality_score,
        claim_directimpact_classification,
        claim_figure2_consequentiality,
    ],
    claim_finding_action_medium_stakes,
    reason=(
        "Figure 2 (@claim_figure2_consequentiality) plots the count of "
        "action tools per O*NET occupation against the consequentiality "
        "score (@claim_consequentiality_score) using the validated "
        "direct-impact classification (@claim_directimpact_classification). "
        "The empirical distribution shows the bulk of action tools fall "
        "in the medium-stakes (50-75) band."
    ),
    prior=0.9,
)

strat_finance_highstakes_outlier = support(
    [claim_figure2_consequentiality, claim_topdown_pipeline],
    claim_finding_finance_highstakes_outlier,
    reason=(
        "The high-stakes financial outlier in Figure 2 "
        "(@claim_figure2_consequentiality) is identified by combining "
        "the consequentiality scoring with the SOC mapping from the "
        "top-down pipeline (@claim_topdown_pipeline); financial "
        "occupations have disproportionately many action tools relative "
        "to the cross-occupation pattern."
    ),
    prior=0.9,
)

# D.3 -- Action-tool US concentration from PyPI geo data.
strat_action_us_concentration = support(
    [
        claim_geography_methodology,
        claim_geography_subsample,
        claim_figure3_geography,
        claim_directimpact_classification,
    ],
    claim_finding_action_us_concentration,
    reason=(
        "The ~50% US share of action-tool downloads is derived from "
        "PyPI IP-based geolocation (@claim_geography_methodology) on "
        "the 528-server / 11.91M-download geo sub-sample "
        "(@claim_geography_subsample), restricted to action-classified "
        "servers (@claim_directimpact_classification) and reported in "
        "Figure 3 (@claim_figure3_geography). The PyPI Western "
        "skew limits external validity but the relative ordering is "
        "robust."
    ),
    prior=0.85,
)

# D.4 -- General-purpose growth from generality classifier.
strat_general_purpose_growth = support(
    [
        claim_generality_taxonomy,
        claim_generality_classification,
        claim_generality_validation,
        claim_generality_overall_shares,
        claim_wls_regression,
    ],
    claim_finding_general_purpose_growth,
    reason=(
        "The 41%->50% rise in general-purpose download share is the "
        "month-by-month aggregate from the Sonnet-4.5 generality "
        "classifier (@claim_generality_taxonomy, "
        "@claim_generality_classification) with 72%/Fleiss kappa = 0.3 "
        "human validation (@claim_generality_validation), summarised "
        "by the polynomial-convergence WLS fit "
        "(@claim_wls_regression). The fair-range kappa is the largest "
        "uncertainty but the trend is detectable."
    ),
    prior=0.8,
)

strat_general_purpose_count_stable = support(
    [
        claim_generality_classification,
        claim_generality_validation,
        claim_wls_regression,
    ],
    claim_finding_general_purpose_count_stable,
    reason=(
        "The count-basis stability at 21% is the same generality "
        "classifier (@claim_generality_classification, "
        "@claim_generality_validation) with the polynomial-convergence "
        "WLS fit (@claim_wls_regression), measured on cumulative "
        "server count rather than downloads."
    ),
    prior=0.85,
)

strat_general_purpose_action_correlation = support(
    [
        claim_generality_classification,
        claim_directimpact_classification,
        claim_generality_validation,
        claim_directimpact_validation,
    ],
    claim_finding_general_purpose_action_correlation,
    reason=(
        "The cross-tab '94% of general-purpose downloads are action / "
        "95% of perception is narrow' is computed by joining the "
        "generality classifier (@claim_generality_classification, "
        "@claim_generality_validation) with the direct-impact "
        "classifier (@claim_directimpact_classification, "
        "@claim_directimpact_validation) and weighting by downloads."
    ),
    prior=0.88,
)

# D.5 -- Action-tool growth driver claim (general-purpose computer use).
strat_action_growth_driver = support(
    [
        claim_finding_action_growth,
        claim_finding_general_purpose_action_correlation,
        claim_directimpact_taxonomy,
    ],
    claim_finding_action_growth_driver,
    reason=(
        "The mechanism claim that general-purpose computer-use tools "
        "drive the action-share growth follows from combining "
        "(a) the headline action-share rise "
        "(@claim_finding_action_growth), (b) the cross-tab observation "
        "that 94% of general-purpose downloads are action "
        "(@claim_finding_general_purpose_action_correlation), and "
        "(c) the CAISI taxonomy that places computer-use tools as a "
        "specific functionality sub-class within action "
        "(@claim_directimpact_taxonomy)."
    ),
    prior=0.85,
)

# D.6 -- Official-server stronger trend (21% -> 71%).
strat_action_growth_official = support(
    [
        claim_finding_action_growth,
        claim_official_subset_definition,
        claim_directimpact_classification,
    ],
    claim_finding_action_growth_official,
    reason=(
        "Restricting the same action-share computation to the "
        "8,469-tool official-commercial subset "
        "(@claim_official_subset_definition) using the same direct-"
        "impact classifier (@claim_directimpact_classification) yields "
        "an even sharper 21%->71% rise, consistent with and "
        "amplifying the headline 27%->65% finding "
        "(@claim_finding_action_growth)."
    ),
    prior=0.88,
)

# ===========================================================================
# Block E: Section-6 financial case study
# ===========================================================================

# E.1 -- The financial case study identifies the crypto-payment trend by
# combining the payments-autonomy scale, the figure-7 growth, and the
# finance-high-stakes outlier finding.
strat_crypto_payment_trend = support(
    [
        claim_figure7_payments_growth,
        claim_finding_finance_highstakes_outlier,
        claim_finding_action_growth,
    ],
    claim_finding_crypto_payment_trend,
    reason=(
        "The detected rising crypto-payment infrastructure trend is "
        "supported by (a) the 33x growth in payment MCP servers "
        "(@claim_figure7_payments_growth), (b) the documented "
        "high-stakes outlier of finance among action tools "
        "(@claim_finding_finance_highstakes_outlier), and (c) the "
        "background trend of overall action-tool growth "
        "(@claim_finding_action_growth). The combination identifies "
        "agentic crypto specifically as a high-velocity high-stakes "
        "subdomain."
    ),
    prior=0.87,
)

# E.2 -- The five discussion claims are each supported by their respective
# headline findings.
strat_disc_attack_surface = support(
    [
        claim_finding_action_growth,
        claim_finding_general_purpose_growth,
        claim_action_space_amplifies_misuse,
    ],
    claim_disc_attack_surface,
    reason=(
        "The misuse-attack-surface implication follows from combining "
        "the empirical growth in action and general-purpose tools "
        "(@claim_finding_action_growth, "
        "@claim_finding_general_purpose_growth) with the Section 2 "
        "channel claim that misuse risk scales with action-space "
        "exposure (@claim_action_space_amplifies_misuse)."
    ),
    prior=0.85,
)

strat_disc_misalignment = support(
    [
        claim_finding_action_growth,
        claim_action_space_amplifies_misalignment,
    ],
    claim_disc_misalignment_consequences,
    reason=(
        "The misalignment-consequences implication combines the "
        "empirical action-share growth (@claim_finding_action_growth) "
        "with the Section 2 claim that misalignment translates into "
        "harm only when action tools are present "
        "(@claim_action_space_amplifies_misalignment)."
    ),
    prior=0.85,
)

strat_disc_software_finance = support(
    [
        claim_finding_it_dominates,
        claim_finding_finance_share,
        claim_finding_finance_highstakes_outlier,
    ],
    claim_disc_software_finance_concentration,
    reason=(
        "The structural-change claim for software & finance is "
        "supported by the empirical IT dominance (67% / 90% from "
        "@claim_finding_it_dominates), the finance share "
        "(@claim_finding_finance_share), and the finance high-stakes "
        "outlier (@claim_finding_finance_highstakes_outlier)."
    ),
    prior=0.85,
)

strat_disc_governance = support(
    [
        claim_finding_general_purpose_growth,
        claim_finding_general_purpose_action_correlation,
        claim_table1_examples,
    ],
    claim_disc_governance_complication,
    reason=(
        "The governance-complication implication follows from the "
        "general-purpose growth (@claim_finding_general_purpose_growth) "
        "and the cross-tab finding that general-purpose tools are "
        "overwhelmingly action tools "
        "(@claim_finding_general_purpose_action_correlation), with "
        "Table 1 examples (@claim_table1_examples) illustrating that "
        "general-purpose action tools have ambiguous risk profiles."
    ),
    prior=0.85,
)

strat_disc_unconstrained = support(
    [
        claim_finding_general_purpose_action_correlation,
        claim_action_space_amplifies_structural,
    ],
    claim_disc_unconstrained_structural,
    reason=(
        "The unconstrained-environment structural-risk implication "
        "combines the cross-tab fact that consequential action is "
        "happening in unconstrained environments "
        "(@claim_finding_general_purpose_action_correlation) with the "
        "Section 2 channel claim about structural risks scaling with "
        "general-purpose action-tool deployment "
        "(@claim_action_space_amplifies_structural)."
    ),
    prior=0.85,
)

# E.3 -- Governance thesis aggregates the discussion claims + the
# regulator-validation evidence + the early-indicator claim.
strat_governance_thesis = support(
    [
        claim_finding_crypto_payment_trend,
        claim_regulator_use_case_validation,
        claim_mcp_early_indicator,
        claim_table7_methods_comparison,
    ],
    claim_governance_thesis,
    reason=(
        "The Section-6 governance thesis is supported by (a) the "
        "demonstrated detection of the agentic crypto trend "
        "(@claim_finding_crypto_payment_trend), (b) the operational "
        "validation by the Bank of England partnership "
        "(@claim_regulator_use_case_validation), (c) the documented "
        "lead time of MCP publication over mainstream-platform "
        "integration (@claim_mcp_early_indicator), and (d) the "
        "comparative-methods analysis showing MCP monitoring is the "
        "cheapest early-scanning option (@claim_table7_methods_comparison)."
    ),
    prior=0.83,
)

# ===========================================================================
# Block F: Conclusion synthesis
# ===========================================================================

strat_conclusion_synthesis = support(
    [
        claim_finding_action_growth,
        claim_finding_action_growth_official,
        claim_finding_general_purpose_growth,
        claim_finding_general_purpose_action_correlation,
        claim_finding_action_us_concentration,
        claim_finding_aiauth_growth,
    ],
    claim_conclusion_action_space_expanded,
    reason=(
        "The Section 7.1 headline conclusion 'the agent action space "
        "expanded along all five attributes' is the conjunction of the "
        "five attribute-level empirical findings: action growth "
        "(@claim_finding_action_growth, "
        "@claim_finding_action_growth_official), general-purpose "
        "growth (@claim_finding_general_purpose_growth, "
        "@claim_finding_general_purpose_action_correlation), "
        "geographic concentration (@claim_finding_action_us_concentration), "
        "and AI-coauthorship growth (@claim_finding_aiauth_growth)."
    ),
    prior=0.9,
)

# ===========================================================================
# Block G: Operators (contradictions and complement)
# ===========================================================================

# G.1 -- The empirical action-tool share growth contradicts the prior
# baseline policy assumption that action tools are rare.
not_both_actions_rare_and_growing = contradiction(
    claim_prior_assumption_action_rare,
    claim_finding_action_growth,
    reason=(
        "The baseline assumption "
        "(@claim_prior_assumption_action_rare) holds that action tools "
        "constitute a small minority of deployed agent tooling. The "
        "empirical headline finding (@claim_finding_action_growth) "
        "shows action tools rose to 65% of downloads by Feb 2026 -- a "
        "clear majority. Both cannot be true simultaneously."
    ),
    prior=0.97,
)

# G.2 -- The empirical action-stakes distribution and the policy-relevant
# baseline assumption sit in tension only through finance: most action
# tools cluster medium-stakes, but high-stakes finance is the documented
# exception. We model this as a contradiction between two finer-grained
# alternatives that both cannot simultaneously be true.
claim_counter_uniform_stakes = claim(
    "**Counter-hypothesis: stakes distribution of action tools is "
    "approximately uniform across O*NET occupations.** A policy "
    "framing that ignores the finance outlier would predict that "
    "action tools spread roughly evenly across the consequentiality "
    "spectrum, with no single high-stakes domain dominating.",
    title="Counter-hypothesis: action-tool stakes are approximately uniform",
)

not_both_uniform_stakes_and_finance_outlier = contradiction(
    claim_counter_uniform_stakes,
    claim_finding_finance_highstakes_outlier,
    reason=(
        "If action-tool consequentiality were approximately uniform "
        "across occupations (@claim_counter_uniform_stakes), finance "
        "could not also be a *disproportionate* high-stakes outlier "
        "(@claim_finding_finance_highstakes_outlier); the two "
        "propositions are mutually inconsistent."
    ),
    prior=0.95,
)

# ===========================================================================
# Block H: Abduction -- explanation of the action-share growth
# ===========================================================================

# The paper argues the action-tool growth is explained by adoption of
# general-purpose computer-use tooling, not by random fluctuation.

claim_obs_action_share_change = claim(
    "**Observation to be explained.** Between 11/2024 and 02/2026, the "
    "monthly download-weighted action-tool share rose from ~27% to "
    "~65%, a ~40-percentage-point shift. The intermediate-month "
    "trajectory traces a smooth, near-monotonic asymptotic-convergence "
    "curve.",
    title="Observation: action-tool share rose ~40pp over 16 months",
)

claim_pred_h_general_purpose_drives = claim(
    "**Hypothesis prediction.** If the action-share rise is driven by "
    "**adoption of general-purpose computer-use tooling** (browser "
    "automation, computer use, AppleScript-desktop integration), then "
    "we should observe (i) general-purpose tools' download share rising "
    "in lockstep, (ii) >90% of general-purpose downloads being action, "
    "(iii) commercial-server action share rising at least as fast, and "
    "(iv) the rise being concentrated in 'computer use' / 'code "
    "execution' / 'software extension' functionality sub-classes. The "
    "paper documents all four predictions hold.",
    title="Hypothesis prediction: general-purpose tooling explains the rise",
)

alt_random_fluctuation = claim(
    "**Alternative explanation: monthly fluctuation / sampling noise.** "
    "Under this alternative, the apparent 27%->65% rise is the product "
    "of monthly noise in the small early-MCP cohort (Nov 2024 had few "
    "servers and large download concentration in a few servers, per "
    "@claim_downloads_concentration). The trajectory could appear "
    "monotonic by chance even without an underlying directional shift.",
    title="Alternative: action-share growth is monthly sampling noise",
)

claim_pred_alt_random = claim(
    "**Alternative prediction.** If the rise were sampling noise rather "
    "than a real directional shift, we would expect (i) the rise to be "
    "non-monotonic with reversals, (ii) WLS fits to have low R^2 and "
    "wide confidence intervals overlapping the no-trend null, and (iii) "
    "the trend to disappear when restricted to the high-traffic "
    "official-commercial subset (where downloads-per-month are large "
    "enough to overwhelm noise). None of these predictions hold."
    ,
    title="Alternative prediction: noise model predicts non-monotonic, low-R^2 trend",
)

# Build the abduction's component strategies.
abd_action_growth_s_h = support(
    [claim_pred_h_general_purpose_drives],
    claim_obs_action_share_change,
    reason=(
        "If the action-share rise is driven by general-purpose tool "
        "adoption (@claim_pred_h_general_purpose_drives), the smooth "
        "27%->65% trajectory is exactly the predicted observable."
    ),
    prior=0.9,
)

abd_action_growth_s_alt = support(
    [alt_random_fluctuation],
    claim_obs_action_share_change,
    reason=(
        "Under the noise alternative (@alt_random_fluctuation), the "
        "27%->65% trajectory could in principle arise from sampling "
        "fluctuation, but only if the empirical predictions of the "
        "noise model held."
    ),
    prior=0.25,
)

abd_action_growth_compare = compare(
    claim_pred_h_general_purpose_drives,
    claim_pred_alt_random,
    claim_obs_action_share_change,
    reason=(
        "The general-purpose-tool hypothesis predicts a smooth "
        "monotonic rise, lockstep general-purpose growth, ~94% "
        "general-purpose-action correlation, and a sharper commercial-"
        "subset trend -- all of which are observed. The noise "
        "alternative predicts non-monotonic trajectories, low R^2, and "
        "the trend disappearing on the high-traffic commercial subset "
        "-- none of which are observed."
    ),
    prior=0.92,
)

abd_action_growth = abduction(
    abd_action_growth_s_h,
    abd_action_growth_s_alt,
    abd_action_growth_compare,
    reason=(
        "Both the general-purpose-tooling hypothesis and the noise "
        "alternative attempt to explain the same observed action-share "
        "trajectory; the hypothesis matches all auxiliary predictions "
        "while the alternative matches none."
    ),
)

# ===========================================================================
# Block I: Wire motivation-preview claims to s5 detailed findings
# ===========================================================================
#
# The motivation introduces five 'preview' claims summarising headlines.
# The detailed findings in s5 are independent expressions of the same
# empirical content. Connect each preview to its detailed counterpart so
# (a) the preview claim becomes a derived conclusion supported by the
# rigorous s5 derivation and (b) the preview is no longer an orphan.

strat_preview_software_dominates = support(
    [claim_finding_it_dominates],
    claim_finding_software_dominates,
    reason=(
        "The motivation-section preview "
        "(@claim_finding_software_dominates) of the IT-dominates "
        "headline is supported by the rigorous Section-5 finding "
        "(@claim_finding_it_dominates) which derives the 67% / 90% "
        "shares from the validated O*NET classifier."
    ),
    prior=0.97,
)

strat_preview_us_concentration = support(
    [claim_finding_action_us_concentration],
    claim_finding_us_concentration,
    reason=(
        "The motivation preview of US concentration "
        "(@claim_finding_us_concentration) is supported by the "
        "Section-5.2 detailed finding "
        "(@claim_finding_action_us_concentration) derived from PyPI "
        "geo data."
    ),
    prior=0.97,
)

strat_preview_action_growth = support(
    [claim_finding_action_growth, claim_finding_action_growth_official],
    claim_finding_action_share_growth,
    reason=(
        "The motivation preview of the action-share growth "
        "(@claim_finding_action_share_growth) is supported by both the "
        "Section-5.3 headline 27%->65% finding "
        "(@claim_finding_action_growth) and the official-server "
        "21%->71% sub-finding (@claim_finding_action_growth_official)."
    ),
    prior=0.97,
)

strat_preview_action_stakes = support(
    [
        claim_finding_action_medium_stakes,
        claim_finding_finance_highstakes_outlier,
    ],
    claim_finding_action_stakes_distribution,
    reason=(
        "The motivation preview of the action-tool stakes distribution "
        "(@claim_finding_action_stakes_distribution) is supported by "
        "the Section-5.1 medium-stakes clustering finding "
        "(@claim_finding_action_medium_stakes) and the finance "
        "high-stakes outlier (@claim_finding_finance_highstakes_outlier)."
    ),
    prior=0.95,
)

strat_preview_aiauth_growth = support(
    [claim_finding_aiauth_growth],
    claim_finding_ai_coauthorship_growth,
    reason=(
        "The motivation preview of the AI-coauthorship growth "
        "(@claim_finding_ai_coauthorship_growth) is supported by the "
        "Section-5.5 detailed 6%->62% finding "
        "(@claim_finding_aiauth_growth)."
    ),
    prior=0.97,
)

# ===========================================================================
# Block J: Wire motivation contribution claims to the relevant evidence
# ===========================================================================

# J.1 -- The dataset contribution rests on the data sources, validation
# pipeline, and the dataset-scale facts.
strat_contribution_dataset = support(
    [
        claim_data_sources,
        claim_validation_pipeline,
        claim_dataset_scale,
    ],
    claim_contribution_dataset,
    reason=(
        "Contribution 1 (the 177k-tool dataset, "
        "@claim_contribution_dataset) is established by the three-source "
        "harvest (@claim_data_sources), the LLM-validated filtering "
        "pipeline (@claim_validation_pipeline), and the resulting "
        "dataset-scale tabulation (@claim_dataset_scale)."
    ),
    prior=0.95,
)

# J.2 -- The time-trend contribution rests on the panel observations.
strat_contribution_timetrend = support(
    [
        claim_finding_action_growth,
        claim_finding_general_purpose_growth,
        claim_finding_aiauth_growth,
    ],
    claim_contribution_timetrend,
    reason=(
        "Contribution 2 (longitudinal evolution, "
        "@claim_contribution_timetrend) is established by the three "
        "main panel-trend findings: action-share rise "
        "(@claim_finding_action_growth), general-purpose-share rise "
        "(@claim_finding_general_purpose_growth), and AI-coauthorship "
        "rise (@claim_finding_aiauth_growth)."
    ),
    prior=0.95,
)

# J.3 -- The governance contribution is an alias for the Section-6
# governance thesis.
strat_contribution_governance = support(
    [
        claim_governance_thesis,
        claim_finding_crypto_payment_trend,
        claim_regulator_use_case_validation,
    ],
    claim_contribution_governance,
    reason=(
        "Contribution 3 (tool-layer monitoring as a regulatory "
        "instrument, @claim_contribution_governance) is the same "
        "argument as the Section-6 governance thesis "
        "(@claim_governance_thesis), evidenced by the financial "
        "case-study detection (@claim_finding_crypto_payment_trend) "
        "and the Bank-of-England partnership "
        "(@claim_regulator_use_case_validation)."
    ),
    prior=0.92,
)

# ===========================================================================
# Block K: Connect remaining orphans
# ===========================================================================

# K.1 -- Table 2 examples are illustrative supporting material for the
# Section-2 thesis on action-space amplification.
strat_table2_supports_amplification = support(
    [claim_table2_examples],
    claim_large_action_space_amplifies_risk,
    reason=(
        "Table 2 (@claim_table2_examples) provides concrete examples "
        "of action tools spanning low/medium/high stakes and "
        "country/continent/worldwide geography, illustrating the "
        "Section-2 thesis that wider action-space tools amplify risk."
    ),
    prior=0.85,
)

# K.2 -- Comparison-with-chatbot-studies claim is a derived comparison
# from the IT-dominance finding and Table-3 evidence-gap context.
strat_comparison_chatbot_studies = support(
    [
        claim_finding_it_dominates,
        claim_existing_evidence_gap_breakdown,
    ],
    claim_comparison_with_chatbot_studies,
    reason=(
        "The cross-study comparison "
        "(@claim_comparison_with_chatbot_studies) follows from the IT "
        "dominance in MCP downloads (@claim_finding_it_dominates) and "
        "the prior-studies summary "
        "(@claim_existing_evidence_gap_breakdown), which together show "
        "the MCP-tool view is more IT-skewed than chatbot conversation "
        "data."
    ),
    prior=0.9,
)

# K.3 -- Conclusion 7.2 limitation rests on the data-sources scope.
strat_limitation_lower_bound = support(
    [
        claim_data_sources,
        claim_downloads_as_usage_proxy,
    ],
    claim_limitation_lower_bound,
    reason=(
        "The Section 7.2 limitation that 177k is a lower bound "
        "(@claim_limitation_lower_bound) follows from the "
        "GitHub+Smithery+lists data-source scope "
        "(@claim_data_sources) -- which excludes private/proprietary "
        "tooling -- and the developer-biased download proxy "
        "(@claim_downloads_as_usage_proxy)."
    ),
    prior=0.95,
)

# K.4 -- Download concentration affects the noise-alternative analysis;
# wire it into the abduction's alternative as supporting context.
strat_downloads_concentration_supports_noise_alt = support(
    [claim_downloads_concentration],
    alt_random_fluctuation,
    reason=(
        "The high download concentration (top 1% of servers carry "
        "43-79% of downloads, @claim_downloads_concentration) is the "
        "factual basis on which the noise-alternative builds: with so "
        "much weight on a few servers, monthly fluctuation in their "
        "classification could in principle distort aggregate shares."
    ),
    prior=0.7,
)

__all__ = [
    "claim_obs_action_share_change",
    "claim_pred_h_general_purpose_drives",
    "alt_random_fluctuation",
    "claim_pred_alt_random",
    "claim_counter_uniform_stakes",
]
