"""Section 4: Open problems, design principles, and limitations."""

from gaia.lang import claim, support

from .motivation import setup_cls_theory
from .s2_spectrum import (
    acquisition_maintenance_tradeoff,
    spectrum_not_pipeline,
)
from .s2_mapping import (
    missing_diagonal,
    framing_limitation,
    scalability_bottleneck,
)
from .s3_insights import (
    lifecycle_neglected,
    transferability_concavity,
)

# --- Open problems (Section 4) ---

problem_adaptive_selection = claim(
    "**Open Problem 1: Adaptive level selection.** Design a meta-controller that, given "
    "a new interaction trace $T$, determines the optimal compression level(s) $L^*$. "
    "The challenge is to formalize a **value-of-information** framework: how much future "
    "utility does the artifact $K_L$ provide relative to the cost of computing and "
    "maintaining it? A key design tension is whether to **jointly optimize** the "
    "meta-controller and level-specific compressors, or to **fix** the meta-controller "
    "and optimize only the compressors. Recent agentic RL surveys ([@Zhang2026agenticrl]) "
    "find that RL primarily amplifies existing capabilities, suggesting that the level "
    "of compression may matter more than the algorithm.",
    title="Open Problem 1: adaptive level selection",
)

problem_cross_level_consistency = claim(
    "**Open Problem 2: Cross-level consistency.** When knowledge exists at multiple "
    "levels simultaneously (e.g., a Level-1 memory and a Level-3 rule about the same "
    "behavior), how should the system detect and resolve inconsistencies? The analogy "
    "to database normalization is suggestive but incomplete -- knowledge artifacts are "
    "**semantic** rather than relational, so equivalence checking cannot be reduced to "
    "key matching.",
    title="Open Problem 2: cross-level consistency",
)

problem_lifecycle_management = claim(
    "**Open Problem 3: Principled lifecycle management.** Borrow from software "
    "engineering: version control for knowledge artifacts, dependency tracking between "
    "levels, deprecation protocols, and conflict resolution. Recent workflow-optimization "
    "surveys ([@Yue2026workflow]) advocate a 'minimum plasticity' principle; an "
    "analogous principle for knowledge management -- **promoting only when evidence "
    "warrants** -- would reduce maintenance burden while preserving adaptability.",
    title="Open Problem 3: principled lifecycle management",
)

# --- Design principles ---

principle_level_agnostic_core = claim(
    "**Design Principle 1: Level-agnostic compression core.** The compression engine "
    "should be parameterized by output level, not hard-coded. DSPy ([@Khattab2024dspy]) "
    "demonstrates that declarative specifications can be compiled into optimized "
    "pipelines at a predetermined level; a level-agnostic core would generalize this "
    "to make the level itself a tunable parameter.",
    title="Principle 1: level-agnostic compression core",
)

principle_bidirectional = claim(
    "**Design Principle 2: Bidirectional promotion and demotion.** Knowledge should "
    "flow upward (memory -> skill -> rule when patterns accumulate) **and** downward "
    "(rule -> skill -> memory when context demands specificity). This bidirectional "
    "flow distinguishes the proposed architecture from current systems that treat "
    "compression as a one-way operation.",
    title="Principle 2: bidirectional promotion/demotion",
)

principle_lifecycle_governance = claim(
    "**Design Principle 3: Continuous lifecycle governance.** Every knowledge artifact "
    "should carry metadata (provenance, confidence, usage frequency, last validation "
    "time) enabling principled maintenance. Without such metadata, deprecation, "
    "conflict resolution, and staleness detection cannot be automated.",
    title="Principle 3: continuous lifecycle governance",
)

# --- Idle-time consolidation ---

idle_time_consolidation = claim(
    "The spectrum suggests **idle-time consolidation**: upward compression (Level 1 -> "
    "Level 2 -> Level 3) should occur during low-activity periods, analogous to "
    "hippocampal-neocortical consolidation during sleep ([@McClelland1995cls]). No "
    "current system implements this -- all surveyed systems compress synchronously at "
    "ingestion time. Asynchronous consolidation would decouple compression cost from "
    "user-facing latency.",
    title="Idle-time consolidation, analogous to sleep",
)

strat_idle_consolidation = support(
    [scalability_bottleneck, acquisition_maintenance_tradeoff],
    idle_time_consolidation,
    reason=(
        "Synchronous compression at ingestion forces the cost of upward compression "
        "to land on the user-facing latency budget. The acquisition-versus-maintenance "
        "trade-off (@acquisition_maintenance_tradeoff) and the linear-cost scalability "
        "bottleneck (@scalability_bottleneck) both indicate that some compression must "
        "happen, but doing it asynchronously (during idle periods) decouples it from "
        "request latency. The biological CLS analogue (@setup_cls_theory) provides a "
        "design template for this asynchronous regime."
    ),
    prior=0.78,
    background=[setup_cls_theory],
)

# --- Concrete diagonal architecture sketch ---

diagonal_architecture = claim(
    "A 'diagonal' system that addresses the missing-diagonal gap might comprise three "
    "components: "
    "(a) a **meta-controller** that routes each trace to one or more level-specific "
    "compressors based on novelty and frequency (a first-seen pattern stays at L1; "
    "after $k$ similar L1 entries accumulate, the promotion engine consolidates them "
    "into an L2 skill; after cross-domain recurrence, the engine generalizes to an L3 "
    "rule); "
    "(b) a **promotion/demotion engine** that handles transitions, validating newly "
    "promoted L2 skills against held-out tasks before replacing source L1 entries, and "
    "demoting when a skill is repeatedly retrieved but unused or when a rule fails in "
    "a specific context; "
    "(c) a **lifecycle manager** that tracks provenance, usage frequency, and last "
    "validation time for every artifact, enabling principled deprecation. "
    "Existing components -- MemSkill's RL controller for routing, EvoSkill's Pareto "
    "selection for promotion, AutoSkill's versioning ([@Yang2026autoskill]) for "
    "lifecycle -- could serve as building blocks.",
    title="Diagonal architecture: meta-controller + promotion/demotion + lifecycle",
)

# --- Worked example ---

worked_example = claim(
    "Worked example of the diagonal architecture: a customer-support agent encounters "
    "a timeout on /api/export and stores an L1 memory. After five similar episodes, "
    "promotion produces an L2 skill (HANDLE EXPORT TIMEOUT: check batch size, reduce if "
    ">1000 rows, retry). After dozens of instances across endpoints, generalization "
    "yields an L3 rule ('Timeouts on data-intensive endpoints typically stem from "
    "oversized batches'). If the rule fails in a novel context, demotion drops back to "
    "L1, restarting evidence collection.",
    title="Worked example: customer support timeout -> L1 -> L2 -> L3",
)

# --- Limitations ---

limitation_scope = claim(
    "**Limitation: scaffold-level scope.** The framework focuses on scaffold-level "
    "knowledge; training-time methods (RLHF, Constitutional AI) are complementary but "
    "distinct. The framework does not unify these training-time methods with the "
    "scaffold-level spectrum.",
    title="Limitation: scaffold-level scope only",
)

limitation_conceptual = claim(
    "**Limitation: conceptual rather than empirically validated.** The framework is a "
    "conceptual unification; the spectrum's utility as a **design tool** awaits "
    "experimental confirmation via the testable predictions (Section 3). The paper "
    "does not itself implement or evaluate a diagonal system.",
    title="Limitation: conceptual, not empirically validated",
)

limitation_discrete_levels = claim(
    "**Limitation: discrete-level abstraction.** The four discrete levels are a "
    "simplifying abstraction; in practice, compression may be continuous. EvolveR "
    "([@Wu2025evolver])'s strategies straddle Levels 2 and 3, suggesting the boundary "
    "may not be sharp in real systems.",
    title="Limitation: discrete levels are a simplification",
)

limitation_snapshot = claim(
    "**Limitation: Q1 2026 snapshot.** The survey is a snapshot of the field as of "
    "Q1 2026; the field moves rapidly and additional systems (such as LightMem "
    "([@Fang2025lightmem])) continue to appear that further corroborate or extend the "
    "patterns identified in the spectrum.",
    title="Limitation: Q1 2026 snapshot",
)

limitation_text_only = claim(
    "**Limitation: text-only focus.** The analysis focuses on text-based agents. The "
    "spectrum naturally extends to multimodal experience -- visual observations and "
    "cross-modal interactions amplify the need for efficient compression at every "
    "level -- but this extension is not formally treated.",
    title="Limitation: text-only focus, multimodal extension untreated",
)

# --- Conclusion synthesis ---

unification_is_timely = claim(
    "Unification of the memory and skill perspectives is **timely**: with 10+ relevant "
    "papers in Q1 2026 alone and production systems increasingly managing persistent "
    "experiential knowledge ([@Chan2026composer2]), without a shared framework two "
    "communities risk solving the same problem twice. The most promising direction is "
    "building systems that **adaptively select compression granularity** to match the "
    "value and generality of each experience, enabling agents that scale efficiently "
    "across long deployments.",
    title="Unification is timely; adaptive selection is the priority",
)

strat_unification_timely = support(
    [missing_diagonal, framing_limitation, lifecycle_neglected],
    unification_is_timely,
    reason=(
        "Three convergent observations support the urgency of unification: the "
        "missing diagonal (@missing_diagonal) shows no system handles cross-level "
        "compression; the framing limitation (@framing_limitation) shows the gap is "
        "structural rather than incidental; and lifecycle neglect (@lifecycle_neglected) "
        "shows the field lacks even basic maintenance infrastructure. Without unification "
        "the disconnect persists and engineering effort is duplicated."
    ),
    prior=0.85,
)

# --- The diagonal architecture proposal as the core synthesis ---

diagonal_is_core_proposal = claim(
    "The diagonal architecture (meta-controller + promotion/demotion engine + lifecycle "
    "manager) is the paper's **core constructive proposal**. It directly addresses the "
    "missing diagonal gap by providing concrete components that can be built from "
    "existing building blocks (MemSkill's RL controller, EvoSkill's Pareto selection, "
    "AutoSkill's versioning), so the proposal is implementable rather than purely "
    "speculative.",
    title="Diagonal architecture is the paper's core constructive proposal",
)

strat_diagonal_proposal = support(
    [diagonal_architecture, missing_diagonal, problem_adaptive_selection],
    diagonal_is_core_proposal,
    reason=(
        "The diagonal architecture (@diagonal_architecture) targets exactly the gap "
        "identified by the missing diagonal (@missing_diagonal) and operationalizes "
        "the adaptive-level-selection open problem (@problem_adaptive_selection). "
        "Because each component can be assembled from existing building blocks, the "
        "proposal is constructive rather than aspirational."
    ),
    prior=0.82,
)
