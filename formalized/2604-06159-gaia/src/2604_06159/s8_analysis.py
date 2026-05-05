"""Section 4: What explains TPO's gains under sparse reward?

Section 4 of [@Kaddour2026]. Three reinforcing mechanisms in a
representative sparse-reward regime ($H = 8$, $V = 2$, $K = 32$,
$B = 256$, 2,000 episodes):

* Sec. 4.1 -- TPO's gradient self-extinguishes empirically: the L2
  norm decays to near zero by ~episode 300 while GRPO's persists
  even after error plateaus at 12.7%.
* Sec. 4.2 -- Signal allocation: ~90% of groups are all-fail at
  initialization (since $(1/V)^H \\approx 0.4$%), but TPO drives
  the all-fail fraction to near zero quickly. The K-sweep and the
  zero-variance masking experiment show TPO degrades smoothly while
  GRPO is non-monotonic; *masking zero-variance groups makes GRPO
  worse* (29.7% vs. 6.3%), surprising on its face.
* Sec. 4.3 -- Multi-epoch reuse extracts more from rare informative
  batches. TPO at 4 epochs is ~5x faster than 1 epoch early; epoch-
  count sweep shows TPO is robust across $\\{1, 2, 4, 8, 16\\}$ while
  GRPO is strongly non-monotonic (37.6% at 2 epochs vs. 1.1% at 16).

The closing claim is explicitly multi-causal: "no single property
explains TPO's sparse-reward advantage; the gradient norm collapses
as the policy approaches its target, performance degrades smoothly
rather than abruptly when K or epoch count varies, and multi-epoch
reuse works without careful tuning."
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Sec. 4 setup
# ---------------------------------------------------------------------------

setup_section4_regime = setting(
    "**Section 4 representative sparse-reward regime.** $H = 8$, "
    "$V = 2$, $K = 32$, $B = 256$, 2,000 episodes (token-reversal "
    "with terminal reward). Per-step diagnostics computed from the "
    "original 10-seed runs; $K$-sweep, epoch sweep, and masking "
    "ablations use 30 seeds. The success rate per sequence at "
    "initialization is $(1/V)^H = (1/2)^8 \\approx 0.4$%, so most "
    "groups carry no signal early in training [@Kaddour2026, Sec. 4].",
    title="Setup (Sec. 4): $H=8, V=2, K=32, B=256$, 2,000 ep; init success rate ~0.4%",
)

# ---------------------------------------------------------------------------
# Sec. 4.1: gradient self-extinguishes
# ---------------------------------------------------------------------------

claim_4_1_grad_norm_collapse = claim(
    "**Sec. 4.1 observation -- TPO's first-epoch gradient L2 norm "
    "spikes during the learning phase and decays to near zero once "
    "the policy converges (~episode 300).** GRPO maintains "
    "*persistent* gradient norms throughout training, even after its "
    "error curve plateaus at 12.7% [@Kaddour2026, Figure 11(a)]. "
    "GRPO's policy keeps moving even after its error has stopped "
    "improving -- it does not settle near a fixed point.",
    title="Observation (4.1): TPO grad norm collapses to ~0 by ep 300; GRPO persists at 12.7% plateau",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 11(a)",
        "caption": "L2 norm of first-epoch gradient over training, $H=8, V=2, K=32$.",
    },
)

claim_4_1_target_mass_allocation = claim(
    "**Sec. 4.1 allocation diagnostic -- TPO rapidly removes weight "
    "from failed candidates; GRPO does not.** Figure 11(b) shows the "
    "per-candidate weight proxy (target mass $q_i$ for TPO; "
    "advantage magnitude $|A_i|$ for GRPO) on successful (solid) "
    "vs. failed (dashed) candidates. TPO drives the failed-candidate "
    "weight to near zero, while GRPO keeps assigning nonzero "
    "advantage magnitude to failures even late in training. This is "
    "an *allocation* diagnostic, not a gradient-decomposition (the "
    "two proxies are not directly comparable in scale); the "
    "fixed-point claim itself comes from panel (a).",
    title="Diagnostic (4.1): TPO drives failed-candidate weight to ~0; GRPO does not",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 11(b)",
    },
)

# ---------------------------------------------------------------------------
# Sec. 4.2: signal allocation when informative groups are rare
# ---------------------------------------------------------------------------

claim_4_2_all_fail_fraction = claim(
    "**Sec. 4.2 -- ~90% of groups are all-fail at initialization; "
    "TPO eliminates them fastest.** Figure 12(a) shows the fraction "
    "of groups in which all $K = 32$ candidates fail. At "
    "initialization this fraction is ~90% (consistent with the "
    "$(1/V)^H \\approx 0.4$% per-sequence success rate). TPO drives "
    "this fraction to near zero quickly, GRPO leaves a larger "
    "residual, and GRPO (no KL) remains substantially worse "
    "[@Kaddour2026, Sec. 4.2, Figure 12].",
    title="Observation (4.2): TPO drives the all-fail fraction to ~0 fastest",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 12(a)",
    },
)

claim_4_2_zero_variance_neutrality = claim(
    "**On the rollout snapshot, TPO is *neutral* on all-fail "
    "groups.** For all-fail groups, the score variance is zero, so "
    "(by the Appendix A convention) standardized scores $u = 0$, "
    "hence $q = p^{\\text{old}}$. The grouped-loss contribution on "
    "the *first* epoch is therefore exactly zero on these groups. "
    "Early in training, when informative groups are scarce, TPO "
    "thus concentrates its first-epoch grouped update on the small "
    "fraction of groups that actually distinguish better-vs-worse "
    "candidates. (This neutrality need not persist across epochs in "
    "the multi-epoch shared-parameter setting -- once informative "
    "groups have moved the policy away from the rollout snapshot, "
    "revisiting an all-fail group yields an anchor pullback toward "
    "$p^{\\text{old}}$.) [@Kaddour2026, Sec. 4.2].",
    title="Mechanism (4.2): all-fail groups have $q = p^{\\text{old}}$, zero first-epoch contribution",
)

claim_4_2_k_sweep = claim(
    "**Sec. 4.2 group-size sweep ($K \\in \\{4, 8, 16, 32, 64\\}$, 30 "
    "seeds).** Final exact-match error:\n\n"
    "| $K$ | TPO error (%) | GRPO error (%) |\n"
    "|----:|--------------:|---------------:|\n"
    "| 4 | 8.9 | 19.4 |\n"
    "| 8 | 5.2 | 19.8 |\n"
    "| 16 | 5.1 | 9.2 |\n"
    "| 32 | 2.6 | 4.4 |\n"
    "| 64 | **0.36** | 5.6 |\n\n"
    "TPO improves smoothly with $K$ (peaks at $K = 64$ with 0.36% "
    "error). GRPO improves to $K = 32$ (4.4%) then *worsens slightly* "
    "at $K = 64$ (5.6%) and is non-monotonic across the sweep. The "
    "paper notes this is a joint sensitivity over (i) candidate "
    "coverage and (ii) grouped-signal sharpness "
    "[@Kaddour2026, Sec. 4.2, Figure 13].",
    title="Sweep (4.2): TPO smooth in $K$ (8.9% -> 0.36%); GRPO non-monotonic",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 13",
    },
)

claim_4_2_zero_variance_masking_hurts = claim(
    "**Sec. 4.2 surprise -- masking zero-variance groups makes GRPO "
    "*worse*, not better.** GRPO (zv-masked) zeros the loss for any "
    "group where all $K$ candidates receive the same reward. In the "
    "30-seed aggregate, this raises GRPO's final exact-match error "
    "from 6.3% to 29.7% (Figure 14). TPO without any masking reaches "
    "0.05% in the same setting. *Interpretation*: in the multi-epoch "
    "setting, once informative groups have moved the shared policy, "
    "revisiting zero-variance groups can provide a useful anchor "
    "pullback toward the rollout snapshot; removing them therefore "
    "hurts. This rules out the obvious 'just delete dead groups' "
    "intervention as a cheap fix for GRPO [@Kaddour2026, Sec. 4.2].",
    title="Surprise (4.2): masking zero-var groups -> GRPO 6.3% -> 29.7% (TPO unmasked = 0.05%)",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 14",
    },
)

# ---------------------------------------------------------------------------
# Sec. 4.3: multi-epoch reuse
# ---------------------------------------------------------------------------

claim_4_3_multi_epoch_speedup = claim(
    "**Sec. 4.3 -- TPO with 4 epochs is ~5x faster than 1 epoch early "
    "and works at parity asymptotically.** At episode 400, TPO (4 "
    "epochs) has reached 0.2% exact-match error while TPO (1 epoch) "
    "is at 1.1%. Both eventually reach $< 0.1$%, confirming that "
    "multi-epoch extraction primarily *accelerates* learning rather "
    "than *enabling* it. DG, limited to one epoch (it diverges with "
    "more, see Appendix E), plateaus at 14% in this setting "
    "[@Kaddour2026, Sec. 4.3, Figure 15].",
    title="Observation (4.3): TPO 4-ep reaches 0.2% by ep 400; 1-ep at 1.1% (~5x faster)",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 15",
    },
)

claim_4_3_epoch_sweep = claim(
    "**Sec. 4.3 epoch sweep ($\\{1, 2, 4, 8, 16\\}$ epochs, 30 "
    "seeds).** Final exact-match error:\n\n"
    "| Epochs | TPO error (%) | GRPO error (%) |\n"
    "|-------:|--------------:|---------------:|\n"
    "| 1 | 0.02 | 4.3 |\n"
    "| 2 | (low; below 2.3%) | 37.6 |\n"
    "| 4 | 0.05 | 6.3 |\n"
    "| 8 | (low) | 3.3 |\n"
    "| 16 | (low) | 1.1 |\n\n"
    "TPO stays below 2.3% across the entire range and is near zero "
    "at 1 and 4 epochs. GRPO is *strongly non-monotonic* (worst at 2 "
    "epochs, recovers at 8-16) -- it can reach low error with the "
    "right epoch count but is much more sensitive to this choice "
    "[@Kaddour2026, Sec. 4.3, Figure 16].",
    title="Sweep (4.3): TPO < 2.3% across all epoch counts; GRPO non-monotonic (37.6% at 2 ep)",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 16",
    },
)

# ---------------------------------------------------------------------------
# Closing multi-cause synthesis
# ---------------------------------------------------------------------------

claim_4_no_single_property = claim(
    "**Sec. 4 closing claim -- no single property explains TPO's "
    "sparse-reward advantage.** The mechanisms identified -- gradient "
    "self-extinguishing as the policy approaches its target (Sec. "
    "4.1), zero-variance neutrality and signal concentration on "
    "informative groups (Sec. 4.2), and stable multi-epoch reuse "
    "without careful tuning (Sec. 4.3) -- *reinforce each other* "
    "and are absent from the baselines. The paper explicitly "
    "frames this as multi-causal: 'no single property explains "
    "TPO's sparse-reward advantage' [@Kaddour2026, Sec. 4.3 closing].",
    title="Synthesis (Sec. 4): multi-causal -- self-extinguishing + signal allocation + stable multi-epoch",
)

__all__ = [
    "setup_section4_regime",
    "claim_4_1_grad_norm_collapse",
    "claim_4_1_target_mass_allocation",
    "claim_4_2_all_fail_fraction",
    "claim_4_2_zero_variance_neutrality",
    "claim_4_2_k_sweep",
    "claim_4_2_zero_variance_masking_hurts",
    "claim_4_3_multi_epoch_speedup",
    "claim_4_3_epoch_sweep",
    "claim_4_no_single_property",
]
