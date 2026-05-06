"""Gaia formalization of Deng et al. (2025) [@Deng2025SIMURA],
'SIMURA: A World-Model-Driven Simulative Reasoning Architecture for
General Goal-Oriented Agents'.

The paper introduces SIMURA, a goal-oriented architecture that augments
black-box autoregressive reasoning with world-model-based planning via
simulation. Built on a principled formulation of the optimal goal-oriented
agent in a general environment, SIMURA's prototype implements all of its
modules (encoder, policy, world model, critic, actor) using LLMs with
natural language as a discrete, hierarchical state-and-action representation.
On complex web-browsing tasks (FlightQA, FanOutQA, WebArena), SIMURA's
full architecture lifts success rate on FlightQA from 0% (BrowsingAgent
baseline) to 32.2%; world-model planning improves over a matched
autoregressive-planning baseline by up to 124% in task-completion rate.
"""

from .motivation import *
from .s2_related_work import *
from .s3_optimal_agent_formulation import *
from .s4_simura_architecture import *
from .s5_world_model_implementation import *
from .s6_main_results import *
from .s7_per_task_results import *
from .s8_generality_and_ablations import *
from .s9_discussion_limitations import *
from .s10_wiring import *
