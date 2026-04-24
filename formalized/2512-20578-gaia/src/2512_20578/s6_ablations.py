"""Section 6: Ablation Studies"""

from gaia.lang import claim, setting, support, induction
from .s3_architecture import (
    hidden_circuit_arch,
    attention_circuit_arch,
    gated_fusion_arch,
)
from .s4_results import gnosis_math_perf, gnosis_superior_overall

# ── Settings ───────────────────────────────────────────────────────────────────

ablation_backbone_setting = setting(
    "All ablation experiments use Qwen3 1.7B-Hybrid as the backbone unless stated otherwise. "
    "The math reasoning test set (AMC12 + AIME + HMMT) is used as the primary benchmark.",
    title="Ablation study setup",
)

# ── Stream Contribution Claims ─────────────────────────────────────────────────

hidden_only_perf = claim(
    "Using only the Hidden Circuit Encoder (no attention circuit) achieves:\n\n"
    "| Domain | AUROC |\n"
    "|--------|-------|\n"
    "| Math | 0.92 |\n"
    "| TriviaQA | 0.87 |\n"
    "| MMLU-Pro | 0.78 |\n\n"
    "The hidden-only variant provides a robust baseline, performing at 0.87 on TriviaQA "
    "(matching the full Gnosis model) but 0.03 below on math and 0.02 below on MMLU-Pro.",
    title="Hidden-only stream performance (Table 5)",
    metadata={"source_table": "Table 5", "source_section": "Section 4.4"},
)

attention_only_perf = claim(
    "Using only the Attention Circuit Encoder (no hidden circuit) achieves:\n\n"
    "| Domain | AUROC |\n"
    "|--------|-------|\n"
    "| Math | 0.92 |\n"
    "| TriviaQA | 0.78 |\n"
    "| MMLU-Pro | 0.80 |\n\n"
    "Attention-only performs 0.03 below full Gnosis on math, 0.09 below on TriviaQA "
    "(largest drop), and matches Gnosis on MMLU-Pro.",
    title="Attention-only stream performance (Table 5)",
    metadata={"source_table": "Table 5", "source_section": "Section 4.4"},
)

fusion_benefit = claim(
    "The fused Gnosis model (hidden + attention circuits) achieves higher AUROC than "
    "either stream alone on math reasoning (0.95 vs. 0.92 for each individual stream), "
    "and outperforms attention-only on TriviaQA (0.87 vs. 0.78). "
    "The two streams provide complementary information: hidden states are most informative "
    "for TriviaQA, while attention maps add discriminative value for math reasoning tasks.",
    title="Fusion benefit: complementary information streams",
    metadata={"source_table": "Table 5", "source_section": "Section 4.4"},
)

# ── Attention Feature Extractor Ablation ─────────────────────────────────────

cnn_stats_perf = claim(
    "Per-map feature extraction ablation results for the Attention Circuit (Qwen3 1.7B):\n\n"
    "| Variant | Math AUROC | TriviaQA AUROC | MMLU-Pro AUROC |\n"
    "|---------|-----------|----------------|----------------|\n"
    "| CNN + Statistics (Gnosis) | 0.92 | 0.78 | 0.80 |\n"
    "| CNN only | 0.92 | 0.79 | 0.79 |\n"
    "| Statistics only | 0.92 | 0.75 | 0.76 |\n\n"
    "CNN + Statistics is the best overall; statistics-only drops by 0.03-0.04 AUROC "
    "on TriviaQA and MMLU-Pro, suggesting handcrafted attention statistics contribute "
    "meaningfully beyond learned CNN features.",
    title="Attention per-map feature extractor ablation (Table 6)",
    metadata={"source_table": "Table 6", "source_section": "Section 4.4"},
)

# ── Attention Circuit Topology Ablation ──────────────────────────────────────

attention_topology_ablation = claim(
    "Attention Circuit architectural component ablation (math reasoning, Qwen3 1.7B):\n\n"
    "| Variant | Params | AUROC |\n"
    "|---------|--------|-------|\n"
    "| Gnosis (Axial + PMA) | 1.4M | 0.92 |\n"
    "| Linear Projection Only | 1.1M | 0.84 |\n"
    "| Global Transformer | 4.5M | 0.92 |\n"
    "| Remove Layer/Head Embeddings | 1.4M | 0.90 |\n"
    "| Replace PMA with Mean Pooling | 0.9M | 0.85 |\n\n"
    "Axial convolutions + PMA achieve the same AUROC as a much larger Global Transformer "
    "(4.5M), while being 3.2× more parameter-efficient. Removing PMA (mean pooling) or "
    "positional embeddings drops AUROC by 0.02-0.07.",
    title="Attention circuit topology ablation (Table 7)",
    metadata={"source_table": "Table 7", "source_section": "Section 4.4"},
)

attention_grid_ablation = claim(
    "Attention map spatial resolution ablation (math reasoning, Qwen3 1.7B):\n\n"
    "| Variant | AUROC |\n"
    "|---------|-------|\n"
    "| All layers, all maps | 0.91 |\n"
    "| First and last layers only | 0.64 |\n"
    "| Small grid (64×64 pixels) | 0.68 |\n"
    "| Large grid (512×512 pixels) | 0.92 |\n\n"
    "Using only first and last layers drops AUROC by 0.27, confirming that middle-layer "
    "attention patterns carry important discriminative information. Resolution of 256×256 "
    "(Gnosis default) is sufficient; larger grids provide marginal improvement.",
    title="Attention map resolution and layer coverage ablation (Table 8)",
    metadata={"source_table": "Table 8", "source_section": "Section 4.4"},
)

# ── Hidden Circuit Component Ablation ────────────────────────────────────────

hidden_component_ablation = claim(
    "Hidden Circuit component ablation results (math reasoning, Qwen3 1.7B):\n\n"
    "| Variant | Params | AUROC | Drop |\n"
    "|---------|--------|-------|------|\n"
    "| Gnosis (full) | 2.6M | 0.92 | — |\n"
    "| Remove Phase 1 (local processing) | 2.4M | 0.89 | −0.03 |\n"
    "| Remove Gating/SE | 2.6M | 0.91 | −0.01 |\n"
    "| Remove Multi-scale convolutions | 2.4M | 0.90 | −0.02 |\n"
    "| Remove SAB (global aggregation) | 1.3M | 0.85 | −0.07 |\n"
    "| Replace PMA with Mean Pooling | 2.1M | 0.89 | −0.03 |\n"
    "| Pooled MLP baseline | 0.7M | 0.82 | −0.10 |\n\n"
    "Removing SAB causes the largest drop (−0.07 AUROC), confirming that permutation-invariant "
    "global aggregation over layer representations is the most critical component. "
    "Local temporal processing (Phase 1) contributes −0.03; a simple pooled MLP baseline "
    "is 0.10 AUROC below full Gnosis.",
    title="Hidden circuit component ablation (Table 9)",
    metadata={"source_table": "Table 9", "source_section": "Section 4.4"},
)

sab_critical = claim(
    "The Set Attention Block (SAB) component in the Hidden Circuit Encoder is the single most "
    "important architectural component: removing it degrades math reasoning AUROC from 0.92 to "
    "0.85 (−0.07 drop), more than removing any other individual component. This confirms that "
    "permutation-invariant aggregation over the layer sequence is essential for learning "
    "correctness-discriminating representations.",
    title="SAB as most critical hidden circuit component",
    metadata={"source_table": "Table 9"},
)

# ── Strategy: architecture is well-designed ───────────────────────────────────

strat_fusion_design = support(
    [hidden_only_perf, attention_only_perf],
    fusion_benefit,
    reason=(
        "Since hidden-only (@hidden_only_perf) achieves 0.92 AUROC on math while "
        "attention-only (@attention_only_perf) also achieves 0.92 AUROC on math, "
        "yet the fused model achieves 0.95, the streams contribute complementary, "
        "non-redundant information—otherwise fusion would not exceed either stream alone."
    ),
    prior=0.88,
)

strat_sab_critical = support(
    [hidden_component_ablation],
    sab_critical,
    reason=(
        "The ablation (@hidden_component_ablation) shows that removing SAB causes a "
        "−0.07 AUROC drop, the largest single-component degradation. All other components "
        "individually cause at most −0.03. This identifies SAB as the most critical component "
        "in @sab_critical."
    ),
    prior=0.92,
)

strat_axial_efficient = support(
    [attention_topology_ablation],
    attention_circuit_arch,
    reason=(
        "The topology ablation (@attention_topology_ablation) shows that axial convolutions + PMA "
        "match a Global Transformer (0.92 vs 0.92 AUROC) at 1.4M vs 4.5M parameters (3.2× more "
        "parameter-efficient), validating the design choice in @attention_circuit_arch."
    ),
    prior=0.91,
)

# ── Connect ablation data to architecture claims ──────────────────────────────

strat_ablation_supports_fusion = support(
    [hidden_only_perf, attention_only_perf, cnn_stats_perf],
    fusion_benefit,
    reason=(
        "Ablation data (@hidden_only_perf, @attention_only_perf, @cnn_stats_perf) shows "
        "both streams achieve 0.92 AUROC individually on math but 0.95 when fused, "
        "and the hybrid CNN+Statistics extractor outperforms either alone, confirming "
        "complementary contributions described in @fusion_benefit."
    ),
    prior=0.93,
)

strat_ablation_grid_coverage = support(
    [attention_grid_ablation],
    attention_circuit_arch,
    reason=(
        "The grid and layer coverage ablation (@attention_grid_ablation) shows that using "
        "only first/last layers drops AUROC from 0.91 to 0.64, and small grids (64×64) "
        "drop to 0.68, validating the design choices (all-layer coverage, 256×256 grid) "
        "in @attention_circuit_arch."
    ),
    prior=0.90,
)
