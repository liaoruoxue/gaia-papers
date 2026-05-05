"""Section 3: The Live Research Manager -- born-agent ARA authoring.

The Live Research Manager (LRM) crystallizes the latent research
trajectory captured in researcher-AI-agent conversations into a living
ARA artifact, with **zero documentation overhead** for the researcher.
Three design principles motivate a three-stage retrospective pipeline
(Context Harvester -> Event Router -> Maturity Tracker) that runs at
session boundaries.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Design principles (§3.1)
# ---------------------------------------------------------------------------

claim_ai_native_research_paradigm = claim(
    "**AI-native research is the operational substrate.** Computer "
    "science research is increasingly *AI-native*: the researcher "
    "collaborates with a general-purpose coding agent across the full "
    "research lifecycle (brainstorming, literature survey, code, "
    "debugging, analysis, drafting). For the first time, the research "
    "process is **born digital and born textual**: every instruction, "
    "intermediate result, design choice, and abandoned direction "
    "already exists as machine-readable text in the researcher-agent "
    "session. Process knowledge is no longer a separate documentation "
    "burden -- it is the *byproduct* of the research itself "
    "[@Lu2024AIScientist; @Kusumegi2025].",
    title="AI-native research: process trace is a byproduct, not an extra deliverable",
)

claim_prior_efforts_failed = claim(
    "**Prior process-preservation efforts failed because documentation "
    "was an unrewarded burden.** Negative-result journals "
    "[@Matosin2014NegativeResults] and registered reports "
    "[@Chambers2013RegisteredReports] aimed to preserve research-process "
    "knowledge but foundered: in both, documentation remained a "
    "*separate, unrewarded* burden on the researcher. AI-native research "
    "dissolves this barrier because the trace already exists; the only "
    "missing piece is a system to crystallize it into structure.",
    title="Prior process-preservation initiatives failed because they added overhead",
)

claim_p1_silent_integration = claim(
    "**Design principle P1: silent, framework-independent integration.** "
    "The Live Research Manager is implemented as an **agent skill** "
    "[@Anthropic2025Skills]: a self-contained natural-language "
    "specification that any general-purpose coding agent (Claude Code, "
    "Cursor, Windsurf) can load. It composes tools the agent already "
    "has (file read/write/edit, shell exec) with the ARA schema, so it "
    "requires *no* custom SDKs or infrastructure changes. It runs as a "
    "background process: silent during active research, retrospective "
    "at session boundaries.",
    title="P1: Silent agent-skill integration; no custom SDK, no inline interruption",
)

claim_p2_epistemic_provenance = claim(
    "**Design principle P2: faithful epistemic provenance.** AI-native "
    "research blurs the boundary between human insight and machine "
    "execution. Every captured event is tagged with **provenance**: "
    "`user`, `ai-suggested`, `ai-executed`, or `user-revised`. An "
    "`ai-suggested` event *never auto-promotes* until the researcher "
    "explicitly confirms it, preserving epistemic integrity. Raw "
    "observations are *staged* rather than forced into categories, "
    "maturing progressively into typed events as evidence accumulates, "
    "so downstream consumers can reconstruct not just *what* was "
    "concluded but *why*.",
    title="P2: Provenance tags + staging of raw observations preserve epistemic integrity",
)

claim_p3_comprehensive_capture = claim(
    "**Design principle P3: comprehensive trajectory capture.** The full "
    "branching research process -- including dead ends and pivots -- is "
    "recorded with cross-layer bindings established *at capture time* "
    "while the conversational context is still available. Post-hoc "
    "reconstruction from archived transcripts loses these causal "
    "chains. The artifact is version-controlled, so every milestone "
    "produces a navigable snapshot, and retroactive revisions are "
    "first-class operations rather than destructive overwrites.",
    title="P3: Capture branching trajectory at session-time; version-controlled artifact",
)

# ---------------------------------------------------------------------------
# System design (§3.2)
# ---------------------------------------------------------------------------

claim_three_stage_pipeline = claim(
    "**Three-stage retrospective pipeline at each session boundary.** "
    "The manager is silent during active research, then runs three "
    "stages at session close (Figure 6): (1) **Context Harvester** "
    "scans the session record (conversation history, tool outputs, "
    "experiment results, code diffs) to extract research-significant "
    "events; (2) **Event Router** classifies each event into one of "
    "seven types and tags provenance, then writes to the appropriate "
    "ARA layer; (3) **Maturity Tracker** reviews the staging area, "
    "promoting observations with sufficient evidence into formal "
    "entries and flagging stale or conflicting items. At the next "
    "session start, the manager reads the artifact back to surface a "
    "structured briefing.",
    title="Three-stage pipeline: Context Harvester -> Event Router -> Maturity Tracker",
    metadata={"source_figure": "Fig. 6 (artifacts/2604.24658.pdf, p. 5)"},
)

claim_seven_event_types = claim(
    "**Seven research event types, each with structured payload "
    "(Table 1).** The Event Router taxonomizes captured activity into "
    "seven types:\n\n"
    "| Event type | Structured payload |\n"
    "|---|---|\n"
    "| `decision` | Choice, alternatives, evidence |\n"
    "| `experiment` | Metrics, claim linkage |\n"
    "| `dead_end` | Hypothesis, failure mode, lesson |\n"
    "| `pivot` | Trigger, rationale |\n"
    "| `claim` | Statement, falsification criteria |\n"
    "| `heuristic` | Trick, sensitivity, bounds |\n"
    "| `observation` | Raw finding, awaiting classification |\n\n"
    "Trace events (decision, experiment, dead_end, pivot) append to "
    "`/trace/`; claims and heuristics enter `/logic/`; unclassifiable "
    "events stage in `/staging/` for later promotion.",
    title="Table 1: seven event types route to /trace, /logic, or /staging",
    metadata={"source_table": "Table 1 (artifacts/2604.24658.pdf, p. 7)"},
)

claim_progressive_crystallization = claim(
    "**Progressive crystallization at two timescales.** Artifact "
    "construction proceeds at two timescales: (a) **Continuously**, at "
    "every session boundary, trace events append to the Exploration "
    "Graph. (b) **Periodically**, when a milestone is reached "
    "(hypothesis confirmed/refuted, working prototype completed, key "
    "design choice finalized), the Maturity Tracker *crystallizes* "
    "accumulated observations into the more structured layers (raw "
    "observations -> formal claims; working code -> documented Physical "
    "Layer entries). This rhythm mirrors how research understanding "
    "actually develops: insights begin as scattered observations, and "
    "forcing premature structure would distort the record.",
    title="Two-timescale rhythm: continuous trace appends + milestone crystallization",
)

claim_closure_signals = claim(
    "**Closure-signal-driven crystallization.** *Maturity* is operationally "
    "defined via **closure signals** -- externally observable patterns "
    "in the researcher-agent conversation that indicate the researcher "
    "has treated an observation as settled. The taxonomy is: (i) "
    "**topic abandonment** (researcher moved on without revisiting in "
    "k=5 turns); (ii) **verbal affirmation** (explicit endorsement: "
    "'yes, we'll go with X'); (iii) **empirical resolution** (a bound "
    "experiment produced a result the researcher commented on -- both "
    "supported and refuted outcomes are valid; refuted promotes to "
    "`dead_end`); and (iv) **artifact commitment** (downstream artifact "
    "depends on the observation: code merged, config fixed, claim used "
    "as premise). At least one signal triggers promotion. A "
    "counter-based threshold would be arbitrary; asking an LLM 'is this "
    "mature?' lacks grounding -- closure signals provide externally "
    "verifiable maturity.",
    title="Closure-signal taxonomy operationally defines 'mature enough to crystallize'",
)

claim_contradiction_handling = claim(
    "**Contradiction trigger: defer rather than overwrite.** When a new "
    "observation contradicts an already-staged or crystallized one, the "
    "Maturity Tracker does not silently overwrite. Both entries are "
    "flagged, the contradiction is appended to the Exploration Graph as "
    "a `decision` node with **unresolved status**, and resolution is "
    "deferred to the next briefing where the researcher adjudicates "
    "explicitly. This preserves the epistemic record (P2): both "
    "interpretations remain visible, and the resolution itself becomes "
    "first-class trace data.",
    title="Contradictions deferred to a researcher-adjudicated decision node",
)

claim_cross_session_continuity = claim(
    "**Cross-session continuity via reasoning log + key-context fields.** "
    "A stateless coding agent has no memory of prior conversations. "
    "Two lightweight mechanisms preserve organizational coherence "
    "across sessions: (i) a `trace/pm_reasoning_log.yaml` records the "
    "manager's own organizational decisions and their rationale at each "
    "boundary -- a few lines per session that gives the manager "
    "self-continuity; (ii) each session record includes a **key "
    "context** field with compressed summaries of the most important "
    "human-agent exchanges. Together they ensure the manager reads "
    "back not only the artifact's current state but the *reasoning "
    "chain* that produced it, maintaining coherent classification at "
    "negligible token cost.",
    title="Cross-session continuity: PM reasoning log + per-session key-context summaries",
)

# ---------------------------------------------------------------------------
# Self-evidence: the paper itself is an ARA (App. A.3)
# ---------------------------------------------------------------------------

claim_paper_is_an_ara = claim(
    "**The ARA paper is itself maintained as an ARA (App. A.3).** The "
    "paper provides its *own* artifact (`ara/`) as concrete evidence: "
    "16 falsifiable claims (`logic/claims.md`); 23 design heuristics "
    "(`logic/solution/heuristics.md`); a 114-node decision DAG "
    "(`trace/exploration_tree.yaml`) including dead-end nodes such as "
    "N50 ('Trimming src/ alone does not recover Cat C'); 38 session "
    "logs (2026-03-12 to 2026-04-26) with `pm_reasoning_log.yaml`; and "
    "94 unpromoted observations in `staging/observations.yaml`. The "
    "self-application is non-trivial evidence that the protocol is "
    "operable in practice on a paper-scale project.",
    title="Self-evidence: this paper's own ARA contains 16 claims / 23 heuristics / 114 nodes / 38 sessions",
    metadata={"source_section": "App. A.3 (artifacts/2604.24658.pdf, pp. 26-29)"},
)

__all__ = [
    "claim_ai_native_research_paradigm",
    "claim_prior_efforts_failed",
    "claim_p1_silent_integration",
    "claim_p2_epistemic_provenance",
    "claim_p3_comprehensive_capture",
    "claim_three_stage_pipeline",
    "claim_seven_event_types",
    "claim_progressive_crystallization",
    "claim_closure_signals",
    "claim_contradiction_handling",
    "claim_cross_session_continuity",
    "claim_paper_is_an_ara",
]
