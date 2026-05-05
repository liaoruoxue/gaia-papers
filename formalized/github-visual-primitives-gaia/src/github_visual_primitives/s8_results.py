"""Section 2.4 / Layer-2 results -- the Pixmo-Count + Maze Navigation +
Path Tracing comparison panel.

Source: Layer-2 Section 2.4 of the Visual Primitives release
[@DeepSeekVisualPrimitives], cross-validated by [@CSDNDeepRead].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: comparison panel and benchmark definitions
# ---------------------------------------------------------------------------

setup_benchmark_panel = setting(
    "**Benchmark panel.** Three spatial-reasoning benchmarks are "
    "used to compare DeepSeek Visual Primitives against frontier "
    "models: **Pixmo-Count** [@PixmoCount] (counting accuracy), "
    "**Maze Navigation** (path-correctness in synthetic mazes), "
    "and **Path Tracing** (correct identification of which "
    "endpoints connect through tangled curves). Frontier models "
    "compared: GPT-5.4 [@GPT54], Claude 4.6 [@Claude46], "
    "Gemini-3-Flash [@Gemini3Flash].",
    title="Setup: benchmark panel (Pixmo-Count, Maze Navigation, Path Tracing) vs GPT-5.4 / Claude 4.6 / Gemini-3-Flash",
)

setup_random_baseline_50 = setting(
    "**Random baseline on Maze Navigation and Path Tracing.** "
    "Both Maze Navigation and Path Tracing are formulated such "
    "that a uniformly random policy scores at approximately 50% "
    "(binary choice over connectivity / direction at each step "
    "or each pair of endpoints). Scores near 50% therefore "
    "indicate near-random performance.",
    title="Setup: ~50% = random baseline on Maze Navigation and Path Tracing",
)

# ---------------------------------------------------------------------------
# Headline table (transcribed verbatim)
# ---------------------------------------------------------------------------

claim_results_table = claim(
    "**Headline results table (Layer-2 Section 2.4, transcribed "
    "verbatim).** Bold marks per-row best.\n\n"
    "| Benchmark | DeepSeek (Visual Primitives) | GPT-5.4 | Claude 4.6 | Gemini-3-Flash |\n"
    "|-----------|-----------------------------:|--------:|-----------:|---------------:|\n"
    "| Pixmo-Count | **89.2%** | 76.6% | 68.7% | 88.2% |\n"
    "| Maze Navigation | **66.9%** | 50.6% | 48.9% | 49.4% |\n"
    "| Path Tracing | **56.7%** | 46.5% | 30.6% | 41.4% |",
    title="Results table (Pixmo-Count + Maze + Path Tracing vs frontier models)",
    metadata={
        "source_table": "artifacts/github-visual-primitives.md, Layer-2 Section 2.4 (results)",
    },
)

# ---------------------------------------------------------------------------
# Per-benchmark atomic accuracy claims
# ---------------------------------------------------------------------------

claim_pixmo_deepseek = claim(
    "**Pixmo-Count: DeepSeek Visual Primitives = 89.2%.** Best "
    "result on the panel; +1.0 pp over the next-best Gemini-3-"
    "Flash (88.2%) and +12.6 pp over GPT-5.4 (76.6%).",
    title="Result: Pixmo-Count -- DeepSeek 89.2% (panel best)",
)

claim_pixmo_frontier = claim(
    "**Pixmo-Count frontier baselines.** Gemini-3-Flash "
    "[@Gemini3Flash] = 88.2%, GPT-5.4 [@GPT54] = 76.6%, Claude "
    "4.6 [@Claude46] = 68.7%. The frontier already does "
    "reasonably well on counting (Gemini), and DeepSeek's lead "
    "on counting alone is modest.",
    title="Result: Pixmo-Count frontier baselines (Gemini 88.2%, GPT-5.4 76.6%, Claude 68.7%)",
)

claim_maze_deepseek = claim(
    "**Maze Navigation: DeepSeek Visual Primitives = 66.9%.** "
    "Best result on the panel; well above the ~50% random "
    "baseline. +16.3 pp over the next-best GPT-5.4 (50.6%).",
    title="Result: Maze Navigation -- DeepSeek 66.9% (panel best, well above random)",
)

claim_maze_frontier = claim(
    "**Maze Navigation frontier baselines.** GPT-5.4 [@GPT54] = "
    "50.6%, Gemini-3-Flash [@Gemini3Flash] = 49.4%, Claude 4.6 "
    "[@Claude46] = 48.9%. **All three frontier models score "
    "near the ~50% random baseline**, indicating that maze "
    "navigation is essentially unsolved by the frontier.",
    title="Result: Maze Navigation frontier baselines (~50%, all near random)",
)

claim_path_deepseek = claim(
    "**Path Tracing: DeepSeek Visual Primitives = 56.7%.** Best "
    "result on the panel; +10.2 pp over the next-best GPT-5.4 "
    "(46.5%) and +26.1 pp over Claude 4.6 (30.6%).",
    title="Result: Path Tracing -- DeepSeek 56.7% (panel best)",
)

claim_path_frontier = claim(
    "**Path Tracing frontier baselines.** GPT-5.4 [@GPT54] = "
    "46.5%, Gemini-3-Flash [@Gemini3Flash] = 41.4%, Claude 4.6 "
    "[@Claude46] = 30.6%. Claude is below the random baseline -- "
    "it is actively disadvantaged on path tracing -- and the "
    "frontier as a whole is at or below random.",
    title="Result: Path Tracing frontier baselines (Claude 30.6% below random)",
)

# ---------------------------------------------------------------------------
# Cross-benchmark population claim
# ---------------------------------------------------------------------------

claim_cross_benchmark_outperformance = claim(
    "**Cross-benchmark population claim: DeepSeek Visual "
    "Primitives significantly outperforms frontier models on "
    "spatial-reasoning benchmarks at extremely low visual-token "
    "cost (~81 KV entries).** The lift is uniformly positive "
    "across all three benchmarks (Pixmo-Count +1.0 pp over the "
    "next best; Maze +16.3 pp; Path Tracing +10.2 pp), and is "
    "achieved at a visual-token budget orders of magnitude below "
    "what the frontier models use.",
    title="Cross-benchmark synthesis: DeepSeek > frontier on spatial-reasoning at 81-KV-entry budget",
)

claim_frontier_near_random_on_spatial = claim(
    "**Spatial-reasoning gap: frontier models at random on Maze "
    "/ Path Tracing.** GPT-5.4, Claude 4.6, and Gemini-3-Flash "
    "score 48.9-50.6% on Maze Navigation and 30.6-46.5% on Path "
    "Tracing -- in or below the ~50% random regime. This isolates "
    "the spatial-reasoning gap from general multimodal capability: "
    "frontier models can read images but cannot reliably trace "
    "paths or solve mazes.",
    title="Synthesis: frontier models score at or below random on Maze + Path Tracing",
)

# ---------------------------------------------------------------------------
# Foil: the prevailing 'more tokens = better' assumption
# ---------------------------------------------------------------------------

claim_more_tokens_is_better = claim(
    "**Foil: the prevailing assumption that more visual tokens = "
    "better multimodal reasoning.** Frontier multimodal LLMs use "
    "visual-token budgets in the thousands per image and treat "
    "the token count as a primary lever for capability. The "
    "implicit assumption is that more visual tokens reliably "
    "improves visual reasoning. This is the foil the 81-KV-entry "
    "outperformance directly contradicts.",
    title="Foil: 'more visual tokens = better reasoning' (the assumption Visual Primitives contradicts)",
)

__all__ = [
    "setup_benchmark_panel",
    "setup_random_baseline_50",
    "claim_results_table",
    "claim_pixmo_deepseek",
    "claim_pixmo_frontier",
    "claim_maze_deepseek",
    "claim_maze_frontier",
    "claim_path_deepseek",
    "claim_path_frontier",
    "claim_cross_benchmark_outperformance",
    "claim_frontier_near_random_on_spatial",
    "claim_more_tokens_is_better",
]
