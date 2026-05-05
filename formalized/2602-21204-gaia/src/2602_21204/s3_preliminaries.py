"""Section 3: Preliminary -- formal TTT-KVB mechanism.

Pure definitional content (settings) needed by Sections 4-7. Defines the
fast-weight network $f_\\theta$, the projection of input tokens into
$(K, V, Q)$, the inner-loop key-value binding objective, and the
update-then-evaluate computational pattern.
"""

from gaia.lang import setting

# ---------------------------------------------------------------------------
# 3. Per-layer mechanism
# ---------------------------------------------------------------------------

setup_fast_weights = setting(
    "**Fast-weight network.** Each TTT sequence-modeling layer maintains "
    "a *fast-weight* network $f_\\theta$ -- typically a lightweight MLP "
    "(e.g. a SwiGLU MLP or a GLU) parameterized by $\\theta$ -- that is "
    "updated *during both training and inference*. The fast weights are "
    "distinguished from the *slow weights* of the surrounding model "
    "(token embeddings, projection matrices, attention output projections), "
    "which are updated only during training.",
    title="Fast-weight network $f_\\theta$",
)

setup_kvq_projection = setting(
    "**Token projections.** For each input token, the layer produces "
    "three projected vectors -- a key $k$, a value $v$, and a query $q$ "
    "-- analogous to the $K$, $V$, $Q$ of standard attention "
    "[@Vaswani2017]. The projections are learnable slow-weight linear "
    "maps; the resulting $(k, v, q)$ tuple drives the inner-loop "
    "fast-weight update and the subsequent output computation.",
    title="Per-token key, value, query projections $(k, v, q)$",
)

setup_inner_loop_loss = setting(
    "**Inner-loop key-value binding objective.** TTT-KVB performs *online "
    "gradient descent* on $f_\\theta$ using a self-supervised key-value "
    "association loss. The most common choices are the squared-error / "
    "MSE loss "
    "$\\mathcal{L}(f_\\theta(k), v) = \\|f_\\theta(k) - v\\|_2^2$ "
    "and the Frobenius dot-product loss "
    "$\\mathcal{L}(f_\\theta(k), v) = -\\langle f_\\theta(k), v\\rangle$ "
    "used in LaCT [@Zhang2025] and ViTTT [@Han2025]. The key $k$ acts as "
    "the input and the value $v$ as the regression target.",
    title="Inner-loop loss $\\mathcal{L}(f_\\theta(k), v)$",
)

setup_update_then_query = setting(
    "**Update-then-query pattern.** At each token step $t$ the TTT layer "
    "executes (i) one or more inner-loop gradient steps on "
    "$\\mathcal{L}(f_{\\theta_t}(k_t), v_t)$ to obtain updated parameters "
    "$\\theta_{t+1}$, then (ii) evaluates the *updated* function "
    "$f_{\\theta_{t+1}}$ on the query $q_t$ to produce the output "
    "$o_t = f_{\\theta_{t+1}}(q_t)$. This update-then-query order is the "
    "computational signature of TTT-KVB.",
    title="Update-then-query computational pattern of TTT-KVB",
)

setup_inner_loop_hyperparameters = setting(
    "**Inner-loop design choices.** A TTT-KVB layer has several "
    "hyperparameters that distinguish concrete instantiations: (a) the "
    "*depth and architecture* of $f_\\theta$ (single linear layer vs "
    "multi-layer SwiGLU MLP); (b) the *number of inner-loop gradient "
    "steps* per token; (c) the *learning rate* (constant or per-token "
    "learnable $\\eta_t$); (d) optional *momentum* $\\alpha_t$; "
    "(e) optional *weight normalization* of $f_\\theta$ after each "
    "update; (f) optional *gradient orthogonalization* (e.g. Muon-style "
    "[@Jordan2024]) applied to the fast-weight gradient before the step.",
    title="Inner-loop design choices: depth / steps / learning rate / momentum / norm / orthogonalization",
)

setup_storage_retrieval_definition = setting(
    "**Storage-and-retrieval interpretation (formal restatement).** Under "
    "the prevailing view, the inner-loop optimization is interpreted as "
    "*storing* key-value associations $\\{(k_i, v_i)\\}_{i \\le t}$ "
    "inside $f_{\\theta_{t+1}}$ -- the network is trained to map each "
    "key to its value. The query $q_t$ then *retrieves* a stored value "
    "by evaluating $f_{\\theta_{t+1}}(q_t)$. Architectural capacity, "
    "optimizer choice, and inner-loop step count are all design "
    "variables motivated by improving the *fidelity* of this memorization "
    "(@setup_memorization_interpretation).",
    title="Formal restatement: storage = inner-loop fit; retrieval = query evaluation",
)

setup_paper_scope = setting(
    "**Scope of this paper.** Among the various TTT formulations [@Sun2025; "
    "@Gandelsman2022; @Sun2020; @Tandon2025; @Behrouz2025b], this paper "
    "*exclusively* analyzes TTT-KVB -- variants that optimize a key-value "
    "binding objective in the inner loop (e.g. LaCT, ViTTT, Titans) -- "
    "and not TTT methods that backpropagate from the final task loss "
    "[@Tandon2025; @Behrouz2025b].",
    title="Paper scope: TTT-KVB only (LaCT, ViTTT, Titans family)",
)

__all__ = [
    "setup_fast_weights",
    "setup_kvq_projection",
    "setup_inner_loop_loss",
    "setup_update_then_query",
    "setup_inner_loop_hyperparameters",
    "setup_storage_retrieval_definition",
    "setup_paper_scope",
]
