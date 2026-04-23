"""Section 7: Information Retrieval"""

from gaia.lang import (
    claim, setting,
    support,
)
from .s3_framework import framework_proposed

# ── Retrieval taxonomy ────────────────────────────────────────────────────────

setting_retrieval_role = setting(
    "Information retrieval governs how the agent system identifies and extracts the most relevant "
    "information from memory storage to support informed reasoning or context-aware response generation "
    "when a new query arrives.",
    title="Retrieval component role",
)

retrieval_lexical = claim(
    "Lexical-based retrieval relies on surface-level token or term overlap, implemented through "
    "techniques such as Jaccard similarity coefficient or BM25 scoring. It provides a strong "
    "baseline for exact term matching, particularly effective for retrieving names, specific "
    "entities, or phrases where precise wording is critical.",
    title="Lexical-based retrieval",
    background=[setting_retrieval_role],
)

retrieval_vector = claim(
    "Vector-based retrieval leverages semantic similarity in a continuous vector space, "
    "encoding both query and memories into high-dimensional vectors via embedding models and "
    "performing top-k nearest neighbor search using cosine similarity. It addresses the "
    "vocabulary mismatch problem inherent in exact keyword matching, capturing latent semantic "
    "nuances. Approximate Nearest Neighbor (ANN) algorithms (HNSW, PQ) maintain efficiency "
    "at memory scale.",
    title="Vector-based retrieval",
    background=[setting_retrieval_role],
)

retrieval_structure = claim(
    "Structure-based retrieval exploits explicit relational connections between memory entities, "
    "operating on graph-based or hierarchical storage, performing graph traversal, neighborhood "
    "expansion, or multi-hop reasoning to retrieve interconnected clusters of information. "
    "Example: Mem0g explores relationships from similarity-identified nodes to build a comprehensive "
    "subgraph. Zep uses BFS-based graph traversal to enhance initial search results with additional "
    "nodes and edges.",
    title="Structure-based retrieval",
    background=[setting_retrieval_role],
)

retrieval_llm_assisted = claim(
    "LLM-assisted retrieval integrates LLMs as an active reasoning component to guide or refine "
    "retrieval. LLMs can directly decide which information to retrieve, transform ambiguous user "
    "prompts into precise search queries, or identify key entities for targeted retrieval. "
    "This paradigm excels at uncovering latent semantic dependencies, ensuring closer alignment "
    "between queries and retrieved knowledge.",
    title="LLM-assisted retrieval",
    background=[setting_retrieval_role],
)

strat_four_retrieval_types = support(
    [framework_proposed],
    retrieval_vector,
    reason=(
        "The unified framework (@framework_proposed) provides a structured lens for categorizing "
        "retrieval strategies. Survey of existing methods reveals four fundamental paradigms: "
        "lexical-based, vector-based, structure-based, and LLM-assisted. Vector-based retrieval "
        "is the most widely used, appearing in all ten representative methods, reflecting the "
        "dominance of dense embedding approaches in modern agent memory systems."
    ),
    prior=0.92,
)
