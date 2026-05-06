"""Section 3: SIMURA -- Generalized Architecture for Optimal Goal-Oriented
Agent. Formulation of agent-environment model, definition of optimal
agent, world-model-based simulative-reasoning extension, and design of the
simulative-reasoning agent (concept-based latent states + hierarchical
planning).

Source: Deng et al. 2025 [@Deng2025SIMURA], Section 3 (3.1-3.4).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 3.1 Formulation of Agent-Environment Model
# ---------------------------------------------------------------------------

setup_agent_environment_model = setting(
    "**Agent-environment model.** Following [@CritiquesWorldModels], "
    "consider an agent $\\pi$ with identity $i$ (e.g., name, "
    "description) and goal $g$ acting in environment $\\mu$ (e.g., "
    "web browser, physical world, the entire universe) with action "
    "space $A$ and state space $S$. At each time $t$, the agent "
    "takes the current state $s_t \\in S$ and outputs the next "
    "action $a_t \\in A$ following $p_\\pi(a_t \\mid s_t)$; the "
    "environment then takes $(s_t, a_t)$ and outputs the next state "
    "$s_{t+1} \\in S$ following $p_\\mu(s_{t+1} \\mid s_t, a_t)$. "
    "The joint trajectory distribution from $s_t$ to $s_T$ is "
    "$p^\\pi_\\mu(a_t, s_{t+1}, \\dots, a_{T-1}, s_T \\mid s_t) = "
    "\\prod_{k=t}^{T-1} p_\\pi(a_k \\mid s_k) \\, p_\\mu(s_{k+1} "
    "\\mid s_k, a_k)$ (Eq. 1).",
    title="Setup: agent-environment model -- (pi, mu, S, A, g) with factored trajectory distribution",
)

setup_reward_and_value = setting(
    "**Reward and value function.** In each state $s_t$ the agent "
    "receives reward $r(g, s_t)$ depending on its goal $g$. Rewards "
    "may be dense (gaming scores) or sparse (curing a disease). The "
    "agent is evaluated by the *expected discounted cumulative "
    "reward* $\\mathbb{E}_{\\pi, \\mu}\\left[\\sum_{k=t}^\\infty "
    "\\gamma_k r(g, s_k) \\mid s_t\\right]$, where the discount "
    "sequence satisfies $\\lim_{t \\to \\infty} \\gamma_t = 0$. "
    "This expectation is the **value function** $V^g_{\\pi,\\mu}(s_t)$ "
    "[@SuttonBarto].",
    title="Setup: value function V^g_{pi, mu}(s_t) and reward r(g, s_t) (dense or sparse)",
)

setup_value_recursion = claim(
    "**Value-function recursion (Eq. 2).** The value function admits "
    "the recursive decomposition "
    "$V^g_{\\pi,\\mu}(s_t) = \\sum_{(a_t, s_{t+1}, \\dots, s_T)} "
    "\\Big(\\sum_{k=t}^{T-1} \\gamma_k r(g, s_k) + \\gamma_T "
    "V^g_{\\pi,\\mu}(s_T)\\Big) \\, p^\\pi_\\mu(a_t, s_{t+1}, "
    "\\dots, s_T \\mid s_t)$, expressing the value at $s_t$ in terms "
    "of values at possible future states $s_T$ weighted by their "
    "trajectory probabilities. This is the standard Bellman-style "
    "decomposition of cumulative return.",
    title="Setup: value-function recursion (Eq. 2) -- value at s_t = expected goal progress + discounted future value",
)

# ---------------------------------------------------------------------------
# 3.2 Definition of Optimal Agent
# ---------------------------------------------------------------------------

setup_optimal_agent_def = setting(
    "**Definition of optimal agent (Eq. 3).** Based on the value "
    "function (@setup_reward_and_value, @setup_value_recursion), the "
    "*optimal agent* in environment $\\mu$ is defined as "
    "$\\pi^*_\\mu := \\arg\\max_\\pi V^g_{\\pi, \\mu}$ -- the policy "
    "that maximizes the expected discounted cumulative reward.",
    title="Setup: definition of optimal agent pi*_mu = arg max_pi V^g_{pi, mu} (Eq. 3)",
)

claim_optimal_decision_rule = claim(
    "**Optimal decision rule (Eq. 4).** From the optimal-agent "
    "definition (@setup_optimal_agent_def) and the value-function "
    "recursion (@setup_value_recursion), the optimal agent in state "
    "$s_t$ follows the decision rule "
    "$\\pi^*_\\mu(s_t) = \\arg\\max_{a_{t:T-1}} \\sum_{s_{t+1:T}} "
    "\\Big(\\sum_{k=t}^{T-1} \\gamma_k r(g, s_k) + \\gamma_T "
    "V^g_{\\pi,\\mu}(s_T)\\Big) \\prod_{i=t}^{T-1} p_\\mu(s_{i+1} "
    "\\mid s_i, a_i)$. Equivalently, the optimal agent must (i) "
    "*propose* candidate action sequences, (ii) *predict* their "
    "trajectory distributions via the environment dynamics "
    "$p_\\mu(s_{i+1} \\mid s_i, a_i)$, and (iii) *evaluate* goal "
    "progress against the cumulative-reward + future-value sum.",
    title="Optimal decision rule (Eq. 4): propose + predict + evaluate (a_t:T-1 = arg max of expected goal progress)",
)

claim_three_required_capabilities = claim(
    "**Optimal-agent decomposition into three required capabilities.** "
    "In practice, candidate actions are sampled from a *policy "
    "function* $\\tilde{\\pi}$ via $p_{\\tilde{\\pi}}(a_t \\mid s_t)$. "
    "Building the optimal agent (@claim_optimal_decision_rule) thus "
    "requires three capabilities: "
    "(1) *Proposing possible actions* via $\\tilde{\\pi}$; "
    "(2) *Predicting outcomes* of those actions via $\\mu$; "
    "(3) *Evaluating goal progress* via $r$ and $V$. "
    "Reactive agents that output the next action directly correspond "
    "to taking only the *first sample* from $\\tilde{\\pi}$ -- analogous "
    "to System-1 (fast, instinctive) reasoning [@Kahneman2011] without "
    "the simulation-and-evaluation step. Augmenting the agent with "
    "explicit $\\mu$ and $V$ recovers the System-2 (deliberate) loop "
    "and creates opportunities to spot and correct errors from the "
    "deliberation process.",
    title="Optimal-agent decomposition: (1) propose, (2) predict, (3) evaluate -- System-1 vs System-2 framing",
)

# ---------------------------------------------------------------------------
# 3.3 World Model for Generalized Simulative Reasoning
# ---------------------------------------------------------------------------

claim_ground_truth_unavailable = claim(
    "**Ground-truth state and environment are usually unavailable.** "
    "The optimal decision rule (@claim_optimal_decision_rule) "
    "presupposes access to the ground-truth state $s$ and to the "
    "environment $\\mu$ for online experience and optimization. "
    "Outside narrow scenarios such as Go/Chess [@AlphaGo; @AlphaZero], "
    "neither is available -- e.g., Mars-landing spacecraft, daily-"
    "environment humanoid robots relying on noisy sensors, etc. The "
    "agent only observes a noisy/incomplete observation $o_t$, not "
    "$s_t$.",
    title="Diagnosis: ground-truth state s and environment mu are typically unavailable; observations o_t are noisy/incomplete",
)

setup_world_model_definition = setting(
    "**World model and belief state (Definition).** A *world model* "
    "$f$ operates on an *internal representation* of the world state "
    "called a **belief state** $\\hat{s}_t$, derived from sensory "
    "input $o_t$ via an *encoder* $h$ (rather than from the true "
    "world state $s_t$). Given proposed action $a_t$, the world model "
    "predicts the next belief state via $p_f(\\hat{s}_{t+1} \\mid "
    "\\hat{s}_t, a_t)$. A WM thus functions as a *generative model "
    "of possible future world states*, enabling **simulative "
    "reasoning** (\"thought experiments\") over multiple steps up "
    "to a planning horizon $T$.",
    title="Setup: world model f, encoder h, belief state s_hat_t -- definition (3.3)",
)

claim_simulative_decision_rule = claim(
    "**Simulation-based decision rule (Eq. 5).** For an optimal agent "
    "$\\pi^*_f$ equipped with world model $f$ in belief state "
    "$\\hat{s}_t$, the simulation-based decision rule is "
    "$\\pi^*_f(\\hat{s}_t) = \\arg\\max_{a_{t:T-1}} \\sum_{\\hat "
    "s_{t+1:T}} \\Big(\\sum_{k=t}^{T-1} \\gamma_k r(g, \\hat s_k) + "
    "\\gamma_T V^g_{\\pi, f}(\\hat s_T)\\Big) \\prod_{i=t}^{T-1} "
    "p_f(\\hat s_{i+1} \\mid \\hat s_i, a_i)$. This is structurally "
    "identical to Eq. 4 (@claim_optimal_decision_rule) with the "
    "ground-truth environment $p_\\mu$ replaced by the world-model "
    "simulator $p_f$ and the ground-truth state $s$ replaced by the "
    "belief state $\\hat s$. A general-purpose WM thus enables "
    "simulation across diverse domains without direct interaction.",
    title="Theory: simulation-based decision rule (Eq. 5) replaces (s, mu) with (s_hat, f) in the optimal rule",
)

# ---------------------------------------------------------------------------
# 3.4 Concept-Based Latent States and Hierarchical Planning -- Argument
# ---------------------------------------------------------------------------

claim_continuous_embedding_brittle = claim(
    "**Argument: continuous-embedding observation encoding is brittle "
    "to real-world noise.** The dominant approach to encoding "
    "observation $o_t$ (webpages, video streams) is to map *all input "
    "tokens* into continuous embeddings of fixed dimensionality "
    "$\\hat s^z_t$. While this *technically preserves all information*, "
    "real-world sensory readings suffer from noise and high "
    "variability (e.g., webpage ads, varying weather/lighting "
    "conditions in video) which makes them *brittle to reason over* "
    "[@Barrett2017].",
    title="Argument: continuous-embedding observation encoding preserves info but is brittle to noise/variability",
)

claim_human_concept_categorization = claim(
    "**Argument: human cognition categorizes raw perception into "
    "discrete concepts.** Human cognition has evolved to counter "
    "perceptual variability by *categorizing raw perception into "
    "discrete concepts* [@Barrett2017], typically encoded as language, "
    "symbols, or structured thoughts. Natural language is inherently "
    "*hierarchical*, capable of encoding concepts from concrete "
    "(e.g., *apple*) to highly abstract (e.g., *religion*). Discrete "
    "representations are also *complete in general* "
    "[@CritiquesWorldModels], ensuring no information is necessarily "
    "lost in the compression process.",
    title="Argument: human cognition uses discrete concepts encoded in language; discrete representations are complete",
)

setup_natural_language_state_def = claim(
    "**Natural-language belief-state representation (Eq. 6).** SIMURA "
    "represents the world state $\\hat s_t$ using a *discrete natural-"
    "language summary* $\\hat s^c_t$ generated by a pretrained encoder "
    "model $h$, formally $p_h(\\hat s_t \\mid o_t) = \\prod_{i=1}^{N_t} "
    "p_h(\\hat s_{t,i} \\mid \\hat s_{t,<i}, o_t)$, where each "
    "$\\hat s_{t,i}$ is a natural-language token. The world model $f$ "
    "predicts the next state $\\hat s^c_{t+1}$ analogously: "
    "$p_f(\\hat s_{t+1} \\mid \\hat s_t, a_t) = \\prod_{i=1}^{N_{t+1}} "
    "p_h(\\hat s_{t+1,i} \\mid \\hat s_{t+1,<i}, \\hat s_t, a_t)$ "
    "(Eq. 7).",
    title="Setup: natural-language belief-state and world-model token-by-token factorization (Eqs. 6, 7)",
)

claim_concept_state_helps_policy = claim(
    "**Empirical observation: concept-based natural-language state "
    "helps downstream modules.** A concept-based natural-language "
    "representation lets the policy and other modules operate on a "
    "*more structured latent space*, which the authors find "
    "**empirically reduces hallucination and enables more robust "
    "planning**, leading to better task performance in practice.",
    title="Empirical: concept-based natural-language state reduces hallucination and improves planning robustness (in-paper observation)",
)

claim_atomic_action_rollout_limits = claim(
    "**Argument: rollouts over the concrete action space limit transfer "
    "and accumulate error.** The customary approach performs rollouts "
    "over the concrete action space $A^{(\\pi)}$. While capturing all "
    "execution details, the *idiosyncrasies of individual action "
    "spaces* (parameter ordering, format, scale) *hinder transfer* "
    "across action spaces / environments / tasks. Furthermore, the "
    "real world contains a *richer range of intentions* than what a "
    "particular action space offers (e.g., clicking on a flight may "
    "mean exploring pricing or committing to the option). Sequential "
    "rollouts over atomic actions are also inefficient and increase "
    "*error accumulation* across many low-level steps (e.g., "
    "swooshing of liquids with each muscle twitch), even when "
    "higher-level dynamics over abstract actions (e.g., spilling "
    "water by tilting the glass) remain stable and predictable.",
    title="Argument: concrete-action-space rollouts hurt transfer + accumulate error vs higher-level abstractions",
)

claim_hierarchical_action_proposal = claim(
    "**Hierarchical-action design.** To close the action-abstraction "
    "gap (@claim_atomic_action_rollout_limits), SIMURA adopts a "
    "*hierarchical architecture* [@Dyna] separating high-level "
    "flexible planning from low-level rigorous execution. The "
    "policy $p_{\\tilde\\pi}(a'_t \\mid \\hat s_t)$ and world model "
    "$p_f(\\hat s_{t+1} \\mid \\hat s_t, a'_t)$ operate over "
    "*simulated actions* $a'_t$ from a separate action space $A'$; "
    "an actor $p_\\alpha(a_t \\mid a'_t, \\hat s_t)$ then selects "
    "the concrete action $a_t \\in A$ given the chosen simulated "
    "action and the current belief. This divide-and-conquer "
    "disentangles reasoning from action-space details and lets a "
    "single $a'_t$ stand for multiple execution steps (e.g., "
    "'explore the website' vs many low-level clicks), shortening "
    "rollouts and reducing error accumulation.",
    title="Design: hierarchical actor -- simulated action a'_t (planning) decoupled from concrete action a_t (execution)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 3",
        "caption": "Fig. 3: SIMURA agent design with separated simulated actions (planning) and concrete actions (execution).",
    },
)

claim_natural_language_action_empirical = claim(
    "**Empirical observation: representing simulated actions as natural "
    "language gives more diverse, grounded action proposals.** SIMURA "
    "represents simulated actions $a'_t$ as natural-language phrases "
    "(e.g., \"Go to the home page of Google Flights.\" or \"Click on "
    "the 'Search' button.\"). The authors find this yields **more "
    "diverse and grounded action proposals** in practice, leading "
    "to better task success.",
    title="Empirical: natural-language simulated actions yield more diverse, grounded proposals (in-paper observation)",
)

# ---------------------------------------------------------------------------
# Full SIMURA decision process (Eq. 8)
# ---------------------------------------------------------------------------

claim_simura_decision_process = claim(
    "**Full SIMURA decision process (Eq. 8).** Given observation "
    "$o_t$, SIMURA solves a three-level optimization: "
    "**Perception**: $\\hat s_t = \\arg\\max_{\\hat s} p_h(\\hat s "
    "\\mid o_t)$. "
    "**Planning**: $a'^*_{t:T'-1} = \\arg\\max_{a'_{t:T-1} \\sim "
    "\\tilde\\pi} \\sum_{\\hat s_{t+1:T'}} v(\\hat s_{T'}) "
    "\\prod_{k=t}^{T'-1} p_f(\\hat s_{k+1} \\mid \\hat s_k, a'_k)$. "
    "**Acting**: $a_t = \\arg\\max_{a} p_\\alpha(a \\mid \\hat s_t, "
    "a'^*_t)$. "
    "Inside the planner, simulative reasoning proposes actions via "
    "the policy $\\tilde\\pi$, predicts next states via the world "
    "model $f$, and evaluates goal progress via the critic $v$ at "
    "horizon $T'$. The agent passes only the first action $a^*_t$ "
    "to the actor $\\alpha$ which finally outputs the concrete "
    "action $a_t$.",
    title="SIMURA's three-level optimization (Eq. 8): Perception (h) -> Planning (pi-tilde, f, v) -> Acting (alpha)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 4",
        "caption": "Fig. 4: full SIMURA decision pipeline -- encoder, planner, actor.",
    },
)

__all__ = [
    "setup_agent_environment_model",
    "setup_reward_and_value",
    "setup_value_recursion",
    "setup_optimal_agent_def",
    "claim_optimal_decision_rule",
    "claim_three_required_capabilities",
    "claim_ground_truth_unavailable",
    "setup_world_model_definition",
    "claim_simulative_decision_rule",
    "claim_continuous_embedding_brittle",
    "claim_human_concept_categorization",
    "setup_natural_language_state_def",
    "claim_concept_state_helps_policy",
    "claim_atomic_action_rollout_limits",
    "claim_hierarchical_action_proposal",
    "claim_natural_language_action_empirical",
    "claim_simura_decision_process",
]
