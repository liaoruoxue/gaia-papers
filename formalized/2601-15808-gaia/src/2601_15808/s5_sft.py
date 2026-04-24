"""Section 5 & 7.3: DeepVerifier-4K Dataset and Open-Source Model Fine-Tuning"""

from gaia.lang import (
    claim, setting,
    support,
)

from .motivation import contrib_dataset
from .s3_taxonomy import taxonomy_dataset
from .s4_deepverifier import full_deepverifier_performance, ck_pro_as_verifier
from .s5_scaling import scaling_generalizes, gaia_full_scaling


# ── Dataset construction settings ────────────────────────────────────────────

sft_base_trajectories = setting(
    "Base trajectories for DeepVerifier-4K are collected from 400 DRA runs on WebAggregatorQA "
    "[@Wang2025], using CK-Pro with Claude-3.7-Sonnet backbone. Tasks span information aggregation "
    "across 10+ domains requiring significant online exploration.",
    title="Base trajectory collection for SFT dataset",
)

sft_filtering_protocol = setting(
    "Filtering: Only true positive verifications (correctly reject wrong answers) and true negative "
    "verifications (correctly accept correct answers) are retained. After balancing these trajectories, "
    "verification trajectories are converted to prompt-response pairs.",
    title="SFT data filtering and balancing protocol",
)

sft_training_config = setting(
    "Training configuration for DeepVerifier-8B: Qwen3-8B base model fine-tuned on a mixture of "
    "DeepVerifier-4K and the CK-Pro-8B training set from Fang et al. (2025b) [@Fang2025b]. "
    "Mixed training preserves foundational capabilities while adding reflection ability.",
    title="SFT training configuration for DeepVerifier-8B",
)

# ── Dataset construction claims ───────────────────────────────────────────────

deepverifier_4k_construction = claim(
    "DeepVerifier-4K is constructed from 400 initial DRA verification trajectories (using "
    "DeepVerifier with Claude-3.7-Sonnet). After filtering for correctly verified true positives "
    "and true negatives and balancing, the dataset contains 4,646 high-quality prompt-response pairs. "
    "Examples emphasize reflection and self-critique.",
    title="DeepVerifier-4K: 4,646 high-quality verification pairs",
    background=[sft_base_trajectories, sft_filtering_protocol],
)

strat_4k_from_filtering = support(
    [full_deepverifier_performance],
    deepverifier_4k_construction,
    reason=(
        "@full_deepverifier_performance establishes that DeepVerifier correctly identifies both "
        "correct and incorrect DRA answers. The 400 base trajectories from WebAggregatorQA "
        "(collected with CK-Pro/Claude-3.7-Sonnet) are filtered by the true-positive/true-negative "
        "protocol, yielding @deepverifier_4k_construction with 4,646 pairs. The key insight is that "
        "the verifier's correct decisions provide high-quality supervision signal [@Wan2026]."
    ),
    background=[sft_base_trajectories, sft_filtering_protocol],
    prior=0.85,
)

# ── Open-source model performance claims ─────────────────────────────────────

deepverifier_8b_gaia = claim(
    "DeepVerifier-8B (Qwen3-8B fine-tuned on DeepVerifier-4K + CK-Pro-8B data) achieves the "
    "highest accuracy among open-source models on GAIA-Full after 10 feedback rounds: 32.2% "
    "(up from 26.7% at 0 rounds, +5.5 points). This surpasses:\n"
    "- CK-Pro-8B (CK-Pro training only): gains only 2.6 points with reflection\n"
    "- Qwen3-8B (no reflection training): shows minimal improvement\n\n"
    "Performance by GAIA difficulty level (GAIA-Full, after 10 rounds):\n\n"
    "| Level | DeepVerifier-8B | CK-Pro-8B | Qwen3-8B |\n"
    "|-------|----------------|-----------|----------|\n"
    "| Level 1 | 40% | 38% | 36% |\n"
    "| Level 2 | 32% | 29% | 28% |\n"
    "| Level 3 | 11% | 8% | 8% |\n"
    "| Average | 34% | 28% | 27% |",
    title="DeepVerifier-8B vs. other open-source models on GAIA",
    background=[sft_training_config, sft_filtering_protocol],
    metadata={"figure": "artifacts/2601.15808.pdf, Figure 1 (lower panel)",
              "caption": "Performance comparison after 10 rounds of verification & feedback on GAIA development set"},
)

reflection_training_matters = claim(
    "Fine-tuning on verification and reflection data (DeepVerifier-4K) is necessary for "
    "open-source models to benefit from test-time scaling. DeepVerifier-8B achieves +5.5 points "
    "improvement with reflection, while CK-Pro-8B (no reflection data) gains only +2.6 points, "
    "and Qwen3-8B (no reflection or CK-Pro training) shows minimal improvement.",
    title="Reflection training is necessary for open-source scaling benefit",
)

strat_reflection_necessary = support(
    [deepverifier_8b_gaia],
    reflection_training_matters,
    reason=(
        "@deepverifier_8b_gaia provides three comparison points: DeepVerifier-8B (+5.5 pts), "
        "CK-Pro-8B (+2.6 pts), Qwen3-8B (~0 pts). The monotone relationship between reflection "
        "training data (full > CK-Pro-only > none) and scaling benefit supports "
        "@reflection_training_matters. The 2x difference (5.5 vs 2.6) between DeepVerifier-8B "
        "and CK-Pro-8B isolates the contribution of DeepVerifier-4K specifically."
    ),
    prior=0.83,
)

open_source_scaling_law = claim(
    "After fine-tuning on DeepVerifier-4K, open-source models (DeepVerifier-8B) exhibit "
    "steady accuracy gains across all 10 feedback rounds on both GAIA subsets: web-based tasks "
    "benefit from better fact verification, and file/reasoning tasks reflect improved general "
    "reasoning control. This demonstrates that reflection ability generalizes across task types "
    "even in 8B-scale models.",
    title="DeepVerifier-4K enables open-source scaling across task types",
    background=[sft_training_config],
)

strat_open_source_generalization = support(
    [deepverifier_8b_gaia, reflection_training_matters],
    open_source_scaling_law,
    reason=(
        "@deepverifier_8b_gaia shows gains on both GAIA-Web (+6.67 pts) and "
        "File/Reasoning/Others (+4.04 pts) subsets, and @reflection_training_matters attributes "
        "this to the DeepVerifier-4K training. @open_source_scaling_law follows: the improvement "
        "is not task-type specific, indicating that the reflection capability is general [@Wan2026]."
    ),
    prior=0.82,
)
