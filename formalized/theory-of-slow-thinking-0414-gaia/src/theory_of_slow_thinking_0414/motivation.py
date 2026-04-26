"""Introduction and Motivation: First-Principles Theory of Slow Thinking"""

from gaia.lang import claim, setting, question, support, deduction, contradiction

# ── Background settings ──────────────────────────────────────────────────────

paper_scope = setting(
    "This paper presents a mathematical first-principles theory of slow thinking "
    "(also called 'active perception') — formalized as a theory called 'active lifting'. "
    "The theory is the first in a planned series covering cognitive functions including "
    "thinking, perception, memory, and spontaneous self-directed learning.",
    title="Scope of paper",
)

ai_evolution_context = setting(
    "The field of AI has advanced through engineering trial-and-error rather than "
    "first principles, leading to periodic over-predictions, resource waste, and "
    "directional errors. By analogy with aviation (which succeeded by first understanding "
    "lift and drag via gas dynamics rather than studying bird anatomy in detail), "
    "a mathematical theory of cognitive functions can serve as first principles for AI.",
    title="Motivation from AI history",
)

slow_thinking_definition = setting(
    "In cognitive science, 'fast thinking' (System 1) refers to unconscious, instinctive "
    "mental processes, and 'slow thinking' (System 2) refers to conscious, deliberative "
    "thinking [@Kahneman2011]. In machine learning, slow thinking refers to the generation "
    "of hidden texts (often called chain-of-thoughts) during the encoding and decoding of "
    "large language models (LLMs), which enhances their performance. Active perception "
    "means converting observations to 'understandable descriptions' with agency: freedom "
    "to invent such descriptions and search for the right one per observation.",
    title="Slow thinking and active perception defined",
)

lifting_problem_setting = setting(
    "Problem 1 (informal): Let P* be a probability distribution over an arbitrary data space X. "
    "Let P_M be the space of distributions modelable under computational constraints (e.g., "
    "parametrizable by neural networks or bounded-depth polynomial-size Boolean circuits). "
    "Construct a 'lifted' version of P* that belongs to P_M by converting P* to a distribution "
    "P_lift over a larger 'latent space' Z so that its structure is unfolded and becomes easier to model.",
    title="Core lifting problem (Problem 1)",
)

# ── Core claims ───────────────────────────────────────────────────────────────

claim_slow_thinking_is_lifting = claim(
    "Slow thinking of LLMs is mathematically a special case of the active lifting theory. "
    "Slow thinking can be understood as LLMs inventing a mental language (the chain-of-thoughts) "
    "to unravel complicated reasoning in input texts, which is formally a lifting of the "
    "observable distribution to a latent sequence space.",
    title="Slow thinking as special case of active lifting",
)

claim_active_lifting_derives_language = claim(
    "The active lifting framework gives rise to 'languages' that are both efficient "
    "(analogous to minimum-length coding) and regular (learnable by neural networks or "
    "bounded-depth circuits). It derives the notions of perceptual efficiency and linguistic "
    "regularity from first principles, thus providing one motivation for the invention of languages.",
    title="Active lifting derives efficient and regular languages",
)

claim_uncertainty_reduction_objective = claim(
    "The maximization of the rate of uncertainty reduction — formalized as minimizing "
    "sum_{t=0}^{inf} H_t, where H_t is the remaining uncertainty at step t — provides "
    "a unified objective that qualitatively derives the entire static theory (representation "
    "hierarchy and sampler hierarchy) and also motivates the active lifting framework.",
    title="Uncertainty reduction as unified objective",
)

claim_three_stage_improvement_roadmap = claim(
    "The theory yields a three-stage roadmap for improving slow thinking models: "
    "Stage 1 improves sampling efficiency via explanatory samplers; "
    "Stage 2 improves approximation ability via persistent and ubiquitous thinking plus "
    "an intrinsic balance of fast and slow thinking; "
    "Stage 3 enables free-form slow thinking unconstrained by any prescribed format.",
    title="Three-stage improvement roadmap",
)

claim_unified_encoder_approach = claim(
    "Active lifting provides a unified approach to constructing encoders for all data modalities. "
    "For image data in particular, the encoder might spontaneously develop a human-like multiscale "
    "compositional representation even without any such prior in its training or architecture.",
    title="Unified encoder approach for all modalities",
)

claim_policy_collapse_cause = claim(
    "A possible cause of the policy collapse problem in slow thinking model training is the "
    "omission of the inquisitive sampler during training. Existing models implement only the "
    "inference sampler (posterior sampler Q*) and train to fit only Q*, neglecting the "
    "inquisitive sampler Q-tilde. This creates a positive feedback cycle where the model "
    "increasingly concentrates sampling on existing modes, leading to entropy collapse.",
    title="Policy collapse cause: missing inquisitive sampler",
)

claim_linguistic_coupling_generative = claim(
    "Active lifting yields a new approach to generative modeling called 'linguistic coupling', "
    "as an alternative to free coupling (GANs, VAEs) and product coupling (diffusion, flow matching). "
    "It potentially solves the non-uniqueness problem of generative modeling by providing a "
    "principled target P*(x|z) for the generator.",
    title="Linguistic coupling: new generative modeling approach",
)

strat_slow_thinking_lifting = support(
    [claim_active_lifting_derives_language],
    claim_slow_thinking_is_lifting,
    reason=(
        "Given the @lifting_problem_setting that defines lifting as converting a target distribution "
        "to one over a larger latent space to make it modelable, and given @claim_active_lifting_derives_language "
        "showing that active lifting produces efficient and regular languages, the chain-of-thought "
        "process of slow thinking models matches this precisely: the 'thoughts' form a latent "
        "sequence space, the projection strips thoughts to recover observable tokens, and the "
        "resulting lifted distribution is easier to model by the LLM."
    ),
    prior=0.95,
    background=[lifting_problem_setting],
)

__all__ = [
    "claim_slow_thinking_is_lifting",
    "claim_active_lifting_derives_language",
    "claim_uncertainty_reduction_objective",
    "claim_three_stage_improvement_roadmap",
    "claim_unified_encoder_approach",
    "claim_policy_collapse_cause",
    "claim_linguistic_coupling_generative",
]
