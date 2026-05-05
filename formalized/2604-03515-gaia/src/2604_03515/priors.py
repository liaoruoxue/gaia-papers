"""Priors for independent (leaf) claims in the 2604.03515 formalization.

Priors are calibrated against:
* The source paper's own confidence framing (Section 6 threats to
  validity; the 267/19/10 verification audit).
* External commonly-accepted facts (capability surveys exist;
  ReAct/Reflexion are standard).
* Per-agent observations: each is a directly-verifiable file/line
  citation, so priors are high (0.92-0.96) unless the source itself
  flags ambiguity.

Rules applied:
* Direct per-agent code observations grounded in verifiable file/line
  citations -> 0.93-0.96.
* Per-table aggregations of those observations -> 0.92-0.94.
* Methodological framing claims (taxonomy structure, dual counting,
  pinned commits) -> 0.92-0.95 (mechanical / procedural).
* Threats-to-validity claims -> 0.85-0.95 (the threats themselves are
  documented in the paper; the *direction* is reliable).
* Baseline assumptions to be contradicted -> 0.5-0.55 (near-uniform;
  let the contradiction operator do the work).
* Counter-hypotheses (uniform-stakes, arbitrary-cosmetic) -> 0.20-0.30
  (low; their own predictions don't match observation).
* Hypothesis predictions (compositional design) -> 0.85.
* Cross-cutting themes (sampling vs iteration, sub-agent delegation,
  online vs offline) -> 0.92-0.94 (well-evidenced patterns).
"""

from .motivation import (
    claim_baseline_capability_taxonomy_sufficient,
    claim_baseline_react_is_dominant_architecture,
)
from .s2_related_work import (
    claim_capability_taxonomies_existed,
    claim_capability_taxonomies_indistinguishable,
    claim_configuration_artifacts_orthogonal,
    claim_individual_system_descriptions,
    claim_react_reflexion_paradigms,
    claim_souza_machado_call,
    claim_swe_effi_token_snowball,
    claim_swebench_central,
    claim_taxonomy_enables_controlled_experiments,
    claim_trajectory_model_confound,
    claim_trajectory_studies_blackbox_limit,
    claim_trajectory_studies_summary,
)
from .s3_methodology import (
    claim_corpus_distinct_strategies,
    claim_dimension_open_coding_pilot,
    claim_dual_tool_counting,
    claim_llm_assisted_navigation,
    claim_nine_to_twelve_dimensions,
    claim_observation_classification_evidence,
    claim_pinned_commits_for_reproducibility,
    claim_table15_pinned_commits,
)
from .s4_control_architecture import (
    claim_cline_recursion,
    claim_graph_qualitatively_different,
    claim_loop_driver_distribution,
    claim_loop_driver_most_fundamental,
    claim_opencode_event_bus,
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
    claim_capability_categories_converge,
    claim_cline_shadow_git,
    claim_codex_meta_tools,
    claim_codex_per_turn_rebuild,
    claim_docker_converges_for_swebench,
    claim_moatless_shadow_mode,
    claim_openhands_browsergym,
    claim_prometheus_per_node_scoping,
    claim_str_replace_convergence,
    claim_swe_agent_ten_parsers,
    claim_table5_tool_sets,
    claim_table6_edit_format,
    claim_table7_tool_discovery,
    claim_table8_retrieval,
    claim_table9_isolation,
)
from .s6_resource_management import (
    claim_agentless_no_state,
    claim_cline_cross_tool_compat,
    claim_cline_llm_initiated,
    claim_codex_dual_persistence,
    claim_codex_most_models,
    claim_codex_pre_vs_mid_turn,
    claim_compaction_required_observation,
    claim_gemini_classifier_chain,
    claim_gemini_probe_verification,
    claim_ide_as_architecture,
    claim_llm_as_memory_author,
    claim_moatless_actor_critic,
    claim_online_vs_offline_selection,
    claim_prometheus_graph_scoped,
    claim_routing_dominant_driver,
    claim_sampling_vs_iteration,
    claim_state_management_extremes,
    claim_subagent_delegation,
    claim_swe_agent_polling_parameter,
    claim_table10_state_management,
    claim_table11_compaction,
    claim_table12_routing,
    claim_table13_memory,
    claim_dars_swe_fork_vs_mini_protocol,
)
from .s7_convergence_divergence import (
    claim_analytic_not_statistical_generalizability,
    claim_open_source_survivorship_threat,
    claim_pilot_dimension_coverage_threat,
    claim_python_dominance_threat,
    claim_single_author_construct_threat,
    claim_static_analysis_misses_runtime,
)
from .s8_implications import (
    claim_alt_arbitrary_cosmetic,
    claim_counter_uniform_convergence,
    claim_pred_alt_arbitrary,
    claim_pred_h_compositional_design,
)
from .s4_control_architecture import (
    claim_loop_types_compose,
    claim_react_band,
)

PRIORS: dict = {
    # ---------------------------------------------------------------
    # Motivation: baseline assumptions to be contradicted
    # ---------------------------------------------------------------
    claim_baseline_capability_taxonomy_sufficient: (
        0.50,
        "A widely held baseline view consistent with prior surveys "
        "(@Masterman2024, @Nowaczyk2025). Set near-uniform so the "
        "contradiction operator with the empirical spectral finding "
        "drives the BP outcome rather than the prior.",
    ),
    claim_baseline_react_is_dominant_architecture: (
        0.50,
        "A baseline view consistent with the popularity of ReAct "
        "[@Yao2023ReAct]. Set near-uniform so the contradiction with "
        "the empirical 11/13 multi-primitive observation drives the "
        "BP outcome.",
    ),
    # ---------------------------------------------------------------
    # s2 Related work
    # ---------------------------------------------------------------
    claim_capability_taxonomies_existed: (
        0.95,
        "Direct citation of existing surveys (Masterman et al. 2024; "
        "Nowaczyk 2025). The papers exist and are tabulated.",
    ),
    claim_capability_taxonomies_indistinguishable: (
        0.93,
        "Direct empirical observation: the author manually verified "
        "every agent in the 13-agent corpus qualifies as 'tool-using, "
        "memory-augmented, planning' under the prior schemes. "
        "Mechanically checkable.",
    ),
    claim_react_reflexion_paradigms: (
        0.92,
        "ReAct/Reflexion as algorithmic paradigms vs scaffold "
        "architectures: the distinction is well-grounded and the 7/13 "
        "observation is verifiable. The 'paradigm vs architecture' "
        "framing is essentially semantic, slightly subjective.",
    ),
    claim_trajectory_studies_summary: (
        0.93,
        "Direct citation of three trajectory studies (Ceka 2025, "
        "Majgaonkar 2026, Bouzenia 2025) with the empirical claims "
        "they reported. Verifiable.",
    ),
    claim_trajectory_studies_blackbox_limit: (
        0.92,
        "The black-box-limit critique is a fair characterization of "
        "trajectory studies that do not inspect scaffold code. The "
        "logical claim ('cannot distinguish among scaffold causes') is "
        "well-supported.",
    ),
    claim_trajectory_model_confound: (
        0.95,
        "Direct factual claim: Majgaonkar et al. did use Claude 3.5 "
        "Sonnet for OpenHands and DeepSeek-V3 for Prometheus. "
        "Mechanically verifiable from their methods section.",
    ),
    claim_swe_effi_token_snowball: (
        0.92,
        "Direct empirical findings reported in Fan et al. 2025 "
        "(SWE-Effi). Numbers come from a published study.",
    ),
    claim_individual_system_descriptions: (
        0.95,
        "Direct citation list of per-system architectural papers "
        "(SWE-agent, Aider, Bui, Agentless, DARS-Agent, "
        "AutoCodeRover, OpenHands). Each cited paper exists and "
        "describes what is claimed.",
    ),
    claim_configuration_artifacts_orthogonal: (
        0.9,
        "Galster et al. 2026 study of 2926 repos provides the "
        "factual basis. The 'configuration vs architecture' "
        "distinction is conceptually clean.",
    ),
    claim_swebench_central: (
        0.95,
        "SWE-bench's de-facto benchmark status is broadly "
        "documented; limitations cited (Garg, Xu, Chen) are real "
        "studies.",
    ),
    claim_taxonomy_enables_controlled_experiments: (
        0.88,
        "Methodological assertion about what the taxonomy enables. "
        "Plausible and well-argued, though future controlled "
        "experiments would verify.",
    ),
    claim_souza_machado_call: (
        0.92,
        "Direct citation of Souza & Machado 2026; their call for "
        "architecture-aware metrics is in the cited paper.",
    ),
    # ---------------------------------------------------------------
    # s3 Methodology
    # ---------------------------------------------------------------
    claim_corpus_distinct_strategies: (
        0.92,
        "The 13-agent corpus does span fixed pipelines, ReAct loops, "
        "phased workflows, depth-first tree search, and full MCTS "
        "(documented in Table 2). Verifiable.",
    ),
    claim_table15_pinned_commits: (
        0.97,
        "Direct table of repository URLs and commit hashes "
        "(Table 15 / Appendix B). Mechanically verifiable.",
    ),
    claim_dimension_open_coding_pilot: (
        0.9,
        "Methodological description of the pilot process. Source "
        "describes the iteration; we accept on author authority.",
    ),
    claim_nine_to_twelve_dimensions: (
        0.92,
        "Methodological description of the 9->12 expansion. "
        "Verifiable from the structure of Section 4.",
    ),
    claim_dual_tool_counting: (
        0.95,
        "Methodological framing for tool counts; the two definitions "
        "are clearly stated and consistently applied.",
    ),
    claim_observation_classification_evidence: (
        0.95,
        "Methodological framing applied across all 13 agent analyses. "
        "Well-grounded in case-study reporting guidelines "
        "[@RunesonHost2009].",
    ),
    claim_pinned_commits_for_reproducibility: (
        0.95,
        "Procedural; pinning to commit hashes is verifiable and the "
        "rationale (active development) is well-documented.",
    ),
    claim_llm_assisted_navigation: (
        0.92,
        "Author's procedural description. Verification of LLM-"
        "generated observations against source is the documented "
        "mitigation; the 296-claim verification pass corroborates.",
    ),
    # ---------------------------------------------------------------
    # s4 Control architecture: per-table evidence
    # ---------------------------------------------------------------
    claim_table2_control_loops: (
        0.94,
        "Table 2 directly documents the 6-position control-loop "
        "spectrum with per-row file/line citations. Mechanically "
        "verifiable.",
    ),
    claim_table3_loop_driver: (
        0.94,
        "Table 3 directly documents the 3-driver assignment with "
        "per-cell file/line citations. Mechanically verifiable.",
    ),
    claim_table4_control_flow: (
        0.94,
        "Table 4 directly documents the 5 control-flow "
        "implementations with per-row file/line citations.",
    ),
    claim_loop_driver_distribution: (
        0.93,
        "Direct per-agent distribution count from Table 3. "
        "Mechanically derivable.",
    ),
    claim_loop_driver_most_fundamental: (
        0.85,
        "Authorial judgement that loop driver is the most "
        "fundamental architectural distinction; well-argued in "
        "Section 4.1.2 and 5.3 but inherently a judgement call.",
    ),
    claim_tree_search_gradient: (
        0.94,
        "Three-agent tree-search gradient (Agentless / DARS / "
        "Moatless) directly documented with file/line citations.",
    ),
    claim_react_band: (
        0.94,
        "7/13 ReAct primary observation directly tabulated; Aider "
        "special case explicitly justified with the inner-loop file "
        "reference (`base_coder.py:932`).",
    ),
    claim_loop_types_compose: (
        0.93,
        "Multiple per-agent demonstrations of nesting (AutoCodeRover, "
        "Moatless ActionAgent decoupling, Cline's recursion). "
        "Compositional pattern is well-evidenced.",
    ),
    claim_cline_recursion: (
        0.95,
        "Direct file reference: `task/index.ts:2268`. "
        "`recursivelyMakeClineRequests` is documented.",
    ),
    claim_graph_qualitatively_different: (
        0.93,
        "Direct file references to LangGraph subgraph wiring; the "
        "four-level nesting example is explicit in the paper.",
    ),
    claim_opencode_event_bus: (
        0.94,
        "Direct file reference to `packages/opencode/src/bus/`; "
        "verifiable as unique in the corpus.",
    ),
    # ---------------------------------------------------------------
    # s5 Tool & environment interface
    # ---------------------------------------------------------------
    claim_table5_tool_sets: (
        0.94,
        "Table 5 directly documents tool counts and capability "
        "coverage with per-row evidence; supplemented by the dual "
        "tool counting methodology.",
    ),
    claim_capability_categories_converge: (
        0.94,
        "The 4-capability convergence (read/search/edit/execute) is "
        "an aggregated tabulation across all LLM-driven agents in "
        "Table 5. Mechanically verifiable.",
    ),
    claim_openhands_browsergym: (
        0.95,
        "OpenHands' BrowserGym integration is documented in its "
        "source and in the BrowserGym paper; verifiable.",
    ),
    claim_codex_meta_tools: (
        0.93,
        "Codex CLI's `tool_search`, `tool_suggest`, "
        "`request_permissions` tools are directly verifiable in the "
        "source.",
    ),
    claim_prometheus_per_node_scoping: (
        0.94,
        "Per-node tool binding is directly documented with the "
        "per-node tool counts (5 / 1 / 1).",
    ),
    claim_autocoderover_proxy_agent: (
        0.95,
        "Direct file reference: `agent_proxy.py:81--82`. The "
        "5-retry / 15-round configuration is explicit.",
    ),
    claim_table6_edit_format: (
        0.94,
        "Table 6 directly tabulates the 5 edit-format variants with "
        "per-row agent assignments.",
    ),
    claim_str_replace_convergence: (
        0.93,
        "5/13 agents with `str_replace_editor` is directly "
        "tabulated; the convergence claim is the reported count.",
    ),
    claim_aider_thirteen_edit_formats: (
        0.95,
        "Aider's 13 coder subclasses are directly enumerable in the "
        "Aider source repository.",
    ),
    claim_swe_agent_ten_parsers: (
        0.95,
        "SWE-agent's 10 parser classes are directly enumerable in "
        "the SWE-agent source.",
    ),
    claim_agentless_simulated_tool_use: (
        0.94,
        "Agentless's hardcoded 'File is successfully edited' "
        "response in the Anthropic path is directly verifiable.",
    ),
    claim_table7_tool_discovery: (
        0.94,
        "Table 7 directly tabulates the 5 tool-discovery strategies "
        "with file/line citations.",
    ),
    claim_codex_per_turn_rebuild: (
        0.95,
        "Direct file reference: `codex.rs:6156--6164` for "
        "`built_tools()` per LLM call.",
    ),
    claim_table8_retrieval: (
        0.94,
        "Table 8 directly tabulates 7 retrieval strategies with "
        "per-row file/line citations.",
    ),
    claim_aider_pagerank_repomap: (
        0.96,
        "Direct file reference (`repomap.py:365--574`); the 10x and "
        "50x boost factors are explicit in the code.",
    ),
    claim_autocoderover_sbfl: (
        0.95,
        "Direct file reference (`analysis/sbfl.py`); SBFL with "
        "Ochiai is documented.",
    ),
    claim_table9_isolation: (
        0.94,
        "Table 9 directly tabulates 7 isolation levels with "
        "per-row agent assignments.",
    ),
    claim_docker_converges_for_swebench: (
        0.93,
        "5/13 SWE-bench agents converge on Docker is directly "
        "tabulated and verifiable.",
    ),
    claim_cline_shadow_git: (
        0.94,
        "`CheckpointTracker.ts` is a documented file in Cline; the "
        "shadow git mechanism is verifiable.",
    ),
    claim_moatless_shadow_mode: (
        0.94,
        "Direct file reference: `agent.py:57` for `shadow_mode` "
        "flag. The in-memory `FileContext` design is verifiable.",
    ),
    # ---------------------------------------------------------------
    # s6 Resource management: per-table evidence + per-agent uniques
    # ---------------------------------------------------------------
    claim_table10_state_management: (
        0.94,
        "Table 10 directly tabulates 8 state-management variants "
        "with per-row file/line citations.",
    ),
    claim_state_management_extremes: (
        0.93,
        "Aider destructive vs OpenHands event-sourced is the "
        "canonical contrast tabulated in Table 10.",
    ),
    claim_agentless_no_state: (
        0.95,
        "Agentless's single-turn-LLM design with JSONL state is "
        "verifiable in the source.",
    ),
    claim_codex_dual_persistence: (
        0.94,
        "Codex CLI's JSONL+SQLite persistence and `Op::Undo` / "
        "`Op::ThreadRollback` operations are verifiable in the "
        "source.",
    ),
    claim_prometheus_graph_scoped: (
        0.94,
        "Per-node message lists and `ResetMessagesNode` are "
        "verifiable in Prometheus's LangGraph code.",
    ),
    claim_table11_compaction: (
        0.94,
        "Table 11 directly tabulates 7 compaction strategies with "
        "per-row file/line citations.",
    ),
    claim_compaction_required_observation: (
        0.95,
        "mini-swe-agent crashing on `ContextWindowExceededError` is "
        "an observed behaviour that confirms compaction is required.",
    ),
    claim_swe_agent_polling_parameter: (
        0.93,
        "SWE-agent's `polling` parameter on `LastNObservations` is "
        "directly verifiable in source.",
    ),
    claim_gemini_probe_verification: (
        0.94,
        "Gemini CLI's Probe verification turn is verifiable; "
        "uniqueness is asserted by the author after surveying all 13 "
        "agents.",
    ),
    claim_cline_llm_initiated: (
        0.94,
        "Cline's `condense` tool is directly verifiable; uniqueness "
        "as 'LLM-initiated' is asserted by author after surveying.",
    ),
    claim_codex_pre_vs_mid_turn: (
        0.94,
        "Codex CLI's pre-turn / mid-turn compaction modes are "
        "verifiable in the source.",
    ),
    claim_table12_routing: (
        0.94,
        "Table 12 directly tabulates 9 routing strategies with "
        "per-row file/line citations.",
    ),
    claim_routing_dominant_driver: (
        0.92,
        "The 'cost is dominant driver' aggregation across the 10 "
        "multi-model agents is well-supported by the per-agent "
        "details (weak models, base/advanced split, etc.).",
    ),
    claim_gemini_classifier_chain: (
        0.94,
        "Gemini CLI's 7-layer routing in `modelRouterService.ts:"
        "39--67` is directly verifiable.",
    ),
    claim_moatless_actor_critic: (
        0.92,
        "Moatless's value function in `value_function/base.py` is "
        "verifiable; uniqueness as 'actor-critic with separate "
        "models' is asserted by author.",
    ),
    claim_codex_most_models: (
        0.93,
        "Codex CLI uses 4 distinct models (primary + Guardian + "
        "2 memory-extraction); each is verifiable via its "
        "respective config.",
    ),
    claim_table13_memory: (
        0.94,
        "Table 13 directly tabulates 7 persistent-memory variants "
        "with per-row file/line citations.",
    ),
    claim_llm_as_memory_author: (
        0.94,
        "Cline's `new_rule` and Gemini CLI's `save_memory` are "
        "verifiable; the LLM-as-author pattern is well-documented.",
    ),
    claim_cline_cross_tool_compat: (
        0.94,
        "Cline reading .cursorrules / .windsurfrules / AGENTS.md is "
        "directly verifiable in the source.",
    ),
    # Cross-cutting themes
    claim_sampling_vs_iteration: (
        0.93,
        "The sampling-vs-iteration distinction is well-evidenced "
        "by per-agent observations (Agentless pure sampling, 6 "
        "iterators, SWE-agent hybrid, Prometheus voting).",
    ),
    claim_subagent_delegation: (
        0.93,
        "5 mechanisms across 5 agents (plus Prometheus implicit) is "
        "directly tabulated; the per-agent details are verifiable.",
    ),
    claim_online_vs_offline_selection: (
        0.92,
        "DARS-Agent's separate online critic + offline reviewer and "
        "Moatless's value-function + discriminator are both "
        "verifiable.",
    ),
    claim_dars_swe_fork_vs_mini_protocol: (
        0.93,
        "DARS-Agent's 1382 LoC fork and mini-swe-agent's Protocol-"
        "based design are mechanically verifiable line-counts.",
    ),
    claim_ide_as_architecture: (
        0.94,
        "Cline's IDE-extension nature and its VS Code API "
        "dependencies are verifiable; uniqueness in the corpus is "
        "asserted after surveying.",
    ),
    # ---------------------------------------------------------------
    # s7 Threats to validity
    # ---------------------------------------------------------------
    claim_single_author_construct_threat: (
        0.95,
        "The single-author design is a documented fact about the "
        "study. The threat itself is well-recognized in case-study "
        "methodology [@RunesonHost2009].",
    ),
    claim_pilot_dimension_coverage_threat: (
        0.85,
        "The pilot used only 2 agents; while the open-ended tenth "
        "section captured 47 cross-cutting findings, residual "
        "missing-dimension risk is real (e.g. prompt engineering "
        "deliberately excluded).",
    ),
    claim_open_source_survivorship_threat: (
        0.95,
        "The exclusion of Claude Code, Copilot Workspace, Cursor, "
        "Windsurf is documented; survivorship bias is a recognized "
        "concern in any open-source corpus study.",
    ),
    claim_python_dominance_threat: (
        0.93,
        "10/13 agents are Python-implemented; SWE-bench's Python-"
        "only nature is documented [@Jimenez2024SWEbench]. The "
        "language-bias threat is well-evidenced.",
    ),
    claim_static_analysis_misses_runtime: (
        0.95,
        "Tautological: source-code analysis cannot directly observe "
        "runtime behaviour. The threat itself is methodologically "
        "well-grounded.",
    ),
    claim_analytic_not_statistical_generalizability: (
        0.92,
        "Methodological framing using Yin's case-study terminology "
        "[@Yin2018]. Well-grounded.",
    ),
    # ---------------------------------------------------------------
    # s8 Synthesis: hypothesis predictions and counter-hypotheses
    # ---------------------------------------------------------------
    claim_pred_h_compositional_design: (
        0.85,
        "If the compositional-design hypothesis holds, the auxiliary "
        "predictions (recurring primitives across agents, 11/13 "
        "multi-primitive concentration, explicit decoupling in "
        "Moatless dual-flow) follow logically and are documented.",
    ),
    claim_alt_arbitrary_cosmetic: (
        0.30,
        "The arbitrary-cosmetic alternative is empirically weak: it "
        "would predict no shared primitives, uniform scatter, and no "
        "explicit decoupling -- none of which hold. Pi(Alt) is the "
        "probability the alternative *alone* explains the spectral "
        "diversity, which is low.",
    ),
    claim_pred_alt_arbitrary: (
        0.25,
        "If the arbitrary-cosmetic alternative held, its predicted "
        "observables (no shared primitives, uniform scatter, no "
        "decoupling design pattern) would manifest. They do not, so "
        "this prediction's compatibility with observation is low.",
    ),
    claim_counter_uniform_convergence: (
        0.25,
        "Counter-hypothesis used to formalize the convergence/"
        "divergence pattern as informative. Empirically weak: the "
        "paper documents a clear mixed pattern. Prior is low; the "
        "contradiction operator further suppresses it.",
    ),
}
