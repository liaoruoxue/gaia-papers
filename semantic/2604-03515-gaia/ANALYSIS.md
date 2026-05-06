# Layer 2 — 2604.03515: Inside the Scaffold

**Layer 1 → Layer 2**: 292 claims + 95 strategies → **5 semantic claims + 1 boundary**

---

## 信念分析

| Claim | Belief | Prior | Δ | 弱点 |
|-------|--------|-------|---|------|
| scaffold_taxonomy_fills_gap | **0.92** | 0.90 | +0.02 | 13 agents 非全量；快速迭代的 scaffold 可能遗漏 |
| agents_are_spectra_not_categories | **0.88** | 0.85 | +0.03 | 12 维可能不穷尽；未排除 observer bias |
| loop_primitives_compose | **0.85** | 0.82 | +0.03 | 5 primitives 是归纳不是推导；2/13 例外未充分解释 |
| convergence_on_constrained_dims | **0.80** | 0.78 | +0.02 | 相关≠因果；external constraint 可能不是唯一驱动力 |
| methodology_commit_pinned_claims | **0.90** | 0.90 | 0 | 方法论主张；需更多 adoption 证据 |

---

## KB 映射

| Claim | Chunk | 关系 | 行动 |
|-------|-------|------|------|
| scaffold_taxonomy_fills_gap | **coding-agent** (新建) | **new** — 这是 coding agent chunk 的奠基文献 | 建 chunk，以本文为框架 |
| agents_are_spectra_not_categories | **coding-agent** | **new** | 作为组织原则 |
| loop_primitives_compose | **agent-loop.md** | **refine** — 与 Claude Code 的 loop 设计对位 | 加 loop 原语比较 |
| convergence_on_constrained_dims | **tool-system.md** | **refine** — tool sandbox/IDE 约束驱动收敛 | 引用 |
