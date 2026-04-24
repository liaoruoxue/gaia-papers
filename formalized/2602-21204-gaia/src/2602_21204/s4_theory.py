"""Section 4-5: Theoretical Analysis — TTT as Linear Attention"""

from gaia.lang import claim, setting, deduction, support, composite

from .motivation import (
    ttt_definition, linear_attention_definition,
    claim_ttt_is_linear_attention, claim_linear_view_explains_paradoxes,
)
from .s2_background import inner_loop_setup, lact_architecture, vitttt_architecture

# --- Settings: Mathematical prerequisites ---

linear_bias_free_assumption = setting(
    "Theorems 5.1-5.3 assume the TTT model's final layer is linear and bias-free: "
    "$f(x; W) = Wx$ where $W$ is the weight matrix of the final layer. This assumption "
    "is satisfied by LaCT and ViTTT when they are configured with linear final-layer "
    "projections (e.g., updating only $W_1$ in the MLP, with $W_2$ fixed and linear).",
    title="Linear bias-free final layer assumption",
)

gradient_computation_setup = setting(
    "For the inner-loop loss $\\ell_t = \\|f(k_t; W_t) - v_t\\|^2$ with $f(x; W) = Wx$, "
    "the gradient of the loss with respect to the final-layer weight $W$ is: "
    "$\\nabla_W \\ell_t = (W_t k_t - v_t) k_t^T$. The effective value vector is defined as "
    "$g_t(k_t) = v_t - W_t k_t$ (negative gradient direction). After one gradient descent "
    "step with learning rate $\\eta$: $W_{t+1} = W_t + \\eta \\phi_t(k_t)^T g_t(k_t)$ "
    "(using feature-mapped keys $\\phi_t(k_t)$).",
    title="Gradient and effective value vector definition",
)

momentum_definition = setting(
    "Gradient descent with momentum updates: $m_t = \\beta m_{t-1} + g_t(k_t)$ where "
    "$\\beta \\in [0,1)$ is the momentum coefficient and $m_t$ is the accumulated momentum "
    "vector. The weight update uses momentum: $W_{t+1} = W_t + \\eta \\phi_t(k_t)^T m_t$.",
    title="Momentum update rule definition",
)

feature_map_notation = setting(
    "The notation $\\phi_t(\\cdot)$ refers to the feature map applied at step $t$, which "
    "may depend on the current model weights $W_t$ (making it a dynamic/history-dependent "
    "kernel). The notation $\\phi_{t+1}(q_t)$ refers to the feature map applied to the "
    "query using the updated weights $W_{t+1}$, reflecting the 'predict after update' "
    "forward pass order in TTT.",
    title="Dynamic feature map notation",
)

# --- Theorem 5.1: Single-step linearization ---

thm_single_step = claim(
    "Theorem 5.1 (Linearization): For a TTT model with a linear, bias-free final layer, "
    "one gradient descent step on the inner-loop loss $\\ell_t = \\|f(k_t; W_t) - v_t\\|^2$ "
    "yields an output of the form: "
    "$$o_t = \\phi_{t+1}(q_t)(W_t + \\phi_t(k_t)^T g_t(k_t))$$"
    "where $g_t(k_t) = v_t - W_t k_t$ is the effective value vector, and $W_t$ is the "
    "accumulated state matrix. This matches the linear attention form "
    "$o_t = \\phi_{t+1}(q_t) S_t$ with $S_t = W_t + \\phi_t(k_t)^T g_t(k_t)$.",
    title="Theorem 5.1: Single gradient step → linear attention",
)

# Theorem 5.1 is proven by algebraic derivation from definitions in the paper.
# Since all premises are settings (mathematical definitions), it is modeled as an
# independent claim. Its prior is set in priors.py.

# --- Theorem 5.2: Multi-step unrolling ---

thm_unrolled = claim(
    "Theorem 5.2 (Unrolling): Sequential application of single gradient descent steps "
    "across a sequence of $T$ tokens yields: "
    "$$o_t = \\phi_{t+1}(q_t)\\left(S_0 + \\sum_{i=1}^{t} \\phi_i(k_i)^T g_i(k_i)\\right)$$"
    "where $S_0 = W_0$ is the initial weight matrix. This is the standard recurrent linear "
    "attention formula accumulated over the full context history up to position $t$.",
    title="Theorem 5.2: Unrolled multi-step → full linear attention",
)

strat_thm52 = deduction(
    [thm_single_step],
    thm_unrolled,
    reason=(
        "Theorem 5.2 follows from Theorem 5.1 (@thm_single_step) by induction over sequence "
        "positions $t = 1, \\ldots, T$. At each step, the accumulated state "
        "$S_t = S_{t-1} + \\phi_t(k_t)^T g_t(k_t)$ is updated by one linear attention "
        "increment. Substituting into the forward pass gives the sum form. "
        "The derivation is a direct telescoping of the recurrence, requiring no additional "
        "assumptions beyond Theorem 5.1."
    ),
    prior=0.99,
    background=[linear_bias_free_assumption, linear_attention_definition],
)

# --- Theorem 5.3: Momentum preserves linear attention ---

thm_momentum = claim(
    "Theorem 5.3 (Momentum): Gradient descent with momentum coefficient $\\beta$ in the "
    "inner loop maintains the linear attention structure, with momentum-weighted effective "
    "value vectors: "
    "$$o_t = \\phi_{t+1}(q_t)\\left(S_0 + \\sum_{i=1}^{t} \\phi_i(k_i)^T \\hat{v}_i\\right)$$"
    "where $\\hat{v}_i = g_i(k_i) \\cdot \\sum_{j=i}^{t} \\beta^{j-i}$ is the momentum-weighted "
    "effective value. The momentum coefficient introduces temporal weighting but does not "
    "break the linear attention form.",
    title="Theorem 5.3: Momentum → temporally-weighted linear attention",
)

strat_thm53 = deduction(
    [thm_unrolled],
    thm_momentum,
    reason=(
        "Starting from Theorem 5.2 (@thm_unrolled), incorporating the momentum update rule "
        "(momentum: $m_t = \\beta m_{t-1} + g_t(k_t)$) replaces each $g_i(k_i)$ with the "
        "accumulated momentum $m_i = \\sum_{j=1}^{i} \\beta^{i-j} g_j(k_j)$. Expanding this "
        "sum and reordering the double summation shows that each $g_i(k_i)$ contributes with "
        "weight $\\hat{v}_i = g_i(k_i) \\cdot \\sum_{j=i}^{t} \\beta^{j-i}$, which is absorbed "
        "into the effective value vector. The outer linear attention structure "
        "$o_t = \\phi_{t+1}(q_t) S_t$ is preserved. The derivation is algebraic."
    ),
    prior=0.99,
    background=[momentum_definition, linear_bias_free_assumption],
)

# --- Concrete reduction: LaCT ---

claim_lact_reduction = claim(
    "LaCT's SwiGLU MLP inner loop reduces to linear attention. The final output is: "
    "$$o_t = \\phi_{t+1}(q_t)\\left(W_{1,0} + \\sum_{i=1}^{t} M(\\phi_i(k_i)^T m_i)\\right)$$"
    "where $W_{1,0}$ is the initial first-layer weight, $M(\\cdot)$ applies gradient "
    "orthogonalization, and $m_i$ incorporates momentum-weighted effective values derived "
    "from the SwiGLU activations. The SwiGLU nonlinearity in intermediate layers is "
    "absorbed into the effective value vectors $m_i$.",
    title="LaCT SwiGLU MLP reduces to linear attention",
)

strat_lact_reduction = support(
    [thm_momentum],
    claim_lact_reduction,
    reason=(
        "Applying Theorem 5.3 (@thm_momentum) to the LaCT architecture (LaCT uses a SwiGLU "
        "MLP with a linear bias-free final layer $W_1$ updated during the inner loop, and a "
        "fixed second layer $W_2$): The SwiGLU activation is absorbed into the computation of "
        "effective value vectors $g_i(k_i)$, which are then accumulated with momentum into "
        "$m_i$. Gradient orthogonalization (operator $M$) is a linear transformation on the "
        "outer product $\\phi_i(k_i)^T m_i$, preserving the linear attention form. The "
        "derivation follows the same algebraic structure as Theorem 5.3 but requires carefully "
        "tracking the SwiGLU output through the gradient computation, introducing the "
        "$M(\\cdot)$ operator."
    ),
    prior=0.88,
    background=[linear_bias_free_assumption, momentum_definition, lact_architecture],
)

# --- Concrete reduction: ViTTT ---

claim_vitttt_glu_reduction = claim(
    "The GLU (gated linear unit) component of ViTTT reduces to a linear attention form: "
    "$$\\phi_{t+1}(q_t) \\odot \\left(q_t(W_1 + k_t^T(v_t \\odot \\phi_t(k_t)))\\right)$$"
    "where $\\odot$ denotes element-wise multiplication. The gating in GLU is absorbed "
    "into the feature map $\\phi_{t+1}(q_t)$ applied to the query.",
    title="ViTTT GLU component reduces to linear attention",
)

claim_vitttt_conv_reduction = claim(
    "The depthwise convolution component of ViTTT admits a sliding-window linear attention "
    "interpretation, where the convolution kernel defines a local attention window and the "
    "channel-wise depthwise operation corresponds to independent per-channel linear attention.",
    title="ViTTT depthwise convolution reduces to sliding-window linear attention",
)

strat_vitttt_glu = support(
    [thm_single_step],
    claim_vitttt_glu_reduction,
    reason=(
        "The GLU in ViTTT applies an element-wise gate: output = $\\sigma(Wq) \\odot Vq$ for "
        "some projections. Following Theorem 5.1 (@thm_single_step) applied to the linear "
        "final layer in ViTTT (ViTTT-B: 90M parameter Vision Transformer using GLU and "
        "depthwise convolution in the inner loop), the gradient update writes the effective "
        "KV outer product into the weight, and the GLU gate $\\sigma(Wq)$ is reinterpreted "
        "as the feature map $\\phi_{t+1}(q_t)$. This gives the stated linear attention form. "
        "The derivation requires identifying the correct feature map that absorbs the GLU gating."
    ),
    prior=0.82,
    background=[linear_bias_free_assumption, vitttt_architecture],
)

strat_vitttt_conv = support(
    [thm_single_step],
    claim_vitttt_conv_reduction,
    reason=(
        "Depthwise convolution in ViTTT (90M parameter model, ImageNet-1K) operates "
        "independently per channel with a local kernel. Following Theorem 5.1 "
        "(@thm_single_step), each channel's convolution within a sliding window can be "
        "rewritten as a query-key-value attention computation restricted to a local "
        "neighborhood. The sliding window corresponds to the attention span, and the "
        "depthwise independence corresponds to per-channel linear attention. The reduction "
        "requires viewing the convolution weights as the accumulated state $S_t$ and the "
        "input features as keys/values."
    ),
    prior=0.78,
    background=[linear_bias_free_assumption, vitttt_architecture],
)

# --- High-level thesis derivation ---

strat_ttt_is_linear_attn = support(
    [thm_unrolled, thm_momentum, claim_lact_reduction, claim_vitttt_glu_reduction,
     claim_vitttt_conv_reduction],
    claim_ttt_is_linear_attention,
    reason=(
        "The three theorems (@thm_unrolled, @thm_momentum) establish that any TTT model with "
        "a linear bias-free final layer and gradient descent (with or without momentum) is "
        "equivalent to a linear attention operator. The concrete reductions of LaCT "
        "(@claim_lact_reduction) and ViTTT (@claim_vitttt_glu_reduction, "
        "@claim_vitttt_conv_reduction) demonstrate this equivalence holds for the specific "
        "architectures studied. Together, these results support the claim that a broad class "
        "of TTT architectures can be expressed as learned linear attention."
    ),
    prior=0.9,
    background=[linear_bias_free_assumption, ttt_definition, linear_attention_definition],
)

# --- Explanation of paradoxes ---

claim_more_steps_mismatch = claim(
    "Under the linear attention interpretation, increasing inner-loop gradient descent "
    "steps changes the effective kernel function $\\phi_t(\\cdot)$ applied to keys "
    "(since $\\phi_t$ depends on $W_t$ which changes with each step). At test time, "
    "the kernel used for queries differs from the kernel used during training (when "
    "fewer steps may have been applied), causing train-test kernel mismatch that "
    "degrades performance.",
    title="More inner-loop steps cause train-test kernel mismatch",
)

claim_gradient_sign_absorbed = claim(
    "Under the linear attention interpretation, flipping the sign of the gradient "
    "(gradient ascent) changes the sign of the effective value vectors "
    "$g_t(k_t) = -(v_t - W_t k_t)$ rather than $(v_t - W_t k_t)$. Since the learned "
    "projections $W_1, W_2$ can adapt to account for this sign flip during training, "
    "the model can compensate via learned parameters, explaining why gradient ascent "
    "performs comparably.",
    title="Gradient sign flip absorbed into learned projections",
)

strat_explain_paradoxes = support(
    [claim_more_steps_mismatch, claim_gradient_sign_absorbed, thm_unrolled],
    claim_linear_view_explains_paradoxes,
    reason=(
        "The linear attention interpretation (@thm_unrolled) provides mechanistic explanations "
        "for the empirical paradoxes. More inner-loop steps cause train-test kernel mismatch "
        "(@claim_more_steps_mismatch) rather than improved memorization, explaining the "
        "inverse performance relationship. Gradient sign flips are absorbed into learned "
        "projections (@claim_gradient_sign_absorbed), explaining gradient ascent equivalence. "
        "Q-K distributional asymmetry is expected because queries and keys serve different "
        "roles in linear attention (query: projection direction; key: state accumulation). "
        "Query substitution tolerance reflects that the feature maps at different steps "
        "($\\phi_{t+1}(k)$ vs. $\\phi_t(k)$) remain functionally distinct despite using "
        "the same input values."
    ),
    prior=0.85,
    background=[ttt_definition, linear_attention_definition],
)
