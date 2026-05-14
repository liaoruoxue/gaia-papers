"""Section 3.2: Extending the RL Conductor -- adaptive worker selection
via randomized-pool finetuning and recursive topologies as a test-time
scaling axis.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 3.2, p. 4-5.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Extension 1: Adaptive Worker Selection
# ---------------------------------------------------------------------------

setup_dynamic_pool_protocol = setting(
    "**Randomized-pool finetuning protocol.** A pretrained Conductor is "
    "finetuned with a small subset of training questions where, for each "
    "question, the available pool is restricted to a **randomly sampled "
    "$k$-model subset** from the larger total pool of $n$ workers. The "
    "Conductor's input instructions are modified accordingly. No new "
    "data is collected; the finetune reuses already-seen training "
    "questions.",
    title="Setup: randomized k-of-n pool finetuning protocol (no new data needed)",
)

claim_dynamic_pool_design_aim = claim(
    "**Design goal of dynamic worker selection.** Restricting the pool "
    "per question makes the Conductor **robust to variation in the "
    "available worker pool** at test time. After finetuning, the "
    "Conductor generalizes to extract strong performance over any "
    "user-specified subset $k \\leq n$, catering to user constraints "
    "such as cost preferences and API availability. This extension "
    "drives flexible coordination -- the Conductor learns to reconfigure "
    "problem breakdowns based on the varying synergies of arbitrary "
    "agent sets.",
    title="Design goal: generalize to arbitrary user-specified subsets of workers",
)

# ---------------------------------------------------------------------------
# Extension 2: Recursive topologies as test-time scaling
# ---------------------------------------------------------------------------

setup_recursive_finetuning_protocol = setting(
    "**Recursive-Conductor finetuning protocol.** A pretrained Conductor "
    "is finetuned for **20 iterations** on a **350-sample filtered "
    "subset** of the training dataset (175 LiveCodeBench + 175 RLPR "
    "questions). For half the samples in each batch, a single recursion "
    "call is manually instantiated, exposing the Conductor to its own "
    "previous coordination strategy as input. The training continues "
    "with 64 rollouts per sample (batch size 256), no reference-model "
    "synchronization, no KL divergence penalty, and a discount factor "
    "of 0.25 scaling the rewards of the initial non-recursive round "
    "(rewards normalized across rounds).",
    title="Setup: recursive finetuning -- 20 iters, 350 samples, half-batch recursion, discount=0.25",
)

claim_recursive_scaling_aim = claim(
    "**Design goal of recursive topologies.** Allowing recursive calls "
    "after the initial root Conductor call creates a tunable test-time "
    "**recursion depth** -- a new form of test-time scaling beyond "
    "open-ended chain-of-thought. Each recursive invocation re-runs the "
    "Conductor with broader context (parent strategy + previous "
    "response), giving it the chance to **adaptively revise or extend** "
    "its initial coordination strategy on the fly. Recursion thus "
    "becomes a tunable compute axis controlling test-time effort.",
    title="Design goal: recursive depth as a new test-time scaling axis (beyond open-ended CoT)",
)

claim_recursion_decision_protocol = claim(
    "**Recursion decision protocol.** When recursion is enabled, after "
    "viewing the final worker response of its previous strategy, the "
    "Conductor either (a) returns the response unchanged (by emitting "
    "three empty lists `model_id=[]`, `subtasks=[]`, `access_list=[]`) "
    "if it deems the response correct, or (b) devises a new sequence of "
    "routing steps to verify or revise the previous response. This "
    "decision is made by the Conductor itself based on the previous "
    "final routing message, which is included in the new agentic "
    "workflow's context via the `access_list` `\"all\"` token.",
    title="Claim: recursion decision -- Conductor self-selects between (return as-is) and (instantiate revision workflow)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Figs. 21-22",
        "caption": "Figs. 21-22: example recursive completions -- one passing through and one instantiating verification.",
    },
)

# ---------------------------------------------------------------------------
# Note on cost-mitigation strategy for recursion experiments
# ---------------------------------------------------------------------------

claim_recursion_cost_cap = claim(
    "**Recursion cost cap in the paper's experiments.** To mitigate "
    "additional inference cost, the recursive variant evaluated in "
    "Section 4.4 uses **less than $2\\times$** the number of original "
    "agentic calls of the non-recursive Conductor. This deliberately "
    "leaves room for further improvement -- larger recursion budgets "
    "would likely yield further gains -- but bounds the experimental "
    "comparison to a fair efficiency-vs-performance tradeoff.",
    title="Claim: recursion experiments use less than 2x non-recursive agentic calls (room for further scaling)",
)

__all__ = [
    "setup_dynamic_pool_protocol",
    "claim_dynamic_pool_design_aim",
    "setup_recursive_finetuning_protocol",
    "claim_recursive_scaling_aim",
    "claim_recursion_decision_protocol",
    "claim_recursion_cost_cap",
]
