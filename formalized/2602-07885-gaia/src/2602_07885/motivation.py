"""Section 1-2: Motivation and Related Work"""

from gaia.lang import claim, setting, question, support, contradiction

# ── Settings: background context ─────────────────────────────────────────────

setup_llm_agents = setting(
    "Large Language Models (LLMs) are increasingly deployed as persistent autonomous "
    "agents that must perform complex, extended reasoning tasks across long-horizon "
    "interactions. Such use cases require robust long-term memory systems capable of "
    "retaining entity states that evolve over time, resolving temporal dependencies "
    "across sessions, and synthesizing evidence distributed across many turns "
    "[@Xi2023; @Wang2024; @Ferrag2025].",
    title="LLM agents and long-term memory",
)

setup_existing_paradigms = setting(
    "Existing memory frameworks for LLM agents fall into two paradigms. Retrieval-"
    "centric approaches (e.g., RAG variants) preserve verbatim details but accumulate "
    "redundancy and incur retrieval noise [@Lewis2021; @Asai2023; @Yan2024; @Gao2024; "
    "@Ram2023]. Memory-augmented approaches (e.g., MemGPT, MemoryBank, A-MEM, O-Mem) "
    "employ LLM-driven summarization for compression but sacrifice fine-grained "
    "fidelity required for precise reasoning [@Packer2024; @Zhong2023; @Xu2025; "
    "@Wang2025].",
    title="Two paradigms in agentic memory",
)

setup_ib_principle = setting(
    "The Information Bottleneck (IB) principle [@Slonim1999; @Tishby2015] frames "
    "compression as a trade-off: minimize the mutual information between input X and "
    "compressed representation M (compression term I(X; M)) while maximizing the "
    "mutual information between M and downstream tasks Y (relevance term I(M; Y)). "
    "Formally, IB minimizes the Lagrangian L = I(X; M) - beta * I(M; Y).",
    title="Information Bottleneck principle",
)

# ── Claims: problem characterization ─────────────────────────────────────────

claim_compression_fidelity_dilemma = claim(
    "Existing long-term memory frameworks for LLM agents face a fundamental dilemma "
    "between compressing redundant information efficiently and maintaining precise "
    "retrieval fidelity for downstream tasks. Neither retrieval-centric nor memory-"
    "augmented paradigms adequately resolves this tension because they lack a unified, "
    "principled objective for what to retain versus discard [@Kuffo2026].",
    title="Compression-fidelity dilemma in agentic memory",
)

claim_retrieval_centric_redundancy = claim(
    "Retrieval-centric memory systems preserve verbatim details but accumulate "
    "redundancy without consolidation, leading to monotonic entropy increase and "
    "elevated retrieval noise. They operate as inference-time optimizations that "
    "refine the read path while treating the underlying memory as a passive index, "
    "rendering them vulnerable to vector dilution under multi-hop evidence synthesis "
    "[@Lewis2021; @Gao2024; @Asai2023].",
    title="Retrieval-centric systems suffer redundancy and vector dilution",
)

claim_memory_augmented_fidelity_loss = claim(
    "LLM-driven summarization in memory-augmented systems compresses interaction "
    "history into discrete units but optimizes for compression efficiency without a "
    "principled mechanism for preserving task-relevant information. As a result, "
    "fine-grained fidelity required for precise reasoning is sacrificed [@Packer2024; "
    "@Zhong2023; @Xu2025; @Wang2025].",
    title="Memory-augmented systems sacrifice fidelity",
)

claim_ib_aligns_with_memory = claim(
    "The compression-fidelity trade-off in agentic memory construction is "
    "fundamentally an information-theoretic optimization problem that aligns with "
    "the Information Bottleneck principle: compress redundant observations while "
    "preserving sufficient fidelity for future tasks [@Slonim1999].",
    title="Memory optimization aligns with the IB principle",
)

claim_high_dim_curse = claim(
    "Direct manipulation of high-dimensional embedding spaces is ill-posed due to "
    "the curse of dimensionality, which manifests as sparsity and noise in "
    "similarity structures [@Slonim2000].",
    title="High-dimensional embedding spaces are noisy",
)

# ── Research questions ────────────────────────────────────────────────────────

q_unified_objective = question(
    "Is there a unified, principled objective that resolves the compression-fidelity "
    "dilemma in agentic long-term memory construction?",
)

q_online_ib = question(
    "Can the offline Agglomerative Information Bottleneck (AIB) algorithm be adapted "
    "to an online streaming setting where future tasks Y are unknown at construction "
    "time?",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_dilemma = support(
    [claim_retrieval_centric_redundancy, claim_memory_augmented_fidelity_loss],
    claim_compression_fidelity_dilemma,
    reason=(
        "If retrieval-centric systems accumulate redundancy "
        "(@claim_retrieval_centric_redundancy) and memory-augmented systems sacrifice "
        "fidelity (@claim_memory_augmented_fidelity_loss), then the two existing "
        "paradigms occupy opposite ends of the compression-fidelity axis without a "
        "unifying objective. The dilemma is a direct consequence."
    ),
    prior=0.92,
    background=[setup_existing_paradigms],
)

contradiction_paradigms = contradiction(
    claim_retrieval_centric_redundancy,
    claim_memory_augmented_fidelity_loss,
    reason=(
        "The two existing paradigms make opposing trade-offs: retrieval-centric "
        "systems prioritize fidelity at the cost of compression, while memory-"
        "augmented systems prioritize compression at the cost of fidelity. They "
        "cannot both be optimal under a unified IB objective; this tension motivates "
        "a principled middle ground."
    ),
    prior=0.78,
)
