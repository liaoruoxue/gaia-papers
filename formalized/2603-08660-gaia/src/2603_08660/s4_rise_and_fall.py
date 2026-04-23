"""Section 4: When Does Intrinsic URLVR Work? Rise-Then-Fall Pattern"""

from gaia.lang import claim, setting, support, induction

from .motivation import urlvr_definition
from .s3_sharpening import (
    sharpening_dual_nature,
    theorem1_sharpening,
    unified_sharpening_framework,
)

# ─── Experimental setup ───────────────────────────────────────────────────────

exp_setup_s4 = setting(
    "Experiments in Section 4 train Qwen3-1.7B-Base on DAPO-17k (~17,000 math problems) using "
    "default hyperparameters unless noted. Evaluation uses AIME 2024, AIME 2025, and AMC 2023 "
    "benchmarks, generating 32 solutions per problem at temperature 0.6 with top-p 0.95, "
    "reporting average accuracy (avg@32). Three training dynamics are tracked: "
    "(1) Majority Voting Reward (proxy intrinsic signal), "
    "(2) Reward Accuracy (whether pseudo-reward matches ground truth), and "
    "(3) Actor Entropy.",
    title="Section 4 experimental setup",
)

# ─── 4.1.1 Early success, later collapse ─────────────────────────────────────

early_success_observation = claim(
    "Intrinsic URLVR (majority voting reward) initially matches or exceeds ground-truth RLVR "
    "training performance on AIME 2024, AIME 2025, and AMC 2023 benchmarks during early training "
    "steps when training Qwen3-1.7B-Base on DAPO-17k.",
    title="Intrinsic URLVR early performance match",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 2"},
    background=[exp_setup_s4],
)

later_collapse_observation = claim(
    "After initial gains, intrinsic URLVR (majority voting reward) training of Qwen3-1.7B-Base on "
    "DAPO-17k exhibits reward hacking: the proxy Majority Voting Reward continues to rise while "
    "both Reward Accuracy and validation benchmark performance decline. Actor Entropy decreases "
    "faster under majority voting than under ground-truth training, connecting reduced uncertainty "
    "to performance degradation.",
    title="Intrinsic URLVR eventual collapse with reward hacking",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 2"},
    background=[exp_setup_s4],
)

hyperparameter_robustness_collapse = claim(
    "Extensive hyperparameter tuning across four key dimensions (training temperature, mini-batch "
    "size, KL regularization, rollout number) across five intrinsic reward methods shows that "
    "nearly all settings eventually degrade. Some hyperparameters (notably mini-batch size and "
    "rollout number) affect *when* collapse occurs but not *whether* it occurs. Even the most "
    "stable settings collapse around 1,000 steps (~4 epochs), suggesting the rise-then-fall "
    "pattern reflects a fundamental limitation rather than an engineering problem.",
    title="Collapse is hyperparameter-independent",
    background=[exp_setup_s4],
)

# ─── 4.1.2 Different failure modes ───────────────────────────────────────────

three_failure_modes = claim(
    "Five intrinsic reward methods—Majority Voting, Self-Certainty, Trajectory-Level Entropy, "
    "Token-Level Entropy, and Probability—exhibit three distinct failure patterns:\n\n"
    "1. **Gradual degradation** (Self-Certainty, Majority Voting): Slowest collapse, maintaining "
    "higher Label Accuracy without catastrophic failure within one epoch. Self-Certainty "
    "sharpens against a uniform reference (less aggressive); Majority Voting operates at the "
    "answer level avoiding token-level artifacts.\n\n"
    "2. **Length collapse** (Probability): Multiplying token probabilities favors shorter "
    "sequences, so model becomes confident but produces overly brief answers. Reward is "
    "maximized by brevity rather than correctness.\n\n"
    "3. **Repetition collapse** (Token-Level Entropy, Trajectory-Level Entropy): Averaging "
    "entropy across tokens can be minimized by repeating high-probability tokens, leading "
    "to repetitive outputs rather than correct reasoning.",
    title="Three distinct intrinsic reward failure modes",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 3"},
    background=[exp_setup_s4],
)

# ─── 4.2.1 Per-problem sharpening ────────────────────────────────────────────

per_problem_sharpening_obs = claim(
    "Per-problem analysis of Qwen3-1.7B-Base trained on 25 individual MATH500 problems for 100 "
    "epochs with Trajectory-Level Entropy reward reveals four patterns:\n\n"
    "| Pattern | Description | Prevalence |\n"
    "|---------|-------------|------------|\n"
    "| Amplifying success | Starts correct, deepens confidence in correct answer | 3 problems |\n"
    "| Amplifying failure | Highest-reward sample nearly always wrong; deepens wrong confidence | ~2 problems |\n"
    "| Wrong→Correct | Starts wrong, but highest-reward sample is mostly correct during training | ~3 problems |\n"
    "| Correct→Wrong | Starts correct, inconsistent reward signal causes gradual degradation | ~1 problem |\n\n"
    "Greedy correctness flipped in only 3/25 cases (12%). In all cases, confidence (color depth) "
    "deepens regardless of whether the answer is correct, confirming sharpening rather than correction.",
    title="Per-problem training dynamics: amplification not correction",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 4"},
    background=[exp_setup_s4],
)

# ─── 4.2.2 OOD cross-problem generalization ──────────────────────────────────

ood_generalization_obs = claim(
    "When Qwen3-1.7B-Base is trained on 6 MATH500 problems where the highest-reward samples are "
    "mostly wrong (low training Label Accuracy throughout), performance on two unseen out-of-distribution "
    "(OOD) test problems (ID 76 and 131) still improves: Test Label Accuracy rises from 0 to 1 "
    "across all 6 training configurations. Sharpening from wrong training problems can generalize "
    "to OOD problems where the model's confidence *does* align with correctness.",
    title="OOD generalization of sharpening despite wrong training labels",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 5"},
    background=[exp_setup_s4],
)

# ─── Key empirical claim ────────────────────────────────────────────────────

rise_then_fall_universal = claim(
    "Intrinsic URLVR universally follows a rise-then-fall pattern across all tested methods and "
    "hyperparameter configurations. Early gains reflect confidence-correctness alignment in the "
    "model's prior for the early-training problems, while eventual collapse is inevitable when "
    "this alignment breaks down. The timing of collapse is determined by the model prior "
    "(confidence-correctness alignment) rather than engineering choices.",
    title="Universal rise-then-fall pattern of intrinsic URLVR",
)

# ─── Induction: universal pattern from multiple observations ─────────────────

s_obs1 = support(
    [rise_then_fall_universal],
    early_success_observation,
    reason=(
        "The universal rise-then-fall law predicts that early success should be visible across "
        "all methods. @early_success_observation confirms this for majority voting vs. ground-truth "
        "training on AIME/AMC benchmarks with Qwen3-1.7B-Base."
    ),
    prior=0.9,
)

s_obs2 = support(
    [rise_then_fall_universal],
    later_collapse_observation,
    reason=(
        "The universal pattern predicts that collapse eventually occurs regardless of proxy reward "
        "going up. @later_collapse_observation confirms reward hacking: proxy reward rises while "
        "true accuracy falls, consistent with the sharpening mechanism."
    ),
    prior=0.9,
)

s_obs3 = support(
    [rise_then_fall_universal],
    hyperparameter_robustness_collapse,
    reason=(
        "If the pattern is fundamental rather than engineering-dependent, collapse should persist "
        "across hyperparameter choices. @hyperparameter_robustness_collapse confirms collapse "
        "across all tested settings, differing only in timing."
    ),
    prior=0.88,
)

ind_12 = induction(s_obs1, s_obs2, law=rise_then_fall_universal,
    reason="Early success and later collapse are two phases of the same rise-then-fall pattern; observations are from the same training run but at different time points.")

ind_rise_fall = induction(ind_12, s_obs3, law=rise_then_fall_universal,
    reason="Hyperparameter robustness is an independent experimental confirmation across different settings.")

strat_theory_to_empirical = support(
    [sharpening_dual_nature, theorem1_sharpening],
    rise_then_fall_universal,
    reason=(
        "The sharpening dual nature (@sharpening_dual_nature) predicts: early training encounters "
        "problems where confidence aligns with correctness (giving early gains), while continued "
        "training eventually reaches problems where alignment breaks down (causing collapse). "
        "Theorem 1 (@theorem1_sharpening) predicts geometric convergence to initial majority, "
        "explaining why collapse is inevitable once alignment degrades. The theoretical prediction "
        "precisely matches the observed rise-then-fall pattern."
    ),
    prior=0.85,
)
