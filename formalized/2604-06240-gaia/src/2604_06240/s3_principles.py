"""Section 3 — What is True of Good Verifiers: Four Design Principles"""

from gaia.lang import claim, setting

# --- Settings ---

process_score_formula = setting(
    "The process score is defined as "
    "$r_{\\text{proc}} = \\frac{\\sum_{i \\in \\mathcal{A}} \\text{earned\\_points}_i}"
    "{\\sum_{i \\in \\mathcal{A}} \\text{max\\_points}_i}$, "
    "where $\\mathcal{A}$ is the set of applicable rubric criteria "
    "(those whose conditions are met or that are unconditional). "
    "The process score is normalized to $[0, 1]$.",
    title="Process score formula",
)

relevance_matrix_def = setting(
    "The relevance matrix $\\mathbf{R} \\in \\mathbb{R}^{(T+1) \\times N}$ "
    "is produced by scoring each of the $T+1$ screenshots against each of "
    "the $N$ rubric criteria. For each criterion $c_j$, the top-$k$ most "
    "relevant screenshots $S_j \\subseteq \\{s_0, \\ldots, s_T\\}$ with $|S_j| \\leq k$ "
    "are selected for further evidence analysis.",
    title="Screenshot relevance matrix definition",
)

# --- Principle 1: Rubric design ---

rubric_quality_critical = claim(
    "Good rubric design is the single most impactful design decision for a CUA verifier: "
    "flawed rubrics produce errors that cascade through the pipeline and cannot be "
    "corrected downstream. Iterative development evidence shows that rubric design "
    "alone accounted for roughly half of the Cohen's $\\kappa$ gains over 32 expert experiments.",
    title="Rubric quality is the dominant factor in verifier quality",
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 1"},
)

phantom_criteria_failure = claim(
    "LLM-generated rubrics frequently introduce requirements never stated in the task "
    "(phantom criteria), inflating the denominator of the process score and over-penalizing "
    "agents that completed the actual task. For example, when asked to find a live music "
    "event on Eventbrite and songs on Spotify, the old rubric added criteria for ticket "
    "information, event links, and Spotify URLs — none of which the user requested. "
    "This turned a 5/6 SUCCESS into a 5/9 FAILURE.",
    title="Phantom criteria failure mode: unrequested requirements penalize correct agents",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 4"},
)

cascading_criteria_failure = claim(
    "When rubric criteria are not logically independent, a single upstream scoring error "
    "propagates into downstream criteria, multiplying the point penalty. For example, "
    "if 'identify the correct neighbourhood' is criterion 1 and 'search for hotels in "
    "that neighbourhood' is criterion 2, a mis-label on criterion 1 causes the agent "
    "to lose points on criterion 2 even if downstream actions were internally consistent.",
    title="Cascading criteria failure mode: dependent criteria multiply penalties",
)

separate_generation_scoring = claim(
    "Generating the rubric and scoring the trajectory in a single LLM call leads to "
    "confirmation bias: the model creates criteria tailored to the agent's behavior "
    "rather than the task requirements. Separating rubric generation (from the task "
    "alone, without seeing the trajectory) from scoring eliminates this coupling.",
    title="Rubric generation must be separated from scoring to avoid confirmation bias",
)

conditional_criteria_design = claim(
    "Some rubric criteria are conditional on the state of the world discovered during "
    "task execution (e.g., 'report window-seat cost if a direct flight exists'). "
    "Conditional criteria must be marked at rubric-generation time and excluded from "
    "both numerator and denominator of the process score when their condition is not met, "
    "ensuring agents are not penalized for outcomes they could not control.",
    title="Conditional criteria prevent penalizing agents for uncontrollable outcomes",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 5"},
)

two_pass_hallucination_detection = claim(
    "Scoring each rubric criterion twice — once with only the agent's text action history "
    "(to check grounding) and once with full screenshot access (to verify visual state) — "
    "surfaces discrepancies that flag potential hallucinations. Screenshots take precedence "
    "over agent claims when they conflict.",
    title="Two-pass scoring detects hallucinations by comparing text-only and screenshot-grounded scores",
)

# --- Principle 2: Process vs Outcome ---

process_outcome_separation = claim(
    "Process and outcome rewards must be reported as two independent signals per trajectory "
    "because the environment plays an outsized role in CUA task success. Conflating them "
    "leads to reward signals that are either too lenient (crediting agents for effort when "
    "the user gets nothing) or too harsh (penalizing agents for factors outside their control). "
    "The process score $r_{\\text{proc}} \\in [0,1]$ reflects execution quality; the outcome "
    "score $r_{\\text{out}} \\in \\{0,1\\}$ reflects whether the user's goal was achieved.",
    title="Process and outcome rewards must be separated to produce fair signals",
    background=[process_score_formula],
)

process_outcome_diverge_on_blockers = claim(
    "Process and outcome scores diverge specifically on environment blocker scenarios: "
    "when an agent is blocked by a login wall, CAPTCHA, out-of-stock item, or other "
    "uncontrollable factor, the process score awards full credit for best-effort execution "
    "while the outcome score marks failure because the user's real-world goal was not achieved. "
    "An agent can thus score 100% on process but 0% on outcome.",
    title="Environment blockers cause process success with outcome failure",
)

outcome_label_primary_intent = claim(
    "The outcome label should focus on primary intent: if the primary intent is to book "
    "a table, the user is flexible on which platform is used unless otherwise stated. "
    "Users are forgiving of nitpicks (rounding \\$5.95 to \\$6) but not forgiving of "
    "unsolicited side effects (buying a warranty when only the product was requested) "
    "or hallucinations (fabricating information).",
    title="Outcome label focuses on primary intent and ignores nitpicks",
)

# --- Principle 3: Controllable vs Uncontrollable ---

controllable_vs_uncontrollable = claim(
    "A CUA verifier must explicitly distinguish controllable from uncontrollable failures. "
    "Uncontrollable factors (not penalized in process): platform/infrastructure issues "
    "(CAPTCHA, login walls), entity non-existence (discontinued products, closed businesses), "
    "availability constraints (out of stock), and search result limitations. "
    "Controllable factors (penalized in process): intent mismatches (wrong product), "
    "reasoning errors, hallucinations, insufficient effort (single failed attempt), "
    "and execution errors (skipping required steps).",
    title="Taxonomy of controllable vs. uncontrollable CUA failure factors",
)

cascading_error_free_scoring = claim(
    "A cascading-error-free scoring strategy ensures that a single early obstacle does not "
    "unfairly penalize all downstream steps. Each rubric criterion is graded based on "
    "whether the agent's actions were reasonable given the information it had at that step, "
    "not whether upstream criteria were scored correctly.",
    title="Cascading-error-free rubric prevents upstream errors from multiplying downstream penalties",
)

# --- Principle 4: Context management ---

screenshot_needle_in_haystack = claim(
    "Providing all screenshots in a single LLM context window forces the LLM to solve "
    "a needle-in-a-haystack problem that scales poorly with longer trajectories. "
    "WebVoyager includes all screenshots; WebJudge ranks the top 30-50. Restricting "
    "to only the last few screenshots risks missing task-relevant evidence from earlier "
    "in the trajectory.",
    title="Naive screenshot context management scales poorly and misses evidence",
)

relevance_matrix_approach = claim(
    "Scoring each screenshot against every rubric criterion to produce a relevance matrix "
    "$\\mathbf{R} \\in \\mathbb{R}^{(T+1) \\times N}$, then grouping the top-$k$ most relevant "
    "screenshots per criterion for further analysis, is more scalable to longer trajectories "
    "and more focused than passing all screenshots. Processing is parallelized: $M$ screenshots "
    "are scored against all $N$ criteria in $M$ parallel LLM calls.",
    title="Per-criterion screenshot relevance matrix enables scalable, focused evidence analysis",
    background=[relevance_matrix_def],
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 6"},
)

# --- Unsolicited side effects ---

unsolicited_side_effects = claim(
    "Unsolicited agent actions with material side effects (e.g., adding unrequested "
    "items to a cart, enrolling in unrequested services) cannot be anticipated at rubric "
    "generation time. They require a dedicated detection pass over the trajectory. "
    "Unsolicited side effects almost always result in outcome failure; they only partially "
    "penalize the process score, weighted by severity.",
    title="Unsolicited side effects require a dedicated detection pass",
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 7"},
)
