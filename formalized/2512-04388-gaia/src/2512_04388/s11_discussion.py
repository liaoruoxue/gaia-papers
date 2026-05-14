"""Section 6: Discussion and Extensions -- the high-level synthesis of the
paper's contributions, the broader meta-agent thesis, and the proposed
future direction of beyond-LLM workers.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 6, p. 10.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Discussion synthesis (Section 6, paragraph 1)
# ---------------------------------------------------------------------------

claim_discussion_synthesis = claim(
    "**Section 6 synthesis.** The Conductor is a new language model "
    "trained with reinforcement learning to push the boundaries of "
    "frontier LLMs through (a) **collective intelligence** and "
    "(b) **automated prompt engineering**. By dividing problems, "
    "delegating subtasks, and designing communication topologies, the "
    "7B Conductor attains state-of-the-art performance across a diverse "
    "set of competitive benchmarks, going well beyond manually-designed "
    "agentic pipelines and expensive multi-agent baselines. The "
    "framework can be easily extended via finetuning to (i) specify "
    "customized agent sets and (ii) unlock recursive test-time scaling.",
    title="Section 6 synthesis: 7B Conductor = collective intelligence + automated prompt engineering + extensions",
)

# ---------------------------------------------------------------------------
# Broader meta-agent thesis (Section 6, paragraph 2)
# ---------------------------------------------------------------------------

claim_meta_agent_thesis = claim(
    "**Broader meta-agent thesis.** The work incentivizes future efforts "
    "in using language models themselves as **intelligent meta-agents**, "
    "flexibly harnessing the complementary capabilities of a broader set "
    "of models. The Conductor demonstrates that a small, specially-"
    "trained LM can serve as an effective meta-orchestrator of much "
    "larger and more diverse worker models -- shifting the design point "
    "from 'one giant model' to 'a smart coordinator + specialized "
    "workers'.",
    title="Broader thesis: LLMs as intelligent meta-agents -- shift from 'giant single model' to 'coordinator + workers'",
)

# ---------------------------------------------------------------------------
# Future directions (Section 6, paragraph 3)
# ---------------------------------------------------------------------------

claim_future_beyond_llms = claim(
    "**Future direction: beyond-LLM workers.** An exciting unexplored "
    "extension is to **go beyond LLMs alone**, introducing workers with "
    "expertise in other modalities such as **AlphaFold-style protein "
    "structure prediction** [@Jumper2021AlphaFold] and "
    "**vision-language-action models** for robotics [@Intelligence2025Pi05]. "
    "Natural language can serve as an expressive unifying interface "
    "across these heterogeneous workers, allowing the Conductor to "
    "tackle ambitious human challenges in fields such as biology, "
    "robotics, and beyond.",
    title="Future direction: beyond-LLM workers via natural language as unifying interface (biology, robotics)",
)

# ---------------------------------------------------------------------------
# Ethics + reproducibility (Section 6)
# ---------------------------------------------------------------------------

claim_ethics_economic_divide = claim(
    "**Ethics caveat: reliance on expensive language models may widen the "
    "economic divide.** While the paper foresees no issues regarding "
    "fairness, privacy, or security beyond broader considerations for "
    "the field, it notes that the **reliance of the method on expensive "
    "(closed-source frontier) language models might further exacerbate "
    "the economic divide and barriers posed by AI**. The dynamic-pool "
    "finetuning extension (Section 3.2) partially mitigates this by "
    "enabling strong performance over open-source-only worker pools.",
    title="Ethics: reliance on expensive frontier LLMs may widen economic divide (partially mitigated by open-pool generalization)",
)

claim_reproducibility = claim(
    "**Reproducibility statement.** Full details of the experimental "
    "setup -- datasets, model specifications, training regime, "
    "evaluation protocol -- are provided in Appendix A and E "
    "[@Nielsen2026Conductor]. The base model (Qwen2.5-7B) and all "
    "datasets used are publicly available. The Conductor prompt "
    "template (Fig. 13), recursion prompt (Fig. 14), and few-shot "
    "examples (Figs. 16-17) are all reported verbatim in the paper.",
    title="Reproducibility: base model + datasets public; full prompt template + few-shot examples in paper appendix",
)

__all__ = [
    "claim_discussion_synthesis",
    "claim_meta_agent_thesis",
    "claim_future_beyond_llms",
    "claim_ethics_economic_divide",
    "claim_reproducibility",
]
