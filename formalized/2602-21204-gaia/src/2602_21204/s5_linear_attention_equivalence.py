"""Section 5: TTT is Secretly Linear Attention.

The theoretical core of the paper. Three theorems establish that
TTT-with-KV-binding can be analytically rewritten as a learned linear
attention operator:

* Theorem 5.1 (single-step linearization): one inner-loop GD step on a
  bias-free linear-final-layer fast-weight network induces a linear
  attention output.
* Theorem 5.2 (sequential unrolling): repeated application yields the
  extended linear-attention form $o_t = \\hat{q}_t (S_0 +
  \\sum_{i \\le t} \\hat{k}_i^\\top \\hat{v}_i)$.
* Theorem 5.3 (momentum extension): the same form survives momentum-
  augmented updates with a momentum-weighted effective value.

Section 5.2 explains the four anomalies of Section 4 in this framework.
Sections 5.3-5.4 instantiate the framework on LaCT and ViTTT
(GLU + depthwise convolution), which are also the two empirical reference
architectures.
"""

from gaia.lang import claim, setting, support, deduction, abduction, compare, contradiction

from .motivation import (
    claim_memorization_hypothesis,
    claim_anomaly_distributional_asymmetry_preview,
    claim_anomaly_replace_q_with_k_preview,
    claim_anomaly_inner_vs_outer_preview,
    claim_anomaly_gradient_ascent_preview,
    claim_contribution_equivalence,
)
from .s2_related_work import (
    setup_linear_attention,
    claim_prior_la_equivalence_restricted,
    claim_ttt_shares_la_compute_profile,
    claim_complexity_drift_under_memorization,
    claim_deltanet_equals_linear_ttt,
)
from .s3_preliminaries import (
    setup_fast_weights,
    setup_kvq_projection,
    setup_inner_loop_loss,
    setup_update_then_query,
    setup_inner_loop_hyperparameters,
)
from .s4_anomalies import (
    claim_anomaly_inner_vs_outer,
    claim_anomaly_gradient_ascent,
    claim_anomaly_distributional_asymmetry,
    claim_anomaly_replace_q_with_k,
    claim_memorization_view_falsified,
)

# ---------------------------------------------------------------------------
# Structural premises for the theorems
# ---------------------------------------------------------------------------

setup_linear_final_layer_assumption = setting(
    "**Structural assumption (Sec. 5.1).** The fast-weight inner-loop "
    "function takes the form $f(x) = \\phi(x; \\Theta) W$, where "
    "$\\phi(x; \\Theta) \\in \\mathbb{R}^{D_h}$ is the hidden "
    "representation of the inner-loop network with parameters $\\Theta$, "
    "and $W \\in \\mathbb{R}^{D_h \\times D_\\text{out}}$ is the *bias-free* "
    "weight matrix of the final linear layer. This factorization is the "
    "*only* structural condition required by Theorems 5.1-5.3.",
    title="Structural assumption: bias-free linear final layer $f(x) = \\phi(x; \\Theta) W$",
)

claim_assumption_holds_for_studied_archs = claim(
    "**Assumption holds for studied architectures.** The bias-free "
    "linear-final-layer factorization $f(x) = \\phi(x; \\Theta) W$ "
    "(@setup_linear_final_layer_assumption) is satisfied by all TTT-KVB "
    "variants analyzed in this paper: LaCT [@Zhang2025] (the SwiGLU MLP "
    "ends with $W_1$), ViTTT [@Han2025] (the GLU output is fed to a "
    "linear projection), and Titans [@Behrouz2024]. Theorems 5.1-5.3 "
    "therefore *apply* to the architectures the paper studies. Outside "
    "this class (e.g. inner loops with non-linear final layers or biases) "
    "the analysis would not directly apply, as acknowledged in Section 7.",
    title="The bias-free linear-final-layer assumption holds for LaCT, ViTTT, Titans",
    background=[setup_linear_final_layer_assumption],
)

setup_one_step_gd = setting(
    "**One-step gradient descent (Sec. 5.1).** At step $t$, the inner "
    "loop performs a single gradient descent step on the loss "
    "$\\mathcal{L}(f_t(k))$ with learning rate $\\eta$, updating *all* "
    "trainable parameters simultaneously: "
    "$(W_{t+1}, \\Theta_{t+1}) = (W_t, \\Theta_t) - \\eta \\nabla_{(W_t, "
    "\\Theta_t)} \\mathcal{L}(f_t(k))$.",
    title="Setting: one-step inner-loop GD update of $(W_t, \\Theta_t)$",
)

setup_momentum_update = setting(
    "**Momentum-augmented update (Sec. 5.3 Theorem).** The momentum "
    "accumulator is "
    "$(\\Delta W_t, \\Delta \\Theta_t) = \\nabla_{(W, \\Theta)} \\mathcal{L}"
    "(f_t(k_t)) + \\alpha_t (\\Delta W_{t-1}, \\Delta \\Theta_{t-1})$, "
    "where $\\alpha_t$ is the (possibly token-dependent) momentum factor "
    "at step $t$. The parameter update is "
    "$(W_{t+1}, \\Theta_{t+1}) = (W_t, \\Theta_t) - \\eta(\\Delta W_t, "
    "\\Delta \\Theta_t)$. Define the cumulative momentum coefficient "
    "$\\beta_i^j = \\prod_{s=i+1}^j \\alpha_s$ for $i < j$ and $\\beta_i^i "
    "= 1$.",
    title="Setting: momentum-augmented inner-loop update with cumulative coefficient $\\beta_i^j$",
)

# ---------------------------------------------------------------------------
# 5.1 Theorem 5.1: single-step linearization
# ---------------------------------------------------------------------------

claim_thm_5_1 = claim(
    "**Theorem 5.1 (single-step linearization, Sec. 5.1).** Under the "
    "linear bias-free final-layer assumption "
    "(@setup_linear_final_layer_assumption) and one inner-loop gradient "
    "step (@setup_one_step_gd), the output of the *updated* TTT model on "
    "a query $q$ can be written as\n\n"
    "$$o = \\phi_{t+1}(q) \\bigl( W_t + \\phi_t(k)^\\top g_t(k) \\bigr), "
    "\\qquad g_t(k) \\triangleq -\\eta \\frac{\\partial \\mathcal{L}}"
    "{\\partial f_t(k)}.$$\n\n"
    "Algebraically this is a linear attention operator (cf. "
    "@setup_linear_attention) of the form "
    "$o = \\hat{q}\\bigl(S_0 + \\hat{k}^\\top \\hat{v}\\bigr)$, with "
    "$\\hat{q} = \\phi_{t+1}(q)$, $\\hat{k} = \\phi_t(k)$, "
    "$\\hat{v} = g_t(k)$, $S_0 = W_t$. **Proof: Appendix B.**",
    title="Theorem 5.1: one-step inner-loop GD induces a single-token linear-attention output",
    background=[setup_linear_final_layer_assumption, setup_one_step_gd, setup_linear_attention],
    metadata={"source_section": "artifacts/2602.21204.pdf, Sec. 5.1, Appendix B"},
)

# ---------------------------------------------------------------------------
# 5.1 Theorem 5.2: sequential unrolling
# ---------------------------------------------------------------------------

claim_thm_5_2 = claim(
    "**Theorem 5.2 (sequential unrolling, Sec. 5.1).** Given a sequence "
    "of query-key pairs $\\{(q_0, k_0), \\ldots, (q_t, k_t)\\}$ with one "
    "GD step per input, repeated application of Theorem 5.1 (@claim_thm_5_1) "
    "yields the closed-form parameter trajectory\n\n"
    "$$W_{t+1} = W_0 + \\sum_{i=0}^t \\phi_i(k_i)^\\top g_i(k_i),$$\n\n"
    "and the output\n\n"
    "$$o_t = \\hat{q}_t\\Bigl(S_0 + \\sum_{i=0}^t \\hat{k}_i^\\top "
    "\\hat{v}_i\\Bigr), \\qquad \\hat{q}_t = \\phi_{t+1}(q_t),\\; "
    "\\hat{k}_i = \\phi_i(k_i),\\; \\hat{v}_i = g_i(k_i),\\; S_0 = W_0.$$ "
    "This is the **extended linear-attention form** on a sequential input. "
    "**Proof by induction on $t$: Appendix C.**",
    title="Theorem 5.2: sequential TTT = extended linear-attention $o_t = \\hat{q}_t(S_0 + \\sum \\hat{k}_i^\\top \\hat{v}_i)$",
    background=[setup_linear_final_layer_assumption, setup_one_step_gd, setup_linear_attention],
    metadata={"source_section": "artifacts/2602.21204.pdf, Sec. 5.1 (Theorem 5.2), Appendix C"},
)

# ---------------------------------------------------------------------------
# 5.1 Theorem 5.3: momentum extension
# ---------------------------------------------------------------------------

claim_thm_5_3 = claim(
    "**Theorem 5.3 (momentum extension, Sec. 5.1).** With the momentum-"
    "augmented update (@setup_momentum_update), unrolling the recurrence "
    "and evaluating on query $q_t$ yields\n\n"
    "$$o_t = \\phi_{t+1}(q_t)\\Bigl( W_0 + \\sum_{i=0}^t \\phi_i(k_i)^\\top "
    "m_i(k_i)\\Bigr), \\qquad m_i(k_i) \\triangleq g_i(k_i) \\cdot "
    "\\sum_{j=i}^t \\beta_i^j.$$\n\n"
    "This is identical in form to Theorem 5.2, except that the effective "
    "value $\\hat{v}_i$ is the *momentum-weighted sum* "
    "$m_i(k_i)$ of the per-step gradients, not the instantaneous gradient. "
    "**Proof by induction with cumulative-momentum bookkeeping: "
    "Appendix D.**",
    title="Theorem 5.3: momentum is absorbed into the effective value $\\hat{v}_i = m_i(k_i)$",
    background=[setup_linear_final_layer_assumption, setup_momentum_update, setup_linear_attention],
    metadata={"source_section": "artifacts/2602.21204.pdf, Sec. 5.1 (Theorem 5.3), Appendix D"},
)

# ---------------------------------------------------------------------------
# Top-level theoretical claim: TTT-KVB == learned linear attention.
# ---------------------------------------------------------------------------

claim_ttt_is_linear_attention = claim(
    "**Theoretical headline.** A broad class of TTT-with-KV-binding "
    "architectures -- specifically, those whose fast-weight network has "
    "a *linear bias-free final layer* (@setup_linear_final_layer_assumption) "
    "-- is *analytically equivalent* to a learned linear attention "
    "operator. The class includes single-step and unrolled GD updates "
    "(Theorems 5.1, 5.2 -- @claim_thm_5_1, @claim_thm_5_2), as well as "
    "momentum-augmented updates (Theorem 5.3 -- @claim_thm_5_3). The "
    "inner loop does *not* perform meta-learning in the conventional "
    "sense; instead it parameterizes a *structured history-dependent "
    "mixing* of $q$, $k$, $v$ vectors via the learnable kernel $\\phi$ "
    "and the effective value $\\hat{v}_i$. This generalizes the "
    "single-linear-layer reduction of Sun et al. (2025) "
    "(@claim_prior_la_equivalence_restricted) to multi-layer non-linear "
    "MLPs and momentum.",
    title="TTT-with-KV-binding == learned linear attention (Theorems 5.1-5.3 jointly)",
)

# ---------------------------------------------------------------------------
# 5.2 Linear-attention explanations of the four anomalies
# ---------------------------------------------------------------------------

claim_la_explains_anomaly_inner_vs_outer = claim(
    "**Linear-attention explanation of Anomaly 3 (Sec. 5.2).** Under "
    "Theorem 5.1, the inner loop does not *store* KV information; it "
    "*defines* an operator that depends on the inner-loop hyperparameters "
    "(including the number of optimization steps). Increasing the number "
    "of inner-loop iterations at *inference time only* induces an "
    "attention operator different from the one used at training time. "
    "Performance therefore degrades because of *train-test operator "
    "mismatch*, not because of degraded memorization. This naturally "
    "matches the observed monotone PSNR/perplexity degradation of "
    "Anomaly 3.",
    title="Anomaly 3 explained: more inner steps $\\Rightarrow$ different operator $\\Rightarrow$ train-test mismatch",
    background=[setup_inner_loop_hyperparameters],
)

claim_la_explains_anomaly_grad_ascent = claim(
    "**Linear-attention explanation of Anomaly 4 (Sec. 5.2).** Under "
    "Theorem 5.1 (@claim_thm_5_1), the effective value vector is "
    "$\\hat{v}_t = g_t(k) = -\\eta \\partial \\mathcal{L} / \\partial f_t(k)$. "
    "Replacing gradient descent by gradient ascent simply *flips the "
    "sign* of $g_t(k)$, hence of $\\hat{v}_t$. Since the surrounding "
    "value-projection slow weights are *learnable* and trained jointly "
    "under the downstream objective, the sign flip is absorbed into the "
    "learned mapping. The model adapts trivially, explaining why "
    "performance is preserved or even improved (Anomaly 4).",
    title="Anomaly 4 explained: gradient-sign flip is absorbed by the learned value projection",
)

claim_la_explains_anomaly_qk_asymmetry = claim(
    "**Linear-attention explanation of Anomaly 1 (Sec. 5.2).** Under "
    "the linear-attention view, $q$ determines the *effective query* "
    "via $\\phi_{t+1}(q)$, while $k$ determines the *effective key and "
    "value* via $\\phi_t(k)$ and $g_t(k)$. They drive distinct components "
    "of the attention operator and need not lie in the same semantic "
    "space at all. Distributional mismatch between $Q$ and $K$ is "
    "therefore *expected*, not pathological -- they are intermediate "
    "features that the model maps to different roles, not symmetric "
    "query-key probes (Anomaly 1).",
    title="Anomaly 1 explained: $q$ and $k$ drive distinct components, asymmetry is expected",
)

claim_la_explains_anomaly_replace_q = claim(
    "**Linear-attention explanation of Anomaly 2 (Sec. 5.2).** Replacing "
    "$q$ with $k$ does *not* collapse the mechanism because the effective "
    "query $\\phi_{t+1}(k)$ and the effective key $\\phi_t(k)$ remain "
    "distinct: $\\phi$ is learnable, evaluated at different parameter "
    "states ($\\Theta_{t+1}$ vs $\\Theta_t$), and the model can map the "
    "same input to different representations through the dynamic kernel. "
    "Attention functionality is preserved (Anomaly 2).",
    title="Anomaly 2 explained: $\\phi_{t+1}(k) \\neq \\phi_t(k)$, so substitution preserves functionality",
)

claim_anomalies_explained_by_la_view = claim(
    "**Synthesis (Sec. 5.2).** Viewed through the lens of linear "
    "attention (@claim_ttt_is_linear_attention), all four empirical "
    "anomalies of Section 4 follow naturally from representation-learning "
    "and train-test consistency considerations:\n\n"
    "* Anomaly 1 (@claim_la_explains_anomaly_qk_asymmetry) -- $q$ and $k$ "
    "play different operator roles and need not share a distribution.\n"
    "* Anomaly 2 (@claim_la_explains_anomaly_replace_q) -- $\\phi_{t+1}(k) "
    "\\neq \\phi_t(k)$ keeps the operator non-degenerate.\n"
    "* Anomaly 3 (@claim_la_explains_anomaly_inner_vs_outer) -- changing "
    "inner steps changes the operator and induces train-test mismatch.\n"
    "* Anomaly 4 (@claim_la_explains_anomaly_grad_ascent) -- gradient "
    "sign is absorbed by the learnable value projection.\n\n"
    "This is the explanatory payoff of the linear-attention re-framing: "
    "what looks like a paradox under memorization becomes a transparent "
    "property of a learned mixer.",
    title="Synthesis: linear-attention view simultaneously explains all four anomalies",
)

# ---------------------------------------------------------------------------
# 5.3 LaCT as linear attention (Section 5.3 + Appendix E)
# ---------------------------------------------------------------------------

setup_lact_swiglu_arch = setting(
    "**LaCT inner-loop architecture (Sec. 5.3, Appendix E.1).** LaCT "
    "[@Zhang2025] uses a bias-free SwiGLU MLP [@Shazeer2020] as its "
    "fast-weight network: "
    "$f(x) = \\bigl(\\mathrm{silu}(xW_0) \\odot (xW_2)\\bigr) W_1$, with "
    "$W_0, W_2 \\in \\mathbb{R}^{D_h \\times D_k}$ and $W_1 \\in "
    "\\mathbb{R}^{D_h \\times D_v}$. The inner-loop loss is the "
    "Frobenius inner product $\\mathcal{L}(f(k), v) = -\\langle f(k), "
    "v\\rangle$. The update applies per-token learnable $\\eta_t$, "
    "momentum $\\alpha_t$, and Muon-style gradient orthogonalization "
    "$\\mathcal{M}(\\cdot)$ [@Jordan2024].",
    title="Setting: LaCT's SwiGLU MLP + Frobenius loss + per-token $\\eta_t$ + Muon",
)

claim_lact_in_la_form = claim(
    "**LaCT in linear-attention form (Eq. 1, Sec. 5.3 + Appendix E.3).** "
    "Setting $\\phi_t(x) = \\mathrm{silu}(xW_{0,t}) \\odot (xW_{2,t})$, "
    "the inner-loop update of LaCT reduces to\n\n"
    "$$o_t = \\phi_{t+1}(q_t) \\Bigl( W_{1,0} + \\sum_{i=0}^t \\mathcal{M}"
    "\\bigl(\\phi_i(k_i)^\\top m_i\\bigr)\\Bigr), \\qquad "
    "m_i(k_i) = v_i \\cdot \\eta_i \\sum_{j=i}^t \\beta_i^j.$$\n\n"
    "This is a linear-attention operator with $\\phi_i(k_i)$ as the "
    "effective key, $m_i(k_i)$ as the (per-token-rate, momentum-weighted) "
    "effective value, $\\phi_{t+1}(q_t)$ as the effective query, and the "
    "Muon orthogonalization $\\mathcal{M}$ applied element-wise to the "
    "key-value outer product.",
    title="LaCT == linear-attention with $\\phi_t(x) = \\mathrm{silu}(xW_{0,t}) \\odot (xW_{2,t})$, Muon on outer product",
    background=[setup_lact_swiglu_arch, setup_momentum_update, setup_linear_attention],
    metadata={"source_section": "artifacts/2602.21204.pdf, Sec. 5.3 (Eq. 1), Appendix E"},
)

setup_weight_norm_in_lact = setting(
    "**Weight normalization in LaCT (Appendix E.4).** LaCT additionally "
    "applies channel-wise $\\ell_2$ weight normalization to $W_1$ after "
    "every inner-loop update: $W_{1,t+1} = \\mathrm{Norm}(W_{1,t} - "
    "\\eta_t \\mathcal{M}(\\Delta W_{1,t}))$. In linear-attention terms, "
    "this corresponds to normalizing the *state* $S_t$ after each step: "
    "$S_{t+1} = \\mathrm{Norm}(S_t + \\phi_t(k_t)^\\top m_t)$.",
    title="Setting: LaCT's channel-wise $\\ell_2$ weight normalization on $W_1$",
)

claim_weight_norm_does_not_break_la = claim(
    "**Weight normalization preserves the linear-attention interpretation "
    "(Appendix E.4).** Weight normalization (@setup_weight_norm_in_lact) "
    "*does not break* the linear-attention view: the output remains a "
    "linear function of the (normalized) state, "
    "$o_t = \\phi_{t+1}(q_t) S_{t+1}$, where $S_{t+1}$ is the *normalized* "
    "accumulated key-value outer products. The query still linearly reads "
    "from a state that accumulates KV information.",
    title="Weight normalization preserves the LA interpretation (only sequentializes the state)",
    background=[setup_weight_norm_in_lact, setup_linear_attention],
)

claim_weight_norm_breaks_simple_sum = claim(
    "**Weight normalization breaks the simple-sum form (Appendix E.4).** "
    "Although weight normalization preserves the LA *interpretation* "
    "(@claim_weight_norm_does_not_break_la), it prevents expressing the "
    "state as a *simple sum* over history. Instead the recurrence "
    "becomes a nested normalization: $S_{t+1} = \\mathrm{Norm}\\bigl("
    "\\mathrm{Norm}(S_{t-1} + \\phi_{t-1}(k_{t-1})^\\top m_{t-1}) + "
    "\\phi_t(k_t)^\\top m_t\\bigr)$. This nested structure has direct "
    "implications for parallelization (Section 6 / Appendix I).",
    title="Weight norm breaks the simple-sum recurrence, blocking parallel prefix-scan",
    background=[setup_weight_norm_in_lact],
)

# ---------------------------------------------------------------------------
# 5.4 ViTTT as linear attention (Section 5.4 + Appendices F, G)
# ---------------------------------------------------------------------------

setup_vittt_glu_arch = setting(
    "**ViTTT GLU component (Sec. 5.4, Appendix F.1).** ViTTT [@Han2025] "
    "uses two independent fast-weight components in its inner loop. The "
    "first is a simplified gated linear unit (GLU): "
    "$f_t(x) = \\mathrm{silu}(xW_{0,t}) \\odot (xW_{1,t})$, with "
    "$W_{0,t}, W_{1,t} \\in \\mathbb{R}^{D_h \\times D_h}$ both square. "
    "Define $\\phi_t(x) \\triangleq \\mathrm{silu}(xW_{0,t})$. The "
    "loss is the Frobenius inner product, as in LaCT.",
    title="Setting: ViTTT GLU $f_t(x) = \\mathrm{silu}(xW_{0,t}) \\odot (xW_{1,t})$, Frobenius loss",
)

claim_vittt_glu_in_la_form = claim(
    "**ViTTT GLU in linear-attention form (Sec. 5.4, Appendix F.3).** "
    "After one GD step on the GLU update, evaluating on query $q_t$ "
    "yields\n\n"
    "$$o_t = \\phi_{t+1}(q_t) \\odot \\Bigl(q_t \\bigl(W_1 + k_t^\\top "
    "(v_t \\odot \\phi_t(k_t))\\bigr)\\Bigr).$$\n\n"
    "This is a linear attention form in which (i) $\\langle q_t, k_t "
    "\\rangle$ is the scalar attention weight modulating $v_t$; "
    "(ii) $\\phi_t(k_t)$ acts as a multiplicative *gate on the values*; "
    "(iii) $\\phi_{t+1}(q_t)$ acts as a multiplicative *gate on the "
    "output*. The state $S_t = W_{1,t}$ accumulates outer products of "
    "keys and gated values.",
    title="ViTTT GLU == linear-attention with $\\phi$-gates on values and output",
    background=[setup_vittt_glu_arch, setup_linear_attention],
    metadata={"source_section": "artifacts/2602.21204.pdf, Sec. 5.4 (GLU), Appendix F"},
)

setup_vittt_dwconv_arch = setting(
    "**ViTTT depthwise-convolution component (Sec. 5.4, Appendix G.1).** "
    "ViTTT additionally includes a $3 \\times 3$ depthwise convolution "
    "layer with fast weights $W_t \\in \\mathbb{R}^{C \\times 1 \\times 3 "
    "\\times 3}$ updated in the inner loop. The forward pass is "
    "$f_t(K) = \\mathrm{Conv}_{3 \\times 3}(K; W_t)$ on spatial key tensor "
    "$K \\in \\mathbb{R}^{C \\times H \\times W}$. The loss is again the "
    "Frobenius inner product.",
    title="Setting: ViTTT $3 \\times 3$ depthwise convolution fast weights",
)

claim_vittt_dwconv_in_la_form = claim(
    "**ViTTT depthwise convolution as sliding-window linear attention "
    "(Sec. 5.4, Appendix G.3).** The output at spatial position $(i,j)$ "
    "after one GD step decomposes as "
    "$O_{c,i,j} = [\\mathrm{Conv}(Q; W_t)]_{c,i,j} + \\eta \\sum_{i', j'} "
    "[\\sum_{\\delta_y, \\delta_x} Q_{c, i+\\delta_y, j+\\delta_x} \\cdot "
    "K_{c, i'+\\delta_y, j'+\\delta_x}] \\cdot V_{c,i',j'}$. The first "
    "term is the initial state; the second is a spatially-local attention "
    "weight (sum of element-wise products over the $3\\times 3$ "
    "neighborhood) times $V$. Because convolution is a sliding-window "
    "linear layer, this TTT component is equivalent to a *sliding-window "
    "linear attention* mechanism.",
    title="ViTTT depthwise conv == sliding-window linear attention with $3\\times 3$ neighborhood overlap weights",
    background=[setup_vittt_dwconv_arch, setup_linear_attention],
    metadata={"source_section": "artifacts/2602.21204.pdf, Sec. 5.4 (DWConv), Appendix G"},
)

claim_vittt_in_la_form = claim(
    "**ViTTT in linear-attention form (Sec. 5.4 discussion).** Since "
    "*both* fast-weight components of ViTTT (the GLU, "
    "@claim_vittt_glu_in_la_form, and the $3\\times 3$ depthwise "
    "convolution, @claim_vittt_dwconv_in_la_form) admit linear-attention "
    "formulations, their *combination* also induces a linear-attention-"
    "like operator. ViTTT is therefore another concrete instance of "
    "TTT-KVB whose behavior is naturally understood through the lens of "
    "linear attention.",
    title="ViTTT (GLU + depthwise conv) is a linear-attention operator",
)

# ---------------------------------------------------------------------------
# Pass 2: strategies wiring theorems and explanations
# ---------------------------------------------------------------------------

# Theorem 5.1 is a pure mathematical derivation under the structural
# assumption (linear bias-free final layer) and one inner-loop GD step.
# It is a deduction: if the assumptions hold, the conclusion follows
# necessarily.
# Note: deduction takes only premises (claims). The structural settings
# enter via background.
strat_thm_5_1 = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_thm_5_1,
    reason=(
        "Direct algebraic computation. From the structural assumption "
        "(@setup_linear_final_layer_assumption) the model factors as "
        "$f_t(x) = \\phi_t(x) W_t$, so the gradient with respect to "
        "$W_t$ at input $k$ is $\\phi_t(k)^\\top \\partial \\mathcal{L}/"
        "\\partial f_t(k)$ by the chain rule. One GD step "
        "(@setup_one_step_gd) yields $W_{t+1} = W_t + \\phi_t(k)^\\top "
        "g_t(k)$ with $g_t(k) = -\\eta \\partial \\mathcal{L}/\\partial "
        "f_t(k)$. Evaluating $f_{t+1}(q) = \\phi_{t+1}(q) W_{t+1}$ "
        "substitutes the new $W_{t+1}$ and produces "
        "$o = \\phi_{t+1}(q)(W_t + \\phi_t(k)^\\top g_t(k))$, which is "
        "the linear-attention form $\\hat{q}(S_0 + \\hat{k}^\\top \\hat{v})$ "
        "of @setup_linear_attention. The derivation is purely "
        "deterministic; see Appendix B for the full proof."
    ),
    background=[
        setup_linear_final_layer_assumption,
        setup_one_step_gd,
        setup_linear_attention,
    ],
    prior=0.99,
)

# Theorem 5.2: induction on Theorem 5.1.
strat_thm_5_2 = deduction(
    [claim_thm_5_1],
    claim_thm_5_2,
    reason=(
        "Inductive extension of @claim_thm_5_1 over $t+1$ tokens. "
        "Base case $t = 0$ is exactly Theorem 5.1. Inductive step: "
        "assume $W_t = W_0 + \\sum_{i=0}^{t-1} \\phi_i(k_i)^\\top "
        "g_i(k_i)$; processing token $t$ adds $\\phi_t(k_t)^\\top "
        "g_t(k_t)$ by Theorem 5.1, giving the closed form for $W_{t+1}$. "
        "Substituting into $o_t = \\phi_{t+1}(q_t) W_{t+1}$ produces "
        "the extended linear-attention form. See Appendix C."
    ),
    background=[
        setup_linear_final_layer_assumption,
        setup_one_step_gd,
        setup_linear_attention,
    ],
    prior=0.99,
)

# Theorem 5.3: parallels Theorem 5.2 with the momentum bookkeeping.
strat_thm_5_3 = deduction(
    [claim_thm_5_1],
    claim_thm_5_3,
    reason=(
        "Inductive extension parallel to Theorem 5.2 (@claim_thm_5_2), "
        "but tracking the momentum recurrence "
        "(@setup_momentum_update). The inductive hypothesis is "
        "$\\Delta W_{t-1} = \\sum_{i=0}^{t-1} \\beta_i^{t-1} \\phi_i(k_i)^\\top "
        "\\partial \\mathcal{L}/\\partial f_i(k_i)$. The cumulative "
        "coefficients satisfy $\\alpha_t \\cdot \\beta_i^{t-1} = "
        "\\beta_i^t$, so the inductive step propagates cleanly. "
        "Exchanging the order of summation in $W_{t+1} = W_0 - \\eta "
        "\\sum_j \\Delta W_j$ groups the gradient terms by source index "
        "$i$, yielding $m_i(k_i) = g_i(k_i) \\sum_{j=i}^t \\beta_i^j$. "
        "See Appendix D for the full bookkeeping."
    ),
    background=[
        setup_linear_final_layer_assumption,
        setup_momentum_update,
        setup_linear_attention,
    ],
    prior=0.99,
)

# Headline theoretical claim: TTT-KVB == linear attention. Synthesis of
# the three theorems plus the recognition that prior work only had the
# restricted single-linear-layer case.
strat_ttt_is_la = support(
    [
        claim_thm_5_1,
        claim_thm_5_2,
        claim_thm_5_3,
        claim_prior_la_equivalence_restricted,
        claim_ttt_shares_la_compute_profile,
        claim_deltanet_equals_linear_ttt,
    ],
    claim_ttt_is_linear_attention,
    reason=(
        "The three theorems (@claim_thm_5_1, @claim_thm_5_2, "
        "@claim_thm_5_3) jointly establish that under the linear "
        "bias-free final-layer condition, single-step, sequentially-"
        "unrolled, and momentum-augmented TTT-KVB updates *all* admit "
        "the linear-attention form $o_t = \\hat{q}_t(S_0 + \\sum "
        "\\hat{k}_i^\\top \\hat{v}_i)$. This generalizes the restricted "
        "single-linear-layer / zero-init reduction of Sun et al. (2025) "
        "(@claim_prior_la_equivalence_restricted) to multi-layer "
        "non-linear $\\phi$ and momentum, and supersedes the prior "
        "single-layer DeltaNet equivalence (@claim_deltanet_equals_linear_ttt). "
        "The shared compute profile of all TTT-KVB variants "
        "(@claim_ttt_shares_la_compute_profile) further corroborates the "
        "unified perspective. Slightly less than 1.0 because the claim "
        "asserts the *interpretation* (\"is secretly linear attention\") "
        "rather than just the algebraic identity -- the theorems give "
        "the identity, and the broader claim about the inner loop *not* "
        "performing meta-learning is an interpretive synthesis on top."
    ),
    prior=0.96,
    background=[setup_linear_final_layer_assumption, setup_linear_attention],
)

# Section 5.2 -- per-anomaly explanations.
strat_la_explains_anomaly_inner_vs_outer = support(
    [claim_ttt_is_linear_attention],
    claim_la_explains_anomaly_inner_vs_outer,
    reason=(
        "Under the LA reformulation (@claim_ttt_is_linear_attention), "
        "the inner-loop hyperparameters (@setup_inner_loop_hyperparameters) "
        "-- including the number of GD steps -- enter the *operator* "
        "itself ($\\phi_{t+1}$, $g_t$, $S_0$ in @claim_thm_5_1). "
        "Changing the step count at inference therefore produces an "
        "operator *different* from the one used at training. Train-test "
        "operator mismatch is a well-known source of degradation. The "
        "explanation is structural and does not require any new "
        "evidence."
    ),
    prior=0.92,
    background=[setup_inner_loop_hyperparameters],
)

strat_la_explains_anomaly_grad_ascent = support(
    [claim_thm_5_1],
    claim_la_explains_anomaly_grad_ascent,
    reason=(
        "Theorem 5.1 (@claim_thm_5_1) gives $\\hat{v} = g_t(k) = "
        "-\\eta \\partial \\mathcal{L}/\\partial f_t(k)$. Replacing GD "
        "with gradient ascent flips this sign to $+\\eta \\partial "
        "\\mathcal{L}/\\partial f_t(k)$, so $\\hat{v} \\to -\\hat{v}$. "
        "But the value-projection slow weights that produce $v$ are "
        "*learnable* and trained jointly under the downstream task "
        "objective; the sign flip is therefore absorbed into the "
        "learned mapping during training. Under this view performance "
        "preservation under sign inversion is *expected*."
    ),
    prior=0.94,
)

strat_la_explains_anomaly_qk_asymmetry = support(
    [claim_thm_5_1],
    claim_la_explains_anomaly_qk_asymmetry,
    reason=(
        "Theorem 5.1 (@claim_thm_5_1) shows $q$ enters only via "
        "$\\hat{q} = \\phi_{t+1}(q)$ while $k$ enters via $\\hat{k} = "
        "\\phi_t(k)$ and $\\hat{v} = g_t(k)$. They are mapped to "
        "different operator components; there is no requirement that "
        "they share a semantic space. The explanation is structural and "
        "follows directly from reading off the theorem."
    ),
    prior=0.94,
)

strat_la_explains_anomaly_replace_q = support(
    [claim_thm_5_1],
    claim_la_explains_anomaly_replace_q,
    reason=(
        "Even when $q$ is replaced by $k$, Theorem 5.1's roles "
        "(@claim_thm_5_1) make the effective query $\\phi_{t+1}(k)$ "
        "*distinct* from the effective key $\\phi_t(k)$ -- they evaluate "
        "the same input through two different parameter states "
        "($\\Theta_{t+1}$ vs $\\Theta_t$). The kernel $\\phi$ is also "
        "learnable; the model can adapt to map the same input to "
        "different representations through these two parameter states. "
        "Operator non-degeneracy is preserved."
    ),
    prior=0.92,
)

strat_anomalies_explained = support(
    [
        claim_la_explains_anomaly_inner_vs_outer,
        claim_la_explains_anomaly_grad_ascent,
        claim_la_explains_anomaly_qk_asymmetry,
        claim_la_explains_anomaly_replace_q,
    ],
    claim_anomalies_explained_by_la_view,
    reason=(
        "Each of the four per-anomaly explanations "
        "(@claim_la_explains_anomaly_inner_vs_outer, "
        "@claim_la_explains_anomaly_grad_ascent, "
        "@claim_la_explains_anomaly_qk_asymmetry, "
        "@claim_la_explains_anomaly_replace_q) reads naturally off "
        "Theorems 5.1-5.3 without additional empirical input. Their "
        "joint coverage of all four anomalies of Section 4 is the "
        "explanatory payoff of the linear-attention re-framing."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Abduction: the LA view and the memorization view both purport to
# explain the *observed cross-task pattern of TTT-KVB behavior*. We use
# the four-anomaly summary (claim_memorization_view_falsified) as the
# *observation* whose explanation is at stake. The LA view explains it
# (the anomalies follow naturally). The memorization view fails to
# explain it (it predicts the opposite of each anomaly).
# ---------------------------------------------------------------------------

s_la_explains_anomalies = support(
    [claim_ttt_is_linear_attention],
    claim_anomalies_explained_by_la_view,
    reason=(
        "The linear-attention re-framing (@claim_ttt_is_linear_attention) "
        "directly predicts each of the four anomalies as natural "
        "structural consequences (Sec. 5.2): different inner steps -> "
        "different operator -> train-test mismatch (Anomaly 3); "
        "$\\hat{v}$ sign absorbed by learnable $v$-projection (Anomaly "
        "4); $q$ and $k$ drive different operator components (Anomaly "
        "1); $\\phi_{t+1}(k) \\neq \\phi_t(k)$ keeps operator "
        "non-degenerate (Anomaly 2)."
    ),
    prior=0.94,
)

s_memorization_does_not_explain = support(
    [claim_memorization_hypothesis],
    claim_anomalies_explained_by_la_view,
    reason=(
        "Under the memorization hypothesis "
        "(@claim_memorization_hypothesis), each of the four anomalies "
        "is paradoxical: better memorization (lower inner loss) should "
        "help downstream perf, gradient ascent should destroy memory, "
        "$Q$-$K$ overlap should hold, and the query should be "
        "functional. The hypothesis cannot natively account for the "
        "explanatory pattern (@claim_anomalies_explained_by_la_view) -- "
        "the memorization view would predict the *opposite* observation."
    ),
    prior=0.20,  # Very low: memorization positively *contradicts* the
    # anomaly pattern, so it has near-zero explanatory power for it.
)

cmp_la_vs_memorization = compare(
    claim_ttt_is_linear_attention,
    claim_memorization_hypothesis,
    claim_anomalies_explained_by_la_view,
    reason=(
        "Both the LA reformulation (@claim_ttt_is_linear_attention) "
        "and the memorization hypothesis (@claim_memorization_hypothesis) "
        "purport to describe the functional mechanism of TTT-KVB. The "
        "LA view derives all four anomalies as natural structural "
        "predictions (Sec. 5.2); the memorization view treats each "
        "anomaly as a paradox and would predict the opposite. The LA "
        "view's explanatory power for the observed anomaly pattern is "
        "therefore strictly superior."
    ),
    prior=0.94,
)

abd_la_over_memorization = abduction(
    s_la_explains_anomalies,
    s_memorization_does_not_explain,
    cmp_la_vs_memorization,
    reason=(
        "Inference to best explanation: the LA view "
        "(@claim_ttt_is_linear_attention) and the memorization view "
        "(@claim_memorization_hypothesis) are competing accounts of "
        "the same TTT-KVB mechanism. The observation to be explained "
        "is the four-anomaly pattern "
        "(@claim_anomalies_explained_by_la_view). The LA view delivers "
        "the explanation structurally from Theorems 5.1-5.3 "
        "(@s_la_explains_anomalies); the memorization view cannot "
        "(@s_memorization_does_not_explain). The LA view is "
        "abductively preferred."
    ),
)

# Note: a separate `contradiction(claim_ttt_is_linear_attention,
# claim_memorization_hypothesis)` would conflict with the equivalence
# constraints created by the abduction's compare(...) substrategy
# (which pulls both predictions toward the observation). The abduction
# itself encodes the dialectic; we leave the formal contradiction
# implicit.

# Connect to the contribution claim from motivation.
strat_equivalence_contribution = support(
    [claim_ttt_is_linear_attention, claim_anomalies_explained_by_la_view],
    claim_contribution_equivalence,
    reason=(
        "The theoretical equivalence (@claim_ttt_is_linear_attention) "
        "establishes the algebraic identity claimed as Contribution 2 "
        "in the introduction (@claim_contribution_equivalence). The "
        "anomaly explanations (@claim_anomalies_explained_by_la_view) "
        "demonstrate the *interpretive payoff* of the equivalence -- "
        "the structured-mixing reading rather than the meta-learning "
        "reading. Together they substantiate the contribution."
    ),
    prior=0.95,
)

# 5.3 LaCT in linear-attention form -- direct deduction from Theorem 5.3.
strat_lact_in_la_form = deduction(
    [claim_thm_5_3],
    claim_lact_in_la_form,
    reason=(
        "Direct application of Theorem 5.3 (@claim_thm_5_3) to LaCT "
        "(@setup_lact_swiglu_arch). The Frobenius inner-product loss "
        "yields $\\partial \\mathcal{L}/\\partial f_t(k_t) = -v_t$, "
        "hence $\\nabla_{W_1} \\mathcal{L} = -\\phi_t(k_t)^\\top v_t$ "
        "with $\\phi_t(x) = \\mathrm{silu}(xW_{0,t}) \\odot (xW_{2,t})$. "
        "Plugging into the momentum recurrence and applying the "
        "Muon orthogonalization $\\mathcal{M}$ to each gradient "
        "accumulator gives the LA form of Eq. 1. See Appendix E.3 for "
        "the full bookkeeping."
    ),
    background=[setup_lact_swiglu_arch, setup_momentum_update, setup_linear_attention],
    prior=0.99,
)

# Weight normalization preserves the LA interpretation.
strat_weight_norm_preserves_la = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_weight_norm_does_not_break_la,
    reason=(
        "Weight normalization (@setup_weight_norm_in_lact) acts on the "
        "state $S_t = W_{1,t}$ after each update: $S_{t+1} = "
        "\\mathrm{Norm}(S_t + \\phi_t(k_t)^\\top m_t)$. The output is "
        "still $o_t = \\phi_{t+1}(q_t) S_{t+1}$ -- a *linear* function "
        "of the (normalized) state. The query still linearly reads "
        "from a state that accumulates KV outer products, which is "
        "exactly the LA form (cf. @setup_linear_attention)."
    ),
    background=[setup_weight_norm_in_lact, setup_linear_attention],
    prior=0.99,
)

# Weight normalization breaks simple-sum recurrence.
strat_weight_norm_breaks_sum = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_weight_norm_breaks_simple_sum,
    reason=(
        "Direct algebraic observation. Under weight normalization "
        "(@setup_weight_norm_in_lact), each step applies "
        "$\\mathrm{Norm}$ to the *result* of the previous step, "
        "yielding nested normalizations $\\mathrm{Norm}(\\mathrm{Norm}"
        "(\\ldots) + \\ldots)$. Since $\\mathrm{Norm}(A + B) \\neq "
        "\\mathrm{Norm}(A) + \\mathrm{Norm}(B)$ in general, the state "
        "cannot be expressed as a simple sum $S_0 + \\sum \\phi_i(k_i)^"
        "\\top m_i$. The implication for parallel prefix scan is treated "
        "in Appendix I.2 (and Section 6.2)."
    ),
    background=[setup_weight_norm_in_lact],
    prior=0.99,
)

# 5.4 ViTTT GLU -- deduction from the same proof template.
strat_vittt_glu_in_la_form = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_vittt_glu_in_la_form,
    reason=(
        "Algebraic computation following the same template as Theorem "
        "5.1. With $f_t(x) = \\mathrm{silu}(xW_0) \\odot (xW_1)$ "
        "(@setup_vittt_glu_arch) and Frobenius loss, the gradient "
        "$\\nabla_{W_1} \\mathcal{L} = -k_t^\\top (v_t \\odot "
        "\\phi_t(k_t))$ with $\\phi_t(x) = \\mathrm{silu}(xW_0)$. "
        "Substituting into one GD step on $W_1$ and reading "
        "$o_t = \\phi_{t+1}(q_t) \\odot (q_t W_{1,t+1})$ yields the "
        "displayed LA form with $\\phi$-gates on values and output. "
        "See Appendix F.3."
    ),
    background=[setup_vittt_glu_arch, setup_linear_attention],
    prior=0.99,
)

# 5.4 ViTTT depthwise convolution.
strat_vittt_dwconv_in_la_form = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_vittt_dwconv_in_la_form,
    reason=(
        "Algebraic computation. For depthwise convolution "
        "(@setup_vittt_dwconv_arch) with Frobenius loss, the gradient "
        "$\\nabla_{W_t} \\mathcal{L} = -K \\star V$ (cross-correlation). "
        "After one GD step, evaluating the output at $(i, j)$ "
        "decomposes into the initial-state convolution term plus a "
        "spatially-local attention weight summing element-wise products "
        "of $Q$ and $K$ over the $3 \\times 3$ neighborhood, weighted "
        "against $V$. Convolution is a sliding-window linear layer; "
        "this TTT component is therefore a sliding-window linear "
        "attention. See Appendix G.3."
    ),
    background=[setup_vittt_dwconv_arch, setup_linear_attention],
    prior=0.99,
)

# Combination of the two ViTTT components.
strat_vittt_in_la_form = support(
    [claim_vittt_glu_in_la_form, claim_vittt_dwconv_in_la_form],
    claim_vittt_in_la_form,
    reason=(
        "Both fast-weight components of ViTTT -- the GLU "
        "(@claim_vittt_glu_in_la_form) and the $3\\times 3$ depthwise "
        "convolution (@claim_vittt_dwconv_in_la_form) -- admit linear-"
        "attention reformulations. Their composition (the ViTTT "
        "fast-weight stack) therefore induces a linear-attention-like "
        "operator. The argument is structural and does not depend on "
        "additional empirical input."
    ),
    prior=0.95,
)


__all__ = [
    # Structural premises
    "setup_linear_final_layer_assumption",
    "claim_assumption_holds_for_studied_archs",
    "setup_one_step_gd",
    "setup_momentum_update",
    # Theorems
    "claim_thm_5_1",
    "claim_thm_5_2",
    "claim_thm_5_3",
    # Theoretical headline
    "claim_ttt_is_linear_attention",
    # 5.2 anomaly explanations
    "claim_la_explains_anomaly_inner_vs_outer",
    "claim_la_explains_anomaly_grad_ascent",
    "claim_la_explains_anomaly_qk_asymmetry",
    "claim_la_explains_anomaly_replace_q",
    "claim_anomalies_explained_by_la_view",
    # 5.3 LaCT
    "setup_lact_swiglu_arch",
    "claim_lact_in_la_form",
    "setup_weight_norm_in_lact",
    "claim_weight_norm_does_not_break_la",
    "claim_weight_norm_breaks_simple_sum",
    # 5.4 ViTTT
    "setup_vittt_glu_arch",
    "claim_vittt_glu_in_la_form",
    "setup_vittt_dwconv_arch",
    "claim_vittt_dwconv_in_la_form",
    "claim_vittt_in_la_form",
]
