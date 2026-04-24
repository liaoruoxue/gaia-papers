"""Phase 2: Free Abstention — Confidence as Dominant Predictor (GPT-4o)"""

from gaia.lang import claim, setting, support, abduction, compare

from .motivation import (
    abstention_paradigm_design,
    two_stage_framework,
    calibration_method,
    dataset_setting,
)
from .s2_phase1 import gpt4o_phase1_accuracy, confidence_predicts_error, models_tested

# ── Phase 2 performance ──────────────────────────────────────────────────────

gpt4o_phase2_performance = claim(
    "GPT-4o Phase 2 performance (with abstention option, n=1,000 questions): "
    "30.0% correct, 13.4% incorrect, 56.6% abstention. "
    "With abstention available, the accuracy among answered questions rose from 63.9% to 69.1%, "
    "consistent with a coverage-accuracy trade-off.",
    title="GPT-4o Phase 2 performance: 56.6% abstention, 69.1% accuracy on answered",
    background=[abstention_paradigm_design, dataset_setting, models_tested],
)

phase1_confidence_stability = claim(
    "The Phase 1 chosen option remained the highest-confidence real option in 82.0% of Phase 2 trials "
    "and 81.6% of Phase 4 trials, demonstrating substantial stability of confidence rankings across "
    "phases despite the presence of the abstention option.",
    title="Phase 1 confidence rankings stable across phases (82.0% agreement in Phase 2)",
    background=[abstention_paradigm_design, models_tested],
)

# ── Model comparison: predictors of abstention ───────────────────────────────

confidence_best_predictor = claim(
    "Phase 1 Chosen Confidence is the dominant predictor of Phase 2 abstention behavior in GPT-4o. "
    "In logistic regression, confidence alone yields AIC = 1227.4 and pseudo-R² = 0.106, reducing "
    "AIC by 119.2 points versus difficulty alone (AIC = 1346.6, pseudo-R² = 0.019). "
    "The confidence effect: β_C = −4.87 ± 0.47, z = −10.37, p < 0.001. "
    "A 0.1-unit increase in confidence (e.g., from 0.70 to 0.80) reduces the probability of "
    "abstaining by approximately 12 percentage points.",
    title="Confidence dominates abstention prediction (AIC reduction 119 vs. difficulty)",
    background=[abstention_paradigm_design, calibration_method, models_tested],
)

rag_poor_predictor = claim(
    "RAG scores (retrieval-augmented generation scores measuring semantic overlap between questions "
    "and retrieved knowledge passages [@Lewis2020]) are a poor predictor of abstention behavior: "
    "AIC = 1365.6, pseudo-R² = 0.005. "
    "Adding RAG to a model already containing confidence produces only a non-significant marginal "
    "improvement (LR χ²(1) = 2.96, p = 0.085, ΔAIC = −1.0).",
    title="RAG scores poor predictor: AIC=1365.6, pseudo-R²=0.005",
    background=[abstention_paradigm_design, models_tested],
)

embeddings_poor_predictor = claim(
    "Surface-level sentence embeddings (10 principal components from dense vector representations "
    "of questions [@Bommasani2021; @Reimers2019]) predict abstention weakly: "
    "AIC = 1368.2, pseudo-R² = 0.017. "
    "Adding embeddings above confidence yields a modest but significant contribution "
    "(LR χ²(10) = 41.42, p < 10⁻⁵, ΔAIC = −21.4), but the reverse (confidence above embeddings) "
    "is far larger (LR χ²(1) = 164.22, p < 10⁻³⁷).",
    title="Sentence embeddings weak predictor: AIC=1368.2, pseudo-R²=0.017",
    background=[abstention_paradigm_design, models_tested],
)

difficulty_marginal = claim(
    "Question difficulty (mean accuracy across 20 GPT-4o runs with different random seeds "
    "for answer-choice permutation) is a marginal predictor of abstention. "
    "In the combined confidence + difficulty model, difficulty effect: "
    "β_D = 0.50 ± 0.26, z = 1.94, p = 0.053. "
    "In the full standardized model, difficulty effect size: β_std = 0.110 ± 0.086, z = 1.29, p = 0.197.",
    title="Question difficulty marginal predictor (β_std = 0.110, p=0.197 in full model)",
    background=[abstention_paradigm_design, models_tested],
)

confidence_effect_size_dominant = claim(
    "In the full logistic regression model with all predictors standardized (zero mean, unit variance), "
    "confidence exhibits the dominant effect size: β_std = −0.989 ± 0.094, z = −10.56, p < 10⁻²⁵. "
    "Confidence is 9.7× larger than RAG (β_std = −0.102), 9.0× larger than difficulty (β_std = 0.110), "
    "and 9.4× larger than the top embedding component (PC6: β_std = 0.106, z = 4.04, p < 10⁻⁴). "
    "Effect sizes are approximately an order of magnitude larger for confidence than all alternatives.",
    title="Confidence effect 9–10× larger than all alternative predictors",
    background=[abstention_paradigm_design, calibration_method, models_tested],
)

# ── Implicit threshold recovery ──────────────────────────────────────────────

implicit_threshold = claim(
    "The implicit abstention threshold recovered from the confidence-only logistic regression model "
    "is approximately 77% calibrated confidence at average question difficulty (the indifference point "
    "T₅₀ where P(abstain) = 0.5). "
    "Policy temperature = 20 confidence units (1/|β_C|), indicating a relatively gradual, "
    "soft probabilistic transition between answering and abstaining around the threshold.",
    title="GPT-4o implicit abstention threshold: 77% confidence, policy temperature 20 units",
    background=[abstention_paradigm_design, two_stage_framework],
)

# ── Alternative hypotheses for what drives abstention ───────────────────────

alt_rag_drives_abstention = claim(
    "An alternative explanation: GPT-4o abstention is driven primarily by knowledge retrieval "
    "accessibility (RAG scores) rather than internal confidence — models abstain when relevant "
    "knowledge is harder to retrieve.",
    title="Alternative: RAG/knowledge-accessibility drives abstention",
)

# ── Abduction: confidence vs. RAG as the driver of abstention ────────────────
# The observation is the abstention pattern; two hypotheses attempt to explain it.

obs_abstention_pattern = claim(
    "GPT-4o Phase 2 abstention behavior shows a strong systematic pattern: "
    "models abstain more on questions where their internal state signals low certainty, "
    "producing an overall abstention rate of 56.6% with a smooth graded response.",
    title="Observation: systematic abstention pattern in Phase 2",
    background=[abstention_paradigm_design, models_tested],
)

confidence_hypothesis = claim(
    "The metacognitive confidence hypothesis: LLMs use internal confidence signals "
    "(derived from calibrated logits) as the dominant driver of abstention decisions, "
    "paralleling confidence-based metacognitive control in biological systems.",
    title="Hypothesis: metacognitive confidence drives abstention",
)

pred_confidence_wins = claim(
    "If confidence drives abstention, Phase 1 Chosen Confidence alone should substantially "
    "outperform RAG scores in predicting Phase 2 abstention (in terms of AIC and pseudo-R²), "
    "and its standardized effect size should be an order of magnitude larger.",
    title="Prediction: confidence outperforms RAG in abstention regression",
)

pred_rag_wins = claim(
    "If RAG-accessibility drives abstention, RAG scores should provide substantial "
    "independent predictive power for abstention, with an effect size comparable to confidence.",
    title="Prediction: RAG scores explain abstention comparably to confidence",
)

comp_confidence_vs_rag = compare(
    pred_confidence_wins,
    pred_rag_wins,
    obs_abstention_pattern,
    reason=(
        "Confidence alone: AIC = 1227.4, pseudo-R² = 0.106. "
        "RAG alone: AIC = 1365.6, pseudo-R² = 0.005. "
        "Adding RAG above confidence: ΔAIC = −1.0 (p = 0.085, non-significant). "
        "Adding confidence above RAG: ΔAIC = −139.1 (p < 10⁻³²). "
        "Standardized effect sizes: confidence β_std = −0.989, RAG β_std = −0.102. "
        "Confidence is 9.7× larger, confirming the confidence hypothesis prediction "
        "and contradicting the RAG-accessibility prediction."
    ),
    prior=0.92,
)

s_conf_h = support(
    [confidence_hypothesis],
    obs_abstention_pattern,
    reason=(
        "The metacognitive confidence hypothesis predicts that internal confidence signals "
        "(@confidence_hypothesis) should produce a strong, graded abstention pattern tied to "
        "the model's certainty about its answer — exactly matching the observed systematic "
        "abstention pattern (@obs_abstention_pattern). "
        "Calibrated confidence strongly predicts error rate (r = −0.97, @confidence_predicts_error), "
        "establishing that these signals carry genuine metacognitive information."
    ),
    prior=0.90,
)

s_rag_alt = support(
    [alt_rag_drives_abstention],
    obs_abstention_pattern,
    reason=(
        "If RAG-accessibility drives abstention (@alt_rag_drives_abstention), questions with "
        "lower knowledge retrieval overlap should trigger abstention, producing a pattern "
        "correlated with RAG scores rather than internal confidence. "
        "However, the RAG-alone model yields pseudo-R² = 0.005 and is non-significant above "
        "confidence, meaning RAG scores have minimal explanatory power for the abstention pattern."
    ),
    prior=0.15,
)

abduction_confidence_dominance = abduction(
    s_conf_h,
    s_rag_alt,
    comp_confidence_vs_rag,
    reason=(
        "Both the confidence hypothesis and the RAG-accessibility hypothesis are candidate "
        "explanations for what drives GPT-4o abstention (@obs_abstention_pattern). "
        "Model comparison across multiple predictor sets reveals confidence as overwhelmingly "
        "dominant, providing strong abductive support for the metacognitive confidence account [@Guo2017]."
    ),
    background=[abstention_paradigm_design, two_stage_framework],
)

strat_implicit_threshold = support(
    [confidence_best_predictor, gpt4o_phase2_performance],
    implicit_threshold,
    reason=(
        "Given that Phase 1 confidence is the dominant predictor of abstention (@confidence_best_predictor), "
        "the logistic regression model Pr(abstain | Conf, Diff) = σ(β₀ + β_C·Conf + β_D·Diff) "
        "recovers decision parameters from the fitted coefficients. "
        "The indifference point T₅₀ = −β₀/β_C at mean difficulty is 77% confidence. "
        "Policy temperature = 1/|β_C| = 20 confidence units, consistent with the gradual "
        "transition in abstention behavior observed across Phase 2 (@gpt4o_phase2_performance). "
        "This parallels confidence-based threshold models from neuroscience [@KepecsMainen2012]."
    ),
    prior=0.88,
)

# ── Connect orphaned empirical evidence to the confidence-dominance claim ────

strat_eff_size_to_best = support(
    [confidence_effect_size_dominant, rag_poor_predictor, embeddings_poor_predictor, difficulty_marginal],
    confidence_best_predictor,
    reason=(
        "The claim that confidence is the dominant predictor (@confidence_best_predictor) is "
        "directly established by four lines of evidence: "
        "(1) standardized effect size β_std = −0.989 for confidence, ~10× larger than all alternatives "
        "(@confidence_effect_size_dominant); "
        "(2) RAG alone: pseudo-R² = 0.005, non-significant above confidence (@rag_poor_predictor); "
        "(3) embeddings alone: limited predictive power, modest gain above confidence (@embeddings_poor_predictor); "
        "(4) difficulty: marginal in combined model (p = 0.053–0.197, @difficulty_marginal). "
        "Together, these show confidence uniquely dominates the prediction."
    ),
    prior=0.92,
)
