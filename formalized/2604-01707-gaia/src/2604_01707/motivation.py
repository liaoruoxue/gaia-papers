"""Introduction and Motivation"""

from gaia.lang import (
    claim, setting, question,
    support, deduction,
    contradiction, complement,
)

# ── Research context ──────────────────────────────────────────────────────────

setting_llm_agents = setting(
    "Large Language Model (LLM)-based agents use an LLM as the core decision model "
    "for sequential action selection. They operate in a closed loop: receive observation, "
    "perform reasoning/planning, execute an action (possibly via tools), obtain feedback, "
    "and proceed to the next step. The action space includes natural-language responses and "
    "structured tool calls.",
    title="LLM-based agents definition",
)

setting_context_window = setting(
    "LLMs condition only on a bounded context window (limited number of tokens). "
    "Information from earlier turns outside the current prompt can be lost. "
    "This degrades performance in long-horizon dialogue and multi-session tasks.",
    title="Context window limitation",
)

setting_prompting = setting(
    "LLM prompting specifies a task by constructing an input context (prompt) containing "
    "task instructions, the current input, and optionally demonstrations or auxiliary evidence. "
    "Prompting is a lightweight, training-free interface for task adaptation.",
    title="LLM prompting definition",
)

# ── Core problem and motivation ───────────────────────────────────────────────

problem_stateless = claim(
    "Without memory, LLM-based agents operate statelessly: they cannot accumulate experience "
    "over time, maintain contextual knowledge across sessions, or make informed decisions that "
    "depend on long-term context. This leads to context overflow, high token costs, high latency, "
    "and unreliable behavior in long-horizon tasks such as multi-turn dialogue, game playing, "
    "and scientific discovery.",
    title="Stateless agent problem",
    background=[setting_context_window],
)

memory_enables = claim(
    "Memory mechanisms allow LLM-based agents to move beyond naive long-context prompting by "
    "maintaining and leveraging relevant information from past interactions. By equipping agents "
    "with memory, they can accumulate experience over time, maintain contextual knowledge, "
    "and make more informed decisions — analogous to how humans rely on memory to learn from "
    "past experiences and guide future actions. Memory-augmented prompting is more token-efficient, "
    "lower-latency, and more reliable than naive long-context prompting.",
    title="Memory as core agent module",
    background=[setting_context_window, setting_llm_agents],
)

strat_mem_motivation = support(
    [problem_stateless],
    memory_enables,
    reason=(
        "The stateless failure mode (@problem_stateless) directly motivates memory augmentation: "
        "an explicit memory module persists interaction-derived information (user preferences, "
        "salient events, intermediate decisions, task constraints) and reintroduces it when relevant, "
        "thereby restoring the contextual continuity lost due to bounded context windows."
    ),
    prior=0.95,
)

# ── Gap in the literature ─────────────────────────────────────────────────────

gap_no_unified_framework = claim(
    "Before this work, there was no unified framework for abstracting and systematically analyzing "
    "agent memory methods. Existing methods were categorized under different dimensions across different "
    "papers, making systematic comparison difficult.",
    title="Gap: no unified framework",
)

gap_no_comprehensive_comparison = claim(
    "Before this work, most memory studies reported overall performance results but rarely examined "
    "the roles and effects of individual components within methods. Comprehensive and systematic "
    "comparisons among different methods — especially regarding accuracy and efficiency — were lacking.",
    title="Gap: no systematic comparison",
)

gap_no_sota_analysis = claim(
    "Before this work, no study had conducted a systematic in-depth analysis covering token cost "
    "efficiency, context scalability, evidence position sensitivity, and LLM backbone dependence "
    "for agent memory methods under the same experimental settings.",
    title="Gap: missing multi-dimensional analysis",
)

# ── Memory vs RAG distinction ─────────────────────────────────────────────────

setting_memory_vs_rag = setting(
    "Memory and Retrieval-Augmented Generation (RAG) are related but distinct mechanisms. "
    "Memory primarily targets stateful, interaction-dependent information that evolves over time "
    "and is required for personalization and cross-session continuity. RAG primarily targets external "
    "knowledge grounding, retrieving evidence from document collections or knowledge bases to supplement "
    "domain knowledge and reduce hallucinations. In practice, they are complementary.",
    title="Memory vs RAG distinction",
)

# ── Research questions ────────────────────────────────────────────────────────

q_unified_framework = question(
    "Can a unified modular framework decompose all representative agent memory methods into "
    "comparable components?",
    title="Q: Unified framework",
)

q_which_method_best = question(
    "Which agent memory method achieves the best performance on long-term conversational benchmarks, "
    "and what design choices drive that performance?",
    title="Q: Best method",
)

q_new_sota = question(
    "Can insights from systematic comparison guide the design of a new memory method that "
    "outperforms all existing state-of-the-art methods?",
    title="Q: New SOTA method",
)
