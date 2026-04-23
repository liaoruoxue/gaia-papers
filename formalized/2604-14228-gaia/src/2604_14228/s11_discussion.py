"""Section 11: Discussion — Value Tensions, Trade-offs, and Empirical Predictions"""

from gaia.lang import claim, setting, support, deduction

from .s2_values_principles import (
    five_values_motivate_architecture,
    long_term_capability_preservation_lens,
)
from .s3_architecture import (
    reasoning_separation_claim,
    context_window_as_binding_constraint,
    seven_independent_safety_layers,
)
from .s4_query_loop import graduated_compaction_claim
from .s5_permissions import (
    approval_fatigue_observation,
    deny_first_motivated_by_approval_fatigue,
    defense_in_depth_shared_failure_modes,
    graduated_trust_spectrum_claim,
)
from .s6_extensibility import four_mechanisms_justified
from .s7_context_memory import claudemd_probabilistic_compliance
from .s8_subagents import isolated_context_boundaries

# ── Settings ───────────────────────────────────────────────────────────────────

value_tensions_table_setting = setting(
    "Tensions between values, with supporting evidence (Table 4). "
    "| Value Pair | Tension | Evidence | "
    "| Authority × Safety | Approval fatigue vs. protection | 93% approval rate undermines human vigilance (Hughes, 2026); safety must compensate via classifier and sandboxing | "
    "| Safety × Capability | Performance vs. defense depth | >50-subcommand fallback skips per-subcommand deny checks due to parsing overhead (Adversa.ai, 2026); safety layers share performance constraints | "
    "| Adaptability × Safety | Extensibility vs. attack surface | Multiple CVEs exploit pre-trust initialization of hooks and MCP servers (Donenfeld and Vanunu, 2026) | "
    "| Capability × Adaptability | Proactivity vs. disruption | 12 to 18% more tasks but preference drops at high frequencies (Chen et al., 2025) | "
    "| Capability × Reliability | Velocity vs. coherence | Bounded context prevents full codebase awareness (Section 7); subagent isolation limits cross-agent consistency (Section 8); complexity increases observed in adjacent tools (He et al., 2025) |",
    title="Value tensions table with empirical evidence",
)

kairos_setting = setting(
    "The feature-gated KAIROS system implements a persistent background agent with tick-based "
    "heartbeats: when no user messages are pending, the system injects periodic <tick> prompts, "
    "and the model decides whether to act or sleep. It addresses the documented tension that "
    "proactive AI assistants increase task completion by 12 to 18% but reduce user preference "
    "at high frequencies (Chen et al., 2025). KAIROS resolves this through terminal focus "
    "awareness (maximizing autonomous action when the user is away, increasing collaboration "
    "when present) and economic throttling via SleepTool (each wake-up costs an API call; "
    "the prompt cache expires after five minutes of inactivity, making sleep/wake an explicit "
    "cost optimization). KAIROS cannot be confirmed as active in production builds.",
    title="KAIROS: feature-gated proactive background agent",
)

recurring_design_commitments_setting = setting(
    "Three cross-cutting design commitments recur across the six subsystem analyses (Section 11.7): "
    "(1) Graduated layering over monolithic mechanisms — safety, context management, and extensibility "
    "all use graduated stacks of independent mechanisms rather than single integrated solutions; "
    "(2) Append-only designs that favor auditability over query power — session transcripts are "
    "append-only JSONL files; permissions are not restored across session boundaries; compaction "
    "applies read-time projections rather than destructive edits; "
    "(3) Model judgment within a deterministic harness — the architecture trusts the model's "
    "judgment within a rich deterministic harness; the estimated 1.6% decision-logic ratio "
    "captures this quantitatively.",
    title="Three recurring design commitments across subsystems",
)

empirical_predictions_setting = setting(
    "Architectural properties generate testable predictions about code quality outcomes: "
    "(1) Bounded context (Section 7) predicts higher rates of pattern duplication and convention "
    "violation in agent-generated code than code produced with full codebase visibility; "
    "(2) Subagent isolation (Section 8) compounds the effect: parallel agents can independently "
    "re-implement solutions that already exist elsewhere. "
    "Adjacent empirical evidence: causal analysis of Cursor adoption across 807 repositories "
    "(He et al., 2025) found code complexity +40.7% (p < 0.001), velocity spike +281% in "
    "month one then baseline by month three. Large-scale audit of 304,000 AI-authored commits "
    "across 6,275 repositories (Liu et al., 2026) found ~25% of AI-introduced issues persisting "
    "to latest revision; security-related issues persisting at substantially higher rate.",
    title="Architectural predictions about code quality outcomes",
)

# ── Core claims about the discussion ──────────────────────────────────────────

infrastructure_over_decision_scaffolding = claim(
    "The architecture documented in Sections 3 to 9 is overwhelmingly deterministic infrastructure "
    "(permission gates, tool routing, context management, recovery logic), with the LLM invoked "
    "as a stateless completion endpoint. An estimated 1.6% of the codebase constitutes decision "
    "logic; the remaining 98.4% is the operational harness. This ratio is not accidental — "
    "it is predicted by the five values and thirteen design principles of Section 2. "
    "The design gives the model maximum decision latitude within a rich operational harness, "
    "running counter to framework-heavy approaches (LangGraph's explicit graph nodes, "
    "Devin's multi-step planner). For agent builders, the implication is that investing in "
    "deterministic infrastructure such as context management, safety layering, and recovery "
    "mechanisms may yield greater reliability gains than adding planning scaffolding.",
    title="1.6% decision logic: infrastructure-over-scaffolding design philosophy",
    background=[recurring_design_commitments_setting],
)

strat_infra_philosophy = support(
    [five_values_motivate_architecture, reasoning_separation_claim],
    infrastructure_over_decision_scaffolding,
    reason=(
        "The five values (@five_values_motivate_architecture) — especially human decision "
        "authority and reliable execution — predict an architecture that creates conditions "
        "for good model decisions rather than constraining them. The reasoning-execution "
        "separation (@reasoning_separation_claim) is the architectural mechanism: the harness "
        "provides deterministic infrastructure; the model provides reasoning. The 1.6%/98.4% "
        "ratio is the quantitative consequence of this design philosophy, confirmed from "
        "source-level analysis (Tier B evidence)."
    ),
    prior=0.88,
)

value_tensions_are_structural = claim(
    "The five values identified in Section 2 generate tensions where pursuing one value "
    "constrains another. These tensions are structural consequences of pursuing multiple values "
    "simultaneously, not design failures. The empirically strongest tensions are: "
    "(1) Authority vs. Safety: 93% approval fatigue means safety cannot rely on human vigilance; "
    "(2) Safety vs. Capability: >50-subcommand fallback shows defense-in-depth degrades under "
    "performance pressure; "
    "(3) Adaptability vs. Safety: CVEs exploit extensibility's pre-trust initialization window; "
    "(4) Capability vs. Adaptability: proactivity increases task completion 12-18% but reduces "
    "preference at high frequencies; "
    "(5) Capability vs. Reliability: bounded context prevents full codebase awareness, while "
    "complexity increases in adjacent tools suggest bounded-context limitations compound over time.",
    title="Five value tensions are structural, not design failures",
    background=[value_tensions_table_setting],
)

strat_value_tensions = support(
    [approval_fatigue_observation, defense_in_depth_shared_failure_modes,
     graduated_trust_spectrum_claim],
    value_tensions_are_structural,
    reason=(
        "The empirical evidence for value tensions is strong: approval fatigue "
        "(@approval_fatigue_observation) directly demonstrates Authority vs. Safety tension; "
        "the defense-in-depth degradation (@defense_in_depth_shared_failure_modes) confirms "
        "Safety vs. Capability tension; the graduated trust spectrum (@graduated_trust_spectrum_claim) "
        "shows these tensions are navigated by habituation rather than deliberate selection. "
        "Table 4 in the source synthesizes these tensions with empirical evidence (Tier A/C). "
        "The tensions are intrinsic to pursuing all five values simultaneously."
    ),
    prior=0.9,
)

context_compression_opacity_tradeoff = claim(
    "The five-layer compaction pipeline achieves effective context management, but compression "
    "is largely invisible to the user. When budget reduction replaces a long tool output with "
    "a reference, when context collapse substitutes messages with a summary, or when snip "
    "trims older history, the user has no easy way to inspect what was lost. The cache-aware "
    "behavior of microcompact adds further opacity, as compression decisions are influenced by "
    "prompt caching in ways not visible to the user. This demonstrates the Capability vs. "
    "transparency architectural trade-off: context efficiency vs. user visibility.",
    title="Context compression opacity: efficiency vs. transparency trade-off",
    background=[value_tensions_table_setting],
)

strat_compression_opacity = support(
    [graduated_compaction_claim, context_window_as_binding_constraint],
    context_compression_opacity_tradeoff,
    reason=(
        "The graduated compaction pipeline (@graduated_compaction_claim) is architecturally "
        "necessary given the context window as binding constraint "
        "(@context_window_as_binding_constraint), but its five-layer design — with feature "
        "flags, cache-aware behavior, and read-time projection — creates opacity. The source "
        "explicitly acknowledges that 'context collapse' operates as 'a read-time projection "
        "over the REPL's full history' without user-visible output. This is confirmed from "
        "the discussion of context efficiency vs. transparency (Section 11.3, Tier A evidence)."
    ),
    prior=0.87,
)

extensibility_combinatorial_interactions = claim(
    "The four extension mechanisms enable rich customization but create combinatorial "
    "interactions that are difficult to predict from any single configuration file. A plugin "
    "contributing a PreToolUse hook interacts with the auto-mode classifier reading cached "
    "CLAUDE.md content; path-scoped rules loaded lazily when new directories are read can "
    "change classifier behavior mid-conversation; the permission handler's four branches "
    "interact with the hook pipeline at multiple points. These cross-cutting concerns create "
    "emergent behaviors that manifest as the Simplicity vs. Extensibility trade-off.",
    title="Extensibility creates combinatorial interactions",
    background=[value_tensions_table_setting],
)

strat_extensibility_interactions = support(
    [four_mechanisms_justified, claudemd_probabilistic_compliance],
    extensibility_combinatorial_interactions,
    reason=(
        "The four extension mechanisms (@four_mechanisms_justified) are individually justified "
        "by graduated context costs, but their interactions create complexity. "
        "CLAUDE.md's probabilistic compliance (@claudemd_probabilistic_compliance) compounds "
        "this: the classifier reads cached CLAUDE.md while hooks modify tool inputs, and the "
        "probabilistic compliance of CLAUDE.md instructions interacts with the deterministic "
        "hook pipeline in ways not easily predicted. This is the Simplicity vs. Extensibility "
        "trade-off identified in Section 11.3 (Tier A evidence)."
    ),
    prior=0.85,
)

bounded_context_code_quality_prediction = claim(
    "The architectural properties documented in this paper generate testable predictions: "
    "agent-generated code will exhibit higher rates of pattern duplication and convention "
    "violation than code produced with full codebase visibility (due to bounded context), and "
    "parallel subagents can independently re-implement solutions that already exist elsewhere "
    "(due to subagent isolation with independently assembled tool pools). Claude Code's "
    "context management pipeline is specifically designed to mitigate these effects (graduated "
    "compression, cache-aware compaction, read-time projection, subagent summary isolation), "
    "but whether these mechanisms are sufficient to overcome structural limitations of bounded "
    "context is a directly measurable empirical question that source-level analysis cannot resolve.",
    title="Bounded context predicts code quality degradation; mitigation mechanisms exist but remain unverified",
    background=[empirical_predictions_setting],
)

strat_code_quality_prediction = support(
    [isolated_context_boundaries, context_window_as_binding_constraint],
    bounded_context_code_quality_prediction,
    reason=(
        "Isolated context boundaries (@isolated_context_boundaries) — each subagent with its "
        "own context window and independently assembled tool pool — architecturally cannot "
        "share global codebase context. The context window as binding constraint "
        "(@context_window_as_binding_constraint) means no single session can maintain "
        "simultaneous awareness of a large codebase. Together, these architectural properties "
        "make the code quality prediction a logical consequence of the design. Empirical "
        "evidence from He et al. (2025) on Cursor (+40.7% complexity, velocity reverting to "
        "baseline) is consistent with these predictions in adjacent systems. "
        "Confirmed as architecturally predicted in Section 11.4 (Tier A/C evidence)."
    ),
    prior=0.85,
)

long_term_sustainability_gap = claim(
    "Two additional tensions surface through the evaluative lens of long-term capability "
    "preservation (Section 2.4). A randomized controlled trial of 16 experienced developers "
    "across 246 tasks (Becker et al., 2025) found that AI tools made developers 19% slower "
    "despite a perceived 20% improvement. An EEG study of 54 participants (Kosmyna et al., 2025) "
    "found that LLM users showed weakened neural connectivity that persisted after AI was removed. "
    "A 25% decline in entry-level tech hiring between 2023 and 2024 (Rak, 2025) suggests the "
    "tension between capability amplification and long-term sustainability extends beyond "
    "individual productivity to the broader developer pipeline. This evidence motivates the "
    "evaluative lens but does not target Claude Code's architecture specifically.",
    title="Long-term sustainability gap: evidence motivating the evaluative lens",
    background=[value_tensions_table_setting],
)

strat_sustainability = support(
    [long_term_capability_preservation_lens, bounded_context_code_quality_prediction],
    long_term_sustainability_gap,
    reason=(
        "The long-term capability preservation lens (@long_term_capability_preservation_lens) "
        "is motivated by empirical findings that AI tools may undermine the very capabilities "
        "they augment. The bounded context code quality prediction "
        "(@bounded_context_code_quality_prediction) extends this to architectural consequences: "
        "systems that produce pattern duplication and convention violation gradually degrade "
        "codebase coherence. The empirical evidence (19% slower, neural connectivity loss, "
        "hiring decline) motivates treating sustainability as a first-class design concern, "
        "not a downstream metric. Tier A/C evidence (Becker et al. 2025, Kosmyna et al. 2025, "
        "Rak 2025)."
    ),
    prior=0.8,
)
