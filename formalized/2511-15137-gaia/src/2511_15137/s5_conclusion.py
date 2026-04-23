"""Section 5: Conclusion and Future Work"""

from gaia.lang import claim

from .s3_experiments import (
    grpo_verif_maintains_solution,
    grpo_verif_improves_verification,
    computational_overhead,
)

conclusion_joint_training_viable = claim(
    "Jointly optimizing LLMs for solution generation and self-verification within a single "
    "RL objective is feasible and beneficial: it enhances verification accuracy by 4.2 "
    "percentage points while maintaining solution accuracy within 0.1 percentage points "
    "of solution-only RL training. The two objectives do not substantially compete.",
    title="Joint training is viable and beneficial",
)

conclusion_verification_reliability = claim(
    "Explicitly incorporating self-verification as an RL training objective improves the "
    "reliability of LLM reasoning by producing models that can more accurately assess "
    "whether their own solutions are correct, which is a prerequisite for self-correction "
    "and iterative refinement.",
    title="Verification training improves reasoning reliability",
)

future_work_efficiency = claim(
    "Future work should address the computational overhead of GRPO-Verif, which requires "
    "generating both a solution and a verification for every training sample. Potential "
    "directions include training-time efficiency optimizations (e.g., shared prefixes, "
    "batched generation) or reducing verification generation frequency.",
    title="Future work: computational efficiency",
    background=[computational_overhead],
)

future_work_alpha_study = claim(
    "The paper uses a fixed $\\alpha = 0.2$ for verification loss weighting. Future work "
    "should systematically study the effect of different $\\alpha$ values on the tradeoff "
    "between solution accuracy and verification accuracy, including whether dynamic "
    "scheduling of $\\alpha$ during training is beneficial.",
    title="Future work: alpha sensitivity study",
)
