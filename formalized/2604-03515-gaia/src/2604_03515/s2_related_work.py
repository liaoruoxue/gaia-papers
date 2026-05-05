"""Section 2: Related Work.

Section 2 of Rombaut 2026 [@Rombaut2026]. Surveys the four research
threads this study sits at the intersection of, in each case
identifying what prior work contributes and what gap it leaves:

* 2.1 LLM agent architecture surveys [@Masterman2024; @Nowaczyk2025]:
  conceptual capability vocabularies, but cannot distinguish
  production coding agents at the implementation level.
* 2.2 Coding agent trajectory and behaviour studies [@Ceka2025;
  @Majgaonkar2026; @Bouzenia2025; @Fan2025SWEEffi]: black-box
  observation; confounded by varying LLMs.
* 2.3 Individual system descriptions [@SWEAgent; @Aider; @Bui2026;
  @Agentless; @DARSAgent; @AutoCodeRover; @OpenHands]: per-system
  depth, but no comparative reference.
* 2.4 Coding agent evaluation and benchmarks [@Jimenez2024SWEbench;
  @Garg2026; @Xu2025SWECompass; @Chen2026; @Souza2026]: benchmark
  scores confound scaffold, model, and configuration.

Each subsection grounds the corresponding gap in motivation.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# 2.1 LLM agent architecture surveys
# ---------------------------------------------------------------------------

claim_capability_taxonomies_existed = claim(
    "**Capability-based agent taxonomies (Section 2.1).** Prior "
    "survey work organizes LLM-based agents by abstract capabilities. "
    "Masterman et al. [@Masterman2024] propose a five-component "
    "reference model (reasoning, planning, tool use, memory, "
    "reflection) and classify interaction patterns across single- "
    "and multi-agent designs. Nowaczyk [@Nowaczyk2025] offers a "
    "capability-based taxonomy (tool-using, memory-augmented, "
    "planning, multi-agent, embodied) and argues that reliability is "
    "an architectural property rather than a function of model "
    "quality alone. Broader surveys [@Zhang2026Survey] cover coding "
    "agents as one category among many.",
    title="2.1 prior surveys organize agents by abstract capabilities",
)

claim_capability_taxonomies_indistinguishable = claim(
    "**Empirical observation (Section 2.1).** Every coding agent in "
    "the present 13-agent corpus qualifies as 'tool-using, "
    "memory-augmented, planning' under the prior capability-based "
    "schemes [@Masterman2024; @Nowaczyk2025]. Yet the scaffold "
    "architectures differ in ways that affect cost, reliability, and "
    "failure modes. Two agents the prior schemes label identically "
    "(e.g. Moatless Tools using MCTS and a simple while-loop "
    "test-driven retry agent) differ fundamentally in control flow, "
    "state management, and resource consumption.",
    title="2.1 every coding agent fits all capability labels -- labels do not discriminate",
)

claim_react_reflexion_paradigms = claim(
    "**ReAct and Reflexion as paradigms, not architectures.** The "
    "ReAct paradigm [@Yao2023ReAct] interleaves reasoning traces and "
    "task-specific actions in a thought-action-observation loop; "
    "seven of the 13 agents in this study use a sequential ReAct "
    "loop as their primary control structure. Reflexion "
    "[@Shinn2023Reflexion] formalizes verbal reinforcement learning "
    "where agents reflect on failed attempts and store reflections "
    "in episodic memory; this pattern is foundational to the "
    "generate-test-repair primitive observed across the corpus. "
    "Crucially, both ReAct and Reflexion describe *algorithmic "
    "paradigms*, not scaffold architectures: the gap between "
    "'interleave thoughts and actions' and a production "
    "implementation with tool registration, context compaction, "
    "multi-model routing, and persistent state is precisely what the "
    "present study documents.",
    title="2.1 ReAct/Reflexion are paradigms, not production scaffold architectures",
)

# ---------------------------------------------------------------------------
# 2.2 Coding agent trajectory and behaviour studies
# ---------------------------------------------------------------------------

claim_trajectory_studies_summary = claim(
    "**Trajectory and behaviour studies (Section 2.2).** A "
    "complementary line of work analyses what coding agents *do* at "
    "runtime by studying execution trajectories. Ceka et al. "
    "[@Ceka2025] collect full execution traces from five agents on "
    "SWE-bench Verified, normalize them into a unified action "
    "schema, and extract recurring decision pathways "
    "(exploration-heavy, patch-first, test-driven). They find bug "
    "localization is the primary bottleneck and that early test "
    "generation correlates strongly with success. Majgaonkar et al. "
    "[@Majgaonkar2026] analyse OpenHands, SWE-agent, and Prometheus "
    "trajectory logs, reporting that failure trajectories are "
    "12-82% longer than successful ones and that repository "
    "navigation dominates over patch writing. Bouzenia and Pradel "
    "[@Bouzenia2025] study RepairAgent, AutoCodeRover, and "
    "OpenHands, finding that 0.5-4.8% thought-action misalignment "
    "strongly correlates with failure.",
    title="2.2 trajectory studies catalogued: behavioural regularities found",
)

claim_trajectory_studies_blackbox_limit = claim(
    "**Trajectory studies treat agents as black boxes (Section 2.2).** "
    "Trajectory studies observe *what* agents do but cannot explain "
    "*why*. A finding such as 'agents with shorter trajectories "
    "succeed more often' cannot distinguish between a scaffold that "
    "enforces early termination, one that implements efficient "
    "search heuristics, and one that simply has a low iteration "
    "budget. The taxonomic source-code analysis presented in this "
    "paper provides the *missing explanatory layer*.",
    title="2.2 trajectory studies cannot attribute behaviour to scaffold design",
)

claim_trajectory_model_confound = claim(
    "**Confounded model and scaffold effects (Section 2.2).** Prior "
    "trajectory studies used different LLMs for different agents "
    "[@Majgaonkar2026; @Bouzenia2025], confounding scaffold effects "
    "with model effects. Majgaonkar et al. compare Claude 3.5 "
    "Sonnet-based OpenHands trajectories against DeepSeek-V3-based "
    "Prometheus trajectories. With the model varying simultaneously "
    "with the scaffold, no behavioural difference observed in "
    "trajectory data can be uniquely attributed to scaffold design.",
    title="2.2 trajectory studies' agent-specific LLM choice confounds scaffold attribution",
)

claim_swe_effi_token_snowball = claim(
    "**Resource-oriented analysis (Section 2.2).** Fan et al. "
    "[@Fan2025SWEEffi] move from behavioural to resource-oriented "
    "analysis, measuring token consumption, cost, and computation "
    "time for five scaffolds across three LLMs. They identify the "
    "**'token snowball effect'** (linear input token growth with "
    "API calls due to naive conversation history accumulation) and "
    "**'expensive failures'** (failing attempts consuming up to "
    "4 times the resources of successful ones). The present "
    "study's context-compaction dimension (Section 4.3.2) explains "
    "the architectural variation behind these observations; "
    "SWE-Effi itself does not examine the scaffold code, "
    "distinguishing only 'agentic' versus 'procedural'.",
    title="2.2 SWE-Effi documents token-snowball + expensive-failure cost patterns",
)

# ---------------------------------------------------------------------------
# 2.3 Individual system descriptions
# ---------------------------------------------------------------------------

claim_individual_system_descriptions = claim(
    "**Individual system descriptions (Section 2.3).** Detailed "
    "architectural descriptions exist for several individual coding "
    "agents and collectively demonstrate that scaffold design "
    "choices significantly affect agent behaviour. Yang et al. "
    "[@SWEAgent] introduce the **agent-computer interface (ACI)** "
    "concept for SWE-agent, showing that designing custom shell "
    "commands to structure repository interaction is itself an "
    "architectural decision. Gauthier [@Aider] describes Aider's "
    "PageRank-weighted repo map and model-specific edit format "
    "selection. Bui [@Bui2026] describes a four-layer terminal "
    "agent architecture with dual-agent design, multi-model "
    "routing, lazy tool discovery, and adaptive context compaction, "
    "concluding that 'tool reliability matters more than model "
    "capability'. Other system papers illuminate the spectrum of "
    "agent autonomy: Xia et al. [@Agentless] argue agentic "
    "scaffolds are unnecessary for many tasks (a fixed pipeline "
    "matches or exceeds agentic approaches); Aggarwal et al. "
    "[@DARSAgent] present tree-structured search with LLM-based "
    "branch selection; Zhang et al. [@AutoCodeRover] describe "
    "AST-based context retrieval with spectrum-based fault "
    "localization; Wang et al. [@OpenHands] describe the "
    "event-sourced architecture and agent delegation mechanisms of "
    "OpenHands.",
    title="2.3 per-system architectural depth exists for ~6 individual coding agents",
)

claim_individual_system_unmapped_space = claim(
    "**The design space remains unmapped (Section 2.3).** Each "
    "individual system description provides architectural depth for "
    "a single agent, but the design space as a whole remains "
    "unmapped: practitioners cannot compare control loop strategies, "
    "tool interface designs, or context management approaches "
    "without reading a dozen or more codebases independently. The "
    "present study's contribution is to *extend per-system depth "
    "across 13 agents*, enabling the comparative analysis that "
    "individual descriptions cannot provide.",
    title="2.3 per-system depth does not aggregate into a comparative reference",
)

claim_configuration_artifacts_orthogonal = claim(
    "**Configuration artefacts vs scaffold architecture (Section 2.3).** "
    "Galster et al. [@Galster2026] analyse 2,926 GitHub repositories "
    "to characterize configuration artefacts (instruction files, "
    "prompt templates, skills definitions, structured configuration) "
    "across five commercial coding tools, finding that configuration "
    "practices remain fragmented and that advanced features (skills, "
    "sub-agent configurations) are rarely used. This work is "
    "*complementary* to the present study: configuration artefacts "
    "control what instructions the agent receives, while scaffold "
    "architecture determines how the agent processes those "
    "instructions. A `CLAUDE.md` file specifying 'always run tests "
    "before committing' is a developer-facing configuration; the "
    "scaffold's generate-test-repair loop that *implements* that "
    "instruction is an architectural feature.",
    title="2.3 configuration vs architecture: complementary, not redundant",
)

# ---------------------------------------------------------------------------
# 2.4 Coding agent evaluation and benchmarks
# ---------------------------------------------------------------------------

claim_swebench_central = claim(
    "**SWE-bench is central but limited (Section 2.4).** SWE-bench "
    "[@Jimenez2024SWEbench] has become the de facto evaluation "
    "standard for coding agents. Its limitations are increasingly "
    "well documented: overly detailed issue descriptions inflate "
    "resolution rates [@Garg2026], single-language bias limits "
    "generalizability [@Jimenez2024SWEbench; @Xu2025SWECompass], "
    "and confounded scaffold-model effects make it difficult to "
    "attribute performance to architectural choices "
    "[@Fan2025SWEEffi]. Newer benchmarks (SWE-bench Pro "
    "[@Deng2025SWEbenchPro], SWE-Compass [@Xu2025SWECompass]) "
    "address subsets of these concerns. Chen et al. [@Chen2026] "
    "find that prompt interventions adding/removing testing change "
    "outcomes by at most 2.6 percentage points, suggesting that "
    "*scaffold-level orchestration of testing* (lint-test cycles, "
    "test-gated retries, MCTS reward signals), rather than "
    "model-native test-writing, is the architecturally relevant "
    "variable.",
    title="2.4 SWE-bench scores confound scaffold, model, and configuration",
)

claim_taxonomy_enables_controlled_experiments = claim(
    "**The taxonomy enables controlled experiments (Section 2.4).** "
    "The present study deliberately does not benchmark agent "
    "performance, because benchmark scores confound scaffold "
    "architecture with model capability, prompt engineering, and "
    "incidental configuration. Isolating the scaffold's contribution "
    "requires the kind of architectural decomposition presented "
    "here. The taxonomy enables future controlled experiments by "
    "identifying the specific variables to hold constant: e.g. "
    "comparing agents with identical tool sets but different loop "
    "strategies, or identical loops but different compaction "
    "strategies, with the model held constant (Section 5.5).",
    title="2.4 controlled experiments need taxonomic variables -- this paper provides them",
)

claim_souza_machado_call = claim(
    "**Architecture-aware evaluation called for (Section 2.4).** "
    "Souza and Machado [@Souza2026] explicitly call for "
    "architecture-aware evaluation metrics that link internal agent "
    "components (planner, memory, tool router) to observable "
    "outcomes, proposing a component-to-metric mapping framework. "
    "However, their proposal is *conceptual*: it has not been "
    "tested on real systems and depends on architectural "
    "documentation that, prior to the present study, did not exist "
    "for most coding agents. The present taxonomy provides the "
    "architectural vocabulary that such evaluation frameworks "
    "require.",
    title="2.4 Souza & Machado's evaluation framework needs the taxonomy this paper provides",
)

__all__ = [
    "claim_capability_taxonomies_existed",
    "claim_capability_taxonomies_indistinguishable",
    "claim_react_reflexion_paradigms",
    "claim_trajectory_studies_summary",
    "claim_trajectory_studies_blackbox_limit",
    "claim_trajectory_model_confound",
    "claim_swe_effi_token_snowball",
    "claim_individual_system_descriptions",
    "claim_individual_system_unmapped_space",
    "claim_configuration_artifacts_orthogonal",
    "claim_swebench_central",
    "claim_taxonomy_enables_controlled_experiments",
    "claim_souza_machado_call",
]
