"""Section 3.4 (Layer-3) -- pipeline alignment with DeepSeek-OCR 2 and the
shared meta-thesis 'organization > volume'.

Source: Layer-3 Section 3.4 of the Visual Primitives release
[@DeepSeekVisualPrimitives], cross-validated by [@CSDNDeepRead].
DeepSeek-OCR 2 reference: [@DeepSeekOCR2].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: who DeepSeek-OCR 2 is and where it sits in the pipeline
# ---------------------------------------------------------------------------

setup_ocr2_role = setting(
    "**DeepSeek-OCR 2 [@DeepSeekOCR2].** A separate DeepSeek "
    "release (arXiv:2601.20552) that addresses the *front-end* "
    "of vision-language modelling: how to *read* an image. OCR 2 "
    "rejects raster-scan tokenization and learns a *causal "
    "encoding order* -- which patches to read in which order, "
    "as a learned function of image content -- and matches "
    "Gemini-1.5 Pro at 256-1120 visual tokens.",
    title="Setup: DeepSeek-OCR 2 = front-end causal encoding-order learner",
)

# ---------------------------------------------------------------------------
# Atomic alignment claims (one per row of the alignment table)
# ---------------------------------------------------------------------------

claim_alignment_problem_axis = claim(
    "**Alignment row 1 -- problem axis.** OCR 2 addresses 'raster-"
    "scan imposes a non-semantic reading order'; Visual "
    "Primitives addresses 'natural language cannot precisely "
    "refer'. Both target *organizational* failures of the "
    "vision-language interface rather than perceptual ones.",
    title="Alignment-1: both target organizational (not perceptual) failures",
)

claim_alignment_solution_axis = claim(
    "**Alignment row 2 -- solution axis.** OCR 2's solution is "
    "*Causal Flow* -- learn what order to read patches in; "
    "Visual Primitives' solution is to embed coordinates inside "
    "the CoT -- *pointing while reasoning*. Both replace a "
    "fixed, lossy interface with a learned, content-adaptive one.",
    title="Alignment-2: both replace fixed lossy interfaces with learned content-adaptive ones",
)

claim_alignment_compression_axis = claim(
    "**Alignment row 3 -- compression-belief axis.** OCR 2 "
    "matches Gemini-1.5 Pro at 256-1120 visual tokens; Visual "
    "Primitives surpasses GPT-5.4 / Claude 4.6 at ~81 KV "
    "entries. Both demonstrate that aggressive visual-token "
    "compression *plus* learned organization beats the frontier "
    "approach of preserving more tokens.",
    title="Alignment-3: both achieve frontier-or-better at large compression ratios",
)

claim_alignment_means_axis = claim(
    "**Alignment row 4 -- mechanical means axis.** OCR 2 uses "
    "two stacked 1D causal flows over patches to construct 2D "
    "understanding; Visual Primitives uses 3x3 patch merging "
    "plus 4x CSA KV compression to drive 7056x end-to-end "
    "reduction. The mechanisms differ but both deliver the "
    "*same* property -- few but well-organized visual tokens.",
    title="Alignment-4: different mechanisms (1D causal flows vs 3x3+CSA), same property (few well-organized tokens)",
)

claim_alignment_table = claim(
    "**OCR 2 / Visual Primitives alignment table (Layer-3 "
    "Section 3.4, transcribed verbatim).**\n\n"
    "| Axis | DeepSeek-OCR 2 | Visual Primitives |\n"
    "|------|----------------|-------------------|\n"
    "| Problem | raster-scan imposes non-semantic order | natural language cannot precisely refer |\n"
    "| Solution | Causal Flow -- learn 'what order to read in' | embed coordinates in CoT -- 'point while reasoning' |\n"
    "| Compression belief | 256-1120 tokens match Gemini-1.5 Pro | ~81 KV surpasses GPT-5.4 / Claude 4.6 |\n"
    "| Means | two stacked 1D causal flows -> 2D understanding | 3x3 patch merge + 4x CSA |",
    title="Alignment table: OCR 2 (front-end) vs Visual Primitives (back-end)",
    metadata={
        "source_table": "artifacts/github-visual-primitives.md, Layer-3 Section 3.4",
    },
)

# ---------------------------------------------------------------------------
# The meta-thesis: organization > volume
# ---------------------------------------------------------------------------

claim_meta_thesis_organization_over_volume = claim(
    "**Meta-thesis (shared with OCR 2): organization > volume.** "
    "Both works embody a shared belief that *how* visual "
    "information is organized matters more than *how much* of it "
    "is preserved. They stand in deliberate opposition to the "
    "frontier-multimodal practice of 'preserve as many visual "
    "tokens as possible'. The two demonstrations are independent "
    "evidence for the same meta-thesis at different layers of "
    "the vision-language stack.",
    title="Meta-thesis: organization > volume (shared with OCR 2)",
)

claim_complete_pipeline = claim(
    "**Complete vision-language pipeline.** OCR 2 supplies the "
    "front-end ('read the image in semantic order'), V4-Flash "
    "MoE supplies the comprehension stage, and Visual Primitives "
    "supplies the back-end ('point during reasoning'). The "
    "three components compose into a complete pipeline that is "
    "compressed at every stage and that uses learned, content-"
    "adaptive interfaces in place of fixed lossy ones.\n\n"
    "```\n"
    "OCR 2 (front-end encoding) -> V4-Flash (comprehension) -> "
    "Visual Primitives (back-end reasoning)\n"
    "'read in semantic order'    -> 'understand'           -> "
    "'point during CoT'\n"
    "encoding order              -> comprehension          -> "
    "pointing during reasoning\n"
    "```",
    title="Complete pipeline: OCR 2 (front-end) + V4-Flash + Visual Primitives (back-end)",
)

claim_opposition_to_industry = claim(
    "**Joint opposition to industry's 'preserve more tokens' "
    "default.** The frontier multimodal-LLM design philosophy "
    "treats preserving as many visual tokens as possible as a "
    "strict capability lever. The OCR 2 + Visual Primitives line "
    "directly contests this: in both works, large compression "
    "ratios (256-1120 tokens, ~81 KV entries) **plus** learned "
    "organization match or beat models with much higher visual-"
    "token budgets. The two works are mutually reinforcing "
    "evidence for the contrarian position.",
    title="Synthesis: OCR 2 + Visual Primitives jointly oppose 'preserve more tokens'",
)

__all__ = [
    "setup_ocr2_role",
    "claim_alignment_problem_axis",
    "claim_alignment_solution_axis",
    "claim_alignment_compression_axis",
    "claim_alignment_means_axis",
    "claim_alignment_table",
    "claim_meta_thesis_organization_over_volume",
    "claim_complete_pipeline",
    "claim_opposition_to_industry",
]
