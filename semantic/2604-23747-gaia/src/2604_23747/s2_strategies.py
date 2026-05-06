"""Layer 2 strategies — SFT-then-RL (2604.23747)"""

from gaia.lang import support, abduction, contradiction
from 2604_23747.motivation import (
    two_bugs_suppress_sft_baseline, mixed_policy_gains_are_artifact,
    sft_then_rl_sufficient, cross_framework_validation_essential,
)

strat_bugs_cause_artifact = support(
    [two_bugs_suppress_sft_baseline],
    mixed_policy_gains_are_artifact,
    reason=(
        "If two bugs together suppress SFT baseline by ~5.7 points, and "
        "published mixed-policy gains over that buggy baseline are in the "
        "3-5 point range, then the gains are fully explained by baseline "
        "suppression. The corrected SFT baseline (54.0) already exceeds "
        "the best reported mixed-policy result (53.2). This is a simple "
        "accounting argument: gains attributed to algorithm are actually "
        "gains from fixing bugs."
    ),
    prior=0.95,
)

strat_sft_then_rl_beats_all = support(
    [mixed_policy_gains_are_artifact],
    sft_then_rl_sufficient,
    reason=(
        "Once the SFT baseline is corrected, standard online RL (SFT→RL) "
        "achieves 57.0 ID / 59.9 OOD — well beyond the best mixed-policy "
        "method. This suggests the mixed-policy innovation was solving a "
        "non-problem (buggy baselines) rather than a real one. The fact that "
        "50-step SFT-then-RL is compute-efficient strengthens the case: you "
        "don't need mixed-policy's complexity."
    ),
    prior=0.85,
)

alt_other_domains = claim(
    "Mixed-policy methods might still have value in domains where bugs "
    "manifest differently (coding, agent tasks) or at larger scales.",
    title="Alternative: mixed-policy may matter in other domains",
)

strat_domain_boundary = abduction(
    sft_then_rl_sufficient,
    [sft_then_rl_sufficient, alt_other_domains],
    reason=(
        "SFT-then-RL convincingly wins on math. But the claim's scope is "
        "limited to math reasoning benchmarks — the paper doesn't test coding "
        "or agent tasks. Bugs are framework-level and likely affect all "
        "domains, but the relative magnitude might differ. Until validated "
        "in other domains, the claim 'SFT-then-RL beats mixed-policy' should "
        "be read as '...on math reasoning at 7-8B scale.'"
    ),
    prior=0.75,
)

strat_cross_framework = support(
    [],
    cross_framework_validation_essential,
    reason=(
        "This paper is the strongest empirical case for cross-framework "
        "validation as mandatory practice. Two bugs went undetected for "
        "months because no one compared SFT baselines across OpenRLHF and "
        "verl. The finding required zero new algorithms — just running the "
        "same SFT recipe on two frameworks and noticing a discrepancy. "
        "This is a meta-scientific claim: the infrastructure of RL research "
        "has blind spots that cross-validation can catch."
    ),
    prior=0.92,
)
