"""Section 7 of [@Park2026Kumiho]: Formal properties -- belief revision in
graph-native memory.

This module atomizes the central formal contribution. Each AGM postulate is
extracted as its own `claim`, the formal definitions (memory graph, belief
base, revision, contraction, expansion, two-tier epistemic model, memory
graph logic) are encoded as `setting`s, and the supplementary postulates
(K*7, K*8) and the Recovery rejection are kept as separate claims since the
paper's commitment to each differs.

The Flouris avoidance argument (Section 7.6) is included here because it is
*formally tied* to the postulate satisfaction: the proofs hold only because
$L_G$ is a propositional fragment that satisfies the AGM prerequisites the
DLs do not.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Formal definitions (Section 7.1) as settings
# ---------------------------------------------------------------------------

setup_def_memory_graph = setting(
    "**Definition 7.1 (Memory Graph).** A memory graph is a tuple "
    "$G = (I, R, E, \\tau)$ where: \n"
    "- $I$ is a finite set of **items** (named, typed memory units);\n"
    "- $R = \\bigcup_{i \\in I} R_i$ is the set of all **revisions**, where "
    "$R_i = (r_i^{(1)}, r_i^{(2)}, \\ldots)$ is the ordered append-only revision "
    "sequence for item $i$;\n"
    "- $E \\subseteq R \\times \\mathrm{EdgeType} \\times R$ is a set of typed, "
    "directed edges between revisions;\n"
    "- $\\tau : \\mathrm{TagName} \\rightharpoonup R$ is a partial function "
    "mapping tag names to revisions (the mutable pointer layer).\n\n"
    "Each revision $r_i^{(k)}$ is **immutable**: once created, its content "
    "$\\phi(r_i^{(k)})$ cannot be modified. Tags are the sole mutable "
    "component [@Park2026Kumiho, Def. 7.1].",
    title="Def. 7.1: Memory graph G = (I, R, E, tau) -- immutable revisions, mutable tags",
)

setup_def_belief_base = setting(
    "**Definition 7.2 (Belief Base).** Given a memory graph "
    "$G = (I, R, E, \\tau)$, the belief base is\n\n"
    "$\\mathcal{B}(\\tau) = \\bigcup_{t \\in \\mathrm{dom}(\\tau)} "
    "\\phi(\\tau(t))$\n\n"
    "where $\\phi(r)$ denotes the propositional content of revision $r$ "
    "(operationally, the revision's structured metadata: summary, topics, "
    "keywords, extracted facts). Unlike the AGM belief set, "
    "$\\mathcal{B}(\\tau)$ is a finite set that is **not** closed under "
    "logical consequence. The system also records every tag assignment, "
    "yielding a history function $\\tau_T$ that resolves the tag mapping as "
    "of time $T$, and induces historical belief bases "
    "$\\mathcal{B}(\\tau_T) = \\bigcup_{t \\in \\mathrm{dom}(\\tau_T)} "
    "\\phi(\\tau_T(t))$, supporting point-in-time queries "
    "[@Park2026Kumiho, Def. 7.2].",
    title="Def. 7.2: Belief base B(tau) = union of tagged-revision content (Hansson level)",
)

setup_def_two_tier = setting(
    "**Definition 7.3 (Two-Tier Epistemic Model).** The full graph "
    "$G = (I, R, E, \\tau)$ contains all revisions ever created, including "
    "deprecated items and archived (untagged) revisions; this is the "
    "**operator-accessible store**. The **agent retrieval surface** "
    "$\\mathcal{B}_{\\mathrm{retr}}(\\tau)$ is the subset reachable through "
    "the retrieval pipeline: a revision $r$ is in the retrieval surface iff "
    "(i) $r$ is referenced by at least one active tag in $\\tau$, AND "
    "(ii) the item containing $r$ is not marked as deprecated. Letting "
    "$I_{\\mathrm{active}} = \\{i \\in I \\mid \\neg \\mathrm{deprecated}(i)\\}$, "
    "$\\mathcal{B}_{\\mathrm{retr}}(\\tau) = "
    "\\bigcup_{t \\in \\mathrm{dom}(\\tau),\\, \\mathrm{item}(\\tau(t)) \\in "
    "I_{\\mathrm{active}}} \\phi(\\tau(t)) \\subseteq \\mathcal{B}(\\tau)$. "
    "Both retrieval branches (fulltext and vector) filter on active status "
    "before scoring via a mandatory `WHERE NOT item.deprecated` clause "
    "[@Park2026Kumiho, Def. 7.3].",
    title="Def. 7.3: Two-tier epistemic model (operator full graph vs. agent retrieval surface)",
)

setup_def_revision_op = setting(
    "**Definition 7.4 (Graph-Native Revision).** Given belief base "
    "$\\mathcal{B}(\\tau)$ and input proposition $A$, the revision operation "
    "$\\mathcal{B} \\ast A$ is implemented as: (1) create a new revision "
    "$r_i^{(k+1)}$ with content $\\phi(r_i^{(k+1)}) = A$; (2) add edge "
    "$(r_i^{(k+1)}, \\mathrm{Supersedes}, r_i^{(k)})$ to $E$; (3) update the "
    "tag $\\tau' = \\tau[t_{\\mathrm{current}} \\mapsto r_i^{(k+1)}]$. The "
    "prior revision $r_i^{(k)}$ remains in $R$ but is no longer tag-"
    "referenced, hence excluded from $\\mathcal{B}(\\tau')$ "
    "[@Park2026Kumiho, Def. 7.4].",
    title="Def. 7.4: Revision = new revision + Supersedes edge + tag re-pointing",
)

setup_def_contraction_op = setting(
    "**Definition 7.5 (Graph-Native Contraction).** Contraction "
    "$\\mathcal{B} \\div A$ is implemented through two complementary "
    "mechanisms: (1) **tag removal** -- remove from $\\tau$ any tag $t$ such "
    "that $A$ appears in $\\phi(\\tau(t))$, yielding $\\tau' = \\tau "
    "\\setminus \\{t \\mid A \\in \\phi(\\tau(t))\\}$; (2) **soft "
    "deprecation** -- mark item $i$ as deprecated; deprecated items are "
    "**excluded from all search and retrieval operations by default**, but "
    "the items remain in the graph and can be recovered via an explicit "
    "opt-in flag (`include_deprecated=true`). The contraction is thus "
    "*behaviorally complete* (the belief vanishes from the agent's retrieval "
    "surface) while remaining *structurally reversible* (the graph retains "
    "the full record) [@Park2026Kumiho, Def. 7.5].",
    title="Def. 7.5: Contraction = tag removal + soft deprecation (behaviorally complete, structurally reversible)",
)

setup_def_selection_function = setting(
    "**Definition 7.6 (Selection Function).** Given $A$ and base "
    "$\\mathcal{B}(\\tau)$, the contraction target set is "
    "$\\mathrm{Targets}(A, \\tau) = \\{(t, r) \\mid t \\in \\mathrm{dom}(\\tau), "
    "r = \\tau(t), A \\in \\phi(r)\\}$. Contraction removes all such tags. "
    "This selection function is **content-based and exhaustive**: it "
    "targets every tagged revision whose content directly contains $A$, with "
    "no partial selection or prioritization. This is the simplest selection "
    "function consistent with the Relevance postulate; it is deterministic "
    "and computable in $O(|\\mathrm{dom}(\\tau)|)$ "
    "[@Park2026Kumiho, Def. 7.6].",
    title="Def. 7.6: Selection function = content-based, exhaustive (deterministic O(|dom(tau)|))",
)

setup_def_expansion_op = setting(
    "**Definition 7.7 (Graph-Native Expansion).** Expansion "
    "$\\mathcal{B} + A$ creates a new revision $r_i^{(k+1)}$ with "
    "$\\phi(r_i^{(k+1)}) = \\phi(r_i^{(k)}) \\cup \\{A\\}$ and assigns a tag "
    "to it, without removing any existing tag assignments. The resulting "
    "belief state is $\\mathcal{B}(\\tau') = \\mathcal{B}(\\tau) \\cup \\{A\\}$ "
    "[@Park2026Kumiho, Def. 7.7].",
    title="Def. 7.7: Expansion = new revision with content union + tag assignment (no removal)",
)

setup_def_lg_logic = setting(
    "**Definition 7.8 (Memory Graph Logic).** The logic "
    "$L_G = (\\mathcal{L}_G, \\mathrm{Cn}_G)$ has: \n"
    "- **Atoms** $\\mathrm{At}_G$: ground triples "
    "$\\langle \\mathrm{item}, \\mathrm{predicate}, \\mathrm{value} \\rangle$ "
    "where item is a memory-reference URI, predicate is one of a fixed set "
    "(summary, topic, keyword, type, tag, edge-type), and value is a string "
    "literal.\n"
    "- **Full language** $\\mathcal{L}_G$: closure of $\\mathrm{At}_G$ "
    "under the standard propositional connectives $\\{\\neg, \\wedge, \\vee, "
    "\\rightarrow\\}$. Compound formulae such as "
    "$\\langle i_1, p_1, v_1 \\rangle \\wedge \\langle i_2, p_2, v_2 \\rangle$ "
    "and $\\neg \\langle i, p, v \\rangle$ are well-formed.\n"
    "- **Belief base vs. full language**: while $\\mathcal{L}_G$ contains "
    "compound formulae, the belief base $\\mathcal{B}(\\tau)$ is always a "
    "finite set of ground atoms drawn from $\\mathrm{At}_G$ (Hansson level), "
    "**not** deductively closed.\n"
    "- **Consequence** $\\mathrm{Cn}_G$: classical propositional closure over "
    "$\\mathcal{L}_G$. No consequence beyond propositional entailment "
    "operates on the graph: no transitive closure of edges, no schema-level "
    "entailment, no rule-based inference.\n"
    "- **Graph traversal isolation**: traversal operations (TraverseEdges, "
    "AnalyzeImpact, ShortestPath) compute structural reachability over $E$ "
    "but their outputs **never enter** $\\mathcal{B}(\\tau)$. The belief "
    "base changes only through three explicit write operations: expansion, "
    "contraction, revision [@Park2026Kumiho, Def. 7.8].",
    title="Def. 7.8: L_G = propositional logic over ground triples; traversal isolated from belief base",
)

setup_satisfaction_system = setting(
    "**Satisfaction system.** Following Aiguier et al. [@Aiguier2018], the "
    "satisfaction triple $(\\mathcal{L}_G, \\mathcal{M}_G, \\models_G)$ "
    "instantiates: $\\mathcal{L}_G$ is the propositional language above, "
    "$\\mathcal{M}_G$ is the set of all truth assignments over "
    "$\\mathrm{At}_G$, and $\\models_G$ is classical propositional "
    "satisfaction. This triple inherits the properties of classical "
    "propositional logic, establishing $L_G$ as a well-defined satisfaction "
    "system [@Park2026Kumiho, Sec. 7.6].",
    title="Setup: satisfaction system (L_G, M_G, |=_G) inherits classical propositional properties",
)

# ---------------------------------------------------------------------------
# 7.6: AGM prerequisites for L_G + Flouris avoidance
# ---------------------------------------------------------------------------

claim_lg_satisfies_agm_prereqs = claim(
    "**Proposition 7.10 ($L_G$ satisfies AGM prerequisites).** The memory "
    "graph logic $L_G$ satisfies inclusion ($A \\subseteq \\mathrm{Cn}(A)$), "
    "monotonicity ($A \\subseteq B \\Rightarrow \\mathrm{Cn}(A) \\subseteq "
    "\\mathrm{Cn}(B)$), idempotence ($\\mathrm{Cn}(\\mathrm{Cn}(A)) = "
    "\\mathrm{Cn}(A)$), the deduction theorem, and compactness "
    "[@Gardenfors1988]. Proof: $L_G$ is a fragment of classical "
    "propositional logic (ground atoms with standard connectives); classical "
    "propositional logic is the canonical Tarskian logic satisfying all "
    "five properties; the deduction theorem holds because $\\mathcal{L}_G$ "
    "includes $\\rightarrow$; compactness holds because propositional logic "
    "is compact [@Park2026Kumiho, Prop. 7.10].",
    title="Prop. 7.10: L_G satisfies inclusion, monotonicity, idempotence, deduction theorem, compactness",
)

claim_flouris_avoidance = claim(
    "**Formal avoidance of the Flouris impossibility.** Flouris et al. "
    "[@Flouris2005DL] proved that DLs (including those underlying OWL) "
    "cannot satisfy AGM. The key structural differences that cause the "
    "Flouris impossibility to fail for $L_G$: (i) **no TBox/ABox "
    "separation** -- DL maintains intensional and extensional layers whose "
    "interactions create non-monotonic revision pathologies; $L_G$ has a "
    "single flat layer. (ii) **closed-world operational semantics** -- "
    "DL's open-world assumption complicates Inclusion; $L_G$ provides "
    "explicit formal negation while using closed-world semantics at the "
    "operational level. (iii) **no complex constructors** -- DL "
    "constructors (disjunction, existential quantification, role inverses, "
    "number restrictions) create closure obligations conflicting with AGM's "
    "minimality requirements [@Flouris2005DL]; $L_G$'s edge types are "
    "simple labeled directed relationships with propositional, not "
    "concept-constructive, closure. Combined with Prop. 7.10, $L_G$ meets "
    "the Flouris et al. necessary conditions for AGM-compliance "
    "[@Park2026Kumiho, Sec. 7.6].",
    title="Flouris avoidance: L_G avoids DL-style impossibility via no TBox/ABox, simple connectives",
)

claim_expressiveness_tradeoff = claim(
    "**The expressiveness trade-off is deliberate.** The formal results hold "
    "precisely because $L_G$ is a **weak logic**. A logic where every ground "
    "triple is an independent propositional atom has essentially no "
    "inferential structure -- logical equivalence reduces to syntactic "
    "identity (Prop. 7.5), and the Flouris impossibility is avoided because "
    "$L_G$ lacks the complex constructors that cause DLs to fail. The "
    "contribution is not 'AGM holds over a strong logic' but **the bridge**: "
    "showing that the specific architectural choices made independently for "
    "production reasons (immutable revisions, mutable tag pointers, typed "
    "edges) happen to satisfy formal rationality postulates studied for "
    "four decades. $L_G$ explicitly *cannot* express subsumption "
    "hierarchies, role composition, disjointness axioms, or cardinality "
    "constraints; any strengthening would re-encounter Flouris-type problems "
    "[@Park2026Kumiho, Sec. 7.6 'Expressiveness trade-off'].",
    title="Trade-off: L_G is weak by design; richer logics would re-encounter Flouris",
)

# ---------------------------------------------------------------------------
# 7.2: AGM postulate satisfaction (atomized) -- the central formal claims
# ---------------------------------------------------------------------------

claim_k2_success = claim(
    "**Proposition 7.1 ($K^\\ast 2$ Success): $A \\in \\mathcal{B} \\ast A$.** "
    "By Definition 7.4, the new revision $r_i^{(k+1)}$ satisfies "
    "$A \\in \\phi(r_i^{(k+1)})$, and the tag $t_{\\mathrm{current}}$ points "
    "to it. Therefore "
    "$A \\in \\bigcup_t \\phi(\\tau'(t)) = \\mathcal{B}(\\tau')$ "
    "[@Park2026Kumiho, Prop. 7.1].",
    title="K*2 Success: A in (B * A) -- new revision contains A, tag updated",
)

claim_k3_inclusion_base_version = claim(
    "**Proposition 7.2 ($K^\\ast 3$ Inclusion, belief-base version): "
    "$\\mathcal{B} \\ast A \\subseteq \\mathcal{B}(\\tau) \\cup \\{A\\}$.** "
    "This is the belief-*base* version of Inclusion [@Hansson1999Textbook], "
    "**not** the belief-set version ($K \\ast A \\subseteq \\mathrm{Cn}(K "
    "\\cup \\{A\\})$). The base version requires that no new atomic beliefs "
    "are introduced beyond $A$ and the surviving prior beliefs. By "
    "Definition 7.4, the revision operation creates a new revision "
    "containing $A$ and may redirect tags, removing some prior beliefs from "
    "$\\mathcal{B}(\\tau)$. No mechanism introduces atoms not already in "
    "$\\mathcal{B}(\\tau) \\cup \\{A\\}$, so base-level inclusion holds "
    "[@Park2026Kumiho, Prop. 7.2].",
    title="K*3 Inclusion: B * A subseteq B union {A} (base-level version)",
)

claim_k4_vacuity = claim(
    "**Proposition 7.3 ($K^\\ast 4$ Vacuity): if $A$ is consistent with "
    "$\\mathcal{B}(\\tau)$, then $\\mathcal{B}(\\tau) \\cup \\{A\\} "
    "\\subseteq \\mathcal{B} \\ast A$.** If $A$ introduces no contradiction, "
    "the revision operation has no conflicting belief to retract; no tag "
    "needs redirection. The prior content is preserved, augmented with $A$ "
    "[@Park2026Kumiho, Prop. 7.3].",
    title="K*4 Vacuity: no conflict => no retraction, prior content preserved + A",
)

claim_k5_consistency = claim(
    "**Proposition 7.4 ($K^\\ast 5$ Consistency): if $A$ is consistent, "
    "then $\\mathcal{B} \\ast A$ is consistent.** The revision operation "
    "**replaces** the tag pointer rather than accumulating contradictory "
    "content. The prior revision (which may have contained content "
    "inconsistent with $A$) is excluded from $\\mathcal{B}(\\tau')$ via the "
    "two-tier epistemic model (Definition 7.3). For atomic revision inputs "
    "($A \\in \\mathrm{At}_G$), distinct ground atoms are logically "
    "independent under propositional semantics ($\\neg \\langle s_1, p_1, "
    "o_1 \\rangle$ is not entailed by $\\langle s_2, p_2, o_2 \\rangle$ for "
    "any distinct atoms); therefore consistency is structurally guaranteed "
    "[@Park2026Kumiho, Prop. 7.4].",
    title="K*5 Consistency: Supersedes replaces (does not accumulate) -- inherits A's consistency",
)

claim_k6_extensionality = claim(
    "**Proposition 7.5 ($K^\\ast 6$ Extensionality): if "
    "$\\mathrm{Cn}_G(\\{A\\}) = \\mathrm{Cn}_G(\\{B\\})$, then "
    "$\\mathcal{B} \\ast A = \\mathcal{B} \\ast B$.** Since the belief base "
    "$\\mathcal{B}(\\tau)$ consists of ground atoms from $\\mathrm{At}_G$ "
    "(Definition 7.8), and ground atoms are logically independent, two atoms "
    "$\\alpha, \\beta \\in \\mathrm{At}_G$ satisfy $\\mathrm{Cn}_G(\\{\\alpha\\}) = "
    "\\mathrm{Cn}_G(\\{\\beta\\})$ iff $\\alpha = \\beta$ (syntactic "
    "identity). Thus, for atomic revision inputs -- the normal case -- "
    "logical equivalence reduces to syntactic identity, and item-level "
    "identity checking is an *exact* implementation, not an approximation "
    "[@Park2026Kumiho, Prop. 7.5].",
    title="K*6 Extensionality: for ground atoms, logical equivalence = syntactic identity",
)

claim_relevance_hansson = claim(
    "**Proposition 7.6 (Relevance, Hansson): if $B \\in \\mathcal{B}(\\tau) "
    "\\setminus (\\mathcal{B} \\div A)$, then $A \\in \\mathrm{Cn}(B' \\cup "
    "\\{B\\})$ for some $B' \\subseteq \\mathcal{B}(\\tau)$ with $A \\notin "
    "\\mathrm{Cn}(B')$.** Contraction (Definition 7.5) removes from "
    "$\\mathcal{B}(\\tau)$ exactly those beliefs residing in revisions whose "
    "content contains $A$ (Definition 7.6). Witnesses: Case 1 ($B = A$): "
    "let $B' = \\emptyset$; then $A \\notin \\mathrm{Cn}(\\emptyset)$ "
    "(since $A$ is contingent), and $A \\in \\mathrm{Cn}(\\{B\\})$. Case 2 "
    "($B \\neq A$ but $B$ co-occurs with $A$ in $\\phi(r)$): let $B' = "
    "\\mathcal{B}(\\tau) \\setminus \\phi(r)$; since $A \\in \\phi(r)$ and "
    "$\\phi(r)$ was the only source of $A$ targeted by content-based "
    "selection, $A \\notin \\mathrm{Cn}(B')$. Relevance holds: every "
    "removed belief's removal is connected to the contracted belief "
    "[@Park2026Kumiho, Prop. 7.6].",
    title="Relevance (Hansson): tag removal targets only revisions containing A",
)

claim_core_retainment_hansson = claim(
    "**Proposition 7.7 (Core-Retainment, Hansson): if $B \\in "
    "\\mathcal{B}(\\tau) \\setminus (\\mathcal{B} \\div A)$, then there "
    "exists $B' \\subseteq \\mathcal{B}(\\tau)$ such that $A \\notin "
    "\\mathrm{Cn}(B')$ but $A \\in \\mathrm{Cn}(B' \\cup \\{B\\})$.** Let "
    "$B \\in \\mathcal{B}(\\tau) \\setminus (\\mathcal{B} \\div A)$; by "
    "Definition 7.6, $B$ resided in a revision $r$ with $A \\in \\phi(r)$. "
    "Witnesses constructed as in Prop. 7.6. The structural co-occurrence is "
    "what makes $B$'s removal attributable to the contraction of $A$, "
    "satisfying Core-Retainment's requirement that every removed belief is "
    "connected to the contracted belief's derivation. Note: Relevance and "
    "Core-Retainment are postulates for **belief bases**, not belief sets; "
    "for deductively closed sets, Core-Retainment implies Recovery, but this "
    "implication does not hold for belief bases, so simultaneous "
    "satisfaction of Core-Retainment and rejection of Recovery creates no "
    "logical inconsistency [@Park2026Kumiho, Prop. 7.7].",
    title="Core-Retainment (Hansson): every removed belief contributed to deriving A",
)

# ---------------------------------------------------------------------------
# Postulate-satisfaction summary table (Table 4)
# ---------------------------------------------------------------------------

claim_table4_postulate_summary = claim(
    "**Postulate satisfaction summary (Table 4 of [@Park2026Kumiho]).**\n\n"
    "| Postulate | System Mechanism | Status |\n"
    "|-----------|------------------|--------|\n"
    "| $K^\\ast 2$ Success | New revision contains $A$; tag updated | check |\n"
    "| $K^\\ast 3$ Inclusion | Base-level: $\\mathcal{B} \\ast A \\subseteq \\mathcal{B} \\cup \\{A\\}$ | check |\n"
    "| $K^\\ast 4$ Vacuity | No conflict => no retraction needed | check |\n"
    "| $K^\\ast 5$ Consistency | Supersedes replaces, not accumulates | check |\n"
    "| $K^\\ast 6$ Extensionality | Syntactic = logical equiv. for ground atoms | check |\n"
    "| Relevance (Hansson) | Tag removal targets relevant revisions | check |\n"
    "| Core-Retainment (Hansson) | Removed beliefs contributed to contracted belief | check |\n"
    "| $K^\\ast 7$ Superexpansion | Conjunction revision $\\subseteq$ sequential | check (argued only) |\n"
    "| $K^\\ast 8$ Subexpansion | Consistent expansion = conjunction revision | check (argued only) |\n"
    "| Recovery (AGM) | Immutable revisions; archive != erase | x (intentional) |\n",
    title="Table 4: 7 postulates proved + K*7/K*8 argued-only + Recovery rejected",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 4",
        "caption": "Postulate satisfaction in the graph-native architecture (Hansson belief base).",
    },
)

# ---------------------------------------------------------------------------
# 7.2 supplementary: K*7 and K*8 (argued, not formally established)
# ---------------------------------------------------------------------------

claim_k7_superexpansion_argued = claim(
    "**Proposition 7.8 ($K^\\ast 7$ Superexpansion, argued): "
    "$\\mathcal{B} \\ast (A \\wedge B) \\subseteq (\\mathcal{B} \\ast A) + B$.** "
    "Conjunction is well-formed in $\\mathcal{L}_G$, so $A \\wedge B$ is a "
    "valid revision input. Revising by $(A \\wedge B)$ creates a single "
    "revision whose content entails both $A$ and $B$. The right-hand side "
    "first revises by $A$ (possibly retracting beliefs inconsistent with "
    "$A$) and then expands by $B$ (adding $B$ without retraction). Since "
    "expansion is monotone, $(\\mathcal{B} \\ast A) + B \\supseteq "
    "\\mathcal{B} \\ast A$ and contains both $A$ and $B$. The conjunction "
    "revision cannot contain more, as it may also retract beliefs inconsistent "
    "with $A \\wedge B$ [@Park2026Kumiho, Prop. 7.8].",
    title="K*7 Superexpansion (argued): conjunction revision subseteq sequential revise-then-expand",
)

claim_k8_subexpansion_argued = claim(
    "**Proposition 7.9 ($K^\\ast 8$ Subexpansion, argued): if $\\neg B "
    "\\notin \\mathrm{Cn}_G(\\mathcal{B} \\ast A)$, then $(\\mathcal{B} \\ast "
    "A) + B \\subseteq \\mathcal{B} \\ast (A \\wedge B)$.** If $B$ is "
    "consistent with the $A$-revised state, expanding by $B$ adds no "
    "information beyond $B$ itself and its consequences. Revising by $A "
    "\\wedge B$ directly incorporates both conjuncts, performing any "
    "necessary retractions in a single step. Since $B$ causes no conflict "
    "in the $A$-revised state, both paths yield the same retractions and "
    "the same final content [@Park2026Kumiho, Prop. 7.9].",
    title="K*8 Subexpansion (argued): if B consistent with B*A, then (B*A)+B subseteq B*(A wedge B)",
)

claim_k7k8_representation_gap = claim(
    "**Representation-theoretic gap for $K^\\ast 7$/$K^\\ast 8$.** The AGM "
    "representation theorem [@Grove1988] establishes that a revision "
    "operator satisfies all eight postulates iff it can be represented as a "
    "**transitively relational partial meet contraction** -- equivalently, "
    "via a total preorder on possible worlds or an epistemic entrenchment "
    "ordering [@Gardenfors1988]. The arguments above show that the "
    "graph-native operator produces results *consistent with* $K^\\ast 7$/"
    "$K^\\ast 8$ but this falls short of a formal proof via representation. "
    "Formally establishing $K^\\ast 7$/$K^\\ast 8$ requires either (a) "
    "explicit construction of an entrenchment ordering over graph triples "
    "and proof that contraction respects it, or (b) proof that the system's "
    "tag-based operations are equivalent to a transitively relational "
    "selection function. Neither is provided. Multiple candidate orderings "
    "exist (temporal recency, structural centrality, confidence scores) but "
    "none is canonical; a *type-dependent* entrenchment function (recency "
    "for preferences, evidential support for facts, confidence for inferred "
    "beliefs) is conjectured but not proved [@Park2026Kumiho, Sec. 7.2 "
    "'Representation-theoretic status'].",
    title="K*7/K*8 representation gap: no explicit entrenchment ordering constructed",
)

# ---------------------------------------------------------------------------
# 7.3: Intentional divergence -- the Recovery postulate
# ---------------------------------------------------------------------------

claim_recovery_violation = claim(
    "**The Recovery postulate $K \\subseteq (K \\div A) + A$ is "
    "intentionally violated.** Consider an item with revision $r_i^{(k)}$ "
    "carrying content $\\phi(r_i^{(k)}) = \\{A, B, C\\}$. Contracting $A$ "
    "via tag removal produces $\\mathcal{B}(\\tau') = \\mathcal{B}(\\tau) "
    "\\setminus \\phi(r_i^{(k)})$. Re-expanding by $A$ creates a *new* "
    "revision $r_i^{(k+1)}$ with $\\phi(r_i^{(k+1)}) = \\{A\\}$. The "
    "beliefs $B, C$ -- which were co-located with $A$ in the original "
    "revision -- are **not** automatically recovered, because the new "
    "revision is constructed from input $A$ alone: $(\\mathcal{B} \\div A) "
    "+ A = \\mathcal{B}(\\tau) \\setminus \\phi(r_i^{(k)}) \\cup \\{A\\} "
    "\\not\\supseteq \\{B, C\\}$ [@Park2026Kumiho, Sec. 7.3].",
    title="Recovery violation: re-expansion is fresh incorporation of A, not rollback to {A,B,C}",
)

claim_recovery_rejection_principled = claim(
    "**The rejection of Recovery is principled, grounded in immutable "
    "versioning.** In a system where contraction *erases* content, Recovery "
    "demands the erased content be reconstructable from what remains plus "
    "the re-added belief. But in a provenance-preserving system, contraction "
    "does not erase -- it archives. The original revision $r_i^{(k)}$, with "
    "its full content, metadata, and edge relationships, remains in the "
    "graph as a historical record. The time-indexed tag history "
    "(Equation 2) means an agent can reconstruct the **exact** belief state "
    "that held before contraction by querying $\\mathcal{B}(\\tau_T)$ for "
    "any prior time $T$. The system simply does not automatically resurrect "
    "archived content by re-adding a single belief. This aligns with "
    "Makinson [@Makinson1987Recovery], Hansson [@Hansson1991NoRecovery], "
    "and Fuhrmann [@Fuhrmann1991], who all argued Recovery imposes "
    "unreasonable constraints when beliefs have non-trivial internal "
    "structure or provenance. In Hansson's belief-base framework, "
    "Recovery is not a postulate; it is replaced by Relevance + "
    "Core-Retainment, which the system satisfies "
    "[@Park2026Kumiho, Sec. 7.3].",
    title="Recovery rejection: immutable versioning provides explicit rollback, not implicit reconstruction",
)

# ---------------------------------------------------------------------------
# 7.4: Levi and Harper identities
# ---------------------------------------------------------------------------

claim_levi_identity = claim(
    "**Levi Identity: $K \\ast A = (K \\div \\neg A) + A$.** Revision can "
    "be decomposed into contraction of the negation followed by expansion. "
    "In the graph-native model, this holds when contraction deterministically "
    "selects which tag-referenced revisions to de-reference: contracting "
    "$\\neg A$ removes revisions whose content entails $\\neg A$, and the "
    "subsequent expansion by $A$ adds a fresh revision. The two-step "
    "process yields the same belief state as direct revision, provided the "
    "contraction selection function is deterministic -- which it is, since "
    "tag removal targets specific revisions identifiable by their content "
    "[@Park2026Kumiho, Sec. 7.4].",
    title="Levi Identity: K * A = (K div ~A) + A holds for deterministic content-based selection",
)

claim_harper_identity = claim(
    "**Harper Identity: $K \\div A = K \\cap (K \\ast \\neg A)$.** Any "
    "belief $B \\in K$ that survives contraction of $A$ must be consistent "
    "with $\\neg A$, and any such $B$ is preserved in $K \\ast \\neg A$. "
    "The graph intersection corresponds to the set of revisions that remain "
    "tag-referenced in both $\\tau$ (original) and $\\tau'$ (after revision "
    "by $\\neg A$) [@Park2026Kumiho, Sec. 7.4].",
    title="Harper Identity: K div A = K cap (K * ~A) holds via tag-intersection",
)

claim_iterated_revision_supersedes = claim(
    "**Iterated revision via Supersedes-chain epistemic ordering.** The "
    "$\\mathrm{Supersedes}$ edge chain $r_i^{(1)} \\leftarrow r_i^{(2)} "
    "\\leftarrow \\cdots \\leftarrow r_i^{(k)}$ provides a natural epistemic "
    "ordering over belief states, corresponding to the framework of Darwiche "
    "and Pearl [@DarwichePearl1997] for iterated belief revision. The "
    "time-indexed tag function $\\tau_T$ elevates this from structural "
    "record-keeping to a fully queryable epistemic history: querying "
    "$\\tau_T(\\mathrm{decided})$ returns the specific revision that carried "
    "the `decided` tag at time $T$, even if that tag has since been moved "
    "or removed. This supports both forward analysis and point-in-time "
    "reconstruction, providing the complete temporal audit trail that "
    "Darwiche-Pearl assumes but rarely sees implemented "
    "[@Park2026Kumiho, Sec. 7.4].",
    title="Iterated revision: Supersedes-chain + tau_T provides Darwiche-Pearl ordering",
)

# ---------------------------------------------------------------------------
# 7.7: Computational complexity
# ---------------------------------------------------------------------------

claim_complexity_bounds = claim(
    "**Computational complexity of the formal operations.** Revision "
    "(Definition 7.4) requires a bounded number of graph operations: one "
    "node creation, one edge creation (Supersedes), one tag reassignment -- "
    "effectively constant in practice (tag uniqueness invariant ensures "
    "$k=1$). Contraction (Definition 7.5) requires identifying tag-"
    "referenced revisions whose content contains the contracted belief and "
    "removing/deprecating those tags -- $O(|\\mathrm{dom}(\\tau)|)$ in the "
    "number of active tags ($<100$ for typical deployments). Expansion "
    "(Definition 7.7) is $O(1)$. Computing $\\mathcal{B}(\\tau)$ requires "
    "collecting content from all tag-referenced revisions -- "
    "$O(|\\mathrm{dom}(\\tau)|)$. Graph traversal for provenance and impact "
    "analysis is bounded by BFS to a configurable depth limit $d$ "
    "(default $d=10$), yielding worst-case $O(b^d)$ for branching factor "
    "$b$; in deployed systems with typical memory graphs ($b \\approx 3$-5), "
    "traversals complete in under 100ms [@Park2026Kumiho, Sec. 7.7].",
    title="Complexity: revision/expansion O(1), contraction O(|dom(tau)|), traversal O(b^d) bounded",
)

# ---------------------------------------------------------------------------
# 7.5: Worked example -- belief revision through preference update
# ---------------------------------------------------------------------------

claim_worked_example_preference = claim(
    "**Worked example: belief revision via preference update.** Initial "
    "state: item $i_1 = \\texttt{color-pref.decision}$ with revision $r_1^{(1)}$ "
    "carrying $\\phi(r_1^{(1)}) = \\{\\langle \\texttt{color-pref}, "
    "\\texttt{summary}, \\text{warm tones} \\rangle\\}$, tagged "
    "$t_{\\mathrm{current}} \\mapsto r_1^{(1)}$; item $i_2 = "
    "\\texttt{palette.decision}$ with $r_2^{(1)}$ tagged similarly; edge "
    "$(r_2^{(1)}, \\mathrm{Depends\\_On}, r_1^{(1)})$. The user states "
    "'Actually, I prefer cool tones now.' The agent invokes revision with "
    "$A = \\langle \\texttt{color-pref}, \\texttt{summary}, \\text{cool "
    "tones} \\rangle$: (1) creates $r_1^{(2)}$ with $\\phi(r_1^{(2)}) = "
    "\\{A\\}$; (2) adds Supersedes edge; (3) updates tag. The new belief "
    "base is $\\mathcal{B}(\\tau') = \\phi(r_1^{(2)}) \\cup \\phi(r_2^{(1)}) "
    "= \\{A\\} \\cup \\phi(r_2^{(1)})$. AnalyzeImpact($r_1^{(2)}, d=2$) "
    "traverses incoming Depends_On edges and surfaces $\\{r_2^{(1)}\\}$ as "
    "a downstream dependent requiring potential re-evaluation. Postulate "
    "verification: Success ($A \\in \\mathcal{B}(\\tau')$ check), "
    "Consistency (no contradictory content check), Inclusion (no new atoms "
    "check). Provenance queries supported: current belief, historical "
    "belief via $\\tau_T$, belief evolution via Supersedes chain, rollback "
    "via tag reassignment [@Park2026Kumiho, Sec. 7.5].",
    title="Worked example: cool-tones revision step-by-step exercises K*2/K*3/K*5 + AnalyzeImpact",
)

__all__ = [
    "setup_def_memory_graph",
    "setup_def_belief_base",
    "setup_def_two_tier",
    "setup_def_revision_op",
    "setup_def_contraction_op",
    "setup_def_selection_function",
    "setup_def_expansion_op",
    "setup_def_lg_logic",
    "setup_satisfaction_system",
    "claim_lg_satisfies_agm_prereqs",
    "claim_flouris_avoidance",
    "claim_expressiveness_tradeoff",
    "claim_k2_success",
    "claim_k3_inclusion_base_version",
    "claim_k4_vacuity",
    "claim_k5_consistency",
    "claim_k6_extensionality",
    "claim_relevance_hansson",
    "claim_core_retainment_hansson",
    "claim_table4_postulate_summary",
    "claim_k7_superexpansion_argued",
    "claim_k8_subexpansion_argued",
    "claim_k7k8_representation_gap",
    "claim_recovery_violation",
    "claim_recovery_rejection_principled",
    "claim_levi_identity",
    "claim_harper_identity",
    "claim_iterated_revision_supersedes",
    "claim_complexity_bounds",
    "claim_worked_example_preference",
]
