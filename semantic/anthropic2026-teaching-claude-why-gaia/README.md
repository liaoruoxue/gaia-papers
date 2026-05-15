# anthropic2026-teaching-claude-why-semantic-gaia

Layer 2 semantic analysis of Anthropic blog "Teaching Claude Why" (2026-05-08).

**Source Layer 1**：`agent-docs/gaia-packages/anthropic2026-teaching-claude-why-gaia/`（formalize 4-phase 产出，8 conclusion + 8 weak_point + 8 deduction）

**实验目的（2026-05-10）**：验证 formalize 产出能否被 gaia-semantic 工作流消费——不匹配点排查 + cross-package string anchor 是否实际能跑通 BP。

## Aggregation 原则

Layer 1 的 8 个 conclusion + 8 weak_point → Layer 2 的 5-7 个 semantic claim + 5 类 judgment。

主线：deliberation > demo（C1+C2 合并）；OOD difficult-advice 是 28× 效率核心机制（C3+C4 合并）；constitutional + fiction 推广（C5+C6 合并）；diverse augmentation 独立信号（C7）；scale + contamination caveat（C8）。
