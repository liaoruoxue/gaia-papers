"""Architecture: ITS Engine, Typed Schema, and Design Principles"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    setting_llm_stateless,
    setting_agent_memory_demand,
    setting_production_requirements,
    claim_memory_tax_exists,
    claim_llm_ingestion_overhead,
)

# --- Settings ---

setting_its_engine = setting(
    "Memanto's retrieval is built on Moorcheh's Information Theoretic Search (ITS) engine, which replaces HNSW-based vector databases with three algorithmic innovations: Maximally Informative Binarization (MIB, 32x compression), Efficient Distance Metric (EDM, information-theoretic distance), and Information Theoretic Score (ITS, normalized [0,1] relevance score).",
    title="ITS engine definition",
)

setting_typed_schema = setting(
    "Memanto implements a schema with 13 predefined semantic categories (fact, preference, decision, commitment, event, instruction, procedure, relationship, belief, goal, context, observation, correction), each assigned distinct retrieval semantics and priority weighting.",
    title="13-category typed memory schema",
)

setting_conflict_resolution = setting(
    "Memanto's conflict resolution mechanism detects semantic contradictions when new memories are committed and offers three resolution options: supersede (replace), retain (keep old), or annotate (preserve both with flag).",
    title="Conflict resolution mechanism",
)

setting_temporal_versioning = setting(
    "Memanto supports three temporal query modalities: as-of (state at timestamp), changed-since (modifications in time range), and current-only (non-superseded memories). Supersession is non-destructive.",
    title="Temporal versioning definition",
)

setting_design_principles = setting(
    "Memanto's six design principles: D1 (Queryable not injectable), D2 (Temporally aware with decay), D3 (Confidence and provenance tracking), D4 (Typed and hierarchical), D5 (Contradiction aware), D6 (Zero overhead ingestion).",
    title="Six design principles",
)

# --- Claims ---

claim_zero_ingestion = claim(
    "Memanto achieves zero-cost ingestion: memory is immediately available for retrieval upon write, with no indexing delay, no mandatory LLM extraction, and <10ms latency per write.",
    title="Zero-cost ingestion",
)

claim_deterministic_retrieval = claim(
    "ITS engine provides deterministic, exact-match semantic search, eliminating the non-determinism inherent in ANN-based systems where identical queries can yield varied results. This enables reproducible agent behavior.",
    title="Deterministic retrieval",
)

claim_mib_no_loss = claim(
    "Maximally Informative Binarization (MIB) compresses high-dimensional float embeddings into compact binary representations with 32x compression and no loss of retrieval-relevant signal.",
    title="MIB lossless compression",
)

claim_its_threshold_deterministic = claim(
    "The Information Theoretic Score (ITS) on a normalized [0,1] scale enables deterministic, threshold-based retrieval, eliminating the need for index construction and ensuring instant write-to-search availability.",
    title="ITS threshold enables deterministic retrieval",
)

claim_typed_schema_enables_filtered = claim(
    "The 13-category typed memory schema enables type-filtered retrieval and provides implicit priority/decay signals, improving retrieval relevance over untyped vector stores.",
    title="Typed schema enables filtered retrieval",
)

claim_conflict_resolution_prevents_drift = claim(
    "Automated conflict resolution prevents 'constraint drift' — the accumulation of contradictions that degrades agent coherence over long-running deployments.",
    title="Conflict resolution prevents constraint drift",
)

# --- Strategies ---

strat_zero_ingestion = support(
    [claim_memory_tax_exists, claim_llm_ingestion_overhead],
    claim_zero_ingestion,
    reason="Memanto eliminates LLM-mediated ingestion by using ITS engine's instant write-to-search capability (@claim_memory_tax_exists). The MIB+EDM+ITS pipeline requires no index construction, removing the 2-3s LLM extraction overhead per write (@claim_llm_ingestion_overhead).",
    prior=0.88,
)

strat_deterministic = support(
    [claim_its_threshold_deterministic],
    claim_deterministic_retrieval,
    reason="ITS's normalized [0,1] score with threshold-based retrieval produces identical results for identical queries, unlike HNSW's approximate nearest neighbor which is non-deterministic (@claim_its_threshold_deterministic).",
    prior=0.85,
)

# Note: claim_typed_schema_enables_filtered and claim_conflict_resolution_prevents_drift
# are leaf claims — their truth is directly evident from the architecture design.
# They don't need strategies with themselves as premises.
