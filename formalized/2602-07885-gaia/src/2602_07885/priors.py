"""Prior assignments for all independent leaf claims in the MEMFLY package."""

from .motivation import (
    claim_retrieval_centric_redundancy,
    claim_memory_augmented_fidelity_loss,
    claim_ib_aligns_with_memory,
    claim_high_dim_curse,
)
from .s3_framework import (
    claim_y_unknown_at_construction,
    claim_llm_implicit_knowledge,
    claim_notes_preserve_fidelity,
    claim_link_preserves_relevance,
    claim_append_preserves_diversity,
    claim_extends_aib,
    claim_merge_reduces_compression,
)
from .s3_retrieval import (
    claim_ier_protocol,
)
from .s4_experiments import (
    claim_avg_gpt4omini,
    claim_avg_gpt4o,
    claim_avg_qwen8b,
    claim_avg_qwen14b,
    claim_ablation_full,
    claim_ablation_no_update,
    claim_ablation_no_link,
    claim_ablation_no_merge,
    claim_ablation_no_denoise,
    claim_ablation_no_topic,
    claim_ablation_no_keyword,
    claim_ablation_no_neighbor,
    claim_ablation_no_ier,
    claim_baselines_optimal_alt,
)

PRIORS = {
    # ── Motivation: existing-paradigm characterizations ──────────────────────
    claim_retrieval_centric_redundancy: (
        0.90,
        "Well-documented characterization of retrieval-centric (RAG) systems in "
        "the literature; multiple cited surveys (Lewis 2021, Gao 2024, Asai 2023) "
        "explicitly identify redundancy and vector dilution issues.",
    ),
    claim_memory_augmented_fidelity_loss: (
        0.85,
        "Acknowledged limitation of LLM-summarization-based memory systems "
        "(MemGPT, MemoryBank, A-MEM, O-Mem). Less unanimously characterized than "
        "RAG redundancy but well established in the cited works.",
    ),
    claim_ib_aligns_with_memory: (
        0.85,
        "Plausible theoretical alignment, but the IB-to-agentic-memory bridge is "
        "the paper's framing rather than a pre-existing result. Strong but not "
        "fully established.",
    ),
    claim_high_dim_curse: (
        0.93,
        "Curse of dimensionality is a textbook fact in high-dimensional similarity "
        "search; cited Slonim & Tishby 2000 establishes the sparsity issue formally.",
    ),

    # ── Framework: foundational claims about IB construction ─────────────────
    claim_y_unknown_at_construction: (
        0.95,
        "Self-evident in the streaming online setting: at construction time, no "
        "future query has been issued, so p(Y|z) is literally unobservable.",
    ),
    claim_llm_implicit_knowledge: (
        0.78,
        "Consistent with extensive literature on LLM-as-judge and LLM-as-optimizer "
        "(Yang et al. 2024). The specific link to JS-divergence approximation is "
        "an analogical hypothesis, not a theorem.",
    ),
    claim_notes_preserve_fidelity: (
        0.92,
        "Direct architectural property: Notes store verbatim raw content r_i, so "
        "the I(N; X) ≈ H(X) condition holds approximately by construction.",
    ),
    claim_link_preserves_relevance: (
        0.78,
        "The Information-theoretic interpretation (Remark 3.2) is plausible but "
        "framed as a hypothesis (the trigger condition I(n_t; Y | n_i) > 0 cannot "
        "be directly evaluated; LLM scores are a heuristic). Ablation supports it.",
    ),
    claim_append_preserves_diversity: (
        0.85,
        "Direct architectural property: APPEND introduces a new node, preserving "
        "novel content. Diversity preservation is operationally clear.",
    ),
    claim_extends_aib: (
        0.92,
        "Factual statement about the algorithmic extension: original AIB is merge-"
        "only, MEMFLY adds Link and Append. Trivially true at the algorithmic level.",
    ),
    claim_ier_protocol: (
        0.92,
        "The IER protocol is described algorithmically with a clear sufficiency "
        "predicate and refinement loop. The architectural description is "
        "unambiguous; high confidence in the protocol statement.",
    ),
    claim_merge_reduces_compression: (
        0.92,
        "Direct algorithmic property: MERGE reduces |V_t|, which mechanically "
        "reduces I(X_{1:t}; M_t) under any reasonable measure. Mathematically clear.",
    ),

    # ── Experiments: per-backbone results (Tables 1 & 2) ─────────────────────
    claim_avg_gpt4omini: (
        0.93,
        "Direct experimental measurement reported in Table 1; high confidence "
        "from a controlled benchmark with standard metrics.",
    ),
    claim_avg_gpt4o: (
        0.93,
        "Direct experimental measurement reported in Table 1; high confidence.",
    ),
    claim_avg_qwen8b: (
        0.93,
        "Direct experimental measurement reported in Table 2; high confidence.",
    ),
    claim_avg_qwen14b: (
        0.92,
        "Direct experimental measurement reported in Table 2; slightly lower "
        "confidence because Qwen3-14B's MEMFLY win margin is smaller and "
        "category-specific (e.g., Single Hop dominates Adversarial loss).",
    ),

    # ── Experiments: ablation rows (Table 3, Qwen3-8B) ───────────────────────
    claim_ablation_full: (
        0.93,
        "Direct experimental measurement of the full MEMFLY system on Qwen3-8B; "
        "this is the reference row in Table 3.",
    ),
    claim_ablation_no_update: (
        0.92,
        "Direct experimental ablation; large effect size (10.65 F1 drop) makes "
        "the measurement robust against noise.",
    ),
    claim_ablation_no_link: (
        0.90,
        "Direct experimental ablation; consistent with the design rationale that "
        "Link preserves multi-hop conditional structure.",
    ),
    claim_ablation_no_merge: (
        0.90,
        "Direct experimental ablation; smaller effect than w/o Link but clearly "
        "above noise floor.",
    ),
    claim_ablation_no_denoise: (
        0.88,
        "Direct experimental ablation; the smallest construction-phase effect, "
        "consistent with denoising being auxiliary.",
    ),
    claim_ablation_no_topic: (
        0.90,
        "Direct experimental ablation reporting F1 = 36.79; second-best retrieval "
        "ablation.",
    ),
    claim_ablation_no_keyword: (
        0.90,
        "Direct experimental ablation reporting F1 = 32.69; the largest retrieval-"
        "phase drop.",
    ),
    claim_ablation_no_neighbor: (
        0.90,
        "Direct experimental ablation reporting F1 = 34.26; primarily affects "
        "Adversarial.",
    ),
    claim_ablation_no_ier: (
        0.90,
        "Direct experimental ablation reporting F1 = 32.94; affects Adversarial "
        "and Open Domain most strongly.",
    ),

    # ── Alternative hypothesis (low prior) ───────────────────────────────────
    claim_baselines_optimal_alt: (
        0.15,
        "Implausible given the diversity of baselines and the consistent margin "
        "across four backbones. Low prior reflects the strong empirical evidence "
        "against this view.",
    ),
}
