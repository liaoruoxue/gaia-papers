"""Section 5: Discussion and Practical Implications"""

from gaia.lang import claim, setting, support, deduction, contradiction
from .motivation import (
    slm_inherent_limits, agent_potential, research_gap, fine_tuning_impractical,
)
from .s3_methodology import (
    experimental_scope,
)
from .s4_results import (
    sas_best_overall_tradeoff, mas_limited_gains, no_universal_winner,
    obs_sas_nrq, obs_completion_rates, obs_latency_tokens,
    obs_agent_more_failures, obs_sas_failure_modes, obs_mas_failure_modes,
    obs_base_uturn, scaling_law_predicts_monotone,
    obs_mas_bankruptcy, obs_sas_reasoning_tasks, obs_base_classification,
    obs_mas_variance,
)
from .s3_methodology import (
    base_slm_design, sas_design, mas_design,
    experimental_scope, prompt_design,
)

# ── Coordination tax concept ──────────────────────────────────────────────────

coordination_tax = claim(
    "Transitioning from Base SLMs to agentic architectures introduces a fundamental "
    "coordination tax: the overhead of managing agent states, inter-agent communication, "
    "and ReAct prompting cycles frequently fails to translate into proportional gains "
    "in task correctness. This is evidenced by MAS's minimal NRQ gain (0.36) relative "
    "to SAS (4.85) despite nearly doubling token consumption [@Zhang2024; @RizviMartel2025].",
    title="Coordination tax in multi-agent systems",
)

context_management_bottleneck = claim(
    "The dominant failure modes in agent systems (Context Length Exceeded in SAS, "
    "Delegation Failure and No Delegation in MAS) indicate that the primary bottleneck "
    "for modern small-model AI deployment is no longer raw generative capability but "
    "rather context management and instruction adherence. Increasing agent count "
    "introduces new vectors for systemic failure (e.g., infinite delegation loops) "
    "rather than enhancing collective intelligence.",
    title="Context management as primary SLM agent bottleneck",
)

architectural_fragility = claim(
    "Wrapping SLMs in complex agent paradigms trades the unpredictability of raw model "
    "outputs for the complexity of managing agent states. This represents a form of "
    "architectural fragility: the system may appear more capable in isolation but "
    "fails more often in practice due to coordination complexity.",
    title="Architectural fragility of complex agent paradigms for SLMs",
)

# ── Practical deployment implications ─────────────────────────────────────────

guideline_sas_for_complex = claim(
    "For complex reasoning and generation tasks (question answering, summarization, "
    "credit risk prediction), SAS is the recommended deployment paradigm for SLMs: "
    "it provides strong effectiveness gains (NRQ = 4.85) with moderate overhead and "
    "is Pareto-optimal in the efficiency–effectiveness trade-off.",
    title="Deployment guideline: use SAS for complex reasoning tasks",
)

guideline_mas_for_high_entropy = claim(
    "MAS should be restricted to high-entropy domains such as financial forecasting "
    "and bankruptcy prediction, where statistical redundancy across multiple specialized "
    "agent perspectives outweighs coordination costs. MAS provides its clearest "
    "advantage on bankruptcy prediction tasks.",
    title="Deployment guideline: restrict MAS to high-entropy domains",
)

guideline_base_for_extraction = claim(
    "For simpler extraction tasks such as named entity recognition and sentiment "
    "analysis, the Base SLM remains superior. Agentic overhead tends to dilute "
    "precise token-level mappings in these tasks, and the completion rate of 99.67% "
    "for Base SLM is much higher than agent alternatives.",
    title="Deployment guideline: use Base SLM for extraction tasks",
)

guideline_fallback = claim(
    "Production agent deployments for SLMs require robust fallback mechanisms: when "
    "an agent system encounters a stuck state or context exhaustion, the system should "
    "automatically revert to the Base SLM to ensure a response is always returned. "
    "This maintains the reliability floor of the Base SLM (99.67% completion rate) "
    "as a safety net.",
    title="Deployment guideline: implement Base SLM fallback for agent systems",
)

study_limitations = claim(
    "This study has several limitations: (1) evaluation is restricted to a fixed set "
    "of 27 SLMs, 20 datasets, and three agent designs — results may differ under other "
    "configurations; (2) agent coordination strategies are simple (ReAct-based) — "
    "stronger control mechanisms may improve MAS stability; (3) adaptive agents that "
    "change behavior dynamically are not evaluated; (4) real user traffic patterns "
    "are not modeled.",
    title="Study limitations and scope",
)

# ── Reasoning strategies ──────────────────────────────────────────────────────

strat_coordination_tax = support(
    [obs_mas_failure_modes, obs_latency_tokens, obs_sas_nrq],
    coordination_tax,
    reason=(
        "MAS NRQ of 0.36 vs. SAS NRQ of 4.85 (@obs_sas_nrq) shows marginal gains. "
        "@obs_latency_tokens shows MAS consumes 14,618 tokens vs. SAS's 8,040, "
        "an 82% overhead increase for this marginal gain. @obs_mas_failure_modes "
        "shows new failure types (delegation failure, infinite loops) introduced by "
        "inter-agent coordination. Together these establish the coordination tax "
        "[@Zhang2024; @RizviMartel2025]."
    ),
    prior=0.88,
)

strat_context_bottleneck = support(
    [obs_sas_failure_modes, obs_mas_failure_modes, obs_agent_more_failures],
    context_management_bottleneck,
    reason=(
        "The most common SAS failures are Context Length Exceeded and No Delegation "
        "(@obs_sas_failure_modes) — both context management failures. MAS adds "
        "Delegation Failure (@obs_mas_failure_modes). @obs_agent_more_failures "
        "confirms agent systems fail substantially more often than the Base SLM. "
        "The pattern of failures points to context management and instruction adherence "
        "as the binding constraint, not raw generation capability."
    ),
    prior=0.85,
)

strat_guidelines = support(
    [no_universal_winner, sas_best_overall_tradeoff, mas_limited_gains,
     obs_base_classification],
    claim(
        "A task-adaptive deployment strategy—using SAS for complex reasoning, MAS only "
        "for high-entropy domains, and Base SLM for simple extraction—is justified by "
        "the empirical evidence and is the recommended practical approach for "
        "resource-constrained financial SLM deployment.",
        title="Task-adaptive deployment strategy recommendation",
    ),
    reason=(
        "@no_universal_winner establishes that one paradigm cannot serve all tasks. "
        "@sas_best_overall_tradeoff justifies SAS as the general default. "
        "@mas_limited_gains justifies restricting MAS to specific high-value cases. "
        "@obs_base_classification justifies keeping Base for simple extraction tasks. "
        "Together these provide a task-specific deployment decision framework."
    ),
    prior=0.88,
)

agent_design_over_scaling = claim(
    "Agent-centric system design (choosing the right paradigm for the task) is "
    "more effective for improving SLM financial task performance than raw parameter "
    "scaling within the sub-10B range. Architectural choices dominate over model "
    "size as the key performance lever in resource-constrained settings.",
    title="Agent design dominates scaling within SLM range",
)

strat_agent_design_over_scaling = support(
    [obs_base_uturn, sas_best_overall_tradeoff],
    agent_design_over_scaling,
    reason=(
        "@obs_base_uturn shows that scaling Base SLMs to 8B–10B parameters yields "
        "diminishing and negative returns in effectiveness. @sas_best_overall_tradeoff "
        "shows that wrapping even smaller models in a SAS paradigm achieves NRQ = 4.85, "
        "far exceeding larger Base SLMs. Therefore architectural design choice is the "
        "dominant lever."
    ),
    prior=0.85,
    background=[scaling_law_predicts_monotone],
)

strat_architectural_fragility = support(
    [coordination_tax, context_management_bottleneck],
    architectural_fragility,
    reason=(
        "@coordination_tax shows that MAS overhead grows faster than benefits. "
        "@context_management_bottleneck shows that failures stem from agent state "
        "management, not raw capability. Together these establish that complex agent "
        "wrappers trade one form of unpredictability for another: raw output variance "
        "becomes agent state management complexity."
    ),
    prior=0.82,
)

strat_guidelines_deployment = support(
    [sas_best_overall_tradeoff, obs_mas_bankruptcy, obs_base_classification,
     obs_completion_rates],
    guideline_fallback,
    reason=(
        "Since @sas_best_overall_tradeoff and @obs_mas_bankruptcy and "
        "@obs_base_classification all indicate task-specific optima, and since "
        "@obs_completion_rates shows agent paradigms can fail on 20-28% of samples, "
        "a fallback to Base SLM is required for production reliability."
    ),
    prior=0.87,
)

strat_guideline_sas = support(
    [sas_best_overall_tradeoff, obs_sas_reasoning_tasks],
    guideline_sas_for_complex,
    reason=(
        "@sas_best_overall_tradeoff provides the overall justification. "
        "@obs_sas_reasoning_tasks shows >150% improvement on QA and summarization "
        "tasks specifically, directly supporting the recommendation of SAS for "
        "complex reasoning tasks."
    ),
    prior=0.88,
)

strat_guideline_mas = support(
    [mas_limited_gains, obs_mas_bankruptcy],
    guideline_mas_for_high_entropy,
    reason=(
        "@mas_limited_gains shows MAS is not generally beneficial. "
        "@obs_mas_bankruptcy shows MAS's one consistent advantage is bankruptcy "
        "prediction, a high-entropy domain. This exception justifies restricting "
        "MAS to such domains."
    ),
    prior=0.82,
)

strat_guideline_base = support(
    [obs_base_classification, obs_agent_more_failures],
    guideline_base_for_extraction,
    reason=(
        "@obs_base_classification shows Base SLM is competitive or superior on "
        "NER, sentiment, and stock prediction. @obs_agent_more_failures confirms "
        "that agent overhead adds failures for no benefit on simple extraction tasks."
    ),
    prior=0.85,
)

strat_mas_variance_contributes = support(
    [obs_mas_variance, obs_mas_failure_modes],
    coordination_tax,
    reason=(
        "@obs_mas_variance shows MAS has inconsistent performance across model scales — "
        "sometimes underperforming SAS despite more coordination. @obs_mas_failure_modes "
        "shows the sources of this variance (delegation failures, stuck handoffs). "
        "High variance is a signature of coordination overhead: the system is sensitive "
        "to agent interaction dynamics rather than task inputs."
    ),
    prior=0.78,
)

strat_prompt_design_rationale = support(
    [prompt_design],
    architectural_fragility,
    reason=(
        "@prompt_design shows that extensive prompt engineering (XML tags, strict JSON, "
        "explicit reasoning control) is required just to make agent paradigms function. "
        "This engineering burden reflects the underlying architectural fragility: the "
        "system requires rigid scaffolding to avoid format drift, tool hallucination, "
        "and infinite loops — fragility not present in the Base SLM."
    ),
    prior=0.75,
)

strat_limitations_scope = support(
    [study_limitations],
    claim(
        "The findings of this study should be interpreted with caution: they apply "
        "specifically to the 27 evaluated SLMs, 20 financial datasets, and three "
        "agent designs studied. Generalization to other model families, task domains, "
        "or stronger coordination mechanisms requires additional empirical validation.",
        title="Scope caveat for study findings",
    ),
    reason=(
        "@study_limitations identifies four specific scope restrictions: fixed model "
        "set, fixed task set, simple coordination strategies, and no adaptive agents. "
        "Each constitutes a potential boundary condition for the findings."
    ),
    prior=0.95,
    background=[experimental_scope],
)
