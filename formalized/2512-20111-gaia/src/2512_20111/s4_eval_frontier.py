"""Section 4: Evaluating Frontier Models with Belief Bottlenecks (prompting-only experiments)."""

from gaia.lang import claim, induction, setting, support

from .motivation import abbel_proposal, finding_belief_grows_slower, finding_failure_modes
from .s2_framework import (
    abbel_relies_on_sufficiency,
    abbel_two_call_loop,
    belief_prompting_definition,
    context_compression_property,
    vanilla_definition,
)

# --- Experimental setup ---

bg_six_environments = setting(
    "Six multi-step environments from Tajwar et al. (2025) [@Tajwar2025] are "
    "used: Wordle (5-letter word, $H=6$, complex reasoning, structured "
    "feedback), Mastermind (4-digit code, $H=12$, complex reasoning, structured "
    "feedback), Twenty Questions ($H=20$, ~$10^3$ topics), Guess My City "
    "($H=20$, ~$10^3$ cities), Murder Mystery ($H=20$, 3 suspects, free-form "
    "observations), and Customer Service ($H=20$, ~$10^2$ faulty parts, "
    "free-form observations).",
    title="Six evaluation environments (Table 3)",
)

bg_three_models = setting(
    "Three frontier models are evaluated zero-shot: Gemini 2.5 Pro, DeepSeek "
    "R1, and DeepSeek V3. For each model, three frameworks are compared: "
    "VANILLA (full history), BELIEF PROMPTING (history + belief), and ABBEL "
    "(belief only). Forty task instances are sampled per environment and "
    "success rate is reported with standard error of the mean.",
    title="Models and evaluation protocol",
)

# --- Performance findings: ABBEL on Gemini 2.5 Pro ---

obs_gemini_abbel_competitive = claim(
    "On Gemini 2.5 Pro, ABBEL maintains or exceeds the success rate of both "
    "VANILLA and BELIEF PROMPTING in most of the six environments, despite "
    "feeding the model only the belief at action time. Notably, on Murder "
    "Mystery, Gemini 2.5 Pro under ABBEL outperforms VANILLA — the authors "
    "attribute this to VANILLA being biased to keep gathering clues and run "
    "out of steps before making an accusation.",
    title="Gemini 2.5 Pro: ABBEL competitive or better (Fig. 2a)",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 2a",
        "caption": "Performance of frontier models across 6 environments under VANILLA, BELIEF PROMPTING, and ABBEL.",
    },
)

obs_deepseek_abbel_worse = claim(
    "On DeepSeek V3 and DeepSeek R1, ABBEL generally performs worse than both "
    "VANILLA and BELIEF PROMPTING, with the exception of Twenty Questions. The "
    "drop is most pronounced in environments with long, unstructured "
    "observations (Customer Service and Murder Mystery), where it is more "
    "ambiguous what information should be maintained in the belief.",
    title="DeepSeek models: ABBEL underperforms (Fig. 2a)",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 2a",
        "caption": "Performance of frontier models across 6 environments under VANILLA, BELIEF PROMPTING, and ABBEL.",
    },
)

obs_belief_prompting_rarely_helps = claim(
    "BELIEF PROMPTING (history + belief) rarely outperforms VANILLA and "
    "sometimes substantially decreases performance. Adding a belief on top of "
    "the full history does not, in their experiments, reliably improve action "
    "quality.",
    title="BELIEF PROMPTING does not reliably improve over VANILLA",
)

# --- Compactness findings ---

obs_belief_lengths_short = claim(
    "Beyond the first few steps, ABBEL belief lengths are significantly shorter "
    "than the corresponding interaction history across all six environments and "
    "all three frontier models, with belief lengths often plateauing or "
    "decreasing. The exception is Gemini 2.5 Pro on Twenty Questions and Guess "
    "My City, where Gemini concatenates all observations into the belief, "
    "causing linear growth.",
    title="ABBEL belief lengths grow much slower than histories (Fig. 2b)",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 2b",
        "caption": "Average length of beliefs generated under ABBEL compared to full histories across 6 environments and 3 models.",
    },
)

# --- Lift the empirical observations to the introduction-level finding ---

# Treat the introduction's claim that belief lengths stay manageable as an
# induction over multiple environment-model pairs (Wordle/Mastermind under
# Gemini, Customer Service under DeepSeek R1, etc.). Use two representative
# observations as the basis.

s_compress_general_from_short = support(
    [finding_belief_grows_slower],
    obs_belief_lengths_short,
    reason=(
        "@finding_belief_grows_slower is the general law that ABBEL beliefs "
        "grow slower than the history; @obs_belief_lengths_short is the "
        "specific Fig. 2b realization across the six environments. The law "
        "predicts the observation."
    ),
    prior=0.92,
)

s_compress_general_from_compress = support(
    [finding_belief_grows_slower],
    context_compression_property,
    reason=(
        "@finding_belief_grows_slower predicts that the structural property "
        "@context_compression_property holds in practice — when belief lengths "
        "grow slower than histories, ABBEL achieves the context compression "
        "the framework promises."
    ),
    prior=0.92,
)

ind_compress = induction(
    s_compress_general_from_short,
    s_compress_general_from_compress,
    law=finding_belief_grows_slower,
    reason=(
        "Two distinct measurements support the law that ABBEL beliefs are "
        "compact: (i) direct token-count plots in Fig. 2b across 6 envs "
        "(@obs_belief_lengths_short), and (ii) the structural compression "
        "property realized in practice (@context_compression_property)."
    ),
)

# --- Failure modes (Section 4.3 final paragraphs) ---

fm_uninformative_repeats = claim(
    "When the agent receives an uninformative observation (e.g., Customer "
    "Service: customer says 'I'm not sure'), ABBEL often does not update the "
    "belief, and at the next step the action prompt produces the same action "
    "again because the belief input is unchanged. VANILLA, which sees the "
    "previous action in $h_t$, is much less likely to repeat an uninformative "
    "action.",
    title="Failure mode: repeated actions after uninformative observations",
)

fm_belief_error_propagation = claim(
    "In environments requiring complex reasoning (Wordle, Mastermind), errors "
    "in the belief introduced at step $t$ (e.g., falsely assuming the secret "
    "code cannot contain repeated characters) propagate to subsequent steps "
    "because the action context contains only the current belief. Self-correction "
    "is possible only after a contradicting observation, and the wasted turns "
    "may be irrecoverable. With access to the full history, error detection and "
    "exact posterior reconstruction are easier.",
    title="Failure mode: belief error propagation",
)

fm_hallucinated_memories = claim(
    "ABBEL agents sometimes hallucinate false memories of past interactions "
    "into the belief — recalling actions or observations that never occurred — "
    "which then misdirect subsequent action selection.",
    title="Failure mode: hallucinated past interactions",
)

# Connect the three failure-mode observations to the introduction-level claim.
# Use induction (multiple independent failure-mode observations) over the law.

s_fm_repeat = support(
    [finding_failure_modes],
    fm_uninformative_repeats,
    reason="@finding_failure_modes (general law of ABBEL prompting failures) predicts the specific @fm_uninformative_repeats observation.",
    prior=0.9,
)

s_fm_err_prop = support(
    [finding_failure_modes],
    fm_belief_error_propagation,
    reason="@finding_failure_modes predicts the specific belief-error-propagation failure mode @fm_belief_error_propagation observed in Wordle/Mastermind traces.",
    prior=0.9,
)

s_fm_hallucinate = support(
    [finding_failure_modes],
    fm_hallucinated_memories,
    reason="@finding_failure_modes predicts the specific hallucinated-memory failure mode @fm_hallucinated_memories observed in trace inspection.",
    prior=0.9,
)

ind_fm_pair = induction(
    s_fm_repeat,
    s_fm_err_prop,
    law=finding_failure_modes,
    reason="Two independent observations of distinct failure modes (uninformative-action repetition and belief-error propagation) support the general law.",
)

ind_failure_modes = induction(
    ind_fm_pair,
    s_fm_hallucinate,
    law=finding_failure_modes,
    reason="A third independent failure-mode observation (hallucinated past interactions) further supports the general law that ABBEL prompting-only has characteristic failure modes.",
)

# --- Section 4.3 secondary observation about reasoning length ---

obs_reasoning_reduction = claim(
    "Conditioning on belief states (under ABBEL or BELIEF PROMPTING) rather "
    "than on full histories significantly reduces the chain-of-thought "
    "reasoning length used at action selection, with ABBEL using even less "
    "reasoning than BELIEF PROMPTING while achieving similar success rates in "
    "several environments.",
    title="Belief bottleneck reduces unnecessary CoT reasoning",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 6 (Appendix C)",
        "caption": "Reasoning length reduction with belief conditioning.",
    },
)

# --- Connect the failure-mode finding to ABBEL prompting limitations ---

prompting_only_inadequate = claim(
    "Prompting-only ABBEL is inadequate for several model–environment pairs: "
    "for each frontier model evaluated, there exists at least one environment "
    "where ABBEL underperforms full-context baselines, motivating the need "
    "for RL fine-tuning to fix belief-update errors.",
    title="Prompting-only ABBEL is insufficient (motivates RL)",
)

strat_prompting_inadequate = support(
    [obs_deepseek_abbel_worse, finding_failure_modes, abbel_relies_on_sufficiency],
    prompting_only_inadequate,
    reason=(
        "@obs_deepseek_abbel_worse documents that ABBEL underperforms on "
        "DeepSeek models, and even Gemini fails on Mastermind. The failure-mode "
        "law @finding_failure_modes (belief errors propagate, uninformative "
        "observations cause action repetition, false memories occur) explains "
        "the underperformance, given the framework's reliance on sufficient "
        "belief updating @abbel_relies_on_sufficiency. Together these establish "
        "that prompting alone is not enough and motivate the RL methods of "
        "Section 5."
    ),
    prior=0.92,
)

# --- Connect remaining observations into the graph ---

# Gemini-competitive and BELIEF-PROMPTING-rarely-helps observations both
# inform the framework's value claim @abbel_proposal: ABBEL is a viable
# framework. (Used as background to keep abbel_proposal a claim while
# bringing these observations into the BP graph.)

# The prompting-only inadequacy is a synthesis: include the Gemini-positive
# evidence as a counter-pull to keep the claim balanced.
strat_gemini_supports_framework = support(
    [obs_gemini_abbel_competitive, obs_belief_prompting_rarely_helps, belief_prompting_definition],
    abbel_proposal,
    reason=(
        "Gemini 2.5 Pro maintaining competitive performance under ABBEL "
        "(@obs_gemini_abbel_competitive) and BELIEF PROMPTING failing to "
        "reliably improve over VANILLA (@obs_belief_prompting_rarely_helps) "
        "— where BELIEF PROMPTING is the ablation that retains both belief "
        "and full history (@belief_prompting_definition) — together support "
        "the framing of ABBEL as a meaningful design: the history-removing "
        "bottleneck is the load-bearing element, not the addition of a "
        "belief on top of full history."
    ),
    prior=0.85,
)

strat_reasoning_reduction = support(
    [abbel_two_call_loop],
    obs_reasoning_reduction,
    reason=(
        "@abbel_two_call_loop conditions action selection on a compact belief "
        "rather than full history, which empirically reduces the chain-of-thought "
        "reasoning length the model produces (Fig. 6, Appendix C) — fewer "
        "history tokens to reason over means less unnecessary CoT."
    ),
    prior=0.85,
)

__all__ = [
    "bg_six_environments",
    "bg_three_models",
    "obs_gemini_abbel_competitive",
    "obs_deepseek_abbel_worse",
    "obs_belief_prompting_rarely_helps",
    "obs_belief_lengths_short",
    "fm_uninformative_repeats",
    "fm_belief_error_propagation",
    "fm_hallucinated_memories",
    "obs_reasoning_reduction",
    "prompting_only_inadequate",
    "ind_compress",
    "ind_failure_modes",
    "strat_prompting_inadequate",
    "strat_gemini_supports_framework",
    "strat_reasoning_reduction",
]
