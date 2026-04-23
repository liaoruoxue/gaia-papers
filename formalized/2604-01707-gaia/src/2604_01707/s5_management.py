"""Section 5: Memory Management"""

from gaia.lang import (
    claim, setting,
    support,
)
from .s3_framework import framework_proposed

# ── Management overview ───────────────────────────────────────────────────────

setting_management_role = setting(
    "Memory management governs how an agent system maintains, refines, and evolves its memory "
    "over time. It mirrors the human memory lifecycle, encompassing five core operations: "
    "connecting, integrating, transforming, updating, and filtering.",
    title="Management component role",
)

# ── Five management operations ────────────────────────────────────────────────

mgmt_connecting = claim(
    "Connecting is a memory management operation that establishes explicit connections between "
    "memory entries sharing semantic similarity, temporal proximity, or contextual relevance. "
    "It is realized through structural edges within a graph (e.g., Zep, Mem0g) or associative "
    "links across discrete records (e.g., A-MEM, MemoryOS). This enables synchronous updates "
    "and alignment across connected memories.",
    title="Connecting operation",
    background=[setting_management_role],
)

mgmt_integrating = claim(
    "Integrating is a memory management operation that aggregates fragmented memories through "
    "abstraction or summarization, reducing redundancy and distilling essential information. "
    "For example, MemoryBank aggregates daily records into event summaries and refines a global "
    "user profile. MemoChat groups dialogues under shared topics and produces topic-level summaries. "
    "This transforms scattered memories into concise high-level representations for long-term storage.",
    title="Integrating operation",
    background=[setting_management_role],
)

mgmt_transforming = claim(
    "Transforming is a memory management operation that transfers information across memory levels "
    "(e.g., short-term to long-term). MemoryOS implements a two-stage migration: short-term memories "
    "move to mid-term via FIFO policy, then mid-term memories are promoted to long-term using a "
    "heat-based score combining access frequency and recency. Zep organizes semantically related "
    "memories into communities forming structured long-term representations.",
    title="Transforming operation",
    background=[setting_management_role],
)

mgmt_updating = claim(
    "Updating is a memory management operation that revises stored memories through three paradigms: "
    "(1) Rule-based updating — e.g., MemoryBank uses Ebbinghaus's Forgetting Curve theory to adjust "
    "memory strength over time; MemoryOS uses semantic/keyword similarity for integration. "
    "(2) LLM-based updating — e.g., MemTree uses an Aggregate Operation where LLM compresses "
    "information before writing to parent nodes; Zep uses LLM resolution tasks with semantic constraints. "
    "(3) Agent-based updating — e.g., MemGPT and MemOS grant agents access to tools for autonomous "
    "memory management (revise, merge, prune).",
    title="Updating operation",
    background=[setting_management_role],
)

mgmt_filtering = claim(
    "Filtering is a memory management operation that removes outdated or redundant information "
    "to keep memory compact and relevant. Two approaches: "
    "(1) Usage-based filtering (MemoryOS, MemoryBank) — relies on access frequency and time-based "
    "decay; rarely retrieved old memories are filtered first. "
    "(2) Content-based filtering (Mem0, Mem0g) — leverages LLMs to detect and filter duplicated "
    "or outdated knowledge, reducing noise and improving retrieval precision.",
    title="Filtering operation",
    background=[setting_management_role],
)

# ── Connection matters for multi-hop ─────────────────────────────────────────

connecting_matters_multihop = claim(
    "Effective memory organization requires mechanisms that build explicit or implicit connections "
    "among related pieces of information, which is particularly important for multi-hop reasoning tasks. "
    "Methods lacking associative operations (MemoryBank, MemGPT, MemoChat) perform poorly on "
    "Multi-Session tasks of LONGMEMEVAL and Multi-Hop tasks of LOCOMO. "
    "In contrast, Mem0 — which concurrently updates similar memories during ingestion — achieves "
    "an integration effect comparable to explicit connecting: on Multi-Session tasks of LONGMEMEVAL, "
    "Mem0 achieves 18.60% F1 and 26.19% BLEU-1 improvements over MemoryBank.",
    title="Connecting improves multi-hop reasoning",
    background=[setting_management_role],
)

strat_connecting_multihop = support(
    [mgmt_connecting, mgmt_integrating],
    connecting_matters_multihop,
    reason=(
        "Explicit connection (@mgmt_connecting) and integration (@mgmt_integrating) operations "
        "establish semantic relationships between memory entries. Without such associations, methods "
        "like MemoryBank, MemGPT, and MemoChat must rely on retrieval alone to bridge multi-hop "
        "reasoning chains, which fails when relevant evidence spans multiple disconnected entries. "
        "The 18.60% F1 improvement of Mem0 over MemoryBank on multi-session tasks provides "
        "direct experimental evidence for this mechanism."
    ),
    prior=0.88,
)
