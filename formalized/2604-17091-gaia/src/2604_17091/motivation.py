"""Introduction: Problem Statement and Core Thesis of GenericAgent"""

from gaia.lang import claim, setting, question, support, deduction

# ── Settings: background context ────────────────────────────────────────────

context_llm_agents = setting(
    "Large language model (LLM) agents such as Claude Code, OpenAI Codex, and OpenClaw "
    "are increasingly deployed as goal-directed systems that operate through terminals, "
    "file systems, browsers, and external tools — far beyond passive text generation.",
    title="LLM agents as action-taking systems",
)

context_long_horizon = setting(
    "Long-horizon agentic tasks require multi-step execution across many turns, "
    "where the agent must maintain coherent state, avoid re-exploring resolved choices, "
    "and accumulate and reuse experience across separate episodes.",
    title="Long-horizon agent challenge",
)

context_context_window = setting(
    "Current LLMs operate within a finite context window. "
    "The effective context length — the fraction of the window from which information "
    "can be reliably retrieved — is substantially smaller than the nominal window size.",
    title="Finite and effective context window constraint",
)

# ── Failure modes identified in prior work ───────────────────────────────────

failure_positional_bias = claim(
    "LLMs exhibit pronounced positional bias when processing long sequences: "
    "relevant information placed in the middle of the context is significantly harder "
    "to retrieve than information near the beginning or end [@LostInMiddle2023].",
    title="Positional bias in long contexts",
)

failure_attention_dilution = claim(
    "Irrelevant content in the context does not merely remain unused — it actively "
    "degrades performance by diverting attention away from decision-critical evidence. "
    "LLMs can be easily distracted by irrelevant context [@LostInMiddle2023].",
    title="Attention dilution from irrelevant content",
)

failure_effective_window = claim(
    "The effective context length of current LLMs falls far short of their nominal "
    "window size: part of the provided context is functionally inaccessible during "
    "generation [@EffectiveContext2024].",
    title="Effective context window shortfall",
)

failure_compounding = claim(
    "The three long-context failure modes — positional bias, attention dilution, and "
    "effective window shortfall — reinforce one another: as context grows, positional "
    "bias worsens, irrelevant content competes more strongly for attention, and the "
    "ratio of effective to nominal window length declines. Beyond a threshold, adding "
    "more context reduces rather than improves decision quality.",
    title="Compounding long-context failure modes",
)

# ── Experience reuse failure ─────────────────────────────────────────────────

failure_experience_reuse = claim(
    "Existing agent frameworks largely fail to accumulate and reuse experience across "
    "task episodes. Most treat each episode as stateless [@LifelongAgentBench2025]. "
    "Even when retrieval-augmented memory is introduced, it stores raw logs rather than "
    "distilled, reusable operational knowledge. Without feedback-driven refinement, "
    "stale or incorrect memories are never corrected, causing silent degradation. "
    "Token expenditure scales linearly with task count, yet effective capability remains "
    "flat — a stagnation loop with no return on accumulated interaction.",
    title="Experience accumulation and reuse failure in existing systems",
)

# ── Core thesis ───────────────────────────────────────────────────────────────

thesis_density = claim(
    "Long-horizon agent performance is determined not by context length, but by how "
    "much decision-relevant information is maintained within a finite context budget. "
    "Context information density — completeness × conciseness within the effective "
    "window — is the primary structural constraint for all LLM-based agent systems.",
    title="Context information density as primary constraint",
)

thesis_minimal_capability = claim(
    "Under the structural constraint of context information density, an agent framework "
    "needs to implement only three capabilities: (1) tool interfacing — keeping the "
    "action space deliberately minimal to avoid prompt overhead; (2) context management "
    "— actively filtering task state and tool outputs before they enter the context; "
    "(3) memory formation — retaining verified experience across episodes into reusable "
    "representations. Any additional complexity that does not serve one of these three "
    "is, in the authors' view, actively degrading information density.",
    title="Minimal complete capability set for agent systems",
)

thesis_token_efficiency = claim(
    "In long-horizon agentic settings, lower token consumption correlates with better "
    "task performance, not worse. An agent that consumes more tokens is more likely "
    "suffering from failures in context management — compensating for degraded per-step "
    "decision quality through additional interactions rather than improving it. "
    "Token consumption reflects the symptoms of context management quality.",
    title="Token consumption as symptom of context management quality",
)

thesis_minimal_architecture = claim(
    "Minimal architecture (a few thousand lines of core code) is a necessary prerequisite "
    "for autonomous agent self-evolution. A system with hundreds of thousands of lines "
    "of code is opaque to the agent — it can neither understand nor modify it. "
    "In a minimal codebase, subagents can read and modify the core code, making "
    "architectural self-update a practically achievable next step.",
    title="Minimal architecture as prerequisite for self-evolution",
)

# ── Research question ─────────────────────────────────────────────────────────

q_main = question(
    "How can a general-purpose LLM agent system be designed to maximize contextual "
    "information density across tool interfacing, context management, and memory "
    "formation, while remaining self-evolving and broadly capable?"
)

# ── Causal strategy: compounding failure → density as constraint ──────────────

strat_compounding = support(
    [failure_positional_bias, failure_attention_dilution, failure_effective_window],
    failure_compounding,
    reason=(
        "The three failure modes identified in prior work (@failure_positional_bias, "
        "@failure_attention_dilution, @failure_effective_window) are mutually reinforcing. "
        "Positional bias makes it harder to retrieve relevant facts as context grows; "
        "attention dilution means irrelevant content competes for model capacity; "
        "and effective window contraction means an increasing fraction of the prompt is "
        "wasted. Together, beyond a threshold, adding context actively harms performance "
        "[@LostInMiddle2023; @EffectiveContext2024]."
    ),
    prior=0.88,
)

strat_density_from_compounding = support(
    [failure_compounding, failure_experience_reuse],
    thesis_density,
    reason=(
        "Because @failure_compounding implies that context quality — not length — "
        "determines decision quality per step, and @failure_experience_reuse shows "
        "that without principled memory, each task starts from scratch at growing cost, "
        "the paper concludes that the binding constraint for long-horizon agents is "
        "how much decision-relevant information fits in the effective context window. "
        "This reframes agent design from 'extend context' to 'maximize density'."
    ),
    prior=0.85,
)

strat_minimal_from_density = deduction(
    [thesis_density],
    thesis_minimal_capability,
    reason=(
        "Given @thesis_density, each step in the agent execution pipeline either "
        "preserves or degrades information density. Tool interfacing determines "
        "interface overhead before execution begins; context management determines "
        "what enters the model per step; memory formation determines cross-episode "
        "reuse. These three are the only places where density is structurally degraded, "
        "so they are the minimal complete capability set [@GenericAgent2026]."
    ),
    prior=0.82,
)
