"""
ARC: Active and Reflection-driven Context Management for Long-Horizon Information Seeking Agents
==================================================================================================

Yao, Huang, Dai, Tan, Duan, Jia, Jiang, Yang (2026). arXiv:2601.12030

This package formalizes the knowledge structure of a paper proposing ARC, a framework for
managing context in long-horizon information-seeking LLM agents. ARC treats interaction
memory as a dynamically managed internal state via:
1. Always-on incremental summarization that preserves recent-turn semantics.
2. Selectively triggered reflection that jointly revises memory and a control checklist.
Implemented by a dedicated, learnable Context Manager (CM) decoupled from the Actor.

Key empirical findings:
1. ARC outperforms ReAct (raw history) and ReSum (passive summarization) on five long-horizon
   information-seeking benchmarks across five actor models, with up to ~11% absolute Pass@1
   gain on BrowseComp-ZH (Qwen2.5-32B).
2. Gains amplify with task difficulty (smaller on HotpotQA, larger on BrowseComp/GAIA).
3. Ablations show joint memory+checklist revision is required; reflection without memory
   revision is harmful (worse than the Summary baseline).
4. A trained 14B ARC-CM outperforms an untrained 120B GPT-OSS CM, supporting that context
   management is a learnable capability rather than emergent from scale.
5. Per-turn (always-on) management strictly beats delayed and budget-triggered alternatives.
"""

from .motivation import (
    deep_search_setting,
    context_rot,
    raw_history_limitation,
    passive_summarization_limitation,
    passive_strategies_share_limitation,
    active_management_view,
    q_active_management,
    q_learnable_cm,
    q_management_frequency,
    contribution_perspective,
    contribution_arc_framework,
    contribution_dual_architecture,
)

from .s3_methodology import (
    dual_architecture,
    actor_policy,
    incremental_summarization,
    raw_recent_turn_retained,
    reflection_operator,
    reflection_trigger,
    cm_training_setup,
    incremental_preserves_evidence,
    reflection_enables_repair,
    decoupling_enables_reuse,
)

from .s4_main_results import (
    benchmark_setup,
    baselines_setup,
    actor_models_setup,
    table1_observation,
    arc_outperforms_react,
    arc_outperforms_resum,
    react_better_than_arc,
    resum_better_than_arc,
    gain_amplifies_with_difficulty,
    arc_lifts_both_small_and_large_actors,
    context_degradation_is_dominant_failure,
)

from .s4_ablations import (
    ablation_setup,
    table2_observation,
    incremental_helps_baseline,
    checklist_alone_marginal,
    reflection_without_memory_harmful,
    joint_revision_required,
    checklist_alone_strong,
    cm_choice_setup,
    table3_observation,
    cm_choice_matters,
    cm_is_learnable,
    cm_emergent_only,
    cm_lifts_actor_ceiling,
    frequency_setup,
    table4_observation,
    per_turn_best,
    delayed_loses_evidence,
    budget_triggered_too_late,
    context_mgmt_is_semantic_alignment,
    budget_triggered_best,
)

from .limitations import (
    limitation_overhead,
    limitation_scope,
    limitation_training_data,
    conclusion_main,
)

__all__ = [
    # Core perspective and contributions
    "active_management_view",
    "contribution_perspective",
    "contribution_arc_framework",
    "contribution_dual_architecture",
    # Methodology (key derived claims)
    "incremental_preserves_evidence",
    "reflection_enables_repair",
    "decoupling_enables_reuse",
    # Main results
    "arc_outperforms_react",
    "arc_outperforms_resum",
    "gain_amplifies_with_difficulty",
    "arc_lifts_both_small_and_large_actors",
    "context_degradation_is_dominant_failure",
    # Ablations and analyses
    "incremental_helps_baseline",
    "checklist_alone_marginal",
    "reflection_without_memory_harmful",
    "joint_revision_required",
    "cm_choice_matters",
    "cm_is_learnable",
    "cm_lifts_actor_ceiling",
    "per_turn_best",
    "context_mgmt_is_semantic_alignment",
    # Limitations and conclusion
    "limitation_overhead",
    "limitation_scope",
    "limitation_training_data",
    "conclusion_main",
]
