"""Section 4: CRAFT method -- LCLR + R2L.

CRAFT comprises two sequential phases:

1. **Latent Contrastive Learning for Reasoning (LCLR)** (Section 4.1) --
   structures the latent space of reasoning traces by combining a
   prototype triplet loss (geometric structure), an InfoNCE-style
   instance invariance loss [@Chen2020SimCLR] (semantic-vs-textual
   robustness), and a safety calibration loss (alignment to interpretable
   probability scores).
2. **Reinforcement over Reasoning Latents (R2L)** (Section 4.2) -- applies
   GRPO [@Ramesh2024GRPO; @Shao2024DeepSeekMath] with three rewards: a
   latent-semantic reward $R_{ls}$ (push hidden states toward the safety
   subspace), a textual safety reward $R_{txt}$ (StrongReject-based
   final-output safety [@Souly2024StrongReject]), and a latent-textual
   consistency reward $R_{cons}$ (synchronize latent and textual safety
   judgments).

The total reward is
$R_{total} = w_{lat} R_{ls} + w_{txt} R_{txt} + w_{cons} R_{cons}$
optimized by GRPO.

Source: [@Luo2026CRAFT, Sec. 4; Fig. 3].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Two-phase pipeline
# ---------------------------------------------------------------------------

setup_two_phase_pipeline = setting(
    "**CRAFT pipeline: LCLR (Phase 1) followed by R2L (Phase 2).** "
    "Phase 1 trains the projection head and prototypes via contrastive "
    "objectives to produce a structured safety latent space. Phase 2 "
    "freezes (or co-trains) the contrastive components and runs GRPO "
    "[@Ramesh2024GRPO] policy optimization with rewards defined over "
    "the structured latent space and the final output. Phase 2's "
    "rewards $R_{ls}$ and $R_{cons}$ cannot be computed without Phase "
    "1's structured latent space.",
    title="Setup: CRAFT is a two-phase pipeline (LCLR -> R2L)",
)

# ---------------------------------------------------------------------------
# LCLR (Section 4.1)
# ---------------------------------------------------------------------------

setup_lclr_total_objective = setting(
    "**LCLR total objective.** The Latent Contrastive Learning for "
    "Reasoning loss is the linear combination "
    "$\\mathcal{L}_{LCLR} = \\mathcal{L}_{proto} + "
    "\\lambda_{inst} \\mathcal{L}_{inst} + "
    "\\lambda_{cal} \\mathcal{L}_{cal}$ "
    "(Eq. 4.1), where $\\lambda_{inst}$ and $\\lambda_{cal}$ are "
    "hyperparameters controlling the contribution of instance "
    "invariance and safety calibration respectively. "
    "$\\mathcal{L}_{proto}$ enforces geometric structure between the "
    "three semantic clusters; $\\mathcal{L}_{inst}$ enforces "
    "invariance to superficial textual variations within the same "
    "trace; $\\mathcal{L}_{cal}$ calibrates the latent to a "
    "probabilistic safety score.",
    title="Setup: LCLR objective L_LCLR = L_proto + lambda_inst*L_inst + lambda_cal*L_cal",
)

setup_proto_loss = setting(
    "**Structured Geometric Alignment ($\\mathcal{L}_{proto}$).** A "
    "margin-based triplet loss with rethink anchoring: "
    "$\\mathcal{L}_{proto} = \\max(0, \\eta - z^\\top \\mu_{safe} + "
    "z^\\top \\mu_{unsafe}) + \\gamma_{rt}(1 - z^\\top \\mu_{rethink})$, "
    "where $\\eta$ is a margin hyperparameter ensuring separability "
    "between extreme behaviors, and $\\gamma_{rt}$ weights the "
    "alignment of rethink traces. The triplet term encourages safe "
    "traces toward $\\mu_{safe}$ and away from $\\mu_{unsafe}$ by at "
    "least margin $\\eta$; the rethink anchor pulls intermediate "
    "traces to $\\mu_{rethink}$. Together they construct a continuous "
    "'safety manifold'.",
    title="Setup: L_proto = triplet loss + rethink anchor (continuous safety manifold)",
)

setup_inst_loss = setting(
    "**Instance-Level Invariance ($\\mathcal{L}_{inst}$).** Inspired by "
    "SimCLR [@Chen2020SimCLR], two augmented views $z_i, z_j$ of the "
    "*same* reasoning trace (generated via token dropout or "
    "paraphrasing) are treated as positives, and all other in-batch "
    "samples as negatives. The InfoNCE objective "
    "$\\mathcal{L}_{inst} = -\\log \\frac{\\exp(z_i^\\top z_j / "
    "\\tau_{temp})}{\\sum_{k=1}^{2N} \\exp(z_i^\\top z_k / \\tau_{temp})}$ "
    "with temperature $\\tau_{temp}$ and batch size $N$ encourages the "
    "latent to be invariant to *superficial* textual variations rather "
    "than to *semantic* changes in reasoning.",
    title="Setup: L_inst = InfoNCE on augmented views (invariance to surface variation)",
)

setup_cal_loss = setting(
    "**Latent Safety Calibration ($\\mathcal{L}_{cal}$).** A safety "
    "scorer $g_\\psi : \\mathbb{R}^k \\to [0, 1]$ maps latent vectors "
    "to soft labels $y_{soft} \\in \\{0, 0.5, 1\\}$ corresponding to "
    "the {unsafe, rethink, safe} hierarchy. The loss combines binary "
    "cross-entropy with KL distillation from a frozen textual safety "
    "verifier $p_{text}$: "
    "$\\mathcal{L}_{cal} = \\text{BCE}(g_\\psi(z), y_{soft}) + "
    "\\beta_{dist} \\cdot \\text{KL}(p_{text} \\| g_\\psi(z))$. "
    "This forces smooth traversals of latent space to correspond to "
    "calibrated, monotonic changes in safety probability.",
    title="Setup: L_cal = BCE + KL distillation from text verifier (interpretable safety scoring)",
)

claim_lclr_design_rationale = claim(
    "**LCLR's three-loss design rationale: each component addresses a "
    "distinct alignment failure mode.** "
    "$\\mathcal{L}_{proto}$ ensures *geometric* separation (preventing "
    "safe and unsafe latents from collapsing to the same region); "
    "$\\mathcal{L}_{inst}$ ensures *robustness* (so that paraphrasing "
    "the harmful prompt does not slide the latent across the safety "
    "boundary); $\\mathcal{L}_{cal}$ ensures *interpretability* (the "
    "latent corresponds to a probabilistic safety score with smooth "
    "traversals). All three are needed: removing $\\mathcal{L}_{proto}$ "
    "loses the geometric structure used by R2L; removing "
    "$\\mathcal{L}_{inst}$ leaves the latent vulnerable to "
    "paraphrase attacks; removing $\\mathcal{L}_{cal}$ decouples the "
    "latent from a usable safety probability "
    "[@Luo2026CRAFT, Sec. 4.1].",
    title="LCLR rationale: each of the three losses addresses a distinct failure mode",
)

# ---------------------------------------------------------------------------
# R2L (Section 4.2)
# ---------------------------------------------------------------------------

setup_r2l_objective_form = setting(
    "**R2L total reward and GRPO optimization.** R2L is built on Group "
    "Relative Policy Optimization (GRPO) [@Ramesh2024GRPO; "
    "@Shao2024DeepSeekMath]. The total reward "
    "$R_{total} = w_{lat} R_{ls} + w_{txt} R_{txt} + w_{cons} R_{cons}$ "
    "(Eq. 4.2) is a positively-weighted combination of three "
    "components: latent-semantic ($R_{ls}$), textual safety "
    "($R_{txt}$), and latent-textual consistency ($R_{cons}$). Weights "
    "$w_{lat}, w_{txt}, w_{cons}$ are positive scalars controlling the "
    "relative contribution of each component.",
    title="Setup: R2L total reward (Eq. 4.2) optimized by GRPO",
)

setup_latent_semantic_reward = setting(
    "**Latent Semantic Reward ($R_{ls}$).** The reward measures "
    "geometric distance of the hidden state $h$ to three curated "
    "semantic regions. Given the projected latent $z = \\phi(h)$, the "
    "reward is "
    "$R_{ls}(z) = \\alpha \\cos(z, \\mu_{safe}) - "
    "\\beta \\cos(z, \\mu_{unsafe}) + \\gamma \\cos(z, \\mu_{rethink})$, "
    "where $\\cos(u,v) = u^\\top v / (\\|u\\|_2 \\|v\\|_2)$ is cosine "
    "similarity and $\\alpha, \\beta, \\gamma$ are tightness "
    "coefficients. Inspired by cosine reward mechanisms "
    "[@Yang2025bDemystifyingLongCoT].",
    title="Setup: R_ls = alpha*cos(z,mu_safe) - beta*cos(z,mu_unsafe) + gamma*cos(z,mu_rethink)",
)

setup_textual_safety_reward = setting(
    "**Textual Safety Reward ($R_{txt}$).** Lets $P(S|y) \\in [0,1]$ "
    "denote the probability that the generated text $y$ is safe "
    "according to the StrongReject [@Souly2024StrongReject] safety "
    "evaluator. To provide a symmetric, zero-centered gradient signal, "
    "$R_{txt} = 2 \\cdot P(S|y) - 1 \\in [-1, 1]$. This penalizes "
    "policy violations sharply while rewarding safe outputs.",
    title="Setup: R_txt = 2 * P(S|y) - 1 from StrongReject score",
)

setup_consistency_reward = setting(
    "**Latent-Textual Consistency Reward ($R_{cons}$).** Let $p_z = "
    "\\sigma(\\psi(z))$ be the safety probability predicted directly "
    "from the latent space by a safety head $\\psi$, and $p_y = "
    "P(S|y)$ the textual safety score. The consistency reward is "
    "defined as the L1 distance: "
    "$R_{cons} = 1 - |p_z - p_y| \\in [0, 1]$. Maximizing $R_{cons}$ "
    "synchronizes internal-state safety judgment with external safety "
    "judgment, addressing the representation-output mismatch that "
    "underlies SSA.",
    title="Setup: R_cons = 1 - |p_z - p_y| (latent-textual consistency)",
)

claim_three_rewards_address_distinct_objectives = claim(
    "**The three R2L rewards address three distinct objectives.** "
    "$R_{ls}$ aligns *intermediate* reasoning traces by driving hidden "
    "representations toward the safety subspace. $R_{txt}$ ensures the "
    "*final response* adheres to safety policies. $R_{cons}$ enforces "
    "*coherence* between intermediate reasoning and final output, "
    "directly targeting the SSA failure mode in which one is safe "
    "while the other is not. Each addresses a different aspect of the "
    "alignment problem; the theorem in Section 5 explicitly relies on "
    "$R_{cons}$ being part of the total reward "
    "[@Luo2026CRAFT, Sec. 4.2].",
    title="R2L design: each of three rewards addresses a distinct alignment objective",
)

claim_rcons_targets_ssa = claim(
    "**$R_{cons}$ is the component that directly addresses SSA.** "
    "Superficial safety alignment is, by definition, the case where "
    "$p_y$ is close to 1 (output safe) but $p_z$ is far from $p_y$ "
    "(latent unsafe). The consistency reward $R_{cons} = 1 - |p_z - "
    "p_y|$ is *minimized* under SSA and *maximized* when latent and "
    "textual safety judgments agree. By including $R_{cons}$ in the "
    "policy-optimization total reward, R2L places explicit "
    "optimization pressure against SSA -- this is the reward component "
    "the Section 5 theorem leverages "
    "[@Luo2026CRAFT, Sec. 4.2; Sec. 5].",
    title="Argument: R_cons is the SSA-targeting reward component in R2L",
)

# ---------------------------------------------------------------------------
# Overall framework (Fig. 3)
# ---------------------------------------------------------------------------

claim_craft_overall_pipeline = claim(
    "**CRAFT overall pipeline (Fig. 3).** The end-to-end framework "
    "operates as follows: (1) **Phase 1 (LCLR)** -- given a batch of "
    "reasoning traces with semantic labels, the projection head "
    "$f_\\omega$ produces normalized latents $z$, and prototypes "
    "$\\mu_c$ are EMA-updated; the LCLR loss "
    "$\\mathcal{L}_{LCLR}$ is minimized. (2) **Phase 2 (R2L)** -- "
    "given a prompt $x$, the policy $\\pi_\\theta$ generates a "
    "reasoning trace and final answer; $R_{ls}$ is computed from the "
    "trace's hidden states via $f_\\omega$ and the prototypes; "
    "$R_{txt}$ is computed from the safety evaluator; $R_{cons}$ is "
    "computed from the safety head $\\psi$ and the same evaluator; "
    "GRPO computes group-relative advantages and updates "
    "$\\pi_\\theta$ [@Luo2026CRAFT, Fig. 3].",
    title="Pipeline: end-to-end LCLR + R2L workflow per Fig. 3",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Figure 3",
        "caption": "Fig. 3: Overall pipeline: Phase 1 LCLR (latent contrastive learning), Phase 2 R2L (GRPO with latent-aware reward).",
    },
)

claim_craft_framework_contribution = claim(
    "**CRAFT integrates contrastive learning with reinforcement "
    "learning over latent representations.** Unlike previous "
    "training-time alignment baselines that operate solely over "
    "textual reasoning traces, CRAFT explicitly defines its "
    "optimization objective over the *hidden state space* (via "
    "$\\mathcal{L}_{proto}, \\mathcal{L}_{inst}, R_{ls}, R_{cons}$). "
    "The contrastive (LCLR) and RL (R2L) components are *complementary*: "
    "LCLR alone provides latent structure but no policy update; R2L "
    "alone has no structured latent space against which to compute "
    "$R_{ls}$ or $R_{cons}$. The integration is what enables "
    "reasoning-level safety alignment "
    "[@Luo2026CRAFT, Sec. 4].",
    title="Framework contribution: integration of contrastive (LCLR) + RL (R2L) over latents",
)

__all__ = [
    "setup_two_phase_pipeline",
    "setup_lclr_total_objective",
    "setup_proto_loss",
    "setup_inst_loss",
    "setup_cal_loss",
    "claim_lclr_design_rationale",
    "setup_r2l_objective_form",
    "setup_latent_semantic_reward",
    "setup_textual_safety_reward",
    "setup_consistency_reward",
    "claim_three_rewards_address_distinct_objectives",
    "claim_rcons_targets_ssa",
    "claim_craft_overall_pipeline",
    "claim_craft_framework_contribution",
]
