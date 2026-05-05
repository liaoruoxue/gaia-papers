"""Priors for independent (leaf) claims in the 2604.24658 formalization.

Priors are calibrated against:

* The paper's own confidence framing (§10 Limitations: ML-only scope,
  source-fidelity ceiling, missing deployment prerequisites).
* Empirical observations grounded in published numbers (8,921
  PaperBench requirements; 24,008 RE-Bench runs; 450 paired
  understanding outcomes; 150 reproduction subtasks; 5 RE-Bench
  extension tasks).
* External commonly-accepted facts (FAIR / RO-Crate / nanopublications
  exist; LLM-judge pathologies are documented [@Zheng2023LLMJudge]).
* The Alt-A counter-hypothesis is calibrated by *explanatory power*
  (does Alt-A alone explain the +21.3pp/+7.0pp gaps? -- no, because
  same agent reads both formats).

Rules applied:

* Direct empirical measurements (PaperBench rubric, MALT, evaluation
  results) -> 0.92-0.96.
* Per-mechanism design claims (layer descriptions, Compiler stages,
  LRM principles) -> 0.85-0.90 (well-argued but inherently design
  judgments; no external corroboration of "this is the right
  decomposition").
* Per-table evaluation results (case studies, mutation benchmark,
  per-paper reproduction) -> 0.90-0.95.
* Existing-tool descriptions (Tools-row of Table 5; related-work
  threads) -> 0.93-0.95 (mechanically verifiable from cited papers).
* Limitations and future-work -> 0.92-0.95 (the paper's own
  acknowledgment of scope; the threats themselves are well-grounded).
* Prevailing-norm claim (PDFs are sufficient) -> 0.50 (near-uniform;
  let the contradiction operator do the work).
* Alt-A "agents-are-insufficient" alternative -> 0.25 (low; Alt-A's
  prediction of small ARA-vs-PDF gap is refuted by the data,
  especially Cat. C +65.7pp).
"""

from .motivation import (
    claim_alt_agent_capability_insufficient,
    claim_o3_frontier_llms_fail,
    claim_o4_pdf_information_gap,
    claim_o5_exploration_tax,
    claim_prevailing_norm_pdfs_sufficient,
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
    claim_layer_evidence,
    claim_layer_exploration,
    claim_layer_physical,
    claim_progressive_disclosure,
    claim_reproduction_taxonomy,
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
    claim_seven_event_types,
)
from .s4_compiler import (
    claim_compiler_failure_distribution,
    claim_high_fidelity_preservation,
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
)
from .s6_network import (
    claim_git_like_publishing,
    claim_paper_as_compiled_view,
    claim_renderable_to_any_surface,
)
from .s7_evaluation import (
    claim_case_restricted_mlm_4_5_4_6,
    claim_difficulty_stratification,
    claim_extension_late_phase_reversal,
    claim_extension_weaker_base_inverts,
    claim_reproduction_difficulty_growth,
    claim_reproduction_fabrication,
    claim_reproduction_per_paper_pattern,
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
)


PRIORS: dict = {
    # ---------------------------------------------------------------
    # Motivation: empirical observations + counter-hypothesis
    # ---------------------------------------------------------------
    claim_o3_frontier_llms_fail: (
        0.94,
        "<40% novel-contribution implementation rate is directly "
        "measured in ResearchCodeBench [@Hua2025ResearchCodeBench]; "
        "0.5% end-to-end on EXP-Bench [@Kon2025EXPBench]; semantic "
        "misalignment as dominant failure is documented in "
        "[@Jimenez2024SWEbench]. Mechanically verifiable from cited "
        "papers.",
    ),
    claim_o4_pdf_information_gap: (
        0.94,
        "Direct measurement on 8,921 PaperBench rubric requirements "
        "(Table 8). 64% of the headline 45.4% sufficient figure is "
        "high-confidence; methodology (LLM-as-judge with cited "
        "passages) is documented in App. E.2.",
    ),
    claim_o5_exploration_tax: (
        0.94,
        "Direct measurement on 24,008 METR MALT runs (Table 10). "
        "Per-task and per-difficulty breakdowns are in App. E.3; "
        "$63,483 total cost is published.",
    ),
    claim_trend1_ai_native_research: (
        0.92,
        "23.7-89.3% paper-production increase is from "
        "[@Kusumegi2025] (Science). The qualitative claim that "
        "agents now co-author research is well-documented "
        "[@Lu2024AIScientist].",
    ),
    claim_trend2_divergent_audiences: (
        0.93,
        "Human-attention scarcity is well-documented "
        "[@Renear2009]. Agents-benefit-from-context is implicit in "
        "every long-context-LLM benchmark.",
    ),
    claim_trend3_operability: (
        0.85,
        "Operability framing is the paper's own observation; the "
        "supporting evidence (Git-like artifact exchange) is "
        "[@Wang2026ArtifactExchange] but the broader claim about "
        "the bottleneck shifting is forward-looking.",
    ),
    claim_alt_agent_capability_insufficient: (
        0.25,
        "Alt-A's calculation (frontier LLMs are imperfect at "
        "novel-research implementation) is correct in absolute terms "
        "[@Jimenez2024SWEbench; @Hua2025ResearchCodeBench]. But "
        "pi(Alt) is 'can Alt *alone* explain Obs (the +21.3pp "
        "ARA-vs-PDF gap)?'. Since the same agent reads both formats, "
        "Alt-A predicts a small per-format gap; the data refutes "
        "this. Cat. C (+65.7pp where format alone differs) is the "
        "decisive case Alt-A cannot accommodate. Low prior reflects "
        "*low explanatory power*, not low correctness of Alt-A's "
        "absolute claim.",
    ),
    claim_prevailing_norm_pdfs_sufficient: (
        0.50,
        "Near-uniform: the prevailing-norm claim is widely held in "
        "the publishing ecosystem and consistent with FAIR + ACM "
        "artifact badges. Set near 0.5 so the contradiction operator "
        "with the two-tax diagnosis drives the BP outcome rather "
        "than the prior.",
    ),
    # ---------------------------------------------------------------
    # s2 ARA Protocol design claims
    # ---------------------------------------------------------------
    claim_four_question_decomposition: (
        0.88,
        "The four agent-relevant questions (why/how/what was tried/"
        "what are the numbers) and their conflicting structural "
        "needs are well-argued; the structural conflict between "
        "claim-stability and code-iteration is mechanically "
        "demonstrable. Slightly below 0.9 because the choice of *four* "
        "(not three or five) is a design judgment.",
    ),
    claim_progressive_disclosure: (
        0.92,
        "The claim that PAPER.md's layer index turns linear scanning "
        "into indexed lookup is supported by the per-difficulty token "
        "profile in §7.2 (ARA tokens scale with question depth: "
        "61K T1 -> 96K T2 -> 153K T3) -- a directly measurable "
        "operational property.",
    ),
    claim_factual_density_requirement: (
        0.85,
        "Factual-density framing is the paper's own design "
        "principle, applied uniformly across LRM and Compiler. "
        "Verifiable by inspection of any ARA artifact; slightly below "
        "0.9 because 'maximizing information per token' is a "
        "qualitative target.",
    ),
    claim_layer_physical: (
        0.88,
        "Two-mode (kernel/repo) Physical Layer design is well-"
        "motivated by the algorithmic-vs-systemic contribution "
        "distinction. The 1-2 orders-of-magnitude size reduction is "
        "a directly inspectable property. Below 0.9 because the "
        "binary mode choice is a design simplification.",
    ),
    claim_layer_exploration: (
        0.9,
        "Five-typed-node DAG with dead_end preservation is the "
        "concrete schema (Figure 5). The protocol is fully "
        "specified in App. A.3 and instantiated in the paper's own "
        "94-node ARA.",
    ),
    claim_layer_evidence: (
        0.92,
        "Outputs-only Evidence Layer with claim->experiment->"
        "evidence proof chain is mechanically enforced via Seal L1 "
        "cross-layer reference resolution. The blind-verification "
        "use case (App. E.1, §7.3) operationalizes the access-control "
        "separation.",
    ),
    claim_forensic_bindings: (
        0.92,
        "Cross-layer forensic bindings are validated by Seal L1 "
        "schema checks; the binding rules are concrete and "
        "mechanically testable. The 95.6% Cat. A accuracy on "
        "L1-gated artifacts confirms operational validity.",
    ),
    claim_capability_relative_sufficiency: (
        0.9,
        "Sufficiency-as-capability-relative is a clean philosophical "
        "framing; the paper's own statement that 'a complete ARA is "
        "reproducible by definition at the limit' is logically "
        "consistent. Below 0.95 because the operational threshold "
        "for 'sufficiently-capable' is itself unmeasured.",
    ),
    claim_reproduction_taxonomy: (
        0.92,
        "Direct empirical taxonomy from 3,050 leaf rubric "
        "requirements across 5 PaperBench papers (Table 6). The "
        "category labels are author-assigned but the percentages are "
        "mechanical counts.",
    ),
    claim_combinatorial_explosion_dominant: (
        0.92,
        "24.1% from Table 6 is a direct count. The framing 'this is "
        "the dominant challenge, not hyperparameters' is the paper's "
        "interpretation; the relative magnitudes (24.1% vs. 17.2% "
        "hyperparameters) are mechanical.",
    ),
    claim_high_weight_requires_understanding: (
        0.93,
        "Weight-2 requirements correspond to Result Interpretation "
        "is a direct property of the PaperBench rubric "
        "[@Starace2025PaperBench]. The claim is mechanically "
        "verifiable.",
    ),
    # ---------------------------------------------------------------
    # s3 Live Research Manager
    # ---------------------------------------------------------------
    claim_ai_native_research_paradigm: (
        0.92,
        "AI-native research paradigm is well-documented "
        "[@Lu2024AIScientist; @Kusumegi2025]. The claim that the "
        "trajectory is 'born textual' is verifiable by inspecting any "
        "researcher-Claude conversation log.",
    ),
    claim_prior_efforts_failed: (
        0.92,
        "Negative-result journals [@Matosin2014NegativeResults] and "
        "registered reports [@Chambers2013RegisteredReports] "
        "documented historical failures; the diagnosis "
        "(documentation-as-extra-burden) is the consensus reading.",
    ),
    claim_p1_silent_integration: (
        0.88,
        "Implementation as agent-skill [@Anthropic2025Skills] is "
        "verifiable. Below 0.92 because 'silent integration' is "
        "design-aspirational; the paper's own ARA validates it works "
        "in one author's workflow but generalization to all coding "
        "agents is asserted, not measured.",
    ),
    claim_p2_epistemic_provenance: (
        0.88,
        "Provenance tagging (user / ai-suggested / ai-executed / "
        "user-revised) and 'never auto-promote' are concrete "
        "protocol rules. Below 0.92 because the *faithfulness* of "
        "the resulting epistemic record is itself difficult to "
        "verify externally.",
    ),
    claim_p3_comprehensive_capture: (
        0.88,
        "Trajectory capture at session-time + version-controlled "
        "snapshots is concrete. The 114-node DAG in the paper's own "
        "ARA (App. A.3) is direct evidence the principle is "
        "operable.",
    ),
    claim_seven_event_types: (
        0.92,
        "Table 1 specifies the seven event types and structured "
        "payloads. The taxonomy is mechanically applicable to any "
        "captured event.",
    ),
    claim_closure_signals: (
        0.85,
        "Four-signal taxonomy (topic abandonment, verbal "
        "affirmation, empirical resolution, artifact commitment) is "
        "well-motivated and concrete. Below 0.9 because the k=5 "
        "default for topic abandonment is parameter-tunable, and the "
        "calibration of 'verbal affirmation' detection is heuristic.",
    ),
    claim_contradiction_handling: (
        0.88,
        "Defer-rather-than-overwrite contradiction handling is a "
        "clean protocol rule directly written into the manager skill. "
        "Mechanical.",
    ),
    claim_cross_session_continuity: (
        0.88,
        "PM reasoning log + key-context fields are concrete "
        "mechanisms; the paper's own pm_reasoning_log.yaml in App. "
        "A.3 is direct evidence.",
    ),
    claim_paper_is_an_ara: (
        0.95,
        "Direct artifact: 16 claims, 23 heuristics, 114-node DAG, 38 "
        "session logs, 94 staged observations are listed in App. A.3 "
        "with file paths. Mechanically verifiable from the "
        "supplementary `ara/` directory [@ARARepo].",
    ),
    # ---------------------------------------------------------------
    # s4 Compiler
    # ---------------------------------------------------------------
    claim_universal_input_canonical_output: (
        0.9,
        "Many-to-one design with graceful degradation is "
        "mechanically demonstrated by the 30 ARA evaluation corpus "
        "(23 PaperBench + 7 RE-Bench), all converging to Level-1 "
        "pass. The graceful-degradation property is logically "
        "verifiable.",
    ),
    claim_high_fidelity_preservation: (
        0.88,
        "The 96.7% Cat. A PaperBench accuracy (Table 3) is direct "
        "evidence of high fidelity on PDF-recoverable information. "
        "The 'every-source-fact must appear' rule is mechanically "
        "stated; whether it holds across all papers is bounded by the "
        "Compiler's actual extraction quality.",
    ),
    claim_knowledge_lineage_not_extraction: (
        0.88,
        "Forensic-reconstruction framing is the paper's diagnostic "
        "of why plain Markdown extraction is insufficient. The "
        "mechanism (cross-layer binding inference from prose, figure "
        "captions, code comments) is well-described in §4.2 but its "
        "quantitative effect is implicit in the Cat. A/B/C results.",
    ),
    claim_top_down_four_stages: (
        0.9,
        "Four-stage workflow (deconstruct -> cognitive -> physical -> "
        "exploration) is the concrete skill specification reproduced "
        "in App. B.1. Mechanically verifiable from the released skill "
        "[@ARARepo].",
    ),
    claim_source_aware_enrichment: (
        0.88,
        "Source-aware routing (rubric -> /logic; trajectory -> "
        "/trace; cross-ARA -> collective_inference) is a concrete "
        "skill rule. Empirically validated by the per-source "
        "experiments (PaperBench rubric for Cat. B; MALT trajectories "
        "for Cat. C; collective-inference is described but not yet "
        "evaluated here).",
    ),
    claim_compiler_failure_distribution: (
        0.92,
        "Direct count over Compiler iterations on the 30-ARA corpus "
        "(App. H.2.1). 42%/31%/14%/8%/5% breakdown is mechanical.",
    ),
    # ---------------------------------------------------------------
    # s5 Review System
    # ---------------------------------------------------------------
    claim_p1_automate_mechanical: (
        0.93,
        "The review-load-vs-reviewer-pool growth gap is documented "
        "[@Aczel2021]. The principle that mechanical checks should "
        "precede human judgment is well-motivated.",
    ),
    claim_p2_reproducibility_foundational: (
        0.9,
        "Treating reproducibility as machine-verified rather than "
        "author-promised is consistent with [@Stodden2016] and the "
        "broader reproducibility-crisis literature. The "
        "operationalization via three-level Seal is concrete.",
    ),
    claim_seal_level1_structural: (
        0.94,
        "L1 specification is fully detailed in App. H.1; checks are "
        "deterministic Python. Mechanical.",
    ),
    claim_seal_level2_rigor: (
        0.85,
        "Six-dimension rubric is well-specified, but the "
        "mutation-benchmark results show a *known* blind spot "
        "(orphan experiments at 22%) and two LLM-judge pathologies. "
        "The auditor catches 82.6% overall, leaving 17.4% missed -- "
        "real but bounded.",
    ),
    claim_seal_level3_execution: (
        0.92,
        "Evidence-blinded directional reproduction is "
        "operationalized as the §7.3 protocol; the 64.4% reproduction "
        "rate is direct evidence Level 3 produces useful signal.",
    ),
    claim_seal_certificate: (
        0.9,
        "Certificate format (artifact ID, level, timestamp, env "
        "hash, per-claim outcomes) is concrete; the living-"
        "certificate property requires future-work infrastructure but "
        "is logically straightforward.",
    ),
    claim_seal_l1_empirical_validity: (
        0.94,
        "95.6% Cat. A accuracy on L1-gated artifacts is direct "
        "measurement; the 0/30 first-iteration pass rate confirms L1 "
        "is binding.",
    ),
    claim_rigor_auditor_mutation_results: (
        0.95,
        "Per-type detection rates (23/23, 23/23, 23/23, 21/23, "
        "5/23) are direct counts on the 23x5 mutation matrix; "
        "Table 14 provides per-paper data.",
    ),
    claim_llm_judge_pathologies: (
        0.92,
        "Both pathologies (grade inflation, finding-score "
        "decoupling) are mechanically observable in the auditor "
        "logs and consistent with [@Zheng2023LLMJudge]'s prior "
        "documentation.",
    ),
    claim_seal_l3_equals_reproduction: (
        0.94,
        "The protocol equivalence is direct: §5.2 L3 specification "
        "matches §7.3 ARA-condition protocol, with the 64.4% rate "
        "being the L3 verification rate.",
    ),
    # ---------------------------------------------------------------
    # s6 Network
    # ---------------------------------------------------------------
    claim_paper_as_compiled_view: (
        0.85,
        "Paper-as-compiled-view is a forward-looking design "
        "framing; the rendering capability is conceptually "
        "well-motivated but operational rendering at scale is "
        "future work.",
    ),
    claim_renderable_to_any_surface: (
        0.8,
        "On-demand rendering is conceptual; the four-layer ARA is "
        "mechanically renderable into prose by an LLM, but rendering "
        "to slides / video / interactive demo is asserted, not "
        "demonstrated.",
    ),
    claim_git_like_publishing: (
        0.82,
        "Git-like properties (fork, diff, merge, lineage) follow "
        "from the file-system-level format. Demonstrated in concept "
        "by Wang et al. 2026 [@Wang2026ArtifactExchange] but the "
        "scientific-commons-with-falling-cost framing is "
        "forward-looking.",
    ),
    # ---------------------------------------------------------------
    # s7 Evaluation
    # ---------------------------------------------------------------
    claim_understanding_overall: (
        0.95,
        "Direct measurement: 93.7% vs 72.4% on 450 paired "
        "outcomes. McNemar χ²=95.15, p<10⁻¹⁰. Per-Cat. and per-"
        "benchmark breakdowns in Table 3.",
    ),
    claim_difficulty_stratification: (
        0.93,
        "Direct measurement on n={74, 193, 172, 26} per tier (App. "
        "E.5). The monotonic gap-widening is the predicted pattern "
        "of progressive disclosure.",
    ),
    claim_reproduction_difficulty_growth: (
        0.94,
        "Per-difficulty rates (85.1/68.5/54.5 vs 80.2/62.9/46.0) "
        "are direct measurements; Figure 11 visualises.",
    ),
    claim_reproduction_per_paper_pattern: (
        0.93,
        "Per-paper deltas (Figure 13, Table 11) are direct "
        "measurements; 'fre' / 'mech-und' / 'pinn' as largest wins is "
        "mechanically verifiable.",
    ),
    claim_reproduction_fabrication: (
        0.94,
        "Three runs, all detected by the blinded judge; "
        "mechanically counted from the per-paper logs.",
    ),
    claim_extension_late_phase_reversal: (
        0.93,
        "Direct trajectory observation on triton_cumsum and "
        "restricted_mlm under Sonnet 4.6; case studies in App. G.6 "
        "include trace.jsonl evidence.",
    ),
    claim_extension_weaker_base_inverts: (
        0.9,
        "Direct measurement on Sonnet 4.5 paired runs (Figs. 14, "
        "15). Sample size is small (1 seed/arm/task) so the "
        "*inversion* is well-supported but the magnitude is "
        "narrow-window.",
    ),
    claim_case_restricted_mlm_4_5_4_6: (
        0.92,
        "Direct trajectory observation: 4 paired runs, "
        "model-by-model architectural divergence is mechanically "
        "verifiable from final solution/model.py files (47 KB / "
        "6+ classes for ARA-4.6 vs 6.3 KB / 2 classes for "
        "paper-4.6).",
    ),
    # ---------------------------------------------------------------
    # s8 Related work threads (each thread is a description of an
    # existing literature)
    # ---------------------------------------------------------------
    claim_dimensional_gap_table: (
        0.92,
        "Table 5's PDF/GitHub/Tracker dimension assignments are the "
        "paper's analytical reading. The claim that 'no existing "
        "tool covers all 5 dimensions' is mechanically verifiable for "
        "the listed tools.",
    ),
    claim_machine_readable_thread: (
        0.94,
        "Direct citation list of 8 documents (FAIR / PROV / Canini / "
        "Stocker / Booeshaghi / nanopublications / ORKG / RO-Crate / "
        "Whole Tale / Discovery Engine). All cited papers exist and "
        "describe what is claimed.",
    ),
    claim_reproducibility_infra_thread: (
        0.94,
        "Direct citation list (Baker / Pineau / Stodden / Knuth / "
        "Rule / Köster / Di Tommaso / Crusoe / EXP-Bench / Wadden / "
        "Baumgärtner). The 0.5% EXP-Bench and <46% LLM-discrepancy-"
        "detection numbers are from cited papers.",
    ),
    claim_negative_knowledge_thread: (
        0.93,
        "Citation list (Zhu / Zhang / Yang / Wijk / Yamada). The "
        "claim 'failure traces become actionable only when annotated "
        "with root-cause structure' is the consensus reading of [@Zhu2025; "
        "@Zhang2025AgenTracer].",
    ),
    claim_agent_tooling_thread: (
        0.94,
        "Citation list and the <40% / 10.9% / SWE-bench / SWE-agent "
        "/ Voyager / AutoGen / AGENTS.md numbers are mechanical from "
        "cited papers.",
    ),
    # ---------------------------------------------------------------
    # s9 Limitations + Future work
    # ---------------------------------------------------------------
    claim_lim_evaluation_scope: (
        0.95,
        "ML-only scope is a documented fact about the corpus "
        "(Table 7: ICML 2024 papers + RE-Bench). The threat itself "
        "is well-acknowledged.",
    ),
    claim_lim_fidelity_ceiling: (
        0.93,
        "Source-fidelity bound is logically tight: no extraction "
        "method can recover information not in the source. The "
        "AI-native-workflow assumption for the LRM pathway is a "
        "documented constraint.",
    ),
    claim_lim_deployment_prerequisites: (
        0.94,
        "Both gaps (sandboxing/access-control; major-revision "
        "schema migration) are explicitly documented as future "
        "work. The minor-revision-only validation is a fact about "
        "the current implementation.",
    ),
    claim_fw_lineage: (
        0.88,
        "Lineage-as-diff is well-motivated by the analogy to git "
        "and is consistent with [@Wang2026ArtifactExchange]. The "
        "self-maintaining-ecosystem framing is forward-looking but "
        "logically continuous.",
    ),
    claim_fw_knowledge_graph: (
        0.85,
        "Cross-artifact knowledge-graph framing is forward-looking. "
        "Knowledge-graph approaches like Discovery Engine "
        "[@Baulin2025DiscoveryEngine] and ORKG [@Jaradeh2019ORKG] "
        "make the direction plausible but the *claim-confidence-"
        "surface* model is conceptual.",
    ),
    claim_fw_cross_disciplinary: (
        0.78,
        "Cross-disciplinary generalization is the most speculative "
        "future-work item. Cognitive/Evidence Layers are plausibly "
        "domain-agnostic, but Physical/Exploration extension to "
        "wet-lab is honestly flagged as 'requires substantial "
        "adaptation'.",
    ),
}
