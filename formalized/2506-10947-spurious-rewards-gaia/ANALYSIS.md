# Critical Analysis — Spurious Rewards: Rethinking Training Signals in RLVR

**Package:** `2506_10947_spurious_rewards`
**Source:** arXiv 2506.10947 — "Spurious Rewards: Rethinking Training Signals in RLVR"
**Analysis date:** 2026-04-22
**BP run:** `gaia infer .` — JT (exact), 11 ms, converged after 2 iterations

---

## 1. Package Statistics

### Node counts

| Node type | Count |
|-----------|-------|
| `claim` (named) | 38 |
| `setting` | 5 |
| `question` | 3 |
| Total beliefs inferred | 60 |

Named claims include 10 independent-premise (leaf) claims assigned explicit priors in `priors.py`, plus additional derived claims, alternative hypotheses, prediction claims, and implication claims.

### Strategy type distribution

| Strategy | Count |
|----------|-------|
| `support` | 16 |
| `deduction` | 0 |
| `abduction` | 2 |
| `induction` | 2 |
| `compare` | 2 |
| `contradiction` | 1 |

The argument leans heavily on `support` chains backed by empirical data. The two `abduction` nodes select between competing hypotheses (pretraining-surfacing vs. RLVR-teaches-new). The `induction` nodes aggregate evidence across three independent model families. The single `contradiction` node formalises the mutual exclusivity between `claim_rlvr_teaches` and `claim_pretraining_hypothesis`.

### Independent-premise (leaf) count

10 explicit priors assigned in `priors.py`:
`claim_qwen7b_math500_results`, `claim_spurious_fails_non_qwen`, `claim_aime_results`, `claim_code_freq_increases_rlvr`, `claim_code_accuracy_advantage`, `claim_qwen_pretraining_code_freq`, `claim_model_family_consistency`, `claim_clipping_amplifies_prior`, `claim_clipping_qwen_specificity`, `claim_prompt_sensitivity`, `claim_ttrl_one_shot_same_pattern`, plus alternative and prediction priors.

### BP summary

| Metric | Value |
|--------|-------|
| Method | Junction Tree (exact) |
| Runtime | 11 ms |
| Converged | Yes |
| Iterations | 2 |
| Tree width | 4 |

Convergence in 2 iterations at treewidth 4 indicates a sparse, tree-like dependency graph with no iterative inference difficulties. The JT method gives exact posteriors.

---

## 2. Summary

The paper argues that RLVR with verifiable rewards does not teach models new reasoning capabilities but instead surfaces latent behavioral patterns installed during pretraining. The central evidence is that completely spurious reward signals — random (Bernoulli γ = 0.5), format-only (any boxed expression), and even deliberately incorrect majority-vote labels — yield 14–24 percentage-point gains on MATH-500 for Qwen2.5-Math-7B, only marginally below the 29 pp achieved by ground-truth rewards. The same signals fail outright on OLMo2 and Llama model families. The mechanistic explanation is a two-step chain: (1) Qwen2.5-Math-7B has a 65% pre-RL baseline of code-assisted reasoning (a high-accuracy strategy at 60.9%), and (2) GRPO's PPO-style clipping term creates a nonzero gradient bias under random rewards that asymmetrically amplifies high-prior token sequences, rapidly shifting the model to ~90%+ code-reasoning frequency. BP assigns the pretraining-surfacing hypothesis (`claim_pretraining_hypothesis`) a near-certain posterior of **0.9999968**, crushes the competing "RLVR teaches new capabilities" claim (`claim_rlvr_teaches`) to **0.00067**, and propagates strong confidence (> 0.97) to the two core empirical anchors (`claim_rlvr_improves_qwen` = 0.9994, `claim_spurious_fails_non_qwen` = 0.9723). The argument structure is tightly integrated across four evidence streams — cross-model replication, AIME out-of-distribution tests, code-frequency decomposition, and clipping-mechanism ablations — making it one of the more internally consistent critiques of benchmark-centric RLVR evaluation in recent ML literature.

---

## 3. Weak Points

The following named claims have BP beliefs below 0.80 or are alternative hypotheses with belief above 0.25 (indicating residual uncertainty).

### Claims with belief < 0.80

| Claim | Belief | Issue |
|-------|--------|-------|
| `claim_bad_code_reduction` | 0.500 | No prior assigned; claim sits at the uninformative default. The Code→Lang 93.9% contribution figure for Qwen2.5-7B is not connected via a `support` chain to any prior-carrying upstream claim, leaving it unresolved by BP. |
| `claim_code_prompting_results` | 0.500 | No prior assigned. The code-forcing prompt ablation (Table 3) is a key empirical control but is not formally linked into the inference graph, weakening its epistemic weight within the DSL. |
| `claim_compound_reward_no_python` | 0.500 | No prior assigned. This is the causal intervention establishing code reasoning as the mechanism for format reward gains — arguably the most important mechanistic result — yet it has no prior and no upstream support. |
| `claim_format_reward_effectiveness` | 0.500 | No prior assigned. The +13.8 pp format-reward result is mentioned in `motivation.py` but not connected to an explicit prior in `priors.py`. |
| `claim_incorrect_reward_mechanism` | 0.500 | No prior assigned. The hypothesized dual mechanism (near-correct labels + format extraction) is speculative and lacks its own empirical support edge. |
| `claim_no_repetition_pattern` | 0.500 | No prior assigned. A potentially significant secondary finding (no-repetition reward also works on Qwen-Math) is entirely disconnected from BP inference. |
| `claim_open_question_mechanism` | 0.500 | No prior assigned; this is explicitly flagged as open, but the 0.5 default obscures the fact that the mechanism description in the paper is genuinely partial. |
| `claim_post_rl_saturation` | 0.500 | No prior assigned. The saturation finding for Qwen-Instruct models (Figure 19) is consistent with the pretraining hypothesis but receives no formal inference weight. |
| `claim_python_reward_results` | 0.500 | No prior assigned. The Python-reward RLVR experiment is a direct test of code elicitation but is not connected to the main inference graph. |
| `claim_qwen15b_results` | 0.500 | No prior assigned. Qwen2.5-Math-1.5B results (slower random-reward gains) are potentially important for size-scaling conclusions but are isolated from BP. |
| `claim_qwen7b_amc_results` | 0.500 | No prior assigned. The AMC results are mentioned in motivation but not linked as a prior-carrying claim. |
| `claim_random_gamma_robustness` | 0.500 | No prior assigned. Gamma-robustness (γ ∈ {0.001, 0.3, 0.5, 0.7} all yield gains) is a key prediction of the pretraining hypothesis, but it sits at 0.5 because `priors.py` omits it. |
| `claim_smaller_models_less_spurious` | 0.500 | No prior assigned. The model-size conjecture is described as a conjecture in the paper itself; appropriate epistemic treatment is lacking. |
| `claim_implication_no_generalization` | 0.833 | Lowest-belief named implication. BP penalizes it relative to other implications because it depends on `claim_qwen_centric_risk` (0.859) and `claim_ttrl_one_shot_same_pattern` (0.900), both of which carry some uncertainty. |

### Alternative hypotheses with belief > 0.25

| Claim | Belief | Issue |
|-------|--------|-------|
| `alt_rlvr_teaches_new` | 0.412 | Despite the main hypothesis being crushed to near-zero, the alternative "RLVR teaches new capabilities" hypothesis retains 0.41 belief because it is a `claim` node whose prior (0.35) was updated upward by its supporting `support` edge — not fully suppressed by the contradiction with `claim_pretraining_hypothesis`. The DSL models `alt_rlvr_teaches_new` as distinct from `claim_rlvr_teaches`, so the contradiction operator does not reach it directly. This creates an apparent inconsistency in the graph: `claim_rlvr_teaches` = 0.00067 but `alt_rlvr_teaches_new` = 0.412. |
| `alt_code_elicitation_only_prompt` | 0.278 | Slightly above 0.25. The prompting-only alternative is partially falsified by compound no-Python reward results, but because `claim_compound_reward_no_python` has no prior (belief = 0.5), the falsifying evidence is not fully propagated. |

---

## 4. Evidence Gaps

### (a) Missing experimental validations

| Gap | Rationale |
|-----|-----------|
| **Replication on GPT-family or proprietary models** | All experiments use open-weight models. The claim that pretraining data distribution determines spurious-reward effectiveness cannot be verified for models whose training data is undisclosed. |
| **Scaling beyond 7B** | The largest model tested is 8B parameters. Whether the pretraining-surfacing effect holds at 70B+ or whether ground-truth rewards become differentially more important at scale is untested. |
| **Longer training runs** | Experiments stop at 300 steps. The AIME 2025 out-of-distribution result hints that ground truth rewards may become dominant at longer training horizons, but this is not tested. |
| **Reward models beyond binary verification** | All five reward types are binary (0/1). Whether dense process-reward models (PRMs) change the picture — and whether they constitute a different kind of "spurious" signal — is not addressed. |
| **Training data diversity beyond DeepScaleR** | All RLVR training uses DeepScaleR prompts. Whether the cross-model pattern holds on different math training datasets (e.g., NuminaMath, OpenMathInstruct) is untested. |

### (b) Untested conditions

| Condition | Why it matters |
|-----------|----------------|
| **Random reward with γ → 0 continuous** | The paper tests discrete γ ∈ {0.001, 0.3, 0.5, 0.7} and analytically argues γ = 0 fails. A continuous sweep near γ = 0 would sharpen the threshold claim. `claim_random_gamma_robustness` has belief 0.5 from the missing prior. |
| **Clipping ablation on Qwen2.5-7B (Bad-Code) and OLMo2** | The clipping-bias mechanism is validated primarily on Qwen2.5-Math-7B. Whether removing clipping on Bad-Code models actually restores performance is not tested, leaving `claim_clipping_qwen_specificity` partially unvalidated. |
| **SFT-then-RLVR pipeline with spurious rewards** | The paper studies base models and instruction-tuned variants. An SFT stage trained on code-reasoning traces, followed by spurious-reward RLVR, could test whether injecting pretraining-like patterns into other model families unlocks the spurious-reward effect. |
| **Non-math reasoning domains** | The entire paper is restricted to mathematical reasoning benchmarks. Whether the pretraining-surfacing mechanism extends to coding benchmarks (HumanEval, MBPP) or logical reasoning is entirely open — `claim_open_question_mechanism` = 0.5. |
| **Post-saturation probe for Qwen-Instruct models** | `claim_post_rl_saturation` = 0.5 due to missing prior. If Qwen-Instruct models have exhausted surfaceable representations, further probing of what genuine new reasoning would look like is needed. |

### (c) Competing explanations not fully resolved

| Competing explanation | Belief | Status |
|-----------------------|--------|--------|
| `alt_rlvr_teaches_new` — RLVR provides gradient direction for genuine learning | 0.412 | Partially suppressed but not eliminated. The formalization's `contradiction` operator targets `claim_rlvr_teaches` (0.00067) but `alt_rlvr_teaches_new` is a distinct node, so it retains residual belief. A future version should directly connect the contradiction to this node. |
| `alt_code_elicitation_only_prompt` — prompting alone explains code-frequency gains | 0.278 | Partially falsified by compound no-Python evidence, but that evidence (`claim_compound_reward_no_python` = 0.5) lacks a prior, so the falsification is attenuated. |
| **Distribution shift / memorization** — Qwen2.5-Math may have seen MATH-500 in pretraining | Not modeled | If Qwen2.5-Math-7B's pretraining data contained MATH-500 problems (a known risk for proprietary data pipelines), many of the "spurious-reward gains" could be explained by contamination-elicitation rather than code-strategy-surfacing. The paper does not formally address this. |
| **GRPO hyperparameter specificity** — results may depend on ε_c, λ, rollout count | Not modeled | The clipping mechanism's strength depends on the clipping threshold ε_c. Sensitivity to this hyperparameter is not ablated, making it unclear whether the mechanism generalizes to other GRPO configurations. |

---

## 5. Contradictions

### (a) Explicit `contradiction()` operators and BP resolution

The formalization contains one explicit contradiction:

**`not_both_teach_surface`** — `contradiction(claim_rlvr_teaches, claim_pretraining_hypothesis, prior=0.92)`

This node formalizes the mutual exclusivity between:
- `claim_rlvr_teaches`: "RLVR fundamentally teaches models new reasoning capabilities" — posterior **0.00067**
- `claim_pretraining_hypothesis`: "RLVR surfaces latent pretrained capabilities" — posterior **0.9999968**

BP resolution: The contradiction node itself has belief **0.9997** (high confidence that the two claims are indeed inconsistent). The overwhelming support for `claim_pretraining_hypothesis` from multiple empirical chains effectively suppresses `claim_rlvr_teaches` to near-zero. The resolution is strongly one-sided: the evidence fully disfavors the "teaches new capabilities" view, at least for Qwen2.5-Math models under 300-step GRPO training.

**Caveat:** `alt_rlvr_teaches_new` (a distinct node, belief = 0.412) is the alternative hypothesis tested in the `abduction` and `compare` nodes. It is not directly connected to the `contradiction` operator and retains residual belief. This is a structural gap: the formalization contradicts `claim_rlvr_teaches` but not `alt_rlvr_teaches_new`, even though they express the same concept.

### (b) Internal tensions not formally modeled

| Tension | Description |
|---------|-------------|
| **`pred_teaches` belief = 0.9947** | The prediction claims for the "teaches new reasoning" hypothesis received a very high posterior (0.9947), even though the hypothesis itself (`claim_rlvr_teaches` = 0.00067) is crushed. This is a structural artifact: `pred_teaches` is a claim node whose prior (0.30) was updated by `compare()` inference, but it is not connected to `claim_rlvr_teaches` in a way that allows the contradiction to suppress it. The high `pred_teaches` belief creates a confusing read-out alongside the near-zero `claim_rlvr_teaches`. |
| **Format reward mechanism vs. code mechanism** | The paper claims format reward (+13.8 pp) works via code elicitation (confirmed by format+no-Python ceasing gains). But `claim_format_reward_effectiveness` = 0.5 (no prior), `claim_compound_reward_no_python` = 0.5 (no prior), so this causal chain is not actually modeled in the inference graph. The compound-reward ablation — arguably the most important mechanistic result — is disconnected from BP. |
| **AIME 2024 vs. AIME 2025 interpretation** | The AIME 2024/2025 split is interpreted as evidence that spurious rewards only work on "in-distribution" problems the model has effectively memorized during pretraining. However, AIME 2025 problems also appear harder in absolute terms for all models, not just under spurious rewards. The paper does not fully disentangle difficulty from distribution shift, and the formalization does not model this confound. |
| **OLMo2-7B-SFT as Bad-Code** | OLMo2-7B-SFT is classified as "Bad-Code" (98% pre-RL code frequency, 21% code accuracy), making it the primary negative example. However, its instruction-tuning history differs fundamentally from Qwen's — its code behavior may be an SFT artifact rather than a pretraining signal, which would partially undermine the pretraining hypothesis. The formalization does not model this alternative explanation for OLMo2-SFT's behavior. |

---

## 6. Confidence Assessment

Beliefs from `gaia infer` tiered by confidence:

### Very high (belief >= 0.97)

| Claim | Belief | Description |
|-------|--------|-------------|
| `claim_pretraining_hypothesis` | 0.9999968 | Core thesis: RLVR surfaces pretraining, not new learning |
| `claim_rlvr_improves_qwen` | 0.9994 | Spurious rewards yield large gains on Qwen2.5-Math |
| `not_both_teach_surface` | 0.9997 | The two hypotheses are mutually exclusive |
| `pred_pretraining` | 0.9992 | Pretraining hypothesis makes accurate predictions |
| `claim_implication_corrupted_supervision` | 0.9786 | Corrupted supervision can still elicit pretraining patterns |
| `claim_qwen7b_math500_results` | 0.9842 | Numerical MATH-500 gains across all reward types |
| `claim_code_accuracy_advantage` | 0.9732 | Code reasoning 60.9% vs language 35.0% for Qwen-Math-7B |
| `claim_qwen_pretraining_code_freq` | 0.9730 | 65% pre-RL code frequency for Qwen2.5-Math-7B |
| `claim_spurious_fails_non_qwen` | 0.9723 | Spurious rewards fail or hurt Llama and OLMo2 |

### High (belief 0.90–0.97)

| Claim | Belief | Description |
|-------|--------|-------------|
| `claim_grpo_clipping_bias` | 0.9503 | Formal derivation of nonzero gradient bias under clipping |
| `claim_prompt_sensitivity` | 0.9481 | Qwen2.5-Math-7B unreasonably sensitive to prompt content |
| `claim_code_freq_increases_rlvr` | 0.9650 | Code frequency 65% to 90%+ after RLVR regardless of reward type |
| `claim_lang_to_code_contribution` | 0.9391 | Lang to Code switching accounts for 58.3% of gains |
| `claim_aime_results` | 0.9418 | AIME 2024 spurious gains; AIME 2025 spurious gains disappear |
| `claim_model_family_consistency` | 0.9418 | Within-family consistency across model sizes |
| `claim_qwen_general_also_gains` | 0.9241 | General-purpose Qwen2.5-7B also gains from spurious rewards |
| `claim_olmo_only_gt` | 0.9241 | OLMo2 gains only from ground truth, hurt by spurious |
| `claim_clipping_qwen_specificity` | 0.9192 | Clipping benefits only models where high-prior behavior is accurate |
| `claim_ttrl_one_shot_same_pattern` | 0.9000 | Published TTRL/One-Shot RL also fails beyond Qwen |
| `claim_llama_partial` | 0.8992 | Llama gains only from informative signals |
| `claim_implication_pretraining_primary` | 0.8885 | Pretraining is primary determinant of RLVR effectiveness |

### Moderate (belief 0.80–0.90)

| Claim | Belief | Description |
|-------|--------|-------------|
| `claim_clipping_amplifies_prior` | 0.880 | Empirical: clipping increases token probability and code frequency |
| `claim_no_clipping_no_gain` | 0.854 | Without GRPO clipping, random rewards yield no robust improvement |
| `claim_qwen_centric_risk` | 0.859 | Research methodology risk from Qwen-centric RLVR evaluation |
| `claim_implication_no_generalization` | 0.833 | RLVR effects are model-family-specific |

### Tentative (belief <= 0.50 or structurally unresolved)

| Claim | Belief | Description |
|-------|--------|-------------|
| `claim_bad_code_reduction` | 0.500 | Code to Lang contributes 93.9% of Qwen2.5-7B gains — unpriorized |
| `claim_compound_reward_no_python` | 0.500 | Causal code-channel intervention — unpriorized, key mechanistic gap |
| `claim_format_reward_effectiveness` | 0.500 | +13.8 pp format reward — unpriorized |
| `claim_random_gamma_robustness` | 0.500 | Gamma-robustness across {0.001, 0.3, 0.5, 0.7} — unpriorized |
| `claim_no_repetition_pattern` | 0.500 | No-repetition reward as second surfaceable pattern — unpriorized |
| `claim_post_rl_saturation` | 0.500 | Post-RL Qwen-Instruct saturation — unpriorized |
| `claim_qwen15b_results` | 0.500 | Qwen2.5-Math-1.5B size-scaling results — unpriorized |
| `alt_rlvr_teaches_new` | 0.412 | Alternative hypothesis retains belief due to graph topology gap |
| `alt_code_elicitation_only_prompt` | 0.278 | Prompting-only alternative not fully falsified due to missing prior |

---

## Key Findings and Recommendations

1. **Thirteen named claims have uninformative 0.5 belief** due to missing priors in `priors.py`. The most critical are `claim_compound_reward_no_python` (the key causal intervention) and `claim_random_gamma_robustness` (a core prediction of the pretraining hypothesis). Adding priors for these would increase coverage from ~35/60 to all named claims.

2. **The contradiction operator does not reach `alt_rlvr_teaches_new`.** The claim `claim_rlvr_teaches` is contradicted and crushed to 0.00067, but the logically equivalent `alt_rlvr_teaches_new` sits at 0.412. Connecting the contradiction directly to `alt_rlvr_teaches_new` would eliminate this inconsistency.

3. **`pred_teaches` at 0.9947 alongside `claim_rlvr_teaches` at 0.00067** is the most semantically confusing output. These nodes should be connected via a `deduction` edge so that suppressing the hypothesis also suppresses its predictions.

4. **The distribution-shift / memorization confound for MATH-500 is not modeled.** Given that Qwen2.5-Math models likely saw MATH-500-style problems in pretraining, this is the most significant unaddressed competing explanation for the core empirical finding.

5. **The overall argument is strong**: the pretraining-surfacing hypothesis reaches 0.9999968 belief, supported by independent evidence streams from three model families, AIME out-of-distribution analysis, code-frequency decomposition, and formal clipping-bias derivation. The core conclusions about Qwen-centric RLVR evaluation risks (`claim_qwen_centric_risk` = 0.859, `claim_implication_no_generalization` = 0.833) are well-supported but carry the most residual uncertainty, warranting the "high" rather than "very high" tier.
