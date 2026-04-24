"""Section 2: The CORAL Framework — Architecture and Design Principles"""

from gaia.lang import (
    claim, setting, question,
    support, deduction, contradiction,
)

from .motivation import (
    open_ended_discovery_setting,
    llm_agent_setting,
    shared_memory_setting,
    heartbeat_setting,
    evolutionary_search_setting,
)

# =============================================================================
# Framework design claims
# =============================================================================

claim_persistent_memory_design = claim(
    "CORAL's shared persistent memory serves as the primary coordination mechanism between "
    "agents, replacing explicit inter-agent communication protocols. Agents write to and "
    "read from three directories—`attempts/` (evaluation history with code, score, and "
    "parent lineage), `notes/` (observations and reflections), and `skills/` (reusable "
    "procedures)—and knowledge diffuses organically without explicit synchronization. "
    "Implementation uses a filesystem with symbolic links so each agent's workspace "
    "points to the shared memory store.",
    title="Persistent memory as coordination mechanism",
    metadata={"source": "artifacts/2604-01658.pdf, Section 2.1"},
)

claim_async_execution = claim(
    "CORAL agents execute asynchronously in isolated workspaces, each maintaining its own "
    "sandboxed environment while sharing access to the common evaluator and memory store "
    "via symbolic links. Asynchronous execution means agents do not need to synchronize "
    "or wait for each other between iterations, enabling organic coordination: faster "
    "agents contribute more frequently to shared memory, slower agents benefit from "
    "accumulated knowledge when they read from memory before each attempt.",
    title="Asynchronous multi-agent execution",
    metadata={"source": "artifacts/2604-01658.pdf, Section 2.2"},
)

claim_heartbeat_mechanism = claim(
    "CORAL's three-tier heartbeat intervention system guides agent behavior without "
    "prescribing specific search strategies. Per-iteration reflection prompts (after "
    "every evaluation) encourage note-taking and observation recording. Periodic "
    "consolidation prompts (every 10 evaluations) synthesize accumulated knowledge into "
    "structured summaries. Stagnation-triggered redirection prompts (after 5 consecutive "
    "non-improving evaluations) push agents toward strategic pivots and exploration of "
    "fundamentally different approaches.",
    title="Heartbeat intervention mechanism",
    metadata={"source": "artifacts/2604-01658.pdf, Section 2.3"},
)

claim_evaluator_design = claim(
    "CORAL uses a pluggable evaluator hierarchy: a task-specific grader (user-defined) "
    "wrapped by a common evaluation harness that provides resource management, timeout "
    "handling, and result standardization. The evaluator is separated from agent workspaces "
    "to prevent cheating or gaming the evaluation signal. Configuration uses YAML task "
    "definitions specifying the grader, budget constraints, and evaluator parameters.",
    title="Pluggable evaluator design",
    metadata={"source": "artifacts/2604-01658.pdf, Section 2.4"},
)

claim_safety_mechanisms = claim(
    "CORAL implements four safety mechanisms for deployment: (1) workspace isolation "
    "prevents agents from accessing each other's private files or the evaluation code, "
    "(2) evaluator separation ensures agents cannot read or modify the grader, "
    "(3) resource controls limit CPU/memory/time per evaluation, and "
    "(4) agent health monitoring (via heartbeat checks) detects and restarts failed agents. "
    "A 17-command CLI interface manages all agent lifecycle operations.",
    title="CORAL safety and infrastructure mechanisms",
    metadata={"source": "artifacts/2604-01658.pdf, Section 2.5"},
)

# =============================================================================
# Design philosophy claims (distinguishing CORAL from baselines)
# =============================================================================

claim_no_fixed_algorithm = claim(
    "Unlike fixed evolutionary search methods (FunSearch, EvoPrompting, OpenEvolve), "
    "CORAL does not impose a predetermined evolutionary algorithm. There is no explicit "
    "population management, selection operator, or crossover mechanism specified by the "
    "framework designer. Instead, agents autonomously decide which prior attempts to build "
    "on, how to combine ideas, and when to explore versus exploit, using the shared memory "
    "store as the implicit population.",
    title="CORAL uses no fixed evolutionary algorithm",
    metadata={"source": "artifacts/2604-01658.pdf, Section 2"},
)

alt_fixed_algorithm_sufficient = claim(
    "Fixed evolutionary algorithms with LLM mutation operators (FunSearch, EvoPrompting, "
    "OpenEvolve) are sufficient for open-ended discovery tasks and autonomous adaptation "
    "provides no additional benefit over well-designed fixed heuristics.",
    title="Alternative: fixed evolutionary algorithms are sufficient",
    metadata={"source": "artifacts/2604-01658.pdf, Section 1 (baseline comparison)"},
)

# Contradiction: CORAL outperforming (claim_coral_outperforms_fixed in motivation) and
# fixed algorithms being sufficient cannot both be true
not_both_sufficient = contradiction(
    claim_no_fixed_algorithm,
    alt_fixed_algorithm_sufficient,
    reason=(
        "If CORAL's autonomous strategy adaptation provides 3-10x higher improvement rates "
        "than fixed baselines, then fixed algorithms are not sufficient. Both cannot hold: "
        "CORAL's design philosophy (no fixed algorithm) and the claim that fixed algorithms "
        "suffice are mutually exclusive."
    ),
    prior=0.95,
)

# =============================================================================
# Strategies connecting framework claims
# =============================================================================

strat_memory_enables_async = support(
    [claim_persistent_memory_design, claim_async_execution],
    claim_heartbeat_mechanism,
    reason=(
        "The heartbeat mechanism (@claim_heartbeat_mechanism) is feasible precisely because "
        "of the persistent memory structure (@claim_persistent_memory_design): each heartbeat "
        "prompt can reference the agent's notes and memory state to contextualize the "
        "reflection or consolidation request. Asynchronous execution (@claim_async_execution) "
        "means heartbeats fire independently per agent without coordination overhead."
    ),
    prior=0.88,
)

strat_framework_enables_safety = support(
    [claim_evaluator_design, claim_async_execution],
    claim_safety_mechanisms,
    reason=(
        "The safety mechanisms (@claim_safety_mechanisms) are enabled by the evaluator "
        "separation design (@claim_evaluator_design): isolated workspaces with symbolic "
        "links to shared memory provide the filesystem-level isolation needed for workspace "
        "sandboxing. Asynchronous execution (@claim_async_execution) in separate processes "
        "enables resource controls per agent without global locks."
    ),
    prior=0.90,
)

strat_no_fixed_alg_from_design = deduction(
    [claim_persistent_memory_design, claim_heartbeat_mechanism],
    claim_no_fixed_algorithm,
    reason=(
        "The architectural choice of shared persistent memory (@claim_persistent_memory_design) "
        "as the implicit population, combined with open-ended heartbeat prompts "
        "(@claim_heartbeat_mechanism) that do not specify which candidates to select or how "
        "to mutate them, logically entails that no fixed evolutionary algorithm is imposed. "
        "The framework design itself constitutes the absence of a fixed algorithm."
    ),
    prior=0.95,
)
