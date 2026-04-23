"""Section 12: Future Directions"""

from gaia.lang import claim, setting, support, question

from .s2_values_principles import long_term_capability_preservation_lens
from .s3_architecture import context_window_as_binding_constraint
from .s6_extensibility import four_mechanisms_justified
from .s7_context_memory import file_based_memory_vs_alternatives
from .s9_persistence import no_permission_restore_on_resume, append_only_auditability
from .s11_discussion import (
    bounded_context_code_quality_prediction,
    long_term_sustainability_gap,
    infrastructure_over_decision_scaffolding,
)

# ── Questions (open research directions) ──────────────────────────────────────

q_silent_failure = question(
    "Whether the observability-evaluation adoption gap (89% observability adoption vs. 52.4% "
    "offline evaluation, per LangChain 2026) reflects a missing tooling layer, a missing "
    "evaluation interface inside the harness, or a model-capability ceiling — and whether "
    "generator-evaluator separation scaffolding (sprint contracts, post-hoc checks) belongs "
    "inside the harness as additional hook events or outside it as a separate evaluation layer.",
    title="Q: Observability-evaluation gap: where does the scaffolding belong?",
)

q_cross_session_persistence = question(
    "Whether agent state and the human-agent working relationship should persist across sessions, "
    "and in what form, for durable state that is neither a static instruction (CLAUDE.md) nor a "
    "single session's transcript — and whether a single substrate can carry both a user's "
    "personal instruction hierarchy and a shared organizational context while preserving "
    "file-based transparency, without reintroducing the resume-restoration concern that "
    "Section 9 closes as a deliberate safety choice.",
    title="Q: Cross-session persistence without stale trust restoration",
)

q_harness_boundary = question(
    "Whether the harness boundary evolution will be most pronounced in where the harness runs, "
    "when it acts (proactivity), what it acts on (physical actions via VLA models), or with "
    "whom it coordinates (role-differentiated multi-agent systems) — and whether a single "
    "harness architecture can span all four extensions or will fragment into specialized stacks.",
    title="Q: Harness boundary: where, when, what, with whom?",
)

q_horizon_scaling = question(
    "Whether the context-management pipeline (Section 7), last-assistant-text return policy "
    "(Section 8), and append-only persistence (Section 9) remain sufficient when sessions "
    "compose into multi-session programs extending over weeks — and whether the harness layer "
    "alone closes the gap, or whether a cross-session memory substrate or coordination "
    "primitives beyond session, sub-agent, and memory are required.",
    title="Q: Horizon scaling from session to scientific program",
)

q_governance = question(
    "Which logging, transparency, and human-oversight affordances coding-agent architectures "
    "should expose under emerging regulatory constraints (EU AI Act fully applicable August 2026, "
    "GPAI Code of Practice) — specifically whether the deny-first evaluation documented in "
    "Section 5 is externally auditable in the forms that emerging frameworks contemplate, "
    "and whether the values-over-rules principle admits the kind of explicit rule articulation "
    "that compliance review may call for.",
    title="Q: Governance and oversight affordances under EU AI Act",
)

q_long_term_capability = question(
    "Whether the empirical claims motivating the long-term capability preservation lens are "
    "measurable at session granularity, and whether architecture can respond to such measurements "
    "once they exist — through comprehension-preserving surfaces, generator-evaluator separation "
    "applied to the human loop, or mechanisms not yet named — and whether the harness is even "
    "the right locus for such action versus the IDE, the organization, or the human development loop.",
    title="Q: Long-term human capability: measurement gap and design gap",
)

# ── Settings ───────────────────────────────────────────────────────────────────

managed_agents_setting = setting(
    "Anthropic's Managed Agents work (Martin et al., 2026) describes virtualizing the components "
    "of an agent (session, harness, sandbox) so that 'each became an interface that made few "
    "assumptions about the others, and each could fail or be replaced independently', drawing "
    "an explicit analogy to how operating systems virtualized hardware into processes and files. "
    "The Harness Design essay (Rajasekaran, 2026) observes that 'the space of interesting "
    "harness combinations doesn't shrink as models improve; it moves.'",
    title="Managed Agents: virtualizing session, harness, sandbox",
)

memory_research_setting = setting(
    "The memory survey of Hu et al. (2025) argues that agent memory is becoming a distinct "
    "cognitive substrate rather than a side effect of context window management, and identifies "
    "automated memory management, RL-driven memory, and trustworthy memory (privacy, "
    "explainability, and hallucination robustness) as open frontiers. Claude Code today exposes "
    "the factual tier (CLAUDE.md, auto memory) and the working tier (the conversation window); "
    "the experiential tier (accumulated, automatically curated playbooks of strategies learned "
    "from past sessions) is the natural next step.",
    title="Memory tiers: factual, working, experiential",
)

# ── Core claims about future directions ───────────────────────────────────────

architecture_as_snapshot = claim(
    "The architecture documented in this paper should be read as a snapshot of a co-evolving "
    "system rather than a fixed optimum. Anthropic's Managed Agents work (Martin et al., 2026) "
    "and the Harness Design essay (Rajasekaran, 2026) both point toward architectural decoupling "
    "where the tightly coupled local architecture analyzed here is one point on a spectrum. "
    "The harness boundary evolution question (where, when, what, with whom) is not resolved "
    "by the source-level analysis in Sections 3 to 9.",
    title="Architecture as snapshot of a co-evolving system, not a fixed optimum",
    background=[managed_agents_setting],
)

strat_snapshot = support(
    [infrastructure_over_decision_scaffolding, context_window_as_binding_constraint],
    architecture_as_snapshot,
    reason=(
        "The infrastructure-over-scaffolding philosophy (@infrastructure_over_decision_scaffolding) "
        "is designed for current model capabilities. As capabilities improve, the harness "
        "combinations that add value will shift, as Rajasekaran (2026) documents. Context "
        "window expansion (@context_window_as_binding_constraint — longer windows reduce "
        "compaction pressure) would simplify the graduated pipeline, demonstrating that "
        "current architectural choices are contingent on current technical constraints. "
        "Confirmed from Section 11.6 architectural decoupling discussion (Tier A evidence)."
    ),
    prior=0.85,
)

memory_experiential_tier_gap = claim(
    "Claude Code currently exposes the factual memory tier (CLAUDE.md, auto memory) and the "
    "working memory tier (the conversation window), but lacks the experiential tier: accumulated, "
    "automatically curated playbooks of strategies learned from past sessions. The context-"
    "engineering literature (Zhang et al., 2025a) has started to provide mechanisms for that "
    "accumulation, and the memory survey of Hu et al. (2025) identifies it as an open frontier "
    "alongside automated memory management, RL-driven memory, and trustworthy memory (privacy, "
    "explainability, and hallucination robustness).",
    title="Missing experiential memory tier: from CLAUDE.md to accumulated playbooks",
    background=[memory_research_setting],
)

strat_memory_gap = support(
    [file_based_memory_vs_alternatives, append_only_auditability],
    memory_experiential_tier_gap,
    reason=(
        "The file-based memory architecture (@file_based_memory_vs_alternatives) provides "
        "auditability and transparency but is static — users edit CLAUDE.md manually. The "
        "append-only session design (@append_only_auditability) preserves full history for "
        "debugging but does not automatically curate strategy playbooks from it. The gap "
        "between what the architecture provides (factual + working tiers) and what Hu et al. "
        "(2025) identifies as the next frontier (experiential tier) is an architectural gap "
        "confirmed by comparing the implemented design with the memory research literature "
        "(Tier C evidence from Hu et al. 2025, Zhang et al. 2025a)."
    ),
    prior=0.82,
)

sustainability_as_first_class_design = claim(
    "Future systems could treat the long-term human capability sustainability gap as a "
    "first-class design problem, not a downstream evaluation metric. The harness documented "
    "in this paper provides limited mechanisms that explicitly preserve long-term human "
    "understanding, codebase coherence, or the developer pipeline. Whether architecture can "
    "respond to session-granularity measurements of comprehension or convention drift — through "
    "comprehension-preserving surfaces, generator-evaluator separation applied to the human "
    "loop, or mechanisms not yet named — is an open design question the paper does not adjudicate.",
    title="Sustainability gap as first-class design problem",
    background=[],
)

strat_sustainability_design = support(
    [long_term_sustainability_gap, bounded_context_code_quality_prediction,
     long_term_capability_preservation_lens],
    sustainability_as_first_class_design,
    reason=(
        "The long-term sustainability evidence (@long_term_sustainability_gap — 19% slower, "
        "neural connectivity loss, hiring decline) combined with the bounded context code quality "
        "predictions (@bounded_context_code_quality_prediction — complexity accrual, technical "
        "debt persistence) motivate treating sustainability as a design input. The evaluative "
        "lens (@long_term_capability_preservation_lens) frames this as an analytical dimension "
        "today; the conclusion of Section 14 proposes elevating it to a first-class design "
        "value. No mechanism class is specified — the paper leaves this as an open design "
        "question (Tier A evidence from Section 14)."
    ),
    prior=0.78,
)

governance_external_constraint = claim(
    "Emerging AI regulation adds an external constraint on agent architectures. The EU AI Act "
    "(fully applicable August 2026), the GPAI Code of Practice, and the MIT AI Agent Index "
    "(finding only 13.3% of indexed agentic systems publish agent-specific safety cards) "
    "create compliance requirements. The deny-first evaluation documented in Section 5 is "
    "internally auditable through session transcripts but not yet externally auditable in the "
    "forms that emerging frameworks contemplate. Whether the values-over-rules principle "
    "admits the kind of explicit rule articulation that compliance review calls for is an "
    "open question lying within the harness rather than the model.",
    title="Governance constraint: internal auditability vs. external compliance requirements",
)

strat_governance = support(
    [append_only_auditability, no_permission_restore_on_resume],
    governance_external_constraint,
    reason=(
        "The append-only JSONL transcript design (@append_only_auditability) provides internal "
        "auditability: every event is human-readable and reconstructable. However, "
        "no_permission_restore_on_resume (@no_permission_restore_on_resume) demonstrates that "
        "the architecture already makes safety-conservative choices at the cost of user friction "
        "— the same design space where external compliance requirements will impose constraints. "
        "The gap between internal auditability and the external reporting forms contemplated "
        "by GPAI Code of Practice is an architectural gap. Confirmed from Sections 12.5 "
        "and 5 (Tier A analysis + Tier C regulatory sources)."
    ),
    prior=0.8,
)
