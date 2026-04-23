"""Prior assignments for independent (leaf) claims in the 2502.06533 formalization.

Run `gaia check --hole .` to see which claims need priors.
Priors are reviewer judgments about plausibility of each independent premise
before inference; they reflect strength of evidence in the source.

Paper: "Ignore the KL Penalty! Boosting Exploration on Critical Tokens to Enhance RL Fine-Tuning"
Authors: Jean Vassoyan, Nathanaël Beau, Roman Plaud
Venue: NAACL 2025 Findings (arXiv 2502.06533)
"""

from . import (
    # Empirical observations (directly measured)
    pretrain_generalization_results,
    larger_pretrain_fewer_rl_errors,
    larger_pretrain_qualitatively_different_errors,
    sparse_reward_difficulty,
    # Per-N empirical observations for critical token uncertainty gap (Table 1)
    obs_ct_n3,
    obs_ct_n5,
    obs_ct_n7,
    # Alternative hypothesis
    alt_standard_kl_sufficient,
    # Prediction claims used in compare()
    pred_prioritized,
    pred_alt_standard,
    # Limitation claims (factual)
    limitation_small_model,
    limitation_simple_task,
    limitation_scratchpad,
    limitation_fixed_reference,
)

PRIORS = {
    # ── Direct empirical results (high credence) ──

    pretrain_generalization_results: (
        0.93,
        "Directly measured accuracy values from experiments on 1,000 test examples "
        "with resampling confidence intervals. Results reproducible from public code "
        "(github.com/jvasso/llm-rl-arithmetic). Straightforward classification accuracy "
        "measurements from controlled experiments. Very high confidence."
    ),

    larger_pretrain_fewer_rl_errors: (
        0.85,
        "Observational claim that follows directly from pre-training accuracy data: "
        "models with higher baseline accuracy necessarily make fewer errors on the same "
        "task. The causal link to exploration incentive is an interpretation, but the "
        "core observation is well-grounded in the empirical results."
    ),

    larger_pretrain_qualitatively_different_errors: (
        0.72,
        "Based on qualitative analysis of error types from Figure 3 (token duplication, "
        "digit copying vs carry propagation failures). Involves subjective categorization "
        "of errors. The 'harder to fix by RL' part is a plausibility argument without "
        "direct quantification. Moderate confidence."
    ),

    sparse_reward_difficulty: (
        0.88,
        "Well-established in the LLM RL fine-tuning literature. The paper's MDP formulation "
        "explicitly defines reward as 1 for correct answer, 0 otherwise. This is an accurately "
        "described and widely recognized challenge in the field."
    ),

    # ── Per-N critical token observations (directly from Table 1) ──
    # These are derived in the induction structure but empirically measured directly.
    # Adding priors anchors them as observations rather than purely theory-derived.

    obs_ct_n3: (
        0.93,
        "Direct measurement from Table 1: Delta_J_hat = -0.33 +/- 0.01 for critical tokens "
        "vs 0.0012 +/- 0.0001 for non-critical at N=3. Precise numerical values with "
        "narrow confidence intervals. Very high credence."
    ),

    obs_ct_n5: (
        0.89,
        "Direct measurement from Table 1: Delta_J_hat = -0.21 +/- 0.18 for critical tokens "
        "vs 0.0002 +/- 0.0001 for non-critical at N=5. High credence; note the wider CI "
        "for critical tokens (0.18) indicating more variability at N=5."
    ),

    obs_ct_n7: (
        0.91,
        "Direct measurement from Table 1: Delta_J_hat = -0.13 +/- 0.04 for critical tokens "
        "vs 0.0004 +/- 0.0001 for non-critical at N=7. High credence; the narrowing gap "
        "at larger N is consistent with better pre-training on longer sequences."
    ),

    # ── Alternative hypothesis ──

    alt_standard_kl_sufficient: (
        0.22,
        "This alternative claims standard KL is sufficient and the performance gap is from "
        "other factors. Prior reflects explanatory power for the observation (20pp accuracy gap): "
        "the standard KL prediction (comparable accuracy) does NOT explain the observed gap, "
        "so pi(Alt) should be low. The theoretical argument against standard KL being sufficient "
        "is also compelling, further reducing this prior."
    ),

    # ── Prediction claims ──

    pred_prioritized: (
        0.78,
        "Before seeing results, the prioritized KL prediction is theoretically motivated: "
        "targeting uncertain tokens for exploration is coherent with the critical-token "
        "characterization. The prediction is specific and testable. High prior."
    ),

    pred_alt_standard: (
        0.28,
        "Before seeing results, the prediction that standard KL achieves comparable accuracy "
        "is plausible only if confidence-weighting provides no additional benefit. "
        "Given the theoretical argument, this prediction is less supported. Low prior."
    ),

    # ── Limitation claims (factual) ──

    limitation_small_model: (
        0.97,
        "Stated fact: GPT-2 has 85M parameters; modern production LLMs are 7B-70B+. "
        "This limitation is straightforwardly true and not debatable."
    ),

    limitation_simple_task: (
        0.95,
        "N-digit addition is objectively simpler than standard LLM benchmarks (MMLU, "
        "HumanEval, GSM8K, etc.). Factually accurate characterization."
    ),

    limitation_scratchpad: (
        0.90,
        "Paper explicitly states it uses scratchpad-based reasoning for token-level analysis. "
        "The generalizability concern about tasks without scratchpads is real and acknowledged "
        "by the authors. High confidence this limitation is genuine."
    ),

    limitation_fixed_reference: (
        0.85,
        "The method uses a fixed reference model's entropy without Bayesian uncertainty. "
        "This is a real methodological choice. The epistemic vs aleatoric uncertainty "
        "concern is technically valid. High confidence this limitation exists."
    ),
}
