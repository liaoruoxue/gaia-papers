"""Section 2: Algorithm and System Design"""

from gaia.lang import claim, setting, support, deduction, contradiction

from .motivation import (
    emergent_coordination_claim,
    framework_overview,
)

# --- Settings (formal definitions/architectural facts) ---

six_node_loop = setting(
    "The ScienceClaw + Infinite system is organized as a six-node ecosystem loop: "
    "(1) agents invoke skills, (2) computations produce artifacts, (3) a shared DAG storage "
    "maintains a global need index, (4) a figure renderer produces visualizations, "
    "(5) the Infinite platform handles publication, and (6) community feedback steers "
    "subsequent cycles.",
    title="Six-node ecosystem loop architecture",
)

agent_profile_definition = setting(
    "Each ScienceClaw agent is instantiated from a declarative JSON profile encoding "
    "research interests and preferred tool domains. Profiles drive tool selection without "
    "a routing table or hardcoded decision tree — tool chains emerge from the agent's "
    "interpretation of its scientific profile.",
    title="Agent profile definition",
)

skill_registry_definition = setting(
    "The open skill registry contains over 300 interoperable scientific skills organized "
    "into nine domain families spanning materials science, protein design, chemistry, "
    "genomics, and music analysis. Skills are composable: each takes structured JSON input "
    "and produces structured JSON output, enabling sequential chaining.",
    title="Open skill registry definition",
)

artifact_schema_definition = setting(
    "Each artifact in the system carries: a UUID4 identifier, a controlled-vocabulary type "
    "tag, a SHA-256 content hash for immutability, and parent artifact IDs forming a "
    "directed acyclic graph (DAG). The global index stores metadata-only entries enabling "
    "cross-agent scanning without full artifact retrieval.",
    title="Artifact schema definition",
)

pressure_scoring_definition = setting(
    "The ArtifactReactor ranks unfulfilled information needs using a pressure score combining "
    "four factors: novelty (how new the need is relative to existing artifacts), centrality "
    "(how many downstream artifacts depend on it), depth (how deep in the DAG it sits), "
    "and age (how long the need has been open). Higher pressure needs are resolved first.",
    title="Pressure scoring formula definition",
)

memory_stores_definition = setting(
    "Persistent agent memory is maintained across three coordinated stores: "
    "(1) AgentJournal — an append-only JSONL log of all actions and observations, "
    "(2) InvestigationTracker — a JSON structure of active and completed investigations, "
    "(3) KnowledgeGraph — a semantic graph of concept nodes with typed edges. "
    "Together these enable cumulative investigation across autonomous cycles.",
    title="Three memory store definitions",
)

heartbeat_definition = setting(
    "The autonomous heartbeat daemon executes a full investigation cycle every six hours, "
    "following five sequential steps: (1) observe community feed, (2) check for human "
    "redirect interventions, (3) detect knowledge gaps, (4) generate hypotheses and run "
    "the investigation pipeline, (5) publish findings and engage with peers. Human redirect "
    "actions take precedence over normal pressure scoring.",
    title="Heartbeat cycle definition",
)

infinite_data_model = setting(
    "The Infinite platform uses a PostgreSQL backend with a Next.js 14 frontend. Posts carry "
    "typed fields (hypothesis, method, findings, dataSources, openQuestions, toolsUsed) and "
    "link to artifact metadata (ID, type, skill, producerAgent, parentArtifactIds). "
    "Machine-readable discourse relations between posts are typed: cite, contradict, extend, replicate.",
    title="Infinite platform data model",
)

karma_tiers = setting(
    "The Infinite governance system assigns users to karma-based tiers: "
    "Banned (κ ≤ -100), Shadowban, Probation, Active, Trusted (κ ≥ 200). "
    "Karma accrues proportionally to artifact chain depth — deeper provenance yields higher "
    "karma, greater platform influence, and relaxed rate limits. "
    "Rate limiting and proof-of-capability validation prevent abuse.",
    title="Karma tier governance definition",
)

llm_backend = setting(
    "The primary language model backend for ScienceClaw agents is Claude Opus 4.6/4.5 "
    "(Anthropic), with the system configurable to use OpenAI or HuggingFace models. "
    "Agent reasoning and tool selection are performed by the LLM with no hardcoded routing.",
    title="LLM backend specification",
)

# --- Claims about system design properties ---

agent_diversity_claim = claim(
    "Two different ScienceClaw agents given the same scientific topic approach it from "
    "systematically different angles because their JSON profiles encode distinct research "
    "interests and preferred tool domains, making profile diversity a prerequisite for "
    "emergent multi-perspective discovery [@Wang2025].",
    title="Agent diversity from profile differences",
)

strat_diversity = support(
    [framework_overview],
    agent_diversity_claim,
    reason=(
        "The framework overview (@framework_overview) establishes that agents are instantiated "
        "from declarative JSON profiles. Because each profile encodes distinct research interests "
        "and preferred tool domains, and because no routing table governs tool selection, "
        "two agents with different profiles will invoke different skill chains even when "
        "investigating the same topic. Profile diversity is therefore structurally necessary "
        "for the multi-perspective convergence that constitutes emergent discovery."
    ),
    prior=0.9,
    background=[agent_profile_definition],
)

artifact_immutability_claim = claim(
    "Artifact immutability in ScienceClaw is enforced by SHA-256 content hashing: once an "
    "artifact is written, its content hash is stored alongside it, and any post-hoc "
    "modification would change the hash, breaking parent-lineage links in the DAG. "
    "This makes the full computational provenance tamper-evident [@Wang2025].",
    title="Artifact immutability via SHA-256",
)

strat_immutability = support(
    [framework_overview],
    artifact_immutability_claim,
    reason=(
        "The framework overview (@framework_overview) establishes the artifact layer as a "
        "core component. The artifact schema (background) specifies that every artifact carries "
        "a SHA-256 content hash and parent artifact IDs. By the properties of cryptographic "
        "hash functions, any modification to artifact content changes the hash. Since the stored "
        "hash is the integrity check, modification is detectable. The DAG structure therefore "
        "provides tamper-evident provenance by construction — this follows directly from the "
        "SHA-256 design choice in the artifact schema."
    ),
    prior=0.95,
    background=[artifact_schema_definition],
)

multiparent_synthesis_claim = claim(
    "The ArtifactReactor's multi-parent synthesis mechanism enables asynchronous cross-agent "
    "collaboration: peer agents discover each other's open information needs through the "
    "global index and produce synthesized artifacts that record all contributing agents as "
    "parents in the DAG, thereby attributing and integrating independent lines of work "
    "without requiring prior agreement between agents [@Wang2025].",
    title="Multi-parent synthesis for asynchronous collaboration",
)

strat_multiparent = support(
    [framework_overview],
    multiparent_synthesis_claim,
    reason=(
        "The framework overview (@framework_overview) establishes that coordination is "
        "plannerless. The artifact schema (background) allows multiple parent IDs per artifact, "
        "enabling synthesis from multiple upstream sources. The pressure scoring mechanism "
        "(background) directs agents toward high-priority unfulfilled needs. Together: an agent "
        "scans the global index for needs, finds a peer's open need, produces a fulfillment "
        "artifact recording both original and fulfilling agents as parents, completing "
        "cross-agent synthesis without any pre-coordination message passing."
    ),
    prior=0.88,
    background=[artifact_schema_definition, pressure_scoring_definition],
)

mutation_layer_claim = claim(
    "The autonomous mutation layer actively prunes the expanding artifact DAG by identifying "
    "and resolving conflicting or redundant workflows, preventing unbounded DAG growth and "
    "maintaining coherence as more agents contribute artifacts over time [@Wang2025].",
    title="Mutation layer for DAG coherence",
)

strat_mutation = support(
    [framework_overview],
    mutation_layer_claim,
    reason=(
        "The framework overview (@framework_overview) describes the mutation layer as a core "
        "component. Because each artifact carries parent lineage and a controlled-vocabulary "
        "type tag (background: artifact schema), the mutation layer can identify artifacts "
        "of the same type that share overlapping inputs, flag them as redundant, and "
        "selectively prune or merge them. Without this layer, the DAG grows combinatorially "
        "as independent agents add artifacts; the mutation layer is necessary for "
        "long-run operational coherence."
    ),
    prior=0.82,
    background=[artifact_schema_definition],
)

community_feedback_loop_claim = claim(
    "Community feedback on the Infinite platform (votes, typed post-links such as contradict "
    "and extend, and human redirect actions) directly steers subsequent autonomous "
    "investigation cycles by influencing agent priority scoring — making the system "
    "semi-open to human direction without requiring continuous human oversight [@Wang2025].",
    title="Community feedback loop steering investigation",
)

strat_feedback = support(
    [framework_overview],
    community_feedback_loop_claim,
    reason=(
        "The framework overview (@framework_overview) describes Infinite as the publication "
        "and feedback component. The heartbeat definition (background) specifies that step 2 "
        "of every autonomous cycle checks for human redirect interventions taking precedence "
        "over normal scoring. The karma governance (background) links community engagement to "
        "platform influence. The Infinite data model (background) provides typed discourse "
        "links (contradict, extend) encoding peer critique in machine-readable form. "
        "The combination creates a feedback path from community engagement to agent "
        "behavior without requiring synchronous human presence."
    ),
    prior=0.85,
    background=[heartbeat_definition, karma_tiers, infinite_data_model],
)

plannerless_coordination_design_claim = claim(
    "The ArtifactReactor implements plannerless coordination via two complementary signals: "
    "(1) explicit need broadcasting, where agents post unsatisfied information needs to the "
    "global index, and (2) implicit schema-overlap matching, where the system automatically "
    "triggers multi-parent synthesis when compatible peer artifacts share overlapping schemas. "
    "Loop prevention is achieved by tracking consumed artifact IDs [@Wang2025].",
    title="ArtifactReactor plannerless coordination mechanism",
)

strat_plannerless = deduction(
    [framework_overview],
    plannerless_coordination_design_claim,
    reason=(
        "The framework overview (@framework_overview) describes the ArtifactReactor as the "
        "coordination engine. The pressure scoring definition (background) specifies the "
        "mechanism for explicit need broadcasting and priority ranking. The artifact schema "
        "(background) provides the controlled-vocabulary type tags necessary for schema-overlap "
        "matching. The combination of these two mechanisms — explicit needs and implicit schema "
        "matching — constitutes the complete ArtifactReactor coordination protocol as described "
        "in the paper. Loop prevention follows from consumed-ID tracking."
    ),
    prior=0.95,
    background=[pressure_scoring_definition, artifact_schema_definition],
)

# Contradiction: central coordination vs plannerless coordination
central_coordination_necessary = claim(
    "Central coordination — where a planner explicitly assigns tasks to agents — is "
    "necessary for multi-agent convergence in distributed scientific investigation.",
    title="Central coordination necessity claim (alternative)",
)

not_both_coord = contradiction(
    central_coordination_necessary,
    emergent_coordination_claim,
    reason=(
        "If plannerless emergent coordination is sufficient for multi-agent convergence "
        "(@emergent_coordination_claim), then central task assignment is not necessary. "
        "The two claims cannot both be true: either central coordination is required "
        "(negating emergent sufficiency) or it is not (affirming plannerless sufficiency)."
    ),
    prior=0.92,
)
