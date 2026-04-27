"""ABBEL: LLM Agents Acting through Belief Bottlenecks Expressed in Language.

Lidayan, Bjorner, Golechha, Goyal, Suhr (2025). Introduces the ABBEL framework
where an LLM agent maintains a natural-language belief state and selects
actions conditioned only on the belief (not the full interaction history),
plus belief-grading and belief-length-penalty rewards for RL fine-tuning under
the framework. Empirical study on six prompting environments (frontier models)
and three RL settings (Combination Lock, multi-objective QA, ColBench).
"""

from .motivation import *
from .s2_framework import *
from .s4_eval_frontier import *
from .s5_rl_training import *

__all__ = [
    # Framework
    "abbel_proposal",
    "abbel_two_call_loop",
    "context_compression_property",
    # Empirical findings (introduction-level laws)
    "finding_belief_grows_slower",
    "finding_failure_modes",
    "finding_rl_helps",
    # Section 4 prompting findings
    "obs_gemini_abbel_competitive",
    "obs_deepseek_abbel_worse",
    "obs_belief_lengths_short",
    "prompting_only_inadequate",
    # Section 5 methods
    "method_belief_length_penalty",
    "method_belief_grading",
    # Section 5 results
    "obs_cl_bg_outperforms",
    "obs_qa_abbel_outperforms_mem1",
    "obs_qa_abbel_lp_memory",
    "obs_cb_abbel_memory_efficient",
    "obs_cb_bg_data_efficient",
    # Discussion synthesis
    "abbel_useful_testbed",
]
