from gaia.lang import (
    support, deduction, abduction, compare, complement, contradiction,
)

from .motivation import (
    setting_rl_reasoning,
    setting_grpo_definition,
    setting_verification_definition,
    verification_gap,
    verification_training_neglect,
    sft_limitation,
    research_question_tradeoff,
    core_contribution,
)

from .s2_method import (
    setting_grpo_objective,
    setting_advantage_normalization,
    setting_reward_scheme,
    grpo_verif_objective,
    grpo_verif_conditioning,
    alpha_hyperparameter,
    grpo_verif_no_critic,
    grpo_verif_addresses_gap,
)

from .s3_experiments import (
    setting_model,
    setting_training_data,
    setting_benchmarks,
    setting_hyperparameters,
    setting_baselines,
    result_solution_accuracy,
    result_verification_accuracy,
    grpo_improves_over_default_solution,
    grpo_improves_over_default_verification,
    grpo_verif_maintains_solution,
    grpo_verif_improves_verification,
    grpo_verif_amc23_verification,
    computational_overhead,
)

from .s4_related import (
    setting_ppo_based_verification,
    setting_star_approach,
    related_rise_comparison,
    related_prm_distinction,
    related_sft_distinction,
    related_novelty,
)

from .s5_conclusion import (
    conclusion_joint_training_viable,
    conclusion_verification_reliability,
    future_work_efficiency,
    future_work_alpha_study,
)

# ============================================================
# Pass 2-4: Strategies and Reasoning Connections
# ============================================================

# --- GRPO improves solution over default ---
strat_grpo_solution_improvement = support(
    [result_solution_accuracy],
    grpo_improves_over_default_solution,
    reason=(
        "The empirical data in @result_solution_accuracy shows GRPO achieves 38.4% average "
        "solution accuracy vs the default's 28.1%, a 10.3pp improvement. Standard GRPO "
        "(@setting_grpo_definition) trains the model with RL rewards tied to solution correctness, "
        "training on 6k math problems (@setting_training_data) with n=8 samples per question. "
        "This provides sufficient policy gradient signal for the improvement."
    ),
    prior=0.95,
    background=[setting_model, setting_benchmarks, setting_grpo_definition, setting_training_data],
)

# --- GRPO incidentally improves verification over default ---
strat_grpo_verification_incidental = support(
    [result_verification_accuracy],
    grpo_improves_over_default_verification,
    reason=(
        "The empirical data in @result_verification_accuracy shows GRPO achieves 32.9% average "
        "verification accuracy vs the default's 16.2%, a 16.7pp incidental gain. GRPO "
        "(@setting_grpo_definition) trains exclusively on solution correctness, yet verification "
        "improves because solving math problems well requires recognizing valid vs invalid "
        "reasoning steps, which implicitly trains verification-adjacent skills."
    ),
    prior=0.80,
    background=[setting_model, setting_benchmarks, setting_grpo_definition],
)

# --- GRPO-Verif objective design enables verification training ---
strat_verif_objective_design = support(
    [grpo_verif_objective, grpo_verif_conditioning],
    grpo_verif_addresses_gap,
    reason=(
        "The GRPO-Verif objective (@grpo_verif_objective) adds an explicit verification term "
        "weighted by $\\alpha$ to the solution loss. Verification responses are conditioned "
        "on both question and solution (@grpo_verif_conditioning), making verification an "
        "explicit gradient signal. By construction, this is within the RL framework, so no "
        "distribution shift from SFT arises. The claim follows as a strong structural implication "
        "from the objective definition."
    ),
    prior=0.95,
    background=[setting_grpo_definition, setting_verification_definition],
)

# --- GRPO-Verif maintains solution accuracy ---
strat_solution_maintained = support(
    [grpo_verif_objective, alpha_hyperparameter],
    grpo_verif_maintains_solution,
    reason=(
        "The GRPO-Verif objective (@grpo_verif_objective) keeps the solution generation term "
        "dominant, with verification weighted by $\\alpha=0.2$ (@alpha_hyperparameter). "
        "This means the policy gradient for solutions is 5× larger than for verifications, "
        "preserving the optimization pressure on solution quality. Empirically, "
        "@result_solution_accuracy shows 38.5% vs 38.4% for GRPO — within noise."
    ),
    prior=0.80,
    background=[setting_model, setting_benchmarks],
)

# --- GRPO-Verif improves verification accuracy ---
strat_verification_improved = support(
    [grpo_verif_objective, grpo_verif_conditioning],
    grpo_verif_improves_verification,
    reason=(
        "By adding explicit verification reward gradient (@grpo_verif_objective), the model "
        "receives direct training signal when its verification judgments are correct or wrong. "
        "The conditioning on solution (@grpo_verif_conditioning) ensures the model learns "
        "solution-specific verification. @result_verification_accuracy documents the 4.2pp "
        "gain (32.9% → 37.1%). The AMC23 gain of 15pp (@grpo_verif_amc23_verification) "
        "is the strongest single-benchmark evidence."
    ),
    prior=0.88,
    background=[setting_model, setting_benchmarks],
)

# --- AMC23 benchmark specific verification gain ---
strat_amc23_verification = support(
    [result_verification_accuracy],
    grpo_verif_amc23_verification,
    reason=(
        "The AMC23 row in @result_verification_accuracy directly records GRPO-Verif verification "
        "accuracy as 40.0% vs GRPO's 25.0%, a 15pp difference. This is a direct reading from "
        "experimental data."
    ),
    prior=0.95,
    background=[setting_model, setting_benchmarks],
)

# --- Abduction: does GRPO-Verif or GRPO better explain the verification accuracy data? ---
# Hypothesis: explicit verification training (GRPO-Verif) explains the 37.1% accuracy
# Alternative: implicit/incidental training (GRPO) is sufficient for good verification
alt_implicit_verif_sufficient = grpo_improves_over_default_verification  # already defined as claim

pred_grpo_verif_verif = grpo_verif_improves_verification
pred_grpo_implicit = grpo_improves_over_default_verification

s_h_verif = support(
    [grpo_verif_addresses_gap],
    result_verification_accuracy,
    reason=(
        "Explicit verification training (@grpo_verif_addresses_gap) directly optimizes for "
        "verification correctness. If explicit verification RL is the causal driver, we expect "
        "GRPO-Verif to outperform GRPO on verification — which is exactly the observed 37.1% > 32.9% "
        "in @result_verification_accuracy."
    ),
    prior=0.88,
)

s_alt_verif = support(
    [grpo_improves_over_default_verification],
    result_verification_accuracy,
    reason=(
        "Implicit/incidental verification training from solution-only GRPO already achieves 32.9% "
        "(@grpo_improves_over_default_verification). If implicit training were sufficient, we would "
        "not observe a meaningful gap between GRPO and GRPO-Verif. The observed data shows 32.9% "
        "for GRPO, which partially — but not fully — explains @result_verification_accuracy.",
    ),
    prior=0.45,
)

comp_verif = compare(
    grpo_verif_improves_verification,
    grpo_improves_over_default_verification,
    result_verification_accuracy,
    reason=(
        "GRPO-Verif's prediction (37.1%) is closer to the observed verification accuracy "
        "than GRPO's implicit prediction (32.9%). The 4.2pp gap in favor of GRPO-Verif is "
        "consistent and observed across 3 of 4 benchmarks."
    ),
    prior=0.82,
)

abduction_verification_mechanism = abduction(
    s_h_verif,
    s_alt_verif,
    comp_verif,
    reason=(
        "Both explicit verification training (GRPO-Verif) and implicit training (GRPO) "
        "attempt to explain the observed verification accuracy levels. Abduction determines "
        "which explanation better accounts for the data."
    ),
)

# --- No tradeoff between solution and verification objectives ---
strat_no_tradeoff = support(
    [grpo_verif_maintains_solution, grpo_verif_improves_verification],
    conclusion_joint_training_viable,
    reason=(
        "The combination of @grpo_verif_maintains_solution (solution accuracy preserved) and "
        "@grpo_verif_improves_verification (verification accuracy improved) together constitute "
        "evidence that the joint objective does not cause a harmful tradeoff. This directly "
        "answers the open question @research_question_tradeoff."
    ),
    prior=0.85,
    background=[research_question_tradeoff],
)

# --- Conclusion: verification reliability ---
strat_reliability_conclusion = support(
    [grpo_verif_improves_verification, grpo_verif_conditioning],
    conclusion_verification_reliability,
    reason=(
        "Improved verification accuracy (@grpo_verif_improves_verification) shows the model "
        "more reliably identifies correct vs incorrect solutions. The conditioning on the "
        "specific solution (@grpo_verif_conditioning) means the model is performing "
        "solution-specific verification, not generic quality assessment. Together these "
        "support the reliability conclusion."
    ),
    prior=0.80,
)

# --- Contradiction: verification hurts solution vs verification doesn't hurt solution ---
# These two stances on the tradeoff cannot both be true
not_both_tradeoff = contradiction(
    research_question_tradeoff,
    grpo_verif_maintains_solution,
    reason=(
        "The open concern (@research_question_tradeoff) that verification training might degrade "
        "solution accuracy is directly refuted by the experimental finding "
        "(@grpo_verif_maintains_solution) that solution accuracy is maintained. Both the concern "
        "and the finding cannot simultaneously be true once experimental evidence is available."
    ),
    prior=0.92,
)

# Note: sft_limitation and grpo_verif_addresses_gap can both be true simultaneously:
# SFT causes distribution shift (a general property of SFT-based verification)
# AND GRPO-Verif avoids it (a property of the proposed approach).
# No operator is needed — they are complementary, not contradictory, facts.
# The paper's argument is captured by strat_sft_distinction which connects both.

# --- Connect orphaned substantive claims with strategies ---

# verification_gap is supported by evidence that GRPO doesn't train verification
strat_verification_gap = support(
    [verification_training_neglect],
    verification_gap,
    reason=(
        "Because existing RL approaches like GRPO neglect explicit verification training "
        "(@verification_training_neglect), models trained this way do not develop reliable "
        "self-verification capabilities. The gap follows directly from the absence of "
        "verification-specific training signal."
    ),
    prior=0.82,
)

# core_contribution is supported by grpo_verif_objective
strat_core_contribution = support(
    [grpo_verif_objective],
    core_contribution,
    reason=(
        "The GRPO-Verif algorithm is defined by its unified objective (@grpo_verif_objective), "
        "which jointly optimizes both solution generation and self-verification without relying "
        "on SFT or a separate critic. The claim @core_contribution summarizes this contribution."
    ),
    prior=0.97,
)

# grpo_verif_no_critic is supported by the objective formulation
strat_no_critic = support(
    [grpo_verif_objective],
    grpo_verif_no_critic,
    reason=(
        "The GRPO-Verif objective (@grpo_verif_objective) uses rule-based rewards for both "
        "solutions and verifications, computed by checking correctness against ground truth. "
        "No learned value function or separate critic model appears in the formulation."
    ),
    prior=0.97,
    background=[setting_grpo_definition],
)

# computational_overhead follows from the algorithm requiring double generation
strat_computational_overhead = support(
    [grpo_verif_objective],
    computational_overhead,
    reason=(
        "The GRPO-Verif objective (@grpo_verif_objective) requires generating verification "
        "response $v^{(i)}$ for each solution $y^{(i)}$. This doubles the generation cost "
        "per training step compared to standard GRPO, which only generates solutions. "
        "The overhead is acknowledged as a limitation in the paper."
    ),
    prior=0.97,
    background=[setting_hyperparameters],
)

# related claims are supported by the algorithm design
strat_rise_comparison = support(
    [grpo_verif_no_critic],
    related_rise_comparison,
    reason=(
        "RISE uses PPO with a shared critic for verification training. GRPO-Verif does not "
        "require a critic (@grpo_verif_no_critic), distinguishing it from RISE's approach. "
        "This difference in critic requirement is the key differentiator."
    ),
    prior=0.88,
    background=[setting_ppo_based_verification],
)

strat_sft_distinction = support(
    [grpo_verif_addresses_gap, sft_limitation],
    related_sft_distinction,
    reason=(
        "GRPO-Verif avoids distribution shift by integrating verification into RL "
        "(@grpo_verif_addresses_gap), whereas SFT-based methods introduce distribution shift "
        "(@sft_limitation). The contrast establishes GRPO-Verif's advantage over SFT approaches."
    ),
    prior=0.90,
)

strat_related_novelty = support(
    [grpo_verif_no_critic, grpo_verif_addresses_gap, grpo_verif_objective],
    related_novelty,
    reason=(
        "GRPO-Verif's novelty stems from: critic-free design (@grpo_verif_no_critic), "
        "integration of verification into RL without distribution shift "
        "(@grpo_verif_addresses_gap), and explicit alpha-weighted auxiliary objective "
        "(@grpo_verif_objective). Together these distinguish it from all prior work."
    ),
    prior=0.88,
)

strat_prm_distinction = support(
    [grpo_verif_no_critic],
    related_prm_distinction,
    reason=(
        "Process Reward Models (PRMs) train a separate model to score intermediate reasoning "
        "steps. GRPO-Verif differs because it trains the same model (not a separate one) "
        "to verify, using group-normalized RL rewards rather than step-level supervision. "
        "The critic-free nature (@grpo_verif_no_critic) is the key distinguishing property."
    ),
    prior=0.90,
)

# future work claims are supported by limitations
strat_future_efficiency = support(
    [computational_overhead],
    future_work_efficiency,
    reason=(
        "The computational overhead (@computational_overhead) of generating both solution "
        "and verification per training step is a concrete limitation that motivates future "
        "work on efficiency optimizations."
    ),
    prior=0.90,
)

strat_future_alpha = support(
    [alpha_hyperparameter],
    future_work_alpha_study,
    reason=(
        "The fixed alpha=0.2 choice (@alpha_hyperparameter) has not been ablated across "
        "a range of values. The effect of different alpha values on solution vs verification "
        "accuracy tradeoff is an open empirical question motivating future work."
    ),
    prior=0.85,
)

# --- Exports ---
__all__ = [
    "core_contribution",
    "grpo_verif_objective",
    "grpo_verif_maintains_solution",
    "grpo_verif_improves_verification",
    "conclusion_joint_training_viable",
    "conclusion_verification_reliability",
    "result_solution_accuracy",
    "result_verification_accuracy",
]
