"""Introduction and Motivation: Experience Representation for Test-Time Control"""

from gaia.lang import claim, setting, question, support, deduction

# --- Research context ---

setup_testtime = setting(
    "Large language models (LLMs) can incorporate reusable experience at test time "
    "via a control signal r = φ(ℋ), where ℋ represents prior trajectories. "
    "The control-relevance condition requires: pθ(y|x, r) ≠ pθ(y|x, ∅), "
    "meaning the representation must change model behavior. "
    "Excluded are parameter updates, one-off conversational recall, and single-use tricks.",
    title="Test-time control via reusable experience",
)

setup_skill_def = setting(
    "A procedural skill package is structured as s = {d_main, d_aux}, where "
    "d_main = {overview, workflow, pitfalls, error_handling} captures the main documentation "
    "and d_aux = {api_notes, examples, scripts} captures auxiliary reference material. "
    "Skills are optimized for human reading and information completeness, "
    "not for inference-time control. In the experiments, skills average approximately 2,500 tokens.",
    title="Procedural skill definition",
)

setup_gene_def = setting(
    "A strategy gene is defined as g = ψ(s) or g = ψ(ℋ), derived from either a "
    "skill package or raw experience trajectories. Its formal structure is "
    "g = (m, u, π, α, c, v), where: "
    "m = task-matching signals, "
    "u = compact summary, "
    "π = strategic steps (the key differentiator), "
    "α = failure-aware AVOID cues, "
    "c = execution constraints, "
    "v = validation hooks. "
    "Genes average approximately 230 tokens in experiments — roughly 11× smaller than skills.",
    title="Strategy gene definition",
)

setup_gep = setting(
    "The Gene Evolution Protocol (GEP) is defined as Γ(g) → g̃ ∈ G̃. "
    "It organizes genes as 'explicit, structured, and protocolized' objects "
    "supporting three operations: matching (find relevant gene for task), "
    "replacement (mutate gene content), and validation (confirm evolved gene works). "
    "GEP maintains three object types: Genes (G), Capsules (C), and Events (E), "
    "forming the object hierarchy O = G ∪ C ∪ E.",
    title="Gene Evolution Protocol (GEP)",
)

setup_eval = setting(
    "Experimental evaluation uses a checkpoint-based pass rate metric: "
    "PassRate = (1/N) Σ(p_i/n_i), where p_i is checkpoints passed and n_i is total "
    "checkpoints for scenario i. All trials use temperature T=0.05, max 16,384 tokens, "
    "120-second timeout per trial. Two models: Gemini 3.1 Pro Preview and Gemini 3.1 "
    "Flash Lite Preview. Total: 4,590 retained trials across 45 scientific code-solving "
    "scenarios spanning bioinformatics, neuroscience, chemistry, seismology, climate, "
    "signal processing, networks, finance, robotics, and quantum computing.",
    title="Evaluation protocol and benchmark",
)

# --- Core research question ---

rq_representation = question(
    "Which representation format—procedural skills or strategy genes—better encodes "
    "reusable experience for effective test-time LLM control and evolution?",
    title="Core research question",
)

# --- Central thesis ---

thesis_form_over_content = claim(
    "The representational form of reusable experience is a first-order factor for "
    "test-time LLM control, independent of content volume. "
    "A compact strategy gene (~230 tokens) outperforms a comprehensive documentation-oriented "
    "skill package (~2,500 tokens) derived from the same underlying experience, "
    "achieving +3.0 percentage points (pp) improvement versus -1.1pp degradation on a "
    "scientific code-solving benchmark (average over Gemini 3.1 Pro and Flash Lite) [@Wang2026].",
    title="Representation form is a first-order control factor",
)

thesis_skill_misaligned = claim(
    "Documentation-oriented procedural skill packages are misaligned with test-time LLM "
    "control. Despite encoding correct information, the documentation format causes "
    "performance degradation (-1.1pp average, dropping from 51.0% to 49.9% pass rate) "
    "because usable control signals are sparse within the ~2,500-token package and "
    "expanded documentation actively hinders rather than helps model performance [@Wang2026].",
    title="Skills are misaligned with test-time control",
)

thesis_gene_superior = claim(
    "Strategy genes are superior representations for test-time LLM control compared "
    "to procedural skills, budget-matched skill fragments, and unstructured text. "
    "The full gene format achieves 54.0% average pass rate (+3.0pp above the 51.0% "
    "no-guidance baseline) using only ~230 tokens, while the complete skill package "
    "achieves 49.9% (-1.1pp below baseline) using ~2,500 tokens [@Wang2026].",
    title="Gene representation outperforms skill representation",
)

strat_thesis_supported = support(
    [thesis_skill_misaligned, thesis_gene_superior],
    thesis_form_over_content,
    reason=(
        "Both probes together establish that @thesis_skill_misaligned (documentation "
        "format harms performance) and @thesis_gene_superior (compact gene format "
        "outperforms) jointly imply that representational form, not content volume, "
        "is the primary driver. The same underlying experience produces opposite "
        "outcomes depending only on how it is packaged, confirming @thesis_form_over_content."
    ),
    prior=0.88,
)
