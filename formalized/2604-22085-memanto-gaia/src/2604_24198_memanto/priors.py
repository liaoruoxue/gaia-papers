from . import (
    claim_conflict_resolution_prevents_drift,
    claim_cost_comparison,
    claim_graph_necessary,
    claim_hindsight_slightly_higher,
    claim_ingestion_zero_vs_hybrid,
    claim_infrastructure_complexity,
    claim_its_threshold_deterministic,
    claim_llm_ingestion_overhead,
    claim_retrieval_latency_comparison,
    claim_stage2_locomo,
    claim_stage2_longmem,
    claim_stage3_locomo,
    claim_stage3_longmem,
    claim_stage4_longmem,
    claim_stage5_locomo,
    claim_stage5_longmem,
    claim_typed_schema_enables_filtered,
)

PRIORS = {
    # Ablation stage results — directly reported, high confidence
    claim_stage2_longmem: (0.95, "Direct experimental result from Table V, +20.4 pp improvement"),
    claim_stage2_locomo: (0.95, "Direct experimental result from Table V, +6.6 pp improvement"),
    claim_stage3_longmem: (0.95, "Direct experimental result, +2.2 pp marginal gain"),
    claim_stage3_locomo: (0.95, "Direct experimental result, +0.1 pp negligible gain"),
    claim_stage4_longmem: (0.95, "Direct experimental result, +5.8 pp"),
    claim_stage5_longmem: (0.95, "Final reported result 89.8%, Table VII"),
    claim_stage5_locomo: (0.95, "Final reported result 87.1%, Table VIII"),

    # Architecture claims — design features, high confidence
    claim_its_threshold_deterministic: (0.88, "ITS engine design claim; deterministic by construction but MIB compression claim unverified by third party"),
    claim_typed_schema_enables_filtered: (0.90, "Directly evident from 13-category schema design"),
    claim_conflict_resolution_prevents_drift: (0.75, "Design claim; conflict detection exists but empirical drift prevention not independently measured in paper"),

    # Memory Tax quantification — from Table X, high confidence
    claim_ingestion_zero_vs_hybrid: (0.93, "Direct measurement: 0 LLM calls vs ≥2, <10ms vs 2-3s"),
    claim_retrieval_latency_comparison: (0.90, "Direct measurement: sub-90ms vs multi-second"),
    claim_cost_comparison: (0.88, "Cost model estimate, may vary by deployment"),

    # Comparative results
    claim_hindsight_slightly_higher: (0.93, "From Table IX: Hindsight 91.4% vs Memanto 89.8% on LONGMEMEVAL"),

    # Alternative hypothesis — low prior because evidence weighs against it
    # Alternative hypothesis — low prior because evidence weighs against it
    claim_graph_necessary: (0.25, "Contradicted by Memanto achieving within 1.6-2.5 pp of Hindsight without graph augmentation. Multi-hop weakness (70.8%) suggests graphs may help for specific reasoning types, but not necessary overall."),

    # Hybrid system overhead
    claim_llm_ingestion_overhead: (0.90, "Well-documented architectural characteristic of Mem0/Zep/Letta systems; ≥2 LLM calls per write is by design for entity extraction and graph construction"),
}
