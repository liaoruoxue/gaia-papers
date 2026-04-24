"""Section 4: Experimental Results"""

from gaia.lang import (
    claim, setting, support, deduction, abduction, induction,
    contradiction, compare,
)

from .motivation import (
    existing_selfplay_plateaus,
    conjecturer_collapse_hypothesis,
    quality_degrades,
    guide_hypothesis,
)
from .s3_algorithm import (
    setup_dataset,
    setup_sgs_roles,
    setup_rsolve,
    setup_rguide,
    setup_guide_rubric,
    setup_solver_objective,
    sgs_two_mechanisms,
    sgs_guide_scores_quality,
    sgs_conjecturer_conditions_on_unsolved,
    guide_sft_prevents_format_errors,
)

# ── Settings ──────────────────────────────────────────────────────────────────

setup_d3k_construction = setting(
    "The D3k dataset is constructed from Goedel-Pset-V1 (auto-formalized problems from "
    "NuminaMath-CoT) through four filtering steps: (1) remove problems with >50% pass rate "
    "on STP-7B (easy problems); (2) remove problems whose negation can be proved by "
    "Kimina-Prover-Preview and remove those proved >2/8 times (false + easy problems); "
    "(3) subsample to 5,000 problems; (4) use GPT-5 mini to remove problems labeled "
    "'unsolvable' due to formalization errors, yielding 3,323 problems [@Lin2025a; @Li2024].",
    title="D3k dataset construction procedure",
)

setup_d3k_composition = setting(
    "D3k contains 3,323 formal math problems in Lean4. By difficulty: roughly 80% are "
    "competition or undergraduate level. By area: Algebra (~35%), Number Theory (~25%), "
    "Geometry (~15%), and other areas. All problems are publicly released on HuggingFace "
    "at LukeBailey181Pub/D_3k.",
    title="D3k dataset composition",
)

setup_base_model = setting(
    "All experiments use DeepSeek-Prover-V2-7B (DSPv2-7B) [@Ren2025] as the base model "
    "for initializing Solver, Conjecturer, and Guide in SGS. DSPv2-7B was pre-trained with "
    "large-scale RL for Lean4, but has poor instruction-following capabilities, achieving "
    "51.5% correct Conjecturer output format before RL training.",
    title="Base model: DeepSeek-Prover-V2-7B",
)

setup_training_infra = setting(
    "Training infrastructure: up to 64 GPU workers (1 GPU, 32 GB memory each) for generation; "
    "up to 128 CPU workers (33 CPU threads each) for verification. Training uses a single "
    "H200 node with ZeRO Stage-2. Batch size: 3,323 (full dataset). Rollouts: k=8 per problem. "
    "Max sequence length: 8,192 tokens. Temperature: 1.0. Adam optimizer, β1=0.9, β2=0.95, "
    "gradient clipping at norm 1.0. Lean4 version 4.15.0, 200s timeout.",
    title="Training infrastructure and hyperparameters",
)

setup_scaling_law_form = setting(
    "Cumulative solve rate is modeled with the sigmoidal scaling law: "
    "RC = R0 + (A − R0) · 1 / (1 + (Cmid/C)^B), "
    "where RC is the cumulative solve rate at C model generations, R0 is the initial solve rate, "
    "A is the asymptotic cumulative solve rate, Cmid is the curve midpoint, and B controls the "
    "rate of approach to asymptote. Parameters A, Cmid, B are fit by minimizing sum of squared "
    "residuals using SciPy's curve_fit. The initial solve rate R0 is fixed to the first observed "
    "value (not a free parameter) [@Khatri2025; @Ruan2024].",
    title="Sigmoidal scaling law for cumulative solve rate",
)

setup_scaling_law_robustness = setting(
    "The fitted scaling law is validated by removing 10%, 20%, and 30% of final training data "
    "and checking stability. With 50% random data drop (100 independent fits), the standard "
    "deviation of fitted asymptote is 1.1%. Differences below 1.1% in fitted asymptotes are "
    "treated cautiously. The scaling law is treated as a useful additional metric, not a "
    "substitute for long-run empirical performance.",
    title="Scaling law robustness and uncertainty",
)

# ── Claims: RL Baselines ───────────────────────────────────────────────────────

rl_baselines_comparison = claim(
    "Three RL baselines are benchmarked on D3k: (1) REINFORCE1/2: achieves 60.3% fitted "
    "asymptotic cumulative solve rate; (2) Expert Iteration (EI): achieves 60.0% asymptotic "
    "solve rate; (3) CISPO: achieves 57.5% asymptotic solve rate. REINFORCE1/2 performs best. "
    "CISPO performs worst due to entropy collapse. Learning rates were individually tuned: "
    "CISPO at 1e-6, EI and REINFORCE1/2 at 3e-6.",
    title="RL baseline comparison on D3k",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 4"},
)

cispo_entropy_collapse = claim(
    "CISPO, when used as a standalone RL objective on D3k, undergoes rapid entropy collapse. "
    "The Solver's average entropy drops quickly toward near-zero, concentrating the distribution "
    "of problem solve rates at 0 and 1. This makes CISPO unsuitable for long-running self-play "
    "because a near-deterministic Solver starves the Conjecturer of training signal.",
    title="CISPO undergoes entropy collapse as RL baseline",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 4 and 11"},
)

reinforce_half_best_baseline = claim(
    "REINFORCE1/2 is the best-performing RL baseline on D3k, achieving a fitted asymptotic "
    "cumulative solve rate of 60.3%, compared to 60.0% for Expert Iteration and 57.5% for "
    "CISPO. REINFORCE1/2 is selected as the Solver objective for SGS.",
    title="REINFORCE1/2 selected as best RL baseline (60.3% asymptotic solve rate)",
)

strat_reinforce_best = support(
    [rl_baselines_comparison, cispo_entropy_collapse],
    reinforce_half_best_baseline,
    reason=(
        "Empirical comparison of all three baselines (@rl_baselines_comparison) shows "
        "REINFORCE1/2 at 60.3% dominates Expert Iteration (60.0%) and CISPO (57.5%). "
        "CISPO's poor performance is explained by its entropy collapse (@cispo_entropy_collapse). "
        "REINFORCE1/2 avoids this collapse and thus provides the strongest foundation "
        "for the Conjecturer in SGS [@Bailey2026]."
    ),
    prior=0.93,
)

# ── Claims: Main SGS Result ────────────────────────────────────────────────────

sgs_higher_asymptotic_rate = claim(
    "SGS achieves a fitted asymptotic cumulative solve rate of 67.1% on D3k, compared to "
    "60.3% for the REINFORCE1/2 baseline — a 7% higher asymptotic solve rate. Both are "
    "fitted using the sigmoidal scaling law to runs of 8M+ total model generations.",
    title="SGS asymptotic solve rate 67.1% vs RL baseline 60.3% (7% gain)",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 1 and 6"},
)

alt_sgs_no_gain = claim(
    "SGS's improvements over the RL baseline could be due to increased compute or "
    "hyperparameter differences rather than the Guide and problem-conditioning mechanisms, "
    "with the Guide component providing no additional benefit beyond the extra data.",
    title="Alternative: SGS gains not from self-guidance but from more compute",
)

pred_sgs = claim(
    "SGS (with Guide + problem conditioning) predicts a 7% higher asymptotic solve rate "
    "than RL alone, reaching 67.1%, because the Guide steers the Conjecturer away from "
    "degenerate problems and toward the Solver's learning frontier.",
    title="SGS predicts higher asymptotic solve rate via guided conjecturer",
)

pred_alt_sgs = claim(
    "If SGS's gains were purely from extra training data without Guide quality control, "
    "the 'No Guide' ablation (which also uses synthetic problems but without Rguide) would "
    "achieve a similar asymptotic solve rate to full SGS.",
    title="Alternative predicts No Guide would match SGS solve rate",
)

comp_sgs_vs_alt = compare(
    pred_sgs, pred_alt_sgs, sgs_higher_asymptotic_rate,
    reason=(
        "The empirical result shows SGS at 67.1% vs No Guide at 65.5%, a 1.6% gap that "
        "exceeds the 1.1% scaling law uncertainty threshold. This shows the Guide provides "
        "genuine benefit beyond extra synthetic data. Furthermore, No Guide's Conjecturer "
        "collapses to disjunctive problems (Figure 2), confirming that pass-rate-only reward "
        "is insufficient. SGS explains the observation better."
    ),
    prior=0.82,
)

s_sgs_h = support(
    [sgs_two_mechanisms, guide_hypothesis],
    sgs_higher_asymptotic_rate,
    reason=(
        "SGS's two anti-collapse mechanisms (@sgs_two_mechanisms) — Guide scoring and "
        "problem conditioning — are predicted to keep the Conjecturer productive over long "
        "runs. The @guide_hypothesis asserts that LLMs can assess subproblem usefulness. "
        "These together predict that SGS will sustain improvement beyond what RL alone achieves, "
        "consistent with the empirically observed 67.1% asymptotic rate [@Bailey2026]."
    ),
    prior=0.82,
)

s_alt_sgs = support(
    [alt_sgs_no_gain],
    sgs_higher_asymptotic_rate,
    reason=(
        "If extra synthetic data without quality control were sufficient, the No Guide variant "
        "would match or approach SGS performance. The No Guide variant gets more solvable "
        "synthetic problems per iteration (Figure 6 right), which under this alternative "
        "should produce at least equal performance. The alternative partially explains the "
        "observed gain but predicts smaller difference between SGS and No Guide."
    ),
    prior=0.35,
)

abduction_sgs_main = abduction(
    s_sgs_h, s_alt_sgs, comp_sgs_vs_alt,
    reason="Both self-guidance and more-data hypotheses attempt to explain SGS's superior solve rate",
)

sgs_surpasses_671b = claim(
    "At 6.3 million total model generations, SGS applied to the 7B parameter "
    "DeepSeek-Prover-V2-7B model exceeds the pass@4 of the much larger 671B parameter "
    "DeepSeek-Prover-V2-671B model on D3k. This demonstrates that sustained self-play "
    "training can close the gap between a 7B and 671B parameter model.",
    title="SGS 7B surpasses DSPv2-671B pass@4 at 6.3M generations",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 1"},
)

strat_sgs_surpasses_671b = support(
    [sgs_higher_asymptotic_rate],
    sgs_surpasses_671b,
    background=[setup_base_model],
    reason=(
        "The sustained improvement of SGS to 67.1% asymptotic solve rate (@sgs_higher_asymptotic_rate) "
        "on a 7B model (@setup_base_model), combined with sufficient compute (6.3M generations), "
        "yields a cumulative solve rate that exceeds the pass@4 benchmark of the 671B counterpart. "
        "The 671B model is used as a yardstick of compute-efficient upper bound for a single "
        "inference run, making this comparison meaningful [@Bailey2026; @Ren2025]."
    ),
    prior=0.90,
)

sgs_progress_on_never_solved = claim(
    "Of the 1,346 problems that the RL baseline never solves in 4M generations, SGS solves "
    "almost 10% of them after 8M generations. The RL baseline solves 0% of these problems. "
    "SGS shows steady and sustained progress on these hard problems from the very beginning "
    "of training.",
    title="SGS solves ~10% of problems RL never solves (1,346 hard problems)",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 13"},
)

strat_progress_hard = support(
    [sgs_conjecturer_conditions_on_unsolved, sgs_guide_scores_quality],
    sgs_progress_on_never_solved,
    reason=(
        "Conditioning on unsolved problems (@sgs_conjecturer_conditions_on_unsolved) ensures "
        "that synthetic problems are generated specifically for the hard, unsolved problems. "
        "The Guide (@sgs_guide_scores_quality) ensures these synthetic problems are relevant "
        "and well-formed stepping stones. Together, this creates a curriculum targeted at "
        "exactly the problems that pure RL cannot reach, explaining steady progress on the "
        "hardest 1,346 problems [@Bailey2026]."
    ),
    prior=0.83,
)

sgs_outperforms_stp = claim(
    "SGS outperforms STP (Self-play Theorem Prover, the closest related self-play method for "
    "Lean4 theorem proving [@Dong2025]) after 1M total model generations, with superior "
    "scaling behavior over longer runs.",
    title="SGS outperforms STP (closest prior Lean4 self-play) after 1M generations",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 12"},
)

strat_sgs_vs_stp = support(
    [sgs_outperforms_stp],
    sgs_higher_asymptotic_rate,
    reason=(
        "STP [@Dong2025] is the most closely related Lean4 self-play baseline. The fact that "
        "SGS outperforms STP after 1M generations and shows superior scaling (@sgs_outperforms_stp) "
        "provides additional evidence of the same 7% asymptotic advantage over competing methods. "
        "Both comparisons (vs RL baseline and vs STP) confirm the superior scaling of SGS [@Bailey2026]."
    ),
    prior=0.85,
)

# ── Claims: Training Dynamics ─────────────────────────────────────────────────

solver_improves_steadily = claim(
    "The Solver's pass@8 on target statements increases steadily over 200 SGS iterations "
    "from approximately 42.5% to approximately 60% without catastrophic forgetting. "
    "The Solver does not suffer from distributional collapse over the course of training.",
    title="Solver pass@8 increases steadily over 200 iterations without forgetting",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 3"},
)

conjecturer_reward_stable = claim(
    "The Conjecturer's average reward increases across SGS training, driven primarily by a "
    "stable Guide reward (Rguide begins high and critically remains stable throughout training) "
    "and an increasing solve-rate reward (Rsolve increases during training). The overall "
    "Conjecturer reward varies between 0 and 7.",
    title="Conjecturer reward increases: stable Rguide, rising Rsolve",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 3"},
)

strat_rguide_stable = support(
    [guide_sft_prevents_format_errors],
    conjecturer_reward_stable,
    background=[setup_guide_rubric],
    reason=(
        "The Guide is initialized with a well-calibrated prompt and fine-tuned for reliable "
        "output formatting (@guide_sft_prevents_format_errors, @setup_guide_rubric). Because "
        "the Guide is not further trained during SGS, its scoring criteria remain stable. The "
        "initial Conjecturer prompt already provides a good prior for producing relevant problems, "
        "so Rguide begins high and the Guide's stability ensures it remains high throughout "
        "training [@Bailey2026]."
    ),
    prior=0.82,
)

synth_progress_toward_target = claim(
    "As the Solver approaches solving a target problem, more synthetic problems generated for "
    "that target are suitable for Solver training (i.e., have non-zero, non-trivial solve rates). "
    "For the final 300 target theorems solved by SGS, the fraction of synthetic problems trained "
    "on increases monotonically across ten equally-sized buckets of pre-solve iterations.",
    title="Synthetic problem solve rate increases as Solver approaches target",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 5"},
)

strat_synth_progress = support(
    [sgs_conjecturer_conditions_on_unsolved, solver_improves_steadily],
    synth_progress_toward_target,
    reason=(
        "The Conjecturer conditions on unsolved problems (@sgs_conjecturer_conditions_on_unsolved), "
        "so as the Solver improves (@solver_improves_steadily) and gets closer to solving "
        "a target, it gains the ability to solve increasingly difficult synthetic variants "
        "of that target. This creates a self-reinforcing feedback loop: approaching the target "
        "unlocks more training signal from synthetic problems, accelerating convergence [@Bailey2026]."
    ),
    prior=0.83,
)

# ── Claims: Ablations ─────────────────────────────────────────────────────────

no_problem_cond_fails = claim(
    "Without problem conditioning (Conjecturer prompted with a fixed generic prompt instead "
    "of the unsolved target problem, with only Rsolve reward), the Conjecturer produces many "
    "solvable problems but these are completely useless for solving target problems. "
    "The 'No Problem Conditioning' ablation does not outperform the RL baseline "
    "(60.3% asymptotic solve rate), despite generating more solvable synthetic problems.",
    title="No Problem Conditioning ablation fails to improve over RL baseline",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 6"},
)

strat_no_cond_fails = support(
    [no_problem_cond_fails],
    quality_degrades,
    background=[setup_rsolve],
    reason=(
        "The No Problem Conditioning ablation (@no_problem_cond_fails) directly demonstrates "
        "that a pass-rate-only reward (@setup_rsolve) without target conditioning produces "
        "many solvable problems that provide no benefit for target solve rate. This confirms "
        "that synthetic problem quality (relevance to targets) degrades when the reward does "
        "not incorporate target conditioning or quality signals [@Bailey2026]."
    ),
    prior=0.90,
)

no_guide_lower_performance = claim(
    "The 'No Guide' ablation (SGS without Rguide, using only Rsolve for the Conjecturer) "
    "achieves a fitted asymptotic cumulative solve rate of 65.5% on D3k, lower than full "
    "SGS at 67.1%. However, No Guide substantially outperforms the RL baseline (60.3%) "
    "and No Problem Conditioning. The No Guide Conjecturer produces more solvable synthetic "
    "problems than SGS, yet achieves lower target solve rates.",
    title="No Guide ablation: 65.5% solve rate vs SGS 67.1%",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 6"},
)

no_guide_conjecturer_collapse = claim(
    "Without the Guide, the 'No Guide' Conjecturer collapses starting around 4M generations: "
    "the percentage of generated problems with disjunctive (OR) conclusions rises above 80% "
    "(vs. <10% in D3k baseline), and the average conclusion length grows to nearly 10 times "
    "the D3k average. These are inelegant, complex problems that hack the solve-rate reward "
    "without being useful for solving target theorems.",
    title="No Guide Conjecturer collapse: >80% disjunctive conclusions, 10x longer",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 2"},
)

strat_guide_prevents_collapse = support(
    [sgs_guide_scores_quality],
    no_guide_conjecturer_collapse,
    background=[setup_rguide],
    reason=(
        "The Guide (@sgs_guide_scores_quality) scores problems low if they are inelegant "
        "or have redundant premises (@setup_rguide). Without this signal, the Conjecturer "
        "is free to exploit the solve-rate reward by producing long disjunctive statements "
        "that are technically solvable (each disjunct may be simple) but are artificial "
        "constructions unrelated to the target problem. The observed collapse pattern "
        "(disjunctive conclusions, 10x length increase) is the empirical confirmation of "
        "this mechanism [@Bailey2026]."
    ),
    prior=0.88,
)

strat_no_guide_lower = support(
    [no_guide_conjecturer_collapse, no_guide_lower_performance],
    conjecturer_collapse_hypothesis,
    reason=(
        "The No Guide ablation (@no_guide_lower_performance) shows that without the Guide, "
        "despite producing more solvable synthetic problems, the Conjecturer collapses to "
        "degenerate problems (@no_guide_conjecturer_collapse). This confirms the core "
        "hypothesis that Conjecturer reward hacking (@conjecturer_collapse_hypothesis) "
        "is the mechanism causing lower performance: more data does not help if the data "
        "quality degrades [@Bailey2026]."
    ),
    prior=0.88,
)

frozen_conjecturer_suboptimal = claim(
    "A 'Frozen Conjecturer' ablation (Conjecturer not trained, fixed distribution, analogous "
    "to AlphaProof's approach [@Hubert2025]) outperforms the RL baseline and No Problem "
    "Conditioning, but is inferior to both full SGS (67.1%) and No Guide (65.5%). The number "
    "of solvable synthetic problems per iteration decreases over time, showing the Solver "
    "quickly saturates the fixed Conjecturer's distribution, reverting the algorithm to RL alone.",
    title="Frozen Conjecturer suboptimal: Solver saturates fixed distribution",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 6"},
)

strat_frozen_suboptimal = support(
    [frozen_conjecturer_suboptimal],
    existing_selfplay_plateaus,
    background=[setup_rsolve],
    reason=(
        "The frozen Conjecturer ablation (@frozen_conjecturer_suboptimal) shows that a "
        "static problem distribution leads the Solver to saturate it, after which the "
        "algorithm reverts to RL alone and plateaus. This directly demonstrates one pathway "
        "to learning plateaus in self-play: when the Conjecturer cannot adapt to the improving "
        "Solver, the benefit of synthetic problems vanishes [@Bailey2026]."
    ),
    prior=0.87,
)

# ── Claims: Solver Entropy and CISPO in SGS ────────────────────────────────────

cispo_solver_kills_conjecturer = claim(
    "When CISPO is used as the Solver objective in SGS (instead of REINFORCE1/2), the Solver's "
    "entropy collapses rapidly, concentrating problem solve rates at 0 and 1. This starves "
    "the Conjecturer of training signal: problems with solve rate 0 or 1 receive Rsolve = 0. "
    "The Conjecturer cannot learn, and SGS with CISPO Solver achieves essentially the same "
    "asymptotic performance as standalone CISPO (57.5%), not the 67.1% of SGS with REINFORCE1/2.",
    title="CISPO Solver entropy collapse starves Conjecturer in SGS",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 7"},
)

reinforce_half_stable_entropy = claim(
    "With REINFORCE1/2 as the Solver objective in SGS, the Solver's entropy remains stable "
    "throughout training. The Conjecturer can produce problems with a spread of intermediate "
    "solve rates, providing sufficient training signal. The presence of synthetic problems "
    "appears to stabilize Solver entropy in a positive feedback loop.",
    title="REINFORCE1/2 maintains stable Solver entropy, enabling Conjecturer learning",
    metadata={"source_figure": "artifacts/2604.20209.pdf, Figure 7"},
)

entropy_conjecturer_coupling = claim(
    "There is a critical coupling between Solver entropy and Conjecturer learning: a "
    "near-deterministic Solver (entropy ≈ 0) concentrates solve rates at 0/1, giving the "
    "Conjecturer zero reward and preventing it from learning. Conversely, a Solver with "
    "stable entropy produces a spread of solve rates, enabling the Conjecturer to receive "
    "and learn from gradient signal. This coupling is identified as a key constraint on "
    "successful LLM self-play algorithm design.",
    title="Solver entropy-Conjecturer learning coupling is key to SGS success",
)

strat_entropy_coupling = support(
    [cispo_solver_kills_conjecturer, reinforce_half_stable_entropy],
    entropy_conjecturer_coupling,
    background=[setup_rsolve],
    reason=(
        "The CISPO ablation (@cispo_solver_kills_conjecturer) directly shows the failure mode: "
        "entropy collapse → solve rates concentrated at 0/1 → Rsolve = 0 for all synthetic "
        "problems (@setup_rsolve) → Conjecturer gets no gradient → no self-play improvement. "
        "The REINFORCE1/2 result (@reinforce_half_stable_entropy) confirms the converse: "
        "stable entropy → spread of solve rates → Conjecturer learns. The causal structure "
        "is: Solver objective choice → entropy → Conjecturer reward signal → self-play "
        "effectiveness [@Bailey2026]."
    ),
    prior=0.87,
)
