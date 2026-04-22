"""Section 3: (Lack of) Generalization to Other Models"""

from gaia.lang import (
    claim, setting,
    support, induction, compare,
    contradiction,
)

from .motivation import (
    setup_models, setup_reward_types,
    claim_spurious_fails_non_qwen, claim_pretraining_hypothesis,
    claim_rlvr_improves_qwen,
    claim_qwen_centric_risk,
)

from .s2_spurious_rewards import (
    claim_qwen7b_math500_results,
)

# ── Cross-model experimental results ──────────────────────────────────────────

claim_qwen_general_also_gains = claim(
    "General-purpose Qwen2.5-7B (not math-specialized; initial MATH-500 ~41.6%) "
    "and Qwen2.5-1.5B also gain from weak and spurious rewards. For Qwen2.5-7B "
    "on MATH-500, all non-random rewards including the spurious incorrect reward "
    "produce clear improvements (+13.2 pp format, +27.8 pp incorrect, +16.4 pp "
    "majority vote, +31.9 pp ground truth). This generalizes the spurious-reward "
    "effect beyond math-specialized models to the general Qwen2.5 family.",
    title="General-purpose Qwen2.5-7B also gains from spurious rewards, not just math-specialized",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 3b"},
)

claim_olmo_only_gt = claim(
    "OLMo2-7B and OLMo2-7B-SFT (instruction-finetuned from OLMo2-7B) show "
    "relatively flat performance on spurious rewards and only significant gains "
    "with ground truth rewards (+16.7 pp for OLMo2-7B on MATH-500). Spurious "
    "rewards (random, incorrect) yield -6.4 pp and -8.3 pp respectively on "
    "OLMo2-7B. This pattern is consistent across MATH-500 and AMC benchmarks.",
    title="OLMo2 models show gains only from ground truth reward, spurious rewards hurt performance",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 3c,d"},
)

claim_llama_partial = claim(
    "Llama3.1-8B-Instruct and Llama3.2-3B-Instruct show gains only from "
    "informative reward signals. Llama3.1-8B-Instruct (baseline 36.8%) gains "
    "+15.5 pp from ground truth but -6.4 pp (random), -8.3 pp (incorrect), "
    "-2.1 pp (format). Llama base models (non-Instruct) show minimal "
    "improvement even from ground truth, suggesting SFT instruction tuning "
    "helps but math-specific pretraining is critical.",
    title="Llama models gain only from informative signals; spurious rewards hurt or have no effect",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 3e-h"},
)

claim_model_family_consistency = claim(
    "Models within the same family generally exhibit similar RLVR behavior "
    "patterns regardless of size or instruction-tuning status. For example, "
    "both Qwen2.5-Math-7B and Qwen2.5-Math-1.5B show gains from all reward "
    "types; both Llama3.1-8B and Llama3.2-3B show similar limited-gain "
    "patterns; and both OLMo2-7B and OLMo2-7B-SFT are only helped by "
    "ground truth rewards. This consistency implicates pretraining data "
    "distribution as a primary determinant.",
    title="Within-family consistency in RLVR behavior implicates pretraining data distribution",
)

claim_smaller_models_less_spurious = claim(
    "Smaller models are generally less likely to benefit from spurious rewards, "
    "particularly random rewards. Qwen2.5-Math-1.5B gains from random reward "
    "are slower and smaller on AMC (+4.9%) compared to Qwen2.5-Math-7B (+21.4% "
    "on MATH-500). The conjecture is that larger models retain more pretraining "
    "knowledge that spurious rewards can surface.",
    title="Smaller models benefit less from spurious rewards than larger models",
)

claim_ttrl_one_shot_same_pattern = claim(
    "Two published RLVR methods — TTRL (Test-Time Reinforcement Learning, Zuo "
    "et al. 2025) and One-Shot RL (Wang et al. 2025b) — show the same pattern "
    "as the spurious rewards: strong improvements on Qwen2.5-Math or Qwen2.5 "
    "models, but the same signals often fail to yield gains on Llama3 or OLMo2 "
    "families. TTRL trains on unlabeled test prompts with online majority-vote "
    "labels; One-Shot RL uses a single training example with correct label.",
    title="TTRL and One-Shot RL methods also fail to generalize beyond Qwen models",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 4"},
)

# ── Reasoning strategies ──────────────────────────────────────────────────────

# Induction: multiple independent model families confirm the pattern
s_qwen_confirms = support(
    [claim_pretraining_hypothesis],
    claim_qwen_general_also_gains,
    reason=(
        "If RLVR surfaces pretrained representations (@claim_pretraining_hypothesis), "
        "then any Qwen model with strong pretraining math content should respond "
        "to spurious rewards. Qwen2.5-7B (general) gaining from spurious rewards "
        "confirms: it is not only math-specialized Qwen models, but the entire "
        "Qwen pretraining corpus that matters."
    ),
    prior=0.85,
)

s_olmo_confirms = support(
    [claim_pretraining_hypothesis],
    claim_olmo_only_gt,
    reason=(
        "If RLVR surfaces pretrained representations (@claim_pretraining_hypothesis), "
        "then OLMo2 — which lacks math-intensive pretraining or effective code "
        "reasoning in its distribution — should not respond to spurious rewards. "
        "@claim_olmo_only_gt matches this prediction: only ground truth rewards "
        "(which provide genuine learning signal) help OLMo2."
    ),
    prior=0.85,
)

s_llama_confirms = support(
    [claim_pretraining_hypothesis],
    claim_llama_partial,
    reason=(
        "Llama models (@claim_llama_partial) show a pattern consistent with "
        "@claim_pretraining_hypothesis: spurious rewards do not help because "
        "Llama's pretraining distribution did not produce the same kind of "
        "ready-to-surface math reasoning representations as Qwen2.5-Math."
    ),
    prior=0.8,
)

ind_qwen_olmo = induction(
    s_qwen_confirms, s_olmo_confirms,
    law=claim_pretraining_hypothesis,
    reason=(
        "Qwen and OLMo2 model families are trained with different data "
        "distributions and show opposite RLVR responses — this independence "
        "makes them strong joint evidence for the pretraining hypothesis."
    ),
)

ind_three_families = induction(
    ind_qwen_olmo, s_llama_confirms,
    law=claim_pretraining_hypothesis,
    reason=(
        "Llama (a third independent model family with different pretraining) "
        "also follows the predicted pattern, further strengthening the induction."
    ),
)

strat_ttrl_generalization = support(
    [claim_ttrl_one_shot_same_pattern, claim_pretraining_hypothesis],
    claim_qwen_centric_risk,
    reason=(
        "The pattern in @claim_ttrl_one_shot_same_pattern mirrors the spurious "
        "reward results: both published methods and spurious rewards work on Qwen "
        "but not on OLMo2/Llama. @claim_pretraining_hypothesis explains why: "
        "these methods all leverage the same Qwen-specific pretrained representations. "
        "This supports the practical concern that RLVR research conclusions are "
        "model-dependent (@claim_qwen_centric_risk)."
    ),
    prior=0.8,
)

strat_family_consistency = support(
    [claim_model_family_consistency],
    claim_pretraining_hypothesis,
    reason=(
        "Within-family consistency (@claim_model_family_consistency) across "
        "model sizes and SFT variants within the same family strongly implicates "
        "pretraining data as the key variable, consistent with "
        "@claim_pretraining_hypothesis. If RLVR algorithm or architecture were "
        "the primary driver, we would expect more variation within families "
        "(different sizes use different architectures)."
    ),
    prior=0.8,
    background=[setup_models],
)
