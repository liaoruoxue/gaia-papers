"""Section 2.2.4: DAG-based Task Decomposition and Execution +
formal guarantees -- AND-tree semantics, FSM, scheduling, deadlock
detector, seven invariants.

Source: Yu et al. 2026 [@Yu2026OMC], Section 2.2.4 (pages 10-12).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: AND-tree + FSM
# ---------------------------------------------------------------------------

setup_and_tree_dag_dependency = setting(
    "**Definition (AND-tree with DAG dependencies).** The task "
    "tree $\\mathcal{T} = (V, E_{\\text{tree}}, E_{\\text{dep}})$ "
    "with the DAG invariant on $G = (V, E_{\\text{tree}} \\cup "
    "E_{\\text{dep}})$. The execution semantics are governed by "
    "AND-semantics on subtree completion plus an FSM on per-node "
    "lifecycle.",
    title="Setup: AND-tree augmented with DAG dependency edges (DAG invariant enforced at insertion)",
)

setup_and_semantics = setting(
    "**Definition (AND-semantics).** A node $v$ is *resolved* "
    "according to:\n\n"
    "$$\\text{resolved}(v) \\iff \\begin{cases} "
    "\\phi_v \\in \\{\\text{accepted}, \\text{finished}\\} & "
    "\\text{if } v \\text{ is a leaf} \\\\ "
    "\\forall v' \\in \\text{children}(v) \\setminus S: "
    "\\text{resolved}(v') & \\text{otherwise} "
    "\\end{cases}$$\n\n"
    "where $S$ is the set of system node types (review requests, "
    "watchdog nudges). This AND-semantics is the key structural "
    "guarantee: completion **must** propagate bottom-up from "
    "leaves through the entire tree -- no subtasks can be silently "
    "dropped.",
    title="Setup: AND-semantics -- resolved(v) requires every non-system child resolved (bottom-up completion is mandatory)",
)

setup_task_lifecycle_fsm = setting(
    "**Definition (Task Lifecycle FSM).** Each task node follows "
    "a finite state machine $M = (\\Phi, \\delta, \\phi_0, F)$ "
    "with initial state $\\phi_0 = \\text{pending}$, terminal "
    "states $F = \\{\\text{finished}, \\text{cancelled}\\}$, and "
    "$\\Phi = \\{\\text{pending}, \\text{processing}, "
    "\\text{holding}, \\text{completed}, \\text{accepted}, "
    "\\text{failed}, \\text{blocked}, \\text{finished}, "
    "\\text{cancelled}\\}$. Two design choices are critical: "
    "(F1) `completed -> accepted` requires explicit supervisor "
    "review, preventing hallucinated results from unblocking "
    "dependents; (F2) the `failed -> processing` retry path is "
    "bounded by a maximum retry count $k_{\\text{retry}}$; "
    "exceeding triggers escalation, guaranteeing no node cycles "
    "indefinitely.",
    title="Setup: task lifecycle FSM (9 states, 2 terminal); explicit review gate + bounded retries are critical design choices",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Figure 5 (page 11)",
    },
)

setup_scheduling_predicate = setting(
    "**Definition (Ready predicate + scheduling).** A node $v$ "
    "becomes executable when its dependencies are satisfied:\n\n"
    "$$\\text{ready}(v) \\iff \\phi_v = \\text{pending} \\land "
    "\\forall u \\in \\text{deps}(v): \\phi_u \\in \\{"
    "\\text{accepted}, \\text{finished}\\}$$\n\n"
    "The scheduler selects the first ready node per employee in "
    "FIFO order, subject to mutual exclusion: "
    "$|\\text{running}(e)| \\le 1$ for all employees $e$. When a "
    "node reaches a resolved state, dependency resolution "
    "propagates forward: dependents with all dependencies resolved "
    "are scheduled; dependents with failed dependencies are marked "
    "`blocked` (or cascade-cancelled if non-recoverable). Cascade "
    "cancellation is transitive: $\\text{cancel}(v) \\Rightarrow "
    "\\forall w: v \\in \\text{deps}(w) \\Rightarrow "
    "\\text{cancel}(w)$.",
    title="Setup: ready predicate (pending + all deps in {accepted, finished}); FIFO per-employee + |running(e)| <= 1 + transitive cancel",
)

setup_bottom_up_propagation = setting(
    "**Definition (Bottom-Up Completion Propagation).** When a "
    "leaf passes review, the AND-semantics trigger recursive "
    "propagation: if all children of a parent are resolved, the "
    "parent auto-promotes "
    "`completed -> accepted -> finished`, which triggers its "
    "parent's resolution check, and so on up to the project root. "
    "Project completion is therefore a *derived* property of "
    "subtask completion, not a separately maintained flag.",
    title="Setup: bottom-up completion propagation -- project completion is derived from subtask completion (not a separate flag)",
)

setup_deadlock_detector = setting(
    "**Definition (Deadlock Detector).** Safety-net rule: if all "
    "non-root nodes are in terminal or `blocked` states but the "
    "root has not resolved, the project is marked `failed`, "
    "preventing silent stalls.",
    title="Setup: deadlock detector -- if every non-root is terminal/blocked but root unresolved, mark project failed (no silent stalls)",
)

# ---------------------------------------------------------------------------
# The seven invariants (page 12)
# ---------------------------------------------------------------------------

claim_invariant_1_dag = claim(
    "**Invariant I1 (DAG Invariant).** "
    "$G = (V, E_{\\text{tree}} \\cup E_{\\text{dep}})$ is always "
    "acyclic. Enforced at insertion via DFS cycle detection.",
    title="Invariant I1: DAG -- combined graph is always acyclic (DFS cycle detection at insertion)",
)

claim_invariant_2_mutual_exclusion = claim(
    "**Invariant I2 (Mutual Exclusion).** "
    "$|\\text{running}(e)| \\le 1$ for all employees $e$. The "
    "Task interface enforces this through per-employee queues.",
    title="Invariant I2: mutual exclusion -- |running(e)| <= 1 (per-employee queue with mutex)",
)

claim_invariant_3_schedule_idempotency = claim(
    "**Invariant I3 (Schedule Idempotency).** Repeated scheduling "
    "of the same node is a no-op, so crash recovery never causes "
    "duplicate execution. This is a precondition for safe "
    "re-scheduling after crashes (see I7).",
    title="Invariant I3: schedule idempotency -- re-scheduling is a no-op (crash-recovery never duplicates)",
)

claim_invariant_4_review_termination = claim(
    "**Invariant I4 (Review Termination).** At most "
    "$k_{\\text{rev}}$ reviews per parent before escalation. Caps "
    "the depth of any accept-or-redecompose loop at a finite "
    "number of rounds.",
    title="Invariant I4: review termination -- at most k_rev reviews per parent before escalation",
)

claim_invariant_5_cascade_completeness = claim(
    "**Invariant I5 (Cascade Completeness).** Cancellation "
    "propagates to all transitive dependents -- ensures no "
    "orphaned downstream nodes when an upstream is cancelled.",
    title="Invariant I5: cascade completeness -- cancellation propagates transitively (no orphaned dependents)",
)

claim_invariant_6_dependency_completeness = claim(
    "**Invariant I6 (Dependency Completeness).** Every "
    "resolved-state transition triggers forward dependency "
    "resolution, so no dependent is left permanently `pending`. "
    "This is the structural property that prevents silent stalls.",
    title="Invariant I6: dependency completeness -- every resolved transition triggers forward resolution (no pending stragglers)",
)

claim_invariant_7_recovery_correctness = claim(
    "**Invariant I7 (Recovery Correctness).** After a crash, "
    "`processing` nodes reset to `pending` and all nodes with "
    "resolved dependencies are re-scheduled, ensuring the system "
    "resumes from a consistent state. Combined with I3 "
    "(idempotency), this gives crash-recovery semantics.",
    title="Invariant I7: recovery correctness -- crash recovers to consistent state via reset + idempotent re-scheduling",
)

# ---------------------------------------------------------------------------
# Theorems: termination + deadlock-freedom
# ---------------------------------------------------------------------------

claim_theorem_termination = claim(
    "**Theorem (Termination of E2R + DAG execution).** Under the "
    "design constraints -- bounded retry $k_{\\text{retry}}$ "
    "(F2 in the FSM), bounded review-round count "
    "$k_{\\text{rev}}$ (I4), task timeout $T_{\\max}$, and cost "
    "budget $B$ (the three circuit breakers, Section 2.2.3) -- "
    "every task node reaches a terminal state in $F = "
    "\\{\\text{finished}, \\text{cancelled}\\}$ in bounded time, "
    "and the project as a whole reaches a terminal state under "
    "the same bounds. **Assumptions**: the underlying executor "
    "(LLM, tool calls, external services) respects the timeout "
    "contract; all retry counters are finite; the workforce $W$ "
    "remains finite. **Conclusion**: every search episode "
    "terminates in bounded wall-clock time + bounded cost under "
    "AND-tree + FSM semantics.",
    title="Theorem (Termination): every node reaches a terminal state in bounded time/cost under k_retry + k_rev + T_max + B",
)

claim_theorem_deadlock_freedom = claim(
    "**Theorem (Deadlock-Freedom of E2R + DAG execution).** Under "
    "the AND-tree + FSM design, the system is deadlock-free: no "
    "execution state can leave a node permanently `pending` "
    "without being either resolved or cancelled. **Assumptions**: "
    "(a) the DAG invariant I1 holds (no cyclic dependencies, so "
    "the dependency graph admits a topological ordering); (b) the "
    "ready predicate fires on every resolved-state transition "
    "(I6, dependency completeness); (c) the deadlock detector is "
    "active (any state where every non-root is "
    "terminal-or-blocked but root is unresolved is converted to a "
    "`failed` terminal state). **Conclusion**: there is no "
    "reachable state in which a non-terminal node has all "
    "dependencies resolved but is not scheduled, nor any state "
    "where the system silently stalls -- the deadlock detector "
    "converts any such pathological state into a terminal "
    "`failed` outcome.",
    title="Theorem (Deadlock-Freedom): DAG invariant + dependency completeness + deadlock detector => no silent stalls",
)

claim_crash_recovery_property = claim(
    "**Crash recovery is built into the design.** Combining I3 "
    "(idempotency) and I7 (recovery correctness): after a crash, "
    "in-flight `processing` nodes reset to `pending`; the "
    "scheduler re-evaluates `ready` on every node and re-schedules "
    "those whose dependencies have resolved. Idempotent "
    "re-scheduling guarantees that recovery never causes duplicate "
    "side-effects or duplicate spend.",
    title="Property: crash-recovery -- idempotent re-scheduling + processing-to-pending reset (no duplicate execution)",
)

# ---------------------------------------------------------------------------
# Mirror-of-human-enterprise framing
# ---------------------------------------------------------------------------

claim_mirrors_human_enterprise = claim(
    "**The E2R + DAG combination mirrors human-enterprise feedback "
    "mechanisms.** Top-down decomposition mirrors how a human "
    "company decomposes goals into tasks; assigning owners to "
    "leaves mirrors task delegation; the explicit review gate "
    "mirrors deliverable acceptance; the accept-or-redecompose "
    "loop mirrors iterating until quality is met; the bounded "
    "retry + escalation policy mirrors performance-management "
    "consequences. The formal guarantees (termination, "
    "deadlock-freedom) provide what human enterprises implicitly "
    "rely on but rarely formalise.",
    title="Claim: E2R + DAG mirrors human-enterprise feedback (decompose / delegate / review gate / accept-or-iterate / escalate)",
)

__all__ = [
    "setup_and_tree_dag_dependency",
    "setup_and_semantics",
    "setup_task_lifecycle_fsm",
    "setup_scheduling_predicate",
    "setup_bottom_up_propagation",
    "setup_deadlock_detector",
    "claim_invariant_1_dag",
    "claim_invariant_2_mutual_exclusion",
    "claim_invariant_3_schedule_idempotency",
    "claim_invariant_4_review_termination",
    "claim_invariant_5_cascade_completeness",
    "claim_invariant_6_dependency_completeness",
    "claim_invariant_7_recovery_correctness",
    "claim_theorem_termination",
    "claim_theorem_deadlock_freedom",
    "claim_crash_recovery_property",
    "claim_mirrors_human_enterprise",
]
