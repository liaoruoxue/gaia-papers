"""Motivation: harnesses are central to coding-agent performance, but
engineering them remains a manual craft because automation hits three
structural obstacles -- a heterogeneous action space, voluminous unstructured
trajectories, and edits whose effect is hard to attribute.

Section 1 (Introduction) of Lin et al. 2026 [@Lin2026AHE]. Reference
implementation: [@AHEcode].
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup: what a harness is and why it matters
# ---------------------------------------------------------------------------

setup_coding_agent_regime = setting(
    "**Coding-agent deployment regime.** A *coding agent* is a large language "
    "model (LLM) deployed against long-horizon software-engineering tasks "
    "such as resolving GitHub issues over real-world repositories "
    "[@SWEbench; @SWEbenchMM; @SWEbenchPro] or executing multi-step "
    "terminal-driven workflows [@TerminalBench2]. Task completion depends "
    "not only on the underlying base language model but equally on the "
    "surrounding engineering components that mediate model-environment "
    "interaction.",
    title="Setup: coding agents on long-horizon software-engineering tasks",
)

setup_harness_definition = setting(
    "**Definition of a harness.** A *harness* is the collection of "
    "model-external, editable components that surround a base LLM and "
    "shape its capabilities on long-horizon tasks. Concretely, the "
    "harness comprises (i) the *system prompt* that shapes work style, "
    "(ii) the *tools* that expose the file system and shell, (iii) the "
    "*middleware* that controls context, execution, and recovery, "
    "(iv) *skills* (reusable workflow patterns), (v) *sub-agent* "
    "configurations, (vi) *long-term memory*, and (vii) tool "
    "descriptions. The harness mediates how the model perceives and "
    "acts on its environment "
    "[@RajasekaranHarness; @Lopopolo; @Trivedy; @OpenHands; @SWEAgent; "
    "@OpenClaw; @HermesAgent].",
    title="Setup: harness = model-external editable components (prompt, tools, middleware, skills, memory, sub-agents)",
)

setup_three_obstacles = setting(
    "**Three structural obstacles to automating harness engineering.** "
    "Automating harness adaptation as an *evolution agent* faces three "
    "matched obstacles: "
    "(O1) **Heterogeneous action space** -- editable harness components "
    "(prompts, tools, middleware, skills, sub-agents, memory, tool "
    "descriptions) live at different abstraction levels, so a flat "
    "edit-anything action space is unwieldy. "
    "(O2) **Voluminous unstructured trajectories** -- a single benchmark "
    "rollout produces millions of raw tokens of tool calls, shell output, "
    "and model thoughts, burying the actionable failure signal. "
    "(O3) **Attribution opacity** -- once an edit is applied, isolating "
    "*which* observable change in the next round is caused by *which* "
    "edit is hard, so trial-and-error edits accumulate without a "
    "feedback signal.",
    title="Setup: three obstacles -- heterogeneous action space, voluminous trajectories, attribution opacity",
)

setup_terminal_bench_2 = setting(
    "**Terminal-Bench 2 [@TerminalBench2].** A coding-agent benchmark "
    "consisting of 89 multi-hour, terminal-driven software-engineering "
    "tasks split into 4 easy, 55 medium, and 30 hard tasks. Each task "
    "runs in an isolated sandbox with a per-task timeout (extended to 1 "
    "hour in the AHE setup). The metric is **pass@1**, the mean binary "
    "success rate over k rollouts per task: pass@1 = (1 / k|D|) * "
    "sum_{i, j} r_{i, j} where r_{i, j} ∈ {0, 1} is the binary verifier "
    "reward of rollout j on task i. Trials that terminate on an "
    "infrastructure exception (sandbox crash, API timeout) contribute "
    "r = 0 rather than being dropped.",
    title="Setup: Terminal-Bench 2 evaluation protocol (89 tasks, pass@1)",
)

setup_swebench_verified = setting(
    "**SWE-bench-verified [@SWEbench].** A coding-agent benchmark of 500 "
    "tasks across seven Python repositories (django, sympy, sphinx-doc, "
    "matplotlib, scikit-learn, pydata, astropy) where each task asks the "
    "agent to resolve a real-world GitHub issue. The companion *tokens "
    "per trial* metric, denoted Tokens_k, is the mean per-trial total of "
    "prompt plus completion tokens across all LLM calls (in thousands), "
    "averaged over completed trials.",
    title="Setup: SWE-bench-verified evaluation protocol (500 tasks across 7 repos)",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "How can an *evolution agent* jointly and stably evolve all editable "
    "components of a coding agent's harness -- the system prompt, tools, "
    "middleware, skills, sub-agents, and long-term memory -- given the "
    "three structural obstacles of heterogeneous action space, "
    "voluminous trajectories, and attribution opacity?",
    title="Central question: how to jointly + stably evolve all editable harness components?",
)

# ---------------------------------------------------------------------------
# Diagnosis: state of the field
# ---------------------------------------------------------------------------

claim_harness_central_to_perf = claim(
    "**Premise: harness design materially shifts task completion on "
    "long-horizon coding benchmarks even with the base model held "
    "fixed.** Independent works [@Trivedy; @OpenHands] document that "
    "swapping in different harnesses changes pass@1 substantially under "
    "an unchanged underlying language model, making harness engineering "
    "a first-class lever for improving coding agents.",
    title="Premise: harness design changes pass@1 with base model fixed",
)

claim_optimal_harness_model_specific = claim(
    "**Premise: the optimal harness is model-specific and must be "
    "re-adapted as the base model changes.** A harness tuned for one "
    "base model often underperforms on another and must be re-tuned for "
    "each new base model release. Combined with the rapid pace of base "
    "model releases [@MiMoV25; @Qwen36; @Qwen3; @DeepSeekV4; @Kimi26; "
    "@Kimi25], this creates a widening gap between model capability and "
    "the harness needed to realize it [@OpenClaw].",
    title="Premise: optimal harness is model-specific and must be re-adapted per base model",
)

claim_manual_harness_practice = claim(
    "**State of practice: harness engineering is a manual craft.** "
    "Developers inspect trajectories, identify recurring failure "
    "patterns, and hand-craft edits across prompts, tools, middleware, "
    "and skills. As base models advance rapidly "
    "[@MiMoV25; @Qwen36; @Qwen3; @DeepSeekV4; @Kimi26; @Kimi25], this "
    "manual loop struggles to keep pace [@OpenClaw].",
    title="State of practice: harness engineering is currently a manual craft",
)

claim_existing_evolution_partial = claim(
    "**State of the literature: existing evolution-agent approaches edit "
    "only one harness component at a time.** Most automated agent-"
    "optimization approaches focus on a single component, typically the "
    "prompt [@Reflexion; @SelfRefine; @ExpeL], skills "
    "[@Voyager; @SkillRL], or an in-context playbook [@ACE]. Only "
    "[@MetaHarness] attempts to jointly evolve the full set of editable "
    "components.",
    title="State of literature: existing self-evolution agents edit only one harness component",
)

claim_two_structural_obstacles = claim(
    "**Why end-to-end joint evolution is hard.** Jointly evolving "
    "multiple harness components end-to-end faces two structural "
    "obstacles: (a) long, unstructured trajectories yield little "
    "actionable signal, and (b) tightly coupled harness frameworks make "
    "edits beyond the prompt error-prone (one prompt change implicitly "
    "depends on a tool, which depends on a middleware, etc.).",
    title="Why end-to-end harness evolution is hard: unstructured trajectories + tight component coupling",
)

# ---------------------------------------------------------------------------
# Central insight + AHE introduction
# ---------------------------------------------------------------------------

claim_observability_bottleneck = claim(
    "**Central insight: the bottleneck is observability, not evolution-"
    "agent capability.** Once the evolution agent receives structured "
    "context over a clear action space, it can reliably converge on "
    "better harness designs [@BitterLesson; @Zunic]. The key lever is "
    "therefore not a more powerful evolution model but observability "
    "infrastructure that reduces noise in component, trajectory, and "
    "decision feedback.",
    title="Insight: harness evolution is bottlenecked by observability, not by evolution-agent capability",
)

claim_ahe_three_pillars = claim(
    "**AHE: a closed loop driven by three matched observability pillars.** "
    "Agentic Harness Engineering (AHE) is a closed evolution loop "
    "centered on three observability pillars matched to the three "
    "obstacles: "
    "**Pillar 1 -- Component observability.** A decoupled harness "
    "substrate exposes seven editable component types as files, so each "
    "failure pattern maps cleanly to a single component class and the "
    "action space is explicit and revertible. "
    "**Pillar 2 -- Experience observability.** A layered, drill-down "
    "evidence corpus distilled from millions of raw trajectory tokens "
    "(roughly 10M -> 10K), so the evolver consumes structured root "
    "causes rather than raw logs. "
    "**Pillar 3 -- Decision observability.** A change manifest pairs "
    "every edit with a self-declared prediction, later verified against "
    "the next round's task-level outcomes; each edit becomes a "
    "falsifiable contract and ineffective ones are reverted at file "
    "granularity.",
    title="AHE: closed loop driven by 3 observability pillars (component / experience / decision)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 2",
        "caption": "Fig. 2: The AHE pipeline links three observable surfaces -- components, rollout experience, edit decisions -- into one closed loop.",
    },
)

# ---------------------------------------------------------------------------
# Headline empirical claims
# ---------------------------------------------------------------------------

claim_main_terminal_headline = claim(
    "**Headline empirical claim (main result, Terminal-Bench 2).** Ten "
    "AHE iterations starting from the bash-only NexAU0 seed lift pass@1 "
    "on Terminal-Bench 2 [@TerminalBench2] (89 tasks, GPT-5.4 high "
    "[@GPT54]) from **69.7%** at iteration 0 to **77.0%** at the best "
    "iteration, surpassing the human-designed harness Codex-CLI "
    "[@CodexCLI] (71.9%) and the self-evolving baselines ACE [@ACE] "
    "(68.9%) and TF-GRPO [@TFGRPO] (72.3%).",
    title="Headline: 10 AHE iterations lift Terminal-Bench 2 pass@1 from 69.7% to 77.0%",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 1 + Table 1",
        "caption": "Fig. 1 + Table 1: AHE evolves a bash-only seed past every human-designed and self-evolving baseline on Terminal-Bench 2.",
    },
)

claim_swe_transfer_headline = claim(
    "**Headline transfer claim (cross-benchmark).** Without further "
    "evolution, the frozen AHE harness evolved on Terminal-Bench 2 "
    "transfers to SWE-bench-verified [@SWEbench]: it tops aggregate "
    "success rate (75.6% vs the seed NexAU0's 75.2%) at **12% fewer "
    "tokens than the seed** (461k vs 526k tokens per trial in "
    "aggregate).",
    title="Headline transfer: frozen AHE on SWE-bench-verified beats seed at 12% fewer tokens",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 2",
        "caption": "Table 2: Cross-benchmark transfer on SWE-bench-verified.",
    },
)

claim_cross_family_headline = claim(
    "**Headline transfer claim (cross-model-family).** On Terminal-Bench "
    "2, the frozen AHE harness re-evaluated on three alternate base-"
    "model families yields gains of **+5.1 to +10.1 pp** without any "
    "re-evolution: gemini-3.1-flash-lite-preview [@Gemini31FlashLite] "
    "+5.1 pp (36.5% -> 41.6%), qwen-3.6-plus [@Qwen36; @Qwen3] +6.3 pp "
    "(56.2% -> 62.5%), and deepseek-v4-flash [@DeepSeekV4] +10.1 pp "
    "(51.7% -> 61.8%). The largest gains occur on bases further from "
    "saturation.",
    title="Headline transfer: frozen AHE yields +5.1 to +10.1 pp on 3 alternate model families",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 3",
        "caption": "Fig. 3: Cross-model transfer on Terminal-Bench 2 (89 tasks).",
    },
)

claim_ablation_headline = claim(
    "**Headline localization claim (component ablation).** The AHE gain "
    "is concentrated in three component classes -- *tools*, *middleware*, "
    "and *long-term memory* -- which each carry the improvement on their "
    "own (+3.3, +2.2, +5.6 pp respectively when swapped alone into the "
    "NexAU0 seed). The *system prompt* swapped alone regresses (-2.3 pp). "
    "This shows that **factual harness structure transfers while "
    "prose-level strategy does not**.",
    title="Headline localization: gain lives in tools/middleware/memory, NOT system prompt",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 3",
        "caption": "Table 3: Component-level ablations on Terminal-Bench 2.",
    },
)

claim_three_contributions = claim(
    "**Stated contributions.** The paper makes three contributions: "
    "(i) it formulates *agent-driven harness evolution* for coding "
    "agents and proposes AHE, identifying observability across "
    "components, trajectories, and decisions as the design pivot; "
    "(ii) it empirically shows that AHE lifts pass@1 on Terminal-Bench "
    "2 from 69.7% to 77.0%, surpasses human-designed and automated "
    "baselines, and produces a frozen harness that transfers across "
    "benchmarks and base-model families; and (iii) it reveals two "
    "limits of agent-driven evolution -- harness components interact "
    "non-additively, and the loop's self-attribution is reliable for "
    "fixes but blind to regressions.",
    title="Three stated contributions of the paper",
)

__all__ = [
    "setup_coding_agent_regime",
    "setup_harness_definition",
    "setup_three_obstacles",
    "setup_terminal_bench_2",
    "setup_swebench_verified",
    "q_central",
    "claim_harness_central_to_perf",
    "claim_optimal_harness_model_specific",
    "claim_manual_harness_practice",
    "claim_existing_evolution_partial",
    "claim_two_structural_obstacles",
    "claim_observability_bottleneck",
    "claim_ahe_three_pillars",
    "claim_main_terminal_headline",
    "claim_swe_transfer_headline",
    "claim_cross_family_headline",
    "claim_ablation_headline",
    "claim_three_contributions",
]
