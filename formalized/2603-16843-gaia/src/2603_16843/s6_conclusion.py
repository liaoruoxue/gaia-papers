"""Section 6: Conclusion — synthesis of the paper's contributions."""

from gaia.lang import claim, support

from .motivation import (
    claim_agency_internalization,
    claim_test_time_cost,
)
from .s3_method import (
    claim_branching_targets_failures,
    claim_cf_internalizes_recovery,
)
from .s4_experiments import (
    claim_leafe_beats_grpo_passk,
    claim_internalization_supported,
    claim_stage1_branching_better,
)

# ── Synthesizing claims ──────────────────────────────────────────────────────

claim_leafe_practical = claim(
    "LEAFE is a practical recipe for developing LLM agents that continue to "
    "improve through deployment-time interaction: it accepts any RLVR-trained "
    "checkpoint as input, requires only that the environment provides "
    "diagnostic feedback and supports rollback, and produces a single-rollout "
    "policy with broader behavioral coverage than the outcome-driven baseline.",
    title="LEAFE is a deployment-ready recipe"
)

claim_pass_burden_shift = claim(
    "By internalizing reflective experience into model weights, LEAFE shifts "
    "the burden of competence from heavy test-time sampling toward the trained "
    "policy itself, reducing reliance on best-of-$K$ and explicit search at "
    "inference time.",
    title="LEAFE shifts competence from test-time sampling to weights"
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_practical = support(
    [
        claim_internalization_supported,
        claim_leafe_beats_grpo_passk,
        claim_stage1_branching_better,
    ],
    claim_leafe_practical,
    reason=(
        "Three pieces of evidence jointly justify the practical claim: "
        "(i) the internalization thesis is empirically supported "
        "(@claim_internalization_supported); (ii) LEAFE consistently beats "
        "GRPO at Pass@128 across diverse benchmarks "
        "(@claim_leafe_beats_grpo_passk); (iii) Stage-1 branching is the "
        "most effective use of a fixed exploration budget "
        "(@claim_stage1_branching_better). Together they make LEAFE a viable "
        "post-RLVR recipe."
    ),
    prior=0.82
)

strat_burden_shift = support(
    [claim_cf_internalizes_recovery, claim_internalization_supported],
    claim_pass_burden_shift,
    reason=(
        "The counterfactual loss internalizes the corrective alternative into "
        "the policy weights (@claim_cf_internalizes_recovery), and the "
        "Pass@128 improvements without test-time rollback "
        "(@claim_internalization_supported) confirm that the resulting policy "
        "no longer needs the Stage-1 reflection loop at inference. This is the "
        "shift the conclusion claim asserts."
    ),
    prior=0.85
)
