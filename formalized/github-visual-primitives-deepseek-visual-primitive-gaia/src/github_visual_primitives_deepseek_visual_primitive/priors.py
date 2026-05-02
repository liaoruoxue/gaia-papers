"""Prior assignments for the title-level leaf claims.

The source artifact for the GitHub repo
`deepseek-ai/Thinking-with-Visual-Primitives` in this package is a thin
stub (title + GitHub link + three keywords + status line). The two
title-level sentences (@thinking_with_visual_primitives_thesis and
@deepseek_visual_primitives_realises_thesis) are the only independent
leaf claims; the three keyword claims are derived from them via support
strategies, so no priors are assigned to derived claims (the inference
engine defaults to 0.5).

Both leaf claims are framing assertions extracted from the artifact's
title and the upstream repository name -- the kind of statement the
authors stake as the headline contribution of the work. The exact
figures are conservative: we have not seen the README, paper, or code,
so we cannot rule out that the precise scope of 'visual primitives'
(e.g. whether the set is fixed at {box, point, mask, mark, crop, sketch}
or strictly narrower / broader) or the precise framing of the
'reference gap' (e.g. whether it is operationalised through an
explicit grounding benchmark or only motivational) differs in detail
from the title-level reading.
"""

from .motivation import (
    deepseek_visual_primitives_realises_thesis,
    thinking_with_visual_primitives_thesis,
)

PRIORS = {
    thinking_with_visual_primitives_thesis: (
        0.9,
        "The central thesis is encoded directly in the upstream repository "
        "name ('Thinking-with-Visual-Primitives') -- the authors literally "
        "name the project after the methodological commitment. Held below "
        "0.95 because, having only the title and three keywords, we cannot "
        "inspect how strongly the README / paper argues for visual-only "
        "intermediate reasoning versus an interleaved language+visual "
        "trace, nor what exactly the primitive set is (boxes only, "
        "boxes+points+masks, or a broader set including marks / crops / "
        "sketches) -- a reading the body might qualify.",
    ),
    deepseek_visual_primitives_realises_thesis: (
        0.88,
        "Implied directly by the artifact title 'DeepSeek Visual "
        "Primitives' paired with the upstream repository name "
        "'Thinking-with-Visual-Primitives' under the standard "
        "'METHOD: thesis' / 'release: framework' convention -- the "
        "DeepSeek-branded release is the concrete instance of the "
        "thesis. Held slightly lower than the thesis itself because "
        "'DeepSeek Visual Primitives' could in principle refer to a "
        "narrower component (e.g. a primitive-detection toolbox) rather "
        "than to the full multimodal-reasoning system, and title-only "
        "evidence cannot discriminate among those readings.",
    ),
}
