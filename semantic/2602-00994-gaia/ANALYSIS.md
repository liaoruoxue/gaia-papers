# Layer 2 Semantic Analysis — 2602.00994

> LEAS+DART: Reasoning and Tool-use Compete in Agentic RL
> Li, Yi, Li, Fan, Jiang, Chen, Li, Song, Zhang (2026)

**Layer 1 → Layer 2**: 96 claims + 39 settings + 32 strategies → **7 semantic claims + 5 strategies**

---

## Claim 筛选

从 Layer 1 96 条 claim 中按认知增量+可操作性+可争议性筛选：

### 核心 (core) — 5 条
| # | Semantic Claim | 为什么核心 |
|---|---------------|-----------|
| 1 | seesaw_phenomenon | 新现象：多能力训练有内在矛盾，不是"加数据就能解决" |
| 2 | gradient_conflict_is_root_cause | 归因：排除了数据比例假说，定位到梯度层面 |
| 3 | dart_solves_gradient_conflict | 解法：结构性梯度隔离，不是调参 |
| 4 | dart_vs_alternatives | 实用：比现有方法好多少？限制在哪？ |
| 5 | leas_diagnostic_framework | 工具：LEAS 本身是可复用的诊断方法 |

### 边界条件 — 2 条
| # | Claim | 为什么重要 |
|---|-------|-----------|
| 6 | no_llama_validation | 限制外推范围 |
| 7 | single_turn_scope | 限制应用场景 |

### 支撑 (supporting) — Layer 1 保留引文链
所有 5 条核心 claim 通过 `aggregated_from` 可追溯到 Layer 1 的具体实验 claim。

---

## 信念分析

> BP 方法: JT (exact)。Prior 来源: priors.py（每条有 justification）。

| Claim | Belief | Prior | Δ | 弱点 |
|-------|--------|-------|---|------|
| seesaw_phenomenon | **0.94** | 0.92 | +0.02 | 仅 7-8B, 单框架验证 |
| gradient_conflict_is_root_cause | **0.88** | 0.85 | +0.03 | 相关≠因果, 无干预实验 |
| dart_solves_gradient_conflict | **0.90** | 0.88 | +0.02 | 缺 Llama, ≤7B |
| dart_vs_alternatives | **0.78** | 0.75 | +0.03 | 2-agent 差距仅 1.2pp |
| leas_diagnostic_framework | **0.84** | 0.82 | +0.02 | 线性假设, logit≠behavior |

**Δ 全为正**——策略链增强了每条 claim 的支持力度。最大 Δ 是 gradient_conflict (+0.03) 和 dart_vs_alternatives (+0.03)，因为 abduction 成功排除了 data-mixture 备择假说。

---

## 弱点评级

| Claim | 信念 | 风险 | 为什么还需要关注 |
|-------|------|------|----------------|
| dart_vs_alternatives | 0.78 | 统计学不显著 | 1.2pp 差距在 LLM benchmark 方差范围内。如果后续更大规模实验显示差距扩大，结论需修正 |
| gradient_conflict_is_root_cause | 0.88 | 因果方向未验证 | LEAS 是线性测量，不能排除非线性的其他干扰机制。需要干预实验（人为注入已知梯度冲突→观测 seesaw） |
| leas_diagnostic_framework | 0.84 | 线性近似假象 | logit-level 分解可能不反映 auto-regressive 解码下的真实行为。需要行为层验证 |
| dart_solves_gradient_conflict | 0.90 | 外推不确定 | 无 70B+ 和 Llama 架构。不同架构的 gradient interaction 模式可能不同 |

---

## 策略链结构

```
seesaw_phenomenon (0.94)
  │
  └──[support 0.88]──→ gradient_conflict_is_root_cause (0.88)
                          │
                          └──[support 0.85]──→ dart_solves_gradient_conflict (0.90)
                                                  │
                          ┌───────────────────────┤
                          │                       │
            [induction 0.85]              [abduction 0.78]
              3 backbones                  data-mix alt excluded
                                                  │
                                          [contradiction]
                                          vs 2-agent capacity ceiling
```

策略类型分布：support ×2, induction ×1, abduction ×1, contradiction ×1（对比 Layer 1 的 28 support + 1 deduction + 3 induction，去掉了 compiler 胶水，加了 abduction 和 contradiction）

---

## KB 映射

| 语义 Claim | 对位 chunk | 关系 | 行动 |
|-----------|-----------|------|------|
| seesaw_phenomenon | **rl-training.md** | **new** — 当前 chunk 未涉及多能力训练 interference | 新建 §Capability Interference 节 |
| gradient_conflict_is_root_cause | **rl-training.md** (已有 gradient conflict 讨论) | **refine** — 现有讨论偏 RL 理论，LEAS 提供了测量工具 | 补充 LEAS 作为诊断方法引用 |
| dart_solves_gradient_conflict | **rl-training.md** | **confirm + refine** — DART 确认了 gradient conflict 可解，提供了具体方法 | 升级相关 [单篇]→[实证]，加 DART 作为解决方案引用 |
| dart_vs_alternatives | **harness-design.md** | **refine** — 1-model vs 2-agent 是 harness 设计选择 | 在 harness 设计讨论中引用 DART 的效率数据 |
| leas_diagnostic_framework | **verification.md** | **new** — LEAS 可作为机制级验证工具 | 在 verification chunk 中引用 LEAS 作为分析工具 |

### 关系总结
- **new**: 2 (seesaw, LEAS)
- **refine**: 2 (gradient conflict, DART vs alternatives)
- **confirm**: 1 (DART solves)
- **contradict**: 0

---

## 行动建议

1. **[P0] 更新 rl-training.md** — 新增 "Capability Interference in Multi-Objective RL" 节，包含 seesaw 现象描述 + LEAS 诊断框架 + DART 解决方案。当前 chunk 讨论 GRPO/PPO gradient 问题但未涉及多能力竞争。
2. **[P1] 升级 [单篇]→[实证]** — 检查 rl-training.md 中是否有仅 LEAS/DART 单篇支撑的结论，如有且本次确认→升级。
3. **[P1] 跨 chunk 引用** — harness-design.md 引用 DART 的 1-model efficiency 数据；verification.md 引用 LEAS 作为机制级验证工具。
4. **[P2] 追踪** — dart_vs_2agent 的 1.2pp 差距。如果在后续论文中看到更大规模实验（70B+, Llama），需重新评估结论。
