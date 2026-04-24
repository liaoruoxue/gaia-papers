"""An Information Theoretic Perspective on Agentic System Design (arXiv:2512.21720)"""

from .motivation import (
    compressor_scaling_dominates,
    deep_research_cost_reduction,
    mi_as_proxy_proposal,
    design_adhoc,
)
from .s2_framework import (
    mc_estimator_def,
    mc_estimator_upper_bound,
    mi_estimator_practical,
    mi_estimator_clipping,
    proxy_consistency,
    gaussian_rd_qualitative,
)
from .s3_results import (
    accuracy_scales_with_compressor,
    larger_compressors_more_concise,
    flops_sublinear_with_compressor,
    predictor_scaling_marginal,
    compressor_family_most_important,
    mi_scales_with_compressor,
    bit_efficiency_scales_with_compressor,
    scaling_robust_to_conciseness_prompt,
    mi_correlates_with_accuracy,
    mi_correlates_with_perplexity,
    predictor_family_independence,
    small_compressor_deep_research,
    qwen14b_deep_research_result,
    local_compute_trade,
)
from .s4_discussion import (
    principle_sublinear_scaling,
    principle_frontload_compute,
    principle_information_density,
    principle_model_family_matters,
    limitation_proxy_variance,
    limitation_non_reasoning_focus,
    future_better_mi_estimator,
    future_training_objective,
    future_routing_strategies,
)

__all__ = [
    # Core thesis
    "compressor_scaling_dominates",
    "deep_research_cost_reduction",
    "mi_as_proxy_proposal",
    # Framework
    "mc_estimator_def",
    "mc_estimator_upper_bound",
    "mi_estimator_practical",
    "proxy_consistency",
    # Key empirical results
    "accuracy_scales_with_compressor",
    "larger_compressors_more_concise",
    "flops_sublinear_with_compressor",
    "predictor_scaling_marginal",
    "compressor_family_most_important",
    "mi_scales_with_compressor",
    "bit_efficiency_scales_with_compressor",
    "mi_correlates_with_accuracy",
    "mi_correlates_with_perplexity",
    "predictor_family_independence",
    # Deep Research
    "small_compressor_deep_research",
    "qwen14b_deep_research_result",
    # Design principles
    "principle_sublinear_scaling",
    "principle_frontload_compute",
    "principle_information_density",
    "principle_model_family_matters",
]
