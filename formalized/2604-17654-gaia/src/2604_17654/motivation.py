"""
Introduction: Motivation for Polychromic Exploratory Policy Optimization (Poly-EPO).

Exploration is identified as a cornerstone of learning from experience for language
model post-training. Standard RL fine-tuning collapses generation diversity; this work
proposes a principled set-RL approach to address this collapse [@OrneHamid2026].
"""

from gaia.lang import claim, setting, question, support, deduction, contradiction

# ──────────────────────────────────────────────────────────────────────
# Background settings
# ──────────────────────────────────────────────────────────────────────

rl_diversity_collapse = claim(
    "Reinforcement learning (RL) fine-tuning of language models (LMs) rapidly collapses "
    "the diversity of model generations onto a narrow set of high-reward behaviors, even "
    "though pretrained base models exhibit high initial diversity [@YCL25; @CZC25].",
    title="RL diversity collapse",
)

exploration_roles = setting(
    "Exploration serves three roles in learning from experience: "
    "(1) it is necessary to discover successful strategies for complex problems (e.g., finding a valid proof technique); "
    "(2) it enables generalization by building a diverse repertoire of strategies (e.g., multiple chess openings); "
    "(3) it is essential for scaling test-time compute methods such as majority voting, aggregation, and search, "
    "whose effectiveness depends on diversity in model generations [@OrneHamid2026].",
    title="Three roles of exploration",
)

standard_rl_limitation = claim(
    "Standard RL algorithms for language model post-training, such as PPO (Proximal Policy Optimization) "
    "[@SWD17] and GRPO (Group Relative Policy Optimization) [@SWZ24], do not explicitly incentivize "
    "the optimistic exploration required to master diverse reasoning paths [@OrneHamid2026].",
    title="Standard RL exploration limitation",
)

reward_shaping_limitation = claim(
    "Prior work addresses exploration via reward shaping — augmenting the canonical task reward $r(x,y)$ "
    "with a weighted exploration bonus $\\lambda d(x,y)$, solving "
    "$\\max_\\theta \\mathbb{E}_{y \\sim \\pi_\\theta(\\cdot|x)}[r(x,y) + \\lambda d(x,y)]$. "
    "This formulation treats exploitation and exploration as separate objectives: "
    "a generation can receive high learning signal by being reward-maximizing OR by being exploratory, "
    "without regard to achieving these goals synergistically. "
    "The method depends on careful tuning or adaptive scheduling of $\\lambda$ [@OrneHamid2026].",
    title="Reward shaping limitation",
)

# ──────────────────────────────────────────────────────────────────────
# Desiderata
# ──────────────────────────────────────────────────────────────────────

desideratum_optimism = setting(
    "Desideratum 1 — Optimism under uncertainty: An effective algorithm should assign a positive "
    "learning signal to trajectories that attempt novel reasoning strategies even when those strategies "
    "have not yet yielded high reward. This ensures the policy continues to explore promising strategies "
    "and broaden its capabilities during training (e.g., a dynamic programming approach should be "
    "reinforced even if early implementations fail unit tests) [@OrneHamid2026].",
    title="Desideratum 1: Optimism",
)

desideratum_synergy = setting(
    "Desideratum 2 — Exploration-exploitation synergy: The learning signal for each generation should "
    "depend on whether that generation helps the model jointly achieve high task performance and explore "
    "diverse strategies, enabling the model to learn through optimization to balance these goals "
    "[@OrneHamid2026].",
    title="Desideratum 2: Synergy",
)

desideratum_scalability = setting(
    "Desideratum 3 — Scalability: The algorithm's sample complexity and computational complexity "
    "should not be a significant overhead for large-scale LM post-training [@OrneHamid2026].",
    title="Desideratum 3: Scalability",
)

# ──────────────────────────────────────────────────────────────────────
# Research question and core claims
# ──────────────────────────────────────────────────────────────────────

rq_exploration = question(
    "How can we post-train language models to explicitly encourage optimistic exploration and "
    "promote synergy between exploration and exploitation, while remaining scalable?",
    title="Research question",
)

set_rl_scalable = claim(
    "Set reinforcement learning (set RL) [@HOX26] provides a principled and scalable approach "
    "to balance exploration and exploitation in LM post-training. While the original set RL "
    "framework [@HOX26] uses a learned critic and vine sampling that is computationally heavy, "
    "this paper shows how to instantiate it scalably for LM post-training by adapting standard "
    "RL algorithms through a modification to the advantage computation [@OrneHamid2026].",
    title="Set RL as scalable solution",
)

poly_epo_claim = claim(
    "Polychromic Exploratory Policy Optimization (Poly-EPO) is a set-RL algorithm that: "
    "(1) improves generalization by achieving higher pass@$k$ coverage (gains of up to 20% on "
    "mathematical reasoning test sets compared to GRPO); "
    "(2) preserves greater diversity in model generations as measured by reasoning-strategy clusters; "
    "(3) scales more effectively with test-time compute under majority voting [@OrneHamid2026].",
    title="Poly-EPO core claim",
)

# ──────────────────────────────────────────────────────────────────────
# Reasoning connections
# ──────────────────────────────────────────────────────────────────────

strat_need_for_algo = support(
    [rl_diversity_collapse, standard_rl_limitation, reward_shaping_limitation],
    set_rl_scalable,
    reason=(
        "Because RL fine-tuning collapses diversity (@rl_diversity_collapse), standard algorithms "
        "lack explicit exploration incentives (@standard_rl_limitation), and reward shaping treats "
        "exploration and exploitation as separate objectives requiring careful $\\lambda$ tuning "
        "(@reward_shaping_limitation), a fundamentally different approach is needed. Set RL addresses "
        "all three issues simultaneously: it assigns rewards at the set level, coupling exploration "
        "and exploitation intrinsically, and the scalable recipe avoids vine sampling."
    ),
    prior=0.9,
)

__all__ = [
    "rl_diversity_collapse",
    "exploration_roles",
    "standard_rl_limitation",
    "reward_shaping_limitation",
    "desideratum_optimism",
    "desideratum_synergy",
    "desideratum_scalability",
    "rq_exploration",
    "set_rl_scalable",
    "poly_epo_claim",
]
