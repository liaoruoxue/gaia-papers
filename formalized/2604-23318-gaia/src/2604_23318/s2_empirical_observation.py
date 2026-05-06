"""Section 2: Distributional divergence in hidden states (the empirical observation).

Section 2 of [@Chen2026SHEAR]. Establishes the empirical observation
that motivates and grounds the entire approach: in a controlled
diagnostic setting, hidden-state distributional structure is strongly
associated with local reasoning quality, and Wasserstein distance is
a useful way to measure this structure.

Setup: MATH500 + Qwen2.5-Math-7B; G=8 rollouts per problem; retain only
problems with mixed correctness (83.8% retained, see Appendix I); for
each retained rollout, take prefixes via sliding window (start length
w=100, stride s=25), excluding final-answer spans. At each truncation
point, estimate continuation success rate by completing 16 times and
measuring fraction correct, and compute Wasserstein distance between
the local (last-w tokens) hidden-state distribution and the closest
matching span from the *opposing* group.

The two key pieces of evidence are (a) the aggregate trend along the
chain (Figure 1a, Spearman -0.96 with closely aligned transition zones)
and (b) the within-trajectory local association (Figure 1b, Spearman
-0.42 over 16,920+ stride-pair shift events with |dAcc| >= 0.0625,
p = 4.6e-59). These are *independently informative*: (a) establishes
the macro-level alignment, (b) refutes the alternative that the signal
is a pure aggregate artifact (e.g. of length).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Diagnostic setup
# ---------------------------------------------------------------------------

setup_diagnostic_protocol = setting(
    "**Section 2 diagnostic protocol.** MATH500 [@Hendrycks2021MATH] is "
    "used as the evaluation benchmark with Qwen2.5-Math-7B "
    "[@Qwen2024Qwen25] as the base model. For each problem the paper "
    "samples $G = 8$ rollouts and retains only problems where the "
    "model produces a *mix* of correct and incorrect answers (this "
    "filtering is required because the diagnostic compares correct vs. "
    "incorrect within the same group, and excludes uniformly-easy or "
    "uniformly-hard problems where no opposing group exists). The "
    "retained subset comprises 83.8% of MATH500 and is balanced across "
    "difficulty (Appendix I, Figure 10: each accuracy bin from 0.125 "
    "to 0.875 contributes 7-18% of the retained problems, with no "
    "single bin dominating).",
    title="Setup: MATH500 + Qwen2.5-Math-7B, G=8, retain mixed-outcome groups (83.8% of MATH500)",
)

setup_sliding_window_diagnostic = setting(
    "**Sliding-window prefix-completion protocol.** For each retained "
    "rollout, prefixes are extracted at varying truncation points "
    "using a sliding window with starting length $w = 100$ tokens and "
    "stride $s = 25$ tokens, excluding spans that contain the final "
    "answer (to avoid leakage from answer-revealing tokens). At each "
    "truncation point: (i) the *continuation success rate* is "
    "estimated by completing the reasoning 16 times from that prefix "
    "and recording the fraction of correct completions -- used as a "
    "proxy for local reasoning quality (since prefixes that preserve "
    "a valid trajectory should admit higher correct-completion "
    "probability); (ii) the hidden states of the most recent $w$ "
    "tokens form an empirical distribution, and the Wasserstein "
    "distance is computed between this local distribution and the "
    "closest matching distribution from the *opposing* group "
    "(correct vs. incorrect).",
    title="Setup: prefix-completion protocol with sliding window (w=100, s=25)",
)

# ---------------------------------------------------------------------------
# Aggregate trend (Figure 1a)
# ---------------------------------------------------------------------------

claim_fig1a_aggregate_anticorrelation = claim(
    "**Figure 1a: aggregate anti-correlation between Wasserstein "
    "distance and continuation success along the chain.** Plotting "
    "both quantities as a function of prefix position (aggregated "
    "across all retained problems), as prefixes extend deeper into "
    "the reasoning chain, continuation success tends to *decline* "
    "(from $\\approx 0.95$ near position 0 to near $0$ by position "
    "$\\approx 2000$, blue curve, left axis) while Wasserstein distance "
    "tends to *increase* (from $\\approx 0.70$ to $\\approx 0.90$, "
    "brown curve, right axis). The transition zones of the two curves "
    "are closely aligned -- the region where success begins to decline "
    "coincides with the region where Wasserstein distance begins to "
    "rise. Spearman correlation $\\rho = -0.96$.",
    title="Fig 1a: aggregate Spearman -0.96 anti-correlation with aligned transition zones",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 1(a)",
        "spearman": "-0.96",
        "data": "MATH500 + Qwen2.5-Math-7B; aggregated across retained problems",
    },
)

# ---------------------------------------------------------------------------
# Within-trajectory local association (Figure 1b)
# ---------------------------------------------------------------------------

setup_mutation_threshold = setting(
    "**Mutation-event threshold.** Continuation success at each prefix "
    "is estimated by completing the reasoning 16 times and recording "
    "the fraction of correct completions, so the *minimum detectable* "
    "change between consecutive prefixes is $1/16 = 0.0625$. The paper "
    "therefore adopts $|\\Delta\\text{Accuracy}| \\geq 0.0625$ as the "
    "threshold for identifying *meaningful local shifts*: changes "
    "below this magnitude are indistinguishable from sampling noise "
    "in a 16-trial estimate, while changes at or above the threshold "
    "correspond to at least one completion flipping correct vs. "
    "incorrect (a meaningful shift in reasoning quality).",
    title="Setup: |dAcc| >= 0.0625 = 1/16 detection threshold",
)

claim_fig1b_local_anticorrelation = claim(
    "**Figure 1b: within-trajectory local anti-correlation.** For each "
    "pair of consecutive prefix positions within the *same* rollout, "
    "the paper computes $\\Delta\\text{Accuracy} = "
    "\\text{Acc}(s_t) - \\text{Acc}(s_{t-1})$ and the concurrent "
    "$\\Delta W = W(s_t) - W(s_{t-1})$, retaining only positions where "
    "$|\\Delta\\text{Accuracy}| \\geq 0.0625$. The scatter of $\\Delta W$ "
    "vs. $\\Delta\\text{Accuracy}$ shows: when continuation success "
    "*locally decreases* (negative $\\Delta\\text{Accuracy}$), "
    "Wasserstein distance tends to *locally increase* (positive "
    "$\\Delta W$), and vice versa. Spearman $\\rho = -0.42$, "
    "$p = 4.6 \\times 10^{-59}$.",
    title="Fig 1b: within-trajectory Spearman -0.42 (p=4.6e-59) at |dAcc| >= 0.0625",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 1(b)",
        "spearman": "-0.42",
        "p_value": "4.5985e-59",
    },
)

# ---------------------------------------------------------------------------
# Implications (synthesised observation)
# ---------------------------------------------------------------------------

claim_aggregate_and_local_complementary = claim(
    "**Aggregate + local evidence are complementary, not redundant.** "
    "The aggregate trend (Figure 1a) alone could be explained by "
    "pure chain-length effects -- both curves drift over chain "
    "position regardless of correctness. The within-trajectory local "
    "analysis (Figure 1b) controls for this confound: it isolates "
    "stride-wise *local* shifts within the same rollout and shows "
    "that reasoning-quality drops co-occur with hidden-state "
    "divergence rises *at the local stride scale*. Taken together, "
    "(a) and (b) show the signal carries genuine local reasoning-"
    "quality information, not just an aggregate length artifact -- "
    "the necessary precondition for using span-level Wasserstein "
    "distance as a *fine-grained* credit signal.",
    title="Implication: local + aggregate together rule out length-only artifact",
)

claim_self_supervised_signal_proposal = claim(
    "**The signal is self-supervised.** The Wasserstein distance is "
    "computed between hidden-state distributions of correct vs. "
    "incorrect rollouts within the *same* GRPO group, partitioned by "
    "the outcome-level reward $r^{(i)} \\in \\{0, 1\\}$. No step-level "
    "annotation is required: the only supervision used is the binary "
    "outcome signal already available in RLVR. If this distributional "
    "divergence signal can be reliably detected, it can serve as a "
    "self-supervised proxy for process-level credit -- the central "
    "observation that motivates the SHEAR method (Section 3) and the "
    "separation theorem (Section 4).",
    title="Implication: outcome-only labels suffice to extract the signal",
)

# ---------------------------------------------------------------------------
# Detailed analysis (Appendix A): cross-sectional + dynamic
# ---------------------------------------------------------------------------

claim_appendix_a_cross_sectional = claim(
    "**Appendix A.1 cross-sectional analysis: W-distance discriminates "
    "*independently of position*.** To rule out 'W-distance is just a "
    "proxy for token depth', the paper bins trajectories into prefix-"
    "position bins and within each bin into W-distance quantiles "
    "(Figure 9). Even in the early stages (position bin $(0, 250]$), "
    "higher W-distance weakly but consistently corresponds to lower "
    "mean empirical accuracy (Spearman $-0.055$, $p = 7.6 \\times "
    "10^{-18}$). The Spearman correlation strengthens as the chain "
    "lengthens: $-0.010$ for $(250, 500]$, $-0.167$ for $(500, 750]$, "
    "$-0.225$ for $(750, 1000]$ -- proving W-distance is an "
    "*independent* indicator of reasoning quality and an early-warning "
    "signal for vulnerable reasoning state.",
    title="Appendix A.1: cross-sectional W-distance discrimination strengthens with position",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 9",
    },
)

__all__ = [
    "setup_diagnostic_protocol",
    "setup_sliding_window_diagnostic",
    "setup_mutation_threshold",
    "claim_fig1a_aggregate_anticorrelation",
    "claim_fig1b_local_anticorrelation",
    "claim_aggregate_and_local_complementary",
    "claim_self_supervised_signal_proposal",
    "claim_appendix_a_cross_sectional",
]
