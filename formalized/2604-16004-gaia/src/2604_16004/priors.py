"""Author-assigned priors for independent (premise) claims.

Only independent claims (those that are NOT the conclusion of any strategy) receive priors
here. Derived claims propagate via BP from their supporting strategies.

Priors are calibrated against the kind of evidence each claim rests on:
  - direct observations / table read-offs:           ~0.95
  - claims explicitly defended in the paper:         0.85 - 0.92
  - background-literature claims (paper-attested):   0.80 - 0.90
  - null hypotheses the paper aims to refute:        0.20 - 0.30
"""

from . import (
    # Motivation premises
    error_propagation_claim,
    external_grounding_gap_claim,
    genrm_single_turn_claim,
    verifier_role_claim,
    # Related-work premise
    prior_tool_augmented_rm_claim,
    # Method premises (forward / backward agent definitions)
    forward_sufficiency_claim,
    backward_necessity_claim,
    tool_augmented_capability_claim,
    # Experimental observation tables
    table1_observation,
    table2_observation,
    # Analysis observations
    ablation_observation,
    generalization_observation,
    latency_observation,
    latency_axiom,
    # Null / contradicted hypothesis
    orm_dominance_null_claim,
)


PRIORS = {
    # --- Motivation: limitation / definitional claims ---------------------------
    verifier_role_claim: (
        0.92,
        "Verifier centrality to TTS is asserted by multiple cited works (Gui 2024; "
        "Kang 2025) and is the foundational premise of the entire TTS literature.",
    ),
    genrm_single_turn_claim: (
        0.95,
        "Single-turn assessment is a definitional / observational property of the "
        "GenRM paradigm as the authors and the cited works describe it.",
    ),
    error_propagation_claim: (
        0.85,
        "Supported by Zhang et al. 2025b and illustrated by the paper's Figure 1 case "
        "study; an established failure mode of single-turn LLM verifiers.",
    ),
    external_grounding_gap_claim: (
        0.85,
        "Well-attested phenomenon for tool-free LLM verifiers (Dong 2025a/b; Feng 2025); "
        "consistent with the broader hallucination literature.",
    ),

    # --- Related work -----------------------------------------------------------
    prior_tool_augmented_rm_claim: (
        0.8,
        "Author's own characterization of the prior tool-augmented RM literature, "
        "with citations (Li 2024; Xu 2025; Peng 2025); plausible but partly polemical.",
    ),

    # --- Method: agent role definitions -----------------------------------------
    forward_sufficiency_claim: (
        0.9,
        "Definitional description of the forward agent, supported by the explicit "
        "Plan-Validate-Verdict template in Section 3.2 and the Figure 3 case study.",
    ),
    backward_necessity_claim: (
        0.9,
        "Definitional description of the backward agent under the same Plan-Validate-"
        "Verdict template; aggregated with the forward agent in Appendix C.3.",
    ),
    tool_augmented_capability_claim: (
        0.92,
        "Tool integration is implemented and described in Appendix B.2.3; agents "
        "demonstrably invoke a Python interpreter in the documented trajectories.",
    ),

    # --- Experimental observations (direct table read-offs) ---------------------
    table1_observation: (
        0.95,
        "Direct numerical read-off from Table 1 (BoN performance); near-self-certifying "
        "given the published table.",
    ),
    table2_observation: (
        0.95,
        "Direct numerical read-off from Table 2 (iterative refinement); high confidence "
        "in the reported numbers.",
    ),
    ablation_observation: (
        0.95,
        "Direct read-off from Figure 4 ablation: forward/backward variants competitive "
        "and full design strictly best on the plotted benchmarks.",
    ),
    generalization_observation: (
        0.95,
        "Direct read-off from Table 4: Agentic-Verifier-Qwen3-4B leads on both "
        "LiveCodeBench and HotpotQA against all listed baselines.",
    ),
    latency_observation: (
        0.95,
        "Direct read-off from Table 5; numbers are reported with explicit hardware "
        "and software configuration (A100 + vLLM, batch=128).",
    ),
    latency_axiom: (
        0.95,
        "Author-reported measurements taken as accurate; this serves as the substituted "
        "premise in the textbook-style deduction over Table 5.",
    ),

    # --- Null / contradicted hypothesis ---------------------------------------
    orm_dominance_null_claim: (
        0.2,
        "Null hypothesis the paper sets out to refute: Table 1 directly contradicts ORM "
        "dominance over Agentic-Verifier-Qwen3-4B. Low prior; the contradiction edge to "
        "bon_sota_claim further suppresses it under BP.",
    ),
}
