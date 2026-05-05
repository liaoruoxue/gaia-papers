"""Motivation: Why a source-code-level taxonomy of coding agent scaffolds?

Section 1 (Introduction) of Rombaut 2026 [@Rombaut2026]. Motivates the
research gap: LLM-based coding agents (Aider, SWE-agent, OpenHands,
etc.) localize bugs, generate patches, and run tests with diminishing
human oversight, but the *scaffold code* surrounding the LLM (control
loop, tool definitions, state management, context strategy) remains
poorly understood. Existing capability-based surveys cannot distinguish
architecturally distinct systems, and trajectory studies treat agents
as black boxes -- observing what they do without examining why.

The paper proposes a source-code-level architectural taxonomy of 13
open-source coding agent scaffolds at pinned commit hashes, organized
into 3 layers (control architecture, tool & environment interface,
resource management) and 12 dimensions, with all claims grounded in
file paths and line numbers.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Background settings (definitions that frame the study)
# ---------------------------------------------------------------------------

setup_coding_agent = setting(
    "**Coding agent (working definition).** A coding agent is a system "
    "built on a Large Language Model (LLM) augmented with code-editing "
    "capabilities -- it can navigate unfamiliar repositories, localize "
    "bugs, generate patches, and run test suites with diminishing human "
    "oversight. Examples include Aider [@Aider], SWE-agent [@SWEAgent], "
    "and OpenHands [@OpenHands]. The most capable systems resolve over "
    "half of real-world GitHub issues on SWE-bench Verified "
    "[@Jimenez2024SWEbench]. This paper analyzes coding agents (not "
    "general-purpose task automation) at the *source-code* level.",
    title="Setup: coding agent = LLM + code-editing scaffold",
)

setup_scaffold = setting(
    "**Scaffold (working definition).** The scaffold is the code that "
    "surrounds the language model: the control loop (how LLM calls and "
    "tool dispatches are sequenced), tool definitions (what callable "
    "functions the LLM sees), state management (how history is "
    "represented), and context strategy (how the prompt is assembled "
    "and compacted). The scaffold determines how the agent behaves, "
    "what mistakes it makes, and where it spends its token budget "
    "[@Bui2026]. It is distinct from the LLM itself and from "
    "developer-facing configuration (instruction files, slash commands).",
    title="Setup: scaffold = the code surrounding the LLM",
)

setup_pinned_commit_methodology = setting(
    "**Pinned-commit source-code analysis.** Each agent's scaffolding "
    "code (control loop, tool definitions, state management) must be "
    "available as readable source code in a public repository, pinned "
    "to a specific commit. This is the empirical substrate on which "
    "the taxonomy is built: every taxonomic claim is grounded in a "
    "file path and line number from a cloned repository at a pinned "
    "commit hash (Appendix B), making each claim independently "
    "verifiable. Active development during the analysis period "
    "(Cline, Aider, OpenHands, Gemini CLI) made unpinned analysis "
    "unreproducible.",
    title="Setup: pinned-commit hashes anchor every taxonomic claim",
)

# ---------------------------------------------------------------------------
# Open research question
# ---------------------------------------------------------------------------

q_central = question(
    "What architectural patterns characterize the scaffold code of "
    "production open-source coding agents, and how can the design "
    "space be systematically mapped at the source-code level?",
    title="Central question: architectural patterns of coding agent scaffolds",
)

# ---------------------------------------------------------------------------
# Problem-framing claims (the gap this paper fills)
# ---------------------------------------------------------------------------

claim_existing_surveys_inadequate = claim(
    "**Existing surveys are inadequate for distinguishing scaffolds.** "
    "Existing LLM-agent surveys [@Masterman2024; @Nowaczyk2025] "
    "organize systems by abstract capabilities (tool use, memory, "
    "planning, reflection). Under these schemes, every coding agent "
    "in this study qualifies as 'tool-using, memory-augmented, "
    "planning'. Yet a coding agent that uses Monte Carlo Tree Search "
    "to explore candidate patches and one that uses a simple while "
    "loop with test-driven retries are *indistinguishable* under "
    "capability-based classification, despite fundamental differences "
    "in control flow, state management, and resource consumption.",
    title="Gap 1: capability-based surveys cannot distinguish architecturally distinct agents",
)

claim_trajectory_studies_blackbox = claim(
    "**Trajectory studies treat agents as black boxes.** Empirical "
    "work characterizes coding agent runtime behavior through "
    "trajectory analysis [@Ceka2025; @Majgaonkar2026; @Bouzenia2025], "
    "revealing that successful agents localize bugs faster, test "
    "earlier, and produce shorter action sequences. However, these "
    "studies *observe what agents do but do not examine the scaffold "
    "code that determines why*. Worse, prior trajectory studies used "
    "different LLMs for different agents [@Majgaonkar2026; "
    "@Bouzenia2025] -- e.g. comparing Claude 3.5 Sonnet OpenHands "
    "trajectories against DeepSeek-V3 Prometheus trajectories -- "
    "making it impossible to isolate scaffold effects from model "
    "effects.",
    title="Gap 2: trajectory studies observe what but not why; confound scaffold with model",
)

claim_no_comparative_source_code_study = claim(
    "**No prior comparative source-code-level study exists.** "
    "Detailed architectural descriptions exist for individual systems "
    "(SWE-agent's agent-computer interface [@SWEAgent], Aider's "
    "PageRank repo map [@Aider], a four-layer terminal agent design "
    "[@Bui2026]), but to the best of the current literature search "
    "no study has systematically compared the scaffolding "
    "architectures of production coding agents at the source-code "
    "level. Practitioners building new agents must read individual "
    "codebases or blog posts to assemble a comparative reference.",
    title="Gap 3: no comparative source-code-level taxonomy of coding agent scaffolds",
)

# ---------------------------------------------------------------------------
# Headline contributions (previewed in introduction; details in s4-s6)
# ---------------------------------------------------------------------------

claim_contribution_taxonomy = claim(
    "**Contribution 1: source-code-level architectural taxonomy.** "
    "A taxonomy derived from source-code analysis of **13 "
    "open-source coding agents** at pinned commit hashes, organized "
    "into **3 layers (control architecture, tool & environment "
    "interface, resource management) and 12 dimensions**. To the "
    "best of the current literature search, this is the first "
    "comparative architectural study of coding agents at the "
    "implementation level [@Rombaut2026].",
    title="Contribution 1: 13-agent / 3-layer / 12-dimension source-code taxonomy",
)

claim_contribution_loop_primitive_thesis = claim(
    "**Contribution 2: scaffolds are compositions of loop primitives "
    "along continuous spectra.** The empirical finding that scaffold "
    "architectures are better characterized as compositions of five "
    "loop primitives (ReAct, generate-test-repair, plan-execute, "
    "multi-attempt retry, tree search) along continuous spectra than "
    "as instances of discrete architectural types. **11 of the 13 "
    "agents layer multiple primitives** rather than relying on a "
    "single control structure; pure single-loop agents (Agentless, "
    "mini-swe-agent) are deliberately minimalist exceptions.",
    title="Contribution 2: 11/13 agents compose multiple loop primitives",
)

claim_contribution_evidence_base = claim(
    "**Contribution 3: a reusable evidence base pinned to commits.** "
    "All 296 extracted taxonomic claims are grounded in specific "
    "file paths and line numbers pinned to commit hashes "
    "(Appendix B), providing a reusable reference for researchers "
    "studying agent behavior and practitioners designing new "
    "scaffolds. A post-hoc verification pass confirmed 267 claims, "
    "corrected 19 (primarily line-number offsets), and accepted 10 "
    "as minor simplifications.",
    title="Contribution 3: 296 commit-pinned, file/line-cited architectural claims",
)

# ---------------------------------------------------------------------------
# Headline empirical findings (previewed in introduction; details in s4-s7)
# ---------------------------------------------------------------------------

claim_finding_spectra_not_categories = claim(
    "**Headline finding 1.** Scaffold architectures **resist discrete "
    "classification**: across all 12 dimensions, agents occupy "
    "positions along *continuous spectra* rather than falling into "
    "discrete categories. Control strategies range from fixed "
    "pipelines (Agentless) to full Monte Carlo Tree Search (Moatless "
    "Tools), tool counts range from 0 (Aider) to 37 action classes "
    "(Moatless Tools), and context compaction spans **seven distinct "
    "strategies**. Within each spectrum, agents occupy distinct "
    "positions reflecting genuine architectural tradeoffs.",
    title="Headline 1: agents lie on continuous spectra across all 12 dimensions",
)

claim_finding_loop_primitives_compose = claim(
    "**Headline finding 2.** Five loop primitives -- **ReAct, "
    "generate-test-repair, plan-execute, multi-attempt retry, and "
    "tree search** -- function as **composable building blocks** that "
    "agents layer in different combinations rather than as mutually "
    "exclusive types. **11 of the 13 agents compose multiple "
    "primitives** (e.g. AutoCodeRover nests ReAct inside each phase "
    "of a phased pipeline; Moatless Tools' ActionAgent can be driven "
    "by AgenticLoop or by SearchTree without changes to the agent "
    "code itself). This compositionality means the design space is "
    "*combinatorial rather than categorical*.",
    title="Headline 2: 5 loop primitives, composable; 11/13 agents compose multiple",
)

claim_finding_convergence_divergence = claim(
    "**Headline finding 3.** Dimensions exhibit a clear "
    "**convergence/divergence pattern**: dimensions converge where "
    "*external constraints dominate* the design (tool capability "
    "categories converge on read/search/edit/execute; edit format "
    "trends toward exact-string-replacement; execution isolation "
    "converges on Docker for benchmark agents) and diverge where "
    "*open design questions remain* (context compaction has 7 "
    "strategies, state management ranges from destructive overwrite "
    "to event sourcing, multi-model routing spans single-model to "
    "7-layer classifier chains). The pattern marks where the design "
    "space has stabilized vs where research investment is most needed.",
    title="Headline 3: convergence on externally-constrained dims, divergence on open questions",
)

claim_finding_methodological_contribution = claim(
    "**Headline finding 4 (methodological).** Every taxonomic claim "
    "is grounded in a **file path and line number** from a cloned "
    "repository at a pinned commit hash. This grounding makes each "
    "claim independently verifiable against the source code, enables "
    "the taxonomy to function as a *reusable reference* for future "
    "studies, and establishes a methodological standard for "
    "architecture-aware research on coding agents.",
    title="Headline 4 (methodological): all taxonomic claims grounded in file paths + line numbers",
)

# ---------------------------------------------------------------------------
# Baseline assumption that the empirical findings will challenge
# ---------------------------------------------------------------------------

claim_baseline_capability_taxonomy_sufficient = claim(
    "**Common prior assumption (to be tested).** A baseline view "
    "consistent with prior LLM-agent surveys [@Masterman2024; "
    "@Nowaczyk2025] holds that abstract capability categories "
    "(tool-using, memory-augmented, planning, reflective) are "
    "**sufficient to distinguish architecturally distinct coding "
    "agents** -- i.e. the agent design space can be carved into "
    "discrete categories along these axes, with each agent "
    "classifiable as belonging to one or a small number of them.",
    title="Baseline assumption: capability-category labels are sufficient to distinguish agents",
)

claim_baseline_react_is_dominant_architecture = claim(
    "**Common prior assumption (to be tested).** A baseline view "
    "consistent with the popularity of the ReAct paradigm "
    "[@Yao2023ReAct] would hold that production coding agents are "
    "essentially instances of a **single dominant control "
    "architecture** (such as ReAct), with the variation between "
    "agents being mostly cosmetic (different tool sets, different "
    "models) rather than fundamental architectural differences.",
    title="Baseline assumption: a single dominant control architecture (e.g. ReAct) suffices",
)

__all__ = [
    "setup_coding_agent",
    "setup_scaffold",
    "setup_pinned_commit_methodology",
    "q_central",
    "claim_existing_surveys_inadequate",
    "claim_trajectory_studies_blackbox",
    "claim_no_comparative_source_code_study",
    "claim_contribution_taxonomy",
    "claim_contribution_loop_primitive_thesis",
    "claim_contribution_evidence_base",
    "claim_finding_spectra_not_categories",
    "claim_finding_loop_primitives_compose",
    "claim_finding_convergence_divergence",
    "claim_finding_methodological_contribution",
    "claim_baseline_capability_taxonomy_sufficient",
    "claim_baseline_react_is_dominant_architecture",
]
