"""
Introduction & Motivation: Active vs Passive Context Management
================================================================

Yao et al. (2026) argue that long-horizon failures of information-seeking LLM agents
stem from passive context management. They introduce ARC, an Active and Reflection-driven
Context management framework that treats interaction memory as a dynamic internal state.
This module captures motivation, problem framing, and core claims.
"""

from gaia.lang import claim, setting, question

# --- Problem framing ---

deep_search_setting = setting(
    "Deep search and long-horizon information seeking are tasks where LLM-based agents must "
    "explore unfamiliar information spaces over many steps, repeatedly issue search queries, "
    "integrate heterogeneous evidence, and sustain coherent reasoning across extended "
    "interaction horizons (multi-step retrieval, evidence integration, decision making).",
    title="Deep search task setting",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

context_rot = claim(
    "LLM performance degrades in long-horizon settings: as interaction histories grow, "
    "models struggle to maintain coherent and task-relevant internal states. This phenomenon "
    "is termed *context rot* and has been attributed to long-term credit assignment failures, "
    "representational bottlenecks, and attention dilution in long contexts [@Hong2025].",
    title="Context rot phenomenon",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

raw_history_limitation = claim(
    "Directly appending raw interaction histories — including reasoning, actions, and observations — "
    "into the working context (e.g., ReAct-style agents) leads to rapid context growth and attention "
    "dilution, harming performance on long-horizon tasks [@Yao2023].",
    title="Raw history accumulation limitation",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

passive_summarization_limitation = claim(
    "Passive compression strategies that periodically summarize past interactions (e.g., ReSum) "
    "control context length but treat context as a static storage artifact rather than an actively "
    "maintained reasoning state. Once compressed, early errors, outdated assumptions, and misaligned "
    "emphasis are difficult to correct because prior summaries are rarely revisited [@Wu2025b].",
    title="Passive summarization limitation",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

passive_strategies_share_limitation = claim(
    "Both raw-history and passive-compression strategies share a common limitation: context is "
    "managed primarily to satisfy length constraints, not to evolve with the agent's understanding. "
    "Information once written is seldom reassessed in light of downstream reasoning outcomes.",
    title="Passive strategies share length-only focus",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

# --- Core perspective shift ---

active_management_view = claim(
    "Context should be treated as a dynamic internal state that can be continuously monitored and "
    "actively managed, rather than as an append-only record or a passively compressed summary. The "
    "challenge of long-horizon information seeking lies not only in deciding what to retain, but in "
    "enabling context to evolve as the agent's understanding changes.",
    title="Active management view (paper's central thesis)",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

# --- Research questions ---

q_active_management = question(
    "Can active, reflection-driven context management improve long-horizon information-seeking "
    "performance over passive accumulation or static summarization?",
    title="Q1: Does active context management help?",
)

q_learnable_cm = question(
    "Is context management a learnable capability that can be supervised independently of action "
    "generation, allowing a smaller trained Context Manager to outperform a larger untrained one?",
    title="Q2: Is the Context Manager learnable?",
)

q_management_frequency = question(
    "Does per-turn (always-on) context management outperform delayed or budget-triggered strategies?",
    title="Q3: Optimal context management frequency?",
)

# --- Contributions ---

contribution_perspective = claim(
    "The paper identifies a fundamental gap between *passive context compression* and *active "
    "context management* in long-horizon information-seeking agents, arguing that context "
    "management is not merely about fitting history into a limited window, but about continuously "
    "maintaining a task-aligned internal reasoning state.",
    title="Contribution 1: Passive vs active distinction",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

contribution_arc_framework = claim(
    "The paper proposes ARC (Active and Reflection-driven Context management), a framework that "
    "treats context as a dynamically managed internal state, enabling continuous revision and "
    "realignment during reasoning via always-on incremental summarization plus selectively "
    "triggered reflection.",
    title="Contribution 2: ARC framework",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

contribution_dual_architecture = claim(
    "The paper introduces a dual-component agent architecture with a dedicated Context Manager (CM), "
    "decoupled from action execution and responsible for online context construction and "
    "reflection-driven revision. The CM is reusable across different actor models.",
    title="Contribution 3: Dual-component architecture (Actor + CM)",
    metadata={"source": "artifacts/2601.12030.pdf, Section 1"},
)

__all__ = [
    "deep_search_setting",
    "context_rot",
    "raw_history_limitation",
    "passive_summarization_limitation",
    "passive_strategies_share_limitation",
    "active_management_view",
    "q_active_management",
    "q_learnable_cm",
    "q_management_frequency",
    "contribution_perspective",
    "contribution_arc_framework",
    "contribution_dual_architecture",
]
