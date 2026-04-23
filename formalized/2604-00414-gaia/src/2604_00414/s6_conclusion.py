"""Section 6: Conclusion — Synthesizing Evidence for Explicit Decision Layer"""

from gaia.lang import claim, support

from .motivation import (
    dc_framework_proposed,
    implicit_control_problem,
    prompt_control_implicit,
    framework_preserves_uncertainty,
    separation_enables_attribution,
    utility_maximization,
)
from .s3_framework import (
    sufficiency_signal_def,
    multi_signal_def,
)
from .s5_exp1_calendar import (
    dc_granite_100pct_success,
    prompt_calendar_degrades,
    retry_calendar_fails,
    unresolvable_widens_gap,
    k1_failure_localized,
)
from .s5_exp2_graph import (
    dc_graph_100pct,
    s2_sufficiency_isolation,
    s5_correlated_update_result,
    prompt_policy_insufficient_for_s5,
)
from .s5_exp3_retrieval import (
    medium_bucket_results,
    easy_bucket_results,
    hard_bucket_results,
    prompt_correct_assessment_wrong_action,
    modularity_signal_isolation,
    failure_attribution_retrieval,
    threshold_robustness,
    explicit_control_law,
    dc_reduces_wasted_calendar,
    dc_improves_graph_success,
    dc_improves_retrieval_medium,
)

# ─── Synthesizing conclusions ──────────────────────────────────────────────────

framework_is_general = claim(
    "The value of an explicit decision layer in LLM systems is not tied to a single task "
    "or signal type. In calendar scheduling, it reduces wasted actions by enforcing "
    "sufficiency-based control. In graph search, it supports multi-belief, cross-turn "
    "decisions that implicit prompting does not reliably recover. In retrieval, it makes "
    "sufficiency a modular and diagnosable signal, enabling attribution and improvement "
    "without changing the controller. The common benefit is architectural: once "
    "decision-relevant state is externalized, control becomes more reliable, interpretable, "
    "and easier to improve [@Sun2026].",
    title="Explicit decision layer provides general architectural benefit across tasks",
)

prompt_fundamental_limit = claim(
    "The fundamental limitation of prompt-based control persists regardless of model "
    "capability: assessment and action are fused inside a single model call, making the "
    "basis for behavior hard to inspect, enforce, diagnose, or repair, especially in "
    "sequential settings where errors compound over time. Even Prompt (w/ policy) — which "
    "explicitly states the decision logic in the system prompt — fails in scenario S5 (35%) "
    "because the bottleneck is not the policy specification but the missing belief state "
    "update that only explicit state maintenance can provide [@Sun2026].",
    title="Prompt-based control has fundamental limitation beyond model capability",
)

# ─── Support strategies for previously orphaned claims ────────────────────────

strat_framework_is_general = support(
    [dc_reduces_wasted_calendar, dc_improves_graph_success, dc_improves_retrieval_medium],
    framework_is_general,
    reason=(
        "The three experiments jointly establish that the explicit decision layer benefit "
        "is task-general: @dc_reduces_wasted_calendar shows calendar scheduling improvement, "
        "@dc_improves_graph_success shows graph disambiguation improvement, and "
        "@dc_improves_retrieval_medium shows retrieval control improvement. All three use "
        "different signal types (structural completeness, graph beliefs, embedding similarity) "
        "and different action spaces, yet all show the same architectural benefit "
        "[@Sun2026]."
    ),
    prior=0.9,
)

strat_prompt_fundamental_limit = support(
    [prompt_control_implicit, prompt_policy_insufficient_for_s5, prompt_correct_assessment_wrong_action],
    prompt_fundamental_limit,
    reason=(
        "The fundamental limit claim is supported by three independent lines of evidence: "
        "(1) @prompt_control_implicit establishes the architectural entanglement, "
        "(2) @prompt_policy_insufficient_for_s5 shows that even explicit policy prompting "
        "fails in S5 (35%) because the belief state is unavailable, and "
        "(3) @prompt_correct_assessment_wrong_action shows that 64% of Prompt medium "
        "failures involve correct assessment but wrong action — the recognition-to-control "
        "mapping fails despite model capability [@Sun2026]."
    ),
    prior=0.88,
)

# Connect orphaned experimental observations to the explicit_control_law
strat_control_law_from_observations = support(
    [dc_granite_100pct_success, dc_graph_100pct, medium_bucket_results],
    explicit_control_law,
    reason=(
        "The three experimental results — @dc_granite_100pct_success (100% calendar "
        "success vs Prompt's 10% at k=4), @dc_graph_100pct (100% graph success vs 35% "
        "in S5), and @medium_bucket_results (88% DC-LLM vs 14% Prompt retrieval) — "
        "jointly provide empirical grounding for @explicit_control_law. Each uses a "
        "different domain and signal type, providing independent converging evidence that "
        "the explicit control layer improves reliability across diverse settings "
        "[@Sun2026]."
    ),
    prior=0.88,
)

# Connect utility_maximization to dc_framework_proposed
strat_utility_supports_unification = support(
    [dc_framework_proposed, prompt_calendar_degrades],
    implicit_control_problem,
    reason=(
        "The prompt degradation observations (@prompt_calendar_degrades) empirically "
        "confirm the implicit control problem (@implicit_control_problem) at scale: "
        "as task complexity increases (more missing fields), the failure modes of "
        "entangled assessment and action become increasingly consequential. The DC framework "
        "(@dc_framework_proposed) addresses this by separating the decision layer "
        "[@Sun2026]."
    ),
    prior=0.85,
)

# Connect sufficiency_signal_def to calendar success
strat_suff_signal_enables_success = support(
    [sufficiency_signal_def],
    dc_granite_100pct_success,
    reason=(
        "The explicit sufficiency signal (@sufficiency_signal_def) is the mechanism "
        "through which DC achieves 100% calendar success: by computing "
        "$\\hat{p}_{\\text{suff}} = |\\text{confirmed fields}|/4$ independently of "
        "action selection, the policy can reliably gate execution on "
        "$\\hat{p}_{\\text{suff}} = 1.0$ and prevent premature execution that causes "
        "Prompt-Clarify's failures at $k \\geq 2$ [@Sun2026]."
    ),
    prior=0.88,
)

# Connect modularity evidence
strat_modularity_from_isolation = support(
    [modularity_signal_isolation, failure_attribution_retrieval, k1_failure_localized],
    framework_is_general,
    reason=(
        "Modularity evidence from three experiments: @modularity_signal_isolation shows "
        "that three DC retrieval variants with the same controller isolate signal quality; "
        "@failure_attribution_retrieval shows that medium vs hard failures have different "
        "root causes attributable to specific components; @k1_failure_localized shows "
        "that the LLaMA 3 k=1 failure is pinpointed to the question generator and fixed "
        "without touching any other component. All three demonstrate the modular "
        "diagnosis-and-repair benefit of the explicit decision layer [@Sun2026]."
    ),
    prior=0.9,
)

# Connect threshold robustness to the retrieval modularity claim
strat_robustness_supports_modularity = support(
    [threshold_robustness],
    modularity_signal_isolation,
    reason=(
        "The offline threshold sweep (@threshold_robustness) confirms @modularity_signal_isolation: "
        "parameters $\\alpha$ and $\\tau$ were selected on a held-out validation set before "
        "test evaluation, and the sweep is computed offline by replaying saved per-round "
        "signal traces. This offline replayability is only possible because the sufficiency "
        "signal is externalized — with implicit Prompt control, no analog exists "
        "[@Sun2026]."
    ),
    prior=0.85,
)

# Connect retry failures to the explicit control benefit
strat_retry_confirms_structural = support(
    [retry_calendar_fails, s2_sufficiency_isolation],
    prompt_fundamental_limit,
    reason=(
        "Retry failures confirm the structural nature of implicit control limitations: "
        "@retry_calendar_fails shows that without any explicit decision layer, the system "
        "exhausts its turn budget on repeated executions (0% success at k>=1), and "
        "@s2_sufficiency_isolation shows Retry drops to 45% (vs DC 100%) in S2 by "
        "executing blindly into a pool of 13 candidates. These are not model failures "
        "but control architecture failures [@Sun2026]."
    ),
    prior=0.88,
)

# Connect easy/hard bucket results to retrieval modularity
strat_easy_hard_complete_picture = support(
    [easy_bucket_results, hard_bucket_results, medium_bucket_results],
    modularity_signal_isolation,
    reason=(
        "The full three-bucket picture supports @modularity_signal_isolation: "
        "@easy_bucket_results shows DC-Dense over-expands (1.12 rounds vs DC-LLM's 0.62), "
        "which is attributable to the relevance-vs-answerability signal distinction; "
        "@hard_bucket_results shows all methods converge at ~18% due to corpus gaps "
        "rather than signal failures; @medium_bucket_results shows the maximal "
        "decision-point differentiation (14% Prompt vs 94% DC-Composite). Together "
        "they enable component-level diagnosis that matches the paper's attribution "
        "analysis [@Sun2026]."
    ),
    prior=0.85,
)

# Connect unresolvable_widens_gap to the framework benefit
strat_unresolvable_confirms_dc = support(
    [unresolvable_widens_gap],
    dc_granite_100pct_success,
    reason=(
        "The unresolvable ambiguity condition (@unresolvable_widens_gap) provides a "
        "stricter test of DC's explicit control: when fields are referenced but not "
        "inferable, only an explicit sufficiency signal that distinguishes 'field present' "
        "from 'field usably specified' can prevent premature execution. DC achieves 100% "
        "even here by continuing to clarify until $\\hat{p}_{\\text{suff}} = 1.0$ "
        "[@Sun2026]."
    ),
    prior=0.9,
)

# Connect framework_preserves_uncertainty to the law
strat_uncertainty_preserved = support(
    [framework_preserves_uncertainty],
    framework_is_general,
    reason=(
        "The framework's design (@framework_preserves_uncertainty) — maintaining "
        "uncertainty in the context while making action selection deterministic — enables "
        "applicability across diverse settings. Since the explicit decision layer does "
        "not require eliminating uncertainty (only externalizing the signals), it can "
        "accommodate any signal type: LLM-based estimates, embedding similarities, "
        "structural checks, or hard domain constraints [@Sun2026]."
    ),
    prior=0.85,
)

# Connect multi_signal_def to dc_graph_100pct
strat_multi_signal_enables_graph = support(
    [multi_signal_def],
    dc_graph_100pct,
    reason=(
        "The multi-signal instantiation (@multi_signal_def) is the mechanism enabling "
        "DC's 100% graph disambiguation success: by maintaining both $\\hat{p}_{\\text{suff}}$ "
        "and $\\hat{p}_{\\text{corr}}$ explicitly, the policy can distinguish between the "
        "S3 case (high $\\hat{p}_{\\text{suff}}$, low $\\hat{p}_{\\text{corr}}$ → backtrack) "
        "and S4 case (low $\\hat{p}_{\\text{suff}}$, low $\\hat{p}_{\\text{corr}}$ → clarify), "
        "and handle the S5 correlated belief update that prompt approaches miss "
        "[@Sun2026]."
    ),
    prior=0.88,
)

# Connect utility_maximization to dc_framework_proposed
strat_utility_from_framework = support(
    [dc_framework_proposed],
    utility_maximization,
    reason=(
        "The decision-centric framework (@dc_framework_proposed) defines $\\delta$ as a "
        "deterministic function mapping context $c$ to action. The constrained utility "
        "maximization formulation (@utility_maximization) is the most common instantiation: "
        "$\\delta(c) = a^* = \\arg\\max_{a \\in \\mathcal{F}(c)} U(a, c)$. Given the "
        "framework provides the interface for $\\delta$, it follows that utility "
        "maximization is a valid and common concrete realization of that interface "
        "[@Sun2026]."
    ),
    prior=0.9,
)
