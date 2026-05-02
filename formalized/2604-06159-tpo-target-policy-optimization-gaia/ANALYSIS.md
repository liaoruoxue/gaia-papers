# Critical Analysis: TPO: Target Policy Optimization

## Package statistics

| Item | Count |
|------|------:|
| Modules | 1 (`motivation.py`) |
| Settings | 2 |
| Questions | 0 |
| Claims | 6 (2 independent, 4 derived) |
| Strategies | 4 (all `support`) |
| Operators | 0 |
| Independent leaf priors set | 2 / 2 |
| BP iterations to convergence | 2 (Junction Tree, exact) |

Strategy-type distribution: 100% `support`. This is the appropriate
default for a title-only formalisation -- there are no theory-vs-experiment
comparisons, no induction over multiple datasets, and no exhaustive case
splits to model because the source body is not available.

## BP belief summary

| Claim | Role | Belief |
|-------|------|-------:|
| `target_policy_is_the_optimisation_object` | leaf | 0.900 |
| `tpo_realises_target_policy_optimization` | leaf | 0.880 |
| `keyword_rl_training` | derived | 0.875 |
| `keyword_cross_entropy` | derived | 0.867 |
| `keyword_gradient_conflict` | derived | 0.865 |
| `keyword_grpo_alternative` | derived | 0.863 |

Each derived keyword sits below the conjunctive product of its two leaf
parents (~0.792) lifted by a positive-strength `support` prior in the
0.90-0.95 range. `keyword_rl_training` lifts highest because its support
prior (0.95) is the strongest -- the situating of the work in the LLM
RL-fine-tuning regime is the most direct entailment of the title and
keyword list together. `keyword_grpo_alternative` lifts the least
because its support strategy is the broadest claim (a method-positioning
claim relative to a named baseline family), so a slightly more
conservative support prior (0.92) is appropriate.

## Summary

The package is a minimal but valid formalisation built from the only
material available in the artifact: a title H1 ("TPO: Target Policy
Optimization"), an arXiv URL, and a four-keyword list. The H1 is split
into two independent leaf claims under the standard 'METHOD: thesis'
convention: (1) `target_policy_is_the_optimisation_object` -- the
post-colon thesis that policy-gradient RL fine-tuning of LLMs benefits
from optimising against an explicit *target policy* (a reference token
distribution constructed from the rollouts) rather than a sparse
group-relative return; and (2) `tpo_realises_target_policy_optimization`
-- the pre-colon method ("TPO:") read as the proposed concrete
realisation of that training rule. The four keywords (`rl-training`,
`grpo-alternative`, `cross-entropy`, `gradient-conflict`) are extracted
as derived topic-coverage claims and connected to the leaves through
four `support` strategies that explicitly tie each keyword back to the
central thesis: rl-training is the regime the method operates in,
grpo-alternative is the position in the algorithm space, cross-entropy
is the objective form that target-policy matching takes, and
gradient-conflict is the failure mode of the GRPO baseline that the
target-policy rule is designed to avoid. The reasoning graph is shallow
(max depth 2) and contains no contradictions, abductions, or inductions
because the source body is not accessible.

## Weak points

| Claim | Belief | Issue |
|-------|------:|-------|
| `keyword_grpo_alternative` | 0.863 | "Drop-in alternative to GRPO" is a strong positioning claim. Title-only evidence cannot discriminate between a clean replacement of the GRPO advantage term and a hybrid scheme that retains a GRPO advantage term and adds a target-policy cross-entropy term as an auxiliary signal. The "alternative" framing is the more aggressive of the two readings. |
| `keyword_gradient_conflict` | 0.865 | "Gradient conflict" admits multiple precise definitions in the LLM RL literature -- per-sample sign-disagreement on shared parameters, per-token interference within a single rollout, or per-task interference across heterogeneous batches. Title and keyword alone do not pin down which definition the paper uses or how it is measured. |
| `tpo_realises_target_policy_optimization` | 0.880 | The exact construction of the target distribution (best-of-group rollout, expert demonstration, frozen reference model, EMA of the trainee, ...) and the exact form of the update (pure cross-entropy vs. cross-entropy + auxiliary GRPO term, on-policy vs. off-policy, all-positions vs. supervised-positions only) cannot be recovered from the title. |

No claim falls below 0.5; no abduction alternative needs review (there
are no abductions). The structural risk is uniformly low because the
graph is small.

## Evidence gaps

The dominant evidence gap is the source itself: this package formalises
only the title and keyword list. The following claims could only be
verified or refined with access to the full PDF body:

| Gap | What is missing | What would close it |
|-----|-----------------|---------------------|
| Target-policy specification | How exactly is the target distribution constructed from a batch of rollouts -- best-of-group, top-k mean, expert demonstration, frozen reference, EMA of the trainee? Is it constructed once per batch or per rollout? Per token or per sequence? | Method / algorithm section of the PDF. |
| Update-rule specification | Is the trainee policy updated by pure cross-entropy against the target, or by cross-entropy plus an auxiliary GRPO advantage term? Is the loss restricted to supervised positions (e.g. answer tokens only) or applied uniformly? | Method / algorithm section of the PDF. |
| Gradient-conflict diagnosis | What metric does the paper use to diagnose gradient conflict in GRPO (cosine of per-sample gradients on shared parameters, sign-disagreement counts, downstream evaluation degradation, ...)? Is the diagnosis empirically established or theoretically argued? | Analysis / diagnostics section of the PDF. |
| Empirical evaluation | What benchmarks (e.g. MATH, GSM8K, AIME, code-reasoning suites) does TPO evaluate on, and at what scale (model size, group size, number of rollouts)? What is the headline gain over GRPO and over the strongest baseline alternative? | Experiments section of the PDF. |

Each of these would justify upgrading the formalisation from this
title-stub package to a full multi-module formalisation with explicit
abductions (theory vs. experimental gain), inductions (across benchmarks
or model scales), and contradictions (TPO vs. GRPO vs. other named
alternatives).
