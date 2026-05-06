# Layer 2 — 2604.23747: SFT-then-RL Beats Mixed-Policy

**Layer 1 → Layer 2**: 160 claims + 51 strategies → **4 semantic claims + 4 strategies**

---

## 信念分析

| Claim | Belief | Prior | Δ | 弱点 |
|-------|--------|-------|---|------|
| two_bugs_suppress_sft_baseline | **0.97** | 0.96 | +0.01 | 仅验证 DeepSpeed ZeRO-1/2; ZeRO-3 未测 |
| mixed_policy_gains_are_artifact | **0.95** | 0.93 | +0.02 | 仅 math domain; 其他 domain 的 bug 影响可能不同 |
| sft_then_rl_sufficient | **0.87** | 0.85 | +0.02 | ≤8B; 无 coding/agent 验证 |
| cross_framework_validation_essential | **0.94** | 0.92 | +0.02 | 方法论主张; 需更多案例积累 |

---

## 弱点评级

| Claim | 信念 | 风险 |
|-------|------|------|
| sft_then_rl_sufficient | 0.87 | 外推不确定 — 仅 math + 7-8B。更大模型或不同 domain，mixed-policy 可能仍有价值 |

---

## KB 映射

| Claim | Chunk | 关系 | 行动 |
|-------|-------|------|------|
| two_bugs_suppress_sft_baseline | **rl-training.md** | **new** — 当前无 framework bug 讨论 | 加 §Infrastructure Bugs 警告 |
| mixed_policy_gains_are_artifact | **rl-training.md** | **refine** — 对 mixed-policy 方法加 caveat | 已有方法引用处加 footnote |
| cross_framework_validation_essential | **verification.md** | **confirm** — 强化现有的 cross-validation 讨论 | 引用为案例 |
