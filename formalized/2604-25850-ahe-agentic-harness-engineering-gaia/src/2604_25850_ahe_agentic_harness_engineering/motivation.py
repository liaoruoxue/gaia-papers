"""Motivation: agentic harness engineering (AHE).

Formalisation of arXiv:2604.25850 ("AHE: Agentic Harness Engineering").
The source artifact in this package is a thin stub (title + arXiv link +
three-keyword list + status line); no PDF body is available. Therefore only
the title-level thesis claim, its companion method claim, and the three
listed keyword topics are extracted as claims.

The H1 of the artifact -- "AHE: Agentic Harness Engineering" -- is split
into two title-level leaves under the standard 'METHOD: thesis' convention:
(i) the thesis that the productive unit of engineering for LLM-based agents
is the **harness** (the surrounding scaffold of prompts, tools, memory,
observability, and control loops) rather than the underlying model itself,
and that this harness deserves a dedicated **engineering discipline**; and
(ii) the companion claim that **AHE** is the proposed name and shape of
that discipline. The three keywords name the supporting axes: (1)
**harness-design** is the constructive axis -- what a well-engineered
agentic harness looks like; (2) **self-evolution** is the dynamic axis --
the harness is not a static artifact but improves itself over its
operational life; and (3) **observability** is the diagnostic axis --
without first-class instrumentation no harness can be debugged, evaluated,
or evolved.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

agent_harness_setting = setting(
    "An *agent harness* is the engineered scaffold that wraps a base "
    "language model to turn it into a working agent: the prompt templates, "
    "tool registry and tool-calling protocol, memory and context-management "
    "policies, planning / control loops, error-recovery behaviour, "
    "permissions, and the observability instrumentation that lets operators "
    "see what is happening at runtime. In production agentic systems the "
    "harness is typically the locus of the engineering work -- model weights "
    "are inherited from a third-party provider while the harness is the "
    "in-house artifact that determines whether the agent is reliable, "
    "debuggable, and improvable.",
    title="Agent harness (formal setting)",
)

ahe_scope = setting(
    "The study scope of AHE is the **discipline** of building, operating, "
    "and improving such harnesses -- analogous to software engineering for "
    "programs, or site-reliability engineering for services. It treats the "
    "harness (not the base model) as the primary engineering object, asks "
    "what its design vocabulary is, what runtime properties it must expose, "
    "and how it should change over its operational lifetime in response to "
    "observed failures and shifting tasks.",
    title="Agentic harness engineering as a discipline (study scope)",
)

# ---------------------------------------------------------------------------
# Headline title-level claims (the H1 of the artifact)
# ---------------------------------------------------------------------------

harness_is_the_engineering_object = claim(
    "The productive unit of engineering for LLM-based agents is the "
    "**harness** -- the scaffold of prompts, tools, memory, control loops, "
    "and observability that surrounds the base model -- rather than the "
    "model weights themselves. As a corollary, the construction and "
    "operation of harnesses deserves a dedicated engineering discipline "
    "with its own design vocabulary, runtime requirements, and improvement "
    "loop, on par with software engineering or site-reliability engineering.",
    title="Central thesis: the harness is the primary engineering object for agents",
    metadata={"source": "artifacts/2604.25850-ahe-agentic-harness-engineering.md (H1 / title)"},
)

ahe_realises_harness_engineering = claim(
    "**AHE** -- the framework named in the title -- is proposed as the "
    "concrete realisation of that discipline: it specifies the design "
    "vocabulary for harnesses (the components and their interfaces), the "
    "runtime properties a harness must expose (notably observability), and "
    "the lifecycle by which a harness improves itself in response to its "
    "own runtime evidence (self-evolution).",
    title="AHE realises agentic harness engineering",
    metadata={"source": "artifacts/2604.25850-ahe-agentic-harness-engineering.md (title: 'AHE:')"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 3 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim that ties back to the central thesis.
# ---------------------------------------------------------------------------

keyword_harness_design = claim(
    "The work develops a **harness-design** vocabulary -- a constructive "
    "account of what the components of a well-engineered agentic harness "
    "are (prompt scaffold, tool layer, memory / context manager, control "
    "loop, error and permissions policy) and how those components compose. "
    "Harness-design is the static-structure axis of AHE: it answers 'what "
    "does a good harness look like' independent of how it changes over "
    "time.",
    title="Keyword: harness-design",
    metadata={"keyword_index": 1, "source": "artifacts/2604.25850-ahe-agentic-harness-engineering.md (keywords)"},
)

keyword_self_evolution = claim(
    "The work treats the harness as **self-evolving** -- a harness is not "
    "a static artifact deployed once, but an object that updates its own "
    "prompts, tool selection, memory policy, and control logic in response "
    "to observed runtime evidence (failures, drifts, new tasks). "
    "Self-evolution is the dynamic-lifecycle axis of AHE: it answers 'how "
    "should a harness change over its operational life'.",
    title="Keyword: self-evolution",
    metadata={"keyword_index": 2, "source": "artifacts/2604.25850-ahe-agentic-harness-engineering.md (keywords)"},
)

keyword_observability = claim(
    "The work makes **observability** -- structured, queryable runtime "
    "instrumentation of the harness's internal states (which prompt fired, "
    "which tool was called with what arguments, which memory was retrieved, "
    "which control branch was taken, why) -- a first-class harness "
    "requirement. Observability is the diagnostic / feedback axis of AHE: "
    "without it neither human debugging nor automated self-evolution has "
    "the evidence it needs to act on.",
    title="Keyword: observability",
    metadata={"keyword_index": 3, "source": "artifacts/2604.25850-ahe-agentic-harness-engineering.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two title-level leaf claims jointly grant evidence to each of the three
# keyword claims: the central harness-as-engineering-object thesis grounds
# both the static design vocabulary and the diagnostic observability
# requirement, while the AHE-as-discipline claim additionally grounds the
# dynamic self-evolution lifecycle.

strat_thesis_grounds_harness_design = support(
    [harness_is_the_engineering_object, ahe_realises_harness_engineering],
    keyword_harness_design,
    background=[agent_harness_setting, ahe_scope],
    reason=(
        "If the harness is the primary engineering object "
        "(@harness_is_the_engineering_object) and AHE is the discipline "
        "that engineers it (@ahe_realises_harness_engineering), then any "
        "such discipline must commit to a constructive vocabulary for what "
        "the engineered object is built out of (@agent_harness_setting, "
        "@ahe_scope). That vocabulary -- the static-structure axis -- is "
        "what the keyword 'harness-design' names."
    ),
    prior=0.93,
)

strat_discipline_grounds_self_evolution = support(
    [ahe_realises_harness_engineering],
    keyword_self_evolution,
    background=[agent_harness_setting, ahe_scope],
    reason=(
        "An engineering discipline for harnesses "
        "(@ahe_realises_harness_engineering) cannot stop at one-shot "
        "construction: harnesses are deployed against shifting tasks and "
        "observed failures (@agent_harness_setting), so the discipline "
        "must specify how a harness changes over its operational life "
        "(@ahe_scope). The keyword 'self-evolution' names exactly that "
        "lifecycle commitment -- the harness updates itself, not merely "
        "is updated by humans on the next release."
    ),
    prior=0.9,
)

strat_thesis_grounds_observability = support(
    [harness_is_the_engineering_object, ahe_realises_harness_engineering],
    keyword_observability,
    background=[agent_harness_setting, ahe_scope],
    reason=(
        "Treating the harness as a first-class engineering object "
        "(@harness_is_the_engineering_object) within a discipline that "
        "must support both human debugging and automated self-evolution "
        "(@ahe_realises_harness_engineering) entails a hard requirement on "
        "structured runtime instrumentation: every prompt fire, tool call, "
        "memory hit, and control-branch decision must be inspectable "
        "(@agent_harness_setting, @ahe_scope). Without that, neither the "
        "operator nor the harness itself has the evidence to act on. The "
        "keyword 'observability' names that requirement."
    ),
    prior=0.94,
)

__all__ = [
    "agent_harness_setting",
    "ahe_scope",
    "harness_is_the_engineering_object",
    "ahe_realises_harness_engineering",
    "keyword_harness_design",
    "keyword_self_evolution",
    "keyword_observability",
]
