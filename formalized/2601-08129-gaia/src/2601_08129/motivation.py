"""Motivation: explicit-orchestration overhead in current MAS-LLM frameworks
versus implicit, stigmergic coordination through shared artifact state with
pressure gradients and temporal decay.

Section 1 (Introduction) of Rodriguez 2026
[@Rodriguez2026PressureField] -- the paper formalizes pressure-field
coordination as a role-free, stigmergic alternative to organizational
MAS paradigms and proves convergence under pressure-alignment conditions.
"""

from gaia.lang import claim, question, setting

# ---------------------------------------------------------------------------
# Operational setup: what an LLM-based MAS is
# ---------------------------------------------------------------------------

setup_mas_llm_regime = setting(
    "**LLM-based multi-agent system (MAS) regime.** A multi-agent system "
    "built on Large Language Models (LLMs) addresses complex task "
    "automation by composing multiple LLM-backed agents that collaborate "
    "to produce a final artifact (a schedule, a code patch, a plan, "
    "etc.) for an input problem. Concrete instantiations include "
    "AutoGen [@AutoGen] (conversation-based message passing among "
    "customizable agents), MetaGPT [@MetaGPT] (Standardized Operating "
    "Procedures encoded into agent workflows with specialized roles "
    "such as architect / engineer / QA in an assembly line), CAMEL "
    "[@CAMEL] (role-playing between an AI assistant and an AI user via "
    "inception prompting), and CrewAI [@CrewAI] (agents with roles, "
    "goals, and backstories collaborating on tasks).",
    title="Setup: LLM-based MAS regime (multiple LLM agents collaborate on a shared task)",
)

setup_artifact_refinement_task = setting(
    "**Artifact refinement task class.** The work targets *artifact "
    "refinement* tasks: starting from an initial artifact (e.g., a "
    "partial meeting schedule), agents iteratively propose patches "
    "until the artifact satisfies measurable quality constraints "
    "(no attendee double-bookings, all meetings placed, balanced room "
    "utilization). The space of valid improvements is open-ended -- "
    "no finite action language enumerates all valid patches in "
    "advance.",
    title="Setup: artifact-refinement task class (iterative patch-based improvement of a shared artifact)",
)

# ---------------------------------------------------------------------------
# Diagnosis: what is wrong with the dominant explicit-orchestration paradigm
# ---------------------------------------------------------------------------

claim_explicit_orchestration_paradigm = claim(
    "**Dominant paradigm: explicit orchestration borrowed from human "
    "organizational structures.** Current MAS-LLM frameworks "
    "[@AutoGen; @MetaGPT; @CAMEL; @CrewAI] treat agents as "
    "organizational units: planners decompose tasks, managers delegate "
    "subtasks to workers, and hierarchical control flow governs agent "
    "interactions. The shared design pattern is *explicit* "
    "orchestration through message passing, role assignment, and "
    "hierarchical task decomposition.",
    title="Diagnosis: dominant MAS-LLM paradigm uses explicit orchestration (planner / manager / worker, message passing, hierarchical control)",
)

claim_orchestration_overhead_scales_poorly = claim(
    "**Coordination overhead scales poorly with agent count and task "
    "complexity.** Explicit orchestration introduces three failure "
    "modes that worsen with scale: (i) *central coordinators become "
    "bottlenecks* (planner / manager LLM calls serialize the "
    "pipeline); (ii) *message-passing overhead grows with agent "
    "count* (pairwise negotiation costs $O(n^2)$ messages, tree-"
    "structured delegation costs $O(n \\log n)$ but adds tree-depth "
    "latency); (iii) *failures in manager agents cascade to all "
    "dependents*. The cost of coordination ends up consuming budget "
    "that would otherwise go to problem-solving.",
    title="Diagnosis: explicit-orchestration coordination overhead scales poorly with agent count / task complexity",
)

# ---------------------------------------------------------------------------
# Central question
# ---------------------------------------------------------------------------

q_central = question(
    "Can multi-agent systems coordinate **without** explicit "
    "orchestration -- without coordinators, planners, or message "
    "passing -- and still match or outperform explicit-coordination "
    "baselines on artifact-refinement tasks? More precisely, can "
    "natural-system-style coordination through environment "
    "modification (stigmergy) be made practical for LLM agents on "
    "open-ended artifact refinement?",
    title="Central question: can MAS coordinate without explicit orchestration and still outperform explicit baselines?",
)

# ---------------------------------------------------------------------------
# Central proposal: pressure-field coordination
# ---------------------------------------------------------------------------

claim_pressure_field_proposal = claim(
    "**Proposal: pressure-field coordination as a stigmergic, role-"
    "free alternative.** Agents operate locally on a shared artifact, "
    "guided only by *pressure gradients* derived from measurable "
    "quality signals (gaps, overlaps, utilization variance, "
    "unscheduled count). They observe local quality signals, take "
    "locally-greedy patch actions, and global coordination emerges "
    "from shared artifact state. *Temporal decay* continuously erodes "
    "fitness so no region becomes permanently 'solved', preventing "
    "premature convergence to local minima. The system is formalized "
    "as optimization over a pressure landscape with $O(1)$ inter-"
    "agent coordination overhead, in contrast to $O(n \\log n)$ for "
    "Generalized Partial Global Planning (GPGP) [@GPGP] and $O(n^2)$ "
    "for pairwise message-passing baselines.",
    title="Proposal: pressure-field coordination -- shared artifact + local pressure gradients + temporal decay, O(1) coordination overhead",
)

claim_foundation_models_enable = claim(
    "**Foundation Models (FMs) enable stigmergic coordination.** "
    "Traditional stigmergic agents (e.g., Ant Colony Optimization, "
    "ACO [@AntSystem; @ACO]) require domain-specific action "
    "representations -- enumerated moves, parameterized operators, "
    "or learned policies. FMs' broad pretraining provides a "
    "'universal actor' capability: a single FM can propose patches "
    "across heterogeneous artifact types (schedules, code, "
    "configurations) through the same interface (observe local "
    "context, receive pressure feedback, generate patch). This is "
    "what makes pressure-field coordination practical for open-ended "
    "artifact refinement, where the space of valid improvements is "
    "unbounded and cannot be enumerated.",
    title="Proposal: FMs enable stigmergic MAS coordination (universal-actor patch proposal without domain-specific action enumeration)",
)

# ---------------------------------------------------------------------------
# Headline empirical claims (reported in abstract / introduction)
# ---------------------------------------------------------------------------

claim_headline_solve_rates = claim(
    "**Headline empirical claim (aggregate solve rates, 1350 trials, "
    "270 per strategy).** Across 1350 total trials of meeting room "
    "scheduling spanning three difficulty levels (easy / medium / "
    "hard) and three agent counts (1, 2, 4):\n\n"
    "| Strategy | Solved/N | Rate | 95% Wilson CI |\n"
    "|---|---|---|---|\n"
    "| Pressure-field (ours) | 131/270 | **48.5%** | 42.6%-54.5% |\n"
    "| Conversation [@AutoGen] | 30/270 | 11.1% | 7.9%-15.4% |\n"
    "| Hierarchical | 4/270 | 1.5% | 0.6%-3.7% |\n"
    "| Sequential | 1/270 | 0.4% | 0.1%-2.1% |\n"
    "| Random | 1/270 | 0.4% | 0.1%-2.1% |\n\n"
    "Pressure-field beats the conversation-based baseline by **about "
    "$4\\times$** and the hierarchical-control baseline by **about "
    "$30\\times$**. Chi-square test across all five strategies yields "
    "$\\chi^2 > 200$ with $p < 0.001$; all pairwise comparisons are "
    "significant at $p < 0.001$.",
    title="Headline: 48.5% (pressure-field) vs 11.1% (conversation, 4x) vs 1.5% (hierarchical, 30x) aggregate solve rate; all p < 0.001",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 3",
        "caption": "Table 3: Aggregate solve rates across 1350 trials (270 per strategy) with Wilson 95% CIs.",
    },
)

claim_headline_easy_problems = claim(
    "**Headline empirical claim (easy problems).** On the *easy* "
    "difficulty tier (3 rooms, 20 meetings, 70% pre-scheduled, 90 "
    "trials per strategy), pressure-field achieves **86.7%** solve "
    "rate (78/90), compared with **33.3%** (30/90) for the next-best "
    "baseline (conversation), 4.4% for hierarchical, and 1.1% for "
    "sequential / random. The gap of 53.4 percentage points exceeds "
    "Cohen's 'large effect' threshold ($h > 0.8$) for every "
    "pairwise comparison on easy problems.",
    title="Headline: easy problems -- pressure-field 86.7% vs conversation 33.3% (next-best) vs hierarchical 4.4%",
)

claim_headline_only_strategy_scales = claim(
    "**Headline empirical claim (only strategy that scales to "
    "harder problems).** On medium (5 rooms, 40 meetings, 50% pre-"
    "scheduled) and hard (5 rooms, 60 meetings, 30% pre-scheduled) "
    "problems, **pressure-field is the only strategy with a non-zero "
    "solve rate**: 43.3% (39/90) on medium and 15.6% (14/90) on "
    "hard, while conversation, hierarchical, sequential, and random "
    "all score 0%.",
    title="Headline: pressure-field is the only strategy with non-zero solve rates on medium (43.3%) and hard (15.6%) problems",
)

claim_headline_decay_ablation = claim(
    "**Headline ablation claim (temporal decay, easy problems, 30 "
    "trials each).** Removing temporal decay reduces the easy-"
    "problem solve rate from **96.7% (29/30)** with decay to **86.7% "
    "(26/30)** without decay -- a 10 percentage-point drop, "
    "directionally consistent with the theoretical Basin Separation "
    "result (Theorem 5.3) that decay is required to escape "
    "suboptimal stable basins. Fisher's exact test yields $p = 0.35$ "
    "at $n = 30$: the directional effect does not reach statistical "
    "significance at the chosen sample size, partly due to a ceiling "
    "effect from the high baseline (96.7%).",
    title="Headline ablation: decay enabled 96.7% vs disabled 86.7% on easy (delta = -10 pp; Fisher's p = 0.35, not significant at n=30)",
)

claim_headline_convergence_theorem = claim(
    "**Headline theoretical claim (convergence).** Under "
    "$\\epsilon$-bounded coupling between regions and a minimum local "
    "pressure reduction $\\delta_{\\min} > (n-1)\\epsilon$ (where $n$ "
    "is the number of regions), the pressure-field system reaches a "
    "stable basin within $T \\le P_0 / (\\delta_{\\min} - "
    "(n-1)\\epsilon)$ ticks from any initial state with pressure "
    "$P_0$ (Theorem 5.1). With $K$ patches validated in parallel per "
    "tick on disjoint regions, this improves to $T \\le P_0 / "
    "(K \\cdot (\\delta_{\\min} - (n-1)\\epsilon))$ (Theorem 5.5).",
    title="Headline theory: convergence in T <= P_0 / (delta_min - (n-1)*eps) ticks under epsilon-bounded coupling",
)

# ---------------------------------------------------------------------------
# Explicit thesis claims about the FM-MAS synthesis
# ---------------------------------------------------------------------------

claim_fm_mas_mutually_enabling = claim(
    "**Argument: FMs and MAS coordination are mutually enabling, "
    "not merely additive.** The bidirectional synthesis: (i) FMs "
    "solve a fundamental MAS problem -- traditional MAS coordination "
    "requires explicit action-space enumeration, but FMs' broad "
    "pretraining provides implicit coverage of improvement strategies "
    "without domain-specific action representations; (ii) MAS "
    "coordination solves a fundamental FM problem -- pressure "
    "gradients provide an *objective* criterion for combining "
    "multiple FM outputs (accept patches that reduce pressure), "
    "replacing ad-hoc voting / ranking / dialogue with principled "
    "quality-based filtering. This bidirectional synthesis is the "
    "paper's central explanatory thesis for why pressure-field beats "
    "conversation-based alternatives.",
    title="Argument: FMs solve MAS's action-enumeration problem; MAS solves FM's output-combination problem (mutually enabling synthesis)",
)

# ---------------------------------------------------------------------------
# Stated contributions
# ---------------------------------------------------------------------------

claim_four_contributions = claim(
    "**Stated contributions (Section 1).** Four contributions: "
    "(C1) **Method** -- formalize pressure-field coordination as a "
    "role-free, stigmergic alternative to organizational MAS "
    "paradigms with $O(1)$ coordination overhead through shared "
    "artifact state; "
    "(C2) **Mechanism** -- introduce *temporal decay* as a mechanism "
    "for preventing premature convergence (10 pp ablation effect on "
    "easy problems, 96.7% vs 86.7%); "
    "(C3) **Theory** -- prove convergence guarantees under pressure-"
    "alignment conditions; "
    "(C4) **Empirical** -- across 1350 total trials (270 per "
    "strategy), pressure-field outperforms all baselines by an order "
    "of magnitude or more, with all pairwise comparisons highly "
    "significant ($p < 0.001$).",
    title="Four stated contributions (method / mechanism / theory / empirical)",
)

__all__ = [
    "setup_mas_llm_regime",
    "setup_artifact_refinement_task",
    "claim_explicit_orchestration_paradigm",
    "claim_orchestration_overhead_scales_poorly",
    "q_central",
    "claim_pressure_field_proposal",
    "claim_foundation_models_enable",
    "claim_headline_solve_rates",
    "claim_headline_easy_problems",
    "claim_headline_only_strategy_scales",
    "claim_headline_decay_ablation",
    "claim_headline_convergence_theorem",
    "claim_fm_mas_mutually_enabling",
    "claim_four_contributions",
]
