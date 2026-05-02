# DeepSeek Visual Primitives — Thinking with Visual Primitives

**日期**: 2026-05-01
**来源**: DeepSeek-AI + 北京大学 + 清华大学 (2026-04-30, GitHub 发布后撤回)
**标识**: GitHub (无 arxiv ID)
**状态**: 论文已删除，内容来自 CSDN 精读 + 多源新闻报道交叉验证

---

## 0. TL;DR

1. **核心区分**：多模态推理的瓶颈不是 Perception Gap（看不清）而是 Reference Gap（指不准）——自然语言在连续视觉空间中天生不具备精确指代能力。
2. **解法**：把 `<|box|>` 和 `<|point|>` 坐标提升为和文字 token 同等的"思维单元"，直接嵌入 CoT，让模型"边推理边指"。
3. **架构**：DeepSeek-ViT + V4-Flash (284B/13B MoE)，7056x 视觉压缩（756×756 → 81 KV entries）。
4. **训练**："专家-合并-蒸馏"三阶段 GRPO 管线，3-way Reward Model（format/quality/accuracy），从 9.8 万数据源筛选 3.2 万 → 4000 万+样本。
5. **与 DeepSeek-OCR 2 形成完整 pipeline**：OCR 2 做前端"语义编码顺序"，Visual Primitives 做后端"动态空间指代"。

---

## Layer 1: 三句话总结

**问题**：多模态 LLM 用自然语言描述空间位置时天然模糊（"左边那个大的红色物体"），在密集场景中导致注意力漂移和逻辑崩塌。

**解法**：将点坐标和边界框作为视觉原语直接嵌入思维链，让模型在推理时同步输出空间锚点——不再是"描述位置"而是"指位置"。

**结果**：在极低 token 成本下（81 视觉 KV），迷宫导航 66.9%（GPT-5.4 50.6%）、路径追踪 56.7%（Claude 30.6%），证明了"信息密度 > 信息量"。

---

## Layer 2: 关键细节

### 2.1 架构

| 组件 | 细节 |
|------|------|
| Vision Encoder | DeepSeek-ViT (自研)，14×14 patch，支持任意分辨率 |
| 空间压缩 | 3×3 patch → 1 token（沿 channel 维度合并） |
| KV 压缩 | CSA (Compressed Sparse Attention) 4× |
| 语言骨干 | DeepSeek-V4-Flash，MoE 284B total / 13B activated |
| 端到端压缩 | 756×756：2916 patches → 324 tokens → ~81 KV entries = 7056x |

### 2.2 数据 Pipeline

**预训练数据筛选**（两阶段质量审核）：

| 阶段 | 输入 | 输出 | 过滤内容 |
|------|------|------|---------|
| Semantic Review (MLLM) | 97,984 数据源 | 43,141 | 纯数字类别、私人标签、模糊缩写 |
| Visual-Geometric | 43,141 | 31,701 | 严重缺标注(>50%)、截断偏移、巨框(>90%) |

**冷启动数据**（post-training）：

| 任务 | 样本量 | 关键设计 |
|------|--------|---------|
| Counting | ~10K | 粗粒度（COCO 密集检测）+ 细粒度（GQA scene graph 生成） |
| Spatial Reasoning/VQA | ~9K | 自然场景 + CLEVR 合成 + 负样本（不存在物体的查询） |
| Maze Navigation | 460K | DFS/Prim/Kruskal 生成，三种拓扑（矩形/圆形/六边形），含死路迷宫 |
| Path Tracing | 125K | Bezier 曲线，同色同宽防止 color shortcut，交点处局部几何连续性 |

### 2.3 训练策略："专家-合并-蒸馏"

```
Phase 1: 分别训 Box Expert (F_TwG) 和 Point Expert (F_TwP)
         ↓  (避免 pattern conflict — 分离训练)
Phase 2: 各自 GRPO RL，3-way Reward Model
         ↓
Phase 3: RFT (Rejection Fine-Tuning) — 用 experts 生成 rollout
         ↓
Phase 4: On-Policy Distillation — 统一模型 F
```

**Reward Model 三维并行**：
- **Format RM**（规则，0-1）：验证原语格式、检测冗余框
- **Quality RM**（LLM 评判，{0, 0.5, 1.0}）：冗余、一致性、自相矛盾、reward hacking
- **Task-Specific Accuracy RM**：各任务独立（计数用平滑指数衰减、迷宫用探索进度+wall violation+路径有效性）

### 2.4 实验结果

| 基准 | DeepSeek | GPT-5.4 | Claude 4.6 | Gemini-3-Flash |
|------|----------|---------|------------|----------------|
| Pixmo-Count | **89.2%** | 76.6% | 68.7% | 88.2% |
| Maze Navigation | **66.9%** | 50.6% | 48.9% | 49.4% |
| Path Tracing | **56.7%** | 46.5% | 30.6% | 41.4% |

迷宫和路径追踪上，所有前沿模型都在随机猜测线（50%）附近，DeepSeek 显著超越。

---

## Layer 3: 关键区分点 + 局限性

### 3.1 "Reference Gap" vs "Perception Gap"

业界主流（GPT-5.4, Claude, Gemini）仍集中在 Perception Gap——更高分辨率、更多 token。本文论证这条路被自然语言的 referential ambiguity 卡住了上限。**多模态的 next frontier 不是"看得更清"而是"指得更准"**。

### 3.2 触发词依赖 = 内在化不完整

模型需要明确触发词才能激活视觉原语——说明还没有学会"何时该指"。这和 paper2arm 中 ARM 7 modality 的 Execution/Skill 面临同样问题：agent 需要被指示才去 invoke，无法自主判断时机。

### 3.3 拓扑泛化弱 = sharpening-vs-generalization 张力

迷宫同分布强但跨场景弱，对应 RL 中 reward 越精细 in-domain 越强但 OOD 越弱的经典 tradeoff。

### 3.4 与 DeepSeek-OCR 2 (2601.20552) 的 pipeline 对位

| 维度 | OCR 2 | Visual Primitives |
|------|-------|-------------------|
| 问题 | Raster-scan 强加非语义顺序 | 自然语言无法精确指代 |
| 解法 | Causal Flow — 学习"该按什么顺序读" | 坐标入 CoT — "边推理边指" |
| 压缩信念 | 256-1120 token 匹配 Gemini-1.5 Pro | 81 KV 超越 GPT-5.4/Claude |
| 手段 | 两段 1D causal → 2D 理解 | 3×3 压缩 + CSA 4× |

**共同元命题**：视觉信息的"组织方式"比"信息量"更重要。两条线都是"大幅压缩 + 智能选择关注点"，和业界"尽量多保留 token"形成明确对立。

**完整 pipeline**：
```
OCR 2（前端编码）     →     V4-Flash（理解）    →    Visual Primitives（后端推理）
"按语义顺序读图"      →     MoE 理解          →     "在 CoT 中指位置"
encoding order        →     comprehension     →     pointing during reasoning
```

---

## Layer 4: 知识库更新

### 需要更新的 chunks

**`chunks/rl-training.md`**：
- 加"专家-合并-蒸馏"作为 GRPO 中不同能力冲突的缓解方案实例（继 LEAS+DART dual LoRA 之后的第二个独立实例）
- 加 3-way RM 设计（format/quality/accuracy 并行打分）作为 reward engineering 参考

**`chunks/verification.md`**：
- 加"空间指代精度"作为多模态 verification 的新维度
- Reference Gap 概念——自然语言的 referential ambiguity 不只在视觉中存在

---

## 来源

- CSDN 精读: https://blog.csdn.net/youcans/article/details/160676169
- 凤凰科技: https://tech.ifeng.com/c/8slgmYsDImm
- 36氪: https://eu.36kr.com/en/p/3789208597372165
- GitHub (已删除): https://github.com/deepseek-ai/Thinking-with-Visual-Primitives
- DeepSeek-OCR 2: https://arxiv.org/abs/2601.20552
