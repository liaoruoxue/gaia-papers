"""Priors for independent (leaf) claims in the 2603.17305 CRAFT formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables and figures (Tables 1-3,
  Fig. 4)** -- 0.92-0.95. Each is a directly measured benchmark score
  reported with explicit 3-seed averaging and variance <= 0.2%; the modest
  discount reflects evaluation-protocol noise (GPT-4o automatic safety
  evaluator, prompt-template effects).
* **Theorem assumptions (Assumption 5.1, 5.2, 5.3)** -- 0.9-0.95. Standard
  regularity assumptions for proofs of policy-optimization convergence and
  local-controllability; well-motivated and broadly accepted in the
  literature.
* **Method-description claims** for the six baselines (SafeChain / RealSafe /
  STAR / SafeKey / IPO / ReasoningShield) -- 0.9-0.94. Author-stated
  characterizations of competing methods, drawn directly from those papers.
* **Empirical observations** (latent separation in Fig. 2, rethink at
  boundary, advanced jailbreaks robustness) -- 0.88-0.92. Direct readings
  of figures with appropriate caveats for visualization fidelity.
* **Hypothesis / alternative in the central abduction**:
  - `claim_pred_latent_explains` -- 0.5 (prediction; comparison strategy
    carries the discriminating signal).
  - `claim_pred_alt_compute` -- 0.5 (prediction; comparison strategy
    carries the discriminating signal).
  - In `s10_wiring`, `s_alt_supports_obs` is given prior=0.25, capturing
    the explanatory-power deficit of the compute / data alternative for
    the cross-model + ablation observation.
* **Foil claims** (`claim_foil_output_alignment_sufficient`,
  `claim_foil_grpo_alone_sufficient`) -- 0.3. Set low because they are
  contradicted by the empirical data (catastrophic LCLR ablation) and the
  theorem (R_cons-essentiality), respectively. The contradiction operators
  carry the BP signal.
* **Limitations / caveats** -- 0.9-0.94. Author-acknowledged and well
  documented; treated as well-attested factual claims.
* **SSA Definition** -- 0.95. Mathematical definition of the failure mode;
  not really questionable as a definition but kept as a claim because the
  paper attributes empirical signature to it (it is not a setting because
  the operationalization could be questioned).
"""

from .motivation import (
    claim_lrm_safety_underexplored,
)
from .s2_related_work import (
    claim_guard_models,
    claim_inference_time_defenses,
    claim_ipo_method,
    claim_lrm_strong_reasoning,
    claim_other_training_methods,
    claim_realsafe_method,
    claim_reasoningshield_method,
    claim_safechain_method,
    claim_safekey_method,
    claim_star_method,
)
from .s3_setup import (
    claim_rethink_at_boundary,
    claim_safe_unsafe_separation,
)
from .s4_method import (
    claim_lclr_design_rationale,
    claim_three_rewards_address_distinct_objectives,
)
from .s5_theory import (
    claim_assumption_continuity,
    claim_assumption_fixed_evaluator,
    claim_assumption_grpo_local_opt,
    claim_ssa_definition,
)
from .s6_main_results import (
    claim_table1_full,
    claim_table2_full,
)
from .s7_avg_improvements import (
    claim_advanced_jailbreaks_robustness,
)
from .s8_ablations import (
    claim_ablation_full_table,
)
from .s9_discussion_limitations import (
    claim_lim_fixed_evaluator,
    claim_lim_misuse_potential,
    claim_lim_pca_visualization_evidence,
    claim_lim_training_budget,
    claim_lim_two_models,
    claim_pred_alt_compute,
    claim_pred_latent_explains,
)


PRIORS: dict = {
    # --------------------------------------------------------------------
    # Empirical tables (3-seed means, <=0.2% variance reported)
    # --------------------------------------------------------------------
    claim_table1_full: (
        0.94,
        "Table 1 reports per-method, per-LRM, per-benchmark jailbreak "
        "scores averaged over 3 seeds with <= 0.2% variance; the values "
        "are directly measured StrongReject scores and GPT-4o-evaluated "
        "reasoning-safety rates.",
    ),
    claim_table2_full: (
        0.94,
        "Table 2 reports per-method, per-LRM, per-benchmark Pass@1 "
        "scores averaged over 3 seeds with <= 0.2% variance; standard "
        "math/code benchmark evaluation.",
    ),
    claim_ablation_full_table: (
        0.94,
        "Table 3 reports the per-component ablation with 3-seed averaging "
        "and consistent variance reporting; the per-row deltas are "
        "directly measurable.",
    ),
    claim_advanced_jailbreaks_robustness: (
        0.92,
        "Figure 4 reports ASR under GPTFuzzer + AutoDAN attacks; values "
        "directly readable from the bar chart with the specific scores "
        "labeled (93.62% / 27.96% / 40.43% / 4.00% on GPTFuzzer; "
        "94.17% / 24.52% / 60.28% / 10.21% on AutoDAN).",
    ),

    # --------------------------------------------------------------------
    # Latent-separation observations (Fig. 2)
    # --------------------------------------------------------------------
    claim_safe_unsafe_separation: (
        0.9,
        "PCA projection in Fig. 2 visibly separates safe and unsafe "
        "clusters in both backbone models. Slight discount reflects the "
        "limitation that 2D PCA is a linear projection that may not "
        "fully capture the latent geometry.",
    ),
    claim_rethink_at_boundary: (
        0.88,
        "Visual readability of rethink concentration at the safe/unsafe "
        "boundary in Fig. 2; the qualitative pattern is clear, with the "
        "PCA-fidelity caveat applied.",
    ),

    # --------------------------------------------------------------------
    # Theorem assumptions (standard regularity)
    # --------------------------------------------------------------------
    claim_ssa_definition: (
        0.95,
        "Definition 5.1 formalizes SSA as p_y close to 1 with "
        "|p_z - p_y| >= delta; the operationalization is mathematically "
        "well-defined and matches the empirical SSA pattern documented "
        "in prior literature (Zhang et al. 2025b, Li et al. 2025a).",
    ),
    claim_assumption_continuity: (
        0.92,
        "Lipschitz continuity holds for any finite-weight neural "
        "network; local controllability is satisfied for sufficiently "
        "expressive policy classes -- standard regularity. Modest "
        "discount because controllability claims for very small "
        "epsilon may be hard to verify in practice for specific "
        "checkpoints.",
    ),
    claim_assumption_grpo_local_opt: (
        0.9,
        "Standard convergence assumption for policy optimization "
        "analysis; GRPO converges in practice on the regimes the paper "
        "evaluates, but global optima are not guaranteed -- the "
        "assumption is the local-optimum condition only.",
    ),
    claim_assumption_fixed_evaluator: (
        0.95,
        "Standard practice during alignment training: P(S|y) is held "
        "fixed during policy optimization; trivially satisfied by the "
        "experimental setup.",
    ),

    # --------------------------------------------------------------------
    # LCLR design rationale (interpretive but well-motivated)
    # --------------------------------------------------------------------
    claim_lclr_design_rationale: (
        0.88,
        "The three-loss design rationale is interpretive: each loss is "
        "claimed to address a distinct failure mode; the ablation "
        "(Table 3) supports this directly, and the rationale matches "
        "established contrastive-learning practice (SimCLR, etc.).",
    ),
    claim_three_rewards_address_distinct_objectives: (
        0.9,
        "The three-reward design is similarly interpretive; the "
        "ablation supports each reward contributing materially.",
    ),

    # --------------------------------------------------------------------
    # Baseline method descriptions
    # --------------------------------------------------------------------
    claim_safechain_method: (
        0.92,
        "SafeChain's SFT-based design and use of curated safe CoT "
        "trajectories are documented in Jiang et al. 2025b.",
    ),
    claim_realsafe_method: (
        0.92,
        "RealSafe-R1's use of distilled R1 safety reasoning traces is "
        "documented in Zhang et al. 2025c.",
    ),
    claim_star_method: (
        0.92,
        "STAR's self-generated policy-aligned reasoning trace fine-"
        "tuning is documented in Wang et al. 2025e.",
    ),
    claim_safekey_method: (
        0.92,
        "SafeKey's extension of STAR with additional supervision "
        "signals is documented in Zhou et al. 2025b.",
    ),
    claim_ipo_method: (
        0.93,
        "IPO's intervention-based preference optimization design is "
        "documented in Zhang et al. 2025b; IPO is the strongest "
        "output-side baseline in Table 1.",
    ),
    claim_reasoningshield_method: (
        0.91,
        "ReasoningShield's safety detection over reasoning traces is "
        "documented in Li et al. 2025a; functions as guard model "
        "rather than training-time aligner.",
    ),
    claim_other_training_methods: (
        0.9,
        "Deliberative Alignment, SaRO, STAIR, R2D, ERPO -- "
        "characterizations from their respective papers; all operate "
        "over textual reasoning traces, not latent representations.",
    ),
    claim_inference_time_defenses: (
        0.9,
        "Survey-style summary of inference-time defenses; the "
        "characterization (reactive, no training-time alignment) is "
        "well-supported by Wang et al. 2025a survey.",
    ),
    claim_guard_models: (
        0.9,
        "ReasoningShield, ThinkGuard, GuardReasoner -- all post-hoc "
        "detectors per their respective papers.",
    ),

    # --------------------------------------------------------------------
    # LRM landscape claim
    # --------------------------------------------------------------------
    claim_lrm_strong_reasoning: (
        0.95,
        "Strong LRM math/logic performance attested across DeepSeek-R1, "
        "Qwen3, OpenAI o1, Phi-4-Reasoning, GPT-4o; well documented and "
        "uncontroversial.",
    ),
    claim_lrm_safety_underexplored: (
        0.85,
        "Comparative claim: safety-of-LRMs is less studied than "
        "reasoning ability. Supported by recent surveys "
        "(Wang et al. 2025a) but a softer comparative claim that "
        "could be questioned.",
    ),

    # --------------------------------------------------------------------
    # Limitations (author-acknowledged)
    # --------------------------------------------------------------------
    claim_lim_two_models: (
        0.94,
        "Two-LRM scope is acknowledged in the paper's Sec. 7 / "
        "Limitations; trivially verifiable from Table 1.",
    ),
    claim_lim_training_budget: (
        0.92,
        "On R1-Distill-Llama-8B, IPO outperforms CRAFT on JBB "
        "Reasoning (0.057 vs 0.065) and SR Reasoning (0.167 vs 0.172) "
        "-- per-cell facts directly readable from Table 1.",
    ),
    claim_lim_fixed_evaluator: (
        0.92,
        "Structural limitation: P(S|y) is fixed by Assumption 5.3 "
        "and inherits StrongReject + GPT-4o weaknesses; standard "
        "limitation of RL-from-AI-feedback.",
    ),
    claim_lim_misuse_potential: (
        0.9,
        "Dual-use disclosure in the Impact Statement; standard "
        "concern for safety-alignment techniques.",
    ),
    claim_lim_pca_visualization_evidence: (
        0.9,
        "PCA caveat: 2D linear projection may not capture full latent "
        "geometry; the qualitative separation is shown but high-"
        "dimensional structure is not characterized.",
    ),

    # --------------------------------------------------------------------
    # Central abduction: hypothesis vs alternative predictions
    # --------------------------------------------------------------------
    claim_pred_latent_explains: (
        0.5,
        "Prediction; the comparison strategy plus the cross-model + "
        "ablation observation carry the discriminating signal.",
    ),
    claim_pred_alt_compute: (
        0.5,
        "Prediction; the comparison strategy plus the cross-model + "
        "ablation observation carry the discriminating signal.",
    ),
}
