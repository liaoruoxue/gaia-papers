"""Section 4.3 (Layer 3): Resource management.

Section 4.3 of Rombaut 2026 [@Rombaut2026]. Four dimensions
characterize the resource layer: (4.3.1) state management, (4.3.2)
context compaction, (4.3.3) multi-model routing, (4.3.4) persistent
memory. The layer's headline finding is *deep divergence on open
design questions* -- 7 distinct compaction strategies, 8 state
management variants, multi-model routing from single-model to 7-layer
classifier chains.

Section 4.4 cross-cutting themes (sampling vs iteration; sub-agent
delegation; online vs offline selection; ecosystem maturity; IDE as
architecture) are also extracted here as the cross-cutting findings
that the open-ended tenth section captured.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 4.3.1 State management (Table 10) -- 8 variants
# ---------------------------------------------------------------------------

claim_table10_state_management = claim(
    "**Table 10 -- state management strategies (Section 4.3.1).** "
    "Eight distinct variants from destructive overwrite to event "
    "sourcing.\n\n"
    "| Strategy | Agents |\n"
    "|---|---|\n"
    "| **Destructive** | Aider: summarization overwrites `done_messages` (`base_coder.py:1024--1034`). |\n"
    "| **Flat list, preserved** | SWE-agent, Codex CLI, Gemini CLI: raw history kept; filtered views created for LLM. mini-swe-agent: raw history kept with no filtering. |\n"
    "| **Typed event log** | OpenCode: SQLite-backed message/part hierarchy with 12 part types (Drizzle ORM). Append-only messages with mutable part states (`message-v2.ts`). |\n"
    "| **Graph-scoped** | Prometheus: separate message lists per graph node (`edit_messages`, `analyzer_messages`, `context_provider_messages`), reset at retry boundaries. |\n"
    "| **Tree-structured (MCTS)** | Moatless Tools: nodes in a tree with per-node file-context snapshots, visit counts, and reward values. |\n"
    "| **Tree-structured (greedy)** | DARS-Agent: nodes with per-node expansion candidates and critic responses (`dars_agent.py:294--297`). No MCTS statistics; state recovered via Docker reset and action replay. |\n"
    "| **Event-sourced** | OpenHands: immutable `EventStream`; views computed from condensation markers (`memory/view.py:13--96`) [@Fowler2005EventSourcing]. |\n"
    "| **No conversation state** | Agentless: each LLM call is single-turn; pipeline state stored as JSONL files on disk. |\n",
    title="Table 10: 8 state-management variants -- destructive to event sourcing",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 10"},
)

claim_state_management_extremes = claim(
    "**Two extremes of state management (Section 4.3.1).** "
    "**Aider's two-list design** (`cur_messages` and "
    "`done_messages`) is simple but **destructive**: summarization "
    "*replaces* the contents of `done_messages`. **OpenHands' "
    "event-sourced architecture** [@Fowler2005EventSourcing] "
    "stores immutable events and computes views via the `View` "
    "class; condensation **inserts markers** rather than deleting "
    "events, preserving the full audit trail. Between these "
    "extremes, OpenCode's SQLite-backed hierarchy uses "
    "append-only messages with **12 typed part variants** -- the "
    "most granular state representation in the corpus after "
    "OpenHands and the only one **backed by a relational "
    "database** rather than in-memory structures.",
    title="4.3.1 state extremes: Aider destructive overwrite vs OpenHands immutable event sourcing",
)

claim_agentless_no_state = claim(
    "**Agentless has no conversation state (Section 4.3.1).** "
    "Agentless sits at the opposite end of the spectrum: it has "
    "**no conversation state at all** since each LLM call is "
    "single-turn. State between pipeline stages is represented as "
    "*immutable JSONL files on disk*, one JSON object per problem "
    "instance per line. This file-based state bus makes the "
    "pipeline trivially **resumable** (`--skip_existing` checks "
    "instance presence in output) and **parallelizable**, but "
    "means there is no conversation history to manage because "
    "*there is no conversation*.",
    title="4.3.1 Agentless is unique: no conversation state -- JSONL files on disk between stages",
)

claim_codex_dual_persistence = claim(
    "**Codex CLI dual persistence (Section 4.3.1).** Codex CLI "
    "stands out among the flat-list agents by adding **dual "
    "persistence**: an append-only JSONL rollout file for "
    "human-readable replay alongside a SQLite database for "
    "queryable state and session resumption. It is also the only "
    "flat-list agent that **supports undo (`Op::Undo`) and thread "
    "rollback (`Op::ThreadRollback`)**.",
    title="4.3.1 Codex CLI is unique: JSONL+SQLite dual persistence with undo/rollback",
)

claim_prometheus_graph_scoped = claim(
    "**Prometheus graph-scoped state is structurally unique "
    "(Section 4.3.1).** Rather than a single growing conversation, "
    "**each LLM node in the Prometheus graph maintains its own "
    "message list**. `ResetMessagesNode` clears specific message "
    "lists when the graph cycles back for retries, **preventing "
    "unbounded accumulation without any token-counting logic**. "
    "Tree-structured state stores per-node metadata that flat "
    "lists cannot represent, but the two tree-search agents use it "
    "differently: Moatless Tools maintains MCTS statistics and "
    "clones file-context snapshots; DARS-Agent stores expansion "
    "candidates and critic responses and recovers branch state by "
    "Docker reset and replay.",
    title="4.3.1 Prometheus is unique: graph-scoped state -- each node owns its message list",
)

# ---------------------------------------------------------------------------
# 4.3.2 Context compaction (Table 11) -- 7 distinct strategies
# ---------------------------------------------------------------------------

claim_table11_compaction = claim(
    "**Table 11 -- context compaction strategies (Section 4.3.2).** "
    "**Seven distinct strategies** from no management to "
    "LLM-initiated compaction.\n\n"
    "| Strategy | Agents | Mechanism |\n"
    "|---|---|---|\n"
    "| **None (crash on overflow)** | mini-swe-agent | Unbounded growth; agent crashes on `ContextWindowExceededError`. |\n"
    "| **Rule-based truncation** | SWE-agent, DARS-Agent | SWE-agent: 7 composable processors; keep first + last $N$ observations, elide rest. Polling parameter for prompt-cache preservation. DARS-Agent: adds `Last5Observations` in its fork. |\n"
    "| **Structural isolation** | Prometheus, AutoCodeRover | Prometheus: per-node message scoping + resets at retry boundaries. AutoCodeRover: round limits (15) + result truncation. |\n"
    "| **Token-based selective inclusion** | Moatless Tools | Greedy recent-first selection within token budget; per-observation summary fallback. |\n"
    "| **LLM summarization (scaffold-triggered)** | Aider, OpenHands, Gemini CLI, Codex CLI, OpenCode | Automatic at token threshold. Aider: recursive hierarchical summarization. Codex CLI: pre-turn and mid-turn modes. OpenCode: two-phase (prune old outputs, then LLM summarization). |\n"
    "| **LLM summarization + verification** | Gemini CLI | Summarize, then 'Probe' verification turn to check for information loss. |\n"
    "| **LLM-initiated compaction** | Cline | `condense` tool: LLM decides when to compact. Also supports scaffold-triggered compaction at token threshold. |\n",
    title="Table 11: 7 distinct context-compaction strategies -- the most diverged dimension",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 11"},
)

claim_compaction_seven_strategies = claim(
    "**Seven compaction strategies across 13 agents (Section "
    "4.3.2).** Context compaction exhibits **seven distinct "
    "strategies** across the corpus, the most divergent of any "
    "dimension. The corpus reveals **two distinct philosophies**: "
    "**'Prevention'** agents bound context growth structurally "
    "(Prometheus scopes per graph node + resets at retry "
    "boundaries; AutoCodeRover caps search rounds at 15 and shows "
    "at most 3 full results per query; Moatless Tools limits "
    "trajectory depth through tree structure). **'Cure'** agents "
    "let context grow and compress when needed (Aider, OpenHands, "
    "Gemini CLI, Codex CLI all trigger LLM-based summarization at "
    "token thresholds). The prevention approach avoids "
    "summarization cost and information loss but requires "
    "anticipating context growth patterns.",
    title="4.3.2 7 compaction strategies; 'prevention' (4 agents) vs 'cure' (5 agents) philosophies",
)

claim_compaction_required_observation = claim(
    "**Compaction is not optional for non-trivial agent tasks "
    "(Section 5.4).** **mini-swe-agent's only failure mode is "
    "context-window exhaustion**: it crashes when the context "
    "window is exceeded. The presence of compaction strategies in "
    "every agent that gives the LLM sustained autonomy beyond "
    "trivial task lengths -- and the crash behaviour of the only "
    "agent without one -- empirically **confirms compaction is "
    "not optional** for agents operating beyond trivial task "
    "lengths.",
    title="4.3.2 mini-swe-agent crashes on context overflow -- confirms compaction is required",
)

claim_swe_agent_polling_parameter = claim(
    "**SWE-agent's polling parameter (Section 4.3.2).** "
    "SWE-agent's `LastNObservations` processor includes a "
    "`polling` parameter that reveals a **subtle interaction "
    "between compaction and API cost**. Many LLM providers offer "
    "**prompt caching**: consecutive calls sharing the same "
    "message prefix skip reprocessing. Without polling, every new "
    "observation changes which messages are included, "
    "**invalidating the cache**. With polling, truncation changes "
    "occur at a rate of only $1/\\text{polling}$ per step, "
    "keeping the prefix stable across consecutive calls. This "
    "cost optimization operates at the intersection of two "
    "otherwise independent concerns and **has not been documented "
    "in prior analyses of SWE-agent**.",
    title="4.3.2 SWE-agent polling parameter: undocumented cache-vs-truncation interaction",
)

claim_gemini_probe_verification = claim(
    "**Gemini CLI's verification probe (Section 4.3.2).** "
    "**Gemini CLI is the only agent that validates its own "
    "context compaction.** After LLM summarization, it runs a "
    "'Probe' turn where the model checks whether critical "
    "information was lost. This self-correction mechanism "
    "addresses a known failure mode of LLM summarization (lossy "
    "compression of technical details) at the cost of an "
    "additional LLM call per compaction event.",
    title="4.3.2 Gemini CLI is unique: self-validating Probe turn after summarization",
)

claim_cline_llm_initiated = claim(
    "**Cline's LLM-initiated compaction (Section 4.3.2).** "
    "Cline's `condense` tool gives the LLM **agency over its own "
    "context management**. The LLM can proactively request "
    "summarization if it judges the context to be unwieldy. **No "
    "other agent in the corpus delegates the compaction decision "
    "to the LLM.** OpenHands provides a "
    "`CondensationRequestAction` that is conceptually similar, "
    "but compaction can also be triggered automatically when "
    "history exceeds condenser thresholds. OpenHands' condenser "
    "architecture is the most extensible in the corpus: nine "
    "pluggable implementations composable into pipelines via a "
    "registry pattern.",
    title="4.3.2 Cline is unique: LLM agency over compaction; OpenHands has 9 pluggable condensers",
)

claim_codex_pre_vs_mid_turn = claim(
    "**Codex CLI distinguishes pre-turn vs mid-turn compaction "
    "(Section 4.3.2).** Codex CLI distinguishes between **pre-turn** "
    "and **mid-turn** compaction: pre-turn compaction runs before "
    "each user turn and clears reference context so the next turn "
    "reinjects initial context cleanly; mid-turn compaction runs "
    "when the token limit is hit during tool execution and "
    "*injects initial context above the last user message*, "
    "matching the model's training expectations about where "
    "context appears. **This awareness of compaction timing "
    "relative to the conversation structure is unique in the "
    "corpus.**",
    title="4.3.2 Codex CLI is unique: pre-turn vs mid-turn compaction (training-distribution-aware)",
)

# ---------------------------------------------------------------------------
# 4.3.3 Multi-model routing (Table 12)
# ---------------------------------------------------------------------------

claim_table12_routing = claim(
    "**Table 12 -- multi-model routing strategies (Section 4.3.3).**\n\n"
    "| Strategy | Agents | Mechanism |\n"
    "|---|---|---|\n"
    "| **Single model** | mini-swe-agent, Agentless (per path) | One model throughout. |\n"
    "| **Router abstraction (default single)** | OpenHands | `RouterLLM` base with `MultimodalRouter`: routes by image presence and token limits. Default: single model via no-op router. |\n"
    "| **Role-based** | Aider, OpenCode | Main/weak/editor for different subtasks. Aider: weak model for summarization and commit messages; editor model for architect mode. OpenCode: per-agent overrides for build, plan, explore, compaction agents. |\n"
    "| **Plan/Act mode-based** | Cline | Independent model per mode (`api/index.ts:76--149`). LLM switches modes via tool calls. |\n"
    "| **Per-attempt cycling** | SWE-agent, AutoCodeRover | Different models for retry attempts. SWE-agent: round-robin through `agent_configs`. AutoCodeRover: round-robin through `model_names`. |\n"
    "| **Safety-focused (Guardian)** | Codex CLI | Separate `gpt-5.4` model evaluates tool-call risk (`guardian.rs`). |\n"
    "| **Task-based dual-model** | Prometheus | Advanced model for reasoning (analysis, editing, patch selection); base model for mechanical tasks (retrieval, verification). Hard-coded per graph node. |\n"
    "| **Actor-critic** | Moatless Tools | Value function (potentially different model) scores nodes (`value_function/base.py`). |\n"
    "| **Classifier chain** | Gemini CLI | 7-layer priority routing: fallback -> override -> approval mode -> Gemma classifier -> LLM classifier -> numerical classifier -> default (`modelRouterService.ts:39--67`). |\n",
    title="Table 12: 9 multi-model routing strategies; cost optimization is the dominant driver",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 12"},
)

claim_routing_dominant_driver = claim(
    "**Cost optimization is the dominant routing driver (Section "
    "4.3.3).** Across the **10 of 13 agents that route to "
    "multiple models**, the dominant motivation is **cost**: "
    "routing mechanical tasks to cheaper models while reserving "
    "expensive ones for reasoning. Aider's 'weak model' handles "
    "summarization and commit messages; in architect mode, a third "
    "'editor model' receives the plan and generates edits. "
    "OpenCode extends this role-based approach with per-sub-agent "
    "model overrides. Prometheus applies the same principle at a "
    "finer granularity: each LangGraph node is hard-coded to use "
    "either the 'advanced' or 'base' model. Reasoning-heavy nodes "
    "(analysis, editing, patch selection -- the last makes 10 "
    "majority-vote calls) use the advanced model; mechanical nodes "
    "(KG traversal, test execution) use the base model.",
    title="4.3.3 cost is the dominant routing driver across the 10 multi-model agents",
)

claim_gemini_classifier_chain = claim(
    "**Gemini CLI's 7-layer classifier chain is the most complex "
    "(Section 4.3.3).** Gemini CLI's **7-layer routing strategy** "
    "is the most complex routing mechanism observed. Each layer "
    "implements a different strategy; the first to produce a "
    "decision wins, so simple cases resolve cheaply while "
    "ambiguous ones fall through to more sophisticated "
    "classifiers. The most distinctive layer is the optional "
    "`GemmaClassifierStrategy`, which **runs a lightweight Gemma "
    "model locally for client-side routing decisions**, avoiding "
    "an API call just to select a model. **No other agent "
    "performs client-side model selection.**",
    title="4.3.3 Gemini CLI is unique: 7-layer chain incl. local Gemma client-side classifier",
)

claim_moatless_actor_critic = claim(
    "**Moatless Tools' actor-critic in tree search (Section "
    "4.3.3).** Moatless Tools' value function "
    "(`value_function/base.py`) assigns numeric rewards to search "
    "tree nodes. When configured to use a different model than the "
    "action agent, the result is an **actor-critic** "
    "architecture: one model generates actions while a separate "
    "model evaluates them. **No other agent uses separate models "
    "for generation and evaluation**; DARS-Agent's LLM critic "
    "performs a similar role but uses the same model for both, "
    "**meaning the critic shares the generator's biases**.",
    title="4.3.3 Moatless Tools is unique: actor-critic with separate generator and value-function models",
)

claim_codex_most_models = claim(
    "**Codex CLI uses the most models in the corpus (Section "
    "4.3.3).** **Codex CLI uses the most models of any agent**: "
    "the primary model for code generation, a **Guardian model** "
    "(`gpt-5.4`) for safety evaluation, and **two dedicated models "
    "for its memory-extraction pipeline** "
    "(`gpt-5.1-codex-mini` for per-rollout extraction, "
    "`gpt-5.3-codex` for consolidation; Section 4.3.4). The "
    "Guardian is **the only instance in the corpus of multi-model "
    "routing for safety rather than cost or capability reasons**.",
    title="4.3.3 Codex CLI uses the most models: 4 distinct (primary + Guardian + 2 memory-extraction)",
)

# ---------------------------------------------------------------------------
# 4.3.4 Persistent memory (Table 13)
# ---------------------------------------------------------------------------

claim_table13_memory = claim(
    "**Table 13 -- persistent memory strategies (Section 4.3.4).**\n\n"
    "| Strategy | Agents | Mechanism |\n"
    "|---|---|---|\n"
    "| **None** | SWE-agent, OpenHands, AutoCodeRover, mini-swe-agent, DARS-Agent | No cross-session persistence. Trajectory files are output artefacts, not consumed by future runs. |\n"
    "| **Pipeline resumability** | Agentless | No cross-task learning, but JSONL outputs enable pipeline resumability (`--skip_existing`), embedding indices persist via `--persist_dir`, repo structures cached via `PROJECT_FILE_LOC`. |\n"
    "| **Config file loading** | Aider (`.aider.conf.yml`) | Static, user-written configuration. Tags cache (`repomap.py:43, 217--265`) persists AST analysis as a performance optimization. |\n"
    "| **LLM-writable rules/memory** | Cline (`.clinerules/`), Gemini CLI (`GEMINI.md`) | The LLM actively writes persistent instructions. Cline: `new_rule` tool. Gemini CLI: `save_memory` tool appends under 'Gemini Added Memories' in `GEMINI.md` (supports `@path/to/file` references). |\n"
    "| **Full session persistence** | OpenCode | SQLite-backed session history with resume capability. All messages, tool outputs, token usage, and costs persist (`session/session.sql.ts:14--76`). |\n"
    "| **Background extraction pipeline** | Codex CLI | Two-phase: Phase 1 extracts memories from recent rollouts (parallel, `gpt-5.1-codex-mini`); Phase 2 consolidates via sub-agent (`gpt-5.3-codex`). Usage-ranked, stale memories pruned. |\n"
    "| **Multi-tier persistence** | Prometheus | Athena (semantic memory service, HTTP API) + Neo4j (KG, 20-language ASTs) + PostgreSQL (LangGraph checkpoints). Memory-first retrieval with KG fallback. |\n",
    title="Table 13: 7 persistent-memory variants -- benchmark vs CLI divide",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 13"},
)

claim_memory_benchmark_vs_cli_divide = claim(
    "**Persistent memory: benchmark vs CLI divide (Section "
    "4.3.4).** A clear division exists between agents designed "
    "for benchmark evaluation and those designed for interactive "
    "use. **All five agents with no persistent memory** "
    "(SWE-agent, OpenHands, AutoCodeRover, mini-swe-agent, "
    "DARS-Agent) treat each task as independent. For benchmark-"
    "only agents this is expected; for OpenHands -- **also widely "
    "used for interactive development (53k stars, second-most in "
    "the corpus)** -- the absence is notable, though its "
    "microagent system loads static project instructions that "
    "partially fill this role. The five CLI agents with "
    "persistent memory (Aider, Cline, Gemini CLI, Codex CLI, "
    "OpenCode) target interactive development where remembering "
    "project conventions has direct value. **Prometheus is an "
    "outlier**: despite being a SWE-bench agent, it implements "
    "multi-tier persistence (Neo4j + PostgreSQL + Athena) more "
    "characteristic of an interactive tool.",
    title="4.3.4 benchmark vs CLI divide on memory; Prometheus is the cross-over outlier",
)

claim_llm_as_memory_author = claim(
    "**LLM as memory author (Section 4.3.4).** Cline and Gemini "
    "CLI share a pattern where **the LLM writes its own "
    "persistent instructions**. Cline's `new_rule` tool creates "
    "`.clinerules` files; Gemini CLI's `save_memory` tool appends "
    "to `GEMINI.md`, which additionally supports `@path/to/file` "
    "references for composing instructions across multiple files. "
    "These memories persist in the project repository and are "
    "loaded into future sessions' system prompts. **Codex CLI "
    "takes a different approach**: a background pipeline extracts "
    "and consolidates memories *without the LLM explicitly "
    "deciding what to remember*.",
    title="4.3.4 LLM-author memory (Cline/Gemini) vs background-extraction (Codex CLI) -- two paradigms",
)

claim_cline_cross_tool_compat = claim(
    "**Cline's cross-tool compatibility (Section 4.3.4).** Cline "
    "reads not only its own `.clinerules/` but also "
    "`.cursorrules`, `.windsurfrules`, and `AGENTS.md`. **This "
    "pragmatic interoperability reflects an emerging ecosystem** "
    "where developers use multiple AI coding tools with shared "
    "project-level instructions [@Galster2026].",
    title="4.3.4 Cline reads cross-tool memory files (Cursor, Windsurf, AGENTS.md)",
)

# ---------------------------------------------------------------------------
# 4.4 Cross-cutting themes
# ---------------------------------------------------------------------------

claim_sampling_vs_iteration = claim(
    "**Cross-cutting theme: sampling vs iteration (Section "
    "4.4.1).** When an LLM-generated patch fails, there are two "
    "fundamentally different ways to try again: generate another "
    "**independent** attempt (sampling), or **refine** the failed "
    "attempt using feedback (iteration). This distinction cuts "
    "across the control loop taxonomy because it describes how "
    "agents handle the *population* of solution attempts.\n\n"
    "* **Pure sampling: Agentless.** Generates multiple patches "
    "independently and selects by majority voting. No patch "
    "benefits from knowing another failed.\n"
    "* **Pure iteration: 6 of 9 LLM-driven agents** (OpenHands, "
    "Codex CLI, Gemini CLI, Cline, mini-swe-agent, OpenCode). A "
    "single attempt is refined through a feedback loop where each "
    "step sees the results of previous steps.\n"
    "* **Decision-layer voting: Prometheus** -- calls the "
    "advanced model 10 times on the same prompt to vote among "
    "*already-generated* candidate patches.\n"
    "* **Hybrid: SWE-agent's RetryAgent** -- multiple complete "
    "attempts (sampling), each a depth-first feedback loop "
    "(iteration), reviewer model selects the best.",
    title="4.4.1 sampling vs iteration cuts across loop taxonomy: 1 sampling / 6 iteration / hybrid",
)

claim_subagent_delegation = claim(
    "**Cross-cutting theme: sub-agent delegation (Section "
    "4.4.2).** **Five agents support sub-agent spawning** through "
    "fundamentally different mechanisms, revealing different "
    "assumptions about who controls the delegation decision:\n\n"
    "* **Codex CLI:** LLM has full control via `spawn_agent`, "
    "`send_input`, `resume_agent`, `wait`, `close_agent` tools. "
    "Depth limited by `agent_max_depth`.\n"
    "* **OpenCode:** role-based -- `task` tool spawns "
    "specialized sub-agents (build, plan, explore, general) with "
    "scaffold-enforced tool permissions.\n"
    "* **OpenHands:** integrated into event-sourced architecture; "
    "parent `AgentController` creates child via "
    "`AgentDelegateAction`; events flow through the same stream.\n"
    "* **Cline:** simpler tool-based delegation via `new_task` "
    "and `use_subagents`.\n"
    "* **Gemini CLI:** `LocalAgentExecutor` runs a separate "
    "ReAct loop with its own turn limits and deadline timer; "
    "**uniquely** includes a recovery phase giving the sub-agent "
    "one final turn when the deadline expires.\n\n"
    "**A sixth, Prometheus**, achieves *implicit* delegation "
    "through subgraph nesting rather than explicit spawning. The "
    "diversity and absence of a dominant pattern suggests "
    "delegation is an active design frontier.",
    title="4.4.2 5 (or 6) agents delegate via 5 different mechanisms -- active design frontier",
)

claim_online_vs_offline_selection = claim(
    "**Cross-cutting theme: online vs offline selection (Section "
    "4.4.3).** Tree-search agents face two distinct selection "
    "problems: which branch to explore *during* the search "
    "(online), and which completed solution to return *after* the "
    "search finishes (offline).\n\n"
    "* **DARS-Agent separates them cleanly.** Online: an LLM "
    "critic at each branch point. Offline: a *separately trained "
    "reviewer* evaluates finished patches. Online critic must be "
    "fast (runs at every branch); offline reviewer can be more "
    "thorough (runs once).\n"
    "* **Moatless Tools also separates them.** Online: value "
    "function during MCTS. Offline: a discriminator. Both can use "
    "the same model, allowing consistent evaluation criteria.\n"
    "* **Final-answer extraction differs.** DARS-Agent always "
    "takes `children[0]` (leftmost-path), relying entirely on the "
    "online critic. Moatless Tools' discriminator actively "
    "**re-evaluates all completed trajectories**, potentially "
    "picking one that was not the most-visited during search.",
    title="4.4.3 tree-search agents separate online (branch selection) and offline (final answer) selection",
)

claim_dars_swe_fork_vs_mini_protocol = claim(
    "**Cross-cutting theme: ecosystem maturity (Section 4.4.4).** "
    "The relationship between DARS-Agent and SWE-agent illustrates "
    "the current state of ecosystem maturity. **DARS-Agent copied "
    "and modified the entire SWE-agent codebase rather than "
    "extending it**: `agents.py` is a 700-line copy of the "
    "original SWE-agent `Agent` class, and `dars_agent.py` is a "
    "parallel 1382-line reimplementation with tree-search logic "
    "added. Bug fixes and improvements in either project do not "
    "propagate. **mini-swe-agent takes the opposite approach**, "
    "reusing SWE-agent's execution environments (SWE-ReX Docker "
    "and Modal backends) while defining its own abstractions. It "
    "specifies agent, model, and environment as **Python "
    "Protocols** [@Levkivskyi2017PEP544] -- structural typing "
    "where any object with the right methods conforms. **Both "
    "fork-based and dependency-based reuse coexist for the same "
    "upstream project**, indicating clean extension points have "
    "not yet emerged.",
    title="4.4.4 DARS forks SWE-agent (1382 LoC); mini-swe-agent uses Protocols -- coexistence of reuse styles",
)

claim_ide_as_architecture = claim(
    "**Cross-cutting theme: IDE as architecture (Section 4.4.5).** "
    "**Cline is the only agent in the corpus that runs as an IDE "
    "extension** rather than a standalone CLI or server "
    "[@Cline]. This architectural choice gives it access to a "
    "category of context CLI agents cannot obtain: **the IDE's own "
    "understanding of the project**. The `@problems` mention pulls "
    "from VS Code's diagnostic API; `@terminal` accesses "
    "integrated terminal output; commands execute in visible "
    "terminal panels via the VS Code terminal API; "
    "`FileContextTracker` monitors which files the model has "
    "seen, read, or modified across turns, **detecting external "
    "modifications to prevent stale context during diff editing**. "
    "The tradeoff is **platform lock-in**: these capabilities "
    "depend on VS Code's extension API, and the richest context "
    "sources cannot run outside VS Code.",
    title="4.4.5 Cline is unique: IDE-extension architecture trades portability for richer context",
)

__all__ = [
    "claim_table10_state_management",
    "claim_state_management_extremes",
    "claim_agentless_no_state",
    "claim_codex_dual_persistence",
    "claim_prometheus_graph_scoped",
    "claim_table11_compaction",
    "claim_compaction_seven_strategies",
    "claim_compaction_required_observation",
    "claim_swe_agent_polling_parameter",
    "claim_gemini_probe_verification",
    "claim_cline_llm_initiated",
    "claim_codex_pre_vs_mid_turn",
    "claim_table12_routing",
    "claim_routing_dominant_driver",
    "claim_gemini_classifier_chain",
    "claim_moatless_actor_critic",
    "claim_codex_most_models",
    "claim_table13_memory",
    "claim_memory_benchmark_vs_cli_divide",
    "claim_llm_as_memory_author",
    "claim_cline_cross_tool_compat",
    "claim_sampling_vs_iteration",
    "claim_subagent_delegation",
    "claim_online_vs_offline_selection",
    "claim_dars_swe_fork_vs_mini_protocol",
    "claim_ide_as_architecture",
]
