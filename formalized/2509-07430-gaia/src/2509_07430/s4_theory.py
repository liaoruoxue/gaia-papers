"""Section 4: Theoretical Analysis — Enhanced Monotonic Improvement Guarantee"""

from gaia.lang import claim, setting

from .motivation import f_divergence_setting, rlvr_setting
from .s2_background import trpo_bound, forward_kl_mass_covering, js_mass_covering
from .s3_method import (
    dphrl_objective,
    dataset_partition,
    exploration_loss,
    preservation_loss,
)

# ── Settings ──────────────────────────────────────────────────────────────────

assumption1 = setting(
    "Assumption 1 (Bounded advantage on preservation set): There exist constants "
    "$C_f > 0$ and $\\delta > 0$ such that for all $q \\in \\mathcal{D}_{pef}$ and "
    "all actions $a$, the advantage function satisfies a bound involving the "
    "f-divergence penalty term, yielding $\\varepsilon_f = \\delta/(1-\\gamma) - "
    "C_f \\gamma \\alpha_2 \\varepsilon_{pef}/(1-\\gamma)^2 > 0$ when the f-divergence "
    "regularization effectively captures the structure of near-perfect queries.",
    title="Assumption 1: bounded advantage on D_pef",
)

# ── Claims ────────────────────────────────────────────────────────────────────

theorem1_statement = claim(
    "Theorem 1 (Enhanced Monotonic Improvement): Let $\\alpha_1 = \\max_s D_{KL}(\\pi(\\cdot|s) \\| \\pi_{old}(\\cdot|s))$ "
    "and $\\alpha_2 = \\max_s D_f(\\pi(\\cdot|s) \\| \\pi_{pef}(\\cdot|s))$ where $\\pi_{pef}$ "
    "is the policy restricted to the near-perfect set. Under Assumption 1, DPH-RL's policy "
    "improvement satisfies: "
    "$J(\\pi) - L_{\\pi_{old}}(\\pi) \\geq -\\frac{2\\gamma\\alpha_1 \\varepsilon_\\pi}{(1-\\gamma)^2} + \\varepsilon_f$, "
    "where $\\varepsilon_f = \\frac{\\delta}{1-\\gamma} - \\frac{C_f \\gamma \\alpha_2 \\varepsilon_{pef}}{(1-\\gamma)^2} > 0$. "
    "The term $\\varepsilon_f > 0$ provides a strictly better lower bound on policy improvement "
    "than the standard TRPO bound (which lacks the $+\\varepsilon_f$ term).",
    title="Theorem 1: enhanced monotonic improvement",
)

theorem1_interpretation = claim(
    "The positive bonus term $\\varepsilon_f$ in Theorem 1 arises because "
    "f-divergence regularization on $\\mathcal{D}_{pef}$ leverages the expert behavior "
    "of near-perfect queries: the policy is incentivized to stay close to the reference "
    "on queries it already handles well, which guarantees positive advantage contributions "
    "from those queries. This is an improvement over the standard TRPO guarantee that only "
    "provides a lower bound (no positive bonus).",
    title="Theorem 1: source of positive bonus",
)

trpo_standard_vs_dphrl = claim(
    "The standard TRPO/PPO bound gives $J(\\pi) - L_{\\pi_{old}}(\\pi) \\geq -\\frac{2\\gamma\\alpha_1\\varepsilon_\\pi}{(1-\\gamma)^2}$, "
    "which can be negative (no guaranteed improvement). DPH-RL's bound adds $+\\varepsilon_f > 0$, "
    "providing a strictly tighter guarantee. The gap between the two bounds is $\\varepsilon_f > 0$.",
    title="DPH-RL vs TRPO improvement bound comparison",
)

grpo_no_bound = claim(
    "GRPO (without KL constraint) does not admit the enhanced TRPO-style monotonic "
    "improvement bound because it lacks any divergence term. The absence of $D_f$ means "
    "there is no $\\varepsilon_f$ bonus: the policy can drift arbitrarily from the reference, "
    "losing existing capabilities without a formal guarantee against forgetting.",
    title="GRPO lacks monotonic improvement guarantee",
)

__all__ = [
    "theorem1_statement",
    "theorem1_interpretation",
    "trpo_standard_vs_dphrl",
    "grpo_no_bound",
]
