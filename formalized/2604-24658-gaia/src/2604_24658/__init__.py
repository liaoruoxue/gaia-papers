"""Gaia formalization of Liu et al. (2026) -- *The Last Human-Written
Paper: Agent-Native Research Artifacts* [@Liu2026ARA].

The paper diagnoses two structural costs of compiling research into
narrative (Storytelling Tax + Engineering Tax), proposes the
Agent-Native Research Artifact (ARA) protocol with four interlocking
layers (Cognitive / Physical / Exploration Graph / Evidence) bound by
forensic links, develops three enabling mechanisms (Live Research
Manager, ARA Compiler, ARA-Native Review System with three-level
Seal), and evaluates the format on PaperBench and RE-Bench across
three layers of research utility (understanding +21.3pp, reproduction
+7.0pp difficulty-weighted, extension early-acceleration on all 5
tasks).
"""

from .motivation import *
from .s2_ara_protocol import *
from .s3_live_research_manager import *
from .s4_compiler import *
from .s5_review_system import *
from .s6_network import *
from .s7_evaluation import *
from .s8_related_work import *
from .s9_limitations import *
from .s10_wiring import *
