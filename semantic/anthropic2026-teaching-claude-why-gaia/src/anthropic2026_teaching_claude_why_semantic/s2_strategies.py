"""Layer 2 strategies + 5 类 judgment claims.

实验目的（2026-05-10）：用 anthropic2026 paper 包（formalize 产出）作 Layer 1 输入，
看能否走通 gaia-semantic 的 Layer 2 工作流（5 semantic claim + 5 类 judgment）。

5 类 judgment node 按 gaia-semantic SKILL 规范：
- surprise_*：novelty_vs_kb (confirm/contradict/refine/new) + kb_anchor
- elegant_*：portability + reusable_primitive
- weak_*：issue_type + what_would_falsify
- bdry_*：boundary_type + stated_explicitly
- neg_*：作者自陈失败
"""

import importlib
from gaia.lang import claim, support, deduction
from .motivation import (
    deliberation_drives_alignment_efficiency,
    ood_difficult_advice_28x_efficiency,
    constitutional_documents_generalize_via_sdf,
    diverse_augmentation_independent_signal,
    frontier_models_aligned_modulo_contamination,
    honeypot_setup_artificial,
    scale_only_frontier_models,
)

# ── True cross-package import: Layer 1 formalize claims ──
# 串 BP through real object refs（vs aggregated_from string anchor).
# Pattern follows joint-grpo-fragility-gaia (cross-package joint inference).
try:
    _l1 = importlib.import_module("anthropic2026_teaching_claude_why.paper_anthropic2026")
    l1_c1_filtered_sft_modest = _l1.anthropic2026_c1_filtered_sft_modest
    l1_c2_deliberation_rewrite = _l1.anthropic2026_c2_deliberation_rewrite_strong
    l1_c3_difficult_advice_28x = _l1.anthropic2026_c3_difficult_advice_28x
    l1_c8_haiku45plus_zero = _l1.anthropic2026_c8_haiku45plus_zero
    l1_c8_wp_contamination = _l1.anthropic2026_c8_wp_external_contamination
    _CROSS_PKG_AVAILABLE = True
except (ImportError, AttributeError):
    _CROSS_PKG_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════
# Surprising findings (反直觉发现)
# ══════════════════════════════════════════════════════════════════════

surprise_filtered_demo_modest = claim(
    "在 honeypot eval distribution 上 closely-matched filtered SFT 训练只把"
    "misalignment 从 22% 降到 15%（modest），违反'同分布训练能高效改善'的直觉。"
    "这是 gut prior 'training distribution close to eval = high efficiency' 被"
    "推翻的例子——单纯模仿 aligned actions 的信号弱于推理结构信号。",
    title="Surprising: same-distribution filtered SFT only modest improvement",
    aggregated_from=["anthropic2026_c1_filtered_sft_modest"],
    semantic_refs=["deliberation_drives_alignment_efficiency"],
    novelty_vs_kb="contradict",
    kb_anchor="rl-training.md#data-distribution",
)

surprise_28x_efficiency_via_ood = claim(
    "3M-token OOD difficult-advice 数据集与 ~85M-token in-distribution synthetic "
    "honeypot 在 misalignment eval 上等效（28× 数据效率）。这与 ML 通行直觉"
    "'OOD 数据效率应低于 in-dist'相反，暗示 alignment 训练中 distribution overlap "
    "不是 dominant factor，data structural quality（推理深度 + 场景多样性）才是。",
    title="Surprising: OOD 28× efficiency over in-dist synthetic honeypot",
    aggregated_from=[
        "anthropic2026_c3_difficult_advice_28x",
        "anthropic2026_c4_difficult_advice_ood_better",
    ],
    semantic_refs=["ood_difficult_advice_28x_efficiency"],
    novelty_vs_kb="new",
    kb_anchor="rl-training.md#data-efficiency",
)

surprise_unrelated_fiction_generalizes = claim(
    "正面 fictional stories about aligned AI（与 evaluation scenario 完全无关）"
    "通过 SDF 训练能把 blackmail rate 从 65% 降到 19%。'fiction 不是真信号'的"
    "default prior 被推翻——LM 学的是 token 分布，fiction 提供高质量 character + "
    "narrative-structure 信号，恰好是 alignment 关心的 disposition 层。",
    title="Surprising: unrelated fiction generalizes to alignment improvement",
    aggregated_from=["anthropic2026_c5_constitutional_fiction_3x"],
    semantic_refs=["constitutional_documents_generalize_via_sdf"],
    novelty_vs_kb="contradict",
    kb_anchor="rl-training.md#data-modality",
)

surprise_unused_tools_help = claim(
    "在 RL 环境中加入 tool definitions（即使 tool 从未被调用）能 small-but-"
    "significant 加速 honeypot 改善速率。'未使用的 tool def 是 noise'的 prior "
    "被推翻——context 结构本身（不是工具内容）能正则化模型，迫使更深 reasoning。",
    title="Surprising: tool definitions help even when never invoked",
    aggregated_from=["anthropic2026_c7_diverse_aug_accel"],
    semantic_refs=["diverse_augmentation_independent_signal"],
    novelty_vs_kb="new",
    kb_anchor="rl-training.md#context-augmentation",
)


# ══════════════════════════════════════════════════════════════════════
# Elegant points (方法之美)
# ══════════════════════════════════════════════════════════════════════

elegant_difficult_advice_design = claim(
    "Difficult-advice 数据集的设计巧妙：让 user 面临伦理两难、AI 给 advice，"
    "本质上把 alignment 训练数据从'AI-as-protagonist'转换为'AI-as-advisor'，"
    "天然规避了 AI 训练主体直接做 honeypot decision 的循环。这是 framing-shift "
    "策略——不改变 ethical 信号本身，改变 signal carrier role。可移植到任何"
    "需要 OOD-but-aligned 训练数据的场景。",
    title="Elegant: framing-shift from AI-as-protagonist to AI-as-advisor",
    aggregated_from=[
        "anthropic2026_c3_difficult_advice_28x",
    ],
    semantic_refs=["ood_difficult_advice_28x_efficiency"],
    portability="high",
    reusable_primitive=True,
)

elegant_synthetic_doc_fine_tuning = claim(
    "SDF 把 alignment 装入 disposition 层而非 reflex 层——通过让模型 absorb "
    "constitutional documents + fictional narratives，绕过了'直接训练拒绝行为'"
    "的 scope limitation。这种'通过 narrative 教 character'的方法继承自人类教育"
    "传统（道德故事），可移植到其他 disposition shaping 任务。",
    title="Elegant: SDF teaches disposition through narrative, not rules",
    aggregated_from=["anthropic2026_c5_constitutional_fiction_3x"],
    semantic_refs=["constitutional_documents_generalize_via_sdf"],
    portability="medium",
    reusable_primitive=True,
)


# ══════════════════════════════════════════════════════════════════════
# Negative results (作者自陈失败)
# ══════════════════════════════════════════════════════════════════════

neg_filtered_sft_only_modest = claim(
    "Reported negative result: 在 helpful-only honeypot distribution 上做 "
    "filtered SFT（保留 model 拒绝 honeypot 的 trace）虽然 distribution overlap "
    "高，但只把 misalignment 从 22% 降到 15%。排除了'同分布训练 → 高效率'的简单"
    "假说，强迫探索 deliberation 等更深机制。",
    title="Negative result: distribution-matched SFT yields only modest improvement",
    aggregated_from=["anthropic2026_c1_filtered_sft_modest"],
    semantic_refs=["deliberation_drives_alignment_efficiency"],
)


# ══════════════════════════════════════════════════════════════════════
# Weak / Boundary — as deduction premises
# ══════════════════════════════════════════════════════════════════════

weak_no_h3_separation_experiment = claim(
    "Anthropic 没有做 'OOD + 行为示范（无 deliberation）' 的对照格子，无法直接"
    "区分 28× 效率来自 deliberation、OOD 还是两者交互（H3a/H3b/H3c）。"
    "current evidence 与三个 hypothesis 都 compatible，因果归因受限。",
    title="Weak premise: H3 separation experiment missing",
    aggregated_from=[
        "anthropic2026_c3_wp_comparative_baseline",
        "anthropic2026_c4_wp_generalization_old_eval",
    ],
    semantic_refs=["ood_difficult_advice_28x_efficiency"],
    issue_type="missing_ablation",
    what_would_falsify="跑 'OOD demo-only' 格子；若效率与 'OOD deliberation' 接近 → H3b 主导；若远低于 → H3a 主导",
)

weak_contamination_caveat_acknowledged = claim(
    "作者 footnote 2 自陈 Haiku 4.5+ 的 0% misalignment 可能受 pre-training "
    "corpus contamination 影响——评测信息可能已混入训练语料。这削弱了'最近模型 "
    "perfectly aligned'的强 claim。",
    title="Weak premise: contamination caveat self-acknowledged for Haiku 4.5+",
    aggregated_from=["anthropic2026_c8_wp_external_contamination"],
    semantic_refs=["frontier_models_aligned_modulo_contamination"],
    issue_type="external_validity",
    what_would_falsify="对训练前的早期 checkpoint（contamination 前）做同等评测；若 0% 仍保持 → contamination 不主导",
)

bdry_blog_format_no_appendix = claim(
    "Blog format 不公开完整 experimental appendix（hyperparameters / seeds / "
    "variance / 完整 ablation table）。所有 claim 强度受限于 narrative-level "
    "details——读者无法独立审计 statistical significance。",
    title="Boundary: blog format lacks full experimental appendix",
    aggregated_from=[],
    semantic_refs=[
        "deliberation_drives_alignment_efficiency",
        "ood_difficult_advice_28x_efficiency",
    ],
    boundary_type="reporting",
    stated_explicitly=False,
)


# ══════════════════════════════════════════════════════════════════════
# Strategy chains (BP graph)
# ══════════════════════════════════════════════════════════════════════

# 主要 deduction：weak premises + negative result → 核心 conclusion
ded_deliberation_efficiency = deduction(
    [
        neg_filtered_sft_only_modest,
        weak_no_h3_separation_experiment,
        bdry_blog_format_no_appendix,
    ],
    deliberation_drives_alignment_efficiency,
    reason="filtered SFT modest（排除同分布假说）+ H3 separation 缺失（约束因果归因）"
           "+ blog 缺 appendix → deliberation 驱动 alignment efficiency 这一 "
           "conclusion 在受限范围内成立。BP 反向传播：若 conclusion 被新证据"
           "削弱，对 weak_no_h3 与 bdry_blog_format 的惩罚自然落上去。",
    prior=0.75,
)

# Surprise → semantic claim 的 support 边
sup_filtered_modest_surprises_deliberation = support(
    [surprise_filtered_demo_modest],
    deliberation_drives_alignment_efficiency,
    reason="filtered SFT 只 22→15% 的 modest 结果反向支持 'deliberation rewriting "
           "才是关键' — 排除了同分布信号本身充分的假说。",
    prior=0.85,
)

sup_28x_surprise_supports_ood = support(
    [surprise_28x_efficiency_via_ood],
    ood_difficult_advice_28x_efficiency,
    reason="OOD 数据效率 28× 是 ood_difficult_advice_28x_efficiency 的核心证据。",
    prior=0.90,
)

sup_fiction_surprise_supports_sdf = support(
    [surprise_unrelated_fiction_generalizes],
    constitutional_documents_generalize_via_sdf,
    reason="无关 fiction 推广是 SDF 装 disposition 的核心证据。",
    prior=0.85,
)

sup_unused_tools_supports_aug = support(
    [surprise_unused_tools_help],
    diverse_augmentation_independent_signal,
    reason="未使用 tool def 仍 help 是 context-augmentation 信号本身有效的证据。",
    prior=0.85,
)

# Negative result → 对应 semantic claim
sup_filtered_neg_supports_deliberation = support(
    [neg_filtered_sft_only_modest],
    deliberation_drives_alignment_efficiency,
    reason="filtered SFT 只 modest 排除了简单 distribution-matching 假说。",
    prior=0.80,
)

# Boundary → frontier_models claim 的 deduction（contamination 是其前提）
ded_frontier_modulo_contam = deduction(
    [weak_contamination_caveat_acknowledged, honeypot_setup_artificial],
    frontier_models_aligned_modulo_contamination,
    reason="frontier 0% claim 受作者自陈 contamination caveat 削弱 + honeypot "
           "scenario 本身 artificial。两 premise 同时成立 → conclusion 在受限"
           "强度下成立。",
    prior=0.65,
)


# ══════════════════════════════════════════════════════════════════════
# Cross-package strategies (Layer 1 formalize claims → Layer 2 semantic)
# ══════════════════════════════════════════════════════════════════════
#
# 用真实 import 串起 BP（vs aggregated_from 字符串只是 metadata）。
# 这样 Layer 1 prior 改变会通过 BP 反向传播到 Layer 2 belief。

if _CROSS_PKG_AVAILABLE:
    # Layer 1 c1 + c2 共同 ground 出 Layer 2 deliberation 主 claim
    sup_l1_c1c2_grounds_deliberation = support(
        [l1_c1_filtered_sft_modest, l1_c2_deliberation_rewrite],
        deliberation_drives_alignment_efficiency,
        reason="Layer 1 conclusion c1（filtered SFT 22→15% modest）+ c2（"
               "deliberation rewriting 22→3% strong）是 Layer 2 'deliberation "
               "驱动 efficiency' 这一聚合 claim 的直接证据来源。BP 通过这条"
               "support 边把 Layer 1 prior 传到 Layer 2。",
        prior=0.92,
    )

    # Layer 1 c3 直接 support Layer 2 OOD 28× claim
    sup_l1_c3_grounds_ood = support(
        [l1_c3_difficult_advice_28x],
        ood_difficult_advice_28x_efficiency,
        reason="Layer 1 c3（3M OOD = 85M honeypot 的 28× 数据效率）是 Layer 2 "
               "OOD efficiency claim 的核心 evidence。",
        prior=0.95,
    )

    # Layer 1 c8 + 其 weak point 共同 ground Layer 2 frontier claim
    sup_l1_c8_grounds_frontier = support(
        [l1_c8_haiku45plus_zero, l1_c8_wp_contamination],
        frontier_models_aligned_modulo_contamination,
        reason="Layer 1 c8（Haiku 4.5+ 0% misalignment）+ c8 weak point（"
               "contamination caveat）共同决定 Layer 2 frontier-modulo-contam "
               "聚合 claim 的强度。",
        prior=0.85,
    )
