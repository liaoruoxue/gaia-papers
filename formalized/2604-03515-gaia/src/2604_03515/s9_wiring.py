"""Pass-3 wiring module: connect orphan claims into the reasoning graph.

This module is *not* a section of the source paper. It exists to ensure
that every per-agent finding, per-table observation, and threats-to-
validity claim participates in the reasoning graph -- either as a
premise of a downstream strategy or as a derived conclusion.

Wiring philosophy:
* Per-table claims (Table 4, 6, 7, 9, 13) feed the corresponding
  per-dimension findings (e.g. Table 4 -> control-flow implementation
  diversity claims).
* Per-agent unique observations (Aider PageRank, Codex dual
  persistence, Cline shadow git, etc.) are evidence that the
  corresponding spectrum is genuinely populated -- they support the
  spectral finding.
* Threats-to-validity claims (single-author bias, snapshot-only,
  Python dominance, open-source survivorship, static-analysis
  blindness) are wired to weaken (via prior calibration) the
  taxonomy contribution; we model them as supports for the broader
  caveat that the taxonomy is a snapshot/lower-bound, then connect
  that caveat into the dimensions-not-independent claim.
"""

from gaia.lang import support

from .motivation import (
    claim_finding_spectra_not_categories,
)
from .s2_related_work import (
    claim_configuration_artifacts_orthogonal,
    claim_individual_system_descriptions,
    claim_individual_system_unmapped_space,
    claim_swe_effi_token_snowball,
    claim_trajectory_studies_summary,
)
from .s3_methodology import (
    claim_dual_tool_counting,
    claim_scope_taxonomic_only,
    claim_table15_pinned_commits,
    claim_table1_thirteen_agents,
)
from .s4_control_architecture import (
    claim_cline_recursion,
    claim_graph_qualitatively_different,
    claim_loop_types_compose,
    claim_opencode_event_bus,
    claim_react_band,
    claim_table2_control_loops,
    claim_table3_loop_driver,
    claim_table4_control_flow,
    claim_tree_search_gradient,
)
from .s5_tool_environment import (
    claim_agentless_simulated_tool_use,
    claim_aider_pagerank_repomap,
    claim_aider_thirteen_edit_formats,
    claim_autocoderover_proxy_agent,
    claim_autocoderover_sbfl,
    claim_cline_shadow_git,
    claim_codex_meta_tools,
    claim_codex_per_turn_rebuild,
    claim_moatless_shadow_mode,
    claim_openhands_browsergym,
    claim_prometheus_per_node_scoping,
    claim_retrieval_correlates_with_loop_driver,
    claim_safety_diverges_for_cli,
    claim_str_replace_convergence,
    claim_swe_agent_ten_parsers,
    claim_table5_tool_sets,
    claim_table6_edit_format,
    claim_table7_tool_discovery,
    claim_table8_retrieval,
    claim_table9_isolation,
    claim_two_retrieval_paradigms,
)
from .s6_resource_management import (
    claim_agentless_no_state,
    claim_cline_cross_tool_compat,
    claim_cline_llm_initiated,
    claim_codex_dual_persistence,
    claim_codex_most_models,
    claim_codex_pre_vs_mid_turn,
    claim_compaction_seven_strategies,
    claim_gemini_classifier_chain,
    claim_gemini_probe_verification,
    claim_ide_as_architecture,
    claim_llm_as_memory_author,
    claim_memory_benchmark_vs_cli_divide,
    claim_moatless_actor_critic,
    claim_online_vs_offline_selection,
    claim_prometheus_graph_scoped,
    claim_routing_dominant_driver,
    claim_state_management_extremes,
    claim_subagent_delegation,
    claim_swe_agent_polling_parameter,
    claim_table10_state_management,
    claim_table11_compaction,
    claim_table12_routing,
    claim_table13_memory,
)
from .s7_convergence_divergence import (
    claim_analytic_not_statistical_generalizability,
    claim_dimensions_not_independent,
    claim_open_source_survivorship_threat,
    claim_pilot_dimension_coverage_threat,
    claim_python_dominance_threat,
    claim_single_author_construct_threat,
    claim_spectral_finding_consolidated,
    claim_static_analysis_misses_runtime,
    claim_taxonomy_is_snapshot,
)

# ---------------------------------------------------------------------------
# Section A: per-table claims feed the per-dimension diversity
# ---------------------------------------------------------------------------

# Table 4 (control-flow implementation) populates the control-loop spectrum
# via Cline's recursion + Prometheus's graph + OpenCode's event bus.
strat_table4_supports_loop_types_compose = support(
    [claim_table4_control_flow, claim_cline_recursion, claim_graph_qualitatively_different,
     claim_opencode_event_bus],
    claim_loop_types_compose,
    reason=(
        "The Section-4.1.3 control-flow-implementation diversity "
        "(@claim_table4_control_flow) -- with Cline's recursion "
        "(@claim_cline_recursion), Prometheus's inspectable graph "
        "(@claim_graph_qualitatively_different), and OpenCode's "
        "global event bus (@claim_opencode_event_bus) as the three "
        "non-imperative-while-loop alternatives -- demonstrates that "
        "the same loop type can be realized through fundamentally "
        "different code-level mechanisms, reinforcing the "
        "loop-composability claim (@claim_loop_types_compose)."
    ),
    prior=0.9,
)

# Table 6 (edit format) supports the str_replace convergence claim plus
# the spectral finding via Aider's 13 formats and Agentless's simulation.
strat_table6_supports_str_replace_convergence = support(
    [claim_table6_edit_format, claim_aider_thirteen_edit_formats,
     claim_swe_agent_ten_parsers, claim_agentless_simulated_tool_use],
    claim_str_replace_convergence,
    reason=(
        "The 5-variant edit-format table (@claim_table6_edit_format) "
        "alongside the model-specific outliers -- Aider's 13 formats "
        "(@claim_aider_thirteen_edit_formats), SWE-agent's 10 "
        "parsers (@claim_swe_agent_ten_parsers), Agentless's "
        "structured-output trick (@claim_agentless_simulated_tool_use) "
        "-- documents the str_replace_editor convergence "
        "(@claim_str_replace_convergence) as the dominant pattern "
        "amid surrounding diversity."
    ),
    prior=0.9,
)

# Table 7 (tool discovery) feeds spectral via the per-turn rebuild example.
strat_table7_supports_spectrum = support(
    [claim_table7_tool_discovery, claim_codex_per_turn_rebuild],
    claim_spectral_finding_consolidated,
    reason=(
        "The 5-strategy tool-discovery spectrum "
        "(@claim_table7_tool_discovery) -- exemplified by Codex CLI's "
        "per-turn dynamic rebuild (@claim_codex_per_turn_rebuild) at "
        "one extreme and Aider/Agentless static registration at the "
        "other -- adds another continuous spectrum to the consolidated "
        "spectral finding (@claim_spectral_finding_consolidated)."
    ),
    prior=0.88,
)

# Table 8 (retrieval) supports the retrieval-correlates-with-loop-driver
# claim and the two-retrieval-paradigms claim.
strat_table8_supports_two_paradigms = support(
    [claim_table8_retrieval, claim_aider_pagerank_repomap, claim_autocoderover_sbfl],
    claim_two_retrieval_paradigms,
    reason=(
        "The 7-strategy retrieval table (@claim_table8_retrieval), "
        "with Aider's PageRank (@claim_aider_pagerank_repomap) and "
        "AutoCodeRover's SBFL (@claim_autocoderover_sbfl) as "
        "scaffold-side investments contrasted against the "
        "LLM-as-navigator approaches, documents the two-paradigm "
        "split (@claim_two_retrieval_paradigms)."
    ),
    prior=0.92,
)

strat_two_paradigms_supports_correlation = support(
    [claim_two_retrieval_paradigms],
    claim_retrieval_correlates_with_loop_driver,
    reason=(
        "The two-retrieval-paradigm finding "
        "(@claim_two_retrieval_paradigms) directly underwrites the "
        "claim that retrieval paradigm correlates with loop driver "
        "(@claim_retrieval_correlates_with_loop_driver), since the "
        "scaffold-side investments cluster with the scaffold-driven "
        "agents and the LLM-navigator pattern with the LLM-driven "
        "agents."
    ),
    prior=0.9,
)

# Table 9 (isolation) supports the safety-diverges claim.
strat_table9_supports_safety_diverges = support(
    [claim_table9_isolation, claim_cline_shadow_git, claim_moatless_shadow_mode],
    claim_safety_diverges_for_cli,
    reason=(
        "The 7-level isolation table (@claim_table9_isolation), with "
        "Cline's shadow git (@claim_cline_shadow_git) and Moatless's "
        "in-memory shadow mode (@claim_moatless_shadow_mode) "
        "alongside the platform-sandboxing/Guardian/human-in-the-loop "
        "alternatives, documents the divergence in CLI safety "
        "approaches (@claim_safety_diverges_for_cli)."
    ),
    prior=0.9,
)

# Table 10 (state) supports the state-management-extremes claim.
strat_table10_supports_extremes = support(
    [claim_table10_state_management, claim_agentless_no_state,
     claim_codex_dual_persistence, claim_prometheus_graph_scoped],
    claim_state_management_extremes,
    reason=(
        "The 8-variant state-management table "
        "(@claim_table10_state_management), with Agentless having no "
        "conversation state (@claim_agentless_no_state), Codex's dual "
        "persistence (@claim_codex_dual_persistence), and "
        "Prometheus's graph-scoped state (@claim_prometheus_graph_scoped) "
        "documenting the extremes, justifies the destructive-to-"
        "event-sourced range (@claim_state_management_extremes)."
    ),
    prior=0.92,
)

# Table 11 (compaction) supports the seven-strategies claim.
strat_table11_supports_seven_strategies = support(
    [claim_table11_compaction, claim_swe_agent_polling_parameter,
     claim_gemini_probe_verification, claim_cline_llm_initiated,
     claim_codex_pre_vs_mid_turn],
    claim_compaction_seven_strategies,
    reason=(
        "The 7-strategy compaction table (@claim_table11_compaction), "
        "with SWE-agent's polling (@claim_swe_agent_polling_parameter), "
        "Gemini CLI's verification probe "
        "(@claim_gemini_probe_verification), Cline's LLM-initiated "
        "compaction (@claim_cline_llm_initiated), and Codex CLI's "
        "pre-/mid-turn distinction (@claim_codex_pre_vs_mid_turn) "
        "as evidence of the strategy-level diversity, supports the "
        "seven-strategy headline (@claim_compaction_seven_strategies)."
    ),
    prior=0.93,
)

# Table 12 (routing) supports the routing-dominant-driver claim.
strat_table12_supports_routing_driver = support(
    [claim_table12_routing, claim_gemini_classifier_chain,
     claim_moatless_actor_critic, claim_codex_most_models],
    claim_routing_dominant_driver,
    reason=(
        "The 9-strategy multi-model routing table "
        "(@claim_table12_routing), with Gemini CLI's 7-layer chain "
        "(@claim_gemini_classifier_chain), Moatless's actor-critic "
        "(@claim_moatless_actor_critic), and Codex CLI using the "
        "most models in the corpus (@claim_codex_most_models) as "
        "exemplars, supports the cost-optimization-as-dominant-"
        "driver finding (@claim_routing_dominant_driver)."
    ),
    prior=0.9,
)

# Table 13 (memory) supports the memory benchmark/CLI divide claim.
strat_table13_supports_memory_divide = support(
    [claim_table13_memory, claim_llm_as_memory_author,
     claim_cline_cross_tool_compat],
    claim_memory_benchmark_vs_cli_divide,
    reason=(
        "The 7-variant persistent-memory table "
        "(@claim_table13_memory), with the LLM-as-memory-author "
        "pattern (@claim_llm_as_memory_author) and Cline's "
        "cross-tool memory-file compatibility "
        "(@claim_cline_cross_tool_compat), supports the benchmark/"
        "CLI divide finding (@claim_memory_benchmark_vs_cli_divide)."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# Section B: per-agent unique observations support the spectral finding
# ---------------------------------------------------------------------------

strat_spectral_per_agent_uniques = support(
    [
        claim_aider_pagerank_repomap,
        claim_openhands_browsergym,
        claim_prometheus_per_node_scoping,
        claim_codex_meta_tools,
        claim_autocoderover_proxy_agent,
    ],
    claim_finding_spectra_not_categories,
    reason=(
        "The motivation preview of the spectral finding "
        "(@claim_finding_spectra_not_categories) is further "
        "supported by per-agent unique observations: Aider's "
        "PageRank repo map (@claim_aider_pagerank_repomap), "
        "OpenHands' BrowserGym tool (@claim_openhands_browsergym), "
        "Prometheus's per-node tool scoping "
        "(@claim_prometheus_per_node_scoping), Codex CLI's "
        "meta-tools and negotiable permissions "
        "(@claim_codex_meta_tools), and AutoCodeRover's secondary "
        "LLM proxy (@claim_autocoderover_proxy_agent). Each "
        "exemplifies a distinct position no other agent occupies."
    ),
    prior=0.88,
)

# ---------------------------------------------------------------------------
# Section C: threats-to-validity wired into the snapshot caveat
# ---------------------------------------------------------------------------

# C.1 -- snapshot caveat is supported by the pinned-commit fact + the
# active-development timeline.
strat_snapshot_caveat = support(
    [claim_table15_pinned_commits],
    claim_taxonomy_is_snapshot,
    reason=(
        "The snapshot caveat (@claim_taxonomy_is_snapshot) follows "
        "from the fact that all 13 agents are pinned to specific "
        "commit hashes (@claim_table15_pinned_commits) -- pinning "
        "ensures reproducibility but also makes the analysis a "
        "snapshot rather than a live description."
    ),
    prior=0.95,
)

# C.2 -- pilot-coverage threat tied to the table-of-13 corpus.
strat_pilot_coverage = support(
    [claim_table1_thirteen_agents],
    claim_pilot_dimension_coverage_threat,
    reason=(
        "The pilot-coverage threat "
        "(@claim_pilot_dimension_coverage_threat) is anchored in "
        "the corpus of 13 agents (@claim_table1_thirteen_agents): "
        "while the open-ended tenth section captured 47 cross-"
        "cutting findings, dimensions surfaceable only by agents "
        "not in the corpus could remain missing."
    ),
    prior=0.85,
)

# C.3 -- single-author threat tied to the verification + 3-level template
# (which mitigates it). Modeled as supporting the dimensions-not-
# independent caveat -- the threats together motivate caution.
strat_single_author_threat_into_caveat = support(
    [claim_single_author_construct_threat,
     claim_pilot_dimension_coverage_threat],
    claim_dimensions_not_independent,
    reason=(
        "The dimensions-not-independent caveat "
        "(@claim_dimensions_not_independent) is reinforced by the "
        "single-author bias threat (@claim_single_author_construct_threat) "
        "-- a single analyst is more likely to have invented "
        "dimension boundaries that overlap -- and by the pilot-"
        "coverage threat (@claim_pilot_dimension_coverage_threat). "
        "These methodological constraints make perfectly-orthogonal "
        "dimension boundaries unlikely a priori."
    ),
    prior=0.75,
)

# C.4 -- external-validity threats (open-source survivorship, Python
# dominance, static-analysis blindness, analytic generalizability) feed
# the snapshot caveat.
strat_external_threats_into_snapshot = support(
    [
        claim_open_source_survivorship_threat,
        claim_python_dominance_threat,
        claim_static_analysis_misses_runtime,
        claim_analytic_not_statistical_generalizability,
    ],
    claim_taxonomy_is_snapshot,
    reason=(
        "The taxonomy-is-snapshot caveat "
        "(@claim_taxonomy_is_snapshot) is reinforced by the "
        "open-source survivorship bias "
        "(@claim_open_source_survivorship_threat), the SWE-bench "
        "Python dominance (@claim_python_dominance_threat), the "
        "static-analysis blindness to runtime behaviour "
        "(@claim_static_analysis_misses_runtime), and the analytic-"
        "but-not-statistical generalizability framing "
        "(@claim_analytic_not_statistical_generalizability). All "
        "four together confirm the taxonomy describes a delimited "
        "snapshot rather than the full design space."
    ),
    prior=0.85,
)

# ---------------------------------------------------------------------------
# Section D: connect remaining individual orphans
# ---------------------------------------------------------------------------

# D.1 -- the dual tool-counting methodology is what makes the tool-set
# table cross-agent-comparable.
strat_dual_counting_supports_table5 = support(
    [claim_dual_tool_counting],
    claim_table5_tool_sets,
    reason=(
        "The dual tool-counting methodology "
        "(@claim_dual_tool_counting) is the methodological "
        "underpinning that makes Table 5 (@claim_table5_tool_sets) "
        "cross-agent-comparable: registration count gives the "
        "interface granularity, capability category count gives "
        "the functional coverage."
    ),
    prior=0.95,
)

# D.2 -- scope-taxonomic-only is a methodological premise for the eval-
# implications discussion (already wired implicitly via the SWE-bench
# claim, but make it explicit).
strat_scope_supports_eval_swebench = support(
    [claim_scope_taxonomic_only],
    claim_individual_system_unmapped_space,
    reason=(
        "The taxonomic-only scope (@claim_scope_taxonomic_only) is "
        "what makes the related-work observation that the design "
        "space remains unmapped (@claim_individual_system_unmapped_space) "
        "actionable in this paper -- the present work fills the "
        "comparative gap *without* attempting to also benchmark "
        "performance, keeping the contribution well-scoped."
    ),
    prior=0.85,
)

# D.3 -- cross-cutting themes (sub-agent delegation, sampling vs
# iteration, online vs offline selection) feed the spectral / loop-
# composition story.
strat_subagent_supports_react_band = support(
    [claim_subagent_delegation],
    claim_react_band,
    reason=(
        "The sub-agent delegation theme (@claim_subagent_delegation) "
        "complements the ReAct-band finding (@claim_react_band): "
        "agents in the ReAct band that adopt sub-agent delegation "
        "(Codex CLI, OpenCode, Cline, Gemini CLI) are precisely "
        "the ones that compose plan-execute on top of pure ReAct, "
        "explaining why the ReAct band is heterogeneous."
    ),
    prior=0.85,
)

strat_online_offline_supports_tree_search = support(
    [claim_online_vs_offline_selection],
    claim_tree_search_gradient,
    reason=(
        "The online-vs-offline selection theme "
        "(@claim_online_vs_offline_selection) refines the "
        "tree-search gradient (@claim_tree_search_gradient): "
        "DARS-Agent and Moatless Tools differ not only in MCTS "
        "machinery but in *how* they cleanly separate online "
        "guidance from offline final-answer selection."
    ),
    prior=0.88,
)

# D.4 -- related-work supports.
strat_individual_systems_into_unmapped = support(
    [claim_individual_system_descriptions, claim_swe_effi_token_snowball,
     claim_trajectory_studies_summary],
    claim_individual_system_unmapped_space,
    reason=(
        "The unmapped-design-space observation "
        "(@claim_individual_system_unmapped_space) is supported by "
        "the existence of per-system descriptions "
        "(@claim_individual_system_descriptions), prior trajectory "
        "studies (@claim_trajectory_studies_summary), and "
        "resource-oriented analyses (@claim_swe_effi_token_snowball) "
        "-- each providing a slice of architectural evidence that "
        "no prior work has aggregated into a comparative reference."
    ),
    prior=0.92,
)

# D.5 -- configuration-vs-architecture (Galster) supports the scope
# claim that this paper's contribution is at the architectural layer.
strat_config_vs_arch_supports_scope = support(
    [claim_configuration_artifacts_orthogonal],
    claim_scope_taxonomic_only,
    reason=(
        "The configuration-vs-architecture distinction "
        "(@claim_configuration_artifacts_orthogonal, citing "
        "Galster et al.) reinforces the taxonomic-only scope "
        "(@claim_scope_taxonomic_only): scaffold architecture and "
        "developer-facing configuration are complementary layers, "
        "and this paper deliberately analyses the former."
    ),
    prior=0.85,
)
