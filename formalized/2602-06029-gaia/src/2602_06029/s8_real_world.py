"""Section 8: Real-world experiments (constrained system identification + composite BO)."""

from gaia.lang import claim, setting, support, abduction, induction, compare
from .motivation import (
    claim_high_curiosity_overexplores,
    claim_contribution_design,
)
from .s5_consistency import claim_theorem_5_1
from .s6_regret import claim_theorem_6_1
from .s7_synthetic_experiments import (
    pred_th5_1_curiosity,
    pred_th6_1_bt,
    pred_th6_1_beta,
)

# --- Constrained system identification (Sec. 8.1, Appendix C.3) ---

setup_csi = setting(
    "**Constrained system identification setup.** Goal: learn unknown system "
    "parameters $\\theta$ when valid observations can only be gathered under "
    "operational constraints $C(y) \\leq 0$. Choose $s = \\theta$ and "
    "$h(y|D_t) = \\mathbb{I}(C(y) > 0)$, giving acquisition\n\n"
    "$$\\alpha(x|D_t) = \\beta\\, I(\\theta;(x,y)|D_t) - "
    "\\mathbb{E}_{p(y|x,D_t)}[\\mathbb{I}(C(y)>0)].$$\n\n"
    "Real-world testbed: 2D plume-field environmental monitoring on a "
    "$100\\times 100$-unit grid with sensor size $a=1.0$, "
    "$\\Delta t = 1.0$ s, plume-rate model "
    "$R_\\theta(x) = R_s/\\log(\\gamma/a)\\cdot\\exp(-\\langle\\theta-x,V\\rangle/(2D))\\cdot K_0(\\|\\theta-x\\|/\\gamma)$ "
    "and Poisson likelihood "
    "$L_\\theta(y|x) = \\exp(-R_\\theta(x)\\Delta t)\\,(R_\\theta(x)\\Delta t)^y / y!$. "
    "Saturation threshold $C(y) = y - y_{\\max}$.",
    title="Constrained system identification: plume-field monitoring",
)

setup_csi_tasks = setting(
    "**Three plume-field tasks (Appendix C.3.2).**\n\n"
    "- **(a) Source localization.** Estimate location $\\theta=[x,y]$ of a "
    "single active source (Source 1; $y_{\\max}=60$); 400 hypotheses on a 5-unit "
    "grid over $[0,100]^2$.\n"
    "- **(b) Wind estimation.** Estimate wind vector $V=[v_x,v_y]$ for a known "
    "source location (Source 2 with true $V=[-0.3, 0.2]$; $y_{\\max}=60$); "
    "400 hypotheses on a 0.1-unit grid over $[-1,1]^2$.\n"
    "- **(c) Active-source identification.** Determine which of six potential "
    "sources are active (true active set: Sources 3, 5, 6, 8 from Sources 3-8; "
    "$y_{\\max}=30$); $2^6 = 64$ hypotheses.",
    title="Plume-field tasks (a)/(b)/(c)",
)

# --- Observation: Figure 3 ablation over beta across tasks (a)/(b)/(c) ---

obs_fig3_csi = claim(
    "**Figure 3 (Constrained System Identification, three panels).** Sweeping "
    "$\\beta\\in\\{0.1, 0.5, 1, 5, 10\\}$ across the three plume-field tasks "
    "shows that:\n\n"
    "- From task (a) to (c) the correlation between sensor measurements and "
    "latent parameters weakens, so the mutual-information term shrinks;\n"
    "- In less informative regimes a *larger* $\\beta$ is needed for the "
    "curiosity term to remain effective;\n"
    "- However, if $\\beta$ is too large, the acquisition becomes overly "
    "exploratory and degrades estimation accuracy (estimation error fails to "
    "decrease or increases).",
    title="Fig 3: optimal beta scales with task informativeness",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 3",
              "caption": "Constrained system identification on environmental monitoring."},
)

# --- Practical guideline distilled from Figure 3 ---

claim_design_guideline_csi = claim(
    "**Design guideline (constrained system identification).** Start with a "
    "moderate $\\beta$; increase it only when the mutual-information term is "
    "consistently small (e.g., due to weak sensor-parameter coupling); stop or "
    "decrease $\\beta$ once further increases no longer reduce, or start to "
    "increase, the estimation error. In practice $\\beta$ should be just large "
    "enough for the curiosity term to matter, but not so large as to induce "
    "unnecessary exploration.",
    title="Design guideline distilled from Figure 3",
)

# Predictions
pred_csi_low_beta_stalls = claim(
    "**Prediction from @claim_theorem_5_1.** When $I(s;(x,y)|D_t)$ is small "
    "(low informativeness), the sufficient-curiosity floor "
    "$\\beta_t \\geq \\min_x \\mathbb{E}[h_t]/I$ is *large*. Setting $\\beta$ "
    "below this floor predicts stalled identification; raising $\\beta$ above "
    "the floor restores convergence.",
    title="Prediction: floor scales inversely with task informativeness",
)

pred_csi_high_beta_overexplores = claim(
    "**Prediction from @claim_theorem_6_1.** Above the floor, the bound's "
    "$\\bar\\beta_T \\rho_T$ term grows in $\\beta$, predicting that pushing "
    "$\\beta$ much higher than necessary degrades estimation/regret performance.",
    title="Prediction: above floor, larger beta degrades performance",
)

# Abduction: Figure 3 patterns are best explained by the joint mechanism of
# both theorems (low-end stall predicted by Th 5.1, high-end degradation by Th 6.1).
sup_h_fig3 = support(
    [pred_csi_low_beta_stalls, pred_csi_high_beta_overexplores],
    obs_fig3_csi,
    reason=(
        "The non-monotone $\\beta$-vs-error relationship in Figure 3 has a "
        "low-$\\beta$ stall (predicted by @pred_csi_low_beta_stalls) and a "
        "high-$\\beta$ degradation (predicted by @pred_csi_high_beta_overexplores), "
        "matching the joint prediction of both theorems."
    ),
    prior=0.9,
)

alt_csi_kernel_only = claim(
    "**Alternative explanation.** The Figure 3 non-monotonicity could be "
    "entirely an artifact of the Poisson likelihood/Bessel-kernel structure of "
    "the plume model, unrelated to the AIF-curiosity mechanism.",
    title="Alternative: plume-model artifact",
)
sup_alt_fig3 = support(
    [alt_csi_kernel_only], obs_fig3_csi,
    reason="The plume model's saturation could in principle produce non-monotone behavior in beta.",
    prior=0.3,
)
cmp_fig3 = compare(
    pred_csi_low_beta_stalls, alt_csi_kernel_only, obs_fig3_csi,
    reason=(
        "The same non-monotone pattern appears across tasks (a)/(b)/(c) which "
        "have *different* plume-model details but share the same AIF mechanism, "
        "so the AIF-curiosity prediction generalizes more naturally than the "
        "model-specific alternative."
    ),
    prior=0.85,
)
abd_fig3 = abduction(
    sup_h_fig3, sup_alt_fig3, cmp_fig3,
    reason="Joint mechanism of Theorems 5.1+6.1 best explains Figure 3.",
)

# Distilled design guideline supported by Figure 3 + theorems
sup_csi_guideline = support(
    [claim_theorem_5_1, claim_theorem_6_1, obs_fig3_csi],
    claim_design_guideline_csi,
    reason=(
        "Combining @claim_theorem_5_1 (which gives a floor on $\\beta$) and "
        "@claim_theorem_6_1 (which penalizes $\\beta$ above what is needed) "
        "with the empirical sweep @obs_fig3_csi yields the practical "
        "moderate-then-tune-up-only-if-needed recipe."
    ),
    prior=0.9,
)

# --- Composite Bayesian optimization (Sec. 8.2, Appendix C.4) ---

setup_cbo = setting(
    "**Composite Bayesian Optimization setup.** Multi-objective BO with an "
    "*unknown* preference function $g(y)$ that must be learned online. "
    "Following [@Lin2022; @Chu2005], $g$ is estimated via probit-likelihood "
    "preference queries from a decision-maker. Choose $s = f_{\\mathcal{X}}$ "
    "and $h(y|D_t) = \\mathrm{EFE}(g(y))$, giving the nested acquisition "
    "(Eq. 11)\n\n"
    "$$\\alpha(x|D_t) = \\beta\\, I(f_x; y|D_t) + "
    "\\mathbb{E}_{p(y|x,D_t)}\\bigl[\\gamma\\, I(g_y; z|D_t) + "
    "\\mathbb{E}_{p(g_y|y,D_t)} g_y\\bigr],$$\n\n"
    "with $x = [x_1, x_2]$ a pair of jointly evaluated candidates and "
    "$\\gamma, \\beta \\geq 0$.",
    title="Composite BO with online preference learning",
)

setup_cbo_task = setting(
    "**Energy-resource-allocation task (Appendix C.4.2).** Distributed Energy "
    "Resources (DERs) deployment in Optimal Power Flow on the IEEE 5-bus "
    "network (`pandapower`). Inputs $x$ are 40-dimensional, outcomes $y$ are "
    "4-dimensional with components: voltage fairness, total cost, priority-area "
    "coverage, resilience.\n\n"
    "**Heuristic models compared:**\n"
    "- Ground-truth preference: $g(y) = a^\\top y$ with $a = [1, -1, 2, 1]$.\n"
    "- Constant-bias $h_0(y) = -a_0^\\top y$ with $a_0 = [1, -1, 10, 1]$.\n"
    "- Learnt $h_1$: query via Eq. 11 with $\\gamma = 1$.\n"
    "- Learnt $h_2$: query via Eq. 11 with $\\gamma = 10$.",
    title="Energy-resource-allocation experimental setup",
)

# --- Observations from Figure 4 ---

obs_fig4a_alignment = claim(
    "**Figure 4(a)+left/center (Heuristic alignment).** Cumulative regret "
    "stabilizes (sub-linear growth) only when the heuristic $h$ (and its bias "
    "$B_t$) converges. The constant-bias heuristic $h_0$ produces approximately "
    "linear regret growth (reaching $R_T \\approx 5000$), while the learned "
    "$h_1$ (with $\\gamma=1$) and $h_2$ (with $\\gamma=10$) show their bias "
    "decreasing over $\\sim 50$ iterations, with $h_1$ achieving lower "
    "long-run regret than $h_2$.",
    title="Fig 4(a): heuristic convergence is necessary for sub-linear regret",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 4 (left two panels)",
              "caption": "Composite BO: heuristic alignment effect."},
)

obs_fig4b_curiosity = claim(
    "**Figure 4(b) (Curiosity sweep).** Sweeping $\\beta\\in\\{0.1, 1, 10\\}$ "
    "with a true heuristic shows that sufficient curiosity is necessary for "
    "regret to converge, *and* once $\\beta$ is large enough to ensure "
    "convergence, increasing $\\beta$ further incurs larger transient regret "
    "before stabilization (the $\\beta=10$ curve overshoots before "
    "converging).",
    title="Fig 4(b): once sufficient, larger beta causes transient overshoot",
    metadata={"figure": "artifacts/2602.06029.pdf, Figure 4 (right panel)",
              "caption": "Composite BO: curiosity sweep."},
)

# --- Abductions for Figure 4 ---

alt_cbo_random = claim(
    "**Alternative explanation.** Figure 4's regret patterns could arise from "
    "the high-dimensional ($x:40$d) IEEE-5-bus problem geometry rather than "
    "from the AIF mechanism per se.",
    title="Alternative: high-dimensional geometry, not AIF mechanism",
)

sup_h_fig4a = support(
    [pred_th6_1_bt], obs_fig4a_alignment,
    reason=(
        "@pred_th6_1_bt directly explains the linear regret growth under "
        "constant bias (un-decreasing $B_t$) versus stabilization under learned "
        "heuristics where $B_t$ shrinks over time."
    ),
    prior=0.9,
)
sup_alt_fig4a = support(
    [alt_cbo_random], obs_fig4a_alignment,
    reason="High-dimensional geometry is a confounder but does not predict the linear vs. sub-linear contrast.",
    prior=0.25,
)
cmp_fig4a = compare(
    pred_th6_1_bt, alt_cbo_random, obs_fig4a_alignment,
    reason=(
        "The qualitative *linear* regret growth under constant bias matches the "
        "additive $\\sum B_t$ term *exactly*; geometry alone cannot pick out "
        "this functional form."
    ),
    prior=0.9,
)
abd_fig4a = abduction(
    sup_h_fig4a, sup_alt_fig4a, cmp_fig4a,
    reason="Theorem 6.1's B_t prediction best explains Fig 4(a).",
)

sup_h_fig4b = support(
    [pred_th6_1_beta, pred_th5_1_curiosity, claim_high_curiosity_overexplores],
    obs_fig4b_curiosity,
    reason=(
        "Below-floor $\\beta=0.1$ matches @pred_th5_1_curiosity (stall), and "
        "above-floor $\\beta=10$ matches @pred_th6_1_beta and "
        "@claim_high_curiosity_overexplores (transient overshoot)."
    ),
    prior=0.9,
)
sup_alt_fig4b = support(
    [alt_cbo_random], obs_fig4b_curiosity,
    reason="Geometry is a confounder but does not predict the floor + overshoot pattern.",
    prior=0.2,
)
cmp_fig4b = compare(
    pred_th6_1_beta, alt_cbo_random, obs_fig4b_curiosity,
    reason=(
        "The two-regime pattern (floor + overshoot) matches the joint "
        "prediction of Theorems 5.1 and 6.1; geometry alone does not."
    ),
    prior=0.9,
)
abd_fig4b = abduction(
    sup_h_fig4b, sup_alt_fig4b, cmp_fig4b,
    reason="Joint Theorems 5.1+6.1 prediction best explains Fig 4(b).",
)

# --- Real-world induction over the two task families ---

claim_real_world_corroborated = claim(
    "**Real-world corroboration.** The two real-world task families—plume-field "
    "monitoring (Sec. 8.1) and IEEE-5-bus DER allocation (Sec. 8.2)—jointly "
    "support Theorems 5.1 and 6.1 across structurally distinct domains "
    "(constraint-driven Poisson observations vs. preference-driven multi-objective "
    "optimization).",
    title="Real-world corroboration of both theorems",
)

sup_overex_csi = support(
    [claim_high_curiosity_overexplores], obs_fig3_csi,
    reason=(
        "@claim_high_curiosity_overexplores predicts that pushing $\\beta$ too "
        "high degrades estimation quality in CSI tasks; this is the high-$\\beta$ "
        "branch of the non-monotonicity in Fig 3."
    ),
    prior=0.85,
)
sup_overex_cbo = support(
    [claim_high_curiosity_overexplores], obs_fig4b_curiosity,
    reason=(
        "@claim_high_curiosity_overexplores predicts that pushing $\\beta$ above "
        "the floor produces transient over-exploration; this is the $\\beta=10$ "
        "overshoot in Fig 4(b)."
    ),
    prior=0.85,
)
ind_real_world = induction(
    sup_overex_csi, sup_overex_cbo,
    law=claim_high_curiosity_overexplores,
    reason=(
        "Both real-world tasks independently exhibit the over-exploration "
        "regime predicted by @claim_high_curiosity_overexplores."
    ),
)

sup_real_world_corroborated = support(
    [claim_theorem_5_1, claim_theorem_6_1, obs_fig3_csi, obs_fig4b_curiosity],
    claim_real_world_corroborated,
    reason=(
        "The two real-world experiments cover qualitatively different problem "
        "structures yet both exhibit the floor+overshoot signature of the AIF "
        "curiosity mechanism predicted jointly by @claim_theorem_5_1 and "
        "@claim_theorem_6_1."
    ),
    prior=0.85,
)

# --- Practical contribution summarized ---

sup_design_contribution = support(
    [claim_design_guideline_csi, obs_fig3_csi, obs_fig4a_alignment, obs_fig4b_curiosity],
    claim_contribution_design,
    reason=(
        "@claim_contribution_design (the practical-design contribution) is "
        "instantiated by @claim_design_guideline_csi (CSI recipe), and is "
        "validated empirically by @obs_fig3_csi, @obs_fig4a_alignment, and "
        "@obs_fig4b_curiosity, which translate the theoretical "
        "$\\beta$-floor/$\\beta$-ceiling tradeoff into actionable rules."
    ),
    prior=0.9,
)

