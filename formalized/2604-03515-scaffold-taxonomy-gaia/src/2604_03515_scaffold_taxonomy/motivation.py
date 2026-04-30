"""Motivation: a source-code taxonomy of coding-agent architectures.

Formalisation of arXiv:2604.03515 ("Inside the Scaffold: A Source-Code
Taxonomy of Coding Agent Architectures"). The source artifact in this
package is a thin stub (title + arXiv link + GitHub link to
`aorwall/moatless-tools` + keyword list + a two-sentence abstract); no PDF
body is available. Therefore only the abstract-level conclusions and the
explicit keyword claims are formalised here.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

coding_agent_setting = setting(
    "A *coding agent* is an LLM-driven system whose task is to read, edit, and "
    "execute source code in pursuit of a user-specified software-engineering "
    "goal (bug fix, feature implementation, refactor, etc.). The *scaffold* of "
    "such an agent is the source-code-level harness that wraps the underlying "
    "LLM: the prompt-and-loop control flow, the set of callable tools, the "
    "memory / context-management discipline, and the agent's persistent state "
    "machine. Different open-source coding agents (Aider, OpenDevin, SWE-agent, "
    "Cline, moatless-tools, ...) instantiate this scaffold in materially "
    "different ways, and those differences are observable directly in the "
    "implementation source.",
    title="Coding-agent scaffold (formal setting)",
)

study_scope = setting(
    "The study scope is a corpus of real-world open-source coding-agent "
    "implementations, examined at the source-code level. The reference "
    "implementation cited via the GitHub link is "
    "https://github.com/aorwall/moatless-tools; the taxonomy is derived by "
    "comparing scaffold designs across this and analogous projects rather than "
    "by running them on benchmarks.",
    title="Study population: open-source coding-agent source code",
)

# ---------------------------------------------------------------------------
# Headline abstract claims (the 2 sentences of the abstract)
# ---------------------------------------------------------------------------

source_code_taxonomy_built = claim(
    "The work delivers a **source-code taxonomy of coding-agent "
    "architectures** -- a structured classification of how coding agents are "
    "built, derived from inspection of their implementation source rather "
    "than from black-box behavioural evaluation.",
    title="Source-code taxonomy of coding-agent architectures",
    metadata={"source": "artifacts/2604.03515-scaffold-taxonomy.md (abstract, sentence 1)"},
)

structural_patterns_derived = claim(
    "The work **analyses real-world implementations to derive structural "
    "patterns** in how coding agents manage **context, tools, and state** -- "
    "i.e. the taxonomy categories are grounded in repeated design choices "
    "observed across multiple existing agent codebases, not synthesised "
    "top-down.",
    title="Structural patterns derived from real-world implementations",
    metadata={"source": "artifacts/2604.03515-scaffold-taxonomy.md (abstract, sentence 2)"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 5 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim of the form "this paper provides a taxonomic treatment of X".
# ---------------------------------------------------------------------------

keyword_agentic_memory = claim(
    "The taxonomy provides a treatment of **agentic memory** in coding "
    "agents -- how implementations represent, persist, and recall information "
    "across reasoning steps (e.g. scratchpads, episodic logs, retrieval over "
    "prior trajectories, long-term knowledge stores).",
    title="Keyword: agentic memory",
    metadata={"keyword_index": 1, "source": "artifacts/2604.03515-scaffold-taxonomy.md (keywords)"},
)

keyword_loop_primitives = claim(
    "The taxonomy provides a treatment of **loop primitives** -- the "
    "control-flow building blocks (think/act/observe loops, plan-then-execute "
    "loops, reflexion loops, hierarchical sub-task loops) that scaffold the "
    "agent's outer reasoning cycle.",
    title="Keyword: loop primitives",
    metadata={"keyword_index": 2, "source": "artifacts/2604.03515-scaffold-taxonomy.md (keywords)"},
)

keyword_context_compaction = claim(
    "The taxonomy provides a treatment of **context compaction** -- the "
    "techniques (summarisation, truncation, selective retention, hierarchical "
    "rollups) that coding agents use to fit their working context into the "
    "underlying model's bounded window as a session grows.",
    title="Keyword: context compaction",
    metadata={"keyword_index": 3, "source": "artifacts/2604.03515-scaffold-taxonomy.md (keywords)"},
)

keyword_tool_capability_categories = claim(
    "The taxonomy provides a treatment of **tool capability categories** -- "
    "the classes of capabilities that coding-agent tools expose (file I/O, "
    "code search, edit/patch application, shell execution, test running, "
    "version control, browser/web access, ...) and how scaffolds organise and "
    "expose them.",
    title="Keyword: tool capability categories",
    metadata={"keyword_index": 4, "source": "artifacts/2604.03515-scaffold-taxonomy.md (keywords)"},
)

keyword_state_management = claim(
    "The taxonomy provides a treatment of **state management** -- how coding "
    "agents track in-progress task state, edit history, open files, planning "
    "artefacts, and recovery checkpoints across the lifetime of a "
    "conversation or task.",
    title="Keyword: state management",
    metadata={"keyword_index": 5, "source": "artifacts/2604.03515-scaffold-taxonomy.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two abstract sentences jointly grant evidence to each of the five
# keyword-topic claims: a source-code-level taxonomy that derives structural
# patterns over context, tools, and state is *the kind of work* that
# necessarily covers each of agentic memory, loop primitives, context
# compaction, tool-capability categories, and state management.

strat_taxonomy_covers_memory = support(
    [source_code_taxonomy_built, structural_patterns_derived],
    keyword_agentic_memory,
    background=[coding_agent_setting, study_scope],
    reason=(
        "A source-code taxonomy (@source_code_taxonomy_built) that derives "
        "structural patterns from how real implementations manage context "
        "(@structural_patterns_derived) necessarily examines how those "
        "implementations represent and persist information across steps. "
        "Within the coding-agent scaffold (@coding_agent_setting) over the "
        "surveyed corpus (@study_scope), that subject is exactly agentic "
        "memory."
    ),
    prior=0.88,
)

strat_taxonomy_covers_loops = support(
    [source_code_taxonomy_built, structural_patterns_derived],
    keyword_loop_primitives,
    background=[coding_agent_setting, study_scope],
    reason=(
        "Classifying coding-agent architectures at the source level "
        "(@source_code_taxonomy_built) and abstracting structural patterns "
        "across implementations (@structural_patterns_derived) requires "
        "naming the recurring outer-loop control-flow primitives. Given the "
        "scaffold setting (@coding_agent_setting) and the surveyed corpus "
        "(@study_scope), loop primitives fall directly out of that exercise."
    ),
    prior=0.92,
)

strat_taxonomy_covers_compaction = support(
    [source_code_taxonomy_built, structural_patterns_derived],
    keyword_context_compaction,
    background=[coding_agent_setting],
    reason=(
        "The abstract explicitly highlights *context* as one of the three "
        "axes along which structural patterns are derived "
        "(@structural_patterns_derived). At the source-code level "
        "(@source_code_taxonomy_built), the principal differentiator across "
        "coding-agent scaffolds (@coding_agent_setting) on the context axis "
        "is how they compact long-running context into a bounded window. "
        "Hence the taxonomy materially covers context compaction."
    ),
    prior=0.9,
)

strat_taxonomy_covers_tool_categories = support(
    [source_code_taxonomy_built, structural_patterns_derived],
    keyword_tool_capability_categories,
    background=[coding_agent_setting, study_scope],
    reason=(
        "*Tools* is the second of the three axes in the abstract "
        "(@structural_patterns_derived). A source-code taxonomy "
        "(@source_code_taxonomy_built) over real coding-agent codebases "
        "(@study_scope) cannot describe tools without grouping the concrete "
        "tool calls those scaffolds (@coding_agent_setting) expose into "
        "capability categories. The keyword claim follows directly."
    ),
    prior=0.93,
)

strat_taxonomy_covers_state = support(
    [source_code_taxonomy_built, structural_patterns_derived],
    keyword_state_management,
    background=[coding_agent_setting, study_scope],
    reason=(
        "*State* is the third axis named in the abstract "
        "(@structural_patterns_derived). A source-code taxonomy "
        "(@source_code_taxonomy_built) of how coding-agent scaffolds "
        "(@coding_agent_setting) handle state across implementations "
        "(@study_scope) is, by construction, a treatment of state "
        "management."
    ),
    prior=0.93,
)

__all__ = [
    "coding_agent_setting",
    "study_scope",
    "source_code_taxonomy_built",
    "structural_patterns_derived",
    "keyword_agentic_memory",
    "keyword_loop_primitives",
    "keyword_context_compaction",
    "keyword_tool_capability_categories",
    "keyword_state_management",
]
