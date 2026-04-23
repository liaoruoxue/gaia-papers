"""Section 6: Extensibility — MCP, Plugins, Skills, and Hooks"""

from gaia.lang import claim, setting, support, compare

from .s2_values_principles import (
    principle_composable_extensibility,
    principle_externalized_programmable_policy,
    principle_context_as_scarce_resource,
)
from .s3_architecture import context_window_as_binding_constraint, reasoning_separation_claim

# ── Extensibility settings ─────────────────────────────────────────────────────

four_mechanisms_setting = setting(
    "Claude Code's four extension mechanisms and their context costs and insertion points: "
    "| Mechanism | Unique Capability | Context Cost | Insertion Point | "
    "| MCP servers | External service integration (multi-transport) | High (tool schemas) | model():tool pool | "
    "| Plugins | Multi-component packaging + distribution | Medium (varies) | All three points | "
    "| Skills | Domain-specific instructions + meta-tool invocation | Low (descriptions only) | assemble():context injection | "
    "| Hooks | Lifecycle interception + event-driven automation | Zero by default | execute():pre/post tool | "
    "MCP servers are configured from multiple scopes: project, user, local, and enterprise. "
    "The MCP client (services/mcp/client.ts) supports 8+ transport types: stdio, SSE, HTTP, "
    "WebSocket, SDK, sse-ide, ws-ide, and claudeai-proxy.",
    title="Four extension mechanisms with context costs",
)

tool_pool_assembly_setting = setting(
    "The assembleToolPool() function (tools.ts) is 'the single source of truth for combining "
    "built-in tools with MCP tools.' The five-step assembly pipeline: "
    "(1) Base tool enumeration: getAllBaseTools() returns up to 54 tools — 19 always included "
    "(BashTool, FileReadTool, AgentTool, SkillTool, etc.), 35 conditional on feature flags; "
    "(2) Mode filtering: getTools() applies mode-specific filtering (CLAUDE_CODE_SIMPLE mode "
    "uses only Bash, Read, Edit); "
    "(3) Deny rule pre-filtering: filterToolsByDenyRules() strips blanket-denied tools; "
    "(4) MCP tool integration: MCP tools filtered by deny rules and merged with built-in tools; "
    "(5) Deduplication: built-in tools take precedence over MCP tools.",
    title="Tool pool assembly pipeline",
)

plugin_system_setting = setting(
    "The PluginManifestSchema (utils/plugins/schemas.ts) accepts ten component types: "
    "commands, agents, skills, hooks, MCP servers, LSP servers, output styles, channels, "
    "settings, and user configuration. Plugins are the primary distribution vehicle for "
    "third-party extensions. A single plugin package can extend Claude Code across multiple "
    "component types simultaneously. The plugin loader validates manifests and routes each "
    "component to its respective registry.",
    title="Plugin manifest: ten component types",
)

skills_setting = setting(
    "Each skill is defined by a SKILL.md file with YAML frontmatter. The "
    "parseSkillFrontmatterFields() function (loadSkillsDir.ts) parses 15+ fields including: "
    "display name, description, allowed tools (granting additional tool access), argument hints, "
    "model overrides, execution context ('fork' for isolated execution), associated agent "
    "definitions, effort levels, and shell configuration. Skills can define their own hooks, "
    "which register dynamically on invocation. The SkillTool meta-tool injects skill "
    "instructions into the current context window.",
    title="Skills: SKILL.md with 15+ frontmatter fields",
)

hooks_system_setting = setting(
    "The source defines 27 hook events (coreTypes.ts) spanning: tool authorization (PreToolUse, "
    "PostToolUse, PostToolUseFailure, PermissionRequest, PermissionDenied), session lifecycle "
    "(SessionStart, SessionEnd, Setup, Stop, StopFailure), user interaction (UserPromptSubmit, "
    "Elicitation, ElicitationResult), subagent coordination (SubagentStart, SubagentStop, "
    "TeammateIdle, TaskCreated, TaskCompleted), context management (PreCompact, PostCompact, "
    "InstructionsLoaded, ConfigChange), workspace events (CwdChanged, FileChanged, "
    "WorktreeCreate, WorktreeRemove), and notifications. Of these, 15 have event-specific "
    "output schemas with rich fields. Four hook command types: shell (type: command), "
    "LLM prompt (type: prompt), HTTP (type: http), and agentic verifier (type: agent).",
    title="27 hook events across six categories",
)

# ── Core claims about extensibility ───────────────────────────────────────────

four_mechanisms_justified = claim(
    "Claude Code uses four distinct extension mechanisms (MCP, plugins, skills, hooks) "
    "rather than a single unified mechanism because different kinds of extensibility impose "
    "different costs on the context window. A single mechanism cannot span the full range "
    "from zero-context lifecycle hooks to schema-heavy tool servers without forcing "
    "unnecessary trade-offs on extension authors. The graduated context-cost ordering "
    "(zero for hooks, low for skills, medium for plugins, high for MCP) means cheap "
    "extensions can scale widely without exhausting the context window, while expensive "
    "ones are reserved for cases that genuinely require new tool surfaces.",
    title="Four mechanisms justified by graduated context costs",
    background=[four_mechanisms_setting, principle_composable_extensibility],
)

strat_four_mechanisms = support(
    [context_window_as_binding_constraint],
    four_mechanisms_justified,
    reason=(
        "Given the context window as binding resource constraint "
        "(@context_window_as_binding_constraint), extension mechanisms that add context "
        "overhead unconditionally would conflict with context management goals. "
        "The composable extensibility principle (@principle_composable_extensibility) "
        "motivates multiple mechanisms at different context costs, so that developers "
        "choose the appropriate cost tier. Hooks (zero context cost) handle lifecycle "
        "interception; skills (descriptions only) shape agent behavior; MCP (tool schemas) "
        "add new callable tools. This is confirmed in tools.ts and the mechanism descriptions "
        "(Tier B evidence). The four-mechanism design increases the learning curve but "
        "enables a broader range of extension patterns."
    ),
    prior=0.85,
)

agent_tool_vs_skill_tool = claim(
    "AgentTool and SkillTool sit alongside each other in the base tool pool as meta-tools, "
    "but they differ fundamentally: SkillTool injects instructions into the current context "
    "window (low context cost, same conversation), while AgentTool spawns a new, isolated "
    "context window (high isolation, separate conversation history). This distinction "
    "determines whether an extension operates within or across context boundaries.",
    title="AgentTool vs SkillTool: context window boundary",
    background=[tool_pool_assembly_setting, skills_setting],
)

strat_agent_skill = support(
    [reasoning_separation_claim, context_window_as_binding_constraint],
    agent_tool_vs_skill_tool,
    reason=(
        "The reasoning-execution separation (@reasoning_separation_claim) means tools are "
        "the model's only interface to the outside world. Context window pressure "
        "(@context_window_as_binding_constraint) means the distinction between within-window "
        "(SkillTool) and cross-window (AgentTool) operations matters architecturally. "
        "AgentTool spawns a new queryLoop() with isolated context; SkillTool injects "
        "a SKILL.md's instructions inline. Confirmed from AgentTool.tsx and skills/ "
        "(Tier B evidence)."
    ),
    prior=0.9,
)

tool_pool_pre_filtering = claim(
    "Blanket-denied tools are removed from the model's view before any call via "
    "filterToolsByDenyRules() at tool pool assembly time. This pre-filtering uses the same "
    "matcher as the runtime permission check, so MCP server-prefix rules like mcp__server "
    "strip all tools from that server before the model sees them. This prevents the model "
    "from attempting to invoke forbidden tools, so the model does not waste context on "
    "tool_use requests that would be denied.",
    title="Tool pre-filtering at assembly time",
    background=[tool_pool_assembly_setting],
)

strat_pre_filtering = support(
    [context_window_as_binding_constraint, reasoning_separation_claim],
    tool_pool_pre_filtering,
    reason=(
        "Context pressure (@context_window_as_binding_constraint) motivates removing "
        "denied tools before the model sees them — tool schemas consume context budget. "
        "The reasoning-execution separation (@reasoning_separation_claim) means the harness "
        "controls what the model can reach; pre-filtering is the harness's enforcement at "
        "the tool surface level. This is confirmed in tools.ts filterToolsByDenyRules() "
        "(Tier B evidence) and documented as a security measure in the authorization pipeline."
    ),
    prior=0.88,
)
