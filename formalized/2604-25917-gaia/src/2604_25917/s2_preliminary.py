"""Section 2 (Preliminary): formal setup of auto-regressive latent
generation, recursive computation, multi-agent systems, the recursive
multi-agent evolution, and the four collaboration patterns.

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 2.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Standard Transformer + auto-regressive generation
# ---------------------------------------------------------------------------

setup_transformer = setting(
    "**Standard Transformer model [@Vaswani2017].** Let $f_\\theta(\\cdot)$ "
    "denote a Transformer parameterized by weights $\\theta$ and composed "
    "of $L$ layer blocks $f_\\theta = \\mathcal{M}_L \\circ \\cdots \\circ "
    "\\mathcal{M}_1$. Given an input embedding sequence $E = [e_1, \\dots, "
    "e_t] \\in \\mathbb{R}^{t \\times d_h}$ of length $t$ with hidden size "
    "$d_h$, the Transformer computes the last-layer hidden state $h_t$ "
    "through one forward pass.",
    title="Setup: Transformer with L layers, last-layer hidden state h_t",
)

setup_text_decoding = setting(
    "**Standard auto-regressive text decoding.** In standard text "
    "decoding, the last-layer hidden state $h_t$ is projected to the "
    "vocabulary space (vocabulary size $|V|$) by an embedding-to-logits "
    "matrix $W_{out} \\in \\mathbb{R}^{|V| \\times d_h}$ to produce a "
    "categorical distribution $p = \\mathrm{softmax}(W_{out} h_t)$ over "
    "the next token; the chosen token is then re-encoded by a token-to-"
    "embedding matrix $W_{in}$ before continuing generation.",
    title="Setup: standard text decoding (project to |V|, sample, re-embed)",
)

setup_latent_generation = setting(
    "**Latent generation (no decoding).** *Latent generation* keeps the "
    "recurrence entirely in continuous representation space: instead of "
    "decoding $h_t$ into a token, the previously generated latent "
    "embedding $h_t$ is fed directly back as the next-step input "
    "embedding. Formally, the next latent state at step $t+1$ is "
    "$h_{t+1} = f_\\theta([E_{\\le t}; h_t])$ (Eq. 1). The new latent "
    "state $h_{t+1}$ is referred to as the model's ongoing **latent "
    "thought**.",
    title="Setup: latent generation -- feed h_t back as next input embedding (Eq. 1)",
)

# ---------------------------------------------------------------------------
# Recursive computation (RLM)
# ---------------------------------------------------------------------------

setup_recursive_lm = setting(
    "**Recursive language model (RLM) [@LoopLM; @TinyRecursive; "
    "@RecursiveLM2025].** A recursive language model increases reasoning "
    "depth by reusing the same Transformer stack $f_\\theta$ for $n$ "
    "successive forward iterations on the same shared weights: "
    "$H^{(0)} = E$, $H^{(r)} = f_\\theta(H^{(r-1)})$ for "
    "$r = 1, \\dots, n$ (Eq. 2). The last round's representation "
    "$H^{(n)}$ is used for the final prediction. RLMs scale latent "
    "reasoning depth without adding parameters, by amortizing the same "
    "transformation across multiple loops.",
    title="Setup: recursive LM -- H^(r) = f_theta(H^(r-1)) over n shared-weight rounds (Eq. 2)",
)

# ---------------------------------------------------------------------------
# Multi-agent system formalization
# ---------------------------------------------------------------------------

setup_mas_formal = setting(
    "**Multi-agent system formalism.** A multi-agent system "
    "$\\mathcal{S}$ [@MASsurvey; @ZouLatentMAS] consists of $N$ agents "
    "$\\mathcal{A} = \\{A_1, \\dots, A_N\\}$, where each agent $A_i$ "
    "corresponds to an LLM $f_{\\theta_i}$ with its own parameters "
    "$\\theta_i$ and last-layer hidden representations $H_i$. The "
    "**collective latent state** of the system is "
    "$\\mathcal{H} = \\{H_1, \\dots, H_N\\}$. Given a problem $x$ with "
    "ground truth $y$, $\\mathcal{S}$ orchestrates agent interactions "
    "to collaboratively produce a final prediction.",
    title="Setup: MAS S = {A_1, ..., A_N}, collective latent state H = {H_1, ..., H_N}",
)

setup_recursive_mas_evolution = setting(
    "**Definition 2.1 (Recursive Multi-Agent Evolution).** A *recursive "
    "evolution* is the progressive refinement of the collective latent "
    "state $\\mathcal{H}$, where each agent adjusts its latent "
    "representation through iterative interaction with the other "
    "agents and its own reasoning state, so that the updated system "
    "is better aligned for the given problem: "
    "$\\mathcal{S}^{(0)} \\xrightarrow{H^{(1)}}_{Evolve} "
    "\\mathcal{S}^{(1)} \\xrightarrow{H^{(2)}}_{Evolve} \\cdots "
    "\\xrightarrow{H^{(n)}}_{Evolve} \\mathcal{S}^{(n)}$.",
    title="Definition 2.1: recursive multi-agent evolution -- progressive refinement of collective latent state",
)

# ---------------------------------------------------------------------------
# Four collaboration patterns
# ---------------------------------------------------------------------------

setup_four_collaboration_patterns = setting(
    "**Four representative MAS collaboration patterns considered.** "
    "Because MAS architectures vary across tasks, the paper does not "
    "restrict the collaboration pattern to a single style. It "
    "instantiates RecursiveMAS under four widely adopted patterns:\n\n"
    "| Pattern | Roles | Behavior |\n"
    "|---|---|---|\n"
    "| **(i) Sequential Style** | Planner -> Critic -> Solver | "
    "chain-of-agents pipeline that progressively decomposes, judges, "
    "refines, and solves the problem |\n"
    "| **(ii) Mixture Style** | Math / Code / Science specialists "
    "+ Summarizer | domain-specialized agents reason in parallel; "
    "the Summarizer aggregates their outputs |\n"
    "| **(iii) Distillation Style** | Expert + Learner | a larger, "
    "more capable Expert agent is paired with a smaller, faster "
    "Learner; expert knowledge is distilled while the Learner emits "
    "the final answer |\n"
    "| **(iv) Deliberation Style** | Reflector + Tool-Caller | an "
    "inner-thinking Reflector iteratively exchanges, critiques, and "
    "refines candidate solutions with a Tool-Caller that invokes "
    "external tools (Python or search APIs); the Tool-Caller "
    "produces the final answer |\n",
    title="Setup: four collaboration patterns (Sequential / Mixture / Distillation / Deliberation)",
    metadata={
        "source_table": "artifacts/2604.25917.pdf, Section 2 + Table 1",
    },
)

setup_agent_configurations = setting(
    "**Agent role-to-model assignments (Table 1).** Each collaboration "
    "pattern uses off-the-shelf models from diverse families (Qwen "
    "[@Qwen3; @Qwen2_5], Llama [@Llama3], Gemma [@Gemma3], Mistral "
    "[@Mixtral]) to form heterogeneous compositions:\n\n"
    "| Pattern | Role | Model |\n"
    "|---|---|---|\n"
    "| Sequential (Light) | Planner | Qwen3-1.7B |\n"
    "| Sequential (Light) | Critic | Llama3.2-1B-Instruct |\n"
    "| Sequential (Light) | Solver | Qwen2.5-Math-1.5B-Instruct |\n"
    "| Sequential (Scaled) | Planner | Gemma3-4B-it |\n"
    "| Sequential (Scaled) | Critic | Llama3.2-3B-Instruct |\n"
    "| Sequential (Scaled) | Solver | Qwen3.5-4B |\n"
    "| Mixture | Code Specialist | Qwen2.5-Coder-3B-Instruct |\n"
    "| Mixture | Science Specialist | BioMistral-7B [@BioMistral] |\n"
    "| Mixture | Math Specialist | DeepSeek-R1-Distill-Qwen-1.5B |\n"
    "| Mixture | Summarizer | Qwen3.5-2B |\n"
    "| Distillation | Learner | Qwen3.5-4B |\n"
    "| Distillation | Expert | Qwen3.5-9B |\n"
    "| Deliberation | Reflector | Qwen3.5-4B |\n"
    "| Deliberation | Tool-Caller | Qwen3.5-4B (with Tool-Integration) |\n",
    title="Setup: agent configurations per pattern (Table 1)",
    metadata={
        "source_table": "artifacts/2604.25917.pdf, Table 1",
    },
)

# ---------------------------------------------------------------------------
# Setup-level claims (these are propositional statements following from
# the formal setup but stated as facts in the paper)
# ---------------------------------------------------------------------------

claim_dh_ll_v_in_practice = claim(
    "**In practice, the hidden dimension is much smaller than the "
    "vocabulary size: $d_h \\ll |V|$.** For modern LLMs, typical hidden "
    "sizes are $d_h \\in [10^3, 10^4]$ while vocabulary sizes are "
    "$|V| \\in [10^4, 10^5]$. Consequently, replacing a vocabulary-"
    "space projection $|V| d_h$ with a latent-space transformation "
    "$d_h^2$ yields a substantial constant-factor saving for every "
    "decoded token (Remark 3.2).",
    title="Setup-fact: d_h << |V| for modern LLMs (basis of Remark 3.2)",
)

__all__ = [
    "setup_transformer",
    "setup_text_decoding",
    "setup_latent_generation",
    "setup_recursive_lm",
    "setup_mas_formal",
    "setup_recursive_mas_evolution",
    "setup_four_collaboration_patterns",
    "setup_agent_configurations",
    "claim_dh_ll_v_in_practice",
]
