"""Revision-semantics scope, NL-to-triple boundary, partial-merging strategies,
symbolic <-> sub-symbolic bridge (Sections 7 and 8.6-8.7 of [@Park2026Kumiho]).

This module captures the *scope and limits* of the formal layer rather than
the postulates themselves (which live in `s5_agm_correspondence.py`). It
includes: the NL-to-triple mapping as a pre-formal step, the three partial-
merging strategies, the symbolic / sub-symbolic asymmetric bridge, and the
deprecated/superseded retrieval semantics.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# NL-to-triple mapping (Section 7)
# ---------------------------------------------------------------------------

claim_nl_to_triple_boundary = claim(
    "**The NL-to-triple mapping is a pre-formal step at the API boundary.** "
    "The agent's natural-language belief (e.g., 'the user prefers cool "
    "tones') is decomposed into typed fields by the `memory_ingest` MCP "
    "tool: `title` becomes the item name, `summary` becomes the revision's "
    "primary content, `tags`/`topics` become metadata keywords, and "
    "`memory_type` classifies the entry. Concretely, the statement 'the "
    "user prefers cool tones' maps to "
    "$\\langle \\texttt{color-preference}, \\texttt{summary}, \\text{prefers "
    "cool tones} \\rangle \\in \\mathrm{At}_G$. The triple structure $(s,p,o)$ "
    "arises from item-field-value decomposition: subject = item name, "
    "predicate = field name, object = field value. This is **not** semantic "
    "parsing -- it is structured output the LLM agent produces by following "
    "its memory skill prompt. The mapping is **lossy by design**: the "
    "ground triple captures only the distilled belief; the full "
    "conversational context is preserved as the artifact "
    "[@Park2026Kumiho, Sec. 7].",
    title="NL-to-triple boundary: structured API contract, not automated NLP extraction",
)

claim_property_graph_not_rdf = claim(
    "**Property graph, not RDF.** Despite the $(s,p,o)$ notation, the "
    "underlying storage is a labeled property graph (Neo4j), not an RDF "
    "triple store. Each memory item is a graph node with typed properties; "
    "each revision is a separate node linked by Supersedes edges; "
    "inter-item relationships (Depends_On, Derived_From, etc.) are "
    "first-class typed edges with optional metadata. The ground-triple "
    "formalism in $\\mathrm{At}_G$ is an **analytical abstraction** for "
    "establishing the AGM correspondence, not an architectural commitment "
    "to triple stores. The property graph supports per-edge metadata, "
    "native node-level indexing, and schema-flexible property bags absent "
    "from basic RDF [@Park2026Kumiho, Sec. 7].",
    title="Property graph != RDF: ground triples are analytical abstraction only",
)

claim_nl_mapping_scope_limit = claim(
    "**The formal guarantees are bounded by NL-to-triple mapping quality.** "
    "The mapping is many-to-one in practice -- the same natural-language "
    "belief could be mapped to different ground triples depending on the "
    "agent's choice of item name, summary wording, or metadata structure. "
    "Two semantically identical beliefs may therefore not be syntactically "
    "identical in $\\mathrm{At}_G$, which means Extensionality ($K^\\ast 6$) "
    "holds over the formal representation but cannot guarantee that the "
    "agent will consistently map equivalent NL inputs to equivalent ground "
    "atoms. This is an inherent limitation of any system that bridges "
    "informal and formal representations; the consistency of the mapping "
    "is a prompt-engineering concern, not a formal one. The formal analysis "
    "begins **after** beliefs have been committed to the graph as ground "
    "triples [@Park2026Kumiho, Sec. 7 'Scope boundary'].",
    title="Scope: formal guarantees apply post-NL-mapping; mapping consistency is a prompt-engineering concern",
)

# ---------------------------------------------------------------------------
# Partial merging strategies (Section 7)
# ---------------------------------------------------------------------------

claim_partial_merge_atomic_replacement = claim(
    "**Partial-merge strategy (i): atomic replacement (current default).** "
    "The agent creates a new revision $r_i^{(k+1)}$ with content "
    "$\\{A', B, C\\}$, superseding $r_i^{(k)}$ entirely. This preserves "
    "the formal properties cleanly because each revision is a self-"
    "contained belief snapshot, but requires the agent (or its memory "
    "skill prompt) to re-include unchanged beliefs $B, C$ in the new "
    "revision. In practice, the `memory_ingest` MCP tool handles this by "
    "accepting the full updated content [@Park2026Kumiho, Sec. 7 "
    "'Granularity of revision'].",
    title="Partial-merge (i): atomic replacement = whole-revision swap (clean formal properties)",
)

claim_partial_merge_finer_atomicity = claim(
    "**Partial-merge strategy (ii): finer-grained atomicity (deployment "
    "option).** Storing one belief per item ($|\\phi(r_i^{(k)})| = 1$ for "
    "all revisions) makes partial updates trivial -- revising $A$ affects "
    "only the item containing $A$. This increases item count but "
    "simplifies the revision operator to single-belief replacement; the "
    "formal properties are preserved and simplified "
    "[@Park2026Kumiho, Sec. 7 'Granularity of revision'].",
    title="Partial-merge (ii): one belief per item (trivial partial updates, more items)",
)

claim_partial_merge_semantic_future = claim(
    "**Partial-merge strategy (iii): LLM-powered semantic merge (future "
    "work).** An LLM-powered merge operator could take the old revision "
    "content and the new input, producing a merged result that preserves "
    "unchanged sub-beliefs while updating only contradictory ones. This "
    "introduces LLM-dependent non-determinism into the revision operator, "
    "complicating formal guarantees: the merge output depends on the LLM's "
    "interpretation of 'partial conflict,' which is not formally "
    "characterizable. Identified as future work, potentially building on "
    "Konieczny and Pino Perez's [@KoniecznyPinoPerez2002] merging framework "
    "[@Park2026Kumiho, Sec. 7 'Granularity of revision'; Sec. 16.2].",
    title="Partial-merge (iii): LLM semantic merge (future work; non-determinism complicates formalism)",
)

# ---------------------------------------------------------------------------
# Compound revision inputs and operational decomposition (Section 7.2)
# ---------------------------------------------------------------------------

claim_compound_input_two_strategies = claim(
    "**Compound revision $A \\wedge B$ admits two operational strategies.** "
    "Strategy 1 (single-revision encoding): the agent stores $A \\wedge B$ "
    "as a single revision whose content set is $\\phi(r) = \\{A, B\\}$. "
    "Strategy 2 (sequential decomposition): first revise by $A$, then "
    "expand by $B$ -- compute $(\\mathcal{B} \\ast A) + B$. By "
    "$K^\\ast 7$ + $K^\\ast 8$, when $B$ is consistent with the "
    "$A$-revised state, both strategies yield the same result. For the "
    "deployed system, where inputs are predominantly ground atoms (and "
    "distinct ground atoms are logically independent), this conflict "
    "condition does not arise: the system's single-belief operational "
    "interface is not a limitation but a practical decomposition that "
    "preserves formal guarantees in the common case "
    "[@Park2026Kumiho, Sec. 7.2 'Compound revision inputs'].",
    title="Compound input: single-revision encoding OR sequential decomposition (both formal-equivalent for atoms)",
)

# ---------------------------------------------------------------------------
# 8.6: Retrieval semantics under belief revision (closing loop)
# ---------------------------------------------------------------------------

claim_deprecated_filter_architectural = claim(
    "**Deprecated revisions are filtered architecturally, not by "
    "convention.** Both retrieval branches (fulltext and vector) apply a "
    "mandatory filter: only revisions belonging to non-deprecated items "
    "($I_{\\mathrm{active}}$) are candidates for scoring. This filter is "
    "enforced at the Cypher query level (a `WHERE NOT item.deprecated` "
    "clause), making it architecturally guaranteed rather than convention-"
    "dependent. The consequence: contraction via deprecation immediately "
    "and completely removes beliefs from the agent's retrieval surface; "
    "neither vector similarity nor fulltext can return deprecated items "
    "without explicit `include_deprecated=true` "
    "[@Park2026Kumiho, Sec. 8.6].",
    title="Deprecated filter: WHERE NOT item.deprecated at Cypher level (architectural guarantee)",
)

claim_superseded_not_excluded = claim(
    "**Superseded revisions are NOT automatically excluded from retrieval.** "
    "A superseded revision is one for which a newer revision exists with a "
    "Supersedes edge. The retrieval surface $\\mathcal{B}_{\\mathrm{retr}}"
    "(\\tau)$ is defined by tag assignments and deprecation status, not by "
    "the Supersedes edge structure. If a superseded revision still carries "
    "an active tag (e.g., `initial`, `v1`), it remains retrievable. This "
    "is by design: an agent may legitimately need to recall what was "
    "*originally* believed (e.g., 'what was the initial API design "
    "decision?') or compare past and present beliefs. Restricting "
    "retrieval to only the latest revision per Supersedes chain would lose "
    "this temporal query capability [@Park2026Kumiho, Sec. 8.6].",
    title="Superseded != deprecated: superseded revisions remain retrievable via active tags",
)

claim_conflict_presentation = claim(
    "**Conflict presentation: retrieval surfaces both beliefs with "
    "metadata.** When both a current and a superseded belief appear in "
    "retrieval results, the pipeline returns both with their respective "
    "scores. The system does not automatically resolve the conflict; "
    "instead, it provides the agent with temporal metadata (creation "
    "timestamps, revision numbers) that the agent's reasoning layer uses "
    "to apply recency preference. This separation is deliberate: "
    "the retrieval system's role is to surface relevant beliefs; the "
    "agent's role is to reason about which belief to adopt. Incorporating "
    "temporal recency as a third retrieval signal is planned future work "
    "[@Park2026Kumiho, Sec. 8.6].",
    title="Conflict presentation: retrieval returns both beliefs + metadata; agent resolves",
)

# ---------------------------------------------------------------------------
# 8.7: Symbolic <-> sub-symbolic bridge
# ---------------------------------------------------------------------------

setup_symbolic_subsymbolic_division = setting(
    "**Symbolic vs. sub-symbolic division of responsibilities.** The "
    "**graph layer** (Neo4j) is the system of record for belief state: "
    "items, revisions, tags, edges, and deprecation status define the "
    "formal structures $\\mathcal{B}(\\tau)$, $\\tau$, $E$. All belief-"
    "revision operations act on this layer. The **vector layer** "
    "(embeddings stored as revision properties) is a *derived index*: each "
    "revision's embedding is computed from its content after creation and "
    "serves exclusively as a retrieval accelerator "
    "[@Park2026Kumiho, Sec. 8.7].",
    title="Setup: symbolic graph layer = system of record; sub-symbolic vectors = derived index",
)

claim_asymmetric_bridge = claim(
    "**The symbolic/sub-symbolic bridge is deliberately asymmetric.** The "
    "vector/LLM layer **reads from** and **writes through** the graph "
    "layer, but cannot bypass it. From vectors to revision pointers: a "
    "vector similarity query returns the Revision node itself, from which "
    "the system extracts the revision's `kref://` URI; this pointer is "
    "then resolved through the graph layer to obtain content, metadata, "
    "and edge relationships. From LLM outputs to graph operations: LLM "
    "output passes through a structured API boundary that maps it to graph "
    "operations -- a summary becomes a revision's `summary` field, a "
    "deprecation recommendation becomes a contraction operation, a "
    "relationship recommendation becomes an edge in $E$. The LLM never "
    "directly manipulates the graph; it produces structured "
    "recommendations that are validated, filtered by safety guards, and "
    "then executed as formally-defined operations. This asymmetric "
    "design ensures the formal properties of Section 7 are preserved "
    "regardless of embedding/LLM quality [@Park2026Kumiho, Sec. 8.7].",
    title="Asymmetric bridge: sub-symbolic reads/writes via graph layer, never bypassing it",
)

claim_formal_robustness_to_subsymbolic = claim(
    "**Formal guarantees are robust to sub-symbolic component failures.** "
    "A deployment with no embedding infrastructure retains all formal "
    "guarantees (at the cost of reduced retrieval recall); a deployment "
    "with a malfunctioning LLM assessment module is contained by the "
    "Dream State safety guards. The sub-symbolic components enhance the "
    "system's practical utility without entering the formal trust "
    "boundary [@Park2026Kumiho, Sec. 8.7].",
    title="Formal robustness: sub-symbolic failures degrade utility but not formal guarantees",
)

# ---------------------------------------------------------------------------
# 7.6: CWA + classical negation duality
# ---------------------------------------------------------------------------

claim_cwa_classical_negation_duality = claim(
    "**Closed-world (operational) and classical (formal) negation are "
    "separated.** $L_G$ uses **classical negation** for the formal "
    "apparatus (Levi identity, Consistency postulate) and **default "
    "(closed-world) negation** operationally at the retrieval surface: a "
    "ground atom not present in $\\mathcal{B}_{\\mathrm{retr}}(\\tau)$ is "
    "treated as absent. This dual treatment follows the Answer Set "
    "Programming tradition: Gelfond and Lifschitz [@GelfondLifschitz1988] "
    "introduced stable-model semantics with default negation; "
    "[@GelfondLifschitz1991] later introduced classical (strong) negation "
    "alongside default negation, establishing a three-valued epistemic "
    "state ($p$ true, $\\neg p$ true, or $p$ unknown) directly relevant to "
    "cognitive memory. The CWA introduces non-monotonic *operational* "
    "semantics, but the *formal* revision operators are defined over "
    "$\\mathcal{L}_G$ with classical propositional semantics following "
    "Reiter's [@Reiter1978CWA] meta-level / object-level distinction "
    "[@Park2026Kumiho, Sec. 7.6].",
    title="CWA / classical-negation duality: operational CWA for retrieval, classical negation for formal proofs",
)

# ---------------------------------------------------------------------------
# 7.2: Postulate-scope statement
# ---------------------------------------------------------------------------

claim_postulate_scope = claim(
    "**Postulate scope: the formal postulates are proved for the belief "
    "base $\\mathcal{B}(\\tau)$, not for the score-ranked retrieval "
    "surface.** $\\mathcal{B}_{\\mathrm{retr}}(\\tau)$ is a subset of "
    "$\\mathcal{B}(\\tau)$ obtained by filtering on active items; since "
    "deprecation is itself a contraction operation, the retrieval surface "
    "inherits postulate satisfaction. What it does *not* inherit is "
    "**deterministic ranking**: the hybrid scoring pipeline introduces "
    "score-based reranking that may surface different subsets of "
    "$\\mathcal{B}_{\\mathrm{retr}}(\\tau)$ depending on query "
    "formulation. This affects which beliefs an agent encounters in "
    "practice but not the formal properties of the underlying belief base "
    "[@Park2026Kumiho, Sec. 7.2 'Postulate scope'].",
    title="Postulate scope: proved for B(tau); retrieval reranking introduces non-determinism",
)

__all__ = [
    "setup_symbolic_subsymbolic_division",
    "claim_nl_to_triple_boundary",
    "claim_property_graph_not_rdf",
    "claim_nl_mapping_scope_limit",
    "claim_partial_merge_atomic_replacement",
    "claim_partial_merge_finer_atomicity",
    "claim_partial_merge_semantic_future",
    "claim_compound_input_two_strategies",
    "claim_deprecated_filter_architectural",
    "claim_superseded_not_excluded",
    "claim_conflict_presentation",
    "claim_asymmetric_bridge",
    "claim_formal_robustness_to_subsymbolic",
    "claim_cwa_classical_negation_duality",
    "claim_postulate_scope",
]
