"""Section 8: Experiments"""

from gaia.lang import (
    claim, setting, question,
    support, deduction, abduction, induction,
    contradiction, compare,
)
from .motivation import (
    gap_no_comprehensive_comparison,
    gap_no_sota_analysis,
    q_which_method_best,
    q_new_sota,
    problem_stateless,
    memory_enables,
)
from .s3_framework import framework_proposed, ten_methods_classified
from .s4_extraction import extraction_completeness_tradeoff
from .s5_management import connecting_matters_multihop
from .s6_storage import hierarchical_advantage

# ── Experimental setup ────────────────────────────────────────────────────────

setting_benchmark_locomo = setting(
    "LOCOMO benchmark: 10 long-term conversations for question-answering evaluation. "
    "Each conversation has an average of 198.6 questions spanning 27.2 sessions and "
    "approximately 588.2 dialogue turns between two speakers. "
    "Question types: Single-Hop Retrieval, Multi-Hop Retrieval, Temporal Reasoning, Open-Domain Knowledge. "
    "Grounded in dialogues between two human users.",
    title="LOCOMO benchmark",
)

setting_benchmark_longmemeval = setting(
    "LONGMEMEVAL benchmark: 500 high-quality questions evaluating four core long-term memory abilities: "
    "Information Extraction (user/assistant/preference sub-tasks), Multi-Session Reasoning, "
    "Knowledge Updates, and Temporal Reasoning. "
    "Each question is grounded in a dedicated conversation history averaging 50.2 sessions and "
    "approximately 115,000 tokens in length. "
    "Based on user-AI interactions.",
    title="LONGMEMEVAL benchmark",
)

setting_eval_metrics = setting(
    "Evaluation metrics: F1 (token-level overlap balancing precision and recall) and "
    "BLEU-1 (unigram-level modified precision with brevity penalty, reflecting lexical fidelity). "
    "Both metrics are reported for each capability category on both datasets. "
    "A uniform simplification step is applied to all generated answers to reduce metric sensitivity to verbosity.",
    title="Evaluation metrics",
)

setting_impl_setup = setting(
    "Implementation: All 10 methods reimplemented in Python under the unified framework. "
    "Hardware: 8 NVIDIA A100 (80 GB) GPUs. "
    "If a method cannot finish in two days, its result is marked as '—'. "
    "Default LLM backbone: Qwen2.5-7B-Instruct. "
    "Context length: 20,000 tokens maximum. Decoding: greedy. "
    "Top-k retrieval: k=10 for all methods. "
    "Embedding model: all-MiniLM-L6-v2.",
    title="Implementation setup",
)

# ── Exp 1: Overall performance ────────────────────────────────────────────────

# LONGMEMEVAL results (7B backbone)
result_longmemeval_7b = claim(
    "Overall performance on LONGMEMEVAL with Qwen2.5-7B-Instruct backbone (F1 / BLEU-1):\n\n"
    "| Method | Info-Ext-user | Info-Ext-asst | Info-Ext-pref | Multi-Session | Knowledge-Upd | Temporal | Overall |\n"
    "|--------|--------------|--------------|--------------|---------------|---------------|----------|--------|\n"
    "| A-MEM | 46.75/41.26 | 43.21/36.74 | 9.76/0.52 | 16.61/14.32 | 19.37/15.54 | 25.59/21.63 | 25.53/21.24 |\n"
    "| MemoryBank | 46.28/42.19 | 49.31/43.08 | 13.96/3.79 | 19.41/16.42 | 17.80/13.15 | 31.51/27.31 | 27.65/23.03 |\n"
    "| MemGPT | 52.82/47.54 | 52.26/44.56 | 13.61/2.90 | 18.61/16.71 | 21.65/14.81 | 28.09/24.85 | 29.16/24.08 |\n"
    "| Mem0 | 56.51/51.23 | 32.35/25.99 | 11.44/0.69 | 23.02/20.72 | 28.86/21.19 | 41.28/36.37 | 32.46/26.95 |\n"
    "| Mem0g | 53.21/47.39 | 18.18/13.82 | 10.23/0.79 | 24.42/22.04 | 29.16/21.60 | 40.43/35.51 | 30.66/25.38 |\n"
    "| MemoChat | 6.44/3.24 | 16.95/12.74 | 7.18/0.12 | 12.27/10.09 | 17.49/11.35 | 6.51/4.28 | 12.16/8.26 |\n"
    "| Zep | — | — | — | — | — | — | — |\n"
    "| MemTree | 68.48/61.85 | 57.79/46.73 | 9.50/1.00 | 21.96/19.88 | 29.97/21.77 | 41.49/38.56 | 36.92/31.05 |\n"
    "| MemoryOS | 56.85/53.49 | 61.32/52.71 | 12.40/1.18 | 19.35/17.80 | 26.34/21.61 | 30.62/27.97 | 32.50/28.31 |\n"
    "| MemOS | 65.48/56.02 | 49.40/42.44 | 12.17/0.77 | 22.81/19.72 | 21.34/15.65 | 33.99/27.75 | 32.48/26.38 |\n\n"
    "Best overall: MemTree at 36.92 F1. Zep failed to complete (>2 days).",
    title="LONGMEMEVAL performance (7B)",
    background=[setting_benchmark_longmemeval, setting_eval_metrics, setting_impl_setup],
    metadata={"source_table": "artifacts/2604.01707.pdf, Table 3"},
)

# LOCOMO results
result_locomo_7b = claim(
    "Overall performance on LOCOMO with Qwen2.5-7B-Instruct backbone (F1 / BLEU-1):\n\n"
    "| Method | Single-Hop | Multi-Hop | Temporal | Open-Domain | Overall |\n"
    "|--------|-----------|----------|----------|-------------|--------|\n"
    "| A-MEM | 33.11/27.59 | 25.38/18.36 | 14.69/12.19 | 14.69/12.55 | 26.71/21.75 |\n"
    "| MemoryBank | 15.34/11.92 | 16.63/12.41 | 11.57/9.49 | 16.09/11.16 | 14.84/11.46 |\n"
    "| MemGPT | 21.31/16.57 | 18.92/13.64 | 17.37/13.61 | 11.14/8.06 | 19.42/15.51 |\n"
    "| Mem0 | 25.92/21.47 | 19.43/14.76 | 37.49/31.26 | 16.93/10.58 | 26.58/21.60 |\n"
    "| Mem0g | 27.90/23.45 | 21.14/13.98 | 35.70/30.54 | 18.67/13.44 | 27.71/22.57 |\n"
    "| MemoChat | 7.21/5.84 | 9.74/6.59 | 5.33/4.26 | 14.31/10.81 | 7.72/5.96 |\n"
    "| Zep | 40.42/34.59 | 30.97/20.31 | 22.64/17.82 | 21.79/17.57 | 33.82/27.42 |\n"
    "| MemTree | 33.36/27.91 | 26.40/17.59 | 25.62/21.45 | 20.67/16.23 | 29.68/23.95 |\n"
    "| MemoryOS | 33.14/28.33 | 28.52/19.90 | 17.65/14.09 | 22.05/16.95 | 28.34/23.11 |\n"
    "| MemOS | 39.55/33.58 | 34.04/23.38 | 37.55/31.90 | 22.55/16.51 | 37.05/30.30 |\n\n"
    "Best overall: MemOS at 37.05 F1.",
    title="LOCOMO performance (7B)",
    background=[setting_benchmark_locomo, setting_eval_metrics, setting_impl_setup],
    metadata={"source_table": "artifacts/2604.01707.pdf, Table 4"},
)

# ── Obs 1: Tree-based / hierarchical advantage ────────────────────────────────

obs_tree_hierarchical_strong = claim(
    "Tree-based memory methods (MemTree and MemOS) generally achieve strong performance by organizing "
    "memory in a multi-layered, multi-granularity fashion. Specifically, MemTree attains the highest "
    "F1 score of 36.92 on LONGMEMEVAL at the 7B scale, while MemOS achieves the highest F1 scores "
    "of 37.05 (7B) and 42.79 (72B) on LOCOMO. Tree structures provide high-level conceptual summaries "
    "at upper layers while preserving fine-grained details at leaf nodes. A similar advantage is "
    "realized through well-designed hierarchical architectures such as MemoryOS and Zep.",
    title="Obs1: Tree/hierarchical methods are strongest",
    background=[setting_benchmark_locomo, setting_benchmark_longmemeval],
)

strat_tree_hierarchical_result = support(
    [result_longmemeval_7b, result_locomo_7b, hierarchical_advantage],
    obs_tree_hierarchical_strong,
    reason=(
        "The experimental tables (@result_longmemeval_7b, @result_locomo_7b) show MemTree and MemOS "
        "consistently leading. The theoretical prediction that hierarchical organization is more "
        "effective (@hierarchical_advantage) is directly confirmed by these empirical rankings. "
        "MemTree's 36.92 F1 (best on LONGMEMEVAL 7B) and MemOS's 37.05/42.79 F1 (best on LOCOMO "
        "7B/72B) constitute independent evidence across two benchmarks."
    ),
    prior=0.90,
)

# ── Obs 2: Information completeness ──────────────────────────────────────────

obs_info_completeness_crucial = claim(
    "Preserving information completeness is crucial for effective memory persistence. "
    "Retaining raw messages during information extraction and incorporating original conversations "
    "during final response generation is essential. Methods that exclusively extract graph-based "
    "triples may suffer from information loss compared to those preserving raw dialogue fragments. "
    "Evidence: Mem0 (direct archive + summarization) outperforms Mem0g (graph-based extraction only) "
    "on LONGMEMEVAL overall F1 at both 7B scale (32.46 vs 30.66) and 72B scale (37.85 vs 38.47, "
    "with Mem0g slightly higher at 72B), and on several sub-tasks.",
    title="Obs2: Information completeness crucial",
    background=[setting_benchmark_longmemeval],
)

strat_completeness_from_results = support(
    [extraction_completeness_tradeoff, result_longmemeval_7b],
    obs_info_completeness_crucial,
    reason=(
        "The theoretical prediction that graph extraction loses information (@extraction_completeness_tradeoff) "
        "is empirically tested by comparing Mem0 (preserves raw) vs Mem0g (graph-only). "
        "The experimental tables (@result_longmemeval_7b) show Mem0 outperforming Mem0g in overall F1 "
        "at 7B (32.46 vs 30.66). This supports the claim that raw message retention helps."
    ),
    prior=0.78,
)

# ── Obs 3: Connecting for multi-hop ──────────────────────────────────────────

obs_connecting_multihop_validated = claim(
    "Experimental results validate that connecting-type memory management significantly improves "
    "multi-hop and multi-session reasoning performance. MemoryBank (no connecting) achieves "
    "only 19.41 F1 on Multi-Session LONGMEMEVAL; Mem0 (implicit connecting via concurrent updates) "
    "achieves 23.02 F1 — an 18.60% relative F1 improvement — and a 26.19% BLEU-1 improvement. "
    "Similarly, on LOCOMO Multi-Hop, methods with explicit connecting (Zep: 30.97, MemOS: 34.04) "
    "outperform methods without (MemoryBank: 16.63, MemGPT: 18.92).",
    title="Obs3: Connecting validated for multi-hop",
    background=[setting_benchmark_longmemeval, setting_benchmark_locomo],
)

strat_connecting_validated = support(
    [connecting_matters_multihop, result_longmemeval_7b, result_locomo_7b],
    obs_connecting_multihop_validated,
    reason=(
        "The theoretical expectation that connecting improves multi-hop reasoning "
        "(@connecting_matters_multihop) is confirmed experimentally. The tables "
        "(@result_longmemeval_7b, @result_locomo_7b) show consistent advantages of "
        "connected memory methods (Mem0, Zep, MemOS, MemTree) over disconnected ones "
        "(MemoryBank, MemGPT, MemoChat) on multi-hop and multi-session tasks."
    ),
    prior=0.88,
)

# ── Obs 4: Temporal tasks need reasoning capacity ─────────────────────────────

obs_temporal_backbone_dependent = claim(
    "Temporal reasoning tasks remain highly sensitive to the reasoning capacity of the backbone LLM. "
    "MemoryOS and MemoChat exhibit a performance leap exceeding 2× on LOCOMO temporal tasks as the "
    "backbone LLM scales from 7B to 72B: MemoryOS improves from 17.65 to 37.36 F1, "
    "MemoChat from 5.33 to 16.64 F1 — both more than doubling. "
    "To improve robustness, specialized architectural components for temporal information processing "
    "are needed rather than relying solely on LLM in-context reasoning.",
    title="Obs4: Temporal tasks backbone-sensitive",
    background=[setting_benchmark_locomo],
)

# ── Exp 2: Token cost ─────────────────────────────────────────────────────────

result_token_cost_tradeoff = claim(
    "Token cost vs performance tradeoff analysis on LOCOMO: Higher performance generally correlates "
    "with increased token consumption, but memory framework design is the primary determinant of "
    "cost efficiency. "
    "MemoryOS achieves strong performance with significantly lower token cost than MemTree or MemOS. "
    "MemoChat and MemoryBank minimize token usage but fail to deliver adequate accuracy. "
    "MemOS allocates more tokens to sophisticated agent-based decision-making than MemGPT, "
    "yielding superior performance despite both being OS-inspired.",
    title="Token cost vs performance tradeoff",
    background=[setting_benchmark_locomo, setting_impl_setup],
    metadata={"figure": "artifacts/2604.01707.pdf, Figure 6"},
)

result_granularity_token_cost = claim(
    "Information processing granularity significantly influences token cost during the extraction "
    "phase: processing individual dialogue turns (fine granularity) versus multiple turns collectively "
    "(coarse granularity). MemoryOS organizes dialogues into segments for mid-term storage; "
    "MemoryBank compiles messages at daily granularity. Due to strong LLM reasoning capabilities, "
    "coarser granularity does not necessarily compromise performance and may even improve it, "
    "offering a viable path toward enhancing memory efficiency.",
    title="Granularity affects token cost",
    background=[setting_impl_setup],
)

result_scalability_token_cost = claim(
    "As memory volume grows (across sessions on LOCOMO), certain methods show poor token cost "
    "scalability. MemTree's processing cost escalates as tree depth increases with dialogue history "
    "accumulation, since every top-down insertion requires updating all nodes along the path. "
    "Zep's graph complexity grows with dialogue turns, causing rising costs for deduplication "
    "and consistency maintenance.",
    title="Scalability issues for MemTree and Zep",
    background=[setting_benchmark_locomo],
    metadata={"figure": "artifacts/2604.01707.pdf, Figure 7"},
)

# ── Exp 3: Context scalability ────────────────────────────────────────────────

result_context_scalability = claim(
    "Context scalability analysis (LONGMEMEVAL context expanded from 50% to 200%): "
    "Nearly all memory architectures exhibit a steady decline in F1 scores as context scale expands. "
    "This performance attrition is driven by increased irrelevant information density, "
    "lowering the signal-to-noise ratio during retrieval. "
    "MemOS and MemGPT (LLM-as-OS paradigm) suffer disproportionately at 200% scale due to "
    "higher tool-call failure rates and indexing conflicts as the candidate space expands. "
    "MemoryOS (rule-based hierarchical management) maintains higher stability by offloading "
    "organizational logic from the LLM to a deterministic framework.",
    title="Context scalability: most methods degrade",
    background=[setting_benchmark_longmemeval],
    metadata={"figure": "artifacts/2604.01707.pdf, Figures 8a, 9"},
)

result_knowledge_update_scalability = claim(
    "Among task categories, Knowledge Update (KU) tasks are particularly sensitive to context scaling: "
    "increased memory volume raises the density of conflicting records, and since KU requires "
    "identifying the latest fact among mutually exclusive versions, more obsolete candidates "
    "directly increase retrieval interference. "
    "In contrast, temporal tasks remain relatively stable as context scales because they rely on "
    "the relative ordering of events, which remains structurally distinct even as background volume grows.",
    title="Knowledge Update most sensitive to scaling",
    background=[setting_benchmark_longmemeval],
)

rule_based_stable_scaling = claim(
    "Rule-based hierarchical memory management (as in MemoryOS) is more robust to context scaling "
    "than agent-based management (MemOS, MemGPT). MemoryOS offloads organizational logic from "
    "the LLM to a deterministic framework, reducing cognitive load on the LLM and maintaining "
    "high stability as context grows. The LLM-as-OS paradigm increases failure rates at scale "
    "because the expanded candidate space raises the difficulty for the LLM to accurately reason "
    "over and execute complex management instructions.",
    title="Rule-based management more robust at scale",
    background=[setting_benchmark_longmemeval],
)

strat_rule_based_scaling = support(
    [result_context_scalability, result_knowledge_update_scalability],
    rule_based_stable_scaling,
    reason=(
        "Context scalability experiments (@result_context_scalability) show MemoryOS maintaining "
        "stability while MemOS/MemGPT degrade more steeply at 200% context. The mechanism "
        "(@result_knowledge_update_scalability) — increased density of conflicting records — "
        "explains why the deterministic rule-based approach outperforms LLM-based management "
        "when the candidate space becomes large."
    ),
    prior=0.85,
)

# ── Exp 4: Position sensitivity ───────────────────────────────────────────────

result_recency_bias = claim(
    "A clear recency bias is observed: most memory methods achieve higher F1 scores when ground-truth "
    "evidence is placed in late sessions rather than early sessions. "
    "Specific improvements (Late vs Early placement, overall F1): "
    "MemTree: 37.37 vs 34.13 F1 (+3.24); MemOS: 34.40 vs 29.10 F1 (+5.30). "
    "As more intervening dialogue accumulates after relevant evidence appears, maintaining "
    "long-range information consistency and retrieval becomes increasingly challenging.",
    title="Recency bias in position sensitivity",
    background=[setting_benchmark_longmemeval],
    metadata={"figure": "artifacts/2604.01707.pdf, Figure 8b"},
)

result_position_category_dependent = claim(
    "Position sensitivity is highly category-dependent. "
    "Transient, session-localized information shows stronger position sensitivity than persistent traits. "
    "Information Extraction sub-tasks (user, assistant) show substantial Early-to-Late F1 gains: "
    "Mem0g: +9.53, MemTree: +10.74, MemOS: +9.23 F1 on user extraction; "
    "MemTree: +8.92, MemOS: +8.30 F1 on assistant extraction. "
    "In contrast, preference extraction (a persistent trait) shows only +1.08, +0.41, +0.66 F1 "
    "respectively for the same three methods. "
    "This indicates position sensitivity correlates with information persistence: "
    "transient session-local details suffer more from later interference.",
    title="Position sensitivity category-dependent",
    background=[setting_benchmark_longmemeval],
    metadata={"source_table": "artifacts/2604.01707.pdf, Table 5"},
)

memoryos_small_recency_gap = claim(
    "MemoryOS exhibits a smaller Late-Early gap (+1.29 F1) compared to MemTree and MemOS, "
    "because its stage-wise hierarchical transfers preserve historical information more evenly: "
    "earlier evidence remains relatively independent within each memory level rather than being "
    "repeatedly merged with later information. Later interactions do not directly reshape earlier "
    "evidence representations in MemoryOS, unlike tree-based methods where updates to higher-level "
    "summaries amplify recent information's influence.",
    title="MemoryOS smaller recency bias",
    background=[setting_benchmark_longmemeval],
)

# ── Exp 5: LLM backbone ───────────────────────────────────────────────────────

result_backbone_comparison = claim(
    "LLM backbone comparison on LOCOMO (F1 / BLEU-1):\n\n"
    "| Model | Metric | Zep | MemTree | MemoryOS | MemOS | Ours |\n"
    "|-------|--------|-----|---------|----------|-------|------|\n"
    "| Qwen2.5-7B | F1 | 33.82 | 29.68 | 28.34 | 37.05 | 38.03 |\n"
    "| Qwen2.5-7B | BLEU-1 | 27.42 | 23.95 | 23.11 | 30.30 | 31.73 |\n"
    "| Qwen2.5-72B | F1 | 37.45 | 34.85 | 39.63 | 42.79 | 43.87 |\n"
    "| Qwen2.5-72B | BLEU-1 | 30.46 | 28.49 | 32.62 | 35.16 | 37.30 |\n"
    "| LLaMA3.1-8B | F1 | — | 23.49 | 32.21 | 33.39 | 35.21 |\n"
    "| LLaMA3.1-8B | BLEU-1 | — | 18.19 | 25.56 | 26.24 | 28.40 |\n"
    "| GPT-4o-mini | F1 | 42.88 | 32.32 | 42.57 | 45.56 | 45.20 |\n"
    "| GPT-4o-mini | BLEU-1 | 36.09 | 25.89 | 34.75 | 38.06 | 38.52 |\n\n"
    "Zep failed on LLaMA3.1-8B due to strict JSON formatting failures. "
    "Most methods achieve best performance with GPT-4o-mini. "
    "Scaling Qwen2.5 from 7B to 72B produces substantial gains for all methods.",
    title="LLM backbone comparison",
    background=[setting_benchmark_locomo, setting_impl_setup],
    metadata={"source_table": "artifacts/2604.01707.pdf, Table 6"},
)

backbone_scaling_benefit = claim(
    "Scaling the Qwen2.5 backbone from 7B to 72B produces substantial performance gains for all "
    "agent memory methods on LOCOMO, indicating existing memory architectures remain heavily "
    "dependent on the backbone's reasoning capability. "
    "This suggests memory architecture design alone cannot fully compensate for backbone limitations.",
    title="Backbone scaling benefits all methods",
    background=[setting_benchmark_locomo],
)

strat_backbone_scaling = support(
    [result_backbone_comparison],
    backbone_scaling_benefit,
    reason=(
        "The backbone comparison table (@result_backbone_comparison) shows consistent F1 improvements "
        "when moving from Qwen2.5-7B to Qwen2.5-72B across all five methods evaluated: "
        "Zep +3.63, MemTree +5.17, MemoryOS +11.29, MemOS +5.74, Ours +5.84 F1. "
        "The uniform improvement direction across different memory architectures suggests "
        "backbone reasoning capability is a shared bottleneck."
    ),
    prior=0.90,
)

# ── Exp 6: New SOTA method ────────────────────────────────────────────────────

new_method_design = claim(
    "The paper proposes a new memory framework combining: "
    "(1) Tree-based organization from MemTree and MemOS for hierarchical summarization; "
    "(2) Three-tier hierarchical storage from MemoryOS (short-term, mid-term, long-term). "
    "New messages are added to short-term memory, then migrated to mid-term as Segment Summaries "
    "via a FIFO policy, then to long-term storage for persistent user knowledge.",
    title="New method design",
    background=[setting_impl_setup],
    metadata={"figure": "artifacts/2604.01707.pdf, Figure 11"},
)

result_new_method_longmemeval = claim(
    "The new method on LONGMEMEVAL with Qwen2.5-7B-Instruct (F1 Score):\n\n"
    "| Category | A-MEM | MemoryBank | MemGPT | Mem0 | Mem0g | MemTree | MemoryOS | MemOS | Ours |\n"
    "|----------|-------|------------|--------|------|-------|---------|----------|-------|------|\n"
    "| Info-Ext-user | 46.75 | 46.28 | 52.82 | 56.51 | 53.21 | 68.48 | 56.85 | 65.48 | 67.38 |\n"
    "| Info-Ext-asst | 43.21 | 49.31 | 52.26 | 32.35 | 18.18 | 57.79 | 61.32 | 49.40 | **69.34** |\n"
    "| Info-Ext-pref | 9.76 | 13.96 | 13.61 | 11.44 | 10.23 | 9.50 | 12.40 | 12.17 | 14.58 |\n"
    "| Multi-Session | 16.61 | 19.41 | 18.61 | 23.02 | 24.42 | 21.96 | 19.35 | 22.81 | 23.14 |\n"
    "| Knowledge-Upd | 19.37 | 17.80 | 21.65 | 28.86 | 29.16 | 29.97 | 26.34 | 21.34 | 29.22 |\n"
    "| Temporal | 25.59 | 31.51 | 28.09 | 41.28 | 40.43 | 41.49 | 30.62 | 33.99 | **43.53** |\n"
    "| **Overall** | 25.53 | 27.65 | 29.16 | 32.46 | 30.66 | 36.92 | 32.50 | 32.48 | **38.79** |\n\n"
    "New method achieves best overall F1 of 38.79, ranking first or second across all categories. "
    "Compared to best existing method (MemTree at 36.92 overall), improvement is +5.07% relative F1. "
    "On Info-Ext-assistant, improvement over best existing (MemoryOS 61.32) is +13.08% relative F1.",
    title="New method LONGMEMEVAL results",
    background=[setting_benchmark_longmemeval, setting_eval_metrics],
    metadata={"source_table": "artifacts/2604.01707.pdf, Table 7"},
)

result_new_method_locomo = claim(
    "The new method on LOCOMO (F1 Score):\n\n"
    "| Category | Size | A-MEM | MemoryBank | MemGPT | Mem0 | Mem0g | Zep | MemTree | MemoryOS | MemOS | Ours |\n"
    "|----------|------|-------|------------|--------|------|-------|-----|---------|----------|-------|------|\n"
    "| Single-Hop | 7B | 33.11 | 15.34 | 21.31 | 25.92 | 27.90 | 40.42 | 33.36 | 33.14 | 39.55 | **45.11** |\n"
    "| Single-Hop | 72B | 42.24 | 24.54 | 28.78 | 32.83 | 29.58 | 42.46 | 38.73 | 43.56 | 44.30 | **48.01** |\n"
    "| Multi-Hop | 7B | 25.38 | 16.63 | 18.92 | 19.43 | 21.14 | 30.97 | 26.40 | 28.52 | 34.04 | 30.01 |\n"
    "| Multi-Hop | 72B | 27.87 | 23.28 | 24.21 | 25.35 | 30.22 | 33.11 | 33.01 | 36.32 | 36.67 | **38.08** |\n"
    "| Temporal | 7B | 14.69 | 11.57 | 17.37 | 37.49 | 35.70 | 22.64 | 25.62 | 17.65 | 37.55 | 32.23 |\n"
    "| Temporal | 72B | 28.01 | 13.21 | 20.28 | 40.76 | 43.89 | 34.58 | 29.81 | 37.36 | **49.59** | 43.97 |\n"
    "| Open-Domain | 7B | 14.69 | 16.09 | 11.14 | 16.93 | 18.67 | 21.79 | 20.67 | 22.05 | 22.55 | 18.92 |\n"
    "| Open-Domain | 72B | 23.27 | 19.12 | 16.42 | 21.04 | 20.37 | 15.87 | 23.02 | 22.57 | 24.88 | 24.27 |\n"
    "| **Overall** | 7B | 26.71 | 14.84 | 19.42 | 26.58 | 27.71 | 33.82 | 29.68 | 28.34 | 37.05 | **38.03** |\n"
    "| **Overall** | 72B | 30.35 | 21.61 | 25.40 | 32.38 | 32.07 | 37.45 | 34.85 | 39.63 | 42.79 | **43.87** |\n\n"
    "New method achieves best overall on LOCOMO at both 7B (38.03) and 72B (43.87). "
    "Note: at 7B, the new method slightly underperforms MemOS on Multi-Hop (30.01 vs 34.04) "
    "and Open-Domain (18.92 vs 22.55), and on Temporal at 7B (32.23 vs 37.55 for MemOS).",
    title="New method LOCOMO results",
    background=[setting_benchmark_locomo, setting_eval_metrics],
    metadata={"source_table": "artifacts/2604.01707.pdf, Table 8"},
)

result_new_method_token_cost = claim(
    "The new method achieves state-of-the-art performance while maintaining a remarkably low "
    "computational overhead of fewer than 450 tokens per dialogue on average — substantially "
    "lower than MemOS or MemTree which incur substantial token overhead despite their strong "
    "accuracy. This represents an optimal balance between performance and token efficiency.",
    title="New method: low token cost",
    background=[setting_impl_setup],
    metadata={"figure": "artifacts/2604.01707.pdf, Figure 10"},
)

# ── New SOTA claim (exported) ─────────────────────────────────────────────────

new_method_sota = claim(
    "The newly designed memory method achieves state-of-the-art performance on both LOCOMO and "
    "LONGMEMEVAL benchmarks, surpassing all ten existing representative methods, while maintaining "
    "low computational overhead (<450 tokens/dialogue). "
    "On LONGMEMEVAL with Qwen2.5-7B-Instruct: overall F1 = 38.79 (best, +5.07% over MemTree at 36.92). "
    "On LOCOMO with Qwen2.5-7B-Instruct: overall F1 = 38.03 (best, +2.65% over MemOS at 37.05). "
    "On LOCOMO with Qwen2.5-72B-Instruct: overall F1 = 43.87 (best, +2.52% over MemOS at 42.79). "
    "The method demonstrates robust generalization across LLM backbones (Qwen2.5-7B/72B, LLaMA3.1-8B, GPT-4o-mini).",
    title="New method achieves SOTA",
    background=[setting_benchmark_locomo, setting_benchmark_longmemeval],
)

strat_new_method_sota = support(
    [result_new_method_longmemeval, result_new_method_locomo, result_new_method_token_cost, new_method_design],
    new_method_sota,
    reason=(
        "The new method's design (@new_method_design) combines tree-based hierarchical organization "
        "with three-tier storage. Experimental results on LONGMEMEVAL (@result_new_method_longmemeval) "
        "show overall F1 38.79, best among all methods. Results on LOCOMO (@result_new_method_locomo) "
        "show overall F1 38.03 (7B) and 43.87 (72B), both best. Token cost (@result_new_method_token_cost) "
        "is <450 tokens/dialogue — substantially less than competing high-performing methods. "
        "The combination of performance leadership across two benchmarks and two backbone scales, "
        "with low token overhead, establishes SOTA status."
    ),
    prior=0.92,
)
