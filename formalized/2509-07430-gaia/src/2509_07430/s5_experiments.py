"""Section 5: Experiments — SQL and Math Reasoning Benchmarks"""

from gaia.lang import claim, setting

from .motivation import (
    pass_at_k_setting,
    passk_degrades,
    catastrophic_forgetting,
    mass_covering_preserves,
)
from .s2_background import (
    grpo_objective,
    dapo_objective,
    forward_kl_mass_covering,
    js_mass_covering,
    rkl_mode_seeking_harm,
)
from .s3_method import dphrl_objective, dataset_partition, generator_method

# ── Settings ──────────────────────────────────────────────────────────────────

sql_experiment_setup = setting(
    "SQL experiments use Llama-3.1-8B-Instruct as the base model. Training data is "
    "sourced from the Spider and BIRD SQL datasets. Evaluation metrics: Pass@1 (greedy "
    "accuracy), Pass@8, and Pass@16 on in-domain Spider and BIRD test sets. "
    "Out-of-domain evaluation uses 6 math benchmarks: AIME24, AMC23, Math500, "
    "Olympiad, Minerva, and College Math.",
    title="SQL experiment setup",
)

math_experiment_setup = setting(
    "Mathematical reasoning experiments use two base models: Llama-3.1-8B-Instruct "
    "and Qwen2.5-Math-7B. Training data is from math competition datasets. Evaluation "
    "metrics: Pass@1 (greedy), Pass@8, Pass@16, Pass@64 on AIME24 benchmark.",
    title="Math experiment setup",
)

baselines = setting(
    "Compared baselines: (1) Base model (no fine-tuning), (2) GRPO (no KL constraint), "
    "(3) DAPO (decoupled clip, no divergence), (4) RKL (PPO with reverse-KL penalty), "
    "(5) DPH-F (DPH-RL with forward-KL), (6) DPH-JS (DPH-RL with Jensen-Shannon, $\\eta=0.2$). "
    "All methods trained for the same number of steps on the same dataset.",
    title="Compared baselines",
)

# ── Claims: SQL In-domain Results ─────────────────────────────────────────────

sql_bird_results = claim(
    "On the BIRD SQL in-domain benchmark (Llama-3.1-8B-Instruct), Pass@8 and Pass@16 results are:\n\n"
    "| Method | Pass@8 | Pass@16 |\n"
    "|--------|--------|---------|\n"
    "| Base Model | 68.8 | 75.0 |\n"
    "| GRPO | 66.2 | 67.7 |\n"
    "| DAPO | 67.2 | 69.0 |\n"
    "| RKL | 69.8 | 71.8 |\n"
    "| DPH-F | 70.1 | 71.6 |\n"
    "| DPH-JS ($\\eta=0.2$) | 70.5 | 72.4 |\n\n"
    "GRPO and DAPO fall below the base model on Pass@8 and Pass@16, confirming diversity "
    "collapse. DPH-JS achieves the highest Pass@8 (70.5), 4.3 points above GRPO (66.2) "
    "and 1.7 points above the base model (68.8).",
    title="BIRD SQL: Pass@k results",
    metadata={"source_table": "artifacts/2509.07430.pdf, Table 1"},
)

sql_spider_results = claim(
    "On the Spider SQL dataset (cross-domain evaluation, Llama-3.1-8B-Instruct), "
    "Pass@8 and Pass@16 results are:\n\n"
    "| Method | Pass@8 | Pass@16 |\n"
    "|--------|--------|---------|\n"
    "| Base Model | 90.9 | 93.2 |\n"
    "| GRPO | 79.5 | 80.6 |\n"
    "| DAPO | 75.3 | 76.7 |\n"
    "| DPH-F | 84.5 | 85.7 |\n"
    "| DPH-JS ($\\eta=0.2$) | 82.7 | 84.1 |\n\n"
    "GRPO and DAPO show severe Pass@k degradation (−11.4 and −15.6 Pass@8 respectively "
    "vs. base). DPH-F recovers 5.0 Pass@8 points vs. GRPO; Pass@16 improvement over "
    "DAPO is 9.0 points (85.7 vs. 76.7 for DPH-F).",
    title="Spider SQL: Pass@k results",
    metadata={"source_table": "artifacts/2509.07430.pdf, Table 1"},
)

# ── Claims: Out-of-domain Math Results ────────────────────────────────────────

ood_math_results = claim(
    "Out-of-domain math evaluation on SQL-trained Llama-3.1-8B-Instruct models "
    "(average across AIME24, AMC23, Math500, Olympiad, Minerva, College Math):\n\n"
    "| Method | Avg. OOD Math Score |\n"
    "|--------|--------------------|\n"
    "| Base Model | 60.35 |\n"
    "| GRPO | 52.37 |\n"
    "| DAPO | 52.63 |\n"
    "| RKL | 48.45 |\n"
    "| DPH-F | 60.98 |\n"
    "| DPH-JS | 60.23 |\n\n"
    "DPH-F and DPH-JS recover essentially all base-model out-of-domain capability "
    "(60.98 and 60.23 vs. 60.35 base), whereas GRPO/DAPO lose ~8 points and RKL loses ~12 points.",
    title="Out-of-domain math: catastrophic forgetting results",
    metadata={"source_table": "artifacts/2509.07430.pdf, Table 2"},
)

# ── Claims: Math Reasoning Results ────────────────────────────────────────────

math_llama_results = claim(
    "Mathematical reasoning results on AIME24 with Llama-3.1-8B-Instruct:\n\n"
    "| Method | Pass@64 | Pass@16 | Pass@8 |\n"
    "|--------|---------|---------|--------|\n"
    "| Base Model | 40.0 | 23.3 | 95.0 |\n"
    "| GRPO | 33.3 | 26.7 | 80.0 |\n"
    "| DPH-F | 36.7 | 26.7 | 90.0 |\n"
    "| DPH-JS | 40.0 | 26.7 | 82.5 |\n\n"
    "GRPO degrades Pass@64 from 40.0 to 33.3 (−6.7). DPH-JS recovers Pass@64 fully "
    "to 40.0 while also improving Pass@16 from 23.3 to 26.7.",
    title="Math reasoning (Llama-3.1-8B): Pass@k results",
    metadata={"source_table": "artifacts/2509.07430.pdf, Table 3"},
)

math_qwen_results = claim(
    "Mathematical reasoning results on AIME24 with Qwen2.5-Math-7B:\n\n"
    "| Method | Pass@64 | Pass@16 | Pass@8 |\n"
    "|--------|---------|---------|--------|\n"
    "| Base Model | 63.3 | 56.7 | 87.5 |\n"
    "| GRPO | 56.6 | 50.0 | 97.5 |\n"
    "| DPH-F | 73.33 | 50.0 | 97.5 |\n"
    "| DPH-JS | 66.7 | 53.3 | 100.0 |\n\n"
    "DPH-F achieves the highest Pass@64 at 73.33 (+10.0 vs. base, +16.7 vs. GRPO). "
    "DPH-JS achieves Pass@8 = 100.0 (perfect). Both DPH variants improve Pass@64 "
    "substantially over GRPO while maintaining or exceeding GRPO's Pass@8.",
    title="Math reasoning (Qwen2.5-Math-7B): Pass@k results",
    metadata={"source_table": "artifacts/2509.07430.pdf, Table 3"},
)

# ── Claims: Diversity Analysis ─────────────────────────────────────────────────

solution_style_diversity = claim(
    "Qualitative analysis of solution styles (Figure 4 of the paper) shows that "
    "reverse-KL trained models converge to generating solutions in a single stylistic "
    "format (e.g., only one SQL join pattern or one proof structure), while forward-KL "
    "and JS-divergence trained models produce multiple distinct solution styles for the "
    "same query, confirming the mass-covering property preserves stylistic diversity.",
    title="Solution style diversity: reverse-KL vs forward-KL",
    metadata={"figure": "artifacts/2509.07430.pdf, Figure 4",
              "caption": "Fig. 4: Solution style comparison across divergence types."},
)

capability_retention = claim(
    "Capability retention analysis (Figure 3 of the paper) shows that GRPO/DAPO lose "
    "approximately 15% of base model capabilities (measured by out-of-domain benchmark "
    "performance drop) while DPH-JS retains 85%+ of base model capabilities. "
    "RKL causes 85% out-of-domain performance collapse in the most severe cases "
    "(SQL-domain specialization with out-of-domain math).",
    title="Capability retention: DPH-JS vs GRPO/RKL",
    metadata={"figure": "artifacts/2509.07430.pdf, Figure 3",
              "caption": "Fig. 3: Capability retention under different divergence types."},
)

__all__ = [
    "sql_bird_results",
    "sql_spider_results",
    "ood_math_results",
    "math_llama_results",
    "math_qwen_results",
    "solution_style_diversity",
    "capability_retention",
]
