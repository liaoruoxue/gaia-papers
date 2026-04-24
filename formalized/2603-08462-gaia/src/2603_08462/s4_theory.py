"""Section 4: Theoretical Analysis — Recovering Length Penalties as Special Cases"""

from gaia.lang import claim, setting, deduction, support

from .s3_methodology import (
    information_cost_def,
    combined_reward_def,
    cib_objective_def,
    rl_objective_formulation,
)
from .motivation import budget_forcing_heuristic

# --- Settings ---

uniform_prior_def = setting(
    "A uniform (maximum entropy) prior $Q$ over the vocabulary assigns equal probability to "
    "every token at every position: $Q(z_t|z_{<t}) = 1/|V|$ for all $t$, where $|V|$ is the "
    "vocabulary size. Under this prior, $-\\log Q(z_t|z_{<t}) = \\log|V|$ is a constant, "
    "so the information cost $C(Z) = |Z| \\cdot \\log|V|$ is proportional to trace length $|Z|$.",
    title="Uniform prior gives constant per-token cost",
)

laplace_prior_def = setting(
    "A Laplace prior over trace length is a distribution that peaks at a target length $L^*$ "
    "and decays exponentially with distance from it. Under such a prior, the log-probability "
    "$\\log Q_\\phi(Z)$ approximates $-\\lambda |\\,|Z| - L^*\\,|$ for some rate $\\lambda$, "
    "yielding a penalty proportional to the absolute deviation from target length.",
    title="Laplace prior gives target-length penalty",
)

# --- Theoretical claims (Propositions 4.1 and 4.2) ---

prop_length_penalty_equivalence = claim(
    "Proposition 4.1: A standard length-based penalty $g(Z) = \\alpha f(|Z|)$ (applied in "
    "existing Budget Forcing methods) is equivalent to the CIB minimality reward "
    "$r_{\\text{min}}(X,Z) = \\sum_t \\log Q_\\phi(z_t|z_{<t})$ under the special case where "
    "$Q_\\phi$ is a maximum entropy (uniform) prior over the vocabulary. Under this prior, "
    "$-\\log Q_\\phi(z_t|z_{<t}) = \\log|V|$ is constant per token, so $C(Z) \\propto |Z|$.",
    title="Proposition 4.1: Length penalties are CIB with uniform prior",
    background=[uniform_prior_def, information_cost_def],
    metadata={"source_section": "Section 4"},
)

strat_prop41 = deduction(
    [rl_objective_formulation],
    prop_length_penalty_equivalence,
    reason=(
        "Under the uniform prior (@uniform_prior_def), $-\\log Q(z_t|z_{<t}) = \\log|V|$ (constant) "
        "for all tokens. Substituting into the information cost definition (@information_cost_def): "
        "$C(Z) = \\sum_{t=1}^{|Z|} \\log|V| = |Z| \\cdot \\log|V|$, proportional to trace length $|Z|$. "
        "This is exactly the form of a standard length penalty $g(Z) = \\alpha|Z|$. "
        "The CIB minimality reward $r_{\\text{min}} = -C(Z)$ in @rl_objective_formulation "
        "therefore reduces to a length penalty when the prior is uniform."
    ),
    prior=0.98,
    background=[uniform_prior_def, information_cost_def],
)

prop_target_length_equivalence = claim(
    "Proposition 4.2: Target-length penalties, such as L1-Exact (LCPO-Exact) [@Aggarwal2025], "
    "which penalize deviation from a target length $L^*$, correspond to the CIB objective with "
    "a Laplace prior $Q_\\phi$ peaked at $L^*$. Under a Laplace prior, "
    "$\\log Q_\\phi(Z) \\approx -\\lambda ||Z| - L^*|$, matching the L1 penalty form.",
    title="Proposition 4.2: Target-length penalties are CIB with Laplace prior",
    background=[laplace_prior_def, information_cost_def],
    metadata={"source_section": "Section 4"},
)

strat_prop42 = deduction(
    [rl_objective_formulation],
    prop_target_length_equivalence,
    reason=(
        "Under the Laplace prior (@laplace_prior_def), the log-probability of a trace of length "
        "$|Z|$ is $\\log Q_\\phi(Z) \\approx -\\lambda||Z|-L^*|$. Substituting into the information "
        "cost definition (@information_cost_def) gives $C(Z) \\approx \\lambda||Z|-L^*|$, which is "
        "exactly the L1 penalty on deviation from target length $L^*$. The CIB framework in "
        "@rl_objective_formulation with Laplace prior thus recovers LCPO-Exact and L1-Exact."
    ),
    prior=0.98,
    background=[laplace_prior_def, information_cost_def],
)

cib_unifies_budget_forcing = claim(
    "The CIB framework unifies all budget-forcing methods as special cases: length penalties "
    "correspond to CIB with uniform priors (Proposition 4.1), and target-length penalties "
    "correspond to CIB with Laplace priors (Proposition 4.2). Semantic priors (from a real "
    "language model $Q_\\phi$) strictly generalize these, capturing token-level relevance "
    "that length-only metrics cannot.",
    title="CIB unifies budget forcing methods as special cases",
    metadata={"source_section": "Section 4"},
)

strat_cib_unifies = deduction(
    [prop_length_penalty_equivalence, prop_target_length_equivalence],
    cib_unifies_budget_forcing,
    reason=(
        "Since @prop_length_penalty_equivalence shows length penalties arise from uniform priors, "
        "and @prop_target_length_equivalence shows target-length penalties arise from Laplace "
        "priors, the CIB framework with a general language model prior strictly includes both "
        "as special cases. This provides the theoretical justification for why semantic priors "
        "should outperform length-only baselines: they use strictly more information about "
        "token identity and context."
    ),
    prior=0.97,
)

semantic_prior_superiority_theory = claim(
    "Because a real (non-uniform, non-Laplace) language model prior $Q_\\phi$ captures the "
    "contextual probability distribution over tokens, it can assign differential costs to tokens "
    "based on their semantic content — penalizing generic filler tokens (high probability under "
    "$Q_\\phi$, low surprisal) more than task-specific reasoning tokens (low probability under "
    "$Q_\\phi$, high surprisal). This theoretical advantage translates to better "
    "accuracy-efficiency trade-offs than uniform or Laplace priors.",
    title="Theoretical basis for semantic prior superiority over length priors",
    background=[information_cost_def],
    metadata={"source_section": "Section 4"},
)

strat_semantic_superiority = support(
    [cib_unifies_budget_forcing],
    semantic_prior_superiority_theory,
    reason=(
        "Since @cib_unifies_budget_forcing shows that length penalties are CIB with degenerate "
        "(uniform or Laplace) priors, any prior that is closer to the true token distribution "
        "will provide a strictly better estimate of semantic redundancy. A language model prior "
        "$Q_\\phi$ trained on natural language assigns probabilities that correlate with semantic "
        "content, enabling cost discrimination that length-only methods cannot achieve."
    ),
    prior=0.85,
)
