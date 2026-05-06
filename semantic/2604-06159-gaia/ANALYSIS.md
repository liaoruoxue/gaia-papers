# Layer 2 — 2604.06159: Target Policy Optimization

**Layer 1 → Layer 2**: 158 claims + 72 strategies → **4 semantic claims + 4 strategies**

---

## 信念分析

| Claim | Belief | Prior | Δ | 弱点 |
|-------|--------|-------|---|------|
| tpo_decouples_rl | **0.92** | 0.90 | +0.02 | η 温度仍是超参; 仅标量反馈 |
| tpo_excels_on_sparse_reward | **0.87** | 0.85 | +0.02 | PG baselines 未精细调参; 无多步任务 |
| tpo_matches_on_dense_reward | **0.84** | 0.82 | +0.02 | 仅 WebArena-Turbo 简化版; 仅 7B |
| tpo_simplicity_advantage | **0.90** | 0.88 | +0.02 | 无消融实验确定哪个组件最重要 |

---

## 弱点评级

| Claim | 信念 | 风险 |
|-------|------|------|
| tpo_excels_on_sparse_reward | 0.87 | PG 调参后差距可能缩小; solve-vs-not-learn 的 gap 降低风险 |
| tpo_matches_on_dense_reward | 0.84 | 仅 WebArena-Turbo 简化版; 无 full benchmark; 仅 7B |

---

## KB 映射

| Claim | Chunk | 关系 | 行动 |
|-------|-------|------|------|
| tpo_decouples_rl | **rl-training.md** | **new** — decoupled RL 是不同于 PG 的新范式 | 新建 §Decoupled RL 节 |
| tpo_excels_on_sparse_reward | **rl-training.md** | **refine** — sparse reward 是 agent RL 的核心挑战 | 补充 TPO 作为 sparse-reward 方案 |
| tpo_matches_on_dense_reward | **rl-training.md** | **confirm** — no-regret 属性使 TPO 可作 default | 引用为 PG 替代方案 |
| tpo_simplicity_advantage | **harness-design.md** | **refine** — agent training 的工程选择 | 在训练基础设施讨论中引用 |
