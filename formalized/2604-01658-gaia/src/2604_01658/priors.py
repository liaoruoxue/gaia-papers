"""
Priors for CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery.

Calibration basis:
- High confidence (0.85–0.95): Directly reported experimental measurements or design facts
  stated by the authors as implemented architecture choices.
- Moderate-high (0.70–0.85): Well-supported empirical findings with consistent direction
  but some variability across conditions.
- Moderate (0.50–0.70): Qualitative claims without strong quantitative backing, or
  theoretical projections.
- Alternatives (0.15–0.35): Competing hypotheses that the paper provides evidence against.
"""

from . import (
    # Independent premises (leaf claims needing priors)
    claim_agents_adaptable,
    claim_async_execution,
    claim_cross_agent_transfer_kernel,
    claim_evaluator_design,
    claim_frontier_model_dependency,
    claim_homogeneous_agents,
    claim_knowledge_access_correlates,
    claim_persistent_memory_design,
    # Abduction alternative hypotheses
    alt_additional_compute_explains,
    alt_fixed_algorithm_sufficient,
    # Abduction prediction claims (from compare)
    pred_coordination,
    pred_compute,
)

PRIORS: dict = {
    # =========================================================================
    # Framework design facts (author-stated architectural choices)
    # =========================================================================
    claim_persistent_memory_design: (
        0.92,
        "The shared persistent memory structure (attempts/, notes/, skills/) is an explicit "
        "architectural design choice stated as implemented. The filesystem implementation "
        "with symbolic links is described in detail. High confidence as a design fact."
    ),
    claim_async_execution: (
        0.92,
        "Asynchronous multi-agent execution with isolated workspaces is an explicit "
        "architectural design stated as implemented. Confidence is high as a factual "
        "description of the framework's implementation."
    ),
    claim_evaluator_design: (
        0.90,
        "The pluggable evaluator hierarchy with YAML task definitions is a concrete "
        "implementation detail the authors describe as part of the deployed system. "
        "High confidence as a stated design fact."
    ),

    # =========================================================================
    # Empirical findings from trajectory analysis
    # =========================================================================
    claim_agents_adaptable: (
        0.82,
        "Agent adaptability (varying local verification 11–61%, knowledge access 7–30%, "
        "Jaccard similarity 0.31–0.43) is reported from trajectory analysis across "
        "multiple tasks and runs. These are measured behaviors from 4 independent trials. "
        "Moderate-high confidence: the pattern is consistent but derived from a limited "
        "set of tasks and runs."
    ),
    claim_cross_agent_transfer_kernel: (
        0.85,
        "Cross-agent transfer statistics (36% of attempts, 17% vs. 9% improvement rate, "
        "66% of records from cross-agent parentage) are directly measured from agent "
        "trajectory logs on Kernel Engineering. High confidence as a directly observed "
        "empirical measurement, though limited to one task."
    ),
    claim_knowledge_access_correlates: (
        0.83,
        "Knowledge access correlation (55% improvement rate when accessing knowledge vs. "
        "26% without) is directly measured from trajectory analysis on Kernel Engineering. "
        "Moderate-high confidence: the correlation is strong and consistent, but correlation "
        "does not fully establish causation (addressed by ablation studies separately)."
    ),

    # =========================================================================
    # Limitation claims (about current system properties)
    # =========================================================================
    claim_frontier_model_dependency: (
        0.85,
        "The frontier model dependency is a stated limitation: Claude Opus 4.6 is used "
        "as the backbone, and the emergent behaviors (local verification, strategic pivots) "
        "are likely capability-dependent. The open-source validation shows performance "
        "generalizes partially, but the degree of frontier dependency is acknowledged "
        "by the authors. Moderate-high confidence."
    ),
    claim_homogeneous_agents: (
        0.95,
        "Homogeneous agent implementation (identical system prompt, same model, no injected "
        "personality differences) is a factual description of the current implementation "
        "explicitly acknowledged as a limitation by the authors. Very high confidence as "
        "a stated implementation fact."
    ),

    # =========================================================================
    # Alternative hypotheses (competing explanations for observed gains)
    # =========================================================================
    alt_additional_compute_explains: (
        0.15,
        "The additional compute explanation is falsified by the co-evolution vs. independent "
        "best-of-4 ablation: under identical compute, co-evolution wins by 6.5%. Prior is "
        "low because this alternative predicts no gap between co-evolution and independent "
        "search, but a clear gap is observed. pi(Alt) = 0.15 (cannot explain the observation)."
    ),
    alt_fixed_algorithm_sufficient: (
        0.10,
        "Fixed evolutionary algorithms being sufficient is falsified by direct comparison: "
        "CORAL achieves 3–10× higher improvement rates than all fixed baselines. This "
        "alternative predicts comparable performance, contradicted by consistent SOTA "
        "across 8/11 tasks. pi(Alt) = 0.10 (very low explanatory power for CORAL's gap)."
    ),

    # =========================================================================
    # Abduction prediction claims
    # =========================================================================
    pred_coordination: (
        0.85,
        "The coordination hypothesis prediction (co-evolution beats independent best-of-4) "
        "is confirmed by the experimental result. Prior reflects the pre-experiment "
        "plausibility of this prediction given the shared memory design."
    ),
    pred_compute: (
        0.20,
        "The compute-only prediction (independent best-of-4 matches co-evolution) is "
        "refuted by the 6.5% gap between co-evolution (1,103 cycles) and independent "
        "best-of-4 (1,180 cycles). Low prior as the experiment contradicts this prediction."
    ),
}
