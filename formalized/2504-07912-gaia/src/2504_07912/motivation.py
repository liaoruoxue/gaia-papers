"""Introduction and Motivation — Echo Chamber: RL Post-training Amplifies Behaviors Learned in Pretraining"""

from gaia.lang import claim, setting, question, support, contradiction

# ── Settings ────────────────────────────────────────────────────────────────

rl_posttraining_definition = setting(
    "Reinforcement learning (RL) post-training refers to fine-tuning a pretrained language model "
    "using RL algorithms (e.g., PPO, GRPO, Expert Iteration) with a reward signal derived from "
    "correctness of generated outputs. In mathematical reasoning, the reward is typically binary: "
    "+1 if the final answer is correct, 0 otherwise.",
    title="RL post-training definition",
)

pretraining_mixture_definition = setting(
    "A pretraining mixture is a weighted combination of multiple distinct data sources, each with "
    "its own statistical properties, formatting conventions, and solution styles. For mathematical "
    "reasoning, typical sources include document corpora (e.g., FineMath, Proof-Pile) and "
    "instruction datasets (e.g., TinyGSM, OpenMathInstruct).",
    title="Pretraining mixture definition",
)

kl_regularization_definition = setting(
    "KL regularization in RL fine-tuning penalises the policy for diverging from a reference "
    "policy (typically the pretrained model) by adding $-\\beta \\cdot D_{\\text{KL}}(\\pi \\| \\pi_{\\text{ref}})$ "
    "to the RL objective, where $\\beta > 0$ is the KL coefficient. "
    "This keeps the fine-tuned policy close to the pretrained distribution.",
    title="KL regularization definition",
)

controlled_pretraining_setup = setting(
    "This paper trains OLMo decoder-only transformer models entirely from scratch on open, "
    "documented datasets. Scales tested: 150 million (M) parameters (width 768, depth 12 layers) "
    "and 1 billion (B) parameters (width 2048, depth 16 layers), both using SwiGLU activations "
    "and Rotary Positional Encoding (RoPE). All pretraining data sources and mixing ratios are "
    "explicitly recorded, eliminating hidden pretraining confounds present when starting from "
    "externally released checkpoints.",
    title="Controlled from-scratch pretraining setup",
)

# ── Research Questions ───────────────────────────────────────────────────────

q_rl_mechanism = question(
    "Does RL post-training introduce genuinely new capabilities, or does it primarily amplify "
    "and refine behaviors already present in the pretrained model?"
)

q_scale_dependence = question(
    "How does the effect of RL post-training on distributional format and performance vary "
    "with model scale (e.g., 150M vs. 1B parameters)?"
)

q_algorithm_sensitivity = question(
    "How sensitive are RL post-training outcomes to the choice of RL algorithm "
    "(PPO vs. GRPO vs. Expert Iteration)?"
)

# ── Motivation Claims ────────────────────────────────────────────────────────

opacity_problem = claim(
    "Most existing studies of RL post-training for reasoning (e.g., DeepSeek-R1 [@DeepSeek2025]) "
    "begin from large models with proprietary or undocumented pretraining data, making it "
    "impossible to isolate RL's contribution from the unknown pretraining initialization. "
    "This opacity confounds attribution of observed capability gains.",
    title="Opacity problem in existing RL studies",
    metadata={"source_section": "Introduction"},
)

controlled_study_value = claim(
    "Training models from scratch on fully documented, open datasets enables a controlled study "
    "of RL post-training: any behavioral change observed after RL can be attributed to the RL "
    "algorithm rather than to unknown pretraining factors. "
    "This is the methodological contribution of the present work [@Zhao2025].",
    title="Value of controlled from-scratch study",
    metadata={"source_section": "Introduction"},
)

strat_controlled_study = support(
    [opacity_problem],
    controlled_study_value,
    reason=(
        "Because existing studies cannot disentangle RL effects from unknown pretraining "
        "(@opacity_problem), a controlled experiment that trains entirely from scratch "
        "(@controlled_pretraining_setup) is the appropriate remedy. "
        "The value of @controlled_study_value follows directly from this gap."
    ),
    prior=0.92,
    background=[controlled_pretraining_setup],
)

echo_chamber_hypothesis = claim(
    "RL post-training acts as an 'echo chamber': it amplifies distributional modes already "
    "present in pretraining data rather than introducing new reasoning strategies or knowledge. "
    "The model's post-RL behavior reflects what was already latent in pretraining, but "
    "concentrated and refined [@Zhao2025].",
    title="Echo chamber hypothesis (central claim)",
    metadata={"source_section": "Introduction"},
)

# Exported conclusions
__all__ = ["echo_chamber_hypothesis", "controlled_study_value", "opacity_problem"]
