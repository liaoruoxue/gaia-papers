"""Section 5: Cross-Model Transfer and Generalization"""

from gaia.lang import claim, setting, support, abduction, compare, induction
from .motivation import gnosis_proposal, internal_cues_exist
from .s3_architecture import frozen_backbone, training_protocol
from .s4_results import gnosis_superior_overall, gnosis_math_perf

# ── Settings ───────────────────────────────────────────────────────────────────

sibling_model_setting = setting(
    "Sibling models are LLMs from the same model family (e.g., Qwen3) that share the same "
    "overall architecture and training procedure but differ in scale (number of parameters). "
    "For example, Qwen3 1.7B, 4B, and 8B are siblings within the Qwen3 family.",
    title="Sibling model definition",
)

zero_shot_transfer_setting = setting(
    "Zero-shot transfer in this context means using a Gnosis head trained on one backbone "
    "(e.g., Qwen3 1.7B) to judge outputs from a different, larger backbone (e.g., Qwen3 4B or 8B) "
    "without any additional fine-tuning on the larger model. The head is applied directly.",
    title="Zero-shot transfer evaluation setup",
)

# ── Transfer Results ───────────────────────────────────────────────────────────

transfer_math_results = claim(
    "Zero-shot transfer of Gnosis head trained on Qwen3 1.7B to larger Qwen3 sibling models "
    "(math reasoning):\n\n"
    "| Setup | AUROC | AUPR-c | ECE |\n"
    "|-------|-------|--------|-----|\n"
    "| Gnosis self-judge 1.7B (baseline) | 0.95 | 0.95 | 0.09 |\n"
    "| Gnosis self-judge 4B-Thinking | 0.96 | 0.98 | 0.05 |\n"
    "| Gnosis self-judge 8B-Hybrid | 0.97 | 0.97 | 0.08 |\n"
    "| Gnosis-1.7B → 4B-Thinking (transfer) | 0.97 | 0.99 | 0.07 |\n"
    "| Gnosis-1.7B → 8B-Hybrid (transfer) | 0.97 | 0.98 | 0.10 |\n\n"
    "Zero-shot transfer AUROC (0.97) matches or exceeds self-trained Gnosis heads, "
    "substantially outperforming Skywork-Reward-8B (0.81 AUROC on math).",
    title="Sibling model transfer results — math (Table 3)",
    metadata={"source_table": "Table 3", "source_section": "Section 4.3"},
)

transfer_trivia_results = claim(
    "Zero-shot transfer of Gnosis head trained on Qwen3 1.7B to Qwen3 4B and 8B siblings "
    "(TriviaQA):\n\n"
    "| Setup | AUROC | AUPR-c | ECE |\n"
    "|-------|-------|--------|-----|\n"
    "| Gnosis self-judge 1.7B | 0.87 | 0.79 | 0.10 |\n"
    "| Gnosis-1.7B → 4B-Thinking (transfer) | 0.86 | 0.86 | 0.04 |\n"
    "| Gnosis-1.7B → 8B-Hybrid (transfer) | 0.84 | 0.88 | 0.12 |\n\n"
    "Transfer AUROC (0.84-0.86) is comparable to self-judge AUROC (0.87), "
    "indicating robust generalization across model scale within a family.",
    title="Sibling model transfer results — TriviaQA (Table 3)",
    metadata={"source_table": "Table 3", "source_section": "Section 4.3"},
)

transfer_mmlu_results = claim(
    "Zero-shot transfer of Gnosis head trained on Qwen3 1.7B to Qwen3 4B and 8B siblings "
    "(MMLU-Pro):\n\n"
    "| Setup | AUROC | AUPR-c | ECE |\n"
    "|-------|-------|--------|-----|\n"
    "| Gnosis self-judge 1.7B | 0.80 | 0.90 | 0.11 |\n"
    "| Gnosis-1.7B → 4B-Thinking (transfer) | 0.81 | 0.93 | 0.16 |\n"
    "| Gnosis-1.7B → 8B-Hybrid (transfer) | 0.83 | 0.94 | 0.15 |\n\n"
    "Transfer AUROC (0.81-0.83) is comparable to self-judge (0.80), suggesting the "
    "internal error-prediction circuits are shared across sibling model scales.",
    title="Sibling model transfer results — MMLU-Pro (Table 3)",
    metadata={"source_table": "Table 3", "source_section": "Section 4.3"},
)

transfer_generalizes = claim(
    "A Gnosis head trained on a small 1.7B model transfers zero-shot to larger 4B and 8B "
    "sibling models (within the same model family), achieving AUROC on math reasoning (0.97) "
    "that matches or exceeds self-trained heads (0.96-0.97) and substantially outperforms "
    "the Skywork-Reward-8B external judge (0.81 AUROC).",
    title="Zero-shot transfer to sibling models generalizes",
    metadata={"source_section": "Section 4.3, Abstract"},
)

transfer_fails_cross_family = claim(
    "Zero-shot transfer of Gnosis fails between architecturally different or stylistically "
    "divergent models (e.g., from a thinking-mode to an instruct-mode model, or between "
    "different model families). The internal circuit representations differ sufficiently "
    "that cross-family transfer yields substantially degraded performance.",
    title="Cross-family transfer limitation",
    metadata={"source_section": "Section 5, Limitations"},
)

shared_circuits_hypothesis = claim(
    "Within a model family, sibling models share similar internal circuit structure for "
    "error prediction: the same features of hidden states and attention patterns that "
    "discriminate correct from incorrect outputs in a small model also discriminate them "
    "in larger siblings, reflecting a shared representational basis.",
    title="Shared error-prediction circuits within model family",
    metadata={"source_section": "Section 4.3"},
)

# ── Abduction: transfer success explains shared circuits ─────────────────────

pred_shared = claim(
    "If sibling models share error-prediction circuits, a Gnosis head trained on a small "
    "sibling should transfer zero-shot with near-self-judge performance to larger siblings.",
    title="Shared circuit prediction: transfer should work",
)

pred_no_shared = claim(
    "If error-prediction circuits differ across scales, zero-shot transfer should fail "
    "(AUROC drops substantially below self-judge performance).",
    title="No-shared-circuit prediction: transfer should fail",
)

s_shared = support(
    [shared_circuits_hypothesis],
    transfer_generalizes,
    reason=(
        "The shared circuit hypothesis (@shared_circuits_hypothesis) predicts that transfer "
        "should succeed (as in @pred_shared), because the same internal features encode "
        "correctness across scales. This is indeed observed in @transfer_generalizes "
        "where 1.7B→4B/8B transfer AUROC matches self-trained."
    ),
    prior=0.82,
)

alt_transfer_accidental = claim(
    "Zero-shot transfer success could be due to domain-level statistical similarities "
    "(same evaluation domains) rather than shared internal circuits, i.e., the head "
    "memorized dataset-level patterns that coincidentally transfer.",
    title="Alternative: transfer due to dataset similarity, not circuits",
)

s_alt_transfer = support(
    [alt_transfer_accidental],
    transfer_generalizes,
    reason=(
        "Dataset-level memorization (@alt_transfer_accidental) could produce transfer "
        "if the models perform similarly on the same test sets, but this doesn't explain "
        "why a 1.7B model's internal representation is predictive for an 8B model's errors."
    ),
    prior=0.28,
)

comp_transfer = compare(
    pred_shared,
    pred_no_shared,
    transfer_generalizes,
    reason=(
        "Observed AUROC of 0.97 on math (1.7B → 4B/8B transfer) versus self-judge 0.97 "
        "shows near-identical performance, strongly supporting shared circuits over "
        "scale-specific circuits."
    ),
    prior=0.85,
)

abduction_transfer = abduction(
    s_shared,
    s_alt_transfer,
    comp_transfer,
    reason=(
        "Both the shared-circuits hypothesis and dataset-similarity alternative attempt "
        "to explain transfer success. The shared-circuits hypothesis better explains "
        "the observation because it predicts scale-invariant transfer, which is observed."
    ),
)

# ── Support for transfer from architecture ────────────────────────────────────

strat_transfer_from_internal = support(
    [internal_cues_exist, frozen_backbone],
    transfer_generalizes,
    reason=(
        "If reliable correctness cues are intrinsic to generation (@internal_cues_exist) "
        "and these cues are encoded in the same architectural components (hidden states, "
        "attention maps) across sibling models, then a frozen Gnosis head (@frozen_backbone) "
        "that reads these cues from a small model can do so from larger siblings without "
        "retraining, predicting the observed transfer success (@transfer_generalizes)."
    ),
    prior=0.78,
)

# ── Connect transfer data to transfer claim ───────────────────────────────────

strat_data_supports_transfer = support(
    [transfer_math_results, transfer_trivia_results, transfer_mmlu_results],
    transfer_generalizes,
    reason=(
        "Detailed transfer results (@transfer_math_results, @transfer_trivia_results, "
        "@transfer_mmlu_results) show zero-shot 1.7B→4B/8B transfer AUROC (0.97/0.86/0.81) "
        "closely matching self-trained heads (0.96/0.87/0.80), directly confirming "
        "@transfer_generalizes."
    ),
    prior=0.96,
)
