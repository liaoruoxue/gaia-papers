"""Motivation: decoupling 'which completions to upweight' from 'how parameters move'.

Section 1 (Introduction) and abstract of Kaddour 2026 [@Kaddour2026]. The
paper opens with a stylised setup: for a given prompt, sample a small group
of candidate completions, score them, and shift probability mass toward
the better ones. Standard policy-gradient (PG) methods couple this
desired *redistribution of probability mass* to the *optimizer mechanics*
that realise it (learning rate, clipping, KL penalties, importance
ratios), and the resulting update can overshoot or undershoot. The paper
proposes a decoupling: first build a target distribution that encodes
the desired redistribution in closed form, then fit the policy to it by
cross-entropy.

This module captures (a) the operational setup, (b) the conceptual
diagnosis (entanglement of two questions), (c) the proposed remedy
(decoupling via target construction), and (d) the headline empirical
preview from Figure 1 (TPO matches baselines on the dense-reward MNIST
contextual bandit but solves a sparse-reward token-reversal task on
which GRPO and DG stall near random).
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Background settings (operational setup the paper takes as given)
# ---------------------------------------------------------------------------

setup_sample_score_paradigm = setting(
    "**Sample-and-score paradigm.** Given a prompt $x$, the algorithm "
    "samples a group of $K$ candidate completions $y_1, \\ldots, y_K$ "
    "from the current policy $\\pi(\\cdot \\mid x)$ and scores them with "
    "a scalar scorer $S$ to obtain raw scores $s_i = S(x, y_i)$. The RL "
    "update must answer two questions on each batch: (1) *which "
    "completions should gain probability mass*, and (2) *how should the "
    "parameters $\\theta$ move to realise that change*. This setting "
    "covers tabular bandits, contextual bandits, sequence tasks with "
    "per-token or terminal reward, and modern LLM RLVR with verifier "
    "scores. The paper takes this group-based, scored-completion "
    "paradigm as the operational frame [@Kaddour2026].",
    title="Setup: prompt -> sample $K$ completions -> score -> update",
)

setup_target_distribution = setting(
    "**Target distribution on the candidate simplex.** Given the "
    "behavior probabilities $p^{\\text{old}}_i = \\pi^{\\text{old}}(y_i \\mid x) "
    "/ \\sum_j \\pi^{\\text{old}}(y_j \\mid x)$ and standardized scores "
    "$u_i$, the target $q$ is defined on the $K$-simplex over the "
    "*sampled* candidates as $q_i \\propto p^{\\text{old}}_i \\cdot "
    "\\exp(u_i / \\eta)$ with temperature $\\eta > 0$ (Eq. 2 of "
    "[@Kaddour2026]). When $\\eta = 1$ this is the closed-form solution "
    "to $\\arg\\max_r \\{\\sum_i r_i u_i - \\eta \\, \\mathrm{KL}(r \\| "
    "p^{\\text{old}})\\}$ over the simplex. Definition only -- this "
    "setting does not yet assert that fitting to $q$ produces good "
    "learning dynamics.",
    title="Setup: target $q_i \\propto p^{\\text{old}}_i \\exp(u_i / \\eta)$",
)

setup_two_questions = setting(
    "**Two questions of a group-based RL update.** On each rollout "
    "batch, any policy update can be decomposed into: (Q1) the "
    "*target* it implicitly defines on the sampled candidates -- the "
    "discrete distribution toward which the update tries to push the "
    "policy; and (Q2) the *step* it takes in parameter space to "
    "realise that target -- determined jointly by the loss form, "
    "the optimizer, the learning rate, and any clipping or KL "
    "penalties. Standard PG, PPO, GRPO, and DG specify Q1 only "
    "implicitly through their scalar advantage weights, so Q2's "
    "choices (e.g. clip range, KL coefficient) directly distort the "
    "intended Q1. This decomposition is the conceptual frame of the "
    "paper [@Kaddour2026].",
    title="Setup: any group update factors into a target (Q1) + an optimizer step (Q2)",
)

# ---------------------------------------------------------------------------
# The motivating research question
# ---------------------------------------------------------------------------

q_central = question(
    "Can decoupling 'which completions should gain probability mass' "
    "from 'how parameters should move to realise that change' yield a "
    "more robust policy update -- one that matches PG/PPO/GRPO/DG on "
    "easy tasks and outperforms them where reward is sparse?",
    title="Central question: does explicit target/optimizer decoupling pay off?",
)

# ---------------------------------------------------------------------------
# Diagnosis claims (the problem PG-style methods are alleged to have)
# ---------------------------------------------------------------------------

claim_pg_entangles_two_questions = claim(
    "**Standard policy-gradient methods entangle the two questions.** "
    "REINFORCE [@Williams1992REINFORCE], TRPO [@Schulman2015TRPO], PPO "
    "[@Schulman2017PPO], GRPO [@Shao2024GRPO], and DG [@Osband2026] all "
    "answer 'which completions to upweight' (Q1) and 'how to move the "
    "parameters' (Q2) at once: they directly multiply a scalar "
    "advantage weight by $\\nabla \\log \\pi(y \\mid x)$, so the same "
    "update step has to implement both the desired probability "
    "redistribution and the optimizer mechanics. Because Q1 is never "
    "expressed as an explicit target distribution, knobs that "
    "nominally belong to Q2 (learning rate, importance-weight clip "
    "range, KL coefficient, gating sigmoid) directly distort the "
    "intended redistribution.",
    title="Diagnosis: PG/PPO/GRPO/DG entangle Q1 (target) and Q2 (step)",
)

claim_entanglement_makes_pg_fragile = claim(
    "**Entanglement makes PG-style learning fragile, especially under "
    "sparse reward.** When the redistribution and the step are coupled, "
    "the update can overshoot or undershoot depending on the learning "
    "rate, the clip range, and other optimizer choices. Sparse-reward "
    "regimes magnify this fragility because most rollout groups carry "
    "no signal, so the few informative groups have to dominate the "
    "average update, and any miscalibration of step size relative to "
    "those rare informative gradients can stall learning. The paper "
    "frames this fragility as the practical motivation for explicit "
    "Q1/Q2 decoupling [@Kaddour2026, Sec. 1; Figure 1].",
    title="Diagnosis: entanglement -> fragility, especially under sparse reward",
)

# ---------------------------------------------------------------------------
# Proposed remedy (TPO at the conceptual level)
# ---------------------------------------------------------------------------

claim_tpo_decouples = claim(
    "**TPO decouples the two questions by construction.** Target "
    "Policy Optimization (TPO) first builds an explicit target "
    "distribution $q_i \\propto p^{\\text{old}}_i \\exp(u_i / \\eta)$ "
    "on the sampled candidates (Q1, in closed form, no critic, no "
    "inner optimization), then fits the policy to $q$ by cross-entropy "
    "(Q2). Because $q$ is treated as fixed (`stop_gradient`), the "
    "loss-gradient on the sampled-completion logits is exactly $p_\\theta "
    "- q$ (Eq. 3 and Proposition 1 of [@Kaddour2026]), which vanishes "
    "when the policy already matches the target. Reweight-then-fit "
    "dates back to [@Dayan1997EM] and was instantiated by REPS "
    "[@Peters2010REPS] and MPO [@Abdolmaleki2018MPO], but those methods "
    "require learned $Q$-functions and constrained optimization over "
    "action spaces. TPO's contribution is to apply the same principle "
    "to the *finite candidate sets* used in group-based RL, where the "
    "target is closed-form and no critic or dual optimization is "
    "needed.",
    title="Remedy: TPO builds a target (Q1), then cross-entropy-fits to it (Q2)",
)

# ---------------------------------------------------------------------------
# Headline empirical preview from Figure 1
# ---------------------------------------------------------------------------

claim_fig1_dense_match = claim(
    "**Figure 1(a) -- TPO matches baselines on the dense-reward MNIST "
    "contextual bandit.** On the MNIST contextual bandit (Section 3.3), "
    "where each step receives a dense per-action reward $R = "
    "\\mathbf{1}\\{A = Y\\}$, TPO converges *slightly faster* than "
    "GRPO and DG over 10,000 steps (mean +/- s.e. over 20 seeds). All "
    "three methods reach error around 3-6% by step 8,000; the curves "
    "are tightly clustered. This is the 'no-regret' claim: switching "
    "from PG-family baselines to TPO does not cost performance on "
    "easy, dense-reward problems.",
    title="Preview: Fig 1a -- TPO matches GRPO/DG on dense-reward MNIST bandit",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 1(a)",
        "caption": "MNIST contextual bandit, classification error vs. step (mean +/- s.e., 20 seeds).",
    },
)

claim_fig1_sparse_outperform = claim(
    "**Figure 1(b) -- TPO solves the sparse-reward token-reversal task "
    "on which GRPO and DG stall.** On a sparse-reward token-reversal "
    "task (terminal exact-match reward, no per-token signal), GRPO and "
    "DG plateau at exact-match error near 1.0 (random-level) over the "
    "1,500-episode budget, while TPO drives the error to near zero. "
    "Both panels use mean +/- s.e. over 20 seeds. This is the headline "
    "qualitative-gap claim of the paper: sparse reward exposes a "
    "regime where TPO does not just slightly improve, it solves a "
    "task on which the PG-family baselines do not learn at all.",
    title="Preview: Fig 1b -- TPO solves sparse-reward token reversal; GRPO/DG stall",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 1(b)",
        "caption": "Token reversal (sparse reward), exact-match error vs. episode (mean +/- s.e., 20 seeds).",
    },
)

claim_fig1_sparse_qualitative_gap = claim(
    "**Sparse-reward gap is qualitative, not quantitative.** The "
    "Figure 1(b) gap between TPO (near-zero error) and the PG-family "
    "baselines (random-level error) is not a small percentage-point "
    "improvement: it is the difference between *solving the task* and "
    "*not learning at all* within the experimental budget. This "
    "phenomenon, previewed in Figure 1 and reproduced systematically "
    "in Sections 3.5-3.7, is the central empirical finding the paper "
    "asks the reader to explain.",
    title="Preview: the sparse-reward gap is solve-vs-not-learn, not a small delta",
)

# ---------------------------------------------------------------------------
# Headline contributions claim (the paper's announced takeaway)
# ---------------------------------------------------------------------------

claim_headline_contribution = claim(
    "**Headline contribution: TPO matches PG/PPO/GRPO/DG on easy "
    "tasks and substantially outperforms them under sparse reward.** "
    "Across tabular bandits (Sec. 3.1-3.2), MNIST contextual bandit "
    "(Sec. 3.3), dense- and sparse-reward transformer sequence tasks "
    "(Sec. 3.4-3.7), and billion-parameter LLM RLVR (Sec. 3.8), the "
    "paper claims TPO matches policy-gradient (PG), PPO, GRPO, and DG "
    "on dense-reward / easier settings and *substantially outperforms* "
    "them on sparse-reward / harder settings. The reference "
    "implementation is at https://github.com/JeanKaddour/tpo "
    "[@TPOcode].",
    title="Headline contribution: match on easy, outperform on sparse-reward",
)

__all__ = [
    "setup_sample_score_paradigm",
    "setup_target_distribution",
    "setup_two_questions",
    "q_central",
    "claim_pg_entangles_two_questions",
    "claim_entanglement_makes_pg_fragile",
    "claim_tpo_decouples",
    "claim_fig1_dense_match",
    "claim_fig1_sparse_outperform",
    "claim_fig1_sparse_qualitative_gap",
    "claim_headline_contribution",
]
