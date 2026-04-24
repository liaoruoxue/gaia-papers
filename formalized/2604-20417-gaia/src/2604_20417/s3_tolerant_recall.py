"""Section 3: Tolerant Recall — Proxy Metric Definition"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    claim_irrelevant_equidistant,
    setup_anns,
    setup_recall,
)
from .s2_semantic_recall import (
    claim_srecall_requires_raw_data,
    claim_srecall_better_proxy,
    defn_srecall,
    defn_semantic_neighbors,
)

# ── Settings ──────────────────────────────────────────────────────────────────

defn_trecall = setting(
    "Tolerant recall ($\\text{trecall}@k$) is defined as follows. Given a "
    "ground-truth set $G_k$ and a retrieved set $R_k$ (each of size $k$), "
    "tolerant recall finds the largest subset $T \\subseteq R_k$ such that every "
    "$t_i \\in T$ corresponds to a unique $g_i \\in G_k$ satisfying either "
    "(a) $g_i = t_i$ (exact match), or (b) $t_i^{\\text{score}} \\geq "
    "g_i^{\\text{score}} \\cdot (1 - x\\%)$ under inner product similarity "
    "(score within $x\\%$ tolerance). Then: "
    "$\\text{trecall}@k = |T| / |G_k|$. "
    "The tolerance $x\\%$ is a hyperparameter.",
    title="Tolerant recall formula"
)

defn_threshold_proxy = setting(
    "A practical proxy for setting the tolerance threshold $x\\%$ is computed as "
    "the relative difference between the scores of the $\\frac{2}{3}k$-th and "
    "$k$-th ground-truth neighbors, normalized by the maximum ground-truth score, "
    "averaged across queries: "
    "$\\frac{\\text{score}_{2k/3} - \\text{score}_k}{\\text{max\\_score}} \\times 100$. "
    "This leverages the score gap among lower-ranked results where irrelevant "
    "neighbors tend to cluster.",
    title="Tolerance threshold proxy formula"
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_trecall_approximates_srecall = claim(
    "Tolerant recall with a 1% tolerance threshold closely approximates semantic "
    "recall in the MSMARCO dataset (250 queries, ScaNN ANNS with 8-bit "
    "quantization). Across all queries: semantic recall = 0.932, tolerant recall "
    "= 0.920. For queries with fewer than 20 semantic neighbors: semantic recall "
    "= 0.903, tolerant recall = 0.859. The per-query distributions in Figure 3 "
    "(artifacts/2604.20417.pdf) show that tolerant recall closely tracks the "
    "semantic recall distribution.",
    title="Tolerant recall approximates semantic recall (MSMARCO)",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 3", "caption": "Per-query distributions of traditional, semantic, and tolerant recall"}
)

claim_trecall_no_raw_data = claim(
    "Tolerant recall can be computed using only embedding vectors and their "
    "similarity scores, without access to the underlying raw objects (text, "
    "images, etc.). This makes it applicable in scenarios where semantic "
    "neighbors cannot be identified, such as embeddings-only datasets.",
    title="Tolerant recall applicable without raw data"
)

claim_trecall_robust_dynamic = claim(
    "Tolerant recall is more robust to frequent dataset updates than traditional "
    "recall. Traditional recall degrades rapidly if the ground truth is not "
    "recomputed after each database update, since new items may displace existing "
    "top-$k$ neighbors. Tolerant recall allows replacements with items scoring "
    "within the tolerance band, reducing sensitivity to minor ground-truth shifts "
    "[@Kuffo2026].",
    title="Tolerant recall robust to dynamic datasets"
)

claim_trecall_mitigates_quantization = claim(
    "Tolerant recall mitigates the evaluation penalties caused by 8-bit scalar "
    "quantization artifacts. Quantization introduces small relative score errors "
    "that can reorder near-equidistant irrelevant neighbors, causing traditional "
    "recall penalties. Tolerant recall absorbs these reorderings by allowing "
    "score-proximate replacements within the retrieved set [@Quantization2025].",
    title="Tolerant recall robust to quantization artifacts"
)

claim_trecall_has_hyperparameter = claim(
    "Unlike semantic recall, tolerant recall requires a tolerance threshold "
    "hyperparameter $x\\%$ that must be configured. This is a limitation relative "
    "to semantic recall, though a practical proxy for setting $x\\%$ is provided "
    "(see @defn_threshold_proxy) [@Kuffo2026].",
    title="Tolerant recall requires threshold hyperparameter"
)

claim_threshold_proxy_effective = claim(
    "The tolerance threshold proxy (relative score difference between the "
    "$\\frac{2}{3}k$-th and $k$-th neighbors) closely matches the semantic recall "
    "metric in both MSMARCO and MIRACL datasets, as shown in Figure 8 "
    "(artifacts/2604.20417.pdf). This proxy provides a practical starting point "
    "for threshold selection without needing semantic neighbor labels.",
    title="Threshold proxy matches semantic recall",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 8", "caption": "Effect of different thresholds on tolerant recall"}
)

# ── Strategies ────────────────────────────────────────────────────────────────

# claim_trecall_no_raw_data is supported by construction from the definition;
# no explicit strategy needed (it follows directly from the defn_trecall setting).

strat_trecall_quant = support(
    [claim_irrelevant_equidistant],
    claim_trecall_mitigates_quantization,
    reason=(
        "Because irrelevant neighbors cluster at nearly the same score "
        "(@claim_irrelevant_equidistant), small quantization errors easily reorder "
        "them. The tolerant recall tolerance band covers this score gap, allowing "
        "retrieved items to substitute for ground-truth items within the band. "
        "Semantic recall avoids this issue entirely by ignoring irrelevant neighbors "
        "[@Quantization2025]."
    ),
    prior=0.87,
    background=[defn_trecall]
)

strat_trecall_approx = support(
    [claim_trecall_mitigates_quantization, claim_irrelevant_equidistant],
    claim_trecall_approximates_srecall,
    reason=(
        "Because tolerant recall absorbs score perturbations among near-equidistant "
        "irrelevant neighbors (@claim_trecall_mitigates_quantization, "
        "@claim_irrelevant_equidistant), its replacements occur mostly among "
        "irrelevant objects, which are also the objects excluded from semantic "
        "recall's denominator. This structural alignment causes tolerant recall "
        "to track semantic recall empirically [@Kuffo2026]."
    ),
    prior=0.83,
    background=[defn_trecall, defn_srecall]
)

strat_threshold_proxy = support(
    [claim_irrelevant_equidistant],
    claim_threshold_proxy_effective,
    reason=(
        "Irrelevant neighbors cluster at nearly the same score "
        "(@claim_irrelevant_equidistant). The lower-ranked neighbors (around the "
        "$\\frac{2}{3}k$ to $k$ range) are dominated by such near-equidistant "
        "irrelevant items. Their score gap thus captures the scale of score "
        "fluctuations needed to substitute irrelevant items, which is exactly what "
        "the tolerance threshold is meant to cover [@Kuffo2026]."
    ),
    prior=0.78,
    background=[defn_threshold_proxy]
)
