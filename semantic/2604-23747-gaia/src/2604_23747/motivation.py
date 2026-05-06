"""Layer 2 — SFT-then-RL Beats Mixed-Policy (2604.23747)

Core finding: reported mixed-policy gains over SFT baselines are largely artifacts of
two framework bugs. Corrected SFT baselines match or exceed mixed-policy methods.
"""

from gaia.lang import claim, setting

# ── Core semantic claims ──

two_bugs_suppress_sft_baseline = claim(
    "Two bugs in widely-used RL training frameworks systematically suppress "
    "SFT baselines: (1) DeepSpeed CPU-offload gradient accumulation bug "
    "(only first micro-batch gradients reach optimizer, introduced in PR "
    "#6550 Sept 2024), (2) loss aggregation bug in OpenRLHF/Llama-Factory/early "
    "verl (per-mini-batch mean instead of per-token mean, distorting total loss). "
    "Combined, these bugs reduce the SFT baseline by ~5.7 points on Qwen2.5-Math-7B. "
    "The bug affects TRL, OpenRLHF, and Llama-Factory — any framework using "
    "DeepSpeed ZeRO-1/2 with CPU-offloaded optimizer.",
    title="Two framework bugs suppress SFT baselines by ~5.7 points",
    aggregated_from=[
        "claim_optimizer_bug", "claim_bug_introduced_in_pr", "claim_bug_propagation",
        "claim_loss_aggregation_bug", "claim_optimizer_fix",
    ],
)

mixed_policy_gains_are_artifact = claim(
    "Published mixed-policy methods (SPIN, LUFFY, ReLIFT, ReFT, RLPF) report "
    "SOTA over SFT baselines. After fixing both bugs, the corrected SFT baseline "
    "on Qwen2.5-Math-7B matches or exceeds all reported mixed-policy ID results. "
    "On Llama-3.1-8B, SFT-then-RL beats the best mixed-policy method by +4.0pp. "
    "The gains attributed to policy mixing were actually artifacts of buggy baselines.",
    title="Reported mixed-policy gains are artifacts of buggy SFT baselines",
    aggregated_from=[
        "claim_qwen_headline", "claim_llama_headline",
        "claim_qwen_sft_corrected", "claim_qwen_plus_3p8",
    ],
)

sft_then_rl_sufficient = claim(
    "Simple SFT-then-RL (corrected SFT baseline → standard online RL) achieves "
    "57.0 ID / 59.9 OOD on Qwen2.5-Math-7B, beating the best mixed-policy method "
    "(SRFT: 53.2 ID). On Llama-3.1-8B, SFT-then-RL beats mixed-policy by +4.0pp. "
    "Moreover, 50-step SFT-then-RL outperforms mixed-policy methods at fewer total "
    "training steps, demonstrating compute efficiency in addition to accuracy.",
    title="Simple SFT-then-RL beats all mixed-policy methods",
    aggregated_from=[
        "claim_qwen_sft_then_rl", "claim_compute_efficiency_headline",
        "claim_llama_headline",
    ],
)

cross_framework_validation_essential = claim(
    "Two bugs spanning three frameworks went undetected for months because "
    "no one compared SFT baselines across independent implementations. The "
    "bugs were discovered by comparing OpenRLHF vs verl SFT baselines and "
    "finding a discrepancy. Cross-framework validation is not a nice-to-have "
    "— it is a necessary diagnostic for catching infrastructure-level errors "
    "that distort research conclusions.",
    title="Cross-framework validation is essential for research integrity",
    aggregated_from=[
        "claim_implications", "claim_optimizer_fix_validated",
    ],
)

# ── Boundary ──

math_domain_only = claim(
    "All experiments use math reasoning benchmarks (MATH, GSM8K). Whether "
    "the same bugs affect other domains (coding, agent tasks) is not tested. "
    "The bugs are framework-level, so they likely affect all domains — but "
    "the magnitude may differ.",
    title="Domain limitation: math only",
)

scale_limited = claim(
    "All experiments use 7-8B models. Whether the bug effect scales with "
    "model size (larger models might be more or less sensitive to gradient "
    "dropping) is unknown.",
    title="Scale limitation: 7-8B only",
)
