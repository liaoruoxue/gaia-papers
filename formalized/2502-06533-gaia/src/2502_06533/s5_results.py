"""Section 5: Experimental Results"""

from gaia.lang import claim, setting, support, abduction, compare, contradiction

from .motivation import arithmetic_task_setup, rl_finetuning_challenge
from .s3_critical_tokens import (
    critical_token_uncertainty_gap,
    critical_tokens_localize_failure,
    pretrain_generalization_results,
    larger_pretrain_fewer_rl_errors,
    larger_pretrain_qualitatively_different_errors,
    pretrain_breadth_generalization_law,
    pretrain_breadth_impacts_exploration,
)
from .s4_method import prioritized_kl_method, prioritized_kl_intuition, beta_hyperparameter

# --- Main result claims ---

prioritized_kl_outperforms_standard = claim(
    "On the N+1=8-digit addition task (RL fine-tuning of a GPT-2 model pre-trained up to N=7 digits), "
    "the Prioritized KL Penalty achieves approximately 60–70% accuracy after 2,000 training episodes, "
    "compared to approximately 40–50% for the standard KL penalty. "
    "The improvement is consistent across multiple training runs.",
    title="Prioritized KL penalty outperforms standard KL on 8-digit addition",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 4"},
)

prioritized_kl_maintains_critical_token_success = claim(
    "During RL fine-tuning with the Prioritized KL Penalty, the model maintains high "
    "success probabilities on critical tokens throughout training (above 80%), whereas "
    "with the standard KL penalty, the model frequently reverts to near-baseline critical-token "
    "success probabilities (~20–40%), suggesting the standard penalty prevents effective "
    "exploration at these token positions.",
    title="Prioritized KL maintains high critical-token success, standard KL reverts",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 4"},
)

standard_kl_blocks_critical_exploration = claim(
    "The standard KL penalty acts as a barrier to exploration on critical tokens: "
    "because the pre-trained model is uncertain at critical token positions, the KL penalty "
    "penalizes any policy divergence there, which prevents the model from discovering "
    "correct strategies for these tokens even when the reward signal indicates improvement is needed.",
    title="Standard KL penalty blocks exploration at critical tokens",
)

alt_standard_kl_sufficient = claim(
    "An alternative explanation is that the standard KL penalty is sufficient for "
    "RL fine-tuning and the performance gap between prioritized and standard KL is due "
    "to other factors (e.g., hyperparameter sensitivity, reward shaping, or architectural choices) "
    "rather than fundamentally different exploration behavior at critical tokens.",
    title="Alternative: standard KL penalty sufficient, performance gap from other factors",
)

pretrain_breadth_ambivalent_rl = claim(
    "Increasing pre-training breadth (larger $N$) improves baseline accuracy but "
    "does not proportionally improve RL fine-tuning gains. Models pre-trained on larger "
    "digit ranges plateau in RL improvement relative to their pre-training baseline, "
    "because they make fewer initial errors and therefore experience weaker exploration pressure.",
    title="Pre-training breadth improves baseline but has diminishing RL fine-tuning gains",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 3"},
)

rl_finetuning_does_improve_accuracy = claim(
    "RL fine-tuning (with either standard or prioritized KL penalty) does improve accuracy "
    "on out-of-distribution (N+1-digit) addition tasks compared to pre-training alone, "
    "demonstrating that RL can successfully drive exploration beyond the pre-training distribution "
    "in this arithmetic setting.",
    title="RL fine-tuning improves OOD accuracy beyond pre-training",
)

# --- Contradiction: prioritized vs standard KL effectiveness ---
not_both_effective = contradiction(
    standard_kl_blocks_critical_exploration,
    alt_standard_kl_sufficient,
    reason=(
        "If the standard KL penalty fundamentally blocks critical-token exploration "
        "(@standard_kl_blocks_critical_exploration), then it cannot simultaneously be sufficient "
        "for effective RL fine-tuning (@alt_standard_kl_sufficient) in out-of-distribution settings. "
        "These two claims cannot both hold."
    ),
    prior=0.92,
)

# --- Abduction: prioritized KL outperforms standard ---
pred_prioritized = claim(
    "The Prioritized KL Penalty predicts higher accuracy than standard KL on N+1=8-digit addition "
    "because it reduces the KL constraint specifically on critical tokens, enabling the policy to "
    "explore at token positions that determine task success.",
    title="Prediction: Prioritized KL should outperform standard KL",
)

pred_alt_standard = claim(
    "The standard KL penalty predicts comparable accuracy to the Prioritized KL Penalty because "
    "any uniform reduction of exploration constraint at uncertain tokens is dominated by the "
    "reward signal, and the confidence-weighting provides no additional benefit.",
    title="Alternative prediction: standard KL achieves comparable accuracy",
)

s_h_outperforms = support(
    [prioritized_kl_method],
    prioritized_kl_outperforms_standard,
    reason=(
        "The @prioritized_kl_method reduces the KL penalty on uncertain tokens, which are "
        "exactly the critical tokens that determine task success (@critical_tokens_localize_failure). "
        "This predicts that the model will more successfully explore and learn correct strategies "
        "at these positions, leading to higher accuracy compared to standard KL."
    ),
    prior=0.80,
    background=[arithmetic_task_setup],
)

s_alt_outperforms = support(
    [alt_standard_kl_sufficient],
    prioritized_kl_outperforms_standard,
    reason=(
        "If the standard KL penalty is sufficient (@alt_standard_kl_sufficient), "
        "there should be no performance gap, predicting comparable accuracy for both methods."
    ),
    prior=0.35,
    background=[arithmetic_task_setup],
)

comp_outperforms = compare(
    pred_prioritized, pred_alt_standard, prioritized_kl_outperforms_standard,
    reason=(
        "Experimental results show prioritized KL achieves 60-70% vs standard KL's 40-50% "
        "on 8-digit addition—a ~20 percentage point gap—strongly matching the prioritized KL "
        "prediction and refuting the alternative."
    ),
    prior=0.85,
)

abd_outperforms = abduction(
    s_h_outperforms, s_alt_outperforms, comp_outperforms,
    reason=(
        "Both @prioritized_kl_method and the @alt_standard_kl_sufficient hypothesis attempt "
        "to explain the accuracy outcome on the 8-digit addition task."
    ),
    background=[arithmetic_task_setup],
)

# --- Support: mechanism — prioritized KL maintains critical token success ---
strat_critical_token_success = support(
    [prioritized_kl_method, critical_token_uncertainty_gap],
    prioritized_kl_maintains_critical_token_success,
    reason=(
        "The @prioritized_kl_method reduces the KL penalty where $\\hat{J} \\approx 0$, "
        "i.e., exactly at critical tokens as identified by @critical_token_uncertainty_gap. "
        "This allows the policy to update freely at those positions. "
        "Empirical results confirm that the model trained with prioritized KL maintains >80% "
        "success on critical tokens while the standard KL model reverts to 20-40%."
    ),
    prior=0.80,
    background=[arithmetic_task_setup],
)

# --- Support: standard KL blocks exploration ---
strat_standard_blocks = support(
    [critical_token_uncertainty_gap, prioritized_kl_maintains_critical_token_success],
    standard_kl_blocks_critical_exploration,
    reason=(
        "Since @critical_token_uncertainty_gap shows the pre-trained model is uncertain at "
        "critical tokens, the standard KL penalty (which uniformly penalizes divergence) "
        "penalizes exploration exactly where it is needed most. "
        "@prioritized_kl_maintains_critical_token_success shows that removing this constraint "
        "on uncertain tokens does lead to better critical-token outcomes, implying the constraint "
        "was indeed the bottleneck."
    ),
    prior=0.78,
    background=[arithmetic_task_setup],
)

# --- Support: RL fine-tuning improves accuracy ---
strat_rl_improves = support(
    [pretrain_generalization_results],
    rl_finetuning_does_improve_accuracy,
    reason=(
        "The @pretrain_generalization_results table shows accuracy for pre-training only. "
        "The RL fine-tuning results (Figure 4) show higher accuracy than these baselines, "
        "confirming @rl_finetuning_does_improve_accuracy—both standard and prioritized KL "
        "achieve better OOD accuracy than the pre-trained model alone."
    ),
    prior=0.88,
    background=[arithmetic_task_setup],
)

# --- Support: pre-training breadth ambivalent effect on RL ---
strat_pretrain_rl_ambivalent = support(
    [larger_pretrain_fewer_rl_errors, larger_pretrain_qualitatively_different_errors,
     pretrain_breadth_generalization_law],
    pretrain_breadth_ambivalent_rl,
    reason=(
        "Models with broader pre-training (@pretrain_breadth_generalization_law: better baseline) "
        "show diminishing RL improvement because: "
        "(1) @larger_pretrain_fewer_rl_errors — fewer initial errors reduce exploration incentive; "
        "(2) @larger_pretrain_qualitatively_different_errors — errors shift to generic mistakes "
        "that are harder to fix by RL. Together, broader pre-training improves baseline but "
        "yields weaker RL gains, making the pre-training effect ambivalent overall."
    ),
    prior=0.75,
    background=[arithmetic_task_setup],
)
