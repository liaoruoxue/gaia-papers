"""Introduction and Motivation: The Design Space of Agentic Coding Tools"""

from gaia.lang import claim, setting, question

# ── Research context ──────────────────────────────────────────────────────────

evolution_of_coding_tools = setting(
    "AI-assisted software development has evolved from autocomplete-style tools "
    "(e.g., GitHub Copilot), through IDE-integrated assistants (e.g., Cursor), "
    "to fully agentic systems that autonomously plan multi-step modifications, "
    "execute shell commands, read and write files, and iterate on their own outputs.",
    title="Evolution of AI coding tools",
)

claude_code_description = setting(
    "Claude Code is an agentic coding tool released by Anthropic that can run "
    "shell commands, edit files, and call external services on behalf of the user. "
    "Its official documentation describes an 'agentic loop' that plans and executes "
    "actions toward accomplishing a goal and can call tools, evaluate results, and "
    "continue until the task is done.",
    title="Claude Code definition",
)

source_code_analysis_method = setting(
    "This study analyzes the publicly available TypeScript source code of Claude Code "
    "(version 2.1.88, obtained from a publicly available npm package extraction), "
    "comprising approximately 1,884 files totaling roughly 512K lines of TypeScript. "
    "Analysis is supplemented by official Anthropic documentation and selected community "
    "analysis. Findings are grounded at three evidence tiers: Tier A (product-documented), "
    "Tier B (code-verified), and Tier C (reconstructed).",
    title="Source-level analysis methodology",
)

# ── Core claims from introduction ──────────────────────────────────────────────

no_architectural_descriptions_published = claim(
    "Anthropic publishes user-facing documentation for Claude Code but not detailed "
    "architectural descriptions. Source code analysis is therefore the primary method "
    "for describing architectural design decisions.",
    title="Lack of published architecture docs",
)

qualitatively_new_workflows = claim(
    "Anthropic's internal survey of 132 engineers and researchers (Huang et al., 2025) "
    "reports that approximately 27% of Claude Code-assisted tasks were work that would "
    "not have been attempted without the tool, suggesting the architecture enables "
    "qualitatively new workflows rather than merely accelerating existing ones.",
    title="Claude Code enables qualitatively new workflows",
)

agentic_shift_introduces_new_requirements = claim(
    "The shift from suggestion-based to autonomous-action coding tools introduces "
    "architectural requirements with no counterpart in completion-based tools: "
    "requirements spanning safety, context management, extensibility, and delegation "
    "that every coding agent must navigate.",
    title="Agentic tools have novel architectural requirements",
)

# ── Research question ──────────────────────────────────────────────────────────

q_design_space = question(
    "How does Claude Code answer the recurring design questions that every agentic "
    "coding system must navigate (safety posture, context management, extensibility, "
    "delegation), and what do these answers reveal about the broader design space "
    "of AI agent systems?",
    title="Research question: Claude Code design space",
)
