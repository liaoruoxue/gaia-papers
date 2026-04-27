"""Section 5: Self-consistent learning (Theorem 5.1: posterior consistency)."""

from gaia.lang import claim, setting, support, deduction
from .motivation import (
    setup_aif,
    claim_pragmatic_curiosity_acquisition,
    claim_low_curiosity_is_myopic,
)
from .s4_definitions import (
    def_posterior_consistency,
    def_potential_energy,
)

# --- Setup specific to Theorem 5.1 ---

setup_discrete_latent = setting(
    "**Theorem 5.1 setup.** The latent parameter $s$ takes values in a discrete "
    "space $\\mathcal{S}$, with true (data-generating) value $s^*\\in\\mathcal{S}$. "
    "At each iteration $t$, the query $x_t$ is selected by the AIF policy:\n\n"
    "$$x_t = \\arg\\max_{x\\in\\mathcal{X}}"
    "\\bigl\\{\\beta_t\\, I(s;(x,y)|D_{t-1}) - "
    "\\mathbb{E}_{p(y|x,D_{t-1})}[h_t(y)]\\bigr\\},$$\n\n"
    "where $I(s;(x,y)|D_{t-1})$ is the conditional mutual information between $s$ "
    "and the next observation pair, and $h_t(y)$ is the (non-negative) potential "
    "energy function at time $t$.",
    title="Theorem 5.1 setup: discrete latent space and AIF policy",
)

setup_observation_gap = setting(
    "**Per-hypothesis observation gap.** For each $s\\neq s^*$, define\n\n"
    "$$\\Delta_s(x_t) := \\int_y p(y|x_t, s)\\,h_t(y)\\,dy - "
    "\\int_y p(y|x_t, s^*)\\,h_t(y)\\,dy,$$\n\n"
    "the difference in expected energy between hypothesis $s$ and the truth $s^*$ "
    "at action $x_t$. This quantifies how much $h_t$ separates $s$ from $s^*$ "
    "via the observation distribution.",
    title="Per-hypothesis observation gap",
)

# --- Three assumptions of Theorem 5.1 (each is a claim, since they constrain reality) ---

claim_assum_finite_prior_entropy = claim(
    "**Assumption (i): Finite prior entropy.** The prior $q_0(s)$ has finite "
    "Shannon entropy, $H_0 := H(q_0(s)) < \\infty$. This means the agent begins "
    "with a well-posed inferential task: initial uncertainty over $\\mathcal{S}$ "
    "is bounded.",
    title="Assumption (i): finite prior entropy",
)

claim_assum_distinguishability = claim(
    "**Assumption (ii): Observational distinguishability.** Under the observation "
    "constraint induced by $h_t(y)$, the true parameter $s^*$ is distinguishable "
    "in the sense that\n\n"
    "$$\\frac{\\sum_{s\\neq s^*}\\Delta_s(x_t)\\,q_{t-1}(s)}"
    "{\\sum_{s\\neq s^*}q_{t-1}(s)} \\geq A_t,$$\n\n"
    "with $A_t \\geq 0$ quantifying the average discriminative strength of the "
    "current observation. If $h_t$ excessively filters the signal (e.g., focuses "
    "only on narrow outcomes), $A_t$ can collapse and the system may fail to "
    "identify $s^*$.",
    title="Assumption (ii): observational distinguishability",
)

claim_assum_sufficient_curiosity_5 = claim(
    "**Assumption (iii): Sufficient curiosity (for consistency).** The curiosity "
    "coefficient satisfies\n\n"
    "$$\\beta_t \\;\\geq\\; \\min_{x\\in\\mathcal{X}} "
    "\\frac{\\mathbb{E}_{p(y|x,D_{t-1})}[h_t(y)]}{I(s;(x,y)|D_{t-1})},$$\n\n"
    "which ensures that the value of information cannot be suppressed by the "
    "expected regret penalty.",
    title="Assumption (iii): sufficient curiosity (Eq. 5)",
)

# --- The theorem statement (a derived claim) ---

claim_theorem_5_1 = claim(
    "**Theorem 5.1 (Posterior Consistency in AIF).** Under assumptions (i)-(iii) "
    "above, define $w_t := \\sum_{s\\neq s^*} q_{t-1}(s)$ as the total posterior "
    "mass on incorrect hypotheses. Then it suffices to run for\n\n"
    "$$T \\;\\geq\\; \\frac{\\bar\\beta_T\\, H_0}{\\underline{A}_T\\,\\epsilon}$$\n\n"
    "iterations to obtain $\\mathbb{E}[w_T]\\leq \\epsilon$, where "
    "$\\underline{A}_T := \\min_{t\\in[1,T]} A_t$ and "
    "$\\bar\\beta_T := \\max_{t\\in[1,T]}\\beta_t$. Proof: see Appendix A.",
    title="Theorem 5.1 statement: sample-complexity bound for posterior consistency",
)

# --- Proof of Theorem 5.1 (rigorous mathematical derivation -> deduction) ---
#
# The proof in Appendix A is a clean chain of equalities/inequalities under the
# stated assumptions; it is mathematically rigorous, so deduction is appropriate.

ded_theorem_5_1 = deduction(
    [
        claim_assum_finite_prior_entropy,
        claim_assum_distinguishability,
        claim_assum_sufficient_curiosity_5,
    ],
    claim_theorem_5_1,
    background=[
        setup_aif,
        setup_discrete_latent,
        setup_observation_gap,
        def_posterior_consistency,
        def_potential_energy,
        claim_pragmatic_curiosity_acquisition,
    ],
    reason=(
        "Appendix A proof. Under the AIF policy (@setup_discrete_latent), "
        "assumption (iii) (@claim_assum_sufficient_curiosity_5) gives "
        "$\\max_x\\{\\beta_t I - \\mathbb{E}[h_t]\\}\\geq 0$, so for the chosen "
        "$x_t$ we have $\\beta_t I(s;(x_t,y_t)|D_{t-1}) \\geq "
        "\\mathbb{E}[h_t(y_t)]$. Defining the instant regret of expected "
        "observation $r_t := \\mathbb{E}[h_t(y_t)] - \\int p(y|x_t,s^*)h_t(y)\\,dy$ "
        "and using $h_t \\geq 0$ (@def_potential_energy), one obtains "
        "$I(s;(x_t,y_t)|D_{t-1}) \\geq r_t/\\bar\\beta_T$. "
        "Telescoping mutual information gives "
        "$\\sum_{t=1}^T \\mathbb{E}[I_t] = \\mathbb{E}[H(q_0)-H(q_T)] \\leq H_0 < \\infty$ "
        "by @claim_assum_finite_prior_entropy. Algebraic expansion of $r_t$ over "
        "$s\\neq s^*$ rewrites it as "
        "$r_t = \\sum_{s\\neq s^*}\\Delta_s(x_t)\\,q_{t-1}(s)$ "
        "(@setup_observation_gap), and assumption (ii) "
        "(@claim_assum_distinguishability) bounds this below by $A_t w_t$, hence "
        "$w_t \\leq r_t/\\underline{A}_T$. Combining yields "
        "$\\sum_{t=1}^T \\mathbb{E}[w_t] \\leq \\bar\\beta_T H_0/\\underline{A}_T$, "
        "so by Markov-style averaging at least one $t$ satisfies "
        "$\\mathbb{E}[w_t]\\leq \\bar\\beta_T H_0/(\\underline{A}_T T)$, giving "
        "the sample-complexity bound. The derivation is purely algebraic given "
        "the three assumptions, so deduction (rather than support) is appropriate. "
        "The derivation also directly contradicts the myopic-exploitation failure "
        "mode @claim_low_curiosity_is_myopic when $\\beta_t$ is at the boundary."
    ),
    prior=0.99,
)

# --- Interpretations of the assumptions and convergence rate (claims) ---

claim_interp_finite_entropy = claim(
    "**Interpretation of assumption (i).** Finite prior entropy ensures that the "
    "parameter space is *learnable*: the initial uncertainty is bounded, meaning "
    "the agent begins with a well-posed inferential task. Without bounded $H_0$ "
    "(e.g., a continuum of equally weighted hypotheses), no finite number of "
    "queries can drive the expected error mass to a target $\\epsilon$.",
    title="Interpretation: finite prior entropy guarantees learnability",
)

claim_interp_distinguishability = claim(
    "**Interpretation of assumption (ii).** Observational distinguishability "
    "guarantees that, under the observation model constrained by $h_t(y)$, the "
    "true parameter generates statistically distinguishable outcomes from other "
    "hypotheses. The condition explicitly couples the *informativeness of "
    "experiments* with the *expressivity of the energy function*: if $h_t(y)$ "
    "excessively filters the signal, the system may fail to identify $s^*$.",
    title="Interpretation: distinguishability couples informativeness and energy",
)

claim_interp_sufficient_curiosity_5 = claim(
    "**Interpretation of assumption (iii).** Sufficient curiosity enforces that "
    "the epistemic term dominates enough to prevent premature exploitation. When "
    "$\\beta_t$ falls below this threshold, the policy may repeatedly select "
    "myopic actions that yield low expected regret but fail to reduce parameter "
    "uncertainty, breaking the consistency guarantee.",
    title="Interpretation: sufficient curiosity prevents premature exploitation",
)

# These three "interpretations" follow from reading the bound and the role of
# each quantity in it. They are derived (supported by the theorem and assumption
# definitions). Use support (not deduction) since the move from the formula to
# the qualitative interpretation involves judgment, not strict entailment.

support_interp_h0 = support(
    [claim_theorem_5_1, claim_assum_finite_prior_entropy],
    claim_interp_finite_entropy,
    reason=(
        "The bound $T \\geq \\bar\\beta_T H_0 / (\\underline{A}_T \\epsilon)$ "
        "in @claim_theorem_5_1 has $H_0$ in the numerator: when $H_0$ "
        "(@claim_assum_finite_prior_entropy) is large, more iterations are needed "
        "to reach the same $\\epsilon$. Finiteness of $H_0$ is what makes the "
        "right-hand side finite, hence learnability is the practical content."
    ),
    prior=0.95,
)

support_interp_AT = support(
    [claim_theorem_5_1, claim_assum_distinguishability],
    claim_interp_distinguishability,
    reason=(
        "$\\underline{A}_T$ appears in the denominator of the sample-complexity "
        "bound (@claim_theorem_5_1). Since $A_t$ is computed using $h_t$ via the "
        "per-hypothesis observation gap, an $h_t$ that suppresses the signal "
        "drives $\\underline{A}_T \\to 0$ and the bound becomes vacuous "
        "(@claim_assum_distinguishability)."
    ),
    prior=0.95,
)

support_interp_beta_5 = support(
    [claim_theorem_5_1, claim_assum_sufficient_curiosity_5, claim_low_curiosity_is_myopic],
    claim_interp_sufficient_curiosity_5,
    reason=(
        "@claim_assum_sufficient_curiosity_5 is the binding floor under which "
        "the proof of @claim_theorem_5_1 fails: the inequality "
        "$\\beta_t I(s;(x_t,y_t)|D_{t-1}) \\geq \\mathbb{E}[h_t(y_t)]$ ceases to "
        "hold, the agent picks myopic-but-uninformative queries, and "
        "@claim_low_curiosity_is_myopic materializes."
    ),
    prior=0.95,
)

# --- Convergence-rate interpretation (the three drivers) ---

claim_rate_dependencies = claim(
    "**Convergence-rate interpretation.** Required iterations to reach "
    "$\\mathbb{E}[w_T] \\leq \\epsilon$ depend on three quantities:\n\n"
    "- $H_0$ (initial uncertainty): larger priors require more evidence to "
    "concentrate.\n"
    "- $\\underline{A}_T$ (minimum discriminative power of queries): experiments "
    "yielding greater inter-hypothesis differences accelerate convergence.\n"
    "- $\\bar\\beta_T$ (curiosity upper bound): higher curiosity encourages "
    "richer sampling but may slow concentration, since resources are devoted to "
    "wide exploration rather than focused identification.",
    title="Theorem 5.1 convergence rate: three drivers",
)

ded_rate_interpretation = deduction(
    [claim_theorem_5_1],
    claim_rate_dependencies,
    reason=(
        "Direct reading of the closed-form bound in @claim_theorem_5_1: $H_0$ "
        "and $\\bar\\beta_T$ in the numerator, $\\underline{A}_T$ in the "
        "denominator, $\\epsilon$ in the denominator (so smaller target requires "
        "more iterations). The sign of each dependency is purely algebraic."
    ),
    prior=0.99,
)

