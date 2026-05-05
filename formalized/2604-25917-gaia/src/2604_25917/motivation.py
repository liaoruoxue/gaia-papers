"""Motivation: extending recursive (looped) language-model scaling from a
single model to a multi-agent system, asking whether agent collaboration
itself can be scaled through recursion.

Section 1 (Introduction) of Yang et al. 2026 [@Yang2026RecursiveMAS]. The
project page [@RecursiveMASPage] hosts code and demos.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup: what an LLM-based multi-agent system is
# ---------------------------------------------------------------------------

setup_mas_regime = setting(
    "**LLM-based multi-agent system (MAS) regime.** A multi-agent system "
    "$\\mathcal{S}$ [@MASsurvey; @AutoGen; @MoA] is composed of $N$ "
    "language-model agents $\\mathcal{A} = \\{A_1, \\dots, A_N\\}$, each a "
    "specialized LLM with its own role and parameters $\\theta_i$. The "
    "system orchestrates interactions among these agents to collaboratively "
    "produce a final prediction for an input problem $x$. Standard MAS "
    "topologies include sequential pipelines [@CAMEL; @ChatDev] that "
    "decompose and solve problems step by step, and mixture-style "
    "settings [@MoA] where domain-specialized agents reason in parallel "
    "and their outputs are aggregated.",
    title="Setup: LLM-based multi-agent system (N agents, role-specialized, collaborative)",
)

setup_single_lm_limits = setting(
    "**Single-language-model limitations.** A single LLM frequently falls "
    "short on complex tasks because of (i) limited per-model capacity, "
    "(ii) myopic auto-regressive generation, and (iii) inefficient "
    "exploration of the solution space, motivating the move to multi-"
    "agent organization.",
    title="Setup: single-LLM limits (capacity, myopia, exploration) motivate MAS",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Recursive (looped) language models scale single-model reasoning by "
    "iteratively refining the same model's computation over latent states. "
    "**Can agent collaboration itself be scaled through recursion?** "
    "Concretely: can a multi-agent system be co-evolved as a unified whole "
    "by treating each agent like a layer of a recursive language model "
    "and looping their latent states across recursion rounds?",
    title="Central question: can multi-agent collaboration itself be scaled through recursion?",
)

# ---------------------------------------------------------------------------
# Diagnosis: state of MAS adaptation
# ---------------------------------------------------------------------------

claim_prompt_adaptation_limit = claim(
    "**Limit of prompt-based MAS adaptation.** Existing MAS works that "
    "adapt the system through iterative refinement of shared *textual* "
    "context [@TextGrad] (e.g., textual feedback signals) only reshape "
    "interaction prompts; the underlying agent parameters do not "
    "improve. As a consequence, prompt-based adaptation cannot lift any "
    "individual agent's intrinsic capability and is bounded by the "
    "fixed text channel.",
    title="Diagnosis: prompt-based MAS adaptation cannot improve individual agents",
)

claim_separate_finetune_limit = claim(
    "**Limit of separately fine-tuning each agent.** A more principled "
    "line of work optimizes each MAS agent through learning -- e.g., "
    "MALT [@MALT], Sirius [@Sirius], multi-agent fine-tuning "
    "[@MultiAgentFinetune]. However, this approach (i) requires updating "
    "all model parameters (non-trivial at scale, and inflexible across "
    "heterogeneous backbones [@OWL]) and (ii) suffers substantial "
    "latency from the *sequential text-channel dependency*: each agent "
    "must wait for the previous agent to finish text generation before "
    "consuming its output.",
    title="Diagnosis: separately fine-tuning each agent (full-param + sequential text dependency) is hard",
)

claim_text_channel_bandwidth_assumption = claim(
    "**Prevailing assumption: the inter-agent text channel is the "
    "bandwidth bottleneck for MAS scaling.** Standard MAS architectures "
    "treat agent communication as discrete text passing -- each agent "
    "decodes a textual message and the next agent re-encodes it. This "
    "implicitly assumes that scaling MAS performance requires either "
    "more capable per-agent models or richer textual exchanges; the "
    "per-token decoding-and-re-encoding bandwidth is taken as the "
    "interface humans and the field commit to.",
    title="Prevailing assumption: text-channel bandwidth is the MAS scaling bottleneck",
)

# ---------------------------------------------------------------------------
# Central proposal: recasting MAS as recursive latent computation
# ---------------------------------------------------------------------------

claim_rlm_view = claim(
    "**Conceptual recasting: MAS as a recursive language model (RLM).** "
    "Recursive (looped) language models [@LoopLM; @TinyRecursive; "
    "@RecursiveLM2025; @Geiping2025; @MoR] iteratively reuse a shared "
    "set of Transformer layers in a continuous latent space to deepen "
    "reasoning. The paper recasts an LLM-based MAS through the same "
    "lens: each agent acts as one *RLM layer*, receiving and emitting "
    "latent representations within a continuous loop. The full system "
    "becomes one recursive computation that can be co-optimized end-"
    "to-end rather than a chain of independent text-mediated calls.",
    title="Insight: cast MAS as a recursive language model -- each agent is one RLM layer",
)

claim_recursivemas_intro = claim(
    "**RecursiveMAS: a system-level agentic recursion framework.** "
    "*RecursiveMAS* connects heterogeneous LLM agents in a unified "
    "collaboration loop via a single lightweight module called the "
    "**RecursiveLink** ($\\mathcal{R}$). An *inner* RecursiveLink "
    "$\\mathcal{R}_{in}$, located inside each agent, consolidates the "
    "agent's last-layer hidden states (latent thoughts) back into its "
    "input embedding space during auto-regressive generation. An *outer* "
    "RecursiveLink $\\mathcal{R}_{out}$ bridges hidden representations "
    "across heterogeneous agents (different model families, different "
    "hidden dimensions). Together, all agents are chained in a recursive "
    "loop, performing iterative latent collaboration; only the last "
    "agent decodes textual output, and only at the final recursion "
    "round.",
    title="Proposal: RecursiveMAS = inner + outer RecursiveLink chaining heterogeneous agents in a latent recursive loop",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 2",
        "caption": "Fig. 2: Overall architecture of RecursiveMAS -- inner link for latent thoughts generation, outer link for cross-agent transfer, looped at the system level.",
    },
)

claim_inner_outer_loop_training = claim(
    "**Inner-outer loop training.** RecursiveMAS pairs the architecture "
    "with a two-stage training paradigm. The **inner loop** warm-starts "
    "each agent in parallel by training only its inner RecursiveLink to "
    "align latent thoughts with the agent's input-embedding distribution. "
    "The **outer loop** then unrolls the full system over $n$ recursion "
    "rounds and trains all outer RecursiveLinks jointly by back-"
    "propagating a shared cross-entropy loss through the whole "
    "recursive computation graph. All base LLM parameters are frozen; "
    "only the lightweight RecursiveLink modules are trained, providing "
    "shared gradient-based credit assignment across recursion rounds.",
    title="Proposal: inner-outer loop training -- frozen LLMs, only RecursiveLinks trained, shared credit across rounds",
)

# ---------------------------------------------------------------------------
# Theoretical justification (introduced in Sec. 1, formalized in Sec. 3-4)
# ---------------------------------------------------------------------------

claim_theory_two_pillars = claim(
    "**Two theoretical pillars justifying latent-space (vs text-mediated) "
    "recursion.** The paper provides two complementary analyses showing "
    "why recursion in RecursiveMAS should occur in latent space rather "
    "than via text-mediated interaction: "
    "(T1) **Runtime complexity** -- RecursiveLink avoids repeated "
    "decoding of intermediate agents, replacing the per-step "
    "vocabulary-projection cost $m|V|d_h$ with the cheaper latent "
    "transformation $m d_h^2$ (Proposition 3.1). "
    "(T2) **Learning dynamics / gradient stability** -- latent "
    "RecursiveLink connections maintain near-constant gradient norm "
    "across recursion rounds, while text-mediated propagation "
    "(softmax + token argmax) suffers gradient vanishing (Theorem 4.1).",
    title="Theory: two pillars -- runtime complexity (Prop. 3.1) + gradient stability (Thm. 4.1) -- favor latent recursion",
)

# ---------------------------------------------------------------------------
# Headline empirical claims (introduced in abstract / Sec. 1)
# ---------------------------------------------------------------------------

claim_headline_accuracy = claim(
    "**Headline empirical claim (accuracy).** Across 9 benchmarks "
    "spanning mathematics (MATH500, AIME2025, AIME2026), science "
    "(GPQA-Diamond), medicine (MedQA), code generation "
    "(LiveCodeBench-v6, MBPP+) and search QA (HotpotQA, Bamboogle), "
    "RecursiveMAS delivers an **average accuracy improvement of 8.3%** "
    "over the strongest baseline on each benchmark (single advanced "
    "agents with LoRA / full-SFT, alternative MAS frameworks like MoA "
    "[@MoA] and TextGrad [@TextGrad], and recursive-computation "
    "baselines like LoopLM [@LoopLM] and Recursive-TextMAS).",
    title="Headline: +8.3% average accuracy improvement over strongest baseline on each benchmark",
)

claim_headline_efficiency = claim(
    "**Headline efficiency claim.** Under identical MAS architectures, "
    "RecursiveMAS achieves a **1.2x to 2.4x end-to-end inference "
    "speedup** over Recursive-TextMAS (text-mediated baseline with the "
    "same recursive structure) and reduces overall token usage by "
    "**34.6% to 75.6%**. Both gains scale with recursion depth $r$: "
    "speedup is 1.2x at $r=1$, 1.9x at $r=2$, and 2.4x at $r=3$; "
    "token reduction is 34.6% / 65.5% / 75.6% at $r=1/2/3$ "
    "respectively.",
    title="Headline: 1.2x-2.4x speedup + 34.6%-75.6% token reduction, scaling with recursion depth",
)

claim_headline_generality = claim(
    "**Headline generality claim.** RecursiveMAS is **structure-"
    "agnostic** and is instantiated under four representative MAS "
    "collaboration patterns: (i) Sequential Style (Planner-Critic-"
    "Solver), (ii) Mixture Style (Math/Code/Science specialists + "
    "Summarizer), (iii) Distillation Style (Expert + Learner), and "
    "(iv) Deliberation Style (Reflector + Tool-Caller). Across all "
    "four patterns and 9 benchmarks, RecursiveMAS yields effective "
    "performance gains over the strongest standalone agents in each "
    "pattern.",
    title="Headline: generality across 4 collaboration patterns x 9 benchmarks (structure-agnostic)",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 1 (Bottom)",
        "caption": "Fig. 1 (Bottom): RecursiveMAS adapts to diverse MAS structures (Sequential / Mixture / Distillation / Deliberation).",
    },
)

claim_scaling_law_headline = claim(
    "**Headline scaling-law claim (Figure 1, Top).** RecursiveMAS "
    "exhibits a clean scaling trend along *both* the training-time "
    "recursion depth and the inference-time recursion depth axes. "
    "Increasing inference depth improves systems trained with fewer "
    "rounds, while deeper training shifts the entire performance "
    "frontier upward; the strongest results lie consistently in the "
    "upper-right region of the (training-recursion, inference-"
    "recursion) plane. This complementary training-inference scaling "
    "is the system-level analog of the recursive-computation scaling "
    "law observed for single recursive language models.",
    title="Headline: scaling law -- complementary training x inference recursion-depth scaling",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 1 (Top)",
        "caption": "Fig. 1 (Top): Performance landscape of RecursiveMAS over training-recursion x inference-recursion depths for sub-1.5B-agent setups.",
    },
)

# ---------------------------------------------------------------------------
# Stated contributions (paraphrased from Sec. 1)
# ---------------------------------------------------------------------------

claim_six_contributions = claim(
    "**Stated contributions.** The paper makes six contributions: "
    "(C1) **Conceptual** -- extending recursive (looped) language-model "
    "scaling from a single model to a multi-agent system; "
    "(C2) **Method** -- RecursiveMAS, casting the entire MAS as one "
    "unified latent-space recursive computation through the "
    "RecursiveLink module (inner + outer); "
    "(C3) **Optimization** -- an inner-outer loop training algorithm "
    "for whole-system co-optimization with shared gradient-based "
    "credit assignment across recursion rounds; "
    "(C4) **Theory** -- runtime-complexity (Prop. 3.1) and learning-"
    "dynamics (Thm. 4.1) analyses establishing that RecursiveMAS is "
    "more efficient than text-based MAS and maintains stable "
    "gradients during recursive training; "
    "(C5) **Empirical** -- 4 collaboration patterns x 9 benchmarks, "
    "+8.3% average accuracy, 1.2x-2.4x inference speedup, 34.6%-"
    "75.6% token reduction; "
    "(C6) **Scaling-law** -- a performance landscape across training "
    "x inference recursion-depth dimensions for each of the 4 "
    "collaboration patterns (Figure 1).",
    title="Six stated contributions (conceptual / method / optimization / theory / empirical / scaling-law)",
)

__all__ = [
    "setup_mas_regime",
    "setup_single_lm_limits",
    "q_central",
    "claim_prompt_adaptation_limit",
    "claim_separate_finetune_limit",
    "claim_text_channel_bandwidth_assumption",
    "claim_rlm_view",
    "claim_recursivemas_intro",
    "claim_inner_outer_loop_training",
    "claim_theory_two_pillars",
    "claim_headline_accuracy",
    "claim_headline_efficiency",
    "claim_headline_generality",
    "claim_scaling_law_headline",
    "claim_six_contributions",
]
