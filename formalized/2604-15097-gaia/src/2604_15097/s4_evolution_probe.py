"""Section 4.3: Evolution Probe — Genes as Better Substrate for Experience Accumulation"""

from gaia.lang import claim, setting, support, abduction, induction
from .motivation import setup_eval, setup_gene_def, setup_gep, setup_skill_def
from .s4_skill_probe import obs_gene_passrate, obs_baseline_passrate, obs_skill_passrate

# --- Carrier format for failure history (Section 4.3.1) ---

obs_skill_plus_failure = claim(
    "Attaching raw failure history to the procedural skill package and using it as "
    "control signal achieves 47.8% average pass rate (-3.2pp below baseline, -2.1pp "
    "below skill alone), with Gemini 3.1 Pro at 53.8% and Flash Lite at 41.8%. "
    "Adding failure information to an already-misaligned representation further "
    "degrades performance [@Wang2026].",
    title="Skill + raw failure history further degrades performance",
    background=[setup_eval, setup_skill_def],
)

obs_freeform_plus_failure = claim(
    "Attaching raw failure history to unstructured freeform text and using it as "
    "control signal achieves 49.6% average pass rate (-1.4pp below baseline), "
    "with Gemini 3.1 Pro at 55.7% and Flash Lite at 43.5%. "
    "Unstructured failure information provides less value than no guidance [@Wang2026].",
    title="Freeform + raw failure history underperforms baseline",
    background=[setup_eval],
)

obs_gene_plus_raw_failure = claim(
    "Attaching raw failure history to the gene and using it as control signal "
    "achieves 52.0% average pass rate (+1.0pp above baseline, but -2.0pp below "
    "standalone gene at 54.0%), with Gemini 3.1 Pro at 55.3% and Flash Lite at 48.6%. "
    "Gene is the best carrier format for failure history, but naive appending still dilutes [@Wang2026].",
    title="Gene + raw failure history: best carrier but still dilutes",
    background=[setup_eval, setup_gene_def],
)

gene_best_failure_carrier = claim(
    "Among tested carrier formats, the strategy gene is the best substrate for "
    "attaching failure history information. Gene + failure achieves 52.0% average "
    "pass rate, versus 47.8% for Skill + failure and 49.6% for Freeform + failure. "
    "However, all naive-appending conditions fall below the standalone gene (54.0%), "
    "indicating that carrier format quality matters but raw appending is insufficient [@Wang2026].",
    title="Gene is the best failure carrier format",
)

strat_gene_best_carrier = support(
    [obs_skill_plus_failure, obs_freeform_plus_failure, obs_gene_plus_raw_failure],
    gene_best_failure_carrier,
    reason=(
        "Ranking the carrier conditions by performance: "
        "@obs_gene_plus_raw_failure (52.0%) > @obs_freeform_plus_failure (49.6%) > "
        "@obs_skill_plus_failure (47.8%). Gene is unambiguously best, but all three "
        "fall below standalone gene (54.0%), establishing both the gene's superiority "
        "as carrier and the limitation of naive appending, confirming @gene_best_failure_carrier."
    ),
    prior=0.90,
)

# --- Editable structure vs. flattened prose (Section 4.3.2) ---

obs_flattened_prose = claim(
    "Using flattened prose (converting the gene's structured format into continuous "
    "unstructured text with the same content) achieves 50.5% average pass rate "
    "(-0.5pp below baseline), with Gemini 3.1 Pro at 56.8% and Flash Lite at 44.1%. "
    "Flattening structure degrades performance even with identical content [@Wang2026].",
    title="Flattened prose underperforms baseline",
    background=[setup_eval],
)

obs_structured_gep = claim(
    "Using the Gene Evolution Protocol (GEP) structured format achieves 54.0% average "
    "pass rate (+3.0pp above baseline), with Gemini 3.1 Pro at 59.9% and Flash Lite at 48.2%. "
    "This is identical to the standalone gene result, confirming GEP structure "
    "preserves gene effectiveness [@Wang2026].",
    title="GEP structured format matches gene performance",
    background=[setup_eval, setup_gep],
)

structure_independent_value = claim(
    "The structured format of strategy genes contributes independently to test-time "
    "control effectiveness, beyond content alone. Structured GEP (54.0%) outperforms "
    "flattened prose (50.5%) with identical content. The -0.5pp degradation from "
    "flattening matches the structural contribution: removing structure costs "
    "~3.5pp relative to the structured gene, and the flattened version falls below baseline [@Wang2026].",
    title="Gene structure contributes value independent of content",
)

strat_structure_value = support(
    [obs_flattened_prose, obs_structured_gep],
    structure_independent_value,
    reason=(
        "The controlled comparison between @obs_flattened_prose (50.5%) and "
        "@obs_structured_gep (54.0%) holds content constant while varying format. "
        "The 3.5pp difference can only be attributed to structure. "
        "The fact that flattened prose falls below baseline (51.0%) while "
        "structured GEP is 3pp above confirms @structure_independent_value."
    ),
    prior=0.88,
)

# --- Failure history encoding within gene (Section 4.3.3) ---

obs_failure_first = claim(
    "When failure information is placed first in the gene (failure warnings prepended "
    "before strategy content), the system achieves 50.5% average pass rate (+0.7pp "
    "above the 49.8% adjusted baseline for this experiment), with Gemini 3.1 Pro at "
    "56.3% and Flash Lite at 44.7% [@Wang2026].",
    title="Failure-first encoding achieves modest improvement",
    background=[setup_eval],
)

obs_strategy_first = claim(
    "When strategy content is placed first in the gene (strategy prepended before "
    "failure information), the system achieves 51.8% average pass rate (+2.0pp above "
    "the 49.8% adjusted baseline), with Gemini 3.1 Pro at 58.4% and Flash Lite at 45.2%. "
    "Ordering strategy before failure improves performance over failure-first placement [@Wang2026].",
    title="Strategy-first encoding outperforms failure-first",
    background=[setup_eval],
)

obs_strategy_only_failure_exp = claim(
    "Using only the strategy component (without any failure information appended) "
    "in the failure encoding experiment achieves 52.3% average pass rate (+2.5pp "
    "above the 49.8% adjusted baseline), with Gemini 3.1 Pro at 56.9% and Flash Lite at 47.7%. "
    "Strategy without failure information is more effective than any strategy+failure combination [@Wang2026].",
    title="Strategy-only (no failure info) outperforms all strategy+failure combinations",
    background=[setup_eval],
)

obs_failure_warnings_only = claim(
    "Using only distilled failure warnings (compact AVOID cues α, derived from failure "
    "history without strategy steps) achieves 54.4% average pass rate (+4.6pp above the "
    "49.8% adjusted baseline), with Gemini 3.1 Pro at 56.8% and Flash Lite at 52.0%. "
    "This is the highest-performing condition in the failure encoding experiment, "
    "outperforming all strategy+failure combinations [@Wang2026].",
    title="Failure warnings only achieves highest performance in failure encoding experiment",
    background=[setup_eval],
)

failure_distillation_principle = claim(
    "Failure experience is most useful when distilled into compact AVOID warnings rather "
    "than combined with strategic content or appended verbatim. Distilled failure warnings "
    "only (54.4%) outperform strategy-only (52.3%), strategy+failure ordered combinations "
    "(50.5%-51.8%), and raw failure+gene (52.0%). "
    "The failure information is most potent when isolated as targeted negative guidance, "
    "not as part of a combined positive+negative bundle [@Wang2026].",
    title="Failure distillation principle: compact warnings outperform verbose failure records",
)

strat_failure_distillation = support(
    [obs_failure_warnings_only, obs_strategy_only_failure_exp,
     obs_strategy_first, obs_failure_first],
    failure_distillation_principle,
    reason=(
        "The four failure encoding conditions rank: "
        "@obs_failure_warnings_only (54.4%) > @obs_strategy_only_failure_exp (52.3%) > "
        "@obs_strategy_first (51.8%) > @obs_failure_first (50.5%). "
        "The dominance of pure warnings over combined strategy+failure objects, "
        "and the ordering effect (strategy before failure is better), together establish "
        "that compact isolated negative guidance outperforms verbose combination, "
        "confirming @failure_distillation_principle."
    ),
    prior=0.88,
)
