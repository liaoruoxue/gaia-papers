"""Section III.A: Six Desiderata for Production Agentic Memory.

Section III.A of [@Abtahi2026Memanto] articulates the six design principles
(D1-D6) that guided Memanto's architecture, derived from systematic
analysis of agent operational requirements, structured feedback from
production AI agent deployments, and a structured dialogue with Claude
[@ClaudeCard] about the limitations of its own memory architecture.

Each desideratum is paired with a coverage claim against competing systems
(Memanto, Mem0, Zep, Letta) reproduced from Table I.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Provenance: how the desiderata were derived
# ---------------------------------------------------------------------------

claim_desiderata_provenance = claim(
    "**Desiderata D1-D6 derived from production deployments + LLM "
    "self-diagnosis.** The six design principles emerged from systematic "
    "analysis of agent operational requirements, structured feedback from "
    "production AI agent deployments, and failure modes documented in the "
    "benchmark literature. A contributing source was a structured "
    "dialogue with Claude [@ClaudeCard] in which the model was asked to "
    "articulate the limitations of its own memory architecture. Claude "
    "identified passive context injection as the root failure mode and "
    "independently surfaced seven specific gaps -- inability to query by "
    "relevance, absence of temporal decay signals, lack of confidence "
    "and provenance tagging, flattening of episodic / semantic / "
    "procedural memory into a single store, absence of contradiction "
    "handling and versioning, lack of scope and permissioning, and "
    "absence of human-readable audit logs -- which map directly onto "
    "D1-D6 [@Abtahi2026Memanto, Sec. III].",
    title="Provenance: D1-D6 derived from production feedback + Claude self-diagnosis (7 gaps -> 6 desiderata)",
)

# ---------------------------------------------------------------------------
# D1-D6 (each as a claim, since each is a normative architectural assertion
# that can be questioned, not a definitional setting)
# ---------------------------------------------------------------------------

claim_d1_queryable_not_injectable = claim(
    "**D1. Queryable, not injectable.** Agents must be able to query "
    "memory based on relevance to the current task, rather than receiving "
    "a static blob of context injected at conversation start. The "
    "distinction is between providing a pre-assembled dossier and "
    "providing a librarian the agent can consult on demand. Static "
    "injection fails when the injected context exceeds the context window, "
    "contains irrelevant content, or misses recently stored facts not yet "
    "in the injected snapshot [@Abtahi2026Memanto, Sec. III.A].",
    title="D1: memory must be queryable on demand, not statically injected",
)

claim_d2_temporal_with_decay = claim(
    "**D2. Temporally aware with decay.** Memory entries should have "
    "temporal weighting and support versioning and decay signals. A "
    "deadline mentioned yesterday carries different urgency from a "
    "preference stated six months ago. This requirement maps directly to "
    "the Knowledge Update and Temporal Reasoning categories of "
    "LongMemEval [@LongMemEval], where systems without temporal "
    "awareness perform significantly below average "
    "[@Abtahi2026Memanto, Sec. III.A].",
    title="D2: memory must support temporal queries, versioning, and decay signals",
)

claim_d3_confidence_provenance = claim(
    "**D3. Confidence and provenance tracking.** A production memory "
    "system must distinguish explicitly stated facts from inferred "
    "patterns and from potentially outdated information. Memory entries "
    "should carry provenance metadata that agents use to calibrate their "
    "confidence in retrieved context and avoid overconfident assertions "
    "on stale data [@Abtahi2026Memanto, Sec. III.A].",
    title="D3: memory entries must carry provenance metadata for confidence calibration",
)

claim_d4_typed_hierarchical = claim(
    "**D4. Typed and hierarchical.** Episodic memory (e.g. *in our "
    "November conversation the user discussed X*), semantic memory (e.g. "
    "*the user is building a vector-database startup*), and procedural "
    "memory (e.g. *when asked for reports the user prefers this format*) "
    "serve fundamentally different retrieval purposes [@Tulving1972] and "
    "should be stored and queried with appropriate type semantics "
    "[@Abtahi2026Memanto, Sec. III.A].",
    title="D4: memory must be typed (episodic / semantic / procedural) with type-appropriate retrieval",
)

claim_d5_contradiction_aware = claim(
    "**D5. Contradiction aware.** When new information contradicts "
    "existing memory, the system must flag the conflict rather than "
    "silently overwrite or create inconsistency. For long-running "
    "agents, unresolved contradictions accumulate into *constraint "
    "drift*, a gradual erosion of the coherence of the agent's world "
    "model. MemoryAgentBench [@MemoryAgentBench] confirms that conflict "
    "resolution remains one of the most significant unsolved challenges, "
    "with all evaluated methods failing on multi-hop conflict scenarios "
    "[@Abtahi2026Memanto, Sec. III.A].",
    title="D5: memory must detect contradictions and flag them for explicit resolution",
)

claim_d6_zero_overhead_ingest = claim(
    "**D6. Zero overhead ingestion.** Every millisecond of ingestion "
    "latency is a millisecond where the agent cannot access its own "
    "recent experience. For real-time agentic workflows, memory must be "
    "available for retrieval at write time, with no indexing delay, no "
    "mandatory LLM extraction step, and no graph-construction bottleneck "
    "[@Abtahi2026Memanto, Sec. III.A].",
    title="D6: memory must be available for retrieval at write time (no indexing / LLM / graph bottleneck)",
)

# ---------------------------------------------------------------------------
# Coverage claim across systems (Table I)
# ---------------------------------------------------------------------------

claim_table1_desiderata_coverage = claim(
    "**Desiderata coverage across systems (Table I).** Memanto is the "
    "only evaluated system that fully supports all six desiderata; "
    "competing systems each fail at least two:\n\n"
    "| System    | D1 | D2 | D3 | D4 | D5 | D6 |\n"
    "|-----------|----|----|----|----|----|----|\n"
    "| Memanto   | yes | yes | yes | yes | yes | yes |\n"
    "| Mem0 [@Mem0]   | yes | yes | partial | partial | no | no |\n"
    "| Zep [@Zep]    | yes | yes | partial | partial | no | no |\n"
    "| Letta [@MemGPT]  | yes | no  | no  | no  | no | partial |\n\n"
    "Key gaps highlighted in Fig. 2: Mem0 and Zep lack conflict "
    "detection (D5) and incur high ingestion cost (D6); Letta is weak "
    "across D2-D5; ENGRAM [@ENGRAM] lacks D3, D5, and D6; A-MEM "
    "[@AMEM] lacks D5-D6 with only partial D2-D4 "
    "[@Abtahi2026Memanto, Table I; Fig. 2].",
    title="Table I: only Memanto fully covers D1-D6; all competitors miss D5 and/or D6",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table I and Fig. 2",
        "caption": "Desiderata coverage across agentic memory systems; radar visualisation in Fig. 2.",
    },
)

# ---------------------------------------------------------------------------
# System overview (III.B): three endpoints
# ---------------------------------------------------------------------------

setup_three_endpoints = setting(
    "**System overview: three endpoints.** Memanto operates as a "
    "persistent FastAPI service exposing three primary endpoints: "
    "(i) `/remember` -- commits items to memory with automatic typing, "
    "tagging, timestamping, conflict detection, and optional namespace "
    "scoping; (ii) `/recall` -- retrieves items via Moorcheh's "
    "ITS-powered semantic search with configurable similarity thresholds "
    "and retrieval limits; (iii) `/answer` -- performs full RAG with "
    "LLM intelligence applied on top of retrieved memory context "
    "[@Abtahi2026Memanto, Sec. III.B].",
    title="Setup: Memanto exposes /remember, /recall, /answer endpoints",
)

setup_two_layer_architecture = setting(
    "**Two-layer frontend + backend architecture.** Memanto's frontend "
    "(Fig. 3) comprises (1) Agent Ecosystem (IDE integrations, agent "
    "CLIs, custom Python/JS/LangChain agents, local web dashboard) and "
    "(2) Memanto Gateway (Memanto CLI Engine + FastAPI Server). The "
    "backend (Fig. 4) comprises (1) Shared Services (nine internal "
    "services: Daily Summary, Conflict Resolution, Answer, Recall, "
    "Remember, Agent Manager, Session/Auth Manager, Memory Sync via "
    "MEMORY.md injection, Tool Connect) and (2) Moorcheh.ai Cloud Layer "
    "(zero-indexing semantic database, agent-optimised RAG pipeline, "
    "native LLM access) [@Abtahi2026Memanto, Sec. III.B; Figs. 3-4].",
    title="Setup: frontend (gateway + agent ecosystem) + backend (services + Moorcheh cloud)",
)

__all__ = [
    "claim_desiderata_provenance",
    "claim_d1_queryable_not_injectable",
    "claim_d2_temporal_with_decay",
    "claim_d3_confidence_provenance",
    "claim_d4_typed_hierarchical",
    "claim_d5_contradiction_aware",
    "claim_d6_zero_overhead_ingest",
    "claim_table1_desiderata_coverage",
    "setup_three_endpoints",
    "setup_two_layer_architecture",
]
