"""Prior assignments for the title-level leaf claims.

The source artifact for arXiv:2602.00994 in this package is a thin stub
(title + arXiv link + three keywords + status line). The two title-level
sentences (@reasoning_and_tooluse_compete and @leas_dart_resolves_competition)
are the only independent leaf claims; the three keyword claims are derived
from them via support strategies, so no priors are assigned to derived
claims (the inference engine defaults to 0.5).

Both leaf claims are framing assertions extracted from the paper's title --
the kind of statement the authors are committing to as the headline
contribution of the work. They are directly verifiable by reading the paper.
The exact figures are conservative: we have not seen the body of the paper,
so we cannot rule out that the precise shape of the claimed competition
(e.g. whether it is symmetric across both skills) or the precise mechanism
of LEAS+DART differs in detail from the abstract-level reading.
"""

from .motivation import (
    leas_dart_resolves_competition,
    reasoning_and_tooluse_compete,
)

PRIORS = {
    reasoning_and_tooluse_compete: (
        0.9,
        "The central thesis is encoded directly in the paper's title "
        "('Reasoning and Tool-use Compete in Agentic RL'). Authors stake "
        "their headline contribution on this assertion, so the claim is "
        "well-evidenced *as the paper's stated finding*. Held below 0.95 "
        "because, having only the title, we cannot inspect the empirical "
        "demonstration of the competition in the body.",
    ),
    leas_dart_resolves_competition: (
        0.88,
        "Implied directly by the leading 'LEAS+DART:' in the title -- the "
        "naming convention 'METHOD: problem statement' is the standard way "
        "authors signal that METHOD is their proposed fix for the problem. "
        "Held slightly lower than the competition claim itself because "
        "'resolves' is stronger than 'mitigates', and abstract-only "
        "evidence cannot distinguish the two.",
    ),
}
