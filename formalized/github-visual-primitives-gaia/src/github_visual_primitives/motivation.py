"""Motivation: multimodal LLMs that describe spatial relations in natural
language hit a referential-ambiguity ceiling in dense visual scenes.

Source: TL;DR + Layer 1 (three-sentence summary) of the Visual Primitives
release [@DeepSeekVisualPrimitives], cross-validated by [@CSDNDeepRead].
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup: multimodal-reasoning regime
# ---------------------------------------------------------------------------

setup_multimodal_reasoning_regime = setting(
    "**Multimodal-reasoning regime.** A *multimodal large language model* "
    "(multimodal LLM) jointly ingests an image and a text prompt and emits "
    "a chain-of-thought (CoT) reasoning trace followed by a final answer. "
    "The visual encoder turns the image into a sequence of patch tokens "
    "that are concatenated with the text-token sequence; the language "
    "backbone then decodes autoregressively over the joint sequence. "
    "Frontier instances of this regime include GPT-5.4 [@GPT54], "
    "Claude 4.6 [@Claude46], and Gemini 3 Flash [@Gemini3Flash].",
    title="Setup: multimodal-LLM reasoning over (image, prompt) -> CoT + answer",
)

setup_dense_scene_definition = setting(
    "**Definition of a dense visual scene.** A *dense scene* contains "
    "many similar objects whose distinguishing features are primarily "
    "*positional* (left/right, near/far, adjacent/distant) rather than "
    "categorical or chromatic. Examples: a cluttered desk with several "
    "pens, a maze with many cells, a path-tracing image with many "
    "Bezier curves crossing. In dense scenes a query of the form "
    "'the X object' is referentially ambiguous unless position is "
    "specified.",
    title="Setup: dense scene = many similar objects, distinguished by position",
)

setup_visual_primitive_tokens = setting(
    "**Visual-primitive tokens.** Two coordinate-bearing token classes "
    "exist in the model vocabulary: `<|box|>` (axis-aligned bounding "
    "box, four scalars) and `<|point|>` (single $(x, y)$ coordinate, "
    "two scalars). Both refer directly into the input image's "
    "continuous coordinate frame and can be emitted autoregressively "
    "as part of the model's output sequence, alongside ordinary text "
    "tokens.",
    title="Setup: visual-primitive token classes (`<|box|>`, `<|point|>`)",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "What is the actual bottleneck that limits multimodal-LLM "
    "reasoning in dense visual scenes -- and how should training and "
    "architecture be redesigned around that bottleneck?",
    title="Central question: where is the multimodal-reasoning bottleneck?",
)

# ---------------------------------------------------------------------------
# Diagnosis: state of the field and the running example
# ---------------------------------------------------------------------------

claim_referential_ambiguity_running_example = claim(
    "**Running example: 'the left big red object'.** When a multimodal "
    "LLM describes spatial relations purely in natural language, "
    "phrases such as 'the left big red object' are intrinsically "
    "ambiguous in dense scenes: 'left' is relative (left of what? from "
    "whose viewpoint?), 'big' is comparative (big relative to which "
    "neighbours?), and the entire phrase still does not pin down a "
    "single $(x, y)$ pixel-space referent. As CoT depth grows, the "
    "ambiguity compounds, producing attention drift and logical "
    "collapse [@CSDNDeepRead].",
    title="Running example: 'the left big red object' is referentially ambiguous in dense scenes",
)

claim_natural_language_imprecise_in_continuous_space = claim(
    "**Natural language is intrinsically imprecise for continuous "
    "visual reference.** Pixel space is continuous and high-resolution; "
    "natural language is discrete and constructed for categorical / "
    "relational reference, not for indexing continuous coordinates. "
    "Even an arbitrarily verbose description compresses a precise "
    "$(x, y)$ location through an information-lossy channel. This is a "
    "property of the language modality itself, not of model scale.",
    title="Premise: natural language is intrinsically imprecise for continuous visual reference",
)

claim_industry_chases_perception = claim(
    "**State of practice: frontier multimodal LLMs chase the Perception "
    "Gap.** GPT-5.4 [@GPT54], Claude 4.6 [@Claude46], and Gemini 3 "
    "Flash [@Gemini3Flash] all invest in higher input resolution and "
    "more visual tokens (the *Perception Gap* axis) to improve "
    "multimodal reasoning. The implicit assumption is that 'see "
    "clearly' implies 'reason correctly'.",
    title="State of practice: frontier models scale resolution + visual-token count",
)

# ---------------------------------------------------------------------------
# TL;DR-level headline contributions (atomic claims, each anchored later)
# ---------------------------------------------------------------------------

claim_tldr_diagnosis = claim(
    "**TL;DR (1) -- diagnosis.** The multimodal-reasoning bottleneck is "
    "the *Reference Gap* (natural language cannot index continuous "
    "visual space precisely), not the *Perception Gap* (resolution / "
    "token count) [@CSDNDeepRead].",
    title="TL;DR-1: bottleneck is Reference Gap, not Perception Gap",
)

claim_tldr_method = claim(
    "**TL;DR (2) -- method.** Lift `<|box|>` and `<|point|>` "
    "coordinate tokens to *thought-unit* status by embedding them "
    "directly inside the chain-of-thought (CoT), so the model "
    "**points while reasoning** rather than describing positions in "
    "prose [@CSDNDeepRead; @ThirtySixKr].",
    title="TL;DR-2: lift `<|box|>`/`<|point|>` to thought-unit status in CoT",
)

claim_tldr_architecture = claim(
    "**TL;DR (3) -- architecture.** A DeepSeek-ViT vision encoder "
    "feeds a DeepSeek-V4-Flash MoE language backbone (284B total / "
    "13B activated) [@DeepSeekV4Flash]; combined with 3x3 patch "
    "merging along the channel dimension and a 4x KV compression "
    "(Compressed Sparse Attention, CSA), the end-to-end visual "
    "compression on a 756x756 image is 7056x (2916 patches -> ~81 KV "
    "entries) [@CSDNDeepRead].",
    title="TL;DR-3: DeepSeek-ViT + V4-Flash MoE; 7056x end-to-end visual compression",
)

claim_tldr_training = claim(
    "**TL;DR (4) -- training.** A four-phase *Expert-Merge-Distill* "
    "pipeline trains separate Box and Point experts via per-expert "
    "GRPO [@GRPO] reinforcement learning under a 3-way Reward Model "
    "(Format / Quality / Task-Specific Accuracy), then rejection-fine-"
    "tunes (RFT) and on-policy distills the experts into a unified "
    "model. Pre-training data is filtered from 97,984 sources to "
    "31,701 via a two-stage quality review; cold-start data totals "
    "~604K samples (Counting ~10K, Spatial Reasoning/VQA ~9K, Maze "
    "Navigation 460K, Path Tracing 125K) [@CSDNDeepRead].",
    title="TL;DR-4: 4-phase Expert-Merge-Distill + 3-way Reward Model + filtered data pipeline",
)

claim_tldr_pipeline_alignment = claim(
    "**TL;DR (5) -- pipeline alignment with DeepSeek-OCR 2.** Visual "
    "Primitives and DeepSeek-OCR 2 [@DeepSeekOCR2] together form a "
    "complete vision-language pipeline: OCR 2 supplies the front-end "
    "*encoding-order* learning ('how to read the image'), while "
    "Visual Primitives supplies the back-end *pointing-during-"
    "reasoning* mechanism ('how to refer inside the image during "
    "CoT'). Both embody the meta-thesis **organization > volume**.",
    title="TL;DR-5: pipeline alignment with DeepSeek-OCR 2 (front-end encoding + back-end pointing)",
)

# ---------------------------------------------------------------------------
# Layer-1 three-sentence headlines (problem / solution / result)
# ---------------------------------------------------------------------------

claim_layer1_problem = claim(
    "**Layer-1 problem.** When multimodal LLMs describe spatial "
    "positions purely in natural language (e.g. 'the left big red "
    "object'), referential ambiguity in dense scenes leads to "
    "attention drift and logical collapse [@CSDNDeepRead].",
    title="Layer-1: problem = NL spatial description -> attention drift in dense scenes",
)

claim_layer1_solution = claim(
    "**Layer-1 solution.** Embed point coordinates and bounding boxes "
    "directly into the chain-of-thought as visual primitives, so the "
    "model emits spatial anchors *synchronously* with its reasoning "
    "rather than describing positions after the fact -- it **points** "
    "rather than **describes** [@CSDNDeepRead].",
    title="Layer-1: solution = visual primitives embedded in CoT (point, do not describe)",
)

claim_layer1_result = claim(
    "**Layer-1 headline result.** At an extremely low visual-token "
    "budget (~81 KV entries), the model achieves Maze Navigation "
    "66.9% (vs GPT-5.4 50.6%) and Path Tracing 56.7% (vs Claude 4.6 "
    "30.6%) [@CSDNDeepRead], demonstrating *information density > "
    "information volume*.",
    title="Layer-1: result = significant outperformance at 81-KV-entry budget on spatial-reasoning benchmarks",
)

__all__ = [
    "setup_multimodal_reasoning_regime",
    "setup_dense_scene_definition",
    "setup_visual_primitive_tokens",
    "q_central",
    "claim_referential_ambiguity_running_example",
    "claim_natural_language_imprecise_in_continuous_space",
    "claim_industry_chases_perception",
    "claim_tldr_diagnosis",
    "claim_tldr_method",
    "claim_tldr_architecture",
    "claim_tldr_training",
    "claim_tldr_pipeline_alignment",
    "claim_layer1_problem",
    "claim_layer1_solution",
    "claim_layer1_result",
]
