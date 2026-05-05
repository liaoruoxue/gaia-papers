"""Section III.C: The Moorcheh Foundation: Information Theoretic Search.

Section III.C of [@Abtahi2026Memanto] describes the retrieval substrate that
Memanto is built on. The Moorcheh engine departs from the dominant
HNSW + cosine-distance paradigm via three algorithmic innovations:
Maximally Informative Binarisation (MIB), Efficient Distance Metric (EDM),
and Information Theoretic Score (ITS). Together these eliminate the need
for index construction, enabling instant write-to-search availability.

The independent MAIR validation [@MoorchehITS] anchors the engine's
performance numbers (NDCG@10, latency, QPS, end-to-end speedup vs
Pinecone+Cohere). Each algorithmic property is extracted as a separate
atomic claim so that benchmark-derived properties (latency, NDCG) are
distinguishable from architectural assertions (no indexing, deterministic
retrieval).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# III.C Three core algorithmic innovations (definitions)
# ---------------------------------------------------------------------------

setup_mib = setting(
    "**Maximally Informative Binarisation (MIB).** MIB compresses high-"
    "dimensional floating-point embedding vectors into compact binary "
    "representations while preserving the information-theoretic content "
    "relevant to retrieval. The compression preserves retrieval-relevant "
    "signal by selecting binarisation thresholds that maximise mutual "
    "information between the binary representation and the original "
    "embedding [@Abtahi2026Memanto, Sec. III.C; @MoorchehITS].",
    title="Setup: MIB compresses float embeddings to binary while preserving information-theoretic content",
)

setup_edm = setting(
    "**Efficient Distance Metric (EDM).** EDM replaces cosine similarity "
    "with an information-theoretic distance that scores memory chunks by "
    "their ability to *reduce uncertainty in the query context*, rather "
    "than by surface-level geometric proximity in embedding space "
    "[@Abtahi2026Memanto, Sec. III.C].",
    title="Setup: EDM = information-theoretic distance (uncertainty reduction), not geometric cosine",
)

setup_its = setting(
    "**Information Theoretic Score (ITS).** ITS is a universal relevance "
    "score on a normalised $[0, 1]$ scale that quantifies the decision-"
    "theoretic value of each retrieved chunk for the current query. ITS "
    "enables deterministic, threshold-based retrieval [@Abtahi2026Memanto, "
    "Sec. III.C].",
    title="Setup: ITS = relevance score on $[0,1]$ enabling threshold-based retrieval",
)

# ---------------------------------------------------------------------------
# Algorithmic properties (claims because each can be questioned)
# ---------------------------------------------------------------------------

claim_mib_32x_compression = claim(
    "**MIB achieves 32x compression with no measurable loss in retrieval-"
    "relevant signal.** The binarisation reduces float-vector storage by "
    "approximately 32x relative to the standard 32-bit floating-point "
    "embedding representation, while empirical evaluation shows no "
    "measurable loss in retrieval-relevant signal "
    "[@Abtahi2026Memanto, Sec. III.C].",
    title="MIB: 32x storage compression with no measurable retrieval-signal loss",
)

claim_no_indexing = claim(
    "**The Moorcheh engine eliminates index construction entirely.** "
    "Together, MIB, EDM, and ITS remove the need for ANN indexing "
    "structures (such as HNSW [@HNSW] graphs) that traditional vector "
    "databases require. The store is *zero-indexing*: a newly inserted "
    "memory becomes immediately queryable without any index update "
    "[@Abtahi2026Memanto, Sec. III.B; Sec. III.C; Sec. V.D].",
    title="Moorcheh is zero-indexing: writes are immediately queryable",
)

claim_instant_write_to_search = claim(
    "**Instant write-to-search availability (sub-10 ms ingestion).** "
    "Because no index update is required, ingestion latency is sub-10 "
    "ms per write, eliminating the ingest-to-query gap that constrains "
    "traditional vector databases [@Abtahi2026Memanto, Sec. III.C; "
    "Table X reports `<10 ms` for Memanto ingestion].",
    title="Moorcheh: ingestion < 10 ms; new memories instantly queryable",
)

claim_deterministic_retrieval = claim(
    "**ITS-based retrieval is deterministic: identical queries produce "
    "identical results.** Threshold-based retrieval over ITS scores is a "
    "deterministic operation: given the same store state and the same "
    "query embedding, the same set of chunks is returned every time. "
    "This contrasts with HNSW-based ANN systems, which can return "
    "different candidate sets depending on index state and graph-traversal "
    "stochasticity. Determinism is critical for reproducible agent "
    "behaviour in regulated environments and for stability of multi-turn "
    "agent interactions [@Abtahi2026Memanto, Sec. III.C; Sec. V.D].",
    title="ITS retrieval is deterministic; ANN systems are not",
)

claim_sub90ms_retrieval = claim(
    "**Retrieval latency is sub-90 ms (Memanto end-to-end), with 9.6 ms "
    "Moorcheh distance-calculation latency on MAIR.** The Moorcheh "
    "engine has been independently validated on the Massive AI Retrieval "
    "(MAIR) benchmark, achieving 9.6 ms distance-calculation latency "
    "(compared to 37-86 ms for PGVector and Qdrant). Memanto's full "
    "retrieval call (embedding + ITS scoring + threshold gating) "
    "completes in under 90 ms, and Table X reports `<90 ms` retrieval "
    "for Memanto vs multi-second round-trips for graph-traversal "
    "competitors [@Abtahi2026Memanto, Sec. III.C; Table X; @MoorchehITS].",
    title="Moorcheh: 9.6 ms MAIR distance calc; Memanto retrieval < 90 ms end-to-end",
)

claim_mair_throughput = claim(
    "**Moorcheh sustains 2,000+ QPS with zero accuracy degradation; "
    "delivers 6.6x end-to-end speedup vs Pinecone + Cohere reranking.** "
    "On the Massive AI Retrieval (MAIR) benchmark [@MoorchehITS], the "
    "Moorcheh engine achieves 64-74% NDCG@10, sustains 2,000+ queries "
    "per second with no measurable accuracy degradation, and delivers a "
    "6.6x end-to-end speedup relative to a Pinecone + Cohere reranking "
    "pipeline baseline [@Abtahi2026Memanto, Sec. III.C].",
    title="MAIR validation: 64-74% NDCG@10, 2000+ QPS, 6.6x speedup vs Pinecone+Cohere",
)

# ---------------------------------------------------------------------------
# Synthesis claim
# ---------------------------------------------------------------------------

claim_its_enables_d6 = claim(
    "**ITS engine architecturally satisfies D6 (zero-overhead "
    "ingestion).** The combination of MIB (32x binary compression), EDM "
    "(information-theoretic distance), and ITS (normalised relevance "
    "score) jointly eliminates index construction, which in turn "
    "eliminates the indexing-induced ingestion delay. This is the "
    "architectural mechanism by which Memanto satisfies D6 -- a "
    "desideratum that all evaluated competing systems either fail or "
    "only partially satisfy [@Abtahi2026Memanto, Sec. III.C; Table I].",
    title="ITS engine architecturally enables D6 (zero-overhead ingestion)",
)

claim_its_enables_determinism = claim(
    "**ITS engine architecturally enables deterministic agentic memory "
    "retrieval (Sec. V.D).** Because ITS-based retrieval is exhaustive "
    "and deterministic rather than ANN-approximate, identical queries "
    "yield identical results. This eliminates a class of non-determinism "
    "that ANN-based systems introduce through probabilistic graph "
    "traversal, which can otherwise propagate inconsistencies across "
    "multi-turn agent interactions [@Abtahi2026Memanto, Sec. V.D].",
    title="ITS engine enables deterministic retrieval, eliminating ANN-induced agent instability",
)

__all__ = [
    "setup_mib",
    "setup_edm",
    "setup_its",
    "claim_mib_32x_compression",
    "claim_no_indexing",
    "claim_instant_write_to_search",
    "claim_deterministic_retrieval",
    "claim_sub90ms_retrieval",
    "claim_mair_throughput",
    "claim_its_enables_d6",
    "claim_its_enables_determinism",
]
