"""Section 4: Related Work -- existing MAS frameworks, what they
provide, and the three structural gaps OMC fills.

Source: Yu et al. 2026 [@Yu2026OMC], Section 4 + Table 4.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Three categorical dimensions: heterogeneity, coordination, evolution
# ---------------------------------------------------------------------------

setup_three_related_work_dimensions = setting(
    "**Three dimensions of organising related work.** Yu et al. "
    "organise prior MAS work along three dimensions corresponding "
    "to the core challenges of AI organisation design: (1) how to "
    "manage heterogeneous agents under a unified abstraction; "
    "(2) how to coordinate dynamic task execution; (3) how to "
    "enable persistent self-improvement.",
    title="Setup: three related-work dimensions (heterogeneity / coordination / evolution)",
)

# ---------------------------------------------------------------------------
# Dimension 1: heterogeneity and runtime abstraction
# ---------------------------------------------------------------------------

claim_heterogeneity_only_at_model_level = claim(
    "**Existing heterogeneous MAS achieve heterogeneity only at the "
    "model level.** Magentic-One [@MagenticOne] and OWL [@OWL] use "
    "specialised orchestrators; X-MAS [@XMAS] and MacNet [@MacNet] "
    "show that heterogeneous DAG topologies outperform homogeneous "
    "baselines; OS-level approaches [@AgentForge; @AIOS] manage "
    "agents as scheduled processes. However, in all of these "
    "frameworks heterogeneity is limited to the *model* (different "
    "LLMs in different roles) -- all agents still share the same "
    "execution runtime. There is no formal substitutable contract "
    "that decouples agent identity from runtime.",
    title="Related: existing heterogeneous MAS support model-level diversity but share a single execution runtime",
)

claim_protocol_and_marketplace_landscape = claim(
    "**Tool-level protocols and platforms exist but no agent-"
    "package marketplace.** On the supply side, MCP [@MCP] and A2A "
    "[@A2A] standardise tool integration; platforms such as "
    "Cerebrum [@Cerebrum], AgentStore [@AgentStore], and "
    "AgentScope [@AgentScope] host community agents and tool "
    "catalogues [@SkillsMP; @MCPZoo]. These ecosystems handle "
    "*tool*-level composition well, but none offers a marketplace "
    "where complete agent packages (skills, tools, scripts, and "
    "persona) can be recruited into a *persistent organisation* "
    "with managed lifecycles.",
    title="Related: existing protocols/marketplaces handle tool composition; none offers complete agent-package recruitment",
)

claim_team_composition_spectrum = claim(
    "**Team composition ranges from fully fixed to fully dynamic, "
    "with no founding-team bootstrap.** Existing MAS span fully "
    "fixed teams [@MagenticOne; @OWL] to fully dynamic agent "
    "generation [@EvoMAC]. Scaling-law studies suggest compact "
    "core teams work best [@MacNet]. Paperclip [@Paperclip] places "
    "the human in a strategic-director role but provides no "
    "founding C-suite to bootstrap from. None addresses cold-start "
    "while supporting on-demand specialist recruitment.",
    title="Related: team composition spectrum (fixed to dynamic) lacks founding-team bootstrap + on-demand specialist recruitment",
)

claim_omc_fills_heterogeneity_gap = claim(
    "**OMC fills the three heterogeneity gaps simultaneously.** "
    "(G1) The Container + Talent abstraction decouples execution "
    "containers from capabilities so heterogeneous backends "
    "(LangGraph, Claude CLI, script-based) coexist within a single "
    "dispatch loop. (G2) The Talent Market provides verified, "
    "complete agent packages that can be recruited on demand. (G3) "
    "A founding C-suite (HR, EA, COO, CSO) handles cold start "
    "while the CEO recruits domain specialists as projects require. "
    "Six typed organisational interfaces play the role of the "
    "*harness* abstraction in agent engineering [@ClaudeCode], "
    "providing the formal substitutable contract that prior work "
    "lacks.",
    title="Related-work synthesis: OMC simultaneously fills heterogeneity / supply / cold-start gaps",
)

# ---------------------------------------------------------------------------
# Dimension 2: dynamic task decomposition and coordination
# ---------------------------------------------------------------------------

claim_dynamic_decomposition_landscape = claim(
    "**Dynamic task decomposition exists but lacks formal "
    "guarantees.** Several systems adapt task decomposition at "
    "runtime [@TDAG; @PlanAndAct] or evolve workflow topologies "
    "through code search [@AFlow] or test-time self-evolution "
    "[@EvoMAC]. Existing platforms manage tasks via ticket-based "
    "inheritance [@Paperclip], pipeline abstractions "
    "[@AgentScope], or hierarchical sub-goal formulation "
    "[@AgentOrchestra]. Yet none of these systems can expand the "
    "task tree at runtime *and* simultaneously provide formal "
    "guarantees on termination or deadlock-freedom under dynamic "
    "decomposition.",
    title="Related: dynamic task decomposition exists but no system provides formal completion guarantees under dynamic expansion",
)

claim_omc_fills_coordination_gap = claim(
    "**OMC's E2R tree search + DAG execution layer fills the "
    "coordination gap.** Subtasks are created on the fly with "
    "explicit dependency tracking; results are validated by an "
    "explicit review gate before propagating downstream; failed "
    "tasks are retried with a circuit breaker that escalates after "
    "repeated failures; an FSM with AND-tree semantics guarantees "
    "every task reaches a terminal state. No competing system in "
    "the architectural comparison (Table 4) provides this "
    "combination of dynamic expansion + formal completion "
    "guarantees.",
    title="Related-work synthesis: OMC supplies formal termination / deadlock-freedom under dynamic task-tree expansion",
)

# ---------------------------------------------------------------------------
# Dimension 3: self-improving and self-evolving agents
# ---------------------------------------------------------------------------

claim_individual_evolution_landscape = claim(
    "**Individual-level self-improvement is well studied.** Agents "
    "can self-improve through iterative playbook updates [@ACE], "
    "meta-agent code generation [@ADAS], induction of reusable "
    "routines from experience [@AgentWorkflowMemory], or meta-"
    "cognitive learning. Textual back-propagation can evolve "
    "agents and their topologies [@EvoMAC].",
    title="Related: individual-agent self-improvement well-developed (playbook updates / meta-agents / workflow memory)",
)

claim_organisation_evolution_underdeveloped = claim(
    "**Organisation-level evolution is underdeveloped.** Some "
    "systems evolve agent connections [@EvoMAC] or learn "
    "orchestration via RL [@EvolvingOrchestration], but these "
    "adaptations rarely persist *across* projects. Paperclip "
    "[@Paperclip] supports runtime skill injection but has no "
    "structured performance management. No comparison system "
    "couples individual self-evolution with persistent "
    "organisation-level evolution.",
    title="Related: organisation-level evolution lacks cross-project persistence and structured performance management",
)

claim_omc_fills_evolution_gap = claim(
    "**OMC closes the evolution loop at three levels.** "
    "(E1) **Individually** -- agents refine working principles "
    "through CEO one-on-ones and post-task self-reflection. "
    "(E2) **Organisationally** -- project retrospectives produce "
    "updated SOPs that are automatically injected into future "
    "agents' contexts, accumulating across projects. "
    "(E3) **Systemically** -- a formal HR pipeline (periodic "
    "evaluations every 3 projects, PIP after 3 consecutive "
    "failures, automated offboarding after 1 PIP failure) creates "
    "real consequences that make improvement non-optional. The "
    "authors are not aware of prior work that applies structured "
    "HR protocols to AI agent lifecycle management.",
    title="Related-work synthesis: OMC closes individual + organisational + systemic evolution loops",
)

# ---------------------------------------------------------------------------
# Table 4: architectural comparison across systems
# ---------------------------------------------------------------------------

claim_table_4_architectural_comparison = claim(
    "**Table 4: Architectural comparison across systems.**\n\n"
    "| System | Design Paradigm | Exec. Model | Agent Contract | State Mgmt. | Multi-Exec. | Agent Source | Self-Evol. | Org. Evol. |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
    "| **OMC (ours)** | **Organisation** | **On-demand** | **6 typed interfaces** | **Disk** | **Multi-family** | **Talent Market** | **Yes** | **Yes** |\n"
    "| MetaGPT [@MetaGPT] / ChatDev [@ChatDev] | SOP pipeline | Sequential | Implicit (SOP) | In-memory | No | Prompt-defined | No | No |\n"
    "| AutoGen [@AutoGen] / LangGraph [@LangGraph] | Message graph | Event/Graph | Callbacks | Checkpoints | No | Developer-defined | No | No |\n"
    "| CrewAI [@CrewAI] / Agno [@Agno] | Role framework | Seq./parallel | Class inheritance | App-defined | No | Developer-defined | No | No |\n"
    "| OpenHands [@OpenHands] | Sandbox | Agent loop | Built-in runtime | Sandboxed | No | Built-in | No | No |\n"
    "| AIOS [@AIOS] | OS kernel | Scheduled | OS syscalls | OS-managed | No | Registry | No | No |\n"
    "| AgentScope [@AgentScope] | Distributed actors | Distributed | Partial | App-defined | No | Developer-defined | No | No |\n"
    "| Paperclip [@Paperclip] | Orchestrator | Ticket-based | Strategic director | App-defined | Multi-family | Prompt-defined | No | No |\n\n"
    "Three structural gaps emerge: (Gap 1) heterogeneity + runtime "
    "abstraction -- few support multiple agent families, none "
    "offers a formal substitutable contract; (Gap 2) dynamic task "
    "coordination -- no system provides provable termination + "
    "deadlock-freedom under dynamic task-tree expansion; (Gap 3) "
    "self- and organisation-level evolution -- no other system "
    "implements both.",
    title="Table 4: architectural comparison across 8 systems exposing three structural gaps",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Table 4 (page 19)",
        "caption": "Table 4: Architectural comparison across MAS systems (8 dimensions, 8 systems).",
    },
)

claim_three_structural_gaps_summary = claim(
    "**Three structural gaps from Table 4.** "
    "(Gap 1) **Heterogeneity / runtime abstraction** -- most "
    "frameworks couple agents to the platform through implicit "
    "mechanisms (SOPs, callbacks, class inheritance); no formal "
    "substitutable contract decouples identity from runtime. "
    "(Gap 2) **Dynamic task coordination** -- existing systems "
    "either hardcode workflow graphs or adapt decomposition at "
    "runtime without formal completion guarantees. (Gap 3) **Self- "
    "and organisation-level evolution** -- no other system "
    "implements both individual self-evolution and organisation-"
    "level evolution; existing frameworks treat agents as stateless "
    "executors.",
    title="Related-work synthesis: three structural gaps -- heterogeneity / coordination / evolution",
)

# ---------------------------------------------------------------------------
# Implicit competing assumptions in the literature
# ---------------------------------------------------------------------------

claim_lit_fixed_team_assumption = claim(
    "**Implicit literature assumption: fixed team structure is "
    "sufficient for production-grade MAS.** Frameworks such as "
    "MetaGPT [@MetaGPT] / ChatDev [@ChatDev] / CrewAI [@CrewAI] / "
    "Magentic-One [@MagenticOne] are built on the design "
    "assumption that hardcoding a team of fixed roles + fixed "
    "runtime is sufficient for production-grade MAS, with team "
    "composition and runtime fixed before the project begins.",
    title="Lit assumption: fixed team structure (composition + runtime) is sufficient for production-grade MAS",
)

claim_lit_tightly_coupled_coordination = claim(
    "**Implicit literature assumption: MAS coordination requires "
    "tightly coupled bespoke logic.** Existing orchestrators "
    "[@CrewAI; @AutoGen; @MagenticOne] use ad-hoc orchestration "
    "code (callbacks, class inheritance, framework-specific "
    "message graphs) tightly bound to a particular runtime. The "
    "implicit assumption is that decoupling identity from runtime "
    "via a typed substitutable contract is impractical or "
    "incompatible with the depth of integration MAS coordination "
    "needs.",
    title="Lit assumption: MAS coordination requires tightly coupled bespoke orchestration logic (decoupling is impractical)",
)

__all__ = [
    "setup_three_related_work_dimensions",
    "claim_heterogeneity_only_at_model_level",
    "claim_protocol_and_marketplace_landscape",
    "claim_team_composition_spectrum",
    "claim_omc_fills_heterogeneity_gap",
    "claim_dynamic_decomposition_landscape",
    "claim_omc_fills_coordination_gap",
    "claim_individual_evolution_landscape",
    "claim_organisation_evolution_underdeveloped",
    "claim_omc_fills_evolution_gap",
    "claim_table_4_architectural_comparison",
    "claim_three_structural_gaps_summary",
    "claim_lit_fixed_team_assumption",
    "claim_lit_tightly_coupled_coordination",
]
