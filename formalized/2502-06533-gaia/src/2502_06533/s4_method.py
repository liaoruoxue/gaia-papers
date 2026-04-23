"""Section 4: Prioritized KL Penalty Method"""

from gaia.lang import claim, setting, support, deduction

from .motivation import kl_penalty_def, negentropy_def, rl_finetuning_challenge
from .s3_critical_tokens import (
    critical_token_def,
    critical_token_uncertainty_gap,
    critical_tokens_localize_failure,
    obs_ct_n3, obs_ct_n5, obs_ct_n7,
)

# --- Method description ---

prioritized_kl_method = claim(
    "The paper proposes a 'Prioritized KL Penalty' that modifies the standard KL penalty "
    "by weighting each token's contribution by the pre-trained model's confidence (normalized negentropy) "
    "at that token position:\\n\\n"
    "$$\\tilde{\\mathcal{L}}_{\\mathrm{KL}} = "
    "\\mathbb{E}\\left[\\hat{J}_{\\theta_{\\mathrm{old}}}(s)^\\beta \\cdot "
    "\\log\\left(\\frac{\\pi_\\theta(a|s)}{\\pi_{\\theta_{\\mathrm{old}}}(a|s)}\\right)\\right]$$\\n\\n"
    "where $\\hat{J}_{\\theta_{\\mathrm{old}}}(s)$ is the normalized negentropy (confidence) of the "
    "pre-trained (reference) model at state $s$, and $\\beta > 0$ is a hyperparameter controlling "
    "the strength of confidence weighting. "
    "When the reference model is highly confident ($\\hat{J} \\approx 1$), the penalty is nearly "
    "unchanged from the standard KL penalty. When the reference model is uncertain ($\\hat{J} \\approx 0$, "
    "i.e., near-critical tokens), the penalty is reduced toward zero, allowing greater policy divergence.",
    title="Prioritized KL penalty formula",
)

prioritized_kl_intuition = claim(
    "The intuition behind the Prioritized KL Penalty is that the standard KL penalty "
    "uniformly constrains the policy across all tokens, including critical tokens where "
    "the pre-trained model is uncertain and where exploration is most needed. "
    "By reducing the KL penalty on uncertain (critical) tokens and preserving it on confident "
    "(non-critical) tokens, the method enables targeted exploration at decision points that "
    "determine task success, without destabilizing the policy at positions where the pre-trained "
    "model already has reliable behavior.",
    title="Prioritized KL penalty: intuition for targeted exploration",
)

beta_hyperparameter = claim(
    "The hyperparameter $\\beta$ in the Prioritized KL Penalty controls the sharpness of "
    "confidence-based weighting. The method was tested across $\\beta \\in \\{10, 50, 100, 150, "
    "200, 300, 500, 1000, 10000\\}$. Performance is robust across $\\beta \\in [10, 500]$, "
    "with optimal performance at $\\beta = 500$; degradation occurs at $\\beta = 1000$ and "
    "drastic failure at $\\beta = 10000$ (excessive penalty reduction leading to instability). "
    "The primary experiments use $\\beta = 150$.",
    title="Beta hyperparameter robustness range [10, 500]",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 6 (Appendix C)"},
)

# --- Strategies ---

# The prioritized KL method design is derived from the combination of:
# (1) definition of KL penalty, (2) negentropy as confidence measure, (3) the critical token insight
strat_method_design = support(
    [critical_token_uncertainty_gap, critical_tokens_localize_failure],
    prioritized_kl_method,
    reason=(
        "Given @critical_token_uncertainty_gap (the pre-trained model is systematically less "
        "confident on critical tokens) and @critical_tokens_localize_failure (these tokens "
        "determine task success), the @prioritized_kl_method follows: weight the KL penalty "
        "by $\\hat{J}^\\beta$ (normalized negentropy to the power $\\beta$) so that uncertain "
        "tokens receive a smaller penalty, enabling the policy to explore freely there while "
        "remaining constrained at confident (non-critical) positions. "
        "This directly translates the @negentropy_def into a penalty weighting scheme."
    ),
    prior=0.85,
    background=[kl_penalty_def, negentropy_def],
)

strat_beta_robust = support(
    [prioritized_kl_method],
    beta_hyperparameter,
    reason=(
        "Given the @prioritized_kl_method, robustness across $\\beta$ values is expected "
        "because $\\hat{J}^\\beta$ is a smooth function of $\\beta$ that converges monotonically: "
        "for $\\hat{J} < 1$ (uncertain tokens), larger $\\beta$ suppresses the penalty more; "
        "for $\\hat{J} = 1$ (confident tokens), penalty is unchanged for any $\\beta$. "
        "Empirical testing across $\\beta \\in [10, 500]$ confirms this robustness."
    ),
    prior=0.82,
    background=[negentropy_def],
)

strat_intuition = support(
    [prioritized_kl_method],
    prioritized_kl_intuition,
    reason=(
        "The @prioritized_kl_method formula directly implies the @prioritized_kl_intuition: "
        "when $\\hat{J} \\approx 0$ (uncertain token, matching the critical token definition), "
        "the weight $\\hat{J}^\\beta \\approx 0$, effectively removing the KL penalty; "
        "when $\\hat{J} \\approx 1$ (confident token), the penalty is unchanged. "
        "This mathematical property corresponds to the stated intuition."
    ),
    prior=0.92,
    background=[kl_penalty_def, negentropy_def, critical_token_def],
)
