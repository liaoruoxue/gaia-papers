"""Introduction and Motivation for ABBEL: belief-bottleneck framework for LLM agents."""

from gaia.lang import claim, question, setting, support

# --- Setup and background ---

q_long_context = question(
    "How can an LLM agent maintain an effective context for long-horizon "
    "sequential decision-making tasks without keeping the entire interaction "
    "history (which exceeds practical context limits)?",
    title="Long-horizon context management question",
)

problem_long_horizon_context = claim(
    "Modern AI agents performing tasks like software development or scientific "
    "research take hundreds or thousands of interaction steps with their "
    "environment, often exceeding the practical context limits of even frontier "
    "language models. This necessitates compressing interaction histories while "
    "preserving information needed for effective decision-making.",
    title="Long interaction histories exceed practical LLM context limits",
)

bg_minimal_sufficient_statistics = setting(
    "Work on minimal sufficient statistics for sequential decision-making dates "
    "back to Aastrom (1965) [@Astrom1965], which used probability distributions "
    "over unknown variables (recursive Bayesian estimation) to compress histories.",
    title="Recursive Bayesian estimation as minimal sufficient statistic",
)

# --- Two enabling observations from prior work ---

natural_language_belief_capability = claim(
    "Recent work shows that large language models can accurately update natural "
    "language descriptions of beliefs when given new observations [@Arumugam2025], "
    "demonstrating that LLMs can serve as inexact-but-flexible belief updaters "
    "where exact probability distributions are unavailable.",
    title="LLMs can update natural-language belief states",
)

belief_prompting_helps = claim(
    "Prompting language agents to explicitly generate a belief about the current "
    "state before acting has been shown to enhance their performance on multi-step "
    "decision tasks [@Kim2025].",
    title="Explicit belief prompting improves agent performance",
)

# --- Research opportunity (premise of the proposal) ---

opportunity_belief_compression = claim(
    "Compressing an interaction history into a posterior belief over task-relevant "
    "variables could, in principle, limit the growth of context length without "
    "harming performance, because such a belief is a sufficient statistic for "
    "decision-making in partially observable settings.",
    title="Belief-state compression is a viable context-management strategy",
)

strat_opportunity = support(
    [problem_long_horizon_context, natural_language_belief_capability, belief_prompting_helps],
    opportunity_belief_compression,
    reason=(
        "The combination of (i) the practical context-length pressure created by "
        "long-horizon tasks (@problem_long_horizon_context), (ii) prior evidence "
        "that LLMs can update natural-language beliefs (@natural_language_belief_capability), "
        "and (iii) prior evidence that explicit belief prompting helps action selection "
        "(@belief_prompting_helps) jointly motivate compressing the interaction history "
        "into a natural-language belief state as a viable bottleneck."
    ),
    prior=0.85,
    background=[bg_minimal_sufficient_statistics],
)

# --- The proposed framework (high-level claim) ---

abbel_proposal = claim(
    "ABBEL (Acting through Belief Bottlenecks Expressed in Language) is a "
    "framework where an LLM agent (i) updates a natural-language belief state "
    "given the latest observation and (ii) selects the next action conditioned "
    "*only* on that belief, with the full interaction history excluded from the "
    "action-selection context. This creates an information bottleneck designed "
    "to preserve sufficient task-relevant information while keeping context "
    "compact and human-interpretable.",
    title="ABBEL framework definition",
)

# --- Key empirical findings, stated upfront in introduction ---

finding_belief_grows_slower = claim(
    "Across the six evaluated multi-step environments, ABBEL-generated belief "
    "states are human-understandable and grow much more slowly than the full "
    "interaction history, even decreasing in some environments as possibilities "
    "are ruled out, while interaction history grows linearly with the number of "
    "steps.",
    title="ABBEL beliefs grow much slower than full history",
)

finding_failure_modes = claim(
    "ABBEL agents (without RL fine-tuning) exhibit characteristic failure modes: "
    "(a) propagating erroneous beliefs across steps, (b) hallucinating false "
    "memories of previous steps, and (c) repeating uninformative actions because "
    "the belief does not change without new information. These failures cause "
    "ABBEL to underperform the full-context (VANILLA) baseline in some "
    "environments for some models.",
    title="ABBEL prompting-only failure modes",
)

finding_rl_helps = claim(
    "Reinforcement-learning fine-tuning of an LLM agent under the ABBEL framework "
    "(with belief grading or belief length penalty rewards) lets ABBEL match or "
    "exceed full-context baselines while using significantly less memory, across "
    "Combination Lock, multi-objective question answering, and ColBench.",
    title="RL fine-tuning closes/exceeds the ABBEL gap",
)

__all__ = [
    "q_long_context",
    "problem_long_horizon_context",
    "bg_minimal_sufficient_statistics",
    "natural_language_belief_capability",
    "belief_prompting_helps",
    "opportunity_belief_compression",
    "abbel_proposal",
    "finding_belief_grows_slower",
    "finding_failure_modes",
    "finding_rl_helps",
    "strat_opportunity",
]
