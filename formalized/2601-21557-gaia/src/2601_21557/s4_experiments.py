"""Section 4: Experiments — Benchmarks, Baselines, and Main Results"""

from gaia.lang import claim, setting, support, abduction, induction, compare, complement

from .motivation import ce_brevity_bias, ce_bloat_bias, no_universal_harness
from .s3_mce_framework import (
    mce_decouples_what_how,
    agentic_crossover_claim,
    context_as_files,
    skill_unifies_levels,
)

# ── Settings ──────────────────────────────────────────────────────────────────

setup_benchmarks = setting(
    "MCE is evaluated on five benchmarks spanning diverse domains: "
    "(1) **FiNER** — financial named entity recognition (XBRL tag prediction, accuracy); "
    "(2) **USPTO-50k** — single-step retrosynthesis prediction (accuracy); "
    "(3) **Symptom2Disease** — medical symptom-to-diagnosis prediction (accuracy); "
    "(4) **LawBench** — Chinese legal criminal charge prediction (micro-F1); "
    "(5) **AEGIS2** — AI safety prompt classification safe/unsafe (F1). "
    "Train/val/test splits follow the ACE benchmark protocol.",
    title="Five evaluation benchmarks",
)

setup_baselines = setting(
    "Baselines compared: (1) Base Model (zero-shot); "
    "(2) In-Context Learning (ICL) — all training samples in context window; "
    "(3) MIPROv2 [@Opsahl2024] — DSPy-based prompt optimization; "
    "(4) GEPA [@Agrawal2025] — reflective prompt rewriting with brevity bias; "
    "(5) Dynamic Cheatsheet (DC) [@Suzgun2025] — additive-curation online; "
    "(6) ACE [@Zhang2026] — modular agentic curation. "
    "All baselines use DeepSeek V3.1 as generator; training budget is no less than MCE's.",
    title="Baselines and fair comparison setup",
)

setup_models = setting(
    "Default generator: DeepSeek V3.1 [@Liu2024]. "
    "AEGIS2 uses Qwen3-8B (safety guardrails require lightweight models). "
    "MCE agentic model: MiniMax M2.1 [@MiniMaxAI2025]. "
    "MCE base-agents may invoke DeepSeek V3.1 during execution. "
    "All models accessed via OpenRouter.",
    title="Model selection",
)

setup_mce_instantiation = setting(
    "MCE is instantiated using the Claude Agent SDK [@Anthropic2025a]. "
    "Context interface is defined as a one-shot retrieval function: query → context. "
    "MCE optimizes context for 5 epochs (iterations). "
    "Training data batching is optionally applied for large datasets.",
    title="MCE experimental instantiation",
)

# ── Main performance results ───────────────────────────────────────────────────

mce_offline_gains = claim(
    "In the offline setting, MCE achieves the highest average relative gain of 89.1% over the base model "
    "across all five benchmarks, compared to: ACE 70.7%, GEPA 61.5%, MIPROv2 48.6%, ICL 32.1%. "
    "Per-benchmark results: FiNER 75% (vs ACE 71%), USPTO-50k 20% (vs ACE 18%), "
    "Symptom2Disease 89.2% (vs ACE 79.2%), LawBench 0.70 F1 (vs ACE 0.65), "
    "AEGIS2 0.80 F1 (vs ACE 0.68).",
    title="MCE offline performance vs baselines",
    metadata={"source_table": "artifacts/2601.21557.pdf, Table 1"},
)

mce_online_gains = claim(
    "In the online setting (single-pass, no iterative evolution), MCE achieves 74.1% average relative gain, "
    "compared to ACE 41.1% and DC 35.8%. Per-benchmark: FiNER 68%, USPTO-50k 20%, "
    "Symptom2Disease 76.4%, LawBench 0.66 F1, AEGIS2 0.63 F1.",
    title="MCE online performance vs baselines",
    metadata={"source_table": "artifacts/2601.21557.pdf, Table 1"},
)

mce_top_rank = claim(
    "MCE achieves the best or second-best performance on all five benchmarks in both offline and "
    "online settings, demonstrating that MCE can discover task-appropriate strategies beyond any "
    "single heuristic (brevity vs. detail).",
    title="MCE top-ranked performance across all benchmarks",
)

strat_mce_top_rank = support(
    [mce_offline_gains, mce_online_gains],
    mce_top_rank,
    reason=(
        "Both offline (@mce_offline_gains) and online (@mce_online_gains) results show MCE achieving "
        "leading or near-leading performance across all five diverse benchmarks. "
        "The consistency across tasks with different CE biases (brevity on LawBench, detail on FiNER) "
        "supports that MCE is not exploiting a single favorable task characteristic."
    ),
    prior=0.90,
)

# ── Context adaptability ──────────────────────────────────────────────────────

mce_context_length_adaptability = claim(
    "MCE adapts context length flexibly to task requirements, overcoming the inductive biases of "
    "prior methods. The two most effective MCE contexts on FiNER have 1.5K and 20K tokens; "
    "on LawBench, the MCE context reaches 44K tokens; on USPTO-50k, it reaches 86K tokens. "
    "In contrast, GEPA typically produces 1–2K tokens (brevity bias) and ACE reaches up to "
    "80K tokens after 5 epochs regardless of task (bloat bias).",
    title="MCE context length adaptability",
    metadata={"figure": "artifacts/2601.21557.pdf, Figure 3 — Context efficiency on FiNER"},
)

strat_adaptability = support(
    [context_as_files, skill_unifies_levels, mce_decouples_what_how],
    mce_context_length_adaptability,
    reason=(
        "MCE's file-based context representation (@context_as_files) imposes no structural constraints on length. "
        "The skill (@skill_unifies_levels) directs the base-agent to determine task-appropriate context size. "
        "The bi-level decoupling (@mce_decouples_what_how) allows the optimization to discover task-optimal length "
        "rather than following a fixed brevity or accumulation heuristic."
    ),
    prior=0.87,
)

# ── Context efficiency ────────────────────────────────────────────────────────

mce_context_efficiency = claim(
    "MCE produces more efficient contexts than ACE at comparable sizes. "
    "At ~1.5K tokens, MCE-S achieves 73% accuracy on FiNER versus 65% for ACE (Step 20 of Epoch 1). "
    "MCE-L reaches 75% accuracy with only 20K tokens, outperforming ACE's 70% accuracy even "
    "after 5 epochs with 79K tokens.",
    title="MCE superior context efficiency vs ACE",
    metadata={"figure": "artifacts/2601.21557.pdf, Figure 3 — Context efficiency on FiNER"},
)

mce_efficiency_mechanism = claim(
    "MCE's superior context efficiency stems from two properties: "
    "(1) the base-agent maintains a global view of accumulated context, enabling restructuring "
    "and refinement of existing knowledge rather than blindly appending new items; "
    "(2) MCE agentically processes large batches of training rollouts, aggregating feedback "
    "across many examples before updating the context.",
    title="Mechanism of MCE context efficiency",
)

strat_efficiency_mechanism = support(
    [context_as_files, skill_unifies_levels],
    mce_efficiency_mechanism,
    reason=(
        "File-based context (@context_as_files) enables the agent to read, restructure, and "
        "rewrite the entire context as a whole (global view), unlike ACE's additive appending to lists. "
        "The skill (@skill_unifies_levels) directs the agent to analyze batches of rollouts holistically, "
        "producing coherent, non-redundant context."
    ),
    prior=0.82,
)

strat_context_efficiency = support(
    [mce_efficiency_mechanism],
    mce_context_efficiency,
    reason=(
        "The global restructuring and batch aggregation described in @mce_efficiency_mechanism "
        "yield coherent, non-redundant contexts. This explains why MCE-S (1.5K tokens, global view) "
        "outperforms ACE at 1.5K (additive append) and why MCE-L (20K) outperforms ACE at 79K."
    ),
    prior=0.85,
)

# ── Training efficiency ────────────────────────────────────────────────────────

mce_training_efficiency = claim(
    "MCE is rollout-efficient: on FiNER, MCE requires only 450 rollouts to reach 95% training accuracy, "
    "while ACE peaks at 94% after 2169 rollouts (4.8x fewer rollouts). "
    "MCE total training duration is 1.9 hours versus ACE's 25.8 hours (13.6x faster).",
    title="MCE 4.8x rollout efficiency and 13.6x training speed vs ACE",
    metadata={"figure": "artifacts/2601.21557.pdf, Figure 4 — Training efficiency on FiNER"},
)

strat_training_efficiency = support(
    [mce_efficiency_mechanism],
    mce_training_efficiency,
    reason=(
        "The same architectural properties that improve context quality (@mce_efficiency_mechanism — "
        "global context view and batch-level optimization) also accelerate convergence. "
        "By processing many rollouts in one pass and making holistic updates, MCE reaches high "
        "accuracy with far fewer individual rollouts."
    ),
    prior=0.83,
)

# ── Transferability ────────────────────────────────────────────────────────────

mce_transfer_superior = claim(
    "MCE contexts transfer better from strong-to-weak models than ACE contexts. "
    "Contexts trained with DeepSeek-V3.1 transferred to Llama3.3-70B, Qwen3-8B, and Gemma3-4B. "
    "Average relative performance drop: MCE 23.6–43.4% vs ACE 23.6–48.3%. "
    "For Qwen3-8B on FiNER, MCE achieves 71% vs ACE 63%; on Symptom2Disease, MCE 80.2% vs ACE 72.2%; "
    "on LawBench, MCE F1=0.45 vs ACE F1=0.32.",
    title="MCE superior strong-to-weak transferability",
    metadata={"source_table": "artifacts/2601.21557.pdf, Table 2"},
)

mce_transfer_mechanism = claim(
    "MCE's superior transferability is attributed to the structured, generalizable nature of "
    "its learned contexts: by restructuring and synthesizing generalizable principles rather than "
    "accumulating task-specific traces, the context remains interpretable and useful for smaller models.",
    title="Mechanism of MCE transferability",
)

strat_transfer_mechanism = support(
    [mce_efficiency_mechanism],
    mce_transfer_mechanism,
    reason=(
        "The same global restructuring and batch synthesis (@mce_efficiency_mechanism) that produce "
        "efficient contexts also produce more generalizable contexts with explicit principles rather "
        "than idiosyncratic patterns tailored to a strong model's capabilities."
    ),
    prior=0.78,
)

strat_transfer_superior = support(
    [mce_transfer_mechanism],
    mce_transfer_superior,
    reason=(
        "Because MCE's contexts encode generalizable principles (@mce_transfer_mechanism) rather than "
        "model-specific reasoning chains, they retain more utility when transferred to smaller models "
        "with different inference capabilities."
    ),
    prior=0.80,
)

# ── Abduction: MCE performance vs ACE ────────────────────────────────────────

# Prediction from MCE design
mce_predicts_improvement = claim(
    "The MCE bi-level framework predicts that by co-evolving skills and context artifacts, "
    "it will consistently outperform fixed-harness CE methods (ACE, GEPA, DC) across diverse task domains.",
    title="MCE prediction: consistent improvement over fixed-harness CE",
)

# Alternative prediction from fixed-harness design (ACE)
alt_fixed_harness = claim(
    "Fixed-harness CE methods (ACE, GEPA) predict that iterative on-policy rollout-reflection-curation "
    "with a well-designed static harness is sufficient to achieve competitive or superior performance "
    "compared to a meta-level skill evolution approach.",
    title="Alternative prediction: fixed harness sufficient",
)

# Observation: empirical results
obs_performance_results = claim(
    "Empirical evaluation on five benchmarks shows MCE achieves 89.1% average relative gain (offline), "
    "outperforming ACE (70.7%), GEPA (61.5%), and all other baselines with consistent top-rank across "
    "all five diverse domains.",
    title="Observation: MCE outperforms all CE baselines",
)

s_h_mce = support(
    [mce_predicts_improvement],
    obs_performance_results,
    reason=(
        "MCE's bi-level design predicts consistent cross-domain improvement by adapting the "
        "optimization procedure itself. @mce_predicts_improvement forecasts exactly the "
        "multi-domain leadership observed."
    ),
    prior=0.88,
)

s_alt_fixed = support(
    [alt_fixed_harness],
    obs_performance_results,
    reason=(
        "A fixed harness (ACE) can partially explain the results — ACE achieves 70.7% avg gain — "
        "but cannot explain why MCE consistently outperforms it on tasks requiring both detailed "
        "and concise context (e.g., 89.2% vs 79.2% on Symptom2Disease and 75% vs 71% on FiNER)."
    ),
    prior=0.45,
)

pred_mce_better = claim(
    "MCE's bi-level skill evolution predicts 5.6–53.8% relative improvement over state-of-the-art CE methods.",
    title="MCE predicted improvement range",
)

pred_ace_competitive = claim(
    "ACE-style fixed harness predicts performance within 5% of the best flexible meta-learning approach.",
    title="ACE predicted competitive performance",
)

comp_mce_vs_ace = compare(
    pred_mce_better,
    pred_ace_competitive,
    obs_performance_results,
    reason=(
        "MCE's actual improvement over ACE ranges from 6% (FiNER offline: 75 vs 71%) to 15% "
        "(Symptom2Disease offline: 89.2 vs 79.2%), far exceeding the within-5% prediction of "
        "fixed-harness sufficiency."
    ),
    prior=0.87,
)

abd_mce_performance = abduction(
    s_h_mce,
    s_alt_fixed,
    comp_mce_vs_ace,
    reason="Both MCE and fixed-harness approaches attempt to explain observed cross-domain performance.",
)
