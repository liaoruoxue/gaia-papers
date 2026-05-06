"""Section 6.3: Ablations -- temporal decay, inhibition, examples,
and negative pheromones. Section 6.4: Scaling experiments (1, 2, 4
agents). Section 6.5: band/model escalation analysis.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Sections 6.3-6.5
+ Tables 4-7 + Figures 2-3.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 6.3.1 Decay ablation (Table 4)
# ---------------------------------------------------------------------------

claim_table_4_decay_ablation = claim(
    "**Table 4: Decay ablation on easy scheduling problems (30 "
    "trials each).**\n\n"
    "| Configuration | Solved/N | Solve rate | 95% CI |\n"
    "|---|---|---|---|\n"
    "| Full (with decay) | 29/30 | **96.7%** | 83.3%-99.4% |\n"
    "| Without decay | 26/30 | 86.7% | 70.3%-94.7% |\n\n"
    "**Fisher's exact test:** $p = 0.35$ -- the 10 percentage-"
    "point difference is *not* statistically significant at "
    "$\\alpha = 0.05$. The non-significance reflects (i) limited "
    "$n = 30$ sample size and (ii) a ceiling effect -- the high "
    "baseline (96.7% with decay) leaves limited statistical room "
    "to detect improvement. The overlapping 95% confidence "
    "intervals (83.3%-99.4% vs 70.3%-94.7%) reflect this "
    "uncertainty.",
    title="Table 4: decay ablation -- 96.7% with decay vs 86.7% without on easy (delta = -10pp; Fisher's p = 0.35, not significant at n=30)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 4 (page 28)",
    },
)

claim_decay_ablation_mechanism = claim(
    "**Mechanistic explanation for the decay-ablation effect.** "
    "Without decay, fitness saturates after the initial round of "
    "patches: regions that received early patches retain high "
    "fitness indefinitely, making them appear 'stable' even when "
    "they still contain unscheduled meetings. Since greedy "
    "selection prioritizes high-pressure regions, these "
    "prematurely-stabilized regions are never reconsidered. **This "
    "mechanism is consistent with the Basin Separation result "
    "(Theorem 5.3)**: without decay, agents may remain trapped in "
    "the first stable basin they reach.",
    title="Mechanism: without decay, agents are trapped in the first stable basin (consistent with Theorem 5.3 Basin Separation)",
)

# ---------------------------------------------------------------------------
# 6.3.2 Full ablation matrix (Table 5)
# ---------------------------------------------------------------------------

claim_table_5_full_ablation = claim(
    "**Table 5: Full ablation matrix (30 trials each on easy "
    "difficulty).**\n\n"
    "| Configuration | Decay | Inhibition | Examples | Solve rate |\n"
    "|---|---|---|---|---|\n"
    "| Full | YES | YES | YES | **96.7%** |\n"
    "| No Decay | NO | YES | YES | 86.7% |\n"
    "| No Inhibition | YES | NO | YES | 96.7% |\n"
    "| No Examples | YES | YES | NO | 90.0% |\n"
    "| Baseline | NO | NO | NO | 90.0% |\n\n"
    "**Per-feature contributions (Full vs single feature removed):** "
    "Decay = +10.0% (96.7% vs 86.7%); Inhibition = +0.0% (no "
    "detectable effect); Examples = +6.7% (96.7% vs 90.0%). The "
    "differences do not reach statistical significance at $n = 30$.",
    title="Table 5: full ablation -- decay +10pp / inhibition +0pp / examples +6.7pp (none significant at n=30 on easy)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 5 (page 29)",
    },
)

claim_inhibition_no_effect_explanation = claim(
    "**Why inhibition shows no detectable effect in this domain.** "
    "Inhibition contributes 0 percentage points to the Full vs "
    "No-Inhibition comparison (both 96.7%). The likely reason is "
    "the **50-tick budget**: it provides sufficient exploration "
    "without explicit cooldowns, so the inhibition mechanism's "
    "anti-oscillation benefit is not exposed within the budget. "
    "Inhibition would likely matter more under tighter tick "
    "budgets or harder problems where oscillation around local "
    "fixes consumes a meaningful fraction of the budget.",
    title="Explanation: inhibition's 0pp effect on easy problems is plausibly due to the generous 50-tick budget masking anti-oscillation benefit",
)

# ---------------------------------------------------------------------------
# 6.4 Scaling experiments (Table 6)
# ---------------------------------------------------------------------------

claim_table_6_scaling = claim(
    "**Table 6: Pressure-field scaling from 1 to 4 agents (easy "
    "difficulty, 30 trials each).**\n\n"
    "| Agents | Solved/N | Rate | 95% CI |\n"
    "|---|---|---|---|\n"
    "| 1 | 25/30 | 83.3% | 66.4%-92.7% |\n"
    "| 2 | 28/30 | 93.3% | 78.7%-98.2% |\n"
    "| 4 | 25/30 | 83.3% | 66.4%-92.7% |\n\n"
    "Performance remains stable across agent counts. The slight "
    "peak at 2 agents (93.3%) is within CI overlap of 1 and 4 "
    "agents, indicating no significant agent-count effect. **This "
    "validates Theorem 5.4: coordination overhead remains $O(1)$, "
    "enabling effective scaling**.",
    title="Table 6: scaling stable across 1/2/4 agents on easy (83.3% / 93.3% / 83.3%; validates Theorem 5.4 O(1) coordination)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 6 (page 31)",
    },
)

# ---------------------------------------------------------------------------
# 6.5 Escalation: FM-MAS symbiosis in practice
# ---------------------------------------------------------------------------

claim_escalation_implements_exploitation_exploration = claim(
    "**Escalation implements ant-colony exploitation-exploration "
    "balance.** Ant colonies abandon stale pheromone trails and "
    "resume random exploration when a food source depletes. The "
    "escalation mechanism instantiates this same principle through "
    "two complementary dynamics: (i) **Band escalation** governs "
    "the exploitation-exploration trade-off *within a single model* "
    "by shifting sampling parameters from low temperature "
    "(exploitation) to high temperature (exploration) when "
    "pressure velocity stalls. (ii) **Model escalation** addresses "
    "a different failure mode -- when exploration within a model's "
    "capability envelope fails, the system recruits more capable "
    "FMs (0.5b -> 1.5b -> 3b).",
    title="Result: band escalation = within-model exploit/explore; model escalation = across-capability recruitment (mirrors ant-colony pheromone dynamics)",
)

claim_escalation_demonstrates_fm_mas_symbiosis = claim(
    "**Escalation makes FM-MAS symbiosis concrete.** The MAS "
    "coordination mechanism (pressure-field) adaptively invokes "
    "higher-capability FMs based on **pressure signals alone** -- "
    "no explicit task decomposition is needed. Stagnant pressure "
    "velocity is sufficient signal that current capabilities are "
    "insufficient. **FM contribution**: each model tier provides "
    "broad solution coverage without explicit action enumeration. "
    "**MAS contribution**: the pressure gradient provides the "
    "objective criterion for *when* to escalate; no heuristics "
    "about 'problem difficulty' are needed.",
    title="Result: escalation = concrete FM-MAS symbiosis (FM provides coverage; MAS provides the when-to-escalate criterion via pressure signal)",
)

# ---------------------------------------------------------------------------
# 6.3.3 negative pheromones (mechanism description; result is qualitative)
# ---------------------------------------------------------------------------

claim_negative_pheromones_design = claim(
    "**Negative pheromones are designed with positive language to "
    "fit small-model instruction-following.** When agents "
    "repeatedly propose ineffective patches and pressure stays at "
    "maximum, the system accumulates rejection history. Unlike the "
    "'AVOID' framing that small (1.5b parameter) models struggle "
    "to follow, rejected empty-room patches are rephrased as "
    "**positive language**: 'TIP: Schedule meetings in Room A "
    "(improves by X)' -- reframing what *not* to do as what *to "
    "try* instead. This is a deliberate design choice to match the "
    "instruction-following capabilities of weak models.",
    title="Mechanism: negative pheromones use positive-language reframing to accommodate small-model instruction-following limits",
)

__all__ = [
    "claim_table_4_decay_ablation",
    "claim_decay_ablation_mechanism",
    "claim_table_5_full_ablation",
    "claim_inhibition_no_effect_explanation",
    "claim_table_6_scaling",
    "claim_escalation_implements_exploitation_exploration",
    "claim_escalation_demonstrates_fm_mas_symbiosis",
    "claim_negative_pheromones_design",
]
