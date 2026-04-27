"""Section 3: Method - Agentic Verifier framework and AgentV-RL training recipe."""

from gaia.lang import claim, setting, support, deduction

from .motivation import paradigm_shift_claim


# --- Task definition / settings ---

bon_setting = setting(
    "Parallel Scaling (Best-of-N): for input x, the actor samples k candidate solutions "
    "{y(j)}; the verifier scores each candidate via the True-token logit of its verifying "
    "rationale and selects the highest-confidence one."
)

sequential_setting = setting(
    "Sequential Scaling: given query x and an initial solution y0, the verifier produces a "
    "critique f0; the actor then refines its solution iteratively, "
    "y_t ~ pi_theta(x, y0, f0, ..., y_{t-1}, f_{t-1})."
)

forward_agent_setting = setting(
    "Forward agent: starting from problem premises, sequentially traces the solution path "
    "via a Plan-Validate-Verdict pipeline, validating that each step v_{i-1} is a sufficient "
    "condition for v_i. Empowered to invoke a Python interpreter and to interleave "
    "Thought-Action-Observation rounds."
)

backward_agent_setting = setting(
    "Backward agent: reasons in reverse from the final answer back to the problem statement "
    "via the same Plan-Validate-Verdict pipeline, checking that all required problem "
    "constraints are fulfilled (necessity check)."
)

agentv_setting = setting(
    "AgentV-RL training recipe: synthetic data engine that role-plays forward and backward "
    "agents to generate verification trajectories with quality control, followed by a "
    "two-stage schema of rejection-sampling SFT and Group Relative Policy Optimization "
    "(GRPO) reinforcement learning. The verifier is trained on 15K SFT and 50K RL samples "
    "starting from Qwen3-4B."
)

grpo_setting = setting(
    "GRPO objective uses a clipped importance ratio with a KL-to-reference penalty and "
    "filters zero-variance reward groups; binary outcome reward r=1 if predicted verdict "
    "matches ground truth, else -1; compiler execution observations are excluded from the "
    "loss to mitigate environment memorization."
)


# --- Core method claims ---

forward_sufficiency_claim = claim(
    "The forward agent performs sufficiency checking by validating that each preceding step "
    "is a sufficient condition for the subsequent derivation.",
    background=[forward_agent_setting],
)

backward_necessity_claim = claim(
    "The backward agent performs necessity checking by validating that the solution is "
    "grounded in the original problem constraints.",
    background=[backward_agent_setting],
)

bidirectional_design_claim = claim(
    "Coordinating a forward (sufficiency) agent and a backward (necessity) agent yields a "
    "bidirectional, tool-augmented review that is more comprehensive than single-turn or "
    "unidirectional verification."
)

bidirectional_design_support = support(
    [forward_sufficiency_claim, backward_necessity_claim, paradigm_shift_claim],
    bidirectional_design_claim,
    reason="Sufficiency + necessity together cover both directions of logical entailment, "
           "instantiating the agentic paradigm.",
    prior=0.85,
)

tool_augmented_capability_claim = claim(
    "Both agents can iteratively decompose complex solutions into verifiable sub-steps and "
    "invoke external tools (e.g., a Python interpreter) for numerical calculation.",
    background=[forward_agent_setting, backward_agent_setting],
)

multi_agent_distillable_claim = claim(
    "The capability of the multi-agent forward+backward system can be distilled into a "
    "single LLM via the AgentV-RL recipe (synthetic-data SFT followed by GRPO RL).",
    background=[agentv_setting],
)

distillation_support = support(
    [bidirectional_design_claim, tool_augmented_capability_claim],
    multi_agent_distillable_claim,
    reason="A single LLM trained on synthetic forward/backward trajectories with tool use "
           "can reproduce the multi-agent behavior pattern.",
    prior=0.75,
)


# --- Algorithmic deduction: GRPO objective produces stable training when advantages are
# normalized within nonzero-variance groups (textbook-substitution-style claim).

grpo_objective_setting = setting(
    "Equation 8: J_GRPO(psi) = E[(1/G) sum_i (1/|H_i|) sum_t min(r_{i,t}*A_{i,t}, "
    "clip(r_{i,t}, 1-eps_low, 1+eps_high)*A_{i,t})] - beta * D_KL(pi_psi || pi_ref), "
    "with r_{i,t} the importance-sampling ratio; zero-variance reward groups are filtered."
)

grpo_stability_claim = claim(
    "Filtering zero-variance reward groups and using clipped importance ratios with a KL "
    "penalty yields a stable GRPO update for verifier training.",
    background=[grpo_objective_setting, grpo_setting],
)

grpo_stability_deduction = deduction(
    [multi_agent_distillable_claim],
    grpo_stability_claim,
    reason="Standard PPO/GRPO theory: clipping bounds the policy update; zero-variance "
           "filtering removes degenerate gradients; KL anchors the policy to a reference. "
           "Substituting these into the objective yields a stable update by construction.",
    prior=0.95,
    background=[grpo_objective_setting],
)
