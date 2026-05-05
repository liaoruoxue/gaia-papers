"""Priors for independent (leaf) claims in the 2604.23747 SFT-then-RL formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables (1-6) and figures (1-3)**
  -- 0.92-0.96. Each is a directly measured benchmark / FLOPs / training-
  curve value reported with explicit standard deviations across 3 seeds; the
  modest discount reflects evaluation-protocol noise (Math-Verify
  variance, prompt template effects).
* **Bug-mechanism claims** (CPU-offload optimizer mechanism, loss-aggregation
  mechanism) -- 0.95-0.96. These are statements about the source code of
  released open-source frameworks (DeepSpeed, OpenRLHF) and have been
  independently validated through merged upstream patches.
* **Method-description claims** (LUFFY / ReLIFT / SRFT / Prefix-RFT / HPT)
  -- 0.9-0.95. Author-stated characterizations of competing methods,
  drawn from those papers directly.
* **Mixed-policy results tables** (Qwen + Llama mixed-policy reported scores)
  -- 0.92. These are reported by competing systems; subject to those
  systems' measurement protocols and any framework-bug effects on their
  *own* SFT baselines.
* **Hypothesis / alternative in the central abduction**:
  - `claim_alt_methodological_advance` -- 0.25. Explanatory power for
    the cross-framework match observation is weak: the alternative
    cannot easily explain why two independent SFT stacks converge to
    the same ~54 score *only* after the two specific bug fixes.
    pi(Alt) here is "Can Alt alone explain Obs?", not "Is Alt's
    reasoning correct?".
* **Foil for contradiction-2 (`claim_optimizer_bug_cosmetic`)** -- 0.3.
  Contradicted by the +5.1 measured deflation, the suppressed gradient
  norm trace, and the cross-framework match.
"""

from .motivation import (
    claim_intuitive_motivation_for_mixing,
    claim_mixed_policy_gains_reported,
)
from .s10_wiring import (
    claim_optimizer_bug_cosmetic,
)
from .s2_related_work import (
    claim_hpt_method,
    claim_luffy_method,
    claim_other_mixed_policy_methods,
    claim_prefix_rft_method,
    claim_relift_method,
    claim_srft_method,
)
from .s3_setup import (
    claim_chat_template_unified,
    claim_luffy_relift_reimpl,
    claim_reproduction_design,
)
from .s4_optimizer_bug import (
    claim_bug_introduced_in_pr,
    claim_bug_mechanism,
    claim_optimizer_fix,
)
from .s5_loss_aggregation_bug import (
    claim_loss_agg_fix,
    claim_loss_agg_mechanism,
)
from .s6_attribution import (
    claim_baseline_openrlhf,
    claim_hyperparam_sensitivity,
    claim_row_both,
    claim_row_loss_agg_only,
    claim_row_optimizer_only,
    claim_row_verl,
)
from .s7_corrected_results import (
    claim_llama_failure_explanation,
    claim_llama_mixed_policy_table,
    claim_qwen_mixed_policy_table,
)
from .s8_truncated_rl import (
    claim_flops_decomposition,
    claim_truncated_id_results,
    claim_truncated_ood_results,
)
from .s9_discussion import (
    claim_alt_methodological_advance,
    claim_entropy_dynamics,
    claim_lim_domain_scope,
    claim_lim_mixed_atop_corrected,
    claim_lim_model_families,
    claim_lim_relift_hpt_unverified,
    claim_pred_alt_explains,
    claim_pred_bug_explains,
    claim_qwen_training_dynamics,
    claim_response_length_dynamics,
)


PRIORS: dict = {
    # --------------------------------------------------------------------
    # Bug mechanisms (open-source code review + upstream-merged PRs)
    # --------------------------------------------------------------------
    claim_bug_mechanism: (
        0.96,
        "Mechanism is verifiable from the DeepSpeed source code at the "
        "affected commit; the bug surfaces as a specific else-branch "
        "around copy_gradients_to_cpu(); the corresponding fix has been "
        "merged upstream as DeepSpeed PR #7967.",
    ),
    claim_loss_agg_mechanism: (
        0.96,
        "Mechanism is verifiable from OpenRLHF/Llama-Factory source "
        "code; the bug class (mean-of-means rather than per-token mean) "
        "is documented by Han and Han (Unsloth blog) and Debut et al. "
        "(HuggingFace blog).",
    ),
    claim_bug_introduced_in_pr: (
        0.95,
        "DeepSpeed PR #6550 commit history (September 2024); a "
        "verifiable provenance claim.",
    ),
    claim_optimizer_fix: (
        0.95,
        "Two-line patch to deepspeed/runtime/zero/stage_1_and_2.py "
        "removing the else-guard around copy_gradients_to_cpu(); "
        "merged upstream as DeepSpeed PR #7967.",
    ),
    claim_loss_agg_fix: (
        0.95,
        "Algorithm 2 (Appendix D) implements the per-token-mean "
        "all-reduce; submitted as OpenRLHF PR #1216; verl already "
        "fixed this in November 2025 (PR #3994).",
    ),

    # --------------------------------------------------------------------
    # Per-row Table 2 measurements (3-seed means and stds)
    # --------------------------------------------------------------------
    claim_baseline_openrlhf: (
        0.93,
        "Table 2 row 1: 48.3 +/- 0.8 across the 6-benchmark subset "
        "(3 seeds, single node).",
    ),
    claim_row_loss_agg_only: (
        0.93,
        "Table 2 row 2: 49.1 +/- 0.9 (3 seeds).",
    ),
    claim_row_optimizer_only: (
        0.93,
        "Table 2 row 3: 53.4 +/- 0.4 (3 seeds; tighter std than baseline).",
    ),
    claim_row_both: (
        0.94,
        "Table 2 row 4: 54.0 +/- 0.2 (3 seeds; tightest std in the table).",
    ),
    claim_row_verl: (
        0.94,
        "Table 2 row 5: 53.8 +/- 0.1 (3 seeds; verl reference).",
    ),

    # --------------------------------------------------------------------
    # Truncated-RL measurements (Table 5)
    # --------------------------------------------------------------------
    claim_truncated_id_results: (
        0.93,
        "Table 5 ID row: 55.6 +/- 0.5 over the 6-benchmark ID subset "
        "(3 seeds).",
    ),
    claim_truncated_ood_results: (
        0.93,
        "Table 5 OOD row: 59.2 +/- 0.2 (3 seeds).",
    ),

    # --------------------------------------------------------------------
    # FLOPs accounting (Appendix B)
    # --------------------------------------------------------------------
    claim_flops_decomposition: (
        0.92,
        "Standard 6ND/8ND scaling-law arithmetic following Hoffmann "
        "et al., Sardana et al.; modest model assumptions on the "
        "average response length (D_data=4,200, D_rollout=2,200/3,000/"
        "4,200 across methods).",
    ),

    # --------------------------------------------------------------------
    # Hyperparameter-sensitivity (Table 3)
    # --------------------------------------------------------------------
    claim_hyperparam_sensitivity: (
        0.93,
        "Table 3 reproduction (3 seeds); Fu et al.'s reported config "
        "yielded 48.3 +/- 0.2, the tuned LUFFY/ReLIFT-style config "
        "yielded 53.8 +/- 0.1, a +5.5-point gap reproducibly "
        "attributable to learning-rate / batch-size / schedule choice.",
    ),

    # --------------------------------------------------------------------
    # Mixed-policy method descriptions
    # --------------------------------------------------------------------
    claim_luffy_method: (
        0.94,
        "LUFFY's regularized importance sampling design and OpenRLHF "
        "SFT stack are documented in [@LUFFY].",
    ),
    claim_relift_method: (
        0.93,
        "ReLIFT's SFT/RL alternation and Llama-Factory SFT stack are "
        "documented in [@ReLIFT].",
    ),
    claim_srft_method: (
        0.93,
        "SRFT's joint SFT+RL loss with adaptive entropy weighting and "
        "the weak-LR (5e-6) SFT config are documented in [@SRFT].",
    ),
    claim_prefix_rft_method: (
        0.93,
        "Prefix-RFT's prefix-sampling design + LUFFY-inherited "
        "baselines documented in [@PrefixRFT].",
    ),
    claim_hpt_method: (
        0.9,
        "HPT's binary SFT-or-GRPO gate documented; SFT setup is *not* "
        "detailed (the bug-attribution assumption is therefore "
        "inference rather than measurement) [@HPT].",
    ),
    claim_other_mixed_policy_methods: (
        0.92,
        "Seven additional mixed-policy methods (UFT, CHORD, SuperRL, "
        "SASR, RED, TemplateRL, MIFO) qualitatively discussed in Sec. 5 "
        "with paraphrases of their abstracts.",
    ),

    # --------------------------------------------------------------------
    # Reported mixed-policy tables
    # --------------------------------------------------------------------
    claim_qwen_mixed_policy_table: (
        0.92,
        "Qwen2.5-Math-7B mixed-policy numbers as reported by "
        "[@LUFFY], [@ReLIFT], [@SRFT], [@PrefixRFT], [@HPT]. "
        "Inherits any framework-bug effects in those papers' own "
        "evaluations of their own methods (which use verl, so are "
        "minimally affected).",
    ),
    claim_llama_mixed_policy_table: (
        0.92,
        "Llama-3.1-8B mixed-policy numbers from the same source "
        "papers; starred entries use a different chat template per "
        "the original works.",
    ),

    # --------------------------------------------------------------------
    # Methodological-design claims
    # --------------------------------------------------------------------
    claim_reproduction_design: (
        0.93,
        "Four-variant progressive bug-fix design at single-node, "
        "3 seeds; sound experimental design that cleanly isolates "
        "per-bug contributions.",
    ),
    claim_luffy_relift_reimpl: (
        0.92,
        "LUFFY/ReLIFT reimplemented in verl with original RL "
        "hyperparameters and the loss-aggregation fix patched into "
        "their training loops; single-seed reports.",
    ),
    claim_chat_template_unified: (
        0.9,
        "Direct empirical observation: when SFT is correctly "
        "implemented, Llama-3.1-8B follows the full Qwen system "
        "prompt without issue. Authors interpret prior 'template-"
        "incompatibility' as a symptom of undertrained SFT.",
    ),

    # --------------------------------------------------------------------
    # Training-dynamics observations (Fig. 3)
    # --------------------------------------------------------------------
    claim_qwen_training_dynamics: (
        0.92,
        "Direct reading of Fig. 3 top-row training-reward curves on "
        "Qwen2.5-Math-7B.",
    ),
    claim_response_length_dynamics: (
        0.9,
        "Direct reading of Fig. 3 middle column (response length).",
    ),
    claim_entropy_dynamics: (
        0.9,
        "Direct reading of Fig. 3 right column (policy entropy).",
    ),

    # --------------------------------------------------------------------
    # Llama failure-mode explanation (interpretive but well-evidenced)
    # --------------------------------------------------------------------
    claim_llama_failure_explanation: (
        0.9,
        "Mechanism-level reading of Fig. 3 dynamics combined with prior "
        "literature on Llama's pre-training distribution "
        "[@SpuriousRewards]; small caveat for interpretive component.",
    ),

    # --------------------------------------------------------------------
    # Mixed-policy literature claim + intuitive motivation
    # --------------------------------------------------------------------
    claim_mixed_policy_gains_reported: (
        0.95,
        "The literature unambiguously reports these gains; this claim "
        "is about the existence of the reports, not their accuracy.",
    ),
    claim_intuitive_motivation_for_mixing: (
        0.85,
        "Conceptual rationale (signal sparsity + complementarity) is "
        "sound; the empirical claim it supports is the one being "
        "questioned, but the reasoning premise is independently "
        "credible.",
    ),

    # --------------------------------------------------------------------
    # Limitations (author-acknowledged caveats)
    # --------------------------------------------------------------------
    claim_lim_domain_scope: (
        0.94,
        "Math-only scope acknowledged in Sec. 6 conclusion + "
        "limitations.",
    ),
    claim_lim_model_families: (
        0.94,
        "Two-model-family limit acknowledged in Sec. 6.",
    ),
    claim_lim_mixed_atop_corrected: (
        0.93,
        "Mixed-policy atop a *correctly trained* SFT remains untested; "
        "carefully framed as a comparison limitation rather than a "
        "thesis weakening.",
    ),
    claim_lim_relift_hpt_unverified: (
        0.93,
        "ReLIFT/HPT SFT configs not released; the bug-attribution "
        "assumption for these two is inference (consistent with their "
        "stated framework choices) rather than direct measurement.",
    ),

    # --------------------------------------------------------------------
    # Central abduction: hypothesis vs alternative
    # --------------------------------------------------------------------
    claim_alt_methodological_advance: (
        0.25,
        "pi(Alt) = explanatory power of the methodological-advance "
        "alternative for the *cross-framework match* observation. Low "
        "because the alternative cannot explain why two independent "
        "SFT stacks (patched OpenRLHF + verl) converge to ~54 *only* "
        "after the two specific bug fixes; under the buggy regime the "
        "two stacks would diverge by ~5.7 points. pi(Alt) here answers "
        "'Can Alt alone explain Obs?', not 'Is Alt internally "
        "coherent?'.",
    ),
    claim_pred_bug_explains: (
        0.5,
        "Prediction; the comparison strategy plus the cross-framework "
        "observation carry the discriminating signal.",
    ),
    claim_pred_alt_explains: (
        0.5,
        "Prediction; the comparison strategy plus the cross-framework "
        "observation carry the discriminating signal.",
    ),

    # --------------------------------------------------------------------
    # Foil for contradiction-2 (the optimizer-cosmetic alternative)
    # --------------------------------------------------------------------
    claim_optimizer_bug_cosmetic: (
        0.3,
        "The optimizer-cosmetic foil is positioned for the "
        "contradiction operator with claim_optimizer_dominates_"
        "attribution. The +5.1-point measured deflation, the "
        "suppressed gradient norms (Fig. 2 right), and the cross-"
        "framework match all directly refute it; setting low so the "
        "contradiction operator has signal to flow.",
    ),
}
