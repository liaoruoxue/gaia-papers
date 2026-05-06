"""Section 4 (Background and Motivation) of [@Park2026Kumiho]: the asset-management
insight, the dual-purpose graph design, and the architectural argument that the
*same* graph that stores cognitive memories also manages agent work products.

This module separates the *architectural claim* (memory primitives = asset
primitives) from the *formal correspondence claim* (graph operations satisfy
AGM postulates -- module `s5_agm_correspondence.py`). Atomization keeps the
two contributions independently judgeable.

Section 12 (Comparative Analysis, Tables 8-9) is included here because it
operationalizes the architectural correspondence as a concrete cross-system
comparison.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 4.3: Dual-purpose graph -- the operational unification
# ---------------------------------------------------------------------------

claim_dual_purpose_graph = claim(
    "**The same graph stores cognitive memories AND manages agent-produced "
    "outputs.** Consider a multi-agent creative pipeline: an image-generation "
    "agent produces a concept-art revision; a video-compositing agent locates "
    "that revision via its URI, checks that it carries the `approved` tag, "
    "and creates its own output with a `Derived_From` edge linking back to "
    "the input; an audio agent does the same for the soundtrack; an editing "
    "agent assembles the final deliverable with typed edges to every "
    "upstream component. Each agent uses the graph both to **remember** "
    "(client preferences, past iterations, feedback history) and to "
    "**operate** (find the right input version, register its output, declare "
    "dependencies). Without this unification, agent-produced artifacts "
    "accumulate in disconnected storage -- files on disk, blobs in buckets, "
    "ephemeral context windows -- with no versioning, no provenance, and no "
    "link to the reasoning that generated them [@Park2026Kumiho, Sec. 4.3].",
    title="Dual-purpose graph: agents remember AND operate via the same graph",
)

claim_governance_via_same_graph = claim(
    "**Governance and multi-agent coordination are served by the same graph.** "
    "Operational coordination (each agent's output is the next agent's input) "
    "and governance auditability (decisions must be explainable by pointing "
    "to the actual evidence and reasoning chain) are served by the same "
    "graph, the same SDK, and the same API. Without this infrastructure, "
    "agent work products are untraceable and agent pipelines are unmanageable. "
    "The system makes agent memory as inspectable as a version-controlled "
    "codebase and as navigable as a managed asset database -- because "
    "structurally, it *is* both [@Park2026Kumiho, Sec. 5.2].",
    title="Same graph serves operational coordination AND human governance audit",
)

claim_governance_native = claim(
    "**Governance infrastructure is native, not bolted on.** As AI agents "
    "transition from experimental tools to production workers, organizations "
    "require the same governance, traceability, and accountability standards "
    "they apply to human employees. Industry frameworks -- ISACA's 2025 "
    "agentic-AI audit analysis, IBM's Agent Decision Records, enterprise "
    "platforms framing agents as governed workforce -- are emerging. The "
    "Kumiho architecture provides this governance natively: every agent "
    "belief has a URI, a revision history, provenance edges to source "
    "evidence, and an immutable audit trail -- the same accountability "
    "infrastructure organizations already apply to version-controlled code "
    "and managed digital assets [@Park2026Kumiho, Sec. 1; Sec. 5.2].",
    title="Governance via URI + revision history + provenance edges + audit trail",
)

# ---------------------------------------------------------------------------
# 12: Comparative analysis dimensions (Table 8)
# ---------------------------------------------------------------------------

claim_table8_comparative_dimensions = claim(
    "**Architectural comparison across nine evaluation dimensions (Table 8 "
    "of [@Park2026Kumiho]).**\n\n"
    "| Dimension | Flat RAG | Tiered Buffers | Extended Context | Static KG | Kumiho |\n"
    "|-----------|----------|----------------|------------------|-----------|--------|\n"
    "| Retrieval | Embedding only | Embedding+scan | In-context | Query language | Hybrid+graph nav |\n"
    "| Statefulness | Stateless | Tiered buffers | Ephemeral | Current state | Versioned history |\n"
    "| Relationships | None | None | None | Fixed ontology | 6 typed edge types |\n"
    "| Provenance | None | None | None | Schema-dependent | Complete lineage |\n"
    "| Temporal Nav. | Point-in-time | Current window | Current window | Mostly current | Full history+tags |\n"
    "| Consolidation | None | Manual/rule | N/A | Batch ETL | LLM Dream State |\n"
    "| LLM Coupling | Low | High | Complete | None | None (MCP) |\n"
    "| Cost Scaling | Linear | Linear | Quadratic | Linear | Linear |\n"
    "| Work Auditability | None | None | None | Partial | Full (SDK+desktop) |\n",
    title="Table 8: Kumiho is unique across 9 dimensions (versioned history + 6 edges + complete lineage + auditability)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 8",
        "caption": "Comparative analysis across nine evaluation dimensions.",
    },
)

claim_table9_feature_comparison = claim(
    "**Feature comparison with concurrent agent-memory systems (Table 9 of "
    "[@Park2026Kumiho], as of Feb 2026; check = present, (check) = partial, "
    "x = absent).**\n\n"
    "| Feature | Graphiti | Mem0g | A-MEM | Letta | MAGMA | Hindsight | MemOS | Kumiho |\n"
    "|---------|----------|-------|-------|-------|-------|-----------|-------|--------|\n"
    "| Property graph storage | check | check | (check) | x | check | x | x | check |\n"
    "| Hybrid retrieval | check | (check) | x | x | (check) | (check) | x | check |\n"
    "| Immutable revision history | (check) | (check) | x | (check) | x | x | x | check |\n"
    "| Formal belief revision | x | x | x | x | x | x | x | check |\n"
    "| URI-based addressing | x | x | x | x | x | x | x | check |\n"
    "| Typed edge ontology >=6 | (check) | x | (check) | x | (check) | x | x | check |\n"
    "| Async consolidation+safety | x | x | x | (check) | x | x | x | check |\n"
    "| LLM-decoupled | (check) | (check) | x | (check) | (check) | (check) | (check) | check |\n"
    "| Unified asset+memory graph | x | x | x | x | x | x | x | check |\n"
    "| Agent work auditability (SDK) | x | x | x | x | x | x | x | check |\n"
    "| Benchmark eval (LoCoMo/LME) | check | check | check | check | check | check | x | check |\n"
    "| BYO-storage | x | x | x | x | x | x | x | check |\n\n"
    "Across 12 features, only Kumiho fully satisfies all 12; in particular, "
    "**formal belief revision**, **URI-based addressing**, **unified asset + "
    "memory graph**, **agent work auditability**, and **BYO-storage** are "
    "unique to Kumiho among the surveyed systems "
    "[@Park2026Kumiho, Sec. 12; Table 9].",
    title="Table 9: Kumiho is unique on 5 features (formalism, URI, unified, audit, BYO-storage)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 9",
        "caption": "Feature comparison with concurrent agent-memory systems.",
    },
)

# ---------------------------------------------------------------------------
# 12.1-12.6: Per-baseline comparison points
# ---------------------------------------------------------------------------

claim_vs_flat_retrieval = claim(
    "**vs. Flat RAG retrieval systems.** Flat retrieval treats each query as "
    "an independent similarity search over static document chunks. Kumiho "
    "extends this along three axes: (i) **statefulness** -- memories evolve "
    "through revisions rather than being overwritten or duplicated; (ii) "
    "**structure** -- typed edges encode causal and evidential relationships; "
    "(iii) **consolidation** -- the Dream State actively distills episodic "
    "experience into semantic knowledge. Flat retrieval remains valuable as "
    "*one component* of a hybrid system: Kumiho incorporates vector "
    "similarity as one of two retrieval branches alongside fulltext search "
    "[@Park2026Kumiho, Sec. 12.1].",
    title="vs. Flat RAG: Kumiho adds statefulness + structure + consolidation",
)

claim_vs_tiered_buffers = claim(
    "**vs. Tiered buffer systems.** Tiered buffers introduce an OS metaphor "
    "but typically operate on flat stores without typed relationships or "
    "immutable versioning. More critically, the memory-management logic is "
    "embedded within the LLM's own reasoning, creating tight LLM-memory "
    "coupling. Kumiho provides richer structure (graph edges, revision "
    "history), stronger safety guarantees (circuit breakers, dry runs, "
    "published-item protection), and LLM-decoupled management (the memory "
    "graph is an external data store, not model-internal state) "
    "[@Park2026Kumiho, Sec. 12.2].",
    title="vs. Tiered buffers: Kumiho adds typed edges, immutable versions, LLM-decoupling",
)

claim_vs_static_kg = claim(
    "**vs. Static knowledge graphs.** Static KGs excel at shared encyclopedic "
    "knowledge with fixed schemas. Kumiho is designed for **experiential** "
    "memory -- agent-scoped, temporally-evolving, with flexible metadata and "
    "a working-memory layer. The two approaches are complementary: a "
    "memory-equipped agent could reference external KGs via `Referenced` "
    "edges while maintaining its own experiential memory in the graph "
    "[@Park2026Kumiho, Sec. 12.4].",
    title="vs. Static KGs: Kumiho targets experiential (agent-scoped, evolving) memory",
)

claim_vs_magma_unified_vs_multi = claim(
    "**vs. MAGMA: unified property graph vs. multi-graph separation.** "
    "MAGMA disentangles memory dimensions into separate graphs (semantic, "
    "temporal, causal, entity), enabling cleaner retrieval routing. Kumiho "
    "unifies all relationships in a single property graph with typed edges, "
    "enabling cross-dimensional traversal: `AnalyzeImpact` propagates across "
    "`Depends_On`, `Derived_From`, and `Supersedes` simultaneously, "
    "discovering dependencies that span multiple memory dimensions. The "
    "trade-off: multi-graph separation avoids cross-dimensional noise but "
    "introduces synchronization complexity for updates spanning multiple "
    "dimensions; the unified property graph accepts edge-type heterogeneity "
    "in exchange for **transactional atomicity** -- a single Neo4j "
    "transaction can create a revision, re-point tags, add `Supersedes` and "
    "`Derived_From` edges, and update provenance metadata, ensuring the "
    "belief state is never partially-updated. This atomicity is what enables "
    "the AGM compliance results: the formal postulates require atomic "
    "revision, and the unified graph makes this a database-level guarantee "
    "rather than an application-level coordination problem "
    "[@Park2026Kumiho, Sec. 12.5].",
    title="vs. MAGMA: unified graph buys atomicity (database-level AGM guarantee)",
)

claim_vs_hindsight_complementary = claim(
    "**vs. Hindsight: pragmatic vs. formally-grounded belief tracking.** "
    "Hindsight [@Hindsight2025] achieves the highest reported LoCoMo score "
    "(89.61%, percentage accuracy) and LongMemEval (91.4%) with confidence-"
    "scored beliefs that update with evidence -- functionally similar to "
    "Kumiho's revision mechanism but without AGM grounding. The relationship "
    "is complementary rather than competitive: Hindsight demonstrates the "
    "empirical value of structured belief tracking; Kumiho's formal "
    "framework provides theoretical guarantees (Relevance, Core-Retainment, "
    "Consistency) that such systems could adopt to ensure belief revision "
    "satisfies minimal change. Hindsight explicitly identifies safe "
    "personality management as an open problem; Kumiho's safety-hardened "
    "consolidation with circuit breakers and published-item protection "
    "addresses precisely this gap [@Park2026Kumiho, Sec. 12.6].",
    title="vs. Hindsight: complementary (Hindsight = empirical, Kumiho = formal)",
)

# ---------------------------------------------------------------------------
# 4.2 + 12.5: The cross-baseline architectural-synthesis claim
# ---------------------------------------------------------------------------

claim_cross_baseline_synthesis_gap = claim(
    "**Cross-baseline architectural-synthesis claim.** Aggregating the per-"
    "system gaps from Section 2.1 (Graphiti has retrieval+versioning but no "
    "formalism / no URI / no BYO-storage; Mem0 has timestamped versioning "
    "but no formalism; Letta has Git-backed versioning but lacks typed edges "
    "/ AGM / impact analysis; A-MEM has dynamic linking but no formalism or "
    "asset graph; MAGMA disentangles dimensions across graphs; Hindsight "
    "has empirical belief tracking but no AGM guarantees; MemOS has tiered "
    "buffers with LLM coupling) yields a population law: **no concurrent "
    "system simultaneously provides (i) formal belief-revision correspondence, "
    "(ii) typed-edge dependency reasoning at scale, (iii) URI-based "
    "deterministic addressing, AND (iv) unified asset + memory management.** "
    "This cross-baseline architectural gap is the empirical justification "
    "for Kumiho's unification thesis [@Park2026Kumiho, Sec. 2.1; Sec. 4.2; "
    "Sec. 12; Tables 1, 8, 9].",
    title="Architectural-synthesis gap: no prior system covers all 4 axes simultaneously",
)

__all__ = [
    "claim_dual_purpose_graph",
    "claim_governance_via_same_graph",
    "claim_governance_native",
    "claim_table8_comparative_dimensions",
    "claim_table9_feature_comparison",
    "claim_vs_flat_retrieval",
    "claim_vs_tiered_buffers",
    "claim_vs_static_kg",
    "claim_vs_magma_unified_vs_multi",
    "claim_vs_hindsight_complementary",
    "claim_cross_baseline_synthesis_gap",
]
