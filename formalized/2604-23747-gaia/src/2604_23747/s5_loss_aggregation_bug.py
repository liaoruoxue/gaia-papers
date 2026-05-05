"""Section 2.2: the OpenRLHF loss aggregation bug.

This module formalizes (a) the precise mechanism of the per-mini-batch
loss-weighting bug, (b) why it is silently inherited from pretraining
codebases (where it is benign because of data packing), (c) its impact on
SFT (where prompts/responses vary in length so it is non-trivial), and
(d) the fix.

Source: [@Limozin2026SFTthenRL, Sec. 2.2; Appendix D].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setting: the per-token mean SFT loss contract
# ---------------------------------------------------------------------------

setup_per_token_mean_loss = setting(
    "**Per-token mean SFT loss contract.** The standard cross-entropy "
    "loss for SFT averages over all *response tokens* in a batch, "
    "masking out both padding and prompt tokens. Formally, for a batch "
    "with M mini-batches and per-rank token-level log-probabilities "
    "$\\ell_i$ and binary loss masks $m_i$, the correct per-token mean "
    "is $L = -\\sum_i m_i \\ell_i / \\sum_i m_i$ where the sums run "
    "over *all* response tokens across all mini-batches and all data-"
    "parallel (DP) ranks. Each response token must contribute equally; "
    "tokens belonging to longer responses do *not* deserve more weight "
    "than tokens belonging to shorter ones.",
    title="Setting: correct SFT loss = per-token mean over all response tokens (masked CE)",
)

setup_dp_ranks = setting(
    "**Distributed data-parallel (DP) loss reduction.** In data-parallel "
    "training with DP world size $D$, each rank computes its local "
    "loss and the distributed optimizer averages gradients across ranks "
    "(equivalent to averaging losses). To recover the correct per-token "
    "mean across ranks, each rank's local loss must be scaled so that "
    "after averaging across $D$ ranks the result equals the global "
    "per-token mean.",
    title="Setting: DP gradient averaging requires global token-count normalization",
)

# ---------------------------------------------------------------------------
# Bug mechanism
# ---------------------------------------------------------------------------

claim_loss_agg_mechanism = claim(
    "**Mechanism of the loss aggregation bug: mean-of-means instead of "
    "true per-token mean.** A common bug in gradient-accumulation code "
    "computes a *mean of per-mini-batch means* instead of the true "
    "per-token mean: since mini-batches contain different numbers of "
    "response tokens, this weights each mini-batch equally regardless "
    "of how many active tokens it contains. The same distortion arises "
    "across DP ranks, where each rank independently computes its "
    "*local* mean loss before averaging across ranks. OpenRLHF "
    "[@OpenRLHF], Llama-Factory [@LlamaFactory], and early versions of "
    "verl [@verl] all exhibit this bug. The bug is documented in "
    "Han and Han [@HanGradAccum] and in Debut et al. [@DebutGradAccum] "
    "[@Limozin2026SFTthenRL, Sec. 2.2].",
    title="Bug mechanism: mean-of-per-mini-batch-means instead of per-token mean",
)

claim_inherited_from_pretrain = claim(
    "**The bug is inherited from pretraining codebases where it was "
    "benign.** In pretraining, *data packing* ensures equal active "
    "token counts across ranks, making the mean-of-means equivalent to "
    "the true per-token mean. The bug is silent in this regime. In SFT, "
    "however, prompts and responses vary in length across samples, so "
    "mini-batches and ranks almost always have different active token "
    "counts -- meaning the bug affects almost every training step "
    "[@Limozin2026SFTthenRL, Sec. 2.2].",
    title="Bug origin: inherited from pretraining codebases (silent there because of data packing)",
)

# ---------------------------------------------------------------------------
# Consequences
# ---------------------------------------------------------------------------

claim_loss_agg_variability = claim(
    "**Consequence: the loss aggregation bug introduces *variability* "
    "in the SFT loss curve without shifting its mean.** Figure 2 "
    "(left) shows that fixing the loss aggregation bug alone reduces "
    "the variability of the SFT training loss but does not shift the "
    "mean. The variability is the bug's signature: per-mini-batch / "
    "per-rank mean-of-means weighting introduces step-to-step "
    "fluctuations that disappear once token-level aggregation is used "
    "[@Limozin2026SFTthenRL, Fig. 2 left; Sec. 4].",
    title="Consequence: loss aggregation bug = variability (not mean shift)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 2 (left)",
        "caption": "Fig. 2 left: training loss; loss-agg bug fix reduces variability without shifting the mean.",
    },
)

claim_loss_agg_smaller_effect = claim(
    "**The loss aggregation bug's effect on final SFT performance is "
    "*smaller* than the optimizer bug, but not negligible.** As shown "
    "in Table 2 of the paper, fixing only the loss aggregation bug "
    "lifts the average score from 48.3 to 49.1 (+0.8 points), while "
    "fixing the optimizer bug alone lifts the same average to 53.4 "
    "(+5.1 points). Fixing the loss aggregation bug *on top of* the "
    "optimizer fix still yields a measurable improvement to 54.0 "
    "(+0.6 points on top of the optimizer fix) and stabilizes loss "
    "variability [@Limozin2026SFTthenRL, Sec. 2.2; Table 2].",
    title="Consequence: loss aggregation bug = small but non-negligible effect (+0.6 to +0.8 pts)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 2",
        "caption": "Table 2: progressive bug-fix waterfall on Qwen2.5-Math-7B.",
    },
)

# ---------------------------------------------------------------------------
# Fix
# ---------------------------------------------------------------------------

claim_loss_agg_fix = claim(
    "**Fix: aggregate token-level loss sums and counts across all DP "
    "ranks and mini-batches before dividing.** The corrected algorithm "
    "(Appendix D, Algorithm 2) computes a local *sum* "
    "$S_k = \\text{MaskedSum}(-\\ell_i, m_i)$ and local token count "
    "$n_k = \\sum_i m_i$ on each rank, all-reduces the token counts to "
    "obtain the global token count $N$, and then sets the local loss "
    "to $L_k = S_k / N \\times D$ (scaling by $D$ to account for "
    "gradient averaging across DP ranks). The fix has been submitted "
    "upstream (OpenRLHF PR #1216). Verl fixed this in November 2025 "
    "(verl PR #3994); OpenRLHF and Llama-Factory have not as of the "
    "paper's submission [@Limozin2026SFTthenRL, Sec. 2.2; Appendix D].",
    title="Fix: token-level all-reduce of sum + count, then scale by DP world size",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Algorithm 2 / Appendix D",
        "caption": "Algorithm 2: corrected SFT loss = MaskedSum / global token count, scaled by D.",
    },
)

# ---------------------------------------------------------------------------
# Patched-OpenRLHF matches verl
# ---------------------------------------------------------------------------

claim_patched_matches_verl = claim(
    "**The fully patched OpenRLHF SFT pipeline matches the "
    "independently implemented verl SFT pipeline.** With both bugs "
    "fixed, OpenRLHF achieves a 54.0 average score on the Table 2 "
    "evaluation subset, statistically indistinguishable from verl's "
    "53.8 score (both within their reported 0.2-0.4 standard "
    "deviations). This independent-implementation match is the "
    "decisive cross-framework validation that the bugs are real and "
    "the fixes are complete [@Limozin2026SFTthenRL, Table 2; Sec. 4].",
    title="Result: patched OpenRLHF (54.0) matches independently-implemented verl (53.8)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 2 (last two rows)",
        "caption": "Table 2: + fix both = 54.0, verl = 53.8 -- statistically equivalent.",
    },
)

__all__ = [
    "setup_per_token_mean_loss",
    "setup_dp_ranks",
    "claim_loss_agg_mechanism",
    "claim_inherited_from_pretrain",
    "claim_loss_agg_variability",
    "claim_loss_agg_smaller_effect",
    "claim_loss_agg_fix",
    "claim_patched_matches_verl",
]
