"""Sections 9, 10: Future Work and Limitations.

Three future-work directions (near/medium/long term) and three explicit
limitations bound the paper's claims. These are formalized as claims
rather than settings because each is contestable and the paper itself
flags them as honest constraints on its current scope.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Future Work (§9)
# ---------------------------------------------------------------------------

claim_fw_lineage = claim(
    "**Near-term future work: artifact lineage and self-maintaining "
    "ecosystems.** ARAs decay without maintenance as dependencies rot "
    "and practices evolve. The natural extension is a **lineage "
    "mechanism** in which each ARA declares its parent artifacts and "
    "expresses its contribution as a structured *diff*, reducing "
    "construction cost (specify only the delta) and verification cost "
    "(re-check only the new contribution). Lineage also enables self-"
    "maintaining ecosystems: agents consuming an ARA detect and repair "
    "staleness, update deprecated dependencies, and propagate "
    "corrections upstream, so every act of consumption becomes an act "
    "of maintenance.",
    title="FW1 (near-term): artifact lineage + diff-based contributions + self-maintaining ecosystems",
)

claim_fw_knowledge_graph = claim(
    "**Medium-term future work: knowledge graph + collaborative "
    "discovery + continuous review.** Aggregated lineages form a "
    "queryable scientific knowledge graph that lifts collaboration and "
    "review from document level to corpus level. Cross-artifact claim "
    "alignment turns literature synthesis into subgraph queries, lets "
    "reviewer agents verify reported baselines, and exposes trajectory "
    "conflicts where a method claimed successful elsewhere was "
    "documented as failing. Review evolves: there is **no single accept "
    "moment, only a claim-confidence surface** that rises with "
    "replications and falls with counter-evidence.",
    title="FW2 (medium-term): cross-artifact knowledge graph + claim-confidence surface (no single accept)",
)

claim_fw_cross_disciplinary = claim(
    "**Long-term future work: cross-disciplinary collective memory.** "
    "The Cognitive and Evidence Layers are plausibly domain-agnostic, "
    "but the Physical Layer and Exploration Graph -- premised on "
    "iterable computational experiments -- may require substantial "
    "adaptation for wet-lab sciences where execution is physical "
    "rather than computational. If these adaptations succeed, ARA "
    "provides a substrate for cross-disciplinary knowledge transfer "
    "where documented failures in one field become actionable "
    "knowledge in another via graph traversal rather than literature "
    "search in unfamiliar notation.",
    title="FW3 (long-term): cross-disciplinary collective memory; wet-lab adaptation needed",
)

# ---------------------------------------------------------------------------
# Limitations (§10) -- explicit constraints on the claims in this paper
# ---------------------------------------------------------------------------

claim_lim_evaluation_scope = claim(
    "**Limitation 1: evaluation scope is restricted to ML papers.** "
    "All evaluation is on machine-learning papers (ICML 2024) plus "
    "RE-Bench R&D tasks. Whether the protocol generalizes to "
    "experimental sciences with physical execution requirements, or to "
    "theoretical disciplines where the Physical Layer is largely "
    "absent, remains **empirically untested**. Extending the Physical "
    "Layer to formal/proof-based results requiring machine-checkable "
    "specifications is a natural future direction. The benchmark was "
    "also constructed by annotators familiar with both the ARA format "
    "and the selected papers, so performance on unfamiliar or niche-"
    "domain artifacts may differ from reported figures.",
    title="Limit 1: ML-only evaluation; generalization to physical/theoretical sciences untested",
)

claim_lim_fidelity_ceiling = claim(
    "**Limitation 2: fidelity is bounded by the source of supervision.** "
    "ARA fidelity is bounded by the supervision source. The Compiler "
    "*faithfully represents* only what the PDF contains -- when a "
    "paper omits experimental details, environment specifications, or "
    "ablation results, no extraction method can recover them. The Live "
    "Research Manager closes this gap by recording trajectories as "
    "research unfolds, but assumes an **AI-native workflow** in which "
    "a coding agent is present throughout the project. For researchers "
    "outside such sessions, the Compiler still produces a valid ARA "
    "from the finished paper, but the resulting artifact inherits the "
    "PDF's omissions; hand-authoring structured fields remains "
    "possible but reintroduces the documentation burden the protocol "
    "aims to eliminate.",
    title="Limit 2: fidelity bounded by source; LRM pre-supposes AI-native workflow",
)

claim_lim_deployment_prerequisites = claim(
    "**Limitation 3: deployment prerequisites not yet implemented.** "
    "Two properties required for production use are aspirational in "
    "the current system: (a) **adversarial robustness and privacy** -- "
    "the current system lacks sandboxed execution, content-level "
    "anomaly detection, and granular access control for the "
    "Exploration Graph; (b) **schema evolution** -- as research "
    "practice changes, the ARA schema will need to add node types, "
    "refine field semantics, and deprecate conventions without "
    "breaking prior artifacts. The paper versions PAPER.md frontmatter "
    "with an explicit `ara_schema` tag and requires validators to "
    "accept unknown fields (forward compatibility) and degrade "
    "gracefully on missing optional fields (backward compatibility), "
    "but has only exercised this discipline across **minor** "
    "revisions. A stable migration story for major revisions remains "
    "future work.",
    title="Limit 3: missing sandboxing, access control, and major-revision schema migration story",
)

# ---------------------------------------------------------------------------
# Conclusion (§11) - core synthesizing claim
# ---------------------------------------------------------------------------

claim_thesis = claim(
    "**Central thesis: the two structural failures of the PDF format "
    "(Storytelling Tax + Engineering Tax) are addressed by the ARA "
    "protocol because narrative compilation is the cause, not agent "
    "capability.** ARA resolves both taxes by restructuring a research "
    "contribution as a machine-actionable artifact -- one that is "
    "navigable, complete, and verifiable without human interpretation. "
    "The empirical evidence (Understanding +21.3pp, Reproduction "
    "+7.0pp weighted, Extension early-acceleration on all 5 tasks) "
    "establishes that an artifact-format intervention closes a "
    "*structural* gap that improvements in agent capability alone "
    "would not close. The broader motivation: AI agents are becoming "
    "first-class participants in research workflows -- not tools that "
    "assist humans but autonomous contributors that read, reproduce, "
    "and extend scientific work -- and that transition demands "
    "infrastructure built around agents from the start.",
    title="Thesis: the two taxes (not agent capability) explain reproduction/extension failures; ARA closes the structural gap",
)

__all__ = [
    "claim_fw_lineage",
    "claim_fw_knowledge_graph",
    "claim_fw_cross_disciplinary",
    "claim_lim_evaluation_scope",
    "claim_lim_fidelity_ceiling",
    "claim_lim_deployment_prerequisites",
    "claim_thesis",
]
