"""Motivation: the two structural costs of compiling research into narrative.

Section 1 (Introduction) of Liu et al. 2026 [@Liu2026ARA]. Frames the
research process as a rich, branching knowledge object that publication
compresses into a linear narrative, imposing two structural costs:

1. **Storytelling Tax** -- failed experiments, rejected hypotheses, and
   the branching exploration are discarded to fit a linear narrative.
2. **Engineering Tax** -- the gap between reviewer-sufficient prose and
   agent-sufficient specification leaves critical implementation details
   unwritten.

These costs are tolerable for human readers but become *critical* when
AI agents must understand, reproduce, and extend published work. The
paper introduces the Agent-Native Research Artifact (ARA) protocol as
the structural response.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Background settings: working definitions
# ---------------------------------------------------------------------------

setup_research_object = setting(
    "**Research as a branching knowledge object.** Research produces a "
    "rich, branching knowledge object: months of hypotheses tested and "
    "rejected, implementation tricks discovered through trial and error, "
    "design alternatives weighed against each other, and the full "
    "exploration trajectory that explains *why* the final approach was "
    "chosen [@Kuhn1962; @Medawar1963]. The 'final result' is a narrow "
    "summary of this branching object.",
    title="Setup: research as a branching, iterative knowledge object",
)

setup_publication_compilation = setting(
    "**Publication compiles the research object into linear narrative.** "
    "The act of publishing translates the branching research object into "
    "a linear narrative document (PDF + optional code repository) "
    "[@Medawar1963; @Canini2026]. The narrative format is a *compilation* "
    "convention: it is independent of any particular file format and "
    "dictates which pieces of the underlying research object survive into "
    "the published artifact.",
    title="Setup: publication = compilation of research object into narrative",
)

setup_two_audiences = setting(
    "**Research artifacts have two distinct consumer classes.** Two "
    "audience types now consume research artifacts: (i) human readers, "
    "whose attention is bandwidth-limited (skim abstracts, scan figures, "
    "rarely engage with supplementary material) [@Renear2009]; and "
    "(ii) AI agents, who can read papers, reproduce experiments, and "
    "extend methods at machine bandwidth [@Lu2024AIScientist]. Their "
    "information needs are fundamentally divergent: human attention is "
    "scarce; agents benefit from exhaustive detail.",
    title="Setup: two distinct consumer classes (humans vs AI agents)",
)

setup_tacit_knowledge = setting(
    "**Tacit knowledge.** Tacit knowledge [@Polanyi1966] is knowledge "
    "transmitted only through direct lab contact or painstaking "
    "reverse-engineering -- algorithmic tricks, implementation decisions, "
    "configuration choices that exist in no written document. It is the "
    "category of knowledge most systematically discarded by narrative "
    "compilation, because its insertion into prose would not change the "
    "reviewer's verdict but is essential for an agent's execution.",
    title="Setup: tacit knowledge (Polanyi 1966)",
)

# ---------------------------------------------------------------------------
# Central research question
# ---------------------------------------------------------------------------

q_central = question(
    "When AI agents are first-class consumers of scientific work --"
    " reading, reproducing, and extending published research -- what"
    " structural form should the primary research artifact take, and how"
    " should the surrounding ecosystem (authoring, compilation, review)"
    " be organized so that the artifact can be operated by agents at"
    " machine bandwidth without imposing additional documentation"
    " burden on researchers?",
    title="Central question: what is the right artifact format for agent-native research?",
)

# ---------------------------------------------------------------------------
# Two empirical observations that motivate the diagnosis
# ---------------------------------------------------------------------------

claim_o4_pdf_information_gap = claim(
    "**Empirical observation O4: PDF information gap is systematic.** "
    "Across the 23 PaperBench papers (8,921 expert-authored "
    "reproduction-rubric requirements [@Starace2025PaperBench]), only "
    "**45.4%** of reproduction requirements are fully specified in the "
    "source PDF; **50.2%** are partially specified and **4.4%** are "
    "absent. The gap is dominated by code-development tasks (37.3% "
    "sufficient) and is structural rather than driven by outliers "
    "(median paper: 45.3% sufficient).\n\n"
    "| Task category | Reqs | Sufficient | Partial | Absent |\n"
    "|---|---:|---:|---:|---:|\n"
    "| Code Development | 3,942 | 37.3% | 54.9% | 7.8% |\n"
    "| Code Execution | 4,355 | 50.5% | 47.9% | 1.6% |\n"
    "| Result Analysis | 624 | 60.6% | 36.9% | 2.6% |\n"
    "| **Overall** | **8,921** | **45.4%** | **50.2%** | **4.4%** |\n",
    title="O4: 54.6% of reproduction requirements partial or absent from PDFs",
    metadata={"source_figure": "Fig. 3a (artifacts/2604.24658.pdf, p. 3); Table 8 (App. E.2)"},
)

claim_o5_exploration_tax = claim(
    "**Empirical observation O5: exploration cost is overwhelmingly "
    "wasted under the current artifact format.** Across **24,008** agent "
    "runs from the METR MALT corpus on RE-Bench [@Wijk2025REBench] "
    "(21 frontier models, 228 tasks), failed runs that did not reach the "
    "reference score account for **90.2%** of total dollar cost ($63,483 "
    "in absolute terms) and **59.2%** of total tokens. The median "
    "failed-to-success token ratio per run is **113×**. Within the 59.2% "
    "wasted-token share, 44.8% map dead ends and 14.4% re-derive "
    "solutions other agents had already produced. Below-reference rate "
    "concentrates on the most open-ended (research-like) tasks: 73.4% "
    "for RE-Bench vs 47.0% for moderate-difficulty HCAST and 0.7% for "
    "well-defined SWAA.",
    title="O5: 90.2% of dollar cost on RE-Bench is below-reference exploration",
    metadata={"source_table": "Table 10 (artifacts/2604.24658.pdf, App. E.3)"},
)

claim_o3_frontier_llms_fail = claim(
    "**Empirical observation O3: frontier LLMs fail on research "
    "implementation.** Even the strongest frontier LLMs correctly "
    "implement fewer than **40%** of novel research contributions when "
    "given the full paper PDF and the companion code repository "
    "[@Hua2025ResearchCodeBench]; on EXP-Bench, end-to-end experiment "
    "success is only **0.5%** despite 20-35% accuracy on individual "
    "components [@Kon2025EXPBench]. The dominant failure mode is "
    "*semantic misalignment* between paper-described intent and "
    "code-realized behaviour [@Jimenez2024SWEbench; @Chen2025ScienceAgentBench].",
    title="O3: frontier LLMs implement <40% of novel research contributions correctly",
)

# ---------------------------------------------------------------------------
# Two structural costs (the diagnosis)
# ---------------------------------------------------------------------------

claim_storytelling_tax = claim(
    "**The Storytelling Tax: narrative compilation systematically erases "
    "research-process knowledge.** Research does not proceed linearly: it "
    "branches, backtracks, and accumulates failure knowledge before "
    "converging on a publishable result [@Kuhn1962; @Medawar1963]. "
    "Narrative compilation flattens this DAG into a polished linear "
    "story, **discarding every failed experiment, rejected hypothesis, "
    "and abandoned approach** along with the human-judgment trajectory "
    "(rejections, revisions, endorsements) that produced the final "
    "version [@Rosenthal1979; @Franco2014]. Although modern platforms "
    "archive *final* artifacts, the *branching process* remains "
    "unrecorded, causing independent rediscovery of the same dead ends "
    "across groups.",
    title="Storytelling Tax: narrative erases the branching research process",
    metadata={"source_figure": "Fig. 2 (artifacts/2604.24658.pdf, p. 3)"},
)

claim_engineering_tax = claim(
    "**The Engineering Tax: the gap between reviewer-sufficient prose "
    "and agent-sufficient specification.** A paper communicates its "
    "contribution at the level of detail needed to convince a human "
    "reviewer; the codebase provides an implementation but not the "
    "operational *specification* needed to execute it. Between the two "
    "lies tacit knowledge [@Polanyi1966] -- algorithmic tricks, "
    "implementation decisions, configuration choices -- that exists in "
    "no written document and is transmitted only through direct lab "
    "contact or painstaking reverse-engineering. The mismatch is "
    "fundamental: the precision needed to *produce belief* (reviewer "
    "judgment) is lower than the precision needed to *produce correct "
    "execution* (agent operation) [@Stodden2016; @Baker2016].",
    title="Engineering Tax: prose-vs-specification gap leaves implementation details unwritten",
    metadata={"source_figure": "Fig. 3 (artifacts/2604.24658.pdf, p. 3)"},
)

claim_taxes_critical_for_agents = claim(
    "**Both taxes are critical when consumers are AI agents.** The "
    "Storytelling and Engineering Taxes are *tolerable* for human "
    "readers, who exercise judgment, can extrapolate from sparse "
    "specification, and can tolerate missing failures because they read "
    "for understanding rather than reproduction. They become *critical* "
    "for AI agents that must (i) understand a field, (ii) reproduce "
    "experiments to validate findings, and (iii) extend published "
    "methods to new settings [@Lu2024AIScientist] -- each task requires "
    "precisely the knowledge that compilation discards.",
    title="The taxes are critical (not merely undesirable) for agent consumers",
)

# ---------------------------------------------------------------------------
# Three trends that make agent-native artifacts feasible
# ---------------------------------------------------------------------------

claim_trend1_ai_native_research = claim(
    "**Trend 1: AI agents have become indispensable research "
    "companions.** Coding agents now co-author code, run experiments, "
    "and iterate on hypotheses alongside human researchers "
    "[@Lu2024AIScientist]. LLM adoption is associated with paper "
    "production increases of **23.7%-89.3%** across scientific fields "
    "[@Kusumegi2025]. As a structural consequence, the full research "
    "trajectory (every failure, implementation trick, configuration "
    "choice, design pivot) is already captured as machine-readable text "
    "in researcher-agent coding sessions. The raw material exists as a "
    "*natural byproduct* of the research process, lacking only a "
    "protocol to systematically preserve it as a first-class output.",
    title="Trend 1: AI-agent-mediated research makes the full trajectory machine-readable",
)

claim_trend2_divergent_audiences = claim(
    "**Trend 2: humans and AI agents have fundamentally divergent "
    "information needs.** Human attention is scarce: readers skim "
    "abstracts, scan figures, and rarely engage with supplementary "
    "material [@Renear2009]. AI agents, by contrast, benefit from "
    "exhaustive detail; *more context strictly improves* their ability "
    "to reproduce, verify, and extend prior work. A single artifact "
    "optimized for human narrative cannot serve both audiences without "
    "compromise on at least one side.",
    title="Trend 2: humans optimize for low context; agents benefit from exhaustive context",
)

claim_trend3_operability = claim(
    "**Trend 3: research is scaling into a massively parallel enterprise "
    "where agents fork, extend, and merge each other's work at machine "
    "speed.** The bottleneck of scientific progress is shifting from "
    "individual productivity to the **operability** of the artifacts "
    "being shared. Narrative PDFs, compiled for sequential human "
    "reading, cannot be forked, diffed, or merged; a structured, "
    "lossless artifact can, enabling research to compound like software "
    "[@Wang2026ArtifactExchange].",
    title="Trend 3: operability of artifacts becomes the new bottleneck",
)

# ---------------------------------------------------------------------------
# Headline contributions (previewed; details in s5-s8)
# ---------------------------------------------------------------------------

claim_contrib_diagnose_two_taxes = claim(
    "**Contribution 1 (diagnosis).** The paper identifies the two "
    "structural costs of compiling research into narrative -- the "
    "**Storytelling Tax** (research-process erasure) and the "
    "**Engineering Tax** (prose-vs-specification gap) -- and argues that "
    "both become critical exactly when AI agents are first-class "
    "consumers of research [@Liu2026ARA].",
    title="Contribution 1: name and characterize the Storytelling and Engineering Taxes",
)

claim_contrib_ara_protocol = claim(
    "**Contribution 2 (the ARA protocol).** The paper introduces the "
    "**Agent-Native Research Artifact (ARA)**: a file-system-level "
    "protocol that recasts the primary research object from narrative "
    "document to agent-executable knowledge package, organized into "
    "**four interlocking layers** -- Cognitive (`/logic`), Physical "
    "(`/src`), Exploration Graph (`/trace`), and Evidence (`/evidence`) "
    "-- with cross-layer **forensic bindings** linking claims to code "
    "to evidence (Figure 4).",
    title="Contribution 2: the four-layer ARA protocol",
    metadata={"source_figure": "Fig. 4 (artifacts/2604.24658.pdf, p. 4)"},
)

claim_contrib_three_mechanisms = claim(
    "**Contribution 3 (three enabling mechanisms).** The paper develops "
    "three mechanisms that operate the ARA ecosystem: a **Live Research "
    "Manager** (§3) that captures research decisions and dead ends as a "
    "byproduct of normal AI-native development; an **ARA Compiler** (§4) "
    "that translates legacy PDFs and repositories into ARA format; and "
    "an **ARA-Native Review System** (§5) that automates objective "
    "verification (analogous to a grammar checker for prose) so human "
    "reviewers focus on significance, novelty, and taste.",
    title="Contribution 3: Live Research Manager + ARA Compiler + Review System",
)

claim_contrib_empirical_results = claim(
    "**Contribution 4 (empirical evaluation).** Across PaperBench "
    "[@Starace2025PaperBench] and RE-Bench [@Wijk2025REBench], agents "
    "operating on an ARA outperform agents reading PDF + companion "
    "GitHub on **all three** layers of research utility: question-"
    "answering accuracy rises from **72.4% to 93.7%** "
    "(Δ=+21.3pp, McNemar χ²=95.15, p<10⁻¹⁰); difficulty-weighted "
    "reproduction success from **57.4% to 64.4%** (Wilcoxon p=0.028, "
    "8/5/2 win/tie/loss); and on five RE-Bench extension tasks, "
    "preserved failure traces accelerate progress, though they can also "
    "constrain a sufficiently-capable model from stepping outside the "
    "documented playbook.",
    title="Contribution 4: ARA wins on understanding, reproduction, extension",
)

# ---------------------------------------------------------------------------
# Counter-hypotheses to the central thesis
# ---------------------------------------------------------------------------

claim_alt_agent_capability_insufficient = claim(
    "**Alternative explanation Alt-A: agents are insufficient regardless "
    "of artifact format.** A natural alternative to the two-tax "
    "diagnosis is that current LLM-based agents cannot reproduce or "
    "extend research because *agent capability* (reasoning, tool use, "
    "long-horizon planning) is the binding constraint, and improving "
    "the artifact format yields little marginal gain on top of stronger "
    "models [@Jimenez2024SWEbench; @Chen2025ScienceAgentBench]. Under "
    "this view, the paper's measured ARA-vs-PDF gap should narrow as "
    "agents improve and disappear at the limit -- a falsifiable "
    "competing prediction.",
    title="Alt-A: 'agents are insufficient' (capability-bound, not artifact-bound)",
)

claim_prevailing_norm_pdfs_sufficient = claim(
    "**Prevailing norm: narrative PDFs are sufficient for scientific "
    "communication.** The status-quo view in the scientific publishing "
    "ecosystem -- consistent with the FAIR data principles "
    "[@Wilkinson2016FAIR], the existing reproducibility infrastructure "
    "[@Stodden2016; @Pineau2021], and the artifact-evaluation badges of "
    "ACM/IEEE -- holds that a peer-reviewed PDF, supplemented by an "
    "available code repository and (sometimes) a data package, is "
    "structurally adequate as the primary scientific artifact. Quality "
    "is then the responsibility of authors, reviewers, and downstream "
    "implementers rather than of the format itself.",
    title="Prevailing norm: PDF + repo + (optional) data is structurally adequate",
)

__all__ = [
    "setup_research_object",
    "setup_publication_compilation",
    "setup_two_audiences",
    "setup_tacit_knowledge",
    "q_central",
    "claim_o4_pdf_information_gap",
    "claim_o5_exploration_tax",
    "claim_o3_frontier_llms_fail",
    "claim_storytelling_tax",
    "claim_engineering_tax",
    "claim_taxes_critical_for_agents",
    "claim_trend1_ai_native_research",
    "claim_trend2_divergent_audiences",
    "claim_trend3_operability",
    "claim_contrib_diagnose_two_taxes",
    "claim_contrib_ara_protocol",
    "claim_contrib_three_mechanisms",
    "claim_contrib_empirical_results",
    "claim_alt_agent_capability_insufficient",
    "claim_prevailing_norm_pdfs_sufficient",
]
