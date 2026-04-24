"""Prior assignments for leaf (independent) claims in 2511-09030-gaia."""

from . import (
    llm_degrade_hanoi,
    llm_context_burden,
    mad_one_step_per_agent,
    alt_single_agent,
    error_rate_mini_low,
    error_rate_nano,
    error_rate_oss_20b,
    errors_decorrelated,
    pred_maker,
    pred_single_agent,
    mdap_orthogonal_direction,
)

PRIORS = {
    # MAD design claim (definitional leaf — by construction of the system)
    mad_one_step_per_agent: (
        0.99,
        "By definition of MAKER/MAD, each agent handles exactly one step. This is the "
        "foundational design choice of the system, not an empirical hypothesis.",
    ),
    # Motivation / problem characterization (empirical observations from prior work)
    llm_degrade_hanoi: (
        0.97,
        "Directly observed and reported in prior work (Shojaee et al. 2025). "
        "The catastrophic degradation at 5-6 disks is a crisp empirical finding.",
    ),
    llm_context_burden: (
        0.90,
        "Well-established mechanism in the LLM literature; auto-regressive models "
        "are known to degrade with growing context. High confidence.",
    ),
    # Single-agent alternative (mathematical consequence)
    alt_single_agent: (
        0.97,
        "Mathematical fact: the expected cost of a non-decomposed single-agent approach "
        "grows as p^(-s) (exponential in s), which is infeasible at s=1M for any p<1.",
    ),
    # Empirical error rate measurements (direct sampling from 10K step experiments)
    error_rate_mini_low: (
        0.92,
        "Based on 10,000 random single-step samples; statistical estimate with small "
        "error bars. High confidence in the reported 0.00223 error rate.",
    ),
    error_rate_nano: (
        0.92,
        "Same 10K-sample measurement methodology as error_rate_mini_low; direct empirical "
        "measurement of gpt-4.1-nano's per-step error rate.",
    ),
    error_rate_oss_20b: (
        0.92,
        "Same measurement methodology; direct empirical measurement for gpt-oss-20B.",
    ),
    errors_decorrelated: (
        0.88,
        "Zero shared errors across two independent 10K-sample runs is compelling evidence. "
        "Slight uncertainty remains about rare pathological steps not captured by 10K samples.",
    ),
    # Abduction hypothesis predictions (theoretical, high-confidence derivations)
    pred_maker: (
        0.90,
        "Follows from the mathematical scaling law (Eq. 13) with measured p=0.99777 and "
        "k=3. High confidence given the well-validated formula and measured error rate.",
    ),
    pred_single_agent: (
        0.99,
        "Mathematical consequence of (1-0.00223)^1048575 ≈ 10^(-1014). Near-certain failure.",
    ),
    # Framing claim (supported by Figure 1 but conceptual)
    mdap_orthogonal_direction: (
        0.85,
        "The framing is well-supported by Figure 1 showing MAKER achieving what no "
        "base LLM can. The orthogonality argument is conceptually clear and empirically "
        "supported by the experimental results.",
    ),
}
