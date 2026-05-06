"""Section 16 (Future Directions) and Section 17 (Conclusion) of
[@Park2026Kumiho]. The future directions are kept here because they
characterize where the formal and architectural commitments need extension;
the conclusion synthesizes the contributions.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 16.1: Evaluation roadmap
# ---------------------------------------------------------------------------

claim_future_goal_aware_indexing = claim(
    "**Future direction: goal-aware prospective indexing.** The 85% "
    "accuracy on goal-type questions (abstract intention inference) "
    "motivates investigation of goal-aware prospective indexing -- "
    "specifically generating implications for stated goals and intentions, "
    "not just events, to create better semantic bridges for the most "
    "abstract constraint type [@Park2026Kumiho, Sec. 16.1].",
    title="Future: goal-aware prospective indexing for the hardest constraint type",
)

claim_future_chronological_ordering = claim(
    "**Future direction: chronological context ordering.** Currently, "
    "recalled memories are presented to the answer model in "
    "relevance-score order; sorting by chronological order may help the "
    "model reason about temporal progressions, particularly for goal-type "
    "constraints where the narrative arc matters "
    "[@Park2026Kumiho, Sec. 16.1].",
    title="Future: chronological context ordering for narrative-arc reasoning",
)

claim_future_ablation_study = claim(
    "**Future direction: enrichment ablation study.** Four configurations "
    "on the same 401-entry benchmark: (i) summary only, (ii) summary + "
    "event extraction, (iii) summary + prospective indexing, (iv) full "
    "system. The hypothesis: events (preserve factual anchors) and "
    "implications (provide semantic bridges) are complementary; neither "
    "alone is sufficient for the highest accuracy. Pre-enrichment "
    "baseline: 61.6% on $n=200$; full system: 93.3% on $n=401$ "
    "[@Park2026Kumiho, Sec. 15.3 ablation note; Sec. 16.1].",
    title="Future: ablation isolating event extraction vs. prospective indexing contributions",
)

claim_future_controlled_cross_system = claim(
    "**Future direction: controlled cross-system comparison.** "
    "Re-evaluating competitor systems (Graphiti, Mem0, Hindsight) on "
    "identical infrastructure and LLM configurations to isolate "
    "architectural contributions from confounds in the LoCoMo results. "
    "The token-level F1 results (Sec. 15.2) partially address this by "
    "enabling metric-comparable evaluation against systems that also "
    "report F1 [@Park2026Kumiho, Sec. 16.1].",
    title="Future: controlled cross-system re-evaluation on identical LLM/infrastructure",
)

claim_future_retrieval_ablation = claim(
    "**Future direction: retrieval-pipeline sensitivity analysis.** "
    "Isolating each retrieval branch's contribution; sensitivity analysis "
    "for $\\beta \\in [0.5, 1.0]$, type weights, and comparison against "
    "RRF [@Cormack2009RRF] and convex combination [@Bruch2023Fusion] on "
    "the same retrieval tasks; circuit breaker threshold analysis "
    "(10% to 90%) on synthetic graphs with ground-truth relevance "
    "labels [@Park2026Kumiho, Sec. 8.2; Sec. 16.1].",
    title="Future: sensitivity analysis on beta, type weights, fusion methods (vs. RRF, convex combination)",
)

# ---------------------------------------------------------------------------
# 16.2: Formal extensions
# ---------------------------------------------------------------------------

claim_future_entrenchment_k7k8 = claim(
    "**Future direction: entrenchment ordering for $K^\\ast 7$/$K^\\ast 8$.** "
    "Constructing an explicit epistemic entrenchment ordering over graph "
    "triples, or proving that tag-based contraction is equivalent to a "
    "transitively relational selection function, would complete the "
    "formal picture. Three candidate sources for such an ordering: "
    "(a) **temporal recency** of the revision containing the belief; "
    "(b) **structural centrality** -- in-degree in the dependency graph; "
    "(c) **confidence metadata** attached by the Dream State pipeline. "
    "None is obviously canonical for all belief types; the conjecture is "
    "a **type-dependent entrenchment function** -- recency for "
    "preferences, evidential support for facts, confidence score for "
    "inferred beliefs. Formalizing requires proving that the type-"
    "restricted orderings compose into a global total preorder satisfying "
    "the Gardenfors-Makinson conditions [@Gardenfors1988], or showing "
    "that a weaker condition (partial preorder with type-local totality) "
    "suffices. Potentially building on Chandler-Booth's "
    "[@ChandlerBooth2025IJCAI] parallel belief revision and Meng et al.'s "
    "[@Meng2025BeliefAlgebras] iterated revision algebras "
    "[@Park2026Kumiho, Sec. 16.2].",
    title="Future: type-dependent entrenchment ordering for K*7/K*8 representation theorem",
)

claim_future_richer_logics = claim(
    "**Future direction: richer logics.** Extending $L_G$ toward "
    "fragments of description logics that remain AGM-compatible "
    "[@Qi2006DLRevision], potentially via Aiguier et al.'s [@Aiguier2018] "
    "satisfaction-system framework. This would enable subsumption "
    "reasoning and role composition within the belief-revision framework "
    "[@Park2026Kumiho, Sec. 16.2].",
    title="Future: richer logics (DL fragments, satisfaction-system framework)",
)

claim_future_partial_merge_operator = claim(
    "**Future direction: partial-merge operator.** Defining a formally "
    "characterized merge operator for partial belief updates within a "
    "single revision. The current whole-revision replacement strategy "
    "is clean but coarse-grained. A merge operator based on Konieczny "
    "and Pino Perez's [@KoniecznyPinoPerez2002] belief-merging framework "
    "could handle contradictory sub-claims by identifying the minimal "
    "set of conflicting atoms and replacing only those, while preserving "
    "unchanged co-located beliefs. The key challenge is ensuring such "
    "an operator satisfies the AGM postulates -- particularly Relevance "
    "[@Park2026Kumiho, Sec. 16.2].",
    title="Future: formally characterized partial-merge operator (Konieczny-Pino Perez framework)",
)

# ---------------------------------------------------------------------------
# 16.3: System extensions
# ---------------------------------------------------------------------------

claim_future_adaptive_consolidation = claim(
    "**Future direction: adaptive consolidation.** Urgency-based "
    "triggering; agent-initiated consolidation. Extending the Dream "
    "State with anticipatory pre-computation -- pre-reasoning about "
    "likely future queries over the graph structure (e.g., pre-computing "
    "AnalyzeImpact cascades for recently revised beliefs) -- following "
    "Letta's sleep-time compute approach [@LettaSleepTime2025] "
    "[@Park2026Kumiho, Sec. 16.3].",
    title="Future: adaptive consolidation + anticipatory pre-computation",
)

claim_future_temporal_recency_retrieval = claim(
    "**Future direction: temporal recency in retrieval.** Incorporating "
    "recency as a third retrieval signal alongside fulltext and vector "
    "scoring would automatically prioritize recent revisions in the "
    "scoring function rather than requiring agent-layer reasoning to do "
    "so [@Park2026Kumiho, Sec. 16.3].",
    title="Future: temporal recency as third retrieval signal alongside BM25 + vector",
)

# ---------------------------------------------------------------------------
# 17: Conclusion synthesis
# ---------------------------------------------------------------------------

claim_conclusion_unification = claim(
    "**Conclusion: unification not novelty.** Several individual "
    "components exist in concurrent systems; Park does not claim novelty "
    "for them individually. The contribution is their **architectural "
    "synthesis**, grounded in formal belief-revision analysis and the "
    "recognition that cognitive memory and work-product management share "
    "**identical structural requirements**. In an era where AI agents "
    "perform consequential work -- producing artifacts, making "
    "decisions, collaborating autonomously in multi-agent pipelines -- "
    "their memory must serve double duty: as the cognitive substrate for "
    "individual agent intelligence and as the shared operational "
    "infrastructure through which agents coordinate, build upon each "
    "other's outputs, and maintain auditable provenance chains "
    "[@Park2026Kumiho, Sec. 17].",
    title="Conclusion: contribution is the architectural synthesis + formal grounding, not novel components",
)

__all__ = [
    "claim_future_goal_aware_indexing",
    "claim_future_chronological_ordering",
    "claim_future_ablation_study",
    "claim_future_controlled_cross_system",
    "claim_future_retrieval_ablation",
    "claim_future_entrenchment_k7k8",
    "claim_future_richer_logics",
    "claim_future_partial_merge_operator",
    "claim_future_adaptive_consolidation",
    "claim_future_temporal_recency_retrieval",
    "claim_conclusion_unification",
]
