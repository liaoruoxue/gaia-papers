"""Section 3: Three HQLT blending methods (Delayed-Streaming, Delayed-Chunk, Synchronous)."""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    def_hqlt,
    proposal_three_blends,
    claim_complementarity_table,
)
from .s2_background import (
    def_kv_memory_state,
    def_softmax_attention,
    def_la_recurrent_form,
    def_delta_rule_update,
    def_chunkwise,
    claim_deltanet_choice_for_hybrid,
)

# ---------------------------------------------------------------------------
# Settings: shared variables used by all HQLT variants
# ---------------------------------------------------------------------------

def_hqlt_state = setting(
    "An HQLT layer at step $t$ maintains: (1) KV-memory of size $S$, "
    "$K_{t-1} \\in \\mathbb{R}^{d_{key} \\times S}$ and "
    "$V_{t-1} \\in \\mathbb{R}^{d_{out} \\times S}$; and (2) FW-memory "
    "$W_{t-1} \\in \\mathbb{R}^{d_{out} \\times d_{key}}$. The slow projection "
    "$[q_t, k_t, v_t, \\beta_t] = W^{slow} x_t$ produces the per-step "
    "query/key/value/learning-rate variables (with $W^{slow} \\in "
    "\\mathbb{R}^{(2 d_{key} + d_{out} + 1) \\times d_{in}}$).",
    title="Setting: shared HQLT state and slow projection (Eq. 9)",
)

def_remove_op = setting(
    "Let $\\ominus$ denote the column-removal operation taking a matrix and one "
    "of its column vectors and returning the matrix with that column deleted.",
    title="Setting: column-removal operator $\\ominus$",
)

# ---------------------------------------------------------------------------
# Section 3.1: Delayed-Streaming HQLT
# ---------------------------------------------------------------------------

def_delayed_stream = setting(
    "The Delayed-Streaming HQLT updates KV-memory by removing the oldest pair "
    "$(k_{t-S}, v_{t-S})$ that falls outside the window and inserting the new "
    "pair $(k_t, v_t)$:\n\n"
    "$$K_t = K_{t-1} \\ominus k_{t-S} \\oplus k_t,\\qquad "
    "V_t = V_{t-1} \\ominus v_{t-S} \\oplus v_t.$$\n\n"
    "The pair *removed* from KV-memory is then fed into FW-memory via the delta "
    "rule:\n\n"
    "$$W_t = W_{t-1} + \\sigma(\\beta_t)(v_{t-S} - W_{t-1}\\phi(k_{t-S})) \\otimes \\phi(k_{t-S}),$$\n\n"
    "and the output combines both branches: $y_t = W_t\\phi(q_t) + V_t \\mathrm{softmax}(K_t^{\\top} q_t)$.",
    title="Setting: Delayed-Streaming HQLT (Eqs. 10-15)",
)

claim_delayed_stream_division = claim(
    "In Delayed-Streaming HQLT, FW-memory $W_t$ stores information from all time "
    "steps $\\tau \\le t-S$ (anything older than $S$ steps), while KV-memory "
    "$(K_t, V_t)$ holds the $S$ most recent steps $t-S < \\tau \\le t$. The two "
    "memory systems thus implement a strict division of labor *over time*: recent "
    "context to KV-memory, old context to FW-memory.",
    title="Delayed-Streaming has age-based division of labor between memories",
    background=[def_delayed_stream],
)

claim_delayed_stream_state_size = claim(
    "Total state size of a Delayed-Streaming HQLT layer is "
    "$S(d_{in} + d_{out}) + d_{out} d_{in}$ matrix entries, fixed independently of "
    "sequence length. This achieves untruncated context modeling at fixed memory "
    "cost.",
    title="Delayed-Streaming has fixed memory independent of $t$",
    background=[def_delayed_stream, def_hqlt_state],
)

# Three mixing variants

def_sum_mixing = setting(
    "Sum mixing combines the two branch outputs additively: "
    "$y_t = W_t \\phi(q_t) + V_t \\mathrm{softmax}(K_t^{\\top} q_t)$ (Eq. 15).",
    title="Setting: sum mixing",
)
def_dynamic_scalar_mixing = setting(
    "Dynamic scalar mixing introduces two slow-net-generated scalars "
    "$\\alpha_t^{FW}, \\alpha_t^{KV} \\in [0, 1]$ (after sigmoid) and combines as "
    "$y_t = \\alpha_t^{FW} \\cdot W_t \\phi(q_t) + \\alpha_t^{KV} \\cdot V_t \\mathrm{softmax}(K_t^{\\top} q_t)$ "
    "(Eq. 16).",
    title="Setting: dynamic scalar mixing",
)
def_dynamic_vector_mixing = setting(
    "Dynamic vector mixing generates a slow-net vector "
    "$\\gamma_t \\in \\mathbb{R}^{d_{out}}$ used as an elementwise convex blend: "
    "$y_t = \\gamma_t \\odot W_t \\phi(q_t) + (1 - \\gamma_t) \\odot V_t \\mathrm{softmax}(K_t^{\\top} q_t)$ "
    "(Eq. 17). It adds about 25M parameters to the 340M model.",
    title="Setting: dynamic vector mixing",
)

# ---------------------------------------------------------------------------
# Section 3.2: Delayed-Chunk HQLT
# ---------------------------------------------------------------------------

def_delayed_chunk = setting(
    "Delayed-Chunk HQLT inserts a softmax inside the intra-chunk attention term "
    "of the chunk-wise update Eq. 6: the second term becomes "
    "$V_n \\mathrm{softmax}(K_n^{\\top} Q_n \\odot M)$ while the inter-chunk term "
    "$W_n Q_n$ continues to flow through the fast weight matrix. The same chunk "
    "scheme is also used at inference time. As a consequence FW-memory only sees "
    "an entire previous chunk and is delayed by up to $S$ steps relative to the "
    "current input.",
    title="Setting: Delayed-Chunk HQLT (intra-chunk softmax inside Eq. 6)",
)

claim_delayed_chunk_connection = claim(
    "Delayed-Chunk HQLT is structurally equivalent to the Infini-attention design "
    "of Munkhdalai et al. [@Munkhdalai2024Infini]: both apply softmax to the "
    "intra-chunk attention term and accumulate inter-chunk content into a fast "
    "weight memory delayed by one chunk.",
    title="Delayed-Chunk HQLT corresponds to Infini-attention [@Munkhdalai2024Infini]",
    background=[def_delayed_chunk],
)

# ---------------------------------------------------------------------------
# Section 3.3: Synchronous HQLT
# ---------------------------------------------------------------------------

def_synchronous = setting(
    "Synchronous HQLT uses the same equations as Delayed-Streaming HQLT except "
    "that the *current* key-value pair $(k_t, v_t)$ is fed simultaneously to both "
    "FW-memory and KV-memory, rather than only to KV-memory. The FW-memory update "
    "becomes $W_t = W_{t-1} + \\sigma(\\beta_t)(v_t - W_{t-1}\\phi(k_t)) \\otimes \\phi(k_t)$, "
    "i.e., FW-memory has no delay.",
    title="Setting: Synchronous HQLT (current $(k_t, v_t)$ goes to both memories)",
)

claim_synchronous_no_delay = claim(
    "Because the *current* key-value pair is delivered to FW-memory in the same "
    "step it is generated (@def_synchronous), Synchronous HQLT can use FW-memory's "
    "expressive computation on the most recent input — there is no $S$-step lag "
    "between input availability and FW-memory update, unlike either delayed "
    "variant.",
    title="Synchronous HQLT has zero-delay access to current input in FW-memory",
    background=[def_synchronous],
)

claim_synchronous_arora_connection = claim(
    "Synchronous HQLT generalises the hybrid design of Arora et al. "
    "[@Arora2024Based] from vanilla linear attention to DeltaNet. Arora et al. "
    "use a vanilla LA whose performance lags far behind softmax attention, "
    "limiting the achievable hybrid quality, whereas Synchronous HQLT inherits "
    "DeltaNet's stronger expressivity.",
    title="Synchronous HQLT extends Arora et al.'s hybrid to a stronger FWP",
    background=[def_synchronous],
)

# ---------------------------------------------------------------------------
# Cross-cutting structural claim about the design space
# ---------------------------------------------------------------------------

claim_delayed_lose_expressivity = claim(
    "Delayed-Streaming and Delayed-Chunk HQLTs feed FW-memory only with inputs "
    "that have already been observed for several time steps (the delay equals "
    "the KV-window size). For state-tracking tasks that require updating the "
    "fast-weight state on every fresh input (e.g., parity, modular arithmetic), "
    "this delay prevents the FW component from operating in real time and "
    "predicts that the delayed variants cannot solve such tasks.",
    title="Delayed variants cannot leverage FW-memory expressivity in real time",
    background=[def_delayed_stream, def_delayed_chunk],
)

claim_synchronous_keeps_expressivity = claim(
    "Synchronous HQLT is the only variant in which FW-memory receives every "
    "input synchronously; it therefore preserves DeltaNet's state-tracking "
    "expressivity and is predicted to solve parity/modular arithmetic tasks at "
    "the same level as standalone DeltaNet.",
    title="Synchronous HQLT preserves DeltaNet's state-tracking expressivity",
    background=[def_synchronous],
)

# ---------------------------------------------------------------------------
# Reasoning: predictions of the three designs follow from their definitions
# ---------------------------------------------------------------------------

strat_pred_delayed_lose_expressivity = deduction(
    [claim_synchronous_no_delay],
    claim_delayed_lose_expressivity,
    reason=(
        "By construction the delayed variants delay the input fed to FW-memory by "
        "the KV-window size $S$, while synchronous delivery (@claim_synchronous_no_delay) "
        "is exactly the property the delayed designs lack. State-tracking tasks like "
        "parity require updating the fast-weight state on the current input; a delay "
        "of $S$ steps interleaves $S$ unrelated tokens between the input and the "
        "update, breaking the inductive structure DeltaNet exploits. Therefore the "
        "delayed variants are *predicted* not to solve these tasks."
    ),
    prior=0.92,
    background=[def_delayed_stream, def_delayed_chunk, def_synchronous],
)

strat_pred_synchronous_keeps_expressivity = deduction(
    [claim_synchronous_no_delay, claim_deltanet_choice_for_hybrid],
    claim_synchronous_keeps_expressivity,
    reason=(
        "Synchronous HQLT delivers the current $(k_t, v_t)$ to FW-memory with no "
        "delay (@claim_synchronous_no_delay), and FW-memory is instantiated as "
        "DeltaNet (@claim_deltanet_choice_for_hybrid). Because DeltaNet alone "
        "solves parity/modular arithmetic, and the FW branch in Synchronous HQLT "
        "receives the same inputs at the same times as standalone DeltaNet, the "
        "Synchronous variant inherits DeltaNet's state-tracking expressivity by "
        "design."
    ),
    prior=0.93,
    background=[def_synchronous],
)

# Wire division/state-size into the delayed-loses-expressivity argument, since the
# strict age-based division is exactly what causes the delay.
strat_division_implies_delay = support(
    [claim_delayed_stream_division, claim_delayed_stream_state_size],
    claim_delayed_lose_expressivity,
    reason=(
        "Delayed-Streaming's strict age-based division of labor "
        "(@claim_delayed_stream_division) is precisely what creates the $S$-step "
        "delay: by construction the FW branch only sees information that has "
        "first cycled through the KV-window of size $S$. The fixed state size "
        "(@claim_delayed_stream_state_size) confirms there is no mechanism to "
        "send recent inputs directly to FW-memory in this design."
    ),
    prior=0.9,
    background=[def_delayed_stream],
)


__all__ = [
    "def_hqlt_state",
    "def_remove_op",
    "def_delayed_stream",
    "claim_delayed_stream_division",
    "claim_delayed_stream_state_size",
    "def_sum_mixing",
    "def_dynamic_scalar_mixing",
    "def_dynamic_vector_mixing",
    "def_delayed_chunk",
    "claim_delayed_chunk_connection",
    "def_synchronous",
    "claim_synchronous_no_delay",
    "claim_synchronous_arora_connection",
    "claim_delayed_lose_expressivity",
    "claim_synchronous_keeps_expressivity",
    "strat_pred_delayed_lose_expressivity",
    "strat_pred_synchronous_keeps_expressivity",
    "strat_division_implies_delay",
]
