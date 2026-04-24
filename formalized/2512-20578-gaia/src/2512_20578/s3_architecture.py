"""Section 3: Gnosis Architecture"""

from gaia.lang import claim, setting, support, deduction
from .motivation import gnosis_proposal, internal_cues_exist

# ── Settings: Architectural Definitions ───────────────────────────────────────

completeness_token_setting = setting(
    "The completeness token is the final token of the LLM's generated response. "
    "Gnosis extracts the hidden states from ALL transformer layers at the position of "
    "this completeness token, producing a matrix of shape [L, d_model] where L is the "
    "number of transformer layers and d_model is the hidden dimension.",
    title="Completeness token and hidden state extraction",
)

attention_map_setting = setting(
    "Gnosis extracts all attention maps from the completeness token position across all "
    "L layers and H attention heads, yielding L*H attention maps each of shape [1, T] "
    "where T is the sequence length. These are spatially resampled to a fixed grid "
    "(default 256x256) for processing.",
    title="Attention map extraction definition",
)

sab_pma_setting = setting(
    "Set Attention Block (SAB) and Pooling by Multi-head Attention (PMA) are components "
    "from Set Transformer [@Lee2024SAB]. SAB applies self-attention within a set of elements "
    "(permutation-equivariant). PMA uses a fixed set of seed vectors to pool an arbitrary-size "
    "input set into a fixed-size output (permutation-invariant). Together they enable "
    "order-invariant aggregation over variable-length sequences.",
    title="SAB and PMA definitions",
)

axial_conv_setting = setting(
    "Axial convolution applies 1D convolutions separately along each dimension of a 2D feature "
    "map (e.g., along the layer axis and along the head axis), capturing structure within each "
    "dimension while sharing parameters across the other. This is more parameter-efficient than "
    "full 2D convolution.",
    title="Axial convolution definition",
)

# ── Architecture Claims ────────────────────────────────────────────────────────

hidden_circuit_arch = claim(
    "The Hidden Circuit Encoder in Gnosis processes the hidden states matrix [L, d_model] "
    "in two phases: "
    "(1) Local temporal processing — multi-scale temporal convolutions with gating and "
    "squeeze-and-excitation (SE) channel attention extract local patterns across the layer sequence, "
    "with 2.6M total parameters. "
    "(2) Global aggregation — Set Attention Blocks (SAB) followed by Pooling by Multi-head Attention (PMA) "
    "aggregate the sequence into a fixed-size representation, independent of sequence length. "
    "The final hidden circuit output is a fixed-dimensional descriptor regardless of L or T.",
    title="Hidden Circuit Encoder architecture",
    metadata={"source_section": "Section 3.1"},
)

attention_circuit_arch = claim(
    "The Attention Circuit Encoder in Gnosis processes L*H attention maps through two stages: "
    "(1) Per-map feature extraction — each attention map is processed by a hybrid CNN + statistics "
    "extractor that combines learned convolutional features with handcrafted statistics (entropy, "
    "max, variance, etc.), producing a feature vector per map. "
    "(2) Cross-map integration — the resulting [L, H, features] array is processed by axial "
    "convolutions (separate 1D convolutions along layer and head axes) plus layer/head positional "
    "embeddings, then aggregated via PMA to a fixed-size descriptor. "
    "Total parameters: 1.4M.",
    title="Attention Circuit Encoder architecture",
    metadata={"source_section": "Section 3.2"},
)

gated_fusion_arch = claim(
    "A gated MLP fusion head combines the hidden-circuit and attention-circuit fixed-size descriptors "
    "into a scalar correctness probability. The fusion uses a learned gate to weight the relative "
    "contribution of each stream before the final scalar prediction. Total fusion parameters: ~0.5M.",
    title="Gated fusion head architecture",
    metadata={"source_section": "Section 3.3"},
)

total_params = claim(
    "Gnosis totals approximately 5 million parameters: ~2.6M in the Hidden Circuit Encoder, "
    "~1.4M in the Attention Circuit Encoder, and ~0.5M in the gated fusion head. "
    "This is approximately 1,600× smaller than the Skywork-Reward-8B external judge "
    "(8 billion parameters).",
    title="Total Gnosis parameter count",
    metadata={"source_section": "Section 3, Abstract"},
)

constant_latency = claim(
    "Gnosis maintains approximately constant latency (~25ms) regardless of the output "
    "sequence length (tested at 12,000 and 24,000 tokens). This is because PMA-based aggregation "
    "compresses variable-length sequences into fixed-budget descriptors before scoring.",
    title="Constant latency regardless of sequence length",
    metadata={"source_section": "Section 4, Table 4"},
)

frozen_backbone = claim(
    "Gnosis trains only its own ~5M parameters while keeping the LLM backbone completely frozen. "
    "No gradient flows through the backbone during training. The mechanism is thus compatible with "
    "any backbone whose hidden states and attention maps are accessible (i.e., open-weight models).",
    title="Frozen backbone training protocol",
    metadata={"source_section": "Section 3"},
)

training_protocol = claim(
    "Gnosis training uses automatic correctness labels (no human annotation): "
    "(1) Generate 2 completions per math prompt (~14k DAPO-Math competition problems) and "
    "1 completion per trivia prompt (40k subsampled from 118k TriviaQA questions). "
    "(2) Label each completion correct/incorrect by ground-truth comparison. "
    "(3) Optimize binary cross-entropy with frozen backbone for 2 epochs using Adam optimizer "
    "(learning rate 1×10⁻⁴). "
    "Training the largest backbone (OpenAI gpt-oss-20B) costs approximately $25 and takes "
    "~12 hours on 2× A100 80GB GPUs.",
    title="Gnosis training protocol",
    metadata={"source_section": "Section 3.4"},
)

# ── Strategy: Architecture enables constant latency ───────────────────────────

strat_pma_enables_constant = deduction(
    [hidden_circuit_arch, attention_circuit_arch],
    constant_latency,
    reason=(
        "Both the Hidden Circuit Encoder (@hidden_circuit_arch) and Attention Circuit Encoder "
        "(@attention_circuit_arch) terminate with PMA (Pooling by Multi-head Attention), "
        "which maps variable-length inputs to a fixed number of seed vectors. "
        "Since the downstream scoring operates on fixed-size descriptors, the computation time "
        "does not grow with sequence length T, yielding constant latency."
    ),
    prior=0.97,
)

strat_params_sum = deduction(
    [hidden_circuit_arch, attention_circuit_arch, gated_fusion_arch],
    total_params,
    reason=(
        "The total parameter count is the sum of the three components: "
        "Hidden Circuit (@hidden_circuit_arch) 2.6M + "
        "Attention Circuit (@attention_circuit_arch) 1.4M + "
        "Gated Fusion Head (@gated_fusion_arch) 0.5M = ~5M total, "
        "as stated in @total_params."
    ),
    prior=0.99,
)

strat_training_no_annotation = support(
    [training_protocol],
    frozen_backbone,
    reason=(
        "The training protocol (@training_protocol) generates correctness labels automatically "
        "from ground-truth comparison, requiring no human annotation. This is consistent with "
        "the frozen backbone design (@frozen_backbone): since backbone weights are not updated, "
        "no backbone-level gradient computation is needed, enabling training to focus entirely "
        "on the lightweight Gnosis head."
    ),
    prior=0.92,
)
