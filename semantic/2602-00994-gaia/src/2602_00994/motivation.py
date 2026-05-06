"""Layer 2 semantic claims — aggregated from Layer 1 96 claims.

2602.00994: Reasoning and Tool-use Compete in Agentic RL
Li et al. 2026. LEAS (diagnostic) + DART (solution) for gradient conflict.
"""

from gaia.lang import claim, setting

# ── Aggregated semantic claims ──

seesaw_phenomenon = claim(
    "Under joint Agentic RL optimization, reasoning and tool-use capabilities "
    "exhibit a seesaw phenomenon: improving one consistently degrades the other. "
    "This is observed across Qwen2.5-7B, Qwen3-8B, Qwen3-7B, and Llama3.1-8B, "
    "and persists at multiple training checkpoints.",
    title="Seesaw phenomenon: reasoning-tool-use trade-off in ARL",
    aggregated_from=[
        "claim_seesaw_phenomenon",
        "claim_capabilities_are_heterogeneous",
        "claim_data_mixture_ineffective",
    ],
)

gradient_conflict_is_root_cause = claim(
    "The seesaw phenomenon is caused by gradient-level conflict between "
    "reasoning and tool-use capabilities, not by data imbalance. Evidence: "
    "(1) adjusting the data mixture ratio fails to resolve interference, "
    "(2) LEAS gradient analysis shows consistently negative interaction "
    "coefficients λ23 (mean ≈ -0.3 across checkpoints), (3) the interaction "
    "component dominates over capability-isolation components when they "
    "interfere.",
    title="Gradient conflict is the root cause of capability interference",
    aggregated_from=[
        "claim_data_mixture_ineffective",
        "obs_lambda23_distribution",
        "claim_interference_dominates",
        "obs_gradient_angles",
    ],
)

dart_solves_gradient_conflict = claim(
    "DART (Disentangled Agentic RL Tuning) resolves the gradient conflict "
    "by applying hard token-level routing through separate LoRA adapters "
    "with frozen backbone. It achieves: (1) +4.91 on Qwen3-8B MATH with "
    "tool-use intact, (2) consistent improvement across three backbones "
    "and two model sizes, (3) robustness to LoRA rank choice, (4) simpler "
    "infrastructure than 2-agent alternatives. The key mechanism is "
    "structural gradient isolation — DART guarantees zero interaction term "
    "between the two capabilities' gradients.",
    title="DART structurally eliminates gradient conflict between capabilities",
    aggregated_from=[
        "claim_dart_zero_interaction",
        "obs_dart_better_reasoning_3b",
        "obs_dart_better_reasoning_7b",
        "obs_rank_insensitive",
        "claim_dart_simpler_stack",
        "claim_dart_solves_gradient_conflict",
        "obs_dart_approaches_2agent",
        "claim_contribution_dart",
    ],
)

dart_vs_alternatives = claim(
    "DART outperforms or matches all tested alternatives: (1) standard "
    "GRPO (+6.35% avg EM across benchmarks), (2) task-specific LoRA "
    "(which cannot disentangle interference), (3) 2-agent systems (DART "
    "approaches their performance while using ~1/8 memory and simpler "
    "infrastructure). The 2-agent comparison is the closest — DART is "
    "within 1.2pp on most benchmarks.",
    title="DART vs alternatives: better or comparable with simpler infrastructure",
    aggregated_from=[
        "claim_dart_more_efficient_than_2agent",
        "claim_2agent_memory_8x",
        "claim_2agent_kv_recompute",
        "claim_multi_lora_cannot_disentangle",
        "obs_2agent_strongest",
        "obs_dart_approaches_2agent",
        "claim_contribution_empirical",
    ],
)

leas_diagnostic_framework = claim(
    "LEAS (Linear Effect Attribution System) provides a quantitative "
    "framework for measuring capability-level interference in ARL. It "
    "decomposes the model's output into reasoning-isolated, tool-use-"
    "isolated, and interaction components via logit-level linear "
    "attribution, enabling per-checkpoint tracking of how capabilities "
    "evolve and interfere during training.",
    title="LEAS quantitatively measures capability-level interference",
    aggregated_from=[
        "claim_contribution_leas",
        "claim_design_matrix_invertible",
        "claim_contrast_isolates_lambda23",
    ],
)

# ── Settings (context, not judged) ──

arl_training_setup = setting(
    "Agentic RL (ARL) trains LLMs to interleave reasoning with tool calls "
    "(search, code execution) under a single RL objective over shared "
    "parameters. Prior work (Toolformer, Search-R1, DeepSeekMath) applies "
    "one RL update per complete trajectory.",
    title="ARL training paradigm",
)

# ── Boundary conditions ──

no_llama_validation = claim(
    "No experimental validation on Llama-series models or models > 7B. "
    "All main experiments use Qwen-series 7-8B. This limits confidence "
    "in cross-architecture generalization.",
    title="Limitation: no Llama or >7B validation",
    aggregated_from=["table1_qwen3b", "table2_qwen7b"],
)

single_turn_scope = claim(
    "Experiments are limited to single-turn agent tasks. Multi-turn "
    "interactions may introduce additional interference patterns not "
    "captured by the current LEAS framework.",
    title="Limitation: single-turn scope",
)
