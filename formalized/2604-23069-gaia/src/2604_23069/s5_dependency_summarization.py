"""Section 3.2: Dependency Summarizer.

Section 3.2 of [@Wu2026ContextWeaver]. The Dependency Summarizer attaches a
brief 'dependency summary' to each node, recording the main reasoning
dependency from the root to that node. Summaries are built *incrementally*
from parent summaries plus the current node's summary, rather than by
re-summarizing the whole history at every step.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Definition
# ---------------------------------------------------------------------------

setup_dependency_summary_field = setting(
    "**Dependency summary field.** Each node $N_k$ maintains a brief "
    "*dependency summary* (a separate field from the node's own "
    "summary) recording the main reasoning dependency *from the root to "
    "that node*, i.e., a compressed narrative of the trajectory "
    "supporting $N_k$ [@Wu2026ContextWeaver, Sec. 3.2].",
    title="Setup: per-node dependency_summary field records root-to-node reasoning narrative",
)

setup_llmsum_summarizer = setting(
    "**LLM-based summarizer $\\mathrm{LLM}_{\\mathrm{SUM}}$.** A "
    "dedicated LLM-based summarization function "
    "$\\mathrm{LLM}_{\\mathrm{SUM}}$ (prompt template in Appendix A.2) "
    "produces dependency summaries from inputs of (i) the parents' "
    "dependency summaries and (ii) the current node's own summary "
    "[@Wu2026ContextWeaver, Sec. 3.2, Appendix A.2].",
    title="Setup: LLM_SUM is the dedicated summarizer function",
)

# ---------------------------------------------------------------------------
# Recurrence (the contribution)
# ---------------------------------------------------------------------------

claim_incremental_recurrence = claim(
    "**Incremental dependency-summary recurrence:**\n\n"
    "$$\\text{dependency\\_summary}_k = \\mathrm{LLM}_{\\mathrm{SUM}}"
    "\\bigl( \\{ \\text{dependency\\_summary}_i \\mid N_i \\in S_k \\}, "
    "\\, \\text{summary}_k \\bigr).$$\n\n"
    "The dependency summary of node $N_k$ is computed from (i) the "
    "dependency summaries of its parents (already cached in the parent "
    "nodes) plus (ii) the current node's own summary. This is the "
    "key construction: the root-to-step path is *compressed "
    "incrementally* into a single reusable unit per node "
    "[@Wu2026ContextWeaver, Sec. 3.2].",
    title="Recurrence: dep_summary_k = LLMSUM({parent.dep_summary}, summary_k)",
)

claim_incremental_advantage_cost = claim(
    "**Advantage 1 of incremental summarization: substantially reduced "
    "computational cost.** The incremental approach avoids repeated "
    "processing of the entire history at every step: each step's "
    "summary is computed once, in $O(|S_k|)$ summary inputs, rather "
    "than re-summarizing the full $k$-step trajectory each time. This "
    "yields a substantial reduction in compute as trajectories grow "
    "long [@Wu2026ContextWeaver, Sec. 3.2].",
    title="Advantage: O(|S_k|) summary inputs per step (no full-history re-summarization)",
)

claim_incremental_advantage_structure = claim(
    "**Advantage 2 of incremental summarization: preserves a compact "
    "dependency-structured memory of how earlier steps guide later "
    "reasoning.** Because each summary is composed of parent-path "
    "summaries plus the new step, the resulting per-node summary "
    "preserves the *structural shape* of the reasoning path "
    "(branches and merges encoded by which parents contributed) rather "
    "than collapsing it into flat prose "
    "[@Wu2026ContextWeaver, Sec. 3.2].",
    title="Advantage: preserves dependency-structured memory of how earlier steps guide later",
)

# ---------------------------------------------------------------------------
# Usage discipline
# ---------------------------------------------------------------------------

claim_dep_summary_usage_discipline = claim(
    "**Dependency summaries are used only for dependency analysis, "
    "never injected directly into the final agent context.** Per the "
    "configuration described in Appendix F.2, the dependency summary "
    "is consumed by the parent-selection analyzer (to reason about "
    "candidate dependencies) but is never spliced into the final "
    "context $C$ delivered to the action LLM. The final context "
    "instead contains the full $T$-$A$-$O$ triples for ancestors "
    "[@Wu2026ContextWeaver, Appendix F.2].",
    title="Usage discipline: dep_summaries inform analyzer only, NOT injected into agent context",
)

claim_root_to_step_reusable_unit = claim(
    "**Each dependency summary is a *reusable unit* shared by all of "
    "the node's descendants.** Because the summary is computed *once* "
    "per node and cached, every descendant of $N_k$ that needs to "
    "reason about $N_k$'s ancestry can simply read $N_k$'s dependency "
    "summary rather than recomputing it. This reusability is what "
    "makes the per-step compute cost bounded "
    "[@Wu2026ContextWeaver, Sec. 3.2].",
    title="Reusable unit: per-node summary is cached and reused by all descendants",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "setup_dependency_summary_field",
    "setup_llmsum_summarizer",
    "claim_incremental_recurrence",
    "claim_incremental_advantage_cost",
    "claim_incremental_advantage_structure",
    "claim_dep_summary_usage_discipline",
    "claim_root_to_step_reusable_unit",
]
