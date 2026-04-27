"""Section 5-6: Conclusion and acknowledged limitations."""

from gaia.lang import claim, setting, support

from .s3_method import bidirectional_design_claim, multi_agent_distillable_claim
from .s4_experiments import (
    bon_sota_claim,
    iter_refine_helpful_claim,
)
from .s4_analysis import (
    bidirectional_synergy_claim,
    scaling_law_claim,
    generalization_claim,
    cost_accuracy_tradeoff_claim,
)


# --- Conclusion ---

agentic_verifier_promising_claim = claim(
    "Agentic Verifier is a promising paradigm for agentic reward modeling, delivering "
    "substantial improvements over SOTA ORMs and PRMs in both parallel and sequential TTS."
)

conclusion_support = support(
    [bon_sota_claim, iter_refine_helpful_claim, bidirectional_synergy_claim,
     scaling_law_claim, generalization_claim],
    agentic_verifier_promising_claim,
    reason="Five converging lines of evidence (BoN SOTA, iterative-refinement gains, "
           "ablation synergy, scaling, and out-of-domain generalization) all point to the "
           "same conclusion.",
    prior=0.9,
)


# --- Limitations (Section 6) ---

limitations_setting = setting(
    "The paper acknowledges three limitations: (1) reliance on synthetic tool-augmented "
    "data may not represent real-world reasoning variety, (2) the multi-turn process "
    "increases computational cost, and (3) performance is tied to the coverage and "
    "reliability of available external tools."
)

synthetic_data_limit_claim = claim(
    "Reliance on synthetic verification trajectories may limit generalization to real-world "
    "reasoning problems whose distribution is not covered by the synthetic engine.",
    background=[limitations_setting],
)

cost_limit_claim = claim(
    "The multi-turn deliberative process increases compute cost and presents challenges "
    "for real-time or resource-limited deployment.",
    background=[limitations_setting],
)

tool_dependency_limit_claim = claim(
    "Performance depends on the coverage and reliability of external tools, which can "
    "bottleneck certain tasks.",
    background=[limitations_setting],
)

cost_limit_support = support(
    [cost_accuracy_tradeoff_claim],
    cost_limit_claim,
    reason="Table 5's measured ~2.7x latency overhead directly evidences the cost concern.",
    prior=0.95,
    background=[limitations_setting],
)

# --- Code release setting (provenance / reproducibility) ---

code_release_setting = setting(
    "The authors note in the abstract that code is available at GitHub, supporting "
    "reproducibility of the AgentV-RL recipe."
)
