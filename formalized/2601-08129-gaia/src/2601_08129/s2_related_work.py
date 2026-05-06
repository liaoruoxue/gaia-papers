"""Section 2: Related Work.

Positions pressure-field coordination across four research traditions:
(1) MAS coordination theory (organizational paradigms, GPGP, SharedPlans,
self-organization), (2) FM enablement of stigmergy, (3) MAS-LLM systems
(AutoGen, MetaGPT, CAMEL, CrewAI), (4) swarm intelligence and stigmergy
(termites, ACO), and (5) decentralized optimization (potential games,
distributed gradient descent).

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 2.
"""

from gaia.lang import claim, setting

# ===========================================================================
# 2.1.1 Organizational paradigms
# ===========================================================================

claim_organizational_paradigms_assign_roles = claim(
    "**All traditional organizational MAS paradigms assign explicit "
    "roles constraining agent behavior.** Horling and Lesser "
    "[@HorlingLesser2004] surveyed nine such paradigms -- from rigid "
    "hierarchies to flexible markets -- finding that all assign "
    "explicit roles. Dignum [@Dignum2009] systematizes this tradition "
    "by defining organizational models through three dimensions: "
    "*structure* (roles and relationships), *norms* (behavioral "
    "constraints), and *dynamics* (how organizations adapt). All "
    "three dimensions require explicit specification and "
    "maintenance: designers must anticipate role interactions, "
    "encode coordination norms, and implement adaptation mechanisms.",
    title="Related: organizational MAS paradigms (9 surveyed by Horling-Lesser, systematized by Dignum) all assign explicit roles",
)

claim_pressure_field_eliminates_three_dimensions = claim(
    "**Pressure-field coordination eliminates Dignum's three "
    "organizational dimensions through gradient-based coordination.** "
    "Roles dissolve: any agent may address any high-pressure region "
    "without negotiating access rights or awaiting task assignment. "
    "Norms become implicit: the pressure function encodes what 'good' "
    "behavior means, and agents that reduce pressure are by "
    "definition norm-compliant. Dynamics emerge naturally: temporal "
    "decay continuously destabilizes the pressure landscape, forcing "
    "ongoing adaptation without explicit organizational change "
    "protocols.",
    title="Result: pressure-field eliminates structure / norms / dynamics specification (Dignum's three dimensions)",
)

claim_malone_crowston_shared_resource = claim(
    "**Malone-Crowston shared-resource pattern, instantiated.** "
    "Malone and Crowston [@MaloneCrowston1994] identify 'shared "
    "resource' management as a fundamental coordination pattern "
    "requiring protocols for access control, conflict resolution, "
    "and priority assignment. Pressure-field coordination implements "
    "this pattern with the *artifact itself* as the shared resource "
    "and pressure gradients as dependency signals: agents share read "
    "access, propose changes to high-pressure regions, and validation "
    "implicitly resolves conflicts -- only pressure-reducing patches "
    "are applied; the highest-scoring patch wins when proposals "
    "conflict.",
    title="Related: Malone-Crowston shared-resource coordination instantiated with artifact-as-resource and pressure-gradients-as-dependency-signals",
)

# ===========================================================================
# 2.1.2 GPGP and communication overhead
# ===========================================================================

claim_gpgp_message_complexity = claim(
    "**Generalized Partial Global Planning (GPGP) "
    "[@GPGP] reduces inter-agent communication from $O(n^2)$ pairwise "
    "negotiation to $O(n \\log n)$ hierarchical aggregation through "
    "summary information exchange.** Even with this reduction, "
    "explicit messages -- task announcements, commitment exchanges, "
    "schedule updates -- still introduce latency and failure points "
    "that grow with agent count $n$.",
    title="Related: GPGP reduces communication to O(n log n) but still incurs explicit-message latency and failure points",
)

claim_pressure_field_o1_overhead = claim(
    "**Pressure-field coordination achieves $O(1)$ inter-agent "
    "communication overhead.** Agents exchange *no* messages; "
    "coordination occurs entirely through shared artifact reads and "
    "writes. This eliminates the message-passing bottleneck that "
    "GPGP's $O(n \\log n)$ aggregation, $O(n^2)$ pairwise "
    "negotiation, and message-passing-coordination baselines all "
    "incur.",
    title="Result: pressure-field has O(1) inter-agent communication overhead (no messages, only shared artifact reads/writes)",
)

# ===========================================================================
# 2.1.3 SharedPlans, Joint Intentions, alignment costs
# ===========================================================================

claim_sharedplans_joint_intentions_cost = claim(
    "**SharedPlans [@SharedPlans] and Joint Intentions "
    "[@JointIntentions] require expensive mutual-belief "
    "machinery.** SharedPlans formalizes collaboration through "
    "shared mental attitudes -- mutual beliefs about goals, "
    "commitments, and action sequences. Joint Intentions adds the "
    "still-stricter requirement that team members hold mutual "
    "beliefs about the joint goal, individual commitments, and "
    "*mutual beliefs about each other's commitments* (recursively). "
    "Both frameworks require intention recognition, commitment "
    "protocols, and belief revision -- computationally expensive "
    "operations that scale poorly with agent count.",
    title="Related: SharedPlans / Joint Intentions require recursive mutual-belief machinery that scales poorly",
)

claim_pressure_alignment_replaces_intention_alignment = claim(
    "**Pressure-field coordination replaces intention alignment "
    "with pressure alignment.** Rather than reasoning about what "
    "other agents believe or intend, agents observe artifact state "
    "and pressure gradients. The shared artifact *is* the mutual "
    "belief: agents perceive the same pressure landscape without "
    "explicit belief exchange, eliminating the recursive 'I believe "
    "that you believe' regress that makes Joint Intentions "
    "computationally expensive at scale.",
    title="Result: pressure-field replaces intention alignment with pressure alignment (artifact = mutual belief)",
)

# ===========================================================================
# 2.1.4 Self-organization criteria
# ===========================================================================

setup_serugendo_four_mechanisms = setting(
    "**Serugendo et al. [@Serugendo2005] four self-organization "
    "mechanisms.** Self-organization in MAS emerges through four "
    "mechanisms: (1) *positive feedback* amplifying beneficial "
    "behaviors, (2) *negative feedback* dampening harmful "
    "behaviors, (3) *randomness* enabling exploration, and (4) "
    "*multiple interactions* allowing local behaviors to propagate "
    "globally.",
    title="Setup: Serugendo's four self-organization mechanisms (positive feedback / negative feedback / randomness / multiple interactions)",
)

setup_dewolf_holvoet_criteria = setting(
    "**De Wolf-Holvoet self-organization criteria "
    "[@DeWolfHolvoet2005].** A self-organizing system is "
    "characterized by (i) absence of external control, (ii) local "
    "interactions producing global patterns, and (iii) dynamic "
    "adaptation. They explicitly cite *gradient fields* as a self-"
    "organization design pattern.",
    title="Setup: De Wolf-Holvoet self-organization criteria (no external control / local-to-global / dynamic adaptation; gradient fields)",
)

claim_pressure_field_instantiates_four_mechanisms = claim(
    "**Pressure-field coordination instantiates all four Serugendo "
    "mechanisms.** "
    "(1) **Positive feedback**: successful patches are stored as "
    "few-shot examples ('positive pheromones'), increasing the "
    "probability of similar improvements in neighboring regions; "
    "(2) **Negative feedback**: temporal decay continuously erodes "
    "fitness so no region becomes permanently 'solved'; inhibition "
    "further dampens over-activity in recently-patched regions; "
    "(3) **Randomness**: stochastic model sampling and band "
    "escalation (Exploitation -> Balanced -> Exploration) inject "
    "controlled randomness; "
    "(4) **Multiple interactions**: each tick produces $K$ parallel "
    "patch proposals, with selection applying the best improvements.",
    title="Result: pressure-field instantiates all four Serugendo mechanisms (positive feedback / negative feedback / randomness / multiple interactions)",
)

claim_pressure_field_satisfies_dewolf_holvoet = claim(
    "**Pressure-field coordination satisfies De Wolf-Holvoet "
    "self-organization criteria.** No external controller exists -- "
    "agents observe and act autonomously based on local pressure "
    "signals. Coordination emerges from local decisions: agents "
    "reduce regional pressure through greedy actions, and global "
    "coordination arises from shared artifact state. Temporal decay "
    "provides dynamic adaptation -- fitness erodes continuously, "
    "preventing premature convergence and enabling continued "
    "refinement. Pressure-field instantiates the gradient-fields "
    "design pattern that De Wolf-Holvoet explicitly cite.",
    title="Result: pressure-field satisfies De Wolf-Holvoet criteria (no external control / local-to-global / dynamic adaptation)",
)

# ===========================================================================
# 2.1.5 Foundation-model enablement (5 capabilities)
# ===========================================================================

claim_fm_capability_1_domain_general_patches = claim(
    "**FM capability 1 -- broad pretraining enables domain-general "
    "patch proposal.** FMs' pretraining on diverse corpora (code, "
    "text, structured data) allows patch generation across artifact "
    "types without fine-tuning. A single LLM can propose meeting "
    "schedule adjustments, code refactorings, or configuration "
    "changes through the same interface (observe local context, "
    "receive pressure feedback, generate improvement). This 'universal "
    "actor' capability is what makes stigmergic coordination "
    "practical for open-ended artifact refinement.",
    title="FM enablement (1/5): broad pretraining -> domain-general patch proposal (universal actor)",
)

claim_fm_capability_2_instruction_following = claim(
    "**FM capability 2 -- instruction-following replaces action-"
    "space enumeration.** FMs operate from natural-language pressure "
    "descriptions alone. Rather than encoding 'reduce scheduling "
    "conflicts' as a formal operator with preconditions and effects, "
    "the system simply prompts: 'This time block has 3 double-"
    "bookings. Propose a schedule change to reduce conflicts.' The "
    "FM interprets this pressure signal and generates appropriate "
    "patches without designer-enumerated actions.",
    title="FM enablement (2/5): instruction-following replaces formal action enumeration",
)

claim_fm_capability_3_zero_shot_quality = claim(
    "**FM capability 3 -- zero-shot reasoning interprets quality "
    "signals.** FMs identify constraint violations, inefficiencies, "
    "and improvement opportunities from examples alone, without "
    "explicit training on domain-specific quality metrics. Conflict "
    "recognition (e.g., 'Meeting A and Meeting B both have Alice at "
    "2pm') transfers from pretraining without training on scheduling.",
    title="FM enablement (3/5): zero-shot reasoning interprets local quality signals (no domain-specific training needed)",
)

claim_fm_capability_4_in_context_pheromone = claim(
    "**FM capability 4 -- in-context learning implements pheromone "
    "memory.** Successful patches become few-shot examples in "
    "subsequent prompts, increasing the probability of similar "
    "improvements. This 'positive pheromone' effect requires no "
    "external memory system -- the prompt itself carries "
    "reinforcement signals.",
    title="FM enablement (4/5): in-context learning = pheromone memory (no external memory system needed)",
)

claim_fm_capability_5_generative_flexibility = claim(
    "**FM capability 5 -- generative flexibility enables unbounded "
    "solution spaces.** Traditional stigmergic systems (ACO "
    "[@ACO; @AntSystem], particle swarm) operate over discrete, "
    "enumerated solution spaces. FMs generate from effectively "
    "continuous spaces, proposing patches that no designer "
    "anticipated -- essential for open-ended artifact refinement "
    "where the space of valid improvements cannot be enumerated in "
    "advance.",
    title="FM enablement (5/5): generative flexibility -> unbounded patch space (vs ACO's discrete enumerated space)",
)

claim_fm_enables_summary = claim(
    "**Summary: five FM capabilities collectively enable stigmergic "
    "coordination on artifact refinement.** Domain-general patches, "
    "instruction-based operation, zero-shot quality recognition, "
    "in-context reinforcement, and generative flexibility together "
    "make stigmergic coordination practical for artifact-refinement "
    "tasks that were previously intractable. The FM-MAS synthesis "
    "is not merely additive: FMs solve the action-enumeration "
    "problem that blocked stigmergic approaches; stigmergic "
    "coordination solves the output-combination problem that limits "
    "single-FM systems.",
    title="Result: five FM capabilities collectively enable stigmergic coordination on artifact refinement",
)

# ===========================================================================
# 2.2 Multi-agent LLM systems
# ===========================================================================

claim_mas_llm_baselines_share_pattern = claim(
    "**MAS-LLM baselines share a common design pattern.** AutoGen "
    "[@AutoGen], MetaGPT [@MetaGPT], CAMEL [@CAMEL], and CrewAI "
    "[@CrewAI] all share the design pattern of **explicit "
    "orchestration through message passing, role assignment, and "
    "hierarchical task decomposition**. Specifically: AutoGen uses "
    "conversation-based message passing among customizable agents; "
    "MetaGPT encodes Standardized Operating Procedures into "
    "specialized roles (architect, engineer, QA) in an assembly-line "
    "paradigm; CAMEL uses role-playing between AI assistant and AI "
    "user with inception prompting; CrewAI defines agents with "
    "roles, goals, and backstories.",
    title="Related: AutoGen / MetaGPT / CAMEL / CrewAI all use explicit-orchestration design pattern (message passing + roles + hierarchy)",
)

claim_explicit_orchestration_scaling_failures = claim(
    "**Explicit-orchestration design pattern faces three concrete "
    "scaling failures.** (1) Central coordinators become "
    "bottlenecks (planner / manager LLM calls serialize the "
    "pipeline). (2) Message-passing overhead grows with agent count "
    "(pairwise communication is $O(n^2)$; tree-structured delegation "
    "is $O(n \\log n)$ but adds tree-depth latency). (3) Failures "
    "in manager agents cascade to all dependents.",
    title="Related: explicit-orchestration scaling failures (3 modes: bottleneck / message overhead / cascade)",
)

# ===========================================================================
# 2.3 Swarm intelligence and stigmergy
# ===========================================================================

setup_grasse_stigmergy = setting(
    "**Stigmergy: Grasse 1959 [@Grasse1959].** Stigmergy is "
    "indirect coordination through environment modification, "
    "introduced to explain termite nest-building. Termites deposit "
    "pheromone-infused material that attracts further deposits, "
    "leading to emergent construction without central planning. This "
    "directly instantiates Malone-Crowston shared-resource "
    "coordination [@MaloneCrowston1994]: pheromone trails encode "
    "dependency information about solution quality.",
    title="Setup: stigmergy (Grasse 1959) -- coordination through environment modification (termite nest-building)",
)

setup_aco_mechanisms = setting(
    "**Ant Colony Optimization (ACO) [@AntSystem; @ACO].** ACO "
    "formalizes stigmergy: artificial pheromone trails guide search "
    "through solution spaces. Key mechanisms: positive feedback "
    "(reinforcing good paths), negative feedback (pheromone "
    "evaporation), and purely local decision-making. ACO has "
    "achieved strong results on combinatorial optimization "
    "(Traveling Salesman Problem (TSP), vehicle routing, "
    "scheduling).",
    title="Setup: ACO mechanisms (positive feedback / negative feedback = evaporation / local decisions)",
)

claim_pressure_field_inherits_aco = claim(
    "**Pressure-field directly inherits stigmergic principles from "
    "ACO and generalizes beyond pathfinding.** The artifact serves "
    "as the shared environment; regional pressures are analogous to "
    "pheromone concentrations; decay corresponds to evaporation. The "
    "generalization: pressure-field applies stigmergic coordination "
    "to **arbitrary artifact refinement** (rather than ACO's path-"
    "finding) and provides **formal convergence guarantees** through "
    "the potential-game framework.",
    title="Related: pressure-field inherits stigmergy from ACO; generalizes beyond pathfinding to arbitrary artifact refinement with formal convergence guarantees",
)

# ===========================================================================
# 2.4 Decentralized optimization
# ===========================================================================

setup_potential_games = setting(
    "**Potential games (Monderer-Shapley [@PotentialGames]).** "
    "Potential games are games where individual incentives align "
    "with a global potential function. Key property: any sequence of "
    "unilateral improvements converges to a Nash equilibrium -- "
    "greedy local play achieves global coordination.",
    title="Setup: potential games (Monderer-Shapley) -- unilateral improvement converges to Nash equilibrium",
)

claim_distributed_gd_requires_protocols = claim(
    "**Distributed gradient-descent methods "
    "[@DistributedSubgradient; @DecentralizedGD] require explicit "
    "communication protocols and synchronization.** The standard "
    "approach combines local gradient steps with consensus "
    "averaging. While these methods achieve convergence rates "
    "matching centralized alternatives, the communication / "
    "synchronization overhead is *not* eliminated. Pressure-field "
    "coordination avoids explicit communication entirely (agents "
    "coordinate only through the shared artifact, $O(1)$ "
    "coordination overhead).",
    title="Related: distributed gradient descent requires communication / synchronization protocols (pressure-field eliminates them)",
)

claim_pressure_as_potential_function = claim(
    "**Pressure-field coordination instantiates potential games on "
    "LLM-based artifact refinement.** Under pressure alignment "
    "[Definition 4.1], the artifact pressure $P(s)$ acts as a "
    "potential function: local improvements by individual agents "
    "decrease global pressure. The 'game' is defined by pressure "
    "functions over quality signals, rather than explicit reward "
    "structures. This connection (extending Shoham-Leyton-Brown's "
    "[@MASBook] multi-agent-learning / game-theory analysis to LLM-"
    "based artifact refinement) provides the theoretical foundation "
    "for the convergence guarantees of Theorems 5.1 and 5.5.",
    title="Related: pressure-field instantiates potential-game framework on LLM artifact refinement (P(s) is the potential function)",
)

__all__ = [
    "claim_organizational_paradigms_assign_roles",
    "claim_pressure_field_eliminates_three_dimensions",
    "claim_malone_crowston_shared_resource",
    "claim_gpgp_message_complexity",
    "claim_pressure_field_o1_overhead",
    "claim_sharedplans_joint_intentions_cost",
    "claim_pressure_alignment_replaces_intention_alignment",
    "setup_serugendo_four_mechanisms",
    "setup_dewolf_holvoet_criteria",
    "claim_pressure_field_instantiates_four_mechanisms",
    "claim_pressure_field_satisfies_dewolf_holvoet",
    "claim_fm_capability_1_domain_general_patches",
    "claim_fm_capability_2_instruction_following",
    "claim_fm_capability_3_zero_shot_quality",
    "claim_fm_capability_4_in_context_pheromone",
    "claim_fm_capability_5_generative_flexibility",
    "claim_fm_enables_summary",
    "claim_mas_llm_baselines_share_pattern",
    "claim_explicit_orchestration_scaling_failures",
    "setup_grasse_stigmergy",
    "setup_aco_mechanisms",
    "claim_pressure_field_inherits_aco",
    "setup_potential_games",
    "claim_distributed_gd_requires_protocols",
    "claim_pressure_as_potential_function",
]
