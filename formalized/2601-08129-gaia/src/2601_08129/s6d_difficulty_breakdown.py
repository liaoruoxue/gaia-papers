"""Section 6.6: Difficulty-tier breakdown -- per-tier solve rates,
the widening-gap pattern, the 'only pressure-field scales' finding.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 6.6 +
Table 8 + Figure 1.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Table 8: per-difficulty solve rates
# ---------------------------------------------------------------------------

claim_table_8_difficulty_breakdown = claim(
    "**Table 8: Solve rate by difficulty level (90 trials each per "
    "difficulty, 270 per strategy total).**\n\n"
    "| Difficulty | Pressure-field | Conversation | Hierarchical | Sequential / Random |\n"
    "|---|---|---|---|---|\n"
    "| Easy | **86.7% (78/90)** | 33.3% (30/90) | 4.4% (4/90) | 1.1% (1/90) |\n"
    "| Medium | **43.3% (39/90)** | 0.0% (0/90) | 0.0% (0/90) | 0.0% (0/90) |\n"
    "| Hard | **15.6% (14/90)** | 0.0% (0/90) | 0.0% (0/90) | 0.0% (0/90) |\n"
    "| **Total** | **48.5% (131/270)** | 11.1% (30/270) | 1.5% (4/270) | 0.4% (1/270) |\n",
    title="Table 8: per-difficulty solve rates -- pressure-field 86.7/43.3/15.6 vs all baselines 0% on medium/hard",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 8 (page 33)",
    },
)

# ---------------------------------------------------------------------------
# Per-difficulty headline claims (used for induction over difficulty tiers)
# ---------------------------------------------------------------------------

claim_easy_pressure_field_86_7 = claim(
    "**Easy difficulty: pressure-field 86.7% (78/90).** On easy "
    "problems (3 rooms, 20 meetings, 70% pre-scheduled), pressure-"
    "field achieves 86.7% solve rate. This is the highest absolute "
    "solve rate the strategy reaches across difficulty tiers and "
    "leaves substantial headroom (less than 100% to find).",
    title="Per-tier observation: easy difficulty -- pressure-field 86.7% (78/90)",
)

claim_easy_conversation_33_3 = claim(
    "**Easy difficulty: conversation 33.3% (30/90).** On easy "
    "problems, conversation is the next-best baseline at 33.3% "
    "solve rate. The 53.4 percentage-point gap (86.7% vs 33.3%) "
    "exceeds Cohen's large-effect threshold ($h > 0.8$).",
    title="Per-tier observation: easy difficulty -- conversation 33.3% (next-best baseline; gap = 53.4 pp)",
)

claim_easy_hierarchical_4_4 = claim(
    "**Easy difficulty: hierarchical 4.4% (4/90).** Hierarchical "
    "solves only 4.4% of easy problems, comparable to sequential / "
    "random baselines (1.1%). Despite explicit coordination, "
    "hierarchical's solve rate on easy problems is in the same "
    "order of magnitude as random selection.",
    title="Per-tier observation: easy difficulty -- hierarchical 4.4% (comparable to random)",
)

claim_medium_pressure_field_43_3 = claim(
    "**Medium difficulty: pressure-field 43.3% (39/90), all "
    "baselines 0%.** On medium problems (5 rooms, 40 meetings, 50% "
    "pre-scheduled), pressure-field solves 43.3% while every other "
    "strategy (conversation, hierarchical, sequential, random) "
    "scores exactly 0/90. The gap is *absolute* -- a problem class "
    "no baseline solves at all.",
    title="Per-tier observation: medium difficulty -- pressure-field 43.3%, all baselines 0% (absolute gap)",
)

claim_hard_pressure_field_15_6 = claim(
    "**Hard difficulty: pressure-field 15.6% (14/90), all "
    "baselines 0%.** On hard problems (5 rooms, 60 meetings, 30% "
    "pre-scheduled), pressure-field solves 15.6% while every other "
    "strategy scores exactly 0/90. Even at the hardest tier, "
    "pressure-field maintains a meaningful (non-zero, double-"
    "digit) solve rate.",
    title="Per-tier observation: hard difficulty -- pressure-field 15.6%, all baselines 0%",
)

# ---------------------------------------------------------------------------
# Aggregate cross-tier claims about scaling pattern
# ---------------------------------------------------------------------------

claim_only_pressure_field_scales = claim(
    "**Pressure-field is the only strategy that scales to harder "
    "problems.** While all strategies degrade on harder problems, "
    "pressure-field maintains meaningful solve rates (43.3% medium, "
    "15.6% hard) where every other baseline collapses to 0%. This "
    "pattern is the empirical signature of the locality-aware "
    "coordination thesis: when problems exhibit locality, "
    "decentralized greedy optimization continues to find solutions "
    "where centralized / dialogue-based / random approaches fail "
    "outright.",
    title="Result: pressure-field is the only strategy with non-zero solve rate on medium and hard (cross-tier scaling property)",
)

claim_gap_widens_with_difficulty = claim(
    "**The pressure-field-vs-baseline gap widens with difficulty.** "
    "On easy problems, pressure-field leads conversation by 53.4 "
    "percentage points (86.7% vs 33.3%). On medium and hard "
    "problems, the gap becomes *absolute*: pressure-field solves "
    "problems no baseline can solve at all (43.3% vs 0% on medium; "
    "15.6% vs 0% on hard). Higher difficulty does not narrow the "
    "advantage; it amplifies it.",
    title="Result: pressure-field-vs-baseline gap widens with difficulty (53.4pp on easy -> absolute gap on medium/hard)",
)

# ---------------------------------------------------------------------------
# Figure 1 visual claim
# ---------------------------------------------------------------------------

claim_figure_1_visual = claim(
    "**Figure 1 visual claim.** Pressure-field outperforms every "
    "baseline at every difficulty level; on medium and hard "
    "problems, only pressure-field achieves non-zero solve rates. "
    "The bar chart with 95% Wilson confidence intervals shows "
    "non-overlapping CIs between pressure-field and every other "
    "strategy at every difficulty.",
    title="Result (Fig. 1): pressure-field dominates at every difficulty; non-overlapping CIs vs every baseline",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Fig. 1 (page 27)",
        "caption": "Fig. 1: Strategy comparison by difficulty level. Error bars show 95% Wilson CIs. Pressure-field outperforms all baselines at every difficulty level.",
    },
)

__all__ = [
    "claim_table_8_difficulty_breakdown",
    "claim_easy_pressure_field_86_7",
    "claim_easy_conversation_33_3",
    "claim_easy_hierarchical_4_4",
    "claim_medium_pressure_field_43_3",
    "claim_hard_pressure_field_15_6",
    "claim_only_pressure_field_scales",
    "claim_gap_widens_with_difficulty",
    "claim_figure_1_visual",
]
