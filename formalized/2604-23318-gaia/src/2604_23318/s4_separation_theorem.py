"""Section 4: Theoretical analysis -- the separation theorem.

Section 4 of [@Chen2026SHEAR]. Establishes the conditions under which
post-divergence spans become distinguishable from pre-divergence spans
in expectation. Two main results:

* Theorem 1 (pairwise separation): for a single (correct, incorrect)
  pair with single divergence point tau, post-divergence spans have
  expected W1 lower-bounded by D(S) - eta(n,d) while pre-divergence
  spans have expected W1 upper-bounded by eta(n,d). Strict separation
  when D(S) > 2 eta(n,d).

* Theorem 2 (group-level separation): the same claim transfers to the
  group-level minimum-distance d_min(S) used in Algorithm 1, with
  divergence point tau* = max_k tau_k (latest divergence vs. any
  correct rollout).

Auxiliary results: Proposition F.1 (symmetric for correct rollouts),
Proposition G.1 (piecewise / multiple divergence points), Lemma 1
(Sinkhorn approximation bound). The theory provides *conditional*
support: the strict-separation condition D(S) > 2 eta(n,d) is verified
empirically in Section 5.1.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Stylized assumptions
# ---------------------------------------------------------------------------

setup_a1_divergence_structure = setting(
    "**Assumption (A1) -- Divergence structure.** Consider a correct "
    "rollout $y^+$ and an incorrect rollout $y^-$ generated for the "
    "same input. There exists a *divergence point* $\\tau$ such that "
    "for $t \\leq \\tau$ the hidden states $h^+_t$ and $h^-_t$ are "
    "independent draws from the same marginal $P_t$ (distributional "
    "equivalence, not token-level alignment), while for $t > \\tau$ "
    "the correct rollout remains distributed as $P_t$ and the "
    "incorrect rollout is distributed as $Q_t \\neq P_t$. The "
    "assumption requires *distributional* equivalence, not token-"
    "level alignment: two rollouts may differ in surface form while "
    "still sharing the same hidden-state distribution at the same "
    "reasoning stage. As a stylized model, exact equivalence is an "
    "idealization -- in practice a small residual gap may persist "
    "before $\\tau$. Figure 1a empirically supports treating this "
    "gap as negligible (mean $W$ in the first quartile of prefix "
    "positions $\\approx 0.67$ vs. $\\approx 0.75$ in the last "
    "quartile).",
    title="Assumption (A1): divergence point $\\tau$; $h^\\pm \\sim P_t$ for $t \\leq \\tau$, $h^- \\sim Q_t$ for $t > \\tau$",
)

setup_a2_bounded_support = setting(
    "**Assumption (A2) -- Bounded support.** For all positions $t$, "
    "the hidden states satisfy $\\|h_t\\|_2 \\leq M$. This is satisfied "
    "in practice by modern transformer architectures, which apply "
    "LayerNorm [@Ba2016LayerNorm] or RMSNorm [@Zhang2019RMSNorm] at "
    "each layer, bounding the magnitude of hidden state vectors.",
    title="Assumption (A2): $\\|h_t\\|_2 \\leq M$ (LayerNorm/RMSNorm guarantee)",
)

setup_a3_concentration = setting(
    "**Assumption (A3) -- Finite-sample Wasserstein concentration.** "
    "For independent samples $X_t \\sim P_t$ with $\\|X_t\\|_2 \\leq M$ "
    "and $\\hat P_n = (1/n) \\sum \\delta_{X_t}$, $\\bar P_n = (1/n) "
    "\\sum P_t$, the assumption is $\\mathbb{E}[W_1(\\hat P_n, \\bar "
    "P_n)] \\leq \\tilde C_d M n^{-1/d}$. For i.i.d. samples this is "
    "the classical bound [@Fournier2015EmpiricalW1]; the paper's "
    "setting is independent but not necessarily identically "
    "distributed, so it adopts this rate as an assumption capturing "
    "the *finite-sample noise floor*. Define the noise floor "
    "$\\eta(n, d) := 2 \\tilde C_d M n^{-1/d}$ (Eq. 5).",
    title="Assumption (A3): $E[W_1(\\hat P_n, \\bar P_n)] \\leq \\tilde C_d M n^{-1/d}$; noise floor $\\eta(n,d) = 2\\tilde C_d M n^{-1/d}$",
)

# ---------------------------------------------------------------------------
# Population quantities
# ---------------------------------------------------------------------------

setup_population_distance = setting(
    "**Population distance $D(S)$ on a span.** For a span $S = [a, b]$ "
    "of length $n = b - a + 1$ define the span-level population "
    "mixtures $\\bar P^+_S = (1/n) \\sum_{t=a}^b P_t$ and $\\bar "
    "P^-_S = (1/n) \\sum_{t=a}^b Q_t$ (Eq. 6); in the pre-divergence "
    "regime $\\bar P^-_S = \\bar P^+_S$. The *population distance* is "
    "$D(S) := W_1(\\bar P^-_S, \\bar P^+_S)$ (Eq. 7). Empirical span "
    "distributions are denoted $\\hat P^-_S$ and $\\hat P^+_S$. By "
    "Kantorovich--Rubinstein duality, $D(S) = \\sup_{\\|f\\|_{\\text{Lip}} "
    "\\leq 1} |(1/n) \\sum_t (\\mathbb{E}_{Q_t}[f] - \\mathbb{E}_{P_t}[f])|$.",
    title="Setup: $D(S) = W_1(\\bar P^-_S, \\bar P^+_S)$, the span population distance",
)

# ---------------------------------------------------------------------------
# Theorem 1 (pairwise separation) -- atomized
# ---------------------------------------------------------------------------

claim_thm1_pre_divergence_upper_bound = claim(
    "**Theorem 1, Part (i) -- pre-divergence upper bound.** Under "
    "(A1)-(A3), for a span $S = [a, b]$ of length $n$ in $y^-$ paired "
    "with the corresponding span in $y^+$, if $b \\leq \\tau$ "
    "(pre-divergence), then $\\mathbb{E}[W_1(\\hat P^-_S, \\hat P^+_S)] "
    "\\leq \\eta(n, d)$. *Proof sketch:* both empirical measures are "
    "drawn from the same span-level population mixture $\\bar P_S = "
    "(1/n) \\sum_{t=a}^b P_t$; by the triangle inequality and (A3), "
    "$\\mathbb{E}[W_1(\\hat P^-_S, \\hat P^+_S)] \\leq "
    "\\mathbb{E}[W_1(\\hat P^-_S, \\bar P_S)] + \\mathbb{E}[W_1(\\bar "
    "P_S, \\hat P^+_S)] \\leq 2 \\tilde C_d M n^{-1/d} = \\eta(n, d)$.",
    title="Theorem 1.(i): pre-divergence $E[W_1(\\hat P^-_S, \\hat P^+_S)] \\leq \\eta(n,d)$",
)

claim_thm1_post_divergence_lower_bound = claim(
    "**Theorem 1, Part (ii) -- post-divergence lower bound.** Under "
    "(A1)-(A3), if $a > \\tau$ (post-divergence), then "
    "$\\mathbb{E}[W_1(\\hat P^-_S, \\hat P^+_S)] \\geq D(S) - \\eta(n, "
    "d)$. *Proof sketch:* the reverse triangle inequality gives "
    "$W_1(\\hat P^-_S, \\hat P^+_S) \\geq W_1(\\bar P^-_S, \\bar P^+_S) "
    "- W_1(\\hat P^-_S, \\bar P^-_S) - W_1(\\hat P^+_S, \\bar P^+_S)$. "
    "Taking expectations and applying (A3) to each deviation term "
    "yields $\\mathbb{E}[W_1(\\hat P^-_S, \\hat P^+_S)] \\geq D(S) - "
    "2 \\tilde C_d M n^{-1/d} = D(S) - \\eta(n, d)$.",
    title="Theorem 1.(ii): post-divergence $E[W_1(\\hat P^-_S, \\hat P^+_S)] \\geq D(S) - \\eta(n,d)$",
)

claim_thm1_strict_separation = claim(
    "**Theorem 1, Part (iii) -- strict separation.** Combining (i) "
    "and (ii): if $D(S) > 2 \\eta(n, d)$, then $\\mathbb{E}[W^{\\text{post}}_1] "
    "- \\mathbb{E}[W^{\\text{pre}}_1] \\geq D(S) - 2\\eta(n, d) > 0$. "
    "I.e. the expected post-divergence empirical Wasserstein distance "
    "is *strictly larger* than the expected pre-divergence empirical "
    "Wasserstein distance whenever the population-level distributional "
    "gap exceeds twice the finite-sample noise floor. This is the "
    "key quantitative content of the theorem -- it gives the "
    "*verifiable condition* $D(S) > 2\\eta(n, d)$ under which "
    "Wasserstein distance discriminates pre/post.",
    title="Theorem 1.(iii): if $D(S) > 2\\eta(n,d)$ then $E[W^{post}] > E[W^{pre}]$",
)

# ---------------------------------------------------------------------------
# Theorem 2 -- group-level separation
# ---------------------------------------------------------------------------

setup_group_level_minimum = setting(
    "**Group-level minimum discrepancy used in Algorithm 1.** Consider "
    "an incorrect rollout $y^-$ and a set of correct rollouts "
    "$\\{y^{+,1}, \\ldots, y^{+,K^+}\\}$. For each correct rollout "
    "$y^{+,k}$, let $\\tau_k$ denote its divergence point relative to "
    "$y^-$; define the *latest divergence point* $\\tau^* := \\max_k "
    "\\tau_k$ (the largest position up to which $y^-$ remains "
    "distributionally aligned with at least one correct rollout). "
    "For a span $S$ in $y^-$, the *group-level empirical minimum "
    "discrepancy* is $d_{\\min}(S) := \\min_{k, j} W_1(\\hat P^-_S, "
    "\\hat P^{+,k}_{S_j})$ (Eq. 8) and the *population* counterpart "
    "is $D^*(S) := \\min_{k, j} W_1(\\bar P^-_S, \\bar P^{+,k}_{S_j})$ "
    "(Eq. 9).",
    title="Setup: $\\tau^* = \\max_k \\tau_k$; $d_{\\min}(S)$ and $D^*(S)$",
)

claim_thm2_group_separation = claim(
    "**Theorem 2 -- group-level separation.** Under (A1)-(A3): "
    "(i) if $b \\leq \\tau^*$ then $\\mathbb{E}[d_{\\min}(S)] \\leq "
    "\\eta(n, d)$; (ii) if $a > \\tau^*$ then $\\mathbb{E}[d_{\\min}(S)] "
    "\\geq D^*(S) - \\eta(n, d)$; (iii) if $D^*(S) > 2\\eta(n, d)$ "
    "the expected post-$\\tau^*$ minimum discrepancy is strictly "
    "larger than the expected pre-$\\tau^*$ minimum discrepancy. "
    "*Proof sketch:* if $b \\leq \\tau^*$ at least one correct "
    "rollout has a matching pre-divergence span, so the minimum "
    "admits the pre-divergence pairwise upper bound. If $a > "
    "\\tau^*$ then for *every* opposing span the reverse-triangle "
    "lower bound applies; taking the minimum over all opposing "
    "spans yields the stated result. Full proofs in Appendix E.",
    title="Theorem 2: separation transfers to the group-level minimum used in Algorithm 1",
)

claim_thm2_design_justification = claim(
    "**Theorem 2 directly justifies Algorithm 1's group-level "
    "minimum.** The condition $D^*(S) > 2\\eta(n, d)$ asks whether a "
    "post-divergence span is distributionally distinguishable from "
    "*every* opposing span up to finite-sample noise. A small "
    "$D^*(S)$ does *not* indicate failure of the method: it means "
    "the span is not globally distinctive from correct reasoning in "
    "the model's representation space, in which case assigning a "
    "*low weight* is appropriate. The theorem is explicitly "
    "*conditional* on the population-level separation exceeding the "
    "finite-sample noise floor; the algorithm's behaviour (low "
    "weight on indistinguishable spans, high weight on distinct "
    "spans) is exactly aligned with this conditional structure.",
    title="Theorem 2 -> Algorithm 1: low $D^*$ -> low weight is *correct* behaviour",
)

# ---------------------------------------------------------------------------
# Auxiliary results
# ---------------------------------------------------------------------------

claim_prop_f1_correct_rollouts = claim(
    "**Proposition F.1 -- symmetric separation for correct rollouts.** "
    "The algorithm applies symmetrically: correct rollouts also "
    "compute distances to the opposing (incorrect) group. For a span "
    "$S = [a, b]$ in correct rollout $y^+$ with divergence point "
    "$\\tau$ relative to $y^-$, define $d^+(S) := \\min_j W_1(\\hat "
    "P^+_S, \\hat P^-_{S_j})$. Then (i) $b \\leq \\tau$: $\\mathbb{E}[d^+(S)] "
    "\\leq \\eta(n, d)$; (ii) $a > \\tau$: $\\mathbb{E}[d^+(S)] \\geq "
    "D^+(S) - \\eta(n, d)$. The proof has identical structure to "
    "Theorem 1 with the roles of $P_t$ and $Q_t$ exchanged. Together "
    "with the sign structure of $A^{(i)}$ this gives bidirectional "
    "credit assignment (Remark 1 in Appendix F): post-divergence "
    "tokens in *correct* rollouts also receive amplified positive "
    "updates.",
    title="Proposition F.1: same separation holds for correct rollouts (symmetric proof)",
)

claim_prop_g1_multiple_divergences = claim(
    "**Proposition G.1 -- piecewise / multiple divergence points.** "
    "The single-divergence model (A1) is an analytical simplification. "
    "Real chains may contain multiple divergences or partial self-"
    "corrections. Generalising to regime boundaries $0 = \\tau_0 < "
    "\\tau_1 < \\cdots < \\tau_{2m+1} = T$ alternating between aligned "
    "($h^-_t \\sim P_t$) and drifted ($h^-_t \\sim Q^{(j)}_t \\neq "
    "P_t$) regimes: spans fully contained within an aligned regime "
    "satisfy the pre-divergence bound; spans fully contained within "
    "a drifted regime satisfy the post-divergence bound with regime-"
    "specific $D(S)$; spans straddling a boundary exhibit "
    "*intermediate* distances proportional to the drifted fraction. "
    "The algorithm operates *identically regardless of the number of "
    "divergence points*: it computes $W$ for all spans and lets the "
    "distances encode the local alignment/drift structure.",
    title="Proposition G.1: theorem extends to piecewise-divergence rollouts",
)

claim_lemma1_sinkhorn_approximation = claim(
    "**Lemma 1 (Appendix B) -- Sinkhorn approximation bound.** For "
    "discrete measures on $\\leq n$ points within a ball of radius "
    "$M$: $W_1(P, Q) \\leq W_\\epsilon(P, Q) \\leq W_1(P, Q) + "
    "\\epsilon \\log n$. The Sinkhorn bias $W_\\epsilon - W_1 \\in "
    "[0, \\epsilon \\log n]$ varies across pairs, so $W_\\epsilon$ "
    "does not *automatically* preserve the $W_1$ ordering. However, "
    "when the true separation gap exceeds $\\epsilon \\log n$, the "
    "ranking between pre- and post-divergence spans is robust. With "
    "the paper's hyperparameters $\\epsilon \\log n \\approx 20.8$, "
    "negligible relative to the observed separation gaps "
    "(Section 5.1).",
    title="Lemma 1: Sinkhorn approximation gap $\\leq \\epsilon\\log n$; ranking robust if separation > $\\epsilon\\log n$",
)

claim_remark_c1_non_cancellation = claim(
    "**Remark C.1 (Appendix C.1) -- non-cancellation regularity.** "
    "$D(S) = 0$ would require $(1/n) \\sum_t Q_t = (1/n) \\sum_t P_t$ "
    "as measures, meaning that distributional differences at "
    "individual positions exactly cancel when averaged. This requires "
    "a precise anti-correlation structure across positions in "
    "distribution space. The paper treats $D(S) > 0$ as a *regularity "
    "condition* and verifies it empirically: the monotonically "
    "increasing AUC between correct and incorrect spans in Figure 3 "
    "(right) confirms that post-divergence spans are indeed "
    "distributionally separated in practice.",
    title="Remark C.1: $D(S) > 0$ is a regularity condition, verified empirically in Sec 5.1",
)

claim_appendix_d_first_moment_bound = claim(
    "**Proposition D.1 (Appendix D) -- $W_1$ strictly bounds first-"
    "moment differences.** The population distance $D(S) = "
    "W_1(\\bar P^-_S, \\bar P^+_S)$ satisfies (a) $D(S) \\geq "
    "\\|(1/n) \\sum_{t=a}^b (m^-_t - m^+_t)\\|_2$ where $m^\\pm_t = "
    "\\mathbb{E}_{P_t / Q_t}[h]$ (first-moment / mean-shift bound); "
    "(b) $D(S) \\geq |(1/n) \\sum_t (\\mathbb{E}_{Q_t}[\\|h - c\\|] - "
    "\\mathbb{E}_{P_t}[\\|h - c\\|])|$ for any reference $c$ (shape "
    "bound); (c) $D(S) = \\sup_{\\|f\\|_{\\text{Lip}} \\leq 1} "
    "|(1/n) \\sum_t (\\mathbb{E}_{Q_t}[f] - \\mathbb{E}_{P_t}[f])|$ "
    "(KR duality, optimal). Choosing $f(h) = v^\\top h$ (linear) "
    "recovers (a); $\\phi_c(h) = \\|h - c\\|_2$ recovers (b). The KR "
    "supremum is *strictly more general* than mean shift -- which is "
    "what predicts that mean-only metrics (cosine) should fail "
    "(empirically confirmed in Section 5.4.1).",
    title="Proposition D.1: $W_1$ via KR duality $\\geq$ mean-shift bound (cosine fails for this reason)",
)

__all__ = [
    "setup_a1_divergence_structure",
    "setup_a2_bounded_support",
    "setup_a3_concentration",
    "setup_population_distance",
    "setup_group_level_minimum",
    "claim_thm1_pre_divergence_upper_bound",
    "claim_thm1_post_divergence_lower_bound",
    "claim_thm1_strict_separation",
    "claim_thm2_group_separation",
    "claim_thm2_design_justification",
    "claim_prop_f1_correct_rollouts",
    "claim_prop_g1_multiple_divergences",
    "claim_lemma1_sinkhorn_approximation",
    "claim_remark_c1_non_cancellation",
    "claim_appendix_d_first_moment_bound",
]
