"""Gaia formalization of Yang et al. (2026) [@Yang2026RecursiveMAS],
'Recursive Multi-Agent Systems'.

The paper introduces RecursiveMAS, a system-level recursive framework that
casts an entire LLM-based multi-agent system (MAS) as a unified latent-space
recursive computation by chaining heterogeneous agents through the
RecursiveLink module and training the whole system via an inner-outer
loop algorithm.

Project Page: [@RecursiveMASPage].
"""

from .motivation import *
from .s2_preliminary import *
from .s3_recursive_link import *
from .s4_inner_outer_loop import *
from .s5_main_results import *
from .s6_efficiency import *
from .s7_in_depth import *
from .s8_related_work import *
from .s9_conclusion import *
from .s10_wiring import *
