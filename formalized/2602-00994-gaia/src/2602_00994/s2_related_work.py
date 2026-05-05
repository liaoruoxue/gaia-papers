"""Section 2: Related Work.

Two strands: (i) ARL with tool-use, where prior systems jointly fine-tune
without studying interference between reasoning and tool-use; (ii) Multi-LoRA
methods, where prior systems use multiple LoRA adapters under a shared
backbone but cannot disentangle ability-level interference because adapters
are mixed softly.
"""

from gaia.lang import claim, setting, support

from .motivation import claim_joint_assumption_unexamined

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

setup_prior_arl_focus = setting(
    "Prior ARL research has focused on three complementary axes: (i) reward "
    "design that elicits emergent tool-use behaviour; (ii) policy refinement "
    "for action interleaving; (iii) large-scale trajectory synthesis for "
    "scalable training. Representative systems include Toolformer "
    "[@Schick2023], Search-R1 [@Jin2025], and DeepSeekMath [@Shao2024].",
    title="Setup: prior ARL focuses on rewards, policy, and trajectories",
)

setup_multi_lora_paradigm = setting(
    "The Multi-LoRA paradigm attaches several LoRA [@Hu2022] adapters to a "
    "shared frozen backbone. A *router* (learned or rule-based) decides "
    "which adapter(s) are active for a given input or token. Two main "
    "design families exist: (a) *router-driven mixtures* such as MixLoRA "
    "and MoELoRA, which softly combine adapter outputs; and (b) "
    "*task-specific selection*, such as LoRAHub and Modula, which dedicate "
    "one adapter to one task.",
    title="Setup: the Multi-LoRA paradigm",
)

# ---------------------------------------------------------------------------
# Claims about prior work's gap
# ---------------------------------------------------------------------------

claim_prior_arl_no_interference_study = claim(
    "Although prior ARL methods (Toolformer [@Schick2023], DeepSeekMath "
    "[@Shao2024], Search-R1 [@Jin2025], AgentTuning) optimize many "
    "components of the agent training pipeline, none of them empirically "
    "study whether reasoning and tool-use capabilities **interfere with "
    "each other** during joint optimization, or whether such interference "
    "could degrade overall performance. This is the gap the present paper "
    "fills with LEAS.",
    title="Prior ARL work does not study reasoning--tool interference",
    background=[setup_prior_arl_focus],
)

claim_multi_lora_cannot_disentangle = claim(
    "Router-driven Multi-LoRA methods (MixLoRA, MoELoRA, SiRA, MoLE) "
    "perform **soft expert mixing**: at each forward pass, the active "
    "adapters' outputs are linearly combined. Because gradients still flow "
    "through *all* mixed adapters proportionally to their routing weights, "
    "different abilities cannot be cleanly disentangled into disjoint "
    "parameter subspaces, so capability-level interference is not removed.",
    title="Soft expert mixing in Multi-LoRA does not disentangle interference",
    background=[setup_multi_lora_paradigm],
)

claim_task_lora_too_coarse = claim(
    "Task-specific Multi-LoRA methods (LoRAHub, Modula, Customizable PEFT) "
    "assign one adapter to all tokens of a given **task**. Within a single "
    "task, all token roles share one adapter, so reasoning and tool-use "
    "tokens of the same QA task still update the same low-rank subspace -- "
    "leaving the reasoning vs. tool-use interference unaddressed.",
    title="Task-level LoRA selection still mixes reasoning and tool-use",
    background=[setup_multi_lora_paradigm],
)

claim_dart_distinguishes_at_token = claim(
    "In contrast to both prior families, DART (this work) routes adapters "
    "at the **token** level *within a single ARL task*: each token "
    "activates exactly one of two disjoint LoRA adapters depending on "
    "whether it is a reasoning or a tool-use token. This token-granularity "
    "routing is what makes the disentanglement effective.",
    title="DART's distinction: token-level routing inside one task",
)

# ---------------------------------------------------------------------------
# Reasoning: prior-work gap (lack of interference study) supports the
# motivational claim that the joint-training assumption was unexamined.
# ---------------------------------------------------------------------------

strat_priorwork_unexamined = support(
    [claim_prior_arl_no_interference_study],
    claim_joint_assumption_unexamined,
    reason=(
        "If no prior ARL system has empirically tested whether reasoning "
        "and tool-use interfere under joint optimization "
        "(@claim_prior_arl_no_interference_study), then the implicit "
        "assumption underlying those systems -- that joint training "
        "improves overall performance -- has been adopted without "
        "empirical validation (@claim_joint_assumption_unexamined). The "
        "motivational claim is a direct consequence of the related-work "
        "gap."
    ),
    prior=0.95,
)

# Both Multi-LoRA failure modes (soft mixing + task-level routing) are
# independent reasons why prior Multi-LoRA work cannot achieve
# capability-level disentanglement. They jointly support the distinction
# claim that DART must operate at token granularity within one task.
strat_dart_token_distinction = support(
    [claim_multi_lora_cannot_disentangle, claim_task_lora_too_coarse],
    claim_dart_distinguishes_at_token,
    reason=(
        "Two independent gaps in prior Multi-LoRA work jointly motivate "
        "DART's token-level routing: soft expert mixing cannot disentangle "
        "interfering capabilities (@claim_multi_lora_cannot_disentangle), "
        "and per-task adapter selection still mixes reasoning and "
        "tool-use within a single task "
        "(@claim_task_lora_too_coarse). The only remaining axis at "
        "which to disentangle reasoning and tool-use within one ARL task "
        "is the token role -- which is what DART exploits "
        "(@claim_dart_distinguishes_at_token)."
    ),
    prior=0.92,
)

__all__ = [
    "setup_prior_arl_focus",
    "setup_multi_lora_paradigm",
    "claim_prior_arl_no_interference_study",
    "claim_multi_lora_cannot_disentangle",
    "claim_task_lora_too_coarse",
    "claim_dart_distinguishes_at_token",
]
