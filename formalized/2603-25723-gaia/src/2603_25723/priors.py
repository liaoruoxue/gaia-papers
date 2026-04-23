"""
Prior assignments for 2603-25723-gaia.
Paper: Natural-Language Agent Harnesses (Pan et al., 2026)
arXiv: 2603.25723

PRIORS maps Knowledge objects to (prior_value, justification) tuples.
Only independent (leaf) claims should be assigned priors here.
Derived claims are excluded — their beliefs are determined by BP propagation.
"""

from .motivation import (
    harness_affects_outcomes,
    harness_logic_buried,
    nlah_natural_language_feasibility,
)
from .s2_approach import (
    nlah_is_portable,
    ihr_separates_concerns,
    nlah_exposes_contracts,
    file_backed_state_addresses_truncation,
)
from .s4_results import (
    rq1_trae_full_ihr_perf,
    rq1_trae_no_rts_perf,
    rq1_trae_no_hs_perf,
    rq1_live_swe_full_ihr_perf,
    rq1_live_swe_no_rts_perf,
    rq1_trae_paired_flips,
    rq1_live_swe_paired_flips,
    trae_child_agent_share,
    rq2_swe_scores,
    rq2_osworld_scores,
    rq2_self_evolution_mechanism,
    rq2_verifier_negative,
    rq2_file_backed_state_mechanism,
    rq3_os_symphony_code_perf,
    rq3_os_symphony_nlah_perf,
    rq3_topology_difference,
    rq3_search_relocation,
    pred_nlah_explains,
    pred_artifact_conventions_explains,
    alt_score_gain_artifacts,
)
from .s5_discussion import (
    alt_stronger_models_reduce_nl_value,
)

PRIORS: dict = {
    rq1_trae_full_ihr_perf: (
        0.95,
        "Directly reported in Table 1 (TRAE Full IHR row). Controlled benchmark evaluation.",
    ),
    rq1_trae_no_rts_perf: (
        0.95,
        "Directly reported in Table 1 (TRAE w/o RTS row).",
    ),
    rq1_trae_no_hs_perf: (
        0.95,
        "Directly reported in Table 1 (TRAE w/o HS row).",
    ),
    rq1_live_swe_full_ihr_perf: (
        0.95,
        "Directly reported in Table 1 (Live-SWE Full IHR row).",
    ),
    rq1_live_swe_no_rts_perf: (
        0.95,
        "Directly reported in Table 1 (Live-SWE w/o RTS row).",
    ),
    rq1_trae_paired_flips: (
        0.95,
        "Directly reported in Table 2. Paired flip counts from 125 stitched samples.",
    ),
    rq1_live_swe_paired_flips: (
        0.95,
        "Directly reported in Table 2.",
    ),
    trae_child_agent_share: (
        0.95,
        "Directly reported in Table 4. Usage split between parent and child agents.",
    ),
    rq2_swe_scores: (
        0.95,
        "Directly reported in Table 3 (SWE Verified rows).",
    ),
    rq2_osworld_scores: (
        0.95,
        "Directly reported in Table 3 (OSWorld rows).",
    ),
    rq3_os_symphony_code_perf: (
        0.95,
        "Directly reported in Table 5 (OS-Symphony Code row).",
    ),
    rq3_os_symphony_nlah_perf: (
        0.95,
        "Directly reported in Table 5 (OS-Symphony NLAH row).",
    ),
    rq2_self_evolution_mechanism: (
        0.82,
        "Figure 4 analysis plus one case study (scikit-learn-25747). Plausible mechanism "
        "but single case limits certainty.",
    ),
    rq2_verifier_negative: (
        0.90,
        "Two quantitative datapoints (-0.8% SWE, -8.4% OSWorld) plus two case studies. "
        "Both benchmarks show same direction.",
    ),
    rq2_file_backed_state_mechanism: (
        0.83,
        "Consistent with Figure 4 right panel and Table 3 (+1.6% SWE, +5.5% OSWorld). "
        "Mechanistic interpretation requires trajectory validation.",
    ),
    rq3_topology_difference: (
        0.90,
        "Supported by specific trace counts from retained archives (36+7 vs 34+2).",
    ),
    rq3_search_relocation: (
        0.85,
        "Based on 6-sample subset from retained archives. Specific breakdown (3/1) adds "
        "credibility despite small sample.",
    ),
    nlah_is_portable: (
        0.85,
        "Core paper claim. Supported by migration experiment. Not independently replicated.",
    ),
    ihr_separates_concerns: (
        0.88,
        "Definitional: IHR is designed with this factorization; ablation design "
        "operationalizes it (w/o RTS, w/o HS).",
    ),
    nlah_exposes_contracts: (
        0.83,
        "Architectural claim from Section 2 specification. Implementation quality affects "
        "how 'first-class' the contracts are in practice.",
    ),
    file_backed_state_addresses_truncation: (
        0.85,
        "Supported by context-folding literature and Section 2.4 operational properties.",
    ),
    harness_logic_buried: (
        0.88,
        "Widely corroborated: Lou et al., LangChain, Anthropic engineering blogs all "
        "acknowledge difficulty of isolating harness effects.",
    ),
    harness_affects_outcomes: (
        0.90,
        "Broad evidence: ReAct (Yao 2023), RAG (Lewis 2021), reflection (Shinn 2023), "
        "scaffold-aware evaluation (Ding 2026). Well-established across independent papers.",
    ),
    nlah_natural_language_feasibility: (
        0.88,
        "AGENTS.md and AgentSkills are documented prior work with concrete deployments.",
    ),
    pred_nlah_explains: (
        0.75,
        "Well-specified prediction consistent with trajectory evidence. Authors' own "
        "interpretation — no independent verification.",
    ),
    pred_artifact_conventions_explains: (
        0.55,
        "Partially supported: file-backed state alone gives +5.5% on OSWorld, not closing "
        "the full 16.8pp gap. Coherent but empirically underpowered.",
    ),
    alt_score_gain_artifacts: (
        0.35,
        "Alternative that artifact conventions alone explain the gap. Weakened: (1) "
        "file-backed state module gives only +5.5% not 16.8pp; (2) topology relocation "
        "is broader than any single module effect.",
    ),
    alt_stronger_models_reduce_nl_value: (
        0.40,
        "Alternative that stronger models make NL harness control less valuable. "
        "Paper's RQ1 evidence contradicts this for current generation. Long-term "
        "plausibility noted but not empirically tested.",
    ),
}
