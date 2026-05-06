"""Section 2: Related Work -- LRMs, reasoning defenses, and the gap CRAFT addresses.

The paper organizes prior work along two dimensions:

1. **Large reasoning models (LRMs)** and the techniques that improve their
   reasoning ability (inference-time scaling vs. learning-to-reason).
2. **Reasoning defense** -- the recent shift from output-only safety to
   safeguarding the reasoning *process*. This is grouped into three
   categories: training-time safety alignment, inference-time defenses, and
   guard models. The paper positions CRAFT in the first category but
   distinguishes itself by **proactively shaping the latent geometry of
   reasoning traces**, rather than relying on output-level constraints.

Source: [@Luo2026CRAFT, Sec. 2].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# LRM landscape
# ---------------------------------------------------------------------------

setup_lrm_taxonomy = setting(
    "**LRM taxonomy: inference scaling vs. learning to reason.** Methods "
    "that improve LRM reasoning fall into two categories: "
    "(i) **inference-time scaling** -- few-shot prompting, in-context "
    "learning [], chain-of-thought (CoT) prompting [@Wei2022CoT], "
    "Tree-of-Thoughts, Graph-of-Thoughts, self-consistency decoding, "
    "Plan-and-Solve, ReAct, Self-Ask, and self-refinement; and "
    "(ii) **learning-to-reason** -- post-training alignment such as "
    "RLHF [@Ouyang2022InstructGPT], DPO [@Rafailov2023DPO], GRPO "
    "[@Ramesh2024GRPO], process supervision [@Lightman2024PRM], and "
    "reinforcement learning with verifiable rewards (RLVR).",
    title="Setup: taxonomy of LRM reasoning-improvement methods (inference vs. learning-to-reason)",
)

claim_lrm_strong_reasoning = claim(
    "**LRMs achieve strong reasoning on math and logic.** Models such as "
    "DeepSeek-R1 [@Guo2025DeepSeekR1], the Qwen3 series [@Yang2025Qwen3], "
    "OpenAI o1 [@Jaech2024OpenAIo1], and Gemini have demonstrated strong "
    "performance on mathematical [@Shao2024DeepSeekMath] and logical "
    "reasoning tasks; these are the same model families that exhibit SSA "
    "and that CRAFT targets.",
    title="LRM landscape: strong math/logic performance attested across major model families",
)

# ---------------------------------------------------------------------------
# Reasoning defenses: three categories
# ---------------------------------------------------------------------------

setup_defense_taxonomy = setting(
    "**Reasoning-defense taxonomy.** Following [@Wang2025aSurveySafety], "
    "reasoning-level safety methods are grouped into three categories: "
    "(1) **training-time safety alignment** -- curating safety-oriented "
    "CoT trajectories or optimizing safety-aware reasoning objectives; "
    "(2) **inference-time defenses** -- allocating more test-time "
    "compute or steering the CoT trajectory during generation; "
    "(3) **guard models** -- post-hoc analyzers of intermediate "
    "reasoning traces that detect risk before the final output. CRAFT "
    "is a training-time alignment method.",
    title="Setup: three reasoning-defense categories (training / inference / guard)",
)

# ---------------------------------------------------------------------------
# Training-time alignment baselines (SafeChain, RealSafe, STAR, SafeKey, IPO,
# Deliberative, SaRO, STAIR, R2D, ERPO)
# ---------------------------------------------------------------------------

claim_safechain_method = claim(
    "**SafeChain [@Jiang2025bSafeChain] is an SFT-based reasoning-safety "
    "method.** It enforces structured safety reasoning via explicit "
    "refusal chains, by carefully filtering safe reasoning traces during "
    "supervised fine-tuning. It improves alignment while largely "
    "preserving reasoning capability, and is one of the six baselines "
    "CRAFT compares against [@Luo2026CRAFT, Sec. 2; Sec. 6].",
    title="Baseline: SafeChain (SFT with curated safe CoT traces)",
)

claim_realsafe_method = claim(
    "**RealSafe-R1 [@Zhang2025cRealSafe] is an SFT-based reasoning-"
    "safety method that aligns intermediate reasoning using distilled "
    "safety reasoning traces derived from the DeepSeek-R1 model "
    "[@Guo2025DeepSeekR1].** It is one of the six baselines CRAFT "
    "compares against [@Luo2026CRAFT, Sec. 6].",
    title="Baseline: RealSafe (SFT with distilled R1 safety traces)",
)

claim_star_method = claim(
    "**STAR [@Wang2025eSTAR] improves model safety by fine-tuning large "
    "reasoning models on self-generated, policy-aligned reasoning traces "
    "that explicitly justify refusal or compliance with safety "
    "guidelines.** STAR is one of the six baselines CRAFT compares "
    "against [@Luo2026CRAFT, Sec. 6].",
    title="Baseline: STAR (self-generated policy-aligned safety reasoning)",
)

claim_safekey_method = claim(
    "**SafeKey [@Zhou2025bSafeKey] extends STAR with additional "
    "supervision signals to strengthen reasoning-level safety "
    "constraints.** SafeKey is one of the six baselines CRAFT compares "
    "against and is among the strongest baselines on the joint "
    "reasoning-+-response safety metric [@Luo2026CRAFT, Sec. 6].",
    title="Baseline: SafeKey (STAR + extra supervision for reasoning safety)",
)

claim_ipo_method = claim(
    "**IPO [@Zhang2025bIPO] is an intervention-based preference "
    "optimization method that aligns reasoning safety by *substituting* "
    "unsafe reasoning steps with safety triggers and using the resulting "
    "pairs for preference learning.** IPO is one of the six baselines "
    "CRAFT compares against and is the strongest output-side baseline "
    "in [@Luo2026CRAFT, Table 1].",
    title="Baseline: IPO (intervention-based preference optimization)",
)

claim_reasoningshield_method = claim(
    "**ReasoningShield [@Li2025aReasoningShield] is a safety-detection "
    "model tailored to reasoning traces; it identifies hidden risks "
    "within intermediate reasoning steps via a structured evaluation "
    "and contrastive learning pipeline.** It functions as a guard model "
    "rather than a training-time alignment method; it is one of the six "
    "baselines CRAFT compares against [@Luo2026CRAFT, Sec. 6].",
    title="Baseline: ReasoningShield (guard model with contrastive risk detection)",
)

claim_other_training_methods = claim(
    "**Other training-time safety-reasoning methods.** Beyond the six "
    "directly-evaluated baselines, the related-work section also "
    "reviews Deliberative Alignment [@Guan2024Deliberative], SaRO "
    "[@Mou2025SaRO], STAIR [@Zhang2025dSTAIR], R2D [@Zhu2025R2D], and "
    "ERPO [@Feng2025ERPO], which encourage models to reason about "
    "safety constraints before answering. None of these methods "
    "explicitly aligns the *latent representations* of reasoning "
    "traces; they all operate over the textual reasoning trace itself.",
    title="Other training-time methods (Deliberative, SaRO, STAIR, R2D, ERPO) -- text-level only",
)

# ---------------------------------------------------------------------------
# Inference-time defenses
# ---------------------------------------------------------------------------

claim_inference_time_defenses = claim(
    "**Inference-time defenses.** This category includes (i) allocating "
    "more test-time reasoning compute [@Zaremba2025Trading], (ii) "
    "decoding-time control that regulates how much CoT is produced "
    "[@Jiang2025bSafeChain], (iii) early-stage priming that injects a "
    "short safety signal at the start to bias subsequent reasoning "
    "[@Jeung2025SAFEPATH], and (iv) process-level intervention that "
    "edits or corrects intermediate reasoning steps "
    "[@Wu2025bThinkingIntervention; @Zhang2025bIPO; "
    "@Li2025aReasoningShield]. These methods are reactive (operating "
    "during generation) rather than proactively shaping the latent "
    "representation; they do not perform training-time alignment.",
    title="Category: inference-time defenses (reactive, no training-time latent alignment)",
)

# ---------------------------------------------------------------------------
# Guard models
# ---------------------------------------------------------------------------

claim_guard_models = claim(
    "**Guard models.** ReasoningShield [@Li2025aReasoningShield], "
    "ThinkGuard [@Wen2025ThinkGuard], and GuardReasoner "
    "[@Liu2025GuardReasoner] are reasoning-aware safeguards that "
    "improve robustness against diverse and previously unseen jailbreak "
    "attempts by analyzing intermediate reasoning traces for hidden "
    "risk. They are post-hoc detectors layered on top of the model's "
    "outputs; they do not change the underlying generation policy.",
    title="Category: guard models (post-hoc reasoning-trace analyzers)",
)

# ---------------------------------------------------------------------------
# The gap: CRAFT's distinguishing position
# ---------------------------------------------------------------------------

claim_prior_work_gap = claim(
    "**Gap in prior work: no training-time method directly shapes the "
    "*latent geometry* of reasoning traces.** All training-time "
    "alignment baselines (SafeChain, RealSafe, STAR, SafeKey, IPO, "
    "Deliberative Alignment, SaRO, STAIR, R2D, ERPO) operate over the "
    "*textual* reasoning trace -- either by curating textual safety "
    "demonstrations, by intervening on text-level intermediate "
    "reasoning, or by optimizing preference pairs derived from textual "
    "traces. Inference-time defenses are reactive rather than aligning. "
    "Guard models are post-hoc detectors. None directly aligns "
    "*hidden representations* of reasoning trajectories during training. "
    "CRAFT addresses this gap by performing *proactive alignment at the "
    "reasoning level*, directly shaping the latent geometry of "
    "reasoning traces during training [@Luo2026CRAFT, Sec. 2].",
    title="Gap: no prior method aligns the latent geometry of reasoning traces during training",
)

claim_lrm_attack_surface_growing = claim(
    "**Stronger reasoning expands the jailbreak attack surface.** "
    "Recent literature [@Jiang2025bSafeChain; @Wang2025aSurveySafety] "
    "shows that long reasoning traces can be exploited or adversarially "
    "optimized -- improving raw reasoning ability without explicit "
    "control over the *internal* reasoning process can increase safety "
    "exposure rather than decrease it. This motivates approaches like "
    "CRAFT that directly regulate intrinsic reasoning, rather than "
    "relying solely on output-level constraints "
    "[@Luo2026CRAFT, Sec. 2].",
    title="Argument: improving reasoning without internal-process control increases attack surface",
)

__all__ = [
    "setup_lrm_taxonomy",
    "setup_defense_taxonomy",
    "claim_lrm_strong_reasoning",
    "claim_safechain_method",
    "claim_realsafe_method",
    "claim_star_method",
    "claim_safekey_method",
    "claim_ipo_method",
    "claim_reasoningshield_method",
    "claim_other_training_methods",
    "claim_inference_time_defenses",
    "claim_guard_models",
    "claim_prior_work_gap",
    "claim_lrm_attack_surface_growing",
]
