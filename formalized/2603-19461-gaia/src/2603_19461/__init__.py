from .motivation import *
from .s3_methods import *
from .s5_results import *
from .s6_safety import *

__all__ = [
    # Core exported conclusions
    "hyperagent_advantage",
    "dgmh_no_domain_alignment",
    "law_dgmh_improves",
    "meta_improvements_transfer",
    "self_improvements_compound",
    "metacognition_necessary",
    "open_ended_mitigates_convergence",
    # Key empirical results
    "dgmh_paper_review_result",
    "dgmh_robotics_result",
    "dgmh_coding_comparable_to_dgm",
    "dgmh_transfer_imp50",
    "dgmh_proofautograder_result",
    # Safety
    "safety_concern_oversight",
]
