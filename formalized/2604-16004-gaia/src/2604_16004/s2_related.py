"""Section 2: Related Work on reward models and test-time scaling."""

from gaia.lang import claim, setting, support

from .motivation import (
    paradigm_shift_claim,
    genrm_single_turn_claim,
)


rm_alignment_setting = setting(
    "Reward Models (RMs) play a pivotal role in aligning large language models with human "
    "preferences. Outcome-level RMs assign scalar rewards to complete responses; PRMs "
    "supervise intermediate steps; GenRMs reformulate reward modeling as next-token "
    "prediction."
)

prior_tool_augmented_rm_claim = claim(
    "Existing tool-augmented and LLM-as-Judge reward models either fail to tightly integrate "
    "tool execution into the reasoning process or do not provide point-wise feedback "
    "required for test-time scaling."
)

bidirectional_novelty_claim = claim(
    "Reformulating verification as a bidirectional, multi-turn, tool-augmented process is "
    "novel relative to prior reward-model and TTS literature."
)

novelty_support = support(
    [prior_tool_augmented_rm_claim, genrm_single_turn_claim, paradigm_shift_claim],
    bidirectional_novelty_claim,
    reason="Prior work either lacks tight tool integration or lacks point-wise feedback; "
           "no prior reward model casts verification as bidirectional + multi-turn + tool-augmented.",
    prior=0.8,
    background=[rm_alignment_setting],
)
