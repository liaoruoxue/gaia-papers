"""Pass 2 wiring: strategies, induction, abduction, contradictions.

Conventions:

* `support` -- soft deduction with author-specified prior. Default for
  premises -> conclusion with reconstruction-source uncertainty.
* `induction` -- chained binary composite over the 3-benchmark panel
  (Pixmo-Count + Maze + Path Tracing) supporting the law 'DeepSeek
  Visual Primitives significantly outperforms frontier models on
  spatial-reasoning benchmarks at extremely low visual-token cost'.
* `abduction` -- the central abductive structure of the paper:
  hypothesis = the visual-primitive design + Reference-Gap diagnosis
  explains the outperformance pattern; alternative = trivial confounds
  (bigger MoE / more training data / better base model) explain it.
  The 81-KV-entry / 7056x compression discriminates.
* `contradiction` -- two contradictions:
    (i) Reference-Gap diagnosis vs prevailing Perception-Gap-is-the-
        bottleneck assumption;
    (ii) the prevailing 'more visual tokens = better' assumption vs the
         81-KV-entry outperformance.

Reconstruction-source uncertainty: the Visual Primitives GitHub repo
[@DeepSeekVisualPrimitives] was withdrawn shortly after release; this
formalization is reconstructed from CSDN [@CSDNDeepRead], Phoenix
Technology [@PhoenixTech], and 36Kr [@ThirtySixKr] coverage. Strategy
priors carry a modest discount (~0.05) for empirical numbers vs
architectural-design claims that are corroborated across multiple
sources.
"""

from gaia.lang import (
    abduction,
    claim,
    compare,
    contradiction,
    induction,
    support,
)

from .motivation import (
    claim_industry_chases_perception,
    claim_layer1_problem,
    claim_layer1_result,
    claim_layer1_solution,
    claim_natural_language_imprecise_in_continuous_space,
    claim_referential_ambiguity_running_example,
    claim_tldr_architecture,
    claim_tldr_diagnosis,
    claim_tldr_method,
    claim_tldr_pipeline_alignment,
    claim_tldr_training,
    setup_dense_scene_definition,
    setup_multimodal_reasoning_regime,
    setup_visual_primitive_tokens,
)
from .s2_diagnosis_reference_gap import (
    claim_industry_perception_path_hits_ceiling,
    claim_next_frontier_is_pointing_not_seeing,
    claim_perception_gap_is_actual_bottleneck,
    claim_reference_gap_is_actual_bottleneck,
    setup_perception_gap_definition,
    setup_reference_gap_definition,
)
from .s3_method_visual_primitives import (
    claim_information_density_over_volume,
    claim_method_lift_to_thought_unit,
    claim_pointing_during_reasoning,
    claim_visual_primitives_close_reference_gap,
    setup_cot_token_stream,
)
from .s4_architecture import (
    claim_2916_to_324_tokens,
    claim_324_to_81_kv,
    claim_756_to_2916_patches,
    claim_architecture_supports_high_density,
    claim_architecture_table,
    claim_end_to_end_7056x,
    setup_3x3_patch_merge,
    setup_csa_4x,
    setup_deepseek_vit,
    setup_v4_flash_backbone,
)
from .s5_data_pipeline import (
    claim_coldstart_design_principles,
    claim_coldstart_table,
    claim_coldstart_total,
    claim_filter_stage1,
    claim_filter_stage2,
    claim_filter_yield,
    claim_pretrain_filter_table,
    setup_postpost_filter_purpose,
    setup_pretrain_source_count,
)
from .s6_training_pipeline import (
    claim_phase1_separate_experts,
    claim_phase2_per_expert_grpo,
    claim_phase3_rft,
    claim_phase4_distillation,
    claim_pipeline_diagram,
    claim_pipeline_motivation,
    setup_expert_notation,
    setup_pattern_conflict,
)
from .s7_reward_model import (
    claim_format_rm,
    claim_quality_rm,
    claim_rm_decomposition_rationale,
    claim_rm_supports_grpo_quality,
    claim_task_accuracy_rm,
    setup_three_way_rm,
)
from .s8_results import (
    claim_cross_benchmark_outperformance,
    claim_frontier_near_random_on_spatial,
    claim_maze_deepseek,
    claim_maze_frontier,
    claim_more_tokens_is_better,
    claim_path_deepseek,
    claim_path_frontier,
    claim_pixmo_deepseek,
    claim_pixmo_frontier,
    claim_results_table,
    setup_benchmark_panel,
    setup_random_baseline_50,
)
from .s9_limitations import (
    claim_lim_synthesis_two_open_problems,
    claim_lim_topology_sharpening_tradeoff,
    claim_lim_topology_weakness,
    claim_lim_trigger_analogue_to_armskill,
    claim_lim_trigger_incomplete_internalization,
    claim_lim_trigger_word_dependency,
    setup_topology_generalization,
    setup_trigger_word_definition,
)
from .s10_ocr2_pipeline import (
    claim_alignment_compression_axis,
    claim_alignment_means_axis,
    claim_alignment_problem_axis,
    claim_alignment_solution_axis,
    claim_alignment_table,
    claim_complete_pipeline,
    claim_meta_thesis_organization_over_volume,
    claim_opposition_to_industry,
    setup_ocr2_role,
)


# ============================================================================
# motivation: TL;DR -> Layer-1 anchors
# ============================================================================

strat_referential_ambiguity_from_language = support(
    [claim_natural_language_imprecise_in_continuous_space],
    claim_referential_ambiguity_running_example,
    reason=(
        "The 'left big red object' running example "
        "(@claim_referential_ambiguity_running_example) is a concrete "
        "instance of the general property "
        "(@claim_natural_language_imprecise_in_continuous_space) that "
        "natural language compresses continuous spatial information "
        "lossily: 'left' is relative, 'big' is comparative, and "
        "neither indexes a specific pixel-space referent."
    ),
    prior=0.92,
    background=[setup_dense_scene_definition, setup_multimodal_reasoning_regime],
)

strat_layer1_problem_from_running_example = support(
    [
        claim_referential_ambiguity_running_example,
        claim_natural_language_imprecise_in_continuous_space,
    ],
    claim_layer1_problem,
    reason=(
        "The Layer-1 problem statement (@claim_layer1_problem) -- that "
        "natural-language spatial description leads to attention drift "
        "and logical collapse in dense scenes -- combines the running "
        "example (@claim_referential_ambiguity_running_example) with "
        "the structural property of language "
        "(@claim_natural_language_imprecise_in_continuous_space). "
        "Repeated lossy reference compounds across CoT depth."
    ),
    prior=0.88,
    background=[setup_dense_scene_definition],
)

strat_tldr_diagnosis_from_layer1 = support(
    [
        claim_reference_gap_is_actual_bottleneck,
    ],
    claim_tldr_diagnosis,
    reason=(
        "The TL;DR-1 diagnosis (@claim_tldr_diagnosis) -- bottleneck "
        "is the Reference Gap, not the Perception Gap -- restates "
        "the Section-3.1 diagnosis "
        "(@claim_reference_gap_is_actual_bottleneck) as a one-line "
        "summary."
    ),
    prior=0.95,
)

strat_layer1_solution_from_method = support(
    [claim_method_lift_to_thought_unit],
    claim_layer1_solution,
    reason=(
        "The Layer-1 solution slogan -- 'embed primitives in CoT, "
        "point rather than describe' (@claim_layer1_solution) -- is "
        "the headline form of the method's core operation: lifting "
        "`<|box|>` and `<|point|>` to thought-unit status inside CoT "
        "(@claim_method_lift_to_thought_unit)."
    ),
    prior=0.95,
)

strat_tldr_method_from_method = support(
    [claim_method_lift_to_thought_unit, claim_pointing_during_reasoning],
    claim_tldr_method,
    reason=(
        "TL;DR-2 (@claim_tldr_method) restates the method core "
        "(@claim_method_lift_to_thought_unit) plus the intended "
        "behaviour (@claim_pointing_during_reasoning) -- 'point "
        "while reasoning' -- as a one-line summary."
    ),
    prior=0.95,
    background=[setup_visual_primitive_tokens],
)


# ============================================================================
# s2: Reference-Gap diagnosis
# ============================================================================

strat_diagnosis_from_language_property = support(
    [claim_natural_language_imprecise_in_continuous_space],
    claim_reference_gap_is_actual_bottleneck,
    reason=(
        "The headline diagnosis (@claim_reference_gap_is_actual_"
        "bottleneck) -- that the Reference Gap, not the Perception "
        "Gap, is the bottleneck -- follows from the structural "
        "property that natural language is intrinsically imprecise "
        "for continuous visual reference "
        "(@claim_natural_language_imprecise_in_continuous_space). If "
        "the language channel is the bottleneck, then more pixels / "
        "tokens (Perception Gap closures) cannot resolve the "
        "limitation."
    ),
    prior=0.85,
    background=[
        setup_perception_gap_definition,
        setup_reference_gap_definition,
    ],
)

strat_industry_ceiling_from_diagnosis = support(
    [
        claim_reference_gap_is_actual_bottleneck,
        claim_industry_chases_perception,
    ],
    claim_industry_perception_path_hits_ceiling,
    reason=(
        "If the actual bottleneck is the Reference Gap "
        "(@claim_reference_gap_is_actual_bottleneck), then the "
        "frontier strategy of scaling resolution / token count "
        "(@claim_industry_chases_perception) hits a referential-"
        "ambiguity ceiling rather than a perception ceiling "
        "(@claim_industry_perception_path_hits_ceiling). The ceiling "
        "is a property of the channel, not of perception."
    ),
    prior=0.84,
)

strat_next_frontier_from_diagnosis = support(
    [claim_reference_gap_is_actual_bottleneck],
    claim_next_frontier_is_pointing_not_seeing,
    reason=(
        "The slogan 'next frontier = pointing precisely, not seeing "
        "clearly' (@claim_next_frontier_is_pointing_not_seeing) is "
        "the design implication of the Reference-Gap diagnosis "
        "(@claim_reference_gap_is_actual_bottleneck): closing the "
        "gap requires a referential modality embedded in the "
        "reasoning trace, not more pixels."
    ),
    prior=0.86,
)

# Contradiction (i): Reference Gap diagnosis vs the Perception-Gap foil
contra_reference_vs_perception = contradiction(
    claim_reference_gap_is_actual_bottleneck,
    claim_perception_gap_is_actual_bottleneck,
    reason=(
        "Both claims are claims about *the* bottleneck of multimodal "
        "reasoning. They cannot both be true: the Reference-Gap "
        "diagnosis (@claim_reference_gap_is_actual_bottleneck) "
        "asserts the language channel is the binding constraint, "
        "while the Perception-Gap foil "
        "(@claim_perception_gap_is_actual_bottleneck) asserts "
        "perception fidelity is. The Visual Primitives empirical "
        "panel discriminates: ~81 KV entries beat 1000+-token "
        "frontier models on spatial reasoning, which is "
        "incompatible with perception being the bottleneck."
    ),
    prior=0.97,
)


# ============================================================================
# s3: visual primitives method
# ============================================================================

strat_method_lifts_from_setup = support(
    [claim_natural_language_imprecise_in_continuous_space],
    claim_method_lift_to_thought_unit,
    reason=(
        "The method-core claim (@claim_method_lift_to_thought_unit) "
        "is the design response to the structural property of "
        "language (@claim_natural_language_imprecise_in_continuous_"
        "space): the two primitive token classes "
        "(@setup_visual_primitive_tokens), embedded in the CoT "
        "single-token-stream regime (@setup_cot_token_stream), are "
        "treated as first-class thought-units rather than auxiliary "
        "outputs. Background setup makes the design choice "
        "realizable; the claim asserts the choice was made."
    ),
    prior=0.9,
    background=[setup_visual_primitive_tokens, setup_cot_token_stream],
)

strat_pointing_from_lifting = support(
    [claim_method_lift_to_thought_unit],
    claim_pointing_during_reasoning,
    reason=(
        "The 'point while reasoning' behaviour "
        "(@claim_pointing_during_reasoning) is the operational "
        "signature of lifting primitives to thought-unit status "
        "(@claim_method_lift_to_thought_unit): once primitives can "
        "be emitted mid-CoT, the model can anchor a position at the "
        "moment it would otherwise have named one in prose."
    ),
    prior=0.92,
)

strat_close_reference_gap = support(
    [
        claim_pointing_during_reasoning,
        claim_natural_language_imprecise_in_continuous_space,
    ],
    claim_visual_primitives_close_reference_gap,
    reason=(
        "Visual primitives close the Reference Gap "
        "(@claim_visual_primitives_close_reference_gap) because "
        "(a) emitting a precise coordinate during CoT "
        "(@claim_pointing_during_reasoning) replaces a referentially "
        "ambiguous natural-language description "
        "(@claim_natural_language_imprecise_in_continuous_space) "
        "with a unique pixel-space referent, and (b) subsequent CoT "
        "can refer back to that anchor without re-introducing "
        "ambiguity."
    ),
    prior=0.9,
)

strat_density_over_volume_from_method = support(
    [
        claim_visual_primitives_close_reference_gap,
        claim_architecture_supports_high_density,
    ],
    claim_information_density_over_volume,
    reason=(
        "The density-over-volume design philosophy "
        "(@claim_information_density_over_volume) is the natural "
        "consequence of (a) primitives carrying high referential "
        "density per token "
        "(@claim_visual_primitives_close_reference_gap) and "
        "(b) the 7056x-compression architecture supporting low-"
        "token-count operation "
        "(@claim_architecture_supports_high_density)."
    ),
    prior=0.9,
)


# ============================================================================
# s4: architecture
# ============================================================================

strat_756_to_2916 = support(
    [claim_architecture_table],
    claim_756_to_2916_patches,
    reason=(
        "Per the architecture table (@claim_architecture_table) "
        "DeepSeek-ViT (@setup_deepseek_vit) uses 14x14 patches, so "
        "a 756x756 input image yields $(756/14)^2 = 2916$ patch "
        "tokens (@claim_756_to_2916_patches). Direct arithmetic "
        "from the patch size and input resolution."
    ),
    prior=0.96,
    background=[setup_deepseek_vit],
)

strat_2916_to_324 = support(
    [claim_756_to_2916_patches],
    claim_2916_to_324_tokens,
    reason=(
        "Applying the 3x3 channel-concatenation patch merge "
        "(@setup_3x3_patch_merge) to the 2916 patch tokens "
        "(@claim_756_to_2916_patches) yields $2916 / 9 = 324$ "
        "tokens (@claim_2916_to_324_tokens)."
    ),
    prior=0.96,
    background=[setup_3x3_patch_merge],
)

strat_324_to_81 = support(
    [claim_2916_to_324_tokens],
    claim_324_to_81_kv,
    reason=(
        "Applying CSA's 4x KV-cache compression (@setup_csa_4x) to "
        "the 324 visual tokens (@claim_2916_to_324_tokens) yields "
        "$\\sim 324 / 4 = 81$ KV entries (@claim_324_to_81_kv)."
    ),
    prior=0.94,
    background=[setup_csa_4x],
)

strat_end_to_end_7056x = support(
    [
        claim_756_to_2916_patches,
        claim_2916_to_324_tokens,
        claim_324_to_81_kv,
    ],
    claim_end_to_end_7056x,
    reason=(
        "The end-to-end 7056x compression "
        "(@claim_end_to_end_7056x) is the chained product of (a) "
        "patch-size pixel-to-patch ratio $14^2 = 196$ "
        "(@claim_756_to_2916_patches), (b) the 9x reduction from "
        "the 3x3 merge (@claim_2916_to_324_tokens), and (c) the 4x "
        "reduction from CSA (@claim_324_to_81_kv): "
        "$196 \\times 9 \\times 4 = 7056$."
    ),
    prior=0.94,
)

# Note: claim_architecture_table is treated as a leaf observation claim
# (it is the verbatim transcription of the source's architecture table),
# so it has no incoming strategy and gets a prior in priors.py. Its
# constituent settings (DeepSeek-ViT, 3x3 patch merge, CSA, V4-Flash)
# anchor the table semantically but are not strategy premises.

strat_high_density_from_compression = support(
    [claim_end_to_end_7056x],
    claim_architecture_supports_high_density,
    reason=(
        "The 7056x end-to-end compression (@claim_end_to_end_7056x) "
        "drives the visual-token budget down to ~81 KV entries on "
        "a 756x756 image, which is what makes the architecture "
        "purpose-built for high-density visual signal "
        "(@claim_architecture_supports_high_density)."
    ),
    prior=0.92,
)

strat_tldr_arch_summary = support(
    [
        claim_architecture_table,
        claim_end_to_end_7056x,
    ],
    claim_tldr_architecture,
    reason=(
        "TL;DR-3 (@claim_tldr_architecture) is the one-line "
        "summary of the architecture table "
        "(@claim_architecture_table) plus the end-to-end "
        "compression ratio (@claim_end_to_end_7056x)."
    ),
    prior=0.93,
)


# ============================================================================
# s5: data pipeline
# ============================================================================

strat_filter_stage1 = support(
    [claim_pretrain_filter_table],
    claim_filter_stage1,
    reason=(
        "Stage-1 Semantic Review (@claim_filter_stage1) is the "
        "first row of the pre-training filter table "
        "(@claim_pretrain_filter_table) -- the two-stage review "
        "purpose (@setup_postpost_filter_purpose) applied to the "
        "97,984-source candidate pool (@setup_pretrain_source_count) "
        "yields 43,141."
    ),
    prior=0.92,
    background=[setup_pretrain_source_count, setup_postpost_filter_purpose],
)

strat_filter_stage2 = support(
    [claim_filter_stage1, claim_pretrain_filter_table],
    claim_filter_stage2,
    reason=(
        "Stage-2 Visual-Geometric Review (@claim_filter_stage2) is "
        "the second row of the pre-training filter table "
        "(@claim_pretrain_filter_table): it takes the 43,141 from "
        "Stage-1 (@claim_filter_stage1) and filters again on "
        "visual-geometric criteria "
        "(@setup_postpost_filter_purpose), yielding 31,701."
    ),
    prior=0.92,
    background=[setup_postpost_filter_purpose],
)

strat_filter_yield = support(
    [
        claim_filter_stage1,
        claim_filter_stage2,
    ],
    claim_filter_yield,
    reason=(
        "Pipeline yield (@claim_filter_yield) is the arithmetic "
        "31,701 / 97,984 = 32.4%, computed from the original "
        "candidate pool size (@setup_pretrain_source_count) and "
        "the two stage outputs (@claim_filter_stage1, "
        "@claim_filter_stage2)."
    ),
    prior=0.96,
    background=[setup_pretrain_source_count],
)

# Note: claim_pretrain_filter_table is treated as a leaf observation
# claim (the verbatim transcription of the source's filter table). Its
# stages claim_filter_stage1 / claim_filter_stage2 are derived FROM
# the table; the table itself is anchored by a prior in priors.py.

strat_coldstart_total = support(
    [claim_coldstart_table],
    claim_coldstart_total,
    reason=(
        "The cold-start total (@claim_coldstart_total) is the "
        "arithmetic sum of the four task counts in the cold-start "
        "table (@claim_coldstart_table): "
        "$10\\text{K} + 9\\text{K} + 460\\text{K} + 125\\text{K} = "
        "604\\text{K}$."
    ),
    prior=0.95,
)

strat_coldstart_design_principles = support(
    [claim_coldstart_table],
    claim_coldstart_design_principles,
    reason=(
        "The three design principles -- negative sampling, colour-"
        "shortcut prevention, topology diversity "
        "(@claim_coldstart_design_principles) -- are read directly "
        "from the per-task design column of the cold-start data "
        "table (@claim_coldstart_table)."
    ),
    prior=0.93,
)

strat_tldr_training_summary = support(
    [
        claim_pipeline_motivation,
        claim_pretrain_filter_table,
        claim_coldstart_table,
    ],
    claim_tldr_training,
    reason=(
        "TL;DR-4 (@claim_tldr_training) restates the four-phase "
        "Expert-Merge-Distill pipeline (@claim_pipeline_motivation), "
        "the pre-training filter (@claim_pretrain_filter_table), "
        "and the cold-start composition (@claim_coldstart_table) "
        "as a one-line summary."
    ),
    prior=0.9,
)


# ============================================================================
# s6: training pipeline (Expert-Merge-Distill)
# ============================================================================

strat_phase1_from_conflict = support(
    [claim_pipeline_diagram],
    claim_phase1_separate_experts,
    reason=(
        "Phase 1 -- separate Box and Point experts "
        "(@claim_phase1_separate_experts) -- is the first stage of "
        "the pipeline diagram (@claim_pipeline_diagram), and is the "
        "design response to the pattern-conflict observation "
        "(@setup_pattern_conflict): jointly training both primitive "
        "classes from scratch causes trigger-activation collisions, "
        "so the recipe trains $F_{\\text{TwG}}$ and "
        "$F_{\\text{TwP}}$ (@setup_expert_notation) independently."
    ),
    prior=0.91,
    background=[setup_pattern_conflict, setup_expert_notation],
)

strat_phase2_from_phase1 = support(
    [claim_phase1_separate_experts],
    claim_phase2_per_expert_grpo,
    reason=(
        "Phase 2 -- per-expert GRPO RL "
        "(@claim_phase2_per_expert_grpo) -- runs RL inside each "
        "expert's own primitive regime (@claim_phase1_separate_"
        "experts) under the 3-way Reward Model "
        "(@setup_three_way_rm), so reward-hacking patterns specific "
        "to one primitive cannot bleed into the other."
    ),
    prior=0.91,
    background=[setup_three_way_rm],
)

strat_phase3_from_phase2 = support(
    [claim_phase2_per_expert_grpo],
    claim_phase3_rft,
    reason=(
        "Phase 3 -- RFT "
        "(@claim_phase3_rft) -- uses the trained experts from "
        "Phase 2 (@claim_phase2_per_expert_grpo) as a rollout "
        "source: high-reward trajectories are selected and used "
        "for supervised rejection-sampled fine-tuning of the "
        "unified model."
    ),
    prior=0.92,
)

strat_phase4_from_phase3 = support(
    [claim_phase3_rft],
    claim_phase4_distillation,
    reason=(
        "Phase 4 -- on-policy distillation into unified $F$ "
        "(@claim_phase4_distillation) -- consumes the RFT'd unified "
        "model (@claim_phase3_rft) and uses the experts from "
        "Phase 1 (@setup_expert_notation) as soft-target teachers "
        "for primitive emission tokens."
    ),
    prior=0.9,
    background=[setup_expert_notation],
)

strat_pipeline_motivation = support(
    [
        claim_phase1_separate_experts,
        claim_phase4_distillation,
    ],
    claim_pipeline_motivation,
    reason=(
        "The Expert-Merge-Distill recipe motivation "
        "(@claim_pipeline_motivation) -- separate to avoid pattern "
        "conflict, then merge -- summarizes the role of each phase: "
        "Phases 1-2 are pre-merge to avoid the conflict "
        "(@setup_pattern_conflict, @claim_phase1_separate_experts), "
        "Phases 3-4 transfer and stabilize the merged behaviour "
        "(@claim_phase4_distillation)."
    ),
    prior=0.92,
    background=[setup_pattern_conflict],
)

# Note: claim_pipeline_diagram is a verbatim transcription of the source
# diagram and is treated as a leaf observation (anchored by a prior in
# priors.py). The four phase claims are derived FROM the diagram, not
# the other way around.


# ============================================================================
# s7: 3-way reward model
# ============================================================================

strat_rm_decomposition = support(
    [
        claim_format_rm,
        claim_quality_rm,
        claim_task_accuracy_rm,
    ],
    claim_rm_decomposition_rationale,
    reason=(
        "The decomposition rationale "
        "(@claim_rm_decomposition_rationale) follows from the "
        "design of the three reward terms (@setup_three_way_rm): "
        "Format RM blocks malformed primitive emission "
        "(@claim_format_rm), Quality RM blocks reasoning "
        "pathologies and reward hacking (@claim_quality_rm), and "
        "Task-Specific Accuracy RM grounds the reward in "
        "ground-truth task performance (@claim_task_accuracy_rm). "
        "Each term targets an orthogonal failure mode."
    ),
    prior=0.92,
    background=[setup_three_way_rm],
)

strat_rm_supports_grpo = support(
    [
        claim_rm_decomposition_rationale,
        claim_phase2_per_expert_grpo,
    ],
    claim_rm_supports_grpo_quality,
    reason=(
        "The 3-way RM is the precondition for stable per-expert "
        "GRPO (@claim_rm_supports_grpo_quality) because each of "
        "Format, Quality, and Task-Specific Accuracy provides "
        "non-substitutable signal "
        "(@claim_rm_decomposition_rationale), and Phase 2's GRPO "
        "step (@claim_phase2_per_expert_grpo) consumes all three "
        "in parallel."
    ),
    prior=0.91,
)


# ============================================================================
# s8: results -- per-benchmark anchors and the cross-benchmark induction
# ============================================================================

strat_pixmo_results_anchor = support(
    [claim_results_table],
    claim_pixmo_deepseek,
    reason=(
        "DeepSeek's Pixmo-Count score 89.2% "
        "(@claim_pixmo_deepseek) is read directly from the "
        "Pixmo-Count row of the results table "
        "(@claim_results_table)."
    ),
    prior=0.95,
)

strat_pixmo_frontier_anchor = support(
    [claim_results_table],
    claim_pixmo_frontier,
    reason=(
        "The Pixmo-Count frontier scores -- Gemini-3-Flash 88.2%, "
        "GPT-5.4 76.6%, Claude 4.6 68.7% (@claim_pixmo_frontier) "
        "-- are read directly from the Pixmo-Count row of the "
        "results table (@claim_results_table)."
    ),
    prior=0.93,
)

strat_maze_results_anchor = support(
    [claim_results_table],
    claim_maze_deepseek,
    reason=(
        "DeepSeek's Maze Navigation score 66.9% "
        "(@claim_maze_deepseek) is read directly from the Maze "
        "row of the results table (@claim_results_table); the "
        "+16.3 pp lift over the next-best frontier model is the "
        "arithmetic difference 66.9% - 50.6%."
    ),
    prior=0.94,
)

strat_maze_frontier_anchor = support(
    [claim_results_table],
    claim_maze_frontier,
    reason=(
        "The Maze Navigation frontier scores -- GPT-5.4 50.6%, "
        "Gemini 49.4%, Claude 48.9% (@claim_maze_frontier) -- are "
        "read directly from the Maze row of the results table "
        "(@claim_results_table); all three are within ~2 pp of "
        "the ~50% random baseline (@setup_random_baseline_50)."
    ),
    prior=0.93,
    background=[setup_random_baseline_50],
)

strat_path_results_anchor = support(
    [claim_results_table],
    claim_path_deepseek,
    reason=(
        "DeepSeek's Path Tracing score 56.7% "
        "(@claim_path_deepseek) is read directly from the Path "
        "Tracing row of the results table "
        "(@claim_results_table); the +10.2 pp lift over GPT-5.4 "
        "is the arithmetic difference 56.7% - 46.5%."
    ),
    prior=0.94,
)

strat_path_frontier_anchor = support(
    [claim_results_table],
    claim_path_frontier,
    reason=(
        "The Path Tracing frontier scores -- GPT-5.4 46.5%, "
        "Gemini 41.4%, Claude 30.6% (@claim_path_frontier) -- are "
        "read directly from the Path Tracing row of the results "
        "table (@claim_results_table); Claude is below the 50% "
        "random baseline (@setup_random_baseline_50)."
    ),
    prior=0.93,
    background=[setup_random_baseline_50],
)

strat_frontier_near_random = support(
    [
        claim_maze_frontier,
        claim_path_frontier,
    ],
    claim_frontier_near_random_on_spatial,
    reason=(
        "Frontier models score at or below random on spatial "
        "reasoning (@claim_frontier_near_random_on_spatial): on "
        "Maze (@claim_maze_frontier) all three are 48.9-50.6%; "
        "on Path Tracing (@claim_path_frontier) Claude is 30.6% "
        "(below random) and GPT-5.4 / Gemini are 46.5% / 41.4%."
    ),
    prior=0.92,
    background=[setup_random_baseline_50],
)

# Per-benchmark generative-direction supports for the cross-benchmark
# induction: cross-benchmark law -> per-benchmark observation.
ind_pixmo = support(
    [claim_cross_benchmark_outperformance],
    claim_pixmo_deepseek,
    reason=(
        "If DeepSeek Visual Primitives significantly outperforms "
        "frontier models on spatial-reasoning benchmarks at "
        "extremely low visual-token cost "
        "(@claim_cross_benchmark_outperformance), the law predicts "
        "a panel-best score on Pixmo-Count "
        "(@claim_pixmo_deepseek)."
    ),
    prior=0.85,
    background=[setup_benchmark_panel],
)

ind_maze = support(
    [claim_cross_benchmark_outperformance],
    claim_maze_deepseek,
    reason=(
        "If DeepSeek significantly outperforms frontier models on "
        "spatial reasoning at low visual-token cost "
        "(@claim_cross_benchmark_outperformance), the law predicts "
        "a panel-best Maze Navigation score "
        "(@claim_maze_deepseek), and predicts the lift to be large "
        "since the baselines hover near random."
    ),
    prior=0.88,
    background=[setup_benchmark_panel, setup_random_baseline_50],
)

ind_path = support(
    [claim_cross_benchmark_outperformance],
    claim_path_deepseek,
    reason=(
        "If DeepSeek significantly outperforms frontier models on "
        "spatial reasoning at low visual-token cost "
        "(@claim_cross_benchmark_outperformance), the law predicts "
        "a panel-best Path Tracing score "
        "(@claim_path_deepseek)."
    ),
    prior=0.86,
    background=[setup_benchmark_panel, setup_random_baseline_50],
)

ind_pixmo_maze = induction(
    ind_pixmo,
    ind_maze,
    law=claim_cross_benchmark_outperformance,
    reason=(
        "Pixmo-Count and Maze Navigation are independent benchmarks "
        "with different stimulus distributions (natural counting "
        "scenes vs synthetic mazes); both panel-best scores from "
        "DeepSeek support the cross-benchmark outperformance law."
    ),
)

ind_three_benchmarks = induction(
    ind_pixmo_maze,
    ind_path,
    law=claim_cross_benchmark_outperformance,
    reason=(
        "Adding Path Tracing -- a third independent benchmark with "
        "yet another stimulus distribution (Bezier curves) -- "
        "completes the 3-benchmark induction. All three panel-best "
        "scores together support the cross-benchmark outperformance "
        "law (@claim_cross_benchmark_outperformance)."
    ),
)


# ============================================================================
# CENTRAL ABDUCTION: the visual-primitive design explains the outperformance
# pattern, NOT trivial confounds (bigger MoE / more data / better base model).
# ============================================================================

# Alternative explanation claim is declared here in the wiring (it is a
# competing-explanation foil that exists only in service of the abduction).
claim_alt_trivial_confounds = claim(
    "**Alternative explanation: trivial confounds.** Could the "
    "DeepSeek panel lift be explained by trivial confounds -- "
    "(a) a bigger MoE backbone (DeepSeek-V4-Flash 284B/13B), "
    "(b) more / better cold-start data (~604K samples), or "
    "(c) a stronger base language model -- rather than by the "
    "visual-primitive design and the Reference-Gap diagnosis? "
    "If so, the visual-primitive method is incidental to the "
    "outperformance.",
    title="Alternative: trivial confounds (bigger MoE / more data / better base) explain the lift",
)

# Hypothesis support: visual-primitive design + Reference-Gap diagnosis.
abd_h = support(
    [
        claim_visual_primitives_close_reference_gap,
        claim_information_density_over_volume,
        claim_architecture_supports_high_density,
    ],
    claim_cross_benchmark_outperformance,
    reason=(
        "Hypothesis H: the visual-primitive design explains the "
        "outperformance pattern (@claim_cross_benchmark_outperformance). "
        "Closing the Reference Gap "
        "(@claim_visual_primitives_close_reference_gap) eliminates "
        "the dominant failure mode of frontier models on dense-"
        "scene spatial reasoning; the density-over-volume "
        "philosophy (@claim_information_density_over_volume) plus "
        "an architecture purpose-built for that philosophy "
        "(@claim_architecture_supports_high_density) is what "
        "delivers the panel-best scores at ~81 KV entries."
    ),
    prior=0.88,
)

# Alternative support.
abd_alt = support(
    [claim_alt_trivial_confounds],
    claim_cross_benchmark_outperformance,
    reason=(
        "Alternative Alt: a bigger MoE / more data / better base "
        "(@claim_alt_trivial_confounds) would normally suffice to "
        "lift benchmark scores. If true, this would explain the "
        "panel-best scores (@claim_cross_benchmark_outperformance) "
        "without the visual-primitive design playing a load-"
        "bearing role."
    ),
    prior=0.3,
)

abd_compare = compare(
    claim_information_density_over_volume,
    claim_alt_trivial_confounds,
    claim_cross_benchmark_outperformance,
    reason=(
        "The 81-KV-entry / 7056x compression result is the "
        "discriminator. H's prediction "
        "(@claim_information_density_over_volume): panel-best "
        "scores at extremely low visual-token cost. Alt's "
        "prediction (@claim_alt_trivial_confounds): panel-best "
        "scores require *more* of the conventional levers "
        "(bigger model, more tokens, more data). The observation "
        "(@claim_cross_benchmark_outperformance) is panel-best "
        "scores at orders-of-magnitude lower visual-token budget "
        "than the frontier, contradicting Alt's prediction "
        "direction. Frontier models have comparable MoE scale; "
        "the discriminator is the compression ratio plus the "
        "per-task lift on Maze (+16.3 pp) and Path Tracing "
        "(+10.2 pp), neither of which is what 'bigger MoE' "
        "would predict."
    ),
    prior=0.92,
)

abd_central = abduction(
    abd_h,
    abd_alt,
    abd_compare,
    reason=(
        "Central abduction. The same observation -- DeepSeek panel-"
        "best on Pixmo-Count + Maze + Path Tracing at ~81 KV "
        "entries (@claim_cross_benchmark_outperformance) -- is "
        "explained by H = visual-primitive design + Reference-Gap "
        "diagnosis (abd_h) and by Alt = trivial confounds "
        "(@claim_alt_trivial_confounds, abd_alt). The discriminator "
        "(abd_compare) is the 81-KV-entry / 7056x compression: H "
        "predicts low-token-budget outperformance, Alt does not."
    ),
)


# ============================================================================
# Cross-benchmark synthesis -> the layer-1 result headline
# ============================================================================

# Note: claim_results_table is treated as a leaf observation (the
# verbatim transcription of the source's results table). The six
# per-benchmark scores are derived FROM the table via the strats below.

strat_layer1_result_from_cross_benchmark = support(
    [
        claim_cross_benchmark_outperformance,
        claim_end_to_end_7056x,
    ],
    claim_layer1_result,
    reason=(
        "The Layer-1 headline result (@claim_layer1_result) "
        "restates the cross-benchmark outperformance claim "
        "(@claim_cross_benchmark_outperformance) at the specific "
        "visual-token budget made possible by the architecture "
        "(@claim_end_to_end_7056x): ~81 KV entries on a 756x756 "
        "image."
    ),
    prior=0.92,
)


# Contradiction (ii): more tokens = better foil vs the 81-KV-entry result
contra_more_tokens_vs_81kv = contradiction(
    claim_more_tokens_is_better,
    claim_cross_benchmark_outperformance,
    reason=(
        "These two cannot both be true. The foil "
        "(@claim_more_tokens_is_better) asserts that more visual "
        "tokens reliably improves visual reasoning; but the "
        "cross-benchmark observation "
        "(@claim_cross_benchmark_outperformance) is panel-best on "
        "spatial reasoning at orders-of-magnitude *fewer* visual "
        "KV entries than frontier models. Either the foil's "
        "directional claim is wrong, or the empirical "
        "outperformance is wrong; the source presents the "
        "outperformance as load-bearing evidence against the foil."
    ),
    prior=0.97,
)


# ============================================================================
# s9: limitations
# ============================================================================

strat_lim_trigger_internalization = support(
    [claim_lim_trigger_word_dependency],
    claim_lim_trigger_incomplete_internalization,
    reason=(
        "Trigger-word dependency means primitive emission is "
        "externally specified rather than internally selected "
        "(@claim_lim_trigger_incomplete_internalization): the "
        "definition of a fully internalized policy "
        "(@setup_trigger_word_definition) requires spontaneous "
        "emission, which the observed dependency "
        "(@claim_lim_trigger_word_dependency) does not satisfy."
    ),
    prior=0.9,
    background=[setup_trigger_word_definition],
)

strat_lim_trigger_analogue = support(
    [claim_lim_trigger_incomplete_internalization],
    claim_lim_trigger_analogue_to_armskill,
    reason=(
        "The 'when-to-invoke' problem of trigger dependency "
        "(@claim_lim_trigger_incomplete_internalization) recurs "
        "across LLM systems whose training signal rewards correct "
        "*invocation* but not correct *timing*. Tool-use agents "
        "and the ARM Execution / Skill modality face the same "
        "structural limit (@claim_lim_trigger_analogue_to_"
        "armskill)."
    ),
    prior=0.78,
)

strat_lim_topology_tradeoff = support(
    [
        claim_lim_topology_weakness,
        claim_task_accuracy_rm,
    ],
    claim_lim_topology_sharpening_tradeoff,
    reason=(
        "Topology generalization weakness "
        "(@claim_lim_topology_weakness) instantiates the classic "
        "RL sharpening-vs-generalization tradeoff "
        "(@claim_lim_topology_sharpening_tradeoff): the per-task "
        "accuracy RM (@claim_task_accuracy_rm), especially the "
        "maze decomposition into exploration progress + wall "
        "violation + path validity, is precisely the kind of "
        "fine-grained reward shaping that sharpens in-domain "
        "performance at the cost of OOD transfer."
    ),
    prior=0.86,
    background=[setup_topology_generalization],
)

strat_lim_synthesis = support(
    [
        claim_lim_trigger_incomplete_internalization,
        claim_lim_topology_sharpening_tradeoff,
    ],
    claim_lim_synthesis_two_open_problems,
    reason=(
        "The two open problems (@claim_lim_synthesis_two_open_"
        "problems) -- when-to-point and topology-agnostic "
        "shaping -- summarize the two limitation interpretations "
        "(@claim_lim_trigger_incomplete_internalization, "
        "@claim_lim_topology_sharpening_tradeoff). Both are "
        "limitations of the current training recipe rather than "
        "of the architectural idea."
    ),
    prior=0.9,
)


# ============================================================================
# s10: pipeline alignment with DeepSeek-OCR 2 + meta-thesis
# ============================================================================

strat_alignment_problem = support(
    [claim_natural_language_imprecise_in_continuous_space],
    claim_alignment_problem_axis,
    reason=(
        "Both works target *organizational* failures of the "
        "vision-language interface "
        "(@claim_alignment_problem_axis): OCR 2 (@setup_ocr2_role) "
        "rejects raster-scan as a non-semantic reading order, and "
        "Visual Primitives addresses the referential imprecision "
        "of natural language (@claim_natural_language_imprecise_"
        "in_continuous_space)."
    ),
    prior=0.88,
    background=[setup_ocr2_role],
)

strat_alignment_solution = support(
    [claim_method_lift_to_thought_unit],
    claim_alignment_solution_axis,
    reason=(
        "Both solutions replace fixed lossy interfaces with "
        "learned content-adaptive ones "
        "(@claim_alignment_solution_axis): OCR 2 learns a Causal "
        "Flow over patches (@setup_ocr2_role); Visual Primitives "
        "lifts coordinates to thought-units in CoT "
        "(@claim_method_lift_to_thought_unit)."
    ),
    prior=0.88,
    background=[setup_ocr2_role],
)

strat_alignment_compression = support(
    [claim_end_to_end_7056x],
    claim_alignment_compression_axis,
    reason=(
        "Both works pair aggressive compression with learned "
        "organization (@claim_alignment_compression_axis): OCR 2 "
        "matches Gemini-1.5 Pro at 256-1120 tokens "
        "(@setup_ocr2_role); Visual Primitives surpasses "
        "GPT-5.4 / Claude 4.6 at ~81 KV entries "
        "(@claim_end_to_end_7056x)."
    ),
    prior=0.88,
    background=[setup_ocr2_role],
)

strat_alignment_means = support(
    [claim_architecture_table],
    claim_alignment_means_axis,
    reason=(
        "Mechanically, OCR 2 uses two stacked 1D causal flows "
        "(@setup_ocr2_role), Visual Primitives uses 3x3 patch "
        "merge plus 4x CSA (@claim_architecture_table); the "
        "mechanisms differ but they deliver the same property "
        "(@claim_alignment_means_axis) -- few but well-organized "
        "visual tokens."
    ),
    prior=0.88,
    background=[setup_ocr2_role],
)

strat_alignment_table = support(
    [
        claim_alignment_problem_axis,
        claim_alignment_solution_axis,
        claim_alignment_compression_axis,
        claim_alignment_means_axis,
    ],
    claim_alignment_table,
    reason=(
        "The four-row alignment table (@claim_alignment_table) is "
        "the tabular presentation of the four axis claims "
        "(@claim_alignment_problem_axis, "
        "@claim_alignment_solution_axis, "
        "@claim_alignment_compression_axis, "
        "@claim_alignment_means_axis)."
    ),
    prior=0.93,
)

strat_meta_thesis = support(
    [
        claim_alignment_compression_axis,
        claim_alignment_means_axis,
        claim_information_density_over_volume,
    ],
    claim_meta_thesis_organization_over_volume,
    reason=(
        "The shared meta-thesis 'organization > volume' "
        "(@claim_meta_thesis_organization_over_volume) is what "
        "both works embody: the compression axis "
        "(@claim_alignment_compression_axis) plus the means axis "
        "(@claim_alignment_means_axis) deliver few-but-well-"
        "organized tokens, which is the operational form of "
        "density-over-volume (@claim_information_density_over_"
        "volume)."
    ),
    prior=0.9,
)

strat_complete_pipeline = support(
    [claim_method_lift_to_thought_unit],
    claim_complete_pipeline,
    reason=(
        "The complete vision-language pipeline "
        "(@claim_complete_pipeline) is the composition of OCR 2 "
        "as front-end encoder (@setup_ocr2_role), V4-Flash MoE "
        "as comprehension stage (@setup_v4_flash_backbone), and "
        "Visual Primitives as back-end reasoner "
        "(@claim_method_lift_to_thought_unit)."
    ),
    prior=0.86,
    background=[setup_ocr2_role, setup_v4_flash_backbone],
)

strat_opposition_to_industry = support(
    [
        claim_meta_thesis_organization_over_volume,
        claim_alignment_compression_axis,
    ],
    claim_opposition_to_industry,
    reason=(
        "OCR 2 and Visual Primitives jointly oppose the frontier "
        "'preserve more visual tokens' default "
        "(@claim_opposition_to_industry) because both achieve "
        "frontier-or-better with much higher compression "
        "(@claim_alignment_compression_axis), and both embody "
        "the meta-thesis (@claim_meta_thesis_organization_over_"
        "volume) that organization beats volume."
    ),
    prior=0.9,
)

strat_tldr_pipeline_alignment = support(
    [claim_alignment_table, claim_complete_pipeline],
    claim_tldr_pipeline_alignment,
    reason=(
        "TL;DR-5 (@claim_tldr_pipeline_alignment) -- pipeline "
        "alignment with OCR 2 -- summarizes the alignment table "
        "(@claim_alignment_table) and the composition of the "
        "complete pipeline (@claim_complete_pipeline)."
    ),
    prior=0.93,
)


__all__ = [
    "claim_alt_trivial_confounds",
    "abd_central",
    "abd_compare",
    "abd_h",
    "abd_alt",
    "ind_three_benchmarks",
    "ind_pixmo_maze",
    "contra_reference_vs_perception",
    "contra_more_tokens_vs_81kv",
]
