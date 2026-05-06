"""Section 3: Method -- the SHEAR algorithm.

Section 3 of [@Chen2026SHEAR]. Formalises the SHEAR method: GRPO
preliminaries (Eq. 1), span decomposition (Eq. 2), the 1-Wasserstein
distance (Eq. 3) and its Sinkhorn approximation, the four-step
weighted-advantage construction (Algorithm 1, Eqs. 4 + steps 1-4),
and the design choices (max-pooling vs. mean-pooling, global mean-
norm normalization).

Algorithm 1 in detail:
  Step 1: For each span S_k^(i), d_k^(i) = min over opposing-rollout
          spans of W_eps(P_hat_k^(i), P_hat_l^(j)).
  Step 2: Divide by global mean hidden-state norm n_bar (preserves
          ranking within group).
  Step 3: Per-token weight omega_t^(i) = (1/n_bar) max_{k: t in S_k} d_k.
  Step 4: tilde A_t^(i) = A^(i) * omega_t^(i).

For incorrect rollouts (A^(i) < 0), high-discrepancy regions get
larger negative updates. For correct rollouts (A^(i) > 0), high-
discrepancy regions get larger positive updates.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 3.1 Preliminaries: GRPO update form
# ---------------------------------------------------------------------------

setup_grpo_update_eq1 = setting(
    "**GRPO policy gradient (Eq. 1).** For input $x$ a policy "
    "$\\pi_\\theta$ generates a rollout $y^{(i)} = (y^{(i)}_1, \\ldots, "
    "y^{(i)}_{T_i})$ receiving binary reward $r^{(i)} \\in \\{0, 1\\}$. "
    "GRPO samples a group $\\mathcal{G}(x) = \\{y^{(1)}, \\ldots, "
    "y^{(G)}\\}$ and forms the policy gradient $\\nabla_\\theta J = "
    "\\mathbb{E}\\left[\\sum_{t=1}^{T_i} A^{(i)} \\nabla_\\theta \\log "
    "\\pi_\\theta(y^{(i)}_t \\mid y^{(i)}_{<t}, x)\\right]$ where the "
    "group-normalized advantage is $A^{(i)} = (r^{(i)} - \\bar r_G) / "
    "(\\sigma_G + \\epsilon)$ (Eq. 1 of [@Chen2026SHEAR]). The "
    "structural feature: the same scalar $A^{(i)}$ multiplies "
    "$\\nabla_\\theta \\log \\pi_\\theta$ at *every* token in the "
    "rollout.",
    title="Setup: GRPO update -- $\\nabla_\\theta J = E[\\sum_t A^{(i)} \\nabla_\\theta \\log\\pi_\\theta]$",
)

# ---------------------------------------------------------------------------
# 3.2 Span decomposition + Wasserstein distance
# ---------------------------------------------------------------------------

setup_span_decomposition_eq2 = setting(
    "**Span decomposition with sliding window (Eq. 2).** Given a "
    "rollout $y^{(i)}$ of length $T_i$, the paper partitions it into "
    "*overlapping* spans using a sliding window of size $w$ and "
    "stride $s \\leq w$: $\\mathcal{S}^{(i)} = \\{S^{(i)}_k = "
    "[a^{(i)}_k, b^{(i)}_k]\\}$ with $a^{(i)}_k = 1 + (k-1)s$ and "
    "$b^{(i)}_k = \\min(a^{(i)}_k + w - 1, T_i)$. Each span "
    "$S^{(i)}_k$ defines an empirical distribution over hidden states "
    "$\\hat P^{(i)}_k = (1/|S^{(i)}_k|) \\sum_{t \\in S^{(i)}_k} "
    "\\delta_{h^{(i)}_t}$ where $h^{(i)}_t \\in \\mathbb{R}^d$ is the "
    "hidden state at the *last transformer layer before LM-head* "
    "[@Yu2026LatentSpace; @Zhang2025ReLaX] for token $y^{(i)}_t$. "
    "Default hyperparameters: $w = 100$, $s = 25$ (Sec. 5.5).",
    title="Setup: overlapping spans of size $w$, stride $s$; per-span empirical distribution $\\hat P^{(i)}_k$",
)

setup_wasserstein_definition = setting(
    "**1-Wasserstein distance (Eq. 3) and Sinkhorn approximation.** "
    "For distributions $P, Q$ on $\\mathbb{R}^d$ the 1-Wasserstein "
    "distance is $W_1(P, Q) = \\inf_{\\gamma \\in \\Gamma(P, Q)} "
    "\\int \\|x - y\\|_2 \\, d\\gamma(x, y)$ where $\\Gamma(P, Q)$ "
    "is the set of couplings with marginals $P$, $Q$. Intuitively, "
    "$W_1$ is the minimum mass-transport cost. In practice the "
    "algorithm computes the *entropically regularized* approximation "
    "$W_\\epsilon$ via the Sinkhorn algorithm [@Cuturi2013Sinkhorn], "
    "which is GPU-efficient. The approximation satisfies $W_1 \\leq "
    "W_\\epsilon \\leq W_1 + \\epsilon \\log n$ for discrete measures "
    "on $n$ points (Appendix B, Lemma 1). With the paper's "
    "hyperparameters $\\epsilon \\log n \\approx 20.8$, which is "
    "small relative to observed separation gaps (Section 5.1).",
    title="Setup: $W_1$ via Sinkhorn $W_\\epsilon$; bias bound $W_\\epsilon - W_1 \\in [0, \\epsilon\\log n]$",
)

# ---------------------------------------------------------------------------
# Why Wasserstein? (deferred to s5; here just declare the choice)
# ---------------------------------------------------------------------------

claim_w_captures_more_than_mean_shift = claim(
    "**Wasserstein distance captures more than first-moment shift.** "
    "By the Kantorovich--Rubinstein duality, $D(S) = W_1(\\bar P^-_S, "
    "\\bar P^+_S) = \\sup_{\\|f\\|_{\\text{Lip}} \\leq 1} |(1/n) "
    "\\sum_t (\\mathbb{E}_{Q_t}[f] - \\mathbb{E}_{P_t}[f])|$. "
    "Restricting $f$ to linear functions recovers first-moment "
    "differences (mean shift), whereas the supremum over all "
    "1-Lipschitz functions also captures changes in variance, shape, "
    "and other aspects of distributional structure. So $W_1$ is "
    "*strictly more general* than first-moment comparisons based on "
    "span means (Appendix D, Proposition D.1; empirical comparison "
    "with cosine, Chamfer, MMD in Section 5.4).",
    title="Method: $W_1$ strictly generalises mean-shift via KR duality (Appendix D)",
)

# ---------------------------------------------------------------------------
# 3.3 SHEAR Algorithm 1 -- the four steps
# ---------------------------------------------------------------------------

setup_opposing_set_eq4 = setting(
    "**Opposing-set construction (Eq. 4).** The rollout group is "
    "partitioned into correct rollouts $\\mathcal{G}^+$ and incorrect "
    "rollouts $\\mathcal{G}^-$. For each rollout $y^{(i)}$ the "
    "*opposing set* is $\\mathcal{O}^{(i)} = \\mathcal{G}^-$ if "
    "$r^{(i)} = 1$ and $\\mathcal{G}^+$ if $r^{(i)} = 0$. If "
    "$\\mathcal{O}^{(i)} = \\emptyset$ (uniformly correct or "
    "uniformly incorrect group), SHEAR *falls back to the standard "
    "GRPO update* for that rollout. This guarantees correct behaviour "
    "on degenerate groups and is why the diagnostic protocol "
    "(Section 2) and method both require mixed-outcome groups.",
    title="Setup: $\\mathcal{O}^{(i)}$ = opposing-outcome rollouts; fall back to GRPO on $\\mathcal{O}^{(i)} = \\emptyset$",
)

claim_step1_min_distance = claim(
    "**Algorithm 1, Step 1: minimum span-level Sinkhorn distance to "
    "the opposing set.** For each span $S^{(i)}_k$ in rollout "
    "$y^{(i)}$, $d^{(i)}_k = \\min_{y^{(j)} \\in \\mathcal{O}^{(i)}} "
    "\\min_{S^{(j)}_\\ell \\in \\mathcal{S}^{(j)}} W_\\epsilon(\\hat "
    "P^{(i)}_k, \\hat P^{(j)}_\\ell)$ (Algorithm 1, line 4). Taking "
    "the *minimum* makes the signal *conservative with respect to "
    "multiple valid solution paths*: a span receives a large "
    "discrepancy only if it remains dissimilar to *every* candidate "
    "alternative in the opposing set. An alternative aggregation "
    "(e.g. mean-distance) would penalise spans that merely happen to "
    "differ from one of several possible reasoning paths, even if "
    "they match another correct path -- exactly the wrong behaviour "
    "for credit assignment.",
    title="Step 1: $d^{(i)}_k$ = min Sinkhorn distance to opposing-group spans",
)

claim_step2_global_norm_norm = claim(
    "**Algorithm 1, Step 2: global mean-norm normalization.** All "
    "span-level discrepancies are divided by the *global* mean "
    "hidden-state norm $\\bar n = (1/N_G) \\sum_{i=1}^G "
    "\\sum_{t=1}^{T_i} \\|h^{(i)}_t\\|_2$ (Algorithm 1, lines 8-9), "
    "where $N_G = \\sum_i T_i$. Since $\\bar n$ is a *positive "
    "constant shared across the entire group*, this rescaling "
    "**preserves the ordering of span discrepancies within the "
    "group**, so the ranking-based separation established in "
    "Section 4 transfers to the normalized weights. A side effect: "
    "different rollouts may receive different *total* gradient "
    "magnitudes, introducing a form of cross-rollout reweighting "
    "(isolated in the Section 5.4.2 ablation).",
    title="Step 2: divide by global $\\bar n$; preserves intra-group ordering",
)

claim_step3_max_pooling = claim(
    "**Algorithm 1, Step 3: token-level aggregation via max-pooling.** "
    "Since each token $t$ belongs to *multiple overlapping spans*, the "
    "weight is the maximum normalized discrepancy among all spans "
    "covering it: $\\omega^{(i)}_t = (1/\\bar n) \\max_{k: t \\in "
    "S^{(i)}_k} d^{(i)}_k$ (Algorithm 1, line 13). Max-pooling "
    "*emphasises the strongest local discrepancy signal* associated "
    "with each token, especially useful in local transition regions "
    "where overlapping spans may mix low- and high-discrepancy "
    "patterns. Mean-pooling would dilute boundary-token signals by "
    "averaging the post-divergence span weight with overlapping "
    "pre-divergence spans (justification in Appendix H.1).",
    title="Step 3: $\\omega^{(i)}_t = (1/\\bar n) \\max_{k: t \\in S^{(i)}_k} d^{(i)}_k$ (max-pool over covering spans)",
)

claim_step4_weighted_advantage = claim(
    "**Algorithm 1, Step 4: weighted advantage.** The token-level "
    "weighted advantage is $\\tilde A^{(i)}_t = A^{(i)} \\cdot "
    "\\omega^{(i)}_t$ (Algorithm 1, line 17). The semantics: "
    "**(i) For incorrect rollouts** ($A^{(i)} < 0$), tokens in "
    "high-discrepancy regions receive *larger negative updates* -- "
    "the policy is penalised more strongly for tokens whose hidden "
    "states diverged most from the correct group. **(ii) For correct "
    "rollouts** ($A^{(i)} > 0$), tokens in high-discrepancy regions "
    "receive *larger positive updates* -- the policy is reinforced "
    "more strongly for tokens whose hidden states are most distinct "
    "from the incorrect group. The sign of the update is unchanged; "
    "only its *magnitude* is reweighted by the local Wasserstein "
    "signal.",
    title="Step 4: $\\tilde A^{(i)}_t = A^{(i)} \\cdot \\omega^{(i)}_t$ -- amplifies in advantage direction",
)

# ---------------------------------------------------------------------------
# Method-level claims about the algorithm
# ---------------------------------------------------------------------------

claim_self_supervised_no_extra_model = claim(
    "**SHEAR is self-supervised: no extra model, no step-level labels, "
    "minimal pipeline change.** All ingredients -- the hidden states "
    "$h^{(i)}_t$, the binary rewards $r^{(i)}$ partitioning correct "
    "and incorrect rollouts, and the GRPO advantage $A^{(i)}$ -- are "
    "*already produced by standard RLVR with GRPO*. The only added "
    "components are the per-batch Sinkhorn computations and a token-"
    "weight buffer; no step-level annotation, no PRM training, no "
    "reward-model inference at training time.",
    title="Method: SHEAR adds only Sinkhorn computation; everything else already exists in GRPO",
)

claim_advantage_direction_preserved = claim(
    "**SHEAR preserves the sign of every update direction.** Because "
    "$\\omega^{(i)}_t \\geq 0$ (a normalized Wasserstein distance), "
    "$\\text{sign}(\\tilde A^{(i)}_t) = \\text{sign}(A^{(i)})$. SHEAR "
    "*never flips* a token's update direction; it only *rescales the "
    "magnitude*. The method is therefore strictly an advantage-"
    "magnitude reweighting, not a fundamental change to the "
    "credit-assignment direction. In particular, SHEAR cannot turn "
    "a wrong-direction GRPO update into a correct one; its "
    "improvement comes from concentrating gradient mass on the "
    "tokens where the GRPO direction is most reliable.",
    title="Method: $\\omega \\geq 0$ -> sign$(\\tilde A) = $ sign$(A)$ (rescale only)",
)

claim_appendix_h_max_vs_mean = claim(
    "**Appendix H.1: max-pooling > mean-pooling for boundary tokens.** "
    "For a token $t$ at the divergence boundary (belonging to both "
    "pre- and post-divergence spans): max-pooling assigns "
    "$\\omega_t = \\max_{k: t \\in S_k} d_k \\geq d_{\\text{post}}$, "
    "preserving the post-divergence signal; mean-pooling assigns "
    "$\\omega_t = (1/|\\{k: t \\in S_k\\}|) \\sum_k d_k$, which is "
    "diluted by pre-divergence spans. Max-pooling is the conservative "
    "choice: it ensures boundary tokens are weighted by their *most* "
    "discriminative span, which is precisely where credit assignment "
    "is most uncertain and impactful.",
    title="Appendix H.1: max-pooling preserves boundary-token signal; mean-pooling dilutes",
)

__all__ = [
    "setup_grpo_update_eq1",
    "setup_span_decomposition_eq2",
    "setup_wasserstein_definition",
    "setup_opposing_set_eq4",
    "claim_w_captures_more_than_mean_shift",
    "claim_step1_min_distance",
    "claim_step2_global_norm_norm",
    "claim_step3_max_pooling",
    "claim_step4_weighted_advantage",
    "claim_self_supervised_no_extra_model",
    "claim_advantage_direction_preserved",
    "claim_appendix_h_max_vs_mean",
]
