"""Layer 2 priors — SFT-then-RL (2604.23747)"""

PRIORS = {
    "two_bugs_suppress_sft_baseline": {
        "prior": 0.96,
        "justification": (
            "Both bugs are unambiguously confirmed: DeepSpeed PR #6550 is the "
            "specific commit that introduced the optimizer bug; the loss "
            "aggregation bug is independently verifiable from OpenRLHF source. "
            "The fix for each bug is 2 lines. The 5.7 point impact is measured "
            "in a controlled experiment (fix one → measure → fix the other → "
            "measure). -0.03: only tested on DeepSpeed ZeRO-1/2 with CPU offload; "
            "ZeRO-3 or GPU-only configurations may have different bugs. -0.01: "
            "single model (Qwen2.5-Math-7B) for the incremental measurement."
        ),
    },
    "mixed_policy_gains_are_artifact": {
        "prior": 0.93,
        "justification": (
            "Simple arithmetic: corrected SFT = 54.0, best reported mixed-policy "
            "(SRFT) = 53.2. The corrected baseline alone exceeds reported SOTA. "
            "On Llama-3.1-8B, SFT-then-RL = +4.0pp over mixed-policy. "
            "-0.05: limited to math benchmarks; -0.02: no test of whether the "
            "same bugs affect mixed-policy methods' own training (they use the "
            "same buggy frameworks for their SFT phase)."
        ),
    },
    "sft_then_rl_sufficient": {
        "prior": 0.85,
        "justification": (
            "57.0 ID / 59.9 OOD on Qwen2.5-Math-7B, beating all mixed-policy "
            "methods. 50-step SFT-then-RL is compute-efficient. "
            "-0.08: all at ≤8B; -0.05: math domain only; -0.02: the SFT phase "
            "benefits from the same bug fixes that the paper advocates — in "
            "other words, SFT-then-RL's advantage over mixed-policy may partly "
            "be because the SFT phase now works correctly."
        ),
    },
    "cross_framework_validation_essential": {
        "prior": 0.92,
        "justification": (
            "The paper's strongest meta-contribution. Two bugs undetected for "
            "months across three frameworks. Discovered by comparing baselines "
            "across frameworks (not by reading code). No new algorithm needed. "
            "-0.05: single case study — we need more examples to establish this "
            "as a general pattern. -0.03: the argument is stronger as a cautionary "
            "tale than as a proven methodology."
        ),
    },
}
