"""Priors for independent (leaf) claims in the 2604.22085 (Memanto) formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables (III-X) and figures
  (5-8)** -- 0.92-0.95. Each is a directly measured benchmark / overhead
  value with explicit table or figure citation; the modest discount
  reflects evaluation-protocol noise (LLM-judge variance, prompt
  adaptation differences) and the ~5-7% labelling-noise ceiling
  acknowledged in V.E.
* **Architectural facts about Moorcheh's engine** (no-indexing, sub-90 ms
  retrieval, 32x MIB compression, deterministic ITS) -- 0.92-0.95.
  These are technical claims about the system the authors ship; they
  could in principle be falsified by independent measurement but are
  internally consistent and corroborated by the MAIR study.
* **Independently validated MAIR throughput (NDCG@10 / 2000+ QPS / 6.6x
  speedup)** -- 0.93. Anchored by [@MoorchehITS] which is a published
  arXiv preprint with explicit numbers.
* **Architectural assertions Memanto makes about its own design**
  (typing dual purpose, conflict mechanism, daily intelligence,
  namespace, manual type assignment) -- 0.93-0.96. Definitional /
  observable facts about the deployed system.
* **Six abstract desiderata D1-D6** -- 0.93-0.96. These are normative
  architectural assertions; modest because the framing is interpretive.
* **Related-work characterisations of competing systems** (Mem0 graph
  yields ~2pp, Mem0/Zep/AMEM cost structures, HNSW delay, Hindsight
  complexity, Merrill simple-can-match) -- 0.85-0.92. Authors
  characterise other systems' designs; small caveat for
  characterisation accuracy.
* **Cognitive-science / cross-paper findings** (Tulving, Baddeley
  correspondence, lost-in-middle, episodic matters) -- 0.9-0.94.
* **Stage-by-stage measurement claims** (Tables III-VI numbers) --
  0.92-0.94.
* **System comparison table (Table IX)** -- 0.92. Drawn from competing
  systems' own published numbers, so subject to those systems'
  measurement protocols.
* **Hypothesis / alternative in the central abduction**:
  - `claim_va_synthesis` (architectural-choice hypothesis) is *derived*
    via the V.A three-factor argument, so no prior here.
  - `alt_lm_data_embeddings` -- 0.25. The alternative's *explanatory
    power* (does LM/embeddings/data alone explain the cross-system
    gap?) is low because the Stage-4 pre-Gemini score already exceeds
    most KG hybrids that themselves use Sonnet 4 / GPT-4 class models.
    pi(Alt) here is "Can Alt alone explain Obs?", not "Is Alt's
    reasoning correct?".
  - `pred_arch_explains` and `pred_lm_explains` -- 0.5 (predictions;
    the comparison strategy plus the observation carry the signal).
* **Foil for the contradiction operator** (`claim_kg_assumption_is_prevailing`)
  -- 0.5. The contradiction operator does the BP work, not the prior.
* **Limitations** -- 0.9-0.94. Author-acknowledged caveats; high
  confidence because they are openly stated.
"""

from .motivation import claim_kg_assumption_is_prevailing
from .s11_wiring import (
    alt_lm_data_embeddings,
    pred_arch_explains,
    pred_lm_explains,
)
from .s2_related_work import (
    claim_alt_architectures_complexity,
    claim_amem_zettelkasten_cost,
    claim_episodic_matters_for_long_horizon,
    claim_hindsight_complexity,
    claim_hnsw_ingest_delay,
    claim_longmemeval_decomposition,
    claim_lost_in_middle,
    claim_mem0_marginal_graph_gain,
    claim_mem0_pipeline_cost,
    claim_memgpt_letta_overhead,
    claim_memoryagentbench_conflict_failures,
    claim_merrill_simple_can_match,
    claim_other_benchmarks,
    claim_rag_canonical,
    claim_survey_landscape,
    claim_zep_temporal_overhead,
)
from .s3_design_principles import (
    claim_d1_queryable_not_injectable,
    claim_d2_temporal_with_decay,
    claim_d3_confidence_provenance,
    claim_d4_typed_hierarchical,
    claim_d5_contradiction_aware,
    claim_d6_zero_overhead_ingest,
)
from .s4_moorcheh_its import (
    claim_deterministic_retrieval,
    claim_instant_write_to_search,
    claim_mair_throughput,
    claim_mib_32x_compression,
    claim_sub90ms_retrieval,
)
from .s5_typed_schema import (
    claim_manual_type_assignment,
    claim_typing_dual_purpose,
)
from .s6_conflict_and_temporal import (
    claim_conflict_addresses_constraint_drift,
    claim_daily_intelligence,
    claim_non_destructive_supersession,
)
from .s7_ablation import (
    claim_recall_tokencost_tradeoff,
    claim_stage1_results,
    claim_stage2_results,
    claim_stage3_results,
    claim_stage4_results,
    claim_stage5_results,
)
from .s9_discussion import claim_recall_consistent_with_lme
from .s8_evaluation import (
    claim_complexity_score_definition,
    claim_idle_cost_serverless,
    claim_infra_complexity,
    claim_ingest_overhead,
    claim_lme_per_category,
    claim_locomo_per_category,
    claim_retrieval_overhead,
    claim_system_comparison_table,
)
from .s10_limitations import (
    claim_lim_benchmark_scope,
    claim_lim_inference_model_dependence,
    claim_lim_multi_agent_sharing,
    claim_lim_scale,
)


PRIORS: dict = {
    # --------------------------------------------------------------
    # Stage-by-stage benchmark measurements (Tables III-VI + Fig. 5)
    # --------------------------------------------------------------
    claim_stage1_results: (
        0.93,
        "Stage 1 baseline numbers (56.6% LME / 76.2% LoCoMo) read "
        "directly from Table III. Standard k=10 / threshold=0.15 / "
        "Sonnet 4 setup; small probability mass left for "
        "Sonnet-4-judge protocol noise.",
    ),
    claim_stage2_results: (
        0.94,
        "Stage 2 numbers (77.0% LME / 82.8% LoCoMo, +20.4 / +6.6 pp) "
        "from Table IV. The +20.4 pp delta is unambiguous in the "
        "table -- a qualitative-magnitude gain robust to seed and "
        "judge variance.",
    ),
    claim_stage3_results: (
        0.93,
        "Stage 3 numbers (79.2% / 82.9%, +2.2 / +0.1 pp) from Table V. "
        "Smaller delta; modestly more sensitive to prompt-protocol "
        "details.",
    ),
    claim_stage4_results: (
        0.93,
        "Stage 4 numbers (85.0% / 86.3%, +5.8 / +3.4 pp) from Table VI. "
        "Direct table readout.",
    ),
    claim_stage5_results: (
        0.93,
        "Stage 5 numbers (89.8% / 87.1%, +4.8 / +0.8 pp) from Fig. 5. "
        "Final SOTA configuration; the absolute values are the "
        "headline numbers of the paper.",
    ),
    # --------------------------------------------------------------
    # Per-category breakdowns and system comparison
    # --------------------------------------------------------------
    claim_lme_per_category: (
        0.93,
        "Table VII per-category LongMemEval results (95.7 / 100 / 93.3 "
        "/ 93.6 / 88.0 / 81.2). The 100% Single-session Assistant cell "
        "is striking; small mass for protocol-specific 'tied at 100%' "
        "rounding artefacts.",
    ),
    claim_locomo_per_category: (
        0.93,
        "Table VIII per-category LoCoMo results (78.7 / 70.8 / 92.4 / "
        "85.4). Direct readout.",
    ),
    claim_system_comparison_table: (
        0.92,
        "Table IX system comparison. All competing-system numbers are "
        "drawn from those systems' own published reports, so the "
        "table inherits whatever measurement noise those reports "
        "contain. The qualitative ranking is robust; absolute deltas "
        "between Mem0g/Zep/Memobase mid-ranks have minor uncertainty.",
    ),
    claim_complexity_score_definition: (
        0.95,
        "The four-binary-indicator definition is stated explicitly in "
        "Sec. IV.D. Mostly definitional.",
    ),
    # --------------------------------------------------------------
    # Memory Tax components (Table X)
    # --------------------------------------------------------------
    claim_ingest_overhead: (
        0.93,
        "Table X ingest column (Memanto 0 LLM/write; Mem0g >=2; Zep "
        ">=2). Direct architectural readout. The >=2 quantifications "
        "for Mem0g/Zep come from those systems' own architectural "
        "documentation.",
    ),
    claim_retrieval_overhead: (
        0.93,
        "Table X retrieval-latency column (<90 ms Memanto vs multi-"
        "second graph traversal). The Memanto number is a measured "
        "system property; the competitor numbers are characterisations "
        "of those systems' typical latency profiles.",
    ),
    claim_infra_complexity: (
        0.94,
        "Memanto requires only Moorcheh + API key; hybrids require "
        "separate vector + graph stacks. This is an architectural "
        "fact about the systems' deployment topology.",
    ),
    claim_idle_cost_serverless: (
        0.93,
        "Moorcheh is serverless (scales to zero); all evaluated "
        "competitors continuously provision compute. Architectural "
        "fact about the systems' billing model.",
    ),
    # --------------------------------------------------------------
    # Moorcheh engine architectural facts
    # --------------------------------------------------------------
    claim_mib_32x_compression: (
        0.92,
        "MIB achieves 32x compression with no measurable retrieval-"
        "signal loss. The 32x figure follows directly from binarising "
        "32-bit floats; the no-loss claim is from [@MoorchehITS] "
        "validation.",
    ),
    claim_instant_write_to_search: (
        0.94,
        "Sub-10 ms ingest follows from the no-indexing property; "
        "Table X reports `<10 ms`. Direct architectural consequence "
        "of MIB+EDM+ITS.",
    ),
    claim_deterministic_retrieval: (
        0.95,
        "Threshold-based ITS retrieval is exhaustive over the binary "
        "store and deterministic by construction (no graph-traversal "
        "stochasticity). This is a structural property, not an "
        "empirical claim.",
    ),
    claim_sub90ms_retrieval: (
        0.93,
        "Memanto end-to-end retrieval <90 ms (Table X) and Moorcheh "
        "9.6 ms distance calc on MAIR (Sec. III.C). Independently "
        "validated.",
    ),
    claim_mair_throughput: (
        0.92,
        "MAIR validation: 64-74% NDCG@10, 2000+ QPS, 6.6x speedup vs "
        "Pinecone+Cohere. Anchored by the separate [@MoorchehITS] "
        "preprint; small caveat for benchmark-specific protocol "
        "differences.",
    ),
    # --------------------------------------------------------------
    # Architectural assertions Memanto makes about its own design
    # --------------------------------------------------------------
    claim_typing_dual_purpose: (
        0.94,
        "Type-filtered retrieval + implicit priority/decay weighting "
        "are stated design properties of the schema. Definitional.",
    ),
    claim_conflict_addresses_constraint_drift: (
        0.92,
        "Sec. III.E describes the mechanism (same-type semantic "
        "similarity + 3-option resolution) and frames it as the "
        "constraint-drift remedy. Author's framing; a reviewer might "
        "question whether the mechanism is sufficient in all cases.",
    ),
    claim_non_destructive_supersession: (
        0.94,
        "Non-destructive supersession is a stated architectural "
        "property (superseded entries marked but retained). "
        "Definitional fact about the system.",
    ),
    claim_daily_intelligence: (
        0.93,
        "Markdown audit-trail artefacts are a stated architectural "
        "feature. Definitional.",
    ),
    claim_manual_type_assignment: (
        0.95,
        "Appendix C explicitly states type assignment is currently "
        "manual at write time. Direct readout.",
    ),
    # --------------------------------------------------------------
    # Six desiderata (D1-D6)
    # --------------------------------------------------------------
    claim_d1_queryable_not_injectable: (
        0.94,
        "D1 -- agents must query memory by relevance, not receive "
        "static injection. Normative design assertion; broadly "
        "accepted in the agent-memory literature.",
    ),
    claim_d2_temporal_with_decay: (
        0.94,
        "D2 -- memory needs temporal queries / versioning / decay. "
        "Aligned with LongMemEval's Knowledge-Update + Temporal-"
        "Reasoning categories.",
    ),
    claim_d3_confidence_provenance: (
        0.93,
        "D3 -- provenance metadata for confidence calibration. "
        "Normative assertion.",
    ),
    claim_d4_typed_hierarchical: (
        0.94,
        "D4 -- typed memory (episodic / semantic / procedural). "
        "Strongly grounded in Tulving + ENGRAM evidence.",
    ),
    claim_d5_contradiction_aware: (
        0.94,
        "D5 -- conflict detection vs constraint drift. "
        "MemoryAgentBench evidence + production-deployment "
        "experience.",
    ),
    claim_d6_zero_overhead_ingest: (
        0.94,
        "D6 -- zero-overhead ingestion. Production-deployment "
        "necessity, supported by the latency analysis in Sec. IV.E.",
    ),
    # --------------------------------------------------------------
    # Related-work characterisations of competing systems
    # --------------------------------------------------------------
    claim_memgpt_letta_overhead: (
        0.88,
        "MemGPT/Letta paging + summarisation latency-variability + "
        "fidelity-loss characterisation. Author's reading; aligned "
        "with the MemGPT paper.",
    ),
    claim_mem0_marginal_graph_gain: (
        0.92,
        "~2pp graph gain over base vector configuration, cited "
        "directly from Mem0's own ablation. The number is in Mem0's "
        "published paper.",
    ),
    claim_mem0_pipeline_cost: (
        0.92,
        "Mem0g pipeline = LLM extraction + index update + graph "
        "sync, ~2s/write. Architectural readout supplemented by "
        "Table X.",
    ),
    claim_zep_temporal_overhead: (
        0.92,
        "Zep temporal versioning + bi-temporal indexing at ~3s "
        "ingestion. Direct from Zep's paper plus Table X.",
    ),
    claim_amem_zettelkasten_cost: (
        0.9,
        "A-MEM full inference per insertion. Architectural fact; "
        "direct from A-MEM paper.",
    ),
    claim_hindsight_complexity: (
        0.92,
        "Hindsight = multi-query + reflection (4/4 complexity). "
        "Direct from Hindsight paper + Sec. IV.D scoring.",
    ),
    claim_merrill_simple_can_match: (
        0.85,
        "Merrill et al. finding that simple retrieval can outperform "
        "elaborate hierarchies. Author's summary of Merrill's work; "
        "small uncertainty about interpretation.",
    ),
    # --------------------------------------------------------------
    # Indexing/ingestion bottleneck literature
    # --------------------------------------------------------------
    claim_rag_canonical: (
        0.95,
        "RAG is the canonical paradigm. Well-established.",
    ),
    claim_hnsw_ingest_delay: (
        0.93,
        "HNSW indices need updates before queries. Architectural fact "
        "about ANN-based vector DBs.",
    ),
    claim_longmemeval_decomposition: (
        0.92,
        "LongMemEval's indexing/retrieval/reading decomposition is "
        "stated in their paper.",
    ),
    claim_lost_in_middle: (
        0.93,
        "Lost-in-middle [@LostMiddle] is widely cited and "
        "replicated.",
    ),
    claim_alt_architectures_complexity: (
        0.88,
        "HippoRAG / RAPTOR / REPLUG add complexity for long-range "
        "capability. Author's summary; well-established.",
    ),
    # --------------------------------------------------------------
    # Cognitive-science and benchmark setup
    # --------------------------------------------------------------
    claim_episodic_matters_for_long_horizon: (
        0.9,
        "MacPherson + ENGRAM finding that typed separation outperforms "
        "undifferentiated storage. Multiple converging sources.",
    ),
    claim_other_benchmarks: (
        0.92,
        "Existence of MemoryBank / PerLTQA / DialSim / "
        "MemoryAgentBench / Terranova benchmarks. Direct readout.",
    ),
    claim_memoryagentbench_conflict_failures: (
        0.93,
        "MemoryAgentBench finding that all evaluated systems fail on "
        "multi-hop conflict scenarios. Direct from their paper.",
    ),
    claim_survey_landscape: (
        0.92,
        "Heterogeneous 2024-26 memory-architecture survey landscape; "
        "Zhang / Abou Ali / Arunkumar / Wang / Sumers all cited. "
        "Direct readout.",
    ),
    # --------------------------------------------------------------
    # Discussion (V.B / V.C / V.D context)
    # --------------------------------------------------------------
    claim_recall_tokencost_tradeoff: (
        0.93,
        "Fig. 6: accuracy plateau above k=60, inflection at k=40; "
        "+20.4 pp >> 4x token cost. Direct figure readout.",
    ),
    claim_recall_consistent_with_lme: (
        0.9,
        "LongMemEval >20K-token finding + Liu et al.'s lost-in-middle "
        "as position-vs-volume. Cross-paper alignment.",
    ),
    # --------------------------------------------------------------
    # Limitations
    # --------------------------------------------------------------
    claim_lim_benchmark_scope: (
        0.94,
        "Both LongMemEval and LoCoMo are conversational; non-"
        "conversational workflows untested. Author-acknowledged.",
    ),
    claim_lim_inference_model_dependence: (
        0.94,
        "Stage 5 contributes +4.8 pp via Gemini 3 upgrade. Author-"
        "acknowledged.",
    ),
    claim_lim_scale: (
        0.92,
        "Moorcheh validated at 10M+ docs / 2000+ QPS; concurrent-"
        "agents stress test pending. Author-acknowledged.",
    ),
    claim_lim_multi_agent_sharing: (
        0.94,
        "Per-agent namespaces preclude shared memory; under "
        "development. Author-acknowledged.",
    ),
    # --------------------------------------------------------------
    # Central abduction: hypothesis / alternative / predictions
    # --------------------------------------------------------------
    alt_lm_data_embeddings: (
        0.25,
        "Alternative: 'Memanto wins because of LM/embeddings/data, "
        "not architecture.' pi(Alt) = explanatory power, not "
        "internal correctness. Stage-4 (pre-Gemini) Memanto already "
        "scores 85.0% LME / 86.3% LoCoMo with Sonnet 4 -- the same "
        "model class many KG hybrids use. The Stage-2 +20.4 pp gain "
        "comes from changing $k$ alone (no LM change). Therefore "
        "the alternative cannot *alone* explain the cross-system "
        "lead; pi(Alt) is set low.",
    ),
    pred_arch_explains: (
        0.5,
        "Prediction under the architectural hypothesis: the lead "
        "should appear before the LM upgrade. Kept neutral; the "
        "compare strategy plus the observation carry the signal.",
    ),
    pred_lm_explains: (
        0.5,
        "Prediction under the LM-dependence alternative: the lead "
        "should appear only after the LM upgrade. Kept neutral.",
    ),
    # --------------------------------------------------------------
    # Foil for the contradiction operator
    # --------------------------------------------------------------
    claim_kg_assumption_is_prevailing: (
        0.5,
        "The implicit prevailing-KG assumption ('KG complexity is "
        "necessary for high-fidelity memory'). Set at neutral 0.5 so "
        "the contradiction with Memanto's empirical demonstration "
        "(@claim_memanto_thesis) does the BP work rather than the "
        "prior.",
    ),
}
