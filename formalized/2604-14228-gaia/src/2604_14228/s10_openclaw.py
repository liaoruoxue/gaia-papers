"""Section 10: Comparative Analysis — Claude Code vs. OpenClaw"""

from gaia.lang import claim, setting, support, compare

from .s2_values_principles import five_values_motivate_architecture
from .s3_architecture import (
    reasoning_separation_claim,
    context_window_as_binding_constraint,
)
from .s5_permissions import deny_first_motivated_by_approval_fatigue
from .s7_context_memory import file_based_memory_vs_alternatives
from .s8_subagents import isolated_context_boundaries

# ── Settings ───────────────────────────────────────────────────────────────────

comparison_table_setting = setting(
    "Architectural comparison: Claude Code vs. OpenClaw across six design dimensions. "
    "| Dimension | Claude Code | OpenClaw | "
    "| System scope | CLI/IDE coding harness, ephemeral per-session process | Persistent WS gateway daemon, multi-channel control plane | "
    "| Trust model | Deny-first per-action rule evaluation with hooks and optional ML classifier; 7 permission modes; graduated trust spectrum | Single trusted operator per gateway; DM pairing and allowlists for inbound channels; opt-in sandboxing with configurable scope (per-agent, per-session, or shared) and multiple backends | "
    "| Agent runtime | Iterative async generator (queryLoop()) as system center | Pi-agent runner embedded inside gateway RPC dispatch; per-session queue serialization (with optional global lane) | "
    "| Extension architecture | 4 mechanisms at graduated context costs: MCP, plugins, skills, hooks | Manifest-first plugin system with 12 capability types and central registry; separate skills layer; built-in MCP via openclaw mcp (server and outbound client registry) | "
    "| Memory and context | CLAUDE.md 4-level hierarchy; 5-layer compaction pipeline; LLM-based memory scan | Workspace bootstrap files (AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, plus conditionally BOOTSTRAP.md, HEARTBEAT.md, MEMORY.md); separate memory system (MEMORY.md, daily notes, optional DREAMS.md); auto-compaction with pluggable providers; optional hybrid search (vector + keyword, conditional on embedding provider); experimental dreaming for long-term promotion | "
    "| Multi-agent and routing | Task-delegating subagents (e.g., Explore, Plan, general-purpose); worktree isolation; final response text returned to parent | Two separate concerns: (a) multi-agent routing with isolated agents, distinct workspaces, and binding-based channel dispatch; (b) sub-agent delegation with configurable nesting depth (max 5, default 1, recommended 2) and thread-bound sessions |",
    title="Six-dimension comparison table: Claude Code vs. OpenClaw",
)

openclaw_scope_setting = setting(
    "OpenClaw is a persistent control plane for multi-channel personal assistance. It runs as a "
    "persistent daemon (default port 18789, loopback-only) that owns all messaging surface "
    "connections and coordinates clients, tools, and device nodes over a typed WebSocket protocol. "
    "OpenClaw can host Claude Code, OpenAI Codex, and Gemini CLI as external coding harnesses "
    "through its ACP (Agent Client Protocol) integration, making the two systems stackable "
    "rather than purely alternative.",
    title="OpenClaw system scope: persistent multi-channel gateway",
)

openclaw_trust_setting = setting(
    "OpenClaw assumes a single trusted operator per gateway instance. Its security architecture "
    "begins with identity and access control (DM pairing codes, sender allowlists, gateway "
    "authentication) rather than per-action safety classification. Tool policy uses configurable "
    "allow/deny lists per agent rather than a centralized classifier. Sandboxing is available as "
    "an opt-in feature with multiple backends (Docker, SSH, or OpenShell) and configurable scope "
    "(per-agent, per-session, or shared). The OpenClaw security documentation explicitly states "
    "that hostile multi-tenant isolation on a shared gateway is not a supported security boundary.",
    title="OpenClaw trust model: perimeter-level vs. per-action",
)

openclaw_memory_setting = setting(
    "OpenClaw injects workspace bootstrap files into the system prompt at session start: five core "
    "files (AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md) plus conditionally BOOTSTRAP.md, "
    "HEARTBEAT.md, and MEMORY.md, with large files truncated. The memory system manages three file "
    "types: MEMORY.md for long-term durable facts, date-stamped daily notes (memory/YYYY-MM-DD.md), "
    "and an optional DREAMS.md for dreaming sweep summaries. When an embedding provider is "
    "configured, memory search uses hybrid retrieval combining vector similarity with keyword "
    "matching. An experimental dreaming system performs background consolidation, scoring candidates "
    "and promoting only qualified items from short-term recall into long-term memory.",
    title="OpenClaw memory: bootstrap files, daily notes, dreaming",
)

# ── Core claims about the comparison ──────────────────────────────────────────

different_trust_boundaries = claim(
    "Claude Code and OpenClaw place the trust boundary at fundamentally different points. "
    "Claude Code places the trust boundary between the model and the execution environment, "
    "evaluating every tool invocation via a deny-first permission system with ML-based "
    "classification. OpenClaw places the trust boundary at the gateway perimeter: security "
    "begins with identity and access control (DM pairing, sender allowlists, gateway "
    "authentication), and per-action classification is replaced by per-agent allow/deny lists. "
    "These represent genuinely different architectural bets that follow from different "
    "deployment contexts: Claude Code assumes an untrusted model on a trusted developer machine; "
    "OpenClaw assumes a single trusted operator per gateway.",
    title="Different trust boundary locations follow from different deployment contexts",
    background=[comparison_table_setting, openclaw_trust_setting],
)

pred_cc_trust = claim(
    "Claude Code's per-action deny-first trust model predicts: every tool invocation subject "
    "to evaluation, graduated modes for different autonomy levels, ML classifier for automated "
    "safety, defense-in-depth with independent layers.",
    title="Claude Code trust model predictions",
)

pred_oc_trust = claim(
    "OpenClaw's perimeter-level trust model predicts: identity-first security with DM pairing, "
    "per-agent (not per-action) allow/deny lists, opt-in sandboxing, no centralized classifier.",
    title="OpenClaw trust model predictions",
)

obs_trust_design = claim(
    "Observed: Claude Code implements deny-first per-action evaluation with 7 permission modes "
    "and an ML classifier; OpenClaw implements gateway-perimeter authentication with DM pairing "
    "and per-agent lists. Both systems match their respective trust model predictions.",
    title="Observed: different trust implementations match different deployment contexts",
)

strat_trust_boundary = support(
    [pred_cc_trust, deny_first_motivated_by_approval_fatigue],
    different_trust_boundaries,
    reason=(
        "Claude Code's deny-first per-action trust (@deny_first_motivated_by_approval_fatigue) "
        "is motivated by the untrusted-model assumption. OpenClaw's perimeter-level trust "
        "follows from the single-trusted-operator assumption. The predictions of each model "
        "match the observed implementations, confirming that trust boundary placement is "
        "a consequence of the deployment context, not an arbitrary design choice. "
        "Confirmed from the comparison table (Table 3) and trust model documentation (Tier C)."
    ),
    prior=0.88,
)

comp_trust = compare(
    pred_cc_trust, pred_oc_trust, obs_trust_design,
    reason=(
        "Claude Code matches the per-action evaluation prediction; OpenClaw matches the "
        "perimeter-level prediction. The architectural inversions are not arbitrary — "
        "they follow from different trust models and deployment topologies."
    ),
    prior=0.85,
)

loop_vs_control_plane = claim(
    "In Claude Code, the queryLoop() async generator is the architectural center: all interfaces "
    "feed into it, and it directly manages context assembly, model calls, tool dispatch, and "
    "recovery. In OpenClaw, the agent runtime (an embedded Pi-agent core) sits inside a larger "
    "gateway dispatch layer. The gateway's agent RPC validates parameters and returns immediately; "
    "the embedded runner then executes the agentic loop while emitting lifecycle and stream "
    "events back through the gateway protocol. Both systems follow the ReAct pattern, but "
    "OpenClaw's loop is a component within a control plane rather than the control plane itself.",
    title="Query loop as center vs. embedded in gateway control plane",
    background=[comparison_table_setting],
)

strat_loop_position = support(
    [reasoning_separation_claim, isolated_context_boundaries],
    loop_vs_control_plane,
    reason=(
        "The reasoning-execution separation (@reasoning_separation_claim) applies in both systems, "
        "but the position of the loop in the overall architecture differs. Claude Code's "
        "isolated context design (@isolated_context_boundaries) places the loop at the center "
        "with all context assembly there. OpenClaw's multi-channel design requires a gateway "
        "control plane above the loop, with the loop emitting events upward. The different "
        "architectural positions follow from the different system scopes (CLI harness vs. "
        "persistent gateway). Confirmed from the comparison table (Table 3, Tier C)."
    ),
    prior=0.85,
)

context_management_inversion = claim(
    "Claude Code and OpenClaw make opposite bets on context management. Claude Code invests in "
    "graduated context compression (five layers with cache-awareness), while OpenClaw invests in "
    "structured long-term memory promotion (dreaming, daily notes, hybrid vector+keyword search). "
    "Both systems share the design commitment to user-visible, editable memory files — the "
    "transparent file-based configuration principle applies to both. OpenClaw also supports "
    "pluggable compaction providers, but its compaction pipeline is less graduated than "
    "Claude Code's five-layer system.",
    title="Context inversion: graduated compression vs. structured long-term promotion",
    background=[comparison_table_setting, openclaw_memory_setting],
)

strat_context_inversion = support(
    [context_window_as_binding_constraint, file_based_memory_vs_alternatives],
    context_management_inversion,
    reason=(
        "Both systems face the context window as a binding resource constraint "
        "(@context_window_as_binding_constraint), but address it differently. Claude Code's "
        "coding-focused, session-scoped design benefits from aggressive graduated compression. "
        "OpenClaw's persistent multi-session gateway design benefits from structured long-term "
        "memory promotion (dreaming) that prevents important facts from being compressed away "
        "across sessions. Both use file-based transparent memory (@file_based_memory_vs_alternatives), "
        "consistent with the transparent configuration principle "
        "(@principle_transparent_file_config). Confirmed from Table 3 (Tier C evidence)."
    ),
    prior=0.85,
)

composable_layered_design_space = claim(
    "The compositional relationship between Claude Code and OpenClaw is architecturally "
    "significant: OpenClaw can host Claude Code as an external coding harness via ACP "
    "(Agent Client Protocol), meaning the two systems are composable rather than exclusive "
    "alternatives. This suggests the design space of AI agents is not a flat taxonomy but "
    "a layered one, where gateway-level systems and task-level harnesses can compose. "
    "The three observations from the comparison: (1) the same recurring design questions "
    "apply beyond coding agents; (2) the systems make opposite bets on several dimensions "
    "following from different trust models and deployment topologies; "
    "(3) the compositional relationship between the two systems is architecturally significant.",
    title="Layered design space: gateway systems and task harnesses compose",
    background=[openclaw_scope_setting, comparison_table_setting],
)

strat_composable = support(
    [reasoning_separation_claim],
    composable_layered_design_space,
    reason=(
        "The composable extensibility principle (@principle_composable_extensibility) in Claude "
        "Code is designed to make it usable as a component. The ACP integration in OpenClaw "
        "confirms that the reasoning-execution separation (@reasoning_separation_claim) — "
        "model invoked as stateless endpoint — makes Claude Code composable within a larger "
        "gateway. The layered design space observation is a direct architectural consequence "
        "of this separability. Confirmed from OpenClaw documentation and ACP integration "
        "description (Tier C evidence)."
    ),
    prior=0.82,
)
