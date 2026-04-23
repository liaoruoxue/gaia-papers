"""Section 4: Linear and Nonlinear Contributors to Detection"""

from gaia.lang import (
    claim, setting,
    support, deduction, infer, abduction,
)

from .motivation import (
    concept_injection_setup,
    gemma3_setup,
    concept_partition_setup,
    claim_not_single_linear,
    steering_linear_rep,
)

# =============================================================================
# Settings
# =============================================================================

mean_diff_direction_def = setting(
    "The mean-difference direction d_delta_mu is the difference in mean activations between "
    "success and failure concept vectors at the injection layer. Each concept vector can be "
    "decomposed as: v_c = (v_c . d_hat_delta_mu) * d_hat_delta_mu + residual, where "
    "d_hat_delta_mu is the unit-normalized mean-difference vector and the residual captures "
    "variance orthogonal to this direction. A ridge regression on concept vectors explains "
    "44.4% of detection variance (R^2 = 0.444).",
    title="Mean-difference direction definition",
)

# =============================================================================
# Section 4.1 – Swap experiments
# =============================================================================

projection_swap_result = claim(
    "Direction swap experiment on 500 concept vectors (Gemma3-27B, L=37): for success "
    "concepts, swapping the projection onto d_delta_mu to failure-like projections reduces "
    "detection rate from 66.1% to 39.0%; swapping residuals also reduces detection to 44.4%. "
    "For failure concepts, both swaps increase detection to similar levels: projection swap "
    "increases from 8.8% to 34.2% and residual swap increases to 32.8%. Results using the "
    "ridge regression direction (dridge) show similar patterns: for success concepts, ridge "
    "projection swap reduces detection from 65.3% to 49.6%, while residual swap reduces it "
    "more strongly (65.3% to 31.6%).",
    title="Direction swap experiment results",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 6",
        "caption": "Fig. 6 | Mean-difference direction (d_delta_mu) swap results. Both projection and residual swaps are effective.",
    },
)

strat_both_components_carry_signal = support(
    [projection_swap_result],
    claim_not_single_linear,
    reason=(
        "The swap experiments show that both the d_delta_mu projection component and the "
        "residual (all variance orthogonal to d_delta_mu) carry detection-relevant signal "
        "of similar magnitude (@projection_swap_result). If detection depended on a single "
        "direction, swapping to failure-like projections should fully flip detection, and "
        "residual swaps should have minimal effect. Instead, residual swaps alone are nearly "
        "as effective as projection swaps, demonstrating the computation is distributed "
        "across at least two orthogonal directions. This evidence directly challenges the "
        "established framework of single-direction linear representations "
        "(@steering_linear_rep) being sufficient for this behavior."
    ),
    prior=0.88,
    background=[mean_diff_direction_def, concept_partition_setup, gemma3_setup,
                steering_linear_rep],
)

# =============================================================================
# Section 4.2 – Bidirectional steering
# =============================================================================

bidirectional_steering_result = claim(
    "Bidirectional steering experiment on 1,000 randomly sampled success-success (S-S) "
    "pairs and 1,000 failure-failure (F-F) pairs: in 23.3% of S-S pairs, both opposite "
    "directions (A-B and B-A) trigger detection, compared to only 3.2% for F-F pairs. "
    "The nonzero rate of bidirectional detection in S-S pairs is inconsistent with a "
    "single linear direction hypothesis, since if detection were governed by one direction, "
    "at most one of A-B or B-A could trigger detection for any pair.",
    title="Bidirectional steering result",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 7",
        "caption": "Fig. 7 | Same-category pair bidirectional steering. S-S pairs (23.3%) show much more bidirectional detection than F-F pairs (3.2%).",
    },
)

strat_bidirectional_nonlinearity = support(
    [bidirectional_steering_result],
    claim_not_single_linear,
    reason=(
        "If detection relied on a single linear direction d, then for any concept pair "
        "(A, B), the projections of A-B and B-A onto d have opposite signs, so at most "
        "one can exceed the detection threshold. The 23.3% bidirectional detection rate "
        "in S-S pairs (@bidirectional_steering_result) directly violates this prediction. "
        "The significantly higher rate in S-S vs F-F pairs suggests the model is attuned "
        "to perturbations along multiple axes (or within subspaces) characteristic of "
        "success concepts, requiring nonlinear computation."
    ),
    prior=0.92,
    background=[concept_partition_setup, gemma3_setup],
)

# =============================================================================
# Section 4.3 – Geometry characterization
# =============================================================================

pca_geometry_result = claim(
    "Principal component analysis (PCA) of 500 L2-normalized concept vectors (L=37, "
    "Gemma3-27B): PC1 explains 18.4% of variance and aligns strongly with d_delta_mu "
    "(cosine similarity = 0.97) but is nearly orthogonal to the refusal direction "
    "(cosine = -0.09). Logit lens on d_delta_mu shows positive loading on tokens "
    "'facts' and 'knowledge', and negative loading on 'confused' and 'ambiguous', "
    "suggesting the mean direction captures 'factual assertiveness' or the distinction "
    "between factual knowledge and uncertain fuzzy content. Projection onto d_delta_mu "
    "correlates with concept verbalizability (Spearman rho = 0.605).",
    title="PCA geometry of concept vectors",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 8a, 8b",
        "caption": "Fig. 8 | Geometry of concept vectors. (a) PCA colored by detection rate. (b) Verbalizability vs. d_delta_mu projection.",
    },
)

delta_pcs_result = claim(
    "Three orthogonal principal components (delta-PCs) extracted from the residual space "
    "of success concept vectors after projecting out d_delta_mu each independently trigger "
    "detection with distinct response profiles and produce bidirectional detection. "
    "The three directions encode distinct semantic contrasts:\n\n"
    "| Direction | Variance explained | Semantic contrast |\n"
    "|-----------|-------------------|-------------------|\n"
    "| delta-PC1 | 19.6% | Casual (-) <-> Formal (+) |\n"
    "| delta-PC2 | 12.0% | Concrete (-) <-> Abstract (+) |\n"
    "| delta-PC3 | 8.4% | Emotions (-) <-> Careers (+) |",
    title="Delta-PC directions and semantic content",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 8c",
        "caption": "Fig. 8c | Detection rate vs. steering strength along delta-PC1-3.",
    },
)

transcoder_features_r2 = claim(
    "Ridge regression to predict per-concept detection rate based on downstream transcoder "
    "features (layers 38-61, Gemma3-27B) achieves R^2 = 0.624 at 4,500 features, "
    "substantially outperforming scalar projection onto d_delta_mu (R^2 = 0.309) and "
    "regression on raw concept vectors (R^2 = 0.444). Binary classification AUC results "
    "show the same ordering: transcoder features 0.898 > concept vectors 0.857 > "
    "d_delta_mu scalar 0.822 > verbalizability 0.696.",
    title="Transcoder features outperform linear projections for detection prediction",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 8d",
        "caption": "Fig. 8d | 30-fold cross-validated R^2 for predicting per-concept detection rates from transcoder features vs. baselines.",
    },
)

refusal_direction_not_mean_diff = claim(
    "The mean-difference direction d_delta_mu between success and failure concepts is nearly "
    "orthogonal to the refusal direction (cosine similarity = -0.09), despite the fact that "
    "refusal ablation increases detection rates. This rules out the hypothesis that successful "
    "detection arises from concept vectors aligning with the refusal direction.",
    title="Mean-difference direction is orthogonal to refusal direction",
    metadata={"source": "artifacts/2603.21396.pdf, Section 4.3"},
)

strat_geometry_nonlinearity = support(
    [pca_geometry_result, delta_pcs_result, transcoder_features_r2,
     refusal_direction_not_mean_diff],
    claim_not_single_linear,
    reason=(
        "The existence of multiple orthogonal detection-relevant directions (delta-PCs, "
        "each independently triggering detection with distinct profiles; @delta_pcs_result) "
        "goes beyond any single linear mechanism. The fact that transcoder features "
        "(nonlinear computation) substantially outperform linear projections in predicting "
        "detection (R^2 0.624 vs 0.309; @transcoder_features_r2) provides further direct "
        "evidence that detection involves higher-dimensional nonlinear computation on top "
        "of the steering vectors. PCA confirming near-orthogonality of d_delta_mu and the "
        "refusal direction (@refusal_direction_not_mean_diff) rules out the most obvious "
        "confound, and the logit lens interpretation of d_delta_mu as 'factual assertiveness' "
        "(@pca_geometry_result) provides semantic grounding."
    ),
    prior=0.9,
    background=[mean_diff_direction_def, gemma3_setup, concept_partition_setup],
)
