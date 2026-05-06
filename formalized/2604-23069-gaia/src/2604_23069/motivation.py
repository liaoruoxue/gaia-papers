"""Motivation: long-context interactions break LLM agents because existing
context-management methods (sliding window, prompt compression, retrieval)
ignore the dependency structure that links one reasoning step to the next.

Section 1 (Introduction) and Abstract of Wu et al. (2026)
[@Wu2026ContextWeaver]. The paper diagnoses three concurrent context-management
families used by tool-using LLM agents -- sliding window, prompt compression,
and retrieval-based memory -- and argues that all three select content by
recency, salience, or semantic similarity, none of which captures the
*dependency structure* (causal: tool-output -> follow-up edit; logical:
reasoning step that reuses, refines, or resolves an earlier hypothesis) that
links one reasoning step to the next. ContextWeaver is proposed as a
selective, dependency-structured memory framework with three components:
(1) dependency-based construction and traversal, (2) compact dependency
summarization, and (3) a lightweight validation layer. Headline empirical
result: on SWE-Bench Verified and SWE-Bench Lite, ContextWeaver improves
pass@1 over a sliding-window baseline *while reducing* reasoning steps and
token usage -- a simultaneous quality + efficiency gain.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setting (the deployment regime the paper targets)
# ---------------------------------------------------------------------------

setup_tool_using_agent = setting(
    "**Tool-using LLM agent regime.** The paper targets large language model "
    "(LLM) agents that iteratively *plan* and *interact* with external systems "
    "via tools (e.g., web search, code execution, data retrieval) "
    "[@Schick2023Toolformer; @Gao2023PAL]. Each tool invocation introduces new "
    "observations and implicit causal links between steps, creating a "
    "reasoning trajectory that is *not* captured by standard conversational "
    "histories [@Yao2022ReAct]. The paper focuses on the histories of "
    "tool-using LLM agents rather than chat agents whose histories consist "
    "only of user-assistant message pairs [@Wu2026ContextWeaver, Sec. 3].",
    title="Setup: tool-using LLM agents that iteratively plan and call external tools",
)

setup_context_length_pressure = setting(
    "**Tool-using interactions grow context length quickly.** Current LLMs "
    "have a maximum context-length limit: the LLM (or underlying "
    "infrastructure) cannot generate a response when the input token count "
    "exceeds that limit. For tool-using agents that iteratively plan and "
    "interact with external systems, contexts grow especially fast "
    "[@Maharana2024LongConv], so it is necessary to selectively compact or "
    "reorganize the agent's interaction history "
    "[@Wu2026ContextWeaver, Sec. 1].",
    title="Setup: tool-using interactions exceed context-length limits, requiring memory management",
)

setup_long_context_degradation = setting(
    "**Long contexts degrade LLM performance even when within the limit.** "
    "Even when the token count does not exceed the model's context window, "
    "long conversations or contexts degrade LLM performance: 'lost-in-the-"
    "middle' positional attenuation [@LiuLost2024] and degraded long in-"
    "context learning [@Li2024LongICL]. This makes naive context retention "
    "an inadequate strategy independently of the hard length cap "
    "[@Wu2026ContextWeaver, Sec. 1].",
    title="Setup: long contexts degrade LLM behavior even below the token limit",
)

setup_history_format = setting(
    "**Tool-using agent history representation.** The history of a tool-"
    "using agent is represented as\n\n"
    "$$H = \\{\\{\\text{system}, Q\\}, \\{T_1, A_1, O_1\\}, \\dots, "
    "\\{T_n, A_n, O_n\\}\\},$$\n\n"
    "where $Q$ is the user query, $\\text{system}$ is the system prompt, "
    "and each triple $(T_i, A_i, O_i)$ defines a single reasoning step: "
    "$T_i$ is the agent's internal *Thought*, $A_i$ specifies the *Action* "
    "(tool invocation), and $O_i$ records the resulting *Observation* "
    "(tool output) [@Wu2026ContextWeaver, Sec. 3].",
    title="Setup: agent history H = (system, Q, T1A1O1, ..., TnAnOn)",
)

setup_causal_vs_logical = setting(
    "**Causal vs. logical dependencies (paper terminology).** The paper "
    "uses 'causal' to refer to dependencies created by *tool outputs* "
    "(e.g., test results that trigger follow-up edits) and 'logical' to "
    "refer to dependencies created by *reasoning steps* that reuse, "
    "refine, or resolve earlier hypotheses "
    "[@Wu2026ContextWeaver, Sec. 1, footnote 1].",
    title="Setup: 'causal' = tool-output-induced; 'logical' = reasoning-induced (paper definitions)",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Can an LLM-agent context-management mechanism that explicitly models "
    "the dependency structure (causal + logical) between reasoning steps -- "
    "rather than selecting context by recency, salience, or semantic "
    "similarity alone -- improve agent task performance on long-horizon "
    "tool-using tasks while *reducing* (not increasing) reasoning steps "
    "and token usage?",
    title="Central question: can dependency-structured memory beat recency/similarity selection AND save tokens?",
)

# ---------------------------------------------------------------------------
# Diagnosis: three families of existing context management
# ---------------------------------------------------------------------------

claim_existing_methods_taxonomy = claim(
    "**Three existing families of context-length control: sliding window, "
    "prompt compression, retrieval-based memory.** Existing methods that "
    "control context length for tool-using agents fall into three groups: "
    "(i) **sliding windows** that keep the most recent turns; "
    "(ii) **prompt-compression** methods that distil salient information "
    "from the original context (gist tokens [@Mu2023Gist], selective "
    "context [@Li2023Selective], LLMLingua [@Jiang2023LLMLingua], "
    "embedding-level compression [@Chevalier2023AutoCompress]); and "
    "(iii) **retrieval-based / hierarchical memory** systems that store "
    "past interactions in databases or hierarchies and retrieve relevant "
    "entries (MemGPT [@Packer2023MemGPT], Generative Agents "
    "[@Park2023GenAgents], Reflexion [@Shinn2023Reflexion]) "
    "[@Wu2026ContextWeaver, Sec. 1, Sec. 2].",
    title="Three families of existing context management: sliding window, compression, retrieval",
)

claim_recency_salience_similarity = claim(
    "**All three existing families select content by recency, salience, or "
    "semantic similarity.** Sliding windows select by *recency*; prompt "
    "compression selects by *salience* (typically perplexity- or "
    "attention-based importance scores); retrieval-based memories select "
    "by *semantic similarity* of stored entries to the current query "
    "[@Wu2026ContextWeaver, Sec. 1].",
    title="Existing methods select by recency / salience / semantic similarity",
)

claim_signals_miss_dependency_structure = claim(
    "**Recency, salience, and semantic similarity do not capture "
    "dependency structure.** None of recency, salience, or semantic "
    "similarity captures the *dependency structure* that links one "
    "reasoning step to the next. In agentic settings, each next action "
    "can depend on (i) earlier decisions, (ii) tool outputs, and "
    "(iii) intermediate hypotheses generated during the trajectory. When "
    "these dependencies are lost, the agent can break ongoing plans, "
    "repeat earlier exploration, or produce steps that no longer match "
    "the earlier context [@Wu2026ContextWeaver, Sec. 1].",
    title="Recency/salience/similarity ignore dependency structure -> broken plans / repeated exploration",
)

claim_separate_layers_assumption = claim(
    "**Implicit prevailing assumption: retrieval-based / recency-based "
    "memory is sufficient for multi-step agent reasoning.** Existing "
    "literature on tool-using agent context management implicitly assumes "
    "that selecting content by recency, salience, or semantic similarity "
    "is sufficient to support multi-step reasoning under a fixed token "
    "budget; this assumption underlies sliding-window, prompt-compression, "
    "and retrieval-based memory designs alike "
    "[@Wu2026ContextWeaver, Sec. 1, Sec. 2].",
    title="Foil: existing wisdom that recency / salience / similarity selection suffices",
)

# ---------------------------------------------------------------------------
# ContextWeaver: the proposed solution
# ---------------------------------------------------------------------------

claim_cw_three_components = claim(
    "**ContextWeaver = three coordinated components.** ContextWeaver is a "
    "selective and dependency-structured memory framework with three main "
    "components: (1) a **dependency-based construction module** that links "
    "each reasoning step to the earlier steps it relies on; (2) **compact "
    "dependency summaries** that provide concise, reusable representations "
    "of the reasoning paths supporting each step; and (3) a **lightweight "
    "validation layer** that incorporates execution feedback. Together "
    "these enable ContextWeaver to preserve the context most relevant to "
    "the agent's next action while remaining within token budgets "
    "[@Wu2026ContextWeaver, Sec. 1, Sec. 3].",
    title="Headline mechanism: dependency construction + compact summaries + validation",
)

claim_dependency_modeling_thesis = claim(
    "**Central thesis: modeling logical and causal dependencies provides "
    "a stable and scalable memory mechanism for tool-using LLM agents.** "
    "By converting each new reasoning step into a structured node, "
    "linking it to its supporting predecessors via an LLM-based "
    "dependency analyzer, summarizing root-to-step paths into reusable "
    "units, and filtering out unreliable nodes via execution feedback, "
    "ContextWeaver builds a directed acyclic graph (DAG) over the agent's "
    "trajectory. Selectively retrieving only the validated ancestry "
    "subgraph for each next decision yields a memory mechanism that is "
    "both *stable* (low run-to-run variance) and *scalable* (fits a "
    "fixed token budget while preserving long-range dependencies) "
    "[@Wu2026ContextWeaver, Abstract, Sec. 1, Sec. 5].",
    title="Thesis: explicit dependency modeling => stable + scalable agent memory",
)

# ---------------------------------------------------------------------------
# Headline empirical contribution
# ---------------------------------------------------------------------------

claim_headline_swe_bench = claim(
    "**Headline empirical result.** On SWE-Bench Verified and SWE-Bench "
    "Lite, ContextWeaver improves pass@1 over a sliding-window baseline "
    "*while* reducing reasoning steps and token usage. The simultaneous "
    "improvement in solve rate and reduction in resource consumption is "
    "the paper's central empirical claim "
    "[@Wu2026ContextWeaver, Abstract; @Jimenez2023SWEBench; "
    "@Chowdhury2024SWEVerified]. Detailed per-model and per-benchmark "
    "numbers are reported in `s8_main_results`.",
    title="Headline: ContextWeaver beats sliding window on SWE-Bench Verified+Lite WITH fewer steps + tokens",
)

claim_efficiency_quality_jointly = claim(
    "**Joint quality-and-efficiency improvement is the discriminating "
    "signal.** A method that simply allocated more compute (larger "
    "context, more retrieval queries, larger backbone LLM) could lift "
    "pass@1, but would *not* simultaneously reduce reasoning steps and "
    "tokens. ContextWeaver's measured pattern -- higher pass@1 *and* "
    "lower steps *and* lower tokens-per-resolve -- is therefore evidence "
    "that the *mechanism* (explicit dependency modeling) is doing the "
    "work, rather than additional compute "
    "[@Wu2026ContextWeaver, Sec. 4.4].",
    title="Argument: simultaneous gain + saving rules out 'more compute' explanations",
)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "setup_tool_using_agent",
    "setup_context_length_pressure",
    "setup_long_context_degradation",
    "setup_history_format",
    "setup_causal_vs_logical",
    "q_central",
    "claim_existing_methods_taxonomy",
    "claim_recency_salience_similarity",
    "claim_signals_miss_dependency_structure",
    "claim_separate_layers_assumption",
    "claim_cw_three_components",
    "claim_dependency_modeling_thesis",
    "claim_headline_swe_bench",
    "claim_efficiency_quality_jointly",
]
