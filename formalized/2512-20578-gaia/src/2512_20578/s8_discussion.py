"""Section 8: Discussion, Limitations, and Conclusions"""

from gaia.lang import claim, setting, support, contradiction
from .motivation import internal_cues_exist, gnosis_proposal
from .s4_results import gnosis_superior_overall, calibration_quality
from .s5_transfer import transfer_generalizes, transfer_fails_cross_family, shared_circuits_hypothesis
from .s7_early_detection import gnosis_generalizes_partial, early_stopping_implication

# ── Discussion Claims ──────────────────────────────────────────────────────────

feature_analysis = claim(
    "Visualization of Gnosis learned representations reveals clear class separation between "
    "correct and incorrect responses. Hidden state features show the clearest separation, "
    "attention features show weaker but still discriminative separation, and the merged "
    "(fused) feature space provides the sharpest overall discrimination between correct "
    "and incorrect outputs.",
    title="Feature space discrimination analysis",
    metadata={"source_section": "Section 4, Feature Analysis"},
)

backbone_accuracy_stats = claim(
    "Backbone LLM outcome statistics on evaluation datasets:\n\n"
    "| Backbone | Domain | Accuracy | Hallucination | No-answer |\n"
    "|----------|--------|----------|---------------|-----------|\n"
    "| Qwen3 1.7B-Hybrid | Math | 44.87% | 47.76% | 7.37% |\n"
    "| Qwen3 1.7B-Hybrid | TriviaQA | 33.54% | 55.67% | 10.79% |\n"
    "| Qwen3 1.7B-Hybrid | MMLU-Pro | 66.09% | 31.53% | 2.39% |\n"
    "| Qwen3 4B-Thinking | Math | 63.27% | 25.31% | 11.42% |\n"
    "| Qwen3 4B-Instruct | Math | 57.51% | 29.26% | 13.22% |\n"
    "| OpenAI gpt-oss-20B | Math | 52.53% | 42.63% | 4.84% |\n\n"
    "Hallucination rates of 25-56% across models confirm the practical importance of "
    "self-verification mechanisms.",
    title="Backbone outcome statistics (Table 11)",
    metadata={"source_table": "Table 11", "source_section": "Section 4, Appendix"},
)

internal_signals_claim = claim(
    "Reliable correctness signals are demonstrably present in LLM internal states (hidden states "
    "and attention patterns) and can be extracted with high accuracy using a lightweight trained "
    "probe (~5M parameters), without any access to external reference answers, external judges, "
    "or additional LLM inference calls.",
    title="Internal signals are reliable and extractable",
    metadata={"source_section": "Section 5, Conclusions"},
)

proprietary_model_limitation = claim(
    "Gnosis requires access to the model's hidden states and attention maps. This access is "
    "unavailable for proprietary API-only models (e.g., GPT-4, Claude), restricting Gnosis "
    "to open-weight models where internal activations are exposed.",
    title="Proprietary model access limitation",
    metadata={"source_section": "Section 5, Limitations"},
)

# ── Contradiction: internal vs. external superiority ─────────────────────────

external_always_superior = claim(
    "External judges (reward models, proprietary LLMs) uniformly outperform internal "
    "probing mechanisms for LLM self-verification in accuracy and calibration.",
    title="External judges always superior claim",
)

not_both_internal_external = contradiction(
    external_always_superior,
    gnosis_superior_overall,
    reason=(
        "If external judges always outperformed internal probes, Gnosis could not achieve "
        "higher AUROC (0.95) and BSS (0.59) than Skywork-8B (0.90 AUROC) and Gemini 2.5 Pro (0.91 AUROC). "
        "The observed results are incompatible with a universal external-judge superiority claim."
    ),
    prior=0.95,
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_internal_signals_supported = support(
    [gnosis_superior_overall, calibration_quality, transfer_generalizes],
    internal_signals_claim,
    reason=(
        "Three lines of evidence jointly support the claim that internal signals are reliable: "
        "(1) Gnosis consistently outperforms external judges (@gnosis_superior_overall), "
        "(2) its calibration is demonstrably sharper (bimodal distributions, @calibration_quality), "
        "and (3) even transfer to new models succeeds (@transfer_generalizes), showing the "
        "signals generalize beyond training conditions."
    ),
    prior=0.88,
)

strat_scope_limitation = support(
    [transfer_fails_cross_family, proprietary_model_limitation],
    gnosis_proposal,
    reason=(
        "The two identified limitations—cross-family transfer failure (@transfer_fails_cross_family) "
        "and proprietary model inaccessibility (@proprietary_model_limitation)—define the scope "
        "of @gnosis_proposal: it is a self-awareness mechanism for open-weight model families, "
        "not a universal correctness verifier. These limitations are acknowledged in the paper "
        "and do not invalidate the claims within the stated scope."
    ),
    prior=0.82,
)

strat_feature_analysis_supports = support(
    [feature_analysis],
    internal_signals_claim,
    reason=(
        "Visualization showing clear class separation in learned Gnosis representations "
        "(@feature_analysis) provides direct evidence that the internal signals are reliably "
        "discriminative, supporting @internal_signals_claim."
    ),
    prior=0.85,
)

strat_hallucination_rates = support(
    [backbone_accuracy_stats],
    gnosis_proposal,
    reason=(
        "Hallucination rates of 25-56% across backbone models (@backbone_accuracy_stats) "
        "confirm the practical significance of the problem that @gnosis_proposal addresses. "
        "High hallucination rates make self-verification a genuine need."
    ),
    prior=0.90,
)
