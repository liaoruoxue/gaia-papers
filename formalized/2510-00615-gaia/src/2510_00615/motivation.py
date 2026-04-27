"""Motivation: long-horizon LLM agents accumulate unbounded context.

Section 1 (Introduction) of ACON [@Trivedi2024 not used here; the introduction
itself sets up the problem of unbounded context growth in long-horizon agents].
"""

from gaia.lang import claim, setting

# Background formal setup ----------------------------------------------------

agent_loop_setup = setting(
    "An LLM agent interacts with a Partially Observable Markov Decision Process "
    "(POMDP) environment $E = \\langle S, A, O, T, R \\rangle$. At each step $t$ the "
    "agent receives the latest observation $o_t$ together with the interaction "
    "history $h_{t-1} = (o_0, a_0, o_1, a_1, \\dots, o_{t-1}, a_{t-1})$ and emits "
    "action $a_t = M(o_t, h_{t-1}; \\theta, P_{agent})$ where $\\theta$ are the "
    "fixed model parameters and $P_{agent}$ is the (static) system prompt.",
    title="Agent loop formal setup",
)

context_cost_definition = setting(
    "The per-task context cost $C(H) = \\sum_{t=1}^{T} C(h_{t-1}, o_t)$ aggregates "
    "the per-step cost of encoding the dynamic context (history $h_{t-1}$ plus "
    "latest observation $o_t$). The static prompt cost is excluded because it can "
    "be budgeted in advance.",
    title="Context cost function (Equation 2)",
)

# Empirical observations / framing claims ------------------------------------

context_grows_unbounded = claim(
    "In long-horizon agentic tasks the interaction history $h_{t-1}$ grows "
    "unboundedly with the number of steps because every action and observation is "
    "appended to the running history.",
    title="Context grows unbounded with horizon",
)

cost_scales_with_context = claim(
    "Transformer inference cost scales (super-linearly through attention) with the "
    "input token count $n$, so per-step cost rises as the history length grows. "
    "Combined with @context_grows_unbounded this makes naive long-horizon agent "
    "rollouts prohibitively expensive.",
    title="Inference cost scales with context length",
)

long_context_distracts = claim(
    "Excessively long contexts dilute relevant information and distract the model "
    "with outdated or extraneous details, lowering downstream accuracy "
    "[@Shi2023].",
    title="Long context distracts the model",
)

heuristics_inadequate = claim(
    "Existing context-management heuristics fall short for long-horizon multi-step "
    "agents: dialogue summarisation targets conversational coherence but loses "
    "multi-step carry-over; document-centric methods (long-context QA, in-context "
    "learning) assume single-step reasoning where context can be discarded after "
    "the answer; FIFO truncation drops potentially load-bearing facts; retrieval "
    "fetches fragments but loses structural state. None of them preserve the "
    "diverse signal types (causal relations, evolving state, preconditions, "
    "decision cues) that productivity agents require.",
    title="Existing heuristics inadequate for long-horizon agents",
)

# Headline contributions of ACON ---------------------------------------------

acon_compresses_history_and_obs = claim(
    "ACON (Agent Context Optimization) is a unified framework that compresses "
    "**both** environment observations and interaction histories into concise but "
    "informative condensations, applied selectively only when the corresponding "
    "length exceeds a threshold ($T_{hist}$ for history, $T_{obs}$ for "
    "observation).",
    title="ACON compresses both history and observation",
)

acon_is_gradient_free = claim(
    "ACON's compression-guideline optimisation operates entirely in natural "
    "language space (no parameter updates of the compressor LLM are required), "
    "making it directly applicable to closed-source / API-only models.",
    title="ACON is gradient-free",
)

acon_distillable = claim(
    "The optimised compressor (a large LLM with the tuned guideline) can be "
    "distilled into a smaller compressor LLM while retaining most of the teacher's "
    "downstream agent accuracy, lowering deployment cost.",
    title="ACON's compressor is distillable",
)

# Headline empirical claims (proven in Section 4) ----------------------------

claim_peak_token_reduction = claim(
    "ACON reduces peak input tokens by **26-54%** across AppWorld, OfficeBench "
    "and 8-objective QA while largely preserving (and sometimes improving) task "
    "accuracy when paired with a strong agent (gpt-4.1).",
    title="Headline: 26-54% peak-token reduction",
)

claim_distillation_preserves_accuracy = claim(
    "When ACON's optimised compressor (gpt-4.1 teacher) is distilled into "
    "smaller models (Qwen3-14B, Qwen3-8B, Phi-4), the student compressors retain "
    "**over 95%** of the teacher compressor's downstream agent accuracy.",
    title="Headline: distillation preserves >=95% accuracy",
)

claim_helps_small_agents = claim(
    "ACON acts as an equaliser for smaller LLM agents: with concise but "
    "informative contexts, Qwen3-14B improves by up to **+32%** on AppWorld, "
    "**+20%** on OfficeBench and **+46%** on 8-objective QA versus the "
    "no-compression baseline.",
    title="Headline: small LM agents benefit most",
)

__all__ = [
    "agent_loop_setup",
    "context_cost_definition",
    "context_grows_unbounded",
    "cost_scales_with_context",
    "long_context_distracts",
    "heuristics_inadequate",
    "acon_compresses_history_and_obs",
    "acon_is_gradient_free",
    "acon_distillable",
    "claim_peak_token_reduction",
    "claim_distillation_preserves_accuracy",
    "claim_helps_small_agents",
]
