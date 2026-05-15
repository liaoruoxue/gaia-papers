"""Layer 2 strategies — SFT-then-RL (2604.23747)."""

from gaia.lang import claim, support, deduction
from .motivation import (
    two_bugs_suppress_sft_baseline,
    mixed_policy_gains_are_artifact,
    sft_then_rl_sufficient,
    cross_framework_validation_essential,
    math_domain_only,
    scale_limited,
)


# ── Bugs cause artifact (rigid: empirical accounting) ──

strat_bugs_explain_gains = deduction(
    [two_bugs_suppress_sft_baseline],
    mixed_policy_gains_are_artifact,
    reason=(
        "Two bugs suppress SFT baseline by ~5.7 points. Published mixed-policy "
        "gains over that buggy baseline are 3-5 points. Corrected SFT (54.0) "
        "already exceeds best mixed-policy (53.2). Simple accounting: gains "
        "attributed to algorithm are gains from baseline correction."
    ),
    prior=0.95,
)

# ── SFT-then-RL sufficiency, scoped to math + 7-8B ──

strat_sft_then_rl_validity = deduction(
    [mixed_policy_gains_are_artifact, math_domain_only, scale_limited],
    sft_then_rl_sufficient,
    reason=(
        "Once mixed-policy gains are shown to be baseline artifacts, simple "
        "SFT-then-RL becomes the natural baseline. Empirically it wins. "
        "Claim is scoped to math reasoning + 7-8B per the boundary premises; "
        "if other domains or larger scales falsify it, BP flags math_domain_only "
        "or scale_limited as the premise to revisit."
    ),
    prior=0.85,
)

# ── Methodological meta-claim (support-style) ──

strat_cross_framework = support(
    [two_bugs_suppress_sft_baseline],
    cross_framework_validation_essential,
    reason=(
        "Two bugs spanning three frameworks went undetected for months because "
        "no one compared SFT baselines across independent implementations. "
        "Discovery came from comparing OpenRLHF vs verl. This is the strongest "
        "empirical case so far for cross-framework validation as mandatory."
    ),
    prior=0.88,
)
