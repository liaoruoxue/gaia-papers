"""Section 5-6: Related Work and Discussion — Implications"""

from gaia.lang import (
    claim, setting,
    support, deduction,
    contradiction,
)

from .motivation import (
    claim_pretraining_hypothesis, claim_rlvr_improves_qwen,
    claim_spurious_fails_non_qwen, claim_qwen_centric_risk,
)

from .s3_cross_model import (
    claim_model_family_consistency, claim_ttrl_one_shot_same_pattern,
)

from .s4_code_reasoning import (
    claim_code_freq_increases_rlvr, claim_lang_to_code_contribution,
    claim_clipping_qwen_specificity, claim_no_repetition_pattern,
    claim_grpo_clipping_bias, claim_no_clipping_no_gain,
)

# ── Implications / Discussion claims ──────────────────────────────────────────

claim_implication_pretraining_primary = claim(
    "Base model pretraining significantly affects RLVR training outcomes: the "
    "reasoning strategies instilled during pretraining heavily impact which "
    "RLVR reward signals are effective and what performance improvements are "
    "achievable. Models with strong math-oriented pretraining (Qwen2.5-Math) "
    "respond to a wide range of rewards; models without it (OLMo2, Llama) "
    "require genuinely informative rewards.",
    title="Implication 1: pretraining is the primary determinant of RLVR effectiveness",
)

claim_implication_corrupted_supervision = claim(
    "Even corrupted or spurious supervision can enhance reasoning performance "
    "when it triggers useful pre-existing behaviors. The reward signal does not "
    "need to be semantically correct — it only needs to provide a training "
    "dynamic that concentrates probability mass on already-learned, "
    "high-performing behavioral patterns.",
    title="Implication 2: corrupted supervision can still improve reasoning by eliciting pretraining",
)

claim_implication_no_generalization = claim(
    "Effects observed in one model family may not generalize to other families. "
    "Conclusions from Qwen-centric RLVR experiments — even if internally "
    "reproducible — cannot be assumed to reflect general principles of RLVR, "
    "because the Qwen2.5-Math family is uniquely susceptible to spurious "
    "training signals due to its pretraining distribution.",
    title="Implication 3: RLVR effects are model-family-specific and do not generalize",
)

claim_prompt_sensitivity = claim(
    "Qwen2.5-Math-7B shows unreasonably high sensitivity to the evaluation "
    "prompt. Initial MATH-500 accuracy varies substantially across prompts: "
    "49.4% (Qwen default), 55.8% (Math Problem prompt), 63.2% (SimpleRL-Zoo), "
    "61.6% (Sober), 68.8% (Spurious LIPSUM prompt). The spurious LIPSUM prompt "
    "— consisting of random LaTeX placeholder text — achieves the highest "
    "initial accuracy. RLVR training trajectories also vary significantly by "
    "prompt, though models generally converge to similar performance.",
    title="Qwen2.5-Math-7B prompt sensitivity: spurious LIPSUM prompt yields highest 68.8% MATH-500 accuracy",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Table 5 and Figure 18"},
)

claim_post_rl_saturation = claim(
    "Models that have already undergone substantial RL post-training (Qwen2.5-"
    "Math-7B-Instruct, Qwen2.5-7B-Instruct) show minimal improvement from "
    "additional RLVR with any reward type, including ground truth rewards. "
    "This suggests these models have already reached saturation in terms of "
    "surfaceable pretraining capabilities, consistent with the pretraining "
    "hypothesis — once the elicitable representations are fully activated, "
    "additional RLVR provides limited marginal gain.",
    title="Post-RL saturated models (Qwen Instruct) show minimal further improvement under RLVR",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 19"},
)

claim_open_question_mechanism = claim(
    "The exact mechanism by which GRPO clipping bias concentrates probability "
    "mass on the model's pre-existing high-prior behaviors remains an open "
    "question. While the mathematical derivation shows the clipping bias is "
    "nonzero and asymmetric (favoring high-prior tokens), the precise sequence "
    "by which this gradient signal translates to increased code reasoning "
    "frequency and performance — and why it is self-reinforcing — is not fully "
    "characterized.",
    title="Open question: exact mechanism connecting clipping bias to code frequency and performance",
)

# ── Contradiction: RLVR teaches vs surfaces ───────────────────────────────────

claim_rlvr_teaches = claim(
    "RLVR fundamentally teaches models new reasoning capabilities beyond what "
    "they have learned during pretraining — the reward signal provides gradient "
    "information that enables novel reasoning skills.",
)

not_both_teach_surface = contradiction(
    claim_rlvr_teaches,
    claim_pretraining_hypothesis,
    reason=(
        "These two claims represent fundamentally incompatible accounts of what "
        "RLVR accomplishes. If RLVR primarily surfaces pretraining representations, "
        "then randomly-rewarded models should improve — and they do. If RLVR "
        "teaches new capabilities, then spurious rewards should not enable gains "
        "beyond what prompting achieves. The evidence from random-reward "
        "experiments falsifies @claim_rlvr_teaches for Qwen2.5-Math models. "
        "Note: these cannot both be true, though it is possible that different "
        "aspects of RLVR serve both functions for different model families or "
        "training regimes."
    ),
    prior=0.92,
)

# ── Key implications supported ────────────────────────────────────────────────

strat_implication_1 = support(
    [claim_model_family_consistency, claim_pretraining_hypothesis,
     claim_clipping_qwen_specificity],
    claim_implication_pretraining_primary,
    reason=(
        "The consistency of RLVR outcomes within model families "
        "(@claim_model_family_consistency), explained by @claim_pretraining_hypothesis "
        "and made mechanistically concrete by @claim_clipping_qwen_specificity, "
        "collectively establish that pretraining is the primary variable determining "
        "RLVR effectiveness, supporting @claim_implication_pretraining_primary."
    ),
    prior=0.9,
)

strat_implication_2 = support(
    [claim_rlvr_improves_qwen, claim_lang_to_code_contribution,
     claim_code_freq_increases_rlvr],
    claim_implication_corrupted_supervision,
    reason=(
        "The fact that random and incorrect rewards yield 21-24 pp gains "
        "(@claim_rlvr_improves_qwen) via eliciting code reasoning "
        "(@claim_code_freq_increases_rlvr, @claim_lang_to_code_contribution) "
        "directly demonstrates @claim_implication_corrupted_supervision: the "
        "corrupted reward provides no correctness information but triggers "
        "a beneficial behavioral shift."
    ),
    prior=0.9,
)

strat_implication_3 = support(
    [claim_spurious_fails_non_qwen, claim_ttrl_one_shot_same_pattern,
     claim_qwen_centric_risk],
    claim_implication_no_generalization,
    reason=(
        "Both our spurious rewards (@claim_spurious_fails_non_qwen) and published "
        "RLVR methods (@claim_ttrl_one_shot_same_pattern) fail to generalize "
        "beyond Qwen models. @claim_qwen_centric_risk establishes that this is "
        "a research methodology problem. Together these establish "
        "@claim_implication_no_generalization: model-specific findings should "
        "not be treated as general principles."
    ),
    prior=0.85,
)

strat_prompt_sensitivity_pretraining = support(
    [claim_prompt_sensitivity, claim_pretraining_hypothesis],
    claim_implication_corrupted_supervision,
    reason=(
        "Even spurious LIPSUM prompts improve Qwen2.5-Math-7B performance by "
        "+19.4 pp above the Qwen default prompt (@claim_prompt_sensitivity), "
        "without any training. This mirrors the spurious-reward phenomenon: "
        "any perturbation that activates a different pretraining distribution "
        "mode can surface better-performing reasoning patterns. This reinforces "
        "@claim_implication_corrupted_supervision — the input need not be "
        "semantically informative to unlock pretrained capabilities."
    ),
    prior=0.75,
)
