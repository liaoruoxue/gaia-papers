"""Section 3: Safety Spaces in Reasoning Models -- formal setup and the
latent-separation observation.

This module formalizes:

1. The mathematical setup: prompt x, reasoning trace tau, hidden state h,
   projection head f_omega, normalized latent z, semantic label
   y in {Unsafe, Rethink, Safe}, learnable class-wise prototypes mu_c
   updated via EMA [@Klinker2011EMA].
2. The probe protocol: Qwen3-4B-Thinking [@Yang2025Qwen3] as probe model on
   prompt-response pairs from R2D-R1 [@Zhu2025R2D] under unethical jailbreak
   prompts; PCA [@Ivosev2008PCA] visualization.
3. The empirical *observation* (claim, not setting): safe and unsafe traces
   occupy clearly separated regions of the latent space; rethink traces
   concentrate near the boundary.

Source: [@Luo2026CRAFT, Sec. 3].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Mathematical setup (definitions only -- these are settings)
# ---------------------------------------------------------------------------

setup_reasoning_trace_notation = setting(
    "**Reasoning-trace notation.** Let $x$ denote an input prompt and "
    "$\\tau = (y_1, \\ldots, y_T)$ the autoregressively generated "
    "reasoning trace from a policy $\\pi_\\theta$. The hidden state of "
    "the *final* reasoning token is denoted $h \\in \\mathbb{R}^d$ "
    "(where $d$ is the model's hidden dimension). The latent "
    "representation used for safety analysis is the final-token hidden "
    "state.",
    title="Setup: notation for reasoning trace tau and final-token hidden state h",
)

setup_projection_head = setting(
    "**Projection head and latent hypersphere.** A learnable projection "
    "head $f_\\omega : \\mathbb{R}^d \\to \\mathbb{R}^k$ maps the "
    "hidden state $h$ to a normalized latent vector "
    "$z = f_\\omega(h) \\in \\mathbb{R}^k$ with $\\|z\\|_2 = 1$. All "
    "latent-space objectives operate on $z$.",
    title="Setup: projection head f_omega producing unit-norm latent z",
)

setup_semantic_labels = setting(
    "**Semantic safety labels.** Each reasoning trace is associated "
    "with a discrete semantic label $y \\in \\{\\text{Unsafe}, "
    "\\text{Rethink}, \\text{Safe}\\}$. The Rethink label captures "
    "traces with *indeterminate* safety -- transitional reasoning "
    "states between aligned and violating behaviors.",
    title="Setup: three-way safety labels {Unsafe, Rethink, Safe}",
)

setup_prototypes = setting(
    "**Class-wise prototypes.** The framework maintains learnable "
    "class-wise prototypes $\\mu_{\\text{Unsafe}}$, "
    "$\\mu_{\\text{Rethink}}$, $\\mu_{\\text{Safe}} \\in \\mathbb{R}^k$ "
    "for each safety category $c$. The prototypes are updated via "
    "exponential moving average (EMA) [@Klinker2011EMA] over the "
    "training batches' projected latents to ensure training stability.",
    title="Setup: EMA-updated class-wise prototypes mu_c (Unsafe / Rethink / Safe)",
)

setup_probe_protocol = setting(
    "**Latent-space probe protocol.** As an illustrative case, the "
    "paper uses Qwen3-4B-Thinking [@Yang2025Qwen3] as a probe model "
    "and examines prompt-response pairs from R2D-R1 [@Zhu2025R2D]. "
    "Under unethical jailbreak prompts, the authors extract safe, "
    "unsafe, and rethink reasoning traces (where rethink denotes "
    "indeterminate safety), enabling a controlled comparison of their "
    "latent representations. The latents are projected to two "
    "dimensions using PCA [@Ivosev2008PCA] for visualization.",
    title="Setup: probe protocol (Qwen3-4B-Thinking + R2D-R1 + PCA)",
)

# ---------------------------------------------------------------------------
# Empirical observation (claim, can be questioned)
# ---------------------------------------------------------------------------

claim_safe_unsafe_separation = claim(
    "**Empirical observation: safe and unsafe reasoning traces occupy "
    "clearly separated regions of the final-token hidden-state PCA "
    "projection.** On both DeepSeek-R1-Distill-Llama-8B "
    "[@Guo2025DeepSeekR1] (Figure 2 left) and Qwen3-4B-Thinking "
    "[@Yang2025Qwen3] (Figure 2 right), the PCA projection of the "
    "final-token hidden state shows distinct clusters for safe vs. "
    "unsafe reasoning traces under jailbreak prompts. The separation "
    "appears in both backbone models, indicating a model-agnostic "
    "structural property [@Luo2026CRAFT, Sec. 3; Fig. 2].",
    title="Observation: safe vs. unsafe latent clusters are clearly separated (model-agnostic)",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Figure 2",
        "caption": "Fig. 2: PCA of final-token hidden states; safe (green) and unsafe (red) clusters separated; rethink (yellow) on the boundary, in both R1-Distill-Llama-8B and Qwen3-4B-Thinking.",
    },
)

claim_rethink_at_boundary = claim(
    "**Empirical observation: rethink traces concentrate at the "
    "boundary between safe and unsafe regions.** In Figure 2 of "
    "[@Luo2026CRAFT], the rethink cluster does not occupy a third "
    "disjoint region but rather forms a *transitional* subspace "
    "between the safe and unsafe clusters. This is consistent with the "
    "semantic interpretation: rethink traces capture intermediate "
    "reasoning that has not yet committed to either a fully safe or a "
    "fully unsafe trajectory, and motivates the rethink-anchoring term "
    "in the CRAFT prototype loss (Section 4) [@Luo2026CRAFT, Sec. 3].",
    title="Observation: rethink traces concentrate at the safe/unsafe boundary",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Figure 2",
        "caption": "Fig. 2: rethink cluster visibly between safe and unsafe clusters in both backbone PCAs.",
    },
)

claim_separation_model_agnostic = claim(
    "**The latent separation is model-agnostic across the two evaluated "
    "LRMs.** Because the same separation pattern appears in two "
    "*independently trained* large reasoning models with different "
    "architectures and training data -- DeepSeek-R1-Distill-Llama-8B "
    "[@Guo2025DeepSeekR1] (an R1-distilled Llama-3 [@Grattafiori2024Llama3] "
    "8B) and Qwen3-4B-Thinking [@Yang2025Qwen3] (a 4B Qwen3 reasoning "
    "checkpoint) -- the structural property of safe / unsafe latent "
    "separation is not a quirk of one training regime, but an "
    "*emergent* property of LRMs that produce explicit reasoning "
    "traces under jailbreak prompts [@Luo2026CRAFT, Sec. 3].",
    title="Observation: separation pattern is model-agnostic (R1-Distill-Llama-8B + Qwen3-4B-Thinking)",
)

# ---------------------------------------------------------------------------
# What the observation implies for the design
# ---------------------------------------------------------------------------

claim_separation_motivates_design = claim(
    "**The latent-separation observation motivates the CRAFT design "
    "choice of operating in latent space.** Because safe and unsafe "
    "reasoning traces are *already* geometrically separated in the "
    "pretrained LRM's final-token hidden state, alignment objectives "
    "defined over hidden states have a meaningful direction to push "
    "toward (the safe cluster mu_safe) and away from (the unsafe "
    "cluster mu_unsafe). The latent space is therefore *a priori* "
    "amenable to contrastive-and-RL-based shaping; the design problem "
    "reduces to (a) crystallizing this separation into explicit "
    "prototypes and (b) using them as reward / regularization signals "
    "in policy optimization [@Luo2026CRAFT, Sec. 3-4].",
    title="Argument: pre-existing latent separation makes hidden-state alignment well-posed",
)

__all__ = [
    "setup_reasoning_trace_notation",
    "setup_projection_head",
    "setup_semantic_labels",
    "setup_prototypes",
    "setup_probe_protocol",
    "claim_safe_unsafe_separation",
    "claim_rethink_at_boundary",
    "claim_separation_model_agnostic",
    "claim_separation_motivates_design",
]
