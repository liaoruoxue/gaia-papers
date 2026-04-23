"""Section 2: Taxonomy of Unsupervised RLVR Methods"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    intrinsic_rewards_definition,
    external_rewards_definition,
    urlvr_definition,
)

# ─── Certainty-Based Intrinsic Rewards ───────────────────────────────────────

certainty_rewards_overview = claim(
    "Certainty-based intrinsic rewards derive a reward signal from the model's own confidence "
    "(logits/probability distributions) over generated token sequences, rewarding high-confidence "
    "predictions. Five variants have been proposed:\n\n"
    "| Method | Estimator | Description |\n"
    "|--------|-----------|-------------|\n"
    "| RLIF | Self-Certainty | Average KL divergence from uniform distribution $U$ to model distribution |\n"
    "| EM-RL | Trajectory-Level Entropy | Average log probability per token (sequence log-prob) |\n"
    "| EM-RL, RENT | Token-Level Entropy | Negative average token-level entropy $-H(\\pi_\\theta)$ |\n"
    "| RLSC | Probability | Product of token probabilities (raw sequence probability) |\n"
    "| RLSF | Probability Disparity | Gap between top-1 and top-2 token probabilities at answer tokens |\n\n"
    "All variants reward high-confidence (low-entropy) predictions through different mathematical "
    "formalizations of confidence.",
    title="Certainty-based reward variants",
    metadata={"source_table": "artifacts/2603.08660.pdf, Table 1"},
)

ensemble_rewards_overview = claim(
    "Ensemble-based intrinsic rewards derive a reward from agreement (consistency) across multiple "
    "model rollouts for the same prompt, under the assumption that cross-sample consistency "
    "correlates with correctness. Key variants:\n\n"
    "| Method | Estimator | Notes |\n"
    "|--------|-----------|-------|\n"
    "| TTRL, SRT, ETTRL, SeRL, SQLM, R-Zero | Majority Voting | Binary reward: answer matches majority |\n"
    "| Co-Reward | Majority Voting across Rephrased Questions | Adds paraphrase consistency |\n"
    "| RLCCF | Self-consistency Weighted Voting | Multi-model collective weighted vote |\n"
    "| EMPO | Semantic Similarity / Clustering | Soft majority vote via semantic cluster size |\n"
    "| CoVo | Trajectory Consistency and Volatility | Combines consistency and reasoning volatility |\n\n"
    "All ensemble methods treat consistency across independent samples as a proxy for correctness.",
    title="Ensemble-based reward variants",
    metadata={"source_table": "artifacts/2603.08660.pdf, Table 2"},
)

intrinsic_rewards_limitation = claim(
    "Intrinsic reward methods are fundamentally limited by the model's internal state: their reward "
    "signal derives entirely from the model's own probability distributions and therefore cannot "
    "provide learning signals beyond what the model already knows. This creates an inherent ceiling "
    "on how far intrinsic URLVR can scale.",
    title="Intrinsic rewards scalability ceiling",
)

# ─── External Reward Methods ─────────────────────────────────────────────────

unlabeled_data_rewards = claim(
    "External URLVR methods using unlabeled data derive rewards from existing text corpora, "
    "treating the corpus itself as a source of latent ground truth. Examples include:\n\n"
    "- **RPT**: Rewards correct next-token predictions on unlabeled text, converting trillions "
    "of tokens into reward signals.\n"
    "- **TPT**: Predicts tokens through step-by-step reasoning before the prediction.\n"
    "- **RLPT**: Operates at the segment level rather than token level.\n"
    "- **RLP**: Trains models to generate reasoning chains before next-token prediction, rewarding "
    "the chain's information gain.\n"
    "- **DuPO**: Pairs a primary task with a dual reconstruction objective; model must recover "
    "the original input from its output.\n"
    "- **SEAL**: Models generate their own QA pairs from unlabeled contexts and are rewarded "
    "based on downstream self-supervised performance.\n\n"
    "These methods scale naturally with data availability, unbounded by human annotation capacity.",
    title="Unlabeled-data external reward methods",
)

gen_verify_asymmetry_rewards = claim(
    "External URLVR methods exploiting generation-verification asymmetry ground rewards in "
    "the observation that generating correct solutions requires deep search but verifying candidates "
    "is often cheap and deterministic. Examples:\n\n"
    "- **LADDER**: Indefinite integration; verifying an antiderivative needs only numerical evaluation.\n"
    "- **RLSR**: Countdown arithmetic puzzles; checking if an expression reaches a target is trivial.\n"
    "- **Absolute Zero (AZR)**: Code generation; execution against test cases is deterministic.\n"
    "- **DeepSeekMath-V2**: Formal theorem proving with Lean proof checker as verifier.\n"
    "- **AlphaProof**: Auto-formalized mathematical problems verified by Lean at scale.\n\n"
    "The external verifier does not degrade as the model improves, maintaining reward quality at scale.",
    title="Generation-verification asymmetry methods",
)

external_rewards_scalability = claim(
    "External reward methods escape the intrinsic reward ceiling through two complementary mechanisms: "
    "(1) unlabeled-data rewards grow with corpus size rather than model capability, providing fresh "
    "learning signal even after the model has absorbed its initialization knowledge; "
    "(2) generation-verification asymmetry rewards are grounded in external computation "
    "(compilers, proof assistants, simulators) that are entirely independent of the model's internal "
    "state and do not degrade as the model improves. Both mechanisms provide scalable rewards "
    "unbounded by human labeling capacity.",
    title="External rewards scalability advantage",
)

strat_external_scalable = support(
    [unlabeled_data_rewards, gen_verify_asymmetry_rewards],
    external_rewards_scalability,
    reason=(
        "The external rewards definition (see @external_rewards_definition) establishes that rewards "
        "come from outside the model's internal state. The unlabeled data paradigm "
        "(@unlabeled_data_rewards) shows rewards scale with data volume. The generation-verification "
        "asymmetry paradigm (@gen_verify_asymmetry_rewards) shows verifiers remain reliable "
        "regardless of model sophistication. Together these establish that external rewards are "
        "not bounded by model knowledge, unlike intrinsic methods."
    ),
    prior=0.88,
    background=[external_rewards_definition],
)

intrinsic_self_referential = claim(
    "Intrinsic URLVR reward methods generate all reward signals exclusively from the model's own "
    "output probability distributions. No information external to the model's internal state "
    "is consulted when computing the reward.",
    title="Intrinsic rewards are self-referential",
)

strat_intrinsic_ceiling = deduction(
    [intrinsic_self_referential],
    intrinsic_rewards_limitation,
    reason=(
        "If intrinsic rewards derive exclusively from the model's own distributions "
        "(@intrinsic_self_referential), then the information content of the reward signal is "
        "bounded by the information already encoded in the model. Any fact not already in the "
        "model's distribution cannot appear in the reward signal—the reward cannot teach the "
        "model about correctness it does not already implicitly know. This is a deductive "
        "consequence of the self-referential nature of intrinsic rewards, not an empirical claim."
    ),
    prior=0.97,
    background=[intrinsic_rewards_definition],
)
