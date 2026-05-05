"""Section IV.C-IV.E: Per-category results, system comparison, and Memory Tax.

Section IV.C-E of [@Abtahi2026Memanto] reports the final Stage-5 per-
category breakdowns (Tables VII-VIII), the comparison against all
publicly reported competing systems (Table IX, Fig. 7-8), and the
quantitative Memory-Tax overhead analysis (Table X).

Each per-category and per-system measurement is extracted as a separate
atomic claim (in line with the Pass 1 atomicity principle: per-benchmark
accuracy claims separated from operational-cost claims).
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# IV.C Per-category final results
# ---------------------------------------------------------------------------

claim_lme_per_category = claim(
    "**LongMemEval per-category accuracy (Stage 5, Gemini 3 inference, "
    "Table VII).**\n\n"
    "| Category | Accuracy |\n"
    "|----------|---------:|\n"
    "| Single-session User | 95.7% |\n"
    "| Single-session Assistant | 100.0% |\n"
    "| Single-session Preference | 93.3% |\n"
    "| Knowledge Update | 93.6% |\n"
    "| Temporal Reasoning | 88.0% |\n"
    "| Multi-session | 81.2% |\n"
    "| **Overall** | **89.8%** |\n\n"
    "The lowest accuracy is on Multi-session (81.2%), reflecting the "
    "inherent difficulty of synthesising information distributed across "
    "extended interaction histories [@Abtahi2026Memanto, Table VII].",
    title="LongMemEval per-category (Stage 5): 89.8% overall, 100% Single-session Assistant, 81.2% Multi-session",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table VII",
        "caption": "LongMemEval final results by category (Stage 5, Gemini 3).",
    },
)

claim_locomo_per_category = claim(
    "**LoCoMo per-category accuracy (Stage 5, Gemini 3 inference, "
    "Table VIII).**\n\n"
    "| Category | Accuracy |\n"
    "|----------|---------:|\n"
    "| Single-Hop | 78.7% |\n"
    "| Multi-Hop | 70.8% |\n"
    "| Open Domain | 92.4% |\n"
    "| Temporal | 85.4% |\n"
    "| **Overall** | **87.1%** |\n\n"
    "[@Abtahi2026Memanto, Table VIII].",
    title="LoCoMo per-category (Stage 5): 87.1% overall, 92.4% Open Domain, 70.8% Multi-Hop (lowest)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table VIII",
        "caption": "LoCoMo final results by category (Stage 5, Gemini 3).",
    },
)

# ---------------------------------------------------------------------------
# IV.D System comparison (Table IX, Figs. 7-8)
# ---------------------------------------------------------------------------

claim_system_comparison_table = claim(
    "**System comparison on LoCoMo and LongMemEval (Table IX).** All "
    "competing-system figures are drawn from their respective published "
    "papers / official benchmark reports.\n\n"
    "| System | LoCoMo | LMEval | Architecture | Retrieval Strategy |\n"
    "|--------|-------:|-------:|--------------|--------------------|\n"
    "| **Memanto (ours)** | **87.1%** | **89.8%** | Vector-only RAG | Single Query |\n"
    "| Hindsight [@Hindsight] | 89.6% | 91.4% | Hybrid (Reflection + Vector) | Parallel Multi-Query |\n"
    "| EmergenceMem | -- | 86.0% | Hybrid (Graph + Vector) | Parallel Multi-Query |\n"
    "| Supermemory | -- | 85.2% | Hybrid (Graph + Vector) | Parallel Multi-Query |\n"
    "| Memobase | 75.8% | -- | Hybrid (Graph + Vector) | Parallel Single Query |\n"
    "| Zep [@Zep] | 75.1% | 71.2% | Hybrid (Graph + Vector) | Parallel Single Query |\n"
    "| Letta [@MemGPT] | 74.0% | -- | Local Filesystem RAG | Recursive |\n"
    "| Full Context | 72.9% | 60.2% | Full Context | N/A |\n"
    "| Mem0g [@Mem0] | 68.4% | -- | Hybrid (Graph + Vector) | Parallel Single Query |\n"
    "| Mem0 [@Mem0] | 66.9% | -- | Vector-only | Parallel Single Query |\n"
    "| LangMem | 58.1% | -- | Vector-only | RAG Single Query |\n\n"
    "Memanto achieves the highest accuracy among all *vector-only* "
    "systems on both benchmarks, surpassing Mem0 by 22.9 pp on "
    "LongMemEval and 20.2 pp on LoCoMo [@Abtahi2026Memanto, Table IX; "
    "Fig. 7].",
    title="Table IX: Memanto leads vector-only systems; +22.9 pp / +20.2 pp over Mem0",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table IX and Fig. 7",
        "caption": "System comparison on LongMemEval and LoCoMo.",
    },
)

claim_hindsight_higher_at_max_complexity = claim(
    "**Hindsight attains higher accuracy than Memanto, but at maximum "
    "complexity (4/4).** Hindsight scores 91.4% LongMemEval / 89.6% "
    "LoCoMo, exceeding Memanto by 1.6 / 2.5 pp respectively. However, "
    "Hindsight's architectural complexity score is 4 / 4 (graph DB + "
    "LLM at ingestion + multi-query retrieval + recursive querying), "
    "requiring dynamic multi-query retrieval and structured reflection "
    "passes [@Abtahi2026Memanto, Sec. IV.D; Fig. 8]. Memanto's "
    "complexity score is 0 / 4.",
    title="Hindsight: +1.6 / +2.5 pp over Memanto, but at complexity 4/4 vs Memanto's 0/4",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 8",
        "caption": "Architectural complexity (0-4) vs best benchmark accuracy.",
    },
)

claim_complexity_score_definition = claim(
    "**Architectural complexity score = sum of four binary indicators "
    "(0-4 scale).** The score is computed as the sum of four binary "
    "indicators: (1) requires a graph database, (2) invokes an LLM at "
    "ingestion time, (3) employs multi-query retrieval, (4) uses "
    "recursive or reflective querying. Each indicator contributes one "
    "point, yielding a 0 (minimal overhead) to 4 (maximum complexity) "
    "scale. Memanto scores 0; Hindsight scores 4 "
    "[@Abtahi2026Memanto, Sec. IV.D; Fig. 8].",
    title="Complexity score (0-4) = graph DB + LLM-at-ingestion + multi-query + recursive",
)

claim_memanto_in_ideal_quadrant = claim(
    "**Memanto occupies the ideal upper-left quadrant of complexity-"
    "vs-accuracy space (Fig. 8).** The figure plots accuracy against "
    "the 0-4 complexity score across all evaluated systems. Memanto "
    "sits at low complexity + high accuracy (the *ideal zone*), while "
    "Hindsight achieves higher accuracy only at maximum complexity. "
    "All other hybrid systems (Mem0g, Zep, EmergenceMem, Supermemory) "
    "occupy the mid-complexity region with mid-range accuracies "
    "[@Abtahi2026Memanto, Fig. 8].",
    title="Fig. 8: Memanto in ideal zone (low complexity, high accuracy)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 8",
        "caption": "Architectural complexity vs accuracy across all evaluated systems.",
    },
)

# ---------------------------------------------------------------------------
# IV.E The Memory Tax (Table X)
# ---------------------------------------------------------------------------

claim_memory_tax_table = claim(
    "**Memory Tax: operational overhead comparison (Table X).** The "
    "Memory Tax is characterised along four dimensions:\n\n"
    "| System | LLM/Write | LLM/Retrieval | Infrastructure | Ingest Latency | Idle Cost |\n"
    "|--------|----------:|--------------:|----------------|----------------|-----------|\n"
    "| **Memanto** | **0** | **1** | Moorcheh Vector DB + API key | **<10 ms** | **Zero** |\n"
    "| Mem0 | 1 | 1 | Vector DB | ~500 ms | Fixed |\n"
    "| Mem0g | >=2 | >=2 | Vector + Neo4j | ~2 s | Fixed |\n"
    "| Zep | >=2 | >=2 | Vector + Graph | ~3 s | Fixed |\n\n"
    "Memanto's zero LLM invocations at write time + sub-10 ms ingestion "
    "+ zero idle cost (serverless) are the key cost-structure "
    "differentiators [@Abtahi2026Memanto, Table X].",
    title="Table X: Memanto = 0 LLM/write, <10ms ingest, zero idle cost",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table X",
        "caption": "Memory Tax: operational overhead comparison.",
    },
)

claim_ingest_overhead = claim(
    "**Ingestion overhead: 0 LLM/write (Memanto) vs >=2 LLM/write "
    "(Mem0g, Zep, A-MEM).** Systems requiring LLM-mediated entity "
    "extraction (Mem0g, Zep, A-MEM) consume tokens and incur non-trivial "
    "latency at *every* write operation. Mem0g and Zep invoke >=2 LLM "
    "calls per write, resulting in approximately 2 s and 3 s ingestion "
    "latencies respectively. For a customer-support agent processing "
    "1,000 messages per day, this overhead accumulates substantially. "
    "Memanto ingests raw conversational content with zero LLM "
    "invocations at write time, eliminating this cost category entirely "
    "[@Abtahi2026Memanto, Sec. IV.E].",
    title="Memanto ingest overhead: 0 LLM/write vs >=2 for Mem0g/Zep/A-MEM",
)

claim_retrieval_overhead = claim(
    "**Retrieval overhead: single-query Memanto < 90 ms vs multi-second "
    "round-trips for graph-traversal systems.** Multi-query and "
    "recursive retrieval strategies multiply inference calls per user "
    "interaction, compounding end-to-end latency. Memanto achieves "
    "sub-10 ms ingestion and sub-90 ms retrieval using a single query, "
    "compared to the multi-second round-trip characteristic of graph-"
    "traversal systems [@Abtahi2026Memanto, Table X; Sec. IV.E].",
    title="Memanto retrieval: <90 ms single-query vs multi-second graph traversal",
)

claim_infra_complexity = claim(
    "**Infrastructure complexity: Memanto = 1 component (Moorcheh + API "
    "key); hybrid systems require independent vector + graph stacks.** "
    "Hybrid systems require independent provisioning, scaling, "
    "monitoring, and maintenance of separate vector and graph database "
    "instances. Memanto requires only the Moorcheh Vector DB and API "
    "key, with no additional infrastructure to configure or operate "
    "[@Abtahi2026Memanto, Sec. IV.E].",
    title="Memanto infra: 1 component vs 2+ components (separate vector + graph) for hybrids",
)

claim_idle_cost_serverless = claim(
    "**Idle cost: Memanto scales to zero during idle periods; all "
    "competitors incur fixed idle costs.** Traditional vector databases "
    "mandate continuously provisioned compute regardless of query "
    "volume. Moorcheh's serverless architecture scales to zero during "
    "idle periods, eliminating fixed infrastructure costs for "
    "intermittent agent workloads [@Abtahi2026Memanto, Sec. IV.E; "
    "Table X].",
    title="Memanto idle cost: zero (serverless); all competitors incur fixed idle cost",
)

claim_daily_cost_estimate = claim(
    "**Estimated daily cost (10K daily memory operations): Memanto $0.50 "
    "vs Mem0-Graph $2.32 vs Zep $1.70.** For an agent executing 10,000 "
    "daily memory operations, estimated daily costs are $0.50 (Memanto), "
    "$2.32 (Mem0-Graph), $1.70 (Zep). This yields annual savings of "
    "approximately $662 per agent relative to Mem0-Graph -- a difference "
    "that compounds substantially across enterprise deployments with "
    "large agent fleets [@Abtahi2026Memanto, Sec. IV.E].",
    title="Daily cost (10K ops/day): $0.50 (Memanto) vs $2.32 (Mem0g) vs $1.70 (Zep)",
)

# ---------------------------------------------------------------------------
# Synthesis: SOTA among vector-only with lowest Memory Tax
# ---------------------------------------------------------------------------

claim_sota_vector_only = claim(
    "**Memanto achieves SOTA among vector-only systems on *both* "
    "LongMemEval (89.8%) and LoCoMo (87.1%).** This dual benchmark lead "
    "is the empirical anchor for the architectural thesis that typed "
    "schema + IT-search can match or exceed KG hybrids without graph "
    "infrastructure. The +22.9 pp / +20.2 pp margins over Mem0 are not "
    "marginal -- they are decisive [@Abtahi2026Memanto, Tables VII-IX].",
    title="Synthesis: SOTA among vector-only on both LongMemEval and LoCoMo",
)

claim_memanto_beats_kg_hybrids = claim(
    "**Memanto surpasses *all* evaluated hybrid graph + vector systems "
    "on both benchmarks (excluding Hindsight, which is reflection-"
    "based).** EmergenceMem (86.0% LME), Supermemory (85.2% LME), Zep "
    "(75.1% / 71.2%), Memobase (75.8% LoCoMo), Mem0g (68.4% LoCoMo), "
    "and Mem0 (66.9% LoCoMo) all fall below Memanto's 89.8 / 87.1 "
    "scores. Hindsight is the only competitor that exceeds Memanto, "
    "and does so at architectural complexity 4/4 vs Memanto's 0/4 "
    "[@Abtahi2026Memanto, Table IX; Fig. 7].",
    title="Memanto beats all hybrid KG+vector systems on both benchmarks (Hindsight excepted, at complexity 4/4)",
)

__all__ = [
    "claim_lme_per_category",
    "claim_locomo_per_category",
    "claim_system_comparison_table",
    "claim_hindsight_higher_at_max_complexity",
    "claim_complexity_score_definition",
    "claim_memanto_in_ideal_quadrant",
    "claim_memory_tax_table",
    "claim_ingest_overhead",
    "claim_retrieval_overhead",
    "claim_infra_complexity",
    "claim_idle_cost_serverless",
    "claim_daily_cost_estimate",
    "claim_sota_vector_only",
    "claim_memanto_beats_kg_hybrids",
]
