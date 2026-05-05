"""Section 4.2 (Layer 2): Tool and environment interface.

Section 4.2 of Rombaut 2026 [@Rombaut2026]. Five dimensions
characterize the interface layer: (4.2.1) tool set design, (4.2.2)
edit and patch format, (4.2.3) tool discovery, (4.2.4) context
retrieval, (4.2.5) execution isolation. The headline finding is
*convergence on capability categories despite divergence in tool count
and interface*.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 4.2.1 Tool set design (Table 5)
# ---------------------------------------------------------------------------

claim_table5_tool_sets = claim(
    "**Table 5 -- tool set size and capability coverage (Section "
    "4.2.1).** Tool count reflects LLM-callable tools; user-facing "
    "commands (e.g. Aider's ~38 slash commands) are excluded.\n\n"
    "| Agent | Tools | Read | Search | Edit | Execute | Validate | Notes |\n"
    "|---|---:|:-:|:-:|:-:|:-:|:-:|---|\n"
    "| Aider | 0 | -- | -- | * | * | -- | Text-parsed edits, 13 formats |\n"
    "| Agentless | 0-1 | -- | -- | * | * | -- | 1 simulated tool in Anthropic path |\n"
    "| AutoCodeRover | 8 | yes | yes | -- | -- | -- | All search/read; no edit tools |\n"
    "| OpenHands | 9+ | yes | -- | yes | yes | -- | +MCP; search via bash |\n"
    "| Moatless Tools | 15-37 | yes | yes | yes | yes | yes | 37 classes; ~15 typical/session |\n"
    "| SWE-agent | 3-35 | yes | yes | yes | yes | -- | 3 default; 35 across 15 bundles |\n"
    "| DARS-Agent | ~15 | yes | yes | yes | yes | -- | Inherited from SWE-agent fork |\n"
    "| Codex CLI | ~20+ | yes | yes | yes | yes | -- | +MCP; +sub-agent spawning |\n"
    "| Gemini CLI | 17+ | yes | yes | yes | yes | -- | +MCP; +tool discovery subprocess |\n"
    "| Prometheus | 17 | yes | yes | yes | yes | -- | 1-12 bound per graph node |\n"
    "| OpenCode | 18+ | yes | yes | yes | yes | -- | +MCP; +plugins; +custom tools |\n"
    "| Cline | 27+ | yes | yes | yes | yes | -- | +MCP; largest flat built-in set |\n"
    "| mini-swe-agent | 1 | yes | -- | -- | -- | -- | All capabilities via bash |\n",
    title="Table 5: tool counts 0-37 across 13 agents; capability categories converge",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 5"},
)

claim_capability_categories_converge = claim(
    "**Capability categories converge on read/search/edit/execute "
    "(Section 4.2.1).** Tool counts range from **0 (Aider) to 37 "
    "action classes (Moatless Tools)**, but raw counts obscure a "
    "convergence in capability categories. **The same four core "
    "capability categories -- read, search, edit, execute -- "
    "appear across all LLM-driven agents**. A fifth category, "
    "*validate* (dedicated test-running or linting tools), appears "
    "only in Moatless Tools; other agents subsume validation under "
    "execute. Agents with fewer tools achieve coverage through "
    "composition: mini-swe-agent's single `bash` tool covers all "
    "four categories by delegating to shell commands. Agents with "
    "more tools decompose these categories into finer-grained "
    "operations (Moatless Tools has separate `FindClass`, "
    "`FindFunction`, `FindCodeSnippet`, `SemanticSearch`, "
    "`GrepTool`, `GlobTool` for the search category alone).",
    title="4.2.1 capability categories converge: 4 core (read/search/edit/execute) in all LLM-driven agents",
)

claim_openhands_browsergym = claim(
    "**OpenHands' BrowserGym (Section 4.2.1).** OpenHands stands "
    "out for including a **BrowserGym-based headless browser** "
    "[@LeSellier2024BrowserGym] as a first-class tool -- the only "
    "agent in the corpus with a built-in web browsing tool for "
    "navigating and interacting with web pages. It also provides a "
    "`think` tool for logging reasoning without side effects and a "
    "`request_condensation` tool letting the LLM request context "
    "compaction (Section 4.3.2).",
    title="4.2.1 OpenHands is unique: built-in BrowserGym headless browser",
)

claim_codex_meta_tools = claim(
    "**Codex CLI meta-tools and request_permissions (Section "
    "4.2.1).** Codex CLI (~20+ tools) is notable for including "
    "**meta-tools that let the LLM discover additional tools at "
    "runtime**: `tool_search` queries registered app tools, and "
    "`tool_suggest` recommends tools for the current task. It also "
    "exposes a `request_permissions` tool that lets the LLM ask "
    "for elevated sandbox access mid-session, **making the agent's "
    "own permissions a negotiable resource rather than a fixed "
    "constraint**. No other agent in the corpus exposes "
    "permissions as an LLM-controllable variable.",
    title="4.2.1 Codex CLI is unique: meta-tools + LLM-negotiable permissions",
)

claim_prometheus_per_node_scoping = claim(
    "**Prometheus per-node tool scoping (Section 4.2.1).** "
    "**Prometheus is the only agent that binds different tool "
    "subsets to different decision points.** Its `EditNode` sees 5 "
    "tools (file operations); its `BugReproducingWriteNode` sees "
    "only `read_file`; its `BugFixVerifyNode` sees only "
    "`run_command`. This **structural guardrailing** constrains "
    "the action space at each step. AutoCodeRover achieves a "
    "similar effect through phase separation -- the patch agent is "
    "not given search tools and is instead prompted to produce "
    "patches directly from context gathered during the search "
    "phase -- but this is a workflow-level constraint rather than "
    "a configurable binding.",
    title="4.2.1 Prometheus is unique: per-node tool scoping (5/1/1 tools per decision point)",
)

claim_autocoderover_proxy_agent = claim(
    "**AutoCodeRover proxy agent (Section 4.2.1).** AutoCodeRover "
    "uses a *secondary LLM call* (`agent_proxy.py:81--82`) to "
    "convert the search agent's natural-language tool selections "
    "into structured JSON. The search agent 'thinks out loud' "
    "about which tools to call; the proxy agent extracts the "
    "structured invocation with up to 5 retries. This adds one LLM "
    "call per search round (with 15 rounds possible, up to 15 "
    "extra calls). **No other agent uses a secondary LLM call for "
    "tool call parsing**; all others rely on function-calling "
    "APIs, regex parsing, or XML extraction.",
    title="4.2.1 AutoCodeRover is unique: proxy LLM converts NL to structured tool calls",
)

# ---------------------------------------------------------------------------
# 4.2.2 Edit and patch format (Table 6) -- convergence on str_replace
# ---------------------------------------------------------------------------

claim_table6_edit_format = claim(
    "**Table 6 -- edit/patch format variants (Section 4.2.2).**\n\n"
    "| Format | Agents |\n"
    "|---|---|\n"
    "| **String replacement (function calling)** | OpenHands and SWE-agent (`str_replace_editor`), Codex CLI (`apply_patch`), OpenCode (`edit`) |\n"
    "| **Write tool (function calling)** | Gemini CLI, Cline |\n"
    "| **Text-parsed edit blocks** | Aider (13 formats), DARS-Agent |\n"
    "| **Simulated tool use** | Agentless (Anthropic path) |\n"
    "| **Pydantic-schema actions** | Moatless Tools, Prometheus |\n",
    title="Table 6: 5 edit-format variants; string-replacement is the convergence point",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 6"},
)

claim_str_replace_convergence = claim(
    "**Convergence on `str_replace_editor` (Section 4.2.2).** The "
    "`str_replace_editor` tool, which takes `old_str` and `new_str` "
    "arguments for exact string replacement, appears in **5 of 13 "
    "agents** (OpenHands, SWE-agent, Codex CLI's `apply_patch` in "
    "freeform mode, Agentless as one of three repair output "
    "formats, and Moatless Tools as `StringReplace`). This "
    "convergence is notable because these agents were **developed "
    "independently**; the shared interface reflects a common "
    "discovery that **exact string matching is more reliable than "
    "line-number-based or unified-diff-based editing for "
    "LLM-generated patches** [@SWEAgent].",
    title="4.2.2 str_replace_editor convergence (5/13 agents) -- independent discovery",
)

claim_aider_thirteen_edit_formats = claim(
    "**Aider's 13 model-specific edit formats (Section 4.2.2).** "
    "Aider is an outlier with **13 registered edit formats**, each "
    "implemented as a separate coder subclass. The format is "
    "selected based on model capabilities: some models handle "
    "unified diffs better, others work better with SEARCH/REPLACE "
    "blocks. **This treatment of edit format as a first-class, "
    "model-specific architectural component is unique in the "
    "corpus**, though OpenCode implements a simpler version (its "
    "tool registry selects between `edit` and `apply_patch` based "
    "on model capabilities, offering 2 formats vs Aider's 13).",
    title="4.2.2 Aider is unique: 13 model-specific edit formats as first-class components",
)

claim_swe_agent_ten_parsers = claim(
    "**SWE-agent supports 10 output parsers (Section 4.2.2).** On "
    "the parsing side, **SWE-agent supports 10 different output "
    "parsers** (`FunctionCallingParser`, `ThoughtActionParser`, "
    "`XMLThoughtActionParser`, ...), enabling the same tool set to "
    "work across models with different output conventions. Together "
    "with Aider's 13 model-specific edit formats, this represents "
    "the highest degree of model-agnosticism in output interfacing "
    "observed in the corpus -- though the two approaches address "
    "different layers (SWE-agent adapts *tool parsing*, Aider "
    "adapts the *edit format* itself).",
    title="4.2.2 SWE-agent: 10 parsers; Aider: 13 edit formats -- model-agnostic by different mechanisms",
)

claim_agentless_simulated_tool_use = claim(
    "**Agentless's simulated tool use (Section 4.2.2).** "
    "Agentless's 'simulated tool use' in its Anthropic path is "
    "**architecturally unique**. When using Anthropic's API, the "
    "LLM calls a `str_replace_editor` tool, but every call "
    "receives the same hardcoded response: 'File is successfully "
    "edited' regardless of input. The LLM never sees actual file "
    "state after its edits; the tool calls are **extracted and "
    "applied post-hoc**. This uses the tool-calling API as a "
    "*structured output extraction technique* rather than for "
    "actual execution.",
    title="4.2.2 Agentless is unique: tool calls as structured-output trick, not real execution",
)

# ---------------------------------------------------------------------------
# 4.2.3 Tool discovery (Table 7)
# ---------------------------------------------------------------------------

claim_table7_tool_discovery = claim(
    "**Table 7 -- tool discovery strategies (Section 4.2.3).**\n\n"
    "| Strategy | Agents |\n"
    "|---|---|\n"
    "| **Static (all at init)** | Aider, Agentless, AutoCodeRover, mini-swe-agent, DARS-Agent, Moatless Tools |\n"
    "| **Per-phase scoping (static per node)** | Prometheus, AutoCodeRover |\n"
    "| **Config-conditional** | SWE-agent, OpenHands |\n"
    "| **Per-turn dynamic rebuild** | Codex CLI (`built_tools()` called every sampling request, `codex.rs:6156--6164`) |\n"
    "| **Dynamic (MCP + subprocess)** | Gemini CLI (`tool_discovery_subprocess`, `tool-registry.ts:312--439`), Cline (MCP servers connected/disconnected at runtime), OpenCode (static core + dynamic custom tools from config dirs, plugin system, MCP integration) |\n",
    title="Table 7: 5 tool-discovery strategies; 6/13 fully static",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 7"},
)

claim_codex_per_turn_rebuild = claim(
    "**Codex CLI's per-turn tool rebuild is distinctive (Section "
    "4.2.3).** While most agents construct the tool set once (or "
    "once per phase), **Codex CLI calls `built_tools()` for every "
    "LLM sampling request**, incorporating any MCP server changes, "
    "newly enabled connectors, or dynamic tools added during the "
    "session. **The tool set is, in principle, different at every "
    "LLM call.** Gemini CLI's `toolDiscoveryCommand` feature takes "
    "a different approach: an external subprocess outputs "
    "`FunctionDeclaration[]` as JSON, allowing arbitrary tool "
    "sources without modifying the agent code.",
    title="4.2.3 Codex CLI is unique: per-turn tool rebuild (potentially different tools every LLM call)",
)

# ---------------------------------------------------------------------------
# 4.2.4 Context retrieval paradigm (Table 8) -- 7 strategy types
# ---------------------------------------------------------------------------

claim_table8_retrieval = claim(
    "**Table 8 -- context retrieval strategies (Section 4.2.4).** "
    "Agents may use multiple strategies. **Seven distinct strategy "
    "types** observed across the corpus.\n\n"
    "| Strategy | Agents | Mechanism |\n"
    "|---|---|---|\n"
    "| **Keyword/regex search** | SWE-agent, OpenHands, Codex CLI, Gemini CLI, Cline, mini-swe-agent, DARS-Agent, OpenCode | LLM invokes `grep`, `find`, `ripgrep` as tools. |\n"
    "| **Repo map (static analysis)** | Aider | PageRank-weighted tree-sitter [@Brunsfeld2018TreeSitter] tag index. NetworkX dependency graph; identifiers in conversation get 10x boost; chat files 50x boost (`repomap.py:365--574`). |\n"
    "| **AST-aware search** | AutoCodeRover, Moatless Tools, DARS-Agent, Prometheus | `search_class`, `search_method`: structure-aware queries over pre-built AST indices. AutoCodeRover's AST tools are Python-only; Prometheus's tree-sitter-based tools cover 20 languages. |\n"
    "| **Knowledge graph traversal** | Prometheus | Neo4j graph built from tree-sitter ASTs covering 20 languages. 11 tools (10 graph traversal + `read_file`) query `FileNode`, `ASTNode`, `TextNode` entities (`graph_traversal.py:93--586`). |\n"
    "| **Embedding-based semantic search** | Moatless Tools | FAISS [@Johnson2021FAISS] vector store via LlamaIndex (`code_index.py:57`). The only agent with embedding-based retrieval as an LLM-callable tool. |\n"
    "| **Hierarchical localization** | Agentless | File -> class/function -> line-level narrowing across pipeline stages. Each level sees only what the previous identified (`FL.py:313--681`). |\n"
    "| **Classical fault localization** | AutoCodeRover | SBFL [@Wong2016SBFL] with Ochiai scoring [@Abreu2007Ochiai] (`analysis/sbfl.py`). Unique in corpus. |\n",
    title="Table 8: 7 distinct context-retrieval strategies",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 8"},
)

claim_two_retrieval_paradigms = claim(
    "**Two retrieval paradigms (Section 4.2.4).** The 13 agents "
    "divide into two paradigms reflecting fundamentally different "
    "assumptions about *where code understanding should live*. The "
    "**first paradigm** (8 agents: SWE-agent, OpenHands, Codex CLI, "
    "Gemini CLI, Cline, mini-swe-agent, DARS-Agent, OpenCode) "
    "treats the LLM as a navigator: the agent provides "
    "general-purpose shell tools (`grep`, `find`, `ripgrep`) and "
    "relies on the LLM to formulate queries, interpret results, "
    "and decide where to look next. The scaffold provides no code "
    "understanding of its own. The **second paradigm** invests in "
    "scaffold-side code understanding: Aider builds a PageRank "
    "[@BrinPage1998] dependency graph; AutoCodeRover and Moatless "
    "Tools parse source into ASTs; Prometheus constructs a Neo4j "
    "knowledge graph covering 20 languages.",
    title="4.2.4 LLM-as-navigator (8 agents) vs scaffold-builds-understanding (5 agents)",
)

claim_retrieval_correlates_with_loop_driver = claim(
    "**Retrieval paradigm correlates with loop driver (Section "
    "4.2.4).** The paradigm choice **correlates with loop driver** "
    "(Section 4.1.2): scaffold-driven agents tend to invest in "
    "retrieval infrastructure, while LLM-driven agents tend to "
    "trust the LLM to navigate with general-purpose tools. The "
    "correlation is unsurprising: if the scaffold controls "
    "sequencing it has the opportunity (and need) to pre-process "
    "the repository; if the LLM controls exploration it can issue "
    "search commands on demand. This correlation is the canonical "
    "example of dimension non-independence (Section 6.2 internal "
    "validity).",
    title="4.2.4 retrieval paradigm and loop driver are correlated -- not independent dimensions",
)

claim_aider_pagerank_repomap = claim(
    "**Aider's PageRank repo map (Section 4.2.4).** Aider's "
    "retrieval mechanism applies **Google's PageRank algorithm** "
    "[@BrinPage1998] to source code structure. Tree-sitter "
    "[@Brunsfeld2018TreeSitter] parses every file to extract symbol "
    "definitions and cross-file references, forming a directed "
    "dependency graph (`repomap.py:365--574`). PageRank scores rank "
    "files by structural centrality, with context-aware boosts: "
    "**identifiers mentioned in conversation receive a 10x weight, "
    "files added to the chat receive 50x**, and a binary search "
    "fills the token budget in rank order. **No other agent in the "
    "corpus uses graph-theoretic relevance ranking.**",
    title="4.2.4 Aider is unique: PageRank-weighted repo map for graph-theoretic retrieval",
)

claim_autocoderover_sbfl = claim(
    "**AutoCodeRover's SBFL (Section 4.2.4).** AutoCodeRover is "
    "the only agent that incorporates **classical fault "
    "localization** [@Wong2016SBFL]. When failing tests are "
    "available, it runs spectrum-based fault localization (SBFL) "
    "with Ochiai suspiciousness scores [@Abreu2007Ochiai]: methods "
    "executed frequently by failing tests and rarely by passing "
    "tests rank highest (`analysis/sbfl.py`). The top 5 suspicious "
    "methods are presented to the LLM as advisory input. **This "
    "bridges two otherwise disconnected communities** (automated "
    "fault localization and LLM-based repair); no other agent in "
    "the corpus uses test-execution-based localization.",
    title="4.2.4 AutoCodeRover is unique: SBFL bridges fault-localization and LLM-repair",
)

# ---------------------------------------------------------------------------
# 4.2.5 Execution isolation (Table 9)
# ---------------------------------------------------------------------------

claim_table9_isolation = claim(
    "**Table 9 -- execution isolation strategies (Section 4.2.5).**\n\n"
    "| Isolation level | Agents |\n"
    "|---|---|\n"
    "| **None (local shell)** | Gemini CLI, Aider, OpenCode |\n"
    "| **Stateless subshells** | mini-swe-agent (`subprocess.run()`, `local.py:28--39`) |\n"
    "| **Platform sandboxing** | Codex CLI (Bubblewrap+Landlock [@Salaun2017Landlock] on Linux, Seatbelt on macOS) |\n"
    "| **Docker container** | SWE-agent, OpenHands, DARS-Agent, AutoCodeRover, Prometheus |\n"
    "| **Shadow git checkpoints** | Cline (isolated git repo tracks state per tool execution, `CheckpointTracker.ts`) |\n"
    "| **Shadow mode (in-memory)** | Moatless Tools (`shadow_mode` flag, `agent.py:57`) |\n"
    "| **Not applicable** | Agentless: LLM never executes arbitrary commands; Docker used only for test execution via SWE-bench harness |\n",
    title="Table 9: 7 isolation levels; Docker dominates SWE-bench agents (5/13 total)",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 9"},
)

claim_docker_converges_for_swebench = claim(
    "**Docker convergence for SWE-bench agents (Section 4.2.5).** "
    "Five Docker-based agents (SWE-agent, OpenHands, DARS-Agent, "
    "AutoCodeRover, Prometheus) -- all benchmark agents -- rely on "
    "**container boundaries as their primary safety mechanism**. "
    "OpenHands' Docker implementation is architecturally "
    "distinctive: a FastAPI action server runs *inside* the "
    "container, and the host-side agent controller communicates "
    "with it via HTTP. This creates a clean API boundary unlike "
    "other Docker agents that exec commands directly into "
    "containers.",
    title="4.2.5 5/13 SWE-bench agents converge on Docker; OpenHands uses HTTP-action-server design",
)

claim_safety_diverges_for_cli = claim(
    "**Safety approaches diverge for CLI agents (Section 4.2.5).** "
    "Agents without container isolation pursue *strikingly "
    "different* safety strategies, suggesting the ecosystem has "
    "**not converged on an isolation standard for interactive "
    "agents**:\n\n"
    "* **Gemini CLI** uses a rule-based policy engine assigning "
    "per-tool approval requirements.\n"
    "* **Codex CLI** combines OS-level platform sandboxing "
    "(Bubblewrap+Landlock on Linux, Seatbelt on macOS) with a "
    "**Guardian safety subagent** (a separate LLM, `gpt-5.4`) "
    "evaluating each tool call's risk on a 0-100 scale, blocking "
    "above 80 (`guardian.rs`). **The only agent using an LLM to "
    "evaluate the safety of another LLM's actions.**\n"
    "* **Aider** relies on the user being present and "
    "supervising; the human is the safety boundary.\n"
    "* **Cline** provides per-tool / per-scope approval "
    "settings, with a `CommandPermissionController` blocking "
    "dangerous shell operators. Settings range from full "
    "autonomous ('YOLO') to per-command-pattern approval.\n"
    "* **OpenCode** uses a policy-based permission system with "
    "three options (Allow Once, Always Allow, Reject); no OS-level "
    "sandboxing.\n"
    "* **mini-swe-agent** uses stateless subshells for "
    "process-level isolation without containerization.",
    title="4.2.5 CLI safety diverges: from human-in-the-loop to LLM-evaluating-LLM (Codex Guardian)",
)

claim_cline_shadow_git = claim(
    "**Cline's shadow git checkpoints (Section 4.2.5).** Cline's "
    "`CheckpointTracker` creates an **isolated git repository per "
    "workspace** that records file system state after each tool "
    "execution. This enables diff-based rollback **without "
    "touching the user's real git history**, and without requiring "
    "Docker. It handles nested git repos by temporarily disabling "
    "them and validates against sensitive directories. A middle "
    "ground between no isolation and containerization, specific to "
    "the IDE context where Cline operates.",
    title="4.2.5 Cline is unique: shadow git checkpoints for IDE-friendly rollback",
)

claim_moatless_shadow_mode = claim(
    "**Moatless Tools' shadow mode (Section 4.2.5).** For tree-"
    "search agents, execution isolation interacts directly with "
    "search cost. **Moatless Tools avoids replay entirely**: its "
    "shadow mode tracks file modifications in a `FileContext` "
    "object **without writing to disk**, and each node clones its "
    "parent's file context. This enables branching at any step "
    "without environment cost. **DARS-Agent's environment reset** "
    "performs a full Docker reset and replays all actions from "
    "root to the branch point -- at depth $N$ this requires "
    "re-executing $N$ commands, addressed by limiting branching to "
    "specific action types via `action_expansion_limit` "
    "(`default_dars.yaml:179--184`).",
    title="4.2.5 Moatless shadow mode (in-memory) vs DARS-Agent Docker-replay -- branching-cost tradeoff",
)

__all__ = [
    "claim_table5_tool_sets",
    "claim_capability_categories_converge",
    "claim_openhands_browsergym",
    "claim_codex_meta_tools",
    "claim_prometheus_per_node_scoping",
    "claim_autocoderover_proxy_agent",
    "claim_table6_edit_format",
    "claim_str_replace_convergence",
    "claim_aider_thirteen_edit_formats",
    "claim_swe_agent_ten_parsers",
    "claim_agentless_simulated_tool_use",
    "claim_table7_tool_discovery",
    "claim_codex_per_turn_rebuild",
    "claim_table8_retrieval",
    "claim_two_retrieval_paradigms",
    "claim_retrieval_correlates_with_loop_driver",
    "claim_aider_pagerank_repomap",
    "claim_autocoderover_sbfl",
    "claim_table9_isolation",
    "claim_docker_converges_for_swebench",
    "claim_safety_diverges_for_cli",
    "claim_cline_shadow_git",
    "claim_moatless_shadow_mode",
]
