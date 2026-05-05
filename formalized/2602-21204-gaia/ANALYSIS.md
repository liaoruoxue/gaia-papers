# Critical Analysis: Liu, Elflein, Litany, Gojcic, Li (2026) -- *Test-Time Training with KV Binding Is Secretly Linear Attention*

Knowledge package: `2602-21204-gaia`. arXiv: 2602.21204v2 (preprint, Feb 27 2026).

## 1. Package Statistics

### Knowledge graph counts

| Item                                              | Count |
|---------------------------------------------------|------:|
| Knowledge nodes (total)                           | 165   |
| Settings                                          | 38    |
| Questions                                         | 2     |
| Claims                                            | 125   |
| Strategies                                        | 49    |
| Operators                                         | 4     |
| Modules                                           | 7     |

### Claim classification

| Role                                              | Count |
|---------------------------------------------------|------:|
| Independent (need prior, all assigned)            | 22    |
| Derived (BP propagates)                           | 42    |
| Structural (operator-derived)                     | 4     |
| Background-only                                   | 1     |
| Compiler helpers                                  | 56    |

### Strategy type distribution

| Type            | Count | Notes |
|-----------------|------:|-------|
| `support`       | 32    | Default for evidence-to-claim and synthesis links |
| `deduction`     | 11    | Theorems 5.1-5.3, ViTTT/LaCT in LA form, parallel equivalence, non-reducibility cases |
| `induction`     | 4     | Two chained inductions over three task families (anomalies; ablation) |
| `abduction`     | 1     | LA view vs memorization view as competing explanations of the four-anomaly pattern |
| `compare`       | 1     | Sub-strategy of the abduction |
| `contradiction` | 4     | Four per-anomaly contradictions: each memorization-view *prediction* contradicts the corresponding observed anomaly |

`support` accounts for ~65% of strategies, within recommended limits; the high `deduction` count (22%) reflects the paper's heavily mathematical Section 5 (three theorems plus per-architecture instantiations).

### Figure / table reference coverage

Every figure and table in the paper is transcribed as a claim with `metadata`:

| Source       | Claim                                                                                  |
|--------------|----------------------------------------------------------------------------------------|
| Fig. 1       | `obs_inner_loss_decreases_with_steps`, `obs_perf_degrades_with_more_steps`            |
| Fig. 2       | `obs_qk_distributions_disjoint`, `obs_vo_distributions_also_disjoint`                  |
| Fig. 4       | `obs_parallel_end_to_end_speedup`                                                      |
| Table 1      | `obs_grad_ascent_table1`, `obs_q_replacement_table1`                                   |
| Table 2      | `obs_ablation_table2`, `obs_variant1_best`, `obs_variant6_minor_degradation`, `obs_remaining_components_marginal`, `obs_parallel_throughput` |
| Sec. 5.1 / Appx B-D | `claim_thm_5_1`, `claim_thm_5_2`, `claim_thm_5_3` |
| Sec. 5.3 / Appx E   | `claim_lact_in_la_form`, `claim_weight_norm_does_not_break_la`, `claim_weight_norm_breaks_simple_sum` |
| Sec. 5.4 / Appx F-G | `claim_vittt_glu_in_la_form`, `claim_vittt_dwconv_in_la_form`, `claim_vittt_in_la_form` |
| Appx H       | `claim_parallel_equivalent_to_recurrent`                                               |
| Appx I       | `claim_dynamic_kernel_breaks_parallel`, `claim_weight_norm_breaks_parallel`            |

### BP result summary

All 22 independent priors are filled. Junction-tree inference converges in **2 iterations, ~24 ms**.

| Region                                              | Mean belief | Notes                                                            |
|-----------------------------------------------------|------------:|------------------------------------------------------------------|
| Theorem-level claims (`claim_thm_5_1/2/3`)           | 0.991       | 0.97 architectural-assumption prior + 0.99 deduction warrants    |
| Top theoretical claim (`claim_ttt_is_linear_attention`) | 0.985    | Six-premise support, all premises strong                         |
| Anomaly explanations (`claim_anomalies_explained_by_la_view`) | 0.985 | LA view's four sub-explanations all near 1.0                  |
| Empirical observations (priors)                       | 0.93        | Anchored by Tables 1-2, Figs. 1-4; range [0.85, 0.97]           |
| Direct anomaly claims (`claim_anomaly_*`)            | 0.81        | Conclusion of two-observation supports with 0.92-0.97 priors      |
| Three-task anomaly induction                          | 0.83        | Per-task observations + cross-task induction chain               |
| Headline contributions (1, 2, 3)                      | 0.90        | (0.835, 0.967, 0.904) -- top of three-deep chains                |
| Memorization predictions (now-falsified)              | 0.11        | Per-anomaly contradictions correctly drive these down            |
| Memorization-view falsification                       | 0.71        | Conclusion of four-anomaly support, 0.92 warrant                 |
| Memorization hypothesis                               | 0.98        | Pulled up by abduction's compare equivalence; *predictions* suppressed instead |
| Parallel-form speedup (`claim_parallel_form_speedup`) | 0.910       | Three-premise support of throughput + e2e + equivalence theorem  |
| Simplifications preserve perf                         | 0.842       | Four-premise empirical support                                    |

The four contradiction operators (each pairing a memorization-view prediction with the corresponding observed anomaly) all "pick a side" cleanly: prediction suppressed to 0.07-0.15, anomaly preserved at 0.76-0.88.

## 2. Summary

The paper makes one diagnostic contribution (four anomalies that falsify the memorization view of TTT-with-KV-binding), one theoretical contribution (a constructive equivalence between TTT-KVB and learned linear attention), and one practical contribution (a six-step ablation that reduces complex TTT formulations to standard linear attention, plus a fully parallel formulation yielding 4.0x layer-throughput and 1.19x end-to-end training speedup).

1. **Section 4 (anomalies).** Four phenomena observed across three task families (LaCT-LLM language modeling, LaCT-NVS novel-view synthesis, ViTTT-B image classification): (a) better inner-loop loss accompanies *worse* downstream performance over 1-64 inner steps (Fig. 1: PSNR drops from ~26 dB to ~18 dB while inner-loss drops from 0 to -60); (b) gradient ascent in the inner loop *preserves* downstream performance (Table 1: 16.43 -> 16.19 perplexity, 25.94 -> 25.85 dB PSNR, 79.34% -> 79.61% Top-1); (c) Q and K t-SNE distributions are visibly disjoint in pretrained LaCT-NVS (Fig. 2); (d) replacing Q with K at the layer output leaves performance essentially unchanged (Table 1: 16.43 -> 16.18 perplexity, 25.94 -> 25.95 dB, 79.34 -> 79.18%).

2. **Section 5 (theorems).** Under the structural assumption that the inner-loop final layer is linear and bias-free (verified for LaCT, ViTTT, Titans), Theorem 5.1 shows one inner-loop GD step transforms the output to $o = \hat{q}(S_0 + \hat{k}^\top \hat{v})$. Theorem 5.2 induces this over a token sequence to give $o_t = \hat{q}_t(S_0 + \sum_{i \le t} \hat{k}_i^\top \hat{v}_i)$. Theorem 5.3 extends to momentum, replacing $\hat{v}_i$ with the cumulative-momentum-weighted $m_i(k_i)$. Section 5.2 reads off natural explanations of all four anomalies; Sections 5.3-5.4 instantiate the framework on LaCT (SwiGLU + Muon) and ViTTT (GLU + 3x3 depthwise conv).

3. **Section 6 (practical).** A six-step ablation progressively removes (1) inner-loop updates of $\Theta$, (2) weight normalization, (3) multi-layer MLP depth, (4) per-token learning rates, (5) momentum, (6) gradient orthogonalization. Variant 1 (only update last layer) is best across all three task families (15.93 perplexity, 25.97 dB, 79.63%); Variant 6 (= standard linear attention) is within +0.4 / -0.2 / +0.2 of baseline. The two parallel-blocking conditions (dynamic kernel and weight-norm) are characterized in Appendix I. The parallel form yields 4.0x TTT-layer throughput (124.6M vs 30.18M tokens/sec on LLM) and 1.19x end-to-end training speedup with comparable convergence.

The structural argument is tight: the four anomalies *jointly falsify* the memorization view via per-anomaly contradiction operators (each driving a memorization-view prediction down to 0.07-0.15). The LA view simultaneously *explains* all four anomalies through Theorems 5.1-5.3, *exposes* the redundant components via the ablation trajectory, and *unlocks* parallelism via the associativity condition. Three-task induction strengthens the cross-architecture generalization. The strongest evidence anchors are Tables 1-2 (priors 0.93-0.97) and the four contradiction operators (1.0 each).

## 3. Weak Points

| Claim / strategy                                       | Belief / prior | Issue                                                                                                                                                                                                                                                                                          |
|--------------------------------------------------------|---------------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `claim_anomaly_distributional_asymmetry`                | 0.76           | Q-K asymmetry rests on a single qualitative t-SNE visualization (Fig. 2) on a single architecture (LaCT-NVS); no quantitative overlap metric is reported. The other three anomalies have stronger (Table 1, Fig. 1) anchors. The 0.92 prior on `obs_qk_distributions_disjoint` reflects this. |
| `claim_memorization_view_falsified`                     | 0.71           | Conclusion of a four-premise support (one per anomaly). Even with strong per-anomaly beliefs (0.76-0.88) the multiplicative effect plus the 0.92 warrant prior caps the belief in the low 0.7s. The four per-anomaly contradiction operators provide complementary hard constraints.       |
| `claim_anomalies_hold_vittt`                            | 0.80           | Only Anomalies 2 (Q->K) and 4 (gradient ascent) are tested on ViTTT-B. Anomalies 1 (Q-K asymmetry) and 3 (inner-loss-vs-perf) are not separately reported, so the per-task confirmation is *partial*. Prior on the support warrant set to 0.85 (vs 0.95 for LaCT-LLM/NVS).            |
| `claim_simplifications_preserve_performance`            | 0.84           | Conclusion of a four-premise support over Table 2 observations. The qualitative claim "most components are redundant" depends on accepting +0.4 perplexity / -0.2 dB as small.                                                                                                          |
| `claim_contribution_anomalies`                          | 0.84           | Top of a three-hop chain (table data -> formal anomalies -> falsification -> contribution). Multiplicative belief decay is the cause.                                                                                                                                                       |
| `claim_anomalies_general_law`                           | 0.83           | Derived from cross-task induction; held back by the partial ViTTT confirmation.                                                                                                                                                                                                                |
| `obs_remaining_components_marginal`                     | 0.88 (prior)   | Synthesis claim about Table 2 -- "most components contribute marginally" -- is qualitative.                                                                                                                                                                                                  |
| Memorization-hypothesis posterior                       | 0.98           | The bare hypothesis (leaf claim, prior 0.55) is pulled high by the abduction's compare(...) equivalence with `claim_anomalies_explained_by_la_view`. The substantive refutation lives in the four contradiction operators that drive each *consequence* of the hypothesis to 0.07-0.15. |

The maximum reasoning-chain depth from leaf observation to contribution claim is **3 hops** (e.g. `obs_perf_degrades_with_more_steps` -> `claim_anomaly_inner_vs_outer` -> `claim_memorization_view_falsified` -> `claim_contribution_anomalies`), keeping multiplicative decay manageable.

## 4. Evidence Gaps

### 4.1 Missing experimental validations

| Gap                                                                                                               | Why it would help                                                                                                                                                              |
|-------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Quantitative Q-K overlap metric on Fig. 2**                                                                     | The distributional-asymmetry anomaly currently rests on a qualitative t-SNE visualization. A measurable mismatch metric (e.g. 1-Wasserstein, MMD between Q and K samples) would replace the visual claim with a numerical one and lift `obs_qk_distributions_disjoint` from 0.92 toward 0.97. |
| **Q-K asymmetry on LLM and image-classification tasks**                                                            | Fig. 2 only visualizes Q-K for LaCT-NVS. Replicating on LaCT-LLM and ViTTT-B would close a per-task confirmation gap and lift `claim_anomalies_general_law`. |
| **Anomalies 1 and 3 on ViTTT-B**                                                                                  | Currently only Anomalies 2 and 4 are tested on ViTTT-B; testing 1 and 3 would close the cross-task confirmation. |
| **Per-step variance / multi-seed runs on Tables 1-2**                                                             | All Table 1-2 cells are single-seed point estimates. Several gaps (Variant 6 vs Baseline = +0.4 perplexity, ViTTT 79.34 vs 79.18 = -0.16%) are within plausible single-seed noise. |
| **Direct intervention test of the LA reformulation's predictions**                                                | Section 5.2 reads explanations *off* the theorems. A causal test would force one of the LA view's predictions and compare the resulting performance curve to the LA-predicted shape. |
| **Throughput and end-to-end speedup on tasks beyond LaCT-LLM**                                                    | Sec. 6.2's 4.0x throughput / 1.19x e2e speedup is reported only on LaCT-LLM. NVS and image classification might have different memory / compute profiles for the parallel form. |
| **Deeper inner-loop MLPs on more tasks**                                                                          | Step 3 (collapse MLP) is the costliest step on NVS (-0.22 dB PSNR). Whether deeper MLPs help on other spatial-reasoning tasks would test the LA view's prediction. |

### 4.2 Untested conditions

- **Non-linear final layers.** Section 7 explicitly acknowledges that all theory assumes a linear bias-free final layer. The behavior of TTT with non-linear final layers is open.
- **Other TTT variants.** The paper analyzes LaCT and ViTTT explicitly; Titans is mentioned but not separately analyzed under the LA reformulation.
- **Larger model scales.** All experiments use 90M-760M parameter models. Whether the simplification trajectory's near-flat performance generalizes to 7B+ is open.
- **TTT-E2E.** The paper exclusively addresses TTT-KVB; whether end-to-end TTT methods admit a similar LA reformulation is not analyzed.

### 4.3 Competing explanations not fully resolved

The paper's principal contradiction is between the LA view and the memorization view. The four per-anomaly contradiction operators correctly suppress each *prediction* of the memorization view. The abduction operator (`abd_la_over_memorization`) further encodes the inference-to-best-explanation. Note that the compare's internal equivalences keep the *bare* memorization hypothesis posterior high (0.98), but every concrete consequence of that hypothesis is suppressed; the dialectical refutation is at the *prediction* level, which is what the four contradictions capture.

## 5. Contradictions

### Explicit contradictions modeled with `contradiction()`

| Operator                          | Side A (memorization-view prediction)                              | Side B (observed anomaly)                       | Resolution                              |
|-----------------------------------|--------------------------------------------------------------------|--------------------------------------------------|-----------------------------------------|
| `contra_inner_vs_outer`           | Lower inner-loss should improve task perf (prior 0.60 -> 0.12)    | More inner steps degrade perf (0.80)             | BP picks Side B (anomaly), prior=0.97. |
| `contra_gradient_ascent`          | Sign-inverted optimization should sharply hurt (prior 0.65 -> 0.11) | Gradient ascent preserves/improves perf (0.84)    | BP picks Side B, prior=0.97.            |
| `contra_qk_overlap`               | Q-K must overlap for retrieval (prior 0.60 -> 0.15)               | Q-K t-SNE shows pronounced mismatch (0.76)       | BP picks Side B, prior=0.95.            |
| `contra_q_required`               | Replacing q with k must degrade perf (prior 0.60 -> 0.07)         | Q-K substitution leaves perf unchanged (0.88)    | BP picks Side B, prior=0.95.            |

All four contradictions resolve cleanly -- the operators hover at >0.998 belief, indicating the constraint is firmly satisfied.

### Internal tensions not modeled as formal contradictions

* **"Most components are redundant" vs "two notable exceptions."** Sec. 6.1 says most TTT design components contribute only marginally, then notes that deeper MLPs help on NVS and gradient orthogonalization helps on LLM. These can both be true (the qualifier "most" admits exceptions) but invite more careful task-dependent analysis.
* **Restricted theory scope vs broad empirical claim.** The theory assumes a linear bias-free final layer, but the empirical claims (anomalies, simplification) are demonstrated on architectures that satisfy this. The implicit scope-match between theory and experiment is consistent but worth noting.

## 6. Confidence assessment

Tier the **exported claims** (cross-package interface) into confidence levels:

| Tier         | Belief range | Exported claims                                                                                  |
|--------------|--------------|--------------------------------------------------------------------------------------------------|
| Very high    | > 0.95       | `claim_anomalies_explained_by_la_view` (0.985), `claim_ttt_is_linear_attention` (0.985), `claim_contribution_equivalence` (0.967) |
| High         | 0.85 - 0.95  | `claim_parallel_form_speedup` (0.910), `claim_contribution_practical` (0.904)                    |
| Moderate     | 0.70 - 0.85  | `claim_simplifications_preserve_performance` (0.842), `claim_contribution_anomalies` (0.835), `claim_memorization_view_falsified` (0.708) |
| Tentative    | < 0.70       | (none of the exported claims)                                                                    |

The theoretical contributions (LA equivalence, anomaly explanations) are at the very-high tier because they are deductive consequences of well-anchored architectural assumptions and observation-grounded anomalies. The practical / synthesis contributions sit in the high-to-moderate range because they are conclusions of multi-premise support strategies whose multiplicative effect bounds belief from above.
