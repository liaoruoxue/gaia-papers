"""Prior assignments for independent (leaf) claims in the HyperAgents formalization.

Run `gaia check --hole .` to see which claims need priors.
Priors are reviewer judgments about plausibility of each independent premise
before inference; they reflect strength of evidence in the source.

Paper: "HyperAgents" (arXiv 2603.19461)
"""

from . import (
    # Motivation
    alignment_assumption_limits_dgm,
    dgm_limitation,
    dgmh_extends_dgm,
    # Empirical measurements — coding
    coding_initial_score,
    dgmh_coding_result,
    dgm_coding_result,
    # Empirical measurements — paper review
    paper_review_initial,
    dgm_paper_review_result,
    # Empirical measurements — robotics
    robotics_initial,
    dgm_robotics_result,
    # Empirical measurements — transfer + compounding
    dgmh_wout_self_improve,
    dgmh_compound_faster,
    dgmh_proofautograder_result,
    dgmh_transfer_agents_score,
    dgm_transfer_imp50,
    # Predictions (abduction framework)
    pred_dgmh_paper,
    pred_dgm_paper,
    pred_dgmh_transfer,
    pred_dgm_transfer,
    # Limitations
    limitation_fixed_task_dist,
    limitation_fixed_outer_loop,
)

PRIORS = {
    # ── Theoretical / structural claims ──────────────────────────────────────

    dgm_limitation: (
        0.88,
        "Well-established in the original DGM paper (Zhang et al. 2025): the instruction-generation "
        "mechanism is described as handcrafted and not modifiable. High confidence in this characterization.",
    ),
    alignment_assumption_limits_dgm: (
        0.78,
        "Argued in the paper and plausible given domain differences between coding and other tasks. "
        "Somewhat uncertain because it is a design-level claim rather than a direct measurement.",
    ),
    dgmh_extends_dgm: (
        0.93,
        "Definitional/architectural claim about DGM-H: it augments DGM with hyperagents. "
        "Described in the Methods section; high confidence.",
    ),

    # ── Empirical measurements — coding ──────────────────────────────────────

    coding_initial_score: (
        0.93,
        "Directly reported initial scores (0.140 on 50-task subset, 0.084 on full Polyglot). "
        "Factual measurement from the experimental setup.",
    ),
    dgmh_coding_result: (
        0.88,
        "Directly reported DGM-H Polyglot results (0.340 CI: 0.300-0.380 on subset; "
        "0.267 CI: 0.231-0.280 on full benchmark), backed by 5 experimental runs. High confidence.",
    ),
    dgm_coding_result: (
        0.88,
        "Reported from the original DGM paper and replicated in this work. "
        "Consistent results across publications.",
    ),

    # ── Empirical measurements — paper review ─────────────────────────────────

    paper_review_initial: (
        0.93,
        "Initial agent score of 0.0 on paper review is a factual observation with clear causal "
        "explanation (no task-specific formatting).",
    ),
    dgm_paper_review_result: (
        0.88,
        "Directly reported DGM and DGM-custom paper review scores with confidence intervals; "
        "5 runs each. High confidence in reported values.",
    ),

    # ── Empirical measurements — robotics ─────────────────────────────────────

    robotics_initial: (
        0.93,
        "Initial agent score of 0.060 on robotics reward design is a factual observation "
        "with clear causal explanation (occasional valid reward function).",
    ),
    dgm_robotics_result: (
        0.88,
        "Directly reported DGM and DGM-custom robotics reward design scores with confidence intervals. "
        "5 runs each.",
    ),

    # ── Empirical measurements — baselines and ablations ─────────────────────

    dgmh_wout_self_improve: (
        0.90,
        "Directly reported DGM-H w/o self-improve baseline performance (0.0 on paper review, "
        "0.213 on robotics), backed by 5 runs with CIs and p-values.",
    ),

    # ── Empirical measurements — transfer and compounding ────────────────────

    dgmh_transfer_agents_score: (
        0.93,
        "Directly reported transfer hyperagent initial scores (0.0 CI: 0.0-0.0) on math grading, "
        "a factual measurement.",
    ),
    dgm_transfer_imp50: (
        0.90,
        "Directly reported DGM-custom transfer imp@50 ≈ 0.0 (CI: 0.0-0.010) on math grading. "
        "Consistent with DGM-custom's domain-specific design.",
    ),
    dgmh_compound_faster: (
        0.80,
        "Described in Figure 4 and its caption: transfer initialization leads to faster progress. "
        "Qualitative claim supported by the figure but without explicit numerical comparison of "
        "rates, introducing some uncertainty.",
    ),
    dgmh_proofautograder_result: (
        0.87,
        "Directly reported (0.700 vs. 0.670 on 200-iteration test; 0.601 vs. 0.561 and 0.175 "
        "vs. 0.178 MAE on full IMO-GradingBench). Well-specified experimental result.",
    ),

    # ── Predictions (abduction framework) ────────────────────────────────────

    pred_dgmh_paper: (
        0.78,
        "Prior that DGM-H would improve paper review: consistent with the design goals and the "
        "general self-improvement mechanism, but the specific domain was a new test.",
    ),
    pred_dgm_paper: (
        0.80,
        "Prior that uncustomized DGM would fail on paper review (score ~0): highly consistent "
        "with the DGM's coding-specific instruction-generation mechanism.",
    ),
    pred_dgmh_transfer: (
        0.72,
        "Prior that hyperagents learn transferable self-improvement strategies: motivated by "
        "the theoretical design but uncertain because general meta-learning is hard.",
    ),
    pred_dgm_transfer: (
        0.78,
        "Prior that DGM-custom lacks transferable meta-improvements: consistent with its "
        "domain-specific customization design.",
    ),

    # ── Limitation claims ─────────────────────────────────────────────────────

    limitation_fixed_task_dist: (
        0.97,
        "Explicitly stated in Section 7 as a limitation. Factual about the system design. "
        "Near-certain.",
    ),
    limitation_fixed_outer_loop: (
        0.97,
        "Explicitly stated in Section 7 as a limitation. Factual about the system design. "
        "Near-certain.",
    ),
}
