"""Layer 2 strategies + judgment claims.

Design (2026-05-09, after feishu discussion with 陈锟):
  - Method-paper conclusions use deduction() because reasoning in method
    papers is rigid — if the method works, then its premises (correctness,
    boundary conditions, caveats) are coherent; conversely if the
    conclusion is weak, BP reverse-propagates penalty to premises.
  - Weak / Boundary claims ARE premises of deduction (not islands).
    They represent "conditions the conclusion depends on". When BP pulls
    the conclusion down, these conditions get flagged.
  - Surprising / Negative results remain support() premises for
    diagnostic claims (where "evidence → conclusion" is inherently soft).

ref: https://dptechnology.feishu.cn/docx/R143djHcloyPpnx7pnMc0Fh0nVe (张天汉 doc)
"""

from gaia.lang import claim, support, deduction
from .motivation import (
    seesaw_phenomenon,
    gradient_conflict_is_root_cause,
    dart_solves_gradient_conflict,
    dart_vs_alternatives,
    leas_diagnostic_framework,
)


# ══════════════════════════════════════════════════════════════════════
# Surprising findings
# ══════════════════════════════════════════════════════════════════════

surprise_data_mix_useless = claim(
    "Adjusting the reasoning vs tool-use data mixture ratio fails to "
    "eliminate capability interference. λ23 stays negative across "
    "mixture sweeps, indicating a gradient-level rather than data-level "
    "source.",
    title="Surprising: data mixture tuning is ineffective",
    aggregated_from=["claim_interference_dominates", "obs_lambda23_distribution"],
    semantic_refs=["gradient_conflict_is_root_cause"],
    novelty_vs_kb="contradict",
    kb_anchor="rl-training.md#data-mixing",
)

surprise_dart_rank_insensitive = claim(
    "DART's improvement is robust to LoRA rank choice. Performance is "
    "nearly flat across a wide rank sweep, indicating the routing "
    "mechanism (not adapter capacity) drives the gain.",
    title="Surprising: DART improvement is rank-insensitive",
    aggregated_from=[
        "obs_rank_insensitive",
        "claim_gain_not_from_extra_capacity",
        "claim_bottleneck_is_interference_not_capacity",
    ],
    semantic_refs=["dart_solves_gradient_conflict"],
    novelty_vs_kb="refine",
    kb_anchor="rl-training.md#lora-tuning",
)


# ══════════════════════════════════════════════════════════════════════
# Negative results
# ══════════════════════════════════════════════════════════════════════

neg_data_mix_fails = claim(
    "Reported negative result: sweeping data-mixture ratios within ARL "
    "training does not eliminate the seesaw pattern. Excludes data "
    "imbalance as the dominant cause.",
    title="Negative result: data mixture sweep fails to remove seesaw",
    aggregated_from=["claim_interference_dominates"],
    semantic_refs=["gradient_conflict_is_root_cause"],
)

neg_task_lora_fails = claim(
    "Reported negative result: task-level LoRA switching performs "
    "comparably to vanilla SearchR1. Modular adapters alone are "
    "insufficient; token-level routing is required.",
    title="Negative result: task-level LoRA does not disentangle",
    aggregated_from=[
        "claim_multi_lora_cannot_disentangle",
        "claim_task_lora_too_coarse",
        "obs_lora_equals_searchr1",
    ],
    semantic_refs=["dart_solves_gradient_conflict"],
)

neg_inference_hybrid_fails = claim(
    "Reported negative result: hybrid models built by composing "
    "reasoning-isolated and tool-use-isolated subnetworks at inference "
    "underperform the linear-decomposition prediction.",
    title="Negative result: inference-time hybrid is not replicable",
    aggregated_from=[
        "claim_disentanglement_not_replicable_at_inference",
        "table3_hybrid",
    ],
    semantic_refs=["leas_diagnostic_framework"],
)


# ══════════════════════════════════════════════════════════════════════
# Weak / Boundary — as deduction premises (not islands)
# ══════════════════════════════════════════════════════════════════════

weak_dart_vs_2agent_marginal = claim(
    "DART's gap to the 2-agent baseline is only ~1.2pp — within typical "
    "LLM benchmark variance. Without multi-seed CI the equivalence claim "
    "is not statistically established.",
    title="Weak premise: DART vs 2-agent equivalence not statistically established",
    aggregated_from=[
        "obs_dart_approaches_2agent",
        "obs_2agent_strongest",
    ],
    semantic_refs=["dart_vs_alternatives"],
    issue_type="weak_evidence",
    what_would_falsify="multi-seed (>=5) reruns with 95% CI; CI straddling 0 falsifies equivalence",
)

weak_correlation_not_causation = claim(
    "No intervention experiment verifying gradient conflict causes "
    "seesaw. Evidence is correlational.",
    title="Weak premise: no causal intervention, only correlation",
    aggregated_from=[
        "obs_gradient_angles",
        "obs_lambda23_distribution",
        "claim_gradient_conflict_explains_interference",
    ],
    semantic_refs=["gradient_conflict_is_root_cause"],
    issue_type="alt_not_excluded",
    what_would_falsify="inject synthetic gradient conflict; project away to see seesaw vanish",
)

weak_leas_logit_only = claim(
    "LEAS decomposition is defined at the logit level with linear "
    "identifiability. Non-linear interactions below the logit layer may "
    "remain invisible.",
    title="Weak premise: LEAS limited to linear logit-level decomposition",
    aggregated_from=[
        "setup_logit_model",
        "setup_identifiability_condition",
        "claim_design_matrix_invertible",
    ],
    semantic_refs=["leas_diagnostic_framework"],
    issue_type="hidden_assumption",
    what_would_falsify="behavioural A/B on λ23≈0 checkpoints showing residual interference",
)

bdry_qwen_only = claim(
    "All main DART experiments use Qwen-series 7-8B models. Llama, "
    "Mistral, and >8B scales are untested.",
    title="Boundary premise: Qwen 7-8B scope",
    aggregated_from=["table1_qwen3b", "table2_qwen7b"],
    semantic_refs=["dart_solves_gradient_conflict", "seesaw_phenomenon"],
    boundary_type="scope",
    stated_explicitly=False,
)

bdry_lora_only = claim(
    "DART's zero-interaction guarantee is derived under the LoRA+frozen "
    "backbone setup; full-parameter fine-tuning is not covered.",
    title="Boundary premise: LoRA + frozen backbone only",
    aggregated_from=[
        "setup_lora",
        "setup_dart_architecture",
        "claim_dart_zero_interaction",
        "claim_freeze_backbone_necessary",
    ],
    semantic_refs=["dart_solves_gradient_conflict"],
    boundary_type="simplification",
    stated_explicitly=True,
)


# ══════════════════════════════════════════════════════════════════════
# Elegant — metadata-only
# ══════════════════════════════════════════════════════════════════════

elegant_dart_token_routing = claim(
    "DART unifies four ad-hoc techniques with a single structural change: "
    "token-level hard routing plus frozen backbone, yielding a provable "
    "zero-interaction property.",
    title="Elegant: DART's token-level routing unifies prior ad-hoc methods",
    aggregated_from=[
        "claim_dart_zero_interaction",
        "claim_freeze_backbone_necessary",
        "claim_dart_distinguishes_at_token",
    ],
    semantic_refs=["dart_solves_gradient_conflict"],
    portability="high",
    reusable_primitive=True,
)

elegant_leas_decomposition = claim(
    "LEAS decomposes multi-capability logits into capability + "
    "interaction components via six contrast models and a linear "
    "identifiability condition — compact and non-invasive to training.",
    title="Elegant: LEAS's 6-contrast linear decomposition",
    aggregated_from=[
        "claim_design_matrix_invertible",
        "claim_contrast_isolates_lambda23",
        "claim_hybrid_no_interaction",
        "setup_leas_protocol",
    ],
    semantic_refs=["leas_diagnostic_framework"],
    portability="medium",
    reusable_primitive=True,
)


# ══════════════════════════════════════════════════════════════════════
# Strategy chains
# ══════════════════════════════════════════════════════════════════════

# Soft (support): evidence → diagnostic claims where link is inherently uncertain
# ────────────────────────────────────────────────────────────────────
strat_seesaw_excludes_data = support(
    [seesaw_phenomenon, neg_data_mix_fails],
    gradient_conflict_is_root_cause,
    reason=(
        "Seesaw exists and data-mixture sweep fails to remove it. Together "
        "these narrow the mechanism to gradient-level interference."
    ),
    prior=0.82,
)

strat_data_mix_surprise_to_conflict = support(
    [surprise_data_mix_useless],
    gradient_conflict_is_root_cause,
    reason=(
        "Direct positive evidence for a non-data mechanism."
    ),
    prior=0.75,
)


# Rigid (deduction): method-paper conclusions depend on premises
# including boundary/weak claims. BP will reverse-propagate penalty
# to these premises if the conclusion is contested by other evidence.
# ────────────────────────────────────────────────────────────────────
strat_dart_validity = deduction(
    [
        gradient_conflict_is_root_cause,
        leas_diagnostic_framework,
        neg_task_lora_fails,
        neg_inference_hybrid_fails,
        surprise_dart_rank_insensitive,
        bdry_lora_only,
        bdry_qwen_only,
    ],
    dart_solves_gradient_conflict,
    reason=(
        "If (a) gradient conflict is the root cause, (b) LEAS provides a "
        "valid measurement framework, (c) task-level LoRA alone fails, "
        "(d) post-hoc composition fails, (e) DART is rank-insensitive, "
        "AND the claim is scoped to (f) LoRA+frozen-backbone and (g) Qwen "
        "7-8B — then DART structurally resolves the interference within "
        "its stated scope. If empirical contradictions appear (e.g., Llama "
        "failures), BP will assign penalty to the relevant premises."
    ),
    prior=0.90,
)

strat_dart_vs_alt_validity = deduction(
    [dart_solves_gradient_conflict, weak_dart_vs_2agent_marginal],
    dart_vs_alternatives,
    reason=(
        "If DART structurally resolves the interference, its efficiency "
        "and performance edge over alternatives follows — but the "
        "2-agent equivalence claim depends on the statistical "
        "significance premise. If future multi-seed evidence shows the "
        "1.2pp gap is real, BP penalises weak_dart_vs_2agent_marginal."
    ),
    prior=0.85,
)
