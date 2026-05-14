"""Section 4.3: Controlled Large-Scale Evaluation -- the constrained-setting
comparison against multi-agent baselines (Figure 4, Figure 5, Table 7) and
the efficiency analysis (Tables 5-6).

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 4.3 + Appendix
B.1 + B.4.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Constrained-setting protocol
# ---------------------------------------------------------------------------

setup_constrained_setting = setting(
    "**Constrained evaluation setting.** All agent workers are capped at "
    "**4096 output tokens** and reasoning budgets are set to their "
    "**minima**: 'minimal' for GPT-5, 128 for Gemini 2.5 Pro, 0 for "
    "Claude Sonnet 4, 'disabled' for Qwen3-32B (thinking). This is the "
    "identical configuration used to train the Conductor. AIME25 and "
    "GPQA-Diamond are evaluated with Lighteval [@Fourrier2023Lighteval]; "
    "BigCodeBench uses its original source repository.",
    title="Setup: constrained setting -- 4096 output cap + minimal reasoning, matches training-time config",
)

setup_baselines_controlled = setting(
    "**Controlled-comparison baselines.** The 7B Conductor is directly "
    "compared against:\n\n"
    "1. **Self-reflection** -- each agent is prompted up to **5 times** "
    "to revise its answer, keeping previous attempts in context "
    "[@Madaan2023SelfRefine; @Du2023MultiAgentDebate].\n"
    "2. **5x context length** -- each agent is given 5x the constrained "
    "output-token budget.\n"
    "3. **Four multi-agent baselines** -- MASRouter [@Yue2025MASRouter] "
    "(train classifier to select model+role from a pre-specified set), "
    "Mixture-of-Agents (MoA) [@Wang2024MoA] (single MoA + aggregator "
    "layer, 8 model calls), RouterDC [@Chen2024RouterDC] "
    "(contrastive-learned query-to-model router), Smoothie "
    "[@Guha2024Smoothie] (label-free routing, both independent and "
    "dependent variants).\n\n"
    "All multi-agent baselines use the **same 7-agent pool** as the "
    "Conductor.",
    title="Setup: baselines = 5x self-reflection + 5x context + 4 multi-agent (MASRouter/MoA/RouterDC/Smoothie)",
)

# ---------------------------------------------------------------------------
# Table 7 full controlled results (the verbatim numbers)
# ---------------------------------------------------------------------------

claim_table7_full = claim(
    "**Table 7: Full controlled-setting results across 4 in-domain "
    "benchmarks.** All numbers are mean accuracy +/- standard error. "
    "The Conductor outperforms all individual workers AND all multi-agent "
    "baselines.\n\n"
    "**Individual workers (4K context / minimal reasoning):**\n\n"
    "| Model | MATH500 | MMLU | RLPR | LCB | Avg. |\n"
    "|---|---|---|---|---|---|\n"
    "| Gemini Pro 2.5 (4K/128) | 85.30 | 91.53 | 39.57 | 40.14 | 64.14 |\n"
    "| Claude Sonnet 4 | 82.90 | 90.66 | 32.60 | 38.00 | 61.04 |\n"
    "| GPT 5 (4K/minimal) | 74.45 | 89.79 | 33.13 | 57.50 | 63.72 |\n"
    "| DeepSeek-R1-Distill-Qwen-32B | 78.50 | 84.41 | 32.75 | 24.86 | 48.95 |\n"
    "| gemma-3-27b-it | 37.45 | 63.58 | 14.93 | 7.21 | 30.79 |\n"
    "| Qwen3-32B (reasoning) | 76.85 | 83.28 | 34.35 | 31.21 | 56.42 |\n"
    "| Qwen3-32B (direct) | 73.15 | 84.02 | 30.60 | 26.79 | 53.64 |\n\n"
    "**5x context length (20K tokens) -- best individual is Gemini 2.5 Pro avg 67.60.**\n\n"
    "**5x self-reflection -- best individual is GPT-5 avg 64.52.**\n\n"
    "**Scaffolding / aggregation baselines:**\n\n"
    "| Method | MATH500 | MMLU | RLPR | LCB | Avg. |\n"
    "|---|---|---|---|---|---|\n"
    "| MASRouter | 80.60 | 86.28 | 32.80 | 27.86 | 56.89 |\n"
    "| MoA | 83.10 | 88.46 | 38.37 | 38.57 | 62.13 |\n"
    "| RouterDC | 59.25 | 87.52 | 27.53 | 35.33 | 52.41 |\n"
    "| Smoothie (Independent) | 76.85 | 83.28 | 34.35 | 31.21 | 56.42 |\n"
    "| Smoothie (Dependent) | 76.95 | 83.56 | 34.45 | 31.00 | 56.48 |\n"
    "| **Conductor (Ours)** | **89.33** | **93.14** | **42.63** | **64.29** | **72.35** |\n",
    title="Table 7: full controlled results -- Conductor avg 72.35 dominates all individuals + all multi-agent baselines",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 7",
        "caption": "Table 7: Self-reflection and multi-agent baseline comparison. Conductor outperforms all multi-agent baselines and all individual workers, including 5x context and 5x self-reflection variants.",
    },
)

claim_conductor_avg_controlled = claim(
    "**Conductor controlled-setting average = 72.35** vs best individual "
    "Gemini-2.5-Pro (4K) **64.14** (delta = +8.21 pp), vs best "
    "5x-context Gemini-2.5-Pro **67.60** (delta = +4.75 pp), vs best "
    "5x-self-reflection GPT-5 **64.52** (delta = +7.83 pp), vs best "
    "multi-agent MoA **62.13** (delta = +10.22 pp).",
    title="Result: Conductor 72.35 avg beats best worker (+8.21), 5x-context (+4.75), 5x-reflect (+7.83), best MAS (+10.22)",
)

claim_avg_workflow_steps = claim(
    "**Conductor average workflow length.** The Conductor learns to "
    "construct efficient agentic workflows with an **average of 3 "
    "steps**, **well below the requested limit of 5 steps**, despite "
    "being trained with no regularization on workflow length. This "
    "stands in contrast to MASRouter, which combines 4-5 different "
    "models and roles into extensive topological sequences.",
    title="Claim: average Conductor workflow = 3 steps (under 5 limit, no regularization)",
)

# ---------------------------------------------------------------------------
# Efficiency comparison (Table 5 -- consensus vs reflect)
# ---------------------------------------------------------------------------

claim_table5_efficiency_consensus = claim(
    "**Table 5: Efficiency vs 5x consensus inference-time scaling on "
    "MMLU.** Performance, average token usage, average cost (USD), and "
    "cost-adjusted performance (performance per cent of cost).\n\n"
    "| Model | Performance | Token Usage | Avg. Cost | Cost-adjusted |\n"
    "|---|---|---|---|---|\n"
    "| Claude 5x consensus | 91.00 | 1412.8 | 0.0211 | 42.94 |\n"
    "| Claude 5x reflect | 90.66 | 2517.0 | 0.0208 | 43.58 |\n"
    "| Gemini 5x consensus | 91.60 | 1658.4 | 0.01658 | 55.23 |\n"
    "| Gemini 5x reflect | 88.33 | 2919.8 | 0.01675 | 52.70 |\n"
    "| GPT 5 5x consensus | 91.30 | 1376.3 | 0.0138 | 66.34 |\n"
    "| GPT 5 5x reflect | 91.79 | 2457.1 | 0.0142 | 64.42 |\n"
    "| **Conductor** | **93.14** | **735.2** | **0.009** | **103.49** |\n\n"
    "The Conductor uses **fewer tokens** and **lower cost** than every "
    "consensus baseline while achieving **higher accuracy**, yielding "
    "a cost-adjusted performance of **103.49 -- 1.56x the best baseline** "
    "(GPT-5 5x consensus 66.34).",
    title="Table 5: Conductor MMLU 93.14 at 735 tokens / $0.009 -- 1.56x cost-adjusted vs best 5x consensus",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 5",
        "caption": "Table 5: Efficiency comparison with 5x inference-time scaling (consensus vs. reflect) on MMLU. The Conductor outperforms consensus while offering substantial efficiency gains.",
    },
)

claim_table6_efficiency_baselines = claim(
    "**Table 6: Efficiency vs multi-agent baselines (4-way training-task "
    "average).** Average performance, token usage, and cost per sample, "
    "averaged over MMLU/RLPR/LiveCodeBench/MATH500.\n\n"
    "| Model | Performance | Token Usage | Cost |\n"
    "|---|---|---|---|\n"
    "| MoA | 62.13 | 11203 | 0.04855 |\n"
    "| Smoothie | 56.48 | 9909 | 0.03929 |\n"
    "| RouterDC | 52.41 | 840 | 0.00561 |\n"
    "| MASRouter | 56.89 | 4970 | 0.01345 |\n"
    "| **Conductor** | **72.35** | **1820** | **0.02384** |\n\n"
    "Conductor outperforms all multi-agent baselines by large margins "
    "(+10 to +20 pp) at the **second-lowest token usage** (only RouterDC "
    "uses fewer tokens, with 20 pp worse accuracy) and **moderate cost**.",
    title="Table 6: Conductor 72.35 perf / 1820 tokens / $0.024 -- 2nd lowest tokens + highest perf among MAS",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 6",
        "caption": "Table 6: Efficiency comparison across multi-agent baselines. Conductor attains lowest tokens at highest performance.",
    },
)

# ---------------------------------------------------------------------------
# Failure-mode analyses (Appendix B.5)
# ---------------------------------------------------------------------------

claim_moa_failure_mode = claim(
    "**MoA failure mode on LiveCodeBench.** MoA underperforms GPT-5 on "
    "LiveCodeBench (38.57 vs 57.50 for GPT-5 alone). Examination of the "
    "evaluation logs reveals that **MoA's performance hinges on its "
    "ability to discern correct vs incorrect candidate solutions among "
    "its 7 candidate responses**. On tasks with high variance in worker "
    "capability and very large solution spaces (e.g., writing optimized "
    "code), MoA is often misled by incorrect solutions of less capable "
    "models. Tasks where worker models are closer in capability "
    "(MATH500/MMLU) see better MoA performance.",
    title="Claim: MoA fails on LCB because correctness-discernment is hard when worker capability variance is high",
)

claim_masrouter_failure_mode = claim(
    "**MASRouter failure mode.** MASRouter relies on **human-engineered "
    "scaffolding** with careful manual placement of selected models in "
    "specific roles. With the Conductor's wider 7-worker pool, "
    "MASRouter struggles to determine which model is best for each "
    "task. Its fixed prompt templates and scaffolds limit generality "
    "beyond the domains they were designed for. By contrast, the "
    "Conductor uses no human-designed fixed prompts.",
    title="Claim: MASRouter fails due to fixed scaffolds + manual role design, brittle across the wider 7-worker pool",
)

# ---------------------------------------------------------------------------
# Cross-baseline summary
# ---------------------------------------------------------------------------

claim_controlled_summary = claim(
    "**Controlled-comparison summary.** With the sole exception of "
    "RouterDC, **all baseline methods in the controlled comparison have "
    "a strictly higher inference cost than the Conductor**. MASRouter's "
    "performance depends on expensive human-designed agentic "
    "coordination combining 4-5 different models in topological "
    "sequences; MoA uses 8 model calls; 5x self-reflection multiplies "
    "agent budget by 5. The Conductor's average 3-step workflows give "
    "it **strictly better cost-vs-accuracy Pareto position** on every "
    "in-domain task.",
    title="Claim: Conductor Pareto-dominates on cost-vs-accuracy in the controlled setting",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 4 + Fig. 5",
        "caption": "Fig. 4: Conductor surpasses all baselines by substantive margins. Fig. 5: Performance vs Efficiency -- Conductor far surpasses multi-agent baselines at a fraction of the cost.",
    },
)

__all__ = [
    "setup_constrained_setting",
    "setup_baselines_controlled",
    "claim_table7_full",
    "claim_conductor_avg_controlled",
    "claim_avg_workflow_steps",
    "claim_table5_efficiency_consensus",
    "claim_table6_efficiency_baselines",
    "claim_moa_failure_mode",
    "claim_masrouter_failure_mode",
    "claim_controlled_summary",
]
