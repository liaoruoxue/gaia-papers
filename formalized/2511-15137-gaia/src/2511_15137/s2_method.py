"""Section 2: Method — GRPO-Verif Algorithm"""

from gaia.lang import claim, setting

from .motivation import (
    setting_grpo_definition,
    setting_verification_definition,
    verification_gap,
)

# --- GRPO base objective ---

setting_grpo_objective = setting(
    "The GRPO base objective (Equation 1) is:\n\n"
    "$$J_{GRPO}(\\theta) = \\mathbb{E}\\left[\\frac{1}{n}\\sum_{i=1}^{n}\\min\\left("
    "r_t^{(i)}(\\theta)\\hat{A}_t^{(i)},\\ \\text{clip}\\left(r_t^{(i)}(\\theta), 1-\\epsilon, 1+\\epsilon\\right)\\hat{A}_t^{(i)}"
    "\\right)\\right] - \\beta D_{KL}$$\n\n"
    "where $r_t^{(i)}(\\theta) = \\pi_\\theta(y_t^{(i)} | q, y_{<t}^{(i)}) / "
    "\\pi_{\\text{old}}(y_t^{(i)} | q, y_{<t}^{(i)})$ is the token-level probability ratio, "
    "$\\hat{A}_t^{(i)}$ is the group-normalized advantage, $\\epsilon$ is the clipping threshold, "
    "and $\\beta$ is the KL divergence penalty coefficient.",
    title="GRPO base objective",
)

setting_advantage_normalization = setting(
    "Group-relative advantage normalization (Equation 5): for a group of n solutions "
    "with rewards $\\{R^{(j)}\\}_{j=1}^n$, the advantage for solution $i$ is:\n\n"
    "$$\\hat{A}_t^{(i)} = \\frac{R^{(i)} - \\text{mean}(\\{R^{(j)}\\})}{\\text{std}(\\{R^{(j)}\\})}$$\n\n"
    "The same normalization formula applies to verification advantages $\\hat{A}_t^{V,(i)}$ "
    "computed over the group of verification rewards $\\{R_V^{(j)}\\}$.",
    title="Group-relative advantage normalization",
)

setting_reward_scheme = setting(
    "Reward scheme for both solution generation and verification in GRPO-Verif:\n\n"
    "| Output type | Condition | Reward |\n"
    "|-------------|-----------|--------|\n"
    "| Solution | Correct answer | +1 |\n"
    "| Solution | Incorrect answer | -1 |\n"
    "| Solution | No valid output | -1.5 |\n"
    "| Verification | Correct judgment | +1 |\n"
    "| Verification | Incorrect judgment | -1 |\n"
    "| Verification | No valid output | -1.5 |",
    title="Reward scheme",
)

# --- GRPO-Verif extension ---

grpo_verif_objective = claim(
    "The GRPO-Verif unified objective (Equations 3-4) is:\n\n"
    "$$J_{\\text{GRPO-Verif}}(\\theta) = \\mathbb{E}\\left[\\frac{1}{n}\\sum_{i=1}^{n}\\left("
    "\\frac{1}{|y^{(i)}|}\\sum_t r_t^{(i)}(\\theta)\\hat{A}_t^{(i)} + "
    "\\alpha \\cdot \\frac{1}{|v^{(i)}|}\\sum_t \\hat{r}_t^{(i)}(\\theta)\\hat{A}_t^{V,(i)}"
    "\\right)\\right]$$\n\n"
    "where $v^{(i)}$ is the verification response for solution $y^{(i)}$, "
    "$\\hat{r}_t^{(i)}(\\theta) = \\pi_\\theta(v_t^{(i)} | q, y^{(i)}, v_{<t}^{(i)}) / "
    "\\pi_{\\text{old}}(v_t^{(i)} | q, y^{(i)}, v_{<t}^{(i)})$ is the verification probability ratio, "
    "$\\hat{A}_t^{V,(i)}$ is the group-normalized verification advantage, and "
    "$\\alpha$ is a scalar hyperparameter controlling verification loss weight (set to 0.2 in experiments).",
    title="GRPO-Verif joint objective",
    background=[setting_grpo_objective, setting_advantage_normalization, setting_reward_scheme],
)

grpo_verif_conditioning = claim(
    "In GRPO-Verif, verification responses are generated conditioned on both the question $q$ "
    "and the corresponding solution $y^{(i)}$: the model produces $v^{(i)} \\sim \\pi_\\theta(\\cdot | q, y^{(i)})$. "
    "This conditioning ensures that the verification task is specific to each solution, "
    "not a generic assessment of the question.",
    title="Verification conditioned on question and solution",
    background=[setting_verification_definition],
)

alpha_hyperparameter = claim(
    "The verification weight hyperparameter $\\alpha$ in GRPO-Verif is set to 0.2 in all experiments. "
    "This value was chosen to provide a meaningful verification training signal while ensuring that "
    "the solution generation objective remains the dominant term in the joint loss.",
    title="Alpha hyperparameter value",
    background=[grpo_verif_objective],
)

grpo_verif_no_critic = claim(
    "GRPO-Verif requires no separate critic or reward model for verification. "
    "Both solution rewards and verification rewards are computed using rule-based correctness "
    "checks (comparing model outputs against ground-truth answers), making the approach "
    "fully self-contained without learned value functions.",
    title="GRPO-Verif is critic-free",
    background=[setting_grpo_definition],
)

grpo_verif_addresses_gap = claim(
    "GRPO-Verif directly addresses the self-verification gap by making verification an "
    "explicit training objective within the RL framework, using the same policy gradient "
    "mechanism as solution generation. This avoids the distribution shift problem of "
    "SFT-based verification training.",
    title="GRPO-Verif addresses verification gap without distribution shift",
    background=[setting_grpo_definition, setting_verification_definition],
)
