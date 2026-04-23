"""Section 6 & 7: Safety Discussion and Limitations"""

from gaia.lang import (
    claim, setting,
    support,
)

from .motivation import (
    setup_hyperagent_def,
    setup_metacognitive,
)
from .s5_results import (
    self_improvements_compound,
    meta_improvements_transfer,
    law_dgmh_improves,
    dgmh_no_domain_alignment,
)
from .s3_methods import dgmh_extends_dgm

# Safety constraints used in this work
setup_safety_constraints = setting(
    "In this work, all experiments are conducted under strict safety constraints: agent-generated "
    "code is executed within carefully sandboxed environments with enforced resource limits "
    "(timeouts, restricted internet access). Evaluation uses predefined tasks and metrics, "
    "and human oversight is maintained throughout.",
    title="Safety constraints in DGM-H experiments",
)

# Safety concerns
safety_concern_oversight = claim(
    "As AI systems gain the ability to modify themselves in increasingly open-ended ways, they "
    "can potentially evolve far more rapidly than humans can audit or interpret. At the cusp of "
    "such explosive capability growth, existing human oversight mechanisms may become increasingly "
    "strained or infeasible.",
    title="Safety concern: self-improving systems may outpace human oversight",
    background=[setup_hyperagent_def, setup_metacognitive],
)

# Limitations
limitation_fixed_task_dist = claim(
    "DGM-H operates with a fixed task distribution. The current implementation does not "
    "co-evolve the task distribution by generating new tasks and curricula that adapt to the "
    "agent's capabilities.",
    title="Limitation: fixed task distribution",
)

limitation_fixed_outer_loop = claim(
    "Components of the DGM-H open-ended exploration loop (parent selection, evaluation protocols) "
    "remain fixed. Hyperagents cannot alter the outer process that determines which agents are "
    "selected or how they are evaluated. This limits full self-modifiability.",
    title="Limitation: fixed outer exploration loop",
)

dgmh_not_fully_self_modifiable = claim(
    "DGM-H does not achieve fully unbounded self-modifiability. Two constraints limit it: "
    "(1) it operates with a fixed task distribution, and (2) outer-loop components (parent "
    "selection, evaluation protocols) remain fixed and cannot be modified by hyperagents. "
    "These constraints improve experimental stability and safety but limit the system's "
    "theoretical ceiling for open-ended improvement.",
    title="DGM-H not fully self-modifiable",
)

strat_limitations = support(
    [limitation_fixed_task_dist, limitation_fixed_outer_loop],
    dgmh_not_fully_self_modifiable,
    reason=(
        "Two concrete limitations constrain DGM-H's self-modifiability: the task distribution "
        "is fixed (@limitation_fixed_task_dist), so the agent cannot generate new tasks or "
        "curricula; and the outer exploration loop components are fixed (@limitation_fixed_outer_loop), "
        "so hyperagents cannot alter parent selection or evaluation protocols. Together, these "
        "prevent truly unbounded recursive self-improvement."
    ),
    prior=0.9,
)

strat_safety = support(
    [law_dgmh_improves, meta_improvements_transfer, self_improvements_compound],
    safety_concern_oversight,
    reason=(
        "The hyperagent framework (@setup_hyperagent_def) enables metacognitive self-modification "
        "(@setup_metacognitive), which accelerates capability gains. The empirical observation that "
        "DGM-H achieves substantial performance gains (@law_dgmh_improves), meta-improvements "
        "transfer across domains (@meta_improvements_transfer), and self-improvements compound "
        "across runs (@self_improvements_compound) collectively support the concern that "
        "self-improving systems can evolve faster than human oversight mechanisms can adapt."
    ),
    prior=0.7,
)
