"""Section 3.2 (Pillar 2): experience observability via the Agent Debugger.

Layered trajectory evidence corpus distilled from raw rollouts and indexed for
drill-down access. Source: Lin et al. 2026 [@Lin2026AHE], Section 3.2.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Pillar 2 setup
# ---------------------------------------------------------------------------

setup_agent_debugger_framework = setting(
    "**Agent Debugger framework [@AgentDebugger].** A framework that "
    "uses an agent to explore raw trajectories framed as a navigable, "
    "file-based environment. Each trajectory message lives in its own "
    "file and is reached through generic shell and scripting tools. "
    "Traces with the same query are placed in one environment, and "
    "the debugger is required to analyze the root cause of failure or "
    "the success pattern.",
    title="Setup: Agent Debugger framework (file-based trajectory exploration)",
)

setup_layered_corpus_artifacts = setting(
    "**Layered evidence corpus structure.** The Agent Debugger produces "
    "two layers of structured analysis plus a trace fallback: "
    "(L1) **Per-task analysis report** -- one Markdown file per task "
    "in `analysis/detail/{task_name}.md` documenting failure root "
    "cause or success pattern, including the pass/fail status of each "
    "rollout. "
    "(L2) **Benchmark-level overview** -- one `analysis/overview.md` "
    "aggregated from every per-task report; the entry point for every "
    "iteration. "
    "(L3) **Original traces (fallback)** -- raw and lightly processed "
    "(deduped, base64-stripped) trajectory files; the Evolve Agent "
    "may consult them to verify claims in the reports.",
    title="Setup: 3-layer evidence corpus (overview / per-task analysis / raw traces)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 2",
        "caption": "Fig. 2: Raw trace ~10M tokens distilled into ~10K-token Evidence corpus that the Evolve Agent reads.",
    },
)

setup_progressive_disclosure = setting(
    "**Progressive disclosure [@ProgressiveDisclosure].** All evidence-"
    "corpus content is provided as files allowing progressive "
    "disclosure: the Evolve Agent reads the overview first, drills "
    "into per-task details for tasks needing deeper investigation, "
    "and only falls back to raw traces when analysis is missing or "
    "insufficient. This saves tokens and enables better agent "
    "decisions.",
    title="Setup: progressive disclosure (overview -> per-task -> raw traces, on demand)",
)

# ---------------------------------------------------------------------------
# Pillar 2 claims
# ---------------------------------------------------------------------------

claim_token_compression = claim(
    "**Token compression: 10M -> 10K through layered distillation.** "
    "A single Terminal-Bench 2 evaluation round produces roughly **10 "
    "million tokens** of raw trajectory across all 89 tasks at $k=2$. "
    "The Agent Debugger distills this into a layered corpus of roughly "
    "**10 thousand tokens** at the overview + per-task-summary level, a "
    "~1000x compression that fits comfortably in a single Evolve Agent "
    "context window.",
    title="Pillar 2 claim: 10M-token raw trace distilled to ~10K-token overview (~1000x compression)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 2",
        "caption": "Fig. 2: ~10M tokens raw -> ~10K tokens distilled overview.",
    },
)

claim_distillation_realizes_experience_obs = claim(
    "**Distillation realizes experience observability.** Because the "
    "Evolve Agent consumes structured root causes (overview + per-task "
    "analysis with explicit pass/fail status grounding) rather than "
    "raw token logs, it can extract failure patterns class-by-class "
    "rather than rollout-by-rollout. This solves obstacle (O2) -- "
    "voluminous unstructured trajectories.",
    title="Pillar 2 claim: layered distillation gives the Evolve Agent structured root causes, not raw logs",
)

claim_per_task_pass_fail_grounding = claim(
    "**Per-task analysis is grounded in pass/fail status.** Each "
    "per-task analysis report includes the pass/fail status of every "
    "rollout for that task, so the Evolve Agent's reading of the "
    "report is anchored in the verifier's verdict rather than in the "
    "Agent Debugger's narrative interpretation. This grounding is "
    "what makes per-task reports usable as failure-pattern evidence "
    "rather than as opinion.",
    title="Pillar 2 claim: per-task analysis is grounded in verifier-verified pass/fail status",
)

claim_partial_pass_anchor = claim(
    "**Partial-pass tasks anchor comparative diagnosis.** Running "
    "$k = 2$ rollouts per task means each task carries a per-rollout "
    "pass/fail signal. **Partial-pass** tasks (one rollout passes, "
    "one fails, both at the same random seed) are the most diagnostic "
    "case: comparing the divergence point between the passing and "
    "failing rollouts of the same task isolates the failure cause "
    "more cleanly than comparing across tasks. The Agent Debugger "
    "explicitly groups traces by query so partial-pass diagnoses are "
    "co-located.",
    title="Pillar 2 claim: partial-pass tasks (k=2 rollouts split) are the most diagnostic signal",
)

__all__ = [
    "setup_agent_debugger_framework",
    "setup_layered_corpus_artifacts",
    "setup_progressive_disclosure",
    "claim_token_compression",
    "claim_distillation_realizes_experience_obs",
    "claim_per_task_pass_fail_grounding",
    "claim_partial_pass_anchor",
]
