"""Section 5: How Can Sharpening from Intrinsic URLVR Be Applied Safely?"""

from gaia.lang import claim, setting, support, abduction, compare

from .s3_sharpening import theorem1_sharpening, sharpening_dual_nature
from .s4_rise_and_fall import rise_then_fall_universal, ood_generalization_obs

# ─── Setup ───────────────────────────────────────────────────────────────────

exp_setup_s5 = setting(
    "Section 5 experiments train Qwen3-1.7B-Base using majority voting reward on DAPO-17k subsets "
    "of varying sizes {32, 128, 512, 2048, 8192, 16384}, fixing global batch size to 32 and "
    "adjusting epochs so all settings complete exactly 600 optimization steps. Results for subset "
    "sizes {32, 128, 512} are verified across 3 random seeds. Ground Truth Reward, Majority Voting "
    "Reward, and Reward Accuracy are monitored to detect reward hacking.",
    title="Section 5 experimental setup",
)

# ─── 5.1 Small datasets prevent collapse ─────────────────────────────────────

small_dataset_stability = claim(
    "Training with 32 or 128 samples (DAPO-32, DAPO-128) maintains stable performance without "
    "model collapse throughout 600 optimization steps. Datasets with ≥512 samples consistently "
    "exhibit reward hacking. DAPO-32 achieves rapid majority consensus (Majority Voting Reward → 1) "
    "while preserving high Ground Truth Reward; this holds across all 3 random seeds.",
    title="Small datasets (≤128 samples) prevent model collapse",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 6"},
    background=[exp_setup_s5],
)

kl_divergence_small_vs_large = claim(
    "KL divergence from the reference model $D^{(t)}_{\\mathrm{KL}}(\\pi^{(t)}_\\theta \\| \\pi_{\\mathrm{ref}})$ "
    "is substantially smaller for small training subsets. DAPO-32 reaches only 0.057 KL after "
    "600 steps, while DAPO-512 reaches approximately 2× higher KL at the same point. This "
    "shows small subsets induce far smaller distributional shifts from the reference policy.",
    title="KL divergence: small datasets cause smaller policy shifts",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 7"},
    background=[exp_setup_s5],
)

localized_overfitting_hypothesis = claim(
    "Small training datasets (≤32 problems) induce *localized overfitting* rather than systematic "
    "global policy shifts. With only 32 problems, even perfect overfitting learns isolated facts "
    "rather than generalizable patterns that alter global policy. The model sharpens confidence on "
    "specific samples through localized parameter updates without altering its global reasoning "
    "policy, thus preserving general capabilities on held-out benchmarks.",
    title="Hypothesis: small datasets cause localized overfitting not global collapse",
)

strat_localized_overfitting = support(
    [kl_divergence_small_vs_large, small_dataset_stability],
    localized_overfitting_hypothesis,
    reason=(
        "The small KL divergence (@kl_divergence_small_vs_large) shows small datasets do not "
        "substantially shift the global policy distribution from the reference. The stable "
        "performance (@small_dataset_stability) shows this limited shift is accompanied by "
        "preserved generalization. Together they support the localized overfitting hypothesis "
        "(@localized_overfitting_hypothesis): only a small region of parameter space is updated, "
        "leaving the broader reasoning capability intact."
    ),
    prior=0.82,
)

# ─── 5.2 Test-time training as safe application ───────────────────────────────

ttt_stability_observation = claim(
    "Test-time training (TTT) of Qwen3-1.7B-Base on AMC 2023 (40 problems, batch size 40) using "
    "majority voting reward is stable: both Ground Truth Reward and Majority Voting Reward rise "
    "and stabilize, with performance improving on both AMC 2023 and the out-of-domain AIME 2024 "
    "benchmark. In contrast, training on DAPO-17k (~17,000 problems) with the same model shows "
    "the familiar rise-then-fall collapse.",
    title="Test-time training avoids collapse; standard training collapses",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 8"},
    background=[exp_setup_s5],
)

ttt_safe_conclusion = claim(
    "Intrinsic URLVR can be safely applied in test-time training (TTT) scenarios because: "
    "(1) TTT datasets are small and domain-specific (≤dozens to hundreds of problems), keeping "
    "training within the safe small-dataset regime; (2) the target evaluation domain aligns well "
    "with the training problems, so confidence-correctness alignment is more likely to hold; "
    "(3) the limited policy shift from small-scale training preserves general capabilities. "
    "This explains why many recent works using intrinsic rewards focus on test-time rather than "
    "train-time settings.",
    title="Test-time training is a safe application of intrinsic URLVR",
)

strat_ttt_safe = support(
    [ttt_stability_observation, small_dataset_stability, localized_overfitting_hypothesis],
    ttt_safe_conclusion,
    reason=(
        "TTT stability (@ttt_stability_observation) demonstrates empirically that the small "
        "dataset regime is safe. The general small dataset result (@small_dataset_stability) "
        "shows this generalizes beyond TTT specifically. The localized overfitting mechanism "
        "(@localized_overfitting_hypothesis) explains why: TTT operates on a small, domain-specific "
        "set that falls within the safe-size threshold, producing only localized parameter updates."
    ),
    prior=0.87,
)

# ─── 5.3 Incorrect majority votes still work for TTT ─────────────────────────

incorrect_majority_ttt_obs = claim(
    "Training Qwen3-1.7B-Base on a deliberately adversarial DAPO-32 subset where almost all "
    "initial majority votes (maj@64) are incorrect (>40% majority wrong threshold), using maj@8 "
    "during training, still produces effective learning on OOD benchmarks without catastrophic "
    "collapse. Label Accuracy shows near-zero match throughout training (consistent collapse in "
    "pseudo-labels), yet AIME 2024 accuracy improves slightly and AMC 2023 accuracy improves from "
    "~0.330 to ~0.375.",
    title="Extreme TTT: incorrect majority votes still produce OOD gains",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 9"},
    background=[exp_setup_s5],
)

strat_incorrect_majority_works = support(
    [localized_overfitting_hypothesis, ood_generalization_obs],
    incorrect_majority_ttt_obs,
    reason=(
        "The localized overfitting mechanism (@localized_overfitting_hypothesis) predicts that "
        "small-scale training does not cause global policy shifts. Even when sharpening wrong "
        "answers, the policy shift is localized to those specific problems. The OOD generalization "
        "finding (@ood_generalization_obs) shows that sharpening on wrong training problems "
        "can still improve OOD performance if confidence-correctness alignment holds for unseen "
        "problems. Together these explain why even all-wrong majority votes in small TTT can "
        "yield gains."
    ),
    prior=0.78,
)
