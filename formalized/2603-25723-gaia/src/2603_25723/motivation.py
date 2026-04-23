"""Introduction and Motivation: Natural-Language Agent Harnesses"""

from gaia.lang import (
    claim, setting, question,
    support, deduction,
)

# --- Settings ---

harness_definition = setting(
    "An agent harness is the control stack that structures multi-step reasoning, "
    "tool use, memory, delegation, and stopping rules across multiple model calls, "
    "beyond any single model call.",
    title="Agent harness definition",
)

context_engineering_definition = setting(
    "Context engineering is the practice of deciding what instructions, evidence, "
    "intermediate artifacts, and state should be made available at each step of a "
    "long agent run.",
    title="Context engineering definition",
)

# --- Core problem claims ---

harness_logic_buried = claim(
    "In most agent systems, the effective harness is scattered across controller code, "
    "hidden framework defaults, tool adapters, verifier scripts, and runtime-specific "
    "assumptions. Harness logic is rarely exposed as a coherent, portable artifact.",
    title="Harness logic is buried and non-portable",
)

harness_affects_outcomes = claim(
    "Differences in scaffolds and harnesses can dominate task outcomes even under fixed "
    "base models. Research on reason-act loops, retrieval-augmented generation, and "
    "explicit self-feedback shows that externalized control patterns are decisive for "
    "agent performance.",
    title="Harness design decisively affects agent outcomes",
)

harness_hard_to_compare = claim(
    "Because harness logic is scattered across controller code and framework defaults, "
    "two agent systems that nominally differ by one design choice often differ "
    "simultaneously in prompts, tool mediation, artifact conventions, verification "
    "gates, and state semantics. This collapses evaluation into controller-bundle "
    "comparisons rather than module-level evidence.",
    title="Harnesses are hard to compare and ablate",
)

# --- Research questions ---

q_behavioral_effect = question(
    "RQ1: Under fixed budgets, how do a shared runtime charter and benchmark-specific "
    "harness logic change agent behavior and task outcomes?",
    title="RQ1: Behavioral effect",
)

q_composability = question(
    "RQ2: Once harness patterns are made explicit, can modules be composed and ablated "
    "at the pattern level?",
    title="RQ2: Composability",
)

q_migration = question(
    "RQ3: What differences remain between native code harnesses and reconstructed "
    "natural-language harnesses under a shared runtime?",
    title="RQ3: Code-to-text migration",
)

# --- Motivating observations ---

nlah_natural_language_feasibility = claim(
    "Natural-language artifacts such as AGENTS.md and skill bundles show that practical "
    "systems can package repository-local conventions and reusable procedures in portable "
    "text. They establish feasibility for reusable control knowledge, but do not make "
    "harness-wide contracts, role boundaries, state semantics, failure handling, and "
    "runtime-facing adapters first-class and jointly executable.",
    title="Natural-language carriers feasible but not harness-complete",
)

strat_buried_causes_comparison_collapse = support(
    [harness_logic_buried, harness_affects_outcomes],
    harness_hard_to_compare,
    reason=(
        "Because @harness_affects_outcomes (harness design is decisive), and "
        "@harness_logic_buried (harness logic is scattered, not exposed as a coherent artifact), "
        "it is impossible to isolate which component drives a difference: any two systems that "
        "nominally differ by one harness choice actually differ across prompts, tool adapters, "
        "verification, and state semantics simultaneously — collapsing comparison to "
        "bundle-level comparisons."
    ),
    prior=0.92,
)

strat_nlah_over_prior_work = support(
    [nlah_natural_language_feasibility, harness_logic_buried],
    harness_hard_to_compare,
    reason=(
        "@nlah_natural_language_feasibility establishes that prior work (AGENTS.md, skill bundles) "
        "shows feasibility of natural-language carriers but does not make harness-wide contracts, "
        "roles, state semantics, and failure handling jointly executable. Since @harness_logic_buried "
        "persists despite these prior approaches, the comparison problem remains: harnesses "
        "are still bundled across code and framework defaults, not exposed as coherent objects."
    ),
    prior=0.85,
)
