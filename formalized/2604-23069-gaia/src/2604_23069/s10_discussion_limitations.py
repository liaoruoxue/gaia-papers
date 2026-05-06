"""Section 5 + Limitations: conclusion, future work, and stated limitations.

Section 5 (Conclusion and Future Work) and the Limitations subsection of
[@Wu2026ContextWeaver]. Captures the paper's own framing of scope and
unresolved issues, plus the qualitative-error-analysis takeaways from
Appendix E.1 that the conclusion implicitly relies on.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Section 5: Conclusion (synthesis claims)
# ---------------------------------------------------------------------------

claim_conclusion_summary = claim(
    "**Conclusion: ContextWeaver organizes an agent's history into a "
    "dependency-structured memory that retains only the steps needed "
    "to support future actions, providing a compact context that fits "
    "within a fixed token window.** By linking each step to the "
    "specific decisions it relies on and summarizing relevant test "
    "outcomes, ContextWeaver provides a compact context within a "
    "fixed window. Empirically, ContextWeaver performs best when the "
    "dependency structure is constructed with sufficient quality, "
    "and can improve performance in these settings without "
    "increasing context size [@Wu2026ContextWeaver, Sec. 5].",
    title="Conclusion: dependency-structured memory retains only future-relevant steps under fixed budget",
)

claim_central_argument_restated = claim(
    "**Central argument restated: maintaining explicit dependencies "
    "improves tool-use reliability under a fixed context budget.** "
    "The combined main-experiment, variance, ablation, iteration-"
    "scaling, and qualitative results support the paper's central "
    "argument that explicit modeling of inter-step dependencies "
    "yields a stable and scalable memory mechanism for tool-using "
    "LLM agents [@Wu2026ContextWeaver, Sec. 5, Abstract].",
    title="Central argument: explicit dependencies => reliable tool use under fixed context budget",
)

# ---------------------------------------------------------------------------
# Future work directions
# ---------------------------------------------------------------------------

claim_future_work_directions = claim(
    "**Stated future work: (i) parent selection with advanced "
    "testing signals, (ii) coverage tracking to capture explored "
    "code paths, (iii) smaller controller models to reduce overhead, "
    "(iv) longer-horizon and multi-agent settings, (v) broader range "
    "of model families and capability levels.** Section 5 explicitly "
    "lists these as open directions to extend ContextWeaver beyond "
    "the current SWE-Bench scope and the Claude/GPT-5/Gemini-3-Flash "
    "model set [@Wu2026ContextWeaver, Sec. 5].",
    title="Future work: better parent signals, coverage tracking, smaller controllers, multi-agent, more models",
)

# ---------------------------------------------------------------------------
# Limitations
# ---------------------------------------------------------------------------

claim_limit_test_driven_environments = claim(
    "**Limitation 1: scope is structured, test-driven environments "
    "such as SWE-Bench.** ContextWeaver's evaluation focuses on "
    "structured agent environments where explicit validation signals "
    "(test pass/fail) are available. While this enables clear "
    "measurement of reasoning quality, it may differ from open-ended "
    "domains lacking built-in feedback loops "
    "[@Wu2026ContextWeaver, Limitations].",
    title="Limit: scope is test-driven environments (SWE-Bench); open-ended domains untested",
)

claim_limit_diverse_signals_future = claim(
    "**Limitation 2: extension to diverse reasoning signals "
    "(implicit assertions, runtime traces, external validators) is "
    "future work.** The current Validation Layer relies on test-suite "
    "outputs; extending it to handle implicit assertions, runtime "
    "traces, or external validators is a promising direction for "
    "future work [@Wu2026ContextWeaver, Limitations].",
    title="Limit: extension to non-test feedback (implicit asserts, traces, external validators) is future work",
)

claim_limit_llm_dependency = claim(
    "**Limitation 3: ContextWeaver's behavior ultimately depends on "
    "the reliability of the underlying LLM (parent-selector, "
    "summarizer, validator).** As an LLM-based controller, "
    "ContextWeaver's behavior depends on the underlying language "
    "model's reliability. The paper mitigates this through "
    "*conservative graph updates* and *transparent node summaries*, "
    "but does not eliminate it. The Unified vs. Hybrid contrast "
    "(Sec 4.2) gives concrete evidence that backbone capability for "
    "*graph construction* is a live failure mode "
    "[@Wu2026ContextWeaver, Limitations, Sec. 4.2].",
    title="Limit: depends on backbone LLM reliability for parent selection / summarization",
)

# ---------------------------------------------------------------------------
# Qualitative error analysis (Appendix E.1) -- residual challenges
# ---------------------------------------------------------------------------

claim_shared_challenges = claim(
    "**Both methods struggle with repository-level ambiguity "
    "(similarly named modules, cross-file dependencies).** The "
    "qualitative error analysis on the 143 instances unsolved by "
    "either method identifies repository-level ambiguity -- in "
    "particular, similarly named modules and cross-file dependencies "
    "-- as a shared limitation. These cases reflect the broader "
    "challenge of maintaining global consistency over long debugging "
    "processes, beyond what memory-selection alone can address "
    "[@Wu2026ContextWeaver, Appendix E.1].",
    title="Shared challenge: repo-level ambiguity (similar names, cross-file deps) unsolved by both",
)

claim_practical_extensions = claim(
    "**Suggested practical extensions: lightweight repository "
    "consistency checks and loop-aware budget control.** The "
    "qualitative error analysis suggests adding lightweight "
    "repository consistency checks and loop-aware budget control as "
    "extensions that could further strengthen robustness while "
    "preserving the gains from dependency-structured memory "
    "[@Wu2026ContextWeaver, Appendix E.1].",
    title="Practical extensions: repo consistency checks + loop-aware budget control",
)

claim_takeaway_appendix_e1 = claim(
    "**Overall takeaway from Appendix E.1: dependency-structured "
    "memory leads to more stable file localization and more "
    "effective reuse of early evidence vs. sliding window.** "
    "ContextWeaver's selective, dependency-structured memory yields "
    "more stable file localization and more effective reuse of "
    "early evidence compared with a sliding-window baseline, "
    "supporting the central argument from a complementary angle "
    "(qualitative inspection of the error distribution) "
    "[@Wu2026ContextWeaver, Appendix E.1].",
    title="App E.1 takeaway: CW => stable file localization + reuse of early evidence",
)

# ---------------------------------------------------------------------------
# Ethics
# ---------------------------------------------------------------------------

claim_ethics_statement = claim(
    "**Ethics: experiments use only publicly available benchmarks "
    "and open-source repositories; no human subjects.** The Ethics "
    "Statement notes that all experiments use publicly available "
    "benchmarks and open-source repositories with no human-subjects "
    "involvement [@Wu2026ContextWeaver, Ethics Statement].",
    title="Ethics: public benchmarks + open-source repos; no human subjects",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "claim_conclusion_summary",
    "claim_central_argument_restated",
    "claim_future_work_directions",
    "claim_limit_test_driven_environments",
    "claim_limit_diverse_signals_future",
    "claim_limit_llm_dependency",
    "claim_shared_challenges",
    "claim_practical_extensions",
    "claim_takeaway_appendix_e1",
    "claim_ethics_statement",
]
