"""Section 5: Theoretical Analysis -- elimination of SSA at GRPO local optima.

The paper proves (Theorem 5.1) that incorporating the latent-textual
consistency reward $R_{cons}$ into the GRPO total reward causes
superficially aligned policies (those satisfying $p_y \\approx 1$ but
$|p_z - p_y| \\geq \\delta$) to be ruled out as local optima.

The argument is a **proof by contradiction** under three assumptions:

1. **Continuity and Local Controllability** (Assumption 5.1) -- the
   projection head $f_\\omega$ and safety head $g_\\psi$ are Lipschitz
   continuous, and there exist locally perturbed policies $\\tilde\\pi$
   that adjust the final latent representation by at most $\\epsilon$
   while leaving the output distribution unchanged.
2. **GRPO Local Optimality** (Assumption 5.2) -- GRPO converges to a
   local optimum $\\pi^\\star$ of the total reward.
3. **Fixed Textual Evaluator** (Assumption 5.3) -- $P(S|y)$ is fixed
   during policy optimization.

Source: [@Luo2026CRAFT, Sec. 5; Theorem 5.1; Appendix B for full proof].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Formal setup (this section's setup is largely consistent with Sec. 4)
# ---------------------------------------------------------------------------

setup_theorem_setup = setting(
    "**Theorem setup.** Given an input prompt $x$, the reasoning model "
    "with policy $\\pi_\\theta$ generates a trajectory "
    "$\\tau = (y_1, \\ldots, y_T)$ with hidden states $h_t = "
    "H_\\theta(x, y_{\\leq t})$. The final latent representation is "
    "$z_T = f_\\omega(h_T)$. Two safety scores are defined: a *latent* "
    "safety score $p_z = g_\\psi(z_T) \\in [0, 1]$ inferred from the "
    "hidden representation, and a *textual* safety score "
    "$p_y = P(S|y) \\in [0,1]$ produced by an external safety evaluator "
    "on the final output $y$. The consistency reward is "
    "$R_{cons} = 1 - |p_z - p_y|$.",
    title="Setup: latent score p_z = g_psi(z_T), textual score p_y = P(S|y), R_cons = 1 - |p_z - p_y|",
)

# ---------------------------------------------------------------------------
# Definitions, assumptions, and theorem (each as separate atomic claim)
# ---------------------------------------------------------------------------

claim_ssa_definition = claim(
    "**Definition 5.1 (Superficial Safety Alignment).** A policy "
    "$\\pi$ exhibits *superficial safety alignment* if there exists "
    "$\\delta > 0$ such that $p_y \\approx 1$ and $|p_z - p_y| \\geq "
    "\\delta$. This captures the failure mode where the model produces "
    "a safe terminal response while traversing unsafe latent reasoning "
    "states. SSA is precisely the condition Theorem 5.1 rules out at "
    "local optima [@Luo2026CRAFT, Def. 5.1].",
    title="Definition 5.1: SSA as p_y approximately 1 with |p_z - p_y| >= delta",
)

claim_assumption_continuity = claim(
    "**Assumption 5.1 (Continuity and Local Controllability).** The "
    "projection head $f_\\omega$ and safety head $g_\\psi$ are "
    "Lipschitz continuous. Moreover, for any policy $\\pi$ and "
    "sufficiently small $\\epsilon > 0$, there exists a locally "
    "perturbed policy $\\tilde\\pi$ whose *output distribution remains "
    "unchanged* while its final latent representation $z_T$ is "
    "adjusted by at most $\\epsilon$. This is the central regularity "
    "assumption -- it allows the proof to construct a policy "
    "perturbation that improves $R_{cons}$ without affecting $R_{txt}$ "
    "[@Luo2026CRAFT, Asm. 5.1].",
    title="Assumption 5.1: Lipschitz heads + local controllability of latent without output change",
)

claim_assumption_grpo_local_opt = claim(
    "**Assumption 5.2 (GRPO Local Optimality).** GRPO "
    "[@Ramesh2024GRPO] converges to a *local optimal stationary "
    "policy* $\\pi^\\star$ with respect to the total reward "
    "$R_{total} = w_{lat} R_{ls} + w_{txt} R_{txt} + w_{cons} R_{cons}$ "
    "of Equation 4.2. This is a standard convergence assumption for "
    "policy optimization [@Luo2026CRAFT, Asm. 5.2].",
    title="Assumption 5.2: GRPO converges to a local optimum of the total reward",
)

claim_assumption_fixed_evaluator = claim(
    "**Assumption 5.3 (Fixed Textual Evaluator).** The textual safety "
    "evaluator $P(S|y)$ is fixed during policy optimization. This is a "
    "modest but necessary assumption -- it allows the proof to argue "
    "that the perturbed policy's $R_{txt}$ matches that of $\\pi^\\star$ "
    "since the output distribution and the evaluator are both unchanged "
    "[@Luo2026CRAFT, Asm. 5.3].",
    title="Assumption 5.3: P(S|y) evaluator is fixed during training",
)

claim_theorem_5p1_statement = claim(
    "**Theorem 5.1 (Elimination of SSA).** If GRPO converges to a "
    "locally optimal policy $\\pi^\\star$ under Assumptions 5.1, 5.2, "
    "and 5.3, then "
    "$\\mathbb{E}_{\\tau \\sim \\pi^\\star}[|p_z - p_y|] \\leq "
    "\\varepsilon$, where $\\varepsilon$ depends on the reward "
    "variance and the policy entropy. In particular, policies "
    "exhibiting SSA cannot be locally optimal.\n\n"
    "**Argument summary (full proof in Appendix B).** Suppose for "
    "contradiction that $\\pi^\\star$ is locally optimal but exhibits "
    "SSA: $p_y \\approx 1$ and $|p_z - p_y| \\geq \\delta$, so "
    "$R_{cons}(\\pi^\\star) \\leq 1 - \\delta$. By Assumption 5.1, "
    "there exists a perturbed policy $\\tilde\\pi$ with the same output "
    "distribution (hence same $p_y$ and same $R_{txt}$) but with "
    "$|p_z - p_y|$ reduced by a nonzero amount. Since $R_{cons}$ is "
    "continuous and strictly decreasing in $|p_z - p_y|$, there exists "
    "$\\eta > 0$ with "
    "$\\mathbb{E}_{\\tilde\\pi}[R_{cons}] > "
    "\\mathbb{E}_{\\pi^\\star}[R_{cons}] + \\eta$, while "
    "$\\mathbb{E}_{\\tilde\\pi}[R_{txt}] = "
    "\\mathbb{E}_{\\pi^\\star}[R_{txt}]$ (same output distribution). "
    "Therefore $\\mathbb{E}_{\\tilde\\pi}[R_{total}] > "
    "\\mathbb{E}_{\\pi^\\star}[R_{total}]$, contradicting the local "
    "optimality of $\\pi^\\star$. Hence SSA policies cannot persist at "
    "convergence [@Luo2026CRAFT, Theorem 5.1; Appendix B].",
    title="Theorem 5.1: GRPO-with-R_cons local optima satisfy E|p_z - p_y| <= epsilon (no SSA)",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Theorem 5.1 + Appendix B",
        "caption": "Theorem 5.1 + proof in Appendix B: superficially aligned policies cannot be local optima of R_total under the three assumptions.",
    },
)

# ---------------------------------------------------------------------------
# Interpretation: what the theorem rules out and what it does NOT rule out
# ---------------------------------------------------------------------------

claim_theorem_rcons_essential = claim(
    "**The theorem's conclusion essentially relies on $R_{cons}$ "
    "being part of $R_{total}$.** If $R_{cons}$ were absent (i.e., "
    "$w_{cons} = 0$), the same proof would not go through: the "
    "perturbation that reduces $|p_z - p_y|$ would not change "
    "$R_{txt}$ (output is preserved by Assumption 5.1), would not "
    "necessarily change $R_{ls}$ (the latent shift is small but in an "
    "undirected sense), and so the perturbed policy would not be "
    "*strictly* better. The latent-textual consistency reward is the "
    "term that *strictly* improves under the SSA-fixing perturbation; "
    "without it the SSA equilibrium is not ruled out "
    "[@Luo2026CRAFT, Sec. 5; Appendix B].",
    title="Theorem dependency: the elimination of SSA *requires* R_cons in R_total",
)

claim_theorem_implies_grpo_alone_insufficient = claim(
    "**Theorem 5.1 implies that GRPO with output-only safety reward is "
    "insufficient to rule out SSA.** A vanilla GRPO objective with "
    "only $R_{txt}$ (the textual safety reward) does not constrain "
    "$p_z$ at all -- the proof's perturbation argument fails because "
    "$R_{txt}$ alone has no term that decreases when $|p_z - p_y|$ "
    "decreases. Therefore there exist locally optimal GRPO policies "
    "(under output-only reward) that exhibit SSA. The theorem provides "
    "a formal counterpart to the empirical SSA observation: standard "
    "RL alignment cannot solve SSA without a latent-textual "
    "consistency term [@Luo2026CRAFT, Sec. 5].",
    title="Implication: GRPO with output-only reward cannot rule out SSA as local optima",
)

claim_epsilon_depends_on_variance_and_entropy = claim(
    "**The bound $\\varepsilon$ in Theorem 5.1 depends on reward "
    "variance and policy entropy.** The theorem does not establish "
    "$|p_z - p_y| = 0$ in expectation, but rather a bounded gap. The "
    "$\\varepsilon$ is non-zero because GRPO operates on stochastic "
    "rollouts (variance term) and maintains policy entropy (regularizer "
    "term). At higher temperatures / less converged policies, the "
    "$\\varepsilon$ will be larger; at convergence with low entropy, "
    "the gap shrinks toward zero. This explains why the empirical "
    "results (Section 6) show *substantial but not complete* "
    "elimination of SSA -- 79.0% reasoning-safety improvement rather "
    "than 100% [@Luo2026CRAFT, Theorem 5.1].",
    title="Theorem caveat: epsilon > 0 from reward variance + policy entropy",
)

# ---------------------------------------------------------------------------
# Theorem assumptions are mild: argument
# ---------------------------------------------------------------------------

claim_assumptions_mild = claim(
    "**The three assumptions are mild and standard.** Assumption 5.1's "
    "Lipschitz continuity holds for any neural network of finite "
    "weights, and the local-controllability portion is satisfied for "
    "any sufficiently expressive policy class -- this is essentially "
    "saying that the *internal* state of the model can be perturbed by "
    "training without necessarily changing the output. Assumption 5.2 "
    "is the standard convergence assumption for any policy "
    "optimization analysis. Assumption 5.3 (fixed evaluator) is "
    "standard practice during alignment training "
    "[@Luo2026CRAFT, Sec. 5].",
    title="Theorem robustness: the three assumptions are mild and well-motivated",
)

__all__ = [
    "setup_theorem_setup",
    "claim_ssa_definition",
    "claim_assumption_continuity",
    "claim_assumption_grpo_local_opt",
    "claim_assumption_fixed_evaluator",
    "claim_theorem_5p1_statement",
    "claim_theorem_rcons_essential",
    "claim_theorem_implies_grpo_alone_insufficient",
    "claim_epsilon_depends_on_variance_and_entropy",
    "claim_assumptions_mild",
]
