"""Introduction and Motivation: Why LLM Optimization Performance Varies"""

from gaia.lang import claim, setting, question

# ── Research context ────────────────────────────────────────────────────────

llm_as_search_operators = setting(
    "Large language models (LLMs) are increasingly deployed as search operators in "
    "iterative optimization systems. In such workflows, LLMs are embedded into "
    "evolutionary or agentic loops as black-box optimizers: they repeatedly propose "
    "candidate solutions, receive fitness feedback, and iteratively refine solutions. "
    "This paradigm has been applied to prompt optimization, symbolic regression, "
    "combinatorial optimization, and scientific discovery.",
    title="LLMs as evolutionary search operators",
)

exploration_exploitation_classical = setting(
    "In classical evolutionary algorithms, the exploration–exploitation trade-off is "
    "managed via stochastic mutation and crossover operators. Novelty (distance to "
    "prior solutions) is treated as a proxy for exploration. Higher novelty in "
    "classical settings typically indicates broader coverage of the search space, "
    "which should improve long-horizon optimization. In meta-heuristics, large "
    "breakthroughs occur at rare intervals, followed by long plateaus or small "
    "refinements [@Mitchell1999].",
    title="Classical evolutionary exploration–exploitation paradigm",
)

llm_mutation_differs = setting(
    "In LLM-driven metaheuristics, the mutation operator is no longer fully random "
    "but is strongly shaped by the LLM's prior toward producing improved solutions "
    "conditioned on parent candidates and their fitness feedback. Consequently, "
    "exploration is more structured and constrained than in classical, non-LLM-driven "
    "evolution—LLMs generate semantically meaningful variations rather than random "
    "perturbations.",
    title="LLM mutation differs from classical stochastic mutation",
)

# ── Research question ───────────────────────────────────────────────────────

rq_what_makes_good_optimizer = question(
    "What explains large model-to-model differences in LLM optimization performance? "
    "Are these differences primarily a reflection of base model capability, or do "
    "they arise from more subtle differences in the exploration–exploitation dynamics "
    "induced by the models?",
    title="Central research question",
)

# ── Core observation motivating the study ──────────────────────────────────

optimization_gap_exists = claim(
    "Under identical evolutionary conditions (fixed selection rules, evaluation "
    "functions, population initialization, and budget of 30 generations × 10 "
    "offspring per generation), different LLMs exhibit vastly different optimization "
    "trajectories and final performance. A pronounced optimization gap exists across "
    "the 15 tested LLMs on 8 tasks: e.g., GPT-4o achieves an average final fitness "
    "of 77.4 vs. GPT-3.5-turbo at 59.3 (Table 2, normalized fitness scores). "
    "Strong early performance does not reliably predict long-horizon outcomes: "
    "Deepseek-V3 performs best in generation 1 (avg first-gen fitness 56.9) "
    "but fails to achieve the largest gains over time (final avg 75.3 vs. "
    "Mistral-24B-Instruct's 81.6).",
    title="Optimization gap between LLMs under identical conditions",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 2"},
)

novelty_not_sufficient_hypothesis = claim(
    "A natural hypothesis is that models generating more novel solutions explore "
    "the search space more effectively and should therefore achieve better "
    "optimization outcomes. Under the classical evolutionary view where novelty "
    "equals exploration, higher novelty should yield better long-horizon fitness.",
    title="Novelty-as-exploration hypothesis (to be tested)",
)

study_scope = claim(
    "The study conducts a large-scale controlled analysis of LLM-based evolutionary "
    "optimization, collecting optimization trajectories for 15 LLMs across 4 task "
    "families (8 tasks), resulting in over 72,000 analyzed candidate solutions "
    "(15 models × 8 tasks × 30 generations × 10 offspring per generation × 2 seeds).",
    title="Study scale: 15 LLMs, 8 tasks, 72K+ solutions",
)
