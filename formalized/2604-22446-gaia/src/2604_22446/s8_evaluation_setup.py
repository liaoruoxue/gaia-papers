"""Section 3.1: Experimental Setup -- PRDBench + agent setup + DEV mode +
metrics.

Source: Yu et al. 2026 [@Yu2026OMC], Section 3.1 (page 13).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Benchmark and task class
# ---------------------------------------------------------------------------

setup_prdbench_benchmark = setting(
    "**PRDBench benchmark [@PRDBench].** A recently proposed "
    "benchmark for assessing LLM-based code agents in realistic "
    "software development scenarios: 50 project-level tasks "
    "spanning 20+ domains. Each task is defined by a structured "
    "Product Requirement Document (PRD) along with comprehensive "
    "evaluation criteria, including high-level requirements, "
    "auxiliary data, detailed test plans, and executable "
    "evaluation scripts -- enabling end-to-end assessment of an "
    "agent's ability to interpret requirements, decompose tasks, "
    "implement solutions, and satisfy functional constraints. "
    "Unlike isolated code-generation benchmarks, PRDBench operates "
    "at the *project* level, requiring long-horizon reasoning, "
    "hierarchical decomposition, and coordinated multi-agent "
    "execution.",
    title="Setup: PRDBench [@PRDBench] = 50 project-level software tasks across 20+ domains with executable evaluation",
)

setup_each_prdbench_is_wild_dynamic = setting(
    "**Each PRDBench task is a Wild Dynamic Agentic Workflow.** "
    "Neither the team (composition, runtimes, capabilities) nor "
    "the workflow (task decomposition, execution ordering) is "
    "known before execution -- making PRDBench particularly "
    "suitable for evaluating OMC since it stress-tests precisely "
    "the wild-dynamic scenario OMC is designed for.",
    title="Setup: each PRDBench task is a wild dynamic agentic workflow (matches OMC's design target)",
)

# ---------------------------------------------------------------------------
# Agent setup
# ---------------------------------------------------------------------------

setup_omc_agent_setup = setting(
    "**OMC agent setup for the PRDBench evaluation.** In addition "
    "to the founding agent (a LangGraph-based agent using Gemini "
    "2.1 Flash Lite Preview), the HR recruited three specialised "
    "employees from the Talent Market at the outset of the first "
    "PRD project: (1) a **Software Engineer** (Claude Code-based, "
    "with the superpowers plugin [@Superpowers]); (2) a "
    "**Software Architect** (Claude Code-based, from "
    "agency-agents [@AgencyAgents]); (3) a **Code Reviewer** "
    "(also from agency-agents). The three specialists span "
    "different Talent sourcing types, demonstrating the "
    "Container-Talent abstraction in deployment.",
    title="Setup: OMC team = founding LangGraph agent + 3 Talent Market specialists (SE / SA / CR) for PRDBench",
)

setup_dev_mode = setting(
    "**DEV mode evaluation protocol.** Each system receives the "
    "PRD as a one-shot input and must complete the task without "
    "iterative feedback or external intervention; final outputs "
    "are evaluated by automated scripts. Single-attempt zero-shot, "
    "matching the official PRDBench DEV mode setting and ensuring "
    "all baselines are evaluated under identical conditions.",
    title="Setup: DEV mode -- one-shot PRD input, no iterative feedback, automated script evaluation (single-attempt zero-shot)",
)

# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

setup_success_rate_metric = setting(
    "**Primary metric: Success Rate.** Percentage of tasks "
    "successfully completed under DEV mode evaluation scripts. "
    "Defined identically to PRDBench's reported metric so OMC "
    "results are directly comparable to PRDBench's baseline "
    "panel.",
    title="Setup: primary metric = Success Rate (% tasks passing DEV-mode automated scripts)",
)

setup_cost_overhead_metric = setting(
    "**Secondary metric: Cost Overhead.** Token usage / API cost "
    "for the entire agent system under zero-shot conditions. "
    "Reported only for OMC: PRDBench did not publish baseline "
    "costs, so direct cost-efficiency comparison is impossible -- "
    "the OMC cost numbers are reported as absolute values, not as "
    "relative comparisons.",
    title="Setup: secondary metric = Cost Overhead (OMC absolute only; baseline costs unreported in PRDBench)",
)

# ---------------------------------------------------------------------------
# Baseline panel
# ---------------------------------------------------------------------------

setup_baseline_panel = setting(
    "**Baseline panel (Section 3.2 / Table 2).** Twelve baselines "
    "spanning two categories:\n\n"
    "(B1) **Minimal** (8 baselines, single LLM with minimal "
    "scaffolding) -- GPT-5.2, Claude-4.5, Gemini-3-Pro, "
    "Qwen3-Coder, Kimi-K2, DeepSeek-V3.2, GLM-4.7, Minimax-M2.\n\n"
    "(B2) **Commercial** (4 baselines, production agent stacks) -- "
    "CodeX [@Codex], Claude Code [@ClaudeCode], Gemini CLI, Qwen "
    "Code.\n\n"
    "All baselines evaluated under identical DEV-mode conditions; "
    "OMC is the sole **Multi-agent** entry, using Claude Code "
    "Sonnet 4.6 + Gemini 3.1 Flash Lite Preview.",
    title="Setup: 12-baseline panel (8 Minimal LLMs + 4 Commercial agents) under identical DEV-mode conditions",
)

# ---------------------------------------------------------------------------
# Cross-domain case studies setup
# ---------------------------------------------------------------------------

setup_four_case_studies = setting(
    "**Four cross-domain case studies (Section 3.3).** Beyond "
    "PRDBench, four single-prompt case studies test cross-domain "
    "generality:\n\n"
    "(C1) **Content generation** (Section 3.3.1) -- weekly trend "
    "summary of hot AI Agent GitHub repos, autonomously written "
    "and emailed; recruits Researcher (GPT-4o) + Writer (Claude "
    "Sonnet 4); ~$4.49 total cost.\n\n"
    "(C2) **Game development** (Section 3.3.2) -- street-fighting "
    "web game with human-in-the-loop iteration; Game Developer "
    "(Claude Sonnet 4) + Art Designer (Gemini 2.5 + NanoBanana); "
    "evaluator-rejection triggers re-exploration that creates a "
    "new sprite-slicing skill.\n\n"
    "(C3) **Audiobook development** (Section 3.3.3) -- "
    "illustrated audiobook of Peaky Blinders with animal "
    "characters; Novel Writer + AV Producer (Gemini 3.1 Pro) "
    "across text + audio + visual; ~$1.57 / 1.56M tokens for 16 "
    "scenes + 16 voice-overs + music + 2 videos.\n\n"
    "(C4) **Automated research survey** (Section 3.3.4) -- "
    "survey on world models for embodied AI (2021-2026); 3 "
    "specialists; <1 hr; $16.26 / 15.9M tokens; 17 documents + "
    "70-node mind map + 3 novel research ideas (HiTeWM, PhysWM, "
    "MAWM).",
    title="Setup: four cross-domain case studies (content / game / audiobook / research survey) -- single-prompt, multi-modal",
)

__all__ = [
    "setup_prdbench_benchmark",
    "setup_each_prdbench_is_wild_dynamic",
    "setup_omc_agent_setup",
    "setup_dev_mode",
    "setup_success_rate_metric",
    "setup_cost_overhead_metric",
    "setup_baseline_panel",
    "setup_four_case_studies",
]
