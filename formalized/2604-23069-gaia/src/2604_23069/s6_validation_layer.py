"""Section 3.3: Validation and Test Layer.

Section 3.3 of [@Wu2026ContextWeaver]. The validation layer records
execution outcomes from each testing or verification step and provides two
complementary signals at different granularities: fine-grained per-test
results (TestTracker) and a coarse node-level label (ValidationDetector).
The label is consumed during graph construction to skip unreliable
predecessors, ensuring that new steps never depend on broken or superseded
states.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Signal granularities
# ---------------------------------------------------------------------------

setup_validation_two_signals = setting(
    "**Validation layer provides two granularities of signal.** "
    "(i) **Fine-grained**: a *TestTracker* parses tool observations "
    "(e.g., pytest, unittest output) and extracts individual test "
    "results into a `test_results` field. (ii) **Coarse / node-level**: "
    "a *ValidationDetector* assigns each node a label "
    "$\\text{validation\\_status} \\in \\{\\text{passed}, "
    "\\text{failed}, \\text{unknown}, \\text{superseded}\\}$ "
    "[@Wu2026ContextWeaver, Sec. 3.3].",
    title="Setup: two granularities -- TestTracker (per-test) + ValidationDetector (per-node label)",
)

# ---------------------------------------------------------------------------
# Fine-grained: TestTracker
# ---------------------------------------------------------------------------

claim_testtracker_extraction = claim(
    "**TestTracker parses tool observations and extracts individual "
    "test outcomes.** The TestTracker module reads pytest / unittest "
    "outputs in observation fields and extracts which tests passed or "
    "failed, populating both per-node `test_results` fields and a "
    "global tracker used to generate the prepended test summary "
    "[@Wu2026ContextWeaver, Sec. 3.3].",
    title="TestTracker: parses pytest/unittest outputs into structured test_results",
)

claim_testtracker_supersedes_pointer = claim(
    "**Per-test results support cross-node 'superseded' linking.** When "
    "a later node fixes an earlier failure, the system links them "
    "through a *superseded* pointer: the failed earlier node is "
    "marked as superseded by the later corrective node. This enables "
    "ContextWeaver to track which fixes addressed which failures "
    "across the trajectory [@Wu2026ContextWeaver, Sec. 3.3].",
    title="superseded pointer: later corrective node supersedes earlier failure",
)

# ---------------------------------------------------------------------------
# Coarse: ValidationDetector
# ---------------------------------------------------------------------------

claim_validation_status_labels = claim(
    "**Node-level validation labels: passed / failed / unknown / "
    "superseded.** Based on the collected per-test results, the "
    "ValidationDetector assigns each node one of four labels "
    "indicating whether the step produced a stable outcome: "
    "*passed* (tests confirmed success), *failed* (tests confirmed "
    "failure), *unknown* (no decisive test signal), *superseded* "
    "(replaced by a later corrective node) "
    "[@Wu2026ContextWeaver, Sec. 3.3].",
    title="Node labels: passed / failed / unknown / superseded",
)

# ---------------------------------------------------------------------------
# How the label feeds graph construction
# ---------------------------------------------------------------------------

claim_failed_skipped_during_construction = claim(
    "**Failed nodes are skipped when searching for parent candidates -- "
    "new steps never depend on broken states.** During graph "
    "construction, nodes marked *failed* are excluded from the "
    "candidate set $C_k$ used by the parent-selection analyzer. As a "
    "result, no new node can take a known-broken node as a parent, and "
    "ongoing reasoning is anchored on stable predecessors "
    "[@Wu2026ContextWeaver, Sec. 3.3, Algorithm 1 line 2].",
    title="Construction rule: failed nodes excluded from parent candidate set C_k",
)

claim_passed_unknown_form_backbone = claim(
    "**Passed and unknown nodes remain available; they form the "
    "'reliable backbone' of the reasoning graph.** Nodes labeled "
    "*passed* or *unknown* remain in the candidate set and form the "
    "reliable backbone of the reasoning graph. *unknown* is "
    "deliberately retained (rather than excluded) so that steps "
    "without decisive test signals -- e.g., file inspections or "
    "exploratory reads -- can still serve as parents "
    "[@Wu2026ContextWeaver, Sec. 3.3].",
    title="passed + unknown remain candidates -> reliable backbone of the reasoning graph",
)

claim_superseded_skipped = claim(
    "**Superseded nodes are skipped during parent search because their "
    "content has been replaced by a later correction.** Once a node "
    "is superseded by a corrective node, future parent selection no "
    "longer considers the superseded node as a candidate, preventing "
    "downstream reasoning from anchoring on stale or "
    "since-overwritten conclusions "
    "[@Wu2026ContextWeaver, Sec. 3.3].",
    title="superseded nodes excluded from future parent candidates",
)

# ---------------------------------------------------------------------------
# Why two signals?
# ---------------------------------------------------------------------------

claim_two_signals_rationale = claim(
    "**Separating node-level status from raw test results enables "
    "fast graph decisions without re-parsing detailed logs.** Keeping "
    "the coarse `validation_status` label distinct from the detailed "
    "`test_results` field allows ContextWeaver to make quick "
    "constructions / pruning decisions ('skip failed parents') without "
    "repeatedly parsing detailed pytest logs at every step "
    "[@Wu2026ContextWeaver, Sec. 3.3].",
    title="Rationale: coarse label + detailed results => fast graph decisions",
)

claim_validation_closes_loop = claim(
    "**The validation layer closes the loop between reasoning and "
    "execution.** ContextWeaver prepends the most recent validation "
    "summary to the assembled prompt before sending it to the agent, so "
    "the model sees the outcome of its previous actions directly in its "
    "next input. This reduces redundant exploration and encourages more "
    "deliberate planning [@Wu2026ContextWeaver, Appendix A].",
    title="Validation layer closes the reasoning-execution loop via prepended summary",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "setup_validation_two_signals",
    "claim_testtracker_extraction",
    "claim_testtracker_supersedes_pointer",
    "claim_validation_status_labels",
    "claim_failed_skipped_during_construction",
    "claim_passed_unknown_form_backbone",
    "claim_superseded_skipped",
    "claim_two_signals_rationale",
    "claim_validation_closes_loop",
]
