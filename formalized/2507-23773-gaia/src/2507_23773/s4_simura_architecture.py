"""Section 3.4 -> 4: SIMURA architecture wiring + LLM-as-substrate prototype.

This module captures the *full SIMURA pipeline as a coherent architecture*
(perception -> planning -> acting), distinct from Section 3.1-3.3 which
develops the optimal-agent theory and from Section 4 (Section 4 in this
package) which reports per-task experimental results.

Source: Deng et al. 2025 [@Deng2025SIMURA], end of Section 3.4 + start of
Section 4 narrative.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Architectural wiring
# ---------------------------------------------------------------------------

setup_simura_modules = claim(
    "**SIMURA modular pipeline.** SIMURA comprises five named "
    "modules connected as in Figure 4: "
    "(M1) **Encoder** $h$: maps observation $o_t$ to a natural-"
    "language belief state $\\hat s_t$. "
    "(M2) **Policy** $\\tilde\\pi$: proposes candidate simulated "
    "actions $a'_t$ given $\\hat s_t$ and goal $g$. "
    "(M3) **World model** $f$: predicts the next belief state "
    "$\\hat s_{t+1}$ given $(\\hat s_t, a'_t)$. "
    "(M4) **Critic** $v$: estimates goal-progress value at the "
    "terminal planning state $\\hat s_{T'}$. "
    "(M5) **Actor** $\\alpha$: maps the chosen simulated action "
    "$a'^*_t$ (and the observation/belief) to a concrete action "
    "$a_t$ in the environment's action space. "
    "All modules communicate through the *natural-language* latent "
    "space; only the actor crosses back to the environment-specific "
    "concrete action space.",
    title="Setup: SIMURA modular pipeline -- (h, pi-tilde, f, v, alpha) communicating via natural language",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 4",
        "caption": "Fig. 4: SIMURA modular architecture -- encoder, policy, world model, critic, actor.",
    },
)

claim_planner_loop = claim(
    "**Planner inner loop.** Inside the planner (M2-M4), simulative "
    "reasoning proposes actions $a'_t \\sim \\tilde\\pi(\\hat s_t)$, "
    "predicts the resulting belief state $\\hat s_{t+1} \\sim f(\\hat "
    "s_t, a'_t)$, and evaluates the rollout via "
    "$\\sum_{k=t}^{T'-1} \\gamma_k r(g, \\hat s_k) + \\gamma_{T'} V^g_"
    "{\\pi, f}(\\hat s_{T'})$ at the planning horizon $T'$. The "
    "search may repeat multiple times, expanding the action tree, "
    "until the planner selects $a'^*_{t:T'-1}$ with highest expected "
    "success and passes only the first step $a'^*_t$ to the actor "
    "$\\alpha$ for concrete execution.",
    title="Architecture: planner inner loop -- propose / simulate / evaluate / select first action",
)

# ---------------------------------------------------------------------------
# Generality / model-agnostic claim
# ---------------------------------------------------------------------------

claim_design_is_environment_agnostic = claim(
    "**SIMURA's architecture is environment-agnostic.** Because the "
    "planning loop (@claim_planner_loop) operates entirely on natural-"
    "language belief states and natural-language simulated actions, "
    "the only environment-specific component is the encoder $h$ "
    "(observation -> belief) and the actor $\\alpha$ (simulated "
    "action -> concrete action). The same SIMURA pipeline therefore "
    "applies in principle to any goal-oriented decision problem with "
    "an observation channel and an action API -- web browsing, "
    "computer use, embodied control, etc.",
    title="Architecture: SIMURA pipeline is environment-agnostic at the planning level (only h, alpha are env-specific)",
)

claim_design_is_model_agnostic = claim(
    "**SIMURA's prototype is model-agnostic.** The paper's prototype "
    "uses LLMs as the substrate for *all* modules (M1-M5), but the "
    "architectural specification only requires that each module "
    "instantiate a probability distribution with the appropriate "
    "input/output type. Any pretrained LLM (proprietary or open-"
    "source), VLM, or future foundation model can serve as the "
    "substrate, including future world-model architectures trained "
    "directly on observation data [@Chae2024WMA; @LeCunOpenReview2022]. "
    "The empirical evaluation uses gpt-4o (and o1, o3-mini for "
    "selected baselines) but the design is not tied to any specific "
    "backbone.",
    title="Architecture: SIMURA is model-agnostic -- any LLM/VLM can substitute for each module",
)

# ---------------------------------------------------------------------------
# LLM-substrate justification
# ---------------------------------------------------------------------------

claim_llm_pretraining_is_world_modeling = claim(
    "**LLMs as world-model substrate.** Massive web-scale pretraining "
    "on next-token prediction $p(x_t \\mid x_{<t})$ is **formally "
    "akin to world modeling** -- both predict the next element of a "
    "sequence given context. Pretrained LLMs therefore possess "
    "significant latent capacity to serve as world models with "
    "natural-language state and simulated-action spaces "
    "[@RAP; @HuShu2023]. This is the conceptual basis for SIMURA's "
    "LLM substrate: even when LLMs alone are insufficient for "
    "complex agentic tasks, SIMURA's divide-and-conquer combines "
    "their existing strengths -- instruction-following, "
    "summarization, reflection, tool use -- to let agentic behavior "
    "emerge.",
    title="Architecture: LLM next-token pretraining ~ world modeling; SIMURA exploits this latent WM capacity",
)

# ---------------------------------------------------------------------------
# Search and tooling
# ---------------------------------------------------------------------------

setup_search_algorithms = setting(
    "**Search algorithms used in SIMURA's planner.** SIMURA's planner "
    "uses readily-available tree-search algorithms over the simulated-"
    "action tree -- specifically Depth-First Search (DFS) and Monte "
    "Carlo Tree Search (MCTS). The planning loop is implemented via "
    "LLM-Reasoners [@LLMReasoners], a library for LLM-based complex "
    "reasoning with advanced search algorithms. For the web-browsing "
    "experiments, the paper uses DFS with $T = t + 1$ planning "
    "horizon and $M = N = 20$ samples (see Section 5).",
    title="Setup: SIMURA planner uses DFS / MCTS search via LLM-Reasoners library",
)

# ---------------------------------------------------------------------------
# Architecture-level claim summarizing why SIMURA addresses the diagnosis
# ---------------------------------------------------------------------------

claim_architecture_addresses_diagnosis = claim(
    "**SIMURA's architecture addresses the diagnosed limitations.** "
    "Two diagnosed limits of current AI-agent practice are: "
    "(D1) one-task-one-agent paradigm (no scalability/transfer), and "
    "(D2) black-box autoregressive reasoning (no explicit "
    "simulation/counterfactual evaluation). SIMURA addresses both by "
    "construction: "
    "(A1) the planning loop is environment-agnostic "
    "(@claim_design_is_environment_agnostic), so a single architecture "
    "applies across tasks; "
    "(A2) the world model + critic explicitly simulate and evaluate "
    "candidate action sequences before commitment, supplying the "
    "counterfactual evaluation that pure autoregressive reasoning "
    "lacks (@claim_planner_loop).",
    title="Architecture-level: SIMURA structurally addresses both diagnosed limits (one-task-one-agent + black-box autoregression)",
)

__all__ = [
    "setup_simura_modules",
    "claim_planner_loop",
    "claim_design_is_environment_agnostic",
    "claim_design_is_model_agnostic",
    "claim_llm_pretraining_is_world_modeling",
    "setup_search_algorithms",
    "claim_architecture_addresses_diagnosis",
]
