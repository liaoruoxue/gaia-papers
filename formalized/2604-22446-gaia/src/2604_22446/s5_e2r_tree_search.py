"""Section 2.2: Strategy Search in Vast Organisational Space by E2R Tree
(pages 7-10).

Tree structure (nodes / edges / actions / strategies / policy), three
stages of Explore-Execute-Review, iterated search with the external
oracle, bounded rationality + circuit breakers.

Source: Yu et al. 2026 [@Yu2026OMC], Section 2.2-2.2.3 + Figure 4.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Motivation: organisational decision-making as game-tree search
# ---------------------------------------------------------------------------

setup_organisational_search_space = setting(
    "**Setup: vast organisational decision space.** When a company "
    "receives a project request, the response space is enormous: "
    "decompositions, assignments, accept/reject decisions, and "
    "post-hoc strategy revisions. Existing MAS handle this either "
    "by hardcoding a fixed workflow graph (cannot adapt to novel "
    "projects) or by allowing free agent negotiation (no "
    "convergence guarantees).",
    title="Setup: vast organisational decision space (decompositions / assignments / reviews / revisions)",
)

setup_e2r_mcts_analogy = setting(
    "**E2R draws structural inspiration from MCTS [@MCTS] but "
    "differs.** Both grow a tree incrementally, evaluate nodes "
    "after expansion, and use evaluations to guide subsequent "
    "exploration. **Differences**: E2R does *not* use simulated "
    "rollouts or UCB-based selection; execution is real (agents "
    "produce actual deliverables, not value estimates), and the "
    "review signal comes from *explicit supervisor evaluation* "
    "rather than terminal-reward backpropagation. The analogy is "
    "structural, not algorithmic.",
    title="Setup: E2R is structurally analogous to MCTS [@MCTS] (tree growth + evaluate-and-guide) but uses real execution + supervisor review",
)

# ---------------------------------------------------------------------------
# 2.2.1 Tree structure: nodes, edges, actions, strategies, policy
# ---------------------------------------------------------------------------

setup_tree_definition = setting(
    "**Definition (Search Tree).** "
    "$\\mathcal{T} = (V, E_{\\text{tree}}, E_{\\text{dep}})$ "
    "grows dynamically during project execution. Each node $v \\in V$ "
    "represents the organisational state at a decision point and "
    "carries: $(d_v, e_v, \\phi_v, r_v, c_v, \\mathcal{W}, "
    "\\mathcal{R})$ where $d_v$ is the task description, $e_v \\in "
    "W \\cup \\{\\emptyset\\}$ is the assigned employee from the "
    "current workforce $W$, $\\phi_v \\in \\Phi$ is the FSM status "
    "(Section 2.2.4), $r_v$ is the result, $c_v \\in "
    "\\mathbb{R}_{\\ge 0}$ is the accumulated cost, "
    "$\\mathcal{W}$ is the tree-wide workforce state (employees, "
    "skills, workload, performance history), and $\\mathcal{R}$ is "
    "the resource state (token budget, cost, time).",
    title="Setup: search tree node = (description, assigned employee, FSM status, result, cost) + shared workforce / resource state",
)

setup_two_edge_types = setting(
    "**Definition (Edges).** Two types: "
    "(E1) **Decomposition edges** $E_{\\text{tree}} \\subseteq V "
    "\\times V$ encode strategy -- $(p, v')$ means 'parent $p$ was "
    "decomposed into child $v'$'. These form a strict tree (each "
    "child has exactly one parent). "
    "(E2) **Dependency edges** $E_{\\text{dep}} \\subseteq V "
    "\\times V$ encode execution ordering -- $(u, v)$ means '$v$ "
    "cannot begin until $u$ is accepted'. These can cross sibling "
    "branches. The combined graph $G = (V, E_{\\text{tree}} \\cup "
    "E_{\\text{dep}})$ must be a DAG, enforced at insertion time "
    "via DFS cycle detection.",
    title="Setup: two edge types -- decomposition (tree) + dependency (DAG); combined graph DAG-invariant enforced at insert",
)

setup_five_action_types = setting(
    "**Definition (Action Set).** "
    "$\\mathcal{A} = \\mathcal{A}_{\\text{decompose}} \\cup "
    "\\mathcal{A}_{\\text{assign}} \\cup "
    "\\mathcal{A}_{\\text{recruit}} \\cup "
    "\\mathcal{A}_{\\text{review}} \\cup "
    "\\mathcal{A}_{\\text{iterate}}$. "
    "$\\mathcal{A}_{\\text{decompose}}$ adds children under a node; "
    "$\\mathcal{A}_{\\text{assign}}$ binds an employee to a leaf; "
    "$\\mathcal{A}_{\\text{recruit}}$ hires a new employee from "
    "the Talent Market when a capability is missing (Section "
    "2.1.2); $\\mathcal{A}_{\\text{review}}$ transitions a node's "
    "status (accept or reject); "
    "$\\mathcal{A}_{\\text{iterate}}$ creates a new root-level "
    "iteration with an updated strategy.",
    title="Setup: five action types -- decompose / assign / recruit / review / iterate",
)

setup_strategy_and_transition = setting(
    "**Definition (Strategy + Structural Transition).** A "
    "strategy $\\sigma = (a_1, a_2, \\ldots, a_m)$ is a sequence "
    "of actions $a_i \\in \\mathcal{A}$. The structural transition "
    "function $T$ deterministically maps "
    "$(\\mathcal{T}, a) \\mapsto T(\\mathcal{T}, a)$ -- adding "
    "nodes, updating edges, changing statuses. Stochasticity "
    "enters during the Execute stage where each agent's internal "
    "reasoning is non-deterministic.",
    title="Setup: strategy = sequence of actions; transition T is deterministic over tree structure (stochasticity is in Execute)",
)

setup_policy_pi = setting(
    "**Definition (Policy $\\pi$).** A policy maps the current "
    "tree to a strategy: "
    "$\\pi(\\mathcal{T}) = \\sigma = (\\alpha_d(v, \\{v'_1, "
    "\\ldots, v'_n\\}), \\alpha_a(v'_1, e_1), \\ldots, "
    "\\alpha_a(v'_n, e_n))$ where $v$ is the node to expand, "
    "$\\{v'_i\\}$ are new child tasks, $\\alpha_d$ decomposes, "
    "$\\alpha_a$ assigns, and $e_i$ is the employee assigned to "
    "$v'_i$ (possibly via a recruit action). The composite operator "
    "$\\Delta(v, e, d, D)$ creates one child with description $d$, "
    "assigns employee $e$, and registers dependency edges $D$. In "
    "the current implementation, $\\pi$ is realised by the "
    "supervising agent (e.g., COO or a senior employee) reasoning "
    "over project state, employee profiles, and history.",
    title="Setup: policy pi -- supervising agent jointly decides decomposition granularity + employee assignment per decision point",
)

# ---------------------------------------------------------------------------
# Three stages of E2R (page 9)
# ---------------------------------------------------------------------------

claim_stage_1_explore = claim(
    "**Stage 1: Explore (strategy selection + task tree "
    "expansion).** Executive agents apply $\\pi(\\mathcal{T})$ to "
    "select how to decompose the current task and whom to assign. "
    "This stage faces the classic exploration-exploitation "
    "trade-off: assign tasks to employees with proven track records "
    "(exploitation) or try less-tested employees / hire a new one "
    "(exploration). The branching factor is unbounded since the "
    "LLM decides decomposition granularity at runtime.",
    title="Stage 1 (Explore): apply pi to select decomposition + assignment (unbounded branching factor decided at runtime by LLM)",
)

claim_stage_2_execute = claim(
    "**Stage 2: Execute (agents carry out assigned work).** Each "
    "assigned employee executes its task through the "
    "organisational layer (Section 2.1). Let $f_{e_v}$ denote the "
    "internal execution function of employee $e_v$, taking the "
    "task description $d_v$ and producing $(r_v, c_v) = f_{e_v}"
    "(d_v)$. The internal $f$ is determined by the agent's own "
    "loop (reasoning, tool use, code generation) and, for "
    "closed-source agents such as Claude, is opaque to the "
    "organisational layer. The DAG execution layer (Section 2.2.4) "
    "formalises dependency resolution and termination guarantees "
    "for this stage.",
    title="Stage 2 (Execute): (r_v, c_v) = f_{e_v}(d_v) -- internal execution opaque to org layer; DAG layer formalises dependencies",
)

claim_stage_3_review = claim(
    "**Stage 3: Review (quality signals propagate and drive "
    "iteration).** For each completed node a reviewer (typically "
    "the parent owner or COO) evaluates $r_v$ and produces a "
    "quality signal $q_v \\in \\{\\text{accept}, "
    "\\text{reject}\\}$, triggering the corresponding FSM "
    "transition. Review signals propagate bottom-up from leaves "
    "to root, accumulating into per-node review signal vectors "
    "$g(v) = (q_v, c_v, \\phi_v)$ for $v \\in "
    "\\text{path}(\\text{leaf}, \\text{root})$. Accept unblocks "
    "dependents or resolves the parent; reject re-enters Stage 1, "
    "growing a fresh subtree under the same parent with updated "
    "context from the failed attempt. This accept-or-redecompose "
    "cycle continues until the root is resolved or a circuit "
    "breaker fires (Section 2.2.3).",
    title="Stage 3 (Review): bottom-up propagation of accept/reject; reject re-enters Stage 1 (accept-or-redecompose loop)",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Figure 4 (page 9)",
    },
)

# ---------------------------------------------------------------------------
# Top-down decomposition + bottom-up aggregation (key architectural claim)
# ---------------------------------------------------------------------------

claim_top_down_bottom_up_unification = claim(
    "**E2R unifies planning, execution, and evaluation in a "
    "single hierarchical loop.** Tasks are decomposed top-down "
    "into accountable units (Stage 1 + Stage 2); execution outcomes "
    "are aggregated bottom-up (Stage 3) to drive systematic review "
    "and refinement. Unlike pipeline systems that separate "
    "planning, execution, and evaluation into distinct phases, E2R "
    "interleaves all three within a single tree-structured search "
    "process.",
    title="E2R: unifies planning + execution + evaluation in one loop (top-down decomposition + bottom-up aggregation)",
)

# ---------------------------------------------------------------------------
# 2.2.2 Iterated search with external oracle
# ---------------------------------------------------------------------------

setup_policy_update_function = setting(
    "**Definition (Policy Update $\\Pi$).** Each iteration "
    "(`iter_001`, `iter_002`, ...) is one search episode. The "
    "policy update function refines $\\pi$ across iterations: "
    "$\\pi_{k+1} = \\Pi(\\mathcal{T}_k, \\pi_k, \\mathcal{H}_k)$, "
    "with $\\mathcal{H}_k = \\{(v, r_v, c_v, q_v)\\}_{v \\in "
    "\\text{completed}}$ accumulating results, costs, and review "
    "signals. In the current implementation $\\pi$ is *not* a "
    "parameterised policy updated by gradient methods; rather "
    "$\\Pi$ enriches the supervising agent's context (history, "
    "updated employee profiles, revised SOPs) so subsequent calls "
    "to $\\pi$ produce better strategies.",
    title="Setup: policy update Pi -- enriches supervising-agent context (history + profiles + SOPs); not gradient-based",
)

claim_external_oracle_role = claim(
    "**The CEO acts as an external oracle providing three types of "
    "intervention.** (O1) **policy override** -- directly "
    "rejecting or redirecting a decomposition strategy; "
    "(O2) **requirement injection** -- adding new constraints "
    "mid-search ('add SEO support', 'change the architecture'); "
    "(O3) **iteration triggering** -- deciding when to launch a "
    "new search episode and when to stop. The CEO is modelled as a "
    "meta-level controller [@RussellWefald] applying domain-"
    "informed optimal stopping. The trade-off: convergence depends "
    "on human judgment quality rather than formal guarantees.",
    title="Claim: CEO = external oracle providing override / requirement-injection / iteration-triggering (meta-level controller [@RussellWefald])",
)

# ---------------------------------------------------------------------------
# 2.2.3 Bounded rationality and circuit breakers
# ---------------------------------------------------------------------------

setup_three_circuit_breakers = setting(
    "**Three circuit breakers (Section 2.2.3).** Real "
    "organisations cannot run infinite simulations. With "
    "$n_{\\text{rev}}(v)$ = number of review rounds, "
    "$t_{\\text{exec}}(v)$ = wall-clock execution time, "
    "$\\text{esc}(v)$ = escalation to a higher-level supervisor:\n\n"
    "(B1) **Review-round limit** -- "
    "$n_{\\text{rev}}(v) \\ge k_{\\text{rev}} \\Rightarrow "
    "\\text{esc}(v)$ (default $k_{\\text{rev}} = 3$).\n"
    "(B2) **Task timeout** -- $t_{\\text{exec}}(v) > T_{\\max} "
    "\\Rightarrow \\phi_v \\gets \\text{failed}$ (default "
    "$T_{\\max} = 3600$s).\n"
    "(B3) **Cost budget** -- $\\sum_{v \\in V} c_v > B "
    "\\Rightarrow \\text{pause}$.\n\n"
    "All three are configurable. Together they guarantee every "
    "search episode terminates in bounded time and cost under the "
    "assumption that the underlying executor (LLM, tool calls, "
    "external services) respects the timeout contract.",
    title="Setup: three circuit breakers -- review-round limit (k_rev=3) / task timeout (T_max=3600s) / cost budget B",
)

claim_circuit_breakers_imply_bounded_termination = claim(
    "**Circuit breakers imply bounded-time, bounded-cost "
    "termination.** Every search episode is guaranteed to "
    "terminate within bounded time and bounded cost: the "
    "review-round limit caps escalation depth; the task timeout "
    "caps wall-clock per node; the cost budget caps cumulative "
    "spend. Termination of the *episode* is therefore a direct "
    "consequence of the three breakers (under the executor-"
    "respects-timeout assumption). The stronger guarantees on the "
    "execution layer itself (deadlock-freedom, AND-tree "
    "completion) are formalised in Section 2.2.4.",
    title="Claim: three circuit breakers => every E2R episode terminates in bounded time + cost (under executor timeout assumption)",
)

# ---------------------------------------------------------------------------
# Integrated function I (combined E2R + DAG)
# ---------------------------------------------------------------------------

setup_iteration_function_iter = setting(
    "**Definition (Iteration function $\\mathcal{I}$).** Each "
    "search iteration combines E2R + DAG execution into "
    "$(\\bar{r}, \\bar{c}, \\bar{q}) = \\mathcal{I}(\\mathcal{T}, "
    "a) = \\mathcal{S}_{\\text{DAG}}(T(\\mathcal{T}, a))$, where "
    "$T(\\mathcal{T}, a)$ is the successor tree under decomposition "
    "action $a$, $\\mathcal{S}_{\\text{DAG}}$ is the DAG scheduler "
    "(Section 2.2.4), and $(\\bar{r}, \\bar{c}, \\bar{q})$ are the "
    "aggregated result, cost, and quality signals returned to the "
    "review phase.",
    title="Setup: iteration function I = S_DAG composed with structural transition T (aggregates result + cost + quality)",
)

__all__ = [
    "setup_organisational_search_space",
    "setup_e2r_mcts_analogy",
    "setup_tree_definition",
    "setup_two_edge_types",
    "setup_five_action_types",
    "setup_strategy_and_transition",
    "setup_policy_pi",
    "claim_stage_1_explore",
    "claim_stage_2_execute",
    "claim_stage_3_review",
    "claim_top_down_bottom_up_unification",
    "setup_policy_update_function",
    "claim_external_oracle_role",
    "setup_three_circuit_breakers",
    "claim_circuit_breakers_imply_bounded_termination",
    "setup_iteration_function_iter",
]
