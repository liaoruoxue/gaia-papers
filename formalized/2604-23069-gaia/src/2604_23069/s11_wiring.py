"""Pass 2 wiring: strategies, abductions, inductions, contradictions for the
Wu et al. (2026) ContextWeaver formalization.

Strategy-type conventions:

* `support` -- soft deduction with author-specified prior. Default for
  "premises imply conclusion" with empirical or interpretive uncertainty.
* `abduction` -- inference to best explanation. Used for the central
  *quality + efficiency joint gain* (CW's dependency mechanism vs. the
  more-compute alternative) and for the Unified-vs-Hybrid contrast.
* `induction` -- chained binary composite. Used to support generalization
  across (Verified, Lite) and across (Claude/Unified, GPT-5/Hybrid).
* `contradiction` -- two foils:
    (i) the prevailing assumption that retrieval/recency-based memory is
        sufficient vs. the multi-component case-study + main-results
        evidence;
    (ii) "more compute always improves agent performance" vs. CW's
        simultaneous gain + token-savings + iteration-savings pattern.
"""

from gaia.lang import (
    abduction,
    compare,
    contradiction,
    induction,
    support,
)

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from .motivation import (
    claim_cw_three_components,
    claim_dependency_modeling_thesis,
    claim_efficiency_quality_jointly,
    claim_existing_methods_taxonomy,
    claim_headline_swe_bench,
    claim_recency_salience_similarity,
    claim_separate_layers_assumption,
    claim_signals_miss_dependency_structure,
    setup_causal_vs_logical,
    setup_context_length_pressure,
    setup_history_format,
    setup_long_context_degradation,
    setup_tool_using_agent,
)
from .s2_related_work import (
    claim_acon_optimization,
    claim_amem_focus,
    claim_compression_lacks_dependency,
    claim_cot_baseline,
    claim_cw_complements_static,
    claim_cw_distinguished_from_episodic_graphs,
    claim_cw_organized_by_dependency_graph,
    claim_dependency_gap_synthesis,
    claim_generative_agents_components,
    claim_gist_tokens,
    claim_lindenbauer_observation_masking,
    claim_memgpt_components,
    claim_openhands_agentless_static,
    claim_openhands_condenser,
    claim_reflexion_components,
    claim_retrieval_lacks_dependency,
    claim_selective_context,
    claim_static_does_not_model_dynamics,
    claim_summarization_flat_loses_structure,
    claim_swe_agent_condensation,
    claim_token_embedding_compression,
    claim_tot_got_episode_focus,
)
from .s3_setup import (
    claim_algorithm1_steps,
    claim_dag_information_flow,
    claim_local_incremental_design,
    claim_warmup_branch,
    claim_weaved_context_definition,
    setup_dag_structure,
    setup_hyperparameters,
    setup_node_definition,
    setup_node_extraction_map,
)
from .s4_dependency_construction import (
    claim_ancestry_bfs,
    claim_ancestry_purpose,
    claim_compression_parity_with_baseline,
    claim_context_weaving_rule,
    claim_logical_analyzer_prompt_design,
    claim_logical_dependency_analyzer,
    claim_node_extraction_query_conditioned,
    claim_node_summary_content,
    claim_observation_compression_format,
    claim_parent_selection_is_reasoning,
    claim_prepended_test_summary,
    claim_top_m_parents,
    claim_walkthrough_pytest_5262,
)
from .s5_dependency_summarization import (
    claim_dep_summary_usage_discipline,
    claim_incremental_advantage_cost,
    claim_incremental_advantage_structure,
    claim_incremental_recurrence,
    claim_root_to_step_reusable_unit,
    setup_dependency_summary_field,
    setup_llmsum_summarizer,
)
from .s6_validation_layer import (
    claim_failed_skipped_during_construction,
    claim_passed_unknown_form_backbone,
    claim_superseded_skipped,
    claim_testtracker_extraction,
    claim_testtracker_supersedes_pointer,
    claim_two_signals_rationale,
    claim_validation_closes_loop,
    claim_validation_status_labels,
    setup_validation_two_signals,
)
from .s7_evaluation import (
    claim_unified_vs_hybrid_regimes,
    claim_variance_protocol,
    setup_baseline_compression_parity,
    setup_metrics,
    setup_shared_configuration,
    setup_sliding_window_baseline,
    setup_summarization_baseline,
    setup_swe_agent_framework,
    setup_swe_bench,
    setup_swe_subsets,
    setup_three_llms,
)
from .s8_main_results import (
    claim_case_django_14631,
    claim_case_pytest_7205,
    claim_case_takeaway,
    claim_claude_unified_lite,
    claim_claude_unified_verified,
    claim_cw_avoids_summarization_pitfall,
    claim_gemini_unified_lite_gain,
    claim_gemini_unified_verified_loss,
    claim_gpt5_hybrid_lite,
    claim_gpt5_hybrid_verified,
    claim_gpt5_unified_underperforms,
    claim_iteration_budget_scaling,
    claim_iteration_distribution_tail,
    claim_iteration_savings_appendix_f,
    claim_lower_variance,
    claim_qualitative_38_vs_27,
    claim_qualitative_recency_bias,
    claim_summarization_uneven,
    claim_table1_full,
    claim_table2_subset_variance,
    claim_token_per_instance_parity,
    claim_tokens_per_resolve_savings,
)
from .s9_ablations import (
    claim_ablation_components_summary,
    claim_dag_chosen_for_stability,
    claim_gpt4o_generalization,
    claim_table3a_dag_vs_tree,
    claim_table3b_window_size,
    claim_table4a_gpt4o_sanity_check,
    claim_window_insensitive,
)
from .s10_discussion_limitations import (
    claim_central_argument_restated,
    claim_conclusion_summary,
    claim_future_work_directions,
    claim_limit_diverse_signals_future,
    claim_limit_llm_dependency,
    claim_limit_test_driven_environments,
    claim_practical_extensions,
    claim_shared_challenges,
    claim_takeaway_appendix_e1,
)

# ---------------------------------------------------------------------------
# Section 1 (Motivation) wiring
# ---------------------------------------------------------------------------

strat_existing_methods_share_signal = support(
    [claim_existing_methods_taxonomy],
    claim_recency_salience_similarity,
    background=[setup_tool_using_agent, setup_context_length_pressure],
    reason=(
        "Across the three families enumerated in "
        "@claim_existing_methods_taxonomy, the underlying selection signal is "
        "uniformly recency (sliding window), salience (gist tokens, "
        "selective context, LLMLingua, AutoCompress), or semantic "
        "similarity (MemGPT, Generative Agents, Reflexion). The taxonomy "
        "therefore directly entails the unified-signal characterization "
        "@claim_recency_salience_similarity. Setting "
        "@setup_tool_using_agent and "
        "@setup_context_length_pressure motivate why these methods are "
        "deployed in the first place."
    ),
    prior=0.93,
)

strat_signals_miss_structure = support(
    [claim_recency_salience_similarity],
    claim_signals_miss_dependency_structure,
    background=[setup_tool_using_agent, setup_history_format, setup_causal_vs_logical],
    reason=(
        "Given the paper's definitions of causal/logical dependencies "
        "(@setup_causal_vs_logical) and the unified-signal "
        "characterization (@claim_recency_salience_similarity), "
        "the dependency-structure between steps is by construction "
        "*not* what those signals score. Sliding window scores by "
        "position; salience methods score by token-level information "
        "density; similarity methods score by embedding distance to a "
        "query. None of these scores reads off whether step-i's "
        "*output* was used by step-j's reasoning, so important "
        "premises whose token-level density or recency is low can be "
        "dropped, leading to broken plans and repeated exploration "
        "(setting @setup_history_format defines the relevant "
        "T-A-O step structure)."
    ),
    prior=0.92,
)

strat_compression_lacks_dependency = support(
    [
        claim_gist_tokens,
        claim_selective_context,
        claim_token_embedding_compression,
    ],
    claim_compression_lacks_dependency,
    reason=(
        "The four cited compression approaches "
        "(gist tokens @claim_gist_tokens, selective context "
        "@claim_selective_context, LLMLingua + AutoCompress "
        "@claim_token_embedding_compression) all operate on token-level "
        "or embedding-level signals about *individual* token importance, "
        "without referring to which token was generated *because of* "
        "which earlier token. Compression is therefore "
        "dependency-blind."
    ),
    prior=0.92,
)

strat_retrieval_lacks_dependency = support(
    [
        claim_memgpt_components,
        claim_generative_agents_components,
        claim_reflexion_components,
    ],
    claim_retrieval_lacks_dependency,
    reason=(
        "The three retrieval/hierarchical-memory systems cited "
        "(MemGPT @claim_memgpt_components, Generative Agents "
        "@claim_generative_agents_components, Reflexion "
        "@claim_reflexion_components) all retrieve content by "
        "similarity / recency / reflection and concatenate retrieved "
        "fragments as a flat token stream. The retrieval mechanism does "
        "not preserve inter-step dependency edges; once retrieved, "
        "fragments lose the structural relationship that made them "
        "individually relevant."
    ),
    prior=0.9,
)

strat_episodic_graphs_distinct = support(
    [claim_cot_baseline, claim_tot_got_episode_focus, claim_amem_focus],
    claim_cw_distinguished_from_episodic_graphs,
    reason=(
        "CoT (@claim_cot_baseline), ToT/GoT (@claim_tot_got_episode_focus), "
        "and A-Mem (@claim_amem_focus) all build graph or tree "
        "structures, but ToT/GoT operate within a single inference "
        "episode (search over alternatives) and A-Mem focuses on "
        "construction/retrieval rather than dependency-driven pruning. "
        "ContextWeaver instead constructs an information-flow DAG over "
        "the *executed trajectory* and maintains a validity-aware "
        "structure across the entire long-running session."
    ),
    prior=0.88,
)

strat_static_complementary = support(
    [claim_openhands_agentless_static, claim_static_does_not_model_dynamics],
    claim_cw_complements_static,
    reason=(
        "Static analysis tools (@claim_openhands_agentless_static) "
        "describe code structure but miss runtime dynamic context "
        "(@claim_static_does_not_model_dynamics). Because ContextWeaver "
        "models the *interaction history* rather than the static code "
        "structure, the two are orthogonal information sources and "
        "therefore complementary rather than substitutes."
    ),
    prior=0.93,
)

strat_summarization_loses_structure = support(
    [
        claim_swe_agent_condensation,
        claim_openhands_condenser,
        claim_acon_optimization,
        claim_lindenbauer_observation_masking,
    ],
    claim_summarization_flat_loses_structure,
    reason=(
        "All four LLM-summarization variants cited "
        "(@claim_swe_agent_condensation, @claim_openhands_condenser, "
        "@claim_acon_optimization, @claim_lindenbauer_observation_masking) "
        "produce flat textual condensations. Whatever the prompt-"
        "engineering or compression-guideline strategy, the output is "
        "prose; once collapsed, the dependency structure (which step "
        "needed which earlier output) cannot be selectively retrieved "
        "by causal/logical relevance. The Lindenbauer 2025 observation "
        "that simple masking matches summarization is independent "
        "evidence that the summarization step itself is not "
        "delivering structural information beyond what masking "
        "achieves."
    ),
    prior=0.9,
)

strat_cw_organized_dep_graph = support(
    [
        claim_summarization_flat_loses_structure,
        claim_weaved_context_definition,
        claim_dag_information_flow,
    ],
    claim_cw_organized_by_dependency_graph,
    reason=(
        "Whereas summarization collapses structure "
        "(@claim_summarization_flat_loses_structure), ContextWeaver's "
        "weaved context (@claim_weaved_context_definition) is built "
        "from a persistent DAG organized by information flow "
        "(@claim_dag_information_flow). The DAG persists across steps, "
        "so dependency-aware selective retrieval is possible at every "
        "decision point."
    ),
    prior=0.93,
)

strat_dependency_gap_synthesis = support(
    [
        claim_compression_lacks_dependency,
        claim_retrieval_lacks_dependency,
        claim_cw_distinguished_from_episodic_graphs,
        claim_static_does_not_model_dynamics,
        claim_summarization_flat_loses_structure,
    ],
    claim_dependency_gap_synthesis,
    reason=(
        "Across compression (@claim_compression_lacks_dependency), "
        "retrieval (@claim_retrieval_lacks_dependency), episodic "
        "reasoning graphs (@claim_cw_distinguished_from_episodic_graphs), "
        "static analysis (@claim_static_does_not_model_dynamics), and "
        "LLM summarization (@claim_summarization_flat_loses_structure), "
        "every neighborhood lacks cross-trajectory inter-step "
        "dependency modeling. The synthesis claim therefore follows "
        "from inspecting each neighborhood in turn."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# Section 3 wiring -- algorithm components and design choices
# ---------------------------------------------------------------------------

strat_algorithm1_decomposition = support(
    [claim_dag_information_flow],
    claim_algorithm1_steps,
    background=[
        setup_node_definition,
        setup_node_extraction_map,
        setup_dag_structure,
        setup_hyperparameters,
    ],
    reason=(
        "Algorithm 1's four-step decomposition implements the "
        "information-flow DAG construction "
        "(@claim_dag_information_flow). The background settings "
        "-- node structure (@setup_node_definition), the extraction "
        "map (@setup_node_extraction_map), DAG structure "
        "(@setup_dag_structure), and hyperparameters "
        "(@setup_hyperparameters) -- fix what each step does."
    ),
    prior=0.96,
)

strat_dag_information_flow = support(
    [claim_parent_selection_is_reasoning],
    claim_dag_information_flow,
    background=[setup_dag_structure],
    reason=(
        "Because the DAG structure (@setup_dag_structure) allows "
        "multiple parents per node and parent selection is treated as "
        "reasoning over information flow rather than similarity "
        "(@claim_parent_selection_is_reasoning), the resulting graph "
        "naturally encodes information flow rather than recency."
    ),
    prior=0.94,
)

strat_node_extraction_query_conditioned = support(
    [claim_node_summary_content],
    claim_node_extraction_query_conditioned,
    background=[setup_node_extraction_map, setup_node_definition],
    reason=(
        "By definition (@setup_node_extraction_map), the extractor phi "
        "takes both H_k and Q as inputs. Combined with the structured "
        "node fields (@setup_node_definition) and the summary content "
        "specification (@claim_node_summary_content), the extractor's "
        "output is necessarily query-conditioned."
    ),
    prior=0.95,
)

strat_logical_analyzer_implements_top_m = support(
    [claim_logical_dependency_analyzer, claim_logical_analyzer_prompt_design],
    claim_top_m_parents,
    reason=(
        "The analyzer score function (@claim_logical_dependency_analyzer) "
        "and the structured prompt that operationalizes it "
        "(@claim_logical_analyzer_prompt_design) together produce a "
        "ranking from which the top-m candidates are selected as the "
        "parent set S_k."
    ),
    prior=0.95,
)

strat_parent_selection_reasoning = support(
    [claim_logical_analyzer_prompt_design, claim_logical_dependency_analyzer],
    claim_parent_selection_is_reasoning,
    reason=(
        "The analyzer prompt (@claim_logical_analyzer_prompt_design) "
        "explicitly enumerates analysis questions about information "
        "flow and causal relationships, instructs the model to ignore "
        "temporal proximity and file similarity, and emits "
        "structured per-candidate reasoning JSON. The combination "
        "operationalizes parent selection as a reasoning task, not a "
        "similarity check."
    ),
    prior=0.93,
)

strat_ancestry_drives_selectivity = support(
    [claim_ancestry_bfs, claim_context_weaving_rule],
    claim_ancestry_purpose,
    reason=(
        "Combining the BFS-derived ancestry set (@claim_ancestry_bfs) "
        "with the context-weaving rule (@claim_context_weaving_rule) "
        "shows directly that membership in A is the on/off switch "
        "between full retention and observation compression."
    ),
    prior=0.97,
)

strat_compression_parity = support(
    [claim_observation_compression_format],
    claim_compression_parity_with_baseline,
    background=[setup_baseline_compression_parity],
    reason=(
        "The observation-compression placeholder format "
        "(@claim_observation_compression_format) is shared between "
        "ContextWeaver and the sliding-window baseline "
        "(@setup_baseline_compression_parity). Therefore the only "
        "difference between conditions is *which* entries are kept "
        "verbatim -- the selection mechanism, not the compression "
        "intensity -- isolating the contribution of dependency-based "
        "selection."
    ),
    prior=0.96,
)

strat_local_incremental = support(
    [claim_warmup_branch, claim_algorithm1_steps],
    claim_local_incremental_design,
    reason=(
        "Algorithm 1 (@claim_algorithm1_steps) only processes the "
        "newest step at each call (extract -> select parents -> "
        "BFS -> weave) and uses a warmup branch (@claim_warmup_branch) "
        "to short-circuit early steps; the existing graph state is "
        "extended rather than rebuilt. This yields a local, "
        "incremental design suitable for long-running sessions."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Section 3.2 wiring -- dependency summarizer
# ---------------------------------------------------------------------------

strat_incremental_recurrence = support(
    [claim_node_summary_content],
    claim_incremental_recurrence,
    background=[setup_dependency_summary_field, setup_llmsum_summarizer],
    reason=(
        "Given the per-node dependency-summary field "
        "(@setup_dependency_summary_field) and the dedicated summarizer "
        "function (@setup_llmsum_summarizer), each node also carries a "
        "summary (@claim_node_summary_content), and the recurrence "
        "dep_summary_k = LLMSUM({parent.dep_summary}, summary_k) is "
        "the explicit construction the paper specifies."
    ),
    prior=0.96,
)

strat_summary_advantage_cost = support(
    [claim_incremental_recurrence, claim_root_to_step_reusable_unit],
    claim_incremental_advantage_cost,
    reason=(
        "Because each node's dependency summary is computed once and "
        "cached (@claim_root_to_step_reusable_unit), the recurrence "
        "(@claim_incremental_recurrence) consumes only |S_k| parent "
        "summaries plus the new step's summary at each step -- O(|S_k|) "
        "rather than O(k) full-history re-summarizations. This "
        "directly yields substantial compute savings on long "
        "trajectories."
    ),
    prior=0.92,
)

strat_summary_advantage_structure = support(
    [claim_incremental_recurrence, claim_dag_information_flow],
    claim_incremental_advantage_structure,
    reason=(
        "The recurrence (@claim_incremental_recurrence) preserves "
        "branch/merge structure because each node's summary is "
        "computed from its specific parent set, not from a flattened "
        "trajectory. Combined with the DAG's information-flow "
        "organization (@claim_dag_information_flow), the per-node "
        "summary preserves the dependency-structured shape of "
        "reasoning."
    ),
    prior=0.9,
)

strat_summary_reusable_unit = support(
    [claim_incremental_recurrence],
    claim_root_to_step_reusable_unit,
    reason=(
        "The recurrence (@claim_incremental_recurrence) caches "
        "dep_summary_k on each node. Subsequent descendants invoke "
        "LLMSUM with their parent's cached summary as input, so each "
        "summary serves as a reusable unit for all later descendants."
    ),
    prior=0.93,
)

# ---------------------------------------------------------------------------
# Section 3.3 wiring -- validation layer
# ---------------------------------------------------------------------------

strat_validation_status_labels = support(
    [claim_testtracker_extraction],
    claim_validation_status_labels,
    background=[setup_validation_two_signals],
    reason=(
        "Given the two-granularity setup (@setup_validation_two_signals) "
        "and the TestTracker that extracts per-test outcomes "
        "(@claim_testtracker_extraction), the ValidationDetector "
        "aggregates these into one of four node-level labels "
        "(passed / failed / unknown / superseded)."
    ),
    prior=0.96,
)

strat_failed_skipped = support(
    [claim_validation_status_labels],
    claim_failed_skipped_during_construction,
    reason=(
        "Given the four-label scheme (@claim_validation_status_labels), "
        "Algorithm 1 line 2 explicitly excludes nodes labelled FAILED "
        "from the candidate set C_k for parent selection."
    ),
    prior=0.97,
)

strat_passed_unknown_backbone = support(
    [claim_validation_status_labels, claim_failed_skipped_during_construction],
    claim_passed_unknown_form_backbone,
    reason=(
        "Once failed nodes are excluded "
        "(@claim_failed_skipped_during_construction) and superseded "
        "nodes are similarly skipped, only passed and unknown nodes "
        "remain candidates (@claim_validation_status_labels). These "
        "form the reliable backbone the analyzer can build on."
    ),
    prior=0.95,
)

strat_superseded_skipped = support(
    [claim_validation_status_labels, claim_testtracker_supersedes_pointer],
    claim_superseded_skipped,
    reason=(
        "Once a corrective node creates the superseded pointer "
        "(@claim_testtracker_supersedes_pointer), the validation "
        "label flips to superseded (@claim_validation_status_labels) "
        "and parent selection skips the stale node."
    ),
    prior=0.95,
)

strat_two_signals_rationale = support(
    [claim_validation_status_labels],
    claim_two_signals_rationale,
    background=[setup_validation_two_signals],
    reason=(
        "Keeping the coarse label separate from the detailed test-"
        "results field (@setup_validation_two_signals, "
        "@claim_validation_status_labels) means construction-time "
        "decisions ('skip failed parents') need only consult the label "
        "rather than re-parse pytest logs."
    ),
    prior=0.94,
)

strat_validation_closes_loop = support(
    [claim_prepended_test_summary, claim_validation_status_labels],
    claim_validation_closes_loop,
    reason=(
        "Prepending the most-recent validation summary "
        "(@claim_prepended_test_summary) feeds the labels "
        "(@claim_validation_status_labels) directly back into the "
        "agent's next decision -- closing the reasoning-execution loop."
    ),
    prior=0.93,
)

# ---------------------------------------------------------------------------
# Section 4 wiring -- main empirical results
# ---------------------------------------------------------------------------

# Per-(model, benchmark) decomposition of Table 1
strat_table1_claude_unified_verified = support(
    [claim_table1_full],
    claim_claude_unified_verified,
    reason=(
        "Table 1 (@claim_table1_full) reports Claude Sonnet 4 / "
        "Unified / Verified pass@1 = 66.0% for ContextWeaver vs 63.2% "
        "for Sliding Window."
    ),
    prior=0.97,
)

strat_table1_claude_unified_lite = support(
    [claim_table1_full],
    claim_claude_unified_lite,
    reason=(
        "Table 1 (@claim_table1_full) reports Claude Sonnet 4 / "
        "Unified / Lite pass@1 = 53.7% for ContextWeaver vs 52.3% for "
        "Sliding Window."
    ),
    prior=0.97,
)

strat_table1_gpt5_hybrid_verified = support(
    [claim_table1_full],
    claim_gpt5_hybrid_verified,
    reason=(
        "Table 1 (@claim_table1_full) reports GPT-5 / Hybrid / "
        "Verified pass@1 = 58.6% for ContextWeaver vs 57.4% Sliding "
        "Window."
    ),
    prior=0.97,
)

strat_table1_gpt5_hybrid_lite = support(
    [claim_table1_full],
    claim_gpt5_hybrid_lite,
    reason=(
        "Table 1 (@claim_table1_full) reports GPT-5 / Hybrid / Lite "
        "pass@1 = 51.3% for ContextWeaver vs 48.3% Sliding Window."
    ),
    prior=0.97,
)

strat_table1_gpt5_unified_underperforms = support(
    [claim_table1_full],
    claim_gpt5_unified_underperforms,
    reason=(
        "Table 1 (@claim_table1_full) directly reports GPT-5 / Unified "
        "ContextWeaver below Sliding Window on both Verified (56.8 vs "
        "57.4) and Lite (42.0 vs 48.3). The under-performance is a "
        "direct read of the table."
    ),
    prior=0.96,
)

strat_table1_gemini_lite_gain = support(
    [claim_table1_full],
    claim_gemini_unified_lite_gain,
    reason=(
        "Table 1 (@claim_table1_full) reports Gemini 3 Flash / Lite "
        "pass@1 = 47.0% for ContextWeaver vs 46.0% Sliding Window."
    ),
    prior=0.97,
)

strat_table1_gemini_verified_loss = support(
    [claim_table1_full],
    claim_gemini_unified_verified_loss,
    reason=(
        "Table 1 (@claim_table1_full) reports Gemini 3 Flash / "
        "Verified pass@1 = 58.4% for ContextWeaver vs 60.4% Sliding "
        "Window."
    ),
    prior=0.97,
)

strat_summarization_uneven = support(
    [claim_table1_full],
    claim_summarization_uneven,
    reason=(
        "Reading down the LLM Summarization rows of Table 1 "
        "(@claim_table1_full) shows the conditional pattern: "
        "summarization helps Claude (64.2/53.0 vs SW 63.2/52.3) but "
        "hurts Gemini (56.8/43.3 vs SW 60.4/46.0) and GPT-5 "
        "(46.7/32.3 vs SW 57.4/48.3)."
    ),
    prior=0.95,
)

strat_cw_avoids_summarization_pitfall = support(
    [
        claim_summarization_uneven,
        claim_observation_compression_format,
        claim_compression_parity_with_baseline,
    ],
    claim_cw_avoids_summarization_pitfall,
    reason=(
        "The summarization-uneven pattern (@claim_summarization_uneven) "
        "is consistent with weaker models dropping crucial details "
        "during prose compression. Because ContextWeaver keeps raw "
        "observations (@claim_observation_compression_format) and "
        "selects what to retain via the dependency graph -- with "
        "compression parity to the baseline "
        "(@claim_compression_parity_with_baseline) -- it does not "
        "rely on the model's prose-compression skill."
    ),
    prior=0.88,
)

# Induction across (Claude/Unified, GPT-5/Hybrid, Gemini/Lite) for headline gain
strat_law_cw_beats_sw = support(
    [claim_headline_swe_bench],
    claim_claude_unified_verified,
    reason=(
        "If the headline law (@claim_headline_swe_bench) -- "
        "ContextWeaver beats Sliding Window on SWE-Bench Verified "
        "and Lite under sufficient graph-construction quality -- "
        "holds, it predicts the Claude/Unified/Verified gain "
        "observed in Table 1."
    ),
    prior=0.85,
)

strat_law_cw_beats_sw_2 = support(
    [claim_headline_swe_bench],
    claim_gpt5_hybrid_verified,
    reason=(
        "The headline law (@claim_headline_swe_bench) predicts the "
        "GPT-5/Hybrid/Verified gain when graph construction is held to "
        "high quality (Claude builds the graph)."
    ),
    prior=0.85,
)

strat_law_cw_beats_sw_3 = support(
    [claim_headline_swe_bench],
    claim_gpt5_hybrid_lite,
    reason=(
        "The headline law (@claim_headline_swe_bench) predicts the "
        "GPT-5/Hybrid/Lite gain when graph construction is held to "
        "high quality."
    ),
    prior=0.85,
)

ind_cw_law_12 = induction(
    strat_law_cw_beats_sw,
    strat_law_cw_beats_sw_2,
    law=claim_headline_swe_bench,
    reason=(
        "Independent confirmations from Claude/Unified/Verified and "
        "GPT-5/Hybrid/Verified -- two different backbone models on the "
        "same Verified split."
    ),
)

ind_cw_law_123 = induction(
    ind_cw_law_12,
    strat_law_cw_beats_sw_3,
    law=claim_headline_swe_bench,
    reason=(
        "Adds the GPT-5/Hybrid/Lite confirmation, generalizing across "
        "benchmarks (Verified + Lite) as well as backbones."
    ),
)

# Iteration / token efficiency wiring
strat_per_instance_token_parity = support(
    [
        claim_iteration_savings_appendix_f,
        claim_iteration_budget_scaling,
    ],
    claim_token_per_instance_parity,
    reason=(
        "The iteration-budget scaling result "
        "(@claim_iteration_budget_scaling) and per-budget iteration "
        "savings (@claim_iteration_savings_appendix_f) together "
        "establish that ContextWeaver does not consume more tokens "
        "per instance than Sliding Window -- because per-step token "
        "consumption is comparable and CW uses fewer steps, "
        "per-instance tokens land near parity rather than higher."
    ),
    prior=0.85,
)

strat_tokens_per_resolve_savings = support(
    [
        claim_token_per_instance_parity,
        claim_iteration_savings_appendix_f,
    ],
    claim_tokens_per_resolve_savings,
    reason=(
        "Given approximate per-instance token parity "
        "(@claim_token_per_instance_parity) and a higher resolve rate "
        "(combined with iteration savings "
        "@claim_iteration_savings_appendix_f), tokens-per-resolve "
        "is lower: same numerator (per-instance tokens) divided by "
        "more successful resolves yields the reported -2.8% (Verified) "
        "and -2.3% (Lite) savings."
    ),
    prior=0.88,
)

strat_iteration_distribution = support(
    [claim_iteration_distribution_tail, claim_iteration_budget_scaling],
    claim_iteration_savings_appendix_f,
    reason=(
        "The percentile analysis (@claim_iteration_distribution_tail) "
        "shows ContextWeaver shifting the curve down at every "
        "percentile, especially in the upper tail. Combined with the "
        "iteration-budget scaling result "
        "(@claim_iteration_budget_scaling), aggregating yields the "
        "observed average iteration savings (-4.7% Verified, -7.3% "
        "Lite)."
    ),
    prior=0.9,
)

# Variance / Table 2
strat_lower_variance = support(
    [claim_table2_subset_variance, claim_variance_protocol],
    claim_lower_variance,
    background=[setup_swe_subsets],
    reason=(
        "Table 2 (@claim_table2_subset_variance), via the 5-run "
        "protocol (@claim_variance_protocol), reports CW std 1.55 vs "
        "SW std 1.94 on the 100-instance Verified subset "
        "(@setup_swe_subsets)."
    ),
    prior=0.96,
)

# Case-study to scope claim
strat_case_takeaway = support(
    [claim_case_django_14631, claim_case_pytest_7205],
    claim_case_takeaway,
    reason=(
        "The django-14631 case (@claim_case_django_14631) shows "
        "ContextWeaver winning on a multi-component cross-file task; "
        "the pytest-7205 case (@claim_case_pytest_7205) shows Sliding "
        "Window winning on a single-location linear task. Together "
        "they support the scope claim: dependency-aware memory helps "
        "long-range cross-file tasks; recency-based selection wins "
        "for sequential local fixes."
    ),
    prior=0.85,
)

strat_qualitative_recency_bias = support(
    [claim_qualitative_38_vs_27, claim_qualitative_recency_bias],
    claim_takeaway_appendix_e1,
    reason=(
        "The unique-success counts (@claim_qualitative_38_vs_27) plus "
        "the failure-mode characterization "
        "(@claim_qualitative_recency_bias) directly support the "
        "Appendix E.1 takeaway about stable file localization and "
        "early-evidence reuse."
    ),
    prior=0.87,
)

# ---------------------------------------------------------------------------
# Section 4.5-4.6 ablations -> design choices
# ---------------------------------------------------------------------------

strat_dag_chosen_for_stability = support(
    [claim_table3a_dag_vs_tree],
    claim_dag_chosen_for_stability,
    reason=(
        "Table 3a (@claim_table3a_dag_vs_tree) shows mean Pass@1 of "
        "DAG (68.0) and Tree (67.0) within ~1pp but DAG std (1.55) "
        "vs Tree std (2.92) -- the choice is for stability, not mean."
    ),
    prior=0.94,
)

strat_window_insensitive = support(
    [claim_table3b_window_size],
    claim_window_insensitive,
    reason=(
        "Table 3b (@claim_table3b_window_size) shows pass@1 across "
        "W in {5, 7, 9} of 68.0/66.0/67.4 -- within ~2pp range, no "
        "strong sensitivity."
    ),
    prior=0.95,
)

strat_gpt4o_generalization = support(
    [claim_table4a_gpt4o_sanity_check],
    claim_gpt4o_generalization,
    reason=(
        "Table 4a (@claim_table4a_gpt4o_sanity_check) reports CW "
        "28.6+/-2.70 vs SW 26.6+/-3.50 on GPT-4o, supporting "
        "cross-model generalization of the ContextWeaver advantage."
    ),
    prior=0.85,
)

strat_ablation_summary = support(
    [
        claim_table3a_dag_vs_tree,
        claim_table3b_window_size,
        claim_table2_subset_variance,
        claim_table4a_gpt4o_sanity_check,
    ],
    claim_ablation_components_summary,
    reason=(
        "The four ablation/sensitivity studies (DAG vs Tree "
        "@claim_table3a_dag_vs_tree, window size "
        "@claim_table3b_window_size, variance subset "
        "@claim_table2_subset_variance, GPT-4o sanity check "
        "@claim_table4a_gpt4o_sanity_check) together cover the "
        "ablation/robustness dimensions reported. Per-component drop "
        "ablations (validation off, summarizer off) are not "
        "reported -- so the per-component evidence remains "
        "architectural rather than fully ablation-isolated."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# Headline argument: composition of the headline empirical claim
# ---------------------------------------------------------------------------

strat_headline_empirical = support(
    [
        claim_claude_unified_verified,  # generalization established via induction over Verified+Lite
        claim_gpt5_hybrid_lite,  # induction completes cross-(model, benchmark)
        claim_tokens_per_resolve_savings,  # token efficiency
        claim_iteration_savings_appendix_f,  # iteration efficiency
        claim_lower_variance,  # stability
    ],
    claim_headline_swe_bench,
    reason=(
        "The headline result (@claim_headline_swe_bench) is the "
        "conjunction of: (i) the per-(model, benchmark) pass@1 gains "
        "(induction across Claude/Unified/Verified "
        "@claim_claude_unified_verified, GPT-5/Hybrid/Lite "
        "@claim_gpt5_hybrid_lite, completed by @ind_cw_law_123); "
        "(ii) the tokens-per-resolve savings "
        "(@claim_tokens_per_resolve_savings); (iii) the iteration "
        "savings (@claim_iteration_savings_appendix_f); and (iv) the "
        "lower run-to-run variance (@claim_lower_variance). "
        "Together these instantiate the abstract: 'improves pass@1 "
        "while reducing reasoning steps and token usage.'"
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# Central thesis composition
# ---------------------------------------------------------------------------

strat_dependency_modeling_thesis = support(
    [
        claim_cw_three_components,
        claim_headline_swe_bench,
        claim_lower_variance,
        claim_dependency_gap_synthesis,
    ],
    claim_dependency_modeling_thesis,
    reason=(
        "The thesis -- modeling logical/causal dependencies provides "
        "stable + scalable agent memory -- is supported by: the "
        "three-component design (@claim_cw_three_components) showing "
        "*how* dependencies are modeled; the headline empirical "
        "result (@claim_headline_swe_bench) showing dependency-aware "
        "memory wins on solve rate + steps + tokens; the lower "
        "variance (@claim_lower_variance) directly evidencing "
        "stability; and the related-work synthesis "
        "(@claim_dependency_gap_synthesis) showing prior work has "
        "this gap."
    ),
    prior=0.88,
)

# ---------------------------------------------------------------------------
# Conclusion + central argument
# ---------------------------------------------------------------------------

strat_conclusion = support(
    [
        claim_dependency_modeling_thesis,
        claim_cw_three_components,
        claim_weaved_context_definition,
    ],
    claim_conclusion_summary,
    reason=(
        "The conclusion summary follows from the central thesis "
        "(@claim_dependency_modeling_thesis), the three-component "
        "design (@claim_cw_three_components), and the weaved-context "
        "definition (@claim_weaved_context_definition) which together "
        "specify how only future-action-relevant steps are retained "
        "under a fixed token budget."
    ),
    prior=0.93,
)

strat_central_argument = support(
    [
        claim_dependency_modeling_thesis,
        claim_headline_swe_bench,
        claim_takeaway_appendix_e1,
    ],
    claim_central_argument_restated,
    reason=(
        "The restated central argument is the conjunction of the "
        "thesis (@claim_dependency_modeling_thesis), the headline "
        "empirical result (@claim_headline_swe_bench), and the "
        "qualitative-error-analysis takeaway "
        "(@claim_takeaway_appendix_e1) about more stable file "
        "localization and reuse of early evidence."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# Limitations: graph-quality dependence
# ---------------------------------------------------------------------------

strat_llm_dependency_limit = support(
    [claim_gpt5_unified_underperforms, claim_gemini_unified_verified_loss],
    claim_limit_llm_dependency,
    reason=(
        "GPT-5/Unified underperforms (@claim_gpt5_unified_underperforms) "
        "and Gemini/Unified/Verified underperforms "
        "(@claim_gemini_unified_verified_loss). Both are direct "
        "evidence of the limitation that ContextWeaver's effectiveness "
        "depends on the backbone LLM's ability to construct "
        "high-quality dependency graphs."
    ),
    prior=0.92,
)

# Wire the test-driven scope limitation
strat_test_driven_scope = support(
    [claim_validation_status_labels, claim_testtracker_extraction],
    claim_limit_test_driven_environments,
    reason=(
        "The validation layer relies on parseable test outcomes "
        "(@claim_testtracker_extraction) to assign node-level labels "
        "(@claim_validation_status_labels). This binds the framework's "
        "evaluation scope to environments where such validation "
        "signals exist (e.g., SWE-Bench)."
    ),
    prior=0.9,
)

strat_diverse_signals_future = support(
    [claim_limit_test_driven_environments],
    claim_limit_diverse_signals_future,
    reason=(
        "Given that the current scope is test-driven environments "
        "(@claim_limit_test_driven_environments), extending the "
        "Validation Layer to handle implicit assertions, runtime "
        "traces, or external validators is a natural future-work "
        "direction."
    ),
    prior=0.92,
)

# Connect future work to conclusion summary
strat_future_work_summary = support(
    [
        claim_limit_diverse_signals_future,
        claim_practical_extensions,
        claim_shared_challenges,
    ],
    claim_future_work_directions,
    reason=(
        "Future-work directions follow from the unresolved issues: "
        "diverse-signal extension (@claim_limit_diverse_signals_future), "
        "practical extensions like repository consistency checks and "
        "loop-aware budgets (@claim_practical_extensions), and "
        "remaining shared challenges (@claim_shared_challenges) such "
        "as repository-level ambiguity."
    ),
    prior=0.88,
)

# Wire shared challenges + practical extensions
strat_shared_challenges = support(
    [claim_qualitative_38_vs_27],
    claim_shared_challenges,
    reason=(
        "143 instances are unsolved by either method "
        "(@claim_qualitative_38_vs_27). Inspection of these residual "
        "failures reveals repository-level ambiguity (similarly named "
        "modules, cross-file dependencies) as a systematic shared "
        "challenge."
    ),
    prior=0.85,
)

strat_practical_extensions = support(
    [claim_shared_challenges],
    claim_practical_extensions,
    reason=(
        "From the shared-challenge inventory "
        "(@claim_shared_challenges) the paper extracts two concrete "
        "practical extensions -- lightweight repository consistency "
        "checks and loop-aware budget control -- as candidate "
        "improvements that preserve dependency-structured memory."
    ),
    prior=0.83,
)

# Wire walkthrough -> support algorithm 1
strat_walkthrough_supports_algorithm = support(
    [claim_walkthrough_pytest_5262],
    claim_algorithm1_steps,
    reason=(
        "The pytest-5262 walkthrough (@claim_walkthrough_pytest_5262) "
        "executes Algorithm 1's four sequential phases on a real "
        "instance, providing a worked example that the framework "
        "operates as specified."
    ),
    prior=0.93,
)

# Wire dependency-summary usage discipline -> tied to local incremental design
strat_dep_summary_discipline = support(
    [claim_incremental_recurrence],
    claim_dep_summary_usage_discipline,
    reason=(
        "The recurrence (@claim_incremental_recurrence) computes "
        "dep_summaries strictly for use by the parent-selection "
        "analyzer; the paper specifies they are never injected into "
        "the final agent context."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# Abduction 1: dependency mechanism vs. more-compute alternative
# ---------------------------------------------------------------------------
#
# Hypothesis: the explicit dependency-graph mechanism (CW's three components)
# explains the observation of simultaneous quality + efficiency joint gain.
# Alternative: 'more compute' (larger context, more retrieval queries,
# stronger LLM) explains the gain.
# Discriminating signal: simultaneous pass@1 increase + tokens-per-resolve
# decrease + iterations decrease. More-compute alternative would NOT show
# this pattern; it would show pass@1 up but tokens/iterations also UP.

from gaia.lang import claim as _claim_helper

# Predictions for compare (each side states what the explanation predicts
# observationally about the joint quality+efficiency pattern).
pred_dep_mech = _claim_helper(
    "**Prediction (H = dependency-graph mechanism is responsible).** "
    "If the dependency-graph mechanism causes the gains, ContextWeaver "
    "should show *simultaneous* pass@1 increase + tokens-per-resolve "
    "decrease + iteration decrease, with backbone LLM and agent "
    "framework held constant. Selectivity (not aggression) drops "
    "irrelevant content while preserving causal/logical premises.",
    title="Pred-H: dep mechanism => pass@1 UP + tokens/iters DOWN, simultaneously",
)

pred_more_compute = _claim_helper(
    "**Prediction (Alt = more-compute explains the gain).** Under "
    "the more-compute hypothesis, raising pass@1 would also raise per-"
    "instance tokens (more context, more retrieval, more thinking). "
    "The alternative cannot natively predict tokens-per-resolve DOWN "
    "with backbone fixed; it would predict tokens FLAT or UP.",
    title="Pred-Alt: more compute => pass@1 UP correlates with tokens UP",
)

# Hypothesis-support: H supports the observed efficiency_quality_jointly
strat_abd_h_dep_mechanism = support(
    [
        pred_dep_mech,
        claim_cw_three_components,
        claim_compression_parity_with_baseline,
    ],
    claim_efficiency_quality_jointly,
    reason=(
        "The dependency-graph mechanism (@claim_cw_three_components) "
        "predicts (@pred_dep_mech) the simultaneous pass@1 + "
        "efficiency pattern. Combined with compression parity "
        "(@claim_compression_parity_with_baseline) that holds "
        "compression aggressiveness constant across conditions, the "
        "mechanism cleanly explains the observed joint pattern."
    ),
    prior=0.9,
)

# Alternative-support: Alt could explain the observation but only if its
# prediction matched the data (it does not).
strat_abd_alt_more_compute = support(
    [pred_more_compute],
    claim_efficiency_quality_jointly,
    background=[setup_three_llms, setup_swe_agent_framework],
    reason=(
        "Under the more-compute alternative (@pred_more_compute), the "
        "same setup (@setup_three_llms, @setup_swe_agent_framework) "
        "with same agent framework and fixed compute per call would "
        "not naturally produce the observed simultaneous gain + "
        "savings pattern. The alternative therefore has weak "
        "explanatory power for @claim_efficiency_quality_jointly."
    ),
    prior=0.25,
)

cmp_dep_vs_more_compute = compare(
    pred_dep_mech,
    pred_more_compute,
    claim_efficiency_quality_jointly,
    reason=(
        "The H prediction (@pred_dep_mech) of pass@1 UP and "
        "tokens/iters DOWN simultaneously matches the observed "
        "joint quality+efficiency pattern "
        "(@claim_efficiency_quality_jointly), grounded in the "
        "tokens-per-resolve savings @claim_tokens_per_resolve_savings. "
        "The Alt prediction (@pred_more_compute) of tokens UP "
        "correlated with pass@1 UP is *contradicted* by that pattern. "
        "Discrimination is strong."
    ),
    prior=0.9,
)

abd_dep_vs_more_compute = abduction(
    strat_abd_h_dep_mechanism,
    strat_abd_alt_more_compute,
    cmp_dep_vs_more_compute,
    reason=(
        "Inference-to-best-explanation: which mechanism best explains "
        "ContextWeaver's pattern of simultaneous pass@1 gain + token "
        "savings + iteration savings? With backbone LLM and agent "
        "framework held constant, only the dependency-graph "
        "mechanism produces the observed signature; a more-compute "
        "hypothesis would predict tokens flat or up, not down."
    ),
)

# ---------------------------------------------------------------------------
# Abduction 2: graph-construction quality is the mediator (Unified vs Hybrid)
# ---------------------------------------------------------------------------

pred_graph_quality_mediator = _claim_helper(
    "**Prediction (H = graph-construction quality is the mediator).** "
    "If graph-construction quality (set by the memory-builder LLM) is "
    "what mediates ContextWeaver's effect, then weak builder + strong "
    "executor (Unified GPT-5) should underperform sliding window, "
    "while strong builder + same executor (Hybrid: Claude builds, "
    "GPT-5 executes) should outperform sliding window. Performance "
    "should track *who builds the graph*.",
    title="Pred-H: graph-quality mediates => Hybrid (Claude builds) flips GPT-5 result",
)

pred_execution_capability = _claim_helper(
    "**Prediction (Alt = raw execution capability dominates).** If "
    "raw execution capability is what dominates, GPT-5's relative "
    "performance to sliding window should not depend on who builds "
    "the graph. Hybrid and Unified GPT-5 should track each other.",
    title="Pred-Alt: execution dominates => Unified vs Hybrid GPT-5 track each other",
)

strat_abd_h_graph_quality_mediator = support(
    [pred_graph_quality_mediator, claim_unified_vs_hybrid_regimes],
    claim_gpt5_hybrid_verified,
    reason=(
        "The graph-quality-mediator hypothesis "
        "(@pred_graph_quality_mediator), combined with the regime "
        "definition (@claim_unified_vs_hybrid_regimes), predicts that "
        "Hybrid GPT-5 (Claude builds, GPT-5 executes) outperforms "
        "Sliding Window on Verified -- which is the observed 58.6 vs "
        "57.4 result @claim_gpt5_hybrid_verified."
    ),
    prior=0.85,
)

strat_abd_alt_execution_capability = support(
    [pred_execution_capability, claim_unified_vs_hybrid_regimes],
    claim_gpt5_hybrid_verified,
    reason=(
        "Under the execution-dominance alternative "
        "(@pred_execution_capability), the regime "
        "(@claim_unified_vs_hybrid_regimes) is essentially irrelevant "
        "and Hybrid GPT-5 vs SW should track Unified GPT-5 vs SW. "
        "But Unified GPT-5 underperforms SW while Hybrid GPT-5 "
        "outperforms it, so the alternative cannot natively explain "
        "the Hybrid-Verified result."
    ),
    prior=0.3,
)

cmp_unified_vs_hybrid_explanation = compare(
    pred_graph_quality_mediator,
    pred_execution_capability,
    claim_gpt5_hybrid_verified,
    reason=(
        "Both supports conclude @claim_gpt5_hybrid_verified (the "
        "Hybrid-GPT-5 Verified outperformance). The graph-quality-"
        "mediator prediction (@pred_graph_quality_mediator) "
        "natively predicts the Hybrid flip (Claude builds, GPT-5 "
        "executes -> outperforms SW). The execution-capability "
        "prediction (@pred_execution_capability) cannot natively "
        "account for the flip, since under that hypothesis Unified "
        "and Hybrid GPT-5 should track each other -- but Unified "
        "GPT-5 underperforms SW (@claim_gpt5_unified_underperforms) "
        "while Hybrid outperforms it. The flip pattern "
        "discriminates."
    ),
    prior=0.9,
)

abd_unified_vs_hybrid = abduction(
    strat_abd_h_graph_quality_mediator,
    strat_abd_alt_execution_capability,
    cmp_unified_vs_hybrid_explanation,
    reason=(
        "Inference-to-best-explanation for the Unified-vs-Hybrid "
        "regime contrast. Graph-construction quality (set by the "
        "memory-builder LLM) explains the GPT-5 flip; raw execution "
        "capability cannot."
    ),
)

# ---------------------------------------------------------------------------
# Contradictions
# ---------------------------------------------------------------------------

# Foil 1: existing wisdom that recency / salience / similarity selection suffices
# is contradicted by the dependency-gap synthesis, the case-study scope claim,
# and the headline result.

contra_recency_sufficient_vs_cw = contradiction(
    claim_separate_layers_assumption,
    claim_dependency_gap_synthesis,
    reason=(
        "The prevailing assumption (@claim_separate_layers_assumption) "
        "that recency/salience/similarity selection suffices for "
        "multi-step agent reasoning cannot both be true together "
        "with the dependency-gap synthesis "
        "(@claim_dependency_gap_synthesis) which establishes that "
        "every existing family LACKS dependency modeling AND that "
        "this gap matters empirically. If the prevailing assumption "
        "held, the dependency-gap synthesis (and the headline "
        "empirical result it implies) could not be true."
    ),
    prior=0.95,
)

# Foil 2 has been intentionally NOT modeled as a separate contradiction.
# The abduction abd_dep_vs_more_compute (with its compare sub-strategy)
# already encodes the 'more compute would predict tokens UP' versus the
# observed 'tokens DOWN' discrimination. Adding a separate
# `contradiction(pred_more_compute, claim_efficiency_quality_jointly)`
# would interfere with the abduction's conclusion, since
# claim_efficiency_quality_jointly is itself the abduction's observation
# variable. Keeping only the recency-sufficiency contradiction as the
# explicit hard constraint avoids this BP interference.

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    # Strategies (named so they appear in gaia check --brief)
    "strat_existing_methods_share_signal",
    "strat_signals_miss_structure",
    "strat_compression_lacks_dependency",
    "strat_retrieval_lacks_dependency",
    "strat_episodic_graphs_distinct",
    "strat_static_complementary",
    "strat_summarization_loses_structure",
    "strat_cw_organized_dep_graph",
    "strat_dependency_gap_synthesis",
    "strat_algorithm1_decomposition",
    "strat_dag_information_flow",
    "strat_node_extraction_query_conditioned",
    "strat_logical_analyzer_implements_top_m",
    "strat_parent_selection_reasoning",
    "strat_ancestry_drives_selectivity",
    "strat_compression_parity",
    "strat_local_incremental",
    "strat_incremental_recurrence",
    "strat_summary_advantage_cost",
    "strat_summary_advantage_structure",
    "strat_summary_reusable_unit",
    "strat_validation_status_labels",
    "strat_failed_skipped",
    "strat_passed_unknown_backbone",
    "strat_superseded_skipped",
    "strat_two_signals_rationale",
    "strat_validation_closes_loop",
    "strat_table1_claude_unified_verified",
    "strat_table1_claude_unified_lite",
    "strat_table1_gpt5_hybrid_verified",
    "strat_table1_gpt5_hybrid_lite",
    "strat_table1_gpt5_unified_underperforms",
    "strat_table1_gemini_lite_gain",
    "strat_table1_gemini_verified_loss",
    "strat_summarization_uneven",
    "strat_cw_avoids_summarization_pitfall",
    "ind_cw_law_12",
    "ind_cw_law_123",
    "strat_per_instance_token_parity",
    "strat_tokens_per_resolve_savings",
    "strat_iteration_distribution",
    "strat_lower_variance",
    "strat_case_takeaway",
    "strat_qualitative_recency_bias",
    "strat_dag_chosen_for_stability",
    "strat_window_insensitive",
    "strat_gpt4o_generalization",
    "strat_ablation_summary",
    "strat_headline_empirical",
    "strat_dependency_modeling_thesis",
    "strat_conclusion",
    "strat_central_argument",
    "strat_llm_dependency_limit",
    "strat_test_driven_scope",
    "strat_diverse_signals_future",
    "strat_future_work_summary",
    "strat_shared_challenges",
    "strat_practical_extensions",
    "strat_walkthrough_supports_algorithm",
    "strat_dep_summary_discipline",
    # Abductions
    "abd_dep_vs_more_compute",
    "abd_unified_vs_hybrid",
    # Contradictions
    "contra_recency_sufficient_vs_cw",
    # Predictions used in abductions
    "pred_dep_mech",
    "pred_more_compute",
    "pred_graph_quality_mediator",
    "pred_execution_capability",
]
