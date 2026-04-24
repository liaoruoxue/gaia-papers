"""Introduction and Motivation: Autonomous Multi-Agent Evolution for Open-Ended Discovery"""

from gaia.lang import (
    claim, setting, question,
    support, deduction,
)

# =============================================================================
# Background / Settings
# =============================================================================

open_ended_discovery_setting = setting(
    "Open-ended discovery refers to the class of problems—spanning mathematics, engineering, "
    "and science—where the objective function is known (or can be specified) but the optimal "
    "strategy for achieving it is unknown, and the solution space is too large for exhaustive "
    "search. Classical examples include combinatorial optimization, algorithm design, and "
    "physical system optimization. Evolutionary search methods have historically been applied "
    "to such problems but require hand-designed mutation operators and search heuristics.",
    title="Open-ended discovery problem class",
)

llm_agent_setting = setting(
    "Large language model (LLM) based agents are autonomous systems that use a frontier "
    "language model as the reasoning core, augmented with tool access (code execution, file "
    "I/O, web search, etc.) and memory mechanisms. In this paper, agents operate via a "
    "17-command CLI interface. Each agent maintains its own isolated workspace (a sandbox "
    "directory) but shares access to a common persistent memory store and evaluator.",
    title="LLM agent definition and capabilities",
)

evolutionary_search_setting = setting(
    "Fixed evolutionary search methods—including FunSearch [@FunSearch2023], EvoPrompting "
    "[@EvoPrompting2023], OpenEvolve [@OpenEvolve2025], and ShinkaEvolve [@ShinkaEvolve2025]—"
    "apply LLMs as mutation operators within a human-designed evolutionary loop. These methods "
    "follow predetermined algorithms: selection, mutation, and evaluation steps are fixed at "
    "design time and do not adapt based on problem structure or accumulated experience.",
    title="Fixed evolutionary search baseline definition",
)

shared_memory_setting = setting(
    "CORAL's shared persistent memory is a filesystem structure shared across all collaborating "
    "agents via symbolic links. It organizes three artifact types:\n\n"
    "| Directory | Contents |\n"
    "|-----------|----------|\n"
    "| `attempts/` | Historical evaluations: code, score, parent lineage |\n"
    "| `notes/` | Agent observations, reflections, and learnings |\n"
    "| `skills/` | Reusable procedures and implementation patterns |\n\n"
    "Memory is persistent across agent restarts and accessible to all agents simultaneously.",
    title="Shared persistent memory structure",
)

heartbeat_setting = setting(
    "CORAL uses three types of heartbeat interventions to guide agent behavior:\n\n"
    "1. **Per-iteration reflection**: After each evaluation, agents are prompted to record "
    "observations, insights, and next steps in the shared notes directory.\n"
    "2. **Periodic consolidation**: Every 10 evaluations, agents synthesize accumulated "
    "knowledge into structured summaries.\n"
    "3. **Stagnation-triggered redirection**: After 5 consecutive non-improving evaluations, "
    "agents receive a prompt to pivot strategy and explore fundamentally different approaches.",
    title="Heartbeat intervention types",
)

evaluation_budget_setting = setting(
    "Experimental budget: CORAL runs for a 3-hour wall-clock limit or 100 evaluation "
    "iterations (whichever is longer for baselines). Results reported as mean over 4 "
    "independent trials. All experiments use Claude Opus 4.6 as the backbone model unless "
    "otherwise specified. Open-source validation uses MiniMax-M2.5 and OpenCode models.",
    title="Experimental evaluation budget and configuration",
)

# =============================================================================
# Research questions
# =============================================================================

q_autonomous_evolution = question(
    "Can LLM-based agents autonomously conduct evolutionary search on open-ended discovery "
    "problems without relying on predetermined algorithms or hand-designed heuristics?",
    title="Main research question: autonomous evolution",
)

q_multi_agent_benefit = question(
    "Does multi-agent co-evolution provide benefits beyond simply running multiple "
    "independent single-agent searches with the same total compute budget?",
    title="Multi-agent coordination question",
)

q_knowledge_causality = question(
    "Does knowledge accumulation (persistent memory) causally improve CORAL's performance, "
    "or is the correlation between knowledge access and improvement spurious?",
    title="Knowledge causality question",
)

# =============================================================================
# Core contribution claims (from introduction and abstract)
# =============================================================================

claim_coral_outperforms_fixed = claim(
    "CORAL, a framework for autonomous LLM-based multi-agent evolution, achieves "
    "state-of-the-art performance on 10 out of 11 diverse benchmark tasks (6 mathematical "
    "optimization, 5 systems optimization), establishing new best-known results on 8 tasks. "
    "CORAL's improvement rate is 3–10× higher than fixed evolutionary search baselines "
    "(FunSearch, EvoPrompting, OpenEvolve, ShinkaEvolve), and it typically converges within "
    "5–20 evaluations versus 60–100 evaluations for baselines [@CORAL2026].",
    title="CORAL outperforms fixed evolutionary search",
    metadata={"source": "artifacts/2604-01658.pdf, Abstract + Section 1"},
)

claim_multi_agent_gains = claim(
    "Four co-evolving CORAL agents achieve better results than a single CORAL agent on "
    "the hardest benchmark tasks, and these gains cannot be explained by additional compute "
    "alone. On the Kernel Engineering stress-test task, four collaborating agents reduced "
    "the cycle count from 1,363 (single-agent best) to 1,103—an 18.3% improvement "
    "[@CORAL2026].",
    title="Multi-agent co-evolution provides gains beyond compute",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.2"},
)

claim_knowledge_causal = claim(
    "Knowledge accumulation via shared persistent memory is causally responsible for a "
    "substantial portion of CORAL's performance gains. Disabling the knowledge accumulation "
    "component degrades Kernel Engineering performance from 1,350 to 1,601 cycles—an 18.6% "
    "regression—confirming the causal role of accumulated knowledge rather than a spurious "
    "correlation with agent capability [@CORAL2026].",
    title="Knowledge accumulation causally improves performance",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.3"},
)

claim_agents_adaptable = claim(
    "CORAL agents autonomously discover and apply effective search strategies without "
    "human-designed heuristics, adapting their approach based on accumulated experience. "
    "Agents vary their local verification behavior (from 11% to 61% local test rates "
    "across tasks), knowledge access patterns (7% to 30% of attempts), and strategy "
    "diversity (Jaccard similarity 0.31–0.43 across agents), demonstrating emergent "
    "adaptive behavior [@CORAL2026].",
    title="Agents autonomously adapt search strategies",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.4"},
)

# =============================================================================
# Strategy connecting contributions
# =============================================================================

strat_coral_sota = support(
    [claim_coral_outperforms_fixed, claim_knowledge_causal, claim_agents_adaptable],
    claim_multi_agent_gains,
    reason=(
        "The multi-agent gains (@claim_multi_agent_gains) build directly on the foundation "
        "established by single-agent CORAL performance (@claim_coral_outperforms_fixed) and "
        "causal knowledge accumulation (@claim_knowledge_causal). The emergent adaptive "
        "strategy variation (@claim_agents_adaptable) provides the mechanism by which agents "
        "divide the search space rather than duplicating effort, enabling coordination gains "
        "that exceed independent parallel search."
    ),
    prior=0.85,
)

__all__ = [
    "claim_coral_outperforms_fixed",
    "claim_multi_agent_gains",
    "claim_knowledge_causal",
    "claim_agents_adaptable",
]
