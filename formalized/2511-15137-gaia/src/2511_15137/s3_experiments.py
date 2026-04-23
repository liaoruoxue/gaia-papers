"""Section 3: Experimental Setup and Results"""

from gaia.lang import claim, setting

from .motivation import verification_gap, verification_training_neglect
from .s2_method import grpo_verif_objective, alpha_hyperparameter

# --- Experimental setup ---

setting_model = setting(
    "Base model: Qwen2.5-3B, a 3-billion parameter language model from the Qwen2.5 series. "
    "All experiments use this single model size.",
    title="Base model: Qwen2.5-3B",
)

setting_training_data = setting(
    "Training data: 6,000 problems sampled from DAPO-Math-17k, a mathematical problem dataset "
    "used in DAPO (Direct Alignment from Preference Optimization) training.",
    title="Training data",
)

setting_benchmarks = setting(
    "Evaluation benchmarks (four datasets):\n\n"
    "| Benchmark | Description |\n"
    "|-----------|-------------|\n"
    "| AMC23 | American Mathematics Competition 2023 |\n"
    "| MATH | MATH dataset (mathematics problems) |\n"
    "| Minerva_Math | Minerva mathematics benchmark |\n"
    "| OlympiadBench | Olympiad-level mathematics problems |",
    title="Evaluation benchmarks",
)

setting_hyperparameters = setting(
    "Training hyperparameters:\n\n"
    "| Parameter | Value |\n"
    "|-----------|-------|\n"
    "| Learning rate | $1 \\times 10^{-6}$ |\n"
    "| Batch size | 32 |\n"
    "| KL penalty $\\beta$ | 0 (disabled) |\n"
    "| Clipping threshold $\\epsilon$ | 0.28 |\n"
    "| Number of generations $n$ | 8 |\n"
    "| Verification weight $\\alpha$ | 0.2 |\n"
    "| Max completion length | 2048 tokens |\n"
    "| Sampling temperature (training) | 1 |\n"
    "| Sampling temperature (evaluation) | 0 (greedy) |",
    title="Training hyperparameters",
)

setting_baselines = setting(
    "Three comparison conditions:\n\n"
    "1. **Default**: Qwen2.5-3B without any RL fine-tuning (zero-shot baseline)\n"
    "2. **GRPO**: Qwen2.5-3B fine-tuned with standard GRPO (solution generation only, $\\alpha=0$)\n"
    "3. **GRPO-Verif**: Qwen2.5-3B fine-tuned with the proposed joint objective ($\\alpha=0.2$)\n\n"
    "Both solution accuracy and verification accuracy are reported for all three conditions.",
    title="Comparison baselines",
)

# --- Results: solution accuracy ---

result_solution_accuracy = claim(
    "Solution accuracy results across four benchmarks (Table 1, solution task rows):\n\n"
    "| Method | AMC23 | MATH | Minerva_Math | OlympiadBench | AVG |\n"
    "|--------|-------|------|--------------|---------------|-----|\n"
    "| Default (no RL) | 27.5% | 52.7% | 11.0% | 21.0% | 28.1% |\n"
    "| GRPO | 45.0% | 63.4% | 19.5% | 25.8% | 38.4% |\n"
    "| GRPO-Verif | 45.0% | 63.2% | 18.8% | 26.8% | 38.5% |\n\n"
    "GRPO-Verif achieves average solution accuracy of 38.5%, compared to GRPO's 38.4% — "
    "a difference of 0.1 percentage points.",
    title="Solution accuracy comparison",
    background=[setting_model, setting_benchmarks, setting_baselines],
    metadata={"source_table": "artifacts/2511.15137.pdf, Table 1"},
)

result_verification_accuracy = claim(
    "Verification accuracy results across four benchmarks (Table 1, verification task rows):\n\n"
    "| Method | AMC23 | MATH | Minerva_Math | OlympiadBench | AVG |\n"
    "|--------|-------|------|--------------|---------------|-----|\n"
    "| Default (no RL) | 12.5% | 26.4% | 10.3% | 15.6% | 16.2% |\n"
    "| GRPO | 25.0% | 57.7% | 21.0% | 27.7% | 32.9% |\n"
    "| GRPO-Verif | 40.0% | 60.7% | 19.9% | 27.8% | 37.1% |\n\n"
    "GRPO-Verif achieves average verification accuracy of 37.1%, compared to GRPO's 32.9% — "
    "an improvement of 4.2 percentage points.",
    title="Verification accuracy comparison",
    background=[setting_model, setting_benchmarks, setting_baselines],
    metadata={"source_table": "artifacts/2511.15137.pdf, Table 1"},
)

# --- Derived result claims ---

grpo_improves_over_default_solution = claim(
    "GRPO training improves solution accuracy over the untuned default by 10.3 percentage points "
    "on average (28.1% → 38.4%), demonstrating that RL fine-tuning substantially improves "
    "mathematical problem solving on the Qwen2.5-3B model.",
    title="GRPO solution improvement over default",
)

grpo_improves_over_default_verification = claim(
    "GRPO training improves verification accuracy over the untuned default by 16.7 percentage points "
    "on average (16.2% → 32.9%), showing that even solution-only RL training incidentally "
    "improves verification ability.",
    title="GRPO verification improvement over default",
)

grpo_verif_maintains_solution = claim(
    "GRPO-Verif maintains solution accuracy statistically equivalent to standard GRPO: "
    "38.5% vs 38.4% average (difference of 0.1 percentage points). The joint verification "
    "objective does not degrade solution generation capability.",
    title="GRPO-Verif maintains solution accuracy",
)

grpo_verif_improves_verification = claim(
    "GRPO-Verif improves average verification accuracy from 32.9% (GRPO) to 37.1% "
    "(GRPO-Verif), a gain of 4.2 percentage points. The largest single-benchmark gain "
    "is on AMC23: 25.0% → 40.0% (+15 percentage points).",
    title="GRPO-Verif improves verification accuracy",
)

grpo_verif_amc23_verification = claim(
    "On AMC23, GRPO-Verif achieves verification accuracy of 40.0% compared to GRPO's 25.0%, "
    "an improvement of 15 percentage points — the largest benchmark-level gain across all datasets.",
    title="GRPO-Verif AMC23 verification improvement",
    metadata={"source_table": "artifacts/2511.15137.pdf, Table 1"},
)

computational_overhead = claim(
    "GRPO-Verif incurs additional computational cost compared to standard GRPO because it "
    "must generate verification responses for each solution in addition to the solution itself. "
    "This doubles the generation cost per training step. The paper acknowledges this as a "
    "limitation requiring future optimization.",
    title="Computational overhead of GRPO-Verif",
    background=[setting_hyperparameters],
)
