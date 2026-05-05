"""Section 3 (Experimental Setup): formal definition of pipelines, evaluation, and reproduction protocol.

The paper establishes a controlled comparison: same base model, dataset, and
evaluation protocol across SFT, SFT-then-RL, and the five mixed-policy
methods. This module captures the formal setups (definitions are settings;
methodological assertions about applicability are claims).

Source: [@Limozin2026SFTthenRL, Sec. 3].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Pipeline definitions (settings)
# ---------------------------------------------------------------------------

setup_sft_then_rl_pipeline = setting(
    "**SFT-then-RL pipeline definition.** The two-stage pipeline (i) first "
    "fine-tunes the base model on expert chain-of-thought traces "
    "[@Wei2022CoT] for a fixed number of epochs (3 in the paper) using "
    "the AdamW optimizer with batch size 64 and learning rate 5x10^-5 "
    "(cosine schedule, 10% warmup, minimum ratio 0.1, beta_1 = 0.9, "
    "beta_2 = 0.999, weight decay 0.01); then (ii) runs Group Relative "
    "Policy Optimization (GRPO) RL for 500 steps using rollout batch "
    "size 128, 8 rollouts per prompt, mini-batch size 64, constant "
    "learning rate 1x10^-6, entropy coefficient 0, temperature 1.0, "
    "max response length 8192 tokens. Following recent works "
    "[@LUFFY; @DAPO; @R1ZeroCritical] the GRPO variant uses asymmetric "
    "clipping (epsilon_low = 0.2, epsilon_high = 0.28), token-level "
    "loss [@DAPO], and removes the KL term and length / standard-error "
    "normalization [@R1ZeroCritical] [@Limozin2026SFTthenRL, Appendix A].",
    title="Setup: SFT-then-RL pipeline (Adam SFT + GRPO RL with explicit hyperparameters)",
)

setup_grpo_500_steps = setting(
    "**Standard RL run length: 500 GRPO steps.** Every method evaluated "
    "trains for 500 GRPO steps on the OpenR1-Math-46k-8192 dataset "
    "[@OpenR1] with 8 rollouts per prompt. The 500-step convention is "
    "shared across LUFFY, ReLIFT, SRFT, Prefix-RFT, and HPT for "
    "comparability [@Limozin2026SFTthenRL, Sec. 3].",
    title="Setup: 500-step convention for the RL phase",
)

setup_truncated_rl_50 = setting(
    "**Truncated RL variant: 50 GRPO steps with elevated learning rate.** "
    "The truncated SFT-then-RL variant uses the same SFT stage but "
    "shortens the RL stage from 500 steps to 50 steps and raises the "
    "constant RL learning rate from 1x10^-6 to 5x10^-6 (a 10x ramp); "
    "all other RL hyperparameters are unchanged. This is a 10x "
    "reduction in RL compute relative to the default schedule "
    "[@Limozin2026SFTthenRL, Sec. 4.3].",
    title="Setup: 50-step truncated RL variant (10x fewer steps, 5x higher LR)",
)

setup_evaluation_benchmarks = setting(
    "**Evaluation benchmarks.** In-distribution (ID): AIME24, AIME25, "
    "AMC, MATH-500 [@MATH500], Minerva [@Minerva], OlympiadBench "
    "[@OlympiadBench]. Out-of-distribution (OOD): ARC-Challenge "
    "[@ARCc], GPQA-Diamond [@GPQA], MMLU-Pro [@MMLUPro]. For benchmarks "
    "with limited sample sizes (AIME24, AIME25, AMC) avg@32 is reported; "
    "for the rest, pass@1. Multiple-choice option order is randomly "
    "shuffled to mitigate information leakage. Evaluation temperature "
    "0.6, max response length 8192 tokens, Math-Verify as the verifier "
    "[@Limozin2026SFTthenRL, Sec. 3].",
    title="Setup: ID and OOD evaluation benchmarks with avg@32 / pass@1 protocol",
)

setup_seed_protocol = setting(
    "**Seed protocol for the corrected baselines.** For each method "
    "involving SFT, three independent training runs with different "
    "random seeds are performed; for SFT-then-RL pipelines, both the "
    "SFT and the subsequent RL stages use different seeds across runs, "
    "so each of the three runs is independent end-to-end. Mean and "
    "standard deviation across the three seeds are reported. For the "
    "LUFFY / ReLIFT reproduction runs, single-seed results are reported "
    "due to compute cost; the performance gaps substantially exceed the "
    "variance observed across the 3-seed baselines "
    "[@Limozin2026SFTthenRL, Sec. 3].",
    title="Setup: 3-seed reporting for corrected baselines; 1-seed for reproductions",
)

setup_compute_setup = setting(
    "**Compute setup.** All experiments are conducted on 4 nodes of 4 "
    "NVIDIA GH200 GPUs (16 GPUs total). Training uses verl [@verl] "
    "(except the SFT bug reproduction in Table 2 which uses OpenRLHF "
    "[@OpenRLHF] with DeepSpeed [@DeepSpeed]). Distributed training "
    "uses PyTorch FSDP [@FSDP]; rollout generation uses vLLM [@vLLM]. "
    "The bugs were identified in DeepSpeed v0.18.9 and OpenRLHF "
    "v0.9.10 [@Limozin2026SFTthenRL, Appendix A].",
    title="Setup: 4 x 4 GH200 nodes; verl training stack; FSDP + vLLM",
)

# ---------------------------------------------------------------------------
# Methodological setup claims (these can be questioned)
# ---------------------------------------------------------------------------

claim_reproduction_design = claim(
    "**Reproduction design isolates each bug's contribution.** Four SFT "
    "variants are trained using OpenRLHF, progressively fixing the loss "
    "aggregation bug, the CPU-offloaded optimizer bug, or both, and "
    "compared against an independently implemented verl baseline on a "
    "representative subset of benchmarks (Table 2). For this "
    "reproduction a single node is used rather than the 4 nodes of the "
    "main technical setup, since the number of nodes affects the "
    "reported gradient norm. This design isolates each bug's "
    "contribution to the SFT-vs-mixed-policy gap "
    "[@Limozin2026SFTthenRL, Sec. 3].",
    title="Method: progressive bug-fix reproduction isolates each bug's contribution",
)

claim_luffy_relift_reimpl = claim(
    "**LUFFY and ReLIFT are reimplemented in verl using their original "
    "hyperparameters.** Because verl does not use DeepSpeed, the "
    "CPU-offload optimizer bug affects only the standalone SFT "
    "baselines those methods compare against, not the methods "
    "themselves -- this means the optimizer bug deflates the baseline "
    "side of every comparison. The loss aggregation bug "
    "(Section 2.2 / s5 module) is patched in LUFFY's RL component and "
    "in ReLIFT's SFT and RL stage losses to keep the comparison fair "
    "[@Limozin2026SFTthenRL, Sec. 3].",
    title="Method: LUFFY/ReLIFT reimplemented in verl with loss-aggregation fix applied to their training loops",
)

claim_chat_template_unified = claim(
    "**Unified chat template across model families.** Prior works "
    "[@LUFFY; @ReLIFT; @SRFT; @PrefixRFT; @HPT; @MIFO; @RED] use a "
    "*simplified* template for Llama-3.1-8B, reporting that it cannot "
    "follow the full Qwen system prompt [@LUFFY]. With a correctly "
    "implemented SFT stage, Llama-3.1-8B follows the full prompt without "
    "issue, so the same template is used for both model families. This "
    "is consistent with the hypothesis that the inability to follow the "
    "system prompt was a *symptom* of undertrained SFT rather than an "
    "intrinsic model limitation [@Limozin2026SFTthenRL, Sec. 3; "
    "Appendix E].",
    title="Method: unified chat template (template-mismatch was a symptom of buggy SFT, not a model limit)",
)

# ---------------------------------------------------------------------------
# FLOPs accounting setup (used to compute compute-efficiency claims)
# ---------------------------------------------------------------------------

setup_flops_accounting = setting(
    "**FLOPs accounting model.** Following [@Limozin2026SFTthenRL, "
    "Appendix B] and prior scaling-law work, a forward pass through a "
    "model with N parameters on D tokens costs approximately 2ND FLOPs, "
    "and a backward pass costs roughly 4ND; SFT therefore requires 6ND "
    "FLOPs per sample. For RL: each on-policy sequence is generated "
    "once by the inference engine (2ND FLOPs) and re-processed by the "
    "training engine for the policy gradient update (1 forward + 1 "
    "backward = 6ND FLOPs), totalling 8ND FLOPs per on-policy rollout. "
    "Off-policy expert traces incur only the training cost (6ND) since "
    "no generation is required. For all methods N = 7x10^9 "
    "(Qwen2.5-Math-7B [@Qwen25Math]) and the average off-policy "
    "demonstration response length is D_data = 4,200 tokens.",
    title="Setup: FLOPs accounting model (6ND for SFT/training; 8ND total per RL rollout)",
)

__all__ = [
    "setup_sft_then_rl_pipeline",
    "setup_grpo_500_steps",
    "setup_truncated_rl_50",
    "setup_evaluation_benchmarks",
    "setup_seed_protocol",
    "setup_compute_setup",
    "claim_reproduction_design",
    "claim_luffy_relift_reimpl",
    "claim_chat_template_unified",
    "setup_flops_accounting",
]
