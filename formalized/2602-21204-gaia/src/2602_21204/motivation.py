"""Introduction and Motivation: TTT with KV Binding Is Secretly Linear Attention"""

from gaia.lang import claim, setting, question, support, deduction, contradiction, complement

# --- Settings: Background context ---

ttt_definition = setting(
    "Test-Time Training (TTT) with KV binding is an architecture in which a neural network "
    "module learns to memorize key-value (KV) pairs at test time via an inner optimization loop. "
    "Given an input token at position t, the model treats it as a query, and the inner loop "
    "updates the model weights to minimize a loss that fits a mapping from keys to values "
    "within the current context window.",
    title="TTT with KV binding definition",
)

linear_attention_definition = setting(
    "Linear attention is a sequence modeling operator of the form: "
    "$o_t = \\phi_{t+1}(q_t) \\cdot S_t$, where $S_t = S_{t-1} + \\phi_t(k_t)^T v_t$ is a "
    "recurrently accumulated state matrix. Here $\\phi$ denotes a feature map (e.g., ELU+1 or "
    "identity), $q_t$ is the query, $k_t$ the key, $v_t$ the value, and $S_t$ the hidden state. "
    "Linear attention avoids the quadratic cost of softmax attention by maintaining a fixed-size "
    "recurrent state.",
    title="Linear attention definition",
)

memorization_hypothesis = claim(
    "The conventional interpretation of TTT with KV binding is that it functions as "
    "'online meta-learning that memorizes a key-value mapping': the inner-loop gradient updates "
    "write information into the model weights, and the forward pass retrieves this information "
    "via query-key matching, analogous to a learnable associative memory. Under this view, "
    "more inner-loop steps yield better memorization and thus better downstream performance.",
    title="Conventional TTT memorization interpretation (hypothesis)",
)

# --- Research questions ---

q_equivalence = question(
    "Can TTT architectures with KV binding be formally rewritten as linear attention operators, "
    "and if so, what does this reveal about their mechanism?",
    title="TTT-linear attention equivalence question",
)

q_implications = question(
    "What practical simplifications follow from understanding TTT as learned linear attention, "
    "in terms of architectural design and inference efficiency?",
    title="Practical implications question",
)

# --- Core claims: Motivation and challenge to memorization ---

claim_memorization_contradicted = claim(
    "Multiple observed phenomena directly contradict the memorization-based interpretation of "
    "TTT with KV binding. Specifically: (1) increasing inner-loop iterations improves fitting "
    "loss but degrades downstream task performance; (2) replacing gradient descent with gradient "
    "ascent preserves or even slightly improves task performance; (3) t-SNE visualization reveals "
    "significant mismatch between query and key distributions in trained models; and (4) "
    "substituting keys for queries produces negligible performance degradation. None of these "
    "observations is consistent with a storage-and-retrieval system.",
    title="Memorization interpretation contradicted by four phenomena",
)

claim_ttt_is_linear_attention = claim(
    "A broad class of TTT architectures with KV binding can be formally expressed as learned "
    "linear attention operators. Under this reinterpretation, TTT is not a memorization "
    "mechanism but rather a learned linear attention with enhanced representational capacity "
    "achieved through expressive kernel functions and dynamic state updates.",
    title="TTT is linear attention (core thesis)",
)

claim_linear_view_explains_paradoxes = claim(
    "The linear attention interpretation of TTT explains all four empirical paradoxes that "
    "contradict the memorization view: more inner-loop steps cause train-test kernel mismatch "
    "(not better memorization); gradient sign flips are absorbed into learned projections; "
    "Q-K distributional asymmetry is expected since they determine distinct attention components; "
    "and query substitution tolerance reflects that the feature maps $\\phi_{t+1}(k)$ and "
    "$\\phi_t(k)$ remain functionally distinct.",
    title="Linear attention view explains empirical paradoxes",
)

claim_principled_simplifications = claim(
    "The linear attention perspective enables principled architectural simplifications of TTT "
    "and fully parallel formulations that preserve performance while improving efficiency, "
    "demonstrated across language modeling, novel view synthesis, and image classification tasks.",
    title="Linear attention view enables principled simplifications",
)
