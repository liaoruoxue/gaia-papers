"""Section 2: Design Philosophies, Design Principles and Architectural Motivations"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    claude_code_description,
    qualitatively_new_workflows,
    agentic_shift_introduces_new_requirements,
)

# ── Five human values ──────────────────────────────────────────────────────────

value_human_decision_authority = setting(
    "Human Decision Authority: The human retains ultimate decision authority over "
    "what the system does, organized through a principal hierarchy (Anthropic, then "
    "operators, then users) that formalizes who holds authority over what. The system "
    "is designed so that humans can observe actions in real time, approve or reject "
    "proposed operations, interrupt in-progress operations, and audit after the fact.",
    title="Value: Human Decision Authority",
)

value_safety_security_privacy = setting(
    "Safety, Security, and Privacy: The system protects humans, their code, their data, "
    "and their infrastructure from harm, even when the human is inattentive or makes "
    "mistakes. This is distinct from Human Decision Authority: where authority is about "
    "the human's power to choose, safety is about the system's obligation to protect "
    "even when that power lapses. The auto-mode threat model explicitly targets four risk "
    "categories: overeager behavior, honest mistakes, prompt injection, and model misalignment.",
    title="Value: Safety, Security, and Privacy",
)

value_reliable_execution = setting(
    "Reliable Execution: The agent does what the human actually meant, stays coherent "
    "over time, and supports verifying its work before declaring success. This spans both "
    "single-turn correctness (did it interpret the request faithfully?) and long-horizon "
    "dependability (does it remain coherent across context window boundaries, session "
    "resumption, and multi-agent delegation?). The system uses a three-phase loop: "
    "gather context, take action, and verify results.",
    title="Value: Reliable Execution",
)

value_capability_amplification = setting(
    "Capability Amplification: The system materially increases what the human can "
    "accomplish per unit of effort and cost. The system is described by its creators "
    "as 'a Unix utility rather than a traditional product,' built from the smallest "
    "building blocks that are 'useful, understandable, and extensible.' The architecture "
    "invests in deterministic infrastructure rather than decision scaffolding, on the "
    "premise that increasingly capable models benefit more from a rich operational "
    "environment than from frameworks that constrain their choices.",
    title="Value: Capability Amplification",
)

value_contextual_adaptability = setting(
    "Contextual Adaptability: The system fits the user's specific context (their project, "
    "tools, conventions, and skill level) and the relationship improves over time. The "
    "extension architecture (CLAUDE.md, skills, MCP, hooks, plugins) provides configurability "
    "at multiple levels of context cost. Longitudinal data shows that auto-approve rates "
    "increase from approximately 20% at fewer than 50 sessions to over 40% by 750 sessions, "
    "reflecting a system designed for trust trajectories rather than fixed trust states.",
    title="Value: Contextual Adaptability",
)

# ── Thirteen design principles ─────────────────────────────────────────────────

principle_deny_first = setting(
    "Deny-first with human escalation: Deny rules override ask rules override allow rules, "
    "and unrecognized actions are escalated to the user rather than allowed silently. "
    "Serves Human Decision Authority and Safety.",
    title="Principle: Deny-first with human escalation",
)

principle_graduated_trust = setting(
    "Graduated trust spectrum: A spectrum of permission modes that users traverse over time, "
    "from plan (user approves all plans) through default, acceptEdits, auto (ML classifier), "
    "dontAsk, to bypassPermissions. Serves Authority and Adaptability.",
    title="Principle: Graduated trust spectrum",
)

principle_defense_in_depth = setting(
    "Defense in depth with layered mechanisms: Multiple overlapping safety boundaries "
    "using different techniques. Serves Safety, Authority, and Reliability.",
    title="Principle: Defense in depth",
)

principle_externalized_programmable_policy = setting(
    "Externalized programmable policy: Policy is externalized via configs and lifecycle "
    "hooks rather than hardcoded. Serves Safety, Authority, and Adaptability.",
    title="Principle: Externalized programmable policy",
)

principle_context_as_scarce_resource = setting(
    "Context as scarce resource with progressive management: The context window is the "
    "binding resource constraint, managed through a graduated pipeline rather than "
    "single-pass truncation. Serves Reliability and Capability.",
    title="Principle: Context as scarce resource",
)

principle_append_only_state = setting(
    "Append-only durable state: Session transcripts are stored as mostly append-only JSONL "
    "files, favoring auditability over query power. Serves Reliability and Authority.",
    title="Principle: Append-only durable state",
)

principle_minimal_scaffolding = setting(
    "Minimal scaffolding, maximal operational harness: The architecture invests in "
    "operational infrastructure that lets the model reason freely, rather than scaffolding-side "
    "reasoning. An estimated 1.6% of the codebase constitutes AI decision logic, with "
    "the remaining 98.4% being operational infrastructure. Serves Capability and Reliability.",
    title="Principle: Minimal scaffolding",
)

principle_values_over_rules = setting(
    "Values over rules: The system cultivates good judgment and sound values that can be "
    "applied contextually, rather than rigid decision procedures, paired with deterministic "
    "guardrails. Serves Capability and Authority.",
    title="Principle: Values over rules",
)

principle_composable_extensibility = setting(
    "Composable multi-mechanism extensibility: Layered extension mechanisms at different "
    "context costs rather than a single unified extension API. Serves Capability and Adaptability.",
    title="Principle: Composable extensibility",
)

principle_reversibility_weighted = setting(
    "Reversibility-weighted risk assessment: Lighter oversight for reversible and read-only "
    "actions; heavier for irreversible ones. Serves Capability and Safety.",
    title="Principle: Reversibility-weighted risk assessment",
)

principle_transparent_file_config = setting(
    "Transparent file-based configuration and memory: User-visible, version-controllable "
    "files rather than opaque databases or embedding-based retrieval. Serves Adaptability "
    "and Authority.",
    title="Principle: Transparent file-based configuration",
)

principle_isolated_subagent_boundaries = setting(
    "Isolated subagent boundaries: Subagents operate in isolation with rebuilt permission "
    "context and tool sets, rather than sharing the parent's context and permissions. "
    "Serves Reliability, Safety, and Capability.",
    title="Principle: Isolated subagent boundaries",
)

principle_graceful_recovery = setting(
    "Graceful recovery and resilience: Silently recover from errors and reserve human "
    "attention for unrecoverable situations. Serves Reliability and Capability.",
    title="Principle: Graceful recovery",
)

# ── Key architectural claims from Section 2 ────────────────────────────────────

five_values_motivate_architecture = claim(
    "Claude Code's architecture is motivated by five human values: human decision authority, "
    "safety and security, reliable execution, capability amplification, and contextual "
    "adaptability. These values are operationalized through thirteen design principles, "
    "each answering a recurring question that production coding agents must resolve.",
    title="Five values motivate thirteen design principles",
    background=[
        value_human_decision_authority,
        value_safety_security_privacy,
        value_reliable_execution,
        value_capability_amplification,
        value_contextual_adaptability,
    ],
)

strat_five_values_motivate = support(
    [qualitatively_new_workflows, agentic_shift_introduces_new_requirements],
    five_values_motivate_architecture,
    reason=(
        "The qualitatively new workflows enabled by Claude Code (@qualitatively_new_workflows) "
        "and the novel architectural requirements of agentic tools "
        "(@agentic_shift_introduces_new_requirements) motivate the five human values "
        "framework. Capability amplification is directly evidenced by the 27% new-task rate. "
        "Safety is required because autonomous action without counterpart in suggestion-based "
        "tools demands new safety architectures. This framework is documented in official "
        "Anthropic sources (Tier A evidence) and confirmed through source-level analysis (Tier B)."
    ),
    prior=0.85,
)

design_principles_distinguish_from_alternatives = claim(
    "Claude Code's principle set is distinctive in combining minimal decision scaffolding "
    "with layered policy enforcement, values-based judgment with deny-first defaults, and "
    "progressive context management with composable extensibility. This distinguishes it "
    "from three major alternative design families: rule-based orchestration (LangGraph), "
    "container-isolated execution (SWE-Agent, OpenHands), and version-control-as-safety (Aider).",
    title="Claude Code principles distinguish from alternatives",
    background=[
        principle_deny_first,
        principle_minimal_scaffolding,
        principle_composable_extensibility,
    ],
)

strat_principles_distinguish = support(
    [five_values_motivate_architecture],
    design_principles_distinguish_from_alternatives,
    reason=(
        "Given the five-value framework (@five_values_motivate_architecture), the thirteen "
        "design principles follow as specific answers to recurring design questions. "
        "The combination of minimal scaffolding + layered policy + values-over-rules is "
        "unique: LangGraph uses explicit state graphs (not minimal scaffolding), "
        "SWE-Agent uses container isolation (not layered policy), and Aider uses git "
        "rollback (not deny-first). These differences are directly traceable to the "
        "different value prioritizations of each system."
    ),
    prior=0.88,
)

long_term_capability_preservation_lens = claim(
    "Long-term human capability preservation is applied as an evaluative lens rather than "
    "a co-equal design value: Anthropic's own study of 132 engineers and researchers "
    "documents a 'paradox of supervision' in which overreliance on AI risks atrophying "
    "the skills needed to supervise it, and independent research finds that developers in "
    "AI-assisted conditions score 17% lower on comprehension tests. This concern is not "
    "prominently reflected as a design driver in Claude Code's architecture.",
    title="Long-term capability preservation as evaluative lens",
)

strat_long_term_lens = support(
    [qualitatively_new_workflows],
    long_term_capability_preservation_lens,
    reason=(
        "The same capability amplification that produces @qualitatively_new_workflows "
        "(27% new tasks) creates the risk of skill atrophy. The evaluative lens surfaces "
        "a tension: while the architecture is optimized for short-term amplification, "
        "empirical evidence (Shen and Tamkin, 2026; Huang et al., 2025) shows potential "
        "long-term costs to human comprehension and skill that the architecture does not "
        "explicitly address. This claim is based on Tier A and Tier C evidence."
    ),
    prior=0.82,
)
