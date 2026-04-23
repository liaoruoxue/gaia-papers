from .motivation import *
from .s2_setup import *
from .s3_distribution_collapse import *
from .s4_results import *
from .s5_discussion import *
from .priors import PRIORS

__all__ = [
    # motivation
    "echo_chamber_hypothesis",
    "controlled_study_value",
    "opacity_problem",
    # s2_setup
    "controlled_ablation_design",
    "format_distinctiveness",
    # s3_distribution_collapse
    "rl_amplifies_single_mode",
    "scale_determines_format_preference",
    "obs_format_collapse_epoch1",
    "obs_diversity_decline",
    "theoretical_mixture_model",
    # s4_results
    "rl_improves_easy_transfers_hard",
    "algorithm_invariant_collapse",
    "law_rl_amplifies_pretraining",
    "obs_gsm8k_pass1_improvement",
    "obs_math500_transfer_1b",
    "obs_omi2_pretrain_best_transfer",
    "obs_within_distribution_refinement",
    "obs_kl_coefficient_effect",
    # s5_discussion
    "implication_pretrain_as_important_as_rl",
    "implication_scale_specific_mixtures",
    "implication_diversity_tradeoff",
    "echo_chamber_confirmed",
    "limitations_and_future",
    "within_distribution_refinement_is_secondary",
]
