"""Prior assignments for independent leaf claims and observation anchors."""

from . import (
    # Motivation leaves
    claim_rich_feedback,
    claim_rlvr_underuses_feedback,
    claim_agency_internalization,
    # Method leaves
    claim_experience_as_intervention,
    claim_lreh_stabilizes,
    claim_initialization_grpo,
    # Experimental leaves & observation anchors
    obs_grpo_passk_pattern,
    obs_ood_mbpp,
    obs_stage1_sampling,
    obs_main_results,
    obs_codecontests_results,
    obs_lcf_ablation,
    obs_synergy_ablation,
    # Abduction predictions
    pred_internalization,
    pred_just_sharpening,
    alt_leafe_just_sharpening,
    # Limitations
    claim_lim_feedback_quality,
    claim_lim_resettable_env,
)

PRIORS = {
    # ── Motivation leaves ───────────────────────────────────────────────────
    claim_rich_feedback: (
        0.95,
        "Well-established characterization of contemporary interactive "
        "agentic environments (compiler errors, state observations, invalid "
        "action signals). Cited to existing literature [@Yang2024; @Shinn2023] "
        "and treated as background fact, not a contested claim of this paper.",
    ),
    claim_rlvr_underuses_feedback: (
        0.85,
        "A descriptive claim about how outcome-based RLVR uses signal: a "
        "trajectory is reduced to one scalar reward and partially-correct "
        "failures contribute little. This follows almost directly from the "
        "definition of RLVR; the only uncertainty is around 'rich feedback "
        "is not used' since RLVR pipelines do consume token-level credit via "
        "policy gradient on the action distribution.",
    ),
    claim_agency_internalization: (
        0.70,
        "A definitional / programmatic claim — the paper *defines* what it "
        "means by agency internalization. The 0.70 prior reflects that this "
        "is the paper's own conceptual framing rather than a measured fact: "
        "competing definitions (e.g. step-wise process reward, dense reward "
        "shaping) could equally well be called 'internalization'.",
    ),

    # ── Method leaves ───────────────────────────────────────────────────────
    claim_experience_as_intervention: (
        0.85,
        "A design principle of LEAFE: experience is concatenated as context, "
        "not used as a token-level training target during exploration. This "
        "is well-defined and consistent with similar in-context-learning / "
        "rollback approaches [@LiGARollback2025; @WangHOPE].",
    ),
    claim_lreh_stabilizes: (
        0.92,
        "Standard property of an imitation-learning loss on demonstrated "
        "successful trajectories — preserves baseline competence by anchoring "
        "the policy to demonstrated behavior. Textbook regularizing "
        "interpretation [@Ahn2024].",
    ),
    claim_initialization_grpo: (
        0.95,
        "Reported directly in §4 (Implementation Details): 'LEAFE is also "
        "initialized from the GRPO-trained model'. This is a procedural "
        "fact about the experimental pipeline, not a contested claim.",
    ),

    # ── Observation anchors (Tables 1, 2, 3, 4, 5, 6) ──────────────────────
    # These are the empirical anchors of the inductions/abduction. They are
    # technically derived (each is the conclusion of one or more support
    # sub-strategies inside an induction or abduction) but their belief must
    # be clamped near the directly-measured value for BP to behave correctly.
    obs_main_results: (
        0.95,
        "Directly transcribed from Table 1 of the paper (artifacts/2603.16843.pdf). "
        "Well-defined Pass@1 / Pass@128 percentages on four standardized "
        "benchmarks with two model families — direct empirical measurement, "
        "high confidence.",
    ),
    obs_codecontests_results: (
        0.93,
        "Directly transcribed from Table 2 (CodeContests with Qwen2.5-72B and "
        "Llama3-70B). Direct empirical measurement.",
    ),
    obs_grpo_passk_pattern: (
        0.92,
        "Direct cross-comparison of cells in Tables 1 and 2 — a factual "
        "summary of the numerical pattern, not a derived inference. The +14 "
        "point Pass@128 gap on CodeContests / Qwen2.5-72B and the WebShop / "
        "Qwen2.5-7B Pass@1 reversal are read off directly.",
    ),
    obs_stage1_sampling: (
        0.92,
        "Directly transcribed from Table 3 (Pass@128 under IS / IR / Stage-1 "
        "sampling on CodeContests, three backbones). Empirical measurement, "
        "high confidence.",
    ),
    obs_lcf_ablation: (
        0.92,
        "Directly transcribed from Table 4 (Pass@1 / Pass@128 with Lreh vs. "
        "Lcf+Lreh on ScienceWorld for three model sizes). Direct empirical "
        "measurement.",
    ),
    obs_ood_mbpp: (
        0.92,
        "Directly transcribed from Table 5 (MBPP Pass@128 for Base / GRPO / "
        "LEAFE on three large backbones). Empirical measurement, but with a "
        "slightly lower prior because OOD evaluation is a single test "
        "benchmark and could be sensitive to prompt template choices.",
    ),
    obs_synergy_ablation: (
        0.90,
        "Directly transcribed from Table 6 (LEAFE alone vs. LEAFE + EE / RL). "
        "Empirical measurement; prior set slightly below the main tables "
        "because the LEAFE-alone CodeContests numbers in Table 6 (e.g. "
        "9.34 / 34.35 on Qwen2.5-32B) appear to use different LEAFE-alone "
        "configurations than Table 2's headline numbers, introducing some "
        "interpretive ambiguity.",
    ),

    # ── Abduction components ───────────────────────────────────────────────
    pred_internalization: (
        0.85,
        "Prediction of the internalization hypothesis: Lcf raises Pass@128 "
        "selectively while Lreh anchors Pass@1. This prediction follows "
        "directly from the design semantics of the two losses — Lreh "
        "imitates successful trajectories (Pass@1 anchor), Lcf supplies "
        "corrective alternatives (Pass@K coverage). High prior conditional "
        "on the internalization framing.",
    ),
    pred_just_sharpening: (
        0.25,
        "Prediction under the 'LEAFE is just better sharpening' alternative: "
        "the two losses should be near-substitutes that affect Pass@1 and "
        "Pass@128 in roughly the same proportion. Low prior because a "
        "sharpening view of LEAFE has no principled reason to predict "
        "loss substitutability — the two losses operate on different data "
        "distributions (successful rollouts vs. branching events) and "
        "therefore should not behave as substitutes even under that view.",
    ),
    alt_leafe_just_sharpening: (
        0.25,
        "Alternative explanation that LEAFE is merely a different sharpening "
        "recipe. Low prior reflecting the explanatory-power semantics: "
        "sharpening alone cannot account for (a) the asymmetric Lcf-vs-Lreh "
        "Pass@128 gain, (b) preserved OOD MBPP performance, or (c) the "
        "absence of test-time rollback at inference — three observations a "
        "pure sharpening view struggles to reconcile.",
    ),

    # ── Limitations (orphaned standalone claims) ───────────────────────────
    claim_lim_feedback_quality: (
        0.85,
        "Self-acknowledged limitation in §4.5; consistent with the method's "
        "structural reliance on diagnostic feedback to identify rollback "
        "targets. High prior because the authors directly assert it and the "
        "mechanism makes it almost definitional.",
    ),
    claim_lim_resettable_env: (
        0.90,
        "Self-acknowledged limitation in §4.5; structurally true because "
        "Stage-1 branching reconstructs $E_\\tau$ by replaying the action "
        "prefix — non-deterministic environments break this contract by "
        "definition. High prior.",
    ),
}
