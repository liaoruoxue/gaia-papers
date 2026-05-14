"""Section 4.1-4.2: Training setup + main 'unconstrained' comparison with the
previous best across 7 benchmarks (Table 1, Figure 1).

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Sections 4.1 + 4.2,
p. 5-6, plus Appendix A.1 (training hyperparameters).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Training setup (Section 4.1 + Appendix A.1)
# ---------------------------------------------------------------------------

setup_base_model = setting(
    "**Base model: Qwen2.5-7B.** The main Conductor experiments start "
    "from a Qwen2.5-7B checkpoint [@Hui2024Qwen25Coder] with max "
    "completion length 1024.",
    title="Setup: base model Qwen2.5-7B with max completion length 1024",
)

setup_worker_pool = setting(
    "**Worker pool for main experiments.** The 7B Conductor is tasked to "
    "devise workflows of up to 5 steps using both proprietary frontier "
    "models -- **Gemini 2.5 Pro** [@Comanici2025Gemini25], **Claude "
    "Sonnet 4** [@Anthropic2025Sonnet], **GPT-5** [@OpenAI2025GPT5] -- "
    "and open-source alternatives -- **DeepSeek-R1-Distill-Qwen-32B** "
    "[@Guo2025DeepSeekR1], **Gemma3-27B-instruct** [@Team2025Gemma3], "
    "**Qwen3-32B** in both non-thinking and thinking modes "
    "[@Yang2025Qwen3]. Total: **7 workers** (3 closed + 4 open).",
    title="Setup: 7-worker pool (3 closed + 4 open) -- Gemini 2.5, Claude 4, GPT-5, R1-distill, Gemma3, Qwen3 x2",
)

setup_training_data = setting(
    "**Training dataset.** 960 problems are selected from four reasoning "
    "domains: MATH500 [@Lightman2023MATH500] (mathematics, 300 train + "
    "100 test from the MATH dataset [@Hendrycks2021MATH]), MMLU "
    "[@Hendrycks2020MMLU] (multitask language understanding, 99,842 "
    "train + 14,042 test), RLPR [@Yu2025RLPR] (real-world general "
    "reasoning, 46,620 train + 15,540 test from WebInstruct "
    "[@Yue2024Mammoth2]), and LiveCodeBench V1 [@Jain2024LiveCodeBench] "
    "(code generation, oldest version used for training). Selection "
    "prioritizes difficulty and diversity.",
    title="Setup: 960 training problems from MATH500 + MMLU + RLPR + LiveCodeBench V1 (four reasoning domains)",
)

setup_eval_benchmarks = setting(
    "**Evaluation benchmarks.** Two tiers of evaluation:\n\n"
    "1. **In-distribution** -- all *unseen* test questions from MATH500, "
    "MMLU, RLPR, and LiveCodeBench V6 (newest LiveCodeBench at writing).\n"
    "2. **Out-of-distribution** -- three unseen test tasks: GPQA-Diamond "
    "[@Rein2024GPQA] (198 graduate-level natural-science MCQ), "
    "BigCodeBench [@Zhuo2024BigCodeBench] (148 'hard' + 'complete' "
    "function-call code generation samples), and AIME25 [@AIME2025] (30 "
    "competition-math questions from the 2025 American Invitational "
    "Mathematics Examination).\n\n"
    "Each evaluation is repeated up to 16 times to account for "
    "stochasticity; mean accuracy and standard errors are reported.",
    title="Setup: in-dist (MATH500/MMLU/RLPR/LCBv6) + OOD (GPQA-D/BigCodeBench/AIME25), 16 repeats each",
)

setup_training_hyperparameters = setting(
    "**Training hyperparameters (Appendix A.1).** 200 GRPO iterations, "
    "4 questions per iteration, 64 rollouts per question with "
    "temperature 1.0. AdamW [@Loshchilov2017AdamW] with $\\beta_1 = "
    "0.9$, $\\beta_2 = 0.999$, $\\epsilon = 0.2$, base learning rate "
    "$10^{-6}$, cosine scheduling, 0.03 warmup ratio. **Reference-model "
    "synchronization disabled** and **KL-divergence penalty set to 0**. "
    "Workers: 4096 max completion tokens, temperature 0.2. Closed-source "
    "reasoning budgets at minima (Gemini 128 tokens, Claude 0, GPT-5 "
    "'minimal'). Compute: 2x NVIDIA H100 80GB GPUs.",
    title="Setup: hyperparameters -- 200 iters, no KL, 2x H100, lr=1e-6, batch=256, 64 rollouts",
)

setup_unconstrained_setting = setting(
    "**Unconstrained evaluation setting.** Section 4.2 results use the "
    "*unconstrained* setting in which completion tokens and reasoning "
    "budgets are set to their maxima per model (Table 3 of paper): "
    "Gemini 2.5 Pro 65535 / 32768, Claude Sonnet 4 64000 / 32768, "
    "GPT-5 128000 / 'high', R1-Distill / Gemma / Qwen3 20480 max "
    "completion tokens. Exception: GPT-5 on BigCodeBench uses 'medium' "
    "reasoning effort because it marginally outperforms 'high' for that "
    "task, consistent with OpenAI's own findings for certain tasks "
    "[@OpenAI2025GPT5].",
    title="Setup: unconstrained setting -- max completion tokens and reasoning budget per Table 3",
)

# ---------------------------------------------------------------------------
# Table 1 -- Main unconstrained comparison
# ---------------------------------------------------------------------------

claim_table1_full = claim(
    "**Table 1: Comparison with previous best 'unconstrained' results.** "
    "The Conductor's performance is significantly beyond official "
    "reported results across several challenging reasoning benchmarks, "
    "setting new records.\n\n"
    "| Model | M500 | MMLU | RLPR | LCB | AIME25 | BCB | GPQA-D | Avg. |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
    "| gemma-3-27b-it | 39.8 | 81.3 | 16.67 | 13.14 | 20.7 | 14.86 | 38.4 | 32.12 |\n"
    "| Qwen3-32B | 73.5 | 83.5 | 31.00 | 21.21 | 20.0 | 30.41 | 64.1 | 53.81 |\n"
    "| Qwen3-32B (thinking) | 80.7 | 84.1 | 37.25 | 25.86 | 72.9 | 28.38 | 66.8 | 56.57 |\n"
    "| R1-Distill-Qwen-32B | 82.5 | 84.4 | 33.50 | 26.86 | 63.0 | 33.07 | 58.1 | 54.49 |\n"
    "| Claude Sonnet 4 | 96.0 | 91.4 | 36.70 | 46.54 | 74.3 | 37.16 | 77.7 | 65.69 |\n"
    "| Gemini 2.5 Pro | 96.0 | 92.4 | 40.55 | 67.24 | 78.3 | 37.51 | 84.8 | 70.97 |\n"
    "| GPT 5 | 99.0 | 93.5 | 42.20 | 82.90 | 90.8 | 32.75 | 82.3 | 74.78 |\n"
    "| **Conductor (Ours)** | **99.4** | **94.1** | **44.75** | **83.93** | **93.3** | **37.86** | **87.5** | **77.27** |\n\n"
    "Conductor is best on **every column** -- in-domain (M500/MMLU/RLPR/LCB) "
    "and unseen-task (AIME25/BCB/GPQA-D) -- and best on average "
    "(77.27 vs GPT-5 74.78).",
    title="Table 1: per-benchmark unconstrained accuracy -- Conductor SOTA on all 7 columns",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 1",
        "caption": "Table 1: Conductor vs previous-best across 7 benchmarks under unconstrained setting.",
    },
)

# ---------------------------------------------------------------------------
# Per-benchmark headline numbers
# ---------------------------------------------------------------------------

claim_math500_unconstrained = claim(
    "**MATH500 (in-domain) unconstrained:** Conductor 99.4 vs GPT-5 99.0 "
    "(delta = +0.4 pp); near the saturation point of this benchmark.",
    title="Result row: MATH500 unconstrained -- Conductor 99.4 vs GPT-5 99.0 (+0.4 pp)",
)

claim_mmlu_unconstrained = claim(
    "**MMLU (in-domain) unconstrained:** Conductor 94.1 vs GPT-5 93.5 "
    "(delta = +0.6 pp).",
    title="Result row: MMLU unconstrained -- Conductor 94.1 vs GPT-5 93.5 (+0.6 pp)",
)

claim_rlpr_unconstrained = claim(
    "**RLPR (in-domain) unconstrained:** Conductor 44.75 vs GPT-5 42.20 "
    "(delta = +2.55 pp).",
    title="Result row: RLPR unconstrained -- Conductor 44.75 vs GPT-5 42.20 (+2.55 pp)",
)

claim_lcb_unconstrained = claim(
    "**LiveCodeBench V6 (in-domain) unconstrained:** Conductor 83.93 vs "
    "GPT-5 82.90 (delta = +1.03 pp). Beyond every prior LLM on the "
    "LiveCodeBench online leaderboard, even surpassing OpenAI's O-series "
    "models [@Jaech2024OpenAIO1], which were not included in the worker "
    "pool due to their exceedingly high cost.",
    title="Result row: LCBv6 unconstrained -- Conductor 83.93 vs GPT-5 82.90 (+1.03 pp); SOTA on leaderboard",
)

claim_aime25_unconstrained = claim(
    "**AIME25 (OOD) unconstrained:** Conductor 93.3 vs GPT-5 90.8 "
    "(delta = +2.5 pp). The paper notes this is **consistent with the "
    "entire generational improvement from o3 to GPT-5** on AIME25 "
    "(approximately 3.3% absolute).",
    title="Result row: AIME25 unconstrained -- Conductor 93.3 vs GPT-5 90.8 (+2.5 pp ~= o3->GPT-5 generation jump)",
)

claim_bcb_unconstrained = claim(
    "**BigCodeBench (OOD) unconstrained:** Conductor 37.86 vs Gemini 2.5 "
    "Pro 37.51 (delta = +0.35 pp). The strongest individual baseline on "
    "this benchmark is Gemini 2.5 Pro / Claude 4, not GPT-5 (32.75); "
    "Conductor still edges them.",
    title="Result row: BigCodeBench unconstrained -- Conductor 37.86 vs Gemini 2.5 Pro 37.51 (+0.35 pp)",
)

claim_gpqa_unconstrained = claim(
    "**GPQA-Diamond (OOD) unconstrained:** Conductor 87.5 vs Gemini 2.5 "
    "Pro 84.8 (delta = +2.7 pp). The paper notes this is also "
    "**consistent with the o3 -> GPT-5 generational improvement** on "
    "GPQA-D (approximately 2.7% absolute).",
    title="Result row: GPQA-D unconstrained -- Conductor 87.5 vs Gemini 84.8 (+2.7 pp ~= generation jump)",
)

claim_avg_unconstrained = claim(
    "**Average unconstrained improvement.** Across 7 benchmarks, the 7B "
    "Conductor averages **77.27** vs the best non-Conductor baseline "
    "GPT-5 **74.78** (delta = +2.49 pp average across columns). On a "
    "per-column basis the Conductor uniformly exceeds the *previous "
    "best* (column-winner among 7 baselines), with delta ranging from "
    "+0.4 pp (M500, near saturation) to +2.7 pp (GPQA-D, generational).",
    title="Result: Conductor avg = 77.27 vs best baseline GPT-5 74.78 (+2.49 pp avg, all 7 columns won)",
)

# ---------------------------------------------------------------------------
# Performance-improvement-scale interpretation (Appendix A.3)
# ---------------------------------------------------------------------------

claim_long_tail_difficulty = claim(
    "**Interpretation of the gain magnitude.** Highly competitive "
    "reasoning benchmarks (AIME25, GPQA-D, etc.) have a "
    "**long-tailed distribution of difficulty** "
    "[@Xu2025Clustering] -- breakthroughs in a small subset of "
    "particularly challenging problems can represent **entire "
    "generational improvements in LLM reasoning**. For example, "
    "GPT-o3 -> GPT-5 is 3.3% on AIME25 and 2.7% on GPQA-D in absolute "
    "terms. The Conductor's gains are of this generational magnitude, "
    "occurring across math, coding, and natural science benchmarks "
    "simultaneously.",
    title="Claim: gain magnitude (2-3 pp on hard benchmarks) is generational, not incremental",
)

__all__ = [
    "setup_base_model",
    "setup_worker_pool",
    "setup_training_data",
    "setup_eval_benchmarks",
    "setup_training_hyperparameters",
    "setup_unconstrained_setting",
    "claim_table1_full",
    "claim_math500_unconstrained",
    "claim_mmlu_unconstrained",
    "claim_rlpr_unconstrained",
    "claim_lcb_unconstrained",
    "claim_aime25_unconstrained",
    "claim_bcb_unconstrained",
    "claim_gpqa_unconstrained",
    "claim_avg_unconstrained",
    "claim_long_tail_difficulty",
]
