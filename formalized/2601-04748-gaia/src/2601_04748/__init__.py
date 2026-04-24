"""
When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail
============================================================================

Li (2026). arXiv:2601.04748

This package formalizes the knowledge structure of a paper investigating when skill-based
single-agent systems (SAS) can replace multi-agent systems (MAS) and when they fail.

Key findings:
1. MAS-to-SAS compilation is feasible for serializable, shared-history, homogeneous-backbone systems,
   reducing tokens ~54% and latency ~50% while preserving accuracy within ±4%.
2. Skill selection exhibits a non-linear phase transition: accuracy is stable up to a critical library
   size κ ≈ 83–92 (for GPT-4o/GPT-4o-mini), then drops sharply — not gradually.
3. Semantic confusability among skills, not library size alone, drives degradation.
4. Policy complexity does not significantly affect selection accuracy (H3 null result).
5. Hierarchical routing mitigates scaling limits, recovering +37–40% accuracy at large library sizes.
"""

from .motivation import (
    mas_effectiveness,
    mas_overhead,
    skill_definition,
    sas_definition,
    compilation_view,
    contribution_compilation,
    contribution_scaling,
    contribution_hierarchy,
)

from .s2_compilation import (
    compilability_conditions,
    compilable_architectures,
    compilation_accuracy,
    compilation_token_reduction,
    compilation_latency_reduction,
    hotpotqa_improvement,
)

from .s4_cognitive_theory import (
    scaling_model,
    h1_phase_transition,
    h2_confusability,
    h3_instructional_saturation,
    h4_hierarchy_mitigation,
)

from .s5_experiments import (
    h1_fit_quality,
    h1_gamma_super_linear,
    h1_kappa_values,
    h2_competitor_results,
    h2_gpt4o_advantage,
    h3_null_result,
    h3_transformer_explanation,
    h4_hierarchy_results,
    h4_gpt4o_smaller_benefit,
)

from .s6_guidelines import (
    guideline_monitor_size,
    guideline_minimize_confusability,
    guideline_adopt_hierarchy,
    guideline_invest_descriptors,
    guideline_match_model,
    guideline_consider_mas,
    limitation_synthetic,
    limitation_selection_only,
    limitation_model_coverage,
    limitation_hierarchy_design,
)

__all__ = [
    # Core contributions (exported interface)
    "compilation_view",
    "contribution_compilation",
    "contribution_scaling",
    "contribution_hierarchy",
    # Compilation
    "compilability_conditions",
    "compilable_architectures",
    "compilation_accuracy",
    "compilation_token_reduction",
    "compilation_latency_reduction",
    # Cognitive theory
    "scaling_model",
    "h1_phase_transition",
    "h2_confusability",
    "h4_hierarchy_mitigation",
    # Experimental results
    "h1_kappa_values",
    "h2_competitor_results",
    "h3_null_result",
    "h4_hierarchy_results",
    # Guidelines
    "guideline_monitor_size",
    "guideline_minimize_confusability",
    "guideline_adopt_hierarchy",
    "guideline_invest_descriptors",
    # Limitations
    "limitation_synthetic",
    "limitation_selection_only",
    "limitation_model_coverage",
]
