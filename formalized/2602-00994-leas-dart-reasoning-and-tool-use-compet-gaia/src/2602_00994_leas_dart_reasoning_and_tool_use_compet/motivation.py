"""Motivation: reasoning and tool-use compete in agentic RL (LEAS+DART).

Formalisation of arXiv:2602.00994 ("LEAS+DART: Reasoning and Tool-use Compete
in Agentic RL"). The source artifact in this package is a thin stub (title +
arXiv link + keyword list); no PDF body is available. Therefore only the
title-level thesis claim and the explicit keyword claims are formalised here.

The H1 of the artifact -- "Reasoning and Tool-use Compete in Agentic RL" --
is itself the central thesis: when an agentic LLM is RL-trained jointly to
both reason internally (chain-of-thought, planning) and to invoke external
tools (search, code execution, retrieval, MCP, ...), the two skills compete
during optimisation rather than cooperating monotonically. LEAS+DART is the
authors' proposed fix to that competition; the three keywords name the
mechanism: (i) RL training is the regime in which the conflict arises,
(ii) gradient conflict is the technical diagnosis of the competition, and
(iii) dual-LoRA is the architectural remedy that decouples the two skills'
parameter updates.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

agentic_rl_setting = setting(
    "An *agentic LLM* is a language model that, in addition to emitting "
    "natural-language reasoning, can issue tool calls (search, code "
    "execution, retrieval, MCP, browser, ...) and condition its next step on "
    "the tool's response. *Agentic RL* is reinforcement learning applied to "
    "such a model end-to-end: a single policy is updated against task-level "
    "rewards that depend on both the quality of the model's internal "
    "reasoning and the appropriateness of its external tool calls. The two "
    "behaviours share the same parameters and are updated by the same "
    "gradient signal.",
    title="Agentic RL (formal setting)",
)

joint_training_scope = setting(
    "The study scope is the joint optimisation of *reasoning skill* "
    "(producing correct intermediate chains-of-thought / plans) and "
    "*tool-use skill* (deciding when and how to call external tools and how "
    "to integrate their outputs) within a single RL fine-tuning run on an "
    "agentic LLM. Performance is measured per-skill (reasoning-only and "
    "tool-use-only sub-tasks) as well as on the full agentic task, so that "
    "interference between the two skills can be observed directly.",
    title="Study scope: joint reasoning + tool-use RL fine-tuning",
)

# ---------------------------------------------------------------------------
# Headline thesis claim (the H1 of the artifact)
# ---------------------------------------------------------------------------

reasoning_and_tooluse_compete = claim(
    "In agentic RL, **reasoning and tool-use compete** -- jointly RL-training "
    "a single agentic LLM policy to be both a better reasoner and a better "
    "tool-user produces destructive interference between the two skills "
    "rather than a clean Pareto improvement: gains on one axis are bought at "
    "measurable cost on the other under standard end-to-end RL training.",
    title="Central thesis: reasoning and tool-use compete in agentic RL",
    metadata={"source": "artifacts/2602.00994-leas+dart-reasoning-and-tool-use-compet.md (H1 / title)"},
)

leas_dart_resolves_competition = claim(
    "**LEAS+DART** -- the method named in the title -- is proposed as a "
    "training-time remedy that **decouples** the optimisation of reasoning "
    "and tool-use sufficiently to eliminate (or substantially reduce) the "
    "competition diagnosed above, recovering joint gains on both skills.",
    title="LEAS+DART resolves the reasoning/tool-use competition",
    metadata={"source": "artifacts/2602.00994-leas+dart-reasoning-and-tool-use-compet.md (title: 'LEAS+DART:')"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 3 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim that ties back to the central thesis.
# ---------------------------------------------------------------------------

keyword_rl_training = claim(
    "The work is situated within **RL training** of agentic LLMs -- it "
    "diagnoses the reasoning-vs-tool-use competition specifically as a "
    "phenomenon of the reinforcement-learning fine-tuning regime (where the "
    "policy receives sparse, task-level rewards covering both skills), as "
    "opposed to supervised fine-tuning or in-context prompting.",
    title="Keyword: RL training",
    metadata={"keyword_index": 1, "source": "artifacts/2602.00994-leas+dart-reasoning-and-tool-use-compet.md (keywords)"},
)

keyword_gradient_conflict = claim(
    "The work identifies **gradient conflict** as the technical mechanism "
    "behind the competition: the per-sample gradients that improve "
    "reasoning trajectories and the per-sample gradients that improve "
    "tool-use trajectories point in opposing directions in shared parameter "
    "subspaces, so that an optimiser step that improves one skill measurably "
    "degrades the other.",
    title="Keyword: gradient conflict",
    metadata={"keyword_index": 2, "source": "artifacts/2602.00994-leas+dart-reasoning-and-tool-use-compet.md (keywords)"},
)

keyword_dual_lora = claim(
    "The work proposes **dual-LoRA** -- two parallel low-rank adapters, one "
    "specialised for reasoning gradients and one for tool-use gradients -- "
    "as the architectural remedy that physically separates the two skills' "
    "update subspaces and so eliminates the shared-parameter gradient "
    "conflict identified above.",
    title="Keyword: dual-LoRA",
    metadata={"keyword_index": 3, "source": "artifacts/2602.00994-leas+dart-reasoning-and-tool-use-compet.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two title-level leaf claims jointly grant evidence to each of the three
# keyword claims: the central competition thesis grounds the RL-training
# situating and the gradient-conflict diagnosis, and the LEAS+DART remedy
# grounds the dual-LoRA proposal.

strat_thesis_grounds_rl_training = support(
    [reasoning_and_tooluse_compete],
    keyword_rl_training,
    background=[agentic_rl_setting, joint_training_scope],
    reason=(
        "The central thesis (@reasoning_and_tooluse_compete) is itself a "
        "claim *about an RL training regime*: 'compete in agentic RL' "
        "predicates the competition on the RL fine-tuning step within the "
        "agentic-LLM setting (@agentic_rl_setting) and the joint-training "
        "scope (@joint_training_scope). Hence the work is squarely about RL "
        "training of agentic LLMs."
    ),
    prior=0.95,
)

strat_thesis_grounds_gradient_conflict = support(
    [reasoning_and_tooluse_compete, leas_dart_resolves_competition],
    keyword_gradient_conflict,
    background=[agentic_rl_setting, joint_training_scope],
    reason=(
        "Saying that two skills *compete* during a shared-parameter RL "
        "update (@reasoning_and_tooluse_compete) within the agentic-LLM "
        "setting (@agentic_rl_setting) and joint training scope "
        "(@joint_training_scope) is operationally a statement that their "
        "gradients conflict in the shared subspace; the fact that LEAS+DART "
        "is needed to fix it (@leas_dart_resolves_competition) further "
        "implies the underlying obstacle is gradient-level interference "
        "rather than e.g. data scarcity. Hence the paper's mechanism story "
        "is gradient conflict."
    ),
    prior=0.9,
)

strat_remedy_grounds_dual_lora = support(
    [leas_dart_resolves_competition, keyword_gradient_conflict],
    keyword_dual_lora,
    background=[agentic_rl_setting],
    reason=(
        "Given that the diagnosed problem is shared-parameter gradient "
        "conflict (@keyword_gradient_conflict), the natural and minimally "
        "invasive remedy is to give each skill its own low-rank adapter so "
        "that their updates live in disjoint subspaces. The 'DART' half of "
        "the LEAS+DART method name (@leas_dart_resolves_competition), "
        "together with the listed keyword 'dual-lora', matches exactly that "
        "design within the agentic-LLM setting (@agentic_rl_setting). Hence "
        "the work's remedy is dual-LoRA."
    ),
    prior=0.92,
)

__all__ = [
    "agentic_rl_setting",
    "joint_training_scope",
    "reasoning_and_tooluse_compete",
    "leas_dart_resolves_competition",
    "keyword_rl_training",
    "keyword_gradient_conflict",
    "keyword_dual_lora",
]
