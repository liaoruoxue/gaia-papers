"""Prior assignments for independent (leaf) claims in this package."""

from . import (
    # CritPt baselines and evolver results
    obs_critpt_baseline_feb,
    obs_critpt_baseline_mar,
    obs_evolver_feb,
    obs_evolver_mar,
    # Evolution phase observation
    obs_memory_grounded_phase,
    # Experimental observations — high prior: direct measurements from controlled trials
    obs_baseline_passrate,
    obs_skill_passrate,
    obs_gene_passrate,
    obs_skill_workflow_useful,
    obs_skill_overview_harmful,
    obs_budget_matched_fragment,
    obs_keywords_only,
    obs_keywords_plus_summary,
    obs_full_gene_construction,
    obs_content_corrupt_wrong_algo,
    obs_content_corrupt_wrong_domain,
    obs_structural_inverted_priority,
    obs_structural_overconstrained,
    obs_gene_plus_api,
    obs_gene_plus_examples,
    obs_skill_plus_failure,
    obs_freeform_plus_failure,
    obs_gene_plus_raw_failure,
    obs_flattened_prose,
    obs_structured_gep,
    obs_failure_first,
    obs_strategy_first,
    obs_strategy_only_failure_exp,
    obs_failure_warnings_only,
    obs_two_complementary_genes,
    obs_three_complementary_genes,
    obs_two_conflicting_genes,
    obs_exploration_augmented_phase,
    # Hypothesis and alternative claims for abduction
    alt_attention_bias,
    pred_gene_structure_helps,
    pred_attention_bias,
)

PRIORS = {
    # --- Evolver result observations (independent empirical results) ---
    obs_evolver_feb: (
        0.90,
        "Directly reported CritPt result: 18.57% accuracy for Evolver (Gene) 2026-02-16. "
        "High confidence as an explicitly reported benchmark result from the paper.",
    ),
    obs_evolver_mar: (
        0.90,
        "Directly reported CritPt result: 27.14% accuracy for Evolver (Gene) 2026-03-26. "
        "High confidence as an explicitly reported benchmark result from the paper.",
    ),
    # --- Memory-grounded phase observation ---
    obs_memory_grounded_phase: (
        0.88,
        "Qualitative description of the Feb 2026 evolver's memory-grounded mechanism "
        "(failure → repair procedure conversion). High confidence in the mechanism description; "
        "moderate uncertainty because the details come from qualitative Appendix D examples.",
    ),
    # --- CritPt baseline observations ---
    obs_critpt_baseline_feb: (
        0.93,
        "Direct measurement: Gemini 3 Pro (non-preview) achieves 9.1% on CritPt benchmark "
        "in the Feb 2026 evaluation. High confidence as a reported benchmark result.",
    ),
    obs_critpt_baseline_mar: (
        0.93,
        "Direct measurement: Gemini 3.1 Pro (non-preview) achieves 17.7% on CritPt benchmark "
        "in the Mar 2026 evaluation. High confidence as a reported benchmark result.",
    ),
    # --- Primary pass-rate observations ---
    # These are direct outputs of 4,590 controlled trials; high confidence.
    obs_baseline_passrate: (
        0.93,
        "Direct experimental measurement from 4,590 trials; checkpoint pass rate is a "
        "deterministic function of outcomes. Slight uncertainty for potential experimental noise.",
    ),
    obs_skill_passrate: (
        0.93,
        "Direct experimental measurement (49.9% avg) from the same 4,590-trial protocol; "
        "same reliability as the baseline measurement.",
    ),
    obs_gene_passrate: (
        0.93,
        "Direct experimental measurement (54.0% avg) from the same 4,590-trial protocol.",
    ),
    # --- Skill decomposition observations ---
    obs_skill_workflow_useful: (
        0.85,
        "Figure 3(a) decomposition shows Skill-Workflow as clearly positive. Moderate uncertainty "
        "because qualitative characterization ('clearly useful') without exact numeric comparison.",
    ),
    obs_skill_overview_harmful: (
        0.88,
        "Figure 3(a) shows Skill-Overview as 'strongly harmful', and full-package degradation "
        "(-1.1pp) is consistent with this. High confidence in direction; slight uncertainty in magnitude.",
    ),
    obs_budget_matched_fragment: (
        0.85,
        "Budget-matched fragment comparison (Figure 3(b)) shows improvement but below Gene. "
        "Moderate uncertainty because exact value not reported, only relative comparison.",
    ),
    # --- Gene construction observations ---
    obs_keywords_only: (
        0.93,
        "Direct measurement: keywords-only condition achieves 53.5% (+2.5pp) in Table 2.",
    ),
    obs_keywords_plus_summary: (
        0.93,
        "Direct measurement: keywords+summary achieves 51.0% (+0.0pp) in Table 2.",
    ),
    obs_full_gene_construction: (
        0.93,
        "Direct measurement: full gene achieves 54.0% (+3.0pp) in Table 2; same as main result.",
    ),
    # --- Robustness perturbation observations ---
    obs_content_corrupt_wrong_algo: (
        0.90,
        "Direct measurement from Figure 4: wrong-algorithm condition 48.8%. High confidence; "
        "experimental condition is precisely defined.",
    ),
    obs_content_corrupt_wrong_domain: (
        0.90,
        "Direct measurement from Figure 4: wrong-domain condition 49.4%.",
    ),
    obs_structural_inverted_priority: (
        0.90,
        "Direct measurement from Figure 4: inverted priority 52.8%. High confidence.",
    ),
    obs_structural_overconstrained: (
        0.90,
        "Direct measurement from Figure 4: overconstrained 55.9%. High confidence.",
    ),
    # --- Documentation reattachment observations ---
    obs_gene_plus_api: (
        0.93,
        "Direct measurement from Table 3: Gene + API notes achieves 51.5% avg.",
    ),
    obs_gene_plus_examples: (
        0.93,
        "Direct measurement from Table 3: Gene + examples achieves 52.0% avg.",
    ),
    # --- Multi-gene composition observations ---
    obs_two_complementary_genes: (
        0.93,
        "Direct measurement from Table 4: two complementary genes achieves 44.9% avg (-6.1pp).",
    ),
    obs_three_complementary_genes: (
        0.93,
        "Direct measurement from Table 4: three complementary genes achieves 50.4% avg (-0.6pp).",
    ),
    obs_two_conflicting_genes: (
        0.93,
        "Direct measurement from Table 4: two conflicting genes achieves 53.2% avg (+2.2pp).",
    ),
    # --- Failure carrier format observations ---
    obs_skill_plus_failure: (
        0.93,
        "Direct measurement from Table 5: Skill + failure achieves 47.8% avg (-3.2pp).",
    ),
    obs_freeform_plus_failure: (
        0.93,
        "Direct measurement from Table 5: Freeform + failure achieves 49.6% avg (-1.4pp).",
    ),
    obs_gene_plus_raw_failure: (
        0.93,
        "Direct measurement from Table 5: Gene + failure achieves 52.0% avg (+1.0pp).",
    ),
    # --- Structure vs. prose observations ---
    obs_flattened_prose: (
        0.93,
        "Direct measurement from Table 6: flattened prose achieves 50.5% avg (-0.5pp).",
    ),
    obs_structured_gep: (
        0.93,
        "Direct measurement from Table 6: structured GEP achieves 54.0% avg (+3.0pp).",
    ),
    # --- Failure encoding observations ---
    obs_failure_first: (
        0.93,
        "Direct measurement from Table 7: failure-first encoding achieves 50.5% (+0.7pp).",
    ),
    obs_strategy_first: (
        0.93,
        "Direct measurement from Table 7: strategy-first achieves 51.8% (+2.0pp).",
    ),
    obs_strategy_only_failure_exp: (
        0.93,
        "Direct measurement from Table 7: strategy-only achieves 52.3% (+2.5pp).",
    ),
    obs_failure_warnings_only: (
        0.93,
        "Direct measurement from Table 7: failure warnings only achieves 54.4% (+4.6pp); "
        "this is the top-performing condition in the failure encoding experiment.",
    ),
    # --- Evolution observations ---
    obs_exploration_augmented_phase: (
        0.88,
        "Observation about the Mar 2026 evolver's gene library structure (210 slots, 36 IDs). "
        "High confidence in the reported numbers; slight uncertainty because library composition "
        "details are qualitative descriptors from Appendix D.",
    ),
    # --- Abduction hypothesis and alternative priors ---
    alt_attention_bias: (
        0.40,
        "The attention-bias alternative hypothesis (structure biases attention independently "
        "of semantic content) is a plausible mechanism but incomplete: it cannot explain why "
        "content corruption drops below baseline while structure tolerates deformation. "
        "Prior reflects partial explanatory power.",
    ),
    pred_gene_structure_helps: (
        0.70,
        "The execution-mode cuing hypothesis (structure templates LLM execution) is the "
        "more complete explanation: it accounts for both structural tolerance and content sensitivity. "
        "Moderate-high prior as the primary hypothesis.",
    ),
    pred_attention_bias: (
        0.45,
        "The prediction derived from the attention-bias hypothesis (format alone suffices) "
        "is partially contradicted by content sensitivity results. Moderate-low prior.",
    ),
}
