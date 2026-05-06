"""Section 4.1-4.3: per-task experimental results -- FlightQA Table 1
+ constraint-scaling analysis (Fig. 9), FanOutQA Table 2, WebArena Table 3.

Source: Deng et al. 2025 [@Deng2025SIMURA], Sections 4.1-4.3.
"""

from gaia.lang import claim, setting

# ===========================================================================
# 4.1 Complex Website Navigation -- FlightQA
# ===========================================================================

# ---------------------------------------------------------------------------
# Dataset construction
# ---------------------------------------------------------------------------

setup_flightqa_dataset = claim(
    "**FlightQA dataset construction.** FlightQA is a new dataset "
    "introduced for controlled and scalable evaluation of agent "
    "reasoning on live web environments. The construction pipeline "
    "(Fig. 8) is: (1) **Constraint Generation** -- prompt an LLM "
    "(gpt-4o) to generate $N = 15$ lists of $C = 3$ starting "
    "constraints (ticket type, route, layover, etc.); "
    "(2) **Constraint Extension** -- iteratively add one constraint "
    "to each list, repeating $K = 5$ times; "
    "(3) **Question Generation** -- convert each constraint list "
    "into a natural-language question. "
    "Result: $N \\times (K+1) = 15 \\times 6 = 90$ questions with "
    "constraint counts ranging from 3 to 8. Generation prompts are "
    "in Appendix C.",
    title="Setup: FlightQA dataset = 15 sequences x 6 constraint counts = 90 questions (3-8 constraints each)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 8",
        "caption": "Fig. 8: FlightQA construction -- constraint generation, extension, question generation.",
    },
)

claim_flightqa_motivates_counterfactual = claim(
    "**FlightQA enables counterfactual analysis of constraint scaling.** "
    "Because each sequence shares its initial constraints and adds "
    "one constraint per step, FlightQA supports a *counterfactual "
    "analysis* that controls for the confounding effect of specific "
    "constraint configurations: an agent capable of robust reasoning "
    "should still succeed when an additional constraint is added to "
    "an existing query, while an agent relying on rote memorization "
    "is likely to fail. This addresses a gap in earlier benchmarks "
    "[@WebVoyager] that rely on self-instruct-based generation with "
    "limited constraint-structure control.",
    title="Setup: FlightQA's iterative-extension construction enables constraint-scaling counterfactual analysis",
)

setup_flightqa_evaluation = claim(
    "**FlightQA evaluation: groundedness + relevance via LLM judge.** "
    "Because FlightQA queries live information from the open "
    "internet (constantly evolving prices/availability), ground-"
    "truth answers cannot be established. Following [@CTC2021], the "
    "agent response is evaluated on two LLM-judged quality aspects: "
    "(E1) **Groundedness** -- whether the response is supported by "
    "the agent's interaction history (browser observations $o_1, "
    "\\dots, o_T$); "
    "(E2) **Relevance** -- whether the response satisfies user "
    "constraints to the extent allowed by the search results. "
    "An answer is **correct** iff it is *both grounded and "
    "relevant*. The LLM judge is prompted (Appendix C) following "
    "G-Eval [@GEval] standards. The full evaluation pipeline is run "
    "with gpt-4o.",
    title="Setup: FlightQA evaluation = LLM-judged Groundedness + Relevance; correct = grounded AND relevant",
)

# ---------------------------------------------------------------------------
# Table 1 main result
# ---------------------------------------------------------------------------

claim_flightqa_table1 = claim(
    "**FlightQA Table 1: full performance + outcome statistics.** "
    "All methods are evaluated on the 90-question FlightQA dataset "
    "with gpt-4o backbone over BrowserGym. (** denotes "
    "$p < 0.01$ over the second-best method; $\\dagger$ marks o1/"
    "o3-mini autoregressive-planner experiments run Feb 2025.)\n\n"
    "| Method | Correct | Grounded | Relevant | Response | Browser "
    "Crash | Max Steps | Repeat | Action Err |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
    "| OpenHands BrowsingAgent | 0.0 | 0.0 | 0.0 | 0.0 | 3.3 | "
    "3.3 | 0.0 | 93.3 |\n"
    "| SIMURA + Autoregressive | 14.4 | 15.6 | 14.4 | 16.7 | 0.0 | "
    "37.8 | 44.4 | 1.1 |\n"
    "| SIMURA + Autoregressive (o1)$\\dagger$ | 1.1 | 1.1 | 1.1 | "
    "1.1 | 11.1 | 40.0 | 37.8 | 10.0 |\n"
    "| SIMURA + Autoregressive (o3-mini)$\\dagger$ | 3.3 | 4.4 | 3.3 "
    "| 4.4 | 3.3 | 51.1 | 32.2 | 8.9 |\n"
    "| **SIMURA + World Model** | **32.2**\\*\\* | **36.7** | "
    "**32.2** | **38.9** | **1.1** | 40.0 | **18.9** | **1.1** |",
    title="FlightQA Table 1: full performance + failure-mode statistics (BrowsingAgent / SIMURA-AR / SIMURA-WM)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Table 1",
        "caption": "Table 1: FlightQA performance and outcome statistics.",
    },
)

claim_flightqa_browsing_action_error = claim(
    "**FlightQA: BrowsingAgent has 93.3% action-error rate.** The "
    "OpenHands BrowsingAgent fails to interact with the live "
    "Google Flights interface in 93.3% of runs due to malformed "
    "browser API calls (action errors). Combined with the 0.0% "
    "correct rate, this indicates the baseline is *unable to "
    "complete the task at all* under the open-web constraints. "
    "SIMURA's structured-language pipeline (encoder + memory + "
    "actor with observation grounding) reduces the action error "
    "rate to **1.1%** -- a 93.3% / 1.1% $\\approx$ 85x reduction.",
    title="FlightQA: structured pipeline reduces action-error rate 93.3% -> 1.1% (~85x)",
)

claim_flightqa_repetition_reduction = claim(
    "**FlightQA: world-model planning reduces repetitive-action "
    "failures from 44.4% to 18.9%.** Within SIMURA's pipeline, "
    "autoregressive planning still produces frequent repetitive "
    "actions (44.4% of runs end via the 3-consecutive-repeat "
    "termination rule), which world-model planning mitigates to "
    "**18.9%**. This pinpoints repetitive-action avoidance as a "
    "specific operational benefit of world-model simulation: "
    "predicting that the same action will lead to the same state "
    "lets the planner spot loops before committing.",
    title="FlightQA: world-model planning reduces repetitive-action failures 44.4% -> 18.9%",
)

claim_flightqa_browsingagent_no_o_models = claim(
    "**BrowsingAgent + o1/o3-mini are excluded from FlightQA "
    "evaluation.** The paper does not report BrowsingAgent with o1/"
    "o3-mini because the resulting agent *frequently hallucinates "
    "answers without interacting with the webpage*, which precludes "
    "valid agent evaluation. These hallucinations also fool the LLM "
    "evaluator at significant rates -- the paper flags this as "
    "additional work needed to secure LLM-judge robustness.",
    title="FlightQA: BrowsingAgent + o1/o3-mini excluded due to hallucination-without-interaction failure mode",
)

# ---------------------------------------------------------------------------
# Constraint-scaling analysis -- Fig. 9
# ---------------------------------------------------------------------------

claim_flightqa_constraint_scaling = claim(
    "**FlightQA Fig. 9: world-model planning maintains advantage "
    "across constraint counts.** Plotting % correct vs number of "
    "constraints (3-8) for both planning variants under SIMURA's "
    "pipeline shows that **world-model planning consistently "
    "outperforms autoregressive planning** across every constraint "
    "count in the data. Both methods show a roughly decreasing "
    "trend as constraints rise initially, with a sharp uptick at 7 "
    "constraints before a drop again -- the paper attributes this "
    "to *backend-LLM memorization* or *implicit constraints* in "
    "fewer-constraint questions. The consistent gap across "
    "constraint counts is read as evidence of improved *reasoning "
    "ability*, not just mean-level shift.",
    title="FlightQA Fig. 9: WM > AR at every constraint count 3-8 (consistent reasoning advantage, not mean shift)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 9",
        "caption": "Fig. 9: % correct vs number of constraints for FlightQA (WM consistently above AR).",
    },
)

# ---------------------------------------------------------------------------
# Hallucination motivating example
# ---------------------------------------------------------------------------

claim_chatgpt_4o_hallucination_example = claim(
    "**Hallucination example (Fig. 7).** Without browser grounding, "
    "ChatGPT-4o asked \"What is the earliest-arriving flight tomorrow "
    "from Pittsburgh to Zurich?\" (Dec. 17, 2024) hallucinated a "
    "10:45am arrival on Kayak.com, while the actual earliest flight "
    "lands at 6:10am. This motivates the live-web evaluation in "
    "FlightQA -- LLMs without grounding produce confident but "
    "incorrect answers for time-sensitive queries.",
    title="FlightQA Fig. 7: ChatGPT-4o hallucinated 10:45am Pittsburgh-Zurich flight; actual earliest is 6:10am (motivates live web eval)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 7",
        "caption": "Fig. 7: ChatGPT-4o flight hallucination vs actual Kayak.com search.",
    },
)

# ===========================================================================
# 4.2 Multi-Hop, Multi-Website QA -- FanOutQA
# ===========================================================================

setup_fanoutqa_eval = setting(
    "**FanOutQA evaluation.** FanOutQA [@FanOutQA] consists of "
    "questions requiring information about multiple entities across "
    "multiple websites (e.g., 'What are the availabilities of the "
    "top-10 restaurants in Paris for a dinner next week?'). Due to "
    "resource constraints, the paper evaluates the **first 100 "
    "examples of the dev set**. Backbone is gpt-4o-2024-05-13 (Nov "
    "10 - Dec 8, 2024); the same browser and termination rules as "
    "FlightQA apply. The paper notes that newer gpt-4o versions "
    "*deteriorated* world-model performance, attributed to changed "
    "response patterns to identical prompts.",
    title="Setup: FanOutQA evaluation -- first 100 dev examples, gpt-4o-2024-05-13 (note: newer gpt-4o degrades WM perf)",
)

claim_fanoutqa_table2 = claim(
    "**FanOutQA Table 2: full performance + outcome statistics.** "
    "Acc. (Strict) is the percentage of responses exactly matching "
    "ground truth. (* denotes $p < 0.05$ over the second-best "
    "method.)\n\n"
    "| Method | Acc. | Acc. (Strict) | Response | Browser Crash | "
    "Max Steps | Repeat | Action Err | Parse Err |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
    "| OpenHands BrowsingAgent | 17.0 | 4.0 | 32.0 | 17.0 | 8.0 | "
    "0.0 | 43.0 | 0.0 |\n"
    "| SIMURA + Autoregressive | 20.2 | 3.0 | 37.0 | 24.0 | 10.0 | "
    "18.0 | 10.0 | 1.0 |\n"
    "| **SIMURA + World Model** | **29.8**\\* | 4.0 | **55.0** | "
    "24.0 | 12.0 | 8.0 | **1.0** | 0.0 |",
    title="FanOutQA Table 2: full performance + outcome statistics (BrowsingAgent / SIMURA-AR / SIMURA-WM)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Table 2",
        "caption": "Table 2: FanOutQA performance and outcome statistics.",
    },
)

claim_fanoutqa_response_rate_jump = claim(
    "**FanOutQA: world-model planning increases response rate "
    "37.0% to 55.0%.** Beyond accuracy, world-model planning more "
    "than doubles the *response-returned* rate compared to "
    "autoregressive planning ($37.0\\%$ -> $55.0\\%$, $+48.6\\%$ "
    "relative). The paper highlights this as a measure of *task-"
    "completion rate* -- the agent more often reaches a state where "
    "it can produce an answer rather than terminating via "
    "max-steps/error.",
    title="FanOutQA: WM increases response-returned rate 37.0% -> 55.0% (+48.6% relative)",
)

claim_fanoutqa_action_error_reduction = claim(
    "**FanOutQA: structured pipeline reduces action errors "
    "43% to 10% (and to 1% with WM).** SIMURA's structured "
    "pipeline (autoregressive variant) already lowers action "
    "errors from $43\\%$ (BrowsingAgent) to $10\\%$, and full "
    "SIMURA reduces them further to $1\\%$ -- a 43x reduction "
    "vs the baseline. Browser crashes (24% for SIMURA) are flagged "
    "as a sizable failure mode unaddressed by the architecture, "
    "indicating room for tooling improvement.",
    title="FanOutQA: structured pipeline reduces action errors 43% -> 10% -> 1%; browser crashes 24% remain (tooling gap)",
)

claim_fanoutqa_browsing_partial_success = claim(
    "**FanOutQA: BrowsingAgent achieves partial success without "
    "memorization.** BrowsingAgent achieves $17.0\\%$ accuracy "
    "despite *not* maintaining cross-website memory, partly "
    "because some FanOutQA questions are answerable from a single "
    "Wikipedia page (e.g., 'What are the publication dates for all "
    "of the Harry Potter books?'). SIMURA still improves over "
    "BrowsingAgent even without world-model planning by "
    "dramatically reducing action errors.",
    title="FanOutQA: BrowsingAgent partial success comes from single-page-answerable questions (not multi-website memory)",
)

# ===========================================================================
# 4.3 General Web Automation -- WebArena
# ===========================================================================

setup_webarena_eval = claim(
    "**WebArena evaluation.** WebArena [@WebArena] is a standard "
    "benchmark featuring simulated websites: a Reddit-like social "
    "forum, a shopping site, a GitLab-based code platform, a map, "
    "and a Wikipedia-like encyclopedia. The paper evaluates a "
    "**random 100-sample subset** with gpt-4o over BrowserGym "
    "accessed via the OpenHands platform (which provides a uniform "
    "evaluation procedure but differs from the standard WebArena "
    "setup; absolute scores not comparable to prior work). The "
    "agent description is rewritten (Appendix B.1) to steer the "
    "agent toward WebArena's specific response format. Maximum "
    "allowed steps = 15 per WebArena's default.",
    title="Setup: WebArena evaluation -- 100-sample random subset, gpt-4o, OpenHands-mediated env (15-step budget)",
)

claim_webarena_table3 = claim(
    "**WebArena Table 3: success rates.**\n\n"
    "| Method | Success Rate (%) |\n"
    "|---|---|\n"
    "| OpenHands BrowsingAgent | 12.0 |\n"
    "| SIMURA + Autoregressive | 19.0 |\n"
    "| **SIMURA + World Model** | **23.0** |\n\n"
    "Cross-architecture: SIMURA full vs BrowsingAgent -> "
    "$+91.7\\%$ relative gain. Within-architecture: "
    "WM vs AR -> $+21.1\\%$ relative gain. Absolute scores are "
    "not directly comparable to prior WebArena reports due to "
    "the OpenHands-mediated setup [@WebArena].",
    title="WebArena Table 3: 12.0 (BrowsingAgent) / 19.0 (SIMURA-AR) / 23.0 (SIMURA-WM) success rates",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Table 3",
        "caption": "Table 3: WebArena (100-sample subset) success rates.",
    },
)

claim_webarena_setup_caveat = claim(
    "**WebArena absolute scores not comparable to prior work.** Due "
    "to following the environment and evaluator provided by OpenHands "
    "(which prioritizes open-web browsing), the WebArena absolute "
    "scores are *not directly comparable* to those reported in prior "
    "WebArena work [@WebArena]. The paper claims only the *relative* "
    "advantage of SIMURA over BrowsingAgent and of world-model "
    "planning over autoregressive planning under matched setup.",
    title="WebArena: absolute-score comparison invalid due to OpenHands-mediated env; only relative gains are claimed",
)

__all__ = [
    "setup_flightqa_dataset",
    "claim_flightqa_motivates_counterfactual",
    "setup_flightqa_evaluation",
    "claim_flightqa_table1",
    "claim_flightqa_browsing_action_error",
    "claim_flightqa_repetition_reduction",
    "claim_flightqa_browsingagent_no_o_models",
    "claim_flightqa_constraint_scaling",
    "claim_chatgpt_4o_hallucination_example",
    "setup_fanoutqa_eval",
    "claim_fanoutqa_table2",
    "claim_fanoutqa_response_rate_jump",
    "claim_fanoutqa_action_error_reduction",
    "claim_fanoutqa_browsing_partial_success",
    "setup_webarena_eval",
    "claim_webarena_table3",
    "claim_webarena_setup_caveat",
]
