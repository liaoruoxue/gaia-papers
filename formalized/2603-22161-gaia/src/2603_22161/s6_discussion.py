"""Discussion: Two-Stage Metacognitive Control in LLMs"""

from gaia.lang import claim, support, induction

from .motivation import two_stage_framework, gap_prior_work, llm_calibration_prior
from .s2_phase1 import gpt4o_phase1_accuracy, gpt4o_calibration_result
from .s3_phase2 import (
    confidence_best_predictor,
    confidence_effect_size_dominant,
    implicit_threshold,
    gpt4o_phase2_performance,
    phase1_confidence_stability,
)
from .s4_phase3 import (
    confidence_causal_role,
    mediation_confidence_redistribution,
    steering_effect_on_abstention,
    mediation_difficulty_robust,
)
from .s5_phase4 import (
    phase4_confidence_dominant,
    phase4_decision_parameters,
    phase1_confidence_retains_power,
    cross_model_variation,
    threshold_increases_accuracy,
    two_stage_fully_validated,
    threshold_increases_abstention,
)

# ── Core synthesized conclusions ─────────────────────────────────────────────

two_stage_account_validated = claim(
    "LLM abstention arises from the joint operation of two computational stages: "
    "Stage 1 — internal confidence representations formed independently of the abstention option, "
    "and Stage 2 — a threshold-based policy σ((T − C) / τ) that maps confidence to abstention decisions. "
    "This two-stage account is supported by: "
    "(a) confidence dominates abstention prediction with effect sizes ~10× larger than alternatives (Phase 2); "
    "(b) activation steering of confidence representations directly shifts abstention rates causally (Phase 3); "
    "(c) instructed threshold manipulation shifts Stage 2 without distorting Stage 1 confidence (Phase 4). "
    "The framework is consistent across GPT-4o, Gemma 3 27B, DeepSeek 671B, and Qwen 80B.",
    title="Two-stage confidence-decision account validated across phases and models",
    background=[two_stage_framework],
)

metacognitive_control_demonstrated = claim(
    "LLMs exhibit structured metacognitive control paralleling biological systems: they generate, "
    "weight, and strategically deploy internal confidence signals to regulate abstention behavior. "
    "This represents a capacity for metacognitive control — using internal evaluations of decision "
    "correctness to regulate behavior — distinct from merely producing calibrated verbal confidence reports. "
    "Notably, LLM verbal confidence reports are often overconfident and miscalibrated "
    "(Steyvers et al., 2025), yet internal confidence signals still adaptively guide behavior, "
    "suggesting a dissociation between metacognitive control and verbal introspection.",
    title="LLMs exhibit metacognitive control dissociated from verbal introspection",
    background=[two_stage_framework],
)

dissociation_verbal_behavioral = claim(
    "There is a dissociation between LLM verbal confidence reports and the internal confidence "
    "signals that guide behavior: verbal reports are frequently overconfident and poorly calibrated, "
    "yet internal (logit-based, temperature-scaled) confidence signals robustly predict and "
    "causally drive abstention behavior.",
    title="Dissociation: miscalibrated verbal reports but reliable internal confidence for behavior",
    background=[two_stage_framework],
)

convergent_computational_architecture = claim(
    "The two-stage confidence-decision architecture is a convergent solution across diverse LLM "
    "implementations: GPT-4o, Gemma 3 27B, DeepSeek 671B, and Qwen 80B all show robust confidence-"
    "driven abstention despite substantial quantitative variation in baseline abstention rates and "
    "decision parameters (scale, shift, temperature). "
    "This convergence suggests the computational demands of metacognitive control impose shared "
    "architectural constraints across training procedures and scales.",
    title="Two-stage metacognitive architecture converges across LLM implementations",
)

# ── Practical implications ────────────────────────────────────────────────────

abstention_improves_reliability = claim(
    "Higher instructed confidence thresholds improve the reliability of GPT-4o answers: "
    "a 10% increase in instructed threshold raises answer accuracy by ~1.1%, demonstrating "
    "a functional coverage-accuracy trade-off that can be controlled via threshold instructions. "
    "This capacity is of practical importance as LLMs transition to autonomous agents that must "
    "recognize uncertainty and know when to act, seek help, or abstain.",
    title="Controllable coverage-accuracy trade-off via threshold instructions",
    background=[two_stage_framework],
)

# ── Induction: two-stage structure holds across all models ────────────────────

obs_gpt4o_two_stage = claim(
    "GPT-4o exhibits the two-stage confidence-decision structure: Phase 1 confidence dominates "
    "Phase 2 abstention (β_std = −0.99, ~10× larger than alternatives), activation steering "
    "causally shifts abstention via confidence redistribution (67.1% mediation), and Phase 4 "
    "threshold instructions alter Stage 2 while preserving Stage 1 confidence (scale = 1.80).",
    title="GPT-4o: two-stage structure confirmed",
    background=[two_stage_framework],
)

obs_gemma_two_stage = claim(
    "Gemma 3 27B exhibits the two-stage confidence-decision structure: confidence predicts "
    "Phase 2 abstention (similar qualitative pattern to GPT-4o per Supplemental Results); "
    "activation steering in Phase 3 causally modulates abstention (59.5 percentage-point range); "
    "and instructed thresholds systematically modulate Phase 4 abstention (scale = 0.66, shift = +1.0%). "
    "Abstention behavior required prompt rephrasing for reliable elicitation.",
    title="Gemma 3 27B: two-stage structure confirmed (with prompt sensitivity)",
    background=[two_stage_framework],
)

obs_deepseek_qwen_two_stage = claim(
    "DeepSeek 671B (Phase 2 abstention 82.0%, Phase 4 scale = 1.05, shift = −8.5%) and "
    "Qwen 80B (Phase 2 abstention 43.8%, Phase 4 scale = 1.49, shift = −52.3%) both exhibit "
    "the two-stage confidence-decision structure: confidence robustly predicts abstention "
    "in all cases per Supplemental Results.",
    title="DeepSeek 671B and Qwen 80B: two-stage structure confirmed",
    background=[two_stage_framework],
)

s1_two_stage = support(
    [convergent_computational_architecture],
    obs_gpt4o_two_stage,
    reason=(
        "If the two-stage architecture is a convergent property of LLMs "
        "(@convergent_computational_architecture), then GPT-4o should exhibit both Stage 1 "
        "confidence-driven abstention and Stage 2 threshold-based policy — which is exactly "
        "what Phase 2, 3, and 4 show for GPT-4o."
    ),
    prior=0.92,
)

s2_two_stage = support(
    [convergent_computational_architecture],
    obs_gemma_two_stage,
    reason=(
        "If the two-stage architecture is a convergent property of LLMs "
        "(@convergent_computational_architecture), then Gemma 3 27B should also exhibit it, "
        "independently of GPT-4o. Activation steering Phase 3 and Phase 4 threshold results "
        "for Gemma 3 27B provide this independent confirmation."
    ),
    prior=0.88,
)

s3_two_stage = support(
    [convergent_computational_architecture],
    obs_deepseek_qwen_two_stage,
    reason=(
        "If the two-stage architecture is a convergent property of LLMs "
        "(@convergent_computational_architecture), DeepSeek and Qwen should also exhibit it "
        "despite very different training procedures and architectures."
    ),
    prior=0.83,
)

ind_gpt4o_gemma = induction(
    s1_two_stage,
    s2_two_stage,
    law=convergent_computational_architecture,
    reason="GPT-4o and Gemma 3 27B represent independent model families confirming convergence.",
)

ind_all_models = induction(
    ind_gpt4o_gemma,
    s3_two_stage,
    law=convergent_computational_architecture,
    reason="DeepSeek and Qwen add further independent evidence from different training pipelines.",
)

# ── Synthesis strategy ────────────────────────────────────────────────────────

strat_metacognitive_control = support(
    [confidence_causal_role, two_stage_account_validated, phase1_confidence_retains_power],
    metacognitive_control_demonstrated,
    reason=(
        "Confidence representations causally drive abstention (Phase 3 activation steering, "
        "@confidence_causal_role). The behavior follows a two-stage architecture where confidence "
        "is independently formed and then policy-applied (@two_stage_account_validated). "
        "Phase 4 shows Stage 1 confidence survives threshold manipulation intact "
        "(@phase1_confidence_retains_power). Together these meet the criteria for metacognitive "
        "control — not merely calibrated output, but internal evaluation-driven behavioral regulation "
        "[@FlemingDaw2017; @KepecsMainen2012]."
    ),
    prior=0.88,
)

strat_dissociation = support(
    [metacognitive_control_demonstrated, llm_calibration_prior],
    dissociation_verbal_behavioral,
    reason=(
        "LLMs exhibit metacognitive control (@metacognitive_control_demonstrated) through internal "
        "logit-based confidence signals, even though prior work shows verbal confidence reports from "
        "LLMs are frequently overconfident and miscalibrated (@llm_calibration_prior). "
        "This gap between verbal report quality and internal signal quality implies a dissociation "
        "between what models say about their confidence and how they actually use confidence internally."
    ),
    prior=0.82,
)

strat_practical_abstention = support(
    [two_stage_account_validated, threshold_increases_accuracy, phase4_decision_parameters],
    abstention_improves_reliability,
    reason=(
        "The validated two-stage framework (@two_stage_account_validated) shows threshold instructions "
        "directly control Stage 2 policy. Higher thresholds increase accuracy among answered questions "
        "(@threshold_increases_accuracy). Decision parameters such as scale = 1.80 quantify how "
        "much confidence overrides instructed threshold (@phase4_decision_parameters), enabling "
        "principled calibration of the coverage-accuracy trade-off."
    ),
    prior=0.87,
)

# ── Derive two_stage_account_validated from convergent multi-phase evidence ───

strat_synthesize_two_stage = support(
    [confidence_best_predictor, confidence_causal_role, two_stage_fully_validated, cross_model_variation],
    two_stage_account_validated,
    reason=(
        "Three phases of converging evidence establish the two-stage account: "
        "(1) Phase 2 logistic regression shows confidence dominates abstention with β_std = −0.989, "
        "~10× larger than all alternative predictors (@confidence_best_predictor), recovers implicit "
        "threshold T₅₀ = 77%; "
        "(2) Phase 3 activation steering provides direct causal evidence that Stage 1 confidence "
        "representations drive abstention (67.1% mediation via confidence redistribution, "
        "@confidence_causal_role); "
        "(3) Phase 4 demonstrates Stage 2 threshold-policy manipulation while Stage 1 confidence "
        "remains intact (@two_stage_fully_validated); "
        "(4) The two-stage structure generalizes across GPT-4o, Gemma 3 27B, DeepSeek, and Qwen "
        "(@cross_model_variation). "
        "Together these confirm the computational account of LLM abstention [@FlemingDaw2017; @KepecsMainen2012]."
    ),
    prior=0.88,
)

# ── Connect orphaned Phase 1 and Phase 2 supporting claims ────────────────────

strat_phase1_supports_design = support(
    [gpt4o_calibration_result, gpt4o_phase1_accuracy],
    gpt4o_phase2_performance,
    reason=(
        "Phase 1 baseline accuracy (63.7%, @gpt4o_phase1_accuracy) and calibration quality "
        "(ECE = 0.046, AUROC = 0.90, @gpt4o_calibration_result) establish that the model has "
        "meaningful internal confidence estimates before abstention is introduced. "
        "These baseline metrics set context for the Phase 2 abstention behavior (56.6% abstention, "
        "accuracy rising from 63.9% to 69.1%, @gpt4o_phase2_performance)."
    ),
    prior=0.88,
)

strat_gap_addressed = support(
    [two_stage_account_validated, gap_prior_work],
    metacognitive_control_demonstrated,
    reason=(
        "Prior work relied on post-hoc or fine-tuned abstention mechanisms, leaving open whether "
        "models natively use internal confidence signals (@gap_prior_work). "
        "The validated two-stage account (@two_stage_account_validated) directly addresses this gap "
        "by demonstrating native confidence-driven metacognitive control through causal interventions "
        "(activation steering) and behavioral modeling."
    ),
    prior=0.87,
)

strat_phase1_stability = support(
    [phase1_confidence_stability],
    confidence_best_predictor,
    reason=(
        "The stability of Phase 1 confidence rankings across phases — chosen option remains "
        "highest-confidence real option in 82.0% of Phase 2 trials and 81.6% of Phase 4 trials "
        "(@phase1_confidence_stability) — validates using Phase 1 confidence as a clean predictor "
        "for Phase 2 abstention behavior. This justifies @confidence_best_predictor's interpretation "
        "that Phase 1 confidence genuinely represents internal metacognitive state."
    ),
    prior=0.87,
)

strat_threshold_abstention_link = support(
    [threshold_increases_abstention],
    phase4_confidence_dominant,
    reason=(
        "The monotonic increase in abstention with instructed threshold "
        "(@threshold_increases_abstention) confirms that models respond to threshold instructions, "
        "providing the variance in abstention needed to detect the effect of Phase 1 confidence "
        "(@phase4_confidence_dominant, β_std = −1.09) above and beyond threshold (β_std = 1.03). "
        "Without monotonic threshold effects, the regression could not isolate confidence."
    ),
    prior=0.85,
)
