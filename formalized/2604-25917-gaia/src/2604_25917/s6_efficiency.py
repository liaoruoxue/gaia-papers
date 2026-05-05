"""Section 5.4: Efficiency analyses on latent-space recursion -- inference
speedup (Fig. 5) and overall token usage reduction (Fig. 6) of
RecursiveMAS vs Recursive-TextMAS, by recursion round.

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 5.4 + Figs. 5-6 +
Table 2 (per-task time/tokens columns).
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Inference time speedup (Figure 5)
# ---------------------------------------------------------------------------

claim_speedup_table = claim(
    "**Average inference-time speedup of RecursiveMAS over Recursive-"
    "TextMAS, by recursion round (Fig. 5).** Average end-to-end "
    "wall-clock speedup factors:\n\n"
    "| Recursion round $r$ | Avg. speedup |\n"
    "|---:|:---:|\n"
    "| 1 | **1.2x** |\n"
    "| 2 | **1.9x** |\n"
    "| 3 | **2.4x** |\n",
    title="Fig. 5: avg inference speedup = 1.2x / 1.9x / 2.4x at r=1/2/3",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 5",
        "caption": "Fig. 5: Inference-time speedup of RecursiveMAS across three recursion rounds (avg 1.2x at r=1, 1.9x at r=2, 2.4x at r=3).",
    },
)

claim_speedup_grows_with_depth = claim(
    "**Inference speedup of RecursiveMAS grows with recursion depth.** "
    "Although deeper recursion adds total cost, RecursiveMAS's "
    "speedup over the text-mediated baseline *increases* with $r$: "
    "from 1.2x (r=1) to 1.9x (r=2) to 2.4x (r=3). The trend is "
    "consistent across all six Table-2 columns and aligns with the "
    "method's design -- recursive collaboration directly in latent "
    "space avoids repeated intermediate text generation, so each "
    "additional round amplifies the constant-factor advantage rather "
    "than diluting it.",
    title="Result: speedup is increasing in recursion depth -- 1.2x -> 1.9x -> 2.4x",
)

# Per-task speedup illustration from Table 2 time rows (Scaled, r=3)
claim_runtime_examples_r3 = claim(
    "**Per-task end-to-end runtime examples at $r = 3$ (Scaled "
    "setup), in seconds.** Drawn from the Table-2 Time rows:\n\n"
    "| Task | RecursiveMAS | Recursive-TextMAS | Speedup |\n"
    "|---|---:|---:|:---:|\n"
    "| MATH500 | 2320 | 6010 | 2.6x |\n"
    "| AIME2025 | 8981 | 19304 | 2.1x |\n"
    "| AIME2026 | 9623 | 19678 | 2.0x |\n"
    "| GPQA-D | 2638 | 7537 | 2.9x |\n"
    "| MedQA | 1912 | 3922 | 2.1x |\n"
    "| LiveCodeBench | 10186 | 22036 | 2.2x |\n",
    title="Table 2 time rows at r=3 (Scaled): per-task speedup = 2.0x to 2.9x",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 2 (Time rows, r=3)",
    },
)

# ---------------------------------------------------------------------------
# Overall token usage reduction (Figure 6)
# ---------------------------------------------------------------------------

claim_token_reduction_table = claim(
    "**Average overall token usage reduction of RecursiveMAS vs "
    "Recursive-TextMAS, by recursion round (Fig. 6).**\n\n"
    "| Recursion round $r$ | Avg. token reduction |\n"
    "|---:|:---:|\n"
    "| 1 | **34.6%** |\n"
    "| 2 | **65.5%** |\n"
    "| 3 | **75.6%** |\n",
    title="Fig. 6: avg token reduction = 34.6% / 65.5% / 75.6% at r=1/2/3",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 6",
        "caption": "Fig. 6: Token reduction of RecursiveMAS across three recursion rounds (avg -34.6% at r=1, -65.5% at r=2, -75.6% at r=3).",
    },
)

claim_token_reduction_explained = claim(
    "**Why token reduction grows so steeply.** Recursive-TextMAS "
    "repeatedly decodes intermediate text at *every* recursion round, "
    "so its token overhead grows roughly linearly with $r$. "
    "RecursiveMAS performs intermediate recursion entirely in the "
    "latent space and only decodes the final answer in the last "
    "round, so its token usage stays nearly constant in $r$. The gap "
    "between linear-in-$r$ TextMAS and constant-in-$r$ RecursiveMAS "
    "thus widens with depth: 34.6% reduction at $r=1$ widens to "
    "75.6% at $r=3$.",
    title="Mechanism: TextMAS tokens scale ~linearly in r; RecursiveMAS tokens are ~constant -> gap widens",
)

# Per-task token examples from Table 2 (Scaled, r=3)
claim_token_examples_r3 = claim(
    "**Per-task overall token usage at $r = 3$ (Scaled setup).** "
    "Drawn from the Table-2 Token rows:\n\n"
    "| Task | RecursiveMAS | Recursive-TextMAS | Reduction |\n"
    "|---|---:|---:|:---:|\n"
    "| MATH500 | 893 | 4100 | -78.2% |\n"
    "| AIME2025 | 5342 | 23651 | -77.4% |\n"
    "| AIME2026 | 6860 | 22915 | -70.1% |\n"
    "| GPQA-D | 2524 | 8091 | -68.8% |\n"
    "| MedQA | 1056 | 3731 | -71.7% |\n"
    "| LiveCodeBench | 2247 | 7078 | -68.3% |\n",
    title="Table 2 token rows at r=3 (Scaled): per-task token reduction = 68% to 78%",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Table 2 (Token rows, r=3)",
    },
)

# ---------------------------------------------------------------------------
# Synthesis: efficiency advantage scales with depth
# ---------------------------------------------------------------------------

claim_efficiency_synthesis = claim(
    "**Efficiency synthesis: latent-space recursion enables "
    "compounding gains.** Both Fig. 5 (speedup) and Fig. 6 (token "
    "reduction) show that the efficiency advantage of RecursiveMAS "
    "*amplifies* with recursion depth. Empirically, this is the "
    "system-level realization of the runtime-complexity gap "
    "predicted by Proposition 3.1 (Section 3): replacing the "
    "$m|V| d_h$ vocabulary projection with the cheaper $m d_h^2$ "
    "latent transformation across $N$ agents and $r$ rounds yields "
    "a constant-factor saving per round that compounds with depth.",
    title="Synthesis: empirical speedup + token reduction compound with r, matching Proposition 3.1",
)

__all__ = [
    "claim_speedup_table",
    "claim_speedup_grows_with_depth",
    "claim_runtime_examples_r3",
    "claim_token_reduction_table",
    "claim_token_reduction_explained",
    "claim_token_examples_r3",
    "claim_efficiency_synthesis",
]
