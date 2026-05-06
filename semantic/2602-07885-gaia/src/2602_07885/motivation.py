"""Layer 2 — Compression-Fidelity Dilemma in Agentic Memory (2602.07885)

Frames agent memory as an Information Bottleneck problem: compress context
while preserving decision-relevant information.
"""

from gaia.lang import claim, setting

compression_fidelity_dilemma = claim(
    "Agentic memory systems face a fundamental compression-fidelity trade-off: "
    "compressing context reduces token cost and latency, but risks losing "
    "decision-relevant information. This is formalized as an Information "
    "Bottleneck (IB) problem: minimize I(X;Z) subject to I(Z;Y) ≥ threshold, "
    "where X is raw context, Z is compressed memory, and Y is downstream "
    "decision quality. The key challenge is that Y is unknown at memory "
    "construction time.",
    title="Compression-fidelity dilemma as Information Bottleneck",
    aggregated_from=[
        "claim_compression_fidelity_dilemma",
        "claim_memory_ib_lagrangian",
        "claim_y_unknown_at_construction",
    ],
)

retrieval_centric_has_limits = claim(
    "Retrieval-centric systems (RAG-style) suffer from two failure modes: "
    "(1) redundancy — semantically similar chunks compete for the same "
    "retrieval budget without adding new information, (2) vector dilution "
    "— in high-dimensional embedding spaces, noise dominates signal, "
    "making nearest-neighbor retrieval unreliable for fine-grained relevance.",
    title="Retrieval-centric memory has fundamental limits",
    aggregated_from=[
        "claim_retrieval_centric_redundancy",
        "claim_high_dim_curse",
    ],
)

greedy_aib_solution = claim(
    "The paper proposes an online greedy extension of Agglomerative "
    "Information Bottleneck (AIB) as a practical memory construction "
    "algorithm. It iteratively merges context chunks to minimize IB "
    "Lagrangian loss, using proxy signals (task performance, similarity "
    "heuristics) in place of the unobservable Y. The greedy approach "
    "is approximate but tractable for real-time agent operation.",
    title="Greedy AIB as practical memory construction",
    aggregated_from=[
        "claim_greedy_aib_extension",
        "claim_proxy_signals",
        "claim_online_intractable",
    ],
)

# ── Boundary ──

proxy_not_ground_truth = claim(
    "Proxy signals for Y (task performance, heuristics) may not faithfully "
    "represent true downstream decision quality. If the proxy diverges from "
    "Y, the memory construction optimizes for the wrong objective.",
    title="Limitation: proxy signal ≠ ground truth decision quality",
)

single_task_evaluation = claim(
    "Evaluation is limited to single-task settings. Multi-task memory "
    "sharing — where the same memory must serve different Y objectives — "
    "is not tested. This is the regime where the IB formulation is most "
    "promising but also most challenging.",
    title="Limitation: single-task evaluation; multi-task untested",
)
