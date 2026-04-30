"""Prior assignments for the abstract-level leaf claims.

The source artifact for arXiv:2604.03515 in this package is a thin stub
(title + arXiv link + GitHub link + keywords + two-sentence abstract). The
two abstract sentences (@source_code_taxonomy_built and
@structural_patterns_derived) are the only independent leaf claims; the five
keyword-topic claims are derived from them via support strategies, so no
priors are assigned to derived claims (the inference engine defaults to 0.5).

Both abstract claims are first-person factual assertions by the authors
about the *scope and methodology* of the work itself -- the kind of
statement that is straightforwardly verifiable by reading the paper.
Therefore both receive high priors. The exact figures are conservative: we
have not seen the body of the paper, so we cannot rule out that the precise
shape of the taxonomy or the size of the surveyed corpus differs from what
the abstract suggests.
"""

from .motivation import (
    source_code_taxonomy_built,
    structural_patterns_derived,
)

PRIORS = {
    source_code_taxonomy_built: (
        0.93,
        "Self-report of contribution in the abstract: the authors explicitly "
        "frame the work as a source-code taxonomy of coding-agent "
        "architectures. This is a methodological framing claim, not a "
        "quantitative result, and is directly verifiable by reading the "
        "paper. High prior.",
    ),
    structural_patterns_derived: (
        0.92,
        "Self-report of methodology in the abstract: the authors state that "
        "the taxonomy was derived by analysing real-world implementations to "
        "extract structural patterns in context / tools / state. The cited "
        "GitHub link (aorwall/moatless-tools) anchors the claim in concrete "
        "open-source code. Small downward adjustment from 0.95 because, "
        "having only the abstract stub, we cannot verify how broad the "
        "surveyed corpus actually is.",
    ),
}
