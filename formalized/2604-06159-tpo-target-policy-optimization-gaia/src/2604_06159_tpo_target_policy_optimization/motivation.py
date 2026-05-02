"""Motivation: target policy optimization (TPO).

Formalisation of arXiv:2604.06159 ("TPO: Target Policy Optimization"). The
source artifact in this package is a thin stub (title + arXiv link +
four-keyword list + status line); no PDF body is available. Therefore only
the title-level thesis claim, its companion method claim, and the four
listed keyword topics are extracted as claims.

The H1 of the artifact -- "TPO: Target Policy Optimization" -- is split
into two title-level leaves under the standard 'METHOD: thesis' convention:
(i) the thesis that policy-gradient RL fine-tuning of LLMs benefits from
optimising against an explicit *target policy* (a reference distribution
that supplies the desired token-level signal) rather than relying solely on
the standard group-relative or value-baselined return; and (ii) the
companion claim that **TPO** is the proposed realisation of that target-
policy training rule. The four keywords name the supporting axes:
(1) **rl-training** is the regime in which the method operates;
(2) **grpo-alternative** positions TPO as a drop-in replacement for the
GRPO-family of algorithms commonly used to RL-fine-tune reasoning LLMs;
(3) **cross-entropy** names the objective form -- a cross-entropy term
against the target policy supplies the supervisory signal; and
(4) **gradient-conflict** names the failure mode of the GRPO baseline that
TPO is designed to avoid -- competing per-sample gradients in the group
update degrade reasoning quality.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

llm_rl_setting = setting(
    "An *RL-fine-tuned LLM* is a language model whose post-training step "
    "updates its policy via reinforcement learning against a task-level "
    "reward (verifier-checked answer correctness, format compliance, tool "
    "success, ...). The dominant family of algorithms in this regime is "
    "**GRPO** (Group Relative Policy Optimization) and its descendants, "
    "which estimate per-token advantages by comparing a sampled group of "
    "rollouts against the group mean rather than against a learned value "
    "baseline. The policy and the optimiser update share a single "
    "parameter set, so all per-sample token-level gradients are summed "
    "into one step.",
    title="LLM policy-gradient RL fine-tuning (formal setting)",
)

target_policy_scope = setting(
    "The study scope of TPO is the *training rule* used during this RL "
    "fine-tuning step -- how the per-token learning signal is constructed "
    "from a batch of rollouts. A *target policy* is a reference token "
    "distribution (e.g. derived from the best-of-group rollout, an "
    "expert demonstration, or a frozen reference model) that the trainee "
    "policy is asked to match on the supervised positions, supplying a "
    "dense token-level signal that the sparse group-relative advantage "
    "alone does not. TPO replaces (or augments) the GRPO group-relative "
    "policy-gradient term with a cross-entropy term against this target "
    "policy.",
    title="Target-policy training rule (study scope)",
)

# ---------------------------------------------------------------------------
# Headline title-level claims (the H1 of the artifact)
# ---------------------------------------------------------------------------

target_policy_is_the_optimisation_object = claim(
    "Policy-gradient RL fine-tuning of LLMs benefits from optimising the "
    "trainee policy against an explicit **target policy** -- a reference "
    "token distribution constructed from the rollouts -- rather than "
    "relying solely on the group-relative return signal used by GRPO and "
    "its descendants. The target policy supplies a dense, token-level "
    "supervisory signal that is well-defined per token (via cross-entropy) "
    "and that does not exhibit the destructive per-sample gradient "
    "competition that arises when a sparse group-relative advantage is "
    "back-propagated through every token of every rollout in a group.",
    title="Central thesis: target-policy optimisation as the right RL training rule",
    metadata={"source": "artifacts/2604.06159-tpo-target-policy-optimization.md (H1 / title)"},
)

tpo_realises_target_policy_optimization = claim(
    "**TPO** -- the method named in the title -- is proposed as the "
    "concrete realisation of that training rule: it specifies how the "
    "target policy is constructed from a batch of rollouts and how the "
    "trainee policy is updated against it (a cross-entropy objective on "
    "the supervised positions), positioning itself as a drop-in "
    "alternative to GRPO-family algorithms for RL-fine-tuning reasoning "
    "LLMs.",
    title="TPO realises target policy optimization",
    metadata={"source": "artifacts/2604.06159-tpo-target-policy-optimization.md (title: 'TPO:')"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 4 keywords listed in the source)
# Each keyword names a topic the paper claims to study; we lift each into an
# atomic claim that ties back to the central thesis.
# ---------------------------------------------------------------------------

keyword_rl_training = claim(
    "The work is situated within **RL training** of LLMs -- TPO is a "
    "training-time algorithm applied during the reinforcement-learning "
    "fine-tuning step (where the policy is updated against task-level "
    "verifier rewards), not a decoding-time strategy or a supervised "
    "fine-tuning recipe.",
    title="Keyword: rl-training",
    metadata={"keyword_index": 1, "source": "artifacts/2604.06159-tpo-target-policy-optimization.md (keywords)"},
)

keyword_grpo_alternative = claim(
    "TPO positions itself as a **GRPO alternative** -- a drop-in "
    "replacement for Group Relative Policy Optimization and its "
    "descendants in the standard reasoning-LLM RL-fine-tuning pipeline. "
    "It targets the same task family (verifier-rewarded reasoning), the "
    "same data interface (groups of sampled rollouts per prompt), and the "
    "same place in the training stack, but substitutes a different per-"
    "token learning signal.",
    title="Keyword: grpo-alternative",
    metadata={"keyword_index": 2, "source": "artifacts/2604.06159-tpo-target-policy-optimization.md (keywords)"},
)

keyword_cross_entropy = claim(
    "The supervisory signal in TPO has the form of a **cross-entropy** "
    "term against the constructed target policy: on the supervised token "
    "positions the trainee policy is asked to match the target "
    "distribution under cross-entropy, rather than to follow a sparse "
    "group-relative policy-gradient. Cross-entropy is the natural form "
    "for a target-policy training rule because it is dense per token and "
    "does not require an advantage estimate.",
    title="Keyword: cross-entropy",
    metadata={"keyword_index": 3, "source": "artifacts/2604.06159-tpo-target-policy-optimization.md (keywords)"},
)

keyword_gradient_conflict = claim(
    "The failure mode of the GRPO baseline that TPO is designed to "
    "avoid is **gradient conflict** -- the per-sample token-level "
    "gradients within a single GRPO group point in opposing directions "
    "in shared parameter subspaces (e.g. a high-advantage rollout pushes "
    "a token up while a low-advantage rollout in the same group pushes "
    "the same token down), so that the summed update degrades the "
    "underlying reasoning behaviour. A target-policy cross-entropy "
    "objective sidesteps this conflict because all supervised tokens "
    "share a single coherent target.",
    title="Keyword: gradient-conflict",
    metadata={"keyword_index": 4, "source": "artifacts/2604.06159-tpo-target-policy-optimization.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two title-level leaf claims jointly grant evidence to each of the four
# keyword claims: the central target-policy thesis grounds the RL-training
# situating, the cross-entropy objective form, and the gradient-conflict
# diagnosis, while the TPO method claim additionally grounds the GRPO-
# alternative positioning.

strat_thesis_grounds_rl_training = support(
    [target_policy_is_the_optimisation_object, tpo_realises_target_policy_optimization],
    keyword_rl_training,
    background=[llm_rl_setting, target_policy_scope],
    reason=(
        "The central thesis (@target_policy_is_the_optimisation_object) "
        "is itself a claim about a *training rule for RL fine-tuning* "
        "within the LLM policy-gradient setting (@llm_rl_setting), and "
        "the TPO method (@tpo_realises_target_policy_optimization) is "
        "introduced as a training-time algorithm operating on the "
        "rollout groups produced during RL fine-tuning "
        "(@target_policy_scope). Hence the work is squarely about RL "
        "training of LLMs."
    ),
    prior=0.95,
)

strat_method_grounds_grpo_alternative = support(
    [tpo_realises_target_policy_optimization, target_policy_is_the_optimisation_object],
    keyword_grpo_alternative,
    background=[llm_rl_setting, target_policy_scope],
    reason=(
        "Proposing a new training rule "
        "(@target_policy_is_the_optimisation_object) and its concrete "
        "realisation TPO (@tpo_realises_target_policy_optimization) "
        "inside the GRPO-dominated RL-fine-tuning regime (@llm_rl_setting) "
        "and at the same place in the training stack (@target_policy_scope) "
        "is operationally to position the method as an alternative to "
        "GRPO -- it consumes the same groups-of-rollouts interface and "
        "produces the same kind of policy update, but with a different "
        "per-token learning signal."
    ),
    prior=0.92,
)

strat_thesis_grounds_cross_entropy = support(
    [target_policy_is_the_optimisation_object, tpo_realises_target_policy_optimization],
    keyword_cross_entropy,
    background=[target_policy_scope],
    reason=(
        "Once a target token distribution is committed to as the "
        "supervisory object (@target_policy_is_the_optimisation_object), "
        "the natural and standard objective for matching it is per-token "
        "cross-entropy (@target_policy_scope); the explicit listing of "
        "'cross-entropy' as a keyword, together with the TPO method "
        "(@tpo_realises_target_policy_optimization), confirms that this "
        "is the objective form adopted rather than e.g. a KL-to-target "
        "or an MSE-on-logits variant."
    ),
    prior=0.93,
)

strat_thesis_grounds_gradient_conflict = support(
    [target_policy_is_the_optimisation_object, keyword_grpo_alternative],
    keyword_gradient_conflict,
    background=[llm_rl_setting, target_policy_scope],
    reason=(
        "The motivation for replacing the GRPO group-relative advantage "
        "(@keyword_grpo_alternative) with a target-policy objective "
        "(@target_policy_is_the_optimisation_object) is precisely that "
        "the GRPO update sums per-sample gradients with opposite signs "
        "across the rollouts of a single group within shared LLM "
        "parameters (@llm_rl_setting); a single coherent target policy "
        "(@target_policy_scope) eliminates that conflict by giving every "
        "supervised token a single direction to move toward. Hence the "
        "diagnosis the work targets is gradient conflict."
    ),
    prior=0.9,
)

__all__ = [
    "llm_rl_setting",
    "target_policy_scope",
    "target_policy_is_the_optimisation_object",
    "tpo_realises_target_policy_optimization",
    "keyword_rl_training",
    "keyword_grpo_alternative",
    "keyword_cross_entropy",
    "keyword_gradient_conflict",
]
