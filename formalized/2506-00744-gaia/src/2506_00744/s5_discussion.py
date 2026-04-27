"""Section 5-6: Related work, limitations, and conclusion."""

from gaia.lang import claim, setting, support

from .motivation import (
    claim_layerwise_hybrid_alt,
    claim_compatibility_with_efficient_kernels,
    proposal_synchronous_best,
)
from .s3_methods import (
    claim_delayed_chunk_connection,
    claim_synchronous_arora_connection,
    def_synchronous,
)
from .s4_experiments import (
    claim_retrieval_unsatisfactory,
    claim_fw_choice_matters,
)

# ---------------------------------------------------------------------------
# Related work (Sec 5)
# ---------------------------------------------------------------------------

claim_intra_layer_uniqueness = claim(
    "QT and LT share the same per-step query/key/value generators, so they can "
    "be blended at the *single-layer* level on a common stream of "
    "$(q_t, k_t, v_t)$. Layer-wise hybrids such as Griffin, Samba and xLSTM "
    "instead alternate distinct layer types and cannot exploit this shared "
    "primitive structure. Intra-layer blending is the architectural niche this "
    "paper occupies.",
    title="QT/LT share q,k,v generators -> intra-layer blending is uniquely available",
)

claim_arora_limitation = claim(
    "Arora et al.'s [@Arora2024Based] hybrid focuses on a recall/throughput "
    "trade-off and uses vanilla LA as its FW-memory operator. Vanilla LA "
    "underperforms more advanced FWPs (DeltaNet, GLA), so their study cannot "
    "characterise the upper limit of intra-layer hybrids that combine softmax "
    "attention with a competitive FWP.",
    title="Arora et al. is limited by their use of vanilla LA",
)

claim_munkhdalai_limitation = claim(
    "Munkhdalai et al.'s [@Munkhdalai2024Infini] Infini-attention uses the "
    "Delayed-Chunk hybrid scheme and a delta-rule FW-memory but omits recent "
    "FWP improvements (careful $\\phi$ choice, removed normaliser, dynamic "
    "learning rate $\\beta_t$). Because Delayed-Chunk also forfeits the "
    "expressivity advantage of DeltaNet, Infini-attention cannot characterise "
    "the true potential of intra-layer hybrid attention.",
    title="Infini-attention is sub-optimal: Delayed-Chunk + outdated FWP choices",
)

# ---------------------------------------------------------------------------
# Limitations (Sec 5)
# ---------------------------------------------------------------------------

claim_long_window_unavoidable = claim(
    "For precise long-range retrieval, the experiments suggest that a large "
    "KV-memory window remains unavoidable: even the best HQLT with a 1024-token "
    "window does not reach the full-context (2048-token) Transformer++ on the "
    "FDA/SWDE/SQuAD suite. There is non-zero chance that more layers/depth "
    "could close this gap with a small window, but the paper does not "
    "demonstrate it.",
    title="Limitation: large KV-window still required for top retrieval",
    background=[def_synchronous],
)

claim_future_revival_mechanism = claim(
    "A potential remediation suggested by the paper is to introduce a "
    "communication mechanism whereby FW-memory can selectively *revive* "
    "memory events and reinsert them into the limited KV-memory, replacing "
    "the current strict sliding-window policy. Such a mechanism is "
    "non-trivial to implement under hardware-efficiency constraints and is "
    "left as future work.",
    title="Future direction: FW-to-KV revival mechanism (not yet built)",
)

# ---------------------------------------------------------------------------
# Final synthesis
# ---------------------------------------------------------------------------

claim_design_principle = claim(
    "The paper's overarching design principle for intra-layer hybrid attention "
    "is: (i) combine the two memory operators on the same per-step "
    "$(q_t, k_t, v_t)$ stream within a single layer; (ii) feed the same input "
    "synchronously to both; and (iii) choose a state-tracking-capable FWP "
    "(DeltaNet) for the FW branch. Following these three principles yields the "
    "best overall design across LM, expressivity, retrieval and RL.",
    title="Design principle: intra-layer + synchronous + DeltaNet FWP",
)

# Reasoning chains: link related-work claims to the main proposal

strat_design_principle = support(
    [proposal_synchronous_best, claim_intra_layer_uniqueness, claim_synchronous_arora_connection],
    claim_design_principle,
    reason=(
        "The three legs of the design principle are the three structural choices "
        "that distinguish this work: (1) intra-layer blending (@claim_intra_layer_uniqueness); "
        "(2) synchronous delivery, supported by @proposal_synchronous_best; and "
        "(3) DeltaNet as FW operator (the upgrade over Arora et al., "
        "@claim_synchronous_arora_connection). Together they characterise the "
        "winning architectural region the paper identifies."
    ),
    prior=0.9,
    background=[def_synchronous],
)

strat_munkhdalai_limitation = support(
    [claim_delayed_chunk_connection],
    claim_munkhdalai_limitation,
    reason=(
        "Infini-attention is structurally a Delayed-Chunk HQLT "
        "(@claim_delayed_chunk_connection); it therefore inherits the expressivity "
        "loss demonstrated for Delayed-Chunk on parity/modular arithmetic, in "
        "addition to using older FWP design choices (no dynamic $\\beta_t$, "
        "extra normaliser kept, etc.). Both factors limit the architecture's "
        "achievable potential."
    ),
    prior=0.85,
)

# Wire the Arora-limitation claim into the FW-choice evidence
strat_arora_limitation = support(
    [claim_fw_choice_matters],
    claim_arora_limitation,
    reason=(
        "The HQLT ablations directly demonstrate that swapping DeltaNet for "
        "vanilla LA collapses both LM and expressivity performance "
        "(@claim_fw_choice_matters). Arora et al.'s use of vanilla LA therefore "
        "puts a firm ceiling on the achievable hybrid quality of their study."
    ),
    prior=0.85,
)

# Wire the long-window-unavoidable claim into the retrieval-unsatisfactory evidence
strat_long_window_unavoidable = support(
    [claim_retrieval_unsatisfactory],
    claim_long_window_unavoidable,
    reason=(
        "If retrieval performance gradually rises with window size up to 1024 "
        "but still trails full-context Transformer++ (@claim_retrieval_unsatisfactory), "
        "then within the tested setup precise long-range retrieval still "
        "demands a large KV-window. The conclusion is hedged because the paper "
        "explicitly notes that more layers/depth might in principle close the "
        "gap with smaller windows."
    ),
    prior=0.85,
    background=[def_synchronous],
)

# Wire intra-layer uniqueness from the existence of layer-wise alternatives:
# the paper's contribution is intra-layer because layer-wise hybrids exist but
# do not exploit shared (q,k,v) generators.
strat_intra_layer_uniqueness = support(
    [claim_layerwise_hybrid_alt],
    claim_intra_layer_uniqueness,
    reason=(
        "Existing hybrids of QT and LT operate at the layer-wise granularity "
        "(@claim_layerwise_hybrid_alt). The opportunity that this work exploits "
        "— intra-layer blending on a shared $(q_t, k_t, v_t)$ stream — is "
        "uniquely available because QT and LT share their per-step generators, "
        "and is not exploited by any of the layer-wise alternatives."
    ),
    prior=0.85,
)

# Tie compatibility-with-efficient-kernels to the design principle (it's part of why
# this design is practical).
# Wire the future-revival-mechanism speculation as a proposed remedy to the
# unavoidable-window limitation
strat_future_revival_motivation = support(
    [claim_long_window_unavoidable],
    claim_future_revival_mechanism,
    reason=(
        "Because precise long-range retrieval still requires a large KV-window "
        "(@claim_long_window_unavoidable), an architectural mechanism that lets "
        "FW-memory selectively revive past events back into the limited "
        "KV-memory could in principle relax this constraint. This is the "
        "concrete future direction the paper proposes."
    ),
    prior=0.5,
)

strat_design_principle_practicality = support(
    [claim_compatibility_with_efficient_kernels],
    claim_design_principle,
    reason=(
        "A design principle is only useful if it can be realised efficiently. "
        "@claim_compatibility_with_efficient_kernels notes that all HQLT variants "
        "remain compatible with FlashAttention-2 and flash-linear-attention, "
        "so the recommended Synchronous + DeltaNet design can be deployed using "
        "existing high-performance kernels — supporting the practical "
        "applicability of @claim_design_principle."
    ),
    prior=0.85,
)


__all__ = [
    "claim_intra_layer_uniqueness",
    "claim_arora_limitation",
    "claim_munkhdalai_limitation",
    "claim_long_window_unavoidable",
    "claim_future_revival_mechanism",
    "claim_design_principle",
    "strat_design_principle",
    "strat_munkhdalai_limitation",
    "strat_arora_limitation",
    "strat_long_window_unavoidable",
    "strat_intra_layer_uniqueness",
    "strat_design_principle_practicality",
    "strat_future_revival_motivation",
]
