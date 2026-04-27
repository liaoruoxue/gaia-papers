"""Section 3.4: Memory Retrieval — Tri-Pathway Hybrid + Iterative Refinement"""

from gaia.lang import claim, setting, support

from .s3_framework import (
    claim_three_layer_hierarchy,
    claim_topics_enable_navigation,
    claim_keywords_resolve_sparsity,
    claim_link_preserves_relevance,
)

# ── Settings: retrieval setup ─────────────────────────────────────────────────

setup_query_parsing = setting(
    "MEMFLY's retrieval pipeline begins with an LLM-based semantic parser F_theta "
    "that disentangles a raw query q into two complementary signals: a topical "
    "embedding h_topic and a set of entity embeddings H_keys = {h_k1, ..., h_km} "
    "representing core entities in the query (Eq. 13).",
    title="Query parsing for retrieval",
)

setup_rrf = setting(
    "Reciprocal Rank Fusion (RRF) [@Cormack2009] aggregates the reciprocal ranks of "
    "candidates across multiple retrieval pathways, prioritizing evidence that "
    "consistently appears at the top of multiple lists without requiring score "
    "normalization.",
    title="Reciprocal Rank Fusion",
)

# ── Claims: three retrieval pathways ─────────────────────────────────────────

claim_macro_semantic_path = claim(
    "Pathway 1 (Macro-Semantic Localization) identifies the top-K_topic relevant "
    "Topic centroids T* = TopK(cos(h_topic, mu_C) | C in T) and retrieves notes via "
    "hierarchy traversal: R_topic = {n in N | exists k in K_n, exists C in T*, "
    "k in C}. This addresses the navigation challenge in large-scale memory "
    "[@Kuffo2026, Eq. 14-15].",
    title="Macro-semantic pathway via Topics",
)

claim_micro_symbolic_path = claim(
    "Pathway 2 (Micro-Symbolic Anchoring) matches query entities against the keyword "
    "index: K* = ⋃ TopK(cos(h_k, e_k')) and retrieves R_key = {n in N | K_n ∩ K* "
    "≠ ∅}. This addresses the precision challenge for entity-centric queries "
    "[@Kuffo2026, Eq. 16-17].",
    title="Micro-symbolic pathway via Keywords",
)

claim_topological_path = claim(
    "Pathway 3 (Topological Expansion) starts from the anchor set "
    "E_anc = R_topic ∪ R_key and expands along E_RELATED edges established during "
    "consolidation: E_expand = {m in N | exists n in E_anc, (n, m) in E_RELATED}. "
    "This addresses connectivity for multi-hop reasoning by retrieving evidence "
    "that is logically related but vectorially distant [@Kuffo2026, Eq. 18-19].",
    title="Topological pathway via E_RELATED edges",
)

claim_evidence_fusion_rrf = claim(
    "The final evidence pool is constructed by Reciprocal Rank Fusion (RRF) over the "
    "three pathways together with the topological expansion: E_pool = TopK_final("
    "score_RRF ∪ E_expand). This prioritizes evidence appearing at the top of "
    "multiple ranked lists without requiring score normalization [@Cormack2009].",
    title="RRF-based evidence fusion",
)

claim_tripath_addresses_query_diversity = claim(
    "Tri-pathway retrieval decomposes queries into complementary semantic signals "
    "(topical and entity-level), then executes parallel traversals over the memory "
    "graph. Unlike conventional flat vector search, this approach matches different "
    "query intents (thematic vs. entity-centric vs. multi-hop) to specialized "
    "structural pathways, exploiting the optimized memory structure [@Kuffo2026].",
    title="Tri-pathway retrieval matches diverse query intents",
)

# ── Claims: iterative evidence refinement ────────────────────────────────────

claim_ier_protocol = claim(
    "The Iterative Evidence Refinement (IER) protocol progressively expands the "
    "evidence pool for complex queries. At each iteration i, a sufficiency predicate "
    "Suf(E_i, q) (computed by an LLM that assesses information completeness, Eq. 21) "
    "decides whether the pool addresses the query. If gaps remain, a refined sub-"
    "query q_{i+1} is synthesized to target missing aspects and retrieval is re-"
    "executed; the pool is updated as E_{i+1} = E_i ∪ {n in R(q_{i+1}) | n ∉ E_i}. "
    "This continues until sufficiency or I_max iterations [@Kuffo2026, Eq. 21-22].",
    title="Iterative Evidence Refinement (IER) protocol",
)

claim_ier_handles_multihop = claim(
    "IER handles complex multi-hop queries by progressively expanding the evidence "
    "pool to cover information that is not directly accessible from the initial "
    "query. The sub-query refinement step explicitly targets missing aspects "
    "identified by the LLM-based sufficiency check, supporting reasoning that "
    "spans multiple distinct evidence chunks [@Kuffo2026].",
    title="IER addresses complex multi-hop queries",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_macro_from_topics = support(
    [claim_topics_enable_navigation],
    claim_macro_semantic_path,
    reason=(
        "Since Topics enable O(1) macro-semantic localization "
        "(@claim_topics_enable_navigation), matching the query's topical embedding "
        "h_topic against Topic centroids mu_C is the natural macro-localization step: "
        "it narrows retrieval to a small number of relevant memory regions before "
        "fine-grained search."
    ),
    prior=0.90,
    background=[setup_query_parsing],
)

strat_micro_from_keywords = support(
    [claim_keywords_resolve_sparsity],
    claim_micro_symbolic_path,
    reason=(
        "Since Keywords serve as distributionally robust symbolic anchors "
        "(@claim_keywords_resolve_sparsity), matching query entity embeddings "
        "against the keyword index leverages this layer's stability to provide "
        "precise entity-centric retrieval that resists vector dilution."
    ),
    prior=0.88,
    background=[setup_query_parsing],
)

strat_topo_from_links = support(
    [claim_link_preserves_relevance],
    claim_topological_path,
    reason=(
        "Because Link operations preserve conditional dependencies "
        "(@claim_link_preserves_relevance) for multi-hop reasoning, traversing "
        "E_RELATED edges from the anchor set retrieves logically related but "
        "vectorially distant evidence. This expansion exploits the structural "
        "memory built during consolidation."
    ),
    prior=0.88,
)

strat_tripath = support(
    [claim_macro_semantic_path, claim_micro_symbolic_path, claim_topological_path, claim_three_layer_hierarchy],
    claim_tripath_addresses_query_diversity,
    reason=(
        "The three pathways correspond to the three layers of the memory hierarchy "
        "(@claim_three_layer_hierarchy), each specialized for a different query "
        "intent: Topics for thematic queries (@claim_macro_semantic_path), Keywords "
        "for entity-centric queries (@claim_micro_symbolic_path), and E_RELATED for "
        "multi-hop queries (@claim_topological_path). Their parallel execution "
        "covers the diversity of agentic queries."
    ),
    prior=0.90,
)

strat_evidence_fusion = support(
    [claim_macro_semantic_path, claim_micro_symbolic_path, claim_topological_path],
    claim_evidence_fusion_rrf,
    reason=(
        "With three heterogeneous ranked lists from the pathways, RRF [@Cormack2009] "
        "is well-suited because it does not require comparable scores across lists. "
        "It promotes evidence appearing high in multiple lists, naturally "
        "consolidating the tri-pathway results."
    ),
    prior=0.85,
    background=[setup_rrf],
)

strat_ier_handles = support(
    [claim_ier_protocol],
    claim_ier_handles_multihop,
    reason=(
        "The IER protocol (@claim_ier_protocol) iteratively detects missing aspects "
        "via an LLM sufficiency check and re-runs the tri-pathway retrieval with "
        "refined sub-queries. This loop accumulates evidence chains that single-"
        "shot retrieval misses, enabling multi-hop reasoning that progressively "
        "uncovers indirect dependencies."
    ),
    prior=0.86,
)
