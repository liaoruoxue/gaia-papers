"""Section 4.2-4.4: Main empirical results.

Sections 4.2 (Unified + Hybrid), 4.3 (case study), and 4.4 (token usage and
coverage trends) of [@Wu2026ContextWeaver]. All numbers transcribed
verbatim from Table 1, Table 2, and Figure 2/3.

Atomicity: per-(model, benchmark) pass@1 results are extracted as separate
claims; per-benchmark efficiency claims (steps, tokens) are separated from
quality claims (pass@1).
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Table 1: full performance comparison across settings
# ---------------------------------------------------------------------------

claim_table1_full = claim(
    "**Table 1: Performance comparison across settings (pass@1, %).** "
    "Sliding Window results report pass@1 with window size 5. Rows "
    "use the Unified setting (same model for agent and memory) "
    "unless noted as Hybrid.\n\n"
    "| Model | Method | Verified | Lite |\n"
    "|-------|--------|---------:|-----:|\n"
    "| Claude Sonnet 4 | **ContextWeaver** | **66.0** | **53.7** |\n"
    "| Claude Sonnet 4 | Sliding Window | 63.2 | 52.3 |\n"
    "| Claude Sonnet 4 | LLM Summarization | 64.2 | 53.0 |\n"
    "| GPT-5 | ContextWeaver | 56.8 | 42.0 |\n"
    "| GPT-5 | ContextWeaver -- Hybrid | **58.6** | **51.3** |\n"
    "| GPT-5 | Sliding Window | 57.4 | 48.3 |\n"
    "| GPT-5 | LLM Summarization | 46.7 | 32.3 |\n"
    "| Gemini 3 Flash | ContextWeaver | 58.4 | **47.0** |\n"
    "| Gemini 3 Flash | Sliding Window | **60.4** | 46.0 |\n"
    "| Gemini 3 Flash | LLM Summarization | 56.8 | 43.3 |\n\n"
    "Headline: Claude Sonnet 4 (Unified) and GPT-5 (Hybrid) show "
    "consistent ContextWeaver gains over Sliding Window on both "
    "Verified and Lite [@Wu2026ContextWeaver, Table 1].",
    title="Table 1: full pass@1 results across 3 LLMs x {CW, SW, Summarization} x {Verified, Lite}",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Table 1",
        "caption": "Table 1: Performance Comparison Across Settings.",
    },
)

# ---------------------------------------------------------------------------
# Per-(model, benchmark) atomic claims for the headline pattern
# ---------------------------------------------------------------------------

claim_claude_unified_verified = claim(
    "**Claude Sonnet 4 / Unified / Verified: ContextWeaver = 66.0% vs. "
    "Sliding Window = 63.2% (+2.8 pp).** ContextWeaver improves "
    "pass@1 by 2.8 percentage points over the sliding-window baseline "
    "on SWE-Bench Verified when Claude Sonnet 4 manages both task and "
    "memory [@Wu2026ContextWeaver, Sec. 4.2 Unified, Table 1].",
    title="Claude/Unified/Verified: 66.0 vs 63.2 (+2.8 pp for CW)",
)

claim_claude_unified_lite = claim(
    "**Claude Sonnet 4 / Unified / Lite: ContextWeaver = 53.7% vs. "
    "Sliding Window = 52.3% (+1.4 pp).** Same direction on Lite split "
    "for Claude Sonnet 4, with a smaller margin "
    "[@Wu2026ContextWeaver, Sec. 4.2 Unified, Table 1].",
    title="Claude/Unified/Lite: 53.7 vs 52.3 (+1.4 pp for CW)",
)

claim_gpt5_hybrid_verified = claim(
    "**GPT-5 / Hybrid / Verified: ContextWeaver = 58.6% vs. Sliding "
    "Window = 57.4% (+1.2 pp).** When the dependency graph is "
    "constructed by the stronger Claude Sonnet 4 and the task is "
    "executed by GPT-5, ContextWeaver outperforms the sliding-window "
    "baseline on SWE-Bench Verified "
    "[@Wu2026ContextWeaver, Sec. 4.2 Hybrid, Table 1].",
    title="GPT-5/Hybrid/Verified: 58.6 vs 57.4 (+1.2 pp for CW)",
)

claim_gpt5_hybrid_lite = claim(
    "**GPT-5 / Hybrid / Lite: ContextWeaver = 51.3% vs. Sliding Window "
    "= 48.3% (+3.0 pp).** Largest hybrid-setting gain occurs on Lite "
    "[@Wu2026ContextWeaver, Sec. 4.2 Hybrid, Table 1].",
    title="GPT-5/Hybrid/Lite: 51.3 vs 48.3 (+3.0 pp for CW)",
)

claim_gpt5_unified_underperforms = claim(
    "**GPT-5 / Unified shows that GPT-5 cannot effectively *construct* "
    "its own dependency graph: Verified 56.8 vs SW 57.4 (-0.6 pp); "
    "Lite 42.0 vs SW 48.3 (-6.3 pp).** When GPT-5 manages its own "
    "memory, ContextWeaver underperforms the sliding window. The gain "
    "appears only in the Hybrid setting where Claude builds the graph. "
    "This is direct evidence that the *quality of dependency-graph "
    "construction* drives ContextWeaver's effectiveness "
    "[@Wu2026ContextWeaver, Sec. 4.2, Table 1].",
    title="GPT-5/Unified underperforms SW => graph-construction quality matters",
)

claim_gemini_unified_lite_gain = claim(
    "**Gemini 3 Flash / Unified / Lite: ContextWeaver = 47.0% vs. "
    "Sliding Window = 46.0% (+1.0 pp).** Gemini 3 Flash benefits from "
    "ContextWeaver on the Lite split "
    "[@Wu2026ContextWeaver, Sec. 4.2 Unified, Table 1].",
    title="Gemini/Unified/Lite: 47.0 vs 46.0 (+1.0 pp for CW)",
)

claim_gemini_unified_verified_loss = claim(
    "**Gemini 3 Flash / Unified / Verified: ContextWeaver = 58.4% vs. "
    "Sliding Window = 60.4% (-2.0 pp).** On Verified with Gemini 3 "
    "Flash, ContextWeaver underperforms the sliding window. Combined "
    "with the GPT-5 Unified-setting result, this demonstrates that "
    "ContextWeaver's gains depend on the backbone LLM's ability to "
    "construct high-quality dependency graphs "
    "[@Wu2026ContextWeaver, Sec. 4.2, Table 1].",
    title="Gemini/Unified/Verified: 58.4 vs 60.4 (-2.0 pp); CW depends on graph quality",
)

# ---------------------------------------------------------------------------
# Summarization baseline pattern
# ---------------------------------------------------------------------------

claim_summarization_uneven = claim(
    "**LLM Summarization is uneven: helps Claude (+1.0/+0.7 pp), "
    "hurts Gemini and GPT-5.** With Claude Sonnet 4, summarization "
    "improves over sliding window (Verified 64.2 vs 63.2; Lite 53.0 "
    "vs 52.3). With Gemini 3 Flash and GPT-5 it hurts: GPT-5 "
    "summarization on Verified is 46.7 (vs SW 57.4) and Lite 32.3 "
    "(vs SW 48.3); Gemini summarization on Verified is 56.8 (vs SW "
    "60.4) and Lite 43.3 (vs SW 46.0). The paper attributes this to "
    "weaker models producing summaries that omit details (specific "
    "error messages, file paths) needed in later steps "
    "[@Wu2026ContextWeaver, Sec. 4.2 LLM Summarization Results, Table 1].",
    title="Summarization is conditional on backbone strength: helps Claude, hurts Gemini & GPT-5",
)

claim_cw_avoids_summarization_pitfall = claim(
    "**ContextWeaver avoids the summarization pitfall by keeping raw "
    "observations and selecting which to retain via the dependency "
    "graph.** Rather than asking the model to compress its own history "
    "into prose, ContextWeaver keeps observations verbatim for "
    "ancestors and only collapses observations of non-ancestors. This "
    "preserves details that summarization-based methods may "
    "incorrectly drop [@Wu2026ContextWeaver, Sec. 4.2].",
    title="CW design advantage: keeps raw obs + dependency-based selection (no model-side prose compression)",
)

# ---------------------------------------------------------------------------
# Section 4.3: Case-study qualitative findings
# ---------------------------------------------------------------------------

claim_case_django_14631 = claim(
    "**Case `django django-14631` (multi-component task): "
    "ContextWeaver wins 4/5 vs. Sliding Window 1/5.** The fix requires "
    "coordinated updates across four code locations in two files: "
    "`forms.py` (clean_fields, changed_data) and `boundfield.py` "
    "(initial, value). ContextWeaver consistently succeeds (e.g., 71 "
    "steps to success) by preserving long-range dependencies between "
    "early architectural analysis (`boundfield.py`) and later "
    "implementation steps (`forms.py`). Sliding Window frequently "
    "loses this structural context (e.g., 83 steps with repeated "
    "re-reading at steps 4-5, 26-27, 33, 44, 47, and incompatible "
    "partial fixes at steps 51, 74, 77, 81), resulting in repeated "
    "code discovery and incompatible partial fixes "
    "[@Wu2026ContextWeaver, Sec. 4.3, Appendix C.1].",
    title="Case django-14631 (multi-file): CW 4/5 vs SW 1/5; CW preserves long-range cross-file deps",
    metadata={"figure": "artifacts/2604.23069.pdf, Sec. 4.3 + Appendix C.1"},
)

claim_case_pytest_7205 = claim(
    "**Case `pytest-dev pytest-7205` (single-location task): Sliding "
    "Window wins 4/5 vs. ContextWeaver 1/5.** The task involves a "
    "single-file, single-location change (replacing an implicit "
    "`str()` call with `saferepr()` in `setuponly.py`). Sliding "
    "Window converges in 27 linear steps. ContextWeaver introduces "
    "unnecessary branching (59 steps with apply-revert cycles at "
    "steps 15, 20, 34, 36, 41, 43) that dilutes focus in strictly "
    "linear debugging trajectories "
    "[@Wu2026ContextWeaver, Sec. 4.3, Appendix C.1].",
    title="Case pytest-7205 (single-loc): SW 4/5 vs CW 1/5; CW branching adds overhead",
    metadata={"figure": "artifacts/2604.23069.pdf, Sec. 4.3 + Appendix C.1"},
)

claim_case_takeaway = claim(
    "**Takeaway: dependency-aware memory is most beneficial for "
    "tasks requiring distant cross-step relationships; recency-based "
    "selection is a stronger inductive bias for strictly sequential "
    "tasks.** The paired case studies establish a precise scope "
    "claim: ContextWeaver's gains concentrate where multi-file or "
    "multi-component dependencies span the trajectory; for purely "
    "sequential local fixes, sliding-window's recency bias matches "
    "the task structure better "
    "[@Wu2026ContextWeaver, Sec. 4.3].",
    title="Scope claim: CW wins on multi-component long-range tasks; SW wins on linear local tasks",
)

# ---------------------------------------------------------------------------
# Section 4.4: Token efficiency and iteration scaling
# ---------------------------------------------------------------------------

claim_iteration_budget_scaling = claim(
    "**Figure 2a: ContextWeaver outperforms Sliding Window across "
    "iteration budgets, with the clearest gains at moderate budgets.** "
    "On both SWE-Bench Verified and Lite, resolve rate as a function "
    "of maximum allowed iterations is consistently higher for "
    "ContextWeaver. The largest gains appear at moderate budgets "
    "(e.g., 60 iterations) where agents often fail due to drift "
    "rather than insufficient capacity. The gap persists as the "
    "budget increases, indicating the improvement is not tied to a "
    "single budget setting [@Wu2026ContextWeaver, Sec. 4.4, "
    "Fig. 2a].",
    title="Fig. 2a: CW beats SW across iteration budgets (largest at moderate, ~60 iters)",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Fig. 2a",
        "caption": "Performance scaling with iteration budget (Claude Sonnet 4).",
    },
)

claim_token_per_instance_parity = claim(
    "**Per-instance tokens are essentially the same as Sliding "
    "Window.** Per-instance token usage is comparable between "
    "ContextWeaver and Sliding Window on both Verified and Lite. This "
    "rules out a trivial explanation in which higher solve rates come "
    "from simply using more tokens per run "
    "[@Wu2026ContextWeaver, Sec. 4.4, Fig. 2b].",
    title="Token efficiency: per-instance tokens roughly equal CW vs. SW",
    metadata={"figure": "artifacts/2604.23069.pdf, Fig. 2b"},
)

claim_tokens_per_resolve_savings = claim(
    "**ContextWeaver achieves 2.8% agent-side token savings on "
    "Verified and 2.3% on Lite, measured per successful resolve.** "
    "Although per-instance tokens are roughly equal, ContextWeaver "
    "*reduces tokens-per-resolve* because more instances are "
    "successfully solved. A fixed token budget therefore produces "
    "more successful fixes [@Wu2026ContextWeaver, Sec. 4.4, "
    "Fig. 2b].",
    title="Tokens-per-resolve savings: -2.8% Verified, -2.3% Lite",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Fig. 2b",
        "caption": "Agent-side tokens per successful resolve.",
    },
)

claim_iteration_savings_appendix_f = claim(
    "**Average iteration savings (Figure 3): -4.7% on Verified, -7.3% "
    "on Lite.** ContextWeaver requires 4.7% fewer iterations on SWE-"
    "Bench Verified and 7.3% fewer on Lite compared to Sliding "
    "Window, in the Claude Sonnet 4 setting. The reduction holds for "
    "both successful resolves and the average over all instances, "
    "indicating improvements are not driven by early exits on easy "
    "instances alone [@Wu2026ContextWeaver, Appendix F, Fig. 3].",
    title="Iterations: -4.7% Verified, -7.3% Lite (averaged over all + over resolves)",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Fig. 3",
        "caption": "Average iterations to resolve, Claude Sonnet 4.",
    },
)

claim_iteration_distribution_tail = claim(
    "**Figure 4: ContextWeaver shifts the iteration-to-resolve curve "
    "downward at every percentile, with the largest gains in the "
    "upper tail.** Across both benchmarks, the gain is most "
    "pronounced on Lite, where difficult instances require "
    "substantially fewer iterations. This pattern indicates that "
    "dependency-aware context selection primarily improves robustness "
    "on hard cases rather than only accelerating already-easy ones "
    "[@Wu2026ContextWeaver, Appendix F, Fig. 4].",
    title="Fig. 4: CW shifts iteration percentile curve down; largest gains in upper tail",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Fig. 4",
        "caption": "Iterations needed to resolve by percentile.",
    },
)

# ---------------------------------------------------------------------------
# Variance / stability subset (Table 2)
# ---------------------------------------------------------------------------

claim_table2_subset_variance = claim(
    "**Table 2: 100-instance Verified subset, 5 runs (Claude Sonnet 4).**\n\n"
    "| Method | Pass@1 (%) | Pass@5 (%) | Avg Steps | "
    "% Instances Fewer Steps |\n"
    "|--------|-----------:|-----------:|----------:|------------------------:|\n"
    "| **ContextWeaver** | **68.0$\\pm$1.55** | **81.0** | **55.8** | **73%** |\n"
    "| Sliding Window | 67.2$\\pm$1.94 | 78.0 | 59.2 | 27% |\n\n"
    "ContextWeaver achieves higher mean Pass@1 (68.0 vs 67.2), "
    "higher Pass@5 (81.0 vs 78.0), fewer average steps (55.8 vs "
    "59.2), and uses fewer steps in 73% of instances "
    "[@Wu2026ContextWeaver, Sec. 4.6, Table 2].",
    title="Table 2 (100-inst Verified, 5 runs): CW 68.0 vs SW 67.2; 73% fewer steps; std 1.55 vs 1.94",
    metadata={
        "figure": "artifacts/2604.23069.pdf, Table 2",
        "caption": "Aggregate performance on 100-instance subset of SWE-Bench Verified.",
    },
)

claim_lower_variance = claim(
    "**ContextWeaver has lower run-to-run standard deviation: 1.55 vs "
    "1.94.** On the 100-instance Verified subset (5 runs, Claude "
    "Sonnet 4), ContextWeaver's standard deviation in Pass@1 is 1.55 "
    "compared to 1.94 for Sliding Window, indicating more consistent "
    "behavior across runs and improved robustness to sampling noise. "
    "Stability matters in agentic settings where small early "
    "deviations can compound over long trajectories "
    "[@Wu2026ContextWeaver, Sec. 4.6, Table 2].",
    title="Variance reduction: std 1.55 (CW) vs 1.94 (SW)",
)

# ---------------------------------------------------------------------------
# Qualitative error analysis (Appendix E.1)
# ---------------------------------------------------------------------------

claim_qualitative_38_vs_27 = claim(
    "**Appendix E.1 qualitative analysis: ContextWeaver solves "
    "330/500 vs. Sliding Window 316/500; CW uniquely solves 38, SW "
    "uniquely solves 27, and 143 are unsolved by either.** Using "
    "gold patches on SWE-Bench Verified, ContextWeaver and the "
    "sliding-window baseline have complementary unique-success sets. "
    "The 143 commonly unsolved instances indicate that many cases "
    "require advances beyond memory selection alone "
    "[@Wu2026ContextWeaver, Appendix E.1].",
    title="Appendix E.1: CW 330/500 vs SW 316/500; CW uniquely solves 38, SW 27, 143 unsolved by both",
)

claim_qualitative_recency_bias = claim(
    "**Where ContextWeaver helps: cases where early structural signals "
    "are informative.** Among the 38 instances solved only by "
    "ContextWeaver, the sliding-window baseline frequently shows "
    "recency bias and edits incorrect files. ContextWeaver preserves "
    "and reuses structurally relevant signals from earlier steps "
    "(e.g., for `sphinx-doc sphinx-7440`, ContextWeaver consistently "
    "retains evidence pointing to `sphinx/domains/std.py`, while the "
    "sliding window keeps only the most recent edited file) "
    "[@Wu2026ContextWeaver, Appendix E.1].",
    title="Where CW helps: early structural signals; SW recency-biases to wrong files",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "claim_table1_full",
    "claim_claude_unified_verified",
    "claim_claude_unified_lite",
    "claim_gpt5_hybrid_verified",
    "claim_gpt5_hybrid_lite",
    "claim_gpt5_unified_underperforms",
    "claim_gemini_unified_lite_gain",
    "claim_gemini_unified_verified_loss",
    "claim_summarization_uneven",
    "claim_cw_avoids_summarization_pitfall",
    "claim_case_django_14631",
    "claim_case_pytest_7205",
    "claim_case_takeaway",
    "claim_iteration_budget_scaling",
    "claim_token_per_instance_parity",
    "claim_tokens_per_resolve_savings",
    "claim_iteration_savings_appendix_f",
    "claim_iteration_distribution_tail",
    "claim_table2_subset_variance",
    "claim_lower_variance",
    "claim_qualitative_38_vs_27",
    "claim_qualitative_recency_bias",
]
