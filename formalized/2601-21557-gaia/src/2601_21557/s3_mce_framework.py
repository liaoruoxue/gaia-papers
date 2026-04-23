"""Section 3: Meta Context Engineering Framework"""

from gaia.lang import claim, setting, question, support, deduction

from .motivation import no_universal_harness, setup_ce_discipline

# ── Settings (formal definitions) ─────────────────────────────────────────────

setup_context_function = setting(
    "A context function $c$ maps each query $x \\in \\mathcal{X}$ to its context, "
    "specified by a representation $\\rho$ (static components) and functional operators $F$ "
    "(dynamic components). Static components $\\rho$ may include knowledge bases, decision rules, "
    "or examples; dynamic operators $F$ implement retrieval, filtering, or composition logic.",
    title="Context function definition",
)

setup_skill = setting(
    "A skill $s \\in \\mathcal{S}$ is an executable specification (a markdown file, SKILL.md) "
    "that defines how the context function should be represented and learned from data. "
    "Given a skill $s$, a base-level agent executes it to produce a context function $c_s = (\\rho_s, F_s)$.",
    title="Skill definition",
)

setup_bilevel_problem = setting(
    "MCE solves the bi-level optimization problem: "
    "$$s^* = \\arg\\max_{s \\in \\mathcal{S}} J_{\\text{val}}(c^*_s)$$ "
    "subject to $c^*_s = \\arg\\max_{c_s} J_{\\text{train}}(c_s; s)$. "
    "The inner optimization finds the best context function given skill $s$; "
    "the outer optimization finds the skill that yields context with maximal validation performance.",
    title="MCE bi-level optimization formulation",
)

setup_evolution_strategy = setting(
    "MCE algorithmic orchestration uses a simple history-informed $(1+1)$-Evolution Strategy (ES): "
    "at each iteration $k$, agentic crossover generates one offspring context $c_k$, which is "
    "compared against the current best $c^*_{k-1}$, and the better one is retained.",
    title="(1+1)-ES algorithmic orchestration",
)

setup_agent_tools = setting(
    "Both meta-level and base-level agents interact with a programming environment through a "
    "standard tool set $\\mathcal{T} = \\{\\text{Read, Write, Edit, Bash, Glob, Grep, TodoWrite}\\}$ "
    "and produce outputs by manipulating a file system workspace.",
    title="Agent tool set",
)

# ── Claims ────────────────────────────────────────────────────────────────────

mce_decouples_what_how = claim(
    "Meta Context Engineering (MCE) decouples *what* to learn (the context function $c_s$) from "
    "*how* to represent and learn it (the skill $s$). This is analogous to separating learned "
    "parameters from model architecture and training algorithms in machine learning, but operating "
    "at a higher level of abstraction where the underlying LLMs are already trained and frozen.",
    title="MCE decoupling of what vs how",
)

strat_mce_decouples = support(
    [no_universal_harness],
    mce_decouples_what_how,
    reason=(
        "Because @no_universal_harness — no single harness is universally optimal — "
        "MCE treats the harness (skill) itself as a learnable variable rather than fixing it. "
        "This decoupling is the central motivation from [@Zhang2026] [@Agrawal2025] limitations."
    ),
    prior=0.90,
)

skill_unifies_levels = claim(
    "Representing CE procedures as skills (self-contained SKILL.md files encapsulating instructions, "
    "resources, and scripts) enables seamless co-evolution of different solution levels, "
    "overcomes fragmentation seen in prior co-evolutionary approaches, and provides a modular "
    "interface that decouples the optimization target from the core agent architecture.",
    title="Skills enable co-evolution and modularity",
)

strat_skill_unifies = support(
    [mce_decouples_what_how],
    skill_unifies_levels,
    reason=(
        "The decoupling of what-to-learn from how-to-learn (@mce_decouples_what_how) is realized "
        "by encapsulating the 'how' in a skill (SKILL.md file). This file-based skill representation "
        "makes the optimization target (context function) separate from the agent architecture, "
        "enabling co-evolution and modular reuse across iterations."
    ),
    prior=0.87,
)

agentic_crossover_claim = claim(
    "Agentic crossover is an LLM agent-driven operator that synthesizes a new skill $s_k$ at "
    "iteration $k$ by selectively combining and refining elements from previous skills in the "
    "skill database $H_{k-1} = \\{(s_i, c_i, J^{\\text{train}}_i, J^{\\text{val}}_i)\\}_{i=1}^{k-1}$. "
    "Unlike fixed recombination rules, the agent can flexibly inspect and selectively recombine "
    "components from ancestor skill directories, enabling more granular and context-aware updates.",
    title="Agentic crossover synthesizes new skills",
)

strat_agentic_crossover = support(
    [skill_unifies_levels],
    agentic_crossover_claim,
    reason=(
        "Skills are modular, file-based artifacts (@skill_unifies_levels), which enables agentic "
        "crossover to inspect and selectively recombine components from previous skill files. "
        "This is only possible because skills encapsulate procedures in a readable, manipulable form — "
        "unlike opaque neural weights or fixed template strings."
    ),
    prior=0.85,
    background=[setup_bilevel_problem],
)

context_as_files = claim(
    "MCE instantiates context functions as collections of files in a designated directory, "
    "including both static components (knowledge bases, decision rules, examples) and dynamic "
    "operators (retrieval, filtering, composition logic implemented as code). "
    "This file-and-code representation imposes no structural constraints, enabling arbitrary "
    "computational procedures for context generation and manipulation.",
    title="Context as file-based programmatic artifacts",
)

strat_context_as_files = support(
    [mce_decouples_what_how],
    context_as_files,
    reason=(
        "MCE decouples context representation from optimization (@mce_decouples_what_how). "
        "Instantiating both static and dynamic components as files and code imposes no a priori structural "
        "constraints, unlike prior methods that fix list-based or trajectory-based representations. "
        "The formal context function definition (setting: @setup_context_function) and skill definition "
        "(setting: @setup_skill) are mathematical background for this design choice.",
    ),
    prior=0.92,
    background=[setup_context_function, setup_skill],
)

mce_opens_design_space = claim(
    "By elevating the decoupling of context representation and optimization procedure to the level "
    "of Meta Context Engineering, MCE opens a new design space for optimizing agentic AI analogous "
    "to the fields of meta-learning, AutoML, neural architecture search, and hyperparameter optimization.",
    title="MCE opens new meta-level design space",
)

strat_mce_design_space = support(
    [mce_decouples_what_how, skill_unifies_levels, context_as_files],
    mce_opens_design_space,
    reason=(
        "The combination of bi-level decoupling (@mce_decouples_what_how), "
        "skill-based unification (@skill_unifies_levels), and unconstrained file-based context "
        "representation (@context_as_files) collectively enables a design space analogous to "
        "meta-learning and AutoML — where the learning procedure itself is the optimization target."
    ),
    prior=0.85,
)
