"""Comparative Results and Memory Tax Quantification"""

from gaia.lang import claim, setting, support, abduction, compare, contradiction

from .motivation import (
    claim_memory_tax_exists,
    claim_llm_ingestion_overhead,
    claim_infrastructure_complexity,
)
from .s3_ablation import claim_stage5_longmem, claim_stage5_locomo

# --- Claims: Final results by category ---

claim_longmem_single_session_asst = claim(
    "Memanto achieves 100.0% accuracy on LONGMEMEVAL 'Single-session Assistant' queries.",
    title="LONGMEMEVAL single-session assistant",
)

claim_longmem_single_session_user = claim(
    "Memanto achieves 95.7% accuracy on LONGMEMEVAL 'Single-session User' queries.",
    title="LONGMEMEVAL single-session user",
)

claim_longmem_multi_session = claim(
    "Memanto achieves 81.2% accuracy on LONGMEMEVAL 'Multi-session' queries, the lowest category, reflecting the difficulty of synthesizing information across extended interaction histories.",
    title="LONGMEMEVAL multi-session",
)

claim_locomo_open_domain = claim(
    "Memanto achieves 92.4% on LOCOMO 'Open Domain' queries.",
    title="LOCOMO open domain",
)

claim_locomo_temporal = claim(
    "Memanto achieves 85.4% on LOCOMO 'Temporal' queries.",
    title="LOCOMO temporal",
)

claim_locomo_single_hop = claim(
    "Memanto achieves 78.7% on LOCOMO 'Single-Hop' queries.",
    title="LOCOMO single-hop",
)

claim_locomo_multi_hop = claim(
    "Memanto achieves 70.8% on LOCOMO 'Multi-Hop' queries, the weakest category.",
    title="LOCOMO multi-hop",
)

# --- Claims: Comparative results ---

claim_vector_only_top = claim(
    "Memanto (89.8% LONGMEMEVAL, 87.1% LOCOMO) achieves the highest accuracy among all vector-only systems, surpassing Mem0 by 22.9 pp on LONGMEMEVAL and 20.2 pp on LOCOMO.",
    title="Vector-only top performer",
)

claim_hindsight_slightly_higher = claim(
    "Hindsight (hybrid system) achieves slightly higher overall accuracy (91.4% LONGMEMEVAL, 89.6% LOCOMO) but with maximum architectural complexity score 4/4, requiring dynamic multi-query retrieval and structured reflection passes.",
    title="Hindsight slightly higher with complexity",
)

claim_memanto_competitive_simpler = claim(
    "Memanto achieves competitive accuracy with a simpler architecture (vector-only, single-query, zero-ingestion-cost) compared to Hindsight's maximum-complexity hybrid system. The accuracy gap is only 1.6 pp (LONGMEMEVAL) and 2.5 pp (LOCOMO).",
    title="Memanto competitive with simpler architecture",
)

# --- Claims: Memory Tax quantification ---

claim_ingestion_zero_vs_hybrid = claim(
    "Memanto incurs zero LLM invocations and <10ms latency per write. Mem0-Graph and Zep require ≥2 LLM calls per write with 2-3s ingestion latency.",
    title="Ingestion cost comparison",
)

claim_retrieval_latency_comparison = claim(
    "Memanto achieves sub-90ms retrieval with a single query. Multi-query and recursive strategies in hybrid systems lead to multi-second round-trip latencies.",
    title="Retrieval latency comparison",
)

claim_cost_comparison = claim(
    "Memanto costs $0.50/day for 10K memory operations vs. $2.32/day for Mem0-Graph and $1.70/day for Zep. Moorcheh's serverless architecture allows scaling to zero during idle periods.",
    title="Daily cost comparison",
)

claim_idle_cost_zero = claim(
    "Memanto scales to zero during idle periods, eliminating fixed infrastructure costs, unlike competing systems with fixed idle costs.",
    title="Zero idle cost",
)

# --- Strategies ---

strat_vector_top = support(
    [claim_stage5_longmem, claim_stage5_locomo],
    claim_vector_only_top,
    reason="Memanto's final scores of 89.8% LONGMEMEVAL and 87.1% LOCOMO (@claim_stage5_longmem, @claim_stage5_locomo) exceed all other vector-only systems, notably Mem0 by 22.9/20.2 pp.",
    prior=0.92,
)

strat_memanto_competitive = support(
    [claim_vector_only_top, claim_hindsight_slightly_higher],
    claim_memanto_competitive_simpler,
    reason="Memanto's vector-only architecture achieves 89.8% vs Hindsight's 91.4% on LONGMEMEVAL (@claim_vector_only_top, @claim_hindsight_slightly_higher). The 1.6 pp gap is small given Memanto's dramatically simpler architecture (single-query, zero ingestion, no graph DB).",
    prior=0.88,
)

strat_memory_tax_quantified = support(
    [claim_ingestion_zero_vs_hybrid, claim_retrieval_latency_comparison, claim_cost_comparison],
    claim_memory_tax_exists,
    reason="The Memory Tax is now quantified: zero LLM calls + <10ms vs ≥2 LLM calls + 2-3s per write (@claim_ingestion_zero_vs_hybrid), sub-90ms vs multi-second retrieval (@claim_retrieval_latency_comparison), $0.50 vs $1.70-2.32/day (@claim_cost_comparison). These concrete overhead differences confirm the tax's existence and magnitude.",
    prior=0.94,
)

# --- Contradiction: vector-only sufficiency vs hybrid necessity ---

claim_vector_sufficient = claim(
    "Vector-only architecture with optimized retrieval is sufficient for high-fidelity agent memory, making knowledge graph augmentation unnecessary.",
    title="Vector-only sufficient for agent memory",
)

claim_graph_necessary = claim(
    "Knowledge graph augmentation is necessary for high-fidelity agent memory; vector-only approaches are fundamentally limited.",
    title="Graph augmentation necessary",
)

not_both = contradiction(
    claim_vector_sufficient,
    claim_graph_necessary,
    reason="If vector-only is sufficient, then graph augmentation is not necessary (and vice versa). They cannot both be true for the same task domain.",
    prior=0.95,
)

strat_vector_sufficient = support(
    [claim_memanto_competitive_simpler],
    claim_vector_sufficient,
    reason="Memanto achieves within 1.6-2.5 pp of the best hybrid system (Hindsight) with a vector-only architecture (@claim_memanto_competitive_simpler). If graph augmentation were necessary, the gap should be much larger.",
    prior=0.78,
)
