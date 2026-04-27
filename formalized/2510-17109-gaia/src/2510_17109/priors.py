"""Prior assignments for VeriMAP knowledge package."""

from .motivation import (
    agent_failure_modes,
    contribution_verimap,
)
from .s2_system import (
    coordinator_retry,
    nl_vf_definition,
    python_vf_definition,
    strict_and_aggregation,
    structured_io_named_vars,
)
from .s3_evaluation import (
    alt_better_planner_alone,
    alt_replan_explained_by_more_attempts,
    alt_strong_executor,
    obs_accuracy_table_gpt41,
    obs_accuracy_table_other,
    obs_case_study_resolution,
    obs_error_table,
    obs_react_claude_olympiads,
    obs_react_o3_olympiads,
    obs_replan_uplift,
    obs_verimap_bigcode,
    obs_verimap_olympiads,
    obs_vf_stats,
    pred_lower_fp,
    pred_replan_uplift,
    pred_verimap_best,
    pred_vf_adapts,
)
from .s4_critical import (
    cost_overhead_prohibitive,
    obs_cost_pattern,
    obs_iter_table,
)


PRIORS: dict = {
    # ---------- Framing claims (Section 1) ----------
    agent_failure_modes: (
        0.92,
        "Well-attested in MAS literature; the three failure modes (no "
        "result, wrong format, semantic misinterpretation) are widely "
        "documented and the paper exemplifies each.",
    ),
    contribution_verimap: (
        0.55,
        "Thesis statement of the paper. Setting roughly neutral so BP "
        "can update from observations rather than baking the conclusion "
        "into the prior.",
    ),

    # ---------- System definitions (Section 2) ----------
    structured_io_named_vars: (
        0.95,
        "Definitional design choice of the system as described; not in "
        "dispute, only verifiable from the paper itself.",
    ),
    python_vf_definition: (
        0.95,
        "Definitional: a deterministic snippet of Python assertions. "
        "True by construction.",
    ),
    nl_vf_definition: (
        0.92,
        "Definitional + the paper documents the verifier-LLM ReAct "
        "implementation explicitly.",
    ),
    strict_and_aggregation: (
        0.95,
        "Stated explicitly and used uniformly in all experiments.",
    ),
    coordinator_retry: (
        0.95,
        "Algorithmic protocol stated in the paper (Algorithm 1) with "
        "default $R_{\\max}=3$.",
    ),

    # ---------- Predictions (Section 3, before observation) ----------
    # These are theory-side predictions — set neutrally so observations drive belief.
    pred_verimap_best: (
        0.55,
        "Theoretical prediction under the VeriMAP thesis; intentionally "
        "near-neutral so the abduction is driven by the observed table, "
        "not by a baked-in prior.",
    ),
    pred_replan_uplift: (
        0.55,
        "Theoretical prediction under the VeriMAP thesis (replanning "
        "uplift larger for VeriMAP than MAP-V).",
    ),
    pred_vf_adapts: (
        0.6,
        "Theoretical prediction: planner-generated VFs adapt to domain. "
        "Slightly higher than 0.5 because VF-type adaptation is a "
        "natural consequence of any context-aware planner.",
    ),
    pred_lower_fp: (
        0.55,
        "Theoretical prediction: Python VFs + strict-AND yield lower FP "
        "(possibly higher FN) than NL verifiers.",
    ),

    # ---------- Alternative explanations (abduction's Alt) ----------
    # pi(Alt) = 'Can Alt independently explain Obs?', NOT 'Is Alt's calculation correct?'
    alt_strong_executor: (
        0.30,
        "The compute-only alternative cannot explain why ReAct (gpt-4.1) "
        "— a strong-model single agent with the same tools — "
        "underperforms VeriMAP on every dataset, especially on hard "
        "ones. It also cannot explain MAP and MAP-V's poor showings "
        "despite using the same toolset. Low pi(Alt).",
    ),
    alt_replan_explained_by_more_attempts: (
        0.25,
        "The 'more-attempts' alternative cannot explain MAP-V's "
        "near-zero replanning uplift on BCB-H (+0.00) under the same "
        "iteration budget as VeriMAP (+9.46). Low pi(Alt).",
    ),
    alt_better_planner_alone: (
        0.30,
        "The fixed-template alternative cannot explain the 56-fold "
        "swing in Python:NL VF ratios across domains. Low pi(Alt).",
    ),

    # ---------- Observations: empirical leaves (high prior, well-documented data) ----------
    obs_accuracy_table_other: (
        0.92,
        "Reported in Table 2 of the paper; numerical values directly "
        "transcribed.",
    ),
    obs_case_study_resolution: (
        0.90,
        "Reported in Figure 3 of the paper; one specific worked example "
        "with the actual VF code shown.",
    ),
    obs_cost_pattern: (
        0.90,
        "Aggregated from Figures 2 and 9 of the paper.",
    ),
    obs_iter_table: (
        0.92,
        "Reported in Table 7 of the paper.",
    ),
    obs_react_o3_olympiads: (
        0.95,
        "Direct subtraction from Table 2 cells.",
    ),
    obs_react_claude_olympiads: (
        0.95,
        "Direct subtraction from Table 2 cells.",
    ),
    obs_verimap_olympiads: (
        0.95,
        "Direct subtraction from Table 1 cells.",
    ),
    obs_verimap_bigcode: (
        0.95,
        "Direct subtraction from Table 1 cells.",
    ),

    # ---------- Counter-claim used in the cost contradiction operator ----------
    cost_overhead_prohibitive: (
        0.10,
        "Paper's data favors the 'modest' reading; this counter-claim "
        "is included only to make the cost-vs-overhead tension explicit "
        "via the contradiction operator.",
    ),

    # ---------- Observation tables (derived but empirically anchored) ----------
    # These are conclusions of abduction support strategies, but they are
    # directly transcribed from the paper's tables — anchor them empirically
    # so BP doesn't drag them toward the abduction warrant prior.
    obs_accuracy_table_gpt41: (
        0.95,
        "Table 1 of the paper, transcribed verbatim. Direct empirical "
        "observation under the documented experimental setup.",
    ),
    obs_replan_uplift: (
        0.95,
        "Direct subtraction from Table 1 cells (VeriMAP and MAP-V rows, "
        "with-vs-without replanning). No interpretation involved.",
    ),
    obs_vf_stats: (
        0.95,
        "Table 3 of the paper, transcribed verbatim.",
    ),
    obs_error_table: (
        0.95,
        "Table 4 of the paper, transcribed verbatim.",
    ),
}
