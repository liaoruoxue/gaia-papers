"""Section 2 (Related Work) of [@Park2026Kumiho]: Agent memory architectures,
belief revision in AI, versioned knowledge graphs, hybrid retrieval and score
fusion, AI agent observability.

Each subsection identifies what concurrent systems do and -- crucially -- what
they lack. The per-system gaps motivate the cross-system architectural-synthesis
claim that drives the unification thesis (formalized in `motivation.py`).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Benchmarks (settings)
# ---------------------------------------------------------------------------

setup_locomo_benchmark = setting(
    "**LoCoMo benchmark.** LoCoMo [@LoCoMo2024] is a multi-session conversation "
    "benchmark comprising 1,986 questions across 10 conversations and five "
    "categories (single-hop, multi-hop, temporal, open-domain, adversarial), "
    "designed to test long-term memory retrieval across extended conversational "
    "histories. The official metric is *token-level F1 with Porter stemming*; "
    "adversarial questions use binary refusal-detection scoring "
    "[@Park2026Kumiho, Sec. 15.2].",
    title="Setup: LoCoMo benchmark (1,986 questions, 5 categories, token-level F1)",
)

setup_locomo_plus_benchmark = setting(
    "**LoCoMo-Plus benchmark.** LoCoMo-Plus [@LoCoMoPlus2026] (Feb 2026) tests "
    "*implicit constraint recall under intentional cue-trigger semantic "
    "disconnect*: a cue dialogue embeds a constraint (e.g., \"Joanna decided "
    "to quit sugar\") that a later trigger query must connect to (e.g., \"I've "
    "been indulging in new desserts\") with no surface lexical overlap. The "
    "benchmark comprises 401 entries stitched into 10 LoCoMo base "
    "conversations spanning four constraint types -- causal ($n=101$), state "
    "($n=100$), value ($n=100$), goal ($n=100$) -- with cue-trigger time gaps "
    "from 2 weeks to 12+ months. All tested baselines, including premium "
    "models with million-token context windows, score 23-46% "
    "[@Park2026Kumiho, Sec. 15.3].",
    title="Setup: LoCoMo-Plus benchmark (401 entries, Level-2 implicit-constraint recall)",
)

setup_human_memory_template = setting(
    "**Human memory as design template.** Cognitive science distinguishes "
    "**working memory** -- a capacity-limited, rapidly-accessible buffer "
    "[@AtkinsonShiffrin1968; @Baddeley2000] -- from **long-term memory**, "
    "further divided into episodic and semantic stores [@Tulving1972]. "
    "Transfer from episodic to semantic memory involves active consolidation "
    "during sleep [@RaschBorn2013]. Human decision-making proceeds through a "
    "loop of *perceive -> recall -> revise -> act* that a memory-equipped AI "
    "agent must replicate [@Park2026Kumiho, Sec. 4.1].",
    title="Setup: human cognitive architecture as design template",
)

# ---------------------------------------------------------------------------
# 2.1 Concurrent agent-memory systems: per-system characterizations
# ---------------------------------------------------------------------------

claim_graphiti_components = claim(
    "**Graphiti / Zep [@Graphiti2025] shares the most surface components with "
    "Kumiho but lacks formal grounding, URI addressing, and BYO-storage.** "
    "Graphiti implements a temporal knowledge graph on Neo4j with entity-event "
    "synthesis, bitemporal versioning, and triple-modality hybrid retrieval "
    "(BM25 + cosine + graph traversal). It reports 94.8% on Deep Memory "
    "Retrieval (DMR) and 18.5% improvement on LongMemEval. The architectural "
    "differences from Kumiho are threefold [@Park2026Kumiho, Sec. 2.1]: (i) "
    "no formal belief-revision correspondence; (ii) no URI addressing scheme "
    "for deterministic cross-system memory references; (iii) processes and "
    "stores full content server-side, whereas Kumiho's BYO-storage keeps raw "
    "data on the user's local storage.",
    title="Diagnosis: Graphiti has retrieval/versioning but no formalism, no URI, no BYO-storage",
)

claim_mem0_components = claim(
    "**Mem0 / Mem0g [@Mem02025] is a triple-store with timestamped versioning "
    "and LLM-based conflict resolution but no formal revision semantics.** "
    "Mem0 reports a 26% improvement over OpenAI Memory on LoCoMo. It provides "
    "neither AGM-compliant revision operators nor immutable revision history "
    "with provenance preservation [@Park2026Kumiho, Sec. 2.1; Table 9].",
    title="Diagnosis: Mem0 has timestamped versioning but no formal AGM revision",
)

claim_letta_components = claim(
    "**Letta / MemGPT [@MemGPT2023; @LettaSleepTime2025] introduced sleep-time "
    "compute (asynchronous background consolidation) -- the same biological "
    "metaphor as Kumiho's Dream State -- and the recent Letta Context "
    "Repositories [@LettaContextRepos2026] (Feb 2026) provide Git-backed "
    "versioned Markdown files with merge-based conflict resolution.** Letta is "
    "the most structurally related production system to Kumiho's versioned "
    "memory concept but differs fundamentally: (i) **versioning substrate** -- "
    "Letta uses Git pragmatically over Markdown files, yielding only "
    "file-and-commit primitives, whereas Kumiho's graph-native approach "
    "yields typed cognitive edges, multi-tag pointer layers, artifact "
    "attachments, and hierarchical project/space scoping; (ii) **conflict "
    "resolution** -- Letta resolves concurrent writes via Git's text-level "
    "merge that detects but cannot semantically resolve contradictory beliefs, "
    "whereas Kumiho's `Supersedes` edge creates a new revision with formal "
    "AGM guarantees (Success, Consistency, Relevance); (iii) **downstream "
    "propagation** -- updating a belief in one Letta file does not "
    "automatically identify dependent files, whereas Kumiho's typed "
    "`Depends_On` edges enable `AnalyzeImpact` traversal "
    "[@Park2026Kumiho, Sec. 2.1].",
    title="Diagnosis: Letta has Git-backed versioning but lacks typed edges, AGM, impact analysis",
)

claim_amem_components = claim(
    "**A-MEM [@AMEM2025NeurIPS] introduces Zettelkasten-inspired dynamic "
    "linking (NeurIPS 2025) but lacks formal belief-revision correspondence, "
    "URI addressing, and unified asset management.** It contributes a dynamic "
    "linking mechanism for memory association but offers no formal guarantees "
    "on belief change or compositional consolidation [@Park2026Kumiho, "
    "Sec. 2.1; Table 9].",
    title="Diagnosis: A-MEM has dynamic linking but no formalism or unified asset graph",
)

claim_magma_components = claim(
    "**MAGMA [@MAGMA2026] proposes a multi-graph architecture with four "
    "orthogonal layers (semantic, temporal, causal, entity) and policy-guided "
    "retrieval traversal, achieving the highest LoCoMo judge score of 0.70 "
    "(LLM-as-judge, not token-level F1) and 61.2% on LongMemEval with 95% "
    "token reduction.** MAGMA's design represents an alternative philosophical "
    "commitment: it disentangles memory dimensions into separate graphs for "
    "cleaner retrieval routing, whereas Kumiho unifies all relationships in a "
    "single property graph with typed edges, enabling cross-dimensional "
    "traversal (`AnalyzeImpact` propagating across all edge types "
    "simultaneously). Multi-graph separation introduces synchronization "
    "complexity for cross-dimensional updates and requires joins across storage "
    "boundaries; the unified property graph accepts edge-type heterogeneity "
    "in exchange for transactional atomicity, which is what enables Kumiho's "
    "AGM-compliance results [@Park2026Kumiho, Sec. 2.1; Sec. 12.5].",
    title="Diagnosis: MAGMA disentangles dimensions across graphs (alt. to Kumiho's unified graph)",
)

claim_hindsight_components = claim(
    "**Hindsight [@Hindsight2025] proposes a four-network memory architecture "
    "(facts, experiences, opinions, observations) achieving 89.61% on LoCoMo "
    "and 91.4% on LongMemEval with confidence-scored beliefs.** Its Opinion "
    "Network maintains beliefs that update with evidence -- a pragmatic form "
    "of belief versioning -- but without formal AGM grounding. The empirical "
    "success of Hindsight demonstrates that practical belief tracking delivers "
    "strong results; Kumiho's contribution complements this by providing the "
    "formal framework that could *guarantee* consistency properties "
    "(Relevance, Core-Retainment) for systems like Hindsight "
    "[@Park2026Kumiho, Sec. 2.1; Sec. 12.6].",
    title="Diagnosis: Hindsight has empirical belief tracking but no AGM guarantees",
)

claim_memos_components = claim(
    "**MemOS [@MemOS2025] (EMNLP 2025 Oral) implements a hierarchical memory "
    "manager with global, local, and working memory buffers inspired by "
    "operating-system design.** It provides tiered buffers but with the "
    "memory-management logic typically embedded within the LLM's own "
    "reasoning process, creating tight LLM-memory coupling -- the very "
    "regime Kumiho's MCP-based decoupling aims to avoid "
    "[@Park2026Kumiho, Sec. 2.1; Sec. 12.2].",
    title="Diagnosis: MemOS has tiered buffers but with LLM-coupled memory management",
)

# ---------------------------------------------------------------------------
# 2.1 Cross-system comparison (Table 1) and benchmark caveat
# ---------------------------------------------------------------------------

claim_table1_comparison = claim(
    "**Cross-system architectural comparison (Table 1 of [@Park2026Kumiho]).** "
    "Across six dimensions (versioning, conflict resolution, retrieval, formal "
    "grounding, URI addressing, consolidation), no concurrent system covers all "
    "six.\n\n"
    "| Dim. | Graphiti | Mem0 | Letta | Hindsight | Kumiho |\n"
    "|------|----------|------|-------|-----------|--------|\n"
    "| Version | Bitemporal | Timestamped | Git | None | Immutable+tags |\n"
    "| Conflict | Temporal | LLM | Git merge | Confidence | AGM `Supersedes` |\n"
    "| Retrieval | BM25+vector | Graph | File | 4-net | Hybrid |\n"
    "| Formal | None | None | None | None | AGM postulates |\n"
    "| URI | x | x | Git | x | `kref://` |\n"
    "| Consolidation | Temporal | None | Git GC | None | Dream State |\n",
    title="Cross-system comparison: no prior system covers all six architectural dimensions",
    metadata={
        "source_table": "artifacts/2603.17244.pdf, Table 1",
        "caption": "Architectural comparison with selected concurrent systems.",
    },
)

claim_benchmark_standardization_caveat = claim(
    "**Benchmark standardization caveat: no standardized LoCoMo leaderboard "
    "exists.** All reported numbers across concurrent systems use varying "
    "evaluation configurations (different judge models, question subsets, "
    "evaluation prompts). EverMemOS's [@EverMemOS2026] 93.05% is evaluated "
    "using their own framework with no independent reproduction. Li et al. "
    "[@LoCoMoPlus2026] introduced LoCoMo-Plus (Feb 2026), demonstrating that "
    "existing LoCoMo scores largely measure explicit factual recall under "
    "strong semantic alignment rather than genuine cognitive memory under "
    "cue-trigger semantic disconnect; all tested systems show substantial "
    "performance drops from LoCoMo to LoCoMo-Plus. Kumiho therefore reports "
    "results on the official token-level F1 metric on LoCoMo and on "
    "LoCoMo-Plus to enable direct comparison [@Park2026Kumiho, Sec. 2.1].",
    title="Caveat: no standardized LoCoMo leaderboard; LoCoMo-Plus added to break comparability gap",
)

# ---------------------------------------------------------------------------
# 2.2 Belief revision in AI
# ---------------------------------------------------------------------------

claim_agm_lineage = claim(
    "**The AGM framework [@AGM1985; @Gardenfors1988] defines rationality "
    "postulates for belief change.** Hansson [@Hansson1999Textbook] extended "
    "this to belief bases -- finite sets not closed under logical consequence -- "
    "which is the appropriate level for computational systems. Kumiho's formal "
    "analysis sits within this tradition [@Park2026Kumiho, Sec. 2.2].",
    title="Theory: AGM postulates + Hansson belief-base extension are the appropriate level",
)

claim_flouris_dl_impossibility = claim(
    "**Flouris et al. [@Flouris2005DL] proved that Description Logics "
    "(including those underlying OWL) cannot satisfy the AGM revision "
    "postulates.** Qi et al. [@Qi2006DLRevision] refined this for specific "
    "DL fragments. These impossibility results are critical context: any AGM-"
    "claiming agent-memory system over a DL-style ontology re-encounters "
    "the same obstructions. Kumiho avoids this by operating on a deliberately "
    "weak propositional fragment over ground triples (Section 7.6 of "
    "[@Park2026Kumiho]).",
    title="Theory: AGM is impossible for DL/OWL; Kumiho avoids by using a weaker logic",
)

claim_agm_ml_correspondences = claim(
    "**Recent work connects AGM-style belief change to machine learning and "
    "LLM editing.** Aravanis [@Aravanis2025] establishes a correspondence "
    "between machine learning and AGM-style belief change; Hase et al. "
    "[@Hase2024ModelEditing] frame LLM model editing as belief revision; "
    "Baitalik et al. [@Baitalik2026AAAIBridge] (AAAI 2026 Bridge) apply "
    "GreedySAT-based consistency to multi-turn dialogues; Wilie et al. "
    "[@WilieEMNLP2024BeliefR] demonstrate LLMs' poor belief revision "
    "capabilities on Belief-R. Kumiho's contribution complements this stream "
    "by applying AGM to the *external memory graph* rather than to the "
    "model's internal weights or prompt context [@Park2026Kumiho, Sec. 2.2].",
    title="Theory: prior AGM/LLM connections target weights or prompts, not external memory",
)

claim_recovery_critiques = claim(
    "**The Recovery postulate has been questioned in the literature.** "
    "Makinson [@Makinson1987Recovery] identified Recovery as 'the only one "
    "among the six basic postulates that is open to query'; Hansson "
    "[@Hansson1991NoRecovery] proposed contraction without Recovery, and "
    "Fuhrmann [@Fuhrmann1991] independently argued that Recovery imposes "
    "unreasonable constraints when beliefs have non-trivial internal "
    "structure or provenance. Kumiho's principled rejection of Recovery "
    "(Section 7.3) provides a concrete operational demonstration of these "
    "theoretical concerns [@Park2026Kumiho, Sec. 2.2; Sec. 7.3].",
    title="Theory: Recovery already questioned (Makinson, Hansson, Fuhrmann)",
)

# ---------------------------------------------------------------------------
# 2.3 Versioned knowledge graphs
# ---------------------------------------------------------------------------

claim_versioned_kg_lineage = claim(
    "**Versioned knowledge graphs have substantial Semantic-Web history.** "
    "R&Wbase [@VanderSande2013RWbase] ('Git for triples') supported branching "
    "and merging for quad-stores; SemVersion [@Volkel2005SemVersion] applied "
    "version control to RDF graphs with structural diff and merge; Quit Store "
    "[@Arndt2018QuitStore] ('Quads in Git') provides a SPARQL 1.1 endpoint "
    "backed by Git-versioned RDF named graphs; OSTRICH [@Taelman2018OSTRICH] "
    "implements hybrid versioned triple storage. Kumiho's contribution is not "
    "the invention of versioned graphs (well-established) but the *application* "
    "of versioned graph primitives to **cognitive memory** specifically, "
    "combined with formal belief-revision analysis. The prior versioned-KG "
    "systems target SPARQL knowledge management, not the distinct requirements "
    "of AI-agent memory: typed dependency edges encoding *epistemic* "
    "(not just ontological) relationships, mutable tag pointers for belief "
    "status, asynchronous LLM-driven consolidation, and AGM correspondence "
    "[@Park2026Kumiho, Sec. 2.3].",
    title="Theory: versioned KGs exist but target SPARQL, not agent-memory belief revision",
)

claim_gcc_text_versioning = claim(
    "**Git-Context-Controller (GCC) [@GCC2025] applies Git semantics (COMMIT, "
    "BRANCH, MERGE) to LLM agent memory at the text-file level, achieving "
    "strong SWE-Bench-Lite results.** Kumiho differs by operating on typed "
    "knowledge-graph triples rather than text files, enabling formal "
    "belief-revision properties and typed dependency reasoning that flat "
    "text-level version control cannot express [@Park2026Kumiho, Sec. 2.3].",
    title="Theory: GCC applies Git to text files; Kumiho applies graph primitives to typed triples",
)

# ---------------------------------------------------------------------------
# 2.4 Hybrid retrieval and score fusion
# ---------------------------------------------------------------------------

claim_bm25_history = claim(
    "**Robertson and Zaragoza [@RobertsonZaragoza2009BM25] formalized BM25**; "
    "Cormack et al. [@Cormack2009RRF] introduced Reciprocal Rank Fusion (RRF). "
    "Bruch et al. [@Bruch2023Fusion] analyzed fusion functions systematically, "
    "showing that convex combinations can outperform RRF on standard IR "
    "benchmarks. Kumiho's max-based fusion -- CombMAX in the terminology of "
    "Fox and Shaw [@FoxShaw1993] -- is a deliberate design choice motivated "
    "by precision preservation, not a novel fusion method "
    "[@Park2026Kumiho, Sec. 2.4].",
    title="Theory: hybrid-retrieval fusion landscape (BM25, RRF, convex, CombMAX)",
)

claim_combmax_caveat = claim(
    "**CombMAX is known to be susceptible to noise from poorly-calibrated "
    "retrievers producing inflated scores [@Bruch2023Fusion].** Kumiho's "
    "$\\beta=0.85$ calibration factor partially mitigates this for vector "
    "scores but has not been empirically validated; sensitivity analysis "
    "comparing against RRF and convex combination is acknowledged as future "
    "work [@Park2026Kumiho, Sec. 2.4; Sec. 8.5.2; Sec. 16].",
    title="Caveat: CombMAX is susceptible to score-inflation noise; comparative analysis pending",
)

# ---------------------------------------------------------------------------
# 2.5 AI agent observability
# ---------------------------------------------------------------------------

claim_observability_gap = claim(
    "**Existing AI-agent observability tools (OpenTelemetry, Langfuse, "
    "LangSmith, Braintrust) trace inference -- not memory.** Kumiho's "
    "contribution differs: the system makes *memory itself* the auditable "
    "artifact. Every agent belief has a URI, a revision history, provenance "
    "edges to source evidence, and an immutable audit trail. The web "
    "dashboard and desktop asset browser render this graph as a browsable, "
    "searchable hierarchy with interactive visualization, enabling human "
    "operators to audit agent reasoning at the *memory* level, not just at "
    "the tool-call level [@Park2026Kumiho, Sec. 2.5].",
    title="Diagnosis: existing observability tools trace inference, not memory",
)

# ---------------------------------------------------------------------------
# Section 3: Why context-window extension is not memory (4 deficiencies)
# ---------------------------------------------------------------------------

claim_attention_not_recall = claim(
    "**Deficiency 1 -- attention is not recall.** A context window provides "
    "attention capacity; memory requires *selective recall* from a large "
    "corpus of past experience [@Park2026Kumiho, Sec. 3].",
    title="Deficiency 1: attention != recall",
)

claim_quadratic_cost_scaling = claim(
    "**Deficiency 2 -- quadratic cost scaling.** Transformer attention scales "
    "as $\\Theta(n^2 \\cdot d)$ [@Vaswani2017Attention]; a retrieval-based "
    "system indexing $N$ memories and retrieving top-$k$ incurs only "
    "$O(\\log N) + O(k^2 \\cdot d)$. Since $k \\ll n$ by design, retrieval is "
    "orders of magnitude cheaper. Sparse attention, sliding windows, and "
    "linear-attention approximations mitigate cost only by sacrificing the "
    "ability to attend to arbitrary positions -- precisely what makes large "
    "windows useful [@Park2026Kumiho, Sec. 3].",
    title="Deficiency 2: attention scales O(n^2*d) vs retrieval's O(log N + k^2*d)",
)

claim_no_structural_representation = claim(
    "**Deficiency 3 -- no structural representation.** A flat token sequence "
    "cannot express that belief $B_2$ supersedes $B_1$, that conclusion $C$ "
    "depends on assumptions $A_1, A_2$, or that a memory has been validated, "
    "deprecated, or flagged for review [@Park2026Kumiho, Sec. 3].",
    title="Deficiency 3: token sequences have no structural representation",
)

claim_model_coupling = claim(
    "**Deficiency 4 -- model coupling.** Context-window contents are ephemeral "
    "and model-specific. Agent memory must be LLM-decoupled: stored in a "
    "persistent, model-independent data structure that any current or future "
    "language model can query [@Park2026Kumiho, Sec. 3].",
    title="Deficiency 4: context-window contents are model-coupled and ephemeral",
)

__all__ = [
    "setup_locomo_benchmark",
    "setup_locomo_plus_benchmark",
    "setup_human_memory_template",
    "claim_graphiti_components",
    "claim_mem0_components",
    "claim_letta_components",
    "claim_amem_components",
    "claim_magma_components",
    "claim_hindsight_components",
    "claim_memos_components",
    "claim_table1_comparison",
    "claim_benchmark_standardization_caveat",
    "claim_agm_lineage",
    "claim_flouris_dl_impossibility",
    "claim_agm_ml_correspondences",
    "claim_recovery_critiques",
    "claim_versioned_kg_lineage",
    "claim_gcc_text_versioning",
    "claim_bm25_history",
    "claim_combmax_caveat",
    "claim_observability_gap",
    "claim_attention_not_recall",
    "claim_quadratic_cost_scaling",
    "claim_no_structural_representation",
    "claim_model_coupling",
]
