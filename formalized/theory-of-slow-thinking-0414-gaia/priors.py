"""Priors for the Theory of Slow Thinking and Active Perception package.

This file assigns priors to independent (leaf) claims — those not derived
from any reasoning strategy. The PRIORS dict maps Knowledge objects to
(prior_value, justification_string) tuples.

DO NOT set priors for derived claims (those that are conclusions of strategies);
their beliefs are determined by BP propagation from these leaf priors.
"""

from .s2_separation import claim_lifting_intractable
from .s5_deepseek import (
    claim_persistent_more_expressive,
    claim_stage1_explanatory_improves,
    claim_stage3_active_lifting,
    pred_alt_marginal,
    pred_explanatory_better,
)

PRIORS = {
    claim_lifting_intractable: (
        0.97,
        "Well-established mathematical result: Proj^{-1}_{<omega}(x) is exponential in |x| "
        "for Examples 5 and 6 (size |Gamma|^|x| and |Sigma|^{c|x|} respectively). "
        "Theorem 10 proves superpolynomially many latent sequences are necessary. "
        "This is a rigorous result with proof.",
    ),
    claim_persistent_more_expressive: (
        0.87,
        "Follows from the representation hierarchy established by Theorems 3, 9, 10. "
        "The hierarchy is well-founded theoretically, but the specific characterization "
        "of 'forgetful' vs 'persistent' latents is qualitatively stated in the paper "
        "without a separate formal theorem.",
    ),
    claim_stage1_explanatory_improves: (
        0.78,
        "Empirical result: GPT-2 Small experiment showing 264% relative improvement "
        "(test loss 1.7345 -> 1.7294 vs 1.7331 for predictive sampler). "
        "Preliminary small-scale experiment, but result is clear and directionally "
        "consistent with strong theoretical backing.",
    ),
    claim_stage3_active_lifting: (
        0.82,
        "Stage 3 (active lifting as free-form slow thinking) is a theoretical design proposal. "
        "Section 6 develops the framework thoroughly but with no experimental validation "
        "in this paper (Section 7 only tests Stage 1). Theoretical coherence is strong.",
    ),
    pred_alt_marginal: (
        0.2,
        "The alternative prediction (marginal improvement from explanatory samplers) "
        "is inconsistent with the rigorous theory showing causal samplers are generically "
        "suboptimal (Theorem 15, Proposition 16). Low prior.",
    ),
    pred_explanatory_better: (
        0.88,
        "Theory (Propositions 14-16) rigorously establishes that causal samplers cannot "
        "approximate Q* in chi^2 divergence. Strong theoretical basis for substantial "
        "improvement from explanatory samplers.",
    ),
}
