"""Section 6: Practical Implications -- simplification + parallelization.

* 6.1 Six-step ablation trajectory: progressively remove TTT design
  components (multi-layer Theta updates, weight normalization, multi-layer
  MLP, per-token learning rates, momentum, gradient orthogonalization) and
  observe that complex TTT formulations reduce to standard linear
  attention with only minor performance degradation.
* 6.2 Fully parallel formulation of TTT: when only the final layer is
  dynamic and weight normalization is removed (Variants 2-6 of the
  ablation), the state update becomes associative and the recurrence
  can be computed via parallel prefix scan. Up to 4.0x TTT-layer
  throughput; 1.19x end-to-end training speedup.
* (Appendix I) Two cases that break reducibility: dynamic kernel
  function (updating $W_0, W_2$) and weight normalization. Each
  introduces nested non-linearity that prevents associativity.
"""

from gaia.lang import claim, setting, support, deduction

from .motivation import claim_contribution_practical
from .s2_related_work import (
    setup_linear_attention,
    claim_complexity_drift_under_memorization,
)
from .s3_preliminaries import (
    setup_inner_loop_hyperparameters,
    setup_update_then_query,
    setup_inner_loop_loss,
)
from .s5_linear_attention_equivalence import (
    setup_linear_final_layer_assumption,
    claim_assumption_holds_for_studied_archs,
    setup_lact_swiglu_arch,
    setup_weight_norm_in_lact,
    setup_vittt_glu_arch,
    setup_vittt_dwconv_arch,
    claim_thm_5_1,
    claim_thm_5_2,
    claim_thm_5_3,
    claim_lact_in_la_form,
    claim_ttt_is_linear_attention,
    claim_weight_norm_breaks_simple_sum,
)

# ---------------------------------------------------------------------------
# 6.1 Reduce TTT to Linear Attention -- six-step ablation trajectory
# ---------------------------------------------------------------------------

setup_ablation_methodology = setting(
    "**Ablation methodology (Sec. 6.1).** Starting from full LaCT "
    "[@Zhang2025] / ViTTT [@Han2025] baselines, the paper applies six "
    "design simplifications in sequence. Each removes one component "
    "whose justification depends on the storage-and-retrieval view but "
    "whose role becomes optional under the linear-attention view. The "
    "trajectory ends at standard linear attention "
    "$o = q(W + \\sum_i k_i^\\top v_i)$ (Variant 6). All experiments use "
    "the official LaCT implementation for LLM and NVS tasks and ViTTT "
    "for image recognition; experimental settings in Appendix A.",
    title="Ablation methodology: 6 sequential simplifications, end at standard LA",
)

setup_ablation_step1_last_layer_only = setting(
    "**Step 1: update only the last-layer parameters.** Theorem 5.1 "
    "(@claim_thm_5_1) shows the effective query/key are $\\phi_{t+1}(q)$ "
    "/ $\\phi_t(k)$. If only the final-layer parameter $W$ is updated "
    "in the inner loop while $\\Theta = \\{W_0, W_2\\}$ remains fixed, "
    "$\\phi(\\cdot)$ becomes a *static learnable kernel function* "
    "(no time index). From the LA perspective, $\\phi$ then plays the "
    "role of a learnable kernel with effective query $\\phi(q)$ and "
    "key $\\phi(k)$.",
    title="Step 1: $\\Theta$ frozen; only $W_1$ dynamic $\\Rightarrow$ static learnable kernel $\\phi$",
)

setup_ablation_step2_remove_weight_norm = setting(
    "**Step 2: remove weight normalization.** After Step 1, "
    "normalization on $\\Theta$ is a no-op. Normalization of $W$ is "
    "equivalent to normalizing the LA *state* $S_t$ "
    "(@claim_weight_norm_breaks_simple_sum). Since such normalization is "
    "uncommon in linear-attention literature, the paper ablates it. "
    "*Crucially, after this step the formulation becomes fully "
    "parallelizable* (Sec. 6.2).",
    title="Step 2: remove weight normalization $\\Rightarrow$ parallelizable formulation",
)

setup_ablation_step3_collapse_mlp = setting(
    "**Step 3: multi-layer MLP $\\to$ single linear layer.** Several TTT "
    "variants [@Han2025; @Behrouz2024] employ deeper inner-loop MLPs but "
    "report inconsistent empirical gains. From the LA perspective, MLP "
    "depth simply induces a more complex kernel $\\phi$ over $q$ and $k$. "
    "When $q$ and $k$ already have sufficient representational capacity "
    "(set by the surrounding slow weights), the added complexity is "
    "unlikely to help. Step 3 collapses the MLP to a single linear layer, "
    "exposing $\\hat{q} = q$ and $\\hat{k} = k$.",
    title="Step 3: collapse multi-layer MLP to single linear layer $\\Rightarrow$ exposes $\\hat{q}=q, \\hat{k}=k$",
)

setup_ablation_step4_remove_pertoken_lr = setting(
    "**Step 4: remove per-token learning rates.** Many TTT methods "
    "[@Behrouz2024; @Zhang2025] introduce a per-token learnable rate "
    "$\\eta_t$. Section 5.3 (@claim_lact_in_la_form) shows that with "
    "Frobenius dot-product loss this $\\eta_t$ is *absorbed into the "
    "learnable $v_t$* via $m_i = v_i \\cdot \\eta_i \\sum_j \\beta_i^j$, "
    "making it functionally redundant. Consistent with this, ViTTT "
    "empirically finds a constant $\\eta = 1.0$ suffices.",
    title="Step 4: per-token $\\eta_t$ is absorbed into $v$, hence redundant",
)

setup_ablation_step5_remove_momentum = setting(
    "**Step 5: remove momentum in SGD.** Theorem 5.3 (@claim_thm_5_3) "
    "shows momentum only changes the effective value from the "
    "instantaneous gradient $g_t(k)$ to a momentum-weighted sum "
    "$m_i = g_i(k_i) \\sum_{j=i}^t \\beta_i^j$ of past gradients. From "
    "the LA perspective this remixes historical key-value contributions "
    "into a single value vector. Since both $\\hat{k}$ and $\\hat{v}$ "
    "are already learnable, this additional mixing is unlikely to "
    "provide meaningful benefit. For both LaCT and ViTTT $g_t(k) = -v$, "
    "so removing momentum recovers $\\hat{v} = v$, the *true* value "
    "vector.",
    title="Step 5: momentum just remixes history; removing it recovers $\\hat{v} = v$",
)

setup_ablation_step6_remove_grad_orthog = setting(
    "**Step 6: remove gradient orthogonalization.** LaCT optionally "
    "applies Muon-style gradient orthogonalization $\\mathcal{M}(\\Delta "
    "W)$. Under the LA reformulation this corresponds to applying the "
    "operator $\\mathcal{M}$ to the state update $\\mathcal{M}(\\hat{k}^"
    "\\top v)$. Step 6 removes this operation. After this final step "
    "*both* LaCT and ViTTT reduce *exactly* to standard linear attention: "
    "$o = q(W + \\sum_i k_i^\\top v_i)$ -- no kernel, no momentum, no "
    "per-token rate, no normalization, no orthogonalization.",
    title="Step 6: remove gradient orthogonalization $\\Rightarrow$ exactly standard linear attention",
)

# ---------------------------------------------------------------------------
# Empirical results of the six-step ablation (Table 2)
# ---------------------------------------------------------------------------

obs_ablation_table2 = claim(
    "**Observation (Table 2, ablation trajectory).** Ablation results "
    "across the three task families. Variant 1 (= Step 1, only update "
    "last layer) achieves the *best overall performance*. Variants 2-6 "
    "admit parallel implementations (column 'Parallel TPS'). "
    "$\\dagger$ marks ablations that do not apply -- in which case the "
    "metric matches the preceding variant. * indicates ViTTT does not "
    "use Muon, so ViTTT-Variant 6 ablates *gradient normalization* "
    "instead.\n\n"
    "| Alias    | Description                                       | Perplexity (LaCT-LLM) ↓ | PSNR dB (LaCT-NVS) ↑ | Top-1 % (ViTTT) ↑ | Recurrent TPS ↑ | Parallel TPS ↑ |\n"
    "|----------|---------------------------------------------------|-----------------------:|---------------------:|------------------:|----------------:|---------------:|\n"
    "| Baseline | LaCT / ViTTT                                       | 16.43                  | 25.94                | 79.34             | 4.30M           | N/A            |\n"
    "| Variant 1 | Update only last-layer parameters               | **15.93**              | **25.97**            | **79.63**         | 10.60M          | N/A            |\n"
    "| Variant 2 | + remove weight normalization                   | 16.31                  | 25.93                | 79.63 $\\dagger$  | 11.02M          | 30.18M         |\n"
    "| Variant 3 | + multi-layer MLP $\\to$ single linear           | 16.23                  | 25.71                | 79.39             | 12.95M          | 49.69M         |\n"
    "| Variant 4 | + remove per-token learnable lr                 | 16.12                  | 25.70                | 79.39 $\\dagger$  | 13.31M          | 53.99M         |\n"
    "| Variant 5 | + remove momentum in SGD                        | 15.97                  | 25.70 $\\dagger$     | 79.39 $\\dagger$  | 14.40M          | 57.28M         |\n"
    "| Variant 6 | + remove gradient orthogonalization (or grad-norm for ViTTT*) | 16.80    | 25.73                | 79.54*            | 89.67M          | **124.6M**     |\n",
    title="Observation (Table 2): six-step ablation reduces TTT to standard LA",
    background=[setup_ablation_methodology],
    metadata={
        "source_table": "artifacts/2602.21204.pdf, Table 2",
        "caption": "Table 2 | Ablation Trajectory Reducing TTT to Standard Linear Attention. Variant 1 achieves best across all three tasks; Variants 2-6 admit parallel implementations.",
    },
)

obs_variant1_best = claim(
    "**Sub-observation (Table 2, Variant 1).** Variant 1 -- which "
    "differs from the baseline *only* in restricting the inner-loop "
    "update to the final MLP layer -- achieves the best performance on "
    "*all three* task families: 15.93 vs 16.43 perplexity (LaCT-LLM), "
    "25.97 vs 25.94 dB PSNR (LaCT-NVS), 79.63% vs 79.34% Top-1 accuracy "
    "(ViTTT). It also more than doubles inference throughput on the LLM "
    "task (10.60M vs 4.30M tokens/sec).",
    title="Sub-observation: Variant 1 (update only last layer) is best on all three tasks",
    background=[setup_ablation_methodology, setup_ablation_step1_last_layer_only],
    metadata={"source_table": "artifacts/2602.21204.pdf, Table 2 (Variant 1 row)"},
)

obs_variant6_minor_degradation = claim(
    "**Sub-observation (Table 2, Variant 6).** Even after applying *all* "
    "six simplifications -- collapsing TTT to standard linear attention "
    "$o = q(W + \\sum k_i^\\top v_i)$ -- the performance degradation "
    "relative to baseline is *minor*: +0.4 perplexity on LLM (16.80 vs "
    "16.43), -0.2 dB PSNR on NVS (25.73 vs 25.94), and +0.2% Top-1 on "
    "image recognition (79.54 vs 79.34). At the same time, throughput "
    "improves dramatically: 89.67M (recurrent) and 124.6M (parallel) vs "
    "4.30M baseline tokens/sec.",
    title="Sub-observation: Variant 6 (= standard LA) is within 0.4 / 0.2 / 0.2 of baseline",
    background=[setup_ablation_methodology, setup_ablation_step6_remove_grad_orthog],
    metadata={"source_table": "artifacts/2602.21204.pdf, Table 2 (Variant 6 row)"},
)

obs_remaining_components_marginal = claim(
    "**Sub-observation (Table 2 narrative).** Most TTT design components "
    "contribute only marginally to performance, with two notable "
    "exceptions: (i) **deeper MLPs** (Step 3) help on the NVS task "
    "(25.93 -> 25.71 dB PSNR loss when collapsed); (ii) **gradient "
    "orthogonalization** (Step 6) helps on the LLM task (15.97 -> 16.80 "
    "perplexity loss when removed). The other components (per-token "
    "learning rate, momentum) leave performance essentially unchanged "
    "when removed.",
    title="Sub-observation: only deep MLP (NVS) and Muon (LLM) contribute non-trivially",
    background=[setup_ablation_methodology],
    metadata={"source_table": "artifacts/2602.21204.pdf, Table 2 + narrative"},
)

claim_simplifications_preserve_performance = claim(
    "**Synthesis (Sec. 6.1).** The six-step ablation trajectory "
    "demonstrates that complex TTT formulations (LaCT, ViTTT) can be "
    "reduced to standard linear attention with only *minor* performance "
    "degradation, and that *most* of the components introduced under "
    "the memorization-fidelity rationale (@claim_complexity_drift_under_memorization) "
    "-- weight normalization, multi-layer MLP depth, per-token learning "
    "rates, momentum, gradient orthogonalization -- are either *redundant* "
    "or *marginal* to final task performance. By contrast, restricting "
    "the inner-loop to update only the final layer (Step 1) actually "
    "*improves* performance across all three task families. This is a "
    "concrete practical payoff of the linear-attention re-framing.",
    title="Synthesis: complex TTT design choices are redundant or marginal; LA reduction preserves perf",
    background=[claim_complexity_drift_under_memorization],
)

# ---------------------------------------------------------------------------
# 6.2 Parallel form of TTT
# ---------------------------------------------------------------------------

setup_associativity_condition = setting(
    "**Associativity condition (Sec. 6.2 / Appendix H).** When "
    "Variant 2's preconditions hold -- weight normalization removed *and* "
    "only $W_1$ dynamic (so the kernel function $\\phi_t(\\cdot) \\equiv "
    "\\phi(\\cdot; \\Theta)$ is *static and independent of sequence "
    "history*) -- the LaCT recurrence (Theorem 5.3, @claim_thm_5_3) "
    "becomes associative. The state update can then be computed via "
    "*parallel prefix scan* rather than sequential token-by-token updates.",
    title="Associativity: static $\\phi$ + no weight-norm $\\Rightarrow$ prefix-scan parallelism",
)

setup_parallel_formulation = setting(
    "**Parallel formulation (Appendix H.1).** For a sequence of $N$ "
    "chunks of size $L$ each, define the batched kernel function "
    "$\\Phi(X) = \\mathrm{silu}(XW_0) \\odot (XW_2) \\in "
    "\\mathbb{R}^{(NL) \\times D_h}$. With block-diagonal mask "
    "$B = \\mathrm{diag}(I_L, \\ldots, I_L)$, scaled values "
    "$\\tilde V = V \\odot \\eta$, momentum matrix $A_{ij} = "
    "\\prod_{s=j+1}^i \\alpha_s$ for $i \\ge j$ (else $0$), and causal "
    "mask $M_{ij} = \\mathbb{1}[i \\ge j]$, the output computes as "
    "$O = \\Phi(Q) W_{1,0} + \\bigl((\\Phi(Q)\\Phi(K)^\\top) \\odot "
    "(A \\odot M)^{\\uparrow L}\\bigr) \\tilde V$, where "
    "$(\\cdot)^{\\uparrow L}$ denotes the Kronecker product with "
    "$1_{L \\times L}$.",
    title="Setting: parallel chunked formulation $O = \\Phi(Q) W_0 + (\\Phi(Q)\\Phi(K)^\\top \\odot \\mathrm{mask}) \\tilde V$",
)

claim_parallel_equivalent_to_recurrent = claim(
    "**Theorem (parallel equivalence, Appendix H.2).** Under the "
    "associativity condition (@setup_associativity_condition), the "
    "parallel formulation (@setup_parallel_formulation) computes "
    "*exactly* the same outputs as the sequential recurrent formulation "
    "of Theorem 5.3 (@claim_thm_5_3), at every chunk index $t$. The "
    "proof proceeds in four steps: unroll the momentum recurrence, "
    "unroll the weight recurrence, expand the sequential output, and "
    "match per-chunk-pair coefficients $c_i^t$ between the two "
    "formulations.",
    title="Parallel formulation is exactly equivalent to sequential recurrence (Appendix H.2)",
    background=[setup_associativity_condition, setup_parallel_formulation],
    metadata={"source_section": "artifacts/2602.21204.pdf, Appendix H.2 (proof)"},
)

obs_parallel_throughput = claim(
    "**Observation (Table 2, Parallel TPS column).** Switching from the "
    "recurrent to the parallel implementation *for the TTT layer alone* "
    "improves inference throughput by up to **4.0x** (124.6M vs 30.18M "
    "tokens/sec on LLM, single batch -- comparing Variant 2's parallel "
    "vs recurrent for the cleanest comparison; or 124.6M vs 89.67M for "
    "Variant 6 alone). All Variants 2 through 6 admit parallel "
    "implementations.",
    title="Observation: parallel TTT layer is up to 4.0x faster than recurrent",
    background=[setup_parallel_formulation, setup_ablation_methodology],
    metadata={
        "source_table": "artifacts/2602.21204.pdf, Table 2 (Parallel TPS column)",
        "caption": "Table 2 reports per-variant inference throughput in tokens/sec for both the recurrent and parallel TTT-layer implementations.",
    },
)

obs_parallel_end_to_end_speedup = claim(
    "**Observation (Fig. 4).** Combining the parallel TTT layer with "
    "Steps 1 and 2 simplifications yields a **1.19x end-to-end training "
    "speedup** on LaCT-LLM (training loss vs wall-clock plot; the "
    "parallel form reaches the same training-loss target faster than "
    "the recurrent baseline) *while maintaining comparable convergence "
    "(visually overlapping loss curves)*. A further 1.06x speedup is "
    "obtained from a related optimization (per Fig. 4 annotation).",
    title="Observation: 1.19x end-to-end training speedup, comparable convergence (Fig. 4)",
    background=[setup_associativity_condition, setup_ablation_methodology],
    metadata={
        "source_figure": "artifacts/2602.21204.pdf, Figure 4",
        "caption": "Fig. 4 | Training loss vs. wall-clock time on LaCT-LLM. Parallel form of Variant 2 achieves 1.19x end-to-end speedup while maintaining comparable convergence.",
    },
)

claim_parallel_form_speedup = claim(
    "**Synthesis (Sec. 6.2).** The fully parallel TTT formulation is "
    "(i) *exact* (theorem-proven equivalent to sequential recurrence, "
    "@claim_parallel_equivalent_to_recurrent), (ii) *fast* (up to 4.0x "
    "TTT-layer throughput, @obs_parallel_throughput), and (iii) *quality-"
    "preserving* (1.19x end-to-end training speedup with no convergence "
    "loss, @obs_parallel_end_to_end_speedup). It is enabled by exactly "
    "the same conditions (static kernel + no weight-norm) under which "
    "TTT reduces to standard linear attention, providing a unified "
    "explanation for both the simplification and parallelization "
    "benefits.",
    title="Synthesis: exact, 4.0x TTT-layer-faster, 1.19x end-to-end-faster, quality-preserving parallel TTT",
)

# ---------------------------------------------------------------------------
# Non-reducible cases (Appendix I) -- supports practical claims by
# bounding the parallelization regime.
# ---------------------------------------------------------------------------

claim_dynamic_kernel_breaks_parallel = claim(
    "**Non-reducible case 1 (Appendix I.1).** When the kernel-function "
    "parameters $W_0, W_2$ are *also* updated in the inner loop, the "
    "kernel becomes history-dependent: "
    "$\\phi_t(K_t) = \\mathrm{silu}(K_t W_{0,t}) \\odot (K_t W_{2,t})$ "
    "with $W_{0,t}$ depending on $\\mathrm{silu}'(K_{t-1} W_{0,t-1})$, "
    "which depends on $W_{0,t-1}$, etc. The nested $\\mathrm{silu}, "
    "\\mathrm{silu}'$ functions create a non-linear dependency chain "
    "that *prevents* expressing the output as a simple weighted sum "
    "over history, breaking the associativity required by parallel "
    "prefix scan. This is precisely why Step 1 (freeze $\\Theta$) is a "
    "*precondition* for parallelization.",
    title="Non-reducible case 1: dynamic kernel ($W_0, W_2$ updated) breaks associativity",
    background=[setup_associativity_condition],
    metadata={"source_section": "artifacts/2602.21204.pdf, Appendix I.1"},
)

claim_weight_norm_breaks_parallel = claim(
    "**Non-reducible case 2 (Appendix I.2).** Even with $\\Theta$ "
    "frozen, applying weight normalization (@setup_weight_norm_in_lact) "
    "introduces non-reducibility because normalization is *not* "
    "associative: $\\mathrm{Norm}(A + B) \\neq \\mathrm{Norm}(A) + "
    "\\mathrm{Norm}(B)$. The state recurrence becomes a nested "
    "normalization $S_{t+1} = \\mathrm{Norm}(\\mathrm{Norm}(S_{t-1} + \\ldots) "
    "+ \\phi(K_t)^\\top m_t)$ that imposes strict sequential dependency "
    "on the prefix scan. This explains why Step 2 (remove weight "
    "normalization) is the *other* precondition for parallelization.",
    title="Non-reducible case 2: weight normalization breaks associativity (non-distributive over +)",
    background=[setup_associativity_condition, setup_weight_norm_in_lact],
    metadata={"source_section": "artifacts/2602.21204.pdf, Appendix I.2"},
)

claim_practical_implications_summary = claim(
    "**Section 6 summary.** Three concrete practical benefits flow from "
    "the linear-attention reformulation of TTT-with-KV-binding "
    "(@claim_ttt_is_linear_attention):\n\n"
    "1. **Simplify** -- the six-step ablation trajectory "
    "(@claim_simplifications_preserve_performance) shows that complex "
    "TTT design choices motivated by the memorization view are largely "
    "redundant.\n"
    "2. **Parallelize** -- under the same simplifications "
    "(@claim_parallel_form_speedup) TTT admits a fully parallel "
    "formulation that yields up to 4.0x TTT-layer throughput and 1.19x "
    "end-to-end training speedup.\n"
    "3. **Generalize** -- the unified linear-attention reduction applies "
    "across LaCT, ViTTT (GLU + depthwise conv), Titans, and other "
    "TTT-KVB variants whose final layer is linear and bias-free.\n\n"
    "The boundary of the parallelizable regime is precisely characterized "
    "by the two non-reducibility cases (@claim_dynamic_kernel_breaks_parallel, "
    "@claim_weight_norm_breaks_parallel).",
    title="Section 6 summary: simplify + parallelize + generalize, with sharp parallel-regime boundary",
)

# ---------------------------------------------------------------------------
# Pass 2: strategies
# ---------------------------------------------------------------------------

# 6.1 -- ablation observations support the synthesis claim.
strat_simplifications_preserve = support(
    [
        obs_ablation_table2,
        obs_variant1_best,
        obs_variant6_minor_degradation,
        obs_remaining_components_marginal,
    ],
    claim_simplifications_preserve_performance,
    reason=(
        "The Table 2 ablation trajectory (@obs_ablation_table2) "
        "documents per-step empirical performance across LaCT-LLM, "
        "LaCT-NVS, and ViTTT. Variant 1 (@obs_variant1_best) -- which "
        "differs from baseline only in restricting inner-loop updates "
        "to the final layer (@setup_ablation_step1_last_layer_only) -- "
        "achieves the *best* performance on all three task families. "
        "Variant 6 (@obs_variant6_minor_degradation) -- standard linear "
        "attention -- is within +0.4 perplexity / -0.2 dB / +0.2% of "
        "baseline, demonstrating that *most* TTT design choices are "
        "redundant in the sense of contributing little to final "
        "performance (@obs_remaining_components_marginal); only deeper "
        "MLP (NVS) and Muon (LLM) provide non-trivial contributions. "
        "Together these observations show the LA-driven simplification "
        "(@claim_complexity_drift_under_memorization is the prevailing "
        "memorization-view rationale being undone) preserves task "
        "performance."
    ),
    prior=0.93,
    background=[
        setup_ablation_methodology,
        setup_ablation_step1_last_layer_only,
        setup_ablation_step6_remove_grad_orthog,
        claim_complexity_drift_under_memorization,
    ],
)

# 6.2 -- parallel equivalence theorem is a deduction from associativity.
strat_parallel_equivalent = deduction(
    [claim_thm_5_3],
    claim_parallel_equivalent_to_recurrent,
    reason=(
        "Under the associativity condition "
        "(@setup_associativity_condition) -- static $\\phi$ + no "
        "weight-norm -- the recurrence of Theorem 5.3 (@claim_thm_5_3) "
        "for $W_{1,t+1}$ is associative. The parallel formulation "
        "(@setup_parallel_formulation) follows from a four-step "
        "algebraic match: (i) unroll the momentum recurrence to closed "
        "form; (ii) unroll the weight recurrence; (iii) compute the "
        "sequential output as $\\Phi(Q_t)W_{1,t+1}$; (iv) verify the "
        "block-(t,i) entry of the parallel mask $(A \\odot M)^{\\uparrow L}$ "
        "equals $\\sum_{j=i}^t \\beta_i^j$, matching the sequential "
        "coefficient $c_i^t$. See Appendix H.2 for the four-step proof."
    ),
    background=[
        setup_associativity_condition,
        setup_parallel_formulation,
    ],
    prior=0.99,
)

# 6.2 parallel speedup -- combination of equivalence + throughput + e2e.
strat_parallel_speedup = support(
    [
        claim_parallel_equivalent_to_recurrent,
        obs_parallel_throughput,
        obs_parallel_end_to_end_speedup,
    ],
    claim_parallel_form_speedup,
    reason=(
        "The parallel form is *exact* "
        "(@claim_parallel_equivalent_to_recurrent), *fast* (up to 4.0x "
        "TTT-layer throughput, @obs_parallel_throughput), and "
        "*quality-preserving* (1.19x end-to-end training speedup with "
        "no convergence degradation, @obs_parallel_end_to_end_speedup). "
        "The three properties jointly substantiate the synthesis claim."
    ),
    prior=0.95,
    background=[setup_associativity_condition],
)

# Non-reducibility cases (Appendix I).
strat_dynamic_kernel_breaks_parallel = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_dynamic_kernel_breaks_parallel,
    reason=(
        "When $W_0, W_2$ are also updated (dynamic kernel), the "
        "expression for $\\phi_t$ at any step $t$ contains "
        "$\\mathrm{silu}'(K_{t-1}W_{0,t-1})$ from the previous step's "
        "gradient, which itself contains $\\mathrm{silu}'$ of an even "
        "earlier step's parameters. The nested $\\mathrm{silu}, "
        "\\mathrm{silu}'$ chain is non-linear in history and prevents "
        "expression as a sum over history, breaking associativity "
        "(@setup_associativity_condition). See Appendix I.1."
    ),
    background=[setup_associativity_condition],
    prior=0.99,
)

strat_weight_norm_breaks_parallel = deduction(
    [claim_assumption_holds_for_studied_archs],
    claim_weight_norm_breaks_parallel,
    reason=(
        "Even with $\\Theta$ frozen, weight normalization "
        "(@setup_weight_norm_in_lact) is non-distributive over addition: "
        "$\\mathrm{Norm}(A + B) \\neq \\mathrm{Norm}(A) + "
        "\\mathrm{Norm}(B)$. The state recurrence $S_{t+1} = "
        "\\mathrm{Norm}(\\mathrm{Norm}(S_{t-1} + \\ldots) + \\phi(K_t)^"
        "\\top m_t)$ becomes a strictly sequential nesting incompatible "
        "with parallel prefix scan (@setup_associativity_condition). "
        "See Appendix I.2."
    ),
    background=[setup_associativity_condition, setup_weight_norm_in_lact],
    prior=0.99,
)

# Section 6 summary
strat_practical_summary = support(
    [
        claim_simplifications_preserve_performance,
        claim_parallel_form_speedup,
        claim_dynamic_kernel_breaks_parallel,
        claim_weight_norm_breaks_parallel,
    ],
    claim_practical_implications_summary,
    reason=(
        "The summary (@claim_practical_implications_summary) is the "
        "conjunction of three positive results -- simplification "
        "(@claim_simplifications_preserve_performance), parallelization "
        "(@claim_parallel_form_speedup), and the unified LA reduction "
        "across LaCT, ViTTT, etc. (covered in Section 5) -- and the "
        "two boundary results "
        "(@claim_dynamic_kernel_breaks_parallel, "
        "@claim_weight_norm_breaks_parallel) that sharply characterize "
        "the parallelizable regime. Each premise is supported by its "
        "own evidence; the summary aggregates them."
    ),
    prior=0.95,
)

# Connect to the contribution claim from motivation.
strat_practical_contribution = support(
    [claim_practical_implications_summary],
    claim_contribution_practical,
    reason=(
        "The Section 6 summary "
        "(@claim_practical_implications_summary) substantiates the "
        "three concrete benefits announced as Contribution 3 in the "
        "introduction (@claim_contribution_practical): simplify, "
        "parallelize, generalize. Each benefit is anchored by "
        "experimental evidence (Table 2, Fig. 4) and theoretical "
        "characterizations of the parallelizable regime."
    ),
    prior=0.95,
)


__all__ = [
    # 6.1 ablation trajectory
    "setup_ablation_methodology",
    "setup_ablation_step1_last_layer_only",
    "setup_ablation_step2_remove_weight_norm",
    "setup_ablation_step3_collapse_mlp",
    "setup_ablation_step4_remove_pertoken_lr",
    "setup_ablation_step5_remove_momentum",
    "setup_ablation_step6_remove_grad_orthog",
    # ablation observations
    "obs_ablation_table2",
    "obs_variant1_best",
    "obs_variant6_minor_degradation",
    "obs_remaining_components_marginal",
    "claim_simplifications_preserve_performance",
    # 6.2 parallel
    "setup_associativity_condition",
    "setup_parallel_formulation",
    "claim_parallel_equivalent_to_recurrent",
    "obs_parallel_throughput",
    "obs_parallel_end_to_end_speedup",
    "claim_parallel_form_speedup",
    # Appendix I
    "claim_dynamic_kernel_breaks_parallel",
    "claim_weight_norm_breaks_parallel",
    # summary
    "claim_practical_implications_summary",
]
