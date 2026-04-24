"""Phase 3: Causal Evidence via Activation Steering (Gemma 3 27B)"""

from gaia.lang import claim, setting, support, abduction, compare

from .motivation import abstention_paradigm_design, two_stage_framework, dataset_setting
from .s2_phase1 import models_tested
from .s3_phase2 import confidence_best_predictor

# ── Activation steering setup ────────────────────────────────────────────────

steering_setup = setting(
    "Activation steering setup for Gemma 3 27B (62-layer transformer): "
    "Steering vectors were derived from Phase 2 residual stream activations at the last prompt token. "
    "High-confidence trials (25 trials) and low-confidence trials (25 trials) were selected based on "
    "confidence margin m = max_i(C_i) − C_abstain, choosing from top-75 and bottom-75 ranked trials, "
    "matched so that the distribution of chosen options (1–4) was balanced (max proportion ≤ 28%). "
    "High-confidence group: mean calibrated confidence = 0.64 (SD = 0.039); "
    "low-confidence group: mean calibrated confidence = 0.29 (SD = 0.031). "
    "The high-confidence steering vector v_high = μ(H) − μ(L) (mean activations of high- minus "
    "low-confidence trials); v_low = −v_high. "
    "At test time: r̃^(l) = r^(l) + α·v^(l), where v^(l) is scaled to 3% of the mean residual norm "
    "at layer l, and α ∈ {0.5, 1.0, 1.5, 2.0} (with negative α for low-confidence steering). "
    "Phase 3 used 500 of the 1,000 Phase 2 questions. Baseline (no-steering) abstention was 28.2% "
    "for these 500 questions on Phase 2.",
    title="Activation steering vector construction and application (Gemma 3 27B)",
)

mediation_setup = setting(
    "Parallel mediation analysis setup for Phase 3: "
    "Two parallel mediators were constructed. "
    "M1 (confidence redistribution mediator) = ΔMax Real Confidence − ΔAbstention Confidence, "
    "where ΔMax Real = max_i(C_i) − max_i(C_baseline_i) and ΔAbstention = C_5 − C_baseline_5. "
    "M2 (policy shift mediator) = σ(α_s + β_s·C_m) − σ(α_b + β_b·C_m), the difference in "
    "predicted abstention probability between steered and baseline calibration curves at each "
    "trial's confidence level C_m. "
    "Item-level baseline corrections control for stable item-level confounds. "
    "Cluster-robust standard errors account for multiple observations per item. "
    "Bootstrap confidence intervals (B=1,000 cluster bootstrap samples) are reported for indirect effects. "
    "The two mediators were only weakly correlated (r = −0.24), supporting parallel pathway treatment.",
    title="Mediation analysis specification (parallel dual mediator)",
)

# ── Activation steering results ──────────────────────────────────────────────

steering_effect_on_abstention = claim(
    "Activation steering with high- and low-confidence vectors markedly shifted Gemma 3 27B abstention rates. "
    "Across layers 30–40 of the 62-layer network: "
    "abstention rate declined from 66.5% at maximum low-confidence steering (α = −2) to "
    "7.0% at maximum high-confidence steering (α = +2) — a 59.5 percentage-point reduction. "
    "This represents a 15.34% change in abstention per unit increase in steering strength "
    "(r = −0.99, p < 0.001). "
    "Peak steering effect occurred at layer 31 (mid-network). "
    "Baseline no-steering abstention rate: 28.2%.",
    title="Steering reduces abstention: 66.5% → 7.0% across full steering range",
    background=[steering_setup, abstention_paradigm_design, models_tested],
)

steering_effect_on_confidence = claim(
    "Activation steering with high-confidence vectors increased max real confidence (max over real options) "
    "and decreased abstention confidence; low-confidence steering had the reverse effects. "
    "Baseline max real confidence = 0.37; baseline abstention confidence = 0.25. "
    "The change in max real confidence was highly correlated with the change in abstention confidence "
    "(r(43,998) = −0.89, p < 0.001, Cohen's d = 4.0), suggesting steering induces a coordinated shift "
    "of confidence from the abstention option toward real answer options.",
    title="Steering induces coordinated confidence redistribution (r = -0.89)",
    background=[steering_setup, models_tested],
)

steering_accuracy_tradeoff = claim(
    "Activation steering produced a small but significant linear decrease in response accuracy "
    "among answered questions as steering strength increased from low confidence (α = −2) to "
    "high confidence (α = +2): accuracy declined from 59.2% to 53.7%, a decrease of 1.36% per "
    "unit increase in steering strength (r = −0.94, p < 0.001, R² = 0.89). "
    "Coverage changed correspondingly from 33.5% to 93% across the full steering range, "
    "reflecting a mild coverage-accuracy trade-off.",
    title="Steering induces mild accuracy-coverage trade-off (1.36%/unit)",
    background=[steering_setup, models_tested],
)

# ── Mediation analysis results ────────────────────────────────────────────────

mediation_total_effect = claim(
    "The total effect of activation steering (signed strength X) on abstention rate is "
    "c = −0.824 (95% CI: [−0.885, −0.673], p < 0.001), confirming that steering "
    "significantly reduced abstention selection rates overall.",
    title="Total steering effect on abstention: c = -0.824 (p < 0.001)",
    background=[mediation_setup, steering_setup],
)

mediation_confidence_redistribution = claim(
    "Confidence redistribution (M1 = ΔMax Real Confidence − ΔAbstention Confidence) is the "
    "dominant mediator of the steering effect on abstention. "
    "Path a1 (steering → M1): a1 = 0.107 (p < 0.001). "
    "Path b1 (M1 → abstention): b1 = −5.15 (p < 0.001). "
    "Indirect effect a1 × b1 = −0.55 (95% CI: [−0.65, −0.47]). "
    "Confidence redistribution accounts for 67.1% of the total steering effect.",
    title="Confidence redistribution: 67.1% of total steering effect",
    background=[mediation_setup, steering_setup],
)

mediation_policy_shift = claim(
    "Policy changes (M2 = difference in predicted abstention probability between steered and "
    "baseline calibration curves) contribute a secondary indirect pathway. "
    "Path a2 (steering → M2): a2 = −0.0038 (p < 0.001). "
    "Path b2 (M2 → abstention): b2 = 56.6 (p < 0.001). "
    "Indirect effect a2 × b2 = −0.22 (95% CI: [−0.24, −0.19]). "
    "Policy shift accounts for 26.2% of the total steering effect.",
    title="Policy shift: 26.2% of total steering effect (secondary pathway)",
    background=[mediation_setup, steering_setup],
)

mediation_combined_coverage = claim(
    "The combined indirect effect through both mediators (confidence redistribution + policy shift) "
    "is −0.77 (95% CI: [−0.89, −0.67]). "
    "Together the two mediators account for 93.3% of the total steering effect. "
    "A residual direct effect c′ = −0.32 (95% CI: [−0.24, −0.09]) remains, possibly reflecting "
    "nonlinear confidence interactions not captured by the parallel mediator model.",
    title="Combined mediation: 93.3% of steering effect explained by two mediators",
    background=[mediation_setup, steering_setup],
)

mediation_difficulty_robust = claim(
    "When item difficulty is added as a covariate in the mediation analysis, "
    "confidence redistribution remains the dominant pathway: a = 0.11, b = −5.56, "
    "indirect effect = −0.60 (95% CI: [−0.69, −0.52]), accounting for 71.0% of the total effect "
    "(total c = −0.84). Item difficulty independently predicts fewer abstentions (γ = −1.06, p < 0.001), "
    "but does not attenuate the mediation through confidence redistribution.",
    title="Mediation result robust to difficulty covariate (71.0% via confidence)",
    background=[mediation_setup, steering_setup],
)

# ── Causal claim: confidence drives abstention ────────────────────────────────

confidence_causal_role = claim(
    "Confidence signals play a causal role in driving abstention in LLMs. "
    "Injecting high-confidence activation patterns at Gemma 3 27B's mid-layers (peak at layer 31) "
    "reduces abstention rates; injecting low-confidence patterns increases them. "
    "Mediation analysis confirms that this causal effect operates predominantly through "
    "confidence redistribution (67.1%) rather than policy changes alone (26.2%), "
    "establishing that Stage 1 confidence representations — not merely the decision policy — "
    "are the primary driver of abstention behavior [@Turner2023; @Panickssery2023].",
    title="Confidence causally drives abstention via Stage 1 representations",
    background=[two_stage_framework, steering_setup],
)

# ── Alternative: steering acts through policy, not confidence ─────────────────

alt_steering_through_policy = claim(
    "An alternative account of the activation steering effect: steering influences abstention "
    "primarily by altering the decision policy (Stage 2 threshold/temperature parameters), "
    "with observed confidence changes being incidental rather than causal.",
    title="Alternative: steering acts through policy changes, not confidence",
)

# The observation is the steering-induced shift in abstention across all conditions
obs_steering_shifts_abstention = claim(
    "Activation steering of Gemma 3 27B shifts abstention rates by up to 59.5 percentage points "
    "(from 66.5% at α = −2 to 7.0% at α = +2), with a 15.34% change per unit steering strength "
    "(r = −0.99, p < 0.001, averaged across layers 30–40). "
    "Baseline abstention was 28.2% with no steering.",
    title="Observation: steering shifts abstention 59.5 pp across full range",
    background=[steering_setup, models_tested],
)

pred_confidence_causal = claim(
    "If confidence redistribution is causal, the dominant mediation pathway (by proportion of "
    "total effect) through M1 (net confidence shift = ΔMax Real − ΔAbstention confidence) "
    "should substantially exceed the M2 (policy shift) pathway.",
    title="Confidence-causal prediction: M1 dominates mediation",
)

pred_policy_causal = claim(
    "If the policy-change alternative is correct, M2 (policy shift in calibration curve) should "
    "dominate the mediation pathway, and M1 should contribute only marginally.",
    title="Policy-alternative prediction: M2 dominates mediation",
)

comp_mechanism = compare(
    pred_confidence_causal,
    pred_policy_causal,
    obs_steering_shifts_abstention,
    reason=(
        "M1 (confidence redistribution) accounts for 67.1% vs. M2 (policy shift) 26.2% of the "
        "total steering effect on abstention. Indirect effect via M1 = −0.55 vs. M2 = −0.22 "
        "(approximately 2.5× larger for M1). Combined mediation = 93.3%. "
        "This clearly favors the confidence-redistribution prediction [@VanderWeele2015]."
    ),
    prior=0.90,
)

s_conf_causal_h = support(
    [confidence_causal_role],
    obs_steering_shifts_abstention,
    reason=(
        "The metacognitive confidence hypothesis predicts that steering confidence representations "
        "should proportionally shift abstention rates. If confidence representations in mid-layers "
        "drive abstention, then injecting high- or low-confidence activation patterns should "
        "reduce or increase abstention, respectively. The observed 59.5 pp range of abstention "
        "shift (r = −0.99) directly matches this prediction."
    ),
    prior=0.90,
)

s_policy_alt = support(
    [alt_steering_through_policy],
    obs_steering_shifts_abstention,
    reason=(
        "If steering primarily alters the decision policy (threshold/temperature), a similar "
        "pattern of abstention shift could be observed without the steering effect being mediated "
        "by confidence redistribution. The policy shift mediator M2 does contribute 26.2%, "
        "showing this pathway exists, but it accounts for a minority of the effect."
    ),
    prior=0.30,
)

abduction_causal = abduction(
    s_conf_causal_h,
    s_policy_alt,
    comp_mechanism,
    reason=(
        "Both confidence redistribution and policy change are candidate mechanisms through which "
        "activation steering could reduce abstention (@obs_steering_shifts_abstention). "
        "The parallel mediation analysis [@VanderWeele2015] decomposes the total steering effect "
        "into these two pathways, discriminating between them quantitatively."
    ),
    background=[mediation_setup, two_stage_framework],
)

strat_causal_conclusion = support(
    [mediation_confidence_redistribution, mediation_difficulty_robust, steering_effect_on_abstention],
    confidence_causal_role,
    reason=(
        "Activation steering directly manipulates Stage 1 confidence representations "
        "(@steering_effect_on_abstention, @steering_effect_on_confidence). "
        "The mediation analysis shows confidence redistribution is the dominant mechanism "
        "(@mediation_confidence_redistribution) and this result is robust when controlling for "
        "item difficulty (@mediation_difficulty_robust). "
        "Together, these establish a causal chain: steering → confidence redistribution → "
        "reduced abstention, consistent with the two-stage framework [@FlemingDaw2017; @KepecsMainen2012]."
    ),
    prior=0.90,
)

# ── Connect orphaned mediation sub-results to main mediation claim ────────────

strat_total_mediation_support = support(
    [mediation_total_effect, mediation_policy_shift, mediation_combined_coverage],
    mediation_confidence_redistribution,
    reason=(
        "The confidence redistribution result (@mediation_confidence_redistribution) is supported "
        "by the overall mediation context: total steering effect c = −0.824 (@mediation_total_effect), "
        "confirming that confidence redistribution's 67.1% contribution is of the actual total effect. "
        "Policy shift (M2) contributes 26.2% (@mediation_policy_shift), leaving a clear majority "
        "for M1. Combined mediation 93.3% (@mediation_combined_coverage) shows both mediators "
        "explain virtually the entire effect, ruling out major unmeasured pathways."
    ),
    prior=0.90,
)

strat_steering_confidence_link = support(
    [steering_effect_on_confidence, steering_accuracy_tradeoff],
    steering_effect_on_abstention,
    reason=(
        "The large abstention shift (66.5% → 7.0%) is mechanistically accompanied by "
        "underlying confidence shifts (@steering_effect_on_confidence): high-confidence steering "
        "increases max real confidence and decreases abstention confidence (r = −0.89, p < 0.001). "
        "The mild accuracy-coverage trade-off (@steering_accuracy_tradeoff) — 59.2% to 53.7% "
        "accuracy as coverage expands from 33.5% to 93% — is consistent with increased answering "
        "driven by boosted confidence rather than improved reasoning."
    ),
    prior=0.88,
)
