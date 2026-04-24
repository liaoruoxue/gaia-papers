"""Pass 2 — Reasoning strategies connecting all claims"""

from gaia.lang import (
    support, deduction, abduction, induction, composite,
    contradiction, complement,
    compare,
)

from .motivation import (
    cua_task_model,
    verifier_formal_def,
    cua_trajectories_hard_to_verify,
    verifier_errors_compound,
    four_principles_sufficient,
    existing_verifiers_inadequate,
    gains_are_architectural,
    auto_research_70pct,
    human_expert_complementary_to_auto,
)
from .s3_principles import (
    process_score_formula,
    relevance_matrix_def,
    rubric_quality_critical,
    phantom_criteria_failure,
    cascading_criteria_failure,
    separate_generation_scoring,
    conditional_criteria_design,
    two_pass_hallucination_detection,
    process_outcome_separation,
    process_outcome_diverge_on_blockers,
    outcome_label_primary_intent,
    controllable_vs_uncontrollable,
    cascading_error_free_scoring,
    screenshot_needle_in_haystack,
    relevance_matrix_approach,
    unsolicited_side_effects,
)
from .s4_system import (
    uv_algorithm_overview,
    uv_design_invariant,
    uv_incorporates_all_principles,
    uv_richer_output,
    verifier_needs_all_screenshots,
    screenshot_staircase_pattern,
)
from .s5_experiments import (
    cuaverifierbench_novel,
    uv_as_annotator,
    iterative_development_requires_benchmark,
    internal_dataset_setting,
    browserbase_dataset_setting,
    auto_research_setup,
)
from .s6_results import (
    uv_outcome_kappa_internal,
    uv_outcome_kappa_browserbase,
    uv_process_kappa_internal,
    uv_fpr_near_zero,
    alt_fpr_reduction_is_model,
    uv_matches_human_interannotator,
    upgrading_backbone_insufficient,
    uv_reasoning_improves_human_labels,
    rubric_score_correlation,
    process_more_subjective_than_outcome,
    native_verifiers_overcount_success,
    agentrewardbench_fpr,
    auto_research_from_blank_result,
    auto_research_conservative,
    auto_research_cont_expert_result,
    auto_research_stochastic_variance,
    gpt52_lowest_fpr,
    fixed_rubric_ablation,
)

# ============================================================
# Motivation layer strategies
# ============================================================

strat_verifier_errors_matter = support(
    [cua_trajectories_hard_to_verify],
    verifier_errors_compound,
    reason=(
        "Because @cua_trajectories_hard_to_verify — trajectories are long, visually rich, "
        "and ambiguous — verification errors are easy to make and hard to detect. "
        "When errors propagate into benchmark scores and RL training signals, "
        "both evaluation quality and training quality are compromised."
    ),
    prior=0.9,
)

strat_principles_address_problem = support(
    [cua_trajectories_hard_to_verify, verifier_errors_compound],
    four_principles_sufficient,
    reason=(
        "The four principles directly address the sources of verification difficulty "
        "identified in @cua_trajectories_hard_to_verify and @verifier_errors_compound: "
        "(1) non-overlapping rubric criteria reduce annotation noise from ambiguity; "
        "(2) process/outcome separation captures the environment's role; "
        "(3) controllable/uncontrollable distinction prevents unfair penalization; "
        "(4) divide-and-conquer screenshot management attends to all evidence without "
        "context window overload. The claim is validated empirically in Section 6."
    ),
    prior=0.85,
)

# ============================================================
# Principle 1 — Rubric design strategies
# ============================================================

strat_phantom_criteria = support(
    [rubric_quality_critical],
    phantom_criteria_failure,
    reason=(
        "Since rubric quality is critical (@rubric_quality_critical) and LLM-generated "
        "rubrics are the root of the pipeline, LLMs tend to hallucinate requirements "
        "beyond the actual task (phantom criteria). The evidence in Table 4 shows "
        "concrete examples: a task asking to find a Spotify song received phantom criteria "
        "for Spotify URLs and event links, turning a SUCCESS into FAILURE."
    ),
    prior=0.9,
)

strat_cascading = support(
    [rubric_quality_critical],
    cascading_criteria_failure,
    reason=(
        "Because @rubric_quality_critical — rubric errors cascade downstream — when "
        "criteria are logically dependent, a single upstream scoring error propagates "
        "to all downstream criteria that depend on it, multiplying the penalty. "
        "Figure 4 shows a concrete case: a computational error in identifying the "
        "longest last name propagated, though in that case the UV's cascading-error-free "
        "design prevented it from affecting the last criterion."
    ),
    prior=0.85,
)

strat_separate_gen_scoring = support(
    [rubric_quality_critical],
    separate_generation_scoring,
    reason=(
        "Empirical evidence during iterative development (@rubric_quality_critical) "
        "showed that combined generation+scoring led the LLM to create criteria tailored "
        "to what it saw the agent do, not what the task required. Separating generation "
        "(task only, no trajectory) from scoring eliminates this confirmation bias. "
        "This was identified as contributing roughly half of the Cohen's kappa gains."
    ),
    prior=0.88,
)

strat_conditional_criteria = support(
    [rubric_quality_critical],
    conditional_criteria_design,
    reason=(
        "Good rubric design (@rubric_quality_critical) requires that criteria reflect "
        "only achievable sub-goals. The process score formula sums only over applicable "
        "criteria $\\mathcal{A}$; conditional criteria implement this by being excluded "
        "from $\\mathcal{A}$ when their condition is not met (e.g., no direct flight exists). "
        "Table 5 shows a concrete example: the window-seat cost criterion is excluded "
        "when no direct flights are available."
    ),
    prior=0.9,
    background=[process_score_formula],
)

strat_two_pass = support(
    [uv_design_invariant],
    two_pass_hallucination_detection,
    reason=(
        "The UV design invariant (@uv_design_invariant) requires no relevant screenshot "
        "evidence to go undetected. Two-pass scoring (text-action-only first, then "
        "screenshot-grounded) operationalizes this by flagging discrepancies where the "
        "agent's claimed actions are not supported by visual evidence — surfacing "
        "hallucinations that a single-pass scorer would miss (Figure 5: '+6.2% CIDEr' "
        "vs '+2.8% CIDEr' in actual screenshot)."
    ),
    prior=0.88,
)

# ============================================================
# Principle 2 — Process/Outcome separation strategies
# ============================================================

strat_process_outcome_sep = support(
    [controllable_vs_uncontrollable],
    process_outcome_separation,
    reason=(
        "Because the environment controls certain outcomes that the agent cannot "
        "(@controllable_vs_uncontrollable), conflating 'did the agent execute well' "
        "with 'did the user's goal succeed' yields unfair signals. Process score "
        "evaluates the agent's controllable actions; outcome evaluates the final state "
        "regardless of cause. The process formula (defined in @process_score_formula) "
        "supports this by operating only on applicable criteria."
    ),
    prior=0.9,
    background=[process_score_formula],
)

strat_diverge_on_blockers = deduction(
    [process_outcome_separation, controllable_vs_uncontrollable],
    process_outcome_diverge_on_blockers,
    reason=(
        "Given that @process_outcome_separation decouples execution quality from goal "
        "achievement, and that @controllable_vs_uncontrollable classifies environment "
        "blockers as uncontrollable factors not penalized in process: it necessarily "
        "follows that an agent blocked by an environment factor receives full process "
        "credit (correct behavior given circumstances) but outcome failure (goal not met). "
        "This is a direct logical consequence of the separation."
    ),
    prior=0.98,
)

strat_primary_intent = support(
    [process_outcome_separation],
    outcome_label_primary_intent,
    reason=(
        "Since outcome focuses on whether the user's goal was achieved "
        "(@process_outcome_separation), and users have primary intent vs. flexible "
        "secondary preferences, the outcome label should focus on primary intent. "
        "This is grounded in the design choice that users are forgiving of minor "
        "format variations but not unsolicited actions or fabrications."
    ),
    prior=0.82,
)

# ============================================================
# Principle 3 — Controllable/Uncontrollable strategies
# ============================================================

strat_cascading_error_free = deduction(
    [controllable_vs_uncontrollable],
    cascading_error_free_scoring,
    reason=(
        "Given the taxonomy in @controllable_vs_uncontrollable (agents should only "
        "be penalized for controllable factors), a cascading-error-free rubric is the "
        "direct implementation: each criterion is evaluated based on what the agent "
        "could control at that step, not what upstream criteria concluded. "
        "This follows necessarily from the controllable/uncontrollable distinction."
    ),
    prior=0.95,
)

# ============================================================
# Principle 4 — Context management strategies
# ============================================================

strat_relevance_matrix = support(
    [screenshot_needle_in_haystack, verifier_needs_all_screenshots],
    relevance_matrix_approach,
    reason=(
        "Given that naive approaches fail (@screenshot_needle_in_haystack: overload "
        "or missing evidence) and that reliable verification requires all screenshots "
        "(@verifier_needs_all_screenshots), the per-criterion relevance matrix approach "
        "solves both problems: it attends to all $T+1$ screenshots (computing "
        "$\\mathbf{R} \\in \\mathbb{R}^{(T+1) \\times N}$) while focusing the analysis "
        "context on the most relevant screenshots per criterion, making it scalable "
        "and complete."
    ),
    prior=0.88,
    background=[relevance_matrix_def],
)

# ============================================================
# System integration strategies
# ============================================================

# Use composite to avoid 4-premise conjunction suppressing belief
# Intermediate: UV implements the three main principles (rubric, P/O sep, controllable)
from .s4_system import uv_incorporates_all_principles as _uv_full
from .s3_principles import rubric_quality_critical as _rqc

# Sub-strategy 1: UV implements rubric + process/outcome principles
_sub1 = support(
    [rubric_quality_critical, process_outcome_separation],
    uv_incorporates_all_principles,
    reason=(
        "The UV implements non-overlapping rubric criteria (@rubric_quality_critical) "
        "via separate generation+scoring stages, and implements process/outcome separation "
        "(@process_outcome_separation) via distinct scoring passes (Steps 6-7 of Algorithm 1)."
    ),
    prior=0.92,
    background=[uv_algorithm_overview],
)

# Sub-strategy 2: UV also implements controllable/uncontrollable + relevance matrix
_sub2 = support(
    [controllable_vs_uncontrollable, relevance_matrix_approach],
    uv_incorporates_all_principles,
    reason=(
        "The UV further implements controllable vs. uncontrollable distinction "
        "(@controllable_vs_uncontrollable) via rubric criteria description fields, "
        "and implements the per-criterion relevance matrix approach "
        "(@relevance_matrix_approach) via Steps 2-4 of Algorithm 1."
    ),
    prior=0.92,
    background=[uv_algorithm_overview],
)

strat_uv_incorporates = composite(
    [rubric_quality_critical, process_outcome_separation,
     controllable_vs_uncontrollable, relevance_matrix_approach],
    uv_incorporates_all_principles,
    sub_strategies=[_sub1, _sub2],
    reason=(
        "The Universal Verifier (Algorithm 1) directly implements all four design principles: "
        "rubric quality (@rubric_quality_critical), process/outcome separation "
        "(@process_outcome_separation), controllable/uncontrollable distinction "
        "(@controllable_vs_uncontrollable), and relevance matrix context management "
        "(@relevance_matrix_approach). Each principle maps directly to one or more algorithm steps."
    ),
    background=[uv_algorithm_overview],
)

strat_uv_richer_output = deduction(
    [process_outcome_separation, controllable_vs_uncontrollable],
    uv_richer_output,
    reason=(
        "Given @process_outcome_separation (two independent signals) and @controllable_vs_uncontrollable "
        "(failure categorization), the UV output is necessarily richer than binary: "
        "it must produce both $r_{\\text{proc}}$ and $r_{\\text{out}}$, plus the diagnostic "
        "report $d$ from the error taxonomy. These follow directly from the design principles."
    ),
    prior=0.97,
    background=[uv_algorithm_overview],
)

strat_uv_design_invariant = support(
    [two_pass_hallucination_detection, relevance_matrix_approach],
    uv_design_invariant,
    reason=(
        "The design invariant of detecting all relevant screenshot evidence is "
        "operationalized by two mechanisms: @two_pass_hallucination_detection flags "
        "discrepancies between text-only and screenshot-grounded scoring, and "
        "@relevance_matrix_approach ensures every screenshot is scored against every "
        "criterion before filtering. Together these guarantee no hallucination-revealing "
        "evidence is missed, as demonstrated by the Figure 5 example (+2.8% vs +6.2% CIDEr)."
    ),
    prior=0.88,
)

strat_benchmark_requires_verifier = support(
    [verifier_errors_compound],
    iterative_development_requires_benchmark,
    reason=(
        "Because @verifier_errors_compound — verifier errors corrupt evaluation and training — "
        "an iterative verifier development process requires a reliable evaluation benchmark "
        "to know if proposed changes improve or harm agreement. Without CUAVerifierBench, "
        "verifier changes cannot be measured, and the iterative loop breaks down."
    ),
    prior=0.9,
)

# ============================================================
# Main result strategies — Abduction for architecture claim
# ============================================================

# UV vs. existing verifiers: abduction that the advantage is architectural
# Observation: upgrading_backbone_insufficient — upgrading baseline to GPT-5.2 fails to replicate UV gains
# Hypothesis H: the UV's advantage is architectural (not model-driven)
# Alternative: the advantage is due to the stronger LLM

s_architectural = support(
    [uv_incorporates_all_principles],
    upgrading_backbone_insufficient,
    reason=(
        "The architectural design (@uv_incorporates_all_principles) predicts that "
        "replacing the UV's architecture with baseline pipelines (WebVoyager/WebJudge) "
        "will fail to replicate the UV's gains even with the same backbone LLM: "
        "the pipeline differences (rubric generation, two-pass scoring, per-criterion "
        "screenshot selection) are responsible for the low FPR and high kappa. "
        "Therefore upgrading baselines to GPT-5.2 should still underperform."
    ),
    prior=0.87,
)

s_model_alt = support(
    [alt_fpr_reduction_is_model],
    upgrading_backbone_insufficient,
    reason=(
        "If the UV's advantage were purely due to GPT-5.2 (@alt_fpr_reduction_is_model), "
        "upgrading WebVoyager/WebJudge to GPT-5.2 should close most of the gap. "
        "This alternative predicts that backbone upgrades should yield substantial "
        "kappa improvement to near UV levels — which would make @upgrading_backbone_insufficient false."
    ),
    prior=0.3,
)

comp_architectural = compare(
    uv_incorporates_all_principles,
    alt_fpr_reduction_is_model,
    upgrading_backbone_insufficient,
    reason=(
        "Upgrading WebVoyager to GPT-5.2 reduces outcome FPR from 0.45 to 0.10 "
        "but simultaneously increases FNR from 0.24 to 0.44, and kappa only improves "
        "from 0.31 to 0.43 — well below UV's 0.64. This confirms the architectural "
        "explanation: the baseline pipeline's missing components (rubric generation, "
        "two-pass scoring) cannot be compensated by a stronger model alone."
    ),
    prior=0.9,
)

abduction_architecture = abduction(
    s_architectural,
    s_model_alt,
    comp_architectural,
    reason=(
        "Both hypotheses (architectural design vs. stronger LLM) attempt to explain "
        "why baseline verifiers with GPT-5.2 still underperform the UV. "
        "The direct backbone upgrade experiment directly tests the model-only alternative."
    ),
)

# ============================================================
# UV matches human agreement — induction over two datasets
# ============================================================

s_internal = support(
    [uv_matches_human_interannotator],
    uv_outcome_kappa_internal,
    reason=(
        "The law @uv_matches_human_interannotator — that the UV agrees with humans as well "
        "as humans agree with each other — predicts that on any well-annotated dataset, "
        "the UV's kappa will fall within the human inter-annotator range. On the internal "
        "dataset ($n=140$), this predicts $\\kappa \\approx 0.6$, confirmed at $\\kappa = 0.64$."
    ),
    prior=0.85,
)

s_browserbase = support(
    [uv_matches_human_interannotator],
    uv_outcome_kappa_browserbase,
    reason=(
        "The same law @uv_matches_human_interannotator predicts that the UV's kappa "
        "will match inter-annotator ranges on the independent Browserbase OM2W dataset "
        "($n=106$, different annotator population, different benchmark). "
        "The inter-annotator range is 0.53-0.57; UV achieves 0.58, confirming the law."
    ),
    prior=0.82,
)

ind_kappa = induction(
    s_internal, s_browserbase,
    law=uv_matches_human_interannotator,
    reason=(
        "Both the internal dataset and the independent Browserbase OM2W dataset provide "
        "independent confirmations that the UV's kappa falls within human inter-annotator "
        "ranges. The two datasets have different annotator populations and different "
        "benchmark sources, making them genuinely independent observations."
    ),
)

# ============================================================
# Auto-research strategies
# ============================================================

strat_auto_research_gap = support(
    [auto_research_conservative],
    auto_research_70pct,
    reason=(
        "The auto-research agent's conservative, incremental editing behavior "
        "(@auto_research_conservative) — adjusting thresholds rather than making structural "
        "changes — explains why it plateaus at ~70% of expert quality. The human expert's "
        "step-function improvements required holistic insight into failure patterns across "
        "many trajectories, not individual case adjustments."
    ),
    prior=0.83,
)

strat_complementarity = support(
    [auto_research_70pct, auto_research_cont_expert_result],
    human_expert_complementary_to_auto,
    reason=(
        "From @auto_research_70pct: auto-research achieves 70% of expert quality — "
        "showing AI can replicate most of the work. From @auto_research_cont_expert_result: "
        "initialized from the human expert's best, auto-research can still find improvements "
        "beyond the expert's peak. Together these establish the complementarity: "
        "humans discover core principles, AI fine-tunes beyond the human frontier."
    ),
    prior=0.85,
)

strat_gains_architectural = deduction(
    [upgrading_backbone_insufficient],
    gains_are_architectural,
    reason=(
        "The backbone upgrade experiment (@upgrading_backbone_insufficient) directly tests "
        "whether the model or the architecture accounts for the gains. Since upgrading to "
        "GPT-5.2 yields only modest kappa improvement while sharply increasing FNR, "
        "it follows with near-certainty that the gains are architectural. "
        "This is a deduction from the experimental result."
    ),
    prior=0.97,
)

# ============================================================
# Supporting evidence strategies
# ============================================================

strat_uv_reasoning_helps = support(
    [uv_design_invariant],
    uv_reasoning_improves_human_labels,
    reason=(
        "The UV's design invariant (@uv_design_invariant) — catching all relevant evidence "
        "including subtle hallucinations — predicts that human annotators will update their "
        "judgments when shown the UV's reasoning, primarily from success to failure. "
        "The empirical result (31 of 34 flips from success→failure) confirms the UV "
        "consistently identifies failures humans miss."
    ),
    prior=0.85,
)

strat_process_subjective = support(
    [process_outcome_separation],
    process_more_subjective_than_outcome,
    reason=(
        "Given @process_outcome_separation: process evaluation requires judging whether "
        "each execution step was reasonable given circumstances, a more nuanced judgment "
        "than the binary outcome question 'did the user's goal get met?'. This inherent "
        "subjectivity of step-level assessment predicts lower inter-annotator agreement "
        "for process ($\\kappa = 0.36-0.45$) than outcome ($\\kappa = 0.53-0.57$)."
    ),
    prior=0.85,
)

strat_native_overcount = support(
    [existing_verifiers_inadequate],
    native_verifiers_overcount_success,
    reason=(
        "Native benchmark verifiers are the same systems identified as inadequate in "
        "@existing_verifiers_inadequate — they lack the UV's architectural safeguards "
        "(rubric generation, two-pass scoring, per-criterion screenshot selection). "
        "Without these protections, they over-count success by 20%+ relative to the "
        "more reliable UV labels, as shown in Table 3."
    ),
    prior=0.88,
)

strat_unsolicited_side_effects = support(
    [outcome_label_primary_intent],
    unsolicited_side_effects,
    reason=(
        "Since @outcome_label_primary_intent specifies that users are not forgiving of "
        "unsolicited side effects, the verifier must have a mechanism to detect them. "
        "Because rubrics are generated from the task description alone (without the trajectory), "
        "they cannot anticipate all ways a task can go wrong. A dedicated detection pass "
        "over the trajectory is therefore necessary."
    ),
    prior=0.88,
)

strat_screenshot_staircase = support(
    [relevance_matrix_approach],
    screenshot_staircase_pattern,
    reason=(
        "The relevance matrix approach (@relevance_matrix_approach) assigns scores to "
        "every (screenshot, criterion) pair. For linear trajectories (most CUA tasks), "
        "later screenshots naturally score higher relevance for later criteria because "
        "the agent progressively completes sub-goals in order, producing the staircase pattern."
    ),
    prior=0.8,
)

# ============================================================
# Additional strategies for orphaned claims
# ============================================================

strat_fpr_near_zero = support(
    [uv_incorporates_all_principles],
    uv_fpr_near_zero,
    reason=(
        "The UV's architecture (@uv_incorporates_all_principles) directly predicts "
        "near-zero FPR: the two-pass hallucination detection (catching visual discrepancies), "
        "per-criterion screenshot selection (not missing evidence), and cascading-error-free "
        "rubric (not penalizing correct behavior) together eliminate false positives. "
        "Empirically: FPR = 0.01 internal, 0.08 Browserbase."
    ),
    prior=0.85,
)

strat_process_kappa = support(
    [uv_incorporates_all_principles],
    uv_process_kappa_internal,
    reason=(
        "The same UV architecture (@uv_incorporates_all_principles) that achieves high "
        "outcome kappa also achieves high process kappa ($\\kappa = 0.59$) on the internal "
        "dataset, because the rubric-based process scoring benefits from the same "
        "non-overlapping criteria design, two-pass scoring, and per-criterion screenshot "
        "selection."
    ),
    prior=0.83,
)

strat_cuaverifierbench = support(
    [iterative_development_requires_benchmark],
    cuaverifierbench_novel,
    reason=(
        "Since iterative verifier development requires a benchmark (@iterative_development_requires_benchmark), "
        "and no existing benchmark provides both process and outcome labels for CUA trajectories, "
        "CUAVerifierBench fills this gap. Its novelty (first dual-label CUA verifier benchmark) "
        "is a direct consequence of the previously unaddressed need."
    ),
    prior=0.9,
)

strat_auto_research_from_blank = support(
    [auto_research_conservative],
    auto_research_from_blank_result,
    reason=(
        "The conservative and incremental editing behavior documented in @auto_research_conservative "
        "explains the quantitative result: the from-blank agent achieves $\\kappa \\approx 0.55$ "
        "(approximately 70% of expert's $\\kappa \\approx 0.7$) because it makes gradual "
        "adjustments rather than the structural leaps that drove the expert's largest gains."
    ),
    prior=0.83,
)

strat_agentrewardbench = support(
    [existing_verifiers_inadequate],
    agentrewardbench_fpr,
    reason=(
        "The pattern of existing verifiers over-counting success (@existing_verifiers_inadequate) "
        "extends to AgentRewardBench's human annotations: when expert annotators apply the "
        "UV's outcome guidelines to 30 sampled successful trajectories, 8/30 ($\\approx 27\\%$) "
        "are found to be false positives — consistent with the broader pattern of inadequate "
        "verification standards in the field."
    ),
    prior=0.75,
)

strat_rubric_score_corr = support(
    [uv_incorporates_all_principles],
    rubric_score_correlation,
    reason=(
        "The UV's structured rubric-based scoring (@uv_incorporates_all_principles) "
        "should produce continuous rubric scores that correlate with human annotators' "
        "continuous rubric scores on the same criteria, since both are evaluating the "
        "same agent behavior against the same rubric. "
        "The Pearson $r = 0.61$ and Spearman $\\rho = 0.58$ confirm this."
    ),
    prior=0.8,
)

strat_stochastic_variance = support(
    [separate_generation_scoring],
    auto_research_stochastic_variance,
    reason=(
        "The separation of rubric generation from scoring (@separate_generation_scoring) "
        "means that non-deterministic LLM rubric generation introduces variance: different "
        "rubrics for the same task can lead to different final kappa values. Since rubric "
        "generation is inherently stochastic, repeat runs with identical prompts will produce "
        "kappa values that vary in the range 0.64-0.71."
    ),
    prior=0.78,
)

strat_gpt52_fpr = support(
    [gains_are_architectural],
    gpt52_lowest_fpr,
    reason=(
        "If the UV's advantage is architectural (@gains_are_architectural), then "
        "model-level differences (GPT-5.2 vs others) should show up primarily in "
        "conservatism (FPR) rather than overall agreement (kappa), since the architecture "
        "is the dominant factor. GPT-5.2's lowest FPR (0.03/0.00) while not having the "
        "highest kappa confirms this: it is the most conservative scorer."
    ),
    prior=0.78,
)

strat_fixed_rubric = support(
    [gains_are_architectural],
    fixed_rubric_ablation,
    reason=(
        "Since the UV's advantage is architectural (@gains_are_architectural), the "
        "scoring model's contribution should be identifiable when the rubric is held "
        "fixed (removing that architectural variable). The fixed-rubric ablation isolates "
        "the scorer effect: GPT-5.1 achieves highest outcome kappa (0.74) while GPT-5.2 "
        "remains most conservative, consistent with architecture dominating over scorer choice."
    ),
    prior=0.78,
)

strat_uv_as_annotator = support(
    [uv_matches_human_interannotator],
    uv_as_annotator,
    reason=(
        "Since the UV agrees with humans as well as humans agree with each other "
        "(@uv_matches_human_interannotator), it is valid to treat the UV as an annotator "
        "equivalent to a human and compute inter-annotator agreement metrics between "
        "the UV and other annotators."
    ),
    prior=0.88,
)

# ============================================================
# Operators: contradictions/complements
# ============================================================

# The architectural vs. model hypotheses are contradictory (cannot both fully explain)
not_both_architectural_and_model = contradiction(
    gains_are_architectural,
    alt_fpr_reduction_is_model,
    reason=(
        "These two claims are mutually exclusive as complete explanations of the UV's "
        "advantage: if the advantage is primarily architectural (not model-driven), "
        "then the model-driven alternative is refuted, and vice versa."
    ),
    prior=0.9,
)
