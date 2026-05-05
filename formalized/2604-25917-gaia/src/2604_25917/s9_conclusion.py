"""Section 8: Conclusion -- synthesizing the framework, theory, and
empirical results into the paper's exported claim.

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 8.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Conclusion synthesis
# ---------------------------------------------------------------------------

claim_conclusion_synthesis = claim(
    "**Conclusion: RecursiveMAS as a scalable, efficient framework for "
    "system-level MAS recursion.** RecursiveMAS introduces a recursive "
    "multi-agent framework that scales agent collaboration through "
    "system-level recursion. It (i) supports latent-thoughts "
    "generation within each agent through the inner RecursiveLink, "
    "(ii) connects heterogeneous agents through the outer "
    "RecursiveLink, and (iii) optimizes the whole system with the "
    "inner-outer loop training paradigm. Theoretically, the framework "
    "(a) achieves more efficient runtime complexity than text-based "
    "baselines (Proposition 3.1) and (b) maintains stable training "
    "dynamics across recursion rounds (Theorem 4.1). Empirically, "
    "across mathematical and scientific reasoning, code generation, "
    "and search benchmarks, RecursiveMAS consistently improves "
    "accuracy (avg +8.3%) while substantially reducing inference "
    "time (1.2x-2.4x speedup) and token usage (34.6%-75.6% "
    "reduction).",
    title="Conclusion: RecursiveMAS = scalable, efficient framework for recursive MAS collaboration",
)

# ---------------------------------------------------------------------------
# Ablation- and analysis-derived sub-claims that synthesize at the close
# ---------------------------------------------------------------------------

claim_unified_evolution_recipe = claim(
    "**Unified-evolution recipe.** The combination of (i) heterogeneous "
    "agents chained as a recursive loop, (ii) frozen base LLMs with "
    "only lightweight RecursiveLinks trained, and (iii) a shared "
    "outer-loop credit signal back-propagated across recursion rounds, "
    "delivers system-level collaboration that improves over both (a) "
    "individually fine-tuned single agents and (b) text-mediated MAS "
    "frameworks, *without* requiring any base LLM re-training. The "
    "recipe is the operational distillation of the inner-outer loop "
    "training paradigm and is the central method-level contribution "
    "of the paper.",
    title="Synthesis: unified-evolution recipe -- frozen LLMs + lightweight recursive links + shared outer-loop credit",
)

# ---------------------------------------------------------------------------
# Limitations / open questions implied by Sec. 5-6 analyses
# ---------------------------------------------------------------------------

claim_limit_inference_round_eq_train = claim(
    "**Implicit limitation: inference recursion depth must match "
    "training depth.** RecursiveMAS performs inference recursion for "
    "the same $n$ rounds as during training (Section 4 last "
    "sentence). The system does not currently support dynamic round "
    "selection, so the test-time efficiency vs accuracy trade-off "
    "is fixed at training time. The Figure 1 (Top) scaling-law "
    "study does sweep training-time and inference-time depths "
    "jointly, but there is no within-trained-model dynamic stopping.",
    title="Limitation: no dynamic stopping -- inference rounds = training rounds",
)

claim_limit_optimal_m_modest = claim(
    "**Implicit limitation: latent-thought budget saturates fast and "
    "must be tuned.** The Table 9 / Fig. 8 ablation shows that "
    "performance saturates around $m \\approx 80$ latent thoughts "
    "per agent. Below this, agents under-reason; above this, "
    "additional latent steps are wasted. The optimal $m$ likely "
    "varies by task complexity and model size and currently must "
    "be selected by hyperparameter search rather than learned "
    "dynamically.",
    title="Limitation: optimal latent-thought length m must be tuned (saturates around m ~ 80)",
)

__all__ = [
    "claim_conclusion_synthesis",
    "claim_unified_evolution_recipe",
    "claim_limit_inference_round_eq_train",
    "claim_limit_optimal_m_modest",
]
