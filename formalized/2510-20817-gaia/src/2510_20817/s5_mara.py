"""Section 5: Directly Optimizing a Multimodal Target — the MARA Algorithm"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    kl_rl_objective,
    multimodal_def,
    mara_exists,
)
from .s3_optimal_distributions import (
    reverse_kl_optimal_dist,
    reverse_kl_obj_def,
)
from .s4_mode_coverage_analysis import (
    beta_as_mode_knob,
    log_prob_ratio_formula,
    low_beta_unimodal,
    equal_reward_unimodal,
)

# ── Settings ───────────────────────────────────────────────────────────────────

mara_algorithm_def = setting(
    "Mode Anchored Reward Augmentation (MARA, Algorithm 1) is defined as follows: "
    "Given batch $\\{y_i\\}_{i=1}^N \\sim \\pi_\\theta$, reward threshold $\\tau \\leq \\max_y R(y)$: "
    "(1) Select anchor: $z = \\arg\\max_{y_i} \\pi_{\\text{ref}}(y_i)$ subject to $R(y_i) \\geq \\tau$; "
    "(2) For each $y_i$ in batch: "
    "if $R(y_i) \\geq \\tau$: set augmented reward $\\bar{r}_i = R(z) + \\beta(\\log \\pi_{\\text{ref}}(z) - \\log \\pi_{\\text{ref}}(y_i))$; "
    "else: keep $\\bar{r}_i = R(y_i)$; "
    "(3) Optimize $\\pi_\\theta$ using augmented rewards $\\{\\bar{r}_i\\}$. "
    "The only changes from standard RL are shown in blue (2 lines).",
    title="MARA algorithm definition (Algorithm 1)",
    metadata={"source": "artifacts/2510.20817.pdf, Algorithm 1"},
)

mara_alt_impl = setting(
    "An alternative implementation of MARA (Algorithm 2): instead of augmenting the reward, "
    "for above-threshold samples replace both the reward $r_i \\leftarrow R(z)$ "
    "AND the reference probability $\\bar{p}_i \\leftarrow \\pi_{\\text{ref}}(z)$. "
    "This is gradient-equivalent to Algorithm 1 when using reverse-KL regularization "
    "(Appendix B.8, Eq. 79-81), providing an alternative implementation perspective.",
    title="Alternative MARA implementation (Algorithm 2)",
    metadata={"source": "artifacts/2510.20817.pdf, Algorithm 2; Appendix B.8"},
)

# ── Core claims about MARA ─────────────────────────────────────────────────────

mara_augmented_reward = claim(
    "The MARA augmented reward function $\\bar{R}(y)$ is defined as: "
    "$\\bar{R}(y) = R(y)$ if $R(y) < \\tau$, and "
    "$\\bar{R}(y) = R(z) + \\beta(\\log \\pi_{\\text{ref}}(z) - \\log \\pi_{\\text{ref}}(y))$ if $R(y) \\geq \\tau$, "
    "where $z = \\arg\\max_y \\pi_{\\text{ref}}(y)$ subject to $R(y) \\geq \\tau$ is the 'anchor' sample "
    "— the most likely high-quality sample under the reference policy. "
    "The augmentation for high-reward samples offsets each sample's reward by its log probability gap from the anchor.",
    title="MARA augmented reward function (Eq. 11)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 5, Eq. (11)"},
)

mara_solution_is_uniform = claim(
    "Optimizing the reverse-KL regularized RL objective with the MARA augmented reward "
    "$\\bar{R}$ yields the solution distribution: "
    "$\\bar{G}_\\beta(y) \\propto \\pi_{\\text{ref}}(y) \\exp(R(y)/\\beta)$ if $R(y) < \\tau$, and "
    "$\\bar{G}_\\beta(y) \\propto \\pi_{\\text{ref}}(z) \\exp(R(z)/\\beta)$ if $R(y) \\geq \\tau$. "
    "For all above-threshold samples the unnormalized density is IDENTICAL: "
    "$\\pi_{\\text{ref}}(z) \\exp(R(z)/\\beta)$ — a constant independent of $y$. "
    "This means the solution places EQUAL probability mass on all high-reward samples, "
    "regardless of their individual reference probabilities.",
    title="MARA solution distribution is uniform over high-reward region (Remark B.3)",
    metadata={"source": "artifacts/2510.20817.pdf, Appendix B.7, Eq. (68)"},
)

mara_anchor_choice = claim(
    "Choosing the anchor $z = \\arg\\max_y \\pi_{\\text{ref}}(y)$ subject to $R(y) \\geq \\tau$ "
    "(the highest reference-probability high-quality sample) ensures that all above-threshold samples "
    "receive the maximum possible density in the solution distribution. "
    "This is because $\\pi_{\\text{ref}}(z) \\exp(R(z)/\\beta)$ is the largest constant the "
    "uniform density can take. Choosing any other anchor still yields uniform mass but at a lower level.",
    title="Anchor choice maximizes high-reward density",
    metadata={"source": "artifacts/2510.20817.pdf, Section 5"},
)

mara_gradient_interpretation = claim(
    "The MARA gradient estimator for an above-threshold sample $y_i$ (i.e., $R(y_i) \\geq \\tau$) "
    "under reverse-KL regularization can be written as: "
    "$\\bar{K}_i = (R(z) - \\beta \\log \\pi_\\theta(y_i)/\\pi_{\\text{ref}}(z)) \\nabla_\\theta \\log \\pi_\\theta(y_i)$. "
    "This is equivalent to using the ANCHOR'S reference probability $\\pi_{\\text{ref}}(z)$ in the KL term, "
    "instead of the sample's own $\\pi_{\\text{ref}}(y_i)$. "
    "Since $z$ is chosen with high $\\pi_{\\text{ref}}$, this selectively reduces the KL regularization penalty "
    "for high-rewarding but low-support samples, effectively 'lifting' them in the solution.",
    title="MARA gradient interpretation: reduced KL for low-support high-reward samples (Appendix B.8)",
    metadata={"source": "artifacts/2510.20817.pdf, Appendix B.8, Eq. (79-81)"},
)

mara_works_fwd_kl = claim(
    "MARA is empirically effective for both forward and reverse KL regularization. "
    "Figure 5 shows that vanilla reverse/forward KL RL collapses to the on-support mode, "
    "while MARA with either KL yields equal high mass over all high-reward regions. "
    "This is consistent with theory: the augmented reward addresses the same underlying probability-ratio "
    "imbalance that causes mode collapse in both KL variants.",
    title="MARA works for both forward and reverse KL",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 5"},
)

mara_threshold_setting = claim(
    "The MARA threshold $\\tau$ can be set in two ways: "
    "(1) If the reward range is known, $\\tau$ can be a fixed constant (e.g., $\\tau = 0.8$ for verifiable rewards). "
    "(2) If the reward range is unknown (e.g., non-verifiable tasks with reward models), "
    "$\\tau$ can be set per-batch as an upper percentile of sampled rewards.",
    title="MARA threshold setting strategy",
)

# ── Strategies ─────────────────────────────────────────────────────────────────

strat_mara_solution = deduction(
    [reverse_kl_optimal_dist, mara_augmented_reward],
    mara_solution_is_uniform,
    reason=(
        "From @reverse_kl_optimal_dist: the solution distribution with augmented reward $\\bar{R}$ is "
        "$\\bar{G}_\\beta(y) \\propto \\pi_{\\text{ref}}(y)\\exp(\\bar{R}(y)/\\beta)$. "
        "Substituting @mara_augmented_reward for the case $R(y) \\geq \\tau$: "
        "$\\log \\pi_{\\text{ref}}(y) + \\bar{R}(y)/\\beta "
        "= \\log \\pi_{\\text{ref}}(y) + R(z)/\\beta + \\log \\pi_{\\text{ref}}(z) - \\log \\pi_{\\text{ref}}(y) "
        "= R(z)/\\beta + \\log \\pi_{\\text{ref}}(z)$. "
        "The $\\pi_{\\text{ref}}(y)$ terms cancel exactly, giving a constant $\\pi_{\\text{ref}}(z)\\exp(R(z)/\\beta)$ "
        "for ALL $y$ with $R(y) \\geq \\tau$. "
        "This is a deterministic algebraic derivation (Appendix B.7, Eq. 72-76).",
    ),
    prior=0.99,
    background=[mara_algorithm_def],
)

strat_mara_from_remark44 = deduction(
    [beta_as_mode_knob, mara_augmented_reward],
    mara_anchor_choice,
    reason=(
        "From @beta_as_mode_knob (Remark 4.4, Eq. 10): two samples have equal probability in the "
        "solution distribution when $R(y_2) - R(y_1) = \\beta(\\log \\pi_{\\text{ref}}(y_1) - \\log \\pi_{\\text{ref}}(y_2))$. "
        "Rearranging: $R(y_2) + \\beta \\log \\pi_{\\text{ref}}(z) - \\beta \\log \\pi_{\\text{ref}}(y_2) = R(y_1) + \\text{const}$. "
        "This is exactly the form of @mara_augmented_reward with $z = y_1$ as anchor. "
        "Choosing $z$ as the maximum $\\pi_{\\text{ref}}$ sample among high-reward samples ensures that "
        "the uniform density level $\\pi_{\\text{ref}}(z)\\exp(R(z)/\\beta)$ is maximized per @mara_solution_is_uniform.",
    ),
    prior=0.99,
)

strat_mara_exists = support(
    [mara_solution_is_uniform, mara_works_fwd_kl],
    mara_exists,
    reason=(
        "MARA achieves a diverse (multimodal) solution by construction: "
        "@mara_solution_is_uniform proves the augmented-reward solution places equal probability "
        "on all high-reward samples, satisfying the multimodality definition. "
        "@mara_works_fwd_kl confirms empirically that this works in practice with both KL variants. "
        "The algorithm requires only 2 lines of pseudocode change (@mara_algorithm_def), "
        "making it a practical drop-in replacement.",
    ),
    prior=0.93,
    background=[multimodal_def, mara_algorithm_def],
)
