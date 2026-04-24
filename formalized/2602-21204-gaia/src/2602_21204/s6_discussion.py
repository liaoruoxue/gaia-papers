"""Section 7: Discussion, Limitations, and Conclusions"""

from gaia.lang import claim, setting, support, contradiction, complement

from .motivation import (
    claim_ttt_is_linear_attention, claim_linear_view_explains_paradoxes,
    claim_principled_simplifications, claim_memorization_contradicted,
    memorization_hypothesis,
)
from .s4_theory import thm_unrolled, thm_momentum, linear_bias_free_assumption
from .s5_simplifications import (
    claim_ablation_summary, claim_variant2_parallel_speedup, claim_training_speedup,
    claim_step6_standard_linear_attn,
)

# --- Limitations ---

claim_linear_layer_limitation = claim(
    "The theoretical analysis (Theorems 5.1-5.3) requires the TTT model's final layer to be "
    "linear and bias-free. Extending the linear attention equivalence to TTT architectures "
    "with nonlinear final layers (e.g., full MLP with nonlinear activations in all layers "
    "without fixing any as linear) remains an open problem.",
    title="Limitation: nonlinear final-layer architectures not covered",
)

claim_bidirectional_connection_open = claim(
    "Deeper bidirectional connections between TTT and modern linear attention mechanisms "
    "(e.g., Mamba, RWKV, GLA) beyond the unidirectional reduction shown remain unexplored. "
    "Whether insights from linear attention research can be directly transferred back to "
    "improve TTT training algorithms is an open question.",
    title="Limitation: bidirectional TTT-linear attention connections unexplored",
)

# --- Contradiction: linear attention vs memorization interpretations ---

not_both_interpretations = contradiction(
    memorization_hypothesis,
    claim_ttt_is_linear_attention,
    reason=(
        "The memorization interpretation claims TTT functions via storage-and-retrieval "
        "of key-value associations, making the query-key similarity the core mechanism. "
        "The linear attention interpretation (@claim_ttt_is_linear_attention) shows TTT "
        "computes a learned linear projection over accumulated state, where query-key "
        "similarity plays no role in storage. These are mechanistically incompatible: "
        "in linear attention, Q and K determine distinct attention components (not "
        "retrieval indices), which is precisely why Q-K distributional mismatch and "
        "query substitution tolerance are observed. Both interpretations cannot simultaneously "
        "correctly characterize the same computation."
    ),
    prior=0.95,
)

# --- Broader implications ---

claim_ttt_research_reframing = claim(
    "The linear attention reinterpretation of TTT suggests that existing TTT research "
    "may have attributed performance gains to memorization that is actually explained "
    "by the expressive representational capacity of learned linear attention with "
    "dynamic kernel functions. Future TTT research should evaluate whether proposed "
    "improvements are due to memorization mechanisms or linear attention improvements.",
    title="TTT research needs reframing under linear attention lens",
)

claim_design_implications = claim(
    "The linear attention perspective provides principled guidance for TTT architectural "
    "design: (1) final-layer-only updates are sufficient; (2) static kernel functions "
    "enable parallel computation; (3) components such as weight normalization, per-token "
    "learning rates, and momentum are optional and may be removed without major performance "
    "loss. These guidelines are validated by the ablation study.",
    title="Linear attention view provides TTT design guidelines",
)

strat_design_guidelines = support(
    [claim_ttt_is_linear_attention, claim_ablation_summary, claim_variant2_parallel_speedup],
    claim_design_implications,
    reason=(
        "The linear attention equivalence (@claim_ttt_is_linear_attention) identifies which "
        "components are structurally essential (final layer state accumulation) vs. incidental "
        "(normalization, momentum, per-token LR). The ablation study (@claim_ablation_summary) "
        "empirically validates these theoretical predictions: the essential components (final "
        "layer) contribute most, while the incidental ones contribute minimally. The "
        "parallelization speedup (@claim_variant2_parallel_speedup) demonstrates that acting "
        "on these insights yields practical efficiency gains."
    ),
    prior=0.87,
    background=[linear_bias_free_assumption],
)

strat_reframing = support(
    [claim_memorization_contradicted, claim_ttt_is_linear_attention,
     claim_linear_view_explains_paradoxes],
    claim_ttt_research_reframing,
    reason=(
        "The combination of: (1) empirical evidence against memorization "
        "(@claim_memorization_contradicted), (2) formal equivalence to linear attention "
        "(@claim_ttt_is_linear_attention), and (3) mechanistic explanations of all paradoxes "
        "(@claim_linear_view_explains_paradoxes) collectively establishes that the memorization "
        "framing is mechanistically incorrect. If the mechanism is linear attention, prior "
        "TTT research that attributed improvements to memorization should be reinterpreted "
        "under the correct mechanistic lens."
    ),
    prior=0.82,
    background=[memorization_hypothesis],
)
