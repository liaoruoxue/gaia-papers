"""Section 2: Background and Related Work"""

from gaia.lang import claim, setting, support
from .motivation import (
    external_judge_weakness,
    multi_sample_weakness,
    text_critique_weakness,
    internal_cues_exist,
)

# ── Settings / Background ──────────────────────────────────────────────────────

verbalized_confidence_setting = setting(
    "Verbalized confidence methods prompt LLMs to produce a numeric probability or qualitative "
    "uncertainty estimate alongside their answer. These probabilities are read from token logits "
    "or explicitly elicited via prompting, e.g., asking the model 'How confident are you?'",
    title="Verbalized confidence elicitation definition",
)

internal_probe_setting = setting(
    "Internal probe methods train a lightweight classifier (e.g., linear probe or MLP) on "
    "intermediate hidden states of an LLM, typically using the final token's last-layer representation, "
    "to predict correctness without re-running the backbone.",
    title="Internal probe methods definition",
)

chain_of_embedding_setting = setting(
    "Chain-of-Embedding (CoE) is a trajectory-based method that applies singular value decomposition (SVD) "
    "to the sequence of hidden state vectors produced during generation, capturing spectral features "
    "of the generation trajectory to detect hallucination.",
    title="Chain-of-Embedding method definition",
)

reward_model_setting = setting(
    "Reward models (RMs) are models fine-tuned on human preference data to assign scalar quality scores "
    "to model outputs. They are typically applied as external judges post-hoc after generation completes, "
    "and scale linearly with output sequence length in inference cost.",
    title="Reward model definition",
)

# ── Claims about Related Work Limitations ──────────────────────────────────────

verbalized_conf_weakness = claim(
    "Verbalized confidence methods are poorly calibrated: LLMs frequently express high confidence "
    "on incorrect answers and low confidence on correct ones. Studies find weak correlation between "
    "verbalized probabilities and true answer correctness, especially for factual questions where "
    "the model has memorized incorrect information [@Xiong2024].",
    title="Verbalized confidence calibration failure",
    metadata={"source_section": "Section 2, Related Work"},
)

internal_probe_weakness = claim(
    "Simple internal probe methods (e.g., MLP on the final hidden state) capture only a snapshot "
    "of model state at one position and one layer, missing the temporal dynamics of reasoning trajectories "
    "and cross-layer/cross-head attention structure. This limits their discriminative power relative "
    "to methods that aggregate across the full generation.",
    title="Simple internal probe limitation",
    metadata={"source_section": "Section 2, Related Work"},
)

chain_of_embedding_weakness = claim(
    "Chain-of-Embedding (CoE) — which applies SVD to the sequence of hidden states — captures "
    "trajectory structure but uses unsupervised spectral decomposition without task-specific "
    "supervision. This limits its ability to learn the specific discriminative features that "
    "separate correct from incorrect responses in a task-adaptive manner.",
    title="Chain-of-Embedding limitation",
    metadata={"source_section": "Section 2, Related Work"},
)

reward_model_cost = claim(
    "External reward models (e.g., Skywork-Reward-8B) require 930ms latency for 12,000-token responses "
    "and 2,465ms for 24,000-token responses, scaling linearly with sequence length. This makes them "
    "impractical for real-time or high-throughput inference pipelines.",
    title="Reward model latency scaling",
    metadata={"source_section": "Section 4, Latency comparison", "source_table": "Table 4"},
)

# ── Strategy: motivation for multi-scale internal approach ─────────────────────

strat_probe_gap = support(
    [internal_probe_weakness, chain_of_embedding_weakness],
    internal_cues_exist,
    reason=(
        "Both simple internal probes (@internal_probe_weakness) and CoE (@chain_of_embedding_weakness) "
        "fail to fully exploit internal signals: single-snapshot probes miss temporal dynamics, "
        "and CoE lacks task-specific supervision. The fact that both partially work (above-chance "
        "AUROC) yet fall short supports the hypothesis that internal cues exist (@internal_cues_exist) "
        "but require a more sophisticated extraction method—motivating Gnosis's multi-scale, "
        "supervised dual-stream architecture."
    ),
    prior=0.70,
)

strat_reward_cost_from_weakness = support(
    [reward_model_cost],
    external_judge_weakness,
    reason=(
        "The concrete latency numbers in @reward_model_cost (930ms at 12k tokens, 2465ms at 24k tokens "
        "for Skywork-8B) quantify the computational overhead claimed in @external_judge_weakness."
    ),
    prior=0.95,
)

strat_verbalconf_weakness = support(
    [verbalized_conf_weakness],
    text_critique_weakness,
    reason=(
        "The observed calibration failure of verbalized confidence methods (@verbalized_conf_weakness) "
        "supports the claim that text-based self-critique correlates weakly with true correctness "
        "(@text_critique_weakness), since verbalized confidence is a key form of text-based self-critique."
    ),
    prior=0.82,
)
