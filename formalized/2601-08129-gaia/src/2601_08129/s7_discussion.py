"""Section 7: Discussion -- why pressure-field dominates (3 factors),
why hierarchical collapses (rejection-loop failure), limitations,
when-to-choose guidance, FM-MAS reciprocity, and societal
implications. Section 8: Conclusion.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Sections 7-8.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 7.1 Three factors explaining pressure-field's dominance
# ---------------------------------------------------------------------------

claim_factor_1_coordination_overhead_harms = claim(
    "**Factor 1: Coordination overhead harms performance under "
    "fixed budgets.** Hierarchical systems spend computational "
    "budget on coordination rather than problem-solving. The "
    "manager-worker protocol requires multiple LLM calls per patch "
    "(planning, delegation, execution), while pressure-field "
    "requires only one LLM call per patch proposal. The overhead "
    "compounds: hierarchical attempts *fewer* patches per tick, "
    "reducing exploration.",
    title="Factor 1 explaining dominance: coordination overhead consumes budget that would otherwise go to patch attempts",
)

claim_factor_2_locality_makes_greedy_effective = claim(
    "**Factor 2: Local greedy decisions are effective for "
    "constraint satisfaction with locality.** Meeting room "
    "scheduling exhibits *locality*: fixing a conflict in one time "
    "block rarely creates conflicts in distant blocks. This "
    "matches pressure-field's locality assumption (formalized as "
    "$\\epsilon = 0$ separable pressure in Appendix B), making "
    "greedy local optimization effective. **Hierarchical "
    "coordination's global planning provides no benefit for "
    "locally-decomposable problems.**",
    title="Factor 2 explaining dominance: locality of meeting scheduling makes greedy local optimization effective; global planning offers no advantage",
)

claim_factor_3_parallel_validation_amplifies = claim(
    "**Factor 3: Parallel validation amplifies pressure-field's "
    "advantage.** Pressure-field validates patches for multiple "
    "regions simultaneously, applying the highest-scoring patch "
    "per region that reduces pressure. Hierarchical validates one "
    "patch at a time, requiring multiple ticks to explore "
    "alternatives. **On problems with many valid solutions, "
    "parallel exploration finds solutions faster** (consistent "
    "with the $K \\times$ speedup of Theorem 5.5).",
    title="Factor 3 explaining dominance: parallel validation amplifies the advantage (consistent with Theorem 5.5)",
)

# ---------------------------------------------------------------------------
# 7.2 Failure analysis: hierarchical's rejection loop
# ---------------------------------------------------------------------------

claim_hierarchical_rejection_loop = claim(
    "**Hierarchical fails through a self-reinforcing rejection "
    "loop.** Hierarchical always selects the *highest-pressure "
    "region*, but the highest-pressure regions are precisely the "
    "ones that are *difficult to improve*. When the LLM proposes a "
    "patch that fails validation (does not reduce pressure), the "
    "region remains highest-pressure and is selected again next "
    "tick. This creates a self-reinforcing cycle.",
    title="Failure mechanism: hierarchical's 'always pick highest-pressure region' policy creates a self-reinforcing rejection loop on difficult regions",
)

claim_hierarchical_rejection_statistics = claim(
    "**Hierarchical's rejection-loop statistics: 66.7% of runs "
    "applied zero patches, 98.7% rejection rate.** Across all 270 "
    "hierarchical trials, **180 / 270 = 66.7% applied zero patches "
    "across all 50 ticks** -- stuck targeting the same intractable "
    "region repeatedly. Of 13,460 proposed patches across all "
    "hierarchical trials, only 173 were accepted -- a **98.7% "
    "rejection rate**. Pressure-field's parallel exploration "
    "prevents this trap: even if one agent's patch is rejected, "
    "other agents make progress on different regions, so no "
    "single difficult region stalls the entire system.",
    title="Failure quantification: 66.7% hierarchical runs applied 0 patches (180/270); 98.7% rejection rate (13,287/13,460)",
)

claim_architectural_lesson = claim(
    "**Architectural lesson from the rejection loop.** "
    "Hierarchical's design embodies a reasonable intuition: focus "
    "intelligent effort on the worst problems. **But this creates "
    "a trap when combined with strict validation: the hardest "
    "problems resist improvement, causing repeated rejection, "
    "which blocks progress everywhere.** Pressure-field avoids this "
    "trap through distributed exploration -- progress happens "
    "where it can, not where a central planner dictates it must.",
    title="Architectural lesson: focusing on worst-region + strict validation creates a coordination dead-end; distributed exploration avoids it",
)

# ---------------------------------------------------------------------------
# 7.3 Limitations
# ---------------------------------------------------------------------------

claim_limitation_modest_hard_solve_rate = claim(
    "**Limitation: absolute solve rates are modest on hard "
    "problems.** Even pressure-field achieves only 15.6% on hard "
    "problems (5 rooms, 60 meetings, 30% pre-scheduled). Meeting-"
    "room scheduling with tight constraints remains challenging "
    "for small models (0.5b-3b parameters); larger models may "
    "achieve higher absolute solve rates.",
    title="Limitation: pressure-field's hard-problem solve rate (15.6%) is modest in absolute terms; small-model substrate is the bottleneck",
)

claim_limitation_domain_specificity = claim(
    "**Limitation: domain specificity.** Results on meeting-room "
    "scheduling may not generalize to domains lacking measurable "
    "pressure gradients or locality properties. Tasks requiring "
    "global planning or long-horizon reasoning may favor "
    "hierarchical approaches. The paper argues that **meeting "
    "scheduling is representative of a broader class of resource-"
    "allocation problems with soft constraints** -- cloud compute "
    "scheduling (VMs to hosts), logistics optimization, workforce "
    "rostering -- that share three properties: decomposable "
    "quality metrics, locality (fixing one allocation rarely "
    "breaks distant allocations), and multiple valid solutions.",
    title="Limitation: domain specificity (results may not generalize to non-local domains); but meeting scheduling is representative of resource-allocation problems with soft constraints",
)

claim_other_practical_limitations = claim(
    "**Additional practical limitations.** (i) Pressure functions "
    "must be hand-designed (not learned from data); (ii) decay "
    "rates $\\lambda_f, \\lambda_\\gamma$ and inhibition period "
    "$\\tau_{inh}$ require task-specific tuning; (iii) tasks "
    "requiring long-horizon global planning may not suit pressure-"
    "field; (iv) Goodhart's Law -- agents may game poorly-"
    "designed metrics; (v) parallel validation has resource cost "
    "$O(K \\cdot |A|)$ memory where $|A|$ is artifact size.",
    title="Limitation: hand-designed pressure / tuning required / Goodhart-gaming risk / parallel validation memory cost",
)

claim_limitation_trajectory_level_risks = claim(
    "**Limitation: validation cannot detect trajectory-level "
    "risks.** Validation filters individual hallucinations "
    "(patches that increase pressure or violate syntactic "
    "constraints are rejected before application), but cannot "
    "detect: (i) **coherence drift** (individual improvements that "
    "collectively shift the artifact toward an inconsistent state); "
    "(ii) **emergent gaming** (patches that exploit pressure-"
    "function weaknesses only over multiple steps); (iii) "
    "**dependency accumulation** (gradual hidden couplings that "
    "reduce future improvability). Mitigating these requires "
    "mechanisms beyond local validation: periodic global coherence "
    "checks, trajectory logging, and pressure functions that "
    "penalize coupling metrics.",
    title="Limitation: trajectory-level risks (coherence drift / emergent gaming / dependency accumulation) escape per-step validation",
)

claim_limitation_decay_miscalibration = claim(
    "**Limitation: decay miscalibration introduces distinct "
    "failure modes.** Two failure modes flank the optimal decay "
    "rate: (i) **Too-fast decay** -- fitness decays faster than "
    "agents can reinforce successful regions, producing perpetual "
    "oscillation (patch -> decay -> re-patch indefinitely); (ii) "
    "**Too-slow decay** -- fitness decays slower than the "
    "exploration timescale, trapping agents in suboptimal basins "
    "(consistent with the 10pp ablation effect). The optimal rate "
    "depends on problem characteristics; the experiments use "
    "fixed $\\lambda_f = 0.1$ (5s half-life), which may be "
    "suboptimal for some instances.",
    title="Limitation: decay miscalibration creates two failure modes (too fast = oscillation; too slow = trapped in suboptimal basin)",
)

# ---------------------------------------------------------------------------
# 7.4 When to choose each approach (decision rules)
# ---------------------------------------------------------------------------

claim_when_pressure_field = claim(
    "**When to choose pressure-field coordination.** Five "
    "indications: (i) **performance matters** (3-30x higher solve "
    "rates than alternatives); (ii) **simplicity is valued** (no "
    "coordinator agent; coordination emerges from shared state); "
    "(iii) **fault tolerance matters** (no single point of "
    "failure; agents can join / leave without protocol overhead); "
    "(iv) **pressure signals are available** (the domain provides "
    "measurable quality gradients); (v) **problems are locally "
    "decomposable** (local fixes improve global quality without "
    "cascading conflicts).",
    title="Guidance: when to prefer pressure-field (5 indications: performance / simplicity / fault tolerance / pressure signals / locality)",
)

claim_when_hierarchical = claim(
    "**When hierarchical coordination may be preferred.** Three "
    "indications: (i) **explicit control is required** "
    "(deterministic task assignment for regulatory or safety "
    "reasons); (ii) **interpretability is critical** (clear audit "
    "trails); (iii) **global planning is essential** (tasks with "
    "strong non-local dependencies may benefit from centralized "
    "reasoning).",
    title="Guidance: when to prefer hierarchical (explicit control required / interpretability critical / global planning essential)",
)

# ---------------------------------------------------------------------------
# 7.7 FM-MAS reciprocity: bidirectional problem-solving
# ---------------------------------------------------------------------------

claim_fm_solves_action_enumeration = claim(
    "**FMs solve a fundamental MAS coordination problem (action "
    "enumeration).** Traditional MAS coordination (GPGP, "
    "SharedPlans, organizational models) requires *explicit* "
    "action-space enumeration: designers must specify what agents "
    "*can do* and under what conditions. For open-ended artifact "
    "refinement, this enumeration is intractable -- the space of "
    "possible improvements is unbounded; no finite action language "
    "captures all valid patches. FMs eliminate this requirement: "
    "broad pretraining provides implicit coverage of improvement "
    "strategies across diverse domains without explicit action "
    "specification.",
    title="Synthesis (FM->MAS): FMs eliminate the action-enumeration requirement that previously blocked stigmergic coordination on open-ended refinement",
)

claim_mas_solves_output_combination = claim(
    "**MAS coordination solves a fundamental FM problem (output "
    "combination).** A single FM produces one response per query; "
    "scaling to complex artifacts requires orchestrating multiple "
    "generations. Current approaches use ad-hoc combination "
    "strategies (voting, ranking, chain-of-thought aggregation, "
    "human-in-the-loop selection). **Pressure-field coordination "
    "provides a principled framework: rather than voting on which "
    "response is 'best' or ranking by heuristic scores, the "
    "pressure gradient defines an *objective* criterion -- accept "
    "patches that reduce pressure, reject those that do not.** This "
    "explains why pressure-field outperforms conversation: dialogue "
    "is an ad-hoc combination strategy, while pressure-field "
    "replaces emergent consensus with objective gradients.",
    title="Synthesis (MAS->FM): pressure-field provides an objective output-combination criterion, replacing ad-hoc voting/dialogue/ranking",
)

# ---------------------------------------------------------------------------
# 7.8 Societal implications
# ---------------------------------------------------------------------------

claim_societal_accountability = claim(
    "**Societal concern: accountability diffusion.** When "
    "coordination emerges from shared pressure gradients rather "
    "than explicit delegation, attributing outcomes to individual "
    "agents becomes challenging. Multiple agents may contribute to "
    "a region through independent pressure-reducing actions, with "
    "no record of which agent 'owned' the outcome. **Mitigation**: "
    "pressure-field deployment in regulated domains must add "
    "audit-log infrastructure recording patch provenance, pressure "
    "signals at proposal time, and validation outcomes -- the "
    "coordination mechanism remains simple, but operational "
    "deployment adds logging.",
    title="Societal: accountability diffusion (no clear attribution); mitigation = audit-log infrastructure",
)

claim_societal_goodhart = claim(
    "**Societal concern: Goodhart's Law and metric gaming.** "
    "Pressure-field coordination is vulnerable to Goodhart's Law "
    "because agents are optimized to reduce designer-specified "
    "pressure. If those functions imperfectly capture true quality "
    "(and they inevitably do), agents will discover and exploit "
    "the mismatch (e.g., reducing complexity by splitting "
    "functions excessively, harming readability while improving "
    "the metric). FMs introduce second-order gaming: LLMs trained "
    "on internet-scale text may have implicit knowledge of how to "
    "game specific benchmarks. **Mitigation**: design pressure "
    "functions defensively with multiple orthogonal axes, "
    "adversarial sensors, and audit whether pressure reduction "
    "correlates with human quality judgment.",
    title="Societal: Goodhart-gaming risk (FM-amplified); mitigation = multiple orthogonal axes + adversarial sensors + human audit",
)

claim_societal_explainability = claim(
    "**Societal concern: explainability.** Hierarchical "
    "explanations follow delegation chains ('Manager X assigned "
    "task Y to Worker Z because condition C held'). Pressure-field "
    "explanations are mechanistically transparent but causally "
    "opaque: 'Region R had high pressure; agent A proposed patch "
    "Δ; pressure dropped by δ.' For domains where outcome "
    "verification is cheap (code formatting, resource "
    "optimization), the trade-off is acceptable; for high-stakes "
    "domains requiring human-stakeholder justification, "
    "hierarchical coordination remains necessary despite overhead.",
    title="Societal: explainability trade-off (mechanistically transparent but causally opaque); domain-dependent deployment",
)

# ---------------------------------------------------------------------------
# 8. Conclusion synthesis
# ---------------------------------------------------------------------------

claim_conclusion_synthesis = claim(
    "**Conclusion synthesis: implicit coordination outperforms "
    "explicit coordination for constraint-satisfaction tasks with "
    "locality.** Pressure-field achieves 48.5% aggregate solve rate "
    "-- nearly half of all problems solved through local pressure-"
    "following alone, with no coordinator, no message passing, no "
    "explicit task delegation. The 30x gap vs hierarchical and 4x "
    "gap vs conversation are highly significant ($p < 0.001$). "
    "**FMs' zero-shot capabilities eliminate the need for domain-"
    "specific action representations; pressure-field coordination "
    "eliminates the need for complex multi-agent protocols; "
    "together they enable simple MASs.**",
    title="Conclusion synthesis: implicit coordination beats explicit coordination on constraint-satisfaction with locality (FM + pressure-field together enable simple MAS)",
)

__all__ = [
    "claim_factor_1_coordination_overhead_harms",
    "claim_factor_2_locality_makes_greedy_effective",
    "claim_factor_3_parallel_validation_amplifies",
    "claim_hierarchical_rejection_loop",
    "claim_hierarchical_rejection_statistics",
    "claim_architectural_lesson",
    "claim_limitation_modest_hard_solve_rate",
    "claim_limitation_domain_specificity",
    "claim_other_practical_limitations",
    "claim_limitation_trajectory_level_risks",
    "claim_limitation_decay_miscalibration",
    "claim_when_pressure_field",
    "claim_when_hierarchical",
    "claim_fm_solves_action_enumeration",
    "claim_mas_solves_output_combination",
    "claim_societal_accountability",
    "claim_societal_goodhart",
    "claim_societal_explainability",
    "claim_conclusion_synthesis",
]
