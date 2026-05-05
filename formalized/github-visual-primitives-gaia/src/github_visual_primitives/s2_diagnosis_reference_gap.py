"""Section 3.1 (Layer 3.1) -- the Reference-Gap-vs-Perception-Gap diagnosis.

Source: Visual Primitives release [@DeepSeekVisualPrimitives], Layer 3
"key distinctions" subsection, cross-validated by [@CSDNDeepRead] and
[@ThirtySixKr].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Definitions of the two gap concepts
# ---------------------------------------------------------------------------

setup_perception_gap_definition = setting(
    "**Definition: Perception Gap.** The *Perception Gap* is the "
    "hypothesised limitation that a multimodal LLM 'cannot see "
    "clearly enough' -- input resolution is too low and/or the visual-"
    "token budget is too small to preserve task-relevant visual "
    "detail. Closing this gap calls for *more* perception (higher "
    "input resolution, more patches, more visual tokens).",
    title="Definition: Perception Gap (cannot see clearly)",
)

setup_reference_gap_definition = setting(
    "**Definition: Reference Gap.** The *Reference Gap* is the "
    "hypothesised limitation that a multimodal LLM 'cannot point "
    "precisely enough' -- natural language, the channel through "
    "which CoT proceeds, is referentially imprecise in continuous "
    "visual space. Closing this gap calls for a *new referential "
    "modality* embedded in the reasoning trace, not for more pixels.",
    title="Definition: Reference Gap (cannot point precisely)",
)

# ---------------------------------------------------------------------------
# Headline diagnosis claim and its consequences
# ---------------------------------------------------------------------------

claim_reference_gap_is_actual_bottleneck = claim(
    "**Diagnosis (headline).** The actual bottleneck of multimodal "
    "reasoning in dense scenes is the *Reference Gap* (referential "
    "imprecision of natural language over continuous visual space), "
    "not the *Perception Gap* (input resolution / visual-token "
    "count). Pixel-level perception is already sufficient on modern "
    "frontier models; what fails is the model's ability to maintain "
    "an unambiguous spatial referent inside its CoT [@CSDNDeepRead].",
    title="Diagnosis: bottleneck is Reference Gap, not Perception Gap",
)

claim_industry_perception_path_hits_ceiling = claim(
    "**Consequence: the prevailing 'more pixels, more tokens' path "
    "hits a referential-ambiguity ceiling.** The frontier strategy of "
    "scaling input resolution and visual-token count [GPT-5.4 "
    "[@GPT54], Claude 4.6 [@Claude46], Gemini 3 Flash [@Gemini3Flash]] "
    "is bounded above by the referential ambiguity of natural language "
    "in CoT, not by perception fidelity. Beyond a threshold, adding "
    "tokens cannot resolve which object 'left big red' picks out -- "
    "the ceiling is a property of the language channel, not of "
    "perception.",
    title="Consequence: the 'more tokens' path is bounded by referential ambiguity, not perception",
)

claim_next_frontier_is_pointing_not_seeing = claim(
    "**Slogan: the next frontier is 'pointing precisely', not "
    "'seeing clearly'.** Closing the Reference Gap is a separate, "
    "complementary axis of progress, requiring (i) a referential "
    "modality embedded in the reasoning trace and (ii) training "
    "signal that rewards precise reference. This reframes what "
    "'better multimodal reasoning' means [@CSDNDeepRead].",
    title="Slogan: next frontier = pointing precisely, not seeing clearly",
)

# ---------------------------------------------------------------------------
# Foil claim used in Pass 2's contradiction operator
# ---------------------------------------------------------------------------

claim_perception_gap_is_actual_bottleneck = claim(
    "**Foil: the prevailing assumption that the Perception Gap is "
    "the bottleneck.** The implicit hypothesis in frontier multimodal "
    "scaling is that better multimodal reasoning is gated by "
    "perception fidelity (resolution, visual-token count) and that "
    "language-level reasoning will follow once perception is "
    "sufficient. This is the foil the Visual Primitives paper "
    "directly contradicts.",
    title="Foil: 'Perception Gap is the bottleneck' (the hypothesis Visual Primitives contradicts)",
)

__all__ = [
    "setup_perception_gap_definition",
    "setup_reference_gap_definition",
    "claim_reference_gap_is_actual_bottleneck",
    "claim_industry_perception_path_hits_ceiling",
    "claim_next_frontier_is_pointing_not_seeing",
    "claim_perception_gap_is_actual_bottleneck",
]
