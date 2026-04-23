"""Section 6: Harness Engineering — Coordinating Runtime Environment"""

from gaia.lang import claim, setting, support

from .motivation import (
    externalization_thesis,
    three_externalization_dimensions,
    representational_transformation_claim,
)
from .s3_memory import memory_as_managed_infrastructure
from .s4_skills import packaged_expertise_claim
from .s5_protocols import adhoc_to_structured, multi_agent_protocol_necessity

# ── Definitional settings ─────────────────────────────────────────────────
harness_definition = setting(
    "The **harness** is the engineering layer that hosts memory, skills, and protocols "
    "at runtime. It is not a fourth kind of externalization but the coordinating "
    "infrastructure that makes the three externalization dimensions operate together. "
    "The harness provides: agent loop and control flow, sandboxing and execution "
    "isolation, human oversight and approval gates, observability and structured "
    "feedback, configuration, permissions and policy encoding, and context budget "
    "management.",
    title="Harness definition",
)

harness_six_dimensions = setting(
    "Harness design is analyzed along six analytical dimensions: "
    "(1) **agent loop and control flow** — the sequence of reasoning and action cycles "
    "the agent executes; (2) **sandboxing and execution isolation** — constraining "
    "what the agent can access or modify in the execution environment; "
    "(3) **human oversight and approval gates** — intervention points where humans "
    "validate or override agent decisions; (4) **observability and structured feedback** "
    "— logging, tracing, and improvement signals from execution; "
    "(5) **configuration, permissions, and policy encoding** — governance rules and "
    "access control over agent resources; (6) **context budget management** — "
    "allocating scarce token resources across competing needs within a session.",
    title="Six harness design dimensions",
)

harness_exemplars_def = setting(
    "Representative harness systems include: SWE-agent and OpenHands (coding harnesses "
    "that manage file systems, test runners, and code review loops); Deep Research "
    "systems (research harnesses that orchestrate search, synthesis, and citation); "
    "LangGraph, CrewAI (general orchestration frameworks providing declarative "
    "control flow); Reflexion and Voyager (harnesses with persistent memory and "
    "skill-building feedback loops).",
    title="Harness exemplar systems",
)

# ── Core claims ───────────────────────────────────────────────────────────
harness_not_fourth_dimension = claim(
    "The harness is **not a fourth externalization dimension** but the runtime "
    "environment that coordinates the three dimensions (memory, skills, protocols). "
    "While memory, skills, and protocols each relocate specific cognitive burdens, "
    "the harness provides the execution substrate, control logic, and governance "
    "mechanisms that allow them to function together as a coherent system [@Zhou2026].",
    title="Harness as coordinator, not fourth dimension",
    background=[harness_definition, harness_six_dimensions],
)

harness_transforms_context_management = claim(
    "Context budget management — allocating finite token capacity across memory "
    "retrieval, skill instructions, protocol schemas, and active reasoning — is "
    "a harness function that determines which externalized knowledge reaches the "
    "model at each step. The harness does not merely pass through externalized "
    "content; it selects, compresses, and prioritizes it under the context constraint, "
    "making context budget management a first-class design dimension [@Zhou2026].",
    title="Context budget management as harness function",
    background=[harness_six_dimensions],
)

harness_human_oversight = claim(
    "Human oversight and approval gates in the harness are not optional safety "
    "additions but structural components that enable agents to take high-stakes "
    "actions: by inserting human approval checkpoints at defined decision boundaries, "
    "the harness expands the action space agents can operate in (irreversible actions "
    "become permissible when a human approval gate precedes them) while limiting "
    "liability. Systems like Deep Research implement multi-level approval gates as "
    "first-class harness components [@Zhou2026].",
    title="Human oversight gates enable expanded agent action space",
    background=[harness_six_dimensions],
)

harness_observability = claim(
    "Observability and structured feedback in the harness serve two functions: "
    "(a) **retrospective** — execution traces become input to memory (episodic) and "
    "skill distillation pipelines; (b) **prospective** — real-time monitoring enables "
    "error detection, timeout handling, and dynamic re-planning. Without structured "
    "observability, the feedback loops between memory, skills, and protocols cannot "
    "close — the harness becomes a one-shot executor rather than a self-improving "
    "system [@Zhou2026].",
    title="Harness observability enables memory-skill feedback loops",
    background=[harness_six_dimensions],
)

harness_design_question_shift = claim(
    "The existence of the harness layer confirms the design-question shift described "
    "in the historical arc: mature agent development is primarily harness engineering "
    "— designing the environment in which the model operates — rather than model "
    "engineering. The harness encodes the agent's goals, capabilities, safety "
    "constraints, and feedback loops, leaving the model to perform bounded inference "
    "within a well-specified environment [@Zhou2026].",
    title="Harness engineering as mature agent development",
    background=[harness_definition, harness_exemplars_def],
)

sandboxing_isolation = claim(
    "Sandboxing and execution isolation in the harness are necessary for agents that "
    "take real-world actions (file writes, code execution, web requests): without "
    "isolation, agent errors and adversarial inputs can produce irreversible side "
    "effects in the host environment. Coding harnesses (SWE-agent, OpenHands) "
    "implement containerized execution environments as standard practice, not as "
    "optional hardening [@Zhou2026].",
    title="Sandboxing as necessary harness component",
    background=[harness_six_dimensions, harness_exemplars_def],
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_not_fourth = support(
    [three_externalization_dimensions],
    harness_not_fourth_dimension,
    reason=(
        "The claim that harness is not a fourth dimension (@harness_not_fourth_dimension) "
        "follows from @three_externalization_dimensions: the three dimensions address "
        "specific cognitive burdens (continuity, variance, coordination) through "
        "representational transformation. The harness (defined in @harness_definition) "
        "provides the execution substrate enabling all three but does not itself "
        "relocate a cognitive burden — it coordinates the relocation performed by "
        "the three dimensions."
    ),
    prior=0.88,
    background=[harness_definition, harness_six_dimensions],
)

strat_context_budget = support(
    [harness_not_fourth_dimension, representational_transformation_claim],
    harness_transforms_context_management,
    reason=(
        "Context budget management (@harness_transforms_context_management) is a "
        "direct instance of @representational_transformation_claim: the harness "
        "transforms which externalized knowledge the model receives, restructuring "
        "the problem representation at each step. Since the harness coordinates all "
        "three externalization dimensions (@harness_not_fourth_dimension), context "
        "budget management is its primary mechanism of representational control."
    ),
    prior=0.85,
    background=[harness_six_dimensions],
)

strat_oversight = support(
    [harness_not_fourth_dimension],
    harness_human_oversight,
    reason=(
        "Human oversight gates (@harness_human_oversight) follow from the harness "
        "role as coordinator (@harness_not_fourth_dimension): the harness encodes "
        "governance mechanisms for when the agent's own reasoning is insufficient. "
        "Approval gates are listed as an explicit harness dimension (in @harness_six_dimensions), "
        "and the argument that they expand rather than restrict action space follows "
        "from the harness's function of enabling high-stakes operations safely."
    ),
    prior=0.80,
    background=[harness_six_dimensions],
)

strat_observability = support(
    [memory_as_managed_infrastructure, packaged_expertise_claim],
    harness_observability,
    reason=(
        "Harness observability (@harness_observability) is jointly supported by: "
        "@memory_as_managed_infrastructure (managed memory requires execution traces "
        "to populate episodic records) and @packaged_expertise_claim (skill "
        "distillation requires structured execution logs to extract reusable procedures). "
        "Observability is listed as an explicit harness dimension (in @harness_six_dimensions). "
        "Without structured feedback, the feedback loops between execution and "
        "infrastructure improvement cannot close."
    ),
    prior=0.83,
    background=[harness_six_dimensions],
)

strat_design_question = support(
    [harness_not_fourth_dimension, externalization_thesis],
    harness_design_question_shift,
    reason=(
        "The harness-as-design-center claim (@harness_design_question_shift) follows "
        "from @harness_not_fourth_dimension (the harness coordinates all externalization) "
        "and @externalization_thesis (agent progress is driven by infrastructure rather "
        "than weight changes). If progress comes from infrastructure and the harness is "
        "the infrastructure's coordinator, then harness engineering is the primary "
        "locus of agent progress. Exemplar systems (in @harness_exemplars_def) "
        "confirm this by demonstrating that mature agents are primarily harness designs."
    ),
    prior=0.82,
    background=[harness_exemplars_def],
)

strat_sandboxing = support(
    [multi_agent_protocol_necessity],
    sandboxing_isolation,
    reason=(
        "Sandboxing necessity (@sandboxing_isolation) is supported by "
        "@multi_agent_protocol_necessity (multi-agent systems require OS-level controls; "
        "sandboxing is the execution-side counterpart to protocol-level permission "
        "enforcement). The harness dimensions framework (in @harness_six_dimensions) "
        "lists isolation as an explicit dimension, and exemplar systems "
        "(in @harness_exemplars_def) — SWE-agent and OpenHands — confirm that "
        "containerized execution is standard practice."
    ),
    prior=0.85,
    background=[harness_six_dimensions, harness_exemplars_def],
)
