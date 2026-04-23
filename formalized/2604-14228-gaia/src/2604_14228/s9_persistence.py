"""Section 9: Session Persistence and Recovery"""

from gaia.lang import claim, setting, support

from .s2_values_principles import five_values_motivate_architecture
from .s3_architecture import deny_first_safety_posture

# ── Settings ───────────────────────────────────────────────────────────────────

transcript_model_setting = setting(
    "Session transcripts are stored as mostly append-only JSONL files at a project-specific "
    "path computed by getTranscriptPath() as join(projectDir, ${getSessionId()}.jsonl). "
    "Three persistence channels operate independently: "
    "(1) Session transcripts — conversation records including user, assistant, attachment, "
    "system messages, compaction events, compaction markers, file-history snapshots, "
    "attribution snapshots, and content-replacement records; project-scoped, one file per session. "
    "(2) Global prompt history — user prompts only, stored in history.jsonl at the Claude "
    "configuration home directory (history.ts); the makeHistoryReader() generator yields entries "
    "in reverse order via readLinesReverse(), supporting Up-arrow and ctrl+r navigation. "
    "(3) Subagent sidechains — separate .jsonl + .meta.json files per subagent. "
    "Cleanup rewrites (overwriting the file) are an explicit exception to append-only semantics.",
    title="Session transcript model: three independent persistence channels",
)

session_identity_setting = setting(
    "The session identity system pairs sessionId with sessionProjectDir, set together during "
    "resume or branch (conversationRecovery.ts, commands/branch/branch.ts). The transcript "
    "path must use the same project directory active when messages were written, to avoid "
    "hooks reading the wrong directory. The compact_boundary marker records headUuid, "
    "anchorUuid, and tailUuid via annotateBoundaryWithPreservedSegment() (compact.ts), "
    "enabling the session loader to patch the message chain at read time. Preserved messages "
    "keep their original parentUuids on disk; the loader uses boundary metadata to link them "
    "correctly, making compaction never modify or delete previously written transcript lines.",
    title="Session identity and compact boundary UUIDs",
)

resume_fork_setting = setting(
    "The --resume flag rebuilds the conversation by replaying the transcript "
    "(conversationRecovery.ts). Fork creates a new session from an existing one "
    "(commands/branch/branch.ts). Both resume and fork do not restore session-scoped "
    "permissions; users must grant permissions again in the new session. "
    "File-history checkpoints for --rewind-files are stored at ~/.claude/file-history/<sessionId>/; "
    "these are file-level snapshots for reverting filesystem changes, not a generic checkpoint store. "
    "Session-scoped permissions live in memory only and are not serialized to the transcript; "
    "resume rebuilds the permission context from CLI args and disk settings, with unrecognized "
    "requests falling back to deny-first prompting.",
    title="Resume, fork, and not restoring permissions",
)

# ── Core claims about session persistence ─────────────────────────────────────

append_only_auditability = claim(
    "The append-only JSONL transcript format is a deliberate choice favoring auditability "
    "and simplicity over query power. Every event is human-readable, version-controllable, "
    "and reconstructable without specialized tooling. Database-backed alternatives would enable "
    "richer queries over session history but introduce deployment dependencies and reduce "
    "transparency. The design applies two principles: 'Conversations Outlive Context' (a "
    "session's useful life cannot be capped by the model's context window — the transcript on "
    "disk records everything, so compaction can recycle the live view without ending the "
    "conversation) and 'Conversations Outgrow a Single Path' (the append-only transcript lets "
    "users rewind, resume, or fork into a new branch without losing prior work).",
    title="Append-only JSONL: auditability over query power",
    background=[transcript_model_setting],
)

strat_append_only = support(
    [five_values_motivate_architecture],
    append_only_auditability,
    reason=(
        "The append-only durable state principle (@principle_append_only_durable_state) directly "
        "motivates JSONL append semantics: the format enables rewind, resume, and fork by "
        "preserving full history without destructive edits. The transparent file-based "
        "configuration principle (@principle_transparent_file_config) motivates human-readable "
        "JSONL over opaque databases: every event is inspectable with standard tools. "
        "The cost — no rich query capability — is accepted explicitly in the source's "
        "comparison with database-backed alternatives. Confirmed from sessionStorage.ts "
        "(Tier B evidence)."
    ),
    prior=0.9,
)

no_permission_restore_on_resume = claim(
    "Resume and fork do not restore session-scoped permissions; users must grant them again "
    "in the new session. This is a deliberate safety-conservative design choice: sessions are "
    "treated as isolated trust domains. Restoring previously granted permissions on resume "
    "would create a convenience benefit but risk carrying stale trust decisions into a changed "
    "context. The architecture opts for re-granting over implicit persistence, accepting user "
    "friction as the cost of maintaining the safety invariant that trust is always established "
    "in the current session.",
    title="Sessions as isolated trust domains: no permission restoration on resume",
    background=[resume_fork_setting, session_identity_setting],
)

strat_no_permission_restore = support(
    [deny_first_safety_posture],
    no_permission_restore_on_resume,
    reason=(
        "The deny-first safety posture (@deny_first_safety_posture) requires that permission "
        "grants not propagate implicitly across session boundaries — a permission given in a "
        "previous session may not be appropriate in a changed context. The reversibility-weighted "
        "risk principle (@principle_reversibility_weighted) favors erring toward safety: the "
        "cost of re-granting permissions (user friction) is reversible, while the cost of "
        "implicit stale trust restoration (security regression) is not. The design explicitly "
        "accepts the friction as necessary. Confirmed from conversationRecovery.ts (Tier B evidence)."
    ),
    prior=0.9,
)

compact_boundary_read_time_patching = claim(
    "The compact_boundary mechanism uses UUID-based read-time chain patching rather than "
    "destructive history rewriting. annotateBoundaryWithPreservedSegment() records headUuid, "
    "anchorUuid, and tailUuid in the boundary event; the session loader patches the message "
    "chain at read time using this metadata. Preserved messages keep their original parentUuids "
    "on disk. This means compaction never modifies or deletes previously written transcript "
    "lines — it only appends new boundary and summary events, preserving the ability to "
    "reconstruct full history if needed.",
    title="UUID-based read-time chain patching: compaction never deletes transcript lines",
    background=[session_identity_setting],
)

strat_compact_boundary = support(
    [append_only_auditability],
    compact_boundary_read_time_patching,
    reason=(
        "Append-only auditability (@append_only_auditability) requires that compaction not "
        "destroy history. The append-only durable state principle "
        "(@principle_append_only_durable_state) prohibits destructive edits. The UUID-based "
        "read-time patching mechanism satisfies both: compaction only appends boundary metadata, "
        "and the loader reconstructs the correct message chain on demand. This is confirmed "
        "in compact.ts (annotateBoundaryWithPreservedSegment) and sessionStorage.ts (Tier B evidence)."
    ),
    prior=0.88,
)
