"""Section 4.3 (RQ2): cross-benchmark and cross-model transfer.

The frozen AHE harness transfers to (a) SWE-bench-verified at 12% fewer tokens
than the seed, and (b) three alternate base-model families with +5.1 to +10.1
pp gains.

Source: Lin et al. 2026 [@Lin2026AHE], Section 4.3 + Table 2 + Fig. 3 +
Table 4.
"""

from gaia.lang import claim

# ===========================================================================
# Cross-benchmark transfer: SWE-bench-verified
# ===========================================================================

claim_swe_table_pass1 = claim(
    "**Table 2 (left columns): SWE-bench-verified pass@1 (success rate) "
    "by repo.** AHE and the two self-evolve baselines (ACE, TF-GRPO) "
    "are evolved on Terminal-Bench 2 and evaluated *without* in-domain "
    "re-evolution. All four columns run on GPT-5.4. Per-row bold marks "
    "the best.\n\n"
    "| Repo | N | ACE | TF-GRPO | NexAU0 | AHE |\n"
    "|---|---:|---:|---:|---:|---:|\n"
    "| All | 500 | 74.6% | 74.2% | 75.2% | **75.6%** |\n"
    "| django | 231 | 79.2% | 78.8% | 79.2% | **81.0%** |\n"
    "| sympy | 75 | 69.3% | 68.0% | **70.7%** | **70.7%** |\n"
    "| sphinx-doc | 44 | 61.4% | 65.9% | 68.2% | **70.5%** |\n"
    "| matplotlib | 34 | 70.6% | 70.6% | **73.5%** | **73.5%** |\n"
    "| scikit-learn | 32 | 93.8% | 93.8% | **93.8%** | 87.5% |\n"
    "| pydata | 22 | 77.3% | 77.3% | **77.3%** | 72.7% |\n"
    "| astropy | 22 | 59.1% | **59.1%** | 54.5% | 50.0% |\n",
    title="Table 2 (left): SWE-bench-verified pass@1 per repo",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 2",
        "caption": "Table 2 left columns: success rate on SWE-bench-verified.",
    },
)

claim_swe_table_tokens = claim(
    "**Table 2 (right columns): SWE-bench-verified Tokens$_k$ per "
    "trial (in thousands).** Lower is better.\n\n"
    "| Repo | N | ACE | TF-GRPO | NexAU0 | AHE |\n"
    "|---|---:|---:|---:|---:|---:|\n"
    "| All | 500 | 679 | 582 | 526 | **461** |\n"
    "| django | 231 | 707 | 583 | 527 | **484** |\n"
    "| sympy | 75 | 602 | 572 | 494 | **479** |\n"
    "| sphinx-doc | 44 | 990 | 848 | 731 | **656** |\n"
    "| matplotlib | 34 | 622 | 530 | 486 | **391** |\n"
    "| scikit-learn | 32 | 451 | 378 | 307 | **257** |\n"
    "| pydata | 22 | 563 | 516 | 386 | **338** |\n"
    "| astropy | 22 | 546 | 470 | 667 | **277** |\n",
    title="Table 2 (right): SWE-bench-verified Tokens_k per trial",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 2",
        "caption": "Table 2 right columns: tokens per trial on SWE-bench-verified.",
    },
)

claim_swe_aggregate_success = claim(
    "**SWE-bench-verified aggregate success rate: AHE 75.6% vs seed "
    "75.2% (+0.4 pp).** The frozen AHE harness, evolved on Terminal-"
    "Bench 2 and applied to SWE-bench-verified without re-evolution, "
    "tops the aggregate success rate over all 500 tasks. Both ACE "
    "(74.6%) and TF-GRPO (74.2%) regress below the untouched NexAU0 "
    "seed.",
    title="SWE transfer: AHE 75.6% > seed 75.2% > ACE 74.6% > TF-GRPO 74.2%",
)

claim_swe_aggregate_tokens = claim(
    "**SWE-bench-verified aggregate tokens: AHE 461k vs seed 526k "
    "(-12.4%).** The frozen AHE harness uses **12% fewer tokens than "
    "the seed** in aggregate (461 vs 526 thousand tokens per trial), "
    "a 32% reduction vs ACE (679k) and a 21% reduction vs TF-GRPO "
    "(582k). Encoding behavior in tools, middleware, and memory "
    "rather than in the prompt avoids the per-call re-derivation "
    "cost that prompt-only baselines pay.",
    title="SWE transfer: AHE 461k tokens, -12.4% vs seed, -32% vs ACE, -21% vs TF-GRPO",
)

claim_swe_concentration = claim(
    "**Per-repo gain concentration: django and sphinx-doc.** The seed-"
    "relative AHE gain on SWE-bench-verified concentrates on django "
    "(+1.8 pp, 79.2 -> 81.0) and sphinx-doc (+2.3 pp, 68.2 -> 70.5), "
    "the two largest and most token-expensive repositories whose "
    "multi-step edit-and-verify loop matches the structure AHE's "
    "tools, middleware, and long-term memory compress on Terminal-"
    "Bench 2. Marginal regressions appear only on the three smallest "
    "repositories (scikit-learn 32 tasks, pydata 22, astropy 22), "
    "consistent with pass@1 variance on small repos exceeding the "
    "per-repo gain.",
    title="SWE transfer: gain concentrates on django + sphinx-doc; regressions only on the 3 smallest repos",
)

claim_succ_per_mtok_table = claim(
    "**Table 4: SWE-bench-verified Succ/Mtok (expected successes per "
    "million tokens, higher is better).** Derived from Table 2 as "
    "pass@1 * 10^3 / Tokens$_k$. AHE leads in 7 of 8 rows (the "
    "exception is small-repo astropy where it is co-leader on cost "
    "efficiency at 1.81 with much fewer tokens).\n\n"
    "| Repo | N | ACE | TF-GRPO | NexAU0 | AHE |\n"
    "|---|---:|---:|---:|---:|---:|\n"
    "| All | 500 | 1.10 | 1.27 | 1.43 | **1.64** |\n"
    "| django | 231 | 1.12 | 1.35 | 1.50 | **1.67** |\n"
    "| sympy | 75 | 1.15 | 1.19 | 1.43 | **1.48** |\n"
    "| sphinx-doc | 44 | 0.62 | 0.78 | 0.93 | **1.07** |\n"
    "| matplotlib | 34 | 1.14 | 1.33 | 1.51 | **1.88** |\n"
    "| scikit-learn | 32 | 2.08 | 2.48 | 3.06 | **3.40** |\n"
    "| pydata | 22 | 1.37 | 1.50 | 2.00 | **2.15** |\n"
    "| astropy | 22 | 1.08 | 1.26 | 0.82 | **1.81** |\n",
    title="Table 4: SWE-bench-verified Succ/Mtok per repo (AHE leads 7 of 8)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 4",
        "caption": "Table 4: Cost-efficiency on SWE-bench-verified, Succ/Mtok = pass@1 * 10^3 / Tokens_k.",
    },
)

# ===========================================================================
# Cross-model transfer: alternate base models on Terminal-Bench 2
# ===========================================================================

claim_cross_model_table = claim(
    "**Fig. 3: cross-model transfer on Terminal-Bench 2 (89 tasks).** "
    "The AHE workspace evolved on GPT-5.4 high is re-evaluated on each "
    "base model without further evolution, paired against the NexAU0 "
    "seed on the same base. All five gains are positive (+2.3 to +10.1 "
    "pp).\n\n"
    "| Base model | Seed pass@1 | AHE pass@1 | Delta |\n"
    "|---|---:|---:|---:|\n"
    "| GPT-5.4 medium | 65.7% | 68.0% | +2.3 pp |\n"
    "| GPT-5.4 high (in-distribution) | 69.7% | 77.0% | +7.3 pp |\n"
    "| GPT-5.4 xhigh | 72.5% | 74.7% | +2.3 pp |\n"
    "| gemini-3.1-flash-lite-preview | 36.5% | 41.6% | +5.1 pp |\n"
    "| deepseek-v4-flash | 51.7% | 61.8% | +10.1 pp |\n"
    "| qwen-3.6-plus | 56.2% | 62.5% | +6.3 pp |\n",
    title="Fig. 3: cross-model transfer (5 alternate bases, all +2.3 to +10.1 pp)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 3",
        "caption": "Fig. 3: Cross-model transfer on Terminal-Bench 2, 89 tasks.",
    },
)

claim_gpt54_med_transfer = claim(
    "**GPT-5.4 medium transfer: +2.3 pp (65.7% -> 68.0%).** The same-"
    "family but lower-reasoning-tier base. Evolution operating point "
    "was fitted to GPT-5.4 high; medium has more time-per-step slack "
    "but loses a reasoning tier of raw capability.",
    title="Cross-family transfer: GPT-5.4 med +2.3 pp (65.7% -> 68.0%)",
)

claim_gpt54_xhigh_transfer = claim(
    "**GPT-5.4 xhigh transfer: +2.3 pp (72.5% -> 74.7%).** Same-family "
    "higher-reasoning tier. xhigh pushes more trials past the per-"
    "task timeout, which the pass@1 convention counts as failures, "
    "discounting the gain.",
    title="Cross-family transfer: GPT-5.4 xhigh +2.3 pp (72.5% -> 74.7%)",
)

claim_qwen_transfer = claim(
    "**qwen-3.6-plus [@Qwen36; @Qwen3] transfer: +6.3 pp (56.2% -> "
    "62.5%).** Cross-family transfer to a Qwen base.",
    title="Cross-family transfer: qwen-3.6-plus +6.3 pp (56.2% -> 62.5%)",
)

claim_gemini_transfer = claim(
    "**gemini-3.1-flash-lite-preview [@Gemini31FlashLite] transfer: "
    "+5.1 pp (36.5% -> 41.6%).** Cross-family transfer to a Gemini "
    "base further from saturation.",
    title="Cross-family transfer: gemini-3.1-flash-lite +5.1 pp (36.5% -> 41.6%)",
)

claim_deepseek_transfer = claim(
    "**deepseek-v4-flash [@DeepSeekV4] transfer: +10.1 pp (51.7% -> "
    "61.8%).** Cross-family transfer to a DeepSeek base, the largest "
    "gain across all 5 alternate bases.",
    title="Cross-family transfer: deepseek-v4-flash +10.1 pp (51.7% -> 61.8%)",
)

# ===========================================================================
# Cross-family vs within-family pattern + interpretation
# ===========================================================================

claim_cross_family_dominate = claim(
    "**Cross-family gains dominate within-family ones.** The three "
    "cross-family gains (deepseek-v4-flash +10.1, qwen-3.6-plus +6.3, "
    "gemini-3.1-flash-lite +5.1) are all larger than the two within-"
    "family GPT-5.4 medium and xhigh gains (+2.3 each). The pattern "
    "tracks distance from saturation: bases further from saturation "
    "lean more on the coordination patterns AHE has fixed inside "
    "tools, middleware, and long-term memory, while a stronger base "
    "re-derives the same coordination from its prompt at low marginal "
    "cost.",
    title="Cross-model finding: cross-family gains > within-family gains; correlated with distance from saturation",
)

claim_non_monotone_within_family = claim(
    "**Within one family the profile is non-monotone.** GPT-5.4 "
    "medium +2.3, GPT-5.4 high +7.3, GPT-5.4 xhigh +2.3. The non-"
    "monotonicity arises because AHE's step budget and per-task "
    "timeout were fitted to GPT-5.4 high during evolution: medium has "
    "more time-per-step slack but loses a reasoning tier, while "
    "xhigh pushes more trials past the timeout (counted as failures). "
    "Either direction discounts the gain.",
    title="Cross-model finding: non-monotone within-family profile (med +2.3, high +7.3, xhigh +2.3)",
)

claim_all_five_positive = claim(
    "**All five cross-model gains are strictly positive.** The "
    "load-bearing finding for the transfer claim is that all five "
    "gains land positive (+2.3, +2.3, +5.1, +6.3, +10.1 pp): the AHE "
    "workspace is not specific to one provider's idioms or one "
    "reasoning depth. The magnitudes track the evolution operating "
    "point rather than raw base capability, so the timeout-budget "
    "coupling is treated as a generalization hazard discussed in "
    "Limitations.",
    title="Cross-model finding: all 5 cross-model transfers are positive (+2.3 to +10.1 pp)",
)

claim_evolved_components_general = claim(
    "**Evolved components encode general engineering experience, not "
    "benchmark-specific tuning.** The combination of (i) cross-"
    "benchmark transfer from Terminal-Bench 2 to SWE-bench-verified at "
    "+0.4 pp aggregate success and -12% tokens, and (ii) all 5 cross-"
    "model gains positive ranging +2.3 to +10.1 pp indicates the "
    "evolved harness encodes general coding-agent engineering "
    "experience rather than features specific to the optimization "
    "target.",
    title="Synthesis: AHE-evolved components encode general experience, not benchmark-specific tuning",
)

__all__ = [
    "claim_swe_table_pass1",
    "claim_swe_table_tokens",
    "claim_swe_aggregate_success",
    "claim_swe_aggregate_tokens",
    "claim_swe_concentration",
    "claim_succ_per_mtok_table",
    "claim_cross_model_table",
    "claim_gpt54_med_transfer",
    "claim_gpt54_xhigh_transfer",
    "claim_qwen_transfer",
    "claim_gemini_transfer",
    "claim_deepseek_transfer",
    "claim_cross_family_dominate",
    "claim_non_monotone_within_family",
    "claim_all_five_positive",
    "claim_evolved_components_general",
]
