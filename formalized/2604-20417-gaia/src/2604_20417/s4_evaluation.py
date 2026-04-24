"""Section 4: Evaluation — MSMARCO Experiments"""

from gaia.lang import claim, setting, support, deduction, abduction, compare, induction

from .motivation import (
    claim_few_relevant_common,
    claim_irrelevant_equidistant,
    claim_recall_misaligned,
    claim_anns_bounded_by_exact,
    setup_anns,
    setup_recall,
)
from .s2_semantic_recall import (
    claim_srecall_better_proxy,
    claim_llm_judging_efficient,
    defn_srecall,
    defn_semantic_neighbors,
    defn_judging_process,
    claim_srecall_hyperparameter_free,
)
from .s3_tolerant_recall import (
    claim_trecall_approximates_srecall,
    claim_trecall_mitigates_quantization,
    defn_trecall,
    defn_threshold_proxy,
    claim_threshold_proxy_effective,
)

# ── Settings: experimental setup ─────────────────────────────────────────────

setup_msmarco_exp = setting(
    "MSMARCO evaluation setup: 8.83M text documents encoded into 3072-dimensional "
    "embeddings using the Gemini Embedding model [@GeminiEmbed2025]. Query set: "
    "250 general-knowledge questions, encoded with the same model. Ground truth: "
    "top-100 nearest neighbors per query via brute-force inner product search "
    "(embeddings normalized so scores $\\in [-1, 1]$). Semantic neighbor labels: "
    "Gemini 2.5 [@Gemini25] used as judge, labeling each ground-truth neighbor "
    "'Relevant' or 'Not Relevant'. ANNS system: ScaNN [@ScaNN2020] with 8-bit "
    "quantization, retrieving top-100 results.",
    title="MSMARCO experiment setup"
)

# ── Claims: analysis of semantic neighbors ────────────────────────────────────

claim_sn_distribution_bimodal = claim(
    "The distribution of semantic neighbors per query in MSMARCO (250 queries, "
    "top-100 ground truth, Gemini 2.5 judge) is bimodal: approximately 40% of "
    "queries have 0-15 relevant documents (few-SN cluster), including 3 queries "
    "with zero relevant results, while another cluster appears near 90-100 "
    "relevant documents. The upper bound artifact arises from using only the "
    "top-100 ground truth — queries in the upper cluster likely have more than "
    "100 relevant documents in the full corpus.",
    title="MSMARCO SN distribution is bimodal",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 2", "caption": "Distribution of semantically relevant neighbors per query"}
)

claim_sn_higher_scores = claim(
    "Semantic neighbors (SN) achieve higher average inner product similarity scores "
    "than non-semantic neighbors (non-SN) across all query groups in MSMARCO. "
    "Specifically:\n\n"
    "| Query Group | N. Queries | Avg. score (SN) | Avg. score (non-SN) |\n"
    "|-------------|-----------|-----------------|---------------------|\n"
    "| All queries | 247       | 0.77 ± 0.02     | 0.73 ± 0.03         |\n"
    "| SN < 20     | 102       | 0.77 ± 0.03     | 0.71 ± 0.02         |\n"
    "| 20 ≤ SN < 80| 91        | 0.76 ± 0.02     | 0.74 ± 0.02         |\n"
    "| SN ≥ 80     | 54        | 0.77 ± 0.01     | 0.76 ± 0.02         |\n\n"
    "The largest gap between SN and non-SN average scores appears for queries "
    "with fewer than 20 SNs.",
    title="SN have higher similarity scores than non-SN",
    metadata={"source_table": "artifacts/2604.20417.pdf, Table 2"}
)

claim_sn_larger_deltas = claim(
    "Semantic neighbors exhibit significantly larger and more variable score "
    "differences (deltas between consecutive neighbors) than non-semantic neighbors "
    "in MSMARCO. Specifically:\n\n"
    "| Query Group | Avg. score delta (SN) | Avg. score delta (non-SN) |\n"
    "|-------------|----------------------|---------------------------|\n"
    "| All queries | 0.006 ± 0.006        | 0.002 ± 0.003             |\n"
    "| SN < 20     | 0.014 ± 0.012        | 0.001 ± 0.002             |\n"
    "| 20 ≤ SN < 80| 0.002 ± 0.003        | 0.001 ± 0.002             |\n"
    "| SN ≥ 80     | 0.001 ± 0.001        | 0.005 ± 0.006             |\n\n"
    "Non-SNs have consistently small score deltas, indicating near-equidistance.",
    title="SN have larger score deltas than non-SN",
    metadata={"source_table": "artifacts/2604.20417.pdf, Table 2"}
)

claim_cross_val_agreement = claim(
    "Cross-validation of 100 queries using Claude Haiku as an independent judge "
    "(outside the Gemini model family) showed an inter-judge agreement rate of "
    "91.1% (Cohen's $\\kappa = 0.82$). Agreement by category: 89.5% for "
    "'Relevant', 93.3% for 'Not Relevant'. Only 2 of 100 queries fell below "
    "70% agreement. When judges disagreed, Gemini more frequently labeled "
    "documents as 'Relevant' (more lenient), while Claude adhered more strictly "
    "to the prompt criteria [@Kuffo2026].",
    title="LLM judge cross-validation agreement (91.1%, κ=0.82)"
)

# ── Claims: main recall comparison ───────────────────────────────────────────

claim_recall_comparison_all = claim(
    "On MSMARCO (250 queries, ScaNN top-100 with 8-bit quantization), the three "
    "metrics compare as follows:\n\n"
    "| Query Group        | Traditional Recall | Semantic Recall | Tolerant Recall |\n"
    "|--------------------|-------------------|-----------------|------------------|\n"
    "| All queries        | 0.863 ± 0.177     | 0.932 ± 0.144   | 0.920 ± 0.125    |\n"
    "| SN < 20            | 0.762 ± 0.204     | 0.903 ± 0.183   | 0.859 ± 0.152    |\n"
    "| 20 ≤ SN < 80       | 0.903 ± 0.133     | 0.937 ± 0.124   | 0.941 ± 0.096    |\n"
    "| SN ≥ 80            | 0.976 ± 0.061     | 0.978 ± 0.062   | 0.991 ± 0.027    |\n\n"
    "Semantic recall is consistently higher than traditional recall, with the "
    "largest gap for queries with few semantic neighbors (SN < 20: 0.903 vs 0.762).",
    title="MSMARCO recall comparison table",
    metadata={"source_table": "artifacts/2604.20417.pdf, Table 3"}
)

claim_few_sn_penalized = claim(
    "Queries with few semantic neighbors (SN < 20) show the largest penalty under "
    "traditional recall: average traditional recall = 0.762 vs. semantic recall = "
    "0.903, a gap of 0.141. In contrast, for queries with many semantic neighbors "
    "(SN ≥ 80), the gap between traditional and semantic recall is negligible "
    "(0.976 vs. 0.978). This confirms that traditional recall's bias primarily "
    "affects queries where irrelevant neighbors dominate the ground truth "
    "[@Kuffo2026].",
    title="Few-SN queries are most penalized by traditional recall"
)

claim_srecall_better_end_user = claim(
    "Semantic recall better reflects search quality as perceived by end users "
    "compared to traditional recall. For top-100 search with ScaNN: semantic "
    "recall = 0.903 vs. traditional recall = 0.762 for queries with few SNs. "
    "For top-20 search: semantic recall = 0.901 vs. traditional recall = 0.869. "
    "The higher semantic recall scores reflect that the ANNS algorithm is actually "
    "retrieving most of the relevant results [@Kuffo2026].",
    title="Semantic recall better reflects end-user experience"
)

claim_rprecision_limitation = claim(
    "R-precision (which retrieves the top-$R$ results for a query with $R$ relevant "
    "objects) inadvertently penalizes ANNS algorithms for embedding model "
    "shortcomings. For example, if a query has $R = 3$ semantic neighbors and the "
    "third-ranked SN is ranked 4th in the exact NNS ground truth, R-precision "
    "counts this as an error even though exact NNS cannot retrieve it in the top-3. "
    "Semantic recall avoids this by allowing relevant documents to appear anywhere "
    "within the top-$k$ results. The rank-biserial correlation between ground-truth "
    "rank and semantic relevance is $-0.72$ ($p \\approx 0$) for queries with "
    "SN < 20, confirming the alignment is negative but imperfect [@Kuffo2026].",
    title="R-precision limitation vs semantic recall"
)

# ── Claims: quantization effect ──────────────────────────────────────────────

claim_quantization_reorders_irrelevant = claim(
    "8-bit scalar quantization introduces small relative score errors that can "
    "reorder near-equidistant irrelevant neighbors, causing traditional recall "
    "penalties. This effect is observed across MSMARCO, GloVe [@GloVe2014], and "
    "BigANN [@BigANN2022] datasets (Figure 4, artifacts/2604.20417.pdf). "
    "Tolerant recall mitigates this by allowing score-proximate replacements; "
    "semantic recall avoids it by considering only relevant results.",
    title="Quantization artifacts reorder irrelevant neighbors",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 4", "caption": "Distribution of error % between full precision and 8-bit quantization scores"}
)

# ── Strategies ────────────────────────────────────────────────────────────────

# Support for the claim that SN have higher scores (requires empirical evidence)
strat_sn_higher_scores = support(
    [claim_sn_higher_scores],
    claim_srecall_better_proxy,
    reason=(
        "The fact that semantic neighbors have higher average similarity scores than "
        "non-semantic neighbors (@claim_sn_higher_scores) implies that the embedding "
        "model does capture semantic relevance to a meaningful degree. This supports "
        "the validity of using exact NNS as a filter: it selects the most relevant "
        "items from the corpus, and semantic recall measures retrieval of those items."
    ),
    prior=0.82
)

# Few-SN queries are most penalized
strat_few_sn_penalized = support(
    [claim_recall_comparison_all, claim_sn_larger_deltas],
    claim_few_sn_penalized,
    reason=(
        "The recall comparison table (@claim_recall_comparison_all) shows the largest "
        "gap between traditional and semantic recall for queries with SN < 20 (0.762 "
        "vs. 0.903). The large score deltas among SNs and small deltas among non-SNs "
        "(@claim_sn_larger_deltas) explain this: for few-SN queries, most of the "
        "top-100 neighbors are irrelevant and near-equidistant, causing frequent "
        "ANNS misses penalized by traditional recall but not by semantic recall "
        "[@Kuffo2026]."
    ),
    prior=0.92
)

strat_srecall_end_user = support(
    [claim_recall_comparison_all, claim_few_sn_penalized],
    claim_srecall_better_end_user,
    reason=(
        "The recall comparison (@claim_recall_comparison_all) shows semantic recall "
        "consistently closer to 1.0 than traditional recall, particularly for "
        "few-SN queries (@claim_few_sn_penalized). Since few-SN queries are the "
        "ones most penalized by irrelevant-neighbor noise, the higher semantic recall "
        "reflects that the ANNS algorithm does find the relevant content — the "
        "traditional recall penalty was noise [@Kuffo2026]."
    ),
    prior=0.90
)

# Abduction: which metric better reflects semantic quality?
# H = semantic recall correctly measures quality
# Alt = traditional recall is equally valid
# Observation = large gap (0.141) between traditional and semantic recall for SN<20 queries

h_srecall_correct = claim(
    "Semantic recall correctly captures retrieval quality because it excludes "
    "irrelevant neighbors from its denominator, making it insensitive to the "
    "near-equidistance of irrelevant objects.",
    title="Hypothesis: semantic recall is the correct quality metric"
)

alt_traditional_valid = claim(
    "Traditional recall is an equally valid measure of retrieval quality: both "
    "relevant and irrelevant nearest neighbors should be penalized equally when "
    "missed, because mathematical proximity is a valid proxy for semantic relevance.",
    title="Alternative: traditional recall is equally valid"
)

# Observation: the measured gap in recall scores for few-SN queries
obs_recall_gap = claim(
    "For MSMARCO queries with fewer than 20 semantic neighbors (SN < 20), "
    "traditional recall = 0.762 while semantic recall = 0.903, a gap of 0.141. "
    "This gap is absent for queries with many SNs (SN ≥ 80: 0.976 vs. 0.978).",
    title="Observed recall gap for few-SN queries"
)

pred_h_metric = claim(
    "If semantic recall correctly captures quality (@h_srecall_correct), then "
    "semantic recall scores should be substantially higher than traditional recall "
    "for few-SN queries, because traditional recall penalizes missed irrelevant "
    "near-equidistant neighbors that semantic recall ignores."
)

pred_alt_metric = claim(
    "If traditional recall is equally valid (@alt_traditional_valid), then "
    "traditional and semantic recall should yield similar scores across all query "
    "types, with no systematic advantage for semantic recall on few-SN queries."
)

comp_metric_quality = compare(
    pred_h_metric,
    pred_alt_metric,
    obs_recall_gap,
    reason=(
        "The observed gap of 0.141 for few-SN queries and its absence for high-SN "
        "queries matches exactly what the semantic recall hypothesis predicts and "
        "is incompatible with the traditional recall equivalence hypothesis "
        "[@Kuffo2026]."
    ),
    prior=0.91
)

s_h_metric = support(
    [h_srecall_correct], obs_recall_gap,
    reason=(
        "If @h_srecall_correct, the near-equidistance of irrelevant neighbors "
        "causes traditional recall penalties for few-SN queries that semantic "
        "recall avoids, predicting the observed recall gap (@obs_recall_gap)."
    ),
    prior=0.88
)

s_alt_metric = support(
    [alt_traditional_valid], obs_recall_gap,
    reason=(
        "If @alt_traditional_valid, both metrics should track similarly since "
        "all nearest neighbors are equally weighted — this alternative cannot "
        "explain the observed 0.141 gap for few-SN queries."
    ),
    prior=0.20
)

abduction_metric_quality = abduction(
    s_h_metric, s_alt_metric, comp_metric_quality,
    reason=(
        "Both hypotheses attempt to explain the observed recall gap for few-SN "
        "queries. Semantic recall's mechanism directly predicts this gap; the "
        "traditional recall equivalence view cannot account for it."
    )
)

strat_quantization = support(
    [claim_sn_larger_deltas, claim_irrelevant_equidistant],
    claim_quantization_reorders_irrelevant,
    reason=(
        "Since non-SNs have consistently small score deltas (@claim_sn_larger_deltas, "
        "@claim_irrelevant_equidistant), quantization errors (even small ones) are "
        "sufficient to reorder them. This reordering causes traditional recall "
        "penalties since ground-truth positions shift. Tolerant recall absorbs "
        "these small reorderings; semantic recall ignores non-SNs entirely "
        "[@Quantization2025]."
    ),
    prior=0.87
)

strat_rprecision = support(
    [claim_anns_bounded_by_exact],
    claim_rprecision_limitation,
    reason=(
        "R-precision assumes the ground-truth rank aligns with semantic relevance. "
        "But since ANNS is bounded by exact NNS (@claim_anns_bounded_by_exact), "
        "a semantically relevant item ranked 4th in exact NNS cannot be retrieved "
        "in the top-3 by any ANNS algorithm. R-precision treats this as a penalty "
        "even though it is physically impossible to avoid. Semantic recall's "
        "denominator ($SN$) only includes items within the top-$k$ window, so it "
        "cannot penalize for items the algorithm is incapable of retrieving "
        "[@Kuffo2026]."
    ),
    prior=0.93,
    background=[defn_srecall]
)

# LLM judging cross-validation supports reliability of the judging methodology
strat_cross_val = support(
    [claim_cross_val_agreement],
    claim_llm_judging_efficient,
    reason=(
        "Inter-judge agreement of 91.1% ($\\kappa = 0.82$) between Gemini and "
        "Claude Haiku (@claim_cross_val_agreement) demonstrates that LLM-based "
        "judging is reliable and consistent across model families. This validates "
        "the judging methodology used to produce the semantic neighbor labels "
        "upon which all semantic recall results depend [@Kuffo2026]."
    ),
    prior=0.88
)
