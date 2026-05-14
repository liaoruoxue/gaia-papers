"""Section 1: Introduction / Motivation -- provider-fragmented frontier LLMs,
manual orchestration limits, the RL Conductor as a learned meta-agent, and
the stated contributions.

Source: Nielsen et al. 2026 [@Nielsen2026Conductor], Section 1, p. 1-2.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup (background facts taken from Section 1)
# ---------------------------------------------------------------------------

setup_frontier_llms = setting(
    "**Frontier large language models.** Through unprecedented scale and "
    "engineering effort, modern Large Language Models (LLMs) from different "
    "providers -- including Claude Sonnet 4 [@Anthropic2025Sonnet], GPT-5 "
    "[@OpenAI2025GPT5], earlier GPT-4 [@OpenAI2023GPT4], Gemini "
    "[@Team2023Gemini; @Comanici2025Gemini25], DeepSeek-R1 "
    "[@Guo2025DeepSeekR1], Qwen3 [@Yang2025Qwen3], Gemma 3 [@Team2025Gemma3], "
    "and Llama 4 [@MetaAI2025Llama4] -- have been expensively trained and "
    "finetuned, demonstrating the ability to solve formidably complex "
    "tasks with performance even approaching that of top human experts "
    "[@Luong2025].",
    title="Setup: provider-diverse frontier LLMs trained at massive scale",
)

setup_agentic_products = setting(
    "**Agentic workflows in commercial AI.** Manually-designed agentic "
    "workflows are critical components of commercial AI products including "
    "Amazon Q Developer [@AWS2025Q], Microsoft Copilot "
    "[@Microsoft2025Copilot], and Cursor [@Anysphere2025Cursor]. The "
    "prevalence of these manually-engineered scaffolds illustrates that "
    "utilizing latent LLM capabilities to their full potential remains a "
    "challenge even for experienced users.",
    title="Setup: manual agentic workflows dominate commercial AI products",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Different frontier LLMs (Claude, GPT-5, Gemini, Qwen3, DeepSeek-R1, "
    "Gemma 3) excel at different sub-domains -- no single LM is universally "
    "optimal across all tasks [@Chang2024SurveyEval]. Manual agentic "
    "scaffolds and self-refinement strategies "
    "[@Wei2022CoT; @Madaan2023SelfRefine] partially address this but are "
    "fixed at human-design time. **Can a small language model be trained -- "
    "end-to-end with reinforcement learning -- to automatically discover "
    "powerful coordination strategies over a pool of much larger and more "
    "powerful LLM workers?**",
    title="Central question: can RL train a small LM to coordinate frontier LLM workers automatically?",
)

# ---------------------------------------------------------------------------
# Diagnosis (Section 1, paragraphs 1-2)
# ---------------------------------------------------------------------------

claim_provider_specialization = claim(
    "**Provider-domain specialization of frontier LLMs.** Different LLMs "
    "from different providers are expensively trained and finetuned to "
    "specialize in particular datasets and domains, with no single LM "
    "universally optimal across all tasks [@Chang2024SurveyEval]. The "
    "Conductor's own evaluation confirms this: GPT-5 leads in math and "
    "competitive coding (AIME, LiveCodeBench), Gemini 2.5 Pro excels at "
    "scientific reasoning (GPQA-Diamond), and Claude Sonnet 4 is among "
    "the dominant models at code generation with diverse function calls "
    "(BigCodeBench) yet relatively weaker in LiveCodeBench. This "
    "specialization extends down to a sub-task level (planner vs writer "
    "roles).",
    title="Diagnosis: no single frontier LLM dominates -- per-task specialization across providers",
)

claim_manual_orchestration_limits = claim(
    "**Limit of manual orchestration / prompt-engineered scaffolds.** "
    "Effective prompting [@Wei2022CoT] and self-refinement strategies "
    "[@Madaan2023SelfRefine] remain a core focus of current research, but "
    "the resulting agentic workflows are manually designed at human "
    "engineering time. Manual scaffolds (i) cannot adapt to per-input "
    "task difficulty, (ii) are limited to coordination patterns the "
    "designer anticipated, and (iii) require re-engineering as the "
    "underlying frontier-LLM pool evolves.",
    title="Diagnosis: manual orchestration cannot adapt per-input and ages out as the LLM pool evolves",
)

claim_prior_routing_inexpressive = claim(
    "**Limit of prior multi-agent routing frameworks.** Prior multi-agent "
    "routing and scaffolding methods -- MASRouter [@Yue2025MASRouter], "
    "RouterDC [@Chen2024RouterDC], Smoothie [@Guha2024Smoothie], MoA "
    "[@Wang2024MoA], multi-agent debate [@Du2023MultiAgentDebate], and "
    "GPTSwarm [@Zhuge2024GPTSwarm] -- train a router classifier or learn "
    "an embedding space that selects models and/or human-designed "
    "coordination topologies from a *pre-specified* option set. Their "
    "expressivity is inherently constrained: they cannot freely "
    "prompt-engineer subtasks in natural language, and the search space "
    "of topologies they can express is fixed at design time.",
    title="Diagnosis: prior routing frameworks are inexpressive -- fixed topology options, no free prompt-engineering",
)

# ---------------------------------------------------------------------------
# Central proposal
# ---------------------------------------------------------------------------

claim_conductor_proposal = claim(
    "**The RL Conductor proposal.** The paper introduces the "
    "**Conductor**: a new kind of reasoning language model trained with "
    "reinforcement learning (GRPO [@Guo2025DeepSeekR1; @Shao2024DeepSeekMath]) "
    "to dynamically (i) divide an input problem into natural-language "
    "**subtasks**, (ii) delegate each subtask to a specific worker LLM "
    "from an available pool, and (iii) specify a per-step **access list** "
    "controlling which previous-step outputs each worker can see -- "
    "defining the communication topology. The Conductor itself is an LLM "
    "outputting three parsed Python lists (`model_id`, `subtasks`, "
    "`access_list`) per workflow, enabling completely flexible "
    "natural-language workflow specification.",
    title="Proposal: the Conductor -- an RL-trained LLM that outputs subtask+model+access-list workflows in natural language",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 2",
        "caption": "Fig. 2: Conductor output -- model_id list, subtasks list, access_list list as parseable Python lists.",
    },
)

claim_conductor_two_emergent_skills = claim(
    "**Two emergent skills of the trained Conductor.** Through pure "
    "end-to-end GRPO reward maximization, the Conductor learns two "
    "emergent coordination skills: "
    "(a) **Targeted communication topologies** -- designing per-input "
    "agentic workflows ranging from simple best-of-N and sequential "
    "chains to parallelizable tree-structured collaborations, harnessing "
    "the individual strengths and synergies of its highly specialized "
    "workers; "
    "(b) **Focused prompt engineering** -- crafting natural-language "
    "subtasks tailored to each assigned worker that maximally leverage "
    "that worker's individual capabilities. "
    "These skills emerge naturally without explicit supervision -- only "
    "the verifiable end-task reward.",
    title="Proposal: two emergent skills -- targeted topology design + focused prompt engineering",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 3",
        "caption": "Fig. 3: Emergence of powerful coordination strategies over training -- early Conductor issues sound subtasks but no verification; near convergence the Conductor uses planners, targeted instructions, refinement, and verification.",
    },
)

# ---------------------------------------------------------------------------
# Two finetuning extensions (Section 1, paragraph "We also effectively
# extend our framework...")
# ---------------------------------------------------------------------------

claim_extension_dynamic_pool = claim(
    "**Extension 1: Adaptive worker pool via randomized-pool finetuning.** "
    "A short finetuning phase trains the pretrained Conductor on "
    "randomly-sampled $k$-element subsets from the full $n$-worker pool. "
    "The resulting Conductor generalizes to **arbitrary user-specified "
    "subsets** of open- and closed-source workers, allowing users to "
    "extract strong performance under cost preferences or API "
    "availability constraints without expensive paid-API calls.",
    title="Proposal: dynamic worker pool -- finetune with randomized k-of-n subsets to generalize to arbitrary user-specified pools",
)

claim_extension_recursive = claim(
    "**Extension 2: Self-referential recursive topologies as test-time "
    "scaling.** A second short finetuning phase allows the Conductor to "
    "specify *itself* as a worker LLM, giving rise to a new kind of "
    "**recursive topology**. In each inner recursive call, the Conductor "
    "is provided its own parent output plus the previous agent's "
    "response, and decides whether to (a) instantiate a new workflow "
    "(refining/correcting the previous result) or (b) end recursion by "
    "returning the previous response. The maximum recursion depth is a "
    "tunable inference-time hyperparameter, enabling a new axis of "
    "dynamic test-time scaling via online iterative adaptation.",
    title="Proposal: recursive topologies -- Conductor selects itself as worker, new test-time scaling axis",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 12",
        "caption": "Fig. 12: Recursive Conductor visualization -- at test time the Conductor adapts its initial coordination strategy on the fly.",
    },
)

# ---------------------------------------------------------------------------
# Headline empirical claims (Section 1, last paragraphs / Figure 1)
# ---------------------------------------------------------------------------

claim_headline_sota = claim(
    "**Headline empirical claim: state-of-the-art on hard reasoning "
    "benchmarks.** A 7B Conductor, trained over a pool of much larger and "
    "more powerful worker LLMs (Gemini 2.5 Pro [@Comanici2025Gemini25], "
    "Claude Sonnet 4 [@Anthropic2025Sonnet], GPT-5 [@OpenAI2025GPT5], "
    "DeepSeek-R1-Distill-Qwen-32B [@Guo2025DeepSeekR1], Gemma 3-27B-it "
    "[@Team2025Gemma3], Qwen3-32B [@Yang2025Qwen3]), attains "
    "**state-of-the-art performance records** on six challenging "
    "reasoning benchmarks under the unconstrained-budget setting "
    "(reported in Table 1): MATH500 99.4, MMLU 94.1, RLPR 44.75, "
    "LiveCodeBench V6 83.93, AIME25 93.3, BigCodeBench 37.86, GPQA-D "
    "87.5 (avg 77.27) -- exceeding the best baseline (GPT-5: avg 74.78) "
    "on every column.",
    title="Headline: 7B Conductor attains SOTA on all 7 benchmarks (avg 77.27 vs GPT-5 74.78)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Fig. 1 + Table 1",
        "caption": "Fig. 1: Conductor attains SOTA in GPQA and LiveCodeBench leaderboards. Table 1: Comparison with previous best unconstrained results across 7 benchmarks.",
    },
)

claim_headline_beats_baselines = claim(
    "**Headline efficacy claim.** Beyond individual frontier workers, the "
    "Conductor outperforms (i) **5x-self-reflection** of each worker, "
    "(ii) **5x-context-length** evaluation of each worker, and "
    "(iii) **expensive prior multi-agent baselines** (MASRouter "
    "[@Yue2025MASRouter], MoA [@Wang2024MoA], RouterDC "
    "[@Chen2024RouterDC], Smoothie [@Guha2024Smoothie]) trained and "
    "evaluated with the same set of 7 agents, at a fraction of the "
    "inference cost (3 average workflow steps vs 4-5 in MASRouter, "
    "8 model calls in MoA).",
    title="Headline: Conductor outperforms self-reflection, 5x context, and prior multi-agent baselines at lower cost",
)

claim_headline_pool_generality = claim(
    "**Headline robustness claim: cross-pool generalization.** The "
    "randomized-pool-finetuned Conductor extracts strong performance "
    "from any user-specified subset of workers. Evaluated on "
    "**open-source-only** pools, it **outperforms Claude Sonnet 4 by "
    "almost 10%** within the constrained setting; evaluated on "
    "**closed-source-only** pools, it matches its original pretrained "
    "performance. This adaptability mitigates the field's inherent "
    "cost-vs-performance tradeoffs.",
    title="Headline: randomized-pool finetuning yields cross-pool generalization (open-only beats Claude by ~10%)",
)

claim_headline_recursive_scaling = claim(
    "**Headline recursive-scaling claim.** Allowing the recursive "
    "Conductor to select itself as a worker -- with at most $2\\times$ "
    "the original agentic-call budget -- yields **substantial additional "
    "gains on out-of-distribution tasks**, especially BigCodeBench "
    "where the pretrained Conductor's coordination strategies must adapt "
    "to GPT-5's surprisingly weak performance. Recursive Conductor "
    "achieves an average of **63.00** vs non-recursive Conductor "
    "**61.93** across AIME25/BigCodeBench/GPQA-D under the constrained "
    "setting.",
    title="Headline: recursive Conductor adds gains via dynamic test-time scaling (63.00 vs 61.93 avg)",
    metadata={
        "figure": "artifacts/2512.04388.pdf, Table 2",
        "caption": "Table 2: Test-time recursion generates further performance gains, especially on BigCodeBench (37.8 -> 40.0).",
    },
)

# ---------------------------------------------------------------------------
# Stated contributions (Section 1, three bullets)
# ---------------------------------------------------------------------------

claim_three_contributions = claim(
    "**Three stated contributions of the Conductor paper.** "
    "(C1) **Method** -- the RL Conductor: a language model trained "
    "through end-to-end reinforcement learning to divide challenging "
    "problems, delegate targeted subtasks, and design communication "
    "topologies for a set of worker LLMs, all in natural language. "
    "(C2) **Empirical headline** -- by obtaining effective prompt "
    "engineering and coordination skills, a small **7B** Conductor "
    "lifts its worker LLMs to new heights, attaining state-of-the-art "
    "results on complex reasoning tasks and outperforming more "
    "expensive multi-agent baselines. "
    "(C3) **Extensions** -- a short finetuning phase unlocks "
    "(a) adaptability to arbitrary agent pools, and (b) powerful "
    "recursive topologies yielding a new test-time scaling axis.",
    title="Three stated contributions: RL Conductor method / 7B SOTA empirical / finetune-unlocked extensions",
)

claim_broader_thesis = claim(
    "**Broader thesis: language-model coordination can be unlocked "
    "through RL.** This is **among the early work** demonstrating that "
    "language-model coordination can be unlocked through reinforcement "
    "learning, where **powerful coordination strategies emerge naturally "
    "in LLMs through pure end-to-end reward maximization** -- without "
    "supervised demonstrations of correct coordination, hand-engineered "
    "scaffolds, or pre-specified topology vocabularies. The end-to-end "
    "RL signal alone is sufficient to discover sophisticated "
    "prompt-engineering and multi-agent coordination behaviors.",
    title="Broader thesis: end-to-end RL on verifiable rewards alone unlocks emergent LLM coordination",
)

__all__ = [
    "setup_frontier_llms",
    "setup_agentic_products",
    "q_central",
    "claim_provider_specialization",
    "claim_manual_orchestration_limits",
    "claim_prior_routing_inexpressive",
    "claim_conductor_proposal",
    "claim_conductor_two_emergent_skills",
    "claim_extension_dynamic_pool",
    "claim_extension_recursive",
    "claim_headline_sota",
    "claim_headline_beats_baselines",
    "claim_headline_pool_generality",
    "claim_headline_recursive_scaling",
    "claim_three_contributions",
    "claim_broader_thesis",
]
