"""Section 5: Discussion, Limitations, and Future Directions"""

from gaia.lang import claim, setting, support

from .s3_mce_framework import (
    mce_opens_design_space,
    skill_unifies_levels,
    agentic_crossover_claim,
    mce_decouples_what_how,
)
from .s4_ablations import mce_law, model_confound_ruled_out

# ── Limitations ────────────────────────────────────────────────────────────────

mce_agentic_model_bottleneck = claim(
    "MCE's meta-level performance is currently bounded by the quality of the agentic model "
    "(MiniMax M2.1 in experiments). As agentic models continue to improve, the meta-level "
    "skill evolution is expected to scale better and this bottleneck is expected to diminish.",
    title="MCE performance bounded by agentic model quality (current limitation)",
)

strat_bottleneck = support(
    [agentic_crossover_claim],
    mce_agentic_model_bottleneck,
    reason=(
        "Agentic crossover (@agentic_crossover_claim) is the meta-level operation that synthesizes "
        "new skills. Its quality is directly determined by the agentic model's reasoning and "
        "synthesis capabilities. Better agentic models will produce better skill evolution and "
        "thus better MCE performance."
    ),
    prior=0.80,
)

mce_one_shot_retrieval = claim(
    "MCE's current experimental instantiation uses one-shot retrieval (query → context) "
    "for methodological consistency with CE baselines. An agentic generator that interacts "
    "directly with file-based context artifacts could be more effective but was not evaluated.",
    title="MCE currently limited to one-shot retrieval interface",
)

strat_one_shot = support(
    [mce_decouples_what_how],
    mce_one_shot_retrieval,
    reason=(
        "MCE's bi-level decoupling (@mce_decouples_what_how) separates the context optimization skill "
        "from the inference interface. In the current experiments, the retrieval interface is fixed "
        "as one-shot (query → context) to match baselines, but the framework does not require this — "
        "the context function could implement any retrieval or interaction pattern."
    ),
    prior=0.90,
)

# ── Future directions ──────────────────────────────────────────────────────────

future_skill_evolution_generalizes = claim(
    "The agentic skill evolution paradigm extends beyond context engineering. "
    "While prior evolutionary approaches target specific solutions, heuristic code, or search algorithms, "
    "MCE evolves skills — a higher-order and integrated abstraction essential for general AI. "
    "MCE is among the first to dynamically evolve skills, bridging manual skill engineering "
    "and autonomous self-improvement.",
    title="Skill evolution paradigm generalizes beyond CE",
)

strat_skill_generalizes = support(
    [skill_unifies_levels, mce_opens_design_space],
    future_skill_evolution_generalizes,
    reason=(
        "Skills (@skill_unifies_levels) are a higher-order abstraction that encapsulate procedures "
        "rather than specific outcomes. The new design space opened by MCE (@mce_opens_design_space) "
        "is not CE-specific — the same meta-level evolution framework could apply to other agentic "
        "capability domains."
    ),
    prior=0.78,
)

future_agentic_generator = claim(
    "Extending MCE to co-evolve context utilization skills alongside context learning skills "
    "is a promising future direction. An agentic generator that interacts directly with "
    "file-based context artifacts could leverage the context more effectively than one-shot retrieval.",
    title="Future: co-evolve context utilization skills",
)

strat_future_agentic = support(
    [mce_one_shot_retrieval],
    future_agentic_generator,
    reason=(
        "MCE's current one-shot retrieval interface (@mce_one_shot_retrieval) is a methodological "
        "constraint imposed for fair comparison with baselines. Relaxing this to allow agentic "
        "interaction with file-based contexts would enable the generator to exploit context structure "
        "more effectively, suggesting a natural extension."
    ),
    prior=0.75,
)

future_skill_composition = claim(
    "Progressive skill disclosure is native to agent skills: agents load skill details into "
    "context only when relevant. This enables MCE to compose and scale skills across domains "
    "with minimal overhead. Investigating skill transfer across tasks and emergent behaviors "
    "from skill composition are interesting open questions.",
    title="Future: skill transfer and composition across domains",
)

strat_future_composition = support(
    [future_skill_evolution_generalizes, skill_unifies_levels],
    future_skill_composition,
    reason=(
        "Because the skill evolution paradigm generalizes beyond CE (@future_skill_evolution_generalizes) "
        "and skills are modular file-based artifacts (@skill_unifies_levels), composing skills across "
        "domains is architecturally natural and represents a logical next step."
    ),
    prior=0.72,
)

mce_reformulates_ce = claim(
    "MCE reformulates context engineering as a learnable agentic capability, unlocking a generic "
    "design space for optimizing general AI. The vision is agents that not only execute tasks "
    "but continuously refine their learning algorithms and memory architectures, enabling "
    "open-ended self-evolution.",
    title="MCE reformulates CE as learnable agentic capability",
)

strat_mce_reformulates = support(
    [mce_opens_design_space, model_confound_ruled_out, mce_law],
    mce_reformulates_ce,
    reason=(
        "MCE opens a new meta-level design space (@mce_opens_design_space) independent of the "
        "specific agentic model (@model_confound_ruled_out), and demonstrates consistent superiority "
        "across diverse domains (@mce_law). Together these establish that the MCE framework itself "
        "is a principled advance in the design of self-improving agentic systems."
    ),
    prior=0.82,
)
