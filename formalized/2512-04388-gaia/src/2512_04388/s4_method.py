"""Section 3 (cont.): Method details that flesh out the Conductor framework
beyond the formal setup of Section 3.1 -- few-shot conditioning, training
acceleration, the emergent prompt-engineering / topology-design / refinement
behaviors.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 3.1 narrative
+ Appendix B.2 / B.7 evidence anchored back to the method.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Method components beyond Section 3.1 formal setup
# ---------------------------------------------------------------------------

setup_few_shot_conditioning = setting(
    "**Few-shot conditioning of the Conductor.** To accelerate learning "
    "and make the framework compatible with arbitrary base models, the "
    "Conductor's system prompt provides detailed instructions alongside "
    "**few-shot examples** of expected output format. Specifically, the "
    "prompt includes 4 example workflows drawn from training-related "
    "task corpora (MATH500, MMLU, RLPR, LiveCodeBench, MedReason "
    "[@Wu2025MedReason], DeepMath [@He2025DeepMath], Countdown "
    "[@Pan2025AdaptiveParallel]) to condition the generative "
    "distribution of the pretrained base model on the orchestration "
    "task. The few-shot examples are real Conductor completions taken "
    "from coldstart training runs.",
    title="Setup: few-shot examples in system prompt condition base-model generative distribution",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 13 + Figs. 16/17",
        "caption": "Fig. 13: Conductor prompt template. Figs. 16/17: in-distribution and out-of-distribution few-shot examples.",
    },
)

setup_ordinal_model_names = setting(
    "**Ordinal model naming in the Conductor prompt.** Available language "
    "models are passed to the Conductor as purely **ordinal numbers** "
    "(`Model 0`, `Model 1`, ..., `Model k`) rather than by their known "
    "names. The motivation is to fully encourage exploration of the "
    "possible models in the pool without bias from prior associations "
    "with known model identities.",
    title="Setup: ordinal model naming (Model 0..k) eliminates prior-association bias",
)

setup_recursion_definition = setting(
    "**Recursive call definition.** A recursive workflow allows the "
    "Conductor to call itself. In each *inner recursive call*, the "
    "Conductor receives as additional context (i) its own *parent* "
    "output (the previous coordination strategy) and (ii) the previous "
    "agent's response. The Conductor then either (a) instantiates a new "
    "workflow refining/correcting the previous result, or (b) returns "
    "the previous response directly by emitting three empty lists. "
    "Infinite recursion is avoided by a hard cap on the maximum number "
    "of recursive calls after the initial root Conductor call.",
    title="Setup: recursive call -- parent output + previous response as additional input; capped depth",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 14",
        "caption": "Fig. 14: The recursive prompt allowing self-referential coordination after viewing the previous coordination strategy outcome.",
    },
)

# ---------------------------------------------------------------------------
# Method-level claims (Section 3 + Section 4.5 + Appendix B.7 about method)
# ---------------------------------------------------------------------------

claim_exploration_sidestep = claim(
    "**Method observation: powerful workers sidestep small-model "
    "exploration problems.** By relying on a powerful set of workers, "
    "the framework empirically sidesteps the canonical exploration "
    "problem faced by other small models trained with RL "
    "[@Cetin2025RLT]: the 7B Conductor reaches convergence with AdamW "
    "[@Loshchilov2017AdamW] in **only 200 GRPO iterations**, with a "
    "small batch size of 256 samples, **without any KL regularization**, "
    "and **without reference-model synchronization**.",
    title="Method observation: powerful workers eliminate exploration bottleneck; convergence in 200 iters w/o KL reg",
)

claim_emergent_prompt_engineering = claim(
    "**Emergent skill: focused prompt-engineering.** As GRPO training "
    "progresses, the trained Conductor produces problem breakdowns and "
    "prompt-engineered subtasks that **match the strengths of each "
    "worker** -- e.g., using Gemini 2.5 Pro and Claude Sonnet 4 as "
    "high-level planners and reserving GPT-5 for final code optimization "
    "on LiveCodeBench. This emergent prompt-engineering capability "
    "scales with the Conductor's own size: a 3B variant converges to "
    "the same agent-selection distribution as the 7B variant but the "
    "7B variant produces qualitatively superior subtask instructions.",
    title="Emergent skill: focused prompt-engineering, scales with Conductor size (Fig. 7)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 7",
        "caption": "Fig. 7: Conductor scale -- the 3B Conductor still learns optimal agent selection, but the 7B Conductor generates additional performance gains through improved prompt engineering.",
    },
)

claim_emergent_topology_design = claim(
    "**Emergent skill: targeted communication topology design.** The "
    "Conductor learns to compose communication topologies adapted to "
    "each input -- combining **independent attempts with final debate "
    "rounds**, tree topologies for problems with independently solvable "
    "subparts, and chain topologies for tightly coupled reasoning. "
    "Categorized modes include: (i) sequential coordination with "
    "planner-executor-checker, (ii) tree coordination with parallel "
    "workers + aggregator, (iii) tree coordination for pure factual "
    "recall (no agent-to-agent collaboration), (iv) sequential logical "
    "reasoning, and (v) **Conductor task abdication** (passing the "
    "subtask-design role to a powerful worker like Gemini 2.5 Pro).",
    title="Emergent skill: targeted topology design -- chain / tree / independent-then-aggregate / abdication modes",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Figs. 19-28",
        "caption": "Appendix F: example Conductor completions illustrating tree, sequential, factual-recall, and abdication topologies.",
    },
)

claim_emergent_task_adaptivity = claim(
    "**Emergent skill: task and difficulty adaptivity.** The trained "
    "Conductor **dynamically allocates more compute to harder problems** "
    "by specifying agentic workflows with an increased number of steps. "
    "For complex LiveCodeBench code generation, workflows typically "
    "deploy multiple planning steps followed by implementation and "
    "verification (3-4 agents). For simpler MMLU multiple-choice "
    "factual-recall problems, workflows typically use only 1-2 steps "
    "of targeted information retrieval. The model explicitly reasons "
    "about task complexity in its chain-of-thought before specifying "
    "its workflow.",
    title="Emergent skill: dynamic per-task workflow-length allocation (Fig. 8)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 8",
        "caption": "Fig. 8: Task adaptivity -- workflow step distribution for MMLU (mostly 2 agents) vs LiveCodeBench (3-4 agents).",
    },
)

claim_meta_orchestrator_thesis = claim(
    "**Method thesis: the Conductor is a meta-orchestrator.** The "
    "Conductor's design and learned behavior establish it as a new kind "
    "of **meta-agent** -- a model whose role is not to solve tasks "
    "directly but to coordinate other models. The natural-language "
    "medium gives the Conductor an unrestricted instruction surface "
    "over its workers; end-to-end RL gives it the credit-assignment "
    "machinery to learn what instructions and topologies serve which "
    "worker on which problem.",
    title="Method thesis: the Conductor is a learned meta-orchestrator over LLM workers",
)

__all__ = [
    "setup_few_shot_conditioning",
    "setup_ordinal_model_names",
    "setup_recursion_definition",
    "claim_exploration_sidestep",
    "claim_emergent_prompt_engineering",
    "claim_emergent_topology_design",
    "claim_emergent_task_adaptivity",
    "claim_meta_orchestrator_thesis",
]
