"""Concrete Kumiho instantiation: hybrid retrieval (Section 8), Dream State
asynchronous consolidation (Section 9), privacy architecture (Section 10),
MCP integration (Section 11), and the reference implementation (Section 14).

This module captures the *engineering contributions* surrounding the formal
core: the retrieval pipeline, the safety architecture, the privacy boundary,
and the MCP tool taxonomy.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 8.1-8.4: Hybrid retrieval pipeline
# ---------------------------------------------------------------------------

setup_hybrid_pipeline = setting(
    "**Two-branch hybrid retrieval pipeline.** Given a query $q$, the "
    "pipeline combines two scoring signals within a single Cypher query "
    "(UNION ALL): \n"
    "1. **Fulltext (BM25)** -- BM25-scored fulltext index query with Lucene; "
    "Levenshtein fuzzy matching (edit distance 1 for terms >2 characters); "
    "available on all tiers.\n"
    "2. **Vector similarity** -- query embedded via configurable model "
    "(default: 1536-dim text embeddings); cosine similarity computed against "
    "revision embedding vectors using the database's native vector index; "
    "available on higher tiers.\n\n"
    "Branch-specific scores: $s_\\ell(m) = \\mathrm{BM25}(q,m)$, "
    "$s_v(m) = \\beta \\cdot \\cos(e(q), e(m))$ with $\\beta = 0.85$. "
    "Type-aware weight $w(m) \\in \\{1.0, 0.9, 0.8\\}$ for "
    "item/revision/artifact matches. Final score: $S(q,m) = w(m) \\cdot "
    "\\max(s_\\ell(m), s_v(m))$ -- max-based fusion (CombMAX in [@FoxShaw1993]) "
    "[@Park2026Kumiho, Sec. 8.2].",
    title="Setup: hybrid retrieval = BM25 + vector via CombMAX with beta=0.85, type weights {1.0, 0.9, 0.8}",
)

claim_combmax_design_choice = claim(
    "**CombMAX (max-based fusion) is a deliberate design choice for "
    "precision preservation.** Max-based fusion selects the single "
    "strongest signal for each candidate. Unlike Reciprocal Rank Fusion "
    "(RRF) [@Cormack2009RRF], which sums over rank positions, or linear "
    "combination methods, which compute weighted averages, CombMAX ensures "
    "that when a memory matches strongly on one modality (e.g., exact "
    "lexical match), a weak score from another modality (e.g., low cosine "
    "similarity due to vocabulary mismatch) does not dilute the result. "
    "This is an argumentative design choice motivated by precision "
    "preservation, not a theoretical superiority result; comparative "
    "evaluation against RRF and convex combination is planned future work "
    "[@Park2026Kumiho, Sec. 8.2; Sec. 16].",
    title="CombMAX: design choice for precision preservation (vs. RRF/convex combination, comp. eval. pending)",
)

# ---------------------------------------------------------------------------
# 8.5: Three engineering observations
# ---------------------------------------------------------------------------

claim_coverage_complementarity = claim(
    "**Observation 1 (Coverage Complementarity).** Hybrid recall "
    "$\\mathrm{Recall}_H(q) \\geq \\max_b \\mathrm{Recall}_b(q)$ follows "
    "trivially from set union; the non-trivial design claim is that each "
    "modality covers cases the other systematically misses. Witness: a "
    "query for 'shade' returns no results from fulltext (the relevant "
    "memory is stored as 'favorite color is blue') but is retrieved by "
    "vector via semantic proximity; conversely, exact-match queries that "
    "vector embeddings would dilute are caught by BM25 "
    "[@Park2026Kumiho, Sec. 8.5.1].",
    title="Observation 1: coverage complementarity (each modality catches what the other misses)",
)

claim_precision_preservation = claim(
    "**Observation 8.1 (Precision Preservation under Max-Fusion).** "
    "$P_H@k(q) \\geq \\max_{b \\in \\{\\ell, v\\}} P_b@k(q)$ -- the hybrid "
    "ranking never has lower precision than the best individual branch, "
    "provided score calibration is adequate. Argument: the merged score "
    "$S(q,m) = w(m) \\cdot \\max(s_\\ell(m), s_v(m))$ assigns each memory "
    "a score at least as high as its strongest branch-specific score; a "
    "displacing memory must score highly on a different branch and is "
    "therefore a genuine strong match on some modality. **Caveat**: "
    "CombMAX is susceptible to noise from poorly-calibrated retrievers "
    "producing inflated scores [@Bruch2023Fusion]; the $\\beta = 0.85$ "
    "calibration partially mitigates this for vector scores but is not "
    "empirically validated [@Park2026Kumiho, Sec. 8.5.2].",
    title="Observation 8.1: max-fusion preserves precision (precision >= best branch, calibration-bounded)",
)

claim_recall_non_degradation = claim(
    "**Observation 2 (Recall Non-Degradation).** In the unbounded retrieval "
    "case, adding memories to the corpus cannot reduce the set of retrieved "
    "true positives -- a property of any non-destructive index. In the "
    "$k$-bounded case, displacement effects can occur, but the precision "
    "preservation argument (Observation 8.1) ensures true positives with "
    "strong signals on any branch resist displacement. Empirical "
    "measurement of recall stability under corpus growth is planned "
    "[@Park2026Kumiho, Sec. 8.5.3].",
    title="Observation 2: recall non-degradation under corpus growth (k-bounded displacement mitigated)",
)

# ---------------------------------------------------------------------------
# 8.8: Client-side LLM reranking
# ---------------------------------------------------------------------------

claim_client_side_reranking = claim(
    "**Client-side LLM reranking via two-stage filtering.** When recall "
    "returns stacked items (multiple revisions about the same topic), "
    "Kumiho selects the most relevant sibling revision via: \n"
    "**Stage 1 (Embedding pre-filter)**: filter by cosine similarity to the "
    "query using `text-embedding-3-small` with threshold 0.30 (cost <$0.001 "
    "per query).\n"
    "**Stage 2 (LLM reranking)**: surviving siblings are presented to the "
    "consuming agent's own LLM with structured metadata (title, summary, "
    "extracted facts, entities, events, implications) alongside the original "
    "query. Three configuration modes:\n\n"
    "| Mode | Context | Reranker | Cost |\n"
    "|------|---------|----------|------|\n"
    "| client | Agent via MCP | Host agent LLM | Zero |\n"
    "| dedicated | API/Playground | User's model | User's key |\n"
    "| auto | Any | Detect context | Adaptive |\n\n"
    "In the `client` mode, the host agent (Claude, GPT-4o, etc.) performs "
    "reranking as part of its normal response generation -- subsumed into "
    "the agent's existing inference call at zero additional cost. This "
    "embodies the LLM-Decoupled Memory principle: the memory layer "
    "provides structured data; the consumer's own intelligence performs "
    "selection. As agent models improve, reranking quality improves "
    "automatically [@Park2026Kumiho, Sec. 8.8; Table 5].",
    title="Client-side LLM reranking: zero-cost via host agent's normal inference (LLM-decoupled principle)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 5",
        "caption": "LLM reranking configuration modes.",
    },
)

# ---------------------------------------------------------------------------
# 9.1-9.3: Dream State pipeline
# ---------------------------------------------------------------------------

setup_dream_state_pipeline = setting(
    "**Nine-stage Dream State asynchronous consolidation pipeline.** "
    "Modeled on biological sleep consolidation [@RaschBorn2013] and "
    "extending Letta's sleep-time compute [@LettaSleepTime2025], the "
    "pipeline processes the system's event stream "
    "(`revision.created`, `edge.created`, `revision.deprecated`) with "
    "cursor-based semantics: \n"
    "1. Ensure Cursor (create `_dream_state` space if missing)\n"
    "2. Load Cursor (read persisted position)\n"
    "3. Collect Events (deduplicate, latest revision wins)\n"
    "4. Fetch Revisions (filter to episodic, exclude deprecated)\n"
    "5. Inspect Bundles (membership lists for context)\n"
    "6. **LLM Assessment** (configurable batch size, default 20: relevance "
    "scoring, deprecation recommendations, tag suggestions, metadata "
    "corrections, relationship identification)\n"
    "7. Apply Actions (under safety guards)\n"
    "8. Save Cursor (persist new position)\n"
    "9. Generate Report (Markdown audit artifact)\n\n"
    "Triggers: scheduled (e.g., nightly), event idle detection, memory "
    "count threshold, explicit API/MCP invocation "
    "[@Park2026Kumiho, Sec. 9.2-9.3].",
    title="Setup: Dream State 9-stage cursor-based pipeline (event stream, LLM assessment, audit report)",
)

claim_dream_state_safety_guards = claim(
    "**Six Dream State safety guards (Table 6 of [@Park2026Kumiho]).**\n\n"
    "| Guard | Mechanism |\n"
    "|-------|-----------|\n"
    "| Dry Run | Assessment-only mode |\n"
    "| Published Protect | Never deprecate 'published' |\n"
    "| Circuit Breaker | Max 50% deprecation per batch |\n"
    "| Error Isolate | Per-action try/except |\n"
    "| Audit Report | Markdown report artifact |\n"
    "| Cursor Persist | Resume from checkpoint |\n\n"
    "**Circuit breaker**: if the LLM recommends deprecating more than 50% "
    "of assessed memories in a single run, this likely indicates a "
    "miscalibrated prompt or adversarial input. The system caps "
    "deprecations at 50% and logs a warning. **Tunability**: "
    "`max_deprecation_ratio` parameter (default 0.5, valid 0.1-0.9; "
    "high-stakes domains like medical/legal/financial use 0.2-0.3; batch "
    "cleanup uses 0.7-0.9 after dry-run). **Published-item protection** "
    "is bypassable only via explicit `allow_published_deprecation=true` "
    "flag, logged for traceability. To Park's knowledge, these specific "
    "safety mechanisms are absent from prior consolidation systems "
    "[@Park2026Kumiho, Sec. 9.5; Table 6].",
    title="Six safety guards (Table 6): dry-run, published protect, circuit breaker, isolate, audit, cursor",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 6",
        "caption": "Dream State safety guards.",
    },
)

claim_consolidation_formal_status = claim(
    "**Formal status of the Dream State pipeline.** The nine-stage pipeline "
    "is an *engineering* contribution, not a formal one. Each individual "
    "action maps to a formally-defined operation: deprecation is contraction "
    "(Definition 7.5), metadata enrichment is expansion (Definition 7.7), "
    "and relationship creation adds edges to $E$. However, Park does "
    "**not** claim that the composition of a batch of such actions across "
    "multiple memories preserves all AGM postulates simultaneously -- "
    "proving compositional preservation under sequential application is an "
    "open problem in belief-revision theory. What the safety guards "
    "provide is not formal guarantees but operational constraints "
    "(published-item immunity, circuit breakers, dry-run validation) that "
    "limit the damage from incorrect LLM assessments "
    "[@Park2026Kumiho, Sec. 9.4 'Formal status of consolidation'].",
    title="Dream State formal status: per-action ok; compositional preservation = open problem",
)

# ---------------------------------------------------------------------------
# 10: Privacy architecture
# ---------------------------------------------------------------------------

setup_privacy_boundary = setting(
    "**Local-first, summary-to-cloud privacy boundary.** Raw content "
    "(chat transcripts, voice recordings, images, tool output, user PII) "
    "remains local to the agent runtime. Only PII-redacted summaries, "
    "extracted facts, topic keywords, artifact pointers (paths, not "
    "content), and embedding vectors cross the boundary into the cloud "
    "graph. PII redaction is applied during the ingest pipeline before "
    "any data reaches the graph database, using an LLM through the "
    "pluggable adapter interface [@Park2026Kumiho, Sec. 10.1].",
    title="Setup: local-first privacy boundary (raw content stays local, PII-redacted summaries to cloud)",
)

claim_byo_storage_benefits = claim(
    "**BYO-storage architecture yields four critical privacy and "
    "compliance benefits.** Artifacts are pointers to files on the user's "
    "own storage; the system never copies, caches, or proxies artifact "
    "content. Consequences: (i) users control data residency and "
    "retention; (ii) the graph database contains no raw user content; "
    "(iii) data exfiltration from the graph yields only metadata; (iv) "
    "compliance with data sovereignty regulations is simplified. This "
    "design reflects the Metadata Over Content principle "
    "[@Park2026Kumiho, Sec. 10.2; Principle 6].",
    title="BYO-storage benefits: data residency + zero raw content + exfiltration-resistant + compliance",
)

claim_threat_model = claim(
    "**Threat model and mitigations (Table 7 of [@Park2026Kumiho]).**\n\n"
    "| Threat | Mitigation |\n"
    "|--------|-----------|\n"
    "| PII leakage via summaries | LLM-based redaction before graph ingest. Limitation: non-zero false negative rates. |\n"
    "| Membership inference via embeddings | Per-tenant embeddings in isolated DB partitions. Limitation: embedding inversion is active research. |\n"
    "| Prompt injection in Dream State | Consolidation operates on stored metadata, not raw user input; safety guards limit blast radius. |\n"
    "| Metadata re-identification | Topics/keywords can be identifying. Limitation: redaction targets named entities, not topical fingerprints. |\n"
    "| Malicious artifacts via tool output | Artifact pointers, not content; graph never executes/parses artifact data. |\n"
    "| Credential leakage | Ingest pipeline rejects known credential patterns (API keys, tokens). |\n\n"
    "Park acknowledges that LLM-based PII redaction is **not a formal "
    "privacy guarantee** -- false negatives and over-redaction are inherent "
    "to the approach; for HIPAA / GDPR Article 9 data, operators should "
    "deploy a dedicated redaction model with measured precision/recall "
    "[@Park2026Kumiho, Sec. 10.4; Table 7].",
    title="Threat model (Table 7): six threats with mitigations + acknowledged formal-guarantee limits",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 7",
        "caption": "Threat model and mitigations for the memory privacy boundary.",
    },
)

# ---------------------------------------------------------------------------
# 11: MCP integration
# ---------------------------------------------------------------------------

claim_mcp_breadth_distinguisher = claim(
    "**MCP integration is necessary but not differentiating; the breadth "
    "of graph operations exposed is what distinguishes Kumiho.** MCP-based "
    "memory systems are now table stakes for adoption (official MCP Memory "
    "Server, Mem0 MCP Server, Redis Agent Memory Server, Neo4j MCP "
    "Servers, MemoryOS-MCP, Basic Memory). What distinguishes Kumiho's "
    "MCP interface is the **breadth of graph operations exposed**: not "
    "just store/retrieve, but reasoning and provenance tools "
    "(`AnalyzeImpact`, `FindPath`, `GetProvenance`) and temporal "
    "point-in-time queries that other MCP memory servers do not provide "
    "[@Park2026Kumiho, Sec. 11.1].",
    title="MCP: necessary for adoption, but breadth of graph operations is the distinguisher",
)

claim_mcp_51_tools = claim(
    "**The MCP server exposes 51 tools across six categories.** "
    "(i) **Cognitive Memory Lifecycle** (memory_ingest, memory_recall, "
    "memory_consolidate, memory_discover_edges, memory_store_execution, "
    "memory_dream_state, memory_add_response); (ii) **Working Memory** "
    "(chat_add, chat_get, chat_clear); (iii) **Graph Navigation** "
    "(get_project, get_spaces, get_item, get_revision, get_artifacts, "
    "search_items); (iv) **Reasoning & Provenance** (get_edges, "
    "get_dependencies, get_dependents, analyze_impact, find_path, "
    "get_provenance_summary); (v) **Temporal Operations** "
    "(get_item_revisions, get_revision_by_tag, get_revision_as_of, "
    "resolve_kref); (vi) **Graph Mutation** (create_item, create_revision, "
    "tag_revision, create_edge, set_metadata, deprecate_item, +13 "
    "additional CRUD operations). The 'one tool call, complete memory' "
    "atomicity is enforced at the MCP boundary "
    "[@Park2026Kumiho, Sec. 11.2-11.3].",
    title="MCP: 51 tools across 6 categories with atomic-write semantics",
)

claim_human_audit_dashboard = claim(
    "**Human-audit dashboard renders the same graph hierarchy used by "
    "agents.** A web dashboard at https://kumiho.io and a companion "
    "desktop asset browser render the cognitive memory graph using the "
    "same project/space/item/revision hierarchy, enabling operators to "
    "inspect what an agent remembered, why, and when through immutable "
    "revision history, lineage traversal, and artifact inspection. Every "
    "consolidation decision is traceable to a Dream State report; every "
    "memory has a provenance chain. The same project/space/item/revision "
    "hierarchy serves both asset browsing and memory inspection, "
    "ensuring agent cognitive state is as navigable as a traditional "
    "asset management system [@Park2026Kumiho, Sec. 11.4; Sec. 14].",
    title="Human-audit dashboard: same graph hierarchy serves agent operation AND human inspection",
    metadata={
        "figure": "artifacts/2603.17244.pdf, Figure 1",
        "caption": "Kumiho dashboard showing the AI Cognitive Memory browser with force-directed graph visualization.",
    },
)

# ---------------------------------------------------------------------------
# 14: Reference implementation
# ---------------------------------------------------------------------------

claim_reference_implementation = claim(
    "**Reference implementation: Kumiho.** The architecture is fully "
    "implemented [@KumihoCode]: \n"
    "- **Kumiho Server** -- Rust-based gRPC server using `tokio`, `tonic`, "
    "`neo4rs` for graph operations, dynamic connection routing, embedding "
    "generation, hybrid search.\n"
    "- **Kumiho SDK** -- Python SDK with typed access, kref validation, "
    "retry logic.\n"
    "- **Kumiho MCP Server** -- Python MCP server wrapping the SDK.\n"
    "- **Kumiho Memory Library** -- Python library with session "
    "management, memory ingest with auto-recall, PII-redacted "
    "summarization with consolidation enrichments (prospective indexing, "
    "event extraction), Dream State pipeline.\n"
    "- **Kumiho Dashboard** -- Web UI at https://kumiho.io with AI "
    "Cognitive Memory browser + Asset Browser.\n"
    "- **Kumiho Desktop** -- Cross-platform Flutter/Dart desktop browser.\n\n"
    "Measured end-to-end latencies: 15ms typical for working memory, "
    "80-120ms for long-term graph queries including hybrid search "
    "[@Park2026Kumiho, Sec. 14].",
    title="Reference implementation: Server (Rust gRPC) + SDK + MCP + Library + Dashboard + Desktop",
)

__all__ = [
    "setup_hybrid_pipeline",
    "setup_dream_state_pipeline",
    "setup_privacy_boundary",
    "claim_combmax_design_choice",
    "claim_coverage_complementarity",
    "claim_precision_preservation",
    "claim_recall_non_degradation",
    "claim_client_side_reranking",
    "claim_dream_state_safety_guards",
    "claim_consolidation_formal_status",
    "claim_byo_storage_benefits",
    "claim_threat_model",
    "claim_mcp_breadth_distinguisher",
    "claim_mcp_51_tools",
    "claim_human_audit_dashboard",
    "claim_reference_implementation",
]
