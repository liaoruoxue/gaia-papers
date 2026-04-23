"""Section 3: Methods — DGM-Hyperagents (DGM-H) Framework"""

from gaia.lang import (
    claim, setting,
    support, deduction,
)

from .motivation import (
    setup_dgm,
    setup_hyperagent_def,
    setup_metacognitive,
    setup_agent_def,
    hyperagent_advantage,
)

# Settings for the DGM-H method
setup_archive = setting(
    "DGM-H maintains an archive of generated hyperagents, initialized with a single hyperagent "
    "and expanded over time by continuously accumulating generated variants. The process alternates "
    "between two phases: metacognitive self-modification and evaluation.",
    title="DGM-H archive structure",
)

setup_parent_selection = setting(
    "Parent selection in DGM-H is probabilistic and proportional to a hyperagent's performance, "
    "and inversely proportional to the number of children that successfully compiled. This biases "
    "sampling toward hyperagents that perform well and generate strong descendants while preserving "
    "exploration.",
    title="Parent selection mechanism",
)

setup_initial_agent = setting(
    "All runs start from the same initial agent, which directly outputs the response from a single "
    "foundation model (FM) call with no task-specific parsing or post-processing.",
    title="Initial agent definition",
)

setup_evaluation_protocol = setting(
    "For each domain, agents are first evaluated on a small subset of training tasks to estimate "
    "effectiveness. Only agents that demonstrate sufficient performance are subsequently evaluated "
    "on the remaining training tasks. Agents that do not pass are treated as having zero performance "
    "on unevaluated tasks. Only the best agents (selected via validation scores, or training scores "
    "when validation tasks do not exist) are evaluated on the test set.",
    title="Staged evaluation protocol",
)

setup_statistical = setting(
    "For each experiment, each method is run 5 times. Results report medians with 95% bootstrap "
    "confidence intervals (CI) computed from 1,000 resamples. Statistical significance uses the "
    "Wilcoxon signed-rank test.",
    title="Statistical methodology",
)

# Method claims
dgmh_extends_dgm = claim(
    "DGM-Hyperagents (DGM-H) augments the original DGM with hyperagents. DGM-H employs the "
    "open-ended exploration process in the DGM (archive, parent selection, evaluation) while "
    "adding metacognitive self-modification: the meta agent that generates modifications is "
    "itself part of the editable hyperagent codebase and can be modified.",
    title="DGM-H as extension of DGM",
    background=[setup_dgm, setup_hyperagent_def, setup_metacognitive],
)

dgmh_no_domain_alignment = claim(
    "By allowing the improvement procedure to evolve, DGM-H eliminates the assumption of "
    "domain-specific alignment between task performance and self-modification skill. This "
    "enables DGM-H to potentially support self-accelerating progress on any computable task.",
    title="DGM-H removes alignment assumption",
    background=[setup_metacognitive, setup_archive],
)

strat_dgmh_no_alignment = support(
    [dgmh_extends_dgm, hyperagent_advantage],
    dgmh_no_domain_alignment,
    reason=(
        "Because DGM-H (@dgmh_extends_dgm) integrates the meta agent into the editable codebase "
        "(@hyperagent_advantage), the self-improvement procedure is no longer fixed. Both task "
        "agents and meta agents evolve, decoupling the requirements for task performance from "
        "meta-level modification skill, so domain-specific alignment is not assumed."
    ),
    prior=0.85,
)

open_ended_mitigates_convergence = claim(
    "The open-ended exploration process in DGM-H maintains an archive of diverse hyperagent "
    "variants, mitigating premature convergence and avoiding local optima by using past agents "
    "as stepping stones for future improvement.",
    title="Open-ended exploration prevents premature convergence",
    background=[setup_archive, setup_parent_selection],
)

strat_open_ended = support(
    [dgmh_extends_dgm],
    open_ended_mitigates_convergence,
    reason=(
        "DGM-H retains all previously generated hyperagents in an archive (@setup_archive) and "
        "uses probabilistic parent selection biased toward high performance and strong descendants "
        "(@setup_parent_selection). This population-based diversity preservation prevents the "
        "system from converging to a single solution path."
    ),
    prior=0.8,
)
