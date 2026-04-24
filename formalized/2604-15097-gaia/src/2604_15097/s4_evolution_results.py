"""Section 4.4: Gene as Carrier for Test-Time Evolution — CritPt Benchmark Results"""

from gaia.lang import claim, setting, support, induction
from .motivation import setup_gene_def, setup_gep
from .s4_evolution_probe import failure_distillation_principle, gene_best_failure_carrier

# --- CritPt benchmark baselines ---

setup_critpt = setting(
    "CritPt is a benchmark for quantum chemistry and materials science code-solving tasks. "
    "Results are reported as accuracy (percentage of tasks solved correctly). "
    "Baselines use the best available Gemini model without evolution: "
    "Gemini 3 Pro (non-preview) for the Feb 2026 evaluation, and "
    "Gemini 3.1 Pro (non-preview) for the Mar 2026 evaluation.",
    title="CritPt benchmark context",
)

obs_critpt_baseline_feb = claim(
    "The CritPt benchmark baseline (Gemini 3 Pro without evolution guidance) achieves "
    "9.1% accuracy on the quantum chemistry and materials science tasks "
    "evaluated as of the 2026-02-16 Evolver run [@Wang2026].",
    title="CritPt Feb-2026 baseline: 9.1%",
    background=[setup_critpt],
)

obs_critpt_baseline_mar = claim(
    "The CritPt benchmark baseline (Gemini 3.1 Pro without evolution guidance) achieves "
    "17.7% accuracy on the quantum chemistry and materials science tasks "
    "evaluated as of the 2026-03-26 Evolver run. The improvement from 9.1% to 17.7% "
    "reflects the stronger underlying model [@Wang2026].",
    title="CritPt Mar-2026 baseline: 17.7%",
    background=[setup_critpt],
)

# --- Evolver results (independent empirical observations) ---

obs_evolver_feb = claim(
    "Evolver (Gene) 2026-02-16 achieves 18.57% accuracy on CritPt, compared to the "
    "9.1% baseline for the same evaluation period (Gemini 3 Pro), representing a "
    "+9.47 percentage point absolute improvement. This version focuses on the "
    "memory-grounded evolution phase, converting failures into structured repair procedures [@Wang2026].",
    title="Evolver (Gene) 2026-02-16: 18.57% accuracy (+9.47pp)",
    background=[setup_critpt, setup_gene_def],
)

obs_evolver_mar = claim(
    "Evolver (Gene) 2026-03-26 achieves 27.14% accuracy on CritPt, compared to the "
    "17.7% baseline for the same evaluation period (Gemini 3.1 Pro), representing a "
    "+9.44 percentage point absolute improvement. This version adds the "
    "exploration-augmented evolution phase, accumulating 210 gene slots across 36 unique IDs, "
    "including 148 arxiv-derived selections, 44 run_experience selections, and "
    "18 builtin_topic_prior selections. The most frequently activated gene is "
    "gene_topic_hamiltonian_inverse_design (25 selections) [@Wang2026].",
    title="Evolver (Gene) 2026-03-26: 27.14% accuracy (+9.44pp)",
    background=[setup_critpt, setup_gene_def, setup_gep],
)

# --- Memory-grounded vs exploration-augmented phases ---

obs_memory_grounded_phase = claim(
    "The memory-grounded evolution phase (Evolver 2026-02-16) converts run failures "
    "into structured repair procedures stored as genes. These repair-procedure genes "
    "encode specific AVOID cues (α component) derived from observed failure modes, "
    "allowing the system to avoid previously seen error patterns on subsequent runs [@Wang2026].",
    title="Memory-grounded phase: failure repair procedures",
)

obs_exploration_augmented_phase = claim(
    "The exploration-augmented evolution phase (Evolver 2026-03-26) adds genes derived "
    "from external sources (arxiv papers, domain prior knowledge) in addition to run "
    "experience, creating a broader repertoire. By Mar 2026, the system maintains "
    "210 gene slots across 36 unique gene IDs, with domain-specific genes like "
    "gene_topic_hamiltonian_inverse_design activated 25 times [@Wang2026].",
    title="Exploration-augmented phase: external knowledge integration",
)

# --- Induction: law predicted by two independent evolver observations ---
# Generative direction: law([gene evolution consistently improves]) → prediction(~9pp over baseline)
# Both obs_evolver_feb and obs_evolver_mar are leaf claims with priors (set in priors.py).
# The law is derived from these two independent confirmations.

law_gene_evolution_improves = claim(
    "Gene-based test-time evolution consistently improves LLM performance on "
    "scientific code-solving benchmarks by approximately 9-10 percentage points "
    "above the contemporaneous baseline model.",
    title="Gene evolution law: consistent ~9-10pp improvement",
)

# Support in generative direction: law predicts the Feb 2026 observation
strat_law_predicts_feb = support(
    [law_gene_evolution_improves],
    obs_evolver_feb,
    reason=(
        "@law_gene_evolution_improves predicts ~9-10pp improvement over the baseline. "
        "The Feb 2026 evaluation with baseline 9.1% should yield ~18-19% accuracy. "
        "The observed @obs_evolver_feb (18.57%) falls within this predicted range, "
        "confirming the law's prediction for this evaluation point.",
    ),
    prior=0.87,
    background=[obs_critpt_baseline_feb],
)

# Support in generative direction: law predicts the Mar 2026 observation
strat_law_predicts_mar = support(
    [law_gene_evolution_improves],
    obs_evolver_mar,
    reason=(
        "@law_gene_evolution_improves predicts ~9-10pp improvement over the baseline. "
        "The Mar 2026 evaluation with baseline 17.7% should yield ~26-28% accuracy. "
        "The observed @obs_evolver_mar (27.14%) falls within this predicted range, "
        "confirming the law's prediction for this evaluation point.",
    ),
    prior=0.87,
    background=[obs_critpt_baseline_mar],
)

# Induction: two independent observations confirm the same law
ind_gene_evolution = induction(
    strat_law_predicts_feb, strat_law_predicts_mar,
    law=law_gene_evolution_improves,
    reason=(
        "Two independent CritPt evaluation points each confirm @law_gene_evolution_improves: "
        "Feb 2026 (+9.47pp, @obs_evolver_feb) and Mar 2026 (+9.44pp, @obs_evolver_mar). "
        "The evaluations are independent (different months, different baseline models), "
        "and both show consistent ~9.4-9.5pp improvement."
    ),
)

# --- Derived conclusions from evolution ---

gene_evolution_persistent_improvement = claim(
    "Gene-based test-time evolution achieves persistent, measurable accuracy improvements "
    "across two independent CritPt evaluation points. The improvement is stable at "
    "approximately +9.4-9.5pp in both evaluations (Feb: +9.47pp, Mar: +9.44pp), "
    "despite the underlying baseline model changing (9.1% → 17.7%). "
    "This consistency suggests evolution benefits are additive rather than model-specific [@Wang2026].",
    title="Gene evolution produces consistent ~9.4pp improvement across evaluations",
)

strat_persistent = support(
    [obs_evolver_feb, obs_evolver_mar],
    gene_evolution_persistent_improvement,
    reason=(
        "Both evolution evaluations show consistent improvement magnitude despite different baselines: "
        "@obs_evolver_feb (+9.47pp above the 9.1% baseline) and "
        "@obs_evolver_mar (+9.44pp above the 17.7% baseline). "
        "The consistency across changing underlying models confirms "
        "@gene_evolution_persistent_improvement."
    ),
    prior=0.85,
)

# --- Evolution enables accumulation ---

gene_enables_accumulation = claim(
    "The gene format enables iterative accumulation of reusable experience through "
    "the GEP protocol. The exploration-augmented evolver (Mar 2026) demonstrates "
    "that genes can be sourced from heterogeneous origins (run experience, arxiv, "
    "domain priors) and organized into a queryable library of 36 unique IDs, "
    "showing the gene format supports both targeted recall and broad exploration [@Wang2026].",
    title="Gene format enables heterogeneous experience accumulation",
)

strat_accumulation = support(
    [obs_exploration_augmented_phase, obs_evolver_mar],
    gene_enables_accumulation,
    reason=(
        "@obs_exploration_augmented_phase documents the multi-source gene library "
        "(210 slots, 36 IDs, three source types), and @obs_evolver_mar shows this "
        "library produces 27.14% accuracy (+9.44pp). The combination of library scale "
        "and performance improvement confirms @gene_enables_accumulation."
    ),
    prior=0.83,
)

# --- Overall findings (Section 4.5) ---

overall_four_findings = claim(
    "The paper's four principal empirical findings are: "
    "(1) Documentation skills are misaligned with test-time LLM control (Skill: -1.1pp); "
    "(2) Representation form is a first-order factor independent of content volume "
    "(Gene: +3.0pp vs Skill: -1.1pp from the same experience); "
    "(3) Gene format is a better substrate for failure accumulation "
    "(Gene+failure: 52.0% vs Skill+failure: 47.8%); "
    "(4) Failure experience is most effective when distilled into compact AVOID warnings "
    "(warnings-only: 54.4%, highest single failure-encoding condition) [@Wang2026].",
    title="Four principal empirical findings",
)

strat_four_findings = support(
    [obs_memory_grounded_phase, obs_evolver_feb, failure_distillation_principle,
     gene_best_failure_carrier],
    overall_four_findings,
    reason=(
        "@obs_memory_grounded_phase establishes the failure-to-gene conversion mechanism; "
        "@obs_evolver_feb shows +9.47pp from memory-grounded evolution; "
        "@failure_distillation_principle shows compact warnings outperform verbose records; "
        "@gene_best_failure_carrier shows gene is best carrier format. "
        "Together these confirm all four findings summarized in @overall_four_findings."
    ),
    prior=0.90,
)
