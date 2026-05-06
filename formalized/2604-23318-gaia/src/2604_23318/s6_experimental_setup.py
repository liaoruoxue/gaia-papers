"""Section 5.2: Experimental setup -- backbones, datasets, evaluation, baselines.

Section 5.2 of [@Chen2026SHEAR]. Defines the configuration shared by
the main results (Section 5.3) and ablations (Section 5.4-5.6).

Backbones:
  Math: Qwen2.5-Math-7B, Qwen2.5-14B-Base, Llama3.1-8B-Instruct
  Code: Qwen2.5-Coder-7B, Qwen2.5-14B-Base, Llama3.1-8B-Instruct

Training:
  Math RL on MATH (8.5K problems)
  Code RL on Eurus-RL-Code (25K samples)

Evaluation (math): AIME24 avg@32, AIME25 avg@32, AMC23 avg@8,
                   MATH500 avg@1, OlympiadBench avg@1, T=0.1, top-p=1.0.
Evaluation (code): HumanEval/+, MBPP/+, LiveCodeBench v6 -- all avg@4.

Checkpoint selection: every 5 training steps, take the highest
benchmark-averaged score over all checkpoints, report mean +/- std
across 3 random seeds. Math reports 3 seeds; code reports single run
in main table.

Baselines: GRPO; Entropy adv. [@Cheng2025EntropyAdv]; PURE
[@Cheng2025PURE]; PRM(Reshape adv.) using Qwen2.5-Math-PRM-7B
[@Zhang2025QwenPRM] (math only).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Backbones + training datasets
# ---------------------------------------------------------------------------

setup_backbones = setting(
    "**Backbones (Section 5.2).** Four backbones from two model "
    "families: Qwen2.5-Math-7B, Qwen2.5-Coder-7B, Qwen2.5-14B-Base "
    "[@Qwen2024Qwen25], and Llama3.1-8B-Instruct [@Grattafiori2024Llama3]. "
    "For mathematical reasoning the paper trains Qwen2.5-Math-7B, "
    "Qwen2.5-14B-Base, and Llama3.1-8B-Instruct. For code generation "
    "the paper trains Qwen2.5-Coder-7B, Qwen2.5-14B-Base, and "
    "Llama3.1-8B-Instruct. The two task settings are trained "
    "*independently*.",
    title="Setup: 3 math backbones + 3 code backbones, trained independently",
)

setup_training_datasets = setting(
    "**Training datasets.** Math: RL training on the MATH dataset "
    "[@Hendrycks2021MATH] following [@Liu2025R1Zero]; MATH contains "
    "8.5K problems spanning algebra, geometry, counting, probability, "
    "number theory, etc. Code: RL training on Eurus-RL-Code "
    "[@Cui2025PRIME] following [@Yang2026GeneralizedDistillation]; "
    "Eurus-RL-Code contains 25K samples. Detailed training settings "
    "in Appendix J: batch size 512, learning rate $1 \\times 10^{-6}$, "
    "clip range $[0.2, 0.28]$, response length up to 3K tokens, mini-"
    "batch size 32, training temperature 1.0, evaluation temperature "
    "0.1, $G = 8$ rollouts/prompt, KL coefficient 0, entropy loss 0.",
    title="Setup: MATH (8.5K) + Eurus-RL-Code (25K); detailed RL hyperparameters",
)

# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

setup_math_eval = setting(
    "**Math evaluation (5 benchmarks).** AIME24 [@AIMO2024AIME24], "
    "AIME25 [@OpenCompass2025AIME25], AMC23 [@MathAI2023AMC23], "
    "MATH500 [@Hendrycks2021MATH], OlympiadBench [@He2024OlympiadBench]. "
    "These span high-school competition (AMC23, MATH500) to olympiad-"
    "level (AIME24/25, OlympiadBench). The paper reports avg@32 on "
    "AIME24/AIME25 (small benchmarks -> averaging stabilises), avg@8 "
    "on AMC23, and avg@1 on MATH500/OlympiadBench (large benchmarks). "
    "avg@$k$ [@Wang2025HighEntropyTokens; @Yang2025DCPO] is the "
    "average correctness over $k$ independently sampled completions "
    "per problem under temperature sampling ($T = 0.1$, top-$p = 1.0$).",
    title="Setup: math eval on 5 benchmarks (AIME24, AIME25, AMC23, MATH500, OlympiadBench)",
)

setup_code_eval = setting(
    "**Code evaluation (5 benchmarks).** HumanEval, HumanEval+, MBPP, "
    "MBPP+ [@Liu2023HumanEvalPlus], LiveCodeBench v6 (Feb 2025-May "
    "2025) [@Jain2024LiveCodeBench]. HumanEval+ and MBPP+ extend the "
    "original test suites with substantially more unit tests "
    "(stricter functional correctness, fewer false positives). "
    "LiveCodeBench probes generalization on contamination-free "
    "problems released *after* the base model's training cutoff. "
    "All five benchmarks reported as avg@4.",
    title="Setup: code eval on 5 benchmarks (HumanEval, HumanEval+, MBPP, MBPP+, LiveCodeBench v6)",
)

setup_checkpoint_selection = setting(
    "**Checkpoint selection (uniform across methods).** Aligning "
    "with [@Zhang2025CritiqueGRPO; @Zhao2026SelfDistilledReasoner], "
    "the paper assesses each run every 5 training steps and applies "
    "the *same* benchmark-based selection protocol to *all* compared "
    "methods. For math, three random seeds; for each seed the highest "
    "benchmark-averaged score across the five math benchmarks over "
    "all evaluated checkpoints is recorded. The reported number is "
    "the mean +/- std of this best-observed score across seeds. For "
    "code, the analogous best-observed average across the five code "
    "benchmarks. This protocol measures *best-observed* performance "
    "under a *uniform model-selection rule* shared by all methods.",
    title="Setup: every-5-steps checkpoint selection, best-observed mean +/- std across 3 seeds (math); uniform across methods",
)

# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

setup_baselines = setting(
    "**Three baseline categories.** (1) Base RLVR algorithm: GRPO "
    "[@Shao2024GRPO], the canonical multi-sample policy-gradient "
    "method and backbone of many reasoning RL pipelines. (2) "
    "Intrinsic-signal-guided credit assignment: Entropy Advantage "
    "Reshaping [@Cheng2025EntropyAdv], a non-PRM approach that "
    "reshapes token-level advantages using entropy signals from the "
    "policy model itself. (3) PRM-based credit assignment: PURE "
    "[@Cheng2025PURE] (process reward models for reasoning + reward-"
    "hacking mitigation) and PRM(Reshape adv.) (GRPO + backward-"
    "filled PRM signals for finer-grained token-level credit). "
    "PRM-based baselines are evaluated only on math, using "
    "Qwen2.5-Math-PRM-7B [@Zhang2025QwenPRM] as the process reward "
    "model.",
    title="Setup: baselines = GRPO + Entropy adv. + PURE + PRM(Reshape adv.) [math only]",
)

# ---------------------------------------------------------------------------
# Methodological framing claims (used for inductions later)
# ---------------------------------------------------------------------------

claim_diversity_of_evaluation = claim(
    "**Evaluation spans heterogeneous models, tasks, and difficulty "
    "levels.** Three model families (Qwen2.5-Math/Coder/14B and "
    "Llama3.1) at three parameter scales (7B, 8B, 14B); two task "
    "modalities (math reasoning, code generation); difficulty range "
    "from high-school competition (AMC23, MATH500) to olympiad "
    "(AIME, OlympiadBench) and from short snippets (HumanEval, MBPP) "
    "to long contamination-free problems (LiveCodeBench). This "
    "diversity is the precondition for induction-over-(model, "
    "benchmark) claims (Section 5.3): if SHEAR consistently improves "
    "across heterogeneous backbones and tasks, the cross-setup "
    "induction is well-supported.",
    title="Setup: 3 backbones x 2 modalities x 5+5 benchmarks supports cross-setup induction",
)

claim_strong_baselines = claim(
    "**Baselines are strong, not strawmen.** Vanilla GRPO is the "
    "current default RLVR algorithm; Entropy adv. is the most "
    "conceptually-related token-level reweighting baseline (also "
    "self-supervised); PURE and PRM(Reshape adv.) use a *7B-scale* "
    "process reward model (Qwen2.5-Math-PRM-7B [@Zhang2025QwenPRM]) "
    "trained on step-level supervision -- the strongest available "
    "PRM family. Every baseline is run under the *same checkpoint-"
    "selection protocol* and the same training infrastructure. SHEAR's "
    "comparisons are therefore against the strongest available "
    "alternatives, not weakened versions.",
    title="Setup: baselines (GRPO, Entropy adv., PURE, PRM 7B reshape) are competitive, not strawmen",
)

__all__ = [
    "setup_backbones",
    "setup_training_datasets",
    "setup_math_eval",
    "setup_code_eval",
    "setup_checkpoint_selection",
    "setup_baselines",
    "claim_diversity_of_evaluation",
    "claim_strong_baselines",
]
