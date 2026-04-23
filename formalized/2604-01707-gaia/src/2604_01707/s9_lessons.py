"""Section 9: Lessons and Opportunities"""

from gaia.lang import (
    claim, question,
    support, deduction,
)
from .s8_experiments import (
    obs_tree_hierarchical_strong,
    obs_info_completeness_crucial,
    obs_connecting_multihop_validated,
    result_granularity_token_cost,
    rule_based_stable_scaling,
    obs_temporal_backbone_dependent,
    new_method_sota,
)

# ── Lessons (evidence-backed) ─────────────────────────────────────────────────

lesson_hierarchical = claim(
    "L1: Compared to flat memory structures, hierarchical organization is more effective in "
    "capturing structural relationships between information. This can be achieved by either "
    "employing tree-based indices (as in MemTree, MemOS) or designing multi-level storage "
    "(as in MemoryOS).",
    title="L1: Hierarchical organization preferred",
)

strat_lesson_hierarchical = support(
    [obs_tree_hierarchical_strong],
    lesson_hierarchical,
    reason=(
        "The experimental observation that tree-based and hierarchical methods (MemTree, MemOS, "
        "MemoryOS) consistently outperform flat methods (@obs_tree_hierarchical_strong) "
        "directly justifies L1 as a design principle for practitioners."
    ),
    prior=0.90,
)

lesson_completeness = claim(
    "L2: Information completeness is fundamental to memory mechanisms. While structured "
    "representations like triples in graphs improve organization, retaining raw dialogue context "
    "is essential to prevent semantic loss during the information extraction or retrieval stage.",
    title="L2: Retain raw context",
)

strat_lesson_completeness = support(
    [obs_info_completeness_crucial],
    lesson_completeness,
    reason=(
        "The experimental finding that graph-only extraction (Mem0g) underperforms "
        "hybrid extraction (Mem0 with raw + summary) in most cases "
        "(@obs_info_completeness_crucial) motivates L2: raw dialogue preservation "
        "should be a design requirement for memory methods."
    ),
    prior=0.82,
)

lesson_granularity = claim(
    "L3: Optimizing memory granularity by processing multiple dialogue turns as a single unit "
    "during the information extraction or memory management stage significantly reduces token "
    "consumption, while appropriate partitioning further maintains the coherence of retrieved "
    "information.",
    title="L3: Coarse granularity reduces token cost",
)

strat_lesson_granularity = support(
    [result_granularity_token_cost],
    lesson_granularity,
    reason=(
        "Token cost analysis shows that coarser extraction granularity (daily summaries in "
        "MemoryBank, segment-level in MemoryOS) achieves lower cost without proportional "
        "performance loss (@result_granularity_token_cost). This is possible because modern "
        "LLMs are capable enough to reason over coarser-grained segments."
    ),
    prior=0.82,
)

# ── Opportunities (research directions) ──────────────────────────────────────

opportunity_multimodal = claim(
    "O1: Real-world settings involve complex and diverse information sources including textual "
    "conversations, historical interaction traces, and multimodal signals (audio, images, videos). "
    "Existing memory mechanisms often focus on a single or limited form, constraining effective "
    "information utilization. A promising research direction is unified memory mechanisms that "
    "support heterogeneous and multimodal memory within a shared storage and retrieval framework.",
    title="O1: Multimodal memory",
)

opportunity_compression = claim(
    "O2: Existing competitive memory methods manage information in ways that lead to rapid storage "
    "growth and increasing management and retrieval overhead. How to compress memory without losing "
    "useful information remains a major challenge. This creates an opportunity to explore latent "
    "representations beyond explicit text and learned compression mechanisms to achieve "
    "high-density yet usable memory.",
    title="O2: Learned memory compression",
)

opportunity_bidirectional = claim(
    "O3: Existing hierarchical memory mechanisms primarily focus on consolidating short-term memory "
    "into long-term storage but do not support the reverse transformation. A promising direction is "
    "to design bidirectional memory transformation mechanisms that enable efficient consolidation "
    "and reconstruction across memory hierarchies.",
    title="O3: Bidirectional memory transformation",
)

# ── Framework completeness ────────────────────────────────────────────────────

framework_completeness_validated = claim(
    "The unified framework is validated as complete and expressive: it successfully decomposes "
    "all ten representative agent memory methods into the four modular components (information "
    "extraction, memory management, memory storage, information retrieval) without requiring "
    "any component to be split or merged. The framework enables systematic comparison of design "
    "choices and the derivation of evidence-backed lessons.",
    title="Framework validated as complete",
)

strat_framework_completeness = support(
    [new_method_sota, lesson_hierarchical, lesson_completeness, lesson_granularity],
    framework_completeness_validated,
    reason=(
        "The framework's completeness is demonstrated by two outcomes: "
        "(1) it enables systematic comparison that yields actionable lessons "
        "(@lesson_hierarchical, @lesson_completeness, @lesson_granularity); "
        "(2) it guides the design of a new SOTA method (@new_method_sota) by combining "
        "modules identified through the framework analysis. A framework that enables "
        "both analysis and synthesis across the state of the art is validated as complete."
    ),
    prior=0.85,
)
