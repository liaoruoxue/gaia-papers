"""Section 7 / Appendix A: Experimental setup and ablation evaluation.

The paper's experiments are spread across Sections 4 (anomaly evidence),
6.1 (ablation), 6.2 (parallel form). Appendix A documents the underlying
setup -- backbones, datasets, training compute -- which this module
records as settings. Section 7 (Conclusion) provides the high-level
empirical synthesis.

Two empirical generalizations are also drawn here:
* Induction across three task families (LLM, NVS, image classification)
  shows the linear-attention re-framing is task-general.
* Induction across the four anomalies shows the memorization-view
  failure is systematic.
"""

from gaia.lang import claim, setting, support, induction

from .motivation import (
    claim_contribution_anomalies,
    claim_contribution_equivalence,
    claim_contribution_practical,
)
from .s4_anomalies import (
    claim_anomaly_inner_vs_outer,
    claim_anomaly_gradient_ascent,
    claim_anomaly_distributional_asymmetry,
    claim_anomaly_replace_q_with_k,
    claim_memorization_view_falsified,
)
from .s5_linear_attention_equivalence import (
    claim_thm_5_1,
    claim_thm_5_2,
    claim_thm_5_3,
    claim_ttt_is_linear_attention,
    claim_lact_in_la_form,
    claim_vittt_in_la_form,
)
from .s6_simplifications_and_parallelization import (
    claim_simplifications_preserve_performance,
    claim_parallel_form_speedup,
    obs_ablation_table2,
    obs_variant1_best,
    obs_variant6_minor_degradation,
    obs_parallel_throughput,
    obs_parallel_end_to_end_speedup,
)

# ---------------------------------------------------------------------------
# Appendix A: experimental setup (settings)
# ---------------------------------------------------------------------------

setup_lact_llm_setup = setting(
    "**LaCT-LLM experimental setup (Appendix A, LM).** Baseline is the "
    "**760M-parameter LaCT-LLM** [@Zhang2025]. Trained on **100B tokens** "
    "from the FineWeb-Edu dataset [@Penedo2024] with batch size 4 per "
    "GPU across 8 NVIDIA A100 GPUs for 20K iterations (~56 hours). "
    "Hyperparameters follow the original LaCT [@Zhang2025] configuration. "
    "Evaluation: perplexity on **2.5B tokens** from the Book-3 dataset "
    "[@Gao2020]. All implementations build on Flame [@ZhangFlame2025].",
    title="Setup: LaCT-LLM 760M, 100B tokens FineWeb-Edu, eval on 2.5B Book-3 tokens",
)

setup_lact_nvs_setup = setting(
    "**LaCT-NVS experimental setup (Appendix A, NVS).** Baseline is a "
    "**12-layer 768-hidden-dim LaCT-NVS** model (~114M parameters) "
    "[@Zhang2025]. Trained on RealEstate10K [@Zhou2018] with batch size "
    "128 per GPU on 4 NVIDIA A100 GPUs for 20K iterations (~38 hours). "
    "Training uses 2 input + 6 target views; evaluation uses 2 input + "
    "3 target views. All images resized to $128 \\times 128$. Loss is "
    "MSE; metric is **Peak Signal-to-Noise Ratio (PSNR)**.",
    title="Setup: LaCT-NVS 12-layer 768d ~114M params, RealEstate10K 128px, MSE / PSNR",
)

setup_vittt_setup = setting(
    "**ViTTT-B experimental setup (Appendix A, image classification).** "
    "Baseline is **ViTTT-B** [@Han2025], a vision transformer with TTT "
    "layers, ~90M parameters. Trained on ImageNet-1K [@Deng2009] with "
    "batch size 256 per GPU on 2 NVIDIA H100 GPUs for 60 epochs (~16 "
    "hours). Evaluation: top-1 accuracy on the ImageNet-1K validation "
    "set. Hyperparameters follow the original ViTTT [@Han2025] "
    "configuration.",
    title="Setup: ViTTT-B ~90M params, ImageNet-1K 60 epochs, top-1 accuracy",
)

# ---------------------------------------------------------------------------
# Three-task induction: anomalies (Sec. 4) generalize across task families
# ---------------------------------------------------------------------------

# Per-task-family observations of the anomaly. Each is "the anomaly law
# (memorization view fails) predicts behaviour on the task; behaviour is
# observed". For the induction we treat each task-family as an independent
# realization of the anomaly law.

claim_anomalies_hold_lact_llm = claim(
    "**Per-task observation (LaCT-LLM).** All four anomalies hold on "
    "the LaCT-LLM language-modeling task: gradient ascent matches "
    "baseline (16.43 vs 16.19 perplexity, Table 1); replacing Q with K "
    "matches baseline (16.43 vs 16.18 perplexity, Table 1); inner-loss "
    "vs perplexity is monotone-inverse over 1-64 inner steps (Fig. 1, "
    "perplexity panel); the Q-K distribution mismatch and inner-loss / "
    "performance inverse relationship are observed in the same model "
    "family.",
    title="Per-task observation: all four anomalies hold on LaCT-LLM",
    background=[setup_lact_llm_setup],
    metadata={"source": "artifacts/2602.21204.pdf, Sec. 4 (Table 1, Fig. 1, Fig. 2)"},
)

claim_anomalies_hold_lact_nvs = claim(
    "**Per-task observation (LaCT-NVS).** All four anomalies hold on "
    "the LaCT-NVS novel-view-synthesis task: gradient ascent matches "
    "baseline (25.94 vs 25.85 dB PSNR, Table 1); replacing Q with K "
    "matches baseline (25.94 vs 25.95 dB PSNR, Table 1); inner-loss vs "
    "PSNR is monotone-inverse over 1-64 inner steps (Fig. 1, PSNR panel "
    "drops from 26 dB to 18 dB); Q-K distribution mismatch is "
    "explicitly visualized for this model in Fig. 2.",
    title="Per-task observation: all four anomalies hold on LaCT-NVS (Q-K mismatch directly visualized here)",
    background=[setup_lact_nvs_setup],
    metadata={"source": "artifacts/2602.21204.pdf, Sec. 4 (Table 1, Fig. 1, Fig. 2)"},
)

claim_anomalies_hold_vittt = claim(
    "**Per-task observation (ViTTT-B).** Anomalies 2 and 4 hold "
    "directly on the ViTTT-B image-classification task: gradient ascent "
    "matches baseline (79.34% vs 79.61% Top-1, Table 1); replacing Q "
    "with K matches baseline (79.34% vs 79.18% Top-1, Table 1). "
    "Anomalies 1 and 3 are not separately reported on ViTTT in Section "
    "4 but the linear-attention reduction (@claim_vittt_in_la_form) "
    "predicts they would also hold.",
    title="Per-task observation: anomalies 2 and 4 hold on ViTTT-B (Anomalies 1, 3 not separately tested)",
    background=[setup_vittt_setup],
    metadata={"source": "artifacts/2602.21204.pdf, Sec. 4 (Table 1)"},
)

claim_anomalies_general_law = claim(
    "**Generalization claim (induction over task families).** The "
    "anomalies that contradict the memorization-based interpretation "
    "of TTT-KVB (@claim_memorization_view_falsified) are not artifacts "
    "of a single architecture or task: they hold across **all three** "
    "evaluated task families -- language modeling (LaCT-LLM, "
    "@claim_anomalies_hold_lact_llm), novel-view synthesis (LaCT-NVS, "
    "@claim_anomalies_hold_lact_nvs), and image classification "
    "(ViTTT-B, @claim_anomalies_hold_vittt). The cross-domain "
    "consistency rules out the possibility that the anomalies are due "
    "to peculiarities of any one regime.",
    title="Generalization: memorization view fails consistently across LLM, NVS, image classification",
)

# ---------------------------------------------------------------------------
# Three-task induction: simplification + parallelization (Sec. 6) generalize
# ---------------------------------------------------------------------------

claim_ablation_holds_lact_llm = claim(
    "**Per-task ablation (LaCT-LLM).** The six-step ablation reduces "
    "LaCT-LLM perplexity from baseline 16.43 to Variant 6 16.80 (+0.4) "
    "while increasing TTT-layer throughput from 4.30M to 124.6M "
    "tokens/sec (~29x, of which ~4x is the parallel-form gain). "
    "Variant 1 (only update last layer) achieves 15.93 perplexity -- "
    "the *best* across the trajectory.",
    title="Per-task ablation: LaCT-LLM degrades by only +0.4 perplexity across the full reduction",
    background=[setup_lact_llm_setup],
    metadata={"source_table": "artifacts/2602.21204.pdf, Table 2 (LaCT-LLM column)"},
)

claim_ablation_holds_lact_nvs = claim(
    "**Per-task ablation (LaCT-NVS).** The six-step ablation reduces "
    "LaCT-NVS PSNR from baseline 25.94 to Variant 6 25.73 dB (-0.2 dB) "
    "while preserving the linear-attention reduction. Step 3 (collapse "
    "MLP) is the costliest step on NVS: PSNR drops from 25.93 to 25.71 "
    "dB. Variant 1 achieves 25.97 dB, slightly above baseline.",
    title="Per-task ablation: LaCT-NVS degrades by only -0.2 dB PSNR across the full reduction",
    background=[setup_lact_nvs_setup],
    metadata={"source_table": "artifacts/2602.21204.pdf, Table 2 (LaCT-NVS column)"},
)

claim_ablation_holds_vittt = claim(
    "**Per-task ablation (ViTTT-B).** The six-step ablation moves ViTTT "
    "Top-1 accuracy from baseline 79.34% to Variant 6 79.54% (+0.2%) -- "
    "the simplified (= standard linear attention) variant matches or "
    "slightly *exceeds* the baseline. Variant 1 (79.63%) is the best in "
    "the trajectory.",
    title="Per-task ablation: ViTTT-B Top-1 +0.2% across the full reduction (simplified beats baseline)",
    background=[setup_vittt_setup],
    metadata={"source_table": "artifacts/2602.21204.pdf, Table 2 (ViTTT column)"},
)

claim_ablation_general_law = claim(
    "**Generalization claim (induction over task families).** The "
    "result that complex TTT design components are largely redundant "
    "(@claim_simplifications_preserve_performance) is corroborated on "
    "*all three* evaluated task families: LaCT-LLM "
    "(@claim_ablation_holds_lact_llm), LaCT-NVS "
    "(@claim_ablation_holds_lact_nvs), and ViTTT-B "
    "(@claim_ablation_holds_vittt). The *direction* of degradation "
    "(within ~1% relative on the natural metric) and the *finding that "
    "Variant 1 is best* are common across all three settings.",
    title="Generalization: ablation reduction holds across LLM, NVS, image classification",
)

# ---------------------------------------------------------------------------
# Section 7 (Conclusion) -- limitation acknowledgement
# ---------------------------------------------------------------------------

setup_scope_limitation = setting(
    "**Acknowledged scope limitation (Sec. 7).** All theoretical "
    "results in Sections 5-6 are derived under the structural "
    "assumption that the inner-loop final layer is *linear and bias-"
    "free*. Extending these insights to *non-linear final layers*, and "
    "exploring deeper connections between TTT and modern linear "
    "attention mechanisms in both directions, are explicitly identified "
    "by the authors as future work.",
    title="Acknowledged scope limitation: theory restricted to linear bias-free final layer",
)

# ---------------------------------------------------------------------------
# Pass 2: induction across task families
# ---------------------------------------------------------------------------

# Anomaly induction: the law (memorization view fails) predicts that the
# four anomalies hold on each task family. Confirmation across all three
# task families inductively boosts the law.
sup_anomalies_lact_llm = support(
    [claim_memorization_view_falsified],
    claim_anomalies_hold_lact_llm,
    reason=(
        "If the memorization view truly fails for TTT-KVB "
        "(@claim_memorization_view_falsified), it should fail on every "
        "concrete TTT-KVB instance -- including LaCT-LLM. The "
        "per-task observation (@claim_anomalies_hold_lact_llm) confirms "
        "this prediction on the language-modeling family."
    ),
    prior=0.93,
    background=[setup_lact_llm_setup],
)

sup_anomalies_lact_nvs = support(
    [claim_memorization_view_falsified],
    claim_anomalies_hold_lact_nvs,
    reason=(
        "Same prediction as @sup_anomalies_lact_llm but for the "
        "novel-view-synthesis task family on LaCT-NVS. The Q-K mismatch "
        "of Anomaly 1 is *directly* visualized on LaCT-NVS (Fig. 2), "
        "providing the cleanest single-task confirmation of the "
        "law."
    ),
    prior=0.95,
    background=[setup_lact_nvs_setup],
)

sup_anomalies_vittt = support(
    [claim_memorization_view_falsified],
    claim_anomalies_hold_vittt,
    reason=(
        "Same prediction extended to ViTTT-B on the image-classification "
        "task family. Only Anomalies 2 (Q->K) and 4 (gradient ascent) "
        "are tested directly here; the law's explanatory coverage of "
        "ViTTT remains partial but consistent."
    ),
    prior=0.85,  # weaker because only 2 of 4 anomalies tested on ViTTT
    background=[setup_vittt_setup],
)

# Build induction chain: each support is law -> per-task observation.
ind_anomalies_12 = induction(
    sup_anomalies_lact_llm,
    sup_anomalies_lact_nvs,
    law=claim_memorization_view_falsified,
    reason=(
        "Two independent task families (language modeling on LaCT-LLM "
        "@sup_anomalies_lact_llm, novel-view synthesis on LaCT-NVS "
        "@sup_anomalies_lact_nvs) -- different model sizes (760M vs "
        "114M), different data domains (text vs images), different "
        "metrics (perplexity vs PSNR) -- both confirm the law that the "
        "memorization interpretation fails."
    ),
)

ind_anomalies_123 = induction(
    ind_anomalies_12,
    sup_anomalies_vittt,
    law=claim_memorization_view_falsified,
    reason=(
        "Adding the third independent task family (image classification "
        "on ViTTT-B, @sup_anomalies_vittt) -- a *different architecture* "
        "(ViTTT vs LaCT) and yet another task domain -- further "
        "strengthens the inductive case. The cross-architecture "
        "generalization is the strongest evidence against an "
        "architecture-specific explanation of the anomalies."
    ),
)

# Anomaly generalization claim is the law; the induction targets it.
strat_anomalies_general = support(
    [claim_memorization_view_falsified],
    claim_anomalies_general_law,
    reason=(
        "The generalization claim (@claim_anomalies_general_law) is the "
        "task-general restatement of the law (@claim_memorization_view_falsified) "
        "supported by the three-task induction (@ind_anomalies_123)."
    ),
    prior=0.93,
)

# Ablation induction: same structure for the simplification result.
sup_ablation_lact_llm = support(
    [claim_simplifications_preserve_performance],
    claim_ablation_holds_lact_llm,
    reason=(
        "The general claim that LA-driven simplifications preserve "
        "performance (@claim_simplifications_preserve_performance) "
        "predicts that the per-task ablation trajectory should be "
        "near-flat on LaCT-LLM. The observed +0.4 perplexity drift "
        "across all six steps (@claim_ablation_holds_lact_llm) "
        "confirms this on the language-modeling task."
    ),
    prior=0.95,
    background=[setup_lact_llm_setup],
)

sup_ablation_lact_nvs = support(
    [claim_simplifications_preserve_performance],
    claim_ablation_holds_lact_nvs,
    reason=(
        "Same prediction extended to LaCT-NVS. The observed -0.2 dB "
        "PSNR drift across all six steps (@claim_ablation_holds_lact_nvs) "
        "confirms the law on novel-view synthesis. Step 3 "
        "(MLP collapse) is the costliest single step here, consistent "
        "with the spatial-reasoning demands of NVS."
    ),
    prior=0.95,
    background=[setup_lact_nvs_setup],
)

sup_ablation_vittt = support(
    [claim_simplifications_preserve_performance],
    claim_ablation_holds_vittt,
    reason=(
        "Extension to image classification on ViTTT-B. Variant 6 "
        "(standard LA) is +0.2% above baseline "
        "(@claim_ablation_holds_vittt) -- the simplified architecture "
        "*matches or exceeds* baseline. This is the strongest "
        "single-task confirmation of the law."
    ),
    prior=0.95,
    background=[setup_vittt_setup],
)

ind_ablation_12 = induction(
    sup_ablation_lact_llm,
    sup_ablation_lact_nvs,
    law=claim_simplifications_preserve_performance,
    reason=(
        "Two task families (LaCT-LLM, LaCT-NVS) with very different "
        "metrics (perplexity vs PSNR) and modalities (text vs images) "
        "both confirm the LA-reduction-preserves-performance law."
    ),
)

ind_ablation_123 = induction(
    ind_ablation_12,
    sup_ablation_vittt,
    law=claim_simplifications_preserve_performance,
    reason=(
        "Adding the cross-architecture ViTTT confirmation strengthens "
        "the inductive case across both task and architecture axes."
    ),
)

# Generalization claim wired off the inductive law.
strat_ablation_general = support(
    [claim_simplifications_preserve_performance],
    claim_ablation_general_law,
    reason=(
        "The generalization claim (@claim_ablation_general_law) is the "
        "task-general restatement of the simplification law "
        "(@claim_simplifications_preserve_performance) supported by the "
        "three-task induction (@ind_ablation_123). Variant 1 being "
        "best across all three task families is the most striking "
        "single-cell pattern repeated in each task."
    ),
    prior=0.93,
)

# Cross-claim contradictions (Pass 2) and synthesis claims wired in s4-s6.
# This module's main job is the multi-task induction.
# ---------------------------------------------------------------------------

__all__ = [
    # Appendix A setups
    "setup_lact_llm_setup",
    "setup_lact_nvs_setup",
    "setup_vittt_setup",
    # Per-task observations of anomalies
    "claim_anomalies_hold_lact_llm",
    "claim_anomalies_hold_lact_nvs",
    "claim_anomalies_hold_vittt",
    "claim_anomalies_general_law",
    # Per-task ablation observations
    "claim_ablation_holds_lact_llm",
    "claim_ablation_holds_lact_nvs",
    "claim_ablation_holds_vittt",
    "claim_ablation_general_law",
    # Limitation
    "setup_scope_limitation",
]
