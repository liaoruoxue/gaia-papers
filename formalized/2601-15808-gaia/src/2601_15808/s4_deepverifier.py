"""Section 4: DeepVerifier — three-stage multi-module verification framework"""

from gaia.lang import (
    claim, setting,
    support, deduction, abduction, compare,
)

from .motivation import asymmetry_of_verification, alternative_paradigm_claim
from .s3_taxonomy import taxonomy_five_categories, rubrics_from_taxonomy, high_token_count


# ── Architecture settings ─────────────────────────────────────────────────────

three_stage_architecture = setting(
    "DeepVerifier adopts a three-stage multi-module architecture: (1) a Decomposition Agent, "
    "(2) a Verification Agent, and (3) a Judge Agent. These modules operate sequentially on "
    "each DRA trajectory-answer pair.",
    title="DeepVerifier three-stage architecture",
)

ck_pro_as_verifier = setting(
    "The CK-Pro agent [@Fang2025b] is used as the Verification Agent in DeepVerifier experiments. "
    "CK-Pro is a modular multi-agent framework: a Main Agent orchestrates sub-agents that interact "
    "with specific resources (search, screenshot), each generating Python code for actions.",
    title="CK-Pro as verification agent implementation",
)

judge_scoring_rubric = setting(
    "The Judge Agent uses a 4-point scoring scale: 1 = entirely incorrect, 2 = mostly incorrect, "
    "3 = mostly correct, 4 = entirely correct. A score ≤ 2 is treated as incorrect (reject); "
    "a score ≥ 3 is treated as correct (accept) in scaling experiments.",
    title="Judge agent 4-point scoring scale",
)

# ── Decomposition module claims ────────────────────────────────────────────────

decomposition_three_steps = claim(
    "The Decomposition Agent operates in three steps:\n\n"
    "1. **Trajectory Summarization**: Produces a compact step-indexed synopsis of the trajectory, "
    "recording for each step the sources visited and concrete information retrieved (facts, numbers, "
    "quotes). Descriptive (not interpretive), enabling downstream checks without reloading the full trace.\n"
    "2. **Potential Error Identification**: Given the trajectory summary and failure taxonomy in the "
    "system prompt, identifies suspicious behaviors mapped to known failure modes as structured "
    "behavior⇒potential-error+taxonomy-label pairs with brief justifications.\n"
    "3. **Follow-Up Question Formulation**: Drafts high-leverage follow-up questions targeting "
    "flagged vulnerabilities. Each question is answerable via external evidence and designed to "
    "decisively confirm or refute a risky claim. Output is up to 3 source-question pairs.",
    title="Decomposition Agent: three-step workflow",
    background=[three_stage_architecture, taxonomy_five_categories, high_token_count],
)

strat_decomposition_design = support(
    [high_token_count, taxonomy_five_categories],
    decomposition_three_steps,
    reason=(
        "@high_token_count makes direct holistic verification infeasible, motivating step 1 "
        "(trajectory summarization). @taxonomy_five_categories provides the failure mode vocabulary "
        "for step 2 (error identification). The asymmetry of verification motivates step 3 (targeted "
        "follow-up questions that check only suspicious, specific claims rather than re-solving the "
        "full task). Together these constraints determine the three-step design of "
        "@decomposition_three_steps [@Wan2026]."
    ),
    background=[asymmetry_of_verification],
    prior=0.86,
)

targeted_subquestions = claim(
    "By focusing only on essential, potentially faulty claims, the Decomposition Agent allows the "
    "Verification Agent to build on well-grounded conclusions, ignore trivial details, and check "
    "only for suspicious or unsupported assertions — avoiding the same reasoning errors as the "
    "original DRA agent.",
    title="Targeted sub-questions avoid re-solving full task",
    background=[three_stage_architecture, asymmetry_of_verification],
)

strat_targeted_vs_holistic = support(
    [decomposition_three_steps],
    targeted_subquestions,
    reason=(
        "@decomposition_three_steps produces yes/no questions of the form 'Does source X state "
        "claim Y?' or 'What is the exact figure for Y in report X?' — these are factual lookups, "
        "not full re-solves. @targeted_subquestions follows because lookup tasks are substantially "
        "easier than the original research task, exploiting @asymmetry_of_verification."
    ),
    prior=0.84,
)

# ── Verification and judge module claims ──────────────────────────────────────

verification_agent_sequential = claim(
    "The Verification Agent sequentially retrieves answers to the follow-up questions generated "
    "by the Decomposition Agent. It uses the CK-Pro multi-agent framework, where the Main Agent "
    "decomposes each follow-up question into sub-tasks assigned to specialized Sub-Agents "
    "(search, screenshot, etc.).",
    title="Verification Agent: sequential follow-up answer retrieval",
    background=[ck_pro_as_verifier, three_stage_architecture],
)

judge_agent_evaluation = claim(
    "The Judge Agent evaluates the unverified answer based on: (1) the trajectory summary, "
    "(2) the potential error list, (3) the follow-up questions, and (4) their verified answers. "
    "It provides a concise explanation followed by a score on the 4-point scale. In feedback mode, "
    "the judge also provides actionable retry instructions and may suggest the correct answer "
    "if derivable from available information.",
    title="Judge Agent evaluation and feedback generation",
    background=[three_stage_architecture, judge_scoring_rubric],
)

# ── Ablation comparison claims ────────────────────────────────────────────────

full_deepverifier_performance = claim(
    "DeepVerifier (full system) achieves the following meta-evaluation performance on the GAIA-Web "
    "verification task (trajectories from CK-Pro with Claude-3.7-Sonnet backbone):\n\n"
    "| System | Precision | Recall | Accuracy | F1 |\n"
    "|--------|-----------|--------|----------|----|\n"
    "| DeepVerifier (full) | 75.00 | 71.43 | 75.56 | 73.17 |\n"
    "| − Verification module | 100.00 | 14.29 | 60.00 | 25.00 |\n"
    "| − Decomposition module | 86.96 | 47.62 | 72.22 | 61.54 |\n\n"
    "All values are percentages × 100.",
    title="DeepVerifier ablation: meta-evaluation F1 on GAIA-Web",
    background=[three_stage_architecture, judge_scoring_rubric, ck_pro_as_verifier],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 2"},
)

ablated_no_verification = claim(
    "Removing the Verification module (no follow-up question answering) yields 100% precision but "
    "only 14.29% recall and 60.00% accuracy (F1 = 25.00). The judge catches obvious execution "
    "failures but overlooks subtle reasoning or factual errors, accepting many incorrect answers "
    "as correct due to inability to detect secondary-source dependence, overconfident claims, "
    "or hallucinated facts.",
    title="Ablation: removal of Verification module",
    background=[three_stage_architecture],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 2"},
)

ablated_no_decomposition = claim(
    "Removing the Decomposition module (no targeted sub-question generation) yields 86.96% precision "
    "but only 47.62% recall and 72.22% accuracy (F1 = 61.54). Without proper decomposition, the "
    "verification agent attempts to check every step by re-solving the entire task, making it "
    "vulnerable to the same reasoning errors as the original agent.",
    title="Ablation: removal of Decomposition module",
    background=[three_stage_architecture],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 2"},
)

deepverifier_superiority = claim(
    "DeepVerifier (full system, F1 = 73.17) achieves a balanced precision-recall tradeoff and "
    "outperforms the ablated versions by 12%–48% in meta-evaluation F1 score: "
    "+48.17 F1 points over the no-Verification ablation and +11.63 F1 points over the "
    "no-Decomposition ablation. DeepVerifier also achieves the highest accuracy (75.56%) "
    "among all variants.",
    title="DeepVerifier outperforms ablations by 12-48% F1",
    background=[judge_scoring_rubric],
)

# Compare vs. no-verification baseline (the most dramatic ablation)
alt_no_verification_verifier = claim(
    "Holistic judge without verification (no follow-up question answering): achieves F1 = 25.00 "
    "with precision 100.00%, recall 14.29%, accuracy 60.00% on GAIA-Web DRA verification task.",
    title="Alternative: holistic judge without verification sub-tasks",
)

alt_no_decomp_verifier = claim(
    "Judge with verification but without decomposition: achieves F1 = 61.54 with precision 86.96%, "
    "recall 47.62%, accuracy 72.22% on GAIA-Web DRA verification task.",
    title="Alternative: verification without decomposition",
)

pred_deepverifier = claim(
    "DeepVerifier with full decomposition+verification predicts balanced precision-recall (F1 ≈ 73), "
    "because decomposition targets only suspicious claims while verification grounds them in evidence.",
    title="DeepVerifier predicted balanced precision-recall",
)

pred_holistic = claim(
    "Holistic judge without targeted sub-questions predicts high precision but low recall (F1 ≈ 25), "
    "because it can only detect obvious errors, missing subtle factual and reasoning failures.",
    title="Holistic judge predicted high precision, low recall",
)

comp_deepverifier_vs_holistic = compare(
    pred_deepverifier,
    pred_holistic,
    full_deepverifier_performance,
    reason=(
        "DeepVerifier's F1 (73.17) far exceeds the no-Verification ablation's F1 (25.00), "
        "confirming that targeted decomposition-based verification substantially improves recall "
        "over holistic judging without sacrificing overall performance. The observed 48% F1 "
        "improvement matches the prediction of @pred_deepverifier."
    ),
    prior=0.92,
)

s_h_deepverifier = support(
    [decomposition_three_steps, targeted_subquestions, rubrics_from_taxonomy],
    full_deepverifier_performance,
    reason=(
        "@decomposition_three_steps provides targeted follow-up questions, @targeted_subquestions "
        "ensures verification avoids re-solving errors, and @rubrics_from_taxonomy structures the "
        "evaluation dimensions. Together these explain the high recall (71.43%) of @full_deepverifier_performance."
    ),
    prior=0.88,
)

s_alt_holistic = support(
    [alt_no_verification_verifier],
    full_deepverifier_performance,
    reason=(
        "@alt_no_verification_verifier (holistic judge) achieves only F1 = 25.00, demonstrating "
        "that the full @full_deepverifier_performance cannot be explained by the holistic approach alone."
    ),
    prior=0.20,
)

abduction_deepverifier_effectiveness = abduction(
    s_h_deepverifier,
    s_alt_holistic,
    comp_deepverifier_vs_holistic,
    reason=(
        "Both DeepVerifier and the holistic judge attempt to explain the same verification task "
        "(GAIA-Web DRA trajectory assessment). @full_deepverifier_performance is the observation "
        "that DeepVerifier achieves F1 = 73.17. The hypothesis is that structured decomposition "
        "and targeted verification drive this performance; the alternative is that holistic judging "
        "alone suffices."
    ),
)

strat_deepverifier_final = support(
    [full_deepverifier_performance],
    deepverifier_superiority,
    reason=(
        "@full_deepverifier_performance provides the numerical basis: DeepVerifier F1 = 73.17, "
        "no-Verification F1 = 25.00, no-Decomposition F1 = 61.54. @deepverifier_superiority "
        "computes the 12%–48% improvement range from these values."
    ),
    prior=0.95,
)
