"""Priors for independent (leaf) claims in the 2604.23069 ContextWeaver
formalization.

Calibration philosophy
----------------------

* **Direct table/figure transcriptions** (Table 1, Table 2, Table 3a, Table
  3b, Table 4a, Fig. 2/3/4) -- 0.92-0.95. The numbers are reported directly
  by the authors with explicit run counts and standard deviations. The
  modest discount reflects evaluation noise (5-run sample size, LLM-judge
  variance, possible cherry-picking concerns standard in the SWE-Bench
  literature).
* **Algorithmic specifications** (Algorithm 1 line-by-line, Sec 3.1
  components, validation-layer label scheme, observation-compression
  format, prepended test summary) -- 0.94-0.96. These are definitions of
  the system the authors built and ship; they are essentially observable
  facts about the implementation rather than empirical claims.
* **Per-system characterizations of competing systems** (gist tokens,
  selective context, MemGPT, Generative Agents, Reflexion, A-Mem, ToT/GoT,
  CoT, OpenHands+Agentless, ACON, Lindenbauer-2025) -- 0.92-0.94.
  Definitional read-offs of each system's published architecture.
* **Setup/protocol claims** (variance protocol, Unified/Hybrid regime
  definitions) -- 0.94-0.96. Methodological choices stated by the authors.
* **Foil for contradiction** (claim_separate_layers_assumption) -- 0.5.
  The contradiction operator does the BP work, not the prior.
* **Hypothesis / alternative predictions** (pred_dep_mech,
  pred_more_compute, pred_graph_quality_mediator,
  pred_execution_capability):
    * pred_dep_mech (H1): 0.85. The dependency mechanism's prediction of
      simultaneous quality gain + token-saving is theoretically grounded
      and the architecture supports it.
    * pred_more_compute (Alt1): 0.3. Per the rule of thumb pi(Alt) =
      explanatory power, *not* whether 'more compute lifts pass@1' is
      true in general. Here the question is: can 'more compute' explain
      the *observed pattern* of pass@1 UP + tokens DOWN? Answer: weakly --
      the alternative natively predicts tokens FLAT/UP, not DOWN. Hence
      low.
    * pred_graph_quality_mediator (H2): 0.85. The hypothesis is grounded
      in the Unified-vs-Hybrid contrast and the Logical Dependency
      Analyzer prompt design.
    * pred_execution_capability (Alt2): 0.3. Cannot natively explain the
      Hybrid flip on GPT-5; weak explanatory power.
"""

from .motivation import (
    claim_cw_three_components,
    claim_existing_methods_taxonomy,
    claim_separate_layers_assumption,
)
from .s2_related_work import (
    claim_acon_optimization,
    claim_amem_focus,
    claim_cot_baseline,
    claim_generative_agents_components,
    claim_gist_tokens,
    claim_lindenbauer_observation_masking,
    claim_memgpt_components,
    claim_openhands_agentless_static,
    claim_openhands_condenser,
    claim_reflexion_components,
    claim_selective_context,
    claim_static_does_not_model_dynamics,
    claim_swe_agent_condensation,
    claim_token_embedding_compression,
    claim_tot_got_episode_focus,
)
from .s3_setup import (
    claim_warmup_branch,
    claim_weaved_context_definition,
)
from .s4_dependency_construction import (
    claim_ancestry_bfs,
    claim_context_weaving_rule,
    claim_logical_analyzer_prompt_design,
    claim_logical_dependency_analyzer,
    claim_node_summary_content,
    claim_observation_compression_format,
    claim_prepended_test_summary,
    claim_walkthrough_pytest_5262,
)
from .s6_validation_layer import (
    claim_testtracker_extraction,
    claim_testtracker_supersedes_pointer,
)
from .s7_evaluation import (
    claim_unified_vs_hybrid_regimes,
    claim_variance_protocol,
)
from .s8_main_results import (
    claim_case_django_14631,
    claim_case_pytest_7205,
    claim_iteration_budget_scaling,
    claim_iteration_distribution_tail,
    claim_qualitative_38_vs_27,
    claim_qualitative_recency_bias,
    claim_table1_full,
    claim_table2_subset_variance,
)
from .s9_ablations import (
    claim_table3a_dag_vs_tree,
    claim_table3b_window_size,
    claim_table4a_gpt4o_sanity_check,
)
from .s11_wiring import (
    pred_dep_mech,
    pred_execution_capability,
    pred_graph_quality_mediator,
    pred_more_compute,
)

PRIORS: dict = {
    # --- Architecture / specification claims (high) ---
    claim_cw_three_components: (
        0.94,
        "Architectural specification of the three-component framework. "
        "Definitional / verifiable from the paper and the implementation.",
    ),
    claim_warmup_branch: (
        0.96,
        "Algorithm 1 lines 8-10 explicitly specify the warmup branch.",
    ),
    claim_weaved_context_definition: (
        0.95,
        "Output specification of Algorithm 1 + Appendix D.",
    ),
    claim_node_summary_content: (
        0.95,
        "Definitional read-off from Sec. 3.1 (Node Extraction).",
    ),
    claim_logical_dependency_analyzer: (
        0.94,
        "Specification + Appendix A.2 prompt fully documents the analyzer.",
    ),
    claim_logical_analyzer_prompt_design: (
        0.95,
        "Direct transcription of Appendix A.2 system prompt.",
    ),
    claim_ancestry_bfs: (
        0.95,
        "Algorithm 1 lines 11-16 specify the BFS bounded by W.",
    ),
    claim_context_weaving_rule: (
        0.95,
        "Sec. 3.1 Context-Weaving + Appendix D directly state the rule.",
    ),
    claim_observation_compression_format: (
        0.96,
        "Appendix D documents the placeholder format verbatim.",
    ),
    claim_prepended_test_summary: (
        0.94,
        "Appendix A documents the prepend mechanism with example.",
    ),
    claim_testtracker_extraction: (
        0.94,
        "Sec. 3.3 specifies the TestTracker module behavior.",
    ),
    claim_testtracker_supersedes_pointer: (
        0.92,
        "Sec. 3.3 describes the superseded pointer mechanism.",
    ),
    claim_walkthrough_pytest_5262: (
        0.94,
        "Step-level walkthrough is reproducible from the trace in "
        "Appendix E.2.",
    ),

    # --- Setup / protocol claims ---
    claim_unified_vs_hybrid_regimes: (
        0.95,
        "Methodological choice stated explicitly in Sec. 4.2.",
    ),
    claim_variance_protocol: (
        0.96,
        "Sec. 4.6 + Appendix E describe the 5-run x 100-instance protocol.",
    ),

    # --- Existing-methods taxonomy + per-system characterizations ---
    claim_existing_methods_taxonomy: (
        0.94,
        "Three-family taxonomy is well-established in the agent-memory "
        "literature.",
    ),
    claim_gist_tokens: (
        0.93,
        "Direct characterization of [@Mu2023Gist].",
    ),
    claim_selective_context: (
        0.93,
        "Direct characterization of [@Li2023Selective].",
    ),
    claim_token_embedding_compression: (
        0.93,
        "LLMLingua + AutoCompress are well-known token/embedding-level "
        "compressors.",
    ),
    claim_memgpt_components: (
        0.93,
        "MemGPT's OS-style hierarchical paging is the canonical "
        "characterization.",
    ),
    claim_generative_agents_components: (
        0.93,
        "Generative Agents' database + reflection design is widely cited.",
    ),
    claim_reflexion_components: (
        0.93,
        "Reflexion's verbal-RL reflection memory is the canonical "
        "description.",
    ),
    claim_amem_focus: (
        0.92,
        "A-Mem's construction/retrieval focus follows from its published "
        "abstract.",
    ),
    claim_cot_baseline: (
        0.95,
        "CoT [@Wei2022CoT] is the universally accepted starting point for "
        "reasoning-graph methods.",
    ),
    claim_tot_got_episode_focus: (
        0.93,
        "ToT/GoT's single-episode design is explicit in their published "
        "papers.",
    ),
    claim_openhands_agentless_static: (
        0.92,
        "OpenHands + Agentless static-retrieval architecture is documented.",
    ),
    claim_static_does_not_model_dynamics: (
        0.92,
        "Definitional fact: AST analysis cannot describe runtime behavior.",
    ),
    claim_swe_agent_condensation: (
        0.92,
        "SWE-Agent's condensation feature is documented in its paper.",
    ),
    claim_openhands_condenser: (
        0.92,
        "OpenHands modular condenser is in the platform documentation.",
    ),
    claim_acon_optimization: (
        0.92,
        "ACON's compression-guideline-optimization design is in its "
        "abstract.",
    ),
    claim_lindenbauer_observation_masking: (
        0.91,
        "Lindenbauer 2025 result is recent (Aug 2025) and reports a "
        "specific empirical claim with reproducible experiments.",
    ),

    # --- Empirical readouts (tables and figures) ---
    claim_table1_full: (
        0.93,
        "Direct transcription of Table 1; modest discount for evaluation "
        "noise (5-run sampling, prompt-format sensitivity).",
    ),
    claim_table2_subset_variance: (
        0.93,
        "Table 2 reports mean+/-std over 5 runs on a documented 100-"
        "instance subset.",
    ),
    claim_table3a_dag_vs_tree: (
        0.93,
        "Table 3a same protocol as Table 2.",
    ),
    claim_table3b_window_size: (
        0.93,
        "Table 3b same protocol as Table 2.",
    ),
    claim_table4a_gpt4o_sanity_check: (
        0.9,
        "Sec. F.1: explicitly framed as exploratory sanity check, smaller "
        "scale; modest extra discount for limited replication.",
    ),
    claim_iteration_budget_scaling: (
        0.92,
        "Fig. 2a shows curves across iteration budgets; readouts are "
        "qualitative (visible lift) but consistent with Table 1.",
    ),
    claim_iteration_distribution_tail: (
        0.92,
        "Fig. 4 percentile analysis is reproducible from raw iteration "
        "logs.",
    ),

    # --- Case-study and qualitative findings ---
    claim_case_django_14631: (
        0.9,
        "Paired 5-run case study with explicit win counts; small sample "
        "but documented.",
    ),
    claim_case_pytest_7205: (
        0.9,
        "Same paired-5-run protocol as django-14631.",
    ),
    claim_qualitative_38_vs_27: (
        0.92,
        "Full 500-instance Verified count with explicit unique-success "
        "decomposition.",
    ),
    claim_qualitative_recency_bias: (
        0.88,
        "Qualitative inspection of failure modes; concrete sphinx-7440 "
        "example, but interpretation discount.",
    ),

    # --- Foil for contradiction ---
    claim_separate_layers_assumption: (
        0.5,
        "Foil: the contradiction operator does the BP work, not the prior.",
    ),

    # --- Predictions (used in abductions) ---
    pred_dep_mech: (
        0.85,
        "H1 prediction: dependency mechanism predicts simultaneous quality "
        "gain + token saving. Theoretically grounded in the architecture.",
    ),
    pred_more_compute: (
        0.3,
        "Alt1 explanatory power: 'more compute lifts pass@1' cannot "
        "natively predict tokens-per-resolve DOWN with backbone fixed; it "
        "predicts tokens FLAT or UP. Low explanatory power for the "
        "observed pattern.",
    ),
    pred_graph_quality_mediator: (
        0.85,
        "H2 prediction: graph-construction quality mediates the effect, "
        "predicting the Hybrid flip. Grounded in the Logical Dependency "
        "Analyzer prompt design.",
    ),
    pred_execution_capability: (
        0.3,
        "Alt2 explanatory power: cannot natively explain the Unified-vs-"
        "Hybrid GPT-5 flip (under this hypothesis Hybrid and Unified "
        "should track each other). Low explanatory power.",
    ),
}
