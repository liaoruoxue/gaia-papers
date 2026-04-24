"""Section 4.3: Tuning for Semantic Recall — Cost-Quality Tradeoffs"""

from gaia.lang import claim, setting, support, compare, abduction, induction

from .motivation import (
    claim_recall_misaligned,
    setup_anns,
)
from .s2_semantic_recall import (
    claim_srecall_better_proxy,
    claim_srecall_hyperparameter_free,
    defn_srecall,
)
from .s3_tolerant_recall import (
    claim_trecall_approximates_srecall,
    defn_trecall,
)
from .s4_evaluation import (
    claim_few_sn_penalized,
    claim_srecall_better_end_user,
    setup_msmarco_exp,
)

# ── Settings ──────────────────────────────────────────────────────────────────

setup_tuning_exp = setting(
    "Tuning experiment setup: Google Vizier [@Vizier2017] used to optimize ScaNN "
    "[@ScaNN2020] hyperparameters on MSMARCO, minimizing 'bytes read' (which "
    "closely correlates with the number of inner product computations [@ScaNN2020]) "
    "subject to a fixed target recall value. CPU cost of query processing used "
    "as the final performance measure.",
    title="Hyperparameter tuning experiment setup"
)

# ── Claims: tuning results ────────────────────────────────────────────────────

claim_tuning_baseline = claim(
    "Tuning ScaNN [@ScaNN2020] for a target traditional recall of 98% on MSMARCO "
    "using Google Vizier [@Vizier2017] yields a Pareto-optimal configuration that "
    "achieves: traditional recall = 98%, tolerant recall = 98.69%, semantic recall "
    "= 98.93%. This configuration serves as the baseline for cost comparisons "
    "[@Kuffo2026].",
    title="Tuning baseline: 98% traditional recall configuration"
)

claim_tuning_tolerant_saves_5pct = claim(
    "Re-tuning ScaNN for a target tolerant recall of 98.69% (matching the baseline "
    "tolerant recall level) yields a configuration with the same tolerant recall "
    "at 5% lower search cost compared to the traditional-recall-tuned baseline "
    "[@Kuffo2026].",
    title="Tuning for tolerant recall saves 5% cost at same quality"
)

claim_tuning_semantic_saves_14pct = claim(
    "Re-tuning ScaNN for a target semantic recall of 98.93% (matching the baseline "
    "semantic recall level) yields a configuration that preserves semantic recall "
    "while reducing search cost by 14% compared to the traditional-recall-tuned "
    "baseline [@Kuffo2026].",
    title="Tuning for semantic recall saves 14% cost at same quality"
)

claim_tuning_95pct_target = claim(
    "Tuning for a 95% target using tolerant recall instead of traditional recall "
    "yields the following cost reductions (compared to tuning for 95% traditional "
    "recall):\n\n"
    "| Dataset | Cost Reduction |\n"
    "|---------|----------------|\n"
    "| BigANN (1B vectors, 128-dim) | ~25% |\n"
    "| GloVe (1M vectors, 100-dim)  | ~5%  |\n"
    "| MSMARCO                       | ~35% |\n\n"
    "These gains arise because non-semantic neighbors are harder to retrieve in "
    "partition-based indexes: they require exploring additional partitions, "
    "increasing search effort without improving semantic quality [@Kuffo2026].",
    title="95% tolerant recall tuning: 5-35% cost reduction across datasets",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 5", "caption": "Recall vs cost: Cost rises sharply as recall increases"}
)

claim_cost_rises_sharply = claim(
    "Search cost rises sharply as recall approaches 1.0 (Figure 5, "
    "artifacts/2604.20417.pdf). This super-linear cost-recall relationship means "
    "that even small reductions in the target recall (e.g., by using a metric "
    "that accurately represents semantic quality rather than mathematical exactness) "
    "yield substantial compute cost savings.",
    title="Cost-recall curve is super-linear near high recall",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 5", "caption": "Figure 5: Recall vs cost curve"}
)

claim_non_sn_harder_to_retrieve = claim(
    "Non-semantic neighbors are harder to retrieve than semantic neighbors in "
    "partition-based ANNS indexes (e.g., ScaNN [@ScaNN2020]). Because non-SNs "
    "are nearly equidistant and not strongly associated with any partition, "
    "retrieving them requires exploring additional partitions beyond what would "
    "suffice to retrieve all SNs. This is the mechanism by which tuning for "
    "semantic or tolerant recall yields cost savings.",
    title="Non-semantic neighbors are harder to retrieve (require more partitions)"
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_tolerant_saves = support(
    [claim_tuning_baseline, claim_non_sn_harder_to_retrieve],
    claim_tuning_tolerant_saves_5pct,
    reason=(
        "Starting from the baseline configuration tuned for 98% traditional recall "
        "(@claim_tuning_baseline), re-tuning for 98.69% tolerant recall (the same "
        "tolerant recall the baseline already achieves) allows the optimizer to "
        "find configurations that skip unnecessary retrieval of near-equidistant "
        "irrelevant neighbors (@claim_non_sn_harder_to_retrieve). The 5% cost "
        "reduction directly demonstrates that the baseline wastes effort on such "
        "neighbors [@Kuffo2026]."
    ),
    prior=0.90,
    background=[setup_tuning_exp]
)

strat_semantic_saves = support(
    [claim_tuning_baseline, claim_non_sn_harder_to_retrieve],
    claim_tuning_semantic_saves_14pct,
    reason=(
        "Starting from the baseline (@claim_tuning_baseline), tuning for 98.93% "
        "semantic recall (the same semantic recall the baseline achieves) allows "
        "the optimizer to avoid the extra partition exploration required by non-SNs "
        "(@claim_non_sn_harder_to_retrieve). The 14% cost reduction (larger than "
        "the 5% from tolerant tuning) reflects that semantic recall more precisely "
        "excludes non-SNs from the objective function [@Kuffo2026]."
    ),
    prior=0.90,
    background=[setup_tuning_exp]
)

strat_95pct_savings = support(
    [claim_cost_rises_sharply, claim_non_sn_harder_to_retrieve],
    claim_tuning_95pct_target,
    reason=(
        "Because cost rises sharply at high recall (@claim_cost_rises_sharply) and "
        "non-SNs require extra retrieval effort (@claim_non_sn_harder_to_retrieve), "
        "switching the 95% target from traditional to tolerant recall shifts the "
        "effective operating point leftward on the cost-recall curve, yielding "
        "disproportionate cost savings. The larger savings on MSMARCO vs. GloVe "
        "reflect more severe few-SN query distributions in MSMARCO [@Kuffo2026]."
    ),
    prior=0.88,
    background=[setup_tuning_exp]
)

# Induction over datasets: tolerant recall tuning consistently saves cost
obs_bigann = claim(
    "Tuning ScaNN for 95% tolerant recall (vs. 95% traditional recall) on BigANN "
    "(1 billion vectors, 128 dimensions) reduces search cost by approximately 25%."
)

obs_glove = claim(
    "Tuning ScaNN for 95% tolerant recall (vs. 95% traditional recall) on GloVe "
    "(1 million vectors, 100 dimensions) reduces search cost by approximately 5%."
)

obs_msmarco_cost = claim(
    "Tuning ScaNN for 95% tolerant recall (vs. 95% traditional recall) on MSMARCO "
    "(8.83 million documents, 3072 dimensions) reduces search cost by approximately 35%."
)

law_tolerant_saves_cost = claim(
    "Across diverse datasets and scales, tuning ANNS hyperparameters for tolerant "
    "recall (or semantic recall) as the optimization objective rather than "
    "traditional recall consistently yields cost savings at the same semantic "
    "quality level, because non-semantic neighbors require disproportionately more "
    "search effort.",
    title="Tolerant/semantic recall tuning consistently saves cost"
)

s_bigann = support(
    [law_tolerant_saves_cost], obs_bigann,
    reason="law predicts BigANN cost savings from tolerant tuning", prior=0.88
)
s_glove = support(
    [law_tolerant_saves_cost], obs_glove,
    reason="law predicts GloVe cost savings from tolerant tuning", prior=0.88
)
s_msmarco_c = support(
    [law_tolerant_saves_cost], obs_msmarco_cost,
    reason="law predicts MSMARCO cost savings from tolerant tuning", prior=0.88
)

ind_bigann_glove = induction(
    s_bigann, s_glove, law=law_tolerant_saves_cost,
    reason="BigANN (1B, 128-dim) and GloVe (1M, 100-dim) are independent datasets with different scales"
)
ind_all_datasets = induction(
    ind_bigann_glove, s_msmarco_c, law=law_tolerant_saves_cost,
    reason="MSMARCO (8.83M, 3072-dim) provides a third independent dataset confirming the law"
)
