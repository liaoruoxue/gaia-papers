# Critical Analysis: Li, Yi, Li, Fan, Jiang, Chen, Li, Song, Zhang (2026) -- *Reasoning and Tool-use Compete in Agentic RL: From Quantifying Interference to Disentangled Tuning*

Knowledge package: `2602-00994-gaia`. arXiv: 2602.00994 (preprint, Feb 3 2026).

## 1. Package Statistics

### Knowledge graph counts

| Item                                              | Count |
|---------------------------------------------------|------:|
| Knowledge nodes (total)                           | 136   |
| Settings                                          | 39    |
| Questions                                         | 1     |
| Claims                                            | 96    |
| Strategies                                        | 32    |
| Operators                                         | 1     |
| Modules                                           | 6     |

### Claim classification

| Role                                              | Count |
|---------------------------------------------------|------:|
| Independent (need prior)                          | 25    |
| Derived (BP propagates)                           | 26    |
| Structural (operator-derived)                     | 1     |
| Compiler helpers (`__implication_*`, `__conjunction_*`) | 44 |

### Strategy type distribution

| Type            | Count |
|-----------------|------:|
| `support`       | 23    |
| `deduction`     | 1     |
| `induction`     | 3 (chained: `ind_dart_12`, `ind_dart_123`, `ind_dart_1234`) |
| Implicit support strategies inside `induction()` | 4 (`sup_dart_3b_inst`, `sup_dart_3b_base`, `sup_dart_7b_inst`, `sup_dart_7b_base`) |
| Operators       | 1 (`contra_joint_vs_interference`) |

`support` accounts for ~72% of strategies -- slightly above the recommended ceiling but appropriate for this paper's structure: the central argument is "build a diagnostic that quantifies a phenomenon, then build a method that removes its mechanistic cause," which is naturally chained-support reasoning rather than abductive / case-analytic. The single `induction` chain (over four (model size, init) backbones) carries the empirical generalization. The single `contradiction` operator captures the paper's core dialectical move (LEAS refutes the prevailing joint-training assumption).

### Figure / table reference coverage

All three main-text tables, both ablation figures, and the appendix figures with quantitative content are transcribed as claims with `metadata={"source_table": ...}` or `metadata={"source_figure": ...}`:

| Source           | Claim                                          |
|------------------|------------------------------------------------|
| Table 1          | `table1_qwen3b`                                |
| Table 2          | `table2_qwen7b`                                |
| Table 3          | `table3_hybrid`                                |
| Fig. 2           | `obs_lambda23_distribution`, `obs_arl_succeeds_in_interference_region` |
| Fig. 3A / 7A     | `obs_gradient_angles`                          |
| Fig. 5           | `obs_dart_better_reasoning_3b`, `obs_dart_better_reasoning_7b` |
| Fig. 6           | `obs_lora_equals_searchr1`, `obs_2agent_strongest`, `obs_dart_approaches_2agent` |
| Fig. 9 (App. G)  | `obs_rank_insensitive`                         |
| Fig. 10 (App. H) | `obs_dart_retrieval_acc`                       |
| Appx F (Table 5) | `claim_2agent_memory_8x`, `claim_2agent_kv_recompute` |

### BP result summary

All 25 independent priors are filled. JT inference converges in **2 iterations, 21 ms**.

| Region                                   | Mean belief | Notes                                                                                |
|------------------------------------------|------------:|--------------------------------------------------------------------------------------|
| Direct empirical observations (priors)   | 0.92        | Anchored by Tables 1-3, Figs. 2-10; range [0.85, 0.95]                              |
| Per-backbone (size, init) derived obs    | 0.996       | Pulled up by the highly-anchored Tables 1+2 (downstream of reading off cells)        |
| Empirical headline gain (`obs_dart_average_gain`) | 0.977 | Average of four near-perfect per-backbone gaps                                       |
| Induction headline (`claim_dart_beats_grpo_universally`) | 0.919 | 4-cell induction with 0.85-0.9 sub-priors                                            |
| Contribution-level claims (LEAS, DART, empirical) | 0.78  | Top-of-chain syntheses, depth-2 to depth-3 chains                                    |
| Mechanistic claim (`claim_gradient_conflict_explains_interference`) | 0.78 | Two empirical anchors + 0.85 prior on warrant                                        |
| Contradiction (joint-assumption vs LEAS) | 0.999       | Picks the LEAS side: `claim_joint_training_helps_assumed` driven down to **0.156**   |
| Interference finding (`claim_interference_dominates`) | 0.72   | Pulled down slightly by being on the contradiction's anchor side                      |

## 2. Summary

The paper makes one diagnostic contribution (LEAS) and one methodological contribution (DART), each empirically validated.

1. **Section 3-4 (LEAS).** A logit-additive correctness model assigns each agent a 6-dimensional binary capability vector $x = [x_1, x_2, x_3, x_{12}, x_{13}, x_{23}]$ encoding base / tool / reasoning capabilities and their pairwise *joint-optimization* interactions. By constructing six model variants (base + 3 gradient-masked + 2 hybrid-inference) whose capability vectors are linearly independent, the per-question $\lambda^q \in \mathbb{R}^6$ is identified, and the sign of $\lambda_{23}^q$ tells whether reasoning and tool-use synergize or interfere under joint training. Empirically on NQ + HotpotQA, $\lambda_{23}^q < 0$ on roughly two-thirds of questions in 3 of 4 (model, dataset) cells, and the questions where ARL most often succeeds are concentrated in the interference region. A separate gradient-angle measurement (Fig. 3A / Fig. 7A) shows that reasoning vs tool-use gradients are near-orthogonal, identifying *gradient compromise in shared parameters* as the mechanistic cause.

2. **Section 5 (DART).** Freeze the backbone, attach two disjoint LoRA adapters ($\theta_r$ and $\theta_a$), and route each token to exactly one adapter via a rule-based router on the structural special tokens (`<think>`, `<search>`). By construction $x_{23} \equiv 0$ at every token, so the LEAS-quantified interference cannot occur. Backbone freezing is shown to be necessary (otherwise gradients re-mix) and not performance-costly (citing [@Mukherjee2025; @Schulman2025]).

3. **Section 6 (empirical).** Four-way (3B/7B) x (Base/Instruct) backbone evaluation across seven QA benchmarks. DART beats Search-R1-GRPO on the 7-benchmark average in every cell: +6.3 / +10.2 / +2.4 / +6.6 EM. Average gain ~6.35 EM (the headline). Two mechanism analyses corroborate: under fixed retrieval (Fig. 5) DART's reasoning is better; in single-ability evaluation (Table 3) DART's adapters outperform inference-time hybrid composition. Ablation 1 (Fig. 6) shows vanilla LoRA = Search-R1 -- so the bottleneck is not capacity but interference; DART approaches the 2-Agent upper bound at single-model cost. Ablation 2 (Fig. 9) shows rank-insensitivity. Appendix F provides the theoretical 8x training-memory and $O(L^2) \to O(1)$ inference-latency advantages of DART over 2-Agent. Appendix H shows DART also improves tool-use (retrieval accuracy).

The structural argument is tight: LEAS *measures* interference, gradient analysis *explains* interference, DART *removes* the mechanism, four-backbone induction *confirms* the empirical payoff, and the contradiction operator captures the dialectical refutation of the prevailing joint-training assumption (driven from prior 0.55 to posterior 0.156). The strongest evidence anchors are the per-backbone EM gaps (belief ~0.996 each) and the per-figure observations (0.92-0.95). The mechanistic and synthesis claims sit at 0.72-0.83 -- moderate to high, with the inevitable belief decay along 2-3 hop chains.

## 3. Weak Points

| Claim / strategy                                | Belief / prior | Issue                                                                                                                                                                                                                                                                                            |
|-------------------------------------------------|---------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `claim_interference_dominates`                  | 0.72           | The headline LEAS finding sits below 0.8 because it is the conclusion of a support strategy with prior 0.9 from two leaf observations of priors 0.92 / 0.85, and is on the high-belief side of the contradiction operator (which still pulls slightly even when the operator picks correctly). The Qwen2.5-3B HotpotQA cell is 57.7% synergy / 42.3% interference -- so the "interference dominates" claim is empirically true on 3/4 cells but not the 4th. |
| `claim_contribution_leas`                       | 0.76           | A 5-premise support: design-matrix invertibility (0.97), hybrid no-interaction (0.95), contrast (0.98), interference (0.72), gradient explanation (0.78) -- the multiplicative effect of the moderate-belief premises pulls the conclusion to the 0.75 range despite a 0.88 warrant prior.       |
| `claim_contribution_empirical`                  | 0.76           | Five-premise support; the chain is a hop deeper than the empirical observations themselves, hence the modest belief.                                                                                                                                                                              |
| `claim_gradient_conflict_explains_interference` | 0.78           | The mechanistic claim relies on a single observation type (gradient angles). It is consistent with @claim_interference_dominates but does not isolate gradient conflict from other potential mechanisms (e.g. capacity allocation effects). The 0.85 warrant prior caps the support strength.    |
| `claim_dart_efficient_disentanglement`          | 0.77           | Conclusion of a 4-premise support; consistent with all evidence, but the chain depth and premise count compound modest-belief dependencies.                                                                                                                                                       |
| `claim_bottleneck_is_interference_not_capacity` | 0.77           | Inferred from "LoRA approx Search-R1" (0.88) plus the LEAS interference claim (0.72). The argument is a logical-elimination one (capacity hypothesis would predict LoRA underperforming) and the warrant is necessarily indirect.                                                                  |
| `obs_arl_succeeds_in_interference_region`       | 0.80           | The Fig. 2 overlay curve is qualitative -- per-bin accuracy values are not tabulated. Set at prior 0.85; BP pulls it slightly down via downstream consistency. A future paper releasing the per-bin table would lift this above 0.95.                                                              |
| `claim_seesaw_phenomenon`                       | 0.83           | Set up as a derived claim from `claim_interference_dominates`; inherits the interference belief and is bounded above by the warrant prior (0.92).                                                                                                                                               |
| `claim_freeze_no_performance_loss`              | 0.85 (prior)   | Independent claim resting on two cited results [@Mukherjee2025; @Schulman2025]. Prior is not set higher because neither cited paper is specifically about the ARL+QA regime; transferability is plausible but not proven.                                                                          |
| `obs_lora_equals_searchr1`                      | 0.88 (prior)   | Fig. 6 reports only radar averages, not per-benchmark deltas. The "nearly identical" claim is supported by the visual overlap but a per-cell table would be stronger evidence.                                                                                                                  |

The maximum reasoning-chain depth from leaf observation to top-level contribution is **3 hops** (e.g. `table1_qwen3b` -> `obs_dart_beats_grpo_3b_inst` -> `claim_dart_beats_grpo_universally` -> `claim_contribution_empirical`), keeping multiplicative belief decay manageable.

## 4. Evidence Gaps

### 4.1 Missing experimental validations

| Gap                                                                                                       | Why it would help                                                                                                                                                                                |
|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Per-bin accuracy table for the Fig. 2 overlay curve                                                       | Currently the "ARL succeeds in the interference region" claim rests on a visual trend; a per-bin table would replace the qualitative claim with quantitative evidence.                              |
| Statistical significance / variance estimates on EM scores                                                | All Tables 1-3 are single-run point estimates. Several DART vs Search-R1-GRPO gaps are small (e.g. +2.4 EM on 7B-Instruct, where two cells favour Search-R1); seed-to-seed variance would resolve. |
| LEAS evaluated on the same seven benchmarks used in Sec. 6                                                | LEAS is only run on NQ + HotpotQA; the empirical experiments use seven benchmarks. Running LEAS on the other five would test whether the interference pattern explains the per-benchmark DART gains. |
| Evidence that DART's gain comes specifically from gradient-orthogonality elimination                      | The mechanistic chain is "LEAS shows interference; gradients are orthogonal; DART removes the mechanism." A direct intervention (e.g. enforce gradient orthogonality without architectural change) would cleanly isolate the proposed mechanism. |
| Per-benchmark deltas in Fig. 6 (LoRA vs Search-R1)                                                        | The "LoRA approx Search-R1" claim is supported only by radar averages. A per-benchmark table would either strengthen or qualify it.                                                              |
| Causal evidence that backbone freezing does *not* cause performance loss in this specific regime          | The current support is two cited generic results [@Mukherjee2025; @Schulman2025] plus the indirect "DART matches 2-Agent" observation; a within-paper full-fine-tuning DART variant would be a direct test. |

### 4.2 Untested conditions

- **Other model families.** Only the Qwen2.5 family (3B, 7B) is tested. Generalisation to Llama, Mistral, DeepSeek, Yi, etc., is unverified.
- **Larger model scales.** DART's effect at 30B+ or MoE backbones is unknown; the paper's own observation that "7B does not consistently beat 3B on retrieval accuracy" (Appendix H) hints at non-trivial scaling behaviour.
- **Task domains beyond tool-augmented QA.** The DART idea is general (any decomposable role partition), but evaluation is limited to QA. Effects on code generation, math reasoning, multi-tool agents are open.
- **More than two roles.** Both LEAS and DART handle binary {reasoning, tool-use}; agents with $\ge 3$ roles (planner, executor, critic, ...) require generalising the construction.
- **Larger LoRA ranks.** Ablation 2 (Fig. 9) goes up to rank 32; behaviour at rank 128+ is open.
- **Other RL algorithms.** Only GRPO is tested; whether the gradient-conflict pattern holds under PPO, DPO, REINFORCE, etc., is not directly verified -- though the gradient-angle protocol is in principle algorithm-agnostic.

### 4.3 Competing explanations not fully resolved

| Competing story                                                                                            | Status                                                                                                                                                                                          |
|------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DART helps because it doubles the per-token specialised parameter capacity                                 | Directly addressed: vanilla LoRA at the same total rank approx Search-R1 (Fig. 6); rank insensitivity (Fig. 9). Capacity hypothesis refuted within the tested rank range.                       |
| DART helps because rule-based routing acts as a stronger inductive prior than gradient flow                | Not directly tested. Hard routing is a mild form of "input-conditional architecture" and could improve generalization independent of gradient isolation.                                         |
| The seesaw phenomenon is partly an artefact of the EM metric / ground-truth label noise                    | Not addressed. EM is the only training signal; LEAS uses EM correctness too. A cleaner metric (e.g. F1, semantic similarity) might produce different $\lambda_{23}$ distributions.                |
| The interaction $\lambda_{23} < 0$ may reflect data-distribution mismatch between $\mathcal{T}_\text{reas}$ and $\mathcal{T}_\text{tool}$ token statistics rather than capability conflict | Not modeled. Token-distribution heterogeneity is observable from the role-router and could be a confound for the gradient-orthogonality result.                                                  |

## 5. Contradictions

### 5.1 Explicit contradictions modeled with `contradiction()`

| Contradiction | Operator belief | Outcome | Comment |
|---------------|----------------:|---------|---------|
| `claim_joint_training_helps_assumed` vs `claim_interference_dominates` | 0.999 | The implicit assumption is suppressed (belief 0.156); the LEAS finding is preserved (0.720). | Functions exactly as intended: the empirical LEAS measurement refutes the prevailing-but-untested assumption that motivated decades of joint-training ARL. The contradiction is the dialectical core of the paper. |

### 5.2 Internal tensions in the source not modeled as formal contradictions

These are real tensions in the paper that are NOT logically contradictory (both sides can be true) but are worth flagging:

| Tension                                                                                                                                                              | Why not a `contradiction()`                                                                                                              |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| "Interference dominates 3 of 4 cells" vs "Qwen2.5-3B HotpotQA is 57.7% synergy"                                                                                       | Population-level claim is consistent with one cell being an exception; the four cells are independent measurements.                       |
| "DART beats Search-R1-GRPO on every backbone" vs "On Qwen2.5-7B-Instruct, DART loses on Bamboogle (0.386 vs 0.400)"                                                  | Average-vs-per-cell. The average gain is positive on every backbone; one of 28 cells (4 backbones x 7 benchmarks) being adverse is consistent with the law. |
| "Backbone freezing does not sacrifice performance" vs "DART reaches only ~1 EM short of 2-Agent (which trains the full backbone)"                                    | The ~1 EM gap could reflect freezing cost OR could be noise; not directly distinguished. Both can be true.                                |
| "DART improves both reasoning (Fig. 5) and tool-use (Fig. 10)" vs "Joint training shows a *seesaw* (improving one degrades the other)"                                | DART's wins on both don't contradict the seesaw -- the seesaw is about *joint shared-parameter* training, which DART eliminates by design. |
| Appendix H: "DART-7B does not consistently outperform DART-3B on retrieval"                                                                                          | Open observation flagged by the authors as future work; not contradictory with the main thesis but suggests non-monotonic scaling of disentanglement benefits with model size. |

## 6. Confidence Assessment

The exported headline claims fall into the following confidence tiers based on posterior belief.

### Very high confidence (belief >= 0.95)

- *(none of the synthesis-level claims reach this tier; the highest-belief named claims are direct table/figure transcriptions and the per-backbone observations they support)*

### High confidence (0.85 <= belief < 0.95)

| Claim                                              | Belief | Why                                                                                          |
|----------------------------------------------------|-------:|----------------------------------------------------------------------------------------------|
| `claim_dart_beats_grpo_universally`                | 0.92   | 4-cell induction over (3B/7B) x (Base/Instruct); per-cell observations all near 0.996.       |
| `claim_dart_improves_tool_use`                     | 0.92   | Anchored by Fig. 10 (4 cells, all favouring DART, gains 2.9-18.5 RetAcc).                    |
| `claim_disentanglement_not_replicable_at_inference` | 0.91 | 8-cell read-off from Table 3, all favouring DART_{Reas/Tool} over hybrids.                  |
| `claim_dart_more_efficient_than_2agent`            | 0.91   | 3 independent efficiency advantages (memory, latency, deployment) all read from Appendix F.   |
| `claim_joint_assumption_unexamined`                | 0.90   | Direct read of the related-work landscape; 0.95 warrant on the related-work argument.        |
| `claim_capabilities_are_heterogeneous`             | 0.89   | Direct optimization-geometric evidence (gradient angles).                                    |
| `claim_joint_degrades_reasoning`                   | 0.89   | Two-cell support from Fig. 5 fixed-retrieval bars; warrant 0.9.                              |

### Moderate-to-high confidence (0.75 <= belief < 0.85)

| Claim                                              | Belief | Why                                                                                                                  |
|----------------------------------------------------|-------:|----------------------------------------------------------------------------------------------------------------------|
| `claim_seesaw_phenomenon`                          | 0.83   | Direct support from `claim_interference_dominates`; warrant 0.92.                                                    |
| `claim_dart_solves_gradient_conflict`              | 0.82   | Composite synthesis from DART structural facts + LEAS mechanistic finding.                                           |
| `claim_contribution_dart`                          | 0.81   | Top-level synthesis claim. Reasonable given DART's structural correctness + empirical support.                       |
| `claim_gain_not_from_extra_capacity`               | 0.80   | Rank-insensitivity finding plus disentanglement-efficiency claim.                                                    |
| `claim_gradient_conflict_explains_interference`    | 0.78   | Mechanistic claim; supported by orthogonality observation + LEAS interference; 0.85 warrant prior.                   |
| `claim_dart_efficient_disentanglement`             | 0.77   | 4-premise synthesis; chain depth 3.                                                                                  |
| `claim_bottleneck_is_interference_not_capacity`    | 0.77   | Indirect (elimination-style) argument from LoRA approx Search-R1 plus interference dominance.                        |
| `claim_contribution_empirical`                     | 0.76   | 5-premise top-level synthesis.                                                                                       |
| `claim_contribution_leas`                          | 0.76   | 5-premise top-level synthesis.                                                                                       |

### Moderate confidence (0.65 <= belief < 0.75)

| Claim                                  | Belief | Why                                                                                                                  |
|----------------------------------------|-------:|----------------------------------------------------------------------------------------------------------------------|
| `claim_interference_dominates`         | 0.72   | The headline LEAS finding. Supported by the histogram (0.89) + overlay (0.80) with 0.9 warrant; bounded above by the inevitable noise in 3 of 4 cells being interference-dominant (the 4th cell is synergy-dominant). |

### Refuted (< 0.2)

| Claim                                  | Belief | Why                                                                                                                  |
|----------------------------------------|-------:|----------------------------------------------------------------------------------------------------------------------|
| `claim_joint_training_helps_assumed`   | 0.156  | Refuted by the LEAS interference finding via the contradiction operator. The contradiction picks the empirically supported side cleanly. |

---

**Bottom line.** The paper's empirical headline ("DART beats joint-training baselines by ~6.35 EM averaged over 7 benchmarks") is robustly supported (induction belief 0.92, per-backbone gaps 0.996). The mechanistic story ("joint training induces gradient-conflict-driven interference; DART eliminates it") is moderately supported (interference 0.72, gradient explanation 0.78, DART-solves-conflict 0.82) -- the chain is correct, but each hop costs a little belief, and the LEAS measurement on only 2 of 7 benchmarks leaves room for cell-specific variation. The most actionable evidence gap is running LEAS on the remaining five benchmarks to verify the interference pattern explains the empirical gains uniformly. The most novel structural element is the use of LEAS's own interaction indicator $x_{23}$ as both a diagnostic (Section 4) and a design constraint (Section 5: DART enforces $x_{23} \equiv 0$ structurally).
