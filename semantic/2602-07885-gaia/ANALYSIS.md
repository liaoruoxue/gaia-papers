# Layer 2 — 2602.07885: Compression-Fidelity in Agentic Memory

**L1 → L2**: 107 claims + 36 strategies → **3 semantic claims + 2 boundary**

---

## 信念分析

| Claim | Belief | Prior | Δ | 弱点 |
|-------|--------|-------|---|------|
| compression_fidelity_dilemma | **0.88** | 0.85 | +0.03 | IB 建模假设 Y 是标量；实际 agent 多为多目标 |
| retrieval_centric_has_limits | **0.85** | 0.82 | +0.03 | 高维 curse 是已知问题；论文贡献在 IB 框架化 |
| greedy_aib_solution | **0.78** | 0.75 | +0.03 | 贪心近似无收敛保证；proxy 可能误导 |

---

## KB 映射

| Claim | Chunk | 关系 | 行动 |
|-------|-------|------|------|
| compression_fidelity_dilemma | **context-management.md** | **refine** — 与现有 context budget 讨论互补 | 加 IB 形式化引用 |
| retrieval_centric_has_limits | **context-management.md** | **confirm** — 确认了 RAG 的天花板 | 加为实证支持 |
| greedy_aib_solution | **context-management.md** | **new** — 具体算法方案 | 加 §Memory Construction 节 |
