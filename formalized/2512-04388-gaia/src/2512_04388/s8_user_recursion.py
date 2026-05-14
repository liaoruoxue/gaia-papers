"""Section 4.4: User-Customization (Dynamic Worker Pool) + Test-Time
Recursive Scaling -- Figure 6 (open/closed pool generalization), Table 2
(recursive Conductor gains), Figure 10 (recursive worker redistribution),
plus the OOD few-shot finding (Table 4, Figure 9), the OOD zero-shot
generalization (Table 8).

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 4.4 + Appendix
B.2 + B.6 + B.10.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Dynamic worker pool results (Figure 6, Section 4.4)
# ---------------------------------------------------------------------------

claim_open_pool_finetuned = claim(
    "**Open-source-only pool: randomized-pool finetuned Conductor "
    "outperforms Claude Sonnet 4.** Evaluated with only open-source "
    "workers, the **randomized-pool finetuned Conductor outperforms "
    "Claude Sonnet 4 by almost 10%** within the constrained setting, "
    "effectively combining individually weaker open-source models with "
    "surprising efficacy. The pretrained-only Conductor relies on "
    "open-source models in very specific scenarios because of their "
    "significantly inferior individual performance; finetuning unlocks "
    "this regime.",
    title="Result: open-only finetuned Conductor beats Claude Sonnet 4 by ~10% (Fig. 6)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 6",
        "caption": "Fig. 6: Finetuned on randomized model pools, the Conductor achieves strong performance over rarely used open-model subsets while maintaining performance on closed-model subsets.",
    },
)

claim_closed_pool_finetuned = claim(
    "**Closed-source-only pool: finetuned Conductor matches pretrained "
    "performance.** When evaluated with only closed-source workers "
    "(Claude Sonnet 4, Gemini 2.5 Pro, GPT-5), the finetuned Conductor "
    "**entirely matches its original pretrained state-of-the-art "
    "performance**. The randomization-based finetuning **does not "
    "compromise** the model's original closed-pool capabilities.",
    title="Result: closed-only finetuned Conductor matches pretrained-Conductor SOTA (no compromise)",
)

claim_pool_generalization_thesis = claim(
    "**Conductor is not exclusively reliant on frontier-model "
    "performance.** The dynamic-pool results reveal a core capability: "
    "the Conductor's performance gains are **not exclusively reliant on "
    "the performance foundation of frontier models**. Indeed, the model "
    "displays **larger absolute gains when using a foundation with a "
    "larger room for improvement** (the open-only regime), consistent "
    "with the hypothesis that the Conductor amplifies its workers' "
    "complementary capabilities rather than free-riding on a single "
    "dominant worker.",
    title="Thesis: gains scale with worker-pool headroom (larger absolute gains on weaker pools)",
)

# ---------------------------------------------------------------------------
# Test-Time Recursive Scaling (Table 2)
# ---------------------------------------------------------------------------

claim_table2_recursion_full = claim(
    "**Table 2: Test-time recursion generates further performance "
    "gains** (constrained-setting evaluation of pretrained Conductor, "
    "recursive Conductor, and 7 individual workers on AIME25 / "
    "BigCodeBench / GPQA-D).\n\n"
    "| Model | AIME25 | BigCodeBench | GPQA-D | Avg. |\n"
    "|---|---|---|---|---|\n"
    "| gemma-3-27b-it | 6.67 | 10.8 | 33.33 | 16.93 |\n"
    "| Qwen3-32B | 23.33 | 23.0 | 54.05 | 33.46 |\n"
    "| Qwen3-32B (thinking) | 23.33 | 20.9 | 59.09 | 34.44 |\n"
    "| R1-Distill-Qwen-32B | 30.00 | 24.3 | 51.01 | 35.10 |\n"
    "| Gemini Pro 2.5 | 46.67 | 35.1 | 75.25 | 52.34 |\n"
    "| Claude Sonnet 4 | 35.33 | 35.8 | 67.30 | 46.14 |\n"
    "| GPT 5 | 46.67 | 33.8 | 72.73 | 51.73 |\n"
    "| **Conductor** | **66.67** | **37.8** | **81.31** | **61.93** |\n"
    "| **Conductor-Recursive** | **66.67** | **40.0** | **82.32** | **63.00** |\n\n"
    "Recursive Conductor adds **+1.07 pp average** over non-recursive "
    "Conductor, with the biggest gain on BigCodeBench (+2.2 pp) where "
    "GPT-5's surprising suboptimality requires online adaptation.",
    title="Table 2: Conductor-Recursive 63.00 avg vs Conductor 61.93 (+1.07 pp) on OOD constrained AIME25/BCB/GPQA-D",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 2",
        "caption": "Table 2: Test-time recursion generates further performance gains, especially on BigCodeBench where GPT-5 underperforms.",
    },
)

claim_recursion_bcb_redistribution = claim(
    "**Recursive worker redistribution on BigCodeBench.** When evaluated "
    "with recursion on BigCodeBench, the Conductor **adaptively "
    "redistributes its agent selection toward Claude Sonnet 4 and "
    "Gemini 2.5 Pro** in the recursive rounds, after observing the "
    "unexpectedly suboptimal behavior of GPT-5 (which is a strong "
    "coder on LiveCodeBench but weak on BigCodeBench's specific "
    "constraint-following requirements). This redistribution is the "
    "operational mechanism by which recursion translates online "
    "observations into improved coordination strategies.",
    title="Result: recursive Conductor redistributes from GPT-5 to Claude/Gemini on BCB (Fig. 10)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 10",
        "caption": "Fig. 10: Recursive Conductor worker distribution on BigCodeBench -- redistribution toward Claude and Gemini reflects their superior performance.",
    },
)

claim_recursion_aime25 = claim(
    "**Recursive Conductor on AIME25: no improvement (already saturated).** "
    "Recursive Conductor 66.67 = non-recursive 66.67 on AIME25 -- no gain, "
    "indicating that on this task the pretrained coordination strategy is "
    "already optimal and recursion correctly chooses to pass through "
    "(return three empty lists). This is an important *negative result* "
    "that demonstrates recursion's correct selectivity: it doesn't waste "
    "compute on already-good strategies.",
    title="Result: recursion gain = 0 on AIME25 (correctly passes through when initial strategy is already optimal)",
)

claim_recursion_gpqa = claim(
    "**Recursive Conductor on GPQA-D: small gain.** Recursive Conductor "
    "82.32 vs non-recursive 81.31 (+1.01 pp). A modest but consistent "
    "improvement on this OOD natural-science benchmark.",
    title="Result: recursion gain = +1.01 pp on GPQA-D",
)

claim_recursion_bcb = claim(
    "**Recursive Conductor on BigCodeBench: largest gain.** Recursive "
    "Conductor 40.0 vs non-recursive 37.8 (+2.2 pp). The BigCodeBench "
    "gain dominates the recursion experiment because GPT-5 underperforms "
    "on BCB's strict formatting/constraint-following requirements, "
    "creating room for the recursive Conductor to adapt away from its "
    "pretrained preferences.",
    title="Result: recursion gain = +2.2 pp on BigCodeBench (the headline recursion result)",
)

claim_recursion_dynamic_scaling_thesis = claim(
    "**Thesis: recursive Conductor demonstrates a new form of dynamic "
    "test-time scaling.** The recursion result -- conditioned on its "
    "previous output, the Conductor can adapt its agent selection and "
    "subtask breakdown to better suit unseen test scenarios -- "
    "constitutes a **new kind of test-time scaling axis**. Unlike "
    "open-ended chain-of-thought scaling (which expands the same "
    "computation along one axis), recursive Conductor scaling adds a "
    "qualitatively different axis: **iterative coordination "
    "re-planning** based on observed intermediate results.",
    title="Thesis: recursive Conductor = new test-time scaling axis -- iterative coordination re-planning",
)

# ---------------------------------------------------------------------------
# OOD few-shot finding (Table 4, Figure 9, Appendix B.2)
# ---------------------------------------------------------------------------

claim_ood_few_shot_finding = claim(
    "**OOD few-shot prompting boosts performance.** Conductor performance "
    "is **increasing in the proportion of few-shot examples taken from "
    "out-of-distribution tasks**. Best performance is attained when ALL "
    "few-shot examples are OOD relative to the target training tasks. "
    "Specifically (Table 4): on MATH500 / MMLU / RLPR / LiveCodeBench, "
    "**all-OOD** few-shot yields **89.33 / 93.14 / 42.63 / 64.29** vs "
    "**mixed** OOD+in-distribution **88.70 / 92.62 / 42.60 / 61.43** vs "
    "**all-in-distribution** **88.20 / 92.31 / 42.60 / 58.32**. The "
    "LiveCodeBench gain is the largest (+5.97 pp OOD vs in-distribution).",
    title="OOD few-shot result: 89.33/93.14/42.63/64.29 (all-OOD) > mixed > all-in-dist (Table 4)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 4 + Fig. 9",
        "caption": "Fig. 9 + Table 4: OOD few-shot examples improve Conductor performance -- best performance with all-OOD examples.",
    },
)

claim_ood_few_shot_explanation = claim(
    "**Posited mechanism for the OOD few-shot finding.** The OOD "
    "few-shot examples **prevent the Conductor from exploiting the "
    "provided strategies** (since the examples don't directly transfer "
    "to the target tasks) and instead **incentivize exploration of the "
    "coordination strategy space**. OOD examples deliver useful "
    "information about compatible agent combinations and formatting "
    "while isolating this information from reward-hackable strategies "
    "that can be lazily repeated.",
    title="Mechanism: OOD few-shot prevents exploitation, incentivizes exploration (anti-reward-hacking)",
)

# ---------------------------------------------------------------------------
# OOD zero-shot transfer in constrained setting (Table 8)
# ---------------------------------------------------------------------------

claim_table8_ood_constrained = claim(
    "**Table 8: OOD evaluation under cost constraints (constrained "
    "setting).** The Conductor delivers performance gains even on tasks "
    "*never seen during training*, in the same constrained setting it "
    "was trained under.\n\n"
    "| Model | AIME25 | BigCodeBench | GPQA-D | Avg. |\n"
    "|---|---|---|---|---|\n"
    "| R1-Distill-Qwen-32B | 30.00 | 24.3 | 51.01 | 35.10 |\n"
    "| gemma-3-27b-it | 6.67 | 10.8 | 33.33 | 16.93 |\n"
    "| Qwen3-32B (thinking) | 23.33 | 20.9 | 59.09 | 34.44 |\n"
    "| Qwen3-32B | 23.33 | 23.0 | 54.05 | 33.46 |\n"
    "| Gemini Pro 2.5 | 46.67 | 35.1 | 75.25 | 52.34 |\n"
    "| Claude Sonnet 4 | 35.33 | 35.8 | 67.30 | 46.14 |\n"
    "| GPT 5 | 46.67 | 33.8 | 72.73 | 51.07 |\n"
    "| **Conductor** | **66.67** | **37.8** | **81.31** | **61.93** |\n\n"
    "Conductor's +9-20 pp gains over its individual workers on these "
    "unseen tasks mirror the in-distribution findings of Section 4.3.",
    title="Table 8: OOD constrained -- Conductor 61.93 avg vs best worker Gemini 52.34 (+9.59 pp)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 8",
        "caption": "Table 8: Out-of-Distribution evaluation under cost constraints.",
    },
)

__all__ = [
    "claim_open_pool_finetuned",
    "claim_closed_pool_finetuned",
    "claim_pool_generalization_thesis",
    "claim_table2_recursion_full",
    "claim_recursion_bcb_redistribution",
    "claim_recursion_aime25",
    "claim_recursion_gpqa",
    "claim_recursion_bcb",
    "claim_recursion_dynamic_scaling_thesis",
    "claim_ood_few_shot_finding",
    "claim_ood_few_shot_explanation",
    "claim_table8_ood_constrained",
]
