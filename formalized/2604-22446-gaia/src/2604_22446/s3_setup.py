"""Section 2 (Methodology -- terminology) of Yu et al. 2026 [@Yu2026OMC].

Defines the core organisational terminology that subsequent sections
build on: Employee, Talent, Container, Talent Market, CEO,
Founding Team, and Wild Dynamic Agentic Workflow. Also captures the
high-level pillar architecture (Section 2 opening).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Core terminology (Section 2 opening, page 5)
# ---------------------------------------------------------------------------

setup_employee_definition = setting(
    "**Definition (Employee).** The fundamental unit of agency in "
    "OMC, analogous to an employee in a real company, characterised "
    "by domain expertise, role responsibilities, skill set, and "
    "tool access. Each employee is decomposed into two components: "
    "a Talent (cognitive identity) and a Container (runtime "
    "environment), forming a single managed AI agent with a "
    "structured lifecycle.",
    title="Setup: Employee = Talent + Container (fundamental unit of agency in OMC)",
)

setup_talent_definition = setting(
    "**Definition (Talent).** A portable package defining an "
    "employee's cognitive identity: prompts, role and work "
    "principles, agent family configuration, tools, skills, and "
    "supporting resources. A Talent is deployable across OMC "
    "instances without execution-specific dependencies. Talents "
    "elevate the unit of reuse from individual tools to complete "
    "agent identities with managed lifecycles.",
    title="Setup: Talent = portable cognitive-identity package (prompts + principles + tools + skills, runtime-independent)",
)

setup_container_definition = setting(
    "**Definition (Container).** The runtime environment that "
    "hosts a Talent, encapsulating the agent runtime, middleware "
    "hooks, wrappers, and resources. Three Container families are "
    "currently supported: (1) Claude Code-based, (2) "
    "LangGraph-based [@LangGraph], (3) script-based. The Container "
    "exposes its capabilities to OMC through six typed "
    "organisational interfaces (Section 2.1).",
    title="Setup: Container = runtime environment (Claude Code / LangGraph / script-based) hosting a Talent",
)

setup_talent_market_definition = setting(
    "**Definition (Talent Market) [@OMCMarket].** A community-"
    "driven agent marketplace hosting verified and popular open-"
    "source agents. Unlike systems that rely on AI-generated "
    "characters, OMC grounds agent selection in community-validated "
    "implementations. When community agents do not cover a "
    "required domain, an AI-powered recommendation engine "
    "discovers and assembles suitable skills from the web, "
    "mitigating the cold-start problem.",
    title="Setup: Talent Market = community-driven marketplace of verified open-source agents (with cold-start AI assembly)",
)

setup_ceo_definition = setting(
    "**Definition (CEO).** The only human in the AI company, also "
    "the creator and maintainer of an OMC instance. Users of an "
    "OMC instance can be internal (the CEO directly) or external "
    "(accessing via an AI economy contract protocol).",
    title="Setup: CEO = the sole human in the AI company (creator/maintainer of an OMC instance)",
)

setup_founding_team_definition = setting(
    "**Definition (Founding Team).** Each OMC instance is "
    "bootstrapped with a default set of employees: a Human "
    "Resource Manager (HR), an Executive Assistant (EA), a Chief "
    "Operating Officer (COO), and a Chief Sales Officer (CSO). "
    "These default employees handle organisational cold-start "
    "(receiving the CEO directive, planning, hiring, contracting) "
    "before any specialist agents are recruited.",
    title="Setup: Founding Team = HR + EA + COO + CSO (default bootstrap employees)",
)

setup_wild_dynamic_workflow = setting(
    "**Definition (Wild Dynamic Agentic Workflow).** A multi-agent "
    "workflow in which neither the team (composition, agent "
    "runtimes, agent capabilities) nor the workflow itself (task "
    "decomposition, execution ordering) is fixed before execution. "
    "All may change at any point during a project. This contrasts "
    "with existing dynamic agentic workflows that adapt task "
    "decomposition at runtime but still require a pre-configured "
    "team, a single shared runtime, and a known workflow template.",
    title="Setup: Wild Dynamic Agentic Workflow = team + runtimes + capabilities + workflow all unfixed pre-execution",
)

# ---------------------------------------------------------------------------
# Three pillars of OMC (Section 2 opening, page 4)
# ---------------------------------------------------------------------------

setup_three_pillars_architecture = setting(
    "**Three pillars of OMC (Section 2 opening).** OMC mirrors how "
    "a real company operates, organised around three pillars: "
    "(P1) **Organisational layer + Talent Market** (Section 2.1) -- "
    "agents are managed and recruited under uniform policies; "
    "(P2) **E2R tree search + DAG scheduling** (Sections 2.2-"
    "2.2.4) -- agents collaborate through structured project "
    "execution; (P3) **Self-evolution** (Section 2.3) -- agents "
    "and the organisation improve over time through reflection and "
    "performance review.",
    title="Setup: OMC's three pillars (organisational layer + E2R/DAG + self-evolution)",
)

# ---------------------------------------------------------------------------
# Core challenge that motivates the design
# ---------------------------------------------------------------------------

claim_radical_heterogeneity_challenge = claim(
    "**Core design challenge: radical heterogeneity of "
    "executors.** The employees that execute tasks in OMC are "
    "*radically heterogeneous*: some are hosted LLM agents "
    "(LangChain / LangGraph), others are interactive coding "
    "sessions (Claude Code), still others are script-based "
    "executors wrapping open-source frameworks. Without a unifying "
    "abstraction, the orchestration layer would degenerate into a "
    "tangle of backend-specific conditional logic, and every new "
    "agent runtime would require invasive changes across "
    "scheduling, lifecycle management, and event propagation.",
    title="Challenge: radical executor heterogeneity makes a unifying abstraction necessary to avoid backend-specific tangles",
)

claim_typed_layer_solves_heterogeneity = claim(
    "**OMC's typed organisational layer solves the heterogeneity "
    "challenge.** OMC standardises how any agent backend connects "
    "to the platform via a typed organisational layer, analogous "
    "to how an OS kernel provides a uniform interface over "
    "heterogeneous hardware. The Talent and Container abstractions "
    "form a digital talent layer: a composable, runtime-independent "
    "representation of agent capabilities that sits between "
    "low-level skills and high-level organisational structure.",
    title="Claim: typed organisational layer abstracts heterogeneity (analogous to OS kernel over heterogeneous hardware)",
)

__all__ = [
    "setup_employee_definition",
    "setup_talent_definition",
    "setup_container_definition",
    "setup_talent_market_definition",
    "setup_ceo_definition",
    "setup_founding_team_definition",
    "setup_wild_dynamic_workflow",
    "setup_three_pillars_architecture",
    "claim_radical_heterogeneity_challenge",
    "claim_typed_layer_solves_heterogeneity",
]
