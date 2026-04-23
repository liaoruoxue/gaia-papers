"""Priors for independent (leaf) claims in the 2510.20817 knowledge package.

Each prior reflects the author's confidence in the claim based on:
- Quality and type of supporting evidence (direct experiment, citation, theory)
- Reproducibility and corroboration across multiple sources
- Whether the claim is definitional/axiomatic or empirical

Prior calibration rationale:
- Experimental results (directly observed from paper figures/tables): 0.90-0.95
- Well-established prior results (corroborated by multiple citations): 0.88-0.95
- Algorithmic/definitional claims (mathematical specifications): 0.95-0.97
- Qualitative/interpretive claims or alternatives: 0.25-0.55
"""

from .motivation import (
    empirical_diversity_collapse,
    vi_kl_intuition_fails_flexible,
    vi_kl_intuition_holds_restrictive,
)
from .s5_mara import (
    mara_augmented_reward,
    mara_works_fwd_kl,
)
from .s6_experiments import (
    alt_exploration,
    exp_12_vanilla_collapses,
    pred_exploration,
    pred_objective,
)

PRIORS = {
    # ── Motivation / Introduction claims ──────────────────────────────────────────

    empirical_diversity_collapse: (
        0.93,
        "Extensively documented finding corroborated by Kirk et al. 2023, Cui et al. 2025, "
        "and multiple works cited in Appendix A. The phenomenon (RL reduces entropy) is "
        "consistently reported across diverse tasks (format, creativity, reasoning). "
        "High confidence in the qualitative direction; exact magnitude varies by setting.",
    ),

    vi_kl_intuition_holds_restrictive: (
        0.97,
        "Standard result in variational inference (Jordan 1999, Blei 2017, Wainwright 2008). "
        "For restricted Gaussian families, reverse-KL mode-seeking vs. forward-KL mass-covering "
        "is a textbook property. No controversy; supported by decades of VI literature.",
    ),

    vi_kl_intuition_fails_flexible: (
        0.90,
        "The paper proves this rigorously for the case where the global optimum is achieved "
        "(Remarks 3.1-3.4, Figure 1b). The argument requires the policy family to be flexible "
        "enough to reach the optimum, which holds for modern LLMs but may fail in practice "
        "due to optimization landscape issues. Moderate-high confidence.",
    ),

    # ── MARA algorithm claims ──────────────────────────────────────────────────────

    mara_augmented_reward: (
        0.97,
        "Definitional claim: Algorithm 1 precisely specifies R_bar(y). This is a mathematical "
        "definition, not an empirical assertion. Very high confidence since it describes "
        "exactly what the algorithm does (Eq. 11). The only uncertainty is transcription "
        "accuracy from the paper.",
    ),

    mara_works_fwd_kl: (
        0.85,
        "Figure 5 shows empirical results for both KL variants. The claim is directly supported "
        "by controlled experiments in the paper. Slight uncertainty: this is a single-paper "
        "result not yet independently replicated, and the theoretical justification for "
        "forward-KL effectiveness is more informal (the paper notes the augmentation addresses "
        "the same probability-ratio imbalance).",
    ),

    # ── Experiment 1-2 claims ──────────────────────────────────────────────────────

    exp_12_vanilla_collapses: (
        0.95,
        "Direct experimental observation from Figure 6a: all but one vanilla RL run (across "
        "reverse-KL and forward-KL, multiple beta values) collapse to generating only '1'. "
        "The result is clear and unambiguous in the figure. Very high confidence.",
    ),

    alt_exploration: (
        0.35,
        "The exploration-failure hypothesis is a plausible alternative a priori, but it is "
        "essentially falsified by the MARA experiment: MARA (which does NOT change exploration "
        "strategy) successfully prevents collapse. The residual prior reflects the possibility "
        "that MARA works partially through exploration-adjacent mechanisms (e.g., reward "
        "shaping may implicitly alter the optimization landscape in complex ways).",
    ),

    pred_objective: (
        0.88,
        "Conditional prediction: IF the RL objective has a unimodal optimal solution, THEN "
        "MARA (which directly constructs a multimodal target) should prevent collapse. "
        "This follows almost definitionally from MARA's design (Section 5, Appendix B.7). "
        "The high prior reflects near-logical entailment from theory.",
    ),

    pred_exploration: (
        0.25,
        "Conditional prediction: IF collapse is due to exploration failure, THEN MARA (which "
        "only modifies reward magnitudes) should NOT prevent collapse. "
        "The paper empirically falsifies this prediction: MARA does prevent collapse without "
        "changing exploration. Hence prior is low but not negligible (exploration arguments "
        "could be partially true in settings the paper did not test).",
    ),
}
