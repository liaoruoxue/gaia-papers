"""
Section 4.3-4.5: Ablations, Context Manager Choice, Management Frequency
==========================================================================

Three controlled studies isolate which ARC components and design choices matter:
- Section 4.3: which subsystem (incremental memory, checklist, reflection, full ARC) matters
- Section 4.4: how the choice of CM model affects performance, including a trained ARC-CM
- Section 4.5: per-turn vs delayed vs budget-triggered context management frequency
"""

from gaia.lang import claim, setting, support, contradiction

from .s3_methodology import (
    incremental_summarization,
    reflection_operator,
    cm_training_setup,
    incremental_preserves_evidence,
    reflection_enables_repair,
    decoupling_enables_reuse,
)

# ---------------------------------------------------------------------
# 4.3 Ablation studies
# ---------------------------------------------------------------------

ablation_setup = setting(
    "Ablation variants share the same Actor (Qwen2.5-32B-Instruct) so that performance "
    "differences isolate the impact of context-management components:\n\n"
    "- **Summary**: incremental online summarization only; no reflection; memory and checklist "
    "are never revised after initialization.\n"
    "- **Summary + Checklist**: reflection updates the checklist as a control signal; the "
    "interaction memory remains purely incremental and is never revised.\n"
    "- **Reflection + Checklist-Only**: reflection triggers when execution stalls and revises "
    "the checklist, but explicitly disables interaction-memory modification.\n"
    "- **ARC (Full)**: incremental construction + triggered reflection that *jointly* revises "
    "memory and checklist.",
    title="Ablation setup",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.3"},
)

table2_observation = claim(
    "Table 2 (averaged Pass@1 over GAIA / xBench-DS / BrowseComp-ZH; same Qwen2.5-32B Actor):\n\n"
    "| Variant | GAIA | xBench-DS | BrowseComp-ZH |\n"
    "|---|---|---|---|\n"
    "| Summary | 32.1 | 38.4 | 14.4 |\n"
    "| Summary + Checklist | 33.0 | 37.6 | 15.0 |\n"
    "| Reflection + Checklist-Only | 26.2 | 34.3 | 6.9 |\n"
    "| ARC (Full) | 34.9 | 40.7 | 18.0 |\n\n"
    "ARC (Full) is best on every benchmark. Summary+Checklist gives only marginal/inconsistent "
    "gains over Summary. The Reflection+Checklist-Only variant — which forbids memory revision — "
    "is *worse* than the Summary baseline on every benchmark, especially BrowseComp-ZH "
    "(6.9 vs 14.4).",
    title="Table 2 ablation results",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.3, Table 2"},
)

incremental_helps_baseline = claim(
    "Incremental summarization alone (the Summary variant) provides a meaningful and consistent "
    "baseline, stabilizing context length and preserving task-relevant evidence.",
    title="Incremental summarization helps as a baseline",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.3, Table 2"},
)

checklist_alone_marginal = claim(
    "Checklist-based reflection alone (without memory revision) yields only marginal or "
    "inconsistent gains over pure incremental summarization (Summary 32.1/38.4/14.4 vs "
    "Summary+Checklist 33.0/37.6/15.0; one benchmark slightly worse).",
    title="Checklist alone yields only marginal gains",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.3, Table 2"},
)

reflection_without_memory_harmful = claim(
    "Reflection that revises only the checklist while *forbidding* interaction-memory revision "
    "is harmful: Reflection+Checklist-Only is strictly worse than the pure-Summary baseline on "
    "all three benchmarks (GAIA 26.2 vs 32.1; xBench-DS 34.3 vs 38.4; BrowseComp-ZH 6.9 vs 14.4). "
    "Reflection without the ability to repair memory creates control/memory inconsistency that "
    "actively hurts performance.",
    title="Reflection without memory revision hurts performance",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.3, Table 2"},
)

joint_revision_required = claim(
    "ARC's strongest performance arises only when reflection *jointly* revises both interaction "
    "memory and checklist; the checklist is most valuable as part of a jointly revisable internal "
    "state, not as an isolated planning artifact.",
    title="Joint memory+checklist revision is required",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.3"},
)

# Counterfactual to be contradicted by the table
checklist_alone_strong = claim(
    "Checklist-based reflection alone (without interaction-memory revision) yields large, "
    "consistent improvements over pure incremental summarization.",
    title="(Counterfactual) Checklist alone is strong",
    metadata={"source": "Counterfactual to Table 2"},
)

# ---------------------------------------------------------------------
# 4.4 Context Manager choice
# ---------------------------------------------------------------------

cm_choice_setup = setting(
    "To isolate the role of the Context Manager, the Actor and execution loop are fixed and "
    "only the CM model varies. The trained ARC-CM uses Qwen3-14B as base.",
    title="CM-choice experiment setup",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.4"},
)

table3_observation = claim(
    "Table 3 (Pass@1 with fixed Actor, varying CM):\n\n"
    "| CM | HotpotQA | GAIA | xBench-DS |\n"
    "|---|---|---|---|\n"
    "| Qwen3-32B | 72.1 | 35.1 | 39.0 |\n"
    "| GPT-OSS-120B | 74.6 | 34.9 | 40.7 |\n"
    "| DeepSeek-v3.2 | 75.4 | 48.4 | 52.0 |\n"
    "| ARC-CM (trained, Qwen3-14B base) | 76.1 | 42.6 | 46.3 |\n\n"
    "ARC-CM (~14B) outperforms the much larger GPT-OSS-120B on every benchmark (76.1 vs 74.6, "
    "42.6 vs 34.9, 46.3 vs 40.7), and outperforms Qwen3-32B as well, while being substantially "
    "smaller. DeepSeek-v3.2 (a larger, stronger general model) still beats ARC-CM on GAIA and "
    "xBench-DS.",
    title="Table 3 CM-choice results",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.4, Table 3"},
)

cm_choice_matters = claim(
    "The choice of Context Manager consistently affects end-to-end performance, especially on "
    "long-horizon benchmarks (GAIA, xBench-DS), with measured spreads of >10 absolute Pass@1 "
    "points across CM choices.",
    title="CM choice materially affects performance",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.4, Table 3"},
)

cm_is_learnable = claim(
    "Context management is a *learnable* capability, not merely an emergent property of model "
    "scale: a trained ARC-CM with Qwen3-14B base outperforms substantially larger untrained "
    "models such as GPT-OSS-120B (~9x more parameters) across HotpotQA, GAIA, and xBench-DS.",
    title="Context management is learnable (ARC-CM beats GPT-OSS-120B)",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.4"},
)

# Counterfactual to be contradicted
cm_emergent_only = claim(
    "Context-management quality is purely an emergent property of CM scale, so a trained 14B CM "
    "cannot outperform a 120B untrained CM.",
    title="(Counterfactual) CM quality is purely emergent from scale",
    metadata={"source": "Counterfactual to Table 3"},
)

cm_lifts_actor_ceiling = claim(
    "Actively learned context management raises the effective reasoning ceiling of the Actor: "
    "the same Actor achieves better long-horizon performance with a smaller trained CM than with "
    "a much larger untrained CM, while reducing summarization and reflection cost during execution.",
    title="Trained CM raises effective reasoning ceiling",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.4"},
)

# ---------------------------------------------------------------------
# 4.5 Management frequency
# ---------------------------------------------------------------------

frequency_setup = setting(
    "The frequency study fixes the Actor, CM, tools, and context budget, varying only when "
    "summarization and reflection checks are performed: (i) **step-by-step** at every turn, "
    "(ii) **delayed** every 3 or 5 turns, and (iii) **budget-triggered** when context length "
    "exceeds 8k, 16k, or 32k tokens. All settings use the same interaction limits. Accuracy is "
    "averaged over GAIA, xBench-DeepSearch, and BrowseComp.",
    title="Management-frequency experiment setup",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.5"},
)

table4_observation = claim(
    "Table 4 (average accuracy over GAIA, xBench-DS, BrowseComp):\n\n"
    "| Strategy | Setting | Accuracy (%) |\n"
    "|---|---|---|\n"
    "| Step-by-step | Every turn | 31.2 |\n"
    "| Delayed | Every 3 turns | 26.5 |\n"
    "| Delayed | Every 5 turns | 24.5 |\n"
    "| Budget-triggered | 8k tokens | 27.1 |\n"
    "| Budget-triggered | 16k tokens | 24.4 |\n"
    "| Budget-triggered | 32k tokens | 24.6 |\n\n"
    "Per-turn step-by-step management (31.2) strictly beats every delayed and every "
    "budget-triggered alternative.",
    title="Table 4 frequency results",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.5, Table 4"},
)

per_turn_best = claim(
    "Per-turn (always-on) summarization and reflection-checking outperform both delayed (every "
    "3 or 5 turns) and budget-triggered (8k/16k/32k token thresholds) strategies on long-horizon "
    "information-seeking benchmarks. Per-turn updates preserve the most recent interaction's "
    "complete semantic information *before* abstraction or omission accumulates across multiple "
    "steps.",
    title="Per-turn management is best",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.5"},
)

delayed_loses_evidence = claim(
    "Delayed summarization must compress several interactions at once, increasing the risk that "
    "intermediate reasoning, failed attempts, or subtle evidence is lost or conflated.",
    title="Delayed summarization conflates evidence",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.5"},
)

budget_triggered_too_late = claim(
    "Budget-triggered strategies are reactive: by the time compression is applied, misleading "
    "assumptions or unproductive patterns may already have shaped subsequent decisions, "
    "preventing timely correction.",
    title="Budget-triggered strategies act too late",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.5"},
)

context_mgmt_is_semantic_alignment = claim(
    "Context management in long-horizon information seeking is not merely about reducing length "
    "but about maintaining a semantically faithful and task-aligned internal reasoning state. "
    "Always-on, per-turn updates with lightweight reflection checks prevent early deviations "
    "from compounding and enable timely correction.",
    title="Context management is about semantic alignment, not length",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.5"},
)

# Counterfactual
budget_triggered_best = claim(
    "Budget-triggered context management (compress only when tokens exceed a threshold) "
    "outperforms per-turn step-by-step management.",
    title="(Counterfactual) Budget-triggered is best",
    metadata={"source": "Counterfactual to Table 4"},
)

# ---------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------

# 4.3 strategies
strat_incremental_helps = support(
    [table2_observation],
    incremental_helps_baseline,
    background=[ablation_setup],
    reason=(
        "Table 2 (@table2_observation) shows the Summary variant achieves 32.1/38.4/14.4 — a "
        "meaningful and stable baseline well above zero on all three benchmarks. Since the "
        "Actor is fixed across variants (@ablation_setup), this isolates incremental "
        "summarization as the contributor to that baseline."
    ),
    prior=0.85,
)

strat_checklist_marginal = support(
    [table2_observation],
    checklist_alone_marginal,
    background=[ablation_setup],
    reason=(
        "Comparing Summary vs Summary+Checklist in Table 2 (@table2_observation): the "
        "differences are +0.9 (GAIA), -0.8 (xBench-DS), +0.6 (BrowseComp-ZH). One benchmark is "
        "even slightly worse, directly substantiating the marginal/inconsistent characterization."
    ),
    prior=0.9,
)

strat_reflection_without_memory_hurts = support(
    [table2_observation],
    reflection_without_memory_harmful,
    background=[ablation_setup, reflection_enables_repair],
    reason=(
        "Reflection+Checklist-Only in Table 2 (@table2_observation) achieves 26.2/34.3/6.9 "
        "vs Summary's 32.1/38.4/14.4 — strictly worse on every benchmark, and dramatically so on "
        "BrowseComp-ZH (less than half the accuracy). Without the ability to repair memory "
        "(@reflection_enables_repair), reflection-driven checklist updates create control/memory "
        "inconsistency that hurts the agent."
    ),
    prior=0.85,
)

strat_joint_revision = support(
    [table2_observation, reflection_without_memory_harmful, checklist_alone_marginal],
    joint_revision_required,
    background=[ablation_setup, reflection_operator],
    reason=(
        "ARC (Full) achieves the best score on every benchmark in Table 2 "
        "(@table2_observation). Neither memory revision alone (Summary, ~baseline) nor checklist "
        "revision alone (@checklist_alone_marginal, marginal; @reflection_without_memory_harmful, "
        "actively harmful) reproduces the full effect. Only the joint update, as specified by "
        "the reflection operator (@reflection_operator), realizes the full gain — directly "
        "supporting the joint-revision claim."
    ),
    prior=0.85,
)

strat_checklist_alone_strong_contra = contradiction(
    table2_observation,
    checklist_alone_strong,
    reason=(
        "Table 2 (@table2_observation) shows Summary+Checklist differs from Summary by less than "
        "1 absolute point on every benchmark (and is worse on xBench-DS), which directly "
        "contradicts the claim of large consistent improvement from checklist-only reflection."
    ),
    prior=0.95,
)

# 4.4 strategies
strat_cm_choice_matters = support(
    [table3_observation],
    cm_choice_matters,
    background=[cm_choice_setup],
    reason=(
        "With the Actor fixed (@cm_choice_setup), Table 3 (@table3_observation) shows GAIA "
        "scores of 35.1, 34.9, 48.4, 42.6 across CM choices — a 13.5-point spread. Such large "
        "variation in end-to-end performance from changing only the CM directly substantiates "
        "the claim that CM choice matters."
    ),
    prior=0.9,
)

strat_cm_is_learnable = support(
    [table3_observation],
    cm_is_learnable,
    background=[cm_choice_setup, cm_training_setup],
    reason=(
        "ARC-CM (Qwen3-14B base, ~14B params) beats GPT-OSS-120B (~120B params) on every "
        "benchmark in Table 3 (@table3_observation): 76.1>74.6, 42.6>34.9, 46.3>40.7. Because "
        "the Actor and execution loop are fixed (@cm_choice_setup), the only variable is the "
        "CM, and the smaller-but-trained model wins — supporting that learning, not scale, "
        "drives CM quality (@cm_training_setup)."
    ),
    prior=0.9,
)

strat_cm_emergent_contra = contradiction(
    table3_observation,
    cm_emergent_only,
    reason=(
        "Table 3 (@table3_observation) shows the trained 14B ARC-CM beating the untrained 120B "
        "GPT-OSS on all three benchmarks. If CM quality were purely emergent from scale, the "
        "120B model could not be beaten by the 14B model — a direct contradiction."
    ),
    prior=0.95,
)

strat_cm_raises_ceiling = support(
    [cm_is_learnable, table3_observation],
    cm_lifts_actor_ceiling,
    background=[cm_choice_setup, decoupling_enables_reuse],
    reason=(
        "Because the Actor is held fixed across CM choices (@cm_choice_setup) and a trained "
        "smaller CM yields strictly better end-to-end Actor performance than larger untrained "
        "CMs (@cm_is_learnable; numbers in @table3_observation), context management acts as a "
        "lever that raises the effective reasoning ceiling of the Actor, not a substitute for "
        "Actor capacity. The decoupled architecture (@decoupling_enables_reuse) makes this "
        "isolation rigorous."
    ),
    prior=0.8,
)

# 4.5 strategies
strat_per_turn_best = support(
    [table4_observation],
    per_turn_best,
    background=[frequency_setup, incremental_preserves_evidence],
    reason=(
        "Table 4 (@table4_observation) shows step-by-step (every turn) at 31.2% strictly above "
        "every delayed (26.5, 24.5) and every budget-triggered (27.1, 24.4, 24.6) alternative "
        "with all other variables held constant (@frequency_setup). This is consistent with the "
        "evidence-preservation rationale (@incremental_preserves_evidence)."
    ),
    prior=0.9,
)

strat_delayed_loses_evidence = support(
    [table4_observation],
    delayed_loses_evidence,
    background=[frequency_setup],
    reason=(
        "Delayed-3 (26.5) and Delayed-5 (24.5) in Table 4 (@table4_observation) are markedly "
        "below step-by-step (31.2), and the gap widens monotonically as the delay grows "
        "(31.2 -> 26.5 -> 24.5). This monotone degradation with delay length is the empirical "
        "signature predicted by the evidence-conflation explanation."
    ),
    prior=0.8,
)

strat_budget_too_late = support(
    [table4_observation],
    budget_triggered_too_late,
    background=[frequency_setup],
    reason=(
        "Budget-triggered variants (27.1, 24.4, 24.6 for 8k/16k/32k) all sit at or below "
        "Delayed-3 in Table 4 (@table4_observation) and well below per-turn (31.2). The "
        "reactive nature of budget triggers means context corrections cannot occur until after "
        "the threshold is crossed — by which point misalignment may have already shaped "
        "decisions."
    ),
    prior=0.75,
)

strat_semantic_alignment = support(
    [per_turn_best, delayed_loses_evidence, budget_triggered_too_late],
    context_mgmt_is_semantic_alignment,
    reason=(
        "If context management were purely about reducing length, budget-triggered strategies "
        "(which directly target length) would be at least competitive with per-turn updates. "
        "Instead, per-turn beats every length-targeted variant (@per_turn_best), delay loses "
        "evidence (@delayed_loses_evidence), and budget triggers are too late "
        "(@budget_triggered_too_late). Together, these support the reframing of context "
        "management as semantic alignment rather than length control."
    ),
    prior=0.8,
)

strat_budget_best_contra = contradiction(
    table4_observation,
    budget_triggered_best,
    reason=(
        "All three budget-triggered settings (8k=27.1, 16k=24.4, 32k=24.6) in Table 4 "
        "(@table4_observation) are below step-by-step (31.2). The claim that budget-triggered "
        "beats per-turn is directly contradicted by the table."
    ),
    prior=0.95,
)

__all__ = [
    # 4.3
    "ablation_setup",
    "table2_observation",
    "incremental_helps_baseline",
    "checklist_alone_marginal",
    "reflection_without_memory_harmful",
    "joint_revision_required",
    "checklist_alone_strong",
    # 4.4
    "cm_choice_setup",
    "table3_observation",
    "cm_choice_matters",
    "cm_is_learnable",
    "cm_emergent_only",
    "cm_lifts_actor_ceiling",
    # 4.5
    "frequency_setup",
    "table4_observation",
    "per_turn_best",
    "delayed_loses_evidence",
    "budget_triggered_too_late",
    "context_mgmt_is_semantic_alignment",
    "budget_triggered_best",
    # Strategies
    "strat_incremental_helps",
    "strat_checklist_marginal",
    "strat_reflection_without_memory_hurts",
    "strat_joint_revision",
    "strat_checklist_alone_strong_contra",
    "strat_cm_choice_matters",
    "strat_cm_is_learnable",
    "strat_cm_emergent_contra",
    "strat_cm_raises_ceiling",
    "strat_per_turn_best",
    "strat_delayed_loses_evidence",
    "strat_budget_too_late",
    "strat_semantic_alignment",
    "strat_budget_best_contra",
]
