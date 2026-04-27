"""Section 9: Conclusion and limitations."""

from gaia.lang import claim, support
from .motivation import (
    claim_curiosity_is_knowledge,
    claim_contribution_consistency,
    claim_contribution_regret,
    claim_contribution_design,
)
from .s5_consistency import claim_theorem_5_1
from .s6_regret import claim_theorem_6_1
from .s7_synthetic_experiments import (
    claim_th5_1_corroborated,
    claim_th6_1_corroborated,
)
from .s8_real_world import claim_real_world_corroborated

# --- Limitation claims ---

claim_lim_conservative = claim(
    "**Limitation: conservativeness.** The sufficient-curiosity guarantees of "
    "@claim_theorem_5_1 and @claim_theorem_6_1 are *sufficient but possibly "
    "conservative*: deriving tight or adaptive $\\beta_t$ schedules remains an "
    "open problem.",
    title="Limitation: bounds may be conservative",
)

claim_lim_assumptions = claim(
    "**Limitation: identifiability and regularity assumptions.** The results "
    "depend on identifiability and regularity assumptions (finite prior entropy, "
    "Lipschitz smoothness, bounded heuristic discrepancy). They can degrade "
    "under model misspecification, nonstationarity, or partial observability.",
    title="Limitation: dependence on identifiability/regularity",
)

claim_lim_alignment_practical = claim(
    "**Limitation: heuristic alignment in practice.** Controlling pragmatic "
    "heuristic alignment ($B_t$) in realistic tasks can be challenging, so the "
    "mechanism-focused experiments do not replace broader benchmarking.",
    title="Limitation: heuristic alignment is hard to control in practice",
)

# --- Final synthesis: the main thesis is supported by the four pillars ---
# Theorem 5.1 (proved + corroborated), Theorem 6.1 (proved + corroborated),
# real-world experiments, and the contribution claims.

sup_main_thesis = support(
    [
        claim_contribution_consistency,
        claim_contribution_regret,
        claim_contribution_design,
        claim_th5_1_corroborated,
        claim_th6_1_corroborated,
        claim_real_world_corroborated,
    ],
    claim_curiosity_is_knowledge,
    reason=(
        "@claim_curiosity_is_knowledge (the main thesis) is established by the "
        "four contribution pillars: (1) the proven posterior-consistency theorem "
        "@claim_contribution_consistency / @claim_theorem_5_1; (2) the proven "
        "cumulative-regret theorem @claim_contribution_regret / "
        "@claim_theorem_6_1; (3) the practical design guidelines "
        "@claim_contribution_design; plus empirical corroboration "
        "(@claim_th5_1_corroborated, @claim_th6_1_corroborated, "
        "@claim_real_world_corroborated). The two theorems share the *identical* "
        "sufficient-curiosity inequality, which is the structural fact that "
        "elevates curiosity to a unifying mechanism."
    ),
    prior=0.9,
)

# Mark the limitations as observations qualifying the main thesis.
support_limitations_qualify = support(
    [claim_lim_conservative, claim_lim_assumptions, claim_lim_alignment_practical],
    claim(
        "The sufficient-curiosity guarantee, while general, is *qualified*: "
        "it is conservative (not necessarily tight), assumption-dependent, and "
        "vulnerable to heuristic-alignment failures in deployment. These are "
        "explicit scope limits acknowledged by the paper.",
        title="Qualified scope of the main thesis",
    ),
    reason=(
        "The three limitation claims jointly constrain the deployment scope of "
        "@claim_curiosity_is_knowledge."
    ),
    prior=0.95,
)

