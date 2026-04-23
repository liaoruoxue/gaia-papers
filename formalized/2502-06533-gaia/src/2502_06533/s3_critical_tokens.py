"""Section 3: Critical Tokens and Experimental Setup"""

from gaia.lang import claim, setting, support, induction, abduction, compare

from .motivation import (
    arithmetic_task_setup,
    negentropy_def,
    pretrain_breadth_impacts_exploration,
    rl_finetuning_challenge,
)

# --- Settings ---

critical_token_def = setting(
    "A 'critical token' is defined as a generated token that satisfies two criteria: "
    "(1) Decisiveness: if the model predicts this token incorrectly, the final answer will "
    "most likely be wrong; (2) Uncertainty: the pre-trained model shows substantially more "
    "uncertainty (lower confidence / higher entropy) on these tokens than on non-critical tokens. "
    "In the N-digit addition task, critical tokens correspond to digit positions that lie beyond "
    "the pre-training distribution (e.g., the carry and high-order digits when adding N+1 digit numbers "
    "after being trained only on up to N-digit numbers).",
    title="Critical token definition",
)

# --- Critical token empirical claims ---

critical_token_uncertainty_gap = claim(
    "Empirical measurements of the normalized negentropy change $\\Delta\\hat{J}$ show a large "
    "gap between critical and non-critical tokens across pre-training lengths $N$:\\n\\n"
    "| Token type | $N=3$ | $N=5$ | $N=7$ |\\n"
    "|------------|-------|-------|-------|\\n"
    "| Critical ($\\Delta\\hat{J}$) | $-0.33 \\pm 0.01$ | $-0.21 \\pm 0.18$ | $-0.13 \\pm 0.04$ |\\n"
    "| Non-critical ($\\Delta\\hat{J}$) | $0.0012 \\pm 0.0001$ | $0.0002 \\pm 0.0001$ | $0.0004 \\pm 0.0001$ |\\n\\n"
    "Negative $\\Delta\\hat{J}$ indicates the model becomes less confident after RL fine-tuning on "
    "the out-of-distribution (longer) addition task; non-critical tokens show essentially no change.",
    title="Critical tokens have large uncertainty gap vs non-critical",
    metadata={"source_table": "Table 1"},
)

critical_tokens_localize_failure = claim(
    "Failures in N+1-digit addition by a model pre-trained on up to N digits can be "
    "localized to specific critical token positions—primarily the carry digit and high-order "
    "digit positions. Errors at critical token positions (e.g., incorrect carry propagation or "
    "digit omission) cause the entire answer to be wrong, while errors at non-critical positions "
    "are rare and do not systematically affect the final answer.",
    title="Task failures localize to critical token positions",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 5"},
)

pretrain_generalization_results = claim(
    "GPT-2 models pre-trained on additions with operand lengths 1 to $N$ digits achieve "
    "the following accuracy on out-of-distribution (longer) additions (varying-digit evaluation mode):\\n\\n"
    "| Pre-training $N$ | Accuracy on $N+1$ | Accuracy on $N+2$ | Accuracy on $N+3$ |\\n"
    "|------------------|-------------------|-------------------|-------------------|\\n"
    "| 7 | ~49% | 0% | 0% |\\n"
    "| 9 | ~79% | ~1% | 0% |\\n"
    "| 11 | ~75% | ~31% | ~0% |\\n"
    "| 13 | ~89% | ~68% | ~20% |\\n\\n"
    "These results are from supervised pre-training alone, without RL fine-tuning. "
    "Confidence intervals are based on 1,000 test examples with resampling.",
    title="Pre-training generalization accuracy by digit length",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 2"},
)

pretrain_breadth_generalization_law = claim(
    "Pre-training on a broader range of digit lengths (larger $N$) consistently improves "
    "out-of-distribution generalization: a GPT-2 model trained up to $N=13$ achieves "
    "$88.9\\% \\pm 2.1\\%$ accuracy on $N+1=14$-digit addition and $67.7\\% \\pm 3.1\\%$ on "
    "$N+2=15$-digit addition (identical-digit evaluation), compared to near-zero for $N=7$ "
    "on $N+2$.",
    title="Broader pre-training improves OOD generalization",
    metadata={"source_table": "Table 4 (Appendix D)"},
)

larger_pretrain_fewer_rl_errors = claim(
    "Models pre-trained on larger digit ranges (larger $N$) make fewer initial errors "
    "on the RL fine-tuning task (N+1-digit addition), which reduces the exploration incentive "
    "during RL because the model encounters fewer distinct failure modes to learn from.",
    title="Larger pre-training → fewer RL-time errors → less exploration pressure",
)

larger_pretrain_qualitatively_different_errors = claim(
    "Models pre-trained on larger digit ranges tend to make qualitatively different types "
    "of errors during RL fine-tuning—generic mistakes such as token duplication and digit "
    "copying—rather than the critical-token errors (carry propagation failures) seen in "
    "models with less extensive pre-training. These generic errors are harder to correct "
    "through RL exploration than critical-token errors.",
    title="Larger pre-training shifts error type to generic, harder-to-fix mistakes",
    metadata={"figure": "artifacts/2502.06533.pdf, Figure 3"},
)

# --- Strategies ---

# The critical token uncertainty gap is a law; individual N observations are independent confirmations.
# Use generative direction: support([law], prediction/observation)
obs_ct_n3 = claim(
    "At pre-training length $N=3$, the normalized negentropy change $\\Delta\\hat{J}$ is "
    "$-0.33 \\pm 0.01$ for critical tokens and $0.0012 \\pm 0.0001$ for non-critical tokens.",
    title="Critical token negentropy gap at N=3",
)

obs_ct_n5 = claim(
    "At pre-training length $N=5$, the normalized negentropy change $\\Delta\\hat{J}$ is "
    "$-0.21 \\pm 0.18$ for critical tokens and $0.0002 \\pm 0.0001$ for non-critical tokens.",
    title="Critical token negentropy gap at N=5",
)

obs_ct_n7 = claim(
    "At pre-training length $N=7$, the normalized negentropy change $\\Delta\\hat{J}$ is "
    "$-0.13 \\pm 0.04$ for critical tokens and $0.0004 \\pm 0.0001$ for non-critical tokens.",
    title="Critical token negentropy gap at N=7",
)

# Generative direction: the law (uncertainty gap claim) predicts each per-N observation
s_ct_n3 = support(
    [critical_token_uncertainty_gap],
    obs_ct_n3,
    reason=(
        "If @critical_token_uncertainty_gap holds as a general law across pre-training lengths, "
        "it predicts a large negative $\\Delta\\hat{J}$ for critical tokens at $N=3$. "
        "The measured value $-0.33 \\pm 0.01$ vs $0.0012 \\pm 0.0001$ confirms this prediction."
    ),
    prior=0.88,
    background=[arithmetic_task_setup, negentropy_def],
)

s_ct_n5 = support(
    [critical_token_uncertainty_gap],
    obs_ct_n5,
    reason=(
        "If @critical_token_uncertainty_gap holds as a general law across pre-training lengths, "
        "it predicts a large negative $\\Delta\\hat{J}$ for critical tokens at $N=5$. "
        "The measured value $-0.21 \\pm 0.18$ vs $0.0002 \\pm 0.0001$ confirms this prediction."
    ),
    prior=0.85,
    background=[arithmetic_task_setup, negentropy_def],
)

s_ct_n7 = support(
    [critical_token_uncertainty_gap],
    obs_ct_n7,
    reason=(
        "If @critical_token_uncertainty_gap holds as a general law across pre-training lengths, "
        "it predicts a large negative $\\Delta\\hat{J}$ for critical tokens at $N=7$. "
        "The measured value $-0.13 \\pm 0.04$ vs $0.0004 \\pm 0.0001$ confirms this prediction."
    ),
    prior=0.87,
    background=[arithmetic_task_setup, negentropy_def],
)

ind_ct_n3_n5 = induction(s_ct_n3, s_ct_n5, law=critical_token_uncertainty_gap,
    reason="N=3 and N=5 experiments use different pre-training datasets, providing independent evidence.")

ind_ct_n3_n7 = induction(ind_ct_n3_n5, s_ct_n7, law=critical_token_uncertainty_gap,
    reason="N=7 experiment further extends the independent replications across pre-training lengths.")

# Support: pre-training breadth → generalization law
strat_pretrain_breadth_law = support(
    [pretrain_generalization_results],
    pretrain_breadth_generalization_law,
    reason=(
        "The tabulated accuracy data in @pretrain_generalization_results shows a monotone trend: "
        "as $N$ increases from 7 to 13, accuracy on $N+1$ improves from ~49% to ~89%, and "
        "on $N+2$ from 0% to ~68%. This pattern supports the general law @pretrain_breadth_generalization_law "
        "that broader pre-training consistently improves OOD generalization."
    ),
    prior=0.85,
    background=[arithmetic_task_setup],
)

# Support: pre-training breadth impacts exploration (motivation claim) — supported by empirical observations
strat_pretrain_ambivalent = support(
    [pretrain_breadth_generalization_law, larger_pretrain_fewer_rl_errors,
     larger_pretrain_qualitatively_different_errors],
    pretrain_breadth_impacts_exploration,
    reason=(
        "Combining @pretrain_breadth_generalization_law (broader pre-training improves baseline) "
        "with @larger_pretrain_fewer_rl_errors (fewer RL-time errors) and "
        "@larger_pretrain_qualitatively_different_errors (harder-to-fix error types), "
        "the @pretrain_breadth_impacts_exploration claim follows: more pre-training helps baseline "
        "but reduces exploration incentive and shifts errors to harder-to-fix types."
    ),
    prior=0.80,
    background=[arithmetic_task_setup],
)

# Support: critical tokens localize failure
strat_localize = support(
    [critical_token_uncertainty_gap],
    critical_tokens_localize_failure,
    reason=(
        "Given the @critical_token_uncertainty_gap showing that the model is systematically "
        "less confident at critical token positions (as defined by @critical_token_def), "
        "errors concentrate at positions where the model is uncertain, and those errors propagate "
        "to cause the entire answer to be wrong, supporting @critical_tokens_localize_failure."
    ),
    prior=0.82,
    background=[arithmetic_task_setup, critical_token_def],
)
