"""Section 1: Introduction and Motivation."""

from gaia.lang import claim, setting, question

# --- Background settings (established framings, not subject to update) ---

setup_seq_decision = setting(
    "A sequential decision-making setting under uncertainty, where an agent must "
    "balance exploration (gathering information to reduce uncertainty about latent "
    "parameters) and exploitation (pursuing task objectives). Decisions are made "
    "iteratively, with each round producing observations that update the agent's beliefs.",
    title="Sequential decision-making under uncertainty",
)

setup_bo_paradigm = setting(
    "Bayesian Optimization (BO) [@Shahriari2016; @Frazier2018]: a goal-seeking paradigm "
    "that selects actions to maximize a reward (or minimize a cost) under uncertainty, "
    "typically emphasizing exploitation tempered by uncertainty-driven exploration.",
    title="Bayesian Optimization paradigm",
)

setup_bed_paradigm = setting(
    "Bayesian Experimental Design (BED) [@Rainforth2023]: an information-seeking "
    "paradigm that selects experiments to maximize information gain about unknown "
    "parameters, often without an explicit performance objective.",
    title="Bayesian Experimental Design paradigm",
)

setup_aif = setting(
    "Active Inference (AIF) [@Friston2010; @Friston2017]: a unifying framework where "
    "action selection is cast as a single variational objective—minimizing the "
    "Expected Free Energy (EFE)—that decomposes into an epistemic term (expected "
    "information gain) and a pragmatic term (expected regret), balanced by a "
    "curiosity coefficient $\\beta_t \\geq 0$.",
    title="Active Inference framework",
)

# --- Research question ---

q_central = question(
    "When can minimizing the Expected Free Energy (EFE) guarantee both "
    "**self-consistent learning** (i.e., the posterior converges to the true "
    "data-generating parameter) and **no-regret optimization** (i.e., the "
    "cumulative regret remains bounded)?",
    title="Central research question",
)

# --- Claims about the tension and the proposed mechanism ---

claim_low_curiosity_is_myopic = claim(
    "If the curiosity coefficient $\\beta_t$ is too low, the EFE-minimizing agent "
    "becomes myopic: it prematurely exploits, fails to resolve uncertainty about the "
    "latent parameter, and the consistency guarantee can be broken.",
    title="Low curiosity yields myopic exploitation",
)

claim_high_curiosity_overexplores = claim(
    "If the curiosity coefficient $\\beta_t$ is too high, the agent over-emphasizes "
    "information gain, devotes resources to unnecessary exploration, discards the "
    "task goal, and incurs catastrophic (large) cumulative regret.",
    title="High curiosity yields catastrophic regret",
)

claim_pragmatic_curiosity_acquisition = claim(
    "Building on AIF, [@Li2026] introduces **pragmatic curiosity**, which implements "
    "AIF as the acquisition rule\n\n"
    "$$\\alpha(x|D_t) = \\beta_t\\, I(s;(x,y)\\mid D_t) - \\mathbb{E}_{p(y|x,D_t)}[h(y|D_t)],$$\n\n"
    "where $s\\in\\mathcal{S}$ is the latent parameter (the learning space), "
    "$h(y|D_t)$ is a problem-dependent potential energy function quantifying the "
    "instantaneous regret associated with outcome $y$, and $\\beta_t\\geq 0$ is the "
    "curiosity coefficient that sets the exchange rate between information gain and "
    "pragmatic cost.",
    title="Pragmatic curiosity acquisition function (Equation 1)",
)

# --- Headline contribution claims (exported) ---

claim_curiosity_is_knowledge = claim(
    "**Main thesis (the slogan \"curiosity is knowledge\").** A *single* condition—"
    "**sufficient curiosity** (a lower bound on $\\beta_t$ that prevents the "
    "epistemic term from being dominated by the pragmatic term)—simultaneously "
    "guarantees (i) Bayesian posterior consistency in learning and (ii) bounded "
    "cumulative regret in optimization for EFE-minimizing AIF agents. Thus "
    "curiosity is elevated from an ad-hoc exploration heuristic into an intrinsic "
    "regularizer that couples belief updating and decision-making.",
    title="Main thesis: sufficient curiosity unifies learning and optimization",
)

claim_contribution_consistency = claim(
    "**Contribution 1.** The paper proves the first sample-complexity bound for "
    "posterior consistency of EFE-minimizing AIF agents (Theorem 5.1). The bound "
    "depends explicitly on prior entropy $H_0$, model discriminability $\\underline{A}_T$, "
    "and the curiosity upper bound $\\bar\\beta_T$.",
    title="Contribution 1: posterior consistency theorem",
)

claim_contribution_regret = claim(
    "**Contribution 2.** The paper proves the first general cumulative-regret bound "
    "for AIF with Gaussian Process settings (Theorem 6.1). The bound holds for "
    "generalized heuristic estimators and regret functions, and recovers the "
    "classical BO-style regret analysis [@Srinivas2009] as a special case.",
    title="Contribution 2: cumulative regret theorem",
)

claim_contribution_design = claim(
    "**Contribution 3.** The paper translates the two theorems into practical "
    "design guidelines for the epistemic-pragmatic balance, hyperparameter "
    "selection, and objective function design in hybrid learning-optimization "
    "problems, validated on synthetic and real-world tasks.",
    title="Contribution 3: practical design guidelines",
)

