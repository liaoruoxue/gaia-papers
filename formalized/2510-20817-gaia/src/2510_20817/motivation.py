"""Introduction and Motivation: KL-Regularized RL and Diversity Collapse"""

from gaia.lang import claim, setting, question, support, deduction, contradiction, complement

# ── Settings: Formal Definitions ──────────────────────────────────────────────

kl_rl_objective = setting(
    "KL-regularized reward maximization objective: "
    "$J(\\pi_\\theta) = \\mathbb{E}_{\\pi_\\theta(y)}[R(y)] - \\beta D(\\pi_\\theta, \\pi_{\\text{ref}})$, "
    "where $R: \\mathcal{Y} \\to \\mathbb{R}$ is the reward function, $\\pi_\\theta$ is the policy, "
    "$\\pi_{\\text{ref}}$ is the reference (base) distribution, $\\beta > 0$ is the regularization coefficient, "
    "and $D(\\cdot, \\cdot)$ is the KL divergence between the policy and the reference.",
    title="KL-regularized RL objective",
)

reverse_kl_def = setting(
    "The reverse KL divergence is defined as $D_{KL}(q \\| p) = \\mathbb{E}_q[\\log q(y) - \\log p(y)]$. "
    "In the variational inference (VI) literature, it is traditionally characterized as 'mode seeking': "
    "the approximating distribution $q$ avoids placing mass where $p$ is small.",
    title="Reverse KL divergence definition",
)

forward_kl_def = setting(
    "The forward KL divergence is defined as $D_{KL}(p \\| q) = \\mathbb{E}_p[\\log p(y) - \\log q(y)]$. "
    "In the variational inference (VI) literature, it is traditionally characterized as 'mass covering': "
    "the approximating distribution $q$ places mass everywhere $p$ has mass.",
    title="Forward KL divergence definition",
)

flexible_family_def = setting(
    "A 'flexible' distribution family (e.g., independent categoricals, large language models) "
    "is one that is sufficiently expressive to match any target distribution to zero KL divergence "
    "in principle. This contrasts with 'restrictive' families such as two-parameter Gaussians, "
    "which are limited to a constrained set of shapes and can only approximate the target.",
    title="Flexible vs. restrictive distribution families",
)

multimodal_def = setting(
    "A solution distribution for KL-regularized reward maximization is 'multimodal' (Definition 3.5) "
    "if all high-reward samples have a high probability. "
    "Formally: a solution is multimodal if for all $y$ with $R(y) \\geq \\tau$ (for some threshold $\\tau$), "
    "$\\pi^*(y)$ is high relative to $\\pi_{\\text{ref}}(y)$.",
    title="Definition of multimodal solution distribution",
)

# ── Questions ─────────────────────────────────────────────────────────────────

q_diversity_collapse = question(
    "Does the KL-regularized RL objective, when optimized to its global optimum, "
    "produce a solution (policy) distribution that is diverse (multimodal)?",
    title="Main research question: diversity of RL optimal solution",
)

q_mode_seeking_intuition = question(
    "Does the mode-seeking / mass-covering characterization of reverse / forward KL from variational "
    "inference transfer to the setting of KL-regularized reward maximization (RL)?",
    title="Applicability of KL intuitions to RL setting",
)

# ── Claims: Introduction ───────────────────────────────────────────────────────

rl_diversity_matters = claim(
    "Output diversity of a policy trained via RL is crucial for downstream applications. "
    "In large language models (LLMs), diversity drives engagement in creative writing and conversation. "
    "More broadly, diversity underlies discovery of novel mathematical solutions, cognitive science models, "
    "and novel algorithms. Furthermore, diversity reflects uncertainty over competing hypotheses, "
    "which is fundamental to scientific discovery. During training, diversity drives exploration "
    "that helps policies converge to better solutions.",
    title="Importance of output diversity in RL post-training",
)

empirical_diversity_collapse = claim(
    "Current empirical evidence suggests RL post-training improves quality at the cost of diversity "
    "(Kirk et al., 2023; Cui et al., 2025). Multiple works report entropy collapse after standard "
    "KL-regularized RL post-training across different tasks: format, creativity, reasoning, and exploration.",
    title="Empirical observation: RL reduces diversity",
    metadata={"source": "artifacts/2510.20817.pdf, Introduction and Appendix A"},
)

vi_kl_intuition_holds_restrictive = claim(
    "For a restrictive variational distribution family (e.g., a two-parameter Gaussian), "
    "the standard intuitions hold: reverse KL divergence minimization is 'mode seeking' (the approximation "
    "collapses onto a single mode of the target), while forward KL minimization is 'mass covering' "
    "(the approximation spreads mass over all modes). "
    "This is because with a restrictive family the KL cannot be driven to zero, "
    "and the two KL variants penalize mismatches differently.",
    title="KL intuitions hold for restrictive distribution families",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 1a"},
)

vi_kl_intuition_fails_flexible = claim(
    "For a flexible distribution family (e.g., independent categoricals, foundational language models), "
    "the standard 'mode seeking' / 'mass covering' intuitions do NOT necessarily hold. "
    "Optimizing either reverse or forward KL to the global optimum can well-approximate a complex, "
    "multimodal target distribution. The mode-coverage behavior depends on the target distribution's "
    "shape, not on the KL variant used.",
    title="KL intuitions do not hold for flexible distribution families",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 1b"},
)

kl_type_not_primary_driver = claim(
    "In KL-regularized RL (where foundation models are used as flexible policies), "
    "the choice of reverse vs. forward KL regularization does not primarily determine "
    "whether the solution distribution is diverse (multimodal). "
    "Instead, mode coverage depends primarily on the regularization strength $\\beta$ "
    "and the relative scales between rewards and reference policy probabilities.",
    title="KL type is not the primary driver of diversity in RL",
)

typical_settings_unimodal = claim(
    "Under commonly used RL hyperparameter settings—specifically, "
    "(a) weak KL regularization (low $\\beta$) with varied rewards across correct answers, or "
    "(b) any regularization strength when correct answers have equal rewards but vastly different "
    "reference policy probabilities—"
    "the globally optimal solution distribution is, by construction, unimodal. "
    "This means diversity collapse is a natural consequence of correctly optimizing the RL objective, "
    "not a pathology of imperfect optimization.",
    title="Typical RL settings produce unimodal optimal solutions",
)

mara_exists = claim(
    "The Mode Anchored Reward Augmentation (MARA) algorithm is a simple, scalable, and theoretically "
    "justified modification to the standard KL-regularized RL objective. "
    "It makes minimal changes to reward magnitudes and optimizes for a target distribution "
    "that places high probability over all high-quality sampling modes simultaneously, "
    "without requiring any external signal of diversity. "
    "MARA can be used as a drop-in replacement for standard RL training (two lines of pseudocode change).",
    title="MARA algorithm: existence and properties",
)

# ── Structural constraints ─────────────────────────────────────────────────────

comp_kl_intuitions = complement(
    vi_kl_intuition_holds_restrictive,
    vi_kl_intuition_fails_flexible,
    reason="The two claims partition the space of distribution family expressiveness: "
           "for restrictive families the classical intuitions hold, for flexible families they do not. "
           "In the RL setting with LLMs (flexible family), only the latter applies.",
    prior=0.95,
)
