"""
priors.py — Prior assignments for 2504-07912-gaia (Echo Chamber paper).

Reviewer rationale:
- Empirical observations from a published, peer-reviewed paper with full
  code/data release: high prior (0.85–0.92), reflecting that these
  measurements are carefully documented and reproducible.
- Theoretical claims (mixture model): moderate-high prior (0.82), as the
  model is intuitive and consistent with RL theory but involves simplifying
  assumptions (mixture decomposition may not hold exactly in practice).
- Alternative hypothesis (pure capability): low prior (0.20), since it is
  a straw-man alternative introduced for abduction comparison.
- echo_chamber_hypothesis: moderate prior (0.60) — the paper's primary
  hypothesis; prior should be informative but not beg the question.
  The abduction evidence drives it to its posterior.
- _anon_000 (hypothetical that RL improves both pass@1 and diversity):
  low prior (0.15) — strong a priori reasons to expect a tradeoff.
- opacity_problem: very high prior (0.92) — widely acknowledged fact.
- code_vs_nl_gap: very high prior (0.95) — objective structural difference.
"""

from .s3_distribution_collapse import (
    obs_tinygsm_dominates_150m,
    obs_omi2_dominates_1b,
    obs_collapse_coincides_with_accuracy,
    obs_diversity_decline,
    theoretical_mixture_model,
    alt_pure_capability,
    pred_echo_chamber,
    pred_pure_capability,
    hypothetical_rl_improves_both,
)
from .s4_results import (
    obs_gsm8k_pass1_improvement,
    obs_math500_transfer_1b,
    obs_omi2_pretrain_best_transfer,
    obs_aime_limited_transfer,
    obs_ppo_most_stable,
    obs_algorithm_agreement_on_format,
    obs_within_distribution_refinement,
    obs_kl_coefficient_effect,
)
from .motivation import opacity_problem, echo_chamber_hypothesis
from .s2_setup import code_vs_nl_gap

PRIORS = {
    # ── Empirical observations (controlled experiments, published results) ──────
    obs_tinygsm_dominates_150m: (
        0.90,
        "Directly observed format proportion trajectory in controlled experiment; "
        "code traces confirm >80% TinyGSM format for 150M models.",
    ),
    obs_omi2_dominates_1b: (
        0.90,
        "Directly observed format proportion trajectory in controlled experiment; "
        "code traces confirm >80% OMI2 (NL) format for 1B models.",
    ),
    obs_collapse_coincides_with_accuracy: (
        0.88,
        "Format tracking curves and accuracy curves plotted jointly show temporal "
        "coincidence within epoch 1; both measurements from same checkpoints.",
    ),
    obs_diversity_decline: (
        0.88,
        "Pass@64 is a standard metric computed from 64 sampled generations; "
        "decline relative to base model is directly measurable and reported.",
    ),
    obs_gsm8k_pass1_improvement: (
        0.90,
        "GSM8K pass@1 is the primary training benchmark metric; 5-15pp improvement "
        "is a direct measurement from the same evaluation pipeline.",
    ),
    obs_math500_transfer_1b: (
        0.90,
        "MATH-500 results tabulated in paper with specific percentages; "
        "8.60%→12.60% and 33.40%→43.60% are verifiable from the paper's tables.",
    ),
    obs_omi2_pretrain_best_transfer: (
        0.88,
        "30pp gap between OMI2 and code-only mixtures on MATH-500 post-RL "
        "is a large, robust effect across all reported configurations.",
    ),
    obs_aime_limited_transfer: (
        0.88,
        "AIME is known to be extremely hard; limited pass@1 transfer is expected "
        "and reported consistently across configurations.",
    ),
    obs_ppo_most_stable: (
        0.87,
        "PPO stability vs. GRPO instability is qualitatively reported; "
        "Expert Iteration underperformance is quantitatively shown.",
    ),
    obs_algorithm_agreement_on_format: (
        0.87,
        "Format tracking applied to GRPO and EI checkpoints shows same collapse pattern; "
        "algorithm-invariance is a strong empirical observation.",
    ),
    obs_within_distribution_refinement: (
        0.85,
        "Single-dataset ablation is a clean comparison; within-distribution "
        "improvements are smaller but consistently observed.",
    ),
    obs_kl_coefficient_effect: (
        0.85,
        "KL hyperparameter sweep is a controlled experiment; the effect on "
        "collapse speed vs. final accuracy is directly measurable.",
    ),

    # ── Background / structural claims ────────────────────────────────────────
    opacity_problem: (
        0.92,
        "The opacity of pretraining data in released LLMs (e.g., Llama, Mistral) "
        "is a widely documented fact in the NLP research community.",
    ),
    code_vs_nl_gap: (
        0.95,
        "The structural difference between Python function syntax (`def solution():`) "
        "and natural language prose is objective and machine-checkable.",
    ),
    theoretical_mixture_model: (
        0.82,
        "The mixture-of-policies model is mathematically well-motivated under KL-regularised "
        "RL, but assumes exact decomposability of the reference policy — a simplification "
        "that may not hold precisely in practice.",
    ),
    echo_chamber_hypothesis: (
        0.60,
        "Moderate prior: the hypothesis is plausible and motivated by the theoretical "
        "model, but prior to seeing the empirical evidence it is not certain. "
        "Posterior will be updated via abduction.",
    ),

    # ── Alternative hypothesis and predictions (abduction) ────────────────────
    alt_pure_capability: (
        0.20,
        "The pure capability hypothesis has weak prior support: RL post-training "
        "without external data cannot logically add new knowledge; it can only "
        "reweight the existing distribution. Set low as straw-man alternative.",
    ),
    pred_echo_chamber: (
        0.60,
        "Prediction follows from the echo chamber hypothesis (same prior).",
    ),
    pred_pure_capability: (
        0.20,
        "Prediction follows from the pure capability hypothesis (same prior).",
    ),

    # ── Contradiction claim (previously anonymous, now named) ────────────────
    hypothetical_rl_improves_both: (
        0.15,
        "A priori unlikely: RL format collapse reduces generation diversity (pass@64). "
        "Strong theoretical and empirical reasons to expect an accuracy-diversity tradeoff. "
        "This hypothetical is included only as the contradiction partner for obs_diversity_decline.",
    ),
}
