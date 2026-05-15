"""Layer 2 priors — SFT-then-RL (2604.23747)."""

from .motivation import (
    two_bugs_suppress_sft_baseline,
    mixed_policy_gains_are_artifact,
    sft_then_rl_sufficient,
    cross_framework_validation_essential,
    math_domain_only,
    scale_limited,
)


PRIORS: dict = {
    two_bugs_suppress_sft_baseline: (
        0.96,
        "Both bugs unambiguously confirmed: DeepSpeed PR #6550 is the commit; "
        "loss aggregation bug independently verifiable from OpenRLHF source. "
        "5.7 point impact measured on Qwen2.5-Math-7B."
    ),
    mixed_policy_gains_are_artifact: (
        0.93,
        "Simple accounting: gains 3-5 pt over baseline that's suppressed 5.7 pt → "
        "fully explained by baseline suppression. Corrected SFT (54.0) ≥ best "
        "mixed-policy (53.2). -0.05: math only."
    ),
    sft_then_rl_sufficient: (
        0.85,
        "57.0 ID / 59.9 OOD on Qwen2.5-Math-7B beats best mixed-policy. "
        "-0.10: 7-8B math only; -0.05: no coding/agent validation."
    ),
    cross_framework_validation_essential: (
        0.92,
        "Methodological claim supported by the case study. -0.08: a single "
        "case is not yet decisive evidence."
    ),
    math_domain_only: (
        0.95,
        "Documented experimental scope."
    ),
    scale_limited: (
        0.95,
        "Documented experimental scope."
    ),
}
