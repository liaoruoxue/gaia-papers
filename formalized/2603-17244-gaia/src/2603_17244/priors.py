"""Priors for independent (leaf) claims in the 2603.17244 (Kumiho) formalization.

Calibration philosophy
----------------------

* **Mathematical / definitional facts** about classical logic, AGM
  prerequisites, recovery-postulate critiques in the literature -- 0.95-0.97.
  These are well-established and citable.
* **Architectural assertions about the deployed system** (P1-P10
  principles, kref URI design, decoupling mechanisms, atomic writes,
  threat-model entries) -- 0.92-0.96. Definitional / observable facts
  about the system the authors ship.
* **Per-system characterizations of competing systems** (Graphiti,
  Mem0, Letta, etc.) come in via support strategies in s11_wiring.py and
  are NOT priors here -- they are derived. Their priors are on their
  *underlying* observations or summary tables (Table 1, Table 9).
* **Numerical readouts from the paper's tables and figures** (Table 11,
  12, 15, 16, 17, 18) -- 0.92-0.95. Direct measurements with explicit
  citation; the modest discount reflects evaluation-protocol noise
  (LLM-judge variance, prompt adaptation differences) and the
  acknowledged self-evaluation bias.
* **Independent-reproduction note** -- 0.93. External independent
  verification by the LoCoMo-Plus authors.
* **Author-acknowledged limitations** -- 0.9-0.94. High confidence
  because they are openly stated and unlikely to be overstated.
* **Hypothesis / alternative in abductions**:
  - `claim_recovery_alt_arch_bug` -- 0.25. The alternative's *explanatory
    power* is weak: an architectural-bug interpretation cannot account
    for the *compensating mechanisms* (explicit rollback, Hansson
    postulates, literature backing) the system actually exhibits.
  - `claim_alt_just_graph_db` -- 0.3. The alternative's *explanatory
    power* is weak: a "just a graph DB" interpretation cannot account
    for zero-extra-primitives, cross-domain operations, and emergent
    AGM correspondence.
  - `pred_*` predictions -- 0.5 each (the comparison strategy plus the
    observation carry the signal).
* **Foils for contradiction operators**:
  - `claim_separate_layers_assumption` -- 0.5. The contradiction
    operator does the BP work, not the prior.
"""

from .motivation import (
    claim_agent_outputs_accumulate,
    claim_separate_layers_assumption,
)
from .s2_related_work import (
    claim_agm_lineage,
    claim_agm_ml_correspondences,
    claim_attention_not_recall,
    claim_benchmark_standardization_caveat,
    claim_bm25_history,
    claim_combmax_caveat,
    claim_flouris_dl_impossibility,
    claim_gcc_text_versioning,
    claim_model_coupling,
    claim_no_structural_representation,
    claim_observability_gap,
    claim_quadratic_cost_scaling,
    claim_recovery_critiques,
    claim_table1_comparison,
    claim_versioned_kg_lineage,
)
from .s3_structural_primitives import (
    claim_atomic_writes,
    claim_decoupling_mcp,
    claim_decoupling_pluggable_llm,
    claim_p10_conservative_consolidation,
    claim_p2_match_storage_latency,
    claim_p3_universal_addressability,
    claim_p5_immutable_revisions,
    claim_p6_metadata_over_content,
    claim_p7_explicit_relationships,
    claim_p8_graph_native_advantage,
    claim_p9_non_blocking_enhancement,
    claim_table10_seven_principles,
)
from .s4_correspondence_thesis import (
    claim_dual_purpose_graph,
    claim_governance_native,
    claim_governance_via_same_graph,
)
from .s5_agm_correspondence import (
    claim_complexity_bounds,
    claim_k7k8_representation_gap,
    claim_lg_satisfies_agm_prereqs,
)
from .s6_revision_semantics import (
    claim_cwa_classical_negation_duality,
    claim_deprecated_filter_architectural,
    claim_partial_merge_atomic_replacement,
    claim_partial_merge_finer_atomicity,
    claim_partial_merge_semantic_future,
    claim_property_graph_not_rdf,
    claim_superseded_not_excluded,
)
from .s7_kumiho_architecture import (
    claim_coverage_complementarity,
    claim_mcp_breadth_distinguisher,
)
from .s8_evaluation import (
    claim_benchmark_construction_caveat,
    claim_independent_reproduction,
    claim_limit_cross_system_methodology,
    claim_limit_eval_scope_complementarity,
    claim_limit_scale,
    claim_limit_self_eval_bias,
    claim_limit_system_performance,
    claim_locomo_plus_cost,
    claim_locomo_plus_table16_by_type,
    claim_locomo_plus_table17_time_gap,
    claim_token_compression_table,
)
from .s9_use_cases import claim_multi_channel_session_identity
from .s11_wiring import (
    claim_alt_just_graph_db,
    claim_recovery_alt_arch_bug,
    pred_arch_bug_explains,
    pred_extra_features,
    pred_immutable_explains,
    pred_isomorphism,
)


PRIORS: dict = {
    # ---- Architectural premises (production system facts) ----
    claim_agent_outputs_accumulate: (
        0.93,
        "Empirical observation about agent-output accumulation; supported by "
        "the multi-agent creative-pipeline use case and the VFX origin "
        "footnote. Modest discount for the framing being interpretive.",
    ),
    claim_atomic_writes: (
        0.95,
        "Architectural assertion: one MCP call creates the complete memory "
        "unit. Definitional / verifiable from the SDK.",
    ),
    claim_decoupling_mcp: (
        0.95,
        "MCP-based decoupling is a verifiable design: any MCP-compatible "
        "agent can use Kumiho via the same interface.",
    ),
    claim_decoupling_pluggable_llm: (
        0.94,
        "Pluggable adapter interface for LLM components is a verifiable "
        "implementation property.",
    ),
    claim_dual_purpose_graph: (
        0.93,
        "Dual-purpose-graph design is the central architectural assertion; "
        "concrete pipeline scenarios in Sec. 4.3 + Sec. 14 dashboard show "
        "this in practice.",
    ),
    claim_governance_native: (
        0.92,
        "Native governance (URI + revision history + provenance edges + "
        "audit trail) is a structural property of the architecture.",
    ),
    claim_governance_via_same_graph: (
        0.93,
        "Same-graph governance + coordination is a verifiable architectural "
        "property; the dashboard renders the same hierarchy used by agents.",
    ),
    claim_separate_layers_assumption: (
        0.5,
        "Foil for the contradiction operator -- BP does the work; prior is "
        "uninformative by design.",
    ),

    # ---- Seven core design principles (P1-P10) ----
    claim_p2_match_storage_latency: (
        0.94,
        "Latency-matching principle: 2-5ms library SDK vs 150-300ms HTTP "
        "is empirically measurable; principle is well-established.",
    ),
    claim_p3_universal_addressability: (
        0.95,
        "Universal addressability via stable URIs is a definitional "
        "principle; the kref:// scheme realizes it concretely.",
    ),
    claim_p5_immutable_revisions: (
        0.96,
        "Immutable revisions + mutable tag pointers is the foundational "
        "structural principle; concrete in the Item-Revision model.",
    ),
    claim_p6_metadata_over_content: (
        0.95,
        "Metadata-over-content / BYO-storage is a verifiable architectural "
        "commitment; the system never copies, caches, or proxies artifact "
        "content.",
    ),
    claim_p7_explicit_relationships: (
        0.94,
        "Explicit-over-inferred-relationships principle is realized as the "
        "6 typed-edge ontology; well-grounded in graph-database tradition.",
    ),
    claim_p8_graph_native_advantage: (
        0.94,
        "Graph-native O(1) traversal vs. relational multi-join is a "
        "well-established complexity-theoretic property.",
    ),
    claim_p9_non_blocking_enhancement: (
        0.94,
        "Non-blocking-enhancement principle is verifiable from the system: "
        "embeddings are async, fire-and-forget.",
    ),
    claim_p10_conservative_consolidation: (
        0.95,
        "Conservative-consolidation principle is realized through circuit "
        "breakers, dry-runs, and protection tags; architecturally enforced.",
    ),
    claim_table10_seven_principles: (
        0.95,
        "Table 10 catalogues the seven principles; this is a "
        "definitional / consolidation claim about the design.",
    ),

    # ---- Logic and AGM background (well-established mathematical facts) ----
    claim_lg_satisfies_agm_prereqs: (
        0.97,
        "L_G is a fragment of classical propositional logic; the Tarskian "
        "properties (inclusion, monotonicity, idempotence, deduction "
        "theorem, compactness) are textbook results [@Gardenfors1988]. "
        "Very high prior.",
    ),
    claim_agm_lineage: (
        0.97,
        "AGM framework [@AGM1985] + Hansson's belief-base extension "
        "[@Hansson1999Textbook] are well-established theoretical "
        "foundations; high prior.",
    ),
    claim_recovery_critiques: (
        0.95,
        "Recovery critiques by Makinson [@Makinson1987Recovery], Hansson "
        "[@Hansson1991NoRecovery], Fuhrmann [@Fuhrmann1991] are published "
        "and widely cited; high prior.",
    ),
    claim_flouris_dl_impossibility: (
        0.95,
        "Flouris et al. [@Flouris2005DL] DL impossibility is a published, "
        "widely-cited result; high prior.",
    ),
    claim_agm_ml_correspondences: (
        0.92,
        "Recent AGM-ML correspondences [@Aravanis2025; @Hase2024ModelEditing; "
        "@WilieEMNLP2024BeliefR] are published; the framing is interpretive "
        "but well-supported.",
    ),
    claim_versioned_kg_lineage: (
        0.94,
        "Versioned-KG lineage (R&Wbase, SemVersion, Quit Store, OSTRICH, "
        "ConVer-G) is well-documented; the historical claim is verifiable.",
    ),
    claim_gcc_text_versioning: (
        0.92,
        "GCC [@GCC2025] applies Git semantics to LLM-agent text-file memory; "
        "verifiable from the GCC paper.",
    ),
    claim_bm25_history: (
        0.95,
        "BM25 [@RobertsonZaragoza2009BM25] + RRF [@Cormack2009RRF] + fusion "
        "literature [@Bruch2023Fusion; @FoxShaw1993] are well-established.",
    ),

    # ---- Context-extension deficiencies ----
    claim_attention_not_recall: (
        0.95,
        "Attention != recall is a structural distinction; well-grounded in "
        "cognitive-science foundations [@AtkinsonShiffrin1968].",
    ),
    claim_quadratic_cost_scaling: (
        0.97,
        "Transformer attention's $\\Theta(n^2 \\cdot d)$ scaling is a "
        "textbook complexity-theoretic result [@Vaswani2017Attention].",
    ),
    claim_no_structural_representation: (
        0.95,
        "Token sequences cannot express belief revision / dependencies / "
        "validation states -- structural fact about flat token sequences.",
    ),
    claim_model_coupling: (
        0.94,
        "Context-window contents are model-specific and ephemeral -- "
        "definitional fact about how prompts work.",
    ),

    # ---- Cross-system tables ----
    claim_table1_comparison: (
        0.93,
        "Table 1 compares 6 axes across Graphiti/Mem0/Letta/Hindsight/Kumiho; "
        "modest discount for characterizations of competing systems.",
    ),

    # ---- Limitations (author-acknowledged caveats) ----
    claim_limit_scale: (
        0.93,
        "Scale tested at 200K nodes; tens-of-millions adversarial regime "
        "untested -- author-acknowledged limit, high prior.",
    ),
    claim_limit_cross_system_methodology: (
        0.94,
        "Cross-system numbers from publications, not controlled re-evaluation -- "
        "openly acknowledged.",
    ),
    claim_limit_eval_scope_complementarity: (
        0.94,
        "LoCoMo + AGM-suite are complementary; integrated belief-revision-"
        "correctness benchmark missing -- openly acknowledged.",
    ),
    claim_limit_self_eval_bias: (
        0.93,
        "Self-evaluation bias openly acknowledged with mitigation strategy.",
    ),
    claim_limit_system_performance: (
        0.93,
        "Latency distributions, throughput, per-belief overhead unreported -- "
        "openly acknowledged.",
    ),

    # ---- Empirical observations (tables and headlines) ----
    claim_token_compression_table: (
        0.94,
        "Table 11 token compression ratios (40x-280x) are direct measurements "
        "from the deployed graph; modest discount for sample-size variation.",
    ),
    claim_locomo_plus_table16_by_type: (
        0.93,
        "Table 16 per-type breakdown -- direct measurements (n=401); modest "
        "discount for non-deterministic LLM behavior in 4o-mini estimates.",
    ),
    claim_locomo_plus_table17_time_gap: (
        0.93,
        "Table 17 time-gap accuracy -- direct measurements; the >6-month cliff "
        "elimination (37.5% -> 84.4%) is a single-experiment observation, "
        "modest discount.",
    ),
    claim_locomo_plus_cost: (
        0.92,
        "~$14 cost is a direct measurement reported component-by-component.",
    ),
    claim_independent_reproduction: (
        0.93,
        "Independent reproduction by LoCoMo-Plus authors is external "
        "verification; reduces self-eval bias concern.",
    ),
    claim_benchmark_standardization_caveat: (
        0.95,
        "Caveat that no standardized LoCoMo leaderboard exists is a "
        "well-documented fact about the benchmark landscape.",
    ),
    claim_benchmark_construction_caveat: (
        0.92,
        "Benchmark-construction caveat (LoCoMo-Plus LLM-assisted "
        "generation) is openly acknowledged; modest discount for the "
        "interpretive framing.",
    ),
    claim_combmax_caveat: (
        0.94,
        "CombMAX susceptibility to score-inflation noise is published "
        "[@Bruch2023Fusion]; well-grounded.",
    ),

    # ---- Architectural sub-claims that are not headlines but ground other claims ----
    claim_observability_gap: (
        0.92,
        "Existing observability tools (OpenTelemetry, Langfuse, etc.) trace "
        "inference, not memory -- a verifiable architectural distinction.",
    ),
    claim_complexity_bounds: (
        0.92,
        "Per-operation complexity bounds are derived from operator "
        "definitions; deployment numbers (b ~ 3-5, traversals < 100ms) are "
        "measured.",
    ),
    claim_coverage_complementarity: (
        0.9,
        "Coverage complementarity is a design-level observation backed by "
        "concrete witness scenarios; modest discount for the qualitative "
        "framing.",
    ),
    claim_property_graph_not_rdf: (
        0.95,
        "Property-graph != RDF is a definitional distinction; the "
        "$(s,p,o)$ formalism is an analytical abstraction.",
    ),
    claim_deprecated_filter_architectural: (
        0.95,
        "WHERE NOT item.deprecated Cypher filter is an architectural "
        "guarantee at the database layer.",
    ),
    claim_superseded_not_excluded: (
        0.94,
        "Superseded != deprecated: superseded revisions remain retrievable "
        "via active tags -- definitional design choice.",
    ),
    claim_cwa_classical_negation_duality: (
        0.93,
        "CWA / classical-negation duality follows the ASP tradition "
        "[@GelfondLifschitz1988; @GelfondLifschitz1991]; well-grounded.",
    ),
    claim_partial_merge_atomic_replacement: (
        0.94,
        "Atomic replacement is the default partial-merge strategy; "
        "verifiable from the operator implementation.",
    ),
    claim_partial_merge_finer_atomicity: (
        0.92,
        "Finer-grained atomicity is a deployment configuration option; "
        "design-level claim about the operator's flexibility.",
    ),
    claim_partial_merge_semantic_future: (
        0.9,
        "Semantic merge as future work is a design-direction claim; "
        "high confidence in the identification, modest discount for "
        "future-work uncertainty.",
    ),
    claim_k7k8_representation_gap: (
        0.95,
        "K*7/K*8 representation-theoretic gap is openly acknowledged "
        "with explicit reference to Grove [@Grove1988]; high prior.",
    ),
    claim_mcp_breadth_distinguisher: (
        0.92,
        "MCP-tool breadth as the distinguisher is a verifiable claim "
        "(other MCP servers don't expose AnalyzeImpact / FindPath / "
        "GetProvenance).",
    ),
    claim_multi_channel_session_identity: (
        0.93,
        "User-centric session ID format is a verifiable design choice.",
    ),

    # ---- Abduction-1: structural-correspondence isomorphism ----
    claim_alt_just_graph_db: (
        0.3,
        "Alt's explanatory power is weak: a 'just a graph DB' interpretation "
        "cannot account for zero-extra-primitives, cross-domain operations, "
        "and the emergent AGM correspondence the architecture exhibits. "
        "Low pi(Alt) reflects explanatory power, NOT 'is the alt's "
        "calculation correct?'.",
    ),
    pred_isomorphism: (
        0.5,
        "Prediction; comparison strategy + observation carry the signal.",
    ),
    pred_extra_features: (
        0.5,
        "Prediction; comparison strategy + observation carry the signal.",
    ),

    # ---- Abduction-2: Recovery-rejection principled vs architectural-bug ----
    claim_recovery_alt_arch_bug: (
        0.25,
        "Alt's explanatory power is weak: an architectural-bug interpretation "
        "cannot account for the *compensating mechanisms* (explicit rollback, "
        "Hansson's Relevance + Core-Retainment, literature backing from "
        "Makinson/Hansson/Fuhrmann) the system exhibits. Low pi(Alt) reflects "
        "explanatory power.",
    ),
    pred_immutable_explains: (
        0.5,
        "Prediction; comparison strategy + observation carry the signal.",
    ),
    pred_arch_bug_explains: (
        0.5,
        "Prediction; comparison strategy + observation carry the signal.",
    ),
}
