"""Priors for 2512-21720: An Information Theoretic Perspective on Agentic System Design.

All claims below are independent premises (leaf nodes in the BP graph).
Priors reflect reviewer confidence that the claim is true as stated,
informed by the paper's evidence, experimental rigor, and domain context.

Empirical results (multi-seed, multi-dataset, direct measurements):
  Confidence is high (0.87-0.93) — directly reported numbers from figures.

Methodological claims (estimator properties):
  Confidence is very high (0.90-0.93) — definitional or near-definitional.

Limitation claims (acknowledged by authors):
  Confidence is moderate-high (0.83-0.88) — author-stated.

Context/framing claims:
  Confidence is moderate (0.78-0.82) — characterization of field state.
"""

from . import (
    # Empirical results (Section 3.1)
    accuracy_scales_with_compressor,
    larger_compressors_more_concise,
    predictor_scaling_marginal,
    # Empirical results (Section 3.2-3.3)
    mi_scales_with_compressor,
    bit_efficiency_scales_with_compressor,
    scaling_robust_to_conciseness_prompt,
    compressor_family_most_important,
    # Deep Research results (Section 3.5)
    qwen14b_deep_research_result,
    small_compressor_deep_research,
    # Methodological claims
    mi_estimator_practical,
    mi_estimator_clipping,
    local_compute_trade,
    # Limitation
    limitation_proxy_variance,
    # Context/framing
    design_adhoc,
)

PRIORS = {
    # ── Empirical results (Section 3.1) ───────────────────────────────────────
    accuracy_scales_with_compressor: (
        0.92,
        "Measured directly on LongHealth and FinanceBench with S=5 random seeds. "
        "3.1x and 2.6x accuracy improvements are large-magnitude, consistent across "
        "three model families (Llama-3, Qwen-2.5, Gemma-3) and replicated across datasets."
    ),
    larger_compressors_more_concise: (
        0.90,
        "Token count is a direct, deterministic measurement. The 4.6x conciseness gain "
        "for 7-12B vs 1-1.5B compressors is measured across multiple model families; "
        "token counting is not subject to LLM judge error."
    ),
    predictor_scaling_marginal: (
        0.88,
        "Measured across Llama predictor sizes (1B, 8B, 70B, 405B) on LongHealth and "
        "FinanceBench with S=5 seeds. The <12% and <1% gains from 70B->405B are direct "
        "accuracy comparisons with clear numerical grounding."
    ),

    # ── Empirical results (Sections 3.2-3.3) ──────────────────────────────────
    mi_scales_with_compressor: (
        0.87,
        "MI is estimated via Monte Carlo estimator with proxy models at 7-8B scale. "
        "Scaling trend is consistent across model families and validated with multiple "
        "proxy choices (Appendix E.1.4). Slight uncertainty from proxy model dependency."
    ),
    bit_efficiency_scales_with_compressor: (
        0.88,
        "Bit efficiency combines MI (estimated) and token count (direct). Both component "
        "trends are well-established. The 5.5x bits-per-token for 7B vs 1.5B Qwen-2.5 "
        "is the headline quantitative result."
    ),
    scaling_robust_to_conciseness_prompt: (
        0.87,
        "Tested across 3 different conciseness prompt levels (3, 6, 9 sentences) on "
        "LongHealth and FinanceBench. Consistency across prompt variants increases "
        "confidence in the core scaling findings."
    ),
    compressor_family_most_important: (
        0.83,
        "Based on logistic regression over correctness on LongHealth and FinanceBench. "
        "Feature importance analysis is standard but may be sensitive to collinearity "
        "between compressor size and family. Moderate-high confidence."
    ),

    # ── Deep Research results (Section 3.5) ───────────────────────────────────
    qwen14b_deep_research_result: (
        0.87,
        "RACE score and cost reported for Qwen-2.5-14B + GPT-4o on DeepResearch Bench. "
        "The 2.3% RACE improvement and 71.9% cost reduction are specific quantitative "
        "claims based on API pricing as of August 2025 — time-sensitive but documented."
    ),
    small_compressor_deep_research: (
        0.86,
        "3B compressor recovering 99% frontier accuracy at 26% API cost is the paper's "
        "practical demonstration on DeepResearch Bench. Confidence slightly lower than "
        "14B result because smaller models are more variable."
    ),

    # ── Methodological claims ──────────────────────────────────────────────────
    mi_estimator_practical: (
        0.93,
        "The estimator requiring only log probabilities is verifiable from the mathematical "
        "definition. Practical use of SGLang is demonstrated in the experiments. "
        "Very high confidence — definitional property of the estimator."
    ),
    mi_estimator_clipping: (
        0.93,
        "Clipping negative MI values to zero is a stated methodological choice. "
        "S=5 random seeds is verifiable experimental design. "
        "Definitional properties of the experimental setup."
    ),
    local_compute_trade: (
        0.90,
        "Consumer hardware capability (27B models on MacBook, Pixel phones) is supported "
        "by published benchmarks and memory estimates from Modal. High confidence in "
        "current-generation hardware facts; trends expected to continue."
    ),

    # ── Limitation claims ─────────────────────────────────────────────────────
    limitation_proxy_variance: (
        0.85,
        "Proxy model dependency at 1-3B scale is an acknowledged methodological "
        "limitation stated by the authors. Small model miscalibration is a widely "
        "recognized empirical phenomenon."
    ),

    # ── Context/framing claims ────────────────────────────────────────────────
    design_adhoc: (
        0.80,
        "The claim that agentic system design is largely ad hoc is a contextual "
        "framing supported by the absence of principled frameworks in the related work. "
        "Moderate-high confidence: characterizes field state, harder to verify precisely."
    ),
}
