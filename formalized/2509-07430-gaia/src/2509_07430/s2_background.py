"""Section 2: Background — Standard RLVR Objectives and Their Limitations"""

from gaia.lang import claim, setting

from .motivation import (
    rlvr_setting,
    pass_at_k_setting,
    reverse_kl_setting,
    f_divergence_setting,
    passk_degrades,
    catastrophic_forgetting,
)

# ── Settings ──────────────────────────────────────────────────────────────────

grpo_objective = setting(
    "The Group Relative Policy Optimization (GRPO) objective maximizes expected reward "
    "without a KL-divergence constraint: "
    "$\\max_{\\pi_\\theta} \\mathbb{E}_{q \\sim \\mathcal{D}}[\\mathbb{E}_{a \\sim \\pi_\\theta(\\cdot|q)}[r(a|q)]]$. "
    "It uses group-normalized advantages (relative to other samples in the same batch) "
    "instead of a value baseline. GRPO applies clip-based PPO updates with group "
    "normalization but no explicit divergence regularization term.",
    title="GRPO objective (definition)",
)

dapo_objective = setting(
    "DAPO (Decoupled Clip and Dynamic sAmpling Policy Optimization) extends GRPO with "
    "dynamic sampling and decoupled clip ratios for better training stability. Like GRPO, "
    "it does not include a divergence penalty against the reference (initial) policy. "
    "DAPO removes entropy-based KL terms entirely.",
    title="DAPO objective (definition)",
)

ppo_objective = setting(
    "The Proximal Policy Optimization (PPO) objective uses a clipped surrogate loss with "
    "reverse-KL divergence penalty: "
    "$\\max_{\\pi_\\theta} \\mathbb{E}[\\hat{A}_t \\cdot \\min(\\rho_t, \\text{clip}(\\rho_t, 1-\\varepsilon, 1+\\varepsilon))] "
    "- \\beta D_{KL}(\\pi_\\theta \\| \\pi_{ref})$, "
    "where $\\rho_t = \\pi_\\theta(a_t|s_t)/\\pi_{old}(a_t|s_t)$ is the probability ratio "
    "and $\\hat{A}_t$ is the advantage estimate.",
    title="PPO with reverse-KL (definition)",
)

trpo_bound = setting(
    "The Trust Region Policy Optimization (TRPO) monotonic improvement theorem states that "
    "for any policy $\\pi$ and old policy $\\pi_{old}$, the true objective satisfies: "
    "$J(\\pi) - L_{\\pi_{old}}(\\pi) \\geq -\\frac{2\\gamma \\alpha_1 \\varepsilon_\\pi}{(1-\\gamma)^2}$, "
    "where $\\alpha_1 = \\max_s D_{KL}(\\pi(\\cdot|s) \\| \\pi_{old}(\\cdot|s))$, "
    "$\\varepsilon_\\pi = \\max_s |\\mathbb{E}_{a \\sim \\pi}[A_{\\pi_{old}}(s,a)]|$, and $\\gamma$ is the discount factor.",
    title="TRPO monotonic improvement bound (definition)",
)

# ── Claims ────────────────────────────────────────────────────────────────────

grpo_no_diversity = claim(
    "GRPO's absence of divergence regularization provides no mechanism to prevent the "
    "policy from drifting away from the reference (base) model's distribution, leaving "
    "low-reward but solution-diverse regions of the policy unprotected from collapse.",
    title="GRPO lacks diversity protection",
)

rkl_mode_seeking_harm = claim(
    "When reverse KL-divergence $D_{KL}(\\pi_\\theta \\| \\pi_{ref})$ is used as a "
    "regularizer in RLVR, it enforces mode-seeking behavior: the policy concentrates on "
    "the dominant high-reward solution modes of the reference policy while suppressing "
    "alternative (low-probability but valid) solution styles. This theoretically forces "
    "convergence to a single high-probability solution pattern, worsening diversity collapse "
    "relative to using no divergence at all.",
    title="Reverse KL enforces harmful mode-seeking",
)

forward_kl_mass_covering = claim(
    "Forward KL-divergence $D_{KL}(\\pi_{ref} \\| \\pi_\\theta)$ is mass-covering: minimizing "
    "$D_{KL}(\\pi_{ref} \\| \\pi_\\theta) = \\sum_a \\pi_{ref}(a|q)\\log\\frac{\\pi_{ref}(a|q)}{\\pi_\\theta(a|q)}$ "
    "penalizes the trained policy $\\pi_\\theta$ whenever it assigns near-zero probability "
    "to actions that the reference policy considers plausible, thereby preventing the "
    "policy from fully abandoning solution modes present in the base model.",
    title="Forward KL is mass-covering",
)

js_mass_covering = claim(
    "Jensen-Shannon divergence $D_{JS}(\\pi_\\theta \\| \\pi_{ref})$ is mass-covering and "
    "symmetric. For the preservation set $\\mathcal{D}_{pef}$, it is computed as: "
    "$D_{JS} = \\sum_a \\pi_{ref}(a|q)\\left[\\frac{u \\log u}{2} - \\frac{u+1}{2}\\log\\frac{u+1}{2}\\right]$ "
    "where $u = \\pi_\\theta(a|q)/\\pi_{ref}(a|q)$. This is bounded and provides a softer "
    "mass-covering constraint than forward-KL.",
    title="Jensen-Shannon divergence is mass-covering",
)

__all__ = [
    "grpo_no_diversity",
    "rkl_mode_seeking_harm",
    "forward_kl_mass_covering",
    "js_mass_covering",
]
