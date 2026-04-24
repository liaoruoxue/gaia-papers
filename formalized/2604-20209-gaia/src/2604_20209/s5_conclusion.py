"""Section 5: Limitations and Conclusion"""

from gaia.lang import claim, setting, support

from .motivation import guide_hypothesis, conjecturer_collapse_hypothesis
from .s3_algorithm import setup_lean4_domain, sgs_two_mechanisms
from .s4_experiments import (
    sgs_higher_asymptotic_rate,
    entropy_conjecturer_coupling,
    solver_improves_steadily,
    reinforce_half_best_baseline,
)

# ── Claims: Limitations ───────────────────────────────────────────────────────

limitation_verifiable_domain = claim(
    "SGS is currently applied only to Lean4 formal theorem proving, a verifiable domain "
    "where the Conjecturer only needs to produce an initial state (problem statement) and "
    "the verification reward is provided automatically by the Lean4 compiler. Extending "
    "SGS to non-verifiable domains requires the Conjecturer to specify an entire MDP "
    "(goal, environment/simulator, and reward function), which is substantially harder.",
    title="SGS limited to verifiable domains; non-verifiable extension is open problem",
)

limitation_frozen_guide = claim(
    "In current SGS experiments, the Guide is frozen (not trained). A frozen Guide is "
    "sufficient to prevent Conjecturer collapse in the tested regime, but may be insufficient "
    "for scaling SGS to solve the most challenging problems. As self-play progresses, the "
    "characteristics of useful stepping-stone problems evolve, and a frozen Guide may "
    "fail to adapt. A natural extension is to train the Guide on Solver training dynamics "
    "(e.g., labeling synthetic problems that quickly lead to their target being solved as "
    "high reward).",
    title="Frozen Guide may be insufficient for hardest problems; trainable Guide is future work",
)

limitation_model_size = claim(
    "SGS experiments fix model size (7B) and scale along the compute axis. The interaction "
    "between SGS and model scale (larger Conjecturer producing higher-quality synthetic "
    "problems) is not tested. The hypothesis that SGS scales well with model size is stated "
    "but not confirmed.",
    title="SGS model-size scaling not tested; hypothesis pending confirmation",
)

# ── Claims: Conclusion ────────────────────────────────────────────────────────

conclusion_sgs_sustains_learning = claim(
    "SGS is an asymmetric self-play algorithm that sustains learning for longer than prior "
    "methods by addressing two instabilities: (1) Conjecturer collapse (solved by the Guide "
    "and problem conditioning), and (2) Solver entropy collapse (solved by the REINFORCE1/2 "
    "objective). The result is a self-play algorithm with a 7% higher asymptotic solve rate "
    "than the strongest RL baseline on formal theorem proving in Lean4.",
    title="SGS conclusion: sustains self-play learning via Guide and entropy management",
)

strat_conclusion = support(
    [sgs_two_mechanisms, entropy_conjecturer_coupling, sgs_higher_asymptotic_rate],
    conclusion_sgs_sustains_learning,
    reason=(
        "The two anti-collapse mechanisms of SGS (@sgs_two_mechanisms) directly address "
        "Conjecturer degradation. The identification of the Solver entropy-Conjecturer coupling "
        "(@entropy_conjecturer_coupling) and selection of REINFORCE1/2 as the Solver objective "
        "addresses the second instability. The empirical result of 7% higher asymptotic solve "
        "rate (@sgs_higher_asymptotic_rate) confirms that both interventions together produce "
        "a self-play algorithm that sustains improvement over long training runs [@Bailey2026]."
    ),
    prior=0.90,
)

future_non_verifiable = claim(
    "SGS could be extended to non-verifiable domains by using approximate verification: "
    "for coding problems (unit tests as verifier), for natural language math (learned "
    "verifiers that have improved rapidly), and for embodied control (VLM reward function "
    "with neural world model for environment generation). Imperfect verification may not "
    "strictly prevent effective self-play.",
    title="Future work: SGS extension to non-verifiable domains via approximate verification",
)

strat_future_non_verifiable = support(
    [limitation_verifiable_domain, future_non_verifiable],
    conclusion_sgs_sustains_learning,
    reason=(
        "The limitation to verifiable domains (@limitation_verifiable_domain) is not fundamental: "
        "approximate verifiers exist for coding, natural language math, and embodied control "
        "(@future_non_verifiable). This generalizability further supports the core claim that "
        "SGS sustains self-play learning (@conclusion_sgs_sustains_learning) beyond the specific "
        "Lean4 domain tested [@Bailey2026]."
    ),
    prior=0.75,
)

strat_limitation_frozen_guide = support(
    [limitation_frozen_guide],
    conclusion_sgs_sustains_learning,
    reason=(
        "The frozen Guide limitation (@limitation_frozen_guide) highlights that current SGS "
        "results are a lower bound on potential performance. If the Guide were trained to adapt "
        "over the course of self-play, the sustained learning benefit would likely be even larger. "
        "This limitation contextualizes the 7% improvement as achievable without a trainable Guide "
        "[@Bailey2026]."
    ),
    prior=0.72,
)

strat_limitation_scale = support(
    [limitation_model_size],
    conclusion_sgs_sustains_learning,
    reason=(
        "The model-size limitation (@limitation_model_size) means that SGS's scaling only along "
        "the compute axis (not model size) is a conservative test. The hypothesis that a larger "
        "Conjecturer would produce higher-quality synthetic problems further supports the claim "
        "that SGS can sustain learning, with model-scale improvements as an additional lever [@Bailey2026]."
    ),
    prior=0.70,
)
