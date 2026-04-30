"""Section 4.3: End-to-End RL Training with PRM"""

from gaia.lang import claim, setting, support
from .s2_architecture import setup_ternary_reward

# ── Settings: RL training setup ───────────────────────────────────────────────

setup_grpo = setting(
    "DataPRM uses Group Relative Policy Optimization (GRPO) with clip-higher and "
    "token-level loss for stable optimization. The total reward combines outcome "
    "and process rewards: $r_{\\text{total}} = (1-\\beta) \\cdot r_{\\text{outcome}} "
    "+ \\beta \\cdot (\\frac{1}{T}\\sum_{t=1}^{T} r_{\\text{prm}}(\\tau_t))$. "
    "A consistency check enforces that the PRM's last-step estimate aligns with "
    "the outcome reward.",
    title="GRPO with combined outcome-process reward"
)

setup_consistency_check = setting(
    "When the PRM's final-step estimate $r_{prm}(\\tau_T)$ disagrees with the "
    "outcome reward $r_{outcome}$, the PRM score is overridden by the outcome "
    "reward. This prevents the model from learning from conflicting signals at "
    "trajectory termination.",
    title="Consistency check at trajectory end"
)

# ── Claims: RL training results ───────────────────────────────────────────────

claim_process_beats_outcome = claim(
    "Models trained with process-supervised rewards (DataPRM) achieve 78.73% on "
    "DABench and 64.84% on TableBench, outperforming both SFT models and models "
    "trained with outcome-only rewards. Process supervision provides a more "
    "informative training signal than outcome supervision alone.",
    title="Process reward outperforms outcome-only reward in RL",
    metadata={"figure": "artifacts/2604.24198.pdf, Figure 5(a)"}
)

claim_no_entropy_collapse = claim(
    "Training with outcome-only rewards causes entropy collapse: after 200 steps, "
    "entropy decreases to approximately 0.12 and reward ceases to increase. "
    "Training with process-supervised rewards avoids this: entropy remains around "
    "0.18 and reward continues rising steadily. More fine-grained rewards enable "
    "more thorough exploration.",
    title="Process reward prevents entropy collapse",
    metadata={"figure": "artifacts/2604.24198.pdf, Figure 5(b)(c)"}
)

claim_pass3_improvement = claim(
    "The model trained with process-supervised rewards shows increased pass@3 "
    "(multi-sample accuracy), while outcome-only trained model shows no growth "
    "in pass@3. Consistently high entropy maintained during process-supervised "
    "training likely contributes to this improvement.",
    title="Process reward improves pass@3 via sustained exploration"
)

# ── Connect claims ────────────────────────────────────────────────────────────

# claim_process_beats_outcome and claim_no_entropy_collapse are leaf claims —
# their priors are assigned in priors.py.

strat_pass3 = support(
    [claim_no_entropy_collapse],
    claim_pass3_improvement,
    reason=(
        "Higher sustained entropy (@claim_no_entropy_collapse) means the model "
        "maintains diverse exploration strategies throughout training. This "
        "diversity directly translates to higher pass@3 — when sampling 3 "
        "trajectories, the model is more likely to include a correct one because "
        "it hasn't collapsed into a narrow strategy."
    ),
    prior=0.82
)
