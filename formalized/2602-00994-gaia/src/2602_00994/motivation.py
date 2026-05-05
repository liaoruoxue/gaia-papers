"""Motivation: ARL jointly optimizes reasoning + tool-use under a single objective.

Section 1 (Introduction) of Li et al. 2026 [@Li2026]. Frames the central
question: does joint training of two heterogeneous capabilities (reasoning and
tool-use) over shared parameters truly improve agent performance, or does it
induce competition between them?
"""

from gaia.lang import claim, setting, question

# ---------------------------------------------------------------------------
# Background settings (definitional / framing)
# ---------------------------------------------------------------------------

setup_arl = setting(
    "Agentic Reinforcement Learning (ARL) is a post-training paradigm in which "
    "a large language model (LLM) is trained to interleave internal reasoning "
    "with external tool execution (e.g. search, code execution, retrieval) in "
    "order to solve complex tasks. The model emits a single token sequence "
    "$\\tau = (c_1, \\ldots, c_T)$ that mixes reasoning tokens (free text "
    "chains of thought) and tool-use tokens (special-format commands such as "
    "`<search> ... </search>`). Most existing ARL methods optimize a single "
    "shared parameter set $\\theta$ on a single scalar reward objective.",
    title="Setup: Agentic RL",
)

setup_joint_assumption = setting(
    "The standard ARL paradigm implicitly assumes that reasoning and tool-use "
    "are **complementary** capabilities that can both be improved by sharing a "
    "single parameter space and a single training signal. This assumption "
    "underlies methods such as Toolformer [@Schick2023], DeepSeekMath "
    "[@Shao2024], and Search-R1 [@Jin2025], which apply one RL update per "
    "trajectory regardless of token role.",
    title="Setup: the joint-training assumption",
)

# ---------------------------------------------------------------------------
# Open question driving the paper
# ---------------------------------------------------------------------------

q_interference = question(
    "Does jointly optimizing reasoning and tool-use over a shared parameter "
    "space actually help, or does it cause the two capabilities to interfere "
    "with each other and degrade overall performance?",
    title="Does joint ARL training induce capability interference?",
)

# ---------------------------------------------------------------------------
# High-level claims established in the introduction (substantiated later)
# ---------------------------------------------------------------------------

claim_capabilities_are_heterogeneous = claim(
    "Reasoning tokens (which articulate logical inference in free text) and "
    "tool-use tokens (which emit structured commands triggering external "
    "side-effects) are functionally heterogeneous: they differ in vocabulary "
    "distribution, syntactic constraints, and the optimal next-token "
    "distribution conditional on context. A single shared parameter set must "
    "therefore service two qualitatively different conditional distributions.",
    title="Reasoning and tool-use are heterogeneous capabilities",
    background=[setup_arl],
)

claim_joint_assumption_unexamined = claim(
    "Despite its widespread adoption in ARL frameworks (Toolformer "
    "[@Schick2023], DeepSeekMath [@Shao2024], Search-R1 [@Jin2025], "
    "AgentTuning), the assumption that joint optimization of reasoning and "
    "tool-use over shared parameters improves overall performance has rarely "
    "been examined empirically.",
    title="The joint-training assumption is unexamined",
    background=[setup_joint_assumption],
)

# The implicit content of the assumption itself -- modelled separately so
# the LEAS interference finding can contradict it.
claim_joint_training_helps_assumed = claim(
    "**Implicit assumption underlying standard ARL.** Joint optimization "
    "of reasoning and tool-use over a single shared parameter set "
    "produces a net improvement in overall agent performance, relative "
    "to training the two capabilities separately. This is the assumption "
    "that the paper's LEAS analysis empirically tests.",
    title="Implicit ARL assumption: joint training improves overall performance",
    background=[setup_joint_assumption],
)

claim_seesaw_phenomenon = claim(
    "Under joint ARL optimization, reasoning and tool-use exhibit a clear "
    "**seesaw phenomenon** [@Yu2020]: improving the model's tool-use capability "
    "tends to degrade its reasoning capability and vice versa. This is the "
    "qualitative observation that motivates the paper.",
    title="Seesaw phenomenon: tool-use and reasoning trade off",
)

# ---------------------------------------------------------------------------
# Core contribution claims (high-level statements; details in s3-s6)
# ---------------------------------------------------------------------------

claim_contribution_leas = claim(
    "**Contribution 1 (LEAS).** The paper introduces the **Linear Effect "
    "Attribution System (LEAS)**, a diagnostic framework inspired by "
    "variance-based attribution [@Greene2003] that decomposes a model's "
    "question-level correctness into individual capability effects "
    "($\\lambda_1, \\lambda_2, \\lambda_3$) and pairwise interaction effects "
    "($\\lambda_{12}, \\lambda_{13}, \\lambda_{23}$). LEAS provides a "
    "quantitative test for whether a pair of capabilities cooperates "
    "($\\lambda_{ij}>0$) or interferes ($\\lambda_{ij}<0$) under joint training.",
    title="Contribution 1: LEAS as quantitative interference diagnostic",
)

claim_contribution_dart = claim(
    "**Contribution 2 (DART).** The paper proposes **Disentangled "
    "Action-Reasoning Tuning (DART)**, a single-model framework that freezes "
    "the pretrained backbone and attaches two disjoint LoRA [@Hu2022] "
    "adapters: one updated only by reasoning-token gradients ($\\theta_r$), "
    "the other updated only by tool-use-token gradients ($\\theta_a$). A "
    "token-level rule-based router decides which adapter is active at each "
    "decoding step, ensuring tool-use and reasoning never share trainable "
    "parameters.",
    title="Contribution 2: DART as gradient-isolated single model",
)

claim_contribution_empirical = claim(
    "**Contribution 3 (empirical).** Across seven tool-augmented QA "
    "benchmarks (NQ, TriviaQA, PopQA, HotpotQA, 2WikiMultiHopQA, Musique, "
    "Bamboogle) and four backbones (Qwen2.5-3B/7B Base/Instruct), DART "
    "consistently outperforms joint-training baselines by an average **EM "
    "improvement of 6.35%+**, and approaches the performance of a 2-Agent "
    "system that uses two full models -- while requiring only one backbone.",
    title="Contribution 3: 6.35%+ average EM improvement over baselines",
)

__all__ = [
    "setup_arl",
    "setup_joint_assumption",
    "q_interference",
    "claim_capabilities_are_heterogeneous",
    "claim_joint_assumption_unexamined",
    "claim_joint_training_helps_assumed",
    "claim_seesaw_phenomenon",
    "claim_contribution_leas",
    "claim_contribution_dart",
    "claim_contribution_empirical",
]
