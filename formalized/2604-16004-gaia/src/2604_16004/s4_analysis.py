"""Section 4.3: Ablations, scaling, generalization, and latency analysis."""

from gaia.lang import claim, setting, support, induction, deduction

from .motivation import paradigm_shift_claim
from .s3_method import (
    bidirectional_design_claim,
    multi_agent_distillable_claim,
    tool_augmented_capability_claim,
)


# --- Ablation: forward-only / backward-only / full ---

ablation_setting = setting(
    "Ablation study (Figure 4) compares (a) forward-agent-only, (b) backward-agent-only, "
    "and (c) the full Agentic Verifier under both BoN sampling and verifier-revision."
)

ablation_observation = claim(
    "In Figure 4, both the forward-only and backward-only variants are competitive, but the "
    "full Agentic Verifier (forward + backward) achieves the best accuracy on MATH500 and "
    "Gaokao2023 across N in {32, 64, 128} and across refinement rounds.",
    background=[ablation_setting],
)

bidirectional_synergy_claim = claim(
    "The forward and backward agents are synergistic: combining them yields strictly better "
    "verification performance than either single-direction variant."
)

ablation_support = support(
    [ablation_observation, bidirectional_design_claim],
    bidirectional_synergy_claim,
    reason="Figure 4 directly demonstrates that the union outperforms each component.",
    prior=0.9,
    background=[ablation_setting],
)

# --- Tool usage ablation ---

tool_ablation_setting = setting(
    "Tool ablations in Appendix C.5: a no-tool variant of Agentic Verifier already "
    "outperforms the base model; adding the Python tool further improves performance, with "
    "tool usage moderate and stable in practice."
)

tool_contributes_claim = claim(
    "Both the agentic structure and tool integration contribute additively to verifier "
    "performance, with the agentic structure providing the larger share of the gain."
)

tool_support = support(
    [tool_augmented_capability_claim],
    tool_contributes_claim,
    reason="No-tool agentic variant beats the base model (agentic gain); enabling tools adds "
           "further improvement (tool gain).",
    prior=0.8,
    background=[tool_ablation_setting],
)

# --- Training-recipe ablation ---

training_ablation_setting = setting(
    "Figure 5 controllable study compares Train-free, SFT, and SFT+RL variants on BoN. "
    "Train-free already beats the base model by up to 2.6 points on Gaokao2023; SFT adds "
    "further gains; SFT+RL achieves the strongest results."
)

training_recipe_claim = claim(
    "Each stage of the AgentV-RL recipe contributes a measurable improvement: Train-free > "
    "Base, SFT > Train-free, SFT+RL > SFT."
)

training_support = support(
    [multi_agent_distillable_claim],
    training_recipe_claim,
    reason="Figure 5 quantifies stepwise gains across Train-free / SFT / SFT+RL settings.",
    prior=0.85,
    background=[training_ablation_setting],
)

# --- Inference-time and model-size scaling (induction over two settings) ---

inference_scaling_setting = setting(
    "Figure 6: sampling multiple verification trajectories per candidate (1, 4, 8) "
    "monotonically improves Best-of-32 accuracy on MATH500 and Gaokao2023."
)

model_size_setting = setting(
    "Table 3: scaling Agentic Verifier from Qwen3-0.6B to 1.7B to 4B yields monotone "
    "accuracy gains (e.g., +5.2 points on Gaokao2023 from 0.6B to 1.7B, with further gains "
    "at 4B) on MATH500 and Gaokao2023 across N in {32, 64, 128}."
)

inference_scaling_obs = claim(
    "Best-of-32 accuracy on MATH500 and Gaokao2023 increases as more verification "
    "trajectories are sampled (1 -> 4 -> 8).",
    background=[inference_scaling_setting],
)

model_size_obs = claim(
    "BoN accuracy on MATH500 and Gaokao2023 increases monotonically as the verifier scales "
    "from 0.6B to 1.7B to 4B parameters.",
    background=[model_size_setting],
)

scaling_law_claim = claim(
    "The Agentic Verifier framework scales positively along both axes available to it: "
    "inference-time compute (sampled trajectories) and model size (Qwen3 family)."
)

# Anchor each observation with an explicit prior so the law can propagate up via induction.
inference_scaling_obs_prior = support(
    [scaling_law_claim],
    inference_scaling_obs,
    reason="If the scaling law holds, sampling more verification trajectories should help.",
    prior=0.9,
)

model_size_scaling_obs_prior = support(
    [scaling_law_claim],
    model_size_obs,
    reason="If the scaling law holds, larger backbone models should help.",
    prior=0.9,
)

scaling_induction = induction(
    inference_scaling_obs_prior,
    model_size_scaling_obs_prior,
    law=scaling_law_claim,
    reason="Two independent scaling axes (inference compute and model size) both confirm "
           "the law.",
)

# --- Generalization ---

generalization_setting = setting(
    "Table 4: Agentic-Verifier-Qwen3-4B achieves 70.86 on LiveCodeBench and 66.00 on "
    "HotpotQA, outperforming Qwen3-4B (57.14 / 40.00), Qwen2.5-7B-Instruct, DS-Distill-14B, "
    "and Mistral-Small-24B-Instruct."
)

generalization_observation = claim(
    "Agentic-Verifier-Qwen3-4B beats all listed baselines on both LiveCodeBench (competitive "
    "code) and HotpotQA (multi-hop QA) in Table 4.",
    background=[generalization_setting],
)

generalization_claim = claim(
    "The bidirectional, tool-augmented agentic-verification paradigm generalizes beyond "
    "math to competitive code and multi-hop QA reasoning."
)

generalization_support = support(
    [generalization_observation, bidirectional_design_claim],
    generalization_claim,
    reason="Two out-of-domain benchmarks show consistent gains, attributed to the same "
           "bidirectional + tool design.",
    prior=0.75,
    background=[generalization_setting],
)

# --- Latency / cost ---

latency_setting = setting(
    "Table 5 latency analysis on a single A100 GPU (vLLM, batch=128) reports Base = 119.0s "
    "(2560 tokens, 1 round), Forward = 159.1s (4114 tokens, 5.7 rounds), "
    "Backward = 164.3s (4235 tokens, 5.6 rounds), Agentic-Verifier = 323.4s "
    "(8349 tokens, 11.3 rounds, 1.6 tool calls)."
)

latency_observation = claim(
    "Agentic Verifier consumes ~3.3x more tokens, ~11x more rounds, and ~2.7x more wall "
    "clock time than the base verifier; forward-only and backward-only variants sit between "
    "the two extremes.",
    background=[latency_setting],
)

cost_accuracy_tradeoff_claim = claim(
    "The accuracy gains of Agentic Verifier come at a substantial computational cost "
    "(tokens, rounds, latency); forward-only and backward-only variants offer scalable "
    "trade-offs for resource-constrained deployment."
)

# Direct read-off from the table; treat as a textbook-style deduction.
latency_axiom = claim(
    "The reported Table 5 numbers are accurate descriptions of the measured cost.",
    background=[latency_setting],
)

cost_tradeoff_deduction = deduction(
    [latency_observation, latency_axiom],
    cost_accuracy_tradeoff_claim,
    reason="Substituting the Table 5 measurements directly establishes the cost differences "
           "and the existence of intermediate variants as scalable trade-offs.",
    prior=0.95,
    background=[latency_setting],
)
