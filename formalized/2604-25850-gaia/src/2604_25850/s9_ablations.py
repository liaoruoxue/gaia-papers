"""Section 4.4 (RQ3): component-level ablations and self-attribution analysis.

The AHE gain localizes to tools, middleware, and long-term memory; the system
prompt alone regresses, suggesting factual structure transfers while prose-
level strategy does not. Components interact non-additively, capping
aggregate gain.

Source: Lin et al. 2026 [@Lin2026AHE], Section 4.4 + Table 3.
"""

from gaia.lang import claim

# ===========================================================================
# Section 4.4.1: where value accumulates across components (Table 3)
# ===========================================================================

claim_ablation_table = claim(
    "**Table 3: component-level ablation on Terminal-Bench 2.** Each "
    "'+ X only' row swaps a single AHE component into the NexAU0 seed "
    "(long-term memory, tool set, middleware, or system prompt) and "
    "leaves the other three at seed defaults. Per-column best in "
    "bold.\n\n"
    "| Variant | All (89) | Easy (4) | Med (55) | Hard (30) |\n"
    "|---|---:|---:|---:|---:|\n"
    "| NexAU0 | 69.7% | 87.5% | 78.2% | 51.7% |\n"
    "| + memory only | 75.3% | 50.0% | 83.6% | **63.3%** |\n"
    "| + tool only | 73.0% | 75.0% | 87.3% | 46.7% |\n"
    "| + middleware only | 71.9% | **100.0%** | 81.8% | 50.0% |\n"
    "| + system_prompt only | 67.4% | 75.0% | 78.2% | 46.7% |\n"
    "| **AHE full** | **77.0%** | **100.0%** | **88.2%** | 53.3% |\n",
    title="Table 3: component-level ablation (each component swapped alone vs full AHE)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 3",
        "caption": "Table 3: component-level ablations on Terminal-Bench 2.",
    },
)

# ---- Atomic per-component ablation deltas vs seed (NexAU0 = 69.7%) ----

claim_memory_only_delta = claim(
    "**Long-term memory only: +5.6 pp (69.7% -> 75.3%).** Swapping "
    "AHE's long-term memory alone into the NexAU0 seed (no other AHE "
    "components) yields the largest single-component lift. Per-"
    "difficulty: Easy 50.0% (-37.5 pp), Medium 83.6% (+5.4 pp), "
    "**Hard 63.3% (+11.6 pp, exceeds full AHE on Hard)**. Memory adds "
    "12 boundary-case lessons (performance margin, queued-over-limit "
    "cancellation, evaluator-style closure, source-packaging layout); "
    "on Hard the lessons lift it above full AHE, while on Easy they "
    "reduce to superfluous re-verification.",
    title="Ablation: + memory only = +5.6 pp aggregate; +11.6 pp on Hard (exceeds full AHE on Hard)",
)

claim_tool_only_delta = claim(
    "**Tools only: +3.3 pp (69.7% -> 73.0%).** Swapping AHE's tools "
    "alone yields a +3.3 pp lift. Per-difficulty: Easy 75.0%, Medium "
    "87.3% (+9.1 pp, lands within 0.9 pp of full AHE's 88.2%), Hard "
    "46.7% (-5.0 pp, regresses on Hard). Tools become a 1364-line "
    "shell that auto-surfaces contract hints from files near each "
    "command; on Hard a built-in publish guard closes the loop too "
    "early.",
    title="Ablation: + tools only = +3.3 pp aggregate; +9.1 pp on Medium (~full AHE)",
)

claim_middleware_only_delta = claim(
    "**Middleware only: +2.2 pp (69.7% -> 71.9%).** Swapping AHE's "
    "middleware alone yields +2.2 pp. Per-difficulty: **Easy 100.0% "
    "(+12.5 pp, ties full AHE on Easy)**, Medium 81.8% (+3.6 pp), "
    "Hard 50.0% (-1.7 pp). Middleware adds a finish-hook that forces "
    "one evaluator-isomorphic closure check; on Easy it clears every "
    "task, while on Hard it inflates turn count.",
    title="Ablation: + middleware only = +2.2 pp aggregate; +12.5 pp on Easy (ties full AHE)",
)

claim_prompt_only_regression = claim(
    "**System prompt only: -2.3 pp (69.7% -> 67.4%).** Swapping AHE's "
    "evolved system prompt alone into the NexAU0 seed -- without the "
    "other three components -- *regresses* below the seed. Per-"
    "difficulty: Easy 75.0% (-12.5 pp), Medium 78.2% (0.0 pp), Hard "
    "46.7% (-5.0 pp). The system prompt encodes 79 lines of universal "
    "discipline whose executability depends on the other three "
    "components.",
    title="Ablation: + prompt only = -2.3 pp aggregate (REGRESSES below seed)",
)

# ---- Per-component failure surfaces (claims separated for atomicity) ----

claim_memory_failure_surface = claim(
    "**Memory's failure surface: boundary-case discipline.** Memory "
    "encodes 12 boundary-case lessons (performance margin, queued-"
    "over-limit cancellation, evaluator-style closure, source-"
    "packaging layout). These are factual contract patterns, not "
    "procedural rules; they lift Hard tasks where contract subtlety "
    "matters and reduce to superfluous re-verification on Easy where "
    "the contract is obvious.",
    title="Memory failure surface: boundary-case contract discipline (12 lessons)",
)

claim_tool_failure_surface = claim(
    "**Tools' failure surface: contract surfacing + publish-state "
    "interlock.** AHE's evolved tools become a 1364-line shell that "
    "auto-surfaces contract hints from files near each command. On "
    "Medium it lands within 0.9 pp of full AHE because Medium tasks "
    "match this surface most closely. On Hard the built-in publish "
    "guard closes the loop too early, regressing -5.0 pp.",
    title="Tools failure surface: contract surfacing + publish-state interlock (1364-line shell)",
)

claim_middleware_failure_surface = claim(
    "**Middleware's failure surface: finish-hook closure check.** "
    "Middleware adds an evaluator-isomorphic closure check at "
    "finish time. On Easy this closure check clears every task "
    "(+12.5 pp). On Hard it inflates turn count and trails by 1.7 "
    "pp.",
    title="Middleware failure surface: finish-hook closure check (clears Easy, inflates Hard)",
)

claim_prompt_failure_surface = claim(
    "**System prompt's failure surface: prose-level discipline rules.** "
    "The evolved system prompt encodes 79 lines of universal discipline "
    "whose **executability depends on the other three components**. "
    "Inserted alone, the rules become advisory text the agent does "
    "not follow at execution time.",
    title="Prompt failure surface: prose-level discipline rules require execution-time backing from tools/middleware/memory",
)

# ===========================================================================
# Components interact non-additively
# ===========================================================================

claim_non_additive_interaction = claim(
    "**Components interact non-additively, capping the aggregate gain.** "
    "The three positive single-component gains sum to +11.1 pp "
    "(memory +5.6 + tools +3.3 + middleware +2.2) but full AHE achieves "
    "only +7.3 pp. **On Hard the memory-only variant (63.3%) exceeds "
    "full AHE (53.3%) by 10.0 pp**: memory, middleware, and the system "
    "prompt all push toward the same closure-style verification, so "
    "stacking them spends turns on redundant re-checks within the long-"
    "horizon budget. The Evolve Agent optimizes an aggregate dominated "
    "by 55 Medium tasks, so it converges to a Medium-heavy trade-off "
    "that returns part of the Hard memory effect; interaction-aware "
    "evolution is left to future work.",
    title="Ablation finding: components interact non-additively (sum of single = +11.1 vs full = +7.3); memory alone > full AHE on Hard",
)

# ===========================================================================
# Localization claims for the headline
# ===========================================================================

claim_factual_structure_transfers = claim(
    "**Localization finding: factual harness structure transfers, "
    "prose-level strategy does not.** Tools / middleware / long-term "
    "memory each carry the gain on their own (+3.3 / +2.2 / +5.6 pp); "
    "the system prompt alone regresses (-2.3 pp). This pattern holds "
    "the central claim that what evolves usefully across iterations "
    "is *factual harness structure* (executable code, indexed "
    "lessons, intercept hooks) rather than *prose-level strategy* "
    "(advisory text rules).",
    title="Headline localization: factual structure (tools/middleware/memory) transfers; prose-level strategy (prompt) does not",
)

# ===========================================================================
# Section 4.4.2: how reliably does self-attribution track reality?
# (anchored to the per-round breakdowns -- the cross-iteration aggregates
# already live in s6_decision_observability.py)
# ===========================================================================

claim_per_round_fix_breakdown = claim(
    "**Per-round fix-prediction statistics (Appendix D / Fig. 11).** "
    "Cross-iteration fix-precision (33.7%) and fix-recall (51.4%) "
    "swing from near-zero to near-saturation across rounds, with "
    "stacked TP / FP / FN bars showing each denominator's "
    "decomposition: in 9 evaluation rounds the agent issued (per "
    "round) 21, 13, 9, 4, 8, 8, 6, 8, 8 predicted fixes (a total "
    "across-rounds count tracking pass@1 movement). Fix-side "
    "attribution is **informative but noisy**.",
    title="Per-round detail: fix-prediction precision/recall swing near-zero to near-saturation across 9 rounds",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 11",
        "caption": "Fig. 11: Per-round fix predictions, precision and recall.",
    },
)

claim_attribution_is_asymmetric = claim(
    "**Self-attribution is asymmetric: reliable for fixes, blind for "
    "regressions.** The Evolve Agent's fix predictions sit ~5x above "
    "random (precision 33.7% vs 6.5%, recall 51.4% vs 10.6%), but its "
    "regression predictions sit only ~2x above random (precision "
    "11.8% vs 5.6%, recall 11.1% vs 5.4%). The agent can justify why "
    "an edit *should* help but cannot reliably name the tasks the "
    "same edit is about to *break*. Closing this gap is identified as "
    "the clearest direction for future self-evolution loops.",
    title="Section 4.4.2 finding: self-attribution is asymmetric (fixes 5x random; regressions only 2x)",
)

claim_regression_blindness_explains_non_monotone = claim(
    "**Regression blindness produces non-monotone evolution steps.** "
    "Because the Evolve Agent foresees only ~11% of upcoming "
    "regressions, edits that fix one cluster of failures sometimes "
    "introduce uncaught regressions on other tasks. This produces "
    "the non-monotone steps in the iteration trajectory of Section "
    "4.2 (the AHE pass@1 line in Fig. 1 oscillates rather than "
    "monotonically rising).",
    title="Section 4.4.2 finding: regression blindness causes the non-monotone steps in the AHE iteration curve",
)

__all__ = [
    "claim_ablation_table",
    "claim_memory_only_delta",
    "claim_tool_only_delta",
    "claim_middleware_only_delta",
    "claim_prompt_only_regression",
    "claim_memory_failure_surface",
    "claim_tool_failure_surface",
    "claim_middleware_failure_surface",
    "claim_prompt_failure_surface",
    "claim_non_additive_interaction",
    "claim_factual_structure_transfers",
    "claim_per_round_fix_breakdown",
    "claim_attribution_is_asymmetric",
    "claim_regression_blindness_explains_non_monotone",
]
