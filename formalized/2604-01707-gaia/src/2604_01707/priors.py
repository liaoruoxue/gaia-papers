"""Prior assignments for independent (leaf) claims."""

from . import (
    extraction_completeness_tradeoff,
    gap_no_comprehensive_comparison,
    gap_no_unified_framework,
    mgmt_connecting,
    mgmt_integrating,
    new_method_design,
    problem_stateless,
    result_backbone_comparison,
    result_context_scalability,
    result_granularity_token_cost,
    result_knowledge_update_scalability,
    result_locomo_7b,
    result_longmemeval_7b,
    result_new_method_locomo,
    result_new_method_longmemeval,
    result_new_method_token_cost,
    storage_graph,
    storage_hierarchical,
)

PRIORS = {
    # Literature gap claims — stated as motivating context in the paper;
    # well-justified by the authors' review of prior work (Table 1)
    gap_no_unified_framework: (
        0.90,
        "Authors conducted a careful literature review and found no unified framework across "
        "the ten representative methods. The diversity of Table 1 classifications confirms this gap.",
    ),
    gap_no_comprehensive_comparison: (
        0.90,
        "Authors explicitly state that comprehensive systematic comparisons among methods "
        "are lacking, supported by the fact that no prior work ran all methods under the same "
        "experimental settings.",
    ),

    # Problem framing — well-established in the LLM agent literature
    problem_stateless: (
        0.92,
        "The context window limitation and resulting stateless-agent problems are well-documented "
        "in the LLM literature (MemGPT, Generative Agents, etc.). High confidence.",
    ),

    # Method definitions — direct textual/structural claims about named methods
    mgmt_connecting: (
        0.95,
        "Direct description of the connecting operation derived from the framework taxonomy. "
        "Definitional — very high confidence.",
    ),
    mgmt_integrating: (
        0.95,
        "Direct description of the integrating operation derived from the framework taxonomy. "
        "Definitional — very high confidence.",
    ),
    storage_hierarchical: (
        0.95,
        "Definition of hierarchical storage with concrete examples (MemoryOS three-tier). "
        "Definitional — very high confidence.",
    ),
    storage_graph: (
        0.95,
        "Definition of graph-based storage with concrete examples (MemTree, Zep). "
        "Definitional — very high confidence.",
    ),

    # Extraction tradeoff — a theoretical claim that may not hold universally
    extraction_completeness_tradeoff: (
        0.75,
        "The claim that graph extraction loses information vs raw preservation is intuitive "
        "and supported by Mem0 vs Mem0g comparisons, but the magnitude of loss varies by context. "
        "Moderate confidence.",
    ),

    # New method design — directly described by authors; architectural design is verifiable
    new_method_design: (
        0.95,
        "The new method's architecture (tree + three-tier) is directly specified by the authors "
        "and depicted in Figure 11. High confidence in the description.",
    ),

    # Experimental results — reported from controlled experiments on known hardware
    # High confidence: standardized setup, two benchmarks, reproducible
    result_longmemeval_7b: (
        0.92,
        "Experimental results from controlled setup on LONGMEMEVAL. "
        "Reimplementation faithfulness is a concern but is partially addressed by using "
        "original code and hyperparameters. High confidence.",
    ),
    result_locomo_7b: (
        0.92,
        "Experimental results from controlled setup on LOCOMO. Same caveats as LONGMEMEVAL. "
        "High confidence.",
    ),
    result_backbone_comparison: (
        0.90,
        "Cross-backbone results on LOCOMO for 5 representative methods. "
        "Slightly lower confidence due to smaller method subset and potential backbone-specific "
        "implementation differences.",
    ),
    result_context_scalability: (
        0.88,
        "Context scalability results from LONGMEMEVAL variants. "
        "Variant construction methodology is in the appendix; moderate-to-high confidence.",
    ),
    result_knowledge_update_scalability: (
        0.88,
        "Category-level scalability analysis for Knowledge Update tasks. "
        "Derives from the same variant experiments as context scalability.",
    ),
    result_granularity_token_cost: (
        0.85,
        "Token cost analysis based on average tokens per dialogue during memory ingestion. "
        "The comparison between MemoryOS and MemoryBank granularity is valid but involves "
        "system-level differences beyond just granularity.",
    ),
    result_new_method_longmemeval: (
        0.90,
        "New method results on LONGMEMEVAL. The method is designed by the paper's authors; "
        "potential for confirmation bias exists, but results on an established benchmark "
        "reduce this concern. High confidence.",
    ),
    result_new_method_locomo: (
        0.90,
        "New method results on LOCOMO. Same caveats as LONGMEMEVAL results. High confidence.",
    ),
    result_new_method_token_cost: (
        0.90,
        "Token cost claim (<450 tokens/dialogue) is a measured quantity from the same "
        "experimental setup. Figure 10 provides visual confirmation.",
    ),
}
