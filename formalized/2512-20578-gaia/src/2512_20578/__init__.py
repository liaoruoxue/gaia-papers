from .motivation import *
from .s2_background import *
from .s3_architecture import *
from .s4_results import *
from .s5_transfer import *
from .s6_ablations import *
from .s7_early_detection import *
from .s8_discussion import *
from .priors import PRIORS

__all__ = [
    # Core thesis
    "internal_cues_exist",
    "gnosis_proposal",
    # Architecture
    "hidden_circuit_arch",
    "attention_circuit_arch",
    "gated_fusion_arch",
    "total_params",
    "constant_latency",
    "frozen_backbone",
    "training_protocol",
    # Main results
    "gnosis_superior_overall",
    "gnosis_math_perf",
    "gnosis_trivia_perf",
    "gnosis_mmlu_perf",
    "calibration_quality",
    "latency_comparison",
    # Transfer
    "transfer_generalizes",
    "transfer_fails_cross_family",
    "shared_circuits_hypothesis",
    # Early detection
    "gnosis_generalizes_partial",
    "early_stopping_implication",
    # Conclusions
    "internal_signals_claim",
]
