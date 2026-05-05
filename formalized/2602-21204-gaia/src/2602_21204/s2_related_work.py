"""Section 2: Related Work -- linear attention and TTT lineages.

Section 2 of Liu et al. 2026 [@Liu2026] surveys two strands:

* 2.1 Linear attention (Katharopoulos 2020 onwards) and its many
  data-dependent variants -- the framework into which the paper will
  reduce TTT-KVB.
* 2.2 Test-time training -- the original distribution-shift formulation
  [@Sun2020], TTT-as-architectural-primitive [@Sun2025], and the
  TTT-KVB / TTT-E2E split [@Tandon2025].

This section provides the background settings and three substantive
historical claims that anchor the paper's contribution: (a) DeltaNet =
TTT with single linear inner layer + MSE loss [@Yang2024a], (b) prior
work has reinterpreted TTT as linear attention only in the restricted
single-linear-layer case [@Sun2025], and (c) the design space of TTT
inner loops has been pushed toward complexity under the memorization
view [@Behrouz2024; @Zhang2025; @Han2025].
"""

from gaia.lang import claim, setting

from .motivation import (
    setup_ttt_paradigm,
    setup_ttt_kvb_focus,
    setup_memorization_interpretation,
)

# ---------------------------------------------------------------------------
# 2.1 Linear attention background
# ---------------------------------------------------------------------------

setup_linear_attention = setting(
    "**Linear attention** [@Katharopoulos2020] is a sequence operator that "
    "replaces the softmax similarity in standard transformer attention "
    "with a kernelized inner product, allowing the per-token computation "
    "to take the form $o_t = \\phi(q_t) \\bigl( S_0 + \\sum_{i \\le t} "
    "\\phi(k_i)^\\top v_i\\bigr)$ for a feature map $\\phi$. This yields "
    "(i) linear-time compute in sequence length and (ii) constant-size "
    "state $S_t \\in \\mathbb{R}^{D_k \\times D_v}$, in contrast to the "
    "$O(L^2)$ compute and $O(L)$ memory of standard softmax attention.",
    title="Setup: linear attention operator (Katharopoulos 2020)",
)

setup_linear_attention_lineage = setting(
    "Recent work has extended linear attention with token-dependent decay "
    "factors [@GuDao2024], data-dependent decay (the *selective mechanism* "
    "in Mamba), and a state-conditioned update rule (DeltaNet "
    "[@Schlag2021]). Chunk parallelization techniques [@Yang2024b] have "
    "made these architectures practically deployable.",
    title="Setup: lineage of linear-attention RNN architectures",
)

# ---------------------------------------------------------------------------
# 2.2 Test-time training background
# ---------------------------------------------------------------------------

setup_ttt_split = setting(
    "When deployed as a sequence-modeling layer, TTT comes in two "
    "variants [@Tandon2025]: (1) **TTT-KVB** uses a key-value binding "
    "loss (e.g. MSE or Frobenius dot product) as the inner-loop "
    "objective [@Sun2025; @Zhang2025; @Han2025; @Behrouz2024]; "
    "(2) **TTT-E2E** backpropagates end-to-end through the inner loop "
    "from the final task loss [@Tandon2025; @Behrouz2025b]. This paper "
    "exclusively addresses TTT-KVB.",
    title="Setup: TTT-KVB vs TTT-E2E split (Tandon et al. 2025)",
)

setup_ttt_application_domains = setting(
    "TTT has been deployed across a wide range of domains: language "
    "modeling [@Sun2025; @Wang2025; @Zhang2025], video generation "
    "[@Dalal2025; @Zhang2025], novel view synthesis [@Zhang2025], and "
    "image classification [@Han2025]. In all these settings the *fast "
    "weights* [@Hinton1987] are updated online at test time using a "
    "self-supervised KV association loss, with the goal of memorizing "
    "history associations.",
    title="Setup: TTT deployment domains and the fast-weight tradition",
)

# ---------------------------------------------------------------------------
# Substantive historical claims (to be cited / used as premises in s5-s6)
# ---------------------------------------------------------------------------

claim_deltanet_equals_linear_ttt = claim(
    "**Existing equivalence (DeltaNet).** DeltaNet [@Schlag2021] and its "
    "variants are equivalent to TTT with a *single linear* inner-loop "
    "layer trained with MSE loss [@Yang2024a]. This is the simplest "
    "TTT-to-linear-attention reduction known prior to this paper, and "
    "it covers only the degenerate single-layer case.",
    title="Prior result: DeltaNet = TTT with single linear layer + MSE",
    background=[setup_ttt_kvb_focus, setup_linear_attention],
)

claim_prior_la_equivalence_restricted = claim(
    "**Prior linear-attention reduction is restricted.** Sun et al. (2025) "
    "[@Sun2025] showed that *in the restricted setting of a single linear "
    "inner-loop layer with zero initialization*, TTT is exactly equivalent "
    "to linear attention. This restricted equivalence is the key prior "
    "result the present paper will *generalize* to multi-layer non-linear "
    "inner-loop functions and momentum-augmented updates (Section 5).",
    title="Prior reduction holds only in the single-linear-layer / zero-init regime",
    background=[setup_ttt_kvb_focus, setup_linear_attention],
)

claim_complexity_drift_under_memorization = claim(
    "**Architectural drift under the memorization view.** Because the "
    "storage-and-retrieval interpretation "
    "(@setup_memorization_interpretation) treats faithful KV memorization "
    "as the desideratum, recent TTT designs have grown increasingly "
    "complex: deeper inner-loop MLPs [@Han2025; @Behrouz2024], "
    "Muon-style gradient orthogonalization [@Zhang2025; @Jordan2024], "
    "weight normalization [@Zhang2025], momentum and per-token learnable "
    "learning rates [@Zhang2025; @Behrouz2024], and alternative "
    "regression targets [@Han2025; @Behrouz2025c]. These additions are "
    "*explicitly motivated* by improving memorization fidelity.",
    title="Memorization-view complexity drift across recent TTT variants",
    background=[setup_memorization_interpretation, setup_ttt_application_domains],
)

claim_ttt_shares_la_compute_profile = claim(
    "**Shared computational profile.** Despite their architectural "
    "complexity, all current TTT-KVB variants share the two defining "
    "computational properties of linear attention "
    "(@setup_linear_attention): linear-time per-token compute and a "
    "constant-size state. This shared compute profile is one of the "
    "*clues* (alongside DeltaNet equivalence and the restricted prior "
    "reduction) that motivates the paper to seek a more general "
    "linear-attention reduction.",
    title="All TTT-KVB variants share linear attention's compute profile (linear time, O(1) state)",
    background=[setup_linear_attention, setup_ttt_kvb_focus],
)

__all__ = [
    "setup_linear_attention",
    "setup_linear_attention_lineage",
    "setup_ttt_split",
    "setup_ttt_application_domains",
    "claim_deltanet_equals_linear_ttt",
    "claim_prior_la_equivalence_restricted",
    "claim_complexity_drift_under_memorization",
    "claim_ttt_shares_la_compute_profile",
]
