"""Section 4: Conclusions and Contributions"""

from gaia.lang import claim, support, deduction

from .motivation import (
    emergent_coordination_claim,
    provenance_traceability_claim,
    framework_overview,
    ai_science_gap,
)
from .s2_system_design import (
    agent_diversity_claim,
    multiparent_synthesis_claim,
    plannerless_coordination_design_claim,
    community_feedback_loop_claim,
    mutation_layer_claim,
    six_node_loop,
    llm_backend,
)
from .s3_case_studies import (
    cross_study_coordination_claim,
    fem_validation_claim,
    analogy_strength_claim,
    materials_top_candidates,
    sstr2_design_recommendation,
    quantitative_summary,
)

# ─────────────────────────────────────────────────────────────────────────────
# Core contribution claims
# ─────────────────────────────────────────────────────────────────────────────

open_ecosystem_claim = claim(
    "ScienceClaw + Infinite constitutes an open scientific ecosystem: any contributor can "
    "deploy new agents into the shared platform without central approval, because the "
    "open skill registry and artifact DAG are designed as extensible infrastructure "
    "rather than closed pipelines. This openness is enforced by the registry's "
    "plug-and-play skill API and the platform's provenance-aware governance [@Wang2025].",
    title="Open and extensible scientific ecosystem",
)

strat_open_ecosystem = support(
    [framework_overview, community_feedback_loop_claim],
    open_ecosystem_claim,
    reason=(
        "The framework overview (@framework_overview) describes an extensible registry of "
        "300+ skills with a structured artifact layer. The community feedback loop "
        "(@community_feedback_loop_claim) shows that governance is reputation-based "
        "(karma tiers) rather than gatekeeping-based, allowing any contributor to "
        "participate and gain influence through quality contributions. Together, the "
        "technical openness of the registry and the governance model of the platform "
        "jointly enable the open ecosystem property."
    ),
    prior=0.85,
)

heterogeneous_tool_chaining_claim = claim(
    "The ScienceClaw framework successfully demonstrates heterogeneous tool chaining: "
    "in the formal analogy study, 9 agents invoked 23 distinct tools from different "
    "domain families (systematic review, ontology construction, network analysis, "
    "power-law regression, L-system grammar synthesis), producing 52 artifacts with "
    "25 cross-agent synthesis events — all without a routing table or hardcoded decision "
    "tree governing tool selection [@Wang2025].",
    title="Heterogeneous tool chaining demonstrated",
)

strat_het_chaining = support(
    [quantitative_summary, plannerless_coordination_design_claim],
    heterogeneous_tool_chaining_claim,
    reason=(
        "The quantitative summary (@quantitative_summary) shows the formal analogy study "
        "used 23 tools with 9 agents. The plannerless coordination design "
        "(@plannerless_coordination_design_claim) establishes that no routing table governs "
        "tool selection. The combination of high tool diversity and plannerless selection "
        "demonstrates that the agent profiles are sufficient to drive heterogeneous chaining "
        "across domain families."
    ),
    prior=0.88,
)

traceable_reasoning_claim = claim(
    "The ScienceClaw + Infinite framework achieves traceable reasoning from raw computation "
    "to published finding: in all four case studies, the artifact DAG records the complete "
    "chain of intermediate computations, and the Infinite platform's discourse relations "
    "(cite, extend, contradict) make the reasoning structure machine-readable and auditable "
    "by later investigators [@Wang2025].",
    title="Traceable reasoning from computation to finding",
)

strat_traceable = deduction(
    [provenance_traceability_claim, community_feedback_loop_claim],
    traceable_reasoning_claim,
    reason=(
        "The provenance traceability claim (@provenance_traceability_claim) establishes that "
        "any number in a published post can be traced through the DAG to its origin. "
        "The community feedback loop claim (@community_feedback_loop_claim) establishes "
        "that the Infinite platform records discourse relations in machine-readable form. "
        "Together these two properties constitute complete traceable reasoning: "
        "computational provenance (from raw data to result) and argumentative provenance "
        "(from result to published interpretation)."
    ),
    prior=0.95,
)

gap_addressed_claim = claim(
    "The ScienceClaw + Infinite framework addresses the gap in autonomous scientific AI: "
    "the four case studies demonstrate that independent agents can sustain multi-cycle "
    "investigations without human task assignment, producing convergent findings through "
    "emergent artifact exchange — a capability not demonstrated by prior AI-in-science "
    "systems [@Wang2025].",
    title="Framework addresses autonomous scientific AI gap",
)

strat_gap_addressed = support(
    [ai_science_gap, cross_study_coordination_claim, traceable_reasoning_claim],
    gap_addressed_claim,
    reason=(
        "The AI science gap (@ai_science_gap) identifies that no prior system supports "
        "a persistent open ecosystem for multi-agent autonomous investigation. The cross-study "
        "coordination evidence (@cross_study_coordination_claim) shows emergent convergence "
        "across four domains without human task assignment. The traceable reasoning claim "
        "(@traceable_reasoning_claim) shows full auditability from computation to finding. "
        "The gap required: autonomous multi-agent operation, emergent convergence, and "
        "traceability — all three are demonstrated."
    ),
    prior=0.82,
)

infrastructure_claim = claim(
    "ScienceClaw + Infinite establishes infrastructure for scientific inquiry that remains "
    "open to continued analysis and contribution: the artifact DAG grows as agents add "
    "findings, the Infinite platform accumulates a growing record of discourse, and new "
    "agents can build on prior artifact chains without re-running upstream computations, "
    "enabling cumulative science across multiple investigation cycles [@Wang2025].",
    title="Cumulative scientific infrastructure",
)

strat_infrastructure = support(
    [mutation_layer_claim, community_feedback_loop_claim, cross_study_coordination_claim],
    infrastructure_claim,
    reason=(
        "The mutation layer (@mutation_layer_claim) prevents unbounded DAG growth by pruning "
        "redundant workflows. The community feedback loop (@community_feedback_loop_claim) "
        "ensures new contributions are integrated into the discourse record. The cross-study "
        "coordination evidence (@cross_study_coordination_claim) shows the system operates "
        "at multi-agent scale. These three properties together support cumulative, "
        "open-ended growth of the scientific knowledge base without requiring system "
        "re-initialization between investigations."
    ),
    prior=0.78,
)
