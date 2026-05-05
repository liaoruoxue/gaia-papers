"""Section 3.1 (Pillar 1): component observability via the NexAU substrate.

Decoupled, file-level harness substrate that maps each failure pattern to a
single component class. Source: Lin et al. 2026 [@Lin2026AHE], Section 3.1.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Pillar 1 setup: seven editable component types
# ---------------------------------------------------------------------------

setup_seven_component_types = setting(
    "**Seven editable component types as files at fixed mount points.** "
    "AHE instantiates the harness $H$ on the NexAU framework "
    "[@NexAU; @NexN1] which exposes seven orthogonal component types "
    "as explicit files at fixed mount points in a single workspace: "
    "(1) **system prompt** (`workspace/systemprompt.md`), "
    "(2) **tool description** (`workspace/tool_descriptions/*.tool.yaml`), "
    "(3) **tool implementation** (`workspace/tools/`), "
    "(4) **middleware** (`workspace/middleware/`), "
    "(5) **skill** (`workspace/skills/`), "
    "(6) **sub-agent configuration** (`workspace/sub_agents/`), and "
    "(7) **long-term memory** (`workspace/LongTermMEMORY.md`). The "
    "component types are loosely coupled: adding a middleware does "
    "not require editing the system prompt, and adding a skill does "
    "not require touching any tool.",
    title="Setup: 7 editable component types as files (prompt / tool desc / tool impl / middleware / skill / sub-agent / long-term memory)",
)

setup_workspace_git_history = setting(
    "**Workspace git history as the action ledger.** Each logical edit "
    "becomes one commit on the workspace's git history, which yields "
    "**file-level diffs** and **rollback granularity** for free. The "
    "Evolve Agent's edits are constrained to the `workspace/` "
    "directory; the `runs/` directory, tracer, verifier, and LLM "
    "configuration are read-only. The seed system prompt is marked "
    "non-deletable (Appendix B.1).",
    title="Setup: workspace git history (one logical edit = one commit, file-level rollback)",
)

# ---------------------------------------------------------------------------
# Pillar 1 claims
# ---------------------------------------------------------------------------

claim_decoupling_realizes_observability = claim(
    "**Decoupling realizes component observability.** Because the seven "
    "component types are loosely coupled and each lives in a fixed file "
    "or directory, every failure pattern observed in trajectories maps "
    "to a single component class, giving the Evolve Agent a clean "
    "*action space* (which file to edit) and localizing every pass-"
    "rate change to one file rather than scattering it across hundreds "
    "of lines of unstructured prompt prose.",
    title="Pillar 1 claim: file-level decoupling makes the action space clean and per-edit pass-rate change localized",
)

claim_explicit_revertible_action_space = claim(
    "**The action space is explicit and revertible.** Each Evolve Agent "
    "edit corresponds to a typed action 'modify component class $c$' "
    "and is recorded as a single git commit on the workspace. Because "
    "edits live in version control and component boundaries are "
    "enforced, **any individual edit can be reverted at file "
    "granularity** without disturbing other components. This solves "
    "obstacle (O1) -- heterogeneous action space -- by giving every "
    "component class a uniform file-shaped action.",
    title="Pillar 1 claim: action space is explicit (typed by component class) and revertible (file-level)",
)

claim_minimal_seed_attribution = claim(
    "**Minimal seed prevents attribution contamination.** Because the "
    "seed NexAU0 is bash-only with no middleware, no skills, and no "
    "long-term memory, every component AHE adds across iterations "
    "must earn its place against measured rollouts. A seed already "
    "fitted to the target benchmark would contaminate every "
    "subsequent edit's attribution: the loop could not distinguish "
    "gains from the seed from gains from the loop.",
    title="Pillar 1 claim: minimal seed earns every component against measured rollouts, prevents attribution contamination",
)

claim_component_type_table = claim(
    "**Component-type table (Appendix B.2).** The Evolve Agent receives "
    "a structured table of the seven component types with their files, "
    "characteristics, and when-to-use guidance:\n\n"
    "| Component | Files | Characteristics | When to use |\n"
    "|---|---|---|---|\n"
    "| System Prompt | `workspace/systemprompt.md` | Advisory; applies to all tasks | Behavioral rules, workflow guidance |\n"
    "| Tool Description | `tool_descriptions/*.tool.yaml` | Co-located with tool | Clarify tool usage, examples, pitfalls |\n"
    "| Tool Implementation | `tools/` | Controls tool behavior directly | New capabilities, smarter error handling |\n"
    "| Middleware | `middleware/` + `code_agent.yaml` | Hooks into agent loop pipeline | Intercept/transform at execution level |\n"
    "| Skill | `skills/` + `code_agent.yaml` | On-demand, loaded when relevant | Reusable workflow patterns |\n"
    "| Sub-Agent | `sub_agents/{name}/` + `code_agent.yaml` | Delegated, isolated context | Offload specialized subtask |\n"
    "| Long-Term Memory | `LongTermMEMORY.md` | Persistent cross-session knowledge | Recurring pitfalls, proven strategies |\n",
    title="Pillar 1 reference: component-type table presented to the Evolve Agent",
)

__all__ = [
    "setup_seven_component_types",
    "setup_workspace_git_history",
    "claim_decoupling_realizes_observability",
    "claim_explicit_revertible_action_space",
    "claim_minimal_seed_attribution",
    "claim_component_type_table",
]
