"""Section 5: Analysis — Limitations, Generality, and Future Directions"""

from gaia.lang import (
    claim, setting, question,
    support, deduction, contradiction,
)

from .motivation import (
    claim_coral_outperforms_fixed,
    claim_multi_agent_gains,
    claim_knowledge_causal,
    claim_agents_adaptable,
)
from .s2_framework import (
    claim_safety_mechanisms,
    claim_no_fixed_algorithm,
    claim_evaluator_design,
)
from .s3_single_agent import (
    claim_sota_8_tasks,
    claim_open_source_validates,
    claim_improvement_rate,
)
from .s4_multi_agent import (
    claim_strategy_diversity,
    claim_knowledge_creation_differential,
    claim_coevolution_beats_independent,
    claim_cross_agent_transfer_kernel,
)

# =============================================================================
# Limitation claims
# =============================================================================

claim_frontier_model_dependency = claim(
    "CORAL currently requires frontier foundation models (e.g., Claude Opus 4.6) to "
    "achieve its performance advantages. The framework's autonomous strategy discovery, "
    "knowledge synthesis, and adaptive reflection depend on models with strong code "
    "generation, reasoning, and instruction-following capabilities. Smaller or weaker "
    "models may not produce the emergent behaviors (local verification, knowledge "
    "creation, strategic pivots) that drive CORAL's performance gains.",
    title="Limitation: requires frontier foundation models",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

claim_homogeneous_agents = claim(
    "CORAL's current implementation uses homogeneous agents: all agents run the same "
    "model with the same system prompt and no injected personality differences. This "
    "means agent diversity emerges purely from stochastic sampling and different "
    "exploration histories. The lack of bootstrapped heterogeneity may limit the "
    "extent of specialization achievable through co-evolution.",
    title="Limitation: homogeneous agents lack bootstrapped diversity",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

claim_evaluator_assumption = claim(
    "CORAL assumes a well-specified, reliable evaluator that agents cannot easily "
    "game or circumvent. In practice, open-ended discovery problems may not have "
    "such clean evaluation functions: natural science experiments may be expensive "
    "or impossible to automate, social science outcomes may be difficult to quantify, "
    "and creative tasks may require human evaluation. CORAL's current design does "
    "not address co-evolution of evaluation criteria alongside solutions.",
    title="Limitation: assumes well-specified evaluator",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

claim_compute_cost = claim(
    "CORAL with frontier models (Claude Opus 4.6) incurs substantial API costs per "
    "evaluation run. Each agent iteration involves multiple LLM calls (reflection, "
    "code generation, consolidation heartbeats), making large-scale deployment "
    "economically intensive. The open-source model validation (MiniMax-M2.5, OpenCode) "
    "partially addresses this but at some performance cost.",
    title="Limitation: high compute cost with frontier models",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

# =============================================================================
# Future directions (as claims about potential extensions)
# =============================================================================

claim_specialized_training = claim(
    "Future work could train specialized smaller models as CORAL agents by using "
    "the framework's trajectory data (attempts, notes, skills) as supervision signal. "
    "A model trained on successful CORAL trajectories might achieve comparable "
    "performance at lower inference cost than frontier models, addressing the "
    "compute limitation.",
    title="Future: train specialized smaller agent models",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

claim_agent_personalities = claim(
    "Injecting distinct agent personalities (e.g., specialist vs. generalist, "
    "exploiter vs. explorer, mathematician vs. engineer) into the system prompt "
    "could bootstrap the strategic heterogeneity needed to further improve "
    "co-evolution efficiency, reducing the Jaccard similarity below the emergent "
    "0.31–0.43 observed in homogeneous runs.",
    title="Future: inject distinct agent personalities",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

claim_coeolving_evaluators = claim(
    "Co-evolving evaluation criteria alongside solutions—having agents propose "
    "improvements to the grader as well as to the solution—could extend CORAL to "
    "open-ended problems where the evaluation function is itself uncertain or "
    "evolving. This requires mechanisms to prevent Goodhart's Law dynamics where "
    "agents optimize for proxy metrics rather than the true objective.",
    title="Future: co-evolve evaluation criteria",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

# =============================================================================
# Generality and scope claims
# =============================================================================

claim_domain_generality = claim(
    "CORAL's performance advantage spans two structurally different problem categories "
    "(mathematical optimization and systems engineering), and the open-source model "
    "validation shows the framework design is not model-specific. This domain generality "
    "supports the claim that CORAL's design principles (shared memory, heartbeats, "
    "autonomous strategy) are broadly applicable to open-ended discovery, not "
    "specialized to a particular problem type.",
    title="CORAL's advantages are domain-general",
    metadata={"source": "artifacts/2604-01658.pdf, Section 5"},
)

claim_emergent_specialization = claim(
    "Co-evolving CORAL agents spontaneously develop specialized roles without explicit "
    "role assignment. On Kernel Engineering, analysis shows agents naturally diverge "
    "into exploration-heavy and exploitation-heavy behaviors based on their accumulated "
    "experience, even though all agents start with identical prompts and capabilities. "
    "This emergent specialization contributes to the co-evolution advantage over "
    "independent parallel search.",
    title="Agents develop emergent specialization",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.4"},
)

# =============================================================================
# Strategies
# =============================================================================

strat_frontier_limits_scope = support(
    [claim_frontier_model_dependency],
    claim_compute_cost,
    reason=(
        "The frontier model dependency (@claim_frontier_model_dependency) directly implies "
        "high compute cost (@claim_compute_cost): frontier models like Claude Opus 4.6 have "
        "substantially higher per-token costs than smaller models. Each CORAL iteration "
        "involves multiple LLM calls, multiplying this cost across many evaluations and "
        "multiple agents."
    ),
    prior=0.88,
)

strat_homogeneity_limits_diversity = support(
    [claim_homogeneous_agents],
    claim_strategy_diversity,
    reason=(
        "Homogeneous agents (@claim_homogeneous_agents) constrain the achievable strategic "
        "diversity: the Jaccard similarity of 0.31–0.43 (@claim_strategy_diversity) is the "
        "maximum achievable through stochastic variation alone. With injected personality "
        "differences, diversity could be higher, suggesting the observed diversity represents "
        "a lower bound on what co-evolution could achieve with heterogeneous agents."
    ),
    prior=0.75,
)

strat_domain_general_from_results = support(
    [claim_sota_8_tasks, claim_open_source_validates],
    claim_domain_generality,
    reason=(
        "SOTA on 8/11 tasks spanning two categories (@claim_sota_8_tasks) demonstrates "
        "cross-domain applicability. Open-source model validation (@claim_open_source_validates) "
        "demonstrates cross-model applicability. Together these provide evidence for "
        "domain generality (@claim_domain_generality) beyond any single problem type or "
        "model family."
    ),
    prior=0.80,
)

strat_emergent_specialization_from_diversity = support(
    [claim_strategy_diversity, claim_cross_agent_transfer_kernel],
    claim_emergent_specialization,
    reason=(
        "Strategic diversity (@claim_strategy_diversity, Jaccard 0.43 for Kernel Engineering) "
        "combined with high cross-agent transfer rates (36% of attempts build on other agents' "
        "work, @claim_cross_agent_transfer_kernel) implies agents developed complementary "
        "specializations: some agents produce the novel solutions (exploration) while others "
        "refine and combine them (exploitation), with transfer enabling cross-specialization "
        "learning."
    ),
    prior=0.72,
)

strat_personality_from_homogeneity = support(
    [claim_homogeneous_agents, claim_emergent_specialization],
    claim_agent_personalities,
    reason=(
        "If homogeneous agents (@claim_homogeneous_agents) can still achieve Jaccard "
        "similarity 0.31–0.43 through emergent specialization (@claim_emergent_specialization), "
        "then injecting distinct personalities (@claim_agent_personalities) would amplify "
        "this differentiation, potentially achieving lower similarity (more diversity) and "
        "stronger co-evolution benefits."
    ),
    prior=0.70,
)

strat_evaluator_assumption_from_design = support(
    [claim_evaluator_design],
    claim_evaluator_assumption,
    reason=(
        "The evaluator design (@claim_evaluator_design) assumes a pluggable, well-specified "
        "grader with clear scoring. This design choice embeds the assumption (@claim_evaluator_assumption) "
        "that the evaluation function is reliable, automatable, and tamper-resistant. Tasks "
        "where the evaluator cannot be well-specified (e.g., natural science experiments, "
        "creative tasks) fall outside CORAL's current scope."
    ),
    prior=0.85,
)

strat_specialized_training_from_cost = support(
    [claim_compute_cost, claim_frontier_model_dependency],
    claim_specialized_training,
    reason=(
        "The high compute cost of frontier model dependency (@claim_compute_cost, "
        "@claim_frontier_model_dependency) motivates the future direction of training "
        "specialized smaller models (@claim_specialized_training). If CORAL trajectories "
        "(attempts, notes, skills) provide supervision signal, smaller models trained on "
        "these trajectories could achieve comparable performance at lower inference cost."
    ),
    prior=0.70,
)

strat_coevolving_evaluators_from_assumption = support(
    [claim_evaluator_assumption],
    claim_coeolving_evaluators,
    reason=(
        "The evaluator assumption limitation (@claim_evaluator_assumption)—that CORAL requires "
        "well-specified evaluation functions—motivates the future direction of co-evolving "
        "evaluation criteria (@claim_coeolving_evaluators). If evaluation criteria could "
        "be refined alongside solutions, CORAL could extend to problems where the objective "
        "function itself is uncertain or evolving."
    ),
    prior=0.65,
)
