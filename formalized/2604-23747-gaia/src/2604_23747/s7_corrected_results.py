"""Section 4 (Main Experiments): the corrected SFT-then-RL pipeline vs published mixed-policy methods.

Tables 1 (Qwen2.5-Math-7B, ID + OOD) and 4 (Llama-3.1-8B) report the corrected
baselines against the five evaluated mixed-policy methods. This module
formalizes the headline numbers (per-method, per-benchmark) and the
quantitative attribution of the perceived mixed-policy gains to deflated
baselines.

Source: [@Limozin2026SFTthenRL, Sec. 4; Sec. 4.1; Table 1; Table 4].
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Qwen2.5-Math-7B corrected baselines (Table 1)
# ---------------------------------------------------------------------------

claim_qwen_sft_corrected = claim(
    "**Corrected SFT baseline on Qwen2.5-Math-7B (verl): 52.2 +/- 0.2 ID "
    "/ 52.4 +/- 1.1 OOD.** With both bugs fixed (verl [@verl] FSDP "
    "[@FSDP] implementation), the standalone SFT baseline on "
    "Qwen2.5-Math-7B [@Qwen25Math] achieves "
    "AIME24=33.6 +/- 1.4, AIME25=28.2 +/- 0.7, AMC=65.4 +/- 0.9, "
    "MATH-500=90.0 +/- 0.9, Minerva=40.6 +/- 0.6, Olympiad=55.7 +/- 0.6 "
    "(ID avg=52.2 +/- 0.2); ARC-c=82.5 +/- 0.6, GPQA=24.6 +/- 2.9, "
    "MMLU-Pro=50.2 +/- 0.3 (OOD avg=52.4 +/- 1.1) "
    "[@Limozin2026SFTthenRL, Table 1].",
    title="Result: corrected SFT (Qwen2.5-Math-7B) = 52.2 ID / 52.4 OOD",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 1 (top)",
        "caption": "Table 1: SFT corrected-baseline row on Qwen2.5-Math-7B.",
    },
)

claim_qwen_sft_then_rl = claim(
    "**Corrected SFT-then-RL baseline on Qwen2.5-Math-7B (verl): "
    "57.0 +/- 0.3 ID / 59.9 +/- 0.9 OOD.** Adding 500 steps of GRPO RL "
    "on top of the corrected SFT achieves "
    "AIME24=40.4 +/- 0.3, AIME25=29.8 +/- 0.7, AMC=73.2 +/- 1.2, "
    "MATH-500=92.0 +/- 0.2, Minerva=43.9 +/- 0.6, Olympiad=62.8 +/- 0.6 "
    "(ID avg=57.0 +/- 0.3); ARC-c=84.0 +/- 0.7, GPQA=40.6 +/- 1.8, "
    "MMLU-Pro=55.1 +/- 0.6 (OOD avg=59.9 +/- 0.9) "
    "[@Limozin2026SFTthenRL, Table 1].",
    title="Result: corrected SFT-then-RL (Qwen2.5-Math-7B) = 57.0 ID / 59.9 OOD",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 1 (top)",
        "caption": "Table 1: SFT-then-RL corrected-baseline row on Qwen2.5-Math-7B.",
    },
)

# ---------------------------------------------------------------------------
# Mixed-policy methods (reported numbers)
# ---------------------------------------------------------------------------

claim_qwen_mixed_policy_table = claim(
    "**Reported mixed-policy ID averages on Qwen2.5-Math-7B (Table 1).** "
    "The five published methods report the following ID averages over "
    "AIME24/AIME25/AMC/MATH-500/Minerva/Olympiad:\n\n"
    "| Method | AIME24 | AIME25 | AMC | MATH-500 | Minerva | Olympiad | ID Avg |\n"
    "|--------|------:|------:|------:|---------:|--------:|---------:|------:|\n"
    "| LUFFY [@LUFFY] | 29.4 | 23.1 | 65.6 | 87.6 | 37.5 | 57.2 | 50.1 |\n"
    "| ReLIFT [@ReLIFT] | 28.3 | 22.9 | 65.1 | 87.9 | -- | 57.3 | -- |\n"
    "| SRFT [@SRFT] | 35.3 | 21.6 | 74.3 | 89.8 | 39.7 | 58.3 | 53.2 |\n"
    "| Prefix-RFT [@PrefixRFT] | 31.8 | 26.4 | 68.2 | 88.4 | 40.3 | 55.7 | 51.8 |\n"
    "| HPT [@HPT] | 33.0 | 21.9 | 69.4 | 89.2 | 46.0 | 56.9 | 52.7 |\n\n"
    "The best published mixed-policy ID average is SRFT at 53.2 "
    "[@Limozin2026SFTthenRL, Table 1].",
    title="Reported ID averages: SRFT 53.2 = best published mixed-policy",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 1",
        "caption": "Table 1: reported mixed-policy method scores on Qwen2.5-Math-7B (published).",
    },
)

# ---------------------------------------------------------------------------
# Headline Qwen claim: +3.8 points
# ---------------------------------------------------------------------------

claim_qwen_plus_3p8 = claim(
    "**Headline: corrected SFT-then-RL beats best published mixed-policy "
    "method by +3.8 points on Qwen2.5-Math-7B ID benchmarks.** The "
    "corrected SFT-then-RL ID average is 57.0; the best published "
    "mixed-policy ID average is SRFT at 53.2; the difference is "
    "**57.0 - 53.2 = +3.8** points. The corrected SFT *alone* (without "
    "any RL) at 52.2 already exceeds LUFFY (50.1), ReLIFT (-- but the "
    "Minerva-excluded subset shows clear gap), and Prefix-RFT (51.8) "
    "[@Limozin2026SFTthenRL, Sec. 4; Table 1].",
    title="Headline (Qwen2.5-Math-7B): SFT-then-RL beats best mixed-policy by +3.8 ID points",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Sec. 4 / Table 1",
        "caption": "Sec. 4: SFT-then-RL 57.0 vs SRFT 53.2 = +3.8 ID.",
    },
)

claim_qwen_ood_competitive = claim(
    "**OOD generalization on Qwen2.5-Math-7B: SFT-then-RL is "
    "second-best (59.9), beaten only by SRFT (62.5).** On the OOD "
    "subset (ARC-c, GPQA-Diamond, MMLU-Pro [@ARCc; @GPQA; @MMLUPro]), "
    "the corrected SFT-then-RL achieves 59.9 OOD average, second only "
    "to SRFT at 62.5 (the same SRFT that allegedly trains on the "
    "weak-LR SFT baseline). All other mixed-policy methods score "
    "57.8-59.0 OOD, so the corrected pipeline is competitive on OOD "
    "even when not topping it [@Limozin2026SFTthenRL, Table 1].",
    title="OOD result: corrected SFT-then-RL is second-best on Qwen2.5-Math-7B (59.9, behind SRFT's 62.5)",
)

# ---------------------------------------------------------------------------
# Reproduction attempts (LUFFY / ReLIFT scored under controlled setup)
# ---------------------------------------------------------------------------

claim_qwen_reproduction = claim(
    "**Reproduction attempts of LUFFY and ReLIFT in verl yield lower "
    "scores than the published numbers.** When LUFFY [@LUFFY] and "
    "ReLIFT [@ReLIFT] are reimplemented in verl using their original "
    "hyperparameters (with the OpenRLHF/Llama-Factory loss aggregation "
    "fix applied to be fair), they achieve LUFFY = 46.3 ID / 58.0 OOD "
    "and ReLIFT = 48.8 ID / 56.2 OOD on Qwen2.5-Math-7B -- below their "
    "respective published 50.1 / 57.8 and (no ID published) / 59.5 "
    "numbers, and well below the 57.0 / 59.9 corrected SFT-then-RL "
    "[@Limozin2026SFTthenRL, Table 1; Sec. 3].",
    title="Reproduction: LUFFY 46.3 ID / ReLIFT 48.8 ID under controlled (fair) verl setup",
)

# ---------------------------------------------------------------------------
# Attribution of perceived gains
# ---------------------------------------------------------------------------

claim_perceived_gains_attribution = claim(
    "**The perceived mixed-policy gains stem from comparison against "
    "deflated SFT baselines.** For LUFFY and ReLIFT the deflation "
    "comes from the framework bugs (Section 2 / s4 + s5 modules) "
    "[@LUFFY; @ReLIFT]; for SRFT it comes from suboptimal "
    "hyperparameters (Section 4 / Table 3) [@SRFT]; for Prefix-RFT it "
    "is inherited from LUFFY's deflated baseline [@PrefixRFT]; for HPT "
    "the SFT setup is undocumented but the paper assumes it inherits "
    "the same affected pipelines [@HPT; @Limozin2026SFTthenRL, Sec. 4].",
    title="Attribution: perceived gains = deflated SFT baselines (bugs + bad hyperparams + inheritance)",
)

# ---------------------------------------------------------------------------
# Llama-3.1-8B corrected baselines (Table 4)
# ---------------------------------------------------------------------------

claim_llama_sft = claim(
    "**Corrected SFT baseline on Llama-3.1-8B: 33.9 +/- 0.9 average.** "
    "On the subset for which all methods provide scores "
    "(AIME24/AMC/MATH-500/Minerva/Olympiad), the corrected standalone "
    "SFT achieves AIME24=7.0 +/- 1.1, AMC=40.4 +/- 0.6, "
    "MATH-500=68.4 +/- 2.3, Minerva=17.3 +/- 0.9, Olympiad=36.2 +/- 1.1, "
    "average=**33.9 +/- 0.9** [@Limozin2026SFTthenRL, Table 4].",
    title="Result: corrected SFT (Llama-3.1-8B) = 33.9 average",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 4",
        "caption": "Table 4: SFT corrected row on Llama-3.1-8B.",
    },
)

claim_llama_sft_then_rl = claim(
    "**Corrected SFT-then-RL baseline on Llama-3.1-8B: 43.7 +/- 0.2 "
    "average.** AIME24=16.5 +/- 0.8, AMC=53.9 +/- 1.3, "
    "MATH-500=78.6 +/- 1.2, Minerva=20.7 +/- 1.5, Olympiad=48.5 +/- 0.1, "
    "average=**43.7 +/- 0.2** [@Limozin2026SFTthenRL, Table 4].",
    title="Result: corrected SFT-then-RL (Llama-3.1-8B) = 43.7 average",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 4",
        "caption": "Table 4: SFT-then-RL corrected row on Llama-3.1-8B.",
    },
)

claim_llama_mixed_policy_table = claim(
    "**Reported mixed-policy averages on Llama-3.1-8B (Table 4).** The "
    "five published methods report the following averages over "
    "AIME24/AMC/MATH-500/Minerva/Olympiad on Llama-3.1-8B "
    "(starred entries use a different chat template per the original "
    "papers):\n\n"
    "| Method | AIME24 | AMC | MATH-500 | Minerva | Olympiad | Avg |\n"
    "|--------|------:|------:|---------:|--------:|---------:|----:|\n"
    "| LUFFY [@LUFFY] | 0.8 | 13.1 | 34.6 | 12.5 | 10.8 | 14.4 |\n"
    "| ReLIFT [@ReLIFT] | 0.6 | 14.5 | 35.4 | 14.7 | 12.8 | 15.6 |\n"
    "| SRFT* [@SRFT] | 1.9 | 14.3 | 40.1 | 15.3 | 9.5 | 16.2 |\n"
    "| Prefix-RFT* [@PrefixRFT] | 1.3 | 13.3 | 40.6 | 18.1 | 11.9 | 17.0 |\n"
    "| HPT* [@HPT] | 2.1 | 18.6 | 47.8 | 18.8 | 20.4 | 21.5 |\n\n"
    "The best published mixed-policy method on Llama is HPT at 21.5 "
    "average [@Limozin2026SFTthenRL, Table 4].",
    title="Reported Llama averages: HPT 21.5 = best published mixed-policy",
)

# ---------------------------------------------------------------------------
# Headline Llama claim: +22.2 points
# ---------------------------------------------------------------------------

claim_llama_plus_22p2 = claim(
    "**Headline: corrected SFT-then-RL beats best published mixed-policy "
    "method by +22.2 points on Llama-3.1-8B math benchmarks.** The "
    "corrected SFT-then-RL average is 43.7; the best published "
    "mixed-policy average is HPT at 21.5; the difference is "
    "**43.7 - 21.5 = +22.2** points. The corrected SFT alone at 33.9 "
    "already exceeds the best mixed-policy by +12.4 points "
    "[@Limozin2026SFTthenRL, Sec. 4.1; Table 4].",
    title="Headline (Llama-3.1-8B): SFT-then-RL beats best mixed-policy by +22.2 points",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 4",
        "caption": "Table 4: 43.7 vs 21.5 = +22.2 on Llama-3.1-8B.",
    },
)

claim_llama_failure_explanation = claim(
    "**Why the failure of mixed-policy methods on Llama is particularly "
    "instructive.** Unlike Qwen2.5-Math-7B [@Qwen25Math] which is "
    "pre-trained with emphasis on math data, Llama-3.1-8B [@Llama3] "
    "has comparatively little mathematical reasoning content in its "
    "pre-training distribution [@SpuriousRewards], making the "
    "*bootstrapping role* of SFT far more critical. The training "
    "dynamics (Fig. 3 bottom row) make this concrete: with SFT-then-RL, "
    "the RL phase starts at approximately 60% training reward because "
    "SFT has already injected the mathematical knowledge Llama lacks "
    "natively; mixed-policy methods, by contrast, start near zero "
    "reward and improve only slowly (LUFFY's reward remains largely "
    "flat over 500 steps, indicating the off-policy demonstrations "
    "provide a learning signal but one too sparse to match SFT-then-RL's "
    "dense reward) [@Limozin2026SFTthenRL, Sec. 4.1].",
    title="Why Llama gap is dramatic: SFT's bootstrapping role is critical when pre-training lacks math",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 3 bottom row",
        "caption": "Fig. 3 bottom: Llama training reward; SFT-then-RL starts at ~60%, mixed-policy stays flat near 0%.",
    },
)

claim_efficiency_gap = claim(
    "**Fundamental efficiency gap: mixed-policy methods must "
    "simultaneously bootstrap reasoning *and* refine it through RL, "
    "but the RL signal is extremely weak when the model cannot yet "
    "produce correct solutions on its own.** The off-policy "
    "demonstrations provide some supervision, but it is diluted by "
    "on-policy rollouts that carry little to no reward signal early "
    "in training. SFT-then-RL cleanly separates these two objectives: "
    "SFT first bootstraps the model into a regime where it reliably "
    "generates correct solutions, then RL refines this already-capable "
    "policy with dense reward signal from the start. While mixed-policy "
    "methods may eventually converge to comparable scores given enough "
    "steps, they do so far less efficiently because the RL component "
    "contributes minimally until the model has acquired sufficient "
    "knowledge -- precisely the knowledge that a dedicated SFT stage "
    "provides upfront [@Limozin2026SFTthenRL, Sec. 4.1].",
    title="Argument: SFT-then-RL is fundamentally more sample-efficient than mixed-policy",
)

# ---------------------------------------------------------------------------
# Per-method comparison summary
# ---------------------------------------------------------------------------

claim_per_method_corrected_beats_each = claim(
    "**The corrected SFT-then-RL pipeline beats each of the five "
    "evaluated mixed-policy methods individually on Qwen2.5-Math-7B ID "
    "average:**\n\n"
    "| vs Method | Mixed-policy ID | SFT-then-RL ID | Delta |\n"
    "|-----------|----------------:|---------------:|-----:|\n"
    "| LUFFY [@LUFFY] | 50.1 | 57.0 | **+6.9** |\n"
    "| ReLIFT [@ReLIFT] | -- (no ID avg published) | 57.0 | -- |\n"
    "| SRFT [@SRFT] | 53.2 | 57.0 | **+3.8** |\n"
    "| Prefix-RFT [@PrefixRFT] | 51.8 | 57.0 | **+5.2** |\n"
    "| HPT [@HPT] | 52.7 | 57.0 | **+4.3** |\n\n"
    "The minimum margin is +3.8 (vs SRFT, the strongest published "
    "mixed-policy method), which is the headline number in the "
    "abstract [@Limozin2026SFTthenRL, Table 1].",
    title="Per-method: corrected SFT-then-RL beats each method individually (min margin +3.8 vs SRFT)",
)

__all__ = [
    "claim_qwen_sft_corrected",
    "claim_qwen_sft_then_rl",
    "claim_qwen_mixed_policy_table",
    "claim_qwen_plus_3p8",
    "claim_qwen_ood_competitive",
    "claim_qwen_reproduction",
    "claim_perceived_gains_attribution",
    "claim_llama_sft",
    "claim_llama_sft_then_rl",
    "claim_llama_mixed_policy_table",
    "claim_llama_plus_22p2",
    "claim_llama_failure_explanation",
    "claim_efficiency_gap",
    "claim_per_method_corrected_beats_each",
]
