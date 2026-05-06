"""Pass 2 wiring: strategies, abductions, inductions, contradictions for the
Park (2026) Kumiho formalization.

Conventions:

* `support` -- soft deduction with author-specified prior. The default for
  "premises imply conclusion" with empirical or interpretive uncertainty.
* `deduction` -- rigid logical entailment (definitional / structural). Used
  heavily here because most AGM postulates follow *deductively* from the
  graph-native operator definitions plus the L_G logic prerequisites -- the
  proofs in Section 7 are propositional-level definitional entailments.
* `compare` -- two predictions vs an observation; sub-strategy of `abduction`.
* `abduction` -- inference to best explanation. Used for the central
  *structural-correspondence insight* (memory primitives = asset-management
  primitives) and for the recovery-rejection alternative.
* `induction` -- chained binary composite. Used twice:
    (i) the cross-baseline architectural-synthesis gap (no concurrent system
        covers all four axes) inducted over Graphiti, Mem0, Letta, A-MEM,
        MAGMA, Hindsight, MemOS;
    (ii) the architectural generalization across LoCoMo + LoCoMo-Plus
        (same prospective indexing / event extraction / LLM reranking
        improvements drive both benchmarks).
* `contradiction` -- the prevailing-separate-layers view vs Kumiho's
  unified-graph demonstration; also the Kumiho-vs-MAGMA philosophical
  commitment (unified property graph vs multi-graph separation).
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
    claim_agent_outputs_accumulate,
    claim_agm_compliance_headline,
    claim_agm_correspondence_thesis,
    claim_components_exist,
    claim_context_extension_not_memory,
    claim_headline_contribution,
    claim_locomo_headline,
    claim_locomo_plus_headline,
    claim_separate_layers_assumption,
    claim_structural_correspondence,
    claim_synthesis_underexplored,
    claim_unified_thesis,
    setup_agentic_regime,
    setup_belief_base_level,
    setup_two_requirements,
)
from .s2_related_work import (
    claim_agm_lineage,
    claim_amem_components,
    claim_attention_not_recall,
    claim_benchmark_standardization_caveat,
    claim_bm25_history,
    claim_combmax_caveat,
    claim_flouris_dl_impossibility,
    claim_gcc_text_versioning,
    claim_graphiti_components,
    claim_hindsight_components,
    claim_letta_components,
    claim_magma_components,
    claim_mem0_components,
    claim_memos_components,
    claim_model_coupling,
    claim_no_structural_representation,
    claim_observability_gap,
    claim_quadratic_cost_scaling,
    claim_recovery_critiques,
    claim_table1_comparison,
    claim_versioned_kg_lineage,
    setup_human_memory_template,
    setup_locomo_benchmark,
    setup_locomo_plus_benchmark,
)
from .s3_structural_primitives import (
    claim_atomic_writes,
    claim_decoupling_mcp,
    claim_decoupling_pluggable_llm,
    claim_decoupling_storage,
    claim_p1_structural_reuse,
    claim_p10_conservative_consolidation,
    claim_p2_match_storage_latency,
    claim_p3_universal_addressability,
    claim_p5_immutable_revisions,
    claim_p6_metadata_over_content,
    claim_p7_explicit_relationships,
    claim_p8_graph_native_advantage,
    claim_p9_non_blocking_enhancement,
    claim_table10_seven_principles,
    setup_dual_store_model,
    setup_item_revision_model,
    setup_kref_uri_scheme,
    setup_memory_type_taxonomy,
    setup_neo4j_substrate,
    setup_six_edge_types,
)
from .s4_correspondence_thesis import (
    claim_cross_baseline_synthesis_gap,
    claim_dual_purpose_graph,
    claim_governance_native,
    claim_governance_via_same_graph,
    claim_table8_comparative_dimensions,
    claim_table9_feature_comparison,
    claim_vs_flat_retrieval,
    claim_vs_hindsight_complementary,
    claim_vs_magma_unified_vs_multi,
    claim_vs_static_kg,
    claim_vs_tiered_buffers,
)
from .s5_agm_correspondence import (
    claim_k2_success,
    claim_k3_inclusion_base_version,
    claim_k4_vacuity,
    claim_k5_consistency,
    claim_k6_extensionality,
    claim_k7_superexpansion_argued,
    claim_k7k8_representation_gap,
    claim_k8_subexpansion_argued,
    claim_lg_satisfies_agm_prereqs,
    claim_complexity_bounds,
    claim_core_retainment_hansson,
    claim_expressiveness_tradeoff,
    claim_flouris_avoidance,
    claim_harper_identity,
    claim_iterated_revision_supersedes,
    claim_levi_identity,
    claim_recovery_rejection_principled,
    claim_recovery_violation,
    claim_relevance_hansson,
    claim_table4_postulate_summary,
    claim_worked_example_preference,
    setup_def_belief_base,
    setup_def_contraction_op,
    setup_def_expansion_op,
    setup_def_lg_logic,
    setup_def_memory_graph,
    setup_def_revision_op,
    setup_def_selection_function,
    setup_def_two_tier,
    setup_satisfaction_system,
)
from .s6_revision_semantics import (
    claim_asymmetric_bridge,
    claim_compound_input_two_strategies,
    claim_conflict_presentation,
    claim_cwa_classical_negation_duality,
    claim_deprecated_filter_architectural,
    claim_formal_robustness_to_subsymbolic,
    claim_nl_mapping_scope_limit,
    claim_nl_to_triple_boundary,
    claim_partial_merge_atomic_replacement,
    claim_partial_merge_finer_atomicity,
    claim_partial_merge_semantic_future,
    claim_postulate_scope,
    claim_property_graph_not_rdf,
    claim_superseded_not_excluded,
    setup_symbolic_subsymbolic_division,
)
from .s7_kumiho_architecture import (
    claim_byo_storage_benefits,
    claim_client_side_reranking,
    claim_combmax_design_choice,
    claim_consolidation_formal_status,
    claim_coverage_complementarity,
    claim_dream_state_safety_guards,
    claim_human_audit_dashboard,
    claim_mcp_51_tools,
    claim_mcp_breadth_distinguisher,
    claim_precision_preservation,
    claim_recall_non_degradation,
    claim_reference_implementation,
    claim_threat_model,
    setup_dream_state_pipeline,
    setup_hybrid_pipeline,
    setup_privacy_boundary,
)
from .s8_evaluation import (
    claim_adversarial_refusal_natural,
    claim_agm_compliance_table18,
    claim_belief_revision_in_practice,
    claim_benchmark_construction_caveat,
    claim_cross_session_provenance_paper,
    claim_dream_state_deployment_validation,
    claim_independent_reproduction,
    claim_limit_lg_expressiveness,
    claim_limit_cross_system_methodology,
    claim_limit_dream_state_llm_dependency,
    claim_limit_eval_scope_complementarity,
    claim_limit_formal_scope,
    claim_limit_scale,
    claim_limit_self_eval_bias,
    claim_limit_system_performance,
    claim_locomo_plus_cost,
    claim_locomo_plus_recall_98_5,
    claim_locomo_plus_table15_baselines,
    claim_locomo_plus_table16_by_type,
    claim_locomo_plus_table17_time_gap,
    claim_locomo_table12_cross_system,
    claim_locomo_table13_per_category,
    claim_model_decoupled_validation,
    claim_token_compression_table,
    setup_locomo_eval_config,
    setup_locomo_plus_config,
)
from .s9_use_cases import (
    claim_coding_agent_use_case,
    claim_decision_auditability_use_case,
    claim_letta_concrete_example,
    claim_multi_agent_creative_pipeline,
    claim_multi_channel_session_identity,
    claim_vfx_pipeline_origin,
)
from .s10_discussion_limitations import (
    claim_conclusion_unification,
)

# ===========================================================================
# 1. AGM postulate satisfaction -- DEDUCTIONS from operator definitions + L_G
# ===========================================================================
# Each postulate proof in Section 7 reduces propositionally, given the
# definitional setup. We use `deduction` because the proofs are definitional/
# structural at the L_G level, not empirical inferences.

deduction_K2_from_revision_def = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_k2_success,
    reason=(
        "**K*2 (Success).** From the revision operator's definition (@setup_def_revision_op): "
        "the new revision r_i^(k+1) is constructed with phi(r_i^(k+1)) = A, "
        "and the tag t_current is updated to point to r_i^(k+1) (@setup_def_belief_base). "
        "Since the belief base is the union of tag-referenced revision contents, "
        "A in B(tau'). The L_G logic (@claim_lg_satisfies_agm_prereqs) provides "
        "the propositional substrate over which the postulate is well-formed. "
        "Proof in [@Park2026Kumiho, Prop. 7.1]."
    ),
    prior=0.99,
    background=[setup_def_revision_op, setup_def_belief_base],
)

deduction_K3_from_revision_def = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_k3_inclusion_base_version,
    reason=(
        "**K*3 (Inclusion, base version).** Hansson's belief-base "
        "[@Hansson1999Textbook] formulation requires B * A subseteq B union {A} "
        "rather than the stronger AGM K*A subseteq Cn(K union {A}). The base "
        "version follows from the revision operator (@setup_def_revision_op): "
        "creating a new revision containing A (or content set entailing A) and "
        "redirecting tags removes some prior beliefs from B(tau) but introduces "
        "no atoms outside B(tau) union {A}. The L_G logic prerequisites "
        "(@claim_lg_satisfies_agm_prereqs) ensure the postulate is well-formed "
        "at the propositional level. Proof in [@Park2026Kumiho, Prop. 7.2]."
    ),
    prior=0.99,
    background=[setup_def_revision_op, setup_def_belief_base, setup_belief_base_level],
)

deduction_K4_from_revision_def = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_k4_vacuity,
    reason=(
        "**K*4 (Vacuity).** From the revision operator definition "
        "(@setup_def_revision_op), if A introduces no contradiction relative to "
        "the existing tagged content, no tag needs redirection, the prior content "
        "is preserved, and only A is augmented. The L_G consequence operator "
        "(@claim_lg_satisfies_agm_prereqs) is the standard propositional Cn, so "
        "consistency-with-prior is well-defined. Proof in "
        "[@Park2026Kumiho, Prop. 7.3]."
    ),
    prior=0.99,
    background=[setup_def_revision_op],
)

deduction_K5_from_supersedes = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_k5_consistency,
    reason=(
        "**K*5 (Consistency).** The revision operator (@setup_def_revision_op) "
        "*replaces* the tag pointer rather than accumulating contradictory "
        "content -- the prior revision is excluded from B(tau') via the two-tier "
        "epistemic model (@setup_def_two_tier). For atomic revision inputs in "
        "At_G, distinct ground atoms are propositionally independent under the "
        "L_G semantics (@setup_def_lg_logic; @claim_lg_satisfies_agm_prereqs), "
        "guaranteeing consistency structurally. Proof in "
        "[@Park2026Kumiho, Prop. 7.4]."
    ),
    prior=0.99,
    background=[setup_def_revision_op, setup_def_two_tier, setup_def_lg_logic],
)

deduction_K6_from_LG_atoms = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_k6_extensionality,
    reason=(
        "**K*6 (Extensionality).** Since the belief base B(tau) consists of "
        "ground atoms from At_G (@setup_def_belief_base; @setup_def_lg_logic) "
        "and ground atoms in the L_G fragment are propositionally independent "
        "(@claim_lg_satisfies_agm_prereqs: classical propositional logic over "
        "atomic ground triples), Cn_G({alpha}) = Cn_G({beta}) iff alpha = beta "
        "(syntactic identity). Item-level identity checking is therefore an "
        "exact implementation, not an approximation, for the atomic case. "
        "Proof in [@Park2026Kumiho, Prop. 7.5]."
    ),
    prior=0.99,
    background=[setup_def_belief_base, setup_def_lg_logic],
)

deduction_relevance_from_selection = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_relevance_hansson,
    reason=(
        "**Relevance (Hansson).** Contraction (@setup_def_contraction_op) removes "
        "from B(tau) exactly those beliefs residing in revisions whose content "
        "contains A, via the content-based selection function "
        "(@setup_def_selection_function). The witness construction (Case 1: "
        "B = A => B' = empty; Case 2: B != A but co-occurs => B' = "
        "B(tau) \\ phi(r)) follows propositionally from the L_G machinery "
        "(@claim_lg_satisfies_agm_prereqs). Proof in "
        "[@Park2026Kumiho, Prop. 7.6]."
    ),
    prior=0.99,
    background=[setup_def_contraction_op, setup_def_selection_function],
)

deduction_core_retainment_from_selection = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_core_retainment_hansson,
    reason=(
        "**Core-Retainment (Hansson).** Symmetric to Relevance: every removed "
        "belief contributed to deriving A's presence in the contracted revision. "
        "Witness via @setup_def_selection_function. The belief-base setting "
        "(@setup_belief_base_level) is essential: for deductively closed sets "
        "Core-Retainment implies Recovery, but for belief bases (which B(tau) "
        "always is) it does not, so simultaneous satisfaction of "
        "Core-Retainment and rejection of Recovery is consistent. Proof in "
        "[@Park2026Kumiho, Prop. 7.7]."
    ),
    prior=0.99,
    background=[setup_def_contraction_op, setup_def_selection_function],
)

# K*7 / K*8: argued, not formally established -- support, not deduction
support_K7_argued = support(
    [claim_lg_satisfies_agm_prereqs, claim_compound_input_two_strategies],
    claim_k7_superexpansion_argued,
    reason=(
        "**K*7 (Superexpansion, argued).** Conjunction A wedge B is well-formed "
        "in L_G (@claim_lg_satisfies_agm_prereqs: closure under standard "
        "connectives). Revising by (A wedge B) creates a single revision whose "
        "content entails both A and B. Sequential decomposition "
        "(@claim_compound_input_two_strategies) -- revise by A then expand by B -- "
        "is monotone and contains both A and B. The conjunction revision cannot "
        "contain more, since it may also retract beliefs inconsistent with "
        "A wedge B. **Status: argued only**: a formal proof requires "
        "construction of an entrenchment ordering "
        "(@claim_k7k8_representation_gap)."
    ),
    prior=0.7,
)

support_K8_argued = support(
    [claim_lg_satisfies_agm_prereqs, claim_compound_input_two_strategies],
    claim_k8_subexpansion_argued,
    reason=(
        "**K*8 (Subexpansion, argued).** If B is consistent with the A-revised "
        "state (the postulate's antecedent), expanding by B adds no information "
        "beyond B and its consequences. Revising by A wedge B directly "
        "incorporates both conjuncts. Both paths yield equivalent retractions "
        "and the same final content. **Status: argued only**: a formal proof "
        "requires the entrenchment ordering identified in "
        "@claim_k7k8_representation_gap."
    ),
    prior=0.7,
)

# Recovery rejection: deductive consequence of Definition 7.4 (revision creates
# fresh content-A revision; co-located beliefs are not auto-restored)
deduction_recovery_violation = deduction(
    [claim_lg_satisfies_agm_prereqs],
    claim_recovery_violation,
    reason=(
        "**Recovery violation.** The revision operator (@setup_def_revision_op) "
        "constructs a new revision r_i^(k+1) with phi(r_i^(k+1)) = {A}, "
        "supersedes r_i^(k) carrying {A, B, C}, and re-points the tag. After "
        "contracting A then re-expanding by A, B and C are NOT in the resulting "
        "tagged content because the new revision is constructed from input A "
        "alone. The L_G semantics (@claim_lg_satisfies_agm_prereqs) confirms "
        "that the union (B div A) cup {A} does not include {B, C}. Proof in "
        "[@Park2026Kumiho, Sec. 7.3]."
    ),
    prior=0.99,
    background=[setup_def_revision_op, setup_def_contraction_op],
)

# Postulate-summary table is supported by all postulate derivations
support_table4_summary = support(
    [
        claim_k2_success,
        claim_k3_inclusion_base_version,
        claim_k4_vacuity,
        claim_k5_consistency,
        claim_k6_extensionality,
        claim_relevance_hansson,
        claim_core_retainment_hansson,
        claim_k7_superexpansion_argued,
        claim_k8_subexpansion_argued,
        claim_recovery_violation,
    ],
    claim_table4_postulate_summary,
    reason=(
        "**Table 4 (postulate satisfaction summary).** The summary table "
        "[@Park2026Kumiho, Table 4] aggregates the per-postulate proofs "
        "established in Propositions 7.1-7.9: K*2 (@claim_k2_success), K*3 "
        "(@claim_k3_inclusion_base_version), K*4 (@claim_k4_vacuity), K*5 "
        "(@claim_k5_consistency), K*6 (@claim_k6_extensionality), Relevance "
        "(@claim_relevance_hansson), Core-Retainment (@claim_core_retainment_hansson), "
        "K*7 (@claim_k7_superexpansion_argued, argued only), K*8 "
        "(@claim_k8_subexpansion_argued, argued only), Recovery "
        "(@claim_recovery_violation, intentionally rejected)."
    ),
    prior=0.97,
)

# ===========================================================================
# 2. Flouris avoidance -- L_G prerequisites + DL-style structural absence
# ===========================================================================

# Prop 7.10 about L_G satisfying AGM prerequisites is left as an
# *independent leaf claim*: it is a well-established mathematical property
# of classical propositional logic (a Tarskian logic satisfying all five
# AGM prerequisites). Setting it as a leaf with high prior is the right
# encoding -- there is no derivation in the paper, only a citation.

support_flouris_avoided = support(
    [claim_lg_satisfies_agm_prereqs, claim_flouris_dl_impossibility],
    claim_flouris_avoidance,
    reason=(
        "**Flouris avoidance.** The Flouris et al. impossibility "
        "(@claim_flouris_dl_impossibility) [@Flouris2005DL] applies to "
        "Description Logics with TBox/ABox separation, open-world assumption, "
        "and complex constructors (concept disjunction, existential "
        "quantification, role inverses, number restrictions). L_G "
        "(@setup_def_lg_logic) has none of these: a single flat layer, formal "
        "negation paired with closed-world operational semantics, and simple "
        "labeled directed edges. Combined with the AGM prerequisites of L_G "
        "(@claim_lg_satisfies_agm_prereqs), L_G meets the Flouris et al. "
        "necessary conditions for AGM-compliance, confirming the impossibility "
        "results do not apply to the property-graph formalism."
    ),
    prior=0.92,
)

support_expressiveness_tradeoff = support(
    [claim_flouris_avoidance, claim_k6_extensionality],
    claim_expressiveness_tradeoff,
    reason=(
        "**Expressiveness trade-off (deliberate).** The formal results hold "
        "precisely because L_G is a *weak* logic. Logical equivalence reduces "
        "to syntactic identity (@claim_k6_extensionality), and the Flouris "
        "impossibility is avoided (@claim_flouris_avoidance) precisely because "
        "L_G lacks the constructors that cause DLs to fail. The contribution "
        "is the **bridge** -- showing production-motivated architectural "
        "choices satisfy AGM postulates -- not 'AGM holds over a strong "
        "logic.' L_G explicitly cannot express subsumption hierarchies, role "
        "composition, disjointness axioms, or cardinality constraints "
        "[@Park2026Kumiho, Sec. 7.6 'Expressiveness trade-off']."
    ),
    prior=0.92,
)

# Levi and Harper identities follow from operator definitions
deduction_levi_identity = deduction(
    [claim_k2_success],
    claim_levi_identity,
    reason=(
        "**Levi identity K * A = (K div ~A) + A.** Holds when contraction is "
        "deterministic (@setup_def_selection_function), since contracting ~A "
        "removes revisions whose content entails ~A and the subsequent "
        "expansion adds a fresh A-revision; combined with K*2 Success "
        "(@claim_k2_success) the two-step process yields the same belief "
        "state as direct revision."
    ),
    prior=0.97,
    background=[setup_def_revision_op, setup_def_contraction_op, setup_def_expansion_op, setup_def_selection_function],
)

deduction_harper_identity = deduction(
    [claim_k5_consistency, claim_relevance_hansson],
    claim_harper_identity,
    reason=(
        "**Harper identity K div A = K cap (K * ~A).** A belief surviving "
        "contraction of A must be consistent with ~A (@claim_k5_consistency) "
        "and is therefore preserved in K * ~A; the graph intersection "
        "corresponds to the set of revisions that remain tag-referenced in "
        "both tau and tau'. Relevance (@claim_relevance_hansson) ensures the "
        "selection is content-targeted."
    ),
    prior=0.97,
    background=[setup_def_revision_op, setup_def_contraction_op],
)

support_iterated_revision = support(
    [claim_levi_identity, claim_harper_identity],
    claim_iterated_revision_supersedes,
    reason=(
        "**Iterated revision via Supersedes-chain.** The Supersedes edge "
        "chain provides a natural epistemic ordering matching Darwiche-Pearl "
        "[@DarwichePearl1997]; the time-indexed tag function tau_T elevates "
        "this to a fully queryable epistemic history. The Levi "
        "(@claim_levi_identity) and Harper (@claim_harper_identity) identities "
        "provide the operator-decomposition machinery DP assumes."
    ),
    prior=0.85,
)

# Complexity bounds are leaf observations from the operator definitions
# and deployment measurements; left as independent claim with prior in priors.py.

# ===========================================================================
# 3. Recovery rejection: ABDUCTION (immutable-versioning explanation vs.
#    text-erasure alternative)
# ===========================================================================

# Construct the abduction skeleton
recovery_violation_obs = claim_recovery_violation
recovery_immutable_explanation = claim_recovery_rejection_principled

# Alternative explanation: the violation is just an architectural bug
claim_recovery_alt_arch_bug = claim(
    "**Alternative: the Recovery violation is an architectural bug, not a "
    "principled choice.** A skeptic could argue that any system rejecting "
    "Recovery is simply broken AGM compliance -- the canonical AGM postulates "
    "include Recovery, and rejecting it makes the system non-AGM-compliant.",
    title="Alt: Recovery violation is a bug, not a principled choice",
)

pred_immutable_explains = claim(
    "**Prediction (H = immutable versioning is principled).** A system that "
    "archives rather than erases content during contraction will (i) preserve "
    "co-located beliefs in graph history, (ii) provide explicit rollback via "
    "tag reassignment, and (iii) satisfy Hansson's Relevance + Core-Retainment "
    "(which replace Recovery in belief-base frameworks).",
    title="Pred-H: principled rejection => archive + explicit rollback + Hansson-postulate compliance",
)

pred_arch_bug_explains = claim(
    "**Prediction (Alt = architectural bug).** A system whose Recovery violation "
    "stems from an oversight would lack (i) explicit rollback mechanisms, (ii) "
    "compensating Hansson postulates, and (iii) literature backing -- the "
    "violation would simply be incomplete AGM coverage.",
    title="Pred-Alt: architectural-bug interpretation => no rollback, no compensating postulates",
)

s_recovery_h = support(
    [recovery_immutable_explanation, claim_p5_immutable_revisions],
    recovery_violation_obs,
    reason=(
        "**H supports the violation observation.** The principled-rejection "
        "explanation (@claim_recovery_rejection_principled) grounded in the "
        "immutable-revision principle (@claim_p5_immutable_revisions) "
        "predicts that re-expansion is fresh incorporation rather than "
        "implicit reconstruction -- which is precisely what the operator "
        "produces (@claim_recovery_violation)."
    ),
    prior=0.93,
)

s_recovery_alt = support(
    [claim_recovery_alt_arch_bug],
    recovery_violation_obs,
    reason=(
        "**Alt could explain the violation.** Architecturally, an oversight "
        "would also produce a Recovery violation (the surface phenomenon is "
        "indistinguishable from a principled rejection at the operator "
        "level)."
    ),
    prior=0.5,
)

comp_recovery = compare(
    pred_immutable_explains,
    pred_arch_bug_explains,
    recovery_violation_obs,
    reason=(
        "**Comparison.** H predicts: (i) explicit rollback via tag "
        "reassignment (present, [@Park2026Kumiho, Sec. 7.3]), (ii) "
        "compensating Hansson postulates Relevance + Core-Retainment "
        "(satisfied, @claim_relevance_hansson, @claim_core_retainment_hansson), "
        "(iii) literature backing (Makinson, Hansson, Fuhrmann, "
        "@claim_recovery_critiques). Alt predicts none of these. H matches "
        "all three observable features; Alt matches none."
    ),
    prior=0.95,
)

abduction_recovery_principled = abduction(
    s_recovery_h,
    s_recovery_alt,
    comp_recovery,
    reason=(
        "**Recovery rejection is principled, not a bug.** Both explanations "
        "could in principle produce the Recovery violation phenomenon, but "
        "only the principled-rejection explanation predicts the "
        "*compensating mechanisms* the system actually exhibits: explicit "
        "rollback via tag reassignment, satisfaction of Hansson's belief-base "
        "postulates that replace Recovery, and alignment with Makinson / "
        "Hansson / Fuhrmann's published critiques."
    ),
)

# ===========================================================================
# 4. The structural-correspondence insight: ABDUCTION
# ===========================================================================
# Hypothesis: memory-primitives = asset-management-primitives is the unifying
# isomorphism that justifies the unified architecture.
# Alternative: Kumiho is just another graph DB with extra features.

claim_alt_just_graph_db = claim(
    "**Alternative: Kumiho is just another graph DB with extra features.** A "
    "skeptic could argue that the apparent unification is incidental: any "
    "sufficiently capable graph database (Neo4j, JanusGraph, Dgraph) plus an "
    "asset-management API would yield the same capabilities, and Kumiho's "
    "'unified primitive set' is just a marketing reframe of standard property-"
    "graph features.",
    title="Alt: Kumiho's unification is incidental; any graph DB + asset API would do",
)

pred_isomorphism = claim(
    "**Prediction (H = memory<->asset isomorphism is real).** If the "
    "isomorphism is genuine, the architecture should: (i) require ZERO "
    "additional primitives to manage agent work products beyond those needed "
    "for cognitive memory; (ii) enable cross-domain operations (e.g., the "
    "same `AnalyzeImpact` traversal works for both belief revision AND asset "
    "lineage); (iii) yield the formal correspondence with AGM as an emergent "
    "property of the same primitives that serve asset management.",
    title="Pred-H: genuine isomorphism => zero extra primitives + cross-domain ops + emergent AGM",
)

pred_extra_features = claim(
    "**Prediction (Alt = just a graph DB with extras).** If the unification "
    "is incidental, the architecture should: (i) require *separate* "
    "extension layers for cognitive memory and asset management; (ii) show "
    "incompatible operations across the two domains (e.g., asset-management "
    "edges that don't apply to memory or vice versa); (iii) lack any "
    "*formal* correspondence between memory operations and asset workflows.",
    title="Pred-Alt: incidental unification => separate layers, incompatible ops, no formal link",
)

obs_correspondence = claim_structural_correspondence

s_isomorphism = support(
    [claim_p1_structural_reuse, claim_unified_thesis, claim_dual_purpose_graph],
    obs_correspondence,
    reason=(
        "**H explains the observed structural correspondence.** The "
        "isomorphism hypothesis (@claim_p1_structural_reuse, "
        "@claim_unified_thesis, @claim_dual_purpose_graph) predicts that the "
        "*identical* primitive set serves both roles -- which is precisely "
        "what Table 2 (@claim_structural_correspondence) shows: each row "
        "matches an asset-management concept to a cognitive-memory concept "
        "with a shared structural concept."
    ),
    prior=0.92,
)

s_just_graph_db = support(
    [claim_alt_just_graph_db],
    obs_correspondence,
    reason=(
        "**Alt could explain superficial similarity.** A graph DB with "
        "added features could in principle produce a similar-looking "
        "table by labeling existing concepts with new domain names."
    ),
    prior=0.3,
)

comp_correspondence = compare(
    pred_isomorphism,
    pred_extra_features,
    obs_correspondence,
    reason=(
        "**Comparison.** H predicts (i) zero additional primitives "
        "(satisfied: Section 6 of [@Park2026Kumiho] uses the SAME edges, "
        "tags, items, revisions for memory and assets), (ii) cross-domain "
        "operations (satisfied: AnalyzeImpact works for both, "
        "@setup_six_edge_types), (iii) emergent AGM (satisfied: "
        "@claim_table4_postulate_summary). Alt predicts the opposite on all "
        "three counts; the actual architecture matches H, not Alt."
    ),
    prior=0.95,
)

abduction_structural_isomorphism = abduction(
    s_isomorphism,
    s_just_graph_db,
    comp_correspondence,
    reason=(
        "**The memory<->asset structural isomorphism is genuine.** Both "
        "explanations can describe the *appearance* of the correspondence "
        "table, but only the isomorphism hypothesis predicts (i) zero extra "
        "primitives, (ii) cross-domain operations sharing the same "
        "AnalyzeImpact / typed-edge machinery, and (iii) the AGM "
        "correspondence emerging from the same primitives. The architecture "
        "exhibits all three; the alternative would predict at least one to "
        "fail. This is the central architectural argument for the "
        "unification thesis."
    ),
)

# ===========================================================================
# 5. CONTRADICTIONS
# ===========================================================================

# Contradiction 1: separate-layers assumption vs. unified-graph thesis
contradiction_separate_vs_unified = contradiction(
    claim_separate_layers_assumption,
    claim_unified_thesis,
    reason=(
        "**Separate-layers assumption vs. unified-graph thesis.** The prevailing "
        "view treats memory and asset tracking as structurally distinct, "
        "demanding separate substrates (@claim_separate_layers_assumption). "
        "Kumiho's thesis demonstrates the opposite: ONE graph-native primitive "
        "set serves both (@claim_unified_thesis). These are not in tension -- "
        "they are formally incompatible: the unified-graph implementation "
        "exists and works, falsifying the separability claim."
    ),
    prior=0.98,
)

# Contradiction 2: Kumiho's unified-graph philosophy vs. MAGMA's multi-graph
# separation (architecturally exclusive design choices)
contradiction_unified_vs_multigraph = contradiction(
    claim_vs_magma_unified_vs_multi,
    claim_magma_components,
    reason=(
        "**Unified property graph vs. multi-graph separation.** Kumiho commits "
        "to one unified property graph with typed edges enabling cross-"
        "dimensional traversal and transactional atomicity "
        "(@claim_vs_magma_unified_vs_multi). MAGMA commits to four orthogonal "
        "graphs to disentangle dimensions (@claim_magma_components). These are "
        "architecturally exclusive design choices on the same artifact (one "
        "graph or many). They cannot both be the right answer for a given "
        "deployment; the empirical comparison is identified as the most "
        "important open question [@Park2026Kumiho, Sec. 12.5]."
    ),
    prior=0.9,
)

# ===========================================================================
# 6. INDUCTIONS
# ===========================================================================

# Induction 1: The cross-baseline architectural-synthesis gap
# Each system gap supports the law "no concurrent system covers all 4 axes"
ind_law = claim_cross_baseline_synthesis_gap

s_gap_graphiti = support(
    [ind_law],
    claim_graphiti_components,
    reason=(
        "**Law predicts Graphiti gap.** If no concurrent system covers all four "
        "axes (@claim_cross_baseline_synthesis_gap), then Graphiti -- a "
        "concurrent system -- should lack at least one. Observation: Graphiti "
        "lacks formal AGM, URI addressing, and BYO-storage "
        "(@claim_graphiti_components, [@Park2026Kumiho, Sec. 2.1])."
    ),
    prior=0.93,
)

s_gap_mem0 = support(
    [ind_law],
    claim_mem0_components,
    reason=(
        "**Law predicts Mem0 gap.** Observation: Mem0 lacks formal revision "
        "(@claim_mem0_components), confirming the law for this baseline."
    ),
    prior=0.93,
)

s_gap_letta = support(
    [ind_law],
    claim_letta_components,
    reason=(
        "**Law predicts Letta gap.** Observation: Letta has Git-backed "
        "versioning but lacks typed edges, AGM, and impact analysis "
        "(@claim_letta_components)."
    ),
    prior=0.93,
)

s_gap_amem = support(
    [ind_law],
    claim_amem_components,
    reason=(
        "**Law predicts A-MEM gap.** Observation: A-MEM has dynamic linking "
        "but no formalism or unified asset graph (@claim_amem_components)."
    ),
    prior=0.93,
)

s_gap_magma = support(
    [ind_law],
    claim_magma_components,
    reason=(
        "**Law predicts MAGMA gap.** Observation: MAGMA disentangles "
        "dimensions across separate graphs (@claim_magma_components), missing "
        "the unified-graph axis."
    ),
    prior=0.9,
)

s_gap_hindsight = support(
    [ind_law],
    claim_hindsight_components,
    reason=(
        "**Law predicts Hindsight gap.** Observation: Hindsight has empirical "
        "belief tracking but no AGM guarantees (@claim_hindsight_components)."
    ),
    prior=0.93,
)

s_gap_memos = support(
    [ind_law],
    claim_memos_components,
    reason=(
        "**Law predicts MemOS gap.** Observation: MemOS has tiered buffers "
        "with LLM-coupled memory management (@claim_memos_components)."
    ),
    prior=0.93,
)

induction_synthesis_gap_12 = induction(
    s_gap_graphiti, s_gap_mem0,
    law=ind_law,
    reason="Graphiti and Mem0 are independent systems; both confirm the gap."
)
induction_synthesis_gap_123 = induction(
    induction_synthesis_gap_12, s_gap_letta,
    law=ind_law,
    reason="Letta is independently developed by another team; gap confirmed."
)
induction_synthesis_gap_1234 = induction(
    induction_synthesis_gap_123, s_gap_amem,
    law=ind_law,
    reason="A-MEM (NeurIPS 2025) is independent; gap confirmed."
)
induction_synthesis_gap_12345 = induction(
    induction_synthesis_gap_1234, s_gap_magma,
    law=ind_law,
    reason="MAGMA (2026) explicitly chose multi-graph; this confirms the law on a different design philosophy."
)
induction_synthesis_gap_123456 = induction(
    induction_synthesis_gap_12345, s_gap_hindsight,
    law=ind_law,
    reason="Hindsight (2025) is empirically strong but lacks formalism; gap confirmed."
)
induction_synthesis_gap_full = induction(
    induction_synthesis_gap_123456, s_gap_memos,
    law=ind_law,
    reason="MemOS (EMNLP 2025 Oral) uses LLM-coupled tiered buffers; final confirmation across all 7 baselines."
)

# Induction 2: Architecture generalization across LoCoMo + LoCoMo-Plus
claim_arch_generalizes_law = claim(
    "**Architecture-generalization law.** Kumiho's three architectural "
    "innovations -- prospective indexing, event extraction, and client-side "
    "LLM reranking -- improve performance on multiple benchmarks with "
    "different scoring protocols, validating that the gains are properties "
    "of the architecture rather than benchmark-specific tuning "
    "[@Park2026Kumiho, Sec. 15.2 'Architecture generalization'; "
    "Sec. 15.3 'Architectural significance'].",
    title="Law: prospective indexing + event extraction + LLM reranking generalize across benchmarks",
)

s_law_locomo = support(
    [claim_arch_generalizes_law],
    claim_locomo_table13_per_category,
    reason=(
        "**Law predicts LoCoMo improvement.** If the three innovations "
        "(@claim_arch_generalizes_law) are general properties, Kumiho should "
        "lead on LoCoMo's official token-level F1 metric. Observation: "
        "0.447 four-category F1 (highest reported), with multi-hop F1 0.355 "
        "exceeding Mem0-Graph by +11.2pp -- precisely where graph-augmented "
        "recall provides structural advantage (@claim_locomo_table13_per_category)."
    ),
    prior=0.93,
)

s_law_locomo_plus = support(
    [claim_arch_generalizes_law],
    claim_locomo_plus_table15_baselines,
    reason=(
        "**Law predicts LoCoMo-Plus dominance.** If the three innovations "
        "generalize, they should also improve on LoCoMo-Plus's harder Level-2 "
        "implicit-constraint metric. Observation: 93.3% (47.6pp over the best "
        "baseline at 45.7%, @claim_locomo_plus_table15_baselines), with the "
        ">6mo cliff eliminated (37.5% -> 84.4%, "
        "@claim_locomo_plus_table17_time_gap)."
    ),
    prior=0.93,
)

induction_arch_generalizes = induction(
    s_law_locomo, s_law_locomo_plus,
    law=claim_arch_generalizes_law,
    reason=(
        "**LoCoMo and LoCoMo-Plus are independent benchmarks** with different "
        "scoring protocols (token-level F1 vs. LLM-judge accuracy), different "
        "question types (factual recall vs. implicit-constraint recall), and "
        "different baselines. The same three innovations (prospective "
        "indexing, event extraction, LLM reranking) improve both, supporting "
        "the architecture-generalization law."
    ),
)

# ===========================================================================
# 7. The unified thesis is supported by the structural correspondence and the
#    architectural-synthesis gap.
# ===========================================================================

support_unified_thesis = support(
    [claim_structural_correspondence, claim_cross_baseline_synthesis_gap],
    claim_unified_thesis,
    reason=(
        "**Unified thesis derivation.** Two independent lines support the "
        "unification thesis: (i) the **structural correspondence** "
        "(@claim_structural_correspondence) shows the same primitive set "
        "*can* serve both roles structurally (Table 2 of "
        "[@Park2026Kumiho]); (ii) the **cross-baseline architectural "
        "synthesis gap** (@claim_cross_baseline_synthesis_gap) shows that NO "
        "concurrent system has built such a unified architecture, leaving "
        "this design space unexplored. Together they motivate building ONE "
        "graph-native primitive set serving BOTH roles."
    ),
    prior=0.93,
)

# Support: P1 Structural Reuse principle is supported by the correspondence + thesis
support_p1_from_correspondence = support(
    [claim_structural_correspondence, claim_unified_thesis, claim_agent_outputs_accumulate],
    claim_p1_structural_reuse,
    reason=(
        "**P1 (Structural Reuse) is the design-principle distillation of the "
        "unification thesis.** The structural correspondence "
        "(@claim_structural_correspondence) shows the primitive sets are "
        "identical; the unification thesis (@claim_unified_thesis) commits "
        "to building ONE primitive set; the bottleneck observation "
        "(@claim_agent_outputs_accumulate) provides the empirical motivation."
    ),
    prior=0.95,
)

# Support: Table 2 of [@Park2026Kumiho] -- the structural correspondence claim
support_correspondence_from_setting = support(
    [claim_p5_immutable_revisions, claim_p3_universal_addressability, claim_p7_explicit_relationships],
    claim_structural_correspondence,
    reason=(
        "**Table 2 follows from the design principles.** Immutable revisions "
        "(@claim_p5_immutable_revisions) match Snapshot in both columns; "
        "universal addressability (@claim_p3_universal_addressability) "
        "matches Identity / Pointer; explicit typed relationships "
        "(@claim_p7_explicit_relationships) match Typed link. The "
        "row-by-row mapping in Table 2 [@Park2026Kumiho] is exhaustive."
    ),
    prior=0.92,
)

# AGM thesis from postulate satisfaction + Flouris avoidance + L_G prereqs
support_agm_correspondence_thesis = support(
    [claim_table4_postulate_summary, claim_flouris_avoidance, claim_lg_satisfies_agm_prereqs],
    claim_agm_correspondence_thesis,
    reason=(
        "**Central formal contribution from postulate proofs + L_G "
        "prerequisites + Flouris avoidance.** The AGM correspondence claim "
        "(@claim_agm_correspondence_thesis) holds because: (i) the "
        "postulate-satisfaction summary (@claim_table4_postulate_summary) "
        "establishes K*2-K*6 + Hansson's base postulates; (ii) the L_G logic "
        "satisfies AGM prerequisites (@claim_lg_satisfies_agm_prereqs); "
        "(iii) Flouris-style impossibilities are avoided "
        "(@claim_flouris_avoidance). Recovery is intentionally rejected, "
        "K*7/K*8 are argued only -- both are explicit in the thesis."
    ),
    prior=0.93,
)

# AGM compliance headline (49 scenarios) from Table 18
support_agm_compliance_headline = support(
    [claim_agm_compliance_table18],
    claim_agm_compliance_headline,
    reason=(
        "**The 100% AGM compliance headline is directly from Table 18.** "
        "The headline (@claim_agm_compliance_headline) summarizes the 49/49 "
        "result tabulated in @claim_agm_compliance_table18."
    ),
    prior=0.97,
)

# AGM compliance table itself: empirical pass result (independent of the
# formal proofs; this is the *implementation* verification)
support_agm_table18_empirical = support(
    [claim_table4_postulate_summary],
    claim_agm_compliance_table18,
    reason=(
        "**The compliance suite verifies that the *implementation* faithfully "
        "executes the *formal specification* established by the postulate "
        "proofs (@claim_table4_postulate_summary).** The 49 scenarios stress "
        "the operators across simple, multi-item, chain, temporal, and "
        "adversarial configurations; passing all 49 confirms implementation-"
        "to-spec fidelity. This is empirical evidence, not formal proof."
    ),
    prior=0.95,
)

# ===========================================================================
# 8. LoCoMo headline derivations
# ===========================================================================

support_locomo_headline = support(
    [claim_locomo_table12_cross_system, claim_locomo_table13_per_category, claim_adversarial_refusal_natural],
    claim_locomo_headline,
    reason=(
        "**LoCoMo headline (0.447 + 97.5%) from cross-system table + "
        "per-category breakdown + adversarial refusal.** The headline "
        "(@claim_locomo_headline) summarizes Tables 12 "
        "(@claim_locomo_table12_cross_system) and 13 "
        "(@claim_locomo_table13_per_category); the 97.5% adversarial refusal "
        "is the natural consequence of the belief-revision architecture "
        "(@claim_adversarial_refusal_natural)."
    ),
    prior=0.95,
)

support_adversarial_natural = support(
    [claim_p5_immutable_revisions, claim_unified_thesis],
    claim_adversarial_refusal_natural,
    reason=(
        "**Adversarial refusal is structurally guaranteed.** Immutable "
        "revisions (@claim_p5_immutable_revisions) preserve only what was "
        "actually discussed; consolidation strips surface cues. Combined "
        "with the unified architecture (@claim_unified_thesis), the memory "
        "graph genuinely contains no fabricated information -- so there is "
        "nothing for the model to hallucinate from."
    ),
    prior=0.9,
)

# LoCoMo-Plus headline from baseline table + recall + model-decoupling
support_locomo_plus_headline = support(
    [claim_locomo_plus_table15_baselines, claim_locomo_plus_recall_98_5, claim_model_decoupled_validation],
    claim_locomo_plus_headline,
    reason=(
        "**LoCoMo-Plus headline (93.3% / 98.5% recall / 47.6pp gap) from "
        "baseline comparison + recall analysis + model-decoupling "
        "validation.** The headline (@claim_locomo_plus_headline) "
        "summarizes Table 15 (@claim_locomo_plus_table15_baselines), the "
        "recall-vs-fabrication breakdown (@claim_locomo_plus_recall_98_5), "
        "and the model-decoupled invariant (@claim_model_decoupled_validation)."
    ),
    prior=0.95,
)

# Pre-enrichment baseline -> >6mo cliff elimination
support_time_gap_table_from_innovations = support(
    [claim_locomo_plus_table17_time_gap],
    claim_locomo_plus_table15_baselines,
    reason=(
        "**The headline 93.3% accuracy is in part driven by the >6-month "
        "cliff elimination (@claim_locomo_plus_table17_time_gap).** Pre-"
        "enrichment >6mo accuracy was 37.5%; with prospective indexing + "
        "event extraction, it rises to 84.4% (+47pp). This is one of the "
        "key mechanisms behind the headline number."
    ),
    prior=0.88,
)

# Recall 98.5% supports model-decoupled validation
support_model_decoupled_from_recall = support(
    [claim_locomo_plus_recall_98_5, claim_decoupling_storage, claim_decoupling_mcp],
    claim_model_decoupled_validation,
    reason=(
        "**Model-decoupling validation: recall is invariant across answer "
        "models.** Both GPT-4o and GPT-4o-mini receive identical recalled "
        "context from the same retrieval pipeline (@claim_locomo_plus_recall_98_5: "
        "98.5% recall). The decoupling principles (@claim_decoupling_storage, "
        "@claim_decoupling_mcp) ensure end-to-end accuracy improves with "
        "model strength without pipeline changes."
    ),
    prior=0.93,
)

# ===========================================================================
# 9. Headline contribution synthesis
# ===========================================================================

support_headline_contribution = support(
    [
        claim_unified_thesis,
        claim_agm_correspondence_thesis,
        claim_locomo_headline,
        claim_locomo_plus_headline,
        claim_agm_compliance_headline,
    ],
    claim_headline_contribution,
    reason=(
        "**Headline contribution synthesis.** Five pillars: (i) unified "
        "memory+asset architecture (@claim_unified_thesis); (ii) AGM "
        "correspondence (@claim_agm_correspondence_thesis); (iii) LoCoMo "
        "0.447/97.5% (@claim_locomo_headline); (iv) LoCoMo-Plus 93.3%/98.5% "
        "(@claim_locomo_plus_headline); (v) AGM compliance 100% "
        "(@claim_agm_compliance_headline). Each is independently established; "
        "together they constitute the full announced contribution "
        "[@Park2026Kumiho, Sec. 1; Sec. 17]."
    ),
    prior=0.95,
)

# ===========================================================================
# 10. Architectural-synthesis gap derivation from per-system gaps
# ===========================================================================

# Note: the induction above (induction_arch_generalizes etc.) uses the law
# direction "law predicts observation". Below, we add a `support` derivation
# for the synthesis-gap law from the cross-system Table 1 + Tables 8/9.

support_synthesis_gap_from_tables = support(
    [claim_table1_comparison, claim_table8_comparative_dimensions, claim_table9_feature_comparison],
    claim_cross_baseline_synthesis_gap,
    reason=(
        "**The cross-baseline architectural-synthesis gap is the empirical "
        "consolidation of three comparison tables.** Table 1 "
        "(@claim_table1_comparison) compares 6 axes; Table 8 "
        "(@claim_table8_comparative_dimensions) compares 9 axes; Table 9 "
        "(@claim_table9_feature_comparison) compares 12 features across 7 "
        "concurrent systems. Across all three tables, no concurrent system "
        "covers all four critical axes simultaneously."
    ),
    prior=0.94,
)

# ===========================================================================
# 11. Components-exist-but-synthesis-missing supports the agm thesis
# ===========================================================================

support_components_exist_landscape = support(
    [claim_graphiti_components, claim_mem0_components, claim_letta_components, claim_amem_components],
    claim_components_exist,
    reason=(
        "**Components-exist landscape claim is the union of per-system "
        "diagnoses.** Graphiti (@claim_graphiti_components) provides "
        "retrieval+versioning; Mem0 (@claim_mem0_components) provides "
        "timestamped versioning; Letta (@claim_letta_components) provides "
        "Git-backed versioning; A-MEM (@claim_amem_components) provides "
        "dynamic linking. Components exist; only the synthesis is missing."
    ),
    prior=0.96,
)

support_synthesis_underexplored = support(
    [claim_components_exist, claim_cross_baseline_synthesis_gap],
    claim_synthesis_underexplored,
    reason=(
        "**Components exist but synthesis is underexplored.** The components "
        "are present across concurrent systems (@claim_components_exist), "
        "yet the cross-system table analysis (@claim_cross_baseline_synthesis_gap) "
        "shows no system has unified them with formal grounding -- which is "
        "exactly the underexploration claim."
    ),
    prior=0.94,
)

# ===========================================================================
# 12. Context-extension-not-memory derivation
# ===========================================================================

support_context_not_memory = support(
    [claim_attention_not_recall, claim_quadratic_cost_scaling, claim_no_structural_representation, claim_model_coupling],
    claim_context_extension_not_memory,
    reason=(
        "**Context-extension-as-memory fails on four structural deficiencies.** "
        "(i) attention != recall (@claim_attention_not_recall); (ii) "
        "quadratic cost scaling (@claim_quadratic_cost_scaling) makes lifelong "
        "context infeasible; (iii) no structural representation "
        "(@claim_no_structural_representation); (iv) model coupling "
        "(@claim_model_coupling) makes context ephemeral and "
        "model-specific."
    ),
    prior=0.92,
)

# ===========================================================================
# 13. Comparative-analysis claims supported by per-baseline evidence
# ===========================================================================

support_table8_dimensions = support(
    [claim_p5_immutable_revisions, claim_p7_explicit_relationships, claim_p3_universal_addressability],
    claim_table8_comparative_dimensions,
    reason=(
        "**Table 8 dimensions reflect the design principles.** Versioned "
        "history (@claim_p5_immutable_revisions), 6 typed edge types "
        "(@claim_p7_explicit_relationships), and full-history-plus-tags "
        "navigation (URI-based, @claim_p3_universal_addressability) are the "
        "Kumiho-column entries that distinguish it from flat RAG, tiered "
        "buffers, extended context, and static KGs."
    ),
    prior=0.92,
)

support_table9_features = support(
    [claim_p5_immutable_revisions, claim_agm_correspondence_thesis, claim_p3_universal_addressability, claim_byo_storage_benefits],
    claim_table9_feature_comparison,
    reason=(
        "**Table 9 unique features = formal AGM + URI + unified asset graph + "
        "BYO-storage + audit.** Immutable revision history "
        "(@claim_p5_immutable_revisions), formal belief revision "
        "(@claim_agm_correspondence_thesis), URI-based addressing "
        "(@claim_p3_universal_addressability), and BYO-storage "
        "(@claim_byo_storage_benefits) are the four cells where Kumiho is "
        "uniquely 'check' across the 12-feature comparison."
    ),
    prior=0.92,
)

# Per-baseline comparative support
support_vs_flat = support(
    [claim_p5_immutable_revisions],
    claim_vs_flat_retrieval,
    reason=(
        "**vs. Flat RAG.** Statefulness (@claim_p5_immutable_revisions), "
        "structure (@setup_six_edge_types), and consolidation "
        "(@setup_dream_state_pipeline) extend flat retrieval along three "
        "axes; flat retrieval remains a *component* (vector branch) of "
        "Kumiho's hybrid pipeline."
    ),
    prior=0.93,
    background=[setup_six_edge_types, setup_dream_state_pipeline]
)

support_vs_tiered = support(
    [claim_p5_immutable_revisions, claim_dream_state_safety_guards, claim_decoupling_storage],
    claim_vs_tiered_buffers,
    reason=(
        "**vs. Tiered buffers.** Versioning (@claim_p5_immutable_revisions), "
        "typed edges (@setup_six_edge_types), safety guards "
        "(@claim_dream_state_safety_guards), and storage decoupling "
        "(@claim_decoupling_storage) all distinguish Kumiho from tiered-"
        "buffer systems with LLM-coupled management."
    ),
    prior=0.92,
    background=[setup_six_edge_types]
)

support_vs_static_kg = support(
    [claim_p5_immutable_revisions],
    claim_vs_static_kg,
    reason=(
        "**vs. Static KGs.** Experiential memory requires versioning "
        "(@claim_p5_immutable_revisions) and a working-memory layer "
        "(@setup_dual_store_model); static KGs target shared encyclopedic "
        "knowledge with fixed schemas."
    ),
    prior=0.92,
    background=[setup_dual_store_model]
)

support_vs_magma = support(
    [claim_table4_postulate_summary],
    claim_vs_magma_unified_vs_multi,
    reason=(
        "**vs. MAGMA: unified graph buys atomicity.** The 6 typed edges "
        "(@setup_six_edge_types) coexist in one property graph, enabling "
        "transactional atomicity that makes the AGM postulate proofs "
        "(@claim_table4_postulate_summary) database-level rather than "
        "application-level."
    ),
    prior=0.85,
    background=[setup_six_edge_types]
)

support_vs_hindsight = support(
    [claim_table4_postulate_summary, claim_dream_state_safety_guards],
    claim_vs_hindsight_complementary,
    reason=(
        "**vs. Hindsight: complementary roles.** Hindsight has empirical "
        "belief tracking but no AGM guarantees; Kumiho's formal framework "
        "(@claim_table4_postulate_summary) and safety guards "
        "(@claim_dream_state_safety_guards) provide the theoretical "
        "consistency properties Hindsight lacks."
    ),
    prior=0.93,
)

# ===========================================================================
# 14. NL-to-triple boundary, partial merge, asymmetric bridge derivations
# ===========================================================================

support_nl_to_triple_boundary = support(
    [claim_atomic_writes, claim_decoupling_mcp],
    claim_nl_to_triple_boundary,
    reason=(
        "**NL-to-triple boundary is a structured API contract, not NLP.** "
        "Atomic writes via single MCP invocation (@claim_atomic_writes) "
        "force the agent's natural-language output through typed fields; "
        "the decoupling-via-MCP (@claim_decoupling_mcp) makes the boundary "
        "model-agnostic."
    ),
    prior=0.93,
)

support_nl_mapping_scope = support(
    [claim_nl_to_triple_boundary, claim_k6_extensionality],
    claim_nl_mapping_scope_limit,
    reason=(
        "**NL mapping scope limits formal guarantees.** The mapping "
        "(@claim_nl_to_triple_boundary) is many-to-one; K*6 "
        "(@claim_k6_extensionality) holds over the *formal* representation "
        "but cannot guarantee that the agent will consistently map "
        "equivalent NL inputs to equivalent ground atoms. Mapping "
        "consistency is therefore a prompt-engineering concern outside the "
        "formal scope."
    ),
    prior=0.92,
)

# Semantic merge is a future-work identification, kept as leaf claim.

support_compound_input_two = support(
    [claim_k7_superexpansion_argued, claim_k8_subexpansion_argued],
    claim_compound_input_two_strategies,
    reason=(
        "**Compound input has two operational strategies, both formal-"
        "equivalent for atoms.** K*7 + K*8 (@claim_k7_superexpansion_argued, "
        "@claim_k8_subexpansion_argued) give equivalence when B is consistent "
        "with B*A; for ground atomic inputs distinct atoms are independent, "
        "so the two strategies are equivalent in the common case."
    ),
    prior=0.9,
)

support_conflict_presentation = support(
    [claim_superseded_not_excluded],
    claim_conflict_presentation,
    reason=(
        "**Conflict presentation follows from the superseded-retrievability "
        "design (@claim_superseded_not_excluded).** The retrieval pipeline "
        "surfaces both beliefs with metadata; the agent reasons about "
        "which to adopt."
    ),
    prior=0.92,
)

support_asymmetric_bridge = support(
    [claim_decoupling_storage],
    claim_asymmetric_bridge,
    reason=(
        "**Asymmetric bridge follows from the storage-decoupling and the "
        "graph-as-system-of-record (@setup_symbolic_subsymbolic_division).** "
        "Storage-decoupling (@claim_decoupling_storage) commits to graph-"
        "structured belief state; embeddings and LLM outputs are derived "
        "indices and recommendations, never bypassing the graph."
    ),
    prior=0.93,
    background=[setup_symbolic_subsymbolic_division]
)

support_formal_robustness = support(
    [claim_asymmetric_bridge, claim_dream_state_safety_guards],
    claim_formal_robustness_to_subsymbolic,
    reason=(
        "**Formal robustness follows from asymmetric bridge + safety "
        "guards.** The bridge (@claim_asymmetric_bridge) means embeddings "
        "and LLM failures cannot violate belief-base structure; safety "
        "guards (@claim_dream_state_safety_guards) contain LLM-assessment "
        "errors operationally."
    ),
    prior=0.9,
)

support_postulate_scope = support(
    [claim_table4_postulate_summary],
    claim_postulate_scope,
    reason=(
        "**Postulate scope.** The two-tier model (@setup_def_two_tier) "
        "shows B_retr ⊆ B; postulate satisfaction (@claim_table4_postulate_summary) "
        "is for B(tau), not for the score-ranked retrieval surface, which "
        "introduces non-deterministic ranking."
    ),
    prior=0.93,
    background=[setup_def_two_tier]
)

# ===========================================================================
# 15. Architecture sub-claims (retrieval, dream state, MCP, audit, etc.)
# ===========================================================================

support_combmax_design = support(
    [claim_bm25_history],
    claim_combmax_design_choice,
    reason=(
        "**CombMAX is a deliberate design choice within the hybrid retrieval "
        "pipeline (@setup_hybrid_pipeline).** The fusion-functions literature "
        "(@claim_bm25_history) [@Bruch2023Fusion; @Cormack2009RRF] documents "
        "the alternatives (RRF, convex combination); CombMAX is chosen for "
        "precision preservation."
    ),
    prior=0.85,
    background=[setup_hybrid_pipeline]
)

support_precision_preservation = support(
    [claim_combmax_caveat],
    claim_precision_preservation,
    reason=(
        "**Precision preservation (Observation 8.1) is a design-level "
        "argument, not a formal IR result.** It follows from the max-fusion "
        "scoring (@setup_hybrid_pipeline) provided score calibration is "
        "adequate; the CombMAX caveat (@claim_combmax_caveat) acknowledges "
        "the calibration dependency."
    ),
    prior=0.78,
    background=[setup_hybrid_pipeline]
)

support_recall_non_degradation = support(
    [claim_precision_preservation],
    claim_recall_non_degradation,
    reason=(
        "**Recall non-degradation: any non-destructive index has this "
        "property in the unbounded case; in the k-bounded case, "
        "displacement is mitigated by precision preservation "
        "(@claim_precision_preservation)."
    ),
    prior=0.88,
    background=[setup_hybrid_pipeline]
)

support_client_side_reranking = support(
    [claim_decoupling_storage, claim_decoupling_pluggable_llm],
    claim_client_side_reranking,
    reason=(
        "**Client-side reranking embodies the LLM-decoupled-memory principle.** "
        "Storage decoupling (@claim_decoupling_storage) and pluggable LLM "
        "(@claim_decoupling_pluggable_llm) allow the consuming agent's "
        "own LLM to perform reranking on structured metadata at zero "
        "additional cost."
    ),
    prior=0.93,
)

support_dream_state_safety = support(
    [claim_p10_conservative_consolidation],
    claim_dream_state_safety_guards,
    reason=(
        "**Six safety guards encode the conservative-consolidation principle "
        "(@claim_p10_conservative_consolidation).** Each guard "
        "(dry-run, published-protect, circuit-breaker, error-isolate, "
        "audit-report, cursor-persist) operates within the pipeline "
        "(@setup_dream_state_pipeline)."
    ),
    prior=0.93,
    background=[setup_dream_state_pipeline]
)

support_consolidation_formal_status = support(
    [claim_dream_state_safety_guards],
    claim_consolidation_formal_status,
    reason=(
        "**The Dream State pipeline is an engineering, not formal, "
        "contribution.** Per-action mappings preserve formal semantics; "
        "compositional preservation across batches is open. Safety guards "
        "(@claim_dream_state_safety_guards) provide operational containment, "
        "not formal guarantees."
    ),
    prior=0.92,
)

support_byo_storage = support(
    [claim_p6_metadata_over_content],
    claim_byo_storage_benefits,
    reason=(
        "**BYO-storage benefits derive from metadata-over-content principle "
        "(@claim_p6_metadata_over_content) and the privacy boundary "
        "(@setup_privacy_boundary).** The graph contains pointers, not "
        "content."
    ),
    prior=0.95,
    background=[setup_privacy_boundary]
)

support_threat_model = support(
    [claim_byo_storage_benefits, claim_dream_state_safety_guards],
    claim_threat_model,
    reason=(
        "**Threat model documents per-threat mitigations.** PII redaction "
        "+ BYO-storage (@setup_privacy_boundary, @claim_byo_storage_benefits) "
        "address the dominant threats; safety guards "
        "(@claim_dream_state_safety_guards) limit prompt-injection blast "
        "radius."
    ),
    prior=0.88,
    background=[setup_privacy_boundary]
)

support_mcp_51_tools = support(
    [claim_mcp_breadth_distinguisher, claim_atomic_writes],
    claim_mcp_51_tools,
    reason=(
        "**The 51-tool MCP surface implements the breadth claim "
        "(@claim_mcp_breadth_distinguisher) with atomic-write semantics "
        "(@claim_atomic_writes)."
    ),
    prior=0.95,
)

support_human_audit = support(
    [claim_p1_structural_reuse, claim_governance_via_same_graph],
    claim_human_audit_dashboard,
    reason=(
        "**The dashboard renders the same graph hierarchy used by agents.** "
        "Structural reuse (@claim_p1_structural_reuse) and the governance "
        "principle (@claim_governance_via_same_graph) entail one substrate "
        "for both agent operation and human inspection."
    ),
    prior=0.94,
)

support_reference_implementation = support(
    [claim_human_audit_dashboard, claim_mcp_51_tools],
    claim_reference_implementation,
    reason=(
        "**The reference implementation [@KumihoCode] instantiates the "
        "architecture.** The dashboard (@claim_human_audit_dashboard) and "
        "the MCP server (@claim_mcp_51_tools) plus the SDK + library + "
        "desktop are documented at https://kumiho.io / "
        "https://github.com/KumihoIO."
    ),
    prior=0.95,
)

# ===========================================================================
# 16. Use cases derived from architectural commitments
# ===========================================================================

support_multi_agent_pipeline = support(
    [claim_dual_purpose_graph, claim_governance_via_same_graph],
    claim_multi_agent_creative_pipeline,
    reason=(
        "**Multi-agent creative pipeline scenario instantiates the "
        "dual-purpose graph (@claim_dual_purpose_graph) with multi-agent "
        "coordination + governance (@claim_governance_via_same_graph) "
        "operating on the same substrate."
    ),
    prior=0.93,
)

support_vfx_origin = support(
    [claim_p1_structural_reuse],
    claim_vfx_pipeline_origin,
    reason=(
        "**VFX pipeline origin is the empirical source of the structural-"
        "reuse principle (@claim_p1_structural_reuse).** Asset-management "
        "primitives in VFX/game-dev pioneered the same graph-native "
        "design decades ago."
    ),
    prior=0.93,
)

support_decision_audit = support(
    [claim_governance_native, claim_p5_immutable_revisions],
    claim_decision_auditability_use_case,
    reason=(
        "**Decision auditability follows from the native-governance design "
        "(@claim_governance_native) plus immutable revisions "
        "(@claim_p5_immutable_revisions): every decision can be traced via "
        "Derived_From + tau_T historical resolution."
    ),
    prior=0.95,
)

support_coding_agent = support(
    [claim_agent_outputs_accumulate, claim_unified_thesis],
    claim_coding_agent_use_case,
    reason=(
        "**Coding/design/research/production agents are concrete instances "
        "of the agent-output accumulation problem (@claim_agent_outputs_accumulate) "
        "addressed by the unified thesis (@claim_unified_thesis)."
    ),
    prior=0.93,
)

support_letta_concrete = support(
    [claim_letta_components],
    claim_letta_concrete_example,
    reason=(
        "**The warm/cool tones example illustrates the three Letta "
        "differences (@claim_letta_components): typed edges (@setup_six_edge_types), "
        "AGM-compliant supersession (@setup_def_revision_op), and "
        "automatic downstream propagation."
    ),
    prior=0.94,
    background=[setup_def_revision_op, setup_six_edge_types]
)

# ===========================================================================
# 17. Worked example follows from the postulates
# ===========================================================================

support_worked_example = support(
    [claim_k2_success, claim_k5_consistency, claim_k3_inclusion_base_version],
    claim_worked_example_preference,
    reason=(
        "**The worked example (favorite color, Section 7.5) exercises K*2 "
        "(@claim_k2_success), K*5 (@claim_k5_consistency), K*3 "
        "(@claim_k3_inclusion_base_version), and Depends_On traversal "
        "(@setup_six_edge_types) end-to-end."
    ),
    prior=0.95,
    background=[setup_six_edge_types]
)

support_belief_revision_practice = support(
    [claim_worked_example_preference, claim_k2_success, claim_k5_consistency],
    claim_belief_revision_in_practice,
    reason=(
        "**Section 15.6's deployed favorite-color case generalizes the "
        "worked example (@claim_worked_example_preference): K*2 "
        "(@claim_k2_success), K*5 (@claim_k5_consistency) hold operationally."
    ),
    prior=0.93,
)

support_cross_session_provenance = support(
    [claim_p5_immutable_revisions],
    claim_cross_session_provenance_paper,
    reason=(
        "**Cross-session provenance via Derived_From edges "
        "(@setup_six_edge_types) and immutable revisions "
        "(@claim_p5_immutable_revisions): the paper's own 6-revision chain "
        "exercises both."
    ),
    prior=0.93,
    background=[setup_six_edge_types]
)

support_dream_state_validation = support(
    [claim_dream_state_safety_guards],
    claim_dream_state_deployment_validation,
    reason=(
        "**Dream State deployment validation: safety guards "
        "(@claim_dream_state_safety_guards) operated as designed during the "
        "LoCoMo eval -- 0 manual interventions required."
    ),
    prior=0.92,
)

# ===========================================================================
# 18. Limitation derivations
# ===========================================================================

support_limit_LG = support(
    [claim_expressiveness_tradeoff, claim_flouris_dl_impossibility],
    claim_limit_lg_expressiveness,
    reason=(
        "**L_G expressiveness limit is the explicit trade-off "
        "(@claim_expressiveness_tradeoff): any strengthening would "
        "re-encounter Flouris (@claim_flouris_dl_impossibility)."
    ),
    prior=0.93,
)

support_limit_formal_scope = support(
    [claim_k7k8_representation_gap, claim_postulate_scope],
    claim_limit_formal_scope,
    reason=(
        "**Formal-scope limit consolidates K*7/K*8 representation gap "
        "(@claim_k7k8_representation_gap) and the postulate-scope statement "
        "(@claim_postulate_scope: proved for B(tau), not for the score-"
        "ranked retrieval surface)."
    ),
    prior=0.94,
)

support_limit_dream_state_llm = support(
    [claim_consolidation_formal_status, claim_dream_state_safety_guards],
    claim_limit_dream_state_llm_dependency,
    reason=(
        "**Dream State LLM dependency is acknowledged as an engineering "
        "(not formal) contribution (@claim_consolidation_formal_status); "
        "safety guards (@claim_dream_state_safety_guards) bound but do "
        "not eliminate gradual quality erosion."
    ),
    prior=0.92,
)

# ===========================================================================
# 19. Conclusion synthesis
# ===========================================================================

support_conclusion = support(
    [claim_unified_thesis, claim_agm_correspondence_thesis, claim_synthesis_underexplored],
    claim_conclusion_unification,
    reason=(
        "**Conclusion: the contribution is the architectural synthesis + "
        "formal grounding (@claim_unified_thesis, @claim_agm_correspondence_thesis), "
        "not novel components (@claim_synthesis_underexplored)."
    ),
    prior=0.95,
)

# ===========================================================================
# 20. Wiring for previously-orphaned claims
# ===========================================================================

# These claims are derived/related but were not wired in earlier passes.
# Each is anchored to its most natural premise(s).

# Imports for s9_use_cases & s10 future work additions
from .s10_discussion_limitations import (
    claim_future_ablation_study,
    claim_future_adaptive_consolidation,
    claim_future_chronological_ordering,
    claim_future_controlled_cross_system,
    claim_future_entrenchment_k7k8,
    claim_future_goal_aware_indexing,
    claim_future_partial_merge_operator,
    claim_future_retrieval_ablation,
    claim_future_richer_logics,
    claim_future_temporal_recency_retrieval,
)
from .s2_related_work import (
    claim_agm_lineage,
    claim_agm_ml_correspondences,
    claim_gcc_text_versioning,
)
from .s5_agm_correspondence import claim_complexity_bounds
from .s7_kumiho_architecture import claim_coverage_complementarity
from .s8_evaluation import (
    claim_independent_reproduction,
    claim_locomo_plus_cost,
    claim_locomo_plus_table16_by_type,
    claim_limit_cross_system_methodology,
    claim_limit_eval_scope_complementarity,
    claim_limit_scale,
    claim_limit_self_eval_bias,
    claim_limit_system_performance,
)
from .s6_revision_semantics import (
    claim_cwa_classical_negation_duality,
    claim_deprecated_filter_architectural,
    claim_partial_merge_atomic_replacement,
    claim_partial_merge_finer_atomicity,
    claim_partial_merge_semantic_future,
    claim_property_graph_not_rdf,
)
from .s2_related_work import (
    claim_benchmark_standardization_caveat,
    claim_observability_gap,
    claim_recovery_critiques,
)
from .s3_structural_primitives import (
    claim_p2_match_storage_latency,
    claim_p8_graph_native_advantage,
    claim_p9_non_blocking_enhancement,
    claim_table10_seven_principles,
)
from .s9_use_cases import claim_multi_channel_session_identity

# AGM-lineage supports the AGM-correspondence thesis at the theoretical level
support_agm_lineage_underlies = support(
    [claim_agm_lineage],
    claim_agm_correspondence_thesis,
    reason=(
        "**AGM lineage underlies the formal contribution.** The AGM framework "
        "[@AGM1985] and Hansson's belief-base extension [@Hansson1999Textbook] "
        "(@claim_agm_lineage) provide the theoretical apparatus the "
        "correspondence thesis builds on."
    ),
    prior=0.93,
)

# Recovery-critiques justify the principled rejection
support_recovery_critiques_justify = support(
    [claim_recovery_critiques],
    claim_recovery_rejection_principled,
    reason=(
        "**Recovery critiques in the literature justify Kumiho's principled "
        "rejection.** Makinson, Hansson, Fuhrmann (@claim_recovery_critiques) "
        "argued Recovery imposes unreasonable constraints on systems with "
        "non-trivial internal structure or provenance -- exactly Kumiho's "
        "regime."
    ),
    prior=0.92,
)

# AGM-ML correspondences situate the AGM thesis within current research
support_agm_ml_situates = support(
    [claim_agm_ml_correspondences],
    claim_synthesis_underexplored,
    reason=(
        "**AGM-ML correspondences (@claim_agm_ml_correspondences) target LLM "
        "weights or prompts; Kumiho applies AGM to external memory.** This "
        "supports the underexplored-synthesis observation: the AGM-memory "
        "intersection is an open design space."
    ),
    prior=0.85,
)

# GCC vs Kumiho file-vs-graph: complementary observation supporting Letta-comp
support_gcc_versus = support(
    [claim_gcc_text_versioning],
    claim_letta_components,
    reason=(
        "**GCC's text-level Git semantics (@claim_gcc_text_versioning) parallel "
        "Letta's file-level Git approach (@claim_letta_components).** Both "
        "are text-versioning approaches Kumiho extends to typed-graph "
        "primitives."
    ),
    prior=0.85,
)

# Complexity bounds support the architectural feasibility claim
support_complexity_supports_arch = support(
    [claim_complexity_bounds],
    claim_reference_implementation,
    reason=(
        "**Bounded complexity (@claim_complexity_bounds) is what makes the "
        "reference implementation tractable in production deployment** with "
        "measured 15ms / 80-120ms latencies."
    ),
    prior=0.9,
)

# Coverage complementarity supports precision preservation indirectly
# (already tied via setup_hybrid_pipeline; here we tie via the design choice)
support_coverage_supports_combmax = support(
    [claim_coverage_complementarity],
    claim_combmax_design_choice,
    reason=(
        "**Coverage complementarity (@claim_coverage_complementarity) "
        "motivates max-fusion: each branch catches different cases; the "
        "stronger signal should not be diluted by the weaker** -- which is "
        "exactly the CombMAX design rationale."
    ),
    prior=0.88,
)

# Property-graph-not-RDF: supports the L_G analytical-abstraction claim
support_pg_not_rdf_supports_LG = support(
    [claim_property_graph_not_rdf],
    claim_nl_to_triple_boundary,
    reason=(
        "**Property graph != RDF (@claim_property_graph_not_rdf): ground "
        "triples are an analytical abstraction over a richer property "
        "graph, not an RDF commitment.** This supports the NL-to-triple "
        "boundary characterization."
    ),
    prior=0.9,
)

# Deprecated filter is architectural; supports the consistency postulate
support_deprecated_supports_K5 = support(
    [claim_deprecated_filter_architectural],
    claim_k5_consistency,
    reason=(
        "**The architecturally-enforced deprecated-filter "
        "(@claim_deprecated_filter_architectural) is what makes K*5 "
        "Consistency hold even when superseded revisions still exist in the "
        "graph -- the WHERE NOT item.deprecated clause excludes them from "
        "B_retr."
    ),
    prior=0.9,
)

# (already wired via support_conflict_presentation above)

# Partial-merge atomic supports the operational-revision encoding
support_partial_atomic_supports_revision = support(
    [claim_partial_merge_atomic_replacement],
    claim_compound_input_two_strategies,
    reason=(
        "**Atomic replacement (@claim_partial_merge_atomic_replacement) is "
        "the default partial-merge strategy and underlies the "
        "single-revision encoding option for compound inputs."
    ),
    prior=0.92,
)

# Partial-merge finer supports the same compound-strategy claim
support_partial_finer_supports_revision = support(
    [claim_partial_merge_finer_atomicity],
    claim_compound_input_two_strategies,
    reason=(
        "**Finer-grained atomicity (@claim_partial_merge_finer_atomicity) is "
        "the deployment alternative supporting the same compound-input "
        "decomposition."
    ),
    prior=0.85,
)

# Partial-merge semantic-future justifies the future-partial-merge direction
support_partial_semantic_future_link = support(
    [claim_partial_merge_semantic_future],
    claim_future_partial_merge_operator,
    reason=(
        "**Semantic-merge as future work (@claim_partial_merge_semantic_future) "
        "is the design-doc anchor for the future-direction partial-merge "
        "operator."
    ),
    prior=0.95,
)

# CWA / classical-negation duality supports the L_G analysis (and Flouris)
support_cwa_supports_flouris_avoid = support(
    [claim_cwa_classical_negation_duality],
    claim_flouris_avoidance,
    reason=(
        "**The CWA / classical-negation duality (@claim_cwa_classical_negation_duality) "
        "is one of the three structural differences from DLs that lets L_G "
        "avoid the Flouris impossibility (Sec. 7.6 'closed-world operational "
        "semantics' point)."
    ),
    prior=0.9,
)

# Observability gap supports the human-audit-dashboard contribution
support_observability_gap_supports_audit = support(
    [claim_observability_gap],
    claim_human_audit_dashboard,
    reason=(
        "**Existing observability tools trace inference, not memory "
        "(@claim_observability_gap); Kumiho's dashboard renders the memory "
        "graph itself as auditable** -- this is the Section 2.5 -> Section "
        "11.4 connection."
    ),
    prior=0.92,
)

# Benchmark-construction caveats support the LoCoMo / LoCoMo-Plus headlines
# being interpretively scoped, not absolute claims
support_benchmark_caveat_locomo = support(
    [claim_benchmark_standardization_caveat],
    claim_locomo_table12_cross_system,
    reason=(
        "**LoCoMo numbers should be interpreted within the standardization "
        "caveat (@claim_benchmark_standardization_caveat).** The cross-system "
        "table is comparable on the *official* metric, but baseline scores "
        "from publications carry their own configuration variance."
    ),
    prior=0.85,
)

# Independent reproduction supports the LoCoMo-Plus headline
support_independent_repro_supports = support(
    [claim_independent_reproduction],
    claim_locomo_plus_headline,
    reason=(
        "**Independent reproduction in the mid-80% range (@claim_independent_reproduction) "
        "supports the LoCoMo-Plus headline** even after discounting from "
        "Kumiho's own 93.3% to a more conservative figure."
    ),
    prior=0.93,
)

# Cost analysis supports the model-decoupling validation
support_cost_supports_decoupling = support(
    [claim_locomo_plus_cost],
    claim_model_decoupled_validation,
    reason=(
        "**The ~$14 cost (@claim_locomo_plus_cost) is achieved using GPT-4o-mini "
        "for bulk operations and GPT-4o only for answer generation -- the "
        "model swap is a configuration change, supporting the model-"
        "decoupling validation."
    ),
    prior=0.9,
)

# Per-type breakdown supports the recall vs fabrication failure analysis
support_type_table_supports_recall = support(
    [claim_locomo_plus_table16_by_type],
    claim_locomo_plus_recall_98_5,
    reason=(
        "**The per-type breakdown (@claim_locomo_plus_table16_by_type) shows "
        "goal-type as hardest at 85% with 4o.** Combined with the failure "
        "taxonomy this supports the 98.5% recall / 78%-fabrication analysis."
    ),
    prior=0.93,
)

# Benchmark-construction caveat supports the recall observation interpretation
support_benchmark_construction_supports = support(
    [claim_benchmark_construction_caveat],
    claim_locomo_plus_headline,
    reason=(
        "**The benchmark-construction caveat (GPT-family alignment, "
        "@claim_benchmark_construction_caveat) contextualizes the LoCoMo-Plus "
        "headline: the result is strong evidence for prospective-indexing "
        "effectiveness even after discounting for model-family alignment."
    ),
    prior=0.85,
)

# Limitations all support the conclusion (synthesizes scope honestly)
support_limit_scale_conclusion = support(
    [claim_limit_scale],
    claim_conclusion_unification,
    reason=(
        "**Scale limitation (@claim_limit_scale) is acknowledged in the "
        "conclusion's framing of the contribution as an architectural "
        "synthesis -- adversarial-scale precision is identified as future "
        "work."
    ),
    prior=0.85,
)

support_limit_cross_system_conclusion = support(
    [claim_limit_cross_system_methodology],
    claim_conclusion_unification,
    reason=(
        "**Cross-system methodology limitation "
        "(@claim_limit_cross_system_methodology) is honestly acknowledged in "
        "the conclusion's framing of the LoCoMo numbers as benchmark-"
        "consistent rather than infrastructure-controlled."
    ),
    prior=0.85,
)

support_limit_eval_scope_conclusion = support(
    [claim_limit_eval_scope_complementarity],
    claim_conclusion_unification,
    reason=(
        "**LoCoMo + AGM-suite complementarity (@claim_limit_eval_scope_complementarity) "
        "is acknowledged: the integrated belief-revision-correctness benchmark "
        "is identified as future work."
    ),
    prior=0.85,
)

support_limit_self_eval_conclusion = support(
    [claim_limit_self_eval_bias],
    claim_conclusion_unification,
    reason=(
        "**Self-evaluation bias (@claim_limit_self_eval_bias) is acknowledged "
        "by reporting raw numbers without favorable interpretation -- "
        "supporting the conclusion's transparency framing."
    ),
    prior=0.88,
)

support_limit_system_perf_conclusion = support(
    [claim_limit_system_performance],
    claim_conclusion_unification,
    reason=(
        "**System-performance reporting limitation (@claim_limit_system_performance) "
        "is acknowledged: only headline 15ms / 80-120ms latencies are "
        "reported; full distributions are pending."
    ),
    prior=0.85,
)

# Future directions support the future-extension framing in the conclusion
support_future_goal_aware = support(
    [claim_locomo_plus_table16_by_type],
    claim_future_goal_aware_indexing,
    reason=(
        "**Goal-type accuracy at 85% (@claim_locomo_plus_table16_by_type) "
        "motivates goal-aware prospective indexing as a targeted future "
        "extension."
    ),
    prior=0.88,
)

support_future_chronological = support(
    [claim_locomo_plus_table16_by_type],
    claim_future_chronological_ordering,
    reason=(
        "**Goal-type questions require narrative-arc reasoning "
        "(@claim_locomo_plus_table16_by_type), motivating chronological "
        "context ordering as a future enhancement."
    ),
    prior=0.85,
)

support_future_ablation = support(
    [claim_locomo_plus_table17_time_gap],
    claim_future_ablation_study,
    reason=(
        "**The pre-enrichment vs full-system jump (@claim_locomo_plus_table17_time_gap: "
        "37.5% -> 84.4%) motivates an enrichment ablation study to isolate "
        "individual contributions."
    ),
    prior=0.9,
)

support_future_controlled_xs = support(
    [claim_limit_cross_system_methodology],
    claim_future_controlled_cross_system,
    reason=(
        "**The cross-system-methodology limitation (@claim_limit_cross_system_methodology) "
        "directly motivates controlled re-evaluation on identical infrastructure."
    ),
    prior=0.95,
)

support_future_retrieval_ablation = support(
    [claim_combmax_caveat],
    claim_future_retrieval_ablation,
    reason=(
        "**CombMAX caveat (@claim_combmax_caveat) motivates retrieval-pipeline "
        "sensitivity analysis (beta, type weights, fusion methods)."
    ),
    prior=0.93,
)

support_future_entrenchment = support(
    [claim_k7k8_representation_gap],
    claim_future_entrenchment_k7k8,
    reason=(
        "**The K*7/K*8 representation gap (@claim_k7k8_representation_gap) "
        "motivates constructing a type-dependent entrenchment ordering."
    ),
    prior=0.95,
)

support_future_richer_logics = support(
    [claim_limit_lg_expressiveness],
    claim_future_richer_logics,
    reason=(
        "**The L_G expressiveness limit (@claim_limit_lg_expressiveness) "
        "motivates extending toward AGM-compatible DL fragments."
    ),
    prior=0.93,
)

support_future_adaptive_consol = support(
    [claim_consolidation_formal_status],
    claim_future_adaptive_consolidation,
    reason=(
        "**The consolidation pipeline's engineering status "
        "(@claim_consolidation_formal_status) leaves room for adaptive "
        "triggering and anticipatory pre-computation."
    ),
    prior=0.85,
)

support_future_temporal_recency = support(
    [claim_belief_revision_in_practice],
    claim_future_temporal_recency_retrieval,
    reason=(
        "**The favorite-color case (@claim_belief_revision_in_practice) "
        "exhibits the retrieval-ranking limitation that motivates temporal "
        "recency as a third retrieval signal."
    ),
    prior=0.92,
)

# Multi-channel session identity supports decoupling validation
support_multi_channel_supports_dec = support(
    [claim_multi_channel_session_identity],
    claim_decoupling_storage,
    reason=(
        "**Multi-channel session identity (@claim_multi_channel_session_identity) "
        "concretely instantiates the storage-decoupling principle: "
        "sessions follow the user, not the platform."
    ),
    prior=0.9,
)

# Principles 2, 8, 9 support the reference implementation
support_p2_supports_impl = support(
    [claim_p2_match_storage_latency],
    claim_reference_implementation,
    reason=(
        "**P2 (@claim_p2_match_storage_latency) is realized in the "
        "library-SDK Redis layer of the reference implementation (15ms "
        "working memory)."
    ),
    prior=0.92,
)

support_p8_supports_impl = support(
    [claim_p8_graph_native_advantage],
    claim_reference_implementation,
    reason=(
        "**P8 (@claim_p8_graph_native_advantage) is realized in the Neo4j "
        "long-term store of the reference implementation (80-120ms graph "
        "queries)."
    ),
    prior=0.92,
)

support_p9_supports_impl = support(
    [claim_p9_non_blocking_enhancement],
    claim_reference_implementation,
    reason=(
        "**P9 (@claim_p9_non_blocking_enhancement) is realized via async "
        "embedding generation in the reference implementation."
    ),
    prior=0.92,
)

# Table 10 of seven principles supports the structural-reuse principle (P1)
support_table10_supports_p1 = support(
    [claim_table10_seven_principles],
    claim_p1_structural_reuse,
    reason=(
        "**Table 10 (@claim_table10_seven_principles) lists the seven "
        "principles; P1 Structural Reuse is the architectural foundation "
        "for the unification thesis."
    ),
    prior=0.93,
)

# Letta concrete example also supports vs-Letta complementary; reuse via Letta
# components - already wired. So this is fine.

# Token compression supports the BYO-storage benefits and metadata-over-content principle
support_token_compression_supports_byo = support(
    [claim_token_compression_table],
    claim_byo_storage_benefits,
    reason=(
        "**Token compression (@claim_token_compression_table) is the "
        "operational realization of metadata-over-content: 40x-280x "
        "compression at storage time, compounding at retrieval time -- one "
        "of the BYO-storage benefits."
    ),
    prior=0.92,
)

# Versioned-KG lineage supports the AGM-correspondence thesis as historical
# context (the architectural primitives are well-established; the contribution
# is the *application* to cognitive memory + AGM correspondence)
support_versioned_kg_lineage = support(
    [claim_versioned_kg_lineage],
    claim_synthesis_underexplored,
    reason=(
        "**Versioned-KG systems exist (@claim_versioned_kg_lineage) targeting "
        "SPARQL knowledge management; their application to AI-agent memory "
        "with formal belief-revision correspondence is the underexplored "
        "synthesis Kumiho occupies."
    ),
    prior=0.9,
)
