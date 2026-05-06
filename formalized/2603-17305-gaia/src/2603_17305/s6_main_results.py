"""Section 6: Main empirical results -- Tables 1, 2 across two LRM backbones.

This module formalizes the two main results tables verbatim:

* **Table 1**: jailbreak-safety performance (StrongReject [@Souly2024StrongReject]
  + JailbreakBench [@Chao2024JailbreakBench]) of CRAFT vs. six baselines
  (SafeChain, RealSafe, STAR, SafeKey, IPO, ReasoningShield) on
  DeepSeek-R1-Distill-Llama-8B [@Guo2025DeepSeekR1] and Qwen3-4B-Thinking
  [@Yang2025Qwen3]. Reasoning-trace safety + final-response safety, lower
  is better. Reported as means; variances <= 0.2% are omitted.
* **Table 2**: reasoning-performance preservation -- Pass@1 on
  AIME 2024 [@MAA2024AIME], MATH-500 [@Lightman2024PRM], LiveCodeBench
  [@Jain2025LiveCodeBench], and Minerva [@Dyer2022Minerva]; higher is
  better. Reported as means.

All experiments are repeated three times with distinct random seeds; means
and (negligible) standard deviations are reported per the original paper.

Source: [@Luo2026CRAFT, Sec. 6; Tables 1, 2].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: experimental conditions
# ---------------------------------------------------------------------------

setup_evaluation_protocol = setting(
    "**Evaluation protocol.** All experiments use 100 directly "
    "malicious prompts from JailbreakBench [@Chao2024JailbreakBench] "
    "and StrongReject [@Souly2024StrongReject] with the average "
    "performance across three attack settings (None, PAP "
    "[@Zeng2024PAP], PAIR [@Chao2025PAIR]) following [@Zhang2025dSTAIR]. "
    "Training uses 2,500 harmful prompts from R2D-R1 [@Zhu2025R2D] with "
    "paired reasoning-response annotations as supervision in Section "
    "4.1, plus benign prompts to mitigate over-refusal [@Cui2025ORBench] "
    "and the safety tax [@Huang2025SafetyTax]. All experiments are "
    "repeated 3x with distinct seeds; variances are uniformly <= 0.2% "
    "and omitted from the tables. Safety is automatically evaluated by "
    "GPT-4o [@Hurst2024GPT4o] following [@Zhang2025bIPO; "
    "@Yu2025MindInconspicuous].",
    title="Setup: 3-seed evaluation; benchmarks, attack settings, training data",
)

setup_compute_environment = setting(
    "**Compute environment.** All experiments are run on a system with "
    "four NVIDIA H100 GPUs (80 GB) and a 12-core Intel Xeon Gold 6338 "
    "CPU at 2.00 GHz. PyTorch + Hugging Face Transformers. Default "
    "system prompts; generation parameters are temperature 0.6, "
    "top-p 0.95, max 31,000 tokens [@Luo2026CRAFT, Appendix C].",
    title="Setup: 4xH100 / Xeon 6338 compute environment; generation hyperparameters",
)

setup_metrics = setting(
    "**Metrics.** *Final-response safety* is measured by the "
    "StrongReject score [@Souly2024StrongReject] on the model's final "
    "answer; lower is more refused/safe. *Reasoning-level safety* is "
    "the proportion of safe versus harmful content within the *reasoning "
    "trace*, computed via GPT-4o auto-evaluation following the "
    "protocol of [@Zhang2025bIPO]. *Reasoning ability* is Pass@1 "
    "accuracy on math (AIME 2024, MATH-500, Minerva) and code "
    "(LiveCodeBench) benchmarks. The exact GPT-4o evaluation prompt is "
    "given in Figure 5 of the paper.",
    title="Setup: StrongReject (response) + GPT-4o reasoning-trace safety + Pass@1 (reasoning)",
)

# ---------------------------------------------------------------------------
# Table 1: per-method, per-benchmark, per-model jailbreak safety
# ---------------------------------------------------------------------------

claim_table1_full = claim(
    "**Table 1: per-method jailbreak-safety scores (lower is safer).** "
    "Across DeepSeek-R1-Distill-Llama-8B [@Guo2025DeepSeekR1] and "
    "Qwen3-4B-Thinking [@Yang2025Qwen3], on JailbreakBench (JBB) and "
    "StrongReject (SR), the methods score as follows on "
    "{Reasoning, Response} (lower = safer):\n\n"
    "**DeepSeek-R1-Distill-Llama-8B**\n\n"
    "| Method | JBB Reasoning | JBB Response | SR Reasoning | SR Response | Avg |\n"
    "|--------|------:|------:|------:|------:|------:|\n"
    "| Base | 0.690 | 0.450 | 0.632 | 0.495 | 0.567 |\n"
    "| SafeChain [@Jiang2025bSafeChain] | 0.561 | 0.253 | 0.553 | 0.387 | 0.439 |\n"
    "| RealSafe [@Zhang2025cRealSafe] | 0.207 | **0.000** | 0.347 | 0.061 | 0.154 |\n"
    "| STAR [@Wang2025eSTAR] | 0.080 | 0.003 | 0.219 | 0.146 | 0.112 |\n"
    "| SafeKey [@Zhou2025bSafeKey] | 0.087 | **0.000** | 0.343 | 0.233 | 0.166 |\n"
    "| IPO [@Zhang2025bIPO] | **0.057** | 0.003 | **0.167** | 0.109 | **0.084** |\n"
    "| ReasoningShield [@Li2025aReasoningShield] | 0.583 | 0.410 | 0.627 | 0.425 | 0.511 |\n"
    "| **CRAFT** | 0.065 | 0.001 | 0.172 | **0.058** | 0.074 |\n\n"
    "**Qwen3-4B-Thinking**\n\n"
    "| Method | JBB Reasoning | JBB Response | SR Reasoning | SR Response | Avg |\n"
    "|--------|------:|------:|------:|------:|------:|\n"
    "| Base | 0.687 | 0.370 | 0.610 | 0.429 | 0.524 |\n"
    "| SafeChain [@Jiang2025bSafeChain] | 0.516 | 0.110 | 0.505 | 0.286 | 0.354 |\n"
    "| RealSafe [@Zhang2025cRealSafe] | 0.249 | 0.103 | 0.234 | 0.144 | 0.183 |\n"
    "| STAR [@Wang2025eSTAR] | 0.220 | 0.119 | 0.165 | 0.132 | 0.159 |\n"
    "| SafeKey [@Zhou2025bSafeKey] | 0.224 | 0.109 | 0.229 | 0.083 | 0.161 |\n"
    "| IPO [@Zhang2025bIPO] | 0.197 | 0.093 | 0.158 | **0.071** | 0.130 |\n"
    "| ReasoningShield [@Li2025aReasoningShield] | 0.577 | 0.240 | 0.592 | 0.283 | 0.423 |\n"
    "| **CRAFT** | **0.181** | **0.073** | **0.132** | 0.083 | **0.117** |\n\n"
    "Best per column in **bold**. Variances omitted as <= 0.2% "
    "uniformly [@Luo2026CRAFT, Table 1].",
    title="Table 1: per-method jailbreak-safety scores across two LRMs (verbatim)",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Table 1",
        "caption": "Table 1: Comparison with reasoning-based alignment methods on JailbreakBench + StrongReject across DeepSeek-R1-Distill-Llama-8B and Qwen3-4B-Thinking; lower is safer.",
    },
)

claim_craft_qwen_best_overall = claim(
    "**On Qwen3-4B-Thinking, CRAFT achieves the best overall (lowest) "
    "average safety score: 0.117.** This is the lowest average among "
    "all eight methods evaluated, beating IPO (0.130, the strongest "
    "baseline), SafeKey (0.161), STAR (0.159), and the rest. CRAFT "
    "is also best on three of four columns (JBB Reasoning 0.181, JBB "
    "Response 0.073, SR Reasoning 0.132) and second-best on the fourth "
    "(SR Response 0.083, narrowly behind IPO's 0.071) "
    "[@Luo2026CRAFT, Table 1].",
    title="Result: on Qwen3-4B-Thinking, CRAFT achieves best overall avg (0.117)",
)

claim_craft_r1distill_competitive = claim(
    "**On DeepSeek-R1-Distill-Llama-8B, CRAFT achieves average 0.074, "
    "the second-best average (behind IPO's 0.084 best -- wait correction).** "
    "Re-reading Table 1: CRAFT achieves average 0.074 on R1-Distill-"
    "Llama-8B; IPO achieves 0.084. CRAFT is therefore the best overall "
    "method on R1-Distill-Llama-8B as well -- 0.074 < 0.084. CRAFT "
    "achieves second-best on JBB Reasoning (0.065 vs IPO's 0.057) and "
    "SR Reasoning (0.172 vs IPO's 0.167), and best on SR Response "
    "(0.058 vs RealSafe/SafeKey's 0.000 in JBB Response only -- but "
    "considering all four columns CRAFT wins overall). The paper "
    "frames CRAFT as not top-ranked in every individual setting on "
    "R1-Distill-Llama-8B but consistently best or second-best, with "
    "best overall average [@Luo2026CRAFT, Table 1; Sec. 6.1].",
    title="Result: on R1-Distill-Llama-8B, CRAFT achieves best overall avg (0.074)",
)

# ---------------------------------------------------------------------------
# Table 2: reasoning-performance preservation
# ---------------------------------------------------------------------------

claim_table2_full = claim(
    "**Table 2: per-method reasoning-performance scores (Pass@1, "
    "higher is better).** On three math benchmarks (AIME 2024 "
    "[@MAA2024AIME], MATH-500 [@Lightman2024PRM], Minerva "
    "[@Dyer2022Minerva]) and one code benchmark (LiveCodeBench "
    "[@Jain2025LiveCodeBench]):\n\n"
    "**DeepSeek-R1-Distill-Llama-8B**\n\n"
    "| Method | AIME24 | MATH-500 | LiveCodeBench | Minerva | Avg |\n"
    "|--------|------:|------:|------:|------:|------:|\n"
    "| Base | 0.507 | 0.918 | 0.102 | 0.221 | 0.437 |\n"
    "| SafeChain | 0.453 | 0.870 | 0.091 | 0.198 | 0.403 |\n"
    "| RealSafe | 0.453 | 0.898 | 0.091 | 0.198 | 0.410 |\n"
    "| STAR | 0.460 | 0.894 | 0.093 | 0.200 | 0.412 |\n"
    "| SafeKey | 0.533 | 0.920 | 0.107 | 0.232 | 0.448 |\n"
    "| IPO | 0.540 | 0.916 | 0.109 | 0.235 | 0.450 |\n"
    "| ReasoningShield | 0.473 | 0.896 | 0.069 | 0.230 | 0.417 |\n"
    "| **CRAFT** | 0.517 | **0.985** | **0.129** | **0.242** | **0.468** |\n\n"
    "**Qwen3-4B-Thinking**\n\n"
    "| Method | AIME24 | MATH-500 | LiveCodeBench | Minerva | Avg |\n"
    "|--------|------:|------:|------:|------:|------:|\n"
    "| Base | 0.700 | 0.952 | 0.219 | 0.404 | 0.569 |\n"
    "| SafeChain | 0.625 | 0.850 | 0.196 | 0.361 | 0.508 |\n"
    "| RealSafe | 0.627 | 0.851 | 0.198 | 0.358 | 0.509 |\n"
    "| STAR | 0.635 | 0.863 | 0.199 | 0.366 | 0.516 |\n"
    "| SafeKey | 0.736 | 0.901 | 0.230 | 0.425 | 0.573 |\n"
    "| IPO | 0.739 | 0.903 | 0.238 | 0.427 | 0.577 |\n"
    "| ReasoningShield | 0.581 | 0.739 | 0.260 | 0.332 | 0.478 |\n"
    "| **CRAFT** | **0.741** | 0.924 | 0.254 | 0.420 | **0.585** |\n\n"
    "CRAFT achieves the highest average reasoning Pass@1 on both "
    "models: 0.468 on R1-Distill-Llama-8B and 0.585 on Qwen3-4B-"
    "Thinking, *exceeding the base models' 0.437 / 0.569* "
    "[@Luo2026CRAFT, Table 2].",
    title="Table 2: per-method reasoning-performance scores (Pass@1, verbatim)",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Table 2",
        "caption": "Table 2: Reasoning-performance comparison across the same baselines + CRAFT on AIME24/MATH-500/LiveCodeBench/Minerva; higher is better.",
    },
)

claim_craft_preserves_reasoning = claim(
    "**CRAFT preserves (and on average improves) reasoning ability "
    "while increasing safety.** The corrected average Pass@1 *exceeds* "
    "the base model on both LRMs: 0.468 vs 0.437 on "
    "R1-Distill-Llama-8B (+0.031, or +7.1% relative); 0.585 vs 0.569 "
    "on Qwen3-4B-Thinking (+0.016, or +2.8% relative). Across both "
    "models the average improvement is 4.7%, driven by exposure to "
    "high-quality reasoning trajectories during SFT/GRPO training. "
    "This contradicts the 'safety tax' [@Huang2025SafetyTax] "
    "expectation that safety alignment necessarily degrades reasoning "
    "[@Luo2026CRAFT, Sec. 6.2; Table 2].",
    title="Result: CRAFT preserves reasoning -- avg +4.7% Pass@1 over base across both LRMs",
)

# ---------------------------------------------------------------------------
# Headline cross-model average improvements (the abstract numbers)
# ---------------------------------------------------------------------------

claim_craft_best_average_safety = claim(
    "**Across both LRMs, CRAFT achieves the lowest average jailbreak "
    "score among the eight methods evaluated.** Specifically, the "
    "average safety scores (mean of the per-LRM avg columns in Table 1) "
    "are: Base 0.546; SafeChain 0.397; RealSafe 0.169; STAR 0.136; "
    "SafeKey 0.164; IPO 0.107; ReasoningShield 0.467; "
    "**CRAFT 0.096**. CRAFT is the only method to achieve below 0.1 "
    "in cross-model average jailbreak score [@Luo2026CRAFT, Table 1].",
    title="Headline: CRAFT achieves lowest cross-model avg jailbreak score (0.096)",
)

claim_craft_vs_baselines_summary = claim(
    "**Relative to the strongest baselines on the safety axis, "
    "CRAFT yields a 5.0% improvement in reasoning-trace safety and "
    "a 22.1% improvement in final-response safety.** The strongest "
    "baselines for reasoning-trace safety are IPO and SafeKey "
    "[@Zhang2025bIPO; @Zhou2025bSafeKey]; relative to them CRAFT's "
    "reasoning-trace safety is 5.0% better and final-response "
    "safety is 22.1% better. While CRAFT is not top-ranked in every "
    "individual cell -- particularly on R1-Distill-Llama-8B where IPO "
    "wins JBB Reasoning -- CRAFT consistently attains best or "
    "second-best performance, and the paper attributes any remaining "
    "gap to current training-budget limitations that could be "
    "mitigated with extended training "
    "[@Luo2026CRAFT, Sec. 6.1].",
    title="Result: vs. strongest baselines (IPO/SafeKey), CRAFT +5.0% reasoning / +22.1% response safety",
)

__all__ = [
    "setup_evaluation_protocol",
    "setup_compute_environment",
    "setup_metrics",
    "claim_table1_full",
    "claim_craft_qwen_best_overall",
    "claim_craft_r1distill_competitive",
    "claim_table2_full",
    "claim_craft_preserves_reasoning",
    "claim_craft_best_average_safety",
    "claim_craft_vs_baselines_summary",
]
