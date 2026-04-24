"""Section 5: Discussion and Future Work"""

from gaia.lang import claim, setting, support

from .motivation import mdap_orthogonal_direction, single_agent_infeasible
from .s3_framework import (
    mad_reduces_context,
    mad_enables_error_correction,
    red_flag_reduces_correlation,
    cost_scales_log_linearly,
)
from .s4_experiments import (
    maker_zero_errors,
    errors_decorrelated,
    red_flag_reduces_collisions,
    error_rate_stable,
)

# --- Correlated Errors as Open Problem ---

correlated_errors_open = claim(
    "Correlated errors — where particular input states cause the LLM to fail "
    "consistently across independent samples — are an open foundational problem. "
    "Even in the Towers of Hanoi experiments, a few steps showed substantially higher "
    "error rates than others for no apparent reason (e.g., step 10241 required 18 "
    "voting rounds). Simple resampling with temperature sufficed here, but real-world "
    "tasks may require more sophisticated decorrelation methods such as prompt "
    "paraphrasing or noise injection.",
    title="Correlated errors remain an open problem requiring sophisticated decorrelation",
)

strat_correlated_errors = support(
    [red_flag_reduces_collisions, errors_decorrelated],
    correlated_errors_open,
    reason=(
        "@red_flag_reduces_collisions shows that red-flagging reduces but does not "
        "eliminate correlated errors, and @errors_decorrelated shows that temperature-based "
        "resampling decorrelates most errors in this domain. However, the pathological "
        "step requiring 18 rounds suggests that some input states create persistent "
        "correlation that simple resampling cannot fully address — motivating future work "
        "on prompt-level decorrelation."
    ),
    prior=0.80,
)

# --- Societal and Safety Implications ---

mdap_reduces_risk = claim(
    "MDAPs (using small, focused microagents instead of large unified models) may reduce "
    "AI safety risks: extreme decomposition limits the scope of each agent, reducing the "
    "chance that any single agent accumulates sufficient context to exhibit misaligned "
    "behavior, and may reduce the risk of unintended sentience emerging in constrained "
    "agents. This is an orthogonal risk-reduction path compared to capability control.",
    title="MDAPs may reduce AI safety and model welfare risks",
)

strat_mdap_safety = support(
    [mdap_orthogonal_direction, mad_reduces_context],
    mdap_reduces_risk,
    reason=(
        "@mdap_orthogonal_direction establishes that MDAPs use smaller, less capable "
        "models. @mad_reduces_context shows that each agent operates with minimal context. "
        "Together, these structural properties limit the scope of any individual agent's "
        "reasoning and reduce the surface area for misaligned or unintended emergent "
        "behavior — a qualitative safety argument supported by alignment research."
    ),
    prior=0.65,
)

# --- Scalability Beyond Towers of Hanoi ---

maker_scalable_beyond = claim(
    "The MAKER framework's log-linear cost scaling (Theta(s*ln(s))) suggests it can "
    "scale far beyond one million steps in principle, and potentially to tasks at the "
    "level of organizational and societal complexity (billions of steps). The framework "
    "has been preliminarily extended to large-digit multiplication, showing promising "
    "results on a task notoriously difficult for transformer-based models.",
    title="MAKER scalable to organizational-scale tasks and beyond Towers of Hanoi",
)

strat_scalable_beyond = support(
    [cost_scales_log_linearly, maker_zero_errors],
    maker_scalable_beyond,
    reason=(
        "@cost_scales_log_linearly provides the theoretical bound that cost grows "
        "only as O(s*ln(s)), and @maker_zero_errors demonstrates empirical success "
        "at 1M steps. Extrapolating the theory suggests feasibility at larger scales. "
        "The multiplication result provides additional evidence of domain generality, "
        "though formal validation at scale beyond Towers of Hanoi is future work."
    ),
    prior=0.72,
)
