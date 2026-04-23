"""Section 4: Empirical Results — Performance, Transfer, and Algorithm Comparison"""

from gaia.lang import claim, setting, support, deduction, induction, abduction, compare

from .motivation import echo_chamber_hypothesis
from .s2_setup import (
    evaluation_metrics_definition,
    rl_algorithms_definition,
    olmo_architecture,
    tinygsm_definition,
    openmathinstruct2_definition,
)
from .s3_distribution_collapse import (
    rl_amplifies_single_mode,
    scale_determines_format_preference,
    obs_format_collapse_epoch1,
    obs_diversity_decline,
    theoretical_mixture_model,
    obs_tinygsm_dominates_150m,
    obs_omi2_dominates_1b,
    obs_collapse_coincides_with_accuracy,
)

# ── Settings ─────────────────────────────────────────────────────────────────

gsm8k_finetuning_setup = setting(
    "RL fine-tuning is applied using GSM8K training split questions (~7,473 problems). "
    "GSM8K consists of grade-school math word problems requiring multi-step arithmetic reasoning. "
    "The binary reward function grants +1 for a final answer matching the ground truth, 0 otherwise.",
    title="GSM8K fine-tuning setup",
)

math500_benchmark = setting(
    "MATH-500 is a benchmark of 500 competition mathematics problems at difficulty levels "
    "1–5 (AMC/AIME style). It is substantially harder than GSM8K and tests whether "
    "improvements on easy problems transfer to harder reasoning tasks.",
    title="MATH-500 benchmark definition",
)

aime_benchmark = setting(
    "AIME (American Invitational Mathematics Examination) problems represent the highest "
    "difficulty level tested. Only a small fraction of state-of-the-art models can solve "
    "any AIME problem. Used to test upper-end transfer.",
    title="AIME benchmark definition",
)

# ── Performance Results ───────────────────────────────────────────────────────

obs_gsm8k_pass1_improvement = claim(
    "After PPO fine-tuning on the GSM8K training set, 1B models show pass@1 accuracy "
    "improvements of 5–15 percentage points depending on pretraining composition, "
    "while Majority@64 improves by approximately 5 percentage points. "
    "Pass@64 accuracy either stays flat or declines relative to the base model.",
    title="GSM8K pass@1 improvement after PPO (1B models)",
    metadata={"source_section": "Section 4", "figure": "artifacts/2504.07912.pdf, Figure 2"},
)

obs_math500_transfer_1b = claim(
    "For 1B models, RL fine-tuning on GSM8K transfers to MATH-500 performance. "
    "Key results by pretraining mixture:\n\n"
    "| Pretraining mixture | Pre-RL pass@1 | Post-RL pass@1 | Gain |\n"
    "|---------------------|---------------|----------------|------|\n"
    "| TinyGSM + 4×OMI1    | 8.60%         | 12.60%         | +4.0% |\n"
    "| TinyGSM + OMI2      | 33.40%        | 43.60%         | +10.2% |\n"
    "| OMI2 only           | ~30%          | ~40%           | ~+10% |\n\n"
    "Models with OpenMathInstruct2 in pretraining show the largest absolute gains (up to ~10 percentage points).",
    title="MATH-500 transfer results for 1B models",
    metadata={
        "source_section": "Section 4",
        "figure": "artifacts/2504.07912.pdf, Table 1 / Figure 4",
    },
)

obs_aime_limited_transfer = claim(
    "On AIME problems, RL fine-tuning on GSM8K produces limited pass@1 and Majority@64 "
    "improvements for most model configurations. Pass@64 improvements are observed across "
    "most configurations, suggesting some benefit from increased diversity at inference time "
    "despite the low pass@1 gains.",
    title="AIME transfer is limited (pass@1 and Majority@64)",
    metadata={"source_section": "Section 4"},
)

obs_omi2_pretrain_best_transfer = claim(
    "Among all pretraining mixtures tested, configurations that include OpenMathInstruct2 "
    "(natural language chain-of-thought at 14M pairs) in pretraining consistently produce "
    "the highest post-RL MATH-500 pass@1 performance for 1B models, outperforming "
    "code-only pretraining mixtures (TinyGSM + OMI1) by approximately 30 percentage points "
    "(43.60% vs. 12.60% on MATH-500 pass@1 after RL).",
    title="OMI2 pretraining yields best transfer after RL (1B models)",
    metadata={"source_section": "Section 4"},
)

# ── Algorithm Comparison ──────────────────────────────────────────────────────

obs_ppo_most_stable = claim(
    "Among the three RL algorithms tested (PPO, GRPO, Expert Iteration), "
    "PPO is the most stable: it consistently improves pass@1 without performance collapses. "
    "GRPO is less stable, occasionally exhibiting reward collapse during training. "
    "Expert Iteration underperforms both PPO and GRPO on final pass@1 accuracy.",
    title="PPO most stable; GRPO unstable; Expert Iteration underperforms",
    metadata={"source_section": "Section 4.3"},
)

obs_algorithm_agreement_on_format = claim(
    "Despite differences in stability and final accuracy, all three RL algorithms (PPO, "
    "GRPO, Expert Iteration) produce the same qualitative format collapse: they converge "
    "to amplifying the same dominant pretraining distribution mode (determined by model "
    "scale) within the same early training epochs.",
    title="All algorithms produce same format collapse pattern",
    metadata={"source_section": "Section 4.3"},
)

# ── Within-Distribution Refinement ───────────────────────────────────────────

obs_within_distribution_refinement = claim(
    "When models are pretrained on a single instruction dataset (no mixture), "
    "RL fine-tuning still produces meaningful improvements. The mechanism shifts from "
    "format selection to within-distribution refinement: RL standardises stylistic "
    "choices within the dominant format (e.g., consistent docstring formatting conventions "
    "in code-style outputs, consistent problem-solving structure in prose-style outputs).",
    title="RL refines within-distribution style when no mixture is present",
    metadata={"source_section": "Section 4.2"},
)

# ── KL Hyperparameter Sensitivity ────────────────────────────────────────────

obs_kl_coefficient_effect = claim(
    "Varying the KL regularisation coefficient $\\beta$ between 0.001 and 0.01 affects "
    "format diversity during training: higher $\\beta = 0.01$ preserves format diversity "
    "longer (slower collapse) while achieving comparable final pass@1 accuracy. "
    "Removing KL regularisation entirely ($\\beta = 0$) performs similarly to standard "
    "KL settings in terms of final pass@1.",
    title="KL coefficient affects collapse speed but not final accuracy",
    metadata={"source_section": "Section 4.4"},
)

# ── Derived Claims from Results ───────────────────────────────────────────────

rl_improves_easy_transfers_hard = claim(
    "RL fine-tuning on easy math problems (GSM8K training set) leads to meaningful "
    "performance improvements on harder benchmarks (MATH-500), demonstrating positive "
    "transfer from simple to complex reasoning. The transfer magnitude depends strongly "
    "on pretraining composition: natural-language pretraining (OMI2) enables larger transfers "
    "than code-only pretraining (TinyGSM + OMI1) for 1B models.",
    title="RL on easy problems transfers to harder reasoning (scale and format dependent)",
    metadata={"source_section": "Section 4"},
)

strat_transfer_evidence = support(
    [obs_gsm8k_pass1_improvement, obs_math500_transfer_1b, obs_omi2_pretrain_best_transfer],
    rl_improves_easy_transfers_hard,
    reason=(
        "@obs_gsm8k_pass1_improvement confirms GSM8K pass@1 gains of 5-15pp after PPO RL. "
        "@obs_math500_transfer_1b shows MATH-500 pass@1 gains of up to 10.2pp after "
        "GSM8K-only RL training, confirming positive transfer to harder problems. "
        "@obs_omi2_pretrain_best_transfer quantifies the composition dependence: "
        "OMI2 pretraining (natural language) yields ~30pp higher MATH-500 accuracy "
        "than code-only pretraining after RL, showing that the format selected by RL "
        "(@scale_determines_format_preference for 1B → OMI2) determines transfer effectiveness."
    ),
    prior=0.87,
    background=[math500_benchmark, gsm8k_finetuning_setup],
)

algorithm_invariant_collapse = claim(
    "The format collapse phenomenon (RL amplifying a single pretraining distribution mode) "
    "is robust across RL algorithm choice: PPO, GRPO, and Expert Iteration all exhibit "
    "qualitatively identical format convergence, suggesting format collapse is a property "
    "of the pretraining-RL interaction, not of any specific RL algorithm [@Zhao2025].",
    title="Format collapse is algorithm-invariant",
    metadata={"source_section": "Section 4.3"},
)

strat_algorithm_invariance = support(
    [obs_algorithm_agreement_on_format, obs_ppo_most_stable],
    algorithm_invariant_collapse,
    reason=(
        "@obs_algorithm_agreement_on_format shows all three algorithms converge to the same "
        "dominant format regardless of their mechanistic differences. "
        "Since @obs_ppo_most_stable confirms the algorithms differ in stability and final "
        "accuracy, yet produce the same collapse pattern, the collapse cannot be explained "
        "by any single algorithm's objective — it must arise from the pretraining initialisation."
    ),
    prior=0.85,
    background=[rl_algorithms_definition],
)

# ── Induction: multiple configurations confirm RL amplifies pretraining ───────

law_rl_amplifies_pretraining = claim(
    "Across all experimental configurations (different pretraining mixtures, model scales, "
    "and RL algorithms), RL post-training consistently amplifies a specific pretraining "
    "distribution mode rather than introducing novel behaviors. This is a universal "
    "property of RL post-training under binary reward on mathematical reasoning.",
    title="Universal law: RL amplifies pretraining modes (all configs)",
)

# Use the already-independent observations from s3 as induction predictions.
# obs_tinygsm_dominates_150m (prior=0.90) and obs_omi2_dominates_1b (prior=0.90)
# are direct empirical anchors; obs_collapse_coincides_with_accuracy (prior=0.88)
# provides temporal confirmation. All three have priors set in s3.
# Use the independent observations from s3 (obs_tinygsm_dominates_150m has prior=0.90,
# obs_omi2_dominates_1b has prior=0.90) as the induction predictions.
# This ensures backward flow from confirmed data to the law.
s_ind_150m = support(
    [law_rl_amplifies_pretraining],
    obs_tinygsm_dominates_150m,
    reason=(
        "The universal law predicts that 150M models will amplify the highest-reward "
        "pretraining format (TinyGSM code-style, due to its structured computability). "
        "This is directly observed as @obs_tinygsm_dominates_150m."
    ),
    prior=0.88,
)

s_ind_1b = support(
    [law_rl_amplifies_pretraining],
    obs_omi2_dominates_1b,
    reason=(
        "The universal law predicts that 1B models will amplify the highest-reward "
        "pretraining format (OMI2 natural language, due to larger capacity for NL reasoning). "
        "This is directly observed as @obs_omi2_dominates_1b."
    ),
    prior=0.88,
)

s_ind_algorithm = support(
    [law_rl_amplifies_pretraining],
    obs_collapse_coincides_with_accuracy,
    reason=(
        "The universal law predicts that format collapse coincides with accuracy gains "
        "regardless of RL algorithm, since the amplification mechanism is a property of "
        "pretraining, not the specific RL objective. @obs_collapse_coincides_with_accuracy "
        "confirms this."
    ),
    prior=0.85,
)

ind_150m_1b = induction(
    s_ind_150m,
    s_ind_1b,
    law=law_rl_amplifies_pretraining,
    reason=(
        "@obs_tinygsm_dominates_150m (150M scale) and @obs_omi2_dominates_1b (1B scale) "
        "are independent experiments at different model sizes — both confirm the law."
    ),
)

ind_all = induction(
    ind_150m_1b,
    s_ind_algorithm,
    law=law_rl_amplifies_pretraining,
    reason=(
        "@obs_collapse_coincides_with_accuracy is an independent temporal observation "
        "confirming that format collapse drives accuracy gains — independent of scale effects."
    ),
)

__all__ = [
    "rl_improves_easy_transfers_hard",
    "algorithm_invariant_collapse",
    "law_rl_amplifies_pretraining",
    "obs_gsm8k_pass1_improvement",
    "obs_math500_transfer_1b",
    "obs_omi2_pretrain_best_transfer",
    "obs_within_distribution_refinement",
    "obs_kl_coefficient_effect",
]
