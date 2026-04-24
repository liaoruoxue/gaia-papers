"""Prior assignments for independent (leaf) claims in the CIB paper package."""

from . import (
    budget_forcing_heuristic,
    deepscaler_7b_prior,
    deepscaler_cib_aggressive,
    pred_cib_better,
    pred_l1_worse,
    transformer_attention_violates_markov,
)

PRIORS = {
    # Empirical observation: CoT methods with token penalties exist; their flat-tax
    # nature is widely documented. High confidence in this characterization.
    budget_forcing_heuristic: (
        0.92,
        "Broadly supported by literature on length penalties (L1, LCPO) treating all tokens "
        "equally regardless of semantic content. Multiple papers confirm this design choice.",
    ),
    # Empirical result: DeepScaleR-1.5B with CIB 7B prior achieves 41% compression.
    # This is a directly measured experimental outcome reported in Table 1.
    deepscaler_7b_prior: (
        0.90,
        "Directly measured experimental result from Table 1. 41% average token reduction with "
        "−0.7pp accuracy loss is a concrete, verifiable empirical measurement.",
    ),
    # Empirical result: DeepScaleR-1.5B with CIB 1.5B prior aggressive achieves 29% compression.
    # This is a directly measured experimental outcome reported in Table 1.
    deepscaler_cib_aggressive: (
        0.90,
        "Directly measured experimental result from Table 1. 29% average token reduction with "
        "+1.3pp accuracy is a concrete, verifiable empirical measurement.",
    ),
    # Prediction from CIB theory: semantic cost should preserve accuracy better than length
    # penalties. This is the core theoretical prediction of the paper.
    pred_cib_better: (
        0.82,
        "Theoretical prediction grounded in CIB framework — semantic surprisal cost should "
        "distinguish essential from filler tokens. Strong theoretical backing, but the "
        "empirical outcome was not guaranteed a priori.",
    ),
    # Prediction from length-penalty theory: flat penalties should lose more accuracy.
    # This follows directly from the semantic blindness of uniform token counting.
    pred_l1_worse: (
        0.75,
        "Theoretical prediction: uniform token penalty cannot distinguish essential reasoning "
        "from cognitive bloat. Moderate confidence — L1 methods may perform better than "
        "expected if training adapts to the penalty signal.",
    ),
    # Core claim about transformers: attention mechanism violates IB Markov assumption.
    # This is a theoretical observation backed by the architecture definition.
    transformer_attention_violates_markov: (
        0.95,
        "Directly follows from the transformer architecture: causal attention allows answer "
        "generation to attend to both prompt X and trace Z via key-value cache, creating "
        "a collider structure (X,Z)→Y rather than Markov chain Y↔X↔Z. High confidence.",
    ),
}
