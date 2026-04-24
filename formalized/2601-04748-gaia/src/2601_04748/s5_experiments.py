"""
Section 5: Scaling Experiments — H1 through H4
================================================

Presents empirical results testing the four cognitive scaling hypotheses (H1-H4) using
controlled synthetic skill libraries with GPT-4o-mini and GPT-4o.
"""

from gaia.lang import claim, setting, support, abduction, induction, complement

from .s4_cognitive_theory import (
    h1_phase_transition,
    h2_confusability,
    h3_instructional_saturation,
    h4_hierarchy_mitigation,
    scaling_model,
    f1_hicks_law,
    f2_cognitive_load,
    f3_similarity_interference,
    f4_hierarchical_chunking,
)

# --- Experimental setup ---

exp_setup_scaling = setting(
    "Scaling experiments use a synthetic skill library spanning 8 domains (mathematics, coding, writing, "
    "analysis, translation, question-answering, formatting, extraction), each with 5 subtypes — "
    "40 distinct skill categories total. Each category has 5 skill templates, yielding a pool of "
    "200 unique skills. Skill descriptors follow the pattern '[Skill Name]: [Capability Description]'. "
    "Models evaluated: GPT-4o-mini and GPT-4o, temperature $T = 0$ for deterministic outputs. "
    "Selection accuracy is measured with 3 random seeds per condition for standard error estimates. "
    "Library sizes range from $|S| \\in \\{5, 10, 20, 50, 100, 150, 200\\}$.",
    title="Scaling experiment setup",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.1"},
)

similarity_distributions = setting(
    "Three similarity distributions control semantic overlap among skills in the library:\n\n"
    "- **Low (Diverse):** Skills sampled round-robin across all 8 domains, maximizing semantic distance.\n"
    "- **High (Similar):** Skills sampled from 2–3 semantically related domains (e.g., mathematics, analysis, extraction).\n"
    "- **Mixed:** Skills sampled uniformly at random across all domains — a naturalistic distribution "
    "with both related and unrelated skills (default for most experiments).",
    title="Similarity distributions for library construction",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.1"},
)

# --- H1 results ---

h1_fit_quality = claim(
    "The proposed accuracy scaling model $ACC \\approx \\alpha / (1 + (|S|/\\kappa)^\\gamma)$ fits "
    "empirical data with excellent quality:\n\n"
    "| Model | $\\alpha$ | $\\kappa$ | $\\gamma$ | $R^2$ |\n"
    "|---|---|---|---|---|\n"
    "| GPT-4o-mini | 0.96 | 91.8 | 1.72 | 0.978 |\n"
    "| GPT-4o | 0.98 | 83.5 | 1.56 | 0.968 |",
    title="H1: Scaling model fit quality (Figure 2)",
    metadata={
        "figure": "artifacts/2601.04748.pdf, Figure 2",
        "caption": "Figure 2: Scaling law fit quality. The proposed functional form achieves excellent fit (R² > 0.97) for both models.",
        "source": "artifacts/2601.04748.pdf, Section 5.2",
    },
)

h1_gamma_super_linear = claim(
    "The fitted decay exponent $\\gamma > 1$ (1.72 for GPT-4o-mini, 1.56 for GPT-4o) indicates "
    "super-linear degradation, consistent with phase transition behavior rather than gradual decay. "
    "Accuracy remains near $\\alpha$ for $|S| \\ll \\kappa$, then collapses precipitously when "
    "$|S| \\gg \\kappa$.",
    title="H1: Super-linear degradation (γ > 1)",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.2"},
)

h1_kappa_values = claim(
    "The fitted capacity threshold $\\kappa$ is 91.8 for GPT-4o-mini and 83.5 for GPT-4o, "
    "representing the library size at which accuracy drops to half its maximum "
    "($\\alpha/2 \\approx 0.48$–$0.49$). Interestingly, GPT-4o exhibits a slightly lower $\\kappa$ "
    "than GPT-4o-mini, contrary to the intuition that stronger models should have higher capacity. "
    "The authors offer two explanations: (1) fitting variance with limited data points, or "
    "(2) model capability and selection capacity may be partially independent.",
    title="H1: Capacity threshold κ ≈ 83–92 for GPT models",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.2"},
)

# --- H2 results ---

h2_competitor_experiment = setting(
    "H2 experiment design: For each base skill (e.g., 'Calculate Sum: Add all numbers together'), "
    "0, 1, or 2 competitor skills are generated with similar descriptions but different operations "
    "(e.g., 'Compute Average: Compute the mean of all values'). Three confusability conditions:\n\n"
    "- **No Competitors ($n_{comp}=0$):** Each skill is semantically distinct. $|S| = n_{base}$.\n"
    "- **Low Confusability ($n_{comp}=1$):** Each base skill has one competitor. $|S| = 2 \\times n_{base}$.\n"
    "- **High Confusability ($n_{comp}=2$):** Each base skill has two competitors. $|S| = 3 \\times n_{base}$.\n\n"
    "Ground truth is unambiguous: each task requires the base skill's specific operation "
    "(e.g., 'compute the sum'), and only the base skill produces the correct answer.",
    title="H2: Competitor experiment design",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.3"},
)

h2_competitor_results = claim(
    "Adding semantic competitors significantly degrades selection accuracy at fixed total library size:\n\n"
    "- Adding **1 competitor** per skill reduces accuracy by **7–30%** (Low condition).\n"
    "- Adding **2 competitors** causes **17–63%** degradation (High condition).\n"
    "- GPT-4o-mini shows larger drops than GPT-4o (e.g., 70% vs 37% accuracy at $n_{base}=10, n_{comp}=2$).\n"
    "- At identical $|S| = 20$, replacing unique skills with base-competitor pairs causes 18–30% accuracy drop.\n"
    "- The no-competitor condition maintains 100% accuracy at $|S| = 20$ where mixed-similarity libraries "
    "(H1) show measurable degradation.",
    title="H2: Competitor degradation 7–63% (Figure 3)",
    metadata={
        "figure": "artifacts/2601.04748.pdf, Figure 3",
        "caption": "Figure 3: Effect of skill competitors on selection accuracy. Higher confusability leads to lower accuracy at fixed library size.",
        "source": "artifacts/2601.04748.pdf, Section 5.3",
    },
)

h2_gpt4o_advantage = claim(
    "GPT-4o consistently outperforms GPT-4o-mini under high confusability conditions, "
    "achieving 70% vs 37% accuracy at $n_{base}=10, n_{comp}=2$. This suggests that model "
    "capability provides partial mitigation against confusability, though does not eliminate "
    "the fundamental scaling challenge.",
    title="H2: GPT-4o shows higher confusability resistance",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.3"},
)

# --- H3 results ---

h3_null_result = claim(
    "Contrary to hypothesis H3 (instructional saturation), the three policy complexity levels "
    "(simple ~30 tokens, medium ~100 tokens, complex ~300 tokens) show **largely overlapping accuracy curves** "
    "for both GPT-4o-mini and GPT-4o. The differences between conditions fall within standard error bounds "
    "at most library sizes. All complexity levels follow the same phase transition pattern observed in H1, "
    "with accuracy declining sharply beyond approximately $|S| = 50$.",
    title="H3: Policy complexity has negligible effect on accuracy (Figure 4)",
    metadata={
        "figure": "artifacts/2601.04748.pdf, Figure 4",
        "caption": "Figure 4: Effect of execution policy complexity on selection accuracy. Three complexity levels show largely overlapping performance curves.",
        "source": "artifacts/2601.04748.pdf, Section 5.4",
    },
)

h3_transformer_explanation = claim(
    "The null result for H3 (policy complexity not affecting accuracy) may be explained by transformer "
    "architectures efficiently filtering relevant information from long contexts — the attention mechanism "
    "may effectively ignore execution policy tokens during skill selection, mitigating the expected "
    "extraneous cognitive load from complex policies.",
    title="H3 null result: transformer attention filters policy tokens",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.4"},
)

# --- H4 results ---

h4_hierarchy_experiment = setting(
    "H4 experiment compares three selection strategies at library sizes beyond the capacity threshold:\n\n"
    "- **Flat Selection:** Direct selection from all $|S|$ skills (baseline).\n"
    "- **Naive Domain Hierarchy:** Two-stage selection — Stage 1 selects domain category, Stage 2 selects within domain.\n"
    "- **Confusability-Aware Hierarchy:** Two-stage selection — Stage 1 selects among distinct clusters, "
    "Stage 2 disambiguates within a small cluster of similar skills.\n\n"
    "Library sizes: $|S| \\in \\{12, 18, 24, 30, 60, 90, 120\\}$ (constructed with $n_{groups}$ groups "
    "of 3 semantically similar skills each — 1 base + 2 competitors).",
    title="H4: Hierarchy experiment setup",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.5"},
)

h4_hierarchy_results = claim(
    "Hierarchical routing substantially recovers accuracy when library size exceeds the capacity threshold "
    "($|S| \\geq 60$, approaching $\\kappa \\approx 90$):\n\n"
    "| Method | GPT-4o-mini at $|S|=120$ | GPT-4o at $|S|=120$ | Improvement (mini) |\n"
    "|---|---|---|---|\n"
    "| Flat Selection | ~45% | ~63% | baseline |\n"
    "| Naive Domain Hierarchy | ~83–85% | ~72% | +37–40% |\n"
    "| Confusability-Aware Hierarchy | ~83–85% | ~72% | +37–40% |\n\n"
    "Both hierarchical methods perform similarly because the experimental design naturally aligns "
    "domain boundaries with confusability clusters.",
    title="H4: Hierarchy improves accuracy +37–40% at large libraries (Figure 5)",
    metadata={
        "figure": "artifacts/2601.04748.pdf, Figure 5",
        "caption": "Figure 5: Effect of hierarchical routing on selection accuracy. At large library sizes (|S|≥60), hierarchy maintains ~72-85% accuracy while flat selection degrades to ~45-63%.",
        "source": "artifacts/2601.04748.pdf, Section 5.5",
    },
)

h4_gpt4o_smaller_benefit = claim(
    "GPT-4o shows higher flat accuracy than GPT-4o-mini at large $|S|$ (63% vs 45%), but also derives "
    "smaller benefit from hierarchical routing (+10% vs +40%). This pattern suggests that stronger models "
    "partially compensate for scaling challenges through better semantic discrimination, but hierarchical "
    "routing remains beneficial for all models.",
    title="H4: Stronger models get smaller hierarchical benefit",
    metadata={"source": "artifacts/2601.04748.pdf, Section 5.5"},
)

# --- Strategies: connecting observations to hypotheses ---

strat_h1_confirmed = support(
    [h1_fit_quality, h1_gamma_super_linear, h1_kappa_values],
    h1_phase_transition,
    background=[exp_setup_scaling],
    reason=(
        "H1 is confirmed by excellent model fit ($R^2 > 0.97$, @h1_fit_quality) and the measured "
        "super-linear decay exponent ($\\gamma > 1$, @h1_gamma_super_linear). The identified capacity "
        "threshold $\\kappa \\approx 83–92$ (@h1_kappa_values) demarcates the stable-accuracy regime "
        "from the collapse regime. Under the controlled experimental setup (@exp_setup_scaling), "
        "the phase transition pattern is clearly observed across both GPT-4o-mini and GPT-4o, "
        "consistent with the theoretical prediction derived from Hick's Law and Cognitive Load Theory [@Li2026].",
    ),
    prior=0.9,
)

strat_h2_confirmed = support(
    [h2_competitor_results, h2_gpt4o_advantage],
    h2_confusability,
    background=[h2_competitor_experiment, exp_setup_scaling],
    reason=(
        "H2 is confirmed by the competitor experiment (@h2_competitor_experiment): at identical total "
        "library size $|S| = 20$, replacing unique skills with base-competitor pairs causes 18–30% "
        "accuracy drop (@h2_competitor_results). The no-competitor condition maintains 100% accuracy "
        "at $|S| = 20$ where mixed-similarity libraries (H1) show degradation, directly demonstrating "
        "that semantic structure — not library size alone — determines selection difficulty. "
        "The GPT-4o advantage under high confusability (@h2_gpt4o_advantage) shows partial mitigation "
        "but not elimination, consistent with F3 interference being a fundamental challenge [@Shepard1987].",
    ),
    prior=0.92,
)

strat_h3_rejected = support(
    [h3_null_result],
    h3_instructional_saturation,
    background=[exp_setup_scaling],
    reason=(
        "H3 is NOT confirmed: the null result (@h3_null_result) shows no significant difference "
        "between policy complexity levels under controlled conditions (@exp_setup_scaling). "
        "The overlapping curves suggest that transformer attention mechanisms efficiently filter "
        "execution policy tokens during selection, contrary to the cognitive load prediction. "
        "This provides weak or no support for H3 — the hypothesis that policy verbosity reduces $\\kappa$ "
        "is not supported by these experiments, though the explanation (@h3_transformer_explanation) "
        "remains speculative.",
    ),
    prior=0.3,
)

strat_h4_confirmed = support(
    [h4_hierarchy_results, h4_gpt4o_smaller_benefit, h1_kappa_values],
    h4_hierarchy_mitigation,
    background=[h4_hierarchy_experiment],
    reason=(
        "H4 is confirmed: when library size exceeds the capacity threshold identified in H1 "
        "($|S| \\geq 60 \\approx \\kappa$, @h1_kappa_values), hierarchical routing recovers "
        "substantial accuracy (+37–40% for GPT-4o-mini, @h4_hierarchy_results). "
        "The two-stage hierarchical design ensures Stage 1 involves ~10–40 distinct clusters "
        "(well below $\\kappa$) and Stage 2 involves only 3 skills per cluster. "
        "This operationalizes the chunking principle (F4): by keeping each decision point below "
        "capacity, hierarchical routing restores reliable selection at scales otherwise intractable "
        "for flat selection (@h4_hierarchy_experiment). The smaller benefit for GPT-4o "
        "(@h4_gpt4o_smaller_benefit) is consistent with model capability providing partial compensation.",
    ),
    prior=0.9,
)

# --- Cross-hypothesis support: H2 explains H1 mechanism ---

strat_h1_h2_mechanism = support(
    [h2_confusability, h2_competitor_results],
    h1_phase_transition,
    reason=(
        "The phase transition observed in H1 (@h1_phase_transition) is mechanistically explained by "
        "H2 (@h2_confusability): as libraries grow with mixed-similarity sampling, the expected number "
        "of semantically similar skill pairs increases, causing the interference term $\\epsilon \\cdot I(S)$ "
        "to grow. The competitor experiment results (@h2_competitor_results) show that the 'no-competitor' "
        "condition maintains 100% accuracy at library sizes where mixed-similarity libraries show degradation — "
        "directly demonstrating that confusability accumulation drives the H1 capacity collapse.",
    ),
    prior=0.85,
)

__all__ = [
    "h1_fit_quality",
    "h1_gamma_super_linear",
    "h1_kappa_values",
    "h2_competitor_results",
    "h2_gpt4o_advantage",
    "h3_null_result",
    "h3_transformer_explanation",
    "h4_hierarchy_results",
    "h4_gpt4o_smaller_benefit",
    "strat_h1_confirmed",
    "strat_h2_confirmed",
    "strat_h3_rejected",
    "strat_h4_confirmed",
    "strat_h1_h2_mechanism",
]
