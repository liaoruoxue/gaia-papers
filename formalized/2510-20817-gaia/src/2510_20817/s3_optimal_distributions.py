"""Section 3: KL-Regularized Reward Maximization — Optimal Solution Distributions"""

from gaia.lang import claim, setting, question, support, deduction, infer

from .motivation import (
    kl_rl_objective,
    reverse_kl_def,
    forward_kl_def,
    flexible_family_def,
    multimodal_def,
    empirical_diversity_collapse,
)

# ── Settings ───────────────────────────────────────────────────────────────────

reverse_kl_obj_def = setting(
    "The reverse-KL regularized RL objective is: "
    "$J_\\beta(\\pi_\\theta) = \\mathbb{E}_{\\pi_\\theta(y)}[R(y)] - \\beta D_{KL}(\\pi_\\theta \\| \\pi_{\\text{ref}})$. "
    "This is the most common KL-regularized policy gradient objective used in practice "
    "(e.g., RLHF, DPO, GRPO variants).",
    title="Reverse-KL regularized RL objective",
)

forward_kl_obj_def = setting(
    "The forward-KL regularized RL objective is: "
    "$J_{\\text{fwd}}(\\pi_\\theta) = \\mathbb{E}_{\\pi_\\theta(y)}[R(y)] - \\beta D_{KL}(\\pi_{\\text{ref}} \\| \\pi_\\theta)$. "
    "Some recent works use this explicitly (motivated by 'mass covering'); "
    "others (e.g., GRPO) may estimate the forward KL incidentally while intending reverse KL.",
    title="Forward-KL regularized RL objective",
)

gateaux_variational_method = setting(
    "The optimal distribution is found by functional optimization: "
    "taking the Gateaux derivative of the Lagrangian objective "
    "(reward maximization subject to the normalization constraint $\\int \\pi(y) dy = 1$) "
    "and applying the fundamental lemma of calculus of variations "
    "(Gelfand & Fomin, 1963) to find the critical point.",
    title="Variational calculus method for optimal distribution",
)

# ── Core theoretical claims ────────────────────────────────────────────────────

reverse_kl_optimal_dist = claim(
    "The optimal solution to the reverse-KL regularized reward maximization problem "
    "$\\arg\\max_{\\pi_\\theta} J_\\beta(\\pi_\\theta)$ is the Gibbs distribution "
    "$G_\\beta(y) = \\frac{1}{\\zeta} \\pi_{\\text{ref}}(y) \\exp\\left(\\frac{R(y)}{\\beta}\\right)$, "
    "where $\\zeta = \\int \\pi_{\\text{ref}}(y) \\exp(R(y)/\\beta) \\, dy$ is the normalizing constant. "
    "This is well-known in prior work (Korbak et al., 2022; Rafailov et al., 2023; Zhang & Ranganath, 2025).",
    title="Optimal distribution for reverse-KL RL (Remark 3.1)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 3.1, Eq. (2)"},
)

reverse_kl_gradient_is_kl_toward_target = claim(
    "Maximizing the reverse-KL regularized RL objective $J_\\beta$ (Eq. 1) is equivalent to "
    "minimizing the reverse KL divergence $D_{KL}(\\pi_\\theta \\| G_\\beta)$ toward the target distribution $G_\\beta$. "
    "Formally: $\\nabla_\\theta D_{KL}(\\pi_\\theta \\| G_\\beta) \\propto -\\nabla_\\theta J_\\beta(\\pi_\\theta)$. "
    "This means gradient ascent on $J_\\beta$ performs distribution matching toward $G_\\beta$ via reverse KL.",
    title="Reverse-KL RL gradient is distribution matching toward G_beta (Remark 3.2)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 3.1, Eq. (3)"},
)

forward_kl_optimal_dist = claim(
    "Under the assumption that $\\beta > 0$, rewards are finite ($R_{\\max} < \\infty$), "
    "and at least one on-support answer achieves $R(y) = R_{\\max}$ with $\\pi_{\\text{ref}}(y) > 0$, "
    "the optimal solution to the forward-KL regularized reward maximization problem is: "
    "$G_{\\text{fwd}}(y) = \\frac{\\beta \\pi_{\\text{ref}}(y)}{\\Lambda - R(y)}$, "
    "where $\\Lambda > \\max_y R(y)$ is the unique Lagrange multiplier ensuring $G_{\\text{fwd}}$ "
    "integrates to 1. This distribution does not have a closed-form expression for $\\Lambda$. "
    "It is a completely different distribution family from the reverse-KL optimal $G_\\beta$.",
    title="Optimal distribution for forward-KL RL (Remark 3.3)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 3.2, Eq. (5)"},
)

forward_kl_gradient_not_forward_kl = claim(
    "The gradient of the forward-KL regularized RL objective $J_{\\text{fwd}}$ "
    "is NOT a forward KL divergence gradient toward any target distribution $h$ "
    "that is defined independently of $\\pi_\\theta$. "
    "Formally, there is no $h$ independent of $\\pi_\\theta$ such that "
    "$\\nabla_\\theta D_{KL}(h \\| \\pi_\\theta) \\propto -\\nabla_\\theta J_{\\text{fwd}}(\\pi_\\theta)$. "
    "Therefore, optimizing $J_{\\text{fwd}}$ cannot be naively equated to 'forward KL optimization' "
    "with its associated intuitions.",
    title="Forward-KL RL gradient is not a forward KL gradient (Remark 3.4)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 3.2, Eq. (6); Appendix B.4"},
)

both_kl_can_multimodal = claim(
    "Both the reverse-KL optimal distribution $G_\\beta$ (Eq. 2) and the forward-KL optimal "
    "distribution $G_{\\text{fwd}}$ (Eq. 5) can be multimodal for appropriate choices of the "
    "regularization coefficient $\\beta$. "
    "Given the same bimodal reward function and reference policy, optimizing with either KL variant "
    "produces solution distributions ranging from unimodal (small $\\beta$) to multimodal "
    "(larger $\\beta$), as shown in Figure 2 of the paper.",
    title="Both KL regularizations can yield multimodal solutions (Section 3.3)",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 2"},
)

forward_kl_off_support = claim(
    "When the forward-KL regularized optimal distribution $G_{\\text{fwd}}$ is used, "
    "if the highest-reward answers exist OUTSIDE the support of $\\pi_{\\text{ref}}$ "
    "(i.e., $R^{\\text{out}}_{\\max} > R^{\\text{in}}_{\\max}$), "
    "then $G_{\\text{fwd}}$ places nonzero probability mass in regions where $\\pi_{\\text{ref}}(y) = 0$. "
    "In this case $G_{\\text{fwd}}$ has no preference among the off-support high-reward samples in terms of density. "
    "If the on-support distribution normalizes to $Z(R^{\\text{out}}_{\\max}) \\geq 1$, "
    "no off-support mass is placed.",
    title="Forward-KL can place mass off reference support (Appendix B.3)",
    metadata={"source": "artifacts/2510.20817.pdf, Appendix B.3"},
)

forward_kl_gradient_is_mle = claim(
    "The gradient of the forward KL divergence $D_{KL}(G_\\beta \\| \\pi_\\theta)$ "
    "equals $-\\mathbb{E}_{G_\\beta}[\\nabla_\\theta \\log \\pi_\\theta(y)]$, "
    "which corresponds to maximum likelihood estimation (supervised fine-tuning) "
    "on trajectories sampled from the target distribution $G_\\beta$. "
    "This is generally intractable because it requires sampling from $G_\\beta$. "
    "Algorithms like STaR and RAFT can be interpreted as approximating this via filtering high-reward trajectories.",
    title="Forward KL gradient is maximum likelihood on G_beta samples (Remark B.2)",
    metadata={"source": "artifacts/2510.20817.pdf, Appendix B.5"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_rev_kl_opt = support(
    [empirical_diversity_collapse],
    reverse_kl_optimal_dist,
    reason=(
        "To understand why @empirical_diversity_collapse occurs, the paper derives the optimal distribution "
        "of reverse-KL regularized RL via functional optimization (Appendix B.1, Eq. 14-18): "
        "write the reverse-KL objective $J_\\beta(\\pi_\\theta)$ as "
        "$-(\\beta+\\eta)D_{KL}(\\pi_\\theta \\| G_{\\beta,\\eta}) + \\text{const}$, "
        "which shows $J_\\beta$ is maximized when $D_{KL}(\\pi_\\theta \\| G_\\beta) = 0$. "
        "The Gibbs form $G_\\beta(y) \\propto \\pi_{\\text{ref}}(y) \\exp(R(y)/\\beta)$ "
        "is the unique maximizer (Appendix B.1). "
        "This derivation is algebraically exact.",
    ),
    prior=0.99,
    background=[gateaux_variational_method, reverse_kl_obj_def, kl_rl_objective],
)

strat_rev_kl_grad = deduction(
    [reverse_kl_optimal_dist],
    reverse_kl_gradient_is_kl_toward_target,
    reason=(
        "From Appendix B.1, the identity "
        "$-\\frac{1}{\\beta} J_\\beta(\\pi_\\theta) = D_{KL}(\\pi_\\theta \\| G_\\beta) - \\log \\zeta$ "
        "follows algebraically from the definition of $G_\\beta$ (@reverse_kl_optimal_dist). "
        "Taking gradients: $\\nabla_\\theta(-\\frac{1}{\\beta} J_\\beta) = \\nabla_\\theta D_{KL}(\\pi_\\theta \\| G_\\beta)$. "
        "Therefore $\\nabla_\\theta J_\\beta = -\\beta \\nabla_\\theta D_{KL}(\\pi_\\theta \\| G_\\beta)$, "
        "showing gradient ascent on $J_\\beta$ is exactly reverse-KL minimization toward $G_\\beta$.",
    ),
    prior=0.99,
    background=[gateaux_variational_method],
)

strat_fwd_kl_opt = support(
    [empirical_diversity_collapse],
    forward_kl_optimal_dist,
    reason=(
        "To explain @empirical_diversity_collapse under forward-KL regularization, "
        "the optimal distribution $G_{\\text{fwd}}$ is derived via the Gateaux derivative of the Lagrangian "
        "(Appendix B.3, Eq. 33-43) using @gateaux_variational_method. "
        "Setting the functional derivative to zero and solving, subject to $\\pi(y) > 0$ on $\\text{supp}(\\pi_{\\text{ref}})$, "
        "yields $\\pi^*(y) = \\beta \\pi_{\\text{ref}}(y) / (\\Lambda - R(y))$ where $\\Lambda > R_{\\max}$. "
        "The uniqueness of $\\Lambda$ follows from the continuity and monotonicity of "
        "$Z(\\Lambda) = \\int \\beta\\pi_{\\text{ref}}(y)/(\\Lambda - R(y)) dy$ as $\\Lambda$ varies from $R_{\\max}$ to $\\infty$. "
        "This derivation is exact (Appendix B.3 proof) given finite rewards and on-support maximizers.",
    ),
    prior=0.99,
    background=[gateaux_variational_method, forward_kl_obj_def, kl_rl_objective],
)

strat_fwd_kl_not_grad = support(
    [forward_kl_optimal_dist],
    forward_kl_gradient_not_forward_kl,
    reason=(
        "Given @forward_kl_optimal_dist, proof by contradiction (Appendix B.4): "
        "Suppose there exists a target $h$ independent of $\\pi_\\theta$ "
        "such that the gradient of the forward-KL objective is proportional to the gradient of $D_{KL}(h\\|\\pi_\\theta)$. "
        "The functional derivative of $J_{\\text{fwd}}$ is $R(y) + \\beta \\pi_{\\text{ref}}(y)/\\pi(y) + \\lambda$ (Eq. 40, 50). "
        "The functional derivative of $D_{KL}(h\\|\\pi)$ is $\\lambda' - h(y)/\\pi(y)$ (Eq. 57). "
        "Setting these proportional and solving for $h(y)$ yields "
        "$h(y) = (\\lambda' - \\alpha\\lambda - \\alpha R(y))\\pi(y) - \\alpha\\beta\\pi_{\\text{ref}}(y)$, "
        "which depends on $\\pi(y)$ for non-constant $R$. "
        "Hence no $h$ independent of $\\pi_\\theta$ exists.",
    ),
    prior=0.99,
    background=[gateaux_variational_method, forward_kl_obj_def],
)

strat_both_multimodal = support(
    [reverse_kl_optimal_dist, forward_kl_optimal_dist],
    both_kl_can_multimodal,
    reason=(
        "From the closed-form expressions for $G_\\beta$ (@reverse_kl_optimal_dist) "
        "and $G_{\\text{fwd}}$ (@forward_kl_optimal_dist), "
        "at sufficiently large $\\beta$ the regularization term dominates, "
        "forcing the policy to remain close to $\\pi_{\\text{ref}}$ everywhere, "
        "including at all high-reward modes. "
        "Figure 2 of the paper empirically demonstrates this: "
        "given a bimodal reward function, both KL variants produce multimodal policies at higher $\\beta$ values. "
        "The specific crossover $\\beta$ is predicted by the probability ratio analysis (Remark 4.4).",
    ),
    prior=0.9,
    background=[multimodal_def],
)
