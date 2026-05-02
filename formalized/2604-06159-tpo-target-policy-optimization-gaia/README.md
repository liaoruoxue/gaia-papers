# 2604-06159-tpo-target-policy-optimization-gaia

Add your description here

<!-- badges:start -->
<!-- badges:end -->

## Overview

> [!TIP]
> **Reasoning graph information gain: `1.1 bits`**
>
> Total mutual information between leaf premises and exported conclusions — measures how much the reasoning structure reduces uncertainty about the results.

```mermaid
---
config:
  flowchart:
    rankSpacing: 80
    nodeSpacing: 30
---
graph TB
    target_policy_is_the_optimisation_object["★ Central thesis: target-policy optimisation as the right RL training rule\n(0.90 → 0.90)"]:::exported
    tpo_realises_target_policy_optimization["★ TPO realises target policy optimization\n(0.88 → 0.88)"]:::exported
    keyword_rl_training["★ Keyword: rl-training\n(0.50 → 0.88)"]:::exported
    keyword_grpo_alternative["★ Keyword: grpo-alternative\n(0.50 → 0.86)"]:::exported
    keyword_cross_entropy["★ Keyword: cross-entropy\n(0.50 → 0.87)"]:::exported
    keyword_gradient_conflict["★ Keyword: gradient-conflict\n(0.50 → 0.86)"]:::exported
    strat_0(["infer\n0.29 bits"]):::weak
    keyword_grpo_alternative --> strat_0
    target_policy_is_the_optimisation_object --> strat_0
    strat_0 --> keyword_gradient_conflict
    strat_1(["infer\n0.26 bits"]):::weak
    target_policy_is_the_optimisation_object --> strat_1
    tpo_realises_target_policy_optimization --> strat_1
    strat_1 --> keyword_cross_entropy
    strat_2(["infer\n0.26 bits"]):::weak
    target_policy_is_the_optimisation_object --> strat_2
    tpo_realises_target_policy_optimization --> strat_2
    strat_2 --> keyword_grpo_alternative
    strat_3(["infer\n0.26 bits"]):::weak
    target_policy_is_the_optimisation_object --> strat_3
    tpo_realises_target_policy_optimization --> strat_3
    strat_3 --> keyword_rl_training

    classDef premise fill:#ddeeff,stroke:#4488bb,color:#333
    classDef exported fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#333
    classDef weak fill:#fff9c4,stroke:#f9a825,stroke-dasharray: 5 5,color:#333
    classDef contra fill:#ffebee,stroke:#c62828,color:#333
```

## Conclusions

| Label | Content | Prior | Belief |
|-------|---------|-------|--------|
| keyword_cross_entropy | The supervisory signal in TPO has the form of a **cross-entropy** term agains... | 0.50 | 0.87 |
| keyword_gradient_conflict | The failure mode of the GRPO baseline that TPO is designed to avoid is **grad... | 0.50 | 0.86 |
| keyword_grpo_alternative | TPO positions itself as a **GRPO alternative** -- a drop-in replacement for G... | 0.50 | 0.86 |
| keyword_rl_training | The work is situated within **RL training** of LLMs -- TPO is a training-time... | 0.50 | 0.88 |
| target_policy_is_the_optimisation_object | Policy-gradient RL fine-tuning of LLMs benefits from optimising the trainee p... | 0.90 | 0.90 |
| tpo_realises_target_policy_optimization | **TPO** -- the method named in the title -- is proposed as the concrete reali... | 0.88 | 0.88 |

<!-- content:start -->
<!-- content:end -->
