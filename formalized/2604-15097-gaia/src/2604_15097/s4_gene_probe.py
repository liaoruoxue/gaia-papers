"""Section 4.2: Gene Probe — Strategy Genes as Better Representation"""

from gaia.lang import claim, setting, support, abduction, compare
from .motivation import (
    setup_eval, setup_skill_def, setup_gene_def,
    thesis_form_over_content, thesis_gene_superior,
)
from .s4_skill_probe import obs_gene_passrate, obs_baseline_passrate, obs_skill_passrate

# --- Gene construction experiment ---

obs_keywords_only = claim(
    "Using only the keywords component of a gene (the task-matching signals m) "
    "as the control signal achieves 53.5% average pass rate (+2.5pp above baseline), "
    "with Gemini 3.1 Pro Preview at 57.9% and Flash Lite at 49.1% [@Wang2026].",
    title="Keywords-only gene component pass rate",
    background=[setup_eval],
)

obs_keywords_plus_summary = claim(
    "Using the keywords plus summary components (m + u) of a gene as the control "
    "signal reverts to 51.0% average pass rate (+0.0pp, equal to no-guidance baseline), "
    "with Gemini 3.1 Pro Preview at 51.3% and Flash Lite at 50.6%. "
    "Adding the compact summary (u) to keywords (m) does not improve and may slightly "
    "hurt performance compared to keywords alone [@Wang2026].",
    title="Keywords+summary gene components pass rate",
    background=[setup_eval],
)

obs_full_gene_construction = claim(
    "The complete gene structure (m, u, π, α, c, v) — including the strategic steps "
    "component π — achieves 54.0% average pass rate (+3.0pp), the highest among all "
    "construction variants. The benefit emerges specifically when the strategy layer π "
    "is added, not from progressive accumulation of the keyword or summary layers [@Wang2026].",
    title="Full gene construction achieves maximum pass rate",
    background=[setup_eval, setup_gene_def],
)

# --- Claim: strategy layer is the critical component ---

strategy_layer_critical = claim(
    "The strategic steps component π of a strategy gene is the critical differentiating "
    "element that drives performance improvement. Without π, gene components (keywords m, "
    "summary u) achieve at most +2.5pp; adding π achieves +3.0pp. More importantly, "
    "adding keywords+summary without π reverts to baseline (0.0pp), showing that "
    "accumulating descriptive tokens without strategic framing provides no benefit [@Wang2026].",
    title="Strategic steps (π) are the critical gene component",
)

strat_strategy_critical = support(
    [obs_keywords_only, obs_keywords_plus_summary, obs_full_gene_construction],
    strategy_layer_critical,
    reason=(
        "The three construction conditions form a diagnostic: "
        "@obs_keywords_only (m only: +2.5pp), @obs_keywords_plus_summary (m+u: 0.0pp), "
        "@obs_full_gene_construction (full with π: +3.0pp). "
        "The non-monotonic pattern — adding summary hurts, but adding strategy helps — "
        "isolates the strategic steps layer π as the active ingredient. "
        "Token accumulation alone does not explain gains, confirming @strategy_layer_critical."
    ),
    prior=0.87,
)

# --- Robustness to perturbations ---

obs_content_corrupt_wrong_algo = claim(
    "When a gene with incorrect algorithm (wrong-algorithm content corruption) is used "
    "as the control signal, average pass rate drops to 48.8% (-2.2pp below the gene's "
    "54.0%, below the 51.0% baseline), indicating that semantic content accuracy matters "
    "for gene effectiveness [@Wang2026].",
    title="Wrong-algorithm gene reduces performance below baseline",
    background=[setup_eval],
)

obs_content_corrupt_wrong_domain = claim(
    "When a gene with incorrect domain (wrong-domain content corruption) is used "
    "as the control signal, average pass rate drops to 49.4% (-1.6pp below the gene's "
    "54.0%), also below the 51.0% baseline, confirming that domain-accurate content "
    "is necessary for gene effectiveness [@Wang2026].",
    title="Wrong-domain gene reduces performance below baseline",
    background=[setup_eval],
)

obs_structural_inverted_priority = claim(
    "When the gene's internal priority ordering is inverted (structural perturbation: "
    "reordering strategic steps in reverse priority), pass rate remains at 52.8% "
    "(−1.2pp from gene's 54.0%, but still +1.8pp above baseline), showing that "
    "structural deformation is tolerated better than content corruption [@Wang2026].",
    title="Inverted-priority gene maintains above-baseline performance",
    background=[setup_eval],
)

obs_structural_overconstrained = claim(
    "When the gene is overconstrained (structural perturbation: adding additional "
    "restrictive constraints beyond the original), pass rate rises to 55.9% "
    "(+1.9pp above gene's 54.0%, +4.9pp above baseline), suggesting that "
    "additional specificity can sometimes help rather than hurt [@Wang2026].",
    title="Overconstrained gene achieves highest single-perturbation pass rate",
    background=[setup_eval],
)

# --- Claim: content vs structure sensitivity ---

gene_sensitive_to_content_not_structure = claim(
    "Strategy genes are more sensitive to content accuracy than to structural "
    "deformation. Content corruptions (wrong algorithm: 48.8%, wrong domain: 49.4%) "
    "drive performance below the 51.0% baseline, while structural perturbations "
    "(inverted priority: 52.8%, overconstrained: 55.9%) remain at or above baseline. "
    "The structure itself carries independent value even when partially malformed [@Wang2026].",
    title="Genes tolerate structural deformation but require content accuracy",
)

strat_content_structure = support(
    [obs_content_corrupt_wrong_algo, obs_content_corrupt_wrong_domain,
     obs_structural_inverted_priority, obs_structural_overconstrained],
    gene_sensitive_to_content_not_structure,
    reason=(
        "The four perturbation conditions divide cleanly: content corruptions "
        "(@obs_content_corrupt_wrong_algo: 48.8%, @obs_content_corrupt_wrong_domain: 49.4%) "
        "fall below baseline, while structural perturbations "
        "(@obs_structural_inverted_priority: 52.8%, @obs_structural_overconstrained: 55.9%) "
        "remain above baseline. This asymmetric pattern establishes that semantic "
        "content must be correct but structural form is flexible, "
        "confirming @gene_sensitive_to_content_not_structure."
    ),
    prior=0.85,
)

# --- Documentation reattachment ---

obs_gene_plus_api = claim(
    "Adding API notes (d_aux api_notes from the skill package) back to the gene "
    "results in 51.5% average pass rate (+0.5pp above baseline, -2.5pp below standalone gene), "
    "with Gemini 3.1 Pro at 51.8% and Flash Lite at 51.2%. "
    "The API documentation dilutes gene effectiveness despite providing correct information [@Wang2026].",
    title="Gene + API notes underperforms standalone gene",
    background=[setup_eval, setup_skill_def],
)

obs_gene_plus_examples = claim(
    "Adding code examples (d_aux examples from the skill package) to the gene "
    "results in 52.0% average pass rate (+1.0pp above baseline, -2.0pp below standalone gene), "
    "with Gemini 3.1 Pro at 57.8% and Flash Lite at 46.1%. "
    "Example reattachment partially dilutes gene effectiveness [@Wang2026].",
    title="Gene + examples underperforms standalone gene",
    background=[setup_eval, setup_skill_def],
)

documentation_dilution = claim(
    "Reattaching documentation components (API notes or examples) to a strategy gene "
    "degrades its test-time control effectiveness below the standalone gene, even when "
    "the documentation is factually correct. Gene + API notes achieves 51.5% and "
    "Gene + examples achieves 52.0%, both below the standalone gene's 54.0%. "
    "Complementarity of gene and documentation does not offset dilution effects [@Wang2026].",
    title="Documentation reattachment dilutes gene effectiveness",
)

strat_dilution = support(
    [obs_gene_plus_api, obs_gene_plus_examples, obs_gene_passrate],
    documentation_dilution,
    reason=(
        "Both augmented conditions degrade performance: @obs_gene_plus_api (51.5%) "
        "and @obs_gene_plus_examples (52.0%) both fall below the standalone "
        "@obs_gene_passrate (54.0%). The pattern holds across both documentation types "
        "and across both models, establishing that documentation reattachment systematically "
        "dilutes gene control effectiveness, confirming @documentation_dilution."
    ),
    prior=0.88,
)

# --- Multi-gene composition ---

obs_two_complementary_genes = claim(
    "Using two complementary strategy genes (covering different but related scenarios) "
    "simultaneously as control signal achieves only 44.9% average pass rate "
    "(-6.1pp below baseline), with Gemini 3.1 Pro at 45.5% and Flash Lite at 44.3%. "
    "This is the worst-performing condition tested [@Wang2026].",
    title="Two complementary genes severely degrades performance",
    background=[setup_eval],
)

obs_three_complementary_genes = claim(
    "Using three complementary strategy genes simultaneously achieves 50.4% average "
    "pass rate (-0.6pp below baseline, but -3.6pp below single gene), "
    "with Gemini 3.1 Pro at 54.5% and Flash Lite at 46.2%. "
    "Performance partially recovers from the two-gene case but remains below single gene [@Wang2026].",
    title="Three complementary genes underperforms single gene",
    background=[setup_eval],
)

obs_two_conflicting_genes = claim(
    "Using two conflicting strategy genes (encoding mutually inconsistent strategies) "
    "simultaneously achieves 53.2% average pass rate (+2.2pp above baseline, -0.8pp "
    "below single gene), suggesting that conflicting signals self-cancel rather than "
    "accumulate harm [@Wang2026].",
    title="Two conflicting genes nearly matches single gene",
    background=[setup_eval],
)

gene_reuse_scope_bounded = claim(
    "Gene reusability has bounded scope in scientific code-solving contexts. "
    "A single targeted gene achieves the highest pass rate (54.0%), while all "
    "multi-gene composition strategies underperform: two complementary genes (44.9%), "
    "three complementary genes (50.4%), two conflicting genes (53.2%). "
    "Accumulating more genes does not improve performance and often causes interference [@Wang2026].",
    title="Gene reusability is scope-bounded; single gene is optimal",
)

strat_scope_bounded = support(
    [obs_two_complementary_genes, obs_three_complementary_genes,
     obs_two_conflicting_genes, obs_gene_passrate],
    gene_reuse_scope_bounded,
    reason=(
        "All multi-gene conditions underperform the single gene (@obs_gene_passrate: 54.0%): "
        "@obs_two_complementary_genes (44.9%), @obs_three_complementary_genes (50.4%), "
        "@obs_two_conflicting_genes (53.2%). The monotone relationship (more genes → worse) "
        "holds for complementary genes, while conflicting genes nearly match the single gene, "
        "suggesting interference rather than complementary benefit drives multi-gene degradation, "
        "confirming @gene_reuse_scope_bounded."
    ),
    prior=0.85,
)

# Abduction: why does structure help even when content is wrong?
alt_attention_bias = claim(
    "The structural format of the gene may bias the model's attention toward "
    "relevant procedural steps via token placement and formatting, independently "
    "of whether the semantic content is accurate (attention-bias hypothesis).",
    title="Alternative: structural format creates attention bias independent of content",
)

pred_gene_structure_helps = claim(
    "The gene's structured format (explicit fields for strategic steps, constraints, "
    "validation hooks) provides a consistent template that the model can execute "
    "even when content is partially wrong, because the structure cues execution mode.",
    title="Gene structure cues execution mode (hypothesis)",
)

pred_attention_bias = claim(
    "If attention bias were the primary mechanism, then shuffling or inverting "
    "gene fields while preserving format should maintain or improve performance, "
    "and the exact semantic content of the strategy steps would not matter.",
    title="Attention bias predicts format-only sufficiency",
)

strat_structure_h = support(
    [pred_gene_structure_helps],
    obs_structural_inverted_priority,
    reason=(
        "@pred_gene_structure_helps: if structure cues execution mode, the model "
        "follows the template even with inverted priority, explaining why "
        "@obs_structural_inverted_priority (52.8%) stays above baseline."
    ),
    prior=0.72,
)

strat_structure_alt = support(
    [alt_attention_bias],
    obs_structural_inverted_priority,
    reason=(
        "@alt_attention_bias: if structural format creates attention bias independently "
        "of content, then inverted priority would still trigger attention to the "
        "strategy section, explaining @obs_structural_inverted_priority staying above baseline."
    ),
    prior=0.55,
)

comp_structure_mechanism = compare(
    pred_gene_structure_helps,
    pred_attention_bias,
    obs_structural_inverted_priority,
    reason=(
        "Both hypotheses explain why structural perturbations maintain above-baseline "
        "performance. The execution-mode cuing hypothesis better accounts for why "
        "content corruption (wrong algorithm/domain) drops below baseline: "
        "if structure alone sufficed, content accuracy wouldn't matter. "
        "Attention bias cannot explain the content sensitivity, giving the "
        "execution-mode hypothesis higher explanatory completeness."
    ),
    prior=0.75,
)

abd_structure_mechanism = abduction(
    strat_structure_h, strat_structure_alt, comp_structure_mechanism,
    reason="Both hypotheses attempt to explain why structural perturbations tolerate deformation",
)
