"""Section 2.1 / Layer-2 architecture -- the encoder, compression layers,
language backbone, and the end-to-end 7056x compression on a 756x756 image.

Source: Layer-2 Section 2.1 of the Visual Primitives release
[@DeepSeekVisualPrimitives], cross-validated by [@CSDNDeepRead].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Architectural setup: encoder + compression operators + LM backbone
# ---------------------------------------------------------------------------

setup_deepseek_vit = setting(
    "**Vision encoder: DeepSeek-ViT (proprietary).** The vision "
    "encoder is DeepSeek-ViT, a Vision Transformer with $14 \\times "
    "14$ patches that supports any input resolution. Each patch is "
    "embedded into a token; a 756x756 input image therefore yields "
    "$(756 / 14)^2 = 54 \\times 54 = 2916$ patch tokens.",
    title="Setup: DeepSeek-ViT vision encoder (14x14 patches, any resolution)",
)

setup_3x3_patch_merge = setting(
    "**Spatial compression: 3x3 patch merge along channel.** A "
    "$3 \\times 3$ patch-merging operator concatenates each "
    "non-overlapping $3 \\times 3$ neighbourhood of patch tokens "
    "along the channel dimension, reducing the spatial token count "
    "by $9\\times$. After this operator a 54x54 grid becomes an "
    "18x18 grid, i.e. 324 tokens.",
    title="Setup: 3x3 patch merge along channel (9x spatial token reduction)",
)

setup_csa_4x = setting(
    "**KV compression: Compressed Sparse Attention (CSA), 4x.** CSA "
    "is a 4x KV-cache compression operator applied inside the "
    "language backbone's attention: each KV slot stores a "
    "compressed representation of four contiguous KV entries, "
    "reducing the KV footprint by $4\\times$ relative to dense "
    "attention.",
    title="Setup: CSA (Compressed Sparse Attention) 4x KV compression",
)

setup_v4_flash_backbone = setting(
    "**Language backbone: DeepSeek-V4-Flash MoE.** The language "
    "backbone is DeepSeek-V4-Flash, a Mixture-of-Experts model "
    "with **284B total parameters** of which **13B are activated** "
    "per token [@DeepSeekV4Flash]. The backbone autoregressively "
    "decodes the joint visual + text token stream, including "
    "primitive tokens.",
    title="Setup: DeepSeek-V4-Flash MoE (284B total / 13B activated)",
)

# ---------------------------------------------------------------------------
# Architecture summary table -- transcribed verbatim from the source
# ---------------------------------------------------------------------------

claim_architecture_table = claim(
    "**Architecture summary (Layer-2 Table 2.1, transcribed "
    "verbatim).**\n\n"
    "| Component | Detail |\n"
    "|-----------|--------|\n"
    "| Vision Encoder | DeepSeek-ViT (proprietary), 14x14 patches, any resolution |\n"
    "| Spatial compression | 3x3 patch -> 1 token (concatenate along channel) |\n"
    "| KV compression | CSA (Compressed Sparse Attention), 4x |\n"
    "| Language backbone | DeepSeek-V4-Flash, MoE 284B total / 13B activated |\n"
    "| End-to-end compression | 756x756: 2916 patches -> 324 tokens -> ~81 KV entries = 7056x |",
    title="Architecture table (transcribed verbatim)",
    metadata={
        "source_table": "artifacts/github-visual-primitives.md, Layer-2 Section 2.1 table",
    },
)

# ---------------------------------------------------------------------------
# Per-stage compression as atomic claims (each can be checked arithmetically)
# ---------------------------------------------------------------------------

claim_756_to_2916_patches = claim(
    "**Stage 1 -- patchification.** A 756x756 input image at 14x14 "
    "patch size yields $(756/14)^2 = 54^2 = 2916$ patch tokens out "
    "of DeepSeek-ViT.",
    title="Stage 1: 756x756 image -> 2916 patches",
)

claim_2916_to_324_tokens = claim(
    "**Stage 2 -- 3x3 patch merge.** The 3x3 channel-concatenation "
    "operator turns 2916 patch tokens into $2916 / 9 = 324$ tokens "
    "before they enter the language backbone.",
    title="Stage 2: 2916 patches -> 324 tokens (9x reduction)",
)

claim_324_to_81_kv = claim(
    "**Stage 3 -- CSA 4x.** CSA stores each block of 4 contiguous "
    "KV entries as a single compressed entry, turning 324 visual "
    "tokens into $\\sim 324 / 4 = 81$ KV entries inside the "
    "attention KV cache.",
    title="Stage 3: 324 tokens -> ~81 KV entries (4x reduction)",
)

claim_end_to_end_7056x = claim(
    "**End-to-end compression: 7056x on a 756x756 image.** Combining "
    "the three stages yields $9 \\times 4 \\times \\text{(pixel "
    "ratio)} = 7056\\times$ overall: 756x756 = 571,536 pixels per "
    "channel; the 3x3 patch merge gives a 9x token-count reduction; "
    "and the CSA gives a 4x KV-cache reduction; together with the "
    "14x14 patchification's pixel-to-patch ratio of $14^2 = 196$, "
    "the end-to-end reduction from raw pixels to KV entries is "
    "$196 \\times 9 \\times 4 = 7056\\times$ (equivalently, "
    "571,536 pixels reduce to ~81 KV entries).",
    title="End-to-end compression: 7056x (pixels -> KV entries) on 756x756",
)

# ---------------------------------------------------------------------------
# Integration: the architecture is purpose-built for high-density visual signal
# ---------------------------------------------------------------------------

claim_architecture_supports_high_density = claim(
    "**The architecture is purpose-built for high-density visual "
    "signal.** The 7056x end-to-end compression deliberately pushes "
    "the visual-token budget down to ~81 KV entries on a 756x756 "
    "image. This makes the visual modality cheap relative to the "
    "text CoT, freeing compute and context budget for the language "
    "backbone's primitive-emission reasoning. The design is "
    "therefore aligned with the *information density > information "
    "volume* philosophy.",
    title="Integration: 7056x compression makes visual signal cheap, supports density-over-volume",
)

__all__ = [
    "setup_deepseek_vit",
    "setup_3x3_patch_merge",
    "setup_csa_4x",
    "setup_v4_flash_backbone",
    "claim_architecture_table",
    "claim_756_to_2916_patches",
    "claim_2916_to_324_tokens",
    "claim_324_to_81_kv",
    "claim_end_to_end_7056x",
    "claim_architecture_supports_high_density",
]
