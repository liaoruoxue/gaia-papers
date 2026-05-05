"""Motivation: TTT-KVB is conventionally interpreted as test-time memorization.

Section 1 (Introduction) of Liu et al. 2026 [@Liu2026]. Sets up the central
dialectic:

* The prevailing interpretation views TTT-with-KV-binding as a
  *storage-and-retrieval* (memorization) mechanism, justifying
  increasingly complex inner-loop architectures (deep MLPs, momentum,
  weight normalization, gradient orthogonalization).
* The paper identifies four empirical anomalies that contradict this
  interpretation, and proposes an alternative:  TTT-KVB is *secretly*
  linear attention, with the inner loop acting as a structured mixer of
  query, key, and value vectors rather than a memory.

The introduction also previews three classes of practical benefits
(simplify / parallelize / generalize) unlocked by the new perspective.
"""

from gaia.lang import claim, setting, question

# ---------------------------------------------------------------------------
# Background settings (definitional / framing)
# ---------------------------------------------------------------------------

setup_ttt_paradigm = setting(
    "**Test-Time Training (TTT)** is a paradigm in which (a subset of) "
    "model parameters continue to be updated *during inference*. "
    "Originally introduced to address train-test distribution shift "
    "[@Sun2020], TTT has more recently been deployed as an architectural "
    "primitive replacing standard softmax attention [@Vaswani2017] in "
    "transformer sequence models, motivated by its linear-time compute "
    "and constant memory usage during autoregressive decoding "
    "[@Zhang2025; @Behrouz2024].",
    title="Setup: Test-Time Training (TTT) as a sequence-modeling primitive",
)

setup_ttt_kvb_focus = setting(
    "Among TTT formulations, this paper focuses on **TTT with KV binding "
    "(TTT-KVB)** [@Tandon2025], in which the inner-loop optimizes a "
    "self-supervised key-value association objective. For each input "
    "token, the projected key $k$ serves as input and the projected value "
    "$v$ serves as a regression target; the inner-loop updates a small "
    "fast-weight network $f_\\theta$ to fit $f_\\theta(k) \\approx v$. "
    "TTT-KVB is contrasted with TTT-E2E methods that backpropagate from "
    "the final task loss [@Tandon2025; @Behrouz2025b].",
    title="Setup: TTT-KVB scope (key-value binding inner-loop)",
)

setup_memorization_interpretation = setting(
    "**Prevailing interpretation.** TTT-KVB is widely interpreted as a "
    "form of *online meta-learning* or *memorization* [@Sun2025; "
    "@Finn2017; @Metz2018]: the inner loop dynamically constructs a "
    "temporary key-value (KV) map by optimizing $f_\\theta$ on previously "
    "observed tokens, and the subsequent inference step is viewed as "
    "*querying* this stored knowledge through $q$. Under this view, "
    "architectural capacity, optimizer choice, and the number of "
    "inner-loop steps are all motivated by achieving more faithful "
    "memorization of key-value associations -- which has driven the "
    "adoption of deep inner-loop networks, sophisticated optimizers, and "
    "normalization schemes [@Zhang2025; @Han2025; @Behrouz2024; @Dalal2025].",
    title="Setup: storage-and-retrieval (memorization) interpretation of TTT-KVB",
)

# ---------------------------------------------------------------------------
# Open question(s) driving the paper
# ---------------------------------------------------------------------------

q_central = question(
    "Is the storage-and-retrieval interpretation of TTT-with-KV-binding "
    "an accurate functional account of how these architectures actually "
    "operate? Equivalently: is the inner loop *memorizing* a key-value "
    "mapping that is later *retrieved* by queries, or is some other "
    "computational mechanism in play?",
    title="Does TTT-KVB really function by test-time memorization?",
)

q_alternative = question(
    "If TTT-KVB does not memorize, what does it actually compute, and "
    "what practical implications does the alternative interpretation "
    "have for the design and implementation of TTT layers?",
    title="If not memorization, then what -- and what does the answer enable?",
)

# ---------------------------------------------------------------------------
# Claim restating the prevailing interpretation as a falsifiable proposition
# ---------------------------------------------------------------------------

claim_memorization_hypothesis = claim(
    "**The memorization hypothesis (the proposition the paper sets out "
    "to falsify).** Under the storage-and-retrieval interpretation "
    "(@setup_memorization_interpretation), TTT-with-KV-binding functions "
    "as a key-value memory: the inner-loop optimization *stores* "
    "associations $k_i \\mapsto v_i$ inside the fast-weight network "
    "$f_\\theta$, and the query $q$ *retrieves* the stored value at "
    "inference time. If true, this mechanism implies several testable "
    "consequences: (i) lower inner-loop loss should improve task "
    "performance (more accurate memorization), (ii) reversing the "
    "optimization sign (gradient ascent) should hurt performance "
    "(unmemorization), (iii) queries and keys must share a common "
    "semantic space (otherwise the query is out-of-distribution for the "
    "memorized function), and (iv) replacing $q$ with $k$ should change "
    "outputs because attention is similarity-based.",
    title="Memorization hypothesis: TTT-KVB stores KV associations and retrieves with $q$",
    background=[setup_ttt_kvb_focus, setup_memorization_interpretation],
)

# ---------------------------------------------------------------------------
# High-level claims previewing the four empirical anomalies (Section 4)
# ---------------------------------------------------------------------------

claim_anomaly_distributional_asymmetry_preview = claim(
    "**Anomaly 1 (Distributional Asymmetry).** Unlike standard attention, "
    "in which queries and keys share the same semantic space because they "
    "are both used to compute similarity scores, the converged TTT models "
    "examined in this paper exhibit a pronounced and consistent "
    "*distributional mismatch* between $Q$ and $K$. The fast-weight "
    "network is trained on the $K$ distribution but evaluated on $Q$, so "
    "its outputs cannot be interpreted as reliable retrieval of stored "
    "$V$.",
    title="Anomaly 1 (preview): Q and K do not share a common distribution",
)

claim_anomaly_replace_q_with_k_preview = claim(
    "**Anomaly 2 (Replace Q with K).** Replacing the query $q$ with the "
    "key $k$ at the TTT layer's output stage has *negligible effect* on "
    "task performance across LaCT-LLM, LaCT-NVS, and ViTTT. In standard "
    "attention this substitution would induce degenerate self-similarity "
    "behavior and a substantial performance drop, which is *not* observed.",
    title="Anomaly 2 (preview): swapping Q for K barely affects task performance",
)

claim_anomaly_inner_vs_outer_preview = claim(
    "**Anomaly 3 (Optimization vs. Performance).** Increasing the number "
    "of inner-loop gradient steps at inference time *reduces* the "
    "inner-loop loss (better key-value fitting) but *consistently degrades* "
    "downstream task performance on both LLM and NVS tasks. Better "
    "memorization is associated with worse, not better, task quality.",
    title="Anomaly 3 (preview): better inner-loss leads to worse downstream perf",
)

claim_anomaly_gradient_ascent_preview = claim(
    "**Anomaly 4 (Gradient Ascent).** Replacing inner-loop gradient "
    "*descent* with gradient *ascent* (flipping the sign of all fast-weight "
    "gradients, which explicitly *worsens* the fit to the key-value "
    "regression objective) preserves task performance and in some cases "
    "even slightly improves it -- across all evaluated models and tasks. "
    "This is the most striking anomaly because it directly negates the "
    "memorization objective.",
    title="Anomaly 4 (preview): gradient ascent preserves or improves performance",
)

# ---------------------------------------------------------------------------
# Core contribution claims (high-level statements; details in s4-s7)
# ---------------------------------------------------------------------------

claim_contribution_anomalies = claim(
    "**Contribution 1 (Empirical anomalies).** The paper identifies four "
    "systematic anomalies (@claim_anomaly_distributional_asymmetry_preview, "
    "@claim_anomaly_replace_q_with_k_preview, "
    "@claim_anomaly_inner_vs_outer_preview, "
    "@claim_anomaly_gradient_ascent_preview) in the empirical behavior "
    "of TTT-with-KV-binding models that are jointly *incompatible* with "
    "the storage-and-retrieval interpretation. Each anomaly is "
    "demonstrated on at least two of the three task families (language "
    "modeling on LaCT-LLM, novel-view synthesis on LaCT-NVS, image "
    "classification on ViTTT-B).",
    title="Contribution 1: four empirical anomalies falsifying the memorization view",
)

claim_contribution_equivalence = claim(
    "**Contribution 2 (Theoretical equivalence).** The paper proves "
    "(Theorems 5.1-5.3) that a broad class of TTT-with-KV-binding "
    "architectures -- including those with multi-layer MLP inner loops "
    "and momentum-augmented gradient updates -- can be analytically "
    "rewritten as a *learned linear attention operator* of the form "
    "$o_t = \\hat{q}_t \\bigl(S_0 + \\sum_{i \\le t} \\hat{k}_i^\\top "
    "\\hat{v}_i\\bigr)$, where the effective query, key, and value "
    "vectors are functions of the inner-loop hidden representation. "
    "Under this view the inner loop performs *structured history-dependent "
    "mixing* of $q$, $k$, $v$ rather than meta-learning a key-value memory. "
    "The required structural condition is that the inner-loop final layer "
    "is linear and bias-free.",
    title="Contribution 2: TTT-KVB analytically equivalent to learned linear attention",
)

claim_contribution_practical = claim(
    "**Contribution 3 (Practical consequences).** Three concrete benefits "
    "follow from the equivalence:\n\n"
    "* **Simplify.** Six-step ablation trajectory (only update last layer; "
    "remove weight normalization; collapse multi-layer MLP to single "
    "linear layer; remove per-token learning rates; remove momentum; "
    "remove gradient orthogonalization) reduces complex TTT formulations "
    "(LaCT, ViTTT) to standard linear attention with only minor "
    "performance degradation (+0.4 perplexity / -0.2 dB PSNR / +0.2% "
    "Top-1 accuracy compared to baseline).\n"
    "* **Parallelize.** Variants 2-6 admit a fully parallel implementation "
    "via prefix-scan that achieves up to 4.0x TTT-layer throughput "
    "(124.6M vs 30.18M tokens/sec on LLM) and a 1.19x end-to-end training "
    "speedup, while preserving model quality.\n"
    "* **Generalize.** Two representative TTT variants (LaCT, ViTTT GLU + "
    "depthwise convolution) are explicitly cast in linear-attention form, "
    "establishing TTT-KVB as a *flexible learned linear attention* "
    "mechanism whose enhanced representational capacity comes from the "
    "learnable kernel function $\\phi$ rather than from memorization.",
    title="Contribution 3: simplification, parallelization, and unification benefits",
)

__all__ = [
    "setup_ttt_paradigm",
    "setup_ttt_kvb_focus",
    "setup_memorization_interpretation",
    "q_central",
    "q_alternative",
    "claim_memorization_hypothesis",
    "claim_anomaly_distributional_asymmetry_preview",
    "claim_anomaly_replace_q_with_k_preview",
    "claim_anomaly_inner_vs_outer_preview",
    "claim_anomaly_gradient_ascent_preview",
    "claim_contribution_anomalies",
    "claim_contribution_equivalence",
    "claim_contribution_practical",
]
