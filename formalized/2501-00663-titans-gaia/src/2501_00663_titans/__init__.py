from .motivation import *
from .s3_neural_memory import *
from .s4_architecture import *
from .s5_experiments import *

__all__ = [
    # Core theoretical contributions
    "law_titans_effective",
    "titans_expressiveness_theorem",
    "forgetting_generalizes_rnn_gates",
    "parallel_training_claim",
    "deep_memory_expressiveness",
    # Architectural claims
    "titans_three_memory_types",
    "mac_advantages",
    # Key experimental results
    "lm_results_760m",
    "niah_results",
    "babilong_results",
    "time_series_results",
    "component_ablation",
]
