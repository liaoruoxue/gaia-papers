"""Section 5: Disentangled Action-Reasoning Tuning (DART).

Building on the LEAS finding that joint optimization of reasoning and
tool-use produces gradient-level conflict (Section 4), DART proposes an
architectural fix: freeze the pretrained backbone, attach two **disjoint**
LoRA adapters, and route each token to exactly one adapter according to its
role. As a result, reasoning and tool-use never share trainable parameters,
so the LEAS interaction indicator $x_{23}$ -- and therefore $\\lambda_{23}$ --
is structurally zero. Section also covers Remark 5.1 (why backbone freezing
does not sacrifice performance) and Appendix F (efficiency vs. 2-Agent).
"""

from gaia.lang import claim, setting, support

from .motivation import claim_contribution_dart
from .s2_related_work import (
    claim_multi_lora_cannot_disentangle,
    claim_dart_distinguishes_at_token,
)
from .s3_preliminaries import setup_lora, setup_role_router, setup_masked_objective
from .s4_leas import (
    claim_gradient_conflict_explains_interference,
    setup_interaction_indicators,
)

# ---------------------------------------------------------------------------
# 5.1 Architecture (settings)
# ---------------------------------------------------------------------------

setup_dart_architecture = setting(
    "**DART architecture (Eq. 10).** The pretrained weight matrix $W$ is "
    "**frozen**. Two disjoint LoRA [@Hu2022] adapters are attached to all "
    "linear layers: $\\theta_r = \\{B_r, A_r\\}$ for reasoning and "
    "$\\theta_a = \\{B_a, A_a\\}$ for tool-use. At each decoding step "
    "$t$, the role router $\\ell(t)$ (@setup_role_router) selects the "
    "active adapter $u_t \\in \\{r, a\\}$, and the forward pass becomes "
    "$h'_t = W h_t + B_{u_t} A_{u_t} h_t$ (Eq. 10). Token roles are "
    "identified by special markers (`<think>...</think>`, "
    "`<search>...</search>`).",
    title="DART forward pass (Eq. 10)",
)

setup_dart_routing_rule = setting(
    "**DART router.** The token-to-adapter mapping is **rule-based** (no "
    "learned router): structural special tokens demarcate reasoning vs "
    "tool-use vs loss-free segments. Reasoning tokens between `<think>` "
    "and `</think>` activate $\\theta_r$; tool-use tokens between "
    "`<search>` and `</search>` activate $\\theta_a$; tokens inside "
    "`<information>...</information>` blocks (tool feedback) and inside "
    "the `<answer>...</answer>` final answer are loss-free.",
    title="DART rule-based router (Fig. 4 / Fig. 7B)",
)

# ---------------------------------------------------------------------------
# Theoretical claims about DART's structure
# ---------------------------------------------------------------------------

claim_dart_zero_interaction = claim(
    "**Structural claim.** Because $\\theta_r$ and $\\theta_a$ are "
    "**disjoint** parameter sets and each token activates exactly one of "
    "them, the gradients of reasoning and tool-use tokens are applied to "
    "**different parameters**. Hence in DART's training, the LEAS "
    "interaction indicator $x_{23}$ defined in Section 4.1 satisfies "
    "$x_{23} = 0$ identically, and the corresponding interaction "
    "coefficient $\\lambda_{23}$ is effectively zero.",
    title="DART structurally enforces $x_{23} = 0$ ($\\lambda_{23} \\equiv 0$)",
    background=[setup_dart_architecture, setup_interaction_indicators],
)

claim_freeze_backbone_necessary = claim(
    "**Remark 5.1 (necessity of backbone freezing).** If $W$ were "
    "trainable, gradients from reasoning and tool-use tokens would both "
    "update $W$ and re-introduce the parameter-sharing that DART is "
    "designed to eliminate -- undermining the disentanglement. Therefore "
    "freezing $W$ is structurally required.",
    title="Backbone freezing is required for true disentanglement",
    background=[setup_dart_architecture],
)

claim_freeze_no_performance_loss = claim(
    "**Remark 5.1 (continued).** Freezing $W$ does not sacrifice "
    "performance, supported by two prior findings: (i) RL-based tuning "
    "primarily affects sparse subnetworks of the backbone "
    "[@Mukherjee2025], and (ii) LoRA can match full-parameter fine-tuning "
    "performance [@Schulman2025]. Both suggest that the effective "
    "RL-trainable subspace is small enough to be captured by low-rank "
    "adapters.",
    title="Backbone freezing does not sacrifice performance",
    background=[setup_lora],
)

claim_dart_distinct_from_moe = claim(
    "**DART is structurally distinct from MoE / soft Multi-LoRA.** Soft "
    "expert mixing (e.g. MoELoRA, MixLoRA, MoLE) routes inputs to a "
    "*weighted combination* of adapters; gradients flow through every "
    "non-zero-weight adapter, so capability-level gradients still mix in "
    "every adapter. DART instead enforces a **hard, mutually exclusive** "
    "routing -- exactly one adapter per token -- which is what makes "
    "$x_{23} = 0$ achievable.",
    title="DART vs MoE: hard routing is what enforces disentanglement",
)

# Wire claim_dart_distinct_from_moe -> from soft mixing failure + token-level
# routing distinction (s2 related work).
strat_dart_distinct = support(
    [claim_multi_lora_cannot_disentangle, claim_dart_distinguishes_at_token],
    claim_dart_distinct_from_moe,
    reason=(
        "Soft expert mixing in router-driven Multi-LoRA cannot remove "
        "capability-level interference because gradients still flow "
        "through every active adapter (@claim_multi_lora_cannot_disentangle). "
        "DART instead applies hard token-level routing within a single "
        "task (@claim_dart_distinguishes_at_token). The combination of "
        "these two facts -- soft mixing fails, DART uses hard routing -- "
        "is exactly what makes DART structurally distinct from MoE-style "
        "approaches."
    ),
    prior=0.92,
)

# ---------------------------------------------------------------------------
# DART vs 2-Agent (Appendix F) -- efficiency claims
# ---------------------------------------------------------------------------

setup_2agent_baseline = setting(
    "**2-Agent baseline (Appendix F, Fig. 8).** A reference architecture "
    "with **two independent full models**: $\\mathcal{M}_\\text{Reas}$ "
    "produces reasoning tokens, $\\mathcal{M}_\\text{Tool}$ executes "
    "tool calls. Models communicate via explicit handoffs orchestrated "
    "externally. This represents *full* parameter disentanglement and "
    "serves as an **upper bound** on what disentanglement can achieve.",
    title="2-Agent system: two full models, hard handoffs (Fig. 8)",
)

setup_efficiency_setup = setting(
    "Let $P$ be the number of backbone parameters and $p$ the number of "
    "LoRA-adapter parameters, with $p \\ll P$ (typically $p < 0.005 P$). "
    "BF16 stores parameters and gradients (2 bytes/param), FP32 stores "
    "Adam optimizer states (8 bytes/param). Sequence length is $L$.",
    title="Efficiency analysis assumptions",
)

claim_2agent_memory_8x = claim(
    "**Theoretical training memory (Appendix F, Table 5).** Under the "
    "LoRA-augmented GRPO setup, the dominant static GPU memory cost of "
    "the 2-Agent baseline is $O(P_{\\text{2-agent}}) \\approx "
    "2 \\times 4P = 8P$ (two trainable backbones, each storing weights + "
    "gradients + optimizer states). DART's cost is $O(P_\\text{DART}) "
    "\\approx P + O(p) \\approx P$. The empirically observed memory "
    "ratio is approximately $8\\times$.",
    title="DART uses ~8x less training-time GPU memory than 2-Agent",
    background=[setup_2agent_baseline, setup_efficiency_setup],
    metadata={"source_table": "artifacts/2602.00994.pdf, Appendix F Table 5"},
)

claim_2agent_kv_recompute = claim(
    "**Inference latency (Appendix F).** When $\\mathcal{M}_\\text{Reas}$ "
    "in a 2-Agent system hands off to $\\mathcal{M}_\\text{Tool}$, the "
    "second model must **re-encode** the entire conversation history of "
    "length $L$ to populate its own KV-cache, costing $O(L^2)$ per "
    "context switch. DART, by contrast, operates on a single shared "
    "backbone, so the KV-cache remains valid across LoRA switches; "
    "swapping the active adapter ranks costs $O(1)$.",
    title="DART avoids $O(L^2)$ KV-cache recompute per context switch",
    background=[setup_2agent_baseline],
)

claim_dart_simpler_stack = claim(
    "**Deployment.** A 2-Agent stack requires an **external orchestrator** "
    "to synchronize states and reformat prompts between the two models. "
    "DART internalizes the routing within a single inference pipeline, "
    "removing the orchestrator dependency.",
    title="DART removes the multi-model orchestrator dependency",
    background=[setup_2agent_baseline],
)

# Synthesis: DART is more efficient than 2-Agent across three dimensions.
claim_dart_more_efficient_than_2agent = claim(
    "**Synthesis (Appendix F).** DART is strictly more efficient than the "
    "2-Agent baseline along three independent axes: training-time GPU "
    "memory ($\\sim 8\\times$ smaller, @claim_2agent_memory_8x), "
    "inference latency ($O(1)$ adapter swap vs $O(L^2)$ KV-cache "
    "recompute, @claim_2agent_kv_recompute), and deployment complexity "
    "(no external orchestrator needed, @claim_dart_simpler_stack). The "
    "performance trade-off is small (DART within ~1 EM of 2-Agent, see "
    "Section 6.3).",
    title="DART is more efficient than 2-Agent across memory, latency, deployment",
)

strat_dart_efficiency = support(
    [
        claim_2agent_memory_8x,
        claim_2agent_kv_recompute,
        claim_dart_simpler_stack,
    ],
    claim_dart_more_efficient_than_2agent,
    reason=(
        "The three independent efficiency advantages -- $\\sim 8\\times$ "
        "less training-time memory (@claim_2agent_memory_8x), "
        "$O(1)$ vs $O(L^2)$ context-switch latency "
        "(@claim_2agent_kv_recompute), and removal of the external "
        "orchestrator (@claim_dart_simpler_stack) -- jointly establish "
        "DART as a strictly more efficient deployment of the "
        "disentangled-capability idea than 2-Agent."
    ),
    prior=0.95,
)

# ---------------------------------------------------------------------------
# Synthesis: DART addresses the LEAS-identified bottleneck
# ---------------------------------------------------------------------------

claim_dart_solves_gradient_conflict = claim(
    "**Synthesis.** Because reasoning and tool-use gradients are routed "
    "to disjoint parameter subsets ($\\theta_r$ vs $\\theta_a$) -- which "
    "is enforced by the hard router (@setup_dart_routing_rule), the "
    "frozen backbone (@claim_freeze_backbone_necessary), and the disjoint "
    "adapter design (@setup_dart_architecture) -- the gradient compromise "
    "identified by LEAS as the cause of interference "
    "(@claim_gradient_conflict_explains_interference) cannot occur. Each "
    "capability's gradient updates only its own adapter, eliminating the "
    "mechanistic source of $\\lambda_{23} < 0$.",
    title="DART eliminates the gradient compromise underlying LEAS interference",
)

strat_dart_solves_conflict = support(
    [
        claim_dart_zero_interaction,
        claim_freeze_backbone_necessary,
        claim_gradient_conflict_explains_interference,
    ],
    claim_dart_solves_gradient_conflict,
    reason=(
        "LEAS attributes the negative $\\lambda_{23}$ to a gradient "
        "compromise in shared parameters "
        "(@claim_gradient_conflict_explains_interference). DART "
        "structurally guarantees $x_{23} = 0$ "
        "(@claim_dart_zero_interaction) by routing each token to a "
        "disjoint adapter and freezing the backbone "
        "(@claim_freeze_backbone_necessary). The same gradients still "
        "exist, but they are written into different parameter subsets, "
        "so the orthogonality observed in Fig. 3 cannot translate into "
        "destructive interference in the update."
    ),
    prior=0.9,
    background=[setup_dart_architecture, setup_dart_routing_rule],
)

# ---------------------------------------------------------------------------
# Top-level claim that DART is the proposed contribution
# ---------------------------------------------------------------------------

strat_dart_contribution = support(
    [
        claim_dart_zero_interaction,
        claim_freeze_backbone_necessary,
        claim_freeze_no_performance_loss,
        claim_dart_distinct_from_moe,
    ],
    claim_contribution_dart,
    reason=(
        "DART's contribution is the *combination* of: (i) hard "
        "token-level routing to disjoint LoRA adapters yielding "
        "$x_{23} = 0$ (@claim_dart_zero_interaction); (ii) the structural "
        "necessity of freezing the backbone for the disentanglement to "
        "be meaningful (@claim_freeze_backbone_necessary); (iii) the "
        "absence of a performance penalty from freezing "
        "(@claim_freeze_no_performance_loss, citing [@Mukherjee2025; "
        "@Schulman2025]); and (iv) the distinction from soft Multi-LoRA / "
        "MoE methods (@claim_dart_distinct_from_moe). Together these make "
        "DART a *single-model* solution to the joint-training "
        "interference identified by LEAS [@Li2026]."
    ),
    prior=0.9,
)

__all__ = [
    # settings
    "setup_dart_architecture",
    "setup_dart_routing_rule",
    "setup_2agent_baseline",
    "setup_efficiency_setup",
    # claims
    "claim_dart_zero_interaction",
    "claim_freeze_backbone_necessary",
    "claim_freeze_no_performance_loss",
    "claim_dart_distinct_from_moe",
    "claim_2agent_memory_8x",
    "claim_2agent_kv_recompute",
    "claim_dart_simpler_stack",
    "claim_dart_more_efficient_than_2agent",
    "claim_dart_solves_gradient_conflict",
]
