"""Section 3: Empirical Results — Scaling, MI Correlation, and Deep Research"""

from gaia.lang import (
    claim, setting, support, deduction, compare, abduction, induction, complement
)
from .motivation import (
    compressor_predictor_pattern,
    compressor_scaling_dominates,
    deep_research_cost_reduction,
    rq_compressor_vs_predictor,
    rq_mi_proxy,
    rq_deep_research,
    mi_as_proxy_proposal,
)
from .s2_framework import (
    experimental_datasets,
    compressor_model_families,
    predictor_models,
    mc_estimator_def,
    bit_efficiency_def,
    rate_distortion_def,
    flops_per_generation_def,
    gaussian_rd_qualitative,
    proxy_consistency,
)

# ── Section 3.1: Compressor vs Predictor Scaling ──────────────────────────────

accuracy_scales_with_compressor = claim(
    "Downstream QA accuracy increases strongly with compressor size. On LongHealth, 7-8B compressors "
    "are up to 3.1x more accurate than 1-1.5B compressors, and surpass the GPT-4o-only baseline "
    "(no compression) by 4 percentage points. On FinanceBench, 7-8B compressors are up to 2.6x more "
    "accurate than 1-1.5B compressors and recover 97% of the GPT-4o-only baseline accuracy. "
    "The same scaling behavior holds for Gemma-3 models.",
    title="Accuracy scales with compressor size",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 2 (Left): Downstream accuracy vs compressor model size on LongHealth and FinanceBench",
        "source_section": "Section 3.1",
    },
)

larger_compressors_more_concise = claim(
    "Larger compressor models are more token-efficient: 7-12B compressors produce outputs up to 4.6x "
    "shorter than their 1-1.5B counterparts within the same model family, without sacrificing accuracy. "
    "Qwen-2.5 models are more concise than Llama and Gemma-3 models, indicating that model families "
    "differ substantially in their compression communication profiles.",
    title="Larger compressors produce shorter outputs",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 2 (Middle): Compression length vs compressor model size",
        "source_section": "Section 3.1",
    },
)

flops_sublinear_with_compressor = claim(
    "FLOPs-per-generation scale sublinearly with compressor model size because larger compressors "
    "generate fewer tokens. For Qwen-2.5, scaling from 1.5B to 7B parameters increases "
    "FLOPs-per-generation by only 1.3% on LongHealth. Different model families exhibit distinct "
    "scaling behaviors in FLOPs-per-generation.",
    title="FLOPs-per-generation scale sublinearly with compressor size",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 2 (Right): GFLOPs-per-compression vs compressor model size",
        "source_section": "Section 3.1",
    },
)

predictor_scaling_marginal = claim(
    "Scaling the predictor LM provides only marginal accuracy improvements once a baseline predictor "
    "capacity (approximately 8B-70B parameters) is reached. The accuracy gain from increasing the "
    "predictor from 70B to 405B is within 12% on LongHealth and within 1% on FinanceBench.",
    title="Predictor scaling yields marginal gains beyond 70B",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 3: Scaling compressors vs predictors on LongHealth",
        "source_section": "Section 3.1",
    },
)

compressor_family_most_important = claim(
    "Logistic regression predicting per-sample binary correctness on LongHealth and FinanceBench "
    "reveals that compressor model family is the single most important factor in downstream accuracy, "
    "with Qwen-2.5 compressors outperforming Llama. Scaling the compressor size matters substantially "
    "more than scaling the predictor size.",
    title="Compressor family is the most important design factor",
    metadata={"source_section": "Section 3.4"},
)

compressor_error_taxonomy = claim(
    "Errors in the compression step fall into three categories: "
    "(a) compression contains an incorrect answer: 36.3% of compressor errors; "
    "(b) compression contains no answer: 33.3% of compressor errors; "
    "(c) compression omits necessary details: 30.4% of compressor errors. "
    "These categories are roughly equally distributed.",
    title="Compressor error taxonomy (three categories)",
    metadata={"source_section": "Section 3.1, Appendix D.7"},
)

local_compute_trade = claim(
    "Consumer hardware (Google Pixel phones, Apple MacBook laptops) can now run open-weight LMs "
    "up to 27B parameters without aggressive quantization under FP16 precision. This enables "
    "front-loading computation into local compressors to reduce cloud serving costs for predictors.",
    title="Local hardware can host 27B-parameter compressors",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 1 (Right): LM sizes runnable on consumer hardware",
        "source_section": "Section 3.1",
    },
)

# ── Section 3.2: MI and Bit Efficiency ─────────────────────────────────────────

mi_scales_with_compressor = claim(
    "Estimated conditional mutual information I_hat(X; Z | Q) increases with compressor model size "
    "across all evaluated model families (Llama-3, Qwen-2.5, Gemma-3) and datasets. "
    "On LongHealth, Qwen-2.5 and Gemma-3 compressions saturate in mutual information at the "
    "largest model sizes, while Llama compressors are far from the theoretical maximum log(N). "
    "On FinanceBench, MI saturation occurs already at the 3B scale.",
    title="Mutual information scales with compressor size",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 4 (Left): Mutual information vs compressor model size on LongHealth",
        "source_section": "Section 3.2",
    },
)

bit_efficiency_scales_with_compressor = claim(
    "Bit efficiency (bits of mutual information per output token, R = I(X; Z | Q) / L) increases "
    "with compressor model size. This is doubly driven: larger compressors carry more mutual "
    "information AND generate fewer tokens, amplifying bit efficiency gains. "
    "A 7B Qwen-2.5 compressor conveys 5.5x more bits per token than the 1.5B counterpart.",
    title="Bit efficiency scales with compressor size",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 4 (Right): Bit efficiency vs compressor model size on LongHealth",
        "source_section": "Section 3.2",
    },
)

scaling_robust_to_conciseness_prompt = claim(
    "Compressor scaling trends in accuracy, compute cost, MI, and bit efficiency are consistent "
    "across different conciseness instructions (3, 6, or 9 sentences). Compressors instructed "
    "to be more concise are more token-efficient and thus compute-efficient, but the relative "
    "improvements from larger compressors persist regardless of prompted output length.",
    title="Compressor scaling robust to conciseness prompt instructions",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 5: Scaling behavior across instructed conciseness levels",
        "source_section": "Section 3.2",
    },
)

# ── Section 3.3: MI Correlates with Downstream Performance ────────────────────

mi_correlates_with_accuracy = claim(
    "Rate-distortion curves fit with exponential decay functions D(R) = C * exp(-b*R) + D_0 "
    "show strong correlation between bit efficiency R and distortion D (1 - accuracy) across "
    "both compressor families (Qwen-2.5 and Llama) and all predictor sizes on LongHealth. "
    "The fitted curves confirm that scaling predictors beyond 70B yields only marginal distortion reduction.",
    title="MI rate-distortion curves fit accuracy data",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 6 (Left): Rate-distortion curves for Llama compressors on LongHealth",
        "source_section": "Section 3.3",
    },
)

mi_correlates_with_perplexity = claim(
    "Mutual information estimated from Llama compressors on FineWeb is strongly negatively "
    "correlated with predictor perplexity: Pearson r = -0.84, R-squared = 0.71. "
    "Higher MI in the compression corresponds to lower predictor perplexity on the held-out text.",
    title="MI strongly correlated with perplexity (r=-0.84) on FineWeb",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 6 (Right): MI vs perplexity for Llama compressors on FineWeb",
        "source_section": "Section 3.3",
    },
)

predictor_family_independence = claim(
    "Further rate-distortion analysis across Qwen-2.5 and Llama compressors reveals that "
    "distortion is primarily determined by compressor model family and size, not by whether "
    "the predictor is from the same model family as the compressor. Predictors do not "
    "perform better when paired with compressors of the same family.",
    title="Predictor performance independent of compressor-predictor family match",
    metadata={"source_section": "Section 3.3"},
)

# ── Section 3.5: Deep Research ────────────────────────────────────────────────

deep_research_setup = setting(
    "The Deep Research evaluation uses DeepResearch Bench [@Du2025], which assesses system "
    "performance across four dimensions: Comprehensiveness, Depth, Instruction-following, and "
    "Readability, combined into a RACE (Reference-based Adaptive Criteria Evaluation) score. "
    "The pipeline: a predictor LM decomposes research tasks into subtasks executed by compressors "
    "in parallel; results are aggregated into a final report. Costs are based on GPT-4o API rates "
    "as of August 2025 ($2.50/1M input tokens, $10.00/1M output tokens).",
    title="Deep Research evaluation setup (DeepResearch Bench)",
)

qwen14b_deep_research_result = claim(
    "A Qwen-2.5-14B compressor paired with a GPT-4o predictor achieves a RACE score 2.3% higher "
    "than the uncompressed baseline (providing raw web search data to GPT-4o), at only 28.1% of "
    "the API cost of the uncompressed baseline — a cost reduction of 71.9%.",
    title="Qwen-2.5-14B achieves +2.3% RACE at 28.1% cost",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 7 (Left): RACE score vs cost for GPT-4o predictor with Qwen-2.5 compressors",
        "source_section": "Section 3.5",
    },
)

small_compressor_deep_research = claim(
    "Qwen-2.5 compressors as small as 3B parameters paired with GPT-4o predictors recover 99% of "
    "frontier-LM accuracy (GPT-4o uncompressed baseline) on DeepResearch Bench at 26% of the "
    "API cost (74% cost reduction).",
    title="3B compressor achieves 99% frontier accuracy at 26% API cost",
    metadata={
        "figure": "artifacts/2512.21720.pdf",
        "caption": "Fig. 7: Deep Research Scaling Results",
        "source_section": "Section 3.5",
    },
)

deep_research_predictor_scaling = claim(
    "In the Deep Research pipeline, larger predictor models consistently improve RACE scores, "
    "while larger compressors provide substantial performance gains at minimal additional API costs. "
    "Both compressor and predictor scaling contribute, but compressors provide larger gains per "
    "unit of additional API spend.",
    title="Deep Research: both axes improve RACE, compressors more cost-efficient",
    metadata={"source_section": "Section 3.5"},
)

# ── Strategies: Compressor scaling ────────────────────────────────────────────

strat_accuracy_conciseness_combine = support(
    [accuracy_scales_with_compressor, larger_compressors_more_concise],
    flops_sublinear_with_compressor,
    reason=(
        "Since larger compressors are both more accurate (@accuracy_scales_with_compressor) "
        "and more concise (@larger_compressors_more_concise), the total FLOPs-per-generation "
        "scales sublinearly: the increase in parameters (and thus FLOPs/token) is partially "
        "offset by the decrease in output token count. For Qwen-2.5, this near-cancellation "
        "means that going from 1.5B to 7B costs only 1.3% more FLOPs on LongHealth."
    ),
    prior=0.88,
)

strat_compressor_vs_predictor = compare(
    accuracy_scales_with_compressor,
    predictor_scaling_marginal,
    compressor_scaling_dominates,
    reason=(
        "The two alternatives are: (H) scaling compressors drives performance "
        "(@accuracy_scales_with_compressor: 3.1x accuracy gain, LongHealth), and "
        "(Alt) scaling predictors drives performance "
        "(@predictor_scaling_marginal: <12% gain from 70B to 405B). "
        "At fixed total compute, compressor scaling yields steeper accuracy improvements. "
        "The observation (@compressor_scaling_dominates) matches the compressor-scaling hypothesis "
        "far better: equal FLOPs in the compressor yield dramatically larger returns."
    ),
    prior=0.90,
)

strat_h_compressor = support(
    [accuracy_scales_with_compressor],
    compressor_scaling_dominates,
    reason=(
        "The accuracy gains from compressor scaling (@accuracy_scales_with_compressor: up to 3.1x "
        "improvement) directly support the claim that compressor scaling dominates system performance. "
        "The evidence is consistent across three model families (Llama-3, Qwen-2.5, Gemma-3) and "
        "two datasets (LongHealth, FinanceBench)."
    ),
    prior=0.88,
)

strat_alt_predictor = support(
    [predictor_scaling_marginal],
    compressor_scaling_dominates,
    reason=(
        "The marginal returns from predictor scaling (@predictor_scaling_marginal: <12% gain "
        "from 70B to 405B on LongHealth) undermine the alternative hypothesis that predictor "
        "scaling drives performance. They provide indirect support that compressor scaling "
        "is the dominant lever, since the alternative explanation (scale the predictor) fails."
    ),
    prior=0.35,
)

abd_compressor_dominance = abduction(
    strat_h_compressor,
    strat_alt_predictor,
    strat_compressor_vs_predictor,
    reason=(
        "The observation is that scaling compressors improves accuracy far more than scaling predictors "
        "at matched compute budgets. Two hypotheses: (H) compressor scaling dominates, (Alt) predictor "
        "scaling drives gains. The compressor scaling evidence (@accuracy_scales_with_compressor) is "
        "3.1x on LongHealth; the predictor scaling evidence is marginal (@predictor_scaling_marginal). "
        "Abduction selects the better explanation: compressor scaling."
    ),
)

# ── Strategies: MI as proxy ────────────────────────────────────────────────────

strat_mi_predicts_accuracy = support(
    [mi_scales_with_compressor, bit_efficiency_scales_with_compressor],
    mi_correlates_with_accuracy,
    reason=(
        "Since MI increases with compressor size (@mi_scales_with_compressor) and bit efficiency "
        "also increases (@bit_efficiency_scales_with_compressor), and since accuracy is also "
        "higher for larger compressors, the rate-distortion framework (@rate_distortion_def) "
        "predicts that fitting D(R) curves should reveal a strong inverse relationship. "
        "The exponential-decay fit on rate-distortion data confirms this quantitatively."
    ),
    prior=0.85,
)

strat_mi_predicts_perplexity = support(
    [mi_scales_with_compressor],
    mi_correlates_with_perplexity,
    background=[mc_estimator_def],
    reason=(
        "MI (estimated via the MC estimator @mc_estimator_def) measures information preserved in "
        "the compression. Since MI scales with compressor size (@mi_scales_with_compressor), and "
        "perplexity under a separate Llama-3.1-8B model measures how predictable the compressed "
        "text is as a substitute for the original, higher MI should correspond to lower perplexity. "
        "On FineWeb with Llama compressors, this yields r=-0.84, R^2=0.71 — "
        "strong empirical confirmation of MI as a task-agnostic performance proxy."
    ),
    prior=0.82,
)

strat_mi_proxy_confirmed = support(
    [mi_correlates_with_accuracy, mi_correlates_with_perplexity, proxy_consistency],
    mi_as_proxy_proposal,
    reason=(
        "MI predicts downstream accuracy (via rate-distortion: @mi_correlates_with_accuracy), "
        "predicts perplexity (r=-0.84: @mi_correlates_with_perplexity), and is robust to proxy "
        "model choice (@proxy_consistency). Together these provide strong empirical validation "
        "that MI is a reliable task-agnostic proxy for compression quality [@He2025]."
    ),
    prior=0.87,
)

# ── Strategies: Deep Research ─────────────────────────────────────────────────

strat_deep_research_validates = support(
    [qwen14b_deep_research_result, small_compressor_deep_research],
    deep_research_cost_reduction,
    reason=(
        "The Deep Research experiment directly validates the cost-reduction principle: "
        "a Qwen-2.5-14B compressor achieves +2.3% RACE at 28.1% cost (@qwen14b_deep_research_result), "
        "and a 3B compressor recovers 99% accuracy at 26% cost (@small_compressor_deep_research). "
        "Both results confirm the abstract's 74% cost-reduction claim under real API pricing "
        "conditions (GPT-4o rates, August 2025)."
    ),
    prior=0.90,
)

strat_local_hardware_enables = support(
    [local_compute_trade, flops_sublinear_with_compressor],
    compressor_scaling_dominates,
    reason=(
        "Consumer hardware can now host up to 27B-parameter compressors (@local_compute_trade), "
        "and FLOPs-per-generation scale sublinearly with compressor size (@flops_sublinear_with_compressor). "
        "This means that front-loading compute into local compressors is both technically feasible "
        "and economically rational: larger on-device compressors reduce cloud predictor serving costs "
        "while providing the dominant performance gains."
    ),
    prior=0.80,
)

__all__ = [
    "accuracy_scales_with_compressor",
    "larger_compressors_more_concise",
    "flops_sublinear_with_compressor",
    "predictor_scaling_marginal",
    "compressor_family_most_important",
    "compressor_error_taxonomy",
    "local_compute_trade",
    "mi_scales_with_compressor",
    "bit_efficiency_scales_with_compressor",
    "scaling_robust_to_conciseness_prompt",
    "mi_correlates_with_accuracy",
    "mi_correlates_with_perplexity",
    "predictor_family_independence",
    "qwen14b_deep_research_result",
    "small_compressor_deep_research",
    "deep_research_predictor_scaling",
]
