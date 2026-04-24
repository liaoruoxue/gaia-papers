"""Section 2: Background — TTT Architecture and Prior Work"""

from gaia.lang import claim, setting, support

from .motivation import ttt_definition, linear_attention_definition, memorization_hypothesis

# --- Settings: formal setup ---

inner_loop_setup = setting(
    "In TTT with KV binding, the inner-loop loss is typically a reconstruction objective: "
    "$\\ell_t = \\|f(k_t; W_t) - v_t\\|^2$, where $f(\\cdot; W_t)$ is the model parametrized "
    "by weights $W_t$, $k_t$ is the key at position $t$, and $v_t$ is the target value. "
    "The weights are updated by gradient descent: $W_{t+1} = W_t - \\eta \\nabla_{W_t} \\ell_t$, "
    "where $\\eta$ is the inner-loop learning rate.",
    title="Inner-loop optimization setup",
)

lact_architecture = setting(
    "LaCT (Language Context TTT) uses a SwiGLU MLP as the model $f$ in the inner loop. "
    "The MLP has two linear layers $W_1, W_2$ and applies SwiGLU activations. The inner-loop "
    "loss uses a Frobenius inner product formulation. LaCT is trained on language modeling "
    "tasks with 760M parameters, using FineWeb-Edu data (100B tokens), sequence length 32k, "
    "and evaluated on Book-3 data (2.5B tokens).",
    title="LaCT architecture definition",
)

vitttt_architecture = setting(
    "ViTTT (Vision Transformer with TTT) applies TTT inside a Vision Transformer. It uses "
    "a GLU (gated linear unit) and depthwise convolution as the inner-loop model. "
    "ViTTT-B has 90M parameters and is evaluated on ImageNet-1K image classification.",
    title="ViTTT architecture definition",
)

lact_nvs_architecture = setting(
    "LaCT-NVS applies LaCT to novel view synthesis (NVS). It uses 114M parameters, trained "
    "on RealEstate10K dataset with 2 input views + 6 target views at 128×128 resolution, "
    "MSE loss, and evaluated using PSNR (peak signal-to-noise ratio).",
    title="LaCT-NVS architecture definition",
)

# --- Background claims about prior TTT work ---

claim_ttt_kv_prior_work = claim(
    "Prior work on TTT with KV binding (e.g., Zhang et al. 2025, Han et al. 2025, "
    "Behrouz et al. 2024) consistently adopts the memorization interpretation: the inner "
    "loop writes KV associations into model weights, and inference retrieves them. "
    "This framing drives architectural choices such as multi-step inner loops, momentum, "
    "and weight normalization.",
    title="Prior TTT work adopts memorization framing",
)

claim_linear_attention_prior_work = claim(
    "Linear attention mechanisms (Katharopoulos et al. 2020) and their modern variants "
    "(e.g., Mamba/SSM by Gu & Dao 2024, RWKV by Peng et al. 2024) replace the softmax "
    "in standard attention with feature map dot products, enabling $O(1)$ recurrent inference. "
    "These methods are motivated by efficiency, not by a storage-and-retrieval interpretation.",
    title="Linear attention prior work",
)
