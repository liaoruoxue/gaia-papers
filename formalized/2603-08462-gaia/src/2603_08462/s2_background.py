"""Section 2: Related Work and Background"""

from gaia.lang import claim, setting, support

from .motivation import (
    cot_prompting_def,
    budget_forcing_def,
    ib_markov_def,
    cot_cost_problem,
    budget_forcing_heuristic,
)

# --- Background settings ---

rlvr_def = setting(
    "Reinforcement Learning from Verifiable Rewards (RLVR) is a training paradigm for LLMs "
    "where the model is optimized using reinforcement learning with reward signals derived from "
    "verifiable correctness (e.g., whether the final answer is correct), rather than from human "
    "preferences. Examples include GRPO and PPO applied to math reasoning.",
    title="RLVR definition",
)

grpo_def = setting(
    "Group Relative Policy Optimization (GRPO) [@Shao2024] is a reinforcement learning algorithm "
    "for LLMs that estimates the baseline from a group of sampled outputs rather than a separate "
    "value model. Used here with group size 16.",
    title="GRPO definition",
)

# --- Claims from related work ---

length_penalty_limitation = claim(
    "Existing length-penalized training methods such as L1 [@Aggarwal2025] apply a penalty "
    "proportional to raw token count. These methods achieve token reduction but treat all tokens "
    "as equally costly regardless of their semantic contribution to the answer, leading to "
    "suboptimal accuracy-efficiency trade-offs.",
    title="Token-count length penalties are semantically blind",
    background=[budget_forcing_def],
    metadata={"source_section": "Section 2.1"},
)

ib_prior_use_in_llms = claim(
    "Prior work has applied Information Bottleneck theory to LLM representation learning and "
    "compression, but standard IB was not used to directly optimize the reasoning trace "
    "generation process under the constraint of transformer attention architecture.",
    title="Prior IB applications to LLMs did not address reasoning trace compression",
    background=[ib_markov_def],
    metadata={"source_section": "Section 2.2"},
)

strat_length_limitation = support(
    [cot_cost_problem, budget_forcing_heuristic],
    length_penalty_limitation,
    reason=(
        "@cot_cost_problem establishes that CoT increases token cost, motivating compression. "
        "@budget_forcing_heuristic establishes that existing methods apply flat token-count taxes. "
        "Together these support @length_penalty_limitation: the specific existing approach (L1) "
        "fails because it cannot distinguish token semantic value."
    ),
    prior=0.88,
)

strat_ib_gap = support(
    [cot_cost_problem],
    ib_prior_use_in_llms,
    reason=(
        "@cot_cost_problem motivates finding principled approaches to reasoning compression. "
        "Despite IB theory being applied to LLMs in other contexts, the gap identified in "
        "@ib_prior_use_in_llms — that standard IB was never applied to CoT generation "
        "optimization under transformer constraints — is the theoretical gap this paper fills."
    ),
    prior=0.82,
)
