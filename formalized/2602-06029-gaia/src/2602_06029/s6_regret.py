"""Section 6: No-regret optimization (Theorem 6.1: cumulative regret bound)."""

from gaia.lang import claim, setting, support, deduction, equivalence
from .motivation import (
    setup_aif,
    claim_pragmatic_curiosity_acquisition,
    claim_high_curiosity_overexplores,
)
from .s4_definitions import (
    def_potential_energy,
    def_cumulative_regret,
    def_regret_function,
)
from .s5_consistency import claim_assum_sufficient_curiosity_5

# --- Setup specific to Theorem 6.1 ---

setup_gp_model = setting(
    "**Theorem 6.1 setup.** The unknown function is modeled by a Gaussian Process "
    "prior $f \\sim \\mathcal{GP}(0, k(x,x'))$ with bounded kernel "
    "$k(x,x')\\leq 1$ for all $x,x'\\in\\mathcal{X}$, and Gaussian likelihood "
    "$p(y|f(x)) = \\mathcal{N}(f(x),\\sigma^2)$. The query at time $t$ is again "
    "the AIF policy "
    "$x_t = \\arg\\max_{x}\\{\\beta_t I(s;(x,y)|D_{t-1}) - "
    "\\mathbb{E}_{p(y|x,D_{t-1})}[h_t(y)]\\}$.",
    title="Theorem 6.1 setup: GP prior, bounded kernel, Gaussian likelihood",
)

setup_max_info_gain = setting(
    "**Maximum information gain.** $\\rho_T$ denotes the maximum information gain "
    "achievable after at most $T$ selected points. It controls the size of the "
    "GP-side terms in the regret bound and depends on the kernel and "
    "$\\mathcal{X}$. Constants used in the bound: "
    "$\\zeta_T = 2\\log(m_T/\\delta)$ with positive sequence "
    "$\\{m_t\\}$ satisfying $\\sum_{t\\geq 1} m_t^{-1} = 1$; "
    "$C = 2/\\log(1+\\sigma^{-2})$.",
    title="Auxiliary GP-bound constants",
)

setup_normal_pdf = setting(
    "**Standard normal PDF / CDF.** $\\phi(z) = (2\\pi)^{-1/2}\\exp(-z^2/2)$ is "
    "the standard normal PDF and $\\Phi(\\cdot)$ its CDF. Used in Lemma B.4.",
    title="Standard normal PDF/CDF",
)

axiom_normal_density = claim(
    "For $y\\sim\\mathcal{N}(\\mu,\\sigma^2)$ the density is "
    "$p(y) = (2\\pi\\sigma^2)^{-1/2}\\exp(-(y-\\mu)^2/(2\\sigma^2))$, and the "
    "substitution $z = (y-\\mu)/\\sigma$ gives $p(y)\\,dy = \\phi(z)\\,dz$.",
    title="Normal-density substitution identity",
)

# --- Three assumptions of Theorem 6.1 ---

claim_assum_smoothness = claim(
    "**Assumption (i): Smoothness of task.** The true regret function "
    "$r:\\mathcal{Y}\\to\\mathbb{R}_{\\geq 0}$ is Lipschitz-continuous with "
    "constant $L\\geq 0$:\n\n"
    "$$|r(y_1) - r(y_2)| \\leq L|y_1 - y_2|, \\quad \\forall\\, y_1,y_2\\in\\mathcal{Y}.$$\n\n"
    "This ensures the optimization landscape is well-behaved so the GP can "
    "generalize from observations.",
    title="Assumption (i): Lipschitz smoothness of true regret",
)

claim_assum_heuristic_alignment = claim(
    "**Assumption (ii): Heuristic alignment.** At each iteration, the discrepancy "
    "between the heuristic energy function $h_t(y)$ and the true regret $r(y)$ "
    "is uniformly bounded:\n\n"
    "$$|r(y) - h_t(y)| \\leq B_t, \\quad \\forall\\, y\\in\\mathcal{Y},$$\n\n"
    "where $B_t$ is the maximal heuristic-to-true-regret discrepancy at time $t$.",
    title="Assumption (ii): bounded heuristic-true-regret discrepancy",
)

claim_assum_sufficient_curiosity_6 = claim(
    "**Assumption (iii): Sufficient curiosity (for regret bound).** The curiosity "
    "coefficient satisfies the same lower bound as in Theorem 5.1, "
    "$\\beta_t \\geq \\min_{x}\\mathbb{E}_{p(y|x,D_{t-1})}[h_t(y)] / "
    "I(s;(x,y)|D_{t-1})$, ensuring the value of information is not suppressed by "
    "the expected regret penalty.",
    title="Assumption (iii): sufficient curiosity (Eq. 8)",
)

# Sufficient-curiosity assumptions for the two theorems are *literally the same
# inequality*, so capture this with an equivalence operator.
equiv_sufficient_curiosity = equivalence(
    claim_assum_sufficient_curiosity_5,
    claim_assum_sufficient_curiosity_6,
    reason=(
        "Equation (5) and Equation (8) are character-for-character identical "
        "lower bounds on $\\beta_t$. The paper highlights this shared mechanism "
        "as the unifying point of the two theorems."
    ),
    prior=0.99,
)

# --- Lemmas underlying the proof ---

lemma_b1_info_gain = claim(
    "**Lemma B.1 (Srinivas et al. 2009 [@Srinivas2009], Lemma 5.3).** The "
    "information gain for $T$ selected points equals "
    "$I(y_T; f_T) = \\tfrac{1}{2}\\sum_{t=1}^T \\log(1+\\sigma^{-2}\\sigma_{t-1}^2(x_t))$, "
    "where $\\sigma_{t-1}^2(x_t)$ is the GP predictive variance at $x_t$.",
    title="Lemma B.1: information gain via predictive variances",
)

lemma_b2_concentration = claim(
    "**Lemma B.2 (Srinivas et al. 2009 [@Srinivas2009], Lemma 5.5).** Pick "
    "$\\delta\\in(0,1)$ and set $\\zeta_t = 2\\log(m_t/\\delta)$ with "
    "$\\sum_{t\\geq 1} m_t^{-1} = 1$, $m_t > 0$. Then with probability "
    "$\\geq 1-\\delta$, $|f(x_t) - \\mu_{t-1}(x_t)| \\leq \\zeta_t^{1/2}\\sigma_{t-1}(x_t)$ "
    "for all $t \\geq 1$.",
    title="Lemma B.2: GP concentration",
)

lemma_b3_mi_equality = claim(
    "**Lemma B.3 (Li et al. 2026 [@Li2026], Lemma 3.2).** For any subset "
    "$X \\subseteq \\mathcal{X}$ with corresponding function values $f_X$, "
    "given history $D_t$ and new observations $Y$ at $X$, the mutual information "
    "satisfies $I(f_{\\mathcal{X}}; (X,Y)|D_t) = I(f_X; Y|D_t)$.",
    title="Lemma B.3: mutual information identity",
)

lemma_b4_abs_normal = claim(
    "**Lemma B.4 (Folded-normal expectation).** If $y\\sim\\mathcal{N}(\\mu,\\sigma^2)$ "
    "and $c\\in\\mathbb{R}$, then "
    "$\\mathbb{E}[|y-c|] = (\\mu-c)[1-2\\Phi((c-\\mu)/\\sigma)] + "
    "\\sigma\\sqrt{2/\\pi}\\exp\\{-(c-\\mu)^2/(2\\sigma^2)\\}$, with $\\Phi(\\cdot)$ "
    "the standard normal CDF.",
    title="Lemma B.4: expected absolute deviation under a normal",
)

lemma_b5_per_step_regret = claim(
    "**Lemma B.5 (Per-step regret bound).** Fix $t\\geq 1$. If "
    "$|f(x_t) - \\mu_{t-1}(x_t)| \\leq \\zeta_t^{1/2}\\sigma_{t-1}(x_t)$, then\n\n"
    "$$r(f(x_t)) \\leq \\beta_t I(f(x_t); y_t|D_{t-1}) + "
    "L(\\zeta_t^{1/2} + \\sqrt{2/\\pi})\\sigma_{t-1}(x_t) + B_t.$$\n",
    title="Lemma B.5: instant regret decomposition",
)

# Lemma B.4 is purely a calculation in probability theory (substitution into the
# normal pdf), so deduction is appropriate.
ded_lemma_b4 = deduction(
    [axiom_normal_density],
    lemma_b4_abs_normal,
    background=[setup_normal_pdf],
    reason=(
        "From @axiom_normal_density: substitute $z=(y-\\mu)/\\sigma$ in the "
        "integral $\\int |y-c|p(y)dy$, split at $y=c$, and use "
        "$\\int z\\phi(z)dz = -\\phi(z) + \\mathrm{const}$. The result follows."
    ),
    prior=0.99,
)

# Lemma B.5 is derived deductively from the AIF policy + Lemma B.3 + B.4 +
# Assumptions (i) and (ii), under the Lemma B.2 concentration event.
ded_lemma_b5 = deduction(
    [
        lemma_b3_mi_equality,
        lemma_b4_abs_normal,
        claim_assum_smoothness,
        claim_assum_heuristic_alignment,
        claim_assum_sufficient_curiosity_6,
    ],
    lemma_b5_per_step_regret,
    background=[setup_gp_model, def_potential_energy, claim_pragmatic_curiosity_acquisition],
    reason=(
        "Appendix B proof of Lemma B.5. Sufficient curiosity "
        "(@claim_assum_sufficient_curiosity_6) plus the AIF decision rule give "
        "$\\mathbb{E}[h_t(y_t)] \\leq \\beta_t I(s;(x_t,y_t)|D_{t-1})$. "
        "Since the latent state can be embedded in the whole function "
        "$f_{\\mathcal{X}}$, $I(s;(x_t,y_t)|D_{t-1}) \\leq "
        "I(f_{\\mathcal{X}}; (x_t,y_t)|D_{t-1}) = I(f(x_t); y_t|D_{t-1})$ by "
        "@lemma_b3_mi_equality. Therefore "
        "$r(f(x_t)) \\leq \\beta_t I(f(x_t);y_t|D_{t-1}) + "
        "\\mathbb{E}[r(f(x_t)) - h_t(y_t)]$. Splitting "
        "$r(f(x_t))-h_t(y_t) = (r(f(x_t))-r(y_t)) + (r(y_t)-h_t(y_t))$, the "
        "first piece is bounded via Lipschitz smoothness "
        "(@claim_assum_smoothness) and Lemma B.4 (@lemma_b4_abs_normal) by "
        "$L(\\zeta_t^{1/2}+\\sqrt{2/\\pi})\\sigma_{t-1}(x_t)$, the second by "
        "$B_t$ (@claim_assum_heuristic_alignment)."
    ),
    prior=0.99,
)

# --- The theorem statement ---

claim_theorem_6_1 = claim(
    "**Theorem 6.1 (Cumulative Regret Bound in AIF).** Under assumptions (i)-(iii), "
    "the cumulative regret $R_T = \\sum_{t=1}^T r(f(x_t))$ satisfies, with "
    "probability $\\geq 1-\\delta$ for $\\delta\\in(0,1)$,\n\n"
    "$$R_T \\;\\leq\\; \\bar\\beta_T \\rho_T + L\\bigl(\\zeta_T^{1/2} + "
    "\\sqrt{2/\\pi}\\bigr)\\sqrt{C T \\rho_T} + \\sum_{t=1}^T B_t,$$\n\n"
    "where $\\bar\\beta_T := \\max_{t\\in[1,T]}\\beta_t$, "
    "$\\zeta_T = 2\\log(m_T/\\delta)$, $C = 2/\\log(1+\\sigma^{-2})$, and "
    "$\\rho_T$ is the maximum information gain at most $T$ selected points. "
    "Proof: see Appendix B.",
    title="Theorem 6.1 statement: cumulative regret bound",
)

ded_theorem_6_1 = deduction(
    [
        lemma_b1_info_gain,
        lemma_b2_concentration,
        lemma_b5_per_step_regret,
    ],
    claim_theorem_6_1,
    background=[
        setup_gp_model,
        setup_max_info_gain,
        def_cumulative_regret,
        def_regret_function,
    ],
    reason=(
        "Appendix B proof. Conditioning on the Lemma B.2 concentration event "
        "(@lemma_b2_concentration), summing the per-step regret bound "
        "@lemma_b5_per_step_regret yields "
        "$R_T \\leq \\bar\\beta_T \\sum I(f(x_t);y_t|D_{t-1}) + "
        "L(\\zeta_T^{1/2}+\\sqrt{2/\\pi})\\sum \\sigma_{t-1}(x_t) + \\sum B_t$. "
        "By Lemma B.1 (@lemma_b1_info_gain) and the chain rule the first sum "
        "equals $I(y_T;f_T)$, bounded by $\\rho_T$. For the variance sum, the "
        "kernel bound $k\\leq 1$ gives "
        "$\\sigma_{t-1}^2(x_t) \\leq \\log(1+\\sigma^{-2}\\sigma_{t-1}^2(x_t))/"
        "\\log(1+\\sigma^{-2})$, so $\\sum\\sigma_{t-1}^2 \\leq C\\, I(y_T;f_T)$, "
        "and Cauchy-Schwarz yields "
        "$\\sum \\sigma_{t-1}(x_t) \\leq \\sqrt{T \\cdot C I(y_T;f_T)} \\leq "
        "\\sqrt{C T \\rho_T}$. Combining gives the stated bound. The argument is "
        "purely algebraic given the lemmas, hence deduction is appropriate."
    ),
    prior=0.99,
)

# --- Interpretation of assumptions ---

claim_interp_smoothness = claim(
    "**Interpretation of (i).** Smoothness of the true regret function ensures "
    "the optimization landscape is well-behaved: nearby outcomes yield similar "
    "regret values. This Lipschitz condition allows the GP model to generalize "
    "effectively from observed samples.",
    title="Interpretation: smoothness enables GP generalization",
)

claim_interp_alignment = claim(
    "**Interpretation of (ii).** Heuristic alignment guarantees the agent's "
    "internal model of regret $h_t(y)$ remains close to the true objective's "
    "regret. When the alignment condition holds, optimization steps guided by "
    "$h_t(y)$ remain consistent with the underlying objective.",
    title="Interpretation: alignment keeps optimization on-objective",
)

claim_interp_sufficient_curiosity_6 = claim(
    "**Interpretation of (iii).** Sufficient curiosity enforces that exploration "
    "is adequately weighted to avoid premature exploitation: the agent must not "
    "undervalue informative queries. This is the *same* curiosity requirement as "
    "in Theorem 5.1, highlighting that a minimum exploration pressure is "
    "essential both for consistent learning and for regret minimization.",
    title="Interpretation: same curiosity floor as Theorem 5.1",
)

support_smoothness_interp = support(
    [claim_assum_smoothness, claim_theorem_6_1],
    claim_interp_smoothness,
    reason=(
        "@claim_assum_smoothness directly produces the term "
        "$L(\\zeta_T^{1/2}+\\sqrt{2/\\pi})\\sqrt{CT\\rho_T}$ in "
        "@claim_theorem_6_1: smaller $L$ shrinks this term, reflecting the "
        "well-behaved-landscape interpretation."
    ),
    prior=0.95,
)

support_alignment_interp = support(
    [claim_assum_heuristic_alignment, claim_theorem_6_1],
    claim_interp_alignment,
    reason=(
        "@claim_assum_heuristic_alignment yields the cumulative misalignment "
        "term $\\sum_{t=1}^T B_t$ in @claim_theorem_6_1, so a tighter alignment "
        "(smaller $B_t$) shrinks the bound and keeps optimization on-objective."
    ),
    prior=0.95,
)

support_curiosity_interp_6 = support(
    [claim_assum_sufficient_curiosity_6, claim_theorem_6_1, claim_high_curiosity_overexplores],
    claim_interp_sufficient_curiosity_6,
    reason=(
        "@claim_assum_sufficient_curiosity_6 is required for @lemma_b5_per_step_regret "
        "(invoked inside @claim_theorem_6_1). Without it, the chain "
        "$\\mathbb{E}[h_t]\\leq\\beta_t I$ breaks and the per-step bound "
        "(and hence the cumulative bound) collapses; meanwhile the "
        "$\\bar\\beta_T \\rho_T$ term explains @claim_high_curiosity_overexplores: "
        "too-large $\\beta_t$ inflates the exploration term."
    ),
    prior=0.95,
)

# --- Cumulative regret bound interpretation (the three drivers) ---

claim_regret_drivers = claim(
    "**Cumulative regret bound interpretation.** $R_T$ depends on three drivers:\n\n"
    "- $L$ (smoothness of true regret): smaller $L$ implies a gentler landscape "
    "and faster convergence.\n"
    "- $B_t$ (heuristic-true-regret discrepancy): if $h_t$ is updated to track "
    "$r$, $\\sum B_t$ shrinks and the bound tightens.\n"
    "- $\\bar\\beta_T$ (maximum curiosity): larger curiosity broadens exploration "
    "and yields more information gain, but also inflates the exploration term "
    "$\\bar\\beta_T \\rho_T$.",
    title="Theorem 6.1 cumulative regret: three drivers",
)

ded_regret_drivers = deduction(
    [claim_theorem_6_1],
    claim_regret_drivers,
    reason=(
        "Direct algebraic reading of the bound in @claim_theorem_6_1: $L$ "
        "multiplies the GP variance-sum term, $\\sum B_t$ enters additively, "
        "and $\\bar\\beta_T$ multiplies $\\rho_T$. The signs of the dependencies "
        "are immediate."
    ),
    prior=0.99,
)

# --- Special-case recovery: classical BO regret as a corollary ---

claim_classical_bo_special_case = claim(
    "The classical BO-style cumulative-regret analysis of [@Srinivas2009] is "
    "recovered as a special case of @claim_theorem_6_1: setting $h_t \\equiv r$ "
    "(i.e., $B_t = 0$) and choosing $s = f_{\\mathcal{X}}$ reduces the AIF "
    "acquisition to the Srinivas et al. formulation, and the Theorem 6.1 bound "
    "specializes to the classical $\\bar\\beta_T \\rho_T + L(\\cdot)\\sqrt{C T \\rho_T}$ form.",
    title="Classical BO regret is a special case of Theorem 6.1",
)

support_special_case = support(
    [claim_theorem_6_1, lemma_b3_mi_equality],
    claim_classical_bo_special_case,
    reason=(
        "Plug $B_t = 0$ (perfect alignment) and $s = f_{\\mathcal{X}}$ into "
        "@claim_theorem_6_1; @lemma_b3_mi_equality reduces the mutual-information "
        "term to the form used in [@Srinivas2009]. The remaining inequalities "
        "match the classical GP-UCB regret bound, modulo our explicit "
        "$\\bar\\beta_T$ which corresponds to the UCB exploration constant."
    ),
    prior=0.85,
)

