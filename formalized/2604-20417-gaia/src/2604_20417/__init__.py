from .motivation import *
from .s2_semantic_recall import *
from .s3_tolerant_recall import *
from .s4_evaluation import *
from .s4b_tuning import *
from .s5_generalizability import *
from .s6_discussion import *
from .priors import PRIORS  # noqa: F401 – ensures priors are registered

__all__ = [
    # Core metric definitions (cross-package interface)
    "claim_srecall_better_proxy",
    "claim_srecall_no_penalty",
    "claim_srecall_hyperparameter_free",
    "claim_trecall_approximates_srecall",
    "claim_trecall_no_raw_data",
    # Main empirical results
    "claim_recall_comparison_all",
    "claim_few_sn_penalized",
    "claim_tuning_semantic_saves_14pct",
    "claim_tuning_tolerant_saves_5pct",
    "claim_tuning_95pct_target",
    "claim_metrics_generalize",
    "law_tolerant_saves_cost",
    # Problem characterization
    "claim_recall_misaligned",
    "claim_few_relevant_common",
    "claim_irrelevant_equidistant",
    "claim_anns_bounded_by_exact",
    # Discussion conclusions
    "claim_relaxing_precision",
    "claim_traditional_optimizes_noise",
]
