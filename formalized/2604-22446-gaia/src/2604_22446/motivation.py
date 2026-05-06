"""Motivation: skills/tools advance individual agents but multi-agent
systems remain stuck behind fixed teams, brittle coordination, and
session-bound learning. The missing layer is a principled organisation
abstraction.

Section 1 (Introduction) of Yu et al. 2026
[@Yu2026OMC] -- introduces OneManCompany (OMC), elevates MAS to the
organisational level via the Talent abstraction, the Talent Market,
and the Explore-Execute-Review (E2R) tree search.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup: skills/tools and the MAS regime
# ---------------------------------------------------------------------------

setup_individual_skills_advances = setting(
    "**Individual agent capability via skills + tools.** Recent LLM "
    "agents (Claude Code [@ClaudeCode], Codex [@Codex], OpenClaw "
    "[@OpenClaw]) accumulate capability through a modular ecosystem "
    "of *skills* and tool integrations [@SkillsMP; @MCPZoo]. Skills "
    "extend an agent's functionality without modifying the underlying "
    "model: they can be reused, composed, and shared across agents. "
    "This individual-level modularity has been the dominant driver "
    "of recent capability gains.",
    title="Setup: skills + tool integrations modularly extend a single agent's capability without retraining",
)

setup_existing_mas_paradigm = setting(
    "**Existing multi-agent LLM systems.** Current orchestration "
    "frameworks (CrewAI [@CrewAI], AutoGen [@AutoGen], Paperclip "
    "[@Paperclip]) coordinate multiple agents via message passing, "
    "role assignment, and shared memory. Either they hardcode a team "
    "structure (brittle to novel projects) or they let agents "
    "negotiate freely (no convergence guarantees). Recent dynamic "
    "agentic workflows [@TDAG; @PlanAndAct; @EvoMAC] adapt task "
    "decomposition at runtime but still operate inside a "
    "pre-configured sandbox: fixed team, single shared runtime, and "
    "constrained workflow topology.",
    title="Setup: existing MAS frameworks (fixed teams, shared runtimes, bounded workflow topologies)",
)

# ---------------------------------------------------------------------------
# Diagnosis: capability vs. organisation gap
# ---------------------------------------------------------------------------

claim_skills_within_agent_only = claim(
    "**Skills operate strictly within a single agent.** Skills "
    "enhance what an agent can *do*, but they do not address how "
    "multiple agents should *work together*. As tasks grow in "
    "complexity, requiring diverse expertise, long-horizon "
    "coordination, and iterative refinement, a single agent, no "
    "matter how skill-equipped, becomes insufficient. Skills are an "
    "individual-level abstraction; they cannot answer 'how should a "
    "workforce of agents be assembled, governed, and improved?'",
    title="Diagnosis: skills are individual-level only -- they extend a single agent but cannot organise a workforce",
)

claim_existing_mas_three_limits = claim(
    "**Existing MAS frameworks have three structural limits.** "
    "(L1) **Fixed team or unconstrained negotiation** -- "
    "orchestrators either hardcode team structure (brittle to novel "
    "projects) or allow free negotiation (no convergence "
    "guarantees). (L2) **Runtime lock-in** -- agents from different "
    "families cannot interoperate because they are tied to "
    "incompatible runtimes; roles are specified through descriptive "
    "prompts rather than executable contracts, leading to "
    "hallucinated capabilities. (L3) **Session-bound, framework-"
    "specific self-improvement** -- where self-improvement exists, "
    "it does not persist across projects.",
    title="Diagnosis: existing MAS face fixed-team brittleness, runtime lock-in, and session-bound learning",
)

claim_dynamic_workflow_still_bounded = claim(
    "**Dynamic agentic workflows are still pre-configured.** "
    "Adaptive task decomposition at runtime [@TDAG; @PlanAndAct; "
    "@EvoMAC] outperforms static pipelines, but even these systems "
    "fix the team before the project starts, force all agents into "
    "the same runtime, and constrain the workflow topology to a "
    "known template. The team, the runtime substrate, and the "
    "workflow shape are all determined ahead of execution.",
    title="Diagnosis: even dynamic agentic workflows still pre-configure the team / runtime / workflow template",
)

claim_missing_organisation_layer = claim(
    "**The missing layer is a principled organisation abstraction.** "
    "Skills are *capability-level* abstractions (what can an agent "
    "do?). Multi-agent systems are *interaction-level* abstractions "
    "(how do agents communicate?). Neither is an *organisation-"
    "level* abstraction that governs how a workforce of agents is "
    "assembled into teams, how work is decomposed and executed, and "
    "how the system evolves over time. The missing layer is "
    "decoupled from individual-agent knowledge -- analogous to how "
    "a real company's organisational principles generalise across "
    "industries independent of specific employee expertise.",
    title="Diagnosis: skills (capability-level) and MAS (interaction-level) leave the organisation-level gap unaddressed",
)

# ---------------------------------------------------------------------------
# Central definition and question
# ---------------------------------------------------------------------------

setup_ai_organisation_definition = setting(
    "**Definition 1 (AI Organisation).** A self-governing system of "
    "heterogeneous agents with: (P1) **structured coordination** -- "
    "agent interactions governed by explicit protocols and "
    "organisational constraints rather than ad hoc prompting; (P2) "
    "**managed lifecycles** -- agents are created, assigned, "
    "evaluated, and retired through well-defined processes; and "
    "(P3) **experience-driven evolution** -- both individual agents "
    "and the organisation improve over time through systematic "
    "feedback and reflection.",
    title="Definition 1: AI organisation = structured coordination + managed lifecycle + experience-driven evolution",
)

q_central = question(
    "How can AI agent workforces be **automatically organised, "
    "coordinated, and evolved** to solve open-ended tasks across "
    "domains? Concretely, can the organisational layer be made "
    "decouplable from individual-agent knowledge so that the same "
    "organisational principles generalise across heterogeneous "
    "agent backends and arbitrary domains?",
    title="Central question: can AI workforces be automatically organised, coordinated, and evolved across domains?",
)

# ---------------------------------------------------------------------------
# Proposed framework: OneManCompany (OMC)
# ---------------------------------------------------------------------------

claim_omc_proposal = claim(
    "**Proposal: OneManCompany (OMC) -- an organisation-level "
    "framework.** OMC [@OMCRepo] elevates multi-agent systems to "
    "the *organisational* level. Three core abstractions: "
    "(A1) a **Talent** is a portable agent identity package "
    "encapsulating role, prompts, skills, tools, and working "
    "principles, deployable on any supported runtime without "
    "modification; (A2) a **Container** is the execution "
    "environment that hosts a Talent (LangGraph [@LangGraph], "
    "Claude CLI, or script-based) and exposes capabilities through "
    "a uniform set of organisational interfaces; (A3) "
    "**Talent + Container = Employee**, a fully managed AI agent "
    "with a structured lifecycle from hiring through performance "
    "review to potential offboarding.",
    title="Proposal: OMC -- Talent (portable identity) + Container (runtime + interfaces) = managed Employee",
)

claim_three_pillars = claim(
    "**OMC is built on three pillars.** "
    "(Pillar 1) **Typed Talent-Container architecture** "
    "(Section 2.1) -- six typed organisational interfaces "
    "(Execution, Task, Event, Storage, Context, Lifecycle) decouple "
    "*who an agent is* (the Talent) from *where it runs* (the "
    "Container), with a community-driven Talent Market [@OMCMarket] "
    "supplying verified agents on demand. "
    "(Pillar 2) **Explore-Execute-Review (E2R) tree search** "
    "(Section 2.2) -- models project execution as search over "
    "organisational strategies, with a DAG-based decomposition + "
    "AND-tree semantics + finite state machine providing formal "
    "guarantees on termination, deadlock-freedom, and crash "
    "recovery. "
    "(Pillar 3) **Agent and organisation self-evolution** "
    "(Section 2.3) -- CEO one-on-ones, post-task reflection, "
    "project retrospectives feeding into updated SOPs, and a formal "
    "HR pipeline (periodic evaluations, PIP, offboarding) with "
    "real consequences.",
    title="Proposal: OMC's three pillars (Talent-Container + E2R tree search + self-evolution)",
)

claim_organisation_decoupling_thesis = claim(
    "**Central thesis: organisation is decouplable from "
    "capability.** A real company's organisational principles "
    "(structure, coordination, lifecycle, evolution) are *decoupled* "
    "from individual-employee expertise -- the same principles work "
    "across software, manufacturing, and consulting. We posit the "
    "same decoupling for AI agents: typed organisational interfaces "
    "+ a portable Talent abstraction + a Talent Market let "
    "heterogeneous agent backends coexist within a single "
    "organisation, governed by the same management machinery, "
    "across any domain.",
    title="Thesis: organisation decoupled from capability is feasible for AI agents (analogous to human companies)",
)

# ---------------------------------------------------------------------------
# Headline empirical claim (Abstract / Section 3.2)
# ---------------------------------------------------------------------------

claim_headline_prdbench = claim(
    "**Headline empirical claim.** On PRDBench [@PRDBench] (50 "
    "project-level software development tasks spanning 20+ "
    "domains, DEV mode = single-attempt zero-shot setting), OMC "
    "achieves a **success rate of 84.67%**, surpassing all "
    "baselines by **at least +15.48 percentage points**. Total cost "
    "for the 50-task run: $345.59 (~$6.91 per task). Cross-domain "
    "case studies (content generation, web game development, "
    "audiobook production, automated research survey) demonstrate "
    "generality across modalities and agent families.",
    title="Headline: OMC achieves 84.67% success on PRDBench (+15.48 pp over best baseline); cross-domain generality demonstrated",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Abstract + Table 2 (page 14)",
    },
)

claim_three_design_aspects_drive_result = claim(
    "**Three design aspects of OMC contribute to the headline "
    "result (Section 3.2).** (D1) The dynamic task tree adjusts "
    "decomposition during execution rather than committing to a "
    "fixed pipeline upfront. (D2) The enforced "
    "completed -> accepted review gate means no subtask result "
    "propagates downstream without supervisor approval, reducing "
    "hallucinated outputs and limiting error cascading. "
    "(D3) Container-Talent separation lets the system recruit "
    "agents from different families (LangGraph, Claude CLI, "
    "script-based) within the same project, matching the right "
    "tool to each subtask.",
    title="Headline: OMC's gain attributable to dynamic decomposition + accept gate + cross-family recruitment",
)

# ---------------------------------------------------------------------------
# Stated contributions
# ---------------------------------------------------------------------------

claim_three_stated_contributions = claim(
    "**Stated contributions (Abstract + Section 1).** "
    "(C1) **Diagnosis** -- multi-agent systems lack a principled "
    "organisational layer decoupled from individual-agent knowledge. "
    "(C2) **Method** -- OMC: Talent-Container architecture + Talent "
    "Market + E2R tree search + self-evolution pipeline. "
    "(C3) **Formal guarantees** -- E2R + AND-tree + FSM yield "
    "termination and deadlock-freedom under bounded retry and "
    "finite resources. "
    "(C4) **Empirical validation** -- 84.67% on PRDBench (+15.48 pp "
    "over best baseline) plus four cross-domain case studies.",
    title="Four stated contributions (diagnosis / method / formal guarantees / empirical validation)",
)

__all__ = [
    "setup_individual_skills_advances",
    "setup_existing_mas_paradigm",
    "claim_skills_within_agent_only",
    "claim_existing_mas_three_limits",
    "claim_dynamic_workflow_still_bounded",
    "claim_missing_organisation_layer",
    "setup_ai_organisation_definition",
    "q_central",
    "claim_omc_proposal",
    "claim_three_pillars",
    "claim_organisation_decoupling_thesis",
    "claim_headline_prdbench",
    "claim_three_design_aspects_drive_result",
    "claim_three_stated_contributions",
]
