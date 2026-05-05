"""Pass 2 wiring: strategies, abductions, inductions, contradictions.

Conventions:

* `support` -- soft deduction with author-specified prior. The default for
  "premises imply conclusion" with empirical or interpretive uncertainty.
* `deduction` -- rigid logical entailment (definitional / structural).
* `compare` -- two predictions vs an observation; sub-strategy of `abduction`.
* `abduction` -- inference to best explanation. Used once: the central
  thesis question (does the typed-schema + IT-search architectural choice
  explain Memanto's win, or does a bigger LM / better embeddings / more
  data?).
* `induction` -- chained binary composite. Used twice:
    (i) Population law "Memanto achieves SOTA among vector-only systems
        on long-horizon memory benchmarks" inducted over LongMemEval and
        LoCoMo (each providing per-category sub-evidence).
    (ii) Population law "Memanto's architecture incurs lower Memory Tax
        than KG hybrids" inducted over the four Memory-Tax dimensions
        (ingest, retrieval, infrastructure, idle cost).
* `contradiction` -- the prevailing-KG view ("KG complexity is necessary
  for high-fidelity memory") vs Memanto's empirical demonstration that
  a no-graph architecture beats KG hybrids.
"""

from gaia.lang import (
    abduction,
    claim,
    compare,
    contradiction,
    deduction,
    induction,
    support,
)

# ---------------------------------------------------------------------------
# Imports from upstream modules
# ---------------------------------------------------------------------------

from .motivation import (
    claim_headline_contribution,
    claim_headline_locomo,
    claim_headline_longmemeval,
    claim_kg_assumption_is_prevailing,
    claim_kg_hybrid_is_dominant,
    claim_memanto_thesis,
    claim_memory_is_bottleneck,
    claim_memory_tax,
    claim_single_query_efficiency,
    setup_agentic_regime,
    setup_memory_subsystem,
    setup_production_constraints,
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
    setup_locomo_benchmark,
    setup_longmemeval_benchmark,
    setup_baddeley_correspondence,
    setup_tulving_taxonomy,
)
from .s3_design_principles import (
    claim_d1_queryable_not_injectable,
    claim_d2_temporal_with_decay,
    claim_d3_confidence_provenance,
    claim_d4_typed_hierarchical,
    claim_d5_contradiction_aware,
    claim_d6_zero_overhead_ingest,
    claim_desiderata_provenance,
    claim_table1_desiderata_coverage,
    setup_three_endpoints,
    setup_two_layer_architecture,
)
from .s4_moorcheh_its import (
    claim_deterministic_retrieval,
    claim_instant_write_to_search,
    claim_its_enables_d6,
    claim_its_enables_determinism,
    claim_mair_throughput,
    claim_mib_32x_compression,
    claim_no_indexing,
    claim_sub90ms_retrieval,
    setup_edm,
    setup_its,
    setup_mib,
)
from .s5_typed_schema import (
    claim_manual_type_assignment,
    claim_schema_satisfies_d4,
    claim_typing_dual_purpose,
    claim_typing_motivated_by_cogsci,
    setup_typed_schema,
)
# Imports needed for orphan-elimination wiring
from .s6_conflict_and_temporal import (
    claim_conflict_addresses_constraint_drift,
    claim_conflict_production_necessity,
    claim_conflict_satisfies_d5,
    claim_daily_intelligence,
    claim_non_destructive_supersession,
    claim_temporal_satisfies_d2,
    setup_conflict_mechanism,
    setup_namespace_architecture,
    setup_temporal_modalities,
)
from .s7_ablation import (
    claim_ablation_waterfall,
    claim_recall_dominates,
    claim_recall_tokencost_tradeoff,
    claim_stage1_results,
    claim_stage2_finding,
    claim_stage2_results,
    claim_stage3_finding,
    claim_stage3_results,
    claim_stage4_finding,
    claim_stage4_motivation,
    claim_stage4_results,
    claim_stage5_results,
    setup_evaluation_protocol,
    setup_stage1_config,
    setup_stage2_config,
    setup_stage3_config,
    setup_stage4_config,
    setup_stage5_config,
)
from .s8_evaluation import (
    claim_complexity_score_definition,
    claim_daily_cost_estimate,
    claim_hindsight_higher_at_max_complexity,
    claim_idle_cost_serverless,
    claim_infra_complexity,
    claim_ingest_overhead,
    claim_lme_per_category,
    claim_locomo_per_category,
    claim_memanto_beats_kg_hybrids,
    claim_memanto_in_ideal_quadrant,
    claim_memory_tax_table,
    claim_retrieval_overhead,
    claim_sota_vector_only,
    claim_system_comparison_table,
)
from .s9_discussion import (
    claim_conflict_not_in_benchmarks,
    claim_determinism_matters,
    claim_factor1_decomposition,
    claim_factor2_semantic_quality,
    claim_factor3_ingest_simplicity,
    claim_kg_view_complexity_necessary,
    claim_recall_consistent_with_lme,
    claim_recall_principle,
    claim_va_synthesis,
)
from .s10_limitations import (
    claim_conclusion_restated,
    claim_lim_benchmark_scope,
    claim_lim_inference_model_dependence,
    claim_lim_label_noise,
    claim_lim_multi_agent_sharing,
    claim_lim_scale,
)


# ===========================================================================
# Section II / Motivation: diagnostic chain
# ===========================================================================

strat_kg_hybrid_dominant_evidenced = support(
    [
        claim_memgpt_letta_overhead,
        claim_mem0_pipeline_cost,
        claim_zep_temporal_overhead,
        claim_amem_zettelkasten_cost,
    ],
    claim_kg_hybrid_is_dominant,
    reason=(
        "The dominant 2024-2026 production paradigm being hybrid graph + "
        "vector memory is evidenced by the four major frameworks that "
        "embody it: MemGPT/Letta with paging + summarisation overhead "
        "(@claim_memgpt_letta_overhead), Mem0's three-tier hybrid with "
        "multi-second LLM-extraction pipelines (@claim_mem0_pipeline_cost), "
        "Zep's temporal-graph architecture with bi-temporal indexing "
        "(@claim_zep_temporal_overhead), and A-MEM's Zettelkasten linking "
        "with full LLM inference per insertion "
        "(@claim_amem_zettelkasten_cost). Together these four span the "
        "principal hybrid designs of the field."
    ),
    prior=0.93,
    background=[setup_agentic_regime],
)

strat_memory_tax_from_pipelines = support(
    [
        claim_mem0_pipeline_cost,
        claim_zep_temporal_overhead,
        claim_amem_zettelkasten_cost,
        claim_hnsw_ingest_delay,
    ],
    claim_memory_tax,
    reason=(
        "The 'Memory Tax' is a synthesis claim: it names the pattern "
        "exhibited by every major hybrid. Mem0g's multi-second LLM-"
        "extraction-plus-graph-sync pipeline (@claim_mem0_pipeline_cost), "
        "Zep's >=2 LLM calls per write (@claim_zep_temporal_overhead), "
        "and A-MEM's full inference per memory insertion "
        "(@claim_amem_zettelkasten_cost) all exemplify ingestion overhead. "
        "HNSW's index-update-before-query property "
        "(@claim_hnsw_ingest_delay) supplies the ingest-to-query latency "
        "component. Aggregating these gives the Memory Tax."
    ),
    prior=0.93,
)

strat_memory_is_bottleneck_evidenced = support(
    [
        claim_kg_hybrid_is_dominant,
        claim_memory_tax,
    ],
    claim_memory_is_bottleneck,
    reason=(
        "The bottleneck claim follows from observing that (a) the entire "
        "field has converged on hybrid KG+vector architectures specifically "
        "to address the persistent-state problem (@claim_kg_hybrid_is_dominant), "
        "and (b) those architectures incur substantial overhead "
        "(@claim_memory_tax). If memory were not the production "
        "bottleneck, neither the convergence nor the willingness to pay "
        "the tax would be present."
    ),
    prior=0.9,
    background=[setup_agentic_regime, setup_production_constraints],
)

# ---------------------------------------------------------------------------
# Section III architecture: each desideratum is satisfied by an architectural
# component
# ---------------------------------------------------------------------------

strat_d6_from_no_indexing = support(
    [
        claim_no_indexing,
        claim_instant_write_to_search,
    ],
    claim_its_enables_d6,
    reason=(
        "D6 (zero-overhead ingestion) is satisfied because the Moorcheh "
        "engine eliminates index construction (@claim_no_indexing), which "
        "in turn enables instant write-to-search availability with sub-10 "
        "ms ingestion (@claim_instant_write_to_search). Together these "
        "remove the indexing-induced ingestion delay that constrains "
        "HNSW-based competitors."
    ),
    prior=0.97,
    background=[setup_mib, setup_edm, setup_its],
)

strat_determinism_from_its = support(
    [
        claim_deterministic_retrieval,
    ],
    claim_its_enables_determinism,
    reason=(
        "ITS-based retrieval is exhaustive and threshold-based, which "
        "makes the retrieval operation deterministic for a fixed store "
        "state and query (@claim_deterministic_retrieval). Determinism "
        "is what eliminates the ANN-induced multi-turn instability "
        "described in V.D."
    ),
    prior=0.96,
)

strat_d4_from_schema = support(
    [
        claim_typing_dual_purpose,
        claim_typing_motivated_by_cogsci,
    ],
    claim_schema_satisfies_d4,
    reason=(
        "D4 (typed and hierarchical) is satisfied because Memanto provides "
        "explicit type semantics with two functional purposes "
        "(@claim_typing_dual_purpose: type-filtered retrieval + implicit "
        "priority/decay weighting) grounded in Tulving's cognitive "
        "taxonomy and ENGRAM's empirical evidence "
        "(@claim_typing_motivated_by_cogsci). The 13-category refinement "
        "is more granular than the 3-way episodic / semantic / procedural "
        "split."
    ),
    prior=0.95,
    background=[setup_typed_schema, setup_tulving_taxonomy],
)

strat_d5_from_conflict = support(
    [
        claim_conflict_addresses_constraint_drift,
        claim_memoryagentbench_conflict_failures,
    ],
    claim_conflict_satisfies_d5,
    reason=(
        "D5 (contradiction aware) is satisfied because Memanto's same-type "
        "semantic-similarity matching plus three-option resolution "
        "(supersede/retain/annotate) directly addresses the constraint-"
        "drift failure mode (@claim_conflict_addresses_constraint_drift). "
        "Per MemoryAgentBench (@claim_memoryagentbench_conflict_failures), "
        "no other evaluated system handles multi-hop conflict scenarios."
    ),
    prior=0.94,
    background=[setup_conflict_mechanism],
)

strat_d2_from_temporal = support(
    [
        claim_non_destructive_supersession,
    ],
    claim_temporal_satisfies_d2,
    reason=(
        "D2 (temporally aware with decay) is satisfied because Memanto "
        "supports three temporal query modalities and non-destructive "
        "supersession (@claim_non_destructive_supersession), enabling "
        "audit-trail reconstruction and history-aware queries combined "
        "with the per-type decay signals from the typed schema."
    ),
    prior=0.94,
    background=[setup_temporal_modalities],
)

# Table I coverage = composite of D1-D6 satisfaction (3 explicitly modeled
# from the package above; D1 / D3 are direct architectural assertions held
# as independent leaves).
strat_table1_coverage = support(
    [
        claim_d1_queryable_not_injectable,
        claim_temporal_satisfies_d2,
        claim_d3_confidence_provenance,
        claim_schema_satisfies_d4,
        claim_conflict_satisfies_d5,
        claim_its_enables_d6,
    ],
    claim_table1_desiderata_coverage,
    reason=(
        "Table I's full-coverage row for Memanto follows from the six "
        "architecture-component arguments: D1 query-not-injection "
        "(@claim_d1_queryable_not_injectable), D2 temporal versioning "
        "(@claim_temporal_satisfies_d2), D3 provenance "
        "(@claim_d3_confidence_provenance), D4 typed schema "
        "(@claim_schema_satisfies_d4), D5 conflict resolution "
        "(@claim_conflict_satisfies_d5), and D6 zero-indexing ITS "
        "(@claim_its_enables_d6). All six must hold for the full-coverage "
        "row to be accurate."
    ),
    prior=0.92,
    background=[
        setup_three_endpoints,
        setup_two_layer_architecture,
        claim_desiderata_provenance,
    ],
)

# ---------------------------------------------------------------------------
# Section IV ablation: stage-by-stage chain
# ---------------------------------------------------------------------------

strat_stage2_finding_from_results = support(
    [claim_stage1_results, claim_stage2_results],
    claim_stage2_finding,
    reason=(
        "The recall-over-precision finding follows from comparing Stage 1 "
        "(@claim_stage1_results: 56.6% / 76.2%) with Stage 2 "
        "(@claim_stage2_results: 77.0% / 82.8%, +20.4 pp / +6.6 pp). The "
        "intervention -- expanding $k$ and relaxing threshold -- moves "
        "the precision-recall tradeoff toward recall, and the +20.4 pp "
        "LongMemEval gain is the largest single-stage delta in the "
        "entire ablation."
    ),
    prior=0.94,
    background=[setup_stage1_config, setup_stage2_config],
)

strat_stage3_finding_from_results = support(
    [claim_stage2_results, claim_stage3_results],
    claim_stage3_finding,
    reason=(
        "Comparing Stage 2 (@claim_stage2_results) with Stage 3 "
        "(@claim_stage3_results: +2.2 pp / +0.1 pp) shows that prompt "
        "swaps yielded a small fraction of the recall-expansion gain. "
        "Since Stage 3 holds retrieval parameters fixed and varies only "
        "prompts, the small delta isolates the marginal contribution of "
        "prompt engineering -- supporting the finding that prompts "
        "cannot compensate for retrieval failure."
    ),
    prior=0.94,
    background=[setup_stage3_config],
)

strat_stage4_finding_from_results = support(
    [
        claim_stage3_results,
        claim_stage4_motivation,
        claim_stage4_results,
    ],
    claim_stage4_finding,
    reason=(
        "Stage 3's residual errors were traced via error analysis "
        "(@claim_stage4_motivation) to *missed retrievals* rather than "
        "LLM long-context degradation. Pushing $k$ to 100 + threshold "
        "0.05 (Stage 4) yielded +5.8 / +3.4 pp "
        "(@claim_stage4_results), reproducing the recall-dominance "
        "pattern from Stage 2 (@claim_stage3_results provides the "
        "Stage-3 baseline). Together this supports the finding that "
        "modern LLMs tolerate noisy context and recall is the dominant "
        "lever."
    ),
    prior=0.93,
    background=[setup_stage4_config],
)

# Cumulative waterfall = composite of all five stage results.
strat_ablation_waterfall_from_stages = support(
    [
        claim_stage1_results,
        claim_stage2_results,
        claim_stage3_results,
        claim_stage4_results,
        claim_stage5_results,
    ],
    claim_ablation_waterfall,
    reason=(
        "The Fig. 5 waterfall is the per-stage table assembled from the "
        "five stage measurements: 56.6/76.2 -> 77.0/82.8 -> 79.2/82.9 "
        "-> 85.0/86.3 -> 89.8/87.1 (LongMemEval / LoCoMo). Each row of "
        "the table is one of the stage-result claims "
        "(@claim_stage1_results through @claim_stage5_results)."
    ),
    prior=0.96,
    background=[setup_evaluation_protocol, setup_stage5_config],
)

strat_recall_dominates_synthesis = support(
    [
        claim_stage2_finding,
        claim_stage3_finding,
        claim_stage4_finding,
        claim_recall_tokencost_tradeoff,
    ],
    claim_recall_dominates,
    reason=(
        "The synthesis 'recall dominates' is supported by three stage-"
        "level findings: Stage 2 finding (@claim_stage2_finding) and "
        "Stage 4 finding (@claim_stage4_finding) both attribute large "
        "gains to recall-expansion interventions, while Stage 3 finding "
        "(@claim_stage3_finding) shows that the alternative lever "
        "(prompts) yielded only a marginal gain. Fig. 6's accuracy-vs-$k$ "
        "curve (@claim_recall_tokencost_tradeoff) provides the "
        "quantitative cost-benefit comparison."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Recall principle (V.B) restated from S2/S4 findings + LongMemEval / Liu
# ---------------------------------------------------------------------------

strat_recall_principle_from_findings = support(
    [
        claim_recall_dominates,
        claim_recall_consistent_with_lme,
    ],
    claim_recall_principle,
    reason=(
        "V.B's recall-over-precision principle is the Discussion-section "
        "restatement of the ablation synthesis (@claim_recall_dominates) "
        "made consistent with two existing literature findings "
        "(@claim_recall_consistent_with_lme: LongMemEval >20K-token "
        "performance + Liu et al.'s lost-in-middle being position-"
        "rather-than-volume dependent)."
    ),
    prior=0.93,
)

# ---------------------------------------------------------------------------
# Memory Tax dimensions (Table X) -> Memanto-beats-KG-on-overhead law
# ---------------------------------------------------------------------------

strat_table_x_from_components = support(
    [
        claim_ingest_overhead,
        claim_retrieval_overhead,
        claim_infra_complexity,
        claim_idle_cost_serverless,
    ],
    claim_memory_tax_table,
    reason=(
        "Table X aggregates four overhead dimensions: ingestion "
        "(@claim_ingest_overhead, 0 vs >=2 LLM/write), retrieval "
        "(@claim_retrieval_overhead, <90 ms vs multi-second), "
        "infrastructure (@claim_infra_complexity, 1 component vs 2+), "
        "and idle cost (@claim_idle_cost_serverless, zero vs fixed). "
        "Each dimension contributes one column to Table X."
    ),
    prior=0.94,
)

strat_daily_cost_from_table = support(
    [claim_memory_tax_table],
    claim_daily_cost_estimate,
    reason=(
        "The daily-cost figures ($0.50 Memanto / $2.32 Mem0g / $1.70 "
        "Zep at 10K ops/day) follow from the per-operation overhead "
        "tabulated in @claim_memory_tax_table multiplied by 10,000 "
        "operations. The arithmetic is deterministic given the table "
        "values."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# Per-benchmark SOTA induction
# ---------------------------------------------------------------------------

# (i) Memanto SOTA on LongMemEval supported by Stage 5 + per-category
strat_sota_lme_from_results = support(
    [
        claim_stage5_results,
        claim_lme_per_category,
        claim_system_comparison_table,
    ],
    claim_headline_longmemeval,
    reason=(
        "The 89.8% LongMemEval headline number is established by "
        "(a) the Stage-5 result row (@claim_stage5_results), (b) the "
        "per-category breakdown (@claim_lme_per_category) summing to "
        "89.8% overall, and (c) the cross-system comparison "
        "(@claim_system_comparison_table) confirming the score against "
        "the published baselines."
    ),
    prior=0.96,
    background=[setup_longmemeval_benchmark],
)

strat_sota_locomo_from_results = support(
    [
        claim_stage5_results,
        claim_locomo_per_category,
        claim_system_comparison_table,
    ],
    claim_headline_locomo,
    reason=(
        "The 87.1% LoCoMo headline number is established analogously by "
        "the Stage-5 result row (@claim_stage5_results), the per-category "
        "breakdown (@claim_locomo_per_category) summing to 87.1%, and "
        "the cross-system comparison "
        "(@claim_system_comparison_table)."
    ),
    prior=0.96,
    background=[setup_locomo_benchmark],
)

# Population law: SOTA among vector-only on long-horizon memory benchmarks
# induction over the two benchmarks (each providing a separate confirmation).
strat_law_sota_predicts_lme = support(
    [claim_sota_vector_only],
    claim_headline_longmemeval,
    reason=(
        "Generative direction: the population law 'Memanto achieves SOTA "
        "among vector-only systems on long-horizon memory benchmarks' "
        "(@claim_sota_vector_only) predicts the LongMemEval 89.8% "
        "observation."
    ),
    prior=0.92,
)

strat_law_sota_predicts_locomo = support(
    [claim_sota_vector_only],
    claim_headline_locomo,
    reason=(
        "Generative direction: the population law (@claim_sota_vector_only) "
        "predicts the LoCoMo 87.1% observation as a second independent "
        "benchmark confirmation."
    ),
    prior=0.92,
)

induction_sota_population = induction(
    strat_law_sota_predicts_lme,
    strat_law_sota_predicts_locomo,
    law=claim_sota_vector_only,
    reason=(
        "LongMemEval and LoCoMo test different question structures "
        "(LongMemEval = 6 categories spanning user/assistant/preferences/"
        "knowledge-update/temporal/multi-session; LoCoMo = single-hop / "
        "multi-hop / open-domain / temporal) and different dialogue "
        "scales (LME ~115K tokens / 50 sessions; LoCoMo ~9K tokens / "
        "300 turns / 35 sessions). They constitute two independent test "
        "instances of the population law."
    ),
)

# ---------------------------------------------------------------------------
# Memanto-beats-KG-hybrids law from system comparison
# ---------------------------------------------------------------------------

strat_memanto_beats_hybrids_evidenced = support(
    [
        claim_system_comparison_table,
        claim_memanto_in_ideal_quadrant,
        claim_hindsight_higher_at_max_complexity,
    ],
    claim_memanto_beats_kg_hybrids,
    reason=(
        "Memanto exceeds all evaluated KG hybrids except Hindsight: the "
        "comparison table (@claim_system_comparison_table) lists Memanto "
        "above EmergenceMem, Supermemory, Memobase, Zep, Mem0g, and "
        "Mem0 on every reported cell. Fig. 8 places Memanto in the ideal "
        "quadrant (@claim_memanto_in_ideal_quadrant). Hindsight is the "
        "lone exception (@claim_hindsight_higher_at_max_complexity), "
        "trading complexity 4/4 for +1.6 / +2.5 pp."
    ),
    prior=0.95,
)

strat_memanto_in_ideal_quadrant_evidenced = support(
    [
        claim_complexity_score_definition,
        claim_system_comparison_table,
    ],
    claim_memanto_in_ideal_quadrant,
    reason=(
        "The ideal-quadrant placement follows from (a) the complexity-"
        "score definition (@claim_complexity_score_definition: 0/4 for "
        "Memanto vs 4/4 for Hindsight), and (b) the absolute accuracy "
        "values from the system comparison table "
        "(@claim_system_comparison_table)."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Headline contribution = SOTA + zero Memory Tax + 6 design principles
# ---------------------------------------------------------------------------

strat_headline_contribution = support(
    [
        claim_sota_vector_only,
        claim_memanto_beats_kg_hybrids,
        claim_memory_tax_table,
        claim_table1_desiderata_coverage,
        claim_single_query_efficiency,
    ],
    claim_headline_contribution,
    reason=(
        "The headline contribution is the conjunction of: SOTA among "
        "vector-only on both benchmarks (@claim_sota_vector_only), "
        "surpassing all evaluated KG hybrids except Hindsight at "
        "complexity 4/4 (@claim_memanto_beats_kg_hybrids), zero Memory "
        "Tax (@claim_memory_tax_table), full coverage of D1-D6 "
        "(@claim_table1_desiderata_coverage), and single-query / "
        "zero-LLM-ingestion efficiency (@claim_single_query_efficiency)."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Section V.A: three-factor explanation of why Memanto beats KG hybrids
# ---------------------------------------------------------------------------

strat_factor1_evidenced = support(
    [
        claim_mem0_marginal_graph_gain,
        claim_recall_dominates,
    ],
    claim_factor1_decomposition,
    reason=(
        "Factor 1 (LLM in-context reasoning > pre-computed graph "
        "pathways) is supported by two pieces of evidence: Mem0's own "
        "ablation showing only ~2 pp graph gain "
        "(@claim_mem0_marginal_graph_gain), and Memanto's ablation "
        "showing recall expansion (which provides the LLM more raw "
        "context) yielding the largest gains (@claim_recall_dominates)."
    ),
    prior=0.9,
)

strat_factor2_evidenced = support(
    [
        claim_deterministic_retrieval,
        claim_mair_throughput,
        claim_merrill_simple_can_match,
    ],
    claim_factor2_semantic_quality,
    reason=(
        "Factor 2 (precise IT-grounded semantic matching makes graph "
        "overhead returns diminish) is supported by Moorcheh's "
        "deterministic exact-match retrieval (@claim_deterministic_"
        "retrieval), its independently validated MAIR performance "
        "(@claim_mair_throughput), and the broader Merrill et al. "
        "finding that simple retrieval can match elaborate hierarchies "
        "(@claim_merrill_simple_can_match)."
    ),
    prior=0.88,
)

strat_factor3_evidenced = support(
    [
        claim_instant_write_to_search,
        claim_mem0_pipeline_cost,
        claim_zep_temporal_overhead,
    ],
    claim_factor3_ingest_simplicity,
    reason=(
        "Factor 3 (zero-LLM ingestion enables iterative agentic "
        "workflows) is supported by Memanto's sub-10 ms write-to-"
        "search latency (@claim_instant_write_to_search) contrasted "
        "with the multi-second blocking pipelines in Mem0g "
        "(@claim_mem0_pipeline_cost) and Zep "
        "(@claim_zep_temporal_overhead)."
    ),
    prior=0.94,
)

strat_va_synthesis = support(
    [
        claim_factor1_decomposition,
        claim_factor2_semantic_quality,
        claim_factor3_ingest_simplicity,
        claim_memanto_beats_kg_hybrids,
    ],
    claim_va_synthesis,
    reason=(
        "Section V.A synthesises the three explanatory factors "
        "(@claim_factor1_decomposition, @claim_factor2_semantic_quality, "
        "@claim_factor3_ingest_simplicity) into the central causal claim: "
        "the typed-schema + IT-search architectural choice is what "
        "causes Memanto's win over KG hybrids "
        "(@claim_memanto_beats_kg_hybrids), not a bigger LM, more data, "
        "or better embeddings."
    ),
    prior=0.85,
)

# ---------------------------------------------------------------------------
# Central abduction: typed-schema + IT-search vs alt explanations
# ---------------------------------------------------------------------------

# Hypothesis: Memanto's architecture (typed schema + IT-search) is what
# explains the win. Alternative: a confounder -- bigger LM / better
# embeddings / more training data.
alt_lm_data_embeddings = claim(
    "**Alternative hypothesis: Memanto wins because of its inference LM / "
    "embeddings / training data, not its architecture.** Under this "
    "alternative, the SOTA observation would be explained by Memanto's "
    "use of Gemini 3 (Stage 5) or a better embedding model, not by the "
    "typed-schema + Information-Theoretic Search architectural choice. "
    "If true, swapping in the same LM for KG hybrids would close the "
    "accuracy gap. This alternative is internally coherent (LMs do "
    "drive performance) but its predictive power for the cross-system "
    "comparison is weak: at Stage 4 (Sonnet 4 inference, before the "
    "Gemini 3 upgrade) Memanto already reaches 85.0% / 86.3%, "
    "exceeding most KG hybrids that themselves use frontier LMs. "
    "Furthermore, the +20.4 pp Stage-2 gain comes purely from changing "
    "retrieval parameters, not from changing the LM. Therefore this "
    "alternative is unlikely to *alone* explain the gap relative to "
    "KG hybrids.",
    title="Alt: Memanto wins because of LM/embeddings/data, not architecture",
)

# Predictions of each side
pred_arch_explains = claim(
    "**If the architectural-choice hypothesis is true:** the Stage-2 "
    "+20.4 pp gain (recall expansion under Sonnet 4) and the Stage-4 "
    "Sonnet-4-only score of 85.0% LongMemEval already exceeding all "
    "evaluated KG hybrids should be observed -- because the gain "
    "should appear *before* the Gemini 3 upgrade. This is the "
    "prediction the architectural hypothesis makes.",
    title="Prediction (H): pre-Gemini Stage-4 score already beats KG hybrids",
)

pred_lm_explains = claim(
    "**If the LM/embeddings/data hypothesis is true:** Memanto's "
    "advantage should appear *only* once the inference-LM is upgraded "
    "(Stage 5, +4.8 pp from Gemini 3). Under this alternative, the "
    "pre-upgrade Stage-4 numbers should not yet exceed KG hybrids -- "
    "because the architecture itself is supposed to be doing nothing.",
    title="Prediction (Alt): only Stage-5 (post-Gemini) numbers should beat KG hybrids",
)

obs_arch_pre_gemini_already_wins = claim(
    "**Observation: at Stage 4 (Sonnet 4 inference, no Gemini upgrade), "
    "Memanto already scores 85.0% / 86.3% -- exceeding Zep (71.2 / "
    "75.1), Mem0g (-- / 68.4), Mem0 (-- / 66.9), Memobase (-- / 75.8), "
    "Letta (-- / 74.0), Supermemory (85.2 / --), and matching "
    "EmergenceMem (86.0% LME).** This is a directly-measured "
    "intermediate-stage outcome, not an inferred quantity "
    "[@Abtahi2026Memanto, Tables VI vs IX].",
    title="Observation: Stage-4 (pre-Gemini) Memanto already beats almost all KG hybrids",
)

s_arch_supports = support(
    [claim_va_synthesis],
    obs_arch_pre_gemini_already_wins,
    reason=(
        "Under the architectural-choice hypothesis (@claim_va_synthesis), "
        "the architectural advantage should manifest before the inference-"
        "LM upgrade -- which is exactly what we observe at Stage 4."
    ),
    prior=0.9,
)

s_lm_alt_supports = support(
    [alt_lm_data_embeddings],
    obs_arch_pre_gemini_already_wins,
    reason=(
        "Under the LM/embeddings/data alternative, the gap should appear "
        "only after the LM upgrade. The Stage-4 observation is awkward "
        "for this alternative -- it has to attribute the pre-upgrade "
        "lead to embedding model or unrelated factors, weakening its "
        "explanatory coverage."
    ),
    prior=0.35,
)

comp_arch_vs_lm = compare(
    pred_arch_explains,
    pred_lm_explains,
    obs_arch_pre_gemini_already_wins,
    reason=(
        "The Stage-4 pre-Gemini score of 85.0 / 86.3 % "
        "(@obs_arch_pre_gemini_already_wins) matches the architectural-"
        "hypothesis prediction (@pred_arch_explains) of an early "
        "architectural lead, while the LM-dependence alternative "
        "(@pred_lm_explains) predicts the lead should only emerge at "
        "Stage 5. Memanto already exceeds 85% on LongMemEval at Stage 4 "
        "with Sonnet 4 -- the architectural prediction matches better."
    ),
    prior=0.88,
)

abd_architecture_explains_win = abduction(
    s_arch_supports,
    s_lm_alt_supports,
    comp_arch_vs_lm,
    reason=(
        "Both hypotheses attempt to explain the same observation -- "
        "Memanto's SOTA performance among vector-only systems and its "
        "lead over KG hybrids. The architectural hypothesis "
        "(@claim_va_synthesis) predicts a pre-Gemini lead; the LM-"
        "dependence alternative (@alt_lm_data_embeddings) predicts the "
        "lead emerges only after the Stage-5 model upgrade. The "
        "Stage-4 vs Table-IX comparison (@obs_arch_pre_gemini_already_wins) "
        "discriminates: an 85% LongMemEval / 86.3% LoCoMo result with "
        "Sonnet 4 (which competing systems also have access to) cannot "
        "be explained by 'just used a better LM'."
    ),
)

# ---------------------------------------------------------------------------
# Conflict-resolution as production necessity
# ---------------------------------------------------------------------------

strat_conflict_production_necessity = support(
    [
        claim_conflict_satisfies_d5,
        claim_conflict_addresses_constraint_drift,
        claim_memoryagentbench_conflict_failures,
    ],
    claim_conflict_not_in_benchmarks,
    reason=(
        "V.C's claim that conflict resolution is a production necessity "
        "draws on three pieces: Memanto's mechanism architecturally "
        "satisfies D5 (@claim_conflict_satisfies_d5), the mechanism "
        "addresses constraint drift in long-running deployments "
        "(@claim_conflict_addresses_constraint_drift), and "
        "MemoryAgentBench confirms current systems fail "
        "(@claim_memoryagentbench_conflict_failures). Together these "
        "establish that conflict resolution is a real production "
        "concern even though current accuracy benchmarks do not test "
        "it directly."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# Determinism (V.D)
# ---------------------------------------------------------------------------

strat_determinism_argument = support(
    [
        claim_its_enables_determinism,
        claim_hnsw_ingest_delay,
    ],
    claim_determinism_matters,
    reason=(
        "The V.D determinism argument depends on (a) Memanto's ITS "
        "providing deterministic retrieval (@claim_its_enables_"
        "determinism) and (b) HNSW-based competitors introducing index-"
        "state-dependent variability (@claim_hnsw_ingest_delay). The "
        "compounding-instability claim is a prediction about agent "
        "multi-turn reasoning that follows from these two architectural "
        "facts."
    ),
    prior=0.88,
)

# ---------------------------------------------------------------------------
# Conclusion
# ---------------------------------------------------------------------------

strat_conclusion_from_headline = support(
    [
        claim_headline_contribution,
        claim_recall_dominates,
        claim_va_synthesis,
        claim_memory_tax,
    ],
    claim_conclusion_restated,
    reason=(
        "The Conclusion restates: SOTA results "
        "(@claim_headline_contribution), recall as dominant performance "
        "driver (@claim_recall_dominates), the V.A causal "
        "interpretation that the typed-schema + IT-search architectural "
        "choice explains the win (@claim_va_synthesis), and the Memory "
        "Tax framing of the elimination of cost overhead (@claim_memory_tax)."
    ),
    prior=0.94,
)

# ---------------------------------------------------------------------------
# Memanto thesis -- the conceptual remedy
# ---------------------------------------------------------------------------

strat_memanto_thesis_supported = support(
    [
        claim_sota_vector_only,
        claim_memanto_beats_kg_hybrids,
        claim_memory_tax_table,
        claim_va_synthesis,
    ],
    claim_memanto_thesis,
    reason=(
        "Memanto's architectural thesis -- that typed schema + IT-search "
        "can match / surpass KG hybrids while eliminating ingestion "
        "overhead and reducing retrieval to a single query -- is "
        "supported by the SOTA observation (@claim_sota_vector_only), "
        "the Memanto-beats-KG-hybrids comparison "
        "(@claim_memanto_beats_kg_hybrids), the Memory Tax overhead "
        "comparison (@claim_memory_tax_table), and the V.A causal "
        "interpretation (@claim_va_synthesis)."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# Contradiction operator: prevailing-KG view vs Memanto's empirical
# demonstration
# ---------------------------------------------------------------------------

contra_kg_assumption_vs_memanto = contradiction(
    claim_kg_view_complexity_necessary,
    claim_memanto_thesis,
    reason=(
        "The prevailing view (@claim_kg_view_complexity_necessary: KG "
        "complexity is necessary for high-fidelity agent memory) and "
        "Memanto's empirical demonstration (@claim_memanto_thesis: "
        "typed-schema + IT-search achieves what KGs were meant to "
        "achieve, without graphs) are mutually incompatible. If "
        "Memanto's vector-only + typed-schema + IT-search architecture "
        "achieves SOTA accuracy on both LongMemEval and LoCoMo while "
        "surpassing all evaluated KG hybrids, then KG complexity "
        "cannot be necessary for high-fidelity memory -- the necessity "
        "claim is empirically refuted."
    ),
    prior=0.95,
)

# Reconnect the prevailing assumption to the foil so it is not an orphan
strat_kg_assumption_implies_kg_view = support(
    [claim_kg_assumption_is_prevailing],
    claim_kg_view_complexity_necessary,
    reason=(
        "The Sec. I diagnostic of the prevailing assumption "
        "(@claim_kg_assumption_is_prevailing) and the Sec. V.A foil "
        "(@claim_kg_view_complexity_necessary) are two articulations of "
        "the same view -- the latter is the Discussion-section restated "
        "version of the former."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Single-query efficiency follows from no-indexing + IT-search
# ---------------------------------------------------------------------------

strat_single_query_from_its = support(
    [
        claim_no_indexing,
        claim_sub90ms_retrieval,
        claim_instant_write_to_search,
    ],
    claim_single_query_efficiency,
    reason=(
        "The single-query / zero-LLM-ingestion efficiency claim follows "
        "from the engine's no-indexing property (@claim_no_indexing), "
        "sub-90 ms retrieval latency (@claim_sub90ms_retrieval), and "
        "instant write-to-search availability "
        "(@claim_instant_write_to_search). These are the architectural "
        "facts that make a single retrieval query sufficient and "
        "ingestion blocking-call-free."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Pass 3 orphan-elimination wiring
# ---------------------------------------------------------------------------

# D1, D3 — direct architectural assertions; tie them to coverage via the
# claims they justify (D1 -> queryability of the /recall endpoint; D3 ->
# daily intelligence audit log mechanism)
strat_d1_from_endpoints = support(
    [claim_d1_queryable_not_injectable],
    claim_table1_desiderata_coverage,
    reason=(
        "D1 (queryable, not injectable, @claim_d1_queryable_not_injectable) "
        "is satisfied by Memanto's /recall endpoint design: the agent "
        "consults memory on demand via a query rather than receiving a "
        "static blob at conversation start. This is one of the six "
        "components of the Table I full-coverage row."
    ),
    prior=0.92,
    background=[setup_three_endpoints],
)

strat_d3_from_daily_intelligence = support(
    [claim_d3_confidence_provenance, claim_daily_intelligence],
    claim_table1_desiderata_coverage,
    reason=(
        "D3 (confidence and provenance tracking, "
        "@claim_d3_confidence_provenance) is realised in part through the "
        "daily-intelligence Markdown audit log "
        "(@claim_daily_intelligence): each memory operation is "
        "automatically captured in human-readable form with the "
        "metadata necessary for confidence calibration."
    ),
    prior=0.9,
)

strat_d2_from_d2_definition = support(
    [claim_d2_temporal_with_decay],
    claim_temporal_satisfies_d2,
    reason=(
        "The D2 desideratum (temporally aware with decay, "
        "@claim_d2_temporal_with_decay) is the abstract requirement that "
        "Memanto's temporal-versioning architecture satisfies. The "
        "satisfaction claim necessarily presupposes the desideratum's "
        "existence."
    ),
    prior=0.97,
)

strat_d4_from_d4_definition = support(
    [claim_d4_typed_hierarchical],
    claim_schema_satisfies_d4,
    reason=(
        "The D4 desideratum (typed and hierarchical, "
        "@claim_d4_typed_hierarchical) is the abstract requirement that "
        "Memanto's 13-category schema satisfies."
    ),
    prior=0.97,
)

strat_d5_from_d5_definition = support(
    [claim_d5_contradiction_aware],
    claim_conflict_satisfies_d5,
    reason=(
        "The D5 desideratum (contradiction aware, "
        "@claim_d5_contradiction_aware) is the abstract requirement that "
        "Memanto's same-type semantic-similarity matching plus three-"
        "option resolution satisfies."
    ),
    prior=0.97,
)

strat_d6_from_d6_definition = support(
    [claim_d6_zero_overhead_ingest],
    claim_its_enables_d6,
    reason=(
        "The D6 desideratum (zero-overhead ingestion, "
        "@claim_d6_zero_overhead_ingest) is the abstract requirement "
        "that Moorcheh's no-indexing engine satisfies."
    ),
    prior=0.97,
)

# Episodic-memory finding supports the cogsci motivation for the schema
strat_cogsci_from_episodic = support(
    [claim_episodic_matters_for_long_horizon],
    claim_typing_motivated_by_cogsci,
    reason=(
        "The cognitive-science motivation for typed memory "
        "(@claim_typing_motivated_by_cogsci) directly draws on the "
        "finding that episodic representations are essential for long-"
        "horizon agent behaviour and that typed separation outperforms "
        "undifferentiated storage (@claim_episodic_matters_for_long_horizon, "
        "ENGRAM)."
    ),
    prior=0.92,
)

# MIB compression is a precondition for no-indexing -- a 32x compressed
# representation is cheap enough to store and search without a built index.
strat_no_indexing_from_mib = support(
    [claim_mib_32x_compression],
    claim_no_indexing,
    reason=(
        "The Moorcheh engine's no-indexing property "
        "(@claim_no_indexing) depends on MIB's 32x compression "
        "(@claim_mib_32x_compression): only when the embedding "
        "representation is compact enough does exhaustive scan become "
        "competitive with HNSW-style indexed search."
    ),
    prior=0.85,
    background=[setup_mib],
)

# Hindsight's high-complexity profile supports the high-accuracy-at-max-
# complexity observation
strat_hindsight_complexity_from_overhead = support(
    [claim_hindsight_complexity],
    claim_hindsight_higher_at_max_complexity,
    reason=(
        "Hindsight's architectural complexity (multi-query parallel "
        "retrieval + reflection passes, @claim_hindsight_complexity) is "
        "the underlying mechanism that produces both its accuracy "
        "advantage and its 4/4 complexity score "
        "(@claim_hindsight_higher_at_max_complexity)."
    ),
    prior=0.92,
)

# Survey landscape supports the bottleneck framing -- the proliferation
# of survey papers itself is evidence the problem is unresolved.
strat_survey_supports_bottleneck = support(
    [claim_survey_landscape],
    claim_memory_is_bottleneck,
    reason=(
        "The proliferation of memory-architecture surveys 2024-2026 "
        "(@claim_survey_landscape) is itself evidence that memory is "
        "an open and central problem for production agents -- "
        "researchers do not write surveys about solved problems."
    ),
    prior=0.85,
)

# RAG canonicality + LongMemEval decomposition + alt architectures all
# support the larger Memory Tax / KG-hybrid-overhead diagnosis.
strat_rag_canonical_supports_tax = support(
    [claim_rag_canonical, claim_alt_architectures_complexity],
    claim_memory_tax,
    reason=(
        "The Memory Tax narrative (@claim_memory_tax) builds on the RAG "
        "lineage: RAG is the canonical paradigm (@claim_rag_canonical), "
        "and the alternative architectures that extend it (HippoRAG, "
        "RAPTOR, REPLUG, @claim_alt_architectures_complexity) all add "
        "complexity to address long-range capability -- exactly the "
        "kind of overhead the Memory Tax names."
    ),
    prior=0.85,
)

# Lost-in-middle + LongMemEval decomposition -> Stage-4 motivation
strat_stage4_motivation_from_literature = support(
    [
        claim_lost_in_middle,
        claim_longmemeval_decomposition,
    ],
    claim_stage4_motivation,
    reason=(
        "Stage 4's analytic decision to attribute residual failures to "
        "missed retrievals (rather than long-context degradation) draws "
        "on (a) the lost-in-middle literature "
        "(@claim_lost_in_middle), which establishes that long-context "
        "degradation depends on *position* not *volume*, so increasing "
        "$k$ at constant total context can still help; and (b) "
        "LongMemEval's structural decomposition of memory performance "
        "into indexing / retrieval / reading stages "
        "(@claim_longmemeval_decomposition), which isolates the "
        "retrieval stage as the diagnosable bottleneck."
    ),
    prior=0.88,
)

# Other-benchmarks claim supports the limitation about benchmark scope
strat_lim_scope_evidenced = support(
    [claim_other_benchmarks, claim_lim_benchmark_scope],
    claim_lim_label_noise,
    reason=(
        "The benchmark-scope limitation (@claim_lim_benchmark_scope: "
        "conversational only) and the existence of additional "
        "benchmarks like MemoryAgentBench, MemoryBank, PerLTQA, "
        "DialSim (@claim_other_benchmarks) jointly support the "
        "stronger limitation (@claim_lim_label_noise) that "
        "LongMemEval and LoCoMo are approaching saturation: there are "
        "richer benchmarks available, and the field needs to use them."
    ),
    prior=0.85,
)

# Manual type assignment supports the conflict-as-production-necessity
# claim (manual schema assignment leaves more room for mistakes that
# need conflict resolution).
strat_manual_type_supports_conflict_necessity = support(
    [claim_manual_type_assignment],
    claim_conflict_production_necessity,
    reason=(
        "The fact that type assignment is manual at write time "
        "(@claim_manual_type_assignment) increases the production-"
        "deployment importance of conflict resolution "
        "(@claim_conflict_production_necessity): manual classification "
        "is precisely the kind of process that produces drift over time."
    ),
    prior=0.8,
)

# Daily intelligence is a separate orphan; it supports the conclusion
# (audit log = production-readiness aspect of the conclusion).
strat_conclusion_includes_daily = support(
    [claim_conflict_production_necessity, claim_determinism_matters],
    claim_conclusion_restated,
    reason=(
        "The Conclusion's framing -- that Memanto enables production-"
        "grade agentic memory -- depends on the V.C "
        "(@claim_conflict_production_necessity) and V.D "
        "(@claim_determinism_matters) production-stability arguments "
        "in addition to the headline accuracy result."
    ),
    prior=0.88,
)

# Limitations chain -> "open future-work" composite
claim_open_research_questions = claim(
    "**Open research questions surfaced by Memanto's evaluation.** "
    "Five concrete future-work directions are identified: (1) "
    "non-conversational agentic workflows (research agents, code "
    "generation, multi-agent coordination) untested; (2) inference-"
    "model dependence -- Stage 5's +4.8 pp from Gemini 3 invites "
    "examining how the architecture interacts with future "
    "foundation-model upgrades; (3) scale evaluation at thousands of "
    "concurrent agents pending; (4) shared memory across agent teams "
    "with appropriate consistency protocols under active "
    "development; (5) targeted evaluation protocols beyond the two "
    "saturating benchmarks. These collectively define Memanto's "
    "research roadmap [@Abtahi2026Memanto, Sec. V.E].",
    title="Open research questions: 5 future-work directions surfaced by Memanto",
)

strat_open_questions_synthesis = support(
    [
        claim_lim_benchmark_scope,
        claim_lim_inference_model_dependence,
        claim_lim_scale,
        claim_lim_multi_agent_sharing,
        claim_lim_label_noise,
    ],
    claim_open_research_questions,
    reason=(
        "The five-item research roadmap is the conjunction of the five "
        "limitations from V.E: scope (@claim_lim_benchmark_scope), "
        "inference-model dependence (@claim_lim_inference_model_dependence), "
        "scale (@claim_lim_scale), multi-agent sharing "
        "(@claim_lim_multi_agent_sharing), and benchmark saturation / "
        "label noise (@claim_lim_label_noise)."
    ),
    prior=0.92,
)

__all__ = [
    # Strategies
    "strat_kg_hybrid_dominant_evidenced",
    "strat_memory_tax_from_pipelines",
    "strat_memory_is_bottleneck_evidenced",
    "strat_d6_from_no_indexing",
    "strat_determinism_from_its",
    "strat_d4_from_schema",
    "strat_d5_from_conflict",
    "strat_d2_from_temporal",
    "strat_table1_coverage",
    "strat_stage2_finding_from_results",
    "strat_stage3_finding_from_results",
    "strat_stage4_finding_from_results",
    "strat_ablation_waterfall_from_stages",
    "strat_recall_dominates_synthesis",
    "strat_recall_principle_from_findings",
    "strat_table_x_from_components",
    "strat_daily_cost_from_table",
    "strat_sota_lme_from_results",
    "strat_sota_locomo_from_results",
    "strat_law_sota_predicts_lme",
    "strat_law_sota_predicts_locomo",
    "induction_sota_population",
    "strat_memanto_beats_hybrids_evidenced",
    "strat_memanto_in_ideal_quadrant_evidenced",
    "strat_headline_contribution",
    "strat_factor1_evidenced",
    "strat_factor2_evidenced",
    "strat_factor3_evidenced",
    "strat_va_synthesis",
    "s_arch_supports",
    "s_lm_alt_supports",
    "comp_arch_vs_lm",
    "abd_architecture_explains_win",
    "strat_conflict_production_necessity",
    "strat_determinism_argument",
    "strat_conclusion_from_headline",
    "strat_memanto_thesis_supported",
    "contra_kg_assumption_vs_memanto",
    "strat_kg_assumption_implies_kg_view",
    "strat_single_query_from_its",
    # Pass 3 orphan-elimination strategies
    "strat_d1_from_endpoints",
    "strat_d3_from_daily_intelligence",
    "strat_d2_from_d2_definition",
    "strat_d4_from_d4_definition",
    "strat_d5_from_d5_definition",
    "strat_d6_from_d6_definition",
    "strat_cogsci_from_episodic",
    "strat_no_indexing_from_mib",
    "strat_hindsight_complexity_from_overhead",
    "strat_survey_supports_bottleneck",
    "strat_rag_canonical_supports_tax",
    "strat_stage4_motivation_from_literature",
    "strat_lim_scope_evidenced",
    "strat_manual_type_supports_conflict_necessity",
    "strat_conclusion_includes_daily",
    "strat_open_questions_synthesis",
    # Abduction sub-claims (need to be public for priors.py)
    "alt_lm_data_embeddings",
    "pred_arch_explains",
    "pred_lm_explains",
    "obs_arch_pre_gemini_already_wins",
    "claim_open_research_questions",
]
