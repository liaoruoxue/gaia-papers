"""Section 4: Analysis of KL-Regularized Optimal Distribution — Mode Coverage"""

from gaia.lang import claim, setting, support, deduction, abduction, induction

from .motivation import (
    kl_rl_objective,
    reverse_kl_def,
    forward_kl_def,
    multimodal_def,
    typical_settings_unimodal,
    kl_type_not_primary_driver,
)
from .s3_optimal_distributions import (
    reverse_kl_optimal_dist,
    forward_kl_optimal_dist,
    both_kl_can_multimodal,
    reverse_kl_obj_def,
)

# ── Settings ───────────────────────────────────────────────────────────────────

prob_ratio_tool = setting(
    "The central analytical tool in Section 4 is the probability ratio $G_\\beta(y_1)/G_\\beta(y_2)$ "
    "between any two samples under the optimal reverse-KL solution distribution. "
    "Because the normalizing constant $\\zeta$ cancels in the ratio, "
    "this ratio can be computed in closed form from only $\\pi_{\\text{ref}}$ and $R$.",
    title="Probability ratio as analytical tool",
)

equal_support_setting = setting(
    "The 'equal support' case: two samples $y_1, y_2$ have the same probability under the "
    "reference distribution, $\\pi_{\\text{ref}}(y_1) = \\pi_{\\text{ref}}(y_2)$.",
    title="Equal support case definition",
)

equal_reward_setting = setting(
    "The 'equal reward' case: two samples $y_1, y_2$ have the same reward, $R(y_1) = R(y_2)$. "
    "This is the standard setup for RL with verifiable rewards (e.g., math): "
    "a correct answer receives reward 1, an incorrect answer receives reward 0.",
    title="Equal reward case definition",
)

# ── Core analysis claims ───────────────────────────────────────────────────────

log_prob_ratio_formula = claim(
    "The log probability ratio between any two samples $y_1, y_2$ under the optimal "
    "reverse-KL solution $G_\\beta$ is: "
    "$$\\log \\frac{G_\\beta(y_1)}{G_\\beta(y_2)} = \\log \\frac{\\pi_{\\text{ref}}(y_1)}{\\pi_{\\text{ref}}(y_2)} + \\frac{1}{\\beta}\\bigl(R(y_1) - R(y_2)\\bigr)$$. "
    "The normalizing constant $\\zeta$ cancels. "
    "This allows exact computation of relative probabilities using only $\\pi_{\\text{ref}}$ and $R$.",
    title="Log probability ratio under G_beta in closed form (Proposition 4.1)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 4, Eq. (7); Appendix B.6"},
)

equal_support_exponential_gap = claim(
    "When two samples have equal reference probability ($\\pi_{\\text{ref}}(y_1) = \\pi_{\\text{ref}}(y_2)$), "
    "their probability ratio in the optimal solution is: "
    "$G_\\beta(y_1)/G_\\beta(y_2) = \\exp\\bigl((R(y_1) - R(y_2))/\\beta\\bigr)$. "
    "A linear difference $\\Delta R$ in rewards produces an EXPONENTIAL difference in optimal-solution probabilities. "
    "At commonly used $\\beta = 10^{-3}$, a reward difference of $\\Delta R = 0.1$ "
    "makes the higher-reward sample $2.6 \\times 10^{43}$ times more likely in the solution distribution. "
    "This implies the solution is highly concentrated around the maximum-reward mode.",
    title="Equal support: exponential probability gap from linear reward gap (Remark 4.2)",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 3"},
)

equal_reward_preserves_ratio = claim(
    "When two samples have equal reward ($R(y_1) = R(y_2)$), their probability ratio in the "
    "optimal solution is: $G_\\beta(y_1)/G_\\beta(y_2) = \\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2)$. "
    "This ratio is INDEPENDENT of the regularization strength $\\beta$. "
    "Therefore, KL-regularized RL with equal rewards never promotes a low-support answer: "
    "the solution preserves the reference policy's relative probabilities among equally rewarded samples, "
    "regardless of which KL variant or what $\\beta$ value is used. "
    "This holds for both reverse and forward KL regularization.",
    title="Equal reward: RL preserves reference probability ratios (Remark 4.3)",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 4"},
)

beta_as_mode_knob = claim(
    "When two samples $y_1, y_2$ have BOTH different rewards AND different reference policy probabilities, "
    "a unique value of $\\beta$ exists that makes them equally probable in the solution distribution. "
    "This occurs when: $R(y_2) - R(y_1) = \\beta (\\log \\pi_{\\text{ref}}(y_1) - \\log \\pi_{\\text{ref}}(y_2))$ (Eq. 10). "
    "This is the true role of the regularization coefficient $\\beta$: it trades off "
    "between preferring higher-rewarding, low-support answers "
    "versus lower-rewarding, high-support answers. "
    "Mode coverage is determined by this interplay, not by the KL variant.",
    title="Beta as mode-selection knob (Remark 4.4)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 4.3, Eq. (10)"},
)

beta_prediction_figure2 = claim(
    "Using Remark 4.4 (Eq. 10), the crossover $\\beta$ for the Figure 2 example can be predicted analytically: "
    "the two high-reward modes have rewards 0.75 and 1.0, and reference log probabilities "
    "$\\log \\pi_{\\text{ref}}(y_1) \\approx -4.05$ and $\\log \\pi_{\\text{ref}}(y_2) \\approx -5.95$. "
    "The predicted crossover is $(1 - 0.75)/(-4.05 + 5.95) \\approx 0.132$. "
    "Indeed, Figure 2 shows the reverse-KL solution switches modal preference between $\\beta=0.10$ and $\\beta=0.15$, "
    "confirming the theory.",
    title="Empirical validation of beta prediction for Figure 2",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 2; Section 4.3"},
)

low_beta_unimodal = claim(
    "At commonly used RL hyperparameter settings (low $\\beta \\approx 10^{-3}$ to $10^{-2}$) "
    "with varied reward levels, "
    "the solution distribution is highly concentrated around a single mode: the one with the highest reward "
    "among well-supported answers. "
    "The exponential amplification factor $\\exp(\\Delta R/\\beta)$ is so large that "
    "any reward difference between correct answers causes extreme probability concentration. "
    "This means diversity collapse is not a training pathology but a consequence of correct optimization.",
    title="Low beta with varied rewards produces unimodal solution",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 3, 7"},
)

equal_reward_unimodal = claim(
    "With any regularization strength $\\beta$, if all correct answers have equal reward "
    "but one answer has much higher reference probability (e.g., 15x more likely under $\\pi_{\\text{ref}}$), "
    "the optimal solution ALSO assigns 15x more probability to that answer. "
    "RL cannot be used to 'discover' lower-support correct answers by adjusting $\\beta$. "
    "Figure 4 demonstrates: the final policy exactly preserves the 15x probability imbalance.",
    title="Equal reward with unequal support: RL cannot equalize probabilities",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 4"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_log_ratio = deduction(
    [reverse_kl_optimal_dist],
    log_prob_ratio_formula,
    reason=(
        "Direct algebraic derivation from $G_\\beta$'s closed form (@reverse_kl_optimal_dist): "
        "$G_\\beta(y_1)/G_\\beta(y_2) = [\\pi_{\\text{ref}}(y_1)\\exp(R(y_1)/\\beta)/\\zeta] / "
        "[\\pi_{\\text{ref}}(y_2)\\exp(R(y_2)/\\beta)/\\zeta]$. "
        "The normalizing constants $\\zeta$ cancel exactly. "
        "Taking logs yields Eq. 7 directly (Appendix B.6, Eq. 65-67). No approximation involved.",
    ),
    prior=0.99,
    background=[prob_ratio_tool],
)

strat_equal_support = deduction(
    [log_prob_ratio_formula],
    equal_support_exponential_gap,
    reason=(
        "Substituting $\\pi_{\\text{ref}}(y_1) = \\pi_{\\text{ref}}(y_2)$ into @log_prob_ratio_formula: "
        "the log ratio term $\\log(\\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2)) = 0$, "
        "leaving $\\log(G_\\beta(y_1)/G_\\beta(y_2)) = (R(y_1)-R(y_2))/\\beta$. "
        "Exponentiating gives $G_\\beta(y_1)/G_\\beta(y_2) = \\exp(\\Delta R/\\beta)$. "
        "Plugging in $\\Delta R = 0.1$ and $\\beta = 10^{-3}$: "
        "$\\exp(0.1/0.001) = \\exp(100) \\approx 2.6 \\times 10^{43}$. "
        "This is a deterministic algebraic calculation from @equal_support_setting.",
    ),
    prior=0.99,
    background=[equal_support_setting],
)

strat_equal_reward = deduction(
    [log_prob_ratio_formula],
    equal_reward_preserves_ratio,
    reason=(
        "Substituting $R(y_1) = R(y_2)$ into @log_prob_ratio_formula: "
        "the reward difference term $(R(y_1)-R(y_2))/\\beta = 0$, "
        "leaving $\\log(G_\\beta(y_1)/G_\\beta(y_2)) = \\log(\\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2))$. "
        "Exponentiating: $G_\\beta(y_1)/G_\\beta(y_2) = \\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2)$. "
        "This is $\\beta$-independent by @equal_reward_setting. "
        "The analogous result holds for forward-KL (@forward_kl_optimal_dist) — "
        "the ratio $G_{\\text{fwd}}(y_1)/G_{\\text{fwd}}(y_2) = \\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2)$ "
        "when rewards are equal (Appendix B.3 footnote 1).",
    ),
    prior=0.99,
    background=[equal_reward_setting],
)

strat_beta_knob = deduction(
    [log_prob_ratio_formula],
    beta_as_mode_knob,
    reason=(
        "From @log_prob_ratio_formula, setting $G_\\beta(y_1)/G_\\beta(y_2) = 1$ "
        "(equal probability in solution distribution): "
        "$0 = \\log(\\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2)) + (R(y_1) - R(y_2))/\\beta$. "
        "Solving for $\\beta$: $\\beta^* = (R(y_2) - R(y_1))/(\\log \\pi_{\\text{ref}}(y_1) - \\log \\pi_{\\text{ref}}(y_2))$. "
        "This gives the unique $\\beta$ at which the two modes are equally probable. "
        "Below this $\\beta$, the reward difference dominates (high-reward mode wins); "
        "above it, the reference probability difference dominates (high-support mode wins). "
        "This is exactly Eq. 10 of the paper, derived from @log_prob_ratio_formula.",
    ),
    prior=0.99,
)

strat_beta_prediction = support(
    [beta_as_mode_knob, both_kl_can_multimodal],
    beta_prediction_figure2,
    reason=(
        "Applying the analytical formula from @beta_as_mode_knob to the specific Figure 2 setting: "
        "$\\beta^* = (1 - 0.75) / (-4.05 + 5.95) = 0.25 / 1.90 \\approx 0.132$. "
        "The Figure 2 empirical data (@both_kl_can_multimodal) shows the mode preference switches "
        "between $\\beta = 0.10$ and $\\beta = 0.15$, which brackets the predicted $\\beta^* \\approx 0.132$. "
        "The match is quantitatively close, supporting the theory.",
    ),
    prior=0.9,
)

strat_low_beta_unimodal = deduction(
    [equal_support_exponential_gap, beta_as_mode_knob],
    low_beta_unimodal,
    reason=(
        "From @equal_support_exponential_gap: at $\\beta = 10^{-3}$, a reward gap of only 0.1 "
        "creates a $2.6 \\times 10^{43}$ probability ratio in the solution. "
        "Even with mild reward variation across correct answers (e.g., length differences in rewards), "
        "the solution is effectively unimodal. "
        "From @beta_as_mode_knob: the crossover $\\beta$ needed to equalize two modes depends on "
        "the log ratio of their reference probabilities divided by their reward gap. "
        "For typical LLM settings where reward differences are small (0.01-0.1) and reference "
        "probability differences are moderate (log ratio ~1-5), "
        "the crossover $\\beta$ is also small — but still much larger than the $\\beta = 10^{-3}$ "
        "commonly used in practice. Hence, in practice, the solution is unimodal.",
    ),
    prior=0.99,
)

strat_equal_reward_unimodal = deduction(
    [equal_reward_preserves_ratio],
    equal_reward_unimodal,
    reason=(
        "Direct consequence of @equal_reward_preserves_ratio: "
        "if $\\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2) = 15$ and $R(y_1) = R(y_2)$, "
        "then $G_\\beta(y_1)/G_\\beta(y_2) = 15$ regardless of $\\beta$. "
        "No choice of $\\beta$ can change this ratio. "
        "Figure 4 illustrates this empirically: the final trained policy maintains exactly the 15x gap "
        "between a high-support and low-support equally-correct answer.",
    ),
    prior=0.99,
    background=[equal_reward_setting],
)

strat_typical_settings = deduction(
    [low_beta_unimodal, equal_reward_unimodal],
    typical_settings_unimodal,
    reason=(
        "Two complementary failure modes (@low_beta_unimodal and @equal_reward_unimodal) "
        "together cover the most common practical RL settings: "
        "(1) When rewards vary (even slightly), the exponential amplification at small $\\beta$ "
        "collapses the distribution onto the single maximum-reward mode. "
        "(2) When rewards are equal (e.g., binary 0/1 correctness), "
        "the reference probability imbalance is exactly preserved, "
        "so the high-support mode always dominates. "
        "These two cases jointly imply that standard RL settings produce unimodal optimal solutions, "
        "and diversity collapse is by-construction, not due to optimization failure.",
    ),
    prior=0.99,
)

strat_kl_type_not_primary = support(
    [equal_support_exponential_gap, equal_reward_preserves_ratio, beta_as_mode_knob],
    kl_type_not_primary_driver,
    reason=(
        "All three core results (@equal_support_exponential_gap, @equal_reward_preserves_ratio, "
        "@beta_as_mode_knob) are derived from @log_prob_ratio_formula which applies to the "
        "reverse-KL case, and the analogous results hold for forward-KL (footnote 1 in the paper). "
        "The key factors determining mode coverage are: "
        "(1) the reward difference $\\Delta R$ (Remark 4.2), "
        "(2) the reference probability ratio $\\pi_{\\text{ref}}(y_1)/\\pi_{\\text{ref}}(y_2)$ (Remark 4.3), "
        "(3) the regularization strength $\\beta$ (Remark 4.4). "
        "None of these depend on the KL variant, confirming @kl_type_not_primary_driver.",
    ),
    prior=0.92,
)
