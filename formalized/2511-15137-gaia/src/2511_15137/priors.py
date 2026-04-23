"""
Prior assignments for independent (leaf) claims in GRPO-Verif formalization.

These priors reflect the evidence quality and plausibility of each independent
claim based on a critical reading of the paper (arXiv 2511.15137).
"""

from . import (
    alpha_hyperparameter,
    grpo_verif_conditioning,
    grpo_verif_objective,
    research_question_tradeoff,
    result_solution_accuracy,
    sft_limitation,
    verification_training_neglect,
)

PRIORS = {
    # The GRPO-Verif joint objective is formally defined in the paper with
    # explicit equations (Eqs 3-4). Its mathematical correctness is not in doubt;
    # what is uncertain is whether the specific formulation is optimal.
    grpo_verif_objective: (
        0.93,
        "The objective is formally defined with explicit equations. It correctly "
        "combines solution and verification losses. Minor uncertainty about whether "
        "the per-token normalization is the optimal choice.",
    ),

    # Verification conditioned on (question, solution) is a clear design decision
    # stated in the method section. No ambiguity about the conditioning.
    grpo_verif_conditioning: (
        0.95,
        "Explicitly stated design choice: verification input is (q, y^(i)). "
        "No ambiguity; this is a definitional property of GRPO-Verif.",
    ),

    # alpha=0.2 is reported as a design choice with no ablation study in the paper.
    # The value is plausible but not validated across alternatives.
    alpha_hyperparameter: (
        0.70,
        "The value alpha=0.2 is asserted without ablation. Plausible as a weak "
        "auxiliary weight, but uncertainty remains about whether it is optimal.",
    ),

    # The result table is a direct empirical observation from the experiment.
    # High prior as it reflects directly reported numbers; risk of data transcription
    # error is low but non-zero.
    result_solution_accuracy: (
        0.92,
        "Directly reported experimental data in Table 1. High confidence in accuracy "
        "of the numbers given replication is straightforward. Slight uncertainty "
        "about generalizability beyond the single model/dataset configuration.",
    ),

    # The claim that SFT causes distribution shift is well-established in the
    # RL-for-LLM literature. The paper correctly identifies this as a limitation.
    sft_limitation: (
        0.85,
        "Distribution shift from SFT in RL settings is a recognized problem in "
        "the literature. The claim is standard and well-supported by prior work.",
    ),

    # The claim that existing RL training neglects verification is clearly true
    # for GRPO; slightly uncertain about whether some intermediate approaches exist.
    verification_training_neglect: (
        0.88,
        "Standard GRPO and similar methods optimize only for solution correctness. "
        "This is confirmed by inspecting the GRPO objective. The claim is accurate "
        "for the baseline GRPO approach studied in this paper.",
    ),

    # The tradeoff concern is a legitimate open question, but the paper's own
    # evidence shows the concern is partially unfounded. Setting prior to reflect
    # that the concern is reasonable a priori but ultimately resolved.
    research_question_tradeoff: (
        0.60,
        "The concern that joint training may hurt solution accuracy is a reasonable "
        "a priori hypothesis, though the paper's results show it does not materialize. "
        "Prior reflects the pre-experimental plausibility of the concern.",
    ),
}
