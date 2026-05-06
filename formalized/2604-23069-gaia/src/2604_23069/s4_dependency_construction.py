"""Section 3.1: Dependency-Aware Context Construction.

Section 3.1 of [@Wu2026ContextWeaver] decomposes the construction module
into four sub-procedures: Node Extraction, Parent Selection (LLM-based
Logical Dependency Analyzer), Ancestry Dependency Construction (BFS up the
DAG), and Context Weaving (full triples for ancestors + compressed
observations for non-ancestors). Each sub-procedure is captured as an
atomic claim so its design choice can be reviewed independently.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Sub-procedure 1: Node Extraction (Sec 3.1)
# ---------------------------------------------------------------------------

claim_node_summary_content = claim(
    "**Node summary captures thought, action, and resulting observation "
    "for the latest step.** The 'summary' field of node $N_k$ encodes a "
    "condensed representation of the agent's thought $T_k$, action "
    "$A_k$, and observation $O_k$, providing a compact reusable record "
    "of the latest reasoning step for downstream dependency analysis "
    "[@Wu2026ContextWeaver, Sec. 3.1].",
    title="Node summary = (thought, action, observation) of latest step",
)

claim_node_extraction_query_conditioned = claim(
    "**Node extraction is query-conditioned, not generic.** The mapping "
    "$\\phi(H_k, Q)$ summarizes the latest step *given* the user query "
    "$Q$, rather than producing a generic summary. This conditioning "
    "ensures the extracted node retains information likely to be "
    "relevant for downstream reasoning toward the user's task, instead "
    "of compressing toward generic-prose averages "
    "[@Wu2026ContextWeaver, Sec. 3.1].",
    title="Design: phi(H_k, Q) is query-conditioned to retain task-relevant detail",
)

# ---------------------------------------------------------------------------
# Sub-procedure 2: Parent Selection (LLM-based dependency analyzer)
# ---------------------------------------------------------------------------

claim_logical_dependency_analyzer = claim(
    "**Parent selection uses an LLM-based 'Logical Dependency "
    "Analyzer'.** For each new node $N_k$, ContextWeaver invokes an "
    "LLM-based analyzer that scores each candidate predecessor $N_i$ by "
    "$\\mathrm{LLM}(N_i \\to N_k \\mid Q)$ -- the estimated likelihood "
    "that $N_k$ depends on $N_i$. The analyzer's full system prompt "
    "instructs it to focus on information flow and causal relationships "
    "rather than file similarity "
    "[@Wu2026ContextWeaver, Sec. 3.1, Appendix A.2].",
    title="Parent selection: LLM scores LLM(N_i -> N_k | Q) per candidate",
)

claim_top_m_parents = claim(
    "**Parent selection returns the top-$m$ scored parents.** Given "
    "candidate set $C_k$ (all currently valid nodes -- not marked "
    "FAILED or SUPERSEDED), the analyzer returns\n\n"
    "$$S_k = \\mathrm{Top}_{N_i \\in C_k}^{m} \\, "
    "\\mathrm{LLM}(N_i \\to N_k \\mid Q),$$\n\n"
    "the top-$m$ candidates by dependency score. Edges $N_i \\to N_k$ "
    "for all $N_i \\in S_k$ are added to the DAG "
    "[@Wu2026ContextWeaver, Sec. 3.1, Algorithm 1 line 6-7].",
    title="Top-m parent selection: S_k = top-m by LLM dependency score",
)

claim_parent_selection_is_reasoning = claim(
    "**Parent selection is treated as a reasoning task, not a similarity "
    "check.** For each candidate, the analyzer reasons about whether the "
    "current step depends on earlier information -- e.g., whether the "
    "step *uses a prior result*, *returns to an earlier issue*, or "
    "*continues a line of reasoning* -- rather than scoring by surface "
    "lexical or file overlap. This produces a graph that reflects "
    "genuine information flow rather than recency or superficial "
    "similarity [@Wu2026ContextWeaver, Sec. 3.1].",
    title="Design: parent selection is reasoning over information flow, not similarity",
)

claim_logical_analyzer_prompt_design = claim(
    "**The analyzer prompt explicitly prefers branching over chaining.** "
    "The system prompt (Appendix A.2) instructs the analyzer to: "
    "(i) prefer branching over chaining for exploration operations, "
    "(ii) treat phase transitions (implementation/testing) as needing "
    "broader context not just immediate predecessors, (iii) ignore "
    "temporal proximity / file similarity / generic-area overlap as "
    "primary signals, and (iv) emit a structured JSON output containing "
    "selected_parent_id, confidence, and a brief reasoning explanation "
    "[@Wu2026ContextWeaver, Appendix A.2].",
    title="Analyzer prompt: branch>chain, ignore proximity/similarity, emit structured JSON",
)

# ---------------------------------------------------------------------------
# Sub-procedure 3: Ancestry Dependency Construction
# ---------------------------------------------------------------------------

claim_ancestry_bfs = claim(
    "**Ancestry construction = upward BFS through parent edges, bounded "
    "by $W$.** After parents $S_k$ are identified, ContextWeaver "
    "collects the prior reasoning steps that causally or logically "
    "contribute to $N_k$ by constructing the ancestry set $A$ -- all "
    "nodes that directly or indirectly support $N_k$. The traversal is "
    "a breadth-first search starting from $N_k$ and expanding along "
    "parent edges; it terminates when the queue is exhausted or "
    "$|A| \\geq W$ [@Wu2026ContextWeaver, Sec. 3.1, Algorithm 1 "
    "lines 11-16].",
    title="Ancestry: upward BFS through parents, terminates at queue empty or |A| >= W",
)

claim_ancestry_purpose = claim(
    "**The ancestry set determines which history entries are retained "
    "in full.** The selected ancestors $A$ govern the final context $C$ "
    "in the next sub-procedure: every history entry whose corresponding "
    "node is in $A$ is kept verbatim, while non-ancestor entries have "
    "their observations compressed. This is the central selectivity "
    "mechanism: ancestry is computed by *dependency reasoning*, not "
    "recency or similarity [@Wu2026ContextWeaver, Sec. 3.1].",
    title="Ancestry set drives selectivity: in-A => full triple, not-in-A => observation compressed",
)

# ---------------------------------------------------------------------------
# Sub-procedure 4: Context Weaving (output construction)
# ---------------------------------------------------------------------------

claim_context_weaving_rule = claim(
    "**Context-weaving rule: ancestors get full $T$-$A$-$O$; "
    "non-ancestors keep $T$ and $A$ but observation $O$ is compressed.** "
    "The final context $C$ is constructed as follows: for each history "
    "index $i = 0, \\dots, k$, if the corresponding node is in the "
    "ancestry set $A$, append the full triple $H_i = (T_i, A_i, O_i)$; "
    "otherwise append a compressed version that retains $T_i$ and $A_i$ "
    "but replaces $O_i$ with a lightweight placeholder "
    "[@Wu2026ContextWeaver, Sec. 3.1 (Context Weaving), Appendix D].",
    title="Weaving: ancestors full triple; non-ancestors keep T+A, compress O",
)

claim_observation_compression_format = claim(
    "**Observation-compression placeholder: 'Old environment output: "
    "(N lines omitted) (M images omitted)'.** For history entries "
    "outside the selected dependency subgraph, ContextWeaver replaces "
    "the original observation content with a lightweight placeholder "
    "that records the amount of omitted content, where $N$ is the count "
    "of omitted text lines and $M$ is the count of omitted images. "
    "This mirrors the lightweight truncation used in the sliding-window "
    "baseline, ensuring that token savings arise from "
    "*structure-aware selection* rather than aggressive semantic "
    "summarization [@Wu2026ContextWeaver, Appendix D].",
    title="Observation placeholder: '(N lines omitted) (M images omitted)' (Appendix D)",
)

claim_compression_parity_with_baseline = claim(
    "**Observation compression matches the sliding-window baseline so "
    "differences arise from structure-aware *selection*, not aggressive "
    "compression.** Because both ContextWeaver and the sliding-window "
    "baseline use the same lightweight observation-compression strategy, "
    "any performance difference between them is attributable to *which* "
    "entries are kept in full (dependency-based vs. recency-based "
    "selection) rather than to differences in compression aggressiveness "
    "[@Wu2026ContextWeaver, Sec. 4.1, Appendix D].",
    title="Compression parity: same compression rule across CW and SW => isolates selection effect",
)

# ---------------------------------------------------------------------------
# Walkthrough exhibit (Appendix E.2)
# ---------------------------------------------------------------------------

claim_walkthrough_pytest_5262 = claim(
    "**Algorithm 1 walkthrough on `pytest-dev pytest-5262` (Appendix "
    "E.2).** A complete step-level trace is provided for node "
    "$N_{18}$ (the agent has just applied a fix and is about to validate "
    "it). Parent selection picks $\\{N_{12}, N_{16}\\}$ (root-cause "
    "analysis + failure confirmation). The merged ancestry "
    "$\\mathcal{P}_{18} = \\{N_6, N_8, N_{12}, N_{14}, N_{16}\\}$ is "
    "computed via two backward chains "
    "($N_{12} \\to N_8 \\to N_6$ and "
    "$N_{16} \\to N_{14} \\to N_8 \\to N_6$). Phase 2 is entered "
    "because $|H| = 18 > W = 5$. Full $T$-$A$-$O$ detail is retained "
    "for $\\{N_6, N_8, N_{12}, N_{14}, N_{16}, N_{18}\\}$; "
    "observations for $H_1$-$H_5, H_7, H_9$-$H_{11}, H_{13}, H_{15}, "
    "H_{17}$ are elided "
    "[@Wu2026ContextWeaver, Appendix E.2].",
    title="Walkthrough (pytest-5262, N_18): parents={N_12,N_16}; ancestry={N_6,N_8,N_12,N_14,N_16}",
    metadata={"figure": "artifacts/2604.23069.pdf, Appendix E.2"},
)

# ---------------------------------------------------------------------------
# Validation summary prepended to context (Appendix A)
# ---------------------------------------------------------------------------

claim_prepended_test_summary = claim(
    "**Validation summary is prepended to the assembled prompt before "
    "sending to the agent.** Once the context has been selected and "
    "compressed, ContextWeaver prepends the most recent validation "
    "summary (e.g., 'TEST STATUS: ✓ test_basic: PASSED, "
    "✗ test_login_validation: FAILED') to the assembled prompt "
    "before sending it to the agent. This keeps the model explicitly "
    "aware of which tests have passed or failed, ensuring future "
    "reasoning steps build on verified results "
    "[@Wu2026ContextWeaver, Appendix A].",
    title="Prepended test summary makes pass/fail status explicit to the model",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "claim_node_summary_content",
    "claim_node_extraction_query_conditioned",
    "claim_logical_dependency_analyzer",
    "claim_top_m_parents",
    "claim_parent_selection_is_reasoning",
    "claim_logical_analyzer_prompt_design",
    "claim_ancestry_bfs",
    "claim_ancestry_purpose",
    "claim_context_weaving_rule",
    "claim_observation_compression_format",
    "claim_compression_parity_with_baseline",
    "claim_walkthrough_pytest_5262",
    "claim_prepended_test_summary",
]
