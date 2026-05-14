# Layer 2 Semantic: Conductor (2512.04388)

Nielsen et al. 2026 — *Learning to Orchestrate Agents in Natural Language with the Conductor*. ICLR 2026.

**From L1 to L2**: 90 user-visible claims → 5 semantic claims + 17 judgment nodes. 7 strategies (1 deduction + 3 support + 3 deduction-validity).

## Belief Analysis

| Claim | Belief | Prior | Δ | Notes |
|-------|--------|-------|---|-------|
| conductor_rl_emergent_coordination | **0.999** | 0.88 | +0.119 | Two surprise support paths + 7-premise deduction. Very high confidence within Qwen 7B scope. |
| conductor_sota_cost_efficient | **0.999** | 0.90 | +0.099 | Strong empirical anchor (Tables 1, 7) + surprise support. Close-margin SE weakness noted but insufficient to pull down. |
| conductor_recursive_scaling | **0.996** | 0.83 | +0.166 | Largest Δ — the AIME25 pass-through (negative result) and BCB redistribution mechanism (Fig. 10) provide strong convergent evidence. |
| conductor_cross_pool_generalization | **0.898** | 0.85 | +0.048 | Modest Δ — evidence is solid but fewer independent chains (two pool results, same finetuning protocol). |
| conductor_broader_thesis_rl_sufficient | **0.976** | 0.78 | +0.196 | Largest absolute Δ — 4-premise deduction pushes posterior near-certain. The thesis that RL alone discovers emergent coordination is well-supported *within the Conductor's scope*. |

### Weak/Boundary Posterior

| Node | Belief | Direction |
|------|--------|-----------|
| bdry_recursion_2x_budget_cap | 0.971 | Minimal adjustment — stated explicitly, not contested |
| bdry_qwen_base_only | 0.966 | No reverse penalty — emergent coordination is strong |
| bdry_max_5_steps | 0.961 | Minor reverse penalty from being in two deductions |
| weak_reasoning_only_domains | 0.946 | Slight uplift — boundary is correct but not debilitating |
| weak_only_7b_conductor_tested | 0.932 | Shared with bdry_verifiable_reward (both at same level from deduction) |
| premise_skills_well_documented | 0.932 | Up from 0.90 — confirmed by BP |
| weak_no_standard_error_tables_1_2_10 | 0.915 | Modest uplift |
| weak_few_shot_are_real_completions | 0.864 | Lowest weak — genuine alt-not-excluded gap |

## Surprising Points

| # | Phenomenon | Belief | KB |
|---|-----------|--------|-----|
| 1 | OOD few-shot outperforms in-distribution (anti-reward-hacking) | 0.865 | new → rl-training.md |
| 2 | Agent-selection vs prompt-engineering have different scaling laws | 0.912 | new → multi-agent.md |
| 3 | 7B coordinator lifts frontier workers past individual ceilings | 0.930 | refine → multi-agent.md |

## Elegant Points

| # | Design | Portability |
|---|--------|------------|
| 1 | Natural-language workflow as unrestricted instruction surface | high |
| 2 | Ordinal model naming eliminates prior-association bias | high |
| 3 | Recursion pass-through avoids wasting compute on optimal strategies | medium |

## KB Mapping

| Semantic Claim | KB Chunk | Relation | Action |
|---------------|----------|----------|--------|
| conductor_rl_emergent_coordination | chunks/multi-agent.md | **new** — RL-trained small coordinator as meta-agent design point | Add section on learned orchestration |
| conductor_sota_cost_efficient | chunks/multi-agent.md | **refine** — multi-agent can beat single-model scaling | Update cost-efficiency evidence |
| conductor_cross_pool_generalization | chunks/multi-agent.md | **new** — randomized-pool generalization | Add to generalization section |
| conductor_recursive_scaling | chunks/agent-loop.md | **new** — recursive self-referential topology as test-time scaling axis | Add to loop/scaling section |
| conductor_broader_thesis_rl_sufficient | chunks/rl-training.md | **refine** — RL alone sufficient for emergent coordination (with verifiable reward boundary) | Strengthen RL section |
| surprise_ood_few_shot_better | chunks/rl-training.md | **new** — OOD conditioning as anti-reward-hacking mechanism | Add to sharpening section |
| Surprise 3B vs 7B scaling gap | chunks/multi-agent.md | **new** — agent-selection scales differently from prompt-engineering | Add to scaling discussion |

## Next: /paper-deep-read 2512.04388

L2 准备就绪。深读时加载本 ANALYSIS.md 的信念表 + KB 映射作为起点，重点验证：
1. weak 节点是否在深读中有新证据补充
2. KB 映射的 7 条更新建议是否准确
3. 是否触发新的 cross-paper contradiction
