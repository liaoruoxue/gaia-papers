"""Section 2: Related Work -- LLM-based agents, world-model-based agents,
web-browsing agents, and generalist agents.

Source: Deng et al. 2025 [@Deng2025SIMURA], Section 2.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 2.1 LLM-Based Agents
# ---------------------------------------------------------------------------

claim_llm_agents_two_lines = claim(
    "**Two main lines of LLM-based agent research.** Two complementary "
    "approaches dominate LLM-based agent construction: "
    "(L1) *Data-collection-then-training* in the targeted environment "
    "-- AutoWebGLM [@AutoWebGLM], AgentQ [@AgentQ], UI-TARS [@UITARS] "
    "-- which depends on environment-specific demonstrations; "
    "(L2) *Prompt-based workflows* with carefully designed modules "
    "-- AWM [@AWM], Voyager [@Voyager] -- which decouple agent design "
    "from per-environment training. SIMURA is built on prompt-based "
    "workflows but, in principle, can leverage observation data to "
    "train its world model [@Chae2024WMA], reducing reliance on "
    "human demonstration and yielding strong generalizability "
    "[@LeCunOpenReview2022].",
    title="Related work: LLM-based agents -- data-collection-then-training vs prompt-based workflows",
)

# ---------------------------------------------------------------------------
# 2.2 World-Model-Based Agents
# ---------------------------------------------------------------------------

claim_world_model_history = claim(
    "**World-model-based planning has a long history but limited "
    "breadth.** Early work demonstrated model-based planning on classic "
    "games -- Atari [@Oh2015AtariVid], Go/Chess/Shogi [@MuZero]. Later "
    "work used world models for policy optimization on control tasks "
    "[@MBPO; @TDMPC]. Recent foundation-model work has applied world-"
    "model-based planning to math reasoning [@RAP], Minecraft "
    "[@Dreamer], and web browsing [@WebDreamer]. SIMURA builds on "
    "this trajectory.",
    title="Related work: world-model-based agents -- games, control, math, Minecraft, web",
)

claim_existing_wm_continuous_embedding_limit = claim(
    "**Existing world models use *continuous holistic embeddings* that "
    "suffer from noise and high variability.** Existing world-model-"
    "based agents typically represent and predict world states using "
    "*continuous holistic embeddings* (single high-dimensional vectors "
    "covering an entire frame/state), which suffer from sensory noise "
    "and high variability that detract from robust and stable decision-"
    "making [@Barrett2017]. SIMURA argues for a *discrete, concept-"
    "based* natural-language latent space instead, which is "
    "empirically observed to give more general applicability across "
    "tasks.",
    title="Related work: continuous holistic-embedding world models are noise-sensitive; SIMURA's natural-language alternative",
)

# ---------------------------------------------------------------------------
# 2.3 Web-Browsing Agents
# ---------------------------------------------------------------------------

claim_existing_web_agents_react_limited = claim(
    "**Existing web-browsing agents are typically built on ReAct-style "
    "autoregressive reasoning and are domain-specialized.** Recent "
    "web-browsing agents -- proprietary (Operator [@Operator], "
    "Anthropic Computer Use [@AnthropicComputerUse], Project Mariner "
    "[@ProjectMariner]) and open-source (OpenHands BrowsingAgent "
    "[@OpenHands], WebVoyager [@WebVoyager], CogAgent [@CogAgent], "
    "WebAgent [@WebAgentGur]) -- are typically built on simple "
    "ReAct-based [@ReAct] autoregressive reasoning. As such they "
    "have difficulty recovering from previous mistakes, and their "
    "specialized design precludes generalization to other domains "
    "(social interactions, the physical world).",
    title="Related work: existing web agents are ReAct-based, autoregressive, domain-specialized",
)

claim_existing_benchmarks_limit = claim(
    "**Existing web-agent benchmarks are simulated, outdated, or weakly "
    "evaluated.** Numerous benchmarks evaluate web agents -- WebArena "
    "[@WebArena], WebVoyager [@WebVoyager], MiniWoB++ [@MiniWoB], "
    "Mind2Web [@Mind2Web], WebShop [@WebShop]. Despite wide adoption, "
    "they are usually either built in *simulated/simplified "
    "environments*, based on *outdated questions*, or *lack convincing "
    "task-completion measurement*. To address these limits, the paper "
    "introduces FlightQA, which evaluates real-time complex website "
    "navigation under controlled constraint complexity (Section 4.1).",
    title="Related work: existing web benchmarks have simulation / staleness / evaluation gaps; FlightQA addresses them",
)

# ---------------------------------------------------------------------------
# 2.4 Generalist Agents
# ---------------------------------------------------------------------------

claim_generalist_two_lines = claim(
    "**Two prevailing lines of generalist-agent research.** "
    "(G1) *Multi-agent workflows* delegating tasks/subtasks to "
    "specialist agents [@OWL; @AgentOrchestra; @MagenticOne]; "
    "extensible but improvements often require new specialist agents. "
    "(G2) *Composable executable scripts* over predefined tools "
    "[@CodeAct; @OpenHands; @smolagents; @Alita]; flexible but "
    "tool-bound. SIMURA aims for a *holistic single architecture* "
    "that leverages shared experience across domains/modalities via "
    "world-model learning and supports high-level natural-language "
    "planning, look-ahead, plan updates, and on-the-fly mistake "
    "correction.",
    title="Related work: generalist-agent lines -- multi-agent workflows vs composable scripts; SIMURA's holistic alternative",
)

__all__ = [
    "claim_llm_agents_two_lines",
    "claim_world_model_history",
    "claim_existing_wm_continuous_embedding_limit",
    "claim_existing_web_agents_react_limited",
    "claim_existing_benchmarks_limit",
    "claim_generalist_two_lines",
]
