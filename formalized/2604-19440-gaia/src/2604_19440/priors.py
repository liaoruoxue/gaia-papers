"""
Priors for 2604-19440: What Makes an LLM a Good Optimizer?

All independent (leaf) claims are assigned priors here.
Derived claims (conclusions of strategies) are NOT assigned priors.

Prior rationale:
- Empirical results (15 LLMs × 8 tasks × 72K solutions) with reported significance:
  high priors (0.85–0.93).
- Qualitative case studies (single model pair, Figure 5): moderate priors (0.80).
- Limitations acknowledged by authors (true by authors' own admission): high priors (0.88–0.90).
- The novelty-as-exploration hypothesis: plausible prior belief in the field but refuted: 0.60.
"""

from . import (
    breakthrough_rate_predicts,
    controlled_comparison,
    fitness_entropy_negative,
    generation_index_negative,
    limitation_fixed_protocol,
    limitation_model_mixing_confound,
    limitation_novelty_operationalization,
    lrr_predicts_strongly,
    model_mixing_degrades_performance,
    novelty_not_significant,
    novelty_not_sufficient_hypothesis,
    novelty_positive_conditional,
    optimization_gap_exists,
    pcd_negative_mediated,
    strong_optimizers_localize,
    temperature_robustness,
    weak_optimizers_drift,
    zeroshot_correlates_with_final,
)

PRIORS = {
    # Empirical findings with high statistical confidence
    breakthrough_rate_predicts: (
        0.92,
        "Highly significant OLS result: β=0.445 (p<0.001, R²=0.198) alone; β=0.389 (p<0.001) joint (Table 14).",
    ),
    zeroshot_correlates_with_final: (
        0.92,
        "Strong positive correlation (r=0.860, p<0.001) across 15 LLMs and 8 tasks (Figure 3).",
    ),
    optimization_gap_exists: (
        0.95,
        "Directly observed outcome gap under identical experimental conditions (Table 2, N=15 models).",
    ),
    novelty_not_significant: (
        0.90,
        "Multiple OLS specifications (M1-M5) all show non-significant novelty (p>0.6); Table 13.",
    ),
    lrr_predicts_strongly: (
        0.92,
        "Highly significant (β=0.528, p<0.001), robust to inclusion of other predictors (Table 1).",
    ),
    pcd_negative_mediated: (
        0.85,
        "PCD coefficient goes from -0.329 (sig) to -0.024 (ns) when LRR added (Table 1).",
    ),
    fitness_entropy_negative: (
        0.88,
        "Significant in both concurrent (p=0.005) and lagged (p=0.002) mixed-effects models (Table 15).",
    ),
    novelty_positive_conditional: (
        0.88,
        "Concurrent mean novelty β=0.070 (p=0.006), but interaction β=-0.090 (p<0.001) dominates (Table 15).",
    ),
    generation_index_negative: (
        0.93,
        "Very strong: concurrent β=-0.250 (p<0.001), lagged β=-0.193 (p<0.001) (Table 15).",
    ),
    model_mixing_degrades_performance: (
        0.85,
        "Monotonic degradation on TSP-60 and bin packing; co-varies with LRR reduction (Figure 7).",
    ),
    temperature_robustness: (
        0.80,
        "Strong on TSP (r=0.76-0.92, p<0.05) but non-significant on Oscillator tasks (Table 11).",
    ),
    # Qualitative case study results
    strong_optimizers_localize: (
        0.80,
        "Qualitative case study (Gemini-1.5-Pro, TSP-60, Figure 5); consistent with quantitative data.",
    ),
    weak_optimizers_drift: (
        0.80,
        "Qualitative case study (Mistral-7B, TSP-60, Figure 5); paired contrast with Gemini-1.5-Pro.",
    ),
    # Methodological claim
    controlled_comparison: (
        0.90,
        "Shared initial population and identical selection/evaluation ensure valid controlled design.",
    ),
    # Limitations (acknowledged by authors — high confidence as observations)
    limitation_fixed_protocol: (
        0.90,
        "Authors explicitly acknowledge: only one fixed evolutionary protocol tested.",
    ),
    limitation_model_mixing_confound: (
        0.88,
        "Authors acknowledge: model mixing may confound LRR with other latent behavioral properties.",
    ),
    limitation_novelty_operationalization: (
        0.88,
        "Authors acknowledge: novelty only measured as nearest-neighbor distance.",
    ),
    # Prior belief under test
    novelty_not_sufficient_hypothesis: (
        0.60,
        "Widely held classical evolutionary intuition; plausible but refuted by study results.",
    ),
}
