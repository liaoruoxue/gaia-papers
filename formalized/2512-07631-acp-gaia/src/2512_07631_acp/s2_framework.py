"""Section 2: Formal Framework"""

from gaia.lang import claim, setting, support, deduction

# --- Formal setup (settings = definitions, not claims) ---

setup_hypothesis_space = setting(
    "Let $\\Theta$ denote the space of candidate solutions. A subset $\\Theta_{\\text{goal}} \\subseteq \\Theta$ "
    "contains acceptable solutions. An agent observes the world by taking actions $a \\in \\mathcal{A}$, "
    "each producing an outcome $y \\in \\mathcal{Y}$ at cost $C_s(a)$.",
    title="ACP formal setup: hypothesis space, actions, costs",
)

def_solvability = setting(
    "Solvability Criterion (Definition 2.1): An agent with budget $B$ can solve a problem if "
    "$B \\geq C_{\\text{effective}}$, where $C_{\\text{effective}}$ is the expected cost under "
    "an optimal information-gathering policy.",
    title="Solvability criterion definition",
)

def_itotal = setting(
    "Total Information Requirement (Definition 2.2): The total information needed is "
    "$I_{\\text{total}} = H(\\mathbf{1}(\\theta \\in \\Theta_{\\text{goal}}))$, "
    "the binary entropy of the goal indicator $\\mathbf{1}(\\theta \\in \\Theta_{\\text{goal}})$ under the prior.",
    title="Total information requirement definition",
)

def_is = setting(
    "Information Gain per Action (Definition 2.3): An action $a$ producing outcome $y$ provides "
    "information $I_s(a) = I(\\mathbf{1}(\\theta \\in \\Theta_{\\text{goal}}); y \\mid a)$, "
    "the mutual information between the outcome and the goal indicator.",
    title="Information gain per action definition",
)

def_optimal_action = setting(
    "Optimal Action Selection (Definition 2.4): At each step, select "
    "$a^* = \\arg\\max_{a \\in \\mathcal{A}} \\left( \\mathbb{E}[I_s(a)] / C_s(a) \\right)$. "
    "This policy maximizes information gained per resource spent.",
    title="Optimal action selection policy",
)

def_ceffective = setting(
    "Effective Cost (Definition 2.5): $C_{\\text{effective}} = (I_{\\text{total}} / \\bar{I}_s) \\times \\bar{C}_s$, "
    "where $\\bar{I}_s$ and $\\bar{C}_s$ are average values under the optimal policy. "
    "When actions have uniform cost, $C_{\\text{effective}}$ simplifies to the number of steps times cost per step.",
    title="Effective cost definition",
)

# --- Key properties (claims derived from definitions) ---

itotal_properties = claim(
    "When $\\Theta_{\\text{goal}}$ contains a fraction $p$ of all candidates, "
    "$I_{\\text{total}} = -p \\log p - (1-p) \\log(1-p)$ (binary entropy), maximized at $p = 1/2$. "
    "Problems with rare solutions (small $p$) require more information than those with abundant solutions, "
    "because the binary goal indicator $\\mathbf{1}(\\theta \\in \\Theta_{\\text{goal}})$ "
    "carries more uncertainty when $p$ is small.",
    title="Total information as function of solution density",
)

is_range = claim(
    "The information gain $I_s(a)$ per action ranges from $I_s \\approx 0$ for uninformative "
    "actions (the outcome reveals nothing about whether $\\theta \\in \\Theta_{\\text{goal}}$) "
    "to $I_s \\approx I_{\\text{total}}$ for decisive tests that fully resolve goal membership. "
    "Uninformative actions arise when outcome $y$ is independent of the goal indicator; "
    "decisive tests are those whose outcome perfectly determines goal membership.",
    title="Information gain range per action",
)

