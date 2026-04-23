"""Section 4: Results and Analysis — Base Capability, Novelty, Breakthroughs, Geometry"""

from gaia.lang import (
    claim, setting,
    support, deduction, abduction, induction,
    compare, contradiction, complement,
    infer,
)
from .motivation import (
    optimization_gap_exists,
    novelty_not_sufficient_hypothesis,
    llm_as_search_operators,
    llm_mutation_differs,
    exploration_exploitation_classical,
    study_scope,
)
from .s3_methodology import (
    evo_loop_design,
    shared_initial_population,
    four_task_families,
    novelty_definition,
    evolution_scale,
    zeroshot_definition,
    spatial_entropy_definition,
    controlled_comparison,
)

# ══════════════════════════════════════════════════════════════════════════════
# 4.1  Base Model Capability
# ══════════════════════════════════════════════════════════════════════════════

zeroshot_correlates_with_final = claim(
    "Zero-shot performance is strongly positively correlated with post-optimization "
    "performance when aggregated across tasks (Figure 3, linear fit r=0.860, "
    "p=3.95e-05). Similar trends are observed at the sub-task level for 6 of 8 "
    "tasks; equation discovery tasks are the exception where the correlation is "
    "weaker. This confirms that base capability is a significant predictor of "
    "optimization potential.",
    title="Zero-shot performance correlates with final optimization outcome",
    metadata={"figure": "artifacts/2604.19440.pdf, Figure 3"},
)

zeroshot_insufficient = claim(
    "Zero-shot performance alone is insufficient to fully explain long-horizon "
    "optimization success. Models with nearly identical zero-shot performance can "
    "diverge substantially after evolution. For example, at a zero-shot score of "
    "approximately 0.4 (Figure 3), multiple models cluster tightly along the "
    "zero-shot axis yet spread widely in their best final performance. "
    "The OLS regression of final performance on zero-shot alone yields R²=0.103, "
    "explaining only ~10% of variance (Table 14, model M7).",
    title="Zero-shot capability is insufficient: residual variance is large",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 14 (M7), Figure 3"},
)

strat_zeroshot_to_final = support(
    [zeroshot_correlates_with_final, controlled_comparison, optimization_gap_exists],
    zeroshot_insufficient,
    reason=(
        "The correlation between @zeroshot_correlates_with_final and final performance "
        "is real but partial (R²=0.103). Under the controlled design "
        "(@controlled_comparison), initial conditions are equalized, so residual "
        "variance must reflect differences in search behavior rather than capability alone. "
        "The scatter around the regression line in Figure 3 is large enough to establish "
        "that zero-shot capability is necessary but not sufficient for good optimization."
    ),
    prior=0.92,
    background=[zeroshot_definition, evo_loop_design, shared_initial_population],
)

# ══════════════════════════════════════════════════════════════════════════════
# 4.2.1  Novelty vs. Breakthrough Dynamics
# ══════════════════════════════════════════════════════════════════════════════

novelty_not_significant = claim(
    "Novelty-based measures—including average novelty and initial novelty "
    "(first-generation diversity)—are not significant predictors of final "
    "optimization performance in OLS regression. "
    "OLS results (Table 13): avg_novelty coefficient β=−0.027 (SE=0.073, p=0.710, "
    "R²=0.001); initial_novelty β=−0.042 (SE=0.102, p=0.681, R²=0.002). "
    "Adding novelty to a model that already includes zero-shot performance "
    "adds essentially no explanatory power (novelty β=0.002, p=0.980 in M4). "
    "Novelty explanatory power is negligible: increasing diversity alone does "
    "not contribute to improved optimization performance.",
    title="Novelty does not predict optimization performance (OLS, Table 13)",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 13"},
)

breakthrough_definition = setting(
    "A breakthrough is defined as a best-so-far improvement event: an offspring "
    "generation in which the current solution exceeds the best fitness solution "
    "in all previous generations, i.e., f_child > f*_{t-1}. "
    "The breakthrough rate is the fraction of generations achieving a breakthrough, "
    "averaged per (model, task) pair.",
    title="Breakthrough: best-so-far improvement event; breakthrough rate definition",
)

breakthrough_rate_predicts = claim(
    "Breakthrough rate (fraction of generations achieving best-so-far improvement) "
    "is the strongest predictor of final optimization performance. "
    "OLS results (Table 14): breakthrough rate alone yields β=0.445 (SE=0.097, "
    "p<0.001, R²=0.198)—approximately two times the explanatory power of "
    "zero-shot capability alone (R²=0.103). In the joint model (M8: zero-shot + "
    "breakthrough rate), breakthrough rate remains highly significant "
    "(β=0.389, p<0.001, R²=0.246), while the zero-shot coefficient decreases "
    "from 0.322 to 0.226 (p=0.076, no longer significant). "
    "This indicates that part of zero-shot's predictive power is mediated through "
    "its ability to generate consistent improvements during search.",
    title="Breakthrough rate strongly predicts final performance (R²=0.198)",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 14"},
)

strat_novelty_vs_br_contradiction = contradiction(
    novelty_not_sufficient_hypothesis,
    novelty_not_significant,
    reason=(
        "The classical novelty-as-exploration hypothesis predicts that novelty should "
        "be a significant positive predictor of optimization success. The OLS result "
        "(@novelty_not_significant, β≈0, p>0.6) directly contradicts this: "
        "novelty coefficients are near zero and non-significant across all model "
        "specifications. These two propositions cannot both be true."
    ),
    prior=0.95,
)

breakthrough_mediates_capability = claim(
    "Part of the predictive power of zero-shot capability on final optimization "
    "performance is mediated through breakthrough rate: models with stronger base "
    "capability tend to generate more consistent improvements during search, "
    "which in turn drives better final fitness. This mediation is evidenced by the "
    "decrease in the zero-shot coefficient from 0.322 (standalone) to 0.226 "
    "(joint with breakthrough rate), with the zero-shot p-value rising from 0.016 "
    "to 0.076 (no longer significant at p<0.05).",
    title="Zero-shot capability partly mediates optimization success through LRR",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 14"},
)

strat_br_mediates = support(
    [breakthrough_rate_predicts, zeroshot_insufficient],
    breakthrough_mediates_capability,
    reason=(
        "Given that @zeroshot_insufficient shows that base capability alone cannot "
        "fully explain final performance variance (R²=0.103), and given that "
        "@breakthrough_rate_predicts shows breakthrough rate explains ~2× more "
        "variance (R²=0.198) and remains significant even controlling for zero-shot, "
        "the mediation pattern (zero-shot coefficient decreasing from 0.322 to 0.226 "
        "when breakthrough rate is added) implies that stronger base models partly "
        "succeed because they better generate incremental improvements during search."
    ),
    prior=0.85,
    background=[breakthrough_definition, evo_loop_design],
)

# ══════════════════════════════════════════════════════════════════════════════
# 4.2.2  Semantic Geometry
# ══════════════════════════════════════════════════════════════════════════════

strong_optimizers_localize = claim(
    "Effective LLM optimizers progressively localize their search in semantic space. "
    "Qualitative case study (Figure 5, TSP-60): Gemini-1.5-Pro forms a convergent "
    "solution cluster in the multidimensional scaling (MDS) projection, with spatial "
    "entropy H_spatial decreasing from ~4.45 at generation 0 to ~4.30 by generation 30. "
    "Mean best fitness increases monotonically from ~0.75 to ~0.95. "
    "Fitness spatial entropy H_fitness also decreases, indicating high-quality "
    "solutions concentrate into a tight semantic region.",
    title="Strong optimizers progressively localize search in semantic space",
    metadata={"figure": "artifacts/2604.19440.pdf, Figure 5"},
)

weak_optimizers_drift = claim(
    "Weak LLM optimizers exhibit large semantic drift: solutions continue to diffuse "
    "across distant regions of semantic space throughout all generations. "
    "Qualitative case study (Figure 5, TSP-60): Mistral-7B-Instruct maintains "
    "high spatial entropy H_spatial (~4.45-4.55, roughly flat across generations) "
    "and high fitness spatial entropy H_fitness (~4.30-4.50 flat), indicating "
    "sustained diffusion without convergence. Mean best fitness shows sporadic "
    "breakthroughs followed by stagnation, reaching only ~0.75 by generation 30 "
    "vs. Gemini-1.5-Pro's ~0.95.",
    title="Weak optimizers exhibit semantic drift without convergence",
    metadata={"figure": "artifacts/2604.19440.pdf, Figure 5"},
)

localization_vs_drift_complement = complement(
    strong_optimizers_localize,
    weak_optimizers_drift,
    reason=(
        "In the TSP-60 case study, Gemini-1.5-Pro and Mistral-7B-Instruct "
        "with nearly identical zero-shot performance exhibit diametrically opposite "
        "geometric search behaviors: one progressively localizes, the other "
        "persistently drifts. These two behavioral modes are exhaustive and "
        "mutually exclusive characterizations of the qualitative trajectory geometry."
    ),
    prior=0.80,
)

# ══════════════════════════════════════════════════════════════════════════════
# 4.2.3  Generation-Level Statistical Test (Mixed-Effects)
# ══════════════════════════════════════════════════════════════════════════════

fitness_entropy_negative = claim(
    "Higher fitness spatial entropy (H_fitness) is negatively associated with "
    "breakthrough probability. Mixed-effects regression (Table 15): H_fitness "
    "coefficient β=−0.073 (SE=0.026, p=0.005) in the concurrent model and "
    "β=−0.074 (SE=0.024, p=0.002) in the lagged model. Maintaining multiple "
    "dispersed high-quality regions hinders breakthrough production.",
    title="Higher fitness spatial entropy reduces breakthrough probability",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 15"},
)

novelty_positive_conditional = claim(
    "Mean novelty is positively associated with breakthrough probability within a "
    "generation, but only when the search is sufficiently localized. "
    "Mixed-effects regression (Table 15): mean_novelty concurrent β=0.070 "
    "(SE=0.026, p=0.006). However, the interaction term (novelty × H_spatial) "
    "is significantly negative: concurrent β=−0.090 (SE=0.010, p<0.001) and "
    "lagged β=−0.051 (SE=0.009, p<0.001). The lagged novelty main effect becomes "
    "non-significant (β=0.016, p=0.517), but the interaction remains strong "
    "(p<0.001), indicating the productivity of novelty depends on the geometric "
    "state of the population, not just contemporaneous correlations.",
    title="Novelty boosts breakthroughs only when search is spatially localized",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 15, Figure 12"},
)

generation_index_negative = claim(
    "Breakthrough probability decreases with generation index. "
    "Mixed-effects regression (Table 15): generation coefficient β=−0.250 "
    "(SE=0.018, p<0.001) concurrent and β=−0.193 (SE=0.017, p<0.001) lagged. "
    "Breakthroughs occur predominantly in early generations when there is still "
    "room for large improvements, and become rarer as the population converges.",
    title="Breakthrough probability decreases with generation index",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 15"},
)

novelty_conditional_on_localization = claim(
    "Novelty is conditionally useful: it increases breakthrough probability only "
    "when the search is sufficiently localized (low spatial entropy). "
    "Under high spatial dispersion, novelty is largely unproductive or even "
    "detrimental. Breakthrough events concentrate in regions of high novelty and "
    "low spatial entropy; high novelty under high dispersion correlates with low "
    "breakthrough probability (Figure 12 heatmap). "
    "This conditional benefit is robust across both concurrent and lagged analyses.",
    title="Novelty × localization interaction: novelty is productive only when localized",
    metadata={"figure": "artifacts/2604.19440.pdf, Figure 12"},
)

strat_gen_index_contributes = support(
    [generation_index_negative],
    novelty_conditional_on_localization,
    reason=(
        "The negative generation index effect (@generation_index_negative, β=−0.250) "
        "shows that breakthroughs concentrate in early generations when the population "
        "has not yet localized. This temporal structure reinforces the localization "
        "story: as generations progress, the population progressively converges "
        "(localization increases), which changes the regime in which novelty operates. "
        "The generation index thus provides indirect evidence for the localization–"
        "novelty interaction described in @novelty_conditional_on_localization."
    ),
    prior=0.80,
    background=[breakthrough_definition],
)

strat_novelty_conditional = support(
    [novelty_positive_conditional, fitness_entropy_negative],
    novelty_conditional_on_localization,
    reason=(
        "From the mixed-effects model: @novelty_positive_conditional establishes "
        "that mean novelty has a positive main effect (β=0.070, p=0.006) on "
        "breakthrough probability, but the novelty × H_spatial interaction "
        "(β=−0.090, p<0.001) is larger in magnitude, indicating that high spatial "
        "entropy cancels and reverses novelty's benefit. "
        "@fitness_entropy_negative confirms that dispersed high-fitness regions "
        "reduce breakthrough probability. Together: novelty is productive only within "
        "already-localized, high-performing regions—not as a general exploration strategy."
    ),
    prior=0.88,
    background=[spatial_entropy_definition, breakthrough_definition],
)

# ══════════════════════════════════════════════════════════════════════════════
# 4.3  Operator-Level Validation
# ══════════════════════════════════════════════════════════════════════════════

local_refiner_hypothesis = claim(
    "Effective LLM optimizers behave as local refiners: they frequently produce "
    "offspring that strictly improve upon their prompted parents while maintaining "
    "controlled semantic step sizes. This is characterized by two operator-level "
    "metrics: (1) Local Refinement Rate (LRR) = fraction of valid offspring that "
    "strictly improve upon their parent; (2) Parent–Child Distance (PCD) = average "
    "semantic distance between each offspring and its prompted parents.",
    title="Local refiner hypothesis: effective LLMs improve parents frequently with small steps",
)

strat_geometry_explains_local_refiner = support(
    [strong_optimizers_localize, weak_optimizers_drift],
    local_refiner_hypothesis,
    reason=(
        "The semantic geometry analysis provides a mechanistic explanation for "
        "the local refiner characterization: @strong_optimizers_localize shows that "
        "effective optimizer models converge their search to promising regions, "
        "enabling repeated incremental improvements—the geometric signature of "
        "local refinement. @weak_optimizers_drift shows that ineffective models "
        "scatter solutions across remote semantic regions without exploiting them, "
        "leading to sporadic gains followed by stagnation "
        "(the classical meta-heuristic pattern from @exploration_exploitation_classical). "
        "These two behaviors provide geometric validation of the local refiner hypothesis."
    ),
    prior=0.85,
    background=[spatial_entropy_definition, exploration_exploitation_classical],
)

lrr_predicts_strongly = claim(
    "Local Refinement Rate (LRR) is a strong positive predictor of final performance. "
    "Model-level OLS regression (Table 1): in the joint model (ZS + LRR + PCD), "
    "LRR coefficient β=0.528 (p<0.001), while PCD effect vanishes (β=−0.024, p=0.838) "
    "once LRR is included. R² increases from 0.204 (ZS + PCD) to 0.367 (ZS + LRR + PCD). "
    "The negative effect of PCD (β=−0.329, p=0.001) disappears when LRR is added, "
    "indicating that large semantic modifications are harmful primarily because they "
    "reduce refinement reliability, not because of step size per se.",
    title="LRR strongly predicts final performance; PCD effect mediated by LRR",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 1"},
)

pcd_negative_mediated = claim(
    "Parent–child semantic distance (PCD) alone is negatively correlated with "
    "final performance (β=−0.329, p=0.001 in ZS+PCD model, Table 1). "
    "However, this negative effect vanishes once local refinement rate (LRR) "
    "is included in the model, indicating that larger edits reduce performance "
    "primarily because they reduce the probability of producing refinements, "
    "not because of step size per se.",
    title="PCD's negative effect on performance is mediated by LRR",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 1"},
)

strat_lrr_mechanism = support(
    [lrr_predicts_strongly, pcd_negative_mediated],
    local_refiner_hypothesis,
    reason=(
        "The operator-level regression confirms the local refiner hypothesis: "
        "@lrr_predicts_strongly shows LRR has the largest coefficient (β=0.528, "
        "p<0.001) in the joint model, adding substantial explanatory power (R² from "
        "0.204 to 0.367). @pcd_negative_mediated shows that PCD's negative effect "
        "is fully explained by its negative impact on LRR—larger steps tend to produce "
        "fewer improvements. This validates the mechanistic story: what matters is not "
        "how far offspring deviate semantically, but whether they reliably improve "
        "upon their parents."
    ),
    prior=0.88,
    background=[evo_loop_design, four_task_families],
)

# ── Perturbation study (model mixing) ────────────────────────────────────────

model_mixing_design = setting(
    "The model mixing perturbation study injects a fraction α of offspring from "
    "a 'weak refiner' model into an otherwise strong-refiner evolutionary run. "
    "At each generation, α × 10 offspring are generated by the weaker model and "
    "(1−α) × 10 by the stronger model. Task-specific model pairs are chosen with "
    "comparable zero-shot performance but contrasting LRR: "
    "TSP-60 (Mistral-24B vs. Mistral-7B), Summarization (DeepSeek-V3 vs. GPT-4o-mini), "
    "Bin-Packing-OR3 (Mistral-24B vs. LLaMA-3.2-3B-Instruct).",
    title="Model mixing perturbation: inject weak-refiner offspring fraction",
)

model_mixing_degrades_performance = claim(
    "Increasing the fraction of weak-refiner offspring monotonically degrades "
    "optimization performance and reduces the overall refinement rate. "
    "On TSP-60 and bin packing-OR3, performance degrades sharply and monotonically "
    "as the proportion of weak-refiner offspring increases (Figure 7). "
    "The same effect exists but is weaker and less consistent in prompt optimization. "
    "Higher weak-offspring ratios consistently reduce the overall refinement rate, "
    "which co-varies with performance degradation.",
    title="Model mixing: injecting weak refiners degrades performance monotonically",
    metadata={"figure": "artifacts/2604.19440.pdf, Figure 7"},
)

strat_model_mixing_validates = support(
    [model_mixing_degrades_performance],
    local_refiner_hypothesis,
    reason=(
        "The perturbation study provides quasi-interventional evidence: by directly "
        "manipulating refinement behavior through model mixing, "
        "@model_mixing_degrades_performance shows that degrading refinement capability "
        "causes predictable drops in optimization performance. This rules out that the "
        "correlation between LRR and performance is spurious. The co-variation of "
        "refinement rate and performance across injection fractions traces the "
        "causal mechanism: LRR → sustained improvements → higher final fitness."
    ),
    prior=0.82,
    background=[model_mixing_design, evo_loop_design],
)

# ── Temperature robustness ──────────────────────────────────────────────────

temperature_robustness = claim(
    "The relationship between local refinement rate and final performance is robust "
    "to substantial variations in decoding temperature. Temperature sensitivity "
    "analysis on TSP and Oscillator tasks with Mistral-7B and Mistral-24B "
    "(T ∈ {0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3}): Pearson r between LRR and "
    "final performance = 0.76 (p=0.027) for Mistral-7B on TSP and 0.92 "
    "(p<0.001) for Mistral-24B on TSP. Oscillator correlations are positive but "
    "not significant (r=0.49, p=0.209 and r=0.32, p=0.433). "
    "Refinement behavior is a stable property of the combined system (model, prompt, "
    "decoding configuration), not tied to a narrow temperature regime.",
    title="LRR-performance relationship robust across temperature settings",
    metadata={"source_table": "artifacts/2604.19440.pdf, Table 11"},
)

# ══════════════════════════════════════════════════════════════════════════════
# 4.4  Cost-Efficiency
# ══════════════════════════════════════════════════════════════════════════════

cost_efficiency_frontier = claim(
    "Optimization performance is not fully determined by base model capability or "
    "cost. Some mid-sized models achieve large fitness improvements at relatively "
    "low cost. Mistral-24B-Instruct lies on the Pareto frontier of optimization "
    "gain vs. monetary cost, combining large fitness improvement with moderate cost "
    "(Figure 8). Larger/more expensive models (e.g., GPT-4o at much higher cost) "
    "do not always yield proportional gains per dollar. Cost-efficient optimization "
    "is achieved by selecting models with favorable refinement behavior rather than "
    "maximum zero-shot capability.",
    title="Cost-efficient optimization: mid-sized refiners on Pareto frontier",
    metadata={"figure": "artifacts/2604.19440.pdf, Figure 8, Figure 15"},
)

strat_cost_efficiency_from_lrr = support(
    [lrr_predicts_strongly],
    cost_efficiency_frontier,
    reason=(
        "Since @lrr_predicts_strongly establishes that LRR (not raw capability or cost) "
        "is the dominant predictor of final performance (β=0.528, R²=0.246 joint), "
        "models with high LRR and moderate cost can outperform more expensive models "
        "with lower LRR. The cost-efficiency data (Figure 8, Figure 15) shows "
        "Mistral-24B-Instruct on the Pareto frontier: large fitness improvement at "
        "moderate API cost, despite not being the most capable model by zero-shot standards. "
        "Its strong refinement behavior generates frequent incremental improvements efficiently."
    ),
    prior=0.82,
    background=[zeroshot_definition],
)

# ══════════════════════════════════════════════════════════════════════════════
# Main synthesis claim
# ══════════════════════════════════════════════════════════════════════════════

optimizable_ability_distinct = claim(
    "LLM optimization performance comprises two distinct abilities: (1) base "
    "zero-shot problem-solving capability, which correlates with but only partially "
    "explains optimization success; and (2) 'optimizable ability'—the capacity to "
    "function as an effective local refiner during evolutionary search, characterized "
    "by high local refinement rate (LRR), progressive localization in semantic space, "
    "and frequent incremental breakthroughs. These abilities are empirically "
    "dissociable: models with similar zero-shot scores can differ substantially in "
    "optimization trajectories and outcomes. Optimizable ability is not simply a "
    "property of base model strength—smaller or cheaper models can outperform larger "
    "ones when they exhibit more reliable refinement behavior.",
    title="Optimizable ability: a distinct dimension from base LLM capability",
)

strat_optimizable_ability_synthesis = support(
    [zeroshot_insufficient, lrr_predicts_strongly, strong_optimizers_localize,
     novelty_conditional_on_localization, model_mixing_degrades_performance],
    optimizable_ability_distinct,
    reason=(
        "Five converging lines of evidence establish optimizable ability as distinct: "
        "(1) @zeroshot_insufficient: zero-shot explains only ~10% of final performance "
        "variance; (2) @lrr_predicts_strongly: LRR explains ~20% alone and ~25% "
        "jointly with zero-shot—more than zero-shot alone; "
        "(3) @strong_optimizers_localize: geometric trajectory analysis shows the "
        "mechanism—progressive localization; "
        "(4) @novelty_conditional_on_localization: novelty benefits are contingent "
        "on already being in an exploitable regime; "
        "(5) @model_mixing_degrades_performance: direct manipulation of refinement "
        "causes predictable performance changes. Together, these support a causal "
        "story: LLMs that reliably improve upon parents (high LRR) progressively "
        "localize their search (low entropy), produce frequent breakthroughs, and "
        "achieve higher final fitness—independently of zero-shot capability."
    ),
    prior=0.88,
    background=[evo_loop_design, shared_initial_population, study_scope],
)
