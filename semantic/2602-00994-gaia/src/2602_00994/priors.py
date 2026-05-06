"""Layer 2 priors — each with justification."""

PRIORS = {
    "seesaw_phenomenon": {
        "prior": 0.92,
        "justification": (
            "Observed across 4 model families (Qwen2.5-7B, Qwen3-8B, Qwen3-7B, "
            "Llama3.1-8B) and at multiple checkpoints. Controlled experiment: "
            "joint training degrades both capabilities vs single-capability training. "
            "Measurement is well-defined (EM for reasoning, retrieval accuracy for "
            "tool-use). -0.05: all measurements are at 7-8B scale; -0.03: single "
            "RL framework (veRL), no cross-framework replication."
        ),
    },
    "gradient_conflict_is_root_cause": {
        "prior": 0.85,
        "justification": (
            "Three lines of convergent evidence: (1) data mixture adjustment fails "
            "→ rules out data imbalance, (2) LEAS λ23 is negative and consistent "
            "across checkpoints → directly measures gradient interference, "
            "(3) interaction component dominates in interference regions. "
            "-0.08: LEAS is a linear approximation — non-linear interference "
            "may exist but is unmeasured. -0.07: no intervention experiment "
            "(e.g., artificially creating gradient conflict and testing if "
            "seesaw appears). Correlation ≠ causation even with the linear model."
        ),
    },
    "dart_solves_gradient_conflict": {
        "prior": 0.88,
        "justification": (
            "DART structurally guarantees zero gradient interaction (x23=0) via "
            "hard token-level routing through separate LoRA adapters with frozen "
            "backbone. Empirical validation: consistent improvement across Qwen3-8B "
            "(+4.91), Qwen3-7B (+3.82), Qwen2.5-7B (+3.15) on MATH. "
            "Rank insensitivity suggests mechanism, not capacity, drives gain. "
            "-0.07: no Llama validation; -0.05: max 7B, no 70B+ evidence."
        ),
    },
    "dart_vs_alternatives": {
        "prior": 0.75,
        "justification": (
            "DART outperforms GRPO (+6.35% avg), task-specific LoRA (can't "
            "disentangle), and approaches 2-agent (~1.2pp gap). 2-agent comparison "
            "is the closest. Memory efficiency (~1/8) is well-documented. "
            "-0.10: the ~1.2pp gap to 2-agent is within benchmark variance for "
            "LLM evaluations and may not be statistically significant. -0.10: "
            "no GPT-4o or Claude-level baselines to compare against. "
            "-0.05: all comparisons use Qwen backbones only."
        ),
    },
    "leas_diagnostic_framework": {
        "prior": 0.82,
        "justification": (
            "LEAS decomposes model output into reasoning-isolated, tool-use-"
            "isolated, and interaction components. Identifiability condition "
            "is satisfied when the design matrix is invertible. "
            "-0.10: linearity assumption — non-linear interactions between "
            "capabilities would be invisible to LEAS. -0.08: LEAS measures "
            "logit-level effects which may not faithfully represent model "
            "behavior under auto-regressive decoding."
        ),
    },
    "no_llama_validation": {
        "prior": 0.95,
        "justification": (
            "All main experiments use Qwen-series 7-8B models. The paper does "
            "not validate on Llama, Mistral, or any model >8B. This is a "
            "well-documented limitation, not a claim that needs to be verified."
        ),
    },
    "single_turn_scope": {
        "prior": 0.90,
        "justification": (
            "All experiments use single-turn agent tasks (MATH, retrieval). "
            "Multi-turn agentic tasks (e.g., SWE-bench, WebArena) may introduce "
            "additional interference sources (context accumulation, action "
            "sequence dependencies) not captured by LEAS."
        ),
    },
}
