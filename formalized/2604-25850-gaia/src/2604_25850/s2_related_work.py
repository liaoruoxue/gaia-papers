"""Section 2: Related work.

Position AHE against (a) the literature on harness engineering and coding-
agent evaluation, and (b) the literature on automated optimization of LLM
agents. Source: Lin et al. 2026 [@Lin2026AHE], Section 2.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Section 2.1: Harness engineering and evaluation for coding agents
# ---------------------------------------------------------------------------

claim_harness_engineering_definition = claim(
    "**Harness engineering as a research practice.** Harness engineering "
    "refers to the practice of designing the system surrounding the "
    "model, including its tools, interfaces, memory, execution "
    "constraints, and feedback loops, which together shape what an "
    "agent can do on long-horizon tasks "
    "[@RajasekaranHarness; @Lopopolo; @Trivedy; @ClaudeCode; @OpenClaw; "
    "@HermesAgent]. Concretely, the harness mediates how the model "
    "perceives and acts on its environment: it exposes the action and "
    "observation interfaces over which tool-augmented reasoning unfolds "
    "[@ClaudeCode], custom agent-computer interfaces for repository "
    "navigation, file editing, and command execution [@SWEAgent], and "
    "sandboxed execution and orchestration support that keep long-"
    "horizon runs reproducible [@OpenHands].",
    title="Related work: harness engineering practice (tools, interfaces, memory, execution, feedback)",
)

claim_evaluation_horizons = claim(
    "**Coding-agent benchmarks span two axes: task horizon and "
    "environmental realism.** Coverage extends from short-horizon "
    "function-level benchmarks focused on contamination and freshness "
    "control [@LiveCodeBench; @BigCodeBench], through repository-scale "
    "executable patch resolution [@SWEbench; @SWEbenchMM; @SWEbenchPro], "
    "to multi-hour, terminal-driven workflows that exercise long-"
    "horizon, realistic execution [@SWELancer; @MLEbench; "
    "@TerminalBench2].",
    title="Related work: benchmark coverage (function-level / repo-scale / terminal multi-hour)",
)

claim_eval_infrastructure = claim(
    "**Parallel infrastructure for reproducible execution.** A separate "
    "infrastructure track packages executable runtimes and verifiers "
    "around these benchmarks [@SWEGym; @R2EGym; @SWEHub], whose "
    "attention to reproducible, traceable, and verifiable execution "
    "directly motivates the observation system AHE builds on.",
    title="Related work: reproducible-execution infrastructure (SWE-Gym, R2E-Gym, SWE-Hub)",
)

# ---------------------------------------------------------------------------
# Section 2.2: Automated optimization of LLM agents
# ---------------------------------------------------------------------------

claim_self_critique_methods = claim(
    "**Optimizer dimension 1: revising the agent's own outputs.** A "
    "subset of automated agent-optimization approaches revise the "
    "agent's own outputs through episodic critique and reflection "
    "[@SelfRefine; @Reflexion; @Critiq]. The optimizer observes the "
    "agent's trace and emits a textual critique that the agent then "
    "consumes; the editable surface is the *agent's behavior at "
    "inference*, not the harness.",
    title="Related work: self-critique/reflection optimizers (Self-Refine, Reflexion, Critiq)",
)

claim_prompt_instruction_methods = claim(
    "**Optimizer dimension 2: prompts and instructions.** Other "
    "approaches target prompts and instructions [@DSPy]: structured "
    "playbooks [@ACE], semantic-advantage priors [@TFGRPO], jointly "
    "optimized instruction-demonstration pipelines for multi-stage "
    "programs [@MIPRO], and reflective updates driven by Pareto-"
    "frontier traces [@GEPA]. The editable surface is the *system "
    "prompt or in-context playbook*; tools, middleware, and memory are "
    "treated as fixed.",
    title="Related work: prompt/instruction optimizers (DSPy, ACE, TF-GRPO, MIPRO, GEPA)",
)

claim_program_structure_methods = claim(
    "**Optimizer dimension 3: program structure.** A separate line "
    "edits program structure itself, in the form of skill libraries "
    "[@Voyager], scored program and agent archives evolved through "
    "mutation [@AlphaEvolve; @ADAS], and graph-structured workflows "
    "searched or learned from rollouts [@AFlow; @SymbolicLearning]. The "
    "editable surface is the *program graph or agent archive*; "
    "individual harness components are not directly optimized.",
    title="Related work: program-structure optimizers (Voyager, AlphaEvolve, ADAS, AFlow)",
)

claim_ace_method = claim(
    "**ACE [@ACE]: Agentic Context Engineering.** ACE is a self-evolution "
    "method that distills natural-language playbooks the agent reads "
    "in-context, evolving the *prompt-context* surface only. It does "
    "not edit tools, middleware, or long-term memory. In the AHE paper "
    "it is one of the two self-evolving baselines starting from the "
    "NexAU0 seed.",
    title="Related work: ACE (prompt-only playbook self-evolution)",
)

claim_tfgrpo_method = claim(
    "**TF-GRPO [@TFGRPO]: Training-Free Group Relative Policy "
    "Optimization.** TF-GRPO is a trajectory-feedback variant of GRPO "
    "that reinforces successful tool sequences without weight updates. "
    "It evolves the *prompt-injected* successful-trajectory pattern; it "
    "does not edit tools, middleware, or long-term memory. It is the "
    "second self-evolving baseline in the AHE comparison.",
    title="Related work: TF-GRPO (training-free trajectory-feedback policy optimization)",
)

claim_codex_human_baseline = claim(
    "**Codex CLI [@CodexCLI]: human-designed harness baseline.** Codex "
    "CLI is a human-designed harness for OpenAI Codex agents, used in "
    "the AHE comparison as one of three human-designed harnesses "
    "(alongside opencode [@Opencode] and terminus-2 [@Terminus2]). It "
    "represents the practitioner state-of-the-art that AHE seeks to "
    "exceed without manual engineering.",
    title="Related work: Codex CLI (human-designed harness, AHE's strongest manual baseline)",
)

claim_meta_harness = claim(
    "**Meta-Harness [@MetaHarness]: end-to-end joint optimization of all "
    "harness components.** Meta-Harness is the only prior approach the "
    "AHE paper identifies as attempting to jointly evolve the full set "
    "of editable components. It is concurrent / very recent work "
    "(March 2026); the AHE paper differentiates by emphasizing "
    "*observability infrastructure* (component / experience / decision) "
    "over the optimizer itself.",
    title="Related work: Meta-Harness (end-to-end joint harness optimization)",
)

# ---------------------------------------------------------------------------
# Section 2.2 closing: AHE's distinguishing design choices
# ---------------------------------------------------------------------------

claim_ahe_combinatorial_whole = claim(
    "**AHE design distinction 1: tunes the full harness as a "
    "combinatorial whole.** Unlike single-surface optimizers (prompt-"
    "only, skill-only, or playbook-only), AHE jointly evolves system "
    "prompt, tools, middleware, skills, sub-agents, and long-term "
    "memory simultaneously. This makes cross-component trade-offs "
    "(e.g., a tool-level guard interacting with a prompt-level rule) "
    "legible to the optimizer.",
    title="AHE distinction: jointly tunes all harness components, exposing cross-component trade-offs",
)

claim_ahe_minimal_human_prior = claim(
    "**AHE design distinction 2: minimal human prior.** AHE's seed "
    "harness NexAU0 is deliberately minimal -- a single shell-execution "
    "tool, no middleware, no skills, no sub-agents, no long-term "
    "memory. Methodology is left for the optimizer to discover from "
    "rollouts rather than fixed by hand. A seed already fitted to the "
    "target benchmark would contaminate every subsequent edit's "
    "attribution.",
    title="AHE distinction: minimal seed (single bash tool) keeps the human prior negligible",
)

__all__ = [
    "claim_harness_engineering_definition",
    "claim_evaluation_horizons",
    "claim_eval_infrastructure",
    "claim_self_critique_methods",
    "claim_prompt_instruction_methods",
    "claim_program_structure_methods",
    "claim_ace_method",
    "claim_tfgrpo_method",
    "claim_codex_human_baseline",
    "claim_meta_harness",
    "claim_ahe_combinatorial_whole",
    "claim_ahe_minimal_human_prior",
]
