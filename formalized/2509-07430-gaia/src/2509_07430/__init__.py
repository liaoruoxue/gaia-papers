from .motivation import (
    pass1_improves,
    passk_degrades,
    catastrophic_forgetting,
    rkl_accelerates_collapse,
    divergence_choice_neglected,
    mass_covering_preserves,
)
from .s2_background import (
    grpo_no_diversity,
    rkl_mode_seeking_harm,
    forward_kl_mass_covering,
    js_mass_covering,
)
from .s3_method import (
    partition_rationale,
    generator_efficiency,
    dphrl_handles_discrete,
    threshold_8_of_8_optimal,
)
from .s4_theory import (
    theorem1_statement,
    theorem1_interpretation,
    trpo_standard_vs_dphrl,
    grpo_no_bound,
)
from .s5_experiments import (
    sql_bird_results,
    sql_spider_results,
    ood_math_results,
    math_llama_results,
    math_qwen_results,
    solution_style_diversity,
    capability_retention,
)
from .s6_conclusions import (
    dphrl_resolves_paradox,
    divergence_is_key_lever,
    dphrl_generalizes,
)

__all__ = [
    # Core problem
    "passk_degrades",
    "catastrophic_forgetting",
    "rkl_accelerates_collapse",
    # Method
    "mass_covering_preserves",
    "partition_rationale",
    "generator_efficiency",
    "threshold_8_of_8_optimal",
    # Theory
    "theorem1_statement",
    "trpo_standard_vs_dphrl",
    # Key experimental results
    "sql_bird_results",
    "sql_spider_results",
    "ood_math_results",
    "math_llama_results",
    "math_qwen_results",
    # Conclusions
    "dphrl_resolves_paradox",
    "divergence_is_key_lever",
    "dphrl_generalizes",
]
