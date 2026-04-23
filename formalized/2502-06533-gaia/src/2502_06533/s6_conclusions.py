"""Section 6: Conclusions and Limitations"""

from gaia.lang import claim, setting, support

from .s5_results import (
    prioritized_kl_outperforms_standard,
    prioritized_kl_maintains_critical_token_success,
    pretrain_breadth_ambivalent_rl,
    rl_finetuning_does_improve_accuracy,
    standard_kl_blocks_critical_exploration,
)
from .s4_method import prioritized_kl_method
from .s3_critical_tokens import critical_token_uncertainty_gap

# --- Generalization claims ---

prioritized_kl_generalizes = claim(
    "The Prioritized KL Penalty approach is proposed to generalize beyond arithmetic tasks: "
    "any RL fine-tuning scenario where a language model must act outside its pre-training "
    "distribution and where critical tokens can be identified by the reference model's uncertainty "
    "could benefit from the same confidence-weighted KL penalty modification.",
    title="Prioritized KL penalty proposed to generalize to other RL fine-tuning tasks",
)

# --- Limitation claims ---

limitation_small_model = claim(
    "The experimental evaluation is restricted to GPT-2 (85M parameters), which is far smaller "
    "than modern large language models used in practice (e.g., 7B–70B parameter models). "
    "It is unclear whether the critical-token phenomenon and the benefits of the Prioritized KL "
    "Penalty scale to much larger models.",
    title="Limitation: experiments restricted to small GPT-2 model",
)

limitation_simple_task = claim(
    "The arithmetic addition task used in the experiments is far simpler than standard LLM "
    "benchmarks (e.g., mathematical reasoning, code generation, dialogue). "
    "The extent to which critical tokens can be identified and exploited in more complex tasks "
    "with longer reasoning chains is not demonstrated.",
    title="Limitation: arithmetic task is simpler than practical LLM benchmarks",
)

limitation_scratchpad = claim(
    "The experimental setup uses formatted scratchpads (step-by-step intermediate computations) "
    "to enable fine-grained token-level analysis. This architectural choice may not generalize "
    "to tasks without structured scratchpad outputs, where critical tokens are harder to identify.",
    title="Limitation: results tied to scratchpad-based reasoning format",
)

limitation_fixed_reference = claim(
    "The method assumes a fixed reference (pre-trained) model and uses its token-level entropy "
    "as the confidence signal. No Bayesian uncertainty over model parameters is considered, "
    "which means the method cannot distinguish between epistemic uncertainty (lack of training data) "
    "and aleatoric uncertainty (inherent task ambiguity).",
    title="Limitation: no Bayesian uncertainty over model parameters",
)

# --- Conclusion claims ---

main_conclusion = claim(
    "More precisely balancing the trade-off between old and new policies—by reducing the KL "
    "penalty specifically on tokens where the pre-trained model is uncertain—can substantially "
    "improve a model's exploration capabilities during RL fine-tuning, as evidenced by "
    "~20 percentage point accuracy improvements on out-of-distribution arithmetic tasks.",
    title="Main conclusion: confidence-weighted KL penalty improves RL exploration",
)

# --- Strategies ---

strat_main_conclusion = support(
    [prioritized_kl_outperforms_standard, prioritized_kl_maintains_critical_token_success,
     standard_kl_blocks_critical_exploration],
    main_conclusion,
    reason=(
        "@prioritized_kl_outperforms_standard shows a ~20pp accuracy gain. "
        "@prioritized_kl_maintains_critical_token_success shows the mechanism: critical-token "
        "success is preserved under prioritized KL. "
        "@standard_kl_blocks_critical_exploration explains why standard KL fails: it prevents "
        "exploration where it is most needed. "
        "Together these three results support @main_conclusion."
    ),
    prior=0.85,
)

strat_generalization = support(
    [prioritized_kl_method, standard_kl_blocks_critical_exploration],
    prioritized_kl_generalizes,
    reason=(
        "The @prioritized_kl_method is defined in terms of the reference model's entropy "
        "(a property of any pre-trained LLM) and the KL penalty (used in virtually all RL "
        "fine-tuning frameworks). @standard_kl_blocks_critical_exploration demonstrates the "
        "mechanism is not specific to arithmetic. Therefore @prioritized_kl_generalizes "
        "to other tasks with similar structure."
    ),
    prior=0.55,
)

# Limitations: each limits the generalization claim
strat_lim_model = support(
    [limitation_small_model],
    prioritized_kl_generalizes,
    reason=(
        "@limitation_small_model restricts confidence in @prioritized_kl_generalizes: "
        "without testing on larger models (7B+), it is uncertain whether the "
        "critical-token phenomenon scales. This premise weakens the generalization claim."
    ),
    prior=0.40,
)

strat_lim_task = support(
    [limitation_simple_task],
    prioritized_kl_generalizes,
    reason=(
        "@limitation_simple_task restricts confidence in @prioritized_kl_generalizes: "
        "arithmetic is far simpler than real LLM tasks (code, dialogue, math reasoning), "
        "and identifying critical tokens may be much harder in complex tasks."
    ),
    prior=0.40,
)

strat_lim_scratchpad = support(
    [limitation_scratchpad],
    prioritized_kl_generalizes,
    reason=(
        "@limitation_scratchpad restricts confidence in @prioritized_kl_generalizes: "
        "the scratchpad format makes critical tokens easy to identify; without scratchpads, "
        "the confidence-weighting may not be applicable."
    ),
    prior=0.45,
)

strat_lim_bayes = support(
    [limitation_fixed_reference],
    prioritized_kl_generalizes,
    reason=(
        "@limitation_fixed_reference restricts @prioritized_kl_generalizes: "
        "the method uses a fixed reference model's entropy, which conflates epistemic and "
        "aleatoric uncertainty. In domains with more model uncertainty, this limitation "
        "becomes more significant."
    ),
    prior=0.50,
)
