"""Motivation: superficial safety alignment in large reasoning models, and the
case for hidden-representation alignment.

Section 1 (Introduction) and abstract of Luo et al. (2026)
[@Luo2026CRAFT]. Large reasoning models (LRMs) such as DeepSeek-R1
[@Guo2025DeepSeekR1], the Qwen3 series [@Yang2025Qwen3], OpenAI o1
[@Jaech2024OpenAIo1], and GPT-4o [@Hurst2024GPT4o] often exhibit a failure
mode the authors call **superficial safety alignment (SSA)**: even when their
final response is a safe refusal, the model's internal chain-of-thought
reasoning trace still leaks harmful content. Standard alignment pipelines
such as RLHF [@Ouyang2022InstructGPT; @Dai2024SafeRLHF], DPO
[@Rafailov2023DPO], and SFT operate at the *output* level and therefore do
not constrain the latent reasoning trajectory; SSA persists.

The paper proposes **CRAFT**, a red-teaming alignment framework that
**aligns the latent space of reasoning traces** -- not just the final output
-- using a combination of contrastive representation learning and
reinforcement learning over hidden states.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Background settings: the regime CRAFT targets
# ---------------------------------------------------------------------------

setup_lrm_regime = setting(
    "**Large reasoning models (LRMs) regime.** The paper targets large "
    "language models post-trained to produce explicit chain-of-thought "
    "(CoT) [@Wei2022CoT] reasoning traces -- so-called large reasoning "
    "models (LRMs) -- such as DeepSeek-R1 [@Guo2025DeepSeekR1], the "
    "Qwen3 series [@Yang2025Qwen3], OpenAI o1 [@Jaech2024OpenAIo1], "
    "Phi-4-Reasoning [@Abdin2025Phi4], and GPT-4o [@Hurst2024GPT4o]. "
    "These models autoregressively predict next tokens conditioned on "
    "prior context and emit a reasoning trace tau = (y_1, ..., y_T) "
    "before the final answer.",
    title="Setup: large reasoning models that emit explicit CoT reasoning traces",
)

setup_jailbreak_threat_model = setting(
    "**Jailbreak threat model.** A *jailbreak attack* supplies an "
    "adversarial prompt -- typically a plain harmful query embedded in a "
    "social-engineering wrapper, or a prompt optimized by attacks such as "
    "GPTFuzzer [@Yu2024aGPTFuzzer], AutoDAN [@Liu2023AutoDAN], PAP "
    "[@Zeng2024PAP], or PAIR [@Chao2025PAIR] -- with the goal of "
    "eliciting harmful content from an aligned model. A defense is "
    "successful if the model produces a safe refusal, ideally also "
    "without leaking harmful content in its intermediate reasoning trace.",
    title="Setup: jailbreak attack threat model and defense desideratum",
)

setup_alignment_baselines = setting(
    "**Standard output-level alignment baselines.** Widely deployed "
    "alignment pipelines including RLHF [@Ouyang2022InstructGPT; "
    "@Dai2024SafeRLHF], DPO [@Rafailov2023DPO], and supervised "
    "fine-tuning (SFT) optimize objectives defined over the model's "
    "*output distribution*: they compare model outputs to preference "
    "rankings, demonstrations, or reward signals derived from generated "
    "text. They do not impose explicit constraints on intermediate "
    "hidden representations or reasoning traces.",
    title="Setup: existing output-level alignment baselines (RLHF, DPO, SFT)",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Can a red-teaming alignment framework that operates over the "
    "*hidden representations* of reasoning traces -- rather than only "
    "over output tokens -- eliminate superficial safety alignment "
    "(unsafe internal reasoning despite safe final outputs) and improve "
    "robustness against jailbreak attacks while preserving general "
    "reasoning capability?",
    title="Central question: does latent-space reasoning alignment eliminate SSA?",
)

# ---------------------------------------------------------------------------
# Phenomenon: superficial safety alignment (SSA)
# ---------------------------------------------------------------------------

claim_ssa_phenomenon = claim(
    "**Superficial safety alignment (SSA) is an empirically observed "
    "failure mode of LRMs.** Even when an LRM is red-teaming aligned via "
    "standard pipelines (RLHF [@Dai2024SafeRLHF], DPO [@Rafailov2023DPO], "
    "or SFT) similar to the alignment of LLaMA3-Instruct "
    "[@Grattafiori2024Llama3] or Gemma-IT [@GemmaTeam2024], the model can "
    "still exhibit *unsafe internal reasoning* despite emitting a *safe* "
    "final response. Concretely, the chain-of-thought trace contains "
    "harmful expressions (slurs, discriminatory framings, harmful "
    "advice) even though the final answer is a refusal. This phenomenon "
    "is documented across multiple recent works "
    "[@Zhou2025aHiddenRisks; @Li2025aReasoningShield; @Zhang2025bIPO].",
    title="Phenomenon: SSA is an empirically attested failure of output-level alignment",
)

claim_output_level_insufficient = claim(
    "**Output-level alignment is insufficient to prevent SSA.** Because "
    "RLHF [@Ouyang2022InstructGPT; @Dai2024SafeRLHF], DPO "
    "[@Rafailov2023DPO], and SFT objectives are defined over the model's "
    "output distribution rather than over its internal reasoning "
    "trajectories, models trained with these methods can exhibit safe "
    "refusal at the output level while their internal reasoning remains "
    "adversarially aligned with the harmful prompt. Output-level "
    "constraints leave the latent reasoning subspace unconstrained.",
    title="Diagnosis: output-only objectives do not constrain internal reasoning",
)

claim_lrm_safety_underexplored = claim(
    "**The safety of LRMs is comparatively underexplored relative to "
    "their reasoning ability.** While LRMs achieve strong performance on "
    "mathematical reasoning [@Shao2024DeepSeekMath], code generation, "
    "and embodied reasoning tasks, recent work shows that long reasoning "
    "traces also expand the *attack surface*: longer chains-of-thought "
    "can be exploited or adversarially optimized, and improving raw "
    "reasoning ability without explicit reasoning-process control "
    "actually increases safety exposure [@Jiang2025bSafeChain; "
    "@Zhou2025aHiddenRisks; @Wang2025aSurveySafety].",
    title="Diagnosis: stronger reasoning expands jailbreak attack surface",
)

# ---------------------------------------------------------------------------
# CRAFT: the proposed method (headline contributions)
# ---------------------------------------------------------------------------

claim_craft_proposal = claim(
    "**Headline proposal: CRAFT, a red-teaming alignment framework that "
    "aligns reasoning at the latent level.** CRAFT is a reasoning-based "
    "alignment method that integrates *contrastive representation "
    "learning* with *reinforcement learning over latent representations* "
    "to mitigate superficial safety alignment and improve robustness "
    "against jailbreak attacks. The framework structures the latent "
    "space of reasoning traces via contrastive objectives and employs a "
    "latent-textual consistency reward to jointly align intermediate "
    "reasoning states *and* final responses, preventing unsafe internal "
    "reasoning from persisting behind superficially safe outputs "
    "[@Luo2026CRAFT, Sec. 1].",
    title="Headline: CRAFT integrates contrastive learning + RL over hidden representations",
)

claim_contribution_framework = claim(
    "**Contribution 1 (framework): CRAFT introduces a latent-space "
    "red-teaming alignment framework for SSA.** The framework combines "
    "contrastive learning over hidden representations of reasoning "
    "traces with a consistency-aware GRPO [@Ramesh2024GRPO; "
    "@Shao2024DeepSeekMath] objective that jointly aligns reasoning "
    "traces and final responses [@Luo2026CRAFT, Sec. 1].",
    title="Contribution: latent-space red-teaming alignment framework combining contrastive + GRPO",
)

claim_contribution_theory = claim(
    "**Contribution 2 (theory): incorporating a latent-textual "
    "consistency reward into GRPO eliminates superficially aligned "
    "policies by ruling them out as local optima.** The paper proves "
    "(Theorem 5.1) that under continuity and local-controllability "
    "assumptions on the projection / safety heads and the GRPO "
    "local-optimality assumption, any policy that satisfies "
    "p_y approximately 1 (safe output) but |p_z - p_y| >= delta (unsafe "
    "latent state) is *not* a local optimum of the total reward; a "
    "perturbation that reduces |p_z - p_y| while preserving the output "
    "distribution strictly increases the reward [@Luo2026CRAFT, Sec. 5; "
    "Theorem 5.1].",
    title="Contribution: theorem -- latent-textual consistency rules out SSA as local optima",
)

claim_contribution_method = claim(
    "**Contribution 3 (methodology): CRAFT designs a contrastive latent "
    "representation learning scheme + a reinforcement-learning objective "
    "over hidden states that enforces safety alignment at both "
    "intermediate-reasoning and output levels.** Concretely, CRAFT "
    "comprises two components -- Latent Contrastive Learning for "
    "Reasoning (LCLR) which structures the latent space via "
    "prototype-based triplet loss + InfoNCE [@Chen2020SimCLR] + "
    "calibration, and Reinforcement over Reasoning Latents (R2L) which "
    "applies GRPO with a latent-semantic reward, a textual safety "
    "reward, and a latent-textual consistency reward "
    "[@Luo2026CRAFT, Sec. 4].",
    title="Contribution: explicit two-stage design (LCLR + R2L) over hidden states",
)

claim_contribution_empirical = claim(
    "**Contribution 4 (empirical headline): CRAFT consistently improves "
    "jailbreak robustness across multiple benchmarks and reasoning "
    "models while preserving reasoning performance.** Specifically, "
    "compared to base models, CRAFT achieves an average **79.0%** "
    "improvement in reasoning-level safety, an average **87.7%** "
    "improvement in final-response safety, and a **4.7%** improvement "
    "in mean reasoning performance across mathematical and code "
    "benchmarks. These results are obtained across two strong reasoning "
    "models (DeepSeek-R1-Distill-Llama-8B [@Guo2025DeepSeekR1] and "
    "Qwen3-4B-Thinking [@Yang2025Qwen3]) on jailbreak benchmarks "
    "JailbreakBench [@Chao2024JailbreakBench] and StrongReject "
    "[@Souly2024StrongReject], and on reasoning benchmarks AIME 2024 "
    "[@MAA2024AIME], MATH-500 [@Lightman2024PRM], LiveCodeBench "
    "[@Jain2025LiveCodeBench], and Minerva [@Dyer2022Minerva] "
    "[@Luo2026CRAFT, Abstract; Sec. 1].",
    title="Headline empirical: 79.0% reasoning-safety / 87.7% response-safety / 4.7% reasoning gain",
)

# ---------------------------------------------------------------------------
# Latent-separation observation that motivates the design
# ---------------------------------------------------------------------------

claim_latent_separation_observation = claim(
    "**Empirical observation that motivates the design: safe and unsafe "
    "reasoning traces occupy *geometrically separated* regions of the "
    "latent space.** Using PCA [@Ivosev2008PCA] projections of the "
    "final-token hidden state for prompt-response pairs from R2D-R1 "
    "[@Zhu2025R2D] under unethical jailbreak prompts, the paper shows "
    "that on both DeepSeek-R1-Distill-Llama-8B [@Guo2025DeepSeekR1] and "
    "Qwen3-4B-Thinking [@Yang2025Qwen3], (i) safe traces cluster in one "
    "region, (ii) unsafe traces cluster in a clearly separated region, "
    "and (iii) 'rethink' traces (with indeterminate safety) "
    "concentrate at the boundary, indicating *transitional* reasoning "
    "states between aligned and violating behaviors. The model-agnostic "
    "nature of this separation is what makes latent-space alignment "
    "viable [@Luo2026CRAFT, Sec. 3; Fig. 2].",
    title="Observation: safe / rethink / unsafe traces are geometrically separable in latent space",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Figure 2",
        "caption": "Fig. 2: PCA projections of final-token hidden states from DeepSeek-R1-Distill-Llama-8B (left) and Qwen3-4B-Thinking (right) showing safe / unsafe / rethink clusters with model-agnostic structure.",
    },
)

# ---------------------------------------------------------------------------
# Implications
# ---------------------------------------------------------------------------

claim_implication_latent_alignment = claim(
    "**Implication: hidden-representation alignment is a viable and "
    "necessary direction for jailbreak defense in LRMs.** Because (i) "
    "SSA is an empirically attested failure of output-level alignment, "
    "(ii) safe and unsafe reasoning traces are geometrically separable "
    "in latent space, and (iii) the latent-textual consistency objective "
    "provably eliminates SSA at local optima, the paper concludes that "
    "alignment objectives operating over hidden states are both "
    "*feasible* and *needed* to address SSA -- output-level alignment "
    "alone cannot reach the same equilibrium [@Luo2026CRAFT, Sec. 7].",
    title="Implication: latent-space alignment is feasible and necessary for SSA mitigation",
)

__all__ = [
    "setup_lrm_regime",
    "setup_jailbreak_threat_model",
    "setup_alignment_baselines",
    "q_central",
    "claim_ssa_phenomenon",
    "claim_output_level_insufficient",
    "claim_lrm_safety_underexplored",
    "claim_craft_proposal",
    "claim_contribution_framework",
    "claim_contribution_theory",
    "claim_contribution_method",
    "claim_contribution_empirical",
    "claim_latent_separation_observation",
    "claim_implication_latent_alignment",
]
