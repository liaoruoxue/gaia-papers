"""
Limitations & Conclusion
========================

The paper acknowledges several limitations and synthesizes the overall conclusion.
"""

from gaia.lang import claim, support

from .motivation import contribution_arc_framework, contribution_dual_architecture
from .s4_main_results import (
    arc_outperforms_react,
    arc_outperforms_resum,
    context_degradation_is_dominant_failure,
)
from .s4_ablations import (
    cm_is_learnable,
    cm_lifts_actor_ceiling,
    per_turn_best,
)

# --- Stated limitations ---

limitation_overhead = claim(
    "ARC introduces an explicit context-management component (the CM), which incurs additional "
    "computational and system overhead compared to single-model agent designs. Although the CM "
    "is decoupled from action execution and can be implemented efficiently, active context "
    "monitoring and revision add cost that may be undesirable in latency- or "
    "resource-constrained settings.",
    title="Limitation: extra computational overhead",
    metadata={"source": "artifacts/2601.12030.pdf, Limitations"},
)

limitation_scope = claim(
    "Evaluation focuses on long-horizon information-seeking and search-based tasks. The "
    "applicability of reflection-driven context management to other agentic scenarios "
    "(e.g., embodied agents, tool-heavy automation, code generation) remains to be explored.",
    title="Limitation: scope restricted to information seeking",
    metadata={"source": "artifacts/2601.12030.pdf, Limitations"},
)

limitation_training_data = claim(
    "Training the Context Manager relies on curated trajectories that exhibit desirable "
    "summarization and reflection behaviors. The dependence on annotated/filtered data may "
    "limit scalability; more data-efficient or self-supervised paradigms remain future work.",
    title="Limitation: CM training depends on curated data",
    metadata={"source": "artifacts/2601.12030.pdf, Limitations"},
)

# --- Conclusion synthesis ---

conclusion_main = claim(
    "Long-horizon failures in deep-search agents stem in large part from how interaction history "
    "is compressed, organized, and reused over time, not solely from limited reasoning capacity. "
    "ARC — an active and reflection-driven framework with always-on incremental memory plus "
    "selectively triggered reflection, implemented by a dedicated learnable Context Manager — "
    "consistently improves long-horizon performance over raw history concatenation and passive "
    "summarization, and effective context management is itself a learnable capability.",
    title="Overall conclusion",
    metadata={"source": "artifacts/2601.12030.pdf, Section 5"},
)

# --- Strategy: synthesize the conclusion from the four main empirical pillars ---

strat_overall_conclusion = support(
    [
        arc_outperforms_react,
        arc_outperforms_resum,
        context_degradation_is_dominant_failure,
        cm_is_learnable,
        per_turn_best,
    ],
    conclusion_main,
    background=[contribution_arc_framework, contribution_dual_architecture],
    reason=(
        "The conclusion combines four empirical pillars established earlier: (1) ARC beats raw "
        "concatenation (@arc_outperforms_react) and (2) passive summarization (@arc_outperforms_resum) "
        "across actors and benchmarks; (3) the failure mode is context degradation rather than "
        "reasoning capacity (@context_degradation_is_dominant_failure); (4) effective context "
        "management is learnable (@cm_is_learnable) and is best applied per-turn (@per_turn_best). "
        "The framework (@contribution_arc_framework) and decoupled architecture "
        "(@contribution_dual_architecture) are the design principles that operationalize these "
        "findings."
    ),
    prior=0.85,
)

__all__ = [
    "limitation_overhead",
    "limitation_scope",
    "limitation_training_data",
    "conclusion_main",
    "strat_overall_conclusion",
]
