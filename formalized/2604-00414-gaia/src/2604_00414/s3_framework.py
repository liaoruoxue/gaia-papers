"""Section 3 & 4: Decision-Centric Abstraction and Sequential Decision-Making"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    dc_framework_proposed,
    separation_enables_attribution,
    utility_maximization,
)

# ─── Settings ────────────────────────────────────────────────────────────────

sequential_setting_def = setting(
    "In sequential settings, LLM systems face a recurring decision at each turn $t$: act on "
    "the current context $c_t$ or seek more information. The decision context $c_t$ contains "
    "the decision-relevant information available at turn $t$: the original request, prior "
    "model outputs, user responses, retrieved evidence, and validation outcomes. The framework "
    "does not prescribe a particular representation of $c_t$; its only architectural requirement "
    "is that whatever drives action selection be exposed explicitly [@Sun2026].",
    title="Sequential decision-making setting definition",
)

# ─── Single sufficiency signal ────────────────────────────────────────────────

sufficiency_signal_def = claim(
    "In the minimal sequential instantiation, action selection depends on a single explicit "
    "signal: a sufficiency score $\\hat{p}_{\\text{suff},t} \\in [0, 1]$, estimated from the "
    "current decision context $c_t$, that reflects whether the current context appears "
    "sufficient to act reliably. A simple threshold policy selects 'execute' when "
    "$\\hat{p}_{\\text{suff},t}$ exceeds a preset threshold and 'clarify' otherwise. The signal "
    "may be produced by an LLM-based estimator, rule-based checks, structural completeness "
    "measures, or retrieval scores [@Sun2026].",
    title="Sufficiency signal for minimal sequential control",
    background=[sequential_setting_def],
)

sequential_makes_failures_attributable = claim(
    "In the sequential decision-centric setting, if the system acts too early, the source of "
    "error can be traced to the sufficiency estimate $\\hat{p}_{\\text{suff},t}$, the policy "
    "$\\delta$, or the execution itself. Structural constraints can be enforced directly at "
    "the decision level — for example, after a failed 'execute', the system can be constrained "
    "to 'clarify' rather than retry blindly, preventing wasted turns that do not acquire new "
    "information [@Sun2026].",
    title="Sequential DC enables failure attribution and structural constraints",
    background=[sequential_setting_def, sufficiency_signal_def],
)

# ─── Multi-signal instantiation ───────────────────────────────────────────────

multi_signal_def = claim(
    "A multi-signal instantiation of the decision-centric framework uses two co-evolving "
    "explicit signals: (1) a sufficiency signal $\\hat{p}_{\\text{suff},t} \\in [0, 1]$, "
    "reflecting whether the current context contains enough information to act reliably "
    "(low value favors information acquisition), and (2) a correctness signal "
    "$\\hat{p}_{\\text{corr},t} \\in [0, 1]$, reflecting whether the current trajectory or "
    "intermediate result appears to be on the right track (low value after an action favors "
    "revision or backtracking) [@Sun2026].",
    title="Multi-signal instantiation with sufficiency and correctness",
    background=[sequential_setting_def],
)

joint_signal_value = claim(
    "The value of exposing both the sufficiency signal $\\hat{p}_{\\text{suff}}$ and "
    "correctness signal $\\hat{p}_{\\text{corr}}$ is that the optimal action depends on "
    "their joint state, not on either signal alone. Crucially, actions can update beliefs "
    "they were not primarily intended to target: a failed 'execute' action lowers perceived "
    "correctness while simultaneously improving sufficiency by eliminating alternative "
    "candidates. This enables richer action spaces without changing the architectural "
    "separation between context, policy, and execution [@Sun2026].",
    title="Value of joint multi-signal state for action selection",
    background=[multi_signal_def],
)

correlated_belief_update = claim(
    "In sequential settings with multiple signals, actions can produce correlated belief "
    "updates across signals. Specifically, a failed traversal (execute action that returns "
    "incorrect result) can simultaneously decrease $\\hat{p}_{\\text{corr}}$ and increase "
    "$\\hat{p}_{\\text{suff}}$ by eliminating candidates that share the traversed node's "
    "minority-valued hidden attribute. This 'passive' sufficiency improvement via elimination "
    "is unobservable to prompt-based systems that do not maintain explicit belief state "
    "[@Sun2026].",
    title="Correlated belief update via failed traversal eliminates candidates",
    background=[multi_signal_def],
)

# ─── Reasoning strategies ────────────────────────────────────────────────────

strat_sequential_attribution = deduction(
    [dc_framework_proposed],
    sequential_makes_failures_attributable,
    reason=(
        "The decision-centric framework (@dc_framework_proposed) separates signal estimation, "
        "policy, and execution. In the sequential setting, the "
        "decision context $c_t$ is explicit and the policy $\\delta$ is deterministic. "
        "It follows by construction that any failure to act correctly at turn $t$ must be "
        "attributable to one of: (a) incorrect $\\hat{p}_{\\text{suff},t}$ (signal error), "
        "(b) wrong policy mapping from correct signal (policy error), or (c) correct decision "
        "but poor execution (execution error). Structural constraints such as 'no-blind-retry' "
        "can be encoded as guards before policy branches [@Sun2026]."
    ),
    prior=0.99,
    background=[sequential_setting_def],
)

strat_joint_from_multi = support(
    [multi_signal_def],
    joint_signal_value,
    reason=(
        "The multi-signal instantiation (@multi_signal_def) exposes $\\hat{p}_{\\text{suff}}$ "
        "and $\\hat{p}_{\\text{corr}}$ as separate observable quantities available to the "
        "policy $\\delta$. Because $\\delta$ takes the full context (including both signals) "
        "as input, the action selected at a joint state $(p_s, p_c)$ can differ from the "
        "action at either marginal. The paper illustrates this concretely: the same low "
        "$\\hat{p}_{\\text{corr}}$ produces 'backtrack' in S3 (high $\\hat{p}_{\\text{suff}}$, "
        "few alternatives) and 'clarify' in S4 (low $\\hat{p}_{\\text{suff}}$, many "
        "alternatives) [@Sun2026]."
    ),
    prior=0.9,
)

strat_correlated_from_joint = support(
    [joint_signal_value, multi_signal_def],
    correlated_belief_update,
    reason=(
        "In the multi-signal setting (@multi_signal_def), both $\\hat{p}_{\\text{suff}}$ and "
        "$\\hat{p}_{\\text{corr}}$ are updated at each turn. @joint_signal_value establishes "
        "that actions update beliefs they were not primarily intended to target. A concrete "
        "mechanism: when the visited node in a graph search has a minority-valued hidden "
        "attribute (value shared by few peer candidates), all other candidates with that "
        "value are eliminated, raising $\\hat{p}_{\\text{suff}}$ (fewer candidates = higher "
        "sufficiency = $1/|\\text{candidates}|$) simultaneously with the decrease in "
        "$\\hat{p}_{\\text{corr}}$ from the failed match. This correlated update is only "
        "possible because both signals are maintained explicitly in the belief state [@Sun2026]."
    ),
    prior=0.9,
)
