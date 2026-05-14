"""Section 2: Reinforcement Learning and Reasoning -- formal RL preliminaries
for LLM reasoning, GRPO objective and advantage definition, format/correctness
rewards in the DeepSeek-R1 line of work.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 2, p. 2-3.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Background setup: the RL-reasoning paradigm
# ---------------------------------------------------------------------------

setup_rl_reasoning_paradigm = setting(
    "**RL reasoning paradigm.** Scaling LLM test-time compute is driven by "
    "the reinforcement-learning 'reasoning' paradigm "
    "[@Jaech2024OpenAIO1; @Guo2025DeepSeekR1; @MetaAI2025Llama4; "
    "@Yang2025Qwen3; @Comanici2025Gemini25], a new stage of training "
    "introduced by the DeepSeek-R1 line of work "
    "[@Wang2023MathShepherd; @Shao2024DeepSeekMath; @Guo2025DeepSeekR1]. "
    "An LLM $\\pi_\\theta$ is optimized by making it generate completions "
    "$o_i$ to a set of verifiable problems "
    "$\\mathcal{D} = \\{(q_1, s_1), \\dots, (q_N, s_N)\\}$ with a custom "
    "system prompt instructing the model to wrap its thinking trace and "
    "final solution in `<think>` and `<solution>` tags.",
    title="Setup: RL reasoning paradigm -- verifiable problems, format-tagged completions, custom system prompt",
)

setup_reward_definition = setting(
    "**Two-condition reward function in the RL reasoning paradigm.** For "
    "each output $o_i$, the reward $r_i$ is determined by:\n\n"
    "1. **Format condition** -- $r_i = -1$ for outputs that do not adhere "
    "to the `<think>` / `<solution>` format.\n"
    "2. **Correctness condition** -- $r_i = 1$ if the correctly formatted "
    "output matches the gold solution $s_i$, and $r_i = -0.5$ otherwise "
    "(format-correct but answer-wrong).",
    title="Setup: two-condition reward (format=-1; correct=1; correct-format-wrong-answer=-0.5)",
)

setup_grpo_objective = setting(
    "**GRPO objective.** GRPO [@Shao2024DeepSeekMath] is a simple online "
    "RL algorithm that uses $\\pi_\\theta$ to generate $G > 1$ grouped "
    "completions $\\{o_1, \\dots, o_G\\}$ per question $q$. For $\\beta "
    "\\geq 0$ and KL penalty to a reference model "
    "$D_{KL}(\\cdot \\| \\pi_{ref})$, the optimization objective "
    "(Equation 1 of the paper) is the KL-discounted clipped policy "
    "maximization:\n\n"
    "$$J(\\theta) = \\mathbb{E}_{q \\sim \\mathcal{D}, \\{o\\}_{1}^{G} "
    "\\sim \\pi_\\theta(\\cdot|q)} \\left[ \\frac{1}{G} \\sum_{i=1}^{G} "
    "\\min\\left( r_i A_i, \\mathrm{clip}(r_i, 1-\\epsilon, 1+\\epsilon) "
    "A_i \\right) - \\beta D_{KL}(\\pi_\\theta \\| \\pi_{ref}) \\right]$$",
    title="Setup: GRPO objective (Equation 1) -- KL-discounted clipped grouped-completion policy maximization",
)

setup_grpo_advantage = setting(
    "**GRPO advantage definition.** GRPO uses Monte-Carlo grouped "
    "completions to compute the advantage function "
    "[@Sutton1999PolicyGradient] (Equation 2):\n\n"
    "$$A_i = \\frac{r_i - \\mathrm{mean}(\\{r_1, \\dots, r_G\\})}"
    "{\\mathrm{std}(\\{r_1, \\dots, r_G\\})}$$\n\n"
    "Group-normalization eliminates the need for a separate value-function "
    "critic and provides a stable per-group reward baseline.",
    title="Setup: GRPO advantage (Equation 2) -- group-normalized reward minus mean over std",
)

# ---------------------------------------------------------------------------
# Established background claim: the recipe works
# ---------------------------------------------------------------------------

claim_grpo_yields_thinking = claim(
    "**Established background result.** The simple GRPO recipe specified "
    "in the system prompt has been shown to be effective at aligning the "
    "model with **self-emergent thinking capabilities**, yielding "
    "unprecedented task specialization in the DeepSeek-R1 line of work "
    "[@Guo2025DeepSeekR1; @Shao2024DeepSeekMath] and subsequent "
    "reasoning-style training of large-scale open and closed-source models "
    "[@Jaech2024OpenAIO1; @MetaAI2025Llama4; @Yang2025Qwen3; "
    "@Comanici2025Gemini25].",
    title="Background result: GRPO + format/correctness reward elicits self-emergent thinking and reasoning behaviors",
)

__all__ = [
    "setup_rl_reasoning_paradigm",
    "setup_reward_definition",
    "setup_grpo_objective",
    "setup_grpo_advantage",
    "claim_grpo_yields_thinking",
]
