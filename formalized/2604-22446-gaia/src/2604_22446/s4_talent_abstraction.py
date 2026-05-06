"""Section 2.1: On-demand Organisation of Heterogeneous Agents by
Talent-Container Architecture (pages 5-6).

Six typed organisational interfaces, the three architectural
properties (identity-substrate separation, multi-tenancy with
isolation, extensibility without modification), Algorithm 1 (Talent
Assembly), the OS-kernel correspondence (Appendix B), and Table 1
(Skills vs Talents).

Source: Yu et al. 2026 [@Yu2026OMC], Section 2.1 + Appendices A, B.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 2.1.1 Six typed organisational interfaces (page 5)
# ---------------------------------------------------------------------------

setup_six_typed_interfaces = setting(
    "**Six typed organisational interfaces (Section 2.1.1, "
    "Appendix A Table 5).** A Container exposes its capabilities to "
    "the OMC platform through six typed interfaces:\n\n"
    "| Interface | Signature | Responsibility |\n"
    "|---|---|---|\n"
    "| Execution | `execute(task, ctx) -> (result, cost)` | Dispatch task to backend, return output |\n"
    "| Task | `enqueue(task); dequeue() -> task` | Per-employee queue, mutual exclusion |\n"
    "| Event | `publish(event); subscribe(filter)` | Organisational event bus |\n"
    "| Storage | `read(key) -> data; write(key, data)` | Persistent memory (short / medium-term) |\n"
    "| Context | `assemble(role, guidance, memory) -> ctx` | Execution context construction |\n"
    "| Lifecycle | `pre_hook(task, ctx); post_hook(task, result)` | Validation, guardrails, self-improvement |\n",
    title="Setup: six typed organisational interfaces (Execution / Task / Event / Storage / Context / Lifecycle)",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Table 5 (Appendix A, page 25)",
    },
)

setup_algorithm_1_talent_assembly = setting(
    "**Algorithm 1 (Talent Assembly).** Composes the six "
    "interfaces during one task execution.\n\n"
    "Inputs: employee $e$ with Container $V_e$, Talent $\\tau_e$, "
    "task node $v$. Outputs: result $r$, cost $c$.\n\n"
    "1. **Queue management**: if $e$ has a running task, "
    "$\\text{Enqueue}(v)$ and return.\n"
    "2. **Context assembly**: "
    "$\\text{ctx} \\gets \\text{AssembleContext}("
    "\\tau_e.\\text{role}, \\tau_e.\\text{principles}, "
    "\\text{GetGuidance}(e), \\text{GetMemory}(e))$.\n"
    "3. **Lifecycle pre-hook**: "
    "$(v, \\text{ctx}) \\gets \\text{PreHook}(v, \\text{ctx})$ "
    "(guardrails, input validation).\n"
    "4. **Dispatch via Container**: "
    "$(r, c) \\gets V_e.\\text{Execute}("
    "v.\\text{desc}, \\text{ctx}, \\tau_e.\\text{tools})$.\n"
    "5. **Lifecycle post-hook**: "
    "$\\text{PostHook}(e, v, r)$ (self-reflection, principle "
    "updates).\n"
    "6. **Event publication**: "
    "$\\text{Publish}(\\varepsilon(v, "
    "\\text{Processing} \\to \\text{Completed}, e, t_{\\text{now}}))$.\n"
    "7. **Return** $(r, c)$.",
    title="Setup: Algorithm 1 (Talent Assembly) -- composes the six interfaces during one task execution",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Algorithm 1 (page 7)",
    },
)

# ---------------------------------------------------------------------------
# Three architectural properties (page 5-6)
# ---------------------------------------------------------------------------

claim_property_1_identity_substrate_separation = claim(
    "**Property P1: Identity-Substrate Separation.** The same "
    "Talent can run on a LangGraph agent, a Claude CLI session, or "
    "a script-based executor without modification, and conversely "
    "the same Container type can host different Talents to produce "
    "employees with different roles on the same backend. The "
    "Talent-Container product space factors cleanly: $|T| \\times "
    "|C|$ deployable employees from $|T| + |C|$ artefacts.",
    title="Property P1: identity-substrate separation (same Talent runs on any Container; same Container hosts any Talent)",
)

claim_property_2_multi_tenancy_isolation = claim(
    "**Property P2: Multi-tenancy with isolation.** All agent-"
    "platform interaction passes through the six typed interfaces, "
    "so no Container can bypass organisational policies on task "
    "validation, event propagation, or memory access. The typed "
    "contract is the *only* communication channel; the platform "
    "never touches backend-specific APIs.",
    title="Property P2: multi-tenancy with isolation (all interaction routed through 6 typed interfaces; no backend backdoors)",
)

claim_property_3_extensibility = claim(
    "**Property P3: Extensibility without platform "
    "modification.** Adding a new agent runtime requires only a "
    "Container implementation conforming to the six contracts. The "
    "lifecycle hooks (`pre_hook`, `post_hook`) enable self-"
    "improvement (working-principle refinement, skill accumulation) "
    "*entirely at the organisational layer*, without modifying the "
    "underlying foundation models.",
    title="Property P3: extensibility (new runtime needs only a 6-interface Container; self-improvement at organisational layer)",
)

# ---------------------------------------------------------------------------
# OS-kernel correspondence (Appendix B, Table 6)
# ---------------------------------------------------------------------------

claim_os_kernel_correspondence = claim(
    "**Six interfaces mirror the canonical OS kernel subsystems "
    "(Appendix B, Table 6).** Standard OS texts [@TanenbaumOS; "
    "@SilberschatzOS] identify six kernel subsystems; OMC's six "
    "organisational interfaces correspond one-to-one:\n\n"
    "| OS Subsystem | OMC Interface | OMC Realisation |\n"
    "|---|---|---|\n"
    "| Process Mgmt | Execution + Task | Dispatch tasks; enforce $|\\text{running}(e)| \\le 1$; per-employee queues |\n"
    "| Memory Mgmt | Context | Assemble execution context (role, principles, memory) per agent |\n"
    "| File System | Storage | Uniform read/write over heterogeneous backends (YAML profiles, logs, memory) |\n"
    "| I/O & Device Mgmt | Container contract | Each Container type implements the six interfaces (no backend-specific APIs) |\n"
    "| IPC | Event | Publish/subscribe event bus across all agents |\n"
    "| Security & Audit | Lifecycle | Pre-hooks enforce guardrails / validation; post-hooks audit and self-reflect |\n",
    title="Property: six interfaces correspond 1-to-1 to the canonical OS kernel subsystems (Process / Memory / FS / I/O / IPC / Security)",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Table 6 (Appendix B, page 25)",
    },
)

# ---------------------------------------------------------------------------
# 2.1.2 Talent Market (page 6) + Appendix D supply chain
# ---------------------------------------------------------------------------

claim_talent_market_grounding = claim(
    "**The Talent Market is grounded in community-validated "
    "agents, not synthesised personas.** Rather than synthesising "
    "agents from descriptive prompts (a practice prone to "
    "capability hallucination), OMC recruits from a pool of "
    "community-verified, benchmark-validated implementations and "
    "provisions them through an automated hiring pipeline. Each "
    "marketplace Talent is a complete, ready-to-deploy package "
    "comprising system prompts and role definitions, tool "
    "configurations and MCP integrations [@MCP], skill scripts, "
    "domain knowledge files, and benchmark results.",
    title="Talent Market: grounded in community-verified, benchmark-validated agent packages (not synthesised personas)",
)

claim_three_sourcing_channels = claim(
    "**Three sourcing channels in the Talent Market (Appendix D).** "
    "(T1) **Curated repository agents** -- manually packaged from "
    "established open-source repos, framework-specific dependencies "
    "stripped, validated against reference tasks. "
    "(T2) **Prompt-sourced agents with skill assembly** -- start "
    "from community personas (e.g., Agency-Agents collection [@AgencyAgents] "
    "with 140+ specialist personas), then automatically query "
    "SkillsMP [@SkillsMP] to attach compatible skills. "
    "(T3) **Dynamic agent assembly from cloud skills** -- assemble "
    "both persona and skill set on demand from SkillsMP via "
    "semantic search. All three produce standard Talent packages "
    "and enter the runtime through the same pathway. Cross-type "
    "feedback: refined skills/personas from deployed agents flow "
    "back to the marketplace.",
    title="Talent Market supply chain: three parallel sourcing channels (curated / persona+skill assembly / dynamic) with cross-type feedback",
)

claim_human_in_loop_recruitment = claim(
    "**Human-in-the-loop hiring with diversity composition.** "
    "When the policy $\\pi(\\mathcal{T})$ requires a capability "
    "absent from the current workforce, triggering a recruit "
    "action $\\alpha_r \\in \\mathcal{A}_{\\text{recruit}}$, HR "
    "queries the Talent Market, compiles a ranked top-$k$ "
    "shortlist by skill match and community ratings, and presents "
    "it to the CEO. The recommendation engine composes the "
    "shortlist with a roughly 80/20 distribution (80% Type 1+2, "
    "20% Type 3) reflecting current relative maturity. Upon CEO "
    "selection, the automated pipeline provisions the Talent with "
    "a Container, assigns a desk, configures tool access, and "
    "registers the new employee.",
    title="Talent Market: top-k shortlist (~80/20 Type1+2/Type3) presented to CEO; automated pipeline provisions selected Talent",
)

# ---------------------------------------------------------------------------
# Table 1: Skills vs Talents
# ---------------------------------------------------------------------------

claim_table_1_skills_vs_talents = claim(
    "**Table 1: Skills & Skill Markets vs Talents & Talent "
    "Markets.**\n\n"
    "| Aspect | Skills & Skill Markets | Talents & Talent Markets |\n"
    "|---|---|---|\n"
    "| Level | Inside one agent | Across a team of agents |\n"
    "| What it is | Small reusable tools/functions | Full agents with roles, tools, and behaviour |\n"
    "| Purpose | Make one agent more capable | Build and run a team to solve tasks |\n"
    "| How they combine | Linked as tool chains inside an agent | Organised into teams with roles and responsibilities |\n"
    "| Runtime | Tied to one system or framework | Can run across different systems |\n"
    "| Flexibility | Usually fixed before execution | Can be added, replaced, or reconfigured on the fly |\n"
    "| Market role | Library of tools to download | Hiring pool of agents to recruit |\n"
    "| Quality control | Examples / documentation | Tested and evaluated agents |\n"
    "| Lifecycle | No clear lifecycle | Managed lifecycle (hire, evaluate, replace) |\n"
    "| Learning | Improves individual agent | Improves both agents and the whole organisation |\n"
    "| Analogy | Software libraries (APIs) | Employees and job markets |\n\n"
    "Skills improve what a single agent can do. Talents organise "
    "multiple agents into a workforce that can be built, managed, "
    "and improved over time.",
    title="Table 1: 11-axis comparison Skills vs Talents (libraries-of-APIs vs employees-and-job-markets)",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Table 1 (page 4)",
    },
)

# ---------------------------------------------------------------------------
# Connection back: typed-interface decoupling thesis
# ---------------------------------------------------------------------------

claim_typed_interface_decoupling_demonstration = claim(
    "**The Talent-Container architecture demonstrates that "
    "typed-interface decoupling of identity from runtime is "
    "feasible.** The architecture is implemented and deployed, "
    "with three Container families (Claude Code, LangGraph, "
    "script-based) hosting Talents recruited from the Talent "
    "Market. This is a concrete existence proof: identity-runtime "
    "decoupling does not require sacrificing coordination depth "
    "(the six interfaces compose into Algorithm 1 with full task / "
    "event / memory / lifecycle semantics).",
    title="Demonstration: typed-interface decoupling of identity from runtime is feasible (deployed across 3 Container families)",
)

__all__ = [
    "setup_six_typed_interfaces",
    "setup_algorithm_1_talent_assembly",
    "claim_property_1_identity_substrate_separation",
    "claim_property_2_multi_tenancy_isolation",
    "claim_property_3_extensibility",
    "claim_os_kernel_correspondence",
    "claim_talent_market_grounding",
    "claim_three_sourcing_channels",
    "claim_human_in_loop_recruitment",
    "claim_table_1_skills_vs_talents",
    "claim_typed_interface_decoupling_demonstration",
]
