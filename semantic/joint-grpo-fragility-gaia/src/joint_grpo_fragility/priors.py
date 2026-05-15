from .claims import grpo_has_systemic_weakness, bdry_grpo_fine_on_corrected_math

PRIORS: dict = {
    grpo_has_systemic_weakness: (
        0.55,
        "Joint claim across 3 papers. Lower prior than 2-paper version "
        "because the addition of SFT-then-RL counter-evidence narrows the "
        "claim's scope (axis-specific rather than universal)."
    ),
    bdry_grpo_fine_on_corrected_math: (
        0.92,
        "Strong direct evidence from 2604.23747 — empirical demonstration "
        "on Qwen2.5-Math-7B with framework bugs fixed."
    ),
}
