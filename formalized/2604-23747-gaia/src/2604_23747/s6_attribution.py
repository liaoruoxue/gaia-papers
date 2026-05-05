"""Section 4 (Decomposing the baseline gap): per-bug quantitative attribution.

Table 2 of the paper isolates the contribution of each bug in the OpenRLHF SFT
pipeline by training four variants and measuring SFT-only evaluation scores
on the AIME24/AIME25/AMC/MATH-500/Olympiad/MMLU-Pro subset. This module
formalizes (a) each row of the waterfall, (b) the quantitative-attribution
claim that the optimizer bug accounts for most of the gap, (c) the
hyperparameter-sensitivity finding for SRFT, and (d) the per-bug effect
on training dynamics.

Source: [@Limozin2026SFTthenRL, Sec. 4 (Decomposing the baseline gap); Table 2;
Table 3; Fig. 2].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setting: the waterfall evaluation subset
# ---------------------------------------------------------------------------

setup_table2_subset = setting(
    "**Table 2 evaluation subset.** Average score is reported over six "
    "benchmarks: AIME24, AIME25, AMC, MATH-500 [@MATH500], OlympiadBench "
    "[@OlympiadBench], MMLU-Pro [@MMLUPro]. Single-node training is used "
    "(rather than 4 nodes) since the number of nodes affects the reported "
    "gradient norm; mean and standard deviation are reported across 3 "
    "seeds for the corrected baselines [@Limozin2026SFTthenRL, Sec. 3; "
    "Table 2].",
    title="Setting: Table 2 evaluation subset = 6 benchmarks averaged, 3 seeds, single-node",
)

# ---------------------------------------------------------------------------
# The four-row waterfall (each row is a measurement claim)
# ---------------------------------------------------------------------------

claim_baseline_openrlhf = claim(
    "**Row 1 (OpenRLHF baseline = 48.3 +/- 0.8).** The unmodified "
    "OpenRLHF [@OpenRLHF] SFT pipeline (both bugs present) trained on "
    "Qwen2.5-Math-7B [@Qwen25Math] achieves an average score of "
    "**48.3 +/- 0.8** across the Table 2 subset, with per-benchmark "
    "scores AIME24=25.8 +/- 0.7, AIME25=25.2 +/- 0.5, AMC=59.0 +/- 1.1, "
    "MATH-500=85.9 +/- 1.0, Olympiad=50.4 +/- 1.8, "
    "MMLU-Pro=43.8 +/- 1.8 [@Limozin2026SFTthenRL, Table 2].",
    title="Row 1: buggy OpenRLHF baseline = 48.3 +/- 0.8 average",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 2 row 1",
        "caption": "Table 2 baseline row.",
    },
)

claim_row_loss_agg_only = claim(
    "**Row 2 (+ fix loss aggregation = 49.1 +/- 0.9).** Fixing only the "
    "loss aggregation bug (Section 2.2 / s5 module) on top of the "
    "OpenRLHF baseline yields an average of **49.1 +/- 0.9**, a gain of "
    "**+0.8** points. Per-benchmark scores: AIME24=28.7, AIME25=24.4, "
    "AMC=60.1, MATH-500=85.5, Olympiad=51.8, MMLU-Pro=44.0 "
    "[@Limozin2026SFTthenRL, Table 2].",
    title="Row 2: + fix loss aggregation = 49.1 (+0.8 over baseline)",
)

claim_row_optimizer_only = claim(
    "**Row 3 (+ fix optimizer = 53.4 +/- 0.4).** Fixing only the "
    "CPU-offloaded optimizer bug (Section 2.1 / s4 module) on top of the "
    "OpenRLHF baseline yields an average of **53.4 +/- 0.4**, a gain of "
    "**+5.1** points. Per-benchmark scores: AIME24=35.1, AIME25=26.9, "
    "AMC=64.9, MATH-500=88.6, Olympiad=55.3, MMLU-Pro=49.4 "
    "[@Limozin2026SFTthenRL, Table 2].",
    title="Row 3: + fix optimizer = 53.4 (+5.1 over baseline)",
)

claim_row_both = claim(
    "**Row 4 (+ fix both = 54.0 +/- 0.2).** Fixing both bugs together "
    "yields an average of **54.0 +/- 0.2**, a gain of **+5.7** points "
    "over the buggy baseline. Per-benchmark scores: AIME24=34.9, "
    "AIME25=28.2, AMC=65.5, MATH-500=89.7, Olympiad=55.6, "
    "MMLU-Pro=49.8 [@Limozin2026SFTthenRL, Table 2].",
    title="Row 4: + fix both = 54.0 (+5.7 over baseline; +0.6 over optimizer-only)",
)

claim_row_verl = claim(
    "**Row 5 (verl reference = 53.8 +/- 0.1).** The independently "
    "implemented verl [@verl] SFT pipeline (FSDP [@FSDP] optimizer; "
    "neither bug present by construction since verl does not use "
    "DeepSpeed) achieves an average of **53.8 +/- 0.1** on the same "
    "Table 2 subset -- statistically indistinguishable from the patched "
    "OpenRLHF result of 54.0 +/- 0.2. Per-benchmark scores: "
    "AIME24=33.6, AIME25=28.2, AMC=65.4, MATH-500=90.0, Olympiad=55.7, "
    "MMLU-Pro=50.2 [@Limozin2026SFTthenRL, Table 2].",
    title="Row 5: verl reference = 53.8 (matches patched OpenRLHF)",
)

# ---------------------------------------------------------------------------
# Quantitative attribution
# ---------------------------------------------------------------------------

claim_attribution_table = claim(
    "**Quantitative attribution table (per-bug contribution to the gap).** "
    "Aggregating Table 2 of the paper, the per-bug contributions to the "
    "5.7-point gap between the buggy OpenRLHF baseline (48.3) and the "
    "fully patched configuration (54.0) decompose as follows:\n\n"
    "| Configuration | Avg | Delta vs baseline |\n"
    "|--------------|----:|------------------:|\n"
    "| OpenRLHF baseline | 48.3 | 0.0 |\n"
    "| + fix loss aggregation only | 49.1 | +0.8 |\n"
    "| + fix optimizer only | 53.4 | +5.1 |\n"
    "| + fix both | 54.0 | +5.7 |\n"
    "| verl reference | 53.8 | +5.5 |\n\n"
    "The optimizer fix recovers approximately +5.1 of the +5.7-point "
    "gap (~89%); the loss aggregation fix contributes the remaining "
    "+0.6 to +0.8 points. The two effects are *roughly* additive "
    "(0.8 + 5.1 = 5.9 vs the joint 5.7) [@Limozin2026SFTthenRL, "
    "Table 2].",
    title="Attribution: optimizer ~+5.1 of 5.7 gap (~89%); loss aggregation +0.6 to +0.8 (~11%)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 2 / Fig. 1 right",
        "caption": "Table 2 + Fig. 1 right: per-bug attribution waterfall.",
    },
)

claim_optimizer_dominates_attribution = claim(
    "**Attribution finding: the CPU-offloaded optimizer bug accounts for "
    "the larger share of the SFT-vs-mixed-policy gap.** Fixing only the "
    "optimizer bug recovers nearly the entire gap (48.3 -> 53.4, a +5.1 "
    "point gain), while fixing only the loss aggregation bug yields a "
    "modest improvement (48.3 -> 49.1, a +0.8 point gain). The "
    "decomposition therefore attributes the *dominant* effect to the "
    "optimizer bug; the loss aggregation bug is a secondary contributor. "
    "This is the empirical content of the 'optimizer bug accounts for "
    "*most* of the gap' headline thesis [@Limozin2026SFTthenRL, Sec. 4; "
    "Fig. 1 right].",
    title="Attribution finding: optimizer bug dominates; loss aggregation bug is secondary",
)

# ---------------------------------------------------------------------------
# Per-bug effect on training dynamics (Fig. 2)
# ---------------------------------------------------------------------------

claim_dynamics_decomposition = claim(
    "**Per-bug effect on training dynamics (Fig. 2).** The two bugs have "
    "distinct, separable signatures in the SFT training curves: "
    "(i) the **aggregation bug** introduces *variability* in the loss "
    "curve without shifting its mean; "
    "(ii) the **optimizer bug** *shifts the mean* of the loss curve "
    "and additionally suppresses gradient norms substantially below "
    "the verl reference (because only the first micro-batch's gradients "
    "reach the optimizer); "
    "(iii) only **both fixes together** reproduce the verl baseline "
    "trajectory in both mean and variability. For gradient norms, only "
    "the optimizer bug has an effect [@Limozin2026SFTthenRL, Fig. 2; "
    "Sec. 4].",
    title="Per-bug dynamics: aggregation -> variability; optimizer -> mean shift + suppressed grad norm",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 2",
        "caption": "Fig. 2: SFT training stability across configurations (loss + gradient norm).",
    },
)

# ---------------------------------------------------------------------------
# Hyperparameter sensitivity (SRFT-specific)
# ---------------------------------------------------------------------------

claim_hyperparam_sensitivity = claim(
    "**Hyperparameter sensitivity (Table 3): SRFT's tenfold-lower "
    "learning rate yields a weaker SFT baseline.** Reproducing the SFT "
    "stage of Fu et al. [@SRFT] with their hyperparameters (10x lower "
    "LR = 5x10^-6, 2x larger batch size = 128, linear schedule with "
    "10% warmup) yields **48.3 +/- 0.2** on the Table 2 subset -- "
    "5.5 points lower than the tuned LUFFY/ReLIFT-style configuration "
    "(53.8 +/- 0.1). Fu et al.'s reported SFT score is 49.7 (close to "
    "our reproduction). Switching to LUFFY/ReLIFT hyperparameters "
    "recovers the 5.5-point gap, reducing the margin between SRFT's "
    "SFT baseline and SRFT's final 55.9 result from 7.6 points down to "
    "2.1 points [@Limozin2026SFTthenRL, Sec. 4; Table 3].",
    title="Hyperparam sensitivity: SRFT's weak-LR SFT baseline accounts for ~5.5 of its apparent gain",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 3",
        "caption": "Table 3: SFT hyperparameter sensitivity; weak-LR config gives 48.3, tuned config gives 53.8.",
    },
)

__all__ = [
    "setup_table2_subset",
    "claim_baseline_openrlhf",
    "claim_row_loss_agg_only",
    "claim_row_optimizer_only",
    "claim_row_both",
    "claim_row_verl",
    "claim_attribution_table",
    "claim_optimizer_dominates_attribution",
    "claim_dynamics_decomposition",
    "claim_hyperparam_sensitivity",
]
