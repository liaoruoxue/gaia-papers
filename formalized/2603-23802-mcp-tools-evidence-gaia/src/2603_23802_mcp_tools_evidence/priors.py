"""Prior assignments for the abstract-level leaf claims.

The source artifact for arXiv:2603.23802 in this package is a thin stub
(title + arXiv link + GitHub link + keywords + two-sentence abstract). The
two abstract sentences (@empirical_177k_tools_analyzed and
@evidence_based_scale_study) are the only independent leaf claims; the five
keyword-topic claims are derived from them via support strategies, so no
priors are assigned to derived claims (the inference engine defaults to 0.5).

Both abstract claims are first-person factual assertions by the authors about
the *scope and methodology* of the work itself -- the kind of statement that
is straightforwardly verifiable by reading the paper. Therefore both receive
high priors. The exact figures are conservative: we have not seen the body of
the paper, so we cannot rule out that the headline number ('177,000') is
slightly different in the final published version.
"""

from .motivation import (
    empirical_177k_tools_analyzed,
    evidence_based_scale_study,
)

PRIORS = {
    empirical_177k_tools_analyzed: (
        0.92,
        "Self-report of methodology in the abstract: the authors explicitly "
        "state that 177,000 MCP tools were analysed empirically. The number is "
        "specific (not a round figure used loosely) and the GitHub link to the "
        "MCP server registry provides a concrete population. Small downward "
        "adjustment from 0.95 to acknowledge that, having only the abstract "
        "stub, we cannot independently verify exact tool counts or sampling "
        "method.",
    ),
    evidence_based_scale_study: (
        0.93,
        "Self-report of study posture: the abstract describes the work as an "
        "evidence-based study of how agents actually use tools at scale. This "
        "is a methodological framing claim, not a quantitative result, and is "
        "directly verifiable by reading the paper. High prior.",
    ),
}
