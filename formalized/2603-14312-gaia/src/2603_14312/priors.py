"""Prior assignments for independent (leaf) claims in the ScienceClaw + Infinite formalization."""

from . import (
    ai_science_gap,
    alt_boron_rich,
    analogy_bayesian,
    analogy_degree_sequence,
    analogy_ontology,
    analogy_power_law,
    central_coordination_necessary,
    design_gap_claim,
    emergent_coordination_claim,
    framework_overview,
    hypothesis_boron_rich,
    lsystem_claim,
    materials_screening_result,
    pca_result,
    pred_artifact,
    pred_covalent,
    provenance_traceability_claim,
    quantitative_summary,
    sstr2_weight_finding,
)

PRIORS = {
    # ─── High confidence: well-described system facts ───────────────────────
    framework_overview: (
        0.92,
        "The three-component architecture (skill registry, artifact DAG, Infinite platform) is "
        "explicitly described in the paper's abstract and system design section. The description "
        "is self-consistent and detailed enough to be credible as a system design claim.",
    ),
    provenance_traceability_claim: (
        0.88,
        "The claim that any published number traces back to its computation follows from the "
        "DAG artifact design, which is well-specified. However, the paper does not include "
        "an adversarial audit of the provenance chain, so minor credibility discount applies.",
    ),
    quantitative_summary: (
        0.90,
        "Table 1 provides explicit artifact, synthesis, and DAG depth counts for all four "
        "studies. These are direct observational records from the running system. High prior "
        "reflects low likelihood of systematic fabrication, though no independent replication exists.",
    ),
    ai_science_gap: (
        0.80,
        "The claim that no prior system supports a persistent open multi-agent autonomous "
        "science ecosystem is a reasonable characterization of the literature circa 2025, "
        "supported by the contrast with cited prior work. Some discount for possible "
        "omission of comparable systems.",
    ),

    # ─── Empirical observations from case studies ────────────────────────────
    materials_screening_result: (
        0.85,
        "The finding of 14 phases satisfying dual constraints (density < 5 g/cm³, modulus > 200 GPa) "
        "with 7 thermodynamically stable is a DFT computation result. High credibility because "
        "DFT for these properties is well-validated; small discount for potential database gaps.",
    ),
    pca_result: (
        0.88,
        "PCA of a 39-resonator feature matrix is a standard, reproducible computation. "
        "The variance fractions (61.2% PC1, 27.4% PC2) are well-determined for a matrix of "
        "this size. High prior reflects methodological soundness.",
    ),
    design_gap_claim: (
        0.82,
        "The design gap coordinates (-0.521, +0.425) and the 12× proximity ratio to biological "
        "centroid are geometric quantities computed from the PCA embedding. Prior is slightly "
        "lower than pca_result because the gap identification involves a subjective threshold "
        "for what counts as a 'gap' in the feature space.",
    ),
    sstr2_weight_finding: (
        0.92,
        "Molecular weight of MGLKNFFLKTFTSC (~1639 Da) is a straightforward computation from "
        "amino acid masses. Octreotide weight (~1019 Da) is a known reference value. "
        "Very high credibility for this numerical fact.",
    ),
    analogy_ontology: (
        0.78,
        "A 66-concept ontology with 9 cross-domain edges from a PRISMA-style review is "
        "described as an output of the autonomous agent process. The review process is "
        "described but not independently verifiable. Moderate prior reflecting the "
        "systematic review methodology but absence of expert validation.",
    ),
    analogy_power_law: (
        0.75,
        "Power-law fit α=1.25±0.08, R²=0.71 on a 60-point normalized dataset. The R²=0.71 "
        "itself indicates moderate fit quality, and the dataset normalization introduces "
        "methodological choices. Moderate prior reflecting quantitative evidence with "
        "acknowledged uncertainty (R²=0.71 is not a tight fit).",
    ),
    analogy_degree_sequence: (
        0.80,
        "Identical degree sequence [3,3,3,2,2,1,1] for reduced network graphs is a "
        "combinatorial fact computable from the network representations. The main uncertainty "
        "is whether the network reduction methodology is consistent between domains.",
    ),
    analogy_bayesian: (
        0.77,
        "Bayesian comparison yielding 0.82 posterior probability that exponents differ by <0.5 "
        "is a statistical result from the paper's analysis. The prior model choice in Bayesian "
        "comparison significantly influences the posterior, and no sensitivity analysis is "
        "reported. Moderate prior reflecting the result with methodological uncertainty.",
    ),
    lsystem_claim: (
        0.78,
        "The six-rule L-system grammar is described as executable and pattern-consistent "
        "with observations in both domains. No formal verification of pattern consistency "
        "is reported beyond visual inspection. Moderate prior.",
    ),

    # ─── Hypothesis claims (author-advocated) ───────────────────────────────
    emergent_coordination_claim: (
        0.80,
        "The claim that plannerless coordination is sufficient for multi-agent convergence "
        "is the paper's central thesis, supported by four case studies showing 12-48% "
        "synthesis fractions. Well-supported but relies on a limited set of four demonstrations "
        "without comparison to a centrally-coordinated baseline.",
    ),

    # ─── Competing hypotheses for abduction ─────────────────────────────────
    hypothesis_boron_rich: (
        0.70,
        "The covalent-network hypothesis for boron stiffness is physically well-motivated "
        "(B-C, B-O, B-N bonds are known to be very strong and short). However, the paper "
        "provides no experimental validation, relying solely on DFT computations. "
        "Moderate prior reflecting physical plausibility without experimental confirmation.",
    ),
    alt_boron_rich: (
        0.30,
        "The DFT-artifact hypothesis (overbinding inflates moduli) is a known limitation "
        "of DFT for short-bond covalent systems, but the systematic nature of the anomaly "
        "(all boron-rich phases, not random scatter) is harder to explain by computational "
        "artifact alone. Lower prior reflecting that the artifact explanation is less "
        "parsimonious than the covalent-network hypothesis.",
    ),
    pred_covalent: (
        0.72,
        "The prediction that boron-rich ceramics will show high specific stiffness "
        "consistently across computational and experimental datasets is plausible given "
        "the physical mechanism, but no experimental cross-check is presented in the paper. "
        "Moderate prior.",
    ),
    pred_artifact: (
        0.28,
        "The prediction that anomalous stiffness disappears with experimental validation "
        "is the null hypothesis for the DFT artifact explanation. Given that B₄C is a "
        "well-characterized superhard material experimentally, this prediction is likely "
        "to fail, hence low prior.",
    ),

    # ─── Alternative claims used in contradiction operator ──────────────────
    central_coordination_necessary: (
        0.20,
        "Prior probability that central coordination is strictly necessary for multi-agent "
        "convergence. The ScienceClaw results plus broader multi-agent systems literature "
        "suggest emergent coordination is generally sufficient for loosely-coupled tasks. "
        "Low prior reflecting that the paper's demonstration directly contradicts this claim.",
    ),
}
