"""Section 4 overview: cross-task overview of SIMURA's empirical
performance across the 3 web-browsing task families (FlightQA, FanOutQA,
WebArena), and the panel-level claims that aggregate per-task results
(0%->32.2% on FlightQA, +124% world-model-vs-autoregressive, multi-task
generality).

Source: Deng et al. 2025 [@Deng2025SIMURA], Section 4 'Overview of
Results' + Fig. 6.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Overall experimental setup
# ---------------------------------------------------------------------------

setup_three_task_families = setting(
    "**Three web-browsing task families evaluated.** SIMURA is "
    "evaluated on three categories of web-browsing tasks: "
    "(T1) **Complex Website Navigation** -- FlightQA (90 questions, "
    "3-8 constraints, live flight search; Section 4.1). "
    "(T2) **Multi-Hop, Multi-Website QA** -- FanOutQA [@FanOutQA] "
    "(first 100 examples of dev set; Section 4.2). "
    "(T3) **General Web Automation** -- WebArena [@WebArena] "
    "(random 100-sample subset; Section 4.3). "
    "T1 stresses *depth* of navigation on a single complex site; T2 "
    "stresses *breadth* across many websites with long-horizon "
    "interaction; T3 stresses *generality* across sites of moderate "
    "complexity (Reddit-like forum, shopping, GitLab, map, "
    "Wikipedia-like encyclopedia).",
    title="Setup: three web-browsing task families -- depth (FlightQA), breadth (FanOutQA), generality (WebArena)",
)

setup_baselines_overall = setting(
    "**Baselines compared in all three task families.** Three "
    "comparators are used in (subsets of) each task family: "
    "(B1) **OpenHands BrowsingAgent** [@OpenHands] -- representative "
    "open-source autoregressive web agent (cross-architecture "
    "baseline). "
    "(B2) **SIMURA + autoregressive planning** -- SIMURA's pipeline "
    "with the world-model-based planner replaced by a "
    "commit-to-first-sample policy (within-architecture baseline; "
    "see @setup_autoregressive_planning_baseline). "
    "(B3) **SIMURA + world-model planning (full)** -- the full "
    "proposed architecture. "
    "The within-architecture comparison (B2 vs B3) isolates the "
    "contribution of world-model planning from the structured-NL "
    "pipeline; the cross-architecture comparison (B1 vs B3) "
    "quantifies the cumulative gain.",
    title="Setup: cross-architecture (BrowsingAgent) vs within-architecture (autoregressive) baselines + full SIMURA",
)

setup_environment_and_budget = setting(
    "**Environment and execution rules (shared across tasks).** All "
    "experiments use BrowserGym [@BrowserGym], an open-source browser "
    "sandbox. Each run terminates when (i) the agent provides a "
    "response, (ii) the agent takes 30 actions (15 for WebArena, per "
    "the WebArena default), (iii) the agent repeats the same action "
    "3 times consecutively, or (iv) the agent causes more than 3 "
    "interaction errors. Backbone LLM is gpt-4o (with named version "
    "for FanOutQA: gpt-4o-2024-05-13). Selected o1 / o3-mini "
    "experiments run on FlightQA only (Feb 3-5, 2025); other "
    "experiments run Nov-Dec 2024.",
    title="Setup: BrowserGym environment + 30-step budget + gpt-4o backbone (Nov-Dec 2024)",
)

# ---------------------------------------------------------------------------
# Headline: Figure 6 overview
# ---------------------------------------------------------------------------

claim_overview_three_task_panel = claim(
    "**Cross-task overview (Figure 6 / Tables 1-3).** Across all "
    "three task families, SIMURA's full architecture shows a clear "
    "advantage over the BrowsingAgent baseline; within SIMURA's "
    "pipeline, world-model-based planning consistently improves over "
    "matched autoregressive planning. The aggregated headline figures "
    "are summarized in the table below (best per row in **bold**):\n\n"
    "| Task family | Metric | BrowsingAgent | SIMURA + AR | "
    "**SIMURA + WM** | WM/AR rel. gain |\n"
    "|---|---|---|---|---|---|\n"
    "| FlightQA (T1) | Correct (%) | 0.0 | 14.4 | **32.2** | +124% |\n"
    "| FanOutQA (T2) | Acc. (%) | 17.0 | 20.2 | **29.8** | +48.6% |\n"
    "| WebArena (T3) | Success (%) | 12.0 | 19.0 | **23.0** | "
    "+21.1% |\n\n"
    "Both BrowsingAgent improvement and world-model-vs-autoregressive "
    "improvement are *consistent across all 3 panels*, supporting the "
    "generality claim. ($p < 0.01$ for FlightQA WM/AR; $p = 0.011$ "
    "for FanOutQA.)",
    title="Cross-task overview (Fig. 6 / Tables 1-3): consistent SIMURA-WM > SIMURA-AR > BrowsingAgent across 3 panels",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 6 + Tables 1, 2, 3",
        "caption": "Fig. 6: aggregated comparison across FlightQA, FanOutQA, WebArena.",
    },
)

# ---------------------------------------------------------------------------
# Headline aggregated empirical claims
# ---------------------------------------------------------------------------

claim_simura_beats_browsingagent_across_tasks = claim(
    "**SIMURA's full architecture outperforms BrowsingAgent across "
    "all three task families.** The relative improvements over "
    "BrowsingAgent are: FlightQA $0\\% \\to 32.2\\%$ (improvement "
    "is unbounded -- the baseline rate is zero); FanOutQA $17.0\\% "
    "\\to 29.8\\%$ ($+12.8$ pp, $+75.3\\%$ relative); WebArena "
    "$12.0\\% \\to 23.0\\%$ ($+11.0$ pp, $+91.7\\%$ relative). The "
    "result is consistent across very different task structures "
    "(deep flight search, broad multi-website QA, general moderate-"
    "complexity automation), supporting the *generality* claim of "
    "SIMURA's architecture.",
    title="Result: SIMURA full > BrowsingAgent on all 3 families (FlightQA, FanOutQA, WebArena)",
)

claim_wm_beats_ar_across_tasks = claim(
    "**World-model planning consistently beats autoregressive "
    "planning within SIMURA's pipeline.** Holding all non-planner "
    "modules fixed, swapping autoregressive single-sample planning "
    "for world-model-based simulation yields: "
    "FlightQA correct rate $14.4\\% \\to 32.2\\%$ ($+17.8$ pp, "
    "$+123.6\\%$ relative; significant at $p < 0.01$); "
    "FanOutQA accuracy $20.2\\% \\to 29.8\\%$ ($+9.6$ pp, "
    "$+47.5\\%$ relative; $p = 0.011$); "
    "WebArena success $19.0\\% \\to 23.0\\%$ ($+4.0$ pp, "
    "$+21.1\\%$ relative). Improvement direction is **identical "
    "across all three tasks** despite very different task "
    "structures.",
    title="Result: SIMURA-WM > SIMURA-AR on all 3 panels (consistent direction; FlightQA +124% relative)",
)

claim_124pct_max_relative_improvement = claim(
    "**Maximum relative improvement: 124% on FlightQA task-completion "
    "rate.** Among the three task families, the largest relative "
    "improvement of world-model planning over autoregressive "
    "planning is observed on FlightQA, where the correct-response "
    "rate rises from $14.4\\%$ to $32.2\\%$ -- $32.2 / 14.4 - 1 "
    "\\approx 1.236$, i.e., **+124% relative gain in task-completion "
    "rate**. This is the abstract's headline number; statistical "
    "significance is $p < 0.01$ via pairwise t-test.",
    title="Result: maximum relative gain = 124% on FlightQA (32.2 / 14.4 - 1; p<0.01 pairwise t-test)",
)

# ---------------------------------------------------------------------------
# Surprise findings -- strong reasoning LLMs as autoregressive planners
# ---------------------------------------------------------------------------

claim_o1_o3mini_close_to_zero = claim(
    "**Strong RL-trained reasoning LLMs (o1, o3-mini) achieve close-"
    "to-zero success rate as autoregressive planners on FlightQA.** "
    "Replacing gpt-4o with the more powerful reasoning LLMs o1 "
    "[@OpenAIo1] and o3-mini [@OpenAIo3mini] inside the *autoregressive "
    "planner* of SIMURA's pipeline yields **1.1%** and **3.3%** "
    "correct rates respectively on FlightQA -- both substantially "
    "below gpt-4o autoregressive planning (14.4%) and dramatically "
    "below world-model planning (32.2%). The result suggests that "
    "even a strong textual-reasoning model can have *limited "
    "success with planning for web interactions* purely through "
    "autoregressive generation.",
    title="Result: o1 / o3-mini autoregressive planning -> 1.1% / 3.3% on FlightQA (well below gpt-4o WM 32.2%)",
)

claim_temporal_repeatability_caveat = claim(
    "**Temporal repeatability caveat.** All experiments were "
    "conducted in 2024 (Nov-Dec) using then-available models and "
    "browser tooling, except the o1/o3-mini autoregressive-planner "
    "experiment which ran Feb 3-5, 2025. While subsequent model "
    "updates may yield higher absolute scores, the paper claims "
    "that the *world-model-vs-autoregressive advantage* under "
    "*identical conditions* is measurable and repeatable.",
    title="Result: temporal caveat -- WM vs AR advantage is the repeatable claim, not absolute score levels",
)

__all__ = [
    "setup_three_task_families",
    "setup_baselines_overall",
    "setup_environment_and_budget",
    "claim_overview_three_task_panel",
    "claim_simura_beats_browsingagent_across_tasks",
    "claim_wm_beats_ar_across_tasks",
    "claim_124pct_max_relative_improvement",
    "claim_o1_o3mini_close_to_zero",
    "claim_temporal_repeatability_caveat",
]
