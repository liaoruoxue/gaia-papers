"""Multi-agent workflow use cases distilled from Sections 4.3, 5.2, 11.4, 14
of [@Park2026Kumiho]. These illustrate how the structural primitives operate
in concrete agent-pipeline scenarios.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Multi-agent creative pipeline (the canonical example from Sec. 4.3)
# ---------------------------------------------------------------------------

claim_multi_agent_creative_pipeline = claim(
    "**Multi-agent creative pipeline scenario.** Image-generation agent "
    "produces a concept-art revision; video-compositing agent locates "
    "that revision via its `kref://` URI, checks the `approved` tag, and "
    "creates its own output with a `Derived_From` edge linking back to "
    "the input; audio agent does the same for the soundtrack; editing "
    "agent assembles the final deliverable with typed edges to every "
    "upstream component. **Each agent uses the graph for both "
    "remembering** (client preferences, past iterations, feedback "
    "history) **and operating** (find the right input version, register "
    "its output, declare dependencies). This unification enables fully "
    "autonomous multi-agent pipelines without separate asset-tracking "
    "systems [@Park2026Kumiho, Sec. 4.3].",
    title="Use case: multi-agent creative pipeline (image -> compositing -> audio -> editing via shared graph)",
)

# ---------------------------------------------------------------------------
# Coding agent / VFX use case (origin of the architectural insight)
# ---------------------------------------------------------------------------

claim_vfx_pipeline_origin = claim(
    "**The architectural correspondence was first recognized in production "
    "VFX pipelines.** Asset-management systems in visual effects and game "
    "development have implemented these exact primitives -- immutable "
    "versioned snapshots, typed dependency edges, mutable status "
    "pointers, URI-based addressing, content-reference separation -- for "
    "decades. The architectural direction is **memory-first**: the "
    "graph-native primitives required for cognitive memory inherently "
    "provide auditable asset management as an emergent capability. "
    "Practical examples: a video compositing agent locating the approved "
    "texture revision produced by an upstream generation agent; an "
    "editing agent tracing which audio mix corresponds to which scene cut "
    "[@Park2026Kumiho, Sec. 4.2 footnote; Principle 1].",
    title="Use case origin: VFX/game-dev asset management pioneered the same primitives decades ago",
)

# ---------------------------------------------------------------------------
# Decision auditability (governance use case)
# ---------------------------------------------------------------------------

claim_decision_auditability_use_case = claim(
    "**Decision auditability use case.** An agent that approved a "
    "deployment, recommended a treatment plan, or signed off on a "
    "financial model must explain *why* -- not by regenerating a "
    "plausible explanation but by **pointing to the actual evidence, the "
    "actual reasoning chain, and the actual prior beliefs that informed "
    "the decision**. This is the same accountability standard applied to "
    "human workers. The memory graph provides this: every belief has a "
    "URI, a revision history, provenance edges to source evidence, and "
    "an immutable audit trail. An operator reviewing an agent's decision "
    "can traverse from the decision memory to its `Derived_From` "
    "sources, check what the agent believed at the time via "
    "time-indexed tag resolution ($\\tau_T$), and inspect the Dream "
    "State consolidation reports [@Park2026Kumiho, Sec. 5.2].",
    title="Use case: decision auditability via Derived_From traversal + tau_T historical tag resolution",
)

# ---------------------------------------------------------------------------
# Coding-agent / multi-channel agent (Sec. 1, Sec. 10.3)
# ---------------------------------------------------------------------------

claim_coding_agent_use_case = claim(
    "**Coding-agent use case.** A coding agent writes and commits code; a "
    "design agent generates and iterates on visual assets; a research "
    "agent gathers, synthesizes, and reports findings; a production "
    "agent coordinates tasks across departments and tracks deliverables. "
    "Each accumulates substantial outputs (code, designs, documents, "
    "intermediate results) that without the unified graph would lack "
    "systematic versioning, provenance tracking, or linkage to the "
    "decisions that created them [@Park2026Kumiho, Sec. 1].",
    title="Use case: coding/design/research/production agents -- each produces auditable accumulating output",
)

claim_multi_channel_session_identity = claim(
    "**Multi-channel session identity use case.** For agents operating "
    "across multiple platforms (messaging services, web interfaces, "
    "desktop applications), session identity is **user-centric, not "
    "channel-centric**. The session ID format encodes context (e.g., "
    "`personal`, `work`), user identity hash, date, and sequence number, "
    "enabling cross-channel memory retrieval unified under one identity. "
    "An agent that forgets a conversation because the user switched from "
    "mobile to desktop has failed at its core purpose: session "
    "continuity follows the user, not the platform "
    "[@Park2026Kumiho, Sec. 10.3].",
    title="Use case: multi-channel session identity follows the user, not the platform",
)

# ---------------------------------------------------------------------------
# Concrete Letta-comparison example (Sec. 2.1)
# ---------------------------------------------------------------------------

claim_letta_concrete_example = claim(
    "**Concrete comparison example: warm-tones / cool-tones conflict.** "
    "If an agent's memory contains 'client prefers warm tones' and a "
    "concurrent write produces 'client now prefers cool tones,' Letta's "
    "Git-backed system generates a text-level merge conflict requiring "
    "human or LLM intervention on the text diff. Kumiho creates a new "
    "revision with a `Supersedes` edge, moves the tag pointer, and makes "
    "the stale belief retrievable only via explicit opt-in -- with "
    "`AnalyzeImpact` propagating the change to downstream decisions "
    "automatically. This concrete example illustrates the three "
    "structural advantages over Git-backed text versioning: typed edges, "
    "AGM-compliant supersession, and automatic downstream propagation "
    "[@Park2026Kumiho, Sec. 2.1].",
    title="Use case: warm/cool tones conflict (Letta = text merge; Kumiho = AGM Supersedes + AnalyzeImpact)",
)

__all__ = [
    "claim_multi_agent_creative_pipeline",
    "claim_vfx_pipeline_origin",
    "claim_decision_auditability_use_case",
    "claim_coding_agent_use_case",
    "claim_multi_channel_session_identity",
    "claim_letta_concrete_example",
]
