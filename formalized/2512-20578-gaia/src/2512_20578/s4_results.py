"""Section 4: Experimental Results — Main Performance Benchmarks"""

from gaia.lang import claim, setting, support, compare, abduction, induction
from .motivation import internal_cues_exist, gnosis_proposal, external_judge_weakness
from .s2_background import reward_model_cost, internal_probe_weakness
from .s3_architecture import (
    total_params,
    constant_latency,
    frozen_backbone,
    training_protocol,
    hidden_circuit_arch,
    attention_circuit_arch,
    gated_fusion_arch,
)

# ── Evaluation Settings ────────────────────────────────────────────────────────

eval_domains = setting(
    "Evaluation is conducted on three disjoint test domains, none overlapping with training data: "
    "(1) Math Reasoning: AMC12, AIME24, AIME25, HMMT Feb 2025 competition problems. "
    "(2) Open-Domain QA: 18k held-out TriviaQA questions. "
    "(3) Academic Knowledge: MMLU-Pro across 14 subject domains. "
    "The math and trivia training data are entirely disjoint from these test sets.",
    title="Evaluation domains and test sets",
)

metrics_setting = setting(
    "Primary metrics: "
    "(1) AUROC — Area Under ROC Curve; higher is better, 1.0 is perfect. "
    "(2) AUPR-c — Area Under Precision-Recall Curve (correct-positive framing). "
    "(3) AUPR-e — Area Under Precision-Recall Curve (error-positive framing). "
    "(4) BSS — Brier Skill Score; measures calibration relative to a naive baseline; higher is better, 1.0 is perfect. "
    "(5) ECE — Expected Calibration Error; lower is better, 0.0 is perfect.",
    title="Evaluation metrics",
)

backbones_setting = setting(
    "Gnosis is evaluated on four frozen backbone LLMs: "
    "(1) Qwen3 1.7B-Hybrid, (2) Qwen3 4B-Thinking, (3) Qwen3 4B-Instruct, "
    "(4) OpenAI gpt-oss-20B (20 billion parameters). "
    "These span a range of 1.7B to 20B parameters.",
    title="Backbone LLMs evaluated",
)

baselines_setting = setting(
    "Baselines compared: "
    "(1) MLP-Prob: simple MLP probe on the final hidden state (internal, training-free variant). "
    "(2) Skywork-Reward-Gemma2-27B: large external reward model (27B parameters). "
    "(3) Skywork-Reward-Llama3.1-8B: 8B external reward model. "
    "(4) Gemini 2.5 Pro: proprietary large external judge model. "
    "Baselines span training-free probes, open-source reward models, and proprietary judges.",
    title="Baselines compared against Gnosis",
)

# ── Main Result Claims ─────────────────────────────────────────────────────────

gnosis_math_perf = claim(
    "Gnosis self-judge performance on math reasoning (AMC12 + AIME + HMMT) for each backbone:\n\n"
    "| Backbone | AUROC | AUPR-c | AUPR-e | BSS | ECE |\n"
    "|----------|-------|--------|--------|-----|-----|\n"
    "| Qwen3 1.7B-Hybrid | 0.95 | 0.95 | 0.94 | 0.59 | 0.09 |\n"
    "| Qwen3 4B-Thinking | 0.96 | 0.98 | 0.91 | 0.65 | 0.05 |\n"
    "| Qwen3 4B-Instruct | 0.93 | 0.96 | 0.89 | 0.51 | 0.08 |\n"
    "| OpenAI gpt-oss-20B | 0.85 | 0.86 | 0.86 | 0.38 | 0.04 |",
    title="Gnosis math reasoning performance (Table 1)",
    metadata={"source_table": "Table 1", "source_section": "Section 4.1"},
)

gnosis_trivia_perf = claim(
    "Gnosis self-judge performance on open-domain QA (TriviaQA held-out, 18k questions):\n\n"
    "| Backbone | AUROC | AUPR-c | AUPR-e | BSS | ECE |\n"
    "|----------|-------|--------|--------|-----|-----|\n"
    "| Qwen3 1.7B-Hybrid | 0.87 | 0.79 | 0.92 | 0.34 | 0.10 |\n"
    "| Qwen3 4B-Thinking | 0.89 | 0.89 | 0.88 | 0.45 | 0.05 |\n"
    "| Qwen3 4B-Instruct | 0.86 | 0.87 | 0.84 | 0.38 | 0.05 |\n"
    "| OpenAI gpt-oss-20B | 0.83 | 0.90 | 0.73 | 0.19 | 0.17 |",
    title="Gnosis TriviaQA performance (Table 1)",
    metadata={"source_table": "Table 1", "source_section": "Section 4.1"},
)

gnosis_mmlu_perf = claim(
    "Gnosis self-judge performance on academic knowledge (MMLU-Pro, 14 domains):\n\n"
    "| Backbone | AUROC | AUPR-c | AUPR-e | BSS | ECE |\n"
    "|----------|-------|--------|--------|-----|-----|\n"
    "| Qwen3 1.7B-Hybrid | 0.80 | 0.90 | 0.56 | 0.15 | 0.11 |\n"
    "| Qwen3 4B-Thinking | 0.82 | 0.93 | 0.55 | 0.21 | 0.05 |\n"
    "| Qwen3 4B-Instruct | 0.74 | 0.87 | 0.51 | 0.10 | 0.05 |\n"
    "| OpenAI gpt-oss-20B | 0.75 | 0.84 | 0.51 | 0.07 | 0.06 |",
    title="Gnosis MMLU-Pro performance (Table 1)",
    metadata={"source_table": "Table 1", "source_section": "Section 4.1"},
)

# External baselines for comparison
external_judge_perf = claim(
    "External baseline performance on math reasoning for Qwen3 1.7B evaluation: "
    "Skywork-Reward-8B AUROC 0.90; Gemini 2.5 Pro AUROC 0.91. "
    "On TriviaQA: Gemini 2.5 Pro AUROC 0.90. "
    "Skywork-Reward-27B achieves similar results to 8B variant. "
    "These external judges each have billions of parameters and require separate inference passes.",
    title="External baseline performance (Table 1)",
    metadata={"source_table": "Table 1", "source_section": "Section 4.1"},
)

mlp_probe_perf = claim(
    "MLP-Prob baseline (simple MLP on pooled final hidden state) performance on Qwen3 1.7B:\n\n"
    "| Domain | MLP-Prob AUROC | Gnosis AUROC | MLP-Prob ECE | Gnosis ECE |\n"
    "|--------|---------------|--------------|--------------|------------|\n"
    "| Math   | 0.86          | 0.95         | 0.19         | 0.09       |\n"
    "| TriviaQA | 0.71        | 0.87         | 0.21         | 0.10       |\n"
    "| MMLU-Pro | 0.69        | 0.80         | 0.23         | 0.11       |",
    title="MLP-Prob vs Gnosis performance (Table 2)",
    metadata={"source_table": "Table 2", "source_section": "Section 4.1"},
)

latency_comparison = claim(
    "Latency comparison for self-judgment at 12k and 24k token response lengths (Qwen3 1.7B, Math):\n\n"
    "| Method | 12k tokens latency | 12k AUROC | 24k tokens latency | 24k AUROC |\n"
    "|--------|---------------------|-----------|---------------------|-----------|\n"
    "| Gnosis | 25ms | 0.95 | 25ms | 0.94 |\n"
    "| Skywork-Reward-8B | 930ms | 0.90 | 2,465ms | 0.88 |\n\n"
    "Gnosis achieves 37× speedup over Skywork-8B at 12k tokens and 99× at 24k tokens, "
    "while also achieving higher AUROC.",
    title="Gnosis latency vs. reward model (Table 4)",
    metadata={"source_table": "Table 4", "source_section": "Section 4.2"},
)

calibration_quality = claim(
    "Gnosis produces sharp, bimodal score distributions: scores cluster near 0 for incorrect "
    "and near 1 for correct responses, with minimal overlap. External judges and reward models "
    "produce diffuse, overlapping score distributions with poor discrimination at the tails. "
    "Gnosis Brier Skill Score (BSS) on math (Qwen3 1.7B) is 0.59 vs. near-zero BSS for "
    "external baselines, indicating substantially better calibrated probability estimates.",
    title="Gnosis calibration superiority (bimodal distributions)",
    metadata={"source_section": "Section 4.1"},
)

# ── Abduction: Gnosis vs. External Judges ────────────────────────────────────

# For math reasoning on Qwen3 1.7B
pred_gnosis_math = claim(
    "Gnosis (trained on the target backbone's internal states) predicts "
    "AUROC 0.95, BSS 0.59, ECE 0.09 for math reasoning on Qwen3 1.7B, "
    "using only ~5M parameters and 25ms latency.",
    title="Gnosis math prediction for Qwen3 1.7B",
)

pred_ext_math = claim(
    "External judges (Skywork-Reward-8B at 0.90, Gemini 2.5 Pro at 0.91 AUROC) "
    "require billions of parameters and hundreds to thousands of milliseconds latency "
    "for the same math reasoning self-judgment task on Qwen3 1.7B.",
    title="External judge math performance for Qwen3 1.7B",
)

obs_math = claim(
    "The observed self-judgment accuracy on math reasoning (Qwen3 1.7B) is: "
    "Gnosis AUROC 0.95 vs. Skywork-8B AUROC 0.90 vs. Gemini 2.5 Pro AUROC 0.91, "
    "with Gnosis also achieving superior BSS (0.59) and ECE (0.09).",
    title="Observed math judgment benchmark result",
    metadata={"source_table": "Table 1", "source_section": "Section 4.1"},
)

s_gnosis_math = support(
    [pred_gnosis_math],
    obs_math,
    reason=(
        "Internal state access (@pred_gnosis_math) provides the backbone model's own "
        "discriminative signal, which should have direct access to the mechanisms causing "
        "errors — explaining the observation (@obs_math) of high AUROC."
    ),
    prior=0.88,
)

alt_external_math = claim(
    "External judges (reward models and proprietary LLMs) could explain the observed "
    "benchmark results at least as well as Gnosis, if their larger parameter counts "
    "provide richer scoring capability.",
    title="Alternative: external judges explain benchmark",
)

s_alt_math = support(
    [alt_external_math],
    obs_math,
    reason=(
        "Large external models (@alt_external_math) have seen vast training data and "
        "could in principle judge correctness at least as well — yet they don't explain "
        "the observation since their AUROC (0.90-0.91) is below Gnosis (0.95)."
    ),
    prior=0.35,
)

comp_math = compare(
    pred_gnosis_math,
    pred_ext_math,
    obs_math,
    reason=(
        "Gnosis AUROC 0.95 exceeds external judges (0.90-0.91) while using 1,600× fewer "
        "parameters and 37-99× less latency. The observation matches Gnosis predictions "
        "more closely in both ranking quality and calibration."
    ),
    prior=0.88,
)

abduction_math = abduction(
    s_gnosis_math,
    s_alt_math,
    comp_math,
    reason=(
        "Both Gnosis and external judges attempt to explain the same correctness "
        "discrimination task on math reasoning. Gnosis better explains the observed "
        "AUROC and calibration, supporting the hypothesis that internal state access "
        "provides superior correctness cues."
    ),
)

# ── Induction: Gnosis outperforms baselines across domains ────────────────────

gnosis_outperforms_math = claim(
    "Gnosis achieves higher AUROC than all compared baselines (MLP-Prob, Skywork-Reward-8B, "
    "Gemini 2.5 Pro) on math reasoning for Qwen3 1.7B: Gnosis 0.95 vs. best baseline 0.91.",
    title="Gnosis outperforms baselines on math",
    metadata={"source_table": "Table 1"},
)

gnosis_outperforms_trivia = claim(
    "Gnosis achieves higher AUROC than MLP-Prob on TriviaQA for Qwen3 1.7B (0.87 vs. 0.71), "
    "and achieves comparable AUROC to Gemini 2.5 Pro (0.87 vs. 0.90) while using "
    "negligible compute.",
    title="Gnosis outperforms or matches baselines on TriviaQA",
    metadata={"source_table": "Table 1"},
)

gnosis_outperforms_mmlu = claim(
    "Gnosis achieves higher AUROC than MLP-Prob on MMLU-Pro for Qwen3 1.7B (0.80 vs. 0.69), "
    "and outperforms or matches large external judges on this academic knowledge benchmark.",
    title="Gnosis outperforms baselines on MMLU-Pro",
    metadata={"source_table": "Table 1"},
)

gnosis_superior_overall = claim(
    "Gnosis consistently outperforms strong internal baselines (MLP-Prob) and large external "
    "judges (Skywork reward models, Gemini 2.5 Pro) in both accuracy (AUROC, AUPR) and "
    "calibration (BSS, ECE) across math reasoning, open-domain QA, and academic knowledge "
    "benchmarks, over frozen backbone LLMs ranging from 1.7B to 20B parameters.",
    title="Gnosis overall superiority claim",
    metadata={"source_section": "Abstract, Section 4"},
)

s_math_ind = support(
    [gnosis_superior_overall],
    gnosis_outperforms_math,
    reason=(
        "The general claim of superiority (@gnosis_superior_overall) predicts that Gnosis "
        "should outperform baselines specifically on math reasoning, which is confirmed "
        "by @gnosis_outperforms_math."
    ),
    prior=0.92,
)

s_trivia_ind = support(
    [gnosis_superior_overall],
    gnosis_outperforms_trivia,
    reason=(
        "The general superiority claim (@gnosis_superior_overall) predicts Gnosis should "
        "outperform baselines on TriviaQA, confirmed by @gnosis_outperforms_trivia."
    ),
    prior=0.88,
)

s_mmlu_ind = support(
    [gnosis_superior_overall],
    gnosis_outperforms_mmlu,
    reason=(
        "The general superiority claim (@gnosis_superior_overall) predicts Gnosis should "
        "outperform baselines on MMLU-Pro, confirmed by @gnosis_outperforms_mmlu."
    ),
    prior=0.85,
)

ind_math_trivia = induction(
    s_math_ind,
    s_trivia_ind,
    law=gnosis_superior_overall,
    reason=(
        "Math and TriviaQA are independent domains (different knowledge types, different "
        "model behaviors), providing independent evidence for @gnosis_superior_overall."
    ),
)

ind_all_three = induction(
    ind_math_trivia,
    s_mmlu_ind,
    law=gnosis_superior_overall,
    reason=(
        "MMLU-Pro provides a third independent domain (academic multi-choice) that further "
        "confirms the general superiority law."
    ),
)

# ── Latency advantage support ─────────────────────────────────────────────────

strat_latency_advantage = support(
    [constant_latency, total_params],
    latency_comparison,
    reason=(
        "Gnosis's constant ~25ms latency (@constant_latency) regardless of sequence length "
        "follows directly from its fixed-budget descriptor design, and its small footprint "
        "(@total_params, ~5M parameters) requires negligible GPU computation. "
        "This architectural property directly causes the 37× speedup at 12k tokens and "
        "99× speedup at 24k tokens shown in @latency_comparison."
    ),
    prior=0.94,
)

# ── Connect observation data to outperformance claims ─────────────────────────

strat_data_supports_math_out = support(
    [gnosis_math_perf, external_judge_perf, mlp_probe_perf],
    gnosis_outperforms_math,
    reason=(
        "The tabulated Gnosis math performance (@gnosis_math_perf, AUROC 0.95 for Qwen3 1.7B) "
        "directly exceeds all baselines in @external_judge_perf (Skywork-8B 0.90, Gemini 0.91) "
        "and @mlp_probe_perf (MLP-Prob 0.86), confirming @gnosis_outperforms_math."
    ),
    prior=0.97,
)

strat_data_supports_trivia_out = support(
    [gnosis_trivia_perf, mlp_probe_perf],
    gnosis_outperforms_trivia,
    reason=(
        "The tabulated Gnosis TriviaQA performance (@gnosis_trivia_perf, AUROC 0.87 for Qwen3 1.7B) "
        "exceeds MLP-Prob (0.71 per @mlp_probe_perf), confirming @gnosis_outperforms_trivia."
    ),
    prior=0.96,
)

strat_data_supports_mmlu_out = support(
    [gnosis_mmlu_perf, mlp_probe_perf],
    gnosis_outperforms_mmlu,
    reason=(
        "The tabulated Gnosis MMLU-Pro performance (@gnosis_mmlu_perf, AUROC 0.80 for Qwen3 1.7B) "
        "exceeds MLP-Prob (0.69 per @mlp_probe_perf), confirming @gnosis_outperforms_mmlu."
    ),
    prior=0.95,
)

strat_calibration_from_data = support(
    [gnosis_math_perf, mlp_probe_perf],
    calibration_quality,
    reason=(
        "Gnosis BSS of 0.59 on math (@gnosis_math_perf) vs MLP-Prob near-zero (@mlp_probe_perf) "
        "and Gnosis ECE of 0.09 vs MLP-Prob ECE of 0.19 demonstrate the sharp, bimodal score "
        "distributions described in @calibration_quality."
    ),
    prior=0.90,
)
