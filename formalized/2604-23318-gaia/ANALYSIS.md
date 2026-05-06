# Critical Analysis -- Chen et al. (2026), "Hidden States Know Where Reasoning Diverges: Credit Assignment via Span-Level Wasserstein Distance"

This analysis is the analytical payoff of the Gaia formalization. By
building the knowledge graph for the SHEAR paper [@Chen2026SHEAR],
we now understand the argument's structure well enough to identify
its strengths and weaknesses. References below are to claim labels
in the package.

## 1. Package Statistics

| Stat | Value |
|------|------:|
| Knowledge nodes | 166 |
| Settings | 24 |
| Questions | 1 |
| Claims | 141 |
| Independent (leaf) claims with priors | 26 |
| Derived claims (BP-propagated) | 43 |
| Strategies | 58 |
| Operators | 2 (`contradiction` x 2) |
| Modules | 11 (motivation + s2-s9 + s10_wiring + priors) |
| BP iterations to convergence | 2 (Junction Tree, exact, 18 ms, treewidth 5) |

Strategy type distribution:

- `support`: heavy on per-(backbone, modality) result reads,
  algorithm-step descriptions, related-work characterisations,
  ablation-table reads.
- `induction`: 2 chains:
  - **Cross-(backbone, modality) generalization** of `SHEAR > GRPO`
    over Qwen2.5-Math-7B + Llama3.1-8B-Instruct + Qwen2.5-14B-Base +
    code panel (3 induction chains, 4 sub-supports).
  - **Distribution-aware metrics outperform mean-only** over $W_1$,
    Chamfer, MMD vs. Cosine (2 induction chains, 4 sub-supports).
- `deduction`: 4 (Theorem 1 strict separation; Theorem 2 group-level;
  Proposition F.1 symmetric correct rollouts; Proposition D.1 mean-
  shift bound; advantage direction preserved).
- `abduction`: 1 -- **hidden-state-faithful** vs. **any-reweighting-
  suffices** discriminated by the Section 5.4.1 distance-metric
  ablation (cosine actively underperforms GRPO).
- `compare`: 1 (sub-strategy of the abduction).
- `contradiction`: 2 -- (a) prevailing assumption *fine-grained
  credit assignment in RLVR requires per-step annotation* vs. SHEAR's
  outcome-only-label demonstration (`contra_no_annotation_required`);
  (b) GRPO's implicit *all tokens deserve equal advantage* assumption
  vs. the within-trajectory empirical divergence finding
  (`contra_uniform_vs_divergence`).

## 2. BP Belief Summary -- Top-5 Named Claims

| Belief | Claim | Notes |
|------:|---|---|
| 0.9992 | `claim_table1_qwen_math_7b` | Direct table readout, prior 0.94, lifted by downstream propagation |
| 0.9992 | `contra_uniform_vs_divergence` | Contradiction operator drives foil to 0.083 |
| 0.9991 | `contra_no_annotation_required` | Foil collapses to 0.034 |
| 0.9990 | `claim_table1_llama_8b` | Direct table readout |
| 0.9990 | `claim_table1_qwen_14b` | Direct table readout |

Both **contradiction operators** function as designed. The empirically-
strongest nodes are the per-backbone main-result tables (0.999), whose
directly-read priors are amplified through the universal-law induction.

The **central abduction** lifts `claim_signal_explains_via_hidden_states`
from prior 0.7 to belief 0.817 -- the discriminating evidence (cosine
underperforms GRPO, distribution-aware metrics succeed) provides modest
but non-trivial uplift; the alternative `claim_signal_alt_any_reweighting`
rises only marginally from prior 0.2 to 0.231.

## 3. Summary of Central Thesis

SHEAR's central thesis is that **hidden-state distributional divergence
between correct and incorrect rollouts in a GRPO group is a viable,
self-supervised process-level credit signal for RLVR**, requiring only
the outcome-level binary correctness labels already produced by the
verifiable reward (`claim_self_supervised_signal_proposal`). The paper
defends this thesis in three coordinated layers:

1. **Empirical existence proof** (Section 2 / Figure 1):
   `claim_aggregate_and_local_complementary` -- *both* aggregate
   (Spearman -0.96) and within-trajectory local (Spearman -0.42, p =
   4.6e-59) anti-correlations between Wasserstein distance and
   continuation success, the within-trajectory analysis controlling
   for the length-only confound.
2. **Theoretical justification** (Section 4 + Appendices C-G): under
   bounded-support, single-divergence-point, and finite-sample-
   concentration assumptions, post-divergence spans have *strictly
   larger* expected Wasserstein distance than pre-divergence spans
   whenever $D(S) > 2\eta(n,d)$ -- Theorem 1
   (`claim_thm1_strict_separation`); the result extends to the group-
   level minimum used in Algorithm 1 (Theorem 2).
3. **Method + empirical validation**: SHEAR = four-step Algorithm 1;
   the resulting weighted advantage $\tilde A^{(i)}_t = A^{(i)} \cdot
   \omega^{(i)}_t$ improves over GRPO on every (backbone, modality)
   pair tested (3 math + 3 code = 6 settings,
   `claim_shear_beats_grpo_universal`, BP belief 0.995) and beats both
   Entropy-adv. and PRM-based baselines on all three math backbones.

The closing argument couples the Section 5.4.1 *distance-metric
ablation* with Proposition D.1: **cosine actively underperforms GRPO**
-- the only metric that drops distributional shape information beyond
mean shift -- which directly verifies KR-duality's prediction that
mean-shift-only is insufficient.

## 4. Weak Points

### W1. Theorem assumption (A1) is empirically slippery

Assumption A1 (`setup_a1_divergence_structure`) posits a *single*
divergence point $\tau$. Real reasoning chains -- especially those
with self-correction -- have multiple divergence regimes. Proposition
G.1 (`claim_prop_g1_multiple_divergences`, prior 0.88) addresses this
*informally* in Appendix G but is not formally proved. The strict-
separation guarantee in Theorem 1.iii applies cleanly only to the
single-divergence case.

### W2. Verification of $D(S) > 2\eta(n, d)$ is indirect

The strict-separation condition requires the population gap $D(S)$
to exceed twice the finite-sample noise floor. The paper *never
estimates* $\tilde C_d$ or $M$ directly and instead substitutes the
qualitative empirical observation that Section 5.1's AUC rises
monotonically (`claim_thm1_condition_verified`, derived belief 0.93).
This is a reasonable correspondence argument but the theorem is *not
directly verified* -- only the qualitative consequence is.

### W3. Code gains are small and not multi-seed

`claim_table2_code_results` reports **single-run** numbers for code
(no error bars), while math results are 3-seed mean +/- std. The
code improvement margins are 0.6-1.1 average points; without
seed-level variance, reading these as statistically distinguishable
from GRPO is a stretch.

### W4. PRM mismatch interpretation is partly post-hoc

On Qwen2.5-14B-Base, both PRM variants fall *4-8 points below*
vanilla GRPO. The paper attributes this to *PRM-policy distribution
mismatch*. But this same observation could also be read as: 7B PRMs
may simply be undertrained for 14B policies. The paper does not run
the 14B-PRM control.

### W5. Hidden-state layer choice is not ablated

The paper specifies `h^{(i)}_t` is the hidden state at the *last
transformer layer before LM-head*. No layer-choice ablation is
reported. A finding that *only* the LM-head-adjacent layer works
would weaken the general "hidden states encode local quality" claim.

### W6. Cosine baseline is a weakened straw cousin of MeanShift

The Section 5.4.1 ablation includes **Cosine between span means** as
the mean-only baseline. Euclidean distance between span means would
be a more natural mean-shift baseline; the abduction's evidential
strength rests on this single Cosine variant.

## 5. Evidence Gaps

### G1. No direct test of the divergence-point assumption

The empirical analyses verify the *consequence* of the divergence-
point model -- that hidden-state divergence tracks reasoning quality.
Neither establishes nor rejects the *premise* that there exists a
sharp position $\tau$ after which incorrect rollouts have distinct
marginal distributions.

### G2. No ablation on $\bar n$ normalization choice

`claim_step2_global_norm_norm` describes the global mean-norm
normalization. Section 5.4.2 ablates *cross-rollout vs. per-rollout*
magnitudes but does not ablate *the use of $\|h\|_2$ at all* (e.g.
unit-normalizing each $h_t$, or no norm normalization).

### G3. Model-scale generalization to large reasoning models

The paper evaluates 7-14B models. Frontier reasoning models (R1-style
70B+ thinking models) may exhibit different hidden-state geometry.
Whether SHEAR generalises to these regimes is open.

### G4. No head-to-head empirical comparison with latent-space methods

Section 7 positions SHEAR within the latent-space methods family
([@Kang2026Ladir; @Du2026LTO; @Yue2025HybridLatent]) but does not
contend with them empirically.

### G5. Reward-hacking and over-confident-token failure modes

PRM(PURE) was specifically designed to mitigate *reward hacking*.
SHEAR's amplification structure could in principle *amplify* reward-
hacking trajectories where high-discrepancy tokens correspond to
verbose-confident patterns. The paper documents no failure modes.

### G6. The within-vs-cross-rollout decomposition is coarse

`claim_5_4_2_within_rollout_dominates` shows the per-rollout variant
still beats GRPO by ~1.1 points; default cross-rollout is +1.8. The
paper interprets this as "rollouts with larger absolute gaps merit
larger gradient mass" but does not test the underlying assumption.

---

The weak points and evidence gaps are *not* fatal -- the paper's
central thesis is well-supported by the combination of theory +
cross-(backbone, modality) empirics + distance-metric ablation. The
contradictions wired in this formalization both resolve in the paper's
favour under BP. The headline contribution (BP 0.89) and pure-bottom-
line summary (BP 0.93) are both robustly above 0.85. The limitations
primarily affect the *theoretical-rigor* limb -- the empirical limb
(SHEAR > GRPO universally) is solidly grounded.
