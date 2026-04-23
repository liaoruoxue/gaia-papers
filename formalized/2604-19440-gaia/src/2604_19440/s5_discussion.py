"""Section 5: Discussion and Conclusion — Implications and Limitations"""

from gaia.lang import claim, setting, support
from .motivation import (
    llm_mutation_differs,
    exploration_exploitation_classical,
    llm_as_search_operators,
)
from .s4_results import (
    optimizable_ability_distinct,
    local_refiner_hypothesis,
    novelty_conditional_on_localization,
    lrr_predicts_strongly,
    cost_efficiency_frontier,
    temperature_robustness,
    model_mixing_degrades_performance,
    novelty_not_significant,
)

# ── Conceptual implications ─────────────────────────────────────────────────

llm_evolution_differs_from_classical = claim(
    "LLM-guided evolution differs qualitatively from classical evolutionary algorithms. "
    "The LLM mutation operator is not random but instantiates a learned generative "
    "prior that induces structured, semantically meaningful variations, strongly "
    "biasing the search toward exploitation rather than random exploration. "
    "This makes novelty-as-exploration a misleading proxy in the LLM setting: "
    "LLM-generated novelty does not arise from blind exploration but from semantic "
    "variation conditioned on parent solutions and fitness context.",
    title="LLM evolution: structured exploitation, not random exploration",
)

strat_llm_differs = support(
    [novelty_not_significant],
    llm_evolution_differs_from_classical,
    reason=(
        "The LLM mutation operator is conditioned on parent candidates and their fitness "
        "(as described in @llm_mutation_differs), making exploration more constrained "
        "than in classical stochastic mutation. @novelty_not_significant confirms "
        "empirically that higher LLM-generated novelty does not translate to better "
        "outcomes—precisely because novelty in this setting reflects the LLM's semantic "
        "variation patterns rather than random coverage of the search space. "
        "Together, these establish that classical exploration–exploitation intuitions "
        "from @exploration_exploitation_classical do not transfer directly to LLM-guided "
        "evolution."
    ),
    prior=0.87,
    background=[exploration_exploitation_classical, llm_as_search_operators,
                llm_mutation_differs],
)

refinement_is_system_property = claim(
    "Local refinement behavior should not be viewed as an inherent property of the "
    "base model alone. It emerges as a property of the entire agentic system: "
    "the model, the prompting strategy, and the decoding configuration. "
    "Temperature changes affect both refinement rates and performance, but the "
    "relationship between refinement behavior and performance remains stable across "
    "a wide range of temperature settings (Table 11: Pearson r = 0.76-0.92 on TSP).",
    title="Refinement is a system property (model + prompt + decoding), not just model",
)

strat_system_property = support(
    [temperature_robustness],
    refinement_is_system_property,
    reason=(
        "The temperature sensitivity analysis (@temperature_robustness) shows that "
        "the LRR–performance correlation holds across a wide temperature range "
        "(T ∈ {0.0–1.3}), ruling out that refinement behavior is tied to a specific "
        "decoding hyperparameter. This supports viewing refinement behavior as an "
        "emergent property of the combined system rather than a fixed model attribute, "
        "suggesting that prompting and decoding can modulate it."
    ),
    prior=0.83,
    background=[],
)

design_implication_select_refiners = claim(
    "For practitioners designing LLM-based optimization systems, the primary "
    "objective should be to control and optimize refinement behavior, rather than "
    "simply maximizing base model capability or using the most expensive model. "
    "Smaller or cheaper models with strong inductive biases toward local refinement "
    "can outperform larger models that produce high-novelty but low-refinement "
    "offspring. Model selection should consider LRR, not just zero-shot benchmarks.",
    title="Design implication: optimize for refinement behavior, not base capability",
)

strat_design_implication = support(
    [optimizable_ability_distinct, cost_efficiency_frontier, lrr_predicts_strongly],
    design_implication_select_refiners,
    reason=(
        "Since @optimizable_ability_distinct establishes that refinement ability is "
        "dissociable from zero-shot capability, and @cost_efficiency_frontier shows "
        "that high-LRR models like Mistral-24B-Instruct reach the Pareto frontier of "
        "cost-performance, and @lrr_predicts_strongly demonstrates LRR explains more "
        "variance than zero-shot, the actionable implication is to evaluate and select "
        "models for their refinement behavior. This is a novel evaluation criterion "
        "beyond standard LLM benchmarks."
    ),
    prior=0.85,
)

training_implication = claim(
    "The results support training or fine-tuning LLMs specifically as effective "
    "search operators—emphasizing local refinement and error correction rather than "
    "general-purpose capability. Specialized training objectives targeting high LRR "
    "may yield better evolutionary search operators than general capability scaling.",
    title="Training implication: specialize LLMs as local refiners",
)

strat_training_implication = support(
    [optimizable_ability_distinct, model_mixing_degrades_performance],
    training_implication,
    reason=(
        "Since @optimizable_ability_distinct shows refinement ability is separable from "
        "general capability, and @model_mixing_degrades_performance confirms that "
        "refinement behavior causally drives performance, it follows that targeted "
        "training objectives for refinement (rather than general capability) could "
        "improve evolutionary search without requiring larger or more expensive models. "
        "This is consistent with the EvoTune and related work directions."
    ),
    prior=0.75,
)

novelty_reinterpretation = claim(
    "Novelty's role in LLM-guided evolutionary search is reinterpreted: rather than "
    "being a stochastic explorer, novelty acts as an immediate driver of exploratory "
    "breakthroughs, but its long-term utility depends on whether the search regime "
    "allows these deviations to be selectively retained and amplified. "
    "In localized, high-performing regions, novelty is productive. "
    "In diffuse, low-quality regions, novelty is largely unproductive or harmful.",
    title="Novelty reinterpreted: immediate driver of exploration, context-dependent utility",
)

strat_novelty_reinterp = support(
    [novelty_conditional_on_localization, novelty_not_significant],
    novelty_reinterpretation,
    reason=(
        "The mixed-effects model reveals a nuanced picture: @novelty_conditional_on_localization "
        "shows novelty's positive main effect (p=0.006) is cancelled by the negative "
        "novelty × H_spatial interaction (p<0.001). @novelty_not_significant confirms "
        "that averaged across all search states (including diffuse ones), novelty does "
        "not predict final performance. Together: novelty is a conditional resource—"
        "useful when spent within an already-exploitable region, wasteful otherwise. "
        "This reconciles novelty's intuitive appeal with the empirical null result."
    ),
    prior=0.85,
)

# ── Limitations ─────────────────────────────────────────────────────────────

limitation_fixed_protocol = claim(
    "The study relies on a fixed evolutionary protocol. Other design choices—"
    "selection pressure, offspring size, alternative sampling strategies—may "
    "influence the exploration–exploitation balance and cross-model differences. "
    "The findings may not generalize to evolutionary loops with substantially "
    "different hyperparameter configurations.",
    title="Limitation: fixed evolutionary protocol may not generalize",
)

limitation_novelty_operationalization = claim(
    "Novelty is primarily operationalized as nearest-neighbor distance. "
    "Broader comparisons to KNN/average-distance novelty and alternative diversity "
    "indices would help assess the robustness of the null novelty result.",
    title="Limitation: novelty operationalized as nearest-neighbor distance only",
)

limitation_model_mixing_confound = claim(
    "The model mixing perturbation study cannot fully isolate local refinement "
    "behavior. Replacing the model that generates offspring may also affect other "
    "latent characteristics (e.g., reasoning patterns or exploration tendencies), "
    "making it difficult to attribute all performance differences solely to "
    "local refinement rate.",
    title="Limitation: model mixing may confound refinement with other latent properties",
)

# Limitations reduce confidence in training_implication (model mixing confound)
# and in the generalizability of design_implication_select_refiners

strat_limitations_qualify_design = support(
    [limitation_fixed_protocol, limitation_model_mixing_confound,
     limitation_novelty_operationalization],
    design_implication_select_refiners,
    reason=(
        "The stated limitations partially qualify the design implication: "
        "@limitation_fixed_protocol means that findings may not generalize to "
        "evolutionary loops with very different selection pressure or offspring size; "
        "@limitation_model_mixing_confound means that model mixing evidence for the "
        "causal role of LRR is not fully isolated; "
        "@limitation_novelty_operationalization means the null novelty result could "
        "be sensitive to the choice of novelty metric. "
        "These limitations lower (but do not eliminate) confidence in "
        "@design_implication_select_refiners as a universal prescription."
    ),
    prior=0.65,
)
