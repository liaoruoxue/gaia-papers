"""Section 5: Discussion"""

from gaia.lang import (
    claim, setting,
    support, deduction,
    contradiction,
)

from .motivation import (
    harness_affects_outcomes,
    harness_logic_buried,
    harness_hard_to_compare,
    nlah_natural_language_feasibility,
)

from .s2_approach import (
    nlah_is_portable,
    nlah_enables_module_ablation,
    ihr_separates_concerns,
)

from .s4_results import (
    rq1_harness_controls_behavior,
    rq2_frontier_concentration,
    rq2_module_families,
    rq3_migration_score_gain,
    rq3_behavioral_relocation,
)

# --- Discussion claims ---

nl_not_replacing_code = claim(
    "Natural language in NLAHs is not argued to replace code. Natural language carries "
    "editable high-level harness logic, while code remains responsible for deterministic "
    "operations, tool interfaces, and sandbox enforcement. The scientific claim is about "
    "the unit of comparison: externalizing harness pattern logic as a readable, "
    "executable object under shared runtime semantics.",
    title="Discussion: NL carries harness logic; code handles deterministic operations",
)

nl_still_matters_for_control = claim(
    "Natural language remains important for agent systems when used to specify "
    "harness-level control — roles, contracts, verification gates, durable state "
    "semantics, and delegation boundaries — rather than only one-shot prompt phrasing. "
    "Gains from complex prompt engineering may diminish for stronger foundation models, "
    "but harness-level control remains a distinct engineering layer.",
    title="Discussion: NL matters for harness-level control, not one-shot prompting",
)

harness_search_space = claim(
    "Once harnesses are explicit objects (NLAHs), they become a search space. Explicit "
    "harness modules can be manually designed, retrieved, migrated, recombined, and "
    "systematically ablated under shared assumptions. Longer term, this suggests "
    "automated search and optimization over harness representations rather than opaque "
    "bundle engineering.",
    title="Discussion: Explicit harness representations enable automated harness search",
)

alt_stronger_models_reduce_nl_value = claim(
    "Stronger foundation models may reduce the incremental value of natural-language "
    "harness control, since improved base models can handle more multi-step reasoning "
    "without explicit scaffolding, making harness-level control less decisive.",
    title="Alternative: Stronger models may reduce value of NL harness control",
)

# --- Contradiction: NL matters for control vs. stronger models reduce NL value ---

not_both_nl_irrelevant = contradiction(
    nl_still_matters_for_control,
    alt_stronger_models_reduce_nl_value,
    reason=(
        "Both claims address the role of natural-language control as foundation models "
        "improve. If @nl_still_matters_for_control holds (harness-level control is a "
        "distinct layer), then @alt_stronger_models_reduce_nl_value cannot fully hold "
        "(the control layer remains valuable even with stronger models). These cannot "
        "both be true simultaneously."
    ),
    prior=0.85,
)

strat_nl_not_replacing_code = support(
    [rq1_harness_controls_behavior],
    nl_not_replacing_code,
    reason=(
        "@rq1_harness_controls_behavior shows that Full IHR is a behaviorally real "
        "control mechanism — not merely a richer prompt. This supports the scoping claim: "
        "natural language is responsible for harness-level control logic (which the data "
        "confirms has real behavioral impact), while code remains responsible for "
        "deterministic operations and tool interfaces. The scientific contribution is "
        "specifically about the harness pattern layer, not a general claim that NL "
        "replaces code."
    ),
    prior=0.88,
)

strat_nl_control_matters = support(
    [rq1_harness_controls_behavior, rq3_behavioral_relocation],
    nl_still_matters_for_control,
    reason=(
        "@rq1_harness_controls_behavior establishes that the runtime charter and harness "
        "logic are behaviorally real controls under current models (process metrics diverge "
        "substantially). @rq3_behavioral_relocation shows that the NLAH migration relocates "
        "reliability mechanisms structurally — not just adding prompt tokens. Together these "
        "support the view that harness-level control is a distinct engineering layer "
        "separate from one-shot prompt phrasing."
    ),
    prior=0.82,
)

strat_harness_search = support(
    [nlah_enables_module_ablation, rq2_module_families],
    harness_search_space,
    reason=(
        "@nlah_enables_module_ablation establishes that explicit NLAHs allow independent "
        "module composition and ablation. @rq2_module_families shows two qualitatively "
        "different module families can be identified through such ablation. Once modules "
        "are explicit objects with measurable effects, the same framework extends to "
        "automated search over harness representations."
    ),
    prior=0.80,
)
