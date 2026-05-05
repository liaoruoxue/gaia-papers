"""Section 4: Empirical Contradictions to Memorization.

Four anomalies in TTT-with-KV-binding model behaviour that are jointly
incompatible with the storage-and-retrieval (memorization) interpretation:

* 4.1 Better inner-loss leads to worse downstream performance (Fig. 1).
* 4.2 TTT with gradient ascent preserves performance (Table 1).
* 4.3 Distributional asymmetry between Q and K (Fig. 2).
* 4.4 Replacing Q with K leaves performance unchanged (Table 1).

Each anomaly is presented at three levels: (i) the *prediction* the
memorization view would make, (ii) the *empirical observation*, (iii)
the *direct contradiction* between (i) and (ii). The contradictions are
modeled with `contradiction()` operators in Pass 2.
"""

from gaia.lang import claim, setting, support, contradiction

from .motivation import (
    claim_memorization_hypothesis,
    claim_anomaly_distributional_asymmetry_preview,
    claim_anomaly_replace_q_with_k_preview,
    claim_anomaly_inner_vs_outer_preview,
    claim_anomaly_gradient_ascent_preview,
    claim_contribution_anomalies,
)
from .s3_preliminaries import (
    setup_fast_weights,
    setup_kvq_projection,
    setup_inner_loop_loss,
    setup_update_then_query,
    setup_inner_loop_hyperparameters,
    setup_storage_retrieval_definition,
)

# ---------------------------------------------------------------------------
# 4.1 Better Inner Loss Leads to Worse Performance (Fig. 1)
# ---------------------------------------------------------------------------

setup_inner_step_protocol = setting(
    "**Inner-step protocol (Sec. 4.1).** The number of inner-loop "
    "gradient steps at *inference time* is varied over "
    "$\\{1, 2, 4, 8, 16, 32, 64\\}$ for a *pretrained* TTT model -- "
    "without changing the architecture, the training data, or the "
    "learned slow-weight parameters. The reference architecture is "
    "LaCT [@Zhang2025] evaluated on (a) language modeling perplexity "
    "and (b) novel view synthesis (NVS) PSNR.",
    title="Protocol: vary inner-loop steps at inference (1, 2, 4, 8, 16, 32, 64)",
)

claim_memorization_predicts_more_steps_better = claim(
    "**Memorization prediction (Sec. 4.1).** Under the storage-and-"
    "retrieval interpretation (@setup_storage_retrieval_definition), "
    "the inner-loop loss "
    "$\\mathcal{L}(f_\\theta(k), v) = \\|f_\\theta(k) - v\\|_2^2$ is a "
    "natural proxy for memorization quality: lower loss corresponds to "
    "more accurate encoding of the key-value mapping. Therefore, "
    "increasing the number of inner-loop steps -- which empirically "
    "reduces inner-loop loss -- *should improve, or at least not harm,* "
    "downstream task performance (PSNR / perplexity).",
    title="Memorization prediction: more inner steps $\\Rightarrow$ better task perf",
    background=[setup_storage_retrieval_definition, setup_inner_loop_loss],
)

obs_inner_loss_decreases_with_steps = claim(
    "**Observation (Fig. 1, inner-loss panels).** As inner-loop iterations "
    "are increased from 1 to 64 at inference, the *inner-loop loss* "
    "decreases monotonically -- from approximately $0$ down to "
    "$\\approx -60$ on the NVS task and from approximately $-0.8$ down to "
    "$\\approx -1.4$ on the LLM task (LaCT uses the Frobenius dot product, "
    "which is *more negative* when fitting is better). Inner-loop "
    "optimization is thus *successful* by its own metric.",
    title="Observation: inner-loop loss decreases monotonically with steps (1 -> 64)",
    background=[setup_inner_step_protocol, setup_inner_loop_loss],
    metadata={
        "source_figure": "artifacts/2602.21204.pdf, Figure 1 (inner loss panels)",
        "caption": "Fig. 1 | Inner-Loop Optimization vs. Performance. Inner-loss decreases over 1-64 steps on both LaCT-LLM and LaCT-NVS.",
    },
)

obs_perf_degrades_with_more_steps = claim(
    "**Observation (Fig. 1, performance panels).** Despite the inner-loop "
    "loss improving (@obs_inner_loss_decreases_with_steps), downstream "
    "task performance *degrades* as inner-loop iterations are increased "
    "from 1 to 64:\n\n"
    "| Task        | Metric             | At 1 step        | At 64 steps      |\n"
    "|-------------|--------------------|------------------|------------------|\n"
    "| LaCT-NVS    | PSNR (higher = better) | $\\approx 26$ dB | $\\approx 18$ dB (drop ~8 dB) |\n"
    "| LaCT-LLM    | Perplexity (lower = better) | $\\approx 15.2$ | $\\approx 15.6$ (rise ~0.4) |\n\n"
    "The inverse relationship between inner-loop fit and task performance "
    "holds across both task families, with the NVS degradation being "
    "particularly large.",
    title="Observation: PSNR drops ~8 dB and perplexity rises ~0.4 as inner-steps increase",
    background=[setup_inner_step_protocol],
    metadata={
        "source_figure": "artifacts/2602.21204.pdf, Figure 1 (PSNR / Perplexity panels)",
        "caption": "Fig. 1 | Inner-Loop Optimization vs. Performance. Increasing inner-loop iterations improves inner-loop loss but degrades task performance, contradicting the memorization-based interpretation of TTT.",
    },
)

claim_anomaly_inner_vs_outer = claim(
    "**Anomaly 3 (formal).** The inverse relationship between inner-loop "
    "loss (which improves with more steps, "
    "@obs_inner_loss_decreases_with_steps) and downstream task "
    "performance (which *degrades* with more steps, "
    "@obs_perf_degrades_with_more_steps) directly contradicts the "
    "memorization prediction (@claim_memorization_predicts_more_steps_better) "
    "that better KV fitting should be at least non-harmful. The anomaly "
    "holds *both* on the LLM (perplexity) task and the NVS (PSNR) task.",
    title="Anomaly 3 (formal): better inner-loss $\\Rightarrow$ worse downstream perf",
)

# ---------------------------------------------------------------------------
# 4.2 TTT with Gradient Ascent (Table 1, columns 'Gradient Ascent')
# ---------------------------------------------------------------------------

setup_gradient_ascent_protocol = setting(
    "**Gradient-ascent protocol (Sec. 4.2).** All inner-loop fast-weight "
    "gradients are sign-flipped: the parameter update becomes "
    "$\\theta_{t+1} = \\theta_t + \\eta \\nabla_\\theta \\mathcal{L}$ "
    "instead of $\\theta_{t+1} = \\theta_t - \\eta \\nabla_\\theta "
    "\\mathcal{L}$. This is applied at *both training and inference* "
    "(the model is pretrained with gradient ascent in the inner loop). "
    "Notably, for LaCT [@Zhang2025] the inner loss is the Frobenius "
    "inner product, so flipping the sign of the gradient is equivalent "
    "to *negating the loss itself*. Three reference models: LaCT-LLM, "
    "LaCT-NVS, ViTTT-B [@Han2025].",
    title="Protocol: replace inner-loop $-\\eta \\nabla \\mathcal{L}$ with $+\\eta \\nabla \\mathcal{L}$",
)

claim_memorization_predicts_grad_ascent_breaks = claim(
    "**Memorization prediction (Sec. 4.2).** Under the storage-and-"
    "retrieval interpretation (@setup_storage_retrieval_definition), "
    "gradient ascent on the KV-binding loss explicitly *worsens* the "
    "fit $f_\\theta(k) \\approx v$. If TTT really memorized key-value "
    "associations, gradient ascent would destroy the memory and induce "
    "a *strong negative effect* on downstream task performance.",
    title="Memorization prediction: gradient ascent should sharply degrade performance",
    background=[setup_storage_retrieval_definition, setup_gradient_ascent_protocol],
)

obs_grad_ascent_inner_loss_increases = claim(
    "**Observation.** Gradient ascent in the inner loop *consistently "
    "increases* the inner-loop loss compared to standard gradient descent "
    "(by construction: the gradient sign is flipped, so the parameter "
    "update moves in the loss-increasing direction). The inner-loop fit "
    "$f_\\theta(k) \\approx v$ is therefore *demonstrably worse* than "
    "under the baseline.",
    title="Observation: gradient ascent demonstrably worsens inner-loop fit",
    background=[setup_gradient_ascent_protocol, setup_inner_loop_loss],
)

obs_grad_ascent_table1 = claim(
    "**Observation (Table 1, Gradient-Ascent row).** Despite the worsened "
    "inner-loop fit, downstream task performance under gradient ascent is "
    "*indistinguishable from* (and slightly better than) the baseline:\n\n"
    "| Model      | Metric                 | Baseline | Gradient Ascent |\n"
    "|------------|------------------------|---------:|----------------:|\n"
    "| LaCT-LLM   | Perplexity (lower=better) | 16.43 | **16.19** |\n"
    "| LaCT-NVS   | PSNR (higher=better) dB | 25.94 | 25.85 |\n"
    "| ViTTT      | Top-1 Acc (higher=better) % | 79.34 | **79.61** |\n\n"
    "On two of three task families gradient ascent is *better* than the "
    "baseline; on the third (NVS) the gap is within noise (-0.09 dB).",
    title="Observation (Table 1): gradient ascent matches or slightly beats baseline on 3 tasks",
    background=[setup_gradient_ascent_protocol],
    metadata={
        "source_table": "artifacts/2602.21204.pdf, Table 1, row 'Gradient Ascent'",
        "caption": "Table 1 | Observations Contradicting the Storage-and-Retrieval Interpretation of TTT.",
    },
)

claim_anomaly_gradient_ascent = claim(
    "**Anomaly 4 (formal).** Gradient ascent inverts the inner-loop "
    "objective and demonstrably worsens KV fitting "
    "(@obs_grad_ascent_inner_loss_increases) -- yet downstream task "
    "performance is *preserved or improved* across LLM, NVS, and image "
    "classification (@obs_grad_ascent_table1). This directly contradicts "
    "the memorization prediction (@claim_memorization_predicts_grad_ascent_breaks) "
    "that TTT relies on a meaningful KV-fitting objective.",
    title="Anomaly 4 (formal): gradient ascent preserves downstream perf",
)

# ---------------------------------------------------------------------------
# 4.3 Distributional Asymmetry Between Q and K (Fig. 2)
# ---------------------------------------------------------------------------

setup_qk_visualization_protocol = setting(
    "**Q-K distribution protocol (Sec. 4.3).** For a pretrained LaCT "
    "[@Zhang2025] NVS model, the projected query vectors $Q$ and key "
    "vectors $K$ are collected for every token across every layer. "
    "Their joint distribution is visualized via t-SNE [@Maaten2008] on a "
    "per-layer basis (Fig. 2 shows blocks 1, 4, 7). The same protocol is "
    "applied to value $V$ and output $O$ for comparison.",
    title="Protocol: t-SNE visualization of $(Q, K)$ and $(V, O)$ in pretrained LaCT-NVS",
)

claim_memorization_requires_qk_overlap = claim(
    "**Memorization prediction (Sec. 4.3).** Under the storage-and-"
    "retrieval interpretation, the inner-loop fast-weight network "
    "$f_\\theta$ is trained on inputs drawn from the $K$ distribution "
    "and used to retrieve $V$ at evaluation time on inputs drawn from "
    "the $Q$ distribution. For *retrieval to be reliable*, $Q$ must lie "
    "within the support of $K$ -- otherwise $f_\\theta$ is evaluated "
    "out-of-distribution and its outputs cannot be guaranteed to lie on "
    "the manifold of $V$. **Substantial distributional overlap between "
    "$Q$ and $K$ is therefore necessary** for the retrieval interpretation "
    "to be coherent.",
    title="Memorization prediction: $Q$ must lie in $K$-support for reliable retrieval",
    background=[setup_storage_retrieval_definition, setup_kvq_projection],
)

obs_qk_distributions_disjoint = claim(
    "**Observation (Fig. 2, Q-K panel).** The t-SNE visualization of $Q$ "
    "and $K$ vectors collected across all tokens and layers (blocks 1, "
    "4, 7) of a pretrained LaCT-NVS model shows a *pronounced and "
    "consistent mismatch* between the $Q$ and $K$ point clouds at every "
    "layer examined. The two distributions form visually disjoint or "
    "weakly overlapping clusters, indicating that $Q$ samples lie *outside* "
    "the support of $K$ samples on which $f_\\theta$ was trained.",
    title="Observation (Fig. 2): Q and K t-SNE distributions are visibly disjoint at every layer",
    background=[setup_qk_visualization_protocol],
    metadata={
        "source_figure": "artifacts/2602.21204.pdf, Figure 2 (Q vs K panel)",
        "caption": "Fig. 2 | Distributional Asymmetry Between Q and K. t-SNE visualizations of (Q, K) and (V, O) features in pretrained LaCT (Zhang et al., 2025) on the NVS task, showing the TTT inner loop is evaluated out of distribution.",
    },
)

obs_vo_distributions_also_disjoint = claim(
    "**Observation (Fig. 2, V-O panel).** A similar mismatch is observed "
    "between value $V$ and output $O$ point clouds: $O$ does *not* lie "
    "on the manifold of $V$ targets at any layer. This corroborates the "
    "Q-K mismatch as a systemic property rather than an isolated artefact "
    "of one layer or one feature set.",
    title="Observation (Fig. 2): V and O distributions are also disjoint",
    background=[setup_qk_visualization_protocol],
    metadata={
        "source_figure": "artifacts/2602.21204.pdf, Figure 2 (V vs O panel)",
        "caption": "Fig. 2 | (V, O) features show analogous distributional mismatch.",
    },
)

claim_anomaly_distributional_asymmetry = claim(
    "**Anomaly 1 (formal).** The pronounced distributional mismatch "
    "between $Q$ and $K$ (@obs_qk_distributions_disjoint), corroborated "
    "by the analogous $V$-$O$ mismatch (@obs_vo_distributions_also_disjoint), "
    "directly contradicts the memorization prediction "
    "(@claim_memorization_requires_qk_overlap) that the function "
    "$f_\\theta$ trained on $K$ must be evaluated within its support to "
    "function as a retrieval mechanism. The TTT inner loop is therefore "
    "*systematically* evaluated out-of-distribution, regardless of how "
    "accurately it fits its training data.",
    title="Anomaly 1 (formal): TTT inner loop is systematically evaluated out-of-distribution",
)

# ---------------------------------------------------------------------------
# 4.4 Replacing Q with K (Table 1, 'Replace Q with K' row)
# ---------------------------------------------------------------------------

setup_q_replacement_protocol = setting(
    "**Q-replacement protocol (Sec. 4.4).** At the TTT layer's output "
    "stage (after the inner-loop update on $(k_t, v_t)$), the query "
    "$q_t$ is *replaced by* $k_t$, i.e. the TTT output becomes "
    "$o_t = f_{\\theta_{t+1}}(k_t)$ instead of $f_{\\theta_{t+1}}(q_t)$. "
    "All other components -- inner-loop optimization, slow-weight "
    "projections that produced $q_t$ -- are unchanged. Models tested: "
    "LaCT-LLM (perplexity), LaCT-NVS (PSNR), ViTTT-B (Top-1 accuracy).",
    title="Protocol: replace $q_t$ with $k_t$ at TTT layer output",
)

claim_memorization_predicts_q_required = claim(
    "**Memorization prediction (Sec. 4.4).** In standard attention, "
    "replacing $Q$ with $K$ would induce *degenerate self-similarity* "
    "behavior: the attention weights would be dominated by $\\langle k, "
    "k\\rangle$ self-products, collapsing the mechanism. Under the "
    "memorization view of TTT, the query $q$ plays an analogous "
    "*retrieval* role, so replacing $q$ with $k$ should similarly "
    "disrupt the read-out and induce a *substantial drop in performance*.",
    title="Memorization prediction: replacing $q$ with $k$ should sharply degrade perf",
    background=[setup_storage_retrieval_definition, setup_kvq_projection],
)

obs_q_replacement_table1 = claim(
    "**Observation (Table 1, 'Replace Q with K' row).** Replacing $q$ "
    "with $k$ produces *negligible* changes in task performance:\n\n"
    "| Model      | Metric                 | Baseline | Replace Q with K |\n"
    "|------------|------------------------|---------:|-----------------:|\n"
    "| LaCT-LLM   | Perplexity (lower=better) | 16.43 | **16.18** |\n"
    "| LaCT-NVS   | PSNR (higher=better) dB | 25.94 | **25.95** |\n"
    "| ViTTT      | Top-1 Acc (higher=better) % | 79.34 | 79.18 |\n\n"
    "On LaCT-LLM and LaCT-NVS the substitution is in fact mildly *better* "
    "than baseline; on ViTTT the gap is within noise (-0.16%). The "
    "magnitude of the change (max 0.16% absolute on accuracy, 0.25 on "
    "perplexity) is far below what a similarity-based retrieval "
    "mechanism would tolerate.",
    title="Observation (Table 1): replacing Q with K leaves performance essentially unchanged",
    background=[setup_q_replacement_protocol],
    metadata={
        "source_table": "artifacts/2602.21204.pdf, Table 1, row 'Replace Q with K'",
        "caption": "Table 1 | Replacing queries with keys breaks the retrieval interpretation, yet task performance remains mostly unchanged.",
    },
)

claim_anomaly_replace_q_with_k = claim(
    "**Anomaly 2 (formal).** The negligible performance change under "
    "Q -> K substitution (@obs_q_replacement_table1) directly contradicts "
    "the retrieval-based prediction (@claim_memorization_predicts_q_required) "
    "that the query must be a meaningful, distinct probe for similarity-"
    "based read-out. The query's apparent functional irrelevance is "
    "incompatible with TTT operating as a similarity-based retrieval "
    "system.",
    title="Anomaly 2 (formal): query $q$ is functionally non-essential",
)

# ---------------------------------------------------------------------------
# Summary claim: the four anomalies jointly falsify the memorization view.
# ---------------------------------------------------------------------------

claim_memorization_view_falsified = claim(
    "**Summary of Section 4.** The four anomalies "
    "(@claim_anomaly_inner_vs_outer, @claim_anomaly_gradient_ascent, "
    "@claim_anomaly_distributional_asymmetry, "
    "@claim_anomaly_replace_q_with_k) jointly establish that TTT-with-KV-"
    "binding does *not* operate as test-time memorization. Downstream "
    "behavior is largely insensitive to (a) the *quality* of inner-loop "
    "optimization, (b) the *direction* of inner-loop optimization, "
    "(c) whether the mechanism even has access to a meaningful query "
    "signal, and (d) the in-distribution vs out-of-distribution status "
    "of the queries fed to the trained fast-weight function. Each of "
    "(a)-(d) is necessary for a storage-and-retrieval interpretation; "
    "the conjunction of their failures falsifies that interpretation.",
    title="Summary: four anomalies jointly falsify the memorization view of TTT-KVB",
)

# ---------------------------------------------------------------------------
# Pass 2: support strategies wiring observations -> anomalies -> falsification
# ---------------------------------------------------------------------------

# 4.1 -- two observations jointly support the formal anomaly statement.
strat_anomaly_inner_vs_outer = support(
    [obs_inner_loss_decreases_with_steps, obs_perf_degrades_with_more_steps],
    claim_anomaly_inner_vs_outer,
    reason=(
        "The protocol (@setup_inner_step_protocol) varies inner-loop "
        "iterations from 1 to 64 at inference time. The first observation "
        "(@obs_inner_loss_decreases_with_steps) confirms the inner-loop "
        "loss decreases monotonically (memorization-fidelity proxy "
        "improves), while the second (@obs_perf_degrades_with_more_steps) "
        "shows downstream PSNR drops by ~8 dB and perplexity rises by "
        "~0.4 over the same range. The conjunction of these two "
        "observations is what constitutes Anomaly 3: better inner-loop "
        "fit accompanies *worse* downstream performance. The "
        "memorization view (@claim_memorization_predicts_more_steps_better) "
        "predicts the opposite (or at worst no degradation), so the "
        "joint observation is anomalous."
    ),
    prior=0.95,
    background=[setup_inner_step_protocol, setup_inner_loop_loss],
)

# 4.2
strat_anomaly_gradient_ascent = support(
    [obs_grad_ascent_inner_loss_increases, obs_grad_ascent_table1],
    claim_anomaly_gradient_ascent,
    reason=(
        "The gradient-ascent protocol "
        "(@setup_gradient_ascent_protocol) flips the sign of the "
        "fast-weight gradients. By construction this *worsens* the "
        "inner-loop fit (@obs_grad_ascent_inner_loss_increases). Yet "
        "Table 1 (@obs_grad_ascent_table1) shows downstream perplexity "
        "(LaCT-LLM), PSNR (LaCT-NVS), and Top-1 accuracy (ViTTT) are "
        "preserved or slightly improved. The conjunction is exactly "
        "Anomaly 4. The memorization view "
        "(@claim_memorization_predicts_grad_ascent_breaks) predicts "
        "strong negative effect from sign-inverted optimization, which "
        "is not observed."
    ),
    prior=0.95,
    background=[setup_gradient_ascent_protocol, setup_inner_loop_loss],
)

# 4.3
strat_anomaly_distributional_asymmetry = support(
    [obs_qk_distributions_disjoint, obs_vo_distributions_also_disjoint],
    claim_anomaly_distributional_asymmetry,
    reason=(
        "Fig. 2's t-SNE visualization "
        "(@setup_qk_visualization_protocol) shows two consistent "
        "distributional mismatches across all examined layers: $Q$ vs "
        "$K$ (@obs_qk_distributions_disjoint) and $V$ vs $O$ "
        "(@obs_vo_distributions_also_disjoint). The corroborating "
        "$V$-$O$ mismatch rules out a one-off layer-specific artifact. "
        "The memorization view requires $Q$ to lie within $K$-support "
        "for retrieval to be reliable "
        "(@claim_memorization_requires_qk_overlap), so the observed "
        "systematic mismatch directly establishes Anomaly 1: the inner "
        "loop is evaluated out-of-distribution."
    ),
    prior=0.92,
    background=[setup_qk_visualization_protocol, setup_kvq_projection],
)

# 4.4
strat_anomaly_replace_q_with_k = support(
    [obs_q_replacement_table1],
    claim_anomaly_replace_q_with_k,
    reason=(
        "The Q -> K replacement protocol "
        "(@setup_q_replacement_protocol) substitutes $k_t$ for $q_t$ at "
        "the TTT layer's output stage. Table 1 "
        "(@obs_q_replacement_table1) shows the substitution leaves "
        "perplexity (16.43 -> 16.18 LLM), PSNR (25.94 -> 25.95 NVS), "
        "and Top-1 accuracy (79.34 -> 79.18 ViTTT) essentially "
        "unchanged -- in fact slightly better on two of three tasks. "
        "Since the memorization view treats $q$ as a meaningful "
        "similarity probe (@claim_memorization_predicts_q_required), "
        "this query-irrelevance is exactly Anomaly 2."
    ),
    prior=0.95,
    background=[setup_q_replacement_protocol],
)

# Connect motivation-section preview claims to the formal versions
# proven in this section. The previews and the formal claims are
# logically equivalent re-statements; we use a deduction-style support
# with high prior.
strat_preview_inner_vs_outer = support(
    [claim_anomaly_inner_vs_outer],
    claim_anomaly_inner_vs_outer_preview,
    reason=(
        "The formal Anomaly 3 statement (@claim_anomaly_inner_vs_outer) "
        "is the substantive content previewed in Sec. 1 "
        "(@claim_anomaly_inner_vs_outer_preview). They make the same "
        "empirical claim at different levels of detail."
    ),
    prior=0.99,
)

strat_preview_grad_ascent = support(
    [claim_anomaly_gradient_ascent],
    claim_anomaly_gradient_ascent_preview,
    reason=(
        "The formal Anomaly 4 statement (@claim_anomaly_gradient_ascent) "
        "is the substantive content previewed in Sec. 1 "
        "(@claim_anomaly_gradient_ascent_preview)."
    ),
    prior=0.99,
)

strat_preview_qk_asymmetry = support(
    [claim_anomaly_distributional_asymmetry],
    claim_anomaly_distributional_asymmetry_preview,
    reason=(
        "The formal Anomaly 1 statement "
        "(@claim_anomaly_distributional_asymmetry) is the substantive "
        "content previewed in Sec. 1 "
        "(@claim_anomaly_distributional_asymmetry_preview)."
    ),
    prior=0.99,
)

strat_preview_replace_q = support(
    [claim_anomaly_replace_q_with_k],
    claim_anomaly_replace_q_with_k_preview,
    reason=(
        "The formal Anomaly 2 statement (@claim_anomaly_replace_q_with_k) "
        "is the substantive content previewed in Sec. 1 "
        "(@claim_anomaly_replace_q_with_k_preview)."
    ),
    prior=0.99,
)

# Summary: four anomalies jointly falsify the memorization view.
strat_memorization_falsified = support(
    [
        claim_anomaly_inner_vs_outer,
        claim_anomaly_gradient_ascent,
        claim_anomaly_distributional_asymmetry,
        claim_anomaly_replace_q_with_k,
    ],
    claim_memorization_view_falsified,
    reason=(
        "Each of the four anomalies "
        "(@claim_anomaly_inner_vs_outer, @claim_anomaly_gradient_ascent, "
        "@claim_anomaly_distributional_asymmetry, "
        "@claim_anomaly_replace_q_with_k) negates a *necessary* "
        "consequence of the storage-and-retrieval interpretation: "
        "(a) inner-loss should track outer perf; (b) optimization "
        "*direction* should matter; (c) $Q$-$K$ distributional overlap "
        "should hold; (d) the query should be a meaningful retrieval "
        "probe. The joint failure of (a)-(d) -- across LLM, NVS, and "
        "(for two of the four) image classification -- exhausts the "
        "memorization view's empirical commitments and falsifies it as "
        "a functional account of TTT-with-KV-binding."
    ),
    prior=0.92,
    background=[setup_storage_retrieval_definition],
)

# Connect summary to the contribution claim from motivation
strat_anomalies_contribution = support(
    [claim_memorization_view_falsified],
    claim_contribution_anomalies,
    reason=(
        "The synthesized falsification of the memorization view "
        "(@claim_memorization_view_falsified), built from four "
        "independent anomalies on at least two of three task families "
        "each, is exactly the empirical content claimed as Contribution 1 "
        "in the introduction (@claim_contribution_anomalies)."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Contradiction operators: each formal anomaly contradicts the
# corresponding memorization-view prediction. These are genuine
# contradictions (NOT (A AND B)) because the memorization prediction
# and the observed anomaly cannot both be true.
# ---------------------------------------------------------------------------

contra_inner_vs_outer = contradiction(
    claim_memorization_predicts_more_steps_better,
    claim_anomaly_inner_vs_outer,
    reason=(
        "Memorization predicts more inner steps $\\Rightarrow$ at "
        "least non-harmful effect on downstream perf "
        "(@claim_memorization_predicts_more_steps_better); the formal "
        "anomaly (@claim_anomaly_inner_vs_outer) asserts more inner "
        "steps consistently *degrade* downstream perf on both LLM and "
        "NVS. These cannot both be true on the same model and task."
    ),
    prior=0.97,
)

contra_gradient_ascent = contradiction(
    claim_memorization_predicts_grad_ascent_breaks,
    claim_anomaly_gradient_ascent,
    reason=(
        "Memorization predicts gradient ascent (which inverts the "
        "KV-fit objective) should *sharply degrade* perf "
        "(@claim_memorization_predicts_grad_ascent_breaks); the formal "
        "anomaly (@claim_anomaly_gradient_ascent) asserts perf is "
        "preserved or slightly improved. These cannot both hold."
    ),
    prior=0.97,
)

contra_qk_overlap = contradiction(
    claim_memorization_requires_qk_overlap,
    claim_anomaly_distributional_asymmetry,
    reason=(
        "Memorization requires substantial $Q$-$K$ distributional "
        "overlap for reliable retrieval "
        "(@claim_memorization_requires_qk_overlap). Anomaly 1 "
        "(@claim_anomaly_distributional_asymmetry) asserts the "
        "opposite: a pronounced systematic $Q$-$K$ mismatch is observed "
        "in pretrained TTT models. These two propositions cannot both "
        "be true of the same trained model."
    ),
    prior=0.95,
)

contra_q_required = contradiction(
    claim_memorization_predicts_q_required,
    claim_anomaly_replace_q_with_k,
    reason=(
        "Memorization predicts replacing $q$ with $k$ should sharply "
        "degrade perf because the query is a meaningful retrieval probe "
        "(@claim_memorization_predicts_q_required); Anomaly 2 "
        "(@claim_anomaly_replace_q_with_k) asserts perf is essentially "
        "unchanged. These cannot both hold."
    ),
    prior=0.95,
)

# Note: a top-level `contradiction(claim_memorization_hypothesis,
# claim_memorization_view_falsified)` would be redundant with the four
# per-anomaly contradictions above and would double-count evidence.
# We leave the dialectic to the per-anomaly contradictions and to the
# abduction operator in s5_linear_attention_equivalence.py
# (claim_ttt_is_linear_attention vs claim_memorization_hypothesis).


__all__ = [
    # 4.1 setup + obs + anomaly
    "setup_inner_step_protocol",
    "claim_memorization_predicts_more_steps_better",
    "obs_inner_loss_decreases_with_steps",
    "obs_perf_degrades_with_more_steps",
    "claim_anomaly_inner_vs_outer",
    # 4.2
    "setup_gradient_ascent_protocol",
    "claim_memorization_predicts_grad_ascent_breaks",
    "obs_grad_ascent_inner_loss_increases",
    "obs_grad_ascent_table1",
    "claim_anomaly_gradient_ascent",
    # 4.3
    "setup_qk_visualization_protocol",
    "claim_memorization_requires_qk_overlap",
    "obs_qk_distributions_disjoint",
    "obs_vo_distributions_also_disjoint",
    "claim_anomaly_distributional_asymmetry",
    # 4.4
    "setup_q_replacement_protocol",
    "claim_memorization_predicts_q_required",
    "obs_q_replacement_table1",
    "claim_anomaly_replace_q_with_k",
    # Summary
    "claim_memorization_view_falsified",
]
