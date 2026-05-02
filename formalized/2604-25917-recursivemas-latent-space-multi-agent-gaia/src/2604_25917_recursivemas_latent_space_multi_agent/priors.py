"""Prior assignments for the title-level leaf claims.

The source artifact for arXiv:2604.25917 in this package is a thin stub
(title + arXiv link + three keywords + status line). The two title-level
sentences (@latent_space_is_the_mas_channel and
@recursivemas_realises_recursive_latent_mas) are the only independent
leaf claims; the three keyword claims are derived from them via support
strategies, so no priors are assigned to derived claims (the inference
engine defaults to 0.5).

Both leaf claims are framing assertions extracted from the paper's title --
the kind of statement the authors stake as the headline contribution of
the work. They are directly verifiable by reading the paper. The exact
figures are conservative: we have not seen the body of the paper, so we
cannot rule out that the precise scope of 'latent-space MAS' (e.g. whether
the channel is pure activation-passing, a learnt projection on top of
activations, or a hybrid latent-plus-token channel) or the precise meaning
of 'recursive' (e.g. self-calls of the same agent vs heterogeneous nested
sub-agents) differs in detail from the title-level reading.
"""

from .motivation import (
    latent_space_is_the_mas_channel,
    recursivemas_realises_recursive_latent_mas,
)

PRIORS = {
    latent_space_is_the_mas_channel: (
        0.9,
        "The central thesis is encoded directly in the paper's title "
        "('Latent-Space Multi-Agent'). The framing -- that the latent "
        "channel is itself the first-class MAS design axis -- is the "
        "authors' headline contribution, so the claim is well-evidenced "
        "*as the paper's stated position*. Held below 0.95 because, "
        "having only the title, we cannot inspect how strongly the body "
        "argues for latent-only versus latent-plus-token channels, nor "
        "what exactly the latent vectors are (raw activations vs a "
        "dedicated learnt embedding) -- a reading the body might "
        "qualify.",
    ),
    recursivemas_realises_recursive_latent_mas: (
        0.88,
        "Implied directly by the leading 'RecursiveMAS:' in the title -- "
        "the naming convention 'METHOD: thesis' is the standard way "
        "authors signal that METHOD is their proposed realisation of the "
        "thesis, and the 'Recursive' qualifier explicitly names the "
        "structural differentiator. Held slightly lower than the thesis "
        "itself because 'recursive' admits multiple precise readings "
        "(homogeneous self-call vs heterogeneous nested sub-agents vs "
        "fixed-depth nested ensemble), and title-only evidence cannot "
        "discriminate among them.",
    ),
}
