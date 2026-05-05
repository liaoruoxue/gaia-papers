"""Section V: Discussion.

Section V of [@Abtahi2026Memanto] gives the paper's interpretive synthesis:

* V.A explains *why* optimised retrieval outperforms graph complexity
  via three mechanism factors.
* V.B states the recall-over-precision principle.
* V.C frames conflict resolution as a production necessity.
* V.D argues for determinism as essential for agentic stability.

The Discussion is where the paper most directly challenges the prevailing
view (that KG complexity is necessary for high-fidelity memory). These
claims become hypothesis nodes for the central abduction in
`s11_wiring.py`.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# V.A Three factors explaining Memanto's strong performance
# ---------------------------------------------------------------------------

claim_factor1_decomposition = claim(
    "**Factor 1: retrieval-reasoning decomposition.** Modern LLMs are "
    "exceptionally capable in-context reasoners when provided with "
    "relevant raw context [@CoT]. Graph-based systems attempt to *pre-"
    "compute* reasoning pathways through entity-relationship structures, "
    "but this pre-computation is inherently lossy: it must commit to a "
    "schema at index time and is therefore *schema-dependent*. By "
    "contrast, providing the LLM a broader set of semantically relevant "
    "raw chunks and relying on its in-context reasoning produces more "
    "flexible and accurate answers. Mem0's own ablation showing "
    "approximately 2% graph gain over base vector configuration [@Mem0] "
    "directly supports this interpretation [@Abtahi2026Memanto, Sec. V.A].",
    title="Factor 1: LLM in-context reasoning > pre-computed graph pathways (which are schema-dependent and lossy)",
)

claim_factor2_semantic_quality = claim(
    "**Factor 2: semantic-matching quality matters more than structure.** "
    "Moorcheh's ITS engine provides deterministic, exact-match semantic "
    "search [@MoorchehITS] rather than the approximate, jitter-prone "
    "results of HNSW-based systems [@HNSW]. When the underlying search "
    "is precise and relevance scoring is information-theoretically "
    "grounded in *uncertainty reduction* rather than geometric proximity, "
    "the structural overhead of a knowledge graph provides only "
    "diminishing marginal returns. This is consistent with ENGRAM's "
    "finding [@ENGRAM] that simple dense retrieval can match complex "
    "architectures [@Abtahi2026Memanto, Sec. V.A].",
    title="Factor 2: when semantic matching is precise + IT-grounded, KG overhead returns diminish",
)

claim_factor3_ingest_simplicity = claim(
    "**Factor 3: ingestion simplicity enables faster iteration.** "
    "Eliminating the LLM-extraction step at ingestion enables sub-second "
    "write-to-retrieval feedback loops, accelerating development and "
    "debugging of agentic workflows. The synchronous extraction "
    "pipelines in Zep and Mem0g convert memory writes into multi-second "
    "blocking calls, a latency profile incompatible with tight reasoning "
    "chains [@Abtahi2026Memanto, Sec. V.A].",
    title="Factor 3: zero-LLM ingestion enables sub-second write-to-retrieval iteration",
)

# ---------------------------------------------------------------------------
# V.A synthesis: typed schema + IT-search beats KG hybrids
# ---------------------------------------------------------------------------

claim_va_synthesis = claim(
    "**Section V.A synthesis: the typed-schema + IT-search combination "
    "explains Memanto's win over KG hybrids.** The three factors -- "
    "(1) LLM in-context reasoning over raw chunks beats pre-computed "
    "schema-dependent graph pathways, (2) IT-grounded exact-match "
    "semantic search makes graph overhead returns diminish, (3) "
    "zero-LLM ingestion enables iterative agentic workflows -- jointly "
    "support the architectural thesis that the typed-schema + IT-search "
    "*combination* is what produces Memanto's empirical advantage over "
    "KG hybrids. This is the central causal claim of the paper: it is "
    "*not* that Memanto uses a bigger LLM, more training data, or "
    "better embeddings; it is the architectural choice "
    "[@Abtahi2026Memanto, Sec. V.A].",
    title="Synthesis: the typed-schema + IT-search combination explains Memanto's win (not LM / data / embeddings)",
)

# ---------------------------------------------------------------------------
# V.B Recall-over-precision principle
# ---------------------------------------------------------------------------

claim_recall_principle = claim(
    "**Recall-over-precision principle.** In agentic memory, recall "
    "systematically outperforms precision as a retrieval objective. "
    "Expanding $k$ from 10 to 100 produces a cumulative +28.4 pp "
    "improvement on LongMemEval (combining S2 +20.4 pp and S4 +5.8 pp "
    "+ small contributions), while prompt optimisation contributes only "
    "+2.2 pp. Systems that invest engineering effort in *precise* "
    "structured retrieval (graph traversal, multi-hop entity "
    "resolution, recursive query decomposition) may be *solving the "
    "wrong problem*. The LLM is a more capable filter than any pre-"
    "computed retrieval structure, at the cost of a few extra tokens of "
    "input context [@Abtahi2026Memanto, Sec. V.B; Fig. 6].",
    title="Recall-over-precision: +28.4 pp from k expansion vs +2.2 pp from prompt optimisation",
)

claim_recall_consistent_with_lme = claim(
    "**Recall principle is consistent with LongMemEval's finding that "
    "performance improves beyond 20K retrieved tokens.** The recall-"
    "over-precision finding is consistent with LongMemEval's [@LongMemEval] "
    "observation that performance continues improving beyond 20K "
    "retrieved tokens with GPT-4o, and with Liu et al.'s [@LostMiddle] "
    "finding that the lost-in-the-middle effect is a function of *where* "
    "information appears rather than *how much* is retrieved "
    "[@Abtahi2026Memanto, Sec. V.B].",
    title="Recall principle aligns with LongMemEval's >20K-token finding and Liu et al.'s lost-in-middle analysis",
)

# ---------------------------------------------------------------------------
# V.C Conflict resolution as production necessity
# ---------------------------------------------------------------------------

claim_conflict_not_in_benchmarks = claim(
    "**Conflict-resolution is critical for production but not "
    "systematically tested in current benchmarks.** Neither LongMemEval "
    "nor LoCoMo systematically tests contradictory memories. In long-"
    "running production deployments, however, contradictions accumulate "
    "via user corrections, updated preferences, and evolving project "
    "contexts. Without explicit conflict detection these produce "
    "*memory poisoning*, leading to increasingly incoherent agent "
    "behaviour over time. Memanto's proactive conflict detection "
    "provides a guardrail that no evaluated competing system offers; "
    "MemoryAgentBench [@MemoryAgentBench] confirms that all current "
    "systems fail on multi-hop conflict scenarios "
    "[@Abtahi2026Memanto, Sec. V.C].",
    title="V.C: conflict resolution is a production necessity not captured by benchmark accuracy",
)

# ---------------------------------------------------------------------------
# V.D Determinism for agentic stability
# ---------------------------------------------------------------------------

claim_determinism_matters = claim(
    "**Determinism in retrieval matters for agentic stability.** LLMs "
    "and autonomous agents exhibit high sensitivity to retrieval "
    "variability: even minor changes in retrieved context can trigger "
    "divergent reasoning paths. ANN-based systems (such as HNSW [@HNSW]) "
    "introduce non-determinism via probabilistic graph traversal -- "
    "identical queries may return different results depending on index "
    "state. This volatility compounds across multi-turn agent "
    "interactions, propagating inconsistencies through conversation "
    "history. Memanto's exhaustive ITS-search architecture provides "
    "deterministic retrieval, eliminating this source of instability. "
    "Furthermore, new documents become immediately queryable without "
    "degrading search quality or requiring batch reprocessing "
    "[@Abtahi2026Memanto, Sec. V.D].",
    title="V.D: ANN non-determinism propagates through agent multi-turn conversations; ITS exhaustive search eliminates it",
)

# ---------------------------------------------------------------------------
# Foil: the prevailing-KG-assumption view (target of the contradiction operator)
# ---------------------------------------------------------------------------

claim_kg_view_complexity_necessary = claim(
    "**Foil: the prevailing industry view that knowledge-graph "
    "complexity is *necessary* for high-fidelity agent memory.** This "
    "is the implicit position embedded in the dominant 2024-2026 "
    "frameworks [@Mem0; @Zep; @MemGPT; @AMEM]: the field's response to "
    "long-horizon agent-memory challenges has been to add explicit "
    "graph structure on top of vector retrieval, accept the resulting "
    "ingestion / retrieval / infrastructure overhead, and treat the "
    "Memory Tax as the unavoidable price of high-fidelity memory. "
    "Memanto's empirical demonstration -- SOTA accuracy among vector-"
    "only systems on both LongMemEval and LoCoMo, surpassing all "
    "evaluated KG hybrids -- contradicts this view: the typed-schema + "
    "IT-search combination achieves what the KG view says only KGs can. "
    "The paper does not state this contradiction in so many words but "
    "Sec. I, Sec. V.A, and the conclusion all frame it as the central "
    "rhetorical move [@Abtahi2026Memanto, abstract; Sec. I; Sec. V.A; "
    "Sec. VI].",
    title="Foil: prevailing view treats KG complexity as necessary; Memanto's results contradict this",
)

__all__ = [
    "claim_factor1_decomposition",
    "claim_factor2_semantic_quality",
    "claim_factor3_ingest_simplicity",
    "claim_va_synthesis",
    "claim_recall_principle",
    "claim_recall_consistent_with_lme",
    "claim_conflict_not_in_benchmarks",
    "claim_determinism_matters",
    "claim_kg_view_complexity_necessary",
]
