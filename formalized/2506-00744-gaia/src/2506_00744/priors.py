"""Priors for independent (leaf) claims in the HQLT package.

Strategy/operator warrant priors are set inline in the DSL via
``prior=`` on each ``support`` / ``deduction`` / ``compare`` /
``contradiction`` call. This file only assigns priors to claims that
are NOT the conclusion of any strategy.
"""

from . import (
    # ---- motivation ----------------------------------------------------------
    claim_qt_precise_recall,
    claim_compatibility_with_efficient_kernels,
    claim_layerwise_hybrid_alt,
    # ---- background ----------------------------------------------------------
    claim_softmax_sharpness,
    claim_qt_storage_grows,
    claim_la_constant_per_step,
    claim_chunkwise_subquadratic,
    claim_deltanet_uses_delta_rule,
    claim_negative_eigvals,
    # ---- methods -------------------------------------------------------------
    claim_delayed_stream_division,
    claim_delayed_stream_state_size,
    claim_delayed_chunk_connection,
    claim_synchronous_no_delay,
    claim_synchronous_arora_connection,
    # ---- experiments: observations -------------------------------------------
    obs_table2_main,
    obs_la_ablation,
    obs_window_ablation_lm,
    obs_mixer_ablation_lm,
    obs_synchronous_la_fails,
    alt_random_failure,
    obs_table3_expressivity,
    obs_table4_retrieval,
    obs_rl_results,
    # ---- design-comparison hypotheses ----------------------------------------
    alt_delayed_chunk_best,
    alt_delayed_stream_best,
)


PRIORS: dict = {
    # =====================================================================
    # Motivation: literature-backed properties of QT and LT
    # =====================================================================
    claim_qt_precise_recall: (
        0.92,
        "Well-established empirical and analytical observation in the "
        "transformer literature: softmax sharpness underlies precise key-value "
        "lookup. Slight reservation because 'precise' is task-dependent.",
    ),
    claim_compatibility_with_efficient_kernels: (
        0.9,
        "Both branches are structurally identical to existing kernels; the "
        "claim follows from architectural inspection but minor implementation "
        "details may differ.",
    ),
    claim_layerwise_hybrid_alt: (
        0.95,
        "Description of an existing class of hybrid models (Griffin, Samba, "
        "xLSTM); essentially a literature observation.",
    ),
    # =====================================================================
    # Background (S2)
    # =====================================================================
    claim_softmax_sharpness: (
        0.92,
        "Well-known mechanistic property of softmax; widely demonstrated.",
    ),
    claim_qt_storage_grows: (
        0.97,
        "Direct algorithmic consequence of the per-step append rule; near-certain.",
    ),
    claim_la_constant_per_step: (
        0.97,
        "Direct algorithmic consequence of the rank-1 update on a fixed-size "
        "matrix state; near-certain.",
    ),
    claim_chunkwise_subquadratic: (
        0.9,
        "Well-established by FlashLinearAttention and follow-up work; minor "
        "uncertainty over chunk-size constants.",
    ),
    claim_deltanet_uses_delta_rule: (
        0.95,
        "Direct algebraic identification of the DeltaNet update with the classic "
        "delta rule; matches the original Schlag et al. derivation.",
    ),
    claim_negative_eigvals: (
        0.85,
        "Identified analytically and confirmed empirically by Grazzi et al.; "
        "small residual uncertainty about the precise role of negative "
        "eigenvalues in deeper or non-standard variants.",
    ),
    # =====================================================================
    # Methods (S3): structural facts following from the equations
    # =====================================================================
    claim_delayed_stream_division: (
        0.95,
        "Direct consequence of the Eq. 10-13 update structure; essentially a "
        "definition rephrased in operational terms.",
    ),
    claim_delayed_stream_state_size: (
        0.95,
        "Counted directly from the matrix dimensions in @def_hqlt_state.",
    ),
    claim_delayed_chunk_connection: (
        0.85,
        "Follows from comparing the equations side by side with Munkhdalai et "
        "al.'s Infini-attention; a few low-level differences (gating, "
        "normalisation) remain.",
    ),
    claim_synchronous_no_delay: (
        0.97,
        "Definitional: in the Synchronous variant, FW-memory is fed (k_t, v_t) "
        "in the same step.",
    ),
    claim_synchronous_arora_connection: (
        0.85,
        "Architectural similarity to Arora et al. is straightforward; the "
        "claim of generalisation to a stronger FWP is supported by ablations "
        "but rests on extrapolating their setup.",
    ),
    # =====================================================================
    # Experiments: observations are well-anchored empirical facts
    # =====================================================================
    obs_table2_main: (
        0.95,
        "Reported numerical table from a 15B-token training run with described "
        "hyper-parameters; reproducible from open code/config.",
    ),
    obs_la_ablation: (
        0.95,
        "Reported ablation row in Table 2; large effect size makes the result "
        "robust to minor noise.",
    ),
    obs_window_ablation_lm: (
        0.95,
        "Direct reading of Table 2 ablation rows.",
    ),
    obs_mixer_ablation_lm: (
        0.92,
        "Direct numerical reading of mixer ablation rows; differences are "
        "small but consistent.",
    ),
    obs_synchronous_la_fails: (
        0.92,
        "Direct ablation row; consistent with the known weakness of vanilla LA "
        "on state-tracking tasks.",
    ),
    obs_table3_expressivity: (
        0.95,
        "Reported expressivity table with very large effect sizes (100% vs 3%); "
        "standard tasks reproducible from prior work [@Grazzi2025].",
    ),
    alt_random_failure: (
        0.15,
        "pi(Alt) for the abduction in s4_experiments. The 'random failure' "
        "alternative struggles to explain the systematic, design-correlated "
        "pattern of failures in Table 3 (both delayed variants fail on both "
        "tasks while Synchronous and Synchronous+vanilla-LA fail/succeed in "
        "exactly the predicted ways). A low explanatory-power prior reflects "
        "this poor fit to the specific observation, not 'training noise never "
        "happens.'",
    ),
    obs_table4_retrieval: (
        0.95,
        "Reported retrieval table; numerical readings are objective.",
    ),
    obs_rl_results: (
        0.85,
        "Reported result with 3 seeds; the paper notes high inter-seed "
        "variance, so the qualitative claim ('largely closes the gap') is "
        "reliable but precise success-rate numbers are noisier.",
    ),
    # =====================================================================
    # Design-comparison hypotheses (BP must pick a winner via contradictions)
    # =====================================================================
    alt_delayed_chunk_best: (
        0.15,
        "pi(Alt) reflects explanatory power: Delayed-Chunk is the worst "
        "performer on expressivity and not best on any reported axis. Cannot "
        "alone explain the paper's evidence pattern.",
    ),
    alt_delayed_stream_best: (
        0.25,
        "pi(Alt) reflects explanatory power: Delayed-Stream wins one row "
        "(1.3B 6-task average 54.5) but fails completely on expressivity. It "
        "explains a small slice of the evidence and contradicts a larger one.",
    ),
}
