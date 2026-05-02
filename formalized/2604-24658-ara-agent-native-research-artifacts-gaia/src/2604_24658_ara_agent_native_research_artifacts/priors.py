"""Prior assignments for the title-level leaf claims.

The source artifact for arXiv:2604.24658 in this package is a thin stub
(title + arXiv link + three keywords + status line). The two title-level
sentences (@artifacts_should_be_agent_native and
@ara_realises_agent_native_artifacts) are the only independent leaf claims;
the three keyword claims are derived from them via support strategies, so
no priors are assigned to derived claims (the inference engine defaults to
0.5).

Both leaf claims are framing assertions extracted from the paper's title --
the kind of statement the authors stake as the headline contribution of the
work. They are directly verifiable by reading the paper. The exact figures
are conservative: we have not seen the body of the paper, so we cannot rule
out that the precise normative shape of 'agent-native' (e.g. whether ARA
deprecates PDFs or merely supplements them) or the precise scope of the
ARA framework differs in detail from the title-level reading.
"""

from .motivation import (
    ara_realises_agent_native_artifacts,
    artifacts_should_be_agent_native,
)

PRIORS = {
    artifacts_should_be_agent_native: (
        0.9,
        "The central thesis is encoded directly in the paper's title "
        "('Agent-Native Research Artifacts'). Authors stake their headline "
        "contribution on this normative assertion, so the claim is "
        "well-evidenced *as the paper's stated position*. Held below 0.95 "
        "because, having only the title, we cannot inspect the empirical "
        "or argumentative case for the agent-native ideal in the body, and "
        "the strength of the claim ('should be') leaves room for a softer "
        "position in the actual text.",
    ),
    ara_realises_agent_native_artifacts: (
        0.88,
        "Implied directly by the leading 'ARA:' in the title -- the naming "
        "convention 'METHOD: thesis' is the standard way authors signal "
        "that METHOD is their proposed realisation of the thesis. Held "
        "slightly lower than the thesis itself because 'realises' is "
        "stronger than 'partially demonstrates', and title-only evidence "
        "cannot distinguish a complete framework from a prototype or a "
        "design sketch.",
    ),
}
