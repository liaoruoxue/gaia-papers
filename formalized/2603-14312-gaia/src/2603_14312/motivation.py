"""Introduction: Motivation for Autonomous Distributed Scientific Discovery"""

from gaia.lang import claim, setting, question

# --- Background settings ---

sci_ai_status_quo = setting(
    "Current AI systems in science remain fundamentally interactive: they respond to human "
    "prompts rather than initiating or sustaining independent investigation cycles. Existing "
    "autonomous frameworks either assist human investigators or automate single pipelines, "
    "but do not support a persistent multi-agent ecosystem.",
    title="Status quo of AI in science",
)

distributed_discovery_analogy = setting(
    "Scientific discovery resembles distributed or crowd-sourced reasoning: independent "
    "investigators, each following their own interests, collectively converge on robust "
    "explanations through artifact exchange and peer critique rather than central direction.",
    title="Distributed discovery model",
)

# --- Core questions ---

q_autonomous_coordination = question(
    "Can independent AI agents conduct scientific investigation without central coordination, "
    "emergently converging on robust findings through shared artifact exchange?",
    title="Core research question",
)

q_traceability = question(
    "How can the reasoning chain from raw computation to published scientific finding be made "
    "fully auditable and traceable in a multi-agent system?",
    title="Traceability question",
)

# --- Claims from Introduction ---

ai_science_gap = claim(
    "There is a fundamental gap between current AI-assisted science (human-prompt-driven) and "
    "genuinely autonomous scientific investigation: no existing system supports a persistent "
    "open ecosystem where multiple independent agents can concurrently investigate, exchange "
    "artifacts, and coordinate without a human directing each step [@Wang2025].",
    title="Gap in autonomous scientific AI",
)

framework_overview = claim(
    "The ScienceClaw + Infinite framework addresses this gap through three integrated components: "
    "(1) an extensible registry of over 300 interoperable scientific skills, "
    "(2) an artifact layer that preserves full computational lineage as a directed acyclic graph (DAG), "
    "and (3) a structured platform (Infinite) for agent-based scientific discourse with "
    "provenance-aware governance [@Wang2025].",
    title="ScienceClaw + Infinite framework overview",
)

emergent_coordination_claim = claim(
    "Plannerless coordination — where agents discover and fulfill each other's open information "
    "needs through a shared global index rather than through explicit task assignment — is "
    "sufficient to produce emergent convergence among independently operating agents across "
    "multiple scientific domains [@Wang2025].",
    title="Plannerless coordination sufficiency claim",
)

provenance_traceability_claim = claim(
    "Every number in a published post in the Infinite platform can be traced back through the "
    "chain of intermediate computations to its originating raw data, because each artifact "
    "carries immutable parent lineage as a directed acyclic graph (DAG) [@Wang2025].",
    title="Full computational provenance claim",
)
