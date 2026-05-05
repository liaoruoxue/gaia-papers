"""Section 3 (preamble): Experimental setup, baselines, matching protocol.

Opening of Section 3 of [@Kaddour2026]. This module captures the
*shared* experimental setup that all sub-experiments (Sec. 3.1-3.8)
inherit: the baselines (PPO, GRPO, DG), the K-candidate grouping for
TPO and GRPO, the strengthened GRPO baseline (clipped surrogate +
z-scored advantages + reverse-KL penalty $\\beta=0.04$, Appendix F),
the prompt-matched vs. interaction-matched comparison protocol, and
the optimizer/learning-rate defaults (Optax Muon at $10^{-3}$,
$B=100$).

Per-experiment claims (per-task numbers, per-figure observations) are
in their own modules (s4-s8). This module isolates only the shared
methodological choices that are referenced as *background* throughout.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Baselines (definitions)
# ---------------------------------------------------------------------------

setup_baselines = setting(
    "**Baselines.** The paper compares TPO against three external "
    "policy-optimization baselines: PPO with the standard clipped "
    "surrogate [@Schulman2017PPO]; GRPO with group-relative z-scored "
    "advantages [@Shao2024GRPO]; and DG (Delightful Policy Gradients), "
    "Osband's sigmoid-gated PG variant [@Osband2026]. Plain PG "
    "(REINFORCE [@Williams1992REINFORCE]) is included only in "
    "Sec. 3.1-3.2 (single-context and multi-context tabular bandits) "
    "and the MNIST contextual bandit (Sec. 3.3).",
    title="Setup: baselines = PG (where applicable), PPO, GRPO, DG",
)

setup_grpo_strengthened = setting(
    "**Our GRPO baseline (Appendix F).** The paper uses the standard "
    "PPO-style clipped surrogate with group-relative ($z$-scored) "
    "advantages, augmented with a reverse-KL penalty ($\\beta = "
    "0.04$) to the rollout snapshot policy. This is a *deliberate "
    "strengthening* over the no-KL variant because removing the KL "
    "term causes GRPO to collapse under sparse terminal reward "
    "(Section 3.6, Table 3). Throughout the paper, 'GRPO' refers to "
    "this KL-anchored variant unless explicitly suffixed (no KL).",
    title="Setup: GRPO = clipped surrogate + z-scored adv. + reverse-KL ($\\beta=0.04$)",
)

setup_grouping_k = setting(
    "**Group sizes.** The grouped methods (TPO, GRPO) sample $K$ "
    "candidates per group. For dense-reward token-level experiments, "
    "$K = 8$ next-token candidates at each prefix state. For "
    "terminal-reward sequence experiments, $K = 8$ full rollouts per "
    "prompt. For LLM RLVR (Sec. 3.8), $K = 16$ rollouts per prompt. "
    "Single-sample baselines (PPO, DG, plain PG) take $K = 1$ "
    "rollout per prompt.",
    title="Setup: $K = 8$ token / 8 sequence / 16 LLM RLVR",
)

setup_optimizer_defaults = setting(
    "**Optimizer defaults.** Unless stated otherwise, all transformer "
    "experiments use Optax's Muon optimizer [@Jordan2024Muon] applied "
    "to 2D parameter tensors with AdamW for non-2D tensors, learning "
    "rate $10^{-3}$ and batch size $B = 100$ [@DeepMind2020Optax]. "
    "Tabular runs (Sec. 3.1-3.2) bypass the neural optimizer and take "
    "normalised logit steps of size $\\alpha = 0.1$ directly. LLM "
    "RLVR (Sec. 3.8) uses AdamW at $10^{-5}$, batch size 16, on "
    "$4 \\times$ A100-80GB.",
    title="Setup: Muon ($10^{-3}$, $B=100$); tabular $\\alpha = 0.1$; LLM RLVR AdamW ($10^{-5}$)",
)

setup_dg_single_epoch = setting(
    "**DG runs at one epoch per rollout.** PPO, GRPO, and TPO take "
    "*multiple* gradient epochs per rollout batch. DG uses a *single* "
    "epoch per rollout batch, following [@Osband2026], because it "
    "diverges with more (Appendix E quantifies this: 4-epoch DG ends "
    "at 48.3% error vs. 2.0% for 1-epoch on reverse-copy with "
    "terminal reward, and 4-epoch DG is worse in 7 of 8 prompt-matched "
    "token-reversal variants). Single-epoch DG is the most favorable "
    "configuration for this baseline.",
    title="Setup: DG = 1 epoch/batch (most favorable for DG; multi-epoch diverges)",
)

# ---------------------------------------------------------------------------
# Matching protocol
# ---------------------------------------------------------------------------

setup_matching_protocol = setting(
    "**Prompt-matched vs. interaction-matched comparison.** Grouped "
    "methods consume $K$x more rollouts than single-sample methods "
    "for the same number of prompts. The paper reports two parallel "
    "comparisons. *Prompt-matched*: same number of prompts; grouped "
    "methods use more total rollouts. *Interaction-matched*: same "
    "total rollouts; single-sample methods see more prompts. The "
    "interaction-matched variant scales single-sample batch size and "
    "learning rate by $K$ and $\\sqrt{K}$ respectively to keep effort "
    "comparable. Both protocols are reported wherever the rollout "
    "budget differs.",
    title="Setup: report both prompt-matched and interaction-matched comparisons",
)

# ---------------------------------------------------------------------------
# Claims about the experimental setup itself
# ---------------------------------------------------------------------------

claim_grpo_kl_strengthens_baseline = claim(
    "**The reverse-KL penalty is GRPO's primary stabilizer under "
    "sparse reward.** Removing GRPO's KL penalty ($\\beta = 0$) makes "
    "it substantially worse: at $H = 7$ on terminal-reward "
    "token-reversal, GRPO (no KL) reaches 66.6% exact-match error vs. "
    "14.5% for KL-anchored GRPO; for $H \\ge 8$, GRPO (no KL) shows "
    "no meaningful learning ($> 95$% error) [@Kaddour2026, Sec. 3.6, "
    "Table 3]. The KL penalty fulfills the role of preventing the "
    "policy from drifting too far from the data that generated the "
    "advantages -- a role that TPO's cross-entropy-to-target "
    "objective fulfills *structurally* without requiring an explicit "
    "penalty (Appendix F).",
    title="Setup: removing KL collapses GRPO (66.6% vs 14.5% at $H=7$), confirming KL is essential",
)

claim_dg_multi_epoch_unstable = claim(
    "**DG is unstable with multi-epoch reuse (Appendix E).** With 4 "
    "gradient epochs per rollout (matching PPO/GRPO/TPO), DG ends at "
    "48.3% exact-match error on reverse-copy terminal-reward "
    "transformer RLVR vs. 2.0% for 1-epoch DG. Across the 8 "
    "prompt-matched token-reversal variants, 4-epoch DG is worse in "
    "7 of 8 settings (largest regressions on sequential reward: flip "
    "0.07% -> 4.56%, reverse-flip 0.00% -> 0.82%). This justifies "
    "the paper's choice to run DG at 1 epoch throughout, which is "
    "the most favorable setting for DG and matches Osband's "
    "intended use [@Osband2026].",
    title="Setup: DG diverges with $>1$ epoch (48.3% vs 2.0% at 4 ep on reverse-copy)",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 18",
        "caption": "DG epoch sensitivity: 1-epoch (2.0%) vs 4-epoch (48.3%) terminal-reward.",
    },
)

__all__ = [
    "setup_baselines",
    "setup_grpo_strengthened",
    "setup_grouping_k",
    "setup_optimizer_defaults",
    "setup_dg_single_epoch",
    "setup_matching_protocol",
    "claim_grpo_kl_strengthens_baseline",
    "claim_dg_multi_epoch_unstable",
]
