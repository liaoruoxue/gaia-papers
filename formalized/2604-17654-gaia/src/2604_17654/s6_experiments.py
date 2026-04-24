"""
Section 6: Experiments — Mathematical Reasoning and Synthetic Domains.

Section 6.1: Mathematical reasoning on POLARIS-53k with Qwen-3-4B-Base.
Section 6.2: Synthetic domains (polynomial solving, multi-digit multiplication).
"""

from gaia.lang import claim, setting, support, abduction, compare
from .s4_poly_epo import poly_epo_algorithm, polychromic_objective_def
from .motivation import rl_diversity_collapse, poly_epo_claim

# ──────────────────────────────────────────────────────────────────────
# Experimental setup
# ──────────────────────────────────────────────────────────────────────

math_setup = setting(
    "Mathematical reasoning experiment setup:\n\n"
    "| Parameter | Value |\n"
    "|-----------|-------|\n"
    "| Base model | Qwen-3-4B-Base |\n"
    "| Training dataset | POLARIS-53k [@AXL25] |\n"
    "| Prompts per batch | 128 |\n"
    "| Rollouts per prompt ($N$) | 8 |\n"
    "| Set size ($n$) | 4 |\n"
    "| Number of sets ($K$) | 70 |\n"
    "| Training epochs | 2 |\n"
    "| Training steps | 850 |\n"
    "| Learning rate | $1 \\times 10^{-6}$ |\n"
    "| KL coefficient | 0.0 |\n"
    "| Clip ratios | $\\epsilon_{\\text{low}} = 0.20$, $\\epsilon_{\\text{high}} = 0.28$ |\n"
    "| Max response length | 4096 tokens |\n"
    "| Device | $4 \\times$ NVIDIA H200 |\n"
    "| LM-judge | Qwen-3-4B-Instruct |\n\n"
    "Evaluation benchmarks: BeyondAIME, AIME 2026, AIME 2025, HMMT November 2025, "
    "HMMT February 2025, Minerva [@OrneHamid2026].",
    title="Math reasoning experimental setup",
)

grpo_baseline_def = setting(
    "GRPO baseline: Standard GRPO [@SWZ24] with advantage "
    "$\\hat{A}_{i,t} = r(x,y_i) - \\text{mean}(\\{r(x,y_1),\\ldots,r(x,y_N)\\})$, "
    "without standard deviation normalization (consistent with Dr.GRPO [@LCL25]). "
    "Uses same base model and training data as Poly-EPO [@OrneHamid2026].",
    title="GRPO baseline definition",
)

grpo_div_baseline_def = setting(
    "GRPO+DIV baseline (reward-shaped exploration): Standard RL with diversity bonus "
    "using the same LM-judge clustering as Poly-EPO. Diversity bonus for generation $y$ given "
    "rollouts $y_{1:N}$ is:\n\n"
    "$$d(x,y|y_{1:N}) = \\frac{N/|\\text{Cluster}(y)| - 1}{N-1}$$\n\n"
    "where $\\text{Cluster}(y)$ is the set of generations in the same cluster as $y$. "
    "Advantage: $\\hat{A}_{i,t} = r(x,y_i) + \\lambda d(x,y_i) - \\text{mean}(\\{r+\\lambda d\\})$. "
    "Optimized with GRPO. This is NOT a set RL objective [@OrneHamid2026].",
    title="GRPO+DIV baseline definition",
)

# ──────────────────────────────────────────────────────────────────────
# Experimental results: pass@k
# ──────────────────────────────────────────────────────────────────────

pass_at_k_result = claim(
    "Pass@$k$ results on mathematical reasoning test sets (Poly-EPO vs GRPO vs GRPO+DIV, "
    "base model Qwen-3-4B-Base, Figure 1):\n\n"
    "- Poly-EPO pass@$k$ improves more strongly as $k$ increases across all 6 benchmarks "
    "(BeyondAIME, AIME 2026, AIME 2025, HMMT Nov 2025, HMMT Feb 2025, Minerva), indicating "
    "higher effective diversity.\n"
    "- GRPO and GRPO+DIV exhibit substantial pass@$k$ degradation: the pretrained base model "
    "(Qwen-3-4B-Base) begins to outperform them as early as $k = 32$.\n"
    "- Poly-EPO achieves pass@$k$ coverage gains of up to 20% on mathematical reasoning test "
    "sets compared to GRPO [@OrneHamid2026].",
    title="Pass@k improvements",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 1: Pass@k evaluations on test sets"},
)

pass_at_k_grpo_degradation = claim(
    "GRPO and GRPO+DIV pass@$k$ degrade to below the pretrained base model (Qwen-3-4B-Base) "
    "performance at $k = 32$ on mathematical reasoning benchmarks. This demonstrates that "
    "standard RL fine-tuning collapses generation diversity sufficiently that the untrained "
    "base model provides better coverage when many samples are drawn [@OrneHamid2026].",
    title="GRPO pass@k degradation below base model",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 1: Pass@k evaluations on test sets"},
)

# ──────────────────────────────────────────────────────────────────────
# Training dynamics
# ──────────────────────────────────────────────────────────────────────

training_diversity_result = claim(
    "Training dynamics on POLARIS-53k — strategy diversity (Figure 2, left): "
    "Average number of unique reasoning-strategy clusters among correct generations per prompt "
    "(assigned by Qwen-3-4b-Instruct):\n\n"
    "- GRPO: number of clusters declines after ~200 training steps, indicating contraction.\n"
    "- GRPO+DIV: metric remains approximately flat, suggesting limited expansion.\n"
    "- Poly-EPO: steadily increases unique clusters to substantially higher levels than either "
    "baseline throughout 850 training steps [@OrneHamid2026].",
    title="Training diversity dynamics",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 2: Training dynamics on POLARIS-53k"},
)

training_coverage_result = claim(
    "Training dynamics on POLARIS-53k — problem coverage (Figure 2, right): "
    "Fraction of training prompts for which the model generates at least one correct rollout:\n\n"
    "- Both Poly-EPO and GRPO+DIV outperform GRPO for much of training.\n"
    "- Methods that explicitly encourage exploration achieve higher coverage.\n"
    "- This shows exploration not only preserves strategic diversity but also improves the "
    "probability of uncovering successful solutions during training [@OrneHamid2026].",
    title="Training coverage dynamics",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 2: Training dynamics on POLARIS-53k"},
)

# ──────────────────────────────────────────────────────────────────────
# Branching analysis
# ──────────────────────────────────────────────────────────────────────

branching_result = claim(
    "Branching analysis (Figure 3): Generation diversity characterized by branching structure "
    "of sampled rollouts organized by shared token prefixes.\n\n"
    "- Poly-EPO models branch substantially earlier in the generation process than GRPO-trained "
    "models, across AIME 2026, BeyondAIME, and Minerva benchmarks.\n"
    "- GRPO models eventually reach a similar number of branches at later token positions, "
    "but generations remain coupled (share the same prefix) much longer before diverging.\n"
    "- Early branching corresponds to committing to distinct reasoning strategies earlier, "
    "indicating broader strategic exploration at test time [@OrneHamid2026].",
    title="Branching structure analysis",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 3: Poly-EPO promotes broader branching"},
)

# ──────────────────────────────────────────────────────────────────────
# Majority voting
# ──────────────────────────────────────────────────────────────────────

majority_vote_result = claim(
    "Majority voting evaluation (Figure 4): All methods initialized from Qwen-3-4B-Base.\n\n"
    "- Poly-EPO majority vote share (fraction of $k$ votes assigned to winning answer) is "
    "consistently lower than GRPO and GRPO+DIV across all benchmarks, indicating greater "
    "response diversity at inference.\n"
    "- Despite higher entropy over final answers, Poly-EPO attains equal or stronger "
    "majority-vote accuracy as $k$ increases, often yielding the largest gains from additional "
    "samples (scales more effectively with test-time compute).\n"
    "- This suggests the diversity induced by Poly-EPO reflects useful diversity in reasoning "
    "trajectories, not merely random variation [@OrneHamid2026].",
    title="Majority voting results",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 4: Majority@k evaluations on Test Sets"},
)

# ──────────────────────────────────────────────────────────────────────
# Synthetic domains (Section 6.2)
# ──────────────────────────────────────────────────────────────────────

synthetic_setup = setting(
    "Synthetic domain experiment setup:\n\n"
    "| Parameter | Value |\n"
    "|-----------|-------|\n"
    "| Base model | Qwen-3-1.7B-Base |\n"
    "| LM-judge | Gemini-2.0-Flash |\n"
    "| Tasks | Multi-digit multiplication, Polynomial solving |\n\n"
    "Task definitions:\n"
    "- **Polynomial solving**: Given a polynomial relation, output $(x,y) \\in \\mathbb{R}^2$ "
    "satisfying it (e.g., $y = x^2 + 3x + 7$, valid solution $(1, 11)$). Diversity is defined "
    "over distinct final answers.\n"
    "- **Multi-digit multiplication**: Compute product of two integers via decomposition "
    "(e.g., $343 \\times 67 = (340+3)(70-3)$). Diversity by clustering strategies "
    "(factorization vs partial products by place values) [@OrneHamid2026].",
    title="Synthetic domain setup",
)

synthetic_diversity_result = claim(
    "Synthetic domain training dynamics (Figure 5): Number of distinct clusters among correct "
    "and incorrect responses per prompt (averaged over batch), for Qwen-3-1.7B-Base:\n\n"
    "- GRPO quickly collapses to a single successful strategy on both tasks.\n"
    "- Poly-EPO continues to explore and discovers more than **5x** as many distinct successful "
    "strategies as GRPO on both multi-digit multiplication and polynomial solving.\n"
    "- Poly-EPO preserves higher diversity over incorrect generations as well, indicating "
    "broader strategy coverage during exploration [@OrneHamid2026].",
    title="Synthetic domain diversity results",
    metadata={"figure": "artifacts/2604.17654.pdf", "caption": "Figure 5: Training dynamics on synthetic domains"},
)

# ──────────────────────────────────────────────────────────────────────
# Reasoning connections
# ──────────────────────────────────────────────────────────────────────

strat_pass_at_k = support(
    [poly_epo_algorithm, polychromic_objective_def],
    pass_at_k_result,
    reason=(
        "Poly-EPO (@poly_epo_algorithm) trains the model via the polychromic objective "
        "(@polychromic_objective_def) to produce sets with diverse reasoning strategies. "
        "This diversity is directly measured by pass@$k$: higher strategy diversity means "
        "a larger fraction of problems can be solved by at least one of $k$ samples. "
        "The improvement over GRPO confirms the polychromic objective successfully incentivizes "
        "diverse strategies beyond reward maximization alone."
    ),
    prior=0.85,
)

strat_grpo_degradation = support(
    [rl_diversity_collapse],
    pass_at_k_grpo_degradation,
    reason=(
        "The diversity collapse identified in the motivation (@rl_diversity_collapse) directly "
        "predicts that GRPO-trained models will have reduced pass@$k$ at large $k$ compared to "
        "the base model. When diversity collapses, all $k$ samples tend to produce the same "
        "reasoning paths, so coverage saturates quickly. The observation that GRPO falls below "
        "base model at $k=32$ is a direct empirical manifestation of diversity collapse."
    ),
    prior=0.9,
)

strat_training_diversity = support(
    [poly_epo_algorithm, polychromic_objective_def],
    training_diversity_result,
    reason=(
        "Poly-EPO's polychromic objective (@poly_epo_algorithm, @polychromic_objective_def) "
        "directly rewards sets for containing diverse reasoning strategies. During training, "
        "this creates a persistent gradient signal toward broader strategy discovery. "
        "The steady increase in unique clusters (vs GRPO's collapse and GRPO+DIV's plateau) "
        "demonstrates that the polychromic set-level objective more effectively incentivizes "
        "strategy diversity than either no-exploration (GRPO) or single-generation diversity "
        "bonus (GRPO+DIV)."
    ),
    prior=0.85,
)

strat_majority_vote = support(
    [pass_at_k_result, training_diversity_result],
    majority_vote_result,
    reason=(
        "Higher pass@$k$ coverage (@pass_at_k_result) and greater training-time diversity "
        "(@training_diversity_result) together imply that Poly-EPO's generations contain useful "
        "diverse reasoning paths. Under majority voting, this useful diversity translates into "
        "improved accuracy as $k$ increases — each additional sample adds genuine information "
        "rather than repeating the same approach. The lower majority vote share confirms that "
        "probability mass is spread over more valid answer candidates, not merely producing noise."
    ),
    prior=0.82,
)

strat_synthetic = support(
    [poly_epo_algorithm],
    synthetic_diversity_result,
    reason=(
        "In synthetic domains with infinitely many valid strategies (@synthetic_setup), "
        "Poly-EPO's polychromic objective (@poly_epo_algorithm) directly rewards discovering "
        "new strategy clusters. GRPO's mode-collapse tendency produces a single high-reward "
        "strategy and stops exploring. The 5x+ diversity gain in correct strategy clusters "
        "directly validates the core claim that Poly-EPO discovers a broader repertoire of "
        "successful strategies, as intended by the polychromic design."
    ),
    prior=0.88,
)

__all__ = [
    "math_setup",
    "pass_at_k_result",
    "pass_at_k_grpo_degradation",
    "training_diversity_result",
    "training_coverage_result",
    "branching_result",
    "majority_vote_result",
    "synthetic_diversity_result",
]
