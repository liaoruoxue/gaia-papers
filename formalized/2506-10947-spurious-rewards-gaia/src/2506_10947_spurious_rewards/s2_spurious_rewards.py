"""Section 2: Spurious Rewards Yield Significant RLVR Gains"""

from gaia.lang import (
    claim, setting,
    support, deduction, abduction, induction, compare,
    contradiction,
)

from .motivation import (
    setup_rlvr, setup_models, setup_benchmarks, setup_reward_types,
    claim_rlvr_improves_qwen, claim_spurious_fails_non_qwen,
    claim_pretraining_hypothesis,
)

# ── Detailed empirical results ─────────────────────────────────────────────────

claim_qwen7b_math500_results = claim(
    "After 300 steps of GRPO training on Qwen2.5-Math-7B (initial MATH-500 "
    "accuracy: 49.4%), MATH-500 accuracy gains by reward type are:\n\n"
    "| Reward Type | MATH-500 Gain (pp) |\n"
    "|-------------|--------------------|\n"
    "| Ground Truth | +29.1 |\n"
    "| Majority Vote | +27.1 |\n"
    "| Incorrect Label | +24.1 |\n"
    "| Random ($\\gamma=0.5$) | +21.4 |\n"
    "| Format | +13.8 |\n\n"
    "All reward types produce significant improvements within the first 50 "
    "training steps.",
    title="Qwen2.5-Math-7B MATH-500 gains across all reward types",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 2a"},
)

claim_qwen7b_amc_results = claim(
    "After 300 steps of GRPO training on Qwen2.5-Math-7B on AMC (average@8), "
    "gains by reward type approach those of ground truth rewards. Format, "
    "incorrect, and random rewards yield approximately 13.8%, 24.1%, and 21.4% "
    "gains respectively, approaching the ~27–29% improvement from majority vote "
    "and ground truth labels.",
    title="Qwen2.5-Math-7B AMC gains across reward types",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 2a"},
)

claim_qwen15b_results = claim(
    "On Qwen2.5-Math-1.5B (a smaller math-specialized Qwen model), all reward "
    "types also yield significant improvements on MATH-500. One exception: "
    "random reward gains are slower (improvement appears after ~100 steps "
    "rather than ~50 steps) and smaller on AMC (only +4.9%). This suggests "
    "smaller models are less able to exploit random rewards, possibly due to "
    "retaining less pretraining knowledge to surface.",
    title="Qwen2.5-Math-1.5B also gains from spurious rewards, but random reward slower",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 2b"},
)

claim_aime_results = claim(
    "On AIME 2024 (harder math Olympiad benchmark, average@8), Qwen2.5-Math-7B "
    "shows significant gains from spurious rewards: format reward (+10.3%), "
    "incorrect and random rewards both (+10.2%), approaching ground truth "
    "rewards (+15.3%). However, on AIME 2025 (created after all models' "
    "knowledge cutoff), ground truth labels show a clear advantage, and spurious "
    "rewards yield only -0.4% to +4.5% — suggesting AIME25 questions are "
    "more out-of-distribution for Qwen's pretrained knowledge.",
    title="AIME results: spurious rewards effective on in-distribution (2024) but not out-of-distribution (2025)",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 14"},
)

claim_random_gamma_robustness = claim(
    "Random reward with Bernoulli($\\gamma$) for $\\gamma \\in "
    "\\{0.7, 0.5, 0.3, 0.001\\}$ all yield significant MATH-500 performance "
    "gains on Qwen2.5-Math-7B, converging to accuracy improvements of "
    "approximately 15–20 percentage points after some period of initial random "
    "walk. Only $\\gamma = 0$ (which analytically yields zero gradient) fails "
    "to produce gains. Convergence speed varies with $\\gamma$, but all "
    "non-zero configurations reach similar high-performance regimes.",
    title="Random reward gains are robust across probability values gamma in {0.001, 0.3, 0.5, 0.7}",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 10"},
)

# ── Reasoning about why spurious rewards work ─────────────────────────────────

claim_incorrect_reward_mechanism = claim(
    "Two hypothesized mechanisms allow incorrect labels to provide effective "
    "training signals in RLVR. First, many majority-vote-selected incorrect "
    "labels remain numerically close to the ground truth values, providing "
    "positive reinforcement for largely correct reasoning chains. Second, "
    "receiving reward requires the model to successfully extract and evaluate "
    "a generated boxed answer against the incorrect label, which implicitly "
    "requires a degree of correct format-following and answer extraction.",
    title="Hypothesized mechanisms: incorrect rewards provide implicit format + near-correct signal",
)

claim_format_reward_effectiveness = claim(
    "Format reward (rewarding any response that contains a non-empty \\\\boxed{} "
    "expression, regardless of correctness) produces +13.8 pp gain on MATH-500 "
    "for Qwen2.5-Math-7B. This reward provides no information about mathematical "
    "correctness but incentivizes prompt-following behavior (the \\\\boxed{} "
    "format is specified in Qwen2.5-Math's system prompt).",
    title="Format reward (+13.8 pp on MATH-500) provides no correctness signal, only format signal",
)

# ── Strategies: ground truth vs spurious (abduction) ─────────────────────────

# For the abduction: hypothesis = RLVR surfaces pretraining, alt = RLVR teaches new knowledge
alt_rlvr_teaches_new = claim(
    "RLVR teaches models genuinely new reasoning capabilities through the "
    "reward signal, and any reward signal that provides some useful gradient "
    "direction will produce proportional improvements in reasoning ability.",
    title="Alternative hypothesis: RLVR teaches new reasoning via reward gradient direction",
)

s_h_pretraining = support(
    [claim_pretraining_hypothesis],
    claim_rlvr_improves_qwen,
    reason=(
        "If RLVR surfaces pretraining representations (@claim_pretraining_hypothesis), "
        "then spurious rewards that provide no useful correctness signal can still "
        "trigger improvements by concentrating the model on its pre-existing high-prior "
        "behaviors. This predicts that @claim_rlvr_improves_qwen — large gains even "
        "from random and incorrect rewards — would be observed for models with strong "
        "pretrained math reasoning patterns."
    ),
    prior=0.85,
)

s_alt_teaches = support(
    [alt_rlvr_teaches_new],
    claim_rlvr_improves_qwen,
    reason=(
        "Under @alt_rlvr_teaches_new, even spurious rewards might provide some "
        "learning signal if by chance the reward correlates weakly with good "
        "responses. However, this hypothesis predicts that truly random rewards "
        "(zero correlation) should provide no improvement, and that improvements "
        "would scale with reward informativeness."
    ),
    prior=0.3,
)

pred_pretraining = claim(
    "The pretraining-surfacing hypothesis predicts that: (a) random rewards with "
    "zero informativeness about correctness still yield gains; (b) gains are "
    "model-family-specific (dependent on pretraining); (c) gains are robust "
    "across different random-reward probabilities.",
)

pred_teaches = claim(
    "The 'RLVR teaches new reasoning' hypothesis predicts that: (a) reward "
    "informativeness should directly determine gain magnitude; (b) random reward "
    "with zero informativeness should yield minimal or no gain; (c) gains should "
    "generalize across model families given similar architecture.",
)

comp_hypotheses = compare(
    pred_pretraining, pred_teaches, claim_rlvr_improves_qwen,
    reason=(
        "The observation of +21.4 pp gain from random reward ($\\gamma=0.5$) and "
        "robustness across $\\gamma \\in \\{0.001, 0.3, 0.5, 0.7\\}$ "
        "(@claim_random_gamma_robustness) directly falsifies the 'teaches new "
        "reasoning' hypothesis (which predicts random reward should not work). "
        "The pretraining hypothesis better explains all observations: gains, "
        "model-family specificity, and gamma-robustness."
    ),
    prior=0.85,
)

abd_rlvr_mechanism = abduction(
    s_h_pretraining, s_alt_teaches, comp_hypotheses,
    reason=(
        "Both hypotheses attempt to explain why RLVR with spurious rewards "
        "improves performance. The abduction selects the explanation that better "
        "accounts for the observed pattern of gains across reward types and "
        "model families."
    ),
)

strat_qwen7b_gains = support(
    [claim_qwen7b_math500_results],
    claim_rlvr_improves_qwen,
    reason=(
        "Following the experimental setup (@setup_rlvr, @setup_models), "
        "Qwen2.5-Math-7B was trained with GRPO for 300 steps under each of the "
        "reward types defined in @setup_reward_types. Performance was evaluated "
        "on MATH-500 (@setup_benchmarks). The numerical results in "
        "@claim_qwen7b_math500_results are directly read from Figure 2a and "
        "Figure 1 of the paper. [@Shao2025spurious]"
    ),
    prior=0.95,
    background=[setup_rlvr, setup_reward_types, setup_models],
)

strat_aime_ood = support(
    [claim_aime_results],
    claim_pretraining_hypothesis,
    reason=(
        "The pattern in @claim_aime_results — spurious rewards work on "
        "AIME 2024 but not AIME 2025 — is highly consistent with "
        "@claim_pretraining_hypothesis. AIME 2025 questions (post-cutoff) "
        "cannot be solved by surfacing pretrained knowledge, so spurious "
        "rewards (which work by eliciting pretraining) lose their effectiveness. "
        "Ground truth rewards retain advantage on out-of-distribution problems "
        "because they provide genuine learning signal."
    ),
    prior=0.8,
    background=[setup_benchmarks],
)
