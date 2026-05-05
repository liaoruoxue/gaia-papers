"""Section 3.3 (Pillar 3): decision observability via the change manifest.

Every edit is paired with a self-declared prediction and verified against the
next round's task-level outcomes. Source: Lin et al. 2026 [@Lin2026AHE],
Section 3.3.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Pillar 3 setup
# ---------------------------------------------------------------------------

setup_change_manifest = setting(
    "**Change manifest schema (Appendix B.2).** Each Evolve Agent edit "
    "ships a `change_manifest.json` entry that names: "
    "(a) `failure_pattern` -- the failure class observed in evidence, "
    "(b) `description` (root cause + targeted fix), "
    "(c) `predicted_fixes` -- task names this edit should turn from "
    "fail to pass, "
    "(d) `risk_tasks` -- task names this edit may turn from pass to "
    "fail, "
    "(e) `constraint_level` -- which component class the edit lives at "
    "(prompt / tool description / tool implementation / middleware / "
    "skill), "
    "(f) `files` -- workspace-relative file paths touched. The manifest "
    "is written to the experiment root, not inside the workspace.",
    title="Setup: change manifest schema (failure pattern + predicted_fixes + risk_tasks + constraint_level)",
)

setup_attribution_check = setting(
    "**Attribution check (Phase 3 of the outer loop).** In iteration "
    "$t \\geq 2$, the loop intersects the prior manifest's "
    "`predicted_fixes` and `risk_tasks` sets with the observed task-"
    "level deltas (which tasks flipped fail -> pass, pass -> fail) "
    "between rounds $t-1$ and $t$, producing a per-edit verdict "
    "$V_t$. If predicted fixes do not materialize, the edit is rolled "
    "back at file granularity by reverting its git commit.",
    title="Setup: attribution check intersects predicted vs observed task-level deltas; ineffective edits rolled back",
)

setup_two_hard_constraints = setting(
    "**Two hard constraints on the Evolve Agent.** The Evolve Agent "
    "operates under two constraints that together realize decision "
    "observability: "
    "(C1) **Controllability** -- the Evolve Agent writes only inside "
    "the harness `workspace/`; the `runs/` directory, tracer, "
    "verifier, and LLM configuration are read-only, and the seed "
    "system prompt is non-deletable. These restrictions block the "
    "shortcuts an unconstrained self-modifier would take, such as "
    "disabling the verifier, swapping the model, or raising the "
    "reasoning budget. "
    "(C2) **Evidence-driven changes** -- every change ships with "
    "(i) failure evidence, (ii) inferred root cause, (iii) targeted "
    "fix, and (iv) predicted impact (expected fixes + at-risk "
    "regressions). Each edit thereby becomes falsifiable by the next "
    "evaluation, replacing rationale-driven self-justification with "
    "a measurable contract between rounds.",
    title="Setup: two hard constraints (controllability + evidence-driven) realize decision observability",
)

# ---------------------------------------------------------------------------
# Pillar 3 claims
# ---------------------------------------------------------------------------

claim_falsifiable_contract = claim(
    "**Each edit is a falsifiable, file-level contract.** The "
    "combination of (a) controllability bounds (workspace-only edits, "
    "read-only verifier), (b) evidence-driven manifest (failure "
    "pattern + predicted fixes + risk tasks), and (c) automatic "
    "attribution check that rolls back at file granularity means "
    "every edit is a falsifiable contract: the next evaluation either "
    "confirms or reverts it.",
    title="Pillar 3 claim: every edit is a falsifiable, file-level contract verified next round",
)

claim_controllability_blocks_shortcuts = claim(
    "**Controllability bounds keep recorded gains attributable to "
    "harness edits.** By making the verifier, tracer, LLM "
    "configuration, and seed prompt read-only / non-deletable, AHE "
    "blocks the shortcuts an unconstrained self-modifier would take "
    "(disabling the verifier, swapping the model, raising the "
    "reasoning budget). Every recorded pass@1 gain is therefore "
    "attributable to harness edits.",
    title="Pillar 3 claim: controllability blocks self-modification shortcuts; gains attributable to harness edits",
)

claim_decision_observability_solves_o3 = claim(
    "**Decision observability solves obstacle (O3) -- attribution "
    "opacity.** Because every edit's predicted impact is recorded "
    "before the next evaluation and verified against task-level "
    "deltas, ineffective edits are detected and reverted "
    "automatically rather than accumulating as silent technical "
    "debt. The Evolve Agent cannot rationalize away an edit that "
    "did not produce its predicted fixes; the manifest binds it.",
    title="Pillar 3 claim: decision observability automates attribution + rollback, solves O3",
)

# ---------------------------------------------------------------------------
# Self-attribution as evidence-driven (vs random) -- empirical claim
# from Section 4.4.2 / Fig. 4 lives here as an *empirical* claim that the
# decision-observability mechanism produces evidence-driven targeting.
# ---------------------------------------------------------------------------

claim_fix_attribution_quantitative = claim(
    "**Fix-side self-attribution metrics (Fig. 4 left, cross-iteration "
    "mean).** Across the 9 evaluation rounds where iteration $t$ "
    "compares its predictions to round $t+1$ ground truth, the "
    "Evolve Agent's fix predictions achieve **precision 33.7%** and "
    "**recall 51.4%**, against random-prediction baselines of **6.5%** "
    "and **10.6%** respectively. Both metrics are roughly 5x above "
    "the random baseline.",
    title="Pillar 3 metric: fix-prediction precision 33.7% / recall 51.4% (5x random baseline 6.5% / 10.6%)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 4 left",
        "caption": "Fig. 4 left: Cross-iteration fix precision and recall vs random-prediction baseline.",
    },
)

claim_regression_attribution_quantitative = claim(
    "**Regression-side self-attribution metrics (Fig. 4 right, cross-"
    "iteration mean).** Across the same 9 evaluation rounds, the "
    "Evolve Agent's regression predictions achieve **precision 11.8%** "
    "and **recall 11.1%**, against random-prediction baselines of "
    "**5.6%** and **5.4%** respectively. Both metrics sit only "
    "approximately 2x above their random baseline.",
    title="Pillar 3 metric: regression-prediction precision 11.8% / recall 11.1% (only 2x random baseline)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 4 right",
        "caption": "Fig. 4 right: Cross-iteration regression precision and recall vs random-prediction baseline.",
    },
)

claim_evidence_driven_targeting = claim(
    "**The Evolve Agent's fix targeting is evidence-driven.** Fix-"
    "precision (33.7%) and fix-recall (51.4%) sit ~5x above random-"
    "prediction baselines (6.5% / 10.6%), so each harness edit lands "
    "on a real, agent-anticipated target rather than on an arbitrary "
    "subset of the panel. The decision-observability machinery is "
    "therefore not just a bookkeeping device -- it carries actionable "
    "predictive content.",
    title="Empirical (Pillar 3): fix targeting is evidence-driven (5x random baseline)",
)

claim_regression_blindness = claim(
    "**The Evolve Agent is blind to upcoming regressions.** Regression-"
    "precision (11.8%) and regression-recall (11.1%) sit only ~2x "
    "above random baselines (5.6% / 5.4%), so most upcoming regressions "
    "go unforeseen. The agent can justify why an edit should help, "
    "but it cannot reliably name the tasks the same edit is about to "
    "break. This is the cause of the non-monotone steps in the AHE "
    "evolution curve and is identified as the clearest direction for "
    "future self-evolution loops.",
    title="Empirical (Pillar 3): regression prediction is near-blind, only 2x random; explains non-monotone evolution",
)

claim_per_round_regression_breakdown = claim(
    "**Per-round regression statistics (Appendix D).** Across the 9 "
    "rounds the Evolve Agent issued **43 unique regression "
    "predictions** of which only **5 landed**, giving cumulative "
    "precision $P = 11.6\\%$. **40 regressions the agent did not "
    "foresee actually occurred**, giving cumulative recall "
    "$R = 11.1\\%$. Per-round bars decompose each denominator into "
    "TP vs FP (precision panel) and TP vs FN (recall panel).",
    title="Pillar 3 detail: per-round regression breakdown (43 predicted, 5 landed; 40 unforeseen actual)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 12",
        "caption": "Fig. 12: Per-round regression predictions, precision and recall.",
    },
)

__all__ = [
    "setup_change_manifest",
    "setup_attribution_check",
    "setup_two_hard_constraints",
    "claim_falsifiable_contract",
    "claim_controllability_blocks_shortcuts",
    "claim_decision_observability_solves_o3",
    "claim_fix_attribution_quantitative",
    "claim_regression_attribution_quantitative",
    "claim_evidence_driven_targeting",
    "claim_regression_blindness",
    "claim_per_round_regression_breakdown",
]
