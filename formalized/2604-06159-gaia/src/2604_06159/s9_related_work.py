"""Section 5: Related work and the comparison table.

Section 5 of [@Kaddour2026]. The paper situates TPO against five
families of methods and consolidates the comparison in Table 4. Key
positioning claims:

* Target-matching / mirror-descent family (REPS, MPO, V-MPO, AWR,
  MDPO, regularised MDPs): TPO uses the same exponential tilt but
  uniquely solves it in *closed form* on the finite candidate set
  -- no critic, no inner loop. AWR uses the same weight but as a
  scalar on log-likelihood, so its gradient does not self-extinguish
  at the target.

* Group-based PG (RLOO, GRPO, Dr.GRPO, DAPO, GSPO): all convert
  group scores into per-sample scalar weights inside a PG objective.
  TPO replaces this with one target distribution on the simplex,
  avoiding importance ratios and clipping entirely.

* Single-sample PG (REINFORCE, TRPO, PPO, REINFORCE++, ReMax): all
  scalar-weighted advantage updates. DG corrects gradient
  misallocation *across* contexts; TPO addresses misallocation
  *within* a context's candidate set; the two are complementary.

* Regression / preference (REBEL, PMPO, DPO, KTO, IPO): different
  loss families.

* Objective corrections (MaxRL, GDPO, MT-GRPO): change *which*
  objective is optimised; TPO changes *how* signals become updates.

* Off-policy / async (ScaleRL, IcePop): orthogonal axis.

The Table 4 row for TPO is "$q \\propto p^{\\text{old}} \\exp(u)$;
CE to $q$" with checkmarks for Group, no Critic, no Fixed reference.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: the comparison Table 4
# ---------------------------------------------------------------------------

setup_table4_axes = setting(
    "**Table 4 axes (definitions).** *Group*: the update structurally "
    "compares candidates within a context (TPO, RLOO, GRPO, REBEL, "
    "PMPO, MPO/V-MPO, MaxRL: yes; everything else: no). *Critic*: "
    "requires a learned $Q$- or $V$-function (AWR, MPO/V-MPO: yes; "
    "TPO and most others: no). *Fixed ref.*: requires a frozen "
    "reference model beyond $\\pi^{\\text{old}}$ (REINFORCE++, ReMax, "
    "PMPO: yes; TPO: no, only $\\pi^{\\text{old}}$ anchor) "
    "[@Kaddour2026, Table 4].",
    title="Setup (5): Table 4 axes = Group / Critic / Fixed ref.",
)

# ---------------------------------------------------------------------------
# Family 1: target-matching / mirror-descent
# ---------------------------------------------------------------------------

claim_target_matching_family = claim(
    "**Target-matching / mirror-descent family.** REPS [@Peters2010REPS], "
    "MPO [@Abdolmaleki2018MPO], V-MPO [@Song2020VMPO], AWR "
    "[@Peng2019AWR], MDPO [@Tomar2022MDPO], and the broader "
    "regularised-MDP framework [@Kakade2001NPG; @Geist2019RegMDP] "
    "all use the same exponential-tilting step. TPO's distinguishing "
    "structural property is that the *finite scored candidate set "
    "provides the target in closed form*, without a critic or inner "
    "optimization loop. AWR uses the same exponential weight but "
    "treats $\\exp(A/\\beta)$ as a *fixed scalar* on each sample's "
    "log-likelihood, so its gradient does not self-extinguish at the "
    "target [@Kaddour2026, Sec. 5].",
    title="Related (5): target-matching family; TPO's USP is closed-form $q$ on the candidate simplex",
)

claim_tpo_kl_regularised_operator = claim(
    "**TPO as a KL-regularised improvement operator.** More "
    "generally, TPO can be read as a KL-regularised policy-"
    "improvement operator on the *sampled candidate simplex* rather "
    "than the full action space. This distinguishes it from the "
    "regularised-MDP framework [@Kakade2001NPG; @Geist2019RegMDP], "
    "which acts on the full action space. The candidate-simplex "
    "restriction is what makes the closed form possible "
    "[@Kaddour2026, Sec. 5].",
    title="Related (5): TPO = KL-regularised improvement op on the candidate simplex",
)

# ---------------------------------------------------------------------------
# Family 2: group-based PG
# ---------------------------------------------------------------------------

claim_group_based_pg_family = claim(
    "**Group-based PG family.** RLOO [@Ahmadian2024RLOO] and GRPO "
    "[@Shao2024GRPO] also score multiple candidates per context, but "
    "convert them into per-sample scalar weights inside a PG "
    "objective. TPO instead builds a *target distribution* on the "
    "candidate simplex and fits the policy to it. Recent GRPO "
    "variants address specific failure modes while remaining scalar-"
    "weighted PG: Dr.GRPO [@Liu2025DrGRPO] removes a difficulty bias "
    "from within-group $\\sigma$-normalization [@Murphy2025RL]; DAPO "
    "[@Yu2025DAPO] uses asymmetric clipping to prevent entropy "
    "collapse; GSPO [@Zheng2025GSPO] fixes a per-token importance-"
    "ratio mismatch when rewards are trajectory-level. TPO replaces "
    "the scalar-weighted update with a single target distribution, "
    "avoiding importance ratios and clipping entirely "
    "[@Kaddour2026, Sec. 5].",
    title="Related (5): TPO replaces scalar PG weights with a single target distribution",
)

claim_difficulty_bias_residual = claim(
    "**Caveat -- difficulty-bias effects can remain in TPO.** "
    "Because TPO still standardizes within-group scores, the same "
    "difficulty-bias effects identified for GRPO (low-variance "
    "groups produce sharp targets after $z$-scoring; "
    "[@Liu2025DrGRPO; @Murphy2025RL]) can in principle remain. The "
    "paper acknowledges this in Section 6 (Limitations).",
    title="Related (5): TPO inherits potential low-variance difficulty bias (within-group $z$-scoring)",
)

# ---------------------------------------------------------------------------
# Family 3: single-sample PG and DG
# ---------------------------------------------------------------------------

claim_single_sample_pg_family = claim(
    "**Single-sample PG family.** REINFORCE [@Williams1992REINFORCE], "
    "TRPO [@Schulman2015TRPO], PPO [@Schulman2017PPO], REINFORCE++ "
    "[@Hu2025REINFORCEpp], and ReMax [@Li2024ReMax] all assign scalar "
    "advantage weights to sampled actions. ReMax removes the value "
    "model and uses a greedy-decode baseline, yielding large memory "
    "and speed gains over PPO, but the gradient remains the standard "
    "score-function estimator [@Kaddour2026, Sec. 5].",
    title="Related (5): single-sample PG = scalar-weighted score-function estimators",
)

claim_dg_complementary_axis = claim(
    "**TPO and DG address complementary misallocation axes.** DG "
    "[@Osband2026] corrects gradient misallocation *across* contexts "
    "via sigmoid gating; TPO addresses misallocation *within* a "
    "context's candidate set via the target distribution. The two "
    "are complementary and can be composed [@Kaddour2026, Sec. 5].",
    title="Related (5): TPO is *within*-context, DG is *across*-context -- complementary",
)

# ---------------------------------------------------------------------------
# Family 4: regression / preference
# ---------------------------------------------------------------------------

claim_regression_preference_family = claim(
    "**Regression and preference families.** REBEL [@Gao2024REBEL] "
    "reduces RL to iterative least-squares regression on reward "
    "differences between paired completions, generalising NPG with "
    "strong agnostic regret bounds. Both REBEL and TPO construct a "
    "target from rewards and the behavior policy, but differ in loss "
    "and structure: REBEL uses squared loss on log-probability ratios "
    "over *pairs*; TPO uses cross-entropy on a distribution over a "
    "*candidate group*. PMPO [@Abdolmaleki2025PMPO] is the closest "
    "target-matching method: it partitions candidates into "
    "accepted/rejected sets and regularises toward a frozen "
    "$\\pi_{\\text{ref}}$, whereas TPO keeps a single soft target "
    "over the *full* group and anchors only to $\\pi^{\\text{old}}$. "
    "Offline pairwise methods (DPO [@Rafailov2023DPO], KTO "
    "[@Ethayarajh2024KTO], IPO [@Azar2024IPO]) are more distant -- "
    "TPO is online, *setwise*, and scorer-agnostic "
    "[@Kaddour2026, Sec. 5].",
    title="Related (5): REBEL/PMPO/DPO/KTO/IPO; TPO is online, setwise, scorer-agnostic",
)

# ---------------------------------------------------------------------------
# Family 5: objective-level corrections
# ---------------------------------------------------------------------------

claim_objective_corrections_family = claim(
    "**Objective-level corrections.** MaxRL [@Tajwar2026MaxRL] "
    "changes *which* objective is optimized (higher-order corrections "
    "under binary rewards). GDPO [@Liu2026GDPO] and MT-GRPO "
    "[@Ramesh2026MTGRPO] correct GRPO's objective for multi-reward "
    "and multi-task settings. TPO is *orthogonal*: it changes *how* "
    "within-context signals become updates. All four corrections are "
    "complementary and could in principle be composed with TPO "
    "[@Kaddour2026, Sec. 5; Sec. 6].",
    title="Related (5): MaxRL/GDPO/MT-GRPO change *which* objective; TPO changes *how* signals -> updates",
)

# ---------------------------------------------------------------------------
# Family 6: off-policy / asynchronous
# ---------------------------------------------------------------------------

claim_off_policy_async_family = claim(
    "**Off-policy and asynchronous training.** Large-scale RL "
    "pipelines decouple rollout generation from parameter updates, "
    "introducing staleness and engine mismatch. ScaleRL "
    "[@Khatri2025ScaleRL] studies this regime and proposes truncated "
    "importance sampling for stabilisation; IcePop [@Team2025IcePop] "
    "addresses inference/training engine probability mismatches via "
    "engine-ratio masking. TPO's within-context correction is "
    "orthogonal to both and can be composed with either off-policy "
    "strategy [@Kaddour2026, Sec. 5].",
    title="Related (5): off-policy/async correction is orthogonal to TPO and composable",
)

__all__ = [
    "setup_table4_axes",
    "claim_target_matching_family",
    "claim_tpo_kl_regularised_operator",
    "claim_group_based_pg_family",
    "claim_difficulty_bias_residual",
    "claim_single_sample_pg_family",
    "claim_dg_complementary_axis",
    "claim_regression_preference_family",
    "claim_objective_corrections_family",
    "claim_off_policy_async_family",
]
