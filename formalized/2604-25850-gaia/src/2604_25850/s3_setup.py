"""Section 3 (top + Algorithm 1): formal AHE setup -- the closed evolution
loop, role agents, evaluation protocol, and seed harness.

Source: Lin et al. 2026 [@Lin2026AHE], Section 3 introduction + Section 4.1
+ Algorithm 1.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Formal definitions: AHE outer loop and its phases
# ---------------------------------------------------------------------------

setup_ahe_outer_loop = setting(
    "**Algorithm 1 -- AHE outer loop.** Given a seed harness $H_0$, a "
    "fixed base model $M$, a benchmark $D$, $k$ rollouts per task, and "
    "a maximum iteration count $N$, the AHE outer loop iterates "
    "phases 1-6 for $t = 1, \\dots, N$: "
    "**Phase 1 (Rollout):** $T_t \\leftarrow$ ROLLOUT$(M, H_{t-1}, D, k)$, "
    "produce $k$ rollouts per task with the previous-iteration harness. "
    "**Phase 2 (Clean):** $\\widetilde T_t \\leftarrow$ CLEAN$(T_t)$, "
    "drop base64 blobs, deduplicate tool output. "
    "**Phase 3 (Attribute, $t \\geq 2$ only):** "
    "$V_t \\leftarrow$ ATTRIBUTE$(C_{t-1}, T_{t-1}, T_t)$ then "
    "$H_{t-1} \\leftarrow$ ROLLBACK$(H_{t-1}, V_t)$ -- intersect the "
    "prior manifest's predicted-fix and predicted-regression sets with "
    "observed task-level deltas to roll back ineffective edits. "
    "**Phase 4 (Distill):** $R_t \\leftarrow$ AGENTDEBUGGER$(\\widetilde T_t)$ "
    "produces the layered evidence corpus. "
    "**Phase 5 (Evolve):** $(H_t, C_t) \\leftarrow$ EVOLVE$(H_{t-1}, R_t, V_t)$, "
    "the Evolve Agent reads the corpus and emits new workspace edits "
    "plus a new change manifest. "
    "**Phase 6 (Commit):** COMMIT$(H_t, C_t, t)$ tags the iteration in "
    "git. The best-so-far harness $H_{best}$ is updated whenever "
    "pass@1$(T_t) >$ pass@1$(H_{best})$. Returns $H_{best}$.",
    title="Setup: AHE outer loop (Algorithm 1)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Algorithm 1",
        "caption": "Algorithm 1: AHE outer loop with 6 phases (rollout, clean, attribute+rollback, distill, evolve, commit).",
    },
)

setup_role_agents = setting(
    "**Three role agents.** The AHE loop has three role agents, all "
    "sharing the same base model $M$ to isolate gain to harness edits "
    "rather than analyzer or editor capability: "
    "(i) **Code Agent** -- the agent under evaluation; runs the rollouts "
    "$T_t$ on benchmark $D$ using harness $H_{t-1}$. "
    "(ii) **Agent Debugger** -- analyzes cleaned trajectories "
    "$\\widetilde T_t$ to produce per-task analysis reports and a "
    "benchmark-level overview, the layered evidence corpus $R_t$. "
    "(iii) **Evolve Agent** -- reads $R_t$ and the prior verdict $V_t$, "
    "decides which harness components to add, modify, or remove, "
    "applies edits to the workspace, and records reasoning in a change "
    "manifest $C_t$.",
    title="Setup: three role agents (Code Agent / Agent Debugger / Evolve Agent), shared base model",
)

setup_seed_nexau0 = setting(
    "**Seed harness $H_0$ -- NexAU0.** A deliberately minimal seed "
    "configuration built on the NexAU agent framework [@NexAU; @NexN1] "
    "that exposes only the `bash` (run_shell_command) tool to the "
    "model, with no skills, no middleware, no sub-agents, and no "
    "long-term memory. Every iteration of the AHE outer loop edits "
    "this workspace, so all reported gains are measured against NexAU0 "
    "as the common starting point. A seed already fitted to the "
    "target benchmark would contaminate every subsequent edit's "
    "attribution.",
    title="Setup: seed harness NexAU0 (single bash tool, minimal)",
)

setup_runtime_infrastructure = setting(
    "**Runtime infrastructure.** All runs use the NexAU framework "
    "[@NexAU; @NexN1] to instantiate the coding agent. Harbor "
    "dispatches tasks, isolates each rollout, and verifies pass/fail. "
    "Every rollout runs inside a fresh E2B remote sandbox so shell "
    "side-effects cannot leak between tasks. InMemoryTracer records "
    "trajectories and mirrors them to Langfuse. The Agent Debugger "
    "executes at concurrency 16 with a 600-second per-task timeout.",
    title="Setup: runtime infrastructure (NexAU + Harbor + E2B sandbox + InMemoryTracer + Langfuse)",
)

setup_evaluation_setup = setting(
    "**Evaluation setup.** Evolution is driven on the full 89 tasks of "
    "Terminal-Bench 2 [@TerminalBench2] (split as 4 easy / 55 medium / "
    "30 hard) with per-task timeout extended to 1 hour. For cross-"
    "benchmark transfer the AHE harness is evaluated on SWE-bench-"
    "verified [@SWEbench] (500 tasks across 7 repositories). Two "
    "metrics per configuration are reported: **pass@1** (mean binary "
    "success over $k$ rollouts per task) and **Tokens$_k$** (mean "
    "per-trial total of prompt + completion tokens across all LLM "
    "calls, in thousands). Infrastructure-aborted or timed-out trials "
    "count as pass@1 failures (matching the official terminal-bench "
    "leaderboard) and are excluded from token means to avoid truncated "
    "figures. A composite **Succ/Mtok = pass@1 * 10^6 / mean tokens "
    "per trial** combines both axes.",
    title="Setup: evaluation protocol (Terminal-Bench 2 + SWE-bench-verified, pass@1 + Tokens_k + Succ/Mtok)",
)

setup_models_used = setting(
    "**Models used.** For both the evolution loop and the main "
    "experiment, all three role agents share GPT-5.4 [@GPT54] at the "
    "high reasoning setting as their base model. For cross-model "
    "transfer, the Code Agent is re-evaluated on five alternate bases: "
    "GPT-5.4 at medium and xhigh reasoning, qwen-3.6-plus "
    "[@Qwen36; @Qwen3], gemini-3.1-flash-lite-preview "
    "[@Gemini31FlashLite], and deepseek-v4-flash [@DeepSeekV4].",
    title="Setup: base models (evolution: GPT-5.4 high; transfer: GPT-5.4 med/xhigh + qwen3.6 + gemini3.1 + deepseek-v4)",
)

setup_k_rollouts = setting(
    "**Rollout count $k$.** AHE runs with $k = 2$ rollouts per task per "
    "iteration on Terminal-Bench 2, which gives each task a pass-rate "
    "signal $r_i \\in \\{0, 0.5, 1\\}$. This stabilizes pass@1 and lets "
    "*partial-pass tasks* anchor comparative diagnosis (the rollouts "
    "that pass and fail on the same task share the same random seed, "
    "so the divergence point is the failure cause). The AHE campaign "
    "runs for $N = 10$ iterations, completing in roughly 32 hours.",
    title="Setup: k=2 rollouts per task; 10 AHE iterations; 32 hours total",
)

# ---------------------------------------------------------------------------
# Setup-level claims
# ---------------------------------------------------------------------------

claim_design_principle_observability = claim(
    "**Design principle: every loop phase must be observable.** AHE "
    "faithfully records the artifacts each phase produces -- the "
    "harness components an iteration writes, the rollout trajectories "
    "it generates, the edit decisions it commits -- and represents "
    "them in structured, layered forms that another agent can read "
    "and act on. Every observable artifact is then a candidate input "
    "to the next iteration.",
    title="Design principle: every AHE loop phase produces structured, agent-readable artifacts",
)

claim_attribute_before_distill = claim(
    "**Critical ordering: attribution runs *before* distillation.** "
    "Phase 3 (ATTRIBUTE + ROLLBACK) is sequenced before Phase 4 "
    "(AGENTDEBUGGER), so its verdict $V_t$ lands inside the evidence "
    "corpus $R_t$ and binds each prior manifest entry as a contract "
    "rather than a rationale. If distillation ran first, the manifest "
    "would be re-rationalized rather than verified.",
    title="Design choice: ATTRIBUTE before DISTILL ensures the manifest is a contract, not a rationale",
)

claim_explore_agent_seed_skills = claim(
    "**Bootstrap: a one-shot explore agent seeds reusable skills.** A "
    "one-shot explore agent runs in parallel with iteration 1 to seed "
    "a small number of reusable skills from the NexAU source code "
    "[@NexAU; @NexN1] and public coding-agent references. These "
    "skills receive no special protection: from iteration 2 onward "
    "the Evolve Agent may keep, refine, or remove them based on "
    "observed rollouts.",
    title="Setup: one-shot explore agent at iteration 1 seeds reusable skills (no special protection)",
)

__all__ = [
    "setup_ahe_outer_loop",
    "setup_role_agents",
    "setup_seed_nexau0",
    "setup_runtime_infrastructure",
    "setup_evaluation_setup",
    "setup_models_used",
    "setup_k_rollouts",
    "claim_design_principle_observability",
    "claim_attribute_before_distill",
    "claim_explore_agent_seed_skills",
]
