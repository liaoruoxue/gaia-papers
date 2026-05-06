"""Section 2.3: Self-Evolution -- individual-level evolution + organisation-
level evolution + HR performance review pipeline.

Source: Yu et al. 2026 [@Yu2026OMC], Section 2.3 (pages 12-13).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 2.3.1 Individual-level evolution
# ---------------------------------------------------------------------------

setup_two_individual_triggers = setting(
    "**Definition (Two individual reflection triggers).** Each "
    "agent maintains a persistent, auto-updating profile "
    "comprising a cross-task progress log and LLM-summarised "
    "working principles. Two triggers drive individual reflection: "
    "(R1) **CEO one-on-one** -- after each session, the agent "
    "performs structured self-reflection (review CEO feedback, "
    "identify expectation gaps, update working principles), "
    "mirroring manager-report one-on-ones in human organisations; "
    "(R2) **post-task review** -- upon task completion, the agent "
    "reviews its own execution trace (decisions, tools invoked, "
    "obstacles) and appends a summary to its progress log, "
    "accumulating a cross-task lessons-learned trajectory.",
    title="Setup: two individual reflection triggers -- CEO one-on-one + post-task review",
)

claim_individual_evolution_modifies_talent_artefacts = claim(
    "**Individual evolution modifies Talent artefacts, not the "
    "foundation model.** Updates change working-principle prompts "
    "and guidance notes (the Talent's prompt-level identity), "
    "*not* the underlying foundation model. This enables "
    "continuous improvement without retraining. In the formal "
    "model, updated working principles are reflected in the "
    "workforce state $\\mathcal{W}$, so subsequent calls to "
    "$\\pi(\\mathcal{T})$ (Section 2.2) see improved profiles.",
    title="Claim: individual evolution updates Talent prompts (not foundation model) -- improvement without retraining",
)

# ---------------------------------------------------------------------------
# 2.3.2 Organisation-level evolution: retrospectives + SOPs
# ---------------------------------------------------------------------------

setup_project_retrospective = setting(
    "**Definition (Project Retrospective).** When a project "
    "reaches completion, the COO convenes a retrospective in "
    "which each participating employee submits a self-assessment "
    "(key decisions, obstacles, solutions). The COO aggregates "
    "self-assessments with objective signals (per-task retry "
    "counts, review rejection reasons, resource consumption) and "
    "distils findings into two outputs: (D1) **individual "
    "feedback** updating each employee's working principles, and "
    "(D2) **organisational SOPs** codifying effective patterns for "
    "future projects (e.g., 'mandate API contract review before "
    "frontend-backend integration'). SOPs persist as workflow "
    "documents and are automatically injected into relevant "
    "agents' contexts on subsequent projects.",
    title="Setup: project retrospective -- COO aggregates self-assessments + objective signals into individual feedback + organisational SOPs",
)

claim_org_knowledge_accumulates_across_projects = claim(
    "**Organisational knowledge accumulates across projects.** "
    "Persisted SOPs are automatically injected into relevant "
    "agents' contexts on subsequent projects, so knowledge "
    "accumulates across the entire project history rather than "
    "being confined to individual agent memories. This is the "
    "structural mechanism that makes the organisation -- not just "
    "individual agents -- improve over time.",
    title="Claim: SOPs persist + auto-inject into future contexts => organisational knowledge accumulates across projects",
)

# ---------------------------------------------------------------------------
# Performance review and HR lifecycle
# ---------------------------------------------------------------------------

setup_hr_performance_pipeline = setting(
    "**Definition (HR Performance Review Pipeline).** Inspired by "
    "real-world HR practice: every three projects, the HR agent "
    "automatically initiates a periodic review for each "
    "participating employee, assessing task completion quality, "
    "review pass rates, and collaboration effectiveness. An "
    "employee failing three consecutive reviews enters a formal "
    "**Performance Improvement Plan (PIP)** -- targeted coaching, "
    "adjusted task assignments, closer supervision. If the "
    "employee fails one additional review under PIP, the system "
    "triggers automated **offboarding**: Container "
    "deprovisioning, desk freed, capability gap flagged for "
    "re-recruitment from the Talent Market.",
    title="Setup: HR pipeline -- every 3 projects review; 3 consecutive fails -> PIP; 1 PIP fail -> automated offboarding",
)

claim_hr_pipeline_closes_market_loop = claim(
    "**The HR pipeline closes the loop between the Talent Market "
    "and organisational evolution.** Underperforming agents are "
    "replaced by fresh recruits via the Talent Market; "
    "high-performing agents accumulate experience that makes them "
    "increasingly effective. The authors are not aware of prior "
    "work that applies structured HR protocols (periodic reviews, "
    "PIP, formal offboarding) to AI agent lifecycle management.",
    title="Claim: HR pipeline closes loop with Talent Market (replace underperformers, retain accumulators); novel for AI agents",
)

# ---------------------------------------------------------------------------
# Three-level evolution synthesis
# ---------------------------------------------------------------------------

claim_three_level_evolution_summary = claim(
    "**Three-level evolution loop.** "
    "(L1) **Individually** -- agents refine working principles "
    "through CEO one-on-ones and post-task self-reflection. "
    "(L2) **Organisationally** -- project retrospectives produce "
    "updated SOPs persisted as workflow documents and auto-"
    "injected into future agents' contexts. "
    "(L3) **Systemically** -- HR pipeline (periodic eval, PIP, "
    "automated offboarding) creates real consequences that make "
    "improvement non-optional. Together, these three levels turn "
    "OMC into a self-evolving organisation rather than a static "
    "framework.",
    title="Synthesis: three-level evolution (individual prompts + organisation SOPs + HR consequences) => self-evolving organisation",
)

__all__ = [
    "setup_two_individual_triggers",
    "claim_individual_evolution_modifies_talent_artefacts",
    "setup_project_retrospective",
    "claim_org_knowledge_accumulates_across_projects",
    "setup_hr_performance_pipeline",
    "claim_hr_pipeline_closes_market_loop",
    "claim_three_level_evolution_summary",
]
