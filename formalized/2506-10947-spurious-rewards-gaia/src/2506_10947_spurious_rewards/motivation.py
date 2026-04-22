"""Introduction and Motivation: Spurious Rewards in RLVR"""

from gaia.lang import (
    claim, setting, question,
    support, deduction,
)

# ── Settings: background context ──────────────────────────────────────────────

setup_rlvr = setting(
    "Reinforcement learning with verifiable rewards (RLVR) is a post-training "
    "technique that uses binary (0/1) reward signals based on whether a model "
    "rollout produces a verifiably correct answer. GRPO (Group Relative Policy "
    "Optimization) is the specific RL algorithm used in this paper, which "
    "normalizes rewards to a group-relative advantage $\\hat{A}(x,y) = "
    "(r(x,y) - \\bar{r}_x) / \\sigma_x$, where $\\bar{r}_x$ is the group-wise "
    "mean reward and $\\sigma_x$ is the standard deviation over rollouts for "
    "prompt $x$. The KL penalty weight is set to $\\lambda = 0$ in all "
    "experiments.",
    title="RLVR and GRPO setup",
)

setup_models = setting(
    "Experiments are conducted on Qwen2.5-Math-7B and Qwen2.5-Math-1.5B "
    "(math-specialized, Yang et al. 2024a), Qwen2.5-7B and Qwen2.5-1.5B "
    "(general-purpose, Yang et al. 2024b), OLMo2-7B and OLMo2-7B-SFT "
    "(OLMo team 2024), and Llama3.1-8B(-Instruct) and Llama3.2-3B(-Instruct) "
    "(Dubey et al. 2024). Training uses GRPO on DeepScaleR data (Luo et al. "
    "2025b) for 300 steps with 8 A100 GPUs, learning rate 5e-7, rollout batch "
    "size 64, mini batch size 128, 16 rollouts per prompt.",
    title="Models and training configuration",
)

setup_benchmarks = setting(
    "Performance is evaluated on MATH-500 (pass@1; Hendrycks et al. 2021), "
    "AMC (average@8), and AIME 2024/2025 (average@8). The default official "
    "system prompt from Yang et al. (2024a) is used for Qwen2.5-Math models; "
    "no system prompt is used for other models; no user prompt is used for any "
    "model in the main experiments.",
    title="Evaluation benchmarks and prompts",
)

setup_reward_types = setting(
    "Five reward functions are studied: "
    "(1) Ground Truth Reward: binary reward for verifiably correct answer — upper bound for supervision quality. "
    "(2) Majority Vote Reward: pseudo-labels from majority answer across 64 pre-RLVR rollouts per prompt. "
    "(3) Format Reward: reward if response contains at least one non-empty \\\\boxed{} expression, regardless of correctness. "
    "(4) Random Reward: reward of 1 assigned with fixed probability $\\gamma$ (default $\\gamma=0.5$), independent of rollout content. "
    "(5) Incorrect Reward: majority-vote labels are used but only the subset with wrong labels is kept; reward for matching these incorrect labels.",
    title="Reward function taxonomy: ground truth, majority vote, format, random, incorrect",
)

# ── Research question ──────────────────────────────────────────────────────────

q_spurious = question(
    "Can reinforcement learning with verifiable rewards (RLVR) improve "
    "mathematical reasoning performance using reward signals that have little, "
    "no, or even negative correlation with the correct answer?",
    title="Core research question: can spurious rewards improve math reasoning?",
)

q_model_dependency = question(
    "Do the effects of weak or spurious rewards in RLVR generalize across "
    "different model families, or are they specific to particular pretraining "
    "distributions?",
    title="Research question: model-dependency of spurious reward effects",
)

q_mechanism = question(
    "What mechanism explains why certain models respond to spurious rewards "
    "while others do not?",
    title="Research question: mechanism of spurious reward effectiveness",
)

# ── Claims from the Introduction ──────────────────────────────────────────────

claim_rlvr_improves_qwen = claim(
    "RLVR with spurious rewards (format reward, random reward, incorrect label "
    "reward) significantly improves MATH-500 performance on Qwen2.5-Math-7B. "
    "Specifically, absolute accuracy gains from 300 GRPO training steps are: "
    "+21.4 pp (random reward, $\\gamma=0.5$), +13.8 pp (format reward), "
    "+24.1 pp (incorrect label reward), +26.0 pp (one-shot RL), +27.1 pp "
    "(majority vote) — compared to +29.1 pp from ground-truth rewards. "
    "Starting accuracy before RLVR: 49.4% on MATH-500.",
    title="Spurious rewards yield significant MATH-500 gains on Qwen2.5-Math-7B",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 1 and Figure 2a"},
)

claim_spurious_fails_non_qwen = claim(
    "Spurious rewards (random, incorrect label) that produce large MATH-500 "
    "gains on Qwen models generally fail to improve or actively harm performance "
    "on other model families. On Llama3.1-8B-Instruct (baseline 36.8%), random "
    "reward yields -6.4 pp, incorrect label yields -8.3 pp, format reward -2.1 "
    "pp, and only ground truth (+15.5 pp) and majority vote (+7.4/+7.2 pp) "
    "produce improvements. OLMo2-7B (baseline 9.0%) shows -6.4 pp from random, "
    "-8.3 pp from incorrect label, and only +16.7 pp from ground truth.",
    title="Spurious rewards fail or hurt non-Qwen models (Llama, OLMo2)",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 1 and Figure 3"},
)

claim_pretraining_hypothesis = claim(
    "The hypothesis that RLVR, at the compute scales of open-source "
    "post-training pipelines, does not teach models fundamentally new reasoning "
    "capabilities, but instead surfaces latent reasoning representations learned "
    "during pretraining. The effectiveness of spurious rewards is therefore "
    "contingent on pre-existing model capabilities aligned with the task.",
    title="RLVR surfaces pretrained latent capabilities rather than teaching new ones",
)

claim_qwen_centric_risk = claim(
    "A significant fraction of recent RLVR research draws conclusions "
    "exclusively or primarily from gains on Qwen2.5-Math-7B — a model for which "
    "even completely spurious reward signals (random reward, incorrect label) "
    "can yield gains of 21-24 percentage points on MATH-500. This creates a "
    "risk that proposed RLVR methods appear effective primarily due to the "
    "Qwen2.5-Math model's unique properties rather than the methods themselves.",
    title="Qwen-centric RLVR research may overestimate method effectiveness",
)

# ── Reasoning strategies ──────────────────────────────────────────────────────

strat_spurious_qwen_observation = support(
    [claim_rlvr_improves_qwen],
    claim_pretraining_hypothesis,
    reason=(
        "The observation (@claim_rlvr_improves_qwen) that even reward signals "
        "with zero or negative correlation to ground truth can yield ~21-27 pp "
        "gains on MATH-500 supports the interpretation that the reward signal "
        "itself is not the primary driver of improvement. Since the reward is "
        "uninformative about answer correctness, the optimization must be "
        "exploiting pre-existing model structure. This motivates "
        "@claim_pretraining_hypothesis that RLVR surfaces latent pretraining "
        "representations. [@Shao2025spurious]"
    ),
    prior=0.8,
    background=[setup_reward_types],
)

strat_non_qwen_contrast = support(
    [claim_spurious_fails_non_qwen],
    claim_pretraining_hypothesis,
    reason=(
        "The sharp contrast between Qwen models (large spurious-reward gains) "
        "and Llama/OLMo2 models (flat or negative results under identical "
        "reward signals, @claim_spurious_fails_non_qwen) is consistent with "
        "@claim_pretraining_hypothesis: the effectiveness depends on what the "
        "model learned during pretraining. Models from the same training family "
        "show similar trends, implicating pretraining data distribution as the "
        "key variable."
    ),
    prior=0.85,
    background=[setup_models],
)
