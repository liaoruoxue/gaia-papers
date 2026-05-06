"""Section 3: ContextWeaver framework setup -- formal problem statement and
graph-construction algorithm overview.

Section 3 (and Section 3 preamble) of [@Wu2026ContextWeaver]. This module
captures the formal scaffolding: agent history representation, the
high-level pipeline (Algorithm 1), the four-step procedure (Node Extraction,
Parent Selection, Ancestry Dependency Construction, Context Weaving), and
its core hyperparameters (warmup window W, max parents m).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Formal problem setup
# ---------------------------------------------------------------------------

setup_node_definition = setting(
    "**Node structure $N_k = (\\text{summary}, \\text{dependency "
    "summary}, \\text{parents}, \\text{validation})$.** ContextWeaver "
    "converts each tool-use step $H_k = \\{T_k, A_k, O_k\\}$ into a "
    "structured *Node* containing: (a) **summary** -- a condensed "
    "representation of the agent's thought, action, and resulting "
    "observation; (b) **dependency summary** -- a concise narrative of "
    "the reasoning dependency paths leading to the node "
    "(see Section 3.2); (c) **parents** -- the node's connections within "
    "a directed acyclic graph (DAG); and (d) **validation** -- "
    "node-level outcomes from the validation layer "
    "(see Section 3.3) [@Wu2026ContextWeaver, Sec. 3.1].",
    title="Setup: Node = (summary, dependency_summary, parents, validation)",
)

setup_node_extraction_map = setting(
    "**Node-extraction mapping $\\phi(H_k, Q)$.** A node-extraction "
    "function $\\phi$ takes the most recent history step $H_k$ and the "
    "user query $Q$ and produces $N_k$. The mapping summarizes the "
    "latest step *given the query*, so the produced node is "
    "task-relevant rather than a generic summary "
    "[@Wu2026ContextWeaver, Sec. 3.1, Eq. for $\\phi$].",
    title="Setup: node extractor phi(H_k, Q) -> N_k summarizes given the query",
)

setup_dag_structure = setting(
    "**Dependency graph is a directed acyclic graph (DAG).** "
    "ContextWeaver organizes operations *not by recency but by "
    "information flow*. Each node $N_k$ may have multiple parents (up to "
    "$m$), so the graph supports branching and merging across parallel "
    "lines of reasoning. This DAG structure allows a node to depend on "
    "*several* earlier nodes rather than being confined to a single "
    "linear chain or tree [@Wu2026ContextWeaver, Sec. 3.1].",
    title="Setup: dependency graph is a DAG (multiple parents per node)",
)

setup_hyperparameters = setting(
    "**Hyperparameters: warmup window $W$ and max parents $m$.** "
    "Algorithm 1 takes two hyperparameters: $W$ (the warmup window size, "
    "which also bounds the size of the ancestry subgraph), and $m$ (the "
    "maximum number of parents per node returned by the dependency "
    "analyzer). All experiments use a single shared configuration with "
    "$W = 5$, matching the sliding-window baseline "
    "[@Wu2026ContextWeaver, Sec. 3.1, Sec. 4.1].",
    title="Setup: hyperparameters W (warmup) and m (max parents); W=5 throughout",
)

# ---------------------------------------------------------------------------
# Algorithm 1: high-level pipeline
# ---------------------------------------------------------------------------

claim_algorithm1_steps = claim(
    "**Algorithm 1 has four sequential steps: Node Extraction -> Parent "
    "Selection -> Ancestry Dependency Construction -> Context Weaving.** "
    "Given history $H$ and query $Q$, ContextWeaver: (1) converts the "
    "latest entry $H_k$ into structured node $N_k$ via "
    "$\\phi(H_k, Q)$; (2) selects up to $m$ parents $S_k$ from the "
    "current valid candidates and adds edges $N_i \\to N_k$ for $N_i "
    "\\in S_k$; (3) collects the ancestry set $A$ via breadth-first "
    "traversal upward through the dependency graph (until $|A| < W$); "
    "and (4) weaves the final context $C$ retaining full $T$-$A$-$O$ "
    "triples for ancestors and compressing observations of "
    "non-ancestors [@Wu2026ContextWeaver, Algorithm 1, Sec. 3.1].",
    title="Algorithm 1: extract -> select parents -> ancestry BFS -> weave context",
)

claim_warmup_branch = claim(
    "**Warmup branch: when $|H| \\leq W$, return the full history "
    "unchanged.** Algorithm 1 short-circuits during the warmup phase: "
    "if the history length is at most the warmup window $W$, the full "
    "history is returned directly (along with the updated graph), with "
    "no compression. This ensures that early steps -- which may carry "
    "essential context with no ancestry yet to traverse -- are kept in "
    "full [@Wu2026ContextWeaver, Algorithm 1, lines 8-10].",
    title="Algorithm 1 warmup: |H| <= W => return full history",
)

claim_local_incremental_design = claim(
    "**ContextWeaver is local and incremental, not full-history "
    "reprocessing.** Instead of reprocessing the full history at every "
    "step, ContextWeaver extends the dependency graph with new nodes "
    "and selectively updates node validity through the Validation Layer. "
    "This design enables efficient updates and makes ContextWeaver "
    "suitable for long-running agent sessions "
    "[@Wu2026ContextWeaver, Sec. 3.1].",
    title="Design choice: local + incremental graph updates (not full-history rebuild)",
)

claim_dag_information_flow = claim(
    "**The DAG organizes operations by information flow rather than "
    "recency.** A reasoning step $N_k$ is a child of $N_i$ when the "
    "later step *depends on* information produced or referenced by the "
    "earlier step, regardless of how many recency-adjacent steps "
    "intervene. This information-flow organization is what enables "
    "the dependency-aware retrieval that distinguishes ContextWeaver "
    "from sliding-window or similarity-based methods "
    "[@Wu2026ContextWeaver, Sec. 3.1].",
    title="Information-flow organization: parent edges follow dependency, not adjacency",
)

# ---------------------------------------------------------------------------
# Output of the framework
# ---------------------------------------------------------------------------

claim_weaved_context_definition = claim(
    "**Weaved context = validated ancestor full $T$-$A$-$O$ triples + "
    "compressed observations for non-ancestors.** The output of the "
    "ContextWeaver pipeline is a *weaved* context $C$ that includes "
    "(i) only validated nodes' supporting dependencies, with full "
    "thought-action-observation detail; and (ii) for all other history "
    "entries, retains $T_i$ and $A_i$ but compresses $O_i$ to a "
    "lightweight placeholder. This forms a selective, dependency-aware "
    "memory state that preserves key evidence for the next action under "
    "strict token constraints "
    "[@Wu2026ContextWeaver, Sec. 3.1, Appendix D].",
    title="Output: weaved context C = full ancestors + observation-compressed non-ancestors",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "setup_node_definition",
    "setup_node_extraction_map",
    "setup_dag_structure",
    "setup_hyperparameters",
    "claim_algorithm1_steps",
    "claim_warmup_branch",
    "claim_local_incremental_design",
    "claim_dag_information_flow",
    "claim_weaved_context_definition",
]
