"""Section 5: Discussion and Implications"""

from gaia.lang import claim, setting, support, deduction, complement

from .motivation import echo_chamber_hypothesis, opacity_problem, controlled_study_value
from .s3_distribution_collapse import (
    rl_amplifies_single_mode,
    scale_determines_format_preference,
    obs_diversity_decline,
    theoretical_mixture_model,
)
from .s4_results import (
    rl_improves_easy_transfers_hard,
    algorithm_invariant_collapse,
    law_rl_amplifies_pretraining,
    obs_omi2_pretrain_best_transfer,
    obs_within_distribution_refinement,
    obs_kl_coefficient_effect,
    obs_aime_limited_transfer,
)

# ── Settings ─────────────────────────────────────────────────────────────────

pretraining_composition_lever = setting(
    "Pretraining data composition — the relative proportion of different data sources "
    "in the training mixture — is a design variable that practitioners can control. "
    "Post-RL performance depends on which format RL selects, which in turn depends on "
    "which formats are present and their relative performance at pretraining time.",
    title="Pretraining composition as a design lever",
)

# ── Implication Claims ────────────────────────────────────────────────────────

implication_pretrain_as_important_as_rl = claim(
    "Pretraining data composition deserves scrutiny comparable to RL algorithm choice "
    "when developing mathematical reasoning models. Because RL amplifies the highest-reward "
    "pretraining distribution, the post-RL performance ceiling is largely determined by "
    "which formats were included in pretraining and how well they perform at pretraining time.",
    title="Pretraining composition is as important as RL algorithm choice",
    metadata={"source_section": "Section 5"},
)

strat_pretrain_importance = support(
    [rl_amplifies_single_mode, obs_omi2_pretrain_best_transfer, algorithm_invariant_collapse],
    implication_pretrain_as_important_as_rl,
    reason=(
        "@rl_amplifies_single_mode shows RL selects among pretraining formats, not inventing new ones. "
        "@obs_omi2_pretrain_best_transfer shows that including OMI2 in pretraining yields ~30pp better "
        "MATH-500 after RL than code-only pretraining — a larger effect than any algorithm choice. "
        "@algorithm_invariant_collapse confirms the RL algorithm choice doesn't change the qualitative outcome. "
        "Together these establish pretraining composition as the dominant lever for post-RL performance."
    ),
    prior=0.88,
    background=[pretraining_composition_lever],
)

implication_scale_specific_mixtures = claim(
    "Optimal pretraining mixture composition is model-scale-dependent: smaller models "
    "(150M) benefit more from code-style datasets (TinyGSM) because RL selects code as "
    "their dominant format; larger models (1B) benefit more from natural-language datasets "
    "(OMI2) because RL selects NL reasoning as their dominant format. "
    "A single universal mixture is unlikely to be optimal across scales.",
    title="Optimal pretraining mixture is scale-dependent",
    metadata={"source_section": "Section 5"},
)

strat_scale_specific_mixtures = support(
    [scale_determines_format_preference, obs_omi2_pretrain_best_transfer],
    implication_scale_specific_mixtures,
    reason=(
        "@scale_determines_format_preference establishes that model scale selects the "
        "amplified format (code at 150M, NL at 1B). @obs_omi2_pretrain_best_transfer "
        "shows that including the format RL will select (OMI2/NL for 1B) in pretraining "
        "is essential for maximising post-RL transfer. Therefore, the optimal pretraining "
        "mixture must be tailored to the target scale."
    ),
    prior=0.82,
)

implication_diversity_tradeoff = claim(
    "RL post-training creates an inherent tradeoff between greedy accuracy (pass@1) and "
    "generation diversity (pass@64). Practitioners who prioritise diverse reasoning "
    "strategies or ensemble-based inference (majority voting, best-of-N) may not benefit "
    "from standard RL fine-tuning, which systematically reduces output diversity.",
    title="RL creates accuracy-diversity tradeoff for practitioners",
    metadata={"source_section": "Section 5"},
)

strat_diversity_tradeoff = support(
    [obs_diversity_decline, obs_kl_coefficient_effect],
    implication_diversity_tradeoff,
    reason=(
        "@obs_diversity_decline directly shows pass@64 declines post-RL across configurations. "
        "@obs_kl_coefficient_effect shows that even varying KL coefficient cannot simultaneously "
        "maximise diversity and pass@1 — higher KL slows collapse but achieves only comparable "
        "final accuracy. The tradeoff appears fundamental to RL format selection."
    ),
    prior=0.85,
)

within_distribution_refinement_is_secondary = claim(
    "Within-distribution stylistic refinement (RL standardising formatting and style within "
    "a single format, observed in single-dataset pretraining experiments) is a secondary "
    "mechanism of RL post-training improvement, separate from and smaller in effect than "
    "the primary mechanism of cross-format selection in mixture pretraining.",
    title="Within-distribution refinement is secondary to format selection",
    metadata={"source_section": "Section 5"},
)

strat_secondary_refinement = support(
    [obs_within_distribution_refinement, rl_amplifies_single_mode],
    within_distribution_refinement_is_secondary,
    reason=(
        "@obs_within_distribution_refinement establishes that single-dataset RL still "
        "improves accuracy via stylistic standardisation. @rl_amplifies_single_mode "
        "shows the primary mechanism in mixture settings is format collapse, with larger "
        "accuracy gains. Since format selection (5-15pp gains) exceeds pure refinement, "
        "refinement is classified as the secondary mechanism."
    ),
    prior=0.80,
)

# ── Complement: two exhaustive explanations of RL gains ──────────────────────

one_of_selection_or_refinement = complement(
    rl_amplifies_single_mode,
    within_distribution_refinement_is_secondary,
    reason=(
        "In any given RL fine-tuning run, either the model has a mixture of pretraining "
        "formats (format selection dominates) or it was pretrained on a single format "
        "(refinement dominates). These cover the exhaustive space of pretraining scenarios."
    ),
    prior=0.85,
)

limitations_and_future = claim(
    "The study has several limitations that bound the generalisability of its conclusions: "
    "(1) Only two model scales (150M, 1B) are tested — behaviour at 7B+ is unknown. "
    "(2) Only English mathematical reasoning is evaluated — multilingual transfer is untested. "
    "(3) Pretraining mixtures are limited to three instruction datasets — more diverse mixtures "
    "may exhibit different collapse patterns. "
    "(4) The mechanism by which model scale determines format preference is not explained — "
    "it is observed but not theorised. "
    "(5) AIME transfer is limited (@obs_aime_limited_transfer), suggesting the study's "
    "findings may not generalise fully to the hardest reasoning tasks.",
    title="Limitations of the study",
    metadata={"source_section": "Section 5 / Limitations"},
)

strat_limitations = support(
    [obs_aime_limited_transfer],
    limitations_and_future,
    reason=(
        "@obs_aime_limited_transfer shows that RL fine-tuning on GSM8K does not "
        "substantially improve pass@1 or Majority@64 on AIME, the hardest benchmark. "
        "This limits the scope of the transfer learning claims and supports the "
        "conclusion that the study's findings are clearest in the easy-to-medium "
        "difficulty range (GSM8K → MATH-500), not at the extreme difficulty end."
    ),
    prior=0.82,
)

echo_chamber_confirmed = claim(
    "The echo chamber hypothesis — that RL post-training amplifies pretraining behaviors "
    "rather than introducing novel capabilities — is confirmed by the combined evidence: "
    "format collapse to pretraining modes, scale-dependent format selection, algorithm "
    "invariance of the collapse pattern, and the theoretical mixture model's quantitative "
    "predictions [@Zhao2025].",
    title="Echo chamber hypothesis confirmed (synthesis)",
    metadata={"source_section": "Section 5 / Conclusion"},
)

strat_echo_confirmed = support(
    [law_rl_amplifies_pretraining, algorithm_invariant_collapse, theoretical_mixture_model],
    echo_chamber_confirmed,
    reason=(
        "@law_rl_amplifies_pretraining (established by induction across multiple configurations) "
        "is the empirical core. @algorithm_invariant_collapse rules out the RL algorithm as "
        "the cause. @theoretical_mixture_model provides the formal mechanism (exponential "
        "reweighting by reward under KL-regularised RL). Together these confirm "
        "@echo_chamber_hypothesis: RL is an amplification mechanism, not a capability-discovery one."
    ),
    prior=0.90,
    background=[controlled_study_value],
)

__all__ = [
    "implication_pretrain_as_important_as_rl",
    "implication_scale_specific_mixtures",
    "implication_diversity_tradeoff",
    "echo_chamber_confirmed",
    "limitations_and_future",
    "within_distribution_refinement_is_secondary",
]
