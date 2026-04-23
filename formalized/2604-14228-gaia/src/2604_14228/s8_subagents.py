"""Section 8: Subagent Delegation and Orchestration"""

from gaia.lang import claim, setting, support

from .s2_values_principles import (
    principle_isolated_subagent_boundaries,
    principle_deny_first,
    principle_reversibility_weighted,
)
from .s3_architecture import (
    context_window_as_binding_constraint,
    reasoning_separation_claim,
)
from .s6_extensibility import agent_tool_vs_skill_tool

# ── Settings ───────────────────────────────────────────────────────────────────

agent_tool_schema_setting = setting(
    "The Agent tool (AgentTool.tsx) is the delegation mechanism, with Task retained as a "
    "legacy alias. The input schema uses feature-gated fields: the isolation field offers "
    "['worktree', 'remote'] for internal users and ['worktree'] for external users. "
    "The cwd field is gated by a feature flag. The run_in_background field is omitted when "
    "background tasks are disabled or when fork-subagent mode is enabled. "
    "runAgent() accepts 21 parameters covering: agent definition, prompts, permissions, "
    "tools, model settings, isolation, and callbacks.",
    title="Agent tool input schema and runAgent() parameters",
)

builtin_subagent_types_setting = setting(
    "Claude Code provides up to six built-in subagent types (depending on feature flags): "
    "(1) Explore — primarily read/search-oriented, write and edit tools in its deny-list; "
    "(2) Plan — creates structured plans, execution proceeds through standard permission model; "
    "(3) General-purpose — broadly capable; "
    "(4) Claude Code Guide — onboarding and documentation assistance, with permissionMode override; "
    "(5) Verification — runs validation checks (test suites, linting); "
    "(6) Statusline-setup — specialized for terminal status line configuration. "
    "Custom subagents are defined via .claude/agents/*.md files or plugin-contributed "
    "agent definitions via loadPluginAgents.ts.",
    title="Six built-in subagent types",
)

isolation_modes_setting = setting(
    "Subagent isolation supports three modes (AgentTool.tsx): "
    "(1) Worktree — creates a temporary git worktree giving the subagent its own copy of "
    "the repository without affecting the parent's working tree; "
    "(2) Remote (internal-only) — launches in a remote Claude Code Remote environment, "
    "always in the background; "
    "(3) In-process (default) — shares the filesystem with the parent but operates in an "
    "isolated conversation context. "
    "Worktree-based isolation provides filesystem-level separation with zero external "
    "dependencies, leveraging Git's built-in mechanism rather than container orchestration.",
    title="Three subagent isolation modes",
)

permission_override_setting = setting(
    "The permission override logic for subagents (runAgent.ts): when a subagent defines a "
    "permissionMode, the override is applied unless the parent is already in "
    "bypassPermissions, acceptEdits, or auto mode — those modes always take precedence "
    "because they represent explicit user decisions. For async agents, the system determines "
    "whether to avoid prompts through a cascade: explicit canShowPermissionPrompts first, "
    "then bubble mode (always show, since they escalate to parent terminal), then the default "
    "(sync agents show prompts, async agents do not). Background agents set "
    "awaitAutomatedChecksBeforeDialog: true, ensuring classifier and hooks resolve before "
    "interrupting the user.",
    title="Subagent permission override logic",
)

sidechain_transcripts_setting = setting(
    "Each subagent writes its own transcript as a separate .jsonl file with a .meta.json "
    "metadata file (sessionStorage.ts, runAgent.ts). Only the subagent's final response "
    "text and metadata return to the parent conversation context; the full subagent history "
    "never enters the parent's context window. Agent teams consume approximately 7x the "
    "tokens of a standard session in plan mode (Anthropic, 2025b).",
    title="Subagent sidechain transcripts: summary-only return",
)

file_locking_coordination_setting = setting(
    "For multi-instance coordination in agent teams, the harness uses file locking rather "
    "than a message broker or distributed coordination service (Anthropic, 2025b). Tasks "
    "are claimed from a shared list via lock-file-based mutual exclusion, with lock files "
    "stored at predictable filesystem paths. This trades throughput for zero-dependency "
    "deployment and full debuggability (any agent's state can be inspected by reading "
    "plain-text JSON files).",
    title="File locking for multi-agent coordination",
)

# ── Core claims about subagent architecture ────────────────────────────────────

isolated_context_boundaries = claim(
    "Subagents operate in isolated context windows with rebuilt permission context and "
    "independent tool sets. The default path does not inherit the parent's conversation "
    "history (the fork-subagent path is an exception). This means most subagent invocations "
    "require a self-contained prompt, because the subagent cannot use the parent's context "
    "for disambiguation. Conversation-based frameworks that share full transcript histories "
    "avoid this cost but risk context explosion as the number of agents grows.",
    title="Subagents have isolated contexts; no history inheritance by default",
    background=[agent_tool_schema_setting, isolation_modes_setting],
)

strat_isolated_context = support(
    [context_window_as_binding_constraint],
    isolated_context_boundaries,
    reason=(
        "Context window pressure (@context_window_as_binding_constraint) makes history "
        "inheritance across subagents architecturally expensive — shared full transcript "
        "histories risk context explosion as agents multiply. The isolated subagent "
        "boundaries principle (@principle_isolated_subagent_boundaries) formalizes the "
        "design choice: subagents get rebuilt permission contexts and independent tool sets, "
        "operating in isolation. The 7x token consumption for agent teams confirms the "
        "cost of even isolated-context parallelism. Confirmed from AgentTool.tsx and "
        "runAgent.ts (Tier B evidence)."
    ),
    prior=0.88,
)

summary_only_return = claim(
    "Subagents return only summary text to the parent, not their full conversation history. "
    "Sidechain transcripts store each subagent's conversation in a separate file, preventing "
    "subagent content from inflating the parent context. This is a deliberate "
    "context-conservation choice: conversation-based frameworks that share full transcript "
    "histories between agents risk context explosion as the number of agents grows. "
    "The 7x token consumption for agent teams in plan mode makes summary-only return "
    "especially critical when subagents are also in isolated contexts.",
    title="Summary-only return to preserve parent context",
    background=[sidechain_transcripts_setting],
)

strat_summary_only = support(
    [isolated_context_boundaries, context_window_as_binding_constraint],
    summary_only_return,
    reason=(
        "Given isolated context boundaries (@isolated_context_boundaries), subagents "
        "each have a full context window of their own. If each returned its full "
        "conversation history to the parent (@context_window_as_binding_constraint "
        "would be immediately violated), N parallel subagents would produce N context "
        "windows worth of history. Summary-only return compresses this to N summaries. "
        "The 7x token multiplier for agent teams confirms that even with summary-only "
        "return, multi-agent use is expensive. Confirmed from sessionStorage.ts:247 "
        "(Tier B evidence)."
    ),
    prior=0.9,
)

worktree_isolation_design = claim(
    "Worktree-based isolation provides filesystem-level separation with zero external "
    "dependencies, using Git's built-in mechanism rather than container orchestration. "
    "This occupies a middle point in the isolation design space: stronger than context-only "
    "isolation (used by conversation-based frameworks like AutoGen) but simpler than "
    "container-based isolation (used by SWE-Agent and OpenHands), which provides stronger "
    "resource boundaries but requires container infrastructure.",
    title="Worktree isolation: between context-only and container-based",
    background=[isolation_modes_setting],
)

strat_worktree = support(
    [isolated_context_boundaries],
    worktree_isolation_design,
    reason=(
        "Isolated subagent boundaries (@principle_isolated_subagent_boundaries) require "
        "some form of filesystem separation for subagents that write code. The reversibility-"
        "weighted principle (@principle_reversibility_weighted) favors solutions where "
        "subagent changes can be merged or discarded. Git worktrees satisfy both: they "
        "provide real filesystem isolation (unlike context-only isolation) without requiring "
        "external infrastructure (unlike Docker). Worktree-based isolation is confirmed "
        "in AgentTool.tsx (Tier B evidence)."
    ),
    prior=0.85,
)

two_tier_permission_scoping = claim(
    "When allowedTools is explicitly provided to runAgent(), a two-tier permission scoping "
    "model applies: SDK-level permissions from --allowedTools are preserved ('explicit "
    "permissions from the SDK consumer that should apply to all agents'), but session-level "
    "rules are replaced with the subagent's declared allowedTools. When allowedTools is not "
    "provided (the common AgentTool path), the parent's session-level rules are inherited "
    "without replacement.",
    title="Two-tier permission scoping for subagents",
    background=[permission_override_setting],
)

strat_two_tier = support(
    [isolated_context_boundaries],
    two_tier_permission_scoping,
    reason=(
        "The deny-first principle (@principle_deny_first) requires that permissions be "
        "explicitly granted, not assumed. Isolated context boundaries (@isolated_context_boundaries) "
        "mean subagents cannot inherit implicit permissions from the parent conversation. "
        "The two-tier model resolves the tension: SDK-level permissions (set by the SDK "
        "consumer, an external trust anchor) propagate to all subagents, while session-level "
        "permissions (set interactively) are replaced by the subagent's own declaration. "
        "This is confirmed from runAgent.ts (Tier B evidence)."
    ),
    prior=0.87,
)
