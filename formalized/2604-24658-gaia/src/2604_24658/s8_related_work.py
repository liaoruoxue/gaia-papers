"""Section 8: Related Work -- machine-readable artifacts, reproducibility,
agent tooling.

Three research threads: machine-readable science, reproducibility
infrastructure, and agent-oriented tooling. ARA's contribution is the
unified protocol that none individually provides; the dimensional
table (Table 5) makes the gap explicit.
"""

from gaia.lang import claim

claim_dimensional_gap_table = claim(
    "**Existing tools cover at most two dimensions structurally; ARA "
    "covers all five (Table 5).** A natural objection is that ARA "
    "merely combines documentation, version control, and experiment "
    "tracking. Even using PDFs + GitHub + trackers (MLflow "
    "[@Zaharia2018MLflow], Weights & Biases [@Biewald2020WandB]) "
    "*simultaneously* leaves the knowledge siloed in three unlinked "
    "formats with no cross-referencing.\n\n"
    "| Dimension | PDF | GitHub | Tracker | ARA |\n"
    "|---|:-:|:-:|:-:|:-:|\n"
    "| Structured scientific logic | ~ | ~ | × | ✓ |\n"
    "| Executable code | × | ✓ | × | ✓ |\n"
    "| Exploration trajectory | × | × | ~ | ✓ |\n"
    "| Grounded evidence | ~ | × | ~ | ✓ |\n"
    "| Cross-layer bindings | × | × | × | ✓ |\n\n"
    "✓ = full; ~ = partial (present but unstructured or scattered); × "
    "= absent. ARA closes the gap not by replacing existing tools but "
    "by providing the **missing structural layer** -- an executable "
    "epistemic graph whose cross-layer bindings make the connections "
    "explicit and machine-traversable.",
    title="Dimensional gap: PDF/GitHub/tracker each cover ≤2 dimensions; ARA covers all 5",
    metadata={"source_table": "Table 5 (artifacts/2604.24658.pdf, p. 17)"},
)

claim_machine_readable_thread = claim(
    "**Machine-readable artifacts thread.** A growing line argues "
    "scientific knowledge should be authored in machine-readable form "
    "during research rather than recovered post-hoc: FAIR principles "
    "[@Wilkinson2016FAIR] standardize data metadata; W3C PROV "
    "[@Lebo2013PROV] formalizes provenance for scientific outputs; "
    "Canini (2026) [@Canini2026] reframes the paper as a *compression "
    "format for human readers* that should yield to structured "
    "knowledge objects; Stocker et al. [@Stocker2025] and Booeshaghi "
    "et al. [@Booeshaghi2026] advocate authoring-time machine-"
    "readability. Concrete formats instantiate parts of this vision: "
    "**nanopublications** [@Groth2010Nanopublications] atomize claims "
    "with provenance; the **Open Research Knowledge Graph** "
    "[@Jaradeh2019ORKG] curates structured contributions across "
    "papers; **RO-Crate** [@SoilandReyes2022ROCrate] bundles research "
    "objects; **Whole Tale** [@Brinckman2019WholeTale] packages "
    "computational environments; the **Discovery Engine** "
    "[@Baulin2025DiscoveryEngine] distills publications into a "
    "Conceptual Tensor. **None provides execution semantics or "
    "captures decision history.** Unlike these formats, ARA jointly "
    "binds scientific logic, minimal executable code, and decision "
    "history into a single protocol with machine-verifiable "
    "reproducibility.",
    title="Machine-readable thread: FAIR/PROV/nanopublications/ORKG/RO-Crate/Whole Tale lack execution + decision history",
)

claim_reproducibility_infra_thread = claim(
    "**Reproducibility infrastructure thread.** The ML reproducibility "
    "crisis [@Baker2016; @Pineau2021] motivated code-sharing standards "
    "[@Stodden2016], scientific workflow engines [@Koster2012Snakemake; "
    "@DiTommaso2017Nextflow; @Crusoe2022CWL], and computational "
    "notebooks [@Knuth1984LiterateProg; @Rule2018Notebooks]. Yet "
    "**workflows encode pipelines without claim semantics**, "
    "**notebooks remain documents with hidden state**, and recent "
    "benchmarks [@Starace2025PaperBench; @Kon2025EXPBench] show "
    "frontier agents cannot recover knowledge PDFs leave implicit -- "
    "EXP-Bench reports only **0.5% end-to-end experiment success** "
    "despite 20-35% component accuracy. On verification, LLMs detect "
    "**fewer than 46%** of paper-code discrepancies "
    "[@Baumgartner2026SciCoQA], extending a longer line of scientific "
    "claim verification [@Wadden2020]. Unlike prior auditing proposals "
    "that address a single dimension, ARA's Seal Certificates "
    "operationalize all of them in one enforceable mechanism.",
    title="Reproducibility infra: workflows lack claim semantics; notebooks have hidden state; agents fail at 0.5%",
)

claim_negative_knowledge_thread = claim(
    "**Negative knowledge and failed-trajectory thread.** Recent work "
    "shows failure traces become *actionable* only once annotated with "
    "root-cause structure [@Zhu2025; @Zhang2025AgenTracer], yet raw "
    "trajectory dumps [@Yang2024SWEAgent] remain difficult to "
    "leverage. Process-level studies [@Wijk2025REBench; "
    "@Yamada2025AIScientistV2] confirm that human experts and agentic "
    "scientists both explore extensive dead ends that never surface in "
    "the write-up. Unlike raw trajectory archives, **ARA's exploration "
    "graph promotes dead ends to first-class `dead_end` nodes with "
    "structured failure modes and claim cross-references**, making "
    "negative knowledge machine-queryable rather than lost to "
    "narrative selection.",
    title="Negative knowledge: ARA promotes dead ends to typed nodes with cross-references",
)

claim_agent_tooling_thread = claim(
    "**Agent-oriented documentation and tooling thread.** Convergent "
    "work shows agents benefit from structured layered representations "
    "[@OpenAI2025AgentsMD; @Vasilopoulos2026CodifiedContext] over flat "
    "corpora, and that the strongest LLMs implement **<40% of novel "
    "contributions correctly**, with semantic misalignment as the "
    "dominant failure [@Jimenez2024SWEbench; "
    "@Chen2025ScienceAgentBench; @Hua2025ResearchCodeBench]. Recent "
    "systems target this gap from three sides: (i) post-hoc paper -> "
    "code generators [@Seo2025Paper2Code; @Li2026TacitKnowledge]; "
    "(ii) knowledge-graph approaches that mine background literature "
    "for technique-code links [@Liu2026KnowledgeGraphs; @Luo2025] -- "
    "yielding up to 10.9% PaperBench gains but leaving the target "
    "contribution's decision history and epistemic structure "
    "*unmodeled*; and (iii) autonomous research agents that conduct "
    "experiments end-to-end [@Boiko2023; @Schmidgall2025AgentLab; "
    "@Lu2024AIScientist], whose unstructured trajectory logs are "
    "themselves discarded once the paper is written. Multi-agent "
    "frameworks [@Wu2024AutoGen], skill-library standards "
    "[@Wang2023Voyager; @Anthropic2025Skills], and artifact-mediated "
    "agent coordination [@Wang2026ArtifactExchange] further show that "
    "**structured artifacts, not natural-language papers, are the "
    "natural unit of exchange for compounding agent capability**. "
    "Unlike post-hoc recovery pipelines and background-knowledge "
    "graphs, ARA encodes claims, evidence, heuristics, and their "
    "executable bindings *at authoring time*, eliminating the recovery "
    "step entirely.",
    title="Agent-tooling thread: structured artifacts > flat corpora; ARA captures at authoring, not post-hoc",
)

__all__ = [
    "claim_dimensional_gap_table",
    "claim_machine_readable_thread",
    "claim_reproducibility_infra_thread",
    "claim_negative_knowledge_thread",
    "claim_agent_tooling_thread",
]
