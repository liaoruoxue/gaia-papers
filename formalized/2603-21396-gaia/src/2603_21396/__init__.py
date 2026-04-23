from .motivation import *
from .s3_behavioral_robustness import *
from .s4_linear_nonlinear import *
from .s5_mechanisms import *
from .s6_underelicitation import *

__all__ = [
    # Core exported conclusions (main paper contributions)
    "claim_behaviorally_robust",
    "claim_not_single_linear",
    "claim_distinct_mechanisms",
    "claim_underelicited",
    # Key mechanistic results
    "dpo_enables_introspection",
    "dpo_contrastive_structure_key",
    "mlp_l45_causal_result",
    "gate_features_identified",
    "gate_causal_necessity",
    "circuit_hierarchy",
    "gate_inverted_v_posttraining",
    "bias_vector_performance",
]
