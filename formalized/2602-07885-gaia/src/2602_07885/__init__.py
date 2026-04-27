from .motivation import *
from .s3_framework import *
from .s3_retrieval import *
from .s4_experiments import *
from .priors import PRIORS  # noqa: F401 — ensures priors are registered

__all__ = [
    # Motivation / problem
    "claim_compression_fidelity_dilemma",
    "claim_retrieval_centric_redundancy",
    "claim_memory_augmented_fidelity_loss",
    "claim_ib_aligns_with_memory",
    # Framework foundations
    "claim_memory_ib_lagrangian",
    "claim_three_layer_hierarchy",
    "claim_gated_three_ops",
    "claim_link_preserves_relevance",
    "claim_merge_reduces_compression",
    "claim_extends_aib",
    # Retrieval
    "claim_macro_semantic_path",
    "claim_micro_symbolic_path",
    "claim_topological_path",
    "claim_tripath_addresses_query_diversity",
    "claim_ier_protocol",
    "claim_ier_handles_multihop",
    # Main empirical results
    "claim_avg_gpt4omini",
    "claim_avg_gpt4o",
    "claim_avg_qwen8b",
    "claim_avg_qwen14b",
    "claim_consistent_across_backbones",
    "claim_open_source_advantage_larger",
    "claim_memfly_outperforms",
    "claim_ib_design_validated",
    "claim_proxy_signals_validated",
    # Ablation conclusions
    "claim_update_critical",
    "claim_link_more_important_than_merge",
    "claim_keyword_critical_for_singlehop",
    "claim_ier_critical_for_multihop",
]
