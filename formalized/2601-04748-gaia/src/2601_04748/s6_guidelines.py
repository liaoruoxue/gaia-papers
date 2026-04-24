"""
Section 5.6 & 6: Practical Guidelines and Conclusions
======================================================

Derives practical design guidelines for skill libraries based on experimental findings,
and presents the paper's conclusions and limitations.
"""

from gaia.lang import claim, setting, support

from .motivation import contribution_compilation, contribution_scaling, contribution_hierarchy
from .s4_cognitive_theory import h1_phase_transition, h2_confusability, h4_hierarchy_mitigation
from .s5_experiments import (
    h1_kappa_values,
    h2_competitor_results,
    h4_hierarchy_results,
    h3_null_result,
)

# --- Practical guidelines ---

guideline_monitor_size = claim(
    "**Design Guideline 1 (Monitor library size):** Track $|S|$ relative to the model's capacity "
    "($\\kappa \\approx 50$–$100$ for tested GPT models). Performance degrades sharply beyond this "
    "threshold. The inflection point — where accuracy begins to decline most rapidly — occurs "
    "earlier than $\\kappa$ itself, so libraries should be kept below the inflection point "
    "for flat selection, or hierarchical routing should be adopted for larger libraries.",
    title="Guideline 1: Monitor library size vs κ",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

guideline_minimize_confusability = claim(
    "**Design Guideline 2 (Minimize confusability):** Before adding skills, audit semantic overlap. "
    "Merge or differentiate skills with similarity above threshold rather than accumulating near-duplicates. "
    "Skill descriptors should emphasize unique characteristics and avoid generic descriptions that could "
    "apply to multiple skills (e.g., prefer 'compute rolling 7-day average' over 'process data').",
    title="Guideline 2: Minimize semantic confusability",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

guideline_adopt_hierarchy = claim(
    "**Design Guideline 3 (Adopt hierarchy at scale):** For large $|S| \\gg \\kappa$, implement "
    "hierarchical routing with confusability-aware grouping. Each routing stage should involve "
    "fewer than $\\kappa$ options. Semantically similar skills (competitors) should be explicitly "
    "grouped together to ensure first-stage categories are semantically distinct.",
    title="Guideline 3: Adopt hierarchical routing for large libraries",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

guideline_invest_descriptors = claim(
    "**Design Guideline 4 (Invest in descriptors):** Since selection relies primarily on skill "
    "descriptors $\\delta$ (not execution policies $\\pi$, per H3 null result), invest effort in "
    "crafting distinctive, specific descriptions. Descriptor quality has a larger impact on "
    "selection accuracy than policy complexity.",
    title="Guideline 4: Invest in distinctive skill descriptors",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

guideline_match_model = claim(
    "**Design Guideline 5 (Match model to task):** Stronger models show higher $\\kappa$ and "
    "better confusability resistance. For applications with inherently large or confusable skill "
    "libraries, model capability investment yields direct accuracy benefits. GPT-4o shows "
    "approximately 18–26% higher accuracy than GPT-4o-mini under high confusability conditions.",
    title="Guideline 5: Match model capability to library complexity",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

guideline_consider_mas = claim(
    "**Design Guideline 6 (Consider alternative architectures):** For large skill libraries, "
    "the scaling limitations suggest that multi-agent architectures with specialized routers may "
    "outperform monolithic single-agent approaches. The SAS paradigm is optimal for small-to-medium "
    "libraries ($|S| < \\kappa$); for very large libraries, the MAS overhead may be justified.",
    title="Guideline 6: Consider MAS for very large skill libraries",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

# --- Limitations ---

limitation_synthetic = claim(
    "**Limitation 1 (Synthetic data):** While enabling controlled experiments, synthetic skill "
    "libraries may not capture the full complexity of real-world skill distributions. Results "
    "on naturally-occurring skill distributions (e.g., from software development, long-horizon "
    "planning, or scientific workflows) remain to be validated.",
    title="Limitation 1: Synthetic skill libraries",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

limitation_selection_only = claim(
    "**Limitation 2 (Selection-only evaluation):** The experiments measure selection accuracy "
    "(whether the correct skill is identified) but not end-to-end task performance (whether "
    "the downstream task is completed correctly). The propagation of selection errors to final "
    "task outcomes remains unquantified.",
    title="Limitation 2: Selection accuracy not end-to-end performance",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

limitation_model_coverage = claim(
    "**Limitation 3 (Limited model coverage):** Results are based on two OpenAI models (GPT-4o-mini "
    "and GPT-4o). Generalization to other architectures (open-source models, different scales, "
    "multimodal models) requires further study. Whether capacity thresholds are universal or "
    "architecture-specific is unknown.",
    title="Limitation 3: Only two OpenAI models tested",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

limitation_hierarchy_design = claim(
    "**Limitation 4 (Hierarchy design):** The hierarchical approaches tested were relatively simple "
    "(naive domain and confusability-aware two-stage routing). More sophisticated routing mechanisms "
    "(learned, dynamic, or adaptive routing) may yield different results. Designing the optimal "
    "hierarchy structure is not addressed.",
    title="Limitation 4: Simple hierarchical routing only",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.6"},
)

# --- Strategies connecting guidelines to experimental results ---

strat_guideline1 = support(
    [h1_kappa_values, h1_phase_transition],
    guideline_monitor_size,
    reason=(
        "Guideline 1 follows directly from the identified capacity threshold $\\kappa \\approx 83–92$ "
        "(@h1_kappa_values) and the sharp phase transition in accuracy (@h1_phase_transition). "
        "Since accuracy collapses non-linearly beyond $\\kappa$, monitoring library size against "
        "this threshold is a practical proxy for predicting degradation.",
    ),
    prior=0.9,
)

strat_guideline2 = support(
    [h2_competitor_results, h2_confusability],
    guideline_minimize_confusability,
    reason=(
        "Guideline 2 follows from H2 experimental results (@h2_competitor_results) showing that "
        "semantic competitors cause 7–63% accuracy drops at fixed library size. Since confusability "
        "is an independent failure mode from library size (@h2_confusability), minimizing overlap "
        "provides accuracy benefits even when $|S|$ cannot be reduced.",
    ),
    prior=0.9,
)

strat_guideline3 = support(
    [h4_hierarchy_results, h4_hierarchy_mitigation],
    guideline_adopt_hierarchy,
    reason=(
        "Guideline 3 follows from H4 experimental results (@h4_hierarchy_results) showing +37–40% "
        "accuracy improvement from hierarchical routing at $|S| \\geq 60$. The mechanism — keeping "
        "each decision point below $\\kappa$ (@h4_hierarchy_mitigation) — directly informs the "
        "practical recommendation to keep each routing stage below $\\kappa$ options.",
    ),
    prior=0.9,
)

strat_guideline4 = support(
    [h3_null_result, h2_competitor_results],
    guideline_invest_descriptors,
    reason=(
        "Guideline 4 follows from the H3 null result (@h3_null_result): policy complexity does not "
        "significantly affect selection accuracy, while H2 experiments show that descriptor quality "
        "(confusability) strongly affects accuracy (@h2_competitor_results). This asymmetry implies "
        "that investment in distinctive descriptors has higher return than investment in policy quality.",
    ),
    prior=0.8,
)

__all__ = [
    "guideline_monitor_size",
    "guideline_minimize_confusability",
    "guideline_adopt_hierarchy",
    "guideline_invest_descriptors",
    "guideline_match_model",
    "guideline_consider_mas",
    "limitation_synthetic",
    "limitation_selection_only",
    "limitation_model_coverage",
    "limitation_hierarchy_design",
    "strat_guideline1",
    "strat_guideline2",
    "strat_guideline3",
    "strat_guideline4",
]
