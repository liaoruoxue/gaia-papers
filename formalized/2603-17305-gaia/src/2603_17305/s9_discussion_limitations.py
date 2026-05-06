"""Section 7: Discussion and Conclusion -- synthesis, limitations, broader
impact.

This module captures the high-level synthesis claims, the
author-acknowledged limitations, and the impact statement.

Source: [@Luo2026CRAFT, Sec. 7; Impact Statement].
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# High-level synthesis
# ---------------------------------------------------------------------------

claim_synthesis_main = claim(
    "**Synthesis: CRAFT addresses superficial safety alignment by "
    "combining contrastive learning and reinforcement learning over "
    "latent representations to shift reasoning trajectories from "
    "unsafe regions toward safety-aligned ones.** Empirically, across "
    "two LRMs (DeepSeek-R1-Distill-Llama-8B [@Guo2025DeepSeekR1] + "
    "Qwen3-4B-Thinking [@Yang2025Qwen3]) and multiple safety "
    "benchmarks, CRAFT substantially improves both reasoning-trace "
    "safety (average +79.0%) and final-response safety (average "
    "+87.7%) while still maintaining competitive performance on math "
    "and code benchmarks (+4.7% Pass@1). Theoretically, the "
    "elimination of SSA at GRPO local optima is guaranteed by "
    "Theorem 5.1 under mild assumptions [@Luo2026CRAFT, Sec. 7].",
    title="Synthesis: latent-space CRAFT eliminates SSA empirically and theoretically",
)

claim_future_adaptive_signals = claim(
    "**Future direction: adaptive safety signals to reduce reliance on "
    "fixed evaluators.** The current $R_{txt}$ uses a fixed external "
    "discriminator (StrongReject [@Souly2024StrongReject]), and "
    "$R_{cons}$ depends on a fixed $P(S|y)$ (Assumption 5.3). The "
    "authors plan to explore *adaptive* safety signals that update "
    "during training, potentially reducing the dependency on a single "
    "external evaluator [@Luo2026CRAFT, Sec. 7].",
    title="Future work: adaptive safety signals to reduce fixed-evaluator dependence",
)

# ---------------------------------------------------------------------------
# Limitations (author-acknowledged + structural)
# ---------------------------------------------------------------------------

claim_lim_two_models = claim(
    "**Limitation: empirical evaluation covers two LRM families and "
    "does not include the full set of frontier reasoning models.** "
    "DeepSeek-R1-Distill-Llama-8B (8B) and Qwen3-4B-Thinking (4B) span "
    "two architectures, but do not include OpenAI o1 [@Jaech2024OpenAIo1], "
    "GPT-4o [@Hurst2024GPT4o] (closed-source), Phi-4-Reasoning "
    "[@Abdin2025Phi4], or larger frontier reasoning models -- so the "
    "+79.0% / +87.7% headlines should be interpreted as empirically "
    "demonstrated on these two open-weight LRMs, with extrapolation to "
    "larger / closed-source LRMs being an open question.",
    title="Limitation: only two open-weight LRMs evaluated (R1-Distill-Llama-8B + Qwen3-4B-Thinking)",
)

claim_lim_training_budget = claim(
    "**Limitation: under R1-Distill-Llama-8B, CRAFT does not top *every* "
    "individual benchmark cell -- IPO narrowly outperforms CRAFT on "
    "JBB Reasoning (0.057 vs 0.065) and on SR Reasoning (0.167 vs "
    "0.172).** The paper attributes this to current training-budget "
    "limitations and conjectures that extended training would close "
    "the gap. For now, the per-cell finding is that CRAFT is the "
    "best *overall* (lowest average) but not the best in every "
    "individual cell on R1-Distill-Llama-8B [@Luo2026CRAFT, Sec. 6.1].",
    title="Limitation: on R1-Distill-Llama-8B, IPO wins 2/4 cells; CRAFT wins overall avg",
)

claim_lim_fixed_evaluator = claim(
    "**Limitation: dependence on a fixed external safety evaluator.** "
    "Both $R_{txt}$ and Assumption 5.3 of Theorem 5.1 require a fixed "
    "$P(S|y)$. If the evaluator is biased, drifts under distribution "
    "shift, or fails on out-of-distribution prompts, the CRAFT signal "
    "inherits these weaknesses. This is a structural limitation "
    "shared with all RL-from-AI-feedback methods that rely on an "
    "external grader; the future-work direction of adaptive signals "
    "is the authors' planned mitigation [@Luo2026CRAFT, Sec. 7; "
    "Asm. 5.3].",
    title="Limitation: dependence on fixed external safety evaluator (StrongReject + GPT-4o)",
)

claim_lim_misuse_potential = claim(
    "**Limitation / dual-use: the same techniques may be repurposed to "
    "*strengthen* adversarial attacks or modulate latent-space biases.** "
    "The authors acknowledge in the Impact Statement that the "
    "latent-space alignment techniques could potentially be misused "
    "to (a) train improved attack models, (b) amplify rather than "
    "mitigate biases, or (c) reduce model generalizability. This is a "
    "standard dual-use concern for safety-alignment techniques and is "
    "not unique to CRAFT [@Luo2026CRAFT, Impact Statement].",
    title="Limitation: dual-use potential -- same techniques may strengthen attacks or biases",
)

claim_lim_pca_visualization_evidence = claim(
    "**Limitation: the latent-separation observation (Fig. 2) is "
    "illustrated via 2D PCA; the full latent geometry may differ.** "
    "PCA [@Ivosev2008PCA] is a linear projection and may not capture "
    "the full structure of the high-dimensional latent space. The "
    "qualitative separation is shown; whether the safe/unsafe "
    "manifolds are truly distinct in higher dimensions, or whether "
    "the boundaries are smoother than PCA suggests, is not "
    "established in the paper. The downstream effect on CRAFT's "
    "design is small (the prototypes $\\mu_c$ are used in cosine-"
    "similarity rewards, not PCA-projected coordinates), but readers "
    "should not over-interpret the visual separation as a complete "
    "characterization of the latent space.",
    title="Limitation: 2D PCA may understate the complexity of the true latent geometry",
)

# ---------------------------------------------------------------------------
# Impact statement (claims about the work's positioning)
# ---------------------------------------------------------------------------

claim_impact_intent = claim(
    "**Impact statement (intent): CRAFT is intended strictly for "
    "defensive alignment and red-teaming, not for enabling new attack "
    "capabilities.** The paper frames the work as targeting SSA -- a "
    "harmful-information-leakage failure mode -- with the goal of "
    "improving robustness to jailbreak attacks. The authors note that "
    "the techniques may nonetheless be misused, and accept the "
    "responsibility to flag this dual-use concern "
    "[@Luo2026CRAFT, Impact Statement].",
    title="Impact: defensive intent (SSA mitigation), with explicit dual-use disclosure",
)

# ---------------------------------------------------------------------------
# Foil claims for contradictions
# ---------------------------------------------------------------------------

claim_foil_output_alignment_sufficient = claim(
    "**Foil position: output-level alignment is sufficient for "
    "jailbreak robustness in LRMs.** Under this position, methods such "
    "as RLHF [@Ouyang2022InstructGPT], DPO [@Rafailov2023DPO], and "
    "output-side preference optimization (e.g., IPO output side) are "
    "fully adequate to align large reasoning models against "
    "jailbreaks; SSA is either not a real phenomenon or is a "
    "downstream artifact that does not warrant special treatment. "
    "This is the de facto position implicit in any approach that "
    "targets only model outputs and not internal reasoning -- and the "
    "position CRAFT explicitly contradicts.",
    title="Foil: output-level alignment is sufficient for LRM jailbreak robustness",
)

claim_foil_grpo_alone_sufficient = claim(
    "**Foil position: vanilla GRPO with output-level safety reward "
    "alone produces robustly aligned LRM policies.** Under this "
    "position, including only $R_{txt}$ (or any output-only safety "
    "reward) in the GRPO total reward suffices to align a reasoning "
    "model: the policy will learn safe outputs, and the latent state "
    "will follow as a downstream consequence. CRAFT's Theorem 5.1 "
    "directly contradicts this -- without $R_{cons}$ in the total "
    "reward, the SSA-eliminating perturbation argument breaks down "
    "and locally-optimal policies *can* exhibit SSA "
    "[@Luo2026CRAFT, Sec. 5].",
    title="Foil: vanilla GRPO with output-only reward produces robustly aligned policies",
)

# ---------------------------------------------------------------------------
# Predictions for the central abduction
# ---------------------------------------------------------------------------

claim_pred_latent_explains = claim(
    "**Prediction (CRAFT's hypothesis): the hidden-representation "
    "alignment mechanism explains the empirical safety gain.** Under "
    "the latent-alignment hypothesis, CRAFT's safety gains over "
    "output-level methods like IPO and SafeKey are caused by the "
    "explicit constraints over hidden states ($\\mathcal{L}_{proto}, "
    "\\mathcal{L}_{inst}, \\mathcal{L}_{cal}, R_{ls}, R_{cons}$). "
    "Predicted observable: cross-model consistency of the gain on a "
    "fixed compute budget, plus catastrophic degradation when LCLR or "
    "$R_{cons}$ is removed.",
    title="Hypothesis prediction: latent-space alignment is the mechanism behind CRAFT's gain",
)

claim_pred_alt_compute = claim(
    "**Alternative-prediction (compute / data alternative): CRAFT's "
    "gains are explained by additional compute, more SFT-style data, "
    "or better prompt engineering rather than the hidden-space "
    "alignment mechanism.** Under this alternative, removing LCLR "
    "should not catastrophically hurt safety (since the bulk of the "
    "gain would come from compute / data); cross-model consistency "
    "would not be expected (compute / data effects vary with "
    "model-specific tuning); and the per-component ablations should "
    "be roughly proportional to compute consumption.",
    title="Alternative prediction: compute / data / prompts (not latent alignment) explain CRAFT's gain",
)

claim_obs_cross_model_plus_ablations = claim(
    "**Observation discriminating between hypothesis and alternative:** "
    "CRAFT achieves *consistent* safety gains across both "
    "DeepSeek-R1-Distill-Llama-8B and Qwen3-4B-Thinking on a fixed "
    "compute budget, *and* the per-component ablation shows "
    "catastrophic degradation when LCLR is removed (avg score "
    "0.082 -> 0.423 = +34.1% absolute, +416% relative). The "
    "compute / data alternative cannot explain why removing one "
    "specific algorithmic component (the latent-space contrastive "
    "structure) collapses the entire gain -- this is the signature of "
    "the latent-alignment mechanism doing the work, not the compute "
    "[@Luo2026CRAFT, Tables 1, 2, 3].",
    title="Observation: cross-model consistency + catastrophic LCLR-ablation discriminate vs compute alt",
)

__all__ = [
    "claim_synthesis_main",
    "claim_future_adaptive_signals",
    "claim_lim_two_models",
    "claim_lim_training_budget",
    "claim_lim_fixed_evaluator",
    "claim_lim_misuse_potential",
    "claim_lim_pca_visualization_evidence",
    "claim_impact_intent",
    "claim_foil_output_alignment_sufficient",
    "claim_foil_grpo_alone_sufficient",
    "claim_pred_latent_explains",
    "claim_pred_alt_compute",
    "claim_obs_cross_model_plus_ablations",
]
