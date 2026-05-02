"""Prior assignments for the title-level leaf claims.

The source artifact for arXiv:2604.25850 in this package is a thin stub
(title + arXiv link + three keywords + status line). The two title-level
sentences (@harness_is_the_engineering_object and
@ahe_realises_harness_engineering) are the only independent leaf claims;
the three keyword claims are derived from them via support strategies, so
no priors are assigned to derived claims (the inference engine defaults to
0.5).

Both leaf claims are framing assertions extracted from the paper's title --
the kind of statement the authors stake as the headline contribution of
the work. They are directly verifiable by reading the paper. The exact
figures are conservative: we have not seen the body of the paper, so we
cannot rule out that the precise scope of 'engineering discipline'
(e.g. whether AHE proposes a full lifecycle methodology or merely a design
pattern catalogue) or the boundary between 'harness' and 'model' differs
in detail from the title-level reading.
"""

from .motivation import (
    ahe_realises_harness_engineering,
    harness_is_the_engineering_object,
)

PRIORS = {
    harness_is_the_engineering_object: (
        0.9,
        "The central thesis is encoded directly in the paper's title "
        "('Agentic Harness Engineering'). The framing -- that the harness "
        "is itself an engineering object worthy of a named discipline -- "
        "is the authors' headline contribution, so the claim is "
        "well-evidenced *as the paper's stated position*. Held below 0.95 "
        "because, having only the title, we cannot inspect how strongly "
        "the body argues for harness-over-model primacy versus the softer "
        "'harness alongside model' position, and 'should be a discipline' "
        "is a normative move whose force can vary in the actual text.",
    ),
    ahe_realises_harness_engineering: (
        0.88,
        "Implied directly by the leading 'AHE:' in the title -- the "
        "naming convention 'METHOD: thesis' is the standard way authors "
        "signal that METHOD is their proposed realisation of the thesis. "
        "Held slightly lower than the thesis itself because 'realises a "
        "discipline' is a strong claim and title-only evidence cannot "
        "distinguish a complete methodology from a design-pattern "
        "catalogue, a position paper, or an early framework sketch.",
    ),
}
