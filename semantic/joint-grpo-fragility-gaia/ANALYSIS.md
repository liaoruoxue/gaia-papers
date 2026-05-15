# Joint Layer 2 — GRPO Fragility (3-paper)

三篇论文围绕 GRPO-based agent RL 的不同观察。**模式 2（boundary）**：两篇正向 + 一篇反向，joint 推断给出 axis-specific 的精细化结论。

**依赖**：
- `2602-00994-gaia` (DART) — 正向：seesaw 多能力干扰
- `2604-06159-gaia` (TPO) — 正向：sparse-reward 失效
- `2604-23747-gaia` (SFT-then-RL) — 反向：标准 math + 修好的 baseline 上 GRPO 没毛病

**Joint factor graph**：`gaia infer --depth 1` 合并 **45 variables, 20 factors**。

---

## 跨论文论证结构

```
[2602.00994 DART]              [2604.06159 TPO]
seesaw_phenomenon              tpo_excels_on_sparse_reward
(capability axis)              (reward axis)
       │                              │
       └──────────┬───────────────────┘
                  │
                  │       ┌──[2604.23747 SFT-then-RL]
                  │       │  mixed_policy_gains_are_artifact (artifact!)
                  │       │  sft_then_rl_sufficient (math 上 GRPO 够用)
                  │       │       │
                  │       │       ↓
                  │       └──→ bdry_grpo_fine_on_corrected_math
                  │                    │
                  ↓                    │
              deduction ←──────────────┘
                  ↓
      grpo_has_systemic_weakness  (axis-specific)
                  prior 0.55 → posterior 0.87
```

**关键设计**：SFT 论文的反方向证据**不是用 `contradiction`**（那会硬撕主 claim），而是包成 boundary premise + 直接引用 SFT 的 motivation claim 进 deduction，让 BP 软调。

---

## BP 信念（Joint）

| Claim | Source | Joint Posterior | Note |
|-------|--------|-----------------|------|
| `mixed_policy_gains_are_artifact` | 2604.23747 | **0.998** | SFT 反方向证据被 joint 强化 |
| `tpo_excels_on_sparse_reward` | 2604.06159 | **0.996** | 单篇 0.995，joint 略升 |
| `sft_then_rl_sufficient` | 2604.23747 | **0.978** | |
| `seesaw_phenomenon` | 2602.00994 | **0.954** | 单篇 0.951，joint 略升 |
| `bdry_grpo_fine_on_corrected_math` | joint | **0.925** | 反方向证据合成的 boundary，被 SFT 拉高 |
| `grpo_has_systemic_weakness` | joint | **0.872** | prior 0.55 → 0.87 |

**对照实验**：
- 仅 DART + TPO 时：`grpo_has_systemic_weakness = 0.932`（无反向证据）
- 加入 SFT 反方向：`= 0.872`（**降低 0.06**）

这是想要的方向——多了一个反方向证据后，主结论信念被合理精细化（**axis-specific 而不是 universal**）。

---

## KB 映射建议

写入 `rl-training.md` 时应明确：

> **GRPO-based agent RL 的 axis-specific 弱点**
>
> 三篇论文给出 nuanced 结论：
> - 多能力训练：DART (2602.00994) 观察到 seesaw 现象，梯度层面负干扰
> - Sparse reward：TPO (2604.06159) 观察到 PG 方法在 zero-reward 上学不动
> - **反方向**：SFT-then-RL (2604.23747) 表明在标准 math 7-8B 上，**只要 baseline 修对**，GRPO + 简单 SFT-then-RL 就够好
>
> 综合 BP 信念 0.87：GRPO 弱点真实存在，但**axis-specific**（在多能力 / sparse reward 轴上），不是无差别的"系统性破"。在标准 reasoning benchmark 上 GRPO 仍然 viable。

---

## 操作备注

- 加第 4 篇时，先**预测信念变化方向**：
  - 若是同向证据（更多 GRPO 失败案例）→ 期望 `grpo_has_systemic_weakness` 略升（但 boundary 不动）
  - 若是反方向证据（GRPO 修复方案）→ 期望主 claim 略降，boundary 被强化
  - 若是新轴向证据（如 GRPO 在多 turn 失效）→ 主 claim 升，可能要新建 boundary
- 跑完 BP 看是否符合预期；不符合就是建模错（多半是 strategy premise 列错了）
- 当前 3 篇 BP 27 ms 收敛，加到 10 篇预期仍秒级；超过 30 篇考虑分层 joint（见 SKILL.md 模式 3）
