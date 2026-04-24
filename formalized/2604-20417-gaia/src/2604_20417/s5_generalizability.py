"""Section 5: Generalizability — MIRACL Dataset Evaluation"""

from gaia.lang import claim, setting, support, induction

from .motivation import (
    claim_few_relevant_common,
    claim_irrelevant_equidistant,
    setup_anns,
)
from .s2_semantic_recall import (
    claim_srecall_better_proxy,
    defn_srecall,
    defn_semantic_neighbors,
)
from .s3_tolerant_recall import (
    claim_trecall_approximates_srecall,
    claim_threshold_proxy_effective,
    defn_trecall,
    defn_threshold_proxy,
)
from .s4b_tuning import (
    law_tolerant_saves_cost,
)

# ── Settings ──────────────────────────────────────────────────────────────────

setup_miracl_exp = setting(
    "MIRACL evaluation setup: 542,166 Thai-language documents embedded into "
    "1024-dimensional vectors using Cohere Embed V3. Query set: 100 questions in "
    "Thai. Ground truth: top-20 nearest neighbors per query via brute-force inner "
    "product search. Semantic neighbor labels: Gemini 2.5 as judge. ANNS system: "
    "FAISS IVF index [@FAISS2025] (3000 partitions, 8-bit scalar quantization, "
    "probing 0.5% of clusters). Tolerant recall: 2% tolerance threshold.",
    title="MIRACL experiment setup"
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_miracl_sn_powerlaw = claim(
    "The distribution of semantic neighbors per query in the MIRACL Thai-language "
    "dataset (100 queries, top-20 ground truth, Gemini 2.5 judge) follows a "
    "power-law-like behavior: 60% of queries have at most 4 semantic neighbors "
    "out of 20. This is similar in character to the MSMARCO distribution, where "
    "approximately 40% of queries have fewer than 15 semantic neighbors out of 100.",
    title="MIRACL SN distribution is power-law (60% queries have ≤4 SNs)",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 6", "caption": "Distribution of semantic neighbors per query in MIRACL"}
)

claim_miracl_sn_larger_deltas = claim(
    "In the MIRACL dataset, semantic neighbors exhibit significantly larger score "
    "deltas than non-semantic neighbors: SN average delta = $0.05 \\pm 0.03$, "
    "non-SN average delta = $0.005 \\pm 0.008$. The 10× larger delta for SNs "
    "compared to non-SNs parallels the pattern observed in MSMARCO.",
    title="MIRACL SN have 10× larger score deltas than non-SN"
)

claim_miracl_recall_results = claim(
    "On the MIRACL Thai dataset (100 queries, FAISS IVF index with 8-bit "
    "quantization, 2% tolerant recall threshold), the recall metrics compare as:\n\n"
    "| Metric             | Average Score |\n"
    "|--------------------|---------------|\n"
    "| Traditional recall | 0.75          |\n"
    "| Semantic recall    | 0.85          |\n"
    "| Tolerant recall    | 0.83          |\n\n"
    "As in MSMARCO, queries with few SNs show low traditional recall while semantic "
    "recall confirms relevant results are retrieved.",
    title="MIRACL recall comparison (traditional=0.75, semantic=0.85, tolerant=0.83)",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 7", "caption": "Per-query distribution of traditional, semantic, and tolerant recall on MIRACL"}
)

claim_miracl_replicates_pattern = claim(
    "The MIRACL evaluation replicates the MSMARCO pattern: queries with few "
    "semantic neighbors exhibit low traditional recall while semantic recall "
    "confirms that the ANNS algorithm is retrieving the relevant results. "
    "This replication occurs across a different language (Thai vs. English), "
    "a different embedding model (Cohere Embed V3 vs. Gemini Embedding), "
    "a different ANNS system (FAISS IVF vs. ScaNN), and a different dataset scale "
    "(542K vs. 8.83M documents) [@Kuffo2026].",
    title="MIRACL replicates MSMARCO pattern across language, model, and system"
)

claim_metrics_generalize = claim(
    "Semantic recall and tolerant recall are applicable across diverse embedding "
    "models, ANNS algorithms, languages, and data scales: demonstrated on MSMARCO "
    "(English, 8.83M docs, Gemini Embedding, ScaNN, 3072-dim) and MIRACL Thai "
    "(Thai, 542K docs, Cohere Embed V3, FAISS IVF, 1024-dim). The core mechanisms "
    "— near-equidistant non-SNs causing spurious traditional recall penalties — "
    "appear in both settings.",
    title="Semantic and tolerant recall generalize across models and datasets"
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_miracl_sn_powerlaw = support(
    [claim_few_relevant_common],
    claim_miracl_sn_powerlaw,
    reason=(
        "The finding that queries commonly have few relevant results "
        "(@claim_few_relevant_common) in MSMARCO is replicated in MIRACL: 60% "
        "of queries have at most 4 SNs. This supports the generalizability of the "
        "few-SN phenomenon as a property of embedding datasets across languages "
        "and domains [@Kuffo2026]."
    ),
    prior=0.87
)

strat_miracl_replicates = support(
    [claim_miracl_recall_results, claim_miracl_sn_larger_deltas],
    claim_miracl_replicates_pattern,
    reason=(
        "The MIRACL recall results (@claim_miracl_recall_results) show the same "
        "pattern as MSMARCO: higher semantic recall (0.85) than traditional (0.75) "
        "for a dataset where 60% of queries have few SNs. The 10× larger SN score "
        "deltas (@claim_miracl_sn_larger_deltas) confirm the equidistance mechanism "
        "operates in Thai-language embeddings as well [@Kuffo2026]."
    ),
    prior=0.90,
    background=[setup_miracl_exp]
)

# Induction over datasets: semantic recall advantage generalizes
obs_msmarco_srecall = claim(
    "In MSMARCO (English, 8.83M docs, Gemini Embedding, ScaNN), semantic recall "
    "(0.932) substantially exceeds traditional recall (0.863) for all queries, "
    "and the gap is largest for few-SN queries (0.903 vs. 0.762)."
)

obs_miracl_srecall = claim(
    "In MIRACL Thai (Thai, 542K docs, Cohere Embed V3, FAISS IVF), semantic recall "
    "(0.85) substantially exceeds traditional recall (0.75) for all queries, "
    "with queries having few SNs showing low traditional recall while semantic "
    "recall confirms relevant retrieval."
)

s_msmarco_gen = support(
    [claim_metrics_generalize], obs_msmarco_srecall,
    reason="law predicts MSMARCO semantic recall advantage over traditional recall", prior=0.92
)

s_miracl_gen = support(
    [claim_metrics_generalize], obs_miracl_srecall,
    reason="law predicts MIRACL semantic recall advantage over traditional recall", prior=0.90
)

ind_generalization = induction(
    s_msmarco_gen, s_miracl_gen, law=claim_metrics_generalize,
    reason=(
        "MSMARCO and MIRACL use different languages, embedding models, ANNS systems, "
        "and dataset scales, providing genuinely independent evidence for generalizability"
    )
)
