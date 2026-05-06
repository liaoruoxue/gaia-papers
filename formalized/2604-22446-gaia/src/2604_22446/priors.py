"""Priors for independent (leaf) claims in the 2604.22446 OMC formalization.

Calibration philosophy
----------------------

* **Direct table / numerical readouts from the paper** (Table 2, Table 1,
  Table 4) -- 0.93-0.95. These are direct verbatim transcriptions from
  the published PDF; uncertainty is essentially transcription risk only.
* **Architectural design properties** (FSM invariants, AND-tree
  semantics, OS-kernel correspondence, six-interface design) -- 0.92-
  0.95. Read directly off the design + Algorithm 1 + the FSM diagram
  (Figure 5). The properties are structural, not empirical.
* **Method-description claims for related-work characterisations**
  (heterogeneity-only-at-model-level, dynamic-decomposition-landscape,
  individual-evolution-landscape, organisation-evolution-
  underdeveloped, protocol-and-marketplace-landscape, team-composition-
  spectrum) -- 0.88-0.92. Author paraphrases of competing-method
  capabilities; the cited papers are real and reasonably checked but
  any literature paraphrase carries small interpretation risk.
* **Three-design-aspects of OMC contributing to the gain** (D1 dynamic
  decomposition / D2 review gate / D3 cross-family recruitment) --
  0.9. Read off Section 3.2 attribution; uncontroversial reading of
  the design.
* **Diagnosis-level claims** (skills-within-agent-only, existing-MAS-
  three-limits, dynamic-workflow-still-bounded) -- 0.88-0.9. These
  are the diagnostic premises driving the missing-organisation-layer
  argument; well-supported by the cited frameworks but contain
  rhetorical compression of nuance.
* **Predicted-fingerprint claims for the central abduction** -- pi(H)
  = 0.7 for organisational-decoupling, pi(Alt) = 0.15 for
  bigger-LM/more-compute. The alternative's prior reflects probability
  the alternative *alone* explains the observed fingerprint, NOT
  whether bigger LMs help in general. The Alt predicts the *opposite
  signs* on the same-substrate-Commercial gap and the Commercial-vs-
  Minimal gap-direction; both are observably violated, so pi(Alt) is
  held substantially below pi(H).
* **Contradicted literature-implied premises** (lit_fixed_team_
  assumption, lit_tightly_coupled_coordination) -- 0.5. These are the
  literature-attributed positions the paper *contradicts*; we set
  them at uninformative 0.5 and let the contradiction operators
  discriminate via BP.
* **Limitations / cost-tradeoff / open questions** -- 0.85-0.9. Self-
  reported caveats from Section 5; the paper explicitly states these.
* **Talent-Market sourcing-channel + grounding claims** (three-sourcing
  channels, talent-market-grounding, human-in-loop-recruitment) --
  0.9. Direct architectural descriptions of Appendix D.
"""

from .motivation import (
    claim_skills_within_agent_only,
    claim_existing_mas_three_limits,
    claim_dynamic_workflow_still_bounded,
)
from .s2_related_work import (
    claim_heterogeneity_only_at_model_level,
    claim_protocol_and_marketplace_landscape,
    claim_team_composition_spectrum,
    claim_dynamic_decomposition_landscape,
    claim_individual_evolution_landscape,
    claim_organisation_evolution_underdeveloped,
    claim_table_4_architectural_comparison,
    claim_lit_fixed_team_assumption,
    claim_lit_tightly_coupled_coordination,
)
from .s3_setup import (
    claim_radical_heterogeneity_challenge,
)
from .s4_talent_abstraction import (
    claim_os_kernel_correspondence,
    claim_talent_market_grounding,
    claim_three_sourcing_channels,
    claim_human_in_loop_recruitment,
    claim_table_1_skills_vs_talents,
)
from .s5_e2r_tree_search import (
    claim_stage_2_execute,
    claim_stage_3_review,
    claim_external_oracle_role,
    claim_circuit_breakers_imply_bounded_termination,
)
from .s6_dag_and_guarantees import (
    claim_invariant_1_dag,
    claim_invariant_2_mutual_exclusion,
    claim_invariant_3_schedule_idempotency,
    claim_invariant_4_review_termination,
    claim_invariant_5_cascade_completeness,
    claim_invariant_6_dependency_completeness,
    claim_invariant_7_recovery_correctness,
)
from .s7_self_evolution import (
    claim_individual_evolution_modifies_talent_artefacts,
    claim_org_knowledge_accumulates_across_projects,
    claim_hr_pipeline_closes_market_loop,
)
from .s9_main_results import (
    claim_table_2_prdbench,
    claim_design_aspect_dynamic_decomposition,
    claim_design_aspect_review_gate,
    claim_design_aspect_cross_family,
)
from .s10_discussion import (
    claim_pred_h_organisational_decoupling_drives,
    claim_pred_alt_bigger_lm_or_more_compute,
    claim_limitation_only_prdbench_quant,
    claim_limitation_self_evolution_not_ablated,
)


PRIORS: dict = {
    # -----------------------------------------------------------------
    # Direct table / numerical readouts
    # -----------------------------------------------------------------
    claim_table_2_prdbench: (
        0.95,
        "Table 2: 12-row baseline panel + OMC entry on PRDBench DEV "
        "mode. OMC 84.67% vs Claude-4.5 Minimal 69.19% (next-best). "
        "Direct verbatim transcription from the published PDF; "
        "uncertainty is transcription risk only. Cost figure $345.59 "
        "is also a direct readout.",
    ),
    claim_table_1_skills_vs_talents: (
        0.95,
        "Table 1: 11-axis comparison of Skills-and-Skill-Markets vs "
        "Talents-and-Talent-Markets. Direct verbatim transcription "
        "from page 4 of the published PDF.",
    ),
    claim_table_4_architectural_comparison: (
        0.93,
        "Table 4: 8-system architectural comparison (8 dimensions). "
        "Direct verbatim transcription from page 19. The slightly "
        "lower prior reflects the larger surface area for "
        "transcription error compared to Table 1 / 2.",
    ),

    # -----------------------------------------------------------------
    # Architectural / design-property claims (read off the design)
    # -----------------------------------------------------------------
    claim_invariant_1_dag: (
        0.95,
        "Invariant I1 (DAG acyclicity, enforced via DFS at "
        "insertion). Read directly off the data-structure invariant "
        "stated in Section 2.2.4. Structurally certain.",
    ),
    claim_invariant_2_mutual_exclusion: (
        0.95,
        "Invariant I2 (|running(e)| <= 1). Direct reading of the "
        "Task-interface mutual exclusion semantics. Structurally "
        "certain.",
    ),
    claim_invariant_3_schedule_idempotency: (
        0.93,
        "Invariant I3 (re-scheduling is a no-op). Architectural "
        "property of the scheduler; design-level certainty.",
    ),
    claim_invariant_4_review_termination: (
        0.95,
        "Invariant I4 (at most k_rev reviews per parent before "
        "escalation). Direct reading of the FSM constraint plus the "
        "circuit-breaker spec.",
    ),
    claim_invariant_5_cascade_completeness: (
        0.93,
        "Invariant I5 (cancel(v) propagates transitively). Direct "
        "reading of the cancellation semantics in Section 2.2.4.",
    ),
    claim_invariant_6_dependency_completeness: (
        0.95,
        "Invariant I6 (every resolved-state transition triggers "
        "forward dependency resolution). Direct reading of the "
        "scheduler design; structurally certain.",
    ),
    claim_invariant_7_recovery_correctness: (
        0.92,
        "Invariant I7 (crash recovery resets processing -> pending "
        "and re-schedules ready dependents). Direct reading of the "
        "recovery contract; the prior reflects modest implementation-"
        "completeness uncertainty.",
    ),
    claim_circuit_breakers_imply_bounded_termination: (
        0.93,
        "Direct logical consequence of the three circuit breakers "
        "(review-round limit, task timeout, cost budget) plus the "
        "executor-respects-timeout assumption. Read off Section "
        "2.2.3.",
    ),
    claim_os_kernel_correspondence: (
        0.92,
        "Six-interface to OS-kernel-subsystem correspondence "
        "(Process / Memory / FS / I/O / IPC / Security). Direct "
        "structural mapping in Appendix B Table 6, supported by "
        "standard OS texts [@TanenbaumOS; @SilberschatzOS].",
    ),

    # -----------------------------------------------------------------
    # Stage-level claims for E2R
    # -----------------------------------------------------------------
    claim_stage_2_execute: (
        0.93,
        "Stage 2 Execute -- (r_v, c_v) = f_{e_v}(d_v) with f opaque "
        "to the org layer for closed-source agents. Direct reading "
        "of Section 2.2.1 + Algorithm 1.",
    ),
    claim_stage_3_review: (
        0.93,
        "Stage 3 Review -- bottom-up propagation of accept/reject + "
        "accept-or-redecompose loop. Direct reading of Section 2.2.1 "
        "+ Figure 4.",
    ),
    claim_external_oracle_role: (
        0.9,
        "CEO as external oracle (override / requirement injection / "
        "iteration triggering). Direct reading of Section 2.2.2; "
        "Russell-Wefald analogy is paper-supplied.",
    ),

    # -----------------------------------------------------------------
    # Talent Market / sourcing claims
    # -----------------------------------------------------------------
    claim_three_sourcing_channels: (
        0.92,
        "Three Talent-sourcing channels (curated repository / "
        "persona+skill assembly / dynamic cloud-skill assembly). "
        "Direct architectural description in Appendix D.",
    ),
    claim_talent_market_grounding: (
        0.9,
        "Talent Market grounded in community-validated, benchmark-"
        "tested implementations (vs synthesised personas). Direct "
        "reading of Section 2.1.2 + Appendix D.",
    ),
    claim_human_in_loop_recruitment: (
        0.9,
        "Top-k shortlist with ~80/20 Type1+2 / Type3 composition; "
        "CEO selection. Direct reading of Section 2.1.2 + "
        "Appendix D.",
    ),

    # -----------------------------------------------------------------
    # Three design aspects of OMC contributing to the gain
    # -----------------------------------------------------------------
    claim_design_aspect_dynamic_decomposition: (
        0.9,
        "D1: dynamic decomposition adjusts mid-execution. Read off "
        "Section 3.2's design-aspect attribution; consistent with "
        "the case-study evidence (game-development re-exploration).",
    ),
    claim_design_aspect_review_gate: (
        0.92,
        "D2: enforced completed -> accepted review gate. Direct "
        "reading of FSM design in Figure 5 plus Section 3.2's "
        "attribution.",
    ),
    claim_design_aspect_cross_family: (
        0.9,
        "D3: Container-Talent separation enables cross-family "
        "recruitment. Direct reading of Section 3.2's attribution + "
        "the Talent-Container architecture in Section 2.1.",
    ),

    # -----------------------------------------------------------------
    # Diagnosis premises
    # -----------------------------------------------------------------
    claim_skills_within_agent_only: (
        0.9,
        "Skills operate within a single agent. Standard observation "
        "in the agent-skills literature [@SkillsMP; @MCPZoo].",
    ),
    claim_existing_mas_three_limits: (
        0.9,
        "Existing MAS frameworks face fixed-team brittleness, "
        "runtime lock-in, and session-bound learning. Author "
        "diagnosis backed by the cited frameworks (CrewAI, AutoGen, "
        "Paperclip).",
    ),
    claim_dynamic_workflow_still_bounded: (
        0.88,
        "Dynamic agentic workflows still pre-configure the team / "
        "runtime / template. Author paraphrase of TDAG / "
        "Plan-and-Act / EvoMAC; well-supported by reading those "
        "systems' designs.",
    ),
    claim_radical_heterogeneity_challenge: (
        0.92,
        "Radical executor heterogeneity (LangGraph / Claude Code / "
        "script) makes a unifying abstraction necessary. Direct "
        "engineering observation supported by the three deployed "
        "Container families.",
    ),

    # -----------------------------------------------------------------
    # Related-work characterizations
    # -----------------------------------------------------------------
    claim_heterogeneity_only_at_model_level: (
        0.9,
        "Author paraphrase of Magentic-One / OWL / X-MAS / MacNet / "
        "AgentForge / AIOS -- model-level heterogeneity but shared "
        "execution runtime. Standard reading of these systems.",
    ),
    claim_protocol_and_marketplace_landscape: (
        0.9,
        "MCP / A2A handle tool-level integration; Cerebrum / "
        "AgentStore / AgentScope host agents. Author observation "
        "that none offers a complete-agent-package marketplace with "
        "managed lifecycle.",
    ),
    claim_team_composition_spectrum: (
        0.88,
        "Team composition ranges from fully fixed [@MagenticOne; "
        "@OWL] to fully dynamic [@EvoMAC]; no founding-team "
        "bootstrap. Author observation supported by reading the "
        "cited systems.",
    ),
    claim_dynamic_decomposition_landscape: (
        0.9,
        "Dynamic task decomposition exists [@TDAG; @PlanAndAct; "
        "@AFlow; @EvoMAC] but lacks formal completion guarantees. "
        "Direct observation supported by surveying these systems.",
    ),
    claim_individual_evolution_landscape: (
        0.9,
        "Individual self-improvement well developed [@ACE; @ADAS; "
        "@AgentWorkflowMemory]. Standard reading of the recent "
        "self-improving-agent literature.",
    ),
    claim_organisation_evolution_underdeveloped: (
        0.88,
        "Organisation-level evolution is underdeveloped (rare cross-"
        "project persistence). Author claim consistent with the "
        "absence of structured HR protocols in prior work.",
    ),

    # -----------------------------------------------------------------
    # Self-evolution architectural claims
    # -----------------------------------------------------------------
    claim_individual_evolution_modifies_talent_artefacts: (
        0.92,
        "Individual evolution updates Talent prompt-level artefacts "
        "(working principles, guidance), not foundation-model "
        "parameters. Direct architectural reading of Section 2.3.1.",
    ),
    claim_org_knowledge_accumulates_across_projects: (
        0.92,
        "SOPs persist + auto-inject across projects. Direct "
        "architectural reading of Section 2.3.2.",
    ),
    claim_hr_pipeline_closes_market_loop: (
        0.9,
        "HR pipeline (review / PIP / offboarding) replaces "
        "underperformers via the Talent Market and retains "
        "high performers. Direct architectural reading of "
        "Section 2.3.2.",
    ),

    # -----------------------------------------------------------------
    # Limitations
    # -----------------------------------------------------------------
    claim_limitation_only_prdbench_quant: (
        0.9,
        "Self-reported caveat (Section 5): only PRDBench "
        "quantitatively evaluated. Direct statement.",
    ),
    claim_limitation_self_evolution_not_ablated: (
        0.9,
        "Self-reported caveat (Section 5): self-evolution mechanisms "
        "not yet quantitatively ablated. Direct statement; explains "
        "why the package contains no ablation tables.",
    ),

    # -----------------------------------------------------------------
    # Central abduction predictions
    # -----------------------------------------------------------------
    claim_pred_h_organisational_decoupling_drives: (
        0.7,
        "Organisational-decoupling hypothesis predicts a four-fact "
        "fingerprint: (F1) same-substrate Commercial gap, (F2) "
        "broad cross-family Minimal gap, (F3) framework-invariant "
        "cross-domain success, (F4) mid-project skill creation. "
        "All four predictions are observed (Table 2 + Section 3.3). "
        "pi(H) = 0.7 reflects: well-motivated by the design "
        "(typed-interface + Talent Market + E2R), all four facts "
        "follow by direct prediction from the design, and the "
        "empirical fingerprint reproduces every signed prediction.",
    ),
    claim_pred_alt_bigger_lm_or_more_compute: (
        0.15,
        "Bigger-LM / better-tools / more-compute alternative is "
        "held at low pi(Alt) = 0.15 because: (i) OMC's Claude "
        "Sonnet 4.6 backbone lets us compare to Claude-4.5 Minimal "
        "and Claude Code Commercial -- the *Commercial* gap is "
        "*wider* (+28 pp) than the Minimal gap (+15.48 pp), the "
        "opposite of what the alternative predicts; (ii) the four "
        "cross-domain case studies use the *same* OMC framework "
        "with no domain-specific scaffolding, contradicting the "
        "alternative's prediction of per-domain customisation; "
        "(iii) mid-project skill creation in the game-development "
        "case is a behaviour outside what 'more compute' alone "
        "predicts. pi(Alt) = probability the alternative *alone* "
        "explains the observed fingerprint, NOT whether bigger "
        "LLMs help in general.",
    ),

    # -----------------------------------------------------------------
    # Contradicted literature assumptions
    # -----------------------------------------------------------------
    claim_lit_fixed_team_assumption: (
        0.5,
        "Literature-implied position the paper contradicts. We set "
        "this at uninformative 0.5 and let the contradiction "
        "operator (with claim_omc_demonstration_dynamic_org_works "
        "on the other side) discriminate via BP propagation.",
    ),
    claim_lit_tightly_coupled_coordination: (
        0.5,
        "Literature-implied position the paper contradicts. We set "
        "this at uninformative 0.5 and let the contradiction "
        "operator (with claim_omc_typed_interfaces_demonstration "
        "on the other side) discriminate via BP propagation.",
    ),
}
