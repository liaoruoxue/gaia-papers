"""Prior assignments for independent (leaf) claims in the 2604-14228 formalization.

Run `gaia check --hole .` to see which claims need priors.
Priors are author-reviewer judgments about the plausibility of each independent premise
before inference; they should reflect the strength of evidence in the source.

Paper: "Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems"
       (arXiv 2604.14228)

Evidence tiers used:
  Tier A: Official Anthropic publications, peer-reviewed empirical studies
  Tier B: TypeScript source-level analysis (primary method of the paper)
  Tier C: Third-party security research, industry surveys, community analysis
"""

from .motivation import qualitatively_new_workflows, agentic_shift_introduces_new_requirements
from .s5_permissions import approval_fatigue_observation, alt_container_isolation
from .s7_context_memory import (
    file_based_memory_vs_alternatives,
    pred_file_based,
    pred_embedding_based,
)
from .s10_openclaw import obs_trust_design, pred_cc_trust, pred_oc_trust

PRIORS = {
    # ── Empirical observations (Tier A: official Anthropic sources) ──

    qualitatively_new_workflows: (
        0.92,
        "Tier A evidence: Huang et al. (2025) is an official Anthropic internal survey of "
        "132 engineers and researchers. The 27% new-task rate and 12% new-work rate are "
        "directly cited in the source paper. The claim is a measured empirical observation "
        "from a large internal study. High confidence despite internal-only study status "
        "because the methodology is disclosed and independently plausible."
    ),

    agentic_shift_introduces_new_requirements: (
        0.93,
        "Tier A/B evidence: The architectural requirements introduced by autonomous tool use "
        "(multi-step execution, permission systems, recovery mechanisms) are directly documented "
        "in the TypeScript source. That these requirements are qualitatively new compared to "
        "suggestion-based tools (GitHub Copilot) is well-established in the literature and "
        "architecturally confirmed. Very high confidence."
    ),

    approval_fatigue_observation: (
        0.91,
        "Tier A evidence: Hughes (2026) is an official Anthropic engineering post documenting "
        "the auto-mode analysis. The 93% approval rate is a specific measured statistic from "
        "production data. High confidence because it is an internal empirical measurement "
        "from the system's own telemetry, not a survey or self-report."
    ),

    # ── Source-confirmed architectural design facts (Tier B) ──

    file_based_memory_vs_alternatives: (
        0.90,
        "Tier B evidence: Directly confirmed from claudemd.ts source analysis. The paper "
        "documents the four-level CLAUDE.md hierarchy, the LLM-based header scan (not "
        "embedding-based), and the absence of a vector index. The claim accurately describes "
        "the observed implementation. High confidence because it is a source-level fact."
    ),

    # ── Analytical prediction claims for abduction strategies ──

    pred_file_based: (
        0.88,
        "Analytical claim: The predictions of file-based memory (auditability, editability, "
        "version control, file-granularity retrieval) are logically entailed by the design "
        "choice. High confidence in the internal consistency of the prediction, though "
        "prediction claims are slightly less certain than direct observations."
    ),

    pred_embedding_based: (
        0.85,
        "Analytical claim: The predictions of embedding-based memory (entry-level retrieval, "
        "opaque infrastructure, scalable to large stores) are standard characterizations "
        "of vector-similarity retrieval systems. High confidence in the prediction's accuracy "
        "as a description of this alternative approach."
    ),

    # ── Comparative system observations (Tier C: community analysis + documentation) ──

    obs_trust_design: (
        0.90,
        "Tier B/C evidence: Claude Code's deny-first design is confirmed from permissions.ts "
        "source (Tier B). OpenClaw's perimeter-level trust model is documented in OpenClaw "
        "source documentation (Tier C). Both implementations match their respective descriptions. "
        "High confidence in the observation."
    ),

    pred_cc_trust: (
        0.88,
        "Analytical claim: The predictions of Claude Code's per-action deny-first trust model "
        "are directly confirmed by the source-level analysis in Sections 3-5. The prediction "
        "accurately describes the observed implementation."
    ),

    pred_oc_trust: (
        0.86,
        "Analytical claim: The predictions of OpenClaw's perimeter-level trust model are "
        "documented in OpenClaw source documentation. Slightly lower confidence than "
        "pred_cc_trust because OpenClaw is Tier C (community) evidence."
    ),

    # ── Alternative architectural approaches (Tier B/C: literature-documented) ──

    alt_container_isolation: (
        0.90,
        "Tier C evidence: Container-based isolation in SWE-Agent and OpenHands is well-"
        "documented in the academic literature (Yang et al. 2024, Wang et al. 2024b) and "
        "confirmed in the paper's Section 5 comparative analysis. High confidence in the "
        "accurate description of this alternative safety architecture."
    ),
}
