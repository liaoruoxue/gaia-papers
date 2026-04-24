"""Introduction and Motivation — CUA Verifier Design"""

from gaia.lang import claim, setting, question

# --- Settings: formal problem setup ---

cua_task_model = setting(
    "A computer use agent (CUA) task is modeled as a tuple $(g, \\mathcal{E})$, "
    "where $g$ is a natural-language goal and $\\mathcal{E}$ is a computer environment "
    "with an observable graphical interface. An agent produces a trajectory "
    "$\\tau = (s_0, a_1, s_1, a_2, \\ldots, a_T, s_T)$ where $s_t$ is a screenshot "
    "and $a_t$ is an action (click, type, scroll). $T$ varies from a handful of steps "
    "to hundreds of steps.",
    title="CUA task and trajectory definition",
)

verifier_formal_def = setting(
    "A verifier is defined as a function $V : (g, \\tau) \\rightarrow \\mathcal{R}$ "
    "mapping a goal and trajectory to a structured scoring response. "
    "Verifier quality is defined as agreement with a human oracle "
    "$V^* : (g, \\tau) \\rightarrow \\mathcal{R}$, measured by precision, recall, "
    "and Cohen's $\\kappa$ over a labeled set of trajectories.",
    title="Formal definition of verifier and verifier quality",
)

# --- Questions ---

q_did_agent_succeed = question(
    "Did the computer use agent actually succeed at the given task?",
    title="Core verification question",
)

# --- Claims from Introduction ---

cua_trajectories_hard_to_verify = claim(
    "Computer use agent (CUA) trajectories are long, visually rich, and ambiguous, "
    "making human annotation both challenging and expensive. Unlike text generation "
    "tasks where outputs can be compared directly, CUA success may be partially "
    "completed, achieved through unexpected paths, or fail subtly in a screenshot "
    "buried deep in a multi-step interaction.",
    title="CUA trajectories are difficult to verify",
)

verifier_errors_compound = claim(
    "Errors in a CUA verifier compound: a verifier that gets it wrong corrupts "
    "both evaluation benchmarks and training data (reinforcement learning signals). "
    "Without reliable verification, neither evaluation nor training signal can be trusted.",
    title="Verifier errors corrupt both evaluation and training",
)

four_principles_sufficient = claim(
    "Four design principles are sufficient to build a verifier (the Universal Verifier) "
    "that agrees with humans as often as humans agree with each other: "
    "(1) constructing rubrics with non-overlapping criteria, "
    "(2) separating process and outcome rewards, "
    "(3) distinguishing controllable vs. uncontrollable failures, "
    "(4) divide-and-conquer screenshot context management.",
    title="Four design principles for best-in-class CUA verifier",
)

existing_verifiers_inadequate = claim(
    "Existing CUA trajectory verifiers (WebVoyager GPT-4o, WebJudge o4-mini) have "
    "false positive rates of 45% and 22% respectively on outcome labels, "
    "and Cohen's $\\kappa$ of 0.31 and 0.44 (internal dataset), far below "
    "the human inter-annotator agreement level.",
    title="Existing verifiers have high false positive rates",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

gains_are_architectural = claim(
    "The Universal Verifier's performance advantage over WebVoyager and WebJudge "
    "stems from architectural design choices (rubric decomposition, two-pass scoring, "
    "structured outcome verification), not merely from using a stronger backbone LLM. "
    "Upgrading WebVoyager's GPT-4o and WebJudge's o4-mini to GPT-5.2 yields only "
    "modest Cohen's $\\kappa$ improvements (WebVoyager: 0.31 → 0.43 on Internal outcome) "
    "while dramatically increasing false negative rates (WebVoyager FNR: 0.24 → 0.44).",
    title="UV advantage is architectural, not model-driven",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

auto_research_70pct = claim(
    "An auto-research agent (Claude Code v2.1.87 with Claude Opus 4.6, 1M context) "
    "achieves approximately 70% of human expert verifier quality in approximately "
    "5% of the time (one day vs. three weeks of expert iteration), but fails to "
    "independently discover the structural design decisions that drive the largest "
    "gains in Cohen's $\\kappa$.",
    title="Auto-research agent achieves 70% of expert quality in 5% of the time",
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 1"},
)

human_expert_complementary_to_auto = claim(
    "Human expertise and automated optimization play complementary roles in verifier "
    "design: human expertise is essential for discovering core design principles "
    "(large structural changes causing step-function $\\kappa$ improvements), "
    "while automated optimization excels at fine-grained tuning. When initialized "
    "from the human expert's best configuration, the auto-research agent surpasses "
    "the expert-designed peak.",
    title="Human expertise and auto-research are complementary",
)
