"""Section 4: Turn Execution — The Agentic Query Loop"""

from gaia.lang import claim, setting, support, deduction

from .s2_values_principles import (
    principle_minimal_scaffolding,
    principle_context_as_scarce_resource,
    principle_graceful_recovery,
    principle_reversibility_weighted,
)
from .s3_architecture import (
    single_query_loop_claim,
    reasoning_separation_claim,
    context_window_as_binding_constraint,
)

# ── Query pipeline settings ────────────────────────────────────────────────────

react_pattern_setting = setting(
    "The ReAct pattern (Yao et al., 2022) is the orchestration pattern where the model "
    "generates reasoning and tool invocations, the harness executes actions, and results "
    "feed the next iteration. This pattern commits to one action sequence per turn without "
    "backtracking, trading search completeness for simplicity and latency.",
    title="ReAct pattern definition",
)

query_pipeline_steps = setting(
    "Each turn of the queryLoop() follows a fixed nine-step sequence (query.ts): "
    "(1) settings resolution — destructure immutable parameters; "
    "(2) mutable state initialization — single State object, updated at seven 'continue sites'; "
    "(3) context assembly — getMessagesAfterCompactBoundary() retrieves post-compaction messages; "
    "(4) pre-model context shapers — five shapers execute sequentially; "
    "(5) model call — for await over deps.callModel() streams the response; "
    "(6) tool-use dispatch — tool_use blocks flow to tool orchestration; "
    "(7) permission gate — each tool request through the permission system; "
    "(8) tool execution and result collection — tool_result messages added; "
    "(9) stop condition — no tool_use blocks (text-only response) terminates the turn.",
    title="Nine-step query pipeline",
)

streaming_tool_executor_setting = setting(
    "StreamingToolExecutor (StreamingToolExecutor.ts) executes tools as they stream in from "
    "the model response, managing concurrent execution with two coordination mechanisms: "
    "(1) sibling abort controller — fires when any Bash tool errors, terminating other in-flight "
    "subprocesses; (2) progress-available signal — wakes the getRemainingResults() consumer. "
    "Results are buffered and emitted in order tools were received, preserving tool result "
    "ordering even when tools run in parallel. Read-only operations execute in parallel; "
    "state-modifying operations like shell commands are serialized.",
    title="StreamingToolExecutor design",
)

five_context_shapers_setting = setting(
    "Five pre-model context shapers execute sequentially in query.ts before every model call: "
    "(1) Budget reduction (applyToolResultBudget()): enforces per-message size limits on tool "
    "results, replacing oversized outputs with content references; always active. "
    "(2) Snip (snipCompactIfNeeded(), gated by HISTORY_SNIP): lightweight older-history trim; "
    "snipTokensFreed is passed to auto-compact because the main token counter cannot see snip's savings. "
    "(3) Microcompact (gated by CACHED_MICROCOMPACT): fine-grained cache-aware compression; "
    "boundary messages deferred until after API response to use actual cache_deleted_input_tokens. "
    "(4) Context collapse (gated by CONTEXT_COLLAPSE): read-time projection over conversation "
    "history; does not mutate stored history; summary messages live in the collapse store, not the REPL array. "
    "(5) Auto-compact: full model-generated summary via compactConversation() in compact.ts; "
    "fires only when context still exceeds pressure threshold after all previous shapers.",
    title="Five pre-model context shapers",
)

stop_conditions_setting = setting(
    "Five conditions can terminate the queryLoop(): "
    "(1) No tool use — model produces only text content (primary stop condition); "
    "(2) Max turns — configurable maxTurns limit reached; "
    "(3) Context overflow — API returns prompt_too_long; "
    "(4) Hook intervention — PostToolUse hook sets hook_stopped_continuation; "
    "(5) Explicit abort — abortController signal fires.",
    title="Five loop stop conditions",
)

# ── Core claims about the agent loop ──────────────────────────────────────────

react_orchestration_claim = claim(
    "Claude Code's core loop follows the ReAct pattern: the model generates reasoning and "
    "tool invocations, the harness executes actions, and results feed the next iteration. "
    "This reactive design trades search completeness for simplicity and latency: each turn "
    "commits to one action sequence without backtracking. Among Anthropic's five composable "
    "workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, "
    "evaluator-optimizer), Claude Code primarily uses the orchestrator-workers pattern "
    "for subagent delegation while keeping the core loop reactive.",
    title="ReAct orchestration with orchestrator-workers for subagents",
    background=[react_pattern_setting, query_pipeline_steps],
)

strat_react = support(
    [single_query_loop_claim, reasoning_separation_claim],
    react_orchestration_claim,
    reason=(
        "The single queryLoop() (@single_query_loop_claim) that serves all surfaces is "
        "structurally compatible with the ReAct pattern: each iteration calls the model "
        "exactly once, dispatches tool_use results, and loops. Because the model reasons "
        "and the harness executes (@reasoning_separation_claim), the ReAct pattern is "
        "the natural fit — the model emits actions, the harness performs them. "
        "This is confirmed in query.ts (Tier B evidence). The orchestrator-workers "
        "extension for subagents is documented in Anthropic's 'Building Effective Agents' "
        "(Tier A evidence)."
    ),
    prior=0.92,
)

graduated_compaction_claim = claim(
    "The five-layer compaction pipeline implements a lazy-degradation principle: apply the "
    "least disruptive compression first (budget reduction, always active), then snip, "
    "microcompact, context collapse, and finally auto-compact (which triggers a full "
    "model-generated summary). Earlier, cheaper layers run before costlier ones. Each layer "
    "operates at a different cost-benefit tradeoff, and no single strategy addresses all "
    "types of context pressure. The cost of this approach is complexity: five interacting "
    "compression layers, several gated by feature flags, create behavior difficult for users "
    "to fully predict. Context collapse operates without user-visible output.",
    title="Five-layer compaction: lazy-degradation principle",
    background=[five_context_shapers_setting, principle_context_as_scarce_resource],
)

strat_graduated_compaction = support(
    [context_window_as_binding_constraint],
    graduated_compaction_claim,
    reason=(
        "Given the context window as binding resource constraint "
        "(@context_window_as_binding_constraint), a single compaction strategy is "
        "insufficient. Budget reduction handles per-tool overflow, snip handles temporal "
        "depth, microcompact handles cache overhead, context collapse handles long histories, "
        "and auto-compact performs semantic compression as last resort. The graduated "
        "approach is confirmed in query.ts lines 365-453 (Tier B evidence). Each layer's "
        "cost-aggressiveness ordering is: budget reduction (lightest, always active) through "
        "auto-compact (heaviest, user-configurable), consistent with lazy-degradation."
    ),
    prior=0.88,
)

concurrent_serial_tool_execution = claim(
    "The tool dispatch mechanism uses concurrent-read, serial-write execution: read-only "
    "operations execute in parallel via StreamingToolExecutor, while state-modifying "
    "operations like shell commands are serialized. This occupies a middle ground between "
    "fully serial dispatch and speculative pre-execution (PASTE approach). Results are "
    "buffered and emitted in the order tools were received, preserving the ordering the "
    "model expects for tool results.",
    title="Concurrent-read, serial-write tool execution",
    background=[streaming_tool_executor_setting],
)

strat_concurrent_serial = support(
    [reasoning_separation_claim],
    concurrent_serial_tool_execution,
    reason=(
        "The reasoning-execution separation (@reasoning_separation_claim) means the harness "
        "controls tool execution order. The reversibility-weighted risk principle "
        "(@principle_reversibility_weighted) motivates lighter constraints on read-only "
        "(reversible) operations and serialization for state-modifying (irreversible) ones. "
        "Concurrent reads improve latency without risk; serialized writes prevent races. "
        "This is confirmed from StreamingToolExecutor.ts and toolOrchestration.ts "
        "(Tier B evidence)."
    ),
    prior=0.85,
)

recovery_mechanisms_claim = claim(
    "The query loop implements five recovery mechanisms for edge cases: "
    "(1) max output tokens escalation — retry with escalated limit, up to three attempts "
    "(MAX_OUTPUT_TOKENS_RECOVERY_LIMIT = 3); "
    "(2) reactive compaction (gated by REACTIVE_COMPACT) — summarize just enough to free space, "
    "fires at most once per turn; "
    "(3) prompt-too-long handling — attempt context-collapse overflow recovery and reactive "
    "compaction before terminating; "
    "(4) streaming fallback — retry with different strategy via onStreamingFallback callback; "
    "(5) fallback model — switch to alternative model if primary fails via fallbackModel parameter.",
    title="Five loop recovery mechanisms",
    background=[stop_conditions_setting],
)

strat_recovery = support(
    [context_window_as_binding_constraint],
    recovery_mechanisms_claim,
    reason=(
        "Graceful recovery (@principle_graceful_recovery) requires handling edge cases "
        "without hard failure. Context-window pressure (@context_window_as_binding_constraint) "
        "makes prompt-too-long a predictable error requiring specific recovery sequences. "
        "The five recovery mechanisms form a graded response: lightweight token escalation "
        "before heavy model switching. These are confirmed from query.ts implementation "
        "(Tier B evidence). The recovery-oriented design means errors become routing signals "
        "rather than hard stops."
    ),
    prior=0.85,
)
