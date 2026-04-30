"""Ablation Study: Five-Stage Progressive Evaluation"""

from gaia.lang import claim, setting, support, induction

from .motivation import setting_production_requirements

# --- Settings ---

setting_benchmarks = setting(
    "Evaluation uses two benchmarks: LONGMEMEVAL (500 questions across 6 categories, dialogues up to 1M tokens) and LOCOMO (multi-modal dialogue with single-hop, multi-hop, open domain, temporal reasoning).",
    title="Evaluation benchmarks",
)

setting_ablation_design = setting(
    "Five-stage progressive ablation: Stage 1 (naive baseline, k=10, threshold=0.15, Claude Sonnet 4), Stage 2 (k=40, threshold=0.10), Stage 3 (prompt optimization from Hindsight), Stage 4 (k=100, threshold=0.05), Stage 5 (Gemini 3 inference model).",
    title="Ablation study design",
)

# --- Claims: Stage results ---

claim_stage1_longmem = claim(
    "Stage 1 (naive baseline): Memanto achieves 56.6% accuracy on LONGMEMEVAL.",
    title="Stage 1 LONGMEMEVAL",
)

claim_stage1_locomo = claim(
    "Stage 1 (naive baseline): Memanto achieves 76.2% accuracy on LOCOMO.",
    title="Stage 1 LOCOMO",
)

claim_stage2_longmem = claim(
    "Stage 2 (recall expansion, k=40, threshold=0.10): Memanto achieves 77.0% on LONGMEMEVAL (+20.4 pp), the largest single improvement.",
    title="Stage 2 LONGMEMEVAL",
)

claim_stage2_locomo = claim(
    "Stage 2 (recall expansion): Memanto achieves 82.8% on LOCOMO (+6.6 pp).",
    title="Stage 2 LOCOMO",
)

claim_stage3_longmem = claim(
    "Stage 3 (prompt optimization): 79.2% on LONGMEMEVAL (+2.2 pp), marginal gain.",
    title="Stage 3 LONGMEMEVAL",
)

claim_stage3_locomo = claim(
    "Stage 3 (prompt optimization): 82.9% on LOCOMO (+0.1 pp), negligible gain.",
    title="Stage 3 LOCOMO",
)

claim_stage4_longmem = claim(
    "Stage 4 (maximum recall, k=100, threshold=0.05): 85.0% on LONGMEMEVAL (+5.8 pp).",
    title="Stage 4 LONGMEMEVAL",
)

claim_stage4_locomo = claim(
    "Stage 4 (maximum recall): 86.3% on LOCOMO (+3.4 pp).",
    title="Stage 4 LOCOMO",
)

claim_stage5_longmem = claim(
    "Stage 5 (Gemini 3 inference model): 89.8% on LONGMEMEVAL (+4.8 pp from Stage 4).",
    title="Stage 5 LONGMEMEVAL",
)

claim_stage5_locomo = claim(
    "Stage 5 (Gemini 3 inference model): 87.1% on LOCOMO (+0.8 pp from Stage 4).",
    title="Stage 5 LOCOMO",
)

# --- Key ablation claims ---

claim_recall_over_precision = claim(
    "Recall decisively outweighs precision for agentic memory: Stage 2's recall expansion (k=10→40) produced the largest single improvement (+20.4 pp on LONGMEMEVAL), while Stage 3's prompt optimization added only +2.2 pp. LLMs tolerate noisy retrieval context and benefit more from broader candidate sets than from aggressive filtering.",
    title="Recall outweighs precision",
)

claim_k40_inflection = claim(
    "Recall expansion shows a clear inflection point around k=40 (Figure 6), with diminishing returns beyond this threshold.",
    title="k=40 inflection point",
)

claim_prompt_limited = claim(
    "Prompt engineering offers limited improvement when the underlying retrieval system fails to surface relevant content. Stage 3 gained only +2.2/+0.1 pp across benchmarks.",
    title="Prompt optimization limited",
)

claim_llm_noise_tolerance = claim(
    "Modern LLMs are robust in-context reasoners capable of filtering irrelevant information from expanded retrieval contexts, shifting the engineering focus from pre-computed structural reasoning to efficient semantic recall.",
    title="LLM noise tolerance",
)

claim_inference_model_matters = claim(
    "Upgrading the inference model from Claude Sonnet 4 to Gemini 3 added +4.8 pp on LONGMEMEVAL, isolating the inference model's contribution from the memory architecture.",
    title="Inference model contribution",
)

# --- Strategies ---

strat_recall_over_precision = support(
    [claim_stage2_longmem, claim_stage2_locomo, claim_stage3_longmem, claim_stage3_locomo],
    claim_recall_over_precision,
    reason="Stage 2 recall expansion (+20.4/+6.6 pp, @claim_stage2_longmem, @claim_stage2_locomo) dwarfs Stage 3 prompt optimization (+2.2/+0.1 pp, @claim_stage3_longmem, @claim_stage3_locomo). The 10x difference in improvement magnitude demonstrates that providing broader context to the LLM outweighs refining the retrieval filter.",
    prior=0.92,
)

strat_k40_inflection = support(
    [claim_stage2_longmem, claim_stage4_longmem],
    claim_k40_inflection,
    reason="Stage 2 (k=40) gave +20.4 pp while Stage 4 (k=100) gave only +5.8 pp additional (@claim_stage2_longmem, @claim_stage4_longmem). The marginal gain per additional chunk drops sharply after k≈40.",
    prior=0.85,
)

strat_prompt_limited = support(
    [claim_stage3_longmem, claim_stage3_locomo],
    claim_prompt_limited,
    reason="Stage 3 prompt optimization yielded negligible improvements (+2.2/+0.1 pp, @claim_stage3_longmem, @claim_stage3_locomo) compared to recall expansion, indicating that once retrieval surfaces relevant content, prompt refinement has limited leverage.",
    prior=0.90,
)

strat_llm_noise_tolerance = support(
    [claim_recall_over_precision],
    claim_llm_noise_tolerance,
    reason="The fact that recall expansion with noisier contexts consistently improves accuracy (@claim_recall_over_precision) implies the LLM can filter noise. If the LLM were noise-sensitive, broader retrieval would hurt, not help.",
    prior=0.82,
)
