"""Prior assignments for independent (leaf) claims in the SGS knowledge package."""

from . import (
    alt_sgs_no_gain,
    cispo_entropy_collapse,
    cispo_solver_kills_conjecturer,
    frozen_conjecturer_suboptimal,
    future_non_verifiable,
    guide_hypothesis,
    guide_sft_prevents_format_errors,
    limitation_frozen_guide,
    limitation_model_size,
    limitation_verifiable_domain,
    no_guide_lower_performance,
    no_problem_cond_fails,
    pred_alt_sgs,
    pred_sgs,
    reinforce_half_stable_entropy,
    rl_baselines_comparison,
    sgs_conjecturer_conditions_on_unsolved,
    sgs_guide_scores_quality,
    sgs_outperforms_stp,
    solver_improves_steadily,
    sparse_reward_problem,
)

PRIORS = {
    # Core hypothesis: empirically validated by the Guide ablation
    guide_hypothesis: (
        0.82,
        "LLMs as Guides is validated by the ablation showing 1.6% performance gap between "
        "SGS (with Guide) and No Guide, and by the Guide's ability to keep disjunctive conclusion "
        "rates near the D3k baseline (<10%) while No Guide collapses to >80%.",
    ),

    # Empirical observations from paper -- all from paper's Figure 4
    rl_baselines_comparison: (
        0.96,
        "Directly observed experimental result from Figure 4: REINFORCE1/2 at 60.3%, EI at "
        "60.0%, CISPO at 57.5%. High-confidence empirical measurement with tuned hyperparameters.",
    ),
    cispo_entropy_collapse: (
        0.95,
        "Directly observed in Figure 4 and 11: CISPO's entropy drops to near-zero. Well-documented "
        "phenomenon confirmed by ablation experiment.",
    ),
    reinforce_half_stable_entropy: (
        0.92,
        "Directly observed in Figure 7 (SGS with REINFORCE1/2 vs CISPO): REINFORCE1/2 maintains "
        "stable entropy throughout training, confirmed by solve rate distribution.",
    ),
    cispo_solver_kills_conjecturer: (
        0.92,
        "Directly observed in Figure 7: SGS with CISPO Solver achieves ~57.5% asymptotic solve "
        "rate (same as standalone CISPO), confirming that entropy collapse starves the Conjecturer.",
    ),
    solver_improves_steadily: (
        0.94,
        "Directly observed in Figure 3: Solver pass@8 increases from ~42.5% to ~60% over 200 "
        "iterations without catastrophic forgetting.",
    ),

    # Ablation results
    no_problem_cond_fails: (
        0.94,
        "Directly observed in Figure 6: No Problem Conditioning does not outperform RL baseline "
        "(60.3%), despite producing many solvable synthetic problems. Clear empirical result.",
    ),
    no_guide_lower_performance: (
        0.94,
        "Directly observed in Figure 6: No Guide achieves 65.5% vs SGS 67.1%. Empirical "
        "measurement with fitted scaling laws, difference (1.6%) exceeds 1.1% uncertainty threshold.",
    ),
    frozen_conjecturer_suboptimal: (
        0.92,
        "Directly observed in Figure 6: Frozen Conjecturer outperforms RL but is inferior to SGS "
        "and No Guide. The decreasing solvable synthetic problem count is directly observed.",
    ),
    sgs_outperforms_stp: (
        0.90,
        "Directly observed in Figure 12: SGS surpasses STP after 1M generations. STP is the "
        "most closely related prior method (Dong & Ma 2025).",
    ),

    # Algorithm design facts
    sgs_conjecturer_conditions_on_unsolved: (
        0.98,
        "Definitional property of SGS algorithm: by construction the Conjecturer generates one "
        "synthetic problem per unsolved target (Algorithm 1 in paper). Deterministic design choice.",
    ),
    sgs_guide_scores_quality: (
        0.97,
        "Definitional property of SGS algorithm: Guide scoring is a core component (Algorithm 1, "
        "Section 3.2). The rubric (relevance + elegance) is explicitly stated.",
    ),
    guide_sft_prevents_format_errors: (
        0.95,
        "Empirical measurement from Section 4.1: base model without SFT produces 54.7% "
        "well-formatted outputs; after SFT on 2,048 examples, >99%. Direct measurement.",
    ),

    # Abduction components: predictions
    pred_sgs: (
        0.83,
        "SGS's predicted higher performance is well-motivated by the two anti-collapse mechanisms "
        "(Guide + problem conditioning) and the Guide hypothesis. Prediction is specific and "
        "falsifiable: 67.1% vs 60.3% baseline.",
    ),
    pred_alt_sgs: (
        0.40,
        "The alternative (SGS gains are purely from more data, not Guide quality) is partially "
        "plausible -- more training data does help. But the No Guide ablation shows the alternative "
        "predicts ~65.5%, not 67.1%, and No Guide Conjecturer collapses to disjunctive problems.",
    ),
    alt_sgs_no_gain: (
        0.28,
        "The alternative (no benefit from self-guidance beyond extra data) is contradicted by: "
        "(1) No Guide ablation showing 1.6% gap, and (2) No Guide Conjecturer collapse to >80% "
        "disjunctive conclusions. The alternative has some merit (conditioning alone helps) but "
        "the Guide's specific benefit is empirically demonstrated.",
    ),

    # Sparse reward problem -- well-established literature
    sparse_reward_problem: (
        0.92,
        "Well-established problem in RL literature: sparse rewards make it hard to learn complex "
        "behaviors. Asymmetric self-play as a solution is proposed in Sukhbaatar 2017 and "
        "Florensa 2018, with substantial empirical support.",
    ),

    # Limitations: all are paper's stated assessments
    limitation_verifiable_domain: (
        0.95,
        "Factual statement about current SGS experiments: only Lean4 formal math is tested. "
        "The extension challenge (full MDP specification) is straightforward engineering assessment.",
    ),
    limitation_frozen_guide: (
        0.90,
        "Paper's stated limitation: Guide is not trained during SGS. The concern about future "
        "scalability is a reasonable engineering judgment about adaptation requirements.",
    ),
    limitation_model_size: (
        0.93,
        "Factual: all experiments use 7B parameter model. The hypothesis about larger model "
        "scaling is stated but not tested -- correctly labeled as future work.",
    ),
    future_non_verifiable: (
        0.75,
        "Extension to non-verifiable domains via approximate verification is plausible (learned "
        "verifiers for math have improved; code unit tests are practical) but untested in SGS "
        "context. Moderate confidence given the rapid progress in learned verifiers.",
    ),
}
