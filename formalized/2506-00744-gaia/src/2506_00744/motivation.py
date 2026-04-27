"""Section 1: Introduction and motivation for Hybrid Quadratic-Linear Transformers."""

from gaia.lang import claim, setting, question, contradiction, support

# ---------------------------------------------------------------------------
# Settings: definitions of the two transformer families and the design goal
# ---------------------------------------------------------------------------

setup_causal_seq = setting(
    "All models studied are causal sequence-processing neural networks. At each "
    "time step $t$, the model receives an input vector $x_t \\in \\mathbb{R}^{d_{in}}$ "
    "and produces an output $y_t \\in \\mathbb{R}^{d_{out}}$ while maintaining an "
    "internal memory of all inputs received so far.",
    title="Common causal sequence-processing setting",
)

def_quadratic_transformer = setting(
    "The quadratic transformer (QT) is the standard transformer of "
    "Vaswani et al. [@Vaswani2017]: at every time step, queries are matched against "
    "key-value pairs stored explicitly for each previous step; outputs are computed "
    "by softmax attention over the stored pairs (KV-memory). Storage scales linearly "
    "with sequence length and self-attention scales quadratically.",
    title="Definition: quadratic transformer (KV-memory)",
)

def_linear_transformer = setting(
    "A linear transformer (LT) / fast weight programmer (FWP) replaces softmax "
    "attention by an outer-product update of a fixed-size matrix-valued state "
    "(fast weight memory, FW-memory) [@Schmidhuber1992; @Katharopoulos2020]. The "
    "per-step computation is constant in $t$, so total time is linear in sequence "
    "length and there is no explicit context-window cap.",
    title="Definition: linear transformer / fast weight programmer (FW-memory)",
)

def_deltanet = setting(
    "DeltaNet [@Schlag2021; @Yang2024Delta] is a linear transformer whose fast "
    "weight matrix is updated by the classic delta learning rule [@Widrow1960]: "
    "$W_t = W_{t-1} + \\sigma(\\beta_t)(v_t - W_{t-1}\\phi(k_t)) \\otimes \\phi(k_t)$, "
    "with a slow-net-generated dynamic learning rate $\\sigma(\\beta_t) \\in (0,1)$. "
    "It enables certain state-tracking computations that softmax attention cannot "
    "express [@Grazzi2025; @Siems2025DeltaProduct].",
    title="Definition: DeltaNet (FW-memory with delta rule)",
)

def_hqlt = setting(
    "A Hybrid Quadratic-Linear Transformer (HQLT) is a single-layer architecture "
    "that maintains both KV-memory $(K_t, V_t)$ and FW-memory $W_t$ in parallel and "
    "produces an output by combining a softmax-attention term and a fast-weight "
    "term that share the same query/key/value generators.",
    title="Definition: Hybrid Quadratic-Linear Transformer (HQLT)",
)

cls_inspiration = setting(
    "The Complementary Learning Systems (CLS) hypothesis [@McClelland1995CLS] "
    "posits that the brain divides labor between distinct but interacting memory "
    "systems (e.g., hippocampal episodic vs neocortical semantic), each suited to "
    "demands the other cannot meet. The paper takes this as inspiration for a "
    "machine analogue: complementary linear and quadratic memory systems.",
    title="Background: Complementary Learning Systems analogy",
)

# ---------------------------------------------------------------------------
# Open question framing the paper
# ---------------------------------------------------------------------------

q_design = question(
    "How can a single sequence-processing memory system simultaneously achieve "
    "precise long-range retrieval (a strength of softmax/KV-memory), unbounded "
    "context length and high expressivity (strengths of FW-memory/DeltaNet), when "
    "these properties are individually incompatible inside either base model?",
    title="Research question: blending complementary memory systems",
)

# ---------------------------------------------------------------------------
# Claims established as backdrop in the introduction (Table 1)
# ---------------------------------------------------------------------------

claim_complementarity_table = claim(
    "KV-memory (quadratic transformer) and FW-memory (linear transformer / FWP) "
    "have complementary properties on four axes:\n\n"
    "| Property            | Key-value memory | Fast weight memory |\n"
    "|---------------------|------------------|---------------------|\n"
    "| Complexity          | quadratic        | linear              |\n"
    "| Context length      | bounded          | unbounded           |\n"
    "| Retrieval precision | high             | low                 |\n"
    "| Expressivity        | low              | high                |\n",
    title="Complementarity of KV-memory vs FW-memory (Table 1)",
    metadata={
        "source_table": "artifacts/2506.00744.pdf, Table 1",
    },
)

claim_qt_quadratic_cost = claim(
    "Standard softmax self-attention has time and memory complexity quadratic in "
    "sequence length $t$, because at each step the query is dot-producted with all "
    "$t$ stored keys and the resulting scores weight all $t$ stored values "
    "[@Vaswani2017]. In practice this forces a finite, predetermined sliding "
    "context window beyond which inputs are discarded.",
    title="QT has quadratic cost and bounded context",
)

claim_lt_linear_cost = claim(
    "A linear transformer / fast weight programmer maintains a fixed-size matrix "
    "state $W_t \\in \\mathbb{R}^{d_{out} \\times d_{key}}$ updated by an outer "
    "product per step. Per-step cost is independent of $t$, so total time is "
    "linear in sequence length and the model can in principle process arbitrarily "
    "long sequences [@Katharopoulos2020; @Schmidhuber1992].",
    title="LT/FWP has linear cost and unbounded context",
)

claim_qt_precise_recall = claim(
    "Softmax over per-step keys yields sharp, item-addressable retrieval: the "
    "query selects a near-one-hot weighting over stored values, enabling precise "
    "recall of specific past tokens. This precision is what FW-memory sacrifices "
    "when softmax is replaced by a separable kernel [@Vaswani2017; @Katharopoulos2020].",
    title="QT enables precise key-value retrieval",
)

claim_deltanet_expressivity = claim(
    "DeltaNet (and related delta-rule FWPs) can solve regular-language recognition "
    "tasks such as parity and modular arithmetic that quadratic transformers and "
    "purely additive linear attention provably cannot solve at fixed depth "
    "[@Grazzi2025; @Siems2025DeltaProduct]. This is the 'expressivity' axis of the "
    "complementarity table.",
    title="DeltaNet has state-tracking expressivity beyond softmax attention",
)

# ---------------------------------------------------------------------------
# Top-level proposal of the paper
# ---------------------------------------------------------------------------

proposal_three_blends = claim(
    "The paper proposes and compares three blending methods that combine KV-memory "
    "and FW-memory inside a single layer: (i) Delayed-Streaming HQLT, (ii) "
    "Delayed-Chunk HQLT, and (iii) Synchronous HQLT. They differ in how and when "
    "input information is delivered to each memory system. The goal of the empirical "
    "study is to identify which blending policy best preserves the strengths of "
    "both base models simultaneously.",
    title="Paper proposal: three HQLT blending methods to compare",
    background=[def_hqlt, q_design],
)

proposal_synchronous_best = claim(
    "The paper's main empirical conclusion is that the Synchronous HQLT is the "
    "best overall blending strategy: it preserves the FW-memory expressivity "
    "advantage of DeltaNet (which the delayed variants lose), while matching or "
    "improving on the language-modeling, retrieval, and POMDP-RL performance of "
    "either base model.",
    title="Main conclusion: Synchronous HQLT is the best blending method",
)

claim_compatibility_with_efficient_kernels = claim(
    "All HQLT variants are compatible with existing hardware-efficient implementations "
    "of quadratic and linear attention (e.g., FlashAttention-2 and the "
    "flash-linear-attention library), because the quadratic and linear branches "
    "remain structurally identical to their base operators and only the per-step "
    "outputs are summed/mixed.",
    title="HQLTs remain compatible with FlashAttention / flash-linear-attention kernels",
)

# ---------------------------------------------------------------------------
# Modelled tension: layer-wise hybrids vs intra-layer blending
# ---------------------------------------------------------------------------

claim_layerwise_hybrid_alt = claim(
    "An alternative way to combine quadratic and linear memory is the layer-wise "
    "strategy used by xLSTM, Griffin, Samba and similar models: different layers "
    "use different memory operators, but no single layer integrates both "
    "operators on the same key/value/query stream.",
    title="Alternative: layer-wise hybrids (xLSTM/Griffin/Samba)",
)

# Layer-wise and intra-layer hybrids can both exist as architectures, so they
# are NOT a logical contradiction. The paper argues intra-layer blending is
# preferable here because QT and LT *share* their key/value/query generators.

# ---------------------------------------------------------------------------
# Structural inferences in the introduction
# ---------------------------------------------------------------------------

strat_complementarity_motivates_hybrid = support(
    [claim_qt_quadratic_cost, claim_lt_linear_cost, claim_qt_precise_recall, claim_deltanet_expressivity],
    claim_complementarity_table,
    reason=(
        "The four-axis complementarity in Table 1 (@claim_complementarity_table) is a "
        "summary of four established properties: quadratic cost & bounded context for QT "
        "(@claim_qt_quadratic_cost), linear cost & unbounded context for LT (@claim_lt_linear_cost), "
        "precise recall for QT (@claim_qt_precise_recall), and DeltaNet's state-tracking "
        "expressivity beyond softmax (@claim_deltanet_expressivity). Each row of Table 1 "
        "is justified by one of these claims drawn from the prior literature."
    ),
    prior=0.95,
    background=[def_quadratic_transformer, def_linear_transformer, def_deltanet],
)

strat_proposal_motivation = support(
    [claim_complementarity_table],
    proposal_three_blends,
    reason=(
        "The four-way complementarity (@claim_complementarity_table) means no single "
        "memory operator achieves all desirable properties; the brain's solution under "
        "the CLS hypothesis (@cls_inspiration) is to maintain multiple memory systems with "
        "complementary strengths. By analogy, the paper proposes intra-layer blending of "
        "QT and LT as three concrete designs that differ in *when* information enters each "
        "system."
    ),
    prior=0.85,
    background=[q_design, def_hqlt, cls_inspiration],
)


__all__ = [
    "setup_causal_seq",
    "def_quadratic_transformer",
    "def_linear_transformer",
    "def_deltanet",
    "def_hqlt",
    "cls_inspiration",
    "q_design",
    "claim_complementarity_table",
    "claim_qt_quadratic_cost",
    "claim_lt_linear_cost",
    "claim_qt_precise_recall",
    "claim_deltanet_expressivity",
    "proposal_three_blends",
    "proposal_synchronous_best",
    "claim_compatibility_with_efficient_kernels",
    "claim_layerwise_hybrid_alt",
    "strat_complementarity_motivates_hybrid",
    "strat_proposal_motivation",
]
