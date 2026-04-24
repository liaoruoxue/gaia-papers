"""Section 2: Preliminaries — Information-Theoretic Framework and MI Estimator"""

from gaia.lang import claim, setting, support, deduction
from .motivation import (
    noisy_channel_framing,
    compressor_predictor_pattern,
    mi_as_proxy_proposal,
)

# ── Settings: Mathematical Definitions ────────────────────────────────────────

mi_definition = setting(
    "Mutual information I(X; Z) between two random variables X and Z is defined via the "
    "KL divergence: I(X; Z) = D_KL(p(x,z) || p(x)p(z)) = E_{x,z~p(x,z)}[log p(z|x)/p(z)]. "
    "Larger I(X; Z) indicates that Z retains more information about X.",
    title="Mutual information definition",
)

mc_estimator_def = setting(
    "The Monte Carlo mutual information estimator for LM compressions is defined as: "
    "I_hat(X; Z) = (1/NM) sum_{i=1}^{N} sum_{j=1}^{M} [log p(z_ij|x_i) - log((1/N) sum_{l=1}^{N} p(z_ij|x_l))], "
    "where z_ij ~ p(z|x_i) for i=1..N, j=1..M and x_l ~ p(x) for l=1..N. "
    "N is the number of contexts sampled from the data distribution; M is the number of "
    "compressions generated per context. This estimator bypasses the intractable marginal p(z).",
    title="Monte Carlo MI estimator definition",
)

rate_distortion_def = setting(
    "Rate-distortion theory formalizes the trade-off between rate R (information conveyed per token, "
    "measured in bits of mutual information per output token) and distortion D (prediction error). "
    "Rate R = I(X; Z | Q) / L, where L is the number of output tokens. "
    "Distortion D = 1 - ACC(Z), where ACC(Z) is downstream task accuracy. "
    "The canonical Gaussian rate-distortion function is R(D) = (1/2) log(sigma^2(X)/D) for 0 <= D <= sigma^2.",
    title="Rate-distortion theory setup",
)

bit_efficiency_def = setting(
    "Bit efficiency (also called information rate) is defined as R = I(X; Z | Q) / L, "
    "where I(X; Z | Q) is the mutual information between context X and compression Z "
    "conditioned on query Q, and L is the number of output tokens in the compression Z. "
    "Bit efficiency measures how many bits of task-relevant information are conveyed per output token.",
    title="Bit efficiency (information rate) definition",
)

proxy_model_setting = setting(
    "Because LMs at 1-3B scale can assign high likelihoods to nonsensical token sequences "
    "(indicating miscalibration), the MI estimator uses a proxy model at the 7-8B scale from a "
    "different model family to evaluate log probabilities p(z|x). The proxy model is not the "
    "compressor itself — it serves only as a probability evaluator.",
    title="Proxy model for MI estimation",
)

flops_per_generation_def = setting(
    "FLOPs per token for a dense transformer LM is approximated as: "
    "C_dense ~ 2 * N_params + 2 * n_layer * n_ctx * d_attn, "
    "where N_params is the number of model parameters, n_ctx is the number of input context tokens, "
    "n_layer is the number of layers, and d_attn is the attention head dimension. "
    "FLOPs-per-generation is the product of FLOPs-per-token and the number of generated tokens.",
    title="FLOPs-per-generation compute cost definition",
)

# ── Experimental Setup Settings ────────────────────────────────────────────────

experimental_datasets = setting(
    "Five datasets are used for empirical evaluation: "
    "(a) LongHealth — synthetic clinical reports with 20 patient histories, treated as QA [@Adams2024]; "
    "(b) FinanceBench — 150 10-K filings paired with QA tasks [@Islam2023]; "
    "(c) QASPER — 5,049 scientific paper QA pairs [@Dasigi2021]; "
    "(d) WildChat — large-scale LM conversation dataset [@Zhao2024]; "
    "(e) FineWeb — processed web pages from CommonCrawl [@Penedo2024]. "
    "Accuracy is measured by a GPT-4o-mini judge for LongHealth, FinanceBench, and QASPER; "
    "perplexity under Llama-3.1-8B is used for WildChat and FineWeb.",
    title="Five evaluation datasets",
)

compressor_model_families = setting(
    "Compressor models are drawn from three open-source LM families: "
    "Llama-3 [@Grattafiori2024], Qwen-2.5 [@Qwen2025], and Gemma-3 [@GemmaTeam2025]. "
    "All are GPT-style (non-reasoning) autoregressive architectures. "
    "Additional preliminary experiments use Qwen-3 family reasoning and mixture-of-experts (MoE) models. "
    "Compressor sizes range from 0.5B to 14B parameters.",
    title="Compressor model families and sizes",
)

predictor_models = setting(
    "Predictor models are larger frontier or open-source LMs: GPT-4o [@He2025] and "
    "Llama-3 (1B, 8B, 70B, 405B) and Qwen-2.5 (72B) families. "
    "Predictors receive the compressor's summary Z and a query Q to produce the final answer Y.",
    title="Predictor model set",
)

# ── Claims: Properties of the MI Estimator ────────────────────────────────────

mc_estimator_upper_bound = claim(
    "The Monte Carlo mutual information estimator I_hat(X; Z) is upper bounded by log(N), "
    "where N is the number of contexts sampled. The bound is tight when "
    "p(z_ij|x_i) >> p(z_ij|x_l) for all l != i (i.e., compressions are highly specific to their source contexts).",
    title="MI estimator upper bound: log(N)",
    metadata={"source_section": "Section 2.2, Appendix B.2"},
)

mi_estimator_practical = claim(
    "The Monte Carlo MI estimator I_hat(X; Z) is practical for LM systems because it requires only "
    "log probabilities p(z|x) from an inference server — no access to the full vocabulary distribution "
    "or training of an auxiliary model is needed. This allows use of accelerated inference engines "
    "such as SGLang [@Zheng2024].",
    title="MI estimator practical feasibility",
    metadata={"source_section": "Section 2.2"},
)

mi_estimator_clipping = claim(
    "The conditional MI estimator I_hat(X; Z | Q) can produce small negative values due to "
    "finite-sample Monte Carlo variance; these are corrected by clipping MI to zero. "
    "With S=5 random seeds per experiment, variance is controlled across all reported results.",
    title="MI estimator clipping and seed control",
    metadata={"source_section": "Section 2.2"},
)

proxy_consistency = claim(
    "The mutual information scaling trends produced by the Monte Carlo estimator remain consistent "
    "across different choices of proxy model (Appendix E.1.4) and also when no proxy model is used "
    "(evaluating log probabilities under the compressor itself, as shown for Qwen-3 in Appendix E.1.5).",
    title="MI scaling trends robust to proxy model choice",
    metadata={"source_section": "Section 3.2, Appendix E.1.4, E.1.5"},
)

gaussian_rd_qualitative = claim(
    "The Gaussian rate-distortion function D(R) = C * exp(-b*R) + D_0 (with offset D_0 for "
    "non-zero distortion floor, and fitted parameters C, b) captures the qualitative shape of "
    "observed rate-distortion curves in LM compression-prediction systems, even though LM data "
    "distributions are not Gaussian. It serves as a simplified model for comparing different predictors.",
    title="Gaussian R-D function as qualitative model",
    metadata={"source_section": "Appendix B.3"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_upper_bound = support(
    [mi_estimator_practical],
    mc_estimator_upper_bound,
    background=[mi_definition, noisy_channel_framing, mc_estimator_def],
    reason=(
        "Starting from the KL divergence representation of MI (@mi_definition) and treating "
        "the compressor as a noisy channel (@noisy_channel_framing), the MC estimator "
        "(@mc_estimator_def) is derived by replacing the intractable marginal p(z) with a "
        "sample average. From this definition, for any z_ij and x_l: "
        "sum_l p(z_ij|x_l) >= p(z_ij|x_i), so each estimator term <= log N. "
        "Averaging yields I_hat(X;Z) <= log N (proved in Appendix B.2). "
        "The estimator is practical via log probabilities (@mi_estimator_practical)."
    ),
    prior=0.97,
)

strat_proxy_robustness = support(
    [mi_estimator_practical, mi_estimator_clipping],
    proxy_consistency,
    background=[proxy_model_setting],
    reason=(
        "If the MI estimator works via log probabilities (@mi_estimator_practical) and uses "
        "clipping to handle finite-sample variance (@mi_estimator_clipping), and proxy "
        "models are needed only for small miscalibrated compressors (@proxy_model_setting), "
        "then qualitative scaling trends should be robust to proxy choice: the relative "
        "ordering of model sizes is stable across proxy families. "
        "Empirical ablations in Appendix E.1.4 and E.1.5 confirm this consistency."
    ),
    prior=0.82,
)

strat_mi_proxy_for_quality = support(
    [mi_estimator_practical, mi_estimator_clipping],
    mi_as_proxy_proposal,
    background=[mi_definition, mc_estimator_def],
    reason=(
        "MI (@mi_definition) directly quantifies how much of the original context X is preserved "
        "in compression Z. The MC estimator (@mc_estimator_def) makes this computable in practice "
        "using only log probabilities (@mi_estimator_practical), with finite-sample artifacts "
        "corrected by clipping (@mi_estimator_clipping). Because MI is computed solely from "
        "the compression without task labels, it is inherently task-agnostic, analogous to "
        "how perplexity quantifies LM quality without task-specific labels [@Kaplan2020]."
    ),
    prior=0.85,
)

__all__ = [
    "mi_definition",
    "mc_estimator_def",
    "rate_distortion_def",
    "bit_efficiency_def",
    "proxy_model_setting",
    "flops_per_generation_def",
    "experimental_datasets",
    "compressor_model_families",
    "predictor_models",
    "mc_estimator_upper_bound",
    "mi_estimator_practical",
    "mi_estimator_clipping",
    "proxy_consistency",
    "gaussian_rd_qualitative",
]
