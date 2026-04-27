"""Motivation: planning, verification, and failure modes in multi-agent LLM systems.

Corresponds to Section 1 (Introduction) of the source paper.
"""

from gaia.lang import claim, setting, question, support

# ---------- Settings: framing definitions ----------

mas_setting = setting(
    "A multi-agent LLM system orchestrates several large-language-model "
    "(LLM) agents that collaborate on a shared objective. Each agent may "
    "specialize in a role such as planning, execution, retrieval, or "
    "verification, and may have access to external tools. The plan is "
    "typically represented as a directed acyclic graph (DAG) of subtasks "
    "where the output of one agent feeds the input of another.",
    title="Multi-agent LLM system",
)

dag_plan_setting = setting(
    "A DAG-structured plan is a directed acyclic graph $G=(V,E)$ where "
    "each node $v \\in V$ is a subtask with an instruction and metadata, "
    "and each edge $(u,v) \\in E$ indicates that subtask $v$ consumes some "
    "output produced by subtask $u$. A topological order over $V$ respects "
    "all dependencies.",
    title="DAG-structured plan",
)

verification_setting = setting(
    "Verification of an agent's output is a procedure that returns a "
    "pass/fail decision (and optionally feedback) given the output and a "
    "specification of acceptable behavior. The specification may be a "
    "Python assertion, a natural-language criterion, an LLM judge, or a "
    "formal symbolic check.",
    title="Verification (general definition)",
)

# ---------- Research questions ----------

q_reliable_mas = question(
    "How can a multi-agent LLM system achieve reliable coordination and "
    "self-refinement when individual agents fail in heterogeneous, "
    "context-dependent ways?",
    title="Research question: reliable multi-agent coordination",
)

# ---------- Claims: framing assertions in the introduction ----------

multi_agent_planning_central = claim(
    "Effective planning is a central component of multi-agent LLM "
    "collaboration: a planner must understand the overall task, decompose "
    "it into subtasks, model dependencies, and assign responsibilities to "
    "agents with different capabilities. Without strong planning, the DAG "
    "workflow becomes fragile because it depends on smooth communication "
    "and accurate handoffs between agents.",
    title="Planning is central (and fragile) in MAS",
)

agent_failure_modes = claim(
    "In multi-agent LLM systems, agents can fail in at least three "
    "qualitatively different ways: (i) producing no result, (ii) producing "
    "output in the wrong format that breaks downstream consumption, and "
    "(iii) producing results that look reasonable but diverge from what "
    "the planner or downstream agents expect (e.g., a 'section extractor' "
    "returning raw text rather than the expected JSON, or "
    "misinterpreting 'summarize key claim' as 'summarize all paragraphs').",
    title="Heterogeneous failure modes in MAS",
)

failures_context_dependent = claim(
    "Execution failure in multi-agent systems is **context-dependent**: an "
    "agent's output may be locally correct yet still cause downstream "
    "failure if it violates plan-level expectations on format, naming, or "
    "interpretation. Therefore, factual or logical correctness alone is "
    "insufficient for reliable multi-agent coordination.",
    title="Failure is context-dependent, not just correctness-bound",
)

existing_verification_misses_context = claim(
    "Existing LLM-system verification mechanisms — typically checking "
    "factual accuracy, logical consistency, or final-answer quality "
    "[@Miao2024SelfCheck; @Stechly2024SelfVerification] — rarely capture "
    "interpretation or handoff failures, because the verifier has no "
    "explicit specification of plan-level acceptance criteria for each "
    "subtask.",
    title="Existing verification misses context-dependent failures",
)

# Subordinate support: from heterogeneous failure modes to context-dependence.
strat_failures_context = support(
    [agent_failure_modes],
    failures_context_dependent,
    background=[mas_setting, dag_plan_setting],
    reason=(
        "From the enumeration of failure modes in @agent_failure_modes — "
        "in particular, format mismatches and misinterpretations of the "
        "subtask brief — it follows that whether an output causes a "
        "downstream failure depends on plan-level expectations, not on "
        "intrinsic correctness alone. Hence failure is context-dependent "
        "in the sense of @failures_context_dependent. The argument relies "
        "on the DAG handoff structure (@dag_plan_setting) of multi-agent "
        "systems (@mas_setting)."
    ),
    prior=0.9,
)

# Subordinate support: existing verification gap follows from "context dependence + correctness-only checks".
strat_existing_gap = support(
    [failures_context_dependent],
    existing_verification_misses_context,
    background=[verification_setting],
    reason=(
        "Standard verification (@verification_setting) checks factual "
        "accuracy, logical consistency, or final-answer quality. Because "
        "failures are context-dependent (@failures_context_dependent), "
        "checks that ignore plan-level acceptance criteria cannot detect "
        "format, naming, or interpretation mismatches. Cited prior work "
        "[@Miao2024SelfCheck; @Stechly2024SelfVerification] documents "
        "exactly this limitation."
    ),
    prior=0.85,
)

# ---------- The contribution claim (overall thesis) ----------

contribution_verimap = claim(
    "VeriMAP — a multi-agent LLM framework whose **planner generates "
    "subtask-level verification functions** (Python and natural-language "
    "VFs), enforces Structured I/O with Named Variables, and pairs "
    "executors with paired verifiers under a coordinator that handles "
    "retries and replanning — improves the robustness, interpretability, "
    "and accuracy of multi-agent LLM systems on diverse complex tasks "
    "[@Xu2025VeriMAP].",
    title="VeriMAP: thesis statement",
)

# Wire 'multi_agent_planning_central' to the rest of the reasoning graph:
# it is an unconditional framing claim that motivates the whole research line.
strat_planning_central = support(
    [agent_failure_modes],
    multi_agent_planning_central,
    background=[mas_setting, dag_plan_setting],
    reason=(
        "Given the heterogeneous failure modes of @agent_failure_modes "
        "(agents producing nothing, wrong format, or misinterpreted "
        "outputs), reliable coordination across the DAG "
        "(@dag_plan_setting) of a multi-agent system (@mas_setting) "
        "fundamentally depends on planning quality — the planner must "
        "decide who does what, what constitutes acceptable output, and "
        "how outputs flow downstream. Hence @multi_agent_planning_central."
    ),
    prior=0.85,
)
