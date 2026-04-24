"""Section 4: Discussion — Design Principles, Limitations, and Future Work"""

from gaia.lang import claim, setting, support, deduction
from .motivation import (
    compressor_predictor_pattern,
    compressor_scaling_dominates,
    deep_research_cost_reduction,
    mi_as_proxy_proposal,
)
from .s2_framework import (
    bit_efficiency_def,
    flops_per_generation_def,
    proxy_model_setting,
    compressor_model_families,
)
from .s3_results import (
    flops_sublinear_with_compressor,
    accuracy_scales_with_compressor,
    predictor_scaling_marginal,
    mi_correlates_with_accuracy,
    mi_correlates_with_perplexity,
    compressor_family_most_important,
    local_compute_trade,
    small_compressor_deep_research,
    scaling_robust_to_conciseness_prompt,
)

# ── Design Principles (from Section 4) ────────────────────────────────────────

principle_sublinear_scaling = claim(
    "Design principle: Compressors can be scaled at a sublinear computational cost. "
    "Because larger compressor models are more information-efficient — they omit fewer tokens "
    "while retaining higher information density — FLOPs-per-generation scale sublinearly as "
    "a function of compressor model size.",
    title="Principle: sublinear compute scaling of compressors",
    metadata={"source_section": "Section 4"},
)

principle_frontload_compute = claim(
    "Design principle: 'Front-load' compute into local compressors to reduce remote costs. "
    "Scaling compressors is more effective than scaling predictors. By running larger compressors "
    "on-device (locally), practitioners can reduce predictor serving costs in the cloud.",
    title="Principle: front-load compute into local compressors",
    metadata={"source_section": "Section 4"},
)

principle_information_density = claim(
    "Design principle: Optimize for information density. Mutual information between an input "
    "context and an agent's output is a task-agnostic indicator of compression quality and is "
    "tightly linked to downstream performance and predictor perplexity.",
    title="Principle: optimize for information density (MI)",
    metadata={"source_section": "Section 4"},
)

principle_model_family_matters = claim(
    "Design principle: Expect model family to differ in scaling trends. The choice of compressor "
    "and predictor model family yields offsets in rate-distortion curves and scaling effects. "
    "Qwen-2.5 compressors scale more compute-efficiently than Llama and Gemma-3; "
    "Qwen-2.5 predictors yield higher accuracies than Llama predictors.",
    title="Principle: model family drives rate-distortion offsets",
    metadata={"source_section": "Section 4"},
)

# ── Limitations ────────────────────────────────────────────────────────────────

limitation_proxy_variance = claim(
    "At the 1-3B model scale, the MI estimator relies on proxy models and log probabilities, "
    "introducing potential variance and biases. Small compressor models may be miscalibrated, "
    "causing the proxy to partially correct for miscalibration rather than purely measuring MI.",
    title="Limitation: proxy model variance at 1-3B scale",
    metadata={"source_section": "Section 4"},
)

limitation_non_reasoning_focus = claim(
    "The paper primarily focuses on GPT-style non-reasoning models with single-round communication, "
    "limiting generalizability to reasoning-augmented models (e.g., chain-of-thought, o1-style) "
    "and iterative multi-agent workflows. Reasoning traces introduce additional structure that "
    "may violate the single-pass compressor-predictor model.",
    title="Limitation: focus on non-reasoning single-round models",
    metadata={"source_section": "Section 4"},
)

limitation_moe_compute = claim(
    "Mixture-of-experts (MoE) models may exhibit different scaling behaviors from dense models "
    "because their effective compute cost depends on the number of activated experts rather than "
    "total parameter count. The FLOPs-per-generation formula for dense models (@flops_per_generation_def) "
    "does not apply directly to MoE architectures.",
    title="Limitation: MoE compute cost differs from dense models",
    metadata={"source_section": "Section 4"},
)

limitation_compression_scope = claim(
    "The paper defines compression as text summarization. Other forms of agentic compression — "
    "structured extraction, function-call generation, code summarization — are not studied, "
    "and the MI estimator's applicability to these settings is not demonstrated.",
    title="Limitation: compression defined as summarization only",
    metadata={"source_section": "Section 4"},
)

# ── Future Work ────────────────────────────────────────────────────────────────

future_better_mi_estimator = claim(
    "Alternative MI estimators such as InfoNCE offer promising improvements over the current "
    "Monte Carlo estimator for LM outputs. Future work should compare estimator quality and "
    "sample efficiency across different MI estimation methods.",
    title="Future work: improved MI estimators (e.g., InfoNCE)",
    metadata={"source_section": "Section 4"},
)

future_training_objective = claim(
    "Training objectives based on rate-distortion analysis represent a promising avenue for "
    "optimizing compressor-predictor communication. Rather than using pretrained compressors, "
    "compressors could be fine-tuned to maximize mutual information with downstream task labels.",
    title="Future work: rate-distortion-based training objectives",
    metadata={"source_section": "Section 4"},
)

future_routing_strategies = claim(
    "Information-theoretic principles could guide compressor routing strategies: "
    "when estimated MI is below a threshold, fall back to remote full-context processing "
    "rather than using the local compressor. This would create a principled adaptive routing policy.",
    title="Future work: MI-guided compressor routing",
    metadata={"source_section": "Section 4"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_principle_sublinear = support(
    [flops_sublinear_with_compressor, accuracy_scales_with_compressor],
    principle_sublinear_scaling,
    reason=(
        "FLOPs-per-generation scale sublinearly with compressor size (@flops_sublinear_with_compressor) "
        "because larger compressors generate fewer tokens (@accuracy_scales_with_compressor — larger "
        "compressors also happen to be more concise). This empirical combination supports the "
        "stated principle: parameter count grows roughly linearly in compute/token, but token count "
        "decreases, yielding sublinear overall scaling per generation."
    ),
    prior=0.90,
)

strat_principle_frontload = support(
    [local_compute_trade, compressor_scaling_dominates],
    principle_frontload_compute,
    reason=(
        "Consumer hardware can already host compressors up to 27B parameters (@local_compute_trade), "
        "and scaling compressors yields more performance than scaling predictors "
        "(@compressor_scaling_dominates). Therefore, the practical recommendation is to run "
        "the largest compressor that fits on local hardware, and serve only the predictor remotely — "
        "cutting cloud API costs substantially, as demonstrated in the Deep Research results."
    ),
    prior=0.88,
)

strat_principle_mi_density = support(
    [mi_correlates_with_accuracy, mi_correlates_with_perplexity],
    principle_information_density,
    reason=(
        "MI predicts accuracy via rate-distortion curves (@mi_correlates_with_accuracy) and "
        "predicts perplexity with r=-0.84 (@mi_correlates_with_perplexity). Together these "
        "empirical results justify adopting information density (bits of MI per output token) "
        "as the primary optimization target for compressor design, rather than task-specific metrics."
    ),
    prior=0.85,
)

strat_principle_family = support(
    [compressor_family_most_important, scaling_robust_to_conciseness_prompt],
    principle_model_family_matters,
    reason=(
        "Logistic regression reveals compressor model family as the most important factor "
        "(@compressor_family_most_important — Qwen-2.5 outperforms Llama). Scaling trends are "
        "robust to prompt variations (@scaling_robust_to_conciseness_prompt), confirming that "
        "model capacity, not prompt formatting, drives the family-level differences."
    ),
    prior=0.82,
)

strat_proxy_limitation = support(
    [limitation_proxy_variance],
    limitation_non_reasoning_focus,
    background=[proxy_model_setting],
    reason=(
        "The MI estimator at small scales relies on a proxy model (@proxy_model_setting) because "
        "1-3B models can assign high likelihoods to nonsensical sequences (@limitation_proxy_variance). "
        "This proxy dependency compounds with the focus on non-reasoning single-round models "
        "(@limitation_non_reasoning_focus): reasoning traces would require even more calibration, "
        "making proxy-based MI estimation harder to validate."
    ),
    prior=0.70,
)

__all__ = [
    "principle_sublinear_scaling",
    "principle_frontload_compute",
    "principle_information_density",
    "principle_model_family_matters",
    "limitation_proxy_variance",
    "limitation_non_reasoning_focus",
    "limitation_moe_compute",
    "limitation_compression_scope",
    "future_better_mi_estimator",
    "future_training_objective",
    "future_routing_strategies",
]
