"""Section 5: Related Work -- RL with tools, multi-agent coordination,
positioning of the Conductor within these two literatures.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 5, p. 9.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Related work area 1: RL with tools
# ---------------------------------------------------------------------------

claim_rl_with_tools_literature = claim(
    "**RL-with-tools literature.** RL [@Guo2025DeepSeekR1; @Lambert2024Tulu3; "
    "@Chu2025SFTvsRL] has become increasingly popular for eliciting "
    "reasoning capabilities in LLMs. Recent works extend RL beyond pure "
    "text reasoning through **tool use**: code execution feedback "
    "[@Gehring2024RLEF; @Le2022CodeRL], dynamic real-time code "
    "execution [@Feng2025ReTool], step-grained tool-usage reward "
    "shaping [@Yu2024StepTool], and text-based web browsing "
    "[@Nakano2021WebGPT]. These works incorporate execution feedback "
    "into end-to-end RL to enhance geometric reasoning, equation "
    "solving, code synthesis, search-augmented QA, and precise "
    "computation.",
    title="Related literature: RL-with-tools (RLEF, ReTool, StepTool, CodeRL, WebGPT) -- single-model RL + external tools",
)

claim_conductor_rl_tool_positioning = claim(
    "**Conductor positioning within RL-with-tools.** The Conductor "
    "framework establishes a **new extension to the tool-using RL "
    "paradigm**, where powerful collaborative reasoning topologies "
    "emerge from RL by equipping the base model with **workflow "
    "delegation through API calling** -- where the 'tool' is a "
    "frontier-LLM worker invoked via a natural-language subtask. This "
    "qualitatively differs from prior RL-with-tools (single base model "
    "+ single deterministic tool) by adding an orchestration layer over "
    "*multiple* heterogeneous LLM workers.",
    title="Positioning: Conductor extends RL-with-tools to LLM-worker API calling as the 'tool'",
)

# ---------------------------------------------------------------------------
# Related work area 2: Multi-agent coordination
# ---------------------------------------------------------------------------

claim_multi_agent_coord_literature = claim(
    "**Multi-agent coordination literature.** With increasingly powerful "
    "individual LLMs, recent works design topological and prompt-based "
    "scaffolds to coordinate groups of agents "
    "[@Du2023MultiAgentDebate; @Wang2024MoA; @Dang2025EvolvingOrchestration; "
    "@Madaan2023SelfRefine; @Yue2025MASRouter]. The literature can be "
    "characterized along several axes:\n\n"
    "- **Hand-designed scaffolds** orchestrating agents within and across "
    "rounds: MoA [@Wang2024MoA], multi-agent debate "
    "[@Du2023MultiAgentDebate].\n"
    "- **Embedding-based routing** -- learn embedding spaces mapping "
    "queries to agents/topologies: Smoothie [@Guha2024Smoothie], "
    "MASRouter [@Yue2025MASRouter].\n"
    "- **Graph-learnable collaboration**: GPTSwarm [@Zhuge2024GPTSwarm].\n"
    "- **Single-best-agent routers**: RouterDC [@Chen2024RouterDC] learn "
    "a router that directs queries to the *single* best-matched agent.",
    title="Related literature: multi-agent coordination (debate, MoA, MASRouter, RouterDC, GPTSwarm, Self-Refine)",
)

claim_conductor_mas_positioning = claim(
    "**Conductor positioning within multi-agent coordination.** The "
    "Conductor framework differs from all existing multi-agent "
    "coordination approaches by **learning powerful agent coordination "
    "strategies through pure end-to-end RL**, allowing complete freedom "
    "to learn **any strategy expressible in natural language** -- not "
    "limited to a pre-specified set of topologies, scaffolds, or "
    "embedding-routed selections. The natural-language medium plus the "
    "end-to-end RL signal jointly distinguish the Conductor from all "
    "prior work.",
    title="Positioning: Conductor is the only fully end-to-end-RL MAS coordinator with unrestricted natural-language output",
)

claim_positioning_summary = claim(
    "**Joint positioning summary.** The Conductor sits at the "
    "**intersection of RL-with-tools and multi-agent coordination**: it "
    "uses RL on verifiable end-task rewards (RL-with-tools paradigm) "
    "and orchestrates multiple worker LLMs (MAS paradigm), with the "
    "novel twist that the 'tool API' is natural-language workflow "
    "delegation. This intersection is the paper's framework-level "
    "contribution.",
    title="Positioning summary: Conductor at the RL-with-tools x MAS-coordination intersection",
)

__all__ = [
    "claim_rl_with_tools_literature",
    "claim_conductor_rl_tool_positioning",
    "claim_multi_agent_coord_literature",
    "claim_conductor_mas_positioning",
    "claim_positioning_summary",
]
