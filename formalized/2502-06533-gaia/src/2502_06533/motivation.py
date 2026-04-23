"""Introduction and Motivation"""

from gaia.lang import claim, setting, question, support

# --- Background settings ---

mdp_formulation = setting(
    "The RL fine-tuning task is formalized as an MDP $\\mathcal{M}=(\\mathcal{S},\\mathcal{A},\\mathcal{T},\\mathcal{R})$ "
    "where $\\mathcal{A}$ is the vocabulary (one token per step), states $s_t \\in \\mathcal{S}$ "
    "represent generated text sequences, the reward $\\mathcal{R}$ is 1 for a correct final answer and 0 otherwise "
    "(sparse reward), and the goal is to find $\\pi^* = \\arg\\max_{\\pi} \\mathbb{E}[\\sum_t \\mathcal{R}(s_t)]$.",
    title="MDP formulation of LLM RL fine-tuning",
)

kl_penalty_def = setting(
    "The standard KL penalty in RL fine-tuning of language models is "
    "$\\mathcal{L}_{\\mathrm{KL}} = \\mathbb{E}[\\log(\\pi_\\theta(a|s)/\\pi_{\\theta_{\\mathrm{old}}}(a|s))]$, "
    "which penalizes divergence of the current policy $\\pi_\\theta$ from the reference (old) policy $\\pi_{\\theta_{\\mathrm{old}}}$ "
    "and is commonly approximated as $(\\log p(x) - \\log q(x))^2/2$.",
    title="Standard KL penalty definition",
)

negentropy_def = setting(
    "The normalized negentropy (confidence measure) for a policy $\\pi$ at state $s$ is defined as "
    "$\\hat{J}_{\\theta_{\\mathrm{old}}}(s) = (H_{\\mathrm{max}} - H(\\pi_{\\theta_{\\mathrm{old}}}(\\cdot|s))) / H_{\\mathrm{max}}$, "
    "where $H$ denotes Shannon entropy and $H_{\\mathrm{max}} = \\log|\\mathcal{A}|$ is the maximum possible entropy "
    "over the vocabulary $\\mathcal{A}$. This measure is bounded in $[0,1]$: it equals 1 when the model is maximally "
    "confident (deterministic) and 0 when maximally uncertain (uniform).",
    title="Normalized negentropy definition",
)

arithmetic_task_setup = setting(
    "Experiments use GPT-2 (85M parameters) with a character-level tokenizer trained on "
    "N-digit addition problems. Pre-training uses supervised learning on additions with operand "
    "lengths 1 to N digits; RL fine-tuning is performed on N+1 or N+2 digit additions "
    "(out-of-distribution with respect to pre-training). "
    "Two evaluation modes are used: (1) fixed-digit: both operands have exactly N digits; "
    "(2) varying-digit: one operand has N digits, the other has fewer. "
    "The RL algorithm is A2C (Advantage Actor-Critic).",
    title="Experimental setup: GPT-2 arithmetic task",
)

# --- Core motivating claims ---

rl_finetuning_challenge = claim(
    "Fine-tuning large language models (LLMs) with reinforcement learning (RL) to achieve "
    "long-term goals is challenging because it requires balancing exploration of novel solutions "
    "against preservation of pre-trained capabilities. Standard KL divergence penalties are used "
    "to prevent the policy from deviating too far from the reference model, but this constrains "
    "exploration in out-of-distribution situations.",
    title="RL fine-tuning exploration challenge",
)

pretrain_breadth_impacts_exploration = claim(
    "The breadth of pre-training (i.e., the range of operand digit lengths seen during "
    "supervised pre-training) plays an ambivalent role in RL exploration: more extensive "
    "pre-training improves baseline generalization but may reduce the incentive to explore "
    "during RL fine-tuning because fewer errors are initially encountered.",
    title="Pre-training breadth has ambivalent effect on exploration",
)

sparse_reward_difficulty = claim(
    "Sparse reward settings—where the model only receives a reward of 1 for a fully correct "
    "answer and 0 otherwise—make credit assignment difficult in LLM RL fine-tuning, "
    "because many intermediate steps contribute to the final outcome but receive no "
    "intermediate reward signal.",
    title="Sparse reward complicates credit assignment",
)

# --- Strategies ---

strat_sparse_reward = support(
    [sparse_reward_difficulty],
    rl_finetuning_challenge,
    reason=(
        "The @sparse_reward_difficulty (only correct final answers are rewarded) is a key "
        "driver of @rl_finetuning_challenge: without intermediate reward signals, the policy "
        "must explore widely to find any correct trajectory, and the KL penalty then limits "
        "this exploration. Sparse reward makes the exploration-preservation tradeoff acute."
    ),
    prior=0.82,
    background=[mdp_formulation],
)

# --- Research question ---

rq_critical_tokens = question(
    "Which tokens in a language model's output are 'critical'—i.e., decisive for whether "
    "the final answer is correct—and can a modified KL penalty that focuses exploration on "
    "these critical tokens improve RL fine-tuning efficiency?"
)
