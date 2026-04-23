"""
Priors for 2509-07430-gaia: The Choice of Divergence in RLVR.

This file assigns prior probabilities to independent (leaf) claims.
Derived claims are excluded — their beliefs are determined by BP propagation.

Prior calibration rationale:
- Experimental results (measured numbers from published tables): 0.92-0.93
  (high confidence; peer-reviewed table data, directly reported)
- Theoretical analysis claims (mathematical correctness, textbook facts): 0.85-0.90
  (high confidence; formal derivations, but not independently verified)
- Qualitative/interpretive claims (design rationale, generalization, efficiency): 0.82-0.87
  (moderate-high; supported by evidence but involve interpretation or figure-reading)
"""

from .motivation import (
    divergence_choice_neglected,
    pass1_improves,
)
from .s2_background import (
    forward_kl_mass_covering,
    js_mass_covering,
    rkl_mode_seeking_harm,
)
from .s3_method import (
    dphrl_handles_discrete,
    threshold_8_of_8_optimal,
)
from .s4_theory import (
    grpo_no_bound,
    trpo_standard_vs_dphrl,
)
from .s5_experiments import (
    capability_retention,
    math_llama_results,
    math_qwen_results,
    ood_math_results,
    solution_style_diversity,
    sql_bird_results,
    sql_spider_results,
)

PRIORS = {
    # ── Experimental results (high confidence — published table data) ──────────────
    sql_bird_results: (
        0.93,
        "Published Table 1 data; exact Pass@8/16 numbers for 6 methods on BIRD SQL. "
        "Values directly reported; pattern of GRPO/DAPO degradation is clear and consistent.",
    ),
    sql_spider_results: (
        0.93,
        "Published Table 1 data for Spider SQL benchmark. GRPO Pass@8 = 79.5 vs base 90.9 "
        "is a large, unambiguous degradation. Cross-domain results are directly reported.",
    ),
    ood_math_results: (
        0.93,
        "Published Table 2 data averaging 6 math benchmarks for SQL-trained models. "
        "Pattern of catastrophic forgetting in GRPO/DAPO and recovery in DPH variants "
        "is robust across 6 diverse benchmarks.",
    ),
    math_llama_results: (
        0.92,
        "Published Table 3 data for Llama-3.1-8B on AIME24. AIME24 has ~30 problems "
        "so Pass@64 estimates carry variance, but values are directly reported from experiments.",
    ),
    math_qwen_results: (
        0.92,
        "Published Table 3 data for Qwen2.5-Math-7B on AIME24. DPH-F Pass@64 = 73.33 "
        "is a notable improvement; slight uncertainty from small test set size.",
    ),
    capability_retention: (
        0.85,
        "Figure 3 qualitative analysis. Approximate 85%/15% retention figures read from "
        "a figure rather than a table; moderate confidence in exact percentages, "
        "high confidence in directional conclusion (DPH-JS retains more than GRPO/RKL).",
    ),
    solution_style_diversity: (
        0.85,
        "Figure 4 qualitative analysis of solution styles. Qualitative claim about "
        "multiple distinct styles vs single style is visually evaluated; harder to "
        "quantify precisely but directionally well-supported by mode-seeking theory.",
    ),
    threshold_8_of_8_optimal: (
        0.83,
        "Table 4 ablation with limited threshold comparisons (6/8 vs 8/8). "
        "The conclusion that 8/8 is optimal is supported by one comparison point. "
        "The '8% of training data' figure is a direct dataset statistic.",
    ),
    # ── Theoretical and mathematical claims ───────────────────────────────────────
    trpo_standard_vs_dphrl: (
        0.88,
        "Mathematical comparison between standard TRPO bound and DPH-RL bound. "
        "The positive bonus term epsilon_f > 0 is formally derived in the paper; "
        "confidence is high but the proof is not independently verified here.",
    ),
    grpo_no_bound: (
        0.90,
        "Definitionally true: GRPO's published formulation explicitly excludes a KL "
        "divergence term. Without any divergence term, no TRPO-style guarantee applies. "
        "This is a formal consequence of GRPO's design, not an empirical claim.",
    ),
    forward_kl_mass_covering: (
        0.90,
        "Well-known information-theoretic property. The mass-covering behavior of "
        "D_KL(p||q) (which penalizes q for assigning near-zero mass where p is non-zero) "
        "is a textbook result in variational inference and information theory.",
    ),
    js_mass_covering: (
        0.90,
        "Well-known property of JS divergence: bounded, symmetric, mass-covering. "
        "Follows from its definition as a symmetrized KL mixture. High confidence.",
    ),
    rkl_mode_seeking_harm: (
        0.87,
        "Reverse-KL's mode-seeking property is textbook variational inference. "
        "The specific application to LLM RLVR (converging to single solution modes) "
        "requires the additional step of applying this to token distributions, "
        "which involves implicit assumptions about LLM solution space structure. "
        "Empirical evidence (RKL OOD math = 48.45, worst of all methods) supports it.",
    ),
    # ── Design and interpretation claims ─────────────────────────────────────────
    divergence_choice_neglected: (
        0.82,
        "Claim about the state of prior art. Mainstream RLVR methods (GRPO, DAPO) "
        "indeed omit divergence constraints per their published formulations. "
        "'Neglected' is a qualitative assessment; some concurrent work may have "
        "explored divergence choices but not as the primary focus.",
    ),
    dphrl_handles_discrete: (
        0.83,
        "Generator-based approach is described in the paper as handling discrete "
        "action spaces via pre-sampled trajectories. The claim that it 'effectively "
        "handles' the challenge is supported by the working system, but no explicit "
        "ablation shows that alternative discrete-space approaches would fail.",
    ),
    pass1_improves: (
        0.92,
        "Well-documented phenomenon across the RLVR literature. RLVR consistently "
        "improves Pass@1 on in-domain tasks — this is the primary motivation for "
        "using RLVR and is confirmed by this paper's own results plus extensive "
        "prior literature (DeepSeekMath, DeepSeek-R1, DAPO, etc.).",
    ),
}
