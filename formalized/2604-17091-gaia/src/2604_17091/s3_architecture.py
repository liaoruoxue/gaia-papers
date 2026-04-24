"""Section 3: Compositional Capabilities and System Architecture"""

from gaia.lang import claim, setting, support, deduction

from .motivation import thesis_minimal_architecture
from .s2_design import (
    def_atomic_tool,
    def_agent_loop,
    claim_self_evolution,
    claim_tool_minimality,
    claim_hierarchical_memory,
)

# ── Settings ──────────────────────────────────────────────────────────────────

def_cli_interface = setting(
    "GA exposes a single unified command-line interface (CLI). All agent interactions — "
    "task submission, progress monitoring, runtime intervention — are handled through "
    "this CLI. The agent is a standalone CLI program, not a service requiring a daemon.",
    title="GA's CLI-only interface",
)

def_subagent_dispatch = setting(
    "Subagent dispatch in GA: a parent agent spawns child GA instances by executing "
    "a standard terminal command (the GA CLI). Each instance runs in its own memory "
    "space with its own conversation history. Communication is via the standard "
    "interaction protocol. No dedicated subagent manager is required.",
    title="Subagent dispatch definition",
)

def_reflect_mode = setting(
    "Reflect Mode: GA continuously monitors for environmental changes via a user-supplied "
    "callback polled at a fixed interval. When the callback returns a non-empty string, "
    "that string is injected as a new prompt. The default trigger fires every six minutes "
    "with a fixed prompt directing autonomous exploration. Reflect Mode requires no "
    "user instruction.",
    title="Reflect Mode polling mechanism",
)

def_skill_tree = setting(
    "GA organizes accumulated skills into a persistent skill tree: a two-level map "
    "where categories (e.g., web_automation, data_processing) contain named skills, "
    "each recording associated tool scripts and a monotonically increasing usage counter. "
    "The skill tree acts as a global capability index and drives autonomous exploration.",
    title="Skill tree data structure",
)

# ── Architecture claims ───────────────────────────────────────────────────────

claim_cli_minimality = claim(
    "GA's extreme architectural minimality — approximately 3,000 lines of core code "
    "with a single CLI interface — is not a functional compromise but a deliberate "
    "design choice. Because the architecture is stripped down and purely CLI-based, "
    "advanced behaviors such as subagent dispatch and Reflect Mode emerge naturally "
    "from the single primitive without requiring new architectural layers.",
    title="CLI minimality enables emergent compositional capabilities",
)

claim_subagent_emergence = claim(
    "Subagent dispatch in GA emerges naturally from the CLI architecture: any agent can "
    "spawn a child GA process via a standard terminal command. This provides "
    "context isolation by design (each process has its own memory space) and enables "
    "map-reduce parallelism without a dedicated subagent manager subsystem.",
    title="Subagent dispatch as emergent property of CLI design",
)

claim_reflect_emergence = claim(
    "Reflect Mode emerges naturally from the CLI architecture: an idle-condition callback "
    "fires every 6 minutes to trigger autonomous exploration. No new architectural "
    "subsystem is required — the dispatcher becomes the agent itself.",
    title="Reflect Mode as emergent property of CLI design",
)

claim_autonomous_exploration = claim(
    "Autonomous exploration in GA combines subagent dispatch (execution substrate) and "
    "Reflect Mode (trigger substrate) to enable the agent to explore new skills during "
    "idle time without user instruction. Skills are organized in a persistent skill tree. "
    "Exploration task generation decides what to explore based on current capability gaps "
    "in the skill tree.",
    title="Autonomous exploration via combined subagent dispatch and Reflect Mode",
)

claim_architectural_self_update = claim(
    "In GA's minimal codebase (~3,000 lines), subagents can read and modify the core "
    "codebase itself, making architectural self-update a practically achievable next step. "
    "Agent evolution has three progressive dimensions: (1) skill consolidation via SOPs, "
    "(2) autonomous exploration via Reflect Mode, (3) architectural self-update. "
    "Minimal architecture is the necessary prerequisite for reaching dimension (3).",
    title="Three dimensions of agent evolution enabled by minimal architecture",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_cli_minimality = support(
    [claim_tool_minimality],
    claim_cli_minimality,
    reason=(
        "@claim_tool_minimality establishes that GA uses only 9 atomic tools. "
        "The CLI-only interface (@def_cli_interface) means all interactions go through "
        "a single command-line entrypoint. Together, the 9 atomic tools plus a unified "
        "CLI define an architecture with ~3,000 lines of core code. Because the "
        "interface is standard, subagent dispatch follows without new code: a subagent "
        "is just another CLI invocation [@GenericAgent2026]."
    ),
    prior=0.88,
    background=[def_cli_interface, def_atomic_tool],
)

strat_subagent = support(
    [claim_cli_minimality],
    claim_subagent_emergence,
    reason=(
        "@claim_cli_minimality establishes GA as a standalone CLI program. "
        "From @def_cli_interface and @def_subagent_dispatch, spawning a subagent is "
        "just running the GA CLI command in a subprocess. Context isolation follows "
        "from process-level memory separation. No dedicated manager is needed — "
        "the mechanism is already in the OS [@GenericAgent2026]."
    ),
    prior=0.92,
    background=[def_cli_interface, def_subagent_dispatch],
)

strat_reflect = support(
    [claim_cli_minimality],
    claim_reflect_emergence,
    reason=(
        "@claim_cli_minimality establishes GA as a standard CLI program. "
        "Reflect Mode (@def_reflect_mode) is a polling callback attached to the "
        "existing CLI agent loop — when idle, the callback fires and injects a prompt. "
        "No separate subsystem is needed; the loop already handles arbitrary prompts "
        "[@GenericAgent2026]."
    ),
    prior=0.90,
    background=[def_cli_interface, def_reflect_mode],
)

strat_autonomous_exploration = support(
    [claim_subagent_emergence, claim_reflect_emergence],
    claim_autonomous_exploration,
    reason=(
        "@claim_subagent_emergence provides the execution substrate for parallel "
        "exploration tasks. @claim_reflect_emergence provides the idle-time trigger "
        "mechanism. Together with the skill tree (@def_skill_tree) that indexes current "
        "capabilities and identifies gaps, these mechanisms enable the agent to identify "
        "capability gaps, trigger exploration during idle time, and crystallize "
        "results into new skill tree entries [@GenericAgent2026]."
    ),
    prior=0.82,
    background=[def_skill_tree],
)

strat_arch_self_update = support(
    [thesis_minimal_architecture, claim_cli_minimality],
    claim_architectural_self_update,
    reason=(
        "@thesis_minimal_architecture argues that a sufficiently small codebase "
        "can be read and modified by the agent itself. @claim_cli_minimality "
        "establishes that GA's core is ~3,000 lines. At this scale, a subagent "
        "can parse, understand, and propose modifications to the core code — "
        "making architectural self-update a tractable next step for dimension (3) "
        "of agent evolution [@GenericAgent2026]."
    ),
    prior=0.62,
)
