"""Prior assignments for the title-level leaf claims.

The source artifact for arXiv:2604.06159 in this package is a thin stub
(title + arXiv link + four keywords + status line). The two title-level
sentences (@target_policy_is_the_optimisation_object and
@tpo_realises_target_policy_optimization) are the only independent leaf
claims; the four keyword claims are derived from them via support
strategies, so no priors are assigned to derived claims (the inference
engine defaults to 0.5).

Both leaf claims are framing assertions extracted from the paper's title --
the kind of statement the authors stake as the headline contribution of
the work. They are directly verifiable by reading the paper. The exact
figures are conservative: we have not seen the body of the paper, so we
cannot rule out that the precise scope of 'target policy' (e.g. whether
TPO constructs the target from the best-of-group rollout, an expert
demonstration, or a frozen reference model) or the exact form of the
update rule differs in detail from the title-level reading.
"""

from .motivation import (
    target_policy_is_the_optimisation_object,
    tpo_realises_target_policy_optimization,
)

PRIORS = {
    target_policy_is_the_optimisation_object: (
        0.9,
        "The central thesis is encoded directly in the paper's title "
        "('Target Policy Optimization'). The framing -- that an explicit "
        "target policy should be the optimisation object during LLM RL "
        "fine-tuning -- is the authors' headline contribution, so the "
        "claim is well-evidenced *as the paper's stated position*. Held "
        "below 0.95 because, having only the title, we cannot inspect "
        "how strongly the body argues for target-policy primacy versus "
        "the softer 'target policy alongside GRPO advantage' position, "
        "nor can we verify the exact construction of the target.",
    ),
    tpo_realises_target_policy_optimization: (
        0.88,
        "Implied directly by the leading 'TPO:' in the title -- the "
        "naming convention 'METHOD: thesis' is the standard way authors "
        "signal that METHOD is their proposed realisation of the thesis. "
        "Held slightly lower than the thesis itself because 'realises a "
        "training rule' is a strong claim and title-only evidence cannot "
        "distinguish a complete algorithm specification from an early "
        "framework sketch, nor pin down the precise update form (pure "
        "cross-entropy vs. cross-entropy + auxiliary GRPO term, on-"
        "policy vs. off-policy target construction, etc.).",
    ),
}
