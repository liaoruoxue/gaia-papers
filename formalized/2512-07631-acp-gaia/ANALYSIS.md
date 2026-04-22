# Critical Analysis: Agent Capability Problem (ACP)

## Package Statistics

| Metric | Value |
|--------|-------|
| Total knowledge nodes | 77 (13 settings, 1 question, 63 claims) |
| Strategies | 24 |
| Independent premises (leaf) | 14 |
| Derived conclusions | 20 |

## Summary

The ACP paper introduces an information-theoretic framework for predicting agent solvability. The core result — Theorem 3.1 (two-sided cost bound) — is technically sound, with the main theoretical claims achieving belief > 0.93. Primary weak points: (1) diminishing returns assumption unproven for LLM/combinatorial settings, (2) RKHS regularity for GP surrogate is strong and unverified, (3) induction from two experiments provides only modest generalization evidence.

## BP Results

| Claim | Belief | Tier |
|-------|--------|------|
| acp_lower_bound_graph | 0.982 | Very high |
| lower_bound_ceffective | 0.972 | Very high |
| two_sided_bound | 0.937 | Very high |
| acp_vs_random_graph | 0.939 | Very high |
| unified_principle | 0.873 | High |
| acp_lower_bounds_llm | 0.785 | Moderate |
| law_acp_lower_bound | 0.756 | Moderate |

## Weak Points

| Claim | Belief | Issue |
|-------|--------|-------|
| law_acp_lower_bound | 0.756 | Induction from only 2 experimental settings |
| acp_lower_bounds_llm | 0.785 | Abduction discrimination weak (H=0.785 vs Alt=0.778) |
| diminishing_returns_rationale | 0.808 | Plausible but unproven for specific domains |
| rkhs_surrogate_error | 0.820 | RKHS assumption strong, rarely verified in practice |
| ceffective_error_propagation | 0.850 | Taylor bound sketched, not tight for large errors |

## Evidence Gaps

- No validation that C_eff guides actual pre-search solvability decisions
- LLM experiment uses only 1D slope identification; multi-dimensional unvalidated
- No ablation on GP surrogate estimation error vs. sample size
- Greedy vs ACP gap <= 9% for n<=15; larger instances untested

## Internal Tensions

1. Diminishing returns assumed but not verified in actual experiments
2. C_effective uses mu_1 (initial gain) as proxy for I_s — may not represent optimal policy
3. ACP prediction exactly equals actual at (n=8, p=0.25) — unusual for a stochastic lower bound

## Confidence Tiers

- Very high: two_sided_bound, lower/upper_bound_ceffective, acp_lower_bound_graph
- High: acp_ceffective_formula, unified_principle, high_prob_bound
- Moderate: acp_lower_bounds_llm, law_acp_lower_bound, ceffective_error_propagation
