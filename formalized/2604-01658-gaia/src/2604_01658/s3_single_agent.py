"""Section 3: Single-Agent Experiments — Performance vs. Fixed Evolutionary Baselines"""

from gaia.lang import (
    claim, setting, support, induction,
)

from .motivation import (
    evaluation_budget_setting,
    claim_coral_outperforms_fixed,
    claim_agents_adaptable,
)
from .s2_framework import (
    claim_persistent_memory_design,
    claim_heartbeat_mechanism,
    claim_no_fixed_algorithm,
)

# =============================================================================
# Experimental setup settings
# =============================================================================

benchmark_tasks_setting = setting(
    "The benchmark suite comprises 11 tasks across two categories:\n\n"
    "**Mathematical optimization (6 tasks):** Combinatorial problems with exact scoring\n"
    "- Cap Set: find largest subset of {0,1,2}^n with no 3-term arithmetic progression\n"
    "- Costas Array: construct permutation matrices with distinct difference vectors\n"
    "- Admissible Set: number theory optimization problem\n"
    "- Boolformer: Boolean formula synthesis\n"
    "- Weave: combinatorial graph weaving problem\n"
    "- Lyapunov: design Lyapunov functions for stability\n\n"
    "**Systems optimization (5 tasks):** Engineering optimization with simulation-based scoring\n"
    "- Two scheduling problems (Transaction Scheduling, Task Assignment)\n"
    "- Two network routing problems\n"
    "- One memory allocation problem\n\n"
    "Stress-test tasks (not in the main 11): Kernel Engineering and Polyominoes packing "
    "(harder, longer-horizon problems used for multi-agent evaluation).",
    title="Benchmark task suite",
)

baselines_setting = setting(
    "Baseline methods evaluated against CORAL (single-agent):\n\n"
    "| Baseline | Type | Description |\n"
    "|----------|------|-------------|\n"
    "| FunSearch | Fixed evolutionary | LLM mutation in island-based evolution |\n"
    "| EvoPrompting | Fixed evolutionary | Prompt-based evolutionary code search |\n"
    "| OpenEvolve | Fixed evolutionary | Open-source AlphaEvolve implementation |\n"
    "| ShinkaEvolve | Fixed evolutionary | Evolutionary optimization with LLMs |\n"
    "| EvoX | Fixed evolutionary | General evolutionary computation framework |\n\n"
    "All baselines use the same LLM (Claude Opus 4.6) and the same evaluation budget "
    "(3-hour wall-clock or 100 iterations). Results averaged over 4 independent trials.",
    title="Baseline methods for single-agent comparison",
)

# =============================================================================
# Individual task performance claims (from Table 1)
# =============================================================================

claim_sota_8_tasks = claim(
    "CORAL (single-agent) establishes new state-of-the-art results on 8 of 11 benchmark "
    "tasks, achieving the best final score across all 11 tasks compared to fixed "
    "evolutionary baselines (FunSearch, EvoPrompting, OpenEvolve, ShinkaEvolve, EvoX). "
    "The 8 new state-of-the-art results span both mathematical (5/6) and systems "
    "optimization (3/5) categories.",
    title="CORAL achieves new SOTA on 8/11 tasks",
    metadata={"source": "artifacts/2604-01658.pdf, Table 1, Section 3"},
)

claim_improvement_rate = claim(
    "CORAL's improvement rate (fraction of evaluations that produce a new best score) "
    "is 3–10× higher than all fixed evolutionary baselines across the 11-task benchmark. "
    "CORAL typically achieves convergence within 5–20 evaluations, whereas baselines "
    "require 60–100 evaluations to reach comparable performance levels.",
    title="CORAL improvement rate 3-10x higher",
    metadata={"source": "artifacts/2604-01658.pdf, Section 3.1"},
)

claim_math_tasks_strong = claim(
    "On mathematical optimization tasks, CORAL single-agent achieves the highest scores "
    "on 5 of 6 tasks compared to all fixed evolutionary baselines. The Cap Set task "
    "shows the largest gap, with CORAL achieving scores that baselines fail to reach "
    "within the evaluation budget.",
    title="CORAL strong on mathematical optimization",
    metadata={"source": "artifacts/2604-01658.pdf, Table 1, Section 3"},
)

claim_systems_tasks_strong = claim(
    "On systems optimization tasks (scheduling, routing, memory allocation), CORAL "
    "single-agent achieves the highest scores on 4 of 5 tasks. Transaction Scheduling "
    "shows CORAL achieving 4,566 cycles in single-agent mode (improved to 4,694 with "
    "4 agents), outperforming all fixed baselines.",
    title="CORAL strong on systems optimization",
    metadata={"source": "artifacts/2604-01658.pdf, Table 1, Section 3"},
)

claim_single_agent_convergence = claim(
    "CORAL single-agent convergence profiles show a distinctly non-monotone improvement "
    "pattern: rapid gains in the first 5–10 evaluations, followed by plateau periods "
    "punctuated by sharp jumps when the agent discovers a new approach. This pattern "
    "contrasts with baseline methods that show more gradual, monotone improvement curves.",
    title="CORAL shows punctuated convergence pattern",
    metadata={"source": "artifacts/2604-01658.pdf, Section 3.2, Figure 2"},
)

# =============================================================================
# Open-source model validation
# =============================================================================

claim_open_source_validates = claim(
    "CORAL's performance advantage generalizes beyond Claude Opus 4.6: experiments with "
    "open-source models (MiniMax-M2.5 and OpenCode) on a subset of benchmark tasks "
    "show that CORAL outperforms fixed evolutionary baselines using open-source LLMs, "
    "confirming the framework's generality beyond a single proprietary model.",
    title="CORAL advantages generalize to open-source models",
    metadata={"source": "artifacts/2604-01658.pdf, Appendix"},
)

# =============================================================================
# Strategies
# =============================================================================

strat_framework_drives_sota = support(
    [claim_no_fixed_algorithm, claim_persistent_memory_design, claim_heartbeat_mechanism],
    claim_sota_8_tasks,
    reason=(
        "The absence of a fixed algorithm (@claim_no_fixed_algorithm) allows agents to "
        "adapt their search strategy to each task's structure. The shared persistent memory "
        "(@claim_persistent_memory_design) enables agents to build on previous discoveries "
        "rather than re-exploring visited regions. Heartbeat interventions "
        "(@claim_heartbeat_mechanism) prevent premature convergence by triggering strategic "
        "pivots when agents stagnate. Together these mechanisms produce the SOTA results "
        "on 8/11 tasks (@claim_sota_8_tasks)."
    ),
    prior=0.82,
)

strat_sota_implies_rate = support(
    [claim_sota_8_tasks],
    claim_improvement_rate,
    reason=(
        "Achieving best final scores on 8/11 tasks (@claim_sota_8_tasks) within the same "
        "evaluation budget as baselines that score lower implies a higher per-evaluation "
        "improvement rate. The 3–10× improvement rate figure is a direct consequence of "
        "reaching higher scores with fewer evaluations: convergence within 5–20 evaluations "
        "versus 60–100 for baselines under the same 3-hour budget."
    ),
    prior=0.88,
)

# Induction: two independent task categories both show CORAL superiority
# Generative direction: law (CORAL outperforms fixed) predicts specific task outcomes
s_math_ind = support(
    [claim_coral_outperforms_fixed],
    claim_math_tasks_strong,
    reason=(
        "The general law that CORAL outperforms fixed evolutionary search "
        "(@claim_coral_outperforms_fixed) predicts that on mathematical optimization tasks, "
        "CORAL should achieve higher scores than baselines. The autonomous strategy adaptation "
        "and shared memory design that drives the law should manifest in math tasks, where "
        "agents discover task-specific combinatorial insights and build on prior solutions."
    ),
    prior=0.82,
)

s_systems_ind = support(
    [claim_coral_outperforms_fixed],
    claim_systems_tasks_strong,
    reason=(
        "The general law that CORAL outperforms fixed evolutionary search "
        "(@claim_coral_outperforms_fixed) predicts that on systems optimization tasks, "
        "CORAL should achieve higher scores than baselines. CORAL's autonomous adaptation "
        "should allow agents to discover task-specific techniques (e.g., local testing on "
        "compiled-code tasks) that fixed algorithms cannot encode."
    ),
    prior=0.80,
)

ind_both_categories = induction(
    s_math_ind, s_systems_ind,
    law=claim_coral_outperforms_fixed,
    reason=(
        "Mathematical optimization and systems optimization tasks are structurally independent "
        "benchmark categories—different problem types, different solution representations, "
        "different evaluation functions. CORAL achieving better scores on both categories "
        "independently provides inductive confirmation of the general law that CORAL outperforms "
        "fixed evolutionary search (@claim_coral_outperforms_fixed)."
    ),
)

strat_open_source_generalization = support(
    [claim_improvement_rate],
    claim_open_source_validates,
    reason=(
        "If the improvement rate advantage (@claim_improvement_rate) derives from framework "
        "design (memory, heartbeats, autonomous strategy) rather than from the specific "
        "capabilities of Claude Opus 4.6, then the advantage should generalize to other "
        "capable LLMs. The open-source validation result confirms this framework-level "
        "generality: MiniMax-M2.5 and OpenCode also outperform fixed baselines under "
        "CORAL's framework."
    ),
    prior=0.75,
)

strat_punctuated_from_heartbeat = support(
    [claim_heartbeat_mechanism, claim_agents_adaptable],
    claim_single_agent_convergence,
    reason=(
        "The punctuated convergence pattern (@claim_single_agent_convergence) — rapid gains "
        "followed by plateaus punctuated by jumps — is mechanistically explained by "
        "heartbeat-triggered strategic pivots (@claim_heartbeat_mechanism): after 5 "
        "non-improving evaluations, the stagnation redirect prompt causes the agent to "
        "fundamentally change strategy, producing sharp jumps. The agent's capacity to "
        "discover new approaches (@claim_agents_adaptable) determines the magnitude of "
        "each jump."
    ),
    prior=0.78,
)
