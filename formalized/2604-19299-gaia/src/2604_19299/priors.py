"""
Priors for 2604-19299-gaia: SLM Deployment Trade-offs under Agent Paradigms.

PRIORS maps Knowledge objects to (prior_value, justification) tuples.
Only independent (leaf) claims should be assigned priors here.
"""

from .motivation import (
    llm_deployment_cost,
    slm_inherent_limits,
    fine_tuning_impractical,
    existing_benchmarks_gap,
    agent_potential,
)
from .s3_methodology import (
    base_slm_design,
    sas_design,
    mas_design,
    prompt_design,
)
from .s4_results import (
    obs_completion_rates,
    obs_latency_tokens,
    obs_energy_per_token,
    obs_sas_pareto,
    obs_base_uturn,
    obs_base_classification,
    obs_mas_bankruptcy,
    obs_mas_variance,
    obs_sas_reasoning_tasks,
    obs_sas_failure_modes,
    obs_mas_failure_modes,
    pred_sas_effective,
    alt_sas_ineffective,
    scaling_law_predicts_monotone,
)
from .s5_discussion import study_limitations

PRIORS: dict = {
    # ── Empirical observations (directly measured from experiment) ─────────────
    obs_completion_rates: (
        0.93,
        "Completion rates directly measured from controlled experiment across 27 models "
        "x 3 paradigms x 20 datasets. 50 samples/dataset, stable counts.",
    ),
    obs_sas_pareto: (
        0.90,
        "Pareto optimality of SAS in Fig. 2 is a visual/analytical claim from "
        "standardized Z-scores. Robust across many model-architecture pairs.",
    ),
    obs_latency_tokens: (
        0.92,
        "Latency and token counts are directly measured hardware metrics with minimal "
        "interpretation required. Reproducible under controlled H100 settings.",
    ),
    obs_energy_per_token: (
        0.91,
        "Energy per token is derived from controlled H100 GPU experiments. High "
        "reliability; minor uncertainty from measurement overhead attribution.",
    ),
    obs_base_uturn: (
        0.88,
        "U-turn pattern observed in Fig. 2 for Base 8B-10B models. Directional trend "
        "clear from composite Z-score data; interpretation requires careful reading.",
    ),
    obs_mas_bankruptcy: (
        0.85,
        "MAS wins on bankruptcy prediction in Fig. 3. Leading advantage may vary by "
        "model; 'often with small margin' introduces some uncertainty.",
    ),
    obs_mas_variance: (
        0.87,
        "High variance in MAS directly visible in Fig. 2 scatter plot. Some "
        "model-specific effects may contribute but overall pattern holds.",
    ),
    obs_sas_reasoning_tasks: (
        0.88,
        ">150% improvement for Qwen2.5-0.5B and Llama-2-7B on QA/summarization is "
        "a specific quantitative observation from Fig. 3. Valid for those pairs.",
    ),
    obs_base_classification: (
        0.87,
        "Base SLM competitive on NER/sentiment from Fig. 3 heatmap. Gemma-3-270M case "
        "clear (agent systems fail); other cases are less decisive.",
    ),
    obs_sas_failure_modes: (
        0.89,
        "Failure mode categorization from Fig. 4 based on direct classification of "
        "inference failures. Classification taxonomy may have edge cases.",
    ),
    obs_mas_failure_modes: (
        0.89,
        "Same as obs_sas_failure_modes — direct failure classification from Fig. 4.",
    ),
    # ── Design/architectural descriptions (factual) ───────────────────────────
    base_slm_design: (
        0.97,
        "Factual description of experimental setup verifiable from paper Section 3.1.1.",
    ),
    sas_design: (
        0.96,
        "Factual description of SAS architecture verifiable from paper Section 3.1.2.",
    ),
    mas_design: (
        0.96,
        "Factual description of MAS architecture verifiable from paper Section 3.1.3.",
    ),
    prompt_design: (
        0.94,
        "Description of prompt engineering principles from Appendix E. Factual.",
    ),
    study_limitations: (
        0.96,
        "Author-stated limitations from Section 5.3. Factual self-assessment.",
    ),
    # ── Motivating/theoretical claims ─────────────────────────────────────────
    llm_deployment_cost: (
        0.90,
        "Well-established: LLMs have high compute, latency, and privacy costs. "
        "Widely accepted in literature and industry practice.",
    ),
    slm_inherent_limits: (
        0.88,
        "SLM limitations in reasoning and knowledge documented in Shen et al. 2024 "
        "and Haque et al. 2025. Some SLM families have improved but limitations persist.",
    ),
    fine_tuning_impractical: (
        0.83,
        "Impracticality for resource-constrained orgs is context-dependent. "
        "Well-supported for SMEs; not universal.",
    ),
    existing_benchmarks_gap: (
        0.85,
        "Claim supported by survey of HELM/Open LLM Leaderboard literature. Slight "
        "overstatement possible — some benchmarks do measure latency.",
    ),
    agent_potential: (
        0.80,
        "Agent paradigms as compensation mechanisms have theoretical backing (Shen "
        "et al. 2024) but the claim is prospective. This paper partially validates it.",
    ),
    scaling_law_predicts_monotone: (
        0.75,
        "Neural scaling law (Kaplan 2020) is well-established but applies to training "
        "loss, not task performance in constrained deployment. The extrapolation to "
        "monotone task-level performance is an over-simplification.",
    ),
    # ── Abduction alternative ──────────────────────────────────────────────────
    alt_sas_ineffective: (
        0.20,
        "The alternative that SLMs are too limited for effective tool use predicts "
        "NRQ near 0. Observed NRQ of 4.85 strongly disconfirms this. Partially holds "
        "for very small models (Gemma-3-270M) but fails overall.",
    ),
    pred_sas_effective: (
        0.85,
        "Hypothesis that tool access improves NRQ via knowledge retrieval is well-"
        "motivated: calculators enable exact arithmetic, web search retrieves current "
        "financial data. Prior reflects theoretical plausibility.",
    ),
}
