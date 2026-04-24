"""Introduction and Motivation: LLM Long-Horizon Execution Challenge"""

from gaia.lang import claim, setting, question, support, deduction

# --- Background Settings ---

setting_llm_error_rate = setting(
    "Large language models (LLMs) have a persistent per-step error rate. "
    "A system with a 1% per-step error rate is expected to fail after only 100 steps "
    "of a million-step task: the probability that all s steps are correct is (1-p)^s, "
    "which decays exponentially to zero as s grows.",
    title="LLM persistent error rate and exponential decay",
)

setting_hanoi_benchmark = setting(
    "The Towers of Hanoi problem is used as a benchmark for LLM long-horizon execution. "
    "The puzzle requires moving D disks from one peg to another obeying the rule that "
    "a larger disk never sits atop a smaller one. The optimal number of steps to complete "
    "the task with D disks is 2^D - 1. With 10 disks this is 1,023 steps; with 20 disks "
    "it is 1,048,575 steps (just over one million).",
    title="Towers of Hanoi benchmark definition",
)

setting_mdap_framework = setting(
    "Massively Decomposed Agentic Processes (MDAPs) is a framework category for LLM-based "
    "systems that decompose tasks into minimal subtasks, apply error correction at the "
    "subtask level through voting, and use red-flagging to reduce correlated errors. "
    "MAKER (Maximal Agentic decomposition with Error-correction and Red-flagging) is the "
    "first implementation of this framework.",
    title="MDAP framework and MAKER definition",
)

# --- Core Problem Claims ---

llm_degrade_hanoi = claim(
    "State-of-the-art LLMs degrade catastrophically on the Towers of Hanoi benchmark: "
    "they can complete the task with a high success rate up to five or six disks, "
    "after which the success rate plummets to zero. This means LLMs inevitably fail "
    "on any task requiring correct execution of more than a few hundred dependent steps. [@Shojaee2025]",
    title="LLM catastrophic degradation on long-horizon Towers of Hanoi",
)

llm_context_burden = claim(
    "Because LLMs are auto-regressive, when generating the i-th action in a long task, "
    "a single agent is increasingly burdened by the growing context produced in generating "
    "all prior actions. As context increases, LLM outputs become increasingly unreliable, "
    "leading to eventual failure on tasks requiring thousands of sequential correct decisions.",
    title="Growing context burden degrades LLM reliability",
)

single_agent_infeasible = claim(
    "A single LLM agent assigned to an s-step task faces an exponentially decaying "
    "probability of producing a fully correct action sequence. The probability that all s "
    "actions are correct is (1-e)^s where e is the per-step error rate, making "
    "million-step task completion essentially impossible without error correction.",
    title="Single-agent approach is infeasible for million-step tasks",
)

strat_single_agent_infeasible = support(
    [llm_degrade_hanoi, llm_context_burden],
    single_agent_infeasible,
    reason=(
        "@llm_degrade_hanoi shows that empirically LLMs fail at long-horizon tasks, "
        "and @llm_context_burden explains the mechanism: growing context degrades "
        "reliability. Together these establish that the single-agent paradigm cannot "
        "scale to million-step tasks without a fundamentally different approach."
    ),
    prior=0.95,
)

# --- Research Question ---

rq_million_steps = question(
    "Can an LLM-based agentic system be designed to reliably solve tasks requiring "
    "over one million sequential steps with zero errors, and what framework enables this?"
)

# --- Orthogonal Scaling Claim ---

mdap_orthogonal_direction = claim(
    "MDAPs (Massively Decomposed Agentic Processes) represent an orthogonal direction "
    "to AI scaling compared to the predominant approach of building larger and more "
    "intelligent base LLMs. Rather than increasing the intelligence (cost per token) of "
    "the underlying model, MDAPs achieve reliability through extreme decomposition and "
    "error correction, enabling tasks beyond the reach of even the most expensive models.",
    title="MDAPs as orthogonal AI scaling direction",
)
