"""Section 4: Related Work"""

from gaia.lang import claim, setting

from .motivation import sft_limitation, verification_training_neglect
from .s2_method import grpo_verif_no_critic

# --- Related work context ---

setting_ppo_based_verification = setting(
    "PPO (Proximal Policy Optimization)-based approaches to LLM training use a separate "
    "critic (value network) to estimate state values during policy optimization. "
    "RISE is an example that incorporates verification into PPO training using unified "
    "batches and a shared critic.",
    title="PPO-based verification approaches",
)

setting_star_approach = setting(
    "STaR (Self-Taught Reasoner) and similar bootstrapping approaches train LLMs to "
    "generate their own rationales, then use correct rationales as supervised training data. "
    "These approaches do not use RL but rely on iterative SFT.",
    title="STaR bootstrapping approach",
)

related_rise_comparison = claim(
    "RISE incorporates self-verification into PPO-based LLM training using unified training "
    "batches and a shared critic network. Unlike GRPO-Verif, RISE requires a critic model, "
    "making it more complex and computationally expensive. GRPO-Verif achieves verification "
    "improvement without a critic by using group-normalized advantages.",
    title="RISE vs GRPO-Verif comparison",
    background=[setting_ppo_based_verification, grpo_verif_no_critic],
)

related_prm_distinction = claim(
    "Process Reward Models (PRMs) provide step-level verification feedback by training a "
    "separate model to score intermediate reasoning steps. GRPO-Verif differs from PRM "
    "approaches in that it trains the same model to both solve and verify, without a "
    "separate step-level reward model.",
    title="PRM vs GRPO-Verif distinction",
)

related_sft_distinction = claim(
    "Prior SFT-based verification methods (e.g., methods using error correction datasets) "
    "train verification capability separately from solution generation, creating a distribution "
    "gap between the SFT training data and the RL policy. GRPO-Verif avoids this gap by "
    "training both objectives jointly within the same RL loop.",
    title="SFT vs GRPO-Verif: distribution alignment",
    background=[sft_limitation],
)

related_novelty = claim(
    "GRPO-Verif is novel in three respects relative to prior work: "
    "(1) it treats problem-solving and verification as integrated rather than separate tasks, "
    "(2) it uses critic-free GRPO instead of PPO-based approaches requiring a separate value function, "
    "(3) it explicitly weights the verification loss as an auxiliary objective with hyperparameter $\\alpha$, "
    "enabling systematic study of verification's impact on both accuracy dimensions.",
    title="Novelty relative to prior work",
)
