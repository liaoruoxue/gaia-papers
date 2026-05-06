"""Sections 5-6: Limitations and Conclusion.

Source: Deng et al. 2025 [@Deng2025SIMURA], Sections 5 (Limitations) and 6
(Conclusion).
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Limitations
# ---------------------------------------------------------------------------

claim_limit_runtime = claim(
    "**Limitation: SIMURA is slower than reactive agents.** Due to "
    "the modular pipeline (7 LLM calls per step) and the thorough "
    "exploration of multiple candidate plans inside the world-model "
    "simulator ($M = N = 20$ samples), SIMURA's wall-clock latency "
    "is higher than typical reactive agents. The paper flags "
    "**caching and parallelization of world-model rollouts** as an "
    "important part of future work.",
    title="Limitation: SIMURA is slower than reactive agents (modular pipeline + 20-sample rollouts)",
)

claim_limit_tooling = claim(
    "**Limitation: agent capabilities are bounded by tooling.** With "
    "open-source browser environments, SIMURA is *frequently blocked "
    "by Captcha or anti-scraping tools* on certain websites. The "
    "browser-crash failure mode also accounts for $24\\%$ of FanOutQA "
    "runs and $1.1\\%$ of FlightQA runs (Table 1, Table 2). Deeper "
    "integration with the user's own browser, plus community "
    "conversations on agent-access protocols and fair-use, are "
    "called out as paths forward.",
    title="Limitation: tooling constraints (Captcha, anti-scraping, browser crashes) bound agent capabilities",
)

claim_limit_modality = claim(
    "**Limitation: text-only observation misses visual layout cues.** "
    "The current SIMURA prototype uses only the text portion of the "
    "webpage observation (HTML accessibility tree), which can miss "
    "*images and layout information* (e.g., element occlusions). "
    "Multimodal perception combined with planning is acknowledged "
    "as challenging but a near-term direction.",
    title="Limitation: text-only observation misses images / layout cues; multimodal extension is future work",
)

# ---------------------------------------------------------------------------
# Conclusion synthesis (Section 6)
# ---------------------------------------------------------------------------

claim_conclusion_synthesis = claim(
    "**Conclusion synthesis.** The paper concludes that augmenting "
    "autoregressive reasoning with **simulation-based planning "
    "through a world model**, while representing internal belief "
    "states in the **semantically structured latent space of "
    "natural language**, yields consistent improvements across a "
    "range of web-interaction tasks. The empirical pattern -- "
    "0% -> 32.2% on FlightQA, +124% over matched autoregressive "
    "planning, consistent gains across FanOutQA and WebArena -- "
    "supports the broader claim that *explicit world-model "
    "reasoning enhances the planning and reasoning capacity of "
    "agents beyond what purely autoregressive reasoning provides*. "
    "The paper positions SIMURA as a *foundation for more capable, "
    "robust, and controllable agentic systems*, with future work "
    "spanning embodied environments, multi-agent interaction, "
    "long-term memory, and explicit world-model reasoning as a "
    "tool for transparency and alignment.",
    title="Conclusion: SIMURA validates simulative reasoning as a core component of general agentic intelligence",
)

claim_future_work_breadth = claim(
    "**Future-work breadth.** The paper enumerates near-term "
    "directions: training a single SIMURA agent across more "
    "environments (embodied sandboxes, physical space), additional "
    "functional components (multi-agent interaction, long-term "
    "memory), multimodal perception, caching/parallelization for "
    "speed, deeper user-browser integration, and safety/alignment "
    "research leveraging the explicit world-model representation "
    "for transparency.",
    title="Future work: cross-environment training, multimodality, multi-agent, long-term memory, caching, safety",
)

__all__ = [
    "claim_limit_runtime",
    "claim_limit_tooling",
    "claim_limit_modality",
    "claim_conclusion_synthesis",
    "claim_future_work_breadth",
]
