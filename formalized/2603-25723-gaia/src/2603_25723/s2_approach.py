"""Section 2: Natural-Language Agent Harnesses and Intelligent Harness Runtime"""

from gaia.lang import (
    claim, setting, question,
    support, deduction,
    contradiction,
)

from .motivation import (
    harness_definition,
    harness_logic_buried,
    harness_hard_to_compare,
    context_engineering_definition,
)

# --- Settings (formal definitions) ---

nlah_definition = setting(
    "A Natural-Language Agent Harness (NLAH) is a structured natural-language "
    "representation of harness control that exposes harness behavior in editable "
    "natural language, bound to explicit contracts and artifact carriers. "
    "A NLAH specifies: (1) roles and delegation boundaries, (2) stage structure "
    "with explicit contracts and gates per stage, (3) tool and output adapters "
    "for runtime bridging, (4) durable state conventions (file paths, artifact "
    "semantics), and (5) a failure taxonomy of named failure modes driving recovery.",
    title="NLAH formal definition",
)

ihr_definition = setting(
    "The Intelligent Harness Runtime (IHR) is a shared runtime that interprets "
    "NLAHs directly. IHR decomposes into three components: (1) an in-loop LLM "
    "that reads the harness, current state, and runtime charter and selects the "
    "next action; (2) a backend providing terminal tools and a multi-agent "
    "interface (spawning and supervising child agents); and (3) a runtime charter "
    "encoding shared policy (budget accounting, artifact semantics, state management, "
    "permission boundaries).",
    title="IHR formal definition",
)

agent_call_definition = setting(
    "Formally, a task is T = (p, F_in, κ), where p is the task prompt, F_in is "
    "the set of input files or linked resources, and κ is an execution contract "
    "(required outputs, budget, permission scope, completion conditions, designated "
    "output paths). An agent call is AgentCall(T, Ω_in_t) = (A_t, ΔΩ_t, y_t), "
    "where Ω_in_t is the visible environment at call start, A_t is the designated "
    "artifact set, ΔΩ_t are environment modifications, and y_t is a normalized "
    "final response.",
    title="Formal agent call definition",
)

file_backed_state_definition = setting(
    "The file-backed state module externalizes durable state into path-addressable "
    "artifacts. It enforces three properties: (1) externalized — state is written to "
    "artifacts rather than held only in transient context; (2) path-addressable — "
    "later stages reopen the exact object by path; (3) compaction-stable — state "
    "survives truncation, restart, and delegation.",
    title="File-backed state module definition",
)

# --- Claims about the NLAH/IHR approach ---

nlah_is_portable = claim(
    "NLAHs are portable, executable artifacts: harness logic that previously required "
    "reading controller source code can be expressed as editable natural-language "
    "text, transferred across runtimes, and interpreted by IHR without re-implementing "
    "the harness in code.",
    title="NLAHs make harness logic portable and executable",
)

ihr_separates_concerns = claim(
    "IHR separates the shared runtime charter (universal policy: budget accounting, "
    "artifact semantics, state management, permission boundaries) from task-family "
    "harness logic (benchmark-specific stages, roles, contracts). This factorization "
    "allows controlled ablations of shared runtime policy versus benchmark-specific "
    "harness logic.",
    title="IHR cleanly separates runtime charter from harness logic",
)

nlah_exposes_contracts = claim(
    "NLAHs make harness-wide contracts, role boundaries, state semantics, failure "
    "handling, and runtime-facing adapters first-class and jointly executable under "
    "a shared runtime. This is the gap not closed by prior natural-language carrier "
    "work (AGENTS.md, skill bundles), which attached local instructions but did not "
    "formalize these as executable harness objects.",
    title="NLAHs expose harness contracts as executable objects",
)

file_backed_state_addresses_truncation = claim(
    "Long-horizon autonomy fails when critical state remains implicit or ephemeral. "
    "The file-backed state module, by enforcing externalized, path-addressable, "
    "and compaction-stable properties, improves agent stability under context "
    "truncation and branching.",
    title="File-backed state improves stability under context truncation",
)

nlah_enables_module_ablation = claim(
    "Because harness patterns are explicit in NLAHs, individual modules (file-backed "
    "state, evidence-backed answering, verifier, self-evolution, multi-candidate "
    "search, dynamic orchestration) can be composed and ablated at the pattern level "
    "under a shared runtime substrate.",
    title="Explicit harness patterns enable module-level ablation",
)

# --- Strategy: why IHR's factorization solves the buried-harness problem ---

strat_nlah_solves_burial = support(
    [nlah_is_portable, ihr_separates_concerns, nlah_exposes_contracts],
    nlah_enables_module_ablation,
    reason=(
        "The NLAH/IHR approach addresses @harness_hard_to_compare by making harness "
        "logic an explicit artifact. @nlah_is_portable means harnesses can be transferred "
        "across runtimes. @ihr_separates_concerns means shared charter and task-specific "
        "logic are cleanly separated, enabling controlled ablations. @nlah_exposes_contracts "
        "means contracts, roles, and adapters are first-class — allowing individual modules "
        "to be composed and ablated independently, unlike bundled code harnesses."
    ),
    prior=0.88,
    background=[harness_hard_to_compare, nlah_definition, ihr_definition],
)

file_backed_state_design_rationale = claim(
    "The file-backed state module design (externalized, path-addressable, compaction-stable) "
    "is motivated by the three failure modes of implicit state in long-horizon agents: "
    "state lost to context truncation, state inaccessible by path after delegation, and "
    "state lost on restart or branching.",
    title="File-backed state module design rationale",
)

strat_file_backed_state_motivation = support(
    [file_backed_state_addresses_truncation],
    file_backed_state_design_rationale,
    reason=(
        "The file-backed state module is motivated by the observation that long-horizon "
        "autonomy breaks when state is implicit or ephemeral (@file_backed_state_addresses_truncation). "
        "The three enforced properties — externalized, path-addressable, compaction-stable — "
        "directly address each failure mode: state lost to context truncation, state inaccessible "
        "by path after delegation, and state lost on restart."
    ),
    prior=0.87,
    background=[file_backed_state_definition],
)
