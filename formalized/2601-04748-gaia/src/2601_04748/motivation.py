"""
Introduction: Multi-Agent Systems vs Single-Agent with Skills
=============================================================

Li (2026) argues that skill-based single-agent systems (SAS) offer a promising middle ground
between monolithic prompting and expensive multi-agent coordination (MAS). This module captures
the motivation, problem framing, and core research questions.
"""

from gaia.lang import claim, setting, question

# --- Core paradigm claims ---

mas_effectiveness = claim(
    "Multi-agent AI systems (MAS), where specialized agents collaborate via explicit communication, "
    "have proven effective for complex reasoning tasks. Systems such as AutoGen and MetaGPT improve "
    "reasoning performance on challenging benchmarks [@Wu2024].",
    title="MAS effectiveness",
    metadata={"source": "artifacts/2601.04748.pdf, Section 1"},
)

mas_overhead = claim(
    "Multi-agent systems incur significant computational overhead due to repeated context exchange, "
    "multi-round coordination, and verbose natural language interactions. This overhead arises because "
    "each agent call re-encodes the task description, intermediate results, and instructions.",
    title="MAS computational overhead",
    metadata={"source": "artifacts/2601.04748.pdf, Section 1"},
)

skill_definition = setting(
    "A skill is a tuple $s = (\\delta, \\pi, \\xi)$ where: "
    "$\\delta$ (skill descriptor) is a semantic description used for skill selection; "
    "$\\pi$ (execution policy) specifies how to perform the skill; "
    "$\\xi \\in \\mathcal{T} \\cup \\{\\emptyset\\}$ is the execution backend — an external tool "
    "($\\xi = t$, externalized skill) or null ($\\xi = \\emptyset$, internalized skill). "
    "Unlike tools, which are automatically triggered, skills are chosen based on the meaning and "
    "content of user requests, encapsulating not just what to do but how to reason [@Anthropic2025].",
    title="Skill definition",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.2"},
)

sas_definition = setting(
    "A Single-Agent with Skills (SAS) is a tuple $S = \\langle a, \\mathcal{S}, \\sigma \\rangle$ where: "
    "$a$ is a base language model; "
    "$\\mathcal{S} = \\{s_1, \\ldots, s_k\\}$ is a skill library; "
    "$\\sigma : \\mathcal{H} \\times \\mathcal{D} \\rightarrow \\mathcal{S}$ is a skill selector "
    "mapping context and skill descriptors $\\mathcal{D} = \\{\\delta_1, \\ldots, \\delta_k\\}$ to a skill. "
    "The selector $\\sigma$ operates over skill descriptors, not full skill specifications, "
    "reflecting that selection is based on semantic descriptors rather than complete procedural knowledge.",
    title="SAS definition",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.2"},
)

compilation_view = claim(
    "A multi-agent system can be 'compiled' into an equivalent single-agent system (SAS) by encoding "
    "each agent's behavior as a skill, thereby eliminating inter-agent communication overhead while "
    "preserving functional capability. The compilation trades inter-agent communication for skill selection.",
    title="Compilation view: MAS to SAS",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.3"},
)

# --- Core research questions ---

q_compilation_feasibility = question(
    "Can a single agent that selects from a library of skills (SAS) achieve similar modularity benefits "
    "to a multi-agent system (MAS), while reducing computational overhead?",
    title="Q1: Compilation feasibility",
)

q_skill_scaling = question(
    "How does the size of the skill library affect an LLM's ability to select the correct skill? "
    "Does skill selection exhibit capacity-limited scaling analogous to human decision-making?",
    title="Q2: Skill selection scaling",
)

# --- Contributions overview ---

contribution_compilation = claim(
    "Skill-based systems (SAS) can approximate multi-agent system (MAS) performance with significantly "
    "lower token usage (−53.7% on average) and latency (−49.5% on average) across three benchmarks "
    "(GSM8K, HumanEval, HotpotQA), while formally characterizing the compilation process from MAS to SAS.",
    title="Contribution 1: Compilation efficiency",
    metadata={"source": "artifacts/2601.04748.pdf, Section 1, Table 3"},
)

contribution_scaling = claim(
    "Skill selection exhibits non-linear scaling limits: selection accuracy remains high up to a "
    "critical library size threshold $\\kappa$ (approximately 83–92 skills for tested GPT models), "
    "then drops sharply. Semantic confusability among skills, not library size alone, is the primary "
    "driver of this degradation.",
    title="Contribution 2: Scaling limits identified",
    metadata={"source": "artifacts/2601.04748.pdf, Section 1"},
)

contribution_hierarchy = claim(
    "Hierarchical routing mitigates the skill selection scaling limits observed in flat libraries. "
    "When flat selection degrades at large library sizes ($|S| \\gg \\kappa$), hierarchical routing "
    "maintains approximately 72–85% accuracy vs. 45–63% for flat selection, providing a "
    "cognitive-science-grounded framework for scalable skill-based agents.",
    title="Contribution 3: Hierarchical routing as mitigation",
    metadata={"source": "artifacts/2601.04748.pdf, Section 1"},
)

__all__ = [
    "mas_effectiveness",
    "mas_overhead",
    "skill_definition",
    "sas_definition",
    "compilation_view",
    "q_compilation_feasibility",
    "q_skill_scaling",
    "contribution_compilation",
    "contribution_scaling",
    "contribution_hierarchy",
]
