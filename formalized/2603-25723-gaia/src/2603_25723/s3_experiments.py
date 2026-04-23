"""Section 3: Experimental Design"""

from gaia.lang import (
    claim, setting, question,
    support,
)

from .motivation import (
    q_behavioral_effect,
    q_composability,
    q_migration,
)

from .s2_approach import (
    nlah_definition,
    ihr_definition,
    ihr_separates_concerns,
    file_backed_state_definition,
)

# --- Settings: experimental setup ---

swe_bench_setting = setting(
    "SWE-bench Verified evaluates repository-level software engineering: given a "
    "GitHub issue, the agent must produce a patch that passes the issue's test suite. "
    "The benchmark uses a curated set of verified human-solvable problems.",
    title="SWE-bench Verified benchmark definition",
)

osworld_setting = setting(
    "OSWorld evaluates computer-use agents on desktop tasks requiring multi-step "
    "GUI interaction, file management, and tool use across operating system environments.",
    title="OSWorld benchmark definition",
)

trae_harness_setting = setting(
    "TRAE (Test-time Reasoning and Execution Agent) is an LLM-based software "
    "engineering agent harness. In this study, TRAE is used as the native code "
    "harness for SWE-bench Verified experiments.",
    title="TRAE harness definition",
)

live_swe_setting = setting(
    "Live-SWE is a lighter-weight SWE benchmark regime used in this study, "
    "evaluating agents on a subset of SWE-bench tasks under tighter budgets.",
    title="Live-SWE benchmark definition",
)

os_symphony_setting = setting(
    "OS-Symphony is the native code harness used for OSWorld evaluation. "
    "It implements a screenshot-grounded repair loop: verify the previous step, "
    "inspect the current screen, choose the next GUI action, and retry locally "
    "when focus or selection errors occur.",
    title="OS-Symphony harness definition",
)

codex_backend_setting = setting(
    "In the IHR instantiation used in experiments, the backend is realized by "
    "OpenAI Codex with terminal tools and a multi-agent interface. The shared "
    "runtime charter is carried by a fixed runtime skill; benchmark-specific "
    "harness logic is carried by harness skills.",
    title="IHR backend instantiation",
)

rq1_ablation_design = setting(
    "RQ1 ablation design: Three conditions are compared under fixed budgets. "
    "(1) Full IHR: runtime skill (shared charter) + harness skill (task-family logic). "
    "(2) w/o RTS: harness skill only, no runtime skill. "
    "(3) w/o HS: runtime skill only, no harness skill. "
    "Evaluated on SWE-bench Verified (TRAE and Live-SWE harness families).",
    title="RQ1 ablation experimental design",
)

rq2_composition_design = setting(
    "RQ2 composition design: Starting from a benchmark-specific Basic baseline, "
    "one module is added at a time: file-backed state, evidence-backed answering, "
    "verifier, self-evolution, multi-candidate search, and dynamic orchestration. "
    "Basic on SWE is a bare Codex baseline with shell, file reading/writing/editing. "
    "Basic on OSWorld is the NLAH realization of OS-Symphony before adding extra modules.",
    title="RQ2 composition experimental design",
)

rq3_migration_design = setting(
    "RQ3 migration study: Each harness appears in two realizations — original source "
    "code and reconstructed NLAH — evaluated under a shared reporting schema. "
    "Target is task-level equivalence (comparable exposed logic, contracts, "
    "and benchmark-facing artifacts), not identical internal traces.",
    title="RQ3 migration experimental design",
)

# --- Claims about experimental setup ---

instantiation_valid = claim(
    "The factorization of IHR into backend (Codex with tools and multi-agent interface), "
    "shared runtime charter (runtime skill), and task-family harness logic (harness skills) "
    "enables controlled ablations: the runtime skill and harness skill can each be independently "
    "removed or replaced to isolate their contributions.",
    title="IHR instantiation supports controlled ablation",
)

strat_instantiation_factorization = support(
    [ihr_separates_concerns],
    instantiation_valid,
    reason=(
        "Because @ihr_separates_concerns — IHR cleanly separates shared runtime charter "
        "from task-family harness logic — the concrete instantiation as runtime skill plus "
        "harness skill directly exposes these two dimensions for ablation. Removing "
        "runtime skill leaves only harness logic; removing harness skill leaves only "
        "the charter. This is a valid controlled experiment design for isolating each "
        "component's contribution."
    ),
    prior=0.90,
    background=[rq1_ablation_design, codex_backend_setting],
)
