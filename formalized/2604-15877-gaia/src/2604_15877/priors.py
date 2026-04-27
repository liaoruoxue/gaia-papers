"""Prior assignments for independent (leaf) claims in this package."""

from . import (
    # Citation analysis observations
    obs_total_references,
    obs_memory_to_skill_citation,
    obs_skill_to_memory_citation,
    obs_skill_surveys_no_memory,
    obs_memory_survey_only_voyager,
    # Spectrum properties
    shared_problem,
    storage_cost_calculation,
    # System mapping observations
    obs_l1_systems,
    obs_l2_systems,
    obs_cross_level_systems,
    obs_l3_empty,
    obs_skillsbench_selfgen,
    # Cross-level performance benchmarks (used as inductive observations)
    obs_skillrl_l2_vs_l1,
    obs_trace2skill_l2_vs_human,
    obs_trace2skill_l2_vs_none,
    obs_skillsbench_curated,
    obs_evoskill_l2_vs_none,
    # Cross-system insights
    framing_limitation,
    scalability_bottleneck,
    shared_subproblems,
    deployment_needs_both,
    evaluation_level_coupling,
    obs_trace2skill_size_transfer,
    obs_merge_swing,
    # Predictions and open problems
    prediction_l2_beats_l1_transfer,
    prediction_multilevel_better,
    prediction_concave_curve,
    prediction_l3_constraints,
    problem_adaptive_selection,
    diagonal_architecture,
)

PRIORS = {
    # --- Citation analysis (direct empirical counts) ---
    obs_total_references: (
        0.95,
        "Direct count from the paper's Abstract and Section 1: 1,136 references "
        "across 22 primary papers. High confidence as an explicitly reported "
        "bibliometric measurement.",
    ),
    obs_memory_to_skill_citation: (
        0.93,
        "Direct numerator/denominator (4/566 = 0.7%) reported in Section 1. "
        "Mechanical citation count, high confidence.",
    ),
    obs_skill_to_memory_citation: (
        0.93,
        "Direct numerator/denominator (7/570 = 1.2%) reported in Section 1. "
        "Mechanical citation count, high confidence.",
    ),
    obs_skill_surveys_no_memory: (
        0.9,
        "Direct review of two skill surveys (Jiang et al. 2026; Xu and Yan 2026) "
        "for any memory-system citation. High confidence as a verifiable claim "
        "about a small finite set of citations.",
    ),
    obs_memory_survey_only_voyager: (
        0.88,
        "Direct review of memory surveys; only one (Yang et al. 2026a) cites a "
        "skill system, restricted to Voyager. High confidence; slight uncertainty "
        "because survey selection may not be exhaustive.",
    ),

    # --- Core unifying observation ---
    shared_problem: (
        0.85,
        "Conceptual reframing of memory and skill systems as instances of "
        "compression at different granularities. High plausibility as a "
        "theoretical lens, but the equivalence is conceptual rather than "
        "formally proved; some practitioners may dispute that memory and skill "
        "extraction are the 'same operation'.",
    ),

    # --- Storage estimate ---
    storage_cost_calculation: (
        0.88,
        "Order-of-magnitude calculation: 1,000 episodes x 500 tokens = 500K; "
        "compressed to 5K (skills) and 500 (rules) tokens. The arithmetic is "
        "trivially correct; uncertainty is in the per-episode token estimate "
        "(~500 tokens) which may vary by domain.",
    ),

    # --- Mapping observations ---
    obs_l1_systems: (
        0.9,
        "Direct count from Table 2: ten Level-1 systems are listed with diverse "
        "mechanisms but converging output format. High confidence as a "
        "verifiable enumeration; slight uncertainty for borderline cases.",
    ),
    obs_l2_systems: (
        0.9,
        "Direct count from Table 2: eight Level-2 systems are listed. High "
        "confidence as a verifiable enumeration.",
    ),
    obs_cross_level_systems: (
        0.9,
        "Direct identification of ExpeL and AutoAgent as cross-level systems "
        "in Table 2; the 'fixed levels, no adaptive selection' characterization "
        "is supported by inspection of each system's documentation.",
    ),
    obs_l3_empty: (
        0.85,
        "Survey-level claim that no surveyed system automates Level-3 rule "
        "extraction. High confidence within the survey scope; slight uncertainty "
        "because the field is broad and a system might be missing from the "
        "survey (e.g., the Q1 2026 snapshot caveat).",
    ),
    obs_skillsbench_selfgen: (
        0.93,
        "Direct measurement from SkillsBench Table 1: LLM-self-generated skills "
        "yield +0.0pp. High confidence as a reported benchmark result.",
    ),

    # --- Cross-level performance benchmarks ---
    # These observations are conclusions of generative-direction support
    # strategies inside the higher-compression-better induction. They are
    # anchored with high priors here because they are direct empirical
    # measurements; without these anchors the induction's law belief would
    # default to 0.5 (no observational grounding).
    obs_skillrl_l2_vs_l1: (
        0.93,
        "Direct measurement from SkillRL Table 1: +68.5pp L2-skills vs. L1-trajectory "
        "retrieval on ALFWorld. High confidence as a reported benchmark result.",
    ),
    obs_trace2skill_l2_vs_human: (
        0.93,
        "Direct measurement from Trace2Skill Table 1: +21.5pp L2 vs. human-written "
        "skills on SpreadsheetBench.",
    ),
    obs_trace2skill_l2_vs_none: (
        0.93,
        "Direct measurement from Trace2Skill Table 1: +42.1pp L2 vs. no skill on "
        "SpreadsheetBench.",
    ),
    obs_skillsbench_curated: (
        0.92,
        "Direct measurement from SkillsBench Table 1: +16.2pp curated L2 vs. no skill on "
        "multi-task evaluation.",
    ),
    obs_evoskill_l2_vs_none: (
        0.9,
        "Direct measurement from EvoSkill Table 1: +5.3% L2 vs. no skill on "
        "BrowseComp. Smaller magnitude but consistent direction.",
    ),

    # --- Independent insight claims ---
    framing_limitation: (
        0.8,
        "Interpretive claim about why the missing diagonal exists (problem framing "
        "rather than missing engineering). Plausible but not directly testable; "
        "moderate-high prior reflecting reasonable inference from the survey "
        "data without independent confirmation.",
    ),
    scalability_bottleneck: (
        0.85,
        "Quantitative scalability argument: linear cost growth in L1-only systems. "
        "The mathematical reasoning is straightforward; uncertainty is in whether "
        "real systems hit this bottleneck in practice (production deployments may "
        "use other mitigations like sharding).",
    ),
    shared_subproblems: (
        0.83,
        "Claim that both communities solve identical sub-problems (retrieval, "
        "conflict detection, staleness, evaluation). Verifiable by inspection of "
        "the surveyed papers; high confidence in the qualitative claim, slight "
        "uncertainty in 'identical' being literally true.",
    ),
    deployment_needs_both: (
        0.85,
        "Pragmatic claim about real deployment requirements (personalization + "
        "capability). Strongly supported by industry experience but not a "
        "controlled empirical result.",
    ),
    evaluation_level_coupling: (
        0.88,
        "Direct observation about current evaluation practice (L1 = QA metrics, "
        "L2 = task success, L3 = no methodology). Verifiable from the surveyed "
        "literature; high confidence.",
    ),

    # --- Empirical observations supporting transferability ---
    obs_trace2skill_size_transfer: (
        0.9,
        "Direct measurement from Trace2Skill (Ni et al. 2026): +57.7pp from 35B "
        "to 122B model transfer. High confidence as a reported benchmark result.",
    ),

    # --- Lifecycle observation ---
    obs_merge_swing: (
        0.85,
        "Direct measurement from Trace2Skill: +/-21pp performance swings during "
        "skill merging with success-trace signals. High confidence as a reported "
        "finding; slight uncertainty in generalization beyond Trace2Skill's "
        "specific setup.",
    ),

    # --- Testable predictions (forward-looking, untested) ---
    prediction_l2_beats_l1_transfer: (
        0.65,
        "Forward-looking prediction not yet validated by a controlled experiment. "
        "Consistent with within-study evidence (SkillRL +68.5pp on ALFWorld) but "
        "the controlled cross-domain transfer experiment has not been run.",
    ),
    prediction_multilevel_better: (
        0.6,
        "Forward-looking prediction about long-horizon multi-level systems. "
        "No system supports adaptive multi-level storage to date; prediction is "
        "well-motivated but speculative.",
    ),
    prediction_concave_curve: (
        0.5,
        "Forward-looking prediction about transferability-vs-specificity curve "
        "shape. Direction (monotonic for L0->L2) supported by data, but the "
        "L2 sweet-spot conjecture has not been tested. Moderate prior reflecting "
        "high uncertainty about the specific functional form.",
    ),
    prediction_l3_constraints: (
        0.7,
        "Forward-looking prediction about L3 framing (guardrails > directives). "
        "Supported by the early RuleShaping evidence (+7-14pp from constraints). "
        "Higher prior than other predictions because partial empirical "
        "confirmation already exists.",
    ),

    # --- Open problems and architecture (proposals, not assertions) ---
    problem_adaptive_selection: (
        0.7,
        "Statement that adaptive level selection is an open problem requiring a "
        "value-of-information meta-controller. Well-motivated by the missing "
        "diagonal, but the framing involves specific design choices "
        "(joint-vs-fixed optimization) that are themselves debatable.",
    ),
    diagonal_architecture: (
        0.6,
        "Specific three-component architecture proposal (meta-controller, "
        "promotion/demotion engine, lifecycle manager). Concrete and "
        "implementable using existing building blocks, but no working "
        "implementation exists; many architectural choices remain open.",
    ),
}
