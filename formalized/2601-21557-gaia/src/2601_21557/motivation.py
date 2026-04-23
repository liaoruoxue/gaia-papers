"""Introduction and Motivation: Context Engineering and Its Limitations"""

from gaia.lang import claim, setting, question, support, deduction, contradiction

# ── Settings ──────────────────────────────────────────────────────────────────

setup_llm_context = setting(
    "Large language model (LLM) efficacy at inference time is governed by the "
    "curation and orchestration of the inference-time context supplied to the model.",
    title="LLM inference-time context governs efficacy",
)

setup_ce_discipline = setting(
    "Context Engineering (CE) is defined as the discipline of principled LLM context "
    "optimization to maximize downstream utility and enable continuous self-improvement. "
    "CE methods optimize what is placed in the context window rather than model weights.",
    title="Context Engineering discipline definition",
)

setup_ce_advantages = setting(
    "Optimizing LLM context (rather than model parameters) has four structural advantages: "
    "(1) **Interpretability** — experience is encoded in natural language rather than opaque weights; "
    "(2) **Efficiency** — rapid deployment without costly parameter updates; "
    "(3) **Modularity** — composition and transfer of established contexts; "
    "(4) **Robustness** — immunity to catastrophic forgetting by decoupling capability "
    "acquisition from model weights.",
    title="CE advantages over parameter optimization",
)

# ── Claims ────────────────────────────────────────────────────────────────────

ce_bias_trajectory = claim(
    "Case-based trajectory context representations retain rich episodic traces but lack "
    "generalization and abstraction across tasks [@Mei2025].",
    title="Trajectory context: rich but lacks generalization",
)

ce_bias_list = claim(
    "Itemized-list context representations accumulate abstract insights but remain flat "
    "and structurally inexpressive, limiting their representational power [@Mei2025].",
    title="List context: abstract but structurally flat",
)

ce_bias_graph = claim(
    "Graph-based hierarchical memory context representations offer flexible organization but "
    "incur high latency and complexity without consistently outperforming naive retrieval [@Mei2025].",
    title="Graph context: flexible but high latency",
)

ce_brevity_bias = claim(
    "Prompt-rewriting CE approaches such as GEPA [@Agrawal2025] favor brevity by producing "
    "concise, high-level rules (typically 1–2K tokens) that fail for tasks requiring detailed "
    "strategies and deep domain knowledge.",
    title="GEPA brevity bias",
)

ce_bloat_bias = claim(
    "Additive-curation CE approaches such as Dynamic Cheatsheet (DC) [@Suzgun2025] and "
    "Agentic Context Engineering (ACE) [@Zhang2026] orchestrate modular agents to iteratively "
    "perform on-policy rollouts, textual reflections, and context updates. These suffer from "
    "structural rigidity and context bloat (ACE reaches up to 80K tokens after 5 epochs).",
    title="ACE/DC context bloat bias",
)

no_universal_harness = claim(
    "No single manually crafted agentic harness for context engineering is universally optimal "
    "across task domains. Different tasks benefit from different context representations "
    "and optimization procedures.",
    title="No universal CE harness",
)

strat_no_universal = support(
    [ce_bias_trajectory, ce_bias_list, ce_bias_graph, ce_brevity_bias, ce_bloat_bias],
    no_universal_harness,
    reason=(
        "Each existing context representation has characteristic trade-offs "
        "(@ce_bias_trajectory, @ce_bias_list, @ce_bias_graph), and each optimization strategy "
        "also exhibits opposing biases (@ce_brevity_bias, @ce_bloat_bias). "
        "The co-existence of these distinct failure modes implies that no single design is universally optimal."
    ),
    prior=0.88,
)

# Research question
q_meta_ce = question(
    "Can a bi-level framework that co-evolves context engineering skills and context artifacts "
    "overcome the inductive biases of fixed agentic harnesses and achieve superior, "
    "task-adaptive context optimization?",
    title="Research question: can bi-level skill evolution overcome CE biases?",
)

# ── Contradictions ────────────────────────────────────────────────────────────

not_both_brevity_bloat = contradiction(
    ce_brevity_bias,
    ce_bloat_bias,
    reason=(
        "Brevity bias (GEPA produces ~1-2K tokens) and context bloat bias (ACE produces ~80K tokens) "
        "are opposing failure modes — a method cannot simultaneously err towards both extremes."
    ),
    prior=0.97,
)
