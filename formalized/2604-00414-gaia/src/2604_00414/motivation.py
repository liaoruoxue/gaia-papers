"""Introduction and Motivation: Decision-Centric Design for LLM Systems"""

from gaia.lang import claim, setting, question, support, deduction, complement, contradiction

# ─── Settings (background context) ───────────────────────────────────────────

deployment_context = setting(
    "Large language model (LLM) systems are increasingly deployed as components of larger "
    "AI pipelines, where they must do more than generate text: they help route requests, "
    "allocate compute, retrieve information, call tools, and participate in multi-step "
    "workflows. In these settings, system behavior depends on both generation quality and "
    "control decisions about when and how to act [@Sun2026].",
    title="LLM deployment context",
)

# ─── Core problem claims ──────────────────────────────────────────────────────

implicit_control_problem = claim(
    "In many current LLM system architectures, control decisions (whether to answer, "
    "clarify, retrieve, call tools, repair, or escalate) remain implicit within generation, "
    "entangling context interpretation, signal estimation, action selection, and output "
    "generation inside a single model call. This makes failures hard to inspect, constrain, "
    "or repair [@Sun2026].",
    title="Implicit control problem in LLM systems",
    background=[deployment_context],
)

prompt_control_implicit = claim(
    "Prompt-based control is implicit: assessment and action are fused inside a single model "
    "call, making the basis for system behavior hard to inspect, enforce, diagnose, or repair, "
    "especially in sequential settings where errors compound over time [@Sun2026].",
    title="Prompt-based control is fundamentally implicit",
    background=[deployment_context],
)

# ─── Framework proposal ───────────────────────────────────────────────────────

dc_framework_proposed = claim(
    "A decision-centric framework (DC) is proposed that separates decision-relevant signals "
    "from the policy that maps them to actions, turning control from an implicit byproduct "
    "of generation into an explicit, inspectable, and enforceable layer of the LLM system. "
    "The three core elements are: (1) a finite set of candidate actions $\\mathcal{A}$, "
    "(2) a decision context $c$ comprising observed, estimated, and learned quantities, and "
    "(3) a deterministic decision function $\\delta: c \\mapsto a \\in \\mathcal{A}$ [@Sun2026].",
    title="Decision-centric framework proposal",
    background=[deployment_context],
)

separation_enables_attribution = claim(
    "Separating the decision context $c$, decision policy $\\delta$, and execution in an LLM "
    "system enables attribution of failures to one of three specific components: signal "
    "estimation (is $c$ correctly computed?), decision policy (does $\\delta$ map $c$ to the "
    "right action?), or execution (does the chosen action perform as expected?) [@Sun2026].",
    title="Separation enables failure attribution",
)

utility_maximization = claim(
    "A common instantiation of the decision function $\\delta$ is constrained utility "
    "maximization: $\\delta(c) = a^* = \\arg\\max_{a \\in \\mathcal{F}(c)} U(a, c)$, where "
    "$U(a, c)$ is a utility function and $\\mathcal{F}(c) \\subseteq \\mathcal{A}$ is the set "
    "of feasible actions under the current context $c$. A common linear specification is "
    "$U(a, c) = R(a, c) - \\sum_k \\lambda_k C_k(a, c)$, where $R$ is reward, $C_k$ the "
    "$k$-th cost term, and $\\lambda_k$ the tradeoff weight. Alternative objectives include "
    "regret-based, constraint-based, and ranking-based formulations [@Sun2026].",
    title="Decision function as constrained utility maximization",
    background=[dc_framework_proposed],
)

framework_preserves_uncertainty = claim(
    "Making the decision interface explicit does not eliminate uncertainty: the decision "
    "context $c$ may be noisy, and the chosen action may still be executed by a stochastic "
    "generator. The benefit is attribution: once context, policy, and execution are separated, "
    "failures can be localized rather than remaining entangled inside a single model call "
    "[@Sun2026].",
    title="Explicit control preserves uncertainty but enables attribution",
    background=[dc_framework_proposed],
)

# ─── Unification claim ───────────────────────────────────────────────────────

dc_unifies_settings = claim(
    "The decision-centric abstraction $(\\mathcal{A}, c, \\delta)$ unifies familiar single-step "
    "LLM control settings such as model routing (action = which model to invoke) and adaptive "
    "inference scaling (action = which inference strategy and how much compute to allocate), "
    "and extends naturally to sequential settings where actions can change the information "
    "available for subsequent decisions [@Sun2026].",
    title="DC abstraction unifies routing, scaling, and sequential control",
    background=[dc_framework_proposed],
)

# ─── Alternative approach (implicit/prompt-based) ────────────────────────────

alt_prompt_sufficient = claim(
    "Prompt-based approaches that leave action selection implicit within a single LLM call "
    "may be sufficient for reliable LLM system control, as models become more capable and "
    "prompts can be improved with stronger engineering.",
    title="Alternative: prompt-based control may be sufficient",
)

# Contradiction: implicit prompt control vs explicit DC control
no_both_sufficient = contradiction(
    alt_prompt_sufficient,
    dc_framework_proposed,
    reason=(
        "The paper argues that the fundamental limitation of prompt-based control — "
        "assessment and action fused inside a single model call — persists regardless of "
        "model capability, making an explicit decision layer architecturally necessary rather "
        "than optional [@Sun2026]."
    ),
    prior=0.85,
)

# ─── Reasoning strategies ────────────────────────────────────────────────────

strat_separation_from_implicit_problem = support(
    [implicit_control_problem],
    dc_framework_proposed,
    reason=(
        "The decision-centric framework is directly motivated by the implicit control problem "
        "(@implicit_control_problem): because current systems entangle assessment and action in "
        "a single model call, the proposed remedy is to separate the decision-relevant signals "
        "from the policy that maps them to actions. Making the decision interface explicit "
        "addresses the core failure mode identified in @implicit_control_problem [@Sun2026]."
    ),
    prior=0.9,
)

strat_attribution_from_separation = deduction(
    [dc_framework_proposed],
    separation_enables_attribution,
    reason=(
        "Given the decision-centric framework (@dc_framework_proposed) decomposes the system "
        "into three explicit, separable components — signal estimation (building $c$), decision "
        "policy ($\\delta$), and execution — it follows by construction that any failure must "
        "originate in exactly one of these three components. Attribution is therefore possible "
        "by logical necessity of the modular decomposition, not by empirical observation "
        "[@Sun2026]."
    ),
    prior=0.99,
)

strat_unifies_from_abstraction = support(
    [dc_framework_proposed],
    dc_unifies_settings,
    reason=(
        "The abstraction $(\\mathcal{A}, c, \\delta)$ in @dc_framework_proposed is generic "
        "enough to encompass model routing (where $\\mathcal{A}$ = candidate models, $c$ = "
        "query features + quality/cost signals, $\\delta$ = constrained utility maximizer) and "
        "adaptive inference scaling (where $\\mathcal{A}$ = inference strategies, $c$ = "
        "difficulty signals + budget constraints, $\\delta$ = same utility maximizer). Both "
        "instantiate the same three-component structure, confirming unification "
        "[@Sun2026]."
    ),
    prior=0.95,
)
