"""Section 2.2 / Layer-2 data pipeline -- two-stage pre-training quality
review and post-training cold-start data composition.

Source: Layer-2 Section 2.2 of the Visual Primitives release
[@DeepSeekVisualPrimitives], cross-validated by [@CSDNDeepRead].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: where the pre-training data comes from
# ---------------------------------------------------------------------------

setup_pretrain_source_count = setting(
    "**Pre-training data sources.** Pre-training begins from a "
    "candidate pool of **97,984** annotated visual data sources "
    "drawn from public detection / VQA / scene-graph corpora "
    "(including COCO [@COCO] and GQA [@GQA] derivatives) and "
    "internal collections, before any quality filtering.",
    title="Setup: pre-training begins with 97,984 annotated visual data sources",
)

setup_postpost_filter_purpose = setting(
    "**Two-stage quality review purpose.** The two-stage review "
    "filters the candidate pool down to data whose annotations are "
    "(i) semantically meaningful (Stage 1) and (ii) visually / "
    "geometrically usable as primitive-emission training targets "
    "(Stage 2). The downstream model can only learn to emit `<|box|>` "
    "/ `<|point|>` tokens precisely if its annotations are "
    "themselves precise.",
    title="Setup: two-stage review purpose -- ensure annotations support precise primitive emission",
)

# ---------------------------------------------------------------------------
# Pre-training quality-review table (transcribed verbatim)
# ---------------------------------------------------------------------------

claim_pretrain_filter_table = claim(
    "**Pre-training quality-review pipeline (Layer-2 Section 2.2 "
    "table, transcribed verbatim).**\n\n"
    "| Stage | Input | Output | Filtered out |\n"
    "|-------|------:|-------:|--------------|\n"
    "| Semantic Review (MLLM judge) | 97,984 | 43,141 | pure-numeric categories, private labels, ambiguous abbreviations |\n"
    "| Visual-Geometric Review | 43,141 | 31,701 | severely under-annotated (>50% missing), truncation offsets, oversized boxes (>90% of frame) |",
    title="Pre-training filter table (97,984 -> 43,141 -> 31,701)",
    metadata={
        "source_table": "artifacts/github-visual-primitives.md, Layer-2 Section 2.2 (pre-training quality review)",
    },
)

claim_filter_stage1 = claim(
    "**Stage-1 (Semantic Review).** A multimodal-LLM judge filters "
    "the 97,984 candidate sources down to **43,141**, removing "
    "categories that are pure numbers, private / non-public labels, "
    "or ambiguous abbreviations. This stage is purely about "
    "semantic content, not visual quality.",
    title="Stage-1 Semantic Review: 97,984 -> 43,141",
)

claim_filter_stage2 = claim(
    "**Stage-2 (Visual-Geometric Review).** A visual-geometric "
    "reviewer further filters 43,141 down to **31,701**, removing "
    "severely under-annotated images (more than 50% of objects "
    "missing annotations), images with truncation / coordinate "
    "offset, and images dominated by oversized boxes covering more "
    "than 90% of the frame.",
    title="Stage-2 Visual-Geometric Review: 43,141 -> 31,701",
)

claim_filter_yield = claim(
    "**Pipeline yield: 31,701 / 97,984 = 32.4% retention.** The "
    "two-stage filter retains roughly one third of the candidate "
    "pool. The aggressive filtering is justified by the downstream "
    "training target -- the model is being asked to emit precise "
    "coordinate-bearing tokens, and noisy annotations would teach "
    "it to emit noisy primitives.",
    title="Pipeline yield: ~32.4% retention after two-stage review",
)

# ---------------------------------------------------------------------------
# Post-training cold-start table (transcribed verbatim)
# ---------------------------------------------------------------------------

claim_coldstart_table = claim(
    "**Post-training cold-start data (Layer-2 Section 2.2 table, "
    "transcribed verbatim).**\n\n"
    "| Task | Sample count | Key design |\n"
    "|------|-------------:|------------|\n"
    "| Counting | ~10K | coarse-grained (COCO [@COCO] dense detection) + fine-grained (GQA [@GQA] scene-graph generation) |\n"
    "| Spatial Reasoning / VQA | ~9K | natural scenes + CLEVR [@CLEVR] synthetic + negative samples (queries for non-existent objects) |\n"
    "| Maze Navigation | 460K | DFS / Prim / Kruskal generation, three topologies (rectangular / circular / hexagonal), includes dead-end mazes |\n"
    "| Path Tracing | 125K | Bezier curves; same colour and width to prevent colour-shortcut; locally continuous geometry at intersections |",
    title="Cold-start data table (Counting 10K + VQA 9K + Maze 460K + Path Tracing 125K)",
    metadata={
        "source_table": "artifacts/github-visual-primitives.md, Layer-2 Section 2.2 (cold-start data)",
    },
)

claim_coldstart_total = claim(
    "**Cold-start data total: ~604K samples.** The four task "
    "categories sum to approximately $10\\text{K} + 9\\text{K} + "
    "460\\text{K} + 125\\text{K} = 604\\text{K}$ post-training "
    "samples, with maze navigation accounting for the bulk (~76%).",
    title="Cold-start total: ~604K samples (maze-dominated)",
)

claim_coldstart_design_principles = claim(
    "**Cold-start design principles.** Three principles run "
    "through the cold-start corpus: (a) **negative sampling** -- "
    "Spatial-Reasoning / VQA includes queries for non-existent "
    "objects to teach refusal of false references; (b) **colour-"
    "shortcut prevention** -- Path Tracing renders all curves with "
    "the same colour and width, forcing reliance on geometry; "
    "(c) **topology diversity** -- maze generation uses three "
    "algorithms (DFS, Prim, Kruskal) and three topologies "
    "(rectangular, circular, hexagonal) and includes dead-end "
    "mazes, broadening in-distribution coverage.",
    title="Cold-start design: negative samples + colour-shortcut prevention + topology diversity",
)

__all__ = [
    "setup_pretrain_source_count",
    "setup_postpost_filter_purpose",
    "claim_pretrain_filter_table",
    "claim_filter_stage1",
    "claim_filter_stage2",
    "claim_filter_yield",
    "claim_coldstart_table",
    "claim_coldstart_total",
    "claim_coldstart_design_principles",
]
