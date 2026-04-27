"""Section 4 — Limitations and critical claims (corresponds to source's
'Limitations' section and the cost analysis in §3.2).

We formalize the three limitations the authors themselves raise — replanning
mechanism simplicity, centralized-planner dependence, resource constraints —
plus the cost-overhead claim and the FN-overconservatism tradeoff that emerges
from the evaluation.
"""

from gaia.lang import claim, setting, support, contradiction

from .motivation import contribution_verimap
from .s2_system import (
    coordinator_replanning,
    planner_generated_vfs,
    structured_io_named_vars,
    strict_and_aggregation,
    executor_can_be_smaller,
)
from .s3_evaluation import (
    obs_accuracy_table_gpt41,
    obs_accuracy_table_other,
    obs_error_table,
    verimap_higher_fn_in_code,
    verimap_lower_fp_than_mapv,
)

# ---------- Settings ----------

cost_setting = setting(
    "API cost per task is computed using vendor-published prices: for "
    "`gpt-4o-mini` the per-1M-token cost is \\$0.15 input, \\$0.08 cached "
    "input, \\$0.60 output; for `gpt-4.1` the per-1M-token cost is \\$2.00 "
    "input, \\$0.50 cached input, \\$8.00 output. Cost is reported as the "
    "average per-task USD cost over the test set.",
    title="API cost model",
    metadata={"figure": "artifacts/2510.17109.pdf, Figure 2 / Figure 9"},
)

# ---------- Observations on cost (Figure 2 / Figure 9) ----------

obs_cost_pattern = claim(
    "The per-task cost distribution across modules is consistent across "
    "all multi-agent variants: the **Executor** is the most expensive "
    "component, followed by the **Verifier**, followed by the "
    "**Planner**. VeriMAP's per-task cost is on the order of \\$0.001 "
    "above MAP-V/MAP, with the gap narrowing on harder benchmarks "
    "(Olympiads) and widening on easier ones (GSM8K).",
    title="Observed cost pattern (Figure 2 / Figure 9)",
    metadata={"figure": "artifacts/2510.17109.pdf, Figure 2 / Figure 9"},
)

obs_iter_table = claim(
    "Average iterations / retries per task (VeriMAP vs MAP-V):\n\n"
    "| Dataset | VeriMAP iter | VeriMAP retry | MAP-V iter | MAP-V retry |\n"
    "|---------|-------------:|--------------:|-----------:|------------:|\n"
    "| MultiHopRAG       | 1.48 | 1.57 | 1.60 | 1.78 |\n"
    "| HumanEval         | 1.33 | 1.71 | 1.05 | 1.09 |\n"
    "| BigCodeBench-Hard | 1.85 | 2.28 | 1.07 | 1.11 |\n"
    "| GSM8K             | 1.17 | 1.14 | 1.09 | 1.35 |\n"
    "| Olympiads         | 1.84 | 2.29 | 1.46 | 1.54 |",
    title="Iteration / retry counts (Table 7)",
    metadata={"source_table": "artifacts/2510.17109.pdf, Table 7"},
)

# ---------- Critical conclusions ----------

cost_overhead_modest = claim(
    "VeriMAP's API-cost overhead over the next-best multi-agent baseline "
    "(MAP-V) is on the order of \\$0.001 per task. The bulk of system "
    "cost goes to the Executor (using `gpt-4o-mini`), so delegating "
    "execution to a smaller model partially offsets the verification and "
    "retry overhead.",
    title="Cost overhead is modest (~$0.001/task)",
)

centralized_planner_dependence = claim(
    "VeriMAP relies on a single centralized planner that dictates task "
    "decomposition, context sharing, and VF generation. System "
    "performance is therefore upper-bounded by planner capability: a "
    "weaker planner produces lower-quality decompositions and VFs, which "
    "the rest of the system cannot compensate for. Empirically, "
    "VeriMAP's MultiHopRAG accuracy drops from 78.20% (gpt-4.1 planner) "
    "to 55.80% (o3 planner) and 64.60% (claude-sonnet-4 planner), "
    "illustrating the dependence.",
    title="Centralized-planner dependence (limitation)",
)

fn_overconservative_tradeoff = claim(
    "VeriMAP's strict-AND aggregation of multiple, often Python-based, "
    "VFs makes it occasionally over-conservative — false-negative rates "
    "jump from 0.68% (MAP-V) to 18.57% (VeriMAP) on HumanEval and from "
    "0.00% to 21.62% on BigCodeBench-Hard. This is a deliberate "
    "structural tradeoff (lower FP at the cost of higher FN) that may "
    "trigger unnecessary retries and replanning in code-heavy domains.",
    title="FP/FN tradeoff is structural (limitation)",
)

# ---------- Strategies ----------

strat_cost_modest = support(
    [obs_cost_pattern, executor_can_be_smaller, obs_iter_table],
    cost_overhead_modest,
    background=[cost_setting],
    reason=(
        "@obs_cost_pattern reports the ~\\$0.001 per-task gap and the "
        "Executor-dominated cost decomposition; @obs_iter_table shows "
        "VeriMAP only modestly inflates per-task iteration counts (e.g., "
        "1.85 vs 1.07 on BCB-H, 1.84 vs 1.46 on Olympiads). Because "
        "VeriMAP can use smaller executors (@executor_can_be_smaller), "
        "the absolute overhead remains modest. The cost model is "
        "@cost_setting."
    ),
    prior=0.9,
)

strat_planner_dependence = support(
    [obs_accuracy_table_gpt41, obs_accuracy_table_other, planner_generated_vfs],
    centralized_planner_dependence,
    reason=(
        "VeriMAP's MultiHopRAG accuracy varies from 78.20% to 55.80% "
        "to 64.60% as the planner LLM changes "
        "(@obs_accuracy_table_gpt41, @obs_accuracy_table_other). Since "
        "the planner is responsible for VF generation "
        "(@planner_generated_vfs), this variability evidences strong "
        "dependence on planner capability."
    ),
    prior=0.9,
)

strat_fn_tradeoff = support(
    [verimap_higher_fn_in_code, verimap_lower_fp_than_mapv, strict_and_aggregation],
    fn_overconservative_tradeoff,
    reason=(
        "The lower-FP / higher-FN pattern (@verimap_lower_fp_than_mapv, "
        "@verimap_higher_fn_in_code) is the predicted consequence of "
        "strict-AND aggregation (@strict_and_aggregation), yielding the "
        "structural tradeoff described in @fn_overconservative_tradeoff."
    ),
    prior=0.9,
)

# ---------- Internal tension: contradiction between two extreme readings ----------

# Contradictory pair we WILL model: cost overhead is modest vs prohibitive.
cost_overhead_prohibitive = claim(
    "VeriMAP's verification, retry, and replanning overhead is "
    "prohibitive for production deployment — the additional API spend "
    "and iteration count outweigh the accuracy benefits.",
    title="Counter-claim: cost overhead is prohibitive",
)

contradiction_cost_modest = contradiction(
    cost_overhead_modest,
    cost_overhead_prohibitive,
    reason=(
        "These two assessments cannot both be true: either the "
        "~\\$0.001/task overhead is acceptable (modest) or it is "
        "prohibitive. The paper's data favors 'modest' (cost analysis "
        "in §3.2)."
    ),
    prior=0.95,
)
