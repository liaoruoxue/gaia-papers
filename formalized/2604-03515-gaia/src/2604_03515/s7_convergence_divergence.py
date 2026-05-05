"""Section 5 (Discussion) -- the cross-cutting convergence/divergence pattern.

Sections 5.1-5.3 of Rombaut 2026 [@Rombaut2026]. Interprets the
12-dimension findings along three lines:

* 5.1 Spectra, not categories: agents lie on continuous spectra; loop
  primitives compose freely; design space is combinatorial.
* 5.2 Convergence and divergence: dimensions converge where external
  constraints dominate (tool capability, edit format, execution
  isolation); diverge where open design questions remain (compaction,
  state, routing).
* 5.3 The scaffold-model interface: scaffold design mediates model
  capability; loop driver is the most fundamental.

Threats-to-validity claims (Section 6) that affect interpretation are
also placed here so the synthesis module can wire them into the
abductions and contradictions.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 5.1 Spectra not categories -- the consolidated claim
# ---------------------------------------------------------------------------

claim_spectral_finding_consolidated = claim(
    "**Section 5.1 -- consolidated spectral finding.** The most "
    "persistent finding across all 12 dimensions is that scaffold "
    "architectures **resist discrete classification**. Within each "
    "spectrum, agents occupy distinct positions reflecting genuine "
    "architectural tradeoffs:\n\n"
    "* **Control loop**: fixed pipeline -> user-driven loop -> "
    "sequential ReAct -> phased loop -> depth-first tree search -> "
    "full MCTS (6 positions, Table 2).\n"
    "* **Tool count**: 0 (Aider) to 37 action classes (Moatless "
    "Tools) (Table 5).\n"
    "* **Context compaction**: none (mini-swe-agent crashes) to "
    "LLM-initiated compaction (Cline) -- 7 distinct strategies "
    "(Table 11).\n"
    "* **State management**: destructive overwrite (Aider) to "
    "event sourcing (OpenHands) -- 8 variants (Table 10).\n\n"
    "**Every agent in the corpus qualifies as 'tool-using, "
    "memory-augmented, planning, reflective' under prior "
    "capability-based taxonomies** [@Masterman2024; "
    "@Nowaczyk2025], yet their implementations differ in ways "
    "those labels cannot express.",
    title="5.1 spectral finding: 12 continuous spectra, not discrete categories",
)

claim_combinatorial_design_space = claim(
    "**Section 5.1 -- combinatorial structural explanation.** The "
    "spectral character has a **structural explanation**: the "
    "loop primitives identified in Section 4.1.1 (ReAct, "
    "generate-test-repair, plan-execute, multi-attempt retry, "
    "tree search) function as **composable building blocks** that "
    "agents freely layer and nest. Because these primitives "
    "compose freely, the space of possible architectures is "
    "**combinatorial rather than categorical**. Assigning a "
    "single label ('ReAct agent', 'pipeline agent') to a system "
    "that layers multiple primitives obscures the design "
    "decisions that actually differentiate it.",
    title="5.1 design space is combinatorial because loop primitives compose freely",
)

claim_decompose_for_evaluation = claim(
    "**Section 5.1 -- prescription: decompose for evaluation.** "
    "For researchers, the spectral finding suggests **evaluating "
    "scaffold dimensions independently** may be more informative "
    "than classifying whole agents. A study comparing 'ReAct "
    "agents' against 'pipeline agents' conflates loop topology, "
    "loop driver, tool set design, and context management into a "
    "single binary. Decomposing along the dimensions identified "
    "here would allow more precise attribution. For practitioners, "
    "the composability suggests design decisions may be **more "
    "orthogonal than they appear**: Moatless Tools demonstrates "
    "that tree search can be layered over an existing per-step "
    "agent without rewriting the agent logic, though whether all "
    "dimension combinations are equally feasible remains an open "
    "empirical question.",
    title="5.1 prescription: decompose along dimensions; not all combinations may be feasible",
)

# ---------------------------------------------------------------------------
# 5.2 Convergence and divergence
# ---------------------------------------------------------------------------

claim_convergence_externally_constrained = claim(
    "**Section 5.2 -- converging dimensions reflect external "
    "constraints.** The converging dimensions tend to reflect "
    "constraints **external to the scaffold designer**:\n\n"
    "* **Tool capability categories** converge on read/search/edit/"
    "execute (Section 4.2.1) because these are the operations that "
    "software engineering tasks require, regardless of "
    "architectural philosophy.\n"
    "* **Edit format** is trending toward string replacement "
    "(Section 4.2.2) because LLMs produce more reliable edits "
    "with exact string matching than with line-number-based or "
    "unified-diff formats -- whether through independent discovery "
    "or imitation of successful designs [@SWEAgent].\n"
    "* **Execution isolation** converges on Docker containers for "
    "benchmark agents (Section 4.2.5) because autonomous code "
    "execution without sandboxing is unacceptable for unattended "
    "evaluation.\n\n"
    "These convergences reflect **solved problems or hard "
    "constraints**: the design space has been explored, and "
    "practitioners have settled on solutions that work.",
    title="5.2 converging dimensions reflect solved problems / hard external constraints",
)

claim_divergence_open_questions = claim(
    "**Section 5.2 -- diverging dimensions reflect open design "
    "questions.** The diverging dimensions tell a different story:\n\n"
    "* **Context compaction** exhibits **7 distinct strategies** "
    "across 13 agents (Section 4.3.2), from no management at all "
    "to LLM-initiated compression with verification probes.\n"
    "* **State management** ranges from destructive overwrite to "
    "event sourcing, with tree-structured, graph-scoped, and "
    "database-backed variants between (Section 4.3.1).\n"
    "* **Multi-model routing** spans single-model simplicity to "
    "7-layer classifier chains (Section 4.3.3).\n\n"
    "These dimensions diverge because they address **open design "
    "questions where no dominant solution has emerged**. Context "
    "compaction balances information preservation against token "
    "cost, with the optimal tradeoff depending on task length, "
    "model capability, and cost tolerance. The divergence is **not "
    "noise**; it reflects genuine uncertainty.",
    title="5.2 diverging dimensions reflect open questions / unsolved tradeoffs",
)

claim_convergence_divergence_implications = claim(
    "**Section 5.2 -- practical implications.** This pattern has "
    "practical implications. The **converging dimensions are "
    "candidates for standardization**: a shared tool protocol "
    "covering the four capability categories (as the Model Context "
    "Protocol [@MCP2024] begins to attempt) would reduce "
    "duplicated effort without constraining architectural "
    "innovation. The **diverging dimensions are where research "
    "investment is most needed**. The diversity of context "
    "compaction strategies suggests no existing approach fully "
    "solves the 'token snowball' problem [@Fan2025SWEEffi]. The "
    "range of strategies (prevention through structural bounding, "
    "cure through summarization, hybrid approaches) represents an "
    "active design frontier.",
    title="5.2 implications: standardize where converged, research where diverged",
)

# ---------------------------------------------------------------------------
# 5.3 Scaffold-model interface
# ---------------------------------------------------------------------------

claim_scaffold_mediates_model = claim(
    "**Section 5.3 -- scaffold mediates model capability.** The "
    "taxonomy reveals that **scaffold design mediates model "
    "capability** in ways prior work has not systematically "
    "examined. The same underlying LLM behaves differently "
    "depending on:\n\n"
    "* How many tools it sees (0 in Aider vs 35 in SWE-agent, "
    "Section 4.2.1).\n"
    "* How context is managed (full unfiltered history in "
    "mini-swe-agent vs event-sourced views with condensation in "
    "OpenHands, Section 4.3.2).\n"
    "* What loop structure surrounds it (single-pass pipeline in "
    "Agentless vs feedback-driven iteration in SWE-agent, "
    "Section 4.1.1).\n"
    "* Who drives the loop (user in Aider, scaffold in "
    "AutoCodeRover, LLM in OpenHands, Section 4.1.2).\n\n"
    "Each scaffold-level decision shapes what the model sees, "
    "what actions it can take, and how its errors propagate or "
    "get corrected.",
    title="5.3 scaffold mediates model: same LLM behaves differently across tool/context/loop choices",
)

claim_loop_driver_determines_localization_burden = claim(
    "**Section 5.3 -- loop driver determines localization "
    "burden.** The scaffold-model interface explains why the "
    "**loop driver dimension** (Section 4.1.2) is **arguably the "
    "most fundamental architectural distinction**. User-driven "
    "agents sidestep the localization bottleneck entirely, while "
    "LLM-driven agents must solve it -- making retrieval strategy "
    "(Section 4.2.4) a critical co-design choice. **The same "
    "model that performs well with user-curated context may "
    "struggle when forced to navigate a repository "
    "autonomously.** This interaction illustrates why scaffold "
    "dimensions cannot be evaluated in isolation; they form an "
    "**interdependent design space**.",
    title="5.3 loop driver determines whether the LLM must solve localization -- co-design with retrieval",
)

# ---------------------------------------------------------------------------
# 6.2 Internal-validity caveat: dimensions are partially correlated
# ---------------------------------------------------------------------------

claim_dimensions_not_independent = claim(
    "**Section 6.2 -- dimensions are partially correlated, not "
    "fully independent.** Section 5.3 notes that loop driver and "
    "retrieval strategy are correlated: scaffold-driven agents "
    "tend to invest in retrieval infrastructure while LLM-driven "
    "agents rely on general-purpose tools. **Similar correlations "
    "may exist between other dimensions** (e.g. tool discovery "
    "strategy and tool count, or state management and context "
    "compaction). The taxonomy presents dimensions as independent "
    "axes, **but in practice they form an interdependent design "
    "space where choices on one dimension constrain options on "
    "others**. The cross-cutting themes (Section 4.4) capture "
    "some interdependencies; a full analysis of dimension "
    "interactions is beyond the scope of this study.",
    title="6.2 caveat: 12 dimensions are not fully independent (loop driver <-> retrieval correlated)",
)

# ---------------------------------------------------------------------------
# Threats to validity claims that the synthesis module wires in
# ---------------------------------------------------------------------------

claim_single_author_construct_threat = claim(
    "**Section 6.1 -- single-author construct-validity threat.** "
    "The **primary construct-validity threat** is single-author "
    "bias. All 13 agent analyses were conducted by a single "
    "author (with LLM-assisted code navigation), meaning that "
    "dimension classifications, evidence selection, and "
    "cross-agent comparisons reflect one person's interpretation "
    "of the source code. **Two mitigations partially address "
    "this**: (1) every taxonomic claim is grounded in specific "
    "file paths and line numbers pinned to commit hashes, making "
    "each claim independently verifiable (the post-hoc "
    "verification pass confirmed 267/296 claims, corrected 19, "
    "accepted 10 as minor simplifications); (2) the analysis "
    "template separates observation, classification, and evidence, "
    "making it possible for a reader to evaluate the "
    "classification independently of the observation "
    "[@RunesonHost2009].",
    title="6.1 threat: single-author bias; mitigated by commit-pinned evidence + 3-level template",
)

claim_pilot_dimension_coverage_threat = claim(
    "**Section 6.1 -- pilot agents may not have surfaced all "
    "dimensions.** The pilot agents (Aider and OpenHands), while "
    "selected to maximize architectural diversity, may not have "
    "surfaced all relevant dimensions. The open-ended tenth "
    "section of the analysis template was designed to capture "
    "observations outside the predefined dimensions, and produced "
    "47 cross-cutting findings that informed the final taxonomy "
    "(Section 4.4). However, **dimensions that neither pilot "
    "agent exhibits and that no subsequent agent made salient "
    "could still be missing**. For example, the taxonomy does not "
    "include a dimension for **prompt engineering strategy** "
    "(system prompt construction, length, few-shot examples, "
    "personas) -- excluded for scope, but an important aspect of "
    "scaffold design not captured.",
    title="6.1 threat: pilot may have missed dimensions (e.g. prompt engineering deliberately excluded)",
)

claim_taxonomy_is_snapshot = claim(
    "**Section 6.2 -- taxonomy is a snapshot at pinned commits.** "
    "The taxonomy describes source code at pinned commits, but "
    "several agents were under active development during the "
    "analysis period. Architectural features may have been added, "
    "removed, or significantly refactored between the analysed "
    "commit and the current version. **Pinning to specific "
    "commits ensures reproducibility of the reported findings but "
    "means the taxonomy is a snapshot, not a live description.** "
    "The commit hashes are listed in Appendix B / Table 15 so "
    "readers can assess how much each agent has evolved since "
    "analysis.",
    title="6.2 threat: taxonomy is a snapshot; commit hashes enable longitudinal re-analysis",
)

claim_open_source_survivorship_threat = claim(
    "**Section 6.3 -- external-validity: open-source "
    "survivorship.** The corpus is restricted to **open-source "
    "agents with readable source code**. Proprietary coding "
    "agents (GitHub Copilot Workspace, Cursor's AI backend, "
    "Windsurf) and agents with compiled or obfuscated source code "
    "(Claude Code) are excluded because their scaffolding is not "
    "publicly inspectable. **This introduces a survivorship "
    "bias**: open-source agents may systematically differ from "
    "proprietary agents in design choices driven by business "
    "constraints, proprietary model access, or different "
    "optimization targets (user experience vs benchmark scores). "
    "The taxonomy should be understood as describing the "
    "**open-source design space, not the full design space** of "
    "coding agents.",
    title="6.3 threat: open-source survivorship -- proprietary agents (Copilot, Cursor, Windsurf, Claude Code) excluded",
)

claim_analytic_not_statistical_generalizability = claim(
    "**Section 6.3 -- analytic, not statistical generalizability.** "
    "The corpus of 13 agents, while covering a range of "
    "architectural strategies, is **not exhaustive**. Agents "
    "released after the analysis period or that did not meet "
    "inclusion criteria may exhibit architectural patterns not "
    "represented. The study aims for **analytical "
    "generalizability** [@Yin2018] (the dimensions and spectra "
    "should be useful for characterizing new agents) rather than "
    "**statistical generalizability** (the distribution of agents "
    "across dimension positions is not claimed to be "
    "representative of any population). As the ecosystem evolves, "
    "both new dimensions and new positions on existing dimensions "
    "are likely to emerge.",
    title="6.3 generalizability: analytic (dimensions transfer) not statistical (distribution unclaimed)",
)

claim_python_dominance_threat = claim(
    "**Section 6.3 -- Python dominance limits cross-language "
    "generality.** The corpus is dominated by **agents targeting "
    "Python-language repositories**, primarily because SWE-bench "
    "(the dominant evaluation benchmark) uses Python projects "
    "exclusively. Agents designed for multi-language or "
    "non-Python ecosystems may face different architectural "
    "constraints (different AST parsing requirements, build/test "
    "toolchains, dependency resolution patterns) that could "
    "produce architectural variation not observed here "
    "[@Jimenez2024SWEbench; @Xu2025SWECompass]. Prometheus's "
    "20-language tree-sitter support and SWE-agent's "
    "language-agnostic shell-based approach suggest some agents "
    "address this limitation, but the analysis does not "
    "systematically evaluate cross-language variation.",
    title="6.3 threat: SWE-bench Python bias may have suppressed multi-language architectural variation",
)

claim_static_analysis_misses_runtime = claim(
    "**Section 6.4 -- static source-code analysis misses runtime "
    "behaviour.** Some architectural features (MCP tool discovery "
    "in practice; whether configurable features like Moatless "
    "Tools' pluggable selector are used in typical deployments) "
    "may only be visible at runtime. **The taxonomy describes "
    "architectural capability, not observed runtime behaviour.**",
    title="6.4 threat: static analysis misses runtime behaviour -- capability not equal observed usage",
)

__all__ = [
    "claim_spectral_finding_consolidated",
    "claim_combinatorial_design_space",
    "claim_decompose_for_evaluation",
    "claim_convergence_externally_constrained",
    "claim_divergence_open_questions",
    "claim_convergence_divergence_implications",
    "claim_scaffold_mediates_model",
    "claim_loop_driver_determines_localization_burden",
    "claim_dimensions_not_independent",
    "claim_single_author_construct_threat",
    "claim_pilot_dimension_coverage_threat",
    "claim_taxonomy_is_snapshot",
    "claim_open_source_survivorship_threat",
    "claim_analytic_not_statistical_generalizability",
    "claim_python_dominance_threat",
    "claim_static_analysis_misses_runtime",
]
