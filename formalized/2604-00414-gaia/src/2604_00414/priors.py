"""Prior assignments for Decision-Centric Design for LLM Systems (2604.00414).

These priors cover independent (leaf) claims — i.e., claims not concluded by any strategy.
Derived claims get their beliefs from BP propagation.

Prior scale:
  0.95+  : directly measured / definitionally certain
  0.85-0.94: reported experimental observations (believed highly reliable)
  0.7-0.84 : architectural claims with strong theoretical motivation
  0.5-0.69 : alternative hypotheses, contested or speculative claims
  0.3-0.49 : claims the paper argues against
"""

from . import (
    # Core premises
    alt_prompt_sufficient,
    implicit_control_problem,
    prompt_control_implicit,
    framework_preserves_uncertainty,
    sufficiency_signal_def,
    multi_signal_def,
    # Experiment 1 (calendar) leaf premises
    prompt_calendar_degrades,
    retry_calendar_fails,
    unresolvable_widens_gap,
    k1_failure_localized,
    prompt_predicts_degradation,
    dc_predicts_high_success,
    # Experiment 2 (graph) leaf premises
    s2_sufficiency_isolation,
    prompt_policy_insufficient_for_s5,
    dc_predicts_s5_success,
    prompt_predicts_s5_failure,
    # Experiment 3 (retrieval) leaf premises
    easy_bucket_results,
    hard_bucket_results,
    failure_attribution_retrieval,
    threshold_robustness,
    prompt_correct_assessment_wrong_action,
    dc_predicts_medium_expand,
    prompt_predicts_medium_failure,
)

PRIORS = {
    # ── Core architectural claims ────────────────────────────────────────────
    implicit_control_problem: (
        0.92,
        "The paper's central premise: widely-observable problem in deployed LLM systems. "
        "Supported by concrete examples (retry loops, prompt-based clarify) across the "
        "literature and confirmed by the paper's own prompt baseline failures.",
    ),
    prompt_control_implicit: (
        0.93,
        "Definitional/architectural claim: assessment and action are fused in a single "
        "LLM call in prompt-based systems. Not contested; directly observable from system "
        "architecture.",
    ),
    framework_preserves_uncertainty: (
        0.95,
        "Architectural design property of the DC framework, not an empirical claim. "
        "Follows from definition: the decision interface is made explicit while the "
        "underlying signals remain stochastic.",
    ),
    sufficiency_signal_def: (
        0.92,
        "The sufficiency signal is well-defined in the paper and instantiated concretely "
        "in experiments (boolean field presence, 1/|candidates|, BM25 similarity). "
        "High confidence as a methodological definition claim.",
    ),
    multi_signal_def: (
        0.9,
        "The two-signal instantiation is a specific architectural choice — well-defined "
        "and directly implemented in the graph disambiguation experiment. High confidence "
        "as a design specification claim.",
    ),

    # ── Alternative hypothesis (the one DC argues against) ──────────────────
    alt_prompt_sufficient: (
        0.25,
        "The paper explicitly argues against prompt-based control being sufficient. "
        "The experimental evidence strongly contradicts this: Prompt achieves only 14% "
        "medium retrieval success, 10% calendar success at k=4, and 35% in graph S5, "
        "with 64% of failures showing correct assessment but wrong action. The fundamental "
        "limitation (assessment-action fusion) persists architecturally.",
    ),

    # ── Experiment 1: Calendar (Granite) — directly measured observations ────
    prompt_calendar_degrades: (
        0.93,
        "Directly measured in N=10 runs per scenario on Granite 4 micro. The degradation "
        "pattern (100%→100%→75%→60%→10%) is a direct experimental observation with "
        "clear trend across k values.",
    ),
    retry_calendar_fails: (
        0.95,
        "Retry baseline failure is mechanistically expected and directly measured: without "
        "any clarify mechanism, the system exhausts its T=6 budget on repeated executions "
        "at all k>=1. 0% success at k>=1 is a direct measurement.",
    ),
    unresolvable_widens_gap: (
        0.9,
        "Directly measured: Table 7 shows DC maintains 100% on unresolvable scenarios "
        "while Prompt-Clarify drops to 50%/60%/10% at k=2/3/4. Pattern is consistent "
        "across all unresolvable scenarios tested.",
    ),
    k1_failure_localized: (
        0.88,
        "Directly observable from the diagnostic trace (Figure 1): logged values "
        "show p_suff=0.75 (correct), missing=[duration_min] (correct), but the question "
        "asks about date and time. The fix (constraining prompt) is directly measured "
        "to restore 100% at k=1.",
    ),

    # ── Prediction claims (serve as hypotheses in abduction) ─────────────────
    dc_predicts_high_success: (
        0.85,
        "The DC approach's prediction of high success follows from the design: "
        "$\\hat{p}_{\\text{suff}}=1.0$ gate before execute, plus no-blind-retry constraint, "
        "should logically prevent premature execution and blind retries. High confidence "
        "that the prediction follows from the design specification.",
    ),
    prompt_predicts_degradation: (
        0.8,
        "The prompt-based prediction of degradation with increasing k follows from the "
        "assessment-action fusion architecture. Moderate-high confidence as it is "
        "theoretically motivated and confirmed by empirical results.",
    ),

    # ── Experiment 2: Graph disambiguation ────────────────────────────────────
    s2_sufficiency_isolation: (
        0.92,
        "Directly measured in N=20 runs: DC 100%, Retry 45%, Prompt 85%, Prompt(w/policy) "
        "95% in S2. The causal isolation (psuFF only, single-signal setting) is by "
        "experimental design.",
    ),
    prompt_policy_insufficient_for_s5: (
        0.92,
        "Directly measured in Table 10: both Prompt and Prompt(w/policy) achieve 35% "
        "in S5, below Retry at 60%. The diagnosis (missing belief state update) is "
        "confirmed by the S5 trace analysis.",
    ),
    dc_predicts_s5_success: (
        0.85,
        "DC's prediction of S5 success follows from the design: explicit belief state "
        "maintained and updated after each action. The key mechanism (psuFF rises via "
        "elimination) is deterministic given the structural correctness estimator.",
    ),
    prompt_predicts_s5_failure: (
        0.82,
        "The prompt-based prediction of S5 failure follows from the missing belief state "
        "in the observation payload: the updated candidate count after elimination is not "
        "available at decision time. Mechanistically motivated.",
    ),

    # ── Experiment 3: Retrieval ────────────────────────────────────────────────
    easy_bucket_results: (
        0.95,
        "All methods achieve 100% on easy questions — directly measured, N=50. "
        "The differential retrieval rounds (DC-Dense 1.12 vs Prompt 0.10 vs DC-LLM 0.62) "
        "are directly measured from logged traces.",
    ),
    hard_bucket_results: (
        0.93,
        "Hard bucket results (~18% for all DC methods) directly measured, N=50. "
        "The corpus gap explanation is confirmed by the attribution analysis (Table 12: "
        "98% hard failures are corpus gaps).",
    ),
    failure_attribution_retrieval: (
        0.88,
        "Attribution analysis is directly computed from logged p_dense and p_llm traces "
        "for each failed DC-Composite episode. Medium: 3/3 both-signals-high. Hard: 40/41 "
        "corpus gaps. Direct measurement from logged signals.",
    ),
    threshold_robustness: (
        0.92,
        "Threshold sweep is computed offline from saved per-round signal traces (no model "
        "re-runs), using a held-out test set (N=50) selected before the test set was run. "
        "Direct computation from logged data.",
    ),
    prompt_correct_assessment_wrong_action: (
        0.93,
        "Directly measured from logged prompt free-text reason strings: 28 of 44 medium "
        "failures (64%) contain explicit statements that passages are insufficient followed "
        "by 'stop'. Direct observation from logged outputs.",
    ),
    dc_predicts_medium_expand: (
        0.85,
        "The DC approach's prediction of medium success follows from signal externalization: "
        "the threshold controller strictly follows p >= tau → stop, else expand, so correct "
        "signal values mechanistically produce correct actions.",
    ),
    prompt_predicts_medium_failure: (
        0.8,
        "Prediction follows from assessment-action fusion: even with correct internal "
        "assessment, the fused call may select stop. Confirmed by the 64% correct-assessment-"
        "wrong-action pattern in the logged reason strings.",
    ),
}
