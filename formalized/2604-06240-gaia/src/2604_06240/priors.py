"""Prior assignments for independent leaf claims.

All 9 independent premises are grounded in direct empirical observations or widely
accepted background facts. Priors reflect evidence strength and source reliability.
"""

from . import (
    alt_fpr_reduction_is_model,
    auto_research_conservative,
    auto_research_cont_expert_result,
    controllable_vs_uncontrollable,
    cua_trajectories_hard_to_verify,
    existing_verifiers_inadequate,
    rubric_quality_critical,
    screenshot_needle_in_haystack,
    verifier_needs_all_screenshots,
    upgrading_backbone_insufficient,
)

PRIORS = {
    # Directly measured and widely accepted. CUA trajectories are visually dense,
    # long, and ambiguous by construction — this is a definitional property well
    # established in the CUA literature (WebArena, VisualWebArena, OSWorld).
    cua_trajectories_hard_to_verify: (
        0.95,
        "Definitionally true of CUA: trajectories span hundreds of screenshots over "
        "diverse web environments. Extensively documented in benchmark papers.",
    ),

    # Measured with error bars over 3 independent runs: WebVoyager FPR = 0.45±0.01,
    # WebJudge FPR = 0.22±0.02, kappa 0.31±0.01 / 0.44±0.01. Strong empirical evidence.
    existing_verifiers_inadequate: (
        0.92,
        "Directly measured in Table 2 with 3-run error bars. FPR >= 0.22 for all baselines.",
    ),

    # Reported as qualitative finding from 32 expert iterations over 3 weeks.
    # Figure 1 shows rubric upgrade causing the largest single kappa jump. Well-supported
    # by the 3 examples in Table 4, but the '~half of kappa gains' is anecdotal.
    rubric_quality_critical: (
        0.88,
        "Supported by Figure 1 trajectory showing rubric upgrade as largest single jump, "
        "and Table 4 with 3 concrete examples. The 'roughly half' fraction is anecdotal.",
    ),

    # Well-documented limitation of LLM context windows on long visual sequences.
    # Multiple benchmarks (OSWorld) confirm LLM performance degrades with trajectory length.
    screenshot_needle_in_haystack: (
        0.9,
        "Well-established limitation in the CUA literature: LLM performance degrades with "
        "trajectory length when all screenshots are packed into one context.",
    ),

    # Logical consequence of the problem definition: if critical state changes can occur
    # at any timestep, any fixed-subset strategy is an approximation. Certain.
    verifier_needs_all_screenshots: (
        0.95,
        "Logically necessary: a verifier attending only to a subset cannot detect failures "
        "that manifest only in screenshots outside that subset.",
    ),

    # The controllable/uncontrollable taxonomy is a design claim, not an empirical
    # measurement. It is reasonable and internally consistent, but its completeness
    # (exhaustiveness of the taxonomy) is hard to verify.
    controllable_vs_uncontrollable: (
        0.85,
        "The taxonomy is internally consistent and covers the main cases. Its completeness "
        "is assumed — edge cases not covered may exist.",
    ),

    # This is the alternative hypothesis in the abduction. The model-only explanation
    # is plausible a priori (GPT-5.2 is substantially stronger) but the paper's
    # experiment shows it is insufficient. Low prior because the evidence strongly
    # favors the architectural explanation.
    alt_fpr_reduction_is_model: (
        0.2,
        "Plausible a priori — GPT-5.2 is a much stronger model — but Table 2 shows "
        "backbone upgrade alone causes sharp FNR increase with only modest kappa gain, "
        "strongly arguing against this as the primary explanation.",
    ),

    # Qualitative characterization from auto-research logs. The paper authors examined
    # agent logs and identified the pattern. Credible but subjective.
    auto_research_conservative: (
        0.85,
        "Qualitative analysis by paper authors of auto-research agent commit logs. "
        "Consistent with the plateau behavior observed in Figure 1 (no step-function jumps).",
    ),

    # Directly observed: Table 17 shows 4 committed improvements out of 11 iterations.
    # The claim about improvements being found is directly observable.
    auto_research_cont_expert_result: (
        0.92,
        "Directly observed in Table 17: 4 of 11 continue-expert iterations were committed "
        "(improved kappa without increasing FPR). Runs 2, 6, 10, 11 all committed.",
    ),

    # Directly measured in Table 2 with 3-run error bars. WebVoyager GPT-5.2 outcome
    # kappa = 0.43±0.01 vs UV 0.64±0.03; WebVoyager FNR rises from 0.24 to 0.44.
    # This is an empirical observation, not a derived claim — it is independently measurable.
    upgrading_backbone_insufficient: (
        0.92,
        "Directly measured in Table 2 (Table 15 with error bars): WebVoyager GPT-5.2 "
        "achieves kappa = 0.43 vs UV's 0.64 on the internal dataset outcome labels, "
        "with FNR rising from 0.24 to 0.44. Consistent result on Browserbase.",
    ),
}
