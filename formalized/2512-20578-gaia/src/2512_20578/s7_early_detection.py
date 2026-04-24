"""Section 7: Early Error Detection and Partial Generation Generalization"""

from gaia.lang import claim, setting, support
from .motivation import gnosis_proposal, internal_cues_exist
from .s3_architecture import constant_latency, frozen_backbone
from .s4_results import gnosis_math_perf, gnosis_superior_overall

# ── Settings ───────────────────────────────────────────────────────────────────

partial_gen_setting = setting(
    "Partial generation evaluation applies Gnosis to incomplete responses: at k% completion, "
    "the model has generated k% of the final response tokens. Gnosis observes the hidden states "
    "and attention maps up to that point and predicts whether the full response will be correct. "
    "Gnosis is not re-trained for partial generation; it is applied zero-shot.",
    title="Partial generation evaluation setup",
)

early_termination_setting = setting(
    "Compute-aware early termination uses Gnosis's partial-generation predictions to stop "
    "generation early when a reasoning trajectory is predicted to fail. This can reduce "
    "wasted compute on doomed responses and trigger compute reallocation (e.g., retry or "
    "switch strategy) before full generation completes.",
    title="Compute-aware early termination concept",
)

# ── Claims ─────────────────────────────────────────────────────────────────────

early_detection_perf = claim(
    "Gnosis applied to partial math reasoning generations (zero-shot, no retraining) achieves:\n\n"
    "| Completion % | Gnosis AUROC | MLP-Prob AUROC | Skywork-8B AUROC |\n"
    "|-------------|-------------|----------------|------------------|\n"
    "| 20% | ~0.88 | below 0.85 | below 0.85 |\n"
    "| 40% | ~0.92 | ~0.86 | ~0.90 |\n"
    "| 60% | ~0.93 | ~0.88 | ~0.91 |\n"
    "| 80% | ~0.94 | ~0.89 | ~0.91 |\n"
    "| 100% (full) | 0.95 | 0.86 | 0.90 |\n\n"
    "At 40% completion, Gnosis matches or exceeds the full-completion performance of "
    "competing methods, enabling early stopping of failing trajectories.",
    title="Early error detection performance at partial completions (Figure 3)",
    metadata={"source_figure": "Figure 3", "source_section": "Section 4.5"},
)

gnosis_generalizes_partial = claim(
    "Gnosis generalizes zero-shot to partial generations without additional training, "
    "enabling early detection of failing reasoning trajectories. After observing only "
    "40% of a math reasoning completion, Gnosis achieves AUROC comparable to competing "
    "methods operating on full completions.",
    title="Zero-shot generalization to partial generations",
    metadata={"source_section": "Section 4.5, Abstract"},
)

early_stopping_implication = claim(
    "Because Gnosis can predict correctness from partial generations, it enables compute-aware "
    "control: systems can terminate failing reasoning trajectories early and reallocate compute "
    "to retries or alternative strategies, reducing average inference cost for multi-step "
    "reasoning tasks.",
    title="Early stopping enables compute-aware control",
    metadata={"source_section": "Section 4.5"},
)

# ── Strategy: partial generalization follows from architecture ────────────────

strat_partial_from_arch = support(
    [internal_cues_exist, constant_latency],
    gnosis_generalizes_partial,
    reason=(
        "If correctness cues are intrinsic to the generation process (@internal_cues_exist), "
        "they should be detectable even from partial generations—the internal signals accumulate "
        "as generation progresses. The constant-latency architecture (@constant_latency) that "
        "aggregates over all available positions via PMA naturally handles variable-length "
        "partial sequences without modification, enabling zero-shot partial generalization "
        "as observed in @gnosis_generalizes_partial."
    ),
    prior=0.80,
)

strat_early_stop_from_partial = support(
    [gnosis_generalizes_partial],
    early_stopping_implication,
    reason=(
        "If Gnosis can predict final correctness from 40% of the generation (@gnosis_generalizes_partial), "
        "then predictions at that point are actionable: a system can terminate the generation "
        "confidently when Gnosis signals failure, realizing the compute savings described "
        "in @early_stopping_implication."
    ),
    prior=0.82,
)

strat_early_detection_support = support(
    [gnosis_generalizes_partial, frozen_backbone],
    early_detection_perf,
    reason=(
        "The zero-shot partial generalization capability (@gnosis_generalizes_partial) and "
        "frozen backbone (@frozen_backbone) design together predict the specific numerical "
        "performance pattern in @early_detection_perf: AUROC should increase smoothly with "
        "completion percentage, starting above competing methods even at 20-40% completion."
    ),
    prior=0.85,
)
