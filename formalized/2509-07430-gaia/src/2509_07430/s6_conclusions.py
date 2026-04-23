"""Section 6: Conclusions and Broader Implications"""

from gaia.lang import claim, support

from .motivation import (
    pass1_improves,
    passk_degrades,
    catastrophic_forgetting,
    rkl_accelerates_collapse,
    divergence_choice_neglected,
    mass_covering_preserves,
    f_divergence_setting,
    pass_at_k_setting,
    reverse_kl_setting,
    rlvr_setting,
)
from .s2_background import (
    grpo_no_diversity,
    rkl_mode_seeking_harm,
    forward_kl_mass_covering,
    js_mass_covering,
    grpo_objective,
    dapo_objective,
    trpo_bound,
)
from .s3_method import (
    partition_rationale,
    generator_efficiency,
    dphrl_handles_discrete,
    threshold_8_of_8_optimal,
    dphrl_objective,
    dataset_partition,
    preservation_loss,
    exploration_loss,
    generator_method,
)
from .s4_theory import (
    theorem1_statement,
    theorem1_interpretation,
    trpo_standard_vs_dphrl,
    grpo_no_bound,
    assumption1,
)
from .s5_experiments import (
    sql_bird_results,
    sql_spider_results,
    ood_math_results,
    math_llama_results,
    math_qwen_results,
    solution_style_diversity,
    capability_retention,
    sql_experiment_setup,
    math_experiment_setup,
)

# ── Claims: Synthesis ──────────────────────────────────────────────────────────

dphrl_resolves_paradox = claim(
    "DPH-RL (Diversity-Preserving Hybrid RL) resolves the RLVR diversity collapse paradox: "
    "it simultaneously improves Pass@1 (greedy accuracy) through exploration on "
    "$\\mathcal{D}_{exp}$ and maintains or improves Pass@k ($k > 1$) through f-divergence "
    "regularization on $\\mathcal{D}_{pef}$, avoiding the trade-off present in standard "
    "RLVR methods.",
    title="DPH-RL resolves diversity collapse paradox",
)

divergence_is_key_lever = claim(
    "The choice of divergence measure in RLVR is a powerful and previously neglected design "
    "dimension: switching from reverse-KL (or no divergence) to mass-covering f-divergences "
    "(forward-KL, JS) provides substantial gains in Pass@k and out-of-domain generalization "
    "without sacrificing Pass@1, demonstrating that divergence selection is as impactful "
    "as policy gradient algorithm choice.",
    title="Divergence choice is the key lever",
)

dphrl_generalizes = claim(
    "DPH-RL's improvements generalize across model families (Llama-3.1-8B-Instruct, "
    "Qwen2.5-Math-7B), task domains (SQL generation, mathematical reasoning), and "
    "evaluation metrics (Pass@1, Pass@8, Pass@16, Pass@64), suggesting the method is "
    "broadly applicable to RLVR settings with verifiable rewards.",
    title="DPH-RL generalizes across models and tasks",
)

# ── Pass 2: Connect — Strategies ──────────────────────────────────────────────

# Reverse KL accelerates diversity collapse (supported by theoretical mode-seeking + empirical)
# Note: rkl_accelerates_collapse is a claim that mode-seeking property CAUSES collapse;
# we support it from the theoretical mechanism and the OOD math empirical evidence.
strat_rkl_accelerates = support(
    [rkl_mode_seeking_harm, ood_math_results],
    rkl_accelerates_collapse,
    reason=(
        "The reverse-KL divergence's mode-seeking property (@rkl_mode_seeking_harm) "
        "theoretically predicts that policies trained with reverse-KL constraints will "
        "concentrate on single solution modes. This theoretical prediction is confirmed "
        "by the empirical RKL results (@ood_math_results): out-of-domain math scores "
        "drop to 48.45 (vs 60.35 base), worse than GRPO (52.37) and DAPO (52.63), "
        "establishing that reverse-KL actively accelerates diversity collapse."
    ),
    prior=0.85,
    background=[reverse_kl_setting],
)

# GRPO degrades Pass@k, supported by SQL bird/spider and math results
strat_grpo_passk = support(
    [sql_bird_results, sql_spider_results, math_llama_results],
    passk_degrades,
    reason=(
        "Three independent experimental observations confirm Pass@k degradation under GRPO: "
        "(1) BIRD SQL: GRPO Pass@8 = 66.2 vs base 68.8 (@sql_bird_results); "
        "(2) Spider SQL: GRPO Pass@8 = 79.5 vs base 90.9 (@sql_spider_results); "
        "(3) Math (Llama): GRPO Pass@64 = 33.3 vs base 40.0 (@math_llama_results). "
        "All three show degradation below the base model's diversity, confirming "
        "@passk_degrades across domains and model types.",
    ),
    prior=0.95,
    background=[pass_at_k_setting, sql_experiment_setup, math_experiment_setup],
)

# Catastrophic forgetting supported by OOD math results
strat_forgetting = support(
    [ood_math_results],
    catastrophic_forgetting,
    reason=(
        "The out-of-domain math evaluation on SQL-trained models (@ood_math_results) "
        "directly measures catastrophic forgetting: GRPO drops from 60.35 to 52.37 "
        "and DAPO from 60.35 to 52.63 on average across 6 math benchmarks, confirming "
        "@catastrophic_forgetting. RKL is worst at 48.45, demonstrating that all "
        "standard RLVR methods fail to prevent out-of-domain capability loss.",
    ),
    prior=0.95,
    background=[sql_experiment_setup],
)

# Mass-covering divergences preserve diversity (forward-KL theory + experiments)
strat_fkl_preserves = support(
    [forward_kl_mass_covering, sql_bird_results, sql_spider_results, ood_math_results],
    mass_covering_preserves,
    reason=(
        "The mass-covering property of forward-KL (@forward_kl_mass_covering) predicts "
        "that it prevents probability mass from collapsing. Empirically: DPH-F achieves "
        "Pass@8 = 70.1 on BIRD (vs 66.2 GRPO) (@sql_bird_results), Pass@8 = 84.5 on "
        "Spider (vs 79.5 GRPO) (@sql_spider_results), and OOD math = 60.98 (fully "
        "recovering base model) (@ood_math_results). These results jointly confirm that "
        "forward-KL regularization preserves diversity (@mass_covering_preserves).",
    ),
    prior=0.90,
    background=[f_divergence_setting, sql_experiment_setup],
)

strat_js_preserves = support(
    [js_mass_covering, sql_bird_results, math_llama_results, math_qwen_results],
    mass_covering_preserves,
    reason=(
        "The Jensen-Shannon divergence's mass-covering property (@js_mass_covering) "
        "similarly predicts diversity preservation. Empirically: DPH-JS achieves "
        "BIRD Pass@8 = 70.5 (best) (@sql_bird_results), Math Llama Pass@64 = 40.0 "
        "(recovering base) (@math_llama_results), and Qwen Pass@8 = 100.0 "
        "(@math_qwen_results). JS provides a softer, bounded constraint that may be "
        "more stable than forward-KL for some model-task combinations.",
    ),
    prior=0.90,
    background=[f_divergence_setting, math_experiment_setup],
)

# Theorem 1 derived from TRPO structure and DPH-RL design
# trpo_bound, preservation_loss, dataset_partition, assumption1 are settings;
# they go in background=
strat_theorem1 = support(
    [trpo_standard_vs_dphrl],
    theorem1_statement,
    reason=(
        "Theorem 1 is derived by extending the standard TRPO monotonic improvement bound. "
        "The standard bound (formalized in @trpo_standard_vs_dphrl) shows the gap "
        "between standard TRPO and DPH-RL: by incorporating the f-divergence "
        "preservation loss on $\\mathcal{D}_{pef}$ and invoking Assumption 1 (bounded "
        "advantage on the near-perfect set), an additional positive term $\\varepsilon_f$ "
        "appears, yielding a strictly better lower bound (@theorem1_statement).",
    ),
    prior=0.80,
    background=[dphrl_objective, preservation_loss, dataset_partition, assumption1, trpo_bound],
)

# DPH-RL resolves paradox, supported by experiments + theory
strat_resolves = support(
    [sql_bird_results, ood_math_results, math_qwen_results, theorem1_statement],
    dphrl_resolves_paradox,
    reason=(
        "DPH-RL's resolution of the diversity-accuracy trade-off is supported by both "
        "empirical results and theory. Empirically: DPH-JS achieves BIRD Pass@8 = 70.5 "
        "while OOD math = 60.23 (fully recovered) and Qwen Pass@8 = 100.0 "
        "(@sql_bird_results, @ood_math_results, @math_qwen_results)—simultaneously "
        "improving Pass@1 in-domain and maintaining Pass@k/OOD performance. "
        "Theoretically, Theorem 1 (@theorem1_statement) guarantees that the f-divergence "
        "regularization provides a positive bonus on well-mastered queries, formally "
        "justifying the dual improvement.",
    ),
    prior=0.88,
    background=[sql_experiment_setup, math_experiment_setup],
)

# Divergence is the key lever
strat_divergence_key = support(
    [dphrl_resolves_paradox, divergence_choice_neglected, mass_covering_preserves],
    divergence_is_key_lever,
    reason=(
        "The conclusion that divergence choice is a powerful and neglected lever "
        "follows from: (1) standard methods (GRPO, DAPO) omit divergence entirely and "
        "suffer collapse (@divergence_choice_neglected); (2) reverse-KL worsens the problem; "
        "(3) swapping to mass-covering f-divergences resolves it (@mass_covering_preserves); "
        "(4) DPH-RL achieves the best of both worlds (@dphrl_resolves_paradox). The single "
        "change of divergence type, with everything else equal, explains the improvement.",
    ),
    prior=0.85,
)

# Generalization across models and tasks
strat_generalizes = support(
    [sql_bird_results, sql_spider_results, math_llama_results, math_qwen_results, ood_math_results],
    dphrl_generalizes,
    reason=(
        "DPH-RL's generalization is demonstrated across: (1) SQL tasks on BIRD and Spider "
        "(@sql_bird_results, @sql_spider_results); (2) math tasks with Llama-3.1-8B-Instruct "
        "(@math_llama_results) and Qwen2.5-Math-7B (@math_qwen_results); (3) OOD cross-domain "
        "evaluation (@ood_math_results). The consistent pattern of improvement across these "
        "varied settings supports the claim of broad applicability.",
    ),
    prior=0.82,
    background=[sql_experiment_setup, math_experiment_setup],
)

# Generator efficiency — supported by method design
strat_generator_eff = support(
    [dphrl_handles_discrete],
    generator_efficiency,
    reason=(
        "Generator-based computation (@dphrl_handles_discrete) avoids online reference model "
        "calls during training. Pre-sampled trajectories from $\\pi_{ref}$ serve as "
        "the denominator in f-divergence computation, adding only a pre-sampling overhead "
        "(one pass through the reference model before training). During training steps, "
        "no reference model inference is needed, making DPH-RL computationally comparable "
        "to GRPO.",
    ),
    prior=0.88,
    background=[generator_method],
)

# Theorem 1 interpretation
strat_theorem1_interp = support(
    [theorem1_statement],
    theorem1_interpretation,
    reason=(
        "The interpretation of $\\varepsilon_f > 0$ as a 'bonus' follows directly from "
        "the theorem statement (@theorem1_statement): the f-divergence on $\\mathcal{D}_{pef}$ "
        "ensures the policy stays near the reference on near-perfect queries, and since "
        "the reference excels on these queries, this regularization guarantees positive "
        "advantage contributions, yielding the positive bonus term.",
    ),
    prior=0.82,
    background=[preservation_loss, dataset_partition],
)

# Note: A contradiction between rkl_accelerates_collapse and mass_covering_preserves
# would be semantically incorrect: both claims can be true simultaneously — RKL accelerates
# collapse for methods using reverse-KL, while mass-covering divergences preserve diversity
# for methods using forward-KL/JS. These apply to DIFFERENT divergence types and are
# compatible. Similarly, "GRPO lacks diversity" and "DPH-RL resolves paradox" both describe
# different systems and can be simultaneously true. No contradiction operators are modeled here.
# These tensions are flagged in ANALYSIS.md as unmodeled comparisons.

# Connect orphaned claims that have supporting evidence

# GRPO lacks a monotonic improvement guarantee — supported by GRPO design (no divergence)
strat_grpo_no_bound = support(
    [grpo_no_bound],
    grpo_no_diversity,
    reason=(
        "The absence of a monotonic improvement guarantee for GRPO (@grpo_no_bound) directly "
        "implies GRPO lacks diversity protection: without a divergence term, the policy can "
        "drift arbitrarily far from the reference, and there is no formal guarantee that "
        "existing capabilities (diverse solutions) are preserved (@grpo_no_diversity).",
    ),
    prior=0.85,
)

# Partition rationale supports the asymmetric DPH-RL design
strat_partition = support(
    [partition_rationale],
    dphrl_resolves_paradox,
    reason=(
        "The principled asymmetric partitioning (@partition_rationale)—applying f-divergence "
        "only on $\\mathcal{D}_{pef}$ while using unconstrained PPO on $\\mathcal{D}_{exp}$—is "
        "the design choice that enables DPH-RL to simultaneously improve exploration and "
        "preserve existing capabilities, directly contributing to its resolution of the "
        "diversity collapse paradox (@dphrl_resolves_paradox).",
    ),
    prior=0.82,
)

# Pass@1 improves supports that DPH-RL doesn't sacrifice greedy accuracy
strat_pass1 = support(
    [pass1_improves, dphrl_resolves_paradox],
    divergence_is_key_lever,
    reason=(
        "That standard RLVR consistently improves Pass@1 (@pass1_improves), combined with "
        "DPH-RL's additional preservation of Pass@k (@dphrl_resolves_paradox), demonstrates "
        "that the divergence choice can decouple these metrics: the correct divergence type "
        "enables simultaneous improvement in both, establishing divergence as a key lever "
        "(@divergence_is_key_lever).",
    ),
    prior=0.83,
)

# Solution style diversity supports mass-covering divergences preserve diversity
strat_style_diversity = support(
    [solution_style_diversity],
    mass_covering_preserves,
    reason=(
        "The qualitative solution style analysis (@solution_style_diversity) directly "
        "demonstrates mass-covering divergences preserve stylistic diversity: forward-KL "
        "and JS-trained models produce multiple distinct solution styles per query, "
        "whereas reverse-KL models converge to a single style. This provides concrete "
        "evidence that @mass_covering_preserves holds at the solution-format level.",
    ),
    prior=0.87,
)

# Capability retention analysis supports DPH-RL resolves paradox
strat_cap_retention = support(
    [capability_retention],
    dphrl_resolves_paradox,
    reason=(
        "The capability retention analysis (@capability_retention) shows DPH-JS retains "
        "85%+ of base model capabilities while GRPO/DAPO lose ~15%. This retention of "
        "existing knowledge alongside task-specific improvement is a core component of "
        "resolving the diversity-accuracy paradox (@dphrl_resolves_paradox).",
    ),
    prior=0.87,
)

# Threshold analysis supports the 8/8 choice as principled
strat_threshold = support(
    [threshold_8_of_8_optimal],
    partition_rationale,
    reason=(
        "The threshold ablation study (@threshold_8_of_8_optimal) validates the partition "
        "strategy: the strictest threshold (8/8 correct rollouts) selects only genuinely "
        "mastered queries, confirming the rationale that $\\mathcal{D}_{pef}$ should contain "
        "only queries where the base model is already reliable (@partition_rationale).",
    ),
    prior=0.83,
)

__all__ = [
    "dphrl_resolves_paradox",
    "divergence_is_key_lever",
    "dphrl_generalizes",
]
