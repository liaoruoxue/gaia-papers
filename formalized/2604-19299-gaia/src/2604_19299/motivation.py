"""Introduction and Motivation: Deployment Trade-offs of SLMs under Agent Paradigms"""

from gaia.lang import claim, setting, question, support, contradiction

# ── Settings (background facts) ──────────────────────────────────────────────

financial_privacy_constraints = setting(
    "Financial services operate under strict privacy regulations, including the "
    "EU General Data Protection Regulation (GDPR) and the Payment Card Industry "
    "Data Security Standard (PCI DSS), which restrict the use of third-party cloud "
    "APIs for processing sensitive customer data [@EuropeanParliament2025].",
    title="Financial privacy regulatory constraints",
)

slm_definition = setting(
    "Small Language Models (SLMs) are defined in this study as open-source language "
    "models with fewer than 10 billion (10B) parameters.",
    title="SLM definition (< 10B parameters)",
)

react_framework = setting(
    "The Reasoning and Acting (ReAct) framework is an agent paradigm that interleaves "
    "chain-of-thought reasoning with external tool invocations in a think–act–observe "
    "cycle [@Yao2022]. All agent systems in this study are implemented using ReAct.",
    title="ReAct framework definition",
)

# ── Problem claims ────────────────────────────────────────────────────────────

llm_deployment_cost = claim(
    "Large language models (LLMs) with many billions of parameters impose substantial "
    "computational costs, high inference latency, and significant privacy risks, which "
    "collectively hinder their widespread deployment in resource-constrained real-world "
    "applications such as regional banks, boutique funds, and individual investor "
    "platforms [@Wang2025].",
    title="LLM deployment barriers in finance",
)

slm_inherent_limits = claim(
    "Small language models (SLMs, fewer than 10B parameters), while computationally "
    "efficient and locally deployable, inherently struggle with multi-step numerical "
    "reasoning, domain-specific financial knowledge, and maintaining factual accuracy "
    "in financial tasks [@Haque2025].",
    title="SLM inherent capability limitations",
)

fine_tuning_impractical = claim(
    "Traditional SLM improvement strategies—including large-scale domain-specific "
    "pre-training and task-specific fine-tuning—remain prohibitively costly and "
    "impractical for resource-constrained organizations such as regional banks and "
    "boutique funds [@Haque2025].",
    title="Fine-tuning impractical for resource-constrained deployment",
)

existing_benchmarks_gap = claim(
    "Existing LLM evaluation benchmarks (e.g., Open LLM Leaderboard, HELM) primarily "
    "measure task accuracy while overlooking deployment-critical factors such as runtime "
    "stability, energy consumption, and latency under resource-constrained settings. "
    "This renders them insufficient for guiding practical deployment decisions.",
    title="Existing benchmarks neglect deployment factors",
)

agent_potential = claim(
    "Agent-based paradigms—including tool use (e.g., calculator, web search, wiki "
    "search) and multi-agent collaboration—offer a promising alternative path to "
    "compensating for SLM capability limitations without requiring costly retraining "
    "[@Shen2024].",
    title="Agent paradigms as compensation mechanism for SLMs",
)

research_gap = claim(
    "It remains empirically unclear whether agent paradigms (single-agent with tools, "
    "multi-agent collaboration) effectively and efficiently enhance SLMs under strict "
    "hardware and privacy constraints in financial settings, and which paradigm offers "
    "the best deployment trade-off.",
    title="Research gap: agent paradigms for constrained SLM deployment",
)

# ── Core research question ────────────────────────────────────────────────────

rq_deployment_tradeoff = question(
    "Which of the three paradigms—base SLM, single-agent system (SAS), or multi-agent "
    "system (MAS)—achieves the best balance among task effectiveness, computational "
    "efficiency, and deployment robustness for small language models (< 10B parameters) "
    "in financial applications under resource and privacy constraints?",
    title="Core research question: optimal paradigm for constrained SLM deployment",
)

# ── Motivating strategy ───────────────────────────────────────────────────────

strat_motivation = support(
    [llm_deployment_cost, slm_inherent_limits, fine_tuning_impractical, existing_benchmarks_gap],
    research_gap,
    reason=(
        "LLMs are too costly and privacy-risky for local financial deployment "
        "(@llm_deployment_cost). SLMs are deployable but capability-limited "
        "(@slm_inherent_limits). Traditional improvement routes (fine-tuning) are "
        "impractical (@fine_tuning_impractical). Existing benchmarks do not address "
        "deployment realities (@existing_benchmarks_gap). Together these create an "
        "unaddressed gap: we do not know whether agent paradigms can fill the capability "
        "gap for SLMs under real operational constraints."
    ),
    prior=0.95,
    background=[financial_privacy_constraints, slm_definition],
)

strat_agent_as_solution = support(
    [agent_potential, research_gap],
    claim(
        "Systematically studying SLMs under base, single-agent, and multi-agent "
        "paradigms across diverse financial tasks and deployment metrics is necessary "
        "to determine whether agent design can substitute for model scale.",
        title="Necessity of systematic paradigm comparison for SLMs",
    ),
    reason=(
        "Agent paradigms present a theoretically sound mechanism to augment SLMs "
        "(@agent_potential), but the @research_gap indicates this has not been "
        "empirically verified at scale for financial SLM deployment. A systematic "
        "large-scale study is therefore required."
    ),
    prior=0.9,
    background=[slm_definition, react_framework],
)
