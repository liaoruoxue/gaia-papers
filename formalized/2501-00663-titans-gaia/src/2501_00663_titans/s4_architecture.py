"""Section 4: Titans Architecture Variants — How to Incorporate Memory"""

from gaia.lang import claim, setting, support, deduction, contradiction

from .motivation import (
    transformer_short_term_memory,
    seq_modeling_setup,
    attention_definition,
    deep_memory_expressiveness,
)
from .s3_neural_memory import (
    forgetting_mechanism_claim,
    persistent_memory_claim,
    parallel_training_claim,
    assoc_memory_loss_def,
    memory_update_rule_def,
    memory_retrieval_def,
)

# ── Settings ──────────────────────────────────────────────────────────────────

mac_architecture_def = claim(
    "The Memory as a Context (MAC) architecture processes input $x \\in \\mathbb{R}^{N \\times d_{\\text{in}}}$ "
    "in segments $S^{(i)}$ of fixed size $C$. For each segment $S^{(t)}$, the model:\n"
    "1. Retrieves long-term memory: $h_t = \\mathcal{M}^*_{t-1}(q_t)$, where $q_t = S^{(t)} W_Q$\n"
    "2. Concatenates persistent memory, retrieved history, and current segment: "
    "$\\tilde{S}^{(t)} = [p_1, \\ldots, p_{N_p}] \\,\\|\\, h_t \\,\\|\\, S^{(t)}$\n"
    "3. Applies full causal attention: $y_t = \\text{Attn}(\\tilde{S}^{(t)})$\n"
    "4. Updates memory: $\\mathcal{M}_t = \\mathcal{M}_{t-1}(y_t)$; "
    "produces output: $o_t = y_t \\otimes \\mathcal{M}^*_t(y_t)$ [@Behrouz2025].",
    title="MAC architecture specification",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4.1, Fig. 2"},
)

mag_architecture_def = claim(
    "The Memory as a Gate (MAG) architecture uses two parallel branches without chunking:\n"
    "1. $\\tilde{x} = [p_1, \\ldots, p_{N_p}] \\,\\|\\, x$ (prepend persistent memory)\n"
    "2. Core branch: $y = \\text{SW-Attn}^*(\\tilde{x})$ (sliding window attention with prefix)\n"
    "3. Memory branch: $\\mathcal{M}(\\tilde{x})$ (neural memory processes entire sequence)\n"
    "4. Gated combination: $o = y \\otimes \\mathcal{M}(\\tilde{x})$ "
    "where $\\otimes$ is a learned non-linear gating with normalization and $\\sigma(\\cdot)$ [@Behrouz2025].",
    title="MAG architecture specification",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4.2, Fig. 4"},
)

mal_architecture_def = claim(
    "The Memory as a Layer (MAL) architecture arranges neural memory and attention sequentially:\n"
    "1. $\\tilde{x} = [p_1, \\ldots, p_{N_p}] \\,\\|\\, x$\n"
    "2. Memory layer: $y = \\mathcal{M}(\\tilde{x})$\n"
    "3. Attention layer: $o = \\text{SW-Attn}(y)$ (sliding window attention)\n\n"
    "This is the most common hybrid architecture design in the literature "
    "(e.g., Samba, Griffin, H3). The memory layer compresses past and current context before attention [@Behrouz2025].",
    title="MAL architecture specification",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4.3, Fig. 5"},
)

# ── Claims ────────────────────────────────────────────────────────────────────

titans_three_memory_types = claim(
    "The Titans family of architectures organizes memory into three types:\n\n"
    "| Memory Type | Component | Behavior at Test Time |\n"
    "|-------------|-----------|----------------------|\n"
    "| Short-term | Attention (full or sliding-window) | In-context learner, weights fixed |\n"
    "| Long-term (contextual) | Neural memory module $\\mathcal{M}$ | Continues learning/updating weights |\n"
    "| Persistent (task) | Learnable data-independent params $P$ | Fixed; encodes task knowledge |\n\n"
    "The three types operate jointly yet each can function independently [@Behrouz2025].",
    title="Titans three-type memory taxonomy",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4"},
)

mac_advantages = claim(
    "The MAC (Memory as a Context) architecture has two key advantages over MAG and MAL:\n"
    "(1) Attention has access to both historical context (retrieved from long-term memory) and "
    "current context, enabling the model to decide dynamically whether long-term memory information "
    "is relevant. (2) The attention module guides the long-term memory to store only useful "
    "information from the current segment, preventing memory overflow from uninformative tokens. "
    "At test time, only long-term memory weights update; attention weights perform in-context learning; "
    "persistent memory is fixed [@Behrouz2025].",
    title="MAC architecture design advantages",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4.1"},
)

mal_limitation = claim(
    "The MAL (Memory as a Layer) architecture has a key drawback: because memory and attention "
    "are applied sequentially (memory first, then attention), neither module can exploit the "
    "complementary information processing of the other during the same pass. The power of the "
    "overall model is limited by the weakest component in the sequential chain. "
    "MAG and MAC, by contrast, allow parallel/joint processing of short- and long-term memory [@Behrouz2025].",
    title="MAL architecture sequential limitation",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4.3"},
)

titans_expressiveness_theorem = claim(
    "**Theorem 4.1 (Titans Expressiveness):** Contrary to Transformers, diagonal linear recurrent models, "
    "and DeltaNet—all of which are limited to the circuit complexity class TC$^0$ [@Merrill2024]—Titans "
    "are capable of solving problems beyond TC$^0$. This means Titans are theoretically more expressive "
    "than Transformers and most modern linear recurrent models in state tracking tasks [@Behrouz2025].",
    title="Titans expressiveness beyond TC0",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 4.4"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_three_memory_from_design = deduction(
    [mac_architecture_def, mag_architecture_def, mal_architecture_def, persistent_memory_claim],
    titans_three_memory_types,
    reason=(
        "By the definitions of MAC (@mac_architecture_def), MAG (@mag_architecture_def), and "
        "MAL (@mal_architecture_def), all Titans variants include: (1) attention (sliding-window "
        "or full) as the short-term in-context module; (2) the neural long-term memory $\\mathcal{M}$ "
        "that continues learning at test time; (3) persistent memory tokens $P$ "
        "(@persistent_memory_claim) that are fixed at test time. The taxonomy follows directly "
        "from these architectural definitions."
    ),
    prior=0.99,
)

strat_mac_advantages_from_design = deduction(
    [mac_architecture_def, transformer_short_term_memory],
    mac_advantages,
    reason=(
        "In MAC (@mac_architecture_def), retrieved long-term memory $h_t$ is concatenated with "
        "current segment $S^{(t)}$ before applying full attention. This gives attention access to "
        "both past (@transformer_short_term_memory models current context) and future-relevant "
        "historical context — enabling the attention to gate how much weight to give long-term "
        "memory. Further, attention output $y_t$ drives the memory update, meaning only "
        "attention-selected useful information gets memorized."
    ),
    prior=0.95,
)

strat_mal_limitation_from_design = deduction(
    [mal_architecture_def],
    mal_limitation,
    reason=(
        "In MAL (@mal_architecture_def), memory produces output $y = \\mathcal{M}(\\tilde{x})$, "
        "which is then processed by attention. The memory module has no access to attention "
        "outputs, and attention has no access to the raw input (only memory's output). "
        "Neither module can benefit from the other's processing in the same forward pass. "
        "This is in contrast to MAC (where attention sees memory outputs and vice versa) "
        "and MAG (where both branches run in parallel on the same input)."
    ),
    prior=0.95,
)

# Contradiction: MAC and MAL represent genuinely different tradeoffs
mac_vs_mal_tradeoff = contradiction(
    mac_advantages,
    mal_limitation,
    reason="MAC and MAL represent incompatible design choices: MAC's full-context attention is more powerful but computationally heavier; MAL's sequential design is more efficient but lacks cross-module information flow.",
    prior=0.85,
)
