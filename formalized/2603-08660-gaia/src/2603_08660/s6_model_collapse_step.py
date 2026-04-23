"""Section 6: Model Collapse Step as a Model Prior Indicator"""

from gaia.lang import claim, setting, support, compare, abduction

from .s3_sharpening import theorem1_sharpening, sharpening_dual_nature
from .s4_rise_and_fall import rise_then_fall_universal, hyperparameter_robustness_collapse

# ─── Setup ───────────────────────────────────────────────────────────────────

exp_setup_s6 = setting(
    "Section 6 evaluates 7 models from 3 families—OLMo-2-1124-7B, Meta-Llama-3.1-8B, "
    "Qwen2.5-Math-1.5B, Qwen2.5-1.5B, Qwen2.5-7B, Qwen3-1.7B-Base, Qwen3-8B-Base—on AIME 2024. "
    "Three indicators are compared: "
    "(1) **GT Gain**: improvement from 1 epoch of standard supervised RLVR on DAPO-17k with "
    "ground-truth rewards; "
    "(2) **Pass@k Gain**: difference between pass@256 and pass@1 on AIME 2024 (no training); "
    "(3) **Model Collapse Step**: training step when Reward Accuracy drops below 1% during "
    "intrinsic URLVR with majority voting and default hyperparameters.",
    title="Section 6 evaluation setup",
)

model_comparison_setup = setting(
    "Section 6.1 compares four specific models in pilot study: Qwen2.5-1.5B and "
    "DeepSeek-R1-Distill-Qwen-1.5B (Qwen family); Llama-3.1-8B and Llama-3.1-Tulu-3-8B-SFT "
    "(LLaMA family). All trained on DAPO-17k with majority voting reward.",
    title="Pilot study model selection",
)

# ─── Pilot study: different models behave differently ────────────────────────

family_differences_obs = claim(
    "Intrinsic URLVR behavior differs substantially between model families and training stages "
    "(Figure 10): In the Qwen family, the SFT variant (DeepSeek-R1-Distill-Qwen-1.5B) maintains "
    "Reward Accuracy above 0.8 throughout training, while the base model (Qwen2.5-1.5B) drops "
    "to near zero by step 200. In the LLaMA family, both variants eventually collapse: Llama-3.1-8B "
    "base fails by step 40, while Llama-3.1-Tulu-3-8B-SFT shows initial gains before collapsing "
    "later. Qwen models appear fundamentally more stable than LLaMA models.",
    title="Cross-family and cross-training-stage differences in collapse timing",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 10"},
    background=[model_comparison_setup, exp_setup_s6],
)

entropy_not_predictor = claim(
    "High Actor Entropy at initialization does not predict better RL trainability. Base models "
    "from both Qwen and LLaMA families start with higher Actor Entropy yet perform worse than "
    "their SFT counterparts, with lower Reward Accuracy and faster collapse. This contradicts "
    "the hypothesis that entropy is the determinant of RL trainability; entropy is a consequence "
    "of the sharpening process, not its predictor.",
    title="Actor entropy is not a reliable predictor of RL trainability",
    background=[exp_setup_s6],
)

# ─── Model Collapse Step definition ──────────────────────────────────────────

model_collapse_step_definition = setting(
    "Model Collapse Step is defined as the training step at which Reward Accuracy falls below 1% "
    "during intrinsic URLVR training with majority voting reward and default hyperparameters. "
    "It captures how long a model can sustain intrinsic URLVR before reward hacking takes over. "
    "Formally: MCS = $\\min\\{t : \\text{RewardAccuracy}(t) < 0.01\\}$.",
    title="Model Collapse Step definition",
)

# ─── Collapse step values for 7 models ───────────────────────────────────────

collapse_step_values = claim(
    "Model Collapse Step values for 7 evaluated models on AIME 2024 with default hyperparameters:\n\n"
    "| Model | Collapse Step | GT Gain (AIME24) |\n"
    "|-------|-------------|------------------|\n"
    "| OLMo-2-1124-7B | 34 | +0.42% |\n"
    "| Meta-Llama-3.1-8B | 40 | +1.01% |\n"
    "| Qwen2.5-Math-1.5B | 160 | +3.96% |\n"
    "| Qwen2.5-1.5B | 221 | +3.96% |\n"
    "| Qwen2.5-7B | 245 | +6.67% |\n"
    "| Qwen3-1.7B-Base | 280 | +7.08% |\n"
    "| Qwen3-8B-Base | 383 | +17.08% |\n\n"
    "Models with later collapse steps consistently yield higher GT Gains from standard supervised RL.",
    title="Model Collapse Step values and GT Gains for 7 models",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 11"},
    background=[exp_setup_s6],
)

# ─── Accuracy as predictor ───────────────────────────────────────────────────

mcs_predicts_rl_gains = claim(
    "Model Collapse Step correlates strongly with Ground Truth (GT) Gain from standard supervised "
    "RLVR training. Models that sustain longer before collapse consistently yield better results "
    "when trained with ground-truth rewards. The correlation is stronger and more reliable than "
    "pass@k Gain, which correlates less reliably with actual RL gains and can be gamed by random "
    "guessing on multiple-choice questions when pass@k → 1 as k → ∞.",
    title="Model Collapse Step strongly predicts RL trainability (GT Gain)",
)

alt_passk_predictor = claim(
    "Pass@k Gain (difference between pass@256 and pass@1 on AIME 2024) serves as a static "
    "indicator of model prior / RL trainability without requiring any training, but has limitations: "
    "lower correlation accuracy with actual RL gains, and fails on multiple-choice questions where "
    "pass@k → 1 as k grows regardless of reasoning quality.",
    title="Pass@k Gain as alternative RL trainability predictor",
)

pred_mcs = claim(
    "Model Collapse Step predicts GT Gain with ranking correlation matching or surpassing pass@k Gain.",
    title="MCS prediction quality claim",
)
pred_passk = claim(
    "Pass@k Gain predicts GT Gain with lower ranking correlation than Model Collapse Step.",
    title="Pass@k prediction quality claim",
)
obs_gt_ranking = claim(
    "GT Gain rankings (from Figure 11): OLMo-7B < LLaMA-8B < Qwen2.5-Math < Qwen2.5-1.5B < Qwen2.5-7B < Qwen3-1.7B < Qwen3-8B, "
    "matching MCS rankings exactly; Pass@k Gain rankings have inversions (Qwen2.5-Math +30% vs Qwen3-1.7B +36.67% vs Qwen3-8B +56.67%, "
    "with LLaMA at +6.67 and OLMo at +6.67 near bottom as expected but Qwen-Math unusually high).",
    title="GT Gain vs MCS vs Pass@k ranking observation",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 11"},
)

comp_mcs_vs_passk = compare(
    pred_mcs, pred_passk, obs_gt_ranking,
    reason=(
        "Model Collapse Step rankings match GT Gain rankings exactly for all 7 models, "
        "while Pass@k Gain shows inversions (particularly Qwen2.5-Math ranks anomalously high "
        "vs actual RL gains, and the metric saturates for multiple-choice). "
        "MCS's dynamic measurement of training behavior better captures the confidence-correctness "
        "alignment that determines RL trainability."
    ),
    prior=0.83,
)

abd_mcs_better = abduction(
    support([mcs_predicts_rl_gains], obs_gt_ranking,
        reason="If MCS is the right indicator, models with higher MCS should rank higher in GT Gain—@collapse_step_values confirms this.", prior=0.88),
    support([alt_passk_predictor], obs_gt_ranking,
        reason="If pass@k is the right indicator, pass@k ranking should match GT Gain—but pass@k shows inversions for Qwen2.5-Math.", prior=0.55),
    comp_mcs_vs_passk,
    reason="Both MCS and pass@k attempt to explain which models will gain most from standard RL; the comparison reveals MCS is more aligned with actual GT Gain.",
)

# ─── Computation cost ────────────────────────────────────────────────────────

mcs_computation_efficiency = claim(
    "Model Collapse Step requires substantially less computation than the gold-standard GT Gain:\n\n"
    "| Indicator | Total Tokens | Requires GT Labels |\n"
    "|-----------|-------------|--------------------|\n"
    "| GT Gain | 6.66B tokens (7k×8×17k×7) | Yes |\n"
    "| Model Collapse Step | 1.19B tokens (7k×8×662×32) | No |\n\n"
    "Model Collapse Step is **5.6× faster** than full supervised RL training while preserving "
    "the relative ranking of model trainability. It requires no ground-truth labels, making it "
    "applicable even when verification is unavailable.",
    title="Model Collapse Step 5.6× computation advantage",
    metadata={"source_table": "artifacts/2603.08660.pdf, Table 3"},
)

# ─── Robustness across hyperparameters ───────────────────────────────────────

mcs_hyperparameter_robustness = claim(
    "Model Collapse Step rankings remain relatively stable across different hyperparameter settings. "
    "With aggressive hyperparameters (mini-batch size MBS=1 or rollout count N=32), collapse "
    "occurs faster in absolute steps, but the relative ranking of 7 models is preserved, enabling "
    "more rapid assessment. With MBS=1 and N=8, total steps across 7 models = 662 (vs. 7×280+ "
    "with default hyperparameters), enabling ≥50 steps faster assessment for strong-prior models.",
    title="MCS rankings stable across hyperparameters; aggressive settings accelerate measurement",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 12"},
)

strat_mcs_predicts = support(
    [theorem1_sharpening, collapse_step_values, mcs_hyperparameter_robustness],
    mcs_predicts_rl_gains,
    reason=(
        "Theorem 1 (@theorem1_sharpening) establishes that longer survival before collapse "
        "implies stronger confidence-correctness alignment in the model prior. The collapse step "
        "values (@collapse_step_values) show a monotonic relationship between collapse timing and "
        "GT Gain across 7 diverse models. The robustness result (@mcs_hyperparameter_robustness) "
        "confirms rankings are stable across hyperparameters, validating MCS as a reliable indicator "
        "rather than an artifact of specific training configurations."
    ),
    prior=0.86,
)
