"""Structural primitives of the architecture (Sections 4-6 of [@Park2026Kumiho]):
the asset-management correspondence, dual-purpose graph design, LLM-memory
decoupling, dual-store working/long-term model, the URI scheme, the
item-revision-tag model, BYO-storage, the memory-type taxonomy, and the typed
edge ontology.

Each primitive is atomized as a definition (`setting`) or a structural claim
that the architecture commits to. The seven core design principles (Section 13
of the paper) are individually atomized here as `claim`s because each is an
architectural assertion that could in principle be questioned.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Section 4.2: Asset-management correspondence (cross-references motivation
# but adds the implementation specifics)
# ---------------------------------------------------------------------------

setup_neo4j_substrate = setting(
    "**Native graph database substrate.** The architecture adopts Neo4j as the "
    "long-term memory storage layer, making relationships first-class "
    "citizens. A dependency between two revisions that would require a "
    "junction-table row plus multi-join in a relational system becomes a "
    "literal directed edge traversable in a single graph operation. "
    "Traditional asset management systems encode these graph-like "
    "relationships in relational databases (PostgreSQL/MySQL) with RPC "
    "frameworks (Thrift/gRPC), where dependency chains require recursive "
    "queries or application-level graph walks over foreign-key joins "
    "[@Park2026Kumiho, Sec. 4.2; Sec. 6.4].",
    title="Setup: Neo4j as native graph substrate makes relationships first-class",
)

# ---------------------------------------------------------------------------
# Section 5.1: LLM-memory decoupling (three mechanisms)
# ---------------------------------------------------------------------------

claim_decoupling_storage = claim(
    "**Decoupling mechanism 1: model-independent storage.** The memory graph "
    "is stored in a standard property graph database. Memories are *structured "
    "data* -- summaries, metadata, tags, edges, artifact pointers -- not "
    "model-specific embeddings or token sequences. This eliminates provider "
    "lock-in, model-upgrade fragility, and architectural non-portability "
    "[@Park2026Kumiho, Sec. 5.1].",
    title="Decoupling 1: structured data storage, not model-specific embeddings",
)

claim_decoupling_mcp = claim(
    "**Decoupling mechanism 2: standardized access protocol via MCP.** Memory "
    "operations are exposed through the Model Context Protocol (MCP) "
    "[@MCP2025], a model-agnostic tool interface. Any MCP-compatible agent "
    "can execute memory operations through the same interface, enabling "
    "platform-agnostic deployment [@Park2026Kumiho, Sec. 5.1; Sec. 11].",
    title="Decoupling 2: MCP standardized access enables platform-agnostic agents",
)

claim_decoupling_pluggable_llm = claim(
    "**Decoupling mechanism 3: pluggable LLM integration.** Components "
    "requiring LLM capabilities -- the Dream State consolidation pipeline, "
    "PII redaction, memory summarization -- accept any LLM through an adapter "
    "interface. The consolidation model can differ from the agent's primary "
    "model [@Park2026Kumiho, Sec. 5.1; Sec. 9.6].",
    title="Decoupling 3: LLM components are pluggable adapters",
)

# ---------------------------------------------------------------------------
# Section 6: System architecture
# ---------------------------------------------------------------------------

setup_dual_store_model = setting(
    "**Dual-store model.** The architecture mirrors the human "
    "working/long-term memory distinction with two stores: (i) **working "
    "memory** -- Redis-backed session buffer accessed via direct library "
    "SDK (not HTTP), with TTL-based expiry (default 1 hour, 50 messages) "
    "and key namespace `cogmem:{proj}:sessions:{sid}:*`; measured latencies "
    "2-5ms via library SDK vs. 150-300ms through HTTP gateway. (ii) "
    "**Long-term memory** -- Neo4j property graph storing all items, "
    "revisions, edges, and tags. The agent interacts through MCP; the "
    "memory graph is LLM-independent [@Park2026Kumiho, Sec. 6.1; Sec. 6.2].",
    title="Setup: dual-store working (Redis) + long-term (Neo4j) model",
)

setup_kref_uri_scheme = setting(
    "**Universal URI scheme.** Every object in the system is addressable "
    "through a hierarchical URI: \n\n"
    "`kref://project/space[/sub]/item.kind[?r=N][&a=artifact]`\n\n"
    "providing: (i) **addressability** -- any memory is referenceable from "
    "any context; (ii) **temporal navigation** -- `?r=N` pins to a specific "
    "revision; (iii) **type safety** -- the `.kind` suffix enables type-aware "
    "retrieval; (iv) **traversal entry points** -- edges reference memory "
    "URIs, enabling graph traversal from any starting point. Among agent "
    "memory systems, no prior use of structured hierarchical URIs with these "
    "properties was found [@Park2026Kumiho, Sec. 1; Sec. 6.3].",
    title="Setup: kref:// URI scheme provides hierarchical addressability + revision pinning",
)

setup_item_revision_model = setting(
    "**Item-Revision model.** Each memory unit is represented as an Item node "
    "with one or more **immutable** Revision nodes forming an append-only "
    "version chain. Each Revision carries structured metadata (summary, "
    "topics, keywords, schema version) and optionally an embedding vector. "
    "Tags (e.g., `current`, `initial`, `published`) are mutable pointers from "
    "tag names to revisions. An agent can: (i) resolve a tag to retrieve the "
    "latest belief; (ii) follow `Supersedes` chains to trace belief evolution; "
    "(iii) follow `Derived_From` edges to understand evidential support; "
    "(iv) move a tag to an earlier revision for belief rollback "
    "[@Park2026Kumiho, Sec. 6.4.1].",
    title="Setup: Item-Revision model = immutable append-only chain + mutable tag pointers",
)

setup_memory_type_taxonomy = setting(
    "**Six memory types.** The system implements six memory types: working "
    "memory (Redis buffer), episodic memory (conversation revisions), "
    "semantic memory (consolidated facts), procedural memory (tool execution "
    "records), associative memory (graph edges + bundles), and meta-memory "
    "(tag system + audit trail) [@Park2026Kumiho, Sec. 6.4.3; Table 3].",
    title="Setup: six memory types (working, episodic, semantic, procedural, associative, meta)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 3",
        "caption": "Memory type taxonomy and implementation.",
    },
)

setup_six_edge_types = setting(
    "**Six typed directed edge types.** The edge system makes reasoning "
    "structure explicit: \n\n"
    "- `Depends_On` -- validity dependency (if target is invalidated, source "
    "may be unreliable)\n"
    "- `Derived_From` -- evidential provenance (source produced using target "
    "as input)\n"
    "- `Supersedes` -- belief revision (source replaces target as current "
    "belief)\n"
    "- `Referenced` -- associative mention (no dependency)\n"
    "- `Contains` -- bundle membership\n"
    "- `Created_From` -- generative lineage\n\n"
    "These enable three traversal operations: `TraverseEdges(k, d, n)`, "
    "`ShortestPath(k_s, k_t)`, and `AnalyzeImpact(k, d)` -- the last is "
    "particularly important for belief revision: when an agent discovers an "
    "assumption is invalid, `AnalyzeImpact` identifies all downstream "
    "conclusions needing re-evaluation [@Park2026Kumiho, Sec. 6.5].",
    title="Setup: six typed edges + three traversal operations (TraverseEdges/ShortestPath/AnalyzeImpact)",
)

# ---------------------------------------------------------------------------
# Section 13: Seven core design principles -- atomized
# ---------------------------------------------------------------------------

claim_p1_structural_reuse = claim(
    "**Principle 1 (Cognitive Memory as Multi-Agent Infrastructure).** AI "
    "agents increasingly produce substantial outputs that are not "
    "systematically tracked, versioned, or linked to the decisions that "
    "created them. In multi-agent workflows this becomes a critical "
    "bottleneck. The structural primitives needed for cognitive memory "
    "(immutable revisions, typed edges, mutable tag pointers, URI addressing) "
    "are *identical* to those needed for managing agent-produced outputs as "
    "versionable, addressable, dependency-linked assets. Rather than "
    "building a memory layer plus a separate asset tracker, we build a "
    "cognitive-memory architecture whose graph-native primitives inherently "
    "serve as the operational infrastructure for multi-agent work "
    "[@Park2026Kumiho, Principle 1; Sec. 4.2].",
    title="Principle 1: structural reuse -- one primitive set for memory AND asset management",
)

claim_p2_match_storage_latency = claim(
    "**Principle 2 (Match Storage Latency to Access Pattern).** Working memory "
    "requires library-level (not RPC-level) access to maintain sub-10ms "
    "latency. The 100-200ms difference between in-process and network access, "
    "compounded across thousands of interactions, accumulates to orders-of-"
    "magnitude differences in agent responsiveness "
    "[@Park2026Kumiho, Principle 2; Sec. 6.2].",
    title="Principle 2: match storage latency to access pattern (library-level for working memory)",
)

claim_p3_universal_addressability = claim(
    "**Principle 3 (Universal Addressability).** Every memory unit must be "
    "referenceable by a stable, parseable, human-readable identifier. Without "
    "addressability, edges become fragile, lineage becomes untraceable, and "
    "consolidation becomes lossy. The `kref://` URI scheme satisfies this "
    "requirement [@Park2026Kumiho, Principle 3; Sec. 6.3].",
    title="Principle 3: universal addressability via stable URIs",
)

claim_p5_immutable_revisions = claim(
    "**Principle 5 (Immutable Revisions, Mutable Pointers).** Memory states "
    "are never overwritten; they are versioned. Tags provide mutable "
    "'current view' semantics without losing history, enabling belief-revision "
    "tracking, audit trails, and rollback. This is the structural foundation "
    "for the AGM correspondence: the contraction operator can archive without "
    "erasing, which is what justifies the principled rejection of the "
    "Recovery postulate [@Park2026Kumiho, Principle 5; Sec. 6.4.1; Sec. 7.3].",
    title="Principle 5: immutable revisions + mutable tag pointers",
)

claim_p7_explicit_relationships = claim(
    "**Principle 7 (Explicit Over Inferred Relationships).** Relationships "
    "between memories must be stored as first-class graph edges, not inferred "
    "at query time through embedding similarity. Similarity finds related "
    "*content*; edges encode *why* content is related "
    "[@Park2026Kumiho, Principle 7; Sec. 6.5].",
    title="Principle 7: relationships are first-class typed edges, not inferred from embeddings",
)

claim_p8_graph_native_advantage = claim(
    "**Principle 8 (Why Graph-Native Edges Matter).** In relational systems, "
    "a dependency between two assets requires a junction table and a "
    "multi-join query. In native graph databases, the same relationship is "
    "a single directed edge traversable in $O(1)$ time. Recursive CTEs can "
    "compute transitive closure over relational joins but require "
    "exponentially more computation as depth increases; a single Cypher "
    "`ShortestPath` query achieves the same result in milliseconds. This "
    "compounds across all graph operations: traversal, impact analysis, "
    "provenance reconstruction [@Park2026Kumiho, Principle 8; Sec. 6.5].",
    title="Principle 8: graph-native edges yield O(1) traversal vs. relational multi-joins",
)

claim_p6_metadata_over_content = claim(
    "**Principle 6 (Metadata Over Content) / BYO-Storage.** Store the minimum "
    "information necessary for recall and reasoning in the cloud graph -- "
    "summaries, relationships, pointers, never file content. Artifact records "
    "contain a `location` field pointing to where raw content resides on the "
    "user's own storage. This content-reference separation -- well-established "
    "in asset-management systems handling petabytes of data -- yields "
    "critical benefits for cognitive memory: lightweight graph database, "
    "architecturally enforced privacy boundaries, compact summary reads "
    "(40x-280x token compression vs. raw transcripts) "
    "[@Park2026Kumiho, Principle 6; Sec. 6.4.2; Sec. 10].",
    title="Principle 6: metadata over content (BYO-storage; raw content stays local)",
)

claim_p9_non_blocking_enhancement = claim(
    "**Principle 9 (Non-Blocking Enhancement).** Enrichment operations "
    "(embeddings, summaries, classifications) must never block the primary "
    "write path. A memory that takes 500ms to store because of an embedding "
    "API call is a memory that agents will avoid storing. Embeddings are "
    "generated asynchronously after each revision creation via a fire-and-"
    "forget background task; on failure, a warning is logged and the "
    "revision remains valid and fulltext-searchable "
    "[@Park2026Kumiho, Principle 9; Sec. 8.3].",
    title="Principle 9: non-blocking enhancement (async embeddings, background enrichment)",
)

claim_p10_conservative_consolidation = claim(
    "**Principle 10 (Conservative Memory Management).** When an AI system "
    "makes automated decisions about memory retention, the default must be "
    "preservation. Deleting a useful memory is worse than retaining a useless "
    "one. Circuit breakers, dry runs, and protection tags ensure that "
    "consolidation enhances quality without risking catastrophic loss "
    "[@Park2026Kumiho, Principle 10; Sec. 9.5].",
    title="Principle 10: conservative consolidation (preservation by default, circuit breakers)",
)

# ---------------------------------------------------------------------------
# The seven core design principles consolidated table (Table 10)
# ---------------------------------------------------------------------------

claim_table10_seven_principles = claim(
    "**Seven core design principles consolidated (Table 10 of "
    "[@Park2026Kumiho]).** \n\n"
    "| #   | Principle                          | Category    |\n"
    "|-----|------------------------------------|-------------|\n"
    "| 1   | Structural Reuse                   | Structure   |\n"
    "| 2   | Universal Addressability           | Structure   |\n"
    "| 3   | Immutable Rev., Mutable Ptr.       | Formal      |\n"
    "| 4   | Explicit Over Inferred Rel.        | Formal      |\n"
    "| 5   | Non-Blocking Enhancement           | Performance |\n"
    "| 6   | Conservative Memory Mgmt.          | Safety      |\n"
    "| 7   | Metadata Over Content              | Safety      |\n\n"
    "These research-level principles define the architecture's formal and "
    "structural commitments [@Park2026Kumiho, Sec. 13; Table 10].",
    title="Seven core design principles (Table 10)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 10",
        "caption": "Core design principles.",
    },
)

# ---------------------------------------------------------------------------
# Atomic-write design (Section 11.3) -- structural primitive at MCP boundary
# ---------------------------------------------------------------------------

claim_atomic_writes = claim(
    "**Atomic memory writes via single MCP invocation.** A single "
    "`memory_ingest` invocation creates the complete memory unit: space "
    "(with auto-creation), item, revision with metadata, artifact "
    "attachment, edges to source materials, bundle membership, tag "
    "assignment, and asynchronous embedding generation. This 'one tool "
    "call, complete memory' design eliminates fragile multi-step "
    "sequences that could leave partially-committed state in the graph "
    "[@Park2026Kumiho, Sec. 11.3].",
    title="Atomic writes: one MCP call creates the complete memory unit",
)

__all__ = [
    "setup_neo4j_substrate",
    "setup_dual_store_model",
    "setup_kref_uri_scheme",
    "setup_item_revision_model",
    "setup_memory_type_taxonomy",
    "setup_six_edge_types",
    "claim_decoupling_storage",
    "claim_decoupling_mcp",
    "claim_decoupling_pluggable_llm",
    "claim_p1_structural_reuse",
    "claim_p2_match_storage_latency",
    "claim_p3_universal_addressability",
    "claim_p5_immutable_revisions",
    "claim_p7_explicit_relationships",
    "claim_p8_graph_native_advantage",
    "claim_p6_metadata_over_content",
    "claim_p9_non_blocking_enhancement",
    "claim_p10_conservative_consolidation",
    "claim_table10_seven_principles",
    "claim_atomic_writes",
]
