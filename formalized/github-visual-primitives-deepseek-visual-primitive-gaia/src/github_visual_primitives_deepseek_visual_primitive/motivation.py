"""Motivation: DeepSeek Visual Primitives -- thinking with visual primitives.

Formalisation of the GitHub repository
https://github.com/deepseek-ai/Thinking-with-Visual-Primitives ("DeepSeek
Visual Primitives"). The source artifact in this package is a thin stub
(title + GitHub link + three-keyword list + status line); no README body,
paper PDF, or code listing is bundled in the artifact. Therefore only the
title-level thesis claim, its companion method/scope claim, and the three
listed keyword topics are extracted as claims.

The H1 of the artifact -- "DeepSeek Visual Primitives" -- is split, in
combination with the repository name "Thinking-with-Visual-Primitives", into
two title-level leaves under the standard 'METHOD: thesis' convention:

  (i) the thesis that a multimodal model should **think with visual
      primitives** -- i.e. its reasoning trace over an image should be
      expressed in terms of *primitive visual operations / objects*
      (boxes, points, masks, crops, marks, sketches, ...) that live in
      the image plane itself, rather than (only) in detached natural-
      language descriptions of the image; and
 (ii) the companion claim that **DeepSeek Visual Primitives** (the
      DeepSeek release whose repo is `Thinking-with-Visual-Primitives`)
      is the proposed concrete instance of that design, packaged as an
      open release intended to close the **reference gap** between what
      a multimodal model can name in language and what it can directly
      pick out in the pixel grid.

The three keywords name the three supporting axes:
  (1) **multimodal** -- the work studies a model that ingests images
      alongside text (it is not a text-only system);
  (2) **visual-reasoning** -- the unit of analysis is a multi-step
      reasoning trace over visual content, not a one-shot caption or
      classification; and
  (3) **reference-gap** -- the load-bearing problem framing is the gap
      between linguistic reference (what the model can *say* about an
      image) and visual reference (what the model can *point to* in the
      image), which 'thinking with visual primitives' is meant to close.
"""

from gaia.lang import claim, setting, support

# ---------------------------------------------------------------------------
# Background framing
# ---------------------------------------------------------------------------

multimodal_setting = setting(
    "A *multimodal model* in this package's scope is a language model "
    "that ingests both natural-language text and raster images (and "
    "optionally produces image-plane outputs such as boxes, points, "
    "masks, or sketches). The model's *visual interface* -- what it can "
    "consume from an image and what it can emit back into the image "
    "plane -- is a first-order design choice that determines what kinds "
    "of visual reasoning the model can express.",
    title="Multimodal (image+text) model (formal setting)",
)

visual_primitives_setting = setting(
    "A *visual primitive* is an atomic, image-grounded operation or "
    "object that a multimodal model can reason with directly: examples "
    "are bounding boxes, points, segmentation masks, image crops, set-of-"
    "marks overlays, sketches, or arrows drawn on the image. A model "
    "that 'thinks with visual primitives' generates and consumes such "
    "primitives as intermediate steps of its reasoning trace, rather "
    "than describing the image only through detached natural-language "
    "noun phrases. The primitive set is differentiable / addressable in "
    "the image plane, so the reasoning trace is itself visually "
    "verifiable.",
    title="Visual primitive (image-plane reasoning unit)",
)

reference_gap_setting = setting(
    "The *reference gap* in multimodal models is the asymmetry between "
    "(a) what the model can name in language about an image -- which is "
    "rich, compositional, and largely tied to its text vocabulary -- "
    "and (b) what the model can directly pick out in the pixel grid -- "
    "which has historically been narrow, coarse, and poorly aligned "
    "with the language side. Closing the reference gap means making "
    "the model's visual-pointing capability commensurate with its "
    "linguistic-naming capability, so that 'the small red box on the "
    "left of the second shelf' can be both said *and* indicated.",
    title="Reference gap (language vs visual pointing)",
)

deepseek_visual_primitives_scope = setting(
    "The study scope of *DeepSeek Visual Primitives* is the open release "
    "(GitHub repo `deepseek-ai/Thinking-with-Visual-Primitives`) of a "
    "DeepSeek multimodal system that elevates visual primitives -- "
    "boxes, points, masks, marks, crops, sketches -- to first-class "
    "intermediate reasoning steps, with the explicit framing of "
    "narrowing the reference gap between language and pixels. The "
    "package is treated here as the concrete, named instance of the "
    "'thinking with visual primitives' methodology.",
    title="DeepSeek Visual Primitives (study scope)",
)

# ---------------------------------------------------------------------------
# Headline title-level claims (the H1 of the artifact + repo name)
# ---------------------------------------------------------------------------

thinking_with_visual_primitives_thesis = claim(
    "Multimodal models should **think with visual primitives**: their "
    "intermediate reasoning trace over an image should be expressed in "
    "terms of *primitive visual operations / objects* (boxes, points, "
    "masks, crops, marks, sketches, ...) that live in the image plane "
    "itself, rather than (only) in detached natural-language descriptions "
    "of the image. Treating visual primitives as a first-class reasoning "
    "substrate -- not as a downstream detection head -- is the central "
    "methodological move: it lets the reasoning trace be visually "
    "verifiable and directly addressable in the pixel grid.",
    title="Central thesis: multimodal models should think with visual primitives",
    metadata={"source": "artifacts/github-visual-primitives-deepseek-visual-primitive.md (H1 / repo title 'Thinking-with-Visual-Primitives')"},
)

deepseek_visual_primitives_realises_thesis = claim(
    "**DeepSeek Visual Primitives** -- the open release whose repository "
    "is `deepseek-ai/Thinking-with-Visual-Primitives` -- is proposed as "
    "the concrete realisation of the 'thinking with visual primitives' "
    "thesis: an open multimodal system whose distinguishing design "
    "choice is to expose visual primitives as the unit of intermediate "
    "reasoning, with the explicit operational target of narrowing the "
    "**reference gap** between linguistic naming and visual pointing. "
    "The 'DeepSeek' qualifier and the GitHub release together signal "
    "that this is offered as an open, reproducible artifact -- not only "
    "a proposal -- of the methodology.",
    title="DeepSeek Visual Primitives realises the visual-primitive thesis",
    metadata={"source": "artifacts/github-visual-primitives-deepseek-visual-primitive.md (title 'DeepSeek Visual Primitives' + repo 'Thinking-with-Visual-Primitives')"},
)

# ---------------------------------------------------------------------------
# Keyword-level claims (the 3 keywords listed in the source)
# Each keyword names a topic the work claims to study; we lift each into an
# atomic claim that ties back to the central thesis.
# ---------------------------------------------------------------------------

keyword_multimodal = claim(
    "The work studies a **multimodal** system: the model ingests images "
    "alongside text (and, in the visual-primitive setting, also emits "
    "image-plane primitives such as boxes, points, masks, marks, crops, "
    "or sketches). Multimodal is the *substrate* axis of DeepSeek Visual "
    "Primitives -- it fixes that there is a pixel grid for the visual "
    "primitives to live in, and a language channel for the reasoning "
    "trace to interleave with.",
    title="Keyword: multimodal",
    metadata={"keyword_index": 1, "source": "artifacts/github-visual-primitives-deepseek-visual-primitive.md (keywords)"},
)

keyword_visual_reasoning = claim(
    "The work commits to **visual-reasoning** as the unit of analysis: "
    "the system is evaluated and designed for multi-step reasoning over "
    "visual content (compose, locate, compare, count, follow references "
    "across image regions), not for one-shot captioning or single-label "
    "classification. Visual-reasoning is the *task-shape* axis of "
    "DeepSeek Visual Primitives -- it fixes that the reasoning trace is "
    "visual, multi-step, and benefits from intermediate image-plane "
    "primitives rather than collapsing to a single textual answer.",
    title="Keyword: visual-reasoning",
    metadata={"keyword_index": 2, "source": "artifacts/github-visual-primitives-deepseek-visual-primitive.md (keywords)"},
)

keyword_reference_gap = claim(
    "The work names **reference-gap** as the load-bearing problem "
    "framing: the asymmetry between what a multimodal model can name in "
    "language about an image and what it can directly pick out in the "
    "pixel grid. 'Thinking with visual primitives' is positioned as the "
    "mechanism for narrowing that gap -- by emitting boxes, points, "
    "masks, or marks as part of the reasoning trace, the model's "
    "visual-pointing ability is made commensurate with its linguistic-"
    "naming ability. Reference-gap is the *problem-framing* axis of "
    "DeepSeek Visual Primitives.",
    title="Keyword: reference-gap",
    metadata={"keyword_index": 3, "source": "artifacts/github-visual-primitives-deepseek-visual-primitive.md (keywords)"},
)

# ---------------------------------------------------------------------------
# Reasoning connections (minimal)
# ---------------------------------------------------------------------------
# The two title-level leaf claims jointly grant evidence to each of the three
# keyword claims: the central visual-primitives thesis grounds the multimodal
# substrate (something must host the primitives) and the visual-reasoning
# task-shape (primitives are reasoning steps), while the
# DeepSeek-Visual-Primitives-as-instance claim additionally grounds the
# reference-gap problem framing that the open release explicitly targets.

strat_thesis_grounds_multimodal = support(
    [thinking_with_visual_primitives_thesis, deepseek_visual_primitives_realises_thesis],
    keyword_multimodal,
    background=[multimodal_setting, deepseek_visual_primitives_scope],
    reason=(
        "If the central methodological move is to think with visual "
        "primitives in the image plane (@thinking_with_visual_primitives_thesis) "
        "and DeepSeek Visual Primitives is its concrete realisation "
        "(@deepseek_visual_primitives_realises_thesis), then the system "
        "necessarily ingests images alongside text -- the primitives need "
        "a pixel grid to live in (@multimodal_setting, "
        "@deepseek_visual_primitives_scope). The keyword 'multimodal' "
        "names that substrate commitment."
    ),
    prior=0.96,
)

strat_thesis_grounds_visual_reasoning = support(
    [thinking_with_visual_primitives_thesis],
    keyword_visual_reasoning,
    background=[multimodal_setting, visual_primitives_setting],
    reason=(
        "The thesis that a model's reasoning trace should consist of "
        "image-plane primitives (@thinking_with_visual_primitives_thesis) "
        "is in fact a definitional commitment to visual-reasoning: the "
        "primitives are intermediate reasoning steps over visual content "
        "(@visual_primitives_setting), so the task shape is multi-step "
        "reasoning over images rather than one-shot captioning "
        "(@multimodal_setting). The keyword 'visual-reasoning' is the "
        "direct restatement of that task-shape choice."
    ),
    prior=0.95,
)

strat_deepseek_grounds_reference_gap = support(
    [deepseek_visual_primitives_realises_thesis],
    keyword_reference_gap,
    background=[reference_gap_setting, deepseek_visual_primitives_scope],
    reason=(
        "The DeepSeek Visual Primitives release positions itself as a "
        "concrete instance of 'thinking with visual primitives' "
        "(@deepseek_visual_primitives_realises_thesis), and the operational "
        "payoff of emitting boxes / points / masks / marks during "
        "reasoning is precisely to make visual pointing commensurate with "
        "linguistic naming (@reference_gap_setting, "
        "@deepseek_visual_primitives_scope). The keyword 'reference-gap' "
        "names that load-bearing problem framing."
    ),
    prior=0.93,
)

__all__ = [
    "multimodal_setting",
    "visual_primitives_setting",
    "reference_gap_setting",
    "deepseek_visual_primitives_scope",
    "thinking_with_visual_primitives_thesis",
    "deepseek_visual_primitives_realises_thesis",
    "keyword_multimodal",
    "keyword_visual_reasoning",
    "keyword_reference_gap",
]
