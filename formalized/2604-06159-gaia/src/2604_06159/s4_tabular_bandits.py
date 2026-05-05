"""Section 3.1-3.2: Tabular bandit experiments and the within/cross-context analysis.

Sections 3.1 (single-context bandit) and 3.2 (multi-context bandit) of
[@Kaddour2026]. These tabular experiments use *exact* logit-space
gradients (no neural optimizer, no sampling variance for population
updates), so they isolate one mechanism at a time:

* Sec. 3.1 -- single-context $K = 100$-armed bandit with one correct
  action: tests within-context update *quality* (how each method
  closes the policy gap once the correct action has been identified).
* Sec. 3.2 -- multi-context $N = 100$ independent $K = 10$ bandits:
  tests how a normalised step is *allocated across* contexts of
  different difficulty. Provides closed-form per-context coefficients
  $\\beta(p_n)$ for CE, DG, GRPO, TPO (Appendix B).

The Sec. 3.2 derivation -- TPO's coefficient $\\beta_{\\text{TPO}}(p_n) =
p_n(\\lambda - 1) / (1 - p_n + \\lambda p_n)$ stays large at small $p_n$
while DG vanishes linearly and GRPO vanishes as $\\sqrt{p_n}$ -- is the
key analytic explanation for why TPO tracks the cross-entropy oracle
and overtakes the scalar-weighted baselines.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Sec. 3.1: single-context bandit setup + results
# ---------------------------------------------------------------------------

setup_single_context_bandit = setting(
    "**Sec. 3.1 setup.** A $K = 100$-armed bandit with exactly one "
    "correct action $y^*$ and reward $R = \\mathbf{1}\\{A = y^*\\}$. "
    "At each step the agent samples $B = 100$ actions, computes a "
    "gradient estimate, and takes a normalised logit step of size "
    "$\\alpha = 0.1$. Results are averaged over 100 seeds. The "
    "softmax policy and its gradients are computed *exactly* (logit "
    "table; no neural optimizer), following [@Osband2026].",
    title="Setup (3.1): single-context $K=100$ bandit, exact logits, $B=100$, 100 seeds",
)

claim_3_1_tpo_dg_fastest = claim(
    "**Sec. 3.1 result -- TPO and DG converge fastest; PG and GRPO "
    "plateau at higher error.** On the single-context $K=100$ bandit, "
    "TPO and DG continue to drive the policy error $\\varepsilon = 1 - "
    "\\pi(y^*)$ below $10^{-2}$ within 100 normalised steps, while "
    "PG and GRPO plateau near $10^{-1}$ over the same horizon "
    "[@Kaddour2026, Figure 3(a)]. The gap is on the *update quality* "
    "axis: TPO and DG keep concentrating probability on the correct "
    "action even after error has dropped to 1%, while PG and GRPO do "
    "not.",
    title="Result (3.1): TPO and DG drive error below 1%; PG and GRPO plateau",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 3(a)",
        "caption": "Single-context $K=100$ bandit, policy error $1 - \\pi(y^*)$ vs. normalised step.",
    },
)

claim_3_1_tpo_lowest_misalignment = claim(
    "**Sec. 3.1 mechanism -- TPO maintains the lowest misalignment to "
    "the oracle PG direction.** On the same single-context bandit, "
    "TPO's update direction stays closest to the oracle policy-"
    "gradient direction $g^*_{\\text{PG}}$ (lowest $1 - \\cos(g, "
    "g^*_{\\text{PG}})$) throughout training, while GRPO becomes "
    "*increasingly misaligned* as the policy concentrates on $y^*$ "
    "[@Kaddour2026, Figure 3(b)]. This mechanism panel explains why "
    "TPO and DG keep improving past 1% error: their direction stays "
    "useful in the high-confidence regime where GRPO does not.",
    title="Mechanism (3.1): TPO stays closest to oracle PG direction throughout training",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 3(b)",
        "caption": "Misalignment $1 - \\cos(g, g^*_{\\mathrm{PG}})$ vs. normalised step.",
    },
)

# ---------------------------------------------------------------------------
# Sec. 3.2: multi-context bandit setup + results
# ---------------------------------------------------------------------------

setup_multi_context_bandit = setting(
    "**Sec. 3.2 setup.** $N = 100$ independent contexts, each a $K = "
    "10$-armed bandit with $\\mathcal{N}(0, 1)$ logit initialization "
    "[@Osband2026]. The methods use *exact population* updates (no "
    "sampling variance), so any gap reflects how each method "
    "*distributes* a normalised step across contexts of different "
    "difficulty. The cross-entropy (CE) oracle is included as a "
    "reference because it is optimal under normalised steps in this "
    "setting.",
    title="Setup (3.2): $N=100$ contexts $\\times K=10$ arms, exact pop. updates",
)

setup_one_hot_logit_form = setting(
    "**Closed-form scalar reduction (Appendix B).** In the one-hot "
    "reward setting of Sec. 3.2, *every* exact update can be written "
    "in logit space as $g_n = \\beta(p_n) \\, (e_{y_n} - \\pi_n)$, "
    "where $p_n = \\pi_n(y_n)$ is the current correct-action "
    "probability in context $n$ and $\\beta(p_n)$ is a method-"
    "specific scalar. All four methods share the same within-context "
    "direction $e_{y_n} - \\pi_n$; they differ *only* in how the "
    "normalised step budget is allocated across contexts via "
    "$\\beta$. This reduction is what makes the per-context "
    "coefficient comparison meaningful.",
    title="Setup (3.2): all updates have form $g_n = \\beta(p_n)(e_{y_n} - \\pi_n)$",
)

claim_beta_table = claim(
    "**Per-context coefficients (Appendix B).** For the one-hot "
    "tabular bandit with $A = K = 10$ arms and default "
    "$\\eta = 1$, the per-context scalar coefficients are:\n\n"
    "| Method | $\\beta(p_n)$ |\n"
    "|--------|--------------|\n"
    "| CE oracle | $1$ (everywhere) |\n"
    "| DG | $p_n / (1 + p_n)$ |\n"
    "| GRPO | $\\sqrt{p_n / (1 - p_n)}$ |\n"
    "| TPO | $p_n (\\lambda - 1) / (1 - p_n + \\lambda p_n)$ |\n\n"
    "where $\\lambda = \\exp(u_{y_n} - u_{a \\ne y_n}) = "
    "\\exp(A / \\sqrt{A - 1}) \\approx 28$ for $A = 10$ "
    "[@Kaddour2026, Sec. 3.2 and Appendix B].",
    title="Tabular: closed-form $\\beta(p_n)$ for CE, DG, GRPO, TPO",
)

claim_beta_small_p_behavior = claim(
    "**Small-$p_n$ behaviour: TPO stays large, DG/GRPO vanish.** As "
    "$p_n \\to 0$ (a hard, almost-unsolved context), $\\beta_{\\text{DG}} "
    "\\approx p_n$ vanishes *linearly* and $\\beta_{\\text{GRPO}} "
    "\\approx \\sqrt{p_n}$ vanishes as a square root, while "
    "$\\beta_{\\text{TPO}}$ stays comparatively large because of "
    "the $\\lambda \\approx 28$ factor in its numerator. Concretely, "
    "at $p_n = 0.1$ and $A = 10$: $\\beta_{\\text{TPO}} = 0.73$ vs. "
    "$\\beta_{\\text{DG}} = 0.09$ and $\\beta_{\\text{GRPO}} = 0.33$. "
    "Under a normalised step budget, this means DG and GRPO spend "
    "most of the step on already-easy contexts; TPO allocates "
    "comparatively more budget to hard contexts [@Kaddour2026, Sec. "
    "3.2].",
    title="Tabular: at $p_n = 0.1$, $\\beta_{\\text{TPO}} = 0.73$ vs. DG = 0.09 vs. GRPO = 0.33",
)

claim_3_2_tpo_closest_to_ce = claim(
    "**Sec. 3.2 result -- TPO is closest to the CE oracle in both "
    "error and direction.** All methods converge eventually; CE is "
    "fastest. Among the RL updates, TPO is the *closest to CE* in "
    "both average error $1 - \\bar{p}$ (Figure 4(a)) and in update "
    "direction (Figure 4(b), $1 - \\cos(g, g^*_{\\text{CE}})$ stays "
    "near $10^{-3}$ throughout training). DG and GRPO improve "
    "slightly faster at the start of training (early transient) but "
    "TPO overtakes them and finishes with the lowest error of the "
    "three. Sub-claim: this is precisely what one would predict from "
    "the closed-form $\\beta(p_n)$ analysis, since TPO's per-context "
    "weight is closer to CE's flat $\\beta = 1$ than DG/GRPO's "
    "vanishing weights are.",
    title="Result (3.2): TPO matches CE direction; finishes lowest error among RL methods",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 4",
        "caption": "Multi-context bandit: average error and CE-misalignment vs. step.",
    },
)

__all__ = [
    "setup_single_context_bandit",
    "setup_multi_context_bandit",
    "setup_one_hot_logit_form",
    "claim_3_1_tpo_dg_fastest",
    "claim_3_1_tpo_lowest_misalignment",
    "claim_beta_table",
    "claim_beta_small_p_behavior",
    "claim_3_2_tpo_closest_to_ce",
]
