"""Section 6: The (Human+AI)^2 Research Network.

Composing the four pillars (protocol §2 + Live Research Manager §3 +
Compiler §4 + Seal-gated review §5) yields a scientific communication
system whose primary object is no longer the static document but the
ARA itself: a single canonical artifact that humans on each end direct
agents to author, certify, render, and extend.
"""

from gaia.lang import claim

claim_paper_as_compiled_view = claim(
    "**The paper becomes a compiled view, not the primary object.** "
    "Composed, the four ARA pillars form a scientific communication "
    "system whose primary object is the **ARA itself**, with the "
    "narrative paper serving as a *compiled view* generated on demand. "
    "Authors no longer work toward papers; they pursue questions, and "
    "the paper-as-output accrues automatically as an ARA along the "
    "way: the Live Research Manager folds each decision, dead end, and "
    "confirmed claim into the artifact during ordinary work, the "
    "Compiler imports legacy sources on demand, and at any milestone "
    "the artifact is routed through the Seal pipeline and registered "
    "publicly.",
    title="Paper-as-compiled-view: the ARA is canonical, papers are renderings",
    metadata={"source_figure": "Fig. 10 (artifacts/2604.24658.pdf, p. 11)"},
)

claim_renderable_to_any_surface = claim(
    "**ARA is renderable to any surface a reader requires.** Because "
    "the ARA is canonical, an agent renders it on demand into whatever "
    "surface the reader needs (paper, video, slides, interactive demo, "
    "or grounded dialogue), shaped by the reader's expertise, "
    "attention budget, and intent. The single canonical artifact "
    "decouples authoring from delivery: every reader can receive the "
    "same scientific content at the resolution that matches their "
    "needs, instead of a single PDF that compromises across all "
    "audiences.",
    title="On-demand rendering: same ARA -> paper / slides / dialogue / interactive demo",
)

claim_git_like_publishing = claim(
    "**Publishing becomes a Git-like operation; contributions compound "
    "at the artifact level.** With both ends agent-mediated and the "
    "artifact the only persistent state, contributions compound at "
    "the level of *artifacts* rather than sentences: another team can "
    "fork a passing artifact, extend a claim, retain attribution to "
    "the parent, and submit the diff for re-review. Reviewers consume "
    "Seal-attested artifacts through their preferred surfaces; "
    "downstream agents read ARAs as structured baselines, training "
    "environments, or starting points for new questions. The scientific "
    "commons becomes queryable: every contribution is an executable "
    "diff, and the cost of understanding/reproduction/extension *falls* "
    "with each new artifact admitted.",
    title="Git-like publishing: forks, diffs, lineage; cost of consumption decreases with corpus",
)

__all__ = [
    "claim_paper_as_compiled_view",
    "claim_renderable_to_any_surface",
    "claim_git_like_publishing",
]
