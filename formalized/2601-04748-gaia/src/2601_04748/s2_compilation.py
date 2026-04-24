"""
Section 2-3: MAS-to-SAS Compilation — Formalization and Efficiency
====================================================================

Defines the formal compilation mapping, compilability conditions, and efficiency trade-offs.
Includes empirical results from three benchmark tasks comparing MAS vs SAS performance.
"""

from gaia.lang import claim, setting, question, support, deduction, complement

from .motivation import (
    mas_effectiveness,
    mas_overhead,
    skill_definition,
    sas_definition,
    compilation_view,
    q_compilation_feasibility,
)

# --- Formal definitions ---

mas_cost_def = setting(
    "The coordination cost of solving task $x$ in a multi-agent system (MAS) over $T$ rounds is: "
    "$$C_{MAS}(x) = \\sum_{t=1}^{T} |y^{(t)}| + T \\cdot c_{sync}$$ "
    "where $|y^{(t)}|$ denotes message length and $c_{sync}$ captures synchronization overhead per round.",
    title="MAS cost definition",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.1, Eq. 1"},
)

sas_cost_def = setting(
    "The cost of a single-agent with skills (SAS) over $T'$ rounds is: "
    "$$C_{SAS}(x) = \\sum_{t=1}^{T'} \\left[ C_{select}(\\sigma, \\mathcal{S}) + C_{exec}(s^{(t)}) \\right]$$ "
    "where $C_{select}$ is the cognitive cost of skill selection and $C_{exec}$ is execution cost.",
    title="SAS cost definition",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.2, Eq. 2"},
)

efficiency_condition = setting(
    "A compilation $\\Phi$ is cost-efficient if the selection overhead is less than the communication overhead: "
    "$$\\sum_t C_{select}(\\sigma, |\\mathcal{S}|) < \\sum_t C_{comm}(G, \\Pi)$$ "
    "The central trade-off: compilation eliminates inter-agent communication but introduces a selection bottleneck.",
    title="Efficiency condition",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.4, Eq. 9"},
)

# --- Compilability conditions ---

compilability_conditions = setting(
    "A multi-agent system $\\mathcal{M}$ is compilable if and only if all three conditions hold:\n\n"
    "- **C1 (Serializable Communication)**: The communication graph $G$ admits a topological ordering — "
    "agent interactions can be sequenced without information loss.\n"
    "- **C2 (Shared History)**: Agent outputs depend only on shared history $h$, with no private state.\n"
    "- **C3 (Homogeneous Backbone)**: All agents use the same underlying model.\n\n"
    "Conversely, compilation fails when agents require true parallelism (independent sampling), "
    "private information, adversarial objectives, or heterogeneous capabilities.",
    title="Compilability conditions (C1, C2, C3)",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.1, Proposition 3.1"},
)

compilable_architectures = claim(
    "The following multi-agent architectures are compilable to SAS:\n\n"
    "| Architecture | Structure | Compilable |\n"
    "|---|---|---|\n"
    "| Pipeline | $a_1 \\to a_2 \\to \\cdots \\to a_n$ | Yes |\n"
    "| Router-Workers | Router $\\to$ {Workers} $\\to$ Aggregator | Yes |\n"
    "| Iterative Refinement | Writer $\\leftrightarrow$ Critic (loop) | Yes |\n"
    "| Debate / Adversarial | Proponent $\\leftrightarrow$ Opponent | No |\n"
    "| Parallel Sampling | Independent agents, best-of-n | No |\n"
    "| Private Information | Agents with hidden state | No |",
    title="Compilable architectures (Table 1)",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.1, Table 1"},
)

# --- Compilation algorithm phases ---

compilation_phase1 = setting(
    "**Phase 1 (Capability Decomposition):** For each agent $a_i$ with system prompt $\\rho_i$, "
    "a decomposition function $f_{decomp}$ extracts a set of discrete atomic capabilities $K_i$: "
    "$$K_i = f_{decomp}(\\rho_i) = \\{\\kappa_{i,1}, \\kappa_{i,2}, \\ldots\\}$$ "
    "Each capability $\\kappa$ represents a specific functional unit (e.g., 'perform code review') "
    "derived from the agent's role, independent of implementation.",
    title="Compilation Phase 1: Capability decomposition",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.3.1, Eq. 3"},
)

compilation_phase2 = setting(
    "**Phase 2 (Backend Assignment):** For each capability $\\kappa$, the compiler determines "
    "the execution backend $\\xi$: externalized ($\\xi = t \\in \\mathcal{T}$) if the capability "
    "requires external grounding, or internalized ($\\xi = \\emptyset$) if purely cognitive. "
    "The skill descriptor $\\delta$ is generated to semanticize $\\kappa$ for retrieval.",
    title="Compilation Phase 2: Backend assignment",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.3.2, Eq. 4"},
)

compilation_phase3 = setting(
    "**Phase 3 (Topology Internalization):** The explicit communication edges in the MAS graph "
    "are transformed into implicit input/output constraints within skill definitions using a "
    "constraint injection function $f_{inject}$: "
    "$$\\pi^{final}_k = f_{inject}(\\pi^{base}_k, N_{out}(a_i))$$ "
    "where $N_{out}(a_i)$ is the set of downstream agents. This appends handover constraints "
    "ensuring output format compatibility with downstream skills.",
    title="Compilation Phase 3: Topology internalization",
    metadata={"source": "artifacts/2601.04748.pdf, Section 2.3.3, Eq. 5-6"},
)

# --- Experimental setup ---

exp_setup_compilation = setting(
    "Compilation efficiency experiments use three benchmarks, each matched to a compilable MAS architecture:\n\n"
    "| Benchmark | Architecture | MAS Agents | SAS Skills | API Calls |\n"
    "|---|---|---|---|---|\n"
    "| GSM8K (grad school math) | Pipeline | Decomposer, Solver, Verifier | decompose, solve, verify | 3→1 |\n"
    "| HumanEval (Python code generation) | Iterative | Coder, Critic, Refiner | code, critique, refine | 3→1 |\n"
    "| HotpotQA (multi-hop QA) | Router-Workers | Router, Retriever, Reasoner, Aggregator | analyze, retrieve, reason, synthesize | 4→1 |\n\n"
    "All experiments use GPT-4o-mini as the backbone model (satisfying condition C3). "
    "The compiled SAS performs equivalent computation in a single API call using structured output sections.",
    title="Compilation experiment setup",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.2.1, Table 2"},
)

# --- Experimental results ---

compilation_accuracy = claim(
    "Compiled SAS achieves accuracy within −2.0% to +4.0% of the original MAS across all benchmarks:\n\n"
    "| Task | MAS Accuracy | SAS Accuracy | Accuracy Δ |\n"
    "|---|---|---|---|\n"
    "| GSM8K | 94.0% | 92.0% | −2.0% |\n"
    "| HumanEval | 100.0% | 100.0% | 0.0% |\n"
    "| HotpotQA | 84.0% | 88.0% | +4.0% |\n"
    "| Average | — | — | +0.7% |",
    title="Compilation: accuracy preserved (Table 3)",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.2.2, Table 3"},
)

compilation_token_reduction = claim(
    "MAS-to-SAS compilation reduces token consumption by 53.7% on average:\n\n"
    "| Task | MAS Avg. Tokens | SAS Avg. Tokens | Token Reduction |\n"
    "|---|---|---|---|\n"
    "| GSM8K | 1407 | 616 | 56.2% |\n"
    "| HumanEval | 1400 | 749 | 46.5% |\n"
    "| HotpotQA | 4359 | 1816 | 58.4% |\n\n"
    "The reduction stems from eliminating redundant context repetition across agent calls — "
    "the SAS shares a single context window rather than re-encoding task descriptions and "
    "intermediate results for each specialized agent.",
    title="Compilation: token reduction 53.7% avg (Table 3)",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.2.2, Table 3"},
)

compilation_latency_reduction = claim(
    "MAS-to-SAS compilation reduces end-to-end latency by 49.5% on average:\n\n"
    "| Task | MAS Avg. Latency (ms) | SAS Avg. Latency (ms) | Latency Reduction |\n"
    "|---|---|---|---|\n"
    "| GSM8K | 10565 | 7537 | 28.7% |\n"
    "| HumanEval | 7227 | 2970 | 58.9% |\n"
    "| HotpotQA | 11671 | 4559 | 60.9% |\n\n"
    "The primary factor is the reduction from 3–4 sequential API calls to a single call. "
    "GSM8K shows a smaller latency reduction (28.7%) despite significant token savings, "
    "suggesting mathematical reasoning computation dominates latency for that task.",
    title="Compilation: latency reduction 49.5% avg (Table 3)",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.2.2, Table 3"},
)

hotpotqa_improvement = claim(
    "On HotpotQA, the compiled SAS outperforms the MAS by 4.0% accuracy (88% vs 84%). "
    "This improvement is attributed to the unified context enabling better information integration "
    "across retrieval and reasoning steps, compared to the MAS where retrieved passages must be "
    "passed between agents multiple times.",
    title="HotpotQA: SAS outperforms MAS",
    metadata={"source": "artifacts/2601.04748.pdf, Section 3.2.2"},
)

# --- Strategies ---

strat_compilation_accuracy = support(
    [compilable_architectures],
    compilation_accuracy,
    background=[exp_setup_compilation],
    reason=(
        "Given compilability conditions C1-C3 (@compilability_conditions) are satisfied for all three "
        "benchmark architectures (@compilable_architectures) and the experimental design uses the same "
        "GPT-4o-mini backbone for MAS and SAS (@exp_setup_compilation), the SAS faithfully encodes "
        "agent behavior as skills and manages sequential skill invocation within a single context window. "
        "The shared context enables coherent state management across skill invocations, preserving the "
        "reasoning structure without explicit inter-agent communication [@Li2026]."
    ),
    prior=0.85,
)

strat_token_reduction = support(
    [compilable_architectures],
    compilation_token_reduction,
    background=[exp_setup_compilation, sas_cost_def, mas_cost_def],
    reason=(
        "Token reduction follows directly from the cost structure difference between MAS and SAS "
        "(@mas_cost_def, @sas_cost_def). In MAS, each agent call re-encodes the full task description, "
        "intermediate results, and instructions — a cost that scales with the number of agents. "
        "The SAS shares a single context window, paying encoding cost only once. "
        "The HotpotQA reduction is largest (58.4%) because its 4-agent pipeline requires passing retrieved "
        "passages between agents multiple times (@exp_setup_compilation). "
        "These compiled architectures satisfy C1 (serializable communication), enabling the single-context approach.",
    ),
    prior=0.9,
)

strat_latency_reduction = support(
    [compilable_architectures],
    compilation_latency_reduction,
    background=[exp_setup_compilation, sas_cost_def, mas_cost_def],
    reason=(
        "Latency reduction results from reducing sequential API calls from 3-4 (MAS) to 1 (SAS), "
        "eliminating inter-agent communication overhead and network round-trip delays (@mas_cost_def, @sas_cost_def). "
        "The smaller improvement for GSM8K (28.7%) despite similar token savings suggests mathematical "
        "computation time — not communication — dominates latency for that task (@exp_setup_compilation). "
        "The compiled architectures (@compilable_architectures) satisfy conditions enabling this serial consolidation.",
    ),
    prior=0.9,
)

strat_hotpotqa_improvement = support(
    [compilation_accuracy],
    hotpotqa_improvement,
    background=[exp_setup_compilation],
    reason=(
        "The HotpotQA improvement is explained by the information integration advantage of SAS: "
        "the unified context window allows the model to cross-reference retrieved facts and reasoning "
        "steps without serialized hand-off, avoiding information loss that occurs when passing passages "
        "through distinct agent boundaries (@exp_setup_compilation). The +4.0% improvement is consistent "
        "with the claim that sequential MAS architectures may lose information at agent boundaries [@Li2026].",
    ),
    prior=0.7,
)

strat_compilation_feasible = support(
    [compilation_accuracy, compilation_token_reduction, compilation_latency_reduction],
    compilation_view,
    reason=(
        "The compilation view (@compilation_view) is supported by empirical evidence that accuracy "
        "is preserved within ±4% (@compilation_accuracy), tokens are reduced 53.7% (@compilation_token_reduction), "
        "and latency is reduced 49.5% (@compilation_latency_reduction). Together these demonstrate "
        "that MAS-to-SAS compilation is both faithful (behavioral equivalence) and cost-efficient "
        "(lower C_SAS than C_MAS for the tested benchmarks) [@Li2026].",
    ),
    prior=0.85,
)

__all__ = [
    "compilability_conditions",
    "compilable_architectures",
    "compilation_accuracy",
    "compilation_token_reduction",
    "compilation_latency_reduction",
    "hotpotqa_improvement",
    "strat_compilation_accuracy",
    "strat_token_reduction",
    "strat_latency_reduction",
    "strat_hotpotqa_improvement",
    "strat_compilation_feasible",
]
