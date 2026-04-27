"""Section 3: The MEMFLY Framework — IB Formulation, Structural Prior, Construction"""

from gaia.lang import claim, setting, support, deduction, induction

from .motivation import (
    claim_compression_fidelity_dilemma,
    claim_high_dim_curse,
    claim_ib_aligns_with_memory,
    setup_ib_principle,
)

# ── Settings: framework setup ─────────────────────────────────────────────────

setup_memory_state = setting(
    "MEMFLY models the memory state at time t as a random variable M_t taking values "
    "in a structured state space. For computational realization, M_t is instantiated "
    "as a dynamic graph G_t = (V_t, E_t, Phi_t), where V_t is the set of memory "
    "nodes, E_t are topological connections, and Phi_t maps each node to a dense "
    "embedding and textual content.",
    title="MEMFLY memory state representation",
)

setup_double_clustering = setting(
    "The Double Clustering framework [@Slonim2000] addresses high-dimensional "
    "co-occurrence sparsity through a two-stage abstraction process: (1) features "
    "are first aggregated into 'word clusters' Y -> Y_tilde based on conditional "
    "distributions p(x|y), yielding distributionally robust intermediate centroids; "
    "(2) data points are clustered X -> X_tilde based on distributions over those "
    "intermediate clusters. This intermediate symbolic layer projects data onto a "
    "denser, less noisy representation.",
    title="Double Clustering principle",
)

setup_aib = setting(
    "The Agglomerative Information Bottleneck (AIB) algorithm [@Slonim1999] is an "
    "offline greedy procedure that, on each step, merges the cluster pair (z_i, z_j) "
    "that minimizes information loss quantified by the Jensen-Shannon divergence: "
    "delta_I_Y(z_i, z_j) = (p(z_i) + p(z_j)) * D_JS(p(Y|z_i), p(Y|z_j)).",
    title="Agglomerative Information Bottleneck (AIB)",
)

setup_streaming = setting(
    "In the agentic setting, memory must be constructed online from a continuous "
    "stream X_{1:t} = {x_1, ..., x_t}, and future reasoning tasks Y are unknown at "
    "construction time. This precludes direct evaluation of distributions p(Y|z) "
    "required by the offline AIB algorithm.",
    title="Online streaming constraint",
)

# ── Claims: IB formulation ────────────────────────────────────────────────────

claim_memory_ib_lagrangian = claim(
    "MEMFLY formulates agentic memory construction as the minimization of a Memory "
    "Information Bottleneck Lagrangian L_IB(M_t) = I(X_{1:t}; M_t) - beta * I(M_t; "
    "Y), where the compression term I(X_{1:t}; M_t) measures how much input-stream "
    "information is retained in the memory state, and the relevance term I(M_t; Y) "
    "measures the mutual information between the memory state and future tasks Y. "
    "The hyperparameter beta > 0 controls the compression-relevance trade-off "
    "[@Kuffo2026, Eq. 1].",
    title="Memory IB Lagrangian objective",
)

claim_y_unknown_at_construction = claim(
    "A key difficulty in applying the Information Bottleneck principle to agentic "
    "memory is that future tasks Y are not directly observable during memory "
    "construction. This invalidates direct computation of distributions p(Y|z) "
    "needed by the standard AIB merge criterion (Eq. 3) [@Kuffo2026].",
    title="Y is unknown at memory construction time",
)

claim_proxy_signals = claim(
    "MEMFLY approximates the latent relevance variable Y through two proxy signals: "
    "(1) local coherence — the semantic consistency within and across memory units, "
    "captured by Keyword co-occurrence patterns; (2) global navigability — the "
    "accessibility of evidence chains, captured by the Topic hierarchy and "
    "associative links. These proxies reflect the observation that reasoning tasks "
    "typically require either entity-centric evidence retrieval or thematic evidence "
    "aggregation [@Kuffo2026].",
    title="Proxy signals for unobservable Y",
)

claim_online_intractable = claim(
    "Directly optimizing the Memory IB Lagrangian over the entire interaction "
    "history is computationally intractable due to the combinatorial explosion of "
    "possible memory configurations. Online streaming therefore requires an "
    "approximate greedy procedure rather than a global optimum search.",
    title="Direct IB optimization is intractable",
)

claim_greedy_aib_extension = claim(
    "MEMFLY adopts a greedy online approximation that, at each time step, minimizes "
    "the incremental Lagrangian cost Delta_L = Delta_I_compress - beta * "
    "Delta_I_relevance (Eq. 2), making locally optimal decisions over a candidate "
    "neighborhood retrieved by sparse-dense indices. This extends the offline AIB "
    "merge step to handle streaming inputs [@Slonim1999].",
    title="Online greedy AIB extension",
)

# ── Claims: LLM as JS-divergence approximator ────────────────────────────────

claim_llm_proxies_js = claim(
    "MEMFLY employs an LLM as a gradient-free policy [@Yang2024] that approximates "
    "AIB merge decisions through semantic assessment. Given two memory units n_t and "
    "n_i, the LLM outputs a redundancy score s_red(n_t, n_i) in [0, 1] and a "
    "complementarity score s_comp(n_t, n_i) in [0, 1]. The hypothesis is "
    "s_red(n_t, n_i) approx 1 - D_JS(p(Y|n_t), p(Y|n_i)), so high redundancy "
    "indicates low JS-divergence and the units provide similar downstream "
    "information [@Kuffo2026, Eq. 4].",
    title="LLM as JS-divergence approximator",
)

claim_llm_implicit_knowledge = claim(
    "Pre-trained LLMs implicitly encode task-relevant distributional properties "
    "across diverse domains. Their semantic similarity assessments correlate with "
    "the JS-divergence between conditional distributions p(Y|z) over plausible "
    "downstream tasks Y, even when those distributions are not directly accessible.",
    title="LLM pre-training implicitly captures task-relevant distributions",
)

# ── Claims: structural prior — Note-Keyword-Topic hierarchy ──────────────────

claim_three_layer_hierarchy = claim(
    "MEMFLY instantiates the memory state as a stratified Note-Keyword-Topic "
    "hierarchy. Layer 1 (Notes N): atomic memory units n_i = (r_i, c_i, h_i, K_i) "
    "preserving raw observational fidelity. Layer 2 (Keywords K): symbolic anchors "
    "extracted by the LLM that bridge dense embeddings and discrete reasoning. "
    "Layer 3 (Topics T): clusters of co-occurring keywords that partition the "
    "memory latent space into navigable regions enabling O(1) macro-semantic "
    "localization [@Kuffo2026].",
    title="Note-Keyword-Topic three-layer hierarchy",
)

claim_notes_preserve_fidelity = claim(
    "The Notes layer is designed to preserve raw observational fidelity, "
    "approximating the IB condition I(N; X) approx H(X). By explicitly maintaining "
    "non-parametric access to original inputs, MEMFLY mitigates hallucination risks "
    "inherent in purely parametric or compression-heavy memory systems [@Kuffo2026].",
    title="Notes layer preserves raw fidelity",
)

claim_keywords_resolve_sparsity = claim(
    "Keywords resolve semantic sparsity by grounding proximity in shared symbolic "
    "substructures rather than potentially spurious vector correlations. They serve "
    "the same functional role as 'word clusters' (Y_tilde) in the double clustering "
    "framework [@Slonim2000], providing a lower-dimensional, distributionally "
    "robust feature space that stabilizes semantic proximity and mitigates vector "
    "dilution [@Kuffo2026].",
    title="Keywords stabilize semantic proximity",
)

claim_topics_enable_navigation = claim(
    "Topics aggregate keywords based on co-occurrence structure, analogous to "
    "document clusters (X_tilde) in the double clustering framework. They serve as "
    "semantic centroids that partition the memory latent into navigable regions, "
    "enabling O(1) macro-semantic localization during retrieval [@Kuffo2026].",
    title="Topics enable O(1) macro-semantic navigation",
)

# ── Claims: gated structural update ──────────────────────────────────────────

claim_gated_three_ops = claim(
    "MEMFLY's gated structural update executes one of three operations on each "
    "incoming note n_t given a candidate ni in the retrieved neighborhood: "
    "MERGE(n_i <- n_i ⊕ n_t) when s_red(n_t, n_i) > tau_m, LINK(n_i <-> n_t) when "
    "s_comp(n_t, n_i) > tau_l, otherwise APPEND(n_t). Thresholds tau_m and tau_l "
    "are hyperparameters [@Kuffo2026, Eq. 6].",
    title="Three structural operations: merge, link, append",
)

claim_merge_reduces_compression = claim(
    "The Merge operation directly reduces I(X_{1:t}; M_t) by reducing the cardinality "
    "|V_t| of memory nodes. Content r_i is unioned with r_t, context c_i' is "
    "synthesized via an LLM-based F_merge function preserving distinct information, "
    "and the embedding and keyword set are updated. This is analogous to the AIB "
    "merge step that selects pairs with minimal JS-divergence [@Slonim1999].",
    title="Merge reduces compression term I(X; M)",
)

claim_link_preserves_relevance = claim(
    "The Link operation does not directly reduce I(X_{1:t}; M_t), but it preserves "
    "conditional dependencies that support I(M_t; Y). Link is triggered when "
    "I(n_t; Y | n_i) > 0 ∧ I(n_t; n_i) > 0 (Eq. 11): n_t provides additional "
    "task-relevant information beyond n_i, and the two are logically related. "
    "Encoding this in E_RELATED preserves conditional structure necessary for "
    "multi-hop reasoning without increasing redundancy [@Kuffo2026, Remark 3.2].",
    title="Link preserves conditional dependencies for I(M; Y)",
)

claim_append_preserves_diversity = claim(
    "The Append operation, triggered when neither merge nor link thresholds are met, "
    "introduces n_t as an autonomous unit. This preserves distributional diversity "
    "for novel content that has neither sufficient redundancy to merge nor "
    "sufficient complementarity to link.",
    title="Append preserves novel content diversity",
)

claim_extends_aib = claim(
    "MEMFLY extends the original AIB algorithm — which supports only merge "
    "operations on fixed co-occurrence matrices — with Link and Append operations "
    "to handle streaming settings where information arrives incrementally and may "
    "exhibit complementary or novel content. This adaptation maintains the greedy "
    "optimization spirit while accommodating agentic memory requirements "
    "[@Kuffo2026, Remark 3.3].",
    title="MEMFLY extends classical AIB beyond merges",
)

# ── Claims: ingestion and topic evolution ────────────────────────────────────

claim_ingestion_denoises = claim(
    "Semantic ingestion projects raw input x_t into a structured Note "
    "n_t = F_ingest(x_t) = (r_t, c_t, h_t, K_t) where r_t preserves raw content, "
    "c_t is a denoised context summary, h_t = Embed(c_t), and K_t is the LLM-"
    "extracted keyword set. This transformation enhances signal-to-noise ratio, "
    "improving I(n_t; Y) relative to I(x_t; Y) [@Kuffo2026, Eq. 5].",
    title="Ingestion denoises and structures input",
)

claim_topic_evolution_modularity = claim(
    "Topic evolution is formalized as constrained graph partitioning over the "
    "Keyword co-occurrence graph G_kw: maximize the modularity Q(T, G_kw) subject "
    "to cardinality bounds delta_min <= |C_i| <= delta_max. MEMFLY uses the Leiden "
    "algorithm [@Traag2019] for efficiency. While modularity differs from direct IB "
    "clustering, empirical studies establish strong correlation between modularity-"
    "based and information-theoretic community structures [@Fortunato2010].",
    title="Topic evolution via Leiden modularity optimization",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_lagrangian_from_ib = deduction(
    [claim_ib_aligns_with_memory],
    claim_memory_ib_lagrangian,
    reason=(
        "Since memory optimization aligns with the IB principle "
        "(@claim_ib_aligns_with_memory) which minimizes I(X; M) - beta * I(M; Y) by "
        "definition [@Slonim1999], substituting the agentic memory state M_t and the "
        "input stream X_{1:t} yields the Memory IB Lagrangian directly."
    ),
    prior=0.95,
    background=[setup_ib_principle, setup_memory_state],
)

strat_intractable = support(
    [claim_memory_ib_lagrangian],
    claim_online_intractable,
    reason=(
        "The Memory IB Lagrangian (@claim_memory_ib_lagrangian) ranges over the "
        "combinatorial space of possible memory configurations at each step. As the "
        "history length grows, exhaustive search over partitions of |X_{1:t}| "
        "becomes computationally infeasible."
    ),
    prior=0.93,
)

strat_greedy_extension = support(
    [claim_online_intractable, claim_y_unknown_at_construction],
    claim_greedy_aib_extension,
    reason=(
        "Given that direct IB optimization is intractable (@claim_online_intractable) "
        "and Y is unknown at construction time (@claim_y_unknown_at_construction), an "
        "online greedy strategy that minimizes the incremental Lagrangian over a "
        "candidate neighborhood is the natural adaptation: it preserves the AIB merge "
        "principle (@setup_aib) while restricting the decision space to a tractable "
        "local subgraph."
    ),
    prior=0.88,
    background=[setup_aib, setup_streaming],
)

strat_llm_js_proxy = support(
    [claim_llm_implicit_knowledge, claim_y_unknown_at_construction],
    claim_llm_proxies_js,
    reason=(
        "JS-divergence between conditional task distributions cannot be computed "
        "directly because Y is unknown (@claim_y_unknown_at_construction). However, "
        "since pre-trained LLMs implicitly encode task-relevant distributional "
        "properties (@claim_llm_implicit_knowledge), their semantic redundancy "
        "scores can act as a gradient-free proxy for 1 - D_JS(p(Y|n_t), p(Y|n_i)) "
        "[@Yang2024]."
    ),
    prior=0.80,
)

strat_keywords_from_double_clustering = support(
    [claim_high_dim_curse],
    claim_keywords_resolve_sparsity,
    reason=(
        "The high-dimensional embedding curse (@claim_high_dim_curse) motivates an "
        "intermediate symbolic layer. Adopting the double clustering insight "
        "(@setup_double_clustering) that compression succeeds via robust feature "
        "centroids, MEMFLY's Keywords serve the role of word clusters Y_tilde — a "
        "denser, distributionally robust feature space that stabilizes proximity."
    ),
    prior=0.85,
    background=[setup_double_clustering],
)

strat_topics_from_double_clustering = support(
    [claim_keywords_resolve_sparsity],
    claim_topics_enable_navigation,
    reason=(
        "Once Keywords stabilize the symbolic substructure "
        "(@claim_keywords_resolve_sparsity), aggregating them by co-occurrence yields "
        "Topics that play the role of document clusters X_tilde in double clustering. "
        "Topics partition the memory latent into navigable macro-regions, enabling "
        "O(1) localization during retrieval."
    ),
    prior=0.85,
    background=[setup_double_clustering],
)

strat_hierarchy_resolves_dilemma = support(
    [claim_notes_preserve_fidelity, claim_keywords_resolve_sparsity, claim_topics_enable_navigation],
    claim_three_layer_hierarchy,
    reason=(
        "The three layers jointly address the compression-fidelity dilemma "
        "(@claim_compression_fidelity_dilemma): Notes preserve raw fidelity "
        "(@claim_notes_preserve_fidelity, fidelity term), Keywords resolve sparsity "
        "(@claim_keywords_resolve_sparsity, robustness term), and Topics enable "
        "navigation (@claim_topics_enable_navigation, retrievability term). Their "
        "composition realizes the stratified structural prior."
    ),
    prior=0.88,
    background=[setup_double_clustering],
)

strat_three_ops_extension = support(
    [claim_extends_aib, claim_merge_reduces_compression, claim_link_preserves_relevance, claim_append_preserves_diversity],
    claim_gated_three_ops,
    reason=(
        "Each operation maps to a specific term of the IB Lagrangian: Merge reduces "
        "I(X; M) (@claim_merge_reduces_compression), Link preserves conditional "
        "structure for I(M; Y) (@claim_link_preserves_relevance), Append maintains "
        "diversity for novel content (@claim_append_preserves_diversity). The three-"
        "way gate is the natural streaming extension of AIB's merge-only step "
        "(@claim_extends_aib)."
    ),
    prior=0.92,
)

strat_topic_modularity = support(
    [claim_topics_enable_navigation],
    claim_topic_evolution_modularity,
    reason=(
        "Maintaining O(1) macro-navigability (@claim_topics_enable_navigation) "
        "requires periodic re-partitioning of the keyword co-occurrence graph. "
        "Modularity-based community detection via Leiden [@Traag2019] is "
        "computationally efficient and empirically correlates with information-"
        "theoretic clustering [@Fortunato2010], making it a sound stand-in for "
        "exact IB clustering."
    ),
    prior=0.82,
)
