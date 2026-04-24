"""Introduction: Motivation and Problem Statement"""

from gaia.lang import claim, setting, question, support, contradiction

# ── Settings: background context ─────────────────────────────────────────────

setup_anns = setting(
    "Approximate Nearest Neighbor Search (ANNS) algorithms are used to retrieve "
    "results that are close — but not necessarily the exact nearest — neighbors "
    "to a query in a high-dimensional embedding space. The approximation trades "
    "search exactness for speed.",
    title="ANNS background"
)

setup_recall = setting(
    "Traditional recall for ANNS is defined as the fraction of retrieved results "
    "that appear in the brute-force (exact) ground truth of top-$k$ nearest "
    "neighbors. Formally: $\\text{recall} = |R \\cap G_k| / |G_k|$, where $R$ is "
    "the set of retrieved neighbors and $G_k$ is the brute-force ground truth.",
    title="Traditional recall definition"
)

setup_embedding = setting(
    "AI embedding models map objects (text, images, video) into high-dimensional "
    "vectors such that semantically similar objects are geometrically close under "
    "distance metrics like Euclidean distance or inner product. The semantic "
    "similarity between objects is thus reflected in their vector proximity.",
    title="Embedding model setup"
)

# ── Claims: problem characterization ─────────────────────────────────────────

claim_recall_widespread = claim(
    "Traditional recall (the fraction of retrieved neighbors matching the exact "
    "brute-force ground truth top-$k$) is the de facto standard metric for "
    "evaluating the retrieval quality of ANNS algorithms in both academia and "
    "industry [@ANNBench2020; @DARTH2025; @VIBE2025].",
    title="Widespread use of traditional recall"
)

claim_recall_misaligned = claim(
    "Traditional recall is misaligned with the goal of embedding-based retrieval "
    "because it penalizes ANNS algorithms for failing to retrieve mathematically "
    "close but semantically irrelevant objects. Failing to retrieve an irrelevant "
    "neighbor is penalized just as much as failing to retrieve a relevant one, "
    "even though only the latter matters to end users [@EmbedPitfalls2025].",
    title="Traditional recall misalignment with semantic quality"
)

claim_anns_bounded_by_exact = claim(
    "ANNS algorithms are fundamentally bounded by exact nearest neighbor search "
    "(NNS): they cannot retrieve semantically relevant objects that an exact NNS "
    "would miss, because both operate within the same embedding space constraints "
    "[@EmbedLimits2025]. An embedding model that places a semantically relevant "
    "object far from the query will cause both exact and approximate NNS to miss it.",
    title="ANNS bounded by exact NNS"
)

claim_curated_gt_unfair = claim(
    "Evaluation using manually curated ground truths (where relevance is judged "
    "independently of vector proximity) can unfairly penalize ANNS algorithms for "
    "limitations of the embedding model, since an ANNS algorithm can only retrieve "
    "objects the embedding model places near the query [@EmbedPitfalls2025].",
    title="Curated ground truth penalizes embedding model limitations"
)

claim_few_relevant_common = claim(
    "A significant fraction of queries in embedding datasets have few semantically "
    "relevant results among their top-$k$ nearest neighbors. In the MSMARCO dataset "
    "with 250 queries and top-100 ground truth, approximately 40% of queries have "
    "fewer than 15 relevant documents, including 3 queries with no relevant results "
    "at all (Figure 2, artifacts/2604.20417.pdf).",
    title="Few-relevant-neighbor queries are common",
    metadata={"figure": "artifacts/2604.20417.pdf, Figure 2", "caption": "Distribution of semantically relevant neighbors per query in MSMARCO"}
)

claim_irrelevant_equidistant = claim(
    "Non-semantic (irrelevant) neighbors tend to cluster at nearly the same "
    "distance from the query embedding, with consistently small score deltas "
    "between consecutive irrelevant neighbors. This near-equidistance makes "
    "irrelevant neighbors particularly hard for ANNS algorithms to retrieve "
    "reliably, since small ranking fluctuations (e.g., from quantization) easily "
    "reorder them. Traditional recall penalizes algorithms for this unavoidable "
    "reordering.",
    title="Irrelevant neighbors are near-equidistant"
)

# ── Research questions ────────────────────────────────────────────────────────

q_better_metric = question(
    "Can we define an evaluation metric for ANNS that measures only semantically "
    "relevant retrieval quality, without penalizing algorithms for missing "
    "irrelevant neighbors?"
)

q_proxy_metric = question(
    "When semantic relevance labels cannot be obtained (e.g., embeddings-only "
    "datasets), what proxy metric best approximates semantic recall?"
)

# ── Connect claims ────────────────────────────────────────────────────────────

strat_recall_misaligned = support(
    [claim_few_relevant_common, claim_irrelevant_equidistant],
    claim_recall_misaligned,
    reason=(
        "When queries have few relevant results (@claim_few_relevant_common), "
        "the ground truth is dominated by irrelevant neighbors. Because irrelevant "
        "neighbors are nearly equidistant (@claim_irrelevant_equidistant), ANNS "
        "algorithms frequently fail to retrieve some of them due to ranking "
        "fluctuations, incurring traditional recall penalties. These penalties "
        "reflect noise rather than real quality loss, demonstrating the misalignment "
        "of traditional recall with the semantic retrieval goal [@Kuffo2026]."
    ),
    prior=0.92,
    background=[setup_recall, setup_anns]
)

strat_curated_unfair = support(
    [claim_anns_bounded_by_exact],
    claim_curated_gt_unfair,
    reason=(
        "Since ANNS is bounded by exact NNS (@claim_anns_bounded_by_exact), any "
        "curated ground truth item that exact NNS cannot retrieve represents a "
        "limitation of the embedding model, not of the ANNS algorithm. Penalizing "
        "ANNS for this conflates two distinct failure modes: embedding model failure "
        "vs. approximation algorithm failure [@EmbedLimits2025]."
    ),
    prior=0.90,
    background=[setup_embedding]
)

not_both_metrics = contradiction(
    claim_recall_widespread,
    claim_recall_misaligned,
    reason=(
        "Traditional recall cannot simultaneously be the correct metric for semantic "
        "quality (widespread-use assumption) and be systematically misaligned with "
        "semantic quality — this tension is the paper's central motivation for new metrics."
    ),
    prior=0.85
)
