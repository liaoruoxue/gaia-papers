"""Layer 2 — Inside the Scaffold: 13-Agent Source-Code Taxonomy (2604.03515)

Core contribution: taxonomy of 13 coding agent scaffolds based on source code
(not capability labels), revealing spectra, loop primitives, and convergence patterns.
"""

from gaia.lang import claim, setting

# ── Core semantic claims ──

scaffold_taxonomy_fills_gap = claim(
    "Prior coding agent surveys classify agents by capability labels (e.g., "
    "'planning', 'tool-use', 'memory'). This taxonomy approach fails because "
    "every agent fits all labels — labels do not discriminate. This paper "
    "builds the first source-code-level taxonomy of 13 production coding "
    "agent scaffolds, grounded in 296 commit-pinned, file/line-cited "
    "architectural claims across 12 orthogonal dimensions in 3 layers "
    "(Control Architecture, Tool & Environment, Resource Management).",
    title="Source-code taxonomy fills gap left by capability-label surveys",
    aggregated_from=[
        "claim_existing_surveys_inadequate",
        "claim_capability_taxonomies_indistinguishable",
        "claim_contribution_taxonomy",
        "claim_contribution_evidence_base",
    ],
)

agents_are_spectra_not_categories = claim(
    "Across all 12 dimensions, agents form continuous spectra rather than "
    "discrete clusters. No single dimension cleanly separates any subset of "
    "agents. This means 'is this a ReAct agent?' or 'does this use planning?' "
    "are the wrong questions — the right question is 'where on each dimension "
    "does this agent fall?'",
    title="Coding agents are spectra, not discrete categories",
    aggregated_from=[
        "claim_finding_spectra_not_categories",
        "claim_react_reflexion_paradigms",
    ],
)

loop_primitives_compose = claim(
    "5 architectural loop primitives (Fetch→Process→Reflect→Decide→Act) "
    "are composed by 11 of 13 agents studied. This composition is the key "
    "architectural differentiator — not the presence/absence of any single "
    "capability, but how loops are chained and nested. This explains why "
    "capability labels fail: they describe what loops DO, not how loops "
    "are STRUCTURED.",
    title="Loop primitives compose as the key architectural differentiator",
    aggregated_from=[
        "claim_contribution_loop_primitive_thesis",
        "claim_finding_loop_primitives_compose",
    ],
)

convergence_on_constrained_dims = claim(
    "Agents converge on dimensions constrained by external infrastructure "
    "(e.g., tool execution sandboxing, file I/O patterns determined by "
    "the IDE). They diverge on dimensions where no external constraint "
    "exists (e.g., planning granularity, error recovery strategy). This "
    "convergence/divergence pattern predicts where future standardization "
    "is likely (high convergence) vs where innovation space remains (high "
    "divergence).",
    title="Convergence on externally-constrained dimensions, divergence on open ones",
    aggregated_from=[
        "claim_finding_convergence_divergence",
    ],
)

methodology_commit_pinned_claims = claim(
    "All taxonomic claims are commit-pinned and file/line-cited to specific "
    "source locations. This enables independent verification and automatic "
    "staleness detection — when a scaffold's source code changes, affected "
    "taxonomic claims can be flagged for re-review. This is a methodological "
    "advance over capability-label surveys which are unfalsifiable (every "
    "agent fits every label).",
    title="Commit-pinned, file/line-cited claims enable verification and staleness detection",
    aggregated_from=[
        "claim_finding_methodological_contribution",
        "claim_contribution_evidence_base",
    ],
)

# ── Boundary ──

snapshot_not_longitudinal = claim(
    "The taxonomy is a snapshot of 13 scaffolds at specific commits. "
    "Scaffolds evolve rapidly (monthly releases). Claims may go stale "
    "within 3-6 months without re-verification.",
    title="Snapshot limitation: scaffolds evolve rapidly",
)
