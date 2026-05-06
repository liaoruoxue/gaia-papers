"""Motivation: from one-task-one-agent black-box autoregressive reasoning to
a generalized goal-oriented agent that plans by simulation in an internal
world model.

Section 1 (Introduction) of Deng et al. 2025 [@Deng2025SIMURA].
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup: foundation-model-based AI agents
# ---------------------------------------------------------------------------

setup_fm_agents = setting(
    "**Foundation-model-based AI agents.** AI agents powered by foundation "
    "models -- Large Language Models (LLM) and Vision Language Models "
    "(VLM) -- have been deployed across web/computer automation "
    "[@Operator; @ProjectMariner; @WebArena; @OSWorld], internet research "
    "[@DeepResearch; @AnthropicComputerUse; @GeminiDeepResearch], social "
    "simulation [@GenerativeAgents], software development "
    "[@Cursor; @OpenHands], and scientific research "
    "[@AICoScientist; @AIScientistV2]. Each existing agent is a "
    "domain-specialized system; the per-task pipeline is the dominant "
    "design pattern.",
    title="Setup: foundation-model-based AI agents and their domain-specialized practice",
)

setup_autoregressive_reasoning_definition = setting(
    "**Definition of *autoregressive reasoning* used in this paper.** The "
    "paper uses 'autoregressive reasoning' to denote the procedural mode "
    "of decision-making that iteratively predicts the next abstract "
    "internal state $z_t$ (e.g., text or latent token) according to the "
    "conditional distribution $p(z_t \\mid z_{<t}, x)$ for input $x$, "
    "*without* explicit modeling or simulation of future outcomes. This "
    "is distinct from autoregressive modeling as a statistical or "
    "architectural property of language models. Reasoning LLMs trained "
    "via end-to-end RL (e.g., OpenAI o1 [@OpenAIo1], DeepSeek-R1 "
    "[@DeepSeekR1]) still operate procedurally in this autoregressive "
    "mode.",
    title="Setup: paper's definition of 'autoregressive reasoning' (procedural, no explicit future simulation)",
)

setup_human_mental_simulation = setting(
    "**Human cognitive baseline: planning by mental simulation.** "
    "Humans, using a single cognitive system, adapt to diverse tasks and "
    "environments not merely by linear reasoning but by *imagining "
    "potential outcomes, simulating possibilities using a mental world "
    "model, and planning accordingly* [@Ball2020; @LeCunWorldModel]. "
    "Hypothetical thinking and counterfactual evaluation are well-"
    "documented features of flexible goal-directed human behavior.",
    title="Setup: human cognitive baseline -- mental simulation in an internal world model",
)

# ---------------------------------------------------------------------------
# Central question motivating SIMURA
# ---------------------------------------------------------------------------

q_central = question(
    "**Central question.** Current AI-agent practice is one-task-one-"
    "agent: each system is tailored to a specific environment, with "
    "decisions produced token-by-token through black-box autoregressive "
    "reasoning that lacks an explicit mechanism for simulating and "
    "evaluating counterfactual futures. Humans plan flexibly by "
    "mentally simulating action consequences in an internal world "
    "model. **Can we design a single, generalized agentic-reasoning "
    "architecture -- derived from a principled formulation of the "
    "optimal goal-oriented agent in any general environment -- that "
    "augments autoregressive reasoning with world-model-based "
    "planning via simulation, and demonstrates measurable advantages "
    "over purely autoregressive baselines?**",
    title="Central question: a generalized world-model-driven simulative reasoning architecture for goal-oriented agents",
)

# ---------------------------------------------------------------------------
# Diagnosis: limits of one-task-one-agent and black-box autoregressive
# reasoning
# ---------------------------------------------------------------------------

claim_one_task_one_agent_limit = claim(
    "**Diagnosis: the one-task-one-agent paradigm lacks scalability and "
    "generality.** Existing foundation-model agents are released as "
    "task-specialized systems: web-automation agents "
    "[@Operator; @ProjectMariner; @OpenHands], internet-research "
    "agents [@DeepResearch; @GeminiDeepResearch], software-engineering "
    "agents [@Cursor; @OpenHands], scientific-research agents "
    "[@AICoScientist; @AIScientistV2], etc. Each architecture is "
    "tailored to its specific task domain, which limits scalability "
    "and transferability across tasks and environments.",
    title="Diagnosis: one-task-one-agent paradigm limits scalability and transferability",
)

claim_autoregressive_planning_limit = claim(
    "**Diagnosis: black-box autoregressive reasoning lacks explicit "
    "simulation and counterfactual evaluation.** Even reasoning LLMs "
    "trained via end-to-end RL [@OpenAIo1; @DeepSeekR1] -- which "
    "exhibit traces of emergent planning and longer-horizon control -- "
    "still produce decisions through token-by-token generation under "
    "$p(z_t \\mid z_{<t}, x)$. They lack an *explicit* mechanism for "
    "simulating and evaluating counterfactual futures. As a result, "
    "even strong models remain vulnerable to **locally myopic "
    "decisions** and **error accumulation over extended trajectories** "
    "[@Andreas2022; @ReAct].",
    title="Diagnosis: autoregressive reasoning has no explicit counterfactual simulation; suffers myopia and error accumulation",
)

# ---------------------------------------------------------------------------
# Proposal: SIMURA architecture
# ---------------------------------------------------------------------------

claim_simura_intro = claim(
    "**SIMURA: Simulative Reasoning Architecture.** The paper proposes "
    "SIMURA, a goal-oriented architecture for generalized agentic "
    "reasoning that addresses the limitations of black-box "
    "autoregressive reasoning by introducing a **world model** as the "
    "engine for planning via simulation. At each step, a **policy** "
    "module proposes a few candidate actions conditioned on agent "
    "identity and goal; a **world model** simulates the next belief "
    "state for each candidate; a **critic** module evaluates simulated "
    "outcomes against the goal; and the planner selects the best "
    "action sequence. To stay tractable, SIMURA reasons in a "
    "compact, semantically structured natural-language state space "
    "and uses a *hierarchical* action architecture that separates "
    "high-level simulated actions ($a'_t$) from low-level concrete "
    "actions ($a_t$).",
    title="Proposal: SIMURA = policy + world model + critic + hierarchical actor over natural-language belief states",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 4",
        "caption": "Fig. 4: design of SIMURA -- encoder, planner (policy + world model + critic), and actor.",
    },
)

claim_natural_language_substrate = claim(
    "**Natural-language belief-state and simulated-action substrate.** "
    "SIMURA represents the belief state $\\hat{s}_t$ and the simulated "
    "action $a'_t$ as **natural-language token sequences**, treating "
    "language as a *discrete*, *hierarchical*, concept-grounded latent "
    "space. The encoder, policy, world model, and critic operate on "
    "these natural-language representations; the lower-level actor "
    "translates the chosen simulated action $a'_t$ into the concrete "
    "action $a_t$ in the environment's specific action space. The "
    "design is **model-agnostic**: any LLM or VLM can in principle "
    "instantiate the modules.",
    title="Proposal: natural language is the discrete hierarchical state-and-action representation; design is model-agnostic",
)

# ---------------------------------------------------------------------------
# Headline empirical claims (introduced in abstract / Sec. 1)
# ---------------------------------------------------------------------------

claim_headline_flightqa = claim(
    "**Headline empirical claim: FlightQA 0% to 32.2%.** On the "
    "newly-introduced FlightQA dataset (complex flight-search website "
    "navigation, 90 questions with 3-8 constraints), SIMURA's full "
    "architecture (world-model planning) achieves **32.2% correct** "
    "responses, while the BrowsingAgent baseline from OpenHands "
    "[@OpenHands] -- a representative open-web autoregressive agent "
    "that generates chain-of-thought before each action -- achieves "
    "**0% correct** under the same gpt-4o backbone, BrowserGym "
    "environment, and 30-action budget.",
    title="Headline: FlightQA correct rate 0.0% (BrowsingAgent) to 32.2% (SIMURA full); same gpt-4o backbone",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 6 / Table 1",
        "caption": "Fig. 6 / Table 1: FlightQA performance summary -- 0% to 32.2% correct.",
    },
)

claim_headline_124_pct = claim(
    "**Headline empirical claim: world-model planning beats autoregressive "
    "planning by up to 124% in task-completion rate.** Under SIMURA's own "
    "modular pipeline (i.e., holding encoder / actor / memory fixed), "
    "swapping the planner from world-model-based simulation to "
    "autoregressive single-sample (commit-to-first) planning lowers task "
    "completion. The 124% figure is the maximum cross-task improvement: "
    "on FlightQA, SIMURA's world-model planner achieves a 32.2% correct "
    "rate vs 14.4% for autoregressive planning under the same gpt-4o "
    "backbone, i.e., $32.2 / 14.4 - 1 \\approx 1.236$, equivalent to a "
    "**124% relative improvement** ($p < 0.01$, pairwise t-test). The "
    "advantage is consistent across the three task families "
    "(FlightQA, FanOutQA, WebArena).",
    title="Headline: world-model planning beats autoregressive planning by up to 124% in task-completion rate",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 6 / Table 1",
        "caption": "Fig. 6 / Table 1: world-model vs autoregressive planning comparison; 32.2/14.4 - 1 ~ 124%.",
    },
)

claim_open_source_release = claim(
    "**Open-source release: REASONERAGENT-WEB.** The paper releases "
    "REASONERAGENT-WEB [@ReasonerAgent], an open-source web-browsing "
    "agent built on SIMURA, available via LLM-Reasoners "
    "[@LLMReasoners] as a research demo and reference implementation.",
    title="Headline: REASONERAGENT-WEB open-source research demo built on SIMURA",
)

# ---------------------------------------------------------------------------
# Stated contributions (paraphrased from Sec. 1)
# ---------------------------------------------------------------------------

claim_contributions = claim(
    "**Stated contributions of the paper.** "
    "(C1) **Diagnosis**: identifies one-task-one-agent practice and "
    "black-box autoregressive reasoning (no explicit simulation, no "
    "counterfactual evaluation) as the central limitations of current "
    "agent design. "
    "(C2) **Theoretical formulation**: derives a principled definition "
    "of the optimal goal-oriented agent in any general environment "
    "(value-function recursion + arg-max decision rule) and its world-"
    "model-augmented counterpart. "
    "(C3) **Architecture**: SIMURA -- a generalized simulative-reasoning "
    "architecture (encoder + policy + world model + critic + "
    "hierarchical actor) operating on natural-language belief states "
    "and simulated actions. "
    "(C4) **Prototype**: an LLM-based instantiation (REASONERAGENT-WEB) "
    "applied to web browsing, with all modules implemented as prompted "
    "LLM components and DFS/MCTS-based planning via LLM-Reasoners "
    "[@LLMReasoners]. "
    "(C5) **Benchmark**: FlightQA, a controllable flight-search dataset "
    "of 90 questions with 3-8 constraints supporting counterfactual "
    "analysis of constraint scaling. "
    "(C6) **Empirical**: FlightQA 0% to 32.2%; +124% relative gain over "
    "matched autoregressive planning; consistent gains across "
    "FanOutQA (+48.6%) and WebArena (+21.1%); ablation showing "
    "structured-language pipeline reduces action errors 93.3% to 1.1%.",
    title="Six stated contributions (diagnosis / formulation / architecture / prototype / benchmark / empirical)",
)

__all__ = [
    "setup_fm_agents",
    "setup_autoregressive_reasoning_definition",
    "setup_human_mental_simulation",
    "q_central",
    "claim_one_task_one_agent_limit",
    "claim_autoregressive_planning_limit",
    "claim_simura_intro",
    "claim_natural_language_substrate",
    "claim_headline_flightqa",
    "claim_headline_124_pct",
    "claim_open_source_release",
    "claim_contributions",
]
