"""Section 5: Experimental Results"""

from gaia.lang import claim, setting, support, abduction, compare

from .s3_methodology import (
    cib_objective_def,
    combined_reward_def,
    semantic_cost_advantage,
    rl_objective_formulation,
)
from .s4_theory import (
    cib_unifies_budget_forcing,
    semantic_prior_superiority_theory,
)
from .motivation import budget_forcing_heuristic

# --- Settings: experimental setup ---

eval_benchmarks_def = setting(
    "Five math reasoning benchmarks are used for evaluation:\n"
    "- MATH500: 500 competition-level math problems\n"
    "- AIME24: 2024 American Invitational Mathematics Examination problems\n"
    "- AIME25: 2025 American Invitational Mathematics Examination problems\n"
    "- Minerva: science reasoning benchmark\n"
    "- OlympiadBench: olympiad-level math problems\n"
    "Models are evaluated on accuracy (higher is better) and average token count (lower is better).",
    title="Evaluation benchmarks definition",
)

base_models_def = setting(
    "Two base models are evaluated: DeepScaleR-1.5B (Deepscaler) and DLER (1.5B and 7B variants). "
    "CIB training uses Qwen2.5-Base as the frozen prior model $Q_\\phi$ in two sizes: 1.5B and 7B. "
    "Training uses GRPO with group size 16, temperature 0.6, top_p 0.95, 16 generations per prompt. "
    "Two compression levels are tested: conservative ($\\beta^- = 5 \\times 10^{-5}$) and "
    "aggressive ($\\beta^+ = 1.5 \\times 10^{-4}$).",
    title="Base models and training setup",
)

# --- Experimental result claims ---

deepscaler_cib_conservative = claim(
    "On DeepScaleR-1.5B with CIB using 1.5B prior ($\\beta^- = 5\\times10^{-5}$, conservative), "
    "average accuracy improves from 44.7% (baseline) to 45.9% (+1.2pp), while average token "
    "count decreases from 6,722 (baseline) to 5,045 tokens (−25%):\n\n"
    "| Benchmark | Acc (base) | Acc (CIB) | Tok (base) | Tok (CIB) |\n"
    "|-----------|-----------|-----------|-----------|----------|\n"
    "| MATH500   | 85.8%     | 87.6%     | 3,190     | 2,359    |\n"
    "| AIME24    | 38.1%     | 39.2%     | 9,269     | 7,156    |\n"
    "| AIME25    | 25.2%     | 27.3%     | 8,901     | 6,725    |\n"
    "| Minerva   | 19.9%     | 20.1%     | 6,375     | 4,512    |\n"
    "| Olympiad  | 54.7%     | 55.4%     | 5,875     | 4,473    |",
    title="DeepScaleR: CIB conservative compression results (25% token reduction, +1.2pp accuracy)",
    background=[eval_benchmarks_def, base_models_def],
    metadata={"source_section": "Section 5, Table 1"},
)

deepscaler_cib_aggressive = claim(
    "On DeepScaleR-1.5B with CIB using 1.5B prior ($\\beta^+ = 1.5\\times10^{-4}$, aggressive), "
    "average accuracy improves from 44.7% (baseline) to 46.0% (+1.3pp), while average token "
    "count decreases from 6,722 (baseline) to 4,797 tokens (−29%):\n\n"
    "| Benchmark | Acc (base) | Acc (CIB) | Tok (base) | Tok (CIB) |\n"
    "|-----------|-----------|-----------|-----------|----------|\n"
    "| MATH500   | 85.8%     | 87.8%     | 3,190     | 2,106    |\n"
    "| AIME24    | 38.1%     | 40.2%     | 9,269     | 6,857    |\n"
    "| AIME25    | 25.2%     | 26.3%     | 8,901     | 6,672    |\n"
    "| Minerva   | 19.9%     | 20.3%     | 6,375     | 4,144    |\n"
    "| Olympiad  | 54.7%     | 55.3%     | 5,875     | 4,208    |",
    title="DeepScaleR: CIB aggressive compression results (29% token reduction, +1.3pp accuracy)",
    background=[eval_benchmarks_def, base_models_def],
    metadata={"source_section": "Section 5, Table 1"},
)

deepscaler_7b_prior = claim(
    "On DeepScaleR-1.5B with CIB using a larger 7B prior model, average accuracy decreases "
    "from 44.7% (baseline) to 44.0% (−0.7pp), while average token count decreases from 6,722 "
    "to 3,951 tokens (−41%). This demonstrates aggressive compression with minimal accuracy cost:\n\n"
    "| Benchmark | Acc (base) | Acc (CIB-7B) | Tok (base) | Tok (CIB-7B) |\n"
    "|-----------|-----------|-------------|-----------|-------------|\n"
    "| MATH500   | 85.8%     | 84.0%       | 3,190     | 1,548       |\n"
    "| AIME24    | 38.1%     | 35.2%       | 9,269     | 5,720       |\n"
    "| AIME25    | 25.2%     | 25.8%       | 8,901     | 5,362       |\n"
    "| Minerva   | 19.9%     | 19.6%       | 6,375     | 3,097       |\n"
    "| Olympiad  | 54.7%     | 55.2%       | 5,875     | 4,029       |",
    title="DeepScaleR: CIB with 7B prior achieves 41% token reduction with only −0.7pp accuracy",
    background=[eval_benchmarks_def, base_models_def],
    metadata={"source_section": "Section 5, Table 1"},
)

dler_7b_cib_conservative = claim(
    "On DLER-7B with CIB using 7B prior ($\\beta^- = 5\\times10^{-5}$, conservative), "
    "average accuracy improves from 54.2% (baseline) to 54.3% (+0.1pp), while average token "
    "count decreases from 2,481 (baseline) to 2,285 tokens (−8%):\n\n"
    "| Benchmark | Acc (base) | Acc (CIB) | Tok (base) | Tok (CIB) |\n"
    "|-----------|-----------|-----------|-----------|----------|\n"
    "| MATH500   | 93.6%     | 94.0%     | 1,159     | 1,033    |\n"
    "| AIME24    | 48.5%     | 49.4%     | 3,261     | 3,003    |\n"
    "| AIME25    | 36.9%     | 37.1%     | 3,264     | 3,113    |\n"
    "| Minerva   | 27.2%     | 26.7%     | 1,872     | 1,643    |\n"
    "| Olympiad  | 65.0%     | 64.3%     | 2,851     | 2,632    |",
    title="DLER-7B: CIB conservative compression (8% token reduction, +0.1pp accuracy)",
    background=[eval_benchmarks_def, base_models_def],
    metadata={"source_section": "Section 5, Table 1"},
)

dler_7b_cib_aggressive = claim(
    "On DLER-7B with CIB using 7B prior ($\\beta^+ = 1.5\\times10^{-4}$, aggressive), "
    "average accuracy decreases from 54.2% (baseline) to 52.9% (−1.3pp), while average token "
    "count decreases from 2,481 (baseline) to 1,687 tokens (−32%):\n\n"
    "| Benchmark | Acc (base) | Acc (CIB) | Tok (base) | Tok (CIB) |\n"
    "|-----------|-----------|-----------|-----------|----------|\n"
    "| MATH500   | 93.6%     | 92.2%     | 1,159     | 678      |\n"
    "| AIME24    | 48.5%     | 48.3%     | 3,261     | 2,617    |\n"
    "| AIME25    | 36.9%     | 35.6%     | 3,264     | 2,580    |\n"
    "| Minerva   | 27.2%     | 25.8%     | 1,872     | 849      |\n"
    "| Olympiad  | 65.0%     | 62.6%     | 2,851     | 1,711    |",
    title="DLER-7B: CIB aggressive compression (32% token reduction, −1.3pp accuracy)",
    background=[eval_benchmarks_def, base_models_def],
    metadata={"source_section": "Section 5, Table 1"},
)

l1_exact_dler7b = claim(
    "L1-Exact (a token-count length-penalty baseline) on DLER-7B achieves: average accuracy "
    "51.5% (−2.7pp from baseline 54.2%), average tokens 1,772 (−29% from baseline 2,481):\n\n"
    "| Benchmark | Acc (L1-Exact) | Tok (L1-Exact) |\n"
    "|-----------|---------------|---------------|\n"
    "| MATH500   | 92.0%         | 726           |\n"
    "| AIME24    | 46.5%         | 2,530         |\n"
    "| AIME25    | 30.8%         | 2,621         |\n"
    "| Minerva   | 26.2%         | 1,148         |\n"
    "| Olympiad  | 62.0%         | 1,833         |",
    title="L1-Exact baseline on DLER-7B: 29% token reduction but −2.7pp accuracy drop",
    background=[eval_benchmarks_def, base_models_def],
    metadata={"source_section": "Section 5, Table 1"},
)

# --- Key comparative claims ---

cib_pareto_dominates_l1 = claim(
    "CIB with semantic prior achieves a superior Pareto frontier over L1-based length penalties "
    "on DLER-7B: at similar compression levels (~29-32%), CIB $\\beta^+$ achieves 52.9% average "
    "accuracy (−1.3pp from baseline) versus L1-Exact's 51.5% (−2.7pp from baseline). "
    "CIB obtains higher accuracy at slightly higher compression (32% vs 29%) than L1-Exact, "
    "confirming that semantic cost better preserves essential reasoning.",
    title="CIB Pareto-dominates L1-Exact: better accuracy at equal or higher compression",
    metadata={"source_section": "Section 5"},
)

pred_cib_better = claim(
    "CIB with semantic prior predicts higher accuracy than L1-Exact at comparable compression "
    "levels because semantic cost selectively removes low-information tokens while preserving "
    "task-critical reasoning steps.",
    title="CIB prediction: semantic cost preserves accuracy better than length penalties",
    background=[semantic_prior_superiority_theory],
)

pred_l1_worse = claim(
    "L1-Exact predicts equal or greater compression at the cost of higher accuracy loss than "
    "CIB, because it cannot distinguish essential from redundant tokens.",
    title="L1-Exact prediction: accuracy loss higher than CIB at comparable compression",
    background=[budget_forcing_heuristic],
)

s_cib_explains = support(
    [pred_cib_better],
    cib_pareto_dominates_l1,
    reason=(
        "@pred_cib_better predicts CIB outperforms L1-Exact at comparable compression. "
        "Empirically, @dler_7b_cib_aggressive achieves 32% compression with −1.3pp accuracy, "
        "while @l1_exact_dler7b achieves only 29% compression with −2.7pp accuracy, "
        "confirming the prediction."
    ),
    prior=0.88,
)

s_l1_explains = support(
    [pred_l1_worse],
    cib_pareto_dominates_l1,
    reason=(
        "@pred_l1_worse predicts L1-Exact will underperform CIB on accuracy for similar "
        "compression. @l1_exact_dler7b shows −2.7pp vs CIB's −1.3pp at similar compression, "
        "matching the prediction that semantically blind penalties harm accuracy more."
    ),
    prior=0.6,
)

comp_cib_vs_l1 = compare(
    pred_cib_better, pred_l1_worse, cib_pareto_dominates_l1,
    reason=(
        "CIB's prediction (@pred_cib_better) that semantic cost preserves accuracy better "
        "matches the observed Pareto dominance in @cib_pareto_dominates_l1. L1-Exact's "
        "prediction (@pred_l1_worse) of higher accuracy loss is also confirmed, but this "
        "is the unfavorable outcome for L1-Exact. CIB explains the observed data better."
    ),
    prior=0.87,
)

abduction_cib_vs_l1 = abduction(
    s_cib_explains, s_l1_explains, comp_cib_vs_l1,
    reason="Both approaches attempt to explain the Pareto frontier behavior of DLER-7B results",
)

larger_prior_more_compression = claim(
    "Larger prior models ($Q_\\phi$) enable more aggressive compression. Using a 7B prior "
    "instead of 1.5B on DeepScaleR-1.5B increases token reduction from 29% to 41%, "
    "suggesting the 7B prior provides sharper estimates of semantic redundancy. "
    "However, accuracy degrades slightly (−0.7pp) with the 7B prior when using $\\beta^+$ "
    "settings tuned for the 1.5B prior, indicating hyperparameter re-tuning may be needed.",
    title="Larger prior model enables more aggressive compression but may require re-tuning",
    metadata={"source_section": "Section 5"},
)

strat_larger_prior = support(
    [deepscaler_cib_aggressive, deepscaler_7b_prior],
    larger_prior_more_compression,
    reason=(
        "@deepscaler_cib_aggressive shows 29% compression with 1.5B prior. "
        "@deepscaler_7b_prior shows 41% compression with 7B prior (same $\\beta^+$ setting). "
        "The 7B model provides more informative surprisal estimates, assigning higher cost "
        "to more tokens, leading to stronger compression pressure. The small accuracy drop "
        "(−0.7pp) suggests the $\\beta$ value optimal for 1.5B prior is too aggressive for 7B."
    ),
    prior=0.84,
)

# --- Information density analysis ---

info_density_result = claim(
    "Qualitative analysis of compressed traces shows CIB systematically eliminates three "
    "categories of 'cognitive bloat': (1) conversational scaffolding (unnecessary verbal "
    "parsing of inputs), (2) redundant verification loops (tautological self-checks), "
    "and (3) inefficient exploration (trial-and-error branches). Compressed traces exhibit "
    "information density $\\gtrsim 0.2$ nats per token versus $\\approx 0.1$ nats for "
    "length-penalized baselines, confirming semantic rather than arbitrary compression.",
    title="CIB compressed traces: higher information density, systematic bloat removal",
    metadata={"source_section": "Section 5, Qualitative Comparison"},
)

strat_deepscaler_conservative = support(
    [rl_objective_formulation],
    deepscaler_cib_conservative,
    reason=(
        "The CIB RL objective (@rl_objective_formulation) trained on DeepScaleR-1.5B with "
        "conservative $\\beta^- = 5\\times10^{-5}$ and 1.5B prior produces compressed traces "
        "while maintaining accuracy. The 25% token reduction with +1.2pp accuracy gain is "
        "consistent with the theory that semantic cost removes redundancy while preserving "
        "correctness-critical content."
    ),
    prior=0.9,
)

strat_dler7b_conservative = support(
    [rl_objective_formulation],
    dler_7b_cib_conservative,
    reason=(
        "The CIB RL objective (@rl_objective_formulation) trained on DLER-7B with conservative "
        "$\\beta^- = 5\\times10^{-5}$ and 7B prior achieves 8% token reduction with negligible "
        "accuracy change (+0.1pp). The 7B prior on a 7B model provides conservative but effective "
        "compression at this $\\beta$ level."
    ),
    prior=0.9,
)

strat_dler7b_aggressive = support(
    [rl_objective_formulation],
    dler_7b_cib_aggressive,
    reason=(
        "The CIB RL objective (@rl_objective_formulation) trained on DLER-7B with aggressive "
        "$\\beta^+ = 1.5\\times10^{-4}$ and 7B prior achieves 32% token reduction with −1.3pp "
        "accuracy loss. This represents a more aggressive point on the Pareto frontier, "
        "trading some accuracy for substantial token savings."
    ),
    prior=0.9,
)

strat_l1_baseline = support(
    [budget_forcing_heuristic],
    l1_exact_dler7b,
    reason=(
        "L1-Exact (@budget_forcing_heuristic illustrates the flat-tax approach) applies a "
        "uniform token-count penalty to DLER-7B. The result — 29% compression with −2.7pp "
        "accuracy loss — is empirically measured and serves as the comparison baseline for "
        "CIB performance on the same model."
    ),
    prior=0.92,
)

strat_info_density = support(
    [semantic_cost_advantage],
    info_density_result,
    reason=(
        "@semantic_cost_advantage predicts that semantic surprisal cost penalizes generic "
        "tokens more than task-specific ones. The qualitative categories of removed content "
        "(conversational scaffolding, verification loops, exploration) are precisely the "
        "patterns that a base language model $Q_\\phi$ would assign high probability (low "
        "surprisal, low cost) — they follow generic discourse patterns. The information "
        "density increase (≳0.2 vs ≈0.1 nats/token) quantifies this effect."
    ),
    prior=0.82,
)
