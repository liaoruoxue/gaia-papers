"""Limitations and Design Principles Validation"""

from gaia.lang import claim, support, deduction

from .motivation import claim_memory_tax_exists, claim_llm_ingestion_overhead
from .s2_architecture import (
    claim_zero_ingestion,
    claim_deterministic_retrieval,
    claim_conflict_resolution_prevents_drift,
    claim_typed_schema_enables_filtered,
)
from .s3_ablation import claim_recall_over_precision, claim_llm_noise_tolerance
from .s4_comparison import claim_memanto_competitive_simpler, claim_vector_sufficient

# --- Limitation claims ---

claim_benchmark_conversation_only = claim(
    "Current benchmarks (LONGMEMEVAL, LOCOMO) focus on conversational settings. Evaluation in non-conversational agentic workflows (research, code generation, multi-agent coordination) is missing.",
    title="Benchmark conversation-only limitation",
)

claim_benchmark_saturation = claim(
    "Existing benchmarks show rapid convergence of competing systems and potential labeling inconsistencies, indicating a need for more targeted and challenging evaluation protocols.",
    title="Benchmark saturation",
)

claim_inference_model_dependence = claim(
    "Final results depend on Gemini 3 as the inference model. Stage 5 contributed +4.8 pp on LONGMEMEVAL, suggesting ongoing improvements in foundational models will shift the differentiator towards retrieval quality.",
    title="Inference model dependence",
)

claim_scale_untested = claim(
    "Memanto's performance with thousands of concurrent agents remains untested. The Moorcheh engine has been validated at large scales, but the full Memanto platform under high concurrency is future work.",
    title="Scale untested",
)

claim_multi_agent_isolation = claim(
    "Agent memories are currently isolated by namespaces. Shared memory across agent teams with appropriate access control is not yet implemented.",
    title="Multi-agent memory isolation",
)

claim_multi_hop_weak = claim(
    "Memanto's weakest category is LOCOMO Multi-Hop at 70.8%, suggesting difficulty with complex cross-reference reasoning that may benefit from graph-based structural links.",
    title="Multi-hop weak category",
)

# --- Design principle validation claims ---

claim_d1_validated = claim(
    "D1 (Queryable not injectable) is validated: agents that actively query memory based on relevance outperform passive context injection, consistent with the recall-over-precision finding.",
    title="D1 validated",
)

claim_d4_validated = claim(
    "D4 (Typed and hierarchical) is validated: 13-category schema enables type-filtered retrieval that improves relevance over untyped stores.",
    title="D4 validated",
)

claim_d5_validated = claim(
    "D5 (Contradiction aware) is validated: automated conflict resolution prevents constraint drift in long-running deployments.",
    title="D5 validated",
)

claim_d6_validated = claim(
    "D6 (Zero overhead ingestion) is validated: Memanto achieves <10ms write latency with zero LLM calls, confirming the design principle.",
    title="D6 validated",
)

# --- Exported conclusion: the core thesis ---

claim_core_thesis = claim(
    "A vector-only architecture with information-theoretic retrieval, typed memory schema, and conflict resolution can achieve competitive accuracy with simpler architecture than hybrid graph+vector systems, while eliminating the Memory Tax. The key principle is that recall outweighs precision for agentic memory: modern LLMs can filter noisy context, so retrieval systems should prioritize broad coverage over aggressive filtering.",
    title="Core thesis: vector-only + recall > precision",
)

# --- Strategies ---

strat_core_thesis = deduction(
    [claim_vector_sufficient, claim_recall_over_precision],
    claim_core_thesis,
    reason="If vector-only is sufficient for competitive accuracy (@claim_vector_sufficient) and recall outweighs precision for agentic memory (@claim_recall_over_precision), then the core thesis follows: vector-only + high-recall retrieval + typed schema is a simpler, cheaper, competitive architecture.",
    prior=0.90,
)

strat_d1_validated = support(
    [claim_recall_over_precision],
    claim_d1_validated,
    reason="The recall-over-precision finding (@claim_recall_over_precision) directly validates D1: agents benefit from querying a broad memory store rather than receiving a narrow, pre-filtered context injection.",
    prior=0.85,
)

strat_d4_validated = support(
    [claim_typed_schema_enables_filtered],
    claim_d4_validated,
    reason="Typed schema enables filtered retrieval, which directly validates D4's principle of typed and hierarchical memory.",
    prior=0.88,
)

strat_d5_validated = support(
    [claim_conflict_resolution_prevents_drift],
    claim_d5_validated,
    reason="Conflict resolution preventing constraint drift directly validates D5's principle of contradiction awareness.",
    prior=0.82,
)

strat_d6_validated = support(
    [claim_zero_ingestion],
    claim_d6_validated,
    reason="Zero-cost ingestion (<10ms, no LLM calls) directly validates D6's principle of zero overhead ingestion.",
    prior=0.90,
)

# claim_multi_hop_weak is a leaf empirical observation, no self-referencing strategy needed
