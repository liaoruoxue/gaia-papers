"""Gaia formalization of *DeepSeek Visual Primitives -- Thinking with Visual
Primitives* [@DeepSeekVisualPrimitives].

The work was released by DeepSeek-AI together with Peking University and
Tsinghua University on 2026-04-30 as a GitHub repository, then withdrawn.
This formalization is reconstructed from secondary sources -- a CSDN deep
read [@CSDNDeepRead], Phoenix Technology coverage [@PhoenixTech] and
36Kr coverage [@ThirtySixKr] -- which cross-validate the architecture,
data pipeline, training recipe, and benchmark results.

Headline thesis: the multimodal-reasoning bottleneck is the *Reference
Gap* (natural language is intrinsically imprecise for spatial reference
in continuous visual space), not the *Perception Gap* (resolution / token
count). The paper lifts box / point coordinate tokens to first-class
"thought-unit" status so the model points while reasoning. Companion
work DeepSeek-OCR 2 [@DeepSeekOCR2] addresses the front-end encoding
order; together they articulate the meta-thesis "organization > volume".
"""

from .motivation import *
from .s2_diagnosis_reference_gap import *
from .s3_method_visual_primitives import *
from .s4_architecture import *
from .s5_data_pipeline import *
from .s6_training_pipeline import *
from .s7_reward_model import *
from .s8_results import *
from .s9_limitations import *
from .s10_ocr2_pipeline import *
from .s11_wiring import *
