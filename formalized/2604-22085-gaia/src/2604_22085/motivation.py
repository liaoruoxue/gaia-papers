"""Motivation: memory as the primary architectural bottleneck for production-grade agents.

Section I (Introduction) and abstract of Abtahi et al. 2026 [@Abtahi2026Memanto].
The paper diagnoses a structural problem in the agentic-memory landscape: as
LLM-based systems shift from single-turn QA to multi-session autonomous
agents, the lack of persistent state becomes the central engineering
challenge. The dominant response in 2024-2026 has been to bolt knowledge
graphs onto vector retrieval ("hybrid graph + vector" architectures). The
paper argues this trend introduces substantial computational overhead -- the
"Memory Tax" -- and asks whether the underlying premise (that graphs are
necessary for high-fidelity agent memory) is even correct.

Memanto is the proposed counter-architecture: a vector-only memory layer
backed by Moorcheh's Information Theoretic Search engine, augmented with a
13-category typed schema, automated conflict resolution, and temporal
versioning. The headline empirical preview: SOTA accuracy on LongMemEval
(89.8%) and LoCoMo (87.1%) using a single retrieval per query, zero LLM
invocations at ingestion, and sub-90 ms retrieval latency.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setting (the deployment regime the paper targets)
# ---------------------------------------------------------------------------

setup_agentic_regime = setting(
    "**Production agentic AI regime.** The paper targets autonomous large "
    "language model (LLM) agents that operate across many sessions, perform "
    "multi-step reasoning, and invoke tools to execute long-horizon tasks "
    "[@Yao2023ReAct; @Wang2024Survey]. In this regime the agent must "
    "maintain *persistent state* across sessions: facts, decisions, "
    "preferences, commitments, and observations gathered in earlier "
    "sessions must remain retrievable in later sessions. A bare LLM is "
    "stateless across calls, so persistent memory must be supplied by an "
    "external subsystem [@Abtahi2026Memanto, Sec. I].",
    title="Setup: production agentic AI requires persistent cross-session memory",
)

setup_memory_subsystem = setting(
    "**Memory subsystem with three operations.** The memory subsystem must "
    "support three operations: (i) **ingestion** -- writing a new memory "
    "entry into persistent store; (ii) **retrieval** -- querying the store "
    "for entries relevant to the agent's current task; and (iii) "
    "**reading** -- consuming retrieved entries as context for the LLM. "
    "Each operation is characterised by *accuracy* (does the system return "
    "the right entries / produce the right answer?), *latency* (how "
    "long?), and *cost* (LLM tokens, infrastructure, operational "
    "complexity) [@Abtahi2026Memanto, Sec. I; @LongMemEval].",
    title="Setup: memory subsystem = ingest + retrieve + read; each has accuracy/latency/cost",
)

setup_production_constraints = setting(
    "**Production constraints.** Production deployment of agentic memory "
    "imposes constraints beyond raw accuracy: (a) **low latency** for "
    "interactive use; (b) **cost efficiency** for high-volume traffic "
    "(industry projections cited in [@Abtahi2026Memanto, Sec. I]: agentic "
    "AI market 7.8B USD growing to >52B USD by 2030; Gartner estimates 40% "
    "of enterprise applications will incorporate AI agents by end-2026 vs "
    "<5% in 2025); (c) **operational simplicity** -- fewer infrastructure "
    "components to provision, scale, monitor, and maintain.",
    title="Setup: production = accuracy + low latency + cost efficiency + operational simplicity",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Is knowledge-graph (KG) complexity actually necessary to achieve "
    "high-fidelity long-horizon agent memory, or can a vector-only "
    "architecture with structured memory typing and information-"
    "theoretic retrieval match or exceed hybrid KG+vector systems "
    "while incurring a fraction of their operational overhead?",
    title="Central question: is KG complexity necessary for high-fidelity agent memory?",
)

# ---------------------------------------------------------------------------
# Diagnosis: the prevailing-KG architecture and its costs
# ---------------------------------------------------------------------------

claim_memory_is_bottleneck = claim(
    "**Memory is the primary architectural bottleneck for production "
    "agents.** As LLMs transition from single-turn question answering to "
    "autonomous agents capable of multi-step reasoning, tool utilisation, "
    "and long-horizon task execution [@Yao2023ReAct], their lack of "
    "persistent state across sessions becomes the central engineering "
    "challenge. Industry adoption is accelerating (projected market "
    "growth 7.8B USD -> >52B USD by 2030; Gartner: 40% of enterprise "
    "applications will incorporate AI agents by end-2026 vs <5% in 2025), "
    "creating an immediate need for memory infrastructure that meets "
    "production requirements simultaneously [@Abtahi2026Memanto, Sec. I].",
    title="Diagnosis: memory is the primary bottleneck for production agentic AI",
)

claim_kg_hybrid_is_dominant = claim(
    "**The dominant production paradigm in 2024-2026 is hybrid graph + "
    "vector memory.** Major frameworks -- Mem0 [@Mem0], Zep [@Zep], Letta "
    "(MemGPT) [@MemGPT], and A-MEM [@AMEM] -- couple dense vector "
    "retrieval with explicit knowledge graphs and/or temporal graph "
    "databases, plus multi-query retrieval pipelines and recursive "
    "LLM-driven ingestion. While these systems achieve competitive "
    "benchmark numbers, the architectural envelope has steadily grown "
    "more complex year-over-year (Fig. 1 of [@Abtahi2026Memanto] traces "
    "Letta 2023 -> Mem0/Zep 2024-25 -> A-MEM/Supermemory 2025-26).",
    title="Diagnosis: the dominant 2024-2026 paradigm is hybrid graph + vector memory",
)

claim_memory_tax = claim(
    "**The 'Memory Tax' is the cumulative compute, latency, and complexity "
    "overhead imposed by hybrid KG+vector memory architectures.** The "
    "paper formally names this phenomenon: ingestion requires LLM-mediated "
    "entity extraction (consuming tokens, inflating write latency), the "
    "graph layer requires schema maintenance, retrieval requires "
    "multi-query orchestration, and the joint stack needs separate "
    "vector and graph database instances to be provisioned, scaled, and "
    "monitored. Concretely, every memory insertion in the graph-augmented "
    "configuration triggers a synchronous multi-stage pipeline (LLM "
    "extraction + vector index update + graph synchronisation), turning "
    "low-latency writes into multi-second blocking calls "
    "[@Abtahi2026Memanto, Sec. I; Sec. II.C].",
    title="Diagnosis: the 'Memory Tax' = compute + latency + complexity overhead of KG hybrids",
)

claim_kg_assumption_is_prevailing = claim(
    "**The prevailing assumption is that knowledge-graph complexity is "
    "*necessary* for high-fidelity agent memory.** Across the dominant "
    "frameworks [@Mem0; @Zep; @MemGPT; @AMEM], the implicit architectural "
    "premise is that explicit relational structure (entities, edges, "
    "schemas) is required to achieve competitive benchmark accuracy on "
    "long-horizon tasks. Memanto's central architectural thesis is that "
    "this premise is *false*: typed semantic schema + information-"
    "theoretic vector retrieval can match or exceed KG-hybrid accuracy "
    "without any graph layer at all [@Abtahi2026Memanto, abstract; "
    "Sec. I; Sec. V.A].",
    title="Diagnosis: prevailing view treats KG complexity as necessary for high-fidelity memory",
)

# ---------------------------------------------------------------------------
# Proposed remedy at the conceptual level
# ---------------------------------------------------------------------------

claim_memanto_thesis = claim(
    "**Memanto's architectural thesis: highly optimised semantic retrieval "
    "+ structured memory typing + automated conflict resolution can match "
    "and surpass hybrid graph-vector architectures while eliminating "
    "ingestion overhead, reducing retrieval to a single query, and "
    "removing the need for schema management.** Memanto is built upon "
    "Moorcheh's Information Theoretic Search engine -- a no-indexing "
    "semantic database based on Information Theoretic Vector Compression "
    "[@MoorchehITS] -- and adds a 13-category typed memory schema, an "
    "automated conflict resolution mechanism, and temporal versioning "
    "[@Abtahi2026Memanto, Sec. I; Sec. III; Sec. IV].",
    title="Thesis: typed schema + IT-search beats KG hybrids without the Memory Tax",
)

# ---------------------------------------------------------------------------
# Headline empirical preview
# ---------------------------------------------------------------------------

claim_headline_longmemeval = claim(
    "**Headline empirical result -- LongMemEval 89.8%.** On the "
    "LongMemEval $S$ benchmark (500 manually curated questions across six "
    "memory categories, embedded in dialogues spanning approximately 115K "
    "tokens / approximately 50 sessions, with Claude Sonnet 4 as LLM "
    "judge) [@LongMemEval], Memanto in its final Stage-5 configuration "
    "(retrieval limit $k=100$, ITS similarity threshold = 0.05, Gemini 3 "
    "inference) achieves 89.8% overall accuracy [@Abtahi2026Memanto, "
    "Table VII; Fig. 5].",
    title="Preview: Memanto reaches 89.8% on LongMemEval (Stage 5)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 5 / Table VII",
        "caption": "Progressive ablation waterfall and per-category LongMemEval accuracy.",
    },
)

claim_headline_locomo = claim(
    "**Headline empirical result -- LoCoMo 87.1%.** On the LoCoMo "
    "benchmark (long-form multi-session dialogues with single-hop, "
    "multi-hop, open-domain, and temporal reasoning categories, "
    "individual dialogues up to 35 sessions / 300 turns / approximately "
    "9K tokens) [@LoCoMo], Memanto in its final Stage-5 configuration "
    "achieves 87.1% overall accuracy [@Abtahi2026Memanto, Table VIII; "
    "Fig. 5].",
    title="Preview: Memanto reaches 87.1% on LoCoMo (Stage 5)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 5 / Table VIII",
        "caption": "Progressive ablation waterfall and per-category LoCoMo accuracy.",
    },
)

claim_single_query_efficiency = claim(
    "**Memanto issues a single retrieval query per question, with no LLM "
    "invocation at ingestion.** Memanto's final evaluation configuration "
    "uses a dynamic retrieval budget of up to 100 chunks (governed by ITS "
    "threshold = 0.05) issued via *one* retrieval query per question; no "
    "multi-query or recursive retrieval strategies are applied "
    "[@Abtahi2026Memanto, Appendix D]. Ingestion writes raw conversational "
    "content into Moorcheh with zero LLM invocations, so write-to-search "
    "availability is sub-10 ms [@Abtahi2026Memanto, Table X]. By contrast, "
    "hybrid KG+vector competitors (Mem0g, Zep, EmergenceMem, Supermemory, "
    "Hindsight) issue multiple parallel or recursive queries and incur "
    "0.5-3 second ingestion latency due to LLM-mediated entity extraction "
    "[@Abtahi2026Memanto, Tables IX-X].",
    title="Preview: single-query retrieval + zero-LLM ingestion (vs multi-query + LLM extraction in baselines)",
)

# ---------------------------------------------------------------------------
# Headline contributions claim (the paper's announced takeaway)
# ---------------------------------------------------------------------------

claim_headline_contribution = claim(
    "**Headline contribution: a vector-only agentic memory architecture "
    "that achieves SOTA on LongMemEval (89.8%) and LoCoMo (87.1%) while "
    "eliminating the Memory Tax.** Memanto combines (i) a typed memory "
    "schema with 13 semantic categories, (ii) integrated conflict "
    "resolution, (iii) temporal versioning, and (iv) Moorcheh's "
    "Information Theoretic Search engine -- without knowledge graphs, "
    "multi-query retrieval, or LLM-mediated ingestion. The system also "
    "(v) formally quantifies the Memory Tax of competing architectures "
    "and (vi) proposes six design principles (D1-D6) for production "
    "agentic memory [@Abtahi2026Memanto, Sec. I.A]. Reference "
    "implementation: [@MemantoCode].",
    title="Headline contribution: Memanto = SOTA on LongMemEval / LoCoMo at zero Memory Tax",
)

__all__ = [
    "setup_agentic_regime",
    "setup_memory_subsystem",
    "setup_production_constraints",
    "q_central",
    "claim_memory_is_bottleneck",
    "claim_kg_hybrid_is_dominant",
    "claim_memory_tax",
    "claim_kg_assumption_is_prevailing",
    "claim_memanto_thesis",
    "claim_headline_longmemeval",
    "claim_headline_locomo",
    "claim_single_query_efficiency",
    "claim_headline_contribution",
]
