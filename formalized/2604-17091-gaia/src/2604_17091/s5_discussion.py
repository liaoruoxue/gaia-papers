"""Section 5: Discussion and Key Findings"""

from gaia.lang import claim, support

from .motivation import (
    thesis_minimal_capability,
    thesis_minimal_architecture,
)

# ── Core discussion claims ────────────────────────────────────────────────────

claim_permissions_ceiling = claim(
    "Permissions define the ceiling of agent capability. What an agent can perceive, "
    "act upon, and receive feedback from directly determines the complexity of reasoning "
    "chains and the difficulty of tasks it can solve. Restricting the action boundary "
    "during the exploration phase caps the capability ceiling at system design time. "
    "An agent restricted to reading a small set of files, unable to execute code or "
    "access external information, can only operate within a truncated state space "
    "regardless of model capability. Narrowing the exploration boundary is not a "
    "path toward useful agents.",
    title="Permissions as agent capability ceiling",
)

claim_architecture_evolution_path = claim(
    "Agent self-evolution has three progressive dimensions: "
    "(1) skill consolidation — converting verified execution traces into reusable SOPs "
    "and executable code (demonstrated in GA's longitudinal study); "
    "(2) autonomous exploration — using Reflect Mode and subagent dispatch to discover "
    "new skills during idle time without user instruction; "
    "(3) architectural self-update — agents reading and modifying the core codebase "
    "itself. Minimal architecture is the necessary prerequisite for reaching "
    "dimension (3). The full validation of the path from (1) to (3) is left as an "
    "open problem.",
    title="Three-dimensional agent evolution path",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_permissions = support(
    [thesis_minimal_capability],
    claim_permissions_ceiling,
    reason=(
        "@thesis_minimal_capability identifies tool interfacing as the first density "
        "degradation point. But permissions also define the reachable state space: "
        "an agent with read-only access cannot build executable skills (dimension 1 "
        "of evolution requires code_run); an agent without web access cannot retrieve "
        "external information. The capability ceiling imposed by permissions is "
        "therefore logically prior to any density optimization [@GenericAgent2026]."
    ),
    prior=0.80,
)

strat_evolution_path = support(
    [thesis_minimal_architecture],
    claim_architecture_evolution_path,
    reason=(
        "@thesis_minimal_architecture argues a small codebase is a necessary "
        "prerequisite for self-modification. The three-dimensional path organizes "
        "progression sequentially: skill consolidation (proven empirically via "
        "nine-round evolution study), autonomous exploration (implemented via Reflect "
        "Mode), and architectural self-update (conjectured, not yet validated). "
        "The progression is logically ordered — each dimension requires the previous "
        "[@GenericAgent2026]."
    ),
    prior=0.70,
)
