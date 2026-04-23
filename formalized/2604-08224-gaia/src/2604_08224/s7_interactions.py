"""Section 7: Cross-Cutting Interactions and Parametric vs Externalized Trade-offs"""

from gaia.lang import claim, setting, support

from .motivation import externalization_thesis, three_externalization_dimensions
from .s3_memory import (
    episodic_to_skill_boundary,
    memory_as_managed_infrastructure,
    retrieval_quality_primacy,
)
from .s4_skills import skill_distillation_coupling, skill_boundary_conditions
from .s5_protocols import protocol_skill_coupling, protocol_memory_coupling
from .s6_harness import harness_observability, harness_transforms_context_management

# ── Settings ───────────────────────────────────────────────────────────────
interaction_map_def = setting(
    "The paper identifies six cross-dimension interactions between memory, skills, "
    "and protocols: (1) memory → skill: experience distillation; (2) skill → memory: "
    "execution recording; (3) skill → protocol: capability invocation; (4) protocol → skill: "
    "capability generation; (5) memory → protocol: strategy selection; "
    "(6) protocol → memory: result assimilation.",
    title="Cross-dimension interaction map",
)

parametric_externalized_tradeoffs_def = setting(
    "The parametric vs. externalized trade-off has four dimensions: "
    "(1) **update frequency** — externalized components can be updated without retraining; "
    "(2) **reusability and portability** — externalized skills and protocols transfer "
    "across agents and model versions; (3) **auditability and governance** — externalized "
    "state is inspectable and governable; (4) **latency and simplicity** — parametric "
    "knowledge is faster (no retrieval) and simpler (no infrastructure) but less "
    "flexible and auditable.",
    title="Parametric vs. externalized trade-off dimensions",
)

# ── Core claims ───────────────────────────────────────────────────────────
dimensions_not_independent = claim(
    "Memory, skills, and protocols do not operate as independent silos: the six "
    "cross-dimension interactions create a coupled system where the effectiveness "
    "of each dimension depends on the other two. In particular, skills improve through "
    "memory distillation, protocols enable skill discovery, and memory is populated "
    "through protocol-mediated tool results. Designing one dimension in isolation "
    "produces suboptimal overall system performance [@Zhou2026].",
    title="Three dimensions form a coupled system",
    background=[interaction_map_def],
)

llm_input_perspective = claim(
    "From the model's input perspective, the three dimensions have distinct roles: "
    "memory provides **contextual input** (relevant retrieved history, world-state); "
    "skills provide **instructional input** (validated procedures, decision heuristics); "
    "protocols define **action schemas** (what the model can request and how it must "
    "format requests). These roles are complementary rather than overlapping — "
    "none of the three substitutes for the others [@Zhou2026].",
    title="Distinct input roles for memory, skills, and protocols",
    background=[interaction_map_def],
)

externalized_update_advantage = claim(
    "The update-frequency advantage of externalized components over parametric "
    "knowledge is the primary reason why externalization enables personalization "
    "at scale: user-specific preferences, project conventions, and evolving domain "
    "knowledge can be updated in memory and skill stores without retraining the model "
    "weights. This decouples model improvement from knowledge freshness [@Zhou2026].",
    title="Externalization enables personalization through update decoupling",
    background=[parametric_externalized_tradeoffs_def],
)

externalized_auditability_advantage = claim(
    "The auditability advantage of externalization — externalized state is inspectable "
    "and governable — is not merely a governance nicety but a prerequisite for "
    "high-stakes deployment: in regulated domains (healthcare, finance, legal), "
    "agents must produce auditable decision trails. Parametric knowledge that "
    "cannot be inspected or attributed cannot satisfy these requirements; externalized "
    "memory, skill logs, and protocol records can [@Zhou2026].",
    title="Auditability as prerequisite for regulated deployment",
    background=[parametric_externalized_tradeoffs_def],
)

latency_simplicity_tradeoff = claim(
    "The latency-simplicity advantage of parametric knowledge (no retrieval overhead, "
    "no infrastructure) means that externalization is not always the right choice: "
    "for stable, frequently-accessed knowledge with low auditability requirements, "
    "retaining it in weights may be more efficient than externalizing it. The "
    "externalization framework is a design lens, not a mandate to externalize "
    "everything [@Zhou2026].",
    title="Parametric knowledge advantage: latency and simplicity",
    background=[parametric_externalized_tradeoffs_def],
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_not_independent = support(
    [
        episodic_to_skill_boundary,
        protocol_skill_coupling,
        protocol_memory_coupling,
    ],
    dimensions_not_independent,
    reason=(
        "The coupling claim (@dimensions_not_independent) is directly supported by "
        "three specific coupling mechanisms: @episodic_to_skill_boundary establishes "
        "memory→skill coupling (experience distillation); @protocol_skill_coupling "
        "establishes protocol↔skill coupling (discovery and permission enforcement); "
        "@protocol_memory_coupling establishes protocol↔memory coupling (result "
        "assimilation and strategy selection). Three independent coupling directions "
        "rule out the 'independent silos' alternative."
    ),
    prior=0.88,
)

strat_llm_input = support(
    [dimensions_not_independent, three_externalization_dimensions],
    llm_input_perspective,
    reason=(
        "The distinct input roles (@llm_input_perspective) follow from the coupling "
        "system (@dimensions_not_independent) and the three-dimensions taxonomy "
        "(@three_externalization_dimensions): memory addresses continuity (contextual "
        "history), skills address variance (instructional procedures), protocols address "
        "coordination (action schemas). These three problems are orthogonal, so the "
        "input roles they generate are complementary rather than overlapping."
    ),
    prior=0.82,
)

strat_update_advantage = support(
    [externalization_thesis],
    externalized_update_advantage,
    reason=(
        "The update advantage (@externalized_update_advantage) is the trade-off "
        "dimension most directly supported by @externalization_thesis: capability "
        "relocation from weights into external stores decouples knowledge freshness "
        "from model training. The trade-off framework (described in "
        "@parametric_externalized_tradeoffs_def) enumerates update frequency as the "
        "first dimension, providing definitional grounding."
    ),
    prior=0.87,
    background=[parametric_externalized_tradeoffs_def],
)

strat_auditability = support(
    [externalized_update_advantage],
    externalized_auditability_advantage,
    reason=(
        "Auditability as deployment prerequisite (@externalized_auditability_advantage) "
        "is an extension of the update-advantage argument (@externalized_update_advantage): "
        "both advantages stem from externalization making knowledge explicit and "
        "accessible rather than implicit in weights. The trade-off framework "
        "(in @parametric_externalized_tradeoffs_def) lists auditability as an explicit "
        "dimension, and regulated domains legally require auditable trails — a "
        "requirement parametric knowledge cannot satisfy by definition."
    ),
    prior=0.83,
    background=[parametric_externalized_tradeoffs_def],
)

strat_latency = support(
    [externalization_thesis],
    latency_simplicity_tradeoff,
    reason=(
        "The latency-simplicity claim (@latency_simplicity_tradeoff) is the "
        "counter-argument: @externalization_thesis frames externalization as a "
        "design choice that relocates cognitive burdens, implying tradeoffs exist. "
        "The trade-off framework (in @parametric_externalized_tradeoffs_def) includes "
        "latency and simplicity as genuine advantages of parametric knowledge, "
        "implying externalization has costs, not only benefits. The paper explicitly "
        "frames externalization as a design lens, not a mandate."
    ),
    prior=0.82,
    background=[parametric_externalized_tradeoffs_def],
)
