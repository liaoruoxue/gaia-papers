"""Section 6.2: Main results -- aggregate solve rates across 1350
trials, per-strategy table, pairwise significance tests, effect sizes.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 6.2 +
Tables 3-4 + Figure 1.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Per-strategy aggregate solve rates (Table 3)
# ---------------------------------------------------------------------------

claim_table_3_aggregate_solve_rates = claim(
    "**Table 3: Aggregate solve rates across all experiments (1350 "
    "total trials, 270 per strategy).**\n\n"
    "| Strategy | Solved/N | Rate | 95% Wilson CI |\n"
    "|---|---|---|---|\n"
    "| Pressure-field | 131/270 | **48.5%** | 42.6%-54.5% |\n"
    "| Conversation | 30/270 | 11.1% | 7.9%-15.4% |\n"
    "| Hierarchical | 4/270 | 1.5% | 0.6%-3.7% |\n"
    "| Sequential | 1/270 | 0.4% | 0.1%-2.1% |\n"
    "| Random | 1/270 | 0.4% | 0.1%-2.1% |\n\n"
    "Chi-square test across all five strategies: $\\chi^2 > 200$, "
    "$p < 0.001$.",
    title="Table 3: aggregate solve rates (270 trials per strategy; pressure-field 48.5% / conversation 11.1% / hierarchical 1.5% / seq 0.4% / random 0.4%)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 3 (page 26)",
        "caption": "Table 3: Aggregate solve rates across all experiments (1350 total trials, 270 per strategy). Chi-square test across all five strategies: chi^2 > 200, p < 0.001.",
    },
)

# ---------------------------------------------------------------------------
# Headline pairwise gap claims (4x and 30x)
# ---------------------------------------------------------------------------

claim_pressure_vs_conversation_4x = claim(
    "**Pressure-field beats conversation by approximately $4\\times$ "
    "in aggregate solve rate.** Pressure-field's 48.5% (131/270) "
    "vs conversation's 11.1% (30/270) -- a ratio of "
    "$48.5 / 11.1 \\approx 4.4 \\times$. Per the chi-square test "
    "across all five strategies and the pairwise comparison, this "
    "gap has $p < 0.001$. Cohen's $h \\approx 1.16$ on easy "
    "problems vs conversation, a *large* effect ($h > 0.8$).",
    title="Result: pressure-field 48.5% vs conversation 11.1% = 4.4x ratio (p < 0.001, Cohen's h = 1.16 on easy)",
)

claim_pressure_vs_hierarchical_30x = claim(
    "**Pressure-field beats hierarchical control by approximately "
    "$30\\times$ in aggregate solve rate.** Pressure-field's 48.5% "
    "(131/270) vs hierarchical's 1.5% (4/270) -- a ratio of "
    "$48.5 / 1.5 \\approx 32.3 \\times$. With $p < 0.001$ across "
    "all pairwise tests, the gap is highly significant.",
    title="Result: pressure-field 48.5% vs hierarchical 1.5% = ~30x ratio (p < 0.001)",
)

claim_conversation_intermediate = claim(
    "**Conversation provides intermediate performance, far below "
    "pressure-field but significantly above hierarchical.** "
    "AutoGen-style conversation achieves 11.1% overall, "
    "significantly better than hierarchical ($p < 0.001$) but far "
    "below pressure-field. Notably, conversation solves *only easy "
    "problems* (33.3% on easy, 0% on medium, 0% on hard).",
    title="Result: conversation = 11.1% intermediate (significantly > hierarchical, far < pressure-field; only solves easy problems)",
)

claim_hierarchical_sequential_random_fail = claim(
    "**Hierarchical, sequential, and random fail to solve almost "
    "anything.** Hierarchical achieves only 1.5% (4/270), "
    "comparable to random (0.4%, 1/270). Both strategies fail "
    "entirely on medium and hard problems. **Despite explicit "
    "coordination, hierarchical's solve rate is in the same order "
    "of magnitude as random selection.**",
    title="Result: hierarchical 1.5% / sequential 0.4% / random 0.4% all fail entirely on medium and hard",
)

# ---------------------------------------------------------------------------
# Effect-size claim (Figure 4)
# ---------------------------------------------------------------------------

claim_effect_sizes_large = claim(
    "**All pairwise effect sizes (pressure-field vs each baseline, "
    "easy difficulty) exceed Cohen's 'large effect' threshold "
    "($h > 0.8$).** Specifically: $h = 1.16$ vs conversation, "
    "$h \\approx 1.97$ vs hierarchical, and $h = 2.18$ vs "
    "sequential / random. The full pairwise breakdown is shown in "
    "Figure 4.",
    title="Result: pairwise effect sizes h = 1.16-2.18 vs each baseline (all > Cohen's large-effect 0.8 threshold) on easy",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Fig. 4 (page 34)",
        "caption": "Fig. 4: Effect sizes (Cohen's h) for pressure-field versus each baseline on easy problems.",
    },
)

# ---------------------------------------------------------------------------
# Discussion-internal claim: contradicts the prevailing assumption
# ---------------------------------------------------------------------------

claim_result_contradicts_explicit_orchestration_assumption = claim(
    "**This result contradicts the common assumption that "
    "explicit hierarchical coordination should outperform implicit "
    "coordination.** The 30x gap (48.5% vs 1.5%) shows that the "
    "overhead of centralized control and message-passing harms "
    "rather than helps performance on constraint-satisfaction "
    "tasks under the locality conditions of meeting-room "
    "scheduling.",
    title="Result: 30x gap directly contradicts the prevailing 'explicit orchestration is necessary' assumption",
)

# ---------------------------------------------------------------------------
# 6.7 Convergence speed (Table 9)
# ---------------------------------------------------------------------------

claim_table_9_convergence_speed = claim(
    "**Table 9: Average ticks to solution by difficulty (solved "
    "cases only).**\n\n"
    "| Strategy | Easy | Medium | Hard |\n"
    "|---|---|---|---|\n"
    "| Pressure-field | 17.8 (n=78) | 34.6 (n=39) | 32.3 (n=14) |\n"
    "| Conversation | 29.4 (n=30) | -- | -- |\n"
    "| Hierarchical | 40.0 (n=4) | -- | -- |\n\n"
    "Dashes indicate no solved cases. On easy problems, pressure-"
    "field solves $1.65\\times$ faster than conversation and "
    "$2.2\\times$ faster than hierarchical.",
    title="Table 9: ticks-to-solution -- pressure-field 17.8 vs conversation 29.4 (1.65x) vs hierarchical 40.0 (2.2x) on easy",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 9 (page 35)",
    },
)

claim_solvability_is_limiting_factor_on_hard = claim(
    "**On hard problems, solvability rather than convergence speed "
    "is the limiting factor.** Pressure-field's convergence speed "
    "on hard problems (32.3 ticks for the 14 solved cases) is "
    "comparable to medium (34.6 ticks for 39 solved cases). The "
    "hard problems that *do* get solved converge at similar rates "
    "to medium ones; the bimodal pattern -- fast convergence when "
    "solvable, complete failure otherwise -- suggests that **model "
    "capability rather than search time is the limiting factor on "
    "hard problems**.",
    title="Result: bimodal hard-problem behavior -- when solvable, convergence is fast (~32 ticks); when not, complete failure (model capability is the bottleneck)",
)

# ---------------------------------------------------------------------------
# 6.8 Final pressure analysis (Table 10)
# ---------------------------------------------------------------------------

claim_table_10_final_pressure = claim(
    "**Table 10: Average final pressure by difficulty (lower is "
    "better).**\n\n"
    "| Strategy | Easy | Medium | Hard |\n"
    "|---|---|---|---|\n"
    "| Pressure-field | 0.13 | 1.02 | 2.48 |\n"
    "| Conversation | 26.5 | 59.3 | 92.2 |\n"
    "| Hierarchical | 28.6 | 59.4 | 88.0 |\n\n"
    "Pressure-field achieves $\\sim 200\\times$ lower final "
    "pressure on easy, $\\sim 57\\times$ lower on medium, and "
    "$\\sim 35\\times$ lower on hard, compared to conversation and "
    "hierarchical baselines. Even when pressure-field does not "
    "fully solve a problem, it reaches a much higher-quality "
    "partial solution.",
    title="Table 10: final pressure -- pressure-field 0.13 / 1.02 / 2.48 vs conversation 26.5 / 59.3 / 92.2 (200x / 57x / 35x lower)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 10 (page 36)",
    },
)

# ---------------------------------------------------------------------------
# 6.9 Token efficiency (Tables 11-13)
# ---------------------------------------------------------------------------

claim_table_11_token_per_trial = claim(
    "**Table 11: Average token usage per trial.**\n\n"
    "| Strategy | Prompt | Completion | Total |\n"
    "|---|---|---|---|\n"
    "| Pressure-field | 532,106 | 85,165 | 617,271 |\n"
    "| Conversation | 154,845 | 6,626 | 161,472 |\n"
    "| Hierarchical | 32,662 | 5,424 | 38,087 |\n"
    "| Sequential | 40,667 | 5,239 | 45,906 |\n"
    "| Random | 41,227 | 5,253 | 46,480 |\n\n"
    "Pressure-field uses about $4\\times$ more tokens per trial "
    "than conversation due to parallel multi-agent execution.",
    title="Table 11: tokens per trial -- pressure-field 617K vs conversation 161K (~4x higher)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 11 (page 36)",
    },
)

claim_table_12_token_per_solve = claim(
    "**Table 12: Token efficiency per successful solve (270 trials "
    "each).**\n\n"
    "| Strategy | Total tokens | Solves | Tokens/solve |\n"
    "|---|---|---|---|\n"
    "| Pressure-field | 166.7 M | 131 | **1.27 M** |\n"
    "| Conversation | 43.6 M | 30 | 1.45 M |\n\n"
    "Pressure-field requires **1.27 M tokens per solve vs "
    "conversation's 1.45 M -- a 12% better cost per successful "
    "outcome**. The apparent per-trial cost disadvantage inverts "
    "when normalizing by success rate.",
    title="Table 12: tokens per solve -- pressure-field 1.27M vs conversation 1.45M (12% more efficient when normalized by success)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 12 (page 37)",
    },
)

claim_table_13_solved_unsolved_split = claim(
    "**Table 13: Average tokens by outcome (solved vs unsolved).**\n\n"
    "| Strategy | Solved trials | Unsolved trials |\n"
    "|---|---|---|\n"
    "| Pressure-field | 318K (n=131) | 900K (n=139) |\n"
    "| Conversation | 78K (n=30) | 172K (n=240) |\n\n"
    "Solved trials terminate early (use fewer tokens). Pressure-"
    "field's $2.8\\times$ gap between solved (318K) and unsolved "
    "(900K) reflects the cost of exhaustive exploration when a "
    "problem proves intractable. Conversation's smaller "
    "($2.2\\times$) gap indicates less intensive search -- which "
    "may explain its lower solve rate on difficult problems.",
    title="Table 13: tokens by outcome -- pressure-field 318K solved / 900K unsolved (2.8x); conversation 78K / 172K (2.2x)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 13 (page 37)",
    },
)

claim_escalation_as_cost_control = claim(
    "**Band-and-model escalation acts as an implicit cost-control "
    "mechanism.** The system begins with cheap exploration: small "
    "models (0.5b) and exploitation-focused sampling. Tokens are "
    "spent on larger models and broader exploration *only when "
    "pressure stagnates* -- that is, when the problem actually "
    "requires more capable search. Easy problems that solve "
    "quickly never trigger escalation, consuming only baseline "
    "tokens. The 4x per-trial cost difference reflects the "
    "*average* across difficulty levels; on easy problems where "
    "pressure-field solves 86.7% of instances, most trials "
    "terminate before expensive escalation occurs.",
    title="Result: escalation = implicit cost control (escalation only when pressure stagnates; easy problems never escalate)",
)

__all__ = [
    "claim_table_3_aggregate_solve_rates",
    "claim_pressure_vs_conversation_4x",
    "claim_pressure_vs_hierarchical_30x",
    "claim_conversation_intermediate",
    "claim_hierarchical_sequential_random_fail",
    "claim_effect_sizes_large",
    "claim_result_contradicts_explicit_orchestration_assumption",
    "claim_table_9_convergence_speed",
    "claim_solvability_is_limiting_factor_on_hard",
    "claim_table_10_final_pressure",
    "claim_table_11_token_per_trial",
    "claim_table_12_token_per_solve",
    "claim_table_13_solved_unsolved_split",
    "claim_escalation_as_cost_control",
]
