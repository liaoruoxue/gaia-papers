"""Section 6-7: Discussion and Conclusions"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    claim_recall_misaligned,
    claim_few_relevant_common,
    claim_irrelevant_equidistant,
    setup_anns,
)
from .s2_semantic_recall import (
    claim_srecall_better_proxy,
    claim_srecall_requires_raw_data,
    claim_srecall_undefined_no_relevant,
    defn_srecall,
)
from .s3_tolerant_recall import (
    claim_trecall_approximates_srecall,
    claim_trecall_robust_dynamic,
    claim_trecall_mitigates_quantization,
    claim_trecall_has_hyperparameter,
)
from .s4_evaluation import (
    claim_srecall_better_end_user,
    claim_few_sn_penalized,
    claim_quantization_reorders_irrelevant,
)
from .s4b_tuning import (
    claim_tuning_semantic_saves_14pct,
    claim_tuning_tolerant_saves_5pct,
    law_tolerant_saves_cost,
    claim_cost_rises_sharply,
)
from .s5_generalizability import (
    claim_metrics_generalize,
)

# ── Claims: discussion ────────────────────────────────────────────────────────

claim_traditional_optimizes_noise = claim(
    "Optimizing ANNS hyperparameters for traditional recall is equivalent to "
    "optimizing for 'mathematical exactness at unnecessary extra retrieval cost': "
    "configurations selected for high traditional recall must incur extra search "
    "effort to retrieve near-equidistant irrelevant neighbors, which does not "
    "improve end-user experience. The long-tailed distributions of traditional "
    "recall reported in prior ANNS work [@DARTH2025; @VIBE2025] likely stem from "
    "queries with few or no relevant neighbors.",
    title="Traditional recall tuning optimizes for noise"
)

claim_binary_relevance_simplification = claim(
    "The binary relevance judgment (Relevant / Not Relevant) used in semantic "
    "recall collapses uncertainty into a hard decision, delegating the confidence "
    "threshold to the judge. This simplification favors reproducibility and "
    "tractability, but richer graded judgments could capture more nuance. "
    "Errors in judgment are unavoidable, and correlations between the judge and "
    "the evaluated system may occur in some scenarios [@Kuffo2026].",
    title="Binary relevance assumption is a simplification"
)

claim_llm_domain_limitation = claim(
    "LLM-based semantic neighbor identification relies on the LLM's knowledge: "
    "for domain-specific datasets (e.g., specialized medical or legal corpora), "
    "the LLM may lack sufficient domain expertise, potentially requiring human "
    "expert validation. This limits the automation benefit of LLM judging for "
    "niche domains [@Kuffo2026].",
    title="LLM judging limited for domain-specific datasets"
)

claim_future_early_termination = claim(
    "Future work should incorporate semantic recall and tolerant recall into "
    "early-termination mechanisms for ANNS [@DARTH2025], allowing search to stop "
    "once sufficient semantic neighbors have been retrieved rather than continuing "
    "to search for near-equidistant irrelevant neighbors.",
    title="Future work: semantic recall in early-termination ANNS"
)

claim_relaxing_precision = claim(
    "ANNS evaluation can relax strict mathematical precision in favor of improved "
    "search efficiency without compromising retrieval quality more than previously "
    "thought, because performance losses that reshuffle only irrelevant results "
    "do not affect end-user experience. Semantic and tolerant recall enable "
    "developers to distinguish between meaningful performance losses (affecting "
    "relevant results) and noise (reshuffling irrelevant ones) [@Kuffo2026].",
    title="ANNS evaluation can relax mathematical precision"
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_traditional_noise = support(
    [claim_few_sn_penalized, claim_cost_rises_sharply],
    claim_traditional_optimizes_noise,
    reason=(
        "Because traditional recall penalizes algorithms for missing irrelevant "
        "neighbors (@claim_few_sn_penalized) and cost rises sharply at high recall "
        "(@claim_cost_rises_sharply), configurations tuned for high traditional "
        "recall must spend disproportionate effort on irrelevant neighbors. This "
        "wasted effort is 'optimizing for noise' — it satisfies the metric without "
        "improving semantic quality [@DARTH2025; @VIBE2025]."
    ),
    prior=0.88,
    background=[setup_anns]
)

strat_relaxing = support(
    [claim_tuning_semantic_saves_14pct, claim_tuning_tolerant_saves_5pct,
     claim_srecall_better_end_user],
    claim_relaxing_precision,
    reason=(
        "The 14% cost saving from semantic recall tuning "
        "(@claim_tuning_semantic_saves_14pct) and 5% from tolerant recall tuning "
        "(@claim_tuning_tolerant_saves_5pct), combined with higher semantic quality "
        "scores (@claim_srecall_better_end_user), demonstrate that relaxing "
        "mathematical exactness (not retrieving every near-equidistant irrelevant "
        "neighbor) preserves or improves semantic quality while reducing cost "
        "[@Kuffo2026]."
    ),
    prior=0.92
)
