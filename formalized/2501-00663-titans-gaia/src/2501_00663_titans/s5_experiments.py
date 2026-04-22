"""Section 5: Experimental Results"""

from gaia.lang import claim, setting, support, compare, abduction, induction

from .motivation import (
    transformer_quadratic_cost,
    linear_recurrent_compression_problem,
    deep_memory_expressiveness,
)
from .s3_neural_memory import (
    forgetting_mechanism_claim,
    forgetting_generalizes_rnn_gates,
    parallel_training_claim,
    momentum_motivation,
    alt_momentary_surprise,
    persistent_memory_claim,
)
from .s4_architecture import (
    titans_three_memory_types,
    mac_advantages,
    mal_limitation,
    titans_expressiveness_theorem,
    mac_architecture_def,
    mag_architecture_def,
    mal_architecture_def,
)

# ── Settings ──────────────────────────────────────────────────────────────────

experimental_setup = setting(
    "Experimental setup for Titans: four model scales are evaluated — 170M, 340M, 400M, and 760M parameters. "
    "The first three are trained on 15B tokens from FineWeb-Edu dataset; the 760M model on 30B tokens. "
    "Training uses AdamW optimizer with learning rate 4e-4, cosine annealing, batch size 0.5M tokens, "
    "weight decay 0.1, and LLaMA 2 tokenizer with 32K vocabulary. Training context length is 4K tokens [@Behrouz2025].",
    title="Training setup",
)

niah_task_def = setting(
    "The Single Needle-in-a-Haystack (S-NIAH) task from the RULER benchmark [@Hsieh2024] evaluates "
    "the effective context length of models. A model must retrieve a specific piece of information "
    "(the needle) from long distractor text (the haystack) at sequence lengths of 2K, 4K, 8K, and 16K tokens. "
    "Three subtasks: S-NIAH-PK (passkey retrieval), S-NIAH-N (number retrieval), S-NIAH-W (word retrieval).",
    title="S-NIAH task definition",
)

babilong_task_def = setting(
    "The BABILong benchmark [@Kuratov2024] evaluates reasoning across facts distributed in extremely long "
    "documents, requiring multi-hop inference over sequences that may span millions of tokens. "
    "Two settings: (1) few-shot (large pre-trained models), (2) fine-tuning (small models fine-tuned).",
    title="BABILong benchmark definition",
)

# ── Experimental results (claims) ────────────────────────────────────────────

lm_results_340m = claim(
    "At 340M parameters / 15B tokens, Titans (LMM alone) achieves WikiText perplexity 26.18 "
    "and LambadA perplexity 29.97, outperforming all non-hybrid baselines including Gated DeltaNet "
    "(27.01 / 30.94) and TTT (27.44 / 34.19). Titans (MAC) achieves 25.43 / 28.13 and "
    "Titans (MAG) achieves 25.07 / 28.72, with both hybrid Titans variants outperforming "
    "non-hybrid baselines on all metrics. Avg. commonsense reasoning accuracy: Titans (MAG) 47.54%, "
    "Titans (MAC) 47.36%, vs. Gated DeltaNet 45.42% (best non-hybrid) (Table 1) [@Behrouz2025].",
    title="Language modeling results at 340M params",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 1"},
)

lm_results_760m = claim(
    "At 760M parameters / 30B tokens, Titans (MAG) achieves WikiText perplexity 18.61 and "
    "LambadA perplexity 19.86, Titans (MAC) achieves 19.93 / 20.12, both outperforming "
    "all baselines including Gated DeltaNet-H2 (19.88 / 20.83, hybrid) and Samba (20.63 / 22.71, hybrid). "
    "Avg. commonsense accuracy: Titans (MAC) 52.51%, Titans (MAG) 52.50%, vs. "
    "Gated DeltaNet-H2 51.49%, Samba 51.08% (Table 1) [@Behrouz2025].",
    title="Language modeling results at 760M params",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 1"},
)

lm_baseline_results = claim(
    "Best competing baseline results (760M): Gated DeltaNet-H2 (hybrid) achieves WikiText perplexity "
    "19.88, LambadA perplexity 20.83, avg. commonsense accuracy 51.49%; "
    "Samba (hybrid) achieves 20.63 / 22.71 / 51.08%. Among non-hybrid baselines at 760M, "
    "Gated DeltaNet achieves WikiText 21.18, avg. accuracy 49.69% (Table 1) [@Behrouz2025].",
    title="Baseline language modeling results (760M)",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 1"},
)

niah_results = claim(
    "On the S-NIAH task from RULER at context lengths 2K–16K tokens (Table 2), "
    "Titans (LMM) achieves S-NIAH-N: 100.0/99.8/93.4/80.2 and S-NIAH-W: 90.4/89.4/85.8/80.6, "
    "dramatically outperforming TTT (S-NIAH-N: 60.2/36.6/10.2/4.4) and Mamba2 (98.4/55.8/14.2/0.0). "
    "Titans (MAC) achieves S-NIAH-W: 98.2/98.2/95.6/95.2 at 2K/4K/8K/16K contexts, "
    "maintaining near-perfect accuracy even at 16K tokens [@Behrouz2025].",
    title="S-NIAH benchmark results",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 2"},
)

babilong_results = claim(
    "On the BABILong benchmark in the few-shot setting, Titans (MAC) outperforms all baselines "
    "including Mamba2.8B, RWKV-6-7B, RecurrentGemma-9B, Gemma-9B, Llama3.1-8B, GPT-4, and GPT-4o-mini, "
    "while having significantly fewer parameters. In the fine-tuning setting, a small fine-tuned "
    "Titans (MAC) outperforms GPT-4, Qwen2.5-72B, Llama3.1-70B, and Llama3.1-8B with RAG "
    "(approx. 70x more parameters for the RAG baseline) (Figure 6) [@Behrouz2025; @Kuratov2024].",
    title="BABILong benchmark results",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Figure 6"},
)

time_series_results = claim(
    "On long-term time series forecasting benchmarks (ETTm1, ETTm2, ETTh1, ETTh2, ECL, Traffic, Weather), "
    "the Neural Memory Module achieves the best Mean Squared Error (MSE) and Mean Absolute Error (MAE) "
    "across all 7 datasets compared to Simba, iTransformer, RLinear, PatchTST, Crossformer, TiDE, "
    "TimesNet, and DLinear (Table 3). Selected results: ETTm1 MSE 0.358 (vs. Simba 0.383), "
    "Traffic MSE 0.415 (vs. Simba 0.493), Weather MSE 0.231 (vs. Simba 0.255) [@Behrouz2025].",
    title="Time series forecasting results",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 3"},
)

dna_results = claim(
    "On GenomicsBenchmarks DNA modeling tasks (Table 4), the Neural Memory Module (Titans LMM) "
    "achieves competitive or best-in-class accuracy across 5 tasks: Enhancer Cohn 75.2% "
    "(vs. HyenaDNA 74.2%), Enhancer Ens 89.6% (vs. Based 89.5%), Human Reg. 89.3% "
    "(vs. HyenaDNA 93.8%, slightly lower), Non-TATA Promoters 96.6% (tied with HyenaDNA/Mamba), "
    "Human OCR Ens. 79.9% (vs. HyenaDNA 80.9%, slightly lower) [@Behrouz2025].",
    title="DNA modeling results on GenomicsBenchmarks",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 4"},
)

deep_memory_ablation = claim(
    "Ablation on memory depth $L_{\\mathcal{M}} \\in \\{1, 2, 3, 4\\}$ (Figure 7) shows: "
    "(1) deeper memory consistently achieves lower perplexity at all sequence lengths and model sizes "
    "(170M, 360M, 760M parameters); (2) deeper memory is more robust to longer sequences, "
    "especially at smaller model sizes; (3) training throughput degrades linearly with depth "
    "(Figure 8): all depth variants scale linearly with context length (constant tokens/second), "
    "but deeper models produce fewer tokens/second (approx. 40K for $L=1$, approx. 27K for $L=4$ "
    "at 16K context length). This reveals a depth-efficiency tradeoff [@Behrouz2025].",
    title="Deep memory ablation results (depth vs. performance vs. throughput)",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Figures 7-8"},
)

component_ablation = claim(
    "Full ablation study (Table 5, 400M LMM base model) shows all components positively contribute:\n\n"
    "| Model variant | Lang. ppl | Reasoning acc | Long-ctx acc |\n"
    "|---------------|-----------|---------------|---------------|\n"
    "| LMM (full) | 27.01 | 47.83% | 92.68% |\n"
    "| Linear Memory | 28.49 | 46.97% | 85.34% |\n"
    "| w/o Convolution | 28.73 | 45.82% | 90.28% |\n"
    "| w/o Momentum | 28.98 | 45.49% | 87.12% |\n"
    "| w/o Weight Decay | 29.04 | 45.11% | 85.60% |\n"
    "| w/o Persistent Memory | 27.63 | 46.35% | 92.49% |\n\n"
    "Greatest contributions (perplexity degradation): weight decay (+2.03), momentum (+1.97), "
    "convolution (+1.72), persistent memory (+0.62) [@Behrouz2025].",
    title="Full component ablation results",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 5"},
)

architecture_design_ablation = claim(
    "Comparing Titans architectural variants (Table 5, 400M scale):\n\n"
    "| Variant | Lang. ppl | Reasoning acc | Long-ctx (BABILong) acc |\n"
    "|---------|-----------|---------------|-------------------------|\n"
    "| LMM (no attn) | 27.01 | 47.83% | 92.68% |\n"
    "| +Attn (MAC) | 26.67 | 48.65% | 97.95% |\n"
    "| +Attn (MAG) | 25.70 | 48.60% | 96.70% |\n"
    "| +Attn (MAL) | 25.91 | 47.87% | 96.91% |\n\n"
    "MAC achieves the best long-context performance (97.95% vs MAG 96.70%); "
    "MAG achieves the best language modeling perplexity (25.70 vs MAC 26.67); "
    "MAG and MAC outperform MAL on all metrics [@Behrouz2025].",
    title="Architecture variant ablation (MAC vs MAG vs MAL)",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 5"},
)

efficiency_results = claim(
    "Training throughput comparison (Figure 9, tokens per second vs. sequence length × batch size): "
    "Neural Memory module is slightly slower than Mamba2 and Gated DeltaNet due to deeper memory "
    "and less optimized kernels. Titans (MAL) is faster than both the memory module alone and "
    "all baselines, attributed to the highly optimized FlashAttention [@DaoGu2024] kernel used "
    "for implementing sliding window attention. All models (recurrent variants) scale linearly "
    "with context length in training throughput [@Behrouz2025].",
    title="Training efficiency and throughput results",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Figure 9"},
)

# ── Strategies connecting design to outcomes ──────────────────────────────────

strat_lm_superiority_from_design = support(
    [forgetting_mechanism_claim, momentum_motivation, deep_memory_expressiveness],
    lm_results_760m,
    reason=(
        "Three design choices jointly explain Titans' language modeling superiority over baselines: "
        "(1) Weight decay (@forgetting_mechanism_claim) — enables selective forgetting, better memory "
        "management than TTT (no forgetting); (2) Momentum (@momentum_motivation) — maintains "
        "informational continuity, outperforming TTT; (3) Deep non-linear memory "
        "(@deep_memory_expressiveness) — can represent non-linear historical dependencies, "
        "outperforming linear models. The 760M Titans (MAG) achieves WikiText ppl 18.61 vs. "
        "Gated DeltaNet-H2 19.88 as the best competing hybrid baseline."
    ),
    prior=0.82,
)

strat_niah_from_forgetting = support(
    [forgetting_mechanism_claim, deep_memory_expressiveness, mac_advantages],
    niah_results,
    reason=(
        "The dramatic NIAH advantage of Titans over baselines is explained by three mechanisms: "
        "(1) @forgetting_mechanism_claim allows clearing irrelevant memory as context changes, "
        "so the needle remains retrievable even after thousands of distractor tokens — "
        "unlike Mamba2 which loses S-NIAH-N accuracy from 98.4% at 2K to 0% at 16K; "
        "(2) @deep_memory_expressiveness enables more precise storage and retrieval of specific "
        "facts compared to linear matrix memory; (3) @mac_advantages — attention guides memory "
        "to store only useful information, preventing overflow of distractors."
    ),
    prior=0.85,
)

strat_babilong_from_design = support(
    [mac_advantages, forgetting_mechanism_claim, parallel_training_claim],
    babilong_results,
    reason=(
        "BABILong requires reasoning across facts in extremely long documents. "
        "@mac_advantages gives MAC access to both historical memory retrieval and current "
        "context simultaneously, enabling multi-hop reasoning across segments. "
        "@forgetting_mechanism_claim prevents memory overflow from distractor text between "
        "relevant facts. @parallel_training_claim enables efficient training on very long sequences. "
        "The result (small fine-tuned Titans outperforming GPT-4 and 70B models) validates that "
        "architectural memory design matters more than raw parameter count."
    ),
    prior=0.80,
)

strat_deep_mem_ablation_from_expressiveness = support(
    [deep_memory_expressiveness],
    deep_memory_ablation,
    reason=(
        "@deep_memory_expressiveness (MLPs with $L \\geq 2$ are universal approximators, hence "
        "strictly more expressive than linear matrix memory) predicts that deeper memory should "
        "achieve better perplexity by capturing non-linear historical dependencies. "
        "The ablation results in Figure 7 confirm this: perplexity decreases monotonically "
        "with depth $L_{\\mathcal{M}}$ across all model sizes and sequence lengths. "
        "The linear throughput cost of depth (Figure 8) confirms this is a genuine "
        "expressiveness-efficiency tradeoff."
    ),
    prior=0.90,
)

strat_component_ablation_confirms_design = support(
    [forgetting_mechanism_claim, momentum_motivation, persistent_memory_claim],
    component_ablation,
    reason=(
        "Each ablated component directly corresponds to a theoretical claim: "
        "(1) 'w/o Weight Decay' tests @forgetting_mechanism_claim — greatest perplexity increase "
        "(27.01 → 29.04); (2) 'w/o Momentum' tests @momentum_motivation — second largest increase "
        "(27.01 → 28.98); (3) 'w/o Persistent Memory' tests @persistent_memory_claim — smallest "
        "increase (27.01 → 27.63). The rank order of ablation impact matches the theoretical "
        "importance ranking."
    ),
    prior=0.88,
)

# ── Induction: Titans performance across diverse tasks ────────────────────────

law_titans_effective = claim(
    "Titans (LMM and its variants MAC, MAG, MAL) are more effective than Transformers and "
    "modern linear recurrent models across diverse sequence modeling tasks, and can effectively "
    "scale to context windows larger than 2M tokens with maintained accuracy [@Behrouz2025].",
    title="Core claim: Titans effectiveness across tasks",
)

obs_lm_effective = claim(
    "Empirical observation: Titans outperform all non-hybrid and hybrid baselines on language "
    "modeling perplexity and commonsense reasoning accuracy at 340M, 400M, and 760M parameter "
    "scales (Table 1) [@Behrouz2025].",
    title="Observation: Titans LM superiority",
)

obs_niah_effective = claim(
    "Empirical observation: Titans maintain near-perfect S-NIAH accuracy (>80% on all subtasks) "
    "at context lengths up to 16K tokens, while baselines (TTT, Mamba2, DeltaNet) degrade "
    "to near-zero at 16K (Table 2) [@Behrouz2025].",
    title="Observation: Titans NIAH superiority",
)

obs_ts_effective = claim(
    "Empirical observation: Neural Memory Module achieves best-in-class MSE and MAE on all 7 "
    "time series forecasting benchmark datasets (Table 3) [@Behrouz2025].",
    title="Observation: Titans time series superiority",
)

s_lm = support(
    [law_titans_effective],
    obs_lm_effective,
    reason="The law (@law_titans_effective) predicts Titans should outperform baselines on language modeling — the observed results confirm this at all three model scales.",
    prior=0.88,
)

s_niah = support(
    [law_titans_effective],
    obs_niah_effective,
    reason="The law (@law_titans_effective) predicts Titans should scale to long contexts effectively — the NIAH results confirm near-perfect retrieval at 16K tokens vs. near-zero for baselines.",
    prior=0.92,
)

s_ts = support(
    [law_titans_effective],
    obs_ts_effective,
    reason="The law (@law_titans_effective) predicts generalization beyond language — time series forecasting results confirm this with best-in-class results across 7 datasets.",
    prior=0.85,
)

ind_lm_niah = induction(
    s_lm, s_niah,
    law=law_titans_effective,
    reason="Language modeling and NIAH are independent tasks with different evaluation criteria; their joint confirmation provides stronger inductive support.",
)

ind_all_tasks = induction(
    ind_lm_niah, s_ts,
    law=law_titans_effective,
    reason="Time series forecasting provides cross-domain evidence independent of NLP tasks, strengthening the inductive case that Titans' advantages generalize across modalities.",
)

# ── MAC vs. MAG comparison for long contexts ─────────────────────────────────

pred_mac_long_context = claim(
    "MAC architecture predicts better performance on long-context tasks than MAG, because "
    "MAC provides attention full access to retrieved long-term memory context, enabling "
    "more accurate multi-hop reasoning across segments [@Behrouz2025].",
    title="Prediction: MAC better for long contexts",
)

pred_mag_short_context = claim(
    "MAG architecture predicts competitive performance with MAC on language modeling and "
    "short-context tasks, but potentially weaker performance on very long-context tasks "
    "since it combines memory and attention outputs via gating rather than joint attention [@Behrouz2025].",
    title="Prediction: MAG competitive on short contexts",
)

obs_architecture_comparison = claim(
    "Observed: MAC achieves significantly better BABILong long-context accuracy (97.95%) than "
    "MAG (96.70%) and MAL (96.91%); MAG achieves slightly better language modeling perplexity "
    "(25.70) than MAC (26.67) at 400M scale (Table 5). At 760M scale, MAC and MAG achieve "
    "comparable commonsense accuracy (52.51% vs. 52.50%) but MAC has higher LambadA accuracy "
    "(20.12 vs. 19.86) while MAG has lower WikiText perplexity (18.61 vs. 19.93) [@Behrouz2025].",
    title="Observation: MAC vs. MAG performance",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Tables 1, 5"},
)

s_mac_better = support(
    [mac_advantages],
    obs_architecture_comparison,
    reason="@mac_advantages predicts MAC's joint attention over historical + current context gives it an edge on long-context tasks — confirmed by BABILong superiority (97.95% vs. 96.70% for MAG).",
    prior=0.80,
)

s_mag_competitive = support(
    [mag_architecture_def],
    obs_architecture_comparison,
    reason="@mag_architecture_def's parallel gating (SWA + neural memory, no chunking overhead) predicts efficiency advantages — confirmed by MAG's better language modeling perplexity (25.70 vs. 26.67).",
    prior=0.65,
)

comp_mac_mag = compare(
    pred_mac_long_context, pred_mag_short_context, obs_architecture_comparison,
    reason="MAC's long-context advantage (BABILong +1.25pp) is larger than MAG's language modeling advantage (perplexity -0.97), suggesting MAC's joint-attention design is the stronger architectural innovation.",
    prior=0.75,
)

abduction_mac_mag = abduction(
    s_mac_better, s_mag_competitive, comp_mac_mag,
    reason="Both MAC and MAG aim to explain the same experimental observations; abduction asks which architectural hypothesis better accounts for the performance patterns across task types.",
)
