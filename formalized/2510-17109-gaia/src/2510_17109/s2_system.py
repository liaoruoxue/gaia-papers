"""Section 2 — VeriMAP system architecture.

Defines the four modules (Planner, Executor, Verifier, Coordinator) and the
key design choices: Structured I/O, Named Variables, planner-generated VFs,
strict-AND aggregation, retry-with-feedback, and replanning on failure.
"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    mas_setting,
    dag_plan_setting,
    verification_setting,
    failures_context_dependent,
    existing_verification_misses_context,
)

# ---------- Settings: definitions of components ----------

verimap_overview_setting = setting(
    "VeriMAP is composed of four modules (Figure 1 of the source paper): "
    "(1) the Verification-Aware **Planner** that decomposes the task and "
    "generates verification functions per subtask, (2) the **Executor** "
    "that solves an individual subtask given local instructions and "
    "context, (3) the **Verifier** that evaluates each subtask's output "
    "against the planner-generated VFs, and (4) the **Coordinator** that "
    "sequences nodes, manages context, runs the retry loop, and triggers "
    "replanning on failure.",
    title="VeriMAP architecture overview",
    metadata={"figure": "artifacts/2510.17109.pdf, Figure 1"},
)

python_vf_setting = setting(
    "A **Python verification function (Python VF)** is a self-contained "
    "Python snippet of assertions over the executor's structured output. "
    "It is executed by a Python interpreter and provides deterministic, "
    "reproducible pass/fail decisions; on failure it returns the full "
    "traceback as feedback.",
    title="Python VF (definition)",
)

nl_vf_setting = setting(
    "A **natural-language verification function (NL VF)** is a "
    "natural-language criterion attached to a subtask. It is judged by a "
    "verifier LLM (a ReAct-style agent with the same tools as the "
    "executor) which returns a binary pass/fail label and a textual "
    "explanation that identifies what was wrong and how to amend it.",
    title="Natural-language VF (definition)",
)

strict_and_setting = setting(
    "VeriMAP's verifier aggregates per-subtask VF results using a strict "
    "logical AND: a subtask is marked **failed** if any single VF fails. "
    "Softer weighted aggregation is mentioned as future work but not used "
    "in the experiments.",
    title="Strict-AND VF aggregation",
)

retry_replan_setting = setting(
    "The Coordinator runs a controlled retry loop with a per-node retry "
    "limit $R_{\\max}$ (default 3) and a global replanning iteration "
    "limit $I_{\\max}$ (default 5). On a failed verification, the loop "
    "retries the execute-verify cycle for the same node with the previous "
    "output added to context. If retries are exhausted, the Coordinator "
    "collects execution traces and triggers replanning to generate a new "
    "DAG; execution restarts from the top of the new plan.",
    title="Retry and replanning protocol",
)

# ---------- Claims about the system design ----------

verimap_modules = claim(
    "VeriMAP integrates planning and verification as four cooperating "
    "modules — Planner, Executor, Verifier, Coordinator — whose interfaces "
    "are defined by the planner's DAG, the per-subtask VFs, and the "
    "Coordinator's topological execution loop with retry and replanning.",
    title="VeriMAP four-module architecture",
)

structured_io_named_vars = claim(
    "VeriMAP enforces two interface invariants on agent-to-agent message "
    "passing: (i) **Structured I/O**, where every agent input/output is a "
    "well-defined object such as a JSON dictionary; and (ii) **Named "
    "Variables**, where each I/O object has a unique, plan-wide consistent "
    "name. Each node thus receives an input as `(name: value)` pairs and "
    "declares its expected output names, so downstream agents can "
    "reliably reference upstream outputs and execution ambiguity is "
    "reduced.",
    title="Structured I/O + Named Variables",
)

planner_generated_vfs = claim(
    "The VeriMAP planner generates per-subtask verification functions of "
    "two kinds: **Python VFs** for tasks with well-defined functional or "
    "structural requirements (deterministic checks of type, format, and "
    "correctness), and **natural-language VFs** for tasks requiring "
    "semantic or open-ended judgment (verifier-LLM checks). Both kinds "
    "are aligned with the subtask's Structured I/O contract.",
    title="Planner-generated VFs (Python + NL)",
)

python_vf_definition = claim(
    "A Python verification function is a self-contained Python snippet of "
    "assertions over the structured output. Being executed by a Python "
    "interpreter, it provides deterministic, reproducible pass/fail "
    "guarantees and returns a complete traceback as feedback when an "
    "assertion fails.",
    title="Python VF — properties",
)

nl_vf_definition = claim(
    "A natural-language verification function is judged by a verifier "
    "LLM (a ReAct-style agent with the same tools as the executor) "
    "and returns a binary success/fail label together with a "
    "constructive textual feedback that explains what was wrong and how "
    "to amend it. NL VFs handle semantic and open-ended criteria that "
    "Python VFs cannot encode.",
    title="NL VF — properties",
)

strict_and_aggregation = claim(
    "VeriMAP's verifier marks a subtask as failed whenever any single VF "
    "fails (strict logical AND). This makes verification conservative — "
    "false positives are reduced at the cost of potentially higher false "
    "negatives.",
    title="Strict-AND aggregation increases conservatism",
)

coordinator_retry = claim(
    "On a failed verification, the Coordinator retries the same node up "
    "to $R_{\\max}$ times (default 3), each time augmenting the context "
    "with the previous output and the verifier's feedback. This local "
    "retry loop converts informative VF failure feedback into corrective "
    "guidance for the executor.",
    title="Per-node retry with feedback",
)

coordinator_replanning = claim(
    "When per-node retries are exhausted, the Coordinator collects "
    "execution traces, invokes the planner with these traces appended to "
    "the original prompt, and restarts execution from the top of the new "
    "plan. Replanning is bounded by an iteration limit $I_{\\max}$ "
    "(default 5); termination is guaranteed because the iteration counter "
    "monotonically increases.",
    title="Coordinator replanning loop",
)

executor_can_be_smaller = claim(
    "Because each Executor handles a single, well-scoped subtask with "
    "planner-supplied instructions and verification criteria, the "
    "Executor can use a smaller, cheaper LLM (the paper uses "
    "`gpt-4o-mini`) without sacrificing system accuracy. The bulk of "
    "global reasoning is offloaded to the planner.",
    title="Smaller executors suffice under planner offload",
)

# ---------- Strategies tying the system claims together ----------

# Why Structured I/O + Named Variables follow from the context-dependence problem.
strat_io_addresses_context = support(
    [structured_io_named_vars, failures_context_dependent],
    existing_verification_misses_context,  # consequence: VeriMAP closes the gap
    background=[verimap_overview_setting, dag_plan_setting],
    reason=(
        "Note: this strategy expresses the *design rationale* — VeriMAP "
        "closes the context gap (@existing_verification_misses_context) "
        "by establishing a structured contract (@structured_io_named_vars) "
        "that makes plan-level expectations machine-checkable, given that "
        "failures are context-dependent (@failures_context_dependent). "
        "The DAG (@dag_plan_setting) and overall architecture "
        "(@verimap_overview_setting) provide the substrate."
    ),
    prior=0.8,
)

# The two VF types follow from definitions + the breadth of subtask kinds.
strat_two_vf_types = support(
    [python_vf_definition, nl_vf_definition],
    planner_generated_vfs,
    background=[python_vf_setting, nl_vf_setting, verimap_overview_setting],
    reason=(
        "The planner emits the union of Python VFs (@python_vf_definition, "
        "definition @python_vf_setting) for structural/functional checks "
        "and NL VFs (@nl_vf_definition, definition @nl_vf_setting) for "
        "semantic checks. Together they cover the breadth of subtask "
        "kinds in the VeriMAP architecture (@verimap_overview_setting)."
    ),
    prior=0.95,
)

# Strict-AND aggregation conservatism is a deductive consequence of definition.
strict_and_restated = claim(
    "Under strict-AND, a passing subtask requires every VF to pass; "
    "equivalently, the system rejects any output that any single VF "
    "marks as wrong.",
    title="Strict-AND restated",
)

strat_strict_and_conservative = deduction(
    [strict_and_aggregation],
    strict_and_restated,
    background=[strict_and_setting],
    reason=(
        "Pure restatement of the definition (@strict_and_setting): "
        "'fail if any VF fails' is logically equivalent to 'pass requires "
        "all VFs to pass' (@strict_and_aggregation)."
    ),
    prior=0.99,
)

# Coordinator replanning follows from the retry+replan protocol definition.
strat_coordinator_replan = deduction(
    [coordinator_retry],
    coordinator_replanning,
    background=[retry_replan_setting, verimap_overview_setting],
    reason=(
        "By the protocol definition (@retry_replan_setting), per-node "
        "retries (@coordinator_retry) are bounded by $R_{\\max}$. Once "
        "exhausted, the Coordinator deterministically invokes the planner "
        "with the collected traces and restarts execution — that is "
        "exactly @coordinator_replanning. The architecture context is "
        "@verimap_overview_setting."
    ),
    prior=0.99,
)

# Executor can be smaller — supported by structured I/O + planner-generated VFs.
strat_smaller_executors = support(
    [structured_io_named_vars, planner_generated_vfs],
    executor_can_be_smaller,
    background=[verimap_overview_setting],
    reason=(
        "When subtask boundaries are precise (@structured_io_named_vars) "
        "and acceptance criteria are explicit (@planner_generated_vfs), "
        "the executor only needs local capability rather than full task "
        "understanding. Hence smaller models like `gpt-4o-mini` can serve "
        "as executors without losing system-level accuracy "
        "(@verimap_overview_setting)."
    ),
    prior=0.8,
)

# Top-level: VeriMAP four-module architecture is the union of the above design choices.
strat_verimap_architecture = support(
    [structured_io_named_vars, planner_generated_vfs, coordinator_replanning],
    verimap_modules,
    background=[verimap_overview_setting],
    reason=(
        "The four-module architecture (@verimap_modules) is constituted "
        "by three distinguishing design choices: (i) the structured "
        "interface contract (@structured_io_named_vars), (ii) per-subtask "
        "VFs generated by the planner (@planner_generated_vfs), and "
        "(iii) the coordinator's retry-and-replan loop "
        "(@coordinator_replanning), all sketched in @verimap_overview_setting."
    ),
    prior=0.95,
)
