"""Section 5: Empirical Evaluations -- benchmarks, baselines, training
setup, and main results across recursion rounds + broader baseline panel.

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 5 + Tables 2-3.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Section 5 setup: tasks, baselines, training
# ---------------------------------------------------------------------------

setup_nine_benchmarks = setting(
    "**Nine evaluation benchmarks.** RecursiveMAS is evaluated on nine "
    "benchmarks across five domains:\n\n"
    "| Domain | Benchmarks |\n"
    "|---|---|\n"
    "| Mathematical Reasoning | MATH500 [@MATH500], AIME2025 [@AIME2025], "
    "AIME2026 [@AIME2026] |\n"
    "| Scientific & Medical | GPQA-Diamond [@GPQA], MedQA [@MedQA] |\n"
    "| Code Generation | LiveCodeBench-v6 [@LiveCodeBench], MBPP+ "
    "[@MBPPplus] |\n"
    "| Search QA | HotpotQA [@HotpotQA], Bamboogle [@Bamboogle] |\n\n"
    "Each dataset uses its standard evaluation metric (numeric match "
    "for math, multiple-choice match for GPQA/MedQA, sandbox execution "
    "for code, LLM-judge for search). For AIME2025/2026, Pass@10 "
    "accuracy is reported to test robustness.",
    title="Setup: 9 benchmarks across math / science-medicine / code / search",
)

setup_baselines = setting(
    "**Baseline categories.** RecursiveMAS is compared against three "
    "baseline categories: "
    "(i) **Single Advanced Agents** -- the final agent of each "
    "collaboration pattern isolated as a standalone model, with both "
    "*LoRA* [@LoRA] and *full supervised fine-tuning* on the same "
    "training set; "
    "(ii) **Recursion-based Methods** -- single recursive language "
    "models, LoopLM [@LoopLM], and **Recursive-TextMAS** (agents "
    "collaborating in the same way as RecursiveMAS but interacting "
    "through *text* instead of latent thoughts); and "
    "(iii) **Representative Multi-Agent Frameworks** -- TextGrad "
    "[@TextGrad] and Mixture-of-Agents (MoA) [@MoA] for holistic "
    "structure-wide comparison.",
    title="Setup: baseline categories (single agents, recursion-based, MAS frameworks)",
)

setup_training_data = setting(
    "**Training data.** The training set is curated across four "
    "domains: s1K [@s1] for mathematical problem solving, m1K [@m1] "
    "for medical and scientific tasks, OpenCodeReasoning "
    "[@OpenCodeReasoning] for code generation, and ARPO-SFT [@ARPO] "
    "for agentic tool-augmentation (Python and search-API) settings. "
    "Each training sample's answer is rewritten into role-specific "
    "supervision targets per collaboration pattern (e.g., for "
    "Sequential-style, the answer is rewritten into an initial plan "
    "for the Planner, a refined critic-guided plan for the Critic, "
    "and the original answer for the Solver).",
    title="Setup: training data sources (s1K, m1K, OpenCodeReasoning, ARPO-SFT) with role-specific rewriting",
)

setup_implementation_details = setting(
    "**Implementation details.** All base LLM parameters are frozen; "
    "only the inner and outer RecursiveLink modules are updated, "
    "using AdamW with learning rate 5e-4, cosine schedule, batch "
    "size 4, and max sequence length 4096. Inference uses top-p 0.95 "
    "with temperature 0.6 (most reasoning tasks) or 0.2 (code "
    "generation). Each task uses a tailored max generation length: "
    "2000 tokens (MATH500), 4000 tokens (MedQA, GPQA-D, "
    "LiveCodeBench, MBPP+), 16000 tokens (AIME2025/2026). Experiments "
    "use HuggingFace Transformers and vLLM [@vLLM] backends on H100 "
    "and A100 GPUs. For Deliberation-Style, a Python sandbox plus "
    "Tavily [@Tavily] search API are provided as tools. Each result "
    "is the mean over five independent runs; standard deviation of "
    "RecursiveMAS results across 5 runs is approximately +/- 0.0041 "
    "for accuracy, +/- 26 for runtime (s), +/- 33 for tokens.",
    title="Setup: training/inference hyperparameters + 5-run mean with reported std",
)

# ---------------------------------------------------------------------------
# Section 5.1: scaling performance via recursion (Table 2)
# ---------------------------------------------------------------------------

claim_table2_full = claim(
    "**Table 2: Main results across recursion rounds $r = 1, 2, 3$ "
    "(accuracy %).** RecursiveMAS is compared against Recursive-"
    "TextMAS under identical MAS structures and recursion budgets. "
    "Light = sub-1.5B per-agent setup (Table 1 row 1, MBPP+ for "
    "Code Gen.); Scaled = 5-10B per-agent setup (Table 1 row 2, "
    "LiveCodeBench for Code Gen.).\n\n"
    "| Round | Method | MATH500 (L/S) | AIME25 (L/S) | AIME26 (L/S) | "
    "GPQA-D (L/S) | MedQA (L/S) | Code Gen (L/S) |\n"
    "|---|---|---|---|---|---|---|---|\n"
    "| r=1 | TextMAS | 71.9 / 84.2 | 24.0 / 71.3 | 16.7 / 76.7 | "
    "28.1 / 61.5 | 29.0 / 76.1 | 30.7 / 38.5 |\n"
    "| r=1 | **RecursiveMAS** | **75.8 / 86.3** | **30.7 / 80.0** | "
    "**17.3 / 82.7** | **30.3 / 63.1** | **30.3 / 78.2** | "
    "**35.1 / 40.1** |\n"
    "| r=2 | TextMAS | 72.5 / 84.4 | 23.3 / 70.7 | 10.0 / 77.3 | "
    "28.7 / 59.1 | 28.3 / 76.1 | 30.0 / 38.0 |\n"
    "| r=2 | **RecursiveMAS** | **76.6 / 87.1** | **33.3 / 86.0** | "
    "**18.7 / 84.0** | **32.3 / 64.6** | **31.2 / 78.3** | "
    "**36.9 / 41.3** |\n"
    "| r=3 | TextMAS | 69.1 / 85.8 | 18.0 / 73.3 | 16.7 / 74.7 | "
    "28.7 / 58.6 | 28.5 / 77.1 | 29.3 / 36.5 |\n"
    "| r=3 | **RecursiveMAS** | **77.8 / 88.2** | **34.0 / 86.7** | "
    "**20.0 / 86.0** | **32.6 / 66.2** | **31.7 / 79.3** | "
    "**37.4 / 42.8** |\n",
    title="Table 2: per-round per-task accuracy (Light / Scaled) of RecursiveMAS vs Recursive-TextMAS",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 2",
        "caption": "Table 2: Main results of RecursiveMAS over different recursion rounds (Light / Scaled) on Math500, AIME2025, AIME2026, GPQA-D, MedQA, Code Gen.",
    },
)

claim_avg_improvement_per_round = claim(
    "**Average improvement of RecursiveMAS over Recursive-TextMAS by "
    "recursion round.** Across the seven (Light + Scaled) accuracy "
    "rows of Table 2, RecursiveMAS exceeds the text-mediated baseline "
    "by an average of **+3.4% at $r=1$**, **+6.0% at $r=2$**, and "
    "**+7.2% at $r=3$**. The performance advantage thus *grows* with "
    "recursion depth.",
    title="Result: avg accuracy gain over TextMAS = +3.4% / +6.0% / +7.2% at r=1/2/3 (grows with depth)",
)

claim_avg_improvement_text_baseline_section = claim(
    "**Average improvement compared with Recursive-TextMAS reported "
    "in Section 5.1 narrative (Light setting).** When restricted to "
    "the Light (sub-1.5B agents) setting and averaged across math / "
    "science / code generation tasks, RecursiveMAS improves over "
    "Recursive-TextMAS by **+8.1% at $r=1$**, **+19.6% at $r=2$**, "
    "and **+20.2% at $r=3$**. These narrative averages emphasize the "
    "Light regime where TextMAS struggles most as recursion deepens.",
    title="Result: Light-setting avg accuracy gain over TextMAS = +8.1% / +19.6% / +20.2% at r=1/2/3",
)

claim_consistent_upward_trend = claim(
    "**RecursiveMAS exhibits a consistent upward accuracy trend with "
    "recursion depth.** For both Light and Scaled versions of "
    "RecursiveMAS, accuracy rises monotonically across $r = 1, 2, 3$ "
    "on each of the seven Table-2 columns (MATH500, AIME2025, "
    "AIME2026, GPQA-D, MedQA, Code Gen.). For example, the Scaled "
    "RecursiveMAS on MATH500 climbs 86.3% -> 87.1% -> 88.2%; on "
    "AIME2025 it climbs 80.0% -> 86.0% -> 86.7%. In contrast, "
    "Recursive-TextMAS shows no consistent monotone trend (often "
    "fluctuates or regresses with deeper recursion).",
    title="Result: RecursiveMAS accuracy is monotone in r across all 7 columns; TextMAS is not",
)

# ---------------------------------------------------------------------------
# Per-row claims (used by abductions / inductions later)
# ---------------------------------------------------------------------------

claim_math500_r3 = claim(
    "**MATH500 at $r = 3$.** Scaled RecursiveMAS achieves 88.2% vs "
    "Recursive-TextMAS 85.8% (delta = +2.4 pp). Light RecursiveMAS "
    "achieves 77.8% vs TextMAS 69.1% (delta = +8.7 pp).",
    title="Result row: MATH500 r=3 -- RecursiveMAS 88.2/77.8 vs TextMAS 85.8/69.1",
)

claim_aime25_r3 = claim(
    "**AIME2025 at $r = 3$ (Pass@10).** Scaled RecursiveMAS 86.7% vs "
    "TextMAS 73.3% (delta = +13.4 pp). Light RecursiveMAS 34.0% vs "
    "TextMAS 18.0% (delta = +16.0 pp).",
    title="Result row: AIME2025 r=3 -- RecursiveMAS 86.7/34.0 vs TextMAS 73.3/18.0",
)

claim_aime26_r3 = claim(
    "**AIME2026 at $r = 3$ (Pass@10).** Scaled RecursiveMAS 86.0% vs "
    "TextMAS 74.7% (delta = +11.3 pp). Light RecursiveMAS 20.0% vs "
    "TextMAS 16.7% (delta = +3.3 pp).",
    title="Result row: AIME2026 r=3 -- RecursiveMAS 86.0/20.0 vs TextMAS 74.7/16.7",
)

claim_gpqa_r3 = claim(
    "**GPQA-Diamond at $r = 3$.** Scaled RecursiveMAS 66.2% vs "
    "TextMAS 58.6% (delta = +7.6 pp). Light RecursiveMAS 32.6% vs "
    "TextMAS 28.7% (delta = +3.9 pp).",
    title="Result row: GPQA-D r=3 -- RecursiveMAS 66.2/32.6 vs TextMAS 58.6/28.7",
)

claim_medqa_r3 = claim(
    "**MedQA at $r = 3$.** Scaled RecursiveMAS 79.3% vs TextMAS 77.1% "
    "(delta = +2.2 pp). Light RecursiveMAS 31.7% vs TextMAS 28.5% "
    "(delta = +3.2 pp).",
    title="Result row: MedQA r=3 -- RecursiveMAS 79.3/31.7 vs TextMAS 77.1/28.5",
)

claim_codegen_r3 = claim(
    "**Code Gen. at $r = 3$.** Scaled RecursiveMAS on LiveCodeBench "
    "42.8% vs TextMAS 36.5% (delta = +6.3 pp). Light RecursiveMAS on "
    "MBPP+ 37.4% vs TextMAS 29.3% (delta = +8.1 pp).",
    title="Result row: Code Gen r=3 -- RecursiveMAS 42.8/37.4 vs TextMAS 36.5/29.3",
)

# ---------------------------------------------------------------------------
# Section 5.2: broader baseline comparison (Table 3)
# ---------------------------------------------------------------------------

claim_table3 = claim(
    "**Table 3: RecursiveMAS vs broader baselines at $r = 3$ "
    "(accuracy %).** All methods are instantiated with identical "
    "backbone models and matched training budgets (trainable "
    "parameter counts, recursion depth, and training set).\n\n"
    "| Method | MATH500 | AIME25 | AIME26 | GPQA-D | LiveCodeBench | "
    "MedQA |\n"
    "|---|---|---|---|---|---|---|\n"
    "| Single Agent (w/ LoRA) | 83.1 | 70.0 | 73.3 | 62.0 | 37.4 | "
    "76.1 |\n"
    "| Single Agent (w/ Full-SFT) | 83.2 | 73.3 | 76.7 | 62.8 | 38.6 "
    "| 77.0 |\n"
    "| Mixture-of-Agents (MoA) | 79.8 | 60.0 | 63.3 | 47.6 | 27.0 | "
    "57.5 |\n"
    "| TextGrad | 84.9 | 73.3 | 76.7 | 62.5 | 39.8 | 77.2 |\n"
    "| LoopLM | 84.6 | 66.7 | 63.3 | 48.1 | 24.9 | 56.4 |\n"
    "| Recursive-TextMAS | 85.8 | 73.3 | 73.3 | 61.6 | 38.7 | 77.0 |\n"
    "| **RecursiveMAS** | **88.0** | **86.7** | **86.7** | **66.2** "
    "| **42.9** | **79.3** |\n",
    title="Table 3: RecursiveMAS at r=3 vs single-agent / MAS / recursion baselines",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 3",
        "caption": "Table 3: RecursiveMAS at r=3 outperforms advanced single-agent, alternative MAS, and recursion-based baselines on all six benchmarks.",
    },
)

claim_avg_improvement_8_3 = claim(
    "**Average accuracy improvement = +8.3% over the strongest "
    "baseline on each benchmark.** Across the six Table-3 benchmarks, "
    "RecursiveMAS averages +8.3 pp over the *per-benchmark* strongest "
    "baseline, i.e., the column-wise winner among "
    "{Single-LoRA, Single-Full-SFT, MoA, TextGrad, LoopLM, "
    "Recursive-TextMAS} on each benchmark.",
    title="Result: +8.3% avg accuracy over per-column-strongest baseline (Table 3)",
)

claim_largest_gains_reasoning = claim(
    "**Largest gains over advanced architectures occur on reasoning-"
    "intensive tasks.** Compared with TextGrad (84.9 / 73.3 / 76.7 / "
    "62.5 on MATH500 / AIME25 / AIME26 / GPQA-D) and LoopLM (84.6 / "
    "66.7 / 63.3 / 48.1), RecursiveMAS lifts AIME2025 by **+13.4 pp** "
    "vs TextGrad and **+20.0 pp** vs LoopLM, AIME2026 by **+10.0 pp** "
    "vs TextGrad and **+23.4 pp** vs LoopLM, and GPQA-D by **+5.4 pp**. "
    "The narrative cites accuracy gains of **18.1% on AIME2025, 13.0% "
    "on AIME2026, and 5.4% on GPQA-Diamond** over the best of "
    "TextGrad / LoopLM panels.",
    title="Result: AIME +13-23 pp / GPQA +5.4 pp over TextGrad / LoopLM (reasoning-intensive concentration)",
)

claim_finetune_strengthens_singles = claim(
    "**Fine-tuning individual agents strengthens performance over "
    "off-the-shelf versions.** Within Table 3, both Single Agent "
    "(LoRA) and Single Agent (Full-SFT) outperform comparable un-"
    "fine-tuned reference points (e.g., Full-SFT 83.2 / 77.0 vs "
    "MoA 79.8 / 57.5 on MATH500 / MedQA), and RecursiveMAS delivers "
    "*further* gains on top by optimizing cross-agent collaboration "
    "at the system level rather than improving any single agent.",
    title="Result: SFT strengthens single agents; RecursiveMAS adds further system-level gain",
)

# ---------------------------------------------------------------------------
# Section 5.3: generality across collaboration patterns (Tables 6, 7, 8)
# ---------------------------------------------------------------------------

claim_table7_mixture = claim(
    "**Table 7: Mixture-Style RecursiveMAS vs each domain "
    "specialist** (accuracy %).\n\n"
    "| Method (Mixture) | AIME2026 | GPQA-Diamond | LiveCodeBench | "
    "MedQA |\n"
    "|---|---|---|---|---|\n"
    "| Math Specialist | 43.3 | 37.4 | 18.9 | 29.0 |\n"
    "| Code Specialist | 13.3 | 26.2 | 21.5 | 43.3 |\n"
    "| Science Specialist | 10.0 | 27.0 | 7.6 | 48.1 |\n"
    "| **RecursiveMAS** | **46.7** | **43.0** | **23.8** | **61.7** |\n",
    title="Table 7: Mixture-Style -- RecursiveMAS beats every domain specialist on all 4 benchmarks",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 7",
    },
)

claim_mixture_avg_gain = claim(
    "**Mixture-Style improvement = +6.2% on average over the "
    "strongest domain specialist per benchmark.** Across the four "
    "Table-7 benchmarks, RecursiveMAS averages +6.2 pp over the "
    "best per-column specialist (Math 43.3 -> 46.7 = +3.4; Science "
    "37.4 -> 43.0 = +5.6 vs Math 37.4; Code 21.5 -> 23.8 = +2.3 vs "
    "Code 21.5; MedQA 48.1 -> 61.7 = +13.6 vs Science 48.1).",
    title="Result: Mixture-Style RecursiveMAS = +6.2% avg over best per-column specialist",
)

claim_table6_distillation = claim(
    "**Table 6: Distillation-Style RecursiveMAS** (accuracy and "
    "end-to-end runtime in seconds).\n\n"
    "| Method (Distillation) | Metric | AIME2026 | GPQA-D | "
    "LiveCodeBench | MBPP+ | MedQA |\n"
    "|---|---|---|---|---|---|---|\n"
    "| Expert Model | Acc. | 90.0 | 72.7 | 46.2 | 73.4 | 86.0 |\n"
    "| Expert Model | Time | 9473 | 2558 | 9352 | 2342 | 2124 |\n"
    "| Learner Model | Acc. | 76.7 | 61.4 | 38.4 | 67.5 | 77.9 |\n"
    "| Learner Model | Time | 4495 | 1289 | 5396 | 1171 | 1183 |\n"
    "| **RecursiveMAS** | Acc. | **83.3** | **70.0** | **40.1** | "
    "**71.9** | **83.0** |\n"
    "| **RecursiveMAS** | Time | 5967 | 1671 | 6863 | 1516 | 1436 |\n",
    title="Table 6: Distillation-Style -- RecursiveMAS lifts Learner toward Expert at ~Learner runtime",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 6",
    },
)

claim_distillation_summary = claim(
    "**Distillation-Style: +8.0% Learner improvement at 1.5x speedup "
    "vs Expert.** Averaged across the five Table-6 benchmarks, "
    "RecursiveMAS lifts the Learner agent by **+8.0%** by distilling "
    "knowledge from the Expert, while retaining a **1.5x end-to-end "
    "speed advantage** over the Expert across all five tasks (e.g., "
    "AIME2026 5967 vs 9473 s, LiveCodeBench 6863 vs 9352 s).",
    title="Result: Distillation-Style RecursiveMAS = +8.0% over Learner, 1.5x speedup vs Expert",
)

claim_table8_deliberation = claim(
    "**Table 8: Deliberation-Style RecursiveMAS vs solo agents** "
    "(accuracy %).\n\n"
    "| Method (Deliberation) | AIME2026 | GPQA-D | HotpotQA | "
    "Bamboogle |\n"
    "|---|---|---|---|---|\n"
    "| Reflector | 76.7 | 61.2 | 27.5 | 40.9 |\n"
    "| Tool-Caller | 86.7 | 63.1 | 39.6 | 49.8 |\n"
    "| **RecursiveMAS** | **90.0** | **65.0** | **41.4** | **53.7** |\n",
    title="Table 8: Deliberation-Style -- RecursiveMAS beats both Reflector and Tool-Caller solo",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 8",
    },
)

claim_deliberation_summary = claim(
    "**Deliberation-Style: +4.8% improvement over the Tool-Caller "
    "agent.** Averaged across the four Table-8 benchmarks (AIME2026, "
    "GPQA-D, HotpotQA, Bamboogle), RecursiveMAS improves the "
    "stronger of the two solo agents (the Tool-Caller) by **+4.8 pp** "
    "(86.7 -> 90.0 = +3.3; 63.1 -> 65.0 = +1.9; 39.6 -> 41.4 = +1.8; "
    "49.8 -> 53.7 = +3.9). Recursive latent coordination remains "
    "effective even when the system includes external tool use.",
    title="Result: Deliberation-Style RecursiveMAS = +4.8% over Tool-Caller via iterative Reflector interaction",
)

# ---------------------------------------------------------------------------
# Section 5.1 scaling-law (Figure 1 Top)
# ---------------------------------------------------------------------------

claim_scaling_law_observation = claim(
    "**Scaling-law observation (Figure 1, Top): performance landscape "
    "over training x inference recursion depths.** Increasing "
    "inference depth continues to improve systems trained with fewer "
    "rounds (vertical scaling), while deeper training shifts the "
    "entire performance frontier upward (horizontal scaling). The "
    "strongest results consistently appear in the **upper-right "
    "region** where both training and inference recursion depths are "
    "large. This trend suggests a **complementary training-inference "
    "scaling effect**: training recursion progressively teaches the "
    "system to form refinement-ready latent states, and inference "
    "recursion translates this learned recursive structure into "
    "additional test-time gains.",
    title="Result: Fig. 1 (Top) -- complementary training x inference recursion scaling",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 1 (Top)",
        "caption": "Fig. 1 (Top): RecursiveMAS performance landscape over training-recursion x inference-recursion depths for the lightweight (sub-1.5B agents) Sequential-Style.",
    },
)

claim_scaling_law_speedups = claim(
    "**Per-pattern speedup callouts in the Figure 1 landscape.** "
    "Inset speedup labels in the four Figure 1 (Bottom) sub-panels "
    "report representative end-to-end speedups: 1.6x, 1.5x, 1.4x, "
    "1.5x, 1.5x across the four collaboration patterns under their "
    "respective training/inference depths. These are sub-panel-"
    "level speedups consistent with the overall 1.2x-2.4x range "
    "reported in the Section 5.4 efficiency tables.",
    title="Result: Fig. 1 per-pattern speedup callouts (1.4x-1.6x), consistent with overall 1.2x-2.4x range",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 1",
    },
)

__all__ = [
    "setup_nine_benchmarks",
    "setup_baselines",
    "setup_training_data",
    "setup_implementation_details",
    "claim_table2_full",
    "claim_avg_improvement_per_round",
    "claim_avg_improvement_text_baseline_section",
    "claim_consistent_upward_trend",
    "claim_math500_r3",
    "claim_aime25_r3",
    "claim_aime26_r3",
    "claim_gpqa_r3",
    "claim_medqa_r3",
    "claim_codegen_r3",
    "claim_table3",
    "claim_avg_improvement_8_3",
    "claim_largest_gains_reasoning",
    "claim_finetune_strengthens_singles",
    "claim_table7_mixture",
    "claim_mixture_avg_gain",
    "claim_table6_distillation",
    "claim_distillation_summary",
    "claim_table8_deliberation",
    "claim_deliberation_summary",
    "claim_scaling_law_observation",
    "claim_scaling_law_speedups",
]
