"""Sections 5.4-5.6 + Section 7 (Conclusion).

Sections 5.4 (Implications for Agent Design), 5.5 (Implications for
Agent Evaluation), 5.6 (Ecosystem Maturity and Standardization), and
Section 7 (Conclusion + future work) of Rombaut 2026 [@Rombaut2026].

These claims function as the synthesizing implications and the future-
work directions that follow from the spectral / convergence-divergence
findings, plus the synthesizing reasoning operators (contradictions
between baseline assumptions and empirical findings; abductions for
the spectral and loop-primitive findings) tying everything together.
"""

from gaia.lang import abduction, claim, compare, contradiction, induction, support

from .motivation import (
    claim_baseline_capability_taxonomy_sufficient,
    claim_baseline_react_is_dominant_architecture,
    claim_contribution_evidence_base,
    claim_contribution_loop_primitive_thesis,
    claim_contribution_taxonomy,
    claim_existing_surveys_inadequate,
    claim_finding_convergence_divergence,
    claim_finding_loop_primitives_compose,
    claim_finding_methodological_contribution,
    claim_finding_spectra_not_categories,
    claim_no_comparative_source_code_study,
    claim_trajectory_studies_blackbox,
    setup_pinned_commit_methodology,
)
from .s2_related_work import (
    claim_capability_taxonomies_existed,
    claim_capability_taxonomies_indistinguishable,
    claim_individual_system_unmapped_space,
    claim_react_reflexion_paradigms,
    claim_souza_machado_call,
    claim_swebench_central,
    claim_taxonomy_enables_controlled_experiments,
    claim_trajectory_model_confound,
    claim_trajectory_studies_blackbox_limit,
)
from .s3_methodology import (
    claim_corpus_distinct_strategies,
    claim_dimension_open_coding_pilot,
    claim_dual_tool_counting,
    claim_llm_assisted_navigation,
    claim_nine_analysis_dimensions,
    claim_nine_to_twelve_dimensions,
    claim_observation_classification_evidence,
    claim_pinned_commits_for_reproducibility,
    claim_table15_pinned_commits,
    claim_table1_thirteen_agents,
    claim_three_layer_organization,
    claim_verification_pass,
)
from .s4_control_architecture import (
    claim_eleven_of_thirteen_compose,
    claim_loop_driver_distribution,
    claim_loop_driver_most_fundamental,
    claim_loop_primitives_thesis,
    claim_loop_types_compose,
    claim_react_band,
    claim_table2_control_loops,
    claim_table3_loop_driver,
    claim_table4_control_flow,
    claim_tree_search_gradient,
)
from .s5_tool_environment import (
    claim_aider_pagerank_repomap,
    claim_capability_categories_converge,
    claim_docker_converges_for_swebench,
    claim_safety_diverges_for_cli,
    claim_str_replace_convergence,
    claim_table5_tool_sets,
    claim_table6_edit_format,
    claim_table8_retrieval,
    claim_table9_isolation,
)
from .s6_resource_management import (
    claim_compaction_required_observation,
    claim_compaction_seven_strategies,
    claim_dars_swe_fork_vs_mini_protocol,
    claim_ide_as_architecture,
    claim_routing_dominant_driver,
    claim_sampling_vs_iteration,
    claim_state_management_extremes,
    claim_subagent_delegation,
    claim_table10_state_management,
    claim_table11_compaction,
    claim_table12_routing,
    claim_table13_memory,
)
from .s7_convergence_divergence import (
    claim_combinatorial_design_space,
    claim_convergence_divergence_implications,
    claim_convergence_externally_constrained,
    claim_decompose_for_evaluation,
    claim_dimensions_not_independent,
    claim_divergence_open_questions,
    claim_loop_driver_determines_localization_burden,
    claim_pilot_dimension_coverage_threat,
    claim_scaffold_mediates_model,
    claim_single_author_construct_threat,
    claim_spectral_finding_consolidated,
    claim_taxonomy_is_snapshot,
)

# ---------------------------------------------------------------------------
# Section 5.4 -- implications for agent design (4 design lessons)
# ---------------------------------------------------------------------------

claim_design_loop_composition = claim(
    "**Section 5.4 -- design lesson 1: loop composition.** "
    "**11 of 13 agents layer multiple loop primitives**, with "
    "pure single-loop agents being deliberately minimalist "
    "exceptions (Agentless = pipeline only; mini-swe-agent = "
    "ReAct only). This pattern suggests that **the ReAct loop, "
    "while foundational, is typically insufficient on its own**; "
    "layering a retry, test-repair, or planning primitive on top "
    "addresses failure modes a single feedback loop cannot handle "
    "[@Shinn2023Reflexion]. Loop composition is a viable design "
    "strategy.",
    title="5.4 design lesson 1: layer multiple loop primitives -- single ReAct is usually insufficient",
)

claim_design_capability_confusion_tradeoff = claim(
    "**Section 5.4 -- design lesson 2: capability-confusion "
    "tradeoff.** Tool counts range from 0 to 37, yet underlying "
    "capability categories converge on **four (read, search, "
    "edit, execute)**. This convergence at the capability level "
    "despite divergence at the tool level suggests the four "
    "categories define a **minimum viable toolset** for "
    "autonomous coding agents. Beyond this baseline, the tradeoff "
    "is between **expressiveness and LLM confusion**: more "
    "specialized tools reduce the LLM's per-tool reasoning burden "
    "but increase the action space [@SWEAgent]. Prometheus's "
    "per-node tool scoping and AutoCodeRover's phase separation "
    "offer two strategies for managing this tradeoff -- "
    "constraining tools visible at each decision point rather "
    "than presenting the full set at every step.",
    title="5.4 design lesson 2: 4 capability categories = minimum; per-step tool scoping manages confusion",
)

claim_design_compaction_required = claim(
    "**Section 5.4 -- design lesson 3: compaction is "
    "non-optional.** Every agent that gives the LLM sustained "
    "autonomy must address context growth. Section 4.3.2 "
    "documents two philosophies: **prevention** (bounding "
    "structurally) and **cure** (compressing on demand). "
    "Prevention avoids information loss but requires anticipating "
    "growth patterns; cure is more flexible but risks lossy "
    "compression. **The only agent with no compaction strategy "
    "(mini-swe-agent) crashes when the context window is "
    "exceeded**, confirming that compaction is not optional for "
    "agents operating beyond trivial task lengths.",
    title="5.4 design lesson 3: compaction is non-optional (mini-swe-agent crashes prove it)",
)

claim_design_subagent_delegation_frontier = claim(
    "**Section 5.4 -- design lesson 4: sub-agent delegation is an "
    "active frontier.** Five of the 13 agents support explicit "
    "sub-agent spawning through five distinct mechanisms; a "
    "sixth (Prometheus) achieves implicit delegation through "
    "subgraph nesting. **The diversity and absence of a dominant "
    "pattern suggests delegation is an active design frontier.** "
    "Variation in *who controls the delegation decision* mirrors "
    "the loop driver spectrum, suggesting the autonomy-versus-"
    "control tradeoff recurs at every level of agent "
    "architecture.",
    title="5.4 design lesson 4: sub-agent delegation is an active frontier (5 mechanisms across 5 agents)",
)

# ---------------------------------------------------------------------------
# Section 5.5 -- implications for agent evaluation
# ---------------------------------------------------------------------------

claim_eval_swebench_confounds = claim(
    "**Section 5.5 -- evaluation implication.** SWE-bench "
    "comparisons between agents confound scaffold design, model "
    "choice, and configuration in a single metric. The taxonomy "
    "makes this confounding concrete: agents use different "
    "models and different numbers of models -- **Codex CLI "
    "routes to four distinct models while mini-swe-agent uses "
    "one** (Section 4.3.3). Per-attempt model cycling in "
    "SWE-agent and AutoCodeRover means a single benchmark run "
    "may involve multiple models, further complicating "
    "attribution. **Architecture-aware evaluation need not "
    "require entirely new benchmarks**; the 12 dimensions suggest "
    "concrete controls that can be applied within existing "
    "evaluation frameworks (e.g. fixing the tool set while "
    "varying the control loop).",
    title="5.5 evaluation: 12 dimensions enable controlled scaffold-vs-model experiments",
)

claim_eval_sampling_iteration_legibility = claim(
    "**Section 5.5 -- the sampling-vs-iteration evaluation gap.** "
    "Agentless's independent sampling strategy and SWE-agent's "
    "iterative retry strategy represent fundamentally different "
    "approaches to the same problem, but **benchmark scores "
    "conflate single-attempt quality with multi-attempt "
    "strategy**. An agent producing mediocre individual patches "
    "but sampling 40 of them and selecting the best may "
    "outperform an agent producing strong individual patches "
    "through iterative refinement. Separating these two "
    "capabilities in evaluation would require **reporting both "
    "single-attempt and multi-attempt metrics** -- a distinction "
    "the taxonomy makes legible but current benchmarks do not "
    "enforce.",
    title="5.5 evaluation gap: sampling vs iteration are distinct capabilities benchmarks conflate",
)

# ---------------------------------------------------------------------------
# Section 5.6 -- ecosystem maturity and standardization
# ---------------------------------------------------------------------------

claim_standardization_mcp_partial = claim(
    "**Section 5.6 -- MCP standardization is partial.** The "
    "convergence on tool capability categories without "
    "convergence on tool interfaces suggests a specific "
    "standardization opportunity. All LLM-driven agents need "
    "tools for reading, searching, editing, and executing code, "
    "but each agent defines its own tool schemas, parameter "
    "names, and output formats. A shared tool interface protocol "
    "could reduce integration cost. **The Model Context Protocol "
    "(MCP) [@MCP2024]**, already supported by **5 agents in the "
    "corpus** (OpenHands, Codex CLI, Gemini CLI, Cline, "
    "OpenCode), represents an early attempt -- **but operates at "
    "the transport layer rather than defining semantic contracts "
    "for specific tool categories**.",
    title="5.6 MCP supported by 5/13 agents; standardizes transport, not semantic contracts",
)

claim_standardization_moatless_modular = claim(
    "**Section 5.6 -- Moatless Tools' dual-flow as a "
    "modularity model.** Moatless Tools' dual-flow architecture "
    "(Section 4.1.1) offers a more focused model of what modular "
    "scaffold design could look like. Its **clean separation "
    "between the per-step executor (`ActionAgent`) and the "
    "orchestration strategy (`AgenticLoop` or `SearchTree`)** "
    "means that adding a new exploration strategy requires "
    "implementing a new orchestrator, not modifying the agent "
    "logic. This separation is **rare in the corpus**; most "
    "agents tightly couple per-step logic with orchestration "
    "strategy. As the ecosystem matures, this kind of modular "
    "separation may prove more valuable than tool protocol "
    "standardization, because it addresses the architectural "
    "level where the most design variation exists.",
    title="5.6 Moatless dual-flow modularity may matter more than tool-protocol standardization",
)

claim_standardization_ide_tradeoff = claim(
    "**Section 5.6 -- IDE coupling is a platform tradeoff.** "
    "Cline's IDE integration illustrates a different facet of "
    "ecosystem evolution: **the tradeoff between platform "
    "coupling and capability richness**. The IDE-native context "
    "Cline accesses (diagnostics, file-change tracking, terminal "
    "integration) is unavailable to CLI agents, but comes at the "
    "cost of VS Code platform lock-in. For the ecosystem as a "
    "whole, this tension may resolve through protocol-level "
    "abstraction (providing IDE-quality context via standardized "
    "APIs), but **no such abstraction exists today**.",
    title="5.6 IDE coupling tradeoff: richness vs portability; no standard abstraction exists",
)

# ---------------------------------------------------------------------------
# Section 7 conclusion + future work
# ---------------------------------------------------------------------------

claim_conclusion_three_findings = claim(
    "**Section 7 conclusion -- three core findings.** Three "
    "findings emerge from the analysis:\n\n"
    "1. **Spectral, not categorical.** Scaffold architectures "
    "are better characterized as positions along continuous "
    "spectra than as instances of discrete types. Prior "
    "capability-based taxonomies cannot distinguish systems "
    "differing fundamentally on these dimensions.\n"
    "2. **Composable loop primitives.** ReAct, "
    "generate-test-repair, plan-execute, multi-attempt retry, "
    "tree search function as composable building blocks; "
    "**11 of 13 agents layer multiple primitives**. The design "
    "space is combinatorial rather than categorical.\n"
    "3. **Convergence/divergence pattern.** Dimensions converge "
    "on **externally constrained choices** (tool capability "
    "categories, edit formats, execution isolation) and diverge "
    "on **open design questions** (context compaction, state "
    "management, multi-model routing).",
    title="7 conclusion: spectral + composable primitives + convergence/divergence",
)

claim_future_controlled_experiments = claim(
    "**Section 7 future work -- controlled experiments.** The "
    "most direct extension is **controlled experimentation**: the "
    "12 dimensions identify specific architectural variables "
    "that can be isolated while holding others constant. "
    "Examples: comparing agents with identical tool sets but "
    "different loop strategies; identical loops but different "
    "compaction strategies; with the model held constant. This "
    "would enable causal attribution of performance differences "
    "to scaffold design rather than to model or configuration "
    "confounds that current benchmark comparisons cannot "
    "disentangle.",
    title="7 future work 1: controlled experiments isolating one dimension at a time",
)

claim_future_longitudinal = claim(
    "**Section 7 future work -- longitudinal analysis.** Repeating "
    "the analysis at later commits would reveal how scaffold "
    "architectures evolve: whether converging dimensions continue "
    "to converge, whether diverging dimensions stabilize, and "
    "whether new dimensions emerge as the ecosystem matures. "
    "**The commit-pinned methodology makes such longitudinal "
    "comparison straightforward.**",
    title="7 future work 2: longitudinal re-analysis at later commits",
)

claim_future_extend_corpus = claim(
    "**Section 7 future work -- corpus extension.** Extending the "
    "corpus to **proprietary agents** (when architectural details "
    "become available through documentation or reverse "
    "engineering) and to **agents targeting languages beyond "
    "Python** would test the generalizability of the observed "
    "spectra. The dimension framework is designed to be language- "
    "and platform-agnostic, but whether the specific positions "
    "observed here generalize to different ecosystems remains an "
    "open question.",
    title="7 future work 3: extend corpus to proprietary + non-Python agents",
)

claim_future_architecture_aware_eval = claim(
    "**Section 7 future work -- architecture-aware evaluation "
    "metrics.** The taxonomy enables the **architecture-aware "
    "evaluation metrics** that prior work has called for "
    "[@Souza2026] but could not implement without architectural "
    "documentation. Linking specific dimension positions (loop "
    "strategy, compaction approach, tool set design) to "
    "observable outcomes (task success, token cost, trajectory "
    "length) would move the field **from system-level "
    "leaderboards toward component-level understanding** of what "
    "makes coding agents effective.",
    title="7 future work 4: architecture-aware evaluation metrics linking dimensions to outcomes",
)

# ===========================================================================
# REASONING STRATEGIES (Pass 2 -- Pass 4: refined types)
# ===========================================================================

# ---------------------------------------------------------------------------
# Block A: Methodology -> the 13-agent corpus & 12-dimension framework
# ---------------------------------------------------------------------------

# A.1 -- The 9 analysis dimensions follow from open coding of the 2 pilot
# agents (deliberate diversity).
strat_nine_dimensions_from_pilot = support(
    [
        claim_dimension_open_coding_pilot,
        claim_observation_classification_evidence,
    ],
    claim_nine_analysis_dimensions,
    reason=(
        "The nine analysis dimensions (@claim_nine_analysis_dimensions) "
        "are the empirical output of the open-coding pilot on Aider + "
        "OpenHands (@claim_dimension_open_coding_pilot), with the "
        "three-level observation/classification/evidence template "
        "(@claim_observation_classification_evidence) ensuring that "
        "each emergent dimension was traceable to concrete source-code "
        "patterns rather than to a priori conceptual categories."
    ),
    prior=0.92,
)

# A.2 -- The 12 taxonomy dimensions follow from the 9 analysis dimensions
# plus the discovery that 3 sub-properties were independently discriminating.
strat_twelve_dims_from_nine = support(
    [
        claim_nine_analysis_dimensions,
        claim_nine_to_twelve_dimensions,
    ],
    claim_three_layer_organization,
    reason=(
        "The 3-layer / 12-dimension structure "
        "(@claim_three_layer_organization) is the result of the 9 "
        "analysis dimensions (@claim_nine_analysis_dimensions) being "
        "expanded to 12 taxonomy dimensions when 3 sub-properties (loop "
        "driver, edit format, control flow implementation) proved "
        "independently discriminating (@claim_nine_to_twelve_dimensions)."
    ),
    prior=0.93,
)

# A.3 -- The 13-agent corpus is what survives the 3 inclusion criteria
# applied to the 22 candidates (this is procedural).
strat_thirteen_corpus = support(
    [claim_corpus_distinct_strategies],
    claim_table1_thirteen_agents,
    reason=(
        "The Table 1 list of 13 agents (@claim_table1_thirteen_agents) "
        "is the result of the deliberate selection (Section 3.1) for "
        "architectural strategy diversity "
        "(@claim_corpus_distinct_strategies)."
    ),
    prior=0.95,
)

# A.4 -- Pinned commits + LLM-assisted-but-verified navigation underwrite
# the verification pass result.
strat_verification_pass = support(
    [
        claim_pinned_commits_for_reproducibility,
        claim_llm_assisted_navigation,
        claim_observation_classification_evidence,
    ],
    claim_verification_pass,
    reason=(
        "The post-hoc verification pass (@claim_verification_pass) "
        "checked 296 claims against the cloned repos at the pinned "
        "commits (@claim_pinned_commits_for_reproducibility); the "
        "verification was tractable because every claim carried a "
        "file-path + line-number pointer (@claim_observation_classification_evidence) "
        "and the LLM-assisted navigation workflow "
        "(@claim_llm_assisted_navigation) was designed to leave such "
        "traces."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# Block B: Per-dimension claims -> the spectral & convergence/divergence
# headlines (each table is one piece of per-dimension evidence)
# ---------------------------------------------------------------------------

# B.1 -- The spectral finding is supported by every per-dimension table
# showing a continuous spectrum.
strat_spectral_finding = support(
    [
        claim_table2_control_loops,
        claim_table5_tool_sets,
        claim_table10_state_management,
        claim_table11_compaction,
        claim_capability_taxonomies_indistinguishable,
    ],
    claim_spectral_finding_consolidated,
    reason=(
        "The 5.1 spectral finding "
        "(@claim_spectral_finding_consolidated) is supported by the "
        "per-dimension evidence tables: 6-position control loop "
        "spectrum (@claim_table2_control_loops), 0-37 tool count range "
        "(@claim_table5_tool_sets), 8-variant state management "
        "(@claim_table10_state_management), 7-strategy compaction "
        "(@claim_table11_compaction). The fact that every agent "
        "qualifies for every capability label "
        "(@claim_capability_taxonomies_indistinguishable) anchors the "
        "claim that capability-based taxonomies cannot capture this "
        "variation."
    ),
    prior=0.93,
)

# B.2 -- The convergence/divergence headline is supported by the converging
# tables (capability categories, edit format, isolation) and the diverging
# tables (compaction, state, routing).
strat_convergence_externally_constrained = support(
    [
        claim_capability_categories_converge,
        claim_str_replace_convergence,
        claim_docker_converges_for_swebench,
    ],
    claim_convergence_externally_constrained,
    reason=(
        "The convergence claim "
        "(@claim_convergence_externally_constrained) is supported by "
        "(a) capability categories converging on read/search/edit/"
        "execute (@claim_capability_categories_converge), (b) the "
        "str_replace_editor independent-discovery convergence in 5/13 "
        "agents (@claim_str_replace_convergence), and (c) Docker "
        "convergence among the 5 SWE-bench agents "
        "(@claim_docker_converges_for_swebench). All three reflect "
        "constraints external to the scaffold designer (task "
        "requirements, LLM patch reliability, unattended-execution "
        "safety)."
    ),
    prior=0.92,
)

strat_divergence_open_questions = support(
    [
        claim_compaction_seven_strategies,
        claim_state_management_extremes,
        claim_routing_dominant_driver,
    ],
    claim_divergence_open_questions,
    reason=(
        "The divergence claim (@claim_divergence_open_questions) is "
        "supported by (a) the seven distinct compaction strategies "
        "(@claim_compaction_seven_strategies), (b) the destructive-to-"
        "event-sourced range of state-management variants "
        "(@claim_state_management_extremes), and (c) the wide range of "
        "multi-model routing mechanisms across 9 of 13 agents "
        "(@claim_routing_dominant_driver). All three address tradeoffs "
        "with no dominant solution."
    ),
    prior=0.92,
)

# B.3 -- The convergence/divergence implication (standardize converged,
# research diverged) follows from the two halves above.
strat_convergence_divergence_combined = support(
    [
        claim_convergence_externally_constrained,
        claim_divergence_open_questions,
    ],
    claim_finding_convergence_divergence,
    reason=(
        "The motivation-section preview "
        "(@claim_finding_convergence_divergence) of the convergence/"
        "divergence pattern is the union of the convergence claim "
        "(@claim_convergence_externally_constrained) and the divergence "
        "claim (@claim_divergence_open_questions)."
    ),
    prior=0.95,
)

strat_convergence_divergence_implications = support(
    [
        claim_convergence_externally_constrained,
        claim_divergence_open_questions,
    ],
    claim_convergence_divergence_implications,
    reason=(
        "The standardize-where-converged/research-where-diverged "
        "implication (@claim_convergence_divergence_implications) is a "
        "direct consequence of (a) the converging dimensions reflecting "
        "external constraints (@claim_convergence_externally_constrained) "
        "and (b) the diverging dimensions reflecting open questions "
        "(@claim_divergence_open_questions): solved problems are ready "
        "for standardization; open problems need research investment."
    ),
    prior=0.88,
)

# ---------------------------------------------------------------------------
# Block C: The loop-primitive thesis (Pass 2 induction over per-agent
# observations) -- 11 of 13 compose multiple primitives
# ---------------------------------------------------------------------------

# C.1 -- Per-agent observations of multi-primitive composition. We make
# these into intermediate claims (one per agent) so the induction is
# explicit at the right level of granularity.

claim_obs_aider_composes = claim(
    "**Per-agent observation: Aider composes multiple loop primitives.** "
    "Aider runs a *user-driven* outer loop with the LLM producing "
    "text-format edits; nested inside is an *autonomous "
    "generate-test-repair* loop where the scaffold runs lint/tests "
    "and re-prompts the LLM with errors for up to "
    "`max_reflections` iterations (`base_coder.py:932`). At least "
    "two primitives composed: user-driven turn + generate-test-repair.",
    title="Per-agent: Aider composes user-turn + generate-test-repair",
)

claim_obs_swe_agent_composes = claim(
    "**Per-agent observation: SWE-agent composes multiple loop "
    "primitives.** SWE-agent's primary loop is a sequential "
    "ReAct cycle, but its `RetryAgent` wraps multiple complete "
    "ReAct trajectories with a reviewer model that selects the "
    "best (Section 4.4.1). At least two primitives composed: "
    "ReAct + multi-attempt retry.",
    title="Per-agent: SWE-agent composes ReAct + multi-attempt retry",
)

claim_obs_openhands_composes = claim(
    "**Per-agent observation: OpenHands composes multiple loop "
    "primitives.** OpenHands runs a sequential ReAct loop and "
    "additionally implements generate-test-repair (linting/test "
    "loops); its sub-agent delegation (`AgentDelegateAction`) is "
    "structurally a plan-execute primitive embedded in the event "
    "stream. At least three primitives composed.",
    title="Per-agent: OpenHands composes ReAct + generate-test-repair + plan-execute (delegation)",
)

claim_obs_codex_composes = claim(
    "**Per-agent observation: Codex CLI composes multiple loop "
    "primitives.** Codex CLI runs a sequential ReAct loop and "
    "exposes sub-agent spawning as a first-class tool suite "
    "(`spawn_agent`, `send_input`, `resume_agent`, `wait`, "
    "`close_agent`), i.e. an LLM-controlled plan-execute "
    "primitive layered on top. At least two primitives composed.",
    title="Per-agent: Codex CLI composes ReAct + plan-execute (sub-agent spawning)",
)

claim_obs_gemini_composes = claim(
    "**Per-agent observation: Gemini CLI composes multiple loop "
    "primitives.** Gemini CLI runs a sequential ReAct loop, "
    "embeds sub-agent execution via `LocalAgentExecutor` "
    "(plan-execute), and uses generate-test-repair for "
    "verification probes after compaction. At least three "
    "primitives composed.",
    title="Per-agent: Gemini CLI composes ReAct + plan-execute + generate-test-repair",
)

claim_obs_cline_composes = claim(
    "**Per-agent observation: Cline composes multiple loop "
    "primitives.** Cline runs a sequential ReAct loop with a "
    "plan-mode/act-mode division (each is a separate plan-execute "
    "phase that the LLM toggles between via tool calls); also "
    "supports new-task delegation. At least two primitives "
    "composed.",
    title="Per-agent: Cline composes ReAct + plan-execute (plan/act modes)",
)

claim_obs_opencode_composes = claim(
    "**Per-agent observation: OpenCode composes multiple loop "
    "primitives.** OpenCode runs a sequential ReAct loop and "
    "spawns role-based sub-agents (build, plan, explore, general) "
    "via the `task` tool -- a plan-execute primitive layered on "
    "top of ReAct. At least two primitives composed.",
    title="Per-agent: OpenCode composes ReAct + plan-execute (role-based sub-agents)",
)

claim_obs_autocoderover_composes = claim(
    "**Per-agent observation: AutoCodeRover composes multiple "
    "loop primitives.** AutoCodeRover runs a *phased* pipeline "
    "(plan-execute) where each stage embeds a multi-turn ReAct "
    "interaction (`agent_search.py:88--163`). It also uses "
    "per-attempt model cycling for retry. At least three "
    "primitives composed.",
    title="Per-agent: AutoCodeRover composes plan-execute + ReAct + multi-attempt retry",
)

claim_obs_prometheus_composes = claim(
    "**Per-agent observation: Prometheus composes multiple loop "
    "primitives.** Prometheus runs a LangGraph state machine "
    "(plan-execute via subgraph nesting), with ReAct embedded "
    "inside each LLM node. Generate-test-repair appears via the "
    "`BugFixVerifyNode`. Decision-layer voting (10x advanced "
    "model calls) is a multi-attempt-retry primitive. At least "
    "four primitives composed.",
    title="Per-agent: Prometheus composes plan-execute + ReAct + generate-test-repair + retry/voting",
)

claim_obs_dars_composes = claim(
    "**Per-agent observation: DARS-Agent composes multiple loop "
    "primitives.** DARS-Agent's main loop is depth-first tree "
    "search with greedy LLM-critic selection at each branch "
    "point; ReAct steps form the nodes; an offline reviewer "
    "(multi-attempt selection) chooses the final patch. At least "
    "three primitives composed.",
    title="Per-agent: DARS-Agent composes tree-search + ReAct + multi-attempt retry (offline reviewer)",
)

claim_obs_moatless_composes = claim(
    "**Per-agent observation: Moatless Tools composes multiple "
    "loop primitives.** Moatless Tools' `ActionAgent` is a "
    "single-step ReAct executor that can be driven by "
    "`AgenticLoop` (sequential ReAct) or by `SearchTree` (full "
    "MCTS); the MCTS itself nests ReAct inside each "
    "Select-Expand-Simulate-Backpropagate step. The discriminator "
    "implements offline multi-attempt selection. At least three "
    "primitives composed.",
    title="Per-agent: Moatless Tools composes ReAct + tree-search (MCTS) + multi-attempt retry (discriminator)",
)

# C.2 -- For each per-agent observation, justify it from the corresponding
# per-table claim.
strat_obs_aider = support(
    [claim_table2_control_loops, claim_react_band, claim_loop_types_compose],
    claim_obs_aider_composes,
    reason=(
        "Aider's user-driven + generate-test-repair composition is "
        "documented in the Table 2 row for Aider "
        "(@claim_table2_control_loops), the discussion of Aider's "
        "inner generate-test-repair loop (@claim_react_band), and the "
        "general observation that loops nest in this corpus "
        "(@claim_loop_types_compose)."
    ),
    prior=0.95,
)

strat_obs_swe_agent = support(
    [claim_table2_control_loops, claim_sampling_vs_iteration],
    claim_obs_swe_agent_composes,
    reason=(
        "SWE-agent's ReAct + RetryAgent composition is documented in "
        "Table 2 (@claim_table2_control_loops) and in the "
        "sampling-vs-iteration discussion of RetryAgent as a "
        "multi-attempt-retry primitive (@claim_sampling_vs_iteration)."
    ),
    prior=0.95,
)

strat_obs_openhands = support(
    [claim_table2_control_loops, claim_subagent_delegation],
    claim_obs_openhands_composes,
    reason=(
        "OpenHands' ReAct + generate-test-repair composition is "
        "documented in Table 2 (@claim_table2_control_loops); its "
        "delegation as a plan-execute primitive is documented in the "
        "sub-agent delegation theme (@claim_subagent_delegation)."
    ),
    prior=0.93,
)

strat_obs_codex = support(
    [claim_table2_control_loops, claim_subagent_delegation],
    claim_obs_codex_composes,
    reason=(
        "Codex CLI's ReAct loop is documented in Table 2 "
        "(@claim_table2_control_loops); its LLM-driven sub-agent "
        "spawning suite is documented in the sub-agent delegation "
        "theme (@claim_subagent_delegation)."
    ),
    prior=0.93,
)

strat_obs_gemini = support(
    [claim_table2_control_loops, claim_subagent_delegation],
    claim_obs_gemini_composes,
    reason=(
        "Gemini CLI's ReAct loop is documented in Table 2 "
        "(@claim_table2_control_loops); its LocalAgentExecutor "
        "sub-agent + verification probe pattern is documented in the "
        "sub-agent delegation theme (@claim_subagent_delegation)."
    ),
    prior=0.92,
)

strat_obs_cline = support(
    [claim_table2_control_loops, claim_subagent_delegation],
    claim_obs_cline_composes,
    reason=(
        "Cline's ReAct loop is documented in Table 2 "
        "(@claim_table2_control_loops); its plan-mode/act-mode division "
        "and new-task delegation are documented in the sub-agent "
        "delegation theme (@claim_subagent_delegation)."
    ),
    prior=0.93,
)

strat_obs_opencode = support(
    [claim_table2_control_loops, claim_subagent_delegation],
    claim_obs_opencode_composes,
    reason=(
        "OpenCode's ReAct loop is documented in Table 2 "
        "(@claim_table2_control_loops); its role-based sub-agent "
        "spawning is documented in the sub-agent delegation theme "
        "(@claim_subagent_delegation)."
    ),
    prior=0.93,
)

strat_obs_autocoderover = support(
    [claim_table2_control_loops, claim_loop_types_compose],
    claim_obs_autocoderover_composes,
    reason=(
        "AutoCodeRover's phased pipeline + nested ReAct interaction "
        "is documented in Table 2 (@claim_table2_control_loops) and "
        "the nesting discussion (@claim_loop_types_compose)."
    ),
    prior=0.95,
)

strat_obs_prometheus = support(
    [
        claim_table2_control_loops,
        claim_subagent_delegation,
        claim_sampling_vs_iteration,
    ],
    claim_obs_prometheus_composes,
    reason=(
        "Prometheus's LangGraph + ReAct nesting is documented in "
        "Table 2 (@claim_table2_control_loops); its subgraph-based "
        "implicit delegation is documented in the sub-agent delegation "
        "theme (@claim_subagent_delegation); its 10x decision-layer "
        "voting is documented in the sampling-vs-iteration discussion "
        "(@claim_sampling_vs_iteration)."
    ),
    prior=0.92,
)

strat_obs_dars = support(
    [claim_table2_control_loops, claim_tree_search_gradient],
    claim_obs_dars_composes,
    reason=(
        "DARS-Agent's tree-search + ReAct nodes + offline reviewer is "
        "documented in Table 2 (@claim_table2_control_loops) and in "
        "the tree-search gradient discussion "
        "(@claim_tree_search_gradient)."
    ),
    prior=0.93,
)

strat_obs_moatless = support(
    [claim_table2_control_loops, claim_loop_types_compose],
    claim_obs_moatless_composes,
    reason=(
        "Moatless Tools' ActionAgent / AgenticLoop / SearchTree "
        "decoupling is documented in Table 2 "
        "(@claim_table2_control_loops) and the loop-composition "
        "discussion (@claim_loop_types_compose)."
    ),
    prior=0.95,
)

# C.3 -- Induction: 11 per-agent observations support the population claim
# that "11 of 13 agents compose multiple primitives". Each support is in
# the generative direction: claim_eleven_of_thirteen_compose -> per-agent
# observation.
ind_compose_aider = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_aider_composes,
    reason=(
        "If 11 of 13 agents compose multiple loop primitives "
        "(@claim_eleven_of_thirteen_compose), Aider being one of the "
        "11 multi-primitive agents predicts the user-turn + "
        "generate-test-repair composition (@claim_obs_aider_composes)."
    ),
    prior=0.92,
)

ind_compose_swe = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_swe_agent_composes,
    reason=(
        "If the population claim holds (@claim_eleven_of_thirteen_compose), "
        "SWE-agent being a multi-primitive agent predicts the ReAct + "
        "multi-attempt-retry composition (@claim_obs_swe_agent_composes)."
    ),
    prior=0.92,
)

ind_compose_openhands = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_openhands_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "OpenHands being a multi-primitive agent predicts the "
        "ReAct + generate-test-repair + plan-execute composition "
        "(@claim_obs_openhands_composes)."
    ),
    prior=0.92,
)

ind_compose_codex = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_codex_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "Codex CLI being a multi-primitive agent predicts the ReAct + "
        "plan-execute composition (@claim_obs_codex_composes)."
    ),
    prior=0.92,
)

ind_compose_gemini = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_gemini_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "Gemini CLI being a multi-primitive agent predicts the ReAct "
        "+ plan-execute + generate-test-repair composition "
        "(@claim_obs_gemini_composes)."
    ),
    prior=0.92,
)

ind_compose_cline = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_cline_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "Cline being a multi-primitive agent predicts the ReAct + "
        "plan-execute composition (@claim_obs_cline_composes)."
    ),
    prior=0.92,
)

ind_compose_opencode = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_opencode_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "OpenCode being a multi-primitive agent predicts the ReAct + "
        "plan-execute composition (@claim_obs_opencode_composes)."
    ),
    prior=0.92,
)

ind_compose_autocoderover = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_autocoderover_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "AutoCodeRover being a multi-primitive agent predicts the "
        "plan-execute + ReAct + multi-attempt-retry composition "
        "(@claim_obs_autocoderover_composes)."
    ),
    prior=0.92,
)

ind_compose_prometheus = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_prometheus_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "Prometheus being a multi-primitive agent predicts the "
        "plan-execute + ReAct + generate-test-repair + retry/voting "
        "composition (@claim_obs_prometheus_composes)."
    ),
    prior=0.92,
)

ind_compose_dars = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_dars_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "DARS-Agent being a multi-primitive agent predicts the "
        "tree-search + ReAct + multi-attempt-retry composition "
        "(@claim_obs_dars_composes)."
    ),
    prior=0.92,
)

ind_compose_moatless = support(
    [claim_eleven_of_thirteen_compose],
    claim_obs_moatless_composes,
    reason=(
        "If 11 of 13 compose (@claim_eleven_of_thirteen_compose), "
        "Moatless Tools being a multi-primitive agent predicts the "
        "ReAct + tree-search (MCTS) + multi-attempt-retry composition "
        "(@claim_obs_moatless_composes)."
    ),
    prior=0.92,
)

# Chain the induction: pair-wise composition over the 11 per-agent
# observations.
ind_compose_a = induction(
    ind_compose_aider, ind_compose_swe, law=claim_eleven_of_thirteen_compose,
    reason="Aider and SWE-agent are independent observations.",
)
ind_compose_b = induction(
    ind_compose_a, ind_compose_openhands, law=claim_eleven_of_thirteen_compose,
    reason="Adding OpenHands -- independent codebase, independent design team.",
)
ind_compose_c = induction(
    ind_compose_b, ind_compose_codex, law=claim_eleven_of_thirteen_compose,
    reason="Adding Codex CLI -- independent of the prior agents.",
)
ind_compose_d = induction(
    ind_compose_c, ind_compose_gemini, law=claim_eleven_of_thirteen_compose,
    reason="Adding Gemini CLI -- independent design team (Google).",
)
ind_compose_e = induction(
    ind_compose_d, ind_compose_cline, law=claim_eleven_of_thirteen_compose,
    reason="Adding Cline -- independent codebase.",
)
ind_compose_f = induction(
    ind_compose_e, ind_compose_opencode, law=claim_eleven_of_thirteen_compose,
    reason="Adding OpenCode -- independent SST codebase.",
)
ind_compose_g = induction(
    ind_compose_f, ind_compose_autocoderover, law=claim_eleven_of_thirteen_compose,
    reason="Adding AutoCodeRover -- independent academic codebase.",
)
ind_compose_h = induction(
    ind_compose_g, ind_compose_prometheus, law=claim_eleven_of_thirteen_compose,
    reason="Adding Prometheus -- independent academic codebase.",
)
ind_compose_i = induction(
    ind_compose_h, ind_compose_dars, law=claim_eleven_of_thirteen_compose,
    reason="Adding DARS-Agent -- independent academic codebase.",
)
ind_compose_full = induction(
    ind_compose_i, ind_compose_moatless, law=claim_eleven_of_thirteen_compose,
    reason=(
        "Adding the 11th independent per-agent observation (Moatless "
        "Tools) closes the induction. The 11 per-agent observations "
        "are largely independent (different codebases, different "
        "teams, different release dates), supporting the population "
        "claim that 11 of the 13 agents compose multiple primitives."
    ),
)

# Bridge the induction conclusion to the headline thesis (motivation
# preview); also support the 5-loop-primitive thesis from per-agent
# observations.
strat_loop_primitives_thesis = support(
    [
        claim_table2_control_loops,
        claim_eleven_of_thirteen_compose,
        claim_loop_types_compose,
    ],
    claim_loop_primitives_thesis,
    reason=(
        "The 5 loop primitive thesis (@claim_loop_primitives_thesis) "
        "is supported by the 6-position control-loop spectrum that "
        "implicitly enumerates ReAct, generate-test-repair (Aider), "
        "plan-execute (phased), multi-attempt retry (sampling), and "
        "tree search (@claim_table2_control_loops); by the empirical "
        "fact that 11 of 13 agents combine multiple "
        "(@claim_eleven_of_thirteen_compose); and by the explicit "
        "nesting / composability documented in "
        "@claim_loop_types_compose."
    ),
    prior=0.92,
)

strat_motivation_preview_loop_primitives = support(
    [claim_loop_primitives_thesis, claim_eleven_of_thirteen_compose],
    claim_finding_loop_primitives_compose,
    reason=(
        "The motivation-section preview "
        "(@claim_finding_loop_primitives_compose) of the loop "
        "primitive thesis is supported by the rigorous Section-4.1.1 "
        "loop-primitive thesis (@claim_loop_primitives_thesis) plus "
        "the 11/13 induction conclusion "
        "(@claim_eleven_of_thirteen_compose)."
    ),
    prior=0.97,
)

strat_combinatorial_design_space = support(
    [claim_loop_primitives_thesis, claim_eleven_of_thirteen_compose],
    claim_combinatorial_design_space,
    reason=(
        "The combinatorial-design-space claim "
        "(@claim_combinatorial_design_space) is the structural "
        "consequence of (a) the 5 loop primitives functioning as "
        "composable building blocks (@claim_loop_primitives_thesis) "
        "and (b) the empirical fact that 11/13 agents combine "
        "multiple (@claim_eleven_of_thirteen_compose). If primitives "
        "compose freely and most agents do compose, the design space "
        "is combinatorial."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# Block D: Wire motivation contributions to the per-section evidence
# ---------------------------------------------------------------------------

strat_contribution_taxonomy = support(
    [
        claim_table1_thirteen_agents,
        claim_three_layer_organization,
        claim_individual_system_unmapped_space,
    ],
    claim_contribution_taxonomy,
    reason=(
        "Contribution 1 (the 13-agent / 3-layer / 12-dimension "
        "taxonomy, @claim_contribution_taxonomy) is established by "
        "the 13-agent corpus (@claim_table1_thirteen_agents), the "
        "3-layer / 12-dimension organization "
        "(@claim_three_layer_organization), and the prior literature "
        "gap that no comparative source-code study existed "
        "(@claim_individual_system_unmapped_space)."
    ),
    prior=0.95,
)

strat_contribution_loop_primitive_thesis = support(
    [
        claim_loop_primitives_thesis,
        claim_eleven_of_thirteen_compose,
        claim_combinatorial_design_space,
    ],
    claim_contribution_loop_primitive_thesis,
    reason=(
        "Contribution 2 (the loop primitive thesis, "
        "@claim_contribution_loop_primitive_thesis) is established by "
        "(a) the 5 loop primitives identified across the corpus "
        "(@claim_loop_primitives_thesis), (b) the 11/13 "
        "compose-multiple induction (@claim_eleven_of_thirteen_compose), "
        "and (c) the combinatorial structural consequence "
        "(@claim_combinatorial_design_space)."
    ),
    prior=0.93,
)

strat_contribution_evidence_base = support(
    [
        claim_table15_pinned_commits,
        claim_observation_classification_evidence,
        claim_verification_pass,
    ],
    claim_contribution_evidence_base,
    reason=(
        "Contribution 3 (the reusable commit-pinned evidence base, "
        "@claim_contribution_evidence_base) is established by the "
        "methodology of pinning to commit hashes "
        "(@setup_pinned_commit_methodology, "
        "@claim_table15_pinned_commits), the three-level "
        "observation/classification/evidence template "
        "(@claim_observation_classification_evidence), and the "
        "post-hoc verification of 296 claims "
        "(@claim_verification_pass)."
    ),
    background=[setup_pinned_commit_methodology],
    prior=0.95,
)

# Methodological-finding preview wiring.
strat_methodological_preview = support(
    [
        claim_observation_classification_evidence,
        claim_table15_pinned_commits,
    ],
    claim_finding_methodological_contribution,
    reason=(
        "The motivation preview of the methodological contribution "
        "(@claim_finding_methodological_contribution) is supported by "
        "the pinned-commit + file/line grounding "
        "(@setup_pinned_commit_methodology, "
        "@claim_observation_classification_evidence, "
        "@claim_table15_pinned_commits)."
    ),
    background=[setup_pinned_commit_methodology],
    prior=0.95,
)

strat_motivation_preview_spectra = support(
    [claim_spectral_finding_consolidated],
    claim_finding_spectra_not_categories,
    reason=(
        "The motivation preview of the spectral finding "
        "(@claim_finding_spectra_not_categories) is supported by the "
        "Section 5.1 consolidated spectral finding "
        "(@claim_spectral_finding_consolidated)."
    ),
    prior=0.97,
)

# ---------------------------------------------------------------------------
# Block E: Section 2 "gap" claims -> motivation gap statements
# ---------------------------------------------------------------------------

strat_existing_surveys_inadequate = support(
    [
        claim_capability_taxonomies_existed,
        claim_capability_taxonomies_indistinguishable,
        claim_react_reflexion_paradigms,
    ],
    claim_existing_surveys_inadequate,
    reason=(
        "The motivation Gap 1 (@claim_existing_surveys_inadequate) "
        "follows from (a) the existence of capability-based surveys "
        "(@claim_capability_taxonomies_existed), (b) the empirical "
        "observation that every agent fits all capability labels "
        "(@claim_capability_taxonomies_indistinguishable), and (c) "
        "the algorithmic-paradigm-vs-architecture gap noted for "
        "ReAct/Reflexion (@claim_react_reflexion_paradigms)."
    ),
    prior=0.94,
)

strat_trajectory_studies_blackbox = support(
    [
        claim_trajectory_studies_blackbox_limit,
        claim_trajectory_model_confound,
    ],
    claim_trajectory_studies_blackbox,
    reason=(
        "The motivation Gap 2 (@claim_trajectory_studies_blackbox) "
        "follows from (a) the black-box limitation of trajectory "
        "studies (@claim_trajectory_studies_blackbox_limit) and (b) "
        "the scaffold/model confound (@claim_trajectory_model_confound)."
    ),
    prior=0.94,
)

strat_no_comparative_study_gap = support(
    [claim_individual_system_unmapped_space],
    claim_no_comparative_source_code_study,
    reason=(
        "The motivation Gap 3 (@claim_no_comparative_source_code_study) "
        "follows directly from the related-work observation that "
        "per-system depth does not aggregate into a comparative "
        "reference (@claim_individual_system_unmapped_space)."
    ),
    prior=0.94,
)

# ---------------------------------------------------------------------------
# Block F: Discussion claims (Sections 5.3-5.6)
# ---------------------------------------------------------------------------

strat_scaffold_mediates_model = support(
    [
        claim_table5_tool_sets,
        claim_table11_compaction,
        claim_table2_control_loops,
        claim_table3_loop_driver,
    ],
    claim_scaffold_mediates_model,
    reason=(
        "The 5.3 scaffold-mediates-model claim "
        "(@claim_scaffold_mediates_model) is supported by the "
        "tool-count range (@claim_table5_tool_sets), the compaction "
        "diversity (@claim_table11_compaction), the control-loop "
        "spectrum (@claim_table2_control_loops), and the loop-driver "
        "spectrum (@claim_table3_loop_driver). Each row in these "
        "tables is a different way the same LLM could be embedded."
    ),
    prior=0.92,
)

strat_loop_driver_localization = support(
    [
        claim_loop_driver_distribution,
        claim_loop_driver_most_fundamental,
        claim_table8_retrieval,
    ],
    claim_loop_driver_determines_localization_burden,
    reason=(
        "The 5.3 loop-driver determines localization burden claim "
        "(@claim_loop_driver_determines_localization_burden) follows "
        "from (a) the loop-driver distribution showing 9 of 13 "
        "LLM-driven (@claim_loop_driver_distribution), (b) the "
        "fundamental-distinction designation "
        "(@claim_loop_driver_most_fundamental), and (c) the 7-strategy "
        "retrieval table (@claim_table8_retrieval) showing the "
        "co-design space."
    ),
    prior=0.9,
)

strat_decompose_for_evaluation = support(
    [
        claim_spectral_finding_consolidated,
        claim_combinatorial_design_space,
        claim_taxonomy_enables_controlled_experiments,
    ],
    claim_decompose_for_evaluation,
    reason=(
        "The 5.1 prescription to decompose along dimensions "
        "(@claim_decompose_for_evaluation) follows from the spectral "
        "finding (@claim_spectral_finding_consolidated), the "
        "combinatorial design space (@claim_combinatorial_design_space), "
        "and the related-work observation that controlled experiments "
        "need taxonomic variables "
        "(@claim_taxonomy_enables_controlled_experiments)."
    ),
    prior=0.9,
)

# F.4 -- Design lessons (5.4) follow from per-section evidence.
strat_design_loop_composition = support(
    [
        claim_eleven_of_thirteen_compose,
        claim_loop_primitives_thesis,
    ],
    claim_design_loop_composition,
    reason=(
        "Design lesson 1 -- loop composition "
        "(@claim_design_loop_composition) -- follows from the 11/13 "
        "compose-multiple finding (@claim_eleven_of_thirteen_compose) "
        "and the 5-loop-primitive identification "
        "(@claim_loop_primitives_thesis)."
    ),
    prior=0.92,
)

strat_design_capability_confusion = support(
    [
        claim_table5_tool_sets,
        claim_capability_categories_converge,
    ],
    claim_design_capability_confusion_tradeoff,
    reason=(
        "Design lesson 2 -- the capability-confusion tradeoff "
        "(@claim_design_capability_confusion_tradeoff) -- follows "
        "from the 0-37 tool-count range (@claim_table5_tool_sets) "
        "combined with the four-capability convergence "
        "(@claim_capability_categories_converge)."
    ),
    prior=0.9,
)

strat_design_compaction_required = support(
    [
        claim_table11_compaction,
        claim_compaction_required_observation,
    ],
    claim_design_compaction_required,
    reason=(
        "Design lesson 3 -- compaction is non-optional "
        "(@claim_design_compaction_required) -- follows from the "
        "7-strategy compaction landscape (@claim_table11_compaction) "
        "and the empirical observation that mini-swe-agent crashes "
        "on overflow (@claim_compaction_required_observation)."
    ),
    prior=0.95,
)

strat_design_subagent_frontier = support(
    [claim_subagent_delegation],
    claim_design_subagent_delegation_frontier,
    reason=(
        "Design lesson 4 -- delegation as an active frontier "
        "(@claim_design_subagent_delegation_frontier) -- follows "
        "directly from the per-mechanism documentation in the "
        "sub-agent delegation theme (@claim_subagent_delegation)."
    ),
    prior=0.92,
)

# F.5 -- Evaluation implications (5.5).
strat_eval_swebench_confounds = support(
    [
        claim_swebench_central,
        claim_table12_routing,
        claim_routing_dominant_driver,
        claim_taxonomy_enables_controlled_experiments,
    ],
    claim_eval_swebench_confounds,
    reason=(
        "The 5.5 SWE-bench-confounds claim "
        "(@claim_eval_swebench_confounds) follows from (a) the "
        "established centrality of SWE-bench (@claim_swebench_central), "
        "(b) the multi-model routing diversity (@claim_table12_routing) "
        "with cost as the dominant driver "
        "(@claim_routing_dominant_driver), and (c) the related-work "
        "consensus that controlled experiments need taxonomic "
        "variables (@claim_taxonomy_enables_controlled_experiments)."
    ),
    prior=0.92,
)

strat_eval_sampling_iteration = support(
    [
        claim_sampling_vs_iteration,
        claim_swebench_central,
    ],
    claim_eval_sampling_iteration_legibility,
    reason=(
        "The 5.5 sampling-vs-iteration evaluation gap "
        "(@claim_eval_sampling_iteration_legibility) follows from "
        "the cross-cutting theme (@claim_sampling_vs_iteration) and "
        "the SWE-bench dominance making this a real evaluation "
        "concern (@claim_swebench_central)."
    ),
    prior=0.9,
)

# F.6 -- Standardization implications (5.6).
strat_standardization_mcp = support(
    [
        claim_capability_categories_converge,
        claim_table5_tool_sets,
    ],
    claim_standardization_mcp_partial,
    reason=(
        "The 5.6 MCP-partial-standardization claim "
        "(@claim_standardization_mcp_partial) follows from the "
        "convergence on four capability categories "
        "(@claim_capability_categories_converge) combined with the "
        "evidence that 5 corpus agents support MCP per Table 5 notes "
        "(@claim_table5_tool_sets)."
    ),
    prior=0.9,
)

strat_standardization_moatless = support(
    [
        claim_loop_types_compose,
        claim_dars_swe_fork_vs_mini_protocol,
    ],
    claim_standardization_moatless_modular,
    reason=(
        "The 5.6 Moatless-modularity-as-model claim "
        "(@claim_standardization_moatless_modular) follows from the "
        "Moatless dual-flow design as a positive example of "
        "composability (@claim_loop_types_compose) and the "
        "ecosystem-maturity contrast where DARS forked but "
        "mini-swe-agent extended via Protocols "
        "(@claim_dars_swe_fork_vs_mini_protocol)."
    ),
    prior=0.9,
)

strat_standardization_ide = support(
    [claim_ide_as_architecture],
    claim_standardization_ide_tradeoff,
    reason=(
        "The 5.6 IDE-coupling tradeoff claim "
        "(@claim_standardization_ide_tradeoff) follows directly from "
        "the IDE-as-architecture theme (@claim_ide_as_architecture)."
    ),
    prior=0.93,
)

# F.7 -- Section 7 conclusion is the union of the three core findings.
strat_conclusion_three_findings = support(
    [
        claim_spectral_finding_consolidated,
        claim_loop_primitives_thesis,
        claim_eleven_of_thirteen_compose,
        claim_finding_convergence_divergence,
    ],
    claim_conclusion_three_findings,
    reason=(
        "The Section-7 conclusion of three core findings "
        "(@claim_conclusion_three_findings) is the conjunction of "
        "(a) the spectral finding "
        "(@claim_spectral_finding_consolidated), (b) the "
        "5-loop-primitive thesis (@claim_loop_primitives_thesis) "
        "with the 11/13 induction (@claim_eleven_of_thirteen_compose), "
        "and (c) the convergence/divergence pattern "
        "(@claim_finding_convergence_divergence)."
    ),
    prior=0.95,
)

# F.8 -- Future-work claims follow from the spectral & taxonomic findings.
strat_future_controlled = support(
    [
        claim_three_layer_organization,
        claim_taxonomy_enables_controlled_experiments,
        claim_eval_swebench_confounds,
    ],
    claim_future_controlled_experiments,
    reason=(
        "The 'controlled experiments' future-work direction "
        "(@claim_future_controlled_experiments) follows from the "
        "12-dimension taxonomy (@claim_three_layer_organization), "
        "the related-work consensus that the taxonomy enables "
        "controlled experiments (@claim_taxonomy_enables_controlled_experiments), "
        "and the implication that current SWE-bench scores confound "
        "design (@claim_eval_swebench_confounds)."
    ),
    prior=0.9,
)

strat_future_longitudinal = support(
    [
        claim_taxonomy_is_snapshot,
        claim_pinned_commits_for_reproducibility,
        claim_table15_pinned_commits,
    ],
    claim_future_longitudinal,
    reason=(
        "The 'longitudinal re-analysis' future-work direction "
        "(@claim_future_longitudinal) follows from the snapshot-only "
        "limitation (@claim_taxonomy_is_snapshot) plus the pinned "
        "commits enabling exact re-analysis "
        "(@claim_pinned_commits_for_reproducibility, "
        "@claim_table15_pinned_commits)."
    ),
    prior=0.93,
)

strat_future_extend_corpus = support(
    [
        claim_taxonomy_is_snapshot,
        claim_pilot_dimension_coverage_threat,
    ],
    claim_future_extend_corpus,
    reason=(
        "The 'extend corpus' future-work direction "
        "(@claim_future_extend_corpus) follows from the snapshot "
        "limitation (@claim_taxonomy_is_snapshot) and the "
        "pilot-dimension-coverage caveat "
        "(@claim_pilot_dimension_coverage_threat)."
    ),
    prior=0.85,
)

strat_future_arch_aware_eval = support(
    [
        claim_souza_machado_call,
        claim_three_layer_organization,
        claim_eval_swebench_confounds,
    ],
    claim_future_architecture_aware_eval,
    reason=(
        "The 'architecture-aware evaluation' future-work direction "
        "(@claim_future_architecture_aware_eval) follows from Souza "
        "& Machado's prior call (@claim_souza_machado_call), the "
        "12-dimension architectural variables this paper provides "
        "(@claim_three_layer_organization), and the demonstration "
        "that current scores confound (@claim_eval_swebench_confounds)."
    ),
    prior=0.9,
)

# ---------------------------------------------------------------------------
# Block G: Operators -- contradictions between baseline assumptions and
# empirical findings
# ---------------------------------------------------------------------------

# G.1 -- The empirical spectral finding contradicts the baseline assumption
# that capability categories suffice to distinguish agents.
not_both_capability_sufficient_and_spectral = contradiction(
    claim_baseline_capability_taxonomy_sufficient,
    claim_spectral_finding_consolidated,
    reason=(
        "The baseline assumption "
        "(@claim_baseline_capability_taxonomy_sufficient) holds that "
        "capability-category labels (tool-using, planning, "
        "reflective) suffice to distinguish architecturally distinct "
        "coding agents. The empirical spectral finding "
        "(@claim_spectral_finding_consolidated) shows every agent in "
        "the corpus qualifies for every label, yet implementations "
        "differ along 12 continuous spectra. Both cannot be true "
        "simultaneously: if agents are spectrally distinct in ways "
        "the labels cannot express, the labels do not suffice to "
        "distinguish them."
    ),
    prior=0.97,
)

# G.2 -- The empirical 11/13 compose-multiple finding contradicts the
# baseline assumption that a single dominant control architecture suffices.
not_both_react_dominant_and_compose = contradiction(
    claim_baseline_react_is_dominant_architecture,
    claim_eleven_of_thirteen_compose,
    reason=(
        "The baseline assumption "
        "(@claim_baseline_react_is_dominant_architecture) holds that "
        "production coding agents are essentially instances of a "
        "single dominant control architecture (such as ReAct). The "
        "empirical observation (@claim_eleven_of_thirteen_compose) "
        "is that 11 of the 13 agents compose multiple loop "
        "primitives rather than relying on any single control "
        "structure. Both cannot be true simultaneously."
    ),
    prior=0.95,
)

# G.3 -- A counter-hypothesis to the convergence/divergence pattern
# is that all 12 dimensions converge equally (or all diverge equally),
# contradicted by the empirical mixed pattern.
claim_counter_uniform_convergence = claim(
    "**Counter-hypothesis: all dimensions converge (or all diverge) "
    "uniformly.** A baseline view holding that the 12 dimensions "
    "exhibit no informative structural pattern -- i.e. that they "
    "all converge on a single solution as the field matures, or "
    "all diverge equally without pattern -- would predict that "
    "examining cross-dimension structure yields no usable signal "
    "for standardization or research investment.",
    title="Counter-hypothesis: dimensions show no informative convergence/divergence pattern",
)

not_both_uniform_and_mixed_pattern = contradiction(
    claim_counter_uniform_convergence,
    claim_finding_convergence_divergence,
    reason=(
        "The counter-hypothesis (@claim_counter_uniform_convergence) "
        "predicts no informative convergence/divergence structure. "
        "The empirical headline (@claim_finding_convergence_divergence) "
        "observes a mixed pattern: dimensions reflecting external "
        "constraints converge (capability categories, edit format, "
        "isolation) while dimensions reflecting open design questions "
        "diverge (compaction, state, routing). Both cannot hold."
    ),
    prior=0.93,
)

# ---------------------------------------------------------------------------
# Block H: Abduction -- explanation of the spectral finding
# ---------------------------------------------------------------------------

# Hypothesis: agents diverge spectrally because loop primitives compose
# freely (combinatorial design space). Alternative: agents diverge
# spectrally because of arbitrary cosmetic differences (no underlying
# composition structure).

claim_obs_spectral_evidence = claim(
    "**Observation to be explained.** Across all 12 architectural "
    "dimensions of 13 open-source coding agents, agents occupy "
    "distinct positions along continuous spectra (control loops "
    "from fixed pipelines to MCTS; tool counts from 0 to 37; "
    "context compaction with 7 distinct strategies; state "
    "management from destructive overwrite to event sourcing). "
    "Agents are not redundantly clustered.",
    title="Observation: agents span continuous spectra on all 12 dimensions",
)

claim_pred_h_compositional_design = claim(
    "**Hypothesis prediction.** If the spectral pattern arises "
    "because **loop primitives compose freely along an "
    "interdependent design space**, then we should observe (i) "
    "the same primitives recurring across many agents in different "
    "combinations, (ii) the population concentrating in the "
    "multi-primitive zone of the space (most agents combining "
    "multiple primitives), and (iii) decoupling of orchestration "
    "from per-step logic emerging as a recognizable design "
    "pattern in at least one agent (Moatless Tools' ActionAgent / "
    "AgenticLoop / SearchTree separation). The paper documents "
    "all three predictions hold.",
    title="Hypothesis prediction: compositional design predicts recurring primitives + 11/13 multi-primitive + dual-flow design",
)

claim_alt_arbitrary_cosmetic = claim(
    "**Alternative explanation: agents diverge for arbitrary, "
    "cosmetic reasons (no underlying composition structure).** "
    "Under this alternative, the per-dimension diversity reflects "
    "engineering taste, team-history accidents, or shallow "
    "interface differences -- without any underlying compositional "
    "structure to explain the recurring patterns. The spectral "
    "diversity is incidental rather than systematic.",
    title="Alternative: spectral diversity is arbitrary engineering taste, not systematic composition",
)

claim_pred_alt_arbitrary = claim(
    "**Alternative prediction.** If agents diverged for arbitrary "
    "reasons, we would expect (i) no shared primitives across "
    "agents (each agent invents its own building blocks), (ii) no "
    "concentration in a multi-primitive zone (agents would scatter "
    "uniformly, with comparable shares of single-loop and "
    "multi-loop), and (iii) no agent would expose its "
    "composability as an explicit design pattern. None of these "
    "predictions hold -- the same 5 primitives recur, 11/13 "
    "agents compose multiple, and Moatless Tools explicitly "
    "decouples per-step from orchestration.",
    title="Alternative prediction: arbitrary divergence implies no shared primitives, no multi-primitive concentration",
)

abd_spectral_s_h = support(
    [claim_pred_h_compositional_design],
    claim_obs_spectral_evidence,
    reason=(
        "Under the compositional-design hypothesis "
        "(@claim_pred_h_compositional_design), the observed spectral "
        "diversity (@claim_obs_spectral_evidence) is exactly the "
        "predicted observable -- the same primitives combine "
        "differently across agents."
    ),
    prior=0.9,
)

abd_spectral_s_alt = support(
    [claim_alt_arbitrary_cosmetic],
    claim_obs_spectral_evidence,
    reason=(
        "Under the arbitrary-cosmetic alternative "
        "(@claim_alt_arbitrary_cosmetic), the same observed "
        "spectral diversity (@claim_obs_spectral_evidence) could in "
        "principle arise from random engineering choices, but only "
        "if the alternative's auxiliary predictions also held."
    ),
    prior=0.25,
)

abd_spectral_compare = compare(
    claim_pred_h_compositional_design,
    claim_pred_alt_arbitrary,
    claim_obs_spectral_evidence,
    reason=(
        "The compositional-design hypothesis predicts shared "
        "primitives across agents, multi-primitive concentration "
        "(11/13), and explicit decoupling designs (Moatless dual-"
        "flow) -- all observed. The arbitrary-cosmetic alternative "
        "predicts no shared primitives, uniform scatter, and no "
        "decoupling -- none observed. The hypothesis matches the "
        "auxiliary predictions; the alternative does not."
    ),
    prior=0.92,
)

abd_spectral = abduction(
    abd_spectral_s_h,
    abd_spectral_s_alt,
    abd_spectral_compare,
    reason=(
        "Both the compositional-design hypothesis and the "
        "arbitrary-cosmetic alternative attempt to explain the "
        "observed spectral diversity. The hypothesis matches all "
        "three auxiliary predictions (recurring primitives, 11/13 "
        "multi-primitive, explicit decoupling), while the "
        "alternative matches none."
    ),
)

# ---------------------------------------------------------------------------
# Block I: Cross-cutting threats wired to weaken the contributions just
# enough to be honest. Single-author bias modestly weakens the contribution
# claims; pilot-coverage modestly weakens the 12-dimension organization.
# ---------------------------------------------------------------------------

strat_dimensions_not_independent_caveat = support(
    [
        claim_loop_driver_determines_localization_burden,
        claim_dars_swe_fork_vs_mini_protocol,
    ],
    claim_dimensions_not_independent,
    reason=(
        "The 6.2 caveat that dimensions are partially correlated "
        "(@claim_dimensions_not_independent) is supported by the "
        "documented loop-driver/retrieval correlation "
        "(@claim_loop_driver_determines_localization_burden) and the "
        "ecosystem-maturity observation that fork-based and "
        "dependency-based reuse coexist for the same project, "
        "implying that 'how an agent extends a parent' constrains "
        "many downstream dimensions "
        "(@claim_dars_swe_fork_vs_mini_protocol)."
    ),
    prior=0.85,
)

# ---------------------------------------------------------------------------
# Public surface (motivation/thesis/synthesis claims that downstream
# packages may reference)
# ---------------------------------------------------------------------------

__all__ = [
    "claim_design_loop_composition",
    "claim_design_capability_confusion_tradeoff",
    "claim_design_compaction_required",
    "claim_design_subagent_delegation_frontier",
    "claim_eval_swebench_confounds",
    "claim_eval_sampling_iteration_legibility",
    "claim_standardization_mcp_partial",
    "claim_standardization_moatless_modular",
    "claim_standardization_ide_tradeoff",
    "claim_conclusion_three_findings",
    "claim_future_controlled_experiments",
    "claim_future_longitudinal",
    "claim_future_extend_corpus",
    "claim_future_architecture_aware_eval",
    "claim_obs_aider_composes",
    "claim_obs_swe_agent_composes",
    "claim_obs_openhands_composes",
    "claim_obs_codex_composes",
    "claim_obs_gemini_composes",
    "claim_obs_cline_composes",
    "claim_obs_opencode_composes",
    "claim_obs_autocoderover_composes",
    "claim_obs_prometheus_composes",
    "claim_obs_dars_composes",
    "claim_obs_moatless_composes",
    "claim_obs_spectral_evidence",
    "claim_pred_h_compositional_design",
    "claim_alt_arbitrary_cosmetic",
    "claim_pred_alt_arbitrary",
    "claim_counter_uniform_convergence",
]
