"""Section 4 (Layer 1): Control architecture.

Section 4.1 of Rombaut 2026 [@Rombaut2026]. Three dimensions
characterize the control layer: (4.1.1) control loop topology, (4.1.2)
loop driver, (4.1.3) control flow implementation. The headline
loop-primitive thesis -- that 11 of 13 agents compose multiple loop
primitives -- is anchored here.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 4.1.1 Control loop strategies (Table 2) -- a 6-position spectrum
# ---------------------------------------------------------------------------

claim_table2_control_loops = claim(
    "**Table 2 -- control loop strategies (Section 4.1.1).** Agents "
    "ordered from least to most flexible exploration strategy. "
    "These loop types are not mutually exclusive; agents frequently "
    "nest one loop type inside another (e.g. AutoCodeRover runs a "
    "multi-turn LLM interaction inside each stage of its pipeline).\n\n"
    "| Position | Agents | Mechanism |\n"
    "|---|---|---|\n"
    "| **Fixed pipeline** | Agentless | 10-stage pipeline of independent scripts connected by JSONL files. No feedback loop between stages. |\n"
    "| **User-driven loop** | Aider | Outer loop is user-initiated. Inner generate-test-repair loop is autonomous for up to `max_reflections` iterations. |\n"
    "| **Sequential ReAct loop** | SWE-agent, OpenHands, Codex CLI, Gemini CLI, mini-swe-agent, Cline, OpenCode | Standard thought-tool-observation cycle. LLM selects next action; loop terminates on completion signal or budget exhaustion. |\n"
    "| **Phased loop** | AutoCodeRover, Prometheus | Distinct stages with different tool access. AutoCodeRover: search-then-patch phase separation. Prometheus: LangGraph state machine [@LangGraph2024] with explicit edges. |\n"
    "| **Depth-first tree search** | DARS-Agent | ReAct steps form nodes in a search tree. At branch points, the environment is reset and replayed from root; an LLM critic selects among sampled alternatives. |\n"
    "| **Full MCTS** | Moatless Tools | Select-Expand-Simulate-Backpropagate with reward values ($-100$ to $+100$) and visit counts. Pluggable selector interface; a discriminator selects the best finished trajectory. |\n",
    title="Table 2: 6-position control loop spectrum across the 13 agents",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 2"},
)

claim_loop_types_compose = claim(
    "**Loop types nest and compose, not mutually exclusive.** Agents "
    "frequently nest one loop type inside another. AutoCodeRover "
    "runs a multi-turn LLM interaction inside each stage of its "
    "pipeline (`agent_search.py:88--163`): a generator function "
    "yields tool selections to the caller, which executes them and "
    "sends results back, making it simultaneously a phased agent "
    "and an iterative agent depending on the level of abstraction. "
    "**Moatless Tools** takes composability further by decoupling "
    "the inner agent from the outer control flow: its `ActionAgent` "
    "(a single-step executor) can be driven either by `AgenticLoop` "
    "(repeatedly producing ReAct behavior) or by `SearchTree` for "
    "MCTS-based exploration, with no changes to the agent code "
    "itself. This separation makes sequential vs tree-search a "
    "configuration choice rather than an architectural one.",
    title="4.1.1 control loops nest -- composability is built into Moatless Tools' design",
)

claim_tree_search_gradient = claim(
    "**Tree-search gradient: 3 agents from flat sampling to MCTS "
    "(Section 4.1.1).** Three agents span a gradient from flat "
    "sampling to informed search:\n\n"
    "* **Agentless** uses *independent sampling*: after localizing "
    "code, it prompts the LLM to generate ~20 candidate patches "
    "independently, each from the same context, then selects the "
    "final patch by majority vote. No tree structure, no "
    "interaction between candidates.\n"
    "* **DARS-Agent** introduces *tree-structured search* into its "
    "main loop. Each node represents an action (edit, create, "
    "submit). At branch points, the agent generates multiple "
    "alternative actions; an LLM critic returns a `<best action "
    "index>` tag. **No numeric rewards, no backpropagation** -- "
    "greedy local decisions only.\n"
    "* **Moatless Tools** implements full *Monte Carlo Tree "
    "Search* (MCTS) [@Browne2012MCTS] -- the same algorithm as "
    "AlphaGo [@Silver2016AlphaGo]. Each node receives numeric "
    "rewards ($-100$ to $+100$); visit counts balance "
    "exploration/exploitation; rewards backpropagate up the tree "
    "(`search_tree.py:326--345`).\n\n"
    "The progression reveals a tradeoff: richer search requires a "
    "branch-state-management mechanism (Moatless: in-memory shadow "
    "execution; DARS: Docker reset and replay).",
    title="4.1.1 3-agent tree-search gradient: flat sampling -> greedy tree -> MCTS",
)

claim_react_band = claim(
    "**Sequential ReAct band: 7 of 13 agents (Section 4.1.1).** "
    "**Seven of the 13 agents use a sequential ReAct loop "
    "[@Yao2023ReAct] as their primary control structure**: "
    "SWE-agent, OpenHands, Codex CLI, Gemini CLI, mini-swe-agent, "
    "Cline, OpenCode. The remaining CLI agents (Cline, Codex CLI, "
    "Gemini CLI, OpenCode) all implement standard sequential ReAct "
    "loops without phased structure or tree search. **Aider** is "
    "a special case in this band: it appears as 'user-driven' "
    "since the LLM has zero callable tools and the outer loop is "
    "user-initiated, but its inner loop "
    "(`base_coder.py:932`) is autonomous -- after the LLM produces "
    "edits, the scaffold runs linting and tests, and if either "
    "fails, re-prompts the LLM with the error output for up to "
    "`max_reflections` iterations. This generate-test-repair cycle "
    "is the only part of Aider where multi-turn LLM interaction "
    "occurs without user input.",
    title="4.1.1 7/13 agents use sequential ReAct as primary control structure",
)

claim_loop_primitives_thesis = claim(
    "**Loop primitive thesis (Section 4.1.1).** **Five loop "
    "primitives** function as composable building blocks across the "
    "corpus, not as mutually exclusive types:\n\n"
    "1. **ReAct** (interleaved thought / tool call / observation) "
    "-- 7 of 13 agents use it as primary; many embed it as a sub-loop.\n"
    "2. **Generate-test-repair** (run tests; if they fail, re-prompt "
    "the LLM with the error and retry) -- foundational primitive "
    "[@Shinn2023Reflexion] visible in Aider, OpenHands, SWE-agent, "
    "Cline, OpenCode, etc.\n"
    "3. **Plan-execute** (separate planning phase that produces a "
    "plan, then an execution phase that follows it) -- visible in "
    "AutoCodeRover, Prometheus, OpenCode (plan agent), Cline (plan "
    "mode).\n"
    "4. **Multi-attempt retry** (generate multiple complete "
    "attempts and select the best) -- visible in SWE-agent's "
    "RetryAgent, Agentless, AutoCodeRover (model cycling).\n"
    "5. **Tree search** (explicit tree-structured exploration) -- "
    "visible in DARS-Agent (greedy) and Moatless Tools (MCTS).",
    title="4.1.1 the 5 loop primitives: ReAct, generate-test-repair, plan-execute, retry, tree search",
)

claim_eleven_of_thirteen_compose = claim(
    "**11 of 13 agents compose multiple loop primitives "
    "(Section 4.1.1).** **Eleven of the 13 agents layer multiple "
    "loop primitives** rather than relying on a single control "
    "structure. The two pure single-loop exceptions are:\n\n"
    "* **Agentless** -- pipeline only.\n"
    "* **mini-swe-agent** -- ReAct only.\n\n"
    "Both are **deliberately minimalist**, designed to demonstrate "
    "that simpler scaffolds suffice for many tasks. All 11 other "
    "agents combine at least two primitives (e.g. "
    "ReAct + generate-test-repair in OpenHands; "
    "phased + ReAct + multi-attempt-retry + tree search in "
    "Moatless Tools).",
    title="4.1.1 11/13 agents compose multiple primitives; only Agentless + mini-swe-agent are pure",
)

# ---------------------------------------------------------------------------
# 4.1.2 Loop driver (Table 3) -- arguably most fundamental
# ---------------------------------------------------------------------------

claim_table3_loop_driver = claim(
    "**Table 3 -- loop driver strategies (Section 4.1.2).** Three "
    "positions: who decides what happens next?\n\n"
    "| Driver | Agents | Mechanism |\n"
    "|---|---|---|\n"
    "| **User-driven** | Aider | The LLM has 0 callable tools. The user selects files (`/add`), runs searches, and provides context. The LLM produces edits in a text format parsed by the scaffold (`base_coder.py:2296--2304`). |\n"
    "| **Scaffold-driven** | Agentless, AutoCodeRover | The scaffold controls sequencing and calls the LLM at fixed points. In Agentless, each LLM call is single-turn with no conversation state. In AutoCodeRover, the scaffold manages phase transitions across up to four stages. |\n"
    "| **LLM-driven** | SWE-agent, OpenHands, Codex CLI, Gemini CLI, Cline, mini-swe-agent, Moatless Tools, DARS-Agent, OpenCode (and Prometheus as hybrid) | The LLM selects tools and controls exploration. Prometheus is a hybrid: within each graph node the LLM drives tool selection via ReAct, but transitions between nodes are scaffold-controlled. |\n",
    title="Table 3: 3 loop drivers -- user (Aider), scaffold (2), LLM (10) ",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 3"},
)

claim_loop_driver_distribution = claim(
    "**Loop-driver distribution (Section 4.1.2).** Aider sits at "
    "one extreme: the LLM never runs `grep`, never opens a file it "
    "was not given, and never decides 'I should look at module Y' "
    "-- all navigation responsibility falls on the user. At the "
    "other extreme, **9 of 13 agents** give the LLM full autonomy "
    "over tool selection. Prometheus occupies a hybrid position. "
    "Between the poles, Agentless and AutoCodeRover (2 of 13) "
    "occupy a scaffold-driven intermediate position where the "
    "scaffold sequences phases but the LLM makes decisions within "
    "each phase.",
    title="4.1.2 loop-driver distribution: 1 user / 2 scaffold / 9 LLM / 1 hybrid",
)

claim_loop_driver_most_fundamental = claim(
    "**Loop driver as the most fundamental architectural distinction "
    "(Section 4.1.2).** The loop driver is **arguably the most "
    "fundamental architectural distinction** in the corpus, with "
    "implications beyond control flow. **User-driven agents "
    "sidestep the bug-localization bottleneck** identified in prior "
    "trajectory analyses [@Ceka2025]: if the user selects files, "
    "incorrect localization is a user error, not an agent failure. "
    "**LLM-driven agents must solve localization** as part of the "
    "task, making retrieval strategy (Section 4.2.4) a critical "
    "co-design choice. The same model performing well with "
    "user-curated context may struggle when forced to navigate a "
    "repository autonomously.",
    title="4.1.2 loop driver is the most fundamental: it determines retrieval co-design",
)

# ---------------------------------------------------------------------------
# 4.1.3 Control flow implementation (Table 4) -- code-level mechanism
# ---------------------------------------------------------------------------

claim_table4_control_flow = claim(
    "**Table 4 -- control flow implementation (Section 4.1.3).** "
    "The semantic loop types above are implemented through five "
    "distinct *code-level* mechanisms, orthogonal to loop topology.\n\n"
    "| Implementation | Agents | Notes |\n"
    "|---|---|---|\n"
    "| **Imperative while loop** | SWE-agent, OpenHands, Codex CLI, Gemini CLI, mini-swe-agent, Aider, OpenCode | The default for 7 of 13 agents. |\n"
    "| **Fixed pipeline (no loop)** | Agentless | Sequential scripts; each LLM call is single-turn. The Anthropic path contains a bounded `for` loop (up to 10 iterations, `model.py:148--284`), but the primary architecture has no loop. |\n"
    "| **Recursion** | Cline | `recursivelyMakeClineRequests` (`task/index.ts:2268`). Call stack grows linearly with conversation length. Only instance of recursion for the main agent loop in the corpus. |\n"
    "| **Graph-as-control-flow** | Prometheus | LangGraph compiled state machine with explicit edges (`issue_graph.py:22--134`). Cycles in the graph create loops; recursion limits (30 for IssueBugSubgraph, 150 for BugReproductionSubgraph) serve as termination guarantee. At least four levels of subgraph nesting. |\n"
    "| **Exception-based signalling** | mini-swe-agent | `InterruptAgentFlow` hierarchy (`Submitted`, `LimitsExceeded`, `FormatError`) carries messages as payloads. The `run()` method catches these, injects messages into history, and either continues or breaks (`default.py:88--96`). |\n",
    title="Table 4: 5 control-flow implementations; 7/13 use imperative while loop",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 4"},
)

claim_graph_qualitatively_different = claim(
    "**The graph approach is qualitatively different (Section 4.1.3).** "
    "Prometheus's graph-based approach is **qualitatively different** "
    "from the others: control flow is **inspectable, serializable, "
    "and checkpointable** by the framework. Subgraphs define their "
    "own state types, and each subgraph is wrapped in a "
    "`SubgraphNode` class that translates between the parent and "
    "child graph states. Example: the parent `IssueState` holds "
    "`issue_title`, `issue_body`, and `issue_comments`; the "
    "`IssueBugSubgraphNode` wrapper passes these as keyword "
    "arguments to `IssueBugSubgraph.invoke()`. At least four "
    "levels of nesting exist: `IssueGraph -> IssueBugSubgraph -> "
    "IssueVerifiedBugSubgraph -> ContextRetrievalSubgraph`.",
    title="4.1.3 graph approach (Prometheus) is uniquely inspectable/serializable",
)

claim_cline_recursion = claim(
    "**Cline uses recursion (Section 4.1.3).** Cline's recursive "
    "implementation is the only instance of recursion for the main "
    "agent loop in the corpus. While semantically equivalent to "
    "iteration, the JavaScript call stack grows with each tool-use "
    "turn. Node.js default stack limits (typically thousands of "
    "frames) are unlikely to be reached during normal sessions, "
    "but the design has architectural consequences: each recursive "
    "frame retains local state, making the control flow harder to "
    "serialize or checkpoint compared to iterative approaches.",
    title="4.1.3 Cline's recursion is unique; harder to serialize than iteration",
)

claim_opencode_event_bus = claim(
    "**OpenCode layers a global publish-subscribe event bus "
    "(Section 4.1.3).** Within the imperative-while-loop group, "
    "**OpenCode** is architecturally distinctive for layering a "
    "global publish-subscribe event bus on top of its while loop "
    "(`packages/opencode/src/bus/`). Components communicate via "
    "typed events rather than direct function calls. **No other "
    "CLI agent in the corpus uses an event bus for "
    "inter-component communication**; OpenHands uses event "
    "sourcing for state management (Section 4.3.1), but its event "
    "stream serves a different purpose (persistence and replay) "
    "than OpenCode's pub/sub bus (decoupled runtime communication).",
    title="4.1.3 OpenCode is unique: pub/sub event bus for inter-component communication",
)

__all__ = [
    "claim_table2_control_loops",
    "claim_loop_types_compose",
    "claim_tree_search_gradient",
    "claim_react_band",
    "claim_loop_primitives_thesis",
    "claim_eleven_of_thirteen_compose",
    "claim_table3_loop_driver",
    "claim_loop_driver_distribution",
    "claim_loop_driver_most_fundamental",
    "claim_table4_control_flow",
    "claim_graph_qualitatively_different",
    "claim_cline_recursion",
    "claim_opencode_event_bus",
]
