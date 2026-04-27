# Critical Analysis — *Internalizing Agency from Reflective Experience* (LEAFE)

Source: `artifacts/2603.16843.pdf` (Ge et al., 2026, arXiv:2603.16843).

## 1. Package statistics

| Metric | Count |
|---|---|
| Settings | 11 |
| Questions | 1 |
| Claims | 54 |
| Strategies | 20 |
| Operators | 0 |
| Independent (leaf) claims | 9 |
| Derived claims (BP-propagated) | 17 |
| Orphaned named claims (no incoming/outgoing strategies) | 5 |
| Compiler-generated structural artifacts (orphaned) | 23 |

**Strategy type distribution** (20 strategies total):

| Type | Count | Notes |
|---|---|---|
| `support` | 16 | Default for empirical-claim → conclusion warrant |
| `induction` | 2 | LEAFE > GRPO (across two observation tables); LEAFE > four baselines (across main + synergy tables) |
| `abduction` | 1 | Internalization H vs. "LEAFE is just better sharpening" Alt against the Lcf ablation |
| `compare` | 1 | The abduction's compare component |

**Modules** (5):

- `motivation.py` — Pass@K, RLVR, distribution sharpening vs. agency internalization
- `s3_method.py` — Tree-Based Experience Generation with Rollback (Stage 1) and Experience Distillation (Stage 2)
- `s4_experiments.py` — Tables 1–6 transcribed; main empirical conclusions with induction + abduction
- `s6_conclusion.py` — Synthesis and burden-shift claim
- `priors.py` — 16 priors (9 leaves + 7 derived-observation anchors per the project convention)

**Figure / table references** — every empirical observation claim carries `metadata={"source_table": "artifacts/2603.16843.pdf, Table N"}` traceability for Tables 1–6.

**BP result summary**

- All exported headline conclusions land in **0.74–0.92**.
- The internalization abduction cleanly separates: H (`claim_internalization_supported`) = 0.92 vs. Alt (`alt_leafe_just_sharpening`) = 0.28.
- All directly-measured observation tables (Tables 1–6) pin between 0.92 and 0.99.
- The two strongest single beliefs are `obs_main_results` (0.996) and `pred_internalization` (0.99) — the second is pulled up by abduction's coupling between H and the experimental-evidence prediction.

## 2. Summary

LEAFE proposes a two-stage recipe — **(1) tree-based, experience-guided rollback branching during exploration**, then **(2) supervised distillation of post-rollback corrected actions back into the policy** — to remedy a specific failure mode of outcome-driven RL with verifiable rewards (RLVR / GRPO): the policy gets sharper (higher Pass@1) without expanding its capability ceiling (Pass@K, large K). The argument structure is clean. A motivation pass establishes that environments emit rich diagnostic feedback that RLVR underuses; a method pass derives why a counterfactual loss on $(h_\tau, a'_\tau)$ pairs internalizes the corrective context-intervention; and an experimental pass marshals five observation tables (Tables 1–6) plus an OOD generalization experiment to validate three exported conclusions: LEAFE consistently beats GRPO at Pass@128, LEAFE beats all four baselines at Pass@128, and the Lcf-vs-Lreh ablation pattern is uniquely consistent with the internalization framing (not with "LEAFE is just a better sharpening recipe"). The abduction on the Lcf ablation is the package's strongest argument — the asymmetric Pass@1 / Pass@128 response to removing Lcf (≤ 0.7 points vs. 2–4.7 points) is a textbook abductive signature that the alternative cannot match. The principal weak link is the headline `claim_leafe_beats_grpo_passk` (BP belief 0.77), which inherits sub-0.95 priors from its observation anchors and its dependence on a wide-but-noisy table where ALFWorld and ScienceWorld show only ~2-point Pass@128 wins for LEAFE. The package as a whole supports the internalization thesis with high confidence on CodeContests / Sokoban and moderate confidence on the smaller-margin interactive benchmarks.

## 3. Weak points

| Claim | Belief | Issue |
|---|---|---|
| `claim_leafe_beats_grpo_passk` | 0.77 | Headline empirical claim. Belief is suppressed by the joint contribution of (a) the eight Pass@128 cells in Table 1 having only ~2-point margins on ALFWorld and ScienceWorld; (b) the induction's two observation anchors are at 0.92–0.95 (not 0.99); (c) GRPO sometimes wins Pass@1, which complicates a strict "LEAFE > GRPO" reading. |
| `claim_leafe_beats_alternatives` | 0.74 | Stronger across the four-baseline comparison than LEAFE-vs-GRPO alone, but suppressed by `obs_synergy_ablation`'s lower anchor prior (0.90) and by the fact that on individual cells (e.g. ALFWorld / Qwen2.5-7B Pass@1) some baselines beat LEAFE. |
| `claim_leafe_practical` | 0.77 | Synthesis of three derived claims, each itself a bit below 1.0; multiplicative depth softens the conclusion. |
| `claim_pass_burden_shift` | 0.82 | Long but reasonable derivation chain (Lcf design → internalization → burden shift). |
| `claim_cf_internalizes_recovery` | 0.81 | Sits two strategies deep into the method module; depends on `claim_branching_targets_failures` (0.84) and `claim_experience_as_intervention` (0.85). Could be lifted by an explicit cross-link to the `obs_lcf_ablation` evidence in s4. |
| `alt_leafe_just_sharpening` | 0.28 | Healthy: clearly defeated. Worth flagging that this alternative is simple — a stronger competing explanation (e.g. "LEAFE is doing implicit DPO over rollback-branch preference data") was not formalized and would deserve its own abduction in a follow-up review. |

No exported claim is below 0.5; no contradiction is in conflict.

## 4. Evidence gaps

### 4a. Missing experimental validations

| Gap | What is missing | What would resolve it |
|---|---|---|
| LEAFE on weak-feedback environments | All five benchmarks (WebShop, ALFWorld, ScienceWorld, Sokoban, CodeContests) emit rich diagnostic feedback; the limitation `claim_lim_feedback_quality` is acknowledged but not measured. | A benchmark with sparse / noisy feedback (e.g. real web tasks without compiler errors) to probe where LEAFE's advantage decays. |
| LEAFE on non-resettable environments | The `Step(·)` rollback assumption (`claim_lim_resettable_env`) is a load-bearing structural premise but the paper does not report a degradation curve as the rollback-fidelity assumption is relaxed. | Stochastic-environment variant with imperfect replay; report Pass@128 sensitivity. |
| Stage-1 alone vs. Stage-2 alone | Table 4 ablates Lreh vs. Lreh+Lcf within Stage 2, but does not isolate Stage 1's contribution against a model that only sees rejection-sampled successes from independent-sampling rollouts. | Run "rejection-sampling + Lreh + Lcf, where Stage-1 branching is replaced by independent sampling" to attribute the observed Pass@128 gain to branching specifically. |
| Pass@K beyond 128 | All headline numbers use Pass@128. Figure 3 plots up to k=1024 on CodeContests but no table shows cross-method numbers at k=512 or 1024. | Tabulated Pass@1024 for at least CodeContests and ScienceWorld. |

### 4b. Untested conditions

| Condition | Why it matters | Currently |
|---|---|---|
| Other base RL recipes (PPO, REINFORCE++, GiGPO, GA-Rollback) as initialization | LEAFE's improvements may be specific to GRPO sharpening signatures. | Only GRPO-initialized LEAFE is reported in the main tables. Comparison to GA-Rollback — the closest related work — appears only in the Related Work prose. |
| Smaller backbones (1B–3B) | Capability-ceiling expansion may saturate or invert at small scale. | Smallest backbone evaluated is Qwen2.5-7B / Llama3.1-8B. |
| Multi-task transfer | Does LEAFE training on benchmark A help benchmark B? | OOD MBPP (Table 5) is a code → code transfer; cross-domain transfer (e.g. CodeContests → WebShop) is not reported. |

### 4c. Competing explanations not fully resolved

| Alternative | Why it is plausible | Evidence that would distinguish |
|---|---|---|
| LEAFE ≈ implicit preference learning over rollback branches | Stage 2's Lcf objective resembles a single-positive DPO with the original action as implicit negative. | Compare LEAFE against an explicit DPO baseline trained on $(h_\tau, a_\tau, a'_\tau)$ triplets. |
| LEAFE benefits primarily from broader trajectory data (more positive rollouts) rather than from corrective-context internalization | Stage 1 branching produces *additional* successful trajectories that feed Lreh. Some Pass@128 gain could be data-volume effect. | Match Lreh data volume between LEAFE and a baseline that synthesizes the same number of successes via independent re-sampling. |
| Test-time reflection is doing the real work | LEAFE's Stage-1 reflection turn could be reproducing the standard Reflexion gain at test time. | The paper reports that Pass@128 numbers are computed without Stage-1 rollback at inference (§4 paragraph 5). This is stated but not directly cross-verified with a "LEAFE-trained model + Reflexion-at-test-time" row. |

## 5. Contradictions

### 5a. Explicit contradictions modelled with `contradiction()`

**None retained.** Two candidate contradictions were drafted and removed during Pass 5 verification:

| Pair considered | Reason for removal |
|---|---|
| `claim_distribution_sharpening` ⊥ `claim_agency_internalization` | These are characterisations of training *outcomes* under different recipes, not mutually exclusive properties of a single trained policy. A policy could partly sharpen and partly internalize. Modelling them as `contradiction()` artificially suppressed both via BP. |
| `claim_distribution_sharpening` ⊥ `claim_leafe_beats_grpo_passk` | These are not contradictory: distribution sharpening is precisely what *predicts* GRPO's Pass@128 plateau, which is what *makes room* for LEAFE to beat GRPO. They are mutually supportive, not exclusive. |

The package therefore ships with **0 hard `contradiction()` operators**, by deliberate Pass 5 audit — not by oversight.

### 5b. Internal tensions worth flagging (informal contradictions)

| Tension | Where in the paper | Status |
|---|---|---|
| GRPO sometimes wins Pass@1 (e.g. WebShop / Qwen2.5-7B 67.45 vs. LEAFE 66.50; CodeContests / Qwen2.5-72B 20.45 vs. 17.12) yet LEAFE consistently wins Pass@128. | Table 1 / Table 2 | Not contradictory but in tension with a clean "LEAFE > GRPO" narrative; flagged via `obs_grpo_passk_pattern`. |
| `obs_synergy_ablation` (Table 6) shows LEAFE-alone Pass@1 numbers (e.g. CodeContests / Qwen2.5-32B = 9.34) that look incompatible with Table 2's headline LEAFE+GRPO Pass@1 numbers — Table 6 appears to compare a different LEAFE-alone configuration. | Tables 2 and 6 | The paper does not explicitly reconcile these. The `obs_synergy_ablation` prior was lowered to 0.90 to reflect this interpretive ambiguity. |
| §4.5 acknowledges that EarlyExp and GRPO can *constrain* the exploration ceiling (Pass@128 drops in some Table 6 cells) but the paper still recommends initializing LEAFE from GRPO. | §4.5 vs. §4 (Implementation Details) | A two-stage stack that (i) deliberately narrows exploration with GRPO and then (ii) re-broadens with LEAFE may be net positive but is rhetorically in tension. |
| `claim_lim_feedback_quality` says LEAFE benefits diminish without diagnostic feedback, yet WebShop's feedback (search hits, attribute mismatches) is arguably the weakest of the five benchmarks and LEAFE still wins Pass@128 there. | §4.5 vs. Table 1 (WebShop column) | Not formally modelled; suggests the limitation is more graceful than the prose implies. |

## 6. Confidence assessment of exported conclusions

| Tier | Belief range | Exported claims |
|---|---|---|
| **Very high** (>= 0.90) | belief >= 0.90 | `claim_internalization_supported` (0.92), `claim_stage1_branching_better` (0.92), `claim_lreh_stabilizes` (0.92, leaf), `claim_aux_pass1_pass128_tradeoff` (0.94), `claim_lim_resettable_env` (0.90, leaf) |
| **High** (0.80-0.89) | 0.80 <= belief < 0.90 | `claim_grpo_sharpens_evidence` (0.86), `claim_distribution_sharpening` (0.86), `claim_branching_targets_failures` (0.84), `claim_cf_internalizes_recovery` (0.81), `claim_pass_burden_shift` (0.82), `claim_test_time_cost` (0.84), `claim_lim_feedback_quality` (0.85, leaf), `claim_rlvr_underuses_feedback` (0.85, leaf) |
| **Moderate** (0.65-0.79) | 0.65 <= belief < 0.80 | `claim_leafe_beats_grpo_passk` (0.77), `claim_leafe_practical` (0.77), `claim_leafe_beats_alternatives` (0.74), `claim_agency_internalization` (0.70, leaf — limited by definitional contestability) |
| **Tentative** (< 0.65) | belief < 0.65 | (none of the exported conclusions) |

The package's core thesis lands in the **high-to-very-high** tier; the headline empirical comparison claims sit in the **moderate** tier because they are constrained by the empirical reality of mixed Pass@1 / Pass@128 outcomes across benchmarks rather than by any structural weakness in the formalization.
