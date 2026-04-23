"""Introduction and Motivation — HyperAgents"""

from gaia.lang import (
    claim, setting, question,
    support, deduction, contradiction,
)

# Settings: formal definitions and background
setup_dgm = setting(
    "The Darwin Gödel Machine (DGM) (Zhang et al., 2025) demonstrates open-ended "
    "self-improvement in coding by maintaining an archive of agent variants. A coding agent "
    "generates and evaluates self-modified variants; successful ones are retained as stepping "
    "stones for further improvement. Both evaluation and self-modification are coding tasks, "
    "so gains in coding ability can translate into gains in self-improvement ability.",
    title="DGM background",
)

setup_agent_def = setting(
    "In this work, an agent is any computable program, optionally including calls to foundation "
    "models (FMs), external tools, or learned components. A task agent solves a given task. "
    "A meta agent modifies existing agents and generates new ones.",
    title="Agent and meta-agent definitions",
)

setup_hyperagent_def = setting(
    "A hyperagent is a self-referential agent that integrates a task agent and a meta agent "
    "within a single editable program. The meta agent is part of the same editable codebase "
    "and can rewrite itself. Implemented in Python (Turing-complete), a hyperagent can "
    "in principle build any computable machine.",
    title="Hyperagent definition",
)

setup_metacognitive = setting(
    "Metacognitive self-modification is the process by which a hyperagent improves not only "
    "the task-performing agent responsible for solving the given task, but also the meta agent "
    "that determines how subsequent hyperagents are generated. The self-improvement mechanism "
    "is itself subject to modification.",
    title="Metacognitive self-modification definition",
)

# Research question
q_general_self_improvement = question(
    "Can a self-improving AI system improve both task performance and its own self-improvement "
    "mechanism, without relying on domain-specific engineering, across any computable task?",
    title="Core research question",
)

# Claims from motivation
dgm_limitation = claim(
    "The Darwin Gödel Machine (DGM) relies on a handcrafted, fixed mechanism to produce "
    "self-improvement instructions. This mechanism is not modifiable. The DGM's capacity for "
    "self-improvement is therefore bottlenecked by this fixed instruction-generation step. "
    "The DGM's ability to improve at self-improving depends on an alignment assumption: that "
    "the skills required to solve evaluation tasks are the same as those required for effective "
    "self-reflection and self-modification.",
    title="DGM's fixed meta-level limitation",
    background=[setup_dgm],
)

alignment_assumption_limits_dgm = claim(
    "The alignment assumption underlying the DGM (that task-solving skills are the same as "
    "self-modification skills) is unlikely to hold outside coding domains, where task-solving "
    "skills may differ substantially from the skills needed to analyze failures, propose "
    "effective self-improvements, and implement them.",
    title="Alignment assumption breaks outside coding",
    background=[setup_dgm],
)

hyperagent_advantage = claim(
    "Hyperagents do not assume alignment between task-solving skills and self-modification skills, "
    "because the meta agent is part of the same editable program and can rewrite itself. Hence, "
    "hyperagents can improve both task performance and the process of improvement across any "
    "computable task.",
    title="Hyperagents eliminate alignment assumption",
    background=[setup_hyperagent_def, setup_metacognitive],
)

strat_hyperagent_advantage = support(
    [alignment_assumption_limits_dgm, dgm_limitation],
    hyperagent_advantage,
    reason=(
        "Because the DGM's self-improvement is limited by domain-specific alignment "
        "(@alignment_assumption_limits_dgm) and a fixed handcrafted mechanism (@dgm_limitation), "
        "making the meta agent itself editable (@setup_hyperagent_def) is the logical solution: "
        "hyperagents decouple task performance from meta-level skill, eliminating the alignment "
        "assumption that constrains the DGM."
    ),
    prior=0.85,
)

# Note: DGM's limitation and hyperagents' advantage can coexist (DGM has the limitation,
# hyperagents address it). No formal contradiction is modeled here.
