"""Section 3: Architecture Overview — Seven Components and Five Layers"""

from gaia.lang import claim, setting, support, deduction

from .motivation import claude_code_description, source_code_analysis_method
from .s2_values_principles import (
    principle_minimal_scaffolding,
    principle_deny_first,
    principle_defense_in_depth,
    principle_context_as_scarce_resource,
    five_values_motivate_architecture,
    design_principles_distinguish_from_alternatives,
)

# ── Architecture settings ──────────────────────────────────────────────────────

seven_component_model = setting(
    "Claude Code's high-level system structure decomposes into seven functional components: "
    "(1) User (submits prompts, approves permissions, reviews output), "
    "(2) Interfaces (interactive CLI, headless CLI 'claude -p', Agent SDK, IDE/Desktop/Browser), "
    "(3) Agent loop (iterative cycle implemented as queryLoop() async generator in query.ts), "
    "(4) Permission system (deny-first rule evaluation in permissions.ts, auto-mode ML classifier, "
    "hook-based interception), "
    "(5) Tools (up to 54 built-in tools assembled via assembleToolPool() in tools.ts), "
    "(6) State and persistence (append-only JSONL session transcripts in sessionStorage.ts), "
    "(7) Execution environment (shell, filesystem, web, MCP server connections). "
    "All entry surfaces converge on the same agent loop.",
    title="Seven-component high-level system structure",
)

five_layer_decomposition = setting(
    "The layered subsystem decomposition expands into five layers: "
    "(1) Surface layer: src/entrypoints/, src/screens/, src/components/ — entry points and rendering; "
    "(2) Core layer: queryLoop() async generator in query.ts, compaction pipeline — agent loop; "
    "(3) Safety/action layer: permissions.ts, yoloClassifier.ts, hook pipeline (27 event types), "
    "extensibility (plugins, skills), built-in and MCP tools, shell sandbox, subagent spawning; "
    "(4) State layer: context assembly (context.ts), runtime state (src/state/), session persistence "
    "(sessionStorage.ts), CLAUDE.md + memory (claudemd.ts), sidechain transcripts; "
    "(5) Backend layer: execution backends, external resources, MCP server connections.",
    title="Five-layer subsystem decomposition",
)

# ── Core architectural design questions answered ────────────────────────────────

reasoning_separation_claim = claim(
    "In Claude Code, the model reasons about what to do while the harness executes actions. "
    "The model emits tool_use blocks; the harness (query.ts) parses them, checks permissions, "
    "dispatches them to tool implementations, and collects results. The model never directly "
    "accesses the filesystem, runs shell commands, or makes network requests. "
    "Community analysis of the extracted source estimates that only approximately 1.6% of "
    "Claude Code's codebase constitutes AI decision logic, with the remaining 98.4% being "
    "operational infrastructure.",
    title="Model reasons; harness executes (1.6%/98.4% split)",
)

strat_reasoning_separation = support(
    [five_values_motivate_architecture],
    reasoning_separation_claim,
    reason=(
        "The principle of minimal scaffolding (@principle_minimal_scaffolding) directly "
        "predicts that the operational harness should dominate code volume. The deny-first "
        "principle (@principle_deny_first) requires that permission checks live in the "
        "harness (not in the model), since a compromised model should not be able to "
        "override sandboxing or deny-first rules. The 1.6%/98.4% split is measured from "
        "the extracted TypeScript source (Tier C evidence), consistent with both principles. "
        "The security consequence: because reasoning and enforcement occupy separate code paths, "
        "a compromised or adversarially manipulated model cannot override harness safety checks."
    ),
    prior=0.87,
)

single_query_loop_claim = claim(
    "Claude Code uses a single queryLoop() function that executes regardless of whether the "
    "user is interacting through an interactive terminal, a headless CLI invocation (claude -p), "
    "the Agent SDK, or an IDE integration (query.ts). Only the rendering and user-interaction "
    "layer varies. This is distinct from mode-specific engines that trade uniformity for "
    "surface-specific optimization.",
    title="Single queryLoop() for all surfaces",
    background=[seven_component_model],
)

strat_single_loop = support(
    [reasoning_separation_claim],
    single_query_loop_claim,
    reason=(
        "The minimal scaffolding principle (@principle_minimal_scaffolding) favors a single "
        "shared loop over mode-specific engines. Given that the model reasons and the harness "
        "executes (@reasoning_separation_claim), a single queryLoop() suffices because the "
        "variation across surfaces is only in rendering and user interaction, not in the "
        "core model-harness protocol. This is confirmed in query.ts (Tier B evidence)."
    ),
    prior=0.9,
)

deny_first_safety_posture = claim(
    "Claude Code's default safety posture is deny-first with human escalation: deny rules "
    "override ask rules override allow rules, and unrecognized actions are escalated to the "
    "user rather than allowed silently (permissions.ts). Multiple independent safety layers "
    "apply in parallel: permission rules, PreToolUse hooks, the auto-mode classifier when "
    "enabled, and optional shell sandboxing. Any single layer can block an action.",
    title="Deny-first default safety posture with layered defense",
    background=[principle_deny_first, principle_defense_in_depth],
)

strat_deny_first_posture = support(
    [five_values_motivate_architecture],
    deny_first_safety_posture,
    reason=(
        "Both the human decision authority and safety values "
        "(@five_values_motivate_architecture) jointly motivate a deny-first default: "
        "deny-first preserves human authority by escalating rather than silently allowing, "
        "while defense in depth protects against single-layer failures. This is confirmed "
        "directly from permissions.ts (Tier B evidence). The alternative — SWE-Agent's "
        "container isolation or Aider's git rollback — reflects different value weightings."
    ),
    prior=0.92,
)

context_window_as_binding_constraint = claim(
    "In Claude Code, the context window (200K tokens for older models, 1M tokens for the "
    "Claude 4.6 series) is the binding resource constraint. Five distinct context-reduction "
    "strategies execute before every model call (query.ts lines 365-453): budget reduction, "
    "snip, microcompact, context collapse, and auto-compact. Several subsystem decisions "
    "also exist to limit context consumption: CLAUDE.md lazy loading, deferred tool schemas, "
    "summary-only subagent returns, and per-tool-result budgets.",
    title="Context window as binding resource constraint with five-layer pipeline",
    background=[principle_context_as_scarce_resource, five_layer_decomposition],
)

strat_context_constraint = support(
    [five_values_motivate_architecture, reasoning_separation_claim],
    context_window_as_binding_constraint,
    reason=(
        "Reliable execution and capability amplification (@five_values_motivate_architecture) "
        "both require effective context management. Since the harness executes and the model "
        "reasons (@reasoning_separation_claim), and since increasingly capable models benefit "
        "from a rich operational environment, the context window becomes the primary bottleneck "
        "worth engineering around. The five-layer pipeline is confirmed in query.ts "
        "(Tier B evidence); no single strategy addresses all types of context pressure, "
        "motivating the graduated approach."
    ),
    prior=0.88,
)

seven_independent_safety_layers = claim(
    "The safety-by-default principle is implemented through seven independent layers. "
    "A request must pass through all applicable layers, and any single layer can block it: "
    "(1) Tool pre-filtering (tools.ts) — blanket-denied tools removed before any call; "
    "(2) Deny-first rule evaluation (permissions.ts) — deny always overrides allow; "
    "(3) Permission mode constraints (types/permissions.ts) — active mode sets baseline; "
    "(4) Auto-mode classifier (yoloClassifier.ts) — ML-based evaluation; "
    "(5) Shell sandboxing (shouldUseSandbox.ts) — filesystem and network isolation; "
    "(6) Not restoring permissions on resume (conversationRecovery.ts); "
    "(7) Hook-based interception (types/hooks.ts) — PreToolUse and PermissionRequest hooks.",
    title="Seven independent safety layers",
    background=[principle_defense_in_depth, five_layer_decomposition],
)

strat_seven_layers = support(
    [deny_first_safety_posture, five_values_motivate_architecture],
    seven_independent_safety_layers,
    reason=(
        "Given the deny-first safety posture (@deny_first_safety_posture), defense in depth "
        "requires multiple independent layers. The seven-layer structure "
        "is confirmed from specific source files: permissions.ts, tools.ts, "
        "yoloClassifier.ts, shouldUseSandbox.ts, conversationRecovery.ts, types/hooks.ts "
        "(Tier B evidence). The independence assumption — if one layer fails, others catch "
        "the violation — is the key architectural bet. Each layer uses a different "
        "technique (declarative rules, ML classification, OS-level sandboxing, hooks), "
        "reducing common failure modes."
    ),
    prior=0.9,
)

architecture_coherence = claim(
    "Claude Code's architectural choices form a coherent design point: the 1.6% decision "
    "logic / 98.4% operational harness ratio, the single queryLoop() for all surfaces, "
    "the deny-first safety posture, and the five-layer context pipeline all follow directly "
    "from the five values and thirteen design principles. The architecture consistently "
    "prioritizes model autonomy within deterministic harness constraints.",
    title="Architecture is coherent with stated values and principles",
)

strat_coherence = support(
    [
        reasoning_separation_claim,
        single_query_loop_claim,
        deny_first_safety_posture,
        context_window_as_binding_constraint,
    ],
    architecture_coherence,
    reason=(
        "Each individual architectural choice (@reasoning_separation_claim, "
        "@single_query_loop_claim, @deny_first_safety_posture, "
        "@context_window_as_binding_constraint) independently follows from the values "
        "and principles. Their joint coherence is structural: a system that trusts the "
        "model to reason freely (minimal scaffolding) must rely on the harness for all "
        "safety guarantees (deny-first + defense-in-depth), must have a single loop to "
        "maintain this invariant across surfaces, and must manage context aggressively "
        "because context is what the model reasons over."
    ),
    prior=0.85,
)
