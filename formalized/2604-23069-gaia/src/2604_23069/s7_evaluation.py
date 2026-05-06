"""Section 4.1: Experiment Setup.

Section 4.1 of [@Wu2026ContextWeaver]. Captures the benchmarks (SWE-Bench
Verified + Lite), backbone LLMs (Claude Sonnet 4, GPT-5, Gemini 3 Flash),
agent framework (SWE-Agent), baselines (sliding-window, LLM-summarization),
fixed shared configuration ($W = 5$, DAG, no instance-specific tuning),
and metrics (resolve rate / pass@1, LLM token usage).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Benchmarks
# ---------------------------------------------------------------------------

setup_swe_bench = setting(
    "**SWE-Bench evaluation harness [@Jimenez2023SWEBench].** SWE-Bench "
    "is a benchmark in which an agent resolves real GitHub issues by "
    "editing codebases. Each instance pairs a problem statement with a "
    "ground-truth patch and a test suite; performance is measured by "
    "the fraction of instances where the agent's edits cause the "
    "test suite to pass [@Wu2026ContextWeaver, Sec. 4.1].",
    title="Setup: SWE-Bench = LLM-agent edits real GitHub repos to make test suites pass",
)

setup_swe_subsets = setting(
    "**Two standard SWE-Bench subsets used: Verified and Lite.** "
    "ContextWeaver is evaluated on (i) **SWE-Bench Verified** "
    "[@Chowdhury2024SWEVerified] -- a human-verified high-quality "
    "subset; and (ii) **SWE-Bench Lite** -- a smaller subset commonly "
    "used for cost-efficient evaluation. Variance is additionally "
    "reported across 5 runs on a randomized 100-instance subset "
    "[@Wu2026ContextWeaver, Sec. 4.1, Appendix E].",
    title="Setup: evaluation on SWE-Bench Verified + Lite + 100-instance variance subset",
)

# ---------------------------------------------------------------------------
# Models and agent framework
# ---------------------------------------------------------------------------

setup_three_llms = setting(
    "**Three backbone LLMs evaluated.** Primary experiments use three "
    "LLMs commonly used for coding tasks: **Claude Sonnet 4**, "
    "**GPT-5**, and **Gemini 3 Flash**. All agents use the same agent "
    "framework with identical tools, prompts, and execution settings "
    "across conditions [@Wu2026ContextWeaver, Sec. 4.1].",
    title="Setup: three LLMs -- Claude Sonnet 4, GPT-5, Gemini 3 Flash",
)

setup_swe_agent_framework = setting(
    "**SWE-Agent framework [@Yang2024SWEAgent] used as the agent "
    "harness.** All conditions run inside SWE-Agent, with identical "
    "tools (registry, edit_anthropic, review_on_submit_m, diff_state, "
    "bash) and prompt templates (Appendix B.1); only the context-"
    "management module varies across conditions "
    "[@Wu2026ContextWeaver, Sec. 4.1, Appendix B.1].",
    title="Setup: SWE-Agent harness with identical tools/prompts; only memory module varies",
)

# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

setup_sliding_window_baseline = setting(
    "**Primary baseline: sliding-window with $n = 5$ recent action-"
    "observation pairs.** The fixed-window baseline keeps only the "
    "most recent $n = 5$ action and observation pairs and discards "
    "earlier ones. The window size $n$ is varied in Section 4.6 "
    "(values $\\{5, 7, 9\\}$). The choice of sliding window is motivated "
    "by its widespread use in prior work on tool-using agents and its "
    "natural fit with the experimental setup "
    "[@Wu2026ContextWeaver, Sec. 4.1, Sec. 4.6].",
    title="Baseline: sliding window with n=5 recent A-O pairs (also studied at n in {5,7,9})",
)

setup_baseline_compression_parity = setting(
    "**Sliding-window baseline uses the *same* observation-compression "
    "strategy as ContextWeaver.** To ensure a fair comparison, the "
    "sliding-window baseline applies the same lightweight observation "
    "placeholder ('(N lines omitted) (M images omitted)') to history "
    "entries outside its window. This isolates the effect of "
    "*selection mechanism* (recency vs. dependency-based) from "
    "differences in compression "
    "[@Wu2026ContextWeaver, Sec. 4.1, Appendix D].",
    title="Setup: sliding window uses CW's compression scheme -> isolates selection mechanism",
)

setup_summarization_baseline = setting(
    "**Secondary baseline: LLM summarization inspired by SWE-Agent / "
    "OpenHands condensers.** As an additional baseline, an LLM-"
    "summarization variant periodically condenses older history into "
    "an LLM-generated summary while retaining the 5 most recent "
    "observation pairs intact. The same backbone model performs both "
    "the task and the summarization. All other settings are identical "
    "to the sliding-window baseline "
    "[@Wu2026ContextWeaver, Sec. 4.1, Appendix F.3].",
    title="Baseline: LLM summarization condenses old history; same model as agent",
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

setup_shared_configuration = setting(
    "**Single shared configuration across all experiments.** "
    "$W = 5$ matching the sliding-window window size; nodes form a "
    "DAG (a tree variant is studied separately in Section 4.5); all "
    "parameters fixed across benchmarks, models, and runs; no "
    "instance-specific tuning is performed "
    "[@Wu2026ContextWeaver, Sec. 4.1, Appendix F.2].",
    title="Setup: W=5, DAG, fixed across all benchmarks/models, no instance-specific tuning",
)

# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

setup_metrics = setting(
    "**Metrics: resolve rate (test-suite pass rate) and LLM token "
    "usage.** Following the SWE-Bench protocol [@Jimenez2023SWEBench], "
    "the paper reports *resolve rate* (the fraction of instances where "
    "the test suite passes after the agent's edits, equivalent to "
    "pass@1) and measures *efficiency* in terms of LLM token usage "
    "(agent-side counts from trajectory model statistics) "
    "[@Wu2026ContextWeaver, Sec. 4.1].",
    title="Metrics: resolve rate (= pass@1) and agent-side LLM token usage",
)

# ---------------------------------------------------------------------------
# Two evaluation regimes
# ---------------------------------------------------------------------------

claim_unified_vs_hybrid_regimes = claim(
    "**Two evaluation regimes: Unified and Hybrid.** Because the "
    "memory module can run independently of the acting agent, the "
    "paper reports two settings. **Unified**: the same model performs "
    "*both* the task and manages its memory. **Hybrid**: memory "
    "construction is decoupled from task execution -- the paper uses "
    "Claude Sonnet 4 to construct the structured memory and GPT-5 to "
    "perform the task. The Hybrid setting tests whether context "
    "constructed by a more capable model improves downstream "
    "performance with a different (and possibly weaker on memory "
    "construction) executor [@Wu2026ContextWeaver, Sec. 4.2].",
    title="Two regimes: Unified (same LLM for memory + task) vs. Hybrid (Claude memory, GPT-5 task)",
)

# ---------------------------------------------------------------------------
# Variance protocol
# ---------------------------------------------------------------------------

claim_variance_protocol = claim(
    "**Variance is reported as mean$\\pm$std across 5 independent runs "
    "on a 100-instance random subset of SWE-Bench Verified.** Because "
    "LLM agents exhibit substantial run-to-run variance from "
    "stochastic generation and long-horizon dependencies, stability is "
    "assessed via 5 independent runs over a randomized 100-instance "
    "subset of SWE-Bench Verified using Claude Sonnet 4 "
    "[@Wu2026ContextWeaver, Sec. 4.1, Sec. 4.6, Appendix E].",
    title="Variance protocol: 5 runs x 100-instance random subset, Claude Sonnet 4",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "setup_swe_bench",
    "setup_swe_subsets",
    "setup_three_llms",
    "setup_swe_agent_framework",
    "setup_sliding_window_baseline",
    "setup_baseline_compression_parity",
    "setup_summarization_baseline",
    "setup_shared_configuration",
    "setup_metrics",
    "claim_unified_vs_hybrid_regimes",
    "claim_variance_protocol",
]
