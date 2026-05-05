"""Section 3 / Layer-2 method -- lifting box and point coordinates to
first-class thought-units inside the chain-of-thought.

Source: TL;DR (2) + Layer-1 solution + Layer-3 framing of the Visual
Primitives release [@DeepSeekVisualPrimitives], cross-validated by
[@CSDNDeepRead].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setup: how visual primitives are emitted by the model
# ---------------------------------------------------------------------------

setup_cot_token_stream = setting(
    "**Setup: CoT as a single token stream.** During inference the "
    "language backbone autoregressively decodes a single token "
    "stream that contains both ordinary text tokens and visual-"
    "primitive tokens (`<|box|>`, `<|point|>`). Coordinates inside "
    "primitive tokens index directly into the input image's "
    "continuous coordinate frame. There is no separate 'spatial "
    "head' -- the same decoder produces words and coordinates.",
    title="Setup: CoT is a single token stream containing text + visual primitives",
)

# ---------------------------------------------------------------------------
# Method core: 'point while reasoning' rather than 'describe positions'
# ---------------------------------------------------------------------------

claim_method_lift_to_thought_unit = claim(
    "**Method core: lift `<|box|>` and `<|point|>` to thought-unit "
    "status.** The two coordinate-bearing token classes are not "
    "auxiliary outputs -- they are first-class units of thought, "
    "interleaved directly inside the CoT alongside text. The model "
    "can emit a `<|point|>(x, y)` mid-sentence to anchor an "
    "intermediate sub-reference before continuing the textual "
    "reasoning [@CSDNDeepRead].",
    title="Method: lift `<|box|>` / `<|point|>` to first-class thought-units in CoT",
)

claim_pointing_during_reasoning = claim(
    "**Behaviour: point while reasoning, do not describe.** The "
    "intended emergent behaviour is that the model emits a spatial "
    "anchor (point or box) **at the moment it would otherwise have "
    "named a position in prose**, and then reasons about that "
    "anchor. This converts referential anchors from a lossy textual "
    "compression ('the left big red object') into a precise "
    "coordinate ('<|point|>(312, 188)'). Reasoning depth no longer "
    "compounds positional ambiguity [@CSDNDeepRead].",
    title="Behaviour: emit spatial anchor synchronously with CoT (point, not describe)",
)

claim_visual_primitives_close_reference_gap = claim(
    "**Mechanism: visual primitives close the Reference Gap.** "
    "Because each `<|point|>(x, y)` and `<|box|>(x1, y1, x2, y2)` "
    "binds to a unique position in pixel space, the referential "
    "ambiguity of natural language is removed at the moment of "
    "reference. Subsequent CoT can refer back to the anchor symbol "
    "without re-introducing ambiguity, eliminating the attention "
    "drift and logical collapse documented in dense-scene "
    "reasoning [@CSDNDeepRead].",
    title="Mechanism: precise primitive coordinates eliminate referential ambiguity in CoT",
)

claim_information_density_over_volume = claim(
    "**Design philosophy: information density > information "
    "volume.** A handful of coordinate-bearing tokens carry more "
    "task-relevant referential information than thousands of natural-"
    "language tokens spent describing the same locations. The "
    "Visual Primitives architecture is therefore tuned for *high-"
    "density* visual signal (few tokens, each highly informative), "
    "in deliberate contrast to the frontier 'preserve as many "
    "tokens as possible' approach.",
    title="Philosophy: information density > information volume",
)

__all__ = [
    "setup_cot_token_stream",
    "claim_method_lift_to_thought_unit",
    "claim_pointing_during_reasoning",
    "claim_visual_primitives_close_reference_gap",
    "claim_information_density_over_volume",
]
