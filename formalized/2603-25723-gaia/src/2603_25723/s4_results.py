"""Section 4: Results — RQ1, RQ2, RQ3"""

from gaia.lang import (
    claim, setting, question,
    support, deduction, abduction, induction, compare,
    contradiction,
)

from .motivation import (
    q_behavioral_effect,
    q_composability,
    q_migration,
    harness_affects_outcomes,
)

from .s2_approach import (
    nlah_is_portable,
    ihr_separates_concerns,
    nlah_enables_module_ablation,
    file_backed_state_addresses_truncation,
    file_backed_state_definition,
)

from .s3_experiments import (
    swe_bench_setting,
    osworld_setting,
    trae_harness_setting,
    live_swe_setting,
    os_symphony_setting,
    rq1_ablation_design,
    rq2_composition_design,
    rq3_migration_design,
)

# =============================================================================
# RQ1: Behavioral Effect
# =============================================================================

# --- Measured data ---

rq1_trae_full_ihr_perf = claim(
    "On SWE-bench Verified with the TRAE harness family, Full IHR achieves a resolved "
    "rate of 74.4%, using 16.3M prompt tokens, 211k completion tokens, 642.6 tool calls, "
    "414.3 LLM calls, and 32.5 minutes average runtime per sample.",
    title="RQ1: TRAE Full IHR performance metrics",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 1"},
)

rq1_trae_no_rts_perf = claim(
    "On SWE-bench Verified with the TRAE harness family, removing the runtime skill "
    "(w/o RTS) achieves 76.0% resolved rate, 11.1M prompt tokens, 137k completion tokens, "
    "451.9 tool calls, 260.5 LLM calls, and 16.6 minutes runtime.",
    title="RQ1: TRAE w/o RTS performance metrics",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 1"},
)

rq1_trae_no_hs_perf = claim(
    "On SWE-bench Verified with the TRAE harness family, removing the harness skill "
    "(w/o HS) achieves 75.2% resolved rate, 1.2M prompt tokens, 13.6k completion tokens, "
    "51.1 tool calls, 34.0 LLM calls, and 6.7 minutes runtime.",
    title="RQ1: TRAE w/o HS performance metrics",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 1"},
)

rq1_live_swe_full_ihr_perf = claim(
    "On Live-SWE with Full IHR: 72.8% resolved rate, 1.4M prompt tokens, 17.0k "
    "completion tokens, 58.4 tool calls, 41.4 LLM calls, 7.6 minutes runtime.",
    title="RQ1: Live-SWE Full IHR performance metrics",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 1"},
)

rq1_live_swe_no_rts_perf = claim(
    "On Live-SWE without the runtime skill (w/o RTS): 76.0% resolved rate, 1.1M "
    "prompt tokens, 11.7k completion tokens, 41.0 tool calls, 28.2 LLM calls, "
    "5.5 minutes runtime.",
    title="RQ1: Live-SWE w/o RTS performance metrics",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 1"},
)

rq1_trae_paired_flips = claim(
    "Paired flip analysis on SWE-bench Verified using 125 stitched samples: "
    "For TRAE vs. w/o RTS: Full IHR uniquely resolves 4, ablation uniquely resolves 6, "
    "both agree on 115. For TRAE vs. w/o HS: Full IHR uniquely resolves 7, ablation "
    "uniquely resolves 8, both agree on 110.",
    title="RQ1: Paired flip counts TRAE",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 2"},
)

rq1_live_swe_paired_flips = claim(
    "Paired flip analysis for Live-SWE vs. ablations (125 stitched samples): "
    "vs. w/o RTS: Full resolves 4, ablation resolves 8, agree on 113. "
    "vs. w/o HS: Full resolves 4, ablation resolves 7, agree on 114.",
    title="RQ1: Paired flip counts Live-SWE",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 2"},
)

trae_child_agent_share = claim(
    "For TRAE with Full IHR, approximately 90% of total usage occurs in delegated "
    "child agents rather than the runtime-owned parent thread: prompt tokens 91.5%, "
    "completion tokens 91.9%, tool calls 90.2%, LLM calls 90.6%.",
    title="TRAE child agent usage share",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 4"},
)

# --- RQ1 derived conclusions ---

rq1_process_moves_more_than_score = claim(
    "Under Full IHR, process metrics (token counts, tool calls, LLM calls, runtime) "
    "move much more than resolved rate compared to ablations. On SWE-bench Verified, "
    "TRAE and Live-SWE stay within a narrow performance band (74.4%–76.0%), but Full "
    "IHR produces dramatically larger process costs: TRAE Full IHR uses 16.3M prompt "
    "tokens vs. 1.2M for w/o HS (13.6x more) and 642.6 tool calls vs. 51.1 (12.6x more).",
    title="RQ1: Process metrics move more than resolved rate",
)

rq1_ihr_is_not_prompt_wrapper = claim(
    "Full IHR is not merely a prompt wrapper. The ~90% delegation to child agents "
    "in TRAE Full IHR (prompt tokens 91.5%, tool calls 90.2%, LLM calls 90.6%) "
    "demonstrates that the added budget reflects multi-stage exploration, candidate "
    "comparison, artifact handoff, and extra verification — not just richer prompting "
    "of a single agent.",
    title="RQ1: IHR is behaviorally real control, not a prompt wrapper",
)

rq1_most_instances_dont_flip = claim(
    "Most SWE-bench instances do not flip between Full IHR and ablations. Across TRAE "
    "and Live-SWE, paired flip analysis shows that 110–115 of 125 stitched samples "
    "agree between Full IHR and each ablation, with only 4–8 unique resolves per side.",
    title="RQ1: Most instances do not flip under harness changes",
)

rq1_harness_controls_behavior = claim(
    "The shared runtime charter plus harness logic are behaviorally real controls "
    "rather than prompt decoration. The runtime and harness change system behavior "
    "(process metrics, trajectory structure) substantially even when resolved rates "
    "shift only narrowly.",
    title="RQ1: Runtime charter and harness logic are real behavioral controls",
)

# --- Strategies for RQ1 ---

strat_rq1_process_vs_score = support(
    [rq1_trae_full_ihr_perf, rq1_trae_no_hs_perf, rq1_trae_no_rts_perf],
    rq1_process_moves_more_than_score,
    reason=(
        "Comparing @rq1_trae_full_ihr_perf (74.4%, 16.3M tokens, 642.6 tool calls) "
        "with @rq1_trae_no_hs_perf (75.2%, 1.2M tokens, 51.1 tool calls) and "
        "@rq1_trae_no_rts_perf (76.0%, 11.1M tokens, 451.9 tool calls) shows that "
        "removing harness skill collapses process metrics by 13x while barely changing "
        "resolved rate. The pattern holds for Live-SWE. Conclusion: the harness and "
        "runtime dramatically reshape agent behavior even when the final score band is narrow."
    ),
    prior=0.95,
    background=[rq1_ablation_design, swe_bench_setting],
)

strat_rq1_not_prompt_wrapper = support(
    [trae_child_agent_share, rq1_trae_full_ihr_perf],
    rq1_ihr_is_not_prompt_wrapper,
    reason=(
        "If Full IHR were merely a richer prompt for a single agent, all computation "
        "would occur in the parent thread. Instead, @trae_child_agent_share shows ~90% "
        "of tokens and calls are delegated to child agents under @rq1_trae_full_ihr_perf. "
        "This indicates a genuine multi-stage, multi-agent workflow rather than prompt decoration."
    ),
    prior=0.93,
    background=[trae_harness_setting],
)

strat_rq1_flip_evidence = support(
    [rq1_trae_paired_flips, rq1_live_swe_paired_flips],
    rq1_most_instances_dont_flip,
    reason=(
        "@rq1_trae_paired_flips shows 115/125 agreements for TRAE vs. w/o RTS, and "
        "110/125 for TRAE vs. w/o HS. @rq1_live_swe_paired_flips shows 113/125 and "
        "114/125 respectively. Both analyses support the conclusion that most instances "
        "are resolved or unresolved robustly across conditions; only the frontier cases flip."
    ),
    prior=0.95,
    background=[swe_bench_setting],
)

strat_rq1_behavioral_controls = support(
    [rq1_process_moves_more_than_score, rq1_ihr_is_not_prompt_wrapper],
    rq1_harness_controls_behavior,
    reason=(
        "@rq1_process_moves_more_than_score establishes that process metrics diverge "
        "sharply between conditions; @rq1_ihr_is_not_prompt_wrapper confirms the "
        "mechanism is genuine multi-stage delegation. Together these establish that "
        "the runtime charter and harness logic exert real behavioral control on the "
        "agent trajectory, not just cosmetic prompting effects."
    ),
    prior=0.90,
)

# =============================================================================
# RQ2: Module Composition and Ablation
# =============================================================================

# --- Measured data ---

rq2_swe_scores = claim(
    "SWE-bench Verified module ablation scores starting from Basic (75.2%): "
    "file-backed state: 76.8% (+1.6), evidence-backed answering: 76.8% (+1.6), "
    "verifier: 74.4% (-0.8), self-evolution: 80.0% (+4.8), "
    "multi-candidate search: 72.8% (-2.4), dynamic orchestration: 75.2% (0.0).",
    title="RQ2: SWE-bench Verified module scores",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 3"},
)

rq2_osworld_scores = claim(
    "OSWorld module ablation scores starting from Basic (41.7%): "
    "file-backed state: 47.2% (+5.5), evidence-backed answering: 41.7% (0.0), "
    "verifier: 33.3% (-8.4), self-evolution: 44.4% (+2.7), "
    "multi-candidate search: 36.1% (-5.6), dynamic orchestration: 44.4% (+2.7).",
    title="RQ2: OSWorld module scores",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 3"},
)

rq2_self_evolution_mechanism = claim(
    "Self-evolution achieves the largest score gain on SWE (+4.8%) and is the only "
    "module that moves upward on the score-cost graph without moving far right (higher "
    "cost). Its benefit is not open-ended reflection, but a more disciplined "
    "acceptance-gated attempt loop that keeps the search narrow until failure signals "
    "justify another pass.",
    title="RQ2: Self-evolution mechanism — disciplined acceptance-gated loop",
    metadata={"source_figure": "artifacts/2603.25723.pdf, Figure 4"},
)

rq2_file_backed_state_mechanism = claim(
    "File-backed state and evidence-backed answering move moderately right (higher "
    "token cost) for only mild score gains on SWE (+1.6% each), consistent with "
    "process-structure benefits (cleaner artifact handoff, explicit evidence discipline) "
    "rather than large correctness gains.",
    title="RQ2: File-backed state provides process-structure benefits at moderate cost",
)

rq2_verifier_negative = claim(
    "The verifier module shows a negative score effect on SWE (-0.8%) and OSWorld "
    "(-8.4%). Case study evidence (django__django-13406 and an OSWorld case) shows "
    "that local acceptance layers can diverge from the benchmark's final acceptance "
    "object: a run can report internal success while the official evaluator still fails.",
    title="RQ2: Verifier module can diverge from benchmark acceptance object",
)

rq2_frontier_concentration = claim(
    "Module effects concentrate on a small solved frontier rather than shifting the "
    "whole benchmark uniformly. Most tasks are either solved robustly by nearly all "
    "conditions or remain unsolved across conditions. The informative differences come "
    "from boundary cases that flip under changed control logic.",
    title="RQ2: Module effects concentrate at the solved frontier",
)

rq2_module_families = claim(
    "Harness modules fall into two qualitatively different families: (1) modules that "
    "improve the solve loop itself (e.g., self-evolution: tighter acceptance-gated loop "
    "better aligned with benchmark gate), and (2) modules that add local process layers "
    "whose notion of success is weakly aligned with the final benchmark (e.g., verifier, "
    "multi-candidate search). The first family helps more reliably.",
    title="RQ2: Two families of harness modules — loop-improving vs. process-layering",
)

# --- RQ2 strategies ---

strat_rq2_module_frontier = support(
    [rq2_swe_scores, rq2_osworld_scores],
    rq2_frontier_concentration,
    reason=(
        "Both @rq2_swe_scores and @rq2_osworld_scores show that most modules produce "
        "small or zero changes in mean score, yet their complementarity with Basic "
        "(union solved set) shows they do change which specific boundary tasks are "
        "recoverable. This pattern is consistent with effects concentrated at the "
        "solved frontier rather than uniform shifts."
    ),
    prior=0.88,
    background=[rq2_composition_design],
)

strat_rq2_self_evolution = support(
    [rq2_swe_scores, rq2_self_evolution_mechanism],
    rq2_module_families,
    reason=(
        "@rq2_swe_scores shows self-evolution is the largest single-module gain (+4.8% SWE). "
        "@rq2_self_evolution_mechanism explains the mechanism: the acceptance-gated attempt "
        "loop aligns the solve criterion with the benchmark gate, improving the frontier "
        "without expanding to a larger, costlier search tree. By contrast, verifier and "
        "multi-candidate search are dominated on the score-cost graph. This contrast "
        "supports the two-family taxonomy in @rq2_module_families."
    ),
    prior=0.85,
    background=[rq2_composition_design, swe_bench_setting],
)

strat_rq2_verifier_divergence = support(
    [rq2_verifier_negative],
    rq2_module_families,
    reason=(
        "@rq2_verifier_negative provides evidence that process-layering modules (verifier) "
        "can actively harm performance when local acceptance diverges from benchmark "
        "acceptance. This is the canonical failure mode of the second module family: "
        "adding process structure whose success criterion is misaligned with the "
        "benchmark's actual evaluator."
    ),
    prior=0.87,
)

# =============================================================================
# RQ3: Code-to-Text Migration
# =============================================================================

rq3_os_symphony_code_perf = claim(
    "OS-Symphony original code harness on OSWorld: 30.4% resolved rate, 11.4M "
    "prompt tokens, 147.2k completion tokens, 99 agent calls, 651 tool calls, "
    "1.2k LLM calls, 361.5 minutes runtime.",
    title="RQ3: OS-Symphony code harness performance",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 5"},
)

rq3_os_symphony_nlah_perf = claim(
    "OS-Symphony reconstructed NLAH under IHR on OSWorld: 47.2% resolved rate, "
    "15.7M prompt tokens, 228.5k completion tokens, 72 agent calls, 683 tool calls, "
    "34 LLM calls, 140.8 minutes runtime.",
    title="RQ3: OS-Symphony NLAH under IHR performance",
    metadata={"source_table": "artifacts/2603.25723.pdf, Table 5"},
)

rq3_behavioral_relocation = claim(
    "Under IHR, OS-Symphony migrated from a screenshot-grounded repair loop (verify "
    "previous step, inspect screen, choose GUI action, retry on focus/selection errors) "
    "to a file-backed and artifact-backed verification approach. Migrated runs "
    "materialize task files, ledgers, and explicit artifacts, and switch more readily "
    "from brittle GUI repair to file, shell, or package-level operations when those "
    "provide a stronger completion certificate.",
    title="RQ3: OS-Symphony behavioral relocation from GUI repair to artifact-backed verification",
)

rq3_search_relocation = claim(
    "Among 6 native-search samples whose migrated inner streams are retained, only 3 "
    "also contain explicit web_search in the migrated version, and 1 additional migrated "
    "sample uses a different form of search. Search is preserved functionally under "
    "migration but relocated topologically — from a native detachable tutorial detour "
    "to a contract-first runtime flow.",
    title="RQ3: Search preserved functionally but relocated topologically",
)

rq3_topology_difference = claim(
    "The native OS-Symphony topology is a desktop control loop with occasional "
    "detachable tutorial detours (36 main traces + 7 short nested search_1 traces). "
    "The migrated IHR topology is a contract-first runtime flow whose state lives in "
    "task files, ledgers, and artifacts (34 retained inner event streams + 2 "
    "missing-inner-stream stubs).",
    title="RQ3: Different topology — GUI loop vs. contract-first artifact flow",
)

rq3_migration_score_gain = claim(
    "The NLAH migration of OS-Symphony achieves 47.2% on OSWorld vs. 30.4% for the "
    "native code harness — a gain of 16.8 percentage points. The more important "
    "difference is behavioral: the migration relocates reliability mechanisms from "
    "local screen repair to durable runtime state and artifact-backed closure.",
    title="RQ3: NLAH migration achieves +16.8pp on OSWorld with behavioral relocation",
)

alt_score_gain_artifacts = claim(
    "The score gain of the NLAH migration (+16.8pp on OSWorld) may reflect IHR's "
    "file-backed state and artifact conventions providing a more reliable completion "
    "signal, rather than the NLAH representation itself being the primary cause.",
    title="Alternative: score gain may reflect IHR artifact conventions, not NLAH representation",
)

# --- Abduction for RQ3 migration score gain ---

pred_nlah_explains = claim(
    "If the NLAH representation and IHR runtime semantics jointly explain the +16.8pp gain, "
    "the migrated harness should exhibit behavioral relocation from GUI repair to "
    "artifact-backed verification, which is consistent with the observed trajectory evidence.",
    title="Prediction: NLAH+IHR explains score gain via behavioral relocation",
)

pred_artifact_conventions_explains = claim(
    "If IHR artifact conventions alone (file-backed state) explain the gain, we would expect "
    "similar gains from adding the file-backed state module alone to the Basic OSWorld baseline, "
    "without requiring full NLAH migration.",
    title="Prediction: IHR artifact conventions alone could explain gain",
)

s_h_migration = support(
    [rq3_migration_score_gain],
    rq3_behavioral_relocation,
    reason=(
        "@rq3_migration_score_gain (47.2% vs. 30.4%) is consistent with @rq3_behavioral_relocation: "
        "the migrated harness switches from brittle GUI repair to durable artifact-backed verification, "
        "which provides more robust completion certificates aligned with the OSWorld evaluator."
    ),
    prior=0.82,
)

s_alt_migration = support(
    [alt_score_gain_artifacts],
    rq3_behavioral_relocation,
    reason=(
        "@alt_score_gain_artifacts: The file-backed state module alone on OSWorld Basic raises "
        "performance from 41.7% to 47.2% (+5.5%), which approaches but does not fully explain "
        "the 16.8pp gap. The alternative's explanatory power is limited."
    ),
    prior=0.35,
)

comp_migration = compare(
    pred_nlah_explains,
    pred_artifact_conventions_explains,
    rq3_behavioral_relocation,
    reason=(
        "@pred_nlah_explains fits well: NLAH migration not only adds file-backed state "
        "but restructures the entire control topology to be contract-first (@rq3_topology_difference), "
        "which provides broader coverage than any single module. @pred_artifact_conventions_explains "
        "is partially supported (file-backed state alone gives +5.5% on OSWorld) but cannot "
        "account for the full gap or the topology relocation."
    ),
    prior=0.78,
)

abduction_rq3_migration = abduction(
    s_h_migration,
    s_alt_migration,
    comp_migration,
    reason=(
        "Both the NLAH+IHR hypothesis and the artifact-conventions-only alternative "
        "attempt to explain the behavioral relocation in the OS-Symphony migration."
    ),
    background=[rq3_migration_design, osworld_setting, os_symphony_setting],
)

# --- Additional strategies to connect RQ3 evidence ---

strat_rq3_score_from_data = support(
    [rq3_os_symphony_code_perf, rq3_os_symphony_nlah_perf],
    rq3_migration_score_gain,
    reason=(
        "@rq3_os_symphony_code_perf (30.4% OSWorld) and @rq3_os_symphony_nlah_perf "
        "(47.2% OSWorld) directly establish the +16.8pp performance gap. "
        "The raw scores are the primary evidence for the migration score gain."
    ),
    prior=0.98,
    background=[rq3_migration_design, osworld_setting],
)

strat_rq3_topology_evidence = support(
    [rq3_topology_difference, rq3_search_relocation],
    rq3_behavioral_relocation,
    reason=(
        "@rq3_topology_difference shows that native OS-Symphony is a desktop control loop "
        "with detachable tutorial detours, while the migrated IHR topology is a contract-first "
        "artifact flow. @rq3_search_relocation corroborates this: search behavior is "
        "preserved functionally but relocated topologically — from a detachable detour to "
        "an integrated part of the contract-first flow. Together these establish the "
        "behavioral relocation from GUI repair to artifact-backed verification."
    ),
    prior=0.90,
    background=[rq3_migration_design],
)

strat_rq1_live_swe_process = support(
    [rq1_live_swe_full_ihr_perf, rq1_live_swe_no_rts_perf],
    rq1_process_moves_more_than_score,
    reason=(
        "@rq1_live_swe_full_ihr_perf (72.8%, 1.4M tokens, 58.4 tool calls) vs. "
        "@rq1_live_swe_no_rts_perf (76.0%, 1.1M tokens, 41.0 tool calls) shows "
        "that even in the lighter Live-SWE regime, Full IHR raises process metrics "
        "(tokens, calls, runtime) substantially while the score stays in a narrow band. "
        "This corroborates the same pattern in the TRAE rows."
    ),
    prior=0.93,
    background=[rq1_ablation_design, live_swe_setting],
)

strat_rq2_file_backed_mechanism = support(
    [rq2_file_backed_state_mechanism, rq2_swe_scores],
    rq2_frontier_concentration,
    reason=(
        "@rq2_file_backed_state_mechanism shows that file-backed state and evidence-backed "
        "answering move moderately right on the score-cost graph for only mild score gains "
        "(+1.6% SWE each) — consistent with process-structure benefits at boundary cases "
        "rather than broad correctness improvements. @rq2_swe_scores provides the "
        "quantitative basis. This pattern supports the frontier-concentration interpretation."
    ),
    prior=0.85,
    background=[rq2_composition_design],
)
