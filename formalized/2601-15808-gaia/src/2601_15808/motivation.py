"""Introduction and Motivation: Inference-Time Scaling of Verification for Deep Research Agents"""

from gaia.lang import (
    claim, setting, question,
    support, contradiction,
)


# ── Background settings ────────────────────────────────────────────────────────

dra_definition = setting(
    "Deep Research Agents (DRAs) are autonomous systems powered by large language models (LLMs) "
    "and vision-language models (VLMs) designed for automated knowledge discovery and complex "
    "problem-solving tasks including coding, web navigation, file processing, and multi-step reasoning.",
    title="Definition of Deep Research Agents",
)

post_training_paradigm = setting(
    "The dominant paradigm for improving DRA capabilities focuses on post-training enhancements: "
    "supervised fine-tuning, reinforcement learning from human feedback, and reward modeling, "
    "all applied before deployment to update model weights.",
    title="Dominant post-training paradigm",
)

asymmetry_of_verification = setting(
    "The asymmetry of verification (Wei, 2025) states that checking the correctness of a solution "
    "is often computationally easier than generating the solution itself. This enables decomposing "
    "complex verification problems into simpler, targeted sub-tasks rather than re-solving the full problem.",
    title="Asymmetry of verification principle",
)

reflexion_background = setting(
    "Reflexion-based methods [@Shinn2023] use textual feedback to bootstrap agent responses, "
    "but generating high-quality feedback itself requires sophisticated reasoning capability, "
    "making naive self-feedback unreliable for DRAs.",
    title="Limitation of naive Reflexion-based self-feedback",
)

# ── Core problem claims ────────────────────────────────────────────────────────

dra_unreliability = claim(
    "Deep Research Agents (DRAs) remain prone to unreliable outputs in long-horizon tasks "
    "due to incorrect actions, API failures, hallucinations, and other errors. In tasks spanning "
    "dozens of pages and hundreds of actions, online human supervision is infeasible, severely "
    "constraining practical deployment.",
    title="DRA reliability problem",
    background=[dra_definition],
)

test_time_scaling_gap = claim(
    "Prior work on inference-time improvement for DRAs has largely emphasized scaling output tokens "
    "or selection across parallel rollouts (e.g., parallel sampling for optimal trajectory search, "
    "narrative-driven aggregation across iterations [@Zhu2025c]). None of these methods "
    "address systematic verification of DRA outputs or structured feedback generation for DRAs.",
    title="Gap in test-time scaling for DRAs",
    background=[dra_definition],
)

feedback_generation_is_hard = claim(
    "The generation of structured, high-quality feedback for DRA outputs is a hard task requiring "
    "sophisticated reasoning capability. Reflexion-based methods that use raw textual feedback "
    "fail to reliably identify subtle reasoning failures, factual errors, or unsupported claims "
    "in long-horizon DRA trajectories.",
    title="Difficulty of structured feedback generation",
    background=[reflexion_background],
)

# ── Research questions ─────────────────────────────────────────────────────────

rq_verification = question(
    "Can the asymmetry of verification be exploited to build an automated, decomposition-based "
    "verifier that outperforms vanilla LLM-judge and agent-as-judge approaches for DRA outputs?",
)

rq_test_time_scaling = question(
    "Can iterative verification feedback enable inference-time scaling of DRA performance "
    "without requiring additional model training?",
)

rq_open_source = question(
    "Can fine-tuning on high-quality DRA verification data enable open-source models to "
    "develop robust reflection and self-critique capabilities for DRA tasks?",
)

# ── Proposed solution claims ───────────────────────────────────────────────────

alternative_paradigm_claim = claim(
    "An alternative paradigm to post-training is self-evolving agents: iteratively verifying "
    "the policy model's outputs guided by meticulously crafted rubrics derived from a systematic "
    "failure taxonomy. This gives rise to inference-time scaling of verification, wherein an agent "
    "self-improves by evaluating its generated answers to produce iterative feedback and refinements, "
    "without updating model weights.",
    title="Inference-time scaling of verification paradigm",
    background=[post_training_paradigm, asymmetry_of_verification],
)

strat_paradigm_motivation = support(
    [dra_unreliability, test_time_scaling_gap, feedback_generation_is_hard],
    alternative_paradigm_claim,
    reason=(
        "The combination of @dra_unreliability (practical deployment barrier), @test_time_scaling_gap "
        "(existing methods miss DRA verification), and @feedback_generation_is_hard (naive feedback "
        "is insufficient) collectively motivates the inference-time verification paradigm (@alternative_paradigm_claim). "
        "By exploiting the asymmetry of verification, rubric-guided decomposition addresses the feedback "
        "quality problem while enabling test-time improvement [@Wan2026]."
    ),
    prior=0.88,
)

# ── Contribution overview claims ───────────────────────────────────────────────

contrib_taxonomy = claim(
    "This work formalizes the agent reflection pipeline for DRAs and introduces a comprehensive "
    "DRA Failure Taxonomy, automatically constructed to categorize agent failures into five major "
    "categories and thirteen sub-categories, from which structured rubrics for outcome-based rewards "
    "are derived.",
    title="Contribution: DRA failure taxonomy",
    background=[dra_definition],
)

contrib_deepverifier = claim(
    "This work presents DeepVerifier, a rubrics-based outcome reward verifier that leverages the "
    "asymmetry of verification and outperforms vanilla agent-as-judge and LLM judge baselines by "
    "12%–48% in meta-evaluation F1 score on DRA verification tasks.",
    title="Contribution: DeepVerifier system",
    background=[asymmetry_of_verification],
)

contrib_inference_scaling = claim(
    "This work demonstrates inference-time scaling of verification that holds for both capable "
    "closed-source LLM APIs and supervised fine-tuned open-source models, delivering 8%–11% "
    "accuracy gains on challenging subsets of the GAIA benchmark [@Mialon2023] and "
    "XBench-DeepSearch [@Chen2025].",
    title="Contribution: inference-time scaling result",
)

contrib_dataset = claim(
    "This work releases DeepVerifier-4K, a curated supervised fine-tuning (SFT) dataset of 4,646 "
    "high-quality agent steps focused on DRA verification, emphasizing reflection and self-critique "
    "to enable open-source model development.",
    title="Contribution: DeepVerifier-4K dataset",
)
