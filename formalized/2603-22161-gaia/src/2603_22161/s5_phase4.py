"""Phase 4: Instructed Threshold Abstention — Stage 2 Policy Manipulation (GPT-4o)"""

from gaia.lang import claim, setting, support

from .motivation import abstention_paradigm_design, two_stage_framework, calibration_method, dataset_setting
from .s2_phase1 import models_tested
from .s3_phase2 import (
    confidence_best_predictor,
    implicit_threshold,
    rag_poor_predictor,
    embeddings_poor_predictor,
)
from .s4_phase3 import confidence_causal_role

# ── Phase 4 setup ────────────────────────────────────────────────────────────

phase4_setup = setting(
    "Phase 4 instructed-threshold design: GPT-4o, DeepSeek 671B, and Qwen 80B were each "
    "instructed to (1) select a 4-way multiple-choice answer, (2) rate confidence on a 0–100 scale "
    "(probability of being judged correct by an oracle), and (3) output the chosen answer if confidence ≥ T, "
    "or output '5' (abstain) if confidence < T, where T ∈ {0%, 10%, 20%, …, 100%}. "
    "For GPT-4o, DeepSeek, Qwen: one standardized prompt was used. "
    "For Gemma 3 27B: the standard prompt produced < 5% abstention up to 80% threshold; "
    "20 paraphrases were generated with Gemini 2.5 Pro; 13/20 exceeded 80% abstention at 100% threshold; "
    "the best-performing paraphrase was used for Gemma 3 27B main results. "
    "Phase 1 confidence (pre-decisional) was used as the predictor; Phase 4 confidence (post-decisional, "
    "already conditioned on the threshold) was analyzed separately as a convergent measure.",
    title="Phase 4 instructed-threshold design and model-specific prompt details",
)

pre_vs_post_decisional = setting(
    "Pre-decisional vs. post-decisional confidence distinction in Phase 4: "
    "Phase 1 confidence is pre-decisional — extracted with no abstention option, representing the "
    "model's raw belief about its answer. "
    "Phase 4 confidence is post-decisional — the model rates confidence after being instructed to "
    "apply a threshold, so it reflects a value already conditioned on the policy. "
    "Empirical signature: when abstention rate is plotted as a 2D function of (threshold, Phase 1 confidence), "
    "the surface shows a smooth diagonal gradient (bandness index = 0.042 — threshold and confidence act "
    "as independent additive inputs). "
    "When plotted against Phase 4 confidence, the surface collapses into horizontal bands "
    "(bandness index = 0.78 — confidence absorbs the threshold effect, reflecting post-decisional processing).",
    title="Pre- vs. post-decisional confidence: diagonal gradient vs. horizontal bands",
)

# ── Phase 4 results ──────────────────────────────────────────────────────────

threshold_increases_abstention = claim(
    "Phase 4 instructed thresholds systematically increase GPT-4o abstention rates: "
    "as the instructed threshold T rises from 0% to 100%, abstention rates increase monotonically.",
    title="Instructed threshold increases abstention monotonically",
    background=[phase4_setup, abstention_paradigm_design, models_tested],
)

threshold_increases_accuracy = claim(
    "Higher instructed thresholds lead to significantly more accurate answered responses in GPT-4o: "
    "logistic regression reveals β = 0.0051 ± 0.001, z = 3.97, p < 0.001, corresponding to "
    "roughly +1.1% increase in accuracy for every 10% increase in threshold — consistent with "
    "stricter thresholds selectively filtering lower-confidence (less reliable) answers.",
    title="Higher threshold → +1.1% accuracy per 10% threshold increase",
    background=[phase4_setup, models_tested],
)

phase4_confidence_dominant = claim(
    "In Phase 4 logistic regression (n = 11,000 trials, one per question-threshold combination), "
    "Phase 1 confidence is the dominant predictor alongside threshold. "
    "Adding confidence to threshold-only model: ΔAIC = −1,953, LR χ²(1) = 1,955, p < 0.001, "
    "pseudo-R² improves from 0.11 to 0.24 (more than doubling). "
    "Standardized effect sizes: confidence β_std = −1.09 ± 0.03 (z = −34.1, p < 10⁻²⁵⁴), "
    "threshold β_std = 1.03 ± 0.03 (z = 38.4, p < 10⁻³²⁰) — roughly comparable. "
    "RAG β_std = −0.22, difficulty β_std = 0.05 (p = 0.071), top embedding β_std = −0.11 — "
    "all substantially smaller. "
    "Confidence effect is 5.1× larger than RAG, 21.3× larger than difficulty, 10.2× larger "
    "than top embedding.",
    title="Phase 4: Confidence β_std = -1.09 comparable to threshold β_std = 1.03",
    background=[phase4_setup, calibration_method, models_tested],
)

phase4_decision_parameters = claim(
    "From the fitted confidence + threshold + difficulty model for GPT-4o Phase 4 "
    "(β_T = 0.033, β_C = −0.058, β_D = 0.159), three interpretable decision parameters are derived: "
    "(1) Scale = −β_C / β_T = 1.80: GPT-4o weights its internal confidence nearly twice as heavily "
    "as the instructed threshold; a 1% increase in confidence offsets ~1.80% of instructed threshold. "
    "(2) Shift = −β₀ / β_T = −97.6%: large negative bias causing the model to abstain even at "
    "confidence levels above threshold (conservative). "
    "(3) Policy temperature = 1/β_T = 31.0 percentage units: soft decision boundary. "
    "Example indifference point: at 80% confidence, T₅₀ ≈ 46%.",
    title="Phase 4 decision parameters: scale=1.80, shift=-97.6%, temperature=31",
    background=[phase4_setup, two_stage_framework, models_tested],
)

phase1_confidence_retains_power = claim(
    "Phase 1 confidence retains strong predictive power across all Phase 4 threshold conditions, "
    "demonstrating that instructed thresholds operate primarily at Stage 2 (thresholding policy) "
    "rather than by distorting Stage 1 confidence representations. "
    "The smooth diagonal gradient of abstention as a function of (threshold, Phase 1 confidence) "
    "— bandness index = 0.042 — confirms Phase 1 confidence acts as an independent pre-decisional "
    "input to the decision process.",
    title="Phase 1 confidence retains predictive power under threshold manipulation",
    background=[phase4_setup, pre_vs_post_decisional, two_stage_framework],
)

# ── Cross-model comparison ───────────────────────────────────────────────────

cross_model_variation = claim(
    "Substantial variation exists across models in Phase 2 baseline abstention rates and Phase 4 "
    "decision parameters, while the fundamental two-stage architecture is preserved across all models. "
    "Phase 2 free abstention rates: DeepSeek 82.0%, GPT-4o 56.6%, Qwen 80B 43.8%, Gemma 3 27B 27.2%. "
    "Phase 4 shift parameters (baseline bias independent of confidence/threshold): "
    "GPT-4o −97.6%, Qwen 80B −52.3%, DeepSeek −8.5%, Gemma 3 27B +1.0%. "
    "Phase 4 scale parameters (confidence weight relative to threshold): "
    "GPT-4o 1.80, Qwen 80B 1.49, DeepSeek 1.05, Gemma 3 27B 0.66. "
    "In all models, Phase 1 confidence robustly predicts abstention, confirming the two-stage "
    "computational structure is a convergent property across LLM architectures.",
    title="Cross-model variation in parameters; two-stage structure preserved across all models",
    background=[phase4_setup, two_stage_framework, models_tested],
)

# ── Reasoning ────────────────────────────────────────────────────────────────

two_stage_stage2_localized = claim(
    "Instructed thresholds operate primarily at Stage 2 (the threshold-based policy) of the "
    "two-stage confidence-decision framework, leaving Stage 1 confidence representations intact. "
    "Evidence: Phase 1 confidence (pre-decisional, measured without abstention option) retains "
    "β_std = −1.09 predictive power across all threshold conditions; abstention as a function of "
    "(threshold, Phase 1 confidence) shows a smooth diagonal gradient (bandness index = 0.042), "
    "indicating the two inputs act independently.",
    title="Threshold manipulation localizes to Stage 2; Stage 1 confidence preserved",
    background=[two_stage_framework, pre_vs_post_decisional],
)

strat_threshold_operates_stage2 = support(
    [phase4_confidence_dominant, phase1_confidence_retains_power],
    two_stage_stage2_localized,
    reason=(
        "If instructed thresholds altered Stage 1 confidence representations themselves, "
        "Phase 1 confidence (pre-decisional) would lose predictive power at higher thresholds. "
        "Instead, Phase 1 confidence retains β_std ≈ −1.09 across all threshold conditions "
        "(@phase4_confidence_dominant). The diagonal gradient pattern (bandness index = 0.042) "
        "confirms threshold and confidence act as independent inputs (pre_vs_post_decisional). "
        "This localizes the threshold effect to Stage 2 of the two-stage framework "
        "[@FlemingDaw2017; @KepecsMainen2012]."
    ),
    prior=0.87,
    background=[pre_vs_post_decisional],
)

two_stage_fully_validated = claim(
    "The full two-stage confidence-decision framework is validated: Stage 1 (confidence formation) "
    "and Stage 2 (threshold-based policy) are operationally separable and independently causal. "
    "Stage 1 evidence: activation steering of confidence representations directly shifts abstention "
    "(Phase 3, 67.1% mediation via confidence redistribution). "
    "Stage 2 evidence: instructed threshold manipulation shifts abstention without disturbing "
    "Stage 1 confidence (Phase 4, Phase 1 confidence retains β_std = −1.09 under all thresholds). "
    "The framework generalizes across GPT-4o, Gemma 3 27B, DeepSeek 671B, and Qwen 80B.",
    title="Full two-stage framework validated: Stage 1 and Stage 2 are separable and causal",
    background=[two_stage_framework],
)

strat_convergent_two_stage = support(
    [confidence_causal_role, two_stage_stage2_localized, cross_model_variation],
    two_stage_fully_validated,
    reason=(
        "Causal evidence from Phase 3 activation steering (@confidence_causal_role) established "
        "that confidence representations drive abstention via Stage 1. Phase 4 localizes threshold "
        "instructions to Stage 2 without disrupting Stage 1 (@two_stage_stage2_localized). "
        "The two-stage structure is consistent across GPT-4o, DeepSeek, Qwen, and Gemma 3 27B "
        "(@cross_model_variation), suggesting a convergent computational solution across LLM architectures."
    ),
    prior=0.87,
)
