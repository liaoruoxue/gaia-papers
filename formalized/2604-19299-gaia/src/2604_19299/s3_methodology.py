"""Section 3: Methodology and Experimental Design"""

from gaia.lang import claim, setting, support, deduction
from .motivation import (
    slm_definition, react_framework, financial_privacy_constraints,
    research_gap,
)

# ── Experimental setup settings ───────────────────────────────────────────────

experimental_scope = setting(
    "The study evaluates 27 open-source language models with fewer than 10B parameters "
    "across three paradigms (Base SLM, Single-Agent System, Multi-Agent System) on 20 "
    "publicly available financial datasets covering 8 task categories. All experiments "
    "are run on NVIDIA H100 80GB GPU, CUDA 12.1, using vLLM for high-throughput "
    "memory-efficient inference. Inference temperature is fixed at 0 (top_p=0.9) to "
    "maximize reproducibility. Agent interaction turns are capped at 5.",
    title="Experimental scope and hardware environment",
)

model_families = setting(
    "The 27 evaluated models span 7 families:\n\n"
    "| Family | Versions | Parameter Range |\n"
    "|--------|----------|-----------------|\n"
    "| Qwen | 2.5-0.5B, 2.5-1.5B, 2.5-3B, 2.5-7B, 3-8B | 0.5B–8B |\n"
    "| Llama | 3.2-1B, 3.2-3B, 2-7B, 3.1-8B, 3-8B | 1B–8B |\n"
    "| Gemma | 3-270M, 3-1B, 2-2B, 3-4B, 2-9B | 0.27B–9B |\n"
    "| Phi | 3.5-mini, 4-mini, 3-small | 3.8B–7B |\n"
    "| DeepSeek-R1 | Distill-Qwen-1.5B/7B, Distill-Llama-8B | 1.5B–8B |\n"
    "| Mistral | 7B-v0.3, Ministral-8B | 7B–8B |\n"
    "| SOLAR | 10.7B-v1.0 | 10.7B |",
    title="Evaluated model families and versions (Table 1)",
    metadata={"source_table": "artifacts/2604.19299.pdf, Table 1"},
)

task_scope = setting(
    "Experiments span 20 publicly available financial datasets across 8 task categories: "
    "sentiment analysis, text classification, named entity recognition (NER), question "
    "answering, stock movement prediction, credit scoring, summarization, and bankruptcy "
    "prediction. 50 instances are sampled per dataset to ensure balanced comparison "
    "[@Xie2023; @Xie2024].",
    title="Task and dataset scope",
)

# ── Architecture design claims ────────────────────────────────────────────────

base_slm_design = claim(
    "The Base SLM paradigm represents direct model deployment without any architectural "
    "changes: the model receives task input and generates output directly, without tool "
    "access or multi-agent coordination. It serves as the reference baseline for "
    "performance, stability, and resource usage.",
    title="Base SLM paradigm design",
)

sas_design = claim(
    "The Single-Agent System (SAS) follows a ReAct think–act–observe cycle. After "
    "receiving a task, the agent decides whether to invoke external tools (calculator, "
    "Wikipedia search, web search) or answer directly. If tools are used, the agent "
    "processes returned results and may repeat the cycle until a final answer is produced. "
    "The SAS simulates a general-purpose financial analyst with unified tool access.",
    title="Single-Agent System (SAS) design",
    background=[react_framework],
)

mas_design = claim(
    "The Multi-Agent System (MAS) consists of one supervisor agent and three specialist "
    "agents: FinancialKnowledgeAgent (tools: calculator, wiki search), "
    "FinancialNLPAgent (tool: web search), and FinancialQuantAgent (tool: calculator "
    "only). The supervisor routes tasks to the appropriate specialist but does not invoke "
    "tools itself. All agents follow the ReAct pattern. This design introduces role "
    "specialization and inter-agent coordination overhead.",
    title="Multi-Agent System (MAS) design",
    background=[react_framework],
)

prompt_design = claim(
    "Agent prompts enforce three principles to ensure stable deployment: (1) strict "
    "structural control via XML-style tags (<think>, <action>, <observation>, "
    "<final_answer>) to prevent format drift; (2) explicit tool governance with hard "
    "JSON formatting rules to prevent hallucinated tool calls; (3) task-grounded "
    "reasoning requiring the model to identify the required answer format before "
    "reasoning. SAS and MAS use identical tool definitions and structural constraints, "
    "differing only in reasoning decomposition (monolithic vs. delegated).",
    title="Agent prompt design principles",
)

# ── Metric definitions ────────────────────────────────────────────────────────

metric_completion_rate = setting(
    "Completion Rate is defined as the proportion of samples for which the system "
    "returns a valid response without runtime errors, timeouts, or malformed outputs:\n\n"
    "$$\\text{Completion Rate} = \\frac{\\text{# of successful responses}}{\\text{# of total samples}}$$\n\n"
    "A higher value indicates better deployment robustness.",
    title="Metric: Completion Rate (robustness)",
)

metric_nrq = setting(
    "Normalized Response Quality (NRQ) aggregates response quality across heterogeneous "
    "tasks and evaluation metrics. For each dataset, the relative quality gain of "
    "architecture $a$ vs. the Base SLM is:\n\n"
    "$$g_{a,d} = \\frac{s_{a,d} - s_{\\text{Base},d}}{|s_{\\text{Base},d}| + \\epsilon}$$ "
    "(higher-is-better metrics), or the negated version for lower-is-better metrics. "
    "Task-level scores are averaged across datasets, then architecture-level NRQ "
    "averages equally across all 8 tasks. By construction, Base SLM has NRQ = 0.",
    title="Metric: Normalized Response Quality (NRQ)",
)

metric_composite_z = setting(
    "The Composite Effectiveness Z-score ($Z_c$) standardizes raw metric values "
    "across datasets for the same model:\n\n"
    "$$Z_c = \\frac{1}{N} \\sum_{i=1}^{N} \\frac{X_i - \\mu_i}{\\sigma_i}$$\n\n"
    "where $\\mu_i$ and $\\sigma_i$ are the mean and standard deviation across "
    "all configurations for dataset $i$. A higher $Z_c$ indicates better overall "
    "effectiveness relative to other model-architecture combinations.",
    title="Metric: Composite Effectiveness Z-score",
)

metric_leading_advantage = setting(
    "The Leading Advantage $\\alpha$ quantifies the decisiveness of performance "
    "differences between the best and second-best architectures:\n\n"
    "$$\\alpha = \\frac{s_{\\text{best}} - s_{\\text{second}}}{|s_{\\text{second}}| + \\epsilon} "
    "\\times 100\\%,\\quad \\epsilon = 10^{-8}$$\n\n"
    "A larger $\\alpha$ indicates a more decisive advantage.",
    title="Metric: Leading Advantage",
)

# ── Methodology justification ─────────────────────────────────────────────────

strat_methodology_design = support(
    [research_gap, base_slm_design, sas_design, mas_design],
    claim(
        "The three-paradigm experimental design (Base SLM, SAS, MAS) with deployment-"
        "oriented metrics (completion rate, NRQ, energy per token, latency) provides a "
        "valid framework for systematically answering the research question about "
        "optimal SLM deployment paradigms in resource-constrained financial settings.",
        title="Validity of the three-paradigm experimental framework",
    ),
    reason=(
        "The @research_gap requires empirical comparison across paradigms. "
        "@base_slm_design establishes the capability baseline. @sas_design introduces "
        "tool augmentation as a middle ground. @mas_design adds role-specialized "
        "coordination. Together they form a progression from simplest to most complex, "
        "enabling isolation of the contribution of each architectural addition. "
        "Deployment metrics (energy, latency, completion rate) fill the gap left by "
        "accuracy-only benchmarks."
    ),
    prior=0.88,
    background=[experimental_scope, model_families, task_scope],
)
