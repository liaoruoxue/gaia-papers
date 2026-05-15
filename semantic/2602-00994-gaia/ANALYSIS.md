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

---

## KB 映射

| 语义 Claim | 对位 chunk | 关系 | 行动 |
|-----------|-----------|------|------|
| seesaw_phenomenon | **rl-training.md** | **new** — 当前 chunk 未涉及多能力训练 interference | 新建 §Capability Interference 节 |
| gradient_conflict_is_root_cause | **rl-training.md** (已有 gradient conflict 讨论) | **refine** — 现有讨论偏 RL 理论，LEAS 提供了测量工具 | 补充 LEAS 作为诊断方法引用 |
| dart_solves_gradient_conflict | **rl-training.md** | **confirm + refine** — DART 确认 gradient conflict 可解 | 升级相关 [单篇]→[实证]，加 DART 作为解决方案 |
| dart_vs_alternatives | **harness-design.md** | **refine** — 1-model vs 2-agent 是 harness 设计选择 | 在 harness 设计讨论中引用 DART 效率数据 |
| leas_diagnostic_framework | **verification.md** | **new** — LEAS 可作为机制级验证工具 | 在 verification chunk 引用 LEAS |

---

## 行动建议

1. **[P0]** 更新 `rl-training.md`，新增 §Capability Interference：seesaw 现象 + LEAS 诊断 + DART 解法
2. **[P1]** 升级 rl-training.md 中相关 [单篇]→[实证] 标签
3. **[P1]** 跨 chunk 引用：harness-design.md 引用 DART 效率数据；verification.md 引用 LEAS
4. **[P2]** 追踪 dart_vs_2agent 的 1.2pp 差距，若后续看到 70B+/Llama 更大实验需重评

---

## 判断节点（5 类）

### Surprising Points（反直觉发现）

| # | 现象 | 为什么反直觉 | Δ(prior→post) |
|---|------|------------|---------------|
| 1 | `surprise_data_mix_useless` | 推翻"多任务干扰靠数据工程解决"的常识；λ23 跨 mix 稳定为负 | 0.90 → 0.94 |
| 2 | `surprise_dart_rank_insensitive` | LoRA rank 不是瓶颈，routing 机制才是 | 0.88 → 0.91 |

### Elegant Points（方法之美）

| # | 设计 | 美在哪 | 可移植性 |
|---|------|-------|----------|
| 1 | `elegant_dart_token_routing` | 一个结构改动替代 4 种 ad-hoc trick；零交互项可证 | high |
| 2 | `elegant_leas_decomposition` | 6 模型 + 线性代数显式分离 λ23，不动训练流程 | medium |

### Weak Points（弱点）

| # | 弱点 | 类型 | 怎么证伪 |
|---|------|------|---------|
| 1 | `weak_dart_vs_2agent_marginal` | weak_evidence | 多 seed ≥5 给 95% CI；跨 0 则结论不成立 |
| 2 | `weak_correlation_not_causation` | alt_not_excluded | 干预实验：注入合成梯度冲突 / 投影到正交子空间 |
| 3 | `weak_leas_logit_only` | hidden_assumption | λ23≈0 ckpt 做行为级 A/B |

### Boundary Conditions（适用前提）

| # | 前提 | 类型 | 跨论文影响 |
|---|------|------|-----------|
| 1 | `bdry_qwen_only` | scope | Llama 上反例先按 boundary 处理 |
| 2 | `bdry_lora_only` | simplification | 全参 fine-tune 下"零交互"保证不成立 |
| 3 | `no_llama_validation` | scope（作者明说） | 限制外推范围 |
| 4 | `single_turn_scope` | scope（作者明说） | 多轮 SAC 外推需重证 |

### Negative Results（作者自陈失败）

| # | 失败实验 | 为什么有信息量 | 对我们 |
|---|--------|--------------|-------|
| 1 | `neg_data_mix_fails` | 排除"数据不平衡"备择解释 | 不要走纯数据工程路线 |
| 2 | `neg_task_lora_fails` | 排除"任何 modular 加法都行"，凸显 token-routing 必要 | 别用 task-level 路由偷懒 |
| 3 | `neg_inference_hybrid_fails` | 划清 LEAS 边界：诊断 ≠ 可部署解耦 | 不要把 LEAS 分解当 deployment artifact |

详见 `src/2602_00994/s2_strategies.py`。

---

## BP 信念分析（deduction-based 图）

**策略**：Weak/Boundary 作为 `deduction` premise 进图（rigid implication + 反向流动）；Surprising/Negative 作为 `support` premise；Elegant 孤岛。

| Claim | Prior | Posterior | Δ |
|-------|-------|-----------|---|
| `gradient_conflict_is_root_cause` | 0.850 | **0.995** | +0.145 |
| `dart_solves_gradient_conflict` | 0.880 | **0.964** | +0.084 |
| `dart_vs_alternatives` | 0.750 | **0.942** | +0.192 |
| `leas_diagnostic_framework` | 0.820 | 0.869 | +0.049 |
| `seesaw_phenomenon` | 0.920 | 0.951 | +0.031 |
| `bdry_qwen_only` | 0.970 | 0.978 | +0.008 |
| `bdry_lora_only` | 0.950 | 0.964 | +0.014 |
| `weak_dart_vs_2agent_marginal` | 0.850 | 0.888 | +0.038 |
| `weak_leas_logit_only` | 0.920 | 0.920 | 0.000 |
| `weak_correlation_not_causation` | 0.900 | 0.900 | 0.000 |
| `surprise_data_mix_useless` | 0.900 | 0.939 | +0.039 |
| `surprise_dart_rank_insensitive` | 0.880 | 0.913 | +0.033 |
| `neg_data_mix_fails` | 0.900 | 0.939 | +0.039 |
| `neg_task_lora_fails` | 0.880 | 0.913 | +0.033 |
| `neg_inference_hybrid_fails` | 0.880 | 0.913 | +0.033 |
| `elegant_dart_token_routing` | 0.850 | 0.850 | 0.000 |
| `elegant_leas_decomposition` | 0.800 | 0.800 | 0.000 |

**解读**：
- 主 claim 全部上升合理区间（0.87-0.99）
- 关键的 `gradient_conflict_is_root_cause` 从 0.85 → 0.995，说明两路 support（seesaw + neg_data_mix_fails + surprise_data_mix_useless）和下游 deduction 的反向流动共同推高
- `dart_vs_alternatives` 涨幅最大（+0.192），因为它只有一条 inbound deduction，证据链清晰
- Weak/Boundary 作为 deduction premise 被轻微上抬（+0.008 ~ +0.038），表示这些适用条件在当前证据下是被认可的；若将来出现反例（如 Llama 跑 DART 没效果），BP 会反向拉低它们，凸显"这些适用条件值得怀疑"
- Elegant 节点 Δ=0（孤岛，按设计）
- 无后验饱和（>0.999）

**跨论文 joint BP**：参见 `semantic/joint-grpo-fragility-gaia/` 包，DART 的 `seesaw_phenomenon` 在 joint 图里被 joint 结论 `grpo_has_systemic_weakness` 反向加强（0.951 → 0.958）。
