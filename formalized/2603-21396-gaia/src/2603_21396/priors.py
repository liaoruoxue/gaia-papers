"""
Priors for 2603-21396: Mechanisms of Introspective Awareness

Rationale:
- All experimental claims come from peer-reviewed work with reported quantitative results,
  reproducibility statements, and public code (github.com/safety-research/introspection-mechanisms).
- Behavioral observation claims (direct metrics from model runs) receive high priors (0.85-0.95):
  these are reproducible measurements with reported 95% CIs.
- Mechanistic/interpretive claims receive moderate priors (0.75-0.85): they involve
  transcoder-based analysis which requires Gemma Scope 2 artifacts and is harder to independently
  verify, though the methodology is clearly stated.
- Claims relying on external replications receive slightly lower priors (0.8) as those are
  not fully within the paper's experimental control.
"""

from . import (
    # Section 3: behavioral robustness
    abliteration_increases_detection,
    attention_heads_not_critical,
    base_model_no_discrimination,
    bidirectional_steering_result,
    dpo_contrastive_structure_key,
    dpo_enables_introspection,
    no_pretext_claim,
    persona_robustness_result,
    prompt_robustness_result,
    # Section 4: linear/nonlinear
    delta_pcs_result,
    pca_geometry_result,
    projection_swap_result,
    refusal_direction_not_mean_diff,
    transcoder_features_r2,
    # Section 5: mechanisms
    circuit_hierarchy,
    detection_peaks_midlayer,
    evidence_carrier_causal_distributed,
    evidence_carriers_identified,
    gate_causal_necessity,
    gate_features_identified,
    gate_inverted_v_posttraining,
    mlp_l45_causal_result,
    positive_attribution_features_no_effect,
    steering_attribution_validation,
    # Section 6: underelicitation
    bias_vector_mechanism,
    bias_vector_performance,
    bias_vector_reporting_style,
    lora_finetuning_replication,
)

PRIORS = {
    # ── Section 3: Behavioral robustness ───────────────────────────────────
    base_model_no_discrimination: (
        0.95,
        "Direct numeric measurement from model run; matched TPR (~40%) and FPR (42.3%) clearly show no discrimination",
    ),
    abliteration_increases_detection: (
        0.93,
        "Quantitative measurement with reported 95% CIs following the Arditi et al. abliteration protocol; 10.8% -> 63.8% TPR",
    ),
    dpo_enables_introspection: (
        0.92,
        "Replicated across OLMo-3.1-32B checkpoints and confirmed with LoRA experiments on two model families",
    ),
    dpo_contrastive_structure_key: (
        0.90,
        "Extensive LoRA ablation table (Table 3) with 95% CI for 11 conditions; contrastive vs. non-contrastive contrast is clear",
    ),
    prompt_robustness_result: (
        0.90,
        "7 prompt variants tested on 2 models; consistent TPR/FPR results despite some variation across framing",
    ),
    no_pretext_claim: (
        0.88,
        "Specific variants designed to remove confabulation incentives (anti-reward, alternative path) maintain 0% FPR",
    ),
    persona_robustness_result: (
        0.88,
        "6 dialogue format variants tested on Gemma3-27B; FPR remains 0% across non-standard role variants",
    ),
    # ── Section 4: Linear vs. nonlinear ────────────────────────────────────
    projection_swap_result: (
        0.90,
        "Swap experiment on 500 concept vectors with clear numeric results for both projection and residual directions",
    ),
    bidirectional_steering_result: (
        0.92,
        "Large-sample test on 2000 pairs; 23.3% vs 3.2% bidirectional detection rate is a clear quantitative signal",
    ),
    pca_geometry_result: (
        0.90,
        "PCA and correlation are standard computations on 500 concept vectors; cosine similarity and Spearman rho are direct calculations",
    ),
    delta_pcs_result: (
        0.85,
        "Three delta-PCs each independently trigger detection; semantic labels from logit lens and steering validated",
    ),
    transcoder_features_r2: (
        0.92,
        "30-fold cross-validated R^2; consistent with AUC results; transcoder features (0.624/0.898) clearly outperform linear baselines",
    ),
    refusal_direction_not_mean_diff: (
        0.93,
        "Direct geometric calculation; cosine similarity = -0.09 between d_delta_mu and refusal direction is near-orthogonal",
    ),
    # ── Section 5: Mechanistic analysis ────────────────────────────────────
    detection_peaks_midlayer: (
        0.88,
        "Layer sweep across all 62 layers; peaks are visually and numerically clear from Figure 9 for both detection and identification",
    ),
    attention_heads_not_critical: (
        0.87,
        "Mean accuracy change -0.1% +/- 0.3% across 50 tested heads; attention layer ablation also produces minimal effects",
    ),
    mlp_l45_causal_result: (
        0.90,
        "L45 MLP shows unique causal profile (necessary + partially sufficient) vs all other layers at two injection layers",
    ),
    gate_features_identified: (
        0.85,
        "Gate selection criteria (top-200 by direct logit attribution) well-defined; inverted-V pattern for L45 F9959 validated",
    ),
    gate_causal_necessity: (
        0.90,
        "Clear progressive ablation curves: 39.5% -> 10.1% detection from ablating <200 gate features; partial patching sufficiency shown",
    ),
    positive_attribution_features_no_effect: (
        0.87,
        "Ablation and patching of top-200 positive attribution features shows near-zero effect; sharp asymmetry vs. gate features is diagnostic",
    ),
    evidence_carriers_identified: (
        0.83,
        "Four-criterion selection procedure well-defined; mix of concept-specific and generic carriers is interpretable",
    ),
    evidence_carrier_causal_distributed: (
        0.85,
        "441k feature ablation curve gradually declining (38.6% -> 13.8%) vs. gate ablation's sharp decline confirms distributed representation",
    ),
    circuit_hierarchy: (
        0.85,
        "Layer histograms show carriers peaking at L38 and gates at L45-61; ablation of carriers doubles gate activation (~1700 -> ~3800)",
    ),
    gate_inverted_v_posttraining: (
        0.85,
        "Inverted-V pattern clearly present in instruct and abliterated models but substantially weaker in base model",
    ),
    steering_attribution_validation: (
        0.80,
        "Steering attribution is a novel analysis tool in this paper; findings are consistent with ablation results but harder to independently verify",
    ),
    # ── Section 6: Underelicitation ────────────────────────────────────────
    bias_vector_performance: (
        0.92,
        "Specific numeric gains (+74.7% detection, +54.7% introspection, 0% FPR) reported on 100 held-out concepts across multiple layers",
    ),
    bias_vector_mechanism: (
        0.82,
        "Steering attribution analysis shows shifted patterns under bias vector; interpretation of amplification vs. creation is reasonable",
    ),
    bias_vector_reporting_style: (
        0.78,
        "Behavioral analysis of bias vector effects; assertive-style interpretation is reasonable but qualitative and harder to verify",
    ),
    lora_finetuning_replication: (
        0.82,
        "External replication by Rivera & Africa (2026); 95.5% detection result cited from contemporaneous work",
    ),
}
