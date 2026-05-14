"""Section 4.5: Analyses + Appendix B.7-B.10 ablations -- Conductor scale,
task adaptivity, subtask ablation, agent-selection ablation, Conductor
replacement ablation, few-shot ablation, alternate fine-grained topology,
performance-diversity case studies.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 4.5 + Appendix
B.7-B.10.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Section 4.5 -- Conductor scale (Figure 7)
# ---------------------------------------------------------------------------

claim_3b_same_agent_dist = claim(
    "**Conductor scale: 3B and 7B converge to the same agent-selection "
    "distribution.** Training a smaller 3B-parameter Conductor following "
    "the same recipe yields, as training progresses, **convergence to "
    "the same distribution of worker agents** as the 7B Conductor -- "
    "both models eventually concentrate selection on the three most "
    "powerful workers (Gemini 2.5 Pro, Claude Sonnet 4, GPT-5).",
    title="Scale result: 3B Conductor converges to same agent-distribution as 7B Conductor (Fig. 7 left)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 7 (left)",
        "caption": "Fig. 7 (left): 3B Conductor agent distribution converges on the three most powerful models.",
    },
)

claim_7b_better_prompt_engineering = claim(
    "**Conductor scale: 7B Conductor outperforms 3B via better prompt "
    "engineering.** Despite matching agent selection, the **7B Conductor "
    "maintains a clear performance edge over 3B at the end of training**, "
    "even when both use identical agent assignments. Comparing subtasks "
    "produced by 7B (Fig. 3) and 3B (Fig. 15), the paper traces this gap "
    "to the **larger model's superior prompt-engineering skills**: the "
    "3B Conductor produces workable but suboptimal subtasks (e.g., "
    "instructing the first model to hide its reasoning in tags due to a "
    "user formatting constraint, impairing collaboration).",
    title="Scale result: 7B outperforms 3B via better prompt engineering (Fig. 7 right + Fig. 15 example)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 7 (right) + Fig. 15",
        "caption": "Fig. 7 (right): Conductor scale -- 7B yields additional performance gains via prompt engineering even at identical agent selection.",
    },
)

claim_scale_thesis = claim(
    "**Conductor-scale thesis: new axis for scaling multi-agent "
    "coordination.** The 3B-vs-7B comparison opens a new axis for "
    "**scaling multi-agent coordination** far beyond prior routing "
    "efforts: the increased natural-language capability of larger base "
    "Conductor models **directly translates** into more intelligent "
    "prompt engineering, unlocking a new level of agency over each "
    "worker. This thesis supports the view that removing manual "
    "constraints on subtask specification (i.e., the natural-language "
    "medium of the Conductor) is critical for scaling.",
    title="Thesis: removing manual subtask constraints opens a new scaling axis -- larger Conductors scale prompt engineering",
)

# ---------------------------------------------------------------------------
# Section 4.5 -- Task adaptivity (Figure 8)
# ---------------------------------------------------------------------------

claim_workflow_step_distribution = claim(
    "**Task-adaptive workflow-step distribution (Figure 8).** As "
    "training progresses, the Conductor learns to:\n\n"
    "- **MMLU** (simpler factual / comprehension): typically **1-2 "
    "steps** of targeted information retrieval; often a single agent "
    "suffices.\n"
    "- **LiveCodeBench** (complex code generation): typically **3-4 "
    "steps**, deploying multiple planners followed by an implementer "
    "and a verifier.\n\n"
    "The model **explicitly reasons about task complexity** in its "
    "chain-of-thought before specifying its workflow -- 'this is a "
    "straightforward comprehension task, so we only need one model' "
    "(Fig. 18 example) vs 'we need 5 models: understand problem, "
    "analyze graph, develop strategy, implement, validate' (Fig. 20 "
    "example).",
    title="Adaptivity result: 1-2 steps on MMLU vs 3-4 steps on LCB; explicit task-complexity reasoning",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 8 + Figs. 18, 20",
        "caption": "Fig. 8: Task adaptivity -- workflow step distributions for MMLU (2 agents typical) vs LiveCodeBench (3-4 agents).",
    },
)

# ---------------------------------------------------------------------------
# Appendix B.7 -- Ablation studies (Tables 9, 10, 11)
# ---------------------------------------------------------------------------

claim_table9_ablations = claim(
    "**Table 9: Three ablations on subtasks / few-shot / fine-grained "
    "topology** (in-domain MATH500 / MMLU / RLPR / LiveCodeBench).\n\n"
    "| Model | MATH500 | MMLU | RLPR | LiveCodeBench |\n"
    "|---|---|---|---|---|\n"
    "| fine-grained topology | 88.67 | 93.55 | 42.28 | 61.24 |\n"
    "| w/o few-shot | 82.00 | 92.69 | 41.50 | 54.86 |\n"
    "| w/o subtasks | 88.5 | 92.75 | 41.95 | 58.62 |\n"
    "| **Conductor (Ours)** | **89.33** | **93.14** | **42.63** | **64.29** |\n\n"
    "Each ablation drops performance on at least 3 of 4 columns "
    "(Conductor wins on MATH500, RLPR, LCB; fine-grained wins on MMLU "
    "by 0.41 pp).",
    title="Table 9: ablation drops -- no few-shot worst (LCB -9.43), no subtasks (LCB -5.67), fine-grained marginal",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 9",
        "caption": "Table 9: Ablation studies on subtasks, few-shot conditioning, and utilizing fine-grained complex topology specification.",
    },
)

claim_subtask_ablation = claim(
    "**Subtask ablation result.** When the Conductor is retrained with "
    "subtask-prompt-engineering disabled (all selected models receive "
    "the uniform prompt `'Solve the user question'`, so the Conductor "
    "only learns model selection + topology), performance drops "
    "consistently across all four in-domain tasks, with the **largest "
    "drop on LiveCodeBench** (64.29 -> 58.62 = **-5.67 pp**). Other "
    "drops: MATH500 -0.83, MMLU -0.39, RLPR -0.68. The pattern reveals "
    "that **careful, targeted prompt engineering matters most when task "
    "complexity is high**, particularly for tasks requiring strict "
    "constraint-following and formatting (like LCB code generation).",
    title="Ablation: removing subtasks costs -5.67 pp on LCB (constraint-heavy); only -0.5 to -0.8 on simpler tasks",
)

claim_few_shot_ablation = claim(
    "**Few-shot ablation result.** Removing the few-shot examples from "
    "the Conductor's system prompt (no exemplar workflows) causes "
    "**substantial performance drops across all four in-domain tasks**: "
    "MATH500 89.33 -> 82.00 (-7.33 pp), MMLU 93.14 -> 92.69 (-0.45), "
    "RLPR 42.63 -> 41.50 (-1.13), LiveCodeBench 64.29 -> 54.86 (-9.43 "
    "pp). This **mirrors prior work in SFT cold-starting** where "
    "conditioning the generative distribution before RL has been "
    "widely observed to improve performance.",
    title="Ablation: removing few-shot costs -7.33 (MATH500) and -9.43 pp (LCB); standard cold-start finding",
)

claim_fine_grained_topology_ablation = claim(
    "**Fine-grained topology ablation: no significant gain.** A variant "
    "where the Conductor can specify, for each agent, *which specific "
    "positions* in the topology should be visible (e.g., `[0, 2, 3]` "
    "instead of just `\"all\"` or `[]`) is a strict generalization of "
    "the binary access scheme. Empirically the Conductor learns to use "
    "the more complex scheme effectively (discovering tree/chain "
    "topologies), but the **fine-grained scheme does not produce "
    "significant performance gains** over the simpler binary version "
    "(MATH500 88.67 vs 89.33 = -0.66; MMLU 93.55 vs 93.14 = +0.41; "
    "RLPR 42.28 vs 42.63 = -0.35; LCB 61.24 vs 64.29 = -3.05). The "
    "paper opts for the simpler binary version in the main text.",
    title="Ablation: fine-grained topology generalization -- no significant gain at 7B; possible at larger scale",
)

claim_table10_agent_selection_ablation = claim(
    "**Table 10: Agent-selection ablation -- 'Conductor w/ all GPT-5'** "
    "fixes every worker to GPT-5.\n\n"
    "| Model | AIME | BCB | GPQA-D | Avg. |\n"
    "|---|---|---|---|---|\n"
    "| Claude Sonnet 4 | 74.30 | 37.16 | 77.70 | 63.05 |\n"
    "| Gemini 2.5 Pro | 78.30 | 37.51 | 84.80 | 66.87 |\n"
    "| GPT-5 | 90.80 | 32.75 | 82.30 | 68.62 |\n"
    "| **Conductor w/ all GPT-5** | **93.33** | 33.50 | 82.60 | 69.81 |\n"
    "| **Conductor (full pool)** | **93.30** | **37.86** | **87.50** | **72.89** |\n\n"
    "The all-GPT-5 Conductor already **exceeds GPT-5 alone** (69.81 vs "
    "68.62) -- demonstrating that **subtask design and topology design "
    "alone (no agent diversity) already help**. The full-pool Conductor "
    "adds **+3.08 pp average** on top by also exploiting agent "
    "diversity, with the biggest gain on BCB and GPQA-D where GPT-5 is "
    "weak.",
    title="Table 10: 'Conductor w/ all GPT-5' beats GPT-5 alone (69.81 vs 68.62); full pool adds +3.08 from diversity",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 10",
        "caption": "Table 10: Conductor performance fixing all agents to GPT-5.",
    },
)

claim_subtask_alone_matters = claim(
    "**Subtask design alone matters: 'all GPT-5' Conductor beats GPT-5.** "
    "The all-GPT-5 Conductor variant (Table 10) consistently exceeds the "
    "performance of GPT-5 alone: AIME 93.33 vs 90.80, BCB 33.50 vs "
    "32.75, GPQA-D 82.60 vs 82.30. This demonstrates that **subtask "
    "design and harnessing the Conductor's coordination scheme are "
    "*indispensable* components of the framework -- not merely useful "
    "when paired with agent diversity**.",
    title="Claim: even with no agent diversity, Conductor subtask+topology design beats single-worker baseline",
)

claim_table11_conductor_replacement = claim(
    "**Table 11: Conductor-replacement ablation -- frontier LLMs as the "
    "Conductor.**\n\n"
    "| Model | LCB | AIME | BCB | GPQA-D | Avg. |\n"
    "|---|---|---|---|---|---|\n"
    "| GPT-5 conduct 7 models | 50.86 | 76.67 | 34.50 | 77.78 | 59.95 |\n"
    "| GPT-5 conduct 3 models | 67.43 | 93.30 | 33.10 | 86.36 | 70.05 |\n"
    "| Gemini 2.5 Pro conduct 3 models | 70.29 | 93.30 | 35.13 | 87.62 | 71.59 |\n"
    "| **Conductor (Ours, 7B Qwen2.5)** | **83.93** | **93.30** | **37.86** | **87.50** | **75.65** |\n\n"
    "Even powerful frontier LLMs, when prompted with the identical "
    "Conductor framework to act as coordinators, **fail to match the "
    "trained 7B Conductor** (delta = +4.06 to +15.70 pp avg).",
    title="Table 11: trained 7B Conductor beats GPT-5/Gemini as conductors by +4 to +16 pp",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 11",
        "caption": "Table 11: Replacing trained Conductor with GPT-5 and Gemini 2.5 Pro.",
    },
)

claim_frontier_orchestrator_evidence = claim(
    "**Evidence for the 'LLMs are inherently suitable meta-"
    "orchestrators' hypothesis.** Despite never being trained on these "
    "tasks, **both GPT-5 and Gemini as 3-model Conductors outperform "
    "their constituent agents on numerous tasks** (e.g., Gemini-conduct "
    "GPQA-D 87.62 vs Gemini alone 84.8, GPT-5-conduct GPQA-D 86.36 vs "
    "GPT-5 alone 82.3). This validates the Conductor's underlying "
    "hypothesis -- powerful LLMs are inherently suitable to act as "
    "effective meta-orchestrators -- and suggests larger base models "
    "are a simple direction for scaling the Conductor framework.",
    title="Claim: frontier-LLM-as-Conductor (untrained) already beats individuals -- LLMs are suitable meta-orchestrators",
)

claim_conductor_training_essential = claim(
    "**Conductor RL training is essential beyond LLMs-as-orchestrators.** "
    "While untrained GPT-5/Gemini Conductors beat their constituents, "
    "they nonetheless **fall well short** of the RL-trained 7B "
    "Conductor (e.g., Gemini-conduct-3 71.59 vs Conductor 75.65 avg -- "
    "**-4.06 pp**). GPT-5 and Gemini-as-Conductor exhibit **over-"
    "reliance on prior biases** about which models are best for which "
    "tasks (e.g., they don't realize Claude is weak on LCB or GPT-5 "
    "is weak on BCB), lacking the **empirical feedback mechanism** the "
    "RL training phase provides.",
    title="Claim: RL training corrects untrained LLMs' prior-bias-driven orchestration mistakes (+4 to +16 pp)",
)

# ---------------------------------------------------------------------------
# Appendix B.3 -- Performance diversity case studies
# ---------------------------------------------------------------------------

claim_per_model_specialization = claim(
    "**Per-model specialization observed in evaluation.** Throughout "
    "evaluation, no single worker model reigns supreme on all tasks: "
    "GPT-5 strong in math + competitive coding (AIME, LiveCodeBench), "
    "Gemini in scientific reasoning (GPQA-D), Claude Sonnet 4 dominant "
    "in code generation with diverse function calls (BigCodeBench) but "
    "relatively weak in competitive coding (LiveCodeBench). "
    "Specialization extends to a **subtask level**: the Conductor's "
    "SOTA LiveCodeBench performance leverages Gemini 2.5 Pro and "
    "Claude Sonnet 4 as **high-level planners** and only later employs "
    "GPT-5 to write the final optimized code.",
    title="Claim: per-task per-subtask model specialization documented -- planner vs writer roles for code generation",
)

claim_weak_models_essential_for_subtasks = claim(
    "**Weak open-source models fill essential subtask roles.** Even "
    "'weaker' open-source models (Qwen3-32B, R1-Distill) fill **roles "
    "that their closed-source counterparts fail at**. Concrete example: "
    "for several BigCodeBench questions, using GPT-5 as final validator "
    "fails BCB's strict formatting requirements; switching to "
    "Qwen3-32B or DeepSeek as final validator allows the Conductor to "
    "succeed. This is more prevalent at sub-task level than at the "
    "global task level (most common globally on RLPR and MMLU).",
    title="Claim: weak open models can be essential at specific sub-task levels (e.g., Qwen as final BCB format checker)",
)

# ---------------------------------------------------------------------------
# Appendix B.6 -- OOD zero-shot generalization (Table 8 in main)
# ---------------------------------------------------------------------------

claim_qwen_thinking_vs_direct_bcb = claim(
    "**Unexpected BigCodeBench result: Qwen3-32B (non-thinking) > Qwen3-"
    "32B (thinking).** On BigCodeBench, Qwen3-32B in direct mode (23.0) "
    "**outperforms** Qwen3-32B in thinking mode (20.9). Analysis of "
    "completion transcripts attributes this to **added verbosity in "
    "thinking mode causing formatting failures** on BCB's strict "
    "specifications. This mirrors the GPT-5 finding that **medium** "
    "reasoning effort can outperform **high** reasoning effort on "
    "BigCodeBench.",
    title="Claim: thinking-mode regresses on BCB due to formatting-failure from verbosity (Qwen3-32B and GPT-5)",
)

__all__ = [
    "claim_3b_same_agent_dist",
    "claim_7b_better_prompt_engineering",
    "claim_scale_thesis",
    "claim_workflow_step_distribution",
    "claim_table9_ablations",
    "claim_subtask_ablation",
    "claim_few_shot_ablation",
    "claim_fine_grained_topology_ablation",
    "claim_table10_agent_selection_ablation",
    "claim_subtask_alone_matters",
    "claim_table11_conductor_replacement",
    "claim_frontier_orchestrator_evidence",
    "claim_conductor_training_essential",
    "claim_per_model_specialization",
    "claim_weak_models_essential_for_subtasks",
    "claim_qwen_thinking_vs_direct_bcb",
]
