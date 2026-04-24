"""Section 4.1: Skill Probe — Documentation-Oriented Skills Misaligned with Control"""

from gaia.lang import claim, setting, support
from .motivation import (
    setup_eval, setup_skill_def, setup_gene_def,
    thesis_skill_misaligned, thesis_gene_superior,
)

# --- Observed pass rates (leaf claims = experimental measurements) ---

obs_baseline_passrate = claim(
    "The no-guidance baseline achieves an average pass rate of 51.0% "
    "(Gemini 3.1 Pro Preview: 60.1%, Gemini 3.1 Flash Lite Preview: 41.8%) "
    "across 45 scientific code-solving scenarios [@Wang2026].",
    title="No-guidance baseline pass rate",
    background=[setup_eval],
)

obs_skill_passrate = claim(
    "The full procedural skill package condition achieves an average pass rate of 49.9% "
    "(Gemini 3.1 Pro Preview: 50.7%, Gemini 3.1 Flash Lite Preview: 49.0%), "
    "which is -1.1pp below the no-guidance baseline of 51.0%. "
    "This represents net performance degradation despite providing additional information [@Wang2026].",
    title="Skill condition pass rate",
    background=[setup_eval, setup_skill_def],
)

obs_gene_passrate = claim(
    "The strategy gene condition achieves an average pass rate of 54.0% "
    "(Gemini 3.1 Pro Preview: 59.9%, Gemini 3.1 Flash Lite Preview: 48.2%), "
    "which is +3.0pp above the no-guidance baseline of 51.0% [@Wang2026].",
    title="Gene condition pass rate",
    background=[setup_eval, setup_gene_def],
)

# --- Skill decomposition findings ---

obs_skill_workflow_useful = claim(
    "Within the procedural skill package, only the Skill-Workflow sub-component "
    "(the step-by-step procedural workflow portion of d_main) shows clearly positive "
    "utility for test-time LLM control. This component contains concentrated, "
    "sequential procedural instructions with minimal extraneous documentation [@Wang2026].",
    title="Skill-Workflow sub-component is useful",
    background=[setup_skill_def],
)

obs_skill_overview_harmful = claim(
    "The Skill-Overview sub-component (the high-level summary portion of d_main) "
    "is strongly harmful to test-time LLM control performance. Adding the overview "
    "section actively degrades model pass rates, suggesting that high-level "
    "documentation language interferes with the model's ability to execute precise "
    "procedural steps [@Wang2026].",
    title="Skill-Overview sub-component is harmful",
    background=[setup_skill_def],
)

obs_budget_matched_fragment = claim(
    "When a budget-matched skill fragment (a portion of the skill package truncated "
    "to approximately 230 tokens, matching the Gene token budget) is used as the "
    "control signal, performance improves relative to the full skill but remains "
    "below the full Gene at 54.0% average pass rate. "
    "This confirms that token budget alone does not explain the Gene's superiority [@Wang2026].",
    title="Budget-matched skill fragment underperforms Gene",
    background=[setup_skill_def, setup_gene_def],
)

# --- Claim: signal concentration ---

signal_sparse = claim(
    "Usable control signals are sparsely distributed within procedural skill packages. "
    "The majority of the ~2,500-token skill package consists of human-readable "
    "documentation (overviews, API notes, examples) that provides little or negative "
    "marginal value for inference-time LLM control; only a narrow procedural slice "
    "(the workflow component) contains effective control signal [@Wang2026].",
    title="Skill signal sparsity",
)

# --- Claim: full-package aggregation harmful ---

aggregation_harmful = claim(
    "Aggregating all documentation sections into a complete skill package produces "
    "worse test-time control than any single useful section alone. The -1.1pp average "
    "degradation of the full skill (49.9%) versus the baseline (51.0%) indicates "
    "that harmful sections (e.g., Skill-Overview) dominate when included alongside "
    "useful sections (e.g., Skill-Workflow) [@Wang2026].",
    title="Skill aggregation is counterproductive",
)

# --- Strategies ---

strat_skill_degrades = support(
    [obs_skill_passrate, obs_baseline_passrate],
    thesis_skill_misaligned,
    reason=(
        "The measured pass rate for the full skill condition is 49.9% "
        "(@obs_skill_passrate), which is 1.1pp below the no-guidance baseline of 51.0% "
        "(@obs_baseline_passrate). This direct comparison shows that adding skill "
        "documentation causes net degradation, confirming @thesis_skill_misaligned."
    ),
    prior=0.92,
)

strat_gene_outperforms = support(
    [obs_gene_passrate, obs_baseline_passrate],
    thesis_gene_superior,
    reason=(
        "The gene condition achieves 54.0% (@obs_gene_passrate) versus the baseline "
        "51.0% (@obs_baseline_passrate), a +3.0pp improvement. Combined with the skill's "
        "-1.1pp degradation, the gene demonstrates clear superiority despite using "
        "approximately 11× fewer tokens, supporting @thesis_gene_superior."
    ),
    prior=0.92,
)

strat_sparsity = support(
    [obs_skill_workflow_useful, obs_skill_overview_harmful, obs_budget_matched_fragment],
    signal_sparse,
    reason=(
        "The decomposition results show @obs_skill_workflow_useful (workflow useful) "
        "while @obs_skill_overview_harmful (overview harmful), and "
        "@obs_budget_matched_fragment (budget-matched fragment better than full but "
        "worse than gene). Together these establish that usable control signal is "
        "concentrated in a narrow slice of the skill package, confirming @signal_sparse."
    ),
    prior=0.85,
)

strat_aggregation = support(
    [obs_skill_passrate, obs_skill_workflow_useful, obs_skill_overview_harmful],
    aggregation_harmful,
    reason=(
        "The full skill achieves 49.9% (@obs_skill_passrate) below baseline, while "
        "@obs_skill_workflow_useful shows the workflow component alone is positive and "
        "@obs_skill_overview_harmful shows the overview is strongly negative. "
        "The full package's underperformance is explained by harmful sections "
        "dominating the useful ones when combined, confirming @aggregation_harmful."
    ),
    prior=0.85,
)

# Note: the opposing effects of skill (-1.1pp) and gene (+3.0pp) are modeled
# through the separate support strategies above. No binary operator needed here since
# both thesis claims can be true simultaneously (one about skill, one about gene).
