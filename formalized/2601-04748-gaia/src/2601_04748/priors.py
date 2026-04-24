"""Priors for arXiv 2601.04748: When Single-Agent with Skills Replace Multi-Agent Systems.

All claims below are independent premises (leaf nodes in the BP graph).
Priors reflect reviewer confidence that the claim is true as stated,
informed by the paper's evidence, experimental rigor, and domain context.

Empirical observation claims (controlled experiments):
  High confidence (0.87-0.92) — directly reported from controlled experiments with 3 seeds.

Meta-analysis claims (table/figure summaries):
  High confidence (0.82-0.88) — accurate reads of reported data.

Note: H3_null_result gets moderate-low confidence (0.78) because null results are
epistemically weaker — absence of observed effect ≠ absence of effect.
"""

from . import (
    # Compilation section
    compilable_architectures,
    # H1 experimental results
    h1_fit_quality,
    h1_gamma_super_linear,
    h1_kappa_values,
    # H2 experimental results
    h2_competitor_results,
    h2_gpt4o_advantage,
    # H3 experimental results
    h3_null_result,
    # H4 experimental results
    h4_hierarchy_results,
    h4_gpt4o_smaller_benefit,
)

PRIORS = {
    # --- Compilation section ---
    compilable_architectures: (
        0.85,
        "The compilability table reflects straightforward analysis of communication graph "
        "structure. Conditions C1-C3 are logically sound. High confidence but not 1.0 "
        "because compilability of 'Iterative Refinement' with potential private state is "
        "somewhat underspecified at the boundary."
    ),

    # --- H1: Non-linear Phase Transition ---
    h1_fit_quality: (
        0.88,
        "The scaling model achieves R^2 > 0.97 for both models — very high fit quality. "
        "Direct data analysis result from controlled experiment. Tempered by: only 2 model "
        "families tested, synthetic library may not generalize, and limited data points "
        "for fitting (6-7 library sizes). High fit may be partly due to flexible functional form."
    ),
    h1_gamma_super_linear: (
        0.87,
        "The super-linear decay exponent gamma > 1 (1.72 and 1.56) is a direct read-off "
        "from fitted model with high R^2. High confidence in the measurement. Some uncertainty: "
        "exponent is a fitted parameter (extrapolation beyond measured range uncertain), and "
        "gamma > 1 boundary is sensitive to fitting noise at a small number of data points."
    ),
    h1_kappa_values: (
        0.82,
        "The capacity threshold kappa ~83-92 is derived from model fit. Moderate-high confidence "
        "as a practical guideline. Lower confidence than fit quality because: (1) model-specific "
        "and may not generalize to other architectures, (2) counterintuitive finding that GPT-4o "
        "has lower kappa than GPT-4o-mini suggests fitting noise may be significant, and "
        "(3) the authors acknowledge this may reflect fitting variance."
    ),

    # --- H2: Confusability-Driven Errors ---
    h2_competitor_results: (
        0.92,
        "The competitor experiment is well-controlled: ground truth is unambiguous by construction "
        "(only the base skill performs the correct operation). The accuracy drops (7-30% for 1 "
        "competitor, 17-63% for 2 competitors) are large effects measured across multiple nbase "
        "values with 3 random seeds. Main caveat: synthetic competitors may not represent "
        "real-world confusability distributions."
    ),
    h2_gpt4o_advantage: (
        0.88,
        "The GPT-4o vs GPT-4o-mini comparison under high confusability (70% vs 37% at nbase=10, "
        "ncomp=2) is a direct measurement from controlled experiment with large effect size. "
        "Tempered by: only two model families tested, temperature=0 removes variance information, "
        "and comparison is at a single operating point rather than across the full curve."
    ),

    # --- H3: Instructional Saturation (null result) ---
    h3_null_result: (
        0.78,
        "The null result (policy complexity has negligible effect) is supported by overlapping "
        "curves within standard error bounds. However, null results are epistemically weaker — "
        "absence of evidence is not strong evidence of absence. Study uses only 3 complexity "
        "levels with moderate granularity (30/100/300 tokens). Finer studies or different "
        "policy types might reveal effects."
    ),

    # --- H4: Hierarchy Mitigation ---
    h4_hierarchy_results: (
        0.90,
        "The hierarchical routing improvement (+37-40% for GPT-4o-mini, +9-10% for GPT-4o at "
        "|S|=120) is a large, consistent effect across both models. Experiment compares three "
        "methods with the same tasks and ground truth. High confidence. Caveat: the hierarchical "
        "design is well-aligned with confusability structure by construction, which may overestimate "
        "benefits for more complex real-world hierarchies."
    ),
    h4_gpt4o_smaller_benefit: (
        0.85,
        "The observation that GPT-4o benefits less from hierarchy (+10% vs +40%) is consistent "
        "with GPT-4o having better baseline semantic discrimination. Effect is directionally "
        "consistent with the model capability interpretation. Some uncertainty: only two model "
        "families compared, and the difference could partly reflect different kappa values "
        "rather than discrimination ability per se."
    ),
}
