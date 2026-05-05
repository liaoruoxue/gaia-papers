# Critical Analysis: DeepSeek Visual Primitives — Thinking with Visual Primitives

Knowledge package: `github-visual-primitives-gaia`. Source: GitHub release by DeepSeek-AI + Peking University + Tsinghua University on 2026-04-30 [@DeepSeekVisualPrimitives], subsequently withdrawn. Content reconstructed from a CSDN deep read [@CSDNDeepRead], Phoenix Technology coverage [@PhoenixTech], and 36Kr coverage [@ThirtySixKr].

## 1. Package Statistics

### Knowledge graph counts

| Item                                       | Count |
|--------------------------------------------|------:|
| Knowledge nodes (total compiled)           |  173  |
| Settings                                   |   20  |
| Questions                                  |    1  |
| Claims (user-visible)                      |   71  |
| Compiler helper claims (`__`)              |   80  |
| Strategies                                 |   61  |
| Operators (`contradiction`)                |    2  |
| Modules                                    |   10  |

### Claim classification

| Role                                      | Count |
|-------------------------------------------|------:|
| Independent (need prior, all assigned)    |  15   |
| Derived (BP propagates)                   |  54   |
| Structural (operator-derived)             |   2   |

### Strategy type distribution

| Type            | Count | Notes |
|-----------------|------:|-------|
| `support`       |   54  | Default soft deduction; covers most chains. |
| `induction`     |    2  | 3-benchmark induction over Pixmo-Count + Maze + Path Tracing supporting the cross-benchmark outperformance law. |
| `abduction`     |    1  | Central abduction: visual-primitive design + Reference-Gap diagnosis (H) vs trivial confounds (Alt = bigger MoE / more data / better base); discriminated by the 81-KV-entry / 7056x compression observation. |
| `compare`       |    1  | Sub-strategy of the central abduction. |
| `contradiction` |    2  | (i) Reference-Gap diagnosis vs the prevailing Perception-Gap-is-the-bottleneck assumption; (ii) the prevailing 'more visual tokens = better' assumption vs the 81-KV-entry outperformance. |

### BP result summary

All 15 independent priors are assigned. Junction-tree exact inference converges in **2 iterations / ~20 ms**. 31 user-visible claims have belief > 0.90; 67 have belief > 0.50; 2 (the foils) are suppressed below 0.07.

| Region                                            | Belief | Notes |
|---------------------------------------------------|-------:|-------|
| `_anon_000` (central abduction conclusion)        | 1.000  | Visual-primitive design abduction concludes near-certain. |
| `contra_reference_vs_perception`                  | 1.000  | Perception-Gap foil contradicted. |
| `contra_more_tokens_vs_81kv`                      | 0.999  | More-tokens-is-better foil contradicted. |
| `claim_maze_deepseek`                             | 0.984  | DeepSeek Maze 66.9% (panel best, +16.3 pp over GPT-5.4). |
| `claim_path_deepseek`                             | 0.984  | DeepSeek Path Tracing 56.7% (panel best, +10.2 pp over GPT-5.4). |
| `claim_pixmo_deepseek`                            | 0.984  | DeepSeek Pixmo-Count 89.2% (panel best). |
| `claim_architecture_supports_high_density`        | 0.952  | 7056x compression supports density-over-volume. |
| `claim_324_to_81_kv`                              | 0.941  | 324 tokens -> 81 KV entries via 4x CSA. |
| `claim_2916_to_324_tokens`                        | 0.934  | 2916 patches -> 324 tokens via 3x3 merge. |
| `claim_results_table`                             | 0.933  | Headline results table; pulled up by induction back-channel. |
| `claim_pixmo_frontier / maze_frontier / path_frontier` | 0.933 | Frontier baselines, anchored by the table. |
| `claim_cross_benchmark_outperformance`            | 0.928  | Central observation; load-bearing for the abduction. |
| `claim_information_density_over_volume`           | 0.928  | H prediction in the central abduction. |
| `claim_alt_trivial_confounds`                     | 0.924  | Alt's belief is pulled up by the abduction back-channel; the abduction conclusion (1.0) reflects that the comparison correctly discriminates H over Alt. |
| `claim_industry_chases_perception`                | 0.920  | State of practice; high prior 0.92. |
| `claim_end_to_end_7056x`                          | 0.918  | 7056x end-to-end compression. |
| `claim_visual_primitives_close_reference_gap`     | 0.916  | Mechanism: precise primitives close the Reference Gap. |
| `claim_phase3_rft / phase4_distillation`          | 0.91   | Last two phases of the Expert-Merge-Distill pipeline. |
| `claim_layer1_solution`                           | 0.921  | Layer-1 solution: point-not-describe. |
| `claim_method_lift_to_thought_unit`               | 0.889  | Method core: primitives as thought-units. |
| `claim_pipeline_motivation`                       | 0.871  | Separate-then-merge motivation. |
| `claim_natural_language_imprecise_in_continuous_space` | 0.856 | Foundational language property; prior 0.85. |
| `claim_reference_gap_is_actual_bottleneck`        | 0.817  | Diagnosis; pulled up by the contradiction with the Perception-Gap foil. |
| `claim_industry_perception_path_hits_ceiling`     | 0.815  | Consequence of the diagnosis. |
| `claim_perception_gap_is_actual_bottleneck`       | 0.065  | Foil; suppressed by contra_reference_vs_perception. |
| `claim_more_tokens_is_better`                     | 0.026  | Foil; suppressed by contra_more_tokens_vs_81kv against the 81-KV-entry outperformance. |

## 2. Summary

The argument structure is **headline = a multimodal-LLM design that lifts box / point coordinate tokens to first-class thought-unit status inside the chain-of-thought significantly outperforms frontier models on spatial-reasoning benchmarks while using orders-of-magnitude fewer visual tokens**, anchored by:

1. **Two contradiction operators**: (i) the Reference-Gap diagnosis vs the prevailing Perception-Gap-is-the-bottleneck assumption, and (ii) the prevailing 'more visual tokens = better' assumption vs the 81-KV-entry outperformance.
2. **One central abduction**: hypothesis = visual-primitive design + Reference-Gap diagnosis explains the cross-benchmark outperformance pattern; alternative = trivial confounds (bigger MoE / more data / better base model). The discriminating observation is **panel-best scores at orders-of-magnitude lower visual-token budget than frontier models** -- directionally incompatible with what 'bigger MoE / more visual tokens' would predict.
3. **One 3-benchmark induction**: Pixmo-Count + Maze Navigation + Path Tracing each independently support the cross-benchmark outperformance law; especially load-bearing because Maze and Path Tracing place all three frontier models at or below the ~50% random baseline, isolating spatial-reasoning capability from general multimodal capability.

The argument's structural strength comes from the **directional opposition** between H's and Alt's predictions: H predicts panel-best at low visual-token budget; Alt predicts panel-best requires more of the conventional levers. The 81-KV-entry observation discriminates because 81 entries is a count, not a continuum -- frontier models are not on the same axis as DeepSeek's compression ratio.

The two formal contradictions are robust: the Reference-Gap-vs-Perception-Gap distinction is exhaustive at the headline level (these are claims about *the* bottleneck), and the 'more tokens = better' foil collapses cleanly when the 81-KV-entry result holds.

## 3. Weak Points

| Claim | Belief | Issue |
|---|---:|---|
| `claim_alt_trivial_confounds` | 0.924 | Alt's belief is *pulled up* by the abduction back-channel; this is structurally expected (any explainer of a high-belief observation is boosted). The abduction conclusion (1.0) reflects that the *comparison layer* correctly discriminates H over Alt -- Alt's high marginal belief does not undermine the abduction. |
| `claim_lim_topology_weakness` | 0.75 | Set at the prior; no incoming strategy lifts it. This is appropriate (it's a leaf observation flagged by the source) but the supporting OOD experiments are not separately reported in secondary sources. Conservative belief is correct. |
| `claim_lim_trigger_word_dependency` | 0.75 | Same as above: leaf observation, no separate ablation evidence in secondary sources. |
| `claim_rm_decomposition_rationale` | 0.744 | Three-premise support pulls down via the BP multiplicative effect; conclusion is plausible but not lifted because each component RM has only 0.80-0.83 prior under reconstruction-source uncertainty. |
| `claim_lim_topology_sharpening_tradeoff / claim_lim_trigger_analogue_to_armskill` | 0.76 / 0.83 | Interpretive claims (parallels to RL theory and to ARM 7-modality skill limit) carry uncertainty inherent in cross-system analogies. |
| `claim_results_table / claim_architecture_table / claim_pipeline_diagram / claim_pretrain_filter_table / claim_coldstart_table` | 0.75-0.93 | All table claims sit on prior 0.75-0.83 (reconstruction-source discount). The cross-benchmark induction back-channel does lift `claim_results_table` to 0.93, but the underlying numerical content rests on a single-rooted provenance chain (the deleted GitHub repo). |

## 4. Evidence Gaps

### 4a. Source-reliability (unique to this package)

| Gap | Notes |
|---|---|
| Original GitHub repository withdrawn | The repo at `https://github.com/deepseek-ai/Thinking-with-Visual-Primitives` was deleted shortly after the 2026-04-30 release. Independent verification of every numerical claim is impossible without it. The CSDN / Phoenix Tech / 36Kr coverage all ultimately trace back to the single source. |
| No peer-reviewed paper, no arXiv ID | The release was a GitHub-only artifact; we cite it as `software` type. There is no arXiv preprint, no peer-reviewed publication, and no replication from the broader community as of the formalization date. |
| Numerical claims rest on single-rooted provenance | Even though three independent secondary sources report the same numbers, all three trace back to the original repo content. Cross-source agreement therefore does not deliver true independence. |
| Per-task ablations not reported | Per-component ablations (e.g. removing CSA, removing 3x3 merge, removing per-expert pre-training, removing one of the three RM terms) are not separately quantified in the secondary sources. The 7056x figure cannot be decomposed into per-component contributions. |

### 4b. Untested conditions

| Gap | Notes |
|---|---|
| OOD topology benchmarks not numerically reported | The topology generalization weakness is qualitative; we have no numbers like 'on hexagonal-out-of-distribution mazes, accuracy drops to X%'. |
| Spontaneous-emission rate not reported | The trigger-word dependency is qualitatively flagged; the actual rate of spontaneous (no-trigger) primitive emission in the trained model is not measured. |
| Cross-modality benchmarks beyond spatial reasoning | Pixmo-Count, Maze, and Path Tracing are all spatial-reasoning tasks. General multimodal benchmarks (MMMU, MMBench, ScienceQA) are not in the panel; whether the visual-primitive method helps or hurts on non-spatial multimodal tasks is unknown. |
| Inference-time cost not characterised | The 81-KV-entry budget is for visual tokens; total inference cost (CoT length + primitive emission overhead + V4-Flash MoE expert routing) is not reported. |
| Ablation of the 4-phase training recipe | Whether all four phases (separate-experts -> per-expert GRPO -> RFT -> on-policy distillation) are necessary, or whether a subset suffices, is not separately measured. |

### 4c. Competing explanations not fully resolved

| Gap | Notes |
|---|---|
| Bigger MoE 13B-activated alternative | The abduction's Alt explicitly raises this; the 81-KV-entry observation discriminates directionally, but a controlled ablation (same V4-Flash backbone, no visual-primitive training) is not reported. |
| Cold-start data scale effect | 604K post-training samples is a substantial corpus; whether the gain comes primarily from the data scale (regardless of the visual-primitive design) or from the design itself is not separately measured. |
| Reward-model-driven sharpening alone | If just the per-task accuracy RM (without primitives) sufficed for Maze 66.9%, the visual-primitive method would not be necessary. The decomposition is not reported. |

## 5. Contradictions

### 5a. Explicit contradictions (modeled with `contradiction()`)

1. **`contra_reference_vs_perception`**: Reference-Gap diagnosis vs Perception-Gap-is-the-bottleneck foil. BP resolves: Reference-Gap diagnosis at 0.82, Perception-Gap foil at 0.07. The contradiction operator carries belief 1.000 -- exactly one of the two is true, and BP picks the Reference Gap.
2. **`contra_more_tokens_vs_81kv`**: 'more visual tokens reliably improves visual reasoning' vs the cross-benchmark outperformance at ~81 KV entries. BP resolves: cross-benchmark outperformance at 0.93, more-tokens-foil at 0.03. The contradiction operator carries belief 0.999.

### 5b. Internal tensions not modeled as formal contradictions

| Tension | Notes |
|---|---|
| Trigger-word dependency vs the 'pointing-during-reasoning' design philosophy | The method's promise is that the model emits primitives at the moment they aid reasoning. The trigger-word dependency means primitive emission is gated on prompt phrasing rather than reasoning need. These are 'in tension' (the method has not yet fully delivered on its philosophy) but both can be true: the architecture supports primitive emission, the training recipe has not yet internalized the selection policy. Flagged here rather than modeled as `contradiction()`. |
| Topology generalization weakness vs the 7056x compression / density-over-volume claim | If the model generalizes weakly across topologies, then high-density representation is partially in-distribution-specific. This does not contradict the density-over-volume thesis, but it qualifies it: the few-but-well-organized tokens are well-organized for *training-distribution* topologies. |
| Information density > volume vs the 460K maze sample count | The cold-start corpus is large (604K total, 460K maze). 'Density > volume' is a model-level claim, not a data-level one; large training data is not in tension with a small visual-token budget. Worth flagging because a casual reader might conflate the two. |

## 6. Confidence Assessment

| Tier | Belief range | Claims |
|------|-------------|--------|
| **Very high (>= 0.95)** | 0.95-1.00 | Both contradiction operators (~1.0); the central abduction conclusion (1.0); per-benchmark DeepSeek scores via the induction back-channel (0.984 each); architecture-supports-high-density (0.952). |
| **High (0.85-0.95)** | 0.85-0.95 | The 7056x compression chain (Stages 1-3 and end-to-end, 0.90-0.94); cross-benchmark outperformance (0.93); information density over volume (0.93); results table and architecture table (0.83-0.93); Phase 1-4 of the training pipeline (0.88-0.91); pointing-during-reasoning (0.92); language imprecision foundational (0.86); industry-chases-perception state of practice (0.92); next-frontier slogan (0.85); meta-thesis (0.83). |
| **Moderate (0.75-0.85)** | 0.75-0.85 | Reference-Gap diagnosis (0.82); industry-perception ceiling (0.81); coldstart / pretrain filter tables (0.80-0.88); RM components (0.80-0.83); RM decomposition rationale (0.74); limitation interpretations (0.76-0.83). |
| **Tentative (< 0.75)** | <0.75 | None among user-visible claims. The two leaf limitation observations (`claim_lim_topology_weakness`, `claim_lim_trigger_word_dependency`) sit at exactly 0.75 (their conservative priors, no upward lift). |
| **Suppressed foils** | < 0.10 | `claim_perception_gap_is_actual_bottleneck` (0.065); `claim_more_tokens_is_better` (0.026). |

## 7. Methodological Note

This package's priors carry a deliberate source-reliability discount. Architectural-design claims corroborated across CSDN / Phoenix Tech / 36Kr sit at 0.78-0.85. Numerical empirical claims (per-method benchmark scores) sit at 0.75 because the original repo is no longer accessible and cross-source agreement does not deliver true independence (all three secondary sources trace back to the same deleted artifact). Architectural claims that are directly arithmetic (Stages 1-3 of the compression chain, the 32.4% filter yield, the 604K cold-start total) are not independently discounted -- the arithmetic is what the source asserts and is internally checkable.

A non-trivial belief calibration consequence: the central abduction conclusion sits at 1.000 *in spite of* the conservative source-reliability priors on `claim_results_table` (0.75) and the architecture and training claims (0.78-0.85). This robustness comes from the directional opposition between H and Alt -- once the observation is conditioned on, the abductive comparison is dominated by which prediction direction matches, not by the absolute prior on the observation. If a future direct verification raises the source-reliability priors, the user-visible derived claim beliefs in the 0.85-0.95 tier would each lift by a few percentage points, but the contradictions and the central abduction would not change qualitatively.
