"""Introduction: The Agent Capability Problem"""

from gaia.lang import claim, question, setting, support
from .s2_framework import itotal_properties, is_range

# --- Research context ---

problem_resource_allocation = claim(
    "Autonomous agents face a resource allocation challenge: an agent facing a new problem "
    "must decide whether attempting a solution is worthwhile, yet most existing frameworks "
    "lack principled methods for making this judgment before substantial resources are spent.",
    title="Resource allocation gap in autonomous agents",
)

q_solvability = question(
    "Given a problem's structure and an agent's capabilities, can we predict whether a "
    "solution exists within a given computational budget?",
    title="Core ACP question",
)

# --- Core claim: ACP framework ---

acp_framing = claim(
    "The Agent Capability Problem (ACP) frames problem-solving as information search: "
    "a solution exists somewhere in hypothesis space $\\Theta$, and each action reduces "
    "uncertainty about its location. The framework predicts resource requirements before "
    "search begins by treating problem-solving as information acquisition.",
    title="ACP information-theoretic framing",
)

# --- ACP effective cost formula ---

acp_ceffective_formula = claim(
    "The ACP defines an effective cost $C_{\\text{effective}} = (I_{\\text{total}} / I_s) \\times C_s$, "
    "where $I_{\\text{total}}$ is the total information needed to identify a solution, "
    "$I_s$ is the information gained per action, and $C_s$ is the cost per action. "
    "This quantity serves two purposes: (1) it provides an upfront solvability estimate — "
    "if $C_{\\text{effective}}$ exceeds budget $B$, the agent should reconsider; "
    "(2) it guides action selection during search by prioritizing high information-to-cost ratios.",
    title="Effective cost formula and dual purpose",
)

# --- Connections to prior work ---

active_learning_connection = claim(
    "Active learning selects maximally informative labels, with Bayesian Active Learning by "
    "Disagreement (BALD) [@Houlsby2011] using exactly the mutual information between predictions "
    "and parameters as its acquisition function, and classical D-optimality [@Chaloner1995] "
    "maximizing the Fisher information matrix determinant — all instantiating the principle of "
    "maximizing information gain [@MacKay1992].",
    title="Active learning as information maximization",
)

bayesian_opt_connection = claim(
    "Bayesian optimization methods Entropy Search (ES) [@Hennig2012] and Predictive Entropy "
    "Search (PES) [@HernandezLobato2014] directly maximize information about the optimum's "
    "location; regret bounds for Gaussian process optimization [@Srinivas2010] explicitly "
    "depend on maximum information gain, proving that efficient optimization requires "
    "efficient information acquisition.",
    title="Bayesian optimization as information maximization",
)

rl_intrinsic_connection = claim(
    "Curious reinforcement learning agents seek surprising observations that improve world models "
    "[@Schmidhuber2010], and Empowerment [@Klyubin2005] defines intrinsic value as channel "
    "capacity between actions and future states — both quantifying agent search efficiency "
    "information-theoretically.",
    title="Reinforcement learning intrinsic motivation as information maximization",
)

unified_principle = claim(
    "Active learning, Bayesian optimization, and curious reinforcement learning each independently "
    "converge on maximizing information gain relative to cost as the right principle for guiding "
    "search. The ACP makes this principle explicit and operationalizes it for solvability assessment "
    "across LLM-based and agentic workflows.",
    title="Unified information-theoretic principle across learning paradigms",
)

strat_unified_principle = support(
    [active_learning_connection, bayesian_opt_connection, rl_intrinsic_connection],
    unified_principle,
    reason=(
        "All three research communities independently converge on mutual information as "
        "the right measure for guiding search (@active_learning_connection via BALD/D-optimality, "
        "@bayesian_opt_connection via ES/PES, @rl_intrinsic_connection via curiosity/empowerment). "
        "Their convergence from independent starting points constitutes strong evidence "
        "that the principle is robust and domain-agnostic."
    ),
    prior=0.92,
)

strat_acp_framing = support(
    [problem_resource_allocation],
    acp_framing,
    reason=(
        "@problem_resource_allocation identifies the gap: agents lack principled pre-search "
        "solvability estimates. The ACP addresses this by framing problem-solving as "
        "information search where each action reduces uncertainty about the solution location."
    ),
    prior=0.88,
)

strat_acp_formula = support(
    [acp_framing, itotal_properties, is_range],
    acp_ceffective_formula,
    reason=(
        "From @acp_framing, problem-solving is information acquisition. "
        "@itotal_properties characterizes $I_{\\text{total}}$ (binary entropy of goal indicator, "
        "higher when solutions are rare) and @is_range characterizes $I_s$ "
        "(mutual information per action, from 0 for uninformative to $I_{\\text{total}}$ for decisive). "
        "Together: $I_{\\text{total}}$ bits needed, $I_s$ bits gained per action of cost $C_s$, "
        "giving $C_{\\text{effective}} = (I_{\\text{total}}/I_s) \\times C_s$ with dual purpose "
        "(upfront estimate + action selection guide)."
    ),
    prior=0.92,
)
