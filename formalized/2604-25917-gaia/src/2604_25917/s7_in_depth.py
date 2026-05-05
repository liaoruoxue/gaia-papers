"""Section 6: In-depth analyses on RecursiveMAS -- RecursiveLink design
ablation (Table 4), semantic representations across recursion (Fig. 7),
optimal latent-thoughts length (Fig. 8 + Table 9), and training cost
(Table 5).

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 6 +
Tables 4, 5, 9 + Figs. 7, 8.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Section 6: RecursiveLink design ablation (Table 4)
# ---------------------------------------------------------------------------

claim_table4_link_designs = claim(
    "**Table 4: Efficacy of RecursiveLink design choices** (accuracy "
    "%, scaled Sequential-Style, $r = 3$).\n\n"
    "| RecursiveLink Design | MATH500 | GPQA-D | LiveCodeBench |\n"
    "|---|---:|---:|---:|\n"
    "| 1-Layer | 84.4 | 63.2 | 40.1 |\n"
    "| Res + 1-Layer | 86.7 | 65.3 | 41.4 |\n"
    "| 2-Layer | 85.6 | 64.5 | 40.5 |\n"
    "| **Res + 2-Layer (ours)** | **88.0** | **66.2** | **42.9** |\n",
    title="Table 4: RecursiveLink design ablation -- 2-layer + residual is best on all 3 benchmarks",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 4",
    },
)

claim_residual_value = claim(
    "**Residual connection consistently improves performance.** "
    "Adding a residual branch lifts the 1-Layer baseline from "
    "84.4 / 63.2 / 40.1 to 86.7 / 65.3 / 41.4 (deltas +2.3 / +2.1 / "
    "+1.3 pp on MATH500 / GPQA-D / LiveCodeBench). On GPQA-D, Res + "
    "1-Layer (65.3%) even exceeds the plain 2-Layer (64.5%) without "
    "residual, indicating that residual contributes more than the "
    "extra layer alone.",
    title="Result: residual connection adds +1.3 to +2.3 pp on top of any layer count",
)

claim_two_layer_value = claim(
    "**A second layer improves accuracy when paired with the "
    "residual.** Going from Res + 1-Layer (86.7 / 65.3 / 41.4) to "
    "Res + 2-Layer (88.0 / 66.2 / 42.9) adds +1.3 / +0.9 / +1.5 pp. "
    "The 2-Layer + residual combination is the chosen production "
    "design and is the architecture of every other reported "
    "RecursiveMAS result.",
    title="Result: 2nd layer adds +0.9 to +1.5 pp on top of residual; chosen production design",
)

# ---------------------------------------------------------------------------
# Section 6: semantic representations across recursion (Figure 7)
# ---------------------------------------------------------------------------

claim_semantic_alignment_observation = claim(
    "**Semantic alignment improves with recursion depth (Fig. 7).** "
    "Under the scaled Sequential-Style RecursiveMAS, the authors "
    "sample 500 question-answer pairs spanning all downstream "
    "domains, embed both the ground-truth answers and the system's "
    "generated answers via the Solver agent's input embedding "
    "layer, and visualize them via PCA projection. At $r = 1$ the "
    "generated distribution is visibly *shifted* from the ground-"
    "truth distribution; at $r = 2$ the discrepancy narrows; by "
    "$r = 3$ the two distributions are largely aligned.",
    title="Result: Fig. 7 -- generated/answer distributions become aligned with ground-truth as r grows",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 7",
        "caption": "Fig. 7: Semantic representations of RecursiveMAS across r=1/2/3 (PCA projection over 500 QA pairs).",
    },
)

claim_iterative_correction_pattern = claim(
    "**Common pattern: incorrect-at-$r=1$ corrected by deeper "
    "recursion.** Detailed case studies (Appendix F, on MATH500 "
    "question '$2^{24}$ as a perfect $n$-th power, $n > 1$') show "
    "RecursiveMAS producing an incorrect answer (6) at $r = 1$, "
    "then correcting to the right answer (7) at $r = 2$ and "
    "consolidating the correct chain of reasoning at $r = 3$. The "
    "pattern is consistent with the Fig. 7 alignment trend: deeper "
    "recursion brings the latent answer closer to the ground-truth "
    "embedding region.",
    title="Result: case study -- incorrect r=1 answer is corrected by r=2/3 recursion",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Appendix F (case study)",
    },
)

# ---------------------------------------------------------------------------
# Section 6 (Table 9, Figure 8): optimal latent-thoughts length m
# ---------------------------------------------------------------------------

claim_table9_latent_length = claim(
    "**Table 9 / Fig. 8: Ablation on the latent-thoughts length $m$** "
    "(accuracy %, scaled Sequential-Style RecursiveMAS).\n\n"
    "| Latent steps $m$ | 0 | 16 | 32 | 48 | 64 | 80 | 96 | 112 | "
    "128 |\n"
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n"
    "| MATH500 | 83.3 | 84.9 | 85.2 | 85.6 | 86.8 | 86.8 | 86.5 | "
    "86.9 | 86.7 |\n"
    "| GPQA-D | 61.4 | 62.0 | 62.8 | 63.6 | 64.1 | 64.2 | 64.5 | "
    "64.3 | 64.4 |\n"
    "| LiveCodeBench | 38.1 | 40.3 | 40.7 | 41.4 | 42.0 | 42.5 | "
    "42.2 | 42.6 | 42.6 |\n",
    title="Table 9: latent-thoughts length sweep m in {0, 16, 32, ..., 128}",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 9 + Fig. 8",
    },
)

claim_optimal_m_around_80 = claim(
    "**Optimal latent-thoughts length saturates around $m \\approx 80$.** "
    "Across MATH500, GPQA-D, and LiveCodeBench, accuracy increases "
    "monotonically over the early regime (low $m$) and then "
    "**stabilizes once $m$ reaches a moderate scale ($m \\approx 80$)**. "
    "Going from $m = 0$ to $m = 80$ adds +3.5 pp on MATH500 (83.3 -> "
    "86.8), +2.8 pp on GPQA-D (61.4 -> 64.2), and +4.4 pp on "
    "LiveCodeBench (38.1 -> 42.5); pushing $m$ further to 128 adds "
    "essentially nothing. RecursiveMAS therefore enables effective "
    "agent reasoning and interaction with only a *modest latent-"
    "thought budget*, in contrast to text-based collaboration that "
    "typically requires longer chain-of-thought and costly token "
    "generation.",
    title="Result: accuracy saturates at m ~ 80 -- modest latent budget suffices",
)

# ---------------------------------------------------------------------------
# Section 6: training cost (Table 5)
# ---------------------------------------------------------------------------

claim_table5_training_cost = claim(
    "**Table 5: Training-cost analysis** (scaled Sequential-Style "
    "MAS setting). Compares RecursiveMAS with direct training "
    "alternatives under matched training data and backbones; "
    "**peak GPU memory** in GB, **trainable parameters** as count "
    "and percentage of full-model parameters, **estimated cost** "
    "in USD (per @Liu et al. 2025; Lu et al. 2023 GPU-usage "
    "convention), and **average accuracy** across all downstream "
    "tasks.\n\n"
    "| Method | GPU Mem. (GB) | Trainable Params | Cost (USD) | "
    "Avg. Acc. (%) |\n"
    "|---|---:|---:|---:|---:|\n"
    "| LoRA Training | 21.67 | 15.92M (0.37%) | $6.64 | 66.9 |\n"
    "| Full-SFT | 41.40 | 4.21B (100%) | $9.67 | 68.6 |\n"
    "| **RecursiveMAS** | **15.29** | **13.12M (0.31%)** | "
    "**$4.27** | **74.9** |\n",
    title="Table 5: training cost -- RecursiveMAS lowest GPU mem / params / cost AND highest avg accuracy",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 5",
    },
)

claim_cost_performance_dominance = claim(
    "**RecursiveMAS dominates LoRA and Full-SFT on cost-vs-accuracy.** "
    "RecursiveMAS uses only 13.12M (0.31%) trainable parameters "
    "(vs LoRA's 15.92M / 0.37% and Full-SFT's 4.21B / 100%), the "
    "lowest peak GPU memory (15.29 vs 21.67 vs 41.40 GB), the "
    "lowest training cost ($4.27 vs $6.64 vs $9.67 USD), *and* the "
    "highest average downstream accuracy (74.9% vs 66.9% vs 68.6%). "
    "RecursiveMAS is therefore Pareto-dominant on cost-vs-"
    "performance among the three.",
    title="Result: RecursiveMAS Pareto-dominates LoRA + Full-SFT on cost-vs-accuracy",
)

__all__ = [
    "claim_table4_link_designs",
    "claim_residual_value",
    "claim_two_layer_value",
    "claim_semantic_alignment_observation",
    "claim_iterative_correction_pattern",
    "claim_table9_latent_length",
    "claim_optimal_m_around_80",
    "claim_table5_training_cost",
    "claim_cost_performance_dominance",
]
