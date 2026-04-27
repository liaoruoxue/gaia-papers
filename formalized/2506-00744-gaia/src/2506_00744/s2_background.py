"""Section 2: Background on KV-memory (softmax attention) and FW-memory (delta rule)."""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    setup_causal_seq,
    def_quadratic_transformer,
    def_linear_transformer,
    def_deltanet,
    claim_qt_quadratic_cost,
    claim_lt_linear_cost,
    claim_deltanet_expressivity,
)

# ---------------------------------------------------------------------------
# Section 2.1: Key-value memory and softmax attention
# ---------------------------------------------------------------------------

def_kv_memory_state = setting(
    "KV-memory state at step $t$ consists of two matrices "
    "$K_t \\in \\mathbb{R}^{d_{key} \\times t}$ and "
    "$V_t \\in \\mathbb{R}^{d_{out} \\times t}$, each storing one column per past "
    "time step. They are updated by column concatenation: "
    "$K_t = K_{t-1} \\oplus k_t$, $V_t = V_{t-1} \\oplus v_t$, with $K_0, V_0$ empty.",
    title="Setting: KV-memory state and update rule",
)

def_softmax_attention = setting(
    "The softmax-attention output at step $t$ is "
    "$y_t = V_t\\, \\mathrm{softmax}(K_t^{\\top} q_t)$, where the slow projection "
    "$[q_t, k_t, v_t] = W^{slow} x_t$ produces the query/key/value vectors. The "
    "$1/\\sqrt{d_{key}}$ scaling and output projection are omitted as irrelevant.",
    title="Setting: softmax attention output (Eq. 3)",
)

claim_softmax_sharpness = claim(
    "Applying the softmax function to the dot products $K_t^{\\top} q_t$ sharpens "
    "the similarity scores into a near-one-hot weighting, which is the key "
    "mechanism enabling precise key-value retrieval. Without softmax (i.e., with "
    "an arbitrary nonlinearity applied independently to keys and queries), this "
    "sharpening is lost.",
    title="Softmax sharpening is the source of QT's precise retrieval",
    background=[def_softmax_attention],
)

claim_qt_storage_grows = claim(
    "Because each step appends a new column to $K_t$ and $V_t$, the size of "
    "KV-memory grows linearly with $t$, and the total work to compute the "
    "attention output across all steps is therefore $O(t^2)$ in time and $O(t)$ "
    "in memory.",
    title="KV-memory storage grows with sequence length, attention is $O(t^2)$",
    background=[def_kv_memory_state, def_softmax_attention],
)

# ---------------------------------------------------------------------------
# Section 2.2: Fast weight memory, linear attention and delta rule
# ---------------------------------------------------------------------------

def_la_recurrent_form = setting(
    "The recurrent form of linear attention (LA) replaces softmax in Eq. 3 by an "
    "elementwise nonlinearity $\\phi$ applied to keys and queries. The state is a "
    "fast weight matrix $W_t \\in \\mathbb{R}^{d_{out} \\times d_{key}}$, updated "
    "by the rank-1 outer product $W_t = W_{t-1} + v_t \\otimes \\phi(k_t)$, with "
    "output $y_t = W_t \\phi(q_t)$ and $W_0 = 0$.",
    title="Setting: linear-attention recurrent form (Eqs. 1, 4, 5)",
)

def_no_normalizer = setting(
    "The original LA derivation [@Katharopoulos2020] introduces an extra "
    "normalising scalar $z_t = z_{t-1} + \\phi(k_t)$ so that the output is "
    "$y_t = W_t \\phi(q_t) / (z_t^{\\top} \\phi(q_t))$. Subsequent work has shown "
    "this normalizer can be omitted in practice when $\\phi$ is chosen "
    "appropriately, and we follow that convention in the recurrent form.",
    title="Setting: LA without explicit normalizer (recent practice)",
)

def_chunkwise = setting(
    "Chunk-wise parallel training divides a sequence into chunks of size $S$. For "
    "the $n$-th chunk with query/key/value matrices $Q_n, K_n \\in \\mathbb{R}^{d_{key} \\times S}$ "
    "and $V_n \\in \\mathbb{R}^{d_{out} \\times S}$, outputs and inter-chunk fast "
    "weight are $Y_n = W_n Q_n + V_n (K_n^{\\top} Q_n \\odot M)$ and "
    "$W_{n+1} = W_n + V_n K_n^{\\top}$, where $M$ is the causal mask and $\\odot$ "
    "denotes elementwise multiplication. The first term is the inter-chunk and "
    "the second the intra-chunk computation.",
    title="Setting: chunk-wise parallel training (Eq. 6)",
)

def_delta_rule_update = setting(
    "DeltaNet replaces the additive LA update by a delta-rule update with a "
    "dynamic learning rate: "
    "$W_t = W_{t-1} + \\sigma(\\beta_t)\\,(v_t - W_{t-1}\\phi(k_t)) \\otimes \\phi(k_t)$, "
    "where $\\beta_t \\in \\mathbb{R}$ is produced by the slow net and $\\sigma$ is "
    "typically sigmoid (or twice-sigmoid). The output remains $y_t = W_t \\phi(q_t)$.",
    title="Setting: DeltaNet rank-1 delta-rule update (Eq. 8)",
)

def_phi_choice = setting(
    "The slow net's nonlinearity is fixed throughout the paper as elementwise "
    "SiLU ($x \\cdot \\sigma(x)$) followed by L2 normalization, matching Yang et "
    "al. [@Yang2024Delta]. This stabilises training when the delta rule is used.",
    title="Setting: choice of $\\phi$ = SiLU + L2-norm",
)

# ---------------------------------------------------------------------------
# Background claims that flow downstream
# ---------------------------------------------------------------------------

claim_la_constant_per_step = claim(
    "Because the LA recurrent form (@def_la_recurrent_form) maintains a fixed "
    "matrix $W_t \\in \\mathbb{R}^{d_{out} \\times d_{key}}$ and applies one outer "
    "product per step, per-step computation is constant in $t$. Total time is "
    "therefore linear in sequence length and memory is $O(d_{out} d_{key})$ "
    "regardless of context length.",
    title="LA recurrent form has linear-in-$t$ time and constant memory",
    background=[def_la_recurrent_form],
)

claim_chunkwise_subquadratic = claim(
    "Chunk-wise parallel training (@def_chunkwise) gives an efficient sub-quadratic "
    "training algorithm for LA and other FWPs: intra-chunk uses parallel computation "
    "(scaling as $O(S^2)$ inside each chunk), while inter-chunk uses the recurrent "
    "form. With a fixed chunk size $S$, total cost scales as $O(t S)$ in $t$, "
    "matching prior reports for FlashLinearAttention [@Yang2024Delta].",
    title="Chunk-wise parallel training is sub-quadratic in sequence length",
    background=[def_chunkwise, def_la_recurrent_form],
)

claim_deltanet_uses_delta_rule = claim(
    "In Eq. 8 (@def_delta_rule_update) the variables $v_t$, $\\phi(k_t)$, and "
    "$\\sigma(\\beta_t)$ play the roles of *target*, *input*, and *learning rate* "
    "of the classic delta rule [@Widrow1960] respectively, so each step performs "
    "one rank-1 delta-rule update of the fast weight matrix.",
    title="DeltaNet's update is one delta-rule step (target/input/learning rate)",
)

claim_negative_eigvals = claim(
    "Setting $\\sigma$ to twice-sigmoid (giving $\\sigma(\\beta_t) \\in (0, 2)$) "
    "introduces negative eigenvalues in the linear state-transition matrix of the "
    "delta rule, which Grazzi et al. [@Grazzi2025] identify as the key ingredient "
    "enabling DeltaNet's strong state-tracking abilities (e.g., parity).",
    title="Twice-sigmoid $\\sigma$ enables negative eigenvalues -> state tracking",
    background=[def_delta_rule_update],
)

claim_deltanet_choice_for_hybrid = claim(
    "Because DeltaNet is the linear transformer with the strongest demonstrated "
    "state-tracking expressivity among scalable variants, the paper adopts "
    "DeltaNet as the FW-memory component in all HQLT models. The hybrid design "
    "is, however, agnostic to the specific FWP and could be instantiated with "
    "Gated Delta Networks [@Yang2025GatedDelta] or DeltaProduct "
    "[@Siems2025DeltaProduct] without structural changes.",
    title="DeltaNet is chosen as the FW-memory component for HQLTs",
)

# ---------------------------------------------------------------------------
# Reasoning: ground the linear-cost claim from Sec 1 in the recurrent form
# ---------------------------------------------------------------------------

strat_lt_linear_cost_grounded = support(
    [claim_la_constant_per_step],
    claim_lt_linear_cost,
    reason=(
        "The motivation-section claim that LT/FWP has linear-in-$t$ cost and unbounded "
        "context (@claim_lt_linear_cost) is grounded by the per-step constant cost of "
        "the LA recurrent form (@claim_la_constant_per_step): a fixed-size matrix state "
        "with $O(1)$ per-step work directly implies linear total time and unbounded "
        "supported context."
    ),
    prior=0.97,
    background=[def_la_recurrent_form],
)

strat_qt_quadratic_cost_grounded = support(
    [claim_qt_storage_grows],
    claim_qt_quadratic_cost,
    reason=(
        "The motivation-section claim that QT has quadratic cost and bounded context "
        "(@claim_qt_quadratic_cost) is grounded by the linear growth of KV-memory "
        "(@claim_qt_storage_grows): each step does $O(t)$ work against the stored "
        "$K_t, V_t$, and total cost across $T$ steps is $\\sum_{t=1}^{T} O(t) = O(T^2)$. "
        "Practical attention therefore caps $T$ via a sliding window."
    ),
    prior=0.97,
    background=[def_kv_memory_state, def_softmax_attention],
)

# Wire DeltaNet expressivity claim from negative-eigvals + delta-rule identification
strat_deltanet_expressivity_grounded = support(
    [claim_negative_eigvals, claim_deltanet_uses_delta_rule],
    claim_deltanet_expressivity,
    reason=(
        "DeltaNet's state-tracking expressivity (@claim_deltanet_expressivity) "
        "is grounded by two background facts: (1) its update is one delta-rule "
        "step (@claim_deltanet_uses_delta_rule), giving it a non-trivial linear "
        "state-transition operator on $W_t$; and (2) the twice-sigmoid choice of "
        "$\\sigma$ admits negative eigenvalues in that operator "
        "(@claim_negative_eigvals), which Grazzi et al. identify as the key to "
        "parity-style state tracking."
    ),
    prior=0.85,
    background=[def_delta_rule_update],
)

# Wire chunkwise subquadratic into the choice of DeltaNet for the hybrid: chunk-wise
# parallelisability is one of the practical reasons DeltaNet is feasible at scale.
strat_deltanet_choice_grounded = support(
    [claim_deltanet_expressivity, claim_chunkwise_subquadratic],
    claim_deltanet_choice_for_hybrid,
    reason=(
        "The choice of DeltaNet as the FW-memory operator "
        "(@claim_deltanet_choice_for_hybrid) is justified by two properties: "
        "(1) DeltaNet has demonstrated state-tracking expressivity beyond "
        "softmax attention (@claim_deltanet_expressivity), and (2) it admits a "
        "chunk-wise sub-quadratic parallel training algorithm "
        "(@claim_chunkwise_subquadratic), making it a scalable FWP. Both are "
        "necessary for the FW branch of HQLT to be a competitive component."
    ),
    prior=0.9,
    background=[def_la_recurrent_form, def_delta_rule_update],
)


__all__ = [
    "def_kv_memory_state",
    "def_softmax_attention",
    "claim_softmax_sharpness",
    "claim_qt_storage_grows",
    "def_la_recurrent_form",
    "def_no_normalizer",
    "def_chunkwise",
    "def_delta_rule_update",
    "def_phi_choice",
    "claim_la_constant_per_step",
    "claim_chunkwise_subquadratic",
    "claim_deltanet_uses_delta_rule",
    "claim_negative_eigvals",
    "claim_deltanet_choice_for_hybrid",
    "strat_lt_linear_cost_grounded",
    "strat_qt_quadratic_cost_grounded",
    "strat_deltanet_expressivity_grounded",
    "strat_deltanet_choice_grounded",
]
