"""Section II: Background and Related Work.

Section II of [@Abtahi2026Memanto] situates Memanto in the broader memory
landscape: cognitive foundations (Tulving, Baddeley), survey taxonomies
(Zhang, Arunkumar, Wang, Sumers), the dominant KG-hybrid frameworks (Mem0,
Zep, MemGPT/Letta, A-MEM, Hindsight), the indexing/ingestion bottleneck
(HNSW/RAG/HippoRAG/RAPTOR/REPLUG), and the principal evaluation benchmarks
(LongMemEval, LoCoMo, MemoryBank, PerLTQA, DialSim, MemoryAgentBench).

The section's central rhetorical move is to characterise each KG-hybrid
framework's *cost structure*, then cite emerging evidence (Merrill et al.
2026, Mem0's own ablation) that simpler retrieval-based systems can match
the more elaborate hierarchies on existing benchmarks.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# II.A Cognitive foundations
# ---------------------------------------------------------------------------

setup_tulving_taxonomy = setting(
    "**Tulving's cognitive memory taxonomy.** Tulving's foundational work "
    "[@Tulving1972] distinguishes three memory types: (i) *episodic* "
    "memory (event-specific, temporally situated experiences), (ii) "
    "*semantic* memory (general knowledge and factual information), and "
    "(iii) *procedural* memory (skills and behavioural rules). Memanto "
    "imports this taxonomy as a design constraint: typed memory "
    "separation is a desideratum (D4) and the 13-category schema is a "
    "more granular instantiation [@Abtahi2026Memanto, Sec. II.A; "
    "Sec. III.D].",
    title="Setup: Tulving's episodic / semantic / procedural memory taxonomy",
)

setup_baddeley_correspondence = setting(
    "**Baddeley working-memory correspondence.** Baddeley's working-"
    "memory model [@Baddeley1992] (phonological loop, visuospatial "
    "sketchpad, central executive) has a strong conceptual "
    "correspondence with retrieval-augmented generation (RAG) "
    "architectures [@RAG]: phonological loop = in-context token buffer; "
    "visuospatial sketchpad = structured retrieval representations; "
    "central executive = the agent's reasoning and control mechanisms "
    "[@Abtahi2026Memanto, Sec. II.A].",
    title="Setup: Baddeley's working-memory model maps to RAG architecture",
)

claim_episodic_matters_for_long_horizon = claim(
    "**Episodic memory is essential for long-horizon agent behaviour.** "
    "MacPherson et al. [@EpisodicLLM] argue that episodic representations "
    "enable temporal specificity and contextual binding that semantic "
    "retrieval alone cannot achieve. ENGRAM [@ENGRAM] operationalises "
    "this insight by implementing three distinct memory types with a "
    "unified routing and retrieval mechanism, and demonstrates that "
    "typed memory separation significantly improves performance on both "
    "LongMemEval and LoCoMo. Memanto extends this principle through a "
    "more granular 13-category schema [@Abtahi2026Memanto, Sec. II.A].",
    title="Episodic memory matters for long-horizon agents; typed separation outperforms undifferentiated storage",
)

# ---------------------------------------------------------------------------
# II.B Memory surveys and taxonomies
# ---------------------------------------------------------------------------

claim_survey_landscape = claim(
    "**Survey landscape (2024-2026): heterogeneous memory architectures, "
    "no consensus.** Zhang et al. [@Zhang2026MemorySurvey] categorise "
    "memory along three dimensions (forms, functions, dynamics), "
    "identifying token-level, parametric, and latent representations as "
    "primary. Abou Ali et al. [@AbouAli2025] propose a dual-paradigm "
    "framework distinguishing symbolic / classical from neural / "
    "generative approaches. Arunkumar et al. [@Arunkumar2026AgenticArch] "
    "describe a four-layer architecture (perception, memory, agent core, "
    "action). Wang et al. [@Wang2024Survey] identify long-term memory as "
    "a central unresolved challenge for LLM-based agents. Sumers et al. "
    "[@Sumers2023] formalise the cognitive-architecture / agent-system "
    "correspondence. Across these surveys, no consensus has emerged on "
    "the *correct* memory architecture for production agents "
    "[@Abtahi2026Memanto, Sec. II.B].",
    title="The survey landscape (2024-26) is heterogeneous; no consensus architecture",
)

# ---------------------------------------------------------------------------
# II.C KG-based memory systems and their costs
# ---------------------------------------------------------------------------

claim_memgpt_letta_overhead = claim(
    "**MemGPT / Letta: virtual-memory abstraction with summarisation cost.** "
    "MemGPT / Letta [@MemGPT] introduces an OS-inspired virtual memory "
    "abstraction in which information is dynamically paged between "
    "context and external storage. The approach relies on recursive "
    "summarisation and hierarchical compression, which introduce latency "
    "variability and loss of information fidelity, particularly when "
    "precise textual recall is required [@Abtahi2026Memanto, Sec. II.C].",
    title="MemGPT/Letta: paging + summarisation = latency variability + fidelity loss",
)

claim_mem0_marginal_graph_gain = claim(
    "**Mem0: three-tier hybrid; graph yields only marginal gains.** Mem0 "
    "[@Mem0] implements a three-tier memory hierarchy (user, session, "
    "agent) combining vector retrieval, graph-based relational storage, "
    "and key-value indexing. Its own ablation results indicate the graph-"
    "augmented variant yields only *marginal* improvements over the base "
    "vector configuration (cited as approximately 2 percentage points "
    "[@Abtahi2026Memanto, Sec. V.A]). This raises questions regarding "
    "the necessity of graph infrastructure relative to its compute and "
    "operational costs.",
    title="Mem0's own ablation: graph variant adds only ~2pp over base vector configuration",
)

claim_mem0_pipeline_cost = claim(
    "**Mem0 ingestion pipeline = LLM extraction + index update + graph "
    "sync, multi-second per write.** In the graph-augmented Mem0 "
    "configuration, each memory insertion triggers a synchronous "
    "multi-stage pipeline: (i) LLM-driven entity extraction, (ii) vector "
    "embedding and index updates, (iii) graph synchronisation. This "
    "transforms low-latency write operations into multi-second blocking "
    "calls, exemplifying the Memory Tax [@Abtahi2026Memanto, Sec. II.C; "
    "Table X reports approximately 2 s ingestion latency for Mem0 g].",
    title="Mem0 ingestion = LLM extraction + index update + graph sync; ~2s/write",
)

claim_zep_temporal_overhead = claim(
    "**Zep / Graphiti: temporal versioning + bi-temporal indexing at the "
    "cost of synchronous extraction latency.** Zep [@Zep] extends the "
    "graph paradigm with temporal versioning and bi-temporal indexing for "
    "enterprise auditing and compliance. The reliance on synchronous "
    "extraction pipelines introduces ingestion latency, delaying the "
    "availability of newly stored information for retrieval (Table X "
    "reports approximately 3 s for Zep) [@Abtahi2026Memanto, Sec. II.C].",
    title="Zep: temporal versioning + bi-temporal indexing, but ~3s ingestion latency",
)

claim_amem_zettelkasten_cost = claim(
    "**A-MEM: Zettelkasten-style associative memory; full inference per "
    "insertion.** A-MEM [@AMEM] adopts a Zettelkasten-inspired design in "
    "which memories are represented as interconnected notes enriched with "
    "contextual metadata. While this enables associative retrieval, it "
    "requires a full LLM inference step for *each* memory insertion, "
    "increasing both latency and cost [@Abtahi2026Memanto, Sec. II.C].",
    title="A-MEM: Zettelkasten linking requires LLM inference per memory insertion",
)

claim_hindsight_complexity = claim(
    "**Hindsight: high accuracy via multi-query parallel retrieval + "
    "reflection passes (max complexity).** Hindsight [@Hindsight] and "
    "subsequent reflective frameworks [@Reflective2025] achieve high "
    "benchmark accuracy through multi-stage retrieval and reflection "
    "mechanisms. They issue parallel queries and execute iterative "
    "reasoning passes, scoring 4/4 on the paper's architectural "
    "complexity index (graph DB / LLM at ingestion / multi-query / "
    "recursive querying) [@Abtahi2026Memanto, Sec. II.C; Sec. IV.D; "
    "Fig. 8].",
    title="Hindsight: multi-query + reflection -> highest accuracy at maximum complexity (4/4)",
)

claim_merrill_simple_can_match = claim(
    "**Emerging evidence: simpler retrieval can match elaborate "
    "hierarchies.** Merrill et al. [@Merrill2026] demonstrate that "
    "comparatively simple retrieval-based systems can outperform more "
    "elaborate memory hierarchies on existing benchmarks, suggesting that "
    "current evaluation protocols may not fully capture the benefits of "
    "structured memory organisation [@Abtahi2026Memanto, Sec. II.C].",
    title="Merrill et al.: simple retrieval can outperform elaborate hierarchies on current benchmarks",
)

# ---------------------------------------------------------------------------
# II.D Indexing and ingestion bottleneck
# ---------------------------------------------------------------------------

claim_rag_canonical = claim(
    "**RAG is the canonical paradigm for augmenting LLMs with external "
    "memory.** Retrieval-Augmented Generation [@RAG] established the "
    "canonical paradigm for combining a parametric LLM with an external "
    "non-parametric memory accessed via dense vector similarity. "
    "Subsequent systems extend RAG with hierarchical memory abstractions "
    "and hybrid storage mechanisms [@Abtahi2026Memanto, Sec. II.D].",
    title="RAG is the canonical LLM + external memory paradigm",
)

claim_hnsw_ingest_delay = claim(
    "**HNSW-based vector databases introduce non-negligible ingest-to-"
    "query delay.** Traditional vector databases rely on approximate "
    "nearest neighbour (ANN) indexing structures such as Hierarchical "
    "Navigable Small World graphs [@HNSW]. These indices must be updated "
    "after each insertion before the new entry becomes queryable, "
    "introducing non-negligible delays between data ingestion and query "
    "availability. For agentic systems operating in interactive or "
    "iterative settings, an agent may need to store information and "
    "immediately retrieve it within the same reasoning trajectory; any "
    "indexing latency directly impairs this capability "
    "[@Abtahi2026Memanto, Sec. II.D].",
    title="HNSW-based vector DBs require index updates that delay ingest-to-query availability",
)

claim_longmemeval_decomposition = claim(
    "**LongMemEval decomposes memory performance into indexing, "
    "retrieval, and reading stages.** LongMemEval [@LongMemEval] provides "
    "a structured analysis of memory system design, decomposing "
    "performance into three stages and identifying key factors: "
    "granularity of stored information, key construction, query "
    "formulation, and reading strategies. Empirical results in the "
    "LongMemEval paper show that fine-grained session decomposition, "
    "enriched key representations, temporally aware query expansion, and "
    "structured reading techniques substantially improve accuracy "
    "[@Abtahi2026Memanto, Sec. II.D].",
    title="LongMemEval framework: indexing + retrieval + reading; each stage has its own design factors",
)

claim_lost_in_middle = claim(
    "**Lost-in-the-middle: LLMs degrade on information located in the "
    "middle of extended contexts.** Liu et al. [@LostMiddle] identify a "
    "degradation effect in which LLMs exhibit reduced accuracy for "
    "information located in the middle portions of extended contexts. "
    "This finding reinforces the importance of *targeted retrieval* "
    "mechanisms that prioritise relevance over raw context length "
    "[@Abtahi2026Memanto, Sec. II.D; revisited in Sec. V.B].",
    title="Lost-in-the-middle [Liu et al. 2024]: LLM accuracy degrades for mid-context info",
)

claim_alt_architectures_complexity = claim(
    "**Alternative architectures (HippoRAG, RAPTOR, REPLUG) trade off "
    "long-range capability against system complexity.** HippoRAG "
    "[@HippoRAG] and RAPTOR [@RAPTOR] address long-range dependencies via "
    "hierarchical or graph-based representations but introduce additional "
    "system complexity. REPLUG [@REPLUG] demonstrates that high-recall "
    "retrieval combined with post-retrieval verification improves "
    "robustness, aligning with the principle of prioritising recall in "
    "memory systems [@Abtahi2026Memanto, Sec. II.D].",
    title="HippoRAG / RAPTOR / REPLUG: address long-range capability at the cost of complexity",
)

# ---------------------------------------------------------------------------
# II.E Evaluation benchmarks
# ---------------------------------------------------------------------------

setup_longmemeval_benchmark = setting(
    "**LongMemEval benchmark.** LongMemEval [@LongMemEval] is a "
    "large-scale benchmark comprising 500 manually curated questions "
    "across six categories: user-specific information, assistant "
    "responses, preferences, knowledge updates, temporal reasoning, and "
    "multi-session interactions. Questions are embedded within extended "
    "dialogues that can scale to over one million tokens across hundreds "
    "of sessions. The standard $S$ setting uses approximately 115K tokens "
    "across approximately 50 sessions [@Abtahi2026Memanto, Sec. II.E; "
    "Sec. IV.A].",
    title="Setup: LongMemEval = 500 questions, 6 categories, ~115K tokens (S setting)",
)

setup_locomo_benchmark = setting(
    "**LoCoMo benchmark.** LoCoMo [@LoCoMo] is a multi-modal dialogue "
    "benchmark spanning four reasoning categories (single-hop, multi-hop, "
    "open-domain, temporal). Individual dialogues extend to 35 sessions, "
    "300 turns, and approximately 9K tokens on average [@Abtahi2026Memanto, "
    "Sec. II.E; Sec. IV.A].",
    title="Setup: LoCoMo = multi-session dialogues, 4 reasoning categories, up to 35 sessions / 300 turns",
)

claim_other_benchmarks = claim(
    "**Other memory benchmarks.** Additional benchmarks include "
    "MemoryBank [@MemoryBank], PerLTQA [@PerLTQA], DialSim [@DialSim], "
    "MemoryAgentBench [@MemoryAgentBench], and long-context evaluation "
    "frameworks [@Terranova2025]. Recent analyses suggest that as model "
    "context windows grow, benchmark performance increasingly reflects "
    "underlying LLM reasoning capability rather than memory architecture "
    "quality, motivating the development of more targeted evaluation "
    "protocols [@Abtahi2026Memanto, Sec. II.E].",
    title="Other benchmarks (MemoryBank, PerLTQA, DialSim, MemoryAgentBench, Terranova) round out the eval landscape",
)

claim_memoryagentbench_conflict_failures = claim(
    "**MemoryAgentBench: all evaluated systems fail on multi-hop "
    "conflict scenarios.** MemoryAgentBench [@MemoryAgentBench] confirms "
    "that conflict resolution remains one of the most significant "
    "unsolved challenges in current memory systems, with all evaluated "
    "methods failing on multi-hop conflict scenarios. This empirical "
    "finding motivates Memanto's built-in conflict-resolution mechanism "
    "(D5) [@Abtahi2026Memanto, Sec. III.A; Sec. V.C].",
    title="MemoryAgentBench: all evaluated systems fail on multi-hop conflict scenarios",
)

__all__ = [
    "setup_tulving_taxonomy",
    "setup_baddeley_correspondence",
    "claim_episodic_matters_for_long_horizon",
    "claim_survey_landscape",
    "claim_memgpt_letta_overhead",
    "claim_mem0_marginal_graph_gain",
    "claim_mem0_pipeline_cost",
    "claim_zep_temporal_overhead",
    "claim_amem_zettelkasten_cost",
    "claim_hindsight_complexity",
    "claim_merrill_simple_can_match",
    "claim_rag_canonical",
    "claim_hnsw_ingest_delay",
    "claim_longmemeval_decomposition",
    "claim_lost_in_middle",
    "claim_alt_architectures_complexity",
    "setup_longmemeval_benchmark",
    "setup_locomo_benchmark",
    "claim_other_benchmarks",
    "claim_memoryagentbench_conflict_failures",
]
