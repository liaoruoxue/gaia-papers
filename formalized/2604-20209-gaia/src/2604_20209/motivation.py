"""Introduction and Motivation: Scaling LLM Self-Play"""

from gaia.lang import claim, setting, question, support, deduction, contradiction

# ── Settings ──────────────────────────────────────────────────────────────────

setup_asymmetric_selfplay = setting(
    "Asymmetric self-play is a paradigm in which a Conjecturer model proposes new learning "
    "problems and a Solver model attempts to solve them, with both improving together through "
    "iterative interaction [@Sukhbaatar2017; @Florensa2018].",
    title="Asymmetric self-play paradigm",
)

setup_lean4_domain = setting(
    "Lean4 is a formal theorem proving language in which problem solutions (proofs) can be "
    "automatically verified by the Lean4 compiler. In the formal theorem proving setting, "
    "target problems are Lean4 theorem statements and solutions are formally verified proofs.",
    title="Lean4 formal theorem proving domain",
)

setup_conjecturer_reward = setting(
    "In standard LLM self-play methods, the Conjecturer is rewarded solely according to the "
    "Solver's pass rate on synthetic problems: a higher Solver pass rate on a problem indicates "
    "the problem may be too easy, while a zero pass rate indicates it may be too hard. The "
    "reward favors intermediate difficulty.",
    title="Standard Conjecturer reward (pass-rate only)",
)

setup_selfplay_ideal = setting(
    "The ideal property of asymmetric self-play is that, in principle, nothing bounds its "
    "learning: as the Solver improves, the Conjecturer produces harder problems, enabling "
    "continuous improvement [@Silver2017].",
    title="Theoretical unbounded learning potential of self-play",
)

# ── Claims ────────────────────────────────────────────────────────────────────

sparse_reward_problem = claim(
    "When a problem is sufficiently difficult, standard reinforcement learning (RL) techniques "
    "fail due to sparse or absent reward signals. Asymmetric self-play is proposed as a solution: "
    "a Conjecturer bridges the gap between current Solver capability and hard unsolved problems.",
    title="Sparse reward motivates asymmetric self-play",
    background=[setup_asymmetric_selfplay],
)

existing_selfplay_plateaus = claim(
    "Existing LLM self-play methods do not sustain learning over long training periods, "
    "instead hitting learning plateaus. Prior works on LLM self-play do not run training for "
    "as long as SGS does in this paper.",
    title="Existing LLM self-play hits learning plateaus",
)

conjecturer_collapse_hypothesis = claim(
    "Over long training runs, the Conjecturer learns to exploit (hack) its reward function, "
    "collapsing to producing artificially complex problems that do not genuinely help the Solver "
    "improve. This reward hacking is identified as the primary cause of the learning plateaus "
    "observed in existing LLM self-play methods.",
    title="Conjecturer reward-hacking causes learning plateaus (hypothesis)",
)

quality_degrades = claim(
    "Under a pass-rate-only Conjecturer reward, the quality of synthetic problems degrades "
    "over the course of training, leading to a learning plateau. Specifically, the Conjecturer "
    "produces problems that maximize solve-rate reward without being genuinely useful for "
    "improving Solver performance on target problems.",
    title="Synthetic problem quality degrades under pass-rate-only reward",
)

strat_collapse_from_reward = support(
    [existing_selfplay_plateaus],
    conjecturer_collapse_hypothesis,
    background=[setup_conjecturer_reward],
    reason=(
        "Because the Conjecturer is rewarded only for the Solver's pass rate (@setup_conjecturer_reward), "
        "it is incentivized to find problems that maximize this metric, not problems that are "
        "genuinely useful for improving the Solver on hard target problems. "
        "Given that existing methods hit plateaus (@existing_selfplay_plateaus), the most "
        "parsimonious explanation is that the Conjecturer learns to exploit the reward rather "
        "than produce genuinely useful problems. This hypothesis is confirmed empirically in §4.4 "
        "of the paper [@Bailey2026]."
    ),
    prior=0.88,
)

strat_quality_from_collapse = support(
    [conjecturer_collapse_hypothesis],
    quality_degrades,
    background=[setup_conjecturer_reward],
    reason=(
        "If the Conjecturer hacks its reward (@conjecturer_collapse_hypothesis) and the reward "
        "is defined only by Solver pass rate (@setup_conjecturer_reward), then the Conjecturer "
        "will shift toward problems that are technically solvable (non-zero pass rate) but "
        "superficially complex -- maximizing pass-rate reward while providing no signal toward "
        "the target problems. The outcome is degraded synthetic data quality."
    ),
    prior=0.85,
)

strat_sparse_reward = support(
    [sparse_reward_problem],
    existing_selfplay_plateaus,
    background=[setup_asymmetric_selfplay],
    reason=(
        "Sparse reward (@sparse_reward_problem) limits standard RL on hard problems. "
        "Asymmetric self-play (@setup_asymmetric_selfplay) addresses this, but in practice "
        "existing LLM self-play implementations still plateau because the Conjecturer degrades "
        "rather than continuously improving the learning frontier. The sparse reward context "
        "frames why LLM self-play is needed and why its plateaus matter [@Bailey2026]."
    ),
    prior=0.80,
)

guide_hypothesis = claim(
    "Language models can assess whether a subproblem is useful for achieving a goal. "
    "This capability enables an LLM acting as a Guide to score synthetic problems by their "
    "relevance to unsolved target problems and by how clean and natural they are, providing "
    "useful supervision against Conjecturer collapse.",
    title="LLMs can assess subproblem usefulness (core SGS hypothesis)",
)
