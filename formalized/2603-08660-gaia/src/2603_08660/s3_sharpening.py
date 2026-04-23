"""Section 3: The Sharpening Mechanism of Intrinsic Rewards"""

from gaia.lang import claim, setting, support, deduction

from .motivation import intrinsic_rewards_definition, urlvr_definition
from .s2_taxonomy import certainty_rewards_overview, ensemble_rewards_overview

# ─── Mathematical setup ───────────────────────────────────────────────────────

kl_regularized_rl = setting(
    "The standard KL-regularized RL objective for LLM training is:\n\n"
    "$$\\max_{\\pi_\\theta} \\mathbb{E}_{y \\sim \\pi_\\theta(\\cdot|x)}[r(x,y)] "
    "- \\beta D_{\\mathrm{KL}}[\\pi_\\theta(\\cdot|x) \\| \\pi_{\\mathrm{ref}}(\\cdot|x)]$$\n\n"
    "where $\\pi_{\\mathrm{ref}}$ is the reference (initial) policy and $\\beta > 0$ controls "
    "the KL regularization strength. The optimal policy has the closed-form solution: "
    "$\\pi^*_\\theta(y|x) = \\frac{1}{Z(x)} \\pi_{\\mathrm{ref}}(y|x) \\exp\\left(\\frac{r(x,y)}{\\beta}\\right)$ "
    "where $Z(x)$ is the partition function.",
    title="KL-regularized RL objective",
)

majority_voting_reward = setting(
    "The majority voting reward used in TTRL at iteration $k$ is defined as: "
    "$r_k(x,y) = \\mathbf{1}[\\mathrm{ans}(y) = \\mathrm{maj}_k(Y_k)]$ "
    "where $Y_k = \\{y_i\\}_{i=1}^N$ are $N$ rollouts sampled from $\\pi^{(k)}_\\theta$, "
    "and $\\mathrm{maj}_k(Y_k)$ is the majority answer among those rollouts. "
    "This is a binary reward: 1 if the answer matches the majority, 0 otherwise.",
    title="TTRL majority voting reward",
)

# ─── One-step update dynamics ────────────────────────────────────────────────

one_step_update_dynamics = claim(
    "A single gradient step with the majority voting reward creates a 'rich-get-richer' dynamic: "
    "trajectories leading to the majority answer have their probabilities consistently increased, "
    "while others are proportionally diminished. After one step, the probability mass on majority "
    "trajectories increases from $p^{(k)}_{\\mathrm{maj}}$ to $p^{(k+1)}_{\\mathrm{maj}} \\geq p^{(k)}_{\\mathrm{maj}}$, "
    "and this holds under two empirically validated assumptions: "
    "(A1) majority stability—the majority answer remains the same across iterations for large $N$—and "
    "(A2) effective learning—the gradient step increases probability of the rewarded answer.",
    title="One-step update rich-get-richer dynamics",
    background=[kl_regularized_rl, majority_voting_reward],
)

# ─── Geometric convergence theorem ───────────────────────────────────────────

theorem1_sharpening = claim(
    "**Theorem 1 (Geometric Convergence to Deterministic Policy):** Under the KL-regularized RL "
    "objective with majority voting reward, and assuming (A1) majority stability and (A2) effective "
    "learning, the probability mass on majority trajectories $p^{(k)}_{\\mathrm{maj}}$ converges "
    "geometrically to 1 with rate $\\rho = e^{-1/\\beta}$. The limiting policy is:\n\n"
    "$$\\lim_{k\\to\\infty} \\pi^{(k)}_\\theta(y|x) = \\begin{cases} "
    "\\frac{\\pi_{\\mathrm{ref}}(y|x)}{\\sum_{y': \\mathrm{ans}(y')=\\mathrm{maj}_0(Y_0)} \\pi_{\\mathrm{ref}}(y'|x)} "
    "& \\text{if } \\mathrm{ans}(y) = \\mathrm{maj}_0(Y_0) \\\\ "
    "0 & \\text{otherwise} \\end{cases}$$\n\n"
    "This means training converges to a deterministic policy concentrated on whatever answer had "
    "the initial majority—regardless of whether that answer is correct.",
    title="Theorem 1: Geometric convergence / sharpening",
    background=[kl_regularized_rl, majority_voting_reward],
)

strat_theorem1 = deduction(
    [one_step_update_dynamics],
    theorem1_sharpening,
    reason=(
        "Starting from the one-step update dynamics (@one_step_update_dynamics) showing that "
        "majority-trajectory probability increases monotonically under assumptions A1 and A2, "
        "iterating this update yields geometric convergence with rate $\\rho = e^{-1/\\beta}$ "
        "(derived from the closed-form optimal policy of the KL-regularized objective). "
        "The limiting policy is the reference policy renormalized to the initial majority "
        "answer's support. This is a mathematical consequence of the KL-regularized RL setup "
        "and does not depend on specifics of the reward's accuracy. Proof in Appendix A.2."
    ),
    prior=0.96,
    background=[kl_regularized_rl, majority_voting_reward],
)

# ─── Generalization to all intrinsic methods ─────────────────────────────────

unified_sharpening_framework = claim(
    "All intrinsic URLVR reward methods—both certainty-based and ensemble-based—can be understood "
    "through a unified lens: they all manipulate the cross-entropy between carefully chosen "
    "distributions in a way that sharpens the model's initial distribution. Despite diverse design "
    "choices (different reward formulas in Tables 1 and 2), all intrinsic methods converge toward "
    "sharpening the model's initial distribution, amplifying existing preferences rather than "
    "discovering new knowledge. This is formalized in a Unified Reward Framework (Appendix A.3) "
    "that covers all variants and shows the same geometric convergence behavior.",
    title="Unified sharpening mechanism for all intrinsic methods",
)

strat_unified_sharpening = support(
    [theorem1_sharpening, certainty_rewards_overview, ensemble_rewards_overview],
    unified_sharpening_framework,
    reason=(
        "Theorem 1 (@theorem1_sharpening) establishes sharpening for majority voting. "
        "The Unified Reward Framework (Appendix A.3 of the paper) extends this by showing "
        "that both certainty-based rewards (@certainty_rewards_overview) and ensemble-based "
        "rewards (@ensemble_rewards_overview), despite different formulas, all reduce to "
        "cross-entropy manipulation that amplifies the model's initial distribution. "
        "The generalized convergence analysis (Appendix A.4) confirms this for each variant, "
        "providing optimal policies for each reward type in Appendix A.5."
    ),
    prior=0.87,
)

# ─── The confidence-correctness alignment condition ──────────────────────────

sharpening_dual_nature = claim(
    "The sharpening mechanism has a dual nature depending on confidence-correctness alignment: "
    "(1) **When alignment is high** (initial confidence correctly predicts answer quality), "
    "sharpening acts as a beneficial amplifier—it concentrates probability on already-correct "
    "answers, improving performance. "
    "(2) **When alignment is low** (initial confidence is poorly calibrated), sharpening "
    "systematically reinforces errors—it concentrates probability on incorrect majority answers, "
    "leading to model collapse. "
    "The same mathematical mechanism thus produces both improvement and degradation, depending "
    "entirely on the quality of the initial model prior.",
    title="Dual nature of sharpening: alignment determines outcome",
)

strat_dual_nature = deduction(
    [theorem1_sharpening],
    sharpening_dual_nature,
    reason=(
        "Theorem 1 (@theorem1_sharpening) shows convergence concentrates on the *initial* majority "
        "answer $\\mathrm{maj}_0(Y_0)$, not necessarily on the correct answer. If the model's "
        "initial distribution assigns highest probability mass to the correct answer "
        "(confidence-correctness alignment), then $\\mathrm{maj}_0$ is correct and convergence "
        "is beneficial. If the model initially prefers wrong answers, then $\\mathrm{maj}_0$ is "
        "wrong and the same convergence amplifies errors. This bifurcation follows directly from "
        "the theorem."
    ),
    prior=0.95,
)
