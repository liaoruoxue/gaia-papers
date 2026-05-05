"""Motivation: are mixed-policy LLM-reasoning gains real, or do they ride on a buggy SFT baseline?

Section 1 (Introduction) and abstract of Limozin et al. 2026 [@Limozin2026SFTthenRL].
The paper diagnoses a structural problem in the recent post-training literature
for LLM reasoning: a growing class of *mixed-policy* methods (which interleave or
blend SFT and RL signals during training) report improvements over the canonical
two-stage SFT-then-RL pipeline. The paper argues that these improvements are
artifacts of two silent bugs in widely-used SFT frameworks (DeepSpeed and
OpenRLHF) which deflate the standalone SFT baselines those methods compare
against. Once the bugs are fixed, a properly trained SFT-then-RL pipeline matches
or exceeds every published mixed-policy method on math reasoning benchmarks.

Reference implementation: [@SFTthenRLCode] (https://github.com/alek6kun/sft_then_rl).
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setting (the regime the paper targets)
# ---------------------------------------------------------------------------

setup_llm_reasoning_regime = setting(
    "**Post-training for LLM reasoning regime.** The paper targets large "
    "language models (LLMs) being post-trained to perform mathematical and "
    "scientific reasoning at competition-level difficulty. The dominant "
    "post-training paradigm popularized by OpenAI's o1 series [@OpenAIo1], "
    "DeepSeek-R1 [@DeepSeekR1], and Kimi k1.5 [@Kimi15] is a two-stage "
    "pipeline: (i) **supervised fine-tuning (SFT)** on expert-generated "
    "chain-of-thought (CoT) demonstrations [@Wei2022CoT] to equip the model "
    "with domain knowledge and output formatting, followed by (ii) "
    "**reinforcement learning from verifiable rewards (RLVR)** which "
    "sharpens the policy toward higher-reward reasoning trajectories.",
    title="Setup: SFT-then-RL is the canonical post-training pipeline for LLM reasoning",
)

setup_mixed_policy_definition = setting(
    "**Mixed-policy methods.** A *mixed-policy method* is a post-training "
    "approach that interleaves or blends supervised (off-policy expert "
    "demonstrations) and reinforcement (on-policy rollout) signals during "
    "the *same* training stage, rather than running SFT and RL "
    "sequentially. Examples include LUFFY [@LUFFY] (mixes off-policy "
    "expert traces into on-policy GRPO), ReLIFT [@ReLIFT] (alternates SFT "
    "and RL phases), SRFT [@SRFT] (jointly optimizes SFT and RL losses "
    "within each batch), Prefix-RFT [@PrefixRFT] (samples prefixes from "
    "expert solutions for on-policy continuation), and HPT [@HPT] "
    "(dynamically switches between SFT and GRPO based on rollout "
    "accuracy).",
    title="Setup: definition of mixed-policy methods (interleaving/blending SFT+RL signals)",
)

setup_evaluation_protocol = setting(
    "**Evaluation protocol used across the mixed-policy literature.** All "
    "the mixed-policy methods evaluated [@LUFFY; @ReLIFT; @SRFT; "
    "@PrefixRFT; @HPT] use the same family of mathematical reasoning "
    "benchmarks: AIME24, AIME25, AMC, MATH-500 [@MATH500], Minerva "
    "[@Minerva], and OlympiadBench (Olympiad) [@OlympiadBench]. For "
    "benchmarks with limited sample sizes (AIME24/25, AMC) avg@32 is "
    "reported; for the rest pass@1. Out-of-distribution (OOD) "
    "generalization is probed on ARC-Challenge [@ARCc], GPQA-Diamond "
    "[@GPQA], and MMLU-Pro [@MMLUPro]. The base models are "
    "Qwen2.5-Math-7B [@Qwen25Math] and Llama-3.1-8B [@Llama3].",
    title="Setup: shared math + OOD evaluation protocol across the mixed-policy literature",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Are the recent reported gains of mixed-policy LLM-reasoning methods "
    "over the SFT-then-RL pipeline real methodological advances, or are "
    "they artifacts of bugs in the SFT frameworks used to train the "
    "baselines they compare against?",
    title="Central question: are mixed-policy gains real, or baseline-deflation artifacts?",
)

# ---------------------------------------------------------------------------
# Diagnosis: the prevailing mixed-policy literature claim and its premise
# ---------------------------------------------------------------------------

claim_mixed_policy_gains_reported = claim(
    "**The mixed-policy LLM-reasoning literature reports consistent "
    "improvements over the standard SFT-then-RL pipeline.** A growing "
    "body of methods [@LUFFY; @ReLIFT; @SRFT; @PrefixRFT; @HPT; @MIFO; "
    "@RED; @UFT; @CHORD; @SuperRL; @SASR; @TemplateRL] reports "
    "state-of-the-art results on mathematical reasoning benchmarks, with "
    "many [@LUFFY; @ReLIFT; @SRFT; @PrefixRFT; @HPT] specifically "
    "claiming improvements over standalone SFT and SFT-then-RL "
    "baselines.",
    title="Diagnosis: published mixed-policy methods consistently report SOTA over SFT-then-RL",
)

claim_intuitive_motivation_for_mixing = claim(
    "**The intuitive motivation for mixed-policy training.** On-policy "
    "RL suffers from *sparse rewards* on hard problems where the model "
    "rarely generates a correct solution; SFT alone does not develop "
    "the model's own reasoning capacity. By combining on-policy rollouts "
    "with off-policy expert demonstrations, mixed-policy methods aim to "
    "leverage SFT's ability to learn from demonstrations beyond the "
    "model's initial capabilities together with RL's ability to refine "
    "and sharpen existing reasoning [@LUFFY; @ReLIFT].",
    title="Diagnosis: the prevailing rationale for mixing SFT + RL signals in one stage",
)

claim_baseline_suspicion = claim(
    "**This paper's central suspicion: the baselines used in the "
    "mixed-policy literature are silently deflated by framework bugs.** "
    "Numerous methods [@LUFFY; @ReLIFT; @SRFT; @PrefixRFT; @HPT] follow "
    "the SFT setup of Yan et al. [@LUFFY] which uses OpenRLHF "
    "[@OpenRLHF] with DeepSpeed [@DeepSpeed] for the SFT stage. The "
    "paper argues that bugs in these shared training frameworks weaken "
    "the standalone SFT baselines, so the apparent mixed-policy "
    "improvement may not reflect a methodological advance but rather a "
    "comparison against a deflated reference [@Limozin2026SFTthenRL, "
    "Sec. 1; Sec. 2].",
    title="Diagnosis: suspicion that mixed-policy gains ride on buggy SFT baselines",
)

# ---------------------------------------------------------------------------
# Headline contributions
# ---------------------------------------------------------------------------

claim_two_bug_thesis = claim(
    "**Headline thesis: two distinct SFT framework bugs explain the gap.** "
    "The paper identifies and fixes *two* SFT bugs that silently degrade "
    "standalone SFT performance: "
    "(a) a **CPU-offloaded optimizer bug in DeepSpeed** [@DeepSpeed] "
    "that silently drops intermediate micro-batches during gradient "
    "accumulation, affecting downstream frameworks including TRL "
    "[@TRL], OpenRLHF [@OpenRLHF], and Llama-Factory [@LlamaFactory]; "
    "(b) a **loss aggregation bug in OpenRLHF** [@OpenRLHF] that "
    "incorrectly weights per-mini-batch losses. Together these two bugs "
    "deflate SFT performance by up to 5.7 points on Qwen2.5-Math-7B "
    "[@Qwen25Math] [@Limozin2026SFTthenRL, Sec. 1].",
    title="Headline: two distinct SFT bugs together suppress baseline performance",
)

claim_optimizer_bug_dominant = claim(
    "**Quantitative attribution: the optimizer bug accounts for *most* "
    "of the SFT-vs-mixed-policy gap; the loss aggregation bug "
    "contributes a smaller additional effect.** Figure 1 (right) of the "
    "paper shows the progressive bug-fix waterfall on Qwen2.5-Math-7B: "
    "the buggy OpenRLHF baseline averages 48.3 across the evaluation "
    "subset; fixing only the loss aggregation bug yields 49.1 (+0.8); "
    "fixing only the CPU-offloaded optimizer bug yields 53.4 (+5.1); "
    "fixing both yields 54.0 (+5.7). The optimizer fix alone recovers "
    "nearly the entire gap; the loss aggregation fix contributes a "
    "smaller measurable improvement on top "
    "[@Limozin2026SFTthenRL, Fig. 1; Table 2].",
    title="Headline: optimizer bug dominates; loss aggregation bug is the smaller effect",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 1 (right)",
        "caption": "Fig. 1 right: SFT evaluation score as bugs are progressively fixed (48.3 to 49.1 to 53.4 to 54.0 average score across the AIME24/AIME25/AMC/MATH-500/Olympiad/MMLU-Pro subset).",
    },
)

claim_qwen_headline = claim(
    "**Headline empirical claim (Qwen2.5-Math-7B): once both bugs are "
    "corrected, SFT-then-RL exceeds every evaluated mixed-policy method "
    "by +3.8 points on in-distribution math benchmarks.** With "
    "Qwen2.5-Math-7B [@Qwen25Math] as the base model, the corrected "
    "SFT-then-RL pipeline (verl [@verl] implementation) achieves a "
    "57.0 in-distribution average over AIME24, AIME25, AMC, MATH-500, "
    "Minerva, and OlympiadBench [@MATH500; @Minerva; @OlympiadBench], "
    "exceeding the next-best mixed-policy method (SRFT [@SRFT] at "
    "53.2) by +3.8 points [@Limozin2026SFTthenRL, Table 1].",
    title="Headline: Qwen2.5-Math-7B SFT-then-RL beats best mixed-policy method by +3.8 ID points",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 1",
        "caption": "Table 1: Corrected baselines vs mixed-policy methods on Qwen2.5-Math-7B (ID + OOD).",
    },
)

claim_llama_headline = claim(
    "**Headline empirical claim (Llama-3.1-8B): the corrected SFT-then-RL "
    "pipeline outperforms every evaluated mixed-policy method by +22.2 "
    "points on math benchmarks.** With Llama-3.1-8B [@Llama3] as the "
    "base model, the corrected SFT-then-RL pipeline achieves 43.7 "
    "average score over AIME24/AMC/MATH-500/Minerva/Olympiad, exceeding "
    "the next-best published mixed-policy method (HPT [@HPT] at 21.5) "
    "by +22.2 points. The corrected SFT baseline alone reaches 33.9, "
    "already exceeding all mixed-policy results by +12.4 points "
    "[@Limozin2026SFTthenRL, Table 4].",
    title="Headline: Llama-3.1-8B SFT-then-RL beats best mixed-policy method by +22.2 points",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 4",
        "caption": "Table 4: Corrected baselines vs published mixed-policy methods on Llama-3.1-8B.",
    },
)

claim_compute_efficiency_headline = claim(
    "**Headline efficiency claim: even a truncated SFT-then-RL variant "
    "with just 50 RL steps outperforms mixed-policy methods on math "
    "benchmarks while using fewer FLOPs.** A truncated SFT-then-RL run "
    "with only 50 RL steps (10x fewer than the default 500) achieves "
    "55.6 ID average on Qwen2.5-Math-7B at 3.63x10^19 FLOPs, while "
    "LUFFY [@LUFFY] uses 6.65x10^19 FLOPs and ReLIFT [@ReLIFT] uses "
    "8.76x10^19 FLOPs and the truncated pipeline still surpasses the "
    "best mixed-policy ID score (53.2 for SRFT) by +2.4 points "
    "[@Limozin2026SFTthenRL, Table 5; Table 6].",
    title="Headline: 50-step SFT-then-RL outperforms mixed-policy methods at fewer FLOPs",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 5 / Table 6",
        "caption": "Tables 5 + 6: Faster RL on Qwen and FLOPs comparison across methods.",
    },
)

claim_implications = claim(
    "**Implication: silent SFT-pipeline bugs were sufficient to "
    "systematically deflate baselines across multiple independent "
    "studies, calling the published mixed-policy gains into question "
    "and motivating cross-framework validation as a methodological "
    "norm.** Because the bugs affect general-purpose SFT pipelines "
    "rather than mixed-policy code specifically, they could potentially "
    "invalidate empirical claims in other research areas that rely on "
    "the same affected frameworks (TRL, OpenRLHF, Llama-Factory). "
    "Cross-validation across independently implemented frameworks "
    "(verl [@verl] / FSDP [@FSDP] / DeepSpeed [@DeepSpeed]) is therefore "
    "essential to guard against systematic baseline deflation "
    "[@Limozin2026SFTthenRL, Sec. 6].",
    title="Implication: cross-framework validation is essential; bugs may affect other ML areas",
)

__all__ = [
    "setup_llm_reasoning_regime",
    "setup_mixed_policy_definition",
    "setup_evaluation_protocol",
    "q_central",
    "claim_mixed_policy_gains_reported",
    "claim_intuitive_motivation_for_mixing",
    "claim_baseline_suspicion",
    "claim_two_bug_thesis",
    "claim_optimizer_bug_dominant",
    "claim_qwen_headline",
    "claim_llama_headline",
    "claim_compute_efficiency_headline",
    "claim_implications",
]
