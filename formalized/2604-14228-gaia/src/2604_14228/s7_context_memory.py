"""Section 7: Context Construction and Memory"""

from gaia.lang import claim, setting, support, compare, abduction

from .s2_values_principles import (
    principle_context_as_scarce_resource,
    principle_transparent_file_config,
)
from .s3_architecture import context_window_as_binding_constraint, reasoning_separation_claim
from .s4_query_loop import graduated_compaction_claim

# ── Settings ───────────────────────────────────────────────────────────────────

context_window_assembly_setting = setting(
    "The context window is assembled from the following sources in order: "
    "(1) System prompt (including output style modifications and --append-system-prompt); "
    "(2) Environment info via getSystemContext() (git status, optional cache-breaking); memoized; "
    "(3) CLAUDE.md hierarchy via getUserContext() — four-level instruction file hierarchy; memoized; "
    "(4) Path-scoped rules (.claude/rules/*) — load lazily when agent reads files in matching directories; "
    "(5) Auto memory — contextually relevant memory entries prefetched asynchronously; "
    "(6) Tool metadata — skill descriptions, MCP tool names, deferred tool definitions (via ToolSearch); "
    "(7) Conversation history — carried forward, subject to compaction; "
    "(8) Tool results — file reads, command outputs, subagent summaries; "
    "(9) Compact summaries — replacing older history segments. "
    "CLAUDE.md content is delivered as user context (a user message), not as system prompt content, "
    "meaning model compliance is probabilistic rather than guaranteed.",
    title="Nine-source context window assembly order",
)

claudemd_hierarchy_setting = setting(
    "CLAUDE.md files follow a four-level loading hierarchy (claudemd.ts): "
    "(1) Managed memory (e.g., /etc/claude-code/CLAUDE.md on Linux) — OS-level policy; "
    "(2) User memory (~/.claude/CLAUDE.md) — private global instructions; "
    "(3) Project memory (CLAUDE.md, .claude/CLAUDE.md, .claude/rules/*.md) — in-repo instructions; "
    "(4) Local memory (CLAUDE.local.md) — gitignored private project-specific instructions. "
    "Files load in 'reverse order of priority': later-loaded files receive more model attention. "
    "Memory files support an @include directive for modular instruction sets. "
    "CLAUDE.md content occupies a different structural position in the API request than the "
    "system prompt, potentially affecting model attention patterns.",
    title="CLAUDE.md four-level hierarchy",
)

llm_memory_scan_setting = setting(
    "The system uses an LLM-based scan of memory-file headers to select up to five relevant "
    "files on demand, surfacing them at file granularity rather than entry granularity. "
    "This contrasts with embedding-based retrieval, which can retrieve individual entries more "
    "selectively at the cost of inspectability and the infrastructure needed to maintain an index.",
    title="LLM-based memory scan (not embedding-based)",
)

compaction_pipeline_output_setting = setting(
    "The buildPostCompactMessages() function (compact.ts) returns a compacted output structure: "
    "[boundaryMarker, ...summaryMessages, ...messagesToKeep, ...attachments, ...hookResults]. "
    "The boundary marker records headUuid, anchorUuid, and tailUuid via "
    "annotateBoundaryWithPreservedSegment() to enable read-time chain patching. "
    "This mostly-append design means compaction never modifies or deletes previously written "
    "transcript lines; it only appends new boundary and summary events. "
    "A GrowthBook feature flag controls whether the compaction path reuses the main "
    "conversation's prompt cache (a January 2026 experiment: 'false path is 98% cache miss, "
    "costs ~0.76% of fleet cache_creation').",
    title="Compaction output structure with UUID boundary markers",
)

# ── Core claims ────────────────────────────────────────────────────────────────

file_based_memory_vs_alternatives = claim(
    "Claude Code uses a file-based transparent memory architecture (CLAUDE.md files as "
    "plain-text Markdown) rather than structured configuration, opaque databases, or "
    "embedding-based retrieval. This trades expressiveness for auditability: users can "
    "read, edit, version-control, and delete any instruction the agent sees. The system "
    "does not use embeddings or a vector similarity index for memory retrieval.",
    title="File-based transparent memory vs. alternatives",
    background=[claudemd_hierarchy_setting, llm_memory_scan_setting],
)

# Build abduction: file-based vs. embedding-based memory

pred_file_based = claim(
    "File-based memory (CLAUDE.md markdown files) predicts: full user auditability and "
    "editability of agent instructions, version-control integration, zero additional "
    "infrastructure required, and retrieval at file granularity (not entry granularity).",
    title="File-based memory predictions",
)

pred_embedding_based = claim(
    "Embedding-based memory predicts: selective entry-level retrieval, opaque indexing "
    "infrastructure requirement, inability for users to easily inspect what the retrieval "
    "system considers relevant, and scalable to large memory stores.",
    title="Embedding-based memory predictions",
)

obs_memory_design = claim(
    "Claude Code's observed memory design: CLAUDE.md files are plain-text Markdown, "
    "user-visible and version-controllable; retrieval uses an LLM-based scan of file "
    "headers (not vector similarity); no embedding infrastructure is required; "
    "surfacing is at file granularity (up to 5 files on demand).",
    title="Observed: file-based memory with LLM scan",
)

support_file_based_memory = support(
    [pred_file_based], obs_memory_design,
    reason=(
        "File-based memory predictions (auditability, editability, version control, "
        "file-granularity retrieval) directly match the observed design: CLAUDE.md files "
        "are plain-text Markdown readable by users, committed alongside the codebase, "
        "and retrieved via LLM scan at file granularity. The transparent file-based "
        "configuration principle (@principle_transparent_file_config) motivates this choice."
    ),
    prior=0.92,
)

support_embedding_memory = support(
    [pred_embedding_based], obs_memory_design,
    reason=(
        "Embedding-based memory predictions (entry-level retrieval, opaque infrastructure) "
        "do not match the observed design: no embedding index exists; retrieval is at file "
        "granularity; users can inspect all instructions. The embedding approach would "
        "provide more selective retrieval but at the cost of inspectability."
    ),
    prior=0.2,
)

comp_memory = compare(
    pred_file_based, pred_embedding_based, obs_memory_design,
    reason=(
        "File-based memory matches all observed properties (auditability, no embedding "
        "infrastructure, file-granularity retrieval). Embedding-based memory would provide "
        "better entry-level selectivity but conflicts with the transparent file-based "
        "configuration principle and the observed implementation."
    ),
    prior=0.88,
)

abd_file_based_memory = abduction(
    support_file_based_memory, support_embedding_memory, comp_memory,
    reason="Both file-based and embedding-based memory are architectural alternatives for the same goal of relevant context retrieval",
)

claudemd_probabilistic_compliance = claim(
    "Because CLAUDE.md content is delivered as user context (a user message) rather than "
    "as system prompt content (context.ts), model compliance with CLAUDE.md instructions "
    "is probabilistic rather than guaranteed. This creates a deliberate separation between "
    "guidance (CLAUDE.md, probabilistic) and enforcement (permission rules, deterministic). "
    "The function setCachedClaudeMdContent() caches loaded content for the auto-mode "
    "classifier, avoiding an import cycle between the CLAUDE.md loader and the permission system.",
    title="CLAUDE.md compliance is probabilistic; permission rules are deterministic",
    background=[context_window_assembly_setting, claudemd_hierarchy_setting],
)

strat_probabilistic_compliance = support(
    [file_based_memory_vs_alternatives, reasoning_separation_claim],
    claudemd_probabilistic_compliance,
    reason=(
        "The file-based memory architecture (@file_based_memory_vs_alternatives) uses "
        "CLAUDE.md as user context — a pragmatic choice that enables version control "
        "and editability but means the model treats instructions as conversational context "
        "rather than system-level commands. The reasoning-execution separation "
        "(@reasoning_separation_claim) means the harness (permission rules) provides "
        "deterministic enforcement while the model (processing CLAUDE.md as user context) "
        "provides probabilistic guidance-following. This is confirmed in context.ts "
        "and claudemd.ts (Tier B evidence)."
    ),
    prior=0.87,
)
