"""Section 15 (Implementation Validation: Case Study) of [@Park2026Kumiho]:
LoCoMo benchmark evaluation, LoCoMo-Plus benchmark evaluation, AGM compliance
verification, token compression, retrieval observations, cross-session
provenance, belief revision in practice, Dream State validation, limitations.

Each table and headline number is transcribed atomically as its own claim so
each can be independently judged.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 15.1: Token compression (Table 11)
# ---------------------------------------------------------------------------

claim_token_compression_table = claim(
    "**Token compression ratios (Table 11 of [@Park2026Kumiho]).** Storing "
    "compact metadata summaries rather than raw transcripts yields "
    "significant token savings:\n\n"
    "| Type | Summary | Raw | Ratio |\n"
    "|------|---------|-----|-------|\n"
    "| Simple fact | ~12 | 500 | 42x |\n"
    "| Preference | ~18 | 800 | 44x |\n"
    "| Profile | ~80 | 4K | 50x |\n"
    "| Paper session | ~65 | 12K | 185x |\n"
    "| Planning | ~90 | 25K | 278x |\n\n"
    "Compression compounds at retrieval time: a typical recall returning "
    "$k=5$ results injects ~250-400 summary tokens vs. ~50,000+ tokens "
    "for raw replay. Cost scales as $O(k \\cdot \\bar{s})$ "
    "(summary mode) vs. $O(k \\cdot \\bar{c})$ (raw replay) "
    "[@Park2026Kumiho, Sec. 15.1; Table 11].",
    title="Token compression: 40x-280x summary-vs-raw ratios",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 11",
        "caption": "Token compression ratios.",
    },
)

# ---------------------------------------------------------------------------
# 15.2: LoCoMo benchmark evaluation
# ---------------------------------------------------------------------------

setup_locomo_eval_config = setting(
    "**LoCoMo evaluation configuration.** Summarized recall mode with "
    "GPT-4o as the answer model, graph-augmented retrieval with "
    "multi-query reformulation, recall limit of 3 memories per query, "
    "context top-$k=7$. Official metric: token-level F1 with Porter "
    "stemming [@LoCoMo2024]. Adversarial scoring: binary refusal "
    "detection, not continuous F1 [@Park2026Kumiho, Sec. 15.2].",
    title="Setup: LoCoMo eval (GPT-4o, graph-augmented recall, k=3 memories, top-7 context)",
)

claim_locomo_table12_cross_system = claim(
    "**LoCoMo token-level F1 cross-system comparison (Table 12 of "
    "[@Park2026Kumiho], four retrieval categories).**\n\n"
    "| System | Single | Multi | Temp. | Open | Overall | Source |\n"
    "|--------|--------|-------|-------|------|---------|--------|\n"
    "| Zep | 0.357 | 0.194 | 0.420 | 0.496 | -- | [@ZepBenchmark2025] |\n"
    "| OpenAI Memory | -- | -- | -- | -- | ~0.34 | [@ZepBenchmark2025] |\n"
    "| Mem0 | 0.387 | 0.286 | 0.489 | 0.477 | ~0.40 | [@ZepBenchmark2025] |\n"
    "| Mem0-Graph | 0.381 | 0.243 | 0.516 | 0.493 | ~0.40 | [@ZepBenchmark2025] |\n"
    "| Memobase | 0.463 | 0.229 | 0.642 | 0.516 | -- | [@Memobase2025] |\n"
    "| ENGRAM | 0.231 | 0.183 | 0.219 | 0.086 | 0.211 | [@ENGRAM2025] |\n"
    "| **Kumiho** | **0.462** | **0.355** | **0.533** | 0.290* | **0.447** | This work |\n\n"
    "*Open-domain questions require world knowledge absent from "
    "conversation history; this is the expected memory-only floor. "
    "Kumiho achieves the highest reported four-category F1 ($n=1{,}540$) "
    "[@Park2026Kumiho, Sec. 15.2; Table 12].",
    title="LoCoMo cross-system comparison (Table 12): Kumiho 0.447 four-cat F1 = highest reported",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 12",
        "caption": "LoCoMo token-level F1: cross-system comparison.",
    },
)

claim_locomo_table13_per_category = claim(
    "**LoCoMo per-category breakdown (Table 13 of [@Park2026Kumiho], "
    "$n=1{,}986$).**\n\n"
    "| Category | $n$ | F1 |\n"
    "|----------|-----|-----|\n"
    "| Single-hop | 841 | 0.462 |\n"
    "| Multi-hop | 282 | 0.355 |\n"
    "| Temporal | 321 | 0.533 |\n"
    "| Open-domain | 96 | 0.290 |\n"
    "| Retrieval average | 1,540 | 0.447 |\n"
    "| Adversarial (refusal acc.) | 446 | 0.975 |\n"
    "| Overall (incl. adversarial) | 1,986 | 0.565 |\n\n"
    "Multi-hop F1 of 0.355 exceeds Mem0 (0.286, +6.9pp) and Mem0-Graph "
    "(0.243, +11.2pp) -- precisely where graph-augmented recall with "
    "edge traversal provides structural advantage over flat vector stores "
    "[@Park2026Kumiho, Sec. 15.2; Table 13].",
    title="LoCoMo per-category (Table 13): multi-hop +11.2pp over Mem0-Graph (graph-augmented advantage)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 13",
        "caption": "LoCoMo per-category breakdown.",
    },
)

claim_adversarial_refusal_natural = claim(
    "**The 97.5% adversarial refusal accuracy is a natural consequence of "
    "belief-revision architecture.** Adversarial questions test whether "
    "the system fabricates plausible-sounding answers in the absence of "
    "supporting memories. The near-perfect refusal score follows directly "
    "from the architecture: the memory graph genuinely does not contain "
    "fabricated information -- immutable revisions preserve only what was "
    "actually discussed, and consolidation-as-denoising strips surface-"
    "level cues that adversarial questions exploit -- so there is "
    "**nothing for the model to hallucinate from** "
    "[@Park2026Kumiho, Sec. 15.2 'Adversarial refusal accuracy'].",
    title="Adversarial 97.5%: belief revision means no fabricated memories => nothing to hallucinate from",
)

# ---------------------------------------------------------------------------
# 15.3: LoCoMo-Plus benchmark
# ---------------------------------------------------------------------------

setup_locomo_plus_config = setting(
    "**LoCoMo-Plus evaluation configuration.** Same graph-native "
    "architecture as LoCoMo, summarized recall mode (title + summary "
    "metadata). Four architectural mechanisms address the cue-trigger "
    "semantic disconnect: (i) **prospective indexing** -- 3-5 hypothetical "
    "future scenarios generated by GPT-4o-mini in parallel during "
    "consolidation, indexed alongside the summary; (ii) **event "
    "extraction** -- structured events with consequences appended to "
    "summaries; (iii) **sibling relevance filtering** -- cosine threshold "
    "0.30 prevents context dilution; (iv) **client-side LLM reranking** "
    "via host agent's own LLM at zero additional cost. Pipeline uses "
    "GPT-4o-mini for bulk LLM operations, GPT-4o only for answer "
    "generation [@Park2026Kumiho, Sec. 15.3].",
    title="Setup: LoCoMo-Plus eval = prospective indexing + event extraction + sibling filter + LLM rerank",
)

claim_locomo_plus_table15_baselines = claim(
    "**LoCoMo-Plus: Kumiho vs. published baselines (Table 15 of "
    "[@Park2026Kumiho], $n=401$).**\n\n"
    "| System | Model | Acc. (%) |\n"
    "|--------|-------|----------|\n"
    "| RAG (text-ada-002) | text-ada-002 | 23.5 |\n"
    "| RAG (text-embed-small) | text-embed-small | 24.9 |\n"
    "| RAG (text-embed-large) | text-embed-large | 29.8 |\n"
    "| Mem0 | Various | 41.4 |\n"
    "| A-MEM | Various | 42.4 |\n"
    "| SeCom | Various | 42.6 |\n"
    "| GPT-4o (full context) | GPT-4o | 41.9 |\n"
    "| GPT-4.1 (full context) | GPT-4.1 | 43.6 |\n"
    "| Gemini 2.5 Flash (1M) | Gemini 2.5 Flash | 44.6 |\n"
    "| Gemini 2.5 Pro (1M) | Gemini 2.5 Pro | 45.7 |\n"
    "| **Kumiho (4o-mini answer)** | GPT-4o-mini | **~88** |\n"
    "| **Kumiho (4o answer)** | GPT-4o | **93.3** |\n\n"
    "Kumiho outperforms the best published baseline (Gemini 2.5 Pro 45.7%) "
    "by 47.6 percentage points. Gemini 2.5 Pro's 1M+ token context fits "
    "entire conversations without retrieval, yet still scores only 45.7% -- "
    "demonstrating that cognitive memory is not a context-capacity problem "
    "but an organization, enrichment, and retrieval problem "
    "[@Park2026Kumiho, Sec. 15.3; Table 15].",
    title="LoCoMo-Plus baselines (Table 15): Kumiho 93.3% vs. best baseline 45.7% (+47.6pp)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 15",
        "caption": "LoCoMo-Plus: Kumiho vs. published baselines.",
    },
)

claim_locomo_plus_table16_by_type = claim(
    "**LoCoMo-Plus accuracy by constraint type (Table 16 of "
    "[@Park2026Kumiho], $n=401$).**\n\n"
    "| Type | $n$ | Correct | 4o (%) | 4o-mini (%) |\n"
    "|------|-----|---------|--------|-------------|\n"
    "| Causal | 101 | 97 | 96.0 | 96.0 |\n"
    "| State | 100 | 96 | 96.0 | 95.0 |\n"
    "| Value | 100 | 96 | 96.0 | ~89 |\n"
    "| Goal | 100 | 85 | 85.0 | ~73 |\n"
    "| **Overall** | **401** | **374** | **93.3** | **~88** |\n\n"
    "Causal/state/value all achieve 96% with GPT-4o (near-ceiling). "
    "Goal-type questions (85%) remain hardest -- they require abstract "
    "reasoning to connect a current trigger to a stored intention. "
    "Model impact is type-dependent: switching 4o-mini -> 4o yields "
    "causal +0%, state +1%, value +7%, goal +12% -- the harder the "
    "constraint type, the more a stronger answer model helps "
    "[@Park2026Kumiho, Sec. 15.3; Table 16].",
    title="LoCoMo-Plus by constraint type (Table 16): goal hardest at 85% (4o), causal/state/value 96%",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 16",
        "caption": "LoCoMo-Plus accuracy by constraint type.",
    },
)

claim_locomo_plus_table17_time_gap = claim(
    "**LoCoMo-Plus accuracy by time gap (Table 17 of [@Park2026Kumiho], "
    "$n=401$, GPT-4o answer).**\n\n"
    "| Time Gap | $n$ | Acc. (%) | Notes |\n"
    "|----------|-----|----------|-------|\n"
    "| <=2 weeks | 35 | 88.6 | More goal-type entries |\n"
    "| 2 wk - 1 mo | 77 | 97.4 | Peak performance |\n"
    "| 1 - 3 mo | 164 | 93.9 | Largest cohort |\n"
    "| 3 - 6 mo | 93 | 93.5 | No degradation |\n"
    "| >6 mo | 32 | 84.4 | Cliff eliminated |\n\n"
    "**The most significant empirical finding**: pre-enrichment accuracy "
    "at >6 months was 37.5%; with prospective indexing and event "
    "extraction active, accuracy at >6 months rises to 84.4% -- a "
    "**47-percentage-point improvement** that validates prospective "
    "indexing as the critical mechanism for bridging long temporal gaps. "
    "As time increases, embedding similarity between cue and trigger "
    "naturally decays; prospective indexing provides alternative "
    "retrieval paths through generated implications whose vocabulary is "
    "independent of the original conversation's wording "
    "[@Park2026Kumiho, Sec. 15.3; Table 17].",
    title="LoCoMo-Plus by time gap (Table 17): >6mo cliff eliminated (37.5% -> 84.4%, +47pp)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 17",
        "caption": "LoCoMo-Plus accuracy by time gap.",
    },
)

claim_locomo_plus_recall_98_5 = claim(
    "**LoCoMo-Plus recall accuracy reaches 98.5% (395/401), with the 6.7% "
    "end-to-end gap entirely attributable to answer-model fabrication on "
    "correctly retrieved context.** Of the 27 failures: **recall miss** -- "
    "6 failures (22%) where no relevant memories were retrieved by any "
    "query variant; **answer fabrication** -- 21 failures (78%) where the "
    "correct memory appeared in the recalled context but the answer model "
    "fabricated around it (dominant pattern: 'surface-theme hijacking' -- "
    "the model follows the trigger's surface theme rather than connecting "
    "to the contradictory or abstract recalled memory). All 15 goal "
    "failures are answer fabrication. This means the memory layer has "
    "effectively solved the retrieval problem; the remaining gap is a "
    "*consumer-side* reasoning challenge, not a memory challenge "
    "[@Park2026Kumiho, Sec. 15.3 'Failure mode taxonomy'].",
    title="LoCoMo-Plus recall 98.5%: 78% of failures = answer fabrication, not retrieval",
)

claim_model_decoupled_validation = claim(
    "**Model-decoupled architecture is empirically validated by "
    "constant 98.5% recall across answer-model swaps.** Switching the "
    "answer model from GPT-4o-mini (~88%) to GPT-4o (93.3%) improves "
    "end-to-end accuracy by 5.3 points without any pipeline changes -- "
    "concentrated in the hardest constraint types (goal +12%, value +7%). "
    "The 98.5% recall accuracy is **invariant** across models -- both "
    "receive identical recalled context from the same retrieval pipeline. "
    "Only end-to-end accuracy differs. Theoretical ceiling with perfect "
    "answer generation is ~99%, limited only by 6 genuine recall misses "
    "[@Park2026Kumiho, Sec. 15.3 'Model-decoupled architecture'].",
    title="Model-decoupling validation: 98.5% recall invariant across answer models (4o vs. 4o-mini)",
)

claim_locomo_plus_cost = claim(
    "**LoCoMo-Plus cost: ~$14 for 401 entries.** Summarization (~$3), "
    "edge discovery (~$2), implication generation (~$1), event extraction "
    "(~$1), answer generation (~$3), judging (~$0.50), sibling embedding "
    "(~$0.10). Cost efficiency stems from structured summarization with "
    "enrichment (cheap, one-time per session) replacing brute-force "
    "full-context retrieval (expensive, per-query). For comparison, "
    "running Gemini 2.5 Pro with full context on 401 entries costs "
    "significantly more while achieving only 45.7% accuracy "
    "[@Park2026Kumiho, Sec. 15.3 'Cost analysis'].",
    title="LoCoMo-Plus cost: ~$14 for 401 entries (vs. expensive full-context Gemini 2.5 Pro at 45.7%)",
)

claim_independent_reproduction = claim(
    "**Independent reproduction by the LoCoMo-Plus authors yielded "
    "results in the mid-80% range.** After Park shared the evaluation "
    "harness and setup with the LoCoMo-Plus authors [@LoCoMoPlus2026], "
    "they independently reproduced the benchmark and reported results in "
    "a similar range, though somewhat lower than the original 93.3% "
    "(mid-80% accuracy). They confirmed that the system reliably "
    "surfaced memory cues that later triggered the correct response and "
    "specifically noted that prospective indexing appeared effective for "
    "the cue-trigger semantic disconnect. Even at mid-80%, this "
    "substantially outperforms all published baselines. Park reports this "
    "not as a claim of exact score replication but as independent support "
    "for the underlying retrieval mechanism "
    "[@Park2026Kumiho, Sec. 15.3 'Independent reproduction'].",
    title="Independent reproduction: mid-80% range still outperforms all published baselines",
)

claim_benchmark_construction_caveat = claim(
    "**LoCoMo-Plus benchmark-construction caveat: GPT-family alignment.** "
    "Because the cue-trigger pairs in LoCoMo-Plus were generated using "
    "LLM-assisted procedures, some latent forward-implication structure "
    "may align particularly well with the kinds of generative associations "
    "GPT-family models are good at producing and recognizing. In Park's "
    "experiments, GPT-4o-family models scored unusually strongly (e.g., "
    "GPT-4o-mini reaching ~88%), suggesting that part of the absolute "
    "score may reflect **model-family alignment** with the benchmark-"
    "construction process rather than memory architecture alone. The "
    "results should be interpreted as strong evidence that prospective "
    "indexing and structured memory retrieval are effective for this "
    "class of implicit-constraint recall, while acknowledging that future "
    "evaluation on more human-authored conversational corpora would "
    "provide a more conservative measure "
    "[@Park2026Kumiho, Sec. 15.3 'Caveats'].",
    title="LoCoMo-Plus caveat: GPT-family model-family alignment with LLM-assisted construction",
)

# ---------------------------------------------------------------------------
# 15.7: AGM compliance verification
# ---------------------------------------------------------------------------

claim_agm_compliance_table18 = claim(
    "**AGM Compliance Verification (Table 18 of [@Park2026Kumiho], 49 "
    "scenarios across 5 categories).**\n\n"
    "| Postulate | Simple | Multi | Chain | Temp. | Adv. | Pass |\n"
    "|-----------|--------|-------|-------|-------|------|------|\n"
    "| $K^\\ast 2$ | check | check | check | check | check | 100% |\n"
    "| $K^\\ast 3$ | check | check | check | check | check | 100% |\n"
    "| $K^\\ast 4$ | check | check | check | check | check | 100% |\n"
    "| $K^\\ast 5$ | check | check | check | check | check | 100% |\n"
    "| $K^\\ast 6$ | check | check | -- | check | check | 100% |\n"
    "| Relevance | check | check | check | check | check | 100% |\n"
    "| Core-Retainment | check | check | check | -- | check | 100% |\n"
    "| **Overall** | 100% | 100% | 100% | 100% | 100% | **100%** |\n\n"
    "**49 scenarios: 49 passed, 0 failed.** Adversarial category tests "
    "edge cases such as case-variant values, long string values, rapid "
    "sequential revisions (10 consecutive revisions to the same item), "
    "similar item names ('color' vs. 'colour'), idempotent revisions, "
    "deep dependency chains (A->B->C->D), and mixed edge types. All "
    "adversarial scenarios pass, confirming that graph-native operations "
    "satisfy formal postulates not only in idealized conditions but under "
    "stress. The compliance suite verifies that the *implementation* "
    "faithfully executes the operational semantics across a diverse "
    "scenario space -- particularly important because the formal "
    "analysis operates over an idealized propositional logic $L_G$, while "
    "the implementation operates over concrete Neo4j operations with real "
    "network latency, concurrent access, and string-based metadata "
    "[@Park2026Kumiho, Sec. 15.7; Table 18].",
    title="AGM Compliance (Table 18): 49/49 scenarios pass across 7 postulates and 5 categories",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 18",
        "caption": "AGM Compliance Verification (49 scenarios).",
    },
)

# ---------------------------------------------------------------------------
# 15.5-15.6: Cross-session provenance + belief revision in practice
# ---------------------------------------------------------------------------

claim_cross_session_provenance_paper = claim(
    "**Cross-session provenance was demonstrated by the iterative "
    "authorship of the paper itself.** The paper was authored across 6 "
    "revision sessions over 3 days (v1 -> v2 -> v3 -> v3-upd -> v4 -> v5 "
    "-> v6) with `derived_from` edges encoding the lineage. This enabled "
    "(i) an agent resuming work on a new session to traverse the chain "
    "and understand what changed and why; (ii) provenance summary "
    "queries on v6 to resolve the full dependency graph including "
    "planning sessions; (iii) an auditable record of the document's "
    "evolution. The agent could recall prior planning context without "
    "re-reading the full paper, using only compact summaries stored in "
    "the graph [@Park2026Kumiho, Sec. 15.5].",
    title="Cross-session provenance: paper authorship itself = 6-revision derived_from chain",
)

claim_belief_revision_in_practice = claim(
    "**Concrete belief-revision case study from deployment (favorite "
    "color).** Step 1 (Feb 5): agent stored 'user's favorite color is "
    "blue' via `memory_ingest`, creating revision $r_1$ tagged `latest`. "
    "Step 2 (Feb 7): user corrected 'favorite color is now black, not "
    "blue.' The pipeline detected the existing item via fulltext search, "
    "triggering revision: created $r_2$, re-pointed `latest -> r_2`, "
    "added Supersedes edge. $K^\\ast 2$ (Success), $K^\\ast 5$ "
    "(Consistency), $K^\\ast 3$ (Inclusion) all hold. Step 3: "
    "AnalyzeImpact on $r_2$ -- empty impact set (no dependents). Step 4: "
    "subsequent query for 'favorite color' returned both $r_1$ (blue, "
    "score 4.70) and $r_2$ (black, score 3.27) with $r_1$ ranking higher "
    "via exact keyword match -- a strength (immutable provenance "
    "preserved) and a current limitation (retrieval ranking does not yet "
    "auto-prioritize recency). The agent's skill prompt instructs it to "
    "prefer the most recent memory at the application layer "
    "[@Park2026Kumiho, Sec. 15.6].",
    title="Belief revision in practice: favorite-color case (revision works; ranking limitation acknowledged)",
)

# ---------------------------------------------------------------------------
# 15.8: Dream State validation
# ---------------------------------------------------------------------------

claim_dream_state_deployment_validation = claim(
    "**Dream State validated in deployment and during benchmark "
    "evaluation.** Early runs on a small graph produced conservative "
    "outcomes (0 deprecations, 0 tag updates), correctly reflecting that "
    "a young graph with few episodic memories has limited consolidation "
    "candidates. The circuit breaker and conservative assessment prompt "
    "avoided premature pruning -- the expected behavior. During the "
    "LoCoMo benchmark evaluation, the pipeline processed all conversation "
    "transcripts into summaries without triggering "
    "`max_deprecation_ratio` (set to 0.5), and `published`-tagged items "
    "were protected regardless of LLM recommendations. **No manual "
    "intervention was required** to prevent consolidation from corrupting "
    "evaluation data -- the architectural safety mechanisms were "
    "sufficient [@Park2026Kumiho, Sec. 15.8].",
    title="Dream State validation: 0 manual interventions during LoCoMo benchmark consolidation",
)

# ---------------------------------------------------------------------------
# 15.9: Limitations
# ---------------------------------------------------------------------------

claim_limit_scale = claim(
    "**Limitation: scale.** During the LoCoMo-Plus evaluation, the graph "
    "accumulated over 200,000 nodes across all benchmark conversations "
    "without observed degradation in retrieval quality or system "
    "throughput, providing empirical evidence that the architecture "
    "scales into the hundreds-of-thousands-of-nodes range under realistic "
    "workloads. **What remains untested**: retrieval precision under "
    "adversarial scale conditions (tens of millions of items with very "
    "low ratio of relevant to irrelevant memories), where vector "
    "similarity alone may surface many plausible but incorrect candidates "
    "[@Park2026Kumiho, Sec. 15.9 'Scale'].",
    title="Limitation: scale tested at 200K nodes; tens-of-millions adversarial regime untested",
)

claim_limit_cross_system_methodology = claim(
    "**Limitation: cross-system comparison methodology.** The LoCoMo "
    "token-level F1 results (Sec. 15.2) use the same scoring function as "
    "competing systems, enabling direct comparison. However, competitor "
    "scores are sourced from their respective publications, **not from "
    "controlled re-evaluation on identical infrastructure and LLM "
    "configurations**. Differences in underlying LLM, prompt engineering, "
    "and evaluation methodology may account for some variance; a fully "
    "controlled comparison using the same LLM, prompt template, and "
    "hardware is needed to isolate architectural contributions from "
    "confounds [@Park2026Kumiho, Sec. 15.9 'Cross-system comparison "
    "methodology'].",
    title="Limitation: cross-system numbers from publications, not controlled re-evaluation",
)

claim_limit_eval_scope_complementarity = claim(
    "**Limitation: evaluation scope complementarity.** LoCoMo evaluates "
    "end-to-end recall quality but does not directly exercise the formal "
    "belief-revision machinery -- its questions do not require detecting "
    "contradictions, superseding prior beliefs, or propagating impact "
    "through dependency chains. The AGM compliance suite (Sec. 15.7) "
    "fills this gap by testing graph-level operations in isolation but "
    "does not measure whether those operations improve downstream agent "
    "behavior. A benchmark requiring the agent to answer questions whose "
    "correctness *depends on* having performed correct belief revision "
    "(e.g., MemoryAgentBench [@MemoryAgentBench2026] conflict-resolution "
    "tasks) is the critical missing evaluation, planned future work "
    "[@Park2026Kumiho, Sec. 15.9 'Evaluation scope complementarity'].",
    title="Limitation: LoCoMo + AGM-suite are complementary; no integrated belief-revision-correctness benchmark",
)

claim_limit_self_eval_bias = claim(
    "**Limitation: self-evaluation bias.** The system is evaluated on its "
    "own deployment data during the authorship of this paper, creating an "
    "inherent circularity. Park attempts to mitigate this by reporting "
    "raw numbers without favorable interpretation and by explicitly "
    "acknowledging shortcomings (e.g., the belief-revision ranking "
    "limitation in Sec. 15.6) [@Park2026Kumiho, Sec. 15.9 'Self-evaluation "
    "bias'].",
    title="Limitation: self-evaluation bias (system evaluated during its own authorship)",
)

claim_limit_lg_expressiveness = claim(
    "**Limitation: $L_G$ expressiveness trade-off.** The formal results "
    "hold for a deliberately weak propositional logic over ground triples. "
    "$L_G$ cannot express subsumption hierarchies, role composition, "
    "disjointness axioms, or cardinality constraints -- features real "
    "knowledge graphs often need. Any strengthening of $L_G$ toward "
    "richer logics would re-encounter Flouris-type [@Flouris2005DL] "
    "impossibility results. The formal contribution is thus scoped: it "
    "demonstrates AGM belief revision is achievable for graph-native "
    "memory at the propositional level but does not extend to more "
    "expressive representations [@Park2026Kumiho, Sec. 15.9 'L_G "
    "expressiveness'].",
    title="Limitation: L_G cannot express DL-style subsumption/role-composition/cardinality",
)

claim_limit_formal_scope = claim(
    "**Limitation: formal scope ($K^\\ast 7$/$K^\\ast 8$ open).** The "
    "primary formal claim covers $K^\\ast 2$-$K^\\ast 6$ plus Relevance "
    "and Core-Retainment. The supplementary postulates ($K^\\ast 7$, "
    "$K^\\ast 8$) remain open -- establishing them requires constructing "
    "an entrenchment ordering or proving the system's operations encode "
    "a transitively relational contraction [@Grove1988]. The postulates "
    "are proved for $\\mathcal{B}(\\tau)$, not for the specific subset "
    "surfaced by the hybrid retrieval pipeline (which introduces score-"
    "based non-determinism) [@Park2026Kumiho, Sec. 15.9 'Formal scope'].",
    title="Limitation: K*7/K*8 not formally established (entrenchment ordering future work)",
)

claim_limit_dream_state_llm_dependency = claim(
    "**Limitation: Dream State LLM dependency.** The consolidation "
    "pipeline's quality depends entirely on the LLM's assessment "
    "accuracy. Incorrect deprecation recommendations, despite safety "
    "guards, could degrade the memory graph over time. The circuit "
    "breaker mitigates catastrophic failures but cannot prevent gradual "
    "quality erosion from consistently biased assessments "
    "[@Park2026Kumiho, Sec. 15.9 'Dream State LLM dependency'].",
    title="Limitation: Dream State LLM dependency (gradual quality erosion possible despite guards)",
)

claim_limit_system_performance = claim(
    "**Limitation: system performance reporting incomplete.** Park does "
    "not report latency distributions, throughput measurements, or "
    "memory overhead per belief beyond the headline 15ms working / "
    "80-120ms long-term query numbers. Basic system metrics are needed "
    "to substantiate the architectural claims "
    "[@Park2026Kumiho, Sec. 15.9 'System performance'].",
    title="Limitation: latency distributions, throughput, per-belief overhead not reported",
)

__all__ = [
    "setup_locomo_eval_config",
    "setup_locomo_plus_config",
    "claim_token_compression_table",
    "claim_locomo_table12_cross_system",
    "claim_locomo_table13_per_category",
    "claim_adversarial_refusal_natural",
    "claim_locomo_plus_table15_baselines",
    "claim_locomo_plus_table16_by_type",
    "claim_locomo_plus_table17_time_gap",
    "claim_locomo_plus_recall_98_5",
    "claim_model_decoupled_validation",
    "claim_locomo_plus_cost",
    "claim_independent_reproduction",
    "claim_benchmark_construction_caveat",
    "claim_agm_compliance_table18",
    "claim_cross_session_provenance_paper",
    "claim_belief_revision_in_practice",
    "claim_dream_state_deployment_validation",
    "claim_limit_scale",
    "claim_limit_cross_system_methodology",
    "claim_limit_eval_scope_complementarity",
    "claim_limit_self_eval_bias",
    "claim_limit_lg_expressiveness",
    "claim_limit_formal_scope",
    "claim_limit_dream_state_llm_dependency",
    "claim_limit_system_performance",
]
