"""Section 5.4-5.6 + 6: Ablations and computational overhead.

Section 5.4-5.6 of [@Chen2026SHEAR]. Three ablation axes:

* 5.4.1 -- Distance metric (Wasserstein, Chamfer, MMD, Cosine).
  Wasserstein peak 0.5068; Chamfer 0.5051; MMD 0.5061; Cosine 0.4837
  (BELOW GRPO baseline 0.4884).
* 5.4.2 -- Cross-rollout vs. per-rollout normalization. Cross-rollout
  (default) 0.5068; per-rollout 0.4995. Both above GRPO 0.4884.
* 5.5 -- Span length w in {80, 100, 120} and stride s. Insensitive to
  span length; sensitive to stride (smaller stride -> better).
* 5.6 -- Rollout group size G in {8, 16}. Both improve with larger G;
  SHEAR's gap over GRPO widens at G=16.

Section 6 -- Computational overhead. SHEAR adds 15.5% on
Qwen2.5-Math-7B, 10.4% on Llama3.1-8B-Instruct, 7.4% on
Qwen2.5-14B-Base. Overhead decreases with model scale (Sinkhorn cost
is fixed-size; forward/backward grows with model).
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 5.4.1 -- Distance metric ablation
# ---------------------------------------------------------------------------

claim_5_4_1_distance_metric_ablation = claim(
    "**Section 5.4.1 -- distance metric ablation on Qwen2.5-Math-7B "
    "(peak benchmark-averaged accuracy across 5 math benchmarks).** "
    "Replace Sinkhorn-approximated $W_1$ with three alternatives that "
    "differ in distributional information retained:\n\n"
    "| Variant | Peak Accuracy | Note |\n"
    "| --- | --- | --- |\n"
    "| GRPO (Baseline) | 0.4884 | reference |\n"
    "| **SHEAR (Wasserstein)** | **0.5068** | full transport metric |\n"
    "| SHEAR (Chamfer) | 0.5051 | point-cloud, not proper transport |\n"
    "| SHEAR (MMD, RBF) | 0.5061 | kernel embedding, all moments |\n"
    "| SHEAR (Cosine) | 0.4837 | mean-shift only, BELOW GRPO |\n\n"
    "Wasserstein, Chamfer, and MMD form a *top tier* with peak "
    "accuracies above the GRPO baseline. Wasserstein achieves the "
    "highest peak; the margin over Chamfer and MMD is small. Cosine "
    "actively HURTS LEARNING (plateaus 0.4837 vs. GRPO 0.4884 "
    "throughout the latter half of training).",
    title="Sec 5.4.1: Wasserstein 0.5068 > Chamfer 0.5051 / MMD 0.5061 > GRPO 0.4884 > Cosine 0.4837",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 5(a)",
    },
)

claim_5_4_1_distributional_signal_richer = claim(
    "**Sec 5.4.1 implication: distribution-aware metrics succeed; "
    "mean-only metrics fail.** Wasserstein, Chamfer, and MMD all "
    "capture distributional structure beyond first-moment shift; "
    "they all beat GRPO. Cosine captures *only* angular separation "
    "between span means -- a pure mean-shift, direction-only signal "
    "-- and falls *below* GRPO. Empirically, mean-direction shifts "
    "in hidden states are *not a faithful proxy* for reasoning "
    "quality; they correlate with surface-level lexical variation "
    "and other reasoning-irrelevant factors, and weighting tokens "
    "by such a signal *injects noise* into the policy gradient. The "
    "fact that the three distribution-aware metrics succeed where "
    "the mean-only metric fails directly supports the central claim "
    "of Section 4: capturing the *full distributional difference*, "
    "rather than a low-order summary, is what makes hidden states a "
    "reliable source of process-level credit.",
    title="Sec 5.4.1 -> Section 4: distribution-aware metrics work; mean-only Cosine fails (predicted by Prop D.1)",
)

# ---------------------------------------------------------------------------
# 5.4.2 -- Cross-rollout vs. per-rollout normalization
# ---------------------------------------------------------------------------

claim_5_4_2_cross_vs_per_rollout = claim(
    "**Section 5.4.2 -- cross-rollout vs. per-rollout normalization "
    "on Qwen2.5-Math-7B.**\n\n"
    "| Variant | Peak Accuracy |\n"
    "| --- | --- |\n"
    "| GRPO (Baseline) | 0.4884 |\n"
    "| **SHEAR (Cross-rollout, default)** | **0.5068** |\n"
    "| SHEAR (Per-rollout) | 0.4995 |\n\n"
    "Cross-rollout: span distances divided by the *global* mean "
    "hidden-state norm $\\bar n$ (allows different rollouts to "
    "receive different total gradient magnitudes). Per-rollout: each "
    "rollout's distances rescaled by a *per-rollout* normalizer "
    "(equalizes the average weight magnitude across rollouts within "
    "a group; explicitly removes any cross-rollout reweighting). "
    "Both variants substantially outperform GRPO; the default "
    "retains a measurable +0.7-pt edge.",
    title="Sec 5.4.2: cross-rollout 0.5068 > per-rollout 0.4995 > GRPO 0.4884; both above baseline",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 5(b)",
    },
)

claim_5_4_2_within_rollout_dominates = claim(
    "**Sec 5.4.2 implication: the within-rollout token-level signal "
    "is the dominant source of improvement.** Even after explicitly "
    "equalizing per-rollout weight magnitudes, SHEAR (per-rollout) "
    "*still* improves over GRPO by a comfortable margin (+1.1 pts). "
    "The method's effectiveness does not hinge on cross-rollout "
    "magnitude differences -- the *per-token ranking of credit* "
    "within a rollout, which the separation theorem in Section 4 "
    "directly addresses, is what carries the learning signal. "
    "Cross-rollout magnitude variation provides a *complementary* "
    "(but small) bonus by allowing rollouts with larger absolute "
    "distributional gaps to receive proportionally larger total "
    "gradient mass.",
    title="Sec 5.4.2 -> Section 4: within-rollout per-token ranking carries the signal (theorem-aligned)",
)

# ---------------------------------------------------------------------------
# 5.5 -- Span length and stride
# ---------------------------------------------------------------------------

claim_5_5_span_stride_sensitivity = claim(
    "**Section 5.5 -- span length $w$ and stride $s$ on Qwen2.5-"
    "Math-7B.** Two patterns from Figure 6: (i) **Performance is "
    "*relatively insensitive* to span length** -- for fixed stride, "
    "varying $w$ from 80 to 120 produces only marginal differences in "
    "final accuracy, indicating the Wasserstein signal is robust "
    "across a range of local window sizes. (ii) **Performance is "
    "*more sensitive* to stride size** -- within each span length, "
    "smaller strides consistently yield higher and more stable "
    "accuracy curves (e.g. at $w = 100$, $s = 25$ outperforms $s = "
    "75$ throughout training). A smaller stride increases overlap "
    "between consecutive spans, providing finer-grained coverage of "
    "the reasoning chain and reducing the risk that a localized "
    "divergence event falls between non-overlapping windows. Default "
    "$w = 100$, $s = 25$ adopted in all main experiments.",
    title="Sec 5.5: insensitive to $w \\in \\{80,100,120\\}$; sensitive to $s$ (smaller better)",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 6",
    },
)

# ---------------------------------------------------------------------------
# 5.6 -- Rollout group size
# ---------------------------------------------------------------------------

claim_5_6_rollout_group_size = claim(
    "**Section 5.6 -- rollout group size $G \\in \\{8, 16\\}$ on "
    "Qwen2.5-Math-7B.** Two observations from Figure 7: (i) increasing "
    "$G$ from 8 to 16 *improves both methods*, confirming that larger "
    "rollout groups provide richer contrastive signal for credit "
    "assignment. (ii) **The gap between SHEAR and GRPO *widens* at $G "
    "= 16$**: SHEAR ($G = 16$) achieves the highest final accuracy "
    "among all four configurations, while GRPO ($G = 16$) plateaus "
    "*below* SHEAR ($G = 8$) in late training. This suggests SHEAR "
    "*benefits more* from additional rollouts than standard GRPO, "
    "likely because a larger opposing set yields more reliable span-"
    "level Wasserstein estimates, amplifying the advantage of fine-"
    "grained credit assignment.",
    title="Sec 5.6: SHEAR-GRPO gap WIDENS at G=16 -> richer opposing set yields better $W$ estimates",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 7",
    },
)

# ---------------------------------------------------------------------------
# Section 6 -- Computational overhead
# ---------------------------------------------------------------------------

claim_section6_overhead = claim(
    "**Section 6 -- computational overhead (Figure 8).**\n\n"
    "| Backbone | SHEAR overhead vs. GRPO |\n"
    "| --- | --- |\n"
    "| Qwen2.5-Math-7B | +15.5% |\n"
    "| Llama3.1-8B-Instruct | +10.4% |\n"
    "| Qwen2.5-14B-Base | +7.4% |\n\n"
    "**The overhead *decreases* with model scale.** Sinkhorn "
    "computation operates on *fixed-size* spans regardless of model "
    "dimension, while the dominant cost of forward/backward passes "
    "*grows* with model size. In all cases, overhead remains below "
    "16%, making SHEAR practical for standard RLVR training pipelines.",
    title="Sec 6: 7.4-15.5% overhead; decreases with model scale (Sinkhorn fixed-cost)",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 8",
    },
)

__all__ = [
    "claim_5_4_1_distance_metric_ablation",
    "claim_5_4_1_distributional_signal_richer",
    "claim_5_4_2_cross_vs_per_rollout",
    "claim_5_4_2_within_rollout_dominates",
    "claim_5_5_span_stride_sensitivity",
    "claim_5_6_rollout_group_size",
    "claim_section6_overhead",
]
