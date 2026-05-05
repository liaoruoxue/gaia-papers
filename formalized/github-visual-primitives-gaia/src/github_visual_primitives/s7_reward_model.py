"""Section 2.3 (Reward Model subsection) -- the 3-way Reward Model used in
per-expert GRPO RL.

Source: Layer-2 Section 2.3 'Reward Model 三维并行' of the Visual
Primitives release [@DeepSeekVisualPrimitives], cross-validated by
[@CSDNDeepRead].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: 3-way RM means three reward terms scored in parallel
# ---------------------------------------------------------------------------

setup_three_way_rm = setting(
    "**Setup: 3-way Reward Model.** During GRPO RL each rollout "
    "is scored by **three parallel reward terms**: Format, "
    "Quality, and Task-Specific Accuracy. The three rewards are "
    "combined into a single scalar reward that GRPO maximizes. "
    "The decomposition is intended to disentangle three failure "
    "modes that would otherwise be conflated.",
    title="Setup: 3-way RM = Format + Quality + Task-Specific Accuracy",
)

# ---------------------------------------------------------------------------
# Atomic claims for each of the three reward terms
# ---------------------------------------------------------------------------

claim_format_rm = claim(
    "**Format RM (rule-based, $\\{0, 1\\}$).** A purely rule-based "
    "checker validates that emitted primitive tokens are well-"
    "formed and detects redundancy: it rejects malformed `<|box|>` "
    "/ `<|point|>` sequences (wrong arity, out-of-image "
    "coordinates, mismatched delimiters) and flags redundant "
    "boxes (e.g. multiple boxes covering the same region). The "
    "Format RM emits a binary score: 1 if the rollout is well-"
    "formed and non-redundant, 0 otherwise.",
    title="Format RM: rule-based, {0, 1}, primitive-format + redundancy detection",
)

claim_quality_rm = claim(
    "**Quality RM (LLM judge, $\\{0, 0.5, 1.0\\}$).** A separate "
    "LLM judges semantic quality of the rollout along four axes: "
    "(i) **redundancy** (repeated reasoning steps), (ii) "
    "**consistency** (does the CoT stay coherent across primitive "
    "emissions?), (iii) **self-contradiction** (does the rollout "
    "contradict its own intermediate conclusions?), and (iv) "
    "**reward hacking** (does the rollout shortcut around the "
    "task using format-legal but task-irrelevant primitives?). "
    "The Quality RM emits a 3-level score in $\\{0, 0.5, 1.0\\}$.",
    title="Quality RM: LLM judge, {0, 0.5, 1.0}, redundancy + consistency + self-contradiction + reward hacking",
)

claim_task_accuracy_rm = claim(
    "**Task-Specific Accuracy RM (per-task, scalar).** Each task "
    "carries its own accuracy reward function tuned for that "
    "task's structure:\n\n"
    "- **Counting**: smoothed exponential decay around the true "
    "count (closer = higher reward, wrong-by-many penalised "
    "smoothly so that off-by-one is preferred over off-by-many).\n"
    "- **Maze Navigation**: composed of *exploration progress* "
    "(fraction of optimal path covered), *wall-violation* penalty "
    "(every illegal traversal costs reward), and *path validity* "
    "(end-to-end reachability of goal).\n\n"
    "The per-task RM is the only reward term that depends on the "
    "ground-truth task answer; the other two terms are answer-"
    "agnostic.",
    title="Task-Specific Accuracy RM: per-task scoring (counting -> smoothed exp decay; maze -> progress + wall + validity)",
)

# ---------------------------------------------------------------------------
# Why three terms in parallel rather than one combined judge?
# ---------------------------------------------------------------------------

claim_rm_decomposition_rationale = claim(
    "**Why decompose: each term targets an orthogonal failure "
    "mode.** Format RM blocks malformed primitive emission, "
    "Quality RM blocks reasoning pathologies and reward hacking, "
    "and Task-Specific Accuracy RM grounds the reward in "
    "ground-truth task performance. A single combined judge "
    "would conflate these axes and give the policy weaker signal "
    "for shaping individual behaviours; three parallel terms "
    "provide cleaner gradient signal per failure mode.",
    title="Rationale: 3-way decomposition gives clean signal per orthogonal failure mode",
)

claim_rm_supports_grpo_quality = claim(
    "**The 3-way RM is what makes the per-expert GRPO step "
    "stable.** Without the Format RM, the policy quickly emits "
    "ill-formed primitives that downstream parsers cannot use; "
    "without the Quality RM, the policy reward-hacks (it learns "
    "to spam syntactically-legal primitives that shortcut the "
    "task); without Task-Specific Accuracy, the policy has no "
    "ground-truth anchor. All three are required for the GRPO "
    "rollouts to converge on policies that emit primitives "
    "*precisely* and *purposefully*.",
    title="Function: 3-way RM is the precondition for stable per-expert GRPO",
)

__all__ = [
    "setup_three_way_rm",
    "claim_format_rm",
    "claim_quality_rm",
    "claim_task_accuracy_rm",
    "claim_rm_decomposition_rationale",
    "claim_rm_supports_grpo_quality",
]
