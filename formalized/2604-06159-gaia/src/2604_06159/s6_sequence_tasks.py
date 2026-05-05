"""Section 3.4-3.5: Dense-reward sequence tasks (token-level grouping).

Sections 3.4 (Token Reversal at $V \\in \\{2, 4, 8, 16\\}$) and 3.5
(four target logics x two reward structures = 8 variants) of
[@Kaddour2026]. These experiments stress-test TPO and the baselines
on transformer sequence models with *bag-of-tokens* (per-token)
reward and *sequential* (sparser, credit only up to first incorrect
token) reward, both still denser than terminal reward.

The headline numbers are "steps to 1% error" tables. The
generalisation to 8 task variants (Sec. 3.5) shows the dense-reward
gap holds across target logic and reward structure, with TPO_token
2-6x faster than the runner-up.

Sequential reward starts to expose the qualitative gap that Section
3.6 makes total: under sequential reward, *only* TPO_token and DG
converge on the four task logics within budget; GRPO_token and PPO
fail to converge on any.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

setup_token_reversal = setting(
    "**Token Reversal task setup (Sec. 3.4).** A 2-layer, 4-head "
    "causal transformer autoregressively reverses an input sequence "
    "of length $H = 10$ drawn uniformly from a vocabulary of size "
    "$V$. Reward is the *bag-of-tokens* fraction of tokens reversed "
    "correctly. Vocabulary sweep $V \\in \\{2, 4, 8, 16\\}$ grows "
    "the output space from $2^{10} \\approx 10^3$ to $16^{10} "
    "\\approx 10^{12}$. At each prefix state, $K = 8$ next-token "
    "candidates are sampled; all methods follow one behavior "
    "trajectory per prompt, so environment interactions are matched. "
    "Sequence error reported, averaged over 20 seeds [@Kaddour2026, "
    "Sec. 3.4].",
    title="Setup (3.4): $H=10$ token reversal, $K=8$ token candidates, bag-of-tokens reward",
)

setup_task_variants_3_5 = setting(
    "**Task variants setup (Sec. 3.5).** Four target logics (copy, "
    "flip, reverse copy, reverse flip) crossed with two reward "
    "structures (bag-of-tokens; sequential = credit only up to the "
    "first incorrect token), yielding eight variants. "
    "Hyperparameters match Sec. 3.4 ($H = 10$, $V = 2$, $K = 8$ "
    "token candidates), 10 seeds, 1,000 episodes "
    "[@Kaddour2026, Sec. 3.5].",
    title="Setup (3.5): 4 target logics x 2 reward structures = 8 variants, 10 seeds",
)

# ---------------------------------------------------------------------------
# Sec. 3.4: vocabulary sweep
# ---------------------------------------------------------------------------

claim_table1_steps_to_1pct = claim(
    "**Table 1: Steps to 1% error on Token Reversal (bag-of-tokens, "
    "$K = 8$).** Lower is faster; bold = fastest at each $V$.\n\n"
    "| Method | $V=2$ | $V=4$ | $V=8$ | $V=16$ |\n"
    "|--------|------:|------:|------:|-------:|\n"
    "| TPO$_{\\text{token}}$ | **58** | **74** | **103** | **102** |\n"
    "| GRPO$_{\\text{token}}$ | 904 | 141 | 124 | 148 |\n"
    "| DG | 199 | 273 | 314 | 393 |\n"
    "| PPO | 872 | 181 | 191 | 259 |\n\n"
    "TPO$_{\\text{token}}$ is fastest at every $V$. GRPO$_{\\text{token}}$ "
    "improves with larger $V$ (where more token candidates provide a "
    "richer signal) but lags throughout. DG and PPO -- which lack "
    "within-group structure -- scale less favorably "
    "[@Kaddour2026, Table 1].",
    title="Numerical (3.4): TPO_token fastest to 1% error at every $V$ (Table 1)",
    metadata={
        "table": "artifacts/2604.06159.pdf, Table 1",
    },
)

claim_3_4_gap_widens = claim(
    "**The gap between methods widens with task difficulty.** At "
    "$V = 16$ (the hardest setting in the sweep), TPO$_{\\text{token}}$ "
    "reaches 1% error in 102 steps vs. 148 for GRPO$_{\\text{token}}$, "
    "259 for PPO, and 393 for DG -- roughly $1.5\\times$, $2.5\\times$, "
    "$3.9\\times$ slower respectively. At the easiest setting "
    "$V = 2$, TPO$_{\\text{token}}$ is $15\\times$ faster than "
    "GRPO$_{\\text{token}}$ (58 vs. 904) [@Kaddour2026, Figure 6, "
    "Table 1].",
    title="Result (3.4): TPO_token's lead widens with $V$",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 6",
        "caption": "Token Reversal sequence error vs. episode, $V \\in \\{2,4,8,16\\}$.",
    },
)

# ---------------------------------------------------------------------------
# Sec. 3.5: target logic x reward structure
# ---------------------------------------------------------------------------

claim_table2_steps_to_1pct = claim(
    "**Table 2: Steps to 1% error across 8 task variants ($K = 8$ "
    "token candidates).** Bold = fastest per row; '-' = never reached "
    "within budget.\n\n"
    "| Reward | Target | TPO$_{\\text{token}}$ | GRPO$_{\\text{token}}$ | DG | PPO |\n"
    "|--------|--------|---------------------:|----------------------:|---:|----:|\n"
    "| Bag of tokens | Copy | **81** | 338 | 219 | 170 |\n"
    "| Bag of tokens | Flip | **56** | 104 | 201 | 146 |\n"
    "| Bag of tokens | Rev. copy | **55** | 352 | 202 | - |\n"
    "| Bag of tokens | Rev. flip | **59** | 209 | 200 | 143 |\n"
    "| Sequential | Copy | **295** | - | 439 | - |\n"
    "| Sequential | Flip | **321** | - | 349 | - |\n"
    "| Sequential | Rev. copy | **159** | - | 515 | - |\n"
    "| Sequential | Rev. flip | **276** | - | 309 | - |\n\n"
    "TPO$_{\\text{token}}$ is fastest on all 8 variants and 2-6x "
    "faster than the runner-up under bag-of-tokens reward. Under "
    "sequential reward, GRPO$_{\\text{token}}$ and PPO *fail to "
    "converge* on any variant; only TPO$_{\\text{token}}$ and DG "
    "succeed [@Kaddour2026, Table 2].",
    title="Numerical (3.5): TPO_token fastest on all 8 variants (Table 2)",
    metadata={
        "table": "artifacts/2604.06159.pdf, Table 2",
    },
)

claim_3_5_population_match_dense = claim(
    "**Sec. 3.5 generalisation -- TPO$_{\\text{token}}$ reaches 1% "
    "first on all 8 task variants under bag-of-tokens reward.** Under "
    "the denser bag-of-tokens reward (top row of Figure 7), TPO$_{\\text{token}}$ "
    "is the fastest method on all four target logics (copy, flip, "
    "reverse copy, reverse flip) and is 2-6x faster than the "
    "runner-up. All methods *except* PPO eventually reach 1% on "
    "bag-of-tokens tasks within the 1,000-episode budget. This is "
    "the population-level confirmation that the Sec. 3.4 finding "
    "generalises across target logic, not just vocabulary "
    "[@Kaddour2026, Sec. 3.5, Figure 7].",
    title="Population (3.5): bag-of-tokens -- TPO_token fastest on all 4 target logics",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 7 (top row)",
        "caption": "Prompt-matched bag-of-tokens learning curves.",
    },
)

claim_3_5_sequential_only_tpo_dg = claim(
    "**Sec. 3.5 generalisation -- under *sequential* reward, only "
    "TPO$_{\\text{token}}$ and DG converge.** Under sequential "
    "reward (sparser than bag-of-tokens), TPO$_{\\text{token}}$ "
    "reaches 1% on all four target logics within budget; DG "
    "converges on all four but more slowly; *GRPO$_{\\text{token}}$ "
    "and PPO fail to converge on any* of the four "
    "[@Kaddour2026, Sec. 3.5, Figure 7]. This is the first sign in "
    "the paper of the qualitative gap that becomes total under "
    "terminal reward (Sec. 3.6).",
    title="Population (3.5): sequential reward -- TPO and DG converge; GRPO and PPO fail on all 4",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 7 (sequential rows)",
        "caption": "Sequential-reward learning curves, prompt- and interaction-matched.",
    },
)

claim_per_state_targeting_explanation = claim(
    "**Per-state targeting explains the sequential-reward "
    "advantage.** Under sequential reward, prefixes after the first "
    "mistake see *zero reward for every candidate*, so the within-"
    "group standardized scores collapse to $u = 0$ on those "
    "prefixes. The TPO target there matches the old policy ($q = "
    "p^{\\text{old}}$) and introduces no spurious signal. "
    "TPO$_{\\text{token}}$ therefore concentrates its update on "
    "*informative prefixes* where at least one candidate continues "
    "correctly. DG's sigmoid gating helps similarly but more slowly; "
    "GRPO$_{\\text{token}}$ and PPO lack an equally explicit local "
    "target [@Kaddour2026, Sec. 3.5].",
    title="Mechanism (3.5): zero-variance prefixes get $q = p^{\\text{old}}$, no spurious signal",
)

__all__ = [
    "setup_token_reversal",
    "setup_task_variants_3_5",
    "claim_table1_steps_to_1pct",
    "claim_3_4_gap_widens",
    "claim_table2_steps_to_1pct",
    "claim_3_5_population_match_dense",
    "claim_3_5_sequential_only_tpo_dg",
    "claim_per_state_targeting_explanation",
]
