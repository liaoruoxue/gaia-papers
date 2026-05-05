"""Section III.D: Typed Memory Schema (13 semantic categories).

Section III.D of [@Abtahi2026Memanto] defines Memanto's typed memory
schema. The schema is the central architectural alternative to
knowledge-graph relational structure: rather than encoding entity-
relationship structure in an explicit graph, Memanto encodes *type*
semantics on each memory entry, where each type carries distinct
retrieval and decay semantics.

The 13-category schema is reproduced verbatim from Table II.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# III.D Typed schema definition (Table II)
# ---------------------------------------------------------------------------

setup_typed_schema = setting(
    "**13-category typed memory schema (Table II).** Memanto implements a "
    "typed memory schema with 13 built-in semantic categories. Each "
    "category carries distinct retrieval semantics and priority "
    "weighting; the user selects a category at write time (current "
    "release) with a planned automated rule-based assignment in a future "
    "release [@Abtahi2026Memanto, Sec. III.D; Appendix C]:\n\n"
    "| Type | Description | Example | Priority Signal |\n"
    "|------|-------------|---------|-----------------|\n"
    "| fact | Objective, verifiable information | User is in PST timezone | Stable, high confidence |\n"
    "| preference | User or system preferences | Prefers dark mode | Moderate decay |\n"
    "| decision | Choices made affecting future | Chose PostgreSQL for DB | High persistence |\n"
    "| commitment | Promises or obligations | Deliver report by Friday | Time critical |\n"
    "| goal | Objectives to achieve | Reach 10K users by Q4 | Active until achieved |\n"
    "| event | Historical occurrences | Meeting with CEO at 2pm | Episodic, decaying |\n"
    "| instruction | Rules and guidelines | Always validate input | Procedural, persistent |\n"
    "| relationship | Entity connections | Alice manages Bob | Graph-like, stable |\n"
    "| context | Situational information | Currently in budget review | Highly temporal |\n"
    "| learning | Lessons from experience | Users need simpler onboarding | Accumulating |\n"
    "| observation | Patterns noticed | Traffic peaks on Fridays | Statistical, evolving |\n"
    "| error | Mistakes to avoid | Do not use deprecated API | Persistent guard |\n"
    "| artifact | Document or code references | Q3 budget spreadsheet | Reference pointer |",
    title="Setup: Memanto typed memory schema = 13 semantic categories (Table II)",
)

# ---------------------------------------------------------------------------
# Claims about what the schema does
# ---------------------------------------------------------------------------

claim_typing_motivated_by_cogsci = claim(
    "**The typed schema is motivated by Tulving's cognitive memory "
    "taxonomy and ENGRAM's empirical finding.** The 13-category schema "
    "is a more granular instantiation of the cognitive episodic / "
    "semantic / procedural distinction [@Tulving1972]: e.g. *event* and "
    "*context* are episodic, *fact* and *learning* are semantic, "
    "*instruction* is procedural. The empirical justification comes from "
    "ENGRAM [@ENGRAM]: typed memory separation significantly outperforms "
    "undifferentiated storage on both LongMemEval and LoCoMo "
    "[@Abtahi2026Memanto, Sec. III.D].",
    title="Schema rationale: Tulving's taxonomy + ENGRAM's empirical evidence for typed separation",
)

claim_typing_dual_purpose = claim(
    "**The typing system serves two purposes: type-filtered retrieval + "
    "implicit priority/decay signals.** First, it enables type-filtered "
    "retrieval -- agents can query specifically for *commitments* or "
    "*decisions* without polluting the result set with unrelated "
    "categories. Second, each type's *Priority Signal* column (e.g. "
    "*context = highly temporal*, *instruction = procedural, persistent*) "
    "provides implicit priority and decay signals that the retrieval "
    "engine uses to weight results appropriately "
    "[@Abtahi2026Memanto, Sec. III.D].",
    title="Typing dual purpose: type-filtered retrieval + implicit priority/decay weighting",
)

claim_schema_satisfies_d4 = claim(
    "**The 13-category schema architecturally satisfies D4 (typed and "
    "hierarchical).** By providing explicit type semantics (with the "
    "13-way categorisation refining the standard episodic / semantic / "
    "procedural three-way split), Memanto satisfies D4 "
    "[@Abtahi2026Memanto, Sec. III.A; Sec. III.D; Table I].",
    title="Schema architecturally satisfies D4 (typed and hierarchical memory)",
)

# ---------------------------------------------------------------------------
# Manual assignment caveat
# ---------------------------------------------------------------------------

claim_manual_type_assignment = claim(
    "**Type assignment is manual at write time in the current release.** "
    "Memory type assignment is currently performed by the user at write "
    "time (selecting from the 13-category schema). Automated type "
    "assignment via a rule-based decision tree is planned for a future "
    "release and will eliminate this manual step "
    "[@Abtahi2026Memanto, Appendix C].",
    title="Caveat: type assignment is manual at write time (auto-assignment planned)",
)

__all__ = [
    "setup_typed_schema",
    "claim_typing_motivated_by_cogsci",
    "claim_typing_dual_purpose",
    "claim_schema_satisfies_d4",
    "claim_manual_type_assignment",
]
