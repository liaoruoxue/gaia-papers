# Critical Analysis: From Procedural Skills to Strategy Genes

## 1. Package Statistics

| Category | Count |
|----------|-------|
| Total knowledge nodes | 96 |
| Settings | 6 |
| Questions | 1 |
| Claims | 89 |
| Strategies | 22 |
| Operators | 0 |
| Independent leaf claims (with priors) | 31 |
| Derived conclusions (BP propagated) | 20 |
| Background-only nodes | 2 |

**Strategy type distribution:**

| Type | Count | % |
|------|-------|---|
| `support` | 19 | 86% |
| `abduction` | 1 | 5% |
| `induction` | 1 | 5% |
| `compare` | 1 | 5% |

**Inference method:** Junction Tree (exact inference, treewidth 4, 14ms)

**BP result summary (selected exported claims):**

| Claim | Belief | Tier |
|-------|--------|------|
| `thesis_form_over_content` | 0.858 | High |
| `thesis_gene_superior` | 0.897 | Very High |
| `thesis_skill_misaligned` | 0.897 | Very High |
| `strategy_layer_critical` | 0.849 | High |
| `gene_sensitive_to_content_not_structure` | 0.802 | High |
| `structure_independent_value` | 0.879 | Very High |
| `failure_distillation_principle` | 0.828 | High |
| `gene_best_failure_carrier` | 0.861 | High |
| `law_gene_evolution_improves` | 0.742 | Moderate |
| `gene_enables_accumulation` | 0.853 | High |
| `gene_evolution_persistent_improvement` | 0.898 | Very High |
| `alt_attention_bias` | 0.502 | Unresolved |

---

## 2. Summary

The paper argues that representational form -- not content volume -- is the primary determinant of reusable experience effectiveness for test-time LLM control. The argument proceeds through three analytical probes using 4,590 controlled trials across 45 scientific code-solving scenarios.

The knowledge graph reflects a reasonably well-structured empirical argument: leaf claims are direct experimental measurements (prior 0.90-0.93), and derived conclusions propagate from them through support strategies. The BP propagation lifts the core thesis (thesis_form_over_content) to 0.858, reflecting that the experimental evidence is substantial but the generalizability remains domain-specific. The evolution probe's law_gene_evolution_improves reaches 0.742 -- appropriate for an induction over just two data points. The most mechanistically interesting finding (strategy_layer_critical at 0.849) rests on a clear three-condition diagnostic and is well supported.

The argument structure is generally clean but has two notable weaknesses: (1) the scope of generalizability is bounded to scientific code-solving tasks, which the authors acknowledge; and (2) the mechanism for why compact structured representations work is underdetermined -- the abduction between execution-mode cuing and attention-bias hypotheses reaches near-equipoise, meaning the paper shows the effect without explaining the cause.

---

## 3. Weak Points

| Claim | Belief | Issue |
|-------|--------|-------|
| `law_gene_evolution_improves` | 0.742 | Only two data points (Feb and Mar 2026 CritPt runs); generalization is modest. |
| `gene_reuse_scope_bounded` | 0.817 | Multi-gene failure may be task-specific; no explanation for why two complementary genes perform worst (44.9%). |
| `documentation_dilution` | 0.853 | Dilution effect size varies by documentation type (API notes: -2.5pp, examples: -2.0pp); no single mechanism explains both. |
| `aggregation_harmful` | 0.795 | Claim that harmful sections "dominate" useful ones is inferred, not directly measured; no ablation isolating the interaction. |
| `signal_sparse` | 0.770 | "Sparse" is a qualitative characterization of Figure 3; the exact proportion of useful signal is unmeasured. |
| `pred_gene_structure_helps` | 0.979 | Boosted by abduction but the mechanism remains unverified -- no direct test of "execution mode cuing" as a hypothesis. |
| `alt_attention_bias` | 0.502 | Neither confirmed nor rejected; represents an unresolved mechanistic alternative. |

---

## 4. Evidence Gaps

### 4a. Missing experimental validations

| Gap | What would close it |
|-----|---------------------|
| No causal mechanism test for structure | An ablation holding content identical but modifying formatting (bullet list vs numbered steps vs prose) would isolate structure as causal. |
| No multi-domain generalization test | Results confined to scientific code-solving; no evaluation on narrative tasks or creative writing where documentation value may differ. |
| No multi-model test beyond Gemini | Both models are from the same provider; whether findings hold for GPT, Claude, or Llama is unknown. |
| No ablation of individual gene components beyond (m), (m+u), (m+u+pi) | The effect of alpha, c, v individually is not tested. |

### 4b. Untested conditions

| Condition | Why it matters |
|-----------|---------------|
| Multi-gene fusion (merging rather than concatenating) | All multi-gene tests use concatenation; intelligent fusion may preserve single-gene effectiveness. |
| Cross-domain gene transfer | Whether a gene trained on spectroscopy transfers to robotics is untested. |

### 4c. Competing explanations not resolved

| Alternative | Status | Discriminating evidence needed |
|-------------|--------|-------------------------------|
| Attention-bias hypothesis | Belief 0.502 -- unresolved | Test with semantically empty but structurally valid genes. |
| Token-budget hypothesis | Not formally modeled | Test with multiple token budget points for skill fragments. |

---

## 5. Contradictions

### 5a. Formal contradictions modeled

None in the final graph. An earlier candidate contradiction between obs_skill_passrate and obs_gene_passrate was removed because both are true simultaneously as numerical measurements; the opposing performance-direction effects are captured through support strategies.

### 5b. Internal tensions in the source

| Tension | Description |
|---------|-------------|
| Two-conflicting-genes result (53.2%) nearly matches single gene (54.0%) | Counterintuitive: conflicting signals do not compound harm. Paper does not explain this. |
| Overconstrained gene (55.9%) outperforms original gene (54.0%) | Structural over-specification improves performance -- suggests original gene may be underspecified. |
| Failure warnings only (54.4%) outperforms strategy-only (52.3%) | AVOID cues alone are more effective than strategic steps alone, but the paper frames gene evolution as primarily strategy-based. |

---

## 6. Confidence Assessment

### Very High (belief >= 0.88)

- **thesis_gene_superior** (0.897): Strategy gene format (+3.0pp) outperforms skill (-1.1pp) on the benchmark. Strong direct evidence.
- **thesis_skill_misaligned** (0.897): Skill packages degrade performance on this benchmark. Direct measurement.
- **structure_independent_value** (0.879): Structure contributes beyond content; clean controlled comparison.
- **gene_best_failure_carrier** (0.861): Among tested formats, gene best hosts failure history.
- **gene_evolution_persistent_improvement** (0.898): ~9.4-9.5pp improvement across two independent CritPt evaluations.

### High (belief 0.80-0.88)

- **thesis_form_over_content** (0.858): Central thesis; well-supported by convergent three-probe evidence.
- **strategy_layer_critical** (0.849): The pi component drives gene effectiveness; three-condition diagnostic.
- **gene_enables_accumulation** (0.853): Demonstrated by 210-gene library in Mar 2026 evolver.
- **failure_distillation_principle** (0.828): Compact AVOID warnings outperform combined strategy-failure bundles.
- **gene_sensitive_to_content_not_structure** (0.802): Content corruption falls below baseline; structural perturbation stays above.

### Moderate (belief 0.70-0.80)

- **law_gene_evolution_improves** (0.742): Consistent ~9-10pp improvement inferred from two data points; limited inductive base.
- **signal_sparse** (0.770): Qualitative characterization of Figure 3 decomposition; no quantitative signal density measure.
- **overall_four_findings** (0.773): Summary claim depends on four sub-findings with varying evidence quality.

### Tentative (belief 0.50-0.70)

- **aggregation_harmful** (0.795 observed, but mechanism is tentative): Causal explanation inferred, not measured.
- **alt_attention_bias** (0.502): Unresolved alternative -- neither confirmed nor rejected by current experimental design.

---

*Generated by the Gaia formalization pipeline. Source: arXiv:2604.15097.*
