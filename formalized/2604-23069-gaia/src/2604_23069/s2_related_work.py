"""Related Works (Section 2): four neighborhoods of prior context-management
work and their structural limitations.

Section 2 of [@Wu2026ContextWeaver] organizes prior work into four
neighborhoods: (a) **Prompt Compression**, (b) **Retrieval and Hierarchical
Memory**, (c) **Graph-Based Reasoning vs. Memory**, and (d) **Static
Analysis and Repository Context**, plus a fifth grouping on (e) **LLM
Summarization** for agent context. The paper argues that each neighborhood
omits the *dependency structure* that ContextWeaver explicitly models.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 2a. Prompt compression
# ---------------------------------------------------------------------------

claim_gist_tokens = claim(
    "**Gist tokens [@Mu2023Gist] offer learned compression context but "
    "have limited interpretability and require additional training.** Gist "
    "tokens are learned compressed representations of context that reduce "
    "token count, but suffer from limited interpretability of the "
    "compressed representation and impose additional training cost on the "
    "underlying LLM [@Wu2026ContextWeaver, Sec. 2].",
    title="Gist tokens: learned compression -> limited interpretability + training overhead",
)

claim_selective_context = claim(
    "**Selective context [@Li2023Selective] relies on semantic similarity "
    "and may wrongly remove important information.** Methods that prune "
    "context tokens by perplexity / semantic-similarity scoring can "
    "incorrectly discard tokens that turn out to matter for later reasoning "
    "steps, leading to suboptimal outputs "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Selective context: similarity-based pruning may discard important content",
)

claim_token_embedding_compression = claim(
    "**Token-level (LLMLingua [@Jiang2023LLMLingua]) and embedding-level "
    "compression methods [@Chevalier2023AutoCompress] also fall in the "
    "compression family.** Both compress prompts to accelerate inference "
    "or fit longer histories under fixed context budgets, but operate on "
    "the linearized token stream without explicit modeling of inter-step "
    "dependencies [@Wu2026ContextWeaver, Sec. 2].",
    title="LLMLingua + AutoCompress: token/embedding-level compression operates on linear streams",
)

claim_compression_lacks_dependency = claim(
    "**Prompt-compression methods do not capture inter-step "
    "dependencies.** Across the prompt-compression family, the underlying "
    "selection signal is information density / perplexity / similarity "
    "rather than the *dependency* between earlier and later reasoning "
    "steps. As a result, compression can drop tokens that are critical "
    "premises for later steps when those tokens are individually "
    "low-salience [@Wu2026ContextWeaver, Sec. 2].",
    title="Compression-family limitation: dependency-blind selection",
)

# ---------------------------------------------------------------------------
# 2b. Retrieval and hierarchical memory
# ---------------------------------------------------------------------------

claim_memgpt_components = claim(
    "**MemGPT [@Packer2023MemGPT] stores past interactions in "
    "hierarchical memory with OS-style paging.** MemGPT models the LLM "
    "context as a tiered memory system (analogous to RAM/disk in an "
    "operating system) and pages relevant interactions into the active "
    "context based on retrieval signals "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="MemGPT: OS-style hierarchical memory paging",
)

claim_generative_agents_components = claim(
    "**Generative Agents [@Park2023GenAgents] use database-like memory "
    "with reflective signals.** Past interactions are stored in a "
    "memory database; retrieval is driven by recency, importance, and "
    "relevance heuristics, and the agent periodically generates "
    "reflections that synthesize prior memories "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Generative Agents: database memory + reflection-driven retrieval",
)

claim_reflexion_components = claim(
    "**Reflexion [@Shinn2023Reflexion] augments memory with verbal "
    "reinforcement reflections.** The agent stores both action traces and "
    "self-generated reflective evaluations, retrieved by relevance to "
    "the current task to inform later attempts "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Reflexion: action traces + reflective evaluations",
)

claim_retrieval_lacks_dependency = claim(
    "**Retrieval-based / hierarchical memory systems still operate over "
    "linearized token streams once retrieved, without modeling logical "
    "or causal relations between steps.** Although these systems scale "
    "to longer interaction histories, retrieval is largely driven by "
    "*semantic similarity, recency, or reflective signals*, and the "
    "retrieved fragments are concatenated as a flat token stream rather "
    "than as a structured dependency graph "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Retrieval-family limitation: similarity/recency-driven, no inter-step structure",
)

# ---------------------------------------------------------------------------
# 2c. Graph-based reasoning vs. memory
# ---------------------------------------------------------------------------

claim_amem_focus = claim(
    "**Recent graph-based memory work focuses on construction and "
    "retrieval (e.g., A-Mem [@Xu2025AMEM]) rather than simplification or "
    "optimization over time.** A-Mem and related graph-memory systems "
    "build agentic memory graphs and retrieve subgraphs for the next "
    "step, but devote less attention to how memory structures should be "
    "*simplified or optimized* as the trajectory grows "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Graph memory (A-Mem): construction + retrieval focus, less on optimization",
)

claim_cot_baseline = claim(
    "**Chain-of-Thought [@Wei2022CoT] is the baseline for graph-based "
    "reasoning frameworks.** CoT prompts the LLM to produce intermediate "
    "reasoning steps before the final answer; subsequent graph-based "
    "reasoning frameworks generalize the linear chain into trees and "
    "graphs of intermediate states "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="CoT: linear chain of intermediate reasoning steps (baseline)",
)

claim_tot_got_episode_focus = claim(
    "**Tree of Thoughts [@Yao2023ToT] and Graph of Thoughts "
    "[@Besta2024GoT] support inference-time search by branching over "
    "alternative intermediate states within a *single* reasoning "
    "episode.** ToT and GoT are designed to organize structured search "
    "over alternative continuations during one reasoning episode, "
    "rather than to organize *persistent memory across long agent "
    "trajectories* spanning many tool calls "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="ToT/GoT: single-episode branching, not persistent multi-step memory",
)

claim_cw_distinguished_from_episodic_graphs = claim(
    "**ContextWeaver uses graph structure to organize past experience -- "
    "specifically, a dependency graph over executed steps -- which "
    "differs from episodic-search graphs.** Instead of relying primarily "
    "on semantic similarity or single-episode search, ContextWeaver "
    "models explicit logical and causal relationships (e.g., when the "
    "output of one step is required by another), enabling more reliable "
    "pruning and more interpretable memory organization "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="CW vs. ToT/GoT/A-Mem: explicit causal+logical relations over executed steps",
)

# ---------------------------------------------------------------------------
# 2d. Static analysis and repository context (SE-specific)
# ---------------------------------------------------------------------------

claim_openhands_agentless_static = claim(
    "**OpenHands [@Wang2024OpenHands; @Wang2025OpenHandsSDK] and "
    "Agentless [@Xia2025Agentless] retrieve over entire code repositories "
    "[@Liu2023RepoBench] using static structural representations such as "
    "Abstract Syntax Trees (ASTs) to capture code dependencies.** These "
    "platforms extract static code structure -- file hierarchies, ASTs, "
    "import graphs -- to localize and reason about repository context "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="OpenHands + Agentless: static AST/repository-graph retrieval",
)

claim_static_does_not_model_dynamics = claim(
    "**Static-analysis methods describe code structure but do not model "
    "the dynamic progression of the agent's debugging process.** In "
    "tasks such as SWE-Bench [@Jimenez2023SWEBench], critical context "
    "often appears in *runtime* error logs, test failure messages, or "
    "temporary variable values rather than in static source files. A "
    "static AST-based view cannot capture this dynamic interaction "
    "history [@Wu2026ContextWeaver, Sec. 2].",
    title="Static analysis: misses runtime/dynamic debugging context",
)

claim_cw_complements_static = claim(
    "**ContextWeaver complements static analysis by modeling the "
    "logical dependencies in the *interaction history*.** ContextWeaver "
    "preserves the *reasoning path* leading to each code modification, "
    "rather than the static code-structure context. It is therefore "
    "compatible with -- not a substitute for -- static AST/repository "
    "retrieval [@Wu2026ContextWeaver, Sec. 2].",
    title="CW complementarity: dependency over interaction history vs. static repo structure",
)

# ---------------------------------------------------------------------------
# 2e. LLM summarization for agent context
# ---------------------------------------------------------------------------

claim_swe_agent_condensation = claim(
    "**SWE-Agent [@Yang2024SWEAgent] introduced context condensation to "
    "keep working context within token limits during repository-level "
    "coding tasks.** SWE-Agent periodically condenses older interactions "
    "into compact textual summaries to avoid context overflow during "
    "long debugging trajectories "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="SWE-Agent: periodic LLM condensation of older interactions",
)

claim_openhands_condenser = claim(
    "**OpenHands provides a modular condenser that compresses event "
    "histories on the fly [@Wang2024OpenHands; @Wang2025OpenHandsSDK].** "
    "The condenser module compresses event histories during agent "
    "execution, decoupling compression from the action loop "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="OpenHands condenser: on-the-fly modular event-history compression",
)

claim_acon_optimization = claim(
    "**ACON [@Kang2025ACON] further refines the LLM-summarization "
    "paradigm by optimizing the compression *guidelines* themselves, "
    "yielding higher-fidelity summaries under tight budgets.** Rather "
    "than learning a compressor model, ACON optimizes the textual "
    "instructions that guide the LLM-based summarization "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="ACON: optimizes the prompt-side compression guidelines",
)

claim_lindenbauer_observation_masking = claim(
    "**Lindenbauer et al. [@Lindenbauer2025Masking] find that simple "
    "observation masking can match LLM summarization at substantially "
    "lower cost.** This empirical result suggests that the value of "
    "LLM-based summarization depends heavily on the task and agent "
    "design and is not unconditionally beneficial "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Lindenbauer 2025: cheap observation masking matches LLM summarization",
)

claim_summarization_flat_loses_structure = claim(
    "**LLM-summarization approaches produce *flat* textual condensations "
    "that discard structural relationships among reasoning steps.** "
    "Periodically summarized histories collapse the dependency graph "
    "(which step required which earlier output) into prose that, however "
    "well-written, no longer permits *selective* retrieval based on "
    "causal/logical relevance "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Summarization-family limitation: flat prose loses structural dependency",
)

claim_cw_organized_by_dependency_graph = claim(
    "**ContextWeaver, in contrast to flat summarization, organizes "
    "context around an explicit dependency graph, enabling selective "
    "retrieval based on causal and logical relevance.** This is the key "
    "distinction from the LLM-summarization neighborhood: the graph "
    "structure persists rather than being collapsed into text "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="CW vs. summarization: explicit dependency graph enables selective retrieval",
)

# ---------------------------------------------------------------------------
# Synthesis: the structural gap CW fills
# ---------------------------------------------------------------------------

claim_dependency_gap_synthesis = claim(
    "**Synthesis: across all four neighborhoods, the structural gap is "
    "the absence of explicit inter-step dependency modeling.** Prompt "
    "compression, retrieval/hierarchical memory, episodic reasoning "
    "graphs (CoT/ToT/GoT), static AST analysis, and LLM-summarization "
    "all either select content by signals that ignore inter-step "
    "dependencies, or model structure within a single episode rather "
    "than across the agent's persistent trajectory. ContextWeaver's "
    "contribution is to fill this gap with a *cross-trajectory* "
    "dependency graph that survives compression "
    "[@Wu2026ContextWeaver, Sec. 2].",
    title="Synthesis: cross-trajectory inter-step dependency modeling is the missing piece",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "claim_gist_tokens",
    "claim_selective_context",
    "claim_token_embedding_compression",
    "claim_compression_lacks_dependency",
    "claim_memgpt_components",
    "claim_generative_agents_components",
    "claim_reflexion_components",
    "claim_retrieval_lacks_dependency",
    "claim_amem_focus",
    "claim_cot_baseline",
    "claim_tot_got_episode_focus",
    "claim_cw_distinguished_from_episodic_graphs",
    "claim_openhands_agentless_static",
    "claim_static_does_not_model_dynamics",
    "claim_cw_complements_static",
    "claim_swe_agent_condensation",
    "claim_openhands_condenser",
    "claim_acon_optimization",
    "claim_lindenbauer_observation_masking",
    "claim_summarization_flat_loses_structure",
    "claim_cw_organized_by_dependency_graph",
    "claim_dependency_gap_synthesis",
]
