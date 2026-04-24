"""Section 4 — Universal Verifier System"""

from gaia.lang import claim, setting
from .s3_principles import (
    rubric_quality_critical,
    separate_generation_scoring,
    conditional_criteria_design,
    two_pass_hallucination_detection,
    process_outcome_separation,
    controllable_vs_uncontrollable,
    relevance_matrix_approach,
    unsolicited_side_effects,
)

# --- Settings ---

uv_algorithm_overview = setting(
    "The Universal Verifier (UV) operates in three phases: "
    "(1) rubric creation: generate $N$ disjoint, meaningful criteria $\\mathcal{C} = \\{c_1, \\ldots, c_N\\}$ from the goal $g$; "
    "(2) multimodal scoring: score each screenshot against every criterion (relevance matrix), "
    "select top-$k$ per criterion, extract evidence, resolve conditional criteria, "
    "perform reality check, rescore with screenshot evidence, detect side effects; "
    "(3) outcome judgment and error diagnosis. "
    "Steps 7-9 (rescoring, side-effect detection, outcome verification) can be run "
    "as multiple parallel instances with process score = median and outcome = majority vote.",
    title="Universal Verifier three-phase architecture",
)

error_taxonomy_setting = setting(
    "The Universal Verifier uses a hand-crafted error taxonomy with 7 categories "
    "and 24 subcodes: (1) Selection errors (missing intent, unauthorized substitution, "
    "wrong action type, wrong values/constraint violation); (2) Hallucination errors "
    "(output contradiction, action contradiction, output fabrication, action fabrication); "
    "(3) Execution and Strategy errors (computational mistakes, platform non-compliance, "
    "incomplete delivery, environment failure, incomplete task execution); "
    "(4) Critical Point errors (premature stop, violation); "
    "(5) Task Ambiguity; (6) Side-Effect errors; (7) Tool Interaction errors.",
    title="CUA failure error taxonomy: 7 categories, 24 subcodes",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 10"},
)

visual_evidence_taxonomy_setting = setting(
    "Five categories for evaluating agent claims against screenshot evidence: "
    "(1) Contradiction: screenshots show X, agent claims not-X — Failure; "
    "(2) Fabrication: agent claims X with zero evidentiary basis — Failure; "
    "(3) Omission: agent did not view all needed screenshots and X is commonly known — Failure; "
    "(4) Supported inference from absence: screenshots show no evidence of X across all pages AND X is not commonly known — Success; "
    "(5) Visual confirmation without explicit statement: screenshots visually confirm the correct result — Success. "
    "Screenshots take precedence over agent claims.",
    title="Visual evidence taxonomy: 5 categories for grounding agent claims",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 7"},
)

cost_structure_setting = setting(
    "LLM call count per UV pipeline step for a trajectory with $M$ screenshots, "
    "$N$ rubric criteria, $K$ max screenshots per criterion, $S$ unique screenshots selected: "
    "Step 1 (rubric generation): 3 calls; "
    "Step 2 (relevance scoring): $M$ calls, fully parallel; "
    "Step 4 (evidence analysis, batched): $S \\leq K \\times N$ calls, fully parallel; "
    "Steps 5-8: 1 call each. "
    "For a typical trajectory ($M=47$, $N=3$, $K=5$, $S=10$): 65 LLM calls total without majority voting.",
    title="Universal Verifier LLM call cost breakdown",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 8"},
)

# --- System claims ---

uv_design_invariant = claim(
    "The key design invariant of the Universal Verifier is that no relevant screenshot "
    "evidence can go undetected in the pipeline. This is specifically designed to not miss "
    "any hallucinations — which can be subtle (e.g., an agent reporting '+6.2% CIDEr score' "
    "when the paper shows '+2.8% CIDEr', a discrepancy that humans are likely to miss).",
    title="UV design invariant: no relevant screenshot evidence goes undetected",
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 5"},
)

uv_incorporates_all_principles = claim(
    "The Universal Verifier incorporates all four design principles from Section 3: "
    "per-task success criteria rubric generation (Principle 1), "
    "separate process and outcome scores (Principle 2), "
    "controllable/uncontrollable distinction via rubric criteria fields (Principle 3), "
    "and per-criterion relevance matrix screenshot selection (Principle 4).",
    title="UV integrates all four design principles",
    background=[uv_algorithm_overview],
)

uv_richer_output = claim(
    "The Universal Verifier outputs a richer response $r = (r_{\\text{proc}}, r_{\\text{out}}, d)$ "
    "than binary verifiers: a process score $r_{\\text{proc}} \\in [0,1]$ (normalized rubric score), "
    "an outcome score $r_{\\text{out}} \\in \\{0,1\\}$ (binary success/failure), and a diagnostic "
    "report $d$ that classifies and localizes each failure within the trajectory using "
    "the 7-category error taxonomy.",
    title="UV produces structured output: process score, outcome label, and diagnostic report",
    background=[error_taxonomy_setting],
)

verifier_needs_all_screenshots = claim(
    "A verifier that inspects only the final screenshot $s_T$ or a fixed subset "
    "$\\{s_{t_1}, \\ldots, s_{t_k}\\} \\subset \\tau$ is a strict approximation of the human oracle "
    "$V^*$ and systematically underperforms on trajectories where $T$ is large, "
    "because critical state changes occur at arbitrary timesteps. "
    "Reliable verification requires attending to all $T+1$ observations.",
    title="Reliable verification requires attending to all screenshots in a trajectory",
)

screenshot_staircase_pattern = claim(
    "The relevance matrix for typical CUA trajectories exhibits a 'staircase' shape: "
    "later screenshots are most relevant to later rubric criteria, reflecting that "
    "most trajectories are relatively linear (progress through sub-goals in order). "
    "The UV exploits this by using recency as a tie-breaking rule for equal relevance scores.",
    title="Relevance matrix shows staircase pattern reflecting linear trajectory structure",
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 6"},
)
