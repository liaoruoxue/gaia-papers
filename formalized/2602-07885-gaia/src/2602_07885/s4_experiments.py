"""Section 4: Experimental Evaluation on LoCoMo"""

from gaia.lang import claim, setting, support, contradiction, induction

from .motivation import claim_compression_fidelity_dilemma
from .s3_framework import (
    claim_three_layer_hierarchy,
    claim_gated_three_ops,
    claim_link_preserves_relevance,
    claim_merge_reduces_compression,
    claim_ingestion_denoises,
    claim_topics_enable_navigation,
    claim_keywords_resolve_sparsity,
    claim_proxy_signals,
)
from .s3_retrieval import (
    claim_tripath_addresses_query_diversity,
    claim_macro_semantic_path,
    claim_micro_symbolic_path,
    claim_topological_path,
    claim_ier_protocol,
    claim_ier_handles_multihop,
)

# ── Settings: experimental setup ──────────────────────────────────────────────

setup_locomo = setting(
    "LoCoMo benchmark [@Maharana2024] is a long-horizon conversation dataset designed "
    "to assess the long-term information synthesis capabilities of LLM agents. It "
    "contains conversations with interleaved topics and evolving entity states, and "
    "covers five reasoning categories: Multi-Hop, Temporal, Open Domain, Single Hop, "
    "and Adversarial.",
    title="LoCoMo benchmark",
)

setup_metrics = setting(
    "Evaluation uses two primary metrics following [@Xu2025]: F1 (token-level overlap "
    "and precision of answer spans) and BLEU-1 [@Papineni2002] (lexical fidelity of "
    "generated responses against ground truth). Ablation additionally reports Recall "
    "(proportion of ground-truth evidence retrieved) and Hit Rate (whether any "
    "relevant evidence appears in candidates).",
    title="Evaluation metrics",
)

setup_implementation = setting(
    "MEMFLY is implemented using a triple-layer graph architecture backed by Neo4j, "
    "integrating both vector indices and explicit topological relationships. "
    "Retrieval hyperparameters: K_topic = 3, K_key = 10, K_final = 20, 1-hop "
    "expansion along E_RELATED, I_max = 3 IER iterations. Construction "
    "hyperparameters: merge threshold tau_m = 0.7 and link threshold tau_l = 0.5 "
    "(set via validation). Backbones: GPT-4o-mini, GPT-4o, Qwen3-8B, Qwen3-14B "
    "with temperature 0.7 (general) / 0.5 (adversarial). Baselines: LOCOMO, "
    "READAGENT, MEMORYBANK, MEMGPT, A-MEM, MEM-0 with their official defaults.",
    title="MEMFLY implementation and hyperparameters",
)

# ── Claims: main empirical results (Tables 1 & 2) ────────────────────────────

claim_avg_gpt4omini = claim(
    "On LoCoMo with GPT-4o-mini, MEMFLY achieves the highest average F1 = 43.76% "
    "and BLEU-1 = 37.27%, outperforming the strongest baseline (A-MEM at 41.97% F1) "
    "by 1.79 F1 points. Per category MEMFLY achieves: Multi-Hop F1 = 32.11, "
    "Temporal F1 = 46.61, Open Domain F1 = 23.98, Single Hop F1 = 44.74, "
    "Adversarial F1 = 51.48 [@Kuffo2026, Table 1].",
    title="GPT-4o-mini results on LoCoMo",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 1"},
)

claim_avg_gpt4o = claim(
    "On LoCoMo with GPT-4o, MEMFLY achieves average F1 = 44.39% and BLEU = 38.70%, "
    "topping all six baselines. The best baseline (LOCOMO) reaches F1 = 44.12; "
    "MEMFLY exceeds it by 0.27 F1 points. MEMFLY tops Multi-Hop (35.89), Open "
    "Domain (25.74), and ties or leads in Temporal (39.78), with strong Single Hop "
    "(49.08) and Adversarial (48.24) results [@Kuffo2026, Table 1].",
    title="GPT-4o results on LoCoMo",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 1"},
)

claim_avg_qwen8b = claim(
    "On LoCoMo with Qwen3-8B, MEMFLY achieves average F1 = 38.62% and BLEU = "
    "34.51%, surpassing the second-best A-MEM (32.76% F1) by 5.86 F1 points. "
    "Per category: Multi-Hop 28.24, Temporal 38.39, Open Domain 15.43, Single Hop "
    "42.09, Adversarial 43.79 [@Kuffo2026, Table 2].",
    title="Qwen3-8B results on LoCoMo",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 2"},
)

claim_avg_qwen14b = claim(
    "On LoCoMo with Qwen3-14B, MEMFLY achieves average F1 = 33.65% and BLEU = "
    "28.45%, the highest across all six baselines. Per category: Multi-Hop 30.80, "
    "Temporal 29.25, Open Domain 14.11, Single Hop 42.25, Adversarial 26.59 "
    "[@Kuffo2026, Table 2].",
    title="Qwen3-14B results on LoCoMo",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 2"},
)

claim_open_source_advantage_larger = claim(
    "MEMFLY's improvement margin over the strongest baseline is larger for open-"
    "source models (Qwen3-8B: +5.86 F1 over A-MEM) than for closed-source models "
    "(GPT-4o-mini: +1.79; GPT-4o: +0.27). This pattern suggests that structured "
    "memory organization compensates more strongly for weaker in-context reasoning "
    "capabilities in smaller / open-source models [@Kuffo2026].",
    title="Open-source models benefit more from structured memory",
)

claim_consistent_across_backbones = claim(
    "MEMFLY achieves the highest average F1 across all four foundation models "
    "evaluated (GPT-4o-mini, GPT-4o, Qwen3-8B, Qwen3-14B), demonstrating that the "
    "improvements generalize across heterogeneous architectures [@Kuffo2026].",
    title="Consistent improvements across backbones",
)

claim_open_domain_gain = claim(
    "MEMFLY achieves the largest gain on Open Domain queries on GPT-4o (25.74% F1 "
    "vs. MEM-0 at 17.73%), an improvement attributable to Topic-based macro-"
    "semantic navigation localizing relevant memory regions before fine-grained "
    "retrieval [@Kuffo2026].",
    title="Open Domain F1 gain attributed to Topic navigation",
)

claim_single_hop_qwen = claim(
    "MEMFLY achieves the top Single Hop F1 on both Qwen models (Qwen3-8B: 42.09; "
    "Qwen3-14B: 42.25), indicating effective Keyword-based anchoring for queries "
    "that require precise entity matching [@Kuffo2026].",
    title="Single Hop F1 attributed to Keyword anchoring",
)

# ── Claims: ablation study (Table 3) ─────────────────────────────────────────

claim_ablation_full = claim(
    "Full MEMFLY (Qwen3-8B) achieves F1 = 38.62, BLEU = 36.85, Recall = 62.22, "
    "Hit Rate = 67.12 on LoCoMo, serving as the ablation reference point "
    "[@Kuffo2026, Table 3].",
    title="MEMFLY full ablation reference",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_update = claim(
    "Removing the entire gated structural update (w/o Update) causes the most severe "
    "degradation: F1 drops from 38.62% to 27.97%, Recall from 62.22% to 42.11%. "
    "Adversarial and Temporal categories show the most pronounced decline. This "
    "confirms that without active consolidation, noise accumulates and temporal "
    "dependencies are disrupted [@Kuffo2026, Figure 2(a)].",
    title="Ablation: w/o Update — most severe degradation",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_link = claim(
    "Disabling the Link operation (w/o Link) drops F1 to 33.57%, larger impact than "
    "w/o Merge (34.79%). Figure 2(a) shows Link removal particularly affects "
    "Adversarial performance, indicating that associative edges are critical for "
    "filtering distractors [@Kuffo2026, Table 3, Figure 2(a)].",
    title="Ablation: w/o Link — Adversarial impact",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_merge = claim(
    "Disabling the Merge operation (w/o Merge) drops F1 to 34.79%, demonstrating "
    "the importance of redundancy consolidation but with smaller magnitude than "
    "removing Link (33.57%) [@Kuffo2026, Table 3].",
    title="Ablation: w/o Merge",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_denoise = claim(
    "Disabling semantic denoising (w/o Denoise) yields F1 = 36.07%, the second-best "
    "construction-phase ablation. Performance remains relatively stable across all "
    "categories, suggesting that denoising provides consistent but auxiliary "
    "improvements [@Kuffo2026, Table 3].",
    title="Ablation: w/o Denoise — auxiliary contribution",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_topic = claim(
    "Disabling Topic-based macro retrieval (w/o Topic) yields F1 = 36.79% — the "
    "second-best retrieval ablation — with relatively uniform degradation across "
    "categories. This indicates Topics provide general retrieval guidance rather "
    "than category-specific support [@Kuffo2026, Figure 2(b)].",
    title="Ablation: w/o Topic — uniform but mild degradation",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_keyword = claim(
    "Disabling Keyword-based micro retrieval (w/o Keyword) yields F1 = 32.69%, the "
    "largest retrieval-phase drop. Single-Hop queries show the most pronounced "
    "decline, validating that symbolic anchoring is essential for precise entity "
    "matching [@Kuffo2026, Figure 2(b)].",
    title="Ablation: w/o Keyword — Single-Hop impact",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_neighbor = claim(
    "Disabling topological E_RELATED expansion (w/o Neighbor) yields F1 = 34.26%, "
    "primarily impacting Adversarial. This confirms that topological expansion via "
    "associative edges helps distinguish relevant evidence from distractors "
    "[@Kuffo2026, Figure 2(b)].",
    title="Ablation: w/o Neighbor — Adversarial impact",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

claim_ablation_no_ier = claim(
    "Disabling Iterative Evidence Refinement (w/o IER) yields F1 = 32.94%, with the "
    "largest degradation on Adversarial and Open Domain categories. This "
    "demonstrates IER is critical for queries requiring progressive evidence "
    "accumulation [@Kuffo2026, Figure 2(b)].",
    title="Ablation: w/o IER — multi-hop impact",
    metadata={"source_table": "artifacts/2602.07885.pdf, Table 3"},
)

# ── Claims: derived ablation conclusions ─────────────────────────────────────

claim_update_critical = claim(
    "The gated structural update is the single most critical component of MEMFLY: "
    "removing it (w/o Update) causes a 10.65 F1-point drop, larger than any single "
    "operation removal. This validates the IB-grounded consolidation as the core "
    "mechanism rather than any auxiliary refinement.",
    title="Gated update is the most critical component",
)

claim_link_more_important_than_merge = claim(
    "Among individual structural operations, removing Link causes a larger F1 drop "
    "(38.62 -> 33.57, -5.05) than removing Merge (38.62 -> 34.79, -3.83). This "
    "indicates that preserving conditional dependencies via E_RELATED edges is more "
    "valuable for downstream task accuracy than reducing redundancy via merges.",
    title="Link contributes more than Merge to downstream F1",
)

claim_keyword_critical_for_singlehop = claim(
    "Keyword-based micro-symbolic anchoring is critical for Single-Hop queries: "
    "removing it produces the largest retrieval-phase drop (F1 = 32.69, the lowest "
    "of all retrieval ablations) with the impact concentrated on Single-Hop "
    "categories where precise entity matching is required [@Kuffo2026, Figure 2(b)].",
    title="Keyword anchoring critical for Single-Hop",
)

claim_ier_critical_for_multihop = claim(
    "IER is critical for queries requiring progressive evidence accumulation: "
    "disabling it yields the second-largest retrieval-phase drop (F1 = 32.94) with "
    "Adversarial and Open Domain showing the largest declines.",
    title="IER critical for progressive multi-hop reasoning",
)

# ── Claims: end-to-end scientific conclusion ─────────────────────────────────

claim_memfly_outperforms = claim(
    "MEMFLY substantially outperforms state-of-the-art baselines in memory "
    "coherence, response fidelity, and answer accuracy on LoCoMo across both "
    "closed-source (GPT-4o-mini/4o) and open-source (Qwen3-8B/14B) backbones, "
    "consistent with the IB-grounded design rationale [@Kuffo2026].",
    title="MEMFLY outperforms state-of-the-art baselines",
)

claim_ib_design_validated = claim(
    "Empirical results validate that grounding agentic memory in the Information "
    "Bottleneck principle — combined with a Note-Keyword-Topic hierarchy and tri-"
    "pathway retrieval — resolves the compression-fidelity dilemma in practice. "
    "The consistent improvements across heterogeneous backbones indicate the "
    "approach is not specific to a single backbone family.",
    title="IB-grounded design validated empirically",
)

claim_proxy_signals_validated = claim(
    "Ablation results empirically validate that optimizing structural surrogates "
    "for the unobservable relevance variable Y (Keyword co-occurrence and Topic "
    "hierarchy) significantly improves downstream response fidelity and accuracy. "
    "Removing any structural component causes meaningful F1 drops, supporting the "
    "claim that these surrogates carry task-relevant information [@Kuffo2026, "
    "Sec. 4.3].",
    title="Structural proxy signals validated by ablation",
)

# ── Strategies ────────────────────────────────────────────────────────────────

# Each backbone provides one supporting empirical observation; the four together
# form the basis for "consistent across backbones". Induction supports must be in
# the generative direction (law -> observation).

s_law_predicts_gpt4omini = support(
    [claim_consistent_across_backbones], claim_avg_gpt4omini,
    reason="If MEMFLY leads consistently across backbones, GPT-4o-mini should show MEMFLY winning average F1 — observed at 43.76%.",
    prior=0.90,
)

s_law_predicts_gpt4o = support(
    [claim_consistent_across_backbones], claim_avg_gpt4o,
    reason="If MEMFLY leads consistently across backbones, GPT-4o should show MEMFLY winning average F1 — observed at 44.39%.",
    prior=0.90,
)

s_law_predicts_qwen8b = support(
    [claim_consistent_across_backbones], claim_avg_qwen8b,
    reason="If MEMFLY leads consistently across backbones, Qwen3-8B should show MEMFLY winning average F1 — observed at 38.62%.",
    prior=0.90,
)

s_law_predicts_qwen14b = support(
    [claim_consistent_across_backbones], claim_avg_qwen14b,
    reason="If MEMFLY leads consistently across backbones, Qwen3-14B should show MEMFLY winning average F1 — observed at 33.65%.",
    prior=0.85,
)

ind_backbones_a = induction(
    s_law_predicts_gpt4omini, s_law_predicts_gpt4o, law=claim_consistent_across_backbones,
    reason="GPT-4o-mini and GPT-4o jointly confirm the consistent-across-backbones law within the closed-source family.",
)

ind_backbones_b = induction(
    ind_backbones_a, s_law_predicts_qwen8b, law=claim_consistent_across_backbones,
    reason="Adding Qwen3-8B extends the law to the open-source family with a different parameter scale.",
)

ind_backbones_c = induction(
    ind_backbones_b, s_law_predicts_qwen14b, law=claim_consistent_across_backbones,
    reason="Adding Qwen3-14B further extends the law to a larger open-source backbone, completing four heterogeneous backbones.",
)

strat_open_source_advantage = support(
    [claim_avg_gpt4omini, claim_avg_qwen8b],
    claim_open_source_advantage_larger,
    reason=(
        "Comparing MEMFLY's margin over the strongest baseline across closed-source "
        "(@claim_avg_gpt4omini: +1.79 over A-MEM) and open-source backbones "
        "(@claim_avg_qwen8b: +5.86 over A-MEM) shows the larger gain on open-source, "
        "directly supporting the open-source advantage claim."
    ),
    prior=0.85,
)

strat_open_domain_gain = support(
    [claim_avg_gpt4o, claim_macro_semantic_path],
    claim_open_domain_gain,
    reason=(
        "The Open Domain F1 gap of 25.74 vs 17.73 reported in (@claim_avg_gpt4o) is "
        "explained mechanistically by Topic-based macro-semantic navigation "
        "(@claim_macro_semantic_path), which localizes relevant memory regions "
        "before fine-grained retrieval — directly the operation Open Domain queries "
        "benefit from."
    ),
    prior=0.85,
)

strat_single_hop = support(
    [claim_avg_qwen8b, claim_avg_qwen14b, claim_micro_symbolic_path],
    claim_single_hop_qwen,
    reason=(
        "Single Hop F1 leadership on both Qwen models (@claim_avg_qwen8b: 42.09 and "
        "@claim_avg_qwen14b: 42.25) is consistent with Keyword-based micro-symbolic "
        "anchoring (@claim_micro_symbolic_path) being the precise entity-matching "
        "mechanism Single Hop queries depend on."
    ),
    prior=0.85,
)

# Ablation derived claims

strat_update_critical = support(
    [claim_ablation_full, claim_ablation_no_update],
    claim_update_critical,
    reason=(
        "The 10.65 F1-point drop from removing the gated update "
        "(@claim_ablation_no_update vs @claim_ablation_full) exceeds the drop from "
        "removing any single operation, establishing the gated update as MEMFLY's "
        "single most critical component."
    ),
    prior=0.93,
)

strat_link_vs_merge = support(
    [claim_ablation_no_link, claim_ablation_no_merge, claim_ablation_full],
    claim_link_more_important_than_merge,
    reason=(
        "Comparing per-operation drops: w/o Link (@claim_ablation_no_link) yields "
        "33.57 F1, w/o Merge (@claim_ablation_no_merge) yields 34.79 F1. Both vs. "
        "Full at 38.62 (@claim_ablation_full): Link removal costs 5.05 F1 while "
        "Merge removal costs 3.83 F1. Conditional structure is therefore more "
        "important for downstream accuracy than redundancy reduction."
    ),
    prior=0.88,
)

strat_kw_singlehop = support(
    [claim_ablation_no_keyword],
    claim_keyword_critical_for_singlehop,
    reason=(
        "The w/o Keyword ablation (@claim_ablation_no_keyword) produces the lowest "
        "retrieval-phase F1 (32.69) with the impact concentrated on Single-Hop "
        "queries — directly supporting the criticality of Keyword anchoring for "
        "precise entity matching."
    ),
    prior=0.88,
)

strat_ier_multihop = support(
    [claim_ablation_no_ier, claim_ier_handles_multihop],
    claim_ier_critical_for_multihop,
    reason=(
        "The w/o IER ablation (@claim_ablation_no_ier) shows the largest declines "
        "on Adversarial and Open Domain — categories that involve multi-hop or "
        "progressive reasoning. Combined with the design intent for IER "
        "(@claim_ier_handles_multihop), this confirms its criticality for "
        "progressive evidence accumulation."
    ),
    prior=0.88,
)

# Final scientific conclusions

strat_memfly_outperforms = support(
    [claim_consistent_across_backbones],
    claim_memfly_outperforms,
    reason=(
        "MEMFLY achieving top average F1 on every evaluated backbone "
        "(@claim_consistent_across_backbones) is the empirical content of "
        "outperforming the state of the art across families."
    ),
    prior=0.90,
)

strat_denoise_supports_ingestion = support(
    [claim_ablation_no_denoise, claim_ablation_full],
    claim_ingestion_denoises,
    reason=(
        "The w/o Denoise ablation (@claim_ablation_no_denoise) drops F1 from "
        "@claim_ablation_full's 38.62 to 36.07, demonstrating that semantic "
        "denoising during ingestion produces measurable downstream gains. This is "
        "consistent with denoising improving the signal-to-noise ratio of stored "
        "Notes (i.e., increasing I(n_t; Y) over I(x_t; Y))."
    ),
    prior=0.78,
)

strat_proxy_signals_supports_proxies = support(
    [claim_ablation_no_keyword, claim_ablation_no_topic, claim_ablation_no_neighbor],
    claim_proxy_signals,
    reason=(
        "The structural ablations on Keyword (@claim_ablation_no_keyword), Topic "
        "(@claim_ablation_no_topic), and Neighbor (@claim_ablation_no_neighbor) "
        "each cause meaningful F1 drops. Since these structures embody the local-"
        "coherence and global-navigability proxies for the unobservable Y, their "
        "individual contributions empirically validate the proxy choice."
    ),
    prior=0.82,
)

strat_proxy_validated = support(
    [
        claim_ablation_no_keyword,
        claim_ablation_no_topic,
        claim_ablation_no_neighbor,
        claim_ablation_no_ier,
        claim_ablation_no_denoise,
        claim_proxy_signals,
    ],
    claim_proxy_signals_validated,
    reason=(
        "Each removal of a structural surrogate (Keyword "
        "(@claim_ablation_no_keyword), Topic (@claim_ablation_no_topic), Neighbor "
        "(@claim_ablation_no_neighbor), IER (@claim_ablation_no_ier)) causes a "
        "meaningful F1 drop. This demonstrates that each surrogate carries task-"
        "relevant information beyond what the remaining components provide."
    ),
    prior=0.88,
)

strat_ib_validated = support(
    [
        claim_memfly_outperforms,
        claim_proxy_signals_validated,
        claim_update_critical,
        claim_three_layer_hierarchy,
    ],
    claim_ib_design_validated,
    reason=(
        "MEMFLY's empirical superiority (@claim_memfly_outperforms), the validated "
        "contribution of its proxy signals (@claim_proxy_signals_validated), the "
        "criticality of the gated IB-grounded update (@claim_update_critical), and "
        "the structural realization of the IB compression-fidelity trade-off "
        "(@claim_three_layer_hierarchy) jointly support that the IB-grounded design "
        "resolves the compression-fidelity dilemma in practice."
    ),
    prior=0.85,
    background=[setup_locomo, setup_metrics],
)

# Connect end-to-end: this resolves the original dilemma

strat_resolves_dilemma = support(
    [claim_ib_design_validated],
    claim_compression_fidelity_dilemma,
    reason=(
        "The IB-grounded design's empirical validation (@claim_ib_design_validated) "
        "shows that the compression-fidelity dilemma admits a constructive "
        "resolution via principled structural priors and a gated update guided by "
        "an IB Lagrangian — confirming the dilemma was real (paper motivation) and "
        "actionable."
    ),
    prior=0.70,
)

# Comparison contradiction: MEMFLY vs. the best baseline at each backbone — each
# observation supports MEMFLY and contradicts the alternative that baselines are
# already optimal.

claim_baselines_optimal_alt = claim(
    "Alternative hypothesis: existing memory frameworks (LOCOMO, READAGENT, "
    "MEMORYBANK, MEMGPT, A-MEM, MEM-0) already achieve near-optimal long-term "
    "memory performance on LoCoMo, leaving little room for improvement.",
    title="Alternative: existing baselines are already near-optimal",
)

contradiction_alt = contradiction(
    claim_avg_gpt4omini,
    claim_baselines_optimal_alt,
    reason=(
        "If existing baselines were near-optimal (@claim_baselines_optimal_alt), "
        "MEMFLY could not improve over the best baseline by 1.79 F1 points on "
        "GPT-4o-mini (@claim_avg_gpt4omini). The two cannot both hold."
    ),
    prior=0.80,
)
