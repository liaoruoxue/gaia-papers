"""Priors for independent (leaf) claims in the 2601.08129 pressure-field
formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables** (Tables 3-13:
  per-strategy / per-difficulty / per-tier solve rates, token usage,
  ablations, scaling, convergence speed, final pressure) -- 0.93-0.95.
  Each is a directly measured experimental value with explicit Wilson
  CIs, sample sizes, and statistical tests. The prior is high because
  the trials were deterministically seeded (Appendix A.5) and Rust +
  Ollama infrastructure makes transcription mechanical.
* **Algorithm/architectural-property claims** (algorithm three
  properties, alignment-separability under the chosen pressure
  function, escalation = exploit/explore) -- 0.92-0.95. These are
  read directly off algorithm and pressure-function design and are
  structurally certain modulo design-faithfulness assumptions.
* **Method-description claims for related-work / baseline
  characterizations** (organizational paradigms / GPGP / SharedPlans /
  Joint Intentions / FM-capability claims / MAS-LLM baselines /
  centralized-hierarchical-message-passing complexities) -- 0.88-0.92.
  Author-stated paraphrases of competing methods drawn from those
  papers directly.
* **Headline empirical pattern claims** (effect sizes large) -- 0.95.
  Read directly from Cohen's h calculations on the per-tier table.
* **Predicted-fingerprint claims for the central abduction**
  (constraint-driven-emergence vs better-prompting) -- pi(H) = 0.55,
  pi(Alt) = 0.2. The alternative's pi(Alt) is the probability that
  better-prompting / more-compute *alone* explains the observed four-
  fact fingerprint, NOT whether better prompting improves
  performance in general. Since better-prompting predicts the
  *opposite* signs for two of the four facts (gap-narrows-with-
  difficulty rather than widens; more-compute should help when
  scaling agents), pi(Alt) is held substantially below pi(H).
* **Pressure-field central proposal** -- 0.85. The method itself is
  described and instantiated; the prior reflects "this is a real,
  well-defined coordination scheme" rather than its empirical
  performance (which is judged by other claims in the graph).
* **Contradictory literature-implied premises**
  (claim_explicit_orchestration_is_necessary,
  claim_coordination_overhead_unavoidable) -- 0.5. These are the
  literature-attributed positions the paper *contradicts*; the
  contradictions push them low via BP, so we set them at uninformative
  0.5 and let the operators discriminate.
* **Pressure-field demonstration / O(1)+convergence claim** -- 0.95.
  These are direct readouts from the empirical / theoretical results
  packaged for the contradiction operator.
* **Central-design-questions / locality-formal claims** -- 0.9. Direct
  readouts of the formalism.
"""

from .motivation import (
    claim_explicit_orchestration_paradigm,
    claim_pressure_field_proposal,
)
from .s2_related_work import (
    claim_organizational_paradigms_assign_roles,
    claim_malone_crowston_shared_resource,
    claim_gpgp_message_complexity,
    claim_sharedplans_joint_intentions_cost,
    claim_fm_capability_1_domain_general_patches,
    claim_fm_capability_2_instruction_following,
    claim_fm_capability_3_zero_shot_quality,
    claim_fm_capability_4_in_context_pheromone,
    claim_fm_capability_5_generative_flexibility,
    claim_mas_llm_baselines_share_pattern,
    claim_explicit_orchestration_scaling_failures,
    claim_distributed_gd_requires_protocols,
)
from .s3_problem_formulation import (
    claim_central_design_questions,
)
from .s4_method import (
    claim_algorithm_three_properties,
)
from .s5_theoretical_analysis import (
    claim_centralized_complexity,
    claim_hierarchical_complexity,
    claim_message_passing_complexity,
)
from .s6_experiments_setup import (
    claim_alignment_separability,
)
from .s6b_main_results import (
    claim_table_3_aggregate_solve_rates,
    claim_effect_sizes_large,
    claim_table_9_convergence_speed,
    claim_table_10_final_pressure,
    claim_table_11_token_per_trial,
    claim_table_13_solved_unsolved_split,
)
from .s6c_ablations import (
    claim_table_5_full_ablation,
    claim_table_6_scaling,
    claim_escalation_implements_exploitation_exploration,
)
from .s6d_difficulty_breakdown import (
    claim_table_8_difficulty_breakdown,
    claim_easy_pressure_field_86_7,
    claim_easy_conversation_33_3,
    claim_easy_hierarchical_4_4,
)
from .s7_discussion import (
    claim_limitation_domain_specificity,
)
from .s11_wiring import (
    claim_pred_h_constraint_driven_emergence,
    claim_pred_alt_better_prompting,
    claim_pressure_field_demonstration,
    claim_o1_overhead_with_convergence,
    claim_explicit_orchestration_is_necessary,
    claim_coordination_overhead_unavoidable,
)


PRIORS: dict = {
    # -----------------------------------------------------------------
    # Tables 3-13: per-strategy / per-difficulty empirical readouts
    # -----------------------------------------------------------------
    claim_table_3_aggregate_solve_rates: (
        0.95,
        "Table 3: aggregate solve rates across 1350 trials (270 per "
        "strategy). Pressure-field 48.5%, conversation 11.1%, "
        "hierarchical 1.5%, sequential 0.4%, random 0.4%, with "
        "Wilson CIs and chi-square test (chi^2 > 200, p < 0.001). "
        "Direct measurement under deterministic seeding (Appendix "
        "A.5) and identical fairness controls.",
    ),
    claim_table_8_difficulty_breakdown: (
        0.95,
        "Table 8: per-difficulty solve rates (90 trials each tier per "
        "strategy). Pressure-field 86.7% / 43.3% / 15.6%; all "
        "baselines 0% on medium and hard. Direct measurement.",
    ),
    claim_easy_pressure_field_86_7: (
        0.95,
        "Easy-tier observation: pressure-field 78/90 = 86.7%. Cell "
        "value of Table 8 with consistent reproduction in Table 5 "
        "ablation matrix.",
    ),
    claim_easy_conversation_33_3: (
        0.95,
        "Easy-tier observation: conversation 30/90 = 33.3%. Cell "
        "value of Table 8.",
    ),
    claim_easy_hierarchical_4_4: (
        0.95,
        "Easy-tier observation: hierarchical 4/90 = 4.4%. Cell value "
        "of Table 8.",
    ),
    claim_table_5_full_ablation: (
        0.93,
        "Table 5: 5-row x 30-trial ablation matrix on easy. Decay "
        "+10pp / inhibition +0pp / examples +6.7pp single-feature "
        "contributions. Per-row 30 trials with deterministic seeding; "
        "the prior is high but reflects the breadth (more cells = "
        "more chances for transcription error).",
    ),
    claim_table_6_scaling: (
        0.93,
        "Table 6: scaling experiment (30 trials each at 1/2/4 agents "
        "on easy). 83.3% / 93.3% / 83.3% with Wilson CIs all "
        "overlapping. Direct measurement.",
    ),
    claim_table_9_convergence_speed: (
        0.93,
        "Table 9: average ticks-to-solution among solved cases. "
        "Pressure-field 17.8 / 34.6 / 32.3 across difficulty tiers; "
        "conversation 29.4 (easy only); hierarchical 40.0 (easy "
        "only). The n's are small (4-78) but readouts are "
        "deterministic given the seeded trials.",
    ),
    claim_table_10_final_pressure: (
        0.93,
        "Table 10: average final pressure across difficulty tiers. "
        "200x / 57x / 35x lower for pressure-field vs baselines. "
        "Direct readout of the seeded-trial pressure histories.",
    ),
    claim_table_11_token_per_trial: (
        0.93,
        "Table 11: token-per-trial averages across all 270 trials "
        "per strategy. Direct measurement; pressure-field consumes "
        "~4x more tokens per trial than conversation.",
    ),
    claim_table_13_solved_unsolved_split: (
        0.93,
        "Table 13: token usage split by outcome (solved vs unsolved "
        "trials) for pressure-field and conversation. Direct "
        "measurement.",
    ),
    claim_effect_sizes_large: (
        0.95,
        "Cohen's h effect sizes h = 1.16-2.18 for pressure-field vs "
        "each baseline on easy problems. Computed deterministically "
        "from Table 8's solve rates; the all-greater-than-0.8 "
        "(large-effect) characterization is standard Cohen's-h "
        "interpretation.",
    ),

    # -----------------------------------------------------------------
    # Algorithm / architectural-property claims (read off design)
    # -----------------------------------------------------------------
    claim_algorithm_three_properties: (
        0.95,
        "Algorithm 1's three properties (locality / bounded "
        "parallelism / decay-driven exploration) are read directly "
        "off the algorithm's pseudocode (Algorithm 1, page 18). "
        "Structurally certain.",
    ),
    claim_alignment_separability: (
        0.95,
        "Per-region pressure separability (epsilon = 0) is read "
        "directly off the meeting-pressure function design "
        "(Section 6.1.1, Appendix B.1): gaps / overlaps / util_var "
        "are per-block local; unsched is added to total pressure "
        "only. The 9,873-transition empirical validation (0 "
        "pressure-degradation events) is independent confirmation; "
        "the prior is high because the property is structural, not "
        "merely observed.",
    ),
    claim_escalation_implements_exploitation_exploration: (
        0.92,
        "Escalation as exploit/explore is read directly off the "
        "band-escalation (Exploitation/Balanced/Exploration sampling "
        "params, Section 6.1.4) and model-escalation (0.5b->1.5b->3b "
        "after 21 ticks at high pressure) design. Structural fact.",
    ),
    claim_central_design_questions: (
        0.92,
        "The four central design questions (existence / quality / "
        "convergence / decentralization) are stated directly in "
        "Section 3.4 as the formalism's research agenda. Direct "
        "extraction; high-confidence.",
    ),

    # -----------------------------------------------------------------
    # Related-work / baseline characterizations (literature paraphrases)
    # -----------------------------------------------------------------
    claim_organizational_paradigms_assign_roles: (
        0.9,
        "Author paraphrase of Horling-Lesser 2004 + Dignum 2009 -- "
        "all 9 surveyed organizational paradigms assign explicit "
        "roles. The cited surveys are direct sources; prior reflects "
        "small risk of paraphrase loss.",
    ),
    claim_malone_crowston_shared_resource: (
        0.88,
        "Author paraphrase of Malone-Crowston 1994's shared-resource "
        "coordination pattern, instantiated by pressure-field's "
        "artifact-as-resource design. The instantiation argument is "
        "the contribution; the underlying Malone-Crowston pattern is "
        "well-established in coordination theory.",
    ),
    claim_gpgp_message_complexity: (
        0.92,
        "Author paraphrase of GPGP [@GPGP] message complexity "
        "(O(n^2) pairwise / O(n log n) hierarchical aggregation). "
        "These are well-established results in the GPGP literature.",
    ),
    claim_sharedplans_joint_intentions_cost: (
        0.9,
        "Author paraphrase of SharedPlans [@SharedPlans] and Joint "
        "Intentions [@JointIntentions] mutual-belief requirements. "
        "Well-established in the joint-activity literature.",
    ),
    claim_fm_capability_1_domain_general_patches: (
        0.92,
        "Author claim that FMs' broad pretraining enables domain-"
        "general patch proposal. Supported by widely-observed FM "
        "behavior across code, text, structured data; direct "
        "empirical observation in the experimental task.",
    ),
    claim_fm_capability_2_instruction_following: (
        0.92,
        "Author claim that FMs' instruction-following capability "
        "lets them operate from natural-language pressure "
        "descriptions. Standard FM property; the experimental "
        "deployment confirms it.",
    ),
    claim_fm_capability_3_zero_shot_quality: (
        0.9,
        "Author claim that FMs zero-shot identify constraint "
        "violations. Standard FM behavior; well-supported in the "
        "scheduling task (model proposes patches without scheduling-"
        "specific training).",
    ),
    claim_fm_capability_4_in_context_pheromone: (
        0.9,
        "Author claim that FMs' in-context learning implements "
        "pheromone memory naturally. Direct application of standard "
        "few-shot prompting to the stigmergic positive-pheromone "
        "mechanism.",
    ),
    claim_fm_capability_5_generative_flexibility: (
        0.92,
        "Author claim that FMs generate from effectively continuous "
        "spaces, in contrast to ACO's discrete enumerated spaces. "
        "Standard FM property contrasting with classical stigmergic "
        "systems.",
    ),
    claim_mas_llm_baselines_share_pattern: (
        0.92,
        "Author paraphrase that AutoGen / MetaGPT / CAMEL / CrewAI "
        "share an explicit-orchestration design pattern. Direct "
        "review of the four cited frameworks; the shared pattern is "
        "well-documented.",
    ),
    claim_explicit_orchestration_paradigm: (
        0.92,
        "Author claim that the dominant MAS-LLM paradigm uses "
        "explicit orchestration borrowed from human organizational "
        "structures. Direct and uncontroversial reading of the "
        "literature.",
    ),
    claim_explicit_orchestration_scaling_failures: (
        0.9,
        "Author claim that explicit-orchestration faces three "
        "scaling failures (bottlenecks, message-overhead growth, "
        "manager-cascade failures). Standard observations in the "
        "MAS literature.",
    ),
    claim_distributed_gd_requires_protocols: (
        0.9,
        "Author claim that distributed GD methods require explicit "
        "communication / synchronization protocols. Standard "
        "characterization of the distributed-optimization "
        "literature.",
    ),
    claim_centralized_complexity: (
        0.92,
        "Author claim that centralized planning is O(m*a) per step "
        "with sequential bottleneck. Standard complexity analysis.",
    ),
    claim_hierarchical_complexity: (
        0.92,
        "Author claim that hierarchical delegation is O(n log n) "
        "with tree-depth latency and manager-failure cascades. "
        "Standard complexity analysis.",
    ),
    claim_message_passing_complexity: (
        0.92,
        "Author claim that message-passing coordination is O(n^2) "
        "in the worst case, partition-sensitive. Standard "
        "complexity analysis.",
    ),

    # -----------------------------------------------------------------
    # Pressure-field central proposal
    # -----------------------------------------------------------------
    claim_pressure_field_proposal: (
        0.88,
        "The pressure-field proposal -- shared artifact + local "
        "pressure gradients + temporal decay, O(1) coordination -- "
        "is described concretely and instantiated in the open-"
        "source Rust experiment. The prior reflects 'this is a "
        "real, well-defined coordination scheme' (its empirical "
        "performance is judged by Table 3, etc., not by this claim "
        "directly).",
    ),

    # -----------------------------------------------------------------
    # Limitations
    # -----------------------------------------------------------------
    claim_limitation_domain_specificity: (
        0.85,
        "The domain-specificity limitation -- meeting-room "
        "scheduling may not generalize to domains lacking locality -- "
        "is a self-reported caveat, supported by the paper's own "
        "argument that meeting scheduling is representative of "
        "resource-allocation problems with soft constraints. Prior "
        "reflects appropriate hedging.",
    ),

    # -----------------------------------------------------------------
    # Central abduction: prediction priors
    # -----------------------------------------------------------------
    claim_pred_h_constraint_driven_emergence: (
        0.7,
        "The 'constraint-driven emergence' hypothesis predicts a "
        "specific four-fact fingerprint (same-substrate 30x, gap-"
        "widens, decay-benefit, scaling-flat). pi(H) = 0.7 -- the "
        "hypothesis is well-motivated by the potential-game theory "
        "(Theorems 5.1-5.5), each of the four facts follows by "
        "direct theoretical implication, and the empirical "
        "fingerprint reproduces every signed prediction.",
    ),
    claim_pred_alt_better_prompting: (
        0.15,
        "The 'better-prompting / more-compute / better-evaluation' "
        "alternative is held at low pi(Alt) = 0.15 because: (i) the "
        "fairness controls (identical FM substrate, identical 50-"
        "tick budget, identical prompts and parsing) explicitly "
        "rule out 'better prompting' or 'more compute' as primary "
        "drivers; (ii) Alt predicts the *opposite signs* on at "
        "least two of the four facts (gap-narrows with difficulty; "
        "scaling agents should add throughput). Per the skill: "
        "pi(Alt) = probability Alt alone *explains* the observed "
        "fingerprint, NOT whether better prompting helps in "
        "general. Both are observably violated in the data, so "
        "pi(Alt) is low.",
    ),

    # -----------------------------------------------------------------
    # Contradiction operands
    # -----------------------------------------------------------------
    claim_explicit_orchestration_is_necessary: (
        0.5,
        "Literature-implied position the paper contradicts. We set "
        "this at uninformative 0.5 and let the contradiction "
        "operator (with claim_pressure_field_demonstration on the "
        "other side) discriminate via BP propagation.",
    ),
    claim_pressure_field_demonstration: (
        0.95,
        "The empirical demonstration that orchestration-free "
        "pressure-field outperforms explicit orchestration on the "
        "270-trial-per-strategy benchmark. Direct readout of "
        "Tables 3 and 8 with statistical tests; high-confidence.",
    ),
    claim_coordination_overhead_unavoidable: (
        0.5,
        "Literature-implied position the paper contradicts. We set "
        "this at uninformative 0.5 and let the contradiction "
        "operator (with claim_o1_overhead_with_convergence on the "
        "other side) discriminate via BP propagation.",
    ),
    claim_o1_overhead_with_convergence: (
        0.95,
        "The pressure-field result: O(1) coordination overhead "
        "(Theorem 5.4) plus convergence guarantees (Theorems 5.1, "
        "5.5). Direct package of theorem statements with empirical "
        "confirmation; high-confidence.",
    ),
}
