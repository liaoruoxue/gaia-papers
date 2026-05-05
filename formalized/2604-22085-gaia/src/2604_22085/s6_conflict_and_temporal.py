"""Sections III.E-III.H: Conflict resolution, temporal versioning,
session/namespace management, and daily intelligence.

These sections of [@Abtahi2026Memanto] cover the remaining architectural
components above the ITS retrieval substrate and the typed schema:

* III.E: built-in semantic conflict detection and three-option resolution
  (supersede / retain / annotate). Addresses *constraint drift*, the
  failure mode in long-running agents.
* III.F: temporal versioning with three query modalities (as-of /
  changed-since / current-only). Non-destructive supersession.
* III.G: namespace + time-bounded session architecture.
* III.H: daily-intelligence artefacts (Markdown audit trail).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# III.E Conflict resolution
# ---------------------------------------------------------------------------

setup_conflict_mechanism = setting(
    "**Conflict-detection mechanism.** When a new memory is committed, "
    "Memanto computes semantic similarity against existing memories of "
    "the same type within the agent's namespace, using a configurable "
    "*contradiction threshold*. If the threshold is exceeded the system "
    "treats the pair as a candidate conflict, flags it, and presents the "
    "agent with three resolution options: (i) *supersede* (replace the "
    "old memory), (ii) *retain* (keep the old memory), or (iii) "
    "*annotate* (preserve both with a conflict flag for human review) "
    "[@Abtahi2026Memanto, Sec. III.E].",
    title="Setup: conflict detection = same-type same-namespace semantic similarity over configurable threshold",
)

claim_conflict_addresses_constraint_drift = claim(
    "**Conflict detection addresses *constraint drift* in long-running "
    "agents.** Without explicit conflict detection, agents gradually "
    "accumulate contradictory memories that erode the coherence of their "
    "reasoning -- a failure mode the paper terms *constraint drift*. The "
    "example is concrete: *Project deadline is April 15* followed by "
    "*Project deadline is May 1* without explicit reconciliation leaves "
    "the agent's world model internally inconsistent. MemoryAgentBench "
    "[@MemoryAgentBench] confirms that conflict resolution remains one "
    "of the most significant unsolved challenges, with all evaluated "
    "methods failing on multi-hop conflict scenarios "
    "[@Abtahi2026Memanto, Sec. III.E; Sec. V.C].",
    title="Conflict detection addresses constraint drift; MemoryAgentBench confirms all current systems fail at it",
)

claim_conflict_satisfies_d5 = claim(
    "**Conflict-resolution mechanism architecturally satisfies D5 "
    "(contradiction aware).** Memanto's same-type semantic-similarity "
    "matching plus three-option resolution (supersede / retain / "
    "annotate) is the architectural mechanism by which D5 is satisfied. "
    "Per Table I, Memanto is the only evaluated system fully covering "
    "D5; Mem0, Zep, and Letta all fail this desideratum entirely "
    "[@Abtahi2026Memanto, Sec. III.A; Sec. III.E; Table I].",
    title="Conflict mechanism architecturally satisfies D5 (no other evaluated system does)",
)

claim_conflict_production_necessity = claim(
    "**Conflict resolution is a production necessity, not just a "
    "benchmark feature.** Neither LongMemEval nor LoCoMo systematically "
    "tests contradictory memories, but in long-running production "
    "deployments contradictions accumulate via user corrections, updated "
    "preferences, and evolving project contexts. Without explicit "
    "conflict detection these produce *memory poisoning*, leading to "
    "increasingly incoherent agent behaviour over time. Memanto's "
    "proactive conflict detection provides a guardrail absent from all "
    "evaluated competing systems [@Abtahi2026Memanto, Sec. V.C].",
    title="Conflict resolution is a production necessity; absent from all evaluated competitors",
)

# ---------------------------------------------------------------------------
# III.F Temporal versioning
# ---------------------------------------------------------------------------

setup_temporal_modalities = setting(
    "**Three temporal query modalities.** Memanto supports three "
    "temporal query types: (i) **As-of queries** -- retrieve the memory "
    "state as it existed at a specific historical timestamp (audit-"
    "trail reconstruction); (ii) **Changed-since queries** -- retrieve "
    "all memories created or modified within a time range (incremental "
    "context updates); (iii) **Current-only queries** -- retrieve only "
    "non-superseded memories (ground-truth state without historical "
    "noise) [@Abtahi2026Memanto, Sec. III.F].",
    title="Setup: temporal query modalities = as-of, changed-since, current-only",
)

claim_non_destructive_supersession = claim(
    "**Memory supersession is non-destructive.** Superseded entries are "
    "marked accordingly but retained in the store, enabling full "
    "temporal reconstruction. This design is critical for compliance-"
    "sensitive deployments in regulated industries and directly "
    "addresses the Knowledge Update evaluation category in LongMemEval "
    "[@LongMemEval; @Abtahi2026Memanto, Sec. III.F].",
    title="Memanto supersession is non-destructive; old entries retained for audit",
)

claim_temporal_satisfies_d2 = claim(
    "**Temporal versioning architecturally satisfies D2 (temporally "
    "aware with decay).** The combination of three temporal query "
    "modalities + non-destructive supersession + per-type decay signals "
    "(Sec. III.D priority column) provides the temporal awareness "
    "demanded by D2 [@Abtahi2026Memanto, Sec. III.A; Sec. III.F; "
    "Table I].",
    title="Temporal versioning architecturally satisfies D2",
)

# ---------------------------------------------------------------------------
# III.G Session and namespace management
# ---------------------------------------------------------------------------

setup_namespace_architecture = setting(
    "**Namespace + session architecture.** Each agent maintains an "
    "independent memory namespace. Sessions are time-bounded windows "
    "with a default duration of six hours that provide temporal "
    "grouping without restricting cross-session retrieval -- all "
    "memories within a namespace remain accessible regardless of "
    "session boundaries, enabling persistent cross-session context "
    "[@Abtahi2026Memanto, Sec. III.G].",
    title="Setup: namespace per agent + 6-hour default sessions; cross-session retrieval unrestricted",
)

# ---------------------------------------------------------------------------
# III.H Daily intelligence
# ---------------------------------------------------------------------------

claim_daily_intelligence = claim(
    "**Daily intelligence: automated session summaries, contradiction "
    "reports, and conflict-resolution prompts persisted as Markdown.** "
    "Memanto generates automated daily intelligence artefacts including "
    "session summaries, contradiction-detection reports, and "
    "interactive conflict-resolution prompts. These artefacts are "
    "persisted as local Markdown files and optionally synced to "
    "Moorcheh's cloud store, providing both human-readable audit trails "
    "and machine-queryable context for agents operating on daily "
    "planning cycles. This satisfies the human-readable audit-log gap "
    "Claude [@ClaudeCard] surfaced during requirements elicitation "
    "[@Abtahi2026Memanto, Sec. III.H].",
    title="Daily intelligence = automated Markdown session summaries + conflict reports + audit logs",
)

__all__ = [
    "setup_conflict_mechanism",
    "claim_conflict_addresses_constraint_drift",
    "claim_conflict_satisfies_d5",
    "claim_conflict_production_necessity",
    "setup_temporal_modalities",
    "claim_non_destructive_supersession",
    "claim_temporal_satisfies_d2",
    "setup_namespace_architecture",
    "claim_daily_intelligence",
]
