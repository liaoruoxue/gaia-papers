"""Motivation: RecursiveMAS -- a latent-space, recursive multi-agent system.

Formalisation of arXiv:2604.25917 ("RecursiveMAS: Latent-Space Multi-Agent").
The source artifact in this package is a thin stub (title + arXiv link +
three-keyword list + status line); no PDF body is available. Therefore only
the title-level thesis claim, its companion method claim, and the three
listed keyword topics are extracted as claims.

The H1 of the artifact -- "RecursiveMAS: Latent-Space Multi-Agent" -- is
split into two title-level leaves under the standard 'METHOD: thesis'
convention:

  (i) the thesis that a multi-agent system (MAS) of language-model agents
      should communicate **in latent space** -- exchanging continuous
      hidden-state messages rather than (or alongside) natural-language
      tokens -- and that this latent-message channel is a first-class
      design axis for MAS, not an implementation detail; and
 (ii) the companion claim that **RecursiveMAS** is the proposed instance
      of that design, and that its distinguishing structural choice over
      prior latent-MAS designs is **recursion** -- agents are organised
      so that an agent can itself host / spawn / call further agents in
      the same latent channel, yielding a nested rather than flat
      organisation.

The three keywords name the three supporting axes:
  (1) **multi-agent** -- the work studies a system of cooperating agents,
      not a single monolithic policy;
  (2) **latent-communication** -- the inter-agent channel carries
      continuous latent vectors, not (only) discrete tokens; and
  (3) **recursive** -- the organisational topology over agents is
      recursive (an agent can call further agents through the same
      latent channel), not a fixed flat panel.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

mas_setting = setting(
    "A *multi-agent system* (MAS) of language-model agents is an "
    "ensemble of distinct LM-backed agents that coordinate to solve a "
    "task: each agent has its own role, prompt, tool access, and local "
    "state, and the agents exchange messages over a shared channel. "
    "The properties of that inter-agent channel -- its representation "
    "(discrete tokens vs continuous vectors), its bandwidth, and its "
    "topology (flat vs nested) -- are first-order design choices that "
    "determine what the MAS can express, how efficiently it can express "
    "it, and how composable it is with itself.",
    title="Multi-agent system of LM agents (formal setting)",
)

latent_channel_setting = setting(
    "A *latent-space communication channel* between agents transmits "
    "continuous hidden-state vectors -- typically the LM's internal "
    "activations or a dedicated learnt embedding -- in place of (or in "
    "addition to) natural-language tokens. Compared to a token channel "
    "it carries strictly more information per message, it is "
    "differentiable end-to-end (so the channel itself can be learnt), "
    "and it is not tied to the surface vocabulary of any one language. "
    "It also gives up the human-readability of token messages and "
    "requires the receiving agent to be representationally compatible "
    "with the sender.",
    title="Latent-space inter-agent channel",
)

recursivemas_scope = setting(
    "The study scope of RecursiveMAS is the design of a latent-space MAS "
    "in which the organisation over agents is *recursive*: a 'parent' "
    "agent can call -- and exchange latent messages with -- one or more "
    "'child' agents that themselves use the same latent channel and may "
    "in turn call further agents. The organisation is therefore a tree "
    "(or DAG) over agents rather than a fixed flat panel of peers, and "
    "any subsystem of the organisation is itself a latent-MAS.",
    title="RecursiveMAS (study scope)",
)

# ---------------------------------------------------------------------------
# Headline title-level claims (the H1 of the artifact)
# ---------------------------------------------------------------------------

latent_space_is_the_mas_channel = claim(
    "For multi-agent systems of language-model agents, the productive "
    "inter-agent channel is a **latent-space** channel -- continuous "
    "hidden-state messages exchanged directly between agents -- rather "
    "than (or alongside) a natural-language token channel. Treating the "
    "latent channel as a first-class design axis (not an implementation "
    "detail) is the central methodological move: it determines the "
    "expressivity, bandwidth, end-to-end learnability, and compositional "
    "behaviour of the MAS.",
    title="Central thesis: latent space is the first-class MAS communication channel",
    metadata={"source": "artifacts/2604.25917-recursivemas-latent-space-multi-agent.md (H1 / title)"},
)

recursivemas_realises_recursive_latent_mas = claim(
    "**RecursiveMAS** -- the system named in the title -- is proposed as "
    "the concrete realisation of latent-space MAS whose distinguishing "
    "structural choice is **recursion**: agents are organised so that an "
    "agent can itself host, spawn, or call further agents through the "
    "same latent channel, yielding a nested (tree / DAG) organisation in "
    "which every subsystem is itself a latent-MAS. The 'Recursive' "
    "qualifier is the load-bearing differentiator from prior flat "
    "latent-MAS proposals.",
    title="RecursiveMAS realises a recursive latent-space MAS",
    metadata={"source": "artifacts/2604.25917-recursivemas-latent-space-multi-agent.md (title: 'RecursiveMAS:')"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 3 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim that ties back to the central thesis.
# ---------------------------------------------------------------------------

keyword_multi_agent = claim(
    "The work studies a **multi-agent** system: the unit of analysis is "
    "an ensemble of cooperating LM-backed agents (each with its own "
    "role, prompt, tool access, and local state) coordinating over a "
    "shared channel, rather than a single monolithic policy. Multi-agent "
    "is the *organisational-substrate* axis of RecursiveMAS -- it fixes "
    "what the channel is a channel *between*.",
    title="Keyword: multi-agent",
    metadata={"keyword_index": 1, "source": "artifacts/2604.25917-recursivemas-latent-space-multi-agent.md (keywords)"},
)

keyword_latent_communication = claim(
    "The work commits to **latent-communication** as the inter-agent "
    "channel: agents exchange continuous latent vectors (hidden states "
    "or dedicated learnt embeddings) instead of (or alongside) discrete "
    "natural-language tokens. Latent-communication is the "
    "*channel-representation* axis of RecursiveMAS -- it fixes what the "
    "messages between agents *are*, and unlocks higher per-message "
    "bandwidth and end-to-end differentiability of the whole MAS.",
    title="Keyword: latent-communication",
    metadata={"keyword_index": 2, "source": "artifacts/2604.25917-recursivemas-latent-space-multi-agent.md (keywords)"},
)

keyword_recursive = claim(
    "The work organises agents **recursively**: an agent can itself "
    "call further agents through the same latent channel, so the "
    "organisation is a nested tree / DAG in which every subsystem is "
    "itself a latent-MAS. Recursive is the *topology* axis of "
    "RecursiveMAS -- it fixes how the agents are wired to each other "
    "(nested, not flat) and is the load-bearing differentiator from "
    "prior flat latent-MAS designs.",
    title="Keyword: recursive",
    metadata={"keyword_index": 3, "source": "artifacts/2604.25917-recursivemas-latent-space-multi-agent.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two title-level leaf claims jointly grant evidence to each of the three
# keyword claims: the central latent-channel thesis grounds both the
# multi-agent substrate (something must be at the endpoints of the channel)
# and the latent-communication channel itself, while the
# RecursiveMAS-as-instance claim additionally grounds the recursive topology.

strat_thesis_grounds_multi_agent = support(
    [latent_space_is_the_mas_channel, recursivemas_realises_recursive_latent_mas],
    keyword_multi_agent,
    background=[mas_setting, recursivemas_scope],
    reason=(
        "If a latent-space channel is the first-class MAS communication "
        "axis (@latent_space_is_the_mas_channel) and RecursiveMAS is its "
        "concrete realisation (@recursivemas_realises_recursive_latent_mas), "
        "then the work necessarily studies a system of multiple distinct "
        "agents -- the channel is by definition a channel *between* agents "
        "(@mas_setting, @recursivemas_scope). The keyword 'multi-agent' "
        "names that organisational-substrate commitment."
    ),
    prior=0.95,
)

strat_thesis_grounds_latent_communication = support(
    [latent_space_is_the_mas_channel],
    keyword_latent_communication,
    background=[mas_setting, latent_channel_setting],
    reason=(
        "The thesis that latent space is the first-class MAS channel "
        "(@latent_space_is_the_mas_channel) is in fact a definitional "
        "commitment to latent-communication: the agents exchange "
        "continuous hidden-state vectors rather than discrete tokens "
        "(@latent_channel_setting), with the bandwidth and "
        "differentiability properties that follow (@mas_setting). The "
        "keyword 'latent-communication' is the direct restatement of "
        "that channel-representation choice."
    ),
    prior=0.96,
)

strat_recursivemas_grounds_recursive = support(
    [recursivemas_realises_recursive_latent_mas],
    keyword_recursive,
    background=[mas_setting, recursivemas_scope],
    reason=(
        "The 'Recursive' qualifier in 'RecursiveMAS' is precisely the "
        "claim that the organisation over agents is recursive -- a "
        "parent agent calls further agents through the same latent "
        "channel, so any subsystem is itself a latent-MAS "
        "(@recursivemas_realises_recursive_latent_mas, "
        "@recursivemas_scope). Distinguishing this work from prior flat "
        "latent-MAS designs is exactly the load-bearing role of the "
        "keyword 'recursive' (@mas_setting)."
    ),
    prior=0.94,
)

__all__ = [
    "mas_setting",
    "latent_channel_setting",
    "recursivemas_scope",
    "latent_space_is_the_mas_channel",
    "recursivemas_realises_recursive_latent_mas",
    "keyword_multi_agent",
    "keyword_latent_communication",
    "keyword_recursive",
]
