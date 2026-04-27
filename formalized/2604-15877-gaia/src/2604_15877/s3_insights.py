"""Section 3: Four structural insights revealed by the spectrum view."""

from gaia.lang import claim, support

from .motivation import (
    community_disconnect,
)
from .s2_mapping import (
    higher_compression_better,
    obs_skillrl_l2_vs_l1,
    obs_evoskill_l2_vs_none,
    obs_trace2skill_l2_vs_human,
    fidelity_matters,
    missing_diagonal,
)

# --- 3.1 Specialization alone is insufficient ---

shared_subproblems = claim(
    "Both the agent memory and agent skill communities independently solve the same "
    "sub-problems without sharing solutions: retrieval over growing knowledge stores, "
    "conflict detection between contradictory entries, staleness recognition, and "
    "evaluation of downstream utility. The spectrum view (which exposes the shared "
    "compression operation) makes this redundancy visible.",
    title="Communities solve identical sub-problems independently",
)

deployment_needs_both = claim(
    "Real deployments require both **personalization** (memory-style user-specific "
    "context retention) and **capability** (skill-style reusable procedural patterns). "
    "An agent that abstracts reusable workflows but forgets user preferences is "
    "incomplete; one that remembers context but cannot consolidate recurring patterns "
    "will overwhelm its retrieval budget.",
    title="Deployments need both personalization and capability",
)

specialization_insufficient = claim(
    "Specialization alone is insufficient as a justification for the memory-skill split. "
    "A unified architecture -- with **level-specific compressors** sharing common "
    "**retrieval, conflict-resolution, and lifecycle infrastructure** -- would avoid "
    "redundant engineering across communities while still allowing specialization at "
    "the compression-output layer.",
    title="Specialization alone cannot justify the community split",
)

strat_specialization_insufficient = support(
    [shared_subproblems, deployment_needs_both, community_disconnect],
    specialization_insufficient,
    reason=(
        "The specialization defense argues that distinct communities address distinct "
        "downstream needs. But the spectrum reveals shared sub-problems "
        "(@shared_subproblems) and deployment requirements that demand both flavors "
        "simultaneously (@deployment_needs_both). Combined with the empirically "
        "documented community disconnect (@community_disconnect), the argument "
        "supports adopting a shared infrastructure layer rather than parallel "
        "engineering tracks."
    ),
    prior=0.85,
)

# --- 3.2 Evaluation methods are level-coupled ---

evaluation_level_coupling = claim(
    "Existing evaluation methodology is **tightly coupled to the compression level**: "
    "Level 1 systems evaluate via question-answering metrics (F1, exact match); Level 2 "
    "systems evaluate via task success rate; Level 3 has no established methodology. "
    "This coupling means systems are optimized for their level's metric, which may not "
    "reflect true downstream utility. For example, MemSkill achieves strong QA F1 but "
    "its impact on multi-step task completion is unclear; EvoSkill's task-success metric "
    "cannot capture user-specific context.",
    title="Evaluation methods are level-coupled",
)

evaluation_should_unify = claim(
    "A unified evaluation framework should assess knowledge artifacts by their "
    "**downstream impact on agent performance across time**, regardless of compression "
    "level -- an efficiency metric that captures *value per token of stored knowledge*. "
    "This would replace level-specific metrics with a level-agnostic measure that "
    "exposes whether highly compressed artifacts genuinely outperform less-compressed "
    "ones at the system level.",
    title="Evaluation should be level-agnostic, value-per-token",
)

strat_evaluation_should_unify = support(
    [evaluation_level_coupling, missing_diagonal],
    evaluation_should_unify,
    reason=(
        "Level-coupled evaluation (@evaluation_level_coupling) prevents fair "
        "cross-level comparison: an L1-optimized system maximizes QA F1, an L2 system "
        "maximizes task success, and the two metrics cannot be directly compared. "
        "Combined with the missing diagonal (@missing_diagonal), which requires "
        "comparing artifacts at different levels to decide promotion or demotion, the "
        "current methodology cannot drive adaptive selection. A level-agnostic "
        "value-per-token metric would enable both fair comparison and adaptive control."
    ),
    prior=0.82,
)

# --- 3.3 Transferability increases with compression ---

transferability_monotonic = claim(
    "Empirical evidence supports a **monotonic relationship** between compression level "
    "and transferability: Level 1 memories transfer across base models (MemSkill: "
    "LLaMA -> Qwen); Level 2 skills transfer across tasks (EvoSkill: SealQA -> "
    "BrowseComp, +5.3%) and across model sizes (Trace2Skill: 35B parameters -> 122B "
    "parameters, +57.7 percentage points). Higher-compression artifacts transfer more "
    "broadly because they carry less context-specific detail.",
    title="Transferability monotonically increases with compression",
)

obs_trace2skill_size_transfer = claim(
    "Trace2Skill ([@Ni2026trace2skill]) reports a +57.7 percentage-point gain when "
    "transferring its Level-2 skills from a 35-billion-parameter model to a "
    "122-billion-parameter model, demonstrating cross-model-size transferability of "
    "Level-2 skills.",
    title="Trace2Skill: +57.7pp 35B -> 122B transfer",
)

strat_transferability_monotonic = support(
    [obs_skillrl_l2_vs_l1, obs_evoskill_l2_vs_none, obs_trace2skill_size_transfer],
    transferability_monotonic,
    reason=(
        "Three cross-domain or cross-model transfer results consistently support "
        "the monotonic transferability claim: SkillRL's L2-over-L1 advantage on "
        "ALFWorld (@obs_skillrl_l2_vs_l1) is one cross-model setting; EvoSkill's "
        "transfer to BrowseComp (@obs_evoskill_l2_vs_none) demonstrates cross-task "
        "transfer; and Trace2Skill's 35B-to-122B transfer (@obs_trace2skill_size_transfer) "
        "demonstrates cross-model-size transfer. All three are consistent with the "
        "direction predicted by higher abstraction = broader applicability."
    ),
    prior=0.78,
)

transferability_concavity = claim(
    "The transferability versus specificity curve **likely follows a concave shape**, "
    "with the sweet spot at Level 2 balancing transferability against specificity. "
    "This conjecture has not been validated by a controlled experiment (one that holds "
    "source experience constant and varies only the compression level), but existing "
    "evidence is consistent with it.",
    title="Concave transferability curve, sweet spot at L2",
)

strat_transferability_concavity = support(
    [transferability_monotonic, fidelity_matters],
    transferability_concavity,
    reason=(
        "The monotonic claim (@transferability_monotonic) covers the L0-to-L2 "
        "transition where transferability rises with compression. The fidelity caveat "
        "(@fidelity_matters) -- that compression must preserve genuinely useful "
        "patterns -- implies an upper bound: at Level 3, compression to abstract "
        "principles may discard the actionable specificity needed for task execution. "
        "Together they suggest a peak at Level 2 (high transfer, still actionable), "
        "consistent with the concavity conjecture."
    ),
    prior=0.65,
)

# --- 3.4 Lifecycle management is neglected ---

lifecycle_neglected = claim(
    "Lifecycle management remains **largely an afterthought** across both communities. "
    "Existing systems focus on knowledge acquisition while treating maintenance as "
    "secondary. Some include partial mechanisms -- Mem0's LLM-driven operations, "
    "Memory-R1's RL-learned updates, ExpeL's importance counting, AutoSkill "
    "([@Yang2026autoskill])'s version management -- but these remain isolated. No "
    "system addresses the full lifecycle: conflict detection across knowledge types, "
    "staleness recognition, principled deprecation, and cross-level consistency.",
    title="Knowledge lifecycle management is neglected",
)

obs_merge_swing = claim(
    "Merging skills does not always help: including success-trace signals during skill "
    "merging can cause performance swings of plus or minus 21 percentage points "
    "([@Ni2026trace2skill]). Agent behavior can degrade over extended operation even "
    "when individual-step correctness is maintained, indicating that lifecycle issues "
    "compound over time.",
    title="Skill merging can swing +/-21pp; behavior degrades over time",
)

lifecycle_borrow_se = claim(
    "The software-engineering community's version-control and deprecation practices "
    "offer a concrete opportunity for transfer to knowledge artifacts. Versioned "
    "artifacts with explicit deprecation protocols would address staleness, "
    "cross-level consistency, and conflict resolution simultaneously.",
    title="Borrow version control and deprecation from software engineering",
)

strat_lifecycle_neglected = support(
    [obs_merge_swing],
    lifecycle_neglected,
    reason=(
        "The +/-21pp swing from skill merging (@obs_merge_swing) provides direct "
        "empirical evidence that current systems lack robust lifecycle mechanisms: "
        "even simple merge operations can degrade performance significantly. "
        "Combined with the partial-or-absent lifecycle support reported in Table 2 "
        "of the source survey, this grounds the qualitative neglect claim in a "
        "measurable failure mode."
    ),
    prior=0.85,
)

# --- Testable predictions (Section 3, end) ---

prediction_l2_beats_l1_transfer = claim(
    "**Testable Prediction 1.** Level-2 compression should outperform Level-1 retrieval "
    "on cross-domain transfer when source experience is held constant. This prediction "
    "follows directly from the monotonic-transferability hypothesis and would be "
    "falsified by a controlled experiment in which an L1 retrieval system matches or "
    "exceeds an L2 skill system on a transfer benchmark with identical training data.",
    title="Prediction 1: L2 > L1 on cross-domain transfer",
)

prediction_multilevel_better = claim(
    "**Testable Prediction 2.** A multi-level knowledge store combining Level 1 "
    "(memories) and Level 2 (skills) should outperform either level alone, with the "
    "performance gap **widening** as deployment length increases. This follows from "
    "the acquisition-versus-maintenance trade-off: L2 alone misses user-specific "
    "context; L1 alone is overwhelmed at scale.",
    title="Prediction 2: L1+L2 store improves with deployment length",
)

prediction_concave_curve = claim(
    "**Testable Prediction 3.** The transferability-versus-specificity curve should be "
    "concave, with Level 2 at the sweet spot. This follows from the conjecture that "
    "transferability rises monotonically with compression but specificity falls; the "
    "two trends imply an interior optimum.",
    title="Prediction 3: concave transferability curve, peak at L2",
)

prediction_l3_constraints = claim(
    "**Testable Prediction 4.** Level-3 declarative rules should help most when framed "
    "as **constraints (guardrails)** rather than directives (positive instructions). "
    "This is consistent with the early evidence from RuleShaping ([@Zhang2026rules]) "
    "showing that negative constraints improve performance by 7-14pp while positive "
    "directives hurt.",
    title="Prediction 4: L3 rules should be guardrails, not directives",
)

predictions_distinguish_taxonomy = claim(
    "Validating or falsifying the four testable predictions (1-4 above) would establish "
    "whether the experience-compression spectrum is a useful **design tool** or merely a "
    "**descriptive framework**. A taxonomy that does not generate falsifiable predictions "
    "lacks engineering leverage; the four predictions provide concrete empirical tests.",
    title="Predictions distinguish design tool from taxonomy",
)

strat_predictions_distinguish = support(
    [
        prediction_l2_beats_l1_transfer,
        prediction_multilevel_better,
        prediction_concave_curve,
        prediction_l3_constraints,
    ],
    predictions_distinguish_taxonomy,
    reason=(
        "The four testable predictions (@prediction_l2_beats_l1_transfer, "
        "@prediction_multilevel_better, @prediction_concave_curve, "
        "@prediction_l3_constraints) are individually falsifiable by concrete "
        "controlled experiments. Their existence demonstrates that the spectrum view "
        "yields engineering-relevant hypotheses, not only descriptive categorization."
    ),
    prior=0.88,
)
