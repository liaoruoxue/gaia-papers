"""Introduction and Motivation: Unsupervised RLVR and the Supervision Bottleneck"""

from gaia.lang import claim, setting, question, support, deduction

# --- Research context ---

supervised_rlvr_success = claim(
    "Supervised Reinforcement Learning with Verifiable Rewards (RLVR) has driven recent "
    "breakthroughs in large language model (LLM) reasoning capability. Models including "
    "DeepSeek-R1, Gemini 2.5, and the Qwen3 series achieve strong performance on mathematics, "
    "coding, and science benchmarks by scaling supervised RLVR with ground-truth labels.",
    title="Supervised RLVR success",
)

supervision_bottleneck = claim(
    "Supervised RLVR faces a fundamental scalability bottleneck: obtaining ground-truth labels "
    "requires prohibitively high human costs, and as models reach or surpass human expertise in "
    "specialized domains, obtaining reliable ground truth supervision becomes increasingly infeasible. "
    "This creates a ceiling for further capability improvement via supervised RLVR.",
    title="Supervision scalability bottleneck",
)

urlvr_definition = setting(
    "Unsupervised RLVR (URLVR) is defined as reinforcement learning for verifiable tasks where "
    "ground-truth labels are difficult to obtain, in which models learn from proxy reward signals "
    "derived without relying on human annotation efforts. The domain is restricted to verifiable "
    "tasks (e.g., math, code, puzzles) with some form of answer-checking, distinguishing it from "
    "general self-rewarding approaches.",
    title="URLVR definition",
)

intrinsic_rewards_definition = setting(
    "Intrinsic reward methods in URLVR generate proxy rewards solely from the model's own internal "
    "states—either from confidence/entropy metrics (certainty-based) or from consistency across "
    "multiple model rollouts (ensemble-based)—without consulting any external verifier or labeled data.",
    title="Intrinsic rewards definition",
)

external_rewards_definition = setting(
    "External reward methods in URLVR generate verifiable rewards through mechanisms independent "
    "of the model's internal state, either by: (1) leveraging unlabeled text corpora as latent "
    "ground truth (next-token prediction objectives, reconstruction signals), or (2) exploiting "
    "generation-verification asymmetries where generating solutions is hard but checking them is cheap "
    "(e.g., running code, evaluating arithmetic expressions, proof checkers).",
    title="External rewards definition",
)

# --- Research gap ---

intrinsic_gap = claim(
    "Despite encouraging early results, the potential and fundamental limitations of intrinsic URLVR "
    "methods remain unclear. Diverse methodologies have been applied across different model families "
    "and evaluation settings without systematic comparison or consensus on what constitutes reliable "
    "unsupervised rewards, and the mechanisms underlying both early gains and failure modes are "
    "underexplored.",
    title="Gap: intrinsic URLVR understanding",
)

# --- Main contributions (research questions) ---

q_scalability = question(
    "Can intrinsic rewards truly scale LLM training beyond what the model already knows, "
    "or is there a fundamental ceiling determined by the model's initial confidence-correctness alignment?"
)

q_safe_application = question(
    "Under what conditions can intrinsic URLVR be applied safely, avoiding model collapse and reward hacking?"
)

q_measure_prior = question(
    "Can we measure the model's prior (confidence-correctness alignment) efficiently, without running "
    "full expensive RL training, to predict RL trainability?"
)

q_external_scaling = question(
    "Do external reward methods (generation-verification asymmetry, unlabeled data) escape the "
    "confidence-correctness ceiling that limits intrinsic methods?"
)

# --- Motivation for the paper's approach ---

strat_bottleneck_motivates_urlvr = support(
    [supervision_bottleneck],
    intrinsic_gap,
    reason=(
        "The supervision bottleneck (@supervision_bottleneck) motivates exploration of URLVR methods. "
        "Early intrinsic works report promising results but have not been systematically analyzed, "
        "creating the research gap (@intrinsic_gap): we do not yet understand when and why these "
        "methods succeed or fail, nor how to measure model prior for base-model selection."
    ),
    prior=0.92,
)
