"""Section 5.1: Calendar Scheduling — Clarify vs. Execute (Experiment 1)"""

from gaia.lang import claim, setting, support, abduction, compare

from .motivation import dc_framework_proposed, implicit_control_problem, alt_prompt_sufficient, separation_enables_attribution
from .s3_framework import sufficiency_signal_def, sequential_makes_failures_attributable

# ─── Settings ─────────────────────────────────────────────────────────────────

calendar_setup = setting(
    "Calendar scheduling experiment: the system must produce a valid JSON calendar event "
    "with four required fields — date, start_time, duration_min, attendees — from a "
    "natural-language request that may be incomplete or ambiguous. Scenarios vary two factors: "
    "(1) missing field count $k \\in \\{0, 1, 2, 3, 4\\}$ and (2) ambiguity type: 'absent' "
    "(field omitted) or 'unresolvable' (field referenced but not inferable, e.g., 'on Jack's "
    "usual slot'). This yields 8 unique scenarios. Turn budget $T=6$. Each scenario runs "
    "$N=10$ independent times. Executed on ibm/granite4:micro and LLaMA 3 (8B) [@Sun2026].",
    title="Calendar experiment setup",
)

dc_calendar_policy = setting(
    "The decision-centric (DC) calendar policy is a deterministic three-branch rule. "
    "Input: $\\hat{p}_{\\text{suff},t}$ (fraction of confirmed fields), last action, "
    "last validation result. Branch 1 (no-blind-retry): if last_action == execute AND "
    "last_val.valid == False → CLARIFY. Branch 2: elif $\\hat{p}_{\\text{suff},t} == 1.0$ "
    "→ EXECUTE. Branch 3: else → CLARIFY (ask about all unconfirmed fields at once). "
    "The sufficiency score $\\hat{p}_t = |\\text{confirmed fields}|/4$ is computed by an LLM "
    "extractor returning boolean presence per field [@Sun2026].",
    title="DC calendar policy specification",
)

# ─── Experimental observation claims ─────────────────────────────────────────

dc_granite_100pct_success = claim(
    "The decision-centric (DC) system achieves 100% success rate across all 8 calendar "
    "scheduling scenarios on Granite 4 micro, with 0 wasted executions at $k=2$ absent, "
    "$k=3$ absent, and 0.10 wasted at $k=1$ absent and $k=4$, and 0–1.65 clarification "
    "turns per run depending on scenario [@Sun2026].",
    title="DC achieves 100% success on all 8 calendar scenarios (Granite)",
    background=[calendar_setup, dc_calendar_policy],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 7",
        "caption": "Table 7: Full results by missing-field count k and ambiguity type. Granite 4 micro, T=6, N=10.",
    },
)

prompt_calendar_degrades = claim(
    "The Prompt-Clarify baseline on Granite 4 micro degrades sharply with increasing "
    "missing fields: success rates are 100% at $k=0$, 100% at $k=1$ absent, 100% at "
    "$k=1$ unresolvable, 100% at $k=2$ absent, 50% at $k=2$ unresolvable, 60% at $k=3$ "
    "(both types), and 10% at $k=4$. Average wasted executions reach 2.90 at $k=4$ "
    "[@Sun2026].",
    title="Prompt-Clarify degrades sharply with missing field count (Granite)",
    background=[calendar_setup],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 7",
        "caption": "Table 7: Full results by missing-field count k and ambiguity type.",
    },
)

retry_calendar_fails = claim(
    "The Retry baseline (regenerate after failure without explicit action decision) achieves "
    "100% success only at $k=0$ (all fields present) and 0% at all $k \\geq 1$ by exhausting "
    "the turn budget $T=6$ on repeated executions without ever clarifying. This confirms that "
    "Retry failures are structural (never clarifying) rather than ambiguity-driven "
    "[@Sun2026].",
    title="Retry baseline fails at all k>=1 by exhausting turn budget",
    background=[calendar_setup],
)

unresolvable_widens_gap = claim(
    "The unresolvable ambiguity condition (field referenced but not inferable) consistently "
    "widens the performance gap between DC and Prompt-Clarify compared to the absent "
    "condition. Prompt-Clarify drops to 50%, 60%, and 10% success at $k=2$, $k=3$, $k=4$ "
    "unresolvable, whereas DC maintains 100% because it continues clarifying until fields "
    "are explicitly confirmed rather than treating vague references as resolved [@Sun2026].",
    title="Unresolvable references widen the DC vs Prompt-Clarify gap",
    background=[calendar_setup, dc_calendar_policy],
)

dc_llama_transfer = claim(
    "The decision-centric approach transfers across model families: on LLaMA 3 (8B), DC "
    "(original) outperforms both Retry and Prompt-Clarify at every missing-field count $k$. "
    "DC (original) achieves 100% at $k=0$, 50% at $k=1$ absent, 100% at $k=1$ unresolvable, "
    "100% at $k=2$, 80% at $k=3$ unresolvable, and 100% at $k=4$. After constraining the "
    "question-generator prompt (DC constrained), success restores to 100% at all $k$ except "
    "$k=3$ unresolvable (90%) [@Sun2026].",
    title="DC transfers across model families (LLaMA 3 results)",
    background=[calendar_setup],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 8",
        "caption": "Table 8: LLaMA 3 (8B) full per-scenario breakdown, N=10, T=6.",
    },
)

# ─── Key diagnostic finding ───────────────────────────────────────────────────

k1_failure_localized = claim(
    "In the LLaMA 3 $k=1$ absent failure of DC (original), the sufficiency estimator "
    "correctly identifies that only duration_min is missing ($\\hat{p}_{\\text{suff}}=0.75$) "
    "and the policy correctly selects 'clarify', but the question generator produces a "
    "question about already-known fields (e.g., 'What time should the meeting start?'), "
    "preventing acquisition of the missing information. Constraining the question-generator "
    "prompt to ask only about the listed missing fields restores 100% success at $k=1$ "
    "absent without modifying the estimator, policy, or executor [@Sun2026].",
    title="k=1 LLaMA failure localized to question generator; fix is surgical",
    background=[calendar_setup, dc_calendar_policy],
    metadata={
        "figure": "artifacts/2604.00414.pdf",
        "caption": "Figure 1: Diagnostic trace for LLaMA 3 at k=1 (before and after fix).",
    },
)

# ─── Prediction claims for abduction ─────────────────────────────────────────

dc_predicts_high_success = claim(
    "The decision-centric framework predicts high task success and low wasted executions "
    "in calendar scheduling because the deterministic, explicit policy prevents premature "
    "execution (by requiring $\\hat{p}_{\\text{suff}}=1.0$ before executing) and prevents "
    "blind retries (by the no-blind-retry constraint in Branch 1 of the policy) "
    "[@Sun2026].",
    title="DC predicts high calendar success via explicit sufficiency gating",
    background=[dc_calendar_policy],
)

prompt_predicts_degradation = claim(
    "Prompt-based approaches predict degrading success rates as missing field count $k$ "
    "increases, because the model must simultaneously assess sufficiency and select actions "
    "within a single generation call, leading to premature execution when ambiguous "
    "information is mistakenly treated as resolved [@Sun2026].",
    title="Prompt-based approach predicts degradation with increasing missingness",
    background=[implicit_control_problem],
)

# ─── Abduction: DC vs Prompt on calendar task ─────────────────────────────────

s_dc_calendar = support(
    [dc_predicts_high_success],
    dc_granite_100pct_success,
    reason=(
        "The DC framework (@dc_predicts_high_success) predicts 100% success across all "
        "scenarios because the explicit sufficiency signal prevents premature execution and "
        "the no-blind-retry constraint prevents futile retries. The observation of 100% "
        "success at all k in Table 7 is exactly what @dc_predicts_high_success predicts "
        "[@Sun2026]."
    ),
    prior=0.9,
)

s_prompt_calendar = support(
    [prompt_predicts_degradation],
    dc_granite_100pct_success,
    reason=(
        "Prompt-based degradation (@prompt_predicts_degradation) would predict low success "
        "at $k=2,3,4$, which is consistent with Prompt-Clarify's 50%, 60%, 10% but "
        "inconsistent with DC's 100% across all $k$. Alt explanation cannot explain DC's "
        "100% success, since the prompt approach does not make this prediction "
        "[@Sun2026]."
    ),
    prior=0.35,
)

comp_calendar = compare(
    dc_predicts_high_success,
    prompt_predicts_degradation,
    dc_granite_100pct_success,
    reason=(
        "DC's prediction of 100% success (@dc_predicts_high_success) matches the observed "
        "outcome exactly. The prompt-based prediction of degradation "
        "(@prompt_predicts_degradation) matches the prompt baseline's behavior but not DC's. "
        "The 90 percentage-point gap at $k=4$ (DC: 100% vs Prompt: 10%) provides strong "
        "differentiation [@Sun2026]."
    ),
    prior=0.92,
)

abduction_calendar = abduction(
    s_dc_calendar,
    s_prompt_calendar,
    comp_calendar,
    reason=(
        "Both DC and prompt-based approaches attempt to explain the observed calendar "
        "scheduling outcomes on Granite 4 micro. The abduction evaluates which system "
        "architecture better explains the empirical performance pattern across 8 scenarios "
        "[@Sun2026]."
    ),
)

# ─── Modular repair benefit ───────────────────────────────────────────────────

strat_localization_enables_repair = support(
    [k1_failure_localized, separation_enables_attribution],
    dc_llama_transfer,
    reason=(
        "The modular architecture of the DC framework (@separation_enables_attribution) "
        "enables the k=1 failure to be precisely localized to the question generator "
        "(@k1_failure_localized). A targeted fix to the question-generation prompt — "
        "leaving the estimator, policy, and executor unchanged — restores 100% success at "
        "$k=1$ absent and 95% at $k=3$ (Table 3). This demonstrates that the transfer of "
        "the approach across model families is preserved once the model-specific component "
        "failure is addressed through modular repair [@Sun2026]."
    ),
    prior=0.85,
)
