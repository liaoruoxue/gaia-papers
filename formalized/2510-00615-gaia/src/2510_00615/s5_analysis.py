"""Section 4.5: Analysis & ablation studies (thresholds, prompt optimiser
choice, contrastive feedback)."""

from gaia.lang import claim, setting, support

from .s3_method import textual_gradient_step, ut_step, co_step

# Threshold ablation ---------------------------------------------------------

threshold_ablation_data = claim(
    "On AppWorld with gpt-4.1, varying the compression thresholds yields a "
    "U-shaped trade-off (Figure 6):\n\n"
    "- **History thresholds** scanned: $T_{hist} \\in \\{2048, 4096, 8192\\}$.\n"
    "- **Observation thresholds** scanned: $T_{obs} \\in \\{512, 1024, 2048\\}$.\n\n"
    "Smaller thresholds reduce tokens but trigger many more compression calls "
    "and degrade accuracy; larger thresholds preserve accuracy but with higher "
    "peak tokens. The Figure-6 right panel shows accuracy peaking around "
    "$T_{hist}=4096$ and $T_{obs}=1024$ (both close to the No-compression "
    "accuracy line) at substantially lower peak tokens than No-compression.",
    title="Threshold ablation: moderate values give the best trade-off",
    metadata={"figure": "artifacts/2510.00615.pdf, Figure 6"},
)

threshold_recommendation = claim(
    "**Moderate thresholds** ($T_{hist}=4096$, $T_{obs}=1024$) are recommended "
    "as the best accuracy/efficiency trade-off on AppWorld with gpt-4.1.",
    title="Recommended thresholds",
)

reason_threshold = (
    "@threshold_ablation_data shows a clear U-shape in the accuracy/peak-token "
    "plane: extreme thresholds either over-compress (accuracy collapse) or "
    "under-compress (peak tokens unchanged from No-compression). The 4096/1024 "
    "configuration sits at the elbow on AppWorld, justifying it as the default "
    "@threshold_recommendation."
)

strat_threshold = support(
    [threshold_ablation_data],
    threshold_recommendation,
    reason=reason_threshold,
    prior=0.85,
)

# Prompt-optimiser ablation --------------------------------------------------

optimizer_ablation_data = claim(
    "Ablation on the prompt-optimiser model and feedback type (AppWorld, gpt-4.1 "
    "agent + history compressor, Table 3):\n\n"
    "| Optimiser | Task contrastive feedback? | Average Acc. |\n"
    "|-----------|:--------------------------:|-------------:|\n"
    "| o3 | yes | **51.2** |\n"
    "| o3 | no | 50.6 (-0.6) |\n"
    "| gpt-4.1 | yes | 47.6 (-3.6) |\n"
    "| gpt-5 | yes | 50.6 (-0.6) |\n",
    title="Prompt-optimiser ablation",
    metadata={"source_table": "artifacts/2510.00615.pdf, Table 3"},
)

contrastive_feedback_helps = claim(
    "Using **contrastive task feedback** (comparing successful uncompressed and "
    "failed compressed trajectories) gives a small but consistent gain over "
    "using failed trajectories alone (51.2 vs 50.6 with the o3 optimiser).",
    title="Contrastive feedback helps marginally",
)

reason_contrastive_helps = (
    "The o3-with-contrastive vs o3-without-contrastive comparison "
    "(@optimizer_ablation_data) isolates the effect of the contrastive signal "
    "from optimiser strength: the +0.6 absolute accuracy gain confirms the "
    "importance of the contrastive design choice motivated in Section 3.3, even "
    "if the gap is modest. This reinforces the textual-gradient mechanism "
    "@textual_gradient_step."
)

strat_contrastive_helps = support(
    [optimizer_ablation_data, textual_gradient_step],
    contrastive_feedback_helps,
    reason=reason_contrastive_helps,
    prior=0.7,
)

strong_optimizer_matters = claim(
    "Optimiser strength has a much larger effect on guideline quality than "
    "the contrastive feedback ablation: switching from o3 to gpt-4.1 as the "
    "optimiser drops accuracy by 3.6 points (51.2 -> 47.6), while switching to "
    "gpt-5 drops it by only 0.6.",
    title="Optimiser strength dominates final accuracy",
)

reason_strong_optimizer = (
    "From @optimizer_ablation_data, the largest accuracy gap (3.6 points) is "
    "between o3 and gpt-4.1 with everything else held fixed; the contrastive "
    "feedback toggle moves accuracy by only 0.6 points. Hence stronger reasoning "
    "models produce better natural-language gradients, dominating the gain from "
    "the contrastive feedback design alone."
)

strat_strong_optimizer = support(
    [optimizer_ablation_data],
    strong_optimizer_matters,
    reason=reason_strong_optimizer,
    prior=0.85,
)

# UT vs CO behavioural claim -------------------------------------------------

ut_co_behaviour = claim(
    "Across benchmarks, the UT step alone improves accuracy while reducing "
    "tokens, whereas the CO step further lowers tokens but typically costs a "
    "small amount of accuracy — except on AppWorld where adding CO yields "
    "additional accuracy gains (e.g. ACON-UT 51.2 -> ACON-UTCO 56.5 in "
    "history compression).",
    title="UT vs CO behaviour across benchmarks",
)

reason_ut_co = (
    "UT @ut_step targets the reward term of the bi-objective and should "
    "preserve or improve accuracy; CO @co_step targets the cost term and is "
    "expected to occasionally trade a small amount of accuracy for further "
    "compression. The exception on AppWorld likely reflects that, on heavy-tail "
    "histories, removing extraneous tokens via CO further declutters the "
    "context — which (per @threshold_ablation_data) can *also* improve accuracy "
    "via reduced distraction."
)

strat_ut_co = support(
    [threshold_ablation_data],
    ut_co_behaviour,
    background=[ut_step, co_step],
    reason=reason_ut_co,
    prior=0.8,
)

__all__ = [
    "threshold_ablation_data",
    "threshold_recommendation",
    "optimizer_ablation_data",
    "contrastive_feedback_helps",
    "strong_optimizer_matters",
    "ut_co_behaviour",
]
