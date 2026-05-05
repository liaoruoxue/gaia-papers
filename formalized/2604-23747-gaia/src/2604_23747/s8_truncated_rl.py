"""Section 4.3 (Training Efficiency): the 50-RL-step truncated variant.

This module formalizes the compute-efficiency claim: a truncated SFT-then-RL
variant with just 50 RL steps still outperforms mixed-policy methods on math
benchmarks while using fewer FLOPs than LUFFY and ReLIFT.

Source: [@Limozin2026SFTthenRL, Sec. 4.3; Table 5; Table 6; Appendix B].
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Truncated 50-step performance (Table 5)
# ---------------------------------------------------------------------------

claim_truncated_id_results = claim(
    "**Truncated SFT-then-RL (50 RL steps) on Qwen2.5-Math-7B achieves "
    "55.6 +/- 0.5 ID average.** Per-benchmark: AIME24=37.1 +/- 2.7, "
    "AIME25=29.4 +/- 0.6, AMC=70.3 +/- 1.5, MATH-500=91.7 +/- 0.8, "
    "Minerva=44.1 +/- 0.0, Olympiad=61.3 +/- 0.9, ID avg = "
    "**55.6 +/- 0.5**. Compared to the full 500-step SFT-then-RL run "
    "at 57.0 +/- 0.3, the truncated run is only **1.4 points behind** "
    "[@Limozin2026SFTthenRL, Table 5].",
    title="Result: truncated 50-step SFT-then-RL = 55.6 ID (only -1.4 vs full 500-step)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 5",
        "caption": "Table 5: Faster RL on Qwen2.5-Math-7B; SFT-then-RL (50 steps) = 55.6 ID / 59.2 OOD.",
    },
)

claim_truncated_ood_results = claim(
    "**Truncated SFT-then-RL (50 RL steps) achieves 59.2 +/- 0.2 OOD "
    "average on Qwen2.5-Math-7B.** Per-benchmark: ARC-c=84.0 +/- 0.5, "
    "GPQA=39.6 +/- 1.0, MMLU-Pro=53.9 +/- 0.4, OOD avg = "
    "**59.2 +/- 0.2**. Compared to the full 500-step run at 59.9 OOD, "
    "the truncated run is only **0.7 points behind** "
    "[@Limozin2026SFTthenRL, Table 5].",
    title="Result: truncated 50-step SFT-then-RL = 59.2 OOD (only -0.7 vs full 500-step)",
)

# ---------------------------------------------------------------------------
# Comparison vs mixed-policy methods at this compute budget
# ---------------------------------------------------------------------------

claim_truncated_beats_mixed_policy = claim(
    "**Even the truncated 50-step variant outperforms every published "
    "mixed-policy method on the Qwen2.5-Math-7B ID benchmarks.** ID "
    "average 55.6 vs the best mixed-policy ID average of SRFT at 53.2 "
    "is a margin of **+2.4** points -- still ahead despite using 10x "
    "fewer RL steps. On OOD, the truncated 59.2 is competitive: "
    "surpassed only by SRFT (62.5) and ReLIFT (59.5) "
    "[@Limozin2026SFTthenRL, Sec. 4.3; Table 5; Table 1].",
    title="Headline: truncated 50-step variant still beats mixed-policy ID by +2.4 (vs SRFT)",
)

# ---------------------------------------------------------------------------
# FLOPs comparison (Table 6)
# ---------------------------------------------------------------------------

claim_flops_table = claim(
    "**FLOPs comparison (Table 6).** Estimated training FLOPs for each "
    "method on Qwen2.5-Math-7B:\n\n"
    "| Method | FLOPs (x 10^19) |\n"
    "|--------|----------------:|\n"
    "| SFT-then-RL (50 steps) | **3.63** |\n"
    "| LUFFY [@LUFFY] | 6.65 |\n"
    "| ReLIFT [@ReLIFT] | 8.76 |\n\n"
    "The truncated SFT-then-RL pipeline uses **45% fewer FLOPs than "
    "LUFFY (3.63 vs 6.65) and 59% fewer than ReLIFT (3.63 vs 8.76)** "
    "[@Limozin2026SFTthenRL, Table 6; Appendix B].",
    title="Result: truncated SFT-then-RL = 3.63 x 10^19 FLOPs (45-59% fewer than LUFFY/ReLIFT)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 6",
        "caption": "Table 6: estimated training FLOPs.",
    },
)

claim_flops_decomposition = claim(
    "**FLOPs decomposition for the truncated SFT-then-RL pipeline.** "
    "From Appendix B of the paper: SFT for 3 epochs over 46k samples "
    "at sequence length D_data=4,200 contributes 2.43x10^19 FLOPs "
    "(6ND per sample x 3 epochs x 46k samples); 50 RL steps at batch "
    "size 128 with 8 on-policy rollouts of average length D_rollout="
    "4,200 tokens contribute 8 x 8 x N x D_rollout = 1.88x10^15 FLOPs "
    "per sample, totalling 1.20x10^19 FLOPs; combined: "
    "2.43 + 1.20 = **3.63x10^19** FLOPs. By contrast, LUFFY's 500 RL "
    "steps with 7 on-policy rollouts contribute 6.65x10^19 FLOPs "
    "overall and ReLIFT's 500 RL steps + 138 SFT updates contribute "
    "8.76x10^19 FLOPs [@Limozin2026SFTthenRL, Appendix B].",
    title="FLOPs decomposition: SFT 2.43e19 + 50-step RL 1.20e19 = 3.63e19",
)

# ---------------------------------------------------------------------------
# Mechanism: why SFT-then-RL is compute-efficient
# ---------------------------------------------------------------------------

claim_dense_reward_from_sft = claim(
    "**Mechanism: SFT bootstraps the model into a regime with dense RL "
    "reward signal from step 1.** The post-SFT Qwen model already "
    "exhibits strong performance, so RL can be shortened without "
    "significant degradation. The training dynamics (Fig. 3) confirm: "
    "the RL phase of SFT-then-RL starts above 80% training reward on "
    "Qwen and continues to improve, while LUFFY and ReLIFT never reach "
    "the reward level that SFT-then-RL begins with. SFT is cheap "
    "relative to RL (it processes tokens without the overhead of "
    "multiple rollouts), and the strong initialization SFT provides "
    "allows truncating RL to just 50 steps without sacrificing final "
    "score [@Limozin2026SFTthenRL, Sec. 4.3; Fig. 3].",
    title="Mechanism: SFT pre-loads dense reward signal so RL can converge in 50 steps",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 3",
        "caption": "Fig. 3: training reward dynamics; SFT-then-RL starts at >80% reward, LUFFY/ReLIFT never reach this.",
    },
)

claim_compute_efficiency_synthesis = claim(
    "**Synthesis: a strong SFT initialization unlocks compute-efficient "
    "RL.** Combining the truncated-RL accuracy result (55.6 ID / 59.2 "
    "OOD on Qwen2.5-Math-7B) with the FLOPs accounting (3.63x10^19 "
    "vs 6.65x10^19 for LUFFY and 8.76x10^19 for ReLIFT), the "
    "truncated SFT-then-RL pipeline delivers stronger results at "
    "lesser compute -- 'majority of RL gains can materialize within "
    "the early stages of RL training' given a strong SFT init "
    "[@Limozin2026SFTthenRL, Sec. 4.3].",
    title="Synthesis: strong SFT init unlocks compute-efficient RL (better accuracy, fewer FLOPs)",
)

__all__ = [
    "claim_truncated_id_results",
    "claim_truncated_ood_results",
    "claim_truncated_beats_mixed_policy",
    "claim_flops_table",
    "claim_flops_decomposition",
    "claim_dense_reward_from_sft",
    "claim_compute_efficiency_synthesis",
]
