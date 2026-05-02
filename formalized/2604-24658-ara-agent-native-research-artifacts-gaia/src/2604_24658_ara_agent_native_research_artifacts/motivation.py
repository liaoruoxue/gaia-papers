"""Motivation: agent-native research artifacts (ARA).

Formalisation of arXiv:2604.24658 ("ARA: Agent-Native Research Artifacts").
The source artifact in this package is a thin stub (title + arXiv link +
three-keyword list + status line); no PDF body is available. Therefore only
the title-level thesis claim, its companion method claim, and the three
listed keyword topics are extracted as claims.

The H1 of the artifact -- "ARA: Agent-Native Research Artifacts" -- is split
into two title-level leaves under the standard 'METHOD: thesis' convention:
(i) the thesis that research artifacts (papers, datasets, code, results)
should be **agent-native** -- i.e. natively consumable, queryable, and
composable by LLM-based research agents rather than retrofitted from
human-facing PDFs; and (ii) the companion claim that **ARA** is the
framework / artifact-format proposed by the authors to realise that
thesis. The three keywords name the supporting mechanism: (1)
**paper-agentification** is the act of turning a paper into an agent-usable
artifact, (2) **arm** (Agent-native Research Module / artifact, depending on
gloss) is the unit of agent-native packaging, and (3)
**knowledge-representation** is the underlying technical axis -- ARA is
ultimately a knowledge-representation proposal about how scientific
contributions should be encoded so that agents can reason over them.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

research_artifact_setting = setting(
    "A *research artifact* is any concrete output of a scientific or "
    "engineering investigation -- a paper, a dataset, a code release, a "
    "benchmark, a notebook, a result table, a model checkpoint, a "
    "specification, etc. Historically these artifacts are produced primarily "
    "for **human** consumers: PDFs are typeset for reading, code is "
    "documented in natural-language READMEs, datasets are described in "
    "data-cards. As LLM-based **research agents** (literature-review agents, "
    "experiment-running agents, replication agents, meta-analysis agents) "
    "become first-class consumers of these artifacts, the human-facing "
    "encoding becomes a bottleneck: agents must re-extract structure from "
    "PDFs, reverse-engineer schemas from prose, and infer provenance that "
    "humans take for granted.",
    title="Research artifacts and their consumers (formal setting)",
)

agent_native_scope = setting(
    "An artifact is *agent-native* when its primary distribution form is "
    "directly machine-readable by LLM-based agents: claims, methods, "
    "datasets, results, and citations are exposed as typed, addressable, "
    "composable units (rather than as flat prose embedded in a PDF) so that "
    "an agent can query, cite, compose, and reason over them without first "
    "having to parse a human-facing rendering. The study scope of ARA is the "
    "design and packaging discipline that produces such artifacts -- i.e. "
    "what the unit of packaging is, what its schema is, and how it composes "
    "with other artifacts in an agent's working context.",
    title="Agent-native artifacts (study scope)",
)

# ---------------------------------------------------------------------------
# Headline title-level claims (the H1 of the artifact)
# ---------------------------------------------------------------------------

artifacts_should_be_agent_native = claim(
    "Research artifacts should be **agent-native** -- i.e. their primary "
    "distribution form should be directly consumable by LLM-based research "
    "agents (typed, addressable, composable units exposing claims, methods, "
    "data, and provenance), rather than human-facing PDFs from which agents "
    "must re-extract structure. The current PDF-first regime is a "
    "first-order bottleneck for agent-driven science.",
    title="Central thesis: research artifacts should be agent-native",
    metadata={"source": "artifacts/2604.24658-ara-agent-native-research-artifacts.md (H1 / title)"},
)

ara_realises_agent_native_artifacts = claim(
    "**ARA** -- the framework named in the title -- is proposed as the "
    "concrete realisation of agent-native research artifacts: it specifies "
    "the unit of packaging, the schema by which claims / methods / data / "
    "provenance are exposed, and the composition discipline that lets a "
    "research agent consume, cite, and compose ARA-packaged artifacts "
    "without going through a human-facing rendering.",
    title="ARA realises agent-native research artifacts",
    metadata={"source": "artifacts/2604.24658-ara-agent-native-research-artifacts.md (title: 'ARA:')"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 3 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim that ties back to the central thesis.
# ---------------------------------------------------------------------------

keyword_paper_agentification = claim(
    "The work develops **paper-agentification** -- the discipline of turning "
    "a conventional human-facing research paper into an agent-consumable "
    "artifact (extracting its claims, methods, results, and citations into "
    "the typed, addressable, composable form an LLM-based agent can query "
    "and reason over). Paper-agentification is the operational verb that "
    "produces an ARA artifact from a legacy PDF.",
    title="Keyword: paper-agentification",
    metadata={"keyword_index": 1, "source": "artifacts/2604.24658-ara-agent-native-research-artifacts.md (keywords)"},
)

keyword_arm = claim(
    "The work introduces **ARM** -- the Agent-native Research Module / "
    "artifact -- as the unit of packaging that the ARA framework produces: "
    "an ARM bundles the claims, evidence, methods, and provenance of a "
    "research contribution in a single addressable, composable unit that an "
    "agent can load, cite, and compose with other ARMs.",
    title="Keyword: ARM (agent-native research module/artifact)",
    metadata={"keyword_index": 2, "source": "artifacts/2604.24658-ara-agent-native-research-artifacts.md (keywords)"},
)

keyword_knowledge_representation = claim(
    "The work is, at its technical core, a **knowledge-representation** "
    "proposal: ARA / ARM specify how scientific contributions are encoded "
    "(claim graphs, typed evidence links, provenance, composition rules) so "
    "that LLM-based agents can do faithful reasoning over them. The "
    "paper-agentification process and the ARM unit are both expressions of "
    "that underlying KR design.",
    title="Keyword: knowledge representation",
    metadata={"keyword_index": 3, "source": "artifacts/2604.24658-ara-agent-native-research-artifacts.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two title-level leaf claims jointly grant evidence to each of the three
# keyword claims: the central agent-native thesis grounds the
# paper-agentification activity and the underlying knowledge-representation
# concern, while the ARA-as-framework claim grounds the ARM unit-of-packaging.

strat_thesis_grounds_paper_agentification = support(
    [artifacts_should_be_agent_native, ara_realises_agent_native_artifacts],
    keyword_paper_agentification,
    background=[research_artifact_setting, agent_native_scope],
    reason=(
        "If research artifacts ought to be agent-native "
        "(@artifacts_should_be_agent_native) and ARA is the proposed "
        "framework that realises that ideal "
        "(@ara_realises_agent_native_artifacts), then converting the "
        "existing legacy stock of human-facing papers "
        "(@research_artifact_setting) into ARA-packaged form "
        "(@agent_native_scope) is the unavoidable operational verb. That "
        "verb is precisely 'paper-agentification'."
    ),
    prior=0.92,
)

strat_framework_grounds_arm = support(
    [ara_realises_agent_native_artifacts],
    keyword_arm,
    background=[research_artifact_setting, agent_native_scope],
    reason=(
        "Any concrete realisation of agent-native artifacts "
        "(@ara_realises_agent_native_artifacts) must commit to a unit of "
        "packaging -- the smallest addressable, composable bundle an agent "
        "loads, cites, and reuses (@agent_native_scope) within the broader "
        "research-artifact landscape (@research_artifact_setting). That "
        "unit, in the authors' nomenclature signalled by the keyword list, "
        "is the ARM."
    ),
    prior=0.93,
)

strat_thesis_grounds_knowledge_representation = support(
    [artifacts_should_be_agent_native, ara_realises_agent_native_artifacts],
    keyword_knowledge_representation,
    background=[agent_native_scope],
    reason=(
        "Specifying *how* scientific contributions are encoded so that "
        "agents can faithfully reason over them (@agent_native_scope) is, by "
        "definition, a knowledge-representation problem. Both the "
        "agent-native thesis (@artifacts_should_be_agent_native) and the "
        "concrete ARA realisation (@ara_realises_agent_native_artifacts) "
        "are statements at that KR layer -- they prescribe the schema of "
        "claims, evidence, methods, and provenance, not merely a file "
        "format. Hence the work is squarely a knowledge-representation "
        "proposal."
    ),
    prior=0.9,
)

__all__ = [
    "research_artifact_setting",
    "agent_native_scope",
    "artifacts_should_be_agent_native",
    "ara_realises_agent_native_artifacts",
    "keyword_paper_agentification",
    "keyword_arm",
    "keyword_knowledge_representation",
]
