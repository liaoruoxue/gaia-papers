from .motivation import *
from .s2_spurious_rewards import *
from .s3_cross_model import *
from .s4_code_reasoning import *
from .s5_discussion import *

__all__ = [
    # Core empirical claims
    "claim_rlvr_improves_qwen",
    "claim_spurious_fails_non_qwen",
    "claim_qwen7b_math500_results",
    "claim_random_gamma_robustness",
    # Core mechanism claims
    "claim_pretraining_hypothesis",
    "claim_code_freq_increases_rlvr",
    "claim_lang_to_code_contribution",
    "claim_grpo_clipping_bias",
    "claim_no_clipping_no_gain",
    "claim_clipping_amplifies_prior",
    # Cross-model generalization
    "claim_model_family_consistency",
    "claim_ttrl_one_shot_same_pattern",
    # Implications
    "claim_implication_pretraining_primary",
    "claim_implication_corrupted_supervision",
    "claim_implication_no_generalization",
    "claim_qwen_centric_risk",
]
