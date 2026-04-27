"""Section 7: Synthetic-experiment validation of the two theorems."""

from gaia.lang import claim, setting, support, abduction, induction, compare
from .s5_consistency import claim_theorem_5_1
from .s6_regret import claim_theorem_6_1

# --- Discrete sandbox setup (Sec. 7.1, Appendix C.1) ---

setup_discrete_sandbox = setting(
    "**Discrete sandbox (Appendix C.1).** Latent state "
    "$s\\in\\{1,\\ldots,6\\}$, action $x\\in\\{1,\\ldots,4\\}$, scalar Gaussian "
    "observation $y_t|(s,x_t)\\sim\\mathcal{N}(\\mu_{s,x_t}, \\sigma^2)$ with "
    "$\\sigma=0.2$. The mean table $\\mu_{s,x_t}$ is constructed so that one "
    "informative action yields well-separated likelihoods (average gap "
    "$\\Delta\\approx 1.5$) while the other actions are nearly indistinguishable "
    "($\\Delta\\approx 0.05$). Energy heuristic "
    "$h_t(y) = a(y-c)^2$ with $c=0$ and $a\\in[0.15,0.35]$. Posterior error mass "
    "$w_t = \\sum_{s\\neq s^*}q_t(s)$ is averaged over 5 random seeds. "
    "Error bars represent $\\pm 0.2\\,\\mathrm{std}$ across seeds.",
    title="Discrete sandbox experimental setup",
)

# --- Three observations from Figure 1 (one per sweep) ---

obs_fig1a_prior_entropy = claim(
    "**Figure 1(a) (Prior Entropy sweep).** With $\\beta=2.0$ fixed, varying the "
    "prior mass $q_0(s^*)\\in\\{0.7, 0.5, 0.25\\}$ (equivalently "
    "$H_0\\in\\{1.09, 1.50, 1.77\\}$ as labeled in the legend) shows that smaller "
    "$H_0$ yields faster posterior contraction: the curve for $H_0=1.09$ reaches "
    "$w_t\\approx 0$ earlier than $H_0=1.77$.",
    title="Fig 1(a): smaller prior entropy yields faster contraction",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 1(a)",
              "caption": "Discrete sandbox, Prior Entropy sweep at fixed beta=2.0."},
)

obs_fig1b_distinguishability = claim(
    "**Figure 1(b) (Discriminative Strength sweep).** With $\\beta=2.0$ fixed, "
    "varying the gap structure to give pre-convergence average $A_t$ values of "
    "$\\{1.017, 0.556, -0.013\\}$ shows that higher discriminative strength "
    "accelerates convergence, while insufficient distinguishability "
    "($\\bar A < 0$) leads to stalled contraction (the green curve does not "
    "reach $w_t\\approx 0$).",
    title="Fig 1(b): higher discriminability accelerates convergence; negative gap stalls",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 1(b)",
              "caption": "Discrete sandbox, Distinguishability sweep at fixed beta=2.0."},
)

obs_fig1c_curiosity = claim(
    "**Figure 1(c) (Curiosity sweep).** Varying $\\beta\\in\\{2.0, 0.8, 0.05\\}$ "
    "with the informative gap structure shows that sufficient curiosity is "
    "necessary for consistent learning: $\\beta=2.0$ and $\\beta=0.8$ drive "
    "$w_t\\to 0$ within $\\sim 25$ iterations, whereas $\\beta=0.05$ stalls at a "
    "high error mass.",
    title="Fig 1(c): sufficient curiosity is necessary for consistency",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 1(c)",
              "caption": "Discrete sandbox, Curiosity sweep."},
)

# --- Theorem 5.1 predictions (theoretical predictions, separated from observations) ---

pred_th5_1_h0 = claim(
    "**Prediction from @claim_theorem_5_1 (prior entropy).** Since $H_0$ appears "
    "linearly in the numerator of the sample-complexity bound, smaller $H_0$ "
    "should reduce the iterations needed to reach a target error mass.",
    title="Theorem 5.1 prediction: smaller H_0 -> faster contraction",
)

pred_th5_1_at = claim(
    "**Prediction from @claim_theorem_5_1 (discriminability).** $\\underline{A}_T$ "
    "appears in the denominator: larger discriminative strength should accelerate "
    "convergence, and $\\underline{A}_T \\to 0$ should make the bound vacuous "
    "(stalled contraction).",
    title="Theorem 5.1 prediction: larger discriminability -> faster convergence",
)

pred_th5_1_curiosity = claim(
    "**Prediction from @claim_theorem_5_1 (sufficient curiosity).** Below the "
    "lower bound on $\\beta_t$, the proof's chain of inequalities fails, so the "
    "consistency guarantee disappears. Empirically this should manifest as "
    "stalled posterior contraction at low $\\beta$.",
    title="Theorem 5.1 prediction: sub-threshold beta -> stalled learning",
)

# --- Alternative explanations for the experimental patterns ---
# These are the plausible "null" / counter-explanations one might invoke for
# the same observations.

alt_purely_random = claim(
    "**Alternative explanation.** The Figure 1 contraction patterns could be "
    "artifacts of random seed variability in only 5 trials rather than evidence "
    "for the theorem's mechanism.",
    title="Alternative: small-sample seed variability",
)

alt_h0_entropy_unrelated = claim(
    "**Alternative explanation.** Figure 1(a)'s ordering of curves could be "
    "coincidence: maybe a more accurate prior simply trivially identifies $s^*$ "
    "without invoking the theorem's mechanism.",
    title="Alternative: prior trivializes identification",
)

# --- Abduction patterns: theorem 5.1 best explains Figure 1 patterns ---

# 1(a) prior entropy
sup_h_fig1a = support(
    [pred_th5_1_h0],
    obs_fig1a_prior_entropy,
    reason=(
        "@pred_th5_1_h0 directly predicts the rank ordering of contraction "
        "curves by $H_0$, which matches Figure 1(a) qualitatively."
    ),
    prior=0.9,
)
sup_alt_fig1a = support(
    [alt_h0_entropy_unrelated],
    obs_fig1a_prior_entropy,
    reason=(
        "Even without the theorem's machinery, a more concentrated prior would "
        "place more mass on $s^*$ from the outset, naively producing faster "
        "apparent contraction."
    ),
    prior=0.5,
)
cmp_fig1a = compare(
    pred_th5_1_h0, alt_h0_entropy_unrelated, obs_fig1a_prior_entropy,
    reason=(
        "Both predictions are qualitatively compatible with the curve ordering, "
        "but the theorem's prediction (@pred_th5_1_h0) is *quantitative* (linear "
        "scaling with $H_0$) whereas the alternative (@alt_h0_entropy_unrelated) "
        "merely predicts an ordering."
    ),
    prior=0.8,
)
abd_fig1a = abduction(
    sup_h_fig1a, sup_alt_fig1a, cmp_fig1a,
    reason="Theorem 5.1's prior-entropy prediction better explains Figure 1(a).",
)

# 1(b) distinguishability — the *negative* gap stall is the key signature.
sup_h_fig1b = support(
    [pred_th5_1_at],
    obs_fig1b_distinguishability,
    reason=(
        "@pred_th5_1_at predicts that as $\\underline{A}_T \\to 0$ the bound "
        "becomes vacuous, matching the stalled green curve at "
        "$\\bar A_t \\approx -0.013$."
    ),
    prior=0.9,
)
sup_alt_fig1b = support(
    [alt_purely_random],
    obs_fig1b_distinguishability,
    reason=(
        "Random seed variability could in principle produce the qualitative "
        "spread between curves."
    ),
    prior=0.3,
)
cmp_fig1b = compare(
    pred_th5_1_at, alt_purely_random, obs_fig1b_distinguishability,
    reason=(
        "@pred_th5_1_at specifically predicts the *stall* pattern when the "
        "discriminative strength becomes negative; randomness alone does not "
        "predict the qualitative regime change."
    ),
    prior=0.9,
)
abd_fig1b = abduction(
    sup_h_fig1b, sup_alt_fig1b, cmp_fig1b,
    reason="Theorem 5.1's discriminability prediction best explains the stall in Fig 1(b).",
)

# 1(c) curiosity sweep — the most direct test of the *sufficient curiosity* condition.
sup_h_fig1c = support(
    [pred_th5_1_curiosity],
    obs_fig1c_curiosity,
    reason=(
        "@pred_th5_1_curiosity predicts that sub-threshold $\\beta$ stalls "
        "contraction; Figure 1(c) shows $\\beta=0.05$ stalled and $\\beta\\geq 0.8$ "
        "contracted."
    ),
    prior=0.9,
)
sup_alt_fig1c = support(
    [alt_purely_random],
    obs_fig1c_curiosity,
    reason="Random variability across only 5 seeds could in principle drive the spread.",
    prior=0.25,
)
cmp_fig1c = compare(
    pred_th5_1_curiosity, alt_purely_random, obs_fig1c_curiosity,
    reason=(
        "The qualitative regime change between $\\beta=0.05$ (stalled) and "
        "$\\beta\\geq 0.8$ (converged) is *precisely* the threshold behavior "
        "predicted by the sufficient-curiosity condition; randomness cannot "
        "explain a regime change."
    ),
    prior=0.92,
)
abd_fig1c = abduction(
    sup_h_fig1c, sup_alt_fig1c, cmp_fig1c,
    reason="Theorem 5.1's sufficient-curiosity prediction best explains Fig 1(c).",
)

# --- Theorem 5.1 corroborated by induction over three independent sweeps ---

claim_th5_1_corroborated = claim(
    "**Theorem 5.1 is empirically corroborated** in the discrete sandbox by "
    "three one-factor-at-a-time sweeps: prior-entropy ordering matches the "
    "$H_0$-dependence, the negative-gap stall matches the "
    "$\\underline{A}_T \\to 0$ regime, and the $\\beta=0.05$ stall matches the "
    "sufficient-curiosity threshold.",
    title="Theorem 5.1 corroborated by Figure 1",
)

# Predictions in the generative direction: theorem predicts each observable.
sup_thm_pred_1a = support(
    [claim_theorem_5_1], obs_fig1a_prior_entropy,
    reason="@claim_theorem_5_1 predicts the H_0 dependence observed in Fig 1(a).",
    prior=0.9,
)
sup_thm_pred_1b = support(
    [claim_theorem_5_1], obs_fig1b_distinguishability,
    reason="@claim_theorem_5_1 predicts the discriminability dependence in Fig 1(b).",
    prior=0.9,
)
sup_thm_pred_1c = support(
    [claim_theorem_5_1], obs_fig1c_curiosity,
    reason="@claim_theorem_5_1 predicts the curiosity dependence in Fig 1(c).",
    prior=0.9,
)
ind_th5_1_ab = induction(
    sup_thm_pred_1a, sup_thm_pred_1b, law=claim_theorem_5_1,
    reason=(
        "Sweeps (a) and (b) vary disjoint design knobs (prior mass vs. mean-table "
        "gap structure), giving structurally independent confirmations."
    ),
)
ind_th5_1_abc = induction(
    ind_th5_1_ab, sup_thm_pred_1c, law=claim_theorem_5_1,
    reason=(
        "Sweep (c) varies a third independent knob ($\\beta$), so the three "
        "confirmations are jointly independent evidence for @claim_theorem_5_1."
    ),
)

sup_th5_1_corroborated = support(
    [claim_theorem_5_1],
    claim_th5_1_corroborated,
    reason=(
        "@claim_theorem_5_1 is the law whose three predictions match Figure 1; "
        "the corroboration claim summarizes the inductive support above."
    ),
    prior=0.92,
)

# --- 1D GP bandit setup (Sec. 7.2, Appendix C.2) ---

setup_gp_bandit = setting(
    "**1D GP bandit (Appendix C.2).** Inputs $x\\in[0,1]$ on a uniform grid of "
    "$N=200$ points. True objective "
    "$f(x) = 0.6\\sin(3\\pi x) + 0.4\\cos(5\\pi x) + 0.2 x$, observations "
    "$y_t = f(x_t) + \\epsilon_t$ with $\\epsilon_t\\sim\\mathcal{N}(0,\\sigma^2)$, "
    "$\\sigma = 0.05$. Mutual information is computed in closed form from the GP "
    "predictive variance. Heuristic "
    "$h_t(y) = |y - y^*| + b_t (y - y^*)$, with bias schedules: aligned ($b_t=0$); "
    "constant bias $b_t = 2$; slow exponential decay $b_t = 2 e^{-0.02 t}$; fast "
    "exponential decay $b_t = 2 e^{-0.25 t}$. Five random seeds; error bars "
    "$\\pm 0.2$ std.",
    title="1D GP bandit experimental setup",
)

# --- Two observations from Figure 2 ---

obs_fig2a_misalignment = claim(
    "**Figure 2(a)+left/center (Misalignment sweep).** With $\\beta=1.0$ fixed, "
    "comparing aligned ($B_t=0$), constant-bias, slow-decay, and fast-decay "
    "heuristics shows that larger and longer-lasting bias produces higher "
    "cumulative regret, with the constant-bias trajectory reaching $R_T \\approx 50$ "
    "while the aligned heuristic stays near zero.",
    title="Fig 2(a): heuristic bias contributes additively to cumulative regret",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 2 (left two panels)",
              "caption": "Misalignment sweep at fixed beta=1.0."},
)

obs_fig2b_curiosity = claim(
    "**Figure 2(b) (Curiosity sweep).** With aligned heuristic, comparing "
    "$\\beta\\in\\{6.0, 3.0, 1.0, 0.3\\}$ shows that *once curiosity is "
    "sufficient*, smaller $\\beta$ achieves the lowest regret (e.g., "
    "$\\beta=0.3$ reaches $R_T \\approx 5$ while $\\beta=6.0$ reaches "
    "$R_T \\approx 17.5$); large $\\beta$ over-emphasizes information gain and "
    "incurs additional exploratory regret.",
    title="Fig 2(b): once sufficient, smaller beta yields lower regret",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 2 (right panel)",
              "caption": "Curiosity sweep with aligned heuristic."},
)

# --- Predictions from Theorem 6.1 ---

pred_th6_1_bt = claim(
    "**Prediction from @claim_theorem_6_1 ($B_t$).** The cumulative misalignment "
    "term $\\sum_{t=1}^T B_t$ enters the regret bound additively, so larger and "
    "longer-lasting bias should produce proportionally higher cumulative regret.",
    title="Theorem 6.1 prediction: B_t enters regret additively",
)

pred_th6_1_beta = claim(
    "**Prediction from @claim_theorem_6_1 ($\\bar\\beta_T$).** $\\bar\\beta_T$ "
    "multiplies $\\rho_T$ in the regret bound, so once curiosity is large enough "
    "to ensure validity (the floor from Eq. 8), further increases in $\\beta$ "
    "should *increase* the dominant exploration term and inflate $R_T$.",
    title="Theorem 6.1 prediction: above the floor, larger beta inflates R_T",
)

# --- Abductions for Figure 2 ---

sup_h_fig2a = support(
    [pred_th6_1_bt], obs_fig2a_misalignment,
    reason="@pred_th6_1_bt directly predicts the rank ordering of regret in Fig 2(a).",
    prior=0.9,
)
sup_alt_fig2a = support(
    [alt_purely_random], obs_fig2a_misalignment,
    reason="Random variability could spread the curves, but cannot explain the magnitudes.",
    prior=0.2,
)
cmp_fig2a = compare(
    pred_th6_1_bt, alt_purely_random, obs_fig2a_misalignment,
    reason=(
        "The constant-bias regret growth is approximately *linear* in $t$, "
        "matching the additive $\\sum B_t$ prediction quantitatively."
    ),
    prior=0.92,
)
abd_fig2a = abduction(
    sup_h_fig2a, sup_alt_fig2a, cmp_fig2a,
    reason="Theorem 6.1's B_t prediction best explains Fig 2(a).",
)

sup_h_fig2b = support(
    [pred_th6_1_beta], obs_fig2b_curiosity,
    reason=(
        "@pred_th6_1_beta predicts that, above the curiosity floor, larger "
        "$\\beta$ yields strictly higher cumulative regret. Fig 2(b) shows "
        "exactly this monotone ordering for $\\beta\\in\\{0.3, 1.0, 3.0, 6.0\\}$."
    ),
    prior=0.9,
)
sup_alt_fig2b = support(
    [alt_purely_random], obs_fig2b_curiosity,
    reason="Seed variability is too small to reorder the four curves.",
    prior=0.2,
)
cmp_fig2b = compare(
    pred_th6_1_beta, alt_purely_random, obs_fig2b_curiosity,
    reason=(
        "The clean monotone ordering of four $\\beta$ values across all 30 "
        "iterations is a precise quantitative signature of "
        "$\\bar\\beta_T \\rho_T$ scaling, not random noise."
    ),
    prior=0.92,
)
abd_fig2b = abduction(
    sup_h_fig2b, sup_alt_fig2b, cmp_fig2b,
    reason="Theorem 6.1's beta prediction best explains Fig 2(b).",
)

# --- Theorem 6.1 corroborated by induction over the two GP-bandit sweeps ---

claim_th6_1_corroborated = claim(
    "**Theorem 6.1 is empirically corroborated** in the 1D GP bandit by two "
    "one-factor-at-a-time sweeps: the misalignment sweep matches the additive "
    "$\\sum B_t$ term, and the curiosity sweep matches the $\\bar\\beta_T \\rho_T$ "
    "term, both within the predicted monotone direction.",
    title="Theorem 6.1 corroborated by Figure 2",
)

sup_thm_pred_2a = support(
    [claim_theorem_6_1], obs_fig2a_misalignment,
    reason="@claim_theorem_6_1 predicts the additive bias-regret pattern in Fig 2(a).",
    prior=0.9,
)
sup_thm_pred_2b = support(
    [claim_theorem_6_1], obs_fig2b_curiosity,
    reason="@claim_theorem_6_1 predicts the beta-monotonicity above the floor in Fig 2(b).",
    prior=0.9,
)
ind_th6_1_ab = induction(
    sup_thm_pred_2a, sup_thm_pred_2b, law=claim_theorem_6_1,
    reason=(
        "The two sweeps vary structurally independent design knobs (heuristic "
        "bias schedule vs. curiosity coefficient)."
    ),
)

sup_th6_1_corroborated = support(
    [claim_theorem_6_1],
    claim_th6_1_corroborated,
    reason=(
        "@claim_theorem_6_1 is the law whose two GP-bandit predictions match "
        "Figure 2; the corroboration claim summarizes the induction above."
    ),
    prior=0.9,
)

