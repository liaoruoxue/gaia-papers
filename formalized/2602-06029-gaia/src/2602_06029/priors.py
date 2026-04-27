"""Priors for the package's independent (leaf) claims.

These are reviewer-assigned priors expressing how plausible each leaf claim is
*independently* of any reasoning chain. Values are within the Cromwell bounds
(1e-3, 0.999). Justifications cite the specific epistemic warrant.
"""

from . import (
    # --- Theorem 5.1 assumptions ---
    claim_assum_finite_prior_entropy,
    claim_assum_distinguishability,
    claim_assum_sufficient_curiosity_5,
    # --- Theorem 6.1 assumptions ---
    claim_assum_smoothness,
    claim_assum_heuristic_alignment,
    claim_assum_sufficient_curiosity_6,
    # --- Math axiom + lemmas (textbook / cited results) ---
    axiom_normal_density,
    lemma_b1_info_gain,
    lemma_b2_concentration,
    lemma_b3_mi_equality,
    # --- Predictions distilled from the theorems ---
    pred_th5_1_h0,
    pred_th5_1_at,
    pred_th5_1_curiosity,
    pred_th6_1_bt,
    pred_th6_1_beta,
    pred_csi_low_beta_stalls,
    pred_csi_high_beta_overexplores,
    # --- Tension claims from the introduction ---
    claim_low_curiosity_is_myopic,
    # --- Contribution claims (independent because @claim_curiosity_is_knowledge supports them) ---
    claim_contribution_consistency,
    claim_contribution_regret,
    # --- Limitations ---
    claim_lim_conservative,
    claim_lim_assumptions,
    claim_lim_alignment_practical,
    # --- Alternative explanations (abduction alternatives) ---
    alt_purely_random,
    alt_h0_entropy_unrelated,
    alt_csi_kernel_only,
    alt_cbo_random,
)

PRIORS = {
    # --- Theorem 5.1 assumptions ---
    # Finite prior entropy is a *meta*-assumption about the modeling setup. In
    # any practical use it can be designed in (use a discrete prior). High plausibility.
    claim_assum_finite_prior_entropy: (
        0.95,
        "Trivially satisfied for any discrete latent space with a finitely-supported prior. "
        "The paper assumes discrete S, so finite H_0 is a design choice the user controls.",
    ),
    # Observational distinguishability holds problem-by-problem. The theorem just
    # *requires* it for its conclusion; whether a *given* problem satisfies it is
    # an empirical matter. Moderate prior to reflect that the assumption can fail.
    claim_assum_distinguishability: (
        0.7,
        "Holds for well-designed experimental setups but can fail if the heuristic h_t "
        "filters out the discriminative signal (paper itself flags this). Moderate prior.",
    ),
    # The sufficient-curiosity inequality is a constraint on the choice of beta_t.
    # In practice the paper provides this as a design rule -- the theorem is conditional.
    claim_assum_sufficient_curiosity_5: (
        0.85,
        "A design constraint: the user/algorithm must set beta_t at or above the floor. "
        "If implemented as adaptive scheduling it holds by construction; high plausibility.",
    ),
    # --- Theorem 6.1 assumptions ---
    claim_assum_smoothness: (
        0.8,
        "Lipschitz smoothness is mild for most engineering objectives but can fail for "
        "discontinuous tasks (the paper explicitly notes this in Sec 6.3 and recommends "
        "deep GPs as mitigation).",
    ),
    claim_assum_heuristic_alignment: (
        0.7,
        "Bounded |r - h_t| holds when h_t is well-designed or learned online. The paper "
        "itself flags this as practically challenging (Sec. 9 limitations) -- moderate plausibility.",
    ),
    # Sufficient curiosity in Th 6.1 is *literally the same inequality* as in Th 5.1
    # (we capture this via equivalence operator). Use the same prior.
    claim_assum_sufficient_curiosity_6: (
        0.85,
        "Identical inequality to Eq. 5 (linked by equivalence in the formalization). "
        "Same justification as claim_assum_sufficient_curiosity_5.",
    ),

    # --- Math axiom + cited lemmas ---
    axiom_normal_density: (
        0.999,
        "Standard textbook identity for the normal distribution under linear substitution.",
    ),
    lemma_b1_info_gain: (
        0.99,
        "Established result (Srinivas et al. 2009, Lemma 5.3); peer-reviewed.",
    ),
    lemma_b2_concentration: (
        0.99,
        "Established result (Srinivas et al. 2009, Lemma 5.5); peer-reviewed.",
    ),
    lemma_b3_mi_equality: (
        0.95,
        "Cites Lemma 3.2 of [Li et al. 2026] (companion paper). Mutual-information "
        "equality is a standard data-processing-style identity.",
    ),

    # --- Predictions ---
    # These are derivative readings of the theorem bounds; they should be high
    # since they are direct algebraic consequences (and would be derived by
    # 'support' from the theorems, but priors model the *standalone* plausibility).
    pred_th5_1_h0: (
        0.9,
        "Direct algebraic reading of T >= bar_beta_T H_0 / (A_T epsilon). "
        "If the bound is correct, the H_0 dependence is automatic.",
    ),
    pred_th5_1_at: (
        0.9,
        "Direct algebraic reading of the same bound; A_T in the denominator.",
    ),
    pred_th5_1_curiosity: (
        0.88,
        "The proof depends on the curiosity floor (Eq. 5); below the floor the "
        "chain of inequalities breaks. Strong (but not deterministic since "
        "necessity vs. sufficiency is conflated in the qualitative claim).",
    ),
    pred_th6_1_bt: (
        0.9,
        "Direct algebraic reading of the additive sum_t B_t term in Eq. 9.",
    ),
    pred_th6_1_beta: (
        0.85,
        "Reading of the bar_beta_T rho_T term in Eq. 9. Subtle: 'larger beta inflates' "
        "is true above the floor but the floor itself is also data-dependent.",
    ),
    pred_csi_low_beta_stalls: (
        0.85,
        "Inverse scaling of the floor with informativeness follows directly from Eq. 5; "
        "high plausibility for the paper's own reading.",
    ),
    pred_csi_high_beta_overexplores: (
        0.85,
        "Same logic as pred_th6_1_beta applied to the CSI setting.",
    ),

    # --- Other independent claims ---
    claim_low_curiosity_is_myopic: (
        0.85,
        "The myopic-exploitation failure mode is well-attested in the AIF literature "
        "and is the dual statement of the sufficient-curiosity floor.",
    ),

    # --- Contribution claims (treated as independent because the theorems supply
    # the warrant for them; the contribution itself is a meta-claim about novelty) ---
    claim_contribution_consistency: (
        0.85,
        "Novelty claim ('first sample-complexity bound for posterior consistency of "
        "EFE-minimizing AIF agents'). Plausible given AIF literature, but novelty is "
        "always somewhat uncertain.",
    ),
    claim_contribution_regret: (
        0.85,
        "Novelty claim ('first general regret bound for AIF with GP settings'). "
        "Plausible; recovers Srinivas et al. 2009 as a special case.",
    ),

    # --- Limitations: these are claims *the paper itself* makes; very plausible ---
    claim_lim_conservative: (
        0.95,
        "Self-reported limitation in Sec. 9; derivative of how the bound was proved "
        "(union bounds, worst-case constants).",
    ),
    claim_lim_assumptions: (
        0.95,
        "Self-reported limitation in Sec. 9; standard caveat for any theoretical guarantee.",
    ),
    claim_lim_alignment_practical: (
        0.9,
        "Self-reported limitation; consistent with the paper's own Sec. 8.2 results "
        "showing learned heuristics outperforming constant biases.",
    ),

    # --- Abduction alternatives ---
    # pi(Alt) measures explanatory power *of Alt for the observation*, NOT the
    # alt's correctness as a standalone hypothesis. Set low because none of these
    # alternatives explain the *qualitative regime changes* observed.
    alt_purely_random: (
        0.15,
        "5-seed random variability cannot explain the qualitative regime change "
        "between, e.g., beta=0.05 (stalled) and beta=0.8 (converged) in Fig 1(c).",
    ),
    alt_h0_entropy_unrelated: (
        0.4,
        "Concentrated prior trivially placing more mass on s* is partially compatible "
        "with Fig 1(a)'s ordering but does not explain the *sample-complexity scaling* "
        "with H_0. Moderate explanatory power for the qualitative ordering only.",
    ),
    alt_csi_kernel_only: (
        0.25,
        "Plume-model artifacts could in principle produce non-monotone behavior, but "
        "the same pattern appearing across three structurally different tasks (a)/(b)/(c) "
        "with different parameter geometries argues against a model-specific cause.",
    ),
    alt_cbo_random: (
        0.2,
        "High-dimensional geometry is a confounder but does not predict the linear "
        "vs. sub-linear regret-growth distinction in Fig 4(a) -- a *functional-form* "
        "signature that geometry alone cannot reproduce.",
    ),
}
