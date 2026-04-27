"""Section 4.2: Main experimental results - parallel and sequential test-time scaling."""

from gaia.lang import claim, setting, support, contradiction

from .motivation import paradigm_shift_claim
from .s3_method import (
    bidirectional_design_claim,
    multi_agent_distillable_claim,
    tool_augmented_capability_claim,
)


# --- Settings: benchmarks and baselines ---

bon_benchmarks_setting = setting(
    "Best-of-N evaluation on MATH500, GSM8K, Gaokao2023, and AIME24 with N in {32, 64, 128}, "
    "comparing against text reasoning LLMs, ORMs (e.g., INF-ORM-Llama3.1-70B, "
    "Skywork-V2-Llama-8B), and PRMs (e.g., Qwen2.5-Math-PRM-7B, Math-Shepherd, Skywork-PRM)."
)

iter_refine_setting = setting(
    "Iterative refinement evaluation across three turns on the same benchmarks, reporting "
    "Acc, Delta-up (correction rate), and Delta-down (degradation rate) per turn against "
    "verifier baselines including DS-Distill-14B and Qwen3-4B-Think."
)

table1_observation = claim(
    "On Table 1, Agentic-Verifier-Qwen3-4B achieves the best BoN accuracy in the Ours "
    "category across MATH500 (up to 79.0% at N=128), GSM8K (93.3%), Gaokao2023 (57.4%), "
    "and AIME24 (53.3%), surpassing the previous best ORM Skywork-V2-Llama-8B on MATH500 "
    "by 25.2 percentage points.",
    background=[bon_benchmarks_setting],
)

table2_observation = claim(
    "On Table 2, Agentic-Verifier-Qwen3-4B yields the highest accuracy and the largest "
    "Delta-up (e.g., 41.6% on MATH500, 40.3% on Gaokao2023 in turn 1) with low Delta-down, "
    "and remains stable across turns 2 and 3 while baselines such as DS-Distill-14B "
    "exhibit larger degradations.",
    background=[iter_refine_setting],
)

# --- Headline scientific claims ---

bon_sota_claim = claim(
    "Agentic Verifier achieves state-of-the-art Best-of-N performance across MATH500, "
    "GSM8K, Gaokao2023, and AIME24, with the 4B variant outperforming the prior best ORM "
    "(Skywork-V2-Llama-8B) on MATH500 by 25.2 percentage points."
)

bon_scales_with_n_claim = claim(
    "Agentic Verifier's BoN accuracy continues to improve as N grows from 32 to 128, "
    "particularly on challenging benchmarks like AIME24 (reaching 53.3% at N=128 with the "
    "4B variant), unlike many baselines whose accuracy plateaus or declines."
)

iter_refine_helpful_claim = claim(
    "Agentic Verifier provides high-quality critiques that drive faster convergence in "
    "iterative refinement: high Delta-up with low Delta-down in early turns and stable or "
    "only slightly declining accuracy in later turns, avoiding the degradation seen with "
    "competing verifiers."
)

# --- Strategy: observations support headline claims (and contradict the null) ---

bon_sota_support = support(
    [table1_observation, bidirectional_design_claim, multi_agent_distillable_claim,
     tool_augmented_capability_claim],
    bon_sota_claim,
    reason="The Table 1 ranking, taken with the bidirectional + tool-augmented design "
           "argument, attributes the SOTA gap to the proposed method.",
    prior=0.9,
    background=[bon_benchmarks_setting],
)

bon_scaling_support = support(
    [table1_observation],
    bon_scales_with_n_claim,
    reason="Reading the @table1_observation rows for N in {32, 64, 128} shows monotone or "
           "near-monotone gains for the 4B variant, especially on AIME24 (40.0 -> 50.0 -> 53.3).",
    prior=0.85,
    background=[bon_benchmarks_setting],
)

iter_refine_support = support(
    [table2_observation, bidirectional_design_claim, tool_augmented_capability_claim],
    iter_refine_helpful_claim,
    reason="Table 2's high Delta-up / low Delta-down for Agentic-Verifier-Qwen3-4B and its "
           "stable performance across turns evidence the helpfulness claim; the multi-turn "
           "tool-augmented design explains the robustness against degradation.",
    prior=0.85,
    background=[iter_refine_setting],
)

# --- Contradicting the null hypothesis: "ORMs beat Agentic Verifier on these benchmarks" ---

orm_dominance_null_claim = claim(
    "Outcome-level reward models (in particular Skywork-V2-Llama-8B and INF-ORM-Llama3.1-70B) "
    "match or exceed Agentic-Verifier-Qwen3-4B on the four BoN benchmarks."
)

orm_null_contradiction = contradiction(
    bon_sota_claim,
    orm_dominance_null_claim,
    reason="Table 1 shows Agentic-Verifier-Qwen3-4B's headline numbers strictly above the "
           "best ORM on every benchmark; the two claims cannot both hold.",
    prior=0.95,
)
