"""Section 5.2: Graph Disambiguation — Joint Beliefs and Correlated Updates (Experiment 2)"""

from gaia.lang import claim, setting, support, abduction, compare

from .motivation import dc_framework_proposed, implicit_control_problem
from .s3_framework import multi_signal_def, joint_signal_value, correlated_belief_update

# ─── Settings ─────────────────────────────────────────────────────────────────

graph_setup = setting(
    "Graph disambiguation experiment: a synthetic knowledge graph with 200 nodes (people), "
    "each described by five categorical attributes: department \\in {Engineering, Marketing, "
    "Sales, Finance}, role \\in {Manager, Analyst, Engineer, Lead}, location \\in {New York, "
    "London, Tokyo, Berlin}, project \\in {Alpha, Beta, Gamma, Delta}, level \\in {L1, L2, L3, "
    "L4}. Edges connect pairs sharing >= 2 attributes; 15% noisy edges added (sharing <= 1 "
    "attribute). Given a partial description, the system identifies the target node by "
    "interleaving three actions: clarify (ask for a missing attribute), execute (visit a "
    "candidate), and backtrack (reject current candidate). Five scenarios: S1 (clean "
    "baseline), S2 (ambiguous, $\\hat{p}_{\\text{suff}}$ only), S3 (unreliable, "
    "$\\hat{p}_{\\text{corr}}$ only), S4 (orthogonal joint belief), S5 (correlated coupled "
    "update). $N=20$ runs per scenario [@Sun2026].",
    title="Graph disambiguation experiment setup",
)

graph_dc_signals = setting(
    "DC signals for graph disambiguation: sufficiency $\\hat{p}_{\\text{suff}} = "
    "1/|\\text{candidates}|$ (increases as candidate set shrinks via clarification or "
    "elimination after failed traversal). Correctness $\\hat{p}_{\\text{corr}}$ estimated "
    "after each visit: for each hidden attribute $k$, compute fraction of active peer "
    "candidates sharing the visited node's value; average over hidden attributes; penalize "
    "similarity to prior rejections by subtracting 0.15–0.35 if >= 50% hidden attribute "
    "match to previously rejected node; clamp to $[0.05, 0.95]$. Thresholds: "
    "$\\tau_{\\text{suff}} = 0.4$, $\\theta_{\\text{corr}} = 0.5$ [@Sun2026].",
    title="DC signal definitions for graph disambiguation",
)

# ─── Experimental results ─────────────────────────────────────────────────────

dc_graph_100pct = claim(
    "The decision-centric (DC) approach achieves 100% success across all five graph "
    "disambiguation scenarios (S1–S5), while baselines degrade: Retry drops to 45% (S2) "
    "and 60% (S5); Prompt reaches 85% (S2) and 35% (S5); Prompt (w/ policy) reaches 95% "
    "(S2) but also only 35% (S5) [@Sun2026].",
    title="DC achieves 100% success across all 5 graph scenarios",
    background=[graph_setup, graph_dc_signals],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 4",
        "caption": "Table 4: Graph disambiguation success rates.",
    },
)

s2_sufficiency_isolation = claim(
    "In scenario S2 (ambiguous, $\\hat{p}_{\\text{suff}}$ only: 13 candidates, 2 known "
    "attributes), DC achieves 100% by clarifying until the candidate pool is small enough "
    "to act on. Retry drops to 45% by executing blindly. Prompt-Clarify reaches 85%, "
    "occasionally acting too early without explicit sufficiency tracking. Prompt (w/ policy) "
    "improves to 95%, indicating that policy prose helps when the correct action can be read "
    "directly from the observable candidate count [@Sun2026].",
    title="S2 isolates sufficiency signal: DC 100% vs Retry 45% vs Prompt 85%",
    background=[graph_setup],
)

s5_correlated_update_result = claim(
    "In scenario S5 (correlated coupled update: 12 initial candidates, 3 known attributes, "
    "forced first execution to decoy D), DC achieves 100% success by updating its belief "
    "state when decoy D's traversal eliminates node E (which shares level=L1, a minority "
    "value), reducing candidates from 5 to 3 and raising $\\hat{p}_{\\text{suff}}$ from "
    "0.200 to 0.333 without any additional clarification turn. Prompt and Prompt (w/ policy) "
    "both achieve only 35% success, even below Retry at 60%, because the updated candidate "
    "state is not available to the LLM at decision time [@Sun2026].",
    title="S5 correlated update: DC 100% vs Prompt 35% — state not available to LLM",
    background=[graph_setup, graph_dc_signals],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 10",
        "caption": "Table 10: Full graph disambiguation results, N=20, structural p_corr estimator.",
    },
)

prompt_policy_insufficient_for_s5 = claim(
    "In scenario S5, embedding the decision policy in the system prompt (Prompt w/ policy) "
    "does not recover the performance gap versus DC: both Prompt and Prompt (w/ policy) "
    "remain at 35% success, even below the Retry baseline at 60%. The bottleneck is not "
    "deciding how to act given observable state, but the absence of the updated belief "
    "state — the effective candidate set has already changed during traversal (from 5 to 3) "
    "and that state update is not available to the LLM at decision time [@Sun2026].",
    title="Policy-in-prompt fails for S5: missing belief state update is the bottleneck",
    background=[graph_setup],
)

# ─── Prediction claims for abduction ─────────────────────────────────────────

dc_predicts_s5_success = claim(
    "The decision-centric framework predicts success in scenario S5 because it maintains "
    "and updates the belief state $\\hat{p}_{\\text{suff}}$ explicitly after each action: "
    "when decoy D (level=L1) fails and eliminates node E (also level=L1), the candidate "
    "count drops from 5 to 3 and $\\hat{p}_{\\text{suff}}$ rises from 0.200 to 0.333 "
    "at $t=2$, enabling the correct backtrack-and-search policy thereafter [@Sun2026].",
    title="DC predicts S5 success via explicit correlated belief state update",
    background=[graph_dc_signals, correlated_belief_update],
)

prompt_predicts_s5_failure = claim(
    "Prompt-based approaches (including Prompt w/ policy) predict failure in scenario S5 "
    "because their decision-relevant state (candidate set size after elimination) is not "
    "exposed at decision time. The LLM must infer the action from a state snapshot that "
    "does not include the implicit elimination that occurred during traversal [@Sun2026].",
    title="Prompt-based approach predicts S5 failure due to unobserved state change",
    background=[implicit_control_problem],
)

# ─── Abduction: DC vs Prompt on S5 ───────────────────────────────────────────

s_dc_s5 = support(
    [dc_predicts_s5_success],
    s5_correlated_update_result,
    reason=(
        "DC's prediction of success in S5 (@dc_predicts_s5_success) requires only that the "
        "explicit belief state be maintained and updated after each action, which is guaranteed "
        "by the architecture. The observed 100% DC success in S5 is fully consistent with "
        "this prediction [@Sun2026]."
    ),
    prior=0.92,
)

s_prompt_s5 = support(
    [prompt_predicts_s5_failure],
    s5_correlated_update_result,
    reason=(
        "The prompt-based prediction of failure (@prompt_predicts_s5_failure) is consistent "
        "with both Prompt (35%) and Prompt (w/ policy) (35%) results. However, this prediction "
        "cannot explain DC's 100% success, since both approaches receive the same state payload "
        "— the difference is purely architectural [@Sun2026]."
    ),
    prior=0.45,
)

comp_s5 = compare(
    dc_predicts_s5_success,
    prompt_predicts_s5_failure,
    s5_correlated_update_result,
    reason=(
        "DC's prediction (@dc_predicts_s5_success) matches the S5 outcome (100% DC success), "
        "while the prompt-based prediction (@prompt_predicts_s5_failure) only explains the "
        "prompt baselines' 35% but not DC's 100%. The 65 percentage-point gap between DC "
        "and the prompt approaches (both receiving identical state payloads) provides strong "
        "differentiation in favor of explicit belief state maintenance [@Sun2026]."
    ),
    prior=0.9,
)

abduction_s5 = abduction(
    s_dc_s5,
    s_prompt_s5,
    comp_s5,
    reason=(
        "Both DC and prompt-based approaches attempt to explain the S5 correlated belief "
        "update scenario outcome. The abduction tests whether explicit belief state "
        "maintenance (DC) or implicit prompt-based state reasoning is the better explanation "
        "for the observed success rates [@Sun2026]."
    ),
)

# ─── Supporting reasoning ─────────────────────────────────────────────────────

strat_joint_signals_needed = support(
    [joint_signal_value],
    dc_graph_100pct,
    reason=(
        "The joint signal value claim (@joint_signal_value) establishes that optimal action "
        "in multi-signal settings depends on the joint state $(\\hat{p}_{\\text{suff}}, "
        "\\hat{p}_{\\text{corr}})$. The graph DC implementation makes "
        "both signals explicit and updates them after each action. S4 demonstrates the "
        "joint dependence: same low $\\hat{p}_{\\text{corr}}$ produces 'backtrack' in S3 "
        "(high $\\hat{p}_{\\text{suff}}$) and 'clarify' in S4 (low $\\hat{p}_{\\text{suff}}$), "
        "while only DC tracks this joint state to achieve 100% across all scenarios "
        "[@Sun2026]."
    ),
    prior=0.88,
    background=[graph_dc_signals],
)
