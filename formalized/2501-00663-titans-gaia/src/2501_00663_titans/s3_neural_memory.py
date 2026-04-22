"""Section 3: Learning to Memorize at Test Time — Neural Long-Term Memory Module"""

from gaia.lang import claim, setting, support, deduction, compare, abduction

from .motivation import (
    attention_definition,
    rnn_memory_definition,
    neuropsych_memory_definition,
    deep_memory_expressiveness,
    linear_transformer_matrix_memory,
    q_deep_memory,
)

# ── Settings ─────────────────────────────────────────────────────────────────

assoc_memory_loss_def = setting(
    "The associative memory loss for the neural long-term memory module $\\mathcal{M}$ is defined as:\n\n"
    "$$\\ell(\\mathcal{M}_{t-1}; x_t) = \\|\\mathcal{M}_{t-1}(k_t) - v_t\\|_2^2$$\n\n"
    "where $k_t = x_t W_K$ and $v_t = x_t W_V$ are key and value projections "
    "($W_K, W_V \\in \\mathbb{R}^{d_{\\text{in}} \\times d_{\\text{in}}}$) of the current token $x_t$. "
    "Minimizing this loss trains $\\mathcal{M}$ to associate keys with values [@Behrouz2025].",
    title="Associative memory loss definition",
)

memory_update_rule_def = setting(
    "The full neural memory update rule with momentum and weight decay is:\n\n"
    "$$\\mathcal{M}_t = (1 - \\alpha_t) \\mathcal{M}_{t-1} + S_t$$\n"
    "$$S_t = \\eta_t S_{t-1} - \\theta_t \\nabla \\ell(\\mathcal{M}_{t-1}; x_t)$$\n\n"
    "where: $\\alpha_t \\in [0, 1]$ is the data-dependent forgetting gate (weight decay), "
    "$\\eta_t$ is the data-dependent surprise decay controlling momentum, "
    "$\\theta_t$ controls how much momentary surprise is incorporated, "
    "and $S_t$ is the momentum (accumulated past surprise) [@Behrouz2025].",
    title="Full memory update rule with momentum and weight decay",
)

memory_retrieval_def = setting(
    "Memory retrieval is performed via a forward pass without weight update: "
    "given input $x_t$, a query $q_t = x_t W_Q$ is computed, and the retrieved memory is:\n\n"
    "$$y_t = \\mathcal{M}^*(q_t)$$\n\n"
    "where $\\mathcal{M}^*(\\cdot)$ denotes inference (forward pass) without weight adjustment [@Behrouz2025].",
    title="Memory retrieval via forward pass",
)

parallel_training_setup = setting(
    "The parallel training algorithm for the neural memory module splits the input sequence "
    "into chunks of size $b \\geq 1$. Within each chunk, all gradients $u_t = \\nabla \\ell(\\mathcal{M}_{t'}; x_t)$ "
    "can be computed simultaneously. The momentum recurrence $S_t = \\eta_t S_{t-1} - \\theta_t u_t$ "
    "is a linear recurrence with $u_t$ as input, enabling parallel associative scan [@SmithWarrington2023].",
    title="Parallel training via chunked associative scan",
)

# ── Claims ────────────────────────────────────────────────────────────────────

surprise_as_gradient = claim(
    "The surprise of a token $x_t$ to the neural memory module can be quantified as the gradient "
    "$\\nabla \\ell(\\mathcal{M}_{t-1}; x_t)$ of the associative memory loss with respect to $x_t$: "
    "the larger the gradient, the more different $x_t$ is from past data stored in $\\mathcal{M}$. "
    "This operationalizes the psychological insight that surprising events are more memorable [@Mandler2014].",
    title="Gradient as surprise metric",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1"},
)

momentum_motivation = claim(
    "A purely momentary surprise metric (gradient at step $t$ only) can cause the model to miss "
    "important information following a highly surprising event, because subsequent gradients become "
    "very small after a large surprise step (the model stagnates in a flat loss region). "
    "Incorporating momentum (past accumulated surprise $S_{t-1}$) addresses this: an initially "
    "surprising event keeps affecting memory updates over subsequent tokens, analogous to how humans "
    "continue processing a memorable event over a span of time [@Behrouz2025].",
    title="Momentum in surprise metric motivation",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1"},
)

forgetting_mechanism_claim = claim(
    "The weight decay term $(1 - \\alpha_t)$ in the memory update rule $\\mathcal{M}_t = (1 - \\alpha_t)\\mathcal{M}_{t-1} + S_t$ "
    "implements an adaptive forgetting gate: when $\\alpha_t \\to 0$, past memory is preserved; "
    "when $\\alpha_t \\to 1$, the entire memory is cleared. This data-dependent mechanism enables "
    "the model to manage limited memory capacity by selectively forgetting irrelevant past "
    "information when context changes [@Behrouz2025].",
    title="Adaptive forgetting mechanism via weight decay",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1"},
)

forgetting_generalizes_rnn_gates = claim(
    "The weight decay forgetting mechanism in the neural long-term memory module is a generalization "
    "of the gating mechanisms in modern linear recurrent models. Specifically, setting the momentum "
    "coefficient $\\eta_t = 0$ in the LMM update rule recovers the Gated DeltaNet update, "
    "and further simplifications recover Mamba2 and other gated linear recurrent models "
    "(Mamba [@GuDao2024], Mamba2 [@DaoGu2024], Gated DeltaNet [@YangGatedDelta2024]). "
    "LMM generalizes these by adding (1) momentum-based surprise accumulation, (2) deep non-linear "
    "memory, and (3) inter-chunk non-linear recurrence.",
    title="LMM forgetting gate generalizes modern RNN gates",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1, Appendix C"},
)

parallel_training_claim = claim(
    "The neural long-term memory training algorithm is parallelizable and uses only matrix "
    "multiplications (matmuls) plus summation. The key insight is that with mini-batch gradient "
    "descent with chunk size $b$, the weight update within a chunk can be written as "
    "$\\Theta_b \\mathbf{B}_b (W_0 X - X) X^\\top$ using only matmuls, where $\\Theta_b$ and "
    "$\\mathbf{B}_b$ are diagonal matrices of learning rates and decay products. "
    "The momentum recurrence $S_t = \\eta_t S_{t-1} - \\theta_t u_t$ is computed in parallel "
    "via parallel associative scan [@SmithWarrington2023], achieving $O(N)$ FLOPs overall [@Behrouz2025].",
    title="Parallelizable training via matmuls and associative scan",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.2, Fig. 1"},
)

online_meta_learning_equivalence = claim(
    "Training the neural long-term memory module $\\mathcal{M}$ is equivalent to meta-learning: "
    "the memory module serves as the inner-loop learner (its weights $\\mathcal{M}$ are updated "
    "via gradient descent on the associative memory loss), while the projection matrices $W_K, W_V$ "
    "are hyperparameters of the inner loop optimized in the outer loop along with the rest of the "
    "architecture. This is analogous to MAML-style meta-learning [@Behrouz2025].",
    title="Memory training as meta-learning inner loop",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1"},
)

persistent_memory_claim = claim(
    "Persistent memory consists of $N_p \\geq 1$ learnable but input-independent parameter vectors "
    "$P = [p_1, p_2, \\ldots, p_{N_p}]$ that are prepended to the input sequence: "
    "$x_{\\text{new}} = [p_1, \\ldots, p_{N_p}] \\,\\|\\, x$. "
    "These parameters are fixed at test time and encode task-level knowledge (task-abstract memory), "
    "complementing the contextual (data-dependent) neural long-term memory. "
    "They also mitigate the implicit attention bias toward initial tokens under causal masking "
    "by redistributing attention weights more uniformly [@Sukhbaatar2019; @Behrouz2025].",
    title="Persistent (task) memory module",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.3"},
)

persistent_memory_ffn_equivalence = claim(
    "Persistent memory weights are functionally equivalent to the feed-forward network (FFN) layers "
    "in standard Transformers. Sukhbaatar et al. [@Sukhbaatar2019] showed that replacing ReLU in "
    "FFN layers with Softmax yields data-independent attention-like weights: "
    "$\\text{FFN}(x) = W_V \\, \\text{Softmax}(W_K x)$, where $W_K$ and $W_V$ play the role of "
    "data-independent $K$ and $V$ matrices. Persistent memory tokens prepended to the sequence "
    "achieve the same effect through the attention mechanism.",
    title="Persistent memory as data-independent FFN equivalent",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.3"},
)

# ── Strategies (Pass 2) ───────────────────────────────────────────────────────

strat_surprise_from_gradient = support(
    [surprise_as_gradient],
    momentum_motivation,
    background=[neuropsych_memory_definition],
    reason=(
        "Given that @surprise_as_gradient uses the gradient $\\nabla \\ell$ as surprise, "
        "a purely momentary gradient signal is insufficient: after a highly surprising token "
        "the gradient becomes very small, causing the model to miss subsequent related tokens. "
        "The neuropsychological parallel (@neuropsych_memory_definition) — an initial surprising "
        "event keeps drawing attention over time — motivates adding a momentum term $S_t$ that "
        "accumulates past surprise, ensuring the informational \"echo\" of a surprising event "
        "persists over subsequent tokens."
    ),
    prior=0.9,
)

strat_meta_learning_equiv = deduction(
    [online_meta_learning_equivalence],
    parallel_training_claim,
    background=[assoc_memory_loss_def, memory_update_rule_def, parallel_training_setup],
    reason=(
        "The meta-learning formulation (@online_meta_learning_equivalence) enables parallel computation: "
        "by definition (@assoc_memory_loss_def), $\\mathcal{M}$ minimizes $\\ell(\\mathcal{M}_{t-1}; x_t)$ "
        "via gradient descent with the update rule (@memory_update_rule_def). "
        "The chunked structure (@parallel_training_setup) allows all gradients $u_t$ within a chunk "
        "to be computed simultaneously via matmul $\\Theta_b \\mathbf{B}_b (W_0 X - X) X^\\top$; "
        "the momentum recurrence is solvable via parallel associative scan [@SmithWarrington2023]. "
        "This is exactly the structure needed for tensorized training."
    ),
    prior=0.95,
)

strat_forgetting_generalizes = support(
    [forgetting_mechanism_claim],
    forgetting_generalizes_rnn_gates,
    background=[memory_update_rule_def],
    reason=(
        "The full LMM update rule (@memory_update_rule_def) includes three novelties: "
        "(1) weight decay $(1-\\alpha_t)$ as a data-dependent forget gate "
        "(@forgetting_mechanism_claim) — setting $\\eta_t=0$ recovers DeltaNet/Gated DeltaNet "
        "[@YangGatedDelta2024]; (2) momentum $\\eta_t S_{t-1}$ — setting $\\eta_t=0$ removes "
        "momentum and yields gated variants; (3) deep non-linear memory replacing linear matrix "
        "memory. Therefore LMM strictly generalizes these models from three aspects."
    ),
    prior=0.92,
)

strat_persistent_memory_equiv = deduction(
    [persistent_memory_claim],
    persistent_memory_ffn_equivalence,
    reason=(
        "By the result of @Sukhbaatar2019 (cited in @persistent_memory_claim), replacing ReLU in "
        "FFN layers with Softmax yields $\\text{FFN}(x) = W_V \\text{Softmax}(W_K x)$, which is "
        "equivalent to an attention module with data-independent keys/values $W_K, W_V$. "
        "Prepending persistent memory tokens $P$ to the sequence achieves the same effect: "
        "during attention, the model learns to attend to these fixed tokens, and the attention "
        "weights become data-independent — functionally equivalent to the FFN."
    ),
    prior=0.95,
)

# ── Theory vs baseline comparison (for abduction setup) ─────────────────────

alt_momentary_surprise = claim(
    "Alternative approach: using only the momentary gradient $-\\theta_t \\nabla \\ell(\\mathcal{M}_{t-1}; x_t)$ "
    "as the surprise metric (no momentum term $\\eta_t S_{t-1}$), as in TTT-layer [@YuSun2024] "
    "and DeltaNet [@YangDeltaNet2024]. This approach misses the token flow/information continuity "
    "across surprising events in a sequence.",
    title="Alternative: momentary-only surprise (no momentum)",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Section 3.1, Appendix C"},
)

obs_momentum_benefit = claim(
    "In ablation experiments, removing the momentum term from the neural memory module "
    "(w/o Momentum variant) increases perplexity from 27.01 to 28.98 and reduces commonsense "
    "reasoning accuracy from 47.83% to 45.49%, with long-context accuracy dropping from "
    "92.68% to 87.12% (Table 5). This demonstrates that momentum contributes meaningfully "
    "to performance across all task types [@Behrouz2025].",
    title="Observed momentum contribution (ablation)",
    metadata={"source": "artifacts/2501.00663-titans.pdf, Table 5"},
)

pred_momentum = claim(
    "The momentum-augmented surprise rule predicts that model performance on tasks requiring "
    "coherent long-range information processing will be better than the momentary-only baseline, "
    "because momentum propagates the informational echo of surprising events over subsequent tokens.",
    title="Prediction: momentum improves long-range coherence",
)

pred_no_momentum = claim(
    "The momentary-only surprise alternative (TTT-style) predicts comparable performance on "
    "short contexts but degraded performance on tasks requiring information continuity over longer "
    "sequences, since context-change signals cannot sustain attention across token boundaries.",
    title="Prediction: no-momentum baseline degrades on long contexts",
)

s_h_momentum = support(
    [momentum_motivation],
    obs_momentum_benefit,
    reason="Momentum-augmented surprise (@momentum_motivation) explains why removing momentum increases perplexity and reduces accuracy: the model loses the ability to maintain informational continuity after surprising events.",
    prior=0.88,
)

s_alt_no_momentum = support(
    [alt_momentary_surprise],
    obs_momentum_benefit,
    reason="Momentary-only surprise (@alt_momentary_surprise) can partially explain the observations, but predicts less degradation on short contexts; it cannot explain the long-context accuracy drop from 92.68% to 87.12%.",
    prior=0.45,
)

comp_momentum = compare(
    pred_momentum, pred_no_momentum, obs_momentum_benefit,
    reason="The observed momentum ablation results (perplexity +1.97, long-context accuracy -5.56pp) match the momentum theory's predictions much better than the no-momentum baseline's predictions, which expected less degradation.",
    prior=0.85,
)

abduction_momentum = abduction(
    s_h_momentum, s_alt_no_momentum, comp_momentum,
    reason="Both the momentum rule and the momentary-only alternative aim to explain the same empirical observations from Table 5. The abduction asks: which better explains the observed performance gap?",
)
