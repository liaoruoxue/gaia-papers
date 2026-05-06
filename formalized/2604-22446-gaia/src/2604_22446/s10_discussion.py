"""Section 5: Discussion -- limitations, cost-performance trade-off,
broader implications + Section 6: Conclusion.

Source: Yu et al. 2026 [@Yu2026OMC], Sections 5-6 (page 20).

Note: The paper does NOT report quantitative ablations -- the authors
explicitly state self-evolution mechanisms have been deployed but not
yet ablated (Limitations).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Limitations (Section 5)
# ---------------------------------------------------------------------------

claim_limitation_only_prdbench_quant = claim(
    "**Limitation L1: quantitative evaluation is confined to "
    "PRDBench.** Quantitative results are only reported on "
    "PRDBench (50 software development tasks). Cross-domain case "
    "studies (content generation, game development, audiobook, "
    "research survey) demonstrate qualitative generality but "
    "systematic evaluation on non-coding benchmarks remains "
    "future work.",
    title="Limitation L1: only PRDBench quantitatively evaluated; non-coding benchmarks remain future work",
)

claim_limitation_self_evolution_not_ablated = claim(
    "**Limitation L2: self-evolution mechanisms are deployed but "
    "not quantitatively ablated.** The self-evolution mechanisms "
    "(one-on-ones, retrospectives, performance reviews) have been "
    "implemented and deployed, but not isolated for ablation. "
    "Isolating the contribution of each mechanism requires "
    "longitudinal studies across many projects -- explicitly "
    "called out as future work. *Therefore the paper does not "
    "report ablation tables for individual self-evolution "
    "components.*",
    title="Limitation L2: self-evolution mechanisms deployed but not quantitatively ablated (longitudinal studies needed)",
)

# ---------------------------------------------------------------------------
# Cost-performance trade-off
# ---------------------------------------------------------------------------

claim_cost_performance_tradeoff = claim(
    "**Cost-performance trade-off + adaptive dispatch.** OMC's "
    "multi-agent coordination incurs significant cost overhead "
    "(~$6.91 per PRDBench task). Justified for complex, project-"
    "level tasks where correctness matters more than token "
    "efficiency, but inappropriate for simple single-turn queries. "
    "OMC therefore introduces an **adaptive dispatch mode**: the "
    "CEO can route simple tasks to a single agent and reserve "
    "multi-agent coordination for tasks above a complexity "
    "threshold.",
    title="Trade-off: ~$6.91/task overhead justified above a complexity threshold; adaptive dispatch routes simple tasks to single agent",
)

# ---------------------------------------------------------------------------
# Broader implications + analogy
# ---------------------------------------------------------------------------

claim_human_enterprise_analogy_general = claim(
    "**Human-enterprise analogy is deliberately general.** The "
    "manage-plan-hire-learn pattern motivating OMC applies to any "
    "domain, not just software development. The four cross-domain "
    "case studies provide initial evidence of this generality. As "
    "the Talent Market grows and more agent families become "
    "available, the organisational layer should become *more* "
    "useful -- analogous to how operating systems gained "
    "importance as hardware diversity increased.",
    title="Implication: organisation-layer value increases with agent-family diversity (OS-kernel analogy at scale)",
)

# ---------------------------------------------------------------------------
# Conclusion (Section 6)
# ---------------------------------------------------------------------------

claim_conclusion_synthesis = claim(
    "**Conclusion synthesis.** AI organisation design -- the "
    "systematic structuring, coordination, and evolution of "
    "heterogeneous agent workforces -- is a missing layer in "
    "multi-agent research. OMC demonstrates that the "
    "organisational machinery of human companies transfers to "
    "this setting: the typed Talent-Container architecture + "
    "Talent Market handles workforce management; E2R tree search "
    "coordinates project execution through structured "
    "decomposition + review gates; the self-evolution pipeline "
    "closes the feedback loop through reflection, retrospectives, "
    "and formal HR processes. On PRDBench this combination yields "
    "84.67% (+15.48 pp) across multi-domain projects with "
    "long-horizon reasoning. Open questions: scaling, per-"
    "component contribution, and Talent Market growth beyond "
    "software.",
    title="Conclusion: organisation-machinery transfers to AI; PRDBench 84.67% (+15.48 pp); open questions on scale + per-component contribution + market growth",
)

claim_open_questions = claim(
    "**Open questions stated in Section 6.** "
    "(Q1) Whether OMC's advantage holds at larger scale (more "
    "tasks, more domains, more agent families). "
    "(Q2) How much each component (Talent-Container, Talent "
    "Market, E2R, self-evolution) contributes in isolation -- "
    "directly tied to Limitation L2 (no quantitative ablation "
    "yet). "
    "(Q3) How the Talent Market ecosystem should grow to cover "
    "domains beyond software development.",
    title="Open: (Q1) larger scale, (Q2) per-component contribution, (Q3) Talent Market growth beyond software",
)

# ---------------------------------------------------------------------------
# Predictions used in the central abduction (Section 11 wiring)
# ---------------------------------------------------------------------------

claim_pred_h_organisational_decoupling_drives = claim(
    "**Hypothesis prediction (organisational decoupling drives "
    "the gain).** If OMC's gain over fixed-team MAS is driven by "
    "the *organisational layer* (typed Talent-Container interfaces "
    "+ on-demand recruitment + dynamic decomposition + review-"
    "gated propagation), then the predicted fingerprint is: "
    "(F1) the gap holds against same-substrate Commercial agents "
    "(Claude Code, +28 pp); "
    "(F2) the gap holds across diverse model families in the "
    "Minimal panel (range +15 to +66 pp); "
    "(F3) cross-domain case studies (content / game / audiobook / "
    "research) succeed without framework changes, exercising the "
    "Container-Talent abstraction across model families; "
    "(F4) the game-development case shows the system *creates a "
    "new skill mid-project* in response to evaluator rejection -- "
    "a behaviour reachable only via the typed organisational "
    "layer.",
    title="Pred-H (organisational-decoupling): same-substrate gap + cross-family gap + cross-domain generality + mid-project skill creation",
)

claim_pred_alt_bigger_lm_or_more_compute = claim(
    "**Alternative prediction (bigger LM / better tools / more "
    "compute).** If the gain were primarily driven by larger LLM, "
    "better tools, or more compute, the predicted fingerprint "
    "would instead be: "
    "(A1) same-substrate gap should *vanish* when OMC's Claude "
    "Sonnet 4.6 backbone is matched against Claude-4.5 Minimal -- "
    "but the observed +15.48 pp gap persists; "
    "(A2) the gap should be *narrower* against Commercial agents "
    "(which have already invested in tooling and harness) than "
    "against Minimal LLMs -- but the observed gap against Claude "
    "Code (Commercial, same family) is +28 pp, *wider* than the "
    "+15 pp against Claude-4.5 Minimal; "
    "(A3) cross-domain case studies would require domain-specific "
    "scaffolding -- but the four cases reuse the *same* OMC "
    "framework with no modifications; "
    "(A4) mid-project skill creation in the game-development case "
    "is a behaviour outside what 'better LLM' alone would "
    "predict.",
    title="Pred-Alt (bigger-LM / better-tools / more-compute): predicts narrower commercial gap + same-substrate convergence + per-domain scaffolding",
)

claim_observed_fingerprint = claim(
    "**Observed fingerprint (Table 2 + Section 3.3).** "
    "(O1) Same-substrate Commercial gap is +28.02 pp (vs Claude "
    "Code) -- *wider* than the +15.48 pp Minimal gap; "
    "(O2) cross-family Minimal gaps span +15 to +66 pp; "
    "(O3) cross-domain case studies (content / game / audiobook / "
    "research) all succeed under the same OMC framework with no "
    "domain-specific modifications; "
    "(O4) the game-development case demonstrates mid-project "
    "skill creation triggered by evaluator rejection.",
    title="Observation: (O1) +28pp commercial > +15pp minimal, (O2) cross-family generality, (O3) framework-invariant cross-domain, (O4) mid-project skill creation",
)

# ---------------------------------------------------------------------------
# Counter-positions for the contradictions in s11
# ---------------------------------------------------------------------------

claim_omc_demonstration_dynamic_org_works = claim(
    "**OMC empirical demonstration: dynamic organisational layer "
    "works.** Across 50 PRDBench tasks under DEV mode + four "
    "single-prompt case studies, OMC's Talent-Container "
    "architecture + Talent Market + E2R tree search delivers "
    "84.67% (+15.48 pp) and four successful cross-domain "
    "deliveries. This is a concrete demonstration that on-demand "
    "organisational dynamics outperform fixed-team MAS *on the "
    "same task panel*, contradicting the implicit literature "
    "assumption that fixed team structures are sufficient.",
    title="Demonstration: dynamic organisational layer outperforms fixed-team MAS (84.67% on PRDBench + 4 cross-domain deliveries)",
)

claim_omc_typed_interfaces_demonstration = claim(
    "**OMC demonstration: typed-interface decoupling is "
    "feasible.** OMC deploys the six typed organisational "
    "interfaces across three Container families (LangGraph, "
    "Claude CLI, script-based) within a single dispatch loop, "
    "successfully orchestrating heterogeneous agents in PRDBench "
    "and four cross-domain case studies. This contradicts the "
    "implicit literature assumption that MAS coordination requires "
    "tightly coupled bespoke logic -- decoupling identity from "
    "runtime is not only possible but yields measurable gains.",
    title="Demonstration: typed-interface decoupling deployed in production (3 Container families + 4 case-study domains)",
)

__all__ = [
    "claim_limitation_only_prdbench_quant",
    "claim_limitation_self_evolution_not_ablated",
    "claim_cost_performance_tradeoff",
    "claim_human_enterprise_analogy_general",
    "claim_conclusion_synthesis",
    "claim_open_questions",
    "claim_pred_h_organisational_decoupling_drives",
    "claim_pred_alt_bigger_lm_or_more_compute",
    "claim_observed_fingerprint",
    "claim_omc_demonstration_dynamic_org_works",
    "claim_omc_typed_interfaces_demonstration",
]
