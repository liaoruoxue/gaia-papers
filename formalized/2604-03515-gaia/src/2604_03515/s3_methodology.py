"""Section 3: Methodology.

Section 3 of Rombaut 2026 [@Rombaut2026]. Specifies the corpus
construction, the analysis dimensions, the dual tool-counting method,
and the per-agent analysis procedure.

* 3.1 Agent selection: 22 candidates -> 13 agents via three inclusion
  criteria; the 13-agent table (Table 1) and pinned commits
  (Appendix B / Table 15).
* 3.2 Analysis dimensions: nine dimensions from open coding of two
  pilot agents (Aider + OpenHands); 9 dimensions yielded 12 taxonomy
  dimensions in the results.
* 3.3 Tool counting methodology: registration count + capability
  category count.
* 3.4 Analysis procedure: observation / classification / evidence
  triple; pinned commits; LLM-assisted code navigation.
* 3.5 Scope and limitations: purely taxonomic, no benchmarking.

Methodological claims here are premises for the empirical findings in
s4-s6.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 3.1 Agent selection
# ---------------------------------------------------------------------------

setup_inclusion_criteria = setting(
    "**Three inclusion criteria for the 13-agent corpus (Section 3.1).** "
    "Candidate agents were narrowed by three inclusion criteria: "
    "(1) **Coding-specific** -- designed for software engineering "
    "tasks, not general-purpose task automation (excludes Open "
    "Interpreter, Deep Agents, MetaGPT [@Hong2024MetaGPT], CrewAI); "
    "(2) **Open source with readable implementation** -- "
    "scaffolding code available in a public repository, pinned to a "
    "specific commit (excludes Claude Code, MASAI, GitHub Copilot "
    "Workspace, Cursor, Windsurf); (3) **Architecturally distinct** "
    "-- near-duplicate agents removed. The candidate pool of 22 "
    "agents is in Appendix A (Table 14); 13 were retained.",
    title="Setup: three inclusion criteria for agent selection",
)

claim_table1_thirteen_agents = claim(
    "**Table 1 -- the 13 analyzed agents.** Ordered by GitHub stars "
    "as a proxy for community adoption [@BorgesValente2018]; CLI = "
    "interactive developer use, SWE-bench = automated issue "
    "resolution, Baseline = mini-swe-agent as deliberate minimal "
    "reference [@MiniSWEAgent].\n\n"
    "| Agent | Category | Language | Stars | Origin |\n"
    "|---|---|---|---:|---|\n"
    "| OpenCode [@OpenCode] | CLI | TypeScript | 135k | SST |\n"
    "| Gemini CLI [@GeminiCLI] | CLI | TypeScript | 100k | Google |\n"
    "| Codex CLI [@CodexCLI] | CLI | Rust / TS | 72k | OpenAI |\n"
    "| OpenHands [@OpenHands] | SWE-bench | Python | 70k | All Hands AI |\n"
    "| Cline [@Cline] | CLI | TypeScript | 60k | Independent |\n"
    "| Aider [@Aider] | CLI | Python | 43k | Independent |\n"
    "| SWE-agent [@SWEAgent] | SWE-bench | Python | 19k | Princeton/CMU |\n"
    "| mini-swe-agent [@MiniSWEAgent] | Baseline | Python | 4k | Princeton/CMU |\n"
    "| AutoCodeRover [@AutoCodeRover] | SWE-bench | Python | 3k | NUS/SonarSource |\n"
    "| Agentless [@Agentless] | SWE-bench | Python | 2k | UIUC |\n"
    "| Prometheus [@Prometheus] | SWE-bench | Python | 1k | EuniAI |\n"
    "| Moatless Tools [@MoatlessTools] | SWE-bench | Python | 600 | Independent |\n"
    "| DARS-Agent [@DARSAgent] | SWE-bench | Python | 70 | Independent |\n",
    title="Table 1: 13 agents (CLI / SWE-bench / Baseline) with star counts",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 1"},
)

claim_corpus_distinct_strategies = claim(
    "**The 13-agent corpus spans the architectural strategy range.** "
    "Selected agents span release dates from June 2023 to March "
    "2025 and represent distinct architectural strategies "
    "(fixed pipelines, sequential ReAct loops, phased workflows, "
    "depth-first tree search, full MCTS). Seven of the 13 agents "
    "have each accumulated over 15,000 GitHub stars "
    "[@BorgesValente2018], indicating substantial developer "
    "adoption. The selection is **not exhaustive** but aims to "
    "cover the range of architectural strategies present in the "
    "open-source coding agent ecosystem as of early 2026.",
    title="3.1 corpus aims for analytic generalizability across architectural strategies",
)

claim_table15_pinned_commits = claim(
    "**Table 15 -- pinned commit hashes (Appendix B).** All 13 "
    "agents were analysed at specific git commit hashes, listed in "
    "Appendix B. All file paths and line numbers cited in Section 4 "
    "refer to these specific commits; readers can clone each "
    "repository and check out the listed commit to reproduce or "
    "verify any claim.\n\n"
    "| Agent | Commit | Repository |\n"
    "|---|---|---|\n"
    "| Gemini CLI | dd8d4c98b3 | github.com/google-gemini/gemini-cli |\n"
    "| OpenHands | 922e3a2431 | github.com/OpenHands/OpenHands |\n"
    "| Aider | 861a1e4d15 | github.com/Aider-AI/aider |\n"
    "| Cline | 71e312e92a | github.com/cline/cline |\n"
    "| SWE-agent | e72a7e4660 | github.com/SWE-agent/SWE-agent |\n"
    "| Codex CLI | 9dba7337f2 | github.com/openai/codex |\n"
    "| OpenCode | f54abe58cf | github.com/anomalyco/opencode |\n"
    "| Agentless | 5ce5888b9f | github.com/OpenAutoCoder/Agentless |\n"
    "| AutoCodeRover | 585d3e639a | github.com/AutoCodeRoverSG/auto-code-rover |\n"
    "| Moatless Tools | 011ead57a5 | github.com/aorwall/moatless-tools |\n"
    "| Prometheus | b1c722be02 | github.com/EuniAI/Prometheus |\n"
    "| DARS-Agent | eab35168a9 | github.com/vaibhavagg303/DARS-Agent |\n"
    "| mini-swe-agent | 6f1b196616 | github.com/SWE-agent/mini-swe-agent |\n",
    title="Table 15 (Appendix B): per-agent pinned commit hashes",
    metadata={"source_table": "artifacts/2604.03515.pdf, Table 15"},
)

# ---------------------------------------------------------------------------
# 3.2 Analysis dimensions
# ---------------------------------------------------------------------------

claim_dimension_open_coding_pilot = claim(
    "**Dimensions emerged via open coding of two pilot agents "
    "(Section 3.2).** The nine analysis dimensions were not fixed "
    "a priori. They emerged through iterative *open coding* "
    "[@StraussCorbin1998] during a pilot analysis of two "
    "architecturally contrasting agents -- **Aider** (a simpler, "
    "interactive CLI scaffold) and **OpenHands** (a complex, "
    "event-driven, containerized scaffold) -- chosen to maximize "
    "architectural diversity. The pilot began with six candidate "
    "dimensions drawn from the conceptual literature "
    "[@Masterman2024]; three additional dimensions were added "
    "during piloting after the source code revealed architectural "
    "variation not captured by the initial set: tool discovery "
    "strategy, context compaction, and persistent memory. "
    "Stabilization consisted of re-applying the revised "
    "nine-dimension framework to both pilot agents to confirm "
    "discriminating findings and no source observations falling "
    "outside the framework.",
    title="3.2 open coding of Aider + OpenHands yielded the nine analysis dimensions",
)

claim_nine_analysis_dimensions = claim(
    "**The nine analysis dimensions (Section 3.2).** Each dimension "
    "captures a distinct architectural decision point in the "
    "scaffold:\n\n"
    "1. **Control loop type** (with sub-property *loop driver*).\n"
    "2. **Tool set and tool interface design** (also records edit "
    "and patch format).\n"
    "3. **Tool discovery strategy** (static vs dynamic).\n"
    "4. **State management strategy** (data structure, "
    "append-only/mutable, what is stored).\n"
    "5. **Context retrieval paradigm** (LLM-directed tool calls, "
    "indexes, embedding search, static repo maps).\n"
    "6. **Execution isolation model** (host filesystem, Docker, "
    "subprocess, remote cloud).\n"
    "7. **Context compaction approach** (truncation, sliding "
    "window, summarization, selective dropping).\n"
    "8. **Multi-model routing** (single vs multi-model; routing "
    "decision mechanism).\n"
    "9. **Persistent memory** (what survives between sessions).\n\n"
    "An open-ended **tenth section** captures observations outside "
    "the nine dimensions, following standard qualitative-coding "
    "practice [@Saldana2021]. In practice this section captured 47 "
    "cross-cutting findings.",
    title="3.2 nine analysis dimensions + open-ended tenth section",
)

claim_nine_to_twelve_dimensions = claim(
    "**From 9 analysis dimensions to 12 taxonomy dimensions.** "
    "During analysis, two sub-properties proved sufficiently "
    "discriminating to warrant independent treatment: **loop "
    "driver** (a sub-property of control loop type) and **edit and "
    "patch format** (a sub-property of tool set design) each "
    "produced distinct spectra with their own evidence tables. A "
    "third dimension, **control flow implementation** (the "
    "code-level mechanism realizing the control loop: while loop, "
    "recursion, compiled graph, exception-based signalling), "
    "emerged during analysis as orthogonal to loop topology and is "
    "presented independently. The expansion from 9 analysis "
    "dimensions to 12 taxonomy dimensions is a normal outcome of "
    "qualitative coding [@Saldana2021]: the framework guides data "
    "collection, but the final categories reflect what the data "
    "reveals.",
    title="3.2 9 analysis dims yielded 12 taxonomy dims (3 sub-properties promoted)",
)

claim_three_layer_organization = claim(
    "**Three-layer organization of the 12 taxonomy dimensions.** "
    "The 12 taxonomy dimensions are organized into three layers:\n\n"
    "* **Layer 1: Control architecture** -- how the agent decides "
    "what to do next (3 dimensions: control loop type, loop driver, "
    "control flow implementation).\n"
    "* **Layer 2: Tool and environment interface** -- how the "
    "agent interacts with code and execution environments (5 "
    "dimensions: tool set design, edit/patch format, tool "
    "discovery, context retrieval, execution isolation).\n"
    "* **Layer 3: Resource management** -- how the agent manages "
    "context, state, and models (4 dimensions: state management, "
    "context compaction, multi-model routing, persistent memory).\n\n"
    "Each dimension is presented as a continuous spectrum with "
    "observed endpoints from the corpus.",
    title="3.2 3 layers / 12 dimensions: control / interface / resource",
    metadata={"figure": "artifacts/2604.03515.pdf, Figure 1 (taxonomy overview)"},
)

# ---------------------------------------------------------------------------
# 3.3 Tool counting methodology
# ---------------------------------------------------------------------------

claim_dual_tool_counting = claim(
    "**Dual tool counting (Section 3.3).** Tool counts are reported "
    "using two complementary methods to avoid conflating interface "
    "granularity with functional coverage:\n\n"
    "* **Registration count** -- tallies tools as the LLM sees "
    "them: each separately registered callable (function-calling "
    "schema entry, system-prompt-defined command, equivalent) is "
    "counted once. This measure is sensitive to how scaffold "
    "developers chose to partition functionality.\n"
    "* **Capability category count** -- groups tools by what they "
    "do: **read, search, edit, execute, validate, repository "
    "state**. Categories were derived inductively from the pilot "
    "and validated against the remaining 11 agents. This measure is "
    "comparable across agents regardless of granularity choices: "
    "an agent with one `bash` tool and an agent with separate "
    "`run command`, `run tests`, and `run linter` tools both cover "
    "the execute category.\n\n"
    "Both counts are reported; the capability category count is "
    "used for cross-agent comparison.",
    title="3.3 registration count + capability category count -- granularity vs coverage",
)

# ---------------------------------------------------------------------------
# 3.4 Analysis procedure
# ---------------------------------------------------------------------------

claim_observation_classification_evidence = claim(
    "**Three-level observation/classification/evidence template "
    "(Section 3.4).** Each agent was analyzed using a structured "
    "template derived from the nine dimensions, applied "
    "consistently across all 13 agents. The template separates "
    "three levels of description, following the case-study "
    "principle that empirical claims should be traceable to primary "
    "data sources rather than inferred from secondary documentation "
    "[@RunesonHost2009]:\n\n"
    "* **Observation** -- what the code does, in terms of data "
    "flow and control flow with specific file and line references.\n"
    "* **Classification** -- how the observed behavior maps to a "
    "taxonomy dimension, with explicit justification.\n"
    "* **Evidence** -- a file path and line number pinned to the "
    "specific commit hash analysed.\n\n"
    "The template was piloted on the same two agents used for "
    "dimension development (Aider and OpenHands), surfacing the "
    "need for the dual tool-counting methodology after observing "
    "raw tool counts were not comparable across agents with "
    "different interface granularity.",
    title="3.4 observation/classification/evidence triple -- traceable to file/line",
)

claim_pinned_commits_for_reproducibility = claim(
    "**Pinned commits for reproducibility (Section 3.4).** All "
    "analyses were pinned to specific git commit hashes (Appendix "
    "B). Several agents (Cline, Aider, OpenHands, Gemini CLI) were "
    "under active development during the analysis period; unpinned "
    "analysis would yield unreproducible results. Where source code "
    "was ambiguous, the analysis records uncertainty explicitly "
    "rather than assigning a confident classification. Dimensions "
    "that genuinely do not apply to an agent (e.g. persistent "
    "memory in agents without inter-session storage) are recorded "
    "as **absent**, not omitted.",
    title="3.4 pinned commits + explicit uncertainty + absent != omitted",
)

claim_llm_assisted_navigation = claim(
    "**LLM-assisted code navigation (Section 3.4).** All analyses "
    "were conducted by the author with substantial use of LLM-based "
    "coding assistants for code navigation, call-chain tracing, and "
    "initial summarization of unfamiliar codebases. **All "
    "LLM-generated observations were verified against the source "
    "code** before inclusion in the analysis documents; the "
    "analysis documents themselves record file paths and line "
    "numbers to enable independent verification. The single-author "
    "design is a threat to construct validity -- mitigations are "
    "discussed in Section 6 (claim *single-author bias mitigation* "
    "in s8).",
    title="3.4 LLM-assisted navigation, verified manually, single-author design",
)

# ---------------------------------------------------------------------------
# 3.5 Scope and limitations
# ---------------------------------------------------------------------------

claim_scope_taxonomic_only = claim(
    "**Purely taxonomic scope (Section 3.5).** This study is purely "
    "taxonomic. **No performance benchmarking was conducted, and no "
    "claims are made about correlations between scaffold design and "
    "task success rates.** The decision to exclude performance "
    "analysis reflects two limitations: (1) SWE-bench results "
    "across agents are not directly comparable because different "
    "agents used different underlying models, and model capability "
    "is a larger confounder than scaffold design; (2) documented "
    "solution leakage in SWE-bench issue descriptions [@Garg2026] "
    "makes raw pass rates an unreliable signal regardless of "
    "controls.",
    title="3.5 scope is purely taxonomic -- no benchmarking, no scaffold->performance claims",
)

# ---------------------------------------------------------------------------
# Verification of the 296-claim evidence base
# ---------------------------------------------------------------------------

claim_verification_pass = claim(
    "**Post-hoc verification of the evidence base (Section 6.1).** "
    "A post-hoc verification pass checked **296 extracted claims** "
    "against the cloned repositories. The pass confirmed **267**, "
    "corrected **19** (primarily line-number offsets from code "
    "evolution between analysis and verification), and accepted "
    "**10** as minor simplifications (e.g. describing a multi-step "
    "process in fewer steps than the code implements, or "
    "attributing a behaviour to a single function when it spans "
    "two). The verification pass was performed by the same "
    "researcher who conducted the original analysis -- weaker than "
    "independent review, but the commit-pinned evidence trail makes "
    "independent verification straightforward.",
    title="3.4/6.1 verification: 267 confirmed / 19 corrected / 10 minor of 296 claims",
)

__all__ = [
    "setup_inclusion_criteria",
    "claim_table1_thirteen_agents",
    "claim_corpus_distinct_strategies",
    "claim_table15_pinned_commits",
    "claim_dimension_open_coding_pilot",
    "claim_nine_analysis_dimensions",
    "claim_nine_to_twelve_dimensions",
    "claim_three_layer_organization",
    "claim_dual_tool_counting",
    "claim_observation_classification_evidence",
    "claim_pinned_commits_for_reproducibility",
    "claim_llm_assisted_navigation",
    "claim_scope_taxonomic_only",
    "claim_verification_pass",
]
