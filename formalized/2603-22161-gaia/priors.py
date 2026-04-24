"""
Priors for the Causal Evidence / Confidence-Driven LLM Abstention package.
arXiv: 2603.22161 — Kumaran et al. (2026), Google DeepMind.

Reviewer notes:
- Empirical measurements (Phase 1-4 logistic regressions, calibration, steering effects):
  directly reported statistical results with large sample sizes (n=1,000 or 11,000).
  These receive high priors (0.88-0.93).
- Mediation analysis results: formally specified models with cluster-robust SE and
  bootstrap CIs. High priors (0.88-0.92).
- Alternative hypotheses: set based on explanatory power for the observation, NOT
  whether the alternative's calculation is correct. RAG and policy alternatives
  receive low priors because they fail to explain the data as well as confidence.
- Cross-model generalizations based partly on Supplemental Results (not main text):
  slightly lower prior (0.85).
"""

from gaia.lang import prior

# ── Phase 1: Baseline calibration and accuracy ────────────────────────────────

prior("gpt4o_phase1_accuracy", 0.92,
      "63.7% Phase 1 accuracy is a direct experimental measurement from 1,000 trials. "
      "High confidence in this count-based result.")

prior("gpt4o_calibration_result", 0.92,
      "ECE = 0.046 and AUROC = 0.90 are standard calibration metrics on 1,000 held-out trials "
      "using the well-established temperature-scaling method of Guo et al. (2017). "
      "High confidence in these directly reported values.")

prior("confidence_predicts_error", 0.93,
      "r = -0.97, p < 0.001, Cohen's d = -8.13 across binned confidence-accuracy pairs. "
      "Very strong correlation; standard psychometric analysis. High confidence.")

prior("phase1_confidence_stability", 0.90,
      "82.0% of Phase 2 trials and 81.6% of Phase 4 trials have Phase 1 chosen option "
      "as highest-confidence real option. Directly counted from trial data. High confidence.")

# ── Phase 2: Free abstention regression results ───────────────────────────────

prior("gpt4o_phase2_performance", 0.93,
      "56.6% abstention, 30.0% correct, 13.4% incorrect from n=1,000 trials. "
      "Direct count from Phase 2 experimental run. High confidence.")

prior("confidence_effect_size_dominant", 0.92,
      "β_std = -0.989, z = -10.56, p < 10^-25 for confidence in full logistic regression. "
      "9-10x larger than all alternative predictors. Very strong statistical evidence.")

prior("rag_poor_predictor", 0.90,
      "RAG alone: pseudo-R² = 0.005. Adding RAG above confidence: ΔAIC = -1.0, p = 0.085 "
      "(non-significant). Strong statistical evidence that RAG does not independently drive abstention.")

prior("embeddings_poor_predictor", 0.90,
      "Sentence embeddings alone: pseudo-R² = 0.017. Modest gain above confidence (LR χ²(10)=41.4, "
      "p < 10^-5, ΔAIC=-21.4) but dwarfed by confidence's contribution. Strong statistical evidence.")

prior("difficulty_marginal", 0.88,
      "Difficulty β_D = 0.50 ± 0.26, z = 1.94, p = 0.053 in confidence+difficulty model; "
      "β_std = 0.110, p = 0.197 in full standardized model. Consistent pattern of marginality.")

# ── Phase 3: Activation steering results ────────────────────────────────────────

prior("steering_effect_on_abstention", 0.93,
      "59.5 pp reduction from 66.5% to 7.0%; 15.34%/unit change; r = -0.99, p < 0.001 "
      "across layers 30-40 of 62-layer network. Extremely strong, precisely measured effect.")

prior("steering_effect_on_confidence", 0.90,
      "Correlated shift in max real confidence and abstention confidence under steering: "
      "r(43,998) = -0.89, p < 0.001, Cohen's d = 4.0. Large effect with huge sample size.")

prior("steering_accuracy_tradeoff", 0.88,
      "Accuracy decline from 59.2% to 53.7% across steering range; 1.36%/unit, r = -0.94, "
      "R² = 0.89. Small but real effect, consistent with coverage-accuracy trade-off.")

# ── Phase 3: Mediation analysis results ──────────────────────────────────────────

prior("mediation_total_effect", 0.92,
      "Total effect c = -0.824, 95% CI [-0.885, -0.673], p < 0.001. "
      "Formally specified mediation model with cluster-robust SE and 1,000 bootstrap samples.")

prior("mediation_confidence_redistribution", 0.90,
      "a1 = 0.107, b1 = -5.15, indirect effect -0.55, 95% CI [-0.65, -0.47]. "
      "67.1% of total effect. Formal bootstrap mediation with cluster correction.")

prior("mediation_policy_shift", 0.88,
      "a2 = -0.0038, b2 = 56.6, indirect effect -0.22, 95% CI [-0.24, -0.19]. "
      "26.2% of total effect. Significant secondary pathway but much smaller than M1.")

prior("mediation_combined_coverage", 0.90,
      "Combined indirect effect -0.77, 95% CI [-0.89, -0.67]. 93.3% of total effect "
      "mediated through measured pathways. Direct effect c' = -0.32 remains.")

prior("mediation_difficulty_robust", 0.90,
      "With difficulty covariate: indirect via confidence = -0.60, 71.0% of total c = -0.84. "
      "Mediation robust to confounding by item difficulty. Same conclusion, same direction.")

# ── Phase 4: Instructed threshold results ────────────────────────────────────────

prior("threshold_increases_abstention", 0.93,
      "Monotonic increase in abstention as threshold rises from 0% to 100%. "
      "Directly counted across 11,000 trials (11 thresholds × 1,000 questions).")

prior("threshold_increases_accuracy", 0.88,
      "β = 0.0051 ± 0.001, z = 3.97, p < 0.001 for threshold on accuracy among answered trials. "
      "+1.1% per 10% threshold increase. Statistically significant, expected direction.")

prior("phase4_confidence_dominant", 0.92,
      "ΔAIC = -1,953 adding confidence to threshold-only model; LR χ²(1) = 1,955, p < 0.001. "
      "β_std = -1.09, z = -34.1, p < 10^-254. Confidence and threshold (β_std=1.03) comparable. "
      "Extremely strong evidence from n=11,000.")

prior("phase4_decision_parameters", 0.88,
      "Scale = 1.80, shift = -97.6%, policy temperature = 31.0 derived from fitted logistic "
      "coefficients. Interpretation (overweighting of confidence, conservative bias) is "
      "model-dependent but coefficients are directly estimated.")

prior("phase1_confidence_retains_power", 0.90,
      "Bandness index = 0.042 for Phase 1 confidence (diagonal gradient in 2D abstention surface). "
      "Contrasts with bandness = 0.78 for Phase 4 confidence. Strong empirical dissociation "
      "between pre- and post-decisional confidence.")

# ── Cross-model generalization ─────────────────────────────────────────────────

prior("cross_model_variation", 0.85,
      "Phase 2 abstention rates directly measured for all 4 models. Phase 4 scale/shift "
      "parameters from fitted models in Supplemental Results. High confidence in Phase 2 "
      "rates; moderate for Supplemental Phase 4 parameters not shown in main text.")

# ── Background / prior work ─────────────────────────────────────────────────────

prior("gap_prior_work", 0.82,
      "Well-documented gap: prior abstention methods use post-hoc calibration or fine-tuning. "
      "The paper surveys many such methods (Tjandra 2024, Yadkori 2024, Chuang 2024, Zhang 2024). "
      "The gap characterization is accurate as of this paper's submission (March 2026).")

prior("llm_calibration_prior", 0.88,
      "Substantial established body of work: Guo 2017 (temperature scaling), Xiong 2023, "
      "Steyvers 2025, Kadavath 2022. The claim that confidence can be extracted and calibrated "
      "is very well established. High prior.")

# ── Hypothesis claims (for abduction strategies) ──────────────────────────────
# These are the COMPETING EXPLANATIONS used as H and Alt in abduction.
# Prior = probability the hypothesis CAN ALONE explain the relevant observation.

prior("confidence_hypothesis", 0.80,
      "Prior probability that internal confidence signals drive LLM abstention. "
      "Motivated by biological metacognition parallels and LLM calibration literature. "
      "Not yet causally established before Phase 3; set at moderately high prior.")

prior("alt_rag_drives_abstention", 0.20,
      "Prior probability that RAG-accessibility (not confidence) drives abstention. "
      "RAG scores should then predict abstention independently of confidence; "
      "pre-experimental plausibility is low but non-negligible (knowledge-gap abstention is real). "
      "Set low because this is the NULL/alternative hypothesis in the paper.")

prior("alt_steering_through_policy", 0.25,
      "Prior that steering works primarily through decision-policy changes (Stage 2), "
      "not confidence redistribution (Stage 1). Physically plausible since steering "
      "could disrupt any part of processing; set low reflecting the prior from the "
      "two-stage framework that Stage 1 confidence is the proximal cause.")

# ── Prediction claims (for compare strategies) ────────────────────────────────
# These express what each hypothesis predicts; set to match the hypothesis prior.

prior("pred_confidence_wins", 0.80,
      "Confidence hypothesis prediction: confidence should dominate RAG in Phase 2 regression. "
      "Set equal to confidence_hypothesis prior.")

prior("pred_rag_wins", 0.20,
      "RAG hypothesis prediction: RAG should explain substantial abstention variance. "
      "Set equal to alt_rag_drives_abstention prior.")

prior("pred_confidence_causal", 0.80,
      "Confidence-redistribution prediction: M1 (net confidence shift) should dominate "
      "Phase 3 mediation. Set equal to confidence_hypothesis prior.")

prior("pred_policy_causal", 0.25,
      "Policy-change prediction: M2 (policy shift) should dominate Phase 3 mediation. "
      "Set equal to alt_steering_through_policy prior.")
