"""Section 4.5-4.6: Mechanism validation -- ablations and robustness.

Section 4.5 (Graph vs. Tree topology), Section 4.6 (window-size sensitivity
+ stability), Appendix F.1 (GPT-4o sanity check) of [@Wu2026ContextWeaver].
Numbers transcribed from Tables 3a, 3b, and 4a.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Section 4.5: DAG vs. Tree topology
# ---------------------------------------------------------------------------

claim_table3a_dag_vs_tree = claim(
    "**Table 3a: DAG vs. Tree topology on 100-instance Verified subset, "
    "5 runs (Claude Sonnet 4).**\n\n"
    "| Method | R1 | R2 | R3 | R4 | R5 | Mean$\\pm$Std |\n"
    "|--------|---:|---:|---:|---:|---:|-----------:|\n"
    "| **ContextWeaver (DAG)** | 71 | 67 | 67 | 68 | 67 | **68.0$\\pm$1.55** |\n"
    "| Tree base (1 parent) | 70 | 65 | 63 | 68 | 69 | 67.0$\\pm$2.92 |\n\n"
    "Restricting the parent selector to a single predecessor per node "
    "yields the tree variant. Means are close (68.0 vs 67.0), but the "
    "DAG variant has substantially lower run-to-run variance "
    "(1.55 vs 2.92) [@Wu2026ContextWeaver, Sec. 4.5, Table 3a].",
    title="Table 3a: DAG 68.0+/-1.55 vs Tree 67.0+/-2.92 on 100-inst Verified",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Table 3a",
        "caption": "DAG vs. Tree comparison.",
    },
)

claim_dag_chosen_for_stability = claim(
    "**DAG configuration is chosen for the main experiments because of "
    "stability, not mean.** The mean Pass@1 difference between DAG "
    "(68.0%) and Tree (67.0%) is small, but the DAG configuration "
    "consistently yields lower run-to-run variance (1.55 vs 2.92). "
    "Accordingly, all main experiments use the DAG-based formulation. "
    "This also addresses the design question of whether multi-parent "
    "support is necessary -- the answer is *yes for stability* "
    "[@Wu2026ContextWeaver, Sec. 4.5].",
    title="Design choice: DAG over Tree for stability (variance), not mean",
)

# ---------------------------------------------------------------------------
# Section 4.6: Window size sensitivity (Table 3b)
# ---------------------------------------------------------------------------

claim_table3b_window_size = claim(
    "**Table 3b: window-size sensitivity, $k \\in \\{5, 7, 9\\}$, "
    "5 runs on 100-instance Verified subset.**\n\n"
    "| Window Size $k$ | R1 | R2 | R3 | R4 | R5 | Mean$\\pm$Std |\n"
    "|----------------:|---:|---:|---:|---:|---:|-----------:|\n"
    "| 5 | 71 | 67 | 67 | 68 | 67 | **68.0$\\pm$1.55** |\n"
    "| 7 | 64 | 70 | 67 | 66 | 63 | 66.0$\\pm$2.45 |\n"
    "| 9 | 69 | 63 | 68 | 68 | 69 | 67.4$\\pm$2.25 |\n\n"
    "Pass@1 is similar across window sizes; performance varies "
    "slightly across runs but no strong sensitivity is observed in "
    "this range [@Wu2026ContextWeaver, Sec. 4.6, Table 3b].",
    title="Table 3b: window size {5,7,9} -> 68.0/66.0/67.4 (no strong sensitivity)",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Table 3b",
        "caption": "Window-size sensitivity study.",
    },
)

claim_window_insensitive = claim(
    "**ContextWeaver is robust to the choice of window size $W$ in "
    "$\\{5, 7, 9\\}$.** Pass@1 results over five runs on the 100-"
    "instance Verified subset are similar across window sizes "
    "(68.0%, 66.0%, 67.4%), with no strong sensitivity. This "
    "indicates the dependency-aware selection mechanism does not "
    "rely on a finely-tuned window size in this range "
    "[@Wu2026ContextWeaver, Sec. 4.6].",
    title="Robustness: not strongly sensitive to W in {5, 7, 9}",
)

# ---------------------------------------------------------------------------
# Appendix F.1: GPT-4o sanity check (Table 4a)
# ---------------------------------------------------------------------------

claim_table4a_gpt4o_sanity_check = claim(
    "**Appendix F.1 / Table 4a: GPT-4o sanity check on 100-instance "
    "Verified subset, 5 runs.**\n\n"
    "| Method | R1 | R2 | R3 | R4 | R5 | Mean$\\pm$Std |\n"
    "|--------|---:|---:|---:|---:|---:|-----------:|\n"
    "| Sliding Window | 25 | 28 | 23 | 25 | 32 | 26.6$\\pm$3.50 |\n"
    "| **ContextWeaver** | 29 | 33 | 27 | 28 | 26 | **28.6$\\pm$2.70** |\n\n"
    "Numbers are absolute resolve counts (not percentages). "
    "ContextWeaver achieves a higher mean (28.6 vs 26.6) and lower "
    "variance (2.70 vs 3.50). Due to cost constraints this is "
    "described as a sanity check rather than a full re-evaluation, "
    "but the aggregate results align with main experiments "
    "[@Wu2026ContextWeaver, Appendix F.1, Table 4a].",
    title="Table 4a (GPT-4o, 100-inst Verified): CW 28.6+/-2.70 vs SW 26.6+/-3.50",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Table 4a",
        "caption": "GPT-4o exploratory comparison.",
    },
)

claim_gpt4o_generalization = claim(
    "**The GPT-4o sanity check supports cross-model generalization of "
    "the ContextWeaver advantage.** ContextWeaver continues to provide "
    "consistent gains and lower variance under a different base model "
    "(GPT-4o) on 100 Verified instances, suggesting that the benefits "
    "of structured context selection are not tied to a specific "
    "backbone LLM and can extend to other underlying models "
    "[@Wu2026ContextWeaver, Appendix F.1].",
    title="GPT-4o generalization sanity check: CW advantage extends beyond Claude/GPT-5/Gemini",
)

# ---------------------------------------------------------------------------
# Cross-ablation summary
# ---------------------------------------------------------------------------

claim_ablation_components_summary = claim(
    "**Mechanism evidence is distributed across multiple ablations:** "
    "(i) DAG vs Tree topology (Sec 4.5) shows multi-parent support "
    "matters for *stability*; (ii) Window-size study (Sec 4.6) shows "
    "robustness to $W$; (iii) Variance subset (Table 2) confirms "
    "lower run-to-run noise; (iv) GPT-4o sanity check (App F.1) "
    "supports cross-model generalization. The paper does not report "
    "a complete drop-each-component ablation (validation, "
    "summarizer), so the empirical evidence for each individual "
    "component's marginal contribution is partial -- it is "
    "*architectural* (each component has a clear functional role "
    "described in Sec 3) rather than fully ablation-isolated "
    "[@Wu2026ContextWeaver, Sec. 4.5-4.6, Appendix F.1].",
    title="Ablation summary: DAG vs Tree, window size, variance, cross-model -- but no per-component drop",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "claim_table3a_dag_vs_tree",
    "claim_dag_chosen_for_stability",
    "claim_table3b_window_size",
    "claim_window_insensitive",
    "claim_table4a_gpt4o_sanity_check",
    "claim_gpt4o_generalization",
    "claim_ablation_components_summary",
]
