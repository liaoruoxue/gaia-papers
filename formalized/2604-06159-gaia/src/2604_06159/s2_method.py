"""Section 2: Target Policy Optimization -- the method.

Section 2 of [@Kaddour2026]. This module formalises the TPO method
itself: notation, the policy-over-the-group $p^\\theta$, the target
$q$ (Eq. 2), the cross-entropy loss (Eq. 3), the closed-form gradient
on group logits ($p^\\theta - q$), the KL-regularised interpretation
(Eq. 4), and Proposition 1 (existence/uniqueness of the target plus
the unique stationary distribution $p^\\theta = q$). Score
standardization is split into its own setting because it is *defined*
in Appendix A but *justified* with a separate argument ("Why
standardize") in Section 2.

The methodological claims here are the warrants for everything in
Sections 3-4: that gradient norms can self-extinguish (Sec. 4.1), that
multi-epoch reuse is stable (Sec. 4.3), and that within-context
allocation differs from PG/GRPO/DG (Sec. 3.2 derivation in App. B).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Notation and the policy-over-the-group
# ---------------------------------------------------------------------------

setup_logits_and_group_policy = setting(
    "**Notation: group logits and policy over the group.** For a "
    "context $x$ (a state or prompt), the agent samples $K$ "
    "candidates $y_1, \\ldots, y_K \\sim \\pi^{\\text{old}}(\\cdot \\mid x)$ "
    "and scores them with a scalar scorer $S$. Let $\\ell^\\theta_i = "
    "\\log \\pi_\\theta(y_i \\mid x)$ be the log-probability the current "
    "policy assigns to candidate $i$. The induced *policy over the "
    "group* is the softmax $p^\\theta_i = \\exp(\\ell^\\theta_i) / "
    "\\sum_{j=1}^K \\exp(\\ell^\\theta_j)$ (Eq. 1 of [@Kaddour2026]). "
    "Writing $p^{\\text{old}}_i$ for the same quantity under "
    "$\\pi^{\\text{old}}$ frozen at rollout time, $p^{\\text{old}}$ "
    "and $p^\\theta$ live on the $K$-simplex over the *sampled* "
    "candidates -- not the full action space.",
    title="Setup: $p^\\theta_i = \\mathrm{softmax}(\\ell^\\theta)_i$ on the sampled group",
)

setup_score_standardization = setting(
    "**Score standardization (Appendix A).** Given raw scores "
    "$s_1, \\ldots, s_K$, the standardized scores are $u_i = (s_i - "
    "\\bar{s}) / \\sigma(s)$ when $\\sigma(s) > 0$, and $u_i = 0$ for "
    "every coordinate when $\\sigma(s) = 0$, where $\\bar{s}$ and "
    "$\\sigma(s)$ are the within-group population mean and standard "
    "deviation (Eq. 5 of [@Kaddour2026]). The zero-variance convention "
    "$u = 0$ is a *definition*, not a claim; its consequences (e.g. "
    "the target $q = p^{\\text{old}}$ on all-fail groups, see Sec. "
    "4.2) are claims that depend on it.",
    title="Setup: $u_i = z\\text{-score}(s_i)$ with $u = 0$ when $\\sigma(s) = 0$",
)

setup_target_definition_eq2 = setting(
    "**Definition: the TPO target distribution.** With behavior "
    "probabilities $p^{\\text{old}}_i$ and standardized scores $u_i$, "
    "the TPO target is $q_i = p^{\\text{old}}_i \\exp(u_i / \\eta) / "
    "\\sum_{j=1}^K p^{\\text{old}}_j \\exp(u_j / \\eta)$ (Eq. 2), "
    "where $\\eta > 0$ is a temperature. The default value is $\\eta "
    "= 1$ throughout the paper. This is a *definition*; whether it "
    "actually solves the KL-regularised optimization in Eq. 4, and "
    "whether the cross-entropy gradient is $p^\\theta - q$, are "
    "claims (see `claim_prop1_target_unique` and "
    "`claim_prop1_gradient_p_minus_q`).",
    title="Setup: $q_i = p^{\\text{old}}_i \\exp(u_i/\\eta) / Z$ (Eq. 2)",
)

setup_loss_definition_eq3 = setting(
    "**Definition: the TPO cross-entropy loss.** TPO fits the policy "
    "to $q$ by minimising $L_{\\text{TPO}}(\\theta) = -\\sum_{i=1}^K "
    "q_i \\log p^\\theta_i$ (Eq. 3 of [@Kaddour2026]), treating $q$ "
    "as fixed (`stop_gradient` on $q$ in code, see Figure 2). On the "
    "first epoch on-policy, $p^\\theta = p^{\\text{old}}$ at rollout "
    "time; if rollouts are reused for additional epochs, $q$ stays "
    "frozen while $\\log p^\\theta$ is recomputed under the updated "
    "$\\theta$.",
    title="Setup: $L_{\\text{TPO}} = -\\sum_i q_i \\log p^\\theta_i$ (Eq. 3)",
)

setup_kl_objective_eq4 = setting(
    "**Definition: the KL-regularised improvement objective on the "
    "candidate simplex.** Eq. 4 of [@Kaddour2026] defines the "
    "constrained optimization $q = \\arg\\max_{r \\in \\Delta_{K-1}} "
    "\\{\\sum_i r_i u_i - \\eta \\, \\mathrm{KL}(r \\| p^{\\text{old}})\\}$ "
    "over the $K$-simplex of distributions on the *sampled* "
    "candidates. This is a definition of an optimization problem; the "
    "*claim* that the closed-form solution is exactly Eq. 2 is "
    "Proposition 1 (`claim_prop1_target_unique`).",
    title="Setup: KL-regularised tilt objective (Eq. 4)",
)

# ---------------------------------------------------------------------------
# Method-level claims (Proposition 1 and its consequences)
# ---------------------------------------------------------------------------

claim_prop1_target_unique = claim(
    "**Proposition 1, part 1: closed-form unique target.** Assuming "
    "$p^{\\text{old}}_i > 0$ for every sampled candidate, the target "
    "in Eq. 2 is the *unique* maximizer of the KL-regularised "
    "objective in Eq. 4 over the $K$-simplex. The proof is one line "
    "of Lagrangian calculus on a strictly concave objective: "
    "$-\\mathrm{KL}(r \\| p^{\\text{old}})$ is strictly concave on "
    "the simplex when $p^{\\text{old}}$ has full support, the "
    "Lagrangian KKT conditions yield $r_i = C \\, p^{\\text{old}}_i "
    "\\exp(u_i / \\eta)$, and the simplex constraint fixes $C$ "
    "[@Kaddour2026, Proposition 1].",
    title="Prop 1.1: $q$ in Eq. 2 is the unique maximiser of Eq. 4",
)

claim_prop1_gradient_p_minus_q = claim(
    "**Proposition 1, part 2: gradient on group logits is $p^\\theta - "
    "q$.** Treating $q$ as fixed (stop-gradient), the gradient of the "
    "softmax cross-entropy in Eq. 3 with respect to the group logits "
    "$\\ell^\\theta_i$ is $\\partial L / \\partial \\ell^\\theta_i = "
    "p^\\theta_i - q_i$. This follows from the standard softmax "
    "cross-entropy derivative and is a deduction from the loss "
    "definition (Eq. 3) plus the policy-over-the-group definition "
    "(Eq. 1) [@Kaddour2026, Proposition 1].",
    title="Prop 1.2: $\\nabla_{\\ell^\\theta} L_{\\text{TPO}} = p^\\theta - q$",
)

claim_prop1_unique_stationary = claim(
    "**Proposition 1, part 3: unique stationary distribution is "
    "$p^\\theta = q$.** Combining the gradient $p^\\theta - q$ with "
    "the existence/uniqueness of $q$ from Eq. 2, the unique "
    "stationary distribution over the *sampled* candidates is "
    "$p^\\theta = q$. In particular, gradient descent on $L_{\\text{TPO}}$ "
    "moves the group policy in direction $q - p^\\theta$ and the "
    "update vanishes exactly when the policy already matches the "
    "target [@Kaddour2026, Proposition 1].",
    title="Prop 1.3: gradient vanishes iff $p^\\theta = q$",
)

claim_standardization_invariance = claim(
    "**Standardization makes the update invariant to score scale.** "
    "Eq. 2 exponentiates the scores, so groups with the same ranking "
    "but different numerical spread would otherwise produce very "
    "different targets: e.g. raw scores $(1, 0, -1)$ yield a gentle "
    "tilt while $(100, 0, -100)$ make the target nearly deterministic. "
    "Standardization makes the update depend on relative within-group "
    "performance rather than arbitrary score units, and *largely "
    "removes the need to tune $\\eta$* (the temperature ablation in "
    "Appendix D shows performance is robust over $\\eta \\in [0.25, "
    "2]$, with only $\\eta = 4$ degrading meaningfully).",
    title="Method: z-scoring makes TPO scale-invariant and removes need to tune $\\eta$",
)

claim_tpo_no_critic_no_dual = claim(
    "**TPO requires no critic and no inner optimization.** Because "
    "the target $q$ in Eq. 2 lives on the $K$-simplex over the "
    "*sampled* candidates -- not the full action space -- the "
    "exponential-tilting solution is available *in closed form* from "
    "the standardized scores and the rollout snapshot probabilities "
    "alone. This contrasts with REPS [@Peters2010REPS], MPO "
    "[@Abdolmaleki2018MPO], and V-MPO [@Song2020VMPO], which apply "
    "the same exponential tilt but require a learned $Q$-function or "
    "value estimate to supply the improvement signal and a "
    "constrained optimization over the action space.",
    title="Method: closed-form $q$, no critic, no dual loop",
)

claim_gradient_self_extinguishes = claim(
    "**TPO's gradient self-extinguishes at the target.** Combining "
    "Proposition 1.2 ($\\nabla_{\\ell^\\theta} L_{\\text{TPO}} = "
    "p^\\theta - q$) with Proposition 1.3 (unique stationary point "
    "$p^\\theta = q$), the gradient norm goes to zero as the policy "
    "converges to the target. PG-family losses do not share this "
    "fixed-point property: they keep producing non-zero gradients "
    "from any group with non-zero advantage variance, even after "
    "training has plateaued. This 'self-extinguishing' property is "
    "the structural mechanism behind the empirical observation in "
    "Sec. 4.1 (Figure 11(a)) that TPO's gradient norm collapses near "
    "zero while GRPO's persists.",
    title="Method: self-extinguishing gradient as a structural property",
)

claim_q_fixed_supports_multi_epoch = claim(
    "**Frozen target $q$ supports stable multi-epoch reuse.** When "
    "rollouts are reused for additional optimization epochs, $q$ "
    "stays frozen (computed once from the rollout-time $p^{\\text{old}}$ "
    "and $u$) while $\\log p^\\theta$ is recomputed under the updated "
    "$\\theta$. Because $q$ does not move, multi-epoch TPO is "
    "minimising a *fixed* cross-entropy objective, which is a stable "
    "supervised problem. Methods like DG [@Osband2026] that lack such "
    "an explicit anchor are sensitive to the number of optimization "
    "epochs (see Sec. 4.3 and Appendix E).",
    title="Method: frozen $q$ -> multi-epoch is supervised, hence stable",
)

claim_token_level_grouping = claim(
    "**Token-level grouping for autoregressive sequence models.** For "
    "autoregressive policies with dense per-token reward, the same "
    "TPO machinery applies at each prefix state: sample $K$ "
    "next-token candidates per prefix, standardize their per-token "
    "scores within the group, and form the target $q$ over the "
    "$K$-token simplex. The variant TPO$_{\\text{token}}$ is used in "
    "Sections 3.4-3.5 (token-level grouping with $K=8$); the "
    "sequence-level variant samples $K$ full rollouts per prompt and "
    "is used in Sections 3.6-3.8 when only terminal reward is "
    "available.",
    title="Method: token-level vs. sequence-level grouping",
)

__all__ = [
    "setup_logits_and_group_policy",
    "setup_score_standardization",
    "setup_target_definition_eq2",
    "setup_loss_definition_eq3",
    "setup_kl_objective_eq4",
    "claim_prop1_target_unique",
    "claim_prop1_gradient_p_minus_q",
    "claim_prop1_unique_stationary",
    "claim_standardization_invariance",
    "claim_tpo_no_critic_no_dual",
    "claim_gradient_self_extinguishes",
    "claim_q_fixed_supports_multi_epoch",
    "claim_token_level_grouping",
]
