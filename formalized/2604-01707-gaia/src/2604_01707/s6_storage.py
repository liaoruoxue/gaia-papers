"""Section 6: Memory Storage"""

from gaia.lang import (
    claim, setting,
    support,
)
from .s3_framework import framework_proposed

# ── Storage taxonomy ──────────────────────────────────────────────────────────

setting_storage_role = setting(
    "Memory storage governs how processed memory is organized and persisted. It has two primary "
    "dimensions: organization-centric (flat vs hierarchical) and representation-centric "
    "(vector-based vs graph-based).",
    title="Storage component role",
)

storage_flat = claim(
    "Flat storage is a single-tier storage approach that aggregates all information within a "
    "homogeneous space (e.g., a FIFO queue or a JSON file). It is simpler but cannot capture "
    "structural relationships between information at different levels of abstraction.",
    title="Flat storage",
    background=[setting_storage_role],
)

storage_hierarchical = claim(
    "Hierarchical storage partitions memory into specialized, multi-tiered architectures, "
    "allowing individual storage components to fulfill distinct functional roles at different "
    "levels of granularity. Example: MemoryOS organizes memory into three tiers — short-term "
    "(timely conversations), mid-term (topic summaries), and long-term (user preferences). "
    "By applying different management and retrieval strategies to respective tiers, hierarchical "
    "storage optimizes the tradeoff between computational overhead and knowledge persistence.",
    title="Hierarchical storage",
    background=[setting_storage_role],
)

storage_vector = claim(
    "Vector-based storage encodes textual memory into high-dimensional embeddings, indexed in "
    "dedicated vector libraries or databases (e.g., FAISS, Qdrant), enabling efficient semantic "
    "similarity search. To maintain efficiency at scale, Approximate Nearest Neighbor (ANN) "
    "algorithms such as HNSW or Product Quantization (PQ) are frequently employed. "
    "Vector-based storage can function standalone or as a building block in complex architectures.",
    title="Vector-based storage",
    background=[setting_storage_role],
)

storage_graph = claim(
    "Graph-based storage uses diverse graph topologies (trees, knowledge graphs, temporal graphs) "
    "to preserve rich structural information inherent in memory. Examples: "
    "MemTree organizes memory into a hierarchical tree where each node encapsulates aggregated "
    "textual content providing varying abstraction levels by depth. "
    "Zep employs a layered temporal knowledge graph representing raw messages as nodes, "
    "extracting subject-predicate-object triples, and clustering entities into communities. "
    "Graph-based methods capture multi-hop associations beyond simple vector similarity.",
    title="Graph-based storage",
    background=[setting_storage_role],
)

# ── Hierarchical advantage ────────────────────────────────────────────────────

hierarchical_advantage = claim(
    "Compared to flat memory structures, hierarchical organization is more effective in capturing "
    "structural relationships between information. This can be achieved either by employing "
    "tree-based indices (as in MemTree, MemOS) or by designing multi-level storage (as in "
    "MemoryOS). Hierarchical methods generally achieve strong benchmark performance because "
    "tree structures provide high-level conceptual summaries at upper layers while preserving "
    "fine-grained details at leaf nodes.",
    title="Hierarchical advantage over flat",
    background=[setting_storage_role],
)

strat_hierarchical_advantage = support(
    [storage_hierarchical, storage_graph],
    hierarchical_advantage,
    reason=(
        "Hierarchical storage (@storage_hierarchical) and graph-based storage (@storage_graph) "
        "both provide structural organization that flat storage lacks. Tree-based indices enable "
        "multi-granularity search — coarse summaries for broad queries, fine-grained details for "
        "specific lookups. Empirical results show that MemTree (flat+tree), MemOS (hierarchical+tree), "
        "and MemoryOS (hierarchical+vector) consistently rank among the top performers, "
        "while flat-only methods like MemoryBank and MemoChat score near the bottom."
    ),
    prior=0.88,
)
