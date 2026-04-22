"""Introduction and Motivation: Memory Limitations of Existing Architectures"""

from gaia.lang import claim, setting, question

# ── Settings: formal definitions and established background ──────────────────

seq_modeling_setup = setting(
    "Let the input be $x \\in \\mathbb{R}^{N \\times d_{\\text{in}}}$ where $N$ is the sequence length "
    "and $d_{\\text{in}}$ is the model dimension. A sequence model maps $x$ to an output $y$ of the same shape.",
    title="Sequence modeling setup",
)

attention_definition = setting(
    "Causal (softmax) attention, as used in Transformers [@Vaswani2017], computes output $y_i$ as a "
    "softmax-weighted sum of value vectors:\n\n"
    "$$y_i = \\sum_{j=1}^{i} \\frac{\\exp(Q_i^\\top K_j / \\sqrt{d_{\\text{in}}}) V_j}"
    "{\\sum_{\\ell=1}^{i} \\exp(Q_i^\\top K_\\ell / \\sqrt{d_{\\text{in}}})}$$\n\n"
    "where $Q = xW_Q$, $K = xW_K$, $V = xW_V$ are query, key, and value projections with learnable "
    "weight matrices $W_Q, W_K, W_V \\in \\mathbb{R}^{d_{\\text{in}} \\times d_{\\text{in}}}$.",
    title="Causal attention definition",
)

linear_attention_definition = setting(
    "Linear attention replaces the softmax kernel in standard attention with a factorized kernel "
    "$\\phi(x, y) = \\phi(x)\\phi(y)$, yielding:\n\n"
    "$$y_i = \\frac{\\phi(Q_i)^\\top \\sum_{j=1}^{i} \\phi(K_j) V_j}"
    "{\\phi(Q_i)^\\top \\sum_{\\ell=1}^{i} \\phi(K_\\ell)}$$\n\n"
    "When the identity kernel is used, this reduces to a recurrent form: "
    "$M_t = M_{t-1} + K_t^\\top V_t$, $y_t = Q_t M_t$, "
    "where $M_t \\in \\mathbb{R}^{d_{\\text{in}} \\times d_{\\text{in}}}$ is a matrix-valued memory state [@Katharopoulos2020].",
    title="Linear attention definition",
)

rnn_memory_definition = setting(
    "A recurrent neural network (RNN) can be defined via two operations on a memory unit "
    "$M \\in \\mathbb{R}^d$:\n\n"
    "- **Write**: $M_t = f(M_{t-1}, x_t)$ (update memory with new input)\n"
    "- **Read**: $y_t = g(M_t, x_t)$ (retrieve output from memory)\n\n"
    "where subscript $t$ denotes the state at time step $t$ [@Vaswani2017].",
    title="RNN as memory read/write system",
)

neuropsych_memory_definition = setting(
    "In neuropsychology, memory is defined as a confederation of distinct systems—"
    "including short-term, working, and long-term memory—each serving different functions "
    "with different neural structures, and each capable of operating independently [@Cowan2008].",
    title="Human memory systems definition",
)

# ── Research questions ───────────────────────────────────────────────────────

q_memory_structure = question(
    "(Q1) What constitutes a good structure for the memory module in a sequence model?",
    title="Q1: Memory structure",
)

q_memory_update = question(
    "(Q2) What is a proper memory update mechanism for a neural sequence model?",
    title="Q2: Memory update",
)

q_memory_retrieval = question(
    "(Q3) What is a good memory retrieval process for a neural sequence model?",
    title="Q3: Memory retrieval",
)

q_modular_memory = question(
    "(Q4) How to design an efficient architecture that incorporates different interconnected "
    "memory modules, analogous to the distinct yet connected memory systems in the human brain?",
    title="Q4: Modular memory architecture",
)

q_deep_memory = question(
    "(Q5) Is a deep memory module needed to effectively store and remember long past history, "
    "given that a single vector or matrix encoding data linearly may be insufficient?",
    title="Q5: Deep memory necessity",
)

# ── Claims from Introduction ─────────────────────────────────────────────────

transformer_quadratic_cost = claim(
    "Standard (softmax) attention in Transformers [@Vaswani2017] requires $O(N^2)$ time and memory "
    "with respect to context length $N$, because computing pairwise similarities between all queries "
    "and keys requires at least $N \\times d_{\\text{in}}$ operations. This quadratic complexity makes "
    "Transformers impractical for very long sequences (e.g., context windows of millions of tokens).",
    title="Transformer quadratic complexity",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 1"},
)

transformer_short_term_memory = claim(
    "Attention in Transformers functions as a short-term memory: it accurately models dependencies "
    "among all tokens within the current context window by storing all key-value pairs without "
    "compression, but is limited to a fixed-length context window due to quadratic complexity. "
    "The output of a Transformer is exclusively conditioned on tokens in the current context window [@Vaswani2017].",
    title="Attention as short-term memory",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 1"},
)

linear_recurrent_compression_problem = claim(
    "Linear Transformers and linear recurrent models (including state space models) exhibit a "
    "fundamental contradiction: they are designed to scale to long contexts via linear complexity, "
    "but their matrix-valued hidden state $M_t \\in \\mathbb{R}^{d \\times d}$ is too small to "
    "faithfully compress very long context information. As sequence length grows, the additive memory "
    "update rule causes memory overflow, significantly damaging model performance [@Katharopoulos2020].",
    title="Linear recurrent compression contradiction",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 1"},
)

existing_architectures_missing_components = claim(
    "Existing architectures—ranging from Hopfield Networks to LSTMs and Transformers—each miss "
    "one or more of the following crucial components of effective learning: (1) distinct memory "
    "systems (short-term, long-term, meta-memory); (2) interconnected yet independently operable "
    "modules; (3) the ability to actively learn and memorize the abstraction of past history at "
    "test time. None of these architectures fully incorporate all aspects of human-brain-like "
    "memory systems [@Cowan2008].",
    title="Missing memory components in existing architectures",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 1"},
)

attention_as_associative_memory = claim(
    "Attention modules in Transformers function as associative memory blocks: they store key-value "
    "associations and retrieve information by computing pairwise similarity between queries (search "
    "signals) and keys (stored contexts). The key-value matrices together constitute the model's "
    "memory, which grows by appending new entries without compression [@Vaswani2017].",
    title="Attention as associative memory block",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 2"},
)

linear_transformer_matrix_memory = claim(
    "Linear Transformers compress historical key-value pairs additively into a fixed-size "
    "matrix-valued memory state $M_t \\in \\mathbb{R}^{d_{\\text{in}} \\times d_{\\text{in}}}$, "
    "whereas linear RNNs (including state space models) use vector-valued memory states. "
    "The memory update is: $M_t = M_{t-1} + K_t^\\top V_t$, which is an online linear regression "
    "objective—this means the optimal solution assumes linear dependencies in historical data [@Katharopoulos2020].",
    title="Linear Transformer matrix-valued memory",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 2"},
)

deep_memory_expressiveness = claim(
    "Deep memory modules with $L_{\\mathcal{M}} \\geq 2$ layers are strictly more expressive than "
    "linear (matrix-valued) memory modules: matrix-valued memory $M = W \\in \\mathbb{R}^{d \\times d}$ "
    "is equivalent to optimizing an online linear regression objective "
    "$\\ell(W_{t-1}; x_t) = \\|W_{t-1} k_t - v_t\\|_2^2$, whose optimal solution assumes linear "
    "dependencies in historical data. Multi-layer perceptrons (MLPs) with at least two layers are "
    "universal approximators and can represent non-linear dependencies [@Hornik1989].",
    title="Deep memory modules more expressive than linear memory",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1"},
)
