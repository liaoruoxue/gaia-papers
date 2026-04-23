"""Section 5: Protocols Externalization — Interaction Structure"""

from gaia.lang import claim, setting, support, contradiction

from .motivation import (
    externalization_thesis,
    llm_baseline_limits,
)
from .s4_skills import skill_boundary_conditions, generation_to_composition

# ── Definitional settings ─────────────────────────────────────────────────
protocol_definition = setting(
    "**Protocols** are machine-readable contracts that govern discovery, invocation, "
    "delegation, and permission management between agents and external parties. "
    "They externalize the interaction structure that previously had to be negotiated "
    "through ad-hoc prompting at each exchange. Protocols specify what can be requested, "
    "how requests are formatted, what permissions are required, and how results are "
    "returned.",
    title="Protocol definition",
)

protocol_categories_def = setting(
    "Protocols are organized into four categories based on the interacting parties: "
    "(1) **agent-tool protocols** — how agents invoke tools, APIs, and external services; "
    "(2) **agent-agent protocols** — communication and delegation between multiple agents; "
    "(3) **agent-user protocols** — interaction with human users including intent capture, "
    "clarification, and approval; (4) **governance protocols** — permissions, monitoring, "
    "and verification across agent populations. Each category addresses a distinct "
    "coordination problem.",
    title="Protocol categories",
)

protocol_components_def = setting(
    "Protocols operate through three core mechanisms: (1) **intent capture and "
    "normalization** — standardizing requests into canonical forms before routing; "
    "(2) **capability discovery and tool description** — making available capabilities "
    "findable through schemas, manifests, and registries; (3) **session and lifecycle "
    "management** — tracking state across multi-turn exchanges, handling timeouts, "
    "retries, and partial failures.",
    title="Protocol core mechanisms",
)

# ── Core claims ───────────────────────────────────────────────────────────
adhoc_to_structured = claim(
    "Protocols externalize interaction structure by converting **ad-hoc coordination** "
    "into **structured exchange**: rather than relying on free-form prompting to "
    "coordinate with tools and other agents, explicit machine-readable contracts govern "
    "invocation, delegation, and permission management. This addresses the coordination "
    "problem — fragile, non-interoperable agent interactions under ad-hoc prompting "
    "[@Zhou2026].",
    title="Protocols transform ad-hoc coordination into structured exchange",
    background=[protocol_definition, llm_baseline_limits],
)

protocol_governance_benefits = claim(
    "Standardized protocols provide three governance benefits beyond basic "
    "interoperability: (1) **security** — explicit permission boundaries prevent "
    "unauthorized tool invocation or capability escalation; (2) **auditability** — "
    "machine-readable interaction logs make agent behavior inspectable; (3) **reduced "
    "vendor lock-in** — standardized interfaces decouple agent logic from specific "
    "tool implementations [@Zhou2026].",
    title="Protocol governance benefits",
    background=[protocol_categories_def],
)

protocol_skill_coupling = claim(
    "Protocols and skills are tightly coupled: skills define what capabilities "
    "are available, while protocols specify how those capabilities are invoked and "
    "what permissions are required. The skill lifecycle's discovery stage relies on "
    "protocol-defined capability manifests and schemas for findability. Conversely, "
    "protocol-defined capability boundaries constrain which skill compositions are "
    "permissible — unsafe compositions identified in skill boundary conditions are "
    "partly prevented by protocol-level permission enforcement [@Zhou2026].",
    title="Protocol-skill coupling",
    background=[protocol_definition, protocol_categories_def],
)

protocol_memory_coupling = claim(
    "Protocols couple to memory in both directions: (a) **memory → protocol** — "
    "retrieved context from memory influences which protocol path is chosen next "
    "(e.g., previously failed tool invocations inform retry strategies); (b) "
    "**protocol → memory** — tool results and approval decisions arriving through "
    "protocolized interfaces are normalized and persisted as memory state. Protocol "
    "normalization (intent capture, canonical formatting) determines what gets stored "
    "and how it is indexed [@Zhou2026].",
    title="Protocol-memory bidirectional coupling",
    background=[protocol_components_def],
)

multi_agent_protocol_necessity = claim(
    "In multi-agent systems, protocols are a **necessity** rather than a convenience: "
    "without shared interaction contracts, agents that share memory or skill resources "
    "will produce conflicts, unauthorized accesses, and silent failures. Governance "
    "protocols — permissions, conflict resolution, access quotas — become functionally "
    "equivalent to inter-process communication and operating-system controls in "
    "distributed computing [@Zhou2026].",
    title="Multi-agent protocol necessity",
    background=[protocol_categories_def],
)

alt_adhoc_prompting = claim(
    "Ad-hoc prompting can substitute for formal protocols when the number of interacting "
    "agents and tools is small enough that coordination failures are rare and detectable. "
    "In small-scale settings (single agent, few tools, human-in-the-loop oversight), "
    "the overhead of formal protocols exceeds their governance benefit.",
    title="Alternative: ad-hoc prompting sufficient at small scale",
)

# ── Contradiction: ad-hoc vs structured at scale ──────────────────────────
not_both_adhoc_and_scale = contradiction(
    adhoc_to_structured,
    alt_adhoc_prompting,
    reason=(
        "At multi-agent scale, both claims cannot hold simultaneously: "
        "@adhoc_to_structured asserts formal protocols are necessary to replace "
        "ad-hoc prompting for reliable coordination; @alt_adhoc_prompting asserts "
        "ad-hoc prompting is sufficient in some regimes. These are incompatible "
        "under the same conditions (large-scale multi-agent deployment)."
    ),
    prior=0.85,
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_adhoc_to_structured = support(
    [externalization_thesis],
    adhoc_to_structured,
    reason=(
        "The ad-hoc-to-structured transformation (@adhoc_to_structured) is the "
        "protocol-layer instance of @externalization_thesis: interaction structure "
        "is relocated from implicit model behavior (ad-hoc prompting) into explicit "
        "machine-readable contracts (defined in @protocol_definition). The coordination "
        "problem identified in @llm_baseline_limits — fragile tool interactions — "
        "is directly addressed by protocol-governed invocation."
    ),
    prior=0.85,
    background=[protocol_definition, llm_baseline_limits],
)

strat_governance = support(
    [adhoc_to_structured],
    protocol_governance_benefits,
    reason=(
        "Protocol governance benefits (@protocol_governance_benefits) follow from "
        "the structured-exchange transformation (@adhoc_to_structured) applied across "
        "the four protocol categories (described in @protocol_categories_def): explicit "
        "contracts carry permission metadata (security), create loggable interaction "
        "records (auditability), and standardize interfaces independent of "
        "implementations (reduced vendor lock-in)."
    ),
    prior=0.82,
    background=[protocol_categories_def],
)

strat_protocol_skill_coupling = support(
    [adhoc_to_structured, skill_boundary_conditions],
    protocol_skill_coupling,
    reason=(
        "Protocol-skill coupling (@protocol_skill_coupling) follows from the skill "
        "lifecycle's discovery stage requiring findable capability descriptions — "
        "exactly what protocol manifests provide (as defined in @protocol_components_def). "
        "Additionally, @skill_boundary_conditions identifies unsafe composition as "
        "a boundary condition, and protocol-level permission enforcement "
        "(from @protocol_definition) provides the mechanism to prevent it. "
        "Both directions of coupling are grounded in these definitional structures."
    ),
    prior=0.80,
    background=[protocol_definition, protocol_categories_def, protocol_components_def],
)

strat_memory_coupling = support(
    [protocol_governance_benefits, multi_agent_protocol_necessity],
    protocol_memory_coupling,
    reason=(
        "Protocol-memory coupling (@protocol_memory_coupling) is entailed by "
        "@multi_agent_protocol_necessity (protocols normalize what shared memory "
        "receives) combined with @protocol_governance_benefits (auditability requires "
        "that protocol-mediated results be persistently logged — i.e., entered into "
        "memory). The bidirectional coupling is the operational mechanism implementing "
        "both governance and continuity."
    ),
    prior=0.78,
    background=[protocol_components_def],
)

strat_necessity = support(
    [protocol_governance_benefits],
    multi_agent_protocol_necessity,
    reason=(
        "Multi-agent protocol necessity (@multi_agent_protocol_necessity) is supported "
        "by @protocol_governance_benefits: the governance benefits (security, auditability, "
        "vendor independence) are precisely what becomes critical at multi-agent scale. "
        "Without these, shared-resource conflicts (memory, skills) escalate from "
        "occasional bugs to systemic failures requiring OS-level controls."
    ),
    prior=0.82,
    background=[protocol_categories_def],
)
