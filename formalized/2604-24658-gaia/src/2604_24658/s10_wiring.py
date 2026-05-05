"""Pass-2 wiring: connect claims with reasoning strategies.

This module contains *only* strategies (support/abduction/induction/
contradiction). It is not a section of the paper; it formalizes the
inference structure connecting the claims defined in motivation through
s9_limitations.

Wiring philosophy:

* Empirical observations (O3, O4, O5) support the two-tax diagnosis
  (Storytelling + Engineering Tax).
* The two taxes jointly support the thesis that structural format,
  not agent capability, is the binding constraint.
* The four ARA layers are *responses* to the four agent-relevant
  questions and the two taxes.
* The three evaluation layers (Understanding / Reproduction /
  Extension) are independent confirmations of the same artifact-format
  hypothesis -> chained `induction` over the three layers.
* The central thesis is an `abduction` against Alt-A ("agents are
  insufficient regardless of format"); the comparison is anchored by
  the per-category gaps disappearing when the trace exists in ARA but
  not in baseline (Cat. C +65.7pp).
* Two `contradiction` operators capture: (i) the prevailing norm
  (PDFs are sufficient) vs. the diagnosis (the two taxes); (ii) Alt-A
  (agent-bound) vs. the thesis (artifact-bound).
"""

from gaia.lang import (
    abduction,
    compare,
    contradiction,
    induction,
    support,
)

from .motivation import (
    claim_alt_agent_capability_insufficient,
    claim_contrib_ara_protocol,
    claim_contrib_diagnose_two_taxes,
    claim_contrib_empirical_results,
    claim_contrib_three_mechanisms,
    claim_engineering_tax,
    claim_o3_frontier_llms_fail,
    claim_o4_pdf_information_gap,
    claim_o5_exploration_tax,
    claim_prevailing_norm_pdfs_sufficient,
    claim_storytelling_tax,
    claim_taxes_critical_for_agents,
    claim_trend1_ai_native_research,
    claim_trend2_divergent_audiences,
    claim_trend3_operability,
)
from .s2_ara_protocol import (
    claim_capability_relative_sufficiency,
    claim_combinatorial_explosion_dominant,
    claim_factual_density_requirement,
    claim_forensic_bindings,
    claim_four_question_decomposition,
    claim_high_weight_requires_understanding,
    claim_layer_cognitive,
    claim_layer_evidence,
    claim_layer_exploration,
    claim_layer_physical,
    claim_progressive_disclosure,
    claim_reproduction_taxonomy,
    claim_two_tax_response_mapping,
)
from .s3_live_research_manager import (
    claim_ai_native_research_paradigm,
    claim_closure_signals,
    claim_contradiction_handling,
    claim_cross_session_continuity,
    claim_p1_silent_integration,
    claim_p2_epistemic_provenance,
    claim_p3_comprehensive_capture,
    claim_paper_is_an_ara,
    claim_prior_efforts_failed,
    claim_progressive_crystallization,
    claim_seven_event_types,
    claim_three_stage_pipeline,
)
from .s4_compiler import (
    claim_compiler_failure_distribution,
    claim_high_fidelity_preservation,
    claim_iterative_validation,
    claim_knowledge_lineage_not_extraction,
    claim_source_aware_enrichment,
    claim_top_down_four_stages,
    claim_universal_input_canonical_output,
)
from .s5_review_system import (
    claim_llm_judge_pathologies,
    claim_p1_automate_mechanical,
    claim_p2_reproducibility_foundational,
    claim_rigor_auditor_mutation_results,
    claim_seal_certificate,
    claim_seal_l1_empirical_validity,
    claim_seal_l3_equals_reproduction,
    claim_seal_level1_structural,
    claim_seal_level2_rigor,
    claim_seal_level3_execution,
    claim_three_stage_review_pipeline,
)
from .s6_network import (
    claim_git_like_publishing,
    claim_paper_as_compiled_view,
    claim_renderable_to_any_surface,
)
from .s7_evaluation import (
    claim_case_fix_embedding,
    claim_case_restricted_mlm_4_5_4_6,
    claim_case_rust_codecontests,
    claim_difficulty_stratification,
    claim_extension_early_acceleration,
    claim_extension_late_phase_reversal,
    claim_extension_weaker_base_inverts,
    claim_headline_extension_outlook,
    claim_headline_three_layer_consistency,
    claim_reproduction_difficulty_growth,
    claim_reproduction_fabrication,
    claim_reproduction_overall,
    claim_reproduction_per_paper_pattern,
    claim_understanding_cat_a_fidelity,
    claim_understanding_cat_b_config,
    claim_understanding_cat_c_failure,
    claim_understanding_overall,
)
from .s8_related_work import (
    claim_agent_tooling_thread,
    claim_dimensional_gap_table,
    claim_machine_readable_thread,
    claim_negative_knowledge_thread,
    claim_reproducibility_infra_thread,
)
from .s9_limitations import (
    claim_fw_cross_disciplinary,
    claim_fw_knowledge_graph,
    claim_fw_lineage,
    claim_lim_deployment_prerequisites,
    claim_lim_evaluation_scope,
    claim_lim_fidelity_ceiling,
    claim_thesis,
)

# ---------------------------------------------------------------------------
# A. Empirical observations -> the two structural costs (Storytelling +
#    Engineering Taxes)
# ---------------------------------------------------------------------------

# A.1 Storytelling Tax: research-process erasure manifests as the
# below-reference exploration cost (90.2% of dollar; 113x failed/success
# token ratio) and as the wider literature on negative-result
# suppression.
strat_o5_supports_storytelling_tax = support(
    [claim_o5_exploration_tax],
    claim_storytelling_tax,
    reason=(
        "The 24,008-run RE-Bench analysis (@claim_o5_exploration_tax) "
        "concretely demonstrates the Storytelling Tax "
        "(@claim_storytelling_tax): 90.2% of dollar cost / 59.2% of "
        "tokens are spent below-reference, and the failure-record from "
        "those runs is *systematically discarded* by narrative "
        "compilation. The 113x failed-to-success token ratio is the "
        "per-task quantitative shadow of the qualitative Storytelling "
        "Tax claim. Without the 24,008-run dataset, the Storytelling "
        "Tax remains an intuition; with it, the cost has a number."
    ),
    prior=0.92,
)

# A.2 Engineering Tax: prose-vs-spec gap manifests as PaperBench's
# 45.4%-sufficient figure and as O3's <40% LLM implementation accuracy.
strat_o4_supports_engineering_tax = support(
    [claim_o4_pdf_information_gap, claim_o3_frontier_llms_fail],
    claim_engineering_tax,
    reason=(
        "The Engineering Tax (@claim_engineering_tax) -- the gap "
        "between reviewer-sufficient prose and agent-sufficient "
        "specification -- is empirically documented by two independent "
        "measurements: (i) PaperBench's 45.4%-sufficient figure across "
        "8,921 expert-authored requirements (@claim_o4_pdf_information_gap), "
        "showing that reproductive specifications themselves are "
        "absent from the reviewer-targeted prose; (ii) frontier LLMs "
        "implementing fewer than 40% of novel contributions correctly "
        "(@claim_o3_frontier_llms_fail), indicating that the absent "
        "specifications are exactly what blocks agent execution. The "
        "two measurements span both the artifact side and the "
        "consumer-execution side of the gap."
    ),
    prior=0.93,
)

# A.3 Both taxes are critical for AI agents because agent-execution
# uses precisely the discarded knowledge.
strat_taxes_critical = support(
    [claim_storytelling_tax, claim_engineering_tax,
     claim_o3_frontier_llms_fail],
    claim_taxes_critical_for_agents,
    reason=(
        "The two-tax diagnosis (@claim_storytelling_tax, "
        "@claim_engineering_tax) becomes empirically critical "
        "(@claim_taxes_critical_for_agents) when consumed by agents "
        "rather than humans: agent-execution requires precisely the "
        "discarded process knowledge (O5: failed exploration) and the "
        "missing specification detail (O4: 54.6% partial/absent), and "
        "the resulting end-to-end implementation accuracy is below 40% "
        "(@claim_o3_frontier_llms_fail) -- a level at which "
        "reproduction and extension cannot proceed reliably."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# B. The four-layer ARA architecture is the structural response to the
#    two taxes
# ---------------------------------------------------------------------------

# B.1 The four layers map directly to the four agent-relevant questions
# and to the two taxes
strat_four_layers_address_two_taxes = support(
    [claim_four_question_decomposition, claim_storytelling_tax,
     claim_engineering_tax, claim_layer_cognitive, claim_layer_physical,
     claim_layer_exploration, claim_layer_evidence],
    claim_two_tax_response_mapping,
    reason=(
        "The four-layer architecture mapping (@claim_two_tax_response_mapping) "
        "follows directly from (i) the four agent-relevant questions "
        "(@claim_four_question_decomposition) which require structurally-"
        "incompatible representations and (ii) the two taxes "
        "(@claim_storytelling_tax, @claim_engineering_tax) which name "
        "the specific failure modes that flat-narrative cannot address. "
        "Each layer materializes one question with the right structural "
        "form: Cognitive (@claim_layer_cognitive) for *why*, Physical "
        "(@claim_layer_physical) for *how*, Exploration "
        "(@claim_layer_exploration) for *what was tried*, Evidence "
        "(@claim_layer_evidence) for *what are the numbers*."
    ),
    prior=0.92,
)

# B.2 The layer decomposition is informed by the 10-category
# reproduction taxonomy
strat_taxonomy_supports_layer_design = support(
    [claim_reproduction_taxonomy, claim_combinatorial_explosion_dominant,
     claim_high_weight_requires_understanding],
    claim_two_tax_response_mapping,
    reason=(
        "The 10-category reproduction-critical taxonomy "
        "(@claim_reproduction_taxonomy), with its non-trivial "
        "combinatorial-matrix dominance "
        "(@claim_combinatorial_explosion_dominant) and the weight-2 "
        "requirements demanding result-interpretation understanding "
        "(@claim_high_weight_requires_understanding), is the empirical "
        "basis for assigning each information category to a primary "
        "ARA layer (@claim_two_tax_response_mapping). The taxonomy "
        "validates that the four layers cover the breadth of "
        "reproduction-critical knowledge rather than being chosen "
        "arbitrarily."
    ),
    prior=0.88,
)

# B.3 Forensic bindings are the structural feature that distinguishes ARA
# from existing tools (Table 5 dimensional gap)
strat_forensic_bindings_close_dimensional_gap = support(
    [claim_forensic_bindings, claim_dimensional_gap_table],
    claim_contrib_ara_protocol,
    reason=(
        "ARA's claim that it provides what existing tools do not "
        "(@claim_contrib_ara_protocol) rests on the dimensional gap "
        "(@claim_dimensional_gap_table) -- existing tools each cover "
        "≤2 of the 5 dimensions, and *none* provide cross-layer "
        "bindings -- and on the forensic-binding mechanism "
        "(@claim_forensic_bindings) that machine-validates "
        "claim<->code<->evidence linkage at Seal Level 1."
    ),
    prior=0.9,
)

# B.4 The contribution-1 (the diagnosis) follows from the empirical
# observations + the gap to existing tools
strat_diagnosis_from_observations = support(
    [claim_o4_pdf_information_gap, claim_o5_exploration_tax,
     claim_storytelling_tax, claim_engineering_tax,
     claim_dimensional_gap_table],
    claim_contrib_diagnose_two_taxes,
    reason=(
        "The diagnosis-contribution (@claim_contrib_diagnose_two_taxes) "
        "is supported by (a) two large-scale empirical measurements "
        "(@claim_o4_pdf_information_gap covering 8,921 reproduction "
        "requirements, @claim_o5_exploration_tax covering 24,008 "
        "agent runs); (b) the two-tax framing "
        "(@claim_storytelling_tax, @claim_engineering_tax) that "
        "explains *why* both observations are structural rather than "
        "incidental; and (c) the dimensional gap "
        "(@claim_dimensional_gap_table) that shows existing tools do "
        "not address the same failure modes."
    ),
    prior=0.92,
)

# B.5 The four-layer protocol contribution
strat_protocol_from_layers = support(
    [claim_layer_cognitive, claim_layer_physical, claim_layer_exploration,
     claim_layer_evidence, claim_forensic_bindings,
     claim_two_tax_response_mapping],
    claim_contrib_ara_protocol,
    reason=(
        "Contribution 2 (the four-layer protocol with forensic "
        "bindings, @claim_contrib_ara_protocol) is the conjunction of "
        "the four layer designs (@claim_layer_cognitive, "
        "@claim_layer_physical, @claim_layer_exploration, "
        "@claim_layer_evidence), the forensic-binding mechanism "
        "(@claim_forensic_bindings), and the structural mapping to "
        "the two taxes (@claim_two_tax_response_mapping) which is the "
        "design rationale that ties the four layers into a coherent "
        "protocol rather than four arbitrary directories."
    ),
    prior=0.9,
)

# B.6 Progressive disclosure + factual density are layer-internal
# properties that strengthen Cognitive Layer effectiveness
strat_progressive_disclosure_supports_cognitive = support(
    [claim_progressive_disclosure, claim_factual_density_requirement],
    claim_layer_cognitive,
    reason=(
        "The Cognitive Layer (@claim_layer_cognitive) achieves its "
        "agent-utility because it ships with two operational "
        "properties: progressive disclosure "
        "(@claim_progressive_disclosure) -- the layer index turns "
        "linear scanning into targeted lookup -- and factual-density "
        "(@claim_factual_density_requirement) -- subjective qualifiers "
        "are stripped, statements carry provenance. Together these "
        "make the layer agent-readable rather than merely "
        "agent-targeted."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# C. The three enabling mechanisms (LRM, Compiler, Review System)
# ---------------------------------------------------------------------------

# C.1 LRM design follows from the AI-native paradigm + prior failures
strat_lrm_principles_from_paradigm = support(
    [claim_ai_native_research_paradigm, claim_prior_efforts_failed,
     claim_p1_silent_integration, claim_p2_epistemic_provenance,
     claim_p3_comprehensive_capture],
    claim_three_stage_pipeline,
    reason=(
        "The three-stage Live Research Manager pipeline "
        "(@claim_three_stage_pipeline) is the system response to "
        "(a) the AI-native paradigm (@claim_ai_native_research_paradigm) "
        "that makes the trajectory machine-readable and "
        "(b) the historical failure of process-preservation efforts "
        "(@claim_prior_efforts_failed) that demanded extra researcher "
        "labour. Three design principles (@claim_p1_silent_integration "
        "for portability, @claim_p2_epistemic_provenance for trustable "
        "provenance, @claim_p3_comprehensive_capture for trajectory "
        "completeness) translate the constraint set into the Context "
        "Harvester / Event Router / Maturity Tracker architecture."
    ),
    prior=0.88,
)

# C.2 Closure-signals + contradiction-handling support progressive
# crystallization
strat_closure_signals_support_crystallization = support(
    [claim_closure_signals, claim_contradiction_handling],
    claim_progressive_crystallization,
    reason=(
        "Progressive crystallization (@claim_progressive_crystallization) "
        "is operationally realised by the closure-signal taxonomy "
        "(@claim_closure_signals), which provides externally-verifiable "
        "maturity criteria, and by the contradiction-handling protocol "
        "(@claim_contradiction_handling), which preserves epistemic "
        "integrity when evidence accumulates non-monotonically."
    ),
    prior=0.88,
)

# C.3 Cross-session continuity feeds the pipeline's effectiveness
strat_cross_session_supports_pipeline = support(
    [claim_cross_session_continuity, claim_seven_event_types,
     claim_progressive_crystallization],
    claim_three_stage_pipeline,
    reason=(
        "The three-stage pipeline (@claim_three_stage_pipeline) "
        "operates faithfully across multi-session research projects "
        "because (i) cross-session continuity is preserved via the PM "
        "reasoning log + key-context fields "
        "(@claim_cross_session_continuity), (ii) the seven event "
        "types (@claim_seven_event_types) provide the structured "
        "vocabulary the Event Router classifies into, and (iii) "
        "progressive crystallization "
        "(@claim_progressive_crystallization) is the temporal "
        "discipline that prevents premature structure."
    ),
    prior=0.88,
)

# C.4 The paper itself being an ARA is direct empirical support that
# the LRM design works
strat_self_ara_supports_lrm = support(
    [claim_paper_is_an_ara],
    claim_three_stage_pipeline,
    reason=(
        "Direct empirical evidence: the paper itself ships an ARA "
        "(@claim_paper_is_an_ara, with 16 claims, 23 heuristics, "
        "114-node DAG, 38 sessions) produced by the Live Research "
        "Manager (@claim_three_stage_pipeline). Self-application is "
        "non-trivial evidence the system is operable on a paper-scale "
        "project."
    ),
    prior=0.85,
)

# C.5 Compiler design follows from its three principles
strat_compiler_principles_to_stages = support(
    [claim_universal_input_canonical_output, claim_high_fidelity_preservation,
     claim_knowledge_lineage_not_extraction, claim_top_down_four_stages,
     claim_iterative_validation, claim_source_aware_enrichment],
    claim_contrib_three_mechanisms,
    reason=(
        "The Compiler half of contribution 3 "
        "(@claim_contrib_three_mechanisms) is supported by its three "
        "design principles: universal input "
        "(@claim_universal_input_canonical_output), high-fidelity "
        "preservation (@claim_high_fidelity_preservation), and "
        "knowledge lineage (@claim_knowledge_lineage_not_extraction); "
        "and by their realization as the four-stage top-down generator "
        "(@claim_top_down_four_stages) with in-loop Seal-L1 validation "
        "(@claim_iterative_validation) and source-aware enrichment "
        "(@claim_source_aware_enrichment)."
    ),
    prior=0.88,
)

# C.6 In-loop validation observation: 0/30 first-iteration pass rate +
# Compiler failure distribution support the iterative-validation claim
strat_compiler_failure_supports_validation = support(
    [claim_compiler_failure_distribution],
    claim_iterative_validation,
    reason=(
        "The Compiler iterative-validation claim "
        "(@claim_iterative_validation) is empirically supported by the "
        "non-trivial failure distribution "
        "(@claim_compiler_failure_distribution): 42% dangling refs, "
        "31% schema gaps, 14% insufficient nodes -- a *structured* "
        "distribution that confirms Level 1 catches genuine structural "
        "deficits rather than rubber-stamping every output. The 0/30 "
        "first-iteration pass rate further confirms Level 1 is the "
        "binding filter."
    ),
    prior=0.9,
)

# C.7 Review-system design follows from its principles
strat_review_principles_to_stages = support(
    [claim_p1_automate_mechanical, claim_p2_reproducibility_foundational,
     claim_seal_level1_structural, claim_seal_level2_rigor,
     claim_seal_level3_execution, claim_seal_certificate,
     claim_three_stage_review_pipeline],
    claim_contrib_three_mechanisms,
    reason=(
        "The Review System half of contribution 3 "
        "(@claim_contrib_three_mechanisms) is supported by its two "
        "principles (@claim_p1_automate_mechanical, "
        "@claim_p2_reproducibility_foundational) and their realization "
        "as the three Seal levels (@claim_seal_level1_structural, "
        "@claim_seal_level2_rigor, @claim_seal_level3_execution) "
        "issuing a Seal Certificate (@claim_seal_certificate) consumed "
        "by the three-stage review pipeline "
        "(@claim_three_stage_review_pipeline)."
    ),
    prior=0.88,
)

# C.8 Mutation benchmark + LLM-judge pathologies + L3=reproduction
# substantiate the Review System empirically
strat_review_empirical_substantiation = support(
    [claim_seal_l1_empirical_validity,
     claim_rigor_auditor_mutation_results, claim_llm_judge_pathologies,
     claim_seal_l3_equals_reproduction],
    claim_three_stage_review_pipeline,
    reason=(
        "The three-stage review pipeline "
        "(@claim_three_stage_review_pipeline) has direct empirical "
        "validation: L1's effectiveness is witnessed by 95.6% Cat. A "
        "accuracy on L1-gated artifacts (@claim_seal_l1_empirical_validity); "
        "L2's Rigor Auditor catches 82.6% of mutations across 5 "
        "injection types (@claim_rigor_auditor_mutation_results) with "
        "a *characterised* blind spot (orphan experiments); known "
        "LLM-judge pathologies (@claim_llm_judge_pathologies) prescribe "
        "the deterministic-finding-aggregation fix; and L3's 64.4% "
        "reproduction rate (@claim_seal_l3_equals_reproduction) "
        "operationalizes execution-reproducibility on well-formed "
        "artifacts."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# D. Three trends -> the (Human+AI)^2 network
# ---------------------------------------------------------------------------

strat_trends_to_network = support(
    [claim_trend1_ai_native_research, claim_trend2_divergent_audiences,
     claim_trend3_operability, claim_paper_as_compiled_view,
     claim_renderable_to_any_surface, claim_git_like_publishing],
    claim_contrib_three_mechanisms,
    reason=(
        "The (Human+AI)² network framing "
        "(@claim_contrib_three_mechanisms) follows from three trends: "
        "AI-native research (@claim_trend1_ai_native_research) makes "
        "the trajectory free; divergent audiences "
        "(@claim_trend2_divergent_audiences) makes single-format "
        "compromise structurally untenable; and operability "
        "(@claim_trend3_operability) elevates the artifact format from "
        "convenience to bottleneck. The network's three observable "
        "properties -- the paper becomes a compiled view "
        "(@claim_paper_as_compiled_view), the artifact renders to any "
        "surface (@claim_renderable_to_any_surface), and publishing "
        "becomes Git-like (@claim_git_like_publishing) -- follow from "
        "those trends."
    ),
    prior=0.85,
)

# ---------------------------------------------------------------------------
# E. Evaluation: three induction layers (understanding / reproduction /
#    extension) over the artifact-format hypothesis
# ---------------------------------------------------------------------------

# E.1 Understanding: the three category gains (Cat. A / B / C) are three
# independent confirmations that ARA outperforms baseline on
# information extraction. We compose them into an induction.

# Each Cat. result is a `support([format_hypothesis], category_gain)`:
# the artifact-format hypothesis is that ARA's structural layers
# preserve information narrative discards, and each category's measured
# gain is the predicted observable consequence.
support_cat_a = support(
    [claim_contrib_ara_protocol],
    claim_understanding_cat_a_fidelity,
    reason=(
        "The ARA protocol (@claim_contrib_ara_protocol) predicts that "
        "the layer-indexed structure should beat linear PDF scanning "
        "on PDF-recoverable questions; Cat. A "
        "(@claim_understanding_cat_a_fidelity, +14.8pp at -12% tokens) "
        "is the directional confirmation."
    ),
    prior=0.88,
)
support_cat_b = support(
    [claim_contrib_ara_protocol],
    claim_understanding_cat_b_config,
    reason=(
        "The ARA protocol (@claim_contrib_ara_protocol) predicts that "
        "centralized configs (`src/configs/`) should beat repo-mining "
        "on configuration questions; Cat. B "
        "(@claim_understanding_cat_b_config, +24.8pp on PaperBench "
        "configuration recovery) is the directional confirmation."
    ),
    prior=0.9,
)
support_cat_c = support(
    [claim_contrib_ara_protocol],
    claim_understanding_cat_c_failure,
    reason=(
        "The ARA protocol (@claim_contrib_ara_protocol) predicts that "
        "the Exploration Graph (`/trace`) should beat PDFs that have "
        "no analogue for failure knowledge; Cat. C "
        "(@claim_understanding_cat_c_failure, +65.7pp -- the largest "
        "single accuracy gap in the evaluation) is the directional "
        "confirmation, and is the cleanest test because the baseline "
        "has no source for failure knowledge."
    ),
    prior=0.95,
)

induction_understanding_ab = induction(
    support_cat_a, support_cat_b,
    law=claim_contrib_ara_protocol,
    reason=(
        "Cat. A and Cat. B test independent ARA mechanisms "
        "(progressive disclosure vs centralized configs) on different "
        "question pools (general fidelity vs configuration recovery), "
        "so they are conditionally independent confirmations of the "
        "ARA protocol (@claim_contrib_ara_protocol)."
    ),
)
induction_understanding_abc = induction(
    induction_understanding_ab, support_cat_c,
    law=claim_contrib_ara_protocol,
    reason=(
        "Cat. C tests the Exploration Graph -- a *third* independent "
        "ARA mechanism (failure-knowledge preservation) -- on the "
        "RE-Bench task corpus disjoint from Cat. A/B's PaperBench "
        "papers. Adding Cat. C to the Cat. A+B induction is a third "
        "conditionally-independent confirmation of "
        "(@claim_contrib_ara_protocol)."
    ),
)

# E.2 The three-category aggregation directly supports the headline
# Understanding result
strat_understanding_overall_from_cats = support(
    [claim_understanding_cat_a_fidelity, claim_understanding_cat_b_config,
     claim_understanding_cat_c_failure, claim_difficulty_stratification],
    claim_understanding_overall,
    reason=(
        "The headline +21.3pp Understanding result "
        "(@claim_understanding_overall) decomposes additively into the "
        "three category gains (@claim_understanding_cat_a_fidelity "
        "+14.8pp; @claim_understanding_cat_b_config +24.8pp; "
        "@claim_understanding_cat_c_failure +65.7pp). The internal-"
        "consistency check is the difficulty stratification "
        "(@claim_difficulty_stratification), which shows the gap "
        "widens as questions become harder -- the structural "
        "prediction of progressive disclosure."
    ),
    prior=0.95,
)

# E.3 Reproduction: per-difficulty growth + fabrication observation
# substantiate the headline reproduction win
strat_reproduction_overall = support(
    [claim_reproduction_difficulty_growth,
     claim_reproduction_per_paper_pattern,
     claim_reproduction_fabrication],
    claim_reproduction_overall,
    reason=(
        "The headline reproduction result "
        "(@claim_reproduction_overall, ARA 64.4% vs BL 57.4% "
        "weighted, p=0.028) decomposes into the per-difficulty growth "
        "(@claim_reproduction_difficulty_growth, gap monotonic "
        "+4.9/+5.6/+8.5pp) and the per-paper pattern "
        "(@claim_reproduction_per_paper_pattern, largest gains on "
        "complex multi-stage pipelines, ties when companion repo is "
        "strong). The fabrication count "
        "(@claim_reproduction_fabrication, 2 BL + 1 ARA) bounds the "
        "honest ceiling: structured artifacts reduce but do not "
        "eliminate hallucination, and the blinded-result protocol is "
        "the necessary backstop."
    ),
    prior=0.92,
)

# E.4 Extension induction: case studies + early-acceleration
# observation jointly support the extension headline
support_extension_early = support(
    [claim_contrib_ara_protocol],
    claim_extension_early_acceleration,
    reason=(
        "The ARA protocol (@claim_contrib_ara_protocol) predicts that "
        "preserved trace + heuristics should let the next agent "
        "shortcut the diagnostic phase. Early-acceleration on all 5 "
        "RE-Bench tasks (@claim_extension_early_acceleration) is the "
        "predicted observable confirmation."
    ),
    prior=0.88,
)
support_extension_case_rust = support(
    [claim_contrib_ara_protocol],
    claim_case_rust_codecontests,
    reason=(
        "The `rust_codecontests` case study "
        "(@claim_case_rust_codecontests) is a clean attribution: an "
        "under-reference MALT data point becomes two heuristics that "
        "ARA agent acts on at t=9 min; paper agent rediscovers the "
        "same idea at t=395 min. The 6-hour compression is the "
        "predicted consequence of ARA's protocol "
        "(@claim_contrib_ara_protocol)."
    ),
    prior=0.85,
)
support_extension_case_fix = support(
    [claim_contrib_ara_protocol],
    claim_case_fix_embedding,
    reason=(
        "The `fix_embedding` case study (@claim_case_fix_embedding) "
        "isolates three behavioural differences -- absent permutation "
        "recovery, constrained LR-region search, MALT-anchored "
        "strategic confidence -- each attributable to a specific "
        "failure-record element present in ARA and absent from "
        "paper.md. This is the cleanest in-corpus attribution that "
        "the ARA protocol (@claim_contrib_ara_protocol) is causally "
        "active rather than incidentally correlated."
    ),
    prior=0.85,
)

induction_extension_pair = induction(
    support_extension_early, support_extension_case_rust,
    law=claim_contrib_ara_protocol,
    reason=(
        "Aggregate early-acceleration across 5 tasks and the rust case "
        "are conditionally-independent observations: the former "
        "averages over heterogeneous tasks, the latter is a "
        "fine-grained mechanism trace on one. Both confirm the ARA "
        "protocol's predicted effect."
    ),
)
induction_extension_triple = induction(
    induction_extension_pair, support_extension_case_fix,
    law=claim_contrib_ara_protocol,
    reason=(
        "Adding the fix_embedding case adds a *clean attribution* "
        "(only the failure record differs between paper and ARA "
        "bundles) -- a third conditionally-independent observation "
        "type. The induction over (aggregate effect, rust mechanism, "
        "fix_embedding attribution) reflects three independent angles "
        "on the same protocol-effect hypothesis "
        "(@claim_contrib_ara_protocol)."
    ),
)

strat_extension_outlook_supported = support(
    [claim_extension_late_phase_reversal,
     claim_extension_weaker_base_inverts,
     claim_case_restricted_mlm_4_5_4_6],
    claim_headline_extension_outlook,
    reason=(
        "The extension outlook (@claim_headline_extension_outlook) "
        "-- that trace value scales with the gap between documented "
        "content and agent bandwidth -- is supported by the "
        "Sonnet-4.6 reversals (@claim_extension_late_phase_reversal), "
        "the Sonnet-4.5 inversions of those reversals "
        "(@claim_extension_weaker_base_inverts), and the "
        "`restricted_mlm` flip across model versions "
        "(@claim_case_restricted_mlm_4_5_4_6, where the same "
        "mechanism wins on 4.5 but loses on 4.6)."
    ),
    prior=0.88,
)

# E.5 Three-layer headline consolidates the three evaluation results
strat_three_layer_consistency = support(
    [claim_understanding_overall, claim_reproduction_overall,
     claim_headline_extension_outlook],
    claim_headline_three_layer_consistency,
    reason=(
        "The three-layer cross-experiment headline "
        "(@claim_headline_three_layer_consistency) is the conjunction "
        "of (@claim_understanding_overall always wins), "
        "(@claim_reproduction_overall wins on aggregate), and "
        "(@claim_headline_extension_outlook with model-bandwidth-"
        "dependent caveat). The three layers are mutually "
        "interpretable: understanding is necessary for reproduction; "
        "reproduction is necessary for extension; the rising bar of "
        "ambition matches the empirically-observed rising "
        "qualification on ARA's win."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# F. The thesis: structural-format intervention closes a gap that agent-
#    capability alone would not. Abduction against Alt-A.
# ---------------------------------------------------------------------------

# Hypothesis support: the empirical gap on understanding/reproduction/
# extension is explained by the structural intervention claim
support_thesis = support(
    [claim_contrib_ara_protocol, claim_understanding_overall,
     claim_reproduction_overall, claim_extension_early_acceleration],
    claim_contrib_empirical_results,
    reason=(
        "Hypothesis branch (structural-format intervention closes the "
        "gap): the headline empirical gains "
        "(@claim_contrib_empirical_results) are the predicted "
        "observable consequence of the four-layer ARA protocol "
        "(@claim_contrib_ara_protocol). Each evaluation layer "
        "(@claim_understanding_overall, @claim_reproduction_overall, "
        "@claim_extension_early_acceleration) is a confirmation; the "
        "Cat. C +65.7pp gap is the cleanest test because failure "
        "knowledge has no analogue in the baseline and so cannot be "
        "explained by any agent-capability improvement."
    ),
    prior=0.92,
)

# Alternative support: if Alt-A held, the agent-bound limit would
# manifest equally in the ARA condition. But ARA-vs-baseline isolates
# format because the same agent reads both. Alt-A's predictions do not
# match.
support_alt_a = support(
    [claim_alt_agent_capability_insufficient],
    claim_contrib_empirical_results,
    reason=(
        "Alternative branch (Alt-A: agent capability is the binding "
        "constraint regardless of artifact format, "
        "@claim_alt_agent_capability_insufficient): under Alt-A, the "
        "ARA-vs-baseline gap should be small or zero because the same "
        "agent (Claude Sonnet 4.6) reads both. The actual gap of "
        "+21.3pp Understanding / +7.0pp Reproduction (especially Cat. "
        "C +65.7pp where format alone differs) shows Alt-A's "
        "explanatory power for the observed gains "
        "(@claim_contrib_empirical_results) is low -- *Alt-A predicts "
        "a small gap that the data refutes*. The prior for Alt-A "
        "*alone* explaining the observation is therefore low, even "
        "though Alt-A's calculation that agents are imperfect is "
        "correct."
    ),
    prior=0.25,  # pi(Alt) reflects explanatory power, not correctness
)

compare_thesis_vs_alt = compare(
    claim_contrib_ara_protocol,  # H's prediction (the protocol)
    claim_alt_agent_capability_insufficient,  # Alt's prediction
    claim_contrib_empirical_results,  # the observation
    reason=(
        "The hypothesis (@claim_contrib_ara_protocol, the four-layer "
        "structural-format intervention) and the alternative "
        "(@claim_alt_agent_capability_insufficient, agent-capability-"
        "bound) both attempt to explain the same observed gains "
        "(@claim_contrib_empirical_results). The decisive test is "
        "Cat. C (failure knowledge), where format alone differs and "
        "the gap is +65.7pp -- a magnitude Alt-A cannot accommodate. "
        "The McNemar χ²=95.15 (p<10⁻¹⁰) and per-difficulty monotonic "
        "growth corroborate. The hypothesis explains the Cat. C gap "
        "exactly (the trace is present in ARA, absent in baseline), "
        "while Alt-A would predict no per-format gap."
    ),
    prior=0.92,
)

abduction_thesis = abduction(
    support_thesis, support_alt_a, compare_thesis_vs_alt,
    reason=(
        "The central thesis abduction: the observed three-layer "
        "evaluation gains are best explained by the structural-format "
        "intervention (the four-layer ARA protocol) rather than by "
        "agent-capability variation. The Cat. C gap (failure knowledge "
        "structurally absent from PDF, structurally present in ARA) "
        "is the discriminating evidence: format-driven, not "
        "capability-driven."
    ),
)

# ---------------------------------------------------------------------------
# G. Two contradictions: prevailing-norm vs diagnosis; Alt-A vs thesis
# ---------------------------------------------------------------------------

# G.1 The prevailing norm (PDFs are sufficient for scientific
# communication) is contradicted by the two-tax diagnosis under
# agent-consumer assumption.
contra_norm_vs_diagnosis = contradiction(
    claim_prevailing_norm_pdfs_sufficient,
    claim_taxes_critical_for_agents,
    reason=(
        "The prevailing scientific-publishing norm "
        "(@claim_prevailing_norm_pdfs_sufficient) holds that PDF + "
        "(optional) repo + (optional) data is structurally adequate "
        "as the primary research artifact. The two-tax diagnosis "
        "applied to AI-agent consumers "
        "(@claim_taxes_critical_for_agents) holds the opposite: when "
        "agents are first-class consumers, the same format is "
        "structurally inadequate because the discarded knowledge "
        "(failed experiments, implementation tricks) is precisely "
        "what agents need to operate. The two cannot both hold of "
        "the same agent-consumer regime; the paper's "
        "evidence (O3, O4, O5; reproduction at 57.4% on PDF+repo) "
        "selects the diagnosis side."
    ),
    prior=0.95,
)

# G.2 The thesis is positively supported by the abduction conclusion +
# the empirical results; the abduction already does the work of
# preferring H over Alt-A. We additionally support thesis directly
# from contrib_empirical_results so it is anchored by the data, not
# just by future-work / limitations.
strat_thesis_from_results = support(
    [claim_contrib_empirical_results, claim_contrib_diagnose_two_taxes,
     claim_contrib_ara_protocol],
    claim_thesis,
    reason=(
        "The thesis (@claim_thesis) is the synthesis of the "
        "diagnosis (@claim_contrib_diagnose_two_taxes), the protocol "
        "response (@claim_contrib_ara_protocol), and the empirical "
        "validation (@claim_contrib_empirical_results). All three "
        "have high posterior belief from the rest of the graph, "
        "directly supporting the thesis that the two structural "
        "taxes (not agent capability) explain the artifact-format "
        "gap closed by ARA."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# H. Related-work threads each contribute a partial coverage
#    that ARA unifies; threads support the contribution of unification
# ---------------------------------------------------------------------------

strat_threads_support_unification = support(
    [claim_machine_readable_thread, claim_reproducibility_infra_thread,
     claim_negative_knowledge_thread, claim_agent_tooling_thread,
     claim_dimensional_gap_table],
    claim_contrib_ara_protocol,
    reason=(
        "ARA's contribution as a *unifying protocol* "
        "(@claim_contrib_ara_protocol) is supported by the four "
        "related-work threads each providing partial coverage: "
        "machine-readable artifacts (@claim_machine_readable_thread) "
        "lacks execution; reproducibility infrastructure "
        "(@claim_reproducibility_infra_thread) lacks claim semantics; "
        "negative-knowledge work (@claim_negative_knowledge_thread) "
        "remains raw; agent tooling (@claim_agent_tooling_thread) "
        "operates post-hoc. The dimensional table "
        "(@claim_dimensional_gap_table) makes the convergent gap "
        "explicit."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# I. Limitations + future work feed thesis qualification
# ---------------------------------------------------------------------------

strat_limits_qualify_thesis = support(
    [claim_lim_evaluation_scope, claim_lim_fidelity_ceiling,
     claim_lim_deployment_prerequisites, claim_capability_relative_sufficiency],
    claim_thesis,
    reason=(
        "The three explicit limitations qualify but do not undercut "
        "the thesis (@claim_thesis): (i) ML-only scope "
        "(@claim_lim_evaluation_scope) makes the thesis empirically "
        "valid for ML and structurally-extensible elsewhere; "
        "(ii) source-fidelity bound (@claim_lim_fidelity_ceiling) "
        "explains why Compiler-only ARAs inherit PDF omissions, "
        "preserving the LRM-pathway as the high-fidelity route; "
        "(iii) deployment prerequisites "
        "(@claim_lim_deployment_prerequisites) are operational rather "
        "than structural. The capability-relative sufficiency "
        "criterion (@claim_capability_relative_sufficiency) ensures "
        "the thesis is robust to agent-capability advances: a "
        "complete ARA is reproducible by definition at the limit."
    ),
    prior=0.85,
)

strat_future_work_supports_thesis = support(
    [claim_fw_lineage, claim_fw_knowledge_graph, claim_fw_cross_disciplinary],
    claim_thesis,
    reason=(
        "The three future-work directions extend the thesis "
        "(@claim_thesis): lineage (@claim_fw_lineage) addresses "
        "artifact decay; the cross-artifact knowledge graph "
        "(@claim_fw_knowledge_graph) lifts the unit of analysis from "
        "document to corpus; cross-disciplinary "
        "(@claim_fw_cross_disciplinary) extends scope. Each direction "
        "is logically continuous with the four-layer protocol and "
        "presupposes the thesis rather than depending on its "
        "verification."
    ),
    prior=0.78,
)
