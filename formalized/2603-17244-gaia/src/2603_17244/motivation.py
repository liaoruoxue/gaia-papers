"""Motivation: AI agents shift from chatbots to workers, creating intertwined needs
for cognitive memory and work-product management that current architectures address
separately if at all.

Section 1 (Introduction) and the abstract of Park (2026) [@Park2026Kumiho]. The
paper diagnoses a structural gap: agents now produce substantial outputs (code,
designs, documents, intermediate results) without systematic versioning,
provenance tracking, or linkage to the decisions that created them. In
multi-agent workflows -- where one agent's output is the next agent's input --
this is a fundamental bottleneck. The core architectural insight is that the
structural primitives required for cognitive memory (immutable revisions, mutable
tag pointers, typed dependency edges, URI-based addressing) are *identical* to
those required for managing agent-produced outputs as versionable, addressable,
dependency-linked assets. The proposal is therefore to build a single graph-
native primitive set serving both roles, grounded formally in a correspondence
between graph operations and the AGM belief-revision postulates.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setting
# ---------------------------------------------------------------------------

setup_agentic_regime = setting(
    "**Production agentic AI regime.** Large language models (LLMs) have shifted "
    "from stateless question-answering systems and conversational chatbots to "
    "AI agents: autonomous workers that execute multi-step tasks, produce "
    "digital artifacts (code, designs, documents, intermediate results), make "
    "consequential decisions, and collaborate with humans and other agents "
    "across extended workflows [@Park2026Kumiho, Sec. 1].",
    title="Setup: AI agents act as autonomous workers, not stateless chatbots",
)

setup_two_requirements = setting(
    "**Two intertwined memory requirements.** This shift creates two requirements "
    "that current architectures address separately, if at all. First, agents need "
    "**cognitive memory** -- the ability to remember past interactions, track how "
    "beliefs evolved, recall why decisions were made, and consolidate experience "
    "into reusable knowledge. Second, agents need **work-product management** -- "
    "the ability to version, locate, and build upon the artifacts they produce "
    "so that downstream agents in a multi-step pipeline can find the right "
    "input revision, understand its provenance, and link their own output back "
    "to the chain [@Park2026Kumiho, Sec. 1].",
    title="Setup: agents need both cognitive memory AND work-product management",
)

setup_belief_base_level = setting(
    "**Belief base, not belief set.** The architecture is formalized at the "
    "level of *belief bases* (finite sets not closed under logical consequence) "
    "following Hansson [@Hansson1999Textbook], rather than AGM belief sets "
    "(infinite, closed under $\\mathrm{Cn}$). The belief base level is the "
    "appropriate abstraction for computational systems because the memory graph "
    "stores finite, explicitly-stored propositions, never deductive closures "
    "[@Park2026Kumiho, Sec. 7].",
    title="Setup: formal analysis is at the Hansson belief-base level",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Can a single graph-native primitive set (immutable revisions, mutable tag "
    "pointers, typed dependency edges, URI-based addressing) serve as both an "
    "AGM-compliant cognitive memory layer for AI agents AND the operational "
    "infrastructure for managing those agents' work products in multi-agent "
    "pipelines, replacing the prevailing pattern of separate memory layer + "
    "asset tracker?",
    title="Central question: can one graph substrate serve cognitive memory AND asset management?",
)

# ---------------------------------------------------------------------------
# Diagnosis: the structural gap in concurrent agent-memory systems
# ---------------------------------------------------------------------------

claim_components_exist = claim(
    "**Individual components for AI-agent memory exist in prior systems.** "
    "Versioning, retrieval, and consolidation primitives are independently "
    "implemented across concurrent systems: Graphiti/Zep [@Graphiti2025] (Neo4j "
    "temporal knowledge graphs with bitemporal versioning and BM25+vector+graph "
    "retrieval), Mem0 [@Mem02025] (timestamped versioned memories with LLM "
    "conflict resolution), Letta/MemGPT [@MemGPT2023; @LettaSleepTime2025] "
    "(virtual-context extension with sleep-time consolidation), A-MEM "
    "[@AMEM2025NeurIPS] (Zettelkasten-inspired dynamic linking), MAGMA "
    "[@MAGMA2026] (multi-graph architecture), Hindsight [@Hindsight2025] "
    "(four-network confidence-scored beliefs), and MemOS [@MemOS2025] "
    "(hierarchical OS-style memory manager) [@Park2026Kumiho, Sec. 2.1].",
    title="Diagnosis: agent-memory components (versioning, retrieval, consolidation) exist independently",
)

claim_synthesis_underexplored = claim(
    "**Their architectural synthesis and formal grounding remain underexplored.** "
    "While individual components exist, no concurrent system provides (i) a unified "
    "architecture binding versioning + retrieval + consolidation under a shared "
    "graph substrate, (ii) a formal correspondence to belief-revision theory, and "
    "(iii) a unification with work-product / asset management. The literature "
    "search reported in [@Park2026Kumiho, Sec. 4.2] found no prior work unifying "
    "cognitive memory and asset management on a shared graph.",
    title="Diagnosis: synthesis + formal grounding + asset unification are missing",
)

claim_agent_outputs_accumulate = claim(
    "**Agent-produced artifacts accumulate without systematic management.** AI "
    "agents increasingly produce substantial digital outputs -- generated images, "
    "code commits, design iterations, research documents, intermediate results -- "
    "that accumulate without systematic versioning, provenance tracking, or "
    "linkage to the decisions that created them. As sessions accumulate, these "
    "outputs become lost, duplicated, or untraceable. In multi-agent workflows -- "
    "where one agent's output is the next agent's input -- this lack of "
    "structure is a fundamental bottleneck (e.g., a video-compositing agent "
    "cannot locate the approved texture revision produced by an upstream "
    "generation agent) [@Park2026Kumiho, Sec. 1; Sec. 4.2; Principle 1].",
    title="Diagnosis: agent outputs accumulate untracked; multi-agent handoff is the bottleneck",
)

claim_separate_layers_assumption = claim(
    "**The prevailing assumption is that memory and asset tracking are separate "
    "concerns requiring separate layers.** Concurrent agent-memory systems "
    "[@Graphiti2025; @Mem02025; @AMEM2025NeurIPS; @MemGPT2023; @MAGMA2026; "
    "@Hindsight2025; @MemOS2025] all treat agent memory as one infrastructure "
    "concern, leaving artifact tracking to file paths, naming conventions, "
    "or dedicated asset-management systems backed by relational databases "
    "(PostgreSQL/MySQL) with RPC frameworks (Thrift/gRPC). The implicit "
    "premise is that cognitive memory and work-product management are "
    "structurally distinct and demand separate substrates "
    "[@Park2026Kumiho, Sec. 4.2].",
    title="Diagnosis: prevailing view treats memory and asset tracking as separate layers",
)

claim_context_extension_not_memory = claim(
    "**Context-window extension does not constitute memory.** The most common "
    "alternative response is to expand the context window itself (4K -> 128K -> "
    "200K+ tokens). Larger windows accommodate more immediate context but provide "
    "no mechanism for versioning beliefs, tracking evidential provenance, "
    "expressing dependency relationships between conclusions, or consolidating "
    "many episodes into generalized knowledge. Transformer attention scales as "
    "$\\Theta(n^2 \\cdot d)$ [@Vaswani2017Attention], whereas a retrieval system "
    "indexing $N$ memories and retrieving top-$k$ incurs $O(\\log N) + O(k^2 "
    "\\cdot d)$, making context extension economically and computationally "
    "infeasible for lifelong agent memory [@Park2026Kumiho, Sec. 1; Sec. 3].",
    title="Diagnosis: context-window extension is attention capacity, not memory",
)

# ---------------------------------------------------------------------------
# The core architectural insight (the unification thesis)
# ---------------------------------------------------------------------------

claim_structural_correspondence = claim(
    "**Cognitive memory and asset management share *identical* core primitives.** "
    "Remembering 'the client prefers warm color palettes' (cognitive memory) and "
    "tracking 'environment-lighting revision 5 is the approved version' "
    "(work-product management) both require: (i) immutable versioned snapshots, "
    "(ii) typed dependency edges, (iii) mutable status pointers, (iv) URI-based "
    "addressing, and (v) content-reference separation. The domains differ in "
    "semantics (belief revision under uncertainty vs. deterministic asset "
    "workflows), but the underlying *data model* is shared. The structural "
    "correspondence (Table 2 of [@Park2026Kumiho]):\n\n"
    "| Asset Management | Cognitive Memory | Concept |\n"
    "|------------------|------------------|---------|\n"
    "| Project          | Scope            | Container |\n"
    "| Space            | Topic            | Namespace |\n"
    "| Item             | Unit             | Identity |\n"
    "| Revision         | Belief snapshot  | Snapshot |\n"
    "| Artifact         | Evidence pointer | Pointer |\n"
    "| Tag              | Status           | Mutable ref |\n"
    "| Edge             | Relation         | Typed link |\n"
    "| Bundle           | Cluster          | Grouping |\n",
    title="Insight: memory primitives = asset-management primitives (Table 2)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 2",
        "caption": "Structural correspondence between asset management and cognitive memory.",
    },
)

claim_unified_thesis = claim(
    "**Architectural thesis: build ONE graph-native primitive set serving BOTH "
    "roles.** Rather than building a memory layer plus a separate asset tracker, "
    "Kumiho builds a single cognitive memory architecture whose graph-native "
    "primitives (immutable revisions, typed edges, mutable tag pointers, URI "
    "addressing) inherently serve as the operational infrastructure for "
    "multi-agent work. Agents use the *same* graph to remember past interactions, "
    "to find each other's outputs, and to build upon them, enabling fully "
    "autonomous multi-agent pipelines without separate asset-tracking systems "
    "[@Park2026Kumiho, abstract; Sec. 1; Sec. 4.2; Sec. 4.3].",
    title="Thesis: ONE graph-native primitive set serves both memory AND asset management",
)

# ---------------------------------------------------------------------------
# The central formal contribution
# ---------------------------------------------------------------------------

claim_agm_correspondence_thesis = claim(
    "**Central formal contribution: a correspondence between AGM belief revision "
    "and graph-native operations.** Park (2026) establishes a structural "
    "correspondence between the Alchourron-Gardenfors-Makinson framework "
    "[@AGM1985] and the operational semantics of the property-graph memory "
    "system, framed at the *belief base* level [@Hansson1999Textbook]. The "
    "correspondence proves satisfaction of the basic AGM postulates "
    "$K^\\ast 2$-$K^\\ast 6$ and Hansson's belief-base postulates (Relevance, "
    "Core-Retainment), provides a principled rejection of the Recovery "
    "postulate grounded in immutable versioning, identifies the supplementary "
    "postulates ($K^\\ast 7$, $K^\\ast 8$) as open questions, and formally "
    "avoids the Flouris et al. impossibility for description logics "
    "[@Flouris2005DL] by working over a deliberately weak propositional "
    "fragment [@Park2026Kumiho, Sec. 7].",
    title="Formal contribution: AGM-vs-graph correspondence at the Hansson belief-base level",
)

# ---------------------------------------------------------------------------
# Headline empirical contributions (proved across Sections 15.2, 15.3, 15.7)
# ---------------------------------------------------------------------------

claim_locomo_headline = claim(
    "**Headline empirical -- LoCoMo 0.447 four-category F1.** On the LoCoMo "
    "benchmark [@LoCoMo2024] with the official token-level F1 metric (Porter "
    "stemming), Kumiho achieves 0.447 four-category F1 ($n=1{,}540$) -- the "
    "highest reported score across the retrieval categories vs. Zep (-) "
    "[@ZepBenchmark2025], Mem0 ~0.40, Memobase [@Memobase2025], and ENGRAM "
    "0.211 [@ENGRAM2025]. Adversarial refusal accuracy reaches 97.5% "
    "($n=446$, binary scoring). Including adversarial, overall F1 is 0.565 "
    "($n=1{,}986$) [@Park2026Kumiho, Sec. 15.2; Tables 12-13].",
    title="Preview: LoCoMo 0.447 four-category F1 + 97.5% adversarial refusal",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 12 / Table 13",
        "caption": "LoCoMo token-level F1 cross-system comparison and per-category breakdown.",
    },
)

claim_locomo_plus_headline = claim(
    "**Headline empirical -- LoCoMo-Plus 93.3% judge accuracy.** On LoCoMo-Plus "
    "[@LoCoMoPlus2026] -- a Level-2 cognitive memory benchmark testing implicit "
    "constraint recall under intentional cue-trigger semantic disconnect -- "
    "Kumiho achieves 93.3% judge accuracy ($n=401$, all four constraint types) "
    "with GPT-4o as the answer model, outperforming the best published baseline "
    "(Gemini 2.5 Pro at 45.7%) by 47.6 percentage points. Recall accuracy "
    "reaches 98.5% (395/401), with 78% of the 6.7% end-to-end gap "
    "attributable to answer-model fabrication on correctly retrieved context. "
    "Independent reproduction by the benchmark authors yielded results in the "
    "mid-80% range -- still substantially outperforming all published baselines "
    "[@Park2026Kumiho, Sec. 15.3; Tables 15-17].",
    title="Preview: LoCoMo-Plus 93.3% judge accuracy + 98.5% recall (best baseline 45.7%)",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 15 / Table 16 / Table 17",
        "caption": "LoCoMo-Plus accuracy vs. published baselines, by constraint type and time gap.",
    },
)

claim_agm_compliance_headline = claim(
    "**Headline empirical -- 100% AGM compliance across 49 scenarios.** An "
    "automated test suite of 49 scenarios across 5 categories (simple, "
    "multi-item, chain, temporal, adversarial) tests all 7 claimed postulates "
    "($K^\\ast 2$-$K^\\ast 6$, Relevance, Core-Retainment). The 100% pass rate "
    "confirms that the implementation faithfully executes the formal "
    "specification, including under adversarial stress (rapid sequential "
    "revisions, deep dependency chains, mixed edge types) [@Park2026Kumiho, "
    "Sec. 15.7; Table 18].",
    title="Preview: 100% AGM compliance pass rate across 49 scenarios",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 18",
        "caption": "AGM compliance verification (49 scenarios) across 7 postulates and 5 categories.",
    },
)

# ---------------------------------------------------------------------------
# Headline contribution claim (the paper's announced takeaway)
# ---------------------------------------------------------------------------

claim_headline_contribution = claim(
    "**Headline contribution: Kumiho is a graph-native cognitive memory "
    "architecture in which a single primitive set serves both belief-revision-"
    "compliant memory and operational asset management.** Specific contributions "
    "[@Park2026Kumiho, Sec. 1]: (i) unified cognitive-memory + asset-management "
    "architecture (Sec. 4); (ii) formal belief-base revision correspondence "
    "with the AGM postulates and Hansson's base postulates (Sec. 7); (iii) "
    "URI-based universal addressing (`kref://project/space/item.kind?r=N&a=art`) "
    "enabling deterministic resolution and provenance traversal; (iv) safety-"
    "hardened consolidation pipeline (Sec. 9) with published-item protection, "
    "circuit breakers, dry-run validation, and cursor-based resumption; (v) SDK "
    "transparency exposing the same graph for agent operation and human audit "
    "(Sec. 5.2); (vi) LoCoMo 0.447 four-category F1 + 97.5% adversarial refusal "
    "(Sec. 15.2); (vii) empirical AGM compliance verification (49 scenarios, "
    "100% pass) (Sec. 15.7); (viii) LoCoMo-Plus 93.3% judge accuracy / 98.5% "
    "recall (Sec. 15.3); (ix) cross-benchmark generalization driven by "
    "prospective indexing, event extraction, and client-side LLM reranking "
    "(Sec. 8.8). Reference implementation: [@KumihoCode].",
    title="Headline contribution: Kumiho = unified memory+asset architecture with AGM correspondence",
)

__all__ = [
    "setup_agentic_regime",
    "setup_two_requirements",
    "setup_belief_base_level",
    "q_central",
    "claim_components_exist",
    "claim_synthesis_underexplored",
    "claim_agent_outputs_accumulate",
    "claim_separate_layers_assumption",
    "claim_context_extension_not_memory",
    "claim_structural_correspondence",
    "claim_unified_thesis",
    "claim_agm_correspondence_thesis",
    "claim_locomo_headline",
    "claim_locomo_plus_headline",
    "claim_agm_compliance_headline",
    "claim_headline_contribution",
]
