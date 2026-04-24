"""Prior assignments for all independent leaf claims."""

from . import (
    alt_traditional_valid,
    claim_anns_bounded_by_exact,
    claim_cost_rises_sharply,
    claim_cross_val_agreement,
    claim_few_relevant_common,
    claim_irrelevant_equidistant,
    claim_miracl_recall_results,
    claim_miracl_sn_larger_deltas,
    claim_non_sn_harder_to_retrieve,
    claim_recall_comparison_all,
    claim_recall_widespread,
    claim_sn_higher_scores,
    claim_sn_larger_deltas,
    claim_tuning_baseline,
    h_srecall_correct,
    pred_alt_metric,
    pred_h_metric,
    obs_bigann,
    obs_glove,
    obs_msmarco_cost,
    obs_msmarco_srecall,
    obs_miracl_srecall,
)

PRIORS = {
    claim_recall_widespread: (
        0.95,
        "Traditional recall is unambiguously the standard metric for ANNS evaluation "
        "in both academic benchmarks (ANN-Benchmarks) and industry; this is documented "
        "fact, not disputed.",
    ),
    claim_anns_bounded_by_exact: (
        0.97,
        "This follows from the mathematical definition of ANNS: it searches within the "
        "embedding space and is constrained by the embedding model's representation. "
        "Formally established and cited by the embedding limitations paper.",
    ),
    claim_few_relevant_common: (
        0.90,
        "Directly observed in the MSMARCO experiment: 40% of 250 queries have <15 "
        "relevant documents out of top-100. This is a direct measurement, high confidence.",
    ),
    claim_irrelevant_equidistant: (
        0.90,
        "Supported by Table 2 data showing consistently small non-SN score deltas "
        "(0.002±0.003 average) vs. larger SN score deltas. This is a measured property.",
    ),
    claim_sn_higher_scores: (
        0.92,
        "Directly measured in Table 2: SN average score 0.77 vs. non-SN 0.73 across "
        "all queries. Empirical measurement, high confidence.",
    ),
    claim_sn_larger_deltas: (
        0.92,
        "Directly measured in Table 2: SN average score delta 0.006±0.006 vs. non-SN "
        "0.002±0.003. Particularly stark for SN<20 queries (0.014 vs. 0.001). "
        "High confidence from direct measurement.",
    ),
    claim_cross_val_agreement: (
        0.95,
        "Directly measured: Claude Haiku vs. Gemini 2.5 agreement rate of 91.1% with "
        "Cohen's κ=0.82 on 100 queries × 100 documents. This is a reported measurement.",
    ),
    claim_recall_comparison_all: (
        0.93,
        "Directly measured experimental results reported in Table 3 of the paper. "
        "ScaNN with 8-bit quantization on MSMARCO. High confidence from direct measurement.",
    ),
    claim_tuning_baseline: (
        0.92,
        "Directly measured: ScaNN tuned via Google Vizier for 98% traditional recall "
        "achieves 98%, 98.69% tolerant, 98.93% semantic recall. Direct experimental result.",
    ),
    claim_cost_rises_sharply: (
        0.88,
        "Visible in Figure 5 (cost-recall curve shows super-linear growth near high recall). "
        "Well-established property of ANNS cost-recall tradeoffs, consistent with prior work.",
    ),
    claim_non_sn_harder_to_retrieve: (
        0.85,
        "Stated by the authors as the mechanism explaining cost savings from semantic "
        "recall tuning. Plausible given the equidistance property, but not directly "
        "measured with an ablation study.",
    ),
    claim_miracl_recall_results: (
        0.92,
        "Directly measured experimental results: traditional=0.75, semantic=0.85, "
        "tolerant=0.83 on MIRACL Thai with FAISS IVF. Direct experimental measurement.",
    ),
    claim_miracl_sn_larger_deltas: (
        0.90,
        "Directly measured: SN delta 0.05±0.03 vs. non-SN 0.005±0.008 in MIRACL. "
        "10× difference is a clear empirical measurement.",
    ),
    h_srecall_correct: (
        0.80,
        "The paper's main thesis: semantic recall correctly captures retrieval quality. "
        "Prior reflects the strength of the motivation and existing work on retrieval "
        "quality; not fully established until the empirical results are accepted.",
    ),
    alt_traditional_valid: (
        0.25,
        "The alternative that traditional recall is equally valid. Prior is low because "
        "the paper's motivation section provides strong theoretical grounds for why it "
        "is misaligned. The 0.25 reflects the possibility that this view has merit "
        "in some scenarios (e.g., when all results are relevant).",
    ),
    pred_h_metric: (
        0.85,
        "The prediction that semantic recall will score higher for few-SN queries if "
        "it is the correct metric. This prediction follows directly from the semantic "
        "recall mechanism; high confidence it would be correct if the hypothesis holds.",
    ),
    pred_alt_metric: (
        0.20,
        "The prediction that traditional and semantic recall would be similar if "
        "traditional recall is equally valid. Low prior because even a casual "
        "inspection of the mechanism suggests a gap would occur for few-SN queries.",
    ),
    obs_bigann: (
        0.90,
        "Directly measured cost reduction result (~25%) reported in the paper for "
        "BigANN (1B vectors) when switching from 95% traditional to 95% tolerant recall target.",
    ),
    obs_glove: (
        0.90,
        "Directly measured cost reduction (~5%) reported for GloVe (1M vectors) "
        "when switching from 95% traditional to 95% tolerant recall target.",
    ),
    obs_msmarco_cost: (
        0.90,
        "Directly measured cost reduction (~35%) reported for MSMARCO when switching "
        "from 95% traditional to 95% tolerant recall target.",
    ),
    obs_msmarco_srecall: (
        0.93,
        "Directly measured from Table 3: MSMARCO overall semantic recall = 0.932 vs. "
        "traditional recall = 0.863. High confidence from direct experimental measurement.",
    ),
    obs_miracl_srecall: (
        0.92,
        "Directly measured on MIRACL Thai: semantic recall = 0.85 vs. traditional "
        "recall = 0.75. High confidence from direct experimental measurement.",
    ),
}
