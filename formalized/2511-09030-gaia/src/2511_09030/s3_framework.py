"""Section 3: The MAKER Framework — Maximal Agentic Decomposition, Voting, and Red-Flagging"""

from gaia.lang import claim, setting, support, deduction, complement

from .motivation import (
    setting_mdap_framework,
    setting_llm_error_rate,
    single_agent_infeasible,
)

# --- Section 3.1: Maximal Agentic Decomposition (MAD) ---

setting_mad_definition = setting(
    "Maximal Agentic Decomposition (MAD) is the extreme case of task decomposition where "
    "m=1, i.e., each subtask consists of exactly one step. A templating function phi maps "
    "the current state x_i and subtask specification to an LLM prompt. Extractors psi_a "
    "and psi_x parse the action and next state from the LLM response. The solution is "
    "computed recursively: r_{i+1} ~ M(phi(x_i)), a_{i+1} = psi_a(r_{i+1}), "
    "x_{i+1} = psi_x(r_{i+1}) for i = 0, ..., s-1.",
    title="Maximal Agentic Decomposition (MAD) formal definition",
)

# --- Leaf claim capturing the key consequence of MAD ---

mad_one_step_per_agent = claim(
    "Under MAD (m=1), each agent in the system is responsible for exactly one step of "
    "the task. Each agent's input consists solely of the current state and the overall "
    "strategy — no history of prior actions is included in the context. "
    "This is by design: the entire MAKER system is built on this one-step-per-agent principle.",
    title="MAD assigns exactly one step per agent with bounded context",
)

mad_reduces_context = claim(
    "With MAD (m=1 step per agent), each agent's context is limited to the minimal "
    "information needed to execute its single assigned step, consisting of the overall "
    "strategy and the current state. This focused context prevents the confusion from "
    "irrelevant prior steps that accumulates in single-agent approaches, and allows the "
    "use of smaller LLMs with more limited context sizes.",
    title="MAD reduces per-agent context burden",
)

strat_mad_reduces_context = support(
    [mad_one_step_per_agent],
    mad_reduces_context,
    reason=(
        "Because each agent (@mad_one_step_per_agent) handles exactly one step and "
        "receives only the current state plus strategy — not the full history of prior "
        "actions — its context is structurally bounded to a constant amount per step. "
        "This directly addresses the context-growth problem identified in the motivation."
    ),
    prior=0.97,
    background=[setting_llm_error_rate],
)

mad_enables_error_correction = claim(
    "The modularity induced by MAD (one step per agent) makes error correction at the "
    "subtask level both effective and scalable: because each agent handles a single step, "
    "multiple independent samples of that step can be drawn cheaply, and voting can be "
    "applied to identify the correct action. This is impossible or prohibitively expensive "
    "with a single large LLM call.",
    title="MAD modularity enables efficient per-step error correction",
)

strat_mad_error_correction = support(
    [mad_reduces_context],
    mad_enables_error_correction,
    reason=(
        "Because each agent's output (@mad_reduces_context) is limited to a single step's "
        "action and next state, the cost of resampling a step is bounded by the cost of "
        "one LLM call. This enables applying voting across multiple independent samples "
        "at a fixed, bounded cost per step — a capability that does not exist when all "
        "s steps are bundled into a single agent call."
    ),
    prior=0.92,
)

# --- Section 3.2: First-to-ahead-by-k Voting and Scaling Laws ---

setting_voting_algorithm = setting(
    "First-to-ahead-by-k voting: For each step, independent samples (votes) are drawn "
    "from the LLM agent. Let V[y] be the vote count for candidate y. A candidate y wins "
    "when V[y] >= k + max_{v != y} V[v], i.e., when it leads all other candidates by "
    "at least k votes. This is equivalent to the gambler's ruin framework where the "
    "correct answer races against the single most-likely alternative.",
    title="First-to-ahead-by-k voting algorithm definition",
)

setting_voting_formula = setting(
    "Scaling law derivation: For a task with s steps, per-step success rate p, "
    "decomposition level m (steps per subtask), and vote margin k, the key probabilities are: "
    "p_vote = p^m (probability correct vote for a subtask of m steps), "
    "p_alt = (1-p)*p^(m-1) (probability of alternative), "
    "p_sub = 1 / (1 + ((1-p)/p)^k) (probability voting succeeds on one subtask, "
    "from gambler's ruin hitting probability), "
    "p_full = p_sub^(s/m) = (1 + ((1-p)/p)^k)^(-s/m) (probability full task succeeds). "
    "These are Equations 10-13 in [@Meyerson2025].",
    title="Voting scaling law formulas (Eqs. 10-13)",
)

voting_pfull_high_mad = claim(
    "Under MAD (m=1), the full-task success probability p_full = (1 + ((1-p)/p)^k)^(-s) "
    "can be maintained arbitrarily close to 1 for any per-step success rate p > 0.5, "
    "by choosing a sufficiently large vote margin k. For a 1-million-step task, "
    "high probability of success is achievable with practical values of k even when "
    "the per-step error rate approaches 1-in-10 (p=0.9).",
    title="Voting maintains near-perfect reliability at 1M steps for any p > 0.5",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 3a"},
)

strat_voting_pfull = deduction(
    [mad_one_step_per_agent],
    voting_pfull_high_mad,
    reason=(
        "Plugging m=1 (the MAD condition from @mad_one_step_per_agent) into the p_full "
        "formula gives p_full = (1 + ((1-p)/p)^k)^(-s). As k increases, ((1-p)/p)^k "
        "shrinks toward 0 for any p > 0.5 (since (1-p)/p < 1), making p_full approach 1. "
        "This is a mathematical consequence of the gambler's ruin hitting probability "
        "formula applied to the voting structure."
    ),
    prior=0.99,
    background=[setting_voting_formula, setting_voting_algorithm, setting_mad_definition],
)

cost_scales_log_linearly = claim(
    "Under MAD (m=1), the expected cost to solve an s-step task with target reliability t "
    "scales as Theta(s * ln(s)): E[cost] = Theta(p^(-1) * c * s * ln(s)) where c is "
    "the cost per LLM sample. Specifically, k_min = Theta(ln(s)) votes are required "
    "per step (Eq. 14), and the ln(s) factor corresponds to votes that can be parallelized. "
    "Thus the parallelized wall-clock time cost scales only as Theta(ln(s)).",
    title="MAKER cost scales log-linearly with number of steps under MAD",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 4b"},
)

strat_log_linear_cost = deduction(
    [mad_one_step_per_agent],
    cost_scales_log_linearly,
    reason=(
        "With m=1 (MAD, from @mad_one_step_per_agent), the scaling law formula gives "
        "p_sub = 1/(1 + ((1-p)/p)^k). Inverting for k_min at target success probability "
        "t yields k_min = Theta(ln(s)) (Appendix B of [@Meyerson2025]). Gambler's ruin "
        "hitting time (Eq. 16) then yields total cost Theta(c * s * k_min) = "
        "Theta(c * s * ln(s)). The ln(s) factor can be parallelized, reducing wall-clock "
        "time to Theta(ln(s))."
    ),
    prior=0.99,
    background=[setting_voting_formula, setting_voting_algorithm, setting_mad_definition],
)

cost_exponential_with_m = claim(
    "When each agent is assigned m > 1 steps per subtask, the expected cost to complete "
    "an s-step task with reliability t scales exponentially in m: E[cost] = Theta(p^(-m) * "
    "c * s * ln(s)). Concretely, for a 1-million-step task with p=0.99 and t=0.9, the "
    "expected cost for m=100 steps/agent is many orders of magnitude higher than for m=1. "
    "This makes non-maximal decomposition infeasible for large s.",
    title="Non-maximal decomposition causes exponential cost explosion",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 5"},
)

strat_exp_cost = deduction(
    [mad_reduces_context],
    cost_exponential_with_m,
    reason=(
        "From the scaling law (Eq. 15): the cost per vote is c_vote = c*m / p^(m-1). "
        "The expected cost per subtask (Eq. 16) multiplied by s/m subtasks yields total "
        "cost Theta(p^(-m) * c * s * ln(s)) (Eq. 17). @mad_reduces_context established "
        "that MAD (m=1) is the baseline; any m > 1 introduces the p^(-m) exponential "
        "factor, which grows without bound as m increases for any p < 1. This makes "
        "non-maximal decomposition infeasible for large tasks."
    ),
    prior=0.99,
    background=[setting_voting_formula, setting_mad_definition],
)

alt_single_agent = claim(
    "A non-decomposed single-agent approach (m = s, one LLM call for the entire task) "
    "is the alternative to MAD. Its expected cost for high reliability grows as p^(-s), "
    "an exponential in s — completely infeasible for s = 1,000,000.",
    title="Single-agent alternative: exponential cost in s",
)

strat_single_agent_infeasible_s3 = support(
    [alt_single_agent],
    single_agent_infeasible,
    reason=(
        "@alt_single_agent establishes that the expected cost of the single-agent approach "
        "grows as p^(-s) — exponential in the number of steps s. For s=1,000,000 and any "
        "p < 1 (i.e., any non-perfect LLM), this is astronomically large, making the "
        "approach infeasible. This confirms the theoretical argument that motivated MAKER."
    ),
    prior=0.97,
    background=[setting_voting_formula],
)

# Note: these two claims are related but NOT XOR complements — a hybrid partial
# decomposition could make both partially false. We model them as separate claims
# connected via the strat_single_agent_infeasible_s3 support chain.

# --- Section 3.3: Red-Flagging ---

setting_red_flag_types = setting(
    "Red-flagging discards LLM responses with high-level indicators of unreliability "
    "before they enter the vote count. Two red flag types are used: "
    "(1) Overly long responses (exceeding a max token cutoff), indicating the model is "
    "over-analyzing a situation in a cycle of confusion. "
    "(2) Incorrectly formatted responses (failing to match the required output schema), "
    "indicating the model's reasoning has gone off the rails. "
    "Flagged responses are discarded and a new sample is drawn, at bounded cost under MAD.",
    title="Red-flagging criteria: long responses and formatting errors",
)

red_flag_reduces_correlation = claim(
    "Red-flagging (discarding long or malformatted LLM responses) reduces correlated "
    "errors across independent voting samples. Responses that are incorrectly formatted "
    "or overly long indicate the LLM has been conditioned into an anomalous state that "
    "also makes other parts of its reasoning incorrect. Discarding such responses prevents "
    "multiple correlated wrong votes from all being wrong for the same systematic reason.",
    title="Red-flagging reduces correlated errors across votes",
)

red_flag_enables_mad = claim(
    "Because MAD limits each agent to one step (bounded cost per call), the cost of "
    "discarding a flagged response and resampling is affordable. Red-flagging therefore "
    "becomes a practical mechanism under MAD that would be prohibitively expensive in "
    "a single large agent call covering all s steps.",
    title="MAD makes red-flag resampling affordable",
)

strat_red_flag_correlation = support(
    [red_flag_enables_mad],
    red_flag_reduces_correlation,
    reason=(
        "@red_flag_enables_mad establishes that resampling is affordable under MAD. "
        "Given that overly long or malformatted responses signal a pathological LLM state "
        "(per the red-flagging criteria) where reasoning is likely compromised, discarding "
        "such responses removes samples that are both wrong AND correlated with each other. "
        "This directly reduces the collision rate (multiple votes wrong for the same reason), "
        "preserving the i.i.d. assumption required for voting to provide reliable error "
        "correction."
    ),
    prior=0.82,
    background=[setting_red_flag_types, setting_mad_definition],
)

strat_red_flag_enables = support(
    [mad_one_step_per_agent],
    red_flag_enables_mad,
    reason=(
        "@mad_one_step_per_agent ensures each agent call costs a fixed, bounded amount. "
        "When a response is flagged and discarded, the cost of a replacement call is "
        "also bounded. This makes the resampling loop in red-flagging affordable."
    ),
    prior=0.95,
    background=[setting_red_flag_types],
)
