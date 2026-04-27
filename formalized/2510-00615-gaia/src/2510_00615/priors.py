"""Prior assignments for the 13 independent leaf claims.

All priors reflect evidence strength and source reliability for the ACON paper
(arXiv:2510.00615). Headline empirical numbers reported in tables are given
high priors; conceptual / qualitative framing claims and abduction-alternative
priors get lower priors per the explanatory-power semantics."""

from .motivation import (
    acon_compresses_history_and_obs,
    context_grows_unbounded,
    cost_scales_with_context,
    heuristics_inadequate,
    long_context_distracts,
)
from .s3_method import strat_distil_pipeline_pivot, trajectory_dense_signal
from .s4_experiments import (
    appworld_history_table,
    appworld_observation_table,
    cost_limitation,
    distillation_results,
    naive_prompting_prediction,
    officebench_table,
    qa_table,
    small_agent_results,
    strong_cost_reduction_claim,
)
from .s5_analysis import optimizer_ablation_data, threshold_ablation_data

PRIORS = {
    # ---- Conceptual framing claims (motivation) ---------------------------
    # Definitionally true: appending every (a_t, o_t) to the running history
    # *is* unbounded growth in token length unless explicitly truncated.
    context_grows_unbounded: (
        0.97,
        "Definitionally true of the agent loop in @agent_loop_setup: every step "
        "appends a new (a_t, o_t) pair, so |h_t| grows monotonically without bound.",
    ),

    # Well-known property of transformer attention; widely supported in the
    # literature on long-context LLMs.
    cost_scales_with_context: (
        0.97,
        "Standard property of transformer attention/decoding: per-token cost is "
        "Theta(n) for KV-attention and Theta(n^2) for full attention. Universally "
        "accepted in the long-context LLM literature.",
    ),

    # Established empirically by Shi et al. (2023) and many follow-ups; the
    # paper itself cites this. Strong priori.
    long_context_distracts: (
        0.92,
        "Empirically established by [@Shi2023] and numerous follow-up studies "
        "showing accuracy degradation when irrelevant context is added.",
    ),

    # Survey-level claim: the paper's own related-works section enumerates the
    # gaps in dialogue summarisation, document compression, KV-cache, and
    # narrow agent compression methods. The qualitative judgement that *all*
    # of them are inadequate for long-horizon agent tasks is the paper's
    # framing — defensible but not as strong as a measurement.
    heuristics_inadequate: (
        0.85,
        "Argued at length in Sections 1-2 with citations covering each existing "
        "approach; the empirical Tables 1-2 also show every baseline (FIFO, "
        "Retrieval, LLMLingua, Prompting) underperforming No-compression on "
        "AppWorld accuracy. Strong support, though 'inadequate' is qualitative.",
    ),

    # Definitional / structural property of the proposed method, not a fact
    # to be tested empirically. The paper *defines* ACON to do both.
    acon_compresses_history_and_obs: (
        0.98,
        "True by construction: ACON is *defined* as the framework that applies "
        "both history compression (@history_compression_rule) and observation "
        "compression (@observation_compression_rule) under selective thresholds.",
    ),

    # ---- Method-section pivot claim --------------------------------------
    # The teacher producing labelled (x, y) pairs is mechanically true once
    # the teacher and guideline exist (Equation 9).
    strat_distil_pipeline_pivot: (
        0.97,
        "Mechanical: with the teacher (phi_T) and optimised guideline P* fixed, "
        "running the teacher on inputs from D_train trivially yields the labelled "
        "(x, f(x; phi_T, P*)) imitation dataset specified in Equation 9.",
    ),

    # Conceptual claim about the value of contrastive trajectories. Plausible
    # and standard in the literature on natural-language gradients, but not
    # a directly measured quantity.
    trajectory_dense_signal: (
        0.85,
        "Standard premise behind textual-gradient methods [@Yuksekgonul2025; "
        "@Khattab2024]: paired success/failure trajectories provide more "
        "diagnostic detail than scalar reward.",
    ),

    # ---- Empirical observation tables (Section 4) ------------------------
    # Reported numbers from Table 1 (gpt-4.1 history compression on AppWorld
    # test-normal). The numbers themselves are directly measured at a fixed
    # seed; the only uncertainty is single-seed variance.
    appworld_history_table: (
        0.93,
        "Directly measured in Table 1 with fixed gpt-4.1-2025-04-14 snapshot and "
        "fixed seed (Reproducibility Statement). Single-seed numbers — small but "
        "non-zero variance budget.",
    ),

    appworld_observation_table: (
        0.93,
        "Directly measured in Table 1 (observation compression rows) under the "
        "same fixed-seed protocol.",
    ),

    officebench_table: (
        0.92,
        "Directly measured in Table 2a; single-seed numbers using fixed gpt-4.1 "
        "snapshot. Slightly lower than AppWorld because OfficeBench test-set size "
        "is not stated in the main text.",
    ),

    qa_table: (
        0.92,
        "Directly measured in Table 2b; EM/F1 averaged across 8 questions. "
        "Single-seed under fixed snapshot.",
    ),

    distillation_results: (
        0.9,
        "Directly measured in Figure 4 across three benchmarks and three student "
        "compressors (Qwen3-14B, Qwen3-8B, Phi-4). Single-seed; some students "
        "*exceed* the teacher on OfficeBench/QA, suggesting variance is not "
        "negligible.",
    ),

    small_agent_results: (
        0.88,
        "Directly measured in Figure 5 with Qwen3-14B as the agent. Reported "
        "numbers in the main text are partial (AppWorld 26.8 -> 33.9; QA 0.158 "
        "-> 0.197 EM); some intermediate values are read from the bar chart.",
    ),

    # ---- Section 4.5 ablation data ---------------------------------------
    threshold_ablation_data: (
        0.9,
        "Directly measured in Figure 6 (single-seed) with three threshold values "
        "each for history and observation. The U-shape is qualitatively clear; "
        "exact peak values are read from the bar chart.",
    ),

    optimizer_ablation_data: (
        0.92,
        "Directly measured in Table 3 with four optimiser configurations on "
        "AppWorld; each row reports a single average accuracy.",
    ),

    # ---- Abduction alternative -------------------------------------------
    # pi(Alt) here is the probability that the *naive Prompting* hypothesis
    # ALONE explains the AppWorld observation table. Prompting reaches only
    # 43.5 vs No-comp 56.0 vs ACON-UTCO 56.5 — naive prompting CANNOT explain
    # ACON-UTCO's recovery to 56.5. Hence pi(Alt) is low (explanatory power),
    # not "naive prompting's calculation is wrong" (it isn't).
    naive_prompting_prediction: (
        0.3,
        "Naive Prompting's own measured numbers (43.5 on AppWorld history) are "
        "factually correct — but that hypothesis cannot explain why ACON-UTCO "
        "reaches 56.5. As an *alternative* explanation of the table, its "
        "explanatory power is low.",
    ),

    # ---- Cost limitation (Figure 7) --------------------------------------
    cost_limitation: (
        0.92,
        "Directly measured in Figure 7: history compression's total API cost is "
        "comparable to or slightly above No-compression, due to KV-cache loss "
        "and compressor calls. The qualitative claim is unambiguous from the bar "
        "chart even without exact dollar values.",
    ),

    # The 'strong' framing of cost reduction is one side of an explicit
    # contradiction with @cost_limitation. It is the *naive interpretation*
    # the paper itself rejects in Section 4.5 (Limitation: Cost Analysis), so
    # its prior is low.
    strong_cost_reduction_claim: (
        0.15,
        "The paper explicitly rebuts this strong framing in Section 4.5 "
        "(Limitation: Cost Analysis). Low prior reflects that the authors "
        "themselves acknowledge it is wrong.",
    ),
}
