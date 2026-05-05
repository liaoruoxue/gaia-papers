"""Priors for independent (leaf) claims in the 2602-21204 package.

All other (derived) claims have their belief computed by Belief Propagation
from these leaves and from the in-DSL ``prior=`` warrants on strategies.

Prior-assignment rationale:

* **Direct empirical observations** transcribed from a table or figure of the
  paper get high priors (0.92-0.95). The data themselves are not in dispute
  (we read them off Tables 1-2, Figs. 1-4); the question of whether they
  support the higher-level conclusions is what BP propagates.
* **Architectural / structural claims** about LaCT, ViTTT, Titans (e.g.
  the bias-free linear-final-layer assumption) get very high priors
  (0.95+) -- they are factual properties of those architectures that can be
  verified by reading the code/equations.
* **Citations to peer-reviewed prior findings** (DeltaNet = TTT with single
  linear layer; the restricted prior LA equivalence; shared compute profile
  across TTT variants) get high priors (0.85-0.95).
* **Memorization-view predictions** (more inner steps -> better, gradient
  ascent breaks model, Q-K must overlap, query is required) are
  *consequences* the prevailing literature derived from the storage-and-
  retrieval interpretation. Each is a defensible inference under that
  interpretation. Priors set in the 0.55-0.65 range -- they reflect what
  *would* be expected under the prevailing view, but BP via the contradiction
  operators with the corresponding anomalies will pull them down.
* **The memorization hypothesis itself** is the proposition the paper
  refutes. Prior set ~0.55: the prevailing view in the field, reasonable
  default before considering the anomaly evidence.
"""

from . import (
    # ----- Memorization-view predictions and hypothesis -----
    claim_memorization_hypothesis,
    claim_memorization_predicts_more_steps_better,
    claim_memorization_predicts_grad_ascent_breaks,
    claim_memorization_requires_qk_overlap,
    claim_memorization_predicts_q_required,
    # ----- Architecture-related structural claims -----
    claim_assumption_holds_for_studied_archs,
    claim_deltanet_equals_linear_ttt,
    claim_prior_la_equivalence_restricted,
    claim_ttt_shares_la_compute_profile,
    # ----- Direct figure / table observations -----
    obs_inner_loss_decreases_with_steps,
    obs_perf_degrades_with_more_steps,
    obs_grad_ascent_inner_loss_increases,
    obs_grad_ascent_table1,
    obs_qk_distributions_disjoint,
    obs_vo_distributions_also_disjoint,
    obs_q_replacement_table1,
    obs_ablation_table2,
    obs_variant1_best,
    obs_variant6_minor_degradation,
    obs_remaining_components_marginal,
    obs_parallel_throughput,
    obs_parallel_end_to_end_speedup,
)


PRIORS: dict = {
    # =====================================================================
    # The memorization hypothesis: the proposition the paper refutes.
    # =====================================================================
    claim_memorization_hypothesis: (
        0.55,
        "Set just above 0.5 to reflect that prior to this paper the "
        "storage-and-retrieval interpretation was the *prevailing* view "
        "in the TTT literature [@Sun2025; @Finn2017; @Metz2018; "
        "@Zhang2025; @Behrouz2024] and motivated essentially every "
        "post-2020 architectural elaboration of TTT-KVB. The "
        "contradiction operators with the four anomaly claims and with "
        "the synthesized falsification will pull this posterior sharply "
        "down once the empirical evidence flows through BP. Not set "
        "lower because, prior to the present paper's anomaly evidence, "
        "the hypothesis was treated as a working assumption rather "
        "than being independently questioned.",
    ),
    # =====================================================================
    # Memorization-view predictions: each is a consequence the prevailing
    # interpretation entails. Priors moderate (~0.55-0.65) -- they are
    # plausible *under that interpretation* but the BP contradiction
    # operators with the anomaly claims will resolve which side wins.
    # =====================================================================
    claim_memorization_predicts_more_steps_better: (
        0.60,
        "Direct entailment of the storage-and-retrieval interpretation: "
        "if KV pairs are being memorized, lower inner-loop loss should "
        "improve retrieval quality and hence task performance. Prior is "
        "in the moderate range because the inference is sound *given* "
        "the memorization premise -- the question is whether the "
        "memorization premise itself holds.",
    ),
    claim_memorization_predicts_grad_ascent_breaks: (
        0.65,
        "Even more direct than the inner-step prediction: gradient "
        "ascent explicitly inverts the memorization objective, so under "
        "any reasonable storage interpretation it should destroy the "
        "memory. Slightly higher prior than the inner-step prediction "
        "because the inference does not depend on the inner-loop "
        "loss-vs-quality monotonicity assumption.",
    ),
    claim_memorization_requires_qk_overlap: (
        0.60,
        "Standard out-of-distribution argument: a function trained on "
        "the K distribution and evaluated on Q must have substantial "
        "Q-K overlap for its outputs to be reliable. The argument is "
        "valid given that one views the inner loop as fitting a "
        "function k -> v; the question is whether that view is "
        "applicable.",
    ),
    claim_memorization_predicts_q_required: (
        0.60,
        "Direct analogy to standard attention's similarity-based "
        "retrieval: replacing q with k would induce degenerate "
        "self-similarity in standard attention, and the same is "
        "expected under any retrieval-based view of TTT. Prior set "
        "moderately because the analogy is not airtight (TTT's read-out "
        "is f(q), not <q, k>), so even a strict retrieval interpretation "
        "leaves some wiggle room.",
    ),
    # =====================================================================
    # Architectural / structural claims: factual properties of the studied
    # architectures.
    # =====================================================================
    claim_assumption_holds_for_studied_archs: (
        0.97,
        "Direct architectural fact: LaCT [@Zhang2025] uses a SwiGLU MLP "
        "ending in W_1 (bias-free linear final layer); ViTTT [@Han2025] "
        "uses a GLU whose final action is a linear projection; Titans "
        "[@Behrouz2024] is similarly structured. Verifiable by reading "
        "the architecture definitions in the cited papers / code; very "
        "high prior. Slight uncertainty (<3%) reflects the possibility "
        "that some published variants of Titans / LaCT might add bias "
        "terms in places not discussed here.",
    ),
    claim_deltanet_equals_linear_ttt: (
        0.93,
        "Cited well-known prior result [@Yang2024a]: DeltaNet "
        "[@Schlag2021] is equivalent to TTT with a single linear "
        "inner-loop layer trained with MSE loss. Established result in "
        "the linear-attention / fast-weight literature; uncertainty "
        "comes only from possible boundary cases of zero-init / no-bias "
        "exactly matching DeltaNet's published form.",
    ),
    claim_prior_la_equivalence_restricted: (
        0.95,
        "Cited result from Sun et al. (2025) [@Sun2025]: in the "
        "restricted setting of a *single linear* inner-loop layer with "
        "*zero initialization*, TTT is exactly equivalent to linear "
        "attention. Verifiable from the cited paper; very high prior.",
    ),
    claim_ttt_shares_la_compute_profile: (
        0.95,
        "Direct architectural observation: every TTT-KVB variant "
        "(LaCT, ViTTT, Titans, etc.) uses (i) per-token compute that "
        "does not grow with sequence length and (ii) constant-size "
        "fast-weight state. Both are immediate from the inner-loop "
        "definition (one GD step per token on a fixed-size network). "
        "Stated explicitly in [@Sun2025; @Zhang2025; @Han2025; "
        "@Behrouz2024].",
    ),
    # =====================================================================
    # Section 4 anomaly evidence: figure / table observations.
    # =====================================================================
    obs_inner_loss_decreases_with_steps: (
        0.93,
        "Fig. 1 (inner-loss panels) directly displays the monotone "
        "decrease in inner-loop loss from approximately 0 to "
        "approximately -60 (NVS) and from -0.8 to -1.4 (LLM) over "
        "1-64 inner-loop iterations. Direct read-off; the visualized "
        "monotonicity is unambiguous. Slight uncertainty for "
        "non-tabulated bin values.",
    ),
    obs_perf_degrades_with_more_steps: (
        0.93,
        "Fig. 1 (PSNR / perplexity panels) directly displays the "
        "performance degradation: PSNR drops from ~26 dB at 1 step to "
        "~18 dB at 64 steps; perplexity rises from ~15.2 to ~15.6 over "
        "the same range. Direct read-off from the figure.",
    ),
    obs_grad_ascent_inner_loss_increases: (
        0.97,
        "By construction: flipping the gradient sign moves the "
        "parameter in the loss-increasing direction. The fact that "
        "this *empirically* increases inner-loop loss is also "
        "noted in the paper text (Sec. 4.2): 'gradient ascent "
        "consistently increases the inner-loop loss'. Very high prior "
        "because the relationship is mathematically forced.",
    ),
    obs_grad_ascent_table1: (
        0.95,
        "Table 1 directly tabulates: LaCT-LLM 16.43 -> 16.19 perplexity "
        "(gradient ascent); LaCT-NVS 25.94 -> 25.85 dB PSNR; ViTTT "
        "79.34 -> 79.61 Top-1. Single-run point estimates without "
        "reported variance, hence < 1.0; transcribed verbatim.",
    ),
    obs_qk_distributions_disjoint: (
        0.92,
        "Fig. 2 (Q vs K t-SNE panels for blocks 1, 4, 7) directly "
        "shows the disjoint or weakly-overlapping point clouds across "
        "every layer examined. Qualitative conclusion is unambiguous "
        "from the visualization. Slight uncertainty because t-SNE "
        "embeddings can vary with hyperparameters and the figure does "
        "not provide a quantitative overlap metric.",
    ),
    obs_vo_distributions_also_disjoint: (
        0.92,
        "Fig. 2 (V vs O panels) shows the same pattern as Q vs K. "
        "Visual confirmation; same caveat about t-SNE-based qualitative "
        "claims as obs_qk_distributions_disjoint.",
    ),
    obs_q_replacement_table1: (
        0.95,
        "Table 1 directly tabulates the 'Replace Q with K' row: "
        "LaCT-LLM 16.43 -> 16.18 perplexity; LaCT-NVS 25.94 -> 25.95 "
        "dB; ViTTT 79.34 -> 79.18 Top-1. Single-run estimates, but the "
        "small magnitude of the gaps means even substantial run-to-run "
        "variance would not change the qualitative conclusion (perf "
        "essentially unchanged).",
    ),
    # =====================================================================
    # Section 6 ablation evidence (Table 2)
    # =====================================================================
    obs_ablation_table2: (
        0.93,
        "Table 2 directly tabulates per-variant performance for all "
        "three task families plus throughput. Six variants x three "
        "metrics x two TPS columns; each cell read off the table. "
        "Single-run point estimates without variance bars.",
    ),
    obs_variant1_best: (
        0.95,
        "Direct arithmetic comparison from Table 2: Variant 1's "
        "perplexity (15.93) < every other variant's; PSNR (25.97) "
        "$\\ge$ every other variant's; Top-1 (79.63%) ties with "
        "Variant 2's 79.63 (the dagger marks Variant 2 as inheriting "
        "Variant 1's value because the corresponding ablation does not "
        "apply to ViTTT). Very high prior; the claim is a numerical "
        "comparison.",
    ),
    obs_variant6_minor_degradation: (
        0.95,
        "Direct arithmetic from Table 2: Variant 6 vs Baseline = +0.4 / "
        "-0.2 / +0.2 on the three task metrics. The qualitative "
        "'minor' label is supported by the small absolute magnitude of "
        "the gaps relative to the metric range.",
    ),
    obs_remaining_components_marginal: (
        0.88,
        "Synthesis observation drawn from cell-by-cell variant deltas "
        "in Table 2. The author's narrative explicitly notes the two "
        "non-trivial exceptions (deeper MLP for NVS, gradient "
        "orthogonalization for LLM); the marginal-impact claim is "
        "supported by the small per-step variant deltas elsewhere. "
        "Slightly less than 0.92 because 'marginal' is somewhat "
        "qualitative and depends on how one weights small absolute "
        "changes against single-run noise.",
    ),
    obs_parallel_throughput: (
        0.95,
        "Direct read-off from Table 2's 'Parallel TPS' column: "
        "Variant 6 reaches 124.6M tokens/sec parallel vs 30.18M "
        "Variant 2 parallel (4.1x), and 89.67M Variant 6 recurrent "
        "(1.4x). The 4.0x figure quoted in the paper text matches the "
        "Variant 2 parallel/recurrent ratio (30.18 / ~7.5M extrapolated "
        "or, more directly, the parallel-vs-baseline ratio for the LLM "
        "task). Direct numerical comparison.",
    ),
    obs_parallel_end_to_end_speedup: (
        0.92,
        "Fig. 4 directly displays the 1.19x end-to-end training-loss-"
        "vs-wall-clock speedup, with parallel and recurrent variant 2 "
        "loss curves overlapping (comparable convergence). The 1.06x "
        "secondary speedup is also annotated. Direct read-off from "
        "the figure; slight uncertainty for missing tabulated values.",
    ),
}
