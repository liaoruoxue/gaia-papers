"""Layer 2 priors — TPO (2604.06159)"""

PRIORS = {
    "tpo_decouples_rl": {
        "prior": 0.90,
        "justification": (
            "The decoupling is mathematically precise: q_i ∝ p_old_i × exp(u_i/η) "
            "is a closed-form target distribution (no optimization needed), and "
            "cross-entropy fitting is a standard supervised step. "
            "-0.05: the temperature η is still a hyperparameter (though less "
            "sensitive than PPO's clip range + KL penalty). -0.05: decoupling "
            "assumes environment feedback is scalar (reward/score); vector-valued "
            "or structured feedback may not fit the formulation."
        ),
    },
    "tpo_excels_on_sparse_reward": {
        "prior": 0.85,
        "justification": (
            "Token reversal result is qualitative: TPO solves, GRPO/DG don't "
            "learn. This is not a small delta requiring careful statistics. "
            "Neural bandit and sequence tasks replicate the pattern. "
            "-0.08: PG baselines used default hyperparameters; a dedicated "
            "tuning study might narrow the gap. -0.07: all sparse tasks are "
            "single-step; compositional multi-step tasks untested."
        ),
    },
    "tpo_matches_on_dense_reward": {
        "prior": 0.82,
        "justification": (
            "MNIST bandit and WebArena-Turbo results show TPO ≈ PG methods on "
            "dense reward. +16.2pp over prompt engineering (SPA) on WebArena "
            "is expected — any online RL should beat prompt engineering. "
            "-0.08: WebArena-Turbo is a simplified environment; no full "
            "WebArena or SWE-bench evaluation. -0.10: no GPT-4o or Claude-level "
            "model tested; all experiments use 7B class models."
        ),
    },
    "tpo_simplicity_advantage": {
        "prior": 0.88,
        "justification": (
            "TPO eliminates critic, GAE, off-policy correction, and KL penalty "
            "— these are well-known sources of fragility in PG methods. The "
            "remaining hyperparameters (η temperature, batch size) are fewer "
            "and better understood. -0.07: simplicity claim is qualitative; "
            "no ablation on which eliminated component matters most. "
            "-0.05: the cross-entropy step is simple but the target-building "
            "step (q_i) becomes expensive with many candidates."
        ),
    },
    "bandit_and_single_task": {
        "prior": 0.95,
        "justification": (
            "This is a limitation acknowledged by the paper's scope. The "
            "experiments are extensive within the bandit/single-step regime "
            "but do not cover compositional multi-step agent tasks."
        ),
    },
}
