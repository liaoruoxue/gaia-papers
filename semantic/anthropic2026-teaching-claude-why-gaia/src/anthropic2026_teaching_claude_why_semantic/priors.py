"""Priors for Layer 2 semantic claims and judgment nodes.

实验目的（2026-05-10）：用 prior + BP 看 anthropic2026 paper 包（formalize Layer 1
等价物）能否被 gaia-semantic Layer 2 工作流消费。
"""

from .motivation import (
    deliberation_drives_alignment_efficiency,
    ood_difficult_advice_28x_efficiency,
    constitutional_documents_generalize_via_sdf,
    diverse_augmentation_independent_signal,
    frontier_models_aligned_modulo_contamination,
    honeypot_setup_artificial,
    scale_only_frontier_models,
)
from .s2_strategies import (
    surprise_filtered_demo_modest,
    surprise_28x_efficiency_via_ood,
    surprise_unrelated_fiction_generalizes,
    surprise_unused_tools_help,
    elegant_difficult_advice_design,
    elegant_synthetic_doc_fine_tuning,
    neg_filtered_sft_only_modest,
    weak_no_h3_separation_experiment,
    weak_contamination_caveat_acknowledged,
    bdry_blog_format_no_appendix,
)


PRIORS: dict = {
    # ── Aggregated semantic claims ──
    deliberation_drives_alignment_efficiency: (
        0.85,
        "Anthropic 报告 22→3% vs 22→15%（5× efficiency gap）+ 跨多个 honeypot scenario 一致。"
        "强 claim 但受 H3 separation 实验缺失约束。boundary：blog 没公开 appendix。"
        "TODO:review"
    ),
    ood_difficult_advice_28x_efficiency: (
        0.78,
        "28× 是 striking number，但 baseline (synthetic honeypot) 设计可能存在效率"
        "上限——synthetic data 本身可能 sub-optimal，导致 OOD 看起来更高效。"
        "TODO:review"
    ),
    constitutional_documents_generalize_via_sdf: (
        0.82,
        "65→19% 的 3× 改善 + 跨 RL 持续 = 较强证据。boundary：仅在 Haiku-class 测试。"
        "TODO:review"
    ),
    diverse_augmentation_independent_signal: (
        0.65,
        "small-but-significant 措辞本身暗示 effect 不大，independent 信号但 magnitude "
        "受限。"
        "TODO:review"
    ),
    frontier_models_aligned_modulo_contamination: (
        0.55,
        "0% 是 striking 但作者自陈 contamination 严重削弱外部 validity。"
        "TODO:review"
    ),

    # ── Boundary (in motivation) ──
    honeypot_setup_artificial: (
        0.70,
        "honeypot 是 artificial scenario 这一 boundary 在 alignment 研究中通用，"
        "强 prior。"
    ),
    scale_only_frontier_models: (
        0.60,
        "scale-coupling 来自 Greenblatt 2024 alignment-faking 跨架构观察，"
        "但 anthropic2026 blog 本身未直接测 sub-frontier。中等 prior。"
    ),

    # ── Surprising findings ──
    surprise_filtered_demo_modest: (
        0.85,
        "filtered SFT 22→15% 是 paper 报告数字 + 反 default prior 强 surprise。"
    ),
    surprise_28x_efficiency_via_ood: (
        0.80,
        "28× 数据效率是 striking 但有 baseline 设计 caveat。"
    ),
    surprise_unrelated_fiction_generalizes: (
        0.78,
        "fiction 推广是反直觉发现，但机制（distribution-learner vs truth-extractor）"
        "在 ML 社区已部分认知。"
    ),
    surprise_unused_tools_help: (
        0.75,
        "未用 tool def 加速 alignment 是新颖发现，magnitude 受限。"
    ),

    # ── Elegant points ──
    elegant_difficult_advice_design: (
        0.88,
        "framing-shift（protagonist → advisor）是清晰 design pattern，"
        "high portability。"
    ),
    elegant_synthetic_doc_fine_tuning: (
        0.80,
        "narrative-based disposition shaping 继承人类教育传统，可推广但限于 "
        "disposition layer。"
    ),

    # ── Negative results ──
    neg_filtered_sft_only_modest: (
        0.85,
        "filtered SFT modest 是 paper 报告的 negative result，强 prior。"
    ),

    # ── Weak premises ──
    weak_no_h3_separation_experiment: (
        0.82,
        "H3 separation 缺失是真实 ablation gap，falsifier 明确（'OOD demo-only' "
        "格子）。"
    ),
    weak_contamination_caveat_acknowledged: (
        0.85,
        "作者自陈 contamination → 弱点强度高。"
    ),
    bdry_blog_format_no_appendix: (
        0.75,
        "blog 缺 appendix 是普遍 reporting boundary，影响所有 claim 但不致命。"
    ),
}
