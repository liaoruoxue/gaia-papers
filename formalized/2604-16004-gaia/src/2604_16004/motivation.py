"""Introduction and Motivation: Limitations of existing reward models for test-time scaling."""

from gaia.lang import claim, setting, support


tts_setting = setting(
    "Test-Time Scaling (TTS) for LLM reasoning includes parallel methods (e.g., Best-of-N) "
    "and sequential refinement, both of which depend on a reward model (verifier) to "
    "discern solution quality and guide search."
)

reasoning_milestones_setting = setting(
    "Recent milestones on the International Mathematical Olympiad by OpenAI and Google "
    "highlight the rapid ascent of reasoning models such as Gemini-3 and DeepSeekMath-V2."
)

verifier_role_claim = claim(
    "The efficacy of Test-Time Scaling for LLM reasoning is fundamentally dependent on the "
    "reward model (verifier) used to score and select candidate solutions.",
    background=[tts_setting],
)

orm_prm_limitation_claim = claim(
    "Outcome-level RMs (ORMs) and process-level RMs (PRMs) only emit scalar values and "
    "therefore lack interpretability when used as verifiers."
)

genrm_single_turn_claim = claim(
    "Generative Reward Models (GenRMs) trained with next-token prediction typically employ "
    "single-turn reasoning to assess candidate solutions."
)

error_propagation_claim = claim(
    "Single-turn GenRMs suffer from error propagation: because LLMs are mostly trained on "
    "correct or near-correct solutions, they struggle to issue a correct verdict when "
    "conditioned on a flawed solution and are easily misled by superficially plausible "
    "but incorrect answers."
)

external_grounding_gap_claim = claim(
    "Single-turn GenRMs lack external grounding: without integration with symbolic solvers "
    "or external tools, they hallucinate on computation-intensive or knowledge-heavy tasks "
    "and exhibit unstable performance."
)

genrm_unreliable_claim = claim(
    "Existing GenRMs are unreliable in complex domains because they suffer from error "
    "propagation and lack external grounding."
)

genrm_unreliable_support = support(
    [error_propagation_claim, external_grounding_gap_claim, genrm_single_turn_claim],
    genrm_unreliable_claim,
    reason="Error propagation plus the absence of external grounding within a single-turn "
           "reasoning pipeline jointly undermine GenRM reliability.",
    prior=0.9,
)

paradigm_shift_claim = claim(
    "Reliable verification calls for an agentic reward modeling paradigm that uses "
    "multi-turn reasoning integrated with external tools."
)

paradigm_shift_support = support(
    [genrm_unreliable_claim, verifier_role_claim],
    paradigm_shift_claim,
    reason="If verifiers are critical to TTS but current GenRMs are unreliable, the natural "
           "remedy is multi-turn, tool-augmented agentic verification.",
    prior=0.85,
)

# NOTE: Single-turn GenRMs and the call for an agentic paradigm are in tension but not
# logically exclusive (single-turn methods *exist* even if they are inferior). We document
# this tension in ANALYSIS.md rather than adding a spurious contradiction edge.
