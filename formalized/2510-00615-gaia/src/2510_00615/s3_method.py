"""ACON method (Section 3): formal compression objective, guideline
optimisation via contrastive feedback, and distillation."""

from gaia.lang import claim, setting, support, deduction, infer

from .motivation import (
    agent_loop_setup,
    context_cost_definition,
    context_grows_unbounded,
    cost_scales_with_context,
    long_context_distracts,
    heuristics_inadequate,
    acon_is_gradient_free,
)

# 3.2 History & observation compression --------------------------------------

compressor_definition = setting(
    "ACON introduces a compressor LLM $f(\\cdot; \\phi, P)$ parameterised by "
    "pre-trained weights $\\phi$ and a natural-language compression guideline "
    "$P$. The compressor receives raw context and returns a condensed version.",
    title="Compressor module $f(\\cdot;\\phi,P)$",
)

history_compression_rule = setting(
    "**History compression** is applied selectively: $h'_t = f(h_t; \\phi, "
    "P_{hist})$ if $|h_t| > T_{hist}$, otherwise $h'_t = h_t$. The compressed "
    "history $h'_t$ then replaces the raw history in the agent's input.",
    title="History compression rule (Equation 3)",
)

observation_compression_rule = setting(
    "**Observation compression** is also applied selectively: $o'_t = f(o_t, "
    "h_{t-1}; \\phi, P_{obs})$ if $|o_t| > T_{obs}$, otherwise $o'_t = o_t$. The "
    "compressed observation replaces the raw one and is stored in the history.",
    title="Observation compression rule (Equation 4)",
)

context_is_world_model = claim(
    "The agent's context functions as a **world model** of the environment, "
    "encoding heterogeneous signal types: causal relations (e.g., 'sending email "
    "leaves drafts'), evolving states (e.g., 'account balance'), preconditions "
    "(e.g., 'login required') and decision cues (e.g., 'due dates'). Effective "
    "compression must therefore preserve all of these signal classes, not just "
    "verbatim text.",
    title="Agent context as world model",
)

acon_objective = setting(
    "The compressor parameters $\\psi \\triangleq (\\phi, P)$ are optimised to "
    "$\\max_{\\psi} \\mathbb{E}[R(s_T(\\psi))] - \\lambda \\mathbb{E}[C(H'(\\psi))]$, "
    "$\\lambda \\geq 0$ — a weighted combination of expected terminal task reward "
    "(maximise) and expected compressed-context cost (minimise).",
    title="ACON optimisation objective (Equation 6)",
)

# Why naive RL is hard

naive_rl_infeasible = claim(
    "Direct reinforcement learning of the compressor against the objective "
    "@acon_objective is impractical: (1) updating the compressor LLM's parameters "
    "$\\phi$ with RL is computationally prohibitive; (2) every reward signal "
    "requires an expensive multi-step rollout of both agent and compressor LLMs; "
    "(3) the policy-gradient estimator suffers high variance because the "
    "compression quality is only revealed indirectly through eventual task "
    "success; and there is no gold supervision for compression itself.",
    title="Naive RL on the ACON objective is infeasible",
)

reason_naive_rl = (
    "@acon_objective is non-differentiable in the discrete context cost and "
    "exposes only sparse terminal-state reward; combined with the cost of LLM "
    "rollouts (one full agent + compressor pass per reward sample) and the "
    "expense of fine-tuning $\\phi$ at scale, all three classical RL difficulties "
    "compound. The authors enumerate exactly these obstacles in Section 3.2."
)

strat_naive_rl_infeasible = support(
    [context_grows_unbounded, cost_scales_with_context],
    naive_rl_infeasible,
    background=[acon_objective, agent_loop_setup, compressor_definition],
    reason=reason_naive_rl,
    prior=0.85,
)

# 3.3 Guideline optimisation -------------------------------------------------

trajectory_dense_signal = claim(
    "Trajectory-level comparisons between agent runs **with** vs **without** "
    "compression supply a denser quality signal than scalar terminal rewards. "
    "Specifically, a task that succeeds with full context $H$ but fails with "
    "compressed context $H'$ pinpoints a concrete loss of information caused by "
    "the compressor.",
    title="Contrastive trajectories yield dense signal",
)

contrastive_subset_construction = setting(
    "Define the contrastive subset $D_{cont} \\subset D_{train}$ as those tasks "
    "where the agent succeeds with the full context $H$ but fails with the "
    "compressed context $H'$.",
    title="Contrastive subset $D_{cont}$",
)

textual_gradient_step = claim(
    "For each task in $D_{cont}$, an optimiser LLM produces natural-language "
    "feedback by contrasting $H$ and $H'$. Concatenating feedback across the "
    "batch and prompting the optimiser to revise the guideline ($P^{(0)} \\to "
    "P^{(1)}$) realises one step of textual gradient descent [@Yuksekgonul2025; "
    "@Khattab2024; @Pryzant2023] in natural language space.",
    title="Textual-gradient guideline update",
)

reason_textual_gradient = (
    "Given @trajectory_dense_signal, the contrastive subset @contrastive_subset_construction "
    "isolates exactly the failures attributable to compression. Feeding both "
    "trajectories plus a structured 'feedback instruction' to a strong LLM yields "
    "a critique that names the lost information; aggregating $n$ such critiques "
    "and asking the optimiser to rewrite the guideline corresponds to a batched "
    "natural-language gradient step in the textual gradient descent framework "
    "[@Yuksekgonul2025; @Khattab2024]. Multiple candidate prompts are generated "
    "and the best on $D_{cont}$ is selected (utility-maximisation step UT)."
)

strat_textual_gradient = support(
    [trajectory_dense_signal],
    textual_gradient_step,
    background=[contrastive_subset_construction, compressor_definition],
    reason=reason_textual_gradient,
    prior=0.9,
)

ut_step = setting(
    "**Utility-maximisation step (UT)**: produce candidate guidelines via the "
    "textual-gradient update and pick the one maximising task accuracy on "
    "$D_{cont}$. This primarily targets the first (reward) term of "
    "@acon_objective.",
    title="UT step",
)

co_step = setting(
    "**Compression-maximisation step (CO)**: a follow-up alternating update "
    "conditioned only on tasks that **succeeded with compression**, asking the "
    "optimiser to flag information that was unused. The resulting guideline "
    "$P^{(2)}$ encourages **shorter** but still sufficient contexts, targeting "
    "the second (cost) term of @acon_objective.",
    title="CO step",
)

acon_two_objective_addresses_tradeoff = claim(
    "Running UT followed by CO addresses both terms of the bi-objective in "
    "@acon_objective: UT raises task reward and CO trims unused context. As "
    "demonstrated experimentally (cf. Tables 1–2), the resulting ACON-UTCO "
    "variant tends to give the best joint accuracy/efficiency trade-off.",
    title="UT+CO addresses both terms of the objective",
)

reason_utco_addresses_tradeoff = (
    "@ut_step optimises the reward term of @acon_objective via "
    "@textual_gradient_step (justified above), while @co_step is an alternating "
    "second pass that explicitly targets the cost term using only successful "
    "compressed runs as evidence of removable content. Together they provide a "
    "gradient-free coordinate-descent-like procedure on @acon_objective."
)

strat_utco_addresses_tradeoff = support(
    [textual_gradient_step],
    acon_two_objective_addresses_tradeoff,
    background=[ut_step, co_step, acon_objective],
    reason=reason_utco_addresses_tradeoff,
    prior=0.85,
)

# 3.4 Distillation -----------------------------------------------------------

distillation_setup = setting(
    "**Compressor distillation.** The teacher with optimised guideline $P^*$ "
    "(parameters $\\phi_T$) generates compressed outputs $y$ from inputs $x$, "
    "where $(x,y) = (h_t, h'_t)$ for history compression or $(x,y) = ((h_{t-1}, "
    "o_t), o'_t)$ for observation compression. The student $\\phi_S$ with "
    "$|\\phi_S| \\ll |\\phi_T|$ is trained with the standard sequence-level "
    "cross-entropy objective [@KimRush2016] over the teacher's "
    "successful-compression dataset $D^+_{train}$, using LoRA [@Hu2022].",
    title="Distillation objective (Equation 9)",
)

distillation_decouples_inference = claim(
    "Once trained, the distilled student replaces the teacher at inference, "
    "decoupling decision-making (still done by the agent LLM) from compression "
    "(now done by a much smaller LLM). The pipeline becomes "
    "$f(\\cdot;\\phi_T,P) \\xrightarrow{\\text{prompt opt.}} f(\\cdot;\\phi_T,P^*) "
    "\\xrightarrow{\\text{distil.}} f(\\cdot;\\phi_S,P^*)$.",
    title="Two-stage pipeline: optimise then distil",
)

reason_distil_pipeline = (
    "Given @distillation_setup, training the student to imitate the teacher's "
    "compressed outputs on $D^+_{train}$ produces a stand-alone compressor "
    "$f(\\cdot;\\phi_S,P^*)$ that requires neither the teacher nor the original "
    "guideline-optimisation pipeline at inference time. Because the student is "
    "much smaller, this directly removes the per-call cost of the teacher LLM "
    "from the agent loop."
)

strat_distil_pipeline_pivot = claim(
    "The teacher LLM with optimised guideline $P^*$ generates a "
    "supervised-imitation training set $\\{(x, f(x; \\phi_T, P^*))\\}$ for the "
    "student compressor.",
    title="Teacher generates supervised distillation data",
)

strat_distil_pipeline = support(
    [strat_distil_pipeline_pivot],
    distillation_decouples_inference,
    background=[distillation_setup, compressor_definition],
    reason=reason_distil_pipeline,
    prior=0.9,
)

# Composite "ACON addresses unbounded context" argument ----------------------

acon_solves_problem = claim(
    "ACON resolves the unbounded-context problem in long-horizon LLM agents by "
    "(i) compressing both history and observation only when their length exceeds "
    "a threshold (@history_compression_rule, @observation_compression_rule), "
    "(ii) optimising the natural-language guideline gradient-free via contrastive "
    "feedback (@textual_gradient_step), and (iii) distilling the optimised "
    "compressor into a small model (@distillation_decouples_inference) so the "
    "compressor's overhead does not dominate the savings.",
    title="ACON solves the unbounded-context problem",
)

reason_acon_solves = (
    "@context_grows_unbounded together with @cost_scales_with_context and "
    "@long_context_distracts establish that an effective long-horizon agent "
    "requires *some* form of context compression. The three ingredients "
    "(@history_compression_rule + @observation_compression_rule for selective "
    "compression, @textual_gradient_step for guideline optimisation in natural "
    "language, and @distillation_decouples_inference for cost reduction) jointly "
    "constitute a compression pipeline that is gradient-free, model-agnostic and "
    "deployable. Whether this *empirically* solves the problem at the headline "
    "rates is established by the experiments in s4_experiments.py."
)

strat_acon_solves = support(
    [
        context_grows_unbounded,
        cost_scales_with_context,
        long_context_distracts,
        heuristics_inadequate,
        textual_gradient_step,
        distillation_decouples_inference,
    ],
    acon_solves_problem,
    background=[
        history_compression_rule,
        observation_compression_rule,
        context_is_world_model,
        acon_objective,
    ],
    reason=reason_acon_solves,
    prior=0.8,
)

# Why the textual-gradient guideline-optimisation pipeline is gradient-free.
reason_gradient_free = (
    "@textual_gradient_step refines the natural-language guideline $P$ via an "
    "LLM-produced critique on contrastive trajectories, never touching the "
    "compressor's parameters $\\phi$. Since neither the agent's $\\theta$ "
    "(@agent_loop_setup) nor the compressor's $\\phi$ are updated, the entire "
    "ACON pipeline is gradient-free and therefore directly applicable to "
    "API-only / closed-source models."
)
strat_gradient_free = support(
    [textual_gradient_step],
    acon_is_gradient_free,
    background=[agent_loop_setup, compressor_definition],
    reason=reason_gradient_free,
    prior=0.95,
)

__all__ = [
    "compressor_definition",
    "history_compression_rule",
    "observation_compression_rule",
    "context_is_world_model",
    "acon_objective",
    "naive_rl_infeasible",
    "trajectory_dense_signal",
    "contrastive_subset_construction",
    "textual_gradient_step",
    "ut_step",
    "co_step",
    "acon_two_objective_addresses_tradeoff",
    "distillation_setup",
    "distillation_decouples_inference",
    "acon_solves_problem",
]
