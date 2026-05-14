"""Section 3.1: Framing Agent Coordination in Natural Language -- formal
definition of an agentic workflow, Conductor output structure, workflow
execution, learning dynamics.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 3.1, p. 3-4.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Formal definitions
# ---------------------------------------------------------------------------

setup_conductor_task = setting(
    "**The Conductor task.** The Conductor's objective is to solve tasks "
    "*indirectly* by designing agentic workflows specific to each input "
    "question $q_i$. The final output of the workflow is returned as the "
    "Conductor's response $o_i$.",
    title="Setup: Conductor task -- solve q_i indirectly via designing workflows",
)

setup_workflow_definition = setting(
    "**Formal workflow definition.** Each *agentic workflow* is defined "
    "as a sequence of **workflow steps**. Each step specifies three "
    "components:\n\n"
    "1. A **subtask** -- a natural-language string describing what should "
    "be done at this step.\n"
    "2. An **assigned worker agent** -- an integer index referencing the "
    "worker LLM responsible for executing that subtask.\n"
    "3. An **access list** -- a list of indices specifying which previous "
    "subtask solutions should be included in the worker's context (or "
    "the special string `\"all\"` for full visibility, or an empty list "
    "for no visibility).\n\n"
    "The information is parsed from the Conductor's response (after its "
    "chain-of-thought) as three Python lists -- `model_id`, `subtasks`, "
    "`access_list` -- with the same number of entries.",
    title="Setup: agentic workflow = ordered tuples (subtask string, worker id, access list)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 2 + Fig. 13",
        "caption": "Fig. 2: Conductor output structure with parseable Python lists. Fig. 13: Conductor prompt specifying the required output format.",
    },
)

setup_topology_expressivity = setting(
    "**Expressivity of natural-language workflow specification.** Because "
    "the Conductor outputs three lists in natural language with arbitrary "
    "access patterns, the workflow space includes simple best-of-$N$, "
    "sequential chain-like topologies, and **parallelizable arbitrary "
    "tree-structured approaches**. This expressivity strictly exceeds "
    "that of prior routers that select from a pre-specified topology "
    "vocabulary [@Yue2025MASRouter; @Chen2024RouterDC; @Guha2024Smoothie].",
    title="Setup: workflow space includes best-of-N + chain + arbitrary tree topologies (vs fixed-vocabulary routers)",
)

setup_workflow_execution = setting(
    "**Workflow execution semantics.** Each workflow is executed "
    "sequentially: the specified worker agents are prompted with their "
    "assigned natural-language subtask in order. In each step, the "
    "worker's context includes the sequence of previous subtasks and "
    "corresponding responses defined in its access list, provided as "
    "past messages in a conversational template. The final worker's "
    "response is returned to the user as the workflow's overall output.",
    title="Setup: workflow execution -- workers run in order, access list controls context visibility",
)

# ---------------------------------------------------------------------------
# Conductor reward (analogous to RL-reasoning reward but adapted)
# ---------------------------------------------------------------------------

setup_conductor_reward = setting(
    "**Conductor reward.** Analogously to the RL reasoning paradigm "
    "(Section 2), the reward $r_i$ for each Conductor response is "
    "determined by two progressive conditions:\n\n"
    "1. **Conductor format condition** -- $r_i = 0$ for responses from "
    "which the three Python lists (`subtasks`, `model_id`, "
    "`access_list`) cannot be parsed.\n"
    "2. **Conductor correctness condition** -- $r_i = 1$ if the final "
    "output from executing a well-formatted workflow $o_i$ matches the "
    "gold solution $s_i$, and $r_i = 0.5$ otherwise (format-correct but "
    "answer-wrong).\n\n"
    "Note the reward range differs from Section 2's RL recipe "
    "(0 / 0.5 / 1) -- the Conductor reward is strictly non-negative, "
    "with a smaller incorrect-but-formatted bonus.",
    title="Setup: Conductor reward -- format=0; correct=1; correct-format-wrong-answer=0.5",
)

# ---------------------------------------------------------------------------
# Section 3.1 derived claims (about the framework)
# ---------------------------------------------------------------------------

claim_natural_language_medium = claim(
    "**Natural language as the workflow specification medium.** Because "
    "the Conductor's output is parsed as natural-language Python lists, "
    "the framework places **complete specification freedom** in the "
    "Conductor's hands: it can freely craft tailored subtasks and "
    "communication strategies across workers without any human-designed "
    "vocabulary or template. The framework is correspondingly "
    "**inherently more expressive** than prior routing approaches that "
    "select pre-specified options.",
    title="Claim: natural-language medium gives complete specification freedom (more expressive than routing)",
)

claim_grpo_emergent_strategies = claim(
    "**End-to-end GRPO training induces emergent coordination strategies.** "
    "Training the Conductor with the GRPO recipe from Section 2 (using "
    "the Conductor reward) yields, *during training*, the **emergence** of "
    "problem breakdowns and prompt-engineered subtasks that match the "
    "strengths of each worker, together with communication strategies "
    "that combine independent attempts with final debate rounds. Early "
    "in training the Conductor issues sound but minimally collaborative "
    "subtasks; near convergence it learns to use planners, issue targeted "
    "instructions, instruct workers to share reasoning, and leverage "
    "verification and refinement.",
    title="Claim: emergent coordination strategies appear over GRPO training (Fig. 3)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 3",
        "caption": "Fig. 3: Emergence of powerful coordination strategies over training. Left: training-set accuracy of 7B Conductor surpasses all individual workers. Right: example early vs late workflows.",
    },
)

claim_compatible_any_rl_algo = claim(
    "**RL-algorithm agnosticism.** Training the Conductor with the "
    "Conductor reward is inherently **compatible with any RL algorithm** "
    "(PPO [@Schulman2017PPO], REINFORCE-style methods "
    "[@Ahmadian2024Back], or GRPO [@Shao2024DeepSeekMath]); the paper "
    "employs the GRPO formulation described in Section 2 for "
    "concreteness.",
    title="Claim: Conductor framework is RL-algorithm-agnostic; the paper uses GRPO",
)

__all__ = [
    "setup_conductor_task",
    "setup_workflow_definition",
    "setup_topology_expressivity",
    "setup_workflow_execution",
    "setup_conductor_reward",
    "claim_natural_language_medium",
    "claim_grpo_emergent_strategies",
    "claim_compatible_any_rl_algo",
]
