"""Layer 2 priors — Knowledge object → (prior, justification)."""

from .motivation import (
    seesaw_phenomenon,
    gradient_conflict_is_root_cause,
    dart_solves_gradient_conflict,
    dart_vs_alternatives,
    leas_diagnostic_framework,
    no_llama_validation,
    single_turn_scope,
)
from .s2_strategies import (
    elegant_dart_token_routing,
    elegant_leas_decomposition,
    surprise_data_mix_useless,
    surprise_dart_rank_insensitive,
    weak_dart_vs_2agent_marginal,
    weak_correlation_not_causation,
    weak_leas_logit_only,
    bdry_qwen_only,
    bdry_lora_only,
    neg_data_mix_fails,
    neg_task_lora_fails,
    neg_inference_hybrid_fails,
)


PRIORS: dict = {
    seesaw_phenomenon: (
        0.92,
        "Observed across 4 model families (Qwen2.5-7B, Qwen3-8B, Qwen3-7B, "
        "Llama3.1-8B) at multiple checkpoints. Joint training degrades "
        "both capabilities vs single-capability training. -0.05: 7-8B only; "
        "-0.03: single RL framework (veRL)."
    ),
    gradient_conflict_is_root_cause: (
        0.85,
        "Three convergent lines: (1) data mixture sweep fails, (2) LEAS "
        "lambda23 < 0 across checkpoints, (3) interaction component "
        "dominates. -0.08: LEAS is linear approximation; -0.07: no "
        "intervention experiment."
    ),
    dart_solves_gradient_conflict: (
        0.88,
        "Structural zero-interaction guarantee + consistent +3.15 to "
        "+4.91 across 3 backbones + rank insensitivity. -0.07: no Llama; "
        "-0.05: max 7B."
    ),
    dart_vs_alternatives: (
        0.75,
        "Beats GRPO (+6.35%) and task-LoRA, approaches 2-agent (~1.2pp). "
        "-0.10: 1.2pp may be within benchmark variance; -0.10: no GPT-4o; "
        "-0.05: Qwen-only."
    ),
    leas_diagnostic_framework: (
        0.82,
        "Identifiability satisfied when design matrix invertible. "
        "-0.10: linearity; -0.08: logit-level may not represent decoded "
        "behavior."
    ),
    no_llama_validation: (
        0.95,
        "Documented limitation, not a contested claim."
    ),
    single_turn_scope: (
        0.90,
        "Single-turn agent tasks only; multi-turn may add interference."
    ),
    surprise_data_mix_useless: (
        0.90,
        "Direct experimental observation: lambda23 stays negative across "
        "data-mix sweeps."
    ),
    surprise_dart_rank_insensitive: (
        0.88,
        "Direct ablation reading from Fig 5 — performance flat across "
        "rank values."
    ),
    weak_dart_vs_2agent_marginal: (
        0.85,
        "The 1.2pp gap is a fact; whether within statistical noise is "
        "the open question (no CI reported)."
    ),
    weak_correlation_not_causation: (
        0.90,
        "Methodological fact: paper does not run an intervention "
        "experiment."
    ),
    weak_leas_logit_only: (
        0.92,
        "LEAS construction is explicitly logit-level and linear by "
        "definition."
    ),
    bdry_qwen_only: (
        0.97,
        "Direct fact: experiments table lists only Qwen-series 7-8B."
    ),
    bdry_lora_only: (
        0.95,
        "Direct mathematical fact: zero-interaction theorem is stated "
        "for the LoRA path with frozen backbone."
    ),
    neg_data_mix_fails: (
        0.90,
        "Reported negative result from ablation experiments."
    ),
    neg_task_lora_fails: (
        0.88,
        "Reported in ablation: task-level LoRA ≈ vanilla SearchR1."
    ),
    neg_inference_hybrid_fails: (
        0.88,
        "Reported in Table 3: hybrid composition does not match "
        "linear-decomposition prediction."
    ),    elegant_dart_token_routing: (
        0.85,
        "Methodological quality assessment; prior reflects clear structural "
        "proof plus empirical confirmation."
    ),
    elegant_leas_decomposition: (
        0.80,
        "Linear-decomposition method is well-defined; prior reflects "
        "identifiability condition being explicit and verifiable."
    ),
}
