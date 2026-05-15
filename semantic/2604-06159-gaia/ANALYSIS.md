# Layer 2 — 2604.06159: Target Policy Optimization

**Layer 1 → Layer 2**: 158 claims + 72 strategies → **5 semantic claims + 4 judgment claims + 4 strategies**

TPO decouples agent RL into Q1 (build target distribution from environment feedback) + Q2 (cross-entropy fit policy to target). Eliminates critic, value function, off-policy correction.

---

## KB 映射

| Claim | Chunk | 关系 | 行动 |
|-------|-------|------|------|
| `tpo_decouples_rl` | **rl-training.md** | **new** — decoupled RL 是不同于 PG 的新范式 | 新建 §Decoupled RL 节 |
| `tpo_excels_on_sparse_reward` | **rl-training.md** | **refine** — sparse reward 是 agent RL 核心挑战 | 补充 TPO 为 sparse-reward 方案 |
| `tpo_matches_on_dense_reward` | **rl-training.md** | **confirm** — no-regret 属性使 TPO 可作 default | 引用为 PG 替代方案 |
| `tpo_simplicity_advantage` | **harness-design.md** | **refine** — agent training 工程选择 | 在训练基础设施讨论中引用 |

---

## 判断节点

### Weak Points

| # | 弱点 | 类型 | 怎么证伪 |
|---|------|------|---------|
| 1 | `weak_pg_baselines_undertuned` | alt_not_excluded | 对 PG 做专门的超参扫描，看能否逼近 TPO |
| 2 | `weak_no_multistep` | scope_limit | 跑 SWE-bench / WebArena-full / 多步 agent benchmark |

### Boundary Conditions

| # | 前提 | 类型 | 作者明说 |
|---|------|------|---------|
| 1 | `bdry_online_rl_only` | scope | 是（不比较 RLHF/DPO） |
| 2 | `bdry_7b_scale` | scope | 否（实验设置隐含） |

---

## BP 信念分析（deduction-based 图）

| Claim | Prior | Posterior | Δ |
|-------|-------|-----------|---|
| `tpo_excels_on_sparse_reward` | 0.850 | **0.995** | +0.145 |
| `tpo_simplicity_advantage` | 0.880 | **0.990** | +0.110 |
| `tpo_decouples_rl` | 0.900 | **0.984** | +0.084 |
| `tpo_matches_on_dense_reward` | 0.820 | **0.977** | +0.157 |
| `bdry_online_rl_only` | 0.970 | 0.982 | +0.012 |
| `weak_no_multistep` | 0.950 | 0.979 | +0.029 |
| `bdry_7b_scale` | 0.950 | 0.967 | +0.017 |
| `no_rlhf_comparison` | 0.950 | 0.950 | 0.000 |
| `bandit_and_single_task` | 0.930 | 0.930 | 0.000 |
| `weak_pg_baselines_undertuned` | 0.850 | 0.908 | +0.058 |

**解读**：
- `tpo_matches_on_dense_reward` 涨幅最大（+0.157）——deduction 链条清晰，主 claim 承接了 decouple 机制的上游信念
- `tpo_excels_on_sparse_reward` 升到 0.995——两条 support 路径（mechanism-driven + empirical evidence）+ deduction 反向流动叠加
- Weak / Boundary 作为 deduction premise 被轻微上抬（+0.012 ~ +0.058），表示在当前证据下这些适用条件不被质疑；若外部反例出现会反向降低
- 无后验饱和

## 行动建议

1. **[P0]** `rl-training.md` 新增 §Decoupled RL：TPO 与 PG/PPO/GRPO 的对比
2. **[P1]** `harness-design.md` 引用 TPO 作为"无 critic / value / GAE"的简化训练选型
3. **[P1]** 跟踪 PG tuning 工作：若后续看到专门的 PG 超参扫描能逼近 TPO，需要回来更新 `weak_pg_baselines_undertuned`
4. **[P2]** 跟踪多步 agent benchmark 上的 TPO 数据

---

**跨论文 joint BP**：参见 `semantic/joint-grpo-fragility-gaia/`，TPO 的 `tpo_excels_on_sparse_reward` 在 joint 图里被 `grpo_has_systemic_weakness` 反向加强（0.995 → 0.996）。与 DART 的 `seesaw_phenomenon` 联合支撑"GRPO 有系统性弱点"的跨论文结论。
