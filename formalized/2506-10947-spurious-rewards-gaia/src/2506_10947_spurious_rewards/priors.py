"""Prior assignments for independent (leaf) claims in the spurious-rewards formalization.

Run `gaia check --hole .` to see which claims need priors.
Priors are author-reviewer judgments about the plausibility of each independent premise
before inference; they should reflect the strength of evidence in the source.

Paper: "Spurious Rewards: Rethinking Training Signals in RLVR" (arXiv 2506.10947)
"""

from . import (
    # Empirical observations (direct experimental results)
    claim_qwen7b_math500_results,
    claim_spurious_fails_non_qwen,
    claim_aime_results,
    claim_code_freq_increases_rlvr,
    claim_code_accuracy_advantage,
    claim_qwen_pretraining_code_freq,
    claim_model_family_consistency,
    claim_clipping_amplifies_prior,
    claim_clipping_qwen_specificity,
    claim_prompt_sensitivity,
    claim_ttrl_one_shot_same_pattern,
    # Alternative hypotheses
    alt_rlvr_teaches_new,
    alt_code_elicitation_only_prompt,
    # Mechanistic/theoretical claims
    claim_grpo_clipping_bias,
    claim_rlvr_teaches,
    # Prediction claims used in compare()
    pred_pretraining,
    pred_teaches,
    pred_rlvr_broader,
    pred_prompt_same,
)

PRIORS = {
    # ── Direct empirical results (high credence — directly read from paper figures/tables) ──

    claim_qwen7b_math500_results: (
        0.97,
        "This is a direct experimental measurement read from Figure 2a of the paper. "
        "The specific numerical gains (+21.4 pp random, +13.8 pp format, +24.1 pp "
        "incorrect, +27.1 pp majority vote, +29.1 pp ground truth) are precisely "
        "reported tabular values from 300 GRPO training steps on a well-defined benchmark. "
        "Very high credence as primary experimental result — independently replicable.",
    ),

    claim_spurious_fails_non_qwen: (
        0.95,
        "Direct experimental measurement from Figure 3 of the paper. The negative and "
        "near-zero gains of spurious rewards on Llama3.1-8B-Instruct (-6.4 pp random, "
        "-8.3 pp incorrect) and OLMo2-7B (-6.4 pp random, -8.3 pp incorrect) are specific "
        "numerical values from the same experimental setup. High credence as the "
        "contrast between model families is the central empirical claim of the paper.",
    ),

    claim_aime_results: (
        0.90,
        "Direct experimental measurement from Figure 14 of the paper. The differential "
        "pattern — spurious rewards work on AIME 2024 (in-distribution) but not AIME 2025 "
        "(post-cutoff) — is a clear and internally consistent finding. Slightly lower "
        "credence than MATH-500 results because AIME has smaller sample size (average@8 "
        "across 30 problems) and stochastic variance is higher.",
    ),

    claim_code_freq_increases_rlvr: (
        0.95,
        "Direct experimental observation from Figure 6a. The 65% → ~90%+ code frequency "
        "increase within 15 training steps is a robust, visually clear finding across "
        "multiple reward types. The correlation with accuracy improvement is further "
        "supported by the Lang→Code decomposition analysis. Very high credence as a "
        "central mechanistic observation.",
    ),

    claim_code_accuracy_advantage: (
        0.95,
        "Directly measured from Table 1 of the paper, stratifying MATH-500 responses "
        "by reasoning strategy (code vs language) before RLVR. The 60.9% vs 35.0% "
        "accuracy difference for Qwen2.5-Math-7B and 52.6% vs 17.2% for Qwen2.5-Math-1.5B "
        "are specific, independently verifiable measurements. Very high credence.",
    ),

    claim_qwen_pretraining_code_freq: (
        0.95,
        "Directly measured from Table 1 of the paper, counting 'python' string occurrences "
        "in pre-RL responses on MATH-500. The 65.0% frequency for Qwen2.5-Math-7B and 0% "
        "for Llama/OLMo2 models is a binary and easily verifiable measurement. High "
        "credence as a baseline measurement with no confounds.",
    ),

    claim_model_family_consistency: (
        0.90,
        "Inferred from the cross-model results in Figure 3 — within-family consistency "
        "is a pattern observed across multiple models (Qwen2.5-Math-7B and -1.5B both "
        "gain from all rewards; Llama3.1 and Llama3.2 both lose from spurious rewards; "
        "OLMo2-7B and OLMo2-7B-SFT both gain only from ground truth). High credence "
        "as a summary observation with consistent supporting data points.",
    ),

    claim_clipping_amplifies_prior: (
        0.88,
        "Empirical finding from Figure 12 of the paper — average token probability "
        "increases monotonically under clipping (reaching ~0.93+) but stays flat without "
        "clipping (~0.85). The correlation with code frequency increase is also shown. "
        "High credence but slightly less than direct accuracy measurements because "
        "interpretations of internal probability trajectories have additional uncertainty.",
    ),

    claim_clipping_qwen_specificity: (
        0.87,
        "Synthesis claim combining Table 1 data (code accuracy 60.9% vs language 35.0% "
        "for Qwen-Math; code 21.0% vs language 40.0% for OLMo2-7B-SFT) with the clipping "
        "mechanism. The reasoning that amplifying high-prior behaviors helps Qwen-Math "
        "but hurts bad-code models is directly grounded in measured accuracy differences. "
        "Slightly lower credence as it integrates multiple measurements.",
    ),

    claim_prompt_sensitivity: (
        0.92,
        "Direct measurement from Table 5 and Figure 18 of the paper. The accuracy "
        "variation across prompts (49.4% Qwen default → 68.8% LIPSUM spurious prompt) "
        "is a striking but clearly documented experimental finding. High credence as "
        "a well-controlled ablation study with specific numerical values.",
    ),

    claim_ttrl_one_shot_same_pattern: (
        0.90,
        "Based on Figure 4 of the paper, which replicates TTRL (Zuo et al. 2025) and "
        "One-Shot RL (Wang et al. 2025b) on diverse model families. The same-pattern "
        "finding — strong on Qwen, weak on Llama/OLMo2 — is the paper's own experimental "
        "replication. High credence as a controlled comparison under standardized conditions.",
    ),

    # ── Mechanistic and theoretical claims ────────────────────────────────────

    claim_grpo_clipping_bias: (
        0.92,
        "The mathematical derivation of the GRPO clipping bias under random rewards "
        "(Appendix B.1.2 of the paper) is a formal algebraic result. The derivation shows "
        "that E[gradient] ≠ 0 under clipping even when E[advantage] = 0. Very high "
        "credence as a mathematical derivation, slightly below 1.0 to account for possible "
        "errors in the derivation steps not independently verified.",
    ),

    # ── Alternative hypotheses (prior reflects initial plausibility before evidence) ──

    alt_rlvr_teaches_new: (
        0.35,
        "The 'RLVR teaches new capabilities' hypothesis is the naive prior before seeing "
        "the paper's evidence. It is reasonable ex ante (reward gradients do provide "
        "learning signal), hence higher than 0.1. The paper's random-reward results "
        "strongly falsify this for Qwen2.5-Math models; the prior at 0.35 reflects "
        "initial plausibility before seeing those results.",
    ),

    alt_code_elicitation_only_prompt: (
        0.25,
        "The alternative that prompting alone explains the code-frequency gains has "
        "low credence because the code frequency increases during RLVR training without "
        "any prompt change. The code-forcing prompt experiments (Table 3) show gains "
        "comparable to RLVR, but cannot explain the training dynamics. Low prior as "
        "the alternative is partially falsified by the no-prompt-change training setup.",
    ),

    claim_rlvr_teaches: (
        0.25,
        "The counterfactual claim that RLVR fundamentally teaches new reasoning skills "
        "is the alternative view being tested. Prior at 0.25 reflects initial reasonable "
        "doubt but acknowledges the paper's evidence (random rewards work just as well "
        "as ground truth rewards on Qwen) strongly argues against this for math-specialized "
        "Qwen models. Low but non-negligible prior.",
    ),

    # ── Prediction claims used in compare() ────────────────────────────────────

    pred_pretraining: (
        0.80,
        "The predictions of the pretraining-surfacing hypothesis — random rewards yield "
        "gains, family-specificity, gamma-robustness — are well-articulated and all three "
        "are confirmed by the paper's experiments. High prior as these are structurally "
        "coherent predictions from a well-defined mechanistic hypothesis.",
    ),

    pred_teaches: (
        0.30,
        "The predictions of the 'RLVR teaches new reasoning' hypothesis — reward "
        "informativeness determines gain, random reward yields no gain, gains generalize "
        "across families — are the null predictions. All three are falsified by the "
        "paper's results. Low prior reflecting initial skepticism before seeing evidence.",
    ),

    pred_rlvr_broader: (
        0.75,
        "The prediction that RLVR causes code elicitation beyond what prompting can "
        "achieve (and that compound rewards affect performance through the code channel) "
        "is supported by the compound no-Python reward experiments. Moderate-high prior "
        "as this is a directionally well-motivated prediction.",
    ),

    pred_prompt_same: (
        0.20,
        "The prediction that if prompting alone were sufficient, compound no-Python "
        "rewards would not specifically affect gains — this prediction is falsified by "
        "the format+no-Python result (gains cease entirely). Low prior reflecting that "
        "the 'prompting alone' alternative is likely insufficient.",
    ),
}
