"""Gaia formalization of Luo et al. (2026), 'Contrastive Reasoning Alignment:
Reinforcement Learning from Hidden Representations' [@Luo2026CRAFT].

Reference implementation: [@CRAFTCode] (anonymous; to be open-sourced after acceptance).

Content note: the source paper contains examples of harmful language in
illustrative figures of jailbreak prompts; this formalization reasons *about*
the paper's findings (claims, evaluations, theorem) without reproducing those
examples.
"""

from .motivation import *
from .s2_related_work import *
from .s3_setup import *
from .s4_method import *
from .s5_theory import *
from .s6_main_results import *
from .s7_avg_improvements import *
from .s8_ablations import *
from .s9_discussion_limitations import *
from .s10_wiring import *
