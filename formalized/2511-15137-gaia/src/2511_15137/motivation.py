"""Introduction and Motivation: Self-Verification Gap in LLM Reasoning"""

from gaia.lang import claim, setting, question

# --- Background settings ---

setting_rl_reasoning = setting(
    "Large language models (LLMs) have demonstrated strong mathematical reasoning "
    "capabilities when trained with reinforcement learning (RL) algorithms such as "
    "Group Relative Policy Optimization (GRPO). RL-based training optimizes LLMs to "
    "produce correct final answers to mathematical problems.",
    title="RL improves LLM reasoning",
)

setting_grpo_definition = setting(
    "Group Relative Policy Optimization (GRPO) is an RL algorithm for LLMs that: "
    "(1) samples n candidate solutions per problem, "
    "(2) assigns rewards based on answer correctness (+1 correct, -1 incorrect, -1.5 invalid), "
    "(3) normalizes advantages within the group using mean and standard deviation, "
    "(4) optimizes the policy using a clipped PPO-style objective with optional KL divergence penalty. "
    "GRPO is critic-free — it does not require a separate value network.",
    title="GRPO definition",
)

setting_verification_definition = setting(
    "Self-verification in LLMs refers to the capability of a model to assess the "
    "correctness of its own generated reasoning trace, given the original question and "
    "the solution. A verifier outputs whether the solution is correct or incorrect. "
    "Self-verification differs from process reward modeling (PRM) in that it uses the "
    "model itself as the verifier without a separate trained critic.",
    title="Self-verification definition",
)

# --- Core motivation claims ---

verification_gap = claim(
    "Despite improvements in mathematical problem-solving through RL training, "
    "LLMs still struggle to consistently verify their own reasoning traces. "
    "Models trained purely to maximize solution correctness do not automatically "
    "develop reliable self-verification capabilities.",
    title="Self-verification gap in RL-trained LLMs",
)

verification_training_neglect = claim(
    "Existing RL-based training approaches for LLMs (such as GRPO) optimize exclusively "
    "for solution generation correctness and do not explicitly train the model to verify "
    "whether a given solution is correct. Verification ability is treated as a byproduct "
    "rather than an explicit training objective.",
    title="Verification neglected in existing RL training",
)

sft_limitation = claim(
    "Prior approaches that incorporate verification into LLM training rely on supervised "
    "fine-tuning (SFT) with error correction data. SFT-based verification training introduces "
    "distribution shift between the SFT data distribution and the RL policy distribution, "
    "which can degrade the quality of the learned policy.",
    title="SFT-based verification causes distribution shift",
)

research_question_tradeoff = claim(
    "It is unclear whether jointly training an LLM for both solution generation and "
    "self-verification improves or hinders reasoning performance. The two objectives may "
    "compete for model capacity, potentially causing a tradeoff where gains in verification "
    "accuracy come at the cost of solution accuracy.",
    title="Open question: joint training tradeoff",
)

core_contribution = claim(
    "The paper introduces GRPO-Verif, an extension of GRPO that jointly optimizes "
    "solution generation and self-verification through a single unified RL loss function, "
    "without relying on supervised fine-tuning or a separate critic model.",
    title="GRPO-Verif contribution",
)
