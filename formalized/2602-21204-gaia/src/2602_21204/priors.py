"""Prior assignments for leaf (independent) claims in the TTT-linear attention package."""

from .motivation import memorization_hypothesis
from .s2_background import claim_linear_attention_prior_work, claim_ttt_kv_prior_work
from .s3_empirical_contradictions import (
    obs_inner_loop_paradox,
    obs_gradient_ascent_llm,
    obs_gradient_ascent_nvs,
    obs_gradient_ascent_vitttt,
    obs_distributional_asymmetry,
    obs_query_redundancy_nvs,
    obs_query_redundancy_vitttt,
)
from .s4_theory import (
    thm_single_step,
    claim_more_steps_mismatch,
    claim_gradient_sign_absorbed,
)
from .s5_simplifications import (
    claim_step1_final_layer_only,
    claim_step2_no_weight_norm,
    claim_step3_single_linear,
    claim_step4_no_per_token_lr,
    claim_step5_no_momentum,
    claim_step6_standard_linear_attn,
    claim_variant2_parallel_speedup,
    claim_standard_la_speedup,
    claim_training_speedup,
)
from .s6_discussion import (
    claim_linear_layer_limitation,
    claim_bidirectional_connection_open,
)

PRIORS = {
    # ---- Background claims ----
    memorization_hypothesis: (
        0.7,
        "The memorization interpretation was the prevailing view before this paper, "
        "adopted by multiple prior works (Zhang et al. 2025, Han et al. 2025, Behrouz 2024). "
        "It is initially plausible (0.7) given the design intent of the KV binding mechanism.",
    ),
    claim_ttt_kv_prior_work: (
        0.95,
        "Prior TTT work universally adopted the memorization interpretation — this is "
        "a factual statement about published research and is well-documented.",
    ),
    claim_linear_attention_prior_work: (
        0.95,
        "Linear attention (Katharopoulos 2020) and its variants (Mamba, RWKV) are "
        "well-established methods in the literature. High prior as factual background.",
    ),

    # ---- Empirical observations (direct experimental measurements) ----
    obs_inner_loop_paradox: (
        0.9,
        "Empirically measured on the 760M LaCT-LLM model. The inner-loop loss vs. perplexity "
        "tradeoff is a direct experimental observation on a large model with clear results.",
    ),
    obs_gradient_ascent_llm: (
        0.88,
        "Direct experimental result on 760M LaCT-LLM. Gradient ascent comparability is "
        "surprising but clearly measured; slight uncertainty about whether effect is robust.",
    ),
    obs_gradient_ascent_nvs: (
        0.92,
        "Direct measurement: 25.85 vs 25.94 dB PSNR on RealEstate10K. Numerical precision "
        "makes this high confidence; 0.09 dB difference is within noise for NVS tasks.",
    ),
    obs_gradient_ascent_vitttt: (
        0.92,
        "Direct measurement: 79.61% vs 79.34% on ImageNet-1K. Slight improvement with "
        "gradient ascent, clearly measured on standard benchmark.",
    ),
    obs_distributional_asymmetry: (
        0.85,
        "t-SNE visualization is qualitative rather than quantitative. The observation of "
        "distributional mismatch is clear from the figure, but t-SNE projections can "
        "distort distances in high dimensions, reducing confidence slightly.",
    ),
    obs_query_redundancy_nvs: (
        0.9,
        "Direct measurement: negligible degradation when substituting keys for queries "
        "in LaCT-NVS. Clear experimental result on RealEstate10K.",
    ),
    obs_query_redundancy_vitttt: (
        0.92,
        "Direct measurement: 79.18% vs 79.34% (0.16 pp degradation) on ImageNet-1K. "
        "Precise numerical result on standard benchmark.",
    ),

    # ---- Theoretical results ----
    thm_single_step: (
        0.95,
        "Theorem 5.1 is a mathematical proof by direct algebraic substitution, given "
        "the linear bias-free assumption. The derivation is straightforward and the "
        "result follows necessarily from the definitions. High prior, but not 0.999 "
        "because the paper may omit edge cases or implicit assumptions.",
    ),
    claim_more_steps_mismatch: (
        0.82,
        "The train-test kernel mismatch explanation is theoretically well-motivated "
        "under the linear attention view. However, it is a mechanistic interpretation "
        "rather than a directly proven fact — requires that training and inference use "
        "different numbers of inner-loop steps.",
    ),
    claim_gradient_sign_absorbed: (
        0.78,
        "The gradient sign absorption into learned projections is plausible under the "
        "linear attention view, but relies on the model actually learning to compensate "
        "during training. This is an explanatory claim, not a theorem, reducing confidence.",
    ),

    # ---- Ablation step results (direct measurements) ----
    claim_step1_final_layer_only: (
        0.92,
        "Directly measured in Table 2: perplexity 15.93, PSNR 25.97, accuracy 79.63%. "
        "Best-performing variant — this is a clear experimental result.",
    ),
    claim_step2_no_weight_norm: (
        0.92,
        "Table 2 result: perplexity 16.31, PSNR 25.93, accuracy 79.63%. "
        "Direct ablation measurement.",
    ),
    claim_step3_single_linear: (
        0.92,
        "Table 2 result: perplexity 16.23, PSNR 25.71, accuracy 79.39%. "
        "Direct ablation measurement.",
    ),
    claim_step4_no_per_token_lr: (
        0.92,
        "Table 2 result: perplexity 16.12, PSNR 25.70, accuracy 79.39%. "
        "Direct ablation measurement.",
    ),
    claim_step5_no_momentum: (
        0.92,
        "Table 2 result: perplexity 15.97, PSNR 25.70, accuracy 79.39%. "
        "Direct ablation measurement.",
    ),
    claim_step6_standard_linear_attn: (
        0.92,
        "Table 2 result: perplexity 16.80, PSNR 25.73, accuracy 79.54%. "
        "Final ablation step — marginal degradation is directly measured.",
    ),

    # ---- Efficiency results ----
    claim_variant2_parallel_speedup: (
        0.88,
        "Throughput measurement: 30.18M vs 4.30M tokens/s (7.0× speedup). "
        "Hardware benchmarks on a single hardware configuration; may vary across setups.",
    ),
    claim_standard_la_speedup: (
        0.88,
        "Throughput measurement: 124.6M tokens/s (29× speedup). Direct measurement, "
        "but represents an upper bound for a specific hardware configuration.",
    ),
    claim_training_speedup: (
        0.87,
        "End-to-end training speedup of 1.19× measured on the LaCT-LLM setup. "
        "Moderate confidence as end-to-end speedup depends on many system factors.",
    ),

    # ---- Limitations ----
    claim_linear_layer_limitation: (
        0.95,
        "The limitation (nonlinear final layers not covered) is a direct consequence "
        "of the theorem assumptions, making it a high-confidence factual statement.",
    ),
    claim_bidirectional_connection_open: (
        0.9,
        "The bidirectional connection as an open question is a factual statement about "
        "the paper's scope — clearly the paper only shows TTT→linear attention, not the reverse.",
    ),
}
