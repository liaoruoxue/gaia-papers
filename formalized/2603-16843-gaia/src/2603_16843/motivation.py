"""Section 1: Introduction — Motivation and Problem Statement."""

from gaia.lang import claim, setting, question, support

# ── Settings: background context ─────────────────────────────────────────────

setup_agent = setting(
    "An LLM-based interactive agent operates in an episodic environment $E$ with "
    "horizon $T$. At each step $t$ the environment emits a textual observation "
    "$o_t$ and the policy $\\pi_\\theta$ samples an action $a_t \\sim "
    "\\pi_\\theta(\\cdot | h_t, q)$ where the history $h_t = (o_0, a_0, \\dots, "
    "o_{t-1}, a_{t-1}, o_t)$ and $q$ is the task instruction. A trajectory "
    "$\\tau = (q, o_0, a_0, \\dots, o_T)$ terminates with a verifier-determined "
    "binary success or failure signal.",
    title="LLM agent / interactive episode setup"
)

setup_passk = setting(
    "Pass@K is the capability metric: for each problem, $K$ rollouts are drawn "
    "from the policy and the problem is scored 1 if at least one rollout "
    "succeeds. Pass@K is the dataset average of those binary scores. Pass@1 "
    "measures single-try (deployment-style) accuracy; Pass@K with large $K$ "
    "(e.g. 128, 1024) approximates the model's capability ceiling under "
    "best-of-$K$ sampling [@Yue2025].",
    title="Pass@K capability metric"
)

setup_rlvr = setting(
    "Reinforcement Learning with Verifiable Rewards (RLVR) post-trains an LLM "
    "policy using a programmatic verifier that returns a single scalar reward "
    "for each completed trajectory (e.g. pass/fail or fraction of unit tests "
    "passed). PPO and group-based optimizers such as GRPO [@DeepSeekR1; @Shao2024] "
    "are standard choices. GRPO normalizes rewards within a group of rollouts of "
    "the same problem and updates the policy via a clipped surrogate plus a KL "
    "regularizer to a reference policy.",
    title="RLVR / GRPO post-training"
)

# ── Claims: problem characterization ─────────────────────────────────────────

claim_rich_feedback = claim(
    "Long-horizon interactive environments (web navigation, program synthesis, "
    "embodied tasks) emit rich and structured feedback — invalid actions, state "
    "transitions, compiler/runtime errors — that pinpoints why a trajectory "
    "becomes unproductive and how it could be corrected, going beyond a simple "
    "success/failure signal [@Yang2024; @Shinn2023].",
    title="Environments emit rich diagnostic feedback"
)

claim_rlvr_underuses_feedback = claim(
    "Outcome-driven RLVR (e.g. GRPO) compresses an entire trajectory into a "
    "single terminal scalar reward. Across many rollouts only a small fraction "
    "is rewarded, so updates concentrate on a handful of already-successful "
    "trajectories while most partially-correct failures contribute little direct "
    "signal. The rich step-level diagnostic content of the feedback is therefore "
    "not used to update the policy.",
    title="RLVR underutilizes step-level environment feedback"
)

claim_distribution_sharpening = claim(
    "RLVR with terminal scalar rewards behaves as **distribution sharpening**: "
    "it concentrates probability mass on a small set of behaviors already latent "
    "in the base model's long tail, boosting Pass@1 but yielding limited or even "
    "negative gains at large $K$ (e.g. Pass@1024) — precisely the regime that "
    "reflects the model's true capability ceiling [@Yue2025; @Zhao2025b].",
    title="RLVR causes distribution sharpening (Pass@1 up, Pass@K flat)"
)

claim_agency_internalization = claim(
    "Robust agentic capability requires **agency internalization**: training the "
    "model to interpret structured environment feedback, identify the critical "
    "decision points that induced failure, and revise those decisions in a "
    "feedback-conditioned, targeted manner — rather than relying on blind "
    "retries or external test-time search (e.g. Tree of Thoughts).",
    title="Agency internalization vs distribution sharpening"
)

claim_test_time_cost = claim(
    "Because outcome-driven training fails to internalize recovery, practitioners "
    "rely on expensive test-time computation (multiple retries, "
    "sampling-and-voting, explicit tree search) to escape early mistakes, "
    "increasing both inference latency and deployment complexity "
    "[@Wang2022b; @YaoToT2023; @Fu2025b].",
    title="Test-time sampling cost from missing internalized recovery"
)

# ── Research questions ────────────────────────────────────────────────────────

q_internalize_recovery = question(
    "How can an agentic LLM be trained so that feedback-grounded recovery "
    "(detecting when a trajectory is failing and revising decisions accordingly) "
    "becomes an intrinsic capability of the model — improving Pass@K rather than "
    "merely sharpening the existing distribution?"
)

# ── Connect claims (Pass 2 connectives) ──────────────────────────────────────

# Distribution sharpening is the consequence of underusing feedback
strat_sharpening_from_underuse = support(
    [claim_rlvr_underuses_feedback],
    claim_distribution_sharpening,
    reason=(
        "Because RLVR only updates on terminal scalar rewards and the rewarded "
        "fraction is small (@claim_rlvr_underuses_feedback), gradient updates "
        "are dominated by the few rewarded trajectories that lie within the "
        "base model's existing solution support. The policy reweights toward "
        "this narrow set rather than discovering new behaviors, manifesting as "
        "the Pass@1-up / Pass@K-flat distribution-sharpening pattern "
        "[@Yue2025; @Zhao2025b]."
    ),
    prior=0.85,
    background=[setup_rlvr, setup_passk]
)

# Test-time cost arises when recovery is not internalized
strat_test_time_cost_from_sharpening = support(
    [claim_distribution_sharpening],
    claim_test_time_cost,
    reason=(
        "If RLVR only sharpens the existing distribution (@claim_distribution_sharpening), "
        "the trained policy still cannot recover from early mistakes within a "
        "single rollout. Practitioners must therefore deploy expensive test-time "
        "branching (best-of-$K$ sampling, MCTS, ToT) to escape failure modes "
        "[@Wang2022b; @YaoToT2023]."
    ),
    prior=0.80
)

# Note: sharpening and internalization are not formal contradictions — they
# can co-occur (a recipe could partially sharpen and partially internalize).
# The paper's claim is the comparative one that GRPO produces predominantly
# sharpening and LEAFE produces internalization. Flagged in the Critical
# Analysis as an unmodeled tension rather than a hard contradiction.
