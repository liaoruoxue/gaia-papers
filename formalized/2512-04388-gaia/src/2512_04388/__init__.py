"""Gaia formalization of Nielsen et al. (2026) [@Nielsen2026Conductor],
'Learning to Orchestrate Agents in Natural Language with The Conductor'
(ICLR 2026).

The paper introduces the **Conductor**: a 7B language-model meta-orchestrator
trained end-to-end with reinforcement learning (GRPO) to dynamically design
agentic workflows for a pool of frontier LLM workers. The Conductor
simultaneously prompt-engineers natural-language subtasks, selects which
workers receive which subtask, and specifies an access list (communication
topology) for each step. Two finetuning extensions add (a) randomized
agent-pool generalization and (b) self-referential recursive topologies as a
new test-time scaling axis. The 7B Conductor attains state-of-the-art on
LiveCodeBench V6, GPQA-Diamond, AIME25, MATH500, MMLU, RLPR, and
BigCodeBench.
"""

from .motivation import *
from .s2_rl_reasoning import *
from .s3_setup import *
from .s4_method import *
from .s5_extensions import *
from .s6_main_results import *
from .s7_controlled_eval import *
from .s8_user_recursion import *
from .s9_analysis_ablations import *
from .s10_related_work import *
from .s11_discussion import *
from .s12_wiring import *
