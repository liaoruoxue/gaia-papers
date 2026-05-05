"""Section 3.3: Neural policy learning -- MNIST contextual bandit.

Section 3.3 of [@Kaddour2026]. The MNIST contextual bandit casts
classification as a *one-step* contextual bandit: the agent samples
$A \\in \\{0, \\ldots, 9\\}$ on each example and receives $R = "
\\mathbf{1}\\{A = Y\\}$ without observing the label $Y$. Each method
samples a *single* action per context, so single-sample GRPO reduces
to batch-normalised REINFORCE.

The section has two strands:

* Learning curves (Figure 5(a)) -- TPO converges fastest (5% error at
  step 1,600 vs. 2,200 for DG) and reaches the lowest final error
  (2.9%); GRPO 5.9%, PG 5.3%, Group PG 7.2%.

* Mechanism panel (Figure 5(b)) -- TPO's *extra* gain over a generic
  one-vs-rest baseline grows with wrong-class concentration (rises to
  +0.073 in the highest-concentration bin), confirming the analytic
  prediction from Appendix C: TPO is unique in turning a *failed*
  sample into a class-specific suppression of the sampled wrong class.

The Group PG ablation isolates target matching as the active
ingredient: keeping the same candidates and standardized scores but
reverting to scalar-weighted REINFORCE raises final error from 2.9%
to 7.2%.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

setup_mnist_bandit = setting(
    "**MNIST contextual bandit setup.** Following [@Osband2026], "
    "MNIST classification is recast as a one-step contextual bandit: "
    "the agent samples $A \\in \\{0, \\ldots, 9\\}$ and receives $R = "
    "\\mathbf{1}\\{A = Y\\}$ without observing the label $Y$. A "
    "two-layer ReLU network trains for 10,000 steps over 20 seeds. "
    "Each method samples a *single* action per context (so single-"
    "sample GRPO reduces to batch-normalised REINFORCE). Optimizer "
    "= Adam, learning rate $10^{-3}$, batch size $B = 100$.",
    title="Setup (3.3): MNIST as a one-step bandit, 1 action/context, 10K steps, 20 seeds",
)

setup_group_pg_ablation = setting(
    "**Group PG: same-signal scalar ablation.** 'Group PG' is the "
    "TPO ablation that *keeps* the same candidates and standardized "
    "scores $u_i$ that TPO uses, but *replaces* the target-matching "
    "cross-entropy loss with scalar-weighted REINFORCE on each "
    "candidate (i.e. it uses $u_a$ as a scalar advantage on the "
    "sampled coordinate and discards the target-distribution "
    "structure). It collapses in expectation to $g_{\\text{Group PG}} "
    "= 6 g_{\\text{PG}}$ on $K = 10$ classes (Appendix C). This "
    "ablation isolates *target matching itself* as the source of "
    "TPO's gain by holding the candidate set and the score signal "
    "constant.",
    title="Setup (3.3): Group PG = TPO's candidates + scalar REINFORCE (same signal, no target structure)",
)

# ---------------------------------------------------------------------------
# Numerical results from Sec. 3.3
# ---------------------------------------------------------------------------

claim_mnist_final_errors = claim(
    "**MNIST final error table (step 10,000).** On the MNIST "
    "contextual bandit, the final classification errors are:\n\n"
    "| Method | Final error (%) |\n"
    "|--------|----------------:|\n"
    "| TPO | **2.9** |\n"
    "| DG | (close to TPO; reaches 5% at step 2,200) |\n"
    "| PG | 5.3 |\n"
    "| GRPO (single-sample) | 5.9 |\n"
    "| Group PG | 7.2 |\n\n"
    "TPO converges fastest (reaches 5% error at step 1,600 vs. 2,200 "
    "for DG), and Group PG's 7.2% vs. TPO's 2.9% is the ablation "
    "that isolates target matching itself as the active ingredient "
    "[@Kaddour2026, Sec. 3.3, Figure 5(a)].",
    title="Numerical (3.3): TPO 2.9% < PG 5.3% < GRPO 5.9% < Group PG 7.2%",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 5(a)",
        "caption": "MNIST contextual bandit learning curves, all single-sample updates.",
    },
)

claim_mnist_tpo_fastest = claim(
    "**MNIST -- TPO converges fastest and reaches lowest final "
    "error.** The tabular pattern from Sec. 3.1-3.2 survives the "
    "transition to a neural policy: TPO converges fastest (5% error "
    "at step 1,600 vs. 2,200 for DG) and reaches the lowest final "
    "error (2.9%) on the MNIST contextual bandit.",
    title="Result (3.3): the tabular pattern survives in a neural policy",
)

claim_grpo_collapses_to_reinforce = claim(
    "**With a single sampled action per context, GRPO reduces to "
    "batch-normalised REINFORCE.** Conditioning on the realised "
    "minibatch statistics $(\\mu_B, \\sigma_B)$, the expected "
    "single-sample GRPO update is $g_{\\text{GRPO}} | \\mu_B, "
    "\\sigma_B = (p / \\sigma_B) (e_y - \\pi)$, exactly REINFORCE "
    "with batch-standardized rewards (Appendix C). It introduces no "
    "new within-example geometry beyond plain PG, which is why GRPO "
    "(5.9%) and PG (5.3%) perform comparably on MNIST [@Kaddour2026, "
    "Appendix C].",
    title="Mechanism (3.3): single-sample GRPO == batch-norm REINFORCE",
)

claim_pg_grpo_grouppg_collapse_to_one_vs_rest = claim(
    "**PG, single-sample GRPO, and Group PG all collapse to a "
    "rescaled one-vs-rest direction.** Appendix C derives that all "
    "three reduce in expectation to $g \\propto p (e_y - \\pi)$ on "
    "MNIST, so they only preserve a scalar 'correct vs. incorrect' "
    "signal. They do not condition on *which* wrong class was "
    "sampled, so a failed sample provides no class-specific signal: "
    "in expectation it just rescales the same one-vs-rest direction "
    "[@Kaddour2026, Appendix C].",
    title="Mechanism (3.3): PG / single-sample GRPO / Group PG collapse to one-vs-rest",
)

claim_tpo_dg_condition_on_action = claim(
    "**Only DG and TPO condition on the *sampled* action.** Both DG "
    "and TPO condition their update on which action was actually "
    "sampled; in general their direction depends on the detailed "
    "distribution of wrong-class mass. But only TPO turns a *failed* "
    "sample into a class-specific *target* update: a correct sample "
    "pulls probability toward the label, while an incorrect sample "
    "*directly suppresses the sampled wrong class* and redistributes "
    "that mass elsewhere (Appendix C: $g_-(j) = \\gamma(\\pi_j)(\\pi "
    "- e_j)$).",
    title="Mechanism (3.3): only TPO turns a failure into a class-specific target update",
)

# ---------------------------------------------------------------------------
# Mechanism prediction and Figure 5(b) confirmation
# ---------------------------------------------------------------------------

claim_concentrated_mistakes_prediction = claim(
    "**Mechanism prediction.** TPO's per-failure suppression of the "
    "sampled wrong class should help *most* when error mass is "
    "*concentrated* on one or a few confusing alternatives (so that "
    "removing one wrong class is a useful redistribution), and "
    "*least* when wrong-class mass is diffuse (where one-vs-rest is "
    "approximately optimal). DG, by contrast, gates on surprisal but "
    "still uses an aggregated 'one-vs-rest' direction "
    "$\\beta_{\\text{DG}}^{\\text{sym}}(p) (e_y - \\pi)$ in the "
    "symmetric limit (Appendix C), so it should *not* show the same "
    "extra gain on concentrated mistakes [@Kaddour2026, Sec. 3.3].",
    title="Mechanism prediction: TPO's gain should grow with wrong-class concentration",
)

claim_concentration_panel_observation = claim(
    "**Figure 5(b) observation -- on misclassified MNIST examples at "
    "step 2,000, TPO's extra gain in $p_y$ over a generic one-vs-rest "
    "baseline grows with wrong-class concentration.** Per misclassified "
    "test example, define wrong-class concentration $c = \\max_{j \\ne "
    "y} \\pi_j / (1 - \\pi_y)$. Comparing the exact first-order gain "
    "in $p_y$ from each method to the scalar one-vs-rest surrogate "
    "from Appendix C:\n\n"
    "| Concentration bin | TPO excess gain | DG excess gain |\n"
    "|-------------------|----------------:|---------------:|\n"
    "| 0.00-0.25 | near 0 | slightly negative |\n"
    "| 0.25-0.50 | small positive | slightly negative |\n"
    "| 0.50-0.75 | larger positive | slightly negative |\n"
    "| 0.75-1.00 | **+0.073** (max) | slightly negative |\n\n"
    "TPO's surplus is near zero when error mass is diffuse and rises "
    "to about $+0.073$ in the highest-concentration bin; DG stays "
    "slightly negative throughout [@Kaddour2026, Sec. 3.3, Figure "
    "5(b)].",
    title="Observation (3.3): TPO excess gain rises to +0.073 at highest-concentration bin",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 5(b)",
        "caption": "Per-bin extra gain in $p_y$ vs. wrong-class concentration $c$, step 2,000.",
    },
)

claim_concentration_panel_predicts = claim(
    "**Figure 5(b) confirms the mechanism prediction.** The "
    "predicted shape ('TPO's surplus is near zero when error mass is "
    "diffuse, but rises in concentrated bins; DG does not') is "
    "exactly what Figure 5(b) shows. This supports the causal "
    "explanation that TPO's MNIST advantage *comes from* its "
    "per-failure class-specific target structure -- not from any "
    "other ingredient (the standardized scores, candidate set, and "
    "softmax architecture are shared by Group PG, which lacks the "
    "target structure and is the worst method on this task at 7.2%).",
    title="Mechanism (3.3): Figure 5(b) confirms TPO's mechanism prediction; rules out one-vs-rest collapse",
)

__all__ = [
    "setup_mnist_bandit",
    "setup_group_pg_ablation",
    "claim_mnist_final_errors",
    "claim_mnist_tpo_fastest",
    "claim_grpo_collapses_to_reinforce",
    "claim_pg_grpo_grouppg_collapse_to_one_vs_rest",
    "claim_tpo_dg_condition_on_action",
    "claim_concentrated_mistakes_prediction",
    "claim_concentration_panel_observation",
    "claim_concentration_panel_predicts",
]
