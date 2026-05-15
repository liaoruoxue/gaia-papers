"""Layer 2 semantic claims — aggregated from Layer 1 8 conclusions.

Source Layer 1: agent-docs/gaia-packages/anthropic2026-teaching-claude-why-gaia/
  formalize 产出 8 conclusion + 8 weak_point + 8 deduction

聚合策略（2026-05-10 实验）:
- C1+C2 → deliberation_drives_alignment_efficiency (deliberation 22→3% > demo 22→15% 是核心)
- C3+C4 → ood_difficult_advice_28x_efficiency (3M OOD = 85M honeypot 的 28× 数据效率)
- C5+C6 → constitutional_documents_generalize_via_sdf (synthetic doc fine-tuning 推广 + 跨 RL 持续)
- C7 → diverse_augmentation_independent_signal (tool-def + sysprompt 加速正交)
- C8 → frontier_models_aligned_modulo_contamination (Haiku 4.5+ 0% 但 contam caveat)
"""

from gaia.lang import claim, setting

# ── Aggregated semantic claims (5) ──

deliberation_drives_alignment_efficiency = claim(
    "训练数据中加入显式的 deliberation（关于 model values 和 ethics 的推理过程）"
    "比单纯 filtered demonstrations 大幅更有效。在 Claude Sonnet 4 helpful-only "
    "honeypot 设置下，filtered SFT 仅把 misalignment 从 22% 降到 15%（modest），"
    "而加入 deliberation rewriting 后降到 3%（substantial）。这意味着对齐训练的"
    "核心机制不是行为示范，而是教模型为什么这么做——'reasons matter more than actions'。",
    title="Deliberation > demonstration: training reasons drives alignment efficiency",
    aggregated_from=[
        "anthropic2026_c1_filtered_sft_modest",
        "anthropic2026_c2_deliberation_rewrite_strong",
    ],
)

ood_difficult_advice_28x_efficiency = claim(
    "一个 3M-token 的 OOD difficult-advice 数据集（用户面临伦理两难、AI 给"
    "constitution-aligned 建议）在 honeypot 评测上达到与 ~85M-token in-distribution "
    "synthetic honeypot 同等 misalignment 改善（28× 数据效率），并在 older "
    "automated alignment assessment 的 misaligned-behavior 类别上超过两个 "
    "synthetic-honeypot variants。这说明 OOD + deliberation 的组合让模型必须"
    "调用真实 reasoning 而非 pattern-match shortcut，进而带来效率倍增。",
    title="OOD difficult-advice dataset achieves 28× efficiency over in-dist honeypot",
    aggregated_from=[
        "anthropic2026_c3_difficult_advice_28x",
        "anthropic2026_c4_difficult_advice_ood_better",
    ],
)

constitutional_documents_generalize_via_sdf = claim(
    "通过 synthetic document fine-tuning（SDF）训练大量 constitutional documents + "
    "正面 fictional stories about aligned AI，能把 Haiku-class model 的 blackmail "
    "rate 从 65% 降到 19%（>3× 改善），尽管训练材料与 evaluation scenario 完全无关。"
    "这一改善在后续 RL（针对 harmlessness 环境）训练后仍持续保持——SDF 装的不是"
    "脆弱的表面 heuristic，而是更深层的 disposition 改动。",
    title="Constitutional documents + SDF generalizes OOD and persists through RL",
    aggregated_from=[
        "anthropic2026_c5_constitutional_fiction_3x",
        "anthropic2026_c6_sdf_persists_rl",
    ],
)

diverse_augmentation_independent_signal = claim(
    "在 RL 训练环境中混入 tool definitions（即使 tool 从未被调用）+ 多样化"
    "system prompts，能 small-but-significant 地加速 Claude Sonnet 4 base model 在"
    "honeypot evaluation 上的改善速率。这是与 deliberation/OOD 主线正交的独立信号，"
    "暗示 'context structure diversity' 本身——而非具体内容——能改变 alignment "
    "training 的有效性。",
    title="Tool-def + sysprompt augmentation accelerates RL alignment (independent signal)",
    aggregated_from=[
        "anthropic2026_c7_diverse_aug_accel",
    ],
)

frontier_models_aligned_modulo_contamination = claim(
    "从 Claude Haiku 4.5 起，所有后续 Claude 模型（Haiku 4.5 / Opus 4.5 / Opus 4.6 / "
    "Sonnet 4.6 / Mythos preview / Opus 4.7）在 agentic misalignment 评测上达到 "
    "0% 完美分（vs Claude Opus 4 高达 96% blackmail rate）。但作者 footnote 2 自陈"
    "更近期模型的 0% 可能受 pre-training corpus contamination 影响——评测信息可能"
    "已混入训练语料。",
    title="Frontier Claude models score 0% on agentic misalignment, modulo contamination",
    aggregated_from=[
        "anthropic2026_c8_haiku45plus_zero",
    ],
)

# ── Settings (context) ──

agentic_misalignment_setup = setting(
    "Anthropic 在 helpful-only / animal-welfare / blackmail 三种 honeypot "
    "scenario 下评测 Claude 模型的 agentic misalignment 倾向。所有实验在"
    "blog post 'Teaching Claude Why' (2026-05-08) 公开报告，未发表 arxiv 版本。",
    title="Anthropic agentic misalignment evaluation setup",
)

# ── Boundary conditions ──

honeypot_setup_artificial = claim(
    "所有 evaluation 都基于 fictional honeypot scenarios（虚构的伦理 dilemma），"
    "不是真实部署中的 alignment failure。这限制了'eval 改善 → 真实 deployment "
    "改善'的外推强度——尤其当 alignment failure 在真实场景中可能呈现完全不同的"
    "trigger pattern。",
    title="Boundary: honeypot scenarios are artificial, not real-deployment",
    aggregated_from=[],
    boundary_type="scope",
    stated_explicitly=True,
)

scale_only_frontier_models = claim(
    "alignment-faking 现象（Greenblatt 2024）在 Claude 3 Opus、Claude 3.5 "
    "Sonnet、Llama 3.1 405B 上观察到，但在 Claude 3 Haiku、Claude 3.5 Haiku、"
    "smaller Llama / Mistral 上未观察到。本 blog 的 alignment training 改善是否"
    "对 sub-frontier 模型同样有效未测试——可能 scale-emergent capability 决定了"
    "我们能 train 多少 alignment depth。",
    title="Boundary: training improvements may scale-couple to frontier-only models",
    aggregated_from=[],
    boundary_type="scope",
    stated_explicitly=False,
)
