"""Introduction: LLM Self-Awareness and the Gnosis Mechanism"""

from gaia.lang import claim, setting, question, support, complement, contradiction

# ── Background / Settings ──────────────────────────────────────────────────────

llm_fluency = setting(
    "Large language models (LLMs) generate fluent and complex outputs "
    "but frequently produce hallucinations — plausible-sounding but incorrect responses.",
    title="LLM fluency vs. hallucination problem",
)

existing_approaches = setting(
    "Existing approaches to LLM correctness verification include: "
    "(1) external judge models that score outputs post-hoc, "
    "(2) multi-sample consistency methods (e.g., self-consistency sampling), and "
    "(3) text-based self-critique where the model reflects on its own outputs. "
    "All three categories rely on additional inference calls or external scoring models.",
    title="Existing verification approach categories",
)

internal_state_def = setting(
    "During LLM inference, each token generation produces hidden states (activations at each transformer layer) "
    "and attention patterns (L x H attention maps, where L is the number of layers and H is the number of heads). "
    "These internal traces are generated as a byproduct of inference and require no extra computation to observe.",
    title="LLM internal states during inference",
)

# ── Research Question ──────────────────────────────────────────────────────────

research_question = question(
    "Can LLMs predict their own failures by inspecting internal states (hidden states "
    "and attention patterns) produced during inference, without external supervision?",
    title="Core research question",
)

# ── Core Claims (Introduction) ─────────────────────────────────────────────────

external_judge_weakness = claim(
    "External judge approaches to LLM correctness verification incur additional computational cost "
    "and often correlate weakly with true correctness. Specifically, large external judges such as "
    "Gemini 2.5 Pro (proprietary, multi-billion parameters) require full sequence processing, "
    "and open-source reward models such as Skywork-Reward-8B require 930ms latency for 12k-token responses "
    "and 2465ms for 24k-token responses.",
    title="External judge computational and accuracy limitations",
    metadata={"source_section": "Introduction, Section 1"},
)

multi_sample_weakness = claim(
    "Multi-sample consistency approaches (e.g., self-consistency sampling) require generating "
    "multiple completions per prompt, multiplying inference cost proportionally to the number of samples. "
    "They also correlate weakly with per-instance correctness when the model is confidently wrong across samples.",
    title="Multi-sample consistency limitations",
    metadata={"source_section": "Introduction, Section 1"},
)

text_critique_weakness = claim(
    "Text-based self-critique (asking the LLM to reflect on its own outputs) correlates weakly "
    "with true correctness because the surface-level verbalized confidence of LLMs is poorly calibrated: "
    "models can express high confidence while being factually wrong.",
    title="Text-based self-critique limitations",
    metadata={"source_section": "Introduction, Section 1"},
)

internal_cues_exist = claim(
    "Reliable correctness cues are intrinsic to the LLM generation process and are encoded in "
    "hidden states and attention patterns, meaning these internal signals can discriminate correct "
    "from incorrect outputs without external supervision.",
    title="Internal correctness cues hypothesis",
    metadata={"source_section": "Introduction, Abstract"},
)

gnosis_proposal = claim(
    "Gnosis is a lightweight (~5 million parameters) self-awareness mechanism that enables frozen LLMs "
    "to perform intrinsic self-verification by decoding signals from hidden states and attention patterns. "
    "Gnosis passively observes internal traces, compresses them into fixed-budget descriptors, and predicts "
    "correctness with negligible inference overhead (~25ms constant latency, independent of sequence length), "
    "adding only ~5M parameters on top of any frozen backbone LLM.",
    title="Gnosis mechanism proposal",
    metadata={"source_section": "Introduction, Abstract"},
)

# ── Strategy: The gap between existing approaches motivates internal inspection ─

strat_motivation = support(
    [external_judge_weakness, multi_sample_weakness, text_critique_weakness],
    internal_cues_exist,
    reason=(
        "All three existing approaches—external judges (@external_judge_weakness), "
        "multi-sample consistency (@multi_sample_weakness), and text-based self-critique "
        "(@text_critique_weakness)—have fundamental weaknesses: they incur extra compute or "
        "correlate weakly with true correctness. This motivates the hypothesis that reliable "
        "correctness signals must lie elsewhere—specifically in the internal representations "
        "that the model computes during generation, which are free to observe."
    ),
    prior=0.72,
)

# ── Complementary framing: internal vs. external ──────────────────────────────

strat_gnosis_addresses = support(
    [internal_cues_exist],
    gnosis_proposal,
    reason=(
        "If reliable correctness cues are encoded in internal states (@internal_cues_exist), "
        "then a lightweight probe trained to read these cues can serve as a self-verifier. "
        "Gnosis is proposed as the concrete realization of this idea: a ~5M-parameter head "
        "that operates on hidden states and attention patterns without modifying or re-running the backbone."
    ),
    prior=0.85,
)
