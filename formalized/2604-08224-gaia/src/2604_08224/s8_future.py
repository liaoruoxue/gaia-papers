"""Section 8: Future Directions and Open Challenges"""

from gaia.lang import claim, setting, question, support

from .motivation import externalization_thesis, three_externalization_dimensions
from .s2_history import era_progression_law, design_question_shift
from .s6_harness import harness_design_question_shift
from .s7_interactions import dimensions_not_independent, externalized_update_advantage

# ── Settings ───────────────────────────────────────────────────────────────
future_directions_def = setting(
    "The paper identifies eight future research directions: (1) self-evolving harnesses; "
    "(2) embodied externalization; (3) shared infrastructure across agents; "
    "(4) governance at scale; (5) planning and goal management externalization; "
    "(6) evaluation and verification externalization; (7) multi-modal externalization; "
    "(8) orchestration logic that is itself inspectable and evolving.",
    title="Eight future research directions",
)

# ── Open questions ─────────────────────────────────────────────────────────
q_self_evolving = question(
    "Can agents adaptively improve their own memory policies, skill libraries, and "
    "protocol configurations based on accumulated experience, without human-authored "
    "updates — a self-evolving harness?",
)

q_shared_infrastructure = question(
    "Can memory stores, skill registries, and protocol definitions be shared across "
    "organizations and agent populations, creating collective cognitive infrastructure "
    "analogous to the internet or software package registries?",
)

q_governance_scale = question(
    "How should permissions, conflict resolution, and integrity be managed across "
    "multi-agent systems where many agents share externalized memory and skill "
    "resources, without central coordination bottlenecks?",
)

# ── Core claims ───────────────────────────────────────────────────────────
self_evolving_harness_claim = claim(
    "Self-evolving harnesses — systems that adaptively improve their own memory "
    "policies, skill libraries, and protocol configurations based on experience — "
    "represent the natural next stage of the externalization progression. Just as "
    "the harness era externalizes the coordination of memory, skills, and protocols, "
    "the self-evolving stage would externalize the **optimization of the harness "
    "itself** into an inspectable and adaptable artifact [@Zhou2026].",
    title="Self-evolving harnesses as next externalization stage",
    background=[future_directions_def],
)

shared_infrastructure_claim = claim(
    "Shared agent infrastructure — collective memory stores, skill registries, and "
    "protocol standards accessible across organizations — would shift agent development "
    "from private scaffolding to collective cognitive infrastructure. This mirrors the "
    "historical transitions from private computing to public libraries, from private "
    "networks to the internet, and from bespoke software to package registries "
    "[@Zhou2026].",
    title="Shared infrastructure as collective cognitive commons",
    background=[future_directions_def],
)

governance_scale_challenge = claim(
    "Governance at scale — managing permissions, conflict resolution, and integrity "
    "when many agents share externalized state — is an unsolved engineering and policy "
    "problem. At single-agent scale, the harness can encode governance as static "
    "configuration; at multi-agent scale with shared resources, governance requires "
    "dynamic arbitration mechanisms comparable to operating-system concurrency controls "
    "[@Zhou2026].",
    title="Governance at scale as open problem",
    background=[future_directions_def],
)

externalization_limits_claim = claim(
    "Externalization is not a solution to all agent limitations: the framework "
    "addresses continuity, variance, and coordination problems, but does not address "
    "fundamental model capability limitations (reasoning depth, domain knowledge gaps, "
    "alignment). Externalization improves what the model can reliably do with its "
    "existing capabilities; it does not expand what the model is capable of in principle "
    "[@Zhou2026].",
    title="Externalization limits: does not address model capability gaps",
    background=[future_directions_def],
)

historical_human_parallel = claim(
    "The paper argues that the progression from weights → context → harness parallels "
    "the human cognitive history of externalization: speech → writing → printing → "
    "computation. In both cases, capability expansion came primarily from improving "
    "the external cognitive environment rather than biological/parametric capacity. "
    "This parallel grounds the prediction that LLM agent progress will continue to "
    "come primarily from infrastructure rather than model scaling [@Zhou2026].",
    title="LLM externalization parallels human cognitive history",
    background=[future_directions_def],
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_self_evolving = support(
    [era_progression_law, externalized_update_advantage],
    self_evolving_harness_claim,
    reason=(
        "Self-evolving harnesses (@self_evolving_harness_claim) follow by applying "
        "@era_progression_law to the harness itself: each era externalizes one more "
        "layer of cognitive burden; the self-evolving stage would externalize harness "
        "optimization. @externalized_update_advantage shows externalization already "
        "enables continuous updates without retraining — self-evolution is the limit "
        "of this trajectory where the harness itself becomes the updatable artifact."
    ),
    prior=0.72,
    background=[future_directions_def],
)

strat_shared_infra = support(
    [dimensions_not_independent, externalization_thesis],
    shared_infrastructure_claim,
    reason=(
        "Shared infrastructure (@shared_infrastructure_claim) follows from "
        "@dimensions_not_independent (the three dimensions are coupled and create "
        "collective value) combined with @externalization_thesis (capability lives in "
        "infrastructure, not weights) — if infrastructure is the locus of capability, "
        "sharing infrastructure is equivalent to sharing capability, making collective "
        "infrastructure a natural economic and technical incentive."
    ),
    prior=0.70,
    background=[future_directions_def],
)

strat_governance_challenge = support(
    [dimensions_not_independent],
    governance_scale_challenge,
    reason=(
        "Governance at scale (@governance_scale_challenge) follows from "
        "@dimensions_not_independent: the coupled three-dimension system requires "
        "coherent governance across all three interaction types simultaneously. "
        "At single-agent scale this is manageable; at multi-agent scale with shared "
        "resources it requires dynamic arbitration — a distributed systems problem "
        "that has not been solved for agent infrastructure."
    ),
    prior=0.78,
    background=[future_directions_def],
)

strat_limits = support(
    [three_externalization_dimensions],
    externalization_limits_claim,
    reason=(
        "Externalization limits (@externalization_limits_claim) follow from the scope "
        "of @three_externalization_dimensions: the three dimensions address continuity, "
        "variance, and coordination — specific operational problems. They do not address "
        "reasoning depth (how far a model can chain inferences), domain knowledge "
        "(what the model knows), or alignment (what the model optimizes for). These "
        "are distinct from operational problems and require different solutions."
    ),
    prior=0.83,
    background=[future_directions_def],
)

strat_historical_parallel = support(
    [era_progression_law, design_question_shift],
    historical_human_parallel,
    reason=(
        "The historical parallel (@historical_human_parallel) is supported by "
        "@era_progression_law (monotonic externalization trend in LLM agent history) "
        "and @design_question_shift (the design question shifted from 'what model?' "
        "to 'what environment?'). The parallel to human cognitive history is an "
        "inductive argument: the same externalization pattern that drove human cognitive "
        "capability expansion is observed in LLM agent development."
    ),
    prior=0.70,
    background=[future_directions_def],
)
