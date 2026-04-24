"""Section 2: Semantic Recall — Definition and Methodology"""

from gaia.lang import claim, setting, support, deduction, abduction, compare

from .motivation import (
    claim_recall_misaligned,
    claim_anns_bounded_by_exact,
    claim_curated_gt_unfair,
    setup_anns,
    setup_recall,
    setup_embedding,
)

# ── Settings ──────────────────────────────────────────────────────────────────

defn_semantic_neighbors = setting(
    "Semantic neighbors (SN) of a query $q$ are defined as the subset of the "
    "brute-force exact NNS top-$k$ ground truth that are semantically relevant "
    "to $q$, as determined by an external judge (human or LLM). Relevance is "
    "binary: each ground-truth neighbor is labeled 'Relevant' or 'Not Relevant' "
    "with respect to $q$.",
    title="Semantic neighbors definition"
)

defn_srecall = setting(
    "Semantic recall ($\\text{srecall}$) is defined as: "
    "$\\text{srecall} = |R \\cap SN| / |SN|$, where $R$ is the set of results "
    "retrieved by an ANNS algorithm and $SN$ is the set of semantic neighbors "
    "in the top-$k$ ground truth. A high srecall indicates the algorithm "
    "retrieves objects that are both mathematically close and semantically meaningful.",
    title="Semantic recall formula"
)

defn_judging_process = setting(
    "Semantic neighbors are identified via a two-step process: (1) compute the "
    "exact NNS ground truth (top-$k$ results via brute-force search); (2) classify "
    "each ground-truth neighbor as semantically relevant or irrelevant using an "
    "external judge (LLM or human). Only the top-$k$ ground-truth neighbors need "
    "to be judged, not the entire dataset.",
    title="Judging process for semantic neighbors"
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_srecall_no_penalty = claim(
    "Semantic recall eliminates the three key limitations of traditional recall: "
    "(i) it does not penalize algorithms for missing mathematically close but "
    "semantically irrelevant objects; (ii) it is not affected by embedding model "
    "limitations since it only considers objects retrievable via exact NNS; "
    "(iii) it requires no threshold hyperparameters, unlike metrics such as "
    "$\\text{recall}@k\\text{-}\\epsilon$ [@ANNBench2020] or Relative Distance "
    "Error [@DARTH2025] [@Kuffo2026].",
    title="Semantic recall advantages over traditional recall"
)

claim_srecall_hyperparameter_free = claim(
    "Semantic recall requires no threshold hyperparameter configuration, in "
    "contrast to $\\text{recall}@k\\text{-}\\epsilon$ (requires $\\epsilon$ "
    "threshold), $\\text{robustness}@k\\text{-}\\gamma$ [@RobustVS2025] (requires "
    "$\\gamma$), and Relative Distance Error [@DARTH2025] (requires a distance "
    "tolerance). The lack of a hyperparameter makes semantic recall more portable "
    "and interpretable across different datasets and systems.",
    title="Semantic recall is hyperparameter-free"
)

claim_llm_judging_efficient = claim(
    "LLM-based identification of semantic neighbors is substantially more efficient "
    "than full dataset curation: instead of judging millions of (query, document) "
    "pairs to construct a gold-standard dataset, only the top-$k$ ground-truth "
    "neighbors per query need to be classified. For 250 queries with top-100 "
    "ground truth, this requires at most 25,000 LLM calls vs. millions for full "
    "curation.",
    title="LLM judging efficiency"
)

claim_srecall_requires_raw_data = claim(
    "Semantic recall requires access to the underlying raw objects (text, images, "
    "etc.) in order to perform semantic relevance judging. Embeddings alone are "
    "insufficient. This is a practical limitation compared to traditional recall, "
    "which only requires the embedding vectors [@Kuffo2026].",
    title="Semantic recall limitation: requires raw data"
)

claim_srecall_undefined_no_relevant = claim(
    "Semantic recall is undefined when a query has no semantically relevant "
    "results in the top-$k$ ground truth (i.e., $|SN| = 0$). Such queries should "
    "be excluded from retrieval-quality evaluation, as no meaningful answers exist "
    "in the embedding space for those queries. Their existence may indicate "
    "regression in the embedding model.",
    title="Semantic recall undefined for zero-SN queries"
)

claim_srecall_better_proxy = claim(
    "Semantic recall is a more accurate indicator of retrieval quality perceived "
    "by end users than traditional recall, because it measures the fraction of "
    "retrieved results that are semantically useful, rather than the fraction "
    "that match a mathematical ground truth that may include irrelevant items "
    "[@Kuffo2026].",
    title="Semantic recall is a better quality proxy"
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_srecall_advantages = deduction(
    [claim_anns_bounded_by_exact],
    claim_srecall_no_penalty,
    reason=(
        "By construction (see @defn_srecall), semantic recall's denominator "
        "contains only semantically relevant objects that appear in the exact NNS "
        "ground truth. Because ANNS is bounded by exact NNS "
        "(@claim_anns_bounded_by_exact), all $SN$ members are theoretically "
        "retrievable. Missing a non-$SN$ object incurs no penalty. This directly "
        "follows from the definition, requiring no empirical validation [@Kuffo2026]."
    ),
    prior=0.97,
    background=[defn_srecall, defn_semantic_neighbors]
)

strat_srecall_better_proxy = support(
    [claim_srecall_no_penalty, claim_recall_misaligned],
    claim_srecall_better_proxy,
    reason=(
        "Because semantic recall does not penalize for irrelevant neighbors "
        "(@claim_srecall_no_penalty) and traditional recall does "
        "(@claim_recall_misaligned), semantic recall more closely tracks the "
        "quality that matters to end users: retrieving relevant objects. "
        "The empirical evidence in Section 4 corroborates this reasoning "
        "[@Kuffo2026]."
    ),
    prior=0.88,
    background=[setup_anns]
)

strat_llm_judging = support(
    [claim_llm_judging_efficient],
    claim_srecall_no_penalty,
    reason=(
        "The efficiency of LLM-based judging (@claim_llm_judging_efficient) makes "
        "it practically feasible to obtain semantic neighbor labels, which is a "
        "prerequisite for computing semantic recall. Without an efficient judging "
        "method, the operational advantage of semantic recall would be undermined "
        "by annotation cost [@Kuffo2026]."
    ),
    prior=0.80,
    background=[defn_judging_process]
)
