"""Phase 1: Baseline Performance and Confidence Calibration (GPT-4o)"""

from gaia.lang import claim, setting, support

from .motivation import calibration_method, dataset_setting

# ── Models tested ────────────────────────────────────────────────────────────

models_tested = setting(
    "Models tested: GPT-4o (via OpenAI Chat Completions API), Gemma 3 27B instruction-tuned "
    "(via official JAX gemma library, checkpoint GEMMA3_27B_IT), DeepSeek-V3 671B (mixture-of-experts, "
    "~37B active per token, via Together.ai, sampling temperature=0.7), and Qwen 80B "
    "(Qwen3-Next-80B-A3B-Instruct, via Together.ai). "
    "Llama 70B instruct 3.1 was tested but excluded due to an abstention rate of only 4% in Phase 2. "
    "Greedy decoding was used throughout except for DeepSeek (temperature=0.7 required for logprob access). "
    "Confidence was extracted from the next-token distribution immediately after the answer prefix 'Answer:'.",
    title="Models tested and decoding settings",
)

# ── Phase 1 results ──────────────────────────────────────────────────────────

gpt4o_phase1_accuracy = claim(
    "GPT-4o achieved 63.7% correct answers on Phase 1 (4-way multiple-choice, no abstention option, "
    "n=1,000 questions from SimpleQA). The majority of errors involved selecting a similar foil, "
    "followed by dissimilar and unrelated foils.",
    title="GPT-4o Phase 1 accuracy: 63.7%",
    background=[dataset_setting, models_tested],
)

gpt4o_calibration_result = claim(
    "GPT-4o confidence calibration (temperature scaling on 1,000 held-out questions) yielded an "
    "optimal scaling temperature of τ_scale = 4.1, ECE = 0.046, and AUROC = 0.90.",
    title="GPT-4o calibration: τ=4.1, ECE=0.046, AUROC=0.90",
    background=[calibration_method, dataset_setting],
)

confidence_predicts_error = claim(
    "Calibrated confidence strongly and negatively predicts error rate on the Phase 1 test set: "
    "r(12) = −0.97, p < 0.001, Cohen's d = −8.13. "
    "Correct responses showed substantially higher mean confidence than errors, confirming that "
    "GPT-4o's calibrated logits provide a meaningful signal of choice accuracy.",
    title="Confidence robustly predicts error rate (r = -0.97)",
    background=[calibration_method, models_tested, dataset_setting],
)

confidence_distributions_separated = claim(
    "Confidence distributions are clearly separated between correct and incorrect Phase 1 trials: "
    "correct responses show substantially higher mean confidence than error trials.",
    title="Confidence distributions separated for correct vs. incorrect responses",
    background=[dataset_setting, models_tested],
)

# ── Reasoning ────────────────────────────────────────────────────────────────

strat_confidence_validity = support(
    [gpt4o_calibration_result, confidence_predicts_error],
    confidence_distributions_separated,
    reason=(
        "The high AUROC of 0.90 (@gpt4o_calibration_result) indicates the calibrated logits "
        "discriminate well between correct and incorrect responses. The strong negative correlation "
        "between calibrated confidence and error rate (r = -0.97, @confidence_predicts_error) "
        "demonstrates that higher confidence consistently corresponds to lower error probability. "
        "Together, these results confirm that the calibrated confidence distributions are meaningfully "
        "separated between correct and incorrect trials [@Guo2017]."
    ),
    prior=0.95,
)
