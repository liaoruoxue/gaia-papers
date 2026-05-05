# Critical Analysis: Limozin et al. (2026) -- *SFT-then-RL Outperforms Mixed-Policy Methods for LLM Reasoning*

Knowledge package: `2604-23747-gaia`. arXiv: 2604.23747v1 (preprint, 26 Apr 2026). Reference implementation: https://github.com/alek6kun/sft_then_rl [@SFTthenRLCode].

## 1. Package Statistics

### Knowledge graph counts

| Item                              | Count |
|-----------------------------------|------:|
| Knowledge nodes (total)           | 179   |
| Settings                          |  18   |
| Questions                         |   1   |
| Claims (user-visible)             |  82   |
| Compiler helper claims (`__`)     |  78   |
| Strategies                        |  51   |
| Operators (`contradiction`)       |   2   |
| Modules                           |  10   |

### Claim classification

| Role                                      | Count |
|-------------------------------------------|------:|
| Independent (need prior, all assigned)    |  39   |
| Derived (BP propagates)                   |  41   |
| Structural (operator-derived)             |   2   |

### Strategy type distribution

| Type            | Count | Notes |
|-----------------|------:|-------|
| `support`       |   46  | Default soft deduction (most reasoning is empirical / interpretive). |
| `deduction`     |    1  | Bug mechanism -> suppressed grad norm follows from the gradient-accumulation contract by definition. |
| `induction`     |    1  | Population law "corrected SFT-then-RL beats every evaluated mixed-policy method" inducted over Qwen2.5-Math-7B + Llama-3.1-8B. |
| `abduction`     |    1  | Bug-attribution H vs methodological-advance Alt; discriminated by the cross-framework OpenRLHF-vs-verl match. |
| `compare`       |    1  | Sub-strategy of the abduction. |
| `contradiction` |    2  | (i) published mixed-policy advantage vs corrected outperformance; (ii) "optimizer bug is cosmetic" vs the +5.1-point quantitative attribution. |

### BP result summary

All 39 independent priors are assigned. Junction-tree exact inference converges in **2 iterations / 41 ms** (treewidth = 6).

| Region                                                          | Belief | Notes |
|-----------------------------------------------------------------|-------:|-------|
| `contra_optimizer_cosmetic_vs_dominant`                          | 1.000 | Contradiction operator near-certain |
| `contra_published_vs_corrected`                                  | 0.994 | Contradiction operator near-certain |
| `claim_attribution_table`                                         | 0.993 | Per-bug attribution from Table 2 rows |
| `claim_restored_confidence`                                       | 0.992 | SFT-then-RL restored as strongest paradigm |
| `claim_llama_plus_22p2`                                           | 0.988 | Llama-3.1-8B headline |
| `claim_synthesis_baselines_deflated`                              | 0.987 | Section 6 synthesis |
| `claim_grad_norm_suppressed`                                      | 0.987 | Deductive consequence of bug mechanism |
| `claim_implications`                                              | 0.979 | Cross-framework + other-areas + restored confidence |
| `claim_llama_headline`                                            | 0.978 | Abstract-level Llama headline |
| `claim_perceived_gains_attribution`                               | 0.977 | Perceived gains = deflated baselines (per-method) |
| `claim_obs_cross_framework_match`                                 | 0.976 | Discriminating observation (OpenRLHF 54.0 = verl 53.8) |
| `claim_loss_agg_smaller_effect`                                   | 0.976 | Loss-agg bug = +0.6 to +0.8 pts |
| `claim_two_bug_thesis`                                            | 0.967 | Joint two-bug thesis |
| `claim_optimizer_dominates_attribution`                           | 0.966 | Optimizer bug ~89% of gap |
| `claim_qwen_headline`                                             | 0.959 | Qwen2.5-Math-7B headline |
| `claim_qwen_plus_3p8`                                             | 0.947 | Corrected SFT-then-RL beats best mixed-policy by +3.8 |
| `claim_optimizer_bug_dominant`                                    | 0.921 | Motivation-section dominant-effect claim |
| `claim_compute_efficiency_headline`                               | 0.906 | Truncated 50-step variant beats mixed-policy at fewer FLOPs |
| `claim_compute_efficiency_synthesis`                              | 0.816 | Conjunction of accuracy + FLOPs + dense-reward mechanism |
| `claim_population_law`                                            | 0.747 | Induction conclusion (over Qwen + Llama) |
| `claim_intuitive_motivation_for_mixing` (foil-side leaf)          | 0.482 | Pulled down by contradiction-1 |
| `claim_alt_methodological_advance`                                | 0.300 | Abduction alternative; suppressed by cross-framework match |
| `claim_published_advantage_holds`                                 | 0.057 | Suppressed by contradiction-1 |
| `claim_optimizer_bug_cosmetic`                                    | 0.011 | Suppressed by contradiction-2 |

12 of the 41 derived claims have belief > 0.99; 33 of 41 have belief > 0.90; 4 user-visible claims have belief < 0.50 (the two foils, the abduction alternative, and the intuitive-motivation leaf -- all expected by the contradiction structure).

## 2. Summary

The argument structure is *headline = bug attribution + corrected-baseline outperformance + compute-efficiency*, anchored by two contradiction operators (the published mixed-policy advantage vs the corrected outperformance; the optimizer-cosmetic alt vs the dominant-effect attribution) and one central abduction (bug-attribution H vs methodological-advance Alt, discriminated by the cross-framework OpenRLHF-vs-verl match). The empirical anchors are the Qwen2.5-Math-7B 57.0 ID / 59.9 OOD result, the Llama-3.1-8B 43.7 result, the Table 2 per-bug waterfall (48.3 -> 49.1 -> 53.4 -> 54.0), and the truncated-50-step result (55.6 ID at 3.63x10^19 FLOPs). The population law "corrected SFT-then-RL beats every evaluated mixed-policy method on math benchmarks" is inducted over the two model families. The cross-framework match between patched OpenRLHF (54.0 +/- 0.2) and verl (53.8 +/- 0.1) provides the discriminating evidence: the abduction posterior comparison conclusion is at >0.999, the alternative is suppressed to 0.30, and the published-advantage foil collapses to 0.06.

## 3. Weak Points

| Claim | Belief | Issue |
|-------|-------:|-------|
| `claim_population_law` | 0.747 | Induction-conclusion law inducted over only two model families (Qwen2.5-Math-7B + Llama-3.1-8B). A third model family (e.g., Mistral, Gemma) would lift the law substantially. The +3.8 vs +22.2 magnitude difference between the two confirmations does provide a robustness check. |
| `claim_compute_efficiency_synthesis` | 0.816 | 4-component conjunction (truncated ID + truncated OOD + FLOPs table + dense-reward mechanism); multiplicative effect even with priors at 0.92-0.93. |
| `claim_compute_efficiency_headline` | 0.906 | Conjunction of accuracy + compute legs; bounded by the weakest constituent. |
| `claim_dense_reward_from_sft` | 0.842 | Mechanism-level argument synthesizing Fig. 3 dynamics across three signals (reward, length, entropy); slightly interpretive. |
| `claim_baseline_suspicion` | 0.848 | Motivation-section suspicion claim; pulled down slightly because it is a 4-conjunct support over the four method descriptions plus the framework provenance. |
| `claim_qwen_plus_3p8` | 0.947 | Strong but somewhat sensitive to whether SRFT (53.2) or another method (HPT 52.7) is the "best published mixed-policy." |

## 4. Evidence Gaps

### Missing experimental validations

| Question | Why it would help |
|----------|-------------------|
| Does the corrected-baseline result hold on a third model family (Mistral, Gemma, Qwen3)? | Would lift the population law from 0.75 toward saturation; the paper itself acknowledges only two model families. |
| Does mixed-policy training applied *atop* a correctly-trained SFT checkpoint yield additional gains? | Section 6 explicitly flags this as untested -- the headline outperformance does not preclude mixed-policy adding value on top of corrected SFT. |
| What are LUFFY's and ReLIFT's results when retrained from scratch with the patched OpenRLHF/Llama-Factory? | Would directly verify whether they maintain or lose their reported advantage when their *own* SFT init is corrected. |
| What is the SRFT result with LUFFY/ReLIFT-style SFT hyperparameters (5e-5 LR, batch 64) on a fully patched stack? | Section 4 / Table 3 shows hyperparam sensitivity for the SFT *baseline* but does not retrain SRFT itself with non-weak SFT init. |
| Does the bug attribution extend to non-math domains (code generation, general reasoning) with the same affected frameworks? | Implication 2 (bugs may affect other ML areas) is a plausibility claim, not a measurement. |
| Are the 7 qualitatively-discussed methods (UFT, CHORD, SuperRL, SASR, RED, TemplateRL, MIFO) similarly affected? | The paper flags them for SFT auditing but does not perform the audit; the population law is currently a 5-method, 2-model-family generalization. |

### Untested conditions

* Larger model scales (>8B parameters) where SFT quality may matter differently (acknowledged limitation).
* Domains other than math (code, general reasoning, scientific QA).
* Other framework combinations (e.g., verl + DeepSpeed for SFT; FSDP-only for RL).
* The 50-step truncation is tested only on Qwen2.5-Math-7B, not on Llama-3.1-8B.

### Competing explanations not fully resolved

* The abduction alternative `claim_alt_methodological_advance` is suppressed to 0.30 but not eliminated. The methodological-advance hypothesis remains viable as a *partial* explanation -- e.g., mixed-policy methods may genuinely add value but only *atop* corrected SFT, which the paper explicitly acknowledges is untested.
* The hyperparameter-sensitivity finding for SRFT (Table 3) is a *separate* baseline-deflation mechanism (weak SFT learning rate) that complements the framework-bug mechanism but is not unified with it. SRFT users could in principle defend their published numbers by arguing the LR choice is intentional / the paper unfair.

## 5. Contradictions

### Explicit contradictions modeled with `contradiction()`

| Operator | Claims | BP resolution |
|----------|--------|---------------|
| `contra_published_vs_corrected` | (a) Foil: published mixed-policy advantage is a real methodological advance (`claim_published_advantage_holds`, posterior 0.06); (b) Corrected-baseline result: SFT-then-RL beats every mixed-policy method on Qwen by +3.8 (`claim_qwen_plus_3p8`, posterior 0.95) | The contradiction collapses the foil to 0.06 while leaving the corrected-baseline result at 0.95. The literature's claim is empirically rejected. |
| `contra_optimizer_cosmetic_vs_dominant` | (a) Foil: the optimizer bug is small / cosmetic (`claim_optimizer_bug_cosmetic`, prior 0.30 -> posterior 0.011); (b) Attribution: the optimizer fix recovers ~5.1 of the ~5.7 total gap (`claim_optimizer_dominates_attribution`, posterior 0.97) | The contradiction collapses the cosmetic foil to ~0.01. |

Both contradictions exhibit the BP-canonical "one side high, one side low" resolution -- the model picks a side cleanly because each foil is supported only by its own prior leaf, while the affirmative side is supported by multiple measurement chains.

### Internal tensions not modeled as formal contradictions

* **Mixed-policy-atop-corrected-SFT.** Section 6 acknowledges that mixed-policy methods atop a correctly-trained SFT checkpoint *might* yield further gains. This is a real open question but is not a `contradiction` because both can be true (corrected SFT-then-RL > current mixed-policy reports, *and* mixed-policy on top of corrected SFT could be even better).
* **SRFT hyperparameter-sensitivity vs framework-bug attribution.** SRFT is uniquely affected by the weak-LR hyperparameter choice rather than the OpenRLHF/Llama-Factory framework bugs (it does not use those frameworks for SFT). This is a different deflation mechanism, and the paper handles it as a complementary attribution; the formalization captures this via a separate strategy connecting `claim_hyperparam_sensitivity` to `claim_perceived_gains_attribution`.

## 6. Confidence Assessment

| Tier | Belief range | Claims |
|------|--------------|--------|
| **Very high** (>= 0.95) | 0.95-1.00 | Both contradictions; per-bug attribution; cross-framework match observation; both bug mechanisms; restored-confidence implication; per-row Table 2 measurements; Llama-3.1-8B headline; SFT-then-RL synthesis; perceived-gains-attribution. |
| **High** (0.85-0.95) | 0.85-0.95 | Two-bug thesis; optimizer-dominates attribution; Qwen +3.8 headline; truncated-RL outperformance; per-method comparison; FLOPs table; dynamics decomposition; Llama failure-mode explanation. |
| **Moderate** (0.70-0.85) | 0.74-0.84 | Population law (induction conclusion); compute-efficiency synthesis; baseline-suspicion claim; mixed-policy-gains-reported leaf; dense-reward-from-SFT mechanism. |
| **Tentative / contested** (< 0.50) | 0.01-0.48 | The two foils (mixed-policy-as-real-advance, optimizer-bug-cosmetic); the abduction alternative; the intuitive-motivation-for-mixing leaf. |

## 7. Interpretation

The paper makes a strong, narrowly-scoped empirical case. Its central contribution is the *cross-framework convergence* observation: two independent SFT implementations (patched OpenRLHF and verl) arrive at statistically equivalent scores once the two specific bugs are fixed, and that convergence is what gives the bug-attribution hypothesis dispositive explanatory power over the methodological-advance alternative. The +3.8 (Qwen) and +22.2 (Llama) headline numbers are reproducible deltas anchored in 3-seed measurements; the per-bug waterfall (48.3 -> 49.1 -> 53.4 -> 54.0) cleanly separates the two bugs' contributions. The principal evidential limitation is the two-model-family scope of the induction: the population law sits at 0.75 because Qwen and Llama, while spanning math-emphasized vs general-purpose pre-training regimes, are still only two confirmations. The honest counter-thesis -- mixed-policy *on top of* a corrected SFT might still help -- remains untested by both this paper and the literature it audits.
