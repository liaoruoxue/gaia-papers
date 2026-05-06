"""Section 5.1: Empirical analysis of the Wasserstein signal.

Section 5.1 of [@Chen2026SHEAR]. The diagnostic in Section 2 motivates
the method qualitatively; Section 5.1 directly evaluates whether the
Wasserstein distance can *discriminate between correct and incorrect
reasoning* at finite-sample sizes -- the property that the separation
theorem (Section 4) predicts conditionally.

Key result (Figure 3): the AUC between correct and incorrect spans
*increases monotonically* with the Wasserstein distance magnitude,
rising from approximately 0.65 at low W-distances to 0.988 at the
highest bin -- providing concrete empirical support for the condition
D(S) > 2 eta(n,d) required by Theorem 1.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup (extends Section 2 setup with ground-truth labels)
# ---------------------------------------------------------------------------

setup_section51_protocol = setting(
    "**Section 5.1 protocol (extends Section 2 setup).** Same prefix-"
    "completion protocol as Section 2 (MATH500 + Qwen2.5-Math-7B; "
    "$G = 8$ rollouts; $w = 100$, $s = 25$ sliding window; final-"
    "answer spans excluded), with one key difference: whereas Section "
    "2 analyzed correlation between Wasserstein distance and "
    "*empirical* continuation accuracy as a motivating observation, "
    "Section 5.1 *additionally leverages the ground-truth correctness "
    "labels of the original rollouts* to directly evaluate whether "
    "Wasserstein distance discriminates correct from incorrect spans "
    "-- the property the separation theorem predicts. This yields "
    "23,704 spans from originally correct rollouts and 21,352 from "
    "originally incorrect rollouts.",
    title="Setup: 23,704 correct + 21,352 incorrect spans on MATH500",
)

# ---------------------------------------------------------------------------
# Within-bin discrimination + AUC
# ---------------------------------------------------------------------------

claim_fig3_topleft_within_bin_separation = claim(
    "**Figure 3 (top-left): within every Wasserstein-distance bin, "
    "originally-correct spans achieve higher empirical accuracy than "
    "originally-incorrect spans.** Each span is plotted as a dot "
    "showing its $W$ to the opposing group vs. its empirical "
    "continuation accuracy $n/16$. Green dots (originally correct) and "
    "red dots (originally incorrect) are stratified: within every "
    "$W$ bin, green dots sit above red dots in accuracy, confirming "
    "that ground-truth correctness information *persists through "
    "truncation and resampling*. More importantly, *higher* $W$ is "
    "systematically associated with *lower* accuracy in *both* "
    "groups, extending the anti-correlation of Section 2 to a "
    "setting conditioned on the original outcome.",
    title="Fig 3 top-left: per-bin green > red; higher $W$ -> lower accuracy in both groups",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 3, top-left",
    },
)

claim_fig3_auc_monotonic = claim(
    "**Figure 3 (right): AUC between correct vs. incorrect spans "
    "increases monotonically with $W$-magnitude.** The per-bin AUC "
    "values are:\n\n"
    "| $W$-distance bin | AUC |\n"
    "| --- | --- |\n"
    "| (0.199, 0.363] | 0.644 |\n"
    "| (0.363, 0.525] | 0.720 |\n"
    "| (0.525, 0.688] | 0.888 |\n"
    "| (0.688, 0.85] | 0.938 |\n"
    "| (0.85, 1.013] | 0.946 |\n"
    "| (1.013, 1.175] | 0.958 |\n"
    "| (1.175, 1.338] | 0.970 |\n"
    "| (1.338, 1.5] | 0.988 |\n\n"
    "AUC rises from $\\approx 0.65$ at low $W$ to $\\approx 0.99$ at "
    "high $W$. The per-bin density plots (Figure 3 bottom) visualize "
    "the transition: at low $W$ the accuracy distributions of correct "
    "vs. incorrect spans overlap almost entirely; at high $W$ they "
    "are well-separated.",
    title="Fig 3 right: AUC monotonic 0.644 -> 0.988 across $W$ bins",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 3, right + bottom row",
        "bin_count": "8 bins from (0.199, 0.363] to (1.338, 1.5]",
    },
)

claim_thm1_condition_verified = claim(
    "**Empirical verification of the separation condition $D(S) > "
    "2\\eta(n, d)$.** The monotonic AUC growth in Figure 3 (right) is "
    "the empirical analog of the population-level inequality $D(S) > "
    "2\\eta(n, d)$ in Theorem 1: as $W$ increases, the population-"
    "level distributional gap exceeds the finite-sample noise floor "
    "by a *widening margin*, so the discrimination becomes near-"
    "perfect. This is the converse direction of the theorem: the "
    "theorem says 'if $D > 2\\eta$ then strict separation'; the "
    "empirics confirm 'where strict separation is observed, $D$ "
    "indeed exceeds $2\\eta$ by a meaningful margin'. Together, the "
    "theory provides the mechanism and the experiment provides the "
    "verification.",
    title="Sec 5.1 -> Theorem 1: empirical $D(S) > 2\\eta(n,d)$ verified by monotonic AUC",
)

claim_signal_finite_sample_practical = claim(
    "**The theoretical separation manifests at *finite sample sizes* "
    "with practical discriminative power.** AUC of 0.99 at the highest "
    "$W$ bin means the Wasserstein-distance signal is not merely a "
    "limiting / asymptotic guarantee but is *operational* at the "
    "training-time sample sizes used in Algorithm 1. Since the "
    "discriminative power is derived *entirely* from the model's own "
    "hidden states, this validates the use of Wasserstein distance "
    "as a principled token-level weight in the GRPO objective "
    "without step-level annotations or an external reward model -- "
    "the headline closing argument of Section 5.1.",
    title="Sec 5.1 conclusion: $W$-signal is operational at training-time sample sizes (AUC up to 0.99)",
)

__all__ = [
    "setup_section51_protocol",
    "claim_fig3_topleft_within_bin_separation",
    "claim_fig3_auc_monotonic",
    "claim_thm1_condition_verified",
    "claim_signal_finite_sample_practical",
]
