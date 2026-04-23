"""Section 7: Discussion — External Rewards and Self-Verification"""

from gaia.lang import claim, setting, support, compare, abduction

from .s2_taxonomy import (
    intrinsic_rewards_limitation,
    external_rewards_scalability,
    gen_verify_asymmetry_rewards,
)
from .s3_sharpening import unified_sharpening_framework
from .s4_rise_and_fall import rise_then_fall_universal

# ─── Setup ───────────────────────────────────────────────────────────────────

exp_setup_s7 = setting(
    "Section 7 experiments train Qwen3-1.7B-Base and Qwen3-4B-Base on a 4k-problem subset of the "
    "Countdown arithmetic task (from Jiayi-Pan/Countdown-Tasks-3to4 dataset), with 1k held-out "
    "for validation. In Countdown, models form arithmetic expressions to reach a target value; "
    "generating correct expressions is hard but verifying them (checking if expression = target) "
    "is trivial. Three training conditions are compared: "
    "(1) Self-Verification (model evaluates its own outputs using a verification prompt), "
    "(2) Trajectory-Level Entropy (intrinsic reward from Table 1), "
    "(3) Oracle Supervision (ground-truth reward). Validation uses avg@16.",
    title="Section 7 Countdown experiment setup",
)

prompt_setup = setting(
    "Self-Verification prompts: two prompts (P1 and P2) are tested to measure prompt sensitivity. "
    "The model generates solutions and evaluates them using a verification prompt outputting binary "
    "correctness. Ground-truth scoring uses the TinyZero evaluation function (checking whether "
    "expressions correctly evaluate to the target). See Appendix C.1 for full prompts.",
    title="Self-verification prompt setup",
)

# ─── Self-verification observations ──────────────────────────────────────────

self_verification_performance = claim(
    "Self-Verification significantly outperforms Trajectory-Level Entropy intrinsic reward on "
    "the Countdown task. For Qwen3-1.7B-Base, Self-Verification reaches validation accuracy "
    "~0.55–0.75 (avg@16) while Trajectory-Level Entropy achieves substantially lower accuracy. "
    "For Qwen3-4B-Base, Self-Verification reaches ~0.7–0.8 validation accuracy. Both models "
    "approach Oracle Supervision performance with Self-Verification.",
    title="Self-Verification outperforms intrinsic reward on Countdown",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 13"},
    background=[exp_setup_s7],
)

self_verification_reward_accuracy = claim(
    "Self-Verification training dynamics show an interesting recovery pattern: Reward Accuracy "
    "initially drops around step 200 as the policy attempts to exploit the verifier, then "
    "recovers and stabilizes above 0.5. Meanwhile, Ground Truth Reward continues to rise "
    "throughout. This recovery indicates the model is genuinely learning to solve problems "
    "rather than gaming the reward signal.",
    title="Self-Verification reward accuracy recovers after initial exploitation attempt",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 13 (bottom)"},
    background=[exp_setup_s7],
)

instruction_alignment_key = claim(
    "Instruction alignment (fine-tuning for instruction following) is critical for successful "
    "self-verification. On the Countdown task with two verification prompts (P1 and P2):\n\n"
    "- **Qwen3-1.7B (instruction-aligned)**: Starts above 60% accuracy, improves to >80%, "
    "succeeds with both P1 and P2 (robust to prompt choice).\n"
    "- **Qwen3-1.7B-Base (base model)**: Only works with P2; highly sensitive to prompt choice; "
    "final performance below instruction model's starting point.\n\n"
    "Instruction-aligned models maintain stable Reward Accuracy with both prompts; "
    "base models have high prompt sensitivity.",
    title="Instruction alignment enables robust self-verification",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 14"},
    background=[exp_setup_s7, prompt_setup],
)

# ─── Comparison: self-verification vs intrinsic ───────────────────────────────

self_verify_no_collapse = claim(
    "Self-Verification does not exhibit the rise-then-fall collapse pattern seen with intrinsic "
    "rewards: Ground Truth Reward and validation accuracy both improve sustained throughout training "
    "without collapsing. The reward hacking phase (Reward Accuracy dip at ~step 200) is transient "
    "and self-correcting, not terminal collapse.",
    title="Self-Verification achieves sustained improvement without collapse",
)

alt_intrinsic_explain_countdown = claim(
    "Trajectory-Level Entropy intrinsic reward attempts to improve performance on the Countdown "
    "task through sharpening the model's distribution, without external verification.",
    title="Alternative: intrinsic reward for Countdown",
)

pred_self_verify = claim(
    "Self-Verification (external reward) sustains improvement without collapse on Countdown.",
    title="Self-Verification sustained improvement prediction",
)
pred_intrinsic_countdown = claim(
    "Intrinsic reward (Trajectory-Level Entropy) achieves lower performance with eventual collapse on Countdown.",
    title="Intrinsic reward degradation prediction for Countdown",
)
obs_countdown_results = claim(
    "Countdown validation accuracy: Self-Verification reaches ~0.55–0.75 (1.7B) and ~0.7–0.8 (4B); "
    "Trajectory-Level Entropy achieves substantially lower accuracy with eventual degradation.",
    title="Countdown performance comparison observation",
    metadata={"figure": "artifacts/2603.08660.pdf, Figure 13"},
)

comp_self_verify_intrinsic = compare(
    pred_self_verify, pred_intrinsic_countdown, obs_countdown_results,
    reason=(
        "Self-Verification uses external asymmetric verification (arithmetic checking), which "
        "provides an accurate reward signal grounded outside the model's internal state. "
        "Intrinsic reward derives from model confidence, which is bounded by what the model "
        "already knows. The generation-verification asymmetry in Countdown (generation is hard, "
        "verification is trivial arithmetic) creates a reliable, non-degrading external signal."
    ),
    prior=0.85,
)

abd_self_verify_advantage = abduction(
    support([self_verify_no_collapse], obs_countdown_results,
        reason="External verification grounds rewards in arithmetic truth, providing signal independent of model state—predicts sustained improvement seen in @self_verification_performance.", prior=0.87),
    support([alt_intrinsic_explain_countdown], obs_countdown_results,
        reason="Intrinsic reward sharpens model distribution but lacks external grounding; the rise-then-fall pattern predicts lower eventual performance.", prior=0.35),
    comp_self_verify_intrinsic,
    reason="Both approaches target the same Countdown task; the performance gap supports the hypothesis that external verification provides superior reward grounding.",
)

# ─── Scalability argument ─────────────────────────────────────────────────────

external_rewards_path_forward = claim(
    "External rewards offer a more promising path for scaling URLVR beyond what intrinsic methods "
    "allow, for two reasons:\n\n"
    "1. **Reliability**: External verifiers (arithmetic evaluators, code executors, proof checkers) "
    "do not degrade as the model improves. A verifier that checks arithmetic expressions remains "
    "equally reliable regardless of model sophistication, unlike intrinsic rewards that shift as "
    "the model's distribution changes.\n\n"
    "2. **Scale**: Verification procedures are often cheap and can be applied to vast unlabeled "
    "data, providing fresh learning signal unbounded by human labeling capacity. This contrasts "
    "with intrinsic rewards, which are bounded by initial model knowledge.\n\n"
    "Key open challenges: developing diverse verifiable environments and extending verification "
    "asymmetries to new scientific domains.",
    title="External rewards as scalable path forward",
)

strat_external_path = support(
    [external_rewards_scalability, self_verify_no_collapse, instruction_alignment_key],
    external_rewards_path_forward,
    reason=(
        "The theoretical scalability advantage of external rewards (@external_rewards_scalability) "
        "is validated empirically by Self-Verification's sustained improvement (@self_verify_no_collapse). "
        "The instruction alignment requirement (@instruction_alignment_key) identifies a practical "
        "condition for successful deployment (models need sufficient instruction-following capability "
        "to reliably operate the verification loop). Together these establish external rewards as "
        "a viable and scalable direction beyond intrinsic URLVR."
    ),
    prior=0.83,
)
