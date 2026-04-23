"""Section 3: Methodology — Evolutionary Loop and Task Design"""

from gaia.lang import claim, setting

# ── Evolutionary loop design ────────────────────────────────────────────────

evo_loop_design = setting(
    "The evolutionary search loop follows Novikov et al. (2025). At each generation t: "
    "(1) An elite subset E_t = Top_{ceil(qN)}(P_t) with q=0.2 is selected. "
    "(2) Parents are sampled from E_t with probability proportional to fitness: "
    "Pr(x | E_t) ∝ f_T(x). "
    "(3) Selected parents are provided as context to the LLM, which generates "
    "10 offspring per generation conditioned on task and parent structure. "
    "(4) Offspring are deduplicated and merged into the population pool; "
    "if pool size exceeds N, only top-N by fitness are retained. "
    "Best-so-far fitness is updated as f*_t = max_{x ∈ P_t} f_T(x). "
    "Invalid/unparsable outputs receive zero fitness.",
    title="Evolutionary search loop specification",
)

shared_initial_population = setting(
    "For each task, an initial population P_0 of valid genomes with their fitness "
    "values is constructed and shared across all models for the same task. "
    "This ensures that differences in final performance are attributable to the "
    "LLMs' search behavior rather than initial conditions.",
    title="Shared fixed initial population across models",
)

four_task_families = setting(
    "Four optimization task families are evaluated: "
    "(1) Route Optimization: Traveling Salesman Problem (TSP-30 and TSP-60 cities). "
    "Genome = tour permutation. Fitness = inverse total distance. "
    "(2) Prompt Optimization: automatic prompt improvement for dialogue summarization "
    "(SAMSum, ROUGE-L metric) and text simplification (ASSET, SARI metric). "
    "Genome = natural language instruction prompt. Evaluator = frozen GPT-4o-mini. "
    "(3) Equation Discovery: symbolic regression for nonlinear oscillators "
    "(Oscillator-1: 3 variables; Oscillator-2: 4 variables). "
    "Genome = Python function. Fitness = 1 - norm(MSE(y_pred, y_true)). "
    "(4) Heuristic Design: online bin packing priority function design "
    "(OR3: 20 instances × 500 items; Weibull: 5 instances × 5,000 items). "
    "Genome = Python priority heuristic. Fitness = inverse bins used.",
    title="Four task families and genome representations",
)

novelty_definition = setting(
    "Task-agnostic novelty of a solution a with respect to prior solutions A_prior "
    "is defined as: nov(a, A_prior) = min_{b ∈ A_prior} D_T(a, b), "
    "where D_T is a task-specific semantic distance metric. "
    "Task-specific distances: TSP uses edge-set distance invariant to rotation; "
    "prompt optimization uses cosine distance in OpenAI text-embedding-ada-002 space; "
    "equation discovery and heuristic design use functional behavior distance "
    "over a fixed input grid. Novelty is normalized per subtask.",
    title="Novelty as minimum semantic distance to prior solutions",
)

evolution_scale = setting(
    "Study involves 15 LLMs spanning 6 model families: OpenAI (GPT-4o, GPT-4o-mini, "
    "GPT-3.5-turbo), Google Gemini (Gemini-1.5-flash, Gemini-1.5-pro), "
    "Google Gemma (Gemma-3n-4b), Meta Llama (Llama-3.1-70B/8B, Llama-3.2-1B/3B), "
    "DeepSeek (Deepseek-V3), MistralAI (Mistral-7B/24B-Instruct, Mistral-large, "
    "Magistral-small). 30 generations per (model, task) pair; each pair repeated "
    "twice (same initial population). Total: over 72,000 API calls. "
    "Temperature = 0.7 (default). Estimated total cost ≈ $500.",
    title="Experimental scale: 15 LLMs, 8 tasks, 2 seeds, 72K+ API calls",
)

zeroshot_definition = setting(
    "Zero-shot performance is defined as the best fitness achieved via "
    "temperature-swept best-of-N sampling: for each (model, task) pair, "
    "candidates are generated across six temperatures T ∈ {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}, "
    "with two samples per temperature, and the best fitness among them is reported. "
    "This measures intrinsic task-specific problem-solving ability without "
    "evolutionary refinement.",
    title="Zero-shot performance definition (best-of-N temperature sweep)",
)

spatial_entropy_definition = setting(
    "Spatial entropy H_spatial measures how broadly candidate solutions spread across "
    "semantic space within a generation. Given embeddings x_i ∈ R^d of solutions and "
    "a Gaussian kernel K(·,·), local density estimates are: "
    "g_i = sum_j K(x_i, x_j), q_i = g_i / sum_k g_k. "
    "Setting w_j = 1 gives H_spatial = -sum_i q_i log q_i (uniform density). "
    "Setting w_j = f_j (fitness weight) gives H_fitness = fitness-weighted spatial "
    "entropy, measuring whether high-quality solutions cluster or disperse. "
    "Low H_spatial = localized search; high H_spatial = diffuse/drifting search.",
    title="Kernel-based spatial entropy and fitness spatial entropy definitions",
)

# ── Methodology claims ──────────────────────────────────────────────────────

controlled_comparison = claim(
    "By sharing the same initial population, using the same selection rules and "
    "evaluation functions across all models, the evolutionary loop creates a "
    "controlled comparison where differences in final fitness are attributable "
    "to the LLMs' search behavior (mutation quality) rather than to differences "
    "in starting conditions or evaluation criteria.",
    title="Controlled comparison design isolates LLM search behavior",
)
