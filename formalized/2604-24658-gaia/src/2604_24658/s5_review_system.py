"""Section 5: ARA Verification and Review -- the three-level Seal protocol.

Because an ARA is a structured machine-executable artifact, properties
that PDF review checks subjectively become objectively verifiable.
The ARA Seal is a three-level credential (structural integrity ->
argumentative rigor -> execution reproducibility) that gates a
three-stage review pipeline. Stage 1-2 resolve mechanical and rigor
issues; only Stage 3 demands human judgment on significance, novelty,
and taste.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Design principles (§5.1)
# ---------------------------------------------------------------------------

claim_p1_automate_mechanical = claim(
    "**Review P1: Automate the mechanical; reserve humans for "
    "judgment.** Structural validity, internal consistency, and claim "
    "reproducibility are *objective* properties that pass or fail "
    "deterministically. Significance, novelty, and taste require "
    "domain expertise. Reviewers should never spend time verifying "
    "that 'Experiment E03 matches Claim C02' when a machine can do so "
    "in seconds; resolving all machine-checkable issues *before* the "
    "artifact reaches a human reviewer ensures expert attention is "
    "spent exclusively on questions that genuinely require it. "
    "Review-load growth at top venues exceeds reviewer-pool growth "
    "[@Aczel2021], making this redirection economically necessary, not "
    "merely convenient.",
    title="Review P1: separate machine-objective verification from human-judgment review",
)

claim_p2_reproducibility_foundational = claim(
    "**Review P2: Reproducibility as a foundational requirement.** "
    "*'Code available upon request'* nominally satisfies today's "
    "reproducibility bar [@Stodden2016]; in an ARA-native system, "
    "reproducibility is a **machine-verified property** of the artifact "
    "itself. Passing ARA Seal Level 1 (structural integrity) is a "
    "**submission requirement**; Level 2 (argumentative rigor) "
    "produces a structured critique before the venue spends compute on "
    "Level 3 (execution reproducibility). Artifacts that fail "
    "structural checks, or whose claims remain obviously under-"
    "supported after Level 2 critique, do not advance to human review.",
    title="Review P2: reproducibility is machine-verified property, not author promise",
)

# ---------------------------------------------------------------------------
# The ARA Seal: three levels (§5.2)
# ---------------------------------------------------------------------------

claim_seal_level1_structural = claim(
    "**Seal Level 1 -- Structural Integrity (seconds, deterministic).** "
    "A Python script verifies (a) directory ontology exists "
    "(`/logic`, `/src`, `/trace`, `/evidence`); (b) mandatory files "
    "present; (c) every structured file conforms to schema (each "
    "claim must have `Statement`, `Status`, `Falsification criteria`, "
    "`Proof`; each experiment `Verifies`, `Setup`, `Procedure`, "
    "`Expected outcome`; each heuristic `Rationale`, `Sensitivity`, "
    "`Bounds`); (d) minimum counts (≥5 concepts, ≥3 experiments, ≥8 "
    "exploration-tree nodes including ≥1 `dead_end` and ≥1 `decision`); "
    "(e) **all cross-layer references resolve** (every experiment ID in "
    "`claims.md` Proof fields exists in `experiments.md`; every claim "
    "ID in `experiments.md` Verifies fields exists in `claims.md`; "
    "every code_ref in `heuristics.md` points to a valid module; "
    "claims referenced in `exploration_tree.yaml` resolve). Level 1 "
    "passes or fails in seconds; failure types: missing file, missing "
    "field, dangling reference, type mismatch, dependency resolution "
    "failure.",
    title="Seal L1: deterministic schema + cross-layer reference checks (seconds)",
    metadata={"source_figure": "Fig. 8 (artifacts/2604.24658.pdf, p. 9)"},
)

claim_seal_level2_rigor = claim(
    "**Seal Level 2 -- Argumentative Rigor (minutes, rubric-anchored "
    "agent).** Without executing code or consulting external sources, "
    "the **Rigor Auditor** agent evaluates whether a Level-1-valid "
    "artifact's *content* is epistemically sound along **six** "
    "objective dimensions, each scored 1-5 on an anchored rubric. "
    "Three load-bearing dimensions: (a) **evidence relevance** -- "
    "every claim's cited experiments substantively address what it "
    "asserts under type-aware entailment (causal claims need isolating "
    "ablations; generalization claims need heterogeneous test "
    "conditions; improvement claims need baseline comparisons); (b) "
    "**falsifiability quality** -- criteria are actionable, "
    "non-tautological, scope-matched, independently testable; and "
    "(c) **methodological rigor** -- baseline adequacy, ablation "
    "coverage, statistical reporting, metric-claim alignment. Three "
    "further dimensions (scope calibration, argument coherence, "
    "exploration integrity) are in App. H.2.2. Findings are collected "
    "with severity (critical/major/minor/suggestion), verbatim "
    "evidence spans, and actionable suggestions; the overall grade is "
    "derived from the mean score and per-dimension floors.",
    title="Seal L2: 6-dimension rubric-anchored agent audit (minutes)",
)

claim_seal_level3_execution = claim(
    "**Seal Level 3 -- Execution Reproducibility (hours-days, "
    "sandboxed coding agent).** The system selects claims by "
    "criticality (those in the contribution list, those anchoring the "
    "most downstream dependencies, or author-flagged) and runs "
    "**scaled-down directional checks** (small data, few epochs, toy "
    "configurations) that test whether claimed properties hold "
    "*qualitatively* rather than reproducing exact numbers. The "
    "verifying agent is **isolated from the artifact's evidence "
    "layer**: it receives only the code kernel and algorithm "
    "descriptions, never the reported numbers, **preventing "
    "fabrication by copying expected outcomes**. Venues set a compute "
    "budget; claims that exceed it are flagged as `unverified`. "
    "Full-scale reproduction is optional and typically post-acceptance.",
    title="Seal L3: budget-bounded, evidence-blind directional reproduction (hours-days)",
)

claim_seal_certificate = claim(
    "**Seal Certificate.** Passing the applicable levels issues a "
    "*Seal Certificate*: a signed record of artifact ID, verification "
    "level achieved, timestamp, environment hash, and per-claim "
    "reproduction outcomes. Downstream agents check this certificate "
    "before investing compute, avoiding redundant re-verification. The "
    "certificate is *living*: full-scale reproductions are appended "
    "post-acceptance; new replications/refutations update the per-"
    "claim status, so confidence accrues continuously rather than at a "
    "single accept-moment.",
    title="Seal Certificate: signed, living credential cached for downstream agent re-use",
)

# ---------------------------------------------------------------------------
# Three-stage review pipeline (§5.3)
# ---------------------------------------------------------------------------

claim_three_stage_review_pipeline = claim(
    "**Three-stage review pipeline mirrors CI/CD (Figure 9).** Each "
    "stage gates the next:\n\n"
    "1. **Stage 1 -- Conceptual Verification (minutes)**: ARA Seal "
    "Level 1 + Rigor Auditor Level 2 + advisory diagnostics "
    "(exploration-tree dead-end coverage, related-work graph baselines, "
    "experiment-claim coverage gaps). Output: a CI Report and a "
    "Level-2 rigor report. Authors iterate before advancing -- "
    "analogous to fixing lint errors and design issues before code "
    "review.\n"
    "2. **Stage 2 -- Empirical Verification (hours-days)**: ARA Seal "
    "Level 3, evidence-blinded. Output: an Empirical Review Report "
    "recording which claims were verified, which failed, which were "
    "deferred due to budget, and what experimental gaps were "
    "identified.\n"
    "3. **Stage 3 -- Human Review (days-weeks)**: humans receive the "
    "submission alongside both reports and focus on judgment "
    "(significance, novelty, taste, ethical implications, contested "
    "AI-reviewer findings adjudicated with the full audit trail). The "
    "key efficiency gain: humans never spend time on 'your code "
    "doesn't run' or 'Table 3 contradicts Claim 2'.",
    title="Three-stage pipeline: Conceptual -> Empirical -> Human, each gates the next",
    metadata={"source_figure": "Fig. 9 (artifacts/2604.24658.pdf, p. 10)"},
)

# ---------------------------------------------------------------------------
# Empirical evaluation of the review system (§7.5)
# ---------------------------------------------------------------------------

claim_seal_l1_empirical_validity = claim(
    "**Seal Level 1 empirical validity: 95.6% Cat-A accuracy on "
    "L1-gated artifacts.** Every ARA entering the Understanding "
    "evaluation passed Level 1; the **95.6% Cat. A accuracy** "
    "(Table 3) on the resulting artifacts is the end-to-end witness "
    "that L1-gating delivers structural completeness sufficient for "
    "agents to retrieve information actually present in the source. "
    "The 4.4% residual is bounded by information genuinely absent from "
    "the source, not by structural defects -- because L1 would have "
    "caught those.",
    title="L1 empirical validity: 95.6% Cat. A accuracy on L1-gated ARAs",
)

claim_rigor_auditor_mutation_results = claim(
    "**Rigor Auditor mutation benchmark: 95/115 = 82.6% overall, with "
    "an orphan-experiment blind spot (Table 4).** Each of the 23 "
    "PaperBench ARAs is seeded with five injection types (115 total). "
    "The Rigor Auditor catches 100% of three high-severity classes "
    "(fabricated claims, rebutted-branch leaks, over-claims), 91% of "
    "missing falsifications, but only **22% of orphan experiments**.\n\n"
    "| Injection type | Severity | n | Detected |\n"
    "|---|---|---:|---:|\n"
    "| Fabricated claim | Critical | 23 | 23 (100%) |\n"
    "| Rebutted-branch leak | Critical | 23 | 23 (100%) |\n"
    "| Over-claim (scope) | Major | 23 | 23 (100%) |\n"
    "| Missing falsification | Major | 23 | 21 (91%) |\n"
    "| Orphan experiment | Minor | 23 | 5 (22%) |\n"
    "| **Overall** | | **115** | **95 (82.6%)** |\n\n"
    "The asymmetry is interpretable: orphans require enumerating "
    "every experiment and cross-checking its `Verifies` target, "
    "whereas the other four surface naturally inside the auditor's "
    "per-claim loop. The natural fix is to move orphan detection into "
    "Level 1 as a deterministic structural check.",
    title="Mutation benchmark: 82.6% overall; orphan-experiment is a known blind spot",
    metadata={"source_table": "Table 4 (artifacts/2604.24658.pdf, p. 16); Table 14 (p. 46)"},
)

claim_llm_judge_pathologies = claim(
    "**Two LLM-as-judge pathologies emerge in Rigor Auditor scoring.** "
    "(i) **Grade inflation**: in 17 of 23 ARAs, the auditor's reported "
    "overall mean is rounded up *just enough* to clear the Accept "
    "threshold. (ii) **Finding-score decoupling**: even when the "
    "auditor correctly flags an injection as `critical` (22/23 "
    "rebutted-branch-leak cases), the corresponding dimension score "
    "does not drop to the level the rubric prescribes "
    "(D5 ∈ {3,4} despite anchors prescribing 1 or 2). Both are "
    "documented LLM-as-judge failure modes [@Zheng2023LLMJudge]; the "
    "remedy: have LLMs *generate findings* but compute the overall "
    "verdict deterministically from the findings list.",
    title="Auditor pathologies: grade inflation + finding-score decoupling",
)

claim_seal_l3_equals_reproduction = claim(
    "**Level 3 = Reproduction-evaluation protocol.** Level 3's "
    "specification (read the artifact, reproduce central claims "
    "directionally under a compute budget, with numerical results "
    "masked) is exactly the ARA-condition protocol of the Reproduction "
    "experiment (§7.3). The **64.4% difficulty-weighted success rate** "
    "is therefore the Level-3 verification rate on well-formed "
    "artifacts; the single ARA fabrication caught by the blinded judge "
    "shows the verifier flags misrepresented results when they appear.",
    title="Level 3 effectiveness = 64.4% reproduction success on well-formed ARAs",
)

__all__ = [
    "claim_p1_automate_mechanical",
    "claim_p2_reproducibility_foundational",
    "claim_seal_level1_structural",
    "claim_seal_level2_rigor",
    "claim_seal_level3_execution",
    "claim_seal_certificate",
    "claim_three_stage_review_pipeline",
    "claim_seal_l1_empirical_validity",
    "claim_rigor_auditor_mutation_results",
    "claim_llm_judge_pathologies",
    "claim_seal_l3_equals_reproduction",
]
