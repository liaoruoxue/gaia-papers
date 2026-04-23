"""Section 3: Distribution Collapse — RL Amplifies a Single Pretraining Mode"""

from gaia.lang import claim, setting, support, deduction, abduction, compare, contradiction

from .motivation import echo_chamber_hypothesis, controlled_study_value
from .s2_setup import (
    format_distinctiveness,
    format_tracking_method,
    tinygsm_definition,
    openmathinstruct1_definition,
    openmathinstruct2_definition,
    rl_algorithms_definition,
    evaluation_metrics_definition,
    controlled_ablation_design,
    olmo_architecture,
)

# ── Settings ─────────────────────────────────────────────────────────────────

mixture_experiment_setup = setting(
    "Mixture experiment: models are pretrained on combinations such as "
    "TinyGSM + 4×OpenMathInstruct1, TinyGSM + OpenMathInstruct2, etc. "
    "After pretraining, PPO fine-tuning is applied on GSM8K training questions "
    "for multiple epochs. Format proportions are tracked at each checkpoint.",
    title="Mixture experiment setup",
)

# ── Observations (high-prior empirical facts) ────────────────────────────────

obs_format_collapse_epoch1 = claim(
    "In models pretrained on mixtures of TinyGSM, OpenMathInstruct1 (OMI1), and "
    "OpenMathInstruct2 (OMI2), RL fine-tuning causes the proportion of outputs "
    "matching a single pretraining distribution to rise from roughly 33% (uniform "
    "mixture baseline) to over 80% within the first training epoch. "
    "Outputs matching the other distributions drop correspondingly to near zero.",
    title="Format collapse to single distribution within epoch 1",
    metadata={
        "source_section": "Section 3",
        "figure": "artifacts/2504.07912.pdf, Figure 2",
        "caption": "Format proportion trajectories during RL training showing rapid convergence.",
    },
)

obs_collapse_coincides_with_accuracy = claim(
    "The rapid format collapse to a single distribution (observed within epoch 1 of RL) "
    "coincides temporally with the largest improvements in pass@1 accuracy on GSM8K. "
    "After collapse, accuracy improvements slow substantially.",
    title="Format collapse coincides with peak accuracy gain",
    metadata={
        "source_section": "Section 3",
        "figure": "artifacts/2504.07912.pdf, Figure 2",
    },
)

obs_diversity_decline = claim(
    "After RL fine-tuning, pass@64 accuracy (probability that at least one of 64 "
    "samples is correct) either stays flat or declines relative to the pretrained "
    "base model, despite pass@1 (single greedy decoding accuracy) improving. "
    "This indicates reduced generation diversity.",
    title="Diversity (pass@64) declines post-RL despite pass@1 gains",
    metadata={"source_section": "Section 3"},
)

obs_tinygsm_dominates_150m = claim(
    "For 150M parameter models pretrained on mixtures including TinyGSM, OMI1, and OMI2, "
    "RL fine-tuning consistently amplifies TinyGSM-format (Python code) outputs. "
    "The 150M model converges to code-style responses in over 80% of generations "
    "regardless of the relative mixture proportion of each dataset.",
    title="150M models converge to TinyGSM (code) format",
    metadata={
        "source_section": "Section 3",
        "figure": "artifacts/2504.07912.pdf, Figure 3",
    },
)

obs_omi2_dominates_1b = claim(
    "For 1B parameter models pretrained on the same dataset mixtures, RL fine-tuning "
    "amplifies OpenMathInstruct2-format (natural language chain-of-thought) outputs. "
    "The 1B model converges to natural-language responses in over 80% of generations, "
    "contrasting directly with the 150M model's preference for code.",
    title="1B models converge to OMI2 (natural language) format",
    metadata={
        "source_section": "Section 3",
        "figure": "artifacts/2504.07912.pdf, Figure 3",
    },
)

# ── Theoretical Model ────────────────────────────────────────────────────────

theoretical_mixture_model = claim(
    "Under the assumption that the pretrained reference policy decomposes as a mixture "
    "of $k$ distinct sub-policies $\\pi_{\\text{ref}} = \\sum_{i=1}^{k} w_i \\pi_i$ "
    "(each $\\pi_i$ corresponding to a pretraining data source with mixture weight $w_i$), "
    "RL optimisation with KL regularisation (coefficient $\\beta$) reweights the mixture: "
    "the post-RL policy concentrates mass on the $\\pi_i$ with highest expected reward, "
    "with reweighting proportional to $\\exp(R_i / \\beta)$ where $R_i$ is the average "
    "reward under sub-policy $i$. This causes exponential amplification of the best-performing format.",
    title="Theoretical mixture model for RL amplification",
    metadata={"source_section": "Section 3 / Theory"},
)

# ── Core Derived Claims ───────────────────────────────────────────────────────

rl_amplifies_single_mode = claim(
    "RL post-training on mathematical reasoning problems amplifies a single pretraining "
    "data distribution mode while suppressing others, regardless of the initial mixture "
    "composition. The selection mechanism preferentially amplifies the highest-reward "
    "format present in pretraining, consistent with an exponential reweighting of "
    "mixture components by their average reward [@Zhao2025].",
    title="RL amplifies single pretraining mode (core empirical finding)",
    metadata={"source_section": "Section 3"},
)

strat_amplification_from_collapse = support(
    [obs_format_collapse_epoch1, obs_collapse_coincides_with_accuracy, theoretical_mixture_model],
    rl_amplifies_single_mode,
    reason=(
        "The empirical observation @obs_format_collapse_epoch1 shows that format proportions "
        "collapse from ~33% each to >80% for a single format within epoch 1. "
        "@obs_collapse_coincides_with_accuracy shows this collapse coincides with peak accuracy "
        "gains, establishing that the format convergence is the mechanism of improvement. "
        "@theoretical_mixture_model provides the formal explanation: RL with KL regularisation "
        "exponentially reweights mixture components, amplifying the highest-reward distribution."
    ),
    prior=0.90,
    background=[mixture_experiment_setup, format_tracking_method],
)

scale_determines_format_preference = claim(
    "Model scale is the primary determinant of which pretraining distribution RL amplifies: "
    "150M models amplify code-style (TinyGSM) outputs; 1B models amplify natural-language "
    "(OpenMathInstruct2) outputs. This scale-dependent preference holds across different "
    "pretraining mixture compositions tested [@Zhao2025].",
    title="Scale determines which format RL amplifies",
    metadata={"source_section": "Section 3"},
)

strat_scale_preference = support(
    [obs_tinygsm_dominates_150m, obs_omi2_dominates_1b],
    scale_determines_format_preference,
    reason=(
        "The contrast between @obs_tinygsm_dominates_150m (150M → code) and "
        "@obs_omi2_dominates_1b (1B → natural language) directly demonstrates that model "
        "scale, not pretraining mixture proportions, selects which format gets amplified. "
        "The same datasets are present in both experiments; only scale differs."
    ),
    prior=0.85,
    background=[olmo_architecture],
)

# ── Contradiction: diversity vs. accuracy ────────────────────────────────────

hypothetical_rl_improves_both = claim(
    "RL post-training simultaneously improves both pass@1 accuracy and pass@64 diversity "
    "across all experimental conditions tested.",
    title="Hypothetical: RL improves both pass@1 and diversity",
)

not_both_diversity_and_pass1_gain = contradiction(
    obs_diversity_decline,
    hypothetical_rl_improves_both,
    reason=(
        "The empirical results show a direct tradeoff: pass@1 improves but pass@64 "
        "declines or stays flat after RL. These two observations are incompatible under "
        "the same experimental conditions."
    ),
    prior=0.95,
)

# ── Abduction: echo chamber vs. pure capability improvement ──────────────────

alt_pure_capability = claim(
    "RL post-training introduces genuinely new mathematical reasoning capabilities not "
    "present in pretraining (alternative explanation: pure capability gain, not format amplification).",
    title="Alternative: RL introduces new capabilities",
)

pred_echo_chamber = claim(
    "Echo chamber hypothesis predicts: format proportions collapse to a single pretraining "
    "distribution mode, coinciding with accuracy gains, and pass@64 diversity declines.",
    title="Echo chamber prediction",
)

pred_pure_capability = claim(
    "Pure capability hypothesis predicts: format diversity is maintained or increases "
    "post-RL (new strategies discovered), and pass@64 improves alongside pass@1.",
    title="Pure capability prediction",
)

s_h_echo = support(
    [echo_chamber_hypothesis],
    obs_format_collapse_epoch1,
    reason=(
        "If @echo_chamber_hypothesis is correct — RL amplifies latent pretraining modes — "
        "then format collapse to a dominant pretraining distribution (@obs_format_collapse_epoch1) "
        "is the expected outcome. The hypothesis directly predicts this observation."
    ),
    prior=0.88,
)

s_alt_capability = support(
    [alt_pure_capability],
    obs_format_collapse_epoch1,
    reason=(
        "A pure capability gain hypothesis could in principle produce format collapse if "
        "the most capable approach happens to be code-style. However, @obs_diversity_decline "
        "(pass@64 declines) and @obs_collapse_coincides_with_accuracy (collapse at epoch 1) "
        "are harder to explain as pure capability discovery. The alternative has moderate "
        "explanatory power but requires auxiliary assumptions.",
    ),
    prior=0.35,
)

comp_echo_vs_capability = compare(
    pred_echo_chamber,
    pred_pure_capability,
    obs_format_collapse_epoch1,
    reason=(
        "The echo chamber prediction (format collapse to pretraining mode + diversity drop) "
        "matches @obs_format_collapse_epoch1 and @obs_diversity_decline exactly. "
        "The pure capability prediction (maintained or increased diversity + pass@64 gains) "
        "is directly contradicted by @obs_diversity_decline. Echo chamber fits substantially better."
    ),
    prior=0.88,
)

abd_echo_chamber = abduction(
    s_h_echo,
    s_alt_capability,
    comp_echo_vs_capability,
    reason=(
        "Both @echo_chamber_hypothesis and @alt_pure_capability are candidate explanations "
        "for the observed format collapse (@obs_format_collapse_epoch1). Abduction selects "
        "the hypothesis with better explanatory fit, here the echo chamber hypothesis."
    ),
    background=[obs_diversity_decline, controlled_ablation_design],
)

__all__ = [
    "rl_amplifies_single_mode",
    "scale_determines_format_preference",
    "obs_format_collapse_epoch1",
    "obs_diversity_decline",
    "theoretical_mixture_model",
]
