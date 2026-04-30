"""Introduction: Motivation and Problem Statement"""

from gaia.lang import claim, setting, question, support

# ── Settings: background context ─────────────────────────────────────────────

setup_prm = setting(
    "Process Reward Models (PRMs) provide step-level supervision during both "
    "training and inference, enabling fine-grained verification of intermediate "
    "reasoning steps. PRMs have demonstrated remarkable success in mathematical "
    "reasoning and code generation [@MathShepherd2024; @QwenPRM2025].",
    title="PRM background"
)

setup_data_analysis = setting(
    "Automated data analysis agents use LLMs as backbones to generate code, "
    "execute it in interpreters, and derive evidence-based insights from complex "
    "datasets. The agent follows a ReAct paradigm: at each step it generates "
    "analysis reasoning (z), code action (a), and receives execution observation (o).",
    title="Data analysis agent setup"
)

setup_outcome_only = setting(
    "Prevailing approaches to automated data analysis focus only on outcome "
    "supervision — verifying whether the final answer is correct — while "
    "overlooking the multi-step rigor of the analysis process.",
    title="Outcome-only supervision paradigm"
)

# ── Claims: problem characterization ─────────────────────────────────────────

claim_silent_errors = claim(
    "Silent Errors: General PRMs fail to identify logical flaws in data analysis "
    "that yield incorrect results without triggering interpreter exceptions. "
    "Example: an agent claims to have drawn a 5.5 km buffer zone on a map and "
    "saves the visualization, but the buffer is not actually rendered. The code "
    "interpreter reports 'Successfully saved' — no exception is raised. General "
    "PRMs judge this step as correct.",
    title="Silent errors in data analysis",
    metadata={"source_table": "artifacts/2604.24198.pdf, Table 1"}
)

claim_grounding_errors = claim(
    "Grounding Errors: General PRMs mistake necessary trial-and-error exploration "
    "for irrecoverable failures. When a data analysis agent's prior knowledge "
    "conflicts with actual data (e.g., using key 'dataset' when the actual key is "
    "'Dataset'), the resulting KeyError triggers environment feedback that enables "
    "correction. General PRMs penalize these exploratory steps as incorrect, "
    "suppressing necessary environment interaction.",
    title="Grounding errors in data analysis",
    metadata={"source_table": "artifacts/2604.24198.pdf, Table 1"}
)

claim_prm_fails_on_analysis = claim(
    "State-of-the-art general PRMs (Math-Shepherd-7B, Qwen2.5-Math-PRM-7B/72B, "
    "ReasonFlux-PRM-7B, ThinkPRM-14B, GenPRM-32B) perform poorly on data analysis "
    "tasks. On the DABStep Hard subset, Math-Shepherd achieves only 23.28% at N=4 "
    "and degrades to 19.31% at N=16, indicating that existing PRMs cannot reliably "
    "distinguish valid reasoning from hallucinations in data analysis.",
    title="General PRMs fail on data analysis tasks",
    metadata={"figure": "artifacts/2604.24198.pdf, Figure 2(a)"}
)

claim_prm_scaling_failure = claim(
    "Existing PRMs exhibit negative scaling: as the candidate pool size N increases, "
    "performance degrades rather than improves. Qwen2.5-Math-PRM-72B drops from "
    "33.33% (N=8) to 31.33% (N=16) on DABStep, indicating that larger candidate "
    "pools introduce more confusion rather than better selection.",
    title="PRM negative scaling on data analysis",
    metadata={"source_table": "artifacts/2604.24198.pdf, Table 2"}
)

# ── Research questions ────────────────────────────────────────────────────────

q_process_supervision = question(
    "How can we effectively implement step-level process supervision for automated "
    "data analysis tasks, given that existing PRMs designed for mathematical "
    "reasoning fail on this domain?"
)

q_silent_error_detection = question(
    "How can a PRM detect silent errors — logical flaws that produce incorrect "
    "results without triggering interpreter exceptions?"
)

q_grounding_error_distinction = question(
    "How can a PRM distinguish between irrecoverable errors and correctable "
    "exploratory steps (grounding errors) in data analysis?"
)

# ── Connect claims ────────────────────────────────────────────────────────────

# claim_silent_errors and claim_grounding_errors are leaf claims —
# their priors are assigned in priors.py. The settings provide context.

strat_prm_fails = support(
    [claim_silent_errors, claim_grounding_errors],
    claim_prm_fails_on_analysis,
    reason=(
        "General PRMs cannot detect silent errors (@claim_silent_errors) and "
        "penalize grounding errors (@claim_grounding_errors). These two failure "
        "modes compound: silent errors go undetected while correctable errors are "
        "prematurely penalized, resulting in poor trajectory selection on data "
        "analysis benchmarks."
    ),
    prior=0.88,
    background=[setup_prm]
)
