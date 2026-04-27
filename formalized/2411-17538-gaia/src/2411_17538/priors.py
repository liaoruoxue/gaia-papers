"""Priors for independent (leaf) claims in the 2411-17538 package.

All other (derived) claims have their belief computed by Belief Propagation
from these leaves and from the in-DSL ``prior=`` warrants on strategies.

Prior-assignment rationale:

* **Direct empirical observations** quoted from a peer-reviewed table or
  figure of the paper get high priors (0.90+). The data themselves are not
  in dispute (we can read them off the tables); the question of whether
  they support the higher-level conclusions is what BP propagates.
* **Mathematical facts** about ZCA whitening (eigenvalue amplification,
  Kessy's correlation property) get high priors (0.92+) because they are
  derivable.
* **Hypotheses and their alternatives in abductions** get the priors
  appropriate to their explanatory power for the specific observation
  (NOT to their general truth).
* **Predictions** are conditional propositions ("if H, then Obs would look
  like X"); they are read off the experimental data once H is fixed, so
  they are essentially logical consequences and get high priors when the
  data clearly match the prediction.
* **Naive expectations** that the paper sets up only to refute get low
  priors (0.10) -- they are explicitly contradicted by observation.
"""

from . import (
    # Mathematical facts about ZCA / Soft-ZCA
    zca_correlation_property,
    zca_amplifies_noise_at_small_eigenvalues,
    # Direct empirical observations (Table 2 / Table 3 / text quotes)
    table2_nonwhitened,
    obs_codebert_low_mrr_low_iso,
    obs_ft_codebert_higher_mrr_low_iso,
    obs_codet5plus_high_mrr_high_iso,
    obs_codellama_low_mrr,
    obs_standard_zca_helps_base_models,
    obs_standard_zca_hurts_ft_and_codet5,
    obs_optimal_epsilon_base,
    obs_optimal_epsilon_ft,
    obs_separate_mostly_better,
    # Per-(model, dataset) Soft-ZCA observations (used inside induction)
    obs_softzca_positive_delta_mrr,
    obs_codellama_largest_gain,
    obs_ft_codebert_modest_gain,
    obs_low_resource_r_helped,
    obs_softzca_pattern,
    obs_codet5plus_dim256_better,
    # Predictions (in abductions)
    pred_softzca_isotropy,
    pred_softzca_dim_artifact,
    pred_lower_dim_helps,
    pred_layer_special,
    # Hypotheses / alternatives (in abductions)
    hypothesis_isotropy_mediates,
    alt_dimensionality_artifact,
    hypothesis_lower_dim_higher_iso,
    alt_downprojection_layer_special,
    # Naive expectation (refuted by observation in s4)
    naive_zca_helps_all,
)


PRIORS: dict = {
    # ----- Mathematical / methodological facts -----
    zca_correlation_property: (
        0.95,
        "Established theorem from Kessy, Lewin, Strimmer (2018, [@Kessy2018]) "
        "showing ZCA uniquely maximises correlation between whitened and "
        "original embeddings -- a peer-reviewed mathematical result.",
    ),
    zca_amplifies_noise_at_small_eigenvalues: (
        0.97,
        "Direct algebraic consequence of the form $\\Sigma^{-1/2} = U "
        "\\Lambda^{-1/2} U^{\\top}$: as $\\lambda_i \\to 0$, "
        "$\\lambda_i^{-1/2} \\to \\infty$. Essentially deterministic.",
    ),

    # ----- Direct experimental observations -----
    table2_nonwhitened: (
        0.95,
        "Reproduces Table 2 of the paper verbatim. The numbers themselves "
        "are not in dispute; small uncertainty allowed for transcription.",
    ),
    obs_codebert_low_mrr_low_iso: (
        0.95,
        "Direct read-off of CodeBERT row of Table 2: MRR 0.000-0.011 and "
        "IsoScores below 0.022 in every cell.",
    ),
    obs_ft_codebert_higher_mrr_low_iso: (
        0.95,
        "Direct read-off of FT CodeBERT vs base CodeBERT in Table 2; the "
        "average IsoScore delta of 0.073 is also explicitly stated in the "
        "paper text.",
    ),
    obs_codet5plus_high_mrr_high_iso: (
        0.95,
        "Direct read-off of CodeT5+ row of Table 2.",
    ),
    obs_codellama_low_mrr: (
        0.95,
        "Direct read-off of Code Llama row of Table 2.",
    ),
    obs_standard_zca_helps_base_models: (
        0.85,
        "Stated in the paper text. Not directly tabulated as a per-cell "
        "number (Table 3 reports best-epsilon results, not the "
        "epsilon=0 effect alone), so the prior is slightly lower than "
        "for fully tabulated quantities.",
    ),
    obs_standard_zca_hurts_ft_and_codet5: (
        0.85,
        "Stated in the paper text and partially reflected in Table 5 "
        "(combined-vs-separate ablation, both at epsilon=0). Same "
        "uncertainty as @obs_standard_zca_helps_base_models.",
    ),
    obs_optimal_epsilon_base: (
        0.9,
        "Stated explicitly in the paper text and visualised in Figure 1. "
        "Slightly less than direct table reads because the 'best epsilon' "
        "language uses a discrete grid scan.",
    ),
    obs_optimal_epsilon_ft: (
        0.9,
        "Stated explicitly in the paper text and consistent with Table 3 "
        "(FT CodeBERT IsoScores all >= 0.99).",
    ),
    obs_separate_mostly_better: (
        0.92,
        "Direct read-off of Table 5: 4/7 base CodeBERT cells and 6/6 FT "
        "CodeBERT cells favour separate whitening; exceptions are small "
        "and confined to low-MRR base-model cells.",
    ),

    # ----- Per-(model, dataset) Soft-ZCA observations -----
    # NOTE: these are the predictions inside the induction over the
    # @finding_softzca_improves_code_search law. They appear as derived
    # claims in the graph, but in fact they are *also* directly read off
    # Table 3 of the paper -- their empirical grounding must be set
    # explicitly so the induction's backward message can boost the law.
    # See gaia formalization skill, "Common Mistakes" entry on observation
    # claims classified as derived.
    obs_softzca_positive_delta_mrr: (
        0.92,
        "Directly read off Table 3: $\\Delta$MRR > 0 in every base-CodeBERT "
        "cell on every CodeSearchNet language (range +0.102 to +0.250). "
        "The observation is empirically anchored independently of any "
        "synthesis claim.",
    ),
    obs_codellama_largest_gain: (
        0.93,
        "Directly read off Table 3: Code Llama $\\Delta$MRR ranges +0.227 "
        "(PHP) to +0.476 (Ruby), the largest gains in the table.",
    ),
    obs_ft_codebert_modest_gain: (
        0.93,
        "Directly read off Table 3: FT CodeBERT $\\Delta$MRR ranges +0.042 "
        "(Go) to +0.075 (Ruby), with IsoScores >= 0.99 in every cell.",
    ),
    obs_low_resource_r_helped: (
        0.92,
        "Directly read off Table 3 (R row): $\\Delta$MRR = +0.077 / +0.035 "
        "/ +0.337 for CodeBERT / CodeT5+ / Code Llama on the held-out R "
        "dataset.",
    ),
    obs_softzca_pattern: (
        0.92,
        "Joint summary of Tables 2 and 3, directly read from the paper's "
        "tables. Slight uncertainty allowed for the qualitative "
        "'co-variation' wording (Tables only carry the quantitative "
        "anchor; the qualitative summary requires light interpretation).",
    ),
    obs_codet5plus_dim256_better: (
        0.95,
        "Directly read off Table 4 (CodeT5+ embedding-size ablation): "
        "dim=256 wins on both MRR and IsoScore in every language row.",
    ),

    # ----- Predictions (essentially logical consequences once H is fixed) -----
    pred_softzca_isotropy: (
        0.9,
        "Conditional prediction: if isotropy mediates the effect, MRR "
        "gains should track IsoScore gains. Tables 2 and 3 jointly "
        "confirm the cell-by-cell pattern.",
    ),
    pred_softzca_dim_artifact: (
        0.45,
        "Conditional prediction under the dimensionality-only "
        "alternative: gains should scale with embedding dimension. The "
        "data only weakly satisfy this (Code Llama wins, but the "
        "FT-vs-base CodeBERT gap is unexplained), so the prediction "
        "itself is only partially confirmed.",
    ),
    pred_lower_dim_helps: (
        0.92,
        "Conditional prediction (dim=256 wins on every language) is "
        "directly verified by every row of Table 4.",
    ),
    pred_layer_special: (
        0.5,
        "Conditional prediction (roughly constant MRR ratio) is only "
        "loosely confirmed by Table 4: ratios range 1.5x-2x.",
    ),

    # ----- Hypothesis / alternative pairs (abduction priors) -----
    hypothesis_isotropy_mediates: (
        0.65,
        "The paper's central mechanistic claim. Given the strong "
        "cell-by-cell co-variation between $\\Delta$MRR and IsoScore "
        "gain, it is moderately well-supported by direct evidence; not "
        "set higher because no causal experiment isolates isotropy from "
        "covariance-conditioning effects.",
    ),
    alt_dimensionality_artifact: (
        0.3,
        "pi(Alt) reflects explanatory power for the *specific* observed "
        "pattern, not whether dimensionality matters in general. The "
        "alternative cannot account for the FT-vs-base CodeBERT gap (both "
        "dim=768) nor for the low-dim CodeT5+ R-language gain, so its "
        "explanatory power for @obs_softzca_pattern is low.",
    ),
    hypothesis_lower_dim_higher_iso: (
        0.7,
        "A plausible geometric argument (volume/sparsity of "
        "high-dimensional spaces) that is at least consistent with the "
        "Table 4 ablation. Not set higher because the ablation does not "
        "isolate dim from the trained down-projection layer.",
    ),
    alt_downprojection_layer_special: (
        0.45,
        "pi(Alt) for the trained-layer alternative: it is consistent "
        "with the MRR ranking but less consistent with the simultaneous "
        "IsoScore gain, so its explanatory power for "
        "@obs_codet5plus_dim256_better is moderate.",
    ),

    # ----- Naive expectation (refuted by observation) -----
    naive_zca_helps_all: (
        0.1,
        "The naive expectation explicitly refuted by Table 5 / paper "
        "text: standard ZCA decreases MRR for FT CodeBERT and CodeT5+ on "
        "most datasets. Set very low because the contradiction operator "
        "with @obs_standard_zca_hurts_ft_and_codet5 reflects "
        "well-documented experimental refutation.",
    ),
}
