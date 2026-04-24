"""Prior assignments for independent (leaf) claims in the GenericAgent knowledge package.

Priors are assigned to claims not concluded by any strategy. They encode our epistemic
confidence in each claim as a stand-alone proposition, independent of BP propagation.
"""

from . import (
    alt_model_advantage,
    alt_web_tools,
    failure_attention_dilution,
    failure_effective_window,
    failure_experience_reuse,
    failure_positional_bias,
    ga_density_architecture,
    obs_multihop,
    obs_open_domain,
    obs_temporal,
    result_context_explosion,
    thesis_minimal_architecture,
    web_density_design,
)

PRIORS = {
    # ── Failure-mode premises (established in cited prior work) ───────────────
    failure_positional_bias: (
        0.92,
        "Well-replicated finding from Liu et al. 2023 ('Lost in the Middle'): "
        "LLMs systematically underperform when critical information is mid-context. "
        "High prior because the finding is reproducible across many model families.",
    ),
    failure_attention_dilution: (
        0.90,
        "Established in Shi et al. 2023 (LLMs distracted by irrelevant context). "
        "High prior as this is a fundamental architectural property of attention "
        "mechanisms with broad empirical support.",
    ),
    failure_effective_window: (
        0.88,
        "Established in An et al. 2024 (ICLR 2025, 'Why does the effective context "
        "length of LLMs fall short?'). High prior because the result is demonstrated "
        "rigorously and accepted at a top venue.",
    ),
    failure_experience_reuse: (
        0.85,
        "The claim that current agents fail to accumulate experience across episodes "
        "is well-supported by the LifelongAgentBench paper and the broad agent "
        "literature. Slightly lower because some frameworks (MemGPT, A-MEM) do "
        "attempt cross-episode memory.",
    ),

    # ── Thesis claims (central assertions of the paper) ──────────────────────
    thesis_minimal_architecture: (
        0.72,
        "The claim that minimal architecture (~3,000 lines) is a necessary prerequisite "
        "for architectural self-update is argued by analogy (agent must understand codebase). "
        "Plausible but not empirically validated in the paper — the self-update dimension "
        "is explicitly left as future work. Moderate prior.",
    ),

    # ── Experimental observations (directly measured) ─────────────────────────
    result_context_explosion: (
        0.95,
        "Directly measured prompt length after installing 20 skills. GA: 2,298 tokens "
        "vs Claude Code 22,821, CodeX 23,932, OpenClaw 43,321. This is a deterministic "
        "measurement with a clear and reproducible protocol. Very high prior.",
    ),

    # ── Hypothesis claims used in abductions ─────────────────────────────────
    ga_density_architecture: (
        0.78,
        "The density-architecture hypothesis (hierarchical memory + minimal tools + "
        "compression = primary driver of advantage) is the paper's central claim and "
        "is supported by multiple experimental dimensions. Moderate-high prior because "
        "the evidence across benchmarks is consistent but alternative explanations "
        "(model quality, benchmark selection) are not fully ruled out.",
    ),
    web_density_design: (
        0.75,
        "The web density design hypothesis (DOM compression + atomic browser tools = "
        "web performance advantage) is supported by the BrowseComp-ZH results (3x score "
        "advantage). Moderate prior because web performance depends on many factors "
        "including benchmark task design, and only two systems are compared.",
    ),

    # ── Empirical observations (induction sub-observations) ───────────────────
    # These are directly measured LoCoMo results — anchoring them with high priors
    # allows the backward message to flow correctly through the induction to the law.
    obs_multihop: (
        0.93,
        "GA's Multi-Hop F1=43.33 exceeds Mem0 F1=39.32, A-MEM F1=29.03, OpenClaw F1=21.43 "
        "on LoCoMo. This is a directly measured experimental result. High prior.",
    ),
    obs_temporal: (
        0.93,
        "GA's Temporal F1=52.23 exceeds Mem0 F1=50.03, A-MEM F1=46.83, OpenClaw F1=22.56 "
        "on LoCoMo. This is a directly measured experimental result. High prior.",
    ),
    obs_open_domain: (
        0.92,
        "GA's Open-Domain F1=20.41 exceeds Mem0 F1=18.32, A-MEM F1=13.11, OpenClaw F1=9.56 "
        "on LoCoMo. Directly measured. Slightly lower prior because open-domain is the "
        "hardest category and margin over Mem0 is smaller (2.09 F1 points).",
    ),

    # ── Alternative explanations (abduction alternatives) ────────────────────
    alt_model_advantage: (
        0.22,
        "The model-selection alternative is partially falsified by the cross-LLM results "
        "(GA still outperforms with Minimax M2.7). However, backbone LLM capability "
        "inevitably contributes some portion of the observed advantage. Low prior because "
        "the architecture-based explanation accounts for the cross-LLM consistency.",
    ),
    alt_web_tools: (
        0.20,
        "The specialized-tools alternative is inconsistent with GA outperforming OpenClaw "
        "even on standard WebCanvas interactions where specialized tools should have the "
        "most advantage. Very low prior — the evidence across all three web benchmarks "
        "is strongly against this alternative.",
    ),
}
