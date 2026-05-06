"""Motivation: extracting fine-grained credit from hidden states without step-level annotation.

Section 1 (Introduction) and Abstract of [@Chen2026SHEAR]. The paper
opens with a diagnosis of GRPO's coarse-grained credit assignment in
RLVR (every token in a rollout receives the same advantage) and the
process-reward-model (PRM) alternative's reliance on costly step-level
annotation. It then poses a representational alternative: ask whether
the policy model's *own* hidden states already carry a signal correlated
with local reasoning quality, exploitable through span-level Wasserstein
distance between correct and incorrect rollouts in a GRPO group, using
ONLY outcome-level correctness labels.

This module captures (a) the operational setup (RLVR, GRPO group of
rollouts, binary outcome labels), (b) the diagnosis (GRPO is coarse-
grained; PRMs require expensive supervision), (c) the representational
question, and (d) the headline three-fold contribution.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Background settings (operational frame)
# ---------------------------------------------------------------------------

setup_rlvr_grpo_paradigm = setting(
    "**RLVR + GRPO paradigm.** Reinforcement learning with verifiable "
    "rewards (RLVR) is the paradigm: given an input $x$ (e.g. a math "
    "problem), a policy $\\pi_\\theta$ samples a *group* of $G$ "
    "rollouts $\\mathcal{G}(x) = \\{y^{(1)}, \\ldots, y^{(G)}\\}$, "
    "each receiving an outcome-level binary reward $r^{(i)} \\in "
    "\\{0, 1\\}$ (correct / incorrect) from a verifier. Group "
    "Relative Policy Optimization (GRPO) [@Shao2024GRPO] is the "
    "default RLVR algorithm: it computes a group-normalized advantage "
    "$A^{(i)} = (r^{(i)} - \\bar r_G) / (\\sigma_G + \\epsilon)$ and "
    "applies the same scalar $A^{(i)}$ to every token in rollout "
    "$y^{(i)}$ (Eq. 1 of [@Chen2026SHEAR]).",
    title="Setup: RLVR with GRPO -- group rollouts, outcome-level rewards, scalar advantage",
)

setup_credit_assignment_problem = setting(
    "**Credit assignment in long reasoning chains.** A central "
    "challenge in RLVR is *credit assignment*: identifying which "
    "tokens or intermediate steps in a reasoning chain are responsible "
    "for the final outcome. GRPO's uniform advantage assignment leaves "
    "this finer-grained problem unresolved -- a single erroneous step "
    "can derail an otherwise sound trajectory, yet all tokens receive "
    "the same gradient signal regardless of contribution. This is "
    "especially problematic on long-form mathematical reasoning "
    "[@Hendrycks2021MATH; @He2024OlympiadBench] and code generation "
    "[@Liu2023HumanEvalPlus; @Jain2024LiveCodeBench], where chains "
    "routinely span hundreds of tokens.",
    title="Setup: credit assignment problem on long reasoning chains",
)

setup_prm_alternative = setting(
    "**Process Reward Models (PRMs) as the dominant fine-grained "
    "alternative.** PRMs [@Lightman2023PRM; @Cui2025PRIME; "
    "@Cheng2025PURE] assign rewards to individual reasoning steps "
    "rather than only to the final outcome. They have shown clear "
    "advantages over outcome-only supervision but rely on costly "
    "step-level supervision: either human-annotated intermediate "
    "labels or an auxiliary reward model trained on such annotations. "
    "The resulting credit signal therefore depends on the quality of "
    "this supervision, and on complicated tasks the correctness of "
    "intermediate steps is often ambiguous even to experts "
    "[@Cui2025PRIME].",
    title="Setup: PRMs give finer credit but require step-level supervision",
)

setup_hidden_states_carry_signal = setting(
    "**Hidden states as a candidate self-supervised signal.** Modern "
    "transformer LLMs maintain token-level hidden states that summarize "
    "the evolving reasoning context. The paper frames the hypothesis "
    "that reasoning errors should induce systematic *distributional* "
    "differences between correct and incorrect trajectories at the "
    "span level -- differences detectable using only the outcome-level "
    "correctness labels already available in RLVR. The candidate "
    "metric is the Wasserstein distance [@Arjovsky2017WGAN; "
    "@Peyre2019COT] between span-level hidden-state empirical "
    "distributions of correct vs. incorrect rollouts within a GRPO "
    "group.",
    title="Setup: span-level Wasserstein distance on hidden states as a self-supervised signal",
)

# ---------------------------------------------------------------------------
# The motivating question
# ---------------------------------------------------------------------------

q_central = question(
    "Can we obtain process-level credit signals for RLVR *without* "
    "step-level annotation or an additional reward model -- by "
    "extracting them from the policy model's own hidden-state "
    "distributions in each GRPO group?",
    title="Central question: process-level credit from hidden states alone?",
)

# ---------------------------------------------------------------------------
# Diagnosis claims (the problem)
# ---------------------------------------------------------------------------

claim_grpo_coarse_grained = claim(
    "**GRPO performs coarse-grained credit assignment.** In Eq. 1 of "
    "[@Chen2026SHEAR], every token $t$ in rollout $y^{(i)}$ receives "
    "the *same* advantage $A^{(i)}$, regardless of where in the "
    "trajectory the actual reasoning success or failure occurred. "
    "If an incorrect rollout contains mostly correct reasoning but "
    "deviates at some step $\\tau$, tokens before $\\tau$ are "
    "penalized in the same way as those after $\\tau$. This "
    "limitation becomes more severe on complicated tasks requiring "
    "many thinking and execution steps, and is especially problematic "
    "in long-form mathematical reasoning and code generation.",
    title="Diagnosis: GRPO assigns the same advantage to every token in a rollout",
)

claim_prm_supervision_cost = claim(
    "**PRMs require costly step-level supervision and inherit "
    "supervision-quality limits.** Training a PRM typically requires "
    "either human-annotated intermediate labels or an auxiliary reward "
    "model trained on such annotations [@Lightman2023PRM; "
    "@Cui2025PRIME]. This makes the resulting credit signal dependent "
    "on the quality of the supervision and creates an annotation-cost "
    "barrier. The issue is particularly acute on complicated tasks "
    "where the correctness of intermediate steps is ambiguous even to "
    "experts. PRMs also create a transfer-gap problem when the policy "
    "model's capacity exceeds that of the PRM -- a problem amplified "
    "as the policy drifts during RL training.",
    title="Diagnosis: PRMs are annotation-expensive and supervision-quality-bound",
)

# ---------------------------------------------------------------------------
# Headline empirical / theoretical / methodological observations
# ---------------------------------------------------------------------------

claim_hidden_state_signal_exists = claim(
    "**Empirical observation: span-level Wasserstein distance between "
    "hidden-state distributions of correct vs. incorrect rollouts "
    "tracks local reasoning quality.** Within each GRPO group on "
    "MATH500 with Qwen2.5-Math-7B [@Qwen2024Qwen25; @Hendrycks2021MATH], "
    "the Wasserstein distance between span-level hidden-state empirical "
    "distributions of correct and incorrect rollouts increases around "
    "regions where their local reasoning quality diverges. The "
    "association holds (a) at the *aggregate* level -- as prefixes "
    "extend deeper into the chain, continuation success declines while "
    "Wasserstein distance rises (Spearman $\\rho = -0.96$ in Figure 1a), "
    "and (b) at the *local within-trajectory* level -- positions where "
    "$|\\Delta\\text{Accuracy}| \\geq 0.0625$ exhibit a Spearman "
    "$\\rho = -0.42$ between $\\Delta W$ and $\\Delta\\text{Accuracy}$ "
    "(Figure 1b, $p = 4.6 \\times 10^{-59}$). Together these "
    "demonstrate the divergence is a *genuine local* representational "
    "phenomenon, not just an aggregate length effect.",
    title="Contribution 1 (Empirical): hidden-state distributional divergence tracks local reasoning quality",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 1",
        "data": "MATH500 + Qwen2.5-Math-7B; G=8 rollouts; w=100, s=25 sliding window",
    },
)

claim_separation_theorem_announced = claim(
    "**Theoretical foundation: separation theorem.** Under mild "
    "structural assumptions (single divergence point $\\tau$; bounded "
    "hidden-state support; $O(M n^{-1/d})$ empirical-Wasserstein "
    "concentration), post-divergence spans have *strictly larger* "
    "expected Wasserstein distance than pre-divergence spans whenever "
    "the population-level distributional gap $D(S)$ exceeds "
    "$2 \\eta(n, d) = 4 \\tilde C_d M n^{-1/d}$. The result extends to "
    "the *group-level* minimum-distance construction used in "
    "Algorithm 1, providing principled justification for using "
    "Wasserstein distance as a credit-assignment signal "
    "(Theorems 1-2 of [@Chen2026SHEAR]).",
    title="Contribution 2 (Theory): separation theorem for pre vs. post-divergence spans",
    metadata={
        "section": "Section 4 + Appendix C, E, F, G",
    },
)

claim_shear_method_announced = claim(
    "**Method: SHEAR (Span-level Hidden-state Enabled Advantage "
    "Reweighting).** SHEAR modifies GRPO by using span-level "
    "Wasserstein distances $d_k^{(i)}$ to scale the rollout-level "
    "advantage at each token. Concretely, for each rollout $y^{(i)}$ "
    "with opposing-group set $\\mathcal{O}^{(i)}$, the algorithm "
    "(i) computes a min-distance $d_k^{(i)} = "
    "\\min_{y^{(j)} \\in \\mathcal{O}^{(i)}} \\min_{S^{(j)}_\\ell} "
    "W_\\epsilon(\\hat P^{(i)}_k, \\hat P^{(j)}_\\ell)$ for each span, "
    "(ii) divides by the global mean hidden-state norm $\\bar n$, "
    "(iii) max-pools to per-token weight $\\omega^{(i)}_t = "
    "\\frac{1}{\\bar n} \\max_{k: t \\in S^{(i)}_k} d_k^{(i)}$, and "
    "(iv) sets the weighted advantage $\\tilde A^{(i)}_t = A^{(i)} "
    "\\cdot \\omega^{(i)}_t$. Tokens in high-discrepancy regions "
    "receive amplified updates in the existing advantage direction. "
    "The method requires *no additional model*, *no step-level labels*, "
    "and only minimal changes to the training pipeline (Algorithm 1).",
    title="Contribution 3 (Method): SHEAR -- Wasserstein-weighted advantage reweighting in GRPO",
    metadata={
        "algorithm": "Algorithm 1 of [@Chen2026SHEAR]",
        "section": "Section 3",
    },
)

claim_empirical_validation_announced = claim(
    "**Empirical validation: SHEAR improves over GRPO and competes "
    "with PRM-based methods.** Experiments on five mathematical "
    "reasoning benchmarks (AIME24 [@AIMO2024AIME24], AIME25 "
    "[@OpenCompass2025AIME25], AMC23 [@MathAI2023AMC23], MATH500 "
    "[@Hendrycks2021MATH], OlympiadBench [@He2024OlympiadBench]) and "
    "five code generation benchmarks (HumanEval, HumanEval+, MBPP, "
    "MBPP+ [@Liu2023HumanEvalPlus], LiveCodeBench [@Jain2024LiveCodeBench]) "
    "across three backbones (Qwen2.5-Math-7B, Qwen2.5-Coder-7B, "
    "Qwen2.5-14B-Base [@Qwen2024Qwen25], Llama3.1-8B-Instruct "
    "[@Grattafiori2024Llama3]) show consistent improvements over "
    "standard GRPO and strong performance relative to supervised PRM "
    "baselines (PURE [@Cheng2025PURE] and PRM(Reshape adv.) using "
    "Qwen2.5-Math-PRM-7B [@Zhang2025QwenPRM]) -- *while requiring no "
    "additional annotation or reward model training*.",
    title="Contribution 3b (Empirical): SHEAR matches/beats GRPO and PRM baselines",
)

# ---------------------------------------------------------------------------
# Headline contribution: the announced takeaway
# ---------------------------------------------------------------------------

claim_headline_contribution = claim(
    "**Headline contribution: hidden-state distributional divergence is "
    "a viable self-supervised process-level credit signal for RLVR.** "
    "The paper combines three pillars: (1) an empirical finding that "
    "span-level Wasserstein distance between hidden-state distributions "
    "of correct/incorrect rollouts tracks local reasoning quality both "
    "across examples and within individual trajectories; (2) a "
    "separation theorem giving conditional theoretical justification; "
    "(3) the SHEAR algorithm operationalizing the signal as a token-"
    "advantage reweighting in GRPO. The combined result is a "
    "fine-grained credit-assignment method that uses *only* "
    "outcome-level labels already available in RLVR and consistently "
    "improves over both vanilla GRPO and PRM-based baselines, with "
    "<16% computational overhead.",
    title="Headline: self-supervised process-level credit from hidden-state divergence",
)

__all__ = [
    "setup_rlvr_grpo_paradigm",
    "setup_credit_assignment_problem",
    "setup_prm_alternative",
    "setup_hidden_states_carry_signal",
    "q_central",
    "claim_grpo_coarse_grained",
    "claim_prm_supervision_cost",
    "claim_hidden_state_signal_exists",
    "claim_separation_theorem_announced",
    "claim_shear_method_announced",
    "claim_empirical_validation_announced",
    "claim_headline_contribution",
]
