"""Section 2: Technical Overview — POMDP setup and the Belief Bottleneck Interaction Framework."""

from gaia.lang import claim, setting, support

# --- Mathematical/formal setup ---

bg_pomdp = setting(
    "Each environment is modeled as a Partially Observable Markov Decision "
    "Process (POMDP). At each step $t$ the hidden state $s_t$ is updated to "
    "$s_{t+1}$ by the action $a_t$ via the transition function $T$, and the "
    "agent receives reward $r_t$ and observation $o_t$ both conditioned on "
    "$a_t$ and $s_t$. The agent does not observe $s_t$ directly.",
    title="POMDP problem setup",
)

bg_wordle_example = setting(
    "Wordle is the running example: the secret 5-letter word is the hidden "
    "initial state $s_0$, the action $a_t$ is a 5-letter English word guess, "
    "the observation $o_t$ is per-letter feedback (absent / present elsewhere / "
    "correct position), reward is 1 if the word was guessed within 6 turns and "
    "0 otherwise, and the horizon is $H = 6$.",
    title="Wordle as concrete POMDP instance",
)

bg_lm_policy = setting(
    "A context-conditioned LLM policy $\\pi(\\cdot \\mid c_t)$ samples the next "
    "token sequence (an action or a belief update) from a fixed pretrained "
    "language model conditioned on context $c_t$.",
    title="LLM policy notation",
)

# --- VANILLA baseline (definition) ---

vanilla_definition = claim(
    "The standard multi-step paradigm (VANILLA) selects actions conditioned on "
    "the full interaction history: $a_t \\sim \\pi(\\cdot \\mid p_I, h_t, p_a)$, "
    "where $p_I$ is the instructions prompt, $h_t = \\langle a_1, o_2, a_2, "
    "o_3, \\ldots, a_{t-1}, o_{t-1}\\rangle$ is the full history, and $p_a$ is "
    "the action-selection prompt. The context length therefore grows linearly "
    "with the number of interaction steps.",
    title="VANILLA: full-history baseline",
)

# --- ABBEL framework (definition + key derived property) ---

abbel_two_call_loop = claim(
    "ABBEL calls the LLM twice per step: (1) Belief update — sample a new "
    "belief $b_t \\sim \\pi(\\cdot \\mid p_I, b_{t-1}, a_{t-1}, o_{t-1}, p_b)$ "
    "from the previous belief, action, observation, and a belief-update prompt "
    "$p_b$; (2) Action selection — sample an action $a_t \\sim \\pi(\\cdot \\mid "
    "p_I, b_t, p_a)$ conditioned only on the new belief and the action prompt "
    "$p_a$. The full interaction history $h_t$ is *not* in the action-selection "
    "context.",
    title="ABBEL alternates belief update and action selection",
)

belief_prompting_definition = claim(
    "BELIEF PROMPTING is an ablation of ABBEL that performs the belief-update "
    "call as in ABBEL but conditions action selection on *both* the belief and "
    "the full interaction history $h_t$. This isolates the effect of the "
    "history-removing bottleneck from the effect of belief generation.",
    title="BELIEF PROMPTING ablation",
)

context_compression_property = claim(
    "When the belief-state length $|b_t|$ is significantly shorter than the "
    "history length $|h_t|$, ABBEL successfully reduces the context length the "
    "agent must process at action-selection time, and the per-step context cost "
    "becomes near-constant rather than linear in $t$.",
    title="ABBEL context-length reduction property",
)

strat_compression_property = support(
    [vanilla_definition, abbel_two_call_loop],
    context_compression_property,
    reason=(
        "By construction, VANILLA's action-selection context contains $h_t$ "
        "(@vanilla_definition), whose length grows linearly in $t$. ABBEL's "
        "action-selection context contains only $b_t$ (@abbel_two_call_loop). "
        "If $|b_t| \\ll |h_t|$, ABBEL's per-step action-selection context is "
        "much smaller, making the property a direct consequence of the "
        "framework definitions (modulo the empirical question of whether "
        "belief lengths actually stay short, addressed in Section 4)."
    ),
    prior=0.95,
    background=[bg_pomdp, bg_lm_policy],
)

# --- Reliance on language-model capacity for sufficient summarization ---

abbel_relies_on_sufficiency = claim(
    "ABBEL's correctness depends on the LLM's ability to propagate sufficient "
    "task-relevant information from $b_{t-1}, a_{t-1}, o_{t-1}$ into $b_t$ "
    "while discarding superfluous details. If the model fails to maintain "
    "sufficient information, action quality at step $t$ degrades because the "
    "lost information is irrecoverable from the bottlenecked context.",
    title="ABBEL relies on sufficient belief updating",
)

strat_relies_on_sufficiency = support(
    [abbel_two_call_loop],
    abbel_relies_on_sufficiency,
    reason=(
        "By @abbel_two_call_loop, the action-selection step $t$ has access only "
        "to the most recent belief $b_t$, not to prior actions, observations, "
        "or beliefs. Therefore any task-relevant information that did not get "
        "carried into $b_t$ is irrecoverable at action time. Whether the LLM "
        "succeeds in propagating sufficient information is an empirical "
        "question — the architectural risk is implied directly by the framework "
        "definition."
    ),
    prior=0.95,
)

__all__ = [
    "bg_pomdp",
    "bg_wordle_example",
    "bg_lm_policy",
    "vanilla_definition",
    "abbel_two_call_loop",
    "belief_prompting_definition",
    "context_compression_property",
    "abbel_relies_on_sufficiency",
    "strat_compression_property",
    "strat_relies_on_sufficiency",
]
