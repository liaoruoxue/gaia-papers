"""Section 4: Unified Objective — Maximizing the Rate of Uncertainty Reduction"""

from gaia.lang import claim, setting, support, deduction

from .motivation import claim_uncertainty_reduction_objective
from .s2_separation import claim_psimple_contains_phmm, claim_projection_reduces_norm
from .s3_samplers import claim_causal_samplers_inadequate, claim_scaling_laws_chi2

# ── Background settings ──────────────────────────────────────────────────────

uncertainty_reduction_objective_setting = setting(
    "The unified objective is: minimize int_0^{inf} C(theta_{step(t)}) dt, "
    "where C(theta) = -integral log P_theta^{<=|x|}(x) dP*(x) - H(P*) is the cross-entropy loss "
    "(reducible uncertainty). This integral objective rewards rapid reduction of C with respect "
    "to real time t, not just minimizing final loss. With step times t_s, this equals "
    "sum_s t_s * (C(theta_{s-1}) - C(theta_s)) plus a term that diverges unless lim C = 0.",
    title="Unified objective: minimize integral of C over time",
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_unified_derives_representation_hierarchy = claim(
    "The unified objective (maximization of uncertainty reduction rate) qualitatively derives "
    "the need for the projection parametrization Proj#P_f over plain P_f. Models in P_simple "
    "are strictly more likely to reach zero terminal loss than models in P_plain "
    "(since P_simple ⊃ P_HMM while P_plain does not contain P_HMM). Even when both reach zero, "
    "models in P_simple train faster due to smaller complexity norm ||P*||_{F,Proj} << ||P*||_F.",
    title="Unified objective derives representation hierarchy preference",
)

claim_unified_derives_sampler_efficiency = claim(
    "The unified objective qualitatively derives the need for efficient samplers. "
    "To maximize uncertainty reduction per unit time, each training step must be as fast as "
    "possible without sacrificing gradient quality. Monte-Carlo estimation reduces step time "
    "from superpolynomial (exact summation over all latent sequences) to practical O(n * |x|^2) "
    "with sampling size n. Approximating the optimal samplers (Q -> Q*, Q-tilde -> Q-tilde*) "
    "reduces gradient estimation error, improving the gain C(theta_{s-1}) - C(theta_s).",
    title="Unified objective derives sampler efficiency requirement",
)

claim_unified_derives_fast_slow_balance = claim(
    "The unified objective provides a principled way to balance fast and slow thinking. "
    "The optimal sampling frequency (how often to insert non-empty thoughts), thought length, "
    "sampling size n, and whether to use one or two samplers are all determined by optimizing "
    "the tradeoff between uncertainty reduction gain and computational time cost. "
    "This automatically recovers human-like flexible switching between fast and slow thinking.",
    title="Unified objective derives intrinsic balance of fast and slow thinking",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_unified_repr = support(
    [claim_psimple_contains_phmm, claim_projection_reduces_norm],
    claim_unified_derives_representation_hierarchy,
    reason=(
        "Under @uncertainty_reduction_objective_setting, the model must minimize C(theta) to zero "
        "as rapidly as possible. @claim_psimple_contains_phmm shows P_simple is a strictly larger "
        "subspace than P_plain, so for a randomly chosen P*, P_simple is more likely to contain it. "
        "@claim_projection_reduces_norm shows that even when both subspaces contain P*, the smaller "
        "norm in P_simple implies faster convergence via the training loss estimate KL ≲ ||P*||_F / t^a. "
        "Thus the unified objective rewards choosing the projection parametrization."
    ),
    prior=0.85,
    background=[uncertainty_reduction_objective_setting],
)

strat_unified_sampler = support(
    [claim_scaling_laws_chi2, claim_causal_samplers_inadequate],
    claim_unified_derives_sampler_efficiency,
    reason=(
        "Under @uncertainty_reduction_objective_setting, faster training steps reduce the integral. "
        "Monte-Carlo sampling reduces step time but introduces gradient estimation error. "
        "@claim_scaling_laws_chi2 shows this error scales as chi^2/n. @claim_causal_samplers_inadequate "
        "shows causal samplers maintain large chi^2, meaning many samples are needed to compensate. "
        "Approximating optimal samplers (explanatory Q*, inquisitive Q-tilde) reduces chi^2, "
        "allowing the same gradient quality with fewer samples n, reducing t_s."
    ),
    prior=0.85,
    background=[uncertainty_reduction_objective_setting],
)

strat_unified_balance = support(
    [claim_unified_derives_sampler_efficiency],
    claim_unified_derives_fast_slow_balance,
    reason=(
        "Under @uncertainty_reduction_objective_setting, every design choice is subject to a "
        "speed-accuracy tradeoff. For @claim_unified_derives_sampler_efficiency, sampling more "
        "(larger n) improves gradient quality but takes more time. Inserting longer thoughts "
        "increases expressivity but increases step time. The objective (62) treats these tradeoffs "
        "uniformly, and end-to-end optimization recovers the human-like property of thinking "
        "more slowly on harder inputs and faster on easier ones."
    ),
    prior=0.80,
    background=[uncertainty_reduction_objective_setting],
)

strat_uncertainty_derives_repr = deduction(
    [claim_unified_derives_representation_hierarchy, claim_unified_derives_sampler_efficiency],
    claim_uncertainty_reduction_objective,
    reason=(
        "The unified objective (62) in @uncertainty_reduction_objective_setting is the sole "
        "source from which both the representation hierarchy (via @claim_unified_derives_representation_hierarchy) "
        "and the sampler hierarchy (via @claim_unified_derives_sampler_efficiency) are derived. "
        "Since these two hierarchies constitute the static theory, the unified objective "
        "qualitatively derives the entire static theory from a single principle."
    ),
    prior=0.99,
    background=[uncertainty_reduction_objective_setting],
)
